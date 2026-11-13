#!/bin/bash
# Ritaglia le illustrazioni grezze alle misure dell'impaginato (immagini/png).
set -euo pipefail
SRC=$(cd "$(dirname "$0")" && pwd)
export WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
python3 "$SRC/genera.py" final > /dev/null
python3 - "$WORK" <<'PY'
import json, sys
work = sys.argv[1]
ill = json.load(open(f'{work}/ill_final.json'))
# fuoco del ritaglio (x, y da 0 a 1) e scontorno
focus = {'copertina': (0.5, 0.5, False), 'geronimo': (0.5, 0.5, True), 'carte': (0.5, 0.35, False),
         'morte': (0.5, 0.0, False), 'vittoria': (0.5, 0.0, False)}
json.dump({k: [v[0], v[1], *focus[k]] for k, v in ill.items()}, open(f'{work}/spec.json', 'w'))
PY
python3 "$SRC/prep_images.py" "$WORK/spec.json"
