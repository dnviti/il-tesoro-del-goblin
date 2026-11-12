#!/bin/bash
# Misura l'altezza naturale di ogni blocco di testo e la salva in heights.json.
set -euo pipefail
SRC=$(cd "$(dirname "$0")" && pwd)
export WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
python3 "$SRC/genera.py" measure > "$WORK/script.txt"
designcraft-cli script "$WORK/script.txt" > "$WORK/out.json"
python3 - "$SRC" "$WORK" <<'PY'
import json, sys
src, work = sys.argv[1:]
r = json.load(open(f'{work}/out.json'))
lab = json.load(open(f'{work}/labels.json'))
ins = r['results'][-1]
b = {it['id']: it['bounds'] for sp in ins['spreads'] for it in sp['items']}
h = {k: round(b[r['results'][i]['id']][3] - b[r['results'][i]['id']][1] + 1, 1) for k, i in lab.items()}
json.dump(h, open(f'{src}/heights.json', 'w'), indent=0)
print(h)
print('overset:', [s.get('preview') for s in ins['stories'] if s.get('overset')])
PY
