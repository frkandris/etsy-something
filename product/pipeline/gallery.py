#!/usr/bin/env python3
"""Listing gallery for one run: flat-lay hero, close-ups, layer board, colour
variants and a specs card - the recipe of the gallery we benchmark against
(MarLaserCut, 2026-09-24), minus its borrowed testimonials.

Everything product-specific (crops, variant palettes, captions) lives in the
run's gallery.json; every number printed on an image comes from report.json.

  python gallery.py --run product/catalog/great-wave/runs/2026-09-24-v1
"""
import argparse
import io
import json
import math
import pathlib
import shutil
import subprocess
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from exportlib import output_directory

ROOT = pathlib.Path(__file__).resolve().parents[2]
SIZE = (2700, 2025)                     # 4:3, what Etsy's grid and zoom both use
PAPER = (244, 241, 234)
FONT = "/System/Library/Fonts/Supplemental/Avenir Next.ttc"
FACES = {"bold": 2, "medium": 5, "regular": 7}   # Demi Bold, Medium, Regular


def font(px, face="regular"):
    try:
        return ImageFont.truetype(FONT, px, index=FACES[face])
    except OSError:
        return ImageFont.load_default(px)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render(layers, out, *extra, samples=32):
    cmd = ["blender", "-b", "--python-exit-code", "1", "-P", str(ROOT / "product/render_flat.py"),
           "--", str(layers), str(out), "--samples", str(samples), *extra]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    if not out.is_file():
        raise RuntimeError(f"render missing: {out}")


def pill(draw, xy, text, fnt, fill, ink, anchor="mm", pad=(34, 18)):
    x0, y0, x1, y1 = draw.textbbox(xy, text, font=fnt, anchor=anchor)
    draw.rounded_rectangle((x0 - pad[0], y0 - pad[1], x1 + pad[0], y1 + pad[1]),
                           radius=(y1 - y0) // 2 + pad[1], fill=fill)
    draw.text(xy, text, font=fnt, fill=ink, anchor=anchor)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by rendered pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):          # a no-break space keeps "3 mm" together
        trial = f"{cur} {word}".strip()
        if cur and draw.textlength(trial, font=fnt) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def layer_tile(svg, colour, width):
    """One sheet as the buyer cuts it: its shape filled with its own paper."""
    text = svg.read_text().replace('fill="none" stroke="#000" stroke-width="0.3"',
                                   f'fill="#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}" stroke="none"')
    png = cairosvg.svg2png(bytestring=text.encode(), output_width=width)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True, type=pathlib.Path)
    ap.add_argument("--samples", type=int, default=32)
    a = ap.parse_args()
    run = a.run.resolve()
    cfg = json.loads((run / "gallery.json").read_text())
    layers = run / "output" / "layers"
    rep = json.loads((layers / "report.json").read_text())
    if not rep.get("release_ready"):
        sys.exit("the run is not a validated release - no listing images from it")
    palette = json.loads((layers / "palette.json").read_text())
    svgs = sorted(layers.glob("layer_*_of_*.svg"), key=lambda p: int(p.stem.split("_")[1]))
    bg = str(ROOT / cfg["surface"])
    ink = hexrgb(cfg.get("ink", "#172A4B"))
    w_mm, h_mm = rep["panel_mm"]
    weakest = math.floor(rep["weakest_mm"] * 10) / 10     # "at least 7.8" must not round up
    accents = sum(rep.get("accent_pieces", {}).values())
    facts = f'{rep["levels"]} LAYERS  ·  SVG + DXF  ·  {w_mm:.0f} × {h_mm:.0f} mm'

    with output_directory(run / "output" / "gallery") as out:
        raw = out / "raw"
        raw.mkdir()
        # 1 - hero, piece raised to leave a caption band
        render(layers, raw / "hero.png", "--bg", bg, "--margin", "0.1", "--shift", "0.06",
               samples=a.samples)
        hero = Image.open(raw / "hero.png").convert("RGB")
        d = ImageDraw.Draw(hero)
        d.text((SIZE[0] // 2, SIZE[1] - 250), cfg["title"], font=font(84, "bold"),
               fill=ink, anchor="mm")
        d.text((SIZE[0] // 2, SIZE[1] - 150), facts, font=font(52, "medium"),
               fill=ink, anchor="mm")
        hero.save(out / "01_hero.png")

        # 2..n - close-ups, rendered at full resolution
        n = 2
        for crop in cfg["crops"]:
            render(layers, out / f"{n:02d}_detail.png", "--bg", bg, "--crop", crop,
                   samples=a.samples)
            n += 1

        # layer board: every sheet in its own colour, numbered back to front
        board = Image.new("RGB", SIZE, PAPER)
        d = ImageDraw.Draw(board)
        d.text((SIZE[0] // 2, 150), f'{rep["levels"]} LAYERS · CUT · STACK · GLUE',
               font=font(80, "bold"), fill=ink, anchor="mm")
        cols, tw, gap_x, row_h = 4, 590, 60, None
        th = round(tw * h_mm / w_mm)
        row_h = th + 150
        gx = (SIZE[0] - cols * tw - (cols - 1) * gap_x) // 2
        gy = 300 + (SIZE[1] - 300 - 200 - 2 * row_h) // 2
        tiles = [(layer_tile(svg, palette[i], tw), f"{i + 1}" + (" · back" if i == 0 else
                  " · top" if i == len(svgs) - 1 else "")) for i, svg in enumerate(svgs)]
        # the piece's bounds: its cream frame is the only near-white in the shot
        clean = Image.open(raw / "hero.png").convert("RGB")
        bbox = clean.convert("L").point(lambda v: 255 if v > 245 else 0).getbbox()
        finished = clean.crop(bbox) if bbox else clean
        tiles.append((finished.resize((tw, th)).convert("RGBA"), "finished"))
        for i, (tile, label) in enumerate(tiles):
            x = gx + (i % cols) * (tw + gap_x)
            y = gy + (i // cols) * row_h
            d.rectangle((x - 14, y - 14, x + tw + 14, y + th + 14), fill=(206, 201, 192))
            board.paste(tile, (x, y), tile)
            d.text((x + tw // 2, y + th + 62), label, font=font(50, "medium"), fill=ink, anchor="mm")
        d.text((SIZE[0] // 2, SIZE[1] - 110), "Numbered files · back panel first · foam spacers between sheets",
               font=font(46), fill=ink, anchor="mm")
        board.save(out / f"{n:02d}_layers.png")
        n += 1

        # colour variants: the same files in other card colours
        half = (SIZE[0] // 2, SIZE[1] // 2)
        grid = Image.new("RGB", SIZE, PAPER)
        for i, (name, hexes) in enumerate(cfg["variants"].items()):
            pal = raw / f"palette_{i}.json"
            pal.write_text(json.dumps([list(hexrgb(h)) for h in hexes]))
            img = raw / f"variant_{i}.png"
            render(layers, img, "--bg", bg, "--palette", str(pal), "--margin", "0.1",
                   "--shift", "0.05",
                   "--size", f"{half[0]}x{half[1]}", samples=a.samples)
            tile = Image.open(img).convert("RGB")
            grid.paste(tile, ((i % 2) * half[0], (i // 2) * half[1]))
            pill(ImageDraw.Draw(grid), ((i % 2) * half[0] + half[0] // 2, (i // 2) * half[1] + half[1] - 62),
                 name, font(44, "medium"), (255, 255, 255), ink)
        pill(ImageDraw.Draw(grid), (SIZE[0] // 2, SIZE[1] // 2), "ONE FILE · ANY CARD COLOUR",
             font(58, "bold"), ink, (255, 255, 255), pad=(48, 26))
        grid.save(out / f"{n:02d}_colours.png")
        n += 1

        # specs: what the buyer gets, every figure from report.json
        card = Image.new("RGB", SIZE, PAPER)
        thumb = Image.open(raw / "hero.png").convert("RGB")
        if bbox:
            thumb = thumb.crop(bbox)            # the piece only; the card draws its own shadow
        thumb.thumbnail((1080, 1500))
        shadow = Image.new("RGBA", (thumb.width + 80, thumb.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle((40, 50, thumb.width + 40, thumb.height + 50), fill=(0, 0, 0, 70))
        shadow = shadow.filter(ImageFilter.GaussianBlur(22))
        ty = (SIZE[1] - thumb.height) // 2
        card.paste(shadow, (110, ty - 40), shadow)
        card.paste(thumb, (150, ty))
        d = ImageDraw.Draw(card)
        x = 150 + thumb.width + 150
        d.text((x, 330), "WHAT YOU GET", font=font(88, "bold"), fill=ink)
        lines = [
            f'{rep["levels"]} layer files, SVG + DXF (R12, mm)',
            f'{w_mm:.0f} × {h_mm:.0f} mm ({w_mm / 25.4:.1f} × {h_mm / 25.4:.1f} in), scalable',
            f'Every bridge at least 2 mm; thinnest point {weakest:g} mm',
            f'{rep["pieces_total"]} pieces, {accents} of them small accents',
            *cfg.get("extra_lines", []),
        ]
        body, text_w = font(50), SIZE[0] - x - 130
        y = 520
        for ln in lines:
            d.ellipse((x, y + 20, x + 20, y + 40), fill=ink)
            for part in wrap(d, ln, body, text_w - 56):
                d.text((x + 56, y), part, font=body, fill=ink)
                y += 68
            y += 44
        if cfg.get("credit"):
            for k, part in enumerate(wrap(d, cfg["credit"], font(40), text_w)):
                d.text((x, SIZE[1] - 300 + k * 56), part, font=font(40), fill=(110, 104, 96))
        card.save(out / f"{n:02d}_specs.png")
        shutil.rmtree(raw)
    print(f"[gallery] {run / 'output' / 'gallery'}")


if __name__ == "__main__":
    main()
