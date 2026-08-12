---
type: Finding
title: 3D-fájlos bolt-lista — SalesDoe adatokkal, a layered lista szerkezetében
description: 15 bolt SalesDoe API-ból, a Google Sheet layered-fül oszlopaival. A medián 489 ezer HUF/hó 33 listinggel — a layered oldal 274 listingjéhez képest. A hiányzó három devizára aznap kért árfolyam.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T17:00:00Z
sources:
  - resource: /assets/data/3d-print-salesdoe-2026-08-12.json
    title: 15 bolt SalesDoe API-adata
---

# 3D-fájlos bolt-lista

Ugyanaz az oszlopszerkezet, mint a Google Sheet **layered niche** fülén (gid 1600752523) és a
[[findings/verified-shop-list]]-en: `bolt | HUF/hó | listing | HUF/listing | ár | év | letöltés% |
deviza`.

## A lista

| bolt | HUF/hó | listing | HUF/listing | ár | nyitás | eladás/hó | letöltés | deviza |
|---|---:|---:|---:|---:|---|---:|---|---|
| NenoWorks | **1 472 832** | 420 | 3 507 | $12,00 | 2025-11 | 388 | 100/100 | USD |
| TheHexAndHaven | **1 419 218** | 31 | 45 781 | $5,99 | 2026-06 | 749 | 31/31 | USD |
| STLVaultStudio | **1 308 914** | 41 | 31 925 | €17,95 | 2026-04 | 200 | 41/41 | EUR |
| ZoeArtpk | 839 223 | 29 | 28 939 | $7,00 | 2026-06 | 379 | 29/29 | USD |
| KidovoStudio | 461 821 | 26 | 17 762 | €3,29 | 2026-03 | 385 | 26/26 | EUR |
| Luminarelle | 444 520 | 38 | 11 698 | €4,80 | 2025-08 | 254 | 38/38 | EUR |
| 3dsaltlab | 434 005 | 140 | 3 100 | $7,00 | 2025-10 | 196 | 100/100 | USD |
| RippleLuv | 70 858 | 65 | 1 090 | $2,00 | 2025-05 | 112 | 64/65 | USD |
| TheNovaPrintables | 52 398 | 20 | 2 620 | £3,00 | 2026-04 | 41 | 20/20 | GBP |
| AuraPrint3D | 16 079 | 33 | 487 | €2,45 | 2025-07 | 18 | 33/33 | EUR |
| STLForgeeStudio | 1 261 709 | 21 | 60 081 | 160 MAD | 2026-01 | 232 | — | MAD |
| LovaSTL | 994 208 | 28 | 35 507 | 250 MAD | 2026-04 | 117 | — | MAD |
| SolvraStudioDesigns | 835 832 | 90 | 9 287 | 10.99 CHF | 2026-04 | 195 | — | CHF |
| STLCraftVibes | 489 456 | 8 | 61 182 | 100 MAD | 2025-10 | 144 | — | MAD |
| ARENPRINT | 120 021 | 269 | 446 | 259 TRY | 2025-10 | 70 | — | TRY |

**Medián: 489 456 HUF/hó, 33 listing, 11 698 HUF/listing.** (n = 15)

A MAD, CHF és TRY kurzust **2026-08-12-én kértem le** (exchangerate-api.com), és felvettem a
[[decisions/2026-08-06-exchange-rates]] táblájába. A kilenc eredeti kurzus ugyanekkor ellenőrizve:
mind 0,6%-on belül, tehát nem kellett újraszámolni semmit.

## Amit a lista mond

**A katalógusméret itt nem hajtóerő.** A layered oldalon a [[findings/verified-shop-list]] élén
274–934 listinges boltok állnak; itt a medián **33 listing**, és a két legjobb bevételű bolt közül
az egyiknek **31**, a másiknak 420 terméke van. A `HUF/listing` szórása ezért óriási: 446-tól
61 182-ig, **137-szeres**.

**Mind digitális, és szinte mind friss.** A tíz mintavett boltból kilencnél a listingek **100%-a
letöltés**. A nyitási dátumok 2025-05 és 2026-06 közé esnek — **a legrégebbi is 15 hónapos**.

**A legjobb HUF/listing nem a legnagyobb boltnál van.** A TheHexAndHaven 31 listinggel termel
45 781 HUF/listinget, a NenoWorks 420-szal 3 507-et. Ez ugyanaz a mintázat, amit a
[[findings/catalogue-size-and-throughput]] „fókusz vs tömeg" néven ír le — csak itt a fókuszút
látszik erősebbnek.

## Fenntartások

1. **A bevétel felső becslés.** A SalesDoe ára a lista- és az akciós ár között ingadozik
   ([[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]]), és ezek a boltok tartós 50–75%-os
   akciót futtatnak. A valós bevétel **jóval alacsonyabb** lehet, és a legmélyebben diszkontálóknál
   torzít a legjobban.
2. **Az `eladás/hó` élettartam-átlag**, nem aktuális futásteljesítmény.
3. **15 bolt, nem véletlen minta** — a Marketplace Insights által felhozott listingek boltjai,
   tehát a látható fej. Megszűnt bolt nincs benne.
4. **A `letöltés%` a SalesDoe mintáján alapul** (legfeljebb 100 listing/bolt), nem a teljes
   katalóguson.
5. **A `HUF/listing` félrevezető lehet** ott, ahol a bolt egyetlen mega-bundle-ből él: a 31 listing
   közül lehet, hogy egy hozza a forgalmat.
6. **A MAD/CHF/TRY kurzus napi jegyzés, nem rögzített konvenció.** A tábla többi sora a
   2026-08-06-i rögzített árfolyamokkal készült. Az eltérés kicsi (a kilenc régi kurzus 0,6%-on
   belül van a mai jegyzéshez képest), de a két oszlop szigorúan véve nem azonos konvenciójú.

## Provenancia

`wiki/assets/data/3d-print-salesdoe-2026-08-12.json`. Kapcsolódik:
[[methods/browser-data-endpoints]], [[findings/3d-print-market-structure]],
[[findings/verified-shop-list]], [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]].
