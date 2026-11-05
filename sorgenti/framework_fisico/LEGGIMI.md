# phys.js esteso (thread «Gioco fisico», 21/10/2026)
Copia di framework/phys.js con tre aggiunte:
- `TEMPOX` = tempi da tavolo (JSON che sovrascrive TEMPO). Usati: {"turno":25,"dado":6,"carta":35,"movimento":18,"casella":12,"scontro":20,"attacco":12,"livello":20,"sconfitta":40}
- `BAGDRAW=1` = i segnalini «?» si pescano dal sacchetto quando ci si ferma (niente piazzamento iniziale)
- `BAG` = composizione del sacchetto (JSON), es. {"indizio":0,"vuota":8}; `ph` nel RES = minuti di inizio / centro / finale
Pacchetto «mezz'ora»: FIS=1 BAGDRAW=1 TEMPOX=... BAG='{"indizio":0,"vuota":8}' BALX={"ladroMov":3,"chierRev":3,"foesOff":["TE-14","TI-39","TI-22"],"ti52":"all","guerPV":2,"clsPV":{"Ladro":1},"bossPV":14}
`tri.sh label BALX` lancia 2, 3 e 4 giocatori in parallelo; `show.py file` riassume. Va messo nella cartella framework accanto a hsim.js (game.js con chierRev e clsPV).

## Senza Caos (21/10 sera)
Il Caos del Goblin è diventato un'espansione: la scatola base non ha più le 10 caselle Caos.
- `NOCAOS=1` toglie le 10 Crepe (tornano sentiero); senza, phys.js simula la base con l'espansione Caos.
- `CAOSQ=1` (con NOCAOS) le trasforma in caselle «?»; `CAOSX=n` tiene solo le prime n.
- `tri.sh label 'BALX' [VAR=valore ...]` usa i tempi da tavolo, il sacchetto e BAG (o BAGJ='{...}'); NPS='2 4' per scegliere i giocatori.
- Esempio: `N=40000 ./tri.sh base_senza_caos '{}' NOCAOS=1 > runs/x.txt; python3 show.py runs/x.txt`
