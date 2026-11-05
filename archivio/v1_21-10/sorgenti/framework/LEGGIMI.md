# Modello della scatola fisica (framework di design, 21/10/2026)

Serve a misurare carte, effetti e plance Terreno come nel documento «Framework di design per espansioni»
(https://claude.ai/artifact/1hHwQUccdsdVdJYvLzL4Y2).

- `build_x.py`: crea `hsim.js` dai sorgenti in `..` (game.js, ui.js, cards.json, hmain.js) con il movimento a percorso (mura, portali, terreno difficile).
- `phys.js`: scatola base fisica (4 classi, 4 razze, niente D4, creature fisse, plancia stampata con Cripte) + effetti di prova sull'eroe 0 + stampa `RES {...}`.
- `boards.js`: le plance Terreno di prova (selva, selvaFitto, cimitero, cimiteroCentro, cittadella, cittadella2, cittadella3, ...).
- `dist.js`: distanze partenza → Cripte per una plancia (`node dist.js selva cittadella3`).
- `fight.js`, `traits.js`: calcolatore di scontro e tratti dei nemici (formula della Minaccia).

Esempi (copiare la cartella in un posto con scrittura veloce, poi):
- `python3 build_x.py`
- misura di un effetto: `EFF=att WHEN=0 node hsim.js 40000 2 std phys.js | grep RES` (effetti: att, ar, mov, pv, clue, card, insp, pe, skip, oskip, heal3, odmg3, att3c, adv1c, ar2c, recover, odisc, oclue, extra; si sommano con `+`; `give:TI-52` dà una carta)
- carta di classe: `CLS0=Mago EFF=give:TI-52 node hsim.js 40000 2 std phys.js` (confronta con `CLS0=Mago EFF=ctrl`)
- plancia: `BOARD=cittadella3 node hsim.js 40000 4 std phys.js | grep RES`
- `delta` = Punti Potere (punti percentuali di vittoria rispetto all'atteso), `min` = durata stimata, `cls` e `spawn` = indici per classe e partenza.
