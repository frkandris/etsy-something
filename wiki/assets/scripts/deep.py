#!/usr/bin/env python3
"""svg/lasercut + dog-svg/bundle: what actually moved between 2024 and 2026."""

N = None
# name: (topic, founded,
#        2024: HUF/mo, listings, sales, median price in HUF,
#        2026: HUF/mo, listings, sales, median price in HUF)
# 2024 HUF prices come from column K (top block) or column I (dog block).
SHOPS = {
 # --- top block --------------------------------------------------------
 "Vectoitaly":       ("skyline -> svg misc", 2018,   58000, 1137,  5264,  630, 102088, 2573, 15504,  656),
 "SeynDigital":      ("lasercut svg",        2022,   80000,  267,  1987, 1112, 148647,  218,  2431, 3163),
 "Publishade":       ("lasercut skyline",    2020,  158000,  278,  6501,  786, 113245,  334,  8222,  936),
 "KenTenGift":       ("lasercut svg",        2017,  180000,  349,  6062, 1938, 402369,  456, 15570, 1740),
 "DJPenscript":      ("coloring/dot-to-dot", 2015,  286000,  270, 25227,    N, 238195,  170, 26810,  633),
 "LovelyLifeDesigns":("country outline",     2018,  293000, 1480, 14895,  897, 322655, 1442, 18724,  949),
 "SmilingWild":      ("dog svg, layered",    2016,  711000, 2669, 72900,  889, 725921,  331, 79697,  809),
 "TheSubRosaDesign": ("cross-stitch",        2015,  820000,  292, 27921, 3230, 775953,  349, 34372, 2847),
 "AsszaBeadingArts": ("beading tutorial",    2013,  866000,  448, 41705, 2512, 739891,  503, 48965, 2241),
 "VeiArts":          ("lasercut map",        2019,   43000,  103,  1129, 2081,      N,    N,     N,    N),
 "NormalGreetings":  ("country symbols",     2021,  134000,  334,  9993,  664,      N,    N,     N,    N),
 "lynraske":         ("svg symbols",         2020,  265000, 1676, 17448,  714,      N,    N,     N,    N),
 "Rishasart":        ("lasercut layered",    2020, 7700000,  447,116586, 1883,      N,    N,     N,    N),
 # --- dog svg / bundle block ------------------------------------------
 "Ribsdesign":       ("bundle, kezdo",       2023,   72712,   42,  1108, 1192,      N,    N,     N,    N),
 "DENIDigitalArt":   ("sok bundle",          2023,  741280,  146,  5268, 1130, 950255,  271, 29008, 1265),
 "PaperDog3D":       ("layered, papir",      2024,  326016,  203,  1347, 1152, 367259,  255,  7140, 1582),
 "EmsiDigital":      ("transparent png",     2023,   78000,  219,   958, 1000,  69438,  269,  3916,  703),
 "PixieHawkGraphics":("grayscale",           2023,   52690,  323,  2645,  479,  94244,  303,  3913,  836),
 "ColorLayerArt":    ("layered",             2023, 1381773,  345,     N, 1481,2192780,  559, 32171, 2214),
 "SVGplugDz":        ("bundle, nem csak dog",2022, 1423760,  410, 37491,  592, 810870,  483, 78270,  583),
 "DXFpage":          ("dxf",                 2019,  440572,  493, 47985, 1178, 863897,  661, 59416,  949),
 "LunamCo":          ("bundle, nem csak dog",2020,  638380,  543,118392,  541, 564965,  557,133615,  307),
 "Art4youSpace":     ("bundle",              2019,  764762,  558,105489, 1411,1463342,  346,113816,  949),
 "UxcomShop":        ("bundle",              2022,  636625,  591,  7410, 1375, 207093,  565, 13451,  802),
 "WildInkDigital":   ("dog bundle",          2023, 1493010, 1099,  6358, 1878, 702253,  875, 19861, 1262),
 "TheMelodyFace":    ("bundle, nem csak dog",2020,  612744, 1435, 69719,  633,2706790,  861, 81808, 1455),
 "MagicVectorLaser": ("layered",             2021, 3090000, 1720,     N, 2000,7105105,  934, 94316, 2372),
 "ARTsteady":        ("layered, nem csak dog",2020,2382957, 2055, 57063, 1341,1579752, 1506, 99823,  759),
 "SignReadyVector":  ("sign vector",         2017,  278517, 2158, 31222, 1059, 347647, 1264, 35868,  696),
 "CraftyArtCafe":    ("olcso bundle",        2022, 1745580, 4119,187526,  470,3911736, 3598,235390,  633),
 "wallartbox":       ("sok bundle",          2021, 1367305,  723, 22967, 1811,      N,    N,     N,    N),
 "DigitalLinks":     ("nem csak dog",        2021,  323064,  869, 46949,  504,      N,    N,     N,    N),
 "TheDigitalCraftCo":("ai?",                 2022,  189365, 1644, 38116,  605,      N,    N,     N,    N),
 # --- only measured in 2026 -------------------------------------------
 "EricaDigitalDesign":("bundle",             2018,       N,    N,     N,    N,1815708,  939,176799,  547),
 "SouthForkSVG":     ("olcso bundle",        2021,       N,    N,     N,    N,1122655, 5952,163707,  310),
 "squishsjewels":    ("?",                   2023,       N,    N,     N,    N, 113562,  292,  5207,  788),
 "PrintCutCA":       ("print & cut",         2023,       N,    N,     N,    N, 330186,  143,  6587, 1582),
 "VectorCraftLab":   ("vector",              2019,       N,    N,     N,    N, 158798,  724, 12250, 1044),
 "CraftySVGKiwi":    ("svg",                 2022,       N,    N,     N,    N,1750234, 1152, 94396,  946),
 "digitaldesignsvg": ("svg/png",             2021,       N,    N,     N,    N, 203084,  239, 18686,  633),
 "BlankPrintsArts":  ("?",                   2024,       N,    N,     N,    N,1857806, 1220,  9942, 5694),
 "SunnyDigitalArts": ("?",                   2022,       N,    N,     N,    N,      N,    N,     N,    N),
}

alive = {k: v for k, v in SHOPS.items() if v[6]}
both = {k: v for k, v in alive.items() if v[2]}


def row(k):
    t, f, r24, l24, s24, p24, r26, l26, s26, p26 = SHOPS[k]
    return t, f, r24, l24, s24, p24, r26, l26, s26, p26


print("=" * 78)
print("A) NYERTESEK ES VESZTESEK  (HUF/ho valtozas, 2024 -> 2026)")
ch = sorted(((v[6] / v[2], k) for k, v in both.items()), reverse=True)
print(f"{'bolt':22}{'valtozas':>9}{'listing':>14}{'ar HUF':>13}   {'sales/2ev':>9}  topic")
for f, k in ch:
    t, _, r24, l24, s24, p24, r26, l26, s26, p26 = row(k)
    dl = f"{l24}->{l26}"
    dp = f"{p24}->{p26}" if p24 else "?"
    ds = f"{s26-s24:+,}" if s24 else "?"
    print(f"{k:22}{f:8.2f}x{dl:>14}{dp:>13}   {ds:>9}  {t}")

print()
print("=" * 78)
print("B) MIT CSINALTAK A NYERTESEK?  (>1.3x novekedes)")
for f, k in ch:
    if f < 1.3:
        continue
    t, _, r24, l24, s24, p24, r26, l26, s26, p26 = row(k)
    print(f"  {k:20} {f:.2f}x | listing {(l26/l24-1)*100:+6.0f}% | "
          f"ar {(p26/p24-1)*100:+6.0f}% | "
          f"bevetel/listing {r24/l24:>6,.0f} -> {r26/l26:>6,.0f} HUF")
print()
print("   VESZTESEK (<0.8x)")
for f, k in ch:
    if f >= 0.8:
        continue
    t, _, r24, l24, s24, p24, r26, l26, s26, p26 = row(k)
    print(f"  {k:20} {f:.2f}x | listing {(l26/l24-1)*100:+6.0f}% | "
          f"ar {(p26/p24-1)*100:+6.0f}% | "
          f"bevetel/listing {r24/l24:>6,.0f} -> {r26/l26:>6,.0f} HUF")

print()
print("=" * 78)
print("C) ARSAV vs TELJESITMENY (2026)")
bands = [(0, 700, "olcso   (<700 HUF)"), (700, 1300, "kozep   (700-1300)"),
         (1300, 2500, "premium (1300-2500)"), (2500, 9e9, "magas   (2500+)")]
for lo, hi, lab in bands:
    g = [k for k, v in alive.items() if v[9] and lo <= v[9] < hi]
    if not g:
        continue
    rev = sorted(alive[k][6] for k in g)
    rpl = sorted(alive[k][6] / alive[k][7] for k in g)
    gr = [alive[k][6] / alive[k][2] for k in g if alive[k][2]]
    med = lambda x: x[len(x)//2] if len(x) % 2 else (x[len(x)//2-1]+x[len(x)//2])/2
    print(f"  {lab:20} n={len(g):2}  median bevetel {med(rev):9,.0f} HUF/ho  "
          f"bevetel/listing {med(rpl):6,.0f}  "
          f"novekedes {med(sorted(gr)):.2f}x" if gr else "")

print()
print("=" * 78)
print("D) UJ BELEPOK: 2021 utan nyitott boltok 2026-os allasa")
newish = sorted(((v[1], v[6], k) for k, v in alive.items() if v[1] >= 2021),
                reverse=True)
for f, r26, k in newish:
    t, _, r24, l24, s24, p24, _, l26, s26, p26 = row(k)
    age = 2026.6 - f
    print(f"  {f}  {k:20} {r26:9,.0f} HUF/ho  {l26:5} listing  "
          f"{r26/l26:6,.0f} HUF/listing  ~{age:.0f} ev  {t}")

print()
print("=" * 78)
print("E) HANY LISTING KELL? (2026, bevetel/listing szerint sorbarendezve)")
eff = sorted(((v[6] / v[7], k) for k, v in alive.items()), reverse=True)
for e, k in eff:
    t, f, *_ , l26, s26, p26 = row(k)
    print(f"  {k:22}{e:8,.0f} HUF/listing -> {500000/e:6,.0f} listing 500k-hoz"
          f"   ({SHOPS[k][7]:5} listing, ar {p26 or 0:,} HUF)  {t}")
