---
type: Decision
title: Sheet-írás Apps Scripttel, nem API-val
description: A gcloud ADC-t a Google policy tiltja, az rclone tokenben nincs Sheets API — marad a felhasználó által futtatott Apps Script.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Döntés: Apps Script a sheet-íráshoz

**Dátum:** 2026-08-06

## Kontextus

Cellaszintű írás kellett a Google Sheetbe (~50 új sor beszúrása képletekkel). Böngészőből, a Sheets
UI-ban gépelve ez lassú és törékeny lett volna.

## Mérlegelt opciók

1. **gcloud ADC** + Sheets REST API — a felhasználó ezt választotta elsőre.
2. **rclone meglévő Drive tokenje** + Sheets API.
3. **Service account** JSON kulccsal.
4. **Apps Script**, amit a felhasználó futtat.
5. Gépelés a Sheets UI-ban.

## Döntés

**Apps Script.** Én generálom a `.gs` fájlt, a vágólapra másolom, a felhasználó beilleszti és
lefuttatja.

## Miért

- Az **1-es opció megbukott**: a `gcloud auth application-default login --scopes=...spreadsheets`
  hívást a Google letiltotta — *„This app is blocked. This app tried to access sensitive info in your
  Google Account."* Szervezeti policy a gcloud kliensre.
- A **2-es megbukott**: az rclone tokenje az rclone saját OAuth projektjéhez (202264815644) tartozik,
  ahol a Sheets API nincs engedélyezve, és mi nem is engedélyezhetjük.
- A **3-as** működött volna, de GCP projekt + kulcsfájl setupot igényelt volna a felhasználótól.
- Az **5-ös** ~50 sor × 15 cella kézi gépelést jelentett volna, autocomplete-hibákkal.

## Következmények

Minden sheet-írás generált `.gs` fájl, ami:
- **előbb ellenőriz, aztán ír** — minden horgonysort validál, és eltérésnél hibával leáll,
- **alulról felfelé szúr be**, hogy a sorszámok ne csússzanak,
- **nem ír felül nem üres fület** (`OVERWRITE` kapcsolóval felülbírálható).

Eddig: `update-revenue-estimation.gs`, `fill-niche-sheet.gs`, `fill-functional-sheet.gs`.
Lásd [[workflows/sheet-updates]].
