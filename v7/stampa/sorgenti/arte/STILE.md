# Illustrazioni v7: stile e flusso (10/11)

Decisione di Daniele (10/11): tutte le carte, le pedine, le plance eroe e le plance di gioco hanno un'illustrazione generata, poi importata e rifinita in PhotoCraft. Stile scelto: quello di `grezze/prova_stile.png`.

## Stile (uguale per tutte le richieste)

Campo `style` del generatore, sempre identico:

> simple hand-drawn cartoon, rough slightly wobbly ink lines, flat colours with light shading, goofy and clumsy, Munchkin-like humour, light steampunk medieval high-magic touches (a few brass gears, rivets, a puff of steam, a glowing rune), only a few simple scene props, readable at small size, easy to redraw, no text, no letters, no border, no frame

- Ambientazione (Daniele, 11/11): steampunk medievale, alta magia, cartoonesca e goliardica.
- **Semplicità (Daniele, 11/11, decisione vincolante):** disegni semplici, sgangherati e simpatici, pochi oggetti. Chi guarda capisce dall'immagine che cosa fa la carta e non si distrae. Devono essere facili da ridisegnare per un illustratore, a costi bassi. Il livello è la «via di mezzo»: i protagonisti della gag più 2–4 oggetti di scena; lo steampunk è un dettaglio (un ingranaggio, una molla, uno sbuffo), non un ambiente pieno di macchinari.
- **Sfondo (Daniele, 11/11, correzione):** ogni immagine ha lo sfondo giusto per la sua scena (taverna, bosco, cripta, mercato…), disegnato semplice: pochi elementi, non una tinta piatta. Stile simile a Munchkin ma riconoscibile e proprio: divertente, un po' pazzo, e sempre rappresentativo di quello che fa la carta. Pedine su fondo chiaro uniforme (vanno ritagliate). Tessere della mappa: colori naturali del terreno, vista dall'alto.
- Tutte le immagini fatte prima di questa decisione (fantasy dettagliato e steampunk ricco dell'11/11 mattina) si rifanno in questo stile.

- Tono goliardico (D21): personaggi buffi, espressioni esagerate, gag visiva presa dalla battuta o dal nome della carta. Mai cupo o solenne, anche per i boss: minacciosi ma ridicoli.
- Niente testo nell'immagine: nomi e regole li stampa il generatore.
- Gli eroi non hanno una classe disegnata sulle carte comuni; sulle carte di classe si vede l'archetipo della classe (Assaltatore corazzato e manesco, Ricercatore inventore con occhialoni, Stregone mago pasticcione, Oracolo indovino con turbante e palla di vetro, Giullare buffone con sonagli).
- Il goblin Geronimo e il forziere MIMI sono ricorrenti: stessa faccia e stessi colori dove compaiono.
- Tessere tematiche (11/11): le tessere `PT-<TEMA>-*` e le sale `PS-<TEMA>` (FORESTA, TUNDRA, CITTA, FORZIERE, SOTTOVELO, MINIERA, YUMA, FLEGIAS, MIMI…) sono nel vecchio stile, **non sono usate dal kit di stampa** (la mappa si compone con le tessere generiche `PT-BASE-*` e `PS-BASE` e i preset) e sono facoltative: si rifanno nello stile semplice solo se un giorno servono.

## Formati

| Oggetto | Riquadro stampato | Ritaglio | Richiesta al generatore |
|---|---|---|---|
| Carte Mappa/Incanto/Equipaggiamento/di classe/Carte Classe/Specie | 154,6 × 108 pt (54,5 × 38,1 mm), finestra «alla Magic» sotto la barra del nome | 1,43:1, centrato | `aspect_ratio` 4:3 (o 16:9); `composition`: «medium shot, the whole subject centred with some headroom, nothing important at the left and right edges» |
| Carte Mostro | 154,6 × 102 pt (54,5 × 36 mm) | 1,52:1, centrato | come sopra |
| Boss (mazzetto 3) | 154,6 × 84 pt (54,5 × 29,6 mm) | 1,84:1, centrato | come sopra, 16:9 |
| Carte Imprevisto | 154,6 × 120 pt (54,5 × 42,3 mm) | 1,29:1, centrato | 4:3 |
| Pedine, plance, plance di gioco | dalla geometria dei generatori | dal riquadro | dal riquadro |

Esportazione: 300 ppi alla misura stampata, sRGB, PNG.

## Cartelle

- `prompt/<mazzo>.csv`: una riga per illustrazione: `id,file,subject,action,scene,composition,lighting,aspect_ratio`. Lo `style` non si ripete: è quello sopra.
- `grezze/<id>.webp`: immagine come esce dal generatore (non si ritocca), salvata in WebP con perdita minima (qualità 92, stessa misura in px della PNG originale) per tenere leggero il repo; `elabora.py` accetta anche una `.png`.
- `pcraft/<id>.pcraft`: progetto PhotoCraft: livello dell'immagine grezza, ritaglio e misura, livelli di regolazione per uniformare i toni (curve, tonalità/saturazione), mai pixel modificati a mano. Non è versionato (cartella in `.gitignore`): si rigenera con `python3 elabora.py --tutti --forza`.
- `png/<id>.png`: esportazione finale letta dai generatori di stampa.

La battuta resta sulla carta, in corsivo in fondo al testo sotto un filetto (non più sull'illustrazione, dall'11/11).

## Rifinitura (`elabora.py`)

- `formati.csv`: tipo, misura in mm e in px a 300 ppi di ogni riquadro, con il punto del generatore che lo disegna.
- `python3 elabora.py <id> [--tipo <tipo>] [--alto|--basso|--sinistra|--destra] [--zoom Z]` rifà una illustrazione; `--tutti` elabora ogni `grezze/*.png` con tipo noto e salta quelle già fatte (`--forza` le rifà). Posizione e zoom del ritaglio per id in `ritagli.csv` (colonne `id,tipo,orizzontale,verticale,zoom`): le grezze 16:9 delle carte usano già tutta l'altezza, quindi la posizione verticale conta solo con zoom > 1, che serve a togliere la fascia pergamena vuota in fondo alle grezze fatte per la vecchia fascetta della battuta. Dettagli in testa allo script.

## Mappa 12×12 (12/11): terreno generato su guide

Il terreno dei 14 fiori (28 facce) e della base è generato con gpt-image-2 a partire da guide piatte (`mappa_guide/`: `MF-<NN><A|B>.png` 1024 × 1024, `MB-NO|NE|SO|SE.png` 1536 × 1024, palette, geometria e `prompt.csv` in `mappa_guide/LEGGIMI.md`). Dati e geometria sono quelli del kit (`dati/fiori.csv`, `base12.csv`), per questo i terreni non si possono sbagliare di posto: si controllano con `mappa_compone.py --verifica`.

Flusso: `grezze/MF-*.webp` e `grezze/MB-*.webp` (come escono dal generatore; la misura può essere diversa dalla guida, per esempio 1254 × 1254, ma la stessa proporzione) → `python3 mappa_compone.py` (allinea alla guida con scala e traslazione piccole, ritaglia sul contorno + 2 mm di abbondanza, quarti della base cuciti lungo i lati degli esagoni, look condiviso di `elabora.py`) → `png/MF-<NN><A|B>.png` (941 × 914 px, 300 ppi) e `png/MB-BASE.png` (3721 × 3180 px) → `componenti_gen/fiori12.py` li usa come fondo di fiori e base se ci sono (altrimenti resta il vettoriale); sopra restano bordi sottili, bordo degli ostacoli, «+1» dell'acqua, Partenze, freccia, id, coordinate e spazi numerati. I fogli dei preset restano vettoriali. `elabora.py --tutti` salta MF-* e MB-*.

Comandi (dalla radice del repo):

```
python3 v7/stampa/sorgenti/arte/mappa_compone.py --verifica   # terreni: esce con 1 se un esagono non somiglia al dato
python3 v7/stampa/sorgenti/arte/mappa_compone.py              # allinea, ritaglia, scrive arte/png/MF-*.png e MB-BASE.png
python3 v7/stampa/sorgenti/arte/mappa_compone.py --verifica-pdf  # contorno dell'arte sui PDF: vuoti dentro, arte fuori (anche in verifica_pdf.py)
bash v7/stampa/sorgenti/componenti_gen/build.sh v7/stampa/sorgenti v7/stampa/playtest_v7   # kit: mappa_base, mappa_fiori, ...
python3 v7/stampa/3d_solidcraft/carta_fiori_3d.py              # carta_fiori_3d.pdf (variante 3D)
python3 v7/stampa/sorgenti/verifica_pdf.py                     # controlli di stampa
```

Contorno degli esagoni (12/11, difetto sulla base): il modello disegna ogni esagono vicino alla guida ma non esatto (bordi spostati fino a ~1,3 mm, a volte un cordolo color pergamena dentro il bordo). `mappa_compone.py` adatta quindi ogni esagono (scala e traslazione sul suo bordo scuro), scarta il bordo del modello e il cordolo, e ritaglia l'arte esattamente sul contorno vettoriale (+0,1 mm sotto la linea); la linea sottile è l'unico contorno. `--verifica-pdf` rende i PDF a 300 dpi e controlla ogni lato (vuoto dentro, arte fuori).
