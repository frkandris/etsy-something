import json, re, collections

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
def bucket(t):
    l, p = bool(LASER.search(t or '')), bool(PAPER.search(t or ''))
    return 'mindketto' if l and p else 'lezer' if l else 'papir' if p else 'egyik sem'

shops = collections.Counter(shop(r) for r in revs)
print(f"Populacio: {len(revs)} dedupolt review / {len({r['listing_title'] for r in revs})} listing / {len(shops)} ELADO")
print("Top eladok:", ", ".join(f"{s}({n})" for s, n in shops.most_common(6)))

# eladonkent: melyik oldalon all?
side_by_shop = collections.defaultdict(collections.Counter)
for r in revs:
    side_by_shop[shop(r)][bucket(r.get('listing_title'))] += 1
lean = collections.Counter()
for s, c in side_by_shop.items():
    lz, pp = c['lezer'] + c['mindketto'] * 0.5, c['papir'] + c['mindketto'] * 0.5
    lean['lezer' if lz > pp * 1.5 else 'papir' if pp > lz * 1.5 else 'vegyes'] += 1
print(f"\nA) ELADOK oldala (populacio: {len(side_by_shop)} elado)")
for k, v in lean.most_common():
    print(f"   {k:10s} {v:3d} elado  {v/len(side_by_shop)*100:5.1f}%")

# fajdalompontok oldalankent, ELADO-szammal
PAIN = {
    'osszeszereles/utmutato': r'\b(hard to|difficult|tricky|confus|struggl|figure out|instruction)',
    'meretezes':              r'\b(resize|re-?size|scal|too big|too large|too small for)',
    'torekeny/vekony':        r'\b(fragile|too thin|very thin|broke|breaking|snapp|delicate|flims)',
    'nem illeszkedik':        r'\b(align|line up|didn.?t fit|doesn.?t fit|gap between|overlap)',
    'hianyzo fajl/reteg':     r'\b(missing|not included|doesn.?t contain|not all layer|didn.?t open|corrupt)',
    'tul sok/felesleges reteg': r'\b(too many layer|removed (a|one|the) layer|left out a layer)',
}
print(f"\nB) Fajdalompontok oldalankent (elado-szam zarojelben)")
print(f"   {'fajdalom':26s} {'lezer-oldal':>16s} {'papir-oldal':>16s}")
for name, pat in PAIN.items():
    rx = re.compile(pat, re.I)
    L = [r for r in revs if rx.search(r.get('review') or '') and bucket(r['listing_title']) in ('lezer', 'mindketto')]
    P = [r for r in revs if rx.search(r.get('review') or '') and bucket(r['listing_title']) in ('papir', 'mindketto')]
    print(f"   {name:26s} {len(L):6d} rev ({len({shop(x) for x in L}):2d}) {len(P):6d} rev ({len({shop(x) for x in P}):2d})")

nL = sum(1 for r in revs if bucket(r['listing_title']) in ('lezer', 'mindketto'))
nP = sum(1 for r in revs if bucket(r['listing_title']) in ('papir', 'mindketto'))
print(f"   [alap: lezer-oldal {nL} review, papir-oldal {nP} review]")

# minden 1-3 csillagos teljes szoveg
print("\nC) MINDEN 1-3 csillagos review (a valodi kudarcok)")
for r in [x for x in revs if (x.get('product_rating') or 5) <= 3]:
    import html
    print(f"   [{r['product_rating']}★ {bucket(r['listing_title']):9s}] {html.unescape(r.get('review') or '')[:220]}")
