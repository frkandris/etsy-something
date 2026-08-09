#!/usr/bin/env python3
"""Step 0b - build the depth map from REAL elevation data instead of an image model.

A topographic map is already a depth map: contour bands nest inside each other
exactly the way 02_trace.py needs. So for terrain subjects the image model is
not needed at all - the elevation raster IS the artwork, and every downstream
step (nesting, neck healing, keyhole, report) runs unchanged.

Source: AWS terrarium tiles (Mapzen/Nextzen heritage) - global, free, no key.
  elevation_m = (R * 256 + G + B / 256) - 32768

Usage:
  python 00b_terrain.py --lat 39.09 --lon -120.03 --km 40 --levels 6 \
      --out <dir> --name lake-tahoe [--shape circle]
"""
import argparse, io, math, pathlib, urllib.request
from PIL import Image, ImageDraw, ImageFilter

TILE = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def deg2tile(lat, lon, z):
    n = 2 ** z
    xt = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    yt = (1 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2 * n
    return xt, yt


def fetch(z, x, y):
    req = urllib.request.Request(TILE.format(z=z, x=x, y=y),
                                 headers={"User-Agent": "layered-map-pipeline"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))


def elevation_grid(lat, lon, km, zoom):
    """Stitch the tiles covering a km-square around (lat, lon), return elevations."""
    # metres per tile at this zoom and latitude
    m_per_tile = 156543.03392 * math.cos(math.radians(lat)) / (2 ** zoom) * 256
    half = (km * 1000.0) / 2.0 / m_per_tile          # in tile units
    cx, cy = deg2tile(lat, lon, zoom)
    x0, x1 = math.floor(cx - half), math.ceil(cx + half)
    y0, y1 = math.floor(cy - half), math.ceil(cy + half)
    n = (x1 - x0) * (y1 - y0)
    print(f"[dem] zoom {zoom}, {x1-x0}x{y1-y0} csempe ({n} letoltes)")
    canvas = Image.new("RGB", ((x1 - x0) * 256, (y1 - y0) * 256))
    for x in range(x0, x1):
        for y in range(y0, y1):
            try:
                canvas.paste(fetch(zoom, x, y), ((x - x0) * 256, (y - y0) * 256))
            except Exception as e:
                print(f"[dem] hianyzo csempe {x},{y}: {e}")
    # crop to the exact requested square
    px0 = int((cx - half - x0) * 256)
    py0 = int((cy - half - y0) * 256)
    side = int(2 * half * 256)
    return canvas.crop((px0, py0, px0 + side, py0 + side))


def to_depth_map(rgb, levels, shape, banding="quantile", size=2048):
    """Quantise elevation into `levels` nested bands + a frame, so the result is
    the same kind of image 00_generate produces: 0 = cut away, N = frontmost."""
    rgb = rgb.resize((size, size), Image.LANCZOS)
    px = rgb.load()
    els = []
    for j in range(size):
        row = []
        for i in range(size):
            r, g, b = px[i, j]
            row.append((r * 256 + g + b / 256) - 32768)
        els.append(row)
    # Quantile bands, not linear ones. A lake surface is a single elevation, so
    # linear banding puts most of the frame in one flat level and the product
    # reads as a blank disc. Equal-AREA bands give every layer real presence.
    flat = sorted(v for row in els for v in row[::5])
    if banding == "linear":
        # equal ELEVATION bands - correct for a peak, where the drama is in the
        # top few hundred metres. Quantile banding would flatten the summit
        # into one plate because it covers little area.
        lo = flat[int(len(flat) * 0.01)]
        hi = flat[int(len(flat) * 0.999)]
        cuts = [lo + (hi - lo) * (i + 1) / levels for i in range(levels)]
    else:
        # equal AREA bands - correct for flat terrain and lakes, where a single
        # elevation covers most of the frame
        cuts = [flat[int(len(flat) * (i + 1) / levels) - 1] for i in range(levels)]
    # collapse duplicate cuts (flat water) so a band is never empty
    ded = []
    for c in cuts:
        if not ded or c > ded[-1] + 0.5:
            ded.append(c)
    if len(ded) < levels:
        print(f"[dem] FIGYELEM: csak {len(ded)} elkulonitheto magassagi sav "
              f"({levels} kert) - tul lapos a terulet, valassz hegyesebb kozeppontot "
              f"vagy nagyobb --km ertekt")
    cuts = ded
    print(f"[dem] magassag {flat[0]:.0f}..{flat[-1]:.0f} m -> {len(cuts)} {banding} sav: "
          + ", ".join(f"{c:.0f}" for c in cuts))

    out = Image.new("L", (size, size), 0)
    op = out.load()
    step = 255 // max(1, len(cuts))
    import bisect
    for j in range(size):
        row = els[j]
        for i in range(size):
            k = bisect.bisect_left(cuts, row[i]) + 1
            op[i, j] = min(len(cuts), k) * step

    # frame: the outer band becomes background (cut away), giving the piece an
    # edge - without it every layer would be a full square with no silhouette
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    m = int(size * 0.06)
    if shape == "circle":
        md.ellipse([m, m, size - m, size - m], fill=255)
    else:
        md.rounded_rectangle([m, m, size - m, size - m], size // 40, fill=255)
    out = Image.composite(out, Image.new("L", (size, size), 0), mask)
    return out.filter(ImageFilter.MedianFilter(5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--km", type=float, default=40.0)
    ap.add_argument("--zoom", type=int, default=10)
    ap.add_argument("--levels", type=int, default=6)
    ap.add_argument("--shape", default="circle", choices=["circle", "square"])
    ap.add_argument("--banding", default="quantile", choices=["quantile", "linear"],
                    help="quantile: sik terep/to; linear: hegycsucs")
    ap.add_argument("--name", default="terrain")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rgb = elevation_grid(a.lat, a.lon, a.km, a.zoom)
    dm = to_depth_map(rgb, a.levels, a.shape, a.banding)
    p = out / f"raw_{a.name}_0.png"
    dm.save(p)
    print(f"[dem] kesz: {p}  ({a.km:.0f} km, {a.lat:.4f},{a.lon:.4f})")


if __name__ == "__main__":
    main()
