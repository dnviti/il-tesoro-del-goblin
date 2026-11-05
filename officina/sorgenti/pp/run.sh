#!/bin/bash
# misura il listino PP sul gioco v2: pp/<nome>.json
cd "$(dirname "$0")/.."
N=${1:-8000}
while IFS='|' read -r name when eff; do
  echo "{\"cmd\":\"card\",\"n\":$N,\"caos\":false,\"card\":{\"nome\":\"$name\",\"kind\":\"incantesimo\",\"when\":\"$when\",\"req\":\"\",\"effects\":$eff,\"pp\":4}}" > pp/$name.msg
done < pp/list.txt
ls pp/*.msg | xargs -P 4 -I{} sh -c 'node wrun.js "$(cat {})" > {}.out 2>&1'
