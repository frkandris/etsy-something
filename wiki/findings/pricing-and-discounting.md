---
type: Finding
title: Árazás és tartós kedvezmény — a legerősebb jelzés az adatban
description: Aki nem akciózik, kétszer annyit keres listingenként; és minden magasabb ársáv veri az alatta lévőt.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/layered_adjusted.json
    id: clean
    title: 65 specialista, ebből 33 igazolt
---

# Árazás és tartós kedvezmény

## Lényeg

A **tartós kedvezmény nem növekedési eszköz, hanem a commodity-pozíció tünete**, és **az ár monoton
együtt jár az eredménnyel**. Ez a két összefüggés minden populációszűrést és a katalógus-korrekciót is
túlélte — ez a legmegbízhatóbb következtetés az egész kutatásból.

## Populáció

33 **igazolt** bolt (katalógusuk ≥80%-a layered). A bevétel katalógus-aránnyal korrigált.

## Kedvezmény vs eredmény

| tartós kedvezmény | boltok | medián HUF/hó | HUF/listing | medián ár |
|---|---:|---:|---:|---:|
| **nincs** | 6 | **575 060** | **4 108** | $8,50 |
| <35% | 8 | 350 743 | 1 239 | $6,17 |
| 35–55% | 14 | 284 190 | 1 207 | $4,97 |
| 55%+ | 5 | 282 369 | 1 396 | $3,20 |

A nem akciózó boltok listingenként **3,3-szor** annyit hoznak, mint a mély diszkontálók.

## Ár vs eredmény

| ársáv | boltok | medián HUF/hó | HUF/listing | medián listing |
|---|---:|---:|---:|---:|
| <$4 | 7 | 163 316 | 1 396 | 169 |
| $4–7 | 15 | 284 592 | 1 174 | 207 |
| $7–12 | 7 | 315 434 | 1 415 | 274 |
| **$12+** | 4 | **842 651** | **7 365** | 236 |

Figyelemre méltó: a $12+ sáv **nem** kevesebb listinggel éri el ezt — a katalógusméret mediánja
gyakorlatilag ugyanaz. A magasabb ár tehát nem kevesebb eladást jelentett ebben a mintában.

## Piaci norma, amivel szemben ez áll

A teljes 173-as populációban: medián eladási ár **$4,79**, medián listaár **$7,23**, medián tartós
kedvezmény **40%**, és a boltok **75%-a** akciózik. Vagyis a nem akciózás kisebbségi, nem többségi
viselkedés — a javasolt pozíció szándékosan szembemegy a norma többségével.

## Fontos: ez korreláció, nem ok-okozat

Nagyon valószínű, hogy **nem az akció hiánya okozza az eredményt**, hanem a jobb, jobban
differenciált termék teszi lehetővé, hogy ne kelljen akciózni. A gyakorlati tanulság iránya ettől nem
változik — a termékből kell kiindulni, nem az árazási trükkből —, de ne várd, hogy az akció
kikapcsolása önmagában megemeli a bevételt.

## Fenntartások

- Kis minták: 6 nem akciózó bolt, 4 bolt a $12+ sávban. Az irány konzisztens, pontbecslésként ne kezeld.
- A kedvezmény a keresési találatok `price` / `originalPrice` mezőiből jön, boltonként mediánolva —
  boltonként néhány listing mintája, nem a teljes katalógusé.
- A SalesDoe-alapú régi táblában ugyanez a torzítás okozott hibát, lásd
  [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]].

## Provenancia

`assets/scripts/layered_deep.py`, 2. és 3. szakasz.
