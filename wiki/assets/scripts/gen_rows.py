#!/usr/bin/env python3
"""Generate the 2026-08-06 rows for the 'revenue estimation' sheet.

Column layout (as used in the existing 2026 rows):
  A date | B url | C topic | D HUF/month | E listings | F sales | G favorites
  H avg sales/month | I median price (text) | J est revenue/month (text)
  K median price in HUF | L =D/E | M =500000/L | N founded | O =days(A,N)/365
  P =E-Eprev | Q =F-Fprev | R =(F-Fprev)*Kprev/24
"""
import json, datetime, re

# HUF rates: USD/EUR kept identical to the ones already used in the sheet's
# 2026 rows; the rest derived from live cross rates (frankfurter, 2026-08-06)
# anchored to USD = 316.33.
RATE = {
    "USD": 316.33, "EUR": 364.6, "GBP": 426.0, "CAD": 226.0, "AUD": 222.8,
    "SGD": 246.7, "SEK": 33.42, "HKD": 40.32, "MYR": 77.35,
}

MONTHS = {m: i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def iso(created):
    """'Mon Aug 24 2020' -> '2020-08-24'"""
    if not created:
        return ""
    _, mon, day, year = created.split()
    return f"{year}-{MONTHS[mon]:02d}-{int(day):02d}"


def num(s):
    return float(s.replace(",", "")) if s else None


def split_money(s):
    """'2,261 USD' -> (2261.0, 'USD')"""
    m = re.match(r"^([\d.,]+)\s+([A-Z]{3})$", s.strip())
    if not m:
        return None, None
    return float(m.group(1).replace(",", "")), m.group(2)


# shop data straight from salesdoe (2026-08-06)
# 2024-row -> [shop, created, listings, sales, fav, avg, median, revenue, dead]
DATA = json.load(open("salesdoe-2026.json"))
BY_SHOP = {d[0].split(" ")[0]: d for d in DATA}

# 2024 row number in the sheet -> shop key
ROWS = [
    (38, "MtInfinityInc"), (39, "CuteCakeTuber"), (40, "GuangCaiArts"),
    (41, "IkoRenStudio"), (42, "miikutea"), (43, "YuxMakerStudio"),
    (44, "TinyMangaGifts"), (45, "LogicCreationDesign"), (46, "Hayukituber"),
    (47, "CraftsClio"), (48, "CybDigital"), (49, "2dlivemodelStudio"),
    (50, "DoodliStudio"), (51, "SenhaiVtuber"), (53, "pngVtubers"),
    (54, "NeoStreamlabs"), (55, "LilWoogies"), (56, "VTubeWorld"),
    (57, "NinisDigitalArt"), (58, "BankuriPet"), (60, "Ribsdesign"),
    (61, "DENIDigitalArtSudio"), (62, "PaperDog3D"), (63, "EmsiDigital"),
    (64, "PixieHawkGraphics"), (65, "ColorLayerArt"), (66, "SVGplugDz"),
    (67, "DXFpage"), (68, "LunamCo"), (69, "Art4youSpace"), (70, "UxcomShop"),
    # row 72 (SmilingWild) is skipped: the same shop already has a 2026 row
    # at row 21, and row 72's 2024 numbers are a bundle-only subset
    (71, "wallartbox"), (73, "DigitalLinks"),
    (74, "WildInkDigital"), (75, "TheMelodyFace"), (76, "TheDigitalCraftCo"),
    (77, "MagicVectorLaser"), (78, "ARTsteady"), (79, "SignReadyVectorArt"),
    (80, "CraftyArtCafe"), (82, "EricaDigitalDesign"), (83, "SouthForkSVG"),
    (84, "squishsjewels"), (85, "SunnyDigitalArts"), (86, "PrintCutCA"),
    (87, "VectorCraftLab"), (88, "CraftySVGKiwi"), (89, "digitaldesignsvgpng"),
    (90, "BlankPrintsArts"),
]

# SmilingWild's 2026 numbers already live in row 21 of the sheet
SMILINGWILD_21 = ["SmilingWild", "Sun Nov 27 2016", "331", "79697", "2828",
                  "685", "2.22 EUR", "1991 EUR", False]

out = []
for row24, shop in ROWS:
    d = SMILINGWILD_21 if shop == "SmilingWild" else BY_SHOP[shop]
    _, created, listings, sales, fav, avg, med, rev, dead = d
    dead = bool(dead)
    rec = {"row2024": row24, "shop": shop, "dead": dead,
           "created": iso(created)}
    if not dead:
        rev_v, cur = split_money(rev)
        med_v, _ = split_money(med)
        rate = RATE[cur]
        rec.update({
            "listings": int(num(listings)), "sales": int(num(sales)),
            "fav": int(num(fav)), "avg": int(num(avg)),
            "median": f"{med_v:g} {cur}", "revenue": f"{rev_v:g} {cur}",
            "huf_month": round(rev_v * rate), "huf_median": round(med_v * rate),
        })
    out.append(rec)

json.dump(out, open("rows-2026.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(out)} rows; dead: {sum(1 for r in out if r['dead'])}")
for r in out[:3]:
    print(r)
