---
type: Pitfall
title: Jó depth mapből széteső macska — eltérő rétegtranszformáció
description: A legalsó kivágott lapot tömör panelnek tekintő margóillesztés és a globális zárás roncsolta a szem és fül nyílásait.
status: stable
generated:
  by: codex
  at: 2026-09-05
sources:
  - resource: ../../product/catalog/recessed-papercut/runs/2026-09-05-v1/output/plate.png
  - resource: ../../product/catalog/recessed-papercut/runs/2026-09-05-v2/output/plate.png
  - resource: ../../product/catalog/recessed-papercut/runs/2026-09-05-v2/output/layers/report.json
  - resource: ../../tests/test_trace_geometry.py
  - resource: ../../tests/test_trace_export.py
---

# Tünet

A recessed-papercut v1 depth mapen felismerhető macska szeme a plate/styled képen darabokra esett, a fül elvált. A geometriai riport mégis zöld volt: a hibás alakzatok mechanikai mérőszámai megfeleltek. Már a trace réteg-előnézete is hibás volt, ezért a Blender önmagában nem lehetett az ok.

# Gyökérok

A margóillesztés a legalsó **kivágott** lapból vonta ki a többi réteg anyagát, mintha az tömör panel volna. Az így kapott részleges nyílásokat körülbelül 21 mm-rel eltolta; az alsó réteg szem/fül nyílásai helyben maradtak. A nesting metszés a két pozíciót összekeverte.

Ezen túl a teljes panel keretszélének összezárása és a margó 2,5 mm sugarú globális zárása a belső dekoratív nyílásokat is betömte. Az illesztés javítása után a fül helyreállt, de a szem csak e második hiba javításával maradt ép.

# Alkalmazott korrekció

A `fit_panel_openings` minden lap nyílását a teljes panelből számítja, és mindegyikre ugyanazt az eltolást és skálázást alkalmazza. A keret varratjavítása csak a varrat közelében adhat anyagot. A margó hozzáadása után nincs globális zárás; a szokásos anyagvastagsági és nyakellenőrzés változatlanul fut.

A v2 ugyanazokat a depth-map- és palettabájtokat használja, mint a v1. Tényleges trace + Blender plate/styled futás és vizuális ellenőrzés történt. A hat kivágott réteg most hat darab (v1: tizenegy), plusz egy tömör hátlap. Mindkét változatban 0 nyak; a legrosszabb vékonyterület 0,03%-ról 0,02%-ra változott. A mechanikai javulás mellett a szem, pupilla, fül és a hosszú sötét nyakszalag is megmaradt.

# Tanulság

A geometriai biztonság és a képhűség két külön ellenőrzés. A közös transzformáció tesztje tartalmazzon nyílást a legalsó kivágott rétegen is; a végponti SVG-teszt tartalmazzon keskeny dekoratív nyílást, amely nem anyaghíd. A javítás akkor indokolt, ha a forrás és a feldolgozás köztes kimenete megmutatja az első eltérést. Lásd [[2026-08-11-a-szuro-torolte-a-felso-lapokat]] és [[workflows/engineering-quality]].
