#!/usr/bin/env python3
"""Turn the Marketplace Insights dumps into one keyword database.

Reads the raw_*.txt / headline_measures.txt files in ../data/keywords/ and
writes keywords.json + a ranked report. Every record carries:
  term, searches, results, ratio (searches per 1000 listings), trend, source seed.
"""
import json, re, pathlib, statistics as st

D = pathlib.Path(__file__).resolve().parent.parent / "data" / "keywords"


def num(s):
    """'2.6k' -> 2600, '1.3M' -> 1300000, '514' -> 514"""
    s = s.strip().replace(",", "")
    if not s:
        return None
    m = re.match(r"^([\d.]+)\s*([kKmM]?)$", s)
    if not m:
        return None
    v = float(m.group(1))
    return int(v * {"": 1, "k": 1e3, "K": 1e3, "m": 1e6, "M": 1e6}[m.group(2)])


def pct(s):
    s = (s or "").strip().replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


db = {}


def add(term, searches, results, trend=None, seed=None):
    term = term.strip().lower()
    s, r = num(searches), num(results)
    if not term or s is None or r is None or r == 0:
        return
    rec = db.get(term)
    # prefer a record that has a trend (headline measurement) over a bare
    # related-table row, and keep the first seed that surfaced it
    if rec and rec.get("trend") is not None and trend is None:
        rec.setdefault("seeds", []).append(seed) if seed else None
        return
    db[term] = {
        "term": term, "searches": s, "results": r,
        "ratio": round(1000 * s / r, 1),
        "trend": pct(trend) if trend else (rec or {}).get("trend"),
        "seeds": sorted(set((rec or {}).get("seeds", []) + ([seed] if seed else []))),
    }


for f in sorted(D.glob("raw_*.txt")):
    for line in f.read_text().splitlines():
        if ">>>" not in line:
            continue
        head, rest = line.split(">>>", 1)
        h = head.strip().split("|")
        if len(h) == 4:
            add(h[0], h[1], h[3], h[2], seed=h[0].strip().lower())
        seed = h[0].strip().lower()
        for item in rest.split(";"):
            p = item.split("|")
            if len(p) == 3:
                add(p[0], p[1], p[2], seed=seed)

hm = D / "headline_measures.txt"
if hm.exists():
    for line in hm.read_text().splitlines():
        p = line.split("|")
        if len(p) == 4:
            add(p[0], p[1], p[3], p[2], seed="headline")

rows = sorted(db.values(), key=lambda r: -r["ratio"])
json.dump(rows, open(D / "keywords.json", "w"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- report
FILE_INTENT = ("svg", "dxf", "cut file", "cutting file", "cricut", "glowforge",
               "laser cut", "template", "digital download", "papercraft",
               "clipart", "png", "stencil", "pattern", "vector")
BASE = db.get("layered svg", {}).get("ratio", 6.3)

print(f"{len(rows)} kulcsszo az adatbazisban")
print(f"alapertek: layered svg = {BASE} kereses/1000 listing")
print()
print("=" * 88)
print("A LEGJOBB ARANYU FAJLSZANDEKU KIFEJEZESEK (min. 60 kereses, hogy ne zaj legyen)")
print(f"{'kifejezes':34}{'kereses':>9}{'talalat':>10}{'ker/1000':>10}{'x alap':>8}{'trend':>8}")
fi = [r for r in rows if any(k in r["term"] for k in FILE_INTENT) and r["searches"] >= 60]
for r in fi[:30]:
    t = f"{r['trend']:+.0f}%" if r["trend"] is not None else ""
    print(f"{r['term']:34}{r['searches']:>9,}{r['results']:>10,}{r['ratio']:>10.1f}"
          f"{r['ratio']/BASE:>7.0f}x{t:>8}")

print()
print("=" * 88)
print("TERMEK-SZANDEKU KIFEJEZESEK a legjobb aranyokkal (mas piac, de jelzes ertekű)")
print(f"{'kifejezes':34}{'kereses':>9}{'talalat':>10}{'ker/1000':>10}{'trend':>8}")
pi = [r for r in rows if not any(k in r["term"] for k in FILE_INTENT) and r["searches"] >= 100]
for r in pi[:15]:
    t = f"{r['trend']:+.0f}%" if r["trend"] is not None else ""
    print(f"{r['term']:34}{r['searches']:>9,}{r['results']:>10,}{r['ratio']:>10.1f}{t:>8}")

print()
print("=" * 88)
print("ELOSZLAS")
rr = [r["ratio"] for r in rows]
print(f"   median arany: {st.median(rr):.1f}   felso decilis: {sorted(rr)[int(len(rr)*.9)]:.1f}")
print(f"   az alapertek ({BASE}) folott: {sum(1 for x in rr if x > BASE)}/{len(rr)} kulcsszo")
