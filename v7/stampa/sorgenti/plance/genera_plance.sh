#!/bin/bash
# Rigenera le 10 plance (una per carta Mappa) come SVG in questa cartella: base.svg (simulatore/mappa.py) e un SVG per
# ogni simulatore/plance/<tema>.py. Con le tessere illustrate (arte/png/PT-<TEMA>-<TERRENO>-1.png per gli 8 terreni
# + PS-<TEMA>.png) la plancia esce tematica (--tema), altrimenti piatta: quando arrivano le tessere di un tema basta
# rilanciare questo script. Tutte senza linee di strada (--senza-linee). Il kit le legge con build.sh / gen.py.
# uso: genera_plance.sh        (da qualsiasi cartella)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
V7="$HERE/../../.."
GEN="$V7/idee/genera_bozza_mappa.py"
ARTE="$HERE/../arte/png"
TERRENI="STRADA BOSCO CASE ROCCE ACQUA GUADO PARTENZA CRIPTA"
export PYTHONDONTWRITEBYTECODE=1

genera() {   # genera <nome file> <dati.py> <TEMA>
  local nome="$1" dati="$2" tema="$3" t ok=1 args
  args=(--dati "$dati" --out "$HERE/$nome.svg" --senza-linee)
  for t in $TERRENI; do [ -f "$ARTE/PT-$tema-$t-1.png" ] || ok=0; done
  [ -f "$ARTE/PS-$tema.png" ] || ok=0
  if [ $ok = 1 ]; then args+=(--tema "$tema"); echo "$nome: tematica ($tema)"; else echo "$nome: piatta (mancano tessere $tema)"; fi
  python3 "$GEN" "${args[@]}" >/dev/null
}

genera base "$V7/simulatore/mappa.py" BASE
for f in "$V7"/simulatore/plance/*.py; do
  nome="$(basename "$f" .py)"
  genera "$nome" "$f" "${nome^^}"
done
