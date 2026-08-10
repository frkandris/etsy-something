---
type: Decision
title: Ne mélységtérképet kérjünk a képmodelltől — lapos papercut illusztrációt, és a mélységet külön lépés adja
description: A felhasználó felvetette, hogy talán a képgenerátort kell irányba állítani, nem a poszterizálót csiszolni. A kutatás igazolta, és egy ennél erősebb tanulságot is hozott: a mélységet ne pixelenként, hanem színrégiónként kell értelmezni.
status: proposed
generated:
  by: claude-fable-5
  at: 2026-08-10T09:30:00Z
---

# A képgenerálás iránya

## Kontextus

A lánc első lépése ma: `gpt-image-2` **mélységtérképet** rajzol (szürkeárnyalatos, világos = közel),
és arra megy a poszterizálás. A felhasználó felvetése: lehet, hogy nem a poszterizálót kell tovább
csiszolni, hanem eleve olyan képet kérni, amit könnyű tiszta rétegekké alakítani.

## Amit a kutatás talált

**A felvetés igazolt: a generált mélységtérkép rossz alap.** Nem található dokumentált eset, ahol
generatív modellt sikeresen promptoltak volna használható mélységtérképre. A közösségi és a kutatói
konvenció egységesen **RGB kép → külön mélységbecslés**. Még a kifejezetten erre tanított
SD 1.5 LoRA leírása is megjegyzi, hogy a „világos = közel" konvenciót a modell nem követi
természetesen ([Civitai](https://civitai.com/models/392921/depth-map-lora-sd15),
[Maker Forums](https://forum.makerforums.info/t/create-depth-maps-from-ai-images-for-3d-laser-engraving-with-one-click/89392)).

**A nagyobb tanulság viszont nem a modellváltás, hanem egy algoritmikus lépés.** Az Adobe/Inria
*Illustrator's Depth* ([arXiv 2511.17454](https://arxiv.org/abs/2511.17454),
[repo](https://github.com/nissmar/illustrators_depth)) nem pixelenként poszterizál: **először
színrégiókra szegmentál, majd minden régiónak a mélység MEDIÁNJÁT adja**, és a rétegeket
alulra-befestéssel (inpaint) állítja elő. Így a beágyazás (nesting) a konstrukcióból következik, nem
utólagos kényszer — és a szilánk-/nyakproblémák nagy része eleve elő sem áll.

Rendezési konzisztencia illusztrációkon: Illustrator's Depth **0,987**, Depth Anything V2 **0,791**,
Depth Pro **0,636**.

## Döntés

Két lépésre bontva:

1. **A prompt vált most azonnal**: ne mélységtérképet kérjünk, hanem **lapos, kevés tónusú papercut
   illusztrációt**. A bevált szókincs a Fooocus papercraft stílusaiból jön
   ([sdxl_styles_twri.json](https://github.com/lllyasviel/Fooocus/blob/main/sdxl_styles/sdxl_styles_twri.json)):
   `3D papercut shadow box of {TÉMA} . layered, dimensional, depth, silhouette, shadow, papercut,
   handmade, high contrast`, negatívon `painting, drawing, photo, 2D, flat, high detail, blurry,
   noisy`. Tónusszám-fogáshoz: `three-tone`, `color block`, `clean shapes`, `isolated on a white
   background`, gradiens tiltva.
2. **A mélységet külön lépés adja**: `Depth Anything V2 **Small**` — és kizárólag a Small, mert a
   Base/Large/Giant **CC-BY-NC**, kereskedelmileg nem használható. A Small Apache-2.0, 24,8M
   paraméter, van Apple Core ML build (~50 MB), Apple Siliconon fut
   ([modellek](https://github.com/DepthAnything/Depth-Anything-V2),
   [Core ML](https://huggingface.co/apple/coreml-depth-anything-v2-small)).
   Fölé jön a **régió-medián** lépés az Illustrator's Depth ötlete alapján.

## Miért

A mostani lánc két nehéz dolgot kér egyszerre ugyanattól a modelltől: legyen szép kompozíció **és**
legyen metrikusan helyes mélységtérkép. A második az, amiben rossz. Szétválasztva mindkét lépés a
saját erősségén dolgozik, és a régió-medián azon a ponton avatkozik be, ahol a jelenlegi lánc a
legtöbb takarítást végzi.

## Amit NEM csinálunk, és miért

| ötlet | miért nem |
|---|---|
| **Illustrator's Depth** kódjának használata | **Adobe Research License — kizárólag nem-kereskedelmi kutatás.** Etsy-termékhez tilos. Az *ötlet* átvehető, a kód nem. |
| **LayerTracer** (arXiv 2502.01105) | a „réteg" nála rajzolási lépéssorozat lapos ikonokhoz, nem mélységi stack; ~50 GB merged modell |
| **ART** (Microsoft, 50+ átlátszó réteg) | a súlyokat 2025.07-ben **visszavonták** tanítóadat-eredet miatt |
| SVGDreamer / VectorFusion / NeuralSVG | SDS-optimalizáció, képenként percek, és lapos vektort ad |
| Recraft natív vektor API | lapos, kevés színű kimenetet ad, de **z-sorrendet nem** — a rétegezés így is ránk marad ($0,08/kép) |
| kész generátorok (atomm.com, myaiart.io) | az atomm az egyetlen valódi versenytárs („3-5 perfectly separated SVG layers", nincs API), de **nulla ellenőrizhető mintakimenet** |

## Nem ellenőrizhető

Az atomm.com kimeneti minősége és Etsy-licencfeltételei; az Illustrator's Depth checkpoint pontos
mérete.

## Mikor vizsgáljuk újra

Ha a lapos-illusztráció + Depth Anything V2 Small út mérhetően nem ad kevesebb takarítást, mint a
mostani mélységtérkép-út, akkor a régió-medián lépés önmagában is bevezethető a jelenlegi láncba.

## Provenancia

`product/pipeline/00_generate.py`, `product/pipeline/02_trace.py`. Kapcsolódik:
[[workflows/recessed-papercut-pipeline]], [[decisions/2026-08-10-cc0-eszkozok-a-hatterben]].
