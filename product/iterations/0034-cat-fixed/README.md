# 0034 — süllyesztett szerkezet, a codex KRITIKUS hibája után

## Amit a codex talált

**KRITIKUS:** a `--full-panel` a `panel − layer1` régiót adta hozzá minden laphoz, csakhogy ez
**a belső lyukakat is tartalmazza** — visszauniózva az 1. réteg tömör lett, nulla nyílással
(a 0032 riportja ezt igazolta: 0 lyuk, míg a 0031-ben 21). Javítva: csak a design KÜLSŐ
kontúrján (a részek `exterior` gyűrűjén) kívüli mező kerül hozzá. A 0034-ben az 1. rétegnek
újra 8 nyílása van.

**MAGAS:** a `--recessed` a renderben megfordította a z-sorrendet, holott a mélységtérkép már a
GENERÁLÁSNÁL süllyesztett — dupla fordítás lett belőle, és a tömör padló került előre, letakarva
mindent (a 0033 első rendere egy fekete négyzet volt). A kapcsoló most csak a keret-geometriát
vezérli.

**MAGAS:** az invertálás az indexkép-normalizálás ELŐTT futott. Egy 0..6 indexkép invertálva
249..255 lesz, `hi=255`, ezért a normalizáló ág nem indul el, és a k-means egyetlen klasztert
lát. Most előbb normalizál, aztán invertál.

**MAGAS:** az alapprompt „pure black background" és „outside the circular piece" szabályai
közvetlenül cáfolták a süllyesztett blokk teljes világos lapját — és a modell az alapprompnak
engedelmeskedett. Recessed módban ezek most kikerülnek a promptból.

## Reviewer visszajelzése (66/100, −2 az előzőhöz képest)

A felső lap zsugorodott lebegő táblává; ezért `--recessed` mellett a lánc már NEM kicsinyíti a
művet a keretnyílásban, a keret ajka a laphoz simul, és a `well` paletta a megadott hexekre állt
(#2E2622 → #F7F5F1) 18%-nál nagyobb luminancia-lépcsőkkel. Új `--min-feature` kapcsoló: a
referencia formanyelve durvább, mint a 2 mm-es vágási határ, ezért 7 mm alatti nyúlványt levág.

Riport: 6 réteg, 0 nyak, leggyengébb 10,42 mm, vékony terület 0,00% minden rétegen.
