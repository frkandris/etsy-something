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
import re
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


def test_bridge_corridor_piece_ends_up_connected():
    """A híd útjában fekvő darab összeköttetésbe kerül, pontosan 292,0 mm²-rel.

    NEM fedi a felesleges kereszt-kötés elleni ágat (`cutlib.py` ~293. sor).
    Mérve: az ág törlése után a kimenet **bitre ugyanaz**, 292,00 mm², négy
    különböző fixture-rel (vékony a korridorban / magas / korridoron kívül
    lelógó / széles). A felesleges híd ugyanabban a folyosóban épül, ezért az
    unió elnyeli — az ág teljesítménybeli, nem geometriai.

    Ezt inkább kimondjuk, mint hogy egy laza területkorláttal úgy tegyünk,
    mintha le lenne fedve: az eredeti, `< minimal * 1.35` alakú állításom a
    mutáns 292,0-ját is átengedte (codex).
    """
    a, b = box(0, 0, 10, 10), box(40, 0, 50, 10)
    c = box(22, 4, 26, 6)                     # pont a leendő híd útjában
    joined, _ = cutlib.bridge_components(unary_union([a, b, c]), width=3.0)
    assert len(cutlib.components(joined)) == 1
    assert joined.area == pytest.approx(292.0, abs=0.05)


def test_bridge_max_span_reports_orphans():
    """A túl távoli darab nem hidalódik, hanem árvaként jelentődik.

    A `len(orphans) == 1` önmagában kevés: a `continue` törlése után a darab
    árvaként JELENTŐDIK, de közben mégis hozzáhidalódik (codex). Ezért a
    kimenet területét is rögzítjük — árva esetén csak a 20 × 20-as darab marad.
    """
    far = unary_union([box(0, 0, 20, 20), box(200, 0, 220, 20)])
    joined, orphans = cutlib.bridge_components(far, width=2.5, max_span=50)
    assert len(orphans) == 1
    assert joined.area == pytest.approx(400.0, abs=0.05)


def test_bridge_anchor_is_excluded_from_the_result():
    """Az `anchor` a hidak kiindulópontja, de nem része a visszaadott anyagnak."""
    anchor = box(-30, 0, -10, 20)
    land = unary_union([box(0, 0, 20, 20), box(60, 0, 80, 20)])
    joined, _ = cutlib.bridge_components(land, width=2.5, anchor=anchor)
    assert not joined.intersects(box(-30, 0, -20, 20))


def test_bridge_empty_input():
    """Üres bemeneten a geometria változatlanul, árvák nélkül jön vissza."""
    empty = Polygon()
    joined, orphans = cutlib.bridge_components(empty, width=2.5)
    assert joined.is_empty and orphans == []


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

    A feltételes `assert` az eredeti alakomban azt jelentette, hogy a teszt
    nem-konvergencia hiányában NEM ÁLLÍT SEMMIT. Itt előbb megköveteljük, hogy
    a beállítás tényleg ne konvergáljon, és csak utána nézzük a jelzést.
    Konkrét magyar szórészletre nem kötünk (codex): a jelzés attól jelzés, hogy
    a nyakak számát kimondja.
    """
    thin = unary_union([box(0, 0, 20, 20), box(19, 9.9, 21, 10.1), box(21, 0, 41, 20)])
    out_geom = cutlib.heal_to_convergence(thin, max_iter=1, add=0.001)
    left = cutlib.necks(out_geom)
    assert left, "a fixture konvergált — így a teszt nem mérné a jelzést"
    assert str(left) in capsys.readouterr().out


def test_heal_with_clip_stays_inside_the_panel():
    """A `clip` ág: a gyógyítás nem lóghat ki a laptáblából.

    A klippelés maga gyárt új nyakat — ezért iterál a függvény.
    """
    thin = unary_union([box(0, 0, 20, 20), box(19, 9.5, 21, 10.5), box(21, 0, 41, 20)])
    panel = box(0, 0, 41, 20)
    healed = cutlib.heal_to_convergence(thin, clip=panel)
    assert healed.difference(panel).area == pytest.approx(0.0, abs=1e-6)


# ----------------------------------------------------------- snap / widest / specks

def test_snap_makes_invalid_geometry_usable():
    """A hajszálvékony él GEOS 'side location conflict'-ot ad metszéskor.

    A `snap` mindkét operandust ugyanarra a rácsra kerekíti — a bowtie
    (önmetsző) poligonnak érvényessé kell válnia.
    """
    bowtie = Polygon([(0, 0), (10, 10), (10, 0), (0, 10)])
    assert not bowtie.is_valid
    assert cutlib.snap(bowtie).is_valid


def test_widest_inscribed_matches_known_width():
    """Egy 6 mm széles sávba írható legszélesebb kör átmérője 6 mm."""
    assert cutlib.widest_inscribed(box(0, 0, 100, 6)) == pytest.approx(6.0, abs=0.02)


def test_widest_inscribed_is_capped_by_hi():
    """A felezés a `hi` fölé nem mehet — enélkül végtelen nagy darabot jelentene."""
    assert cutlib.widest_inscribed(box(0, 0, 500, 500), hi=12.0) == pytest.approx(12.0, abs=0.01)


def test_drop_specks_removes_islands_and_lakes():
    """A küszöb alatti sziget ÉS a küszöb alatti lyuk is kiesik."""
    lake = Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])           # 1 mm² tó
    plate = Polygon(box(0, 0, 50, 50).exterior, [lake.exterior])
    speck = box(80, 0, 81, 1)                                  # 1 mm² sziget
    cleaned, dropped = cutlib.drop_specks(unary_union([plate, speck]), min_area=40)
    assert dropped == 1                                        # a sziget
    assert cleaned.area == pytest.approx(2500.0, abs=0.01)     # a tó betemetve
    assert len(cutlib.polys(cleaned)[0].interiors) == 0


def test_drop_specks_returns_none_when_nothing_survives():
    """Ha minden darab a küszöb alatt van, a hívó `None`-t kap, nem üres uniót."""
    cleaned, dropped = cutlib.drop_specks(box(0, 0, 2, 2), min_area=40)
    assert cleaned is None and dropped == 1


def test_text_width_grows_with_the_string():
    """A szélesség a befoglaló darabba illesztéshez kell — hosszabb név szélesebb."""
    assert cutlib.text_width("MEXICO", 4.0) > cutlib.text_width("PERU", 4.0) > 0


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

def test_svg_text_keeps_counters_as_holes():
    """REGRESSZIÓ: az „O" belső lyuka lyuk maradjon, ne tömör folt.

    A renderen ettől lett a felirat halandzsa. Az eredeti állításom
    (`d.count("<path") == 1`) az IMPLEMENTÁCIÓT rögzítette: a betűnkénti,
    de saját `evenodd`-dal ellátott path vizuálisan ugyanúgy helyes lenne,
    mégis eltörte volna (codex). A viselkedés az, ami számít: a két gyűrűnek
    UGYANABBAN a path-elemben kell lennie, `evenodd` kitöltéssel.
    """
    d = cutlib.svg_text("O", 10, 10, 4, 100)
    tags = re.findall(r"<path[^>]*>", d)
    holders = [t for t in tags if t.count("M ") >= 2]
    assert len(holders) == 1, "a külső és a belső gyűrű nem egy path-ban van"
    assert 'fill-rule="evenodd"' in holders[0]


def test_svg_text_empty_input():
    """Üres feliratból nincs path — a hívó ezt `None`-ként várja."""
    assert cutlib.svg_text("", 10, 10, 4, 100) is None


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


def test_graticule_stays_inside_the_panel():
    """A rács nem lóghat túl a lapon — a metszés a panelre szorítja.

    Az eredeti állításom itt `None`-t várt egy rácsköznél kisebb panelen; a
    valóság az, hogy az origóra illesztett vonalak akkor is beleesnek, és egy
    sarok-hálót adnak. A `not lines` ág a gyakorlatban nem érhető el.
    """
    panel = box(0, 0, 400, 200)
    web = cutlib.graticule(panel, step_mm=40, width=1.2)
    assert web.difference(panel).area == pytest.approx(0.0, abs=1e-6)
