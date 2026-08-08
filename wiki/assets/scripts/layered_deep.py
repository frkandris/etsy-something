#!/usr/bin/env python3
"""Everything the data says about the layered niche, on verified shops only."""
import json, re, statistics as st, collections

med = lambda a: st.median(a) if a else 0
rows = json.load(open("layered_adjusted.json"))
CLEAN = [r for r in rows if r["share"] >= 0.8]          # >=80% layered catalogue
cat = json.load(open("catalog_sample.json"))
import glob
search = []
skip = {"build1.json","rows-2026.json","salesdoe-2026.json","niche_shops.json",
        "niche_rows.json","shoptest.json","t2.json","old_shop_listings.json",
        "shopreq.json","shopreq2.json","oldreq.json","niche_shopdetails.json",
        "niche_shopdetails2.json","catalog_sample.json","catreq.json",
        "layered_adjusted.json","fn_shops.json","fn_shopdetails.json",
        "fn_catalog.json","fnreq.json","fncatreq.json"}
for f in glob.glob("*.json"):
    if f in skip: continue
    try: d = json.load(open(f))
    except Exception: continue
    if isinstance(d, list) and d and isinstance(d[0], dict) and "shopName" in d[0]:
        search += d

print("=" * 76)
print(f"A TISZTA POPULACIO: {len(CLEAN)} bolt (katalogusuk >=80%-a layered)")
print()

print("1. MERET")
rev = sorted((r["adj"] for r in CLEAN), reverse=True)
for lo, hi, lab in [(2e6, 9e9, ">2M"), (1e6, 2e6, "1-2M"), (5e5, 1e6, "500k-1M"),
                    (2e5, 5e5, "200-500k"), (0, 2e5, "<200k")]:
    n = [x for x in rev if lo <= x < hi]
    print(f"   {lab:10} {len(n):3} bolt  {'#'*len(n)}")
print(f"   median {med(rev):,.0f} HUF/ho   felso kvartilis {sorted(rev)[int(len(rev)*.75)]:,.0f}")

print()
print("2. AR")
for lo, hi, lab in [(0, 4, "<$4"), (4, 7, "$4-7"), (7, 12, "$7-12"), (12, 999, "$12+")]:
    g = [r for r in CLEAN if lo <= r["price"] < hi]
    if not g: continue
    print(f"   {lab:8} {len(g):3} bolt  median {med([r['adj'] for r in g]):>10,.0f} HUF/ho  "
          f"{med([r['adj']/r['listings'] for r in g if r['listings']]):>7,.0f} HUF/listing  "
          f"median {med([r['listings'] for r in g]):>5,.0f} listing")

print()
print("3. KEDVEZMENY")
for lo, hi, lab in [(0, .001, "nincs"), (.001, .35, "<35%"), (.35, .55, "35-55%"), (.55, 1, "55%+")]:
    g = [r for r in CLEAN if lo <= r["disc"] < hi]
    if not g: continue
    print(f"   {lab:8} {len(g):3} bolt  median {med([r['adj'] for r in g]):>10,.0f} HUF/ho  "
          f"{med([r['adj']/r['listings'] for r in g if r['listings']]):>7,.0f} HUF/listing  "
          f"ar ${med([r['price'] for r in g]):.2f}")

print()
print("4. KATALOGUSMERET")
for lo, hi, lab in [(0, 100, "<100"), (100, 300, "100-300"), (300, 700, "300-700"), (700, 9e9, "700+")]:
    g = [r for r in CLEAN if lo <= r["listings"] < hi]
    if not g: continue
    print(f"   {lab:10} {len(g):3} bolt  median {med([r['adj'] for r in g]):>10,.0f} HUF/ho  "
          f"{med([r['adj']/r['listings'] for r in g]):>7,.0f} HUF/listing")

print()
print("5. KOR / BELEPES")
for lo, hi, lab in [(0, 1.5, "<1.5 ev"), (1.5, 3, "1.5-3 ev"), (3, 5, "3-5 ev"), (5, 99, "5+ ev")]:
    g = [r for r in CLEAN if lo <= r["age_y"] < hi]
    if not g: continue
    print(f"   {lab:10} {len(g):3} bolt  median {med([r['adj'] for r in g]):>10,.0f} HUF/ho  "
          f"median {med([r['listings'] for r in g]):>5,.0f} listing  "
          f"tempo {med([r['listings']/(r['age_y']*12) for r in g]):>5.1f} listing/ho")

print()
print("6. ORSZAG")
c = collections.Counter(r["country"] for r in CLEAN)
print("   " + "   ".join(f"{k}:{v}" for k, v in c.most_common(10)))
eu = [r for r in CLEAN if r["country"] in ("DE","FR","LV","LT","GB","CZ","IT","ES","NL","PL","RO","BG","HU","AT")]
lc = [r for r in CLEAN if r["country"] in ("VN","PK","TR","IN","ID","BD","PH","UA","RU")]
print(f"   Europa (nyugat/kozep): {len(eu)} bolt, median {med([r['adj'] for r in eu]):,.0f} HUF/ho, "
      f"{med([r['adj']/r['listings'] for r in eu]):,.0f} HUF/listing, ar ${med([r['price'] for r in eu]):.2f}, "
      f"akcio {med([r['disc'] for r in eu])*100:.0f}%")
print(f"   Alacsony koltsegu:     {len(lc)} bolt, median {med([r['adj'] for r in lc]):,.0f} HUF/ho, "
      f"{med([r['adj']/r['listings'] for r in lc]):,.0f} HUF/listing, ar ${med([r['price'] for r in lc]):.2f}, "
      f"akcio {med([r['disc'] for r in lc])*100:.0f}%")

print()
print("7. A TELJES TISZTA LISTA (korrigalt bevetel szerint)")
print(f"   {'bolt':24}{'HUF/ho':>10}{'listing':>8}{'HUF/list':>9}{'ar$':>7}{'akcio':>6}{'ev':>5}{'lay%':>6}  orsz")
for r in sorted(CLEAN, key=lambda r: -r["adj"]):
    print(f"   {r['shop']:24}{r['adj']:>10,.0f}{r['listings']:>8}"
          f"{r['adj']/r['listings'] if r['listings'] else 0:>9,.0f}{r['price']:>7.2f}"
          f"{r['disc']*100:>5.0f}%{r['age_y']:>5.1f}{r['share']*100:>5.0f}%  {r['country']}")

# ---------------- title corpus -------------------------------------------
clean_names = {r["shop"] for r in CLEAN}
titles = [r["title"] for r in cat if r["shop_name"] in clean_names]
low = [t.lower() for t in titles]
print()
print("=" * 76)
print(f"MIT IRNAK A CIMEKBE ({len(titles)} listing a tiszta boltoktol)")

print()
print("8. GEP / SZOFTVER EMLITES")
for k, pat in [("Cricut", "cricut"), ("Glowforge", "glowforge"), ("LightBurn", "lightburn"),
               ("xTool", "xtool"), ("CNC router", "cnc"), ("Silhouette", "silhouette"),
               ("lezer altalaban", "laser")]:
    n = sum(pat in t for t in low)
    print(f"   {k:18} {n:>4} listing ({100*n/len(low):>2.0f}%)")

print()
print("9. FAJLFORMATUM")
for k in ["svg", "dxf", "cdr", "ai", "pdf", "eps", "lbrn", "png"]:
    n = sum(bool(re.search(rf"\b{k}\b", t)) for t in low)
    print(f"   {k.upper():6} {n:>4} ({100*n/len(low):>2.0f}%)")

print()
print("10. RETEGSZAM A CIMBEN")
layers = [int(m) for t in low for m in re.findall(r"(\d{1,2})\s*[- ]?layers?\b", t)
          if 2 <= int(m) <= 30]
if layers:
    cc = collections.Counter(layers)
    print("   " + "  ".join(f"{k}:{v}" for k, v in sorted(cc.items())))
    print(f"   emliti a retegszamot: {len(layers)} listing, median {med(layers):.0f} reteg")

print()
print("11. TEMAK a tiszta boltok katalogusaban")
THEMES = {
    "allat": ("dog","cat","wolf","lion","tiger","horse","deer","bird","owl","elephant",
              "dragon","fish","butterfly","bear","animal","fox","panda"),
    "mandala/ornamens": ("mandala","ornament","rosette","geometric"),
    "vallasi": ("jesus","cross","christ","buddha","mary","religio","islam","allah","om "),
    "unnep/szezon": ("christmas","halloween","easter","valentine","thanksgiving",
                     "pumpkin","santa","snowflake","mother","father"),
    "termeszet/novény": ("tree","flower","forest","leaf","rose","nature","mountain","wave","sea"),
    "jarmu": ("car","truck","motorcycle","bike","plane","ship","train","boat"),
    "ember/portre": ("woman","man","face","portrait","girl","couple","family"),
    "fantasy/pop": ("skull","superhero","anime","gothic","fantasy","dragon","horror"),
}
for name, ws in sorted(THEMES.items(), key=lambda kv: -sum(any(w in t for w in kv[1]) for t in low)):
    n = sum(any(w in t for w in ws) for t in low)
    print(f"   {name:20} {n:>4} listing ({100*n/len(low):>2.0f}%)")

print()
print("12. BUNDLE vs EGYEDI")
b = sum(bool("bundle" in t or "pack" in t or "set of" in t or re.search(r"\d{2,}\s*(designs|files)", t)) for t in low)
print(f"   bundle/pack/csomag: {b} listing ({100*b/len(low):.0f}%)")
bp = [r["price"] for r in search if r["shopName"] in clean_names
      and ("bundle" in r["title"].lower() or "pack" in r["title"].lower())]
sp = [r["price"] for r in search if r["shopName"] in clean_names
      and not ("bundle" in r["title"].lower() or "pack" in r["title"].lower())]
print(f"   median ar bundle: ${med(bp):.2f}   egyedi: ${med(sp):.2f}")

print()
print("13. COMMERCIAL LICENCE")
n = sum("commercial" in t for t in low)
print(f"   emliti: {n} listing ({100*n/len(low):.0f}%)")
shops_cl = {r["shop_name"] for r in cat if r["shop_name"] in clean_names
            and "commercial" in r["title"].lower()}
g = [r for r in CLEAN if r["shop"] in shops_cl]
ng = [r for r in CLEAN if r["shop"] not in shops_cl]
print(f"   emlito boltok:     {len(g):2}  median {med([r['adj'] for r in g]):>10,.0f} HUF/ho  "
      f"{med([r['adj']/r['listings'] for r in g]):>7,.0f} HUF/listing")
print(f"   nem emlito:        {len(ng):2}  median {med([r['adj'] for r in ng]):>10,.0f} HUF/ho  "
      f"{med([r['adj']/r['listings'] for r in ng]):>7,.0f} HUF/listing")
