---
type: Finding
title: Kulcsszó-adatbázis — 345 kifejezés volumennel és telítettséggel
description: 345 kulcsszo volumennel; a kulcsszo-meresek ervenyesek, de a beloluk levont norse/kelta termekajanlas a review-adaton megbukott.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T10:00:00Z
sources:
  - resource: /assets/data/keywords/keywords.json
    title: 345 kulcsszó, Etsy Marketplace Insights, 2026-08-07/08
  - resource: /assets/data/keywords/raw_01.txt
    title: nyers crawl-kimenet (raw_01–raw_04)
---

# Kulcsszó-adatbázis

> **AUDIT 2026-08-08 UTÁN.** A **norse/kelta „legjobb hosszú farok" következtetés visszavonva.** A
> [[findings/review-mining]] szerint a témában rangsoroló 16 bolt 609 review-jából csak **2,8%**
> rétegzett, 58,8% gravírozó/tárgy — a kereslet valós, de más termékformát akar. A kulcsszó-mérések
> önmagukban érvényesek, a belőlük levont termékajánlás nem.

## Hogyan épült

A seedek a **konkurencia terméknevéből** jöttek ([[findings/listing-craft]] korpusza, 777 cím a 33
igazolt bolttól). Minden seed lekérdezés a Marketplace Insightson két dolgot ad:

1. a seed saját adatát (keresés, találat, trend),
2. egy lapozható kapcsolódó táblát **~36 további kulcsszóval, mindegyik saját keresés- és
   találatszámával**.

Ez utóbbi a lényeg: egy lekérdezés ~36 rekordot ad ingyen. **10 seed → 345 kulcsszó.**
Seedek: `cat svg`, `dog breed svg`, `shadow box svg`, `deer svg`, `tree of life svg`,
`3d papercraft`, `celtic svg`, `religious svg`, `viking svg`, `floral svg`.

Adat: `assets/data/keywords/keywords.json`. Szkriptek: `assets/scripts/build_keyword_db.py`,
`assets/scripts/gen_keyword_sheet.py`. Sheet: `fill-keyword-sheet.gs` (maga hozza létre a fület).

## A metrika

**`keresés / 1000 listing`** — havi keresés ezer versenyző listingre. Alapérték: `layered svg` = **6,3**.

**Szándék szerint el kell különíteni:** fájlszándék (vágósablont keres — a mi piacunk) vs
terméktartás (kész tárgyat keres). A `shadow box` 153,5-e az utóbbi.

## Motívumcsaládok — a kínálati oszlop a döntő

Csak fájlszándékú kifejezéseken:

| család | kulcsszó | medián arány | legjobb | össz. keresés | **medián kínálat** |
|---|---:|---:|---:|---:|---:|
| shadow box | 2 | 43,6 | 75,6 | 2 886 | 29 450 |
| mandala | 1 | 18,8 | 18,8 | 741 | 39 500 |
| **tree of life** | 8 | **12,2** | 26,0 | 1 231 | **10 550** |
| macska | 7 | 8,6 | 38,9 | 5 503 | 93 900 |
| kutya | 14 | 7,7 | 45,9 | 2 848 | 16 200 |
| **kelta** | 15 | 7,1 | 17,0 | 984 | **8 700** |
| **viking / norse** | 19 | 6,5 | **109,4** | 1 693 | **5 700** |
| szarvas / vad | 12 | 5,0 | 14,8 | 2 924 | 40 850 |
| vallási | 14 | 3,7 | 15,0 | 11 335 | 108 750 |
| virágos | 17 | 3,1 | 34,3 | 13 162 | 363 400 |
| papercraft | 13 | 0,2 | 34,7 | 2 572 | 384 400 |

**A medián arány félrevezet a hosszú farkú családoknál.** A viking család mediánja azért alacsony
(6,5), mert sok apró kifejezést tartalmaz (`odin svg` 22 keresés, `viking axe stencil` 15) — de a
**kínálata mindössze 5 700 listing**, a mandala 39 500-ának és a virágos 363 400-ának töredéke.

## A viking / kelta / tree of life komplexum

Ez a három család **egy vizuális nyelvet** beszél (csomózás, rúnák, mitológia), tehát **egy
designstílus lefedi mindhármat**. Együtt:

| | viking+kelta+tree of life | kutya |
|---|---:|---:|
| kulcsszó | **42** | 14 |
| összes keresés | **3 908** | 2 848 |
| medián kínálat | **~7 000** | 16 200 |

**Több hosszú farkú volumen, feleannyi versenytárs, és tematikailag koherens.** Ez erősebb hosszú
farok, mint a kutyafajta — lásd [[findings/keyword-demand-sweep]], ahol a kutya-tézis kiindult.

És illeszkedik a termékhez: a **kelta csomózás természeténél fogva rétegzett**, tehát a multilayer
forma nem ráerőltetett, hanem a motívum sajátja.

A 42 kulcsszó ráadásul kész katalógusterv: pont a [[findings/catalogue-size-and-throughput]] szerinti
100–300 listinges optimum alsó felébe esik. *(Az ajánlás maga a review-adaton megbukott, lásd a lap tetejét.)*

## A legjobb fájlszándékú kifejezések

| kifejezés | keresés | találat | ker./1000 | x alap |
|---|---:|---:|---:|---:|
| **viking helmet svg** | 197 | **1 800** | **109,4** | 17x |
| **shadow box svg** | 2 600 | 34 400 | 75,6 | 12x |
| dachshund svg | 514 | 11 200 | 45,9 | 7x |
| **viking svg** | 543 | 12 900 | 42,1 | 7x |
| kitty svg | 661 | 17 000 | 38,9 | 6x |
| golden retriever svg | 434 | 11 400 | 38,1 | 6x |
| low poly papercraft | 330 | 9 500 | 34,7 | 6x |
| hibiscus svg | 484 | 14 100 | 34,3 | 5x |
| sunflower svg | 1 500 | 47 200 | 31,8 | 5x |
| tree of life svg | 533 | 20 500 | 26,0 | 4x |
| viking png | 243 | 12 100 | 20,1 | 3x |
| tree of life stencil | 139 | 7 400 | 18,8 | 3x |
| tree of life dxf | 133 | 7 100 | 18,7 | 3x |
| celtic knot svg | 156 | 9 200 | 17,0 | 3x |
| viking ship svg | 96 | 5 800 | 16,6 | 3x |
| celtic knot stencil | 82 | 5 200 | 15,8 | 3x |

Termékszándékú, de a kínálati hiány miatt jelzésértékű: `yggdrasil` 645 / 7 100 = **90,8**,
`celtic knot wall art` 321 / 5 800 = **55,3**, `tree of life tapestry` 527 / 7 700 = 68,4.

## Amit kerülni kell

- **papercraft** — medián arány 0,2, medián kínálat 384 400. `papercraft template` 294 keresés
  2,4M találatra. Az egyetlen kivétel a `low poly papercraft` (34,7), ami külön terméknyelv.
- **virágos** — nagy volumen (13 162 keresés), de 363 400-as medián kínálat. Kivétel: `hibiscus svg`
  (34,3), `sunflower svg` (31,8), `daisy svg` (14,8).
- **vallási** — 11 335 keresés, de 108 750-es medián kínálat.

## Fenntartások

- **10 seedből épült**, a családok mérete egyenetlen (mandala n=1, shadow box n=2) — ezeket a
  mediánokat ne vedd komolyan.
- A kapcsolódó tábla az Etsy saját ajánlása, tehát **nem semleges minta**.
- Minden mérés 2026 augusztusából; a trendek egymáshoz képest összevethetők, de szezonálisan
  torzítottak. 300 keresés alatt a trend zaj — a sheet külön oszlopban jelzi.
- A `viking svg` −31,4%-os és a `celtic svg` +7,5%-os trendje ellentmond egymásnak; egyik sem elég
  nagy minta ahhoz, hogy irányt olvassunk ki belőle.
