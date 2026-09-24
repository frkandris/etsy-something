---
type: Finding
title: Projektállapot és technikai audit — 2026-09-05
description: Helyi ellenőrzések, reprodukált csempézési hiba és eltérő exportbiztonság a termékláncok között.
status: draft
generated:
  by: codex
  at: 2026-09-05
sources:
  - resource: ../../product/pipeline/cutlib.py
  - resource: ../../tests/test_cutlib.py
  - resource: ../../product/pipeline/run_theme.sh
  - resource: ../../product/pipeline/10_worldmap.py
  - resource: ../../product/iterations/0050-worldmap/report.json
---

# Lényeg

A projekt működő kutatási és termékfejlesztési prototípus. A helyi tesztek zöldek,
de a vágófájlok kiadhatóságát nem garantálják. Az audit nem futtatott új piaci
adatgyűjtést, képmodell-hívást, Blender-rendert vagy fizikai tesztvágást.

## Ellenőrzések és hatókör

- `./check.sh`: Ruff sikeres, a meglévő 30 pytest-teszt sikeres (0,52 s).
- `tests/mutation_check.py`: a 13 beépített mutáció mindegyikénél nem nulla
  pytest-kilépési kódot észlelt a keret. Ez e konkrét mutációkra vonatkozik.
- Kódolvasás: közös geometria, tesztek, trace/export, térképláncok, shell-vezérlés,
  profilok; a dokumentáció és két mentett termékrender szemrevételezése.

## Reprodukált hiba: a csempe túllépheti a gép méretkorlátját

A `cutlib.tile_piece()` a kis fragmentumokat visszaolvasztja egy szomszédba,
de az egyesítés után nem ellenőrzi újra a maximális méretet. A meglévő
`tests/test_cutlib.py` `_arm_piece()` tesztgeometriáján is reprodukálható:

```python
from shapely.geometry import box
from shapely.ops import unary_union
from cutlib import tile_piece

g = unary_union([box(0, 0, 300, 300), box(300, 149.75, 1000, 150.25)])
tiles = tile_piece(g, 330, 280, min_area=40)
print([(t.bounds[2] - t.bounds[0], t.bounds[3] - t.bounds[1]) for t, _ in tiles])
```

Mért darabméretek mm-ben: `(250, 150)`, **`(750, 150.25)`**, `(250, 150)`,
`(250, 150)`. A 330 × 280 mm-es korlát tehát sérül. A méretet vizsgáló meglévő
teszt egyszerű téglalappal fut; a szilánkbeolvasztást ellenőrző teszt nem állít
maximális méretet. A két feltételt együtt kell ellenőrizni.

## Export és hibajelzés

- A `10_worldmap.py` hibás geometriánál is kiírja a fájlokat, majd sikeresen
  visszatér. Az `0050-worldmap/report.json` mentett állapota `all_ok: false`,
  a szárazföldi rétegen két nyakkal. Ez mentett eredmény, nem az audit során
  újragenerált térkép.
- A `11_worldmap_flat.py` a végén jelenti a nyakakat és a darabméretet,
  de nem állítja meg hibás állapottal az exportot ezek alapján.
- A `run_theme.sh` `set -e` mellett, `pipefail` nélkül csővezetéken át futtatja
  a trace-t és a rendert. A végső `tail` sikeres kilépése elfedheti a tényleges
  generátorhibát; meglévő kimenet esetén régi fájlokkal folytatódhat a lánc.
- A `02_trace.py` szigorúbb ellenőrzést és staging könyvtárat használ, de a
  végső `rmtree(final_out)` + `rename` nem megszakításbiztos atomikus csere.

## Reprodukálhatóság és dokumentáció

- A `pyproject.toml` lint- és tesztkonfigurációt tartalmaz, telepítési
  függőséglistát nem; verziózárolás és CI-konfiguráció nem található a követett fájlokban.
- A profilok pipeline-receptje és a `run_theme.sh` trace-paraméterei külön élnek;
  utóbbi csak a renderelésnél tölti be a papercut profilt.
- A `wiki/CLAUDE.md` még azt állítja, hogy nincs kód, git és build tooling.
- A [[workflows/production-pipeline]] továbbra is „$9–28, akció nélkül” ajánlást
  tartalmaz, miközben az [[overview]] ezt visszavont következtetésként kezeli.
- A `product/LISTING.md` fizikai tesztvágás hiányát rögzíti. A megvizsgált
  dokumentációban ennek későbbi lezárását és saját listingek tényleges
  konverziós mérését nem találtam; ez nem bizonyítja, hogy a repón kívül sincs ilyen.

Kapcsolódik: [[workflows/self-testing-code]], [[workflows/product-profiles]],
[[workflows/worldmap-pipeline]]. A feltárt hibák ebben az auditban nem lettek javítva.

Utókövetés: a javítások és a tényleges termékiterációk eredménye a [[2026-09-05-reference-iteration]] lapon. Az audit fenti megállapításai a javítás előtti állapotot rögzítik.
