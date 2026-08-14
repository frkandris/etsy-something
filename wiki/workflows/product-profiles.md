---
type: Workflow
title: Termék-profilok és a közös vágás-geometria
description: Egy termék receptje egyetlen JSON-fájl, a mért geometriai tanulságok pedig egy közös modulban élnek. Azért lett így, mert a világtérkép beállításai bedrótozva csendben elvitték a papírvágás-láncot.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-14T22:00:00Z
---

# Termék-profilok és a közös vágás-geometria

## Miért

Három lánc van (papírvágás, terrain, világtérkép), és lesz több. A renderelő **közös**, ezért a
világtérképhez hangolt értékek — átlátszóság, keretvastagság, robbantási stílus, jelenet —
bedrótozva **más termékek kimenetét némán megváltoztatták**. A legsúlyosabb eset: a `plate` nézetet
átállítottam tömör stúdióháttérre, mert önálló termékképnek úgy szebb — de a papírvágás-lánc a
`04_composite.py`-vel fotó-háttérre teszi a rendert, és az **az alfa-csatornából** számol befoglaló
dobozt és kontakt-árnyékot. Tömör háttérrel az egész vásznat ragasztotta volna a fotóra.

**A tanulság általánosítva:** ha egy érték termékenként más, akkor nem konstans, hanem profil-adat.

## A profil

`product/profiles/<név>.json` — egy termék teljes receptje:

```json
{
  "name": "papercut",
  "pipeline": { "script": "02_trace.py", "args": ["--levels", "7", "..."] },
  "render":   { "palette": "well", "frame": true, "studio_bg": false,
                "frame_width": 0.085, "explode": "fan", "room": "shelf" },
  "views":    ["plate", "styled", "exploded"]
}
```

Használat: `blender -b -P product/render_blender.py -- <dir> <out.png> plate --profile papercut`

**A parancssori kapcsoló felülír**, tehát egy gyors próbához nem kell fájlt szerkeszteni. A
`--profile` a többi flag ELŐTT olvasódik ki — ez a lánc visszatérő #1 hibája volt (flag az
argv-szűrés után mindig `False`).

### Ami profil-adat lett

| kulcs | papírvágás | világtérkép | mit rontott el bedrótozva |
|---|---|---|---|
| `studio_bg` | `false` | `true` | a kompozit alfa-lánca (ez volt a legsúlyosabb) |
| `frame_width` | 0.085 | 0.052 | a 82 pontos keret elvékonyodott |
| `explode` | `fan` | `standing` | a jóváhagyott legyező-nézet eltűnt |
| `room` | `shelf` | `sideboard` | a polcos enteriőr komódra cserélődött |
| `canvas` | négyzetes | 2000×1360 | négyzetes mű fekvő vásznon |
| `mixed_wood` | `false` | `true` | korábban a paletta NEVÉHEZ volt kötve |

## A közös modul — `product/pipeline/cutlib.py`

Ide az kerül, amit egyik láncon **megmértünk**, és a másikon is érvényes:

- `necks` / `widen_necks` — nyak-detektor és **lokális** szélesítés (csak a nyak-zóna, nem az egész
  forma, így a kontúr karaktere marad)
- `heal_to_convergence` — a gyógyítás **ismételve**, amíg el nem fogy. A világtérképen mértük, hogy
  a klippelés maga gyárt új nyakat, a minta 1 → 1 → 0. **Egy kör után megállni csendes hiba:** a
  riport zöld, a lap mégis szétesik. A papírvágás-lánc `heal_all()`-ja addig egy kört futott.
- `ghost_outline` — ragasztási sablon: a darabok kontúrja 0,5 mm-rel beljebb a fogadó lapra
  gravírozva, így maga a lap mondja meg, hova kerül a darab
- `svg_text` / `text_paths` / `dxf_text` — felirat útvonalként. **Egy path, evenodd kitöltéssel:**
  betűnként külön path esetén az O, A, R belső lyuka tömör folt lesz, és a renderen a szöveg
  halandzsává mosódik. A DXF-nél az Y-tükrözés és az 50-es forgatás-kód kötelező.
- `snap` — `set_precision(make_valid(g), 0.01)` mindkét operandusra: ez a bevált javítás a GEOS
  „side location conflict"-ra hajszálvékony éleknél.

## Ami még nem közös

A papírvágás `heal_necks`-e és a `cutlib.widen_necks` két külön megközelítés; egyelőre mindkettő
él, mert nincs mérésünk arról, melyik őrzi jobban a kontúrt. A `02_trace.py` a saját
`heal_necks`-ét használja, de már **konvergenciáig iterálva**.

## Provenancia

`product/profiles/*.json`, `product/pipeline/cutlib.py`, `product/render_blender.py`.
Kapcsolódik: [[workflows/recessed-papercut-pipeline]], [[workflows/worldmap-pipeline]].
