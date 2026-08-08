---
type: Glossary
title: Fogalmak
description: A kutatásban használt metrikák és megbízhatósági szintek definíciói.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Fogalmak

## Populáció-szintek

- **nyers populáció** — minden bolt, ami megjelent a keresési találatokban (layered: 173).
  Használható a piac zsúfoltságának jellemzésére, **bevételi állításra nem**.
- **specialista** — legalább 3 **különálló** listinggel rangsorolt (layered: **35**; funkcionálisnál a
  küszöb 2). *A korábbi 65-ös szám hibás volt: keresési sorokat számolt*. Lásd [[pitfalls/2026-08-07-duplicate-search-hits]].
- **igazolt (verified)** — specialista, **és** a saját katalógusából mintavett 24 listing legalább
  80%-a a niche-be tartozik (layered: **21**). Minden `findings/` szám alapértelmezésben ezen a halmazon
  számol.

## Metrikák

- **korrigált bevétel** — `(összes eladás ÷ hónapok) × tényleges ár × 316,33 × katalógus-arány`.
  Élettartam-átlag, nem futásteljesítmény. Lásd [[methods/revenue-estimation-method]].
- **HUF/listing** — korrigált bevétel ÷ aktív listingszám. A niche fő hatékonysági mutatója: megmondja,
  hány listing kell egy adott bevételhez.
- **tartós kedvezmény** — `1 − (eladási ár ÷ listaár)`. A boltok 75%-ánál állandó, nem időszakos.
- **layered arány** — a bolt katalógusából mintavett listingek közül hány százalék tartalmaz
  layered kulcsszót (`multilayer`, `layered`, `N layer`, `3d mandala`, `shadow box`).
- **találat / különálló találat** — hányszor jött elő a bolt az öt keresésben. A „különálló" a
  deduplikált szám; csak ez használható.

## Termékfogalmak

- **multilayer / layered SVG** — több (jellemzően 5–12) rétegre bontott vektorfájl, amiből
  egymásra ragasztva térhatású fali dekor lesz. Célgép: lézervágó, CNC router, papírvágó.
- **commercial licence** — a fájl olyan licence, ami engedi, hogy a vevő terméket gyártson és adjon
  el belőle. Az igazolt boltok 1%-a említi, de akik igen, jóval jobb számokat hoznak
  ([[findings/listing-craft]]).
- **kerf** — a lézervágás által elmart anyagszélesség; a rétegek illesztéséhez kompenzálni kell.
- **horgonyár (anchor price)** — a felárazott „eredeti" ár, amihez képest a tartós akciót hirdetik.
