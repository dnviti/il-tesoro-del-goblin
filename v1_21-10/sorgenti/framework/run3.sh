#!/bin/bash
cd "$(dirname "$0")"
read np board <<< "$1"
BOARD=$board node hsim.js ${N:-40000} $np std phys.js | grep RES | sed "s/^RES /{\"np\":$np,/; s/^{\"np\":$np,{/{\"np\":$np,/"
