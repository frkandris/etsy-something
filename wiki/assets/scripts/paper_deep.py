import json, re, collections, html

rows = []
for f in ('wiki/assets/data/reviews.json', 'wiki/assets/data/nc_reviews.json'):
    rows += json.load(open(f))
seen, revs = set(), []
for r in rows:
    k = r.get('receipt_id')
    if k in seen: continue
    seen.add(k); revs.append(r)
shop = lambda r: (r.get('product_details') or {}).get('seller_name') or '?'
clean = lambda s: html.unescape(s or '').replace('\n', ' ').strip()

LASER = re.compile(r'\b(laser|glowforge|lightburn|xtool|cnc|plywood|mdf|wood|wooden|engrav)', re.I)
PAPER = re.compile(r'\b(cricut|silhouette|cardstock|card ?stock|paper ?cut|papercut|paper|cameo)', re.I)
def side(t):
    l, p = bool(LASER.search(t or '')), bool(PAPER.search(t or ''))
    return 'mindketto' if l and p else 'lezer' if l else 'papir' if p else 'egyik sem'

# --- ki all a papiros oldalon
by_shop = collections.defaultdict(collections.Counter)
for r in revs:
    by_shop[shop(r)][side(r.get('listing_title'))] += 1
paper_shops = []
for s, c in by_shop.items():
    lz, pp = c['lezer'] + c['mindketto'] * .5, c['papir'] + c['mindketto'] * .5
    if pp > lz * 1.5:
        paper_shops.append((s, sum(c.values()), c))
paper_shops.sort(key=lambda x: -x[1])
print("A) PAPIROS ELADOK (a korpuszban)")
for s, n, c in paper_shops:
    ex = next((r for r in revs if shop(r) == s), None)
    rating = (ex.get('product_details') or {}).get('shop_average_rating')
    cnt = (ex.get('product_details') or {}).get('shop_total_rating_count')
    print(f"   {s:26s} {n:3d} review a mintaban | bolt {rating}★ / {cnt} ertekeles")

PSET = {s for s, _, _ in paper_shops}
prev = [r for r in revs if shop(r) in PSET]
print(f"\n   -> {len(prev)} review {len(PSET)} papiros eladotol")

# --- mit arulnak: termekforma a cimekben
FORMS = {
    'shadow box':      r'shadow ?box',
    'lightbox/lámpa':  r'\b(light ?box|lantern|luminar|lamp)',
    'kártya/pop-up':   r'\b(card|pop ?up|greeting)',
    'mandala':         r'mandala',
    'fali dekor':      r'\b(wall art|wall decor)',
    'doboz/explosion': r'\b(explosion box|gift box|favor box)',
    'virág':           r'\b(flower|floral|rose|bouquet)',
}
titles = {r['listing_title'] for r in prev}
print(f"\nB) A papiros eladok TERMEKFORMAI (populacio: {len(titles)} kulonallo listing)")
for n, pat in FORMS.items():
    rx = re.compile(pat, re.I)
    hit = [t for t in titles if rx.search(t)]
    sh = {shop(r) for r in prev if rx.search(r['listing_title'])}
    print(f"   {n:18s} {len(hit):4d} listing ({len(hit)/len(titles)*100:4.1f}%)  {len(sh)} elado")

# --- retegszam a papiros cimekben
lay = collections.Counter()
for t in titles:
    m = re.search(r'(\d{1,2})\s*(?:-|\s)?layer', t, re.I)
    if m: lay[int(m.group(1))] += 1
print(f"\nC) Kiirt retegszam a papiros cimekben ({sum(lay.values())} listing irja ki)")
print("   ", ", ".join(f"{k}:{v}" for k, v in sorted(lay.items())))
if lay:
    allv = sorted(x for k, v in lay.items() for x in [k]*v)
    print(f"   median: {allv[len(allv)//2]} reteg")

# --- papir-specifikus fajdalom, TELJES szoveggel
PAIN = {
    'keret/méret nem passzol': r'\b(frame|8x8|10x10|12x12|shadow ?box size|fit(s)? (in|the) frame|mat size)',
    'ragasztás':               r'\b(glue|glueing|gluing|adhesive|foam|tape|sticky)',
    'vágás nem sikerült':      r'\b(didn.?t cut|cut through|blade|mat|tore|ripped|jagged)',
    'túl apró elem':           r'\b(tiny|too small|intricate|weeding|weed)',
    'útmutató':                r'\b(instruction|assembly|which order|order of layer|numbered)',
    'színválasztás':           r'\b(colou?r|shade|palette)',
}
print(f"\nD) PAPIR-SPECIFIKUS fajdalom ({len(prev)} papiros-eladoi review)")
for n, pat in PAIN.items():
    rx = re.compile(pat, re.I)
    h = [r for r in prev if rx.search(r.get('review') or '')]
    sh = {shop(r) for r in h}
    print(f"   {n:26s} {len(h):3d} rev, {len(sh)} elado")
    for r in h[:3]:
        print(f"        · {clean(r['review'])[:120]}")
