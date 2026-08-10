#!/usr/bin/env python3
"""Step 1b - turn a FLAT papercut illustration into a depth map.

Why this exists. Until now step 0 asked the image model to draw a depth map
directly, and that is the one thing it is bad at: there is no documented case
of a generative model reliably honouring "light = near". What it IS good at is
drawing flat, few-tone papercut art with clean region boundaries. So step 0 now
asks for the picture itself, and this script works out the sheets.

The joining trick comes from Illustrator's Depth (arXiv 2511.17454): do NOT
posterise per pixel. Segment into flat colour regions first, then give every
region ONE value. A per-pixel posterise turns every wobble into a ragged
contour; one value per region cannot. (We took the idea only - their code is
Adobe-Research-licensed and non-commercial.)

Which value, though - and this is where measuring beat the plan.

  --order tone   (default)  the region's TONE is its sheet
  --order depth             a monocular depth model ranks the regions

The depth route was the intended one. Depth Anything V2 read our cat as a
solid object standing in front of a wall: a beautiful silhouette and almost no
internal structure, so every sheet inside the subject collapsed into one. That
is the right answer to the question it was asked and the wrong answer to ours.
In a papercut the tone IS the sheet - the artist picks cream for the top sheet
and deep brown for the bottom of the well - so once the model draws real
papercut art instead of a depth map, the ordering is already in the picture.

Kept both, because --order depth is the correct choice for a *relief* carved
from a photograph, where tone means light and not height.

Model (depth route only): Depth Anything V2 SMALL - Apache-2.0. Base/Large/
Giant are CC-BY-NC and cannot be used for a product.

  python 01b_depth.py --art flat.png --out depth_map.png --levels 6
"""
import argparse, pathlib
import numpy as np
from PIL import Image

MODEL = "depth-anything/Depth-Anything-V2-Small-hf"   # Apache-2.0

LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def estimate_depth(img):
    """Monocular depth, normalised to 0..1 with 1 = nearest."""
    import torch
    from transformers import pipeline
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"[depth] {MODEL} ({dev})")
    pipe = pipeline("depth-estimation", model=MODEL, device=dev)
    d = np.asarray(pipe(img)["predicted_depth"], dtype=np.float32)
    if d.shape != (img.height, img.width):
        d = np.asarray(Image.fromarray(d).resize(img.size, Image.BILINEAR),
                       dtype=np.float32)
    lo, hi = float(d.min()), float(d.max())
    return (d - lo) / (hi - lo) if hi > lo else np.zeros_like(d)


def quantise(img, levels):
    """Collapse the illustration onto exactly `levels` flat tones.

    The picture is already flat by construction, so this only has to absorb the
    model's slight drift within one sheet. Clusters come back ordered dark to
    light, which for a papercut is deepest sheet to top sheet.
    """
    from sklearn.cluster import KMeans
    a = np.asarray(img.convert("RGB"), dtype=np.float32).reshape(-1, 3)
    km = KMeans(n_clusters=levels, n_init=6, random_state=0).fit(a[::5])
    cent = km.cluster_centers_
    order = np.argsort(cent @ LUMA)                 # dark -> light
    remap = np.zeros(levels, dtype=np.int32)
    remap[order] = np.arange(levels)
    q = remap[km.predict(a)].reshape(img.height, img.width)
    for i, k in enumerate(order):
        share = float((q == i).mean()) * 100
        print(f"[depth]   szint {i}  luma {float(cent[k] @ LUMA):5.1f}  {share:5.1f}%")
    return q.astype(np.int32)


def clean(q, levels, min_px):
    """Drop specks, then hand their pixels to the nearest surviving region.

    Done on the LABELLED components rather than the tone map, so a small
    isolated blob disappears while a large region of the same tone survives.
    """
    from skimage.measure import label
    from scipy.ndimage import distance_transform_edt
    keep = np.zeros(q.shape, dtype=bool)
    for c in range(levels):
        m = q == c
        if not m.any():
            continue
        lab = label(m, connectivity=1)
        cnt = np.bincount(lab.ravel())
        big = np.isin(lab, np.nonzero(cnt >= min_px)[0][1:])
        keep |= big
    dropped = int((~keep).sum())
    if dropped:
        _, (iy, ix) = distance_transform_edt(~keep, return_indices=True)
        q = q[iy, ix]
        print(f"[depth] {dropped * 100.0 / q.size:.2f}% szemcse beolvasztva")
    return q


def by_depth(img, q, levels):
    """Re-rank the tone clusters by the depth model's median instead of luma."""
    d = estimate_depth(img)
    med = [float(np.median(d[q == c])) if (q == c).any() else -1.0
           for c in range(levels)]
    order = np.argsort(med)                          # far -> near
    remap = np.zeros(levels, dtype=np.int32)
    remap[order] = np.arange(levels)
    print("[depth] melyseg-sorrend:", " ".join(f"{c}->{remap[c]}" for c in range(levels)))
    return remap[q], d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", required=True, help="lapos papercut illusztracio")
    ap.add_argument("--out", required=True)
    ap.add_argument("--levels", type=int, default=6)
    ap.add_argument("--order", choices=["tone", "depth"], default="tone")
    ap.add_argument("--min-region-pct", type=float, default=0.03,
                    help="ennel kisebb folt beolvad a szomszedjaba (a kep %-aban)")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()

    img = Image.open(a.art).convert("RGB")
    q = quantise(img, a.levels)
    d = None
    if a.order == "depth":
        q, d = by_depth(img, q, a.levels)
    q = clean(q, a.levels, int(img.width * img.height * a.min_region_pct / 100))

    used = len(np.unique(q))
    print(f"[depth] {used} szint {a.levels} kertbol  (rendezes: {a.order})")
    dm = (q.astype(np.float32) * (255.0 / max(1, a.levels - 1))).astype(np.uint8)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(dm).save(out)
    print(f"[depth] kesz: {out}")
    if a.debug:
        if d is None:
            d = estimate_depth(img)
        Image.fromarray((d * 255).astype(np.uint8)).save(out.with_name("debug_depth.png"))


if __name__ == "__main__":
    main()
