---
type: Workflow
title: Réteges világtérkép-lánc — a harmadik pipeline-változat
description: Itt nincs képgenerátor. A mélység nem becsült, hanem mért: a Natural Earth batimetria-kontúrjai eleve egymásba ágyazottak. A vágásbiztonsági gépezet ugyanaz, a front-end teljesen más.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-13T20:00:00Z
---

# Réteges világtérkép-lánc

Egy versenytárs-listing kapcsán ([VyvaStudioDigital](https://www.etsy.com/listing/1794946470/),
HUF 4 160, 29 review, Star Seller — és a bolt szerepel a saját
[[findings/verified-shop-list]]-ünkön is) épült meg a lánc harmadik változata.

## Miben más

| | papírvágás-lánc | világtérkép-lánc |
|---|---|---|
| forrás | gpt-image-2 lapos illusztráció | **Natural Earth vektoradat** |
| mélység | becsült (tónus-rangsor) | **mért** (batimetria-kontúrok) |
| beágyazás | k-means + nyakgyógyítás kényszeríti ki | **eleve adott** — a 200 m-es kontúr tartalmazza az 1000 m-est |
| licenc | modellenként eltérő, buktatós | **közkincs**, korlátozás nélkül |

A hátulja viszont azonos: vágásbiztonsági riport, minimális web, nyak-detektor, SVG + DXF R12.

## A szerkezet

A szárazföld a legfelső lap, alatta a tenger lépcsőzik lefelé. Fizikailag ez ugyanaz a süllyesztett
felépítés, mint a papírvágásnál, csak fordított szereposztással: ott a **mező** volt a felső lap,
itt a **szárazföld**.

```
6. lap  szárazföld     37 573 mm²   ← legfelül, dió
5. lap  200 m          43 851 mm²
4. lap  1000 m         46 417 mm²
3. lap  2000 m         54 030 mm²
2. lap  4000 m         76 241 mm²
1. lap  6000 m         81 184 mm²   ← hátlap, majdnem teli
```

## Amit menet közben tanultunk

**A 0 m-es szint felesleges.** A `ne_10m_bathymetry_L_0` maga a partvonal, tehát a lapja azonos a
szárazföldével — két egyforma lap készült tőle. A szkript ma hibával leáll, ha valaki megadja.

**A Natural Earth kontúrjai NEM tökéletesen egymásba ágyazottak.** A 200 m-es lap területe nagyobb
lett, mint az 1000 m-esé — vagyis a felső lap kilógott az alatta lévő alól, ami a fizikai stackben
látható hiba. **32,7% lógott ki.** A javítás ugyanaz a lépés, mint a papírvágás-láncban: minden
lapot a mögötte lévőre klippelünk. *Az „adat eleve helyes" feltevés itt bukott meg.*

**A szorosok nyakat adnak.** A Panama- és a Szuezi-földszoros 400 mm-es táblán 2 mm alatti, tehát
a szárazföld lap szétesne. A `--thicken` zárja őket (nyitás-zárás), a méret érdemi változtatása
nélkül.

**A gravírozási réteget országonként kell építeni.** Az `unary_union` összeolvasztja a szomszédos
országokat, és pont a belső határok tűnnek el — az egész réteg 2 mm hosszú lett tőle. Országonként
véve 2 428 mm.

**A gravír-overlay igazítása nem az objektum-origókon múlik.** A renderelő a rétegek origóját
áthelyezi (`origin_set` + középre tolás), ezért az `objs[0].location` másolása a címkéket a térben
szórta szét. A helyes igazítás ugyanaz a `(-cx, -cy)` eltolás, amit a rétegek kaptak — a lépték
magától stimmel, mert a viewBox közös.

**Az SVG-importált görbék `bound_box`-a hamis — mindegyiké, nem csak a gravíré.** Először a 223
gravírgörbénél tűnt fel (2,3 egységnek mérték magukat a 0,4 egységes művön), és a kizárásuk
(`ENGRAVE_OBJS`) elégnek látszott. A következő körben kiderült, hogy a **lapok** görbéi is ±1,2-es
dobozt jelentenek a valós ±0,2 helyett — az evaluated depsgraph-os másolat sem igaz. Ez mérgezte
az exploded kamera-illesztését (a mű aprócska lett) és a styled ültetést (a mű a padló alá
süllyedt). A végleges javítás: a `world_bbox` a görbéket tesszellált `to_mesh()` csúcsokból méri.

**A kimeneti mappát takarítani kell.** Egy korábbi, más `--levels` futás fájljai bennmaradtak, és a
renderelő egy kevert készletet olvasott be.

## Használat

```bash
python product/pipeline/10_worldmap.py --out <dir> \
  --width 400 --levels 200,1000,2000,4000,6000 --thicken 0.9 --borders
blender -b -P product/render_blender.py -- <dir> <out.png> plate bathy --paper
```

Adat: [Natural Earth](https://www.naturalearthdata.com/) — **közkincs**, kereskedelmi felhasználás
korlátozás nélkül, attribúció nem kötelező. A letöltés a `nvkelso/natural-earth-vector`
GitHub-tükörről megy, mert a hivatalos CDN megbízhatatlan; a fájlok a
`product/pipeline/geodata/` alatt gyorsítótárazódnak (gitignore-olva, ~200 MB).

## Ami nincs kész

- **A renderelő keret-geometriája négyzetet feltételez.** A 2:1-es térképnél a hátlap kilóg és a mű
  nem tölti ki a keretnyílást. A `--frame` nélküli `plate` nézet viszont helyes — a fenti
  parancssor ezért nem használ keretet. Ez a renderelő refaktorja, nem a térkép-láncé.
- **Nincsenek feliratok** (országnevek, iránytű, címtábla), amiket a referenciatermék gravíroz.
- **A `--min-island` 25 mm²-es küszöbe 220 szigetet dob el** a szárazföld lapon. Ez szándékos (egy
  ennél kisebb darab kiesik a lapból), de a szám a riportban szerepel, hogy látszódjon.

## Provenancia

`product/pipeline/10_worldmap.py`, `product/iterations/0050-worldmap/`. Kapcsolódik:
[[workflows/recessed-papercut-pipeline]], [[findings/geographic-motifs]],
[[findings/verified-shop-list]].
