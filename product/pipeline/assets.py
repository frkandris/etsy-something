#!/usr/bin/env python3
"""CC0 3D assets and HDRIs from Poly Haven.

Two problems this solves, both of which the reviewer kept scoring lowest:

1. Hand-modelled props (cylinders for vases, spheres for plants) read as
   placeholders no matter how they are lit.
2. A flat photo backdrop does not move. In a 6-second orbit the frame turns
   while the room stays nailed down, which announces the composite instantly.

Real geometry plus an HDRI environment fixes both: the props sit at their own
depths and parallax correctly, and the HDRI lights the scene and fills the
background with something that rotates with the view.

Licence: everything on Poly Haven is CC0 - commercial use, no attribution
required (https://polyhaven.com/license). Still worth recording what we pulled,
so the manifest below is written next to the files.

  python assets.py fetch            # download the default kit
  python assets.py list plant       # search the catalogue
"""
import argparse, hashlib, json, pathlib, sys, urllib.request

API = "https://api.polyhaven.com"
UA = {"User-Agent": "etsy-something-pipeline/1.0 (+layered svg research)"}
HERE = pathlib.Path(__file__).resolve().parent
STORE = HERE / "assets"

# A small kit, chosen for a warm homely shelf: something to stand the frame
# next to, something green, something with a flame, something woven.
KIT_MODELS = [
    "potted_plant_02",        # trailing green
    "antique_ceramic_vase_01",
    "book_encyclopedia_set_01",
    "wooden_candlestick",
    "wicker_basket_01",
    "brass_vase_01",
]
KIT_HDRIS = ["lythwood_lounge", "fireplace", "anniversary_lounge"]
RES_MODEL = "2k"     # 2k textures are plenty at 1080 px output
RES_HDRI = "2k"


def api(path):
    req = urllib.request.Request(API + path, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=90))


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest, False
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r:
        dest.write_bytes(r.read())
    return dest, True


def fetch_model(aid):
    """Blend file plus its texture dependencies, kept in the layout Blender
    expects (the .blend references textures by relative path)."""
    files = api(f"/files/{aid}")
    blend = files.get("blend", {}).get(RES_MODEL, {}).get("blend")
    if not blend:
        print(f"  [!] {aid}: nincs {RES_MODEL} blend")
        return None
    root = STORE / "models" / aid
    p, new = download(blend["url"], root / f"{aid}.blend")
    n = 1 if new else 0
    for rel, info in blend.get("include", {}).items():
        _, was_new = download(info["url"], root / rel)
        n += 1 if was_new else 0
    print(f"  {aid:28s} {p.stat().st_size/1e6:5.1f} MB  +{len(blend.get('include', {}))} textura"
          f"{'  (uj)' if n else '  (mar megvolt)'}")
    return p


def fetch_hdri(aid):
    files = api(f"/files/{aid}")
    hdr = files.get("hdri", {}).get(RES_HDRI, {}).get("hdr")
    if not hdr:
        print(f"  [!] {aid}: nincs {RES_HDRI} hdr")
        return None
    p, new = download(hdr["url"], STORE / "hdris" / f"{aid}.hdr")
    print(f"  {aid:28s} {p.stat().st_size/1e6:5.1f} MB{'  (uj)' if new else '  (mar megvolt)'}")
    return p


def cmd_fetch(a):
    print("modellek:")
    models = [fetch_model(m) for m in (a.models or KIT_MODELS)]
    print("hdri:")
    hdris = [fetch_hdri(h) for h in (a.hdris or KIT_HDRIS)]
    man = {"source": "polyhaven.com", "licence": "CC0",
           "models": [m.name for m in models if m], "hdris": [h.name for h in hdris if h]}
    (STORE / "MANIFEST.json").write_text(json.dumps(man, indent=1))
    print(f"\n{STORE}")


def cmd_list(a):
    assets = api(f"/assets?t={a.type}")
    q = a.query.lower()
    for k, v in sorted(assets.items()):
        blob = (k + " " + v.get("name", "") + " " + " ".join(v.get("tags", []))).lower()
        if q in blob:
            print(f"  {k:34s} {v.get('name','')}")


ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
f = sub.add_parser("fetch"); f.add_argument("--models", nargs="*"); f.add_argument("--hdris", nargs="*")
f.set_defaults(fn=cmd_fetch)
l = sub.add_parser("list"); l.add_argument("query"); l.add_argument("--type", default="models")
l.set_defaults(fn=cmd_list)
a = ap.parse_args(); a.fn(a)
