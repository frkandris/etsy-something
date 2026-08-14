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
            return g
        g = widen_necks(g, min_web, add)
        if clip is not None:
            g = snap(g).intersection(snap(clip))
    # A nev konvergenciat iger; ha max_iter utan MEGSEM sikerult, azt ki kell
    # mondani, nem csendben visszaadni a meg nyakas geometriat (codex).
    left = necks(g, min_web)
    if left:
        print(f"[!] heal_to_convergence: {max_iter} kor utan meg {left} nyak "
              f"maradt - a hivo dolga eldonteni, mi legyen")
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


# --- EGY LAPBOL VAGOTT MU: osszefuggoseg -----------------------------------
# Reteges terméknél a keretet nem ero sziget eldobhato, mert a mogotte levo
# lapon ott az anyag (lasd 02_trace.py --connected). EGY lapbol vagott munal
# ez nem jarhato: ott a darabokat OSSZE KELL KOTNI, kulonben a vago asztalarol
# kulon darabokban jon le. Ez az a kepesseg, ami a reteges lancokbol hianyzik.

def components(geom, min_area=0.0):
    """A geometria kulonallo darabjai, terulet szerint csokkenoen."""
    ps = [p for p in polys(geom) if p.area >= min_area]
    return sorted(ps, key=lambda p: p.area, reverse=True)


def bridge_components(geom, width=2.5, min_area=0.0, anchor=None,
                      max_span=None, min_web=MIN_WEB):
    """A kulonallo darabokat EGY osszefuggo darabba koti hidakkal.

    Minimalis feszitofa a darabok kozott: minden lepesben a mar osszekotott
    halmazhoz LEGKOZELEBBI meg szabad darabot kotjuk be, a ket legkozelebbi
    pontjuk kozott huzott `width` szeles hiddal. Igy a hidak ossz-hossza kicsi,
    es nincs felesleges kereszt-kotes.

    anchor    -- ha meg van adva (pl. keretgyuru), ez a kiindulo halmaz, tehat
                 minden darab hozza kapcsolodik, nem csak egymashoz
    max_span  -- ennel tavolabbi darabot nem kot be (a tul hosszu hid csunya);
                 az ilyen darab kimarad, es a hivo dolga eldonteni, mi legyen
                 vele. A visszaadott masodik ertek ezek listaja.

    Visszaad: (osszekotott_geometria, be_nem_kotott_darabok)
    """
    parts = components(geom, min_area)
    if not parts:
        return geom, []
    from shapely.ops import nearest_points

    if anchor is not None:
        joined, free = [anchor], list(parts)
    else:
        joined, free = [parts[0]], list(parts[1:])
    bridges, orphans = [], []

    while free:
        best = None
        for i, p in enumerate(free):
            for q in joined:
                d = p.distance(q)
                if best is None or d < best[0]:
                    best = (d, i, q)
        d, i, q = best
        p = free.pop(i)
        if max_span is not None and d > max_span:
            orphans.append(p)
            continue
        # d == 0 lehet PUSZTA PONT-ERINTKEZES is (sarok a sarokhoz): azt a
        # unio osszekotottnek mutatja, fizikailag viszont nulla szeles. Ezert
        # hidat epitunk akkor is, ha a ket darab csak erint (codex).
        _touch_only = d <= 1e-9 and p.intersection(q).area <= 1e-12
        if d > 1e-9 or _touch_only:
            a, b = nearest_points(p, q)
            if a.distance(b) <= 1e-9:
                # PONT-ERINTKEZES: a nearest_points ugyanazt a pontot adja, a
                # nulla hosszu LineString buffere pedig URES - az elozo
                # javitasom ezert volt hatastalan (codex). Az iranyt a ket
                # darab kozeppontja adja, es a hidat arra huzzuk at.
                from shapely.geometry import Point as _Pt
                pc, qc = p.representative_point(), q.representative_point()
                dxc, dyc = qc.x - pc.x, qc.y - pc.y
                ln0 = math.hypot(dxc, dyc) or 1.0
                off = max(width, min_web)
                a = _Pt(a.x - dxc / ln0 * off, a.y - dyc / ln0 * off)
                b = _Pt(b.x + dxc / ln0 * off, b.y + dyc / ln0 * off)
            from shapely.geometry import LineString
            # A hid NYULJON BELE mindket darabba. A puszta vegpont-erintes
            # (lapos sapka) nem olvad ossze; a kerek sapka width/2-vel tulnyul,
            # de a nyak-detektor erozioja a gorbult csatlakozasnal meg atvagja.
            # Merve: 2,5 mm-es hid MIN_WEB=2,0 mellett meg nyaknak szamit,
            # 3,0 mm-es mar nem. Fix tulnyulassal a szelesseg szabadon valhat.
            dx, dy = b.x - a.x, b.y - a.y
            ln = math.hypot(dx, dy) or 1.0
            ov = max(width, min_web)          # ennyivel er bele mindket oldalon
            a2 = (a.x - dx / ln * ov, a.y - dy / ln * ov)
            b2 = (b.x + dx / ln * ov, b.y + dy / ln * ov)
            bridges.append(LineString([a2, b2]).buffer(width / 2, cap_style=2))
        joined.append(p)

    keep = [p for p in joined if anchor is None or p is not anchor]
    return unary_union(keep + bridges).buffer(0), orphans


def graticule(panel, step_mm, width=1.2, origin=(0.0, 0.0)):
    """Szelessegi/hosszusagi racs anyagcsikokkent a panelen belul.

    Egy lapbol vagott terkepnel ez a legelegansabb osszekoto halo: egyszerre
    dekoracio es szerkezet - a kontinensek a racson keresztul fuggenek ossze,
    nem kell kulon hidat rajzolni.
    """
    from shapely.geometry import LineString
    mnx, mny, mxx, mxy = panel.bounds
    lines = []
    x = origin[0] + math.ceil((mnx - origin[0]) / step_mm) * step_mm
    while x <= mxx:
        lines.append(LineString([(x, mny), (x, mxy)]))
        x += step_mm
    y = origin[1] + math.ceil((mny - origin[1]) / step_mm) * step_mm
    while y <= mxy:
        lines.append(LineString([(mnx, y), (mxx, y)]))
        y += step_mm
    if not lines:
        return None
    web = unary_union([ln.buffer(width / 2, cap_style=2) for ln in lines])
    return web.intersection(panel).buffer(0)


def tile_piece(geom, max_w, max_h, min_area=25.0):
    """A lezerágynál nagyobb darabot szamozott zonakra vagja.

    A referenciatermek 1325 mm szeles, a legnagyobb egyedi darabja 330x280 mm -
    kulonben nem fer a kis gepekbe. A vagas TENGELYRE MEROLEGES egyenes menten
    megy, mert az illeszkedes igy a legkonnyebb: a vevo egyenes el menten tolja
    ossze a darabokat.

    Visszaad: [(alkatresz, (sor, oszlop)), ...] balrol-jobbra, fentrol-lefele.
    """
    if geom is None or geom.is_empty:
        return []                      # ures bemeneten NaN-t dobott (codex)
    mnx, mny, mxx, mxy = geom.bounds
    nx = max(1, math.ceil((mxx - mnx) / max_w - 1e-9))
    ny = max(1, math.ceil((mxy - mny) / max_h - 1e-9))
    if nx == 1 and ny == 1:
        # KOMPONENSENKENT szurunk, ahogy a csempezett ag is: az osszterulet-
        # vizsgalat atengedett tobb, kulon-kulon kuszob alatti poligonbol allo
        # MultiPolygont (codex)
        keep = [(q, (0, 0)) for q in polys(geom) if q.area >= min_area]
        return keep
    from shapely.geometry import box as _box
    step_x, step_y = (mxx - mnx) / nx, (mxy - mny) / ny
    out = []
    for r in range(ny):
        for c in range(nx):
            cell = _box(mnx + c * step_x, mny + r * step_y,
                        mnx + (c + 1) * step_x, mny + (r + 1) * step_y)
            part = geom.intersection(cell)
            for q in polys(part):
                # A csempezes NEM veszithet anyagot: a csempehataron keletkezo
                # apro fragmentum a darab resze, nem kulonallo sziget. Merve:
                # a min_area itteni alkalmazasa 34 712 mm2-t tuntetett el az
                # azsiai darabbol (codex). A kuszob a BEMENETRE vonatkozik,
                # nem a vagas melléktermékeire.
                out.append((q, (r, c)))
    return out
