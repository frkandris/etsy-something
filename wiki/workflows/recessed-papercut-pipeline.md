---
type: Workflow
title: Süllyesztett papírvágás-lánc — a referencia-termék tényleges szerkezete
description: A termék intaglio, nem relief: fehér fedőlap nyílásokkal, lefelé sötétedő lapokkal. A lánc öt lépése, a hozzá tartozó kapcsolók, és a menet közben tanult sorrendi szabály.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-10T05:00:00Z
sources:
  - resource: /assets/data/off-etsy-monetisation-report-2026-08-09.md
    title: nem forrás, csak kapcsolódó
---

# Süllyesztett papírvágás-lánc

## A szerkezeti tévedés, ami a leghosszabb kerülőt okozta

Nyolc körön át **kiemelkedő reliefet** építettem: kisebb rétegek egymás tetején, a legvilágosabb
elöl. A referencia-termék ennek a **fordítottja**: teljes fehér fedőlap, amiben nyílások vannak, és
a lapok lefelé sötétednek — a szem egy lépcsős kútba néz.

**Amiből eldőlt:** a `ref-abstract-dog` nagyítása. A kis köröknek **belső faluk és színes fenekük**
van, tehát átfúrt lyukak; és minden forma határán a felső él sötétebb, vagyis a felület lefelé lép.
Ezt a felhasználó vette észre, én a képet nézve nem.

**A javítás nem a renderben volt.** Először ott próbáltam (fehér lap boolean-nal a stack elé),
és az fragile volt. A helyes hely a **generátor**: a mező legyen a legvilágosabb szint, mert ő maga
a felső lap; nincs kivágandó fekete háttér. Innentől a meglévő nesting-gépezet magától a helyes
sorrendet adja, és a renderben semmit nem kellett fordítani.

## A lánc

| lépés | fájl | mit csinál |
|---|---|---|
| 0 | `00_generate.py` | gpt-image-2 mélységtérkép; `--recessed` a süllyesztett szerkezethez, `--ref/--crop` stílus-referenciához |
| 2 | `02_trace.py` | poszterizálás → potrace → shapely; nesting-kényszer, nyak-gyógyítás, vágásbiztonsági riport |
| 3 | `03_listing_images.py` | galéria: hero-overlay, specs-kártya, closeup, assembly |
| 4 | `04_composite.py` | `--shoot` háttérfotó generálás, `--place` kompozit vetett és kontaktárnyékkal |
| 5 | `05_video.py` | teljes szinuszos kamera-ciklus → kockánkénti kompozit → H.264 loop |

Stílus-készletek: `styles.py` (papercut-colour, papercut-mono, wood-relief, wood-terrain,
splatter-pop). Egy stílus egyben tartja a promptot, a szintszámot és a kapcsolókat — ezért nem
fordulhat elő, hogy egy papíros design fa-palettán renderelődik.

## A visszatérő sorrendi szabály

**Minden új geometriai lépést a nyak-gyógyító lánc ELÉ kell tenni, és a lánc gyógyítással
záruljon.** Ez négyszer derült ki ugyanígy:

1. a nesting-klippelés maga gyárt nyakat → a lánc gyógyítással zárul
2. a `--full-panel` unió 0,79 mm-es szilánkokat hagyott a korong pereme és a négyzet sarka között
3. a margósáv- és szemcse-tisztítás ugyanígy
4. a lyukasztás nyakat vágott a 2. rétegen

Egyik esetben sem új javítás kellett, hanem a meglévő gépezet a helyes ponton.

## Kapcsolók, amiket a reviewer kényszerített ki

| kapcsoló | miért |
|---|---|
| `--full-panel` | minden lap teljes négyzet, csak nyílásokkal (a modell korongot rajzol) |
| `--margin 30` | érintetlen sáv a lap szélén — a referenciákon a margóban semmi nincs |
| `--speckle 2.5` | nyitás **után** zárás; a nyitás önmagában tűlyukakat hagy |
| `--min-feature 6` | a referencia formanyelve durvább, mint a 2 mm-es vágási határ |
| `--punch 20` | a pöttyök eljárásszerűen: méret- és mélységszórással, egyoldali klaszterben |

## Néma hibák, amiket a codex talált

- **`o.bound_box` a kiértékeletlen kalitka**: extrude esetén lemarad, és a keret ebből épült — a
  nyílás 1,8-szer túl szélesre nyílt. A depsgraph `evaluated_get()` adja a valós határokat.
- **A flageket az argv szűrése után olvastam ki**, ezért `--white-top` és `--recessed` mindig
  `False` volt. Több körön át kerestem máshol az okot.
- **Két zsugorító blokk** volt a renderben; egyet javítottam, a másikról nem tudtam.
- **A lyukasztás a legmélyebb lapokat vágta át**, nem a felsőket: a pötty a hátlapon ment
  keresztül, a látható fedőlap ép maradt.
- **A `--full-panel` a belső lyukakat is visszaadta**, ezért az 1. réteg tömör lett (0 nyílás).

## A reviewer pontszám-íve

32 → 50 → 62 → 68 → 66 → 72 → 74 → 77 → 79 → 82. Az egyetlen visszalépés (68→66) akkor történt,
amikor a felső lap zsugorodott lebegő táblává — a javítás fényt derített három addig elfedett
problémára.

**Ami a 82-nél maradt:** rétegszám (3-4 olvasható lépcső a referencia 5-6 helyett), a pöttyök
tényleges klaszterezése (a paraméter megvan, a kimenet nem méri), és a szalagok vastagsága.
A reviewer szerint viszont innentől a **bemutatás** a nagyobb tétel: keretvariáció és tematikus
enteriőr — ezért lett témánként eltérő keret és háttérfotó.

## Provenancia

`product/pipeline/*`, `product/themes/*`. Kapcsolódik: [[findings/paper-layered-market]],
[[findings/competitor-listing-images]], [[workflows/production-pipeline]].
