#!/bin/bash
# Ten variants of one subject, all the way to a stacked preview, so the choice
# is made on what the piece will actually look like rather than on a prompt.
# Serve them with:  python -m http.server --directory <outdir>
set -u
cd "$(dirname "$0")/../.."
SUBJECTS_FILE="$1"; OUT="$2"; N="${3:-10}"; REF="${4:-}"
mkdir -p "$OUT"
for i in $(seq 1 "$N"); do
  D="$OUT/v$(printf %02d "$i")"
  mkdir -p "$D"
  [ -f "$D/preview_stacked.png" ] && { echo "v$i mar kesz"; continue; }
  SUBJECT=$(sed -n "${i}p" "$SUBJECTS_FILE")
  [ -f "$D/raw_v_0.png" ] || .venv/bin/python product/pipeline/00_generate.py --subject-text "$SUBJECT" \
      --name v --flat --levels 7 --size 1024x1024 --out "$D" \
      ${REF:+--ref "$REF"} >/dev/null 2>&1
  [ -f "$D/raw_v_0.png" ] || { echo "v$i generalas HIBA"; continue; }
  [ -f "$D/depth_map.png" ] || .venv/bin/python product/pipeline/01b_depth.py \
      --art "$D/raw_v_0.png" --out "$D/depth_map.png" --levels 7 >/dev/null 2>&1
  [ -f "$D/depth_map.png" ] || { echo "v$i melyseg HIBA"; continue; }
  .venv/bin/python product/pipeline/02_trace.py --src "$D/depth_map.png" --levels 7 \
      --min-part 60 --merge-below 0.005 --margin 8 --no-keyhole --full-panel --connected \
      --palette "$D/palette_full.json" --out "$D/layers" >"$D/trace.log" 2>&1 \
    || { echo "v$i trace HIBA (lasd $D/trace.log)"; continue; }
  blender -b -P product/render_blender.py -- "$D/layers" "$PWD/$D/plate.png" plate \
      --frame --paper --recessed --palette-file "$D/layers/palette.json" >/dev/null 2>&1
  echo "v$i kesz"
done
