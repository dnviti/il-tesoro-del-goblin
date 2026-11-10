# Kit di stampa del playtest v7

Il kit è in **produzione** e non va stampato senza richiesta. Si stampa **solo fronte**: i dorsi delle carte coperte sono in `carte_*_retri.pdf`, nella stessa posizione del loro fronte (non specchiati). Regole e componenti: `../regolamento/Spec_v7.md` (vincolante; §2 componenti, §9 Stati e tessere, §13 Carte Classe e Profezie, §14 contratto delle carte, §18 valori PLAYTEST).

- `playtest_v7/`: kit A4, 62 fogli (57 cartoncino + 5 carta comune). Ordine e carta in `playtest_v7/ordine_di_stampa.txt`.
- `playtest_v7_A3/`: kit A3, 34 fogli (31 cartoncino + 3 carta comune). Ordine e carta in `playtest_v7_A3/ordine_di_stampa.txt`.
- `sorgenti/`: generatori e dati. Il codice viene dalla v6 (`../../v6_08-11/stampa/sorgenti/`) adattato alla v7.

## Comandi (dalla radice del repo)

```
python3 v7/stampa/sorgenti/carte/genera_carte.py                    # carte A4
python3 v7/stampa/sorgenti/carte/genera_carte.py --formato A3        # carte A3
v7/stampa/sorgenti/componenti_gen/build.sh v7/stampa/sorgenti v7/stampa/playtest_v7              # componenti A4
v7/stampa/sorgenti/componenti_gen/build.sh v7/stampa/sorgenti/A3 v7/stampa/playtest_v7_A3 A3     # componenti A3
python3 v7/stampa/sorgenti/verifica_pdf.py                           # controlli A4 (--formato A3 per l'A3)
```

Servono `designcraft-cli`, `vectorcraft-cli`, `pdfcraft-cli` e poppler. `genera_carte.py` si ferma se un testo non entra nel suo riquadro (preflight di DesignCraft) o se una carta viola lo schema: si accorcia il testo nel CSV, mai il corpo. Un foglio di fronti senza nessun dorso (le Carte Classe in fondo al mazzo di classe) non ha la pagina dei retri: ogni pagina dei retri dice «coi fronti del foglio k». `gen.py` si ferma se una finestra delle rotelle mostra più di un valore. La prova di stampa di `gen.py` conta i fogli delle carte con `genera_carte.mazzi()` e `genera_carte.fogli_dorsi()`, quindi legge anche i CSV delle carte. `verifica_pdf.py` controlla che ogni pagina dei retri abbia dorsi e che ogni dorso stia nella cella del suo fronte, con gli ID di tutte le carte (CA…CG comprese).

**Provare dati nuovi senza toccare il kit:** `genera_carte.py --dati CARTELLA --uscita CARTELLA` legge i CSV da un'altra cartella e scrive PDF e progetti altrove; `build.sh <sorgenti_tmp> <pdf_tmp> A4 --dati CARTELLA` fa lo stesso per i componenti (anche A3); poi `verifica_pdf.py <pdf_tmp>`. Nessun numero di carte è fisso nel codice (mostri, fogli, divisori, prova di stampa).

**Illustrazioni:** `genera_carte.py` mette `sorgenti/arte/png/<id>.png` (stile e misure in `sorgenti/arte/STILE.md`; per le carte con più copie, Specie e Imprevisti, prima `<id>-<n>.png` della copia «n di m») nel riquadro dell'illustrazione di carte comuni, di classe, Carte Classe, Specie, Mostri e Imprevisti: riempie il riquadro centrata e ritagliata, la battuta va su una fascetta pergamena in fondo al riquadro (sui Mostri più piccola: 1 riga se entra, se no 2), le etichette rosse (PLAYTEST, PROVVISORIO, BOSS) e MAZZO su un cartellino pergamena, il PL resta sopra. Senza immagine per quella carta resta come prima (riquadro tinto). `--arte CARTELLA` legge le immagini da un'altra cartella, `--senza-arte` le ignora tutte. Carte Aiuto, Divisori e dorsi non hanno illustrazione.

## Dati delle carte (Spec v7 §14)

- **Carte comuni:** `sorgenti/dati/carte_comuni.csv`.
- **Carte di classe:** `sorgenti/dati/classi/<classe>.csv`, un file per classe (assaltatore, ricercatore, stregone, oracolo, giullare). Si uniscono in quest'ordine, poi per direzione A, B.
- **Colonne:** `id, tipo, nome, classe, direzione, pl, rarita, slot, testo, testo_situazionale, nota` più `battuta` facoltativa in fondo (`nota` non si stampa; niente colonna `fonte`).
  - `id`: `TE-nn`, `TI-nn`, `TM-nn` nel mazzo comune; `CA`, `CR`, `CS`, `CO`, `CG` da 01 a 10 nelle classi (01-05 direzione A, 06-10 direzione B). Gli id sono stabili (simulatore e regolamento li citano).
  - `tipo`: TE/TI/TM (anche Equipaggiamento/Incanto/Mappa).
  - `classe`: `Tutte le classi` nel mazzo comune (va bene anche `Comune`), il nome della classe nei file di classe.
  - `direzione`: A o B, solo per le carte di classe; il nome viene da `DIREZIONI` in `genera_carte.py` (Spaccatutto, Armadio a due ante, Ficcanaso, Mani lunghe, Fumo e fiamme, So tutto io, Ci ho preso!, Malocchio, Gioco di mano, Carta nella manica). Se la riga del tipo supera 49 caratteri, «EQUIPAGGIAMENTO» diventa «EQUIP.».
  - `pl`: solo per gli Equipaggiamenti (Comune 1, Rara 2, Leggendaria 3).
  - `testo_situazionale`: la riga «Se…» o «Profezia…», stampata in corsivo sotto il testo.
  - `nota` con «segnaposto»: la carta porta la scritta rossa SEGNAPOSTO (nessuna carta v7 ce l'ha).
  - `battuta` (facoltativa, ultima colonna di tutti i CSV di carte: comuni, classi, mostro, imprevisto, specie, Carte Classe): riga di colore in corsivo piccolo, centrata nel riquadro dell'illustrazione al posto del codice segnaposto, sopra il PL; al massimo 70 caratteri e 2 righe (oltre, lo script si ferma). Vuota o assente: niente. Sui boss con battuta «BOSS» diventa un'etichetta rossa.
- **Carte Mostro:** quante ne servono (id NE- liberi); abilità fino a ~200 caratteri (7 righe, 6 sui boss); nomi oltre 20 caratteri in corpo più piccolo. Il colore degli Imprevisti dipende dall'id (IM-01…04), non dal nome.
- **Sulla carta:** la direzione (lettera nel tondo del colore della classe e nome) apre la riga del tipo; il PL è in basso a destra nel riquadro dell'illustrazione. Il testo entra in circa 9 righe (~260 caratteri).

## Componenti (Spec v7 §2, §9, §13)

- **Plance eroe neutre (D14):** 4 uguali, senza classe e senza specie; 24 dischi uguali.
- **Rotelle:** PL 0-12 al posto di PE/livello, senza scritte di mazzetto; PV max ogni valore da 5 a 13.
- **Rotella della Profezia (R 13.5):** base quadrata 58 × 58 mm con la corona (1-6, P pari, D dispari, A alto, B basso) e disco Ø 52; A4 in `pedine.pdf` (foglio 2, sotto i Boss), A3 in `tessere_esplorazione.pdf`. 27 fermacampioni in tutto.
- **Tessere Stato:** 24: Rallentato 4, Occhio 2, Sussurro 2, Riflesso 2, Silenzio 4, Fede 2, Vantaggio 2, Svantaggio 3, Fermo 3 (R 9.7; una copia per fonte, al massimo 4: Silenzio 4 perché TI-23 Fermi tutti in 4 giocatori lo dà a 3 avversari e NE-37/NE-50 al quarto). Quante e quali stanno in `sorgenti/dati/stati.csv`. A4 in `segnalini.pdf` (foglio 2), A3 in `tessere_esplorazione.pdf` (in alto).
- **Tessere Usato:** 20 (anche come segnaposto delle carte giocate, R 4.4).
- **Pedine:** 13: 5 eroi con il Giullare (colore #a8407e, uguale al dorso del suo mazzo), MIMI, Geronimo e 6 sagome dei Boss (D20: 1 custode + 5 del mazzetto 3); nomi in `sorgenti/dati/pedine.csv` e `BOSS` di `gen.py`. A4: 2 fogli; A3 in `componenti_misti.pdf` (i 6 Boss in una fila).
- **Carte Classe TC-01…05:** testi della Spec §13; TC-04 Oracolo marcata PLAYTEST; riga in fondo «Mazzetto: 6 delle 10 carte di classe · Mano: 3 + 3».
- **Carte Aiuto:** «Il turno» (Inizio con la pesca, Muovi, Esplora, Fine, riquadro delle carte) e «Riepilogo» (scontro, ricompense, «?», sconfitta, mano, vittoria) secondo la Spec v7.
- **Divisori:** il numero di carte stampato si conta dai CSV.
- **Plancia:** la bozza `../idee/v7_bozza_mappa.svg` (D16), letta da `svg.py board()`; Sala del Tesoro della v6 con le corone delle rotelle del tavolo. La legenda della bozza non è sulla plancia.

## Stato del kit (10/11)

- Tutte le carte sono quelle della v7, nessuna è segnaposto: 63 carte comuni (25 Equipaggiamenti, 30 Incanti, 8 Mappe), 50 carte di classe e 5 Carte Classe, 8 Carte Specie, 48 Mostri (D20: mazzetto 1 26, mazzetto 2 16, 6 boss), 11 Imprevisti, 8 Carte Aiuto e 5 Divisori. Testi e regole delle carte: Spec v7 §14 (formule §14.5, glossario §15); revisione incrociata del 10/11 nelle `nota` dei CSV («Revisione 10/11»).
- Valori ancora da provare: Spec v7 §18; punti aperti con Desy e i loro default: Spec v7 §19.
- Le istruzioni di stampa dettagliate della v6 (`ISTRUZIONI_DI_STAMPA*.md`) non sono rifatte: ordine e carta stanno in `ordine_di_stampa.txt`; taglio e montaggio sono scritti sui fogli stessi.
