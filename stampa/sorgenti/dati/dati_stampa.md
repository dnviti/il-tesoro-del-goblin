# Dati di stampa del playtest (regole = bozza Word del 2/11, con le regole decise dall'autore nella bozza del 3/11)

Tutte le fonti sono lette dal commit `2aa7f84`. Percorsi `v2/…` = vecchi; dopo la ristrutturazione: `v2/sorgenti` → `gioco/sorgenti`, `v2/regolamento_stampa` → `regolamento/sorgenti`, `v2/originali` → `carte/originali`.
Le scelte provvisorie, le correzioni alle carte e le modifiche dovute alla bozza del 3/11 (pareggio, 3 Indizi, Forte Volontà, Incanto, niente critici) sono in `decisioni_provvisorie.md`. Formato foglio: A4.

## 0. Convenzioni dei CSV

- UTF-8, riga di intestazione, separatore virgola, campi con virgole tra virgolette, fine riga `\n`.
- **Una riga per copia fisica** in tutti i file, tranne `segnalini.csv` (colonna `copie`: Indizi 12, Clessidre 12, Forte Volontà 4).
- Le Carte Aiuto hanno il testo su più righe: dentro lo stesso campo, le righe sono separate da un a capo (`\n`).
- Il testo da stampare è nella colonna `testo` (o `bonus`, `passoN_testo`, `retro_*`). La colonna `nota` non va stampata.
- Classi rinominate ovunque (Guerriero → Assaltatore, Mago → Stregone, Ladro → Ricercatore, Oracolo invariato). Eccezioni volute: il nome di luogo «Cimitero dei Maghi» (TM-05) e il nome carta «Occhio dello Stregone» (TI-06).
- Tutti i testi sono copiati da `cards_v2.json`, `nemici_v2.json`, `xlsx_v2.py` (lista `IMP`) o dalla bozza. Fanno eccezione, e sono segnalati: le 3 carte corrette (TI-12, TC-01, TC-04), la scelta PROVVISORIA del Yumaniano, le Carte Aiuto e i testi cambiati dalla bozza del 3/11 (Ispirazione → Forte Volontà, Incantesimo → Incanto, elenco in `decisioni_provvisorie.md`, sezione 3). Divisori e Pedine: nome e disposizione sono una scelta (vedi sotto).

## 1. Conteggi (le carte sommano a 121)

| File | Righe | Componente | Carte |
|---|---|---|---|
| `carte_comuni.csv` | 44 | 8 Mappe (TM-01…08) + 12 Equipaggiamenti (TE: 02,05…10,16…20) + 24 Incanti (TI-01…24) | 44 |
| `carte_classe.csv` | 29 | Assaltatore 8, Ricercatore 5, Stregone 4, Oracolo 12; 24 carte uniche, 5 doppie stampate una volta per mazzo (colonna `mazzo`) | 29 |
| `carte_classe_ritratto.csv` | 4 | Carte Classe TC-01…04 | 4 |
| `carte_mostro.csv` | 24 | mazzetto 1: NE-01…13 (13); mazzetto 2: NE-14…21 (8); boss NE-26…28 (3). Mini-boss NE-22…25 esclusi | 24 |
| `carte_imprevisto.csv` | 11 | Trappola ×5, Locanda ×2, Fonte ×2, Fabbro ×2 | 11 |
| `carte_aiuto.csv` | 4 | 4 copie identiche | 4 |
| `divisori.csv` | 5 | vedi sotto | 5 |
| **Totale carte** | | 44 + 29 + 4 + 24 + 11 + 4 + 5 | **121** |
| `tessere_specie.csv` | 8 | Umano ×2, Elfo ×2, Sanguar ×2, Yumaniano ×2 (nella bozza: «da confermare») | – |
| `tessere_esplorazione.csv` | 36 | 25 rosse (TX-01…25) + 11 blu (TX-26…36) | – |
| `segnalini.csv` | 3 righe, 28 pezzi | 12 Indizi, 12 Clessidre, 4 Forte Volontà | – |
| `pedine.csv` | 9 | 4 eroi, MIMI, Geronimo + 3 sagome Boss (vedi nota) | – |

Verifiche fatte sullo script `gen.py` (in /tmp, eliminato): 44 + 29 + 4 + 24 + 11 = 112 righe di carta con testo, più 4 Aiuto e 5 Divisori = 121; ogni riga ha lo stesso numero di campi dell'intestazione; nessuna occorrenza residua di Guerriero/Mago/Ladro nei testi.

### Dettagli per file

- **`carte_comuni.csv`**: colonne `id, tipo, tipo_nome, nome, rarita, slot, classe_riga, testo, corretto_dalla_bozza, nota, fonte`. `classe_riga` = «Tutte le classi». Il testo è il campo `testo` di `cards_v2.json` (non `testo_originale`). Modifiche: TI-12 (D20 → 2D6) e, dal 3/11, Incantesimo → Incanto e Ispirazione → Forte Volontà (TM-07, TI-01, TI-08, TI-21, TI-23; elenco in `decisioni_provvisorie.md`, sezione 3). TE-18 e TE-20 hanno una nota APERTO (citano Locanda/Fonte come caselle).
- **`carte_classe.csv`**: colonne `mazzo, id, tipo, tipo_nome, nome, rarita, slot, classe_riga, testo, copia, nota, fonte`. `classe_riga` è la dicitura stampata in fondo («Assaltatore - Oracolo» per le doppie); `copia` = «1 di 2» / «2 di 2» per le 5 doppie. Righe per mazzo: Assaltatore 8, Ricercatore 5, Stregone 4, Oracolo 12. Doppie: TE-01 (Assaltatore - Oracolo), TE-04 (Stregone - Oracolo), TI-30, TI-34, TI-35 (Assaltatore - Oracolo).
- **`carte_classe_ritratto.csv`**: i 4 testi «Classe: <nome>». TC-01 corretta (+1 PV, −1 AR come da bozza), TC-04 allineata (Locanda dal sacchetto); TC-03 «uno Stregone».
- **`carte_mostro.csv`**: colonne `id, mazzetto, nome, lettera, lv, pv, att, ar, difesa, danno, abilita, ricompense, ricompensa_se_mazzetto_3, nota, fonte`.
  - `difesa` = 8 + AR (scala 2D6), ricalcolata: il valore di `nemici_v2.json` (14 + AR) è ignorato. Esempio verificato con la bozza: Guardiano di MIMI AR 3 → Difesa 11, Lupo grigio AR 0 → Difesa 8.
  - `danno` ricavato dal LV con la tabella della bozza (LV 1: D6 − 1; LV 2: D6; LV 3+: D6 + 1); coincide con il campo `danno` del JSON per tutte le 24 carte. Sul layout Nemico del pptx il danno non ha un campo: il regolamento dice «il livello dice quanto fa male».
  - `fx` (chiave del motore) e `origine` non vanno stampati.
  - Boss (NE-26…28): `ricompense` = «MIMI: vinci la partita» (boss custode); `ricompensa_se_mazzetto_3` = «1 indizio · +1 livello · Forte Volontà» (copiato dai mini-boss del JSON, uguale al testo «Boss del mazzetto 3: 1 Indizio, sali subito di livello e prendi l'Ispirazione» della bozza; Ispirazione → Forte Volontà e «sali di livello» → «+1 livello» dal 3/11). Va stampata sulla carta Boss insieme all'altra, perché il boss pescato a inizio partita fa da custode e gli altri 2 formano il mazzetto 3.
  - Mazzetto 1 = LV 1-2, mazzetto 2 = LV 3-4, ricompense: mazzetto 1 «1 indizio · 1 punto esperienza»; mazzetto 2 «1 indizio · 1 punto esperienza · Forte Volontà».
- **`carte_imprevisto.csv`**: `testo` = lista `IMP` di `v2/sorgenti/xlsx_v2.py` riga 75 (IM-01 Trappola ×5, IM-02 Locanda ×2, IM-03 Fonte ×2, IM-04 Fabbro ×2). `testo_bozza` solo dove la bozza ha una formulazione diversa (Trappola, Locanda, Fabbro): scegliere una sola versione.
- **`carte_aiuto.csv`**: 4 copie identiche (una per giocatore).
  - Fronte: «Il turno in 5 passi», 5 passi con nome, icona (`parts.py turn_strip()`: clessidra, carte, piedi, occhio, bandiera) e testo, copiati dalla tabella della bozza.
  - Retro: pagina «Riepilogo» della bozza: Scontro, Ricompense, Tessere «?», Sconfitta, Vittoria. Dal 3/11: in Scontro tolta la riga dei critici e aggiunte le due righe del pareggio decise dall'autore; Vittoria con 3 Indizi; Forte Volontà nelle Ricompense.
  - Disposizione e titolo «Riepilogo» sono una scelta di impaginazione.
- **`divisori.csv`**: INFERENZA. Nessun file definisce i 5 Divisori. Ipotesi usata: i 4 «Separatore di tipo» del modello dell'autore (`Carte_Trama_…_v2.pptx`: MAPPA, INCANTESIMO, EQUIPAGGIAMENTO, CLASSE; titolo in maiuscolo e codice TM/TI/TE/TC, colore del tipo) più NEMICO come quinto tipo del catalogo (`xlsx_v2.py` ha 5 colori: TM TE TI TC NE). Dal 3/11 il divisore TI si chiama INCANTO. Alternativa: 4 divisori di classe + «Carte comuni», se si preferisce dividere per mazzo di classe. Da confermare con l'autore.
- **`tessere_specie.csv`**: 4 specie × 2 copie. Colonne `id, specie, copia, bonus, nota_a_piè, provvisorio, nota, fonte`. Bonus da copiare (bozza, tabella «Le specie»): Umano «+1 MOV e +1 a una statistica a scelta», Elfo «+2 a una statistica a scelta», Sanguar «+2 MOV (sono non morti)», Yumaniano «+1 AR e +1 a una statistica a scelta (PROVVISORIO)». Nota a piè uguale per tutte: «Bonus a scelta: ATT, MOV o AR. I PV crescono solo con i livelli.» Le tessere si incastrano nella scheda eroe («Tessera Specie, si incastra qui»).
- **`tessere_esplorazione.csv`**: 25 rosse = Mostro (icona `spade`, `#a8352a`, scritta «Mostro»), 11 blu = Imprevisto (icona `dado`, `#2f5d9c`, scritta «Imprevisto»), da `build.py` righe 107-108 e `parts.py color_token()`. Retro: cerchio `#3b2a1c` con bordo oro `#b8862b` e «?» in Cinzel 800 oro (`parts.py back_token()`). Sono tonde nel disegno; il diametro reale non è definito.
- **`segnalini.csv`**: icone dalla scheda eroe (`parts.py scheda()`): Indizio `pergamena`, Clessidra `clessidra`, Forte Volontà (ex Ispirazione) `stella` oro. Non sono disegnati come segnalini nel regolamento: `parts.py simple_token()` esiste ma non è usato in `build.py`.
- **`pedine.csv`**: 4 eroi (Assaltatore, Ricercatore, Stregone, Oracolo), MIMI (forziere), Geronimo (primo giocatore). Aggiunte 3 sagome Boss (Guardiano di MIMI, Mimic ancestrale, Re Goblin Grugno): la bozza le elenca come componente a parte («3 Boss») e scrive «I boss e MIMI sulle sagome». I colori di miniatura e dorso delle classi non sono definiti nel repo («la miniatura e il mazzetto dello stesso colore»): vanno scelti.

## 2. Plancia e scheda eroe: cosa c'è disegnato

I generatori `board()` (in `svg.py`) e `scheda()` (in `parts.py`) **producono SVG direttamente**, senza dipendenze: sono funzioni Python pure che restituiscono una stringa SVG. Verificato eseguendoli da un checkout di `2aa7f84` (output XML ben formato).

Comando (da un checkout, o dal repo dopo la ristrutturazione al posto di `v2/regolamento_stampa` con `regolamento/sorgenti`):

```
mkdir /tmp/co && git -C <repo> archive 2aa7f84 v2/regolamento_stampa/book v2/regolamento_stampa/fonts | tar -x -C /tmp/co
cd /tmp/co/v2/regolamento_stampa/book
python3 -c "from parts import *; open('plancia.svg','w').write(board(W=26)); open('scheda.svg','w').write(scheda())"
```

- `board(W=26)` (W = larghezza di un esagono in unità SVG) → viewBox `0 0 366.6 461.5`, rapporto 0,794. Su A4 verticale con margini di 10 mm: 190 × 239 mm, esagoni di 13,5 mm. Parametri: `caos_tiles=False` (default; le 10 Crepe sono dell'espansione), `label=True` (lettere A–J e numeri 1–10), `show_bands=True`, `heroes=None`.
- `scheda()` → viewBox `0 0 540 430`, rapporto 1,256 (il parametro `w` è ignorato). Su A4 orizzontale con margini di 10 mm: 238,6 × 190 mm.
- Gli SVG non hanno `width`/`height`, solo `viewBox`: si scalano a piacere. I testi usano `font-family` Alegreya Sans e Cinzel **non incorporati**: installare i font prima di convertire in PDF/PNG, o convertire i testi in tracciati.
- Per le stesse immagini a piccole dimensioni nel regolamento: `board(W=20)` (build.py riga 118).

### Plancia «Le Terre di Hande» (`svg.py board()`)

- 10 × 10 esagoni, colonne A–J e righe 1–10; il «Cuore» (colonne 2–7 e righe 2–7 contando da 0, cioè C–H e 3–8) con fondo `#e6d6b4` e bordo oro tratteggiato. Girata di 180° è identica.
- 6 Partenze numerate 1–6 (viola `#7a4f86`) in colonna/riga (0-based) (2,0), (7,0), (9,4), (7,9), (2,9), (0,5): ogni partenza ha di fronte quella con numero +3.
- 4 Cripte numerate 1–4 (oro) in (3,3), (6,3), (3,6), (6,6).
- 36 caselle «?» (15 coppie simmetriche = 30, più 6 che in origine erano Locanda, Fonte, Fabbro, ora tutte «?»). Le altre caselle sono sentieri senza simbolo.
- Fascia alta «Sala del Tesoro» con 4 cerchi: «Custode» (grande, oro), «MIMI», «Boss», «Boss»; sotto, «PV del boss» con 9 caselle numerate 9 → 1 (le caselle 4…1 più scure).
- Fascia bassa «Promemoria»: «Turno: Clessidre · Carte · Muovi · Esplora · Fine» e «Perdita D6: 1 tutto · 2 elmo · 3 arma DX · 4 arma SX · 5 armatura · 6 niente».
- Legenda (build.py): «Partenze 1–6: si tira il D6», «Casella ?: pesca una tessera», «Cripte 1–4: una nasconde MIMI», «Il Cuore».
- Compatibile con la bozza: nessuna classe, specie o D20.

### Scheda eroe (`parts.py scheda()`; scheda «a doppio strato»)

- Fila alta con 5 slot (bordo alto, le carte vi si infilano): Classe, Elmo, Arma DX, Arma SX, Armatura.
- Riquadro «Tessera Specie · si incastra qui»; «Si parte da: PV 5 · ATT 1 / MOV 1 · AR 1»; «Livello su: +1 ATT, MOV o AR oppure +2 PV».
- Tracce: PV con 20 caselle («caselle 1–20 · rosso = PV attuali · nero = PV massimi»; **nel disegno le caselle PV non hanno cifre**, il codice le scrive solo se le caselle sono 12 o meno: aggiungere le cifre 1–20 in stampa); ATT 0–8; MOV 0–6; AR 0–8 con la Difesa 8–16 stampata sotto («Difesa (8 + AR): già stampata sotto ogni casella»); PE 0–8 con caselle dorate in 2, 4, 6, 8 («caselle dorate = Livello 2, 3, 4, 5»).
- Colonna destra: Indizi (2 caselle, «al 2°: tesoro!»; nel kit dal 3/11: 3 caselle, «al 3°: tesoro!»), Clessidre (3 caselle, «mai più di 3»), Ispirazione (1 casella, «una sola»; nel kit: «Forte Volontà»), «Dal sacchetto»: «+1 PE, +2 PV» (Locanda), «2 carte» (Fonte), «1 equip.» (Fabbro).
- Piè di pagina: «I cubetti mostrano sempre il valore finale, equipaggiamento compreso.»; «Effetti in corso · carte con i cubetti Durata»; «Scarti · a faccia in su».
- Nessun nome di classe o specie: la scheda è già compatibile con la bozza. L'Assaltatore parte con 6 PV (scritto sulla sua Carta Classe, non sulla scheda).

## 3. Identità visiva da mantenere

Fonti: `regolamento/sorgenti/book/{svg,parts,build}.py` e `fonts/`; `carte/originali/*.pptx`; `officina/Officina_del_Goblin.html`; `gioco/…_v2.html`.

### Font

- **Cinzel** (titoli, nomi sulle carte Nemico, numeri sulle tessere): pesi 600 e 800.
- **Alegreya** (testo del regolamento e delle carte, 10,4 pt, interlinea 1,4): 400, 700, corsivo 400.
- **Alegreya Sans** (tabelle, etichette, scheda, tessere): 400, 700, 800.
- File `.woff2`, sottoinsiemi latini (`unicode-range` U+0000-00FF, U+2000-206F, U+2212 ecc.). **Mancano `≥` (U+2265) e `→` (U+2192)**, usati nella Carta Aiuto (retro): il sottoinsieme non li contiene, vanno scelti da un font completo.
- **Avvertenza sul grassetto**: nei file `Alegreya-normal-700.woff2` e `Alegreya-normal-400.woff2` il blob git è lo stesso (`94d5815…`, 43476 byte), e `Cinzel-normal-800.woff2` è uguale a `Cinzel-normal-600.woff2` (`a54fd00…`, 25904 byte). Quindi **non esistono grassetti veri** per Alegreya e Cinzel: il grassetto nel regolamento è sintetizzato dal motore di stampa. Alegreya Sans ha invece 3 file diversi (400, 700, 800). Per la stampa installare Cinzel (600/800) e Alegreya (400/700, corsivo) veri dal catalogo Google Fonts (NON verificato qui) invece di riusare questi `.woff2`.
- Nel pptx dell'autore tutto è in **Georgia** (carte Trama e Nemico): carattere sostitutivo del modello, non quello del regolamento. Il gioco HTML v2 usa **Pirata One** per i titoli (`--f-display`) e Alegreya/Alegreya Sans: è un'identità solo digitale.

### Colori (regolamento: `svg.py` riga 2-3, `build.py` righe 7-63)

| Uso | Valore |
|---|---|
| Inchiostro `INK` | `#2a2118` |
| Marrone `BROWN` (bordi, sottotitoli) | `#6b4a2b` |
| Rosso `RED` (titoli h1, PV, accenti) | `#9c2f24` |
| Oro `GOLD` (cornice, Cripte, PE) | `#b8862b` |
| Blu `BLUE` (AR, Difesa) | `#2f5d7c` |
| Carta/pagina `PAPER` | `#f4ead5` |
| Cuore della plancia / fondo plancia e tessere | `#e6d6b4` / `#efe1c3` |
| Esagoni / linee | `#f7efdc` / `#b9a582` |
| Riquadri chiari (box, caselle) | `#fffaf0`; box rosso: bordo `#9c2f24`, fondo `#fbefe6` |
| Partenze (viola) | `#7a4f86` |
| Locanda / Fonte / Fabbro | `#c0662b` / `#2f7a8a` / `#4a5568` |
| Tessera rossa / blu | `#a8352a` / `#2f5d9c` |
| Retro tessera | fondo `#3b2a1c`, oro `#b8862b` |
| Copertina | fondo `#2b1d14`, titolo `#f6d68b` |

- Pagina: sfondo `PAPER` con ombreggiatura radiale, cornice oro 0,5 mm a 9 mm dal bordo con angoli di 2 mm (opacità 0,55), riquadri con bordo marrone 0,35 mm e angoli 2 mm. h1 Cinzel 800 17 pt rosso; h2 Cinzel 800 11 pt marrone.
- Libreria di 21 icone vettoriali in `svg.py icon()` (clessidra, spade, cuore, scudo, stivale, stella, pergamena, forziere, casa, goccia, martello, teschio, trappola, occhio, dado, carte, freccia, piedi, bandiera, elmo, cripta): riusarle.

### Cornice delle carte

- **Carte Trama** (`Carte_Trama_Il_Tesoro_del_Goblin_v2.pptx`, modello dell'autore): 15,24 × 22,49 cm; Georgia; blu notte `#101830`/`#0B1530`, oro `#B8860B`/`#D9A93C`/`#8A5A12`, pergamena `#FFF1D0`, inchiostro `#1A1208`. Struttura: titolo in alto (38 pt), riquadro illustrazione (13,38 × 10,72 cm), testo dell'effetto (19 pt) con parole chiave in grassetto e valori tra parentesi, linea con rombo oro, etichetta della classe in basso («Mago - Stregone» nel modello). Le cornici sono sfondo bloccato (immagini PNG nel pptx). Colori dei tipi nella legenda dell'autore: **Mappa rossa, Incantesimo blu, Equipaggiamento verde, Classe viola (proposta, da approvare)**. Il gioco digitale usa altri colori (TI `#7656c2`, TE `#b2742f`, TC `#b23741`, TM `#3b7d4f`): per la stampa fa fede la legenda dell'autore.
- **Carte Nemico** (`Layout_Carta_Nemico_Canva.pptx` / `Carte_Nemico_v2.pptx`): orizzontale 28,575 × 19,05 cm (3:2); Georgia; fondo blu `#0B1530`, oro `#D9A93C`, titoli `#F6D77A`, pannelli pergamena `#F1DCAE`, testo `#101A33`, medaglione viola `#2A1259` con lettera `#C9A6FF`, cuore PV `#D62B2B`, scudo AR `#E0A43A`. Struttura: medaglione con lettera, titolo, «LV. n», illustrazione (13,9 × 9,4 cm), tre pannelli PV/ATT/AR, «ABILITÀ SPECIALI» e «RICOMPENSE». Riprodotta in `parts.py enemy_card()` (viewBox 450 × 300).
- **Carta fisica nel gioco/officina**: rapporto 63 : 88, fondo `#fbf8ef`, bordo `#6d5321` 2 px, angoli 14 px (`.card` in `officina/Officina_del_Goblin.html`).
- Anatomia di un equipaggiamento (regolamento p. 13, `card_anatomy()`): fascia in alto con nome e bonus, che resta visibile quando la carta è infilata nella scheda; linea di infilata; illustrazione; testo; icona di durata (spade = scontri, clessidra = turni, numero = cubetti); in basso classi e codice carta.
- Formato carta non definito nel repo per la stampa A4 (il pptx Trama è 15,24 × 22,49 cm, il rapporto dell'officina è 63 : 88): va deciso.

## 4. Cosa non è stato fatto o verificato

- Nessuna carta/tessera è stata composta: sono solo dati. Nessuna immagine è stata prodotta nel repo.
- I colori di miniature e dorsi di classe non sono nel repo (la bozza dice solo «dello stesso colore»); i colori giocatore del gioco digitale (`--p0…p3`: `#e8714f`, `#4fbcd0`, `#c08be6`, `#a3d65c`) non sono legati alle classi.
- Il contenuto dei Divisori e il formato fisico delle carte e delle tessere sono una scelta aperta.
- Il bonus Yumaniano e le correzioni TC-01, TC-04, TI-12 aspettano la conferma dell'autore.
