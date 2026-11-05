# Sorgenti della versione giocabile (21/10/2026)

- `game.js` motore (tabella `BAL` in alto = tutti i numeri del bilanciamento), `ui.js` interfaccia e simulatore, `template.html` pagina e regole, `cards.json` le 108 carte.
- Build: `python3 build.py` crea `tesoro_del_goblin.html` e `check.js`.
- Simulatore da riga di comando: `node mkharness.js` crea `hsim.js`; poi `node hsim.js 20000 rand std exp.js` (giocatori 2|3|4|rand, regole std|rand). Variabili: `BALX='{"chiave":valore}'` per provare numeri, `FORCE=Classe ONLY=Classe` per il tasso di vittoria di una classe, `ABL=TI-xx` per togliere una carta all'IA, `MUOUT=file.json` con `mu.js` per i matchup, `DUMP=file.json` per salvare le partite. `base4.js` simula la scatola base a 4 classi.
- Catalogo: `python3 xlsx_update.py` riscrive l'Excel a partire da `cards.json` e `before_texts.json`.
