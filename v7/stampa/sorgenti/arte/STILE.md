# Illustrazioni v7: stile e flusso (10/11)

Decisione di Daniele (10/11): tutte le carte, le pedine, le plance eroe e le plance di gioco hanno un'illustrazione generata, poi importata e rifinita in PhotoCraft. Stile scelto: quello di `grezze/prova_stile.png`.

## Stile (uguale per tutte le richieste)

Campo `style` del generatore, sempre identico:

> hand-painted storybook fantasy illustration, humorous Munchkin-like cartoon, bold ink outlines, warm parchment palette, no text, no letters, no border, no frame

- Tono goliardico (D21): personaggi buffi, espressioni esagerate, gag visiva presa dalla battuta o dal nome della carta. Mai cupo o solenne, anche per i boss: minacciosi ma ridicoli.
- Niente testo nell'immagine: nomi e regole li stampa il generatore.
- Gli eroi non hanno una classe disegnata sulle carte comuni; sulle carte di classe si vede l'archetipo della classe (Assaltatore corazzato e manesco, Ricercatore inventore con occhialoni, Stregone mago pasticcione, Oracolo indovino con turbante e palla di vetro, Giullare buffone con sonagli).
- Il goblin Geronimo e il forziere MIMI sono ricorrenti: stessa faccia e stessi colori dove compaiono.

## Formati

| Oggetto | Riquadro stampato | Ritaglio | Richiesta al generatore |
|---|---|---|---|
| Carte Mappa/Incanto/Equipaggiamento/Classe/Specie | 150,6 × 50 pt (53,1 × 17,6 mm) | 3:1, centrato | `aspect_ratio` 16:9; `composition`: «wide panoramic shot, the whole subject inside the central horizontal band, calm uncluttered lower quarter» |
| Carte Mostro, Imprevisto | dalla geometria di `carte/genera_carte.py` | dal riquadro | 16:9, stessa composizione |
| Pedine, plance, plance di gioco | dalla geometria dei generatori | dal riquadro | dal riquadro |

Esportazione: 300 ppi alla misura stampata, sRGB, PNG.

## Cartelle

- `prompt/<mazzo>.csv`: una riga per illustrazione: `id,file,subject,action,scene,composition,lighting,aspect_ratio`. Lo `style` non si ripete: è quello sopra.
- `grezze/<id>.png`: immagine come esce dal generatore (non si ritocca).
- `pcraft/<id>.pcraft`: progetto PhotoCraft: livello dell'immagine grezza, ritaglio e misura, livelli di regolazione per uniformare i toni (curve, tonalità/saturazione), mai pixel modificati a mano.
- `png/<id>.png`: esportazione finale letta dai generatori di stampa.

La battuta resta sulla carta, su una fascetta pergamena nella parte bassa dell'illustrazione.

## Rifinitura (`elabora.py`)

- `formati.csv`: tipo, misura in mm e in px a 300 ppi di ogni riquadro, con il punto del generatore che lo disegna.
- `python3 elabora.py <id> [--tipo <tipo>] [--alto|--basso|--sinistra|--destra]` rifà una illustrazione; `--tutti` elabora ogni `grezze/*.png` con tipo noto e salta quelle già fatte (`--forza` le rifà). Posizioni di ritaglio per id in `ritagli.csv`. Dettagli in testa allo script.
