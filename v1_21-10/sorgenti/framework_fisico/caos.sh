#!/bin/bash
# Espansione «Il Caos del Goblin · Le Crepe di MIMI» v2.0: regole definitive (21/10 sera)
# uso: N=30000 ./caos.sh etichetta   (2, 3 e 4 giocatori in parallelo; NPS="4" per uno solo)
cd "$(dirname "$0")"
cat phys.js caos_add.js > physC.js
J='{"trav":"twin","cob":true,"cards":"all","magoPag":1,"chiLan":"att","cobNoClue":1,"vento":99}'
OVL=physC.js ./tri.sh "${1:-caos}" '{}' CX="${CX:-$J}"
