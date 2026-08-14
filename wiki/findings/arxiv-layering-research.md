---
type: Finding
title: arXiv-sweep a réteges relief-generáláshoz — mi van megoldva és mi nincs
description: A rétegbontásra gazdag és közvetlenül alkalmazható irodalom van (VLM-vezérelt szemantikus peeling), a lézervágás fizikájára és a galéria-konverzióra viszont semmi. Az amodális kiegészítés követelményét a láncunk már teljesíti — megmérve.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-14T23:30:00Z
---

# arXiv-sweep a réteges relief-generáláshoz

Öt kérdésre kerestünk mérhető eredményt a kiemelkedő reliefes portré-lánchoz
([[workflows/product-profiles]], `profiles/relief-portrait.json`). Az eredmény
**erősen aszimmetrikus**, és ezt érdemes előre kimondani: két kérdésre az arXiv
egyszerűen nem a megfelelő forrás.

## Ami megvan és beépíthető

**A rétegbontás már nem tónus-kvantálás.** Ez a fő nyitott kérdésünkre a válasz:
a jelenlegi irodalom **VLM-vezérelt szemantikus rétegbontást** használ, ami
pontosan anatómiai/szemantikus régiókra bont, nem tónus-küszöbre.

- **2604.10940** (AmodalSVG) — Semantic Layer Peeling, **amodális kiegészítéssel**
  (az alsó réteg teljes alakzat, nem a felső által kivágott csonk) és
  rétegenként eltérő primitív-budgettel.
- **2505.23740** (LayerPeeler) — a rétegsorrend **okklúziós gráfból** származik,
  nem tónusból; diffúziós modell állítja vissza az eltakart tartalmat.
- **2406.05404** — progresszív szemantikus egyszerűsítés: a lépéssorozat **maga
  a rétegstack**, felülről lefelé.
- **2206.04655** (LIVE) — önmetszés-mentes rétegek. Vágható geometriánál ez nem
  esztétika: a lézer nem tud önmagát metsző útvonalat értelmesen vágni.

**Az egyszerűsítés két külön tengely.** A **2211.17256** (CLIPascene) szétválasztja
a *hűséget* (mennyire pontos a kontúr) és az *egyszerűséget* (hány elem marad).
Nálunk egyetlen globális `--simplify` van, ami rossz kompromisszum: a **külső
sziluett** — ami itt maga a vágásél — magas hűséget kíván, a **belső
rétegvonalak** viszont mehetnek durvábbra. A **2202.05822** (CLIPasso) az
absztrakciót primitívszám-budgettel vezérli, a **2603.28363** pedig
referencia nélküli, elem-szintű ellenőrzést ad (23 100 emberi rajz, 300 osztály):
definiálható egy elemlista — hegyes álló fül, hosszú pofa, szemvonal —, és
VQA-val ellenőrizhető, hogy a bontás után is megvan-e mind.

**A mélységet a vetett árnyék adja, nem az önárnyékolás.** A **2405.14530**
megerősíti, hogy a puszta shading **matematikailag többértelmű** (bas-relief
ambiguity: ugyanaz a kép lehet lapos vagy mély). A **2201.01889** mérése szerint
a **nem-fotorealisztikus, kemény élű vetett árnyék jobban működik**, mint a
fotorealisztikus lágy árnyék, és a hatás ott a legerősebb, ahol a jelenet
amúgy is lapos. A **2008.05505** szerint a luminancia önálló mélységjel.
Következmény a renderre: a rétegek közti árnyék legyen tiszta és kemény élű, a
rétegek luminanciája pedig lépcsőzött — a frontális, árnyék nélküli
terméklátvány garantáltan laposnak fog látszani.

## Amit már teljesítünk — megmérve

Az AmodalSVG kritikus pontja, hogy **az alsó rétegeknek a felsők alatt is
folytatódniuk kell**, különben ragasztáskor rés keletkezik. A német juhász
készletén (`0052-german-shepherd`, 7 réteg) ezt lemértük:

| réteg | terület | a mögötte lévőn kívül |
|---|---:|---:|
| 1 | 46 065 mm² | — (a teljes sziluett) |
| 2 | 45 876 mm² | 0,0 mm² (0,00%) |
| 3 | 34 247 mm² | 0,0 mm² (0,00%) |
| 4 | 24 999 mm² | 0,0 mm² (0,00%) |
| 5 | 16 053 mm² | 0,0 mm² (0,00%) |
| 6 | 7 547 mm² | 0,0 mm² (0,00%) |
| 7 | 1 775 mm² | 0,0 mm² (0,00%) |

**A követelmény konstrukció szerint teljesül**, mert a `mask_at` egymásba
ágyazott küszöbökből dolgozik (`tone >= thr`, növekvő `thr`), és az
`enforce_nesting()` ezt még klippeli is. Nem kell utólagos amodális kiegészítés.

*Mérési megjegyzés:* az első mérésem minden rétegre 0 mm²-t adott — a parserem
vesszőre bontott, a fájlok viszont szóközzel írják a koordinátákat. Egy 0 mm²-es
réteg nyilvánvalóan lehetetlen, ezért került újramérésre; a fenti tábla a
javított parserrel készült.

## Amire az arXiv NEM ad választ

**Lézervágás fizikája rétegelt lemezen.** Nincs kerf-szélesség, égett él vagy
minimális elemvastagság mérés 3 mm-es nyírfa rétegelt lemezre. (A „kerf" keresés
Kernel Random Forest cikkeket ad; a lézervágás-találatok fémre és SiC-ra
vonatkoznak.) Ez a tudás gyártói adatlapokon és fatechnológiai folyóiratokban
él. Egyetlen használható tétel a **2209.00116** (LaserSVG): szabvány-kompatibilis
SVG-kiterjesztés, ami **az anyagvastagságot paraméterként hordozza a fájlban**,
így ugyanaz a sablon más vastagságra igazodik. Ez közvetlenül eladható előny is,
és illeszkedik a profil-alapú paraméterezésünkhöz.

**Termékfotó és konverzió.** Nincs kutatás arról, hogy makrofotó vs. enteriőr-kép
hogyan hat a konverzióra, és nincs optimális képszám sem — ez marketing/IS
irodalom. A **2408.11349** (Mercari) annyit ad, hogy egy 20M+ felhasználós
piactéren az LLM-generált esztétikai címkék korrelálnak a valós viselkedéssel, és
az élesített modell online kísérletben szignifikáns eladásnövekedést hozott
(százalék nincs közölve). A **2602.15278** viszont figyelmeztet: a VLM-alapú
képpontozás **szisztematikus torzításokkal** jön — ezt tudni kell, mielőtt a
`render-critic` pontszámára hagyatkozunk.

**Hány réteg éri meg.** A „mennyi lépcső kell a mély benyomáshoz" és a
telítődési pont kérdésére **nincs arXiv-válasz** — ez Journal of Vision /
Perception körébe tartozik. Ha döntéskritikus, magunknak kell megmérnünk.

## Populáció-megjegyzés

**Ebben a sweepben nincs saját mérési szám**, egyetlen kivétellel: a fenti
amodális tábla a mi 7 rétegű német juhász készletünkön mért érték. Minden más
tétel külső eredmény vagy módszertani állítás, nem a mi populációnkon mért adat.

## Provenancia

arXiv API sweep, ~20 lekérdezés, 5 témakör. Kapcsolódik:
[[workflows/product-profiles]], [[workflows/recessed-papercut-pipeline]],
[[decisions/2026-08-10-keprogeneralas-iranya]].
