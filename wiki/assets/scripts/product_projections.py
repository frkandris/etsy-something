#!/usr/bin/env python3
"""The two remaining parked product projections, measured on existing data.

1. flat print  - the layered artwork sold as printable art instead of a cut file
2. gift box    - the layered pattern applied to the side of a box
"""
import json, collections, pathlib

D = pathlib.Path(__file__).resolve().parent.parent / "data"
rev = json.load(open(D / "reviews.json"))            # 33 verified layered shops
ncrev = json.load(open(D / "nc_reviews.json"))       # 16 norse/celtic shops
cat = json.load(open(D / "catalog_sample.json"))
fncat = json.load(open(D / "fn_catalog.json"))       # 73 functional-segment shops
verified = {r["shop"] for r in json.load(open(D / "layered_adjusted.json")) if r["share"] >= 0.8}

sold, nsold = collections.Counter(), collections.Counter()
for r in rev:
    t = (r.get("listing_title") or "").strip()
    if t:
        sold[t] += 1
for r in ncrev:
    t = (r.get("listing_title") or "").strip()
    if t:
        nsold[t] += 1
supply = collections.Counter(r["title"] for r in cat if r["shop_name"] in verified)
fnsupply = collections.Counter(r["title"] for r in fncat)
R, S, NR, FS = sum(sold.values()), sum(supply.values()), sum(nsold.values()), sum(fnsupply.values())


def probe(name, words, exclude=()):
    def hit(t):
        tl = t.lower()
        return any(w in tl for w in words) and not any(x in tl for x in exclude)
    rn = sum(k for t, k in sold.items() if hit(t))
    rl = len([t for t in sold if hit(t)])
    sn = sum(k for t, k in supply.items() if hit(t))
    nn = sum(k for t, k in nsold.items() if hit(t))
    nl = len([t for t in nsold if hit(t)])
    fn = sum(k for t, k in fnsupply.items() if hit(t))
    idx = (rn / R) / (sn / S) if sn else None
    print(f"\n{name}")
    print(f"   layered boltok:   {rn:>4} review / {rl:>3} listing   |   kinalat {sn:>3} "
          f"({100*sn/S:.1f}%)   index {idx if idx is None else round(idx,2)}")
    print(f"   norse/kelta boltok:{nn:>4} review / {nl:>3} listing")
    print(f"   funkcionalis szegmens kinalata: {fn} listing ({100*fn/FS:.1f}%)")
    ex = sorted(((k, t) for t, k in sold.items() if hit(t)), reverse=True)[:5]
    ex += sorted(((k, t) for t, k in nsold.items() if hit(t)), reverse=True)[:5]
    for k, t in ex[:8]:
        print(f"      {k:>3}x  {t[:80]}")


print("=" * 78)
print("1. SIK PRINT — a retegzett grafika nyomtathato kepkent")
probe("print / poster / printable",
      ("printable", "print art", "art print", "wall print", "poster", "digital print",
       "instant print", "printable art"),
      exclude=("blueprint",))
probe("csak 'print' szo (tagabb)", (" print",), exclude=("blueprint", "3d print", "printer"))

print()
print("=" * 78)
print("2. AJANDEKDOBOZ / TAROLO — a retegzett minta doboz oldalan")
probe("box (gift/storage/keepsake), a shadow box kivetelevel",
      ("gift box", "storage box", "keepsake box", "jewelry box", "wooden box",
       "box svg", "trinket box", "memory box"),
      exclude=("shadow box", "shadowbox", "light box", "lightbox"))
probe("barmilyen 'box' a shadow box nelkul", ("box",),
      exclude=("shadow box", "shadowbox", "light box", "lightbox"))

print()
print("=" * 78)
print("3. VISZONYITAS — a mar igazolt iranyok ugyanezen a mercen")
probe("mecses / lampas", ("tealight", "lantern", "candle holder", "night lamp"))
probe("kereszt", ("cross",), exclude=("crossword",))
