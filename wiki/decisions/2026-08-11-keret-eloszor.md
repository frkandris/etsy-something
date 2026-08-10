---
type: Decision
title: Keret-először: a rétegsorrend tervezői döntés, nem mért mennyiség
description: A kutatás szerint a valódi eladók nem bontanak képet rétegekre — keretet rajzolnak, és rétegenként uniózzák hozzá az elemeket. Ezért a generált kép stílus-referencia marad, a kényszereket pedig a promptba és a láncba tesszük.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-11T04:30:00Z
---

# Keret-először

## Kontextus

Három egymás utáni kísérlet bukott meg azon, hogy egy kész illusztrációból akartuk *kimérni* a
rétegsorrendet:

| kísérlet | miért bukott |
|---|---|
| a képmodell rajzoljon mélységtérképet | nincs dokumentált eset, hogy egy generatív modell megbízhatóan tartaná a „világos = közel" konvenciót |
| monokuláris mélységbecslés (Depth Anything V2 Small) | a rajzot fal előtt álló tömör tárgynak olvassa: gyönyörű sziluett, a témán belül szinte semmi szerkezet |
| tónus-rangsorolás | önmagában majdnem helyes (33 régióból 1 sérti), de a **szintszám** és a szigorú beágyazás feltevése hibás |

## Amit a kutatás talált

A valódi eladók **nem bontanak képet**. A dokumentált műhely-munkafolyamat *keret-először*:
megrajzolják a keretet, majd rétegenként `Union`-nal hozzáadják az elemeket, és a kimondott szabály,
hogy **minden új réteg minden eleme kapcsolódjon a kerethez**
([Inkscape-tutorial](https://dinosaurmama.com/post/free-shadow-box-template/)). Mandaláknál
koncentrikus `Path Offset` egyetlen sziluettből. Vagyis a rétegsorrend a szakmában **tervezői
döntés**, ezért nem is lehetett kimérni.

Ugyanezt mondja egy független AI→SVG gyakorlati teszt: ha a kép nem rétegekre készült, a konverter
összemossa ([forrás](https://dinosaurmama.com/post/ai-svg/)).

## Döntés

A generált kép **stílus-referencia és formaforrás**, a gyárthatósági kényszereket két helyre tesszük:

1. **A promptba.** Kapcsoltsági blokk: nincs sziget — minden alakzat érintsen egy azonos tónusú
   alakzatot vagy fusson ki a kép széléig; az arc elemei (szem, orr) érjenek össze a hozzájuk
   tartozó folttal, ne pontként üljenek egy világos pofa közepén.
2. **A láncba.** `--connected`: minden réteg egyetlen, a keretig érő darab; a leváló sziget nem
   vész el, egy lappal hátrébb kerül (a rétegek egymásba ágyazottak, tehát a lenyomata ott anyag).

## Miért

Mert a kényszert *előre* kell közölni, nem utólag kikényszeríteni. Amikor utólag tettük, a lánc
kitörölte azokat a részleteket, amiken a felismerhetőség múlt — a macska írisze például világos
sziget a sötétebb szőrben, tehát pontosan az, amit a szabály tilt.

## Következmények

- A paletta is a rajzból jön (`palette.json`), nem kézzel hangolt rámpából: a rámpa majdnem fekete
  mélye eltemetett egy világos-dominás designt.
- A papírvastagság 3,2 mm-ről 2,2 mm-re: a lépcsőárnyék minden mélyedést majdnem feketére vitt.
- Az „egy szint = egy szín" feltevés **elhagyva**. Egy valódi többrétegű papírvágásban több,
  különböző színű darab ül ugyanazon a lapon; a szín és a mélység független.

## Nyitott kérdés

Az árasztásos mező-keresés akkor bukik, ha a világos háttér **átfolyik** a témán belüli világos
sávokba (a `0043/c2` illusztrációnál a krém mező összeér a macska világos szőrével). Ilyenkor az
árasztás felfalja a témát. Következő kör: a mező-maszk korlátozása a kép szélétől mért távolsággal,
vagy a kapcsoltsági prompt kiegészítése azzal, hogy a téma körvonala mindenütt záruljon.

## Provenancia

`product/pipeline/00_generate.py` (FLAT + kapcsoltsági blokk), `product/pipeline/01b_depth.py`,
`product/pipeline/02_trace.py` (`--connected`). Kapcsolódik:
[[pitfalls/2026-08-11-a-szuro-torolte-a-felso-lapokat]], [[decisions/2026-08-10-keprogeneralas-iranya]].
