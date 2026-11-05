# Materiali stampabili per il playtest

Kit per le prime partite di prova. Regole di riferimento: **bozza Word del 2/11** (`regolamento/Regolamento_Tesoro_del_Goblin_bozza.docx`): classi Assaltatore, Ricercatore, Stregone, Oracolo; specie Umano, Elfo, Sanguar, Yumaniano (8 tessere); iniziativa a 1 D6. Dettagli e motivazioni in `sorgenti/dati/decisioni_provvisorie.md`.

## Scelte provvisorie (marcate PROVVISORIO dove il testo è stampato)

- **Draft:** si passa sempre a destra (solo regolamento, nessun componente).
- **Yumaniano:** +1 AR e +1 a una statistica a scelta (tessere SP-07 e SP-08, con marcatore).
- **Mazzetto dei mostri:** si sceglie dal livello dell'eroe (1-2 / 3-4 / 5), non dagli Indizi.
- **Pareggio di iniziativa:** si ritira (retro della Carta Aiuto, riga in rosso).

Altri testi modificati rispetto al PDF v5, segnalati con PROVVISORIO sulle carte:

- **TI-12 Parola di Confusione:** svantaggio = tira due volte i 2D6 e vale il totale peggiore (era «due D20»).
- **TC-01 Assaltatore:** «(+1) PV» e «(-1) AR» (da confermare).
- **TC-04 Oracolo:** il potere torna pronto quando peschi una Locanda dal sacchetto.

## PDF in `playtest_v5/`

Tutti A4. Stampa **al 100 % / dimensioni effettive** (niente «adatta alla pagina»), margini minimi 5 mm. Ogni pezzo ha 3 mm di abbondanza e linea di taglio.

| File | Contenuto | Pezzi | Pagine | Stampa e montaggio |
|---|---|---|---|---|
| `carte_comuni.pdf` | 8 Mappe, 12 Equipaggiamenti, 24 Incantesimi | 44 | 5 + 5 | Fronte-retro, capovolgi sul lato lungo. 9 carte da 63×88 mm per foglio; ritaglia sulle tacche. |
| `carte_classe.pdf` | Mazzi Assaltatore 8, Ricercatore 5, Stregone 4, Oracolo 12 + 4 ritratti TC-01…04 | 33 | 4 + 4 | Come sopra. |
| `carte_mostro.pdf` | Mazzetto 1 (13), mazzetto 2 (8), boss (3) | 24 | 3 + 3 | Come sopra. |
| `carte_imprevisto.pdf` | Trappola, Locanda, Fonte, Fabbro | 11 | 2 + 2 | Come sopra. |
| `carte_aiuto_divisori.pdf` | 4 Carte Aiuto + 5 Divisori | 9 | 1 + 1 | Come sopra. |
| `plancia.pdf` | Plancia «Le Terre di Hande» in 4 fogli | 1 (355,6 × 447,7 mm) | 4 | Solo fronte. Foglio 1 sotto; ritaglia i margini bianchi dei fogli 2-4 sulle tacche e sovrapponili (16 mm circa) facendo coincidere le **croci rosse** e il disegno; incolla su cartoncino 1-2 mm. |
| `schede_eroe.pdf` | Schede Assaltatore, Ricercatore, Stregone, Oracolo | 4 (222 × 176,8 mm) | 4 orizzontali | Solo fronte. Traccia PV numerata 1-20. |
| `tessere_esplorazione.pdf` | 25 rosse Mostro, 11 blu Imprevisto | 36 (Ø 24 mm) | 2 | Fronte-retro, lato lungo; il retro è uguale al fronte (il colore si legge da ogni lato). |
| `tessere_specie.pdf` | Umano, Elfo, Sanguar, Yumaniano ×2 | 8 (50 × 25 mm) | 1 | Solo fronte. |
| `segnalini.pdf` | 12 Indizi, 12 Clessidre, 4 Ispirazione | 28 (Ø 20 mm) | 1 | Solo fronte. Le caselle della scheda sono da 9 mm: i segnalini si appoggiano accanto. |
| `pedine.pdf` | 4 eroi, MIMI, Geronimo (24 × 82 mm aperte); 3 boss (40 × 104 mm aperte) | 9 | 1 | Ritaglia, piega sulla linea tratteggiata, incolla fronte e retro, piega le due linguette (una avanti, una indietro) per il piede a T. |

**Totali:** 121 carte (44 + 33 + 24 + 11 + 9); 36 tessere esplorazione, 8 tessere specie, 28 segnalini, 9 pedine, 4 schede eroe, 1 plancia.

## Da procurarsi (non stampabile)

32 cubetti Durata bianchi · 24 cubetti statistica (4 set) · 1 cubetto boss giallo · 4 dadi D6 · 1 sacchetto per le tessere. Consigliato: cartoncino 1-2 mm per plancia e schede.

## Font

- **Carte:** Noto Serif (titoli e testo) e IBM Plex Sans Condensed (etichette, statistiche, Carta Aiuto).
- **Componenti:** Liberation Serif Bold (titoli) e Liberation Sans Narrow (etichette).
- **Perché:** Cinzel e Alegreya del repo hanno il grassetto sintetizzato e mancano di ≥ e →. Tutti i font sono incorporati nei PDF.

## Come rigenerare

- **Carte:** `python3 stampa/sorgenti/carte/genera_carte.py` (legge i CSV in `sorgenti/dati/` e usa `designcraft-cli`). Sorgenti modificabili: `sorgenti/carte/*.designcraft`.
- **Componenti:** `stampa/sorgenti/componenti_gen/build.sh stampa/sorgenti stampa/playtest_v5` (usa `vectorcraft-cli`). Sorgenti modificabili: `sorgenti/<componente>/pagina_NN.vectorcraft` (con gli SVG accanto). I PDF attuali sono stati esportati da VectorCraft e uniti con PdfCraft; contengono come allegato il `.vectorcraft` di origine (voluto).
- **Dati:** `sorgenti/dati/` (CSV, `dati_stampa.md`, `decisioni_provvisorie.md`).

## Limiti e punti aperti

- Una stampante domestica può tagliare l'abbondanza esterna e le tacche: la linea di taglio dista 4,5 mm dal bordo del foglio (l'abbondanza arriva a 1,5 mm).
- **TE-18 Veste del Pellegrino / TE-20 Tunica del Viandante:** parlano di Locanda e Fonte sulla plancia, ma ora sono carte Imprevisto. Testo stampato com'era; da decidere con l'autore.
- **Divisori:** contenuto dedotto, nessun file lo definisce; il retro ripete il fronte.
- Ritratti di classe con dorso generico «Carta Classe»; colori di MIMI, Geronimo, boss e specie scelti dal designer.
- Carte Imprevisto: usano il testo della bozza dove esiste.
- **Inizia subito v5** ha ancora i vecchi nomi di classe, 5 specie e «Guerriero 6»: non distribuirlo o correggerlo.
- Gioco HTML e officina sono ancora sulla scala D20; il catalogo xlsx v2 non va usato per la stampa.
- Nessuna illustrazione: solo aree segnaposto.
- Colori convertiti in CMYK (PDF/X-4): possibili lievi differenze di resa. La Carta Aiuto (retro) è a 6,1 pt.
