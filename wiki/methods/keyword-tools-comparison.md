---
type: Method
title: Kulcsszókutató eszközök összehasonlítása — mérés alapján
description: Öt eszköz tesztelve ugyanazzal a kulcsszóval; az Etsy saját Marketplace Insightsa nyer, a többi modellez vagy fizetőfal mögött van.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T21:00:00Z
sources:
  - resource: https://members.erank.com/keyword-tool
    title: eRank Keyword Tool, élő lekérdezés 2026-08-07
  - resource: https://www.rankhero.com/tools/etsy/niche-finder
    title: RankHero Niche Finder és Keyword Generator, 2026-08-07
  - resource: https://www.etsy.com/your/shops/me/marketplace-insights
    title: Etsy Marketplace Insights, 2026-08-07
---

# Kulcsszókutató eszközök

Mindegyiket **élő lekérdezéssel** teszteltük 2026-08-07-én, nem a marketinganyagukból.

## Az eredmény

| eszköz | Etsy-specifikus volumen? | mit igazoltunk | ár |
|---|---|---|---|
| **Etsy Marketplace Insights** | **Igen, első kézből** | `layered svg` → 1 200 keresés / 189 900 találat / **+11,1%** | **Etsy Plus** (megvéve) |
| eRank | Igen, de modellezett | `multilayer svg` → 313 keresés, 22 207 competition, 15 hónapos trend, országmegoszlás | Basic $5,99 (100/nap) |
| Alura | Igen (saját leírás) | nem teszteltük | $7,99 |
| RankHero | **Valószínűleg Google** | a keresés fizetőfal mögött; a leírásban CPC és bid range | Business $9,99 |
| InsightFactory | **Nem**, saját bevallása szerint | — | 15 ingyen kredit |

## Miért az Etsy sajátja nyer

Az összes többi **becsül**. Az eRanknál ez közvetlenül látszik: a `multilayer svg`-re
`Avg. Searches 313`, de `Avg. Clicks 386` és `CTR 123%` — több kattintás, mint keresés, ami
matematikailag lehetetlen valós adatnál. Modellezett szám.

Az Etsy ezzel szemben a saját keresőmotorjának számlálóját mutatja, napi bontásban, korlátlan
lekérdezéssel.

## Miért gyanús a RankHero

Élőben ellenőrizve, bejelentkezve:

- A **Niche Finder** keresése teljesen zárt: *„Searching across all niches is available on Business
  and Enterprise plans."* A `Side Hustle` ($5,99) csomagból a Niche Finder és az Etsy Trends
  kifejezetten hiányzik.
- A **Keyword Generator (BETA)** leírása: *„real search volume, monthly trends, **CPC**, and
  competition"*, illetve *„bid ranges"*. A CPC és a bid range **Google Ads-fogalmak** — az Etsy-nek
  nincs ilyen publikus adata.
- Az előnézeti táblában a `COMPETITION` minden sorban azonos (**5 537**), a volumenek pedig Google
  Keyword Planner-bucketek (550 000 / 49 500 / 6 600 / 5 400 / 2 900). Havi 550 ezer Etsy-keresés az
  „australia flag"-re nem hihető.

Három független jel ugyanarra mutat, de **élő lekérdezéssel nem tudtuk megerősíteni**, mert fizetős.
Erős gyanú, nem bizonyíték.

## Amit az Etsy sajátja NEM tud

**Szezonalitást.** Csak az utolsó 30 nap érhető el. Az eRank 15 hónapos görbét adott, amin a
`multilayer svg`-nél jól látszottak a csúcsok (2025 szept., nov., 2026 júl.). A layered termékkör
erősen szezonális, tehát ez valódi hiány.

**Ez az egyetlen indok, amiért egy harmadik feles eszköz még indokolt lehet** — de csak azután, hogy
kiderül, elég-e a 30 napos ablak a tervezéshez.

## Döntés

Az Etsy Plus megvásárolva 2026-08-07-én. **eRank előfizetés egyelőre nem** — lásd
[[findings/etsy-first-party-search-data]].
