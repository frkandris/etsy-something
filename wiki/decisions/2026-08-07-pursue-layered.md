---
type: Decision
title: A layered irányt visszük, nem a funkcionálisat
description: Mindkét szegmens felmérve; statisztikailag azonosak, így a váltásnak nincs adatalapja.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Döntés: marad a layered

**Dátum:** 2026-08-07 · **Döntő:** a felhasználó

## Kontextus

A layered keresésből indult a kutatás. Menet közben javaslat született a **funkcionális lézervágott
tárgyakra** (doboz, urna, keret) váltásra, amit viszont akkor még **egyetlen bolt kategórialistája**
támasztott alá, felmérés nélkül. A felhasználó jogosan kifogásolta, hogy egy nem kutatott területre
irányítja a javaslat.

## Mérlegelt opciók

1. **Layered fali dekor** — az eredeti tézis, 173 bolt felmérve (dedupolva 35 specialista,
   ebből 21 igazolt).
2. **Funkcionális tárgyak** — 285 bolt felmérve utólag, 73 szakosodott.
3. Mindkettő párhuzamosan.

## Döntés

**Layered.** A funkcionális szegmenst felmértük, hogy a döntés ne feltételezésen álljon —
[[findings/functional-segment-comparison]].

## Miért

A két szegmens **statisztikailag gyakorlatilag azonos**: medián korrigált bevétel 144 939 vs 138 388
HUF/hó, azonos méreteloszlás, azonos kedvezmény-norma, hasonló belépési esély. A funkcionális oldal
szétaprózottabb (285 vs 173 bolt ugyanannyi listingre) és olcsóbb ($4,00 vs $5,10).

Vagyis a váltásnak **nincs mérhető haszna**, viszont van költsége: a layered irányban már van 33
igazolt referenciabolt, kategória-térkép, kulcsszó- és formátumelemzés. A tudás átvitele veszteséges
lenne.

~~A pozicionálási tanulság mindkét szegmensben ugyanaz (nem akciózni, magasabb ár…)~~ — **az ár- és
akció-állítás a 2026-08-08-i auditon megbukott** ([[pitfalls/2026-08-08-wrong-unit-of-independence]]).
Ami maradt: a **közepes katalógusméret** (100–300 listing), és az ebben a szegmensválasztástól
független.

## Következmények

- A [[workflows/production-pipeline]] a layered termékre készül.
- Az eredeti „funkcionális tárgyakra váltani" javaslat visszavonva, de az adat megmarad
  (`assets/data/fn_*.json`, `fill-functional-sheet.gs`) — ha a layered nem indul be, ez a fallback
  már fel van mérve.

## Mikor vizsgáljuk újra

Ha 6–12 hónap után a layered katalógus nem termel, vagy ha a funkcionális szegmensre is lefut a
katalógus-korrekció és lényegesen más képet ad.
