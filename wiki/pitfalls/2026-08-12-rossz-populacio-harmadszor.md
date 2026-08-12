---
type: Pitfall
title: A hibás populációt használtam — harmadszor, ugyanabban a projektben
description: Az összehasonlításhoz a nem deduplikált 33-as layered listát vettem alapul, pedig a saját wikiben ott a pitfall, hogy az auditált populáció 21. A hiba 68%-kal lenyomta a layered mediánt, és megfordította a fő következtetést.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T20:00:00Z
---

# A hibás populációt használtam — harmadszor

## Tünet

A layered vs 3D összehasonlítás fő állítása ez volt: *„ugyanaz a pénz, egynyolcad annyi
listinggel"* — medián 420 ezer (layered) vs 489 ezer (3D) HUF/hó, vagyis a 3D **jobb**.

A codex-audit kiszúrta, hogy a layered oldalt a **hibás, nem deduplikált 33-as** listán számoltam.
Az auditált 21-es populáción a medián **706 907 HUF/hó** — **68%-kal magasabb**, és ezzel a 3D
oldal nem jobb, hanem **31%-kal alacsonyabb**.

## Gyökérok

**A wikiben ott volt.** A [[pitfalls/2026-08-08-wrong-unit-of-independence]] pontosan ezt írja le:
„specialista 65 → **35**, igazolt 33 → **21**". A [[findings/verified-shop-list]] tetején
figyelmeztető blokk áll ugyanerről. Én mégis a lista **törzséből** szedtem ki a boltneveket
regexszel, és nem néztem meg a figyelmeztetést a lista fölött.

Vagyis nem az adat hiányzott, és nem is a dokumentáció — **a saját dokumentációmat nem olvastam el
addig a mondatig, ameddig kellett volna**.

## Két további hiba ugyanebben a körben

- **Kevert percentilis-definíció.** A `p90/p10` arányt más képlettel számoltam, mint a táblában
  szereplő percentiliseket, ezért 14,2× és 27,1× jött ki 12,0× és 23,0× helyett. A közölt arányok
  **nem voltak reprodukálhatók a mellettük álló számokból** — ez önmagában is elég ok lett volna
  gyanút fogni.
- **„Egyötöd annyi idő alatt".** A boltok **korának** mediánját mértem, és időigénynek neveztem.
  Time-to-revenue mutatót az adat nem tartalmaz. Az állítást visszavontam.

## Alkalmazott korrekció

- Minden percentilis újraszámolva az **auditált 20 boltra** (a 21-ből egy nem adott mai adatot),
  egységes percentilis-definícióval.
- A hibás oszlop **benne maradt** a táblában, jelölve — hogy látszódjon, mekkora a különbség.
- A fő állítás átírva: nem „ugyanaz a pénz", hanem **kevesebb pénz, egytizednyi katalógussal**.

## Tanulság

**A pitfall-oldal megírása nem véd meg a hibától; a szűrő újrahasználata véd meg.** A helyes
populáció egy futtatható szkriptben állt elő (`assets/scripts/rebuild_corrected.py`), a hibás
viszont egy Markdown-táblában — és én a Markdownból szedtem ki regexszel, mert az volt kéznél.

Ellenőrizhető jövőbeli munkán: **ha egy populációnak van szkriptes definíciója, a nevek onnan
jöjjenek, ne egy findings-tábla törzséből.** Ha csak táblából tudsz dolgozni, olvasd el a tábla
fölötti bekezdést is — ebben a projektben ott áll a figyelmeztetés.

## Provenancia

[[findings/niche-comparison]], `wiki/assets/scripts/rebuild_corrected.py`. Kapcsolódik:
[[pitfalls/2026-08-08-wrong-unit-of-independence]], [[pitfalls/2026-08-07-duplicate-search-hits]].
