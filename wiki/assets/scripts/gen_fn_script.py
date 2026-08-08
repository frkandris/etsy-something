#!/usr/bin/env python3
"""Apps Script for the functional (non-layered) laser-cut segment sheet."""
import json, statistics as st, datetime as dt

USD = 316.33
NOW = dt.datetime(2026, 8, 7)
med = lambda a: st.median(a) if a else 0

details = json.load(open("fn_shopdetails.json"))
search = json.load(open("fn_shops.json"))
cat = json.load(open("fn_catalog.json"))

# what the shop actually sells, from a 24-listing sample of its own catalogue
FUNC = ("box", "urn", "frame", "organizer", "holder", "shelf", "tray",
        "lamp", "stand", "vase", "planter", "coaster", "clock", "caddy",
        "container", "drawer", "basket", "bin", "case")
LAY = ("multilayer", "multi-layer", "multi layer", "layered", " layer",
       "layers", "3d mandala", "shadow box")
titles = {}
for r in cat:
    titles.setdefault(r["shop_name"], []).append(r["title"].lower())

hit_titles = {}
for f in ["laser_cut_box_svg_file", "wooden_gift_box_laser_cut_file",
          "laser_cut_picture_frame_svg", "laser_cut_urn_svg_file",
          "commercial_licence_laser_cut_files"]:
    for r in json.load(open(f"fn/{f}.json")):
        hit_titles.setdefault(r["shopName"], set()).add(r["title"])

out = []
for s in details:
    name = s["shop_name"]
    q = search.get(name, {})
    if not q.get("p"):
        continue
    created = dt.datetime.fromtimestamp(s["create_date"], dt.UTC).replace(tzinfo=None)
    months = max(1, (NOW - created).days / 30.44)
    price = st.median(q["p"])
    lst = st.median(q["op"]) if q.get("op") else None
    disc = (1 - price / lst) if lst else 0
    sold_mo = (s.get("sold_count") or 0) / months
    rev_sale = sold_mo * price * USD
    rev_list = sold_mo * lst * USD if lst else ""
    ts = titles.get(name, [])
    func_share = (sum(any(k in t for k in FUNC) for t in ts) / len(ts)) if ts else ""
    lay_share = (sum(any(k in t for k in LAY) for t in ts) / len(ts)) if ts else ""
    listings = s.get("active_listing_count") or 0
    adj = rev_sale * func_share if ts else ""
    ex = sorted(hit_titles.get(name, [""]))[0]
    out.append([
        name, "https://www.etsy.com/shop/" + name, s.get("country_code") or "?",
        created.date().isoformat(), round((NOW - created).days / 365, 1),
        listings, s.get("sold_count") or 0, s.get("average_rating"),
        s.get("total_rating_count") or 0,
        round(price, 2), round(lst, 2) if lst else "", round(disc, 4) if disc else "",
        round(rev_list) if rev_list else "", round(rev_sale),
        round(sold_mo, 1),
        round(rev_sale / listings) if listings else "",
        q.get("distinct", 0),
        round(func_share, 2) if ts != [] else "",
        round(lay_share, 2) if ts != [] else "",
        round(adj) if adj != "" else "",
        round(adj / listings) if (adj != "" and listings) else "",
        ex[:90],
    ])

out.sort(key=lambda x: (x[19] if isinstance(x[19], (int, float)) else -1), reverse=True)

HEADERS = [
    "shop", "URL", "orszag", "nyitas", "ev", "listing", "osszes eladas",
    "rating", "review", "elad. ar USD", "listaar USD", "tartos kedvezmeny",
    "arbevetel listaaron HUF/ho", "diszkontalt arbevetel HUF/ho", "eladas/ho",
    "HUF/listing", "kulonallo talalat", "funkcionalis arany (kat. minta)",
    "layered arany (kat. minta)", "korrigalt arbevetel HUF/ho",
    "korrigalt HUF/listing", "pelda listing cim",
]

script = '''/**
 * Functional laser-cut file segment - boxes, urns, frames, holders.
 *
 * Population: the top results of five Etsy searches (laser cut box svg file /
 * wooden gift box laser cut file / laser cut picture frame svg / laser cut urn
 * svg file / commercial licence laser cut files) = 500 listings from 285 shops.
 * Only the 73 shops that ranked with at least TWO DISTINCT listings are listed
 * here; the other 212 appeared once each and are the noise class - on the
 * layered sheet that group turned out to be mostly shops from other niches
 * with one keyword-optimised item.
 *
 * Every shop was then catalogue-sampled (24 of its own listings) so the last
 * columns can say what it really sells:
 *   "funkcionalis arany" - share of its catalogue that is boxes/urns/frames
 *   "layered arany"      - share that is layered wall art (the other segment)
 *   "korrigalt arbevetel" = discounted revenue x functional share
 *
 * Revenue is a LIFETIME AVERAGE: total sales / months open x current price.
 * Close to the run rate for a young shop, diluted by the slow early years for
 * an old one - do not compare across ages without that in mind.
 */

var SHEET_ID = 594784454;
var OVERWRITE = false; // set to true to overwrite a sheet that already has data

var HEADERS = __HEADERS__;
var DATA = __DATA__;

function fillFunctionalSheet() {
  var ss = SpreadsheetApp.getActive() || SpreadsheetApp.openById(
    '1j-52jMBxTxgZ3-ywNekNGKjraP6u2QYDKxLVdMfsqUQ');
  var sh = null, all = ss.getSheets();
  for (var i = 0; i < all.length; i++) {
    if (all[i].getSheetId() === SHEET_ID) { sh = all[i]; break; }
  }
  if (!sh) throw new Error('No sheet with id ' + SHEET_ID);

  if (!OVERWRITE && sh.getLastRow() > 0) {
    throw new Error('"' + sh.getName() + '" is not empty (' + sh.getLastRow() +
      ' rows). Clear it, or set OVERWRITE = true at the top of the script.');
  }

  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS])
    .setFontWeight('bold').setWrap(true);
  sh.getRange(2, 1, DATA.length, HEADERS.length).setValues(DATA);

  sh.getRange(2, 10, DATA.length, 2).setNumberFormat('0.00');   // prices
  sh.getRange(2, 12, DATA.length, 1).setNumberFormat('0%');     // discount
  sh.getRange(2, 13, DATA.length, 2).setNumberFormat('#,##0');  // revenues
  sh.getRange(2, 16, DATA.length, 1).setNumberFormat('#,##0');  // HUF/listing
  sh.getRange(2, 18, DATA.length, 2).setNumberFormat('0%');     // shares
  sh.getRange(2, 20, DATA.length, 2).setNumberFormat('#,##0');  // corrected
  sh.setFrozenRows(1);
  sh.autoResizeColumns(1, HEADERS.length);

  Logger.log(DATA.length + ' shops written');
}
'''
script = (script
          .replace('__HEADERS__', json.dumps(HEADERS, ensure_ascii=False))
          .replace('__DATA__', json.dumps(out, ensure_ascii=False, indent=0)))
open("fill-functional-sheet.gs", "w").write(script)

print("rows:", len(out))
print()
fs = [r for r in out if isinstance(r[17], float)]
print(f"median funkcionalis arany: {med([r[17] for r in fs])*100:.0f}%")
print(f"median layered arany:      {med([r[18] for r in fs])*100:.0f}%")
adj = [r[19] for r in out if isinstance(r[19], (int, float))]
raw = [r[13] for r in out if isinstance(r[13], (int, float))]
print(f"median bevetel: nyers {med(raw):,.0f} -> KORRIGALT {med(adj):,.0f} HUF/ho")
print()
for lo, hi, lab in [(0.8, 1.01, "80-100% funkcionalis"), (0.5, 0.8, "50-80%"),
                    (0.2, 0.5, "20-50%"), (0, 0.2, "<20%")]:
    g = [r for r in fs if lo <= r[17] < hi]
    print(f"   {lab:22} {len(g):3} bolt   median korrigalt "
          f"{med([r[19] for r in g if isinstance(r[19],(int,float))]):>10,.0f}")
print()
print("TOP 10 KORRIGALT")
print(f"   {'bolt':24}{'func%':>7}{'korrigalt':>11}{'listing':>8}{'HUF/list':>10}{'ar$':>7}{'akcio':>7}  orsz")
for r in out[:10]:
    print(f"   {r[0]:24}{r[17]*100 if isinstance(r[17],float) else 0:>6.0f}%{r[19]:>11,.0f}"
          f"{r[5]:>8}{r[20]:>10,.0f}{r[9]:>7.2f}{(r[11] or 0)*100:>6.0f}%  {r[2]}")
