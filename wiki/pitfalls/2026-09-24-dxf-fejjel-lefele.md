---
type: Pitfall
title: Minden DXF fejjel lefelé — két lánc, két ellentétes hiba
description: A trace- és mindkét térkép-lánc DXF-je az SVG függőleges tükörképe volt; a tesztek szimmetrikus ábrán és a hibás értéket rögzítő állítással zöldek maradtak.
status: stable
generated:
  by: claude-opus-5-5
  at: 2026-09-24
sources:
  - resource: ../../product/pipeline/02_trace.py
  - resource: ../../product/pipeline/10_worldmap.py
  - resource: ../../product/pipeline/11_worldmap_flat.py
  - resource: ../../tests/test_trace_export.py
  - resource: ../../tests/test_map_orientation.py
  - resource: ../../tests/test_flat_map_export.py
---

# Tünet

Nem volt látható tünet: minden DXF-et csak szerkezetileg (fejléc, `EOF`, fájlszám) ellenőriztünk,
a Blender-render és a galéria pedig az SVG-ből készül. A vevő, aki a DXF-et tölti be a vágóba, egy
függőlegesen tükrözött terméket vágott volna. Az aszimmetrikus motívumoknál (portré, térkép) ez
fejjel lefelé álló, tükrözött kép. A 2026-09-24-i kódátnézés vette észre, kódolvasással.

# Gyökérok

Az SVG-ben az Y lefelé nő, a DXF-ben felfelé. A két lánc ellentétes irányból rontotta el:

- **`02_trace.py`** — a geometria már SVG-konvencióban (Y lefelé) van; az SVG így helyes. A DXF
  ugyanezeket a számokat írta, **tükrözés nélkül**. Helyes: `MM - y`.
- **`10_worldmap.py`, `11_worldmap_flat.py`** — a modell a Miller-vetület miatt északra növő Y-t
  használ; az SVG-be ezért helyes a `H - y`. A DXF-be **is** `H - y` került, holott ott a nyers `y`
  a helyes. A 10-es lánc feliratai nyers `y`-t kaptak, tehát egy DXF-en belül a feliratok és a
  darabok egymáshoz képest is elcsúsztak.

# Hogyan maradt rejtve

1. A trace-exportteszt **szimmetrikus, középre igazított** téglalapokat használt: a függőleges
   tükörkép bitre ugyanaz a befoglaló doboz.
2. A `cutlib.dxf_text` tesztje (`test_dxf_text_flips_y`) **a hibás értéket rögzítette**, és a
   mutációs keret ezt a tesztet „igazolta”: a mutáció csak azt méri, hogy a teszt észleli-e a
   *változást*, azt nem, hogy a várt érték helyes-e. A függvényt élesben senki nem hívta.
3. Minden réteg ugyanúgy tükröződött, ezért a rétegek egymáshoz illesztése ép maradt.

# Alkalmazott korrekció

- A trace DXF `MM - y`, a két térkép DXF nyers `y`. A 10-es „WORLD MAP” cím SVG-ben és DXF-ben
  most ugyanazt a modellkoordinátát kapja (korábban az SVG-ben alul, a DXF-ben felül volt).
- A nem használt és hibás konvenciót rögzítő `cutlib.dxf_text`, a tesztje és a hozzá tartozó
  mutáció törölve. Mutációk: 13 → 12.
- Három új teszt aszimmetrikus ábrával; mindhárom elbukik a régi konvención. Ezek:
  `test_dxf_is_not_upside_down_relative_to_svg`,
  `test_worldmap_dxf_keeps_north_up_and_svg_puts_north_on_top`,
  `test_flat_map_dxf_is_north_up_like_its_svg`.
- A mentett receptek újrafuttatva (`--no-render`) a két trace-katalógusra, a két általános
  trace-profilra és a `marlaser-worldmap`-re, összesen 94 kimeneti fájl: **csak a 29 DXF változott**,
  mindegyik pontosan `y → H − y` szerint. Egyetlen SVG, paletta vagy riport sem változott.

**Nem javított:** a repóban tárolt korábbi DXF-ek (`product/catalog/*/runs/*/output/`,
`product/iterations/`) továbbra is tükrözöttek. **Döntés (2026-09-24, felhasználó):** legacy
rekordként maradnak, nem generáljuk újra őket. Kiadásra csak a javított kóddal készült új futás DXF-je
használható.

# Tanulság

- **Formátumkonverzió tesztje aszimmetrikus ábrával készüljön.** Egy szimmetrikus fixture a tükrözést,
  a forgatást és a 180°-os elfordítást sem látja.
- **Két kimeneti formátumot egymáshoz mérj**, ne külön-külön. A „van fejléc és EOF” nem állítás a
  geometriáról.
- **A mutációs teszt a teszt érzékenységét igazolja, nem a helyességét.** Ha a várt értéket a kódból
  másoltuk ki, a hibát rögzíti. Lásd [[workflows/self-testing-code]].
