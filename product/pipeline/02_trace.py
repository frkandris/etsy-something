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
from shapely.geometry import shape, Polygon, MultiPolygon, Point
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
    hi = max(v for v, n in enumerate(hist) if n)
    if hi <= levels + 2:            # index map (01_illustrate writes 0..N) -> spread to 0..255
        g = g.point(lambda v: min(255, v * (255 // max(1, hi))))
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
    if any(c == 0 for c in cnt):
        raise SystemExit(f"a kep csak {sum(1 for c in cnt if c)} tonust hasznal, "
                         f"{k} kell - futtasd kevesebb --levels ertekkel")
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
        if g.geom_type in ("Polygon", "MultiPolygon"):
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
        # a pinhole filter must not eat long narrow slots: a 10 x 0.3 mm cut is
        # only 3 mm^2 but is a real design feature, so gate on extent, not area
        holes = [r for r in p.interiors
                 if Polygon(r).area >= MIN_HOLE or _extent(r) >= 2.5]
        out.append(Polygon(p.exterior, holes))
    # potrace emits a vertex per pixel; 0.12 mm is far below any cutter's
    # tolerance and shrinks the delivered files by an order of magnitude
    return unary_union(out).simplify(0.12).buffer(0)


def parts_of(geom):
    return list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]


def _extent(ring):
    minx, miny, maxx, maxy = Polygon(ring).bounds
    return max(maxx - minx, maxy - miny)


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
    """min over pieces of their thickest point - catches end-to-end slivers.
    Does NOT catch a thin neck between two fat blobs; necks() does that."""
    return min(widest_inscribed(p) for p in parts_of(geom))


def necks(geom):
    """Count thin necks: places where eroding by MIN_WEB/2 splits one piece
    into several substantial fragments. A dumbbell with a 0.2 mm bridge has a
    fat widest-point on both sides, so frailest() alone would pass it - this
    is the check that fails it instead."""
    n = 0
    for p in parts_of(geom):
        er = p.buffer(-MIN_WEB / 2)
        if er.is_empty:
            continue
        frags = [f for f in parts_of(er) if f.area >= MIN_PART / 4]
        if len(frags) > 1:
            n += len(frags) - 1
    return n


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


def heal_necks(geom, clip=None):
    """Locally widen thin bridges to a safe width. Only zones that CONNECT two
    substantial fragments are bridges - an ornate piece is full of thin edge
    detail that must not be ballooned. Additions are clipped to the plate
    behind so the nesting guarantee survives the repair."""
    healed = []
    for p in parts_of(geom):
        er = p.buffer(-MIN_WEB / 2)
        frags = [f for f in parts_of(er) if f.area >= MIN_PART / 4]
        if len(frags) <= 1:
            healed.append(p)
            continue
        fat_parts = [f.buffer(MIN_WEB / 2 + 0.05) for f in frags]
        neck_zone = p.difference(unary_union(fat_parts))
        bridges = [nz for nz in parts_of(neck_zone)
                   if sum(1 for fp in fat_parts if nz.distance(fp) < 0.1) >= 2]
        if bridges:
            p = unary_union([p] + [b.buffer(MIN_WEB * 0.9) for b in bridges]).buffer(0)
        healed.append(p)
    out = unary_union(healed)
    if clip is not None:
        out = out.intersection(clip).buffer(0)
    return out


def keyhole(geom):
    """Cut a keyhole hanger into the back plate: 7 mm entry circle + 3.5 mm
    slot rising to a small circle. Scans down from the top edge for the first
    spot with 3 mm of solid material around the hole - an ornate silhouette's
    upper band is often lace, not plate."""
    minx, miny, maxx, maxy = geom.bounds
    cx = (minx + maxx) / 2
    for dy in range(14, 70, 4):
        for dx in (0, -8, 8, -16, 16):
            ex, ey = cx + dx, miny + dy
            entry = Point(ex, ey).buffer(3.5, 64)
            slot = Polygon([(ex - 1.75, ey - 10), (ex + 1.75, ey - 10),
                            (ex + 1.75, ey), (ex - 1.75, ey)])
            top = Point(ex, ey - 10).buffer(1.75, 32)
            hole = unary_union([entry, slot, top])
            if geom.contains(hole.buffer(3.0)):
                print(f"[i] kulcslyuk: ({ex - minx:.0f}, {dy}) mm a bal-felso saroktol")
                return geom.difference(hole)
    print("[!] kulcslyuk kihagyva - nincs eleg tomor anyag a felso savban")
    return geom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--levels", type=int, default=6)
    ap.add_argument("--thicken", type=float, default=0.6, help="mm, hairline repair")
    ap.add_argument("--min-part", type=float, default=MIN_PART,
                    help="mm2, below this a piece is left to the plate behind")
    ap.add_argument("--no-keyhole", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    out = pathlib.Path(a.out or src.parent / "layers"); out.mkdir(parents=True, exist_ok=True)
    for stale in out.glob("layer_*.*"):    # a failed level must not be masked
        stale.unlink()                     # by a file from an earlier run
    img = Image.open(src)
    scale = MM / img.width
    g, edges, cent = posterise(img, a.levels)

    print(f"forras: {src.name}  {img.width}x{img.height}px")
    print("tonusszintek: " + ", ".join(f"{c:.0f}" for c in cent))

    # pass 1: trace + clean every level
    geoms = {}
    for k in range(1, a.levels + 1):
        geom = clean(trace(mask_at(g, edges[k])), scale, a.thicken, a.min_part,
                     img.height * scale)
        if geom is not None:
            geoms[k] = geom
    if 1 not in geoms:
        raise SystemExit("az 1. reteg (hatlap) ures - hasznalhatatlan bemenet")

    # pass 2: scale FIRST, so every mm threshold below (min_part, MIN_WEB,
    # neck healing) operates on the final physical size. The object (back
    # plate bbox), not the image canvas, is exactly MM wide - the listing
    # promises the finished size.
    minx, miny, maxx, maxy = geoms[1].bounds
    f = MM / max(maxx - minx, maxy - miny)
    for k in geoms:
        gk = affinity.scale(geoms[k], xfact=f, yfact=f, origin=(0, 0))
        geoms[k] = affinity.translate(gk, -minx * f, -miny * f)

    # pass 3: independent potrace runs + simplify break exact nesting, so
    # enforce it: each layer is clipped to the final layer behind it. This is
    # what makes the MIN_PART argument true - a dropped piece's footprint is
    # guaranteed to be present on the plate behind. Healing widens necks and
    # can leave clip-slivers, so alternate the two until stable.
    def enforce_nesting():
        for k in sorted(geoms)[1:]:
            prev = geoms.get(k - 1)
            if prev is None:
                continue
            clipped = geoms[k].intersection(prev).buffer(0)
            clipped = unary_union([p for p in parts_of(clipped)
                                   if p.area >= a.min_part])
            if clipped.is_empty:
                del geoms[k]
            else:
                geoms[k] = clipped

    def heal_all():
        for k in sorted(geoms):
            geoms[k] = heal_necks(geoms[k], clip=geoms.get(k - 1))

    # the clip is what CREATES necks (it cuts pieces at the previous layer's
    # boundary), so the chain must END on a heal, never on a clip
    enforce_nesting()
    heal_all()
    enforce_nesting()
    heal_all()

    if not a.no_keyhole:
        geoms[1] = keyhole(geoms[1])

    print(f"objektum: {MM:.0f} mm (a hatlap befoglaloja, nem a vaszon)")
    print(f"\n{'reteg':>6}{'darab':>7}{'lyuk':>6}{'terulet mm2':>13}{'leggyengebb':>14}"
          f"{'vekony%':>9}{'nyak':>6}  statusz")
    rows = []
    for k in sorted(geoms):
        geom = geoms[k]
        pieces = parts_of(geom)
        holes = sum(len(p.interiors) for p in pieces)
        nw = frailest(geom)
        ta = thin_area(geom, MIN_WEB)
        nk = necks(geom)
        ok = nw >= MIN_WEB and ta < 0.02 and nk == 0
        st = "OK" if ok else ("TORIK" if nw < MIN_WEB else
                              "NYAK" if nk else "VEKONY RESZEK")
        print(f"{k:>6}{len(pieces):>7}{holes:>6}{geom.area:>13,.0f}{nw:>13.2f}mm"
              f"{ta*100:>8.2f}%{nk:>6}  {st}")
        rows.append((k, geom, len(pieces), holes, nw, ta))

        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{MM}mm" height="{MM}mm" '
               f'viewBox="0 0 {MM} {MM}">\n  <path d="{d_of(geom)}" fill-rule="evenodd" '
               f'fill="none" stroke="#000" stroke-width="0.3"/>\n</svg>\n')
        (out / f"layer_{k}_of_{a.levels}.svg").write_text(svg)

        # R12 with an explicit version header, mm units and a declared CUT
        # layer - LightBurn imports an unitless DXF at a guessed scale, and a
        # strict reader may reject an undeclared layer.
        e = ["0", "SECTION", "2", "HEADER",
             "9", "$ACADVER", "1", "AC1009",
             "9", "$INSUNITS", "70", "4",
             "0", "ENDSEC",
             "0", "SECTION", "2", "TABLES",
             "0", "TABLE", "2", "LAYER", "70", "1",
             "0", "LAYER", "2", "CUT", "70", "0", "62", "7", "6", "CONTINUOUS",
             "0", "ENDTAB", "0", "ENDSEC",
             "0", "SECTION", "2", "ENTITIES"]
        for gg in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
            for ring in [gg.exterior] + list(gg.interiors):
                e += ["0", "POLYLINE", "8", "CUT", "66", "1", "70", "1",
                      "10", "0.0", "20", "0.0", "30", "0.0"]
                pts = list(ring.coords)
                if len(pts) > 1 and pts[0] == pts[-1]:
                    pts = pts[:-1]        # 70=1 closes the loop; a repeated
                for x, y in pts:          # point would add a zero-length edge
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

    # assembly guide: one panel per layer, the fresh layer in orange on top of
    # the stack so far - answers "where do the loose front pieces go"
    PW = 700
    sc2 = PW / MM
    cols = 3
    rows_n = (len(rows) + cols - 1) // cols
    guide = Image.new("RGB", (PW * cols, (PW + 46) * rows_n), (250, 247, 242))
    gd = ImageDraw.Draw(guide)

    def draw_geom(target, geom, colour, ox, oy):
        mask = Image.new("L", (PW, PW), 0)
        md = ImageDraw.Draw(mask)
        for gg in parts_of(geom):
            md.polygon([(x * sc2, y * sc2) for x, y in gg.exterior.coords], fill=255)
            for ring in gg.interiors:
                md.polygon([(x * sc2, y * sc2) for x, y in ring.coords], fill=0)
        target.paste(Image.new("RGB", (PW, PW), colour), (ox, oy), mask)

    for i, (k, geom, *_x) in enumerate(rows):
        ox, oy = (i % cols) * PW, (i // cols) * (PW + 46)
        for k2, geom2, *_y in rows[:i]:
            draw_geom(guide, geom2, (196, 181, 160), ox, oy)
        draw_geom(guide, geom, (214, 116, 40), ox, oy)
        gd.text((ox + 12, oy + PW + 8), f"{k}. reteg", fill=(60, 50, 40))
    guide.save(out / "assembly_guide.png")
    print(f"\nkiirva: {out}  ({len(list(out.iterdir()))} fajl)")


if __name__ == "__main__":
    main()
