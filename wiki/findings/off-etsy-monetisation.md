---
type: Finding
title: A pipeline monetizálása az Etsyn kívül — csatorna-rangsor 3 hónapos időtávra
description: "Külső kutatás (2026-08-09): marketplace-terítés (CF+DesignBundles+Cults3D) a legjobb óradíj; Glowforge Catalog passzív royalty; SaaS-irány 3 hónapon belül nulla bevétel."
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-09T00:30:00Z
sources:
  - resource: /assets/data/off-etsy-monetisation-report-2026-08-09.md
    title: A felhasználó által hozott külső piackutatási jelentés, teljes szöveg
---

# A pipeline monetizálása az Etsyn kívül

## Lényeg

Külső kutatás (a felhasználó hozta, 2026-08-09). A kérdés: az automatizált „kép → vágásbiztos
réteges vektor" pipeline kibocsátását hol érdemes még pénzzé tenni az Etsyn kívül. A rangsor
**bevétel / befektetett munkaóra** alapján, 3 hónapos ablakban:

1. **Marketplace-terítés** (Creative Fabrica + Design Bundles + Cults3D párhuzamosan) — a
   feltöltés marginális költsége listánként közel nulla, a platform hozza a vevőt. Nem-exkluzív:
   ugyanaz a fájl mehet mindenhová + az Etsyre.
2. **Glowforge Catalog** — pay-per-print royalty, védett fájl; Premium-tagság + jóváhagyás kell,
   az árazás átláthatatlan és a Glowforge kezében van.
3. **Saját webshop** (Gumroad → Payhip) — ~90% margó, de a forgalmat neked kell hoznod.
4. **B2B / extended licenc** — magas ticket, lassú beindulás.
5. **Pipeline mint SaaS** — legnagyobb plafon, 3 hónapon belül gyakorlatilag nulla bevétel.

## Kulcsszámok

| állítás | szám | forrás jellege |
|---|---|---|
| CF „multilayer laser cut" telítettség | 5 991 tétel (+143k ingyenes lézeres fájl) | pillanatfelvétel |
| CF kifizetés előfizetéses letöltésre | „pár cent"/letöltés; egyszeri eladásnál ~0,40–0,45 $ | designer-beszámolók |
| CF passzív jövedelem realitása | 50–200 designnal néhány tíz $/hó; 500 termék ↛ 100 $/év is előfordul | designer-beszámolók, erős szórás |
| Cults3D payout | **80%** designernek, díjak nélkül; lézeres kínálat ~3–4k fájl (kicsi) | platform-közlés |
| Design Bundles payout | 75% (direkt) / 50% (affiliate) | platform-közlés |
| Glowforge Catalog kereslet | „5 hónap alatt 122×" | gyártói blog |
| Etsy kontextus | eladók 7M→5,6M; vevők −3,4% YoY; take rate 24,5%; organikus Google-forgalom −50%/2 év | Marketplace Pulse, 10-K, CraftedCharts |

## Következmények a projektre

- A számozott iterációs mappák (`product/iterations/`) kimenete közvetlenül teríthető: a
  nem-exkluzivitás miatt a CF/DB/Cults3D listázás nem üti az Etsy-tervet, csak megsokszorozza
  ugyanazt a munkát. A batch-feltöltés automatizálható — ez ugyanaz a tézis, mint a
  [[workflows/production-pipeline]] hosszú farok logikája.
- A **vágásbiztonsági riport mint differenciáló** ([[workflows/production-pipeline]]: connectivity,
  min. web, nyak-detektálás, kulcslyuk) a SaaS-irányban lenne a fő érv — de a kutatás szerint ez
  3 hónapon belül nem termel, és az xTool AIMake / CF Spark kommoditizálja a generálást.
- A MakerPlace by Michaels kizárt (csak handmade fizikai termék).
- Küszöbök a stratégiaváltáshoz a teljes jelentésben (assets).

## Fenntartások

Külső kutatás, saját méréssel nem ellenőriztük. A jövedelem-adatok designer-beszámolókból
származnak, erős szórással; a telítettségi számok pillanatfelvételek. A CF nem publikál
letöltés-riportot, a Glowforge algoritmusa titkos.

## Provenancia

Teljes szöveg: `wiki/assets/data/off-etsy-monetisation-report-2026-08-09.md`. Kapcsolódik:
[[findings/competitor-listing-images]], [[findings/keyword-database]], [[decisions/2026-08-07-pursue-layered]].
