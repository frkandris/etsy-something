#!/usr/bin/env python3
"""Step 4 - put the framed piece into a real photographed interior.

Geometry could never carry the background: spheres and cylinders read as
placeholders no matter how they are lit, and that single axis was what the
reviewer kept scoring lowest. So the scene stops being modelled and becomes a
photograph, with the frame rendered on transparency and composited into it.

  --shoot   generate the backdrop photo with the image model (once per scene)
  --place   composite an alpha render onto a backdrop

The contact shadow is the part that sells it. A cut-out pasted on a photo looks
pasted; the same cut-out with a soft dark pool under its base looks like it is
standing on the table.
"""
import argparse, base64, io, json, math, os, pathlib, sys, urllib.request
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

MODEL = "gpt-image-2"

SCENES = {
    "warm-shelf": (
        "A photograph of an empty corner of a warm, styled living room, shot on "
        "a 50mm lens at f/2.0. In the foreground a light oak table surface runs "
        "across the bottom third, in sharp focus at the front and softening "
        "toward the back. Behind it a warm ochre plaster wall, and arranged "
        "along it - clearly out of focus - a trailing potted plant, a stack of "
        "two hardback books, a small carved wooden figure and a ceramic vase. "
        "Soft daylight from the upper left, warm and gentle, with visible soft "
        "shadows. THE CENTRE OF THE FRAME MUST BE EMPTY: leave a clear open "
        "space on the table for an object to be placed later. Nothing hanging "
        "on the wall, no picture frames anywhere. Natural photograph, no text."),
    "nordic-desk": (
        "A photograph of a pale Scandinavian desk against a white wall, 50mm at "
        "f/2.0. A white oak desktop across the bottom third in sharp focus; "
        "behind it, softly out of focus, a small green plant in a white pot, a "
        "ceramic mug and a folded linen cloth. Cool bright daylight from the "
        "left. THE CENTRE MUST BE EMPTY - clear space on the desk for an object "
        "to be placed later. No frames on the wall. Natural photograph, no text."),
}


def shoot(scene, out):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY hianyzik")
    body = json.dumps({"model": MODEL, "prompt": SCENES[scene],
                       "size": "1536x1024", "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    print(f"[bg] {MODEL} 1536x1024  jelenet: {scene}")
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.load(r)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    print(f"[bg] {out}  {out.stat().st_size/1024:.0f} KB")


def place(bg_path, art_path, out_path, cx=0.5, base=0.78, height=0.62, warm=1.0):
    """cx/base: where the frame's bottom centre sits, as a fraction of the photo.
    height: the frame's height as a fraction of the photo height."""
    bg = Image.open(bg_path).convert("RGB")
    art = Image.open(art_path).convert("RGBA")
    # crop to the actual object: the render has transparent margin around it, and
    # anchoring the shadow to the image edge left it floating below the frame
    bb = art.split()[3].getbbox()
    if bb:
        art = art.crop(bb)
    W, H = bg.size

    th = int(H * height)
    tw = int(art.width * th / art.height)
    art = art.resize((tw, th), Image.LANCZOS)

    # match the backdrop's warmth so the frame does not read as a sticker
    if warm != 1.0:
        r, g, b, a = art.split()
        r = r.point(lambda v: min(255, int(v * warm)))
        b = b.point(lambda v: int(v / warm))
        art = Image.merge("RGBA", (r, g, b, a))

    x0 = int(W * cx - tw / 2)
    y0 = int(H * base - th)

    # cast shadow: the object's own silhouette, squashed and thrown to the right
    # (the backdrop's light comes from the upper left), anchored to the BASE
    alpha = art.split()[3]
    base_y = y0 + th
    sh_h = max(8, int(th * 0.13))
    sh = alpha.resize((int(tw * 1.02), sh_h), Image.LANCZOS)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sl = Image.new("RGBA", sh.size, (36, 24, 14, 255))
    sl.putalpha(sh.point(lambda v: int(v * 0.42)))
    shadow.paste(sl, (x0 + int(tw * 0.045), base_y - int(sh_h * 0.55)), sl)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(8, th * 0.030)))
    out = Image.alpha_composite(bg.convert("RGBA"), shadow)

    # the contact pool: tight, dark, and touching the base line - this is what
    # stops the object reading as pasted on
    tight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tight)
    td.ellipse([x0 + tw * 0.02, base_y - th * 0.030,
                x0 + tw * 0.98, base_y + th * 0.022], fill=(28, 18, 11, 190))
    tight = tight.filter(ImageFilter.GaussianBlur(radius=max(3, th * 0.011)))
    out = Image.alpha_composite(out, tight)

    out.paste(art, (x0, y0), art)

    # a whisper of grain over everything, so the render and the photo share one
    # noise floor - without it the frame stays suspiciously clean
    import random
    random.seed(7)
    g = Image.new("L", (W // 2, H // 2))
    g.putdata([random.gauss(128, 7) for _ in range(g.width * g.height)])
    g = g.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.4))
    out = Image.blend(out.convert("RGB"),
                      Image.merge("RGB", (g, g, g)), 0.030)
    out = ImageEnhance.Color(out).enhance(1.03)
    out.save(out_path)
    print(f"[bg] kesz: {out_path}  ({W}x{H})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shoot", choices=list(SCENES))
    ap.add_argument("--bg")
    ap.add_argument("--art")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cx", type=float, default=0.5)
    ap.add_argument("--base", type=float, default=0.78)
    ap.add_argument("--height", type=float, default=0.62)
    ap.add_argument("--warm", type=float, default=1.0)
    a = ap.parse_args()
    if a.shoot:
        shoot(a.shoot, pathlib.Path(a.out))
    else:
        place(a.bg, a.art, a.out, a.cx, a.base, a.height, a.warm)
