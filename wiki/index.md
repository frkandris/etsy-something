---
okf_version: "0.2"
type: Index
title: etsy-something — kutatási wiki
description: Belépési pont; innen indul minden.
---

# etsy-something — kutatási wiki

Piackutatás egy Etsy digitális termék niche-ről. Kezdd itt: **[[overview]]** — a teljes kép egy
oldalon.

A karbantartás szabályai: **[[CLAUDE|CLAUDE.md]]** (séma). Változásnapló: **[[_log]]**.

## Referencia

- [[longtail]] — **hosszú farok szógyűjtemény** (412 kifejezés, 8 család, bővíthető)

- [[workflows/worldmap-pipeline]] — **világtérkép-lánc**: mért mélység, generátor nélkül
- [[workflows/product-profiles]] — termék-profilok (JSON) és a közös vágás-geometria; miért lett profil-adat, ami korábban konstans volt
- [[workflows/recessed-papercut-pipeline]] — **a süllyesztett papírvágás-lánc** (a tényleges termékszerkezet)

## Eredmények — `findings/`

- [[findings/layered-niche-size-and-structure]] — mekkora és mennyire zsúfolt a piac
- [[findings/pricing-and-discounting]] — **a legerősebb jelzés**: ár és tartós kedvezmény
- [[findings/catalogue-size-and-throughput]] — hány listing kell, milyen tempóval
- [[findings/geography-and-cost-competition]] — kivel versenyzel, hol a rés
- [[findings/listing-craft]] — címek: gépek, formátumok, rétegszám, témák
- [[findings/competitor-listing-images]] — képek: színes karton + keret + lifestyle háttér nyer
- [[findings/off-etsy-monetisation]] — külső kutatás: hol pénz a pipeline az Etsyn kívül
- [[findings/geographic-motifs]] — városok/tavak/hegyek/államok/országok: mi él és mi halott
- [[findings/laser-vs-paper-split]] — **lézer vs papír**: a kínálat szétválik, a fájdalom nem
- [[findings/paper-layered-market]] — **a papíros piac**: övé a legjobb kulcsszó, de távtartó és keretméret kell
- [[findings/verified-shop-list]] — a bolt-lista (a 33-as szűrő hibás volt, dedupolva 21)
- [[findings/functional-segment-comparison]] — a felmért alternatíva, és miért nem váltunk
- [[findings/independent-second-opinion]] — **független elemzés** ugyanabból az adatból
- [[findings/review-mining]] — **mi fogy ténylegesen**: kínálat vs eladás, és a norse/kelta bukása
- [[findings/keyword-database]] — **345 kulcsszó volumennel**: hol a hosszú farok a kutyákon túl
- [[findings/keyword-demand-sweep]] — **kereslet 40+ kifejezésre**: hol a rés, és miért a thumbnail dönt
- [[findings/etsy-first-party-search-data]] — **kereslet első kézből**: volumen, trend, és a vevői szókincs
- [[findings/niche-comparison]] — **layered vs 3D**: azonos alapú összehasonlítás, percentilisekkel
- [[findings/3d-shop-list]] — **3D bolt-lista** SalesDoe bevétellel, a layered lista szerkezetében
- [[findings/3d-print-market-structure]] — **3D piacszerkezet**: boltok, hosszú farok, és a licenc mint vásárlási jelzés
- [[findings/3d-print-first-look]] — **3D nyomtatás**: jobb kereslet/kínálat, de a konverzió nem követi
- [[findings/2024-vs-2026-cohort]] — az egyetlen valódi idősorunk

## Referenciaboltok — `shops/`

- [[shops/magicvectorlaser]] — a niche felső mércéje
- [[shops/colorlayerart]] — a friss belépő bizonyítéka
- [[shops/laserartisandesigns]] — a legkonzisztensebb adatpont
- [[shops/woodlusterstore]] — a legkisebb működő katalógus
- [[shops/beameez]] — **visszavont** adatpont, tanulságként megtartva

## Módszer — `methods/`

- [[methods/measurement-chain]] — **kezdd itt**: a keresés → találat → bolt → termék → eladás lánc
- [[methods/data-collection-pipeline]] — a négy lépés
- [[methods/revenue-estimation-method]] — mit jelent a bevételszám és mit nem
- [[methods/browser-data-endpoints]] — **böngészős végpontok**: Marketplace Insights, autocomplete, bolt-oldal, SalesDoe API
- [[methods/apify-actors]] — melyik actor mit ad, mibe kerül
- [[methods/keyword-tools-comparison]] — öt kulcsszóeszköz mérés alapján

## Mérési csapdák — `pitfalls/`

- [[pitfalls/2026-08-12-rossz-populacio-harmadszor]] — a hibás populáció, harmadszor
- [[pitfalls/2026-08-11-a-szuro-torolte-a-felso-lapokat]] — a szűrő a felső lapokat és a nyílásokat is törölte
- [[pitfalls/2026-08-07-single-listing-attribution]] — a populáció fele hamis pozitív volt
- [[pitfalls/2026-08-07-duplicate-search-hits]] — ugyanaz a listing háromszor számolva
- [[pitfalls/2026-08-07-whole-shop-revenue-attribution]] — −55% a mediánban
- [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]] — lista- vagy akciós ár?

## Döntések — `decisions/`

- [[decisions/2026-08-11-keret-eloszor]] — a rétegsorrend tervezői döntés, nem mérés
- [[decisions/2026-08-10-keprogeneralas-iranya]] — lapos illusztráció + külön mélységbecslés
- [[decisions/2026-08-10-cc0-eszkozok-a-hatterben]] — a háttér CC0 3D geometria, nem lapos fotó
- [[decisions/2026-08-07-pursue-layered]] — marad a layered
- [[decisions/2026-08-06-apps-script-for-sheets]] — sheet-írás Apps Scripttel
- [[decisions/2026-08-06-exchange-rates]] — rögzített árfolyamok
- [[decisions/2026-08-08-parked-directions]] — **várólista**: termék-vetületek és review-bányászat

## Folyamatok — `workflows/`

- [[workflows/norse-celtic-catalogue-plan]] — ~~katalógusterv~~ **visszavonva**, dokumentációként
- [[workflows/production-pipeline]] — AI-támogatott layered fájlgyártás
- [[workflows/sheet-updates]] — hogyan írunk a Sheetbe

## Szótár és kérdések

- [[glossary]] · [[faq]]

## Nyers anyag — `assets/`

`assets/data/` a lehúzott adathalmazok, `assets/scripts/` az elemző szkriptek. **Csak olvasható.**
