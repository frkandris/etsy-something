---
type: Finding
title: Mekkora és mennyire zsúfolt a layered niche
description: 173 látható bolt, ebből 33 katalógussal igazolt; az igazolt medián 320 ezer HUF/hó, és 47 új bolt nyílt az elmúlt évben.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/niche_rows.json
    id: pop
    title: 173 bolt Etsy bolt-szintű adattal
  - resource: /assets/data/layered_adjusted.json
    id: clean
    title: 65 specialista katalógusból számolt layered aránnyal
---

# A layered niche mérete és szerkezete

## Lényeg

A niche **valós és népes — nem két szerencsés bolt** —, de zsúfolt, épp elárasztás alatt áll, és a
medián szereplő szerényen keres.

## Populáció

2026-08-07-én épült öt Etsy keresésből (`multilayer svg laser cut`, `multilayer svg`,
`3d layered mandala svg`, `layered svg laser cut file`, `3d multilayer svg dxf`), keresésenként 100
listing = 500 listing → **173 különálló bolt**. Innen szűrve 65 **specialistára** és 33 **igazolt**
boltra (definíciók: [[glossary]]; a szűrés története: [[overview]]).

## Számok — igazolt populáció (33 bolt)

| sáv | boltok |
|---|---:|
| >2M HUF/hó | 3 |
| 1–2M | 1 |
| 500k–1M | 7 |
| 200–500k | 11 |
| <200k | 11 |

**Medián 320 156 HUF/hó. Felső kvartilis 617 358.**

## Számok — nyers populáció (173 bolt), a zsúfoltsághoz

| sáv | boltok |
|---|---:|
| >2M HUF/hó | 11 |
| 1–2M | 12 |
| 500k–1M | 19 |
| 200–500k | 45 |
| 50–200k | 42 |
| <50k | 43 |

**A 173 boltból 47 az előző 12 hónapban nyílt** (27%), medián 57 listinggel és 61 ezer HUF/hó-val. A
belépési küszöb láthatóan leesett — feltehetően ugyanaz az AI-eszközkészlet miatt, ami a mi
belépésünket is olcsóvá tenné. Ez kétélű, és ez a fő ok, amiért árréscsökkenésre kell számítani.

## Bezárt boltok

**Nulla** a mintában. Ez nem eredmény, hanem műtermék: a populáció *aktuális* keresési találatokból
épült, tehát a megszűnt boltok szerkezetileg láthatatlanok. Halandóságot így nem lehet mérni. Az
egyetlen valós halandósági számunk a 2024-es követő kohorszból jön — 57 boltból 13 tűnt el két év
alatt, lásd [[findings/2024-vs-2026-cohort]].

## Fenntartások

- A bevétel **élettartam-átlag** (összes eladás ÷ nyitás óta eltelt hónapok × mai ár), nem aktuális
  futásteljesítmény. Lásd [[methods/revenue-estimation-method]].
- A keresési mintavétel azokat a boltokat részesíti előnyben, amelyek ma jól rangsorolnak; egy valós
  bevételű, de ezekre az öt kifejezésre gyengén optimalizált bolt hiányzik.
- A „173 bolt" a keresésenkénti top ~100 találatban látható szám, nem a piac mérete.

## Provenancia

`assets/scripts/niche.py` (nyers populáció), `assets/scripts/adjust.py` (katalógus-korrekció),
`assets/scripts/layered_deep.py` (igazolt populáció bontásai).
