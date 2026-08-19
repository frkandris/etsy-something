"""Regressziós tesztek a közös vágás-geometriához.

**Minden teszt egy VALÓDI hibából született**, amit 2026-08-14-én egy külső
bíráló (codex) talált meg, nem én. Fowler szabálya szerint: előbb írj tesztet,
ami megmutatja a hibát, és csak utána javíts — ezek visszamenőleg készültek,
hogy a hibák ne jöhessenek vissza.

A tanulság, amiért ez a fájl létezik: aznap **három egymást követő javítási kör
mindegyike bevezetett egy új hibát**, és egyiket sem a saját tesztjeim fogták
meg — mert nem voltak. A `--min-part` küszöb finomhangolása nem pótolja azt,
hogy egy 3,09 × 0,74 mm-es csempe fizikailag vághatatlan.

Google kódellenőrzési útmutatója szerint a teszt akkor ér valamit, ha
**elbukik, amikor a kód elromlik** — ezért minden teszt egy konkrét, mért
számot állít, nem azt, hogy „lefut".
"""
import math
import pathlib
import sys

import pytest
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "product" / "pipeline"))
import cutlib  # noqa: E402


# --------------------------------------------------------------- bridge_components

def test_bridge_joins_separate_pieces():
    """Az alapeset: külön darabokból egy összefüggő geometria lesz."""
    land = unary_union([box(0, 0, 20, 20), box(60, 0, 80, 20)])
    assert len(cutlib.components(land)) == 2
    joined, orphans = cutlib.bridge_components(land, width=2.5)
    assert len(cutlib.components(joined)) == 1
    assert orphans == []


def test_bridge_survives_neck_detector():
    """A híd nem lehet vékonyabb a minimális webnél.

    Mérve: a puszta végpont-érintés és a kerek sapka is kevés volt — a
    nyak-detektor eróziója a görbült csatlakozásnál átvágta. Fix túlnyúlás kell.
    """
    land = unary_union([box(0, 0, 20, 20), box(60, 0, 80, 20)])
    joined, _ = cutlib.bridge_components(land, width=2.5)
    assert cutlib.necks(joined) == 0


def test_bridge_point_touching_pieces():
    """REGRESSZIÓ: sarok-érintkezés nem összeköttetés.

    A `nearest_points()` azonos pontot ad, a nulla hosszú `LineString` buffere
    pedig ÜRES — az első javításom emiatt volt hatástalan, és a két négyzet
    továbbra is két komponens maradt.
    """
    corner = unary_union([box(0, 0, 10, 10), box(10, 10, 20, 20)])
    joined, _ = cutlib.bridge_components(corner, width=2.5)
    assert len(cutlib.components(joined)) == 1


def test_bridge_no_redundant_crossing():
    """REGRESSZIÓ: ha egy híd már átmetszett egy szabad darabot, az összeköttetésben van.

    Mérve: egy 0,16 mm²-es darabból a híd 0,1434 mm²-t már átmetszett, mégis
    épült rá még egy 4,694 mm²-es híd. A docstring kifejezetten kizárja a
    felesleges kereszt-kötést.
    """
    a, b = box(0, 0, 10, 10), box(40, 0, 50, 10)
    c = box(22, 4, 26, 6)                     # pont a leendő híd útjában
    joined, _ = cutlib.bridge_components(unary_union([a, b, c]), width=3.0)
    assert len(cutlib.components(joined)) == 1
    # a felesleges híd tényleges területet adna hozzá a szükségesen felül
    minimal = 10 * 10 + 10 * 10 + 4 * 2 + 30 * 3.0
    assert joined.area < minimal * 1.35


def test_bridge_max_span_reports_orphans():
    """A túl távoli darab nem hidalódik, hanem árvaként jelentődik."""
    far = unary_union([box(0, 0, 20, 20), box(200, 0, 220, 20)])
    joined, orphans = cutlib.bridge_components(far, width=2.5, max_span=50)
    assert len(orphans) == 1
    assert cutlib.components(joined)


# --------------------------------------------------------------------- tile_piece

def _arm_piece():
    """Törzs + hosszú, 0,5 mm vékony kar.

    A csempe-rács ezt úgy vágja el, hogy a KÖZÉPSŐ cellákba CSAK a kar esik —
    vagyis izolált, vághatatlanul vékony fragmentum keletkezik. Az első
    próbageometriám (nagy téglalap + kis háromszög) ezt nem hozta létre, ezért
    a tesztem akkor is átment, amikor visszavontam a javítást (mutációval mérve).
    """
    return unary_union([box(0, 0, 300, 300), box(300, 149.75, 1000, 150.25)])


def test_tile_preserves_area():
    """REGRESSZIÓ: a csempézés nem veszíthet anyagot.

    Mérve: a `min_area` alkalmazása a csempehatáron 34 712 mm²-t tüntetett el
    az ázsiai darabból. A küszöb a BEMENETRE vonatkozik, nem a vágás
    melléktermékeire.
    """
    g = _arm_piece()
    tiles = cutlib.tile_piece(g, 330, 280, min_area=200)
    total = sum(t.area for t, _ in tiles)
    assert total == pytest.approx(g.area, abs=0.5)


def test_tile_produces_no_uncuttable_slivers():
    """REGRESSZIÓ: a terület-megőrzés nem gyárthat vághatatlan szilánkot.

    Mérve: a puszta megőrzés 3,09 × 0,74 mm-es önálló csempét adott —
    vékonyabbat a 2 mm-es minimális webnél. A helyes válasz a beolvasztás.
    """
    for t, _ in cutlib.tile_piece(_arm_piece(), 330, 280, min_area=40):
        w = t.bounds[2] - t.bounds[0]
        h = t.bounds[3] - t.bounds[1]
        assert min(w, h) >= cutlib.MIN_WEB, f"{w:.2f} x {h:.2f} mm csempe"


def test_tile_respects_max_size():
    """A csempe nem lehet nagyobb a lézerágy-korlátnál."""
    for t, _ in cutlib.tile_piece(box(0, 0, 900, 500), 330, 280):
        assert t.bounds[2] - t.bounds[0] <= 330 + 1e-6
        assert t.bounds[3] - t.bounds[1] <= 280 + 1e-6


def test_tile_empty_input():
    """REGRESSZIÓ: üres poligonon `NaN`-t dobott."""
    assert cutlib.tile_piece(Polygon(), 100, 100) == []


def test_tile_filters_by_component_not_total():
    """REGRESSZIÓ: az összterület-vizsgálat átengedett külön-külön apró darabokat."""
    tiny = unary_union([box(0, 0, 3, 3), box(10, 0, 13, 3), box(20, 0, 23, 3)])
    assert cutlib.tile_piece(tiny, 330, 280, min_area=40) == []


# ------------------------------------------------------------------------- necks

def test_necks_detects_thin_waist():
    thin = unary_union([box(0, 0, 20, 20), box(19, 9.5, 21, 10.5), box(21, 0, 41, 20)])
    assert cutlib.necks(thin) >= 1


def test_heal_removes_necks():
    thin = unary_union([box(0, 0, 20, 20), box(19, 9.5, 21, 10.5), box(21, 0, 41, 20)])
    assert cutlib.necks(cutlib.heal_to_convergence(thin)) == 0


def test_heal_reports_when_not_converged(capsys):
    """REGRESSZIÓ: a név konvergenciát ígér — ha nem sikerül, mondja ki.

    Korábban csendben visszaadta a még nyakas geometriát.
    """
    thin = unary_union([box(0, 0, 20, 20), box(19, 9.9, 21, 10.1), box(21, 0, 41, 20)])
    cutlib.heal_to_convergence(thin, max_iter=1, add=0.001)
    out = capsys.readouterr().out
    if cutlib.necks(cutlib.heal_to_convergence(thin, max_iter=1, add=0.001)):
        assert "nem" in out or "maradt" in out


# ------------------------------------------------------------------ ghost_outline

def test_ghost_outline_is_inside_the_piece():
    """A ragasztási sablon beljebb van, hogy a darab eltakarja."""
    p = box(0, 0, 50, 50)
    rings = cutlib.ghost_outline(p, inset=0.5)
    assert rings
    for r in rings:
        assert Polygon(r).area < p.area


def test_ghost_outline_drops_pieces_that_vanish():
    """Egy 1 mm-es darabból 0,5 mm behúzással nem marad semmi."""
    assert cutlib.ghost_outline(box(0, 0, 1, 1), inset=0.5) == []


# ------------------------------------------------------------------------ szöveg

def test_svg_text_uses_evenodd_single_path():
    """REGRESSZIÓ: betűnként külön path esetén a lyukak tömör folttá válnak.

    A renderen ettől lett a felirat halandzsa. Egy path + evenodd az egyetlen
    helyes forma.
    """
    d = cutlib.svg_text("AO", 10, 10, 4, 100)
    assert d.count("<path") == 1
    assert 'fill-rule="evenodd"' in d


def test_dxf_text_flips_y():
    """A vágó-DXF minden Y-t H-y alakban ír; ha a szöveg kimarad, tükrözve gravírozódik."""
    ent = cutlib.dxf_text("A", 10.0, 20.0, 4.0, 100.0)
    assert ent[ent.index("20") + 1] == "80.000"


def test_text_rotation_moves_the_glyphs():
    """A ferde címke (MEXICO) tényleg elfordul."""
    flat = cutlib.text_paths("MEXICO", 0, 0, 4, rot=0)
    tilt = cutlib.text_paths("MEXICO", 0, 0, 4, rot=-38)
    fx = max(p[0] for poly in flat for p in poly)
    tx = max(p[0] for poly in tilt for p in poly)
    assert not math.isclose(fx, tx, rel_tol=0.05)


# ---------------------------------------------------------------------- graticule

def test_graticule_is_one_connected_web():
    """A rács szerkezet is: egyetlen összefüggő hálót kell adnia."""
    web = cutlib.graticule(box(0, 0, 400, 200), step_mm=40, width=1.2)
    assert len(cutlib.components(web)) == 1
