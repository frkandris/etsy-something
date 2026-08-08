#!/usr/bin/env python3
"""Emit the Apps Script that adds the 2026-08-06 rows."""
import json

rows = json.load(open("rows-2026.json"))

# what the 2024 row above offers for the diff formulas
NO_PREV = set(range(82, 91))          # rows 82-90: url only
PRICE_K = {36, 38, 39, 40, 41, 42, 53}  # normal block: HUF median price -> K
PRICE_I = set(range(60, 81))          # dog block: the HUF price sits in I
NO_F = {65, 77}                       # ColorLayerArt / MagicVectorLaser: no sales


def entry(r, anchor):
    e = {
        "anchor": anchor,
        "slug": r["shop"],
        "dead": r["dead"],
        "prevE": anchor not in NO_PREV,
        "prevF": anchor not in NO_PREV and anchor not in NO_F,
        "prevPrice": "K" if anchor in PRICE_K else ("I" if anchor in PRICE_I else ""),
    }
    if not r["dead"]:
        e.update({
            "hufMonth": r["huf_month"], "listings": r["listings"],
            "sales": r["sales"], "fav": r["fav"], "avg": r["avg"],
            "median": r["median"], "revenue": r["revenue"],
            "hufMedian": r["huf_median"], "founded": r["created"],
        })
    return e


entries = [entry(r, r["row2024"]) for r in rows]

# Qagazzz already has a 2026 row (row 37); its anchor is row 36
qagazzz = json.load(open("salesdoe-2026.json"))[0]
assert qagazzz[0] == "Qagazzz", qagazzz[0]
q = entry({
    "shop": "Qagazzz", "dead": False, "huf_month": round(2261 * 316.33),
    "listings": 53, "sales": 7521, "fav": 1417, "avg": 105,
    "median": "4.46 USD", "revenue": "2261 USD",
    "huf_median": round(4.46 * 316.33), "created": "2020-08-24",
}, 36)

script = '''/**
 * Fills in the 2026-08-06 rows on the "revenue estimation" sheet.
 *
 * Every shop that had no 2026 row yet gets one inserted right below its
 * 2024-08-04 row. Shops that are not trading any more get a row with just
 * the date, matching how VeiArts / NormalGreetings / lynraske / Rishasart
 * were already handled.
 *
 * Run updateRevenueEstimation(). It verifies every anchor row before it
 * touches anything, so a mismatch aborts before any edit is made.
 */

var SPREADSHEET_ID = '1j-52jMBxTxgZ3-ywNekNGKjraP6u2QYDKxLVdMfsqUQ';
var SHEET_NAME = 'revenue estimation';
var TODAY = new Date(2026, 7, 6); // 2026-08-06

var ENTRIES = __DATA__;

// Qagazzz's 2026 row (row 37) already exists with its URL and topic filled in.
var QAGAZZZ = __QAGAZZZ__;

function updateRevenueEstimation() {
  var ss = SpreadsheetApp.getActive() ||
           SpreadsheetApp.openById(SPREADSHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) throw new Error('No sheet named ' + SHEET_NAME);

  // --- verify first, edit later -------------------------------------------
  var problems = [];
  ENTRIES.concat([QAGAZZZ]).forEach(function (e) {
    var date = sh.getRange(e.anchor, 1).getDisplayValue();
    var url = String(sh.getRange(e.anchor, 2).getValue());
    if (date !== '2024-08-04') {
      problems.push('row ' + e.anchor + ': date is "' + date + '"');
    }
    if (url.toLowerCase().indexOf('/shop/' + e.slug.toLowerCase()) === -1) {
      problems.push('row ' + e.anchor + ': expected ' + e.slug + ', got ' + url);
    }
  });
  if (String(sh.getRange(37, 1).getDisplayValue()) !== '2026-08-06') {
    problems.push('row 37: expected the empty 2026-08-06 Qagazzz row');
  }
  if (problems.length) {
    throw new Error('Aborted, the sheet does not look as expected:\\n' +
                    problems.join('\\n'));
  }

  writeRow(sh, 37, QAGAZZZ, false);

  // Insert bottom-up so the anchor row numbers stay valid.
  for (var i = ENTRIES.length - 1; i >= 0; i--) {
    var e = ENTRIES[i];
    sh.insertRowAfter(e.anchor);
    writeRow(sh, e.anchor + 1, e, true);
  }

  Logger.log(ENTRIES.length + ' rows added, Qagazzz filled in');
}

/**
 * @param {Sheet} sh
 * @param {number} r         the row being written
 * @param {Object} e         the shop's 2026 data
 * @param {boolean} withUrl  false for Qagazzz, whose B and C are already set
 */
function writeRow(sh, r, e, withUrl) {
  var p = r - 1; // the 2024 row this one is compared against
  sh.getRange(r, 1).setValue(TODAY);
  if (e.dead) return; // not trading: the date alone, as before

  if (withUrl) {
    sh.getRange(r, 2).setValue('https://www.etsy.com/shop/' + e.slug);
    sh.getRange(r, 3).setValue(sh.getRange(p, 3).getValue()); // same topic
  }

  var row = [
    e.hufMonth,                                   // D HUF / month
    e.listings,                                   // E Listings
    e.sales,                                      // F Sales
    e.fav,                                        // G Favorites
    e.avg,                                        // H Avg. Sales / Month
    e.median,                                     // I Median Price
    e.revenue,                                    // J Est. Revenue / Month
    e.hufMedian,                                  // K Median Price in HUF
    '=D' + r + '/E' + r,                          // L Revenue HUF / Listings
    '=500000/L' + r,                              // M for 500k HUF revenue
    isoDate(e.founded),                           // N founded
    '=days(A' + r + ', N' + r + ')/365',          // O years
    e.prevE ? '=E' + r + '-E' + p : '',           // P listings diff
    e.prevF ? '=F' + r + '-F' + p : '',           // Q items sold
    (e.prevF && e.prevPrice)                      // R est. revenue / month
      ? '=(F' + r + '-F' + p + ')*' + e.prevPrice + p + '/24'
      : ''
  ];
  sh.getRange(r, 4, 1, row.length).setValues([row]);
}

function isoDate(s) {
  var p = s.split('-');
  return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
}
'''
script = (script
          .replace('__DATA__', json.dumps(entries, ensure_ascii=False, indent=1))
          .replace('__QAGAZZZ__', json.dumps(q, ensure_ascii=False)))

open("update-revenue-estimation.gs", "w").write(script)
print("written:", len(script), "chars,", len(entries), "entries + Qagazzz")
