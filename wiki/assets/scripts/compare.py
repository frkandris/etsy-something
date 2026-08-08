#!/usr/bin/env python3
"""Layered wall art vs functional laser-cut objects, on the same basis."""
import json, statistics as st, datetime as dt

USD = 316.33
NOW = dt.datetime(2026, 8, 7)
med = lambda a: st.median(a) if a else 0


def build(details, search, key_p="p"):
    out = []
    for s in details:
        q = search.get(s["shop_name"], {})
        if not q.get(key_p):
            continue
        created = dt.datetime.fromtimestamp(s["create_date"], dt.UTC).replace(tzinfo=None)
        months = max(1, (NOW - created).days / 30.44)
        price = st.median(q[key_p])
        lst = st.median(q["op"]) if q.get("op") else None
        out.append({
            "shop": s["shop_name"], "country": s.get("country_code") or "?",
            "age_y": (NOW - created).days / 365,
            "listings": s.get("active_listing_count") or 0,
            "sold": s.get("sold_count") or 0,
            "price": price, "disc": (1 - price / lst) if lst else 0,
            "rev": (s.get("sold_count") or 0) / months * price * USD,
        })
    return out


fn = build(json.load(open("fn_shopdetails.json")), json.load(open("fn_shops.json")))
lay = json.load(open("layered_adjusted.json"))

print("=" * 74)
print("KET SZEGMENS UGYANAZON A MERCEN")
print(f"{'':34}{'layered':>18}{'funkcionalis':>18}")
print(f"{'boltok 500 listingbol':34}{173:>18}{285:>18}")
print(f"{'szakosodott (>=2-3 talalat)':34}{65:>18}{73:>18}")
print(f"{'median elad. ar USD':34}{med([r['price'] for r in lay]):>18.2f}"
      f"{med([r['price'] for r in fn]):>18.2f}")
print(f"{'median kedvezmeny':34}{med([r['disc'] for r in lay])*100:>17.0f}%"
      f"{med([r['disc'] for r in fn])*100:>17.0f}%")
print(f"{'median listing':34}{med([r['listings'] for r in lay]):>18,.0f}"
      f"{med([r['listings'] for r in fn]):>18,.0f}")
print(f"{'median bevetel HUF/ho (nyers)':34}{med([r['rev_hu'] for r in lay]):>18,.0f}"
      f"{med([r['rev'] for r in fn]):>18,.0f}")
print(f"{'median HUF/listing':34}"
      f"{med([r['rev_hu']/r['listings'] for r in lay if r['listings']]):>18,.0f}"
      f"{med([r['rev']/r['listings'] for r in fn if r['listings']]):>18,.0f}")

print()
print("MERETELOSZLAS")
for lo, hi, lab in [(1e6, 9e9, ">1M HUF/ho"), (5e5, 1e6, "500k-1M"),
                    (2e5, 5e5, "200-500k"), (0, 2e5, "<200k")]:
    a = [r for r in lay if lo <= r["rev_hu"] < hi]
    b = [r for r in fn if lo <= r["rev"] < hi]
    print(f"   {lab:14} layered {len(a):>3} ({100*len(a)/len(lay):>2.0f}%)   "
          f"funkcionalis {len(b):>3} ({100*len(b)/len(fn):>2.0f}%)")

print()
print("BELEPESI ESELY, 3 evnel fiatalabbak")
for name, rows, k in (("layered", lay, "rev_hu"), ("funkcionalis", fn, "rev")):
    y = [r for r in rows if r["age_y"] < 3]
    over = [r for r in y if r[k] >= 5e5]
    print(f"   {name:14} {len(y):>3} fiatal bolt, ebbol {len(over)} ({100*len(over)/len(y):.0f}%) "
          f"van 500k folott   median {med([r[k] for r in y]):>9,.0f} HUF/ho")

print()
print("ORSZAGOK - funkcionalis szegmens")
c = {}
for r in fn:
    c[r["country"]] = c.get(r["country"], 0) + 1
print("   " + "  ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:8]))

print()
print("FUNKCIONALIS SZEGMENS - TOP 10")
print(f"   {'bolt':24}{'HUF/ho':>11}{'listing':>8}{'HUF/listing':>12}{'ar$':>7}{'akcio':>7}{'ev':>5}  orsz")
for r in sorted(fn, key=lambda r: -r["rev"])[:10]:
    print(f"   {r['shop']:24}{r['rev']:>11,.0f}{r['listings']:>8}"
          f"{(r['rev']/r['listings'] if r['listings'] else 0):>12,.0f}"
          f"{r['price']:>7.2f}{r['disc']*100:>6.0f}%{r['age_y']:>5.1f}  {r['country']}")
