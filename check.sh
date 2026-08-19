#!/usr/bin/env bash
# Egyetlen ellenőrző parancs: `./check.sh`
#
# Miért van ez: 2026-08-14-én három egymást követő javítási kör mindegyike
# bevezetett egy új hibát, és mindet egy külső bíráló (codex) találta meg, nem
# a saját ellenőrzésem. Egy több perces Blender-render vagy egy LLM-bírálat
# nem helyettesíti azt, hogy fél másodperc alatt megtudjam, elromlott-e a
# vágás-geometria.
#
# A sorrend szándékos: a lint fut előbb, mert az F821 (nem létező név) hibát
# már elkapta egy több perces futás ELŐTT.
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python

echo "== ruff =="
$PY -m ruff check product/ tests/

echo "== pytest =="
$PY -m pytest

echo "== rendben =="
