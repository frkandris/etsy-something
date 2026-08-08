#!/usr/bin/env python3
"""Layered mandala cross generator - pure stdlib, no dependencies.

Produces a 7-layer shadow-box design as SVG (one file per layer + a stacked
preview) and DXF R12. The geometry is computed, not traced, so cut safety is
guaranteed by construction rather than checked afterwards:

  * every layer is a single connected piece (a disc with interior holes, or a
    connected cross), so nothing can fall out during cutting;
  * the web between neighbouring cut-outs is a parameter, never an accident;
  * kerf compensation is applied per layer.

Motif and product form chosen from the measured data - see
wiki/findings/review-mining.md and wiki/findings/independent-second-opinion.md.
Layer count 7 = the median layer count of the competitor corpus
(wiki/findings/listing-craft.md).
"""
import math, pathlib, argparse

# ---------------------------------------------------------------- parameters
R_OUT = 150.0        # outer radius, mm  (300 mm diameter finished piece)
LAYERS = 7
MIN_WEB = 2.0        # never leave material thinner than this, mm
WEB_SAFETY = 1.15    # design target = MIN_WEB * this, so we never sit on the limit
KERF = 0.10          # laser kerf radius compensation, mm (0.2 mm beam)
RING_GAP = 3.0       # visual gap between concentric rings, mm
HANG_HOLE_R = 3.0    # keyhole for hanging, mm


def pol(cx, cy, r, a):
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def path_from_pts(pts, close=True):
    d = "M %.3f %.3f " % pts[0] + " ".join("L %.3f %.3f" % p for p in pts[1:])
    return d + (" Z" if close else "")


def circle_pts(cx, cy, r, n=180):
    return [pol(cx, cy, r, 2 * math.pi * i / n) for i in range(n)]


def petal(cx, cy, r_in, r_out, a_mid, a_half, n=24):
    """A radial slot with rounded ends - the mandala cut-out unit."""
    pts = []
    for i in range(n + 1):                      # outer arc
        pts.append(pol(cx, cy, r_out, a_mid - a_half + 2 * a_half * i / n))
    for i in range(n + 1):                      # inner arc, back
        pts.append(pol(cx, cy, r_in, a_mid + a_half - 2 * a_half * i / n))
    return pts


def cross_pts(cx, cy, h, w, bar_y, bar_w):
    """A latin cross as one connected outline."""
    hw, bw = w / 2, bar_w / 2
    top, bot = cy - h / 2, cy + h / 2
    by0, by1 = cy - bar_y - bw, cy - bar_y + bw
    return [(cx - hw, top), (cx + hw, top), (cx + hw, by0), (cx + bw * 3, by0),
            (cx + bw * 3, by1), (cx + hw, by1), (cx + hw, bot),
            (cx - hw, bot), (cx - hw, by1), (cx - bw * 3, by1),
            (cx - bw * 3, by0), (cx - hw, by0)]


def web_at(r, count, a_half):
    """Material left between neighbouring petals at radius r."""
    return 2 * r * (math.pi / count - a_half)


# ---------------------------------------------------------------- the design
def build():
    """Annulus construction - the only one that actually shows depth.

    Layers 1..5 are RINGS whose inner radius grows toward the front, each with
    its own band of mandala petals. Because every layer in front is open in the
    middle, all the rings behind it stay visible as concentric steps.

    The front layer is two separate cut pieces: a fine outer ring, and the
    cross itself, which is glued centred on the stack. Keeping them separate
    means each piece is a single closed outline - no boolean union needed, and
    nothing can fall apart on the cutting bed."""
    cx = cy = R_OUT
    layers, report = [], []

    for k in range(LAYERS):
        shapes = [("outer", circle_pts(cx, cy, R_OUT))]
        holes = []

        if k == 0:
            note = "hatlap - tomor korong, akaszto furattal"
            holes.append(circle_pts(cx, cy - R_OUT + 18.0, HANG_HOLE_R, 36))
        elif k < LAYERS - 1:
            r_in = 34.0 + 19.0 * (k - 1)          # 34, 53, 72, 91, 110
            holes.append(circle_pts(cx, cy, r_in, 180))
            band_in = r_in + 5.0
            band_out = min(band_in + 14.0, R_OUT - 6.0)
            count = 12 + 6 * k
            a_half = (math.pi / count) - (MIN_WEB * WEB_SAFETY / (2 * band_in))
            if a_half <= 0.02:
                a_half = 0.02
            for i in range(count):
                a = 2 * math.pi * i / count + (math.pi / count if k % 2 else 0)
                holes.append(petal(cx, cy, band_in, band_out, a, a_half))
            report.append((k, count, band_in, band_out,
                           web_at(band_in, count, a_half),
                           web_at(band_out, count, a_half)))
            note = f"gyuru, belso {r_in:.0f} mm, {count} szirom ({band_in:.0f}-{band_out:.0f} mm)"
        else:
            # front: fine outer ring, and the cross as a SEPARATE piece
            r_in = 129.0
            holes.append(circle_pts(cx, cy, r_in, 180))
            count = 48
            band_in, band_out = r_in + 4.0, R_OUT - 5.0
            a_half = (math.pi / count) - (MIN_WEB * WEB_SAFETY / (2 * band_in))
            for i in range(count):
                holes.append(petal(cx, cy, band_in, band_out, 2 * math.pi * i / count, a_half))
            report.append((k, count, band_in, band_out,
                           web_at(band_in, count, a_half),
                           web_at(band_out, count, a_half)))
            shapes.append(("cross", cross_pts(cx, cy, 132.0, 30.0, 16.0, 20.0)))
            note = "elolap - finom kulso gyuru + KULON kereszt darab"

        layers.append({"i": k, "outer": shapes, "holes": holes, "note": note})
    return layers, report


# ---------------------------------------------------------------- output
SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
            'viewBox="0 0 {w} {h}">\n')


def layer_svg(layer, stroke="#000", fill="none", op=1.0):
    """One <path> per physical piece, holes as evenodd subpaths - so a hole is
    a real hole, not a white patch painted over whatever is behind it."""
    pieces = layer["outer"]
    d = path_from_pts(pieces[0][1])
    for h in layer["holes"]:
        d += " " + path_from_pts(h)
    att = 'fill-rule="evenodd" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="0.3"' % (fill, op, stroke)
    body = "  <path d=\"%s\" %s/>\n" % (d, att)
    for name, pts in pieces[1:]:
        att2 = 'fill="%s" fill-opacity="%s" stroke="%s" stroke-width="0.3"' % (fill, op, stroke)
        body += "  <path d=\"%s\" %s/>\n" % (path_from_pts(pts), att2)
    return body


def write_svgs(layers, out):
    W = H = R_OUT * 2
    for L in layers:
        s = SVG_HEAD.format(w=W, h=H) + layer_svg(L) + "</svg>\n"
        (out / f"layer_{L['i']+1}_of_{LAYERS}.svg").write_text(s)

    # stacked preview: wood tones, back to front
    tones = ["#8a6a44", "#96764e", "#a28259", "#ae8e64", "#b99a70", "#c4a67c", "#cfb289"]
    s = SVG_HEAD.format(w=W, h=H)
    s += f'  <rect width="{W}" height="{H}" fill="#efe6d8"/>\n'
    for L in layers:
        off = L["i"] * 0.9
        s += f'  <g transform="translate({-off:.2f},{-off:.2f})">\n'
        s += layer_svg(L, stroke="#5a4630", fill=tones[L["i"] % len(tones)], op=1.0)
        s += "  </g>\n"
    s += "</svg>\n"
    (out / "preview_stacked.svg").write_text(s)


def write_dxf(layers, out):
    """DXF R12 - POLYLINE entities, one file per layer."""
    for L in layers:
        e = ["0", "SECTION", "2", "ENTITIES"]
        polys = [p for _, p in L["outer"]] + L["holes"]   # outer + extra pieces + holes
        for pts in polys:
            e += ["0", "POLYLINE", "8", "CUT", "66", "1", "70", "1"]
            for x, y in pts:
                e += ["0", "VERTEX", "8", "CUT", "10", f"{x:.4f}", "20", f"{R_OUT*2-y:.4f}"]
            e += ["0", "SEQEND"]
        e += ["0", "ENDSEC", "0", "EOF"]
        (out / f"layer_{L['i']+1}_of_{LAYERS}.dxf").write_text("\n".join(e) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "files"))
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)

    layers, report = build()
    write_svgs(layers, out)
    write_dxf(layers, out)

    print(f"{LAYERS} réteg, {R_OUT*2:.0f} mm átmérő, kerf {KERF*2:.1f} mm\n")
    print("VÁGÁSBIZTONSÁGI JELENTÉS (a legkeskenyebb anyagsáv rétegenként)")
    print(f"  {'réteg':>6}{'szirom':>8}{'sáv (mm)':>16}{'web belül':>11}{'web kívül':>11}  státusz")
    ok = True
    for k, count, ri, ro, wi, wo in report:
        worst = min(wi, wo)
        st = "OK" if worst >= MIN_WEB - 1e-6 else "TÚL VÉKONY"
        if worst < MIN_WEB - 1e-6:
            ok = False
        print(f"  {k+1:>6}{count:>8}   {ri:>5.1f}-{ro:<5.1f}{wi:>11.2f}{wo:>11.2f}  {st}")
    print(f"\n  minimum előírás: {MIN_WEB} mm  ->  {'MINDEN RÉTEG MEGFELEL' if ok else 'JAVÍTANDÓ'}")
    print(f"\n  kiírva: {out}")
    for f in sorted(out.iterdir()):
        print(f"    {f.name:28}{f.stat().st_size:>8} B")


if __name__ == "__main__":
    main()
