# etsy-something

Piackutatás egy Etsy digitális termék niche-ről: **multilayer / layered lézervágott SVG fájlok**.

**Kezdd itt: [`wiki/overview.md`](wiki/overview.md)** — a teljes kép egy oldalon.

## Mi ez

Nem kódprojekt. Egy kutatás, aminek a fő terméke a `wiki/` — egy LLM által karbantartott
tudásbázis, ami a mért következtetéseket a hozzájuk tartozó **populációval és fenntartásokkal**
együtt rögzíti.

```
wiki/
├── CLAUDE.md      a séma — mikor és hogyan kell frissíteni
├── index.md       tartalomtérkép
├── overview.md    a teljes kép
├── findings/      mért következtetések (mindegyik megmondja, melyik populáción számol)
├── methods/       hogyan készült az adat, mit jelent, mibe kerül újra
├── shops/         referenciaboltok, a visszavont adatpontokkal együtt
├── pitfalls/      mérési hibák postmortemjei  <- a legértékesebb rész
├── decisions/     döntések és az indoklásuk
├── workflows/     ismételhető eljárások
└── assets/        nyers adat + elemző szkriptek (csak olvasható)
```

## A legfontosabb szabály

**Soha ne írj le számot a populációja nélkül.** Ebben a projektben a
`173 bolt` / `65 specialista` / `33 igazolt` megkülönböztetés a különbség egy igaz és egy hamis
állítás között. Négy ígéretes következtetés bukott meg azon, hogy ezt elmulasztottuk — lásd
[`wiki/pitfalls/`](wiki/pitfalls/).

## A jelenlegi következtetés

Rétegzett lézervágott SVG, a **nem akciózó, magasabb árú végén** (70–200 listing, $9–28, tartós
kedvezmény nélkül). Termékirány eladási adat alapján: **kereszt + mandala + amerikai zászló
kombók**, mellé **mécses/lámpás csomagok**. Részletek:
[`wiki/findings/review-mining.md`](wiki/findings/review-mining.md).

## Apps Script fájlok

A Google Sheet írása generált `.gs` fájlokkal megy, amiket a felhasználó futtat — az indoklás:
[`wiki/decisions/2026-08-06-apps-script-for-sheets.md`](wiki/decisions/2026-08-06-apps-script-for-sheets.md).
