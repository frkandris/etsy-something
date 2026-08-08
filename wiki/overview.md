---
type: Overview
title: Mit vizsgálunk és mire jutottunk
description: A teljes projekt egy oldalon — a kérdés, az adat, a válasz, és a hozzá tartozó megbízhatóság.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/layered_adjusted.json
    title: specialista boltok katalógusból számolt layered aránnyal (dedupolva 35, ebből 21 igazolt)
  - resource: /assets/data/catalog_sample.json
    title: 1543 listing a boltok saját katalógusából mintavéve
---

# Áttekintés

## A kérdés

Van-e olyan digitális termék niche az Etsy-n, amibe érdemes belépni, és ha igen, milyen termékkel,
áron és katalógusmérettel? A kiindulópont egy meglévő követő tábla volt: ~57 bolt felmérve
**2024-08-04**-én, majd újra **2026-08-06**-án (lásd [[findings/2024-vs-2026-cohort]]).

## A válasz egy bekezdésben

**Multilayer / layered lézervágott SVG fájlok**, **100–300 listinges katalógussal** — ez az egyetlen
strukturális eredmény, ami a 2026-08-08-i auditot is túlélte. Az igazolt populáció (21 bolt) medián
boltja **417 ezer HUF/hó**-t termel.

**Termékirány eladási adatból** (a 21 igazolt bolt **1 027 deduplikált** review-ja), ott ahol több
különböző eladó adja a jelet: **kereszt** 57 review / 8 eladó, **hazafias** 68 / 10,
**western-farm** 28 / 10, **koponya** 18 / 8. A motívumokat **külön-külön** kell kezelni: a
kereszt+mandala párosítás áll (27 review, 6 eladó), a **hármas** kereszt+mandala+zászló viszont
egyetlen listing egyetlen eladótól. Lásd
[[findings/review-mining]] és [[decisions/2026-08-07-pursue-layered]].

> **Az audit után visszavont állítások:** a „ne akciózz" és az „ár monoton együtt jár az
> eredménnyel" **nem tartja magát** deduplikált populáción; az európai klaszter 2 boltra esett; a
> mécses/lámpás „rés" egyetlen eladó katalógusa volt. Részletek:
> [[pitfalls/2026-08-08-wrong-unit-of-independence]].

## Hogyan épült a populáció — és miért fontosabb ez bármelyik egyes számnál

Három egyre szigorúbb szűrő, és mindegyik megváltoztatta a választ:

| szűrő | boltok | medián HUF/hó |
|---|---:|---:|
| megjelent az 5 Etsy keresésben (500 listing) | 173 | 205 816 |
| legalább 3 **különálló** listinggel rangsorolt („specialista") | **35** | 320 156 |
| **katalógus mintavéve, ≥80%-ban layered („igazolt")** | **21** | **416 893** |

*(Mindkét medián **katalógus-aránnyal korrigált**; korrekció nélkül 471 998 és 435 019 volna — a
kettőt nem szabad egy oszlopban keverni. A 65 és 33 a 2026-08-08-i auditig érvényes, hibás szám volt: a szűrő keresési sorokat számolt
különálló listingek helyett. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].)*

A középső lépés kiszórta azokat a boltokat, amelyek **egyetlen** kulcsszóra optimalizált listinggel
rangsoroltak, miközben teljesen mást árulnak — a nyers populáció 49%-át. Az utolsó lépés minden bolt
bevételét újrasúlyozta azzal, hogy a saját katalógusának hány százaléka valóban layered; ez a
specialista mediánt 55%-kal vágta le (321 653 → 144 939 mind a 65 boltra), és az egyik kiemelt boltot
1,3M HUF/hó-ról **nullára** vitte.

A `findings/` minden száma megmondja, e három populáció közül melyikhez tartozik. Az a szám, amelyik
nem mondja meg, definíció szerint hibás. A [[pitfalls/_index|pitfalls]] mappa mutatja, hányféleképpen
ment ez félre, mielőtt jóra fordult.

## A piac alakja

- **Zsúfolt és épp elárasztás alatt.** 173 bolt látszik öt keresés top találataiban; közülük **47 az
  elmúlt 12 hónapban nyílt**. Lásd [[findings/layered-niche-size-and-structure]].
- **Alacsony költségű országok uralják.** A 21 igazolt boltból 10 ukrán, mellette Törökország,
  Vietnám, Indonézia. A volumenversenyt ellenük elveszíted.
- **Tartósan akciós.** A boltok 75%-a állandó 30–70%-os „akciót" futtat. Hogy ez árt-e vagy segít,
  **a mi adatunkból nem dönthető el** — dedupolva a nem akciózó csoport 3 bolt, és a sávok eredménye
  nem monoton. Lásd [[findings/pricing-and-discounting]].
- **Az ár és az eredmény kapcsolata bizonytalan.** A dedupolt populáción a listingenkénti bevétel
  az árral **csökken** (1 720 → 1 581 → 1 338 → 817), a $12+ sávban egy bolt maradt. A korábbi
  „monoton" állítás visszavonva.

## A két ténylegesen cselekvési következtetés

1. **100–300 listing legyen a cél, ne 500+.** A dedupolt populáción is ez a legjobb listingenkénti
   sáv (**2 009 HUF/listing**, szemben a 300–700 sáv 825-ével), és egyedül is elérhető havi ~4–10
   listinggel. Ez az egyetlen strukturális eredmény, ami az auditot túlélte.
   [[findings/catalogue-size-and-throughput]]
2. **Termékirány eladási adatból, nem keresésiből:** kereszt (57 review / **8 eladó**), hazafias
   (68 / 10), western-farm (28 / 10), koponya (18 / 8) — a 21 igazolt bolt deduplikált review-in.
   [[findings/review-mining]]

## Amit a munka elvégzéséről tudunk

A [[workflows/production-pipeline]] tartalmazza az AI-támogatott termelési utat (képmodell →
poszterizálás → rétegenkénti trace → boolean unió → vágásbiztonsági ellenőrzés → Blender mockup), az
átfutási számokat és a gépbeszerzés sorrendjét. Röviden: a geometria determinisztikus szkript, az AI
a két végén segít (koncepciógrafika, mockup render), a fizikai validáció pedig kölcsönkérhető, nem
kell megvenni.

## Hol vannak a számok

- Eredmények és populációik: [[findings/_index]]
- Referenciaboltok: [[shops/_index]]
- Hogyan gyűjtöttük az adatot, és mibe kerül újra: [[methods/_index]]
- A mérési hibák, hogy ne ismétlődjenek: [[pitfalls/_index]]
- Nyers adatok: `assets/data/`, elemző szkriptek: `assets/scripts/`
