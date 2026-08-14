#!/usr/bin/env python3
"""Réteges 3D világtérkép lézervágáshoz — a lánc harmadik változata.

Miben más ez, mint a papírvágás-lánc: **itt nincs képgenerátor**. A mélységet nem
becsülni kell, mert méréssel adott. A Natural Earth batimetria-kontúrjai
(0, 200, 1000 ... 10000 m) természetüknél fogva **egymásba ágyazottak** — pontosan
az a szerkezet, amit a papíros láncban k-means-szel és nyakgyógyítással kellett
előállítani. A szárazföld a legfelső lap, alatta a tenger lépcsőzik lefelé.

  szárazföld            = legfelső lap
  0-200 m               = egy lépcsővel lejjebb
  200-1000 m            = kettővel
  ...
  a legmélyebb kontúr   = a hátlap

Adat: Natural Earth (naturalearthdata.com), **közkincs** — kereskedelmi
felhasználás korlátozás nélkül, attribúció nem kötelező. A letöltés a
nvkelso/natural-earth-vector GitHub-tükörről megy, mert a hivatalos CDN
megbízhatatlan.

  python 10_worldmap.py --out <dir> [--width 400] [--levels 0,200,1000,3000,6000]

Kimenet: rétegenként SVG és DXF, gravírozási réteg az országhatárokkal, és a
papíros lánccal azonos formátumú vágásbiztonsági riport.
"""
import argparse, json, math, pathlib, urllib.request, sys
from shapely.geometry import shape, Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity, make_valid, set_precision

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson"
CACHE = pathlib.Path(__file__).resolve().parent / "geodata"

# mélységszint -> Natural Earth fájlnév. A betű a fájlban a mélységsorrend.
BATHY = {0: "ne_10m_bathymetry_L_0", 200: "ne_10m_bathymetry_K_200",
         1000: "ne_10m_bathymetry_J_1000", 2000: "ne_10m_bathymetry_I_2000",
         3000: "ne_10m_bathymetry_H_3000", 4000: "ne_10m_bathymetry_G_4000",
         5000: "ne_10m_bathymetry_F_5000", 6000: "ne_10m_bathymetry_E_6000",
         7000: "ne_10m_bathymetry_D_7000", 8000: "ne_10m_bathymetry_C_8000",
         9000: "ne_10m_bathymetry_B_9000", 10000: "ne_10m_bathymetry_A_10000"}

MIN_WEB = 2.0          # mm — a lézer által elviselt legkeskenyebb anyag
MIN_ISLAND = 25.0      # mm² — ennél kisebb sziget kiesik a lapból, nem vágjuk ki


def fetch(name):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{name}.geojson"
    if not p.exists():
        print(f"[geo] letöltés: {name}")
        urllib.request.urlretrieve(f"{NE}/{name}.geojson", p)
    return json.loads(p.read_text())


def geoms_of(gj):
    out = []
    for f in gj.get("features", []):
        try:
            g = shape(f["geometry"])
        except Exception:
            continue
        if not g.is_valid:
            g = make_valid(g)
        if g.geom_type in ("Polygon", "MultiPolygon"):
            out.append(g)
    return unary_union(out) if out else None


def miller(lon, lat):
    """Miller cylindrical. A referenciatermék arányai ehhez állnak legközelebb:
    a plate carrée túl nyújtott sarkú, a Robinson ívelt széle pedig nem fér
    téglalap keretbe."""
    y = 1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(lat)))
    return lon, math.degrees(y)


def project(geom, lat_min, lat_max):
    """Vágás szélességi körre, majd Miller-vetítés. A vetítés pontonként megy,
    ezért a vágást ELŐBB kell elvégezni, különben a pólusok végtelenbe futnak."""
    clip = box(-180, lat_min, 180, lat_max)
    g = geom.intersection(clip)
    if g.is_empty:
        return g

    def tx(x, y, z=None):
        return miller(x, y)

    from shapely.ops import transform
    return transform(tx, g)


def polys(geom):
    """Csak a POLIGONOK. A make_valid és a difference GeometryCollectiont is adhat,
    amiben vonalak és pontok is vannak — azok nem vágandó anyagok."""
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


def drop_specks(geom, min_area):
    """Sziget, ami kisebb a küszöbnél, kiesik a lapból — nem vágjuk ki.
    Lyukra ugyanez: egy 1 mm²-es tavat nem érdemes kivágni."""
    parts = polys(geom)
    keep = []
    dropped = 0
    for p in parts:
        if p.area < min_area:
            dropped += 1
            continue
        holes = [r for r in p.interiors if Polygon(r).area >= min_area]
        keep.append(Polygon(p.exterior, holes))
    return (unary_union(keep) if keep else None), dropped


def widest_inscribed(p):
    lo, hi = 0.0, 12.0
    for _ in range(16):
        mid = (lo + hi) / 2
        if p.buffer(-mid / 2).is_empty:
            hi = mid
        else:
            lo = mid
    return lo


def widen_necks(geom, add=0.45):
    """Lokalis kiszelesites CSAK a nyak-szakaszon (Epilog-ajanlas: offset ~0,5 mm
    es unio - de mi nem az egesz format hizlaljuk, csak a nyak-zonat, igy a
    kontur karaktere marad). A nyak-zona: a darab minusz a kover reszek."""
    out = []
    for p in polys(geom):
        er = p.buffer(-MIN_WEB / 2)
        frags = [f for f in polys(er) if f.area >= 5.0]
        if len(frags) <= 1:
            out.append(p)
            continue
        fat = unary_union([f.buffer(MIN_WEB / 2 + 0.05) for f in frags])
        neck_zone = p.difference(fat)
        widened = p.union(neck_zone.buffer(add)).buffer(0)
        out.append(widened)
    return unary_union(out)


def necks(geom):
    """Vékony nyak: ahol MIN_WEB/2-vel erodálva a darab több érdemi részre esik."""
    n = 0
    for p in polys(geom):
        er = p.buffer(-MIN_WEB / 2)
        if er.is_empty:
            continue
        frags = [f for f in (er.geoms if er.geom_type == "MultiPolygon" else [er])
                 if f.area >= 20.0]
        if len(frags) > 1:
            n += len(frags) - 1
    return n


def to_svg(geom, w, h, path, stroke_only=False):
    def ring(coords):
        return "M " + " L ".join(f"{x:.3f},{h - y:.3f}" for x, y in coords) + " Z"
    parts = list(geom.geoms) if geom.geom_type in ("MultiPolygon", "MultiLineString") else [geom]
    d = []
    for p in parts:
        if p.geom_type == "LineString":
            d.append("M " + " L ".join(f"{x:.3f},{h - y:.3f}" for x, y in p.coords))
            continue
        d.append(ring(p.exterior.coords))
        for r in p.interiors:
            d.append(ring(r.coords))
    style = ('fill="none" stroke="#f00" stroke-width="0.1"' if stroke_only
             else 'fill="#000" fill-rule="evenodd"')
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}mm" height="{h:.2f}mm" '
        f'viewBox="0 0 {w:.3f} {h:.3f}">\n  <path {style} d="{" ".join(d)}"/>\n</svg>\n')


def to_dxf(geom, h, path):
    """R12 poliline — ezt minden lézervágó szoftver beolvassa."""
    out = ["0", "SECTION", "2", "ENTITIES"]
    parts = list(geom.geoms) if geom.geom_type in ("MultiPolygon", "MultiLineString") else [geom]
    for p in parts:
        rings = ([p.coords] if p.geom_type == "LineString"
                 else [p.exterior.coords] + [r.coords for r in p.interiors])
        for r in rings:
            pts = list(r)
            out += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
            for x, y in pts:
                out += ["0", "VERTEX", "8", "0", "10", f"{x:.4f}", "20", f"{h - y:.4f}"]
            out += ["0", "SEQEND"]
    out += ["0", "ENDSEC", "0", "EOF"]
    path.write_text("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=float, default=400.0, help="mm, a kész tábla szélessége")
    ap.add_argument("--style", choices=["bathy", "ripple"], default="ripple",
                    help="ripple: part-parhuzamos, simitott hullamsavok (a referencia "
                         "stilusa - nem valosaghu, de sokkal szebb); bathy: valodi "
                         "Natural Earth melysegkonturok")
    ap.add_argument("--ripple-dists", default="5,11,18,27,38",
                    help="mm - a hullamsavok tavolsaga a parttol, a legbelsotol")
    ap.add_argument("--levels", default="200,1000,2000,4000,6000",
                    help="tengermélység-lépcsők méterben, a legsekélyebbtől. "
                         "A 0 m-t NE add meg: a 0 m-es kontúr maga a partvonal, "
                         "tehát a lapja azonos a szárazföld lapjával.")
    ap.add_argument("--thicken", type=float, default=0.0,
                    help="mm — szorosok és földnyelvek zárása. A Panama- és a "
                         "Szuezi-földszoros 400 mm-es táblán 2 mm alatti; enélkül "
                         "a szárazföld lap nyakas marad.")
    ap.add_argument("--lat", default="-58,80", help="szélességi vágás (dél,észak)")
    ap.add_argument("--margin", type=float, default=12.0, help="mm keretsáv")
    ap.add_argument("--simplify", type=float, default=0.25,
                    help="mm — a partvonal egyszerűsítése; a lézer alatta úgysem követi")
    ap.add_argument("--min-island", type=float, default=MIN_ISLAND)
    ap.add_argument("--borders", action="store_true", help="országhatár gravírozási réteg")
    ap.add_argument("--countries", action="store_true",
                    help="a szárazföld lap ország-darabokra bontva, gravírozott nevekkel")
    ap.add_argument("--label-h", type=float, default=3.0,
                    help="mm — gravírozott betűmagasság; ez dönti el, hány ország címkézhető")
    a = ap.parse_args()

    lat_min, lat_max = (float(v) for v in a.lat.split(","))
    levels = sorted(int(v) for v in a.levels.split(","))
    if 0 in levels:
        sys.exit("a 0 m-es szint azonos a szárazfölddel — hagyd ki a --levels listából")
    for lv in levels:
        if lv not in BATHY:
            sys.exit(f"nincs {lv} m-es Natural Earth kontúr; elérhető: {sorted(BATHY)}")

    print(f"[geo] Miller-vetítés, {lat_min}..{lat_max} szélesség, {a.width:.0f} mm széles tábla")

    land = project(geoms_of(fetch("ne_10m_land")), lat_min, lat_max)
    seas = ({lv: project(geoms_of(fetch(BATHY[lv])), lat_min, lat_max) for lv in levels}
            if a.style == "bathy" else {})

    # közös lépték: minden réteg UGYANAZZAL a transzformációval, különben nem illeszkednek
    # ripple modban nincs tenger-kontur: a leptek a szarazfoldbol jon,
    # a savok ugyis a partbol szarmaznak
    ref_geom = land if a.style == "ripple" else land.union(seas[levels[0]])
    mnx, mny, mxx, mxy = ref_geom.bounds
    sc = (a.width - 2 * a.margin) / (mxx - mnx)
    H = (mxy - mny) * sc + 2 * a.margin

    def place(g):
        # ELŐBB az origóba, AZTÁN skálázni. A scale(origin=(mnx,mny)) a pontot a
        # helyén hagyja, tehát a térkép a -180..180 tartományban maradt volna, és
        # a panelnek csak a jobb fele fedte volna — a nyugati féltekét levágta.
        g = affinity.translate(g, -mnx, -mny)
        g = affinity.scale(g, xfact=sc, yfact=sc, origin=(0, 0))
        return affinity.translate(g, a.margin, a.margin)

    land = place(land)
    seas = {k: place(v) for k, v in seas.items()}
    panel = box(0, 0, a.width, H)

    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    # a regi lapok kitakaritasa: egy korabbi, mas --levels futas fajljai kulonben
    # bennmaradnak, es a renderelo egy kevert keszletet olvas be
    for old in (list(out.glob("layer_*.svg")) + list(out.glob("layer_*.dxf"))
                + list(out.glob("engrave_*.svg")) + list(out.glob("engrave_*.dxf"))):
        old.unlink()

    # A lapok: a legfelső a szárazföld, alatta minden lépcsővel nagyobb a MEGMARADÓ
    # anyag, mert a mélyebb víz nyílása kisebb. Ez a papíros lánc süllyesztett
    # szerkezetének a fordítottja: ott a mező volt a felső lap, itt a szárazföld.
    if a.countries:
        # FOK-TERBEN polygonize-olunk, es a kesz lapokat vetitjuk. Merve:
        # fok-terben a lapok a szarazfold 92%-at fedik; mm-terben (vetites es
        # place utan) ugyanez a lanc a 11%-at adta - a nagy koordinatak es a
        # racsra pattintas tori a gyuruzarast.
        from shapely.ops import polygonize
        from shapely.algorithms.polylabel import polylabel as _plabel
        gj = fetch("ne_10m_admin_0_countries")
        land_deg = geoms_of(fetch("ne_10m_land")).intersection(box(-180, lat_min, 180, lat_max))
        borders_deg, country_geoms = [], []
        for f in gj.get("features", []):
            try:
                g = shape(f["geometry"])
            except Exception:
                continue
            if not g.is_valid:
                g = make_valid(g)
            g = g.intersection(box(-180, lat_min, 180, lat_max))
            if g.is_empty:
                continue
            name = (f.get("properties", {}) or {}).get("NAME", "")
            country_geoms.append((name, g))
            borders_deg.append(g.boundary)
        linework = unary_union([land_deg.boundary] + borders_deg)
        faces = list(polygonize(linework))
        min_island_deg = a.min_island / (( (a.width - 2*a.margin) / 360.0 ) ** 2)  # mm2 -> deg2 kozelites
        pieces = []
        for q in faces:
            if q.intersection(land_deg).area < q.area * 0.5:
                continue
            pm = place(project(q, lat_min, lat_max))
            pm = pm.simplify(a.simplify * 0.6).buffer(-0.05).buffer(0)
            if not pm.is_empty and pm.area >= a.min_island:
                pieces.extend(polys(pm))
        labels = []
        land_snap = set_precision(land.buffer(0), 0.01)
        for name, g in country_geoms:
            gp = set_precision(place(project(g, lat_min, lat_max)), 0.01)
            gp = gp.intersection(land_snap)
            big = max(polys(gp), key=lambda x: x.area, default=None)
            if big is None:
                continue
            r = widest_inscribed(big) / 2
            if name and r >= a.label_h * 0.72 and big.area >= 150:
                c = _plabel(big, tolerance=0.5)
                hgt = min(a.label_h, r * 0.9)
                # a nev SZELESSEGE is ferjen bele a darabba (codex: a
                # DEM. REP. CONGO 22,5 mm volt egy 19,9 mm-es orszagon)
                from matplotlib.textpath import TextPath as _TP
                from matplotlib.font_manager import FontProperties as _FP
                _t = _TP((0, 0), name.upper(), size=hgt,
                         prop=_FP(family="DejaVu Sans", weight="bold"))
                tw = _t.get_extents().width
                bw = big.bounds[2] - big.bounds[0]
                if tw > bw * 0.85:
                    hgt *= (bw * 0.85) / tw
                if hgt < 2.2:
                    # a 1.6 mm-es kuszob alatt a betu a renderen halandzsava
                    # mosodott (reviewer) - inkabb nincs cimke, mint olvashatatlan
                    continue
                labels.append((name.upper(), c.x, c.y, hgt))
        print(f"[i] orszag-darabok (polygonize, fok-terben): {len(pieces)}, cimkezheto: {len(labels)}")
        land_cut = MultiPolygon(pieces)
        print(f"[i] orszag-lapok ossz-terulete: {sum(x.area for x in pieces):,.0f} mm2 (teljes szarazfold: {land.area:,.0f})")
    else:
        land_cut, labels = None, []

    sheets = []
    sheets.append(("szárazföld",
                   land_cut if (a.countries and land_cut is not None) else land))
    if a.style == "ripple":
        # A referencia vize NEM valosaghu: part-parhuzamos, lagyan hullamzo
        # savok. Ugyanez itt: a szarazfold novekvo buffere, erosen lekerekitve.
        # A savok konstrukcio szerint egymasba agyazottak.
        dists = sorted(float(v) for v in a.ripple_dists.split(","))
        # a savokhoz nem kell a teljes felbontasu partvonal - ugyis 5-18 mm-es
        # simitas jon ra. A simplify(1.2) 20x-os gyorsulas, lathatatlan aron.
        land_rip = land.simplify(1.2).buffer(0)
        for d in dists:
            # a reviewer az elso korben amorfnak latta a savokat: a 4.5+0.35d
            # simitas (a 38 mm-es savon 18 mm) mar elmosta a part-parhuzamot.
            # Kisebb sugar: a sav kovesse a partot, csak a zajt vegye le.
            r = 2.5 + d * 0.18
            band = land_rip.buffer(d, join_style=1)
            band = band.buffer(r, join_style=1).buffer(-r, join_style=1)
            band = band.simplify(0.8).intersection(panel).buffer(0)
            sheets.append((f"part+{d:g}mm", band.union(land)))
    else:
        for lv in levels:
            sheets.append((f"{lv} m", panel.difference(seas[lv]).union(land)))
    sheets.append(("hátlap", panel))
    sheets.reverse()          # 1. lap = a hatlap, N. = szárazföld

    # BEÁGYAZÁS KIKÉNYSZERÍTÉSE. A Natural Earth kontúrjai elvben egymásba
    # ágyazottak, a gyakorlatban nem: a 200 m-es lap területe nagyobb lett, mint
    # az 1000 m-esé, tehát a k. lap NEM fért bele a k-1.-be. Ha ezt nem javítjuk,
    # a fizikai stackben az egyik lap kilóg a másik alól. Ugyanaz a lépés, mint a
    # papírvágás-láncban: minden lapot a mögötte lévőre klippelünk.
    fixed = [(sheets[0][0], set_precision(make_valid(sheets[0][1]), 0.01))]
    for name, g in sheets[1:]:
        # snap mindket oldalra: a 167 darabos orszag-lap hajszal-elei GEOS
        # side-location-conflictot adtak a klippelesnel
        g = set_precision(make_valid(g), 0.01)
        clipped = g.intersection(fixed[-1][1])
        if not (a.countries and name == "szárazföld"):
            # a klippeles uj nyakat gyart, a szelesites utani klippeles megint
            # - a codex merte ki, hogy konvergal (1 -> 1 -> 0), tehat iteralunk
            for _ in range(4):
                if necks(clipped) == 0:
                    break
                clipped = widen_necks(clipped)
                clipped = set_precision(make_valid(clipped), 0.01).intersection(fixed[-1][1])
        if clipped.area < g.area * 0.999:
            print(f"[i] {name}: beágyazásra klippelve "
                  f"({(1 - clipped.area / g.area) * 100:.1f}% lógott ki)")
        fixed.append((name, clipped))
    sheets = fixed

    rows = []
    final_land = None
    for i, (name, g) in enumerate(sheets, 1):
        is_pieces = (a.countries and name == "szárazföld")
        g = set_precision(make_valid(g), 0.001)
        if not is_pieces:
            g = g.simplify(a.simplify)
        if a.thicken > 0 and not (a.countries and name == "szárazföld"):
            # zárás: a nyak összeforr, a forma mérete lényegében marad.
            # Az orszag-darabos lapra TILOS: a zaras a szomszedos orszagokat
            # a kozos hatar menten osszehegeszti, es megint egy tomb lenne.
            g = g.buffer(a.thicken).buffer(-a.thicken * 0.72)
        if not is_pieces:
            # a keretsáv a TENGER-lapokon anyag: egyben tartja a lapot. Az
            # orszag-darabok lapjára NEM kerül: a referencián a darabok
            # szabadon állnak, az alattuk lévő lapra ragasztva.
            g = g.union(panel.difference(box(a.margin, a.margin, a.width - a.margin, H - a.margin)))
        g, dropped = drop_specks(g, a.min_island)
        if g is None:
            print(f"[!] {i}. lap ({name}) üres")
            continue
        parts = polys(g)
        if not parts:
            print(f"[!] {i}. lap ({name}) üres a tisztítás után")
            continue
        frail = min(widest_inscribed(p) for p in parts)
        nk = necks(g)
        rows.append((i, name, len(parts), sum(len(p.interiors) for p in parts),
                     g.area, frail, nk, dropped))
        tag = name.replace(" ", "")
        if is_pieces:
            final_land = g
        to_svg(g, a.width, H, out / f"layer_{i}_of_{len(sheets)}.svg")
        to_dxf(g, H, out / f"layer_{i}_of_{len(sheets)}_{tag}.dxf")

    if a.borders:
        # ORSZÁGONKÉNT kell a határvonal. Az unary_union összeolvasztja a
        # szomszédos országokat, és pont a belső határok tűnnek el - az egész
        # gravírozási réteg 2 mm hosszú lett tőle.
        gj = fetch("ne_10m_admin_0_countries")
        bl = []
        for f in gj.get("features", []):
            try:
                g = shape(f["geometry"])
            except Exception:
                continue
            if not g.is_valid:
                g = make_valid(g)
            g = project(g, lat_min, lat_max)
            if g.is_empty:
                continue
            for q in polys(g):
                bl.append(place(q).boundary)
        lines = unary_union(bl)
        # a partvonalat nem gravírozzuk: az úgyis vágásél
        lines = lines.difference(land.boundary.buffer(0.4)).intersection(land)
        lines = lines.simplify(a.simplify)
        to_svg(lines, a.width, H, out / "engrave_borders.svg", stroke_only=True)
        to_dxf(lines, H, out / "engrave_borders.dxf")
        print(f"[i] gravírozási réteg: országhatárok ({lines.length:.0f} mm vonalhossz)")

    def text_paths(name, x, y, hgt):
        """Szoveg -> zart konturok (mm), kozepre igazitva."""
        from matplotlib.textpath import TextPath
        from matplotlib.font_manager import FontProperties
        tp = TextPath((0, 0), name, size=hgt,
                      prop=FontProperties(family="DejaVu Sans", weight="bold"))
        polysets = tp.to_polygons()
        if not polysets:
            return []
        xs = [pt[0] for poly in polysets for pt in poly]
        w = max(xs) - min(xs) if xs else 0
        out = []
        for poly in polysets:
            out.append([(x - w / 2 + px - min(xs), y - hgt / 2 + py) for px, py in poly])
        return out

    if a.countries and labels:
        # SVG szoveg-elemek: a LightBurn es a Glowforge is olvassa; a DXF-be
        # R12 TEXT entitasok mennek ugyanazokkal a pozíciókkal
        txt = ['<svg xmlns="http://www.w3.org/2000/svg" '
               f'width="{a.width:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {a.width:.3f} {H:.3f}">']
        def emit_text(name, x, y, hgt, sw="0.08"):
            # EGY path, minden kontur alutvonalkent: kulon path-onkent a betuk
            # lyuk-konturjai (O, A, R belseje) tomor foltta valtak, es a
            # graviro nagyitasban halandzsanak olvasodott (reviewer)
            subs = []
            for poly in text_paths(name, x, y, hgt):
                subs.append("M " + " L ".join(f"{px:.2f},{H - py:.2f}"
                                              for px, py in poly) + " Z")
            if subs:
                txt.append(f'  <path d="{" ".join(subs)}" fill="#803c14" '
                           'fill-rule="evenodd" stroke="none"/>')
        for name, x, y, hgt in labels:
            emit_text(name, x, y, hgt)
        # cimtabla kozepre alul. Iranytu NINCS tobbe: a szelen ulve a paszpartu
        # levagta, az exploded-ben pedig egy elszakadt "S" betu lebegett a keret
        # alatt - a reviewer 3 korben jelolt hibat rajta, torolve biztonsagosabb.
        emit_text("WORLD MAP", a.width / 2, a.margin * 0.35 + 2.1, 4.2, sw="0.1")
        txt.append("</svg>")
        (out / "engrave_labels.svg").write_text("\n".join(txt))
        dxf = ["0", "SECTION", "2", "ENTITIES"]
        # a vago-DXF minden Y-t H-y alakban ir - a cimkeknek is igy kell,
        # kulonben fuggolegesen tukrozve gravirozodnanak (codex merte ki)
        for name, x, y, hgt in labels + [("WORLD MAP", a.width/2, H - a.margin*0.35, 4.2)]:
            dxf += ["0", "TEXT", "8", "0", "10", f"{x:.3f}", "20", f"{y:.3f}",
                    "40", f"{hgt:.3f}", "72", "1", "11", f"{x:.3f}", "21", f"{y:.3f}",
                    "1", name]
        dxf += ["0", "ENDSEC", "0", "EOF"]
        (out / "engrave_labels.dxf").write_text("\n".join(dxf))
        print(f"[i] gravírozott nevek: {len(labels)} ország + címtábla")

    if a.countries and final_land is not None:
        # GHOST-OUTLINE: minden orszagdarab konturja 0,5 mm-rel BELJEBB
        # offsetelve, halvany gravirkent a fogado (legfelso tenger-) lapra -
        # ragasztas utan nem latszik ki, de a vevo pontosan tudja, hova
        # kerul a darab. A referencia sarok-stenciljenel erosebb: itt maga a
        # lap a sablon.
        ghosts = []
        for pc in polys(final_land):
            gi = pc.buffer(-0.5)
            if not gi.is_empty:
                for q in polys(gi):
                    ghosts.append(q.boundary)
        if not ghosts:
            print("[!] ghost-outline: nincs eleg nagy darab, kihagyva")
        else:
            gl = unary_union(ghosts).simplify(a.simplify)
            to_svg(gl, a.width, H, out / "engrave_ghost.svg", stroke_only=True)
            to_dxf(gl, H, out / "engrave_ghost.dxf")
            print(f"[i] ghost-outline gravir: {len(ghosts)} darab-kontur "
                  f"({gl.length:.0f} mm) - a 200 m-es lapra megy")

    print(f"\nkész tábla: {a.width:.0f} x {H:.0f} mm\n")
    print(f"{'lap':>4}{'mélység':>12}{'darab':>7}{'lyuk':>6}{'terület mm2':>13}"
          f"{'leggyengébb':>13}{'nyak':>6}{'eldobott':>9}  státusz")
    ok = True
    for i, name, np_, nh, area, frail, nk, dropped in rows:
        st = "OK" if (frail >= MIN_WEB and nk == 0) else ("NYAK" if nk else "VÉKONY")
        if st != "OK":
            ok = False
        print(f"{i:>4}{name:>12}{np_:>7}{nh:>6}{area:>13,.0f}{frail:>11.2f}mm{nk:>6}"
              f"{dropped:>9}  {st}")

    report = {"width_mm": a.width, "height_mm": round(H, 1), "sheets": len(rows),
              "levels_m": levels, "lat_clip": [lat_min, lat_max],
              "min_web_mm": MIN_WEB, "min_island_mm2": a.min_island,
              "all_ok": ok, "source": "Natural Earth (public domain)",
              "layers": [{"n": i, "depth": name, "pieces": np_, "holes": nh,
                          "area_mm2": round(area), "weakest_mm": round(frail, 2),
                          "necks": nk, "dropped_islands": dropped}
                         for i, name, np_, nh, area, frail, nk, dropped in rows]}
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"\nkiírva: {out}")


if __name__ == "__main__":
    main()
