---
type: Workflow
title: Mérhető kódminőség és független review
description: A Fowler- és Google-gyakorlatok alkalmazása a helyi termék-pipeline-ra.
status: stable
generated:
  by: codex
  at: 2026-09-05
sources:
  - url: https://martinfowler.com/bliki/SelfTestingCode.html
  - url: https://martinfowler.com/articles/practical-test-pyramid.html
  - url: https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - url: https://google.github.io/eng-practices/review/reviewer/standard.html
---

# Alkalmazott gyakorlatok

Fowler [Self Testing Code](https://martinfowler.com/bliki/SelfTestingCode.html) elve alapján a gyors ellenőrzés egy paranccsal fut: `./check.sh`. Lint, shell-szintaxis és viselkedést ellenőrző tesztek alkotják. A [tesztpiramis](https://martinfowler.com/articles/practical-test-pyramid.html) alapján a geometria sok olcsó egységtesztet kap, a publikálási lánc a külső folyamat határán helyettesített teszteket, a valódi SVG/DXF-export pedig kis offline integrációs próbát. A Blender-vizuális ellenőrzés külön, tényleges renderrel történik.

A [Google review-szempontjai](https://google.github.io/eng-practices/review/reviewer/looking-for.html) közül a működés, a párhuzamos futások, a komplexitás, a tesztek érdemi védelme és a dokumentáció a releváns ellenőrzési pontok. Ezért a runner profilbetöltése, riportellenőrzése és termékfuttatása külön függvény; a hibás profil, nézet és státusz már az adott határon hibát ad. A CLI által kezelt kimenetet és draft-módot a recept nem írhatja felül.

A bemenet másolata és a hash ugyanazokra a bájtokra vonatkozik. A termék teljes könyvtára csak sikeres generálás, validáció és render után cserélődik. A hibatesztek megvizsgálják, hogy a korábbi kiadás ténylegesen megmarad-e, és elindul-e tévesen a következő lépés.

A mutációs ellenőrzés (`.venv/bin/python tests/mutation_check.py`) előbb a változatlan alaptesztet futtatja, majd **ideiglenes másolatot** módosít. Az élő `cutlib.py`-t nem írja át; megszakítás vagy párhuzamos fejlesztés így nem hagy szándékosan elrontott kódot a munkakönyvtárban. Pytest-setup/collection hiba nem számít észlelt mutációnak.

# Review és lezárás

A Claude-review külön, csak olvasó Claude Code-folyamat. A forráskódot és a módosításokat kapja meg, az eredeti bírálatok a `reviews/` alatt maradnak. A javítható és reprodukálható megállapítások után ismét teszt és új review következik. A [Google review-standardja](https://google.github.io/eng-practices/review/reviewer/standard.html) szerint a mérce a kód egészségének javulása és a technikai bizonyíték; az ízlésbeli megjegyzések külön szerepelnek.

Zöld állapotot csak a tényleges tesztkimenet és a független reviewer lezárt megállapításai igazolnak. Ez a vizsgált változáscsomagra vonatkozik, nem a teljes kódbázis bizonyított hibamentességére, fizikai tesztvágásra vagy távoli CI-futásra.

A paletták is bemenetek: a runner a trace `--palette` és render `palette_file` fájljait külön snapshotként megőrzi és hash-eli. A zárolás felhasználónkénti privát temp könyvtárban él, nem a termékcsomagban; azonos célra indított második folyamat azonnal érthető hibát kap. A konkurenciateszt valódi gyermekfolyamattal ellenőrzi ezt. A trace és térkép közös geometriai mérőfüggvényeket használ, hogy a javítások ne csak az egyik másolatba kerüljenek.

A képjavítás konkrét példája: [[pitfalls/2026-09-05-recessed-layer-registration]]. A regressziós teszt a legalsó lap kivágását és a végső SVG-ben megmaradó keskeny nyílást is vizsgálja; a mechanikai zöld riport önmagában nem védi a macska felismerhetőségét.

2026-09-05 lezárás: 80 sikeres helyi teszt, tiszta környezetben is sikeres ellenőrzés, 13/13 észlelt mutáció; a Claude második review-ja APPROVE, minden első körös finding resolved. A nem blokkoló megjegyzések és a review korlátai megmaradnak a [jegyzőkönyvben](../../reviews/README.md). Távoli CI és fizikai tesztvágás nem történt.

## 2026-09-16 — célzott folytatás

Fowler [Self Testing Code](https://martinfowler.com/bliki/SelfTestingCode.html) és a Google [review-szempontjai](https://google.github.io/eng-practices/review/reviewer/looking-for.html), valamint [kis változáscsomagokra vonatkozó útmutatója](https://google.github.io/eng-practices/review/developer/small-cls.html) alapján a korábbi review négy konkrét megjegyzését dolgoztuk fel:

| Elv | Megvalósítás | Bizonyíték |
|---|---|---|
| Viselkedést védő tesztek, hiba reprodukálása | Átirányított/megosztott zárfájl, új shellfájl, üres geometria vizsgálata | Az új készlet a korábbi kódon 11 esetben elbukik; FIFO-esetre korlátos gyermekfolyamat akadályozza meg a teszt beragadását. |
| Kis, érthető felelősségek | A célkönyvtár zárolása külön context manager; a helyreállítás és publikálás változatlan | Meglévő konkurencia- és visszaállítási tesztek sikeresek. |
| Határok ellenőrzése | A megnyitott lock könyvtár tulajdonosa/jogosultsága, a relatívan megnyitott zárfájl típusa/tulajdonosa/linkszáma ellenőrzött; symlink nem követhető | Hat hibás fájlrendszer-eset, meglévő export megőrzése, régi 0644 lockkal kompatibilitás. |
| Világos függvényszerződés | Az egycellás `tile_piece` megőrzi a területküszöböt elérő darabokat; vastagságukat a hívó release gate-je ellenőrzi | Külön szerződésteszt és meglévő flat-map végponti elutasítási teszt. |
| Folyamatosan használható ellenőrzés | A `check.sh` a gyökér `.sh` fájljait, valamint a `product/pipeline` és `tests` alatti shellfájlokat automatikusan ellenőrzi | Új, még nem trackelt, szóközös nevű és almappás fájlokat is vizsgáló tesztek. |

A 2026-09-16-i teljes helyi készlet: **97 sikeres teszt 4,29 s alatt**, Ruff és shell-szintaxis sikeres; **13/13 mutáció észlelt**. [Naplók és az aznapi kódeltérés](../../reviews/2026-09-16/README.md). A korábbi 80 tesztes eredmény történeti adat marad.

A lock fájlokat futó exportok mellett nem szabad törölni: az azonos útvonalon létrehozott új inode megkerülhetné a meglévő zárolást. A megoldás a projekt meglévő macOS/Linux (POSIX) célkörnyezetét használja. A generált termékeket és a `wiki/assets` kutatási forrásokat nem szerkeszti ez a karbantartási kör.

Ugyanebben a körben a review utáni kiegészítés a shell-felderítés hibakódját is ellenőrzi: a fájllista előállítása külön, hibára megálló lépés. A köztes 96 tesztes állapothoz képest egy új regresszió került be; a korábbi folyamathelyettesítés elnyelte a szimulált `find` 7-es hibakódját. [Piros kontroll](../../reviews/2026-09-16/discovery-red.log).

2026-09-16 végső ellenőrzés: a második célzott Claude-review APPROVE, üres findings lista; kisebb nem blokkoló tisztázási megjegyzésekkel. A vizsgált források hash-e a lezáráskor egyezett.

## 2026-09-24 — egyszerűsítés és kódátnézés

Az átnézés kódolvasással és célzott futtatással dolgozott, nem további védőrétegekkel. Két súlyos
hibát talált, amelyeket a zöld készlet nem fogott meg. A részletek a
[[pitfalls/2026-09-24-dxf-fejjel-lefele]] oldalon vannak.

| változás | miért |
|---|---|
| DXF-tájolás javítva a trace- és mindkét térkép-láncban, 3 aszimmetrikus regressziós teszttel | minden DXF az SVG függőleges tükörképe volt |
| 9 hatástalan kapcsoló törölve a `02_trace.py`-ból (1202 → 982 sor) | egyik profil sem használta, és 4 közülük csendben semmit nem csinált |
| Az exportzár egyetlen `flock` (~35 → ~10 sor), a `check.sh` shell-felderítése `git ls-files` | FIFO-, linkszám- és tulajdonos-ellenőrzés egy egyfelhasználós helyi eszközben felesleges teher |
| 16 teszt törölve (zárfájl-jogosultság 7, a `check.sh` saját felderítése 9) | a törölt implementációs részleteket tesztelték, nem a termék viselkedését |
| Renderer: ismeretlen palettanév esetén nem száll el, az exploded nézet halott objektív-sora törölve | a `PALETTE` név a fallback után is a hibás érték maradt, és a `KeyError` a hátlapnál jött. Az exploded kamerát mindig 85 mm-re írta felül a közös ág |
| `gen_candidates.sh` törölve | egyszeri futás rekordja volt, és egy másik session scratchpadjéből olvasta az API-kulcsot |

**Igazolás:** 83 teszt sikeres, 12/12 mutáció elbukik. A mentett receptek újrafuttatása után 94
kimeneti fájlból csak a 29 DXF változott; az SVG-k, a paletták és a riportok bájtra azonosak.

**Nyitott, igazolt megállapítások (nem javítva):**

- `shelf` nézet kerettel: a keret és a hátlap laposan fekszik a felállított mű előtt. Egyik profil
  sem használja ezt a nézetet.
- `styled` + `room: sideboard` (a `worldmap` profil): a földsík eltakarja a komód elejét.
- A renderer több hibaága 0-s kóddal lép ki: hiányzó kellék, hiányzó HDRI, ismeretlen `room`,
  `props` vagy `explode` érték, hiányzó `engrave_labels.svg`.
- `02_trace.py`: a `max_parts`-szerű rétegtörlés után az `enforce_nesting` a `k-1`. réteget keresi,
  és ha az törlődött, nem klippel. Hibás geometriát ezzel eddig nem mértünk.
- Duplikáció: a `10_worldmap.py` a `geolib` másolatát tartalmazza, a három DXF/SVG-író külön él,
  a `render_blender.py`-ban a kamera- és „felállítás”-kód 4–7 példányban szerepel.

A `11_worldmap_flat.py` riportja `all_ok` mellett is felsorol kimaradt országokat. Ez szándékos: a
`--hard-floor` alatti darab fizikailag vághatatlan, és a riport név szerint felsorolja.
