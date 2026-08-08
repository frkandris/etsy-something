/**
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

var ENTRIES = [
 {
  "anchor": 38,
  "slug": "MtInfinityInc",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K",
  "hufMonth": 1542368,
  "listings": 564,
  "sales": 7089,
  "fav": 1352,
  "avg": 179,
  "median": "143.2 SGD",
  "revenue": "6252 SGD",
  "hufMedian": 35327,
  "founded": "2023-04-17"
 },
 {
  "anchor": 39,
  "slug": "CuteCakeTuber",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K",
  "hufMonth": 966919,
  "listings": 78,
  "sales": 4961,
  "fav": 1131,
  "avg": 139,
  "median": "9.59 EUR",
  "revenue": "2652 EUR",
  "hufMedian": 3497,
  "founded": "2023-08-14"
 },
 {
  "anchor": 40,
  "slug": "GuangCaiArts",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K",
  "hufMonth": 1022876,
  "listings": 114,
  "sales": 6178,
  "fav": 2410,
  "avg": 207,
  "median": "20 CAD",
  "revenue": "4526 CAD",
  "hufMedian": 4520,
  "founded": "2024-02-12"
 },
 {
  "anchor": 41,
  "slug": "IkoRenStudio",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K"
 },
 {
  "anchor": 42,
  "slug": "miikutea",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K",
  "hufMonth": 1607273,
  "listings": 8,
  "sales": 3441,
  "fav": 1416,
  "avg": 116,
  "median": "40 USD",
  "revenue": "5081 USD",
  "hufMedian": 12653,
  "founded": "2024-02-14"
 },
 {
  "anchor": 43,
  "slug": "YuxMakerStudio",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 555064,
  "listings": 2,
  "sales": 1960,
  "fav": 404,
  "avg": 56,
  "median": "150 MYR",
  "revenue": "7176 MYR",
  "hufMedian": 11602,
  "founded": "2023-09-16"
 },
 {
  "anchor": 44,
  "slug": "TinyMangaGifts",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 1472325,
  "listings": 13,
  "sales": 1496,
  "fav": 1409,
  "avg": 31,
  "median": "1333 HKD",
  "revenue": "36516 HKD",
  "hufMedian": 53747,
  "founded": "2022-07-15"
 },
 {
  "anchor": 45,
  "slug": "LogicCreationDesign",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": ""
 },
 {
  "anchor": 46,
  "slug": "Hayukituber",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 519294,
  "listings": 8,
  "sales": 1445,
  "fav": 778,
  "avg": 38,
  "median": "26.73 GBP",
  "revenue": "1219 GBP",
  "hufMedian": 11387,
  "founded": "2023-06-19"
 },
 {
  "anchor": 47,
  "slug": "CraftsClio",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": ""
 },
 {
  "anchor": 48,
  "slug": "CybDigital",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 1392043,
  "listings": 78,
  "sales": 1769,
  "fav": 1097,
  "avg": 79,
  "median": "40 EUR",
  "revenue": "3818 EUR",
  "hufMedian": 14584,
  "founded": "2024-09-22"
 },
 {
  "anchor": 49,
  "slug": "2dlivemodelStudio",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 1265320,
  "listings": 144,
  "sales": 3751,
  "fav": 1155,
  "avg": 165,
  "median": "12 USD",
  "revenue": "4000 USD",
  "hufMedian": 3796,
  "founded": "2024-09-13"
 },
 {
  "anchor": 50,
  "slug": "DoodliStudio",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 59794,
  "listings": 41,
  "sales": 581,
  "fav": 133,
  "avg": 25,
  "median": "5 EUR",
  "revenue": "164 EUR",
  "hufMedian": 1823,
  "founded": "2024-08-18"
 },
 {
  "anchor": 51,
  "slug": "SenhaiVtuber",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": ""
 },
 {
  "anchor": 53,
  "slug": "pngVtubers",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "K",
  "hufMonth": 1572300,
  "listings": 93,
  "sales": 31173,
  "fav": 3298,
  "avg": 867,
  "median": "8 AUD",
  "revenue": "7057 AUD",
  "hufMedian": 1782,
  "founded": "2023-08-08"
 },
 {
  "anchor": 54,
  "slug": "NeoStreamlabs",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 2294428,
  "listings": 924,
  "sales": 36313,
  "fav": 3183,
  "avg": 912,
  "median": "6.415 EUR",
  "revenue": "6293 EUR",
  "hufMedian": 2339,
  "founded": "2023-04-12"
 },
 {
  "anchor": 55,
  "slug": "LilWoogies",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 903479,
  "listings": 394,
  "sales": 9046,
  "fav": 2174,
  "avg": 258,
  "median": "8.1 EUR",
  "revenue": "2478 EUR",
  "hufMedian": 2953,
  "founded": "2023-09-06"
 },
 {
  "anchor": 56,
  "slug": "VTubeWorld",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": ""
 },
 {
  "anchor": 57,
  "slug": "NinisDigitalArt",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 62347,
  "listings": 20,
  "sales": 1296,
  "fav": 289,
  "avg": 51,
  "median": "3 EUR",
  "revenue": "171 EUR",
  "hufMedian": 1094,
  "founded": "2024-06-24"
 },
 {
  "anchor": 58,
  "slug": "BankuriPet",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "",
  "hufMonth": 599129,
  "listings": 178,
  "sales": 4383,
  "fav": 938,
  "avg": 142,
  "median": "5.15 USD",
  "revenue": "1894 USD",
  "hufMedian": 1629,
  "founded": "2024-01-12"
 },
 {
  "anchor": 60,
  "slug": "Ribsdesign",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I"
 },
 {
  "anchor": 61,
  "slug": "DENIDigitalArtSudio",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 950255,
  "listings": 271,
  "sales": 29008,
  "fav": 848,
  "avg": 738,
  "median": "4 USD",
  "revenue": "3004 USD",
  "hufMedian": 1265,
  "founded": "2023-04-28"
 },
 {
  "anchor": 62,
  "slug": "PaperDog3D",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 367259,
  "listings": 255,
  "sales": 7140,
  "fav": 972,
  "avg": 236,
  "median": "5 USD",
  "revenue": "1161 USD",
  "hufMedian": 1582,
  "founded": "2024-01-31"
 },
 {
  "anchor": 63,
  "slug": "EmsiDigital",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 69438,
  "listings": 269,
  "sales": 3916,
  "fav": 324,
  "avg": 99,
  "median": "1.65 GBP",
  "revenue": "163 GBP",
  "hufMedian": 703,
  "founded": "2023-04-22"
 },
 {
  "anchor": 64,
  "slug": "PixieHawkGraphics",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 94244,
  "listings": 303,
  "sales": 3913,
  "fav": 328,
  "avg": 99,
  "median": "25 SEK",
  "revenue": "2820 SEK",
  "hufMedian": 836,
  "founded": "2023-04-21"
 },
 {
  "anchor": 65,
  "slug": "ColorLayerArt",
  "dead": false,
  "prevE": true,
  "prevF": false,
  "prevPrice": "I",
  "hufMonth": 2192800,
  "listings": 559,
  "sales": 32171,
  "fav": 2848,
  "avg": 957,
  "median": "7 USD",
  "revenue": "6932 USD",
  "hufMedian": 2214,
  "founded": "2023-10-19"
 },
 {
  "anchor": 66,
  "slug": "SVGplugDz",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 810870,
  "listings": 483,
  "sales": 78270,
  "fav": 2018,
  "avg": 1455,
  "median": "1.6 EUR",
  "revenue": "2224 EUR",
  "hufMedian": 583,
  "founded": "2022-02-12"
 },
 {
  "anchor": 67,
  "slug": "DXFpage",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 863897,
  "listings": 661,
  "sales": 59416,
  "fav": 3656,
  "avg": 674,
  "median": "3 USD",
  "revenue": "2731 USD",
  "hufMedian": 949,
  "founded": "2019-04-01"
 },
 {
  "anchor": 68,
  "slug": "LunamCo",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 564965,
  "listings": 557,
  "sales": 133615,
  "fav": 2416,
  "avg": 1888,
  "median": "0.97 USD",
  "revenue": "1786 USD",
  "hufMedian": 307,
  "founded": "2020-09-13"
 },
 {
  "anchor": 69,
  "slug": "Art4youSpace",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 1463343,
  "listings": 346,
  "sales": 113816,
  "fav": 6158,
  "avg": 1307,
  "median": "3 USD",
  "revenue": "4626 USD",
  "hufMedian": 949,
  "founded": "2019-05-05"
 },
 {
  "anchor": 70,
  "slug": "UxcomShop",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 207093,
  "listings": 565,
  "sales": 13451,
  "fav": 460,
  "avg": 245,
  "median": "2.2 EUR",
  "revenue": "568 EUR",
  "hufMedian": 802,
  "founded": "2022-01-09"
 },
 {
  "anchor": 71,
  "slug": "wallartbox",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I"
 },
 {
  "anchor": 73,
  "slug": "DigitalLinks",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I"
 },
 {
  "anchor": 74,
  "slug": "WildInkDigital",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 702253,
  "listings": 875,
  "sales": 19861,
  "fav": 1558,
  "avg": 493,
  "median": "3.99 USD",
  "revenue": "2220 USD",
  "hufMedian": 1262,
  "founded": "2023-03-28"
 },
 {
  "anchor": 75,
  "slug": "TheMelodyFace",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 2706790,
  "listings": 861,
  "sales": 81808,
  "fav": 3635,
  "avg": 1142,
  "median": "3.99 EUR",
  "revenue": "7424 EUR",
  "hufMedian": 1455,
  "founded": "2020-08-17"
 },
 {
  "anchor": 76,
  "slug": "TheDigitalCraftCo",
  "dead": true,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I"
 },
 {
  "anchor": 77,
  "slug": "MagicVectorLaser",
  "dead": false,
  "prevE": true,
  "prevF": false,
  "prevPrice": "I",
  "hufMonth": 7105088,
  "listings": 934,
  "sales": 94316,
  "fav": 10394,
  "avg": 1408,
  "median": "7.5 USD",
  "revenue": "22461 USD",
  "hufMedian": 2372,
  "founded": "2021-01-07"
 },
 {
  "anchor": 78,
  "slug": "ARTsteady",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 1579752,
  "listings": 1506,
  "sales": 99823,
  "fav": 3163,
  "avg": 1350,
  "median": "2.4 USD",
  "revenue": "4994 USD",
  "hufMedian": 759,
  "founded": "2020-06-08"
 },
 {
  "anchor": 79,
  "slug": "SignReadyVectorArt",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 347647,
  "listings": 1264,
  "sales": 35868,
  "fav": 1342,
  "avg": 340,
  "median": "2.2 USD",
  "revenue": "1099 USD",
  "hufMedian": 696,
  "founded": "2017-10-25"
 },
 {
  "anchor": 80,
  "slug": "CraftyArtCafe",
  "dead": false,
  "prevE": true,
  "prevF": true,
  "prevPrice": "I",
  "hufMonth": 3911737,
  "listings": 3598,
  "sales": 235390,
  "fav": 6054,
  "avg": 4290,
  "median": "2 USD",
  "revenue": "12366 USD",
  "hufMedian": 633,
  "founded": "2022-01-10"
 },
 {
  "anchor": 82,
  "slug": "EricaDigitalDesign",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 1815708,
  "listings": 939,
  "sales": 176799,
  "fav": 10601,
  "avg": 1855,
  "median": "1.5 EUR",
  "revenue": "4980 EUR",
  "hufMedian": 547,
  "founded": "2018-08-28"
 },
 {
  "anchor": 83,
  "slug": "SouthForkSVG",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 1122655,
  "listings": 5952,
  "sales": 163707,
  "fav": 3998,
  "avg": 2640,
  "median": "0.98 USD",
  "revenue": "3549 USD",
  "hufMedian": 310,
  "founded": "2021-06-06"
 },
 {
  "anchor": 84,
  "slug": "squishsjewels",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 113562,
  "listings": 292,
  "sales": 5207,
  "fav": 137,
  "avg": 140,
  "median": "2.49 USD",
  "revenue": "359 USD",
  "hufMedian": 788,
  "founded": "2023-06-29"
 },
 {
  "anchor": 85,
  "slug": "SunnyDigitalArts",
  "dead": true,
  "prevE": false,
  "prevF": false,
  "prevPrice": ""
 },
 {
  "anchor": 86,
  "slug": "PrintCutCA",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 330186,
  "listings": 143,
  "sales": 6587,
  "fav": 175,
  "avg": 197,
  "median": "7 CAD",
  "revenue": "1461 CAD",
  "hufMedian": 1582,
  "founded": "2023-10-22"
 },
 {
  "anchor": 87,
  "slug": "VectorCraftLab",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 158798,
  "listings": 724,
  "sales": 12250,
  "fav": 701,
  "avg": 149,
  "median": "3.3 USD",
  "revenue": "502 USD",
  "hufMedian": 1044,
  "founded": "2019-10-07"
 },
 {
  "anchor": 88,
  "slug": "CraftySVGKiwi",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 1750254,
  "listings": 1152,
  "sales": 94396,
  "fav": 2217,
  "avg": 1890,
  "median": "2.99 USD",
  "revenue": "5533 USD",
  "hufMedian": 946,
  "founded": "2022-06-08"
 },
 {
  "anchor": 89,
  "slug": "digitaldesignsvgpng",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 203084,
  "listings": 239,
  "sales": 18686,
  "fav": 671,
  "avg": 321,
  "median": "2 USD",
  "revenue": "642 USD",
  "hufMedian": 633,
  "founded": "2021-10-01"
 },
 {
  "anchor": 90,
  "slug": "BlankPrintsArts",
  "dead": false,
  "prevE": false,
  "prevF": false,
  "prevPrice": "",
  "hufMonth": 1857806,
  "listings": 1220,
  "sales": 9942,
  "fav": 328,
  "avg": 327,
  "median": "18 USD",
  "revenue": "5873 USD",
  "hufMedian": 5694,
  "founded": "2024-01-26"
 }
];

// Qagazzz's 2026 row (row 37) already exists with its URL and topic filled in.
var QAGAZZZ = {"anchor": 36, "slug": "Qagazzz", "dead": false, "prevE": true, "prevF": true, "prevPrice": "K", "hufMonth": 715222, "listings": 53, "sales": 7521, "fav": 1417, "avg": 105, "median": "4.46 USD", "revenue": "2261 USD", "hufMedian": 1411, "founded": "2020-08-24"};

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
    throw new Error('Aborted, the sheet does not look as expected:\n' +
                    problems.join('\n'));
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
