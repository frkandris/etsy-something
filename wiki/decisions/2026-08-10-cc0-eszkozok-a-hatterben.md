---
type: Decision
title: A háttér CC0 3D eszközökből épül, nem saját geometriából és nem lapos fotóból
description: A felhasználó diagnózisa két rossz opciót nevezett meg — a számolt geometria helyőrzőnek látszik, a lapos fotó nem mozog. A Poly Haven CC0 modelljei és HDRI-jei mindkettőt megoldják, mert valódi mélységben álló geometriák.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-10T09:00:00Z
---

# A háttér CC0 3D eszközökből épül

## Kontextus

A termékfotó háttere két úton készült, és a felhasználó mindkettőt elutasította — helyesen:

1. **Saját geometria** (henger = váza, gömb = növény): „a számolt dolgok rondák". Bármilyen
   megvilágítás mellett helyőrzőnek látszik.
2. **Lapos generált fotó, amire kompozitálom a keretet**: „a flat kép meg nem mozog (pl. a videók
   használhatatlanok emiatt, mert csak a keret mozgott, a háttér fixen állt)".

A második a súlyosabb: egy 6 másodperces körbefordulásban a keret elfordul, a szoba viszont
oda van szögezve. Ez azonnal leleplezi a kompozitot.

## Mérlegelt opciók

| opció | miért esett ki |
|---|---|
| jobb saját geometria | ugyanaz a fal — a nem-fotorealisztikus prop nem lesz jobb több élsimítástól |
| több generált háttér, kockánként más | a modell nem tartja a konzisztenciát két kocka között; villog |
| parallax a lapos fotó megcsúsztatásával | 2,5D csalás, a props egymáshoz képest nem mozdul |
| **CC0 3D eszközök + HDRI** | **ez lett** |

## Döntés

A `styled` nézet valódi geometriát épít: [Poly Haven](https://polyhaven.com/license) CC0 modelleket
appendel (`bpy.ops.wm.append` az eszköz nevű kollekcióra), asztallapra rendezi őket eltérő
mélységben, és egy belteri HDRI-t tesz a világ háttérébe — az egyszerre világít és tölti ki a
hátteret.

Letöltő: `product/pipeline/assets.py`. A Poly Haven API kulcs nélküli, de **egyedi `User-Agent`
fejlécet kötelezővé tesz**. Készlet: cserepes növény, antik kerámia váza, enciklopédia-sor, fa
gyertyatartó, fonott kosár, sárgaréz váza; HDRI: `lythwood_lounge`, `fireplace`,
`anniversary_lounge`. Együtt 138 MB, `product/pipeline/assets/` alatt, gitignore-olva; a forrás és a
licenc a `MANIFEST.json`-ban.

## Miért

- **Parallax.** A propok saját mélységben állnak, ezért körbefordulásnál helyesen mozdulnak
  egymáshoz képest. Ezt semmilyen lapos háttér nem tudja utánozni.
- **A HDRI kettőt csinál egyszerre.** Világít *és* háttér — nincs külön háttérkép, amit a
  világításhoz kellene hangolni, és a nézettel együtt forog.
- **CC0.** Kereskedelmi felhasználás, attribúció nélkül. Etsy-terméknél ez nem mellékes.

## Következmények

- A `04_composite.py` kompozit útja **nem tűnik el**, de a `styled` nézet mellett másodlagos lett.
- A kamerát nem kézzel megadott dőlésszög állítja, hanem a **műtárgy középpontjára irányul**
  (`atan2(D, camz - TGT)`). Fix dőlésszögnél a kép fele csupasz asztallap lett; irányítással a zoom
  szabad paraméter marad (`--scene-zoom`, alapérték 1,30).
- Az asztallap a kamerán **túlnyúlik**, mert a látható elülső éle egy világos, üres sávot csinált a
  kép alsó harmadából.

## Mikor vizsgáljuk újra

Ha a Poly Haven készlet szűknek bizonyul (több téma, több enteriőr-hangulat) — akkor bővítés
ugyanezzel a letöltővel, nem irányváltás.

## Provenancia

`product/pipeline/assets.py`, `product/render_blender.py` (`styled` nézet). Kapcsolódik:
[[workflows/recessed-papercut-pipeline]], [[decisions/2026-08-10-keprogeneralas-iranya]].
