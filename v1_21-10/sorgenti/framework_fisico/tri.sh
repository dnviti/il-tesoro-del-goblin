#!/bin/bash
# uso: N=20000 ./tri.sh label 'BALX' [env extra...]
cd "$(dirname "$0")"
L="$1"; B="${2:-{\}}"; N=${N:-20000}; shift 2
T='{"turno":25,"dado":6,"carta":35,"movimento":18,"casella":12,"scontro":20,"attacco":12,"livello":20,"sconfitta":40}'
for np in ${NPS:-2 3 4}; do (env FIS=1 BAGDRAW=1 TEMPOX="$T" BAG="${BAGJ:-{\"indizio\":0,\"vuota\":8\}}" BALX="$B" "$@" node hsim.js $N $np std ${OVL:-phys.js} | grep "RES\|CXSTAT" | sed "s/^RES /$L np$np /; s/^CXSTAT /$L np$np CX /" ) & done; wait
