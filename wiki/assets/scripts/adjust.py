#!/usr/bin/env python3
"""How much of each specialist shop's catalogue is actually layered."""
import json, statistics as st

cat = json.load(open("catalog_sample.json"))
nr = {x["shop"]: x for x in json.load(open("niche_rows.json"))}
LAY = ("multilayer", "multi-layer", "multi layer", "layered", " layer",
       "layers", "3d mandala", "shadow box")

shops = {}
for r in cat:
    shops.setdefault(r["shop_name"], []).append(r["title"].lower())

med = lambda a: st.median(a) if a else 0
rows = []
for s, ts in shops.items():
    x = nr[s]
    if not x["rev_hu"]:
        continue
    share = sum(any(k in t for k in LAY) for t in ts) / len(ts)
    rows.append({**x, "share": share, "n": len(ts), "adj": x["rev_hu"] * share})

print(f"{len(rows)} bolt, {len(cat)} mintavett listing")
print()
print("LAYERED RESZESEDES A KATALOGUSBAN")
for lo, hi, lab in [(0.8, 1.01, "80-100% (tiszta layered bolt)"),
                    (0.5, 0.8, "50-80%"), (0.2, 0.5, "20-50%"),
                    (0, 0.2, "<20% (mas a fo profil)")]:
    g = [r for r in rows if lo <= r["share"] < hi]
    print(f"   {lab:32} {len(g):3} bolt   "
          f"median nyers {med([r['rev_hu'] for r in g]):>10,.0f} -> "
          f"korrigalt {med([r['adj'] for r in g]):>10,.0f}")

print()
print(f"   median layered reszesedes: {med([r['share'] for r in rows])*100:.0f}%")
print(f"   osszes median: nyers {med([r['rev_hu'] for r in rows]):,.0f} -> "
      f"KORRIGALT {med([r['adj'] for r in rows]):,.0f} HUF/ho")

print()
print("A NEM AKCIOZO KLASZTER KORRIGALVA")
print(f"   {'bolt':22}{'layered%':>9}{'nyers':>11}{'korrigalt':>11}{'listing':>8}{'HUF/listing':>12}  orsz")
for r in sorted([r for r in rows if r["disc"] == 0], key=lambda r: -r["adj"]):
    print(f"   {r['shop']:22}{r['share']*100:>8.0f}%{r['rev_hu']:>11,.0f}"
          f"{r['adj']:>11,.0f}{r['listings']:>8}{r['adj']/r['listings']:>12,.0f}  {r['country']}")

print()
print("TOP 12 KORRIGALT BEVETEL SZERINT")
print(f"   {'bolt':22}{'layered%':>9}{'korrigalt':>11}{'listing':>8}{'ar$':>7}{'akcio':>7}{'ev':>5}  orsz")
for r in sorted(rows, key=lambda r: -r["adj"])[:12]:
    print(f"   {r['shop']:22}{r['share']*100:>8.0f}%{r['adj']:>11,.0f}{r['listings']:>8}"
          f"{r['price']:>7.2f}{r['disc']*100:>6.0f}%{r['age_y']:>5.1f}  {r['country']}")

print()
print("BELEPESI ESELY UJRA, korrigalt bevetellel (<3 ev)")
y = [r for r in rows if r["age_y"] < 3]
for lo, hi, lab in [(1e6, 9e9, ">1M"), (5e5, 1e6, "500k-1M"),
                    (2e5, 5e5, "200-500k"), (0, 2e5, "<200k")]:
    g = [r for r in y if lo <= r["adj"] < hi]
    print(f"   {lab:10} {len(g):3} ({100*len(g)/len(y):.0f}%)")

json.dump(rows, open("layered_adjusted.json", "w"), indent=1)
