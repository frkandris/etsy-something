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
# Every tracked or new (not ignored) *.sh file. The assignment keeps git's exit
# status, so a failed listing stops the check instead of checking nothing.
shell_files=$(git ls-files -co --exclude-standard -- '*.sh')
while IFS= read -r script; do
  if [[ -n "$script" ]]; then bash -n "$script"; fi
done <<< "$shell_files"

echo "== pytest =="
$PY -m pytest

echo "== rendben =="
