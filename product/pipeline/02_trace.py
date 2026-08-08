#!/usr/bin/env python3
"""Step 2 - depth map -> cuttable layers.

  posterise to N levels
    -> level k mask = everything at depth >= k   (nested, so each layer is a
       solid plate, never a ring of loose islands)
    -> potrace each mask straight to GeoJSON
    -> shapely: repair, drop specks, drop pinholes, measure the narrowest web
    -> SVG + DXF per layer, plus a safety report

The repair and the safety report are the point. An AI illustration is full of
hairline detail that looks fine on screen and snaps off on the cutting bed;
this step finds it and either thickens it or tells you it is still too thin.
"""
import json, math, subprocess, tempfile, pathlib, argparse
from PIL import Image, ImageDraw, ImageFilter
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

MM = 300.0          # finished diameter
MIN_WEB = 2.0       # mm - narrowest material we accept
MIN_PART = 400.0    # mm2 - smaller pieces stay one plate back, not glued separately
MIN_HOLE = 4.0      # mm^2 - drop pinholes smaller than this


def posterise(img, levels):
    """1-D k-means on the grey histogram -> levels+1 clusters (0 = background).

    Fixed-width bands would be wrong: an AI illustration puts its tones where it
    wants them, not on an even ladder, and the background is a huge spike at 0.
    """
    g = img.convert("L").filter(ImageFilter.MedianFilter(5))
    hist = g.histogram()
    k = levels + 1
    cent = [i * 255 / (k - 1) for i in range(k)]
    for _ in range(60):
        tot = [0.0] * k
        cnt = [0.0] * k
        for v, n in enumerate(hist):
            if not n:
                continue
            j = min(range(k), key=lambda i: abs(v - cent[i]))
            tot[j] += v * n
            cnt[j] += n
        new = [tot[i] / cnt[i] if cnt[i] else cent[i] for i in range(k)]
        if max(abs(a - b) for a, b in zip(new, cent)) < 0.25:
            cent = new
            break
        cent = new
    cent.sort()
    # threshold between cluster i-1 and i
    edges = [0.0] + [(cent[i - 1] + cent[i]) / 2 for i in range(1, k)]
    return g, edges, cent


def mask_at(g, thr):
    """Everything at or above this depth -> a nested plate.

    Black = material for potrace, so material must be painted black here.
    """
    return g.point(lambda v: 0 if v >= thr else 255).convert("1")


def trace(mask):
    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        mask.save(t / "m.pbm")
        subprocess.run(["potrace", "-b", "geojson", "-a", "1.0", "-t", "4",
                        "-o", str(t / "m.json"), str(t / "m.pbm")], check=True)
        gj = json.loads((t / "m.json").read_text())
    polys = []
    for f in gj.get("features", []):
        try:
            g = shape(f["geometry"])
        except Exception:
            continue
        if g.is_valid and g.geom_type in ("Polygon", "MultiPolygon"):
            polys.append(g if g.is_valid else g.buffer(0))
    return unary_union(polys) if polys else None


def clean(geom, scale, thicken, min_part, height):
    """Repair, thicken hairlines, drop specks and pinholes. Units: mm.

    Dropping a small piece is lossless in silhouette: the masks are nested, so
    every piece of layer k already sits inside layer k-1. A dropped piece just
    stays one plate further back instead of becoming a separate chip to glue.
    """
    if geom is None or geom.is_empty:
        return None
    # One fixed transform for every layer, derived from the image extent - never
    # from each layer's own bounding box, or the layers would not register.
    g = affinity.scale(geom, xfact=scale, yfact=-scale, origin=(0, 0))
    g = affinity.translate(g, 0, height)
    g = g.buffer(0)
    if thicken > 0:                       # close hairline gaps, then shrink back
        g = g.buffer(thicken).buffer(-thicken * 0.65)
    parts = [p for p in (g.geoms if g.geom_type == "MultiPolygon" else [g])
             if p.area >= min_part]
    if not parts:
        return None
    out = []
    for p in parts:
        holes = [r for r in p.interiors if Polygon(r).area >= MIN_HOLE]
        out.append(Polygon(p.exterior, holes))
    # potrace emits a vertex per pixel; 0.12 mm is far below any cutter's
    # tolerance and shrinks the delivered files by an order of magnitude
    return unary_union(out).simplify(0.12).buffer(0)


def parts_of(geom):
    return list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]


def widest_inscribed(p):
    """Thickest point of one piece, by erosion bisection."""
    lo, hi = 0.0, 12.0
    for _ in range(16):
        mid = (lo + hi) / 2
        if p.buffer(-mid / 2).is_empty:
            hi = mid
        else:
            lo = mid
    return lo


def frailest(geom):
    """The flimsiest cut piece on the sheet: min over pieces of their thickest
    point. A piece whose *widest* spot is under MIN_WEB is a sliver end to end."""
    return min(widest_inscribed(p) for p in parts_of(geom))


def thin_area(geom, w):
    """How much of the piece is thinner than w - the bit that snaps off."""
    keep = geom.buffer(-w / 2).buffer(w / 2)
    return max(0.0, geom.area - keep.area) / geom.area if geom.area else 0.0


def d_of(geom):
    d = []
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        for ring in [g.exterior] + list(g.interiors):
            pts = list(ring.coords)
            d.append("M " + " L ".join("%.3f %.3f" % p for p in pts) + " Z")
    return " ".join(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--levels", type=int, default=6)
    ap.add_argument("--thicken", type=float, default=0.6, help="mm, hairline repair")
    ap.add_argument("--min-part", type=float, default=MIN_PART,
                    help="mm2, below this a piece is left one plate further back")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    out = pathlib.Path(a.out or src.parent / "layers"); out.mkdir(parents=True, exist_ok=True)
    img = Image.open(src)
    scale = MM / img.width
    g, edges, cent = posterise(img, a.levels)

    print(f"forras: {src.name}  {img.width}x{img.height}px -> {MM:.0f} mm")
    print("tonusszintek: " + ", ".join(f"{c:.0f}" for c in cent))
    print(f"\n{'reteg':>6}{'darab':>7}{'lyuk':>6}{'terulet mm2':>13}{'leggyengebb':>14}"
          f"{'vekony%':>9}  statusz")
    rows = []
    for k in range(1, a.levels + 1):
        geom = clean(trace(mask_at(g, edges[k])), scale, a.thicken, a.min_part,
                     img.height * scale)
        if geom is None:
            print(f"{k:>6}{'-':>7}{'-':>6}{'-':>13}{'-':>14}{'-':>9}  URES")
            continue
        pieces = parts_of(geom)
        holes = sum(len(p.interiors) for p in pieces)
        nw = frailest(geom)
        ta = thin_area(geom, MIN_WEB)
        ok = nw >= MIN_WEB and ta < 0.06
        st = "OK" if ok else ("TORIK" if nw < MIN_WEB else "VEKONY RESZEK")
        print(f"{k:>6}{len(pieces):>7}{holes:>6}{geom.area:>13,.0f}{nw:>13.2f}mm"
              f"{ta*100:>8.1f}%  {st}")
        rows.append((k, geom, len(pieces), holes, nw, ta))

        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{MM}mm" height="{MM}mm" '
               f'viewBox="0 0 {MM} {MM}">\n  <path d="{d_of(geom)}" fill-rule="evenodd" '
               f'fill="none" stroke="#000" stroke-width="0.3"/>\n</svg>\n')
        (out / f"layer_{k}_of_{a.levels}.svg").write_text(svg)

        e = ["0", "SECTION", "2", "ENTITIES"]
        for gg in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
            for ring in [gg.exterior] + list(gg.interiors):
                e += ["0", "POLYLINE", "8", "CUT", "66", "1", "70", "1"]
                for x, y in ring.coords:
                    e += ["0", "VERTEX", "8", "CUT", "10", f"{x:.4f}", "20", f"{y:.4f}"]
                e += ["0", "SEQEND"]
        e += ["0", "ENDSEC", "0", "EOF"]
        (out / f"layer_{k}_of_{a.levels}.dxf").write_text("\n".join(e) + "\n")

    # stacked preview
    tones = ["#6b4f33", "#7b5d3e", "#8b6b49", "#9b7955", "#ab8761", "#bb956d", "#cba379"]
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{MM}mm" height="{MM}mm" '
         f'viewBox="0 0 {MM} {MM}">\n  <rect width="{MM}" height="{MM}" fill="#ece2d3"/>\n')
    for k, geom, *_ in rows:
        o = (k - 1) * 1.0
        s += (f'  <g transform="translate({-o:.2f},{-o:.2f})"><path d="{d_of(geom)}" '
              f'fill-rule="evenodd" fill="{tones[(k-1) % len(tones)]}" stroke="#3d2e1e" '
              f'stroke-width="0.25"/></g>\n')
    s += "</svg>\n"
    (out / "preview_stacked.svg").write_text(s)

    # raster preview - no SVG renderer needed to eyeball the result.
    # Each layer is composited through its OWN mask (holes transparent), so the
    # layers underneath show through the cut-outs. That see-through depth is the
    # entire product, so painting holes with the background colour would hide
    # exactly the thing we need to judge.
    P = 1400
    sc = P / MM
    prev = Image.new("RGB", (P, P), (236, 226, 211))
    for k, geom, *_ in rows:
        o = (k - 1) * 1.0 * sc
        col = tuple(int(tones[(k - 1) % len(tones)][i:i + 2], 16) for i in (1, 3, 5))
        mask = Image.new("L", (P, P), 0)
        md = ImageDraw.Draw(mask)
        for gg in parts_of(geom):
            md.polygon([(x * sc - o, y * sc - o) for x, y in gg.exterior.coords], fill=255)
            for ring in gg.interiors:
                md.polygon([(x * sc - o, y * sc - o) for x, y in ring.coords], fill=0)
        prev.paste(Image.new("RGB", (P, P), col), (0, 0), mask)
    prev.save(out / "preview_stacked.png")
    print(f"\nkiirva: {out}  ({len(list(out.iterdir()))} fajl)")


if __name__ == "__main__":
    main()
