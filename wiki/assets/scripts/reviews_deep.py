#!/usr/bin/env python3
"""What the 2190 reviews say once you stop guessing categories in advance."""
import json, collections, re, pathlib, datetime as dt

D = pathlib.Path(__file__).resolve().parent.parent / "data"
rev = json.load(open(D / "reviews.json"))          # 33 verified layered shops
cat = json.load(open(D / "catalog_sample.json"))
verified = {r["shop"] for r in json.load(open(D / "layered_adjusted.json")) if r["share"] >= 0.8}

sold = collections.Counter()
dated = []
for r in rev:
    t = (r.get("listing_title") or "").strip()
    if not t:
        continue
    sold[t] += 1
    if r.get("date"):
        dated.append((r["date"][:10], t))
R = sum(sold.values())

supply = collections.Counter()
for r in cat:
    if r["shop_name"] in verified:
        supply[r["title"]] += 1
S = sum(supply.values())

STOP = set("""svg dxf cnc file files laser cut cutting cricut glowforge vector digital
download instant for the and with of layered multilayer multi layer wood wooden plywood
template designs design diy craft pdf png ai eps jpg bundle set pack router lightburn
xtool silhouette cameo commercial use printable making art wall decor home 3d cutfile
cut-file paper papercut shadow box shadowbox""".split())


def terms(title, n=1):
    ws = [w for w in re.findall(r"[a-z][a-z'-]{2,}", title.lower()) if w not in STOP]
    if n == 1:
        return ws
    return [" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def freq(counter, total, n=1):
    c = collections.Counter()
    for title, k in counter.items():
        for t in set(terms(title, n)):
            c[t] += k
    return c, total


sw, _ = freq(sold, R)
sp, _ = freq(supply, S)

print(f"KERESLET-INDEX szavankent: (review-arany) / (listing-arany)")
print(f"csak ahol legalabb 8 review es 4 listing all mogotte\n")
print(f"{'szo':22}{'review':>8}{'listing':>9}{'index':>8}")
rows = []
for w, n in sw.items():
    m = sp.get(w, 0)
    if n >= 8 and m >= 4:
        rows.append((n / R / (m / S), w, n, m))
for idx, w, n, m in sorted(rows, reverse=True)[:22]:
    print(f"{w:22}{n:>8}{m:>9}{idx:>8.2f}")
print("\n   ...és a másik vég (túlkínált):")
for idx, w, n, m in sorted(rows)[:8]:
    print(f"{w:22}{n:>8}{m:>9}{idx:>8.2f}")

print()
print("=" * 74)
print("AMIT A KINALAT EGYALTALAN NEM FED LE, de fogy")
print("(legalabb 5 review, 0 vagy 1 listing a mintaban)")
gaps = []
for w, n in sw.items():
    if n >= 5 and sp.get(w, 0) <= 1:
        gaps.append((n, w, sp.get(w, 0)))
for n, w, m in sorted(gaps, reverse=True)[:26]:
    print(f"   {w:26}{n:>5} review   {m} listing")

print()
print("=" * 74)
print("SZEMELYRE SZABAS / EGYEDI RENDELES")
PERS = ("custom", "personaliz", "name", "monogram", "memorial", "wedding",
        "anniversary", "family", "gift for")
pn = sum(k for t, k in sold.items() if any(w in t.lower() for w in PERS))
ps = sum(k for t, k in supply.items() if any(w in t.lower() for w in PERS))
print(f"   review: {pn} ({100*pn/R:.1f}%)   listing: {ps} ({100*ps/S:.1f}%)   "
      f"index: {(pn/R)/(ps/S):.2f}")

print()
print("FOGLALKOZAS / HIVATAS")
OCC = ("firefighter", "nurse", "police", "veteran", "military", "teacher", "doctor",
       "trucker", "farmer", "welder", "pilot", "army", "navy", "hero")
on = sum(k for t, k in sold.items() if any(w in t.lower() for w in OCC))
os_ = sum(k for t, k in supply.items() if any(w in t.lower() for w in OCC))
print(f"   review: {on} ({100*on/R:.1f}%)   listing: {os_} ({100*os_/S:.1f}%)   "
      f"index: {((on/R)/(os_/S)) if os_ else float('inf'):.2f}")

print()
print("=" * 74)
print("IDOBELISEG — az utolso 3 honap legtobbet ertekelt listingjei")
CUT = "2026-05-08"
rec = collections.Counter(t for d, t in dated if d >= CUT)
print(f"   {sum(rec.values())} review 2026-05-08 ota\n")
for t, n in rec.most_common(12):
    print(f"   {n:>3}x  {t[:84]}")
