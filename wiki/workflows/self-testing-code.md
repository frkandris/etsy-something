---
type: Workflow
title: Öntesztelő kód — miért van tesztkészlet egy piackutatási repóban
description: A vágás-geometriának regressziós tesztkészlete van, mert 2026-08-14-én három egymást követő javítási kör mindegyike bevezetett egy új hibát, és mindet külső bíráló találta meg. A tesztek mutációval igazoltak: visszavontuk a javítást, és megnéztük, elbuknak-e.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-19T00:00:00Z
---

# Öntesztelő kód

## A probléma, ami ezt kikényszerítette

2026-08-14-én a `cutlib.py` **három egymást követő javítási körében mindegyik kör bevezetett egy
új hibát**, és egyiket sem a saját ellenőrzésem fogta meg:

| kör | a javítás | amit a javítás elrontott |
|---|---|---|
| 1 | `min_area` a csempehatáron | 34 712 mm² anyag eltűnt az ázsiai darabból |
| 2 | terület-megőrzés | 3,09 × 0,74 mm-es csempe — vékonyabb a 2 mm-es minimális webnél |
| 3 | pont-érintkezés hidalása | `nearest_points()` azonos pontot ad → nulla hosszú `LineString` → ÜRES buffer, a javítás hatástalan |

Mindhármat egy külső bíráló (codex) találta meg. A visszacsatolási hurok addig **percekben és
LLM-hívásokban** mérődött; most **fél másodperc**.

## A gyakorlat

```bash
./check.sh        # ruff + pytest, ebben a sorrendben
```

A sorrend nem esztétika: a ruff `F821` (nem létező név) egyszer már elkapott egy hibát egy
**több perces Blender-futás előtt** — a `heal_to_convergence` import nem landolt, mert a
csere-mintám elvétette a tényleges sortördelést.

## A nem nyilvánvaló rész: a teszt igazolása

A Google kódellenőrzési útmutatója szerint a teszt akkor ér valamit, ha **elbukik, amikor a kód
elromlik**. Ez nem magától értetődő, és nálunk konkrétan nem is teljesült: a 19 tesztből
**kettő hasztalan volt**.

Az igazolás módja **mutáció**: visszavontam a javítást a `cutlib.py`-ban, és megnéztem, elbukik-e a
hozzá tartozó teszt.

| mutáció | első kör | a javítás után |
|---|---|---|
| pont-érintkezés javítás visszavonva | elbukik ✓ | — |
| üres bemenet guard visszavonva | elbukik ✓ | — |
| `evenodd` egy-path visszavonva | elbukik ✓ | — |
| DXF Y-tükrözés visszavonva | elbukik ✓ | — |
| **csempe terület-megőrzés visszavonva** | **ÁTMEGY ✗** | elbukik ✓ |
| **szilánk-beolvasztás visszavonva** | **ÁTMEGY ✗** | elbukik ✓ |

**Miért mentek át:** a próbageometriám (nagy téglalap + kis háromszög) egyszerűen **nem hozta létre
a hibát** — a csempe-rács nem vágott le belőle izolált, vékony fragmentumot. A teszt lefutott, zöld
lett, és semmit nem mért. Az új fixture (`_arm_piece`: 300 × 300-as törzs + 700 mm hosszú, **0,5 mm
vékony** kar) úgy van megválasztva, hogy a rács középső cellái **csak a kart** tartalmazzák.

## Tanulság

**A zöld teszt nem bizonyíték.** Egy teszt, ami sosem látta a hibát, pontosan olyan zöld, mint
amelyik megvédene tőle. Az egyetlen olcsó igazolás: **rontsd el a kódot, és nézd meg, elbukik-e**.

Ez ugyanaz a mintázat, mint a mérési hibáinknál: a
[[pitfalls/2026-08-14-a-hiba-a-forrasban-volt]] szerint *ha a defekt minden rétegen megjelenik, a
forrás a hibás; ha egyen, a lánc*. Itt: **ha a teszt a hibás kódon is zöld, a fixture a hibás, nem
a küszöb.**

## Populáció-megjegyzés

A fenti számok **19 teszt** és **6 mutáció** populációjára vonatkoznak, kizárólag a `cutlib.py`
vágás-geometriájára. A `render_blender.py`, a `02_trace.py` és a profilbetöltés **fedetlen** — az
ottani regressziókat (`film_transparent`, keretszélesség, paletta-szivárgás) továbbra is csak
render-bírálat fogja meg.

## Provenancia

Források: [Fowler, SelfTestingCode](https://martinfowler.com/bliki/SelfTestingCode.html) —
„előbb írj tesztet, ami megmutatja a hibát, és csak utána javíts";
[Google eng-practices, What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
— a bírálói prioritási sorrend negyedik eleme a Tests, azzal a kikötéssel, hogy a teszt legyen
érvényes és bukjon el a kód romlásakor.

Kapcsolódik: [[workflows/product-profiles]], [[findings/arxiv-layering-research]].
