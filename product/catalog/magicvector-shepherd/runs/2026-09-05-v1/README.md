# Németjuhász · 2026-09-05-v1

Referencia: [MagicVectorLaser, 4328814517](https://www.etsy.com/au/listing/4328814517/german-shepherd-multilayer-svg-laser-cut). A hero-, szem- és ferde részletképet vizuálisan ellenőriztük; másolatuk a `product/references/magicvector-shepherd/` könyvtárban található.

A forrásképet a mentett `prompt.txt` alapján Imagegen készítette. A `source.png` a tényleges raszteres bemenet; nem egy késztermék-fotó került a kimenet helyére. A referencia irányított szőrvonalait, hosszú pofáját és eltérő festett rétegeit céloztuk.

A `profile.json` receptje 8 tónusklasztert kér, ebből a fekete háttér levonása után **7 fizikai réteg** marad. A referencia 8 réteges. Eltérő méretezés és a biztonságos minimális részletméret miatt nem erőltettünk be egy újabb, üres vagy gyenge réteget.

Mért eredmény: **0 nyak, 85 összes különálló rétegdarab, 1,75% legrosszabb vékonyterület**, sikeres export. Ez sok ragasztási munka; a következő érdemi fejlesztés a szem/orr külön színmaszkja és a szőrcsoportok összefüggőbb szerkesztése. A puszta további tónusszám-emelés ezt nem oldja meg.

```sh
.venv/bin/python product/pipeline/run_product.py \
  --profile product/catalog/magicvector-shepherd/runs/2026-09-05-v1/profile.json \
  --src product/catalog/magicvector-shepherd/runs/2026-09-05-v1/source.png \
  --out product/builds/shepherd-reference-v1
```

[Hero](output/plate.png) · [Közeli részlet](output/macro.png) · [SVG/DXF és ragasztási segédlet](output/layers/) · [Riport](output/layers/report.json)
