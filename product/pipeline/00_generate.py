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

RECESSED = """
CONSTRUCTION - READ THIS FIRST. This is a RECESSED paper-cut: a stack of
sheets where the TOP sheet is a full panel and the picture is made by
OPENINGS cut through it, each sheet below having its own smaller openings, so
the eye looks DOWN into a stepped well.
Therefore:
- The empty field around the subject is the LIGHTEST level - it IS the top
  sheet, and it is part of the picture.
- Every darker level is a sheet further down. The deepest recesses are the
  darkest.
- PURE BLACK MUST NOT APPEAR ANYWHERE except as the very deepest recess.
- THE TOP SHEET FILLS THE WHOLE SQUARE, EDGE TO EDGE. The lightest level runs
  right off all four edges of the picture. There is NO margin, NO black border,
  NO drawn frame and NO decorated corners - the sheet simply continues to the
  edge, exactly like a mat board in a frame.
- THE TOP SHEET IS ALSO PART OF THE SUBJECT. It must reach INTO the design and
  form some of the subject itself - a muzzle, a cheek, a chest, a highlight -
  in the SAME lightest tone as the surrounding field, connected to it or
  clearly reading as the same sheet. Roughly a fifth of the area inside the
  subject should be that same top-sheet tone. The subject must not be a hole
  filled entirely with darker levels.
- The subject occupies only the MIDDLE 70 PERCENT of the width. A wide band of
  the plain top sheet stays empty on all four sides.
- Each level is 3 to 8 LARGE liquid shapes. No filaments, no fur strands, no
  whiskers thinner than 1/70 of the width - if a detail cannot be that thick,
  leave it out.
- CRITICAL - the shapes must NOT stay inside the subject's outline. On every
  level, 2 or 3 bands must CROSS the outline and SWEEP FAR out into the empty
  field: each band is HALF THE WIDTH OF THE PICTURE long, curving through two
  or three S-bends, tapering steadily from full width down to a fine rounded
  teardrop tip, and finishing well out in the open - at least a quarter of the
  picture width clear of the subject. Short stubs beside the outline are wrong.
  Think a long ribbon of poured paint flung across the sheet that happens to
  form the subject where it pools, not an animal with drips on its chin.
  No closed, self-contained outline anywhere on the lower levels.
- Scatter about TWENTY small round openings across the empty field, sizes
  varying from tiny to medium, each reaching a different depth so a colour
  shows at its floor rather than blackness.

"""


FLAT = """A FLAT PAPERCUT ILLUSTRATION for layered wall art.

Subject: {subject}

Drawn as flat colour blocks only. This is the picture itself, not a plan for
one - draw it the way a papercut artist would cut it.

- EXACTLY {levels} flat tones, no more. Every tone is one sheet of paper.
  Solid fill, hard edges. NO gradients, NO shading, NO drop shadows, NO
  texture, NO grain, NO outlines, NO highlights.
- The palette is a warm neutral ramp from cream to deep brown. Each tone is
  clearly separable from its neighbours - if two tones could be confused at a
  glance, push them apart.
- The lightest tone is the field around the subject and RUNS OFF ALL FOUR
  EDGES. No border, no frame, no decorated corners.
- The lightest tone must also reach INTO the subject and form part of it - a
  muzzle, a cheek, a chest - roughly a fifth of the subject's area.
- Each tone is 3 to 8 LARGE liquid shapes. Nothing thinner than 1/70 of the
  picture width: no filaments, no fur strands, no whiskers. If a detail cannot
  be that thick, leave it out.
- 2 or 3 bands per tone must CROSS the subject's outline and sweep far out
  into the empty field, half the picture wide, tapering to a rounded teardrop
  tip. Think poured paint that happens to pool into the subject.
- Scatter about twenty small round dots of varying size across the field.
- The subject occupies the middle 70 percent of the width.

Square, flat, centred, no text, no signature, no background scene.
"""

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
- CUTTABILITY IS A HARD CONSTRAINT. Every shape must be a solid area, never a line.
  No hairlines, no outlines, no thin strokes anywhere. Minimum thickness of ANY
  feature is 1/90 of the image width - if a detail cannot be drawn that thick,
  leave it out instead. Whiskers must be long TAPERED SOLID WEDGES, thick where
  they meet the face. Dots must be at least 1/60 of the image width across.
  Ornament inside the fur must be broad ribbons, not pen strokes.
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
    "abstract-cat": (
        "A cat head seen straight on, built entirely from nested MELTING, "
        "DRIPPING organic shapes - like thick paint poured in layers, each level "
        "an irregular blob with rounded lobes and soft drips running downward. "
        "NO border, NO frame, NO ornament: the area around the head is one flat "
        "empty background level filling at least a third of the picture. "
        "The outermost, largest level is the plain background. Big rounded eyes "
        "and a small muzzle stay clearly readable near the centre; long tapered "
        "whiskers sweep out sideways. Few, LARGE, simple shapes - bold poster "
        "art, not fine detail.", "square"),
    "cat-splatter": (
        "A cat head floating in the middle of a completely EMPTY white field. "
        "CRITICAL: there must be NO border, NO frame, NO ring, NO margin band "
        "and NO ornament of any kind around the head - the entire area outside "
        "the head is ONE single flat background level that runs all the way to "
        "the edges of the picture. The head occupies only the middle 55 percent "
        "of the width, leaving a wide empty margin on all four sides. "
        "The head is built from nested PAINT-SPLATTER shapes: bold rounded "
        "lobes with a few soft drips running downward, each depth level a "
        "separate flat blob sitting inside the one behind it. Few, LARGE, "
        "simple shapes - not fine detail. Ears, muzzle and eyes clearly "
        "readable. Scatter about FOURTEEN TINY round DOTS, each only about "
        "2 percent of the picture width across, clustered close around the "
        "lower and side contour of the head - they must stay well away from the "
        "edges of the picture. Give the dots DIFFERENT depth levels from each "
        "other so they read as different colours.",
        "square"),
    "cat-portrait-eye": (
        "A cat head-and-shoulders portrait in three-quarter profile, looking "
        "slightly upward, with long whiskers extending outward past the edges. "
        "NO background scene: the decoration is drawn INTO the fur as "
        "art-nouveau swirls, spirals and rows of dots. "
        "IMPORTANT: the EYE and the NOSE must each be their own separate small "
        "region at the very brightest level, clearly ringed by a darker level "
        "so they read as isolated pieces - they are the accent colour in the "
        "finished piece. Keep a clear margin: no shape may touch the outer edge.",
        "square"),
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

STYLE REFERENCE: the attached image is a photograph of a finished layered
paper-cut artwork. Study its SHAPE LANGUAGE and copy it exactly:
- how few and how LARGE the shapes are, and how soft and rounded their lobes
- how each colour region nests inside the one behind it as a stacked layer
- the melting, poured, drip-like edges
- how much empty field is left around the subject
Do NOT copy its subject, its colours, its frame or its background.

OUTPUT FORMAT IS UNCHANGED: give me the flat greyscale DEPTH MAP described
above - each of the reference's colour layers becomes one flat grey level,
darker further back, pure black outside the piece. Never output colour."""


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


def generate(subject_key, out_dir, size="1024x1024", n=1, ref=None, crop=None,
             levels=LEVELS, subject_text=None, name=None, recessed=False, flat=False):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY hianyzik")
    if subject_text:
        subj, fmt = subject_text, "square"
    else:
        subj, fmt = SUBJECTS[subject_key]
    if flat:
        # the model draws the PICTURE, not a plan for one; 01b_depth.py works
        # out which sheet sits in front of which. Asking one model to do both
        # is what kept producing unreadable depth maps.
        prompt = FLAT.format(subject=subj, levels=levels)
        recessed = False
    else:
        prompt = PROMPT.format(subject=subj, levels=levels, format=FORMATS[fmt])
    if recessed:
        # the base prompt's "pure black background" and "outside the circular
        # piece" directly contradict a full light panel, and the model obeyed
        # them - that is why black background kept coming back
        prompt = (RECESSED + prompt)
        prompt = prompt.replace(
            "- Pure black (#000000) is the area cut away entirely, outside the "
            "circular piece.\n", "")
        prompt = prompt.replace(
            "- Use EXACTLY {levels} flat shades of grey plus pure black background. "
            "Nothing else.".format(levels=levels),
            "- Use EXACTLY {levels} flat shades of grey. No pure black anywhere "
            "except the deepest recess.".format(levels=levels))
        prompt = prompt.replace(
            "- Darker grey = further back, lighter grey = closer to the viewer. "
            "White is the frontmost element.",
            "- Lighter grey = closer to the viewer; the LIGHTEST grey is the top "
            "sheet and fills the whole square.")
    if ref:
        from PIL import Image
        import io
        img = Image.open(ref)
        if crop:
            x, y, w, h = crop
            img = img.crop((x, y, x + w, y + h))
        buf = io.BytesIO(); img.save(buf, "PNG")
        body, ctype = _multipart(
            {"model": MODEL, "prompt": prompt + ("" if flat else REF_NOTE), "size": size, "n": str(n)},
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
        p = out_dir / f"raw_{name or subject_key}_{i}.png"
        p.write_bytes(raw)
        paths.append(p)
        print(f"[gen] {p}  {len(raw)/1024:.0f} KB")
    if data.get("usage"):
        print(f"[gen] usage: {data['usage']}")
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="celtic-tree", choices=list(SUBJECTS))
    ap.add_argument("--subject-text", default=None, help="szabad tema, a SUBJECTS helyett")
    ap.add_argument("--name", default=None, help="fajlnev-toredek")
    ap.add_argument("--flat", action="store_true",
                    help="lapos papercut illusztracio (a melyseget 01b_depth.py adja)")
    ap.add_argument("--recessed", action="store_true",
                    help="sullyesztett szerkezet: a mezo a legfelso, legvilagosabb lap")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--levels", type=int, default=LEVELS)
    ap.add_argument("--ref", default=None, help="stilus-referencia kep (image-to-image)")
    ap.add_argument("--crop", default=None, help="x,y,w,h - a referencia kivagando resze")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "work"))
    a = ap.parse_args()
    crop = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    generate(a.subject, pathlib.Path(a.out), a.size, a.n, a.ref, crop, a.levels,
             a.subject_text, a.name, a.recessed, a.flat)
