---
type: Finding
title: Layered SVG vs 3D nyomtatás — azonos alapú összehasonlítás
description: A 3D oldal a mediánon KEVESEBBET keres (489 vs 707 ezer HUF/hó), de egytizednyi katalógussal. A különbség nem a bevételben van, hanem a listingenkénti hozamban — és a 3D szórása kétszer akkora.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T19:00:00Z
sources:
  - resource: /assets/data/niche-comparison-2026-08-12.json
    title: 30 layered + 15 3D bolt, azonos módszerrel, azonos napon
---

# Layered SVG vs 3D nyomtatás

## Miért kellett újramérni

A két oldal bevételi számai **eddig nem voltak összehasonlíthatók**: a layered a projekt saját
képletével készült (akciós ár × katalógus-arány), a 3D SalesDoe listaárral. Ezért 2026-08-12-én
**mindkét oldalt újramértem SalesDoe API-val, ugyanazon a napon, ugyanazzal a képlettel**:

```
HUF/hó = eladás/hó × medián ár (SalesDoe) × árfolyam
```

Ez **mindkét oldalon felső becslés** (a SalesDoe ára a lista- és az akciós ár között ingadozik) —
de a torzítás **ugyanaz a két oldalon**, ezért az *összehasonlítás* érvényes, még ha az abszolút
számok nem is.

## Lényeg

**A 3D oldal a mediánon kevesebbet keres — de egytizednyi katalógussal.**

Az auditált layered populáción a medián **706 907 HUF/hó**, a 3D oldalon **489 456** — a 3D
**31%-kal alacsonyabb**. Ugyanakkor a layered medián bolt ehhez **326 listinget** tart, a 3D-s
**33-at**. Listingenként ez **1 845 vs 11 698 HUF/hó**, és a p75-nél a szakadék még nagyobb
(3 967 vs 33 716).

**Vagyis nem az a kérdés, melyik piac gazdagabb, hanem hogy mibe kerül bennmaradni.** Azonos
bevételhez a layered oldalon nagyságrenddel több terméket kell megcsinálni és karbantartani.

**Amit cserébe kapsz: kétszer akkora szórást.** A 3D p90/p10 aránya **23,0×**, az auditált layeredé
**12,0×**, és az alsó tizedben a 3D lényegesen rosszabb (59 782 vs 165 287 HUF/hó). Ez nem „jobb
piac", hanem **más kockázati profil**.

## Populáció

- **layered: 20 bolt** — az **auditált 21-es** populációból ([[pitfalls/2026-08-08-wrong-unit-of-independence]]),
  amelyből a `PremiumLaserFiles` nem adott mai adatot. Kritérium: legalább 3 **különálló** listinggel
  rangsorolt, és a katalógusmintája legalább 80%-ban layered.
  Az első körben tévedésből a **hibás, nem deduplikált 33-as** listán számoltam; azt az oszlopot
  dokumentációként meghagytam.
- **3D: 15 bolt**, a Marketplace Insights által felhozott listingek boltjaiból. **Nem véletlen
  minta** — a piac látható feje.

## Számok

### Bevétel-percentilisek (HUF/hó, azonos módszer, egységes percentilis-definícióval)

| | layered, hibás 33-as (n=30) | **layered AUDITÁLT (n=20)** | 3D (n=15) |
|---|---:|---:|---:|
| p90 | 1 576 544 | **1 981 604** | 1 375 096 |
| p75 | 870 106 | **1 175 324** | 1 127 958 |
| **medián** | 419 658 | **706 907** | 489 456 |
| p25 | 248 439 | **346 769** | 277 013 |
| p10 | 138 475 | **165 287** | 59 782 |
| p90/p10 szórás | 11,4× | 12,0× | **23,0×** |

**Az első oszlop dokumentációként marad benne**, mert eredetileg azon számoltam — és pont ez volt a
hiba: a 33-as lista a nem deduplikált szűrőn alapul. Az auditált 21-ből 20-hoz volt mai
SalesDoe-adat (a `PremiumLaserFiles` nem adott).

### A ráfordítás — itt a valódi különbség

| | layered auditált | 3D |
|---|---:|---:|
| listing medián | **326** | **33** |
| HUF/listing p25 | 1 026 | 2 860 |
| HUF/listing **medián** | 1 845 | **11 698** |
| HUF/listing p75 | 3 967 | **33 716** |
| kor medián | 38 hónap | 7 hónap |

### Kor-kontroll — csak a 12 hónapnál fiatalabbak

| | layered auditált (n=**4**) | 3D (n=13) |
|---|---:|---:|
| medián HUF/hó | 827 190 | 835 832 |
| listing medián | 404 | **31** |
| HUF/listing | 1 386 | **17 762** |

**Ezt a sort n=4 mellett nem szabad következtetésnek venni** — a négy bolt (BKCUT, ApexLayer3D,
FanfenStudio, CutingDesignsSVG) közül kettő vietnámi tömegtermelő. Irányjelzőnek annyit mond, hogy
a fiatal boltoknál a bevétel közel azonos, a listingszám-különbség viszont **nem tűnik el**.

### A két szélső eset

| | legjobb | legrosszabb |
|---|---|---|
| layered auditált | MagicVectorLaser 3 338 072 HUF/hó (933 listing) | CutingDesignsSVG 254 172 (211 listing) |
| 3D | NenoWorks 1 472 832 HUF/hó (420 listing) | AuraPrint3D 16 079 (33 listing) |

## Niche-k és fókusz

### A layered oldalon

A kereslet ott van, ahol **fájlt** keresnek, nem terméket: `shadow box svg` **79,2** keresés/1000
listing és **0,92‰** konverzió — ez a niche legjobb kombinációja, és jobb, mint maga a
`layered svg` (5,9 / 0,63‰). A `multilayer svg` (22,2 / 0,20‰) és a `layered mandala svg`
(7,4 / 0,18‰) gyenge konverziójú.

**Fókusz:** a `shadow box svg` szócsalád, és a [[findings/paper-layered-market]] szerint a papíros
oldal — de távtartóval és keretmérettel, mert a vevői fájdalom ott van.

### A 3D oldalon

A legjobban konvertáló kifejezés **nem termékről szól, hanem a licencről**: `commercial use stl`
**4,38‰**, `stl commercial use` 2,58‰, `stl bundle commercial use` 2,15‰. A `commercial use`
toldattal a medián konverzió **2,37‰**, nélküle **0,45‰** — ötszörös.

Az egyetlen kifejezés, ahol a **kereslet/kínálat arány és a konverzió is jó**:
**`stl files commercial use`** — 992 keresés/hó, 89,2 keresés/1000 listing, 1,36‰.

Termékcsaládként az **articulated / flexi** a legkiforrottabb (`flexi animals stl` 25,3 / 2,37‰).
Kerülendő a `3d printed …` család: az tárgyat akar, nem fájlt (`3d printed` 68 217 keresés,
**0,07‰**).

**Fókusz:** kereskedelmi licenccel árult, articulated/flexi témájú fájlcsomag, `commercial use`
kulcsszóval a címben.

## Fenntartások

1. **Túlélési torzítás, és a két oldalon különböző irányú.** A 3D minta 13/15-ben egy évnél
   fiatalabb boltokból áll, akik **most rangsorolnak** — a megbukott fiatal boltok láthatatlanok.
   A layered oldalon több az idős túlélő. **Ez a legsúlyosabb fenntartás**: a 3D oldal
   `HUF/listing` fölényét is felfelé torzítja, mert csak a beváltókat látjuk.
2. **Az élettartam-átlag a régi boltokat bünteti.** Egy 32 hónapos bolt átlagát lehúzza a lassú
   indítás; egy 7 hónaposét nem. A layered medián ezért valószínűleg **alulbecsli** a jelenlegi
   futásteljesítményt — vagyis a valós különbség kisebb lehet, mint a táblában.
3. **Mindkét oldal felső becslés** (SalesDoe lista-vs-akciós ár), és a 3D oldalon a tartós 50–75%-os
   akció miatt a torzítás valószínűleg **nagyobb**.
4. **n = 20 vs 15.** Mindkét oldal percentilisei bizonytalanok, a p90 és a p10 különösen.
5. **A katalógus-arány egyik oldalon sincs bekalkulálva** — a projekt saját képletének `layered%`
   szorzója itt nem szerepel, tehát ez nem ugyanaz a szám, mint a [[findings/verified-shop-list]]-en.
6. **Az „egyötöd annyi idő" állítást visszavontam.** A kor mediánját mértem, nem a bevételig eltelt
   időt — time-to-revenue mutatót ez az adat nem tartalmaz.
7. **A 3D medián (489 456) a leggyengébb egyedi szám** az egész táblában: szelektált mintából jön,
   SalesDoe-árral, nagyon fiatal boltok élettartam-átlagából, és a mediánt adó bolt katalógusának
   digitális aránya nincs ellenőrizve.

## Amit még meg kell mérni a döntés előtt

Egy teljes, **induláskor rögzített kohorsz 12 hónapos kimenetele** mindkét oldalon: az összes új
bolt hány százaléka ér el egy éven belül érdemi havi bevételt — a **nem rangsorolókat, a nulla
közelieket és a bezártakat is beleértve**, tényleges akciós árakkal. Ez adná meg azt, amit ez a
tábla nem tud: nem azt, hogy a *most látható nyertesek* hogyan néznek ki, hanem hogy **belépőként
mekkora eséllyel** jutsz oda.

## Provenancia

`wiki/assets/data/niche-comparison-2026-08-12.json`. Kapcsolódik:
[[findings/verified-shop-list]], [[findings/3d-shop-list]],
[[findings/3d-print-market-structure]], [[methods/browser-data-endpoints]],
[[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]].
