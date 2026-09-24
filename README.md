# etsy-something

Etsy-piackutatás és termék-pipeline egy digitális letölthető niche-hez.

**Három szál fut benne:**

- **Kutatás** — mért piaci adatok (kereslet, kínálat, bolt-bevételek) a layered/multilayer
  SVG niche-ről és a 3D-nyomtatás fájlpiacáról, első kézből származó Etsy-forrásokból.
- **Termék-pipeline** — generált és adatvezérelt rétegzett designok (papírvágás, lézervágás,
  világtérkép) vágásra kész SVG/DXF kimenettel és Blender-renderekkel (`product/`).
- **Tudásbázis** — minden következtetés populációval, fenntartásokkal és a mérési hibák
  postmortemjeivel együtt van rögzítve.

**Kezdd itt: [`wiki/index.md`](wiki/index.md)** — a tartalomtérkép, ahonnan minden elérhető.
A teljes kép egy oldalon: [`wiki/overview.md`](wiki/overview.md).

## Fejlesztői környezet

A tesztelt helyi környezet: Python 3.14.7, Blender 5.2.1 LTS, potrace 1.16.
A Blender és a potrace legyen a PATH-on; a CairoSVG-hez rendszer-Cairo szükséges.
macOS/Homebrew: `brew install python@3.14 potrace cairo` és Blender telepítése.

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
./check.sh
```

A `requirements.lock` a működő core + tesztkörnyezet rögzített függőségeit tartalmazza.
A fotóból becsült mélység opcionális függőségei: `requirements-ml.txt`.
A GitHub Actions ugyanezt az ellenőrzést futtatja Linuxon; a Blender-vizuális QA helyi.

## Egy termék előállítása

```sh
.venv/bin/python product/pipeline/run_product.py \
  --profile relief-portrait --src product/themes/german-shepherd/src_relief2.png \
  --out product/builds/shepherd
```

A profil vezérli a geometriát és a renderelést. `--no-render`: csak SVG/DXF;
`--views plate,macro`: kiválasztott nézetek; `--draft`: kifejezetten jelölt piszkozat.
Az eredmény tartalmazza a receptet, a forrás SHA-256 azonosítóját és a validációs riportot.
Sikertelen futáskor a korábbi teljes kimenet megmarad. A könyvtárcsere megszakítás után
helyreállítható, párhuzamos írók ellen zárolt; nem atomikus olvasói pillanatkép.

## Referencia szerinti iterációk

[Összehasonlító galéria](product/catalog/index.html) · [Termékcsaládok és receptek](product/catalog/README.md).
Az új futások a `product/catalog/<forrástermék>/runs/` alatt élnek. A `history/` hivatkozásai a régi számozott iterációkra mutatnak.

A `--profile magicvector-shepherd` vagy `--profile recessed-papercut` a katalógus legújabb mentett receptjét választja. A generikus profilnevek feloldása is támogatott; ez önmagában nem igazolja a recept kimenetét. A `worldmap` / `vyva-worldmap` kísérleti: nincs lezárt, validált teljes futása, a geometriai ellenőrzés leállíthatja.

## Engineering ellenőrzés

A `./check.sh` a lintet, a shell-szintaxist és a gyors viselkedési teszteket futtatja.
A `.venv/bin/python tests/mutation_check.py` külön, ideiglenes másolatban ellenőrzi a geometriai tesztek hibaérzékenységét; az élő forrást nem módosítja.
A runner a bemeneti rajz másolatát is megőrzi az `inputs/` alatt, és a hash ebből készül. Hibás profil, ismeretlen nézet vagy ellentmondásos riport nem kerül ki sikeres kiadásként.

[Alkalmazott Fowler- és Google-gyakorlatok](wiki/workflows/engineering-quality.md). A független Claude-review eredményei a `reviews/` alatt találhatók.

### Igazolt receptek és a régi shell-belépési pont

Tényleges SVG/DXF- és Blender-futással ellenőrzött: `magicvector-shepherd`, `recessed-papercut`, `marlaser-worldmap`. A generikus `worldmap-flat` ugyanezt a validált térképreceptet tartalmazza. A `papercut` és `relief-portrait` általános kiindulási profil; az új forrásrajz saját validációt igényel.

A wrapper új hívása: `run_theme.sh THEME SOURCE PROFILE [LEVELS]`. Nincs automatikus választás a több `raw_*.png` közül. Példa a repó gyökeréből:

```sh
./product/pipeline/run_theme.sh german-shepherd \
  product/catalog/magicvector-shepherd/runs/2026-09-05-v1/source.png magicvector-shepherd
```

A régi, témánként hardcode-olt háttér/keretválasztás és a `04_composite.py` lépés kikerült ebből a wrapperből; `render_photo.png` nem készül. A profil választja a Blender-nézeteket és a keretet, a kimenet `product/themes/THEME/current/`. Külön kompozit készítése továbbra is külön művelet.

A forráskép mellett a trace- és renderpaletták is az `inputs/` alá kerülnek, hash-sel. A kiadott profil és a manifest parancsai ezekre a megőrzött fájlokra mutatnak. A célkönyvtárba eső eredeti palettát a runner is elutasítja. Zárak a rendszer ideiglenes mappájában vannak, nem a termékben; ugyanarra a célra futó második export azonnal beszédes hibát kap.

A 2026-09-16-i célzott engineering-javítások ellenőrzése: [naplók és változások](reviews/2026-09-16/README.md). A `check.sh` a gyökér, a `product/pipeline/` és a `tests/` shell-szkriptjeit is felderíti.
