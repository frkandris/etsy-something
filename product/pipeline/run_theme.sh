#!/bin/bash
# Egy tema teljes lancon valo atvitele. A melysegterkep mar sullyesztett.
set -e
cd "$(dirname "$0")/../.."
KEY="$1"; LEVELS="${2:-8}"
D=product/themes/$KEY
SRC=$(ls $D/raw_*.png | head -1)
.venv/bin/python product/pipeline/02_trace.py --src "$SRC" --levels $LEVELS \
  --min-part 500 --min-feature 6.0 --speckle 2.5 --margin 30 --punch 20 \
  --no-keyhole --full-panel --out $D/layers 2>&1 \
  | grep -v -E "Deprecat|px = list" | tail -14
blender -b -P product/render_blender.py -- $D/layers "$PWD/$D/plate.png" \
  plate well --frame --paper --recessed 2>&1 | grep -E "mu=|kesz|Error" | tail -2
.venv/bin/python product/pipeline/04_composite.py --bg product/pipeline/backdrops/warm-shelf.png \
  --art $D/plate.png --out $D/render_photo.png --cx 0.44 --base 0.94 --height 0.88 \
  --warm 1.02 --square 2>&1 | tail -1
