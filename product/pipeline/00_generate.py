#!/usr/bin/env python3
"""Step 0 - generate the artwork as a DEPTH MAP with an image model.

The pipeline does not need a pretty picture, it needs a picture that
posterises cleanly into N nested depth levels. So the prompt constrains the
model hard: flat tones, no gradients, no texture, no shadow, nested silhouettes.

Output is the same depth_map.png that 01_illustrate.py produces by hand, so
step 02 consumes either one without changes.

Key is read from OPENAI_API_KEY (kept outside the repo).

Two ways to call the model:
- text only: fresh composition from the subject prompt
- --ref [--crop x,y,w,h]: image-to-image via the edits endpoint. Feed it OUR
  earlier output (or a crop of it - e.g. just the knot border or the root
  weave, without the background) and the new image inherits that drawing
  style. This is how a multi-design series stays visually consistent, and how
  a weak region gets redrawn without losing the rest.
"""
import os, sys, base64, json, pathlib, argparse, urllib.request, uuid

MODEL = "gpt-image-2"
LEVELS = 6

PROMPT = """A design for LAYERED LASER-CUT WALL ART, drawn as a flat greyscale DEPTH MAP.

Subject: {subject}

STRICT RENDERING RULES - these matter more than beauty:
- Use EXACTLY {levels} flat shades of grey plus pure black background. Nothing else.
- Pure black (#000000) is the area cut away entirely, outside the circular piece.
- Darker grey = further back, lighter grey = closer to the viewer. White is the frontmost element.
- Each shade must be a SOLID FLAT FILL. Absolutely no gradients, no shading, no texture,
  no grain, no blur, no drop shadows, no highlights, no lighting.
- Shapes must be clean, closed silhouettes with smooth outlines, like cut paper.
- Every lighter region must sit fully INSIDE a darker region - the levels nest like a
  contour map, never overlapping partially.
- Keep all detail thicker than about 1/200 of the image width, so it survives cutting.
- Perfectly centred, {format}.
- Flat front view, orthographic, no perspective.
- No text, no numbers, no signature, no watermark, no frame, no border decoration outside the circle."""

FORMATS = {
    "circle": "radially balanced, filling the frame as a circular medallion",
    "square": ("filling the frame as a SQUARE panel with a decorative border "
               "running along all four edges - the outermost depth level is the "
               "square border frame itself"),
}

SUBJECTS = {
    # The two winning cat listings (50 and 49 listing-level reviews) are both
    # PORTRAITS with no background scene at all - the ornament lives inside the
    # fur as swirls and dots. Round 1 built a moon scene and was wrong.
    "cat-portrait": (
        "A cat head-and-shoulders portrait in three-quarter profile, looking "
        "slightly upward, with long whiskers extending outward past the edges. "
        "There is NO background scene and no border ornament - the decoration is "
        "drawn INTO the fur itself: art-nouveau swirls, spirals, teardrops and "
        "rows of dots flowing along the cheeks, brow and chest, each swirl a "
        "distinct depth level. The muzzle, chest ruff and brow are the frontmost "
        "levels; the outer fur and ears fall back level by level. Fill the frame "
        "with the head; leave only a plain flat field behind it.", "square"),
    "cat-frontal": (
        "A fluffy long-haired cat face seen straight on and symmetrical, filling "
        "the frame. NO background scene. The outline of each depth level is an "
        "organic paint-splatter shape with soft drips, not a realistic fur "
        "outline. Big round eyes, small nose, prominent cheek ruff. Each level "
        "nests inside the one behind it like poured paint.", "square"),
    "cat-moon": (
        "A sitting cat seen in silhouette from behind, tail curled, looking up at "
        "a large full moon. Behind the moon a night sky with stars; in the "
        "foreground grasses and wildflowers, and framing the whole scene an arch "
        "of leafy branches. The cat is the frontmost layer, the moon a large flat "
        "disc behind it, the sky the deepest layer. A layered scene with clear "
        "foreground, midground and background - not an ornament.", "square"),
    "cat-window": (
        "A cat sitting on a windowsill seen from inside a cosy room, viewed "
        "through the window frame: potted plants on the sill, a hanging plant "
        "above, a crescent moon and stars outside. Nested depth: window frame "
        "frontmost, cat and plants next, night sky deepest.", "square"),
    "cat-mandala": (
        "A cat face centred in an ornate round mandala of interlacing petals, "
        "paw prints and swirling filigree, with whiskers extending into the "
        "pattern. Symmetrical, dense, carved-looking.", "circle"),
    "dachshund-longhair": (
        "A long-haired dachshund lying down elegantly, flowing feathered coat drawn "
        "as sweeping nested tone bands, long silky ear, gentle eye. Behind it a "
        "soft damask filigree field with two small hearts and a bone. A clean "
        "border frames the panel.", "square"),
    "celtic-dara": (
        "A Celtic Dara knot (shield knot) medallion: four interlocked loops "
        "weaving over and under around a central woven square, every strand a "
        "bold band one depth level lighter where it passes over. Dense knotwork "
        "corners and a braided border on the square panel edges. Carved stone "
        "Celtic style.", "square"),
    "dachshund": (
        "A dachshund (sausage dog) portrait in profile, sitting, smooth coat, "
        "unmistakable breed silhouette: very long body, short legs, long muzzle, "
        "big floppy ear. The dog is the front layers; behind it an ornamental "
        "background of paw prints, bones and swirling filigree. A clean border "
        "frames the panel. The dog's body is built from flowing, nested tone "
        "bands like layered paper art.", "square"),
    "celtic-knot": (
        "A Celtic trinity knot (triquetra) interlaced with a circle, drawn as "
        "bold woven bands - each strand clearly passes over and under the "
        "others, and the over-strand is one depth level lighter than the "
        "under-strand at every crossing. Around it, a dense interlaced Celtic "
        "knotwork field fills the corners of the square panel, with a woven "
        "border along the edges. In the style of carved stone Celtic art.",
        "square"),
    "celtic-tree": (
        "A Celtic Tree of Life medallion. A gnarled tree with tapering trunk, "
        "flowing branches that curve outward and downward into interlaced Celtic knotwork, "
        "and mirrored roots below forming the same weave, all enclosed by a circular band. "
        "Around the outside, a woven Celtic knot border of interlacing strands. "
        "Ornate, symmetrical, intricate - in the style of carved wooden Celtic art.",
        "circle"),
    "hummingbird": (
        "A hummingbird in flight beside a large ornamental flower, surrounded by "
        "filigree scrollwork and layered petals, enclosed in a circular medallion.",
        "circle"),
    "wolf": (
        "A wolf head facing forward, framed by a circular mandala of pine trees and "
        "mountains, with ornamental filigree filling the corners.", "circle"),
}


REF_NOTE = """
STYLE REFERENCE: the attached image shows the exact drawing style, stroke
weight and flat grey depth-level scheme to reproduce. Draw the NEW subject
below as a complete new composition in that same visual voice - do not copy
the reference's subject, only its style and its flat-grey depth convention."""


def _multipart(fields, files):
    b = uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, (fn, blob, ct) in files.items():
        out += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                f"filename=\"{fn}\"\r\nContent-Type: {ct}\r\n\r\n").encode() + blob + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={b}"


def generate(subject_key, out_dir, size="1024x1024", n=1, ref=None, crop=None, levels=LEVELS):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY hianyzik")
    subj, fmt = SUBJECTS[subject_key]
    prompt = PROMPT.format(subject=subj, levels=levels, format=FORMATS[fmt])
    if ref:
        from PIL import Image
        import io
        img = Image.open(ref)
        if crop:
            x, y, w, h = crop
            img = img.crop((x, y, x + w, y + h))
        buf = io.BytesIO(); img.save(buf, "PNG")
        body, ctype = _multipart(
            {"model": MODEL, "prompt": prompt + REF_NOTE, "size": size, "n": str(n)},
            {"image": ("ref.png", buf.getvalue(), "image/png")})
        url = "https://api.openai.com/v1/images/edits"
        print(f"[gen] {MODEL}  {size}  temaja: {subject_key}  ref: {ref}"
              + (f" crop {crop}" if crop else ""))
    else:
        body = json.dumps({"model": MODEL, "prompt": prompt, "size": size, "n": n}).encode()
        ctype = "application/json"
        url = "https://api.openai.com/v1/images/generations"
        print(f"[gen] {MODEL}  {size}  temaja: {subject_key}")
    req = urllib.request.Request(
        url, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.load(r)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, item in enumerate(data["data"]):
        raw = base64.b64decode(item["b64_json"])
        p = out_dir / f"raw_{subject_key}_{i}.png"
        p.write_bytes(raw)
        paths.append(p)
        print(f"[gen] {p}  {len(raw)/1024:.0f} KB")
    if data.get("usage"):
        print(f"[gen] usage: {data['usage']}")
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="celtic-tree", choices=list(SUBJECTS))
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--levels", type=int, default=LEVELS)
    ap.add_argument("--ref", default=None, help="stilus-referencia kep (image-to-image)")
    ap.add_argument("--crop", default=None, help="x,y,w,h - a referencia kivagando resze")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "work"))
    a = ap.parse_args()
    crop = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    generate(a.subject, pathlib.Path(a.out), a.size, a.n, a.ref, crop, a.levels)
