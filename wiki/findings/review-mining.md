---
type: Finding
title: Review-bányászat — mi fogy ténylegesen
description: 2190 review; a norse/kelta gravirozast akar, nem retegzett falidiszt. Az itteni szamok a hibas 33-as populacion keszultek - a 21 boltos ujraszamolas a lap tetejen.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T12:00:00Z
sources:
  - resource: /assets/data/reviews.json
    title: 1581 review a 33 igazolt layered bolttól, 2025-04-29 – 2026-08-08
  - resource: /assets/data/nc_reviews.json
    title: 609 review 16 norse/kelta boltról, 2023-09-20 – 2026-08-08
---

# Review-bányászat

> **AUDIT 2026-08-08 UTÁN — 2. kör.** Az alábbi számok a **hibás 33-as populáción** és
> **deduplikálatlan** review-kon készültek (36 duplikált sor volt bennük). A **21 igazolt** bolt
> **1 027 deduplikált** review-ján újraszámolva: kereszt **57 review / 34 listing / 8 eladó**,
> hazafias **68 / 35 / 10**, western-farm **28 / 19 / 10**, koponya **18 / 14 / 8**,
> óra **11 / 8 / 3**, mirror **1 / 1 / 1**. Az irány (kereszt–hazafias–western–koponya, több
> eladóval) áll; a konkrét számok az alább közölteknél kisebbek.
>
> **AUDIT 2026-08-08 UTÁN — 1. kör.** A **mécses/lámpás, suncatcher, mirror és ajándékdoboz ajánlás visszavonva**:
> ezek egy-két eladó katalógusai (tealight 23/29 és lantern 23/23 ugyanattól a YarensWoodDream
> bolttól, suncatcher 14/14 PetalSmith3D, ajándékdoboz 30/30 LaserArtisanDesigns). Különálló
> **listingeket** számoltam különálló **eladók** helyett. Ami megmaradt, mert 13–16 eladó adja:
> **kereszt** (104 review / 13 eladó), **hazafias** (100 / 14), **western-farm** (49 / 16),
> **koponya** (26 / 13). Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

## Miért ez a legjobb jelünk

Minden korábbi mérésünk **kereslet** (keresés) vagy **kínálat** (listing). A review az egyetlen
adat, ami **tényleges eladáshoz** kötődik, és ráadásul **listing-szintű és dátumozott** — szemben a
bolt-szintű, élettartam-átlagos bevételbecsléssel ([[methods/revenue-estimation-method]]).

Egy review alsó becslés az eladásra (nem mindenki értékel), de a motívumok **egymáshoz viszonyított
aránya** ettől még használható.

Actor: `hello.datawizards/etsy-reviews`, boltnevek tömbje + `itemLimit`. Ad `listing_title`,
`date`, `product_rating`, `product_url`. Költség ~0,0057 USD/review.

## 1. Kínálat vs tényleges eladás a 33 igazolt layered boltban

1 581 review, 1 041 különböző listing. A „listing %" a katalógus-mintából
([[findings/listing-craft]]), a „review %" ugyanezen boltok eladásaiból.

| motívum | listing % | review % | **index** |
|---|---:|---:|---:|
| **hazafias** | 0,8% | 1,5% | **1,88** |
| **ember / portré** | 1,0% | 1,6% | **1,60** |
| jármű / gép | 1,5% | 2,2% | 1,39 |
| egyéb | 17,5% | 19,2% | 1,10 |
| természet / fa | 4,2% | 4,5% | 1,06 |
| **mandala / zentangle** | 39,6% | 40,4% | **1,02** |
| vallási | 5,9% | 5,5% | 0,93 |
| állat | 21,9% | 20,2% | 0,92 |
| **virágos** | 5,4% | 3,4% | **0,63** |

**Index > 1,4 = alulkínált** (többet vesznek belőle, mint amennyit listáznak), **< 0,7 = túlkínált**.

### A mandaláról tévedtünk

A [[findings/keyword-database]] alapján azt állítottam, hogy a mezőny tömegével gyárt mandalát,
miközben a `mandala svg` kereslete −25,3%. A review-adat ezt **cáfolja**: 39,6% kínálat 40,4%
eladást termel, index **1,02**. A mandala nem túlkínált, hanem pontosan arányos. A keresési trend és
a tényleges eladás itt szétvált.

### Termékforma a review-kban

shadow box / papercut **35,7%**, fali panel 18,5%, egyéb tárgy 15,1%, besorolatlan 30,7%. Ez
megerősíti a [[findings/listing-craft]] kínálati arányát: a shadow box a vezető forma.

### A tényleges bestsellerek

| review | listing |
|---:|---|
| 20x | Laser cut Cross cutting files Multilayer **Mandala Cross** Religious |
| 17x | Multilayer layer design, laser cut, SVG, ai, dxf… |
| 15x | 7 layer 3D Multilayer **clock** design, mandala wall art |
| 11x | Layered **Christian Cross** SVG: Laser Cut Mandala Wall Art |
| 10x | 7-Multi Layer **Cross American Flag** SVG DXF |
| 10x | **Firefighter SVG** Layered / Wood Art / Shadow Box / Flames / Heroic |
| 9x | 3D **Hummingbird** Shadow Box SVG |
| 9x | **World Map** Laser Cut File SVG layered |
| 8x | **Custom Order** Multilayer SVG (két különböző listing, 8x + 8x) |

A kereszt+mandala kombó, a hazafias/foglalkozási téma (tűzoltó, zászló) és az **egyedi rendelés**
kiugranak.

## 2. A norse/kelta tézis megbukott

A [[workflows/norse-celtic-catalogue-plan]] arra épült, hogy a `viking helmet svg` (109,4
keresés/1000 listing) feltáratlan rés. Ennek ellenőrzésére lekérdeztem azt a 16 boltot, amelyik
ténylegesen rangsorol norse/kelta kifejezésekre — **609 review**:

| | review | arány |
|---|---:|---:|
| **rétegzett** (layered / multilayer / shadow box) | **17** | **2,8%** |
| gravírozás / tárgy (coaster, könyvjelző, érme, puzzle, doboz) | 358 | **58,8%** |
| norse/kelta témájú | 81 | 13,3% |

A téma legkelendőbb terméke a *„Tree of Life SVG Bundle: Celtic, Family Tree Roots"* (15 review) —
**lapos** design-csomag. A norse/kelta listingek közül csak **három** rétegzett, együtt 11 review
három év alatt (`Nordic Helm of Awe` 5x, `Viking Compass Wall Decor` 4x, `Viking Compass svg` 2x).

**A kereslet valós, de gravírozó fájlt és tárgyat akar, nem rétegzett falidíszt.** A jó arányszám
azért jó, mert kevés a listing — de a mögötte lévő szándék más termékre irányul.

## A visszatérő hibaminta

Ez a **harmadik** eset, amikor ígéretes eredmény alaposabb mérésen megbukott:
[[pitfalls/2026-08-07-single-listing-attribution]] (NenoWorks),
[[pitfalls/2026-08-07-duplicate-search-hits]] (Beameez), és most a norse/kelta.

Mindháromszor ugyanaz: **egy jó arányszám mögött nem néztük meg, mi van valójában.** A tanulság
általánosítva: *keresési arányszámra sosem szabad terméktervet építeni anélkül, hogy megnéznénk,
mit vesznek meg ténylegesen azok, akik arra a kifejezésre rangsorolnak.*

## Amit ez alátámaszt

Eladási adaton nyugvó irány: **vallási + hazafias + foglalkozási (tűzoltó, veterán) rétegzett
design, kereszt+mandala kombóval, plusz egyedi rendelés mint termék.** A mandala alapmotívumként
marad, mert arányosan fogy.

## Fenntartások

- A review **alsó becslés**; a review-arány és az eladási arány nem azonos, ha a motívumok
  értékelési hajlandósága eltér.
- A 33 boltos minta boltonként 50 friss review; a 16 boltos minta futása megszakadt (ABORTED), így
  609 review lett a tervezett ~640 helyett.
- A besorolás címszavas, a „egyéb" kategória 17–30% — a nagyságrendek jók, a századok nem.
- A hazafias (1,88) és portré (1,60) index **kis abszolút számokon** áll (0,8% és 1,0% kínálat).

## 3. Keresleti index szavanként — a tényleges javaslat alapja

A `review-arány / listing-arány` hányados szavanként, ott ahol legalább 8 review és 4 listing áll
mögötte. Szkript: `assets/scripts/reviews_deep.py`.

### Alulkínált (index > 1,4)

| szó | review | listing | index | megjegyzés |
|---|---:|---:|---:|---|
| cross | 104 | 15 | **3,41** | 44 különböző listingen — széles piac |
| hummingbird | 22 | 4 | 2,70 | |
| cow | 36 | 7 | 2,53 | highland cow, cowboy, western farmhouse |
| patriotic | 76 | 16 | 2,33 | |
| skull | 26 | 6 | 2,13 | sugar skull, Day of the Dead |
| flag | 54 | 13 | 2,04 | |
| horse | 21 | 6 | 1,72 | |
| religious | 43 | 13 | 1,63 | |
| christian | 31 | 10 | 1,52 | |
| clock | 47 | 16 | 1,44 | termékforma, 19 különböző listing |

### Túlkínált (index < 0,45) — kerülendő

| szó | review | listing | index |
|---|---:|---:|---:|
| sign (welcome sign) | 11 | 36 | **0,15** |
| deer | 11 | 24 | **0,23** |
| santa | 10 | 17 | 0,29 |
| owl | 12 | 17 | 0,35 |
| elephant | 8 | 10 | 0,39 |
| christmas | 40 | 46 | 0,43 |
| forest | 21 | 24 | 0,43 |

A `deer` külön tanulság: a [[findings/keyword-database]] szerint a `deer svg` **+55,1%**-kal nőtt
(vadászszezon előtt), és ezt biztató jelként említettem. Az eladási index **0,23** — masszívan
túlkínált. **A keresési trend megint mást mondott, mint a tényleges vétel.**

## 4. Termékforma-hiány: mécses / lámpás / gyertyatartó

| szó | review | különböző listing | a 33 bolt katalógusában |
|---|---:|---:|---:|
| tealight | 27 | **14** | **0** |
| lantern | 23 | **11** | 1 |
| lamp | 16 | 7 | 1 |
| suncatcher (stained glass) | 14 | 7 | 0 |
| mirror | 12 | 3 | 0 |

~~Ez nem egyszereplős torzítás — 7–14 különböző listing mindegyiknél.~~ **HIBÁS:** a listingszám nem
függetlenségi egység. Eladók szerint: tealight 2 eladó (23/29 egy bolttól), lantern **1 eladó**,
lamp 2, suncatcher **1**, mirror 2. Ez egy-két bolt katalógusa, nem piaci jel.

Ez a [[decisions/2026-08-08-parked-directions]] „rétegelt lámpa" ötletének igazolása, és egyben az
ottani óvatosságom cáfolata: a `light box svg` gyenge kulcsszava (4,8 arány, −48,4%) alapján
lebeszéltem volna róla. **A hiba a szótárban volt, nem a termékben** — a piac
`tealight` / `candle holder` / `lantern` / `night lamp` néven veszi.

A formátum jellemzően **csomag**: „8 Pcs Bundle Halloween Lantern", „10x Bundle Lantern Modern",
„54x Pack 3D Wood Lantern Wild Life Animal".

## 5. Amit temperálni kell a korábbi lelkesedésből

- **Egyedi rendelés / személyre szabás: index 1,10** — arányos, nem rés. A két „Custom Order"
  listing (8x, 8x) erős egyedi teljesítmény, de a kategória egésze nem alulkínált.
- **Foglalkozási téma: index 0,89** — szintén arányos. A `Firefighter` 5 listingen 16 review; jó,
  de nem kiugró.

## Az ajánlás

**Elsődleges: kereszt, hazafias, western és koponya motívum — külön-külön tesztelve.** (A hármas
kereszt+mandala+zászló kombó **nem** áll: egyetlen listing egyetlen eladótól. A kereszt+mandala
párosítás igen: 27 review, 6 eladó.) Ez a legjobban bizonyított
kereslet az egész projektben (index 3,41 / 2,33 / 2,04, 44 különböző keresztes listingen), és
koherens kulturális piac — amerikai hazafias–hit vonal, ami illeszkedik ahhoz, hogy a keresők
37,4%-a amerikai ([[findings/etsy-first-party-search-data]]).

~~Másodlagos termékforma: mécses / lámpás csomagok.~~ **VISSZAVONVA** — a jel 2 eladótól jön,
23/29 review egyetlen boltból. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

**További alulkínált motívumok:** western/farm (cow 2,53, horse 1,72), koponya (2,13), kolibri
(2,70), óra mint forma (1,44).
