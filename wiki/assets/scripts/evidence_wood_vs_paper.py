import json, re, collections, math

rows = []
for f in ('wiki/assets/data/reviews.json', 'wiki/assets/data/nc_reviews.json'):
    rows += json.load(open(f))
seen, revs = set(), []
for r in rows:
    k = r.get('receipt_id')
    if k in seen: continue
    seen.add(k); revs.append(r)
shop = lambda r: (r.get('product_details') or {}).get('seller_name') or '?'

LASER = re.compile(r'\b(laser|glowforge|lightburn|xtool|cnc|plywood|mdf|wood|wooden|engrav)', re.I)
PAPER = re.compile(r'\b(cricut|silhouette|cardstock|card ?stock|paper ?cut|papercut|paper|cameo)', re.I)
def side(t):
    l, p = bool(LASER.search(t or '')), bool(PAPER.search(t or ''))
    return 'both' if l and p else 'laser' if l else 'paper' if p else 'none'

for r in revs:
    r['_side'] = side(r.get('listing_title'))

print("=" * 74)
print("A BIZONYITEKI ALAP — fa vs papir")
print("=" * 74)
print(f"Nyers review sor            : {len(rows)}")
print(f"Dedupolt (receipt_id)       : {len(revs)}")
print(f"Kulonallo listing           : {len({r['listing_title'] for r in revs})}")
print(f"Kulonallo ELADO             : {len({shop(r) for r in revs})}")
print(f"Forras                      : Apify, 2026-08-08 (egyszeri lehuzas, nem frissult)")

c = collections.Counter(r['_side'] for r in revs)
print(f"\nReview-k oldal szerint      : " + ", ".join(f"{k}={v}" for k, v in c.most_common()))

# --- TISZTA, nem atfedo osszehasonlitas
L = [r for r in revs if r['_side'] == 'laser']
P = [r for r in revs if r['_side'] == 'paper']
print(f"\nATFEDESMENTES minta         : laser-only {len(L)} review / {len({shop(r) for r in L})} elado")
print(f"                              paper-only {len(P)} review / {len({shop(r) for r in P})} elado")
print(f"('both' {c['both']} review NEM szamit egyik oldalra sem ebben a szigoru valtozatban)")

def prop_test(name, pat):
    rx = re.compile(pat, re.I)
    a = sum(1 for r in L if rx.search(r.get('review') or ''))
    b = sum(1 for r in P if rx.search(r.get('review') or ''))
    n1, n2 = len(L), len(P)
    p1, p2 = a / n1, b / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    lo, hi = (p1 - p2) - 1.96 * se, (p1 - p2) + 1.96 * se
    verdict = "KULONBSEG" if lo > 0 or hi < 0 else "NEM DONTHETO EL"
    print(f"  {name:24s} fa {a:3d}/{n1} ={p1*100:5.2f}%   papir {b:3d}/{n2} ={p2*100:5.2f}%"
          f"   kulonbseg 95% CI [{lo*100:+5.2f};{hi*100:+5.2f}] pp  -> {verdict}")

print("\nFAJDALOMPONTOK, atfedesmentes mintan, 95%-os konfidencia-intervallummal:")
prop_test('osszeszereles/utmutato', r'\b(hard to|difficult|tricky|confus|struggl|figure out|instruction)')
prop_test('torekeny/vekony',        r'\b(fragile|too thin|very thin|broke|breaking|snapp|delicate|flims)')
prop_test('meretezes',              r'\b(resize|re-?size|scal|too big|too large|too small for)')
prop_test('nem illeszkedik',        r'\b(align|line up|didn.?t fit|doesn.?t fit|gap between|overlap)')

low = [r for r in revs if (r.get('product_rating') or 5) <= 3]
print(f"\nCSILLAGOK: 5*={sum(1 for r in revs if r.get('product_rating')==5)}, "
      f"4*={sum(1 for r in revs if r.get('product_rating')==4)}, <=3*={len(low)} ({len(low)/len(revs)*100:.2f}%)")
print(f"  a <=3* mind ({len(low)}) lezer-oldali listingen van; ha aranyos lenne, "
      f"~{len(low)*len(P)/(len(L)+len(P)):.1f} papiros esetet varnank")
