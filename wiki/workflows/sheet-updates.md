---
type: Workflow
title: Hogyan írunk a Google Sheetbe
description: Generált Apps Script, ami előbb validál, alulról felfelé szúr be, és nem ír felül nem üres fület.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Sheet-frissítés

Minden írás **generált Apps Script**, amit a felhasználó futtat — az indoklás:
[[decisions/2026-08-06-apps-script-for-sheets]].

## A minta

1. **Generátor szkript** (`assets/scripts/gen_*.py`) beágyazza az adatot egy `.gs` fájlba.
2. `node --check` szintaxis-ellenőrzés (a `.gs` érvényes JS).
3. Másolás a projektgyökérbe **és** `pbcopy`-val a vágólapra.
4. A felhasználó: `Bővítmények → Apps Script`, beilleszt, futtat.

## Kötelező biztonsági elemek minden generált szkriptben

- **Előbb validál, aztán ír.** Minden horgonysort ellenőriz (dátum + várt bolt URL-je), és
  eltérésnél `throw`-ol, **mielőtt** bármit módosítana.
- **Alulról felfelé szúr be**, hogy a sorszámok ne csússzanak el menet közben.
- **Nem ír felül nem üres fület** — `OVERWRITE = false` az alapértelmezés.
- A fület `getSheetId()` alapján keresi, nem név alapján (a nevet a felhasználó átírhatja).

## Meglévő szkriptek

| fájl | fül | mit csinál |
|---|---|---|
| `update-revenue-estimation.gs` | gid 541292880 | 49 új 2026-08-06-os sor + a Qagazzz sor kitöltése |
| `fill-niche-sheet.gs` | gid 1600752523 | 173 layered bolt, kedvezmény és korrigált bevétel oszlopokkal |
| `fill-functional-sheet.gs` | gid 594784454 | 73 funkcionális bolt, katalógus-aránnyal |

## A `revenue estimation` fül képlet-konvenciói

A 2026-os sorokban: `L =D/E`, `M =500000/L`, `O =days(A,N)/365`, `P =E-Eelőző`, `Q =F-Felőző`,
`R =(F-Felőző)*Kelőző/24`. A `D` (HUF/hó) és `K` (medián ár HUF) kézi érték.

**Az alsó „dog svg" blokkban (60–80. sor) a HUF-os medián ár az `I` oszlopban van, nem `K`-ban** —
ott az `R` képlet `I`-re hivatkozik.

**Konvenció:** üres 2026-os sor (csak dátum) = a bolt épp nem üzemel.
