# Egyrétegű világtérkép · 2026-09-05-v1

Referencia: [MarLaserCut, 1516752782](https://www.etsy.com/listing/1516752782/map-of-the-world-laser-cut-file-svg). A hero-, falon bemutatott és közeli képeket vizuálisan ellenőriztük; mentésük: `product/references/marlaser-worldmap/`.

A korábbi véletlenszerű sötét kontinensszínek helyett egységes, világos fa, visszafogott erezet és sötétebb gravír készült. Az országhatárok renderelt vonalszélessége most valóban látszik: csak a renderhez használt SVG tartalmaz kitöltött szalagokat, a gyártási karcolás továbbra is középvonal. A render-overlay egyszerűsítése 0,06 mm; a gyártási fájlt ez nem módosítja. Az ismételt országnevek helyett országonként csak a legnagyobb címkézhető töredék kap nevet.

A déli kivágás -80°-ig bővült: Antarktisz visszakerült. Ez Miller-vetítésű, szélesség szerint vágott térkép, nem a referencia illusztrációjának azonos másolata. A tábla névleges mérete **1325 × 772,8 mm**.

Mért eredmény: **85 földrajzi darab, 91 gyártási csempe, 15 ágyhoz igazított fájl, 113 országfelirat, 0 nyak**. A legnagyobb élű csempe 288,7 × 182,1 mm; minden csempe a 330 × 280 mm korláton belül marad. A 4 körös helyi javítás 1 gyenge nyakat hagyott: a szigorú export leállt. A 12 körig engedett javítás után a végső riport sikeres. A fizikai méretküszöb miatt 65 apró ország/terület nem kap külön alkatrészt; tételes listájuk a riportban van.

A referencia óceánnevei, városnevei, repülői és iránytűje még hiányoznak. A jelenlegi kép terméknézet, nem kész bútoros enteriőr. Ezek a következő külön tervezési feladatok; az országok kontrasztját vagy darabszámát önmagában növelve nem pótolhatók.

```sh
.venv/bin/python product/pipeline/run_product.py \
  --profile marlaser-worldmap --out product/builds/worldmap-reference-v1
```

[Termékkép](output/wall.png) · [Gyártási fájlok](output/layers/) · [Riport](output/layers/report.json) · [Recept](profile.json)
