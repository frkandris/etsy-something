---
type: FAQ
title: Visszatérő kérdések
description: Amit már megválaszoltunk, hogy ne kelljen újra levezetni.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Visszatérő kérdések

## Nem csak két szerencsés bolt ez az egész?

Nem. 173 bolt látszik öt keresés top találataiban; deduplikálva 35 specialista, ebből **21** katalógussal
igazolt layered bolt. De a
kétely jogos volt és termékeny: pont ebből derült ki, hogy a populáció fele egyetlen listinggel került
be ([[pitfalls/2026-08-07-single-listing-attribution]]).

## Mennyi az esély, hogy beindul?

A ma is rangsoroló, 3 évnél fiatalabb specialista boltok kb. **24%-a** van 500 ezer HUF/hó fölött.
**Ez nem belépési valószínűség**, hanem rangsorolás-túlélési arány: a megbukott és bezárt belépők
szerkezetileg hiányoznak a mintából. Lásd [[findings/catalogue-size-and-throughput]].

## Hány listing kell?

**100–300** — a dedupolt adaton ez a legjobb listingenkénti sáv (2 009 HUF/listing, n=8), a 300–700
sávban 825. A <100 sávban a deduplikálás után **egy** bolt maradt. *(A korábban idézett két kis kivétel — 29 és 72 listing — a deduplikálás után kiesett.)*

## Kell lézervágó?

Nem kell megvenni. Fali panelnél nincs illesztés, tehát nem kell iteratív tesztvágás — alkalmi
hozzáférés elég a validációhoz és a valódi fotókhoz. Lásd [[workflows/production-pipeline]].

## Miért ne akciózzunk, ha mindenki akciózik? — **VISSZAVONVA**

**Ez az állítás megbukott a 2026-08-08-i auditon:** deduplikált populáción a nem akciózó csoport
**3 boltra** esik és a sávok nem monotonok, tehát a kérdés a mi adatunkból **nem dönthető el**.
Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]]. Az eredeti érvelés: **Fontos:** ez korreláció
— valószínűleg a jobb termék teszi lehetővé az akciómentességet, nem fordítva.
[[findings/pricing-and-discounting]]

## Miért nem SalesDoe-t használunk a niche-kutatásban?

Két indok volt, és **2026-08-12-én az egyik elavult**:

- **Érvényes:** a medián ára a lista- és az akciós ár között ingadozik, ami a mélyen
  diszkontálóknál felfelé torzít. [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]]
- **Elavult:** „boltonként egy böngésző-kattintást igényel" — **van API-ja**
  (`/api/shops/shop?shop_name=`), tehát tömegesen lekérdezhető.
  Lásd [[methods/browser-data-endpoints]].

Tehát a bolt-bevételhez **használható**, ha az árat külön ellenőrizzük; a niche kereslet-oldalához
továbbra sem ő az elsődleges forrás, hanem az Etsy Marketplace Insights.

## Tudjuk már a keresési volument?

Igen, 2026-08-07 óta: az **Etsy Marketplace Insights** (Etsy Plus) első kézből adja, korlátlanul.
A `layered svg` 1 200 keresést kap 30 nap alatt, 189 900 találat mellett, **+11,1%-os trenddel**.
Amit nem ad: 30 napnál hosszabb historikus adatot, tehát szezonalitást.
[[findings/etsy-first-party-search-data]]

## Mennyibe kerül egy új niche felmérése?

Nagyságrendileg **8–12 USD** Apify-on (5 keresés + bolt-adat + katalógus-mintavétel), plusz
~30–45 perc. Lásd [[methods/apify-actors]].

## Miért nem lehet API-ból írni a Sheetet?

A Google szervezeti policy tiltja a gcloud ADC klienst a `spreadsheets` scope-ra, az rclone tokenje
pedig olyan projekthez tartozik, ahol a Sheets API nincs engedélyezve.
[[decisions/2026-08-06-apps-script-for-sheets]]
