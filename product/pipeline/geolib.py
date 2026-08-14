"""Natural Earth adatforrás és vetítés — a térkép-termékek közös alapja.

Közkincs adat (naturalearthdata.com), kereskedelmi felhasználás korlátozás
nélkül. A letöltés a nvkelso/natural-earth-vector GitHub-tükörről megy, mert a
hivatalos CDN megbízhatatlan; a fájlok `geodata/` alatt gyorsítótárazódnak.
"""
import json, math, pathlib, urllib.request

from shapely.geometry import box, shape
from shapely.ops import transform, unary_union
from shapely import make_valid

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson"
CACHE = pathlib.Path(__file__).resolve().parent / "geodata"


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

    return transform(tx, g)






