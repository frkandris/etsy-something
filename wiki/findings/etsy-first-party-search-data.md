---
type: Finding
title: Etsy Marketplace Insights — első kézből jövő keresési adat
description: A `layered svg` havi 1200 keresést kap 189,9 ezer találat mellett és +11,1%-kal nő; a vevők viszont egészen más szavakat gépelnek, mint amikre a mezőny optimalizál.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T21:00:00Z
sources:
  - resource: https://www.etsy.com/your/shops/me/marketplace-insights
    title: Etsy Marketplace Insights (Etsy Plus, LasercutSupplier shop), 2026-08-07
---

# Etsy Marketplace Insights

**2026-08-07-től elérhető** az Etsy Plus előfizetéssel a `LasercutSupplier` boltban. Ez az **egyetlen
első kézből jövő keresési adatforrásunk** — minden más eszköz (eRank, Alura, RankHero) modellez.
Lásd [[methods/keyword-tools-comparison]].

## Amit a saját kulcsszavunkra mond

`layered svg`, utolsó 30 nap:

| | |
|---|---:|
| keresés | **1 200** |
| trend | **↑ +11,1%** |
| találat (versenyző listing) | **189 900** |
| arány | 1 : 158 |

**A +11,1% a kutatás legfontosabb új száma:** a kereslet nő. Ezt egyik harmadik feles eszköz sem
adta meg, és a [[faq]] korábban „nem tudjuk"-ként rögzítette.

## A döntő felfedezés: eladói vs vevői szókincs

Az Etsy „similar search terms" táblája a `layered svg`-hez:

| keresőkifejezés | keresés / 30 nap | találat | keresés / 1000 listing |
|---|---:|---:|---:|
| personalized gifts | 92 200 | 1,6M | **57,6** |
| bedroom wall art | 26 800 | 2,1M | **12,8** |
| sublimation designs | 6 400 | 714 200 | 9,0 |
| **layered svg** | **1 200** | **189 900** | **6,3** |
| digital download art | 12 400 | 4,2M | 3,0 |
| printable art | 8 700 | 3,3M | 2,6 |

A `bedroom wall art` **22-szer** annyi keresést kap, mint a `layered svg`, és kétszer jobb a
kereslet/kínálat aránya.

**Következtetés: az eddigi kutatás végig eladói szókincsben mozgott.** A `multilayer`, `layered`,
`SVG`, `DXF`, `laser cut` gyártói kifejezések. A [[findings/listing-craft]] címelemzése (85% említ
lézert, 36% CNC-t, 94% SVG-t) ezek szerint azt méri, hogy **a mezőny egymásnak optimalizál**, nem a
vevőnek.

Ezt megerősíti az eRank országmegoszlása ugyanerre a témára: a `multilayer svg` keresőinek **9,7%-a
ukrán** — vagyis egy érdemi rész nem vevő, hanem konkurencia-kutatás
([[methods/keyword-tools-comparison]]).

## Mit tud és mit nem

**Tud:** valós keresésszám, valós találatszám, napi bontású 30 napos görbe, trend százalék, hasonló
keresőkifejezések valós volumennel, kategóriánkénti „mit keresnek most" lista, mentett keresések.
Korlátlan lekérdezés az Etsy Plusszal.

**Nem tud:** 30 napnál hosszabb historikus adatot — vagyis **szezonalitást nem mutat**. A layered
termékkör viszont erősen szezonális (karácsony, halloween, Valentin), és a szezonalitás-görbe az
eRankon megvolt (15 hónap). Ez az egyetlen dolog, amiért egy harmadik feles eszköz még indokolt
lehet.

Figyelem: a „search results" minden illeszkedő listinget számol, ami tág kifejezéseknél felfelé
torzít. Az arányok irányadóak, nem pontosak.

## Következmény a stratégiára

A [[decisions/2026-08-07-pursue-layered]] terméktézisét ez **nem** dönti meg — a termék marad. Amit
megdönt, az a **megszólítás**: a listing címeket vevői kifejezésekre kell építeni (`bedroom wall
art`, `3d wall art`, `personalized wall art`), nem gyártóira, és a gyártói szavak csak másodlagos
kulcsszóként kerüljenek be.

Ez a rés nem a termékben van, hanem abban, hogy a mezőny rosszul címez.

## Nyitott feladat

A [[findings/listing-craft]] témalistáját (ember/portré 42%, mandala 40%, állat 29%, természet 17%,
vallási 12%, ünnep 11%) végig kell futtatni a Marketplace Insightson **vevői kifejezésekkel**, és
minden témára kiszámolni a keresés/találat arányt és a trend irányát.
