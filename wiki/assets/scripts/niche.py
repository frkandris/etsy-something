#!/usr/bin/env python3
"""Multilayer / layered laser-cut SVG niche: the whole visible population."""
import json, statistics as st, datetime as dt

USD = 316.33
NOW = dt.datetime(2026, 8, 7)

search = json.load(open("niche_shops.json"))
shops = json.load(open("niche_shopdetails.json")) + json.load(open("niche_shopdetails2.json"))

rows = []
for s in shops:
    name = s["shop_name"]
    q = search.get(name, {})
    created = dt.datetime.utcfromtimestamp(s["create_date"])
    months = max(1, (NOW - created).days / 30.44)
    price = st.median(q["p"]) if q.get("p") else None
    lst = st.median(q["op"]) if q.get("op") else None
    disc = (1 - price / lst) if (price and lst) else 0
    sold = s.get("sold_count") or 0
    rows.append({
        "shop": name, "country": s.get("country_code") or "?",
        "created": created.date().isoformat(), "age_y": (NOW - created).days / 365,
        "listings": s.get("active_listing_count") or 0,
        "sold": sold, "open": s.get("is_open"),
        "rating": s.get("average_rating"), "reviews": s.get("total_rating_count") or 0,
        "price": price, "list_price": lst, "disc": disc,
        "hits": q.get("n", 0),
        # lifetime average monthly revenue at today's median sale price
        "rev_hu": (sold / months * price * USD) if price else None,
        "sold_per_mo": sold / months,
    })

live = [r for r in rows if r["rev_hu"]]
med = lambda a: st.median(a) if a else 0

print("=" * 78)
print(f"POPULACIO: {len(rows)} bolt (500 listing / 5 kereses top talalatai)")
print()
print("1. MERETELOSZLAS  (becsult atlagos HUF/ho a bolt teljes elettartamara)")
rev = sorted((r["rev_hu"] for r in live), reverse=True)
for label, lo in [(">2M HUF/ho", 2e6), ("1-2M", 1e6), ("500k-1M", 5e5),
                  ("200-500k", 2e5), ("50-200k", 5e4), ("<50k", 0)]:
    hi = {2e6: 9e9, 1e6: 2e6, 5e5: 1e6, 2e5: 5e5, 5e4: 2e5, 0: 5e4}[lo]
    n = sum(1 for x in rev if lo <= x < hi)
    print(f"   {label:12} {n:3} bolt  {'#'*n}")
print(f"   median: {med(rev):,.0f} HUF/ho   felso kvartilis: {sorted(rev)[int(len(rev)*.75)]:,.0f}")

print()
print("2. ORSZAG (top 8)")
c = {}
for r in rows:
    c[r["country"]] = c.get(r["country"], 0) + 1
for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:8]:
    print(f"   {k:4} {v:3} bolt ({100*v/len(rows):.0f}%)")

print()
print("3. KOR: mikor nyitottak?")
for lo, hi, lab in [(0, 1, "<1 ev"), (1, 2, "1-2 ev"), (2, 3, "2-3 ev"),
                    (3, 5, "3-5 ev"), (5, 99, "5+ ev")]:
    g = [r for r in rows if lo <= r["age_y"] < hi]
    gl = [r["rev_hu"] for r in g if r["rev_hu"]]
    print(f"   {lab:8} {len(g):3} bolt   median {med(gl):>10,.0f} HUF/ho   "
          f"median listing {med([r['listings'] for r in g]):>6,.0f}   "
          f"median eladas {med([r['sold'] for r in g]):>8,.0f}")

print()
print("4. BELEPESI ESELY: 3 evnel fiatalabb boltok eloszlasa")
young = sorted((r for r in rows if r["age_y"] < 3 and r["rev_hu"]),
               key=lambda r: -r["rev_hu"])
print(f"   {len(young)} fiatal bolt a mintaban")
for lo, lab in [(1e6, ">1M HUF/ho"), (5e5, "500k-1M"), (2e5, "200-500k"), (0, "<200k")]:
    hi = {1e6: 9e9, 5e5: 1e6, 2e5: 5e5, 0: 2e5}[lo]
    n = [r for r in young if lo <= r["rev_hu"] < hi]
    print(f"   {lab:12} {len(n):3} ({100*len(n)/len(young):.0f}%)")
print()
print("   A legjobb fiatalok:")
for r in young[:10]:
    print(f"     {r['shop']:24} {r['created']}  {r['rev_hu']:>10,.0f} HUF/ho  "
          f"{r['listings']:>5} listing  {r['sold']:>7,} eladas  {r['country']}  "
          f"ar ${r['price']:.2f} (-{r['disc']*100:.0f}%)")

print()
print("5. ARAZAS ES KEDVEZMENY (a niche normaja)")
pr = [r for r in rows if r["price"]]
print(f"   median eladasi ar:  ${med([r['price'] for r in pr]):.2f}")
print(f"   median listaar:     ${med([r['list_price'] for r in pr if r['list_price']]):.2f}")
d = [r["disc"] for r in pr if r["disc"] > 0]
print(f"   median kedvezmeny:  {med(d)*100:.0f}%   "
      f"({len(d)}/{len(pr)} bolt akciozik = {100*len(d)/len(pr):.0f}%)")

print()
print("6. BEZART BOLTOK a mintaban")
closed = [r for r in rows if not r["open"]]
print(f"   {len(closed)}/{len(rows)} ({100*len(closed)/len(rows):.0f}%)")

print()
print("7. TOP 15 A NICHE-BEN")
print(f"   {'bolt':24}{'HUF/ho':>11}{'listing':>8}{'eladas':>9}{'kor':>6}{'ar':>7}{'akcio':>7}  orsz")
for r in sorted(live, key=lambda r: -r["rev_hu"])[:15]:
    print(f"   {r['shop']:24}{r['rev_hu']:>11,.0f}{r['listings']:>8}{r['sold']:>9,}"
          f"{r['age_y']:>6.1f}{r['price']:>7.2f}{r['disc']*100:>6.0f}%  {r['country']}")

json.dump(rows, open("niche_rows.json", "w"), indent=1)
