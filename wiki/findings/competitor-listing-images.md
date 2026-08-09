---
type: Finding
title: Versenytárs listing-képek — mit mutat a mezőny a thumbnailben és a galériában
description: "Kvalitatív képfelmérés 2026-08-08: a nagy volumenű eladók színes kartonrétegeket, fehér shadow-box keretet és lifestyle hátteret mutatnak; a fa-tónus a kisebbség."
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-08T22:00:00Z
sources:
  - resource: https://www.etsy.com/search?q=celtic+tree+of+life+layered+svg+shadow+box
    title: Keresési találati oldal + 3 megnyitott listing, 2026-08-08
---

# Versenytárs listing-képek

## Lényeg

A `celtic tree of life layered svg shadow box` keresés első ~16 találatát és 3 listing teljes
galériáját néztük végig böngészőből. A legfontosabb minta: **a nagy volumenű eladók nem
fa-tónusú lézeres renderrel adnak el, hanem színes kartonrétegekkel, fehér shadow-box keretben,
lifestyle háttérrel** — és a vevői review-fotók igazolják, hogy a vevők tényleg Cricuttal,
kartonból vágják ki.

## Populáció

Kvalitatív minta: 1 keresési oldal (~16 találat) + 3 listing-galéria végiglapozva 2026-08-08-án.
Nem reprezentatív mérés — irányjelző a saját képkészletünkhöz.

## Megfigyelések listingenként

| bolt | listing review | jel | képrecept |
|---|---:|---|---|
| **UpSVGStudio** | **bolt** 390 review / 6k eladás / 2 év (a listingen csak **7** review) | erős bolt-szintű jel, listing-szintű nem | színes karton (krém/pink/magenta/arany), **fehér shadow-box keret**, bokeh lifestyle háttér; a vevői review-fotó (Cricut, karton) gyakorlatilag megegyezik a renderrel |
| **LaserLee** (lightbox) | bolt 2,6k★ | Star Seller | hero szöveg-overlay-jel (formátumlista + „MATERIAL 1/8 in (3.2 mm) - 2 SIZES"), videó, **meleg fényfüzérrel megvilágított** közeli, flat-lay „mit vágsz ki" tábla |
| **ColorLayerArt** (bundle) | bolt 2,6k★ | Star Seller | 8 variáns egy hero-n, **sötét (éjszakai) hátsó réteg** + arany/fa tónusok + szelektív zöld lomb; bundle-ökre pozicionál |
| VyvaStudioDigital | bolt 2k★ | — | photoreal fa-tónusú render komódon állítva, lakás-környezet |

A keresőoldalon a színes (teal/piros/arany, pink/magenta) hero-k vizuálisan dominálnak a
fa-tónusúak felett; a mi jelenlegi render_hero-nk (egyszínű natúr fa, szürke háttér) a mezőny
leghalványabb kvartilisébe esne.

## Következmények a saját listingre

1. **Színes rétegváltozat kell** a fa-tónus mellé — a rétegfájl ugyanaz, csak a render
   palettája más. A Cricut/karton vevőkör a címelemzés szerint is jelen van
   ([[findings/listing-craft]]: Cricut 28%).
2. **Fehér shadow-box keret + lifestyle háttér** a hero-n; a steril szürke stúdió-háttér nem
   versenyképes.
3. **Szöveg-overlay a hero-n**: formátumok (SVG/DXF/PDF), rétegszám, méret — a mezőny
   következetesen ráírja.
4. **Sötét hátsó réteg** trükk: a legfelső rétegek akkor olvashatók, ha a legalsó kontrasztot ad
   (ColorLayerArt éjszakai égboltja). A mi 1. rétegünk jelenleg ugyanolyan tónusú, mint a többi.
5. Galéria-szerkezet: hero → videó → közeli → flat-lay rétegtábla → „what you get" → köszönőkártya.

## Kiegészítés — tacskó és celtic knot felmérés (2026-08-09 éjjel)

| bolt | jel | recept |
|---|---|---|
| **MagicVectorLaser** | bolt 5k★ | kutyafajta-BUNDLE (34 fej egy hero-n), fa tónus |
| **StudioTokanoLayerSVG** | bolt 1,5k★ | keretezett színes karton tacskó-portré, „7 layers" badge, szöveg-overlay |
| **Namlaserart** | bolt 761★ | portré-rács keretekben, barna monokróm |
| **MaWoodCreationStore** | bolt 1k★ / 9,7k eladás | négyzetes trinity-knot mandala, fekete+fehér+piros, fonott szegély; review-fotók igazolják a vágást |

Következmény: mindkét új témánk (0007–0012 iterációk) a fenti recepteket követi — négyzetes
formátum, tömör hátlap sötét kontraszttal, fajtaszínű vagy MaWood-kontrasztú paletta, polcos
lifestyle render (--grain + shelf nézet a render_blender.py-ban).

## Fenntartások

Kis, kvalitatív minta; a review-számok bolti szintűek (az UpSVGStudio 390-e is BOLT-szintű: a konkrét listingen 7 review van — 2026-08-09-i javítás).
A színes vs fa-tónus preferenciát eladási adat nem, csak a review-fotók és a review-számok
támasztják alá.

## Provenancia

Böngészős bejárás 2026-08-08, screenshotok a session transcriptben. Kapcsolódik:
[[findings/review-mining]] (mit vágnak ki ténylegesen), [[findings/listing-craft]] (címek),
[[workflows/production-pipeline]].
