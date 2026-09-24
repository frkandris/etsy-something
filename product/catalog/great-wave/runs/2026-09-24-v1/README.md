# Nagy hullám (Hokusai) · 2026-09-24-v1

**Forrásmű:** Katsushika Hokusai, *A nagy hullám Kanagava partjainál* (kb. 1830–32), közkincs. A
referencia a Metropolitan Museum Open Access szkennelése (JP1847, az API szerint `isPublicDomain: true`):
`product/references/hokusai-great-wave-met-JP1847.jpg`.

**Piaci mérce, nem másolat:** [MarLaserCut listingje](https://www.etsy.com/listing/1708708292/),
9 réteg, 39,8 × 26 cm, naplementés paletta. A tervét nem használtuk; a mi rajzunk a Hokusai-kompozíciót
követi, a nyomat eredeti színeivel.

## Hogyan készült

1. `prompt.txt` → gpt-image-2, a Met-szkenneléssel mint referenciával, 3 változat (`candidates/`).
   Minden spot-szín egy lap, hátulról előre felsorolva.
2. `01b_depth.py --sheet-colours … --scene`: a színek **sorrendje** adja a lapot, nem a világosságuk
   (a halvány ég a leghátsó, a krém hab a legfelső). A `--scene` miatt az 1. lap a tömör, égszínű hátlap.
3. `02_trace.py` a `profile.json` szerint: 400 mm széles, 12 mm-es krém keret minden lapon, `--connected`.
4. Blender: `plate`, `macro`, `exploded`, `styled`.

A három jelöltből a 2. lett a forrás (`source.png`). A 0. jelöltet a kapu elutasította (1 nyak a
legfelső lapon). Az 1. is kiadható lett volna: 15 darab, de a legvékonyabb pontja 5,9 mm. A 2.
jelöltnél ugyanez 7,8 mm, a legrosszabb vékony terület 0,12% (az 1.-nél 0,21%).

## Mért eredmény

| | |
|---|---|
| panel | 400 × 266,8 mm (3:2) |
| lapok | 7: tömör hátlap + 6 kivágott lap, mindegyik keretes |
| darabok | 17, ebből 10 külön ragasztandó akcentus (a Fuji a 4–7. lapon, és a lebegő hab) |
| legvékonyabb pont | 7,8 mm (cél: 2 mm) |
| nyak | 0 |
| legrosszabb vékony terület | 0,12% |

Ez szoftveres geometriai ellenőrzés; **fizikai tesztvágás nem történt**. A versenytárs egyetlen
listing-szintű panasza (26 értékelésből egy) az volt, hogy a finom hab papírban és Cricuttal nem
vágódik ki tisztán. Itt minden anyagrész legalább 2 mm, a legvékonyabb pont 7,8 mm.

```sh
.venv/bin/python product/pipeline/01b_depth.py --art product/catalog/great-wave/runs/2026-09-24-v1/source.png \
  --out product/catalog/great-wave/runs/2026-09-24-v1/depth_map.png --scene --min-region-pct 0.01 \
  --sheet-colours "#EADCBF,#9A958C,#D8A56E,#A9CBDA,#2E6598,#172A4B,#F7F2E4"
.venv/bin/python product/pipeline/run_product.py --profile great-wave \
  --src product/catalog/great-wave/runs/2026-09-24-v1/depth_map.png --out product/builds/great-wave
```

[Plate](output/plate.png) · [Makró](output/macro.png) · [Szétszedve](output/exploded.png) ·
[Enteriőr](output/styled.png) · [SVG/DXF](output/layers/) · [Riport](output/layers/report.json) ·
[Szerelési útmutató](output/layers/assembly_guide.png)

## Listing-galéria (`output/gallery/`)

A versenytárs galériájának receptje alapján: 8 kép, 2700 × 2025 px (4:3).

| kép | mit mutat |
|---|---|
| `01_hero` | a mű szemből, világos vakolaton, vetett árnyékkal, felirat a `report.json` számaival |
| `02`–`05_detail` | közelik teljes felbontásban renderelve (hullámtaréj, Fuji és csónakok, bal alsó hab, jobb oldali hullám kerettel) |
| `06_layers` | a 7 lap egyenként a saját színében, számozva, mellettük a kész mű |
| `07_colours` | ugyanazok a fájlok 4 kartonszínben (a versenytársnál nincs ilyen) |
| `08_specs` | mit kap a vevő; minden szám a `report.json`-ból jön |

A vásárlói vélemények kollázsát (a versenytárs 9. képe) szándékosan kihagytuk: nekünk még nincs
értékelésünk, és a versenytárs is más termékek értékeléseit mutatja.

A renderer `product/render_flat.py`: ortografikus kamera szemből, ferde napfény, Cycles. A háttér a
Poly Haven `white_plaster_02` textúrája (CC0), a `gallery.json` szerinti világos szürkére térképezve.
A textúra letöltése (a `product/pipeline/assets/` gitignore-olt):

```sh
mkdir -p product/pipeline/assets/textures && curl -L -o product/pipeline/assets/textures/white_plaster_02_diff_4k.jpg \
  https://dl.polyhaven.org/file/ph-assets/Textures/jpg/4k/white_plaster_02/white_plaster_02_diff_4k.jpg
.venv/bin/python product/pipeline/gallery.py --run product/catalog/great-wave/runs/2026-09-24-v1   # ~4 perc
```
