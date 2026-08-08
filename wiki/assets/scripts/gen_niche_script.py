#!/usr/bin/env python3
"""Apps Script that fills the new 'layered niche' sheet."""
import json

USD = 316.33
rows = json.load(open("niche_rows.json"))

# what each shop's matching listings were actually called - used to flag
# shops that are really 3D-printing / CNC sellers with one on-topic listing
import glob
titles = {}
skip = {"build1.json","rows-2026.json","salesdoe-2026.json","niche_shops.json",
        "niche_rows.json","shoptest.json","t2.json","old_shop_listings.json",
        "shopreq.json","shopreq2.json","oldreq.json","niche_shopdetails.json",
        "niche_shopdetails2.json"}
for f in glob.glob("*.json"):
    if f in skip: continue
    try: d = json.load(open(f))
    except Exception: continue
    if isinstance(d, list) and d and isinstance(d[0], dict) and "shopName" in d[0]:
        for r in d:
            titles.setdefault(r["shopName"], []).append(r["title"].lower())
STL = ("stl", "3d print", "3mf", "filament", "bambu", "resin", "gcode")

# catalogue sample: what share of each specialist shop's own listings is layered
share = {r["shop"]: r["share"] for r in json.load(open("layered_adjusted.json"))}

out = []
for r in rows:
    price, lst, disc = r["price"], r["list_price"], r["disc"]
    sold_mo = r["sold_per_mo"]
    rev_sale = sold_mo * price * USD if price else ""
    rev_list = sold_mo * lst * USD if lst else ""
    out.append([
        r["shop"],
        "https://www.etsy.com/shop/" + r["shop"],
        r["country"],
        r["created"],
        round(r["age_y"], 1),
        r["listings"],
        r["sold"],
        r["rating"],
        r["reviews"],
        round(price, 2) if price else "",
        round(lst, 2) if lst else "",
        round(disc, 4) if disc else "",              # discount as a fraction
        round(rev_list) if rev_list else "",         # revenue at the anchor price
        round(rev_sale) if rev_sale else "",         # revenue actually collected
        round(sold_mo, 1),
        round(rev_sale / r["listings"]) if rev_sale and r["listings"] else "",
        r["hits"],
        "eros" if r["hits"] >= 5 else ("kozepes" if r["hits"] >= 3 else "gyenge"),
        "; ".join(filter(None, [
            "STL/3D-nyomtatas is" if any(k in t for t in titles.get(r["shop"], [])
                                         for k in STL) else "",
            "fizikai termek?" if price and price > 30 else "",
        ])),
        round(share[r["shop"]], 2) if r["shop"] in share else "",
        round(rev_sale * share[r["shop"]]) if (rev_sale and r["shop"] in share) else "",
        titles.get(r["shop"], [""])[0][:90],
    ])

# specialists first (>=3 hits), then by revenue
out.sort(key=lambda x: (x[16] >= 3, x[13] if isinstance(x[13], (int, float)) else -1),
         reverse=True)

HEADERS = [
    "shop", "URL", "orszag", "nyitas", "ev", "listing", "osszes eladas",
    "rating", "review", "elad. ar USD", "listaar USD", "tartos kedvezmeny",
    "arbevetel listaaron HUF/ho", "diszkontalt arbevetel HUF/ho",
    "eladas/ho", "HUF/listing", "talalat 5 keresesbol", "megbizhatosag",
    "jelzes", "layered arany (katalogus minta)", "korrigalt arbevetel HUF/ho",
    "pelda listing cim",
]

script = '''/**
 * Fills the layered / multilayer laser-cut SVG niche sheet.
 *
 * CAVEAT: a shop lands here because at least one of its listings ranked for
 * these searches, and the revenue below is the WHOLE shop's, not just its
 * layered-SVG part. Half the population matched on a single listing - those
 * are often 3D-printing or CNC shops with one keyword-optimised item. Use the
 * "megbizhatosag" column: only "eros" / "kozepes" rows are safe to reason from.
 *
 * Population: 173 shops, collected from the top results of five Etsy searches
 * (multilayer svg laser cut / multilayer svg / 3d layered mandala svg /
 * layered svg laser cut file / 3d multilayer svg dxf), 500 listings in total,
 * enriched with Etsy shop data on 2026-08-07.
 *
 * "arbevetel listaaron"   = sales/month x list price   (what an estimator that
 *                           ignores permanent discounts would report)
 * "diszkontalt arbevetel" = sales/month x actual sale price
 * "korrigalt arbevetel"   = the above x the share of the shop's own catalogue
 *                           that is actually layered (24-listing sample; only
 *                           filled for the 65 shops that ranked >=3 times)
 * Both are lifetime averages: total sales / months open. For a young shop that
 * is close to its current run rate; for an old one it is diluted by its slow
 * early years, so do not compare across ages without that in mind.
 */

var SHEET_ID = 1600752523;
var OVERWRITE = false; // set to true to overwrite a sheet that already has data

var HEADERS = __HEADERS__;
var DATA = __DATA__;

function fillNicheSheet() {
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

  sh.getRange(2, 12, DATA.length, 1).setNumberFormat('0%');          // discount
  sh.getRange(2, 19, DATA.length, 1).setNumberFormat('0%');          // layered share
  sh.getRange(2, 20, DATA.length, 1).setNumberFormat('#,##0');       // adjusted
  sh.getRange(2, 13, DATA.length, 2).setNumberFormat('#,##0');       // revenues
  sh.getRange(2, 16, DATA.length, 1).setNumberFormat('#,##0');       // HUF/listing
  sh.getRange(2, 10, DATA.length, 2).setNumberFormat('0.00');        // prices
  sh.setFrozenRows(1);
  sh.autoResizeColumns(1, HEADERS.length);

  Logger.log(DATA.length + ' shops written');
}
'''
script = (script
          .replace('__HEADERS__', json.dumps(HEADERS, ensure_ascii=False))
          .replace('__DATA__', json.dumps(out, ensure_ascii=False, indent=0)))

open("fill-niche-sheet.gs", "w").write(script)
print("rows:", len(out), "chars:", len(script))
