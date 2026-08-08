# 0006 — ellenőrzött kelta életfa (codex 2. kör után)

A 0005 forrása, a 2. kör 5 új findingja utáni lánccal:
- nyak-detektor fragmentküszöb 100→20 mm² (MIN_FRAG) — a kis végtag egy hajszálhídon most már hiba
- a gyógyítás nem ragaszthat össze két külön darabot (no-fuse szabály), buffer 1,8→1,2 mm
- rövid nyakra lencse-fallback; gyógyíthatatlan nyaknál (mögöttes lyuk) a kis végtag amputálva —
  a folt a mögöttes lapon marad, mint minden demóciónál
- a mm-skála a hátlap sziluettjéből jön MÁR a clean() előtt (pre-pass trace)
- keskeny rések (pl. 10×0,3 mm) túlélik a thicken-zárást (előre kigyűjtve, utólag visszavágva)
- demóció-audit: kiírja, mennyi terület esik egynél több lappal hátrébb
- hibás biztonsági riport → nincs fájl-export (--draft felülbírálja); a stale fájlok törlése
  csak sikeres build után
- kulcslyuk: centroid-központú szkennelés, kihagyás = hiba (--no-keyhole a tudatos elhagyás)

Riport: 1/1/1/1/1/5 darab, 0 nyak, leggyengébb 7,23 mm, vékony ≤0,97%, 1 amputáció a 3. rétegen.
