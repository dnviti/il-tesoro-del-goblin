#!/bin/bash
# runv.sh label 'BALX' N  → 2,3,4 giocatori in parallelo
L=$1; X=$2; N=${3:-3000}
for n in 2 3 4; do BALX="$X" timeout 900 node hsim.js $N $n std expd.js > runs/${L}_$n.txt 2>&1 & done; wait
for n in 2 3 4; do echo "== $L ${n}p"; grep -E "CLS|TIME [0-9]|COUNTS|errors" runs/${L}_$n.txt | sed 's/"parts.*//' ; done
