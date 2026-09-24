# Süllyesztett macskaportré · 2026-09-05-v2

A v1 depth_map.png és palette_full.json változatlan másolatából készült, új képgenerálás nélkül. A rétegek margóhoz igazítása most a legalsó kivágott panel nyílásait is ugyanazzal a transzformációval mozgatja. A korábbi körülbelül 21 mm-es relatív eltolás megszűnt. A keretszél javítása nem zárja össze a szem és a szalagok belső nyílásait.

A tényleges SVG-kből újrarenderelt [plate](output/plate.png) és [styled](output/styled.png) képet vizuálisan ellenőriztük: a mandulaszem, pupilla, fül és hosszú sötét nyakszalag felismerhetően követi a depth mapet. [Korábbi hibás render](../2026-09-05-v1/output/plate.png).

A hat kivágott panel mindegyike egy darab; hozzájuk egy tömör hátlap tartozik. A geometriai riport: 0 nyak, legrosszabb vékonyterület 0,02%, all_ok és release_ready igaz. Ez szoftveres geometriai ellenőrzés; fizikai tesztvágás nem történt. A referencia színei és stilizálása továbbra sem azonosak a kimenettel.

```sh
.venv/bin/python product/pipeline/run_product.py \
  --profile recessed-papercut \
  --src product/catalog/recessed-papercut/runs/2026-09-05-v2/depth_map.png \
  --out product/builds/cat-reference-v2
```

[Recept](profile.json) · [Riport](output/layers/report.json) · [Manifest és bemeneti hash-ek](output/manifest.json)
