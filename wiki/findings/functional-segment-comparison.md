---
type: Finding
title: A funkcionális szegmens (doboz, urna, keret) összehasonlítva
description: Külön felmérve 285 bolt: statisztikailag gyakorlatilag azonos a layereddel, tehát a váltás nem indokolt.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/fn_shops.json
    title: 285 bolt 5 keresésből
  - resource: /assets/data/fn_catalog.json
    title: 1711 mintavett listing 73 bolttól
---

# Funkcionális szegmens vs layered

> **AUDIT 2026-08-08 UTÁN.** A táblázat **kevert alapon** áll: a bevétel-medián sor katalógussal
> korrigált, a HUF/listing, a méreteloszlás és a belépési arány viszont **nyers, teljes bolti** érték.
> Egységesen korrigálva: HUF/listing 793 / 788 (nem 1 353 / 1 789), >1M 8% / 12% (nem 18% / 19%),
> <200k 55% / 59% (nem 38% / 38%). A fő következtetés — **a két szegmens gyakorlatilag azonos** —
> ettől nem változik. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

## Miért mértük meg

Egy javaslat elhangzott, hogy érdemes lenne layered fali dekor helyett **funkcionális lézervágott
tárgyakra** (ajándékdoboz, urna, képkeret, tartó) váltani — de az a javaslat egyetlen bolt
kategórialistájából jött, felmérés nélkül. A [[decisions/2026-08-07-pursue-layered]] döntés
előfeltétele volt, hogy ezt a szegmenst rendesen felmérjük.

## Populáció

Öt keresés 2026-08-07-én (`laser cut box svg file`, `wooden gift box laser cut file`,
`laser cut picture frame svg`, `laser cut urn svg file`, `commercial licence laser cut files`),
500 listing → **285 bolt**. Ebből **73** rangsorolt legalább 2 különálló listinggel; ezekre
katalógus-mintavétel is futott (1711 listing).

## Az összehasonlítás

| | layered | funkcionális |
|---|---:|---:|
| bolt 500 listingből | 173 | **285** |
| szakosodott | 65 | 73 |
| medián eladási ár | $5,10 | $4,00 |
| medián tartós kedvezmény | 30% | 30% |
| medián listing | 249 | 167 |
| medián bevétel (nyers) | 321 653 | 323 317 |
| medián bevétel (katalógussal korrigált) | 144 939 | 138 388 |
| medián HUF/listing | 1 353 | 1 789 |
| >1M HUF/hó | 18% | 19% |
| <200k | 38% | 38% |
| belépési esély (<3 év, 500k+) | 19% | 24% |

**Következtetés: a két szegmens statisztikailag gyakorlatilag azonos.** A funkcionális oldal
szétaprózottabb (285 vs 173 bolt ugyanannyi listingre) és valamivel olcsóbb, de a méreteloszlás és a
belépési esély gyakorlatilag megegyezik.

## Amit viszont megerősít

A katalógus-mintavétel szerint a **medián funkcionális arány 58%, a medián layered arány 0%** — a két
szegmens tehát tényleg elkülönül, nem ugyanazokat a boltokat mértük kétszer.

És ugyanaz a pozicionálási minta jött ki függetlenül: a listingenkénti élmezőnyben
**Vasily39** (CZ, 287 listing, $8,46, **0% akció**, 9 019 HUF/listing) és
[[shops/laserartisandesigns]] (GB, 72 listing, $42,31, **0% akció**, 21 692 HUF/listing) — miközben a
2 500–2 900 listinges izraeli óriások 800–900 HUF/listinget hoznak.

## Fenntartás

A kategorizálás **címszavas** 24 listing mintán: egy „Wedding Card Box SVG" beleszámít, egy „Keepsake
Chest" nem, mert nincs benne kulcsszó. A nagyságrend jó, a századok nem.

## Provenancia

`assets/scripts/compare.py`, `assets/scripts/gen_fn_script.py`.
