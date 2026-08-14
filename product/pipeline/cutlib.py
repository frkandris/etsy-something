"""Közös vágás-geometriai eszközök a réteges termék-láncokhoz.

Ide az kerül, amit egyik láncon **megmértünk**, és a másikon is érvényes. A
termék-specifikus hangolás (küszöbök, stílus, kompozíció) marad a láncokban.

Eddig a papírvágás- (`02_trace.py`) és a világtérkép-lánc (`10_worldmap.py`)
külön tanulta meg ugyanazt; ez a modul az a hely, ahol egy jövőbeli negyedik
termék készen kapja.
"""
import math

from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import make_valid, set_precision

MIN_WEB = 2.0          # mm — a lézer által elviselt legkeskenyebb anyag
SNAP = 0.01            # mm — GEOS-rács a "side location conflict" ellen


def polys(geom):
    """Csak a POLIGONOK. A make_valid és a difference GeometryCollectiont is
    adhat, amiben vonalak és pontok is vannak — azok nem vágandó anyagok."""
    if geom is None or geom.is_empty:
        return []
    if geom.geom_type == "Polygon":
        return [geom]
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        out = []
        for g in geom.geoms:
            out += polys(g)
        return out
    return []


def snap(geom, grid=SNAP):
    """A hajszálvékony élek GEOS 'side location conflict'-ot adnak a
    metszéseknél. A bevált javítás: MINDKÉT operandust ugyanarra a rácsra
    kerekíteni, mielőtt metszünk."""
    return set_precision(make_valid(geom), grid)


def widest_inscribed(p, hi=12.0, iters=16):
    """A darabba írható legszélesebb kör átmérője (mm), felezéssel."""
    lo = 0.0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if p.buffer(-mid / 2).is_empty:
            hi = mid
        else:
            lo = mid
    return lo


def necks(geom, min_web=MIN_WEB, frag_area=20.0):
    """Vékony nyak: ahol min_web/2-vel erodálva a darab több érdemi részre
    esik. A visszaadott szám a szétesések darabszáma, nem a darabok száma."""
    n = 0
    for p in polys(geom):
        er = p.buffer(-min_web / 2)
        if er.is_empty:
            continue
        frags = [f for f in polys(er) if f.area >= frag_area]
        if len(frags) > 1:
            n += len(frags) - 1
    return n


def widen_necks(geom, min_web=MIN_WEB, add=0.45):
    """Lokális kiszélesítés CSAK a nyak-szakaszon.

    Az Epilog ajánlása offset + unió az egész formára, de az mindent hizlal.
    Itt a nyak-zónát számoljuk ki (a darab mínusz a kövér részek), és csak azt
    bufferezzük — így a kontúr karaktere megmarad.
    """
    out = []
    for p in polys(geom):
        er = p.buffer(-min_web / 2)
        frags = [f for f in polys(er) if f.area >= 5.0]
        if len(frags) <= 1:
            out.append(p)
            continue
        fat = unary_union([f.buffer(min_web / 2 + 0.05) for f in frags])
        out.append(p.union(p.difference(fat).buffer(add)).buffer(0))
    return unary_union(out) if out else geom


def heal_to_convergence(geom, clip=None, min_web=MIN_WEB, add=0.45, max_iter=4):
    """Nyak-gyógyítás ISMÉTELVE, amíg el nem fogy.

    A világtérképnél mértük ki, hogy **a klippelés maga gyárt új nyakat**, tehát
    egyetlen gyógyító kör nem elég: a szélesítés utáni újraklippelés megint
    nyakat csinálhat. A megfigyelt minta 1 -> 1 -> 0, vagyis konvergál, de
    ellenőrizni kell. Egy kör után megállni csendes hiba.
    """
    g = geom
    for _ in range(max_iter):
        if necks(g, min_web) == 0:
            break
        g = widen_necks(g, min_web, add)
        if clip is not None:
            g = snap(g).intersection(snap(clip))
    return g


def ghost_outline(pieces, inset=0.5, min_area=4.0):
    """Ragasztási sablon: a darabok kontúrja `inset` mm-rel BELJEBB.

    A fogadó lapra gravírozva maga a lap mondja meg, hova kerül minden darab —
    a vevőnek nem kell külön útmutatót nézegetnie. A beljebb húzás azért kell,
    hogy a felragasztott darab eltakarja a vonalat.

    Üres eredményt sosem ad vissza gravírozandó geometriaként: a túl kicsi
    darabok egyszerűen kimaradnak.
    """
    rings = []
    for p in polys(pieces):
        inner = p.buffer(-inset)
        for q in polys(inner):
            if q.area >= min_area:
                rings.append(q.exterior)
                rings += list(q.interiors)
    return rings


def text_paths(name, x, y, hgt, rot=0.0, family="DejaVu Sans", weight="bold"):
    """Szöveg -> zárt kontúrok (mm), középre igazítva, opcionális forgatással.

    A lézervágók és a Blender SVG-importere sem olvassa a <text> elemet, ezért
    a feliratot útvonallá kell alakítani.
    """
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), name, size=hgt,
                  prop=FontProperties(family=family, weight=weight))
    polysets = tp.to_polygons()
    if not polysets:
        return []
    xs = [pt[0] for poly in polysets for pt in poly]
    w = (max(xs) - min(xs)) if xs else 0.0
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for poly in polysets:
        pts = []
        for px, py in poly:
            dx = px - min(xs) - w / 2
            dy = py - hgt / 2
            pts.append((x + dx * cr - dy * sr, y + dx * sr + dy * cr))
        out.append(pts)
    return out


def text_width(name, hgt, family="DejaVu Sans", weight="bold"):
    """A felirat szélessége mm-ben — a befoglaló darabba illesztéshez."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    return TextPath((0, 0), name, size=hgt,
                    prop=FontProperties(family=family,
                                        weight=weight)).get_extents().width


def svg_text(name, x, y, hgt, h, rot=0.0, fill="#803c14"):
    """A feliratot EGY path-ként adja vissza, evenodd kitöltéssel.

    Betűnként külön path esetén az O, A, R belső lyuka nem lyuk lesz, hanem
    tömör folt — a renderen a szöveg halandzsává mosódik. Egy path + evenodd
    az egyetlen helyes forma.
    """
    subs = []
    for poly in text_paths(name, x, y, hgt, rot):
        subs.append("M " + " L ".join(f"{px:.2f},{h - py:.2f}"
                                      for px, py in poly) + " Z")
    if not subs:
        return None
    return (f'  <path d="{" ".join(subs)}" fill="{fill}" '
            'fill-rule="evenodd" stroke="none"/>')


def dxf_text(name, x, y, hgt, h, rot=0.0):
    """R12 TEXT entitás. Az Y-t H-y alakban írjuk — a vágó-DXF minden
    geometriája így megy, és ha a szöveg kimarad belőle, függőlegesen tükrözve
    gravírozódik. Az 50-es kód a forgatás."""
    return ["0", "TEXT", "8", "ENGRAVE", "10", f"{x:.3f}", "20", f"{h - y:.3f}",
            "40", f"{hgt:.3f}", "50", f"{rot:.1f}", "72", "1",
            "11", f"{x:.3f}", "21", f"{h - y:.3f}", "1", name]


def drop_specks(geom, min_area):
    """Sziget, ami kisebb a küszöbnél, kiesik a lapból — nem vágjuk ki.
    Lyukra ugyanez: egy 1 mm²-es tavat nem érdemes kivágni.
    Visszaadja a megtisztított geometriát és az eldobott darabok számát."""
    keep, dropped = [], 0
    for p in polys(geom):
        if p.area < min_area:
            dropped += 1
            continue
        holes = [r for r in p.interiors if Polygon(r).area >= min_area]
        keep.append(Polygon(p.exterior, holes))
    return (unary_union(keep) if keep else None), dropped
