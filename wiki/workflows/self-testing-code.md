---
type: Workflow
title: Öntesztelő kód — miért van tesztkészlet egy piackutatási repóban
description: A vágás-geometriának regressziós tesztkészlete van (30 teszt), mert 2026-08-14-én három egymást követő javítási kör mindegyike bevezetett egy új hibát. A tesztek mutációval igazoltak (13/13 elbukik a hibás kódon) — és maga a mutációs keret kétszer hazudott, mielőtt helyes lett.
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
./check.sh                                   # ruff + pytest, 0,2 mp — minden javítás után
.venv/bin/python tests/mutation_check.py     # elbuknak-e a tesztek a hibás kódon (lassú)
```

A sorrend nem esztétika: a ruff `F821` (nem létező név) egyszer már elkapott egy hibát egy
**több perces Blender-futás előtt** — a `heal_to_convergence` import nem landolt, mert a
csere-mintám elvétette a tényleges sortördelést.

## A nem nyilvánvaló rész: a teszt igazolása

A Google kódellenőrzési útmutatója szerint a teszt akkor ér valamit, ha **elbukik, amikor a kód
elromlik**. Ez nem magától értetődő, és nálunk konkrétan nem is teljesült.

Az igazolás módja **mutáció**: `tests/mutation_check.py` visszavonja a javításokat a `cutlib.py`-ban
— egyenként, a valódi javítás valódi visszacsinálásával —, és megnézi, elbukik-e a hozzá tartozó
teszt. Jelenlegi állás: **13/13 mutáció elbukik**, 30 teszt mellett.

Amit ez útközben feltárt:

| mit találtunk | hol volt a hiba |
|---|---|
| 2 teszt zöld maradt a hibás kódon (csempe: terület-megőrzés, szilánk-beolvasztás) | a **fixture-ben**: a próbageometriám nem hozta létre a hibát |
| `test_bridge_no_redundant_crossing` a laza `< minimal * 1.35` korláttal a mutánst is átengedte | az **állításban**: az ág valójában nem is megfigyelhető (lásd lent) |
| `test_bridge_max_span_reports_orphans` átengedte a `continue` törlését | az **állításban**: az árva jelentődött, de közben mégis hozzáhidalódott |
| `svg_text` üres feliraton **összeomlik**, nem `None`-t ad | **valódi, lappangó hiba a kódban** — a `if not subs: return None` őr elérhetetlen volt |

A fixture-hiba oka konkrétan: a nagy téglalap + kis háromszög párosból a csempe-rács soha nem
vágott le izolált, vékony fragmentumot. A teszt lefutott, zöld lett, és semmit nem mért. Az új
fixture (`_arm_piece`: 300 × 300-as törzs + 700 mm hosszú, **0,5 mm vékony** kar) úgy van
megválasztva, hogy a rács középső cellái **csak a kart** tartalmazzák.

## Amit NEM fedünk le, és ezt ki is mondjuk

A `bridge_components` felesleges-kereszt-kötés elleni ága (~293. sor) **nem figyelhető meg a
kimeneten**: az ág törlése után négy különböző fixture-rel is **bitre ugyanaz**, 292,00 mm² jött ki.
A felesleges híd ugyanabban a folyosóban épül, ezért az unió elnyeli. Ez teljesítménybeli ág, nem
geometriai — és ezt a teszt docstringje kimondja, ahelyett hogy egy laza korláttal úgy tennénk,
mintha le lenne fedve.

## A keret kétszer hazudott

Ez a rész fontosabb, mint amilyennek látszik: **a mutációs keretem kétszer jelentett valótlant**,
mindkétszer „minden rendben" irányba tévedve.

1. **Szövegillesztés a pytest kimenetére.** Az első, shellben írt változat a `*"failed"*` mintára
   illesztett. Amikor a `pyproject.toml`-ba bekerült a pytest-konfiguráció, az összefoglaló sor
   formátuma megváltozott, és a keret **mind a nyolc mutációt „átmegy"-ként** jelentette — pont az
   ellenkezőjét a valóságnak. Azóta minden a **kilépési kódon** megy.
2. **`__pycache__`.** A pyc érvénytelenítése `(mtime, méret)` párost néz. A gyors, egymást követő
   újraírásoknál a pytest a **mutálatlan kódot** futtatta, és két mutáció így „túlélőnek" látszott.
   Azóta a keret törli a `__pycache__`-t és `PYTHONDONTWRITEBYTECODE=1`-gyel indít.

Ehhez jött egy harmadik, csendesebb csapda: a `replace(old, new, 1)` az **első** előfordulást
cseréli, az üres-bemenet őr viszont a `polys()`-ban is ott van — vagyis a rossz függvényt mutáltam,
miközben a mutáció „alkalmazottnak" látszott. A keret most **hibát jelez, ha a mintázat nem
egyedi**, és akkor is, ha egyáltalán nem található meg.

## Tanulság

**A zöld teszt nem bizonyíték** — és **a zöld mutációs jelentés sem az**. Egy teszt, ami sosem látta
a hibát, pontosan olyan zöld, mint amelyik megvédene tőle; egy keret, ami a rossz fájlt méri,
pontosan olyan magabiztos, mint amelyik a jót.

Ez ugyanaz a mintázat, mint a mérési hibáinknál: a
[[pitfalls/2026-08-14-a-hiba-a-forrasban-volt]] szerint *ha a defekt minden rétegen megjelenik, a
forrás a hibás; ha egyen, a lánc*. Itt kétszer is a **mérőeszköz** volt a hibás, nem a mért dolog —
és mindkétszer az árulta el, hogy az eredmény **túl egyöntetű volt ahhoz, hogy igaz legyen** (nyolc
átmenő mutáció egyszerre, illetve két túlélő olyan teszteknél, amiket kézzel már elbuktattam).

## Populáció-megjegyzés

A fenti számok **30 teszt** és **13 mutáció** populációjára vonatkoznak, kizárólag a `cutlib.py`
vágás-geometriájára. A `render_blender.py`, a `02_trace.py`, a `geolib.py` és a profilbetöltés
**fedetlen** — az ottani regressziókat (`film_transparent`, keretszélesség, paletta-szivárgás)
továbbra is csak render-bírálat fogja meg.

## Provenancia

Források: [Fowler, SelfTestingCode](https://martinfowler.com/bliki/SelfTestingCode.html) —
„előbb írj tesztet, ami megmutatja a hibát, és csak utána javíts";
[Google eng-practices, What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
— a bírálói prioritási sorrend negyedik eleme a Tests, azzal a kikötéssel, hogy a teszt legyen
érvényes és bukjon el a kód romlásakor.

Kapcsolódik: [[workflows/product-profiles]], [[findings/arxiv-layering-research]].
