---
type: Pitfall
title: Ha a hiba MINDEN rétegen végigvonul, a forrást nézd — négyszer ugyanaz
description: Négy különböző tünetet kezeltem a láncban, pedig mind a négy a forrásképből jött. A megkülönböztető jel egyszerű: ha a hiba rétegfüggetlenül ismétlődik, akkor nem a geometria rontja el, hanem már így kapja.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-14T23:59:00Z
---

# Ha a hiba minden rétegen végigvonul, a forrást nézd

## Tünet

Egyetlen napon négy különböző hibát kezdtem a **láncban** javítani, és mind a
négyszer a **forrásképben** volt a megoldás:

1. **Krém háttérlap a kutya mögött.** Az első magyarázatom — „a fehér háttér
   külön rétegként bekerül" — hibás volt, és a ráírt `--drop-field` kapcsoló
   ezért alig 2 500 mm²-t vitt el. A `mask_at` docstringje mondta meg a valódi
   okot: a maszk **tónus fölött** válogat anyagot (`0 if v >= thr else 255`),
   tehát a 255-ös fehér háttér **mind a nyolc szinten** anyag. Nem egy réteget
   adott hozzá, hanem mindet kitöltötte a vászon széléig.
2. **Lebegő krém-sziget a pofán**, **elszakadt töredék a robbantott nézeten**,
   és **örvény alakú legyező** — a bíráló mind a hármat egy gyökérokra vezette
   vissza: a rajz sugárirányú szőrszálakat különített el saját tónussá, amikből
   vékony sarló-sávok lettek. Küszöb-emeléssel (20 → 16 sziget) csak tünetet
   kezeltem; a prompt megerősítése után **20 → 7**.

## Gyökérok

A vágás-lánc **hűségesen** viszi tovább, amit kap. Ha a forrásban vékony
sáv van, a láncban is vékony sáv lesz — a nyakgyógyítás, a sziget-küszöb és a
simplify mind *utólagos kármentés*, nem javítás.

## A megkülönböztető jel

**Ha a hiba rétegfüggetlenül, minden lapon ugyanúgy jelentkezik, akkor a forrás
adja.** Ha egyetlen rétegen van, akkor a lánc rontotta el.

A krém háttérlap mind a nyolc rétegen ott volt. A vékony sarló-sávok minden
tónuson. Ezzel szemben a nyak Panamánál *egy* darabon volt — az valóban
geometriai kérdés, és a `heal_to_convergence` meg is oldotta.

## Alkalmazott korrekció

A `--relief` prompt mostantól kimondja a vágási megkötéseket **a képre**:
minden tónus legfeljebb 2-3 összefüggő, hüvelykujjnyi széles tömör folt; tilos
a vékony sarló/gyűrű/ív alakú sáv; a fogazottság a **kontúron** él, nem önálló
szilánkként. Eredmény: 0 nyak mind a rétegen, 12 mm-es legvékonyabb pont a
2 mm-es határ mellett, és 7 akcentus-sziget 20 helyett.

## Tanulság

Ez a projekt ezt **már tudta**: a süllyesztett papírvágás-lánc wiki-oldala
rögzíti, hogy a szerkezeti tévedés javítása „nem a renderben volt… a helyes hely
a **generátor**". Ugyanez a mondat érvényes a geometriára is.

Ellenőrizhető jövőbeli munkán: **mielőtt küszöböt hangolsz vagy javító lépést
adsz a lánchoz, nézd meg, hány rétegen jelentkezik a hiba.** Ha mindegyiken,
a forráson múlik, és a lánc-oldali javítás csak elfedi.

## Provenancia

`product/pipeline/00_generate.py` (`--relief`), `02_trace.py` (`mask_at`,
`--drop-field`), `product/iterations/0052-german-shepherd`. Kapcsolódik:
[[workflows/recessed-papercut-pipeline]], [[findings/arxiv-layering-research]].
