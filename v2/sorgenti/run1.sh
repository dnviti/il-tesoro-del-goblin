#!/bin/bash
# run1.sh label 'BALX' N players
BALX="$2" timeout 1500 node hsim.js ${3:-8000} ${4:-4} std expd.js > runs/$1.txt 2>&1
echo "== $1: $(grep -E '^CLS' runs/$1.txt) | $(grep -oE 'TIME [0-9]p: [0-9.]+ min' runs/$1.txt)"
