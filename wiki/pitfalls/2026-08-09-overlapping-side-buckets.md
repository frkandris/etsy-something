---
type: Pitfall
title: Átfedő oldal-besorolás — a „mindkettő" listingek mindkét alapba beleszámítottak
description: A fa/papír fájdalompont-összehasonlítás átfedő mintán készült, ami eltüntetett két valódi különbséget; javítva átfedésmentes mintával és konfidencia-intervallummal.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-09T15:00:00Z
---

# Átfedő oldal-besorolás

## Tünet

A [[findings/laser-vs-paper-split]] első változata azt állította, hogy a fájdalompontok
**nem** válnak szét fa és papír között: összeszerelés 2,5% vs 2,6%, törékenység 0,9% vs 1,0%.
Ebből azt a stratégiai következtetést vontam le, hogy „egy fájl kell, ami mindkét anyagon
működik", és hogy a vágásbiztonsági differenciálónk mindkét oldalon egyformán ér.

## Gyökérok

A listingeket négy csoportba soroltam a cím alapján: `lezer`, `papir`, `mindketto`, `egyik sem`.
Az összehasonlításnál a **`mindketto` csoportot mindkét oldal alapjához hozzáadtam**:

- „lézer-oldal" = lezer + mindketto = 1488 review
- „papír-oldal" = papir + mindketto = 798 review

A 602 `mindketto` review így **mindkét százalékba beleszámított**. Mivel a papír-only minta
mindössze 196 review, a közös 602 elem **háromszorosára hígította** a papír oldalt lézeres
tartalommal — vagyis a két arány matematikailag egymás felé húzódott. A módszer garantálta,
hogy ne találjak különbséget.

## Hogyan derült ki

A felhasználó azt kérte, mutassam meg, **mennyi adatból** mondom a következtetést. Amikor a
minta méretét tételesen kiírtam, azonnal látszott, hogy a két alap (1488 és 798) összege
nagyobb, mint a korpusz erre a kérdésre értelmezhető része, mert 602 elem duplán szerepel.

## Alkalmazott korrekció

Átfedésmentes minta (`mindketto` **egyik** oldalra sem számít) + kétarányos 95%-os
konfidencia-intervallum:

| panasz | fa (886 rev / 42 eladó) | papír (196 rev / 17 eladó) | különbség 95% CI | ítélet |
|---|---:|---:|---|---|
| összeszerelés / útmutató | 21 = 2,37% | 5 = 2,55% | [−2,60; +2,24] pp | **nem dönthető el** |
| **törékeny / túl vékony** | 6 = 0,68% | **0 = 0,00%** | [+0,14; +1,22] pp | **valódi különbség** |
| **méretezés** | 17 = 1,92% | **0 = 0,00%** | [+1,02; +2,82] pp | **valódi különbség** |
| rétegek nem illeszkednek | 5 = 0,56% | 1 = 0,51% | [−1,06; +1,17] pp | nem dönthető el |

## Stratégiai következmény

Ez **nem apró számjavítás**, mert megfordítja a differenciálónk értékét:

- A **törékenység és a méretezés lézer-oldali probléma** — a papír-only mintában (196 review)
  **egyetlen** ilyen panasz sincs.
- A vágásbiztonsági riport és a biztonságos méretezési alsó határ tehát a **fa** oldalon ér
  sokat, a papíron kevesebbet.
- Ha a papíros irányt visszük, a differenciálót **máshol** kell keresni: összeszerelési
  útmutató, keretméret-illeszkedés, színséma — lásd [[findings/paper-layered-market]].

## Tanulság

**Átfedő csoportokat soha ne hasonlíts össze.** Ha egy elem több csoportba is beletartozhat,
vagy hagyd ki a többesélyeseket az összehasonlításból, vagy rendeld egyértelműen egyhez —
de ne add hozzá mindkettőhöz. Az átfedés mindig a **kisebb** csoportot torzítja jobban, és
mindig a „nincs különbség" irányba.

**És minden arány mellé írj mintaméretet és konfidencia-intervallumot.** A „2,5% vs 2,6%"
magabiztosnak hangzott; a valóságban a különbség CI-je ±2,4 százalékpont volt, vagyis a mérés
eleve alkalmatlan volt a kérdés eldöntésére. Ez ugyanaz a családi hiba, mint a
[[pitfalls/2026-08-08-wrong-unit-of-independence]]: nem a szám volt rossz, hanem az, amit
a szám mérni tudott.
