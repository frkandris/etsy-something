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
    a = ap.parse_args()

    lat_min, lat_max = (float(v) for v in a.lat.split(","))
    levels = [int(v) for v in a.levels.split(",")]
    if 0 in levels:
        sys.exit("a 0 m-es szint azonos a szárazfölddel — hagyd ki a --levels listából")
    for lv in levels:
        if lv not in BATHY:
            sys.exit(f"nincs {lv} m-es Natural Earth kontúr; elérhető: {sorted(BATHY)}")

    print(f"[geo] Miller-vetítés, {lat_min}..{lat_max} szélesség, {a.width:.0f} mm széles tábla")

    land = project(geoms_of(fetch("ne_10m_land")), lat_min, lat_max)
    seas = {lv: project(geoms_of(fetch(BATHY[lv])), lat_min, lat_max) for lv in levels}

    # közös lépték: minden réteg UGYANAZZAL a transzformációval, különben nem illeszkednek
    mnx, mny, mxx, mxy = land.union(seas[levels[0]]).bounds
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
    for old in list(out.glob("layer_*.svg")) + list(out.glob("layer_*.dxf")):
        old.unlink()

    # A lapok: a legfelső a szárazföld, alatta minden lépcsővel nagyobb a MEGMARADÓ
    # anyag, mert a mélyebb víz nyílása kisebb. Ez a papíros lánc süllyesztett
    # szerkezetének a fordítottja: ott a mező volt a felső lap, itt a szárazföld.
    sheets = []
    sheets.append(("szárazföld", land))
    for lv in levels:
        sheets.append((f"{lv} m", panel.difference(seas[lv]).union(land)))
    sheets.reverse()          # 1. lap = a legmélyebb (a hátlap), N. = szárazföld

    # BEÁGYAZÁS KIKÉNYSZERÍTÉSE. A Natural Earth kontúrjai elvben egymásba
    # ágyazottak, a gyakorlatban nem: a 200 m-es lap területe nagyobb lett, mint
    # az 1000 m-esé, tehát a k. lap NEM fért bele a k-1.-be. Ha ezt nem javítjuk,
    # a fizikai stackben az egyik lap kilóg a másik alól. Ugyanaz a lépés, mint a
    # papírvágás-láncban: minden lapot a mögötte lévőre klippelünk.
    fixed = [sheets[0]]
    for name, g in sheets[1:]:
        clipped = g.intersection(fixed[-1][1])
        if clipped.area < g.area * 0.999:
            print(f"[i] {name}: beágyazásra klippelve "
                  f"({(1 - clipped.area / g.area) * 100:.1f}% lógott ki)")
        fixed.append((name, clipped))
    sheets = fixed

    rows = []
    for i, (name, g) in enumerate(sheets, 1):
        g = set_precision(make_valid(g), 0.001).simplify(a.simplify)
        if a.thicken > 0:
            # zárás: a nyak összeforr, a forma mérete lényegében marad
            g = g.buffer(a.thicken).buffer(-a.thicken * 0.72)
        # a keretsáv minden lapon anyag: ez tartja össze a szigeteket is
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
