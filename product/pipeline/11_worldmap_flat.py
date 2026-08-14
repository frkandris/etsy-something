#!/usr/bin/env python3
"""Egyrétegű, kontinensenként vágott világtérkép — a lánc negyedik változata.

Miben más ez, mint a réteges világtérkép (`10_worldmap.py`): **itt nincs
mélység**. A termék egyetlen anyagvastagság, és nem egy összefüggő lap, hanem
**kontinensenként külön darab** — a köztük lévő tenger maga a fal. A vevő a
mellékelt sablon szerint ragasztja fel őket.

Ebből következik a lánc három új képessége:

1. **Háromféle vonaltípus egy fájlban.** A kontinens- és szigetkontúr *vágás*,
   az országhatár a darabon belül *karcolás* (nem vágjuk át, mert akkor
   szétesne), a feliratok *gravírozás*. A vágóban ez rétegenként/színenként
   különül el — eddig egyik láncunk sem írt ki egy fájlba több vonaltípust.
2. **Kontinens-csoportosítás.** A Natural Earth `CONTINENT` attribútuma adja a
   csoportot; a szigetek automatikusan külön darabok lesznek, mert a unió
   összefüggő komponensei.
3. **Csempézés.** A tábla 1325 mm széles, de a legnagyobb darab 330×280 mm
   lehet, hogy kis lézerágyba is beférjen — a nagyobb darabok számozott zónákra
   hasadnak.

  python 11_worldmap_flat.py --out <dir> [--width 1325] [--max-piece 330x280]

Adat: Natural Earth, **közkincs**.
"""
import argparse
import json
import pathlib
import sys

from shapely.geometry import MultiLineString
from shapely.ops import unary_union

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cutlib import (components, heal_to_convergence, necks,  # noqa: E402
                    polys, snap,
                    text_paths, text_width, tile_piece, widest_inscribed)
from geolib import fetch, project  # noqa: E402
from shapely import affinity, make_valid  # noqa: E402

# A vago konvencioja (a referenciatermek is ezt hasznalja): a szin mondja meg,
# mit csinaljon a gep. Ugyanez a DXF-ben kulon retegnev.
RUSSIA_TO_ASIA = {"Russia"}
CUT, SCORE, ENGRAVE = "#ff0000", "#0000ff", "#808080"
LAYERS = {CUT: "CUT", SCORE: "SCORE", ENGRAVE: "ENGRAVE"}


def ring_d(coords, h):
    return "M " + " L ".join(f"{x:.3f},{h - y:.3f}" for x, y in coords) + " Z"


def line_d(coords, h):
    return "M " + " L ".join(f"{x:.3f},{h - y:.3f}" for x, y in coords)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=float, default=1325.0,
                    help="mm, a kesz terkep szelessege (referencia: 1325)")
    ap.add_argument("--max-piece", default="330x280",
                    help="mm, a legnagyobb egyedi darab (kis lezerágy-korlát)")
    ap.add_argument("--lat", default="-58,84", help="szelessegi vagas (del,eszak)")
    ap.add_argument("--min-island", type=float, default=40.0,
                    help="mm2 — ennel kisebb sziget kiesik (kulon darabkent "
                         "nehezen kezelheto)")
    ap.add_argument("--hard-floor", type=float, default=40.0,
                    help="mm2 — ez alatt meg orszagmento kivetellel sem tartunk "
                         "meg darabot: kezzel kezelhetetlen")
    ap.add_argument("--simplify", type=float, default=0.25)
    ap.add_argument("--label-h", type=float, default=4.0, help="mm betumagassag")
    ap.add_argument("--no-labels", action="store_true")
    ap.add_argument("--no-heal", dest="heal", action="store_false",
                    help="ne gyogyitsa a vekony nyakakat (alapbol gyogyit)")
    ap.add_argument("--min-web", type=float, default=2.0,
                    help="mm — a lezer altal elviselt legkeskenyebb anyag")
    a = ap.parse_args()

    lat_min, lat_max = (float(v) for v in a.lat.split(","))
    max_w, max_h = (float(v) for v in a.max_piece.lower().split("x"))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    # ---- adat: orszagok kontinensenkent --------------------------------
    gj = fetch("ne_10m_admin_0_countries")
    by_cont = {}
    for f in gj["features"]:
        pr = f["properties"]
        cont = pr.get("CONTINENT") or "Other"
        if cont == "Seven seas (open ocean)":
            continue                       # ezek szigetcsoportok, nem kontinens
        # A Natural Earth OROSZORSZAGOT EUROPABA sorolja. Fali terkepnel ez
        # katasztrofa: az "Europa" darab igy Portugaliatol Csukotkaig er, 697 mm
        # szeles lesz (merve) - egyetlen hobbi-lezerbe sem fer bele, es a
        # csempezes csak onkenyesen tudja elvagni. A hagyomanyos fali-terkep
        # besorolas Oroszorszagot Azsiahoz teszi; igy Europa kompakt marad, az
        # Azsia-blokk vagasa pedig a kontinenshataron megy.
        if cont == "Europe" and pr.get("NAME") in RUSSIA_TO_ASIA:
            cont = "Asia"
        from shapely.geometry import shape
        g = make_valid(shape(f["geometry"]))
        if g.geom_type not in ("Polygon", "MultiPolygon"):
            continue
        by_cont.setdefault(cont, []).append((pr.get("NAME", ""), g))
    print(f"[geo] kontinensek: {', '.join(sorted(by_cont))}")

    # ---- lepték: a teljes szarazfold a megadott szelessegre ------------
    all_land = unary_union([g for lst in by_cont.values() for _, g in lst])
    all_land = project(all_land, lat_min, lat_max)
    mnx, mny, mxx, mxy = all_land.bounds
    sc = a.width / (mxx - mnx)
    H = (mxy - mny) * sc

    def place(g):
        g = project(g, lat_min, lat_max)
        if g.is_empty:
            return g
        g = affinity.translate(g, -mnx, -mny)
        return affinity.scale(g, xfact=sc, yfact=sc, origin=(0, 0))

    print(f"[geo] tabla: {a.width:.0f} x {H:.0f} mm, "
          f"legnagyobb darab: {max_w:.0f} x {max_h:.0f} mm")

    # ---- darabok: kontinensenkent, komponensekre bontva -----------------
    lost = []            # (orszagnev, terulet) — a hard-floor alatt
    healed = []          # (kontinens, nyak_elotte, nyak_utana)
    pieces = []          # (kontinens, index, geometria)
    scores = []          # (kontinens, index, hatarvonalak a darabon belul)
    labels = []          # (nev, x, y, magassag)
    for cont in sorted(by_cont):
        cgeoms = [(n, place(g)) for n, g in by_cont[cont]]
        cgeoms = [(n, g) for n, g in cgeoms if not g.is_empty]
        if not cgeoms:
            continue
        merged = snap(unary_union([g for _, g in cgeoms]))
        all_parts = components(merged)
        parts = [q for q in all_parts if q.area >= a.min_island]
        dropped = len(all_parts) - len(parts)

        # ORSZAG SOSEM TUNHET EL. A puszta terulet-kuszob egesz orszagokat
        # torolt: Sri Lanka 74 mm2, Tajvan 46, Ciprus 8 - es a Fulop-szigetekbol
        # csak Luzon maradt, Mindanao (105 mm2) kiesett. Egy vilagterkepen ez
        # nem "apro sziget", hanem hianyzo orszag. Ezert: ha egy orszagnak EGY
        # darabja sem eri el a kuszobot, a legnagyobbat visszatesszuk - hacsak
        # az sem eri el a fizikai also hatart (--hard-floor), mert az mar
        # kezzel kezelhetetlen es a lezer alatt is elveszik.
        rescued = []
        for n, g in cgeoms:
            # A korabbi teszt (atfedes > az ORSZAG teruletenek 40%-a) atengedte
            # azt az esetet, amikor az orszag fodarabja MAR benne van a parts-ban:
            # Indonezia 584 mm2-es es a Fulop-szigetek 124 mm2-es fodarabja
            # 100%-ban atfedett egy letezo elemet, megis ujra bekerult - dupla
            # vagokontur, dupla score es dupla cimke lett belole (codex merte ki).
            # A helyes kerdes: van-e MAR olyan darab, ami az orszag legnagyobb
            # komponenset erdemben lefedi.
            cand = components(snap(g))
            if not cand:
                continue
            big = cand[0]
            if any(q.intersection(big).area > big.area * 0.5 for q in parts):
                continue
            if big.area >= a.hard_floor:
                parts.append(big)
                rescued.append((n, big.area))
            else:
                lost.append((n, big.area))
        if rescued:
            print(f"[i] {cont}: {len(rescued)} orszag megmentve a kuszob alol: "
                  + ", ".join(f"{n} ({ar:.0f} mm2)" for n, ar in sorted(
                      rescued, key=lambda t: -t[1])[:6]))
        parts = sorted(parts, key=lambda q: q.area, reverse=True)
        for i, p in enumerate(parts):
            p = p.simplify(a.simplify).buffer(0)
            if p.is_empty:
                continue
            # NYAK-GYOGYITAS. Reteges terméknél a vekony nyak esztetikai kerdes
            # (a mogotte levo lapon ott az anyag), EGYRETEGU fadarabnal viszont
            # toresveszely: merve Panama, a Malaj-felsziget es Sulawesi karjai
            # mennek MIN_WEB ala. A gyogyitas lokalis - csak a nyak-zonat
            # szelesiti -, es konvergenciaig iteral, mert egy kor nem eleg.
            p_raw = p          # a gyogyitas ELOTTI perem - a karcolas ehhez mer
            if a.heal:
                n0 = necks(p)
                if n0:
                    p = heal_to_convergence(p, min_web=a.min_web)
                    healed.append((cont, n0, necks(p)))
            pieces.append((cont, i, p))
            # KARCOLT orszaghatarok: a darabon BELULI hatarok. A kulso
            # kontur mar vagas, azt le kell vonni, kulonben ketszer megy rajta
            # a gep (es a karcolas atvagna a peremet).
            inner = []
            for n, g in cgeoms:
                gi = snap(g).intersection(snap(p))
                # CSAK a poligonok: az intersection GeometryCollectiont is ad
                # (erintkezo vonal- es pontdarabkakkal), es annak a .boundary-ja
                # shapely 2-ben None - ezen hasalt el az elso futas.
                gp = polys(gi)
                if not gp:
                    continue
                gi = unary_union(gp)
                # GEOS "side location conflict": a bevalt javitas mindket
                # operandus racsra kerekitese - ez a sor maradt ki belole.
                try:
                    # A levonas a GYOGYITAS ELOTTI peremhez mer: a gyogyitas
                    # elmozditja a kontur egy reszet, es akkor a partvonal mar
                    # nem esik egybe a kulso hatarral - a karcolt hossz 8580-rol
                    # 18589 mm-re ugrott, vagyis a gep a mar KIVAGOTT konturt is
                    # vegigkarcolta volna.
                    b = snap(gi.boundary).difference(snap(p_raw.boundary.buffer(0.35)))
                except Exception as exc:                       # noqa: BLE001
                    print(f"[!] {n}: karcolt hatar kihagyva ({exc.__class__.__name__})")
                    b = None
                if b is not None and not b.is_empty:
                    inner.append(b)
                if not a.no_labels:
                    big = max(polys(gi), key=lambda x: x.area, default=None)
                    if big is None or big.area < 120:
                        continue
                    r = widest_inscribed(big) / 2
                    hgt = min(a.label_h, r * 0.85)
                    if hgt < 2.2:
                        continue
                    bw = big.bounds[2] - big.bounds[0]
                    tw = text_width(n.upper(), hgt)
                    if tw > bw * 0.85:
                        hgt *= (bw * 0.85) / tw
                    if hgt < 2.2:
                        continue
                    from shapely.algorithms.polylabel import polylabel
                    c = polylabel(big, tolerance=0.5)
                    labels.append((n.upper(), c.x, c.y, hgt))
            if inner:
                scores.append((cont, i, unary_union(inner)))
        if dropped:
            print(f"[i] {cont}: {len(parts)} darab, {dropped} apro sziget kiesett")
        else:
            print(f"[i] {cont}: {len(parts)} darab")

    # ---- csempezes a lezerágy-korláthoz ---------------------------------
    tiled, oversize = [], 0
    for cont, i, p in pieces:
        zones = tile_piece(p, max_w, max_h, min_area=a.min_island)
        if len(zones) > 1:
            oversize += 1
        for q, (r, c) in zones:
            tiled.append((cont, i, q, (r, c), len(zones) > 1))
    if healed:
        _b = sum(h[1] for h in healed)
        _a2 = sum(h[2] for h in healed)
        print(f"[i] nyak-gyogyitas: {_b} -> {_a2} ({len(healed)} darabon)")
    print(f"[i] darabok: {len(pieces)} -> csempezve {len(tiled)} "
          f"({oversize} darab volt tul nagy)")

    # ---- kimenet --------------------------------------------------------
    def svg_open():
        return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{a.width:.2f}mm" '
                f'height="{H:.2f}mm" viewBox="0 0 {a.width:.3f} {H:.3f}">']

    def add_poly(buf, geom, colour, w=0.1):
        d = []
        for p in polys(geom):
            d.append(ring_d(p.exterior.coords, H))
            for r in p.interiors:
                d.append(ring_d(r.coords, H))
        if d:
            buf.append(f'  <path d="{" ".join(d)}" fill="none" stroke="{colour}" '
                       f'stroke-width="{w}"/>')

    def add_lines(buf, geom, colour, w=0.08):
        ls = geom.geoms if isinstance(geom, MultiLineString) else [geom]
        d = [line_d(g.coords, H) for g in ls if g.geom_type == "LineString"]
        if d:
            buf.append(f'  <path d="{" ".join(d)}" fill="none" stroke="{colour}" '
                       f'stroke-width="{w}"/>')

    def add_text(buf, name, x, y, hgt, colour=ENGRAVE):
        subs = []
        for poly in text_paths(name, x, y, hgt):
            subs.append("M " + " L ".join(f"{px:.2f},{H - py:.2f}"
                                          for px, py in poly) + " Z")
        if subs:
            buf.append(f'  <path d="{" ".join(subs)}" fill="{colour}" '
                       'fill-rule="evenodd" stroke="none"/>')

    # teljes terkep egy fajlban
    buf = svg_open()
    for _c, _i, q, _rc, _t in tiled:
        add_poly(buf, q, CUT)
    for _c, _i, s in scores:
        add_lines(buf, s, SCORE)
    for n, x, y, hgt in labels:
        add_text(buf, n, x, y, hgt)
    buf.append("</svg>")
    (out / "world_map.svg").write_text("\n".join(buf) + "\n")

    # kontinensenkenti fajlok (a referencia is ad ilyet)
    cdir = out / "continents"
    cdir.mkdir(exist_ok=True)
    for cont in sorted({c for c, _, _ in pieces}):
        b = svg_open()
        for c2, _i, q, _rc, _t in tiled:
            if c2 == cont:
                add_poly(b, q, CUT)
        for c2, _i, s in scores:
            if c2 == cont:
                add_lines(b, s, SCORE)
        b.append("</svg>")
        (cdir / f"{cont.replace(' ', '_').lower()}.svg").write_text("\n".join(b) + "\n")

    # DXF: retegnevvel, nem szinnel
    dxf = ["0", "SECTION", "2", "ENTITIES"]

    def dxf_rings(geom, layer):
        for p in polys(geom):
            for ring in [p.exterior] + list(p.interiors):
                dxf.extend(["0", "POLYLINE", "8", layer, "66", "1", "70", "1"])
                for x, y in ring.coords:
                    dxf.extend(["0", "VERTEX", "8", layer,
                                "10", f"{x:.4f}", "20", f"{H - y:.4f}"])
                dxf.append("0")
                dxf.append("SEQEND")

    for _c, _i, q, _rc, _t in tiled:
        dxf_rings(q, "CUT")
    for _c, _i, s in scores:
        for g in (s.geoms if isinstance(s, MultiLineString) else [s]):
            if g.geom_type != "LineString":
                continue
            dxf.extend(["0", "POLYLINE", "8", "SCORE", "66", "1", "70", "0"])
            for x, y in g.coords:
                dxf.extend(["0", "VERTEX", "8", "SCORE",
                            "10", f"{x:.4f}", "20", f"{H - y:.4f}"])
            dxf.extend(["0", "SEQEND"])
    for n, x, y, hgt in labels:
        dxf.extend(["0", "TEXT", "8", "ENGRAVE", "10", f"{x:.3f}",
                    "20", f"{H - y:.3f}", "40", f"{hgt:.3f}", "72", "1",
                    "11", f"{x:.3f}", "21", f"{H - y:.3f}", "1", n])
    dxf.extend(["0", "ENDSEC", "0", "EOF"])
    (out / "world_map.dxf").write_text("\n".join(dxf))

    # CSEMPE-FAJLOK: darabonkent kulon, SAJAT origora tolva. A codex jogosan
    # jelezte, hogy a 330x280-as korlat eddig csak MERES volt: a csempeket
    # globalis, 1325 mm-es koordinatakon exportaltuk egyetlen fajlba, tehat kis
    # lezerágyon meg sem lehetett nyitni. Itt minden csempe sajat fajlt kap,
    # 0,0-ba tolva, a ra eso score-vonalakkal es cimkekkel egyutt.
    tdir = out / "tiles"
    tdir.mkdir(exist_ok=True)
    n_tiles = 0
    for cont, i, q, (r, c) in [(a_, b_, c_, d_) for a_, b_, c_, d_, e_ in tiled if e_]:
        b = q.bounds
        loc = affinity.translate(q, -b[0], -b[1])
        w_, h_ = b[2] - b[0], b[3] - b[1]
        buf2 = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_:.2f}mm" '
                f'height="{h_:.2f}mm" viewBox="0 0 {w_:.3f} {h_:.3f}">']
        d2 = []
        for pp in polys(loc):
            d2.append("M " + " L ".join(f"{x:.3f},{h_ - y:.3f}"
                                        for x, y in pp.exterior.coords) + " Z")
            for rr in pp.interiors:
                d2.append("M " + " L ".join(f"{x:.3f},{h_ - y:.3f}"
                                            for x, y in rr.coords) + " Z")
        buf2.append(f'  <path d="{" ".join(d2)}" fill="none" stroke="{CUT}" '
                    'stroke-width="0.1"/>')
        # a csempere eso karcolt hatarok, ugyanabba a lokalis rendszerbe tolva
        for c2, i2, sg in scores:
            if c2 != cont or i2 != i:
                continue
            cut = sg.intersection(q.buffer(0.02))
            if cut.is_empty:
                continue
            cut = affinity.translate(cut, -b[0], -b[1])
            ls = cut.geoms if hasattr(cut, "geoms") else [cut]
            dd = ["M " + " L ".join(f"{x:.3f},{h_ - y:.3f}" for x, y in gg.coords)
                  for gg in ls if gg.geom_type == "LineString"]
            if dd:
                buf2.append(f'  <path d="{" ".join(dd)}" fill="none" '
                            f'stroke="{SCORE}" stroke-width="0.08"/>')
        buf2.append("</svg>")
        nm = f"{cont.replace(' ', '_').lower()}_{i}_{r}{c}.svg"
        (tdir / nm).write_text("\n".join(buf2) + "\n")
        n_tiles += 1
    if n_tiles:
        print(f"[i] csempe-fajlok: {n_tiles} db, mindegyik sajat origon "
              f"(kis lezerágyra nyithato)")

    # ELHELYEZESI SABLON: a darabok kontúrja vékonyan, zóna-számokkal. A
    # referenciatermek ezt kulon kepen adja - nalunk vagható/nyomtatható fájl.
    tpl = svg_open()
    for cont, _i, q, (r, c), is_tiled in tiled:
        add_poly(tpl, q, "#c8c8c8", w=0.3)
        if is_tiled:
            ct = q.representative_point()
            add_text(tpl, f"{cont[:2].upper()}{r}{c}", ct.x, ct.y, 6.0, "#c8c8c8")
    tpl.append("</svg>")
    (out / "placement_template.svg").write_text("\n".join(tpl) + "\n")

    # ---- RENDER-BARAT KIMENET -------------------------------------------
    # A renderelo `layer_*.svg`-t keres KITOLTOTT alakzatokkal, a gravir-
    # overlay pedig `engrave_labels.svg`-t. Ha ezt a ket fajlt is kiirjuk, a
    # meglevo render-gepezet valtozatlanul mukodik ezen a termeken is - nem
    # kell kulon betolto.
    rb = svg_open()
    # DARABONKENT KULON <path>. Egyetlen path-ba rakva a Blender SVG-importere
    # EGY gorbe-objektumot csinal mind a 79 kulonallo darabbol, es a kitoltesnel
    # osszekeveri oket: Afrika es Del-Amerika puszta konturkent jott ki, az
    # Indiai-ocean folott pedig haromszog-mutermekek jelentek meg. Kulon
    # path-onkent minden darab sajat objektum lesz, es magaban toltodik ki.
    # A csempezes ide nem jon: az gyartasi ugy, a vevo a kesz terkepet latja.
    for _c, _i, q in pieces:
        for pp in polys(q):
            d = [ring_d(pp.exterior.coords, H)]
            for r in pp.interiors:
                d.append(ring_d(r.coords, H))
            rb.append(f'  <path d="{" ".join(d)}" fill="#000" fill-rule="evenodd"/>')
    rb.append("</svg>")
    (out / "layer_1_of_1.svg").write_text("\n".join(rb) + "\n")

    eb = svg_open()
    for _c, _i, sgeom in scores:
        add_lines(eb, sgeom, "#803c14", w=0.35)
    for n, x, y, hgt in labels:
        add_text(eb, n, x, y, hgt, "#803c14")
    eb.append("</svg>")
    (out / "engrave_labels.svg").write_text("\n".join(eb) + "\n")

    # ---- riport ---------------------------------------------------------
    biggest = max(tiled, key=lambda t: max(t[2].bounds[2] - t[2].bounds[0],
                                           t[2].bounds[3] - t[2].bounds[1]))
    bb = biggest[2].bounds
    neck_total = sum(necks(q) for _c, _i, q, _rc, _t in tiled)
    report = {
        "tabla_mm": [round(a.width, 1), round(H, 1)],
        "darabok": len(pieces),
        "csempezve": len(tiled),
        "legnagyobb_darab_mm": [round(bb[2] - bb[0], 1), round(bb[3] - bb[1], 1)],
        "max_engedett_mm": [max_w, max_h],
        "nyakak": neck_total,
        "karcolt_hatar_mm": round(sum(s.length for _c, _i, s in scores), 1),
        "gravirozott_nevek": len(labels),
        "kimaradt_orszagok": [{"nev": n, "mm2": round(ar, 1)} for n, ar in
                              sorted(lost, key=lambda t: -t[1])],
    }
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"[i] legnagyobb darab: {bb[2]-bb[0]:.0f} x {bb[3]-bb[1]:.0f} mm "
          f"(engedett {max_w:.0f} x {max_h:.0f})")
    print(f"[i] karcolt hatar: {report['karcolt_hatar_mm']:.0f} mm, "
          f"gravirozott nev: {len(labels)}, nyak: {neck_total}")
    if lost:
        print(f"[!] {len(lost)} orszag a fizikai also hatar alatt maradt, "
              f"nem kerult a keszletbe: "
              + ", ".join(n for n, _ in sorted(lost, key=lambda t: -t[1])[:8]))
    print(f"kiirva: {out}")


if __name__ == "__main__":
    main()
