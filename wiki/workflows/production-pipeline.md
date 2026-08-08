---
type: Workflow
title: AI-támogatott layered fájl termelési folyamat
description: Képmodell → poszterizálás → rétegenkénti trace → boolean unió → vágásbiztonság → Blender mockup.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Termelési folyamat

> **Státusz:** javaslat, még nem futott le élesben. Amit alátámaszt, az a
> [[findings/catalogue-size-and-throughput]] tempó-adata és a
> [[findings/listing-craft]] formátum-elvárásai.

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
Árazás: **$9–28, akció nélkül** — [[findings/pricing-and-discounting]].
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
