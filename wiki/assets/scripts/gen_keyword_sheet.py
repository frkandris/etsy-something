#!/usr/bin/env python3
"""Apps Script that writes the keyword database into a new sheet tab."""
import json, pathlib

D = pathlib.Path(__file__).resolve().parent.parent / "data" / "keywords"
rows = json.load(open(D / "keywords.json"))

FILE_INTENT = ("svg", "dxf", "cut file", "cutting file", "cricut", "glowforge",
               "laser cut", "template", "digital download", "papercraft",
               "clipart", "png", "stencil", "pattern", "vector")
FAMILY = {
    "kutya": ("dog", "puppy", "dachshund", "chihuahua", "corgi", "retriever",
              "shepherd", "collie", "bulldog", "paw", "pet"),
    "macska": ("cat", "kitty", "kitten"),
    "szarvas / vad": ("deer", "buck", "hunting", "wildlife", "woodland", "reindeer", "elk"),
    "tree of life / kelta": ("tree of life", "celtic", "yggdrasil", "sacred geometry", "spiritual"),
    "mandala": ("mandala", "zentangle", "rosette"),
    "shadow box": ("shadow box", "shadowbox", "light box"),
    "papercraft": ("papercraft", "paper craft", "paper art", "papercut", "cardstock", "low poly"),
    "unnep": ("christmas", "halloween", "easter", "valentine", "holiday", "ornament"),
    "nev / monogram": ("monogram", "name sign", "family tree", "custom"),
    "viragos": ("floral", "flower", "rose", "sunflower", "botanical"),
}


def fam(t):
    for k, ws in FAMILY.items():
        if any(w in t for w in ws):
            return k
    return "egyeb"


out = []
for r in rows:
    t = r["term"]
    out.append([
        t,
        r["searches"], r["results"], r["ratio"],
        round(r["ratio"] / 6.3, 1),
        r["trend"] if r["trend"] is not None else "",
        "fajl" if any(k in t for k in FILE_INTENT) else "termek",
        fam(t),
        "zaj" if r["searches"] < 300 and r["trend"] is not None else "",
        ", ".join(r["seeds"][:3]),
    ])
out.sort(key=lambda x: -x[3])

HEAD = ["kulcsszo", "kereses / 30 nap", "talalat", "kereses / 1000 listing",
        "x alapertek (layered svg)", "trend %", "szandek", "csalad",
        "trend megbizhatosag", "honnan jott"]

js = '''/**
 * Etsy Marketplace Insights keyword database.
 *
 * 210 keywords collected 2026-08-07/08 from the shop's own Marketplace Insights
 * (Etsy Plus). Seeds came from the competitor title corpus; each seed query also
 * yields ~36 related keywords WITH their own search and result counts, which is
 * where most of these rows come from.
 *
 * "kereses / 1000 listing" is the headline metric: monthly searches per thousand
 * competing listings. Higher = less saturated. The baseline is `layered svg` at
 * 6.3; the "x alapertek" column is the multiple of that.
 *
 * "szandek" separates FILE intent (someone buying a cutting file - our market)
 * from PRODUCT intent (someone buying a finished object). Do not compare across
 * the two: `shadow box` at 153.5 is mostly people buying a physical memory box.
 *
 * Trends were all measured in August 2026, so they are comparable with each
 * other but confounded with season. Below ~300 monthly searches the trend
 * percentage is noise - flagged in the "trend megbizhatosag" column.
 *
 * Creates the sheet if it does not exist; refuses to overwrite a non-empty one
 * unless OVERWRITE is true.
 */

var SHEET_NAME = 'keywords';
var OVERWRITE = false;

var HEAD = __HEAD__;
var DATA = __DATA__;

function fillKeywordSheet() {
  var ss = SpreadsheetApp.getActive() || SpreadsheetApp.openById(
    '1j-52jMBxTxgZ3-ywNekNGKjraP6u2QYDKxLVdMfsqUQ');
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
  } else if (!OVERWRITE && sh.getLastRow() > 0) {
    throw new Error('"' + SHEET_NAME + '" is not empty (' + sh.getLastRow() +
      ' rows). Clear it, or set OVERWRITE = true at the top of the script.');
  }

  sh.getRange(1, 1, 1, HEAD.length).setValues([HEAD])
    .setFontWeight('bold').setWrap(true);
  sh.getRange(2, 1, DATA.length, HEAD.length).setValues(DATA);

  sh.getRange(2, 2, DATA.length, 2).setNumberFormat('#,##0');
  sh.getRange(2, 4, DATA.length, 2).setNumberFormat('0.0');
  sh.getRange(2, 6, DATA.length, 1).setNumberFormat('+0.0;-0.0');
  sh.setFrozenRows(1);
  sh.getRange(1, 1, DATA.length + 1, HEAD.length).createFilter();
  sh.autoResizeColumns(1, HEAD.length);

  Logger.log(DATA.length + ' keywords written to ' + SHEET_NAME);
}
'''
js = (js.replace('__HEAD__', json.dumps(HEAD, ensure_ascii=False))
        .replace('__DATA__', json.dumps(out, ensure_ascii=False, indent=0)))
p = pathlib.Path(__file__).resolve().parent.parent.parent.parent / "fill-keyword-sheet.gs"
p.write_text(js)
print("rows:", len(out), "->", p)
