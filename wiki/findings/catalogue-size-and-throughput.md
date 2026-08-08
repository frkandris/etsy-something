---
type: Finding
title: Katalógusméret, belépési kohorszok és termelési tempó
description: A 100-300 listinges sav a legjobb listingenkenti hozamu (dedupolva is); a belepesi arany rangsorolas-tulelesi arany, nem valoszinuseg.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
sources:
  - resource: /assets/data/layered_adjusted.json
    title: igazolt boltok (dedupolva 21; a 33-as szűrő hibás volt)
---

# Katalógusméret és termelési tempó

> **AUDIT 2026-08-08 UTÁN.** A katalógusméret-eredmény **túlélte** a deduplikálást: a 100–300-as sáv
> dedupolva **2 009 HUF/listing** (300–700: 825), tehát a fő ajánlás áll. A **belépési esély** viszont
> félrevezetően volt megfogalmazva: a nevező csak olyan fiatal boltokat tartalmaz, amelyek **ma
> rangsorolnak** a top találatok közt — a megbukott és bezárt belépők szerkezetileg hiányoznak
> (0/173 bezárt bolt a mintában, szemben a követett kohorsz 13/57-ével). Ez **rangsorolás-túlélési
> arány, nem belépési valószínűség**. Lásd [[pitfalls/2026-08-08-wrong-unit-of-independence]].

## Lényeg

Két járható út van: **tömeg** (700+ listing) vagy **fókusz** (100–300 listing magasabb áron). A
tömegút a vietnámi/ukrán stúdiók pályája; a fókuszút az, amit egyedül meg lehet nyerni. **100 listing
alatt a medián bolt kicsi**, tehát a „30 listinggel is megy" gondolat kivétel, nem szabály.

## Populáció

33 **igazolt** bolt, katalógus-aránnyal korrigált bevétel.

## Katalógusméret vs eredmény

| listing | boltok | medián HUF/hó | HUF/listing |
|---|---:|---:|---:|
| <100 | 6 | 70 338 | 1 429 |
| **100–300** | 15 | 321 653 | **1 674** |
| 300–700 | 10 | 375 415 | 825 |
| 700+ | 2 | 1 545 840 | 1 626 |

A 300–700-as sáv listingenként a leggyengébb: ott már benne vagy a tömegversenyben, de még nincs meg
a 700+ mérete.

## Kor, méret, tempó

| kor | boltok | medián HUF/hó | medián listing | tempó |
|---|---:|---:|---:|---:|
| <1,5 év | 12 | 208 955 | 189 | **20,4 listing/hó** |
| 1,5–3 év | 7 | 416 893 | 249 | 9,8 |
| 3–5 év | 3 | 532 762 | 199 | 4,6 |
| 5+ év | 11 | 474 337 | 295 | 3,8 |

A tempó-oszlop a fontos: **a friss belépők négy-ötször gyorsabban töltik a katalógust**, mint a
beágyazott boltok. Ez a belépés valós ára — nem a designok darabszáma, hanem a felfutási ütem.

A kor szerinti bevétel-emelkedés **részben műtermék**: a bevétel élettartam-átlag, így a régi
boltoknál a lassú kezdeti évek lefelé húzzák, a fiataloknál viszont a mai futás közeli. Ne olvasd ki
belőle, hogy „3–5 év alatt itt tartasz".

## Belépési esély

3 évnél fiatalabb boltok, **specialista** populáció (65-ből 37 bolt), katalógus-korrekció után:

| sáv | boltok |
|---|---:|
| >1M HUF/hó | 1 (3%) |
| 500k–1M | 5 (14%) |
| 200–500k | 9 (24%) |
| <200k | 22 (59%) |

Vagyis nagyjából **minden hatodik-hetedik friss belépő jut 500 ezer fölé**. A korrekció előtt ez 19%
volt, lásd [[pitfalls/2026-08-07-whole-shop-revenue-attribution]].

## Gyakorlati célszám

**100–300 listing, havi 4–10 új tétel.** (Dedupolva a 100–300 sáv 2 009 HUF/listinget hoz, n=8; a
<100 sávban **egy** bolt maradt.) Ez a fókuszút alsó fele, egyedül tartható tempóval. *(A korábban idézett két kis bolt — [[shops/laserartisandesigns]] és [[shops/woodlusterstore]] — a
deduplikálás után kiesett a populációból, tehát a „kis katalógus magas árral” érv elvesztette a
bizonyítékát.)*

## Provenancia

`assets/scripts/layered_deep.py` 4. és 5. szakasz; `assets/scripts/adjust.py` (belépési esély).
