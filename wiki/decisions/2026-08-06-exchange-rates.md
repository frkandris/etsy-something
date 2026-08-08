---
type: Decision
title: Árfolyam-konvenció: USD 316,33 és EUR 364,6
description: A felhasználó meglévő soraiból visszafejtve, nem napi jegyzésből — a konzisztencia fontosabb.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Döntés: rögzített árfolyamok

**Dátum:** 2026-08-06

## Kontextus

A SalesDoe különböző devizákban adja a bevételt (USD, EUR, GBP, CAD, AUD, SGD, SEK, HKD, MYR), a
tábla viszont HUF-ban számol.

## Döntés

| deviza | HUF |
|---|---:|
| USD | **316,33** |
| EUR | **364,60** |
| GBP | 426,0 |
| CAD | 226,0 |
| AUD | 222,8 |
| SGD | 246,7 |
| SEK | 33,42 |
| HKD | 40,32 |
| MYR | 77,35 |

## Miért

Az USD és EUR értéket **a felhasználó meglévő 2026-08-06-os soraiból fejtettem vissza** (pl.
SeynDigital 470 USD → 148 647 HUF), nem élő jegyzésből. A többit a `frankfurter.dev` aznapi
keresztárfolyamaiból számoltam, **az USD = 316,33-hoz igazítva**.

Az élő jegyzés aznap USD/HUF 315,15 volt, tehát a különbség 0,4% — elhanyagolható. A **konzisztencia
a meglévő sorokkal** viszont fontos: különben ugyanannak a boltnak a 2026-os sora más árfolyamon
állna, mint a szomszédjáé, és a diffek értelmezhetetlenné válnának.

## Következmények

Ha egy jövőbeli felmérés új dátummal készül, **ne** ezeket az árfolyamokat használd — akkor új
konvenció kell, és azt itt kell rögzíteni.
