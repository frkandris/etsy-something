---
type: Pitfall
title: A teljes bolt bevétele a niche-hez írva
description: A specialista-szűrés után is a bolt egészének bevételével számoltunk; a katalógus-korrekció 55%-ot vitt le a mediánból.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# A teljes bolt bevétele a niche-hez írva

**Dátum:** 2026-08-07 · **Súlyosság:** minden abszolút számot érintett

## Tünet

A specialista-szűrés (≥3 találat) után is minden bolt **teljes** élettartamú eladásából számoltam a
niche-bevételt — pedig egy vegyes profilú bolt (pl. CNC + lézer + STL) eladásainak csak töredéke
tartozik ide.

## Gyökérok

Nem volt adatom a boltok saját katalógusáról, csak arról, mivel kerültek be a keresésbe. A bekerülési
listing ≠ a bolt profilja.

## Hogyan derült ki

A felhasználó rákérdezett, hogy a javaslat alapját adó boltok nem csak „belekeveredtek"-e a
keresésbe. Ennek ellenőrzéséhez futott le a katalógus-mintavétel — boltonként 24 listing, 65 boltra,
összesen 1 543 listing.

## Alkalmazott korrekció

```
korrigált bevétel = bevétel × (a katalógusból layered listingek aránya)
```

| katalógus layered aránya | boltok | nyers medián | korrigált |
|---|---:|---:|---:|
| 80–100% | 33 | 329 148 | 320 156 |
| 50–80% | 8 | 256 950 | 157 058 |
| 20–50% | 11 | 95 254 | 26 385 |
| **<20%** | **13** | **472 797** | **~0** |

**Az összes bolt mediánja 321 653 → 144 939 HUF/hó (−55%).** A belépési esély (500k+, <3 év) 19%-ról
kb. 16%-ra változott.

Figyelemre méltó: a „belekeveredett" (<20%) csoportnak volt a **legmagasabb** nyers mediánja — a nagy
számok aránytalanul azoktól jöttek, akik nem is ebben utaznak. Pontosan ez tette a hibát veszélyessé:
felfelé torzított, nem lefelé.

## Tanulság

**Bolt-szintű metrikát soha ne rendelj niche-hez a bolt katalógusának ismerete nélkül.** A
katalógus-mintavétel olcsó (~2 USD 65 boltra) ahhoz képest, amennyit a hiba ér. Ez most a
[[methods/data-collection-pipeline]] kötelező 4. lépése.
