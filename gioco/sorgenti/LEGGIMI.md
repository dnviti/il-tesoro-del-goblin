# Sorgenti del gioco giocabile v2 (Carte Trama v2)

Risultato: `../Il_Tesoro_del_Goblin_gioco_v2.html`, un solo file HTML autonomo. Tutti i comandi si lanciano **da questa cartella** (i percorsi sono relativi). Serve Python 3; per il simulatore Node.

Attenzione: il motore è ancora a **D20** (regole del 21/10 con le patch del 2/11 sugli eventi e sui colori). La patch `patch_2d6.py` (2D6, regolamento v5) **non è stata applicata**: il gioco è quindi indietro rispetto al regolamento (vedi `../../README.md`).

## Contenuto

| File | Cosa fa |
|---|---|
| `dati_v2.py` | **Sorgente vera dei dati**: le Carte Trama v2 (72 carte) e i nemici (28), con `testo_originale` (testo dell'autore), `testo` (adattato alla scatola) e `modifica`. Scrive `cards_v2.json` e `nemici_v2.json` |
| `cards_v2.json`, `nemici_v2.json` | Dati generati da `dati_v2.py` (da non modificare a mano) |
| `game.js`, `ui.js`, `template.html` | Motore, interfaccia e simulatore, pagina |
| `build.py` | Unisce template + game.js + ui.js + i due json |
| `patch_v2.py`, `blocks/`, `draft_val.json` | Rigenerano `game.js` dal motore del 21/10 (`game_21-10.js`) |
| `patch_eventi.py`, `patch_colori.py` | Patch del 2/11, **già applicate** a `game.js` |
| `patch_2d6.py` | Patch del 2D6, **da applicare** quando si decide di allineare il gioco al regolamento v5 |
| `xlsx_v2.py` | Scrive il catalogo Excel (`../../carte/Catalogo_carte_v2.xlsx`) |
| `mknem.py` | Scrive le Carte Nemico (pptx) a partire dal layout Canva |
| `rules_v2.html` | Frammento HTML della pagina «Regole adottate» (non usato da `build.py`) |
| `specie.py` | Sostituisce «razza» con «specie» nei file indicati |
| `mkharness.js`, `hmain.js`, `exp.js`, `run1.sh`, `runv.sh`, `valstat.js`, `cardstat.js`, `diag*.js` | Simulatore da riga di comando e analisi (vedi sotto) |
| `smoke.js`, `smoke2.js` | Prove a video del gioco (Playwright) |

## Rigenerare il gioco

```
python3 dati_v2.py                      # solo se cambiano i dati delle carte (riscrive i due json)
python3 build.py                        # crea tesoro_del_goblin.html e check.js
mv tesoro_del_goblin.html ../Il_Tesoro_del_Goblin_gioco_v2.html
```

`build.py` dà `tesoro_del_goblin.html`, che va **rinominato a mano** come sopra. `check.js` serve al simulatore. Entrambi sono rigenerabili e non sono tracciati da git.

## Rigenerare game.js (solo se serve ripartire dal motore del 21/10)

`game.js` nel repository è già l'uscita finale di tutta la catena. Per rifarla:

```
python3 patch_v2.py game_21-10.js game.js     # usa blocks/ e draft_val.json
python3 patch_eventi.py game.js
python3 patch_colori.py game.js
python3 patch_2d6.py game.js                  # NON ancora applicata
```

Le patch non sono idempotenti: falliscono se lanciate su un `game.js` già modificato. `game_21-10.js` è l'ingresso di `patch_v2.py` ed è identico a `../../archivio/v1_21-10/sorgenti/game.js`: tenuto qui perché la cartella resti autonoma. `draft_val.json` si rifà con `valstat.js`.

## Catalogo e carte Nemico

- `python3 xlsx_v2.py ../../carte/Catalogo_carte_v2.xlsx` (richiede openpyxl). Il foglio Leggimi e la colonna «Difesa (10+AR)» descrivono ancora il D20.
- `python3 mknem.py ../../carte/originali/Layout_Carta_Nemico_Canva.pptx nemici.json ../../carte/Carte_Nemico_v2.pptx` (richiede python-pptx). `nemici.json` deve essere senza i mini-boss: con `nemici_v2.json` completo escono 28 carte invece delle 24 di `Carte_Nemico_v2.pptx` (che ha anche la slide del modello).

## Simulatore

```
python3 build.py && node mkharness.js     # crea hsim.js (non tracciato)
node hsim.js 20000 4 std expd.js          # N partite, giocatori, regole, file di analisi
./run1.sh etichetta '{"chiave":valore}' 8000 4
./runv.sh etichetta '{"chiave":valore}' 3000   # 2, 3, 4 giocatori
```

`run1.sh` e `runv.sh` scrivono in `runs/` (cartella da creare, non tracciata) e usano un file di analisi `expd.js` che **non è nel repository**; `exp.js` è il file di analisi presente. I risultati delle simulazioni sono in `../../simulazioni/`.

Gli stessi sorgenti alimentano il motore dell'Officina: `../../officina/sorgenti/build_motore_v2.py` legge game.js, ui.js e i due json da questa cartella.

Note: `exp.js` con la variabile `REP` carica `report.js`, che esiste solo in `../../archivio/v1_21-10/sorgenti/`. `mkharness.js` legge `check.js` e scrive `hsim.js` nella stessa cartella.

## Collaudo del kit di stampa (`sim_playtest.py`)

Il simulatore qui sopra è sulla scala D20. Per il kit fisico del playtest (2D6 + ATT ≥ AR del bersaglio, tabella dei danni, 3 Indizi) c'è `sim_playtest.py`. È un file solo, con la sola libreria standard, e legge i CSV stampati in `../../stampa/sorgenti/dati/`. Va lanciato dalla radice del repository:

```
python3 gioco/sorgenti/sim_playtest.py --esatto --partite 10000 --uscita simulazioni/playtest_v6_2026-11-08.txt
python3 gioco/sorgenti/sim_playtest.py --partite 10000 --bonus-indizio 1  # taratura Indizi: D6 ≤ LV + 1 (2 = LV + 2)
python3 gioco/sorgenti/sim_playtest.py --partite 10000 --senza-carte      # sensibilità: mani vuote
```

`--esatto` calcola le probabilità esatte degli scontri delle 4 classi, dal livello 1 al 5, contro i 24 mostri. `--partite N` gioca N partite Monte Carlo a 2, 3 e 4 giocatori. Le regole simulate e le approssimazioni sono stampate in testa al rapporto.
