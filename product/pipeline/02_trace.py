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
MIN_FRAG = 20.0     # mm^2 - a region this big hanging on a thin neck is a defect


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
        return None, None
    # One fixed transform for every layer, derived from the image extent - never
    # from each layer's own bounding box, or the layers would not register.
    g = affinity.scale(geom, xfact=scale, yfact=-scale, origin=(0, 0))
    g = affinity.translate(g, 0, height)
    g = g.buffer(0)
    # narrow slots (a 10 x 0.3 mm cut) are design features the closing pass
    # below would seal shut - collect them first, re-cut them after
    slots = [Polygon(r) for p in parts_of(g) for r in p.interiors
             if _extent(r) >= 2.5 and Polygon(r).buffer(-0.8).is_empty]
    if thicken > 0:                       # close hairline gaps, then shrink back
        g = g.buffer(thicken).buffer(-thicken * 0.65)
        if slots:
            g = g.difference(unary_union(slots)).buffer(0)
    kept, dropped = [], []
    for p in parts_of(g):
        (kept if p.area >= min_part else dropped).append(p)
    if not kept:
        return None, None
    out = []
    for p in kept:
        # a pinhole filter must not eat long narrow slots: gate on extent too
        holes = [r for r in p.interiors
                 if Polygon(r).area >= MIN_HOLE or _extent(r) >= 2.5]
        out.append(Polygon(p.exterior, holes))
    # potrace emits a vertex per pixel; 0.12 mm is far below any cutter's
    # tolerance and shrinks the delivered files by an order of magnitude
    final = unary_union(out).simplify(0.12).buffer(0)
    return final, (unary_union(dropped) if dropped else None)


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
        frags = [f for f in parts_of(er) if f.area >= MIN_FRAG]
        if len(frags) > 1:
            n += len(frags) - 1
    return n


def thin_limbs(p, frags):
    """Long thin protrusions (a 30 x 1.5 mm tail) that erosion removes without
    splitting the piece - the neck detector is blind to them. Returns the
    zones worth widening: long and substantial, not decorative tips."""
    fat = unary_union([f.buffer(MIN_WEB / 2 + 0.05) for f in frags]) if frags \
        else None
    if fat is None:
        return []
    zone = p.difference(fat)
    return [z for z in parts_of(zone)
            if _extent(z.exterior) >= 6.0 and z.area >= 15.0]


def thin_area(geom, w):
    """How much of the piece is thinner than w - the bit that snaps off."""
    keep = geom.buffer(-w / 2).buffer(w / 2)
    return max(0.0, geom.area - keep.area) / geom.area if geom.area else 0.0


def d_of(geom):
    d = []
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        for ring in [g.exterior] + list(g.interiors):
            pts = ["%.3f %.3f" % p for p in ring.coords]
            # dedupe after rounding and drop the explicit closing point - the
            # Z command closes the path, a repeated point is a zero-length edge
            dd = [q for i, q in enumerate(pts) if i == 0 or q != pts[i - 1]]
            if len(dd) > 1 and dd[0] == dd[-1]:
                dd = dd[:-1]
            d.append("M " + " L ".join(dd) + " Z")
    return " ".join(d)


def heal_necks(geom, clip=None):
    """Locally widen thin bridges to a safe width. Only zones that CONNECT two
    substantial fragments are bridges - an ornate piece is full of thin edge
    detail that must not be ballooned. Additions are clipped to the plate
    behind so the nesting guarantee survives the repair."""
    pieces = parts_of(geom)
    healed, all_adds = [], []
    for i, p in enumerate(pieces):
        er = p.buffer(-MIN_WEB / 2)
        frags = [f for f in parts_of(er) if f.area >= MIN_FRAG]
        if len(frags) <= 1:
            limbs = thin_limbs(p, frags)
            if limbs:
                add = unary_union([z.buffer(MIN_WEB * 0.6) for z in limbs])
                others = [q for j, q in enumerate(pieces) if j != i] + all_adds
                if others:
                    add = add.difference(unary_union(others).buffer(0.6))
                all_adds.append(add)
                p = unary_union([p, add]).buffer(0)
            healed.append(p)
            continue
        fat_parts = [f.buffer(MIN_WEB / 2 + 0.05) for f in frags]
        neck_zone = p.difference(unary_union(fat_parts))
        bridges = [nz for nz in parts_of(neck_zone)
                   if sum(1 for fp in fat_parts if nz.distance(fp) < 0.1) >= 2]
        bridges += thin_limbs(p, frags)      # widen long thin tails too
        if not bridges:
            # a neck shorter than the fragments' dilation has no zone of its
            # own - patch the meeting point of every close fragment pair
            for i1 in range(len(frags)):
                for i2 in range(i1 + 1, len(frags)):
                    if frags[i1].distance(frags[i2]) < MIN_WEB + 0.3:
                        lens = frags[i1].buffer(MIN_WEB * 0.8).intersection(
                               frags[i2].buffer(MIN_WEB * 0.8))
                        if not lens.is_empty:
                            bridges.append(lens)
        if bridges:
            add = unary_union([b.buffer(MIN_WEB * 0.6) for b in bridges])
            # a repair must never fuse two separate pieces - avoid every other
            # piece AND every addition a previous piece already made (two
            # repairs growing into the same 1 mm gap would meet in the middle)
            others = [q for j, q in enumerate(pieces) if j != i] + all_adds
            if others:
                add = add.difference(unary_union(others).buffer(0.6))
            all_adds.append(add)
            p = unary_union([p, add]).buffer(0)
        healed.append(p)
    out = unary_union(healed)
    if clip is not None:
        out = out.intersection(clip).buffer(0)
    # amputation fallback: a neck that could not be widened (usually because
    # the plate behind has a hole exactly there, so the clip removed the
    # repair) is resolved by cutting the SMALL limb off at the neck - its
    # footprint stays visible on the plate behind, same as any demoted piece.
    # A neck between two LARGE regions is left alone and fails the report.
    final = []
    for p in parts_of(out):
        er = p.buffer(-MIN_WEB / 2)
        frags = [f for f in parts_of(er) if f.area >= MIN_FRAG]
        if len(frags) > 1:
            small = [f for f in frags if f.area < MIN_PART]
            big = [f for f in frags if f.area >= MIN_PART]
            small = sorted((f for f in small if f.area <= 60.0),
                           key=lambda f: f.area)
            total = 0.0
            capped = []
            for f in small:          # 60 mm2 is the TOTAL amputation budget
                if total + f.area > 60.0:
                    break
                total += f.area
                capped.append(f)
            small = capped
            if big and small:
                # cap: anything bigger than a fingertip is a design element -
                # removing it silently would hide damage, so leave it and let
                # the report fail instead
                cut = unary_union([f.buffer(MIN_WEB / 2 + 0.25) for f in small])
                p = p.difference(cut).buffer(0)
                p = unary_union([q for q in parts_of(p) if q.area >= MIN_FRAG])
                if not p.is_empty:
                    print(f"[i] amputalva {len(small)} gyogyithatatlan nyakon "
                          f"logo kis vegtag ({sum(f.area for f in small):.0f} mm2)")
        if not p.is_empty:
            final.append(p)
    return unary_union(final) if final else out


def keyhole(geom):
    """Cut a keyhole hanger into the back plate: 7 mm entry circle + 3.5 mm
    slot rising to a small circle. Scans down from the top edge for the first
    spot with 3 mm of solid material around the hole - an ornate silhouette's
    upper band is often lace, not plate."""
    minx, miny, maxx, maxy = geom.bounds
    cx = geom.centroid.x        # hang point off the centroid = the piece tilts
    best = None
    for dy in range(14, 70, 4):
        for dx in (0, -4, 4, -8, 8, -12, 12, -16, 16):
            ex, ey = cx + dx, miny + dy
            entry = Point(ex, ey).buffer(3.5, 64)
            slot = Polygon([(ex - 1.75, ey - 10), (ex + 1.75, ey - 10),
                            (ex + 1.75, ey), (ex - 1.75, ey)])
            top = Point(ex, ey - 10).buffer(1.75, 32)
            hole = unary_union([entry, slot, top])
            if geom.contains(hole.buffer(3.0)):
                # centredness beats height: 1 mm sideways tilts the whole
                # piece, 1 mm deeper is invisible
                score = (abs(dx), dy)
                if best is None or score < best[0]:
                    best = (score, ex, ey, hole)
        if best is not None and best[0][0] == 0:
            break                # centred spot found, no need to scan deeper
    if best is None:
        print("[!] kulcslyuk kihagyva - nincs eleg tomor anyag a felso savban")
        return geom
    _, ex, ey, hole = best
    print(f"[i] kulcslyuk: ({ex - minx:.0f}, {ey - miny:.0f}) mm, "
          f"{ex - cx:+.0f} mm a sulyponti tengelytol")
    return geom.difference(hole)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--levels", type=int, default=6)
    ap.add_argument("--thicken", type=float, default=0.6, help="mm, hairline repair")
    ap.add_argument("--min-part", type=float, default=MIN_PART,
                    help="mm2, below this a piece is left to the plate behind")
    ap.add_argument("--no-keyhole", action="store_true")
    ap.add_argument("--solid-back", action="store_true",
                    help="a hatlap lyukai kitoltve - tomor hatter a csipke moge, "
                         "ahogy a keretezett shadow boxoknal szokas")
    ap.add_argument("--draft", action="store_true",
                    help="hibas biztonsagi riport mellett is irjon fajlokat")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    out = pathlib.Path(a.out or src.parent / "layers"); out.mkdir(parents=True, exist_ok=True)
    img = Image.open(src)
    g, edges, cent = posterise(img, a.levels)

    print(f"forras: {src.name}  {img.width}x{img.height}px")
    print("tonusszintek: " + ", ".join(f"{c:.0f}" for c in cent))

    # pass 0: the mm scale must come from the OBJECT (the level-1 silhouette
    # bbox), not the canvas, and it must be known BEFORE clean() runs -
    # thicken/min_part/min_hole are physical thresholds. A canvas-derived
    # scale would shrink or inflate them by the empty-margin ratio.
    raw1 = trace(mask_at(g, edges[1]))
    if raw1 is None or raw1.is_empty:
        raise SystemExit("az 1. reteg (hatlap) ures - hasznalhatatlan bemenet")
    rminx, rminy, rmaxx, rmaxy = raw1.bounds
    scale = MM / max(rmaxx - rminx, rmaxy - rminy)

    # pass 1: trace + clean every level at final physical scale
    geoms, dropped = {}, {}
    for k in range(1, a.levels + 1):
        geom, drp = clean(trace(mask_at(g, edges[k])), scale, a.thicken,
                          a.min_part, img.height * scale)
        if geom is not None:
            geoms[k] = geom
            if drp is not None:
                dropped[k] = drp
    if 1 not in geoms:
        raise SystemExit("az 1. reteg (hatlap) ures - hasznalhatatlan bemenet")

    # anchor the object at the origin
    minx, miny, maxx, maxy = geoms[1].bounds
    for k in geoms:
        geoms[k] = affinity.translate(geoms[k], -minx, -miny)
    for k in dropped:
        dropped[k] = affinity.translate(dropped[k], -minx, -miny)

    if a.solid_back:
        # fill the back plate FIRST: the nesting clip and the demotion audit
        # must see the plate the buyer actually receives
        geoms[1] = unary_union([Polygon(p.exterior) for p in parts_of(geoms[1])])

    # the thicken closing grows the object slightly; renormalise so the
    # promised size is exact
    minx, miny, maxx, maxy = geoms[1].bounds
    f2 = MM / max(maxx - minx, maxy - miny)
    if abs(f2 - 1.0) > 1e-4:
        for k in geoms:
            geoms[k] = affinity.scale(geoms[k], xfact=f2, yfact=f2, origin=(0, 0))
        for k in dropped:
            dropped[k] = affinity.scale(dropped[k], xfact=f2, yfact=f2, origin=(0, 0))

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

    # demotion audit: a piece dropped from layer k is promised to remain
    # visible on a plate behind it. Nesting guarantees the footprint stays
    # inside layer 1, but say honestly how much falls MORE than one plate back.
    for k in sorted(dropped):
        prev = geoms.get(k - 1)
        if prev is None or k == 1:
            continue
        deeper = dropped[k].difference(prev)
        if deeper.area > 1.0:
            print(f"[i] {k}. reteg: {dropped[k].area:.0f} mm2 eldobva, ebbol "
                  f"{deeper.area:.0f} mm2 tobb mint egy lappal hatrebb latszik")

    if not a.no_keyhole:
        cut = keyhole(geoms[1])
        if cut is geoms[1]:
            raise SystemExit("nincs hova vagni a kulcslyukat - futtasd "
                             "--no-keyhole kapcsoloval, ha tudatosan hagyod el")
        geoms[1] = cut
        # the hole pierces only the back plate; front layers may overlap it
        # by design (they hide it). This is a deliberate nesting exception.

    print(f"objektum: {MM:.0f} mm (a hatlap befoglaloja, nem a vaszon)")
    print(f"\n{'reteg':>6}{'darab':>7}{'lyuk':>6}{'terulet mm2':>13}{'leggyengebb':>14}"
          f"{'vekony%':>9}{'nyak':>6}  statusz")
    rows, all_ok = [], True
    for k in sorted(geoms):
        geom = geoms[k]
        pieces = parts_of(geom)
        holes = sum(len(p.interiors) for p in pieces)
        nw = frailest(geom)
        ta = thin_area(geom, MIN_WEB)
        nk = necks(geom)
        ok = nw >= MIN_WEB and ta < 0.02 and nk == 0
        all_ok = all_ok and ok
        st = "OK" if ok else ("TORIK" if nw < MIN_WEB else
                              "NYAK" if nk else "VEKONY RESZEK")
        print(f"{k:>6}{len(pieces):>7}{holes:>6}{geom.area:>13,.0f}{nw:>13.2f}mm"
              f"{ta*100:>8.2f}%{nk:>6}  {st}")
        rows.append((k, geom, len(pieces), holes, nw, ta))

    if len(geoms) < a.levels:
        all_ok = False
        print(f"[!] {a.levels} szintbol csak {len(geoms)} adott reteget")
    if not all_ok and not a.draft:
        raise SystemExit("HIBAS RETEG - nem irok ki fajlokat. Reszeredmenyhez: --draft")

    # build into a staging dir and swap at the very end - neither a failed
    # report nor a mid-export crash may leave a half-mixed output directory
    import shutil
    stage = out.parent / (out.name + ".staging")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    final_out, out = out, stage

    for k, geom, *_ in rows:
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
                pts = [(f"{x:.4f}", f"{y:.4f}") for x, y in ring.coords]
                # dedupe AFTER rounding - two distinct floats can land on the
                # same 4-decimal value and would leave a zero-length edge
                dd = [q for i, q in enumerate(pts) if i == 0 or q != pts[i - 1]]
                if len(dd) > 1 and dd[0] == dd[-1]:
                    dd = dd[:-1]          # 70=1 closes the loop
                for x, y in dd:
                    e += ["0", "VERTEX", "8", "CUT", "10", x, "20", y]
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

    report = {
        "levels": a.levels,
        "layers": {k: {"pieces": pc, "holes": ho, "weakest_mm": round(nw, 2),
                       "thin_pct": round(ta * 100, 2)}
                   for k, _, pc, ho, nw, ta in rows},
        "pieces_total": sum(pc for _, _, pc, *_ in rows),
        "weakest_mm": round(min(nw for *_, nw, _ in rows), 2),
        "necks": 0 if all_ok else None,
        "keyhole": not a.no_keyhole,
        "draft": a.draft,
        "size_mm": MM,
    }
    (out / "report.json").write_text(json.dumps(report, indent=1))

    if final_out.exists():
        shutil.rmtree(final_out)
    stage.rename(final_out)
    print(f"\nkiirva: {final_out}  ({len(list(final_out.iterdir()))} fajl)")


if __name__ == "__main__":
    main()
