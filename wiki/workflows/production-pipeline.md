---
type: Workflow
title: AI-támogatott layered fájl termelési folyamat
description: Képmodell → poszterizálás → rétegenkénti trace → boolean unió → vágásbiztonság → Blender mockup.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

## Aktuális belépési pont — 2026-09-05

A támogatott futtató a `product/pipeline/run_product.py`: a profil vezérli a geometriát és a Blender-nézeteket. A `product/catalog/<forrástermék>/runs/<futás>/` a forrást, a receptet és a kimenetet tartja együtt; a `history/` a régi számozott iterációkra mutat. A további régi lépéssor történeti referencia.

```sh
.venv/bin/python product/pipeline/run_product.py --profile marlaser-worldmap \
  --out product/builds/worldmap
```

Állatportrénál `--src` is kell. A `run_theme.sh THEME SOURCE PROFILE [LEVELS]` csak explicit wrapper. A korábbi `04_composite.py` / `render_photo.png` lépést és témánkénti háttérválasztást nem futtatja; helyettük a profil Blender-nézetei készülnek. A `worldmap`/`vyva-worldmap` kísérleti, lezárt validált futás nélkül. Ellenőrzési és review-eljárás: [[workflows/engineering-quality]].


## Jelenet-mód — 2026-09-24 (Nagy hullám)

Az eddigi termékek portrék voltak: a kép szélén a felső lap „mezője” állt. Egy **széltől szélig
tartó jelenetnél** (ég, tenger) ez a feltevés rossz, ezért két kapcsoló készült:

- `01b_depth.py --sheet-colours "#hex,…"` — a rajz spot-színei **lapsorrendben** (0 = hátlap, az
  utolsó a felső lap). A sorrendet a színek listája adja, nem a világosságuk: a halvány ég a
  leghátsó, a krém hab a legfelső. A prompt ugyanezeket a színeket írja elő.
- `01b_depth.py --scene` — a kép köré 3 px-es 0-s perem kerül, így az 1. lap maga a tömör hátlap.
  `--full-panel` nélkül, `--margin`-nal futtatva minden lap keretet kap.

Útközben két rejtett hiba derült ki; a portrék egyiket sem mutatták meg:

- **Négyzetes vászon.** Az SVG/DXF mindig `--size × --size` négyzetre ment, a 3:2-es jelenet a
  felső kétharmadba került. Most a vászon a panel: a hosszabb oldal a `--size`, a rövidebb a mért
  érték (a németjuhász relief így 193,8 × 300 mm-es lapot kap a korábbi 300 × 300 helyett). A
  riportban `panel_mm`.
- **Leválasztott keret.** A trace-elt lap a panel szélén néhány századmilliméterrel elmarad. Az
  illesztés ezeket a csíkokat nyílásként kicsinyítette, így a keret belső határán hajszálvékony vágás
  keletkezett, a keretet pedig a sáv-lépés laza darabként eldobta. Most a legszélső 1 mm nem számít
  nyílásnak. Regressziós teszt: `test_scene_keeps_the_frame_band_on_every_sheet`.

A két javítás után a mentett receptek geometriája változatlan: a macskáknál bájtra azonos alakzatok,
csak a gyűrűk sorrendje más. Eredmény: [[shops/marlasercut]],
`product/catalog/great-wave/runs/2026-09-24-v1/README.md`.

# Termelési folyamat

> **Státusz: élesben fut** (2026-08-08-tól). Implementáció: `product/pipeline/00_generate.py`
> (gpt-image-2 mélységtérkép, `--ref/--crop` image-to-image stílusreferenciával),
> `product/pipeline/02_trace.py` (k-means poszterizálás → potrace → shapely → nesting-kényszer →
> nyak-gyógyítás → kulcslyuk → SVG/DXF + biztonsági riport), `product/render_blender.py`.
> Az iterációk számozott mappákban: `product/iterations/0001-…`. Az első teljes végigfutás
> és a codex-audit utáni javítások: `product/iterations/0005-fixed-celtic-tree/README.md`.
> Egy design gépi ideje a teljes láncon: ~3 perc.

**Kulcsgondolat: fájlt adsz el, nem tárgyat.** A gépek nem a termeléshez kellenek, hanem (1) annak
bizonyítására, hogy a fájl kivágható, és (2) eladható fotóhoz.

## 1. Témaválasztás — adatból, nem ihletből

A [[findings/listing-craft]] témamegoszlása és a [[shops/colorlayerart]] kategórialistája együtt
gyakorlatilag tartalomnaptár: ünnepek (karácsony, halloween, Valentin, húsvét, anyák/apák napja,
július 4.) + örökzöld alap (állat, mandala, Tree of Life, vallási).

A leghatékonyabb a **hosszú farok egy sablonnal**: egy jó „kutyafajta" sablonból 200+ listing jön ki,
mindegyik külön keresési kifejezésre.

## 2. Alapgrafika — képmodell (Flux / SDXL / Midjourney)

Nem kész terméket generálsz, hanem **vázlatot**, ami rétegezhető: magas kontraszt, koncentrikus
mélységszintek, tiszta zárt formák, se gradiens, se hajszálvékony részlet.

## 3. Rétegszétválasztás — ez szkript, nem AI

A kulcstrükk: **poszterizáld N tónusra, és a k-adik réteg a k…N tónusok uniója legyen.** Így minden
réteg tömör alap, nem esik szét lebegő szigetekre.

```
ImageMagick (poszterizálás N szintre)
  → vtracer / potrace (rétegenkénti trace, CLI, batch-elhető)
  → Python + shapely (boolean unió, sziget-szűrés, kerf offset)
  → SVG + DXF export, rétegenként is
```

A célformátum a [[findings/listing-craft]] szerint: **SVG (94%) + DXF (25%)**, opcionálisan PDF/PNG.

## 4. Vágásbiztonsági ellenőrzés — determinisztikus

Minimum web-vastagság (3 mm rétegelt lemeznél ~1,5–2 mm alatt eldobandó), minimális sziget-terület,
összefüggőség rétegenként, kerf-kompenzáció. **Ez a lépés menti meg a boltot** az „a fájl nem
vágható ki" típusú 1 csillagos értékelésektől.

## 5. Mockup — a legnagyobb automatizálási nyereség ÉS maga a versenyelőny

> A [[findings/keyword-demand-sweep]] szerint a hosszú farkot nem kulcsszóval nyered meg, hanem
> thumbnaillel: a `dachshund svg` 11 200 versenytársa között a lapos sziluettek közül egy rétegzett
> 3D render vizuálisan kilóg. Ez a lépés ezért nem kényelmi kérdés.

**Blender headless + Python**: rétegek importálása SVG-ből, extrudálás, z-eltolás, fa textúra,
render egy előre beállított jelenetbe. Egy szkript → N termékfotó konzisztens arculattal, plusz egy
körbeforgó videó. A [[shops/colorlayerart]] képei pontosan így néznek ki.

## 6. Listing

Cím: gépkompatibilitás felsorolva (`laser`, `CNC`, `Cricut`, `Glowforge`), formátumok, **rétegszám**.
Árazás: a korábbi **$9–28, akció nélkül** ajánlás visszavonva. A deduplikált
minta nem igazol általános ár- vagy akcióstratégiát; a saját terméken mérendő.
Lásd [[findings/pricing-and-discounting]] és [[overview]].
20 design után a családra egy bundle listing (a bundle a mezőny mindössze 4%-a, medián $8,80 vs
$4,80 — kihasználatlan rés).

## Időbecslés

| | egyszeri | designonként |
|---|---|---|
| pipeline felépítése | 4–8 hét esténként | — |
| koncepció + generálás | | 10–15 perc |
| trace + rétegezés | | ~1 perc gép |
| kézi tisztítás, ellenőrzés | | 15–25 perc |
| render mockup + videó | | ~2 perc gép |

**20–40 perc emberi munka designonként.** Havi 4–10 designnál ez 3–7 óra + admin.

## Gépek

- **Lézervágó: ne vegyél.** Fali panelnél nincs illesztés, tehát nem kell iteratív tesztvágás.
  Alkalmankénti hozzáférés (a felhasználónál: „Sanyi papa") elég a validációhoz és a valódi fotókhoz.
- **Papírvágó (Cricut/Silhouette):** olcsó, és külön piac ugyanarra a fájlra — a címek 28%-a említi
  a Cricutot.
- **3D nyomtató:** ehhez a termékhez mellékes.

## Kockázatok

- **Védjegy.** A [[shops/colorlayerart]] „Grin Pumpkin"-je láthatóan Grinch. Ezt ne másold — a
  2024-es kohorszban 13 bolt tűnt el két év alatt ([[findings/2024-vs-2026-cohort]]).
- **AI-nyilatkozat.** Az Etsy elvárja a generatív AI szerepének jelölését.
- **Felfutás.** A [[shops/colorlayerart]] 2,5 év alatt ért 559 listingig. Az első ~6 hónap
  gyakorlatilag bevétel nélküli katalógus- és értékelésépítés.
