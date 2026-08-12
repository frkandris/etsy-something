---
type: Finding
title: A 3D-fájlpiac szerkezete az Etsyn — boltok, hosszú farok, és a licenc mint vásárlási jelzés
description: 34 bolt eladási adata, 204 hosszú farok kifejezés és 56 mért keresés alapján. Két külön kohorsz létezik, a belépőknek 3-10 hónap alatt sikerült, és a legjobban konvertáló kifejezés nem termékről szól, hanem a kereskedelmi licencről.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T15:00:00Z
sources:
  - resource: /assets/data/3d-print-shops-2026-08-12.json
    title: 34 bolt eladási és kor-adata
  - resource: /assets/data/3d-print-longtail-2026-08-12.json
    title: 204 hosszú farok kifejezés, ebből 16 mérve
  - resource: /assets/data/3d-print-marketplace-insights-2026-08-12.json
    title: 56 keresőkifejezés első kézből
---

# A 3D-fájlpiac szerkezete az Etsyn

## Honnan jön az adat

Ugyanaz a mérési lánc, mint a mostani niche-nél ([[methods/measurement-chain]]), csak Apify nélkül —
minden böngészőből, a bejelentkezett munkamenetből:

| lépés | forrás | mit adott |
|---|---|---|
| kereslet | Etsy Marketplace Insights | 56 kifejezés: keresés/30 nap, versengő listingszám, konverzió |
| hosszú farok | Etsy autocomplete (`suggestions_ajax.php`) | 204 egyedi kifejezés 36 magból |
| kínálat + bolt | a Marketplace Insights eredménylapjába ágyazott `listingCards` | 381 listing, boltnévvel, review-val, akciós árral |
| bolt-adat | nyilvános Etsy bolt-oldalak | 34 bolt: eladásszám, kor, katalógusméret, értékelés |

**Amit ez a kör nem mért:** a bolt katalógusának tényleges 3D-arányát és a boltonkénti medián
eladási árat. Emiatt **HUF-bevételt nem számolok** — csak **eladás/hó darabszámot**. A projekt
bevételi képlete ([[methods/revenue-estimation-method]]) enélkül nem alkalmazható tisztességesen.

## Lényeg — emberi nyelven

**1. Két külön piac van egy név alatt, és csak az egyikbe lehet ma belépni.**
A „3D nyomtatás az Etsyn" valójában egy **régi, fizikai** piac (nyomtatott figurák, süteménykiszúrók,
matricák) és egy **új, fájlos** piac. A 26 régi boltból **csak 4-nek van fájlos jele**; mediánjuk 5
éves, 252 termékes, 444 eladás/hó. Ide nem lehet belépni. A 8 új, fájlos bolt mediánja **7 hónapos**
és **208 eladás/hó** — ide igen.

**2. A belépés ideje hónapokban mérhető, nem években.** Mind a nyolc új fájlos bolt **Star Seller**,
és a legfiatalabb **3 hónapos** 717 eladással. Ez élesen más, mint a mostani niche-ben, ahol a
[[findings/catalogue-size-and-throughput]] szerint 100 listing alatt a medián bolt kicsi.

**3. A katalógusméret itt nem számít — a csomag mérete számít.** A `STLCraftVibes` **8 termékkel**
csinált 1348 eladást 9 hónap alatt. A kohorsz mediánja 68 termék, és a termékenkénti forgalom
**2,6 eladás/hó/termék**. Az eladott egység nem egy design, hanem **egy archívum**: a top listingek
„800 TB+ · 2 millió fájl" és „12 000+ articulated animal" típusúak, tartós 50–75%-os „kedvezménnyel".

**4. A legjobban konvertáló kifejezés nem termékről szól, hanem a licencről.** A `commercial use stl`
**4,38‰**-en konvertál — hétszer jobban, mint a mostani niche `layered svg`-je (0,63‰), és
hatvanszor jobban, mint a legnagyobb kereslet/kínálat arányú `gridfinity` (0,07‰). A mintában a
`commercial use` toldatot tartalmazó kifejezések mediánja **2,37‰**, nélküle **0,45‰**.
**Ötszörös különbség, ugyanabban a termékkategóriában.** Aki fájlt vesz kereskedelmi licenccel, az
nem gyűjtő, hanem viszonteladó — dolgozni akar vele, és ezért fizet.

**5. A nagy forgalmú kifejezések nem vevőt hoznak.** A `3d printed` 68 217 keresést kap havonta, és
**0,07‰**-en konvertál; a `3d printed gift` 617 keresésen **nullát**. Az Etsy saját „Shop
customizable ideas" sora is kizárólag **fizikai** terméket ajánl erre. Aki fájlt árul, ezekre a
kifejezésekre nem akar rangsorolni — pontosan úgy, ahogy a `shadow box` sem a mi kifejezésünk, csak
a `shadow box svg`.

## Populáció

- **34 bolt**: 8 új fájlos (kohorsz A) + 26 régi (kohorsz B). **Nem véletlen minta** — a piac látható
  feje. A megszűnt és a soha fel nem rangsorolt boltok szerkezetileg láthatatlanok.
- **381 listing** 20 lekérdezésből, 261 bolttól. Ebből **11 bolt rangsorolt 3+ külön listinggel**.
- **56 keresőkifejezés** mérve, **204 hosszú farok kifejezés** begyűjtve (81 fájl-szándékú).
- **16 hosszú farok kifejezés** mérve volumennel és konverzióval.

## Számok

### Boltok — a két kohorsz

| | kohorsz A (új, fájlos) | kohorsz B (régi) |
|---|---:|---:|
| boltok száma | 8 | 26 |
| kor mediánja | **7 hónap** | 60 hónap |
| katalógus mediánja | **68 termék** | 252 termék |
| eladás/hó mediánja | **208** | 444 |
| Star Seller | **8/8** | — |
| fájlos jel | 8/8 | **4/26** |

A kohorsz A teljes egészében: NenoWorks (3 272 eladás / 8 hó / 420 termék), STLForgeeStudio
(1 495 / 6 / 21), SolvraStudioDesigns (717 / 3 / 96), 3dsaltlab (1 936 / 9 / 141), STLVaultStudio
(806 / 4 / 41), STLCraftVibes (**1 348 / 9 / 8**), ARENPRINT (722 / 10 / 270), TheNovaPrintables
(158 / 3 / 20).

### Hosszú farok — a licenc-szándék kiemelkedik

| kifejezés | keresés/30 nap | listing | keresés/1000 | **konv. ‰** |
|---|---:|---:|---:|---:|
| `commercial use stl` | 129 | 10 521 | 12,3 | **4,38** |
| `stl commercial use` | 124 | 8 354 | 14,8 | **2,58** |
| `flexi animals stl` | 189 | 7 465 | 25,3 | **2,37** |
| `stl bundle commercial use` | 53 | 5 659 | 9,4 | **2,15** |
| `cookie cutter stl bundle` | 43 | 6 387 | 6,7 | **2,13** |
| `articulated dragon stl` | 114 | 8 459 | 13,5 | **1,64** |
| **`stl files commercial use`** | **992** | **11 124** | **89,2** | **1,36** |
| `stl pack` | 1 459 | 44 212 | 33,0 | 0,72 |
| `3d printer stl files` | 398 | 193 854 | 2,1 | 0,33 |
| `planter stl file` | 63 | 8 154 | 7,7 | 0,00 |

**A `stl files commercial use` a mezőny egyetlen olyan tagja, ahol a kereslet/kínálat arány (89,2)
és a konverzió (1,36‰) EGYSZERRE jó**, és a volumen sem elhanyagolható (992 keresés/hó).

### Alterületek, ahogy a vevő nevezi őket

A 204 begyűjtött kifejezés családokba rendezve:

| család | jellemző kifejezések | mit mond |
|---|---|---|
| **licenc-szándék** | `commercial use stl`, `stl files commercial use`, `stl bundle commercial` | a legjobb konverzió, viszonteladói szándék |
| **articulated / flexi** | `flexi animals stl`, `articulated animal stl files bundle`, `flexi dragon`, `articulated hummingbird stl`, `articulated skeleton earrings` | a legnagyobb és legkiforrottabb fájlos család |
| **fájlformátum / csomag** | `stl pack`, `stl files bundle`, `3d print stl files`, `stl figure` | a generikus fájlkeresés, közepes konverzió |
| **szezonális** | `stl file halloween`, `stl bundle halloween`, `3d print stl halloween` | augusztusban a `halloween stl` már 1 958 keresés |
| **nyomtató / eljárás** | `stl bundle fdm`, `stl bundle resin printer`, `print in place stl files` | apró volumen, gyakorlatilag nulla konverzió |
| **fizikai termék** (NEM fájl) | `3d printed cat house`, `3d printed dog bust`, `3d printed earrings`, `3d printed clicker` | a legnépesebb család — de tárgyat akar, nem fájlt |

## Fenntartások

1. **Nincs HUF-bevétel ebben a körben.** Az eladás/hó darabszám, nem pénz. A boltonkénti medián ár
   és a katalógus 3D-aránya hiányzik — enélkül a projekt bevételi képlete nem alkalmazható.
2. **A 34 bolt a látható fej**, nem a piac. Halandóságot nem látunk. Ugyanez a torzítás a
   [[methods/data-collection-pipeline]]-ban is ki van mondva.
3. **Az „eladás/hó" élettartam-átlag.** Egy 3 hónapos boltnál közel van a valósághoz, egy 15
   évesnél nem.
4. **A „217 bolt egyszer szerepelt" NEM piaci szétaprózottság**, hanem mintavételi műtermék: 20
   lekérdezésből ~19 kártyával egy bolt nem is *tud* háromszor megjelenni, hacsak nem uralja a
   mezőnyt. Csak a 3+ csoport valódi jelzés, és az is alsó becslés.
5. **A kohorsz A nyolc boltja kicsi minta**, és a „mind Star Seller" állítás részben szelekciós:
   akit a Marketplace Insights felhoz, az eleve jól teljesít.
6. **Egyetlen augusztusi 30 napos ablak.** A szezonális családok (halloween, karácsony) különböző
   felfutási ponton állnak.

## Provenancia

`wiki/assets/data/3d-print-shops-2026-08-12.json`, `.../3d-print-longtail-2026-08-12.json`,
`.../3d-print-marketplace-insights-2026-08-12.json`. Kapcsolódik:
[[findings/3d-print-first-look]], [[methods/measurement-chain]],
[[methods/revenue-estimation-method]], [[findings/catalogue-size-and-throughput]].
