---
type: Finding
title: Lézervágott vs papír/karton layered — külön piac-e, és mi fáj a vevőnek
description: "1878 review / 49 eladó: a KÍNÁLAT erősen szétválik (67% lézer-eladó, 12% papír), a FÁJDALOM viszont nem — az összeszerelés mindkét oldalon 2,5% körül a legfőbb panasz. A 9 legrosszabb review-ból 2 pontosan a vágásbiztonságról szól."
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-09T12:00:00Z
sources:
  - resource: /assets/data/reviews.json
    title: 1581 review (Apify, 2026-08-08)
  - resource: /assets/data/nc_reviews.json
    title: 609 review (Apify, 2026-08-08); együtt dedupolva 1878
---

# Lézervágott vs papír/karton layered

> **KORREKCIÓ 2026-08-09.** Az alábbi „a fájdalom nem válik szét" állítás **átfedő mintán**
> készült: a `mindketto` besorolású listingek mindkét oldal alapjába beleszámítottak, ami a kisebb
> (papír) oldalt lézeres tartalommal hígította. Átfedésmentes újraszámolással (laser-only 886
> review / 42 eladó, paper-only 196 review / 17 eladó) **két panasznál valódi különbség van**:
> a **törékenység** (fa 0,68% vs papír **0,00%**, 95% CI [+0,14; +1,22] pp) és a **méretezés**
> (fa 1,92% vs papír **0,00%**, CI [+1,02; +2,82] pp). Az összeszerelés és az illeszkedés
> továbbra sem dönthető el (a CI átmegy a nullán). A javított kép a
> [[pitfalls/2026-08-09-overlapping-side-buckets]] oldalon, a stratégiai következménnyel együtt.

## Lényeg

A hipotézis — hogy a lézeres és a papíros layered nagyon más piac — **félig igazolódott, és a
másik fele a fontosabb**:

- **A kínálat tényleg szétválik.** 49 eladóból **33 (67,3%) lézer-oldali**, 6 (12,2%) papír-oldali,
  10 (20,4%) vegyes. A keresési oldalon még élesebb: `laser cut svg` 1 900 keresés, `cricut shadow
  box` 130, `3d papercut` 7.
- **A fájdalom viszont NEM válik szét.** Az első számú panasz mindkét oldalon ugyanaz és
  gyakorlatilag azonos arányban: **összeszerelés / útmutató hiánya — lézer 2,5%, papír 2,6%.**
  A törékenység is: 0,9% vs 1,0%.
- **A vevő gyakran nem is dönti el előre az anyagot.** Egy kifejezetten lézeres nevű bolt
  (MagicVectorLaser) review-ja: *„High quality. Worked with cardstock."* A fájl ugyanaz, az anyag
  a vevő döntése.

Vagyis: **nem két terméket kell csinálni, hanem egy fájlt, ami mindkét anyagon kiszámíthatóan
működik — és ezt ki is kell mondani.** A mezőny ezt nem teszi.

## Populáció

**1878 dedupolt review** (nyers 2190, `receipt_id` szerint dedupolva), **1272 különálló listing**,
**49 eladó**. Az oldalbesorolás a *listing címe* alapján történt (gép- és anyagszavak), az arányokat
**eladóra és review-alapra normalizálva** közlöm — nem keresési sorra. Lásd
[[pitfalls/2026-08-08-wrong-unit-of-independence]].

## A kínálat szétválik

| oldal | eladó | arány |
|---|---:|---:|
| lézer | 33 | 67,3% |
| vegyes | 10 | 20,4% |
| papír | 6 | 12,2% |

Kereslet oldalról ugyanez (Insights, 2026-08-09, 30 nap):

| kifejezés | keresés | találat | ker./1000 |
|---|---:|---:|---:|
| laser cut svg | 1 900 | 536,1k | 3,5 |
| glowforge svg | 358 | 275,4k | 1,3 |
| cricut shadow box | 130 | 20,7k | 6,3 |
| cardstock svg | 84 | 24,8k | 3,4 |
| 3d papercut | 7 | 13k | 0,5 |

A lézeres oldal **15-ször nagyobb keresési volumenű**, de sokkal telítettebb. A papíros oldal
kicsi — **de vigyázat**: a gépnév eladói szó. A vevő a motívumra keres, nem a gépre
([[findings/etsy-first-party-search-data]]), ezért ez a táblázat a kínálatot méri jobban, mint a
keresletet.

## A fájdalom nem válik szét

| panasz | lézer-oldal (1488 review) | papír-oldal (798 review) |
|---|---|---|
| **összeszerelés / útmutató** | 37 rev = **2,5%**, 23 eladó | 21 rev = **2,6%**, 12 eladó |
| méretezés / átskálázás | 24 rev = 1,6%, 17 eladó | 7 rev = 0,9%, 7 eladó |
| törékeny / túl vékony | 14 rev = 0,9%, 11 eladó | 8 rev = 1,0%, 5 eladó |
| rétegek nem illeszkednek | 6 rev = 0,4%, 5 eladó | 2 rev = 0,25%, 2 eladó |
| hiányzó fájl vagy réteg | 2 rev, 2 eladó | 1 rev, 1 eladó |

Az egyetlen valódi eltérés a **méretezés** (1,6% vs 0,9%): a lézeres vevő gyakrabban skáláz, mert
az anyagvastagság és a gépasztal mérete köti.

## A 9 legrosszabb review — mind lézer-oldali listingen

A korpusz **99,5%-a 4–5 csillag** (5★: 1798, 4★: 71, ≤3★: 9). A kilenc kudarc a teljes lista:

| ★ | mit mond |
|---|---|
| 1 | „only engraveable files, cannot cut the files out!" |
| 1 | „svg file doesn't contain all the layers as advertised" |
| 2 | „dxf and dwg files are not included in the download" |
| 1 | eladó törölte a listinget, nincs visszatérítés |
| 1 | ugyanez spanyolul: a bolt levette a terméket, újra fizettetnék |
| 1 | üres/értelmetlen szöveg |
| 1 | **„The original size of the design is 294 × 274 mm, and at this scale the details are too small. Some lines end up being thinner than 0.5 mm"** |
| 3 | „archivos… algo pesados y hacen lento el equipo" (a fájl túl nehéz, lassítja a gépet) |
| 2 | **„file worked great. finished product was very thin and broke easily."** |

**A kilencből kettő pontosan az, amit a vágásbiztonsági riportunk mér** (minimum anyagszélesség),
egy pedig a fájlsúly, amit a `simplify` lépés kezel. Ez a differenciálónk első független
megerősítése — nem mi mondjuk, hogy fontos, hanem a csalódott vevő.

## A rés, amit senki nem tölt be

A fájdalom-sorrend alapján három dolog hiányzik a mezőnyből, és mindhárom **abból esik ki, amit
már kiszámolunk**:

1. **Összeszerelési útmutató** — a #1 panasz mindkét oldalon, 35 eladót érint.
   Nálunk már van: `assembly_guide.png` (rétegenként egy panel).
2. **Biztonságos méretezési tartomány** — a méretezés a 2. panasz, és a legrosszabb review
   szó szerint erről szól. **Senki nem ír alsó határt.** Nálunk kiszámítható a leggyengébb
   darabból: `min_scale_pct = MIN_WEB / leggyengébb`. Beépítve a `report.json`-ba
   (a 0011-es kelta csomónál: **34%, azaz 101 mm-ig biztonságos**).
3. **Anyagfüggetlen ígéret** — mivel a vevő maga választ anyagot, a fájlnak papíron és
   3 mm lemezen is működnie kell, és ezt ki kell írni. A 2 mm-es minimum web mindkettőn tartható.

## Fenntartások

- Az oldalbesorolás **listingcím-alapú**, nem a ténylegesen használt anyag. A review-szövegek
  csak ~8%-ában van egyáltalán anyagszó.
- **A 9 kudarc mind lézer-oldalon van, papíron egy sem** — de 9 esetnél ez lehet véletlen
  (arányosan ~3 papírosat várnánk). Nem állítom, hogy a papír biztonságosabb.
- A korpusz 2026-08-08-i Apify-lehúzás, nem frissült; a kreditek elfogytak.
- A `cricut shadow box` −71,7%-os trendje 130 keresésen áll, a zajküszöb alatt — értelmezhetetlen.

## Provenancia

`<scratchpad>/pvl2.py` az `assets/data/reviews.json` + `nc_reviews.json` fájlokon.
Kapcsolódik: [[findings/review-mining]], [[findings/listing-craft]],
[[findings/competitor-listing-images]], [[workflows/production-pipeline]].
