#!/usr/bin/env bash
# Egyetlen ellenőrző parancs: `./check.sh`
#
# Miért van ez: 2026-08-14-én három egymást követő javítási kör mindegyike
# bevezetett egy új hibát, és mindet egy külső bíráló (codex) találta meg, nem
# a saját ellenőrzésem. Egy több perces Blender-render vagy egy LLM-bírálat
# nem helyettesíti azt, hogy néhány másodperc alatt megtudjam, elromlott-e a
# vágás-geometria.
#
# A sorrend szándékos: a lint fut előbb, mert az F821 (nem létező név) hibát
# már elkapta egy több perces futás ELŐTT.
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python

echo "== ruff =="
$PY -m ruff check product/ tests/

echo "== shell syntax =="
# Discover maintained *.sh files, including newly added/untracked files.
# Generated products, historical runs and research assets are outside scope.
# Materialize the list first so find failures cannot hide in process substitution.
shell_list=$(mktemp)
trap 'rm -f -- "$shell_list"' EXIT
printf '%s\0' ./*.sh > "$shell_list"
for directory in product/pipeline tests; do
  [[ -d "$directory" ]] || continue
  find "$directory" -type f -name '*.sh' -print0 >> "$shell_list"
done
while IFS= read -r -d '' script; do
  bash -n "$script"
done < "$shell_list"

echo "== pytest =="
$PY -m pytest

echo "== rendben =="
