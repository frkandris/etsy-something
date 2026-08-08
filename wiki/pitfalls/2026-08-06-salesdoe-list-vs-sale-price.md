---
type: Pitfall
title: A SalesDoe medián ára a lista- és az akciós ár között ingadozik
description: Emiatt a bevételbecslése a mélyen diszkontáló boltoknál jelentősen felfelé torzít.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# SalesDoe: lista- vagy akciós ár?

**Dátum:** 2026-08-06 · **Súlyosság:** a régi `revenue estimation` tábla abszolút számait érinti

## Tünet

A BlankPrintsArts-ot „magas áron nagy volument elérő" boltként emeltem ki: SalesDoe medián ár
**18 USD (5 694 HUF)**, becsült bevétel 1,86M HUF/hó.

A boltoldalon viszont mind az 1 211 tétel akciós, és a kiemelt bundle-ök egységesen **2 627 HUF**
(7 507-ről, −65%).

## Gyökérok

A SalesDoe medián ára **nem következetesen** a lista- vagy az akciós ár:

| bolt | SalesDoe medián | látott akciós ár | látott listaár |
|---|---:|---:|---:|
| BlankPrintsArts | 5 694 | 2 627 | 7 507 |
| ColorLayerArt | 2 214 | 1 313–1 501 | 2 920–3 336 |
| MagicVectorLaser | 2 372 | 1 878–2 128 | 3 130–3 546 |
| TheMelodyFace | 1 455 | 1 155–1 592 | 3 856–5 393 |

Három esetben a kettő **között** van, egyben az akciós árral egyezik. Valószínű ok: ingyenes fiókkal
a SalesDoe a legfrissebb 25 listingből mintázik, és nem egységesen kezeli az akciót.

## Alkalmazott korrekció

- A BlankPrintsArts-ra épített állítás visszavonva.
- A niche-kutatás **nem** SalesDoe-t használ, hanem az Apify keresési találatok `price` /
  `originalPrice` mezőit, ahol a kettő explicit külön van. Lásd
  [[methods/revenue-estimation-method]].
- A `revenue estimation` fülhöz külön kedvezmény-oszlopok készültek volna, de az 52 bolt lekérése
  30–60 USD lett volna; **nyitott feladat**.

## Tanulság

Ahol tartós akció van (a boltok 75%-ánál), ott **egy „medián ár" mező önmagában használhatatlan** —
lista- és akciós árat külön kell megkapni, különben a becslés a legmélyebben diszkontálóknál torzít a
legjobban, vagyis pont ott, ahol a legfontosabb lenne.
