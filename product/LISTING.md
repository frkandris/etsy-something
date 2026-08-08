# Listing #1 — Celtic Tree of Life Layered Shadow Box

**Státusz: kész a feltöltésre, DE fizikai tesztvágás nélkül.** Lásd a *Mielőtt kiteszed* részt.

**v2 — képmodell-pipeline.** Az 5 versenytárs-listing átnézése után a procedurális geometriát
lecseréltük AI-illusztrációból vezetett rétegekre (`pipeline/00_generate.py` →
`pipeline/02_trace.py` → `render_blender.py`). A régi generátor és mockup megmaradt referenciának.

![hero](iterations/0005-fixed-celtic-tree/render_hero.png)

---

## Miért ez a motívum

| jel | adat |
|---|---|
| **Tree of Life eladás** | 16 review / 12 termék / **8 független eladó** (21 igazolt bolt); 25 / 18 / **12** a teljes 33-as mintán |
| kelta önmagában | 6 review / **3 eladó** — a több-eladós küszöb alatt, ezért nem önállóan |
| **kereslet** | `tree of life svg` 533 keresés / 20 500 találat = **26,0 per 1000** (4x az alapérték) |
| | `yggdrasil` 645 / 7 100 = **90,8** — a legkevésbé telített kifejezés az adatbázisban |
| | `celtic knot svg` 156 / 9 200 = 17,0 |
| **termékforma** | `shadow box svg` **75,6 per 1000** (a legjobb fájlszándékú kifejezés) + 328 review / **12 eladó** |

A kelta fonás a **vizuális nyelvet** adja (és természeténél fogva rétegzett), az életfa az
**eladási bizonyítékot**. A codex független elemzése is az életfát hozta harmadik tesztként.

## Cím (106 karakter, limit 140)

```
Celtic Tree of Life SVG, Layered Shadow Box, 6 Layer Mandala Wall Art, Laser Cut DXF for Glowforge & Cricut
```

Elöl a legnagyobb keresésű saját kifejezés, mögötte a legjobb arányú termékforma, végül a gépek
(a mezőny címeinek 85%-a említ lézert, 28% Cricutot, 23% Glowforge-ot).

## Tagek (13 db, mind ≤20 karakter)

```
tree of life svg · celtic knot svg · shadow box svg · layered svg · multilayer svg
laser cut file · glowforge files · cricut cut file · celtic wall art · 3d wall art
yggdrasil svg · dxf laser file · tree wall decor
```

## Ár

listaár **$11.95**, tartós **40%** kedvezmény, tényleges **$7.17** (≈2 270 HUF).

A deduplikált keresési minta (342 termék) mediánja 1 520 HUF, de az 5 legközelebbi versenytárs
átnézése azt mutatta, hogy az egyedi (nem bundle) intricate designok 2 200–2 500 HUF körül mennek —
a v2 design már ebbe a sávba tartozik. A 40% tartós kedvezmény a piaci norma (a boltok 79,5%-a
akciózik, medián 40%), azzal nem megyünk szembe.

## Leírás

> **Celtic Tree of Life — 6-layer shadow box, ready to cut, layers numbered.**
>
> A 300 mm (11.8") layered Tree of Life inside a woven Celtic knot ring. Interlaced knotwork
> branches, a mirrored root weave and a braided border build six true depth levels — the over-under
> of the knots is a real physical step, not an engraving.
>
> **What you get** • 6 numbered layers, SVG + DXF (R12) • stacked preview showing assembly order
> • designed for 3 mm (1/8") plywood, MDF or card stock — 6 layers, ~18–19 mm assembled
>
> **Cut-safe by design** Layers 1–5 are each a **single connected piece** — nothing falls out on
> the bed; the front accent layer is 6 large pieces, all over 400 mm². Every layer passes an
> automated fragility check: weakest piece ≥ 6 mm at its widest, thin (breakage-prone) area at most
> 0.9% of any layer, and **zero thin necks** — narrow bridges between solid regions are detected
> and locally widened before export. Widths are measured on the cut centreline, before kerf.
>
> **Assembly** Cut layers 1–6, stack back to front, glue. Layers 1–5 are one piece each; layer 6
> is six accent pieces — the included **assembly guide** shows each layer highlighted in place, so
> every piece has an unambiguous home. The back plate has a keyhole hanger (7 mm entry, 3.5 mm
> slot) cut near the top. Total depth 17.8–19.1 mm depending on material (3 mm vs 1/8").
>
> **Machines** Glowforge · xTool · Ortur · CNC router · Cricut & Silhouette (3 mm card stock)
>
> Instant digital download — no physical item is shipped.

## Fájlcsomag (iterations/0005-fixed-celtic-tree/layers/)

```
layer_1_of_6  hátlap, tömör sziluett — 1 darab
layer_2_of_6  fonott szegély + belső mező, 223 kivágással — 1 darab
layer_3_of_6  szegély-fonat mélyebb szálai + lombkorona — 1 darab
layer_4_of_6  fa + gyökérfonat teste — 1 darab
layer_5_of_6  fonatok felül futó szálai — 1 darab
layer_6_of_6  törzs, ágak és a szegély kiemelt szálai — 6 darab
preview_stacked.png/svg + assembly_guide.png + render_hero.png
```

Mindegyik SVG **és** DXF R12 formátumban. Összesen **11 darab** ragasztandó elem — az 1–5. réteg
egy-egy összefüggő lap.

## Hogyan készült (v2 pipeline)

`pipeline/00_generate.py` — gpt-image-2 rajzolja a motívumot **mélységtérképként**: pontosan 6
lapos szürkeárnyalat, egymásba ágyazott szintek, textúra és árnyék nélkül. A prompt a
poszterizálhatóságot kényszeríti ki, nem a szépséget.

`pipeline/02_trace.py` — hisztogram k-means poszterizálás → rétegenként potrace vektorizálás →
shapely javítás (hajszálvékony részek vastagítása, tűlyukak és szilánkok eldobása) →
**vágásbiztonsági riport** rétegenként: darabszám, legvékonyabb anyag, törésveszélyes terület.
Kulcstrükk: mivel a szintek egymásba ágyazottak, egy 400 mm²-nél kisebb darab eldobása nem lyuk —
az a folt egy mögöttes lapon marad látható — sosem lesz átmenő lyuk, mert a nestinget a lánc
explicit kikényszeríti (minden réteg a mögötte lévőhöz van vágva). A demóció-audit minden futásnál
kiírja, mekkora terület esik egynél több lappal hátrébb (a kelta fánál ez 518 mm², a felület
0,2%-a). MIN_PART=0-val 168 különálló darab lenne, a szállított fájlokban 11. A vékony nyakakat (két tömör régiót összekötő, 2 mm-nél
keskenyebb híd) a lánc detektálja és lokálisan kiszélesíti; a kulcslyuk-akasztót a hátlap tömör
sávjába szkenneléssel helyezi el.

`render_blender.py` — headless Cycles render, a rétegek valódi 3 mm vastagsággal, hogy a
lépcsős árnyékok látszódjanak. A [[findings/keyword-demand-sweep]] szerint **a thumbnail nyeri meg
a hosszú farkot, nem a kulcsszó** — ezért ez a lépés nem kényelmi kérdés.

## Mielőtt kiteszed — ami hiányzik

1. **Fizikai tesztvágás.** A geometria konstrukció szerint biztonságos, de **nem vágtuk ki**. A
   független elemzés szerint a legrosszabb vevői visszajelzések pontosan ebből jönnek: hiányzó
   rétegek, törő elemek, nem vágható geometria. Sanyi papánál egy lap 3 mm rétegelt lemez eldönti.
2. **Anyagszerű render.** A mockup egyszínű fa; valódi rétegelt lemez textúra és egy fal-környezet
   sokat javítana rajta.
3. **Esztétikai finomítás.** A mandala szirmok geometrikusak, a fa ágai szimmetrikusak. Működik,
   de nem kézműves hatású. A generátor paraméterezhető.

## Amit bizonyít, és amit nem

**Bizonyítja:** a pipeline működik végponttól végpontig — motívumválasztás mért adatból, geometria
generálás, vágásbiztonsági ellenőrzés, 3D termékfotó. Egy új design perceken belül újragenerálható.

**Nem bizonyítja:** hogy el fog kelni. Az egész kutatás nem tudta megmondani az új listingek
tényleges eladását — ez a hiányzó döntő mérés, és ez a listing az első adatpont hozzá.
