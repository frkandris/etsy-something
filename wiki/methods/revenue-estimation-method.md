---
type: Method
title: Hogyan számoljuk a bevételt — és mit nem jelent
description: Élettartam-átlag: összes eladás ÷ nyitás óta eltelt hónapok × mai tényleges ár × katalógus-arány.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Bevételbecslés

## A képlet

```
HUF/hó = (összes eladás ÷ nyitás óta eltelt hónapok)
         × medián tényleges eladási ár (USD)
         × 316,33
         × a katalógus layered aránya
```

Bemenetek: `sold_count`, `create_date`, `active_listing_count` az Etsy bolt-adatból (Apify);
`price` / `originalPrice` a keresési találatokból, boltonként mediánolva; a katalógus-arány a bolt
saját listingjeiből vett 24-es mintából.

## Amit jelent

Az adott bolt **teljes élettartamára vetített átlagos havi bevétele**, a mai árszinten, csak a niche-be
tartozó termékekre.

## Amit NEM jelent

- **Nem aktuális futásteljesítmény.** Egy fiatal boltnál közel van hozzá (rövid az élettartam), egy
  régi boltnál viszont a lassú kezdeti évek lehúzzák. **Kor szerint ezért nem szabad összevetni.**
- **Nem árbevétel.** Az Etsy-díjak, a visszatérítések és az áfa nincsenek levonva.
- **Nem veszi figyelembe a szezonalitást** és a bolt növekedési vagy zsugorodási pályáját.

## Miért ez, és nem a SalesDoe becslése

A SalesDoe `Est. Revenue / Month` mezője kényelmesebb lenne, de három baja van: (1) csak a
felhasználó bejelentkezett munkamenetén át érhető el, boltonként egy kattintással; (2) a medián ára a
listaár és az akciós ár között ingadozik, ami a mélyen diszkontálóknál jelentősen felfelé torzít
(lásd [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]]); (3) ingyenes fiókkal a legfrissebb 25
listingből mintáz.

A saját képlet cserébe hordozza a maga torzítását (élettartam-átlag), ami viszont **ismert és
egyirányú**, tehát korrigálható fejben.

## Árfolyam-konvenció

**USD = 316,33 HUF**, **EUR = 364,6 HUF**. Ezek nem a napi jegyzések, hanem a felhasználó meglévő
2026-08-06-os sorai alapján visszafejtett értékek — a konzisztencia fontosabb volt, mint a pontosság.
Lásd [[decisions/2026-08-06-exchange-rates]].
