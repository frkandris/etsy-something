---
type: Workflow
title: Norse / kelta / tree of life katalógusterv
description: VISSZAVONT katalogusterv - a review-adat szerint a norse/kelta kereslet gravirozast akar, nem retegzett falidiszt.
status: deprecated
generated:
  by: claude-opus-5
  at: 2026-08-08T10:30:00Z
sources:
  - resource: /assets/data/keywords/norse_celtic_complex.json
    title: a komplexum 88 kulcsszava mérési adattal
---

# Norse / kelta / tree of life katalógusterv

> **VISSZAVONVA 2026-08-08.** A review-mérés megmutatta, hogy a norse/kelta keresések mögötti
> szándék **gravírozás és tárgy** (coaster, könyvjelző, érme, puzzle), nem rétegzett falidísz: a
> témában rangsoroló 16 bolt 609 review-jából mindössze **2,8% rétegzett**, 58,8% gravírozó/tárgy.
> Lásd [[findings/review-mining]]. Az oldal dokumentációként marad meg.

## Miért ez a téma

88 kulcsszó, **22 535 keresés/hó**, medián kínálat ~7 000 listing kulcsszavanként — a mandala
39 500-ának és a virágos 363 400-ának töredéke. És egy formanyelv fedi le mindet: csomózás, rúna,
mitológia. A kelta csomózás ráadásul **természeténél fogva rétegzett**, tehát a multilayer forma a
motívum sajátja, nem ráerőltetés.

## A designlista

Egy design több kulcsszót is céloz, ezért a 88 kulcsszó **~18 rajzot** jelent, nem 88-at.

### Első kör — a legjobb arányúak (10 design)

| # | design | célkulcsszavak | keresés | kínálat |
|---|---|---|---:|---:|
| 1 | **viking sisak** | `viking helmet svg` (109,4) | 197 | **1 800** |
| 2 | **Yggdrasil / világfa** | `yggdrasil` (90,8), `tree of life svg` (26,0), `tree of life dxf` (18,7) | 1 311 | 7,1–20,5k |
| 3 | **kelta csomó** | `celtic knot svg` (17,0), `celtic knot stencil` (15,8), `celtic knot wall art` (55,3) | 559 | 5,2–9,2k |
| 4 | **hosszúhajó** | `viking ship svg` (16,6) | 96 | 5 800 |
| 5 | **Mjölnir / Thor** | `thor svg` (14,0), `thor hammer svg` (6,1) | 128 | 5,6–6,7k |
| 6 | **kelta kereszt** | `celtic cross svg` (10,0) | 71 | 7 100 |
| 7 | **sacred geometry** | `sacred geometry svg` (11,3) | 78 | 6 900 |
| 8 | **walesi sárkány** | `welsh dragon svg` (9,4) | 30 | 3 200 |
| 9 | **Odin** | `odin svg` (9,2) | 22 | 2 400 |
| 10 | **Claddagh** | `claddagh svg` (8,0) | 39 | 4 900 |

### Második kör (8 design)

Fenrir/farkas (`viking wolf svg` 6,3) · viking fejsze (`viking axe svg` 7,2,
`viking axe stencil` 4,8) · Vegvísir/iránytű (`viking compass svg` 3,8) · rúnasor
(`viking runes svg` 6,5) · Valhalla (`valhalla svg` 4,8) · pajzs (`shield svg` 2,8) ·
tree of life mandala változat (`tree of life mandala` 10,0) · skandináv folk minta
(`nordic folk art` 6,6, `scandinavian svg` 4,7).

## Címzés

A [[findings/keyword-demand-sweep]] tanulsága szerint **a vevő nem gépeli be a terméktípust a témával
együtt**. Tehát a cím a bejáratott generikus kifejezésre épül, és a terméktípus mögé kerül:

```
Viking Helmet SVG, Multilayer Shadow Box File, Laser Cut DXF for Glowforge & Cricut
```

Elöl a keresett kifejezés (`viking helmet svg`), utána a `shadow box` (a legjobb fájlszándékú
terméktípus, 75,6), végül a gépkompatibilitás ([[findings/listing-craft]]: 85% lézer, 36% CNC,
28% Cricut, 23% Glowforge).

## Ami eldönti, hogy működik-e

**A thumbnail, nem a kulcsszó.** A `viking helmet svg` 1 800 versenyző listingje között egy rétegzett
3D render vizuálisan kilóg a lapos sziluettek közül. A
[[workflows/production-pipeline]] Blender-render lépése ezért itt a versenyelőny, nem kényelmi kérdés.

## Nyitott kérdés, mielőtt ez élesbe megy

**Fogy-e ebből ténylegesen valami, vagy csak keresik?** A kereslet mért, az eladás nem. Ezt a
[[decisions/2026-08-08-parked-directions]] review-bányászata tudná megmondani: a konkrét listingek
értékeléseinek dátumaiból kiderül, mi kel el *most*. Ezt érdemes megcsinálni, mielőtt 18 design
legyártásába kezdenél.

## Fenntartások

- A kulcsszavak nagy része **kis volumenű** (20–200 keresés/hó). Az érték az aggregátumban van, nem
  egyetlen kifejezésben — vagyis ez csak akkor működik, ha a teljes 18 designos katalógus elkészül.
- A `viking svg` trendje −31,4%, a `celtic svg`-é +7,5% — a téma iránya nem eldöntött, és mindkét
  minta kicsi.
- Minden mérés 2026 augusztusából.
