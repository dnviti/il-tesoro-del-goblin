#!/bin/bash
cd "$(dirname "$0")"
read np when eff cls0 <<< "$1"
EFF=$eff WHEN=$when CLS0=$cls0 node hsim.js ${N:-40000} $np std phys.js | grep RES | sed "s/^RES /{\"np\":$np,/; s/^{\"np\":$np,{/{\"np\":$np,/"
