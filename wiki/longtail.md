---
type: Reference
title: Hosszú farok szógyűjtemény — bővíthető kifejezés-készlet családonként
description: 412 kifejezés 8 családban (kutyafajta, macskafajta, USA államok, nemzeti parkok, zodiákus/születési, papíros jelenetek, kelta/norse, alkalmak), mérés-idősorral.
status: living
generated:
  by: claude-fable-5
  at: 2026-08-09T16:00:00Z
---

# Hosszú farok szógyűjtemény

**Miért van:** a projekt alaptézise, hogy a kategóriát nem egy nagy kulcsszóval nyered meg, hanem
sok apró alfajjal ([[findings/keyword-demand-sweep]]). Ehhez kell egy hely, ahonnan mindig lehet
nyúlni a következő 20 listingért, és ami **nő**, nem újraíródik.

**Hol:** `assets/data/longtail/<család>.json`. Kezelő: `assets/scripts/longtail.py`.

## Állapot (2026-08-09)

| család | kifejezés | mérve | megjegyzés |
|---|---:|---:|---|
| dog-breeds | 129 | 3 | a `dachshund svg` 45,9/1000 a bizonyított minta |
| paper-scenes | 50 | 0 | **a papíros oldal szótára** — jelenet, nem ornamens |
| us-states | 50 | 2 | családként halott (0,7), egyenként él (texas 11,3) |
| us-national-parks | 47 | 1 | a hegy-család legjobb kifejezése (12,8, +13,8%) |
| cat-breeds | 45 | 0 | kisebb piac, azonos logika |
| zodiac-birth | 36 | 0 | 12+12+12, teljes lefedés olcsó |
| celtic-norse | 28 | 3 | `yggdrasil` 90,8 — a legkevésbé telített mért kifejezés |
| occasions | 27 | 0 | szezonális, augusztusban minden alulmér |
| **összesen** | **412** | **9** | 2,2% |

## Használat

```
python wiki/assets/scripts/longtail.py list                  # mi van benne
python wiki/assets/scripts/longtail.py todo --limit 40        # mit mérjünk, kész Insights-URL-lel
python wiki/assets/scripts/longtail.py record dog-breeds beagle --searches 180 --results 4200 --trend=+5.1
python wiki/assets/scripts/longtail.py rank                   # rangsor keresés/1000 szerint
python wiki/assets/scripts/longtail.py add paper-scenes "koi pond" "zen garden"
```

**A `record` idősort épít**, nem ír felül: ugyanaz a szó többször mérhető, a régi mérés megmarad.
Így a szezonalitás később kiolvasható — ami fontos, mert minden eddigi mérésünk augusztusi
([[findings/keyword-demand-sweep]]).

A `rank` a **300 keresés/hó zajküszöb** felett és alatt külön listáz. A küszöb alatti
trendszázalék értelmezhetetlen.

## Mit ne várj tőle

A gyűjtemény **kereslet-oldali**. Azt nem mondja meg, mi **fogy** — ahhoz review-bányászat kell
([[findings/review-mining]]), és ez a mérési lánc ötödik, hiányzó rétege
([[methods/measurement-chain]]). Egy magas keresés/1000 arány önmagában csak azt jelenti, hogy
kevesen kínálják — nem azt, hogy sokan veszik.

## Bővítés

Új család akkor kell, ha egy kutatás új motívum-dimenziót nyit (így született a `paper-scenes`
a [[findings/paper-layered-market]] alapján). A `note` mezőben mindig legyen ott, melyik finding
indokolja a családot.
