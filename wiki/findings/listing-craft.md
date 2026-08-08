---
type: Finding
title: Mit írnak a listing címekbe — gépek, formátumok, rétegszám, témák
description: 777 listing címének elemzése az igazolt boltoktól: 85% említ lézert, 94% SVG-t, a medián rétegszám 7, és a bundle csak 4%.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/catalog_sample.json
    title: 1543 mintavett listing, ebből 777 az igazolt boltoktól
---

# Listing-készítés: mit tartalmaznak a címek

## Populáció

**777 listing** a 33 **igazolt** bolt saját katalógusából (boltonként max. 24 tétel mintavéve
2026-08-07-én).

## Gép- és szoftverkompatibilitás a címben

| említés | listing | arány |
|---|---:|---:|
| lézer általában | 664 | 85% |
| CNC router | 277 | 36% |
| Cricut | 218 | 28% |
| Glowforge | 178 | 23% |
| LightBurn | 28 | 4% |
| xTool | 21 | 3% |
| Silhouette | 27 | 3% |

**Tanulság:** a cím nem egy gépet céloz, hanem többet egyszerre. A `Cricut` (28%) azért fontos, mert
az papírvágós közönség — vagyis ugyanaz a fájl két külön vevőkört szolgál ki, és a legtöbb bolt ezt ki
is használja a címben.

## Fájlformátumok

| formátum | listing | arány |
|---|---:|---:|
| SVG | 734 | 94% |
| DXF | 196 | 25% |
| PDF | 47 | 6% |
| PNG | 44 | 6% |
| AI | 42 | 5% |
| EPS | 11 | 1% |
| CDR / LBRN | 3 / 1 | ~0% |

Az **SVG + DXF** páros a de facto szállítási minimum. A CDR és a LightBurn-natív `.lbrn` gyakorlatilag
nincs jelen — ez elvi differenciálási lehetőség, de nincs rá kereslet-bizonyítékunk.

## Rétegszám

54 listing írja ki a rétegszámot a címbe, **medián 7 réteg**. Eloszlás:

| réteg | 3 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| listing | 2 | 8 | 9 | 11 | 11 | 4 | 4 | 4 | 1 |

A 9+ rétegű tartomány ritka (13 listing), és a felső árszegmens boltjainál fordul elő
([[shops/beameez]] 9 réteg, Arqovia 14 réteg, DIYMakerDesigns 10 réteg / 700×700 mm). Ez a
differenciálás egyik kézzelfogható tengelye: **több réteg és nagyobb méret**.

## Témák

| téma | listing | arány |
|---|---:|---:|
| ember / portré | 324 | 42% |
| mandala / ornamens | 313 | 40% |
| állat | 227 | 29% |
| természet / növény | 129 | 17% |
| vallási | 94 | 12% |
| ünnep / szezon | 86 | 11% |
| jármű | 36 | 5% |
| fantasy / pop | 24 | 3% |

(Az arányok összege 100% felett van, mert egy cím több témát is érinthet.)

## Bundle vs egyedi

Csak **29 listing (4%)** bundle/pack. A bundle medián ára **$8,80**, az egyedié **$4,80** — vagyis a
csomagolás nagyjából megduplázza a jegyárat, és a mezőny alig használja. Ez a legolcsóbban kihasználható
rés az adatban.

## Commercial licence

Mindössze **6 listing (1%)** említi. Az a **2 bolt**, amelyik igen, mediánban **728 965 HUF/hó**-t és
**6 544 HUF/listing**-et hoz, szemben a másik 31 bolt 315 434-es és 1 415-ös értékével.

Óvatosan: két bolt, és mindkettő amúgy is a felső mezőnyben van, tehát ez ugyanaz az összefüggés, mint
a nem akciózásnál — valószínűleg mindkettő a „komolyabb termék" tünete, nem az oka. De ez a leginkább
kihasználatlan pozicionálási elem az egész mintában.

## Provenancia

`assets/scripts/layered_deep.py` 8–13. szakasz.
