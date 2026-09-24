#!/usr/bin/env bash
# Explicit convenience wrapper; all geometry and rendering come from PROFILE.
# SOURCE/PROFILE paths are relative to the caller, as with run_product.py.
set -euo pipefail
if (( $# < 3 || $# > 4 )); then
  echo 'Usage: run_theme.sh THEME SOURCE PROFILE [LEVELS]' >&2
  exit 2
fi
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
KEY="$1"
if [[ ! "$KEY" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo 'THEME must contain only letters, digits, hyphens or underscores' >&2
  exit 2
fi
args=(--profile "$3" --src "$2" --out "$ROOT/product/themes/$KEY/current")
if [[ -n "${4:-}" ]]; then args+=(--levels "$4"); fi
exec "$ROOT/.venv/bin/python" "$ROOT/product/pipeline/run_product.py" "${args[@]}"
