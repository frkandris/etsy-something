---
type: Method
title: Hogyan gyűjtöttük az adatot
description: Etsy keresés → bolt-populáció → bolt-adat → katalógus-mintavétel, mind Apify actorokon keresztül.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Adatgyűjtési folyamat

Négy lépés, mindegyik külön Apify futtatás. A nyers kimenetek az `assets/data/`-ban vannak, tehát
**újrafuttatás nélkül is minden újraszámolható**.

## 1. Populáció: Etsy keresés

`webdatalabs/etsy-scraper-pro` — keresőkifejezésenként 100 találat. Ez az egyetlen actor, ami
**egyszerre adja az akciós és az eredeti árat** (`price`, `originalPrice`, `onSale`), ezért erre épül
az egész kedvezmény-elemzés.

Layered: 5 keresés, 500 listing → 173 bolt. Funkcionális: 5 keresés, 500 listing → 285 bolt.

## 2. Szűrés specialistára

A bolt akkor kerül tovább, ha **legalább 3 különálló listinggel** rangsorolt (funkcionálisnál 2).
A „különálló" szó hangsúlyos — lásd [[pitfalls/2026-08-07-duplicate-search-hits]].

## 3. Bolt-adat

`getdataforme/etsy-shop-details-scraper` — `sold_count`, `create_date`, `active_listing_count`,
`average_rating`, `total_rating_count`, `country_code`, `is_open`. Egy futtatásban legfeljebb ~100
bolt; a 173-as populációhoz két futtatás kellett.

## 4. Katalógus-mintavétel

`hello.datawizards/etsy-shop-scraper` — boltonként 24 listing címe. Ebből számoljuk, hogy a bolt
katalógusának hány százaléka tartozik ténylegesen a niche-be. **Ez a lépés a legfontosabb**, és
kezdetben kimaradt; lásd [[pitfalls/2026-08-07-whole-shop-revenue-attribution]].

## Amit ez a folyamat szerkezetileg nem tud

- **Halandóságot** (a megszűnt boltok nem jelennek meg a keresési találatokban).
- **Keresési volument** (mennyien keresnek egy kifejezésre).
- **Aktuális futásteljesítményt** (csak élettartam-összesítést kapunk).
- **Az akciók időbeliségét** (egy pillanatfelvételt látunk, nem tudjuk, mióta tart az „akció").
