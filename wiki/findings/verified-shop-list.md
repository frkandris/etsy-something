---
type: Finding
title: A layered bolt-lista (a 33-as szuro hibas volt; dedupolva 21)
description: A 33-as lista a hibas szuron alapul; dedupolva 21 bolt a referencia-populacio.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/layered_adjusted.json
    title: specialista boltok share mezovel
---

# A bolt-lista (33-as, hibás szűrővel)

> **AUDIT 2026-08-08 UTÁN.** A lista a **hibás, nem deduplikált** szűrőn alapul: a 33-ból csak **21**
> teljesíti a ≥3 **különálló** listing feltételt. A táblázat dokumentációként marad. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

Ez a kutatás **referencia-populációja**: minden más `findings/` oldal ezen a halmazon számol, hacsak
külön nem jelzi. Kritérium: legalább 3 különálló listinggel rangsorolt a niche keresésekben, **és** a
saját katalógusából mintavett 24 listing legalább 80%-a layered.

A `HUF/hó` oszlop katalógus-aránnyal korrigált élettartam-átlag — lásd
[[methods/revenue-estimation-method]] arról, mit jelent és mit nem.

| bolt | HUF/hó | listing | HUF/listing | ár | akció | év | layered% | ország |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| MarLaserCut | 9 424 361 | 274 | 34 395 | $102.97 | 50% | 4.1 | 96% | AU |
| MagicVectorLaser | 2 274 147 | 934 | 2 435 | $5.10 | 36% | 5.6 | 100% | UA |
| CNCArtStore | 2 259 521 | 408 | 5 538 | $7.49 | 0% | 6.3 | 92% | UA |
| CutCutePaper | 1 255 180 | 274 | 4 581 | $8.40 | 30% | 6.0 | 92% | BG |
| ColorLayerArt | 987 537 | 559 | 1 767 | $3.26 | 55% | 2.8 | 100% | UA |
| LaserArtisanDesigns | 867 770 | 72 | 12 052 | $28.21 | 0% | 2.5 | 83% | GB |
| SVGColorCNC | 817 533 | 1001 | 817 | $12.00 | 34% | 6.5 | 100% | UA |
| HouseLaserCut | 624 562 | 345 | 1 810 | $3.20 | 60% | 2.5 | 96% | UA |
| Arqovia | 617 358 | 295 | 2 093 | $6.65 | 0% | 6.4 | 92% | LV |
| BKCUT | 590 159 | 570 | 1 035 | $7.48 | 25% | 0.6 | 96% | VN |
| DIYMakerDesigns | 532 762 | 199 | 2 677 | $14.26 | 0% | 3.6 | 92% | DE |
| VectorSVGLaboratory | 474 337 | 189 | 2 510 | $4.65 | 40% | 5.4 | 100% | UA |
| ApexLayer3D | 430 674 | 577 | 746 | $4.99 | 50% | 0.4 | 100% | VN |
| YarensWoodDream | 416 893 | 249 | 1 674 | $3.12 | 25% | 2.1 | 96% | TR |
| FanfenStudio | 398 717 | 207 | 1 926 | $4.50 | 50% | 0.3 | 83% | ID |
| VyvaStudioDigital | 321 653 | 131 | 2 455 | $5.91 | 40% | 10.1 | 88% | NZ |
| PetalSmith3D | 320 156 | 400 | 800 | $5.98 | 40% | 1.3 | 100% | VN |
| WoodLusterStore | 315 434 | 29 | 10 877 | $9.00 | 0% | 1.1 | 96% | AR |
| LeVanilleShop | 284 592 | 180 | 1 581 | $4.13 | 30% | 5.3 | 96% | UA |
| CutingDesignsSVG | 282 369 | 211 | 1 338 | $8.80 | 60% | 0.9 | 100% | UA |
| DigitaldesignsfromA | 278 433 | 328 | 849 | $8.00 | 0% | 2.8 | 100% | UA |
| MaWoodCreationStore | 248 225 | 534 | 465 | $6.00 | 40% | 6.2 | 100% | GE |
| VectorDanaArt | 163 316 | 117 | 1 396 | $2.80 | 60% | 2.1 | 100% | UA |
| StudioTokanoLayerSVG | 144 939 | 304 | 477 | $5.96 | 25% | 15.8 | 100% | ? |
| CutCraftStudioStore | 135 541 | 171 | 793 | $4.38 | 40% | 0.9 | 92% | UA |
| MoodonwooD2 | 114 329 | 201 | 569 | $4.62 | 40% | 8.3 | 100% | UA |
| nostomalayersvg | 109 674 | 76 | 1 443 | $6.38 | 25% | 2.5 | 100% | TR |
| MultiLayerMaster | 86 724 | 427 | 203 | $4.79 | 20% | 1.1 | 88% | UA |
| DigitalLayeredDreams | 58 116 | 164 | 354 | $2.64 | 70% | 1.1 | 96% | UA |
| deliciousranger | 41 074 | 169 | 243 | $3.30 | 45% | 4.5 | 100% | ID |
| PremiumLaserFiles | 31 002 | 25 | 1 240 | $2.95 | 50% | 1.0 | 92% | TR |
| BosuyBober | 23 488 | 20 | 1 174 | $4.95 | 40% | 0.1 | 100% | UA |
| MultiLayerArts | 18 393 | 13 | 1 415 | $11.00 | 50% | 1.5 | 85% | AE |

## Amit érdemes kiolvasni belőle

- A lista teteje (MarLaserCut, MagicVectorLaser, CNCArtStore) 274–934 listinggel dolgozik, tehát a
  csúcs nem apró boltoké.
- A **MarLaserCut** $102,97-es ára kilóg; valószínűleg nagy csomagok vagy fizikai termék is van
  benne. Kezeld külön, ne húzza el a mediánokat.
- A két kis katalógusú kivétel ([[shops/laserartisandesigns]] 72, [[shops/woodlusterstore]] 29)
  mindkettő **0% akció** és $9 fölötti ár — lásd [[findings/pricing-and-discounting]].
- 15 ukrán bolt: lásd [[findings/geography-and-cost-competition]].
