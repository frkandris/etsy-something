# assets — nyers anyag (csak olvasható)

**Ne szerkeszd.** Ezek a források, nem wiki-oldalak. Újra-előállításuk pénzbe (Apify) és élő
böngésző-munkamenetbe kerül.

## `data/`

| fájl | mi | mikor |
|---|---|---|
| `multilayer_svg.json`, `3d_layered_mandala_svg.json`, `3d_multilayer_svg_dxf.json`, `layered_svg_laser_cut_file.json`, `mls_search.json` | az 5 layered keresés nyers találata (100–100 listing) | 2026-08-07 |
| `niche_shops.json` | 173 bolt aggregálva a keresésekből (árak, találatszám) | 2026-08-07 |
| `niche_shopdetails.json`, `niche_shopdetails2.json` | Etsy bolt-adat a 173 boltra | 2026-08-07 |
| `niche_rows.json` | a 173 bolt összefűzve, származtatott mezőkkel | 2026-08-07 |
| `catalog_sample.json` | 1543 listing 65 bolt saját katalógusából | 2026-08-07 |
| `layered_adjusted.json` | **a fő adathalmaz** — 65 bolt layered aránnyal és korrigált bevétellel | 2026-08-07 |
| `functional-searches/` | az 5 funkcionális keresés nyers találata | 2026-08-07 |
| `fn_shops.json`, `fn_shopdetails.json`, `fn_catalog.json` | ugyanez a funkcionális szegmensre | 2026-08-07 |
| `salesdoe-2026.json` | 51 bolt SalesDoe adata a 2024-es kohorszból | 2026-08-06 |
| `rows-2026.json` | ebből generált sorok a `revenue estimation` fülhöz | 2026-08-06 |

## `scripts/`

Az elemző szkriptek, amik a `findings/` minden számát előállították. Futtathatók a `data/` mappából.

| szkript | mit számol |
|---|---|
| `niche.py` | nyers populáció eloszlásai |
| `adjust.py` | katalógus-arány és korrigált bevétel |
| `layered_deep.py` | az igazolt populáció összes bontása + cím-elemzés |
| `compare.py` | layered vs funkcionális összehasonlítás |
| `analysis.py`, `deep.py` | a 2024 vs 2026 kohorsz-elemzés |
| `gen_*.py` | az Apps Script generátorok |
