---
type: Finding
title: Földrajz — kivel versenyzel, és hol van a rés
description: A 33 igazolt boltból 15 ukrán; a négy közép-/nyugat-európai bolt viszont 2,6-szor annyit hoz listingenként, magasabb áron és nulla akcióval.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/layered_adjusted.json
    title: 33 igazolt bolt országkóddal
---

# Földrajz és költségverseny

> **AUDIT 2026-08-08 UTÁN.** Dedupolva az **európai csoport 4-ről 2 boltra esik**, tehát az oldal fő
> összehasonlítása (743 ezer vs 285 ezer HUF/hó) **nem használható**. A dedupolt értékek: Európa n=2,
> medián 936 269 HUF/hó és 3 337 HUF/listing; alacsony költségű ország n=16, 423 783 és 1 460. Az
> irány ugyanaz maradt, de **két bolt nem bizonyíték**. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

## Lényeg

A niche-t alacsony költségű országok uralják, de **nem ők a legjobb gazdaságosságúak**. A néhány
európai szereplő kevesebb listinggel, magasabb áron, akció nélkül működik — és listingenként
többszörösét hozza. Ez a rés, ahová magyar szereplőként be lehet állni.

## Populáció

33 **igazolt** bolt (katalógus ≥80% layered).

## Országok

| ország | boltok |
|---|---:|
| Ukrajna | 15 |
| Törökország | 3 |
| Vietnám | 3 |
| Indonézia | 2 |
| Grúzia, Új-Zéland, Németország, Ausztrália, Argentína, ismeretlen | 1–1 |

## A két csoport összehasonlítva

| | Európa (nyugat/közép) | alacsony költségű ország |
|---|---:|---:|
| boltok | 4 | 23 |
| medián HUF/hó | **742 564** | 284 592 |
| HUF/listing | **3 629** | 1 240 |
| medián ár | **$11,33** | $4,65 |
| medián kedvezmény | **0%** | 40% |

Az európai csoport mediánja listingenként **2,9-szerese** a másikénak, és a különbség teljes egészében
az ár- és akciópolitikában van, nem a katalógusméretben.

## Miért nem lehet ezt egyszerűen lemásolni a másik irányból

Az alacsony költségű stúdiók termelési tempója havi 20–80 listing (lásd
[[findings/catalogue-size-and-throughput]]). Ezt európai költségszinten nem lehet kitermelni. Fordítva
viszont igaz: a magas ár + akciómentesség pozíciót nem a költségszint akadályozza, hanem az, hogy jobb
és differenciáltabb terméket kell hozzá csinálni.

## Fenntartás

**Négy bolt.** Ez a legkisebb minta, amiből a wiki bármit állít, és a legóvatosabban kezelendő
következtetés. Az irányt megerősíti, hogy a funkcionális szegmensben ugyanez a minta jött ki
függetlenül (Vasily39 CZ, LaserArtisanDesigns GB — lásd
[[findings/functional-segment-comparison]]), de két különálló négy-elemű megfigyelés még mindig nem
bizonyíték.

Az „ország" az Etsy bolt-adatában szereplő `country_code`, ami a **regisztráció** helye — nem
feltétlenül az, hol dolgozik ténylegesen a csapat.

## Provenancia

`assets/scripts/layered_deep.py` 6. szakasz.
