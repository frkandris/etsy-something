#!/usr/bin/env python3
"""A hosszú farok szógyűjtemény karbantartója.

A gyűjtemény `wiki/assets/data/longtail/<csalad>.json` fájlokban él. Minden
kifejezéshez tartozik egy `measurements` lista, ami IDŐSOR: ugyanazt a szót
többször is meg lehet mérni, és a régi mérés megmarad. Ezért a fájl nőni tud
anélkül, hogy bármit felülírnánk.

  python longtail.py list                      — mit tartalmaz
  python longtail.py add <csalad> szo1 szo2    — új kifejezés(ek)
  python longtail.py todo [--limit 40]         — mit nem mértünk még (Insights-URL-ekkel)
  python longtail.py record <csalad> <szo> --searches 514 --results 11200
  python longtail.py rank [--min-searches 300] — a mért kifejezések rangsora

A `rank` a projekt mértékegységét használja: keresés / 1000 találat.
Alapérték: `layered svg` = 6,3. Zajküszöb: 300 keresés alatt a trend
értelmezhetetlen (findings/keyword-demand-sweep).
"""
import argparse, json, pathlib, sys, urllib.parse

D = pathlib.Path(__file__).resolve().parents[1] / "data" / "longtail"
INSIGHTS = "https://www.etsy.com/your/shops/me/marketplace-insights/search?query="


def families():
    return sorted(p.stem for p in D.glob("*.json"))


def load(fam):
    p = D / f"{fam}.json"
    if not p.exists():
        sys.exit(f"nincs ilyen csalad: {fam}  (van: {', '.join(families())})")
    return p, json.loads(p.read_text())


def save(p, d):
    d["entries"].sort(key=lambda e: e["term"])
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def query_of(d, term):
    return d.get("query_pattern", "{term}").replace("{term}", term)


def cmd_list(a):
    tot = mtot = 0
    print(f"{'csalad':22s}{'kifejezes':>10s}{'merve':>8s}  megjegyzes")
    for f in families():
        _, d = load(f)
        n = len(d["entries"])
        m = sum(1 for e in d["entries"] if e["measurements"])
        tot += n; mtot += m
        print(f"{f:22s}{n:>10d}{m:>8d}  {d.get('note','')[:60]}")
    print(f"{'OSSZESEN':22s}{tot:>10d}{mtot:>8d}  ({mtot/tot*100 if tot else 0:.1f}% merve)")


def cmd_add(a):
    p, d = load(a.family)
    have = {e["term"] for e in d["entries"]}
    new = [t for t in a.terms if t not in have]
    d["entries"] += [{"term": t, "measurements": []} for t in new]
    save(p, d)
    print(f"{a.family}: +{len(new)} uj ({len(a.terms)-len(new)} mar volt), "
          f"osszesen {len(d['entries'])}")


def cmd_todo(a):
    out = []
    for f in (a.family and [a.family] or families()):
        _, d = load(f)
        for e in d["entries"]:
            if not e["measurements"]:
                q = query_of(d, e["term"])
                out.append((f, e["term"], INSIGHTS + urllib.parse.quote(q)))
    for f, t, u in out[: a.limit]:
        print(f"{f:20s} {t:28s} {u}")
    print(f"-- {len(out)} meretlen kifejezes osszesen")


def cmd_record(a):
    p, d = load(a.family)
    e = next((x for x in d["entries"] if x["term"] == a.term), None)
    if e is None:
        e = {"term": a.term, "measurements": []}
        d["entries"].append(e)
    ratio = round(a.searches / a.results * 1000, 1) if a.results else None
    e["measurements"].append({"date": a.date, "searches": a.searches,
                              "results": a.results, "per_1000": ratio,
                              "trend_pct": a.trend})
    save(p, d)
    print(f"{a.family}/{a.term}: {a.searches} keres / {a.results} talalat = {ratio} per 1000")


def cmd_rank(a):
    rows = []
    for f in families():
        _, d = load(f)
        for e in d["entries"]:
            if not e["measurements"]:
                continue
            m = e["measurements"][-1]
            if m.get("per_1000") is None:
                continue
            rows.append((m["per_1000"], m["searches"], m["results"], f, e["term"], m["date"]))
    rows.sort(reverse=True)
    noisy = [r for r in rows if r[1] < a.min_searches]
    solid = [r for r in rows if r[1] >= a.min_searches]
    print(f"{'per1000':>8}{'keres':>8}{'talalat':>10}  {'csalad':18s}kifejezes")
    print(f"-- {a.min_searches}+ keresessel ({len(solid)} db, ertelmezheto) --")
    for r in solid[: a.limit]:
        print(f"{r[0]:>8.1f}{r[1]:>8d}{r[2]:>10d}  {r[3]:18s}{r[4]}")
    print(f"-- zajkuszob alatt ({len(noisy)} db, csak tajekoztato) --")
    for r in noisy[: max(0, a.limit // 3)]:
        print(f"{r[0]:>8.1f}{r[1]:>8d}{r[2]:>10d}  {r[3]:18s}{r[4]}")


ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
sub.add_parser("list").set_defaults(fn=cmd_list)
s = sub.add_parser("add"); s.add_argument("family"); s.add_argument("terms", nargs="+"); s.set_defaults(fn=cmd_add)
s = sub.add_parser("todo"); s.add_argument("--family"); s.add_argument("--limit", type=int, default=40); s.set_defaults(fn=cmd_todo)
s = sub.add_parser("record"); s.add_argument("family"); s.add_argument("term")
s.add_argument("--searches", type=int, required=True); s.add_argument("--results", type=int, required=True)
s.add_argument("--trend", default=None); s.add_argument("--date", default="2026-08-09"); s.set_defaults(fn=cmd_record)
s = sub.add_parser("rank"); s.add_argument("--min-searches", type=int, default=300)
s.add_argument("--limit", type=int, default=30); s.set_defaults(fn=cmd_rank)
a = ap.parse_args(); a.fn(a)
