---
type: Pitfall
title: Rossz függetlenségi egység — kétszer, ugyanabban a projektben
description: A specialista-szűrő sorokat számolt listingek helyett, a review-jelek listingeket számoltak eladók helyett; mindkettő a már dokumentált Beameez-hiba ismétlése.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T16:00:00Z
sources:
  - resource: /assets/scripts/rebuild_corrected.py
    title: a javított újraszámolás
---

# Rossz függetlenségi egység

**Dátum:** 2026-08-08 · **Hogyan derült ki:** külső codex-audit · **Súlyosság:** a fő
következtetések többségét érintette

## Tünet

Két állítás, amit erős bizonyítéknak neveztem:

1. „**65 specialista** bolt, ebből **33 igazolt**" — az egész kutatás populációja.
2. „A mécses/lámpás jel **nem egyszereplős torzítás — 7–14 különböző listing** mindegyiknél."

Mindkettő hibás.

## Gyökérok

**Mindkét esetben rossz egységben mértem a függetlenséget.**

**(1) A specialista-szűrő a keresési találatok *sorait* számolta, nem a különálló listingeket.** Az öt
keresés átfedő halmazokat ad vissza, tehát ugyanaz a listing háromszor is beszámított. Pontosan ez a
[[pitfalls/2026-08-07-duplicate-search-hits]] hibája — amit **dokumentáltam**, de csak a funkcionális
szegmens pipeline-jában javítottam ki, a layeredben nem.

| | hibás | dedupolva |
|---|---:|---:|
| specialista (≥3 találat) | 65 | **35** |
| igazolt (≥80% layered) | 33 | **21** |
| medián korrigált bevétel | 320 156 | **416 893** |

**(2) A review-jeleknél különálló *listingeket* számoltam, nem különálló *eladókat*.** Egy bolt tíz
listingje nem tíz független piaci megfigyelés.

| jel | review | listing | **eladó** | legnagyobb eladó részesedése |
|---|---:|---:|---:|---|
| mécses / lámpás | 29 | 16 | **2** | **23/29 (YarensWoodDream)** |
| suncatcher | 14 | 7 | **1** | 14/14 (PetalSmith3D) |
| mirror | 12 | 3 | **2** | 11/12 (MultiLayerArts) |
| ajándékdoboz | 30 | 13 | **1** | 30/30 (LaserArtisanDesigns) |
| kereszt | 104 | 44 | **13** | 39/104 |
| hazafias | 100 | 57 | **14** | 17/100 |
| cow / western | 49 | 35 | **16** | 14/49 |
| koponya | 26 | 22 | **13** | 5/26 |

## Mit döntött el

**A mécses/lámpás ajánlás megbukott.** Egy eladó katalógusát neveztem piaci résnek. Ugyanígy a
suncatcher, a mirror és az ajándékdoboz.

**A kereszt / hazafias / western / koponya irány megmaradt** — 13–16 különböző eladó, a legnagyobb
sem visz többet a harmadánál. Ez a szűrő tehát nem mindent tüntetett el, hanem **szétválasztotta a
valódi jelet az egyszereplős műtermékektől**.

## Ami emiatt még dőlt

A dedupolt populáción a korábbi fő eredmények sem tartják magukat:

- **„Ne akciózz"** — a nem akciózó csoport 6-ról **3 boltra** esett, és a kedvezmény-sávok
  eredménye már **nem monoton**: nincs akció **2 093**, <35% 1 035, 35–55% 1 583, 55%+ 1 767
  HUF/listing. A legmagasabb továbbra is a nem akciózó csoport — de **3 bolton**, és a sorrend
  közben megtörik, tehát következtetést nem hordoz.
  Lásd [[findings/pricing-and-discounting]].
- **„Az ár monoton együtt jár az eredménnyel"** — a HUF/listing dedupolva **csökken** az árral
  (1 720 → 1 581 → 1 338 → 817), és a $12+ sávban **egy** bolt maradt.
- **Az európai klaszter** 4-ről **2 boltra** esett — nem használható.

## Tanulság

**Minden aggregált jelnél ki kell mondani, mi a független megfigyelési egység, és aszerint kell
számolni.** Nem elég „több adatpont van" — meg kell nézni, hány *egymástól független* forrásból
jönnek.

Gyakorlati szabály ehhez a projekthez: **minden bolt-szintű állítás mellé az eladók száma és a
legnagyobb eladó részesedése**; minden keresésből épített populációnál **deduplikált** listingszám.

Ez a hiba **kétszer** fordult elő, a második alkalommal azután, hogy az elsőt már postmortembe
írtam. A dokumentálás önmagában nem véd — a szűrőt a *meglévő* elemzésekre is vissza kell vezetni,
nem csak az ezután készülőkre.
