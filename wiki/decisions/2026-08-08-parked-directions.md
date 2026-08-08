---
type: Decision
title: Elnapolt irányok — termék-vetületek és review-bányászat
description: Négy irány, amit a felhasználó megjelölt, de a kulcsszókutatás befejezése utánra halasztott.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T09:30:00Z
---

# Elnapolt irányok — **LEZÁRVA 2026-08-08**

Mindhárom termék-vetület megmérve a meglévő review-adaton
(`assets/scripts/product_projections.py`), a review-bányászat pedig elkészült.
Eredmény egy táblában:

| irány | review | különböző listing | kínálat a 33 boltnál | index | döntés |
|---|---:|---:|---:|---:|---|
| ~~mécses / lámpás~~ | 29 | 16 | 1 | ~14 | **VISSZAVONVA** — 2 eladó, 23/29 egyetlen boltból |
| ajándékdoboz | 32 | 15 | 11 | 1,43 | később |
| sík print | **0** | **0** | 0 | — | **elvetve** |

Részletek: [[findings/review-mining]] és lentebb.

**Dátum:** 2026-08-08 · **Döntő:** a felhasználó · **Státusz:** várólistán, nem elvetve

A kulcsszó-adatbázis ([[findings/keyword-database]]) befejezése és elemzése után ezekkel kell
foglalkozni. Azért van rögzítve, hogy ne a beszélgetésben vesszen el.

## 1. A rétegzett minta termék-vetületei

Ugyanaz a rétegzett geometria több végtermékben is felhasználható, és ezek **külön keresési piacok**,
külön kulcsszavakkal:

- **sík minta kinyomtatva a falra — ELVETVE.** A layered boltok 1 581 review-jából és 777
  katalógustételéből **nulla** ilyen. Ami „print" néven előjött, az más boltoktól való és nem
  rétegzett (DTF holló-design, utazóposzterek, botanikus printek). Független ellenérv a
  [[findings/keyword-database]]-ből: `printable art` 8 700 keresés / 3,3M találat = **2,6 per 1000**,
  `digital download art` = 3,0 — a teljes 345-ös adatbázis legrosszabb arányai közt.
- **ajándékdoboz oldala — KÉSŐBB.** Index 1,43 (32 review / 15 listing). A tételek gyakorlatilag
  mind a [[shops/laserartisandesigns]]-tól valók (bor-ajándékdoboz 8x, ékszerdoboz 3x, mindkettő
  `Commercial Licence` bundle-lel). A norse/kelta boltoknál más műfaj (kockatartó, gyűrűsdoboz).
  Ellenérv: a funkcionális szegmens kínálatában **már 205 doboz-listing van (12%)** — nem üres
  piac; a LaserArtisanDesigns a licencmodelltől teljesít jól, nem a hiánytól.
- **rétegelt lámpa — IGAZOLVA, ez a legerősebb termékforma-hiány.** 29 review **16 különböző
  listingen**, miközben az igazolt boltok katalógusában **egy** ilyen tétel van — **de a 29 review 2 eladótól jön, 23 egyetlen boltból**, ezért az irány visszavonva. A funkcionális
  szegmens kínálatában viszont 97 tealight/lantern listing (5,7%) — vagyis működő piac, amit a
  rétegzett boltok nem szolgálnak ki. **A korábbi óvatosságom téves volt:** a `light box svg`
  gyenge kulcsszava (4,8 / −48,4%) félrevezetett — a piac `tealight` / `candle holder` /
  `lantern` / `night lamp` néven veszi, és jellemzően **csomagban** (3x, 8x, 10x, 54x pack).

**Miért érdekes:** egy elkészült rétegterv többféle terméklistinget táplálhat, vagyis a
designonkénti 20–40 perc ([[workflows/production-pipeline]]) több bevételi csatornára oszlik.

## 2. Review-bányászat: mi fogy ténylegesen — **KÉSZ 2026-08-08**, lásd [[findings/review-mining]]

A boltok **review oldalaiból** kiolvasható, hogy melyik konkrét listingek kapnak értékelést, és
milyen ütemben. Ez lényegesen jobb jel, mint bármi, amit eddig mértünk:

- a jelenlegi bevételbecslésünk **bolt-szintű és élettartam-átlag**
  ([[methods/revenue-estimation-method]]),
- a review-k viszont **listing-szintűek és dátumozottak**, tehát megmutatják, mi fogy *most*.

Ezzel a [[findings/keyword-database]] keresleti oldala összeköthető a tényleges eladással: nem csak
azt tudnánk, mit keresnek, hanem azt is, mit vesznek meg.

Apify oldalról van rá kész actor (`hello.datawizards/etsy-reviews`, `easyapi/etsy-reviews-scraper`) —
lásd [[methods/apify-actors]].

## A lezárás utáni sorrend

1. **Kereszt + mandala + zászló kombók** — a legszélesebb bizonyított kereslet (index 3,41, 44
   különböző listing).
2. ~~Mécses / lámpás csomagok~~ — **visszavonva**: a jel 2 eladótól jön (23/29 a YarensWoodDream
   boltból), tehát egy katalógus, nem piaci rés.
   Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].
3. **Ajándékdoboz commercial licence-szel** — csak ha az első kettő megy.
4. ~~Sík print~~ — elvetve.
