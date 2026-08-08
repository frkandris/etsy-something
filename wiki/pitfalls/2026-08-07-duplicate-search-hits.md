---
type: Pitfall
title: Ugyanaz a listing háromszor számolva megbízhatóságnak
description: A találatszám nem különálló listingeket számolt, így egy listing több keresésből 'megbízható' boltot csinált.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Duplikált találatok mint hamis megbízhatóság

**Dátum:** 2026-08-07 · **Súlyosság:** egy kiemelt adatpontot érintett

## Tünet

A [[shops/beameez]] „3 találattal", tehát **közepes megbízhatósággal** került a specialista halmazba,
és a legjobb listingenkénti hozamú boltként (38 533 HUF/listing) a fő ajánlás alapja lett.

## Gyökérok

A találatszámot a keresési eredményekben megjelenő **sorok** számából képeztem, nem a **különálló
listingekéből**. A Beameez három találata:

```
Layered Mandala Laser Cut File, 9-Layer 3D Wall Art SVG DXF AI LightBurn Download
Layered Mandala Laser Cut File, 9-Layer 3D Wall Art SVG DXF AI LightBurn Download
Layered Mandala Laser Cut File, 9-Layer 3D Wall Art SVG DXF AI LightBurn Download
```

Ugyanaz az **egy** listing, három különböző keresésből. A szűrő, amit az előző hiba
([[pitfalls/2026-08-07-single-listing-attribution]]) ellen vezettem be, pont ezt nem fogta meg.

## Hogyan derült ki

A katalógus-mintavétel: a Beameez 24 listingjéből **nulla** layered.

## Alkalmazott korrekció

- A funkcionális szegmens felmérésénél már **különálló címeket** számolok (`fn_shops.json`
  `distinct` mezője).
- A Beameez-re épített minden állítás visszavonva.

## Tanulság

**Az öt keresés nem öt független minta** — átfedő találathalmazokat adnak. Bármilyen „hányszor jött
elő" metrika csak deduplikálás után értelmes. Általánosabban: egy származtatott megbízhatósági
mutató annyit ér, amennyire a hibát, ami ellen készült, ténylegesen kizárja — ezt külön ellenőrizni
kell, nem feltételezni.
