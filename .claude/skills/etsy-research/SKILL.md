---
name: etsy-research
description: Etsy piackutatás végigvitele — kereslet, kínálat, bolt-bevétel, hosszú farok — a projekt saját mérési láncán, böngészőből, Apify nélkül. Használd, ha egy új niche-t, alterületet vagy kulcsszócsaládot kell felmérni, vagy meglévő mérést frissíteni.
---

# Etsy-kutatás

Ez a skill **nem tananyag, hanem sorrend és kapuk**. A 2026-08-12-i 3D-körben nem tudás hiányzott,
hanem az, hogy a meglévő wikit nem néztem meg, mielőtt forrást választottam — és emiatt egy már
dokumentált eszközt (SalesDoe) hagytam ki, majd rossz indokot írtam a fájlba.

## 0. kapu — olvasás, mielőtt bármit lekérdeznél

**Kötelező, ebben a sorrendben. Ne ugord át, akkor sem, ha „csak egy gyors mérés".**

1. `wiki/CLAUDE.md` — a séma és a „Mikor frissítsd" lista. Ez az aktuális feladat ellenőrzőlistája.
2. `wiki/methods/measurement-chain.md` — **kezdd itt**: keresés → találat → bolt → termék → eladás.
   Minden lépésnél ott van, mit tud és mit **nem** tud a forrás, és hol buktunk el vele.
3. `wiki/methods/browser-data-endpoints.md` — a négy végpont, amit ténylegesen hívni fogsz.
4. `wiki/faq.md` — **ez az a fájl, amit kihagytam.** Itt van megindokolva, melyik eszközt miért
   használjuk vagy nem használjuk. Ha egy forrás ellen szól, olvasd el az indokot, és nézd meg,
   **érvényes-e még** (a SalesDoe-nál az egyik érv elavult, a másik nem).
5. `wiki/pitfalls/` — mind. Ez hét dokumentált mérési hiba; a többségét egyszer már elkövettük.

Csak ezután válassz forrást. Ha a wiki egy forrás ellen szól és mégis használod, **írd le, miért
gondolod, hogy az indok már nem áll**.

## 1. Kereslet — Etsy Marketplace Insights

Ez az egyetlen első kézből jövő keresleti adat. `keresés / 1000 listing` a projekt alap-mérőszáma;
a viszonyítási pont a `layered svg`. **Ugyanaznap mérd le az alapértéket is** — két különböző napi
érték nem kerülhet egy táblába.

Nézd a `queryCvr`-t is, ne csak az arányt. A kettő rendszeresen **ellentmond** egymásnak, és a
magas arány + nulla konverzió gyanús negyed (ott a kereslet más termékformát akar).

## 2. Hosszú farok — Etsy autocomplete

A javaslat azt jelenti, hogy az Etsy **látta** a lekérdezést, nem azt, hogy van volumene. Minden
javaslatot mérj le az 1. lépésben, mielőtt következtetsz belőle.

Csoportosítsd **szándék** szerint, ne téma szerint: fájl-szándék, terméktartás, licenc-szándék,
szezonális. A layered kutatás legfontosabb szétválasztása is ez volt (`shadow box` vs
`shadow box svg`).

## 3. Kínálat és boltok

A bolt-populáció a Marketplace Insights `listingCards`-jából jön. **Specialista = legalább 3
külön listinggel rangsorol.** Aki egyszer szerepel, az zaj.

## 4. Bolt-bevétel — SalesDoe API

Van API, tehát tömegesen megy. A `price` viszont a lista- és az akciós ár között ingadozik, ezért
**minden belőle számolt bevétel felső becslés** — mondd is ki. Ahol tartós akció van (ebben a
piacban szinte mindenhol), ott az akciós árat külön szerezd meg.

## 5. kapu — mielőtt SZÁMOT írsz le

Mind az öt kérdésre legyen válaszod. Ha nincs, a szám nem mehet ki.

| # | kérdés | a hiba, amit megelőz |
|---|---|---|
| 1 | **Mi a populáció?** Hány, milyen szűréssel, deduplikálva? | `173 bolt` / `35 specialista` / `21 igazolt` — ez a különbség igaz és hamis állítás között |
| 2 | **Mi a függetlenségi egység?** Ugyanaz a bolt/listing hányszor számít bele? | egyszer már 65 „specialistát" vitt le 35-re |
| 3 | **Lista- vagy akciós ár?** | a mélyen diszkontálóknál torzít a legjobban, vagyis pont ott, ahol számít |
| 4 | **Van rögzített árfolyam a devizára?** | árfolyamot **kitalálni tilos** — ha nincs a `decisions/2026-08-06-exchange-rates` táblájában, a bolt darabszámmal szerepel, HUF nélkül |
| 5 | **Mintavételi műtermék-e?** | „217 bolt egyszer szerepelt" nem szétaprózottság, ha lekérdezésenként csak 19 kártyát láttál |

Külön: **a magas kereslet/kínálat arány önmagában nem következtetés.** Ellenőrizd a konverzióval,
és nézd meg, hogy a kereslet a **te termékformádat** akarja-e. A norse/kelta bukás pontosan ez volt.

## 6. Kimenet — a wiki szerződése

1. **Nyers adat** → `wiki/assets/data/<tema>-<forras>-<ÉÉÉÉ-HH-NN>.json`, `meta` blokkal: forrás,
   módszer, populáció, és a **fenntartások felsorolva**.
2. **Finding** → `wiki/findings/<tema>.md` a séma szerint: Lényeg / Populáció / Számok /
   Fenntartások / Provenancia. A Lényeg **emberi nyelven**, ne számfelsorolás.
3. **Napló** → egy önmagában érthető sor a `wiki/_log.md` tetejére.
4. **Index** → sor a `wiki/index.md` megfelelő szakaszába.
5. **Ha egy szám megváltozott korrekció miatt** → kötelező `wiki/pitfalls/ÉÉÉÉ-HH-NN-<slug>.md`.
   Soha ne írj felül csendben egy számot.

## 7. Felülvizsgálat

Kérj **codex-elemzést** a nyers adatra és a findingre, mielőtt lezárod. A kérdés ne az legyen, hogy
„jó-e", hanem: *mi következik az adatból és mi nem; hol húzok túl következtetést; melyik számomat
vonnád kétségbe; ha egy dolgot kéne még megmérni, mi lenne.* Az így kapott kritikát **építsd be
fenntartásként**, ne vitatkozz vele.

## Eszköz

`harvest.js` — másold be a böngésző konzoljába (vagy futtasd a `javascript_tool`-lal) egy
bejelentkezett Etsy-fülön. Telepíti a `window.ER` objektumot mind a négy gyűjtővel. Részletek a
fájl tetején.

**A CDP-hívás 45 másodperc után elszáll**, ezért mindig **8-as adagokban** futtasd a ciklusokat, és
a részeredményt tartsd `window`-on — a következő hívás onnan folytatja.
