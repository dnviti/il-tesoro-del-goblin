# Dati di stampa del playtest (regole = bozza Word del 2/11, con le regole decise dall'autore nella bozza del 3/11)

Tutte le fonti sono lette dal commit `2aa7f84`. Percorsi `v2/…` = vecchi; dopo la ristrutturazione: `v2/sorgenti` → `gioco/sorgenti`, `v2/regolamento_stampa` → `regolamento/sorgenti`, `v2/originali` → `carte/originali`.
Le scelte provvisorie, le correzioni alle carte e le modifiche dovute alla bozza del 3/11 (pareggio, 3 Indizi, Forte Volontà, Incanto, niente critici), alla v6 e alla v6-bis dell'8/11 (stati, Carte Classe e Specie, stampa solo fronte) sono in `decisioni_provvisorie.md`. Formato foglio: A4 (e A3), **solo fronte**.

## 0. Convenzioni dei CSV

- UTF-8, riga di intestazione, separatore virgola, campi con virgole tra virgolette, fine riga `\n`.
- **Una riga per copia fisica** in tutti i file, tranne `segnalini.csv` (colonna `copie`; dalla v6-bis niente Clessidre: vedi `decisioni_provvisorie.md`, sezione 8).
- Le Carte Aiuto hanno il testo su più righe: dentro lo stesso campo, le righe sono separate da un a capo (`\n`).
- Il testo da stampare è nella colonna `testo` (o `bonus`, `nota` di `carte_specie.csv`, `passoN_testo`, `riquadro_carte`, `retro_*`). Altrove la colonna `nota` non va stampata.
- Classi rinominate ovunque (Guerriero → Assaltatore, Mago → Stregone, Ladro → Ricercatore, Oracolo invariato). Eccezioni volute: il nome di luogo «Cimitero dei Maghi» (TM-05) e il nome carta «Occhio dello Stregone» (TI-06).
- Tutti i testi sono copiati da `cards_v2.json`, `nemici_v2.json`, `xlsx_v2.py` (lista `IMP`) o dalla bozza. Fanno eccezione, e sono segnalati: TI-12, la scelta PROVVISORIA del Yumaniano, le Carte Aiuto, i testi cambiati dalla bozza del 3/11 (Ispirazione → Forte Volontà, Incantesimo → Incanto, elenco in `decisioni_provvisorie.md`, sezione 3) e quelli della v6-bis (stati, Locanda, TE-08, TI-03, Carte Classe TC-01…04, Carte Specie: sezione 8). Divisori e Pedine: nome e disposizione sono una scelta (vedi sotto).

## 1. Conteggi (le carte sommano a 133)

| File | Righe | Componente | Carte | Dorso |
|---|---|---|---|---|
| `carte_comuni.csv` | 44 | 8 Mappe (TM-01…08) + 12 Equipaggiamenti (TE: 02,05…10,16…20) + 24 Incanti (TI-01…24) | 44 | sì, «Carta comune» |
| `carte_classe.csv` | 29 | Assaltatore 8, Ricercatore 5, Stregone 4, Oracolo 12; 24 carte uniche, 5 doppie stampate una volta per mazzo (colonna `mazzo`) | 29 | sì, colore e nome della classe |
| `carte_classe_ritratto.csv` | 4 | Carte Classe TC-01…04 | 4 | no (scoperta sulla plancia eroe) |
| `carte_specie.csv` | 8 | Carte Specie TS-01…04, 2 copie ciascuna (Umano, Elfo, Sanguar, Yumaniano) | 8 | no (scoperta sulla plancia eroe) |
| `carte_mostro.csv` | 24 | mazzetto 1: NE-01…13 (13); mazzetto 2: NE-14…21 (8); boss NE-26…28 (3). Mini-boss NE-22…25 esclusi | 24 | sì, «Mostro» + numero del mazzetto |
| `carte_imprevisto.csv` | 11 | Trappola ×5, Locanda ×2, Fonte ×2, Fabbro ×2 | 11 | sì, «Imprevisto» |
| `carte_aiuto.csv` | 4 | 4 righe identiche; ogni riga stampa 2 carte: «Il turno» e «Riepilogo» | 8 | no |
| `divisori.csv` | 5 | vedi sotto | 5 | no |
| **Totale carte** | | 44 + 29 + 4 + 8 + 24 + 11 + 8 + 5 | **133** | 108 dorsi |
| `tessere_esplorazione.csv` | 36 | 25 rosse (TX-01…25) + 11 blu (TX-26…36) | – | |
| `segnalini.csv` | vedi il file | Indizi, Forte Volontà, Usato e tessere Stato (componenti, non carte) | – | |
| `pedine.csv` | 9 | 4 eroi, MIMI, Geronimo + 3 sagome Boss (vedi nota) | – | |

`tessere_specie.csv` (8 tessere 50 × 25 mm) è stato tolto nella v6-bis: lo sostituisce `carte_specie.csv`.

### PDF delle carte (stampa solo fronte, v6-bis)

| PDF | Contenuto | Fogli A4 | Fogli A3 |
|---|---|---|---|
| `carte_comuni.pdf` + `carte_comuni_retri.pdf` | 44 fronti + 44 dorsi | 5 + 5 | 3 + 3 |
| `carte_classe.pdf` + `carte_classe_retri.pdf` | 33 fronti (29 dei mazzi + TC-01…04) + 29 dorsi (le celle delle Carte Classe sono vuote) | 4 + 4 | 3 + 3 |
| `carte_specie.pdf` | 8 Carte Specie, un lato | 1 | 1 |
| `carte_mostro.pdf` + `carte_mostro_retri.pdf` | 24 fronti + 24 dorsi | 3 + 3 | 2 + 2 |
| `carte_imprevisto.pdf` + `carte_imprevisto_retri.pdf` | 11 fronti + 11 dorsi | 2 + 2 | 1 + 1 |
| `carte_aiuto_divisori.pdf` | 4 × («Il turno» + «Riepilogo») + 5 Divisori, un lato | 2 | 1 |
| **Totale carte** | 133 carte + 108 dorsi | **31** | **20** |

Ogni PDF ha un foglio per pagina, da stampare solo fronte. I dorsi non sono specchiati: il dorso nella posizione p del foglio k di `<nome>_retri.pdf` va con il fronte nella posizione p del foglio k di `<nome>.pdf`. Ogni fronte e ogni dorso si ritaglia da solo con la dima 63 × 88 mm; poi si incollano dorso contro dorso (colla stick su tutta la superficie, pressati) o si infilano insieme in una bustina 66 × 91 mm. Dentro un mazzo i dorsi sono tutti uguali: l'abbinamento conta solo per mazzo (Classe: per colore della classe; Mostro: per numero del mazzetto).

### Anatomia delle carte (v6-bis)

- **Cella:** carta 63 × 88 mm più l'abbondanza (2,5 mm in A4, 3 mm in A3) su tutti e 4 i lati; griglia 3 × 3 (A4) o 4 × 4 (A3) centrata; tacche d'angolo nel margine dove c'è posto e filetti bianchi a ogni angolo di rifilo, dentro l'abbondanza. Testo a ≥ 3 mm dal rifilo.
- **Carte comuni e di classe** (`carta_trama`): titolo; etichetta tipo · slot; riquadro segnaposto dell'illustrazione con il codice del tipo (e «MAZZO <CLASSE>» per le carte di classe, «PROVVISORIO» dove serve); testo dell'effetto (valori tra parentesi in grassetto); in basso classi, rarità/copia e ID. Nessuna icona di durata: gli effetti finiscono alla Fine del turno o diventano stati.
- **Carta Classe** (TC-01…04): come sopra, etichetta «CARTA CLASSE», testo del potere una volta per partita, in basso la composizione della mano («Mano: 5 delle 8 carte di classe + 5 comuni»). Un lato.
- **Carta Specie** (TS-01…04): cornice nel colore della specie (Umano `#4a5568`, Elfo `#2f7a8a`, Sanguar `#7a2f4f`, Yumaniano `#8a6a1c`), etichetta «CARTA SPECIE», segnaposto «TS», bonus in grande, nota in piccolo, copia e ID. Un lato.
- **Carta Mostro**: medaglione con lettera, nome, LV e mazzetto, ID, segnaposto (BOSS per i boss), 3 riquadri PV/ATT/AR (dalla sera dell'8/11; prima c'era anche la Difesa), danno, abilità, ricompense (boss: «Custode» e «Mazzetto 3» su 3 righe).
- **Carta Imprevisto**: fascia colorata con il nome, «IMPREVISTO», segnaposto «?», testo, copia e ID.
- **Carte Aiuto:** «Il turno» (3 passi numerati e riquadro «Carte») e «Riepilogo» (Scontro, Ricompense, Tessere «?», Sconfitta, Vittoria), due carte a un lato.
- **Divisori:** un lato, colore del tipo, codice grande, titolo e contenuto.
- **Dorsi** (`dorso`): fondo colorato, doppia cornice, «IL TESORO DEL GOBLIN», nome del mazzo; nell'abbondanza in basso un'etichetta minuscola con il mazzo e l'ID del fronte («Mostro 2 · NE-19»), che sparisce col taglio. Nel margine del foglio: «RETRI · foglio k di n · coi fronti del foglio k».

Verifiche fatte sullo script `gen.py` (in /tmp, eliminato) prima della v6-bis: 44 + 29 + 4 + 24 + 11 = 112 righe di carta con testo, più 4 Aiuto e 5 Divisori = 121; ogni riga ha lo stesso numero di campi dell'intestazione; nessuna occorrenza residua di Guerriero/Mago/Ladro nei testi. Dalla v6-bis: + 8 Carte Specie + 4 Carte Aiuto (ogni Carta Aiuto diventa 2 carte) = 133 (`genera_carte.py` stampa «totale carte: 133»).

### Dettagli per file

- **`carte_comuni.csv`**: colonne `id, tipo, tipo_nome, nome, rarita, slot, classe_riga, testo, corretto_dalla_bozza, nota, fonte`. `classe_riga` = «Tutte le classi». Il testo è il campo `testo` di `cards_v2.json` (non `testo_originale`). Modifiche: TI-12 (D20 → 2D6) e, dal 3/11, Incantesimo → Incanto e Ispirazione → Forte Volontà (TM-07, TI-01, TI-08, TI-21, TI-23; elenco in `decisioni_provvisorie.md`, sezione 3). TE-18 e TE-20 hanno una nota APERTO (citano Locanda/Fonte come caselle).
- **`carte_classe.csv`**: colonne `mazzo, id, tipo, tipo_nome, nome, rarita, slot, classe_riga, testo, copia, nota, fonte`. `classe_riga` è la dicitura stampata in fondo («Assaltatore - Oracolo» per le doppie); `copia` = «1 di 2» / «2 di 2» per le 5 doppie. Righe per mazzo: Assaltatore 8, Ricercatore 5, Stregone 4, Oracolo 12. Doppie: TE-01 (Assaltatore - Oracolo), TE-04 (Stregone - Oracolo), TI-30, TI-34, TI-35 (Assaltatore - Oracolo).
- **`carte_classe_ritratto.csv`**: colonne `id, nome, classe, classe_riga, testo, corretto_dalla_bozza, nota, fonte`. I 4 testi «Classe: <nome>» della v6-bis (spec §4.1: poteri una volta per partita con la tessera Usato, nessuna statistica); `classe_riga` = composizione della mano, stampata in fondo. `corretto_dalla_bozza` vuoto (niente PROVVISORIO sulla carta).
- **`carte_specie.csv`**: colonne `id, nome, specie, copia, bonus, nota, provvisorio, fonte`. 4 specie × 2 copie (stesso ID per le 2 copie). `bonus` e `nota` si stampano; `provvisorio` = «sì» per il Yumaniano (bozza: «Da decidere»).
- **`carte_mostro.csv`**: colonne `id, mazzetto, nome, lettera, lv, pv, att, ar, danno, abilita, ricompense, ricompensa_se_mazzetto_3, nota, fonte`.
  - `ar` = AR da superare con 2D6 + ATT (decisione dell'utente 8/11 sera, niente più Difesa): è il valore che fino ad allora era stampato come Difesa (8-11); la `nota` riporta l'AR di prima. La carta stampa 3 riquadri: PV, ATT, AR.
  - `danno` ricavato dal LV con la tabella della bozza (LV 1: D6 − 1; LV 2: D6; LV 3+: D6 + 1); coincide con il campo `danno` del JSON per tutte le 24 carte. Sul layout Nemico del pptx il danno non ha un campo: il regolamento dice «il livello dice quanto fa male».
  - `fx` (chiave del motore) e `origine` non vanno stampati.
  - Boss (NE-26…28): `ricompense` = «MIMI: vinci la partita» (boss custode); `ricompensa_se_mazzetto_3` = «Indizio se D6 ≤ 5 · +1 livello · Forte Volontà» (in origine «1 indizio · +1 livello · Forte Volontà», copiato dai mini-boss del JSON, uguale al testo «Boss del mazzetto 3: 1 Indizio, sali subito di livello e prendi l'Ispirazione» della bozza; Ispirazione → Forte Volontà e «sali di livello» → «+1 livello» dal 3/11; Indizio con il D6 dalla v6, decisione dell'utente dell'8/11). Va stampata sulla carta Boss insieme all'altra, perché il boss pescato a inizio partita fa da custode e gli altri 2 formano il mazzetto 3.
  - Mazzetto 1 = LV 1-2, mazzetto 2 = LV 3-4, ricompense dalla v6 (8/11): mazzetto 1 «Indizio se D6 ≤ LV · 1 PE»; mazzetto 2 «Indizio se D6 ≤ LV · 1 PE · Forte Volontà», con il LV della carta scritto come numero (fino alla v5: «1 indizio · 1 punto esperienza», mazzetto 2 «… · Forte Volontà»).
- **`carte_imprevisto.csv`**: `testo` = lista `IMP` di `v2/sorgenti/xlsx_v2.py` riga 75 (IM-01 Trappola ×5, IM-02 Locanda ×2, IM-03 Fonte ×2, IM-04 Fabbro ×2). `testo_bozza` solo dove la bozza ha una formulazione diversa (Trappola, Locanda, Fabbro): scegliere una sola versione.
- **`carte_aiuto.csv`**: 4 righe identiche (una per giocatore); ogni riga stampa 2 carte a un lato.
  - «Il turno» (`fronte_titolo`, `passo1…3_*`, `riquadro_carte`): dalla v6-bis «Il turno in 3 passi» (Muovi, Esplora, Fine) con nome, icona (`parts_stampa.py turn_strip()`: piedi, occhio, bandiera) e testo, più il riquadro senza numero su quando si giocano carte ed Equipaggiamenti. Storia: v5 5 passi (con «Carte»), v6 4 passi (con «Clessidre»).
  - «Riepilogo» (`retro_*`): pagina «Riepilogo» della bozza: Scontro, Ricompense, Tessere «?», Sconfitta, Vittoria. Dal 3/11: tolta la riga dei critici e aggiunte le due righe del pareggio; 3 Indizi; Forte Volontà nelle Ricompense. v6: Indizio dei mostri «D6 ≤ LV». v6-bis: fuga «mai dal custode», sacchetto vuoto, Rotella del custode (`decisioni_provvisorie.md`, sezione 8).
  - Disposizione e titolo «Riepilogo» sono una scelta di impaginazione.
- **`divisori.csv`**: INFERENZA. Nessun file definisce i 5 Divisori. Ipotesi usata: i 4 «Separatore di tipo» del modello dell'autore (`Carte_Trama_…_v2.pptx`: MAPPA, INCANTESIMO, EQUIPAGGIAMENTO, CLASSE; titolo in maiuscolo e codice TM/TI/TE/TC, colore del tipo) più NEMICO come quinto tipo del catalogo (`xlsx_v2.py` ha 5 colori: TM TE TI TC NE). Dal 3/11 il divisore TI si chiama INCANTO; dalla v6-bis DV-04 divide «Carte Classe e Carte Specie» (12). Un lato. Alternativa: 4 divisori di classe + «Carte comuni», se si preferisce dividere per mazzo di classe. Da confermare con l'autore.
- **`tessere_esplorazione.csv`**: 25 rosse = Mostro (icona `spade`, `#a8352a`, scritta «Mostro»), 11 blu = Imprevisto (icona `dado`, `#2f5d9c`, scritta «Imprevisto»), da `build.py` righe 107-108 e `parts.py color_token()`. Ø 24 mm, un lato: dalla v6-bis il retro resta bianco (prima era il cerchio «?» di `parts.py back_token()`).
- **`segnalini.csv`**: dalla v6-bis SG-01 Indizio ×16 (`pergamena`), SG-03 Forte Volontà ×4 (`stella` oro), SG-04 Usato ×12 (spunta); Ø 20 mm, un lato. Le tessere Stato (6 tipi, 14 pezzi, 26 × 18 mm) sono in `stati.csv`. La riga Clessidra è stata tolta (vedi `decisioni_provvisorie.md`, sezione 8).
- **`pedine.csv`**: 4 eroi (Assaltatore, Ricercatore, Stregone, Oracolo), MIMI (forziere), Geronimo (primo giocatore). Aggiunte 3 sagome Boss (Guardiano di MIMI, Mimic ancestrale, Re Goblin Grugno): la bozza le elenca come componente a parte («3 Boss») e scrive «I boss e MIMI sulle sagome». I colori di miniatura e dorso delle classi non sono definiti nel repo («la miniatura e il mazzetto dello stesso colore»): vanno scelti.

## 2. Plancia e scheda eroe: cosa c'è disegnato (disegni di partenza, prima della v6-bis)

Dalla v6-bis la scheda eroe è diventata la plancia eroe con le rotelle e la plancia di gioco ha la Rotella dello scontro e del custode: sono generate da `stampa/sorgenti/componenti_gen/` (spec v6-bis §5-6). Qui resta la descrizione dei disegni d'origine.

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
- Fascia bassa «Promemoria»: «Perdita D6: 1 tutto · 2 elmo · 3 arma DX · 4 arma SX · 5 armatura · 6 niente» e la riga del turno, che nel kit attuale è «Turno: Muovi · Esplora · Fine» con «Sacchetto vuoto: rimetti dentro le tessere usate» (v6-bis; fino alla v5 elencava 5 passi). Nella v6-bis la traccia «PV del boss» qui sopra è sostituita dalla Rotella dello scontro e dalla Rotella del custode.
- Legenda (build.py): «Partenze 1–6: si tira il D6», «Casella ?: pesca una tessera», «Cripte 1–4: una nasconde MIMI», «Il Cuore».
- Compatibile con la bozza: nessuna classe, specie o D20.

### Scheda eroe (`parts.py scheda()`; scheda «a doppio strato»)

- Fila alta con 5 slot (bordo alto, le carte vi si infilano): Classe, Elmo, Arma DX, Arma SX, Armatura.
- Riquadro «Tessera Specie · si incastra qui»; «Si parte da: PV 5 · ATT 1 / MOV 1 · AR 1»; «Livello su: +1 ATT, MOV o AR oppure +2 PV».
- Tracce: PV con 20 caselle («caselle 1–20 · rosso = PV attuali · nero = PV massimi»; **nel disegno le caselle PV non hanno cifre**, il codice le scrive solo se le caselle sono 12 o meno: aggiungere le cifre 1–20 in stampa); ATT 0–8; MOV 0–6; AR 0–8 con un secondo valore stampato sotto ogni casella (scala del regolamento v5, tolta); PE 0–8 con caselle dorate in 2, 4, 6, 8 («caselle dorate = Livello 2, 3, 4, 5»).
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
| Blu `BLUE` (AR) | `#2f5d7c` |
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
- Anatomia di un equipaggiamento nel regolamento base v5 (p. 13, `regolamento/sorgenti/book/parts.py card_anatomy()`, storico): fascia in alto con nome e bonus, linea di infilata, illustrazione, testo, icona di durata, classi e codice carta. Il kit v6-bis non usa icone di durata: l'anatomia delle carte stampate è nella sezione 1.
- Formato carta del kit: 63 × 88 mm (formato Magic, dima MTG), con 2,5 mm (A4) o 3 mm (A3) di abbondanza per carta (sezione 1).

## 4. Cosa non è stato fatto o verificato

- Nessuna carta/tessera è stata composta: sono solo dati. Nessuna immagine è stata prodotta nel repo.
- I colori di miniature e dorsi di classe non sono nel repo (la bozza dice solo «dello stesso colore»); i colori giocatore del gioco digitale (`--p0…p3`: `#e8714f`, `#4fbcd0`, `#c08be6`, `#a3d65c`) non sono legati alle classi.
- Il contenuto dei Divisori e il formato fisico delle carte e delle tessere sono una scelta aperta.
- Il bonus Yumaniano e la correzione TI-12 aspettano la conferma dell'autore; i poteri delle Carte Classe della v6-bis sono da provare nel playtest.
