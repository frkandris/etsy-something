# etsy-something

Piackutatás egy Etsy digitális termék niche-ről (multilayer / layered lézervágott SVG fájlok), plusz
a Google Sheet frissítésére generált Apps Script fájlok.

## Projekt tudásbázis — `wiki/`

A `wiki/` egy LLM által karbantartott tudásbázis ehhez a kutatáshoz. Azt tartalmazza, ami a
táblázatokból nem derül ki: a mért következtetéseket a hozzájuk tartozó populációval, a
módszertant, a döntéseket és az indoklásukat, és a mérési hibák postmortemjeit.

**Minden nem triviális feladat előtt ebben a projektben:**

- Olvasd el a `wiki/CLAUDE.md`-t — ez a séma. Meghatározza, mikor kell frissíteni a wikit és hogyan
  kell oldalt írni. A „Mikor frissítsd" listát kezeld az aktuális feladat ellenőrzőlistájaként.
- Fusd át a `wiki/index.md`-t — ez a tartalomtérkép. Keresd meg az érintett területhez tartozó
  oldalakat, és olvasd el őket. **Különösen a `wiki/pitfalls/` mappát**: ott van dokumentálva az a
  négy mérési hiba, ami már egyszer megváltoztatta a fő következtetést.

**Munka közben:**

- Ha új mérés fut le, egy szám korrekció miatt megváltozik, döntés születik, vagy egy boltot
  megvizsgálunk — hozd létre vagy frissítsd a megfelelő wiki-oldalt a séma szerint, és fűzz egy sort
  a `wiki/_log.md`-hoz.
- **Soha ne írj le számot a populációja nélkül.** Ebben a projektben a `173 bolt` / `65 specialista`
  / `33 igazolt` megkülönböztetés a különbség egy igaz és egy hamis állítás között.
- A `wiki/assets/` csak olvasható: nyers adatok és elemző szkriptek. Ne szerkeszd őket.

## Google Sheet

`1j-52jMBxTxgZ3-ywNekNGKjraP6u2QYDKxLVdMfsqUQ` — fülek: `revenue estimation` (gid 541292880),
layered niche (gid 1600752523), funkcionális szegmens (gid 594784454).

Az írás mindig generált Apps Scripttel megy, amit a felhasználó futtat — az indoklás és a kötelező
biztonsági elemek: `wiki/workflows/sheet-updates.md`.

## Titkok

Az Apify token a session scratchpadben van, **nem** ebben a mappában. Ne commitold sehova.
