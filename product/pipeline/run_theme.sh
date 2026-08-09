#!/bin/bash
# Egy tema teljes lancon valo atvitele: trace -> plate render -> foto-kompozit.
# A melysegterkep mar sullyesztett (a generator --recessed modjaval keszult),
# ezert a trace-nek NEM kell invertalnia.
set -e
cd "$(dirname "$0")/../.."
KEY="$1"; LEVELS="${2:-7}"
D=product/themes/$KEY
SRC=$(ls $D/raw_*.png | head -1)
.venv/bin/python product/pipeline/02_trace.py --src "$SRC" --levels $LEVELS \
  --min-part 400 --min-feature 4.0 --no-keyhole --full-panel --out $D/layers 2>&1 \
  | grep -v -E "Deprecat|px = list" | tail -12
blender -b -P product/render_blender.py -- $D/layers "$PWD/$D/plate.png" \
  plate well --frame --paper --recessed 2>&1 | grep -E "mu=|kesz|Error" | tail -2
.venv/bin/python product/pipeline/04_composite.py --bg product/pipeline/backdrops/warm-shelf.png \
  --art $D/plate.png --out $D/render_photo.png --cx 0.44 --base 0.94 --height 0.88 \
  --warm 1.02 --square 2>&1 | tail -1
