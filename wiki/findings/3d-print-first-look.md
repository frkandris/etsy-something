---
type: Finding
title: 3D nyomtatás az Etsyn — első mérés, és miért nem elég az irányváltáshoz
description: Az Etsy saját keresési adata szerint a 3D-fájlpiac kereslet/kínálat aránya nagyságrenddel jobb a layered SVG-nél, de a konverzió ezt nem követi, és a két adathalmaz populációja nem ugyanaz. A mérés önmagában nem dönti el a kérdést.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T12:00:00Z
sources:
  - resource: /assets/data/3d-print-marketplace-insights-2026-08-12.json
    title: Etsy Marketplace Insights, 40 kifejezés
  - resource: /assets/data/3d-print-etsy-sweep-2026-08-12.json
    title: böngészős találati-lista mintavétel, 24 lekérdezés
  - resource: /assets/data/3d-print-arxiv-2026-08-12.md
    title: szakirodalmi felmérés (arXiv-fókusz), 1170 sor, 97 tétel
---

# 3D nyomtatás az Etsyn — első mérés

## Lényeg

A 3D-fájlpiac **kereslet/kínálat aránya nagyságrenddel jobb**, mint a mostani niche-é: a
`layered svg` **5,9 keresés / 1000 listing**, a 3D-terminusok **mediánja 26,9**, a `3d print files`
pedig **172,9**. Ez 34 használható kifejezésen mérve.

**Ez viszont önmagában nem dönti el a kérdést**, és három okból nem szabad irányváltásnak olvasni:

1. **A konverzió nem követi az arányt.** A három legjobb kereslet/kínálat arányú kifejezés
   (`gridfinity` 322,7 · `lithophane` 212,7 · `3d printed lamp` 183,5) mind a **legrosszabb
   konverziós sávban** van (0,07–0,18 eladás/1000 keresés). Fordítva: a `fidget toy stl` aránya
   csak 5,9, a konverziója viszont **2,16** — a mezőny legjobbja. Ez két külön piac.
2. **A populációk nem azonosak.** Az `avgTotalListings` nem deduplikált termékszám: ugyanaz a
   mega-bundle több kifejezés kínálatába is beleszámít, és egy fizikai tárgy, egy önálló STL meg
   egy kétmillió fájlos archívum egyaránt egy listing.
3. **Egyetlen 30 napos ablak**, augusztusban. A `halloween stl` (62,1) és a `christmas stl` (15,9)
   különböző szezonális felfutási ponton áll.

## Populáció

- **40 keresőkifejezés** mérve Etsy Marketplace Insightsban (LasercutSupplier bolt, Etsy Plus),
  2026-08-12. Ebből **34 használható**: a `print in place` (9 keresés / 68 747 listing) mérése
  szemét — az Etsy három közönséges szónak veszi, nem lekérdezésnek —, az `ams multicolor stl`
  pedig nem adott adatot, a maradék négy a saját niche alapértéke.
- **24 lekérdezés** böngészős találati-lista mintája. **Fontos korlát:** az Etsy lekérdezésenként
  csak az **első ~12 kártyát** rendereli szerveroldalon, magyar, személyre szabott találati listán.
  Minden ebből számolt arány (digitális %, mediánár, review-összeg) **erre a 12 találatra**
  vonatkozik, nem a piacra.

## Számok

### Kereslet / kínálat — a legjobb és a legrosszabb vég

| kifejezés | keresés / 30 nap | listing | **keresés / 1000** | konv. ‰ |
|---|---:|---:|---:|---:|
| `gridfinity` | 1 006 | 3 117 | **322,7** | 0,07 |
| `lithophane` | 1 328 | 6 243 | **212,7** | 0,18 |
| `3d printed lamp` | 2 636 | 14 369 | **183,5** | 0,07 |
| `3d print files` | 45 614 | 263 787 | **172,9** | 0,57 |
| `articulated dragon` | 1 659 | 15 710 | **105,6** | 0,49 |
| `3d printer files` | 19 504 | 208 796 | **93,4** | 0,53 |
| … | | | | |
| **`layered svg` (a mostani niche)** | **1 103** | **185 987** | **5,9** | **0,63** |
| `wall art stl` | 115 | 54 615 | 2,1 | 0,57 |
| `3d printed gift` | 617 | 366 235 | 1,7 | 0,00 |

### Konverzió szerint — más sorrend

| kifejezés | konv. ‰ | keresés / 1000 | keresés / 30 nap |
|---|---:|---:|---:|
| `fidget toy stl` | **2,16** | 5,9 | 72 |
| `stl bundle` | **1,22** | 35,8 | 2 133 |
| `dice tower stl` | **1,19** | 33,4 | 268 |
| `planter stl` | 0,92 | 26,3 | 306 |
| `shadow box svg` *(saját niche)* | 0,92 | 79,2 | 2 679 |
| `headphone stand stl` | 0,71 | 24,6 | 96 |
| `layered svg` *(saját niche)* | 0,63 | 5,9 | 1 103 |

**A saját niche konverziója nem rossz** — a `layered svg` 0,63‰-e a 3D-mezőny felső harmadában
lenne. Amiben elmarad, az kizárólag a kereslet/kínálat arány.

## Alterületek — mi látszik a kínálati oldalon

A találati listák teteje (top ~12/lekérdezés) alapján:

- **Mega-bundle a fájlos oldal domináns terméke.** „800 TB+ · 2 millió fájl" 3 143 HUF-ért 70%
  „kedvezménnyel", „12 000+ articulated animal" 846 HUF-ért 75%-kal. Az eladott egység már nem egy
  design, hanem **egy archívum**. A tartós kedvezmény ugyanaz a minta, amit a
  [[findings/pricing-and-discounting]] a layered oldalon dokumentált, csak szélsőségesebben.
- **A bundle-eladók nem tisztelik a technológiai határt.** A `stl files` top találatai közt van egy
  **720 000+ lézervágott fájlos** csomag (svg dxf cdr ai eps, CNC és Glowforge) 638 HUF-ért, 210
  review-val, és egy 8 000+ keychain csomag STL-t *és* SVG-t együtt ad. Aki ide belép, ugyanazokkal
  az aggregátorokkal versenyez, akik a mostani niche-ben is ott vannak.
- **Az Etsy maga fizikai irányba tereli a `3d printed` lekérdezést.** A „Shop customizable ideas"
  sor kizárólag személyre szabott **fizikai** terméket ajánl (name sign, portré-figura, logó), nem
  fájlt. A `3d printed name sign` top-12-jében a listingek **42%-a** digitális, a `3d print wall
  art`-nál 54% — szemben a tiszta fájl-kifejezések ~92%-ával.

## Fenntartások

A codex-elemzés öt pontja, amiket megtartok kritikaként a saját mérésemmel szemben:

1. **A `keresés / 1000 listing` önmagában nem elég.** Fedezet/óra kell mellé, mert a magas arány
   fakadhat abból is, hogy a kereslet olyasmit akar, amit nem a mi termékformánk szolgál ki. A
   [[findings/review-mining]] norse/kelta bukása pontosan ez volt.
2. **A `gridfinity` gyanús pontosan úgy, ahogy a norse/kelta volt.** Kiváló arány, majdnem nulla
   konverzió — valószínűleg más termékformát keresnek (kész tárolót, nem fájlt).
3. **A függetlenségi egység csapdája ismét fenyeget.** Ha ugyanaz a mega-bundle tíz lekérdezésben
   feljön, az **egy listing és egy eladó**, nem tíz adatpont — ez a hiba egyszer már 65
   „specialistát" vitt le 35-re ([[pitfalls/2026-08-08-wrong-unit-of-independence]]).
4. **A review-összegek élettartam-adatok**, nem friss kereslet, és eladó szerint nincsenek
   deduplikálva. Gyenge jel, csak irányjelzőnek használható.
5. **A layered alapérték két különböző napról nem keverhető.** A 2026-08-07-i mérés 1 200 keresés /
   189 900 listing, a mostani 1 103 / 185 987. Egy táblában csak azonos napi értékek szerepelhetnek
   — ebben az oldalban végig a **2026-08-12-i** szám van.

## Amit a szakirodalom hozzátesz

A párhuzamos arXiv-kutatás (`assets/data/3d-print-arxiv-2026-08-12.md`, 1170 sor, 97 tétel) hat
dolgot mond, ami a terméktervezést közvetlenül érinti:

- **A fizetős fájl nem geometriát ad el.** A Thingiverse 158 373 modelljének **90,6%-a nyílt
  licencű**, és a CC-licenceknek csak 13,8%-a tiltja a kereskedelmi felhasználást. Amit fizetni
  érdemes: **garantáltan ép háló** és **dokumentáció** — a repozitóriumok tele vannak nem-manifold,
  önmetsző hálókkal.
- **A letöltésszám nem kereslet.** 30 népszerű modellen 500 nap alatt **7 823 249 letöltésre
  19 425 elkészített darab** jutott, és az arány romlott. Bármilyen volumenbecslés, ami letöltésre
  épül, nagyságrendekkel felülbecsül.
- **A generatív 3D látványra optimalizál, nem nyomtathatóságra.** A TRELLIS nyers kimenetének
  normalizált támaszigénye 0,343, nyomtathatóságra optimalizálva 0,176; a részlet a textúrában van,
  ami egyszínű nyomtatásnál **elvész**.
- **Licencbuktató, ami ránk vonatkozik:** a Hunyuan3D 2.0 és 2.1 licence szó szerint **nem
  érvényes az Európai Unióban** — Magyarországról nem használható jogtisztán. Ami igen: TRELLIS
  (MIT), TripoSR/TripoSG (MIT), InstantMesh (Apache-2.0), Shap-E (MIT). Ugyanaz a hibaosztály,
  mint a Depth Anything V2-nél (Small Apache-2.0, Large CC-BY-NC).
- **A parametrikus sablon erősebb termék, mint a kész fájl.** A metamodelleket **többször
  hasznosítják újra, mint az általuk generált konkrét modelleket** (Kyriakou, MIS Quarterly), és a
  saját tervezésű termékre a fizetési hajlandóság kb. **+100%** (Franke–Schreier). **De** a prémium
  az *érzékelt saját hozzájáruláson* múlik: egy „egy kattintás, kész" automata személyre szabás
  kevesebbet érhet, mint egy lassabb, látható konfigurátor.
- **A print-in-place tervezési ablak: két szám, és ennyi az egész irodalom.** **0,5 mm** minimális
  hézag az összeolvadás ellen (FDM/PLA), és **0,15–0,25 mm** az optimum egy 10 mm-es forgó ízületen
  (FFF/PLA). Anyagra és rétegmagasságra bontott táblázat **nincs** — ez ugyanaz a szerepű szám itt,
  mint a papírvágásnál a 2 mm-es minimális web, tehát **magunknak kell megmérnünk**.

## Amit legközelebb meg kell mérni

Egy szám hiányzik, és az dönt: **fedezet termékfejlesztési óránként**, azonos időszakban, azonos
feltételekkel futó párhuzamos teszttel — ugyanannyi új listing mindkét irányba, egyszerre indítva,
azonos hirdetési feltétellel, és listingenként mérve a megjelenést, kattintást, rendelést, nettó
bevételt és a tényleges fejlesztési időt.

Két dolog van, amire **egyáltalán nincs irodalom**, és a döntést mindkettő érinti: az Etsy
digitális letöltésekről nulla tudományos munka van (a Printables/Cults3D/MyMiniFactory
akadémiailag nem létezik, és semmi nincs a fizetős STL árazásáról vagy árrugalmasságáról), és
**nincs független benchmark arról, hogy melyik generátor hány százalékban ad vízhatlan, javítás
nélkül szeletelhető hálót** — pedig pontosan ez a szám dönti el, használható-e a generatív 3D
termékgyártásra.

**Pilot nélkül nem váltanék.** Az adat azt támasztja alá, hogy a 3D-fájlpiac **erősebb validációt
érdemel**, nem azt, hogy jobb.

## Provenancia

`wiki/assets/data/3d-print-marketplace-insights-2026-08-12.json` (Etsy Marketplace Insights, 40
kifejezés), `wiki/assets/data/3d-print-etsy-sweep-2026-08-12.json` (böngészős minta, 24
lekérdezés). Kapcsolódik: [[findings/etsy-first-party-search-data]],
[[findings/keyword-demand-sweep]], [[findings/pricing-and-discounting]],
[[findings/review-mining]], [[pitfalls/2026-08-08-wrong-unit-of-independence]].
