# 0005 — javított kelta életfa (codex 1. kör után)

Ugyanaz a 0003-as forráskép, a codex-audit 14 findingja utáni lánccal:
- nesting explicit kikényszerítve (minden réteg a mögötte lévőhöz vágva) — a MIN_PART-demóció
  („a kis darab egy lappal hátrébb marad") most már garantált, nem csak közelítő
- nyak-detektor + lokális gyógyítás: a klippelés által létrehozott 2 mm alatti hidak kiszélesítve
  (a lánc gyógyítással zárul, mert a klippelés maga is nyakat gyárt)
- tárgyméret = 300 mm a hátlap befoglalójára (nem a vászonra) — a 0003 valójában 291 mm volt
- kulcslyuk-akasztó (7 mm + 3,5 mm slot) szkenneléssel elhelyezve a hátlap tömör sávjában
- DXF: $ACADVER + $INSUNITS(mm) + CUT layer deklaráció + dupla záró vertex eltávolítva
- hosszú keskeny rések megmaradnak (extent-alapú lyukszűrés terület helyett)
- kézi depth_map (0..N indexkép) útvonal megjavítva; üres/összeeső tónus → explicit hiba
- assembly_guide.png: rétegenként egy panel, az új réteg narancssal kiemelve

Riport: 1/1/1/1/1/6 darab, 0 nyak, leggyengébb 6,46 mm, vékony terület ≤0,89%.
