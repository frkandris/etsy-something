# Listing #1 — Celtic Tree of Life Layered Shadow Box

**Státusz: kész a feltöltésre, DE fizikai tesztvágás nélkül.** Lásd a *Mielőtt kiteszed* részt.

![mockup](mockup_01.png)

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

listaár **$7.95**, tartós **40%** kedvezmény, tényleges **$4.77** (≈1 510 HUF).

A deduplikált keresési minta (342 termék) mediánja 1 520 HUF, a boltok 79,5%-a akciózik, medián
kedvezmény 40%. Ez a piaci norma — a korábbi „ne akciózz / magasabb ár" ajánlás az auditon
megbukott, ezért nem megyünk vele szembe az első listinggel.

## Leírás

> **Celtic Tree of Life — 6-layer shadow box, ready to cut, layers numbered.**
>
> A 300 mm (11.8") layered Tree of Life inside a Celtic star-knot ring. Four concentric mandala
> rings build the depth, a 16-point interlaced knot frames it, and the tree is a separate piece you
> glue centred on top.
>
> **What you get** • 6 numbered layers, SVG + DXF (R12) • stacked preview showing assembly order
> • designed for 3 mm (1/8") plywood or MDF, 18 mm total depth
>
> **Cut-safe by design** Every layer is verified to be a **single connected piece** — nothing falls
> out on the bed. Narrowest web **2.3 mm** on every layer, computed per layer, not estimated.
> Kerf compensation 0.2 mm applied.
>
> **Assembly** Cut layers 1–6, stack back to front, glue. The tree goes last, centred. The back
> plate has a 6 mm keyhole for hanging.
>
> **Machines** Glowforge · xTool · Ortur · CNC router · Cricut & Silhouette (3 mm card stock)
>
> Instant digital download — no physical item is shipped.

## Fájlcsomag

```
layer_1_of_6  hátlap, tömör korong + akasztófurat
layer_2_of_6  gyűrű, belső 40 mm, 24 szirom
layer_3_of_6  gyűrű, belső 64 mm, 32 szirom
layer_4_of_6  gyűrű, belső 88 mm, 40 szirom
layer_5_of_6  kelta csomó-gyűrű (16/5 csillagfonat) + külső perem, 8 küllővel bekötve
layer_6_of_6  életfa — külön darab, középre ragasztva
preview_stacked.svg + mockup_01.png
```

Mindegyik SVG **és** DXF R12 formátumban.

## Hogyan készült

`generate_celtic_tree.py` — tisztán számolt geometria, shapely boolean unióval. Minden réteget
**összefüggőség-ellenőrzés** után ír ki: ha egy réteg két darabra esne, a generátor jelzi és nem
megy tovább. Ez menet közben **kétszer is fogott hibát**: az 5. réteg csomó-szalagja szabadon
lebegett (küllőkkel megoldva), és korábban az előlap eltakarta az összes alatta lévő réteget.

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
