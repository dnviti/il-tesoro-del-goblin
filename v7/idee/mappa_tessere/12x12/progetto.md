# Mappa 12×12 a fiori: progetto

12/11/2026. Sostituisce il lavoro precedente sui fiori (`../fiori/`). Contiene tutte le decisioni di Daniele della giornata:
- §8 della fase A: ostacoli al 26 %, base in 2 fogli, Partenze non simmetriche ma bilanciate, Cripta su «?», carta Mappa che cambia 3 fiori, vicoli ciechi accettati;
- la regola del terreno delle 19:01;
- le decisioni dell'orchestratore su «?» e Cripta.

La Spec, il simulatore e il manuale li aggiornano altri. Il kit di stampa è fatto: vedi il §8.

File di questa cartella:
- `mappa12.py`: geometria, pezzi, regole, simulazione dei draft, ricerca del caso peggiore, scelta delle Partenze, preset con i 3 fiori di cambio, tempi, scrittura e verifica dei CSV del kit. Si lancia con `python3 v7/idee/mappa_tessere/12x12/mappa12.py`. Opzioni:
  - `--veloce`: meno prove;
  - `--partenze`: rifà la scelta delle Partenze;
  - `--scrivi-preset`: rifà la ricerca dei preset (circa 7 minuti);
  - `--scrivi-dati`: riscrive i CSV;
  - `--verifica-csv`: rimonta i 10 preset dai CSV e li controlla.

  Tutti i numeri di questo documento sono il suo output.
- `preset12.py`: i 10 preset e i loro 3 fiori di cambio.
- `disegna12.py`: mock-up con il disegno del kit. Genera `m12_pezzi` (i 14 fiori), `m12_draft` (draft casuale con «?» e Cripta) e `m12_strettoie`.

## 1. Regole (testo per il regolamento)

**Terreno.**
- Si cammina su ogni esagono che non sia un ostacolo.
- **Ostacoli:** bosco, rocce e case. Non ci si entra.
- **Terreno libero:** prato, sentiero, mattonato, pavimento, guado, ponte. Il tipo è solo estetico: entrare costa 1 passo.
- **Terreno accidentato:** l'acqua (sull'esagono c'è un piccolo «+1»). Entrarci costa 1 MOV in più, cioè 2 passi. Altri terreni accidentati potranno arrivare (nei dati c'è l'attributo `accidentato`).
- Non ci sono muri.

**Coordinate.** x è la colonna (1-12), y la riga (1-12), stampate sulla fascia della base: in alto sopra la riga 1, in basso sotto la riga 12, e ai due lati. Per trovare (x, y) si scende alla riga y e si contano x esagoni lungo la riga.

**Montaggio con il draft.**
1. Metti al centro la base (i 2 fogli uniti), con le 6 Partenze già stampate, e accanto la Sala del Tesoro.
2. Mescola i 14 fiori in un sacchetto o nella scatola, senza guardare. Ognuno ne pesca: con 2 giocatori 7, con 3 giocatori 4, con 4 giocatori 3. Con 3 o 4 giocatori i 2 avanzi restano scoperti accanto alla base.
3. A turno, dal primo giocatore in senso orario, posa uno dei tuoi fiori in uno spazio libero, con la faccia e la rotazione che vuoi. Alla fine i 2 avanzi li posa uno a testa l'ultimo giocatore del giro e poi il penultimo.
4. Dividete i 24 segnaposto «?» (2 giocatori 12, 3 giocatori 8, 4 giocatori 6). A turno posane uno su un esagono percorribile (libero o acqua; mai una Partenza) ad almeno 2 esagoni da ogni Partenza, uno per esagono. Poi una tessera Esplorazione coperta su ogni «?», come oggi.
5. Ogni eroe tira il D6 per la sua Partenza iniziale, come oggi.

**Montaggio con un preset.** Al posto dei passi 2 e 3: il foglio del preset (`mappa_preset.pdf`) dice, per ogni spazio, il fiore con la faccia (per esempio «9A») e il numero 1-6 dell'anello dello spazio verso cui va la freccia d'ottone del fiore. Poi i passi 4 e 5.

**Cripta.**
- La prima volta che un eroe prende il 3° Indizio, tira 2D6 per la x e 2D6 per la y e metti la Cripta su (x, y). Va sempre da 2 a 12, quindi riga e colonna 1 non hanno mai la Cripta.
- Se l'esagono ha una «?», la Cripta resta lì e la «?» con la sua tessera torna coperta nella riserva. Sull'acqua resta.
- Si sposta solo da un ostacolo o da una Partenza. Va sull'esagono percorribile più vicino che non sia una Partenza, non abbia una «?» e non stia in riga o colonna 1; a pari distanza vince quello più in alto (y più piccola), poi quello più a sinistra (x più piccola).
- La Cripta sbarra il passaggio come un mostro scoperto.
- «Il tesoro cambia Cripta»: togli la Cripta e tira di nuovo.

**Carta Mappa a metà partita (solo 3 fiori).**
- Il foglio della carta ha 3 righe «spazio · fiore e faccia · freccia», da applicare in ordine. Se il fiore indicato sta in un altro spazio, si scambia con quello che occupa lo spazio indicato: il fiore tolto va nello spazio liberato con la sua faccia e la sua freccia. Poi si mettono la faccia e la freccia indicate.
- Vale uguale se la mappa in gioco viene da un draft o da un altro preset.
- Prima del cambio, le «?» e le loro tessere sui fiori che si muovono tornano nella riserva; chi ha giocato la carta le rimette sui fiori nuovi, su esagoni percorribili ad almeno 2 esagoni dalle Partenze.
- Poi la Cripta si ritira col 2D6 + 2D6.
- Se una Mappa lascia il gioco senza sostituta (TI-22), si applicano le 3 righe di Strettoie.

## 2. Geometria, base e Partenze

- **Spazi:** il reticolo dei fiori è (q + 5r + 1) mod 7. Dà 14 spazi da 7 esagoni (lo spazio s girato di 180° è il 15 − s) e 46 esagoni di bordo stampati sulla base.
- **Base:** 2 fogli A4 uniti al centro, 326 × 280 mm con la fascia delle coordinate da 5,5 mm. Porta la fascia, gli spazi numerati con i numeri 1-6 sull'anello, il terreno di bordo (prato), le Partenze e 4 ostacoli singoli: bosco in (7,2) e (6,11), rocce in (2,9) e (11,4).
- **Partenze, non simmetriche e bilanciate, P1-P6 in senso orario:** (5,1), (11,2), (12,8), (9,12), (2,10), (1,4).
  - Le ha scelte `--partenze`: sono 6 esagoni della base, a 5 esagoni o più l'uno dall'altro, che rendono più uguali i passi di MOV attesi fino alla Cripta (2D6 esatti, spostamento compreso, acqua = 2) su 300 draft.
  - Scarto atteso: 0,93 passi. Su 5.000 draft simulati le medie vanno da 7,31 a 8,32 passi (scarto 1,01).

## 3. I 14 fiori

**Regola di disegno, che garantisce il collegamento.** Ogni faccia rispetta una delle due forme:
- il centro è percorribile e sull'anello ci sono al massimo 3 ostacoli, mai due vicini;
- il centro è un ostacolo e sull'anello ce n'è al massimo 1.

L'acqua non è un ostacolo, quindi non conta. L'argomento del collegamento della fase A resta valido:
- ogni fiore è tutto percorribile al suo interno;
- ogni coppia di esagoni su un lato ne ha uno percorribile;
- i lati «deboli» non sono mai vicini.

| Fiore | Faccia A | Faccia B |
|---|---|---|
| 1, 2 | 3 boschi a stella (prato) | 3 massi (pavimento) |
| 3 | 3 boschi (sentiero) | borgo a stella, 3 case (mattonato) |
| 4 | boschi e massi (prato) | 3 cascine (mattonato) |
| 5, 6 | 2 boschetti (prato / sentiero) | cava, 3 rocce / villaggio, 3 case |
| 7, 8 | strettoia con 2 ostacoli opposti (bosco; bosco e rocce) | 2 massi / 2 case |
| 9 | ruscello con guado e 2 boschi | 2 massi |
| 10 | ruscello con ponte e 2 rocce | 2 case |
| 11 | mulino sul fiume: guado e 2 case (mattonato) | rupe: rocce al centro e 1 sull'anello |
| 12 | fiume con ponte e 2 boschi | piazza: case al centro e 1 sull'anello |
| 13 | lago nel bosco: acqua al centro e 1 sull'anello, 2 boschi | miniera, 3 rocce |
| 14 | laghetto tra i massi: acqua al centro, 2 rocce e 1 bosco | mercato, 3 case |

Ostacoli per faccia: da 2 a 3, in media 2,46. Sulle 28 facce ci sono 25 bosco, 24 rocce e 20 case, più 11 acqua, 2 guadi e 2 ponti.

## 4. Simulazione (5.000 draft casuali, seme fisso)

| Misura | Risultato |
|---|---|
| mappa tutta collegata (tutte le Partenze, nessuna sacca) | 100 % |
| ostacoli (bosco, rocce, case) | 26,7 % in media (26-28 %) |
| terreno accidentato (acqua) | 3,8 % |
| ostacoli sugli esagoni di bordo | 9,1 % del bordo, contro il 36,2 % del centro 6×6 |
| ammasso di ostacoli più grande | 3,7 esagoni in media (massimo 6) |
| vicoli ciechi | 1,6 per mappa (accettati) |
| Cripta spostata (da ostacolo o Partenza) | 34,4 %, al massimo di 2 esagoni |
| Cripta su una «?» (resta lì) | 18,9 % |
| passi di MOV Partenza → Cripta, media | P1 7,56 · P2 8,12 · P3 7,50 · P4 7,31 · P5 7,80 · P6 8,32 |
| ricerca del caso peggiore (60 × 300 mosse) | nessun piazzamento con parti staccate |

## 5. Preset e cambi

| Preset | Ostacoli | Acqua | Bosco / rocce / case | Fiume (colonne, righe 4-9) | Passi attesi | Cambio (3 fiori, in ordine) | Carattere ottenuto col cambio |
|---|---|---|---|---|---|---|---|
| Strettoie | 28 % | 6 % | 9 / 18 / 13 | 10 | 7,8-8,2 | S9: 8B·6 · S6: 3B·3 · S11: 6B·2 | 82 % |
| TM-01 Forziere | 26 % | 8 % | 27 / 8 / 2 | 10 | 7,7-8,1 | S3: 3A·5 · S13: 6A·6 · S12: 1A·4 | 46 % |
| TM-02 Città | 27 % | 6 % | 6 / 15 / 18 | 8 | 7,6-8,3 | S11: 4B·1 · S10: 6B·2 · S13: 12B·1 | 45 % |
| TM-03 Foresta | 26 % | 8 % | 27 / 8 / 2 | 9 | 8,3-8,4 | S2: 1A·6 · S4: 3A·1 · S10: 2A·3 | 43 % |
| TM-04 Tundra | 26 % | 8 % | 19 / 16 / 2 | 10 | 7,6-8,5 | S13: 2B·4 · S4: 7B·4 · S7: 6A·1 | 43 % |
| TM-05 Sottovelo | 26 % | 7 % | 19 / 5 / 14 | 10 | 7,6-8,0 | S3: 2A·3 · S1: 5A·5 · S4: 14B·5 | 43 % |
| TM-06 Miniera | 27 % | 5 % | 15 / 24 / 0 | 7 | 7,3-7,8 | S14: 13B·5 · S1: 5B·6 · S13: 11B·6 | 30 % |
| TM-07 Yuma | 26 % | 8 % | 27 / 8 / 2 | 10 | 8,0-8,2 | S4: 13A·1 · S8: 10A·4 · S7: 11A·3 | 39 % |
| TM-08 Flegias | 27 % | 6 % | 13 / 10 / 16 | 10 | 7,8-8,4 | S12: 3B·2 · S3: 6B·3 · S11: 4B·2 | 59 % |
| TM-09 MIMI | 26 % | 6 % | 18 / 13 / 6 | 7 | 7,5-8,0 | S12: 13A·3 · S7: 6A·4 · S3: 10B·6 | 32 % |

Come leggere le colonne:
- «S9: 8B·6» vuol dire spazio 9, fiore 8 faccia B, freccia verso il 6.
- «Carattere ottenuto col cambio» è la parte del carattere del preset completo che i 3 fiori portano, partendo dagli altri 9 preset, in media.
- I 3 fiori di ogni carta li ha scelti `cerca_cambio`: sono le 3 righe del preset che, applicate a partire dagli altri preset e da 6 draft, danno il punteggio di carattere più alto.

`--verifica-csv` rimonta i 10 preset dai CSV del kit. Tutti sono collegati e restano collegati dopo il cambio fatto partendo da ognuno degli altri preset.

## 6. Tempi

Il modello è quello di `../modello_tempi.py` (le costanti della proposta del 12/11), più queste stime [INFERENZA]:
- decidere dove posare un fiore: 3 / 6 / 12 s; una «?»: 1 / 2,5 / 5 s;
- con 3 e 4 giocatori conta l'85 % e il 75 % della decisione, perché gli altri pensano mentre aspettano.

Come nel confronto con oggi, le tessere Esplorazione sopra le «?» non sono comprese.

| | Veloce | Tipico | Lento |
|---|---|---|---|
| draft, 2 giocatori | 3:16 | **5:26** | 9:07 |
| draft, 3 giocatori | 3:06 | **5:05** | 8:23 |
| draft, 4 giocatori | 3:00 | **4:50** | 7:55 |
| preset | 2:32 | **4:11** | 6:50 |
| carta Mappa a metà partita (3 fiori, «?» da rimettere, Cripta di nuovo) | 0:47 | **1:10** | 1:44 |
| oggi (100 tile + 16 muri, 10×10) | 7:00 | 11:13 | 17:57 |

## 7. Dati del kit (`v7/stampa/sorgenti/dati/`)

- **`fiori.csv`** (196 righe): fiore (1-14), faccia (A|B), nome, posizione, direzione, terreno, categoria, accidentato (0|1).
  - posizione: 0 = centro; 1-6 = anello in senso antiorario da E; l'1 è l'esagono della freccia.
  - direzione: E, NE, NO, O, SO, SE con la freccia verso 1.
  - terreno: prato, sentiero, mattonato, pavimento, guado, ponte, acqua, bosco, rocce o case.
  - categoria: libero, accidentato o ostacolo.
- **`base12.csv`** (144 righe, una per esagono): x, y, parte (base|spazio), spazio, posizione nello spazio; per i 46 esagoni della base anche terreno, categoria, accidentato e partenza (1-6).
- **`preset12.csv`** (140 righe): preset, carta (TM-0x; vuota per Strettoie), spazio, fiore, faccia, freccia (1-6), cambio (1-3 = le righe della carta Mappa, in ordine).
- **Rotazione:** la posizione p di una faccia va nella posizione ((p − 1 + freccia − 1) mod 6) + 1 dello spazio.

## 8. Kit di stampa (A4)

| File | Pagine | Contenuto |
|---|---|---|
| `mappa_base.pdf` | 2 | la base in 2 metà, cartoncino da 250-300 g; si taglia sulla linea esterna e sulla giunzione; 5 rombi di rame a cavallo della giunzione per allinearle; si uniscono col nastro dietro |
| `mappa_fiori.pdf` | 6 = 3 fogli fronte/retro | pagine dispari fronte (facce A con le linee di taglio), pari retro (facce B specchiate per girare il foglio sul lato lungo dell'Epson ET-2870, senza linee); abbondanza di 2 mm su tutte e due le facce; id piccolo nell'angolo; foglio 3 con 24 segnaposto «?» (Ø 20 mm) e il segnalino Cripta, a due facce uguali |
| `mappa_preset.pdf` | 10 (carta comune) | schema di ogni preset con fiore e faccia in grande per ogni spazio, la freccia e il suo numero, i 3 fiori di cambio con il bordo di rame e numerati, le regole del cambio |
| `sala_tesoro.pdf` | 1 | la Sala del Tesoro (rotelle del custode e dello scontro, Spostamenti del tesoro), senza i muri |

La mappa A3 non c'è: si stampano i PDF A4. Il kit A3 ha solo la Sala del Tesoro in un pezzo.

Generatore: `componenti_gen/fiori12.py` (dati e disegno) e la sezione «MAPPA 12×12» di `gen.py`.

Tolti dal kit:
- le tessere esagonali singole (`tessere_mappa`), i muri, i fogli dei preset 10×10 (`preset_mappa`), anche in A3;
- le plance intere 10×10 (`sorgenti/plance/`, opzioni `--plance` e `--plancia`, `svg.board()`).
