---
type: Schema
title: Wiki séma — hogyan olvasd és tartsd karban ezt a tudásbázist
description: Az etsy-something kutatási wiki karbantartási szerződése; minden munkamenet ezt olvassa el először.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Wiki séma

Ez egy **LLM által karbantartott tudásbázis egy piackutatási projekthez**, nem kódbázishoz. Karpathy
LLM Wiki mintáját követi (kereszthivatkozott Markdown mappák, séma-fájl, append-only napló), minden
fogalmi oldalon [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
frontmatterrel.

Az általános mintától eltér, mert ebben a projektben **nincs kód, nincs git, nincs build tooling**. A
szokásos `apps/`, `features/`, `integrations/`, `tech-debt/` kategóriák nem értelmezhetők, ezért
kimaradtak. A `bugs/` helyett [[pitfalls/_index|pitfalls]] van — kutatásban a visszatérő hiba egy
*mérési* hiba, és ezek a postmortemek a legértékesebb tartalom itt.

## A három réteg

1. **Források (csak olvasható alapigazság).**
   - A Google Sheet `1j-52jMBxTxgZ3-ywNekNGKjraP6u2QYDKxLVdMfsqUQ` — fülek: `revenue estimation`
     (gid 541292880), layered niche (gid 1600752523), funkcionális szegmens (gid 594784454).
   - Maga az Etsy (boltoldalak, keresési találatok).
   - SalesDoe (`salesdoe.com/shop-overview`) — a felhasználó bejelentkezett böngésző-munkamenetét igényli.
   - Apify actorok — lásd [[methods/apify-actors]].
   - `assets/data/` — a 2026-08-06/07-én lehúzott nyers JSON adatok. Ezek **változatlanok**;
     újra-előállításuk pénzbe és élő böngésző-munkamenetbe kerül.
   - `assets/scripts/` — az elemző szkriptek, amik a `findings/` minden számát előállították.
2. **A wiki (írható).** Minden az `assets/`-en kívül.
3. **A séma.** Ez a fájl.

## Mikor frissítsd

- **Új mérés fut le** (új keresés, új Apify lehúzás, új SalesDoe kör) → frissítsd vagy hozd létre a
  megfelelő `findings/` oldalt, és tedd a nyers adatot az `assets/data/`-ba.
- **Egy szám megváltozik** korrekció miatt → frissítsd a finding oldalt **és** írj egy
  `pitfalls/YYYY-MM-DD-<slug>.md`-t arról, mi volt rossz és hogyan derült ki. Soha ne írj felül
  csendben egy számot; írd le a régi értéket és azt, miért mozdult.
- **Döntés születik** irányról, eszközről, módszerről → `decisions/YYYY-MM-DD-<slug>.md`.
  A **Miért** szakasz a lényeg.
- **Egy referenciaboltot megvizsgálunk** → `shops/<név>.md`.
- **Egy ismételhető eljárás kialakul** → `workflows/`.
- **Egy fogalmat vagy metrikát definiálni kell** → [[glossary]].
- **Felmerül egy kérdés, ami újra fel fog** → [[faq]].
- **Mindig** fűzz egy önmagában érthető sort a [[_log]]-hoz.

## Mikor NE frissítsd

- Ha csak megismételnéd, amit az adathalmaz már tartalmaz — inkább hivatkozz az
  `assets/data/<fájl>.json`-ra.
- Tervek, szándékok. Ez a wiki azt rögzíti, amit *megmértünk* és amit *eldöntöttünk*, nem azt, amit
  szeretnénk.
- Beszélgetés-menet. Csak a következtetés és a provenancia marad meg.

## Hogyan írj oldalt

- **Egy fogalom egy oldal.** ~200 sor felett bontsd ketté.
- **Előbb a válasz, utána a provenancia.** Minden nem magától értetődő szám mellett ott van, honnan
  jön: melyik adathalmaz, melyik szkript, melyik populáció.
- **Mindig írd oda a populációt.** Egy szám a populációja nélkül (`173 bolt` vs `35 specialista` vs
  `21 igazolt`) rosszabb, mint a semmi — ez a projekt pontosan ezen égett meg. Lásd
  [[pitfalls/2026-08-07-whole-shop-revenue-attribution]].
- **Abszolút dátumok**, `YYYY-MM-DD`. Soha nem „nemrég" vagy „jelenleg".
- **Hivatkozz bőven** Obsidian-stílusú kettős szögletes zárójellel, az oldal útvonalát megadva
  (pl. a findings mappa egy oldalára `findings/pricing-and-discounting` néven).
- **Az ellentmondást jelezd**, ne írd felül: tartsd meg az igazabb változatot, és rögzítsd a
  korrekciót a [[_log]]-ban és egy `pitfalls/` oldalon.
- **A frontmatter kötelező** minden oldalon a `_log.md` és az `_index.md` fájlok kivételével:
  `type`, `title`, `description`, `status`, `generated`, és `sources` ott, ahol az állítás
  adathalmazon nyugszik.

## Oldalvázak

**`decisions/`** — Kontextus / Mérlegelt opciók / Döntés / **Miért** / Következmények / Mikor vizsgáljuk újra.

**`pitfalls/`** — Tünet / **Gyökérok** / Hogyan derült ki / Alkalmazott korrekció / Tanulság.
A Tanulság úgy legyen megfogalmazva, hogy *jövőbeli* munkán is ellenőrizhető legyen, ne csak ezen az eseten.

**`findings/`** — Lényeg / Populáció / Számok / Fenntartások / Provenancia.

**`_log.md`** — append-only, legújabb elöl, soronként egy önmagában érthető bejegyzés:
`YYYY-MM-DD — mi változott és miért (oldal)`.

## Megbízhatósági szókincs

Ezeket használd következetesen; definíciójuk a [[glossary]]-ben:

- **igazolt (verified)** — a bolt saját katalógusát mintavételeztük, és megerősíti a besorolást.
- **specialista** — legalább 3 *különálló* listinggel rangsorolt a niche keresésekben, katalógus nincs mintavéve.
- **igazolatlan (unverified)** — csak keresési találatban szerepelt. Mintavételig zajnak tekintendő.

## A séma fejlesztése

Csak akkor adj hozzá kategóriát, ha a tartalom tényleg egyikbe sem fér be. Hozd létre a mappát és az
`_index.md`-t, vedd fel ide a fába, adj hozzá „Mikor frissítsd" triggert, linkeld az [[index]]-ből,
és naplózd. Alapértelmezés: **ne** adj hozzá.
