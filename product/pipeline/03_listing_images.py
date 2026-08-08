#!/usr/bin/env python3
"""Step 3 - listing image set from the renders.

The high-review competitors' galleries share a structure (see
wiki/findings/competitor-listing-images.md): a hero with a text overlay
(format list, material, size, layer count), close-ups, a flat-lay of what you
cut, and an assembly guide. This composes those from the render + the trace
outputs, so every design ships with a consistent gallery.

Usage:
  python 03_listing_images.py --dir <iteration_dir> --title "Dachshund Shadow Box" \
      --layers 7 [--size-mm 300]
Reads  <dir>/render_hero.png (or --hero) and <dir>/layers/assembly_guide.png.
Writes <dir>/listing/01_hero.png, 02_specs.png, 03_closeup.png, 04_assembly.png
"""
import argparse, json, math, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

INK = (36, 30, 26)
PAPER = (247, 243, 236)
ACCENT = (191, 108, 34)


def font(size, bold=False):
    for name in (["/System/Library/Fonts/Supplemental/Avenir Next.ttc",
                  "/System/Library/Fonts/Supplemental/Futura.ttc",
                  "/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else
                 ["/System/Library/Fonts/Supplemental/Avenir Next.ttc",
                  "/System/Library/Fonts/Supplemental/Arial.ttf"]):
        try:
            return ImageFont.truetype(name, size, index=1 if name.endswith(".ttc") and bold else 0)
        except Exception:
            continue
    return ImageFont.load_default(size)


def hero_overlay(hero, title, layers, size_mm, out):
    """Competitor recipe: the hero card carries title + formats + material."""
    img = hero.convert("RGB").resize((2000, 2000))
    dr = ImageDraw.Draw(img, "RGBA")
    # top band
    dr.rectangle([0, 0, 2000, 170], fill=(*INK, 216))
    dr.text((1000, 62), title, font=font(76, bold=True), fill=PAPER, anchor="mm")
    dr.text((1000, 132), "LAYERED LASER CUT FILES  ·  SVG + DXF",
            font=font(42), fill=(222, 210, 196), anchor="mm")
    # bottom chips
    chips = [f"{layers} LAYERS", f'{size_mm} mm / {size_mm/25.4:.1f}"',
             "3 mm (1/8\") MATERIAL", "GLOWFORGE · CRICUT · CNC"]
    y0, y1 = 1856, 1944
    total = sum(font(40, bold=True).getlength(c) + 96 for c in chips)
    x = (2000 - total) / 2
    for c in chips:
        w = font(40, bold=True).getlength(c) + 72
        dr.rounded_rectangle([x, y0, x + w, y1], 14, fill=(*INK, 216))
        dr.text((x + w / 2, (y0 + y1) / 2), c, font=font(40, bold=True),
                fill=PAPER, anchor="mm")
        x += w + 24
    img.save(out)


def specs_card(hero, layers, size_mm, pieces, weakest, out, rep=None):
    """The trust card. Every claim comes from the build's report.json - a
    hand-typed number or an unconditional promise is how a listing ends up
    lying about a --draft or --no-keyhole build."""
    img = Image.new("RGB", (2000, 2000), PAPER)
    dr = ImageDraw.Draw(img)
    h = hero.convert("RGB").resize((1180, 1180))
    img.paste(h, (410, 130))
    dr.text((1000, 1420), "CUT-SAFE, VERIFIED", font=font(84, bold=True),
            fill=INK, anchor="mm")
    lines = [
        f"{layers} numbered layers  ·  {pieces} pieces total",
        f"every piece at least {weakest} mm at its widest",
    ]
    if rep is None or rep.get("necks") == 0:
        lines.append("no thin necks - narrow bridges are auto-widened")
    if rep is None or rep.get("keyhole"):
        lines.append("keyhole hanger cut into the back plate")
    lines.append(f"{size_mm} mm ({size_mm/25.4:.1f}\") finished size, scalable")
    y = 1530
    for ln in lines:
        dr.text((1000, y), ln, font=font(52), fill=(80, 68, 58), anchor="mm")
        y += 86
    img.save(out)


def closeup(hero, out):
    img = hero.convert("RGB")
    w, h = img.size
    crop = img.crop((int(w * 0.28), int(h * 0.18), int(w * 0.86), int(h * 0.76)))
    crop = crop.resize((2000, 2000)).filter(ImageFilter.UnsharpMask(2, 60, 3))
    crop.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--layers", type=int, default=0, help="report.json feluliria")
    ap.add_argument("--pieces", type=int, default=0, help="report.json feluliria")
    ap.add_argument("--weakest", default="6")
    ap.add_argument("--size-mm", type=int, default=300)
    ap.add_argument("--hero", default=None)
    a = ap.parse_args()

    d = pathlib.Path(a.dir)
    hero = Image.open(a.hero or d / "render_hero.png")
    out = d / "listing"
    out.mkdir(exist_ok=True)
    rep = None
    repf = d / "layers" / "report.json"
    if repf.exists():
        rep = json.loads(repf.read_text())
        a.layers = rep["levels"]
        a.pieces = rep["pieces_total"]
        # floor to one decimal - "at least 6" over a 5.96 mm piece is a lie
        a.weakest = f"{math.floor(rep['weakest_mm'] * 10) / 10:g}"
        a.size_mm = int(rep["size_mm"])
        if rep.get("draft"):
            raise SystemExit("draft build - listing kepet nem gyartunk belole")
    hero_overlay(hero, a.title, a.layers, a.size_mm, out / "01_hero.png")
    specs_card(hero, a.layers, a.size_mm, a.pieces, a.weakest, out / "02_specs.png", rep)
    closeup(hero, out / "03_closeup.png")
    guide = d / "layers" / "assembly_guide.png"
    if guide.exists():
        g = Image.open(guide).convert("RGB")
        s = 2000 / max(g.size)
        g = g.resize((int(g.width * s), int(g.height * s)))
        canvas = Image.new("RGB", (2000, 2000), PAPER)
        canvas.paste(g, ((2000 - g.width) // 2, (2000 - g.height) // 2))
        dr = ImageDraw.Draw(canvas)
        dr.text((1000, 80), "ASSEMBLY ORDER - LAYER BY LAYER",
                font=font(64, bold=True), fill=INK, anchor="mm")
        canvas.save(out / "04_assembly.png")
    print(f"[listing] kesz: {out}  ({len(list(out.iterdir()))} kep)")


if __name__ == "__main__":
    main()
