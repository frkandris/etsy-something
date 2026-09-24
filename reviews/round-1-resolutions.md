# Claude round 1 — javítások

A `claude-round-1-findings.json` REQUEST_CHANGES eredményének feloldásai, ellenőrzendő állítások a második kör számára.

| Finding | Javítás / bizonyíték |
|---|---|
| F1 | check.sh fájlonként bash -n; test_shell_entrypoints szándékosan hibás második shellfájllal. |
| F2 | run_theme.sh THEME SOURCE PROFILE [LEVELS], explicit választás; README és workflow dokumentálja a régi hardcode háttér/keret/composite eltávolítását. |
| F3 | Felhasználónkénti privát temp lock könyvtár, hash alapú nevek; nincs lock a payloadban. Régi katalógus lockok eltávolítva. |
| F4 | Mindhárom v1 katalógusfutás újrafuttatva az új runnerrel (trace/map + Blender), inputs snapshot és render_commands gépi manifest. A macska ezt követően v2-ben kapott geometriai javítást; v1 történeti, hibás vizuális baseline. |
| F5 | Trace és render paletták másolva/hash-elve, output/input ütközés elutasítva; snapshot teszt az eredeti paletta módosításával és törlésével. |
| F6 | trace a cutlib polys/widest_inscribed/necks függvényeit használja; specializált heal_necks megmaradt. Vegyes/nested GeometryCollection teszt. |
| F7 | worldmap explicit experimental, worldmap-flat a validált recepttel egyezik; README megkülönbözteti a validált családokat a kiinduló receptektől. |
| F8 | Mindkét térkép a végleges kimeneti útvonalat írja a tranzakció után. |
| F9 | Nem blokkoló flock célzott hibával; valódi gyermekfolyamatos konkurencia-teszt. |
| F10 | Friss stagingből törlő holt ágak megszűntek. |
| F11 | Katalógus latest_run nélkül a deklarált profile-ra esik vissza, recept nélkül célzott hiba. |

N1–N10: közös require_valid; palette_src név; üres tiled célzott hiba; mutációs kerethiba külön kezelve; top-level importok; gyors készlet mért 2,35 s/80 teszt; relief profil note javítva; render parancsok mentve; argparse rövidítések tiltva; workflow frissítve.

Két további, tényleges hibából származó változás:

- `11_worldmap_flat.py`: a teljesen vékony szigetnek nincs neck-je; a végső gate most a legszélesebb beírt kört is méri. `test_flat_map_export.py` 100×1 mm-es valós generátorfutása a javítás előtt átment, utána megállítja a hibás exportot és megőrzi a régit. A 91 darabos valós map újravalidálása: weakest 2,904 mm, a vágófájlok az előző eredménnyel azonosak (`map-revalidation.json`).
- `02_trace.py`: a margóillesztés csak a felső lapok relatív nyílásait mozgatta, a legalsó nyílásokat helyben hagyta. `fit_panel_openings` a teljes panelhez képest minden lap nyílásait ugyanúgy mozgatja. A keretszél zárása csak a varrat közelében ad anyagot; a margó hozzáadása nem zárja a belső dekoratív nyílásokat. Két numerikus illesztésteszt és a valódi SVG/DXF integrációs tesztben vékony dekoratív nyílás védi. A változatlan cat depth mapből készült v2 plate/styled render vizuálisan ellenőrizve, report all_ok, 6 egydarabos panel + hátlap.

A kódreview nem helyettesíti a fizikai tesztvágást vagy a képek vizuális értékelését. A check.log a helyben futtatott ellenőrzést rögzíti.
