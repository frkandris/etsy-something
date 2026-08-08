#!/usr/bin/env python3
"""Rebuild every headline number with the corrections from the 2026-08-08 audit.

Fixes applied:
  - specialist filter counts DISTINCT listings, not search-result rows
  - theme classifier uses word boundaries ('man' no longer matches 'mandala')
  - review signals report seller concentration, not just listing count
"""
import json, glob, os, re, collections, statistics as st, pathlib

D = pathlib.Path(__file__).resolve().parent.parent / "data"
med = lambda a: st.median(a) if a else 0

# ---------------------------------------------------------------- population
search = []
for f in ["multilayer_svg", "3d_layered_mandala_svg", "3d_multilayer_svg_dxf",
          "layered_svg_laser_cut_file", "mls_search"]:
    p = D / f"{f}.json"
    if p.exists():
        search += json.load(open(p))
distinct = collections.defaultdict(set)
for r in search:
    distinct[r["shopName"]].add(r.get("url") or r["title"])

lay = {x["shop"]: x for x in json.load(open(D / "layered_adjusted.json"))}
SPEC = {s for s in lay if len(distinct.get(s, ())) >= 3}
VER = {s for s in SPEC if lay[s]["share"] >= 0.8}
print(f"POPULACIO dedupolva: specialista {len(SPEC)} (volt 65), igazolt {len(VER)} (volt 33)")
V = [lay[s] for s in VER]
print(f"   median korrigalt bevetel: {med([x['adj'] for x in V]):,.0f} HUF/ho (volt 320 156)")
rr = sorted(x["adj"] for x in V)
print(f"   felso kvartilis: {rr[int(len(rr)*.75)]:,.0f}")
for lo, hi, lab in [(2e6, 9e9, ">2M"), (1e6, 2e6, "1-2M"), (5e5, 1e6, "500k-1M"),
                    (2e5, 5e5, "200-500k"), (0, 2e5, "<200k")]:
    print(f"   {lab:10} {sum(1 for x in V if lo <= x['adj'] < hi)}")

print("\nAR vs EREDMENY (dedupolt igazolt populacio)")
for lo, hi, lab in [(0, 4, "<$4"), (4, 7, "$4-7"), (7, 12, "$7-12"), (12, 999, "$12+")]:
    g = [x for x in V if lo <= x["price"] < hi]
    if not g:
        continue
    print(f"   {lab:8} n={len(g):>2}  median {med([x['adj'] for x in g]):>9,.0f} HUF/ho  "
          f"{med([x['adj']/x['listings'] for x in g if x['listings']]):>7,.0f} HUF/listing  "
          f"eladas/ho {med([x['sold_per_mo'] for x in g]):>6.0f}")

print("\nKEDVEZMENY (dedupolt)")
for lo, hi, lab in [(0, .001, "nincs"), (.001, .35, "<35%"), (.35, .55, "35-55%"), (.55, 1, "55%+")]:
    g = [x for x in V if lo <= x["disc"] < hi]
    if not g:
        continue
    print(f"   {lab:8} n={len(g):>2}  median {med([x['adj'] for x in g]):>9,.0f} HUF/ho  "
          f"{med([x['adj']/x['listings'] for x in g if x['listings']]):>7,.0f} HUF/listing")

print("\nKATALOGUSMERET (dedupolt)")
for lo, hi, lab in [(0, 100, "<100"), (100, 300, "100-300"), (300, 700, "300-700"), (700, 9e9, "700+")]:
    g = [x for x in V if lo <= x["listings"] < hi]
    if not g:
        continue
    print(f"   {lab:10} n={len(g):>2}  median {med([x['adj'] for x in g]):>9,.0f}  "
          f"{med([x['adj']/x['listings'] for x in g]):>7,.0f} HUF/listing")

print("\nORSZAG (dedupolt igazolt)")
EU = ("DE", "FR", "LV", "LT", "GB", "CZ", "IT", "ES", "NL", "PL", "RO", "BG", "HU", "AT")
LC = ("VN", "PK", "TR", "IN", "ID", "BD", "PH", "UA", "RU")
for name, cc in (("Europa", EU), ("alacsony koltsegu", LC)):
    g = [x for x in V if x["country"] in cc]
    if g:
        print(f"   {name:18} n={len(g):>2}  median {med([x['adj'] for x in g]):>9,.0f}  "
              f"{med([x['adj']/x['listings'] for x in g]):>7,.0f} HUF/listing  "
              f"ar ${med([x['price'] for x in g]):.2f}  akcio {med([x['disc'] for x in g])*100:.0f}%")

# ---------------------------------------------------------------- themes
print("\n" + "=" * 70)
print("TEMAK szohatarral (a 'man' in 'mandala' hiba javitva)")
cat = json.load(open(D / "catalog_sample.json"))
titles = [r["title"].lower() for r in cat if r["shop_name"] in VER]
TH = {
    "mandala / zentangle": r"mandala|zentangle|rosette",
    "allat": r"\b(dog|cat|wolf|lion|tiger|horse|deer|bird|owl|elephant|dragon|fish|butterfly|bear|fox)\b|animal",
    "termeszet / novény": r"\b(tree|forest|leaf|rose|nature|mountain|wave|sea|flower|floral)\b",
    "vallasi": r"\b(jesus|cross|christ|buddha|mary|church)\b|religio|islam|allah",
    "unnep / szezon": r"christmas|halloween|easter|valentine|pumpkin|santa|snowflake",
    "ember / portre": r"\b(woman|man|men|face|portrait|girl|couple|family)\b",
    "jarmu": r"\b(car|truck|motorcycle|bike|plane|ship|train|boat)\b",
}
for k, pat in sorted(TH.items(), key=lambda kv: -sum(bool(re.search(kv[1], t)) for t in titles)):
    n = sum(bool(re.search(pat, t)) for t in titles)
    print(f"   {k:22}{n:>5} ({100*n/len(titles):>4.1f}%)")

# ---------------------------------------------------------------- reviews
print("\n" + "=" * 70)
print("REVIEW-JELEK ELADO-KONCENTRACIOVAL")
rev = json.load(open(D / "reviews.json"))
def sig(name, words):
    hit = [r for r in rev if any(w in (r.get("listing_title") or "").lower() for w in words)]
    sel = collections.Counter(r.get("product_details", {}).get("seller_name") for r in hit)
    lst = len({r.get("listing_title") for r in hit})
    top = sel.most_common(1)[0] if sel else ("-", 0)
    print(f"   {name:22}{len(hit):>4} review  {lst:>3} listing  {len(sel):>2} elado   "
          f"legnagyobb: {top[1]}/{len(hit)} ({top[0]})")
for n, w in [("mecses/lampas", ("tealight", "lantern", "candle holder", "night lamp")),
             ("suncatcher", ("suncatcher",)), ("mirror", ("mirror",)),
             ("kereszt", ("cross",)), ("hazafias", ("patriotic", "american flag", " flag")),
             ("cow / western", ("cow", "cowboy", "western")), ("koponya", ("skull",)),
             ("ora", ("clock",)), ("ajandekdoboz", ("gift box", "wine bottle"))]:
    sig(n, w)
