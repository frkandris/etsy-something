# 0022 — macska 8. kör: a legjobb eddig

A teljes recept együtt, a scout és a kritikus visszajelzései után:
- **kompozíció**: 3/4 profil portré, felfelé néző, díszítés a szőrbe rajzolva (nem jelenet)
- **paletta** (catteal): fekete hátlap kontraszt-horgonynak → petrol → teal → fehér,
  12 L*-os value-lépcsőkkel
- **meleg akcentus**: zöld szem + rózsaszín orr — spline-onkénti material_index-szel
  (objektumonként nem ment: a trace rétegenként EGY path-ot ír, így az egész réteg egy
  többspline-os curve, és minden darab egyszerre kapott anyagot)
- **keret**: fehér, mély shadow-box, 9% szélesség; a kamera keretezése is ehhez igazítva
- **prompt**: kemény minimum-vastagság (a 0021 hajszálvonalai után)
- `--min-part 130` a 400 helyett, hogy a szem-darabok átmenjenek

Riport: 7 réteg, 0 nyak, legvékonyabb rétegdarab 3,74 mm.
Fájlok: `render_hero_v2.png` (akcentussal), `render_shelf.png`, `preview.gif` (24 kocka).
