---
type: Finding
title: Referencia szerinti termékiteráció és auditjavítás — 2026-09-05
description: Három ténylegesen renderelt új változat, szigorú exportellenőrzés és termékcsaládok szerinti katalógus.
status: draft
generated:
  by: codex
  at: 2026-09-05
sources:
  - resource: ../../product/catalog/index.html
  - resource: ../../product/catalog/magicvector-shepherd/runs/2026-09-05-v1/output/layers/report.json
  - resource: ../../product/catalog/recessed-papercut/runs/2026-09-05-v1/output/layers/report.json
  - resource: ../../product/catalog/marlaser-worldmap/runs/2026-09-05-v1/output/layers/report.json
  - url: https://www.etsy.com/au/listing/4328814517/german-shepherd-multilayer-svg-laser-cut
  - url: https://www.etsy.com/listing/1516752782/map-of-the-world-laser-cut-file-svg
---

# Elvégzett technikai javítások

A [[2026-09-05-project-audit]] után a csempézés már nem egyesít túl nagy vagy nem szomszédos darabokat. A fizikailag lehetetlen karos próbageometriát hibával utasítja el, nem vágási fájlnak álcázza. Külön próba ellenőrzi az anyagmegmaradást és az ágyméretet egy valóban csempézhető alakzaton.

Mindhárom exportág közös, zárolt és megszakítás után helyreállítható könyvtárcserét használ. Hibás térképgeometria nem kerül ki sikeres futásként. A kifejezett draft sosem release-ready. A könyvtárcsere továbbra sem atomikus olvasói pillanatkép; a két átnevezés között rövid rés van.

A `run_product.py` a profilból indítja a geometriát és a renderelést, ellenőrzi a visszatérési kódokat és a kimenetet, megőrzi a forrás hashét és a receptet. A `run_theme.sh` pipefail-t használ. A forrást/profilt tartalmazó kimeneti könyvtárat a runner elutasítja, nehogy a csere törölje a bemenetet. Verziózott Python-függőségek és GitHub Actions ellenőrzés kerültek a projektbe. A CI konfigurálva van; távoli Actions-futás nem történt ebben a munkamenetben.

Helyi ellenőrzés: **46 teszt sikeres**, Ruff sikeres, **13/13 beépített mutáció észlelt**. Ezek nem állítanak teljes geometriai lefedettséget. A tényleges új termékfutások riportját és renderét külön ellenőriztük.

# Vizuális eredmények

A [galéria](../../product/catalog/index.html) egymás mellé teszi a referenciát, a régi és az új pipeline-kimenetet. A két állatportré új raszteres bemenetét Imagegen készítette; a késztermékképek az exportált SVG-ből készültek Blenderben. A prompt és a bemenet a futás mappájában megmarad.

| Termék | Mért új kimenet | Látható javulás | Megmaradt különbség |
|---|---|---|---|
| Németjuhász | 7 réteg, 85 rétegdarab, 0 nyak, legrosszabb vékonyterület 1,75% | Irányított szőrmintázat, karakteresebb pofa, elkülönülő rétegpaletta | Referencia 8 réteg; sok külön ragasztás, túl világos orr |
| Macska | 6 kivágott panel + tömör hátlap, 11 rétegdarab + hátlap, 0 nyak, 0,03% | Több tér a keretben, tisztább szalagok, külön sötét hátlap | A szem környéke töredezett; a referencia szalagjai folytonosabbak |
| Egyrétegű térkép | 91 csempe, 113 felirat, 0 nyak, minden darab ≤330×280 mm | Egységes világos fa, renderben is látható határok, egy ország egy felirat, Antarktisz | Város- és óceánnevek, dekorációk és enteriőrfotó hiányoznak |

Az Antarktiszos térkép első 4 körös javítása 1 nyakat hagyott. Az új hibakapu ténylegesen megállította ezt az exportot. A 12 körig engedett helyi javítás után 0 nyak maradt; a minőségi küszöböt nem csökkentettük.

A geometriai siker nem fizikai tesztvágás és nem Etsy-konverziós mérés. A legfontosabb következő designfejlesztés az állatportrék szem/orr színének önálló kezelése és a rétegek összefüggőbb szerkesztése, nem további számozott variációk gyártása azonos bemenetből.

# Referenciák és nyitott korlátok

A MagicVectorLaser és MarLaserCut pontos listingjeinek képei vizuálisan hozzáférhetők voltak. A macskához a korábbi mentett képet használtuk, az eredeti pontos URL ismeretlen. A VyvaStudio 1794946470 listingjének aktuális képei nem voltak elérhetők; ennél nem állítunk új vizuális referenciaegyezést. A réteges térkép teljes újragenerálását a hosszú GEOS-bufferelésnél megszakítottuk; ehhez nem készült új, validált kiadás. A régi 0050 eredmény történeti, továbbra is hibás riportú fájl marad.

A `product/catalog/<forrástermék>/history/` hivatkozások a régi számozott mappákra mutatnak. Az új `runs/` tartalmazza a receptet, forrást, promptot és tényleges kimenetet. A korai, nem azonosított forrású kísérletek külön csoportban vannak; ezeket nem rendeltük találomra egy Etsy-termékhez.

# 2026-09-05 korrekció — macska v2 és review utáni ellenőrzések

A fenti táblázat a három v1 futás történeti állapota. A felhasználói vizuális ellenőrzés után kiderült, hogy a macska töredezett szeme pipeline-hiba, nem az új rajz hiányossága. A [[pitfalls/2026-09-05-recessed-layer-registration]] javítása után változatlan depth mapből készült v2: 6 egydarabos kivágott panel + hátlap, 0 nyak, 0,02% legrosszabb vékonyterület. A galéria most ezt mutatja a v1 mellé téve.

A kódreview-javítások után a gyors készlet 80 tesztje 2,35 másodperc alatt sikeres; ez felváltja az audit első körének 46 tesztes állapotát. A runner már a palettákat is másolja/hash-eli, a régi run_theme belépő explicit THEME SOURCE PROFILE [LEVELS] paramétereket kér. A témánkénti hardcode háttér/keret és 04_composite lépés helyét profilból választott Blender-nézetek vették át, render_photo.png nem készül. A három v1 futást az aktuális runnerrel újrageneráltuk, majd a macskához külön v2 készült; a manifestek gépi eredmények.
