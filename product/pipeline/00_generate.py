#!/usr/bin/env python3
"""Step 0 - generate the artwork as a DEPTH MAP with an image model.

The pipeline does not need a pretty picture, it needs a picture that
posterises cleanly into N nested depth levels. So the prompt constrains the
model hard: flat tones, no gradients, no texture, no shadow, nested silhouettes.

Output is the same depth_map.png that 01_illustrate.py produces by hand, so
step 02 consumes either one without changes.

Key is read from OPENAI_API_KEY (kept outside the repo).
"""
import os, sys, base64, json, pathlib, argparse, urllib.request

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
- Perfectly centred, radially balanced, filling the frame as a circular medallion.
- Flat front view, orthographic, no perspective.
- No text, no numbers, no signature, no watermark, no frame, no border decoration outside the circle."""

SUBJECTS = {
    "celtic-tree": (
        "A Celtic Tree of Life medallion. A gnarled tree with tapering trunk, "
        "flowing branches that curve outward and downward into interlaced Celtic knotwork, "
        "and mirrored roots below forming the same weave, all enclosed by a circular band. "
        "Around the outside, a woven Celtic knot border of interlacing strands. "
        "Ornate, symmetrical, intricate - in the style of carved wooden Celtic art."),
    "hummingbird": (
        "A hummingbird in flight beside a large ornamental flower, surrounded by "
        "filigree scrollwork and layered petals, enclosed in a circular medallion."),
    "wolf": (
        "A wolf head facing forward, framed by a circular mandala of pine trees and "
        "mountains, with ornamental filigree filling the corners."),
}


def generate(subject_key, out_dir, size="1024x1024", n=1):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY hianyzik")
    prompt = PROMPT.format(subject=SUBJECTS[subject_key], levels=LEVELS)
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": size, "n": n}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    print(f"[gen] {MODEL}  {size}  temaja: {subject_key}")
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
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "work"))
    a = ap.parse_args()
    generate(a.subject, pathlib.Path(a.out), a.size, a.n)
