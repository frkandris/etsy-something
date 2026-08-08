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
    title: 65 specialista bolt katalógusból számolt layered aránnyal
  - resource: /assets/data/catalog_sample.json
    title: 1543 listing a boltok saját katalógusából mintavéve
---

# Áttekintés

## A kérdés

Van-e olyan digitális termék niche az Etsy-n, amibe érdemes belépni, és ha igen, milyen termékkel,
áron és katalógusmérettel? A kiindulópont egy meglévő követő tábla volt: ~57 bolt felmérve
**2024-08-04**-én, majd újra **2026-08-06**-án (lásd [[findings/2024-vs-2026-cohort]]).

## A válasz egy bekezdésben

**Multilayer / layered lézervágott SVG fájlok.** A belépés a **nem akciózó, magasabb árú végén**
érdemes: nagyjából **70–200 listing, $9–28-as áron, tartós kedvezmény nélkül**. Az igazolt populáció
medián boltja **320 ezer HUF/hó**-t termel; a négy közép-/nyugat-európai igazolt bolt mediánja
**743 ezer HUF/hó és 3 629 HUF/listing**, szemben a 23 alacsony költségű országbeli bolt 285 ezres
és 1 240-es értékével. A belépési esély valós, de nem nagylelkű: a három évnél fiatalabb boltok
nagyjából **ötödé jut 500 ezer HUF/hó fölé**. Lásd [[decisions/2026-08-07-pursue-layered]].

## Hogyan épült a populáció — és miért fontosabb ez bármelyik egyes számnál

Három egyre szigorúbb szűrő, és mindegyik megváltoztatta a választ:

| szűrő | boltok | medián HUF/hó |
|---|---:|---:|
| megjelent az 5 Etsy keresésben (500 listing) | 173 | 210 327 |
| legalább 3 különálló listinggel rangsorolt („specialista") | 65 | 321 653 |
| **katalógus mintavéve, ≥80%-ban layered („igazolt")** | **33** | **320 156** |

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
- **Alacsony költségű országok uralják.** A 33 igazolt boltból 15 ukrán, mellette Törökország,
  Vietnám, Indonézia. A volumenversenyt ellenük elveszíted.
- **Tartósan akciós — és az akciózók veszítenek.** A boltok 75%-a állandó 30–70%-os „akciót" futtat.
  Az a hat igazolt bolt, amelyik **nem** akciózik, a legjobb gazdaságosságú a mezőnyben.
  Lásd [[findings/pricing-and-discounting]].
- **Az ár monoton együtt jár az eredménnyel.** Minden ársáv $12+-ig veri az alatta lévőt, havi
  bevételben és listingenkénti bevételben egyaránt.

## A két ténylegesen cselekvési következtetés

1. **Ne akciózz, és árazz $9–28 közé.** Ez a legerősebb és legkövetkezetesebb jelzés az adatban, és
   minden korrekciót túlélt. [[findings/pricing-and-discounting]]
2. **100–300 listing legyen a cél, ne 500+.** Ez a legjobb listingenkénti sáv, és egyedül is
   elérhető havi ~4–10 listinggel. 100 listing alatt a medián bolt kicsi (70 ezer HUF/hó) — a 29 és
   72 listinges kivételek léteznek, de kivételek. [[findings/catalogue-size-and-throughput]]

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
