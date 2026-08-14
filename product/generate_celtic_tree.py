#!/usr/bin/env python3
"""Celtic Tree of Life - layered shadow box generator.

Motif chosen from measured data: Tree of Life carries the sales evidence
(16 reviews / 12 products / 8 independent sellers among the 21 verified shops;
25/18/12 across all 33), while Celtic knotwork carries the visual language that
suits layering. Celtic alone was too thin (6 reviews / 3 sellers).
Demand: `tree of life svg` 533 searches / 20 500 results = 26.0 per 1000.

Geometry is computed and unioned with shapely, so every emitted piece is
verified to be a single connected polygon before it is written - the file
cannot contain a part that falls out on the cutting bed.
"""
import math, pathlib, argparse
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union

R_OUT = 150.0        # outer radius, mm -> 300 mm finished piece
LAYERS = 6
MIN_WEB = 2.0
WEB_SAFETY = 1.15
KERF = 0.10
HANG_R = 3.0


# ------------------------------------------------------------------ motifs
def branch(pts, t, ang, length, width, depth, spread, shrink):
    """Recursive limb; collects buffered segments into pts."""
    if depth == 0 or length < 6:
        return
    x, y = t
    x2, y2 = x + length * math.cos(ang), y + length * math.sin(ang)
    seg = LineString([(x, y), (x2, y2)]).buffer(width / 2, resolution=8,
                                                cap_style=1, join_style=1)
    pts.append(seg)
    for s in (-1, 1):
        branch(pts, (x2, y2), ang + s * spread, length * shrink,
               max(width * 0.72, MIN_WEB * WEB_SAFETY), depth - 1,
               spread * 0.88, shrink)


def tree_of_life(cx, cy, r_ring, ring_w):
    """Classic Celtic tree: canopy above, roots below, both meeting a ring."""
    parts = []
    # the enclosing ring the limbs grow into
    ring = Point(cx, cy).buffer(r_ring, 128).difference(
        Point(cx, cy).buffer(r_ring - ring_w, 128))
    parts.append(ring)
    # trunk
    for w, y0, y1 in ((0.085, 0.46, 0.16), (0.065, 0.16, -0.14)):
        parts.append(LineString([(cx, cy + r_ring * y0), (cx, cy + r_ring * y1)])
                     .buffer(r_ring * w, cap_style=2))
    # canopy: three limbs upward, roots: mirrored downward
    for up in (True, False):
        base = (cx, cy - r_ring * 0.10) if up else (cx, cy + r_ring * 0.42)
        base_ang = -math.pi / 2 if up else math.pi / 2
        for s in (-1, 0, 1):
            branch(parts, base, base_ang + s * 0.60, r_ring * 0.30,
                   r_ring * 0.062, 4, 0.50, 0.72)
    tree = unary_union(parts)
    if tree.geom_type == "MultiPolygon":          # keep only the connected body
        tree = max(tree.geoms, key=lambda g: g.area)
    return tree


def knot_ring(cx, cy, r_mid, band, n, q):
    """Celtic star-knot: a {n/q} star polygon buffered into an interlaced band."""
    pts = [(cx + r_mid * math.cos(2 * math.pi * i / n),
            cy + r_mid * math.sin(2 * math.pi * i / n)) for i in range(n)]
    line, i = [], 0
    for _ in range(n + 1):
        line.append(pts[i % n]); i += q
    ribbon = LineString(line).buffer(band / 2, resolution=12, join_style=1)
    return ribbon


# ------------------------------------------------------------------ helpers
def rings_with_petals(cx, cy, r_in, r_out, count):
    a_half = (math.pi / count) - (MIN_WEB * WEB_SAFETY / (2 * r_in))
    a_half = max(a_half, 0.02)
    holes = []
    for i in range(count):
        a = 2 * math.pi * i / count
        wedge = Polygon([(cx, cy)] + [
            (cx + r_out * 1.05 * math.cos(a - a_half + 2 * a_half * j / 16),
             cy + r_out * 1.05 * math.sin(a - a_half + 2 * a_half * j / 16))
            for j in range(17)])
        band = Point(cx, cy).buffer(r_out, 128).difference(Point(cx, cy).buffer(r_in, 128))
        holes.append(wedge.intersection(band))
    web = 2 * r_in * (math.pi / count - a_half)
    return unary_union(holes), web


def poly_paths(geom):
    out = []
    geoms = geom.geoms if geom.geom_type.startswith("Multi") else [geom]
    for g in geoms:
        if g.is_empty:
            continue
        out.append(list(g.exterior.coords))
        out += [list(r.coords) for r in g.interiors]
    return out


def check_connected(geom, name):
    n = len(geom.geoms) if geom.geom_type == "MultiPolygon" else 1
    return n, ("OK" if n == 1 else f"{n} DARAB - SZETESIK")


# ------------------------------------------------------------------ design
def build():
    cx = cy = R_OUT
    layers, report = [], []
    for k in range(LAYERS):
        if k == 0:
            body = Point(cx, cy).buffer(R_OUT, 256).difference(
                Point(cx, cy - R_OUT + 18).buffer(HANG_R, 32))
            note = "hatlap - tomor korong, akaszto furattal"
        elif k < LAYERS - 2:
            r_in = 40.0 + 24.0 * (k - 1)                     # 40, 64, 88
            body = Point(cx, cy).buffer(R_OUT, 256).difference(
                Point(cx, cy).buffer(r_in, 128))
            count = 16 + 8 * k
            holes, web = rings_with_petals(cx, cy, r_in + 6, r_in + 20, count)
            body = body.difference(holes)
            report.append((k, count, r_in + 6, r_in + 20, web))
            note = f"gyuru, belso {r_in:.0f} mm, {count} szirom"
        elif k == LAYERS - 2:
            outer = Point(cx, cy).buffer(R_OUT, 256).difference(
                Point(cx, cy).buffer(138.0, 128))
            knot = knot_ring(cx, cy, 118.0, 9.5, 16, 5)
            # radial spokes bridge the knot to the rim, otherwise the ribbon
            # would be a free-floating second piece (the check below catches it)
            spokes = []
            for i in range(8):
                a = 2 * math.pi * i / 8 + math.pi / 8
                spokes.append(LineString([
                    (cx + 112 * math.cos(a), cy + 112 * math.sin(a)),
                    (cx + 145 * math.cos(a), cy + 145 * math.sin(a))]).buffer(
                        MIN_WEB * WEB_SAFETY / 2, cap_style=2))
            body = unary_union([outer, knot] + spokes)
            note = "kelta csomo-gyuru (16/5 csillag fonat) + kulso perem"
        else:
            body = tree_of_life(cx, cy, 104.0, 11.0)
            note = "eletfa - kulon darab, kozepre ragasztva"
        n, st = check_connected(body, note)
        layers.append({"i": k, "geom": body, "note": note, "parts": n, "status": st})
    return layers, report


# ------------------------------------------------------------------ output
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{w}mm" '
        'viewBox="0 0 {w} {w}">\n')


def d_of(geom):
    d = []
    for ring in poly_paths(geom):
        d.append("M " + " L ".join("%.3f %.3f" % p for p in ring) + " Z")
    return " ".join(d)


def write(layers, out):
    W = R_OUT * 2
    for L in layers:
        s = HEAD.format(w=W)
        s += f'  <path d="{d_of(L["geom"])}" fill-rule="evenodd" fill="none" stroke="#000" stroke-width="0.3"/>\n</svg>\n'
        (out / f"layer_{L['i']+1}_of_{LAYERS}.svg").write_text(s)

    tones = ["#7d5f3d", "#8b6c47", "#997a52", "#a7885d", "#b59668", "#c3a473"]
    s = HEAD.format(w=W) + f'  <rect width="{W}" height="{W}" fill="#ede3d4"/>\n'
    for L in layers:
        o = L["i"] * 1.1
        s += f'  <g transform="translate({-o:.2f},{-o:.2f})">'
        s += f'<path d="{d_of(L["geom"])}" fill-rule="evenodd" fill="{tones[L["i"]]}" stroke="#4a3826" stroke-width="0.35"/></g>\n'
    s += "</svg>\n"
    (out / "preview_stacked.svg").write_text(s)

    for L in layers:                                   # DXF R12
        e = ["0", "SECTION", "2", "ENTITIES"]
        for ring in poly_paths(L["geom"]):
            e += ["0", "POLYLINE", "8", "CUT", "66", "1", "70", "1"]
            for x, y in ring:
                e += ["0", "VERTEX", "8", "CUT", "10", f"{x:.4f}", "20", f"{W-y:.4f}"]
            e += ["0", "SEQEND"]
        e += ["0", "ENDSEC", "0", "EOF"]
        (out / f"layer_{L['i']+1}_of_{LAYERS}.dxf").write_text("\n".join(e) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "files_celtic_tree"))
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    layers, report = build()
    write(layers, out)

    print(f"Celtic Tree of Life - {LAYERS} reteg, {R_OUT*2:.0f} mm atmero\n")
    print("OSSZEFUGGOSEG (minden reteg egyetlen darab kell legyen)")
    for L in layers:
        print(f"  reteg {L['i']+1}: {L['status']:20} {L['note']}")
    print("\nVAGASBIZTONSAG (legkeskenyebb anyagsav)")
    ok = all(w >= MIN_WEB - 1e-6 for *_, w in report)
    for k, count, ri, ro, web in report:
        print(f"  reteg {k+1}: {count:>3} szirom  {ri:>5.0f}-{ro:<5.0f} mm  web {web:.2f} mm  "
              f"{'OK' if web >= MIN_WEB - 1e-6 else 'TUL VEKONY'}")
    print(f"\n  minimum {MIN_WEB} mm -> {'MEGFELEL' if ok else 'JAVITANDO'}")
    print(f"\n  {out}")
    for f in sorted(out.iterdir()):
        print(f"    {f.name:26}{f.stat().st_size:>9} B")


if __name__ == "__main__":
    main()
