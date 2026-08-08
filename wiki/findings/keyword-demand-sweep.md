---
type: Finding
title: Kereslet-mérés az Etsy Marketplace Insightson — 40+ kifejezés
description: A shadow box svg a legjobb fájlszándékú kifejezés (75,4 keresés/1000 listing); a hosszú farok volumenben nyer, de a kombinációt senki nem keresi, ezért a differenciálás vizuális, nem lexikai.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T00:00:00Z
sources:
  - resource: https://www.etsy.com/your/shops/me/marketplace-insights
    title: Etsy Marketplace Insights, 2026-08-07/08, LasercutSupplier bolt (Etsy Plus)
---

# Kereslet-mérés

**Mértékegység: `keresés / 1000 találat`** — hány havi keresés jut ezer versenyző listingre. Minél
magasabb, annál kevésbé telített a kifejezés.

**Minden mérés 2026 augusztusában készült.** Ez fontos: a trendszázalékok egymáshoz képest
összehasonlíthatók (ugyanaz az időszak), de az abszolút irány össze van keverve a szezonnal — nem
december van. Ezért jelent valamit, hogy a `christmas shadow box` **augusztusban** +9,3%.

**Zajküszöb:** nagyjából **300 havi keresés alatt a trendszázalék értelmezhetetlen**. A `layered svg`
napi görbéje 9 és 112 között ingadozik. Ne használd: `mandala shadow box` −100% (14 keresésből),
`paper cut svg` +266,7% (67-ből), `layered dog svg` +540% (51-ből), `layered wall art` +61,5% (195-ből).

## Metodikai megkülönböztetés: fájlszándék vs terméktartás

A kifejezések **két különböző vevőt** szolgálnak ki, és nem mérhetők össze:

- **Fájlszándék** — vágósablont keres (`layered svg`, `shadow box svg`, `dachshund svg`). Ez a mi
  piacunk.
- **Terméktartás** — kész fizikai terméket keres (`shadow box` 11 100 keresésének nagy része
  emléktárgy-dobozt jelent, nem sablont; ugyanígy `welcome sign`, `door hanger`, `nursery wall art`).

A `shadow box` 153,5-ös aránya ezért **nem a mi résünk**.

## A legjobb fájlszándékú kifejezések

| kifejezés | keresés | találat | ker./1000 | trend |
|---|---:|---:|---:|---:|
| **shadow box svg** | 2 600 | 34 400 | **75,6** | −7,0% |
| dog shadow box | 354 | 8 200 | 43,2 | −10,2% |
| mandala svg | 741 | 39 500 | 18,8 | −25,3% |
| 3d shadow box svg | 286 | 24 500 | 11,7 | −4,9% |
| **layered svg** (alapérték) | 1 200 | 189 900 | **6,3** | +11,1% |
| light box svg | 92 | 19 300 | 4,8 | −48,4% |
| papercut shadow box | 29 | 9 900 | 2,9 | −33,3% |
| paper cut svg | 67 | 568 700 | 0,12 | zaj |

A kínálati hiány a **`shadow box svg`** szón ül — tizenkétszerese az alapértéknek. A
`papercut shadow box` és a `light box svg` halott.

## Hosszú farok: fajták (fájlszándék)

| fajta | keresés | találat | ker./1000 | trend |
|---|---:|---:|---:|---:|
| dachshund svg | 514 | 11 200 | 45,9 | −22,4% |
| golden retriever svg | 434 | 11 400 | 38,1 | +9,8% |
| chihuahua svg | 218 | 5 900 | 36,9 | −27,5% |
| french bulldog svg | 208 | 8 800 | 23,6 | +2,0% |
| corgi svg | 199 | 16 900 | 11,8 | −6,5% |
| german shepherd svg | 130 | 8 000 | 16,3 | 0,0% |
| border collie svg | 132 | 15 500 | 8,5 | −37,3% |

**Medián: 208 keresés, 23,6 per 1000.** Mind a hét a legnépszerűbb harminc fajtából való.

### A hosszú farok mérlege

**Volumenben nyer.** Konzervatív extrapoláció: top 30 fajta × ~250 + a maradék ~170 × ~40 ≈
**14–16 ezer keresés/hó** a teljes fajtakészletre, szemben a `shadow box svg` 2 600-ával. Ez 5–6x, és
illeszkedik a [[findings/catalogue-size-and-throughput]] 100–300 listinges optimumához.

**Versenyben nem nyer.** Medián 23,6 per 1000 — négyszerese a `layered svg`-nek, de harmada a
`shadow box svg`-nek. A `dachshund svg`-n 11 200 listing verseng. Ezek telített mezők.

**És a kombinációt senki nem keresi:**

| kifejezés | keresés | találat | ker./1000 |
|---|---:|---:|---:|
| dog breed svg | 115 | 51 000 | 2,3 |
| layered dog svg | 51 | 9 600 | 5,3 |

## A fő következtetés

**A hosszú farkot nem kulcsszóval nyered meg, hanem thumbnaillel.**

„dachshund layered svg"-re nem lehet rankelni, mert nincs rá kereslet. A `dachshund svg`-re kell,
11 200 versenytárs között — ott viszont, ahol mindenki lapos fekete sziluettet mutat, **egy rétegzett
3D render vizuálisan kilóg**. A differenciálás vizuális, nem lexikai.

Ebből következik, hogy a [[workflows/production-pipeline]] Blender-render lépése **nem kényelmi
kérdés, hanem maga a versenyelőny** — oda kell a munka, nem a kulcsszókutatásba.

**Gyakorlati recept:** cím = bejáratott generikus kifejezés (`dachshund svg`) + `shadow box` +
gépkompatibilitás; kép = rétegzett 3D render. A keresést a kulcsszó hozza, a kattintást a látvány.

## Amit az egyszereplős kategóriákról megtudtunk

A [[findings/listing-craft]] felvetette, hogy az egyszereplős terméktípusok feltáratlan rést
jelenthetnek. **A válasz nagyrészt nemleges:** `wine bottle gift box` 2,3 és −50%, `mandala clock`
38,3 de −30%, `monogram wall art` 25,6 de −21,3%. Azért van egy bolt, mert **fogy a kereslet** — a
magas listingenkénti szám kis nevezőből jön.

Egy kivétel: **`christmas shadow box`** 258 keresés / 14 000 találat = 18,4, **+9,3% augusztusban** —
valódi szezon előtti emelkedés.

## Fenntartások

- Hét fajta mérve, mind a népszerű sávból. A ritkább 170 fajta volumene **becslés, nem mérés**.
- A „search results" minden illeszkedő listinget számol, tág kifejezéseknél felfelé torzít.
- Az augusztusi mérés a szezonálisan gyenge időszak; decemberi ismétlés más képet adhat.
