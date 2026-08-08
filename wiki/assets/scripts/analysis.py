#!/usr/bin/env python3
"""2024 vs 2026 comparison across the tracked Etsy shops."""

# shop: (niche, 2024 HUF/month, 2024 listings, 2024 sales,
#        2026 HUF/month, 2026 listings, 2026 sales)   None = unknown / dead
D = None
S = {
    # --- svg / lasercut ---------------------------------------------------
    "VeiArts":          ("svg",  43000,  103,  1129,  D, D, D),
    "Vectoitaly":       ("svg",  58000, 1137,  5264, 102088, 2573, 15504),
    "SeynDigital":      ("svg",  80000,  267,  1987, 148647,  218,  2431),
    "NormalGreetings":  ("svg", 134000,  334,  9993,  D, D, D),
    "Publishade":       ("svg", 158000,  278,  6501, 113245,  334,  8222),
    "KenTenGift":       ("svg", 180000,  349,  6062, 402369,  456, 15570),
    "lynraske":         ("svg", 265000, 1676, 17448,  D, D, D),
    "DJPenscript":      ("svg", 286000,  270, 25227, 238195,  170, 26810),
    "LovelyLifeDesigns":("svg", 293000, 1480, 14895, 322655, 1442, 18724),
    "SmilingWild":      ("svg", 711000, 2669, 72900, 725921,  331, 79697),
    "Rishasart":        ("svg",7700000,  447,116586,  D, D, D),
    "TheSubRosaDesign": ("svg", 820000,  292, 27921, 775953,  349, 34372),
    "AsszaBeadingArts": ("svg", 866000,  448, 41705, 739891,  503, 48965),
    # --- vtuber / pngtuber ------------------------------------------------
    "TuberDesigns":     ("vtb",4960000,  140, 12238,3095110,  141, 23791),
    "MarinkiArt":       ("vtb",1100000,  100, 11036,1782171,   74, 16722),
    "azuyani":          ("vtb",1230000,   15,  4661, 665870,   13,  4967),
    "Qagazzz":          ("vtb", 862000,   41,  3443, 715222,   53,  7521),
    "MtInfinityInc":    ("vtb",1260000,  203,  3024,1542368,  564,  7089),
    "CuteCakeTuber":    ("vtb",2036000,   65,  2514, 966919,   78,  4961),
    "GuangCaiArts":     ("vtb",1600000,   44,  2053,1022876,  114,  6178),
    "IkoRenStudio":     ("vtb", 603000,   17,  2053,  D, D, D),
    "miikutea":         ("vtb",2276000,    6,  1811,1607273,    8,  3441),
    "YuxMakerStudio":   ("vtb",      D,    2,  1253, 555106,    2,  1960),
    "TinyMangaGifts":   ("vtb",      D,   14,   784,1472325,   13,  1496),
    "LogicCreationDes": ("vtb",      D,    7,   711,  D, D, D),
    "Hayukituber":      ("vtb",      D,    5,   605, 519294,    8,  1445),
    "CraftsClio":       ("vtb",      D,   15,   433,  D, D, D),
    "CybDigital":       ("vtb",      D,   41,   336,1392043,   78,  1769),
    "2dlivemodelStudio":("vtb",      D,   27,   218,1265320,  144,  3751),
    "DoodliStudio":     ("vtb",      D,   22,   113,  59794,   41,   581),
    "SenhaiVtuber":     ("vtb",      D,    6,    13,  D, D, D),
    "pngVtubers":       ("vtb", 902000,  106, 10463,1572300,   93, 31173),
    "NeoStreamlabs":    ("vtb",      D,  440,  5680,2294428,  924, 36313),
    "LilWoogies":       ("vtb",      D,  389,  5555, 903479,  394,  9046),
    "VTubeWorld":       ("vtb",      D,   21,   505,  D, D, D),
    "NinisDigitalArt":  ("vtb",      D,   12,   354,  62347,   20,  1296),
    "BankuriPet":       ("vtb",      D,   99,   274, 599129,  178,  4383),
    # --- dog svg / bundle shops -------------------------------------------
    "Ribsdesign":       ("dog",  72712,   42,  1108,  D, D, D),
    "DENIDigitalArt":   ("dog", 741280,  146,  5268, 950255,  271, 29008),
    "PaperDog3D":       ("dog", 326016,  203,  1347, 367259,  255,  7140),
    "EmsiDigital":      ("dog",  78000,  219,   958,  69438,  269,  3916),
    "PixieHawkGraphics":("dog",  52690,  323,  2645,  94244,  303,  3913),
    "ColorLayerArt":    ("dog",1381773,  345,     D,2192780,  559, 32171),
    "SVGplugDz":        ("dog",1423760,  410, 37491, 810870,  483, 78270),
    "DXFpage":          ("dog", 440572,  493, 47985, 863897,  661, 59416),
    "LunamCo":          ("dog", 638380,  543,118392, 564965,  557,133615),
    "Art4youSpace":     ("dog", 764762,  558,105489,1463342,  346,113816),
    "UxcomShop":        ("dog", 636625,  591,  7410, 207093,  565, 13451),
    "wallartbox":       ("dog",1367305,  723, 22967,  D, D, D),
    "DigitalLinks":     ("dog", 323064,  869, 46949,  D, D, D),
    "WildInkDigital":   ("dog",1493010, 1099,  6358, 702253,  875, 19861),
    "TheMelodyFace":    ("dog", 612744, 1435, 69719,2706790,  861, 81808),
    "TheDigitalCraftCo":("dog", 189365, 1644, 38116,  D, D, D),
    "MagicVectorLaser": ("dog",3090000, 1720,     D,7105105,  934, 94316),
    "ARTsteady":        ("dog",2382957, 2055, 57063,1579752, 1506, 99823),
    "SignReadyVector":  ("dog", 278517, 2158, 31222, 347647, 1264, 35868),
    "CraftyArtCafe":    ("dog",1745580, 4119,187526,3911736, 3598,235390),
    # --- only found in 2026 (no 2024 numbers were collected) --------------
    "EricaDigitalDesign":("dog",     D,    D,     D,1815708,  939,176799),
    "SouthForkSVG":     ("dog",      D,    D,     D,1122655, 5952,163707),
    "squishsjewels":    ("dog",      D,    D,     D, 113562,  292,  5207),
    "SunnyDigitalArts": ("dog",      D,    D,     D,  D, D, D),
    "PrintCutCA":       ("dog",      D,    D,     D, 330186,  143,  6587),
    "VectorCraftLab":   ("dog",      D,    D,     D, 158798,  724, 12250),
    "CraftySVGKiwi":    ("dog",      D,    D,     D,1750234, 1152, 94396),
    "digitaldesignsvg": ("dog",      D,    D,     D, 203084,  239, 18686),
    "BlankPrintsArts":  ("dog",      D,    D,     D,1857806, 1220,  9942),
}

NICHE = {"svg": "svg / lasercut", "vtb": "vtuber / pngtuber", "dog": "dog svg / bundle"}


def med(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


print("=" * 72)
print("1. MORTALITY  (tracked in 2024, gone by 2026)")
for k in ("svg", "vtb", "dog"):
    tracked = [s for s, v in S.items() if v[0] == k and v[2] is not None]
    dead = [s for s in tracked if S[s][5] is None]
    print(f"  {NICHE[k]:20} {len(dead):2}/{len(tracked):2} dead "
          f"({100*len(dead)/len(tracked):.0f}%)  {', '.join(dead)}")

print()
print("2. REVENUE CHANGE among the survivors (HUF/month)")
for k in ("svg", "vtb", "dog"):
    ch = [(s, S[s][1], S[s][4]) for s, v in S.items()
          if v[0] == k and v[1] and v[4]]
    grew = [s for s, a, b in ch if b > a]
    print(f"  {NICHE[k]:20} {len(grew)}/{len(ch)} grew, "
          f"median change {med([b/a for _, a, b in ch]):.2f}x")

print()
print("3. REVENUE PER LISTING, 2026 (HUF/month per listing)")
print("   = how much one listing is worth; 500k/this = listings needed")
for k in ("svg", "vtb", "dog"):
    per = [(S[s][4] / S[s][5], s) for s, v in S.items()
           if v[0] == k and v[4] and v[5]]
    m = med([p for p, _ in per])
    print(f"  {NICHE[k]:20} median {m:8,.0f} HUF/listing "
          f"-> {500000/m:6,.0f} listings for 500k HUF/month")
    for p, s in sorted(per, reverse=True)[:4]:
        print(f"      {s:22} {p:9,.0f}  ({S[s][5]:5} listings, "
              f"{S[s][4]:9,.0f} HUF/mo)")

print()
print("4. SALES VELOCITY 2024 -> 2026 (total sales added in 24 months)")
for k in ("svg", "vtb", "dog"):
    v = [(S[s][6] - S[s][3], s) for s, x in S.items()
         if x[0] == k and x[3] and x[6]]
    print(f"  {NICHE[k]:20} median {med([a for a, _ in v]):8,.0f} sales / 2 years")

print()
print("5. THE 2026 TOP EARNERS (HUF/month)")
top = sorted(((v[4], s, v[0], v[5]) for s, v in S.items() if v[4]), reverse=True)
for r, (rev, s, k, li) in enumerate(top[:12], 1):
    print(f"  {r:2}. {s:22} {rev:10,.0f}  {li:5} listings  {NICHE[k]}")
