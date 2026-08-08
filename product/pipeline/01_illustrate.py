#!/usr/bin/env python3
"""Step 1 - produce a DEPTH MAP for the layered piece.

The output is a greyscale PNG where the pixel value encodes how far forward
that area sits: 0 = background (cut away), 1 = back plate, ... N = frontmost.
That is exactly the form a posterised AI illustration would take, so step 2
consumes this file identically whether it was drawn here or generated.

This particular drawing is an illustrative Celtic Tree of Life: tapering
organic limbs, leaf clusters, a woven knot border. It is deliberately richer
than the earlier procedural version, because looking at the actual competition
showed that intricacy - not geometric correctness - is what the market pays for.
"""
import math, random, pathlib, argparse
from PIL import Image, ImageDraw, ImageFilter

SIZE = 2400          # px, square
LEVELS = 6           # depth levels above background
random.seed(20260808)


def taper_line(dr, p0, p1, w0, w1, v, steps=28):
    """A limb that thins along its length - drawn as stacked discs."""
    for i in range(steps + 1):
        t = i / steps
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        w = w0 + (w1 - w0) * t
        dr.ellipse([x - w, y - w, x + w, y + w], fill=v)


def limb(dr, base, ang, length, w, depth, v, leaf_v, curve=0.0):
    """Recursive branch with slight curvature, leaves at the tips."""
    if depth == 0 or length < 14:
        # leaf cluster
        for _ in range(6):
            a = ang + random.uniform(-0.9, 0.9)
            d = random.uniform(6, 20)
            lx, ly = base[0] + d * math.cos(a), base[1] + d * math.sin(a)
            r = random.uniform(7, 13)
            dr.ellipse([lx - r, ly - r * 0.62, lx + r, ly + r * 0.62], fill=leaf_v)
        return
    ang2 = ang + curve
    tip = (base[0] + length * math.cos(ang2), base[1] + length * math.sin(ang2))
    taper_line(dr, base, tip, w, w * 0.62, v)
    for s in (-1, 1):
        limb(dr, tip, ang2 + s * random.uniform(0.42, 0.66), length * 0.70,
             max(w * 0.66, 2.6), depth - 1, v, leaf_v,
             curve=s * random.uniform(0.05, 0.20))
    if depth > 2:                      # an extra inner twig for density
        limb(dr, tip, ang2 + random.uniform(-0.2, 0.2), length * 0.5,
             max(w * 0.5, 2.4), depth - 2, v, leaf_v)


def knot_border(dr, cx, cy, r_mid, band, n, q, v_over, v_under):
    """Woven border: the two interleaved strands sit on different depths, so
    the over-under of real knotwork becomes an actual physical step."""
    pts = [(cx + r_mid * math.cos(2 * math.pi * i / n),
            cy + r_mid * math.sin(2 * math.pi * i / n)) for i in range(n)]
    order, i = [], 0
    for _ in range(n + 1):
        order.append(pts[i % n]); i += q
    for k in range(len(order) - 1):
        v = v_over if k % 2 == 0 else v_under
        taper_line(dr, order[k], order[k + 1], band / 2, band / 2, v, steps=40)


def build(out):
    img = Image.new("L", (SIZE, SIZE), 0)
    dr = ImageDraw.Draw(img)
    c = SIZE // 2
    R = SIZE * 0.47

    # level 1: back plate (full disc)
    dr.ellipse([c - R, c - R, c + R, c + R], fill=1)

    # level 2: inner field, slightly proud
    dr.ellipse([c - R * 0.90, c - R * 0.90, c + R * 0.90, c + R * 0.90], fill=2)

    # level 3-4: woven knot border, two strands on two depths
    knot_border(dr, c, c, R * 0.815, R * 0.075, 16, 5, 4, 3)

    # level 3: the ring the tree grows into
    ring_r, ring_w = R * 0.60, R * 0.045
    for rr in (ring_r,):
        dr.ellipse([c - rr - ring_w, c - rr - ring_w, c + rr + ring_w, c + rr + ring_w], fill=3)
        dr.ellipse([c - rr + ring_w, c - rr + ring_w, c + rr - ring_w, c + rr - ring_w], fill=2)

    # level 5: trunk + canopy + roots, level 6: leaves
    trunk_top = (c, c - R * 0.06)
    trunk_bot = (c, c + R * 0.30)
    taper_line(dr, trunk_bot, trunk_top, R * 0.055, R * 0.038, 5, steps=40)
    for up in (True, False):
        base = trunk_top if up else trunk_bot
        a0 = -math.pi / 2 if up else math.pi / 2
        for s in (-1.0, -0.42, 0.42, 1.0):
            limb(dr, base, a0 + s * 0.55, R * (0.20 if up else 0.17),
                 R * 0.030, 4, 5, 6, curve=s * 0.10)

    img = img.filter(ImageFilter.ModeFilter(size=5))      # kill single-pixel noise
    img.save(out / "depth_map.png")

    # human-viewable version
    img.point(lambda v: int(v * 255 / LEVELS)).save(out / "depth_map_preview.png")
    hist = img.histogram()[:LEVELS + 1]
    print("melysegterkep kesz:", out / "depth_map.png")
    for i, n in enumerate(hist):
        print(f"  szint {i}: {n:>10,} px  {'(hatter)' if i == 0 else ''}")
    return img


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "work"))
    a = ap.parse_args()
    o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
    build(o)
