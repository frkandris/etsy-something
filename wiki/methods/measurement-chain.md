---
type: Method
title: A mérési lánc — keresés → találat → bolt → termék → eladás
description: Öt réteg, öt különböző mértékegység; a projekt minden hibája abból jött, hogy két réteget összekevertünk.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-08T18:00:00Z
---

# A mérési lánc

Ez a projekt **öt különböző dolgot** mér, öt különböző forrásból. Mindegyik mást tud megmondani, és
mindegyiknek **más a mértékegysége**. A wiki összes visszavont következtetése abból származott, hogy
két réteg számait összekevertük.

Ez az oldal a térkép: mit mér az adott réteg, mi az egysége, mit **nem** tud, és hol futottunk bele.

```
KERESLET                                                              ELADÁS
   │                                                                     │
   ▼                                                                     ▼
1. KERESÉS ──► 2. TALÁLAT ──► 3. BOLT ──► 4. TERMÉK ──► 5. REVIEW
   hányan          hányan       ki árulja    mit árul       mit vettek
   keresik         árulják      valójában    valójában      meg tényleg
```

---

## 1. Keresés — a kereslet

**Mit mér:** hányan gépelték be az adott kifejezést az Etsy keresőjébe az elmúlt 30 napban.
**Forrás:** Etsy Marketplace Insights (a saját bolt seller felülete, Etsy Plus).
**Egység:** **keresőkifejezés**. 345 kifejezés mérve 2026-08-07/08-án.

**Amit tud:** valós, első kézből jövő keresletet. Nem becslés — ezért veri az eRank/Alura/RankHero
modellezett számait ([[methods/keyword-tools-comparison]]).

**Amit nem tud:**
- **kinek mi a szándéka.** A `shadow box` 11 100 keresésének nagy része **kész fizikai terméket**
  keres, nem vágósablont. A `layered svg` 1 200-a fájlt. A kettő nem összemérhető.
- **ki vásárol.** A `multilayer svg` keresőinek 9,7%-a ukrán — jórészt konkurencia, nem vevő.
- **szezonalitást.** Csak 30 nap érhető el, és minden mérésünk augusztusi.

**Ahol elbuktunk:** a `viking helmet svg` 109,4-es kereslet/kínálat aránya alapján egy 18 designos
katalógustervet írtam. A review-réteg később megmutatta, hogy azok a keresők **gravírozó fájlt**
akarnak. Egy arányszám nem mondja meg a szándékot. → [[findings/review-mining]]

---

## 2. Találat — a kínálat

**Mit mér:** hány listing verseng ugyanarra a kifejezésre. Ugyanabból a forrásból jön, mint a keresés.
**Egység:** **listing**.

Ebből képezzük a projekt fő telítettségi mutatóját:

> **keresés / 1000 találat** — hány havi keresés jut ezer versenyző listingre.
> Viszonyítási alap: `layered svg` = **6,3**. A 345 kulcsszó mediánja **4,1**.

**Amit nem tud:** a „találat" minden illeszkedő listinget számol, tág kifejezéseknél tehát felfelé
torzít. És a jó arány **kínálati hiányt** jelez, nem keresletet: lehet, hogy azért kevés a listing,
mert nem éri meg.

---

## 3. Bolt — ki árulja

**Mit mér:** ki van a találatok mögött, mekkora, mióta működik, mennyit adott el összesen.
**Forrás:** Etsy bolt-adat (Apify), a keresésekből kinyert boltnevekre.
**Egység:** **bolt**.

**Itt van a projekt összes populációs csapdája.** Három egymásba ágyazott halmaz:

| populáció | definíció | boltok |
|---|---|---:|
| **nyers** | megjelent az 5 keresés találatai közt | **173** |
| **specialista** | legalább 3 **különálló** listinggel rangsorolt | **35** |
| **igazolt** | ráadásul a saját katalógusa ≥80%-ban layered | **21** |

**Kötelező szabály:** minden szám mellé oda kell írni, melyik populáción számoltuk. Egy szám a
populációja nélkül ebben a projektben nem pontatlan, hanem **hamis**.

**Amit nem tud:**
- **halandóságot.** A populáció *mai* keresési találatokból épült, tehát a megszűnt boltok
  szerkezetileg láthatatlanok: 0/173 bezárt bolt. Az egyetlen valós halandósági adatunk a 2024-es
  követő kohorszból jön: **13/57 megszűnt két év alatt**.
- **belépési valószínűséget.** Amit „belépési esélynek" neveztünk, az valójában
  **rangsorolás-túlélési arány**: csak azokat a fiatal boltokat látjuk, amelyek ma is rangsorolnak.

**Ahol elbuktunk:** a specialista-szűrő a keresési találatok **sorait** számolta, nem a különálló
listingeket — az öt keresés átfed, tehát ugyanaz a listing háromszor is beszámított. 65 helyett 35,
33 helyett 21. → [[pitfalls/2026-08-08-wrong-unit-of-independence]]

---

## 4. Termék — mit árul valójában

**Mit mér:** a bolt **saját katalógusából** vett minta (boltonként max. 24 listingcím), szemben azzal,
ami véletlenül rangsorolt.
**Egység:** **listing (cím)**. 1 543 listing 65 boltról; ebből 504 a 21 igazolt bolttól.

**Miért kell külön réteg:** egy bolt bekerülhet a niche-be **egyetlen** kulcsszóra optimalizált
listinggel, miközben teljesen mást árul. A katalógus-minta ezt leplezi le.

Ebből számoljuk a **korrigált bevételt**:

```
korrigált bevétel = (összes eladás ÷ hónapok) × ár × 316,33 × a katalógus layered aránya
```

**Amit nem tud:** ez **élettartam-átlag**, nem mai futásteljesítmény. Fiatal boltnál közel van
hozzá, réginél a lassú kezdeti évek lehúzzák — **kor szerint ezért nem szabad összevetni**.

**Ahol elbuktunk (kétszer):** először a katalógus-mintavétel hiányzott, és a teljes bolti bevételt
írtuk a niche-hez — a specialista medián 55%-kal esett, amikor pótoltuk. Másodszor a
címosztályozó a `man` szót rész-szóként kereste, ami a `mandala` minden előfordulására illeszkedett:
az „ember/portré 42%" valójában 2,4%.

---

## 5. Review — mit vettek meg ténylegesen

**Mit mér:** konkrét listingekhez kötött, **dátumozott** értékelések.
**Forrás:** Apify, boltonként a legfrissebb 50 (illetve 40).
**Egység — és ez a lényeg:** a sor egy review, de a **független megfigyelési egység az ELADÓ**.

1 581 nyers review → 36 duplikált sor levonva **1 545**; ebből a 21 igazolt bolthoz **1 027**.

**Miért ez a legjobb jelünk:** minden más réteg keresletet vagy kínálatot mér. Ez az egyetlen, ami
**tényleges vásárláshoz** kötődik, ráadásul listing-szinten és dátummal.

**Amit nem tud:**
- **abszolút eladást.** A review alsó becslés (nem mindenki értékel); csak az arányok használhatók.
- **piaci részesedést.** Boltonként a legfrissebb 50-et látjuk, tehát a boltok nagyjából **egyenlő
  súlyt** kapnak méretüktől függetlenül, és a forgalmas boltok rövidebb időszakot fednek le.
- **konverziót.** Azt látjuk, mit vettek meg — nem azt, hányan látták és nem vették meg.

**Ahol elbuktunk:** a mécses/lámpás irányt „nem egyszereplős torzításnak" neveztem, mert 7–14
**különálló listing** állt mögötte. De 29 review-ból **23 ugyanattól a bolttól** jött. Listingeket
számoltam eladók helyett. Ugyanaz a hibaosztály, mint a 3. rétegben — csak más egységgel.

---

## A lánc olvasási szabályai

**1. Rétegen belül hasonlíts, ne rétegek között.** A `shadow box` 153,5-ös aránya (1. réteg) és a
`layered svg` 6,3-a nem összemérhető, mert más a vevői szándék. A review-arány (5. réteg) és a
keresési trend (1. réteg) rendszeresen **ellentmond** egymásnak — a `deer svg` **+55,1%**-kal nőtt
keresésben, miközben az eladási indexe **0,23**, azaz masszívan túlkínált.

**2. Mindig mondd meg, mi a független egység.** Kulcsszónál a kifejezés, boltnál a **deduplikált**
bolt, review-nál az **eladó**. „Több adatpont van" nem érv, ha ugyanabból a forrásból jönnek.

**3. Lefelé haladva erősebb a bizonyíték, de szűkebb a minta.** A keresési adat 345 kifejezést fed
le, a review-adat 21 boltot. Ami mindkét végén megjelenik, az a legmegbízhatóbb — a **shadow box**
termékforma például kereslet-oldalon a legjobb arányú fájlszándékú kifejezés (75,6), eladás-oldalon
pedig **12 független eladótól** 328 review.

**4. Ha a rétegek ellentmondanak, az eladás nyer.** A kereslet szándékot nem mutat; az eladás igen.

## Kapcsolódó

[[findings/etsy-first-party-search-data]] · [[findings/keyword-database]] ·
[[findings/layered-niche-size-and-structure]] · [[findings/listing-craft]] ·
[[findings/review-mining]] · [[methods/revenue-estimation-method]] ·
[[pitfalls/2026-08-08-wrong-unit-of-independence]]
