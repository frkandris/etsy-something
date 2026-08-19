"""Mutációs ellenőrzés: elbukik-e a teszt, amikor a kód elromlik?

Futtatás:  .venv/bin/python tests/mutation_check.py

**Miért kell ez a pytest mellé.** A Google kódellenőrzési útmutatója szerint a
teszt akkor ér valamit, ha elbukik a kód romlásakor. Ez nálunk konkrétan nem
teljesült: az első 19 tesztből **kettő zöld maradt a hibás kódon is**, mert a
próbageometriám egyszerűen nem hozta létre a hibát. Egy ilyen teszt pontosan
olyan zöld, mint amelyik megvédene — a különbség csak így mérhető.

**Ez nem gyors** (mutációnként egy pytest-indítás), ezért NEM része a
`check.sh`-nak. Akkor futtasd, amikor új tesztet írsz vagy `cutlib.py`-t
javítasz.

*Figyelmeztetés a keretre magára:* az első, shellben írt változatom a pytest
összefoglaló sorára illesztett szöveget, és amikor a pytest-konfiguráció
megváltoztatta a sor formátumát, **mind a nyolc mutációt „átmegy"-ként
jelentette** — pont az ellenkezőjét a valóságnak. Ezért megy itt minden a
**kilépési kódon**, nem szövegen.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / "product" / "pipeline" / "cutlib.py"
PY = str(ROOT / ".venv" / "bin" / "python")

# (leírás, a védő teszt neve, régi kódrészlet, mire cseréljük)
# Minden sor egy VALÓDI javítás visszavonása, nem kitalált elrontás.
MUTATIONS = [
    ("csempe: min_area a csempehatáron (anyagvesztés)",
     "test_tile_preserves_area",
     "            for q in polys(part):\n                out.append((q, (r, c)))",
     "            for q in polys(part):\n                if q.area >= min_area:\n"
     "                    out.append((q, (r, c)))"),

    ("csempe: szilánk-beolvasztás elhagyva (vághatatlan darab)",
     "test_tile_produces_no_uncuttable_slivers",
     "    usable, tiny = [], []",
     "    return out\n    usable, tiny = [], []"),

    # A mintázatnak EGYEDINEK kell lennie: ugyanez az őr a `polys()`-ban is ott
    # van, és az első előfordulás cseréje a rossz függvényt mutálta - a
    # `tile_piece` érintetlen maradt, a mutáció mégis "alkalmazva" látszott.
    # Ezért van itt a záró komment is.
    ("csempe: üres bemenet őre törölve (NaN)",
     "test_tile_empty_input",
     "        return []                      # ures bemeneten NaN-t dobott (codex)",
     "        pass                           # ures bemeneten NaN-t dobott (codex)"),

    ("híd: pont-érintkezés iránya (nulla hosszú LineString → üres buffer)",
     "test_bridge_point_touching_pieces",
     "            if a.distance(b) <= 1e-9:",
     "            if False:"),

    ("híd: max_span 'continue' törölve (árva mégis hidalódik)",
     "test_bridge_max_span_reports_orphans",
     "            orphans.append(p)\n            continue\n",
     "            orphans.append(p)\n"),

    ("szöveg: betűnként külön path (a lyukak tömör foltok lesznek)",
     "test_svg_text_keeps_counters_as_holes",
     '    return (f\'  <path d="{" ".join(subs)}" fill="{fill}" \'\n'
     "            'fill-rule=\"evenodd\" stroke=\"none\"/>')",
     '    return "".join(f\'  <path d="{x}" fill="{fill}" fill-rule="evenodd"/>\' for x in subs)'),

    ("szöveg: üres-név őr törölve (matplotlib AttributeError)",
     "test_svg_text_empty_input",
     "    if not name:\n        return []\n",
     ""),

    ("DXF: Y-tükrözés elhagyva (fejjel lefelé gravírozott felirat)",
     "test_dxf_text_flips_y",
     '"20", f"{h - y:.3f}"',
     '"20", f"{y:.3f}"'),

    ("gyógyítás: nem-konvergencia jelzése törölve (néma hiba)",
     "test_heal_reports_when_not_converged",
     "    left = necks(g, min_web)\n    if left:",
     "    left = 0\n    if False:"),

    ("gyógyítás: clip-metszés elhagyva (kilóg a laptáblából)",
     "test_heal_with_clip_stays_inside_the_panel",
     "        if clip is not None:\n            g = snap(g).intersection(snap(clip))\n",
     ""),

    ("drop_specks: lyuk-szűrés elhagyva (1 mm²-es tavat is kivágunk)",
     "test_drop_specks_removes_islands_and_lakes",
     "        holes = [r for r in p.interiors if Polygon(r).area >= min_area]",
     "        holes = list(p.interiors)"),

    ("snap: make_valid elhagyva (GEOS side location conflict)",
     "test_snap_makes_invalid_geometry_usable",
     "    return set_precision(make_valid(geom), grid)",
     "    return set_precision(geom, grid)"),

    ("widest_inscribed: rossz irányú felezés (kétszeres szélesség)",
     "test_widest_inscribed_matches_known_width",
     "        if p.buffer(-mid / 2).is_empty:",
     "        if p.buffer(-mid).is_empty:"),
]


def main():
    original = TARGET.read_text()
    backup = pathlib.Path(tempfile.gettempdir()) / "cutlib_mutation_backup.py"
    backup.write_text(original)

    survivors, skipped = [], []
    try:
        for desc, test, old, new in MUTATIONS:
            if old not in original:
                # A kód elmozdult a mutáció alól. Ezt KI KELL MONDANI: a csendben
                # kihagyott mutáció ugyanaz a hazugság, mint a zöld haszontalan teszt.
                skipped.append(desc)
                print(f"  KIMARAD  {desc}\n           (a mintázat nincs meg a forrásban)")
                continue
            if original.count(old) > 1:
                # Nem egyedi mintazat: a `replace(..., 1)` mas fuggvenyt mutalna.
                skipped.append(desc)
                print(f"  KIMARAD  {desc}\n           (a mintázat {original.count(old)} "
                      f"helyen szerepel — tedd egyedivé)")
                continue
            TARGET.write_text(original.replace(old, new, 1))
            # A `__pycache__` a mutacio NEMA ELLENSEGE: a pyc ervenytelenitese
            # (mtime, meret) parost nez, es a gyors, egyforma meretu ujrairasoknal
            # a pytest a MUTALATLAN kodot futtatta - ket mutacio ezert latszott
            # tulelonek, holott a teszt valojaban elkapta oket.
            shutil.rmtree(TARGET.parent / "__pycache__", ignore_errors=True)
            failed = subprocess.run(
                [PY, "-m", "pytest", f"tests/test_cutlib.py::{test}", "-q"],
                cwd=ROOT, capture_output=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            ).returncode != 0
            print(f"  {'OK  ' if failed else 'BAJ '}     {desc}")
            if not failed:
                survivors.append((desc, test))
    finally:
        TARGET.write_text(original)

    print(f"\n{len(MUTATIONS) - len(survivors) - len(skipped)}/{len(MUTATIONS)} mutáció elbukik.")
    if skipped:
        print(f"{len(skipped)} mutáció nem volt alkalmazható — frissítsd a mintázatokat.")
    for desc, test in survivors:
        print(f"[!] TÚLÉLŐ: {desc}\n    a {test} nem védi meg — a fixture nem hozza létre a hibát")
    return 1 if (survivors or skipped) else 0


if __name__ == "__main__":
    sys.exit(main())
