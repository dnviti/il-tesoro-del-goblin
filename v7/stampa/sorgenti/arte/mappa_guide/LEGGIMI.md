# Guide per la mappa 12×12 (immagini di ingresso del generatore)

Rifare tutto: `python3 genera_guide.py` (dati: `../../dati/*.csv`, geometria e palette: `../mappa_comune.py`).

| File | Cosa | Misura |
|---|---|---|
| `MF-<NN><A\|B>.png` (28) | una faccia di fiore, esagoni a punta in alto, esagono 0 al centro, anello 1-6 antiorario da EST (1 = E, 2 = NE, 3 = NW, 4 = W, 5 = SW, 6 = SE), freccia a EST come stampato | 1024 × 1024 px, 12 px/mm, centro (512, 512): fiore 907 × 873 px (75,6 × 72,75 mm), margine 58 px ai lati e 75 px sopra/sotto |
| `MB-NO/NE/SO/SE.png` (4) | un quarto della base 12 × 12 | 1536 × 1024 px, 7 px/mm: finestra 219,43 × 146,29 mm |
| `palette.json` | colore piatto di ogni terreno (e della pergamena `#f1dcae`) | |
| `geometria.json` | misure, origini delle finestre, formule pixel↔mm, misura dei PNG di stampa | |
| `prompt.csv` | `id,file,size,description`: una riga per guida, descrizione del terreno in inglese | |

## Disegno delle guide
- Ogni esagono pieno del colore piatto del suo terreno; lati a 1 px (`#1a1a1a`); nessun testo né icona.
- Fuori dal fiore e, nella base, sui 98 esagoni degli spazi dei fiori: pergamena neutra `#f1dcae` (i fiori li coprono).
- Partenze della base: giallo piatto `#f4d21f`.
- Il ponte è l'esagono marrone scuro (ponte di legno sull'acqua), il guado l'esagono turchese (sassi nell'acqua).

## Base: pixel ↔ mm
Coordinate della griglia: origine nell'angolo in alto a sinistra, x verso destra, y verso il basso; centro dell'esagono
(c, r): `x = 25,2 · (c − 0,5 + (0,5 se r pari))`, `y = R · (1 + 1,5 (r − 1))`, R = 14,549 mm. Griglia 315 × 269,16 mm.
Nella guida: `px = (x − x0) · 7`, `py = (y − y0) · 7`, con l'origine (x0, y0) della finestra:

| Quarto | x0 mm | y0 mm |
|---|---|---|
| NO | −4 | −4 |
| NE | 99,57 | −4 |
| SO | −4 | 126,87 |
| SE | 99,57 | 126,87 |

Le finestre si sovrappongono di 115,9 mm in orizzontale e 15,4 mm in verticale (3:2 non permette metà esatte a questa
scala). Il compositore prende ogni esagono dal solo quarto che lo possiede (colonna ≤ 6 ovest, riga ≤ 6 nord): il
taglio segue i lati degli esagoni, nessuna sfumatura tra generazioni diverse.
