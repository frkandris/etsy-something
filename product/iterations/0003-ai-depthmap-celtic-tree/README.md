# 0003 — AI mélységtérkép: kelta életfa

Első kép-vezérelt iteráció: gpt-image-2 rajzolja a motívumot 6 lapos szürkeszintű
mélységtérképként (`00_generate.py`), a `02_trace.py` poszterizál → potrace → shapely →
SVG/DXF + vágásbiztonsági riport. MIN_PART=400 trükk: 116→11 ragasztandó darab.
Ismert hibák (codex 1. kör, 2026-08-08): frailest-metrika nyakvak, nesting nem kényszerített,
nincs akasztófurat, tárgyméret 291 mm a 300 helyett — javítva a 0005-ben.
