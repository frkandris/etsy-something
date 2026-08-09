# 0023 — macska splatter, referencia-stílusú kimenet

A felhasználó referenciaképe (zsiráf, fehér mezőn lebegő foltszínes motívum, fehér mély keret,
meleg életkép-háttér bokehval) alapján épített változat.

Három új dolog a láncban:
- **`cat-splatter` téma**: lebegő fej, körülötte EGY üres mező (min. 40% a képből), splatter
  körvonalak csöpögéssel, szórt pöttyök — nem kitöltő ornamens
- **`splatter` paletta**: fehér mező + telített foltszínek (nem sötét→világos rámpa)
- **`lifestyle` nézet**: fa asztallap, meleg fal, elmosott kellékek, valódi **mélységélesség**
  (f/2.2), szemből, a keretre fókuszálva

Menet közben három hiba javítva:
1. a paletta-interpoláció **pasztellé mosta** a foltszíneket → ha van elég szín, most közvetlenül
   veszi őket, nem kever
2. a keret a forgatás **után** épült, ezért laposan maradt az asztalon → most előbb épül és
   együtt fordul a képpel
3. a 90°-os forgatás képlete rossz volt: a helyes leképzés (x,y,z) → (x, −z, y), én a z-t
   konstansra állítottam — a lapos műnél (y≈0) ez véletlenül működött, a keretnél a vízszintes
   léceket a középvonalra roskasztotta

Riport: 8 réteg, 0 nyak, minden réteg OK.
