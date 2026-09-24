# Süllyesztett macskaportré · 2026-09-05-v1

Referencia: a korábban elmentett `product/pipeline/references/ref-abstract-cat.png`. A pontos eredeti Etsy-URL nem szerepel az azonosított forrásokban; nem kapcsoltunk hozzá találomra másik terméket.

Új, egyszerűbb forrásrajz készült (`source.png`, `prompt.txt`), majd `01b_depth.py` bontotta 7 tónusra. A `depth_map.png` a trace bemenete, a `palette_full.json` az eredeti színsor. Ebből **6 kivágott panel + 1 tömör hátlap** készült. A hátlap SVG/DXF fájlja és sötét színe most külön megmarad, nem vész el a tónusok átszámozásakor.

Mért eredmény: **0 nyak, 11 rétegdarab + hátlap, 0,03% legrosszabb vékonyterület**, sikeres export. A keret körül több levegő marad, a korábbi nagy, töredezett foltok helyett szélesebb szalagok jelennek meg. A szem környéke még túl apró és tagolt, a referencia szalagjai folytonosabbak. A styled kép környezete is zsúfoltabb a kívánatosnál; elsődleges összehasonlításra a plate szolgál.

```sh
.venv/bin/python product/pipeline/01b_depth.py \
  --art product/catalog/recessed-papercut/runs/2026-09-05-v1/source.png \
  --out product/catalog/recessed-papercut/runs/2026-09-05-v1/depth_map.png --levels 7
.venv/bin/python product/pipeline/run_product.py \
  --profile product/catalog/recessed-papercut/runs/2026-09-05-v1/profile.json \
  --src product/catalog/recessed-papercut/runs/2026-09-05-v1/depth_map.png \
  --out product/builds/cat-reference-v1 --views plate,styled
```

[Hero](output/plate.png) · [Környezeti kép](output/styled.png) · [SVG/DXF és hátlap](output/layers/) · [Riport](output/layers/report.json)

2026-09-05 korrekció: a fenti v1 render illesztési és túlzott simítási hibás. A geometriai zöld státusz önmagában nem igazolta a forráshűséget. Javítás és változatlan depth mapből készült új render: [v2](../2026-09-05-v2/README.md).
