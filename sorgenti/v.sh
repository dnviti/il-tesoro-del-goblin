#!/bin/bash
# usage: v.sh label 'BALX json' N players [evalfile]
BALX="$2" node hsim.x.js $3 $4 std ${5:-exp.js} > runs/v_$1.txt 2>&1
