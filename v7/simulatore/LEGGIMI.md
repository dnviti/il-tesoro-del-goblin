# Simulatore v7

Monte Carlo di partite intere del playtest v7, sulle regole di `../regolamento/Spec_v7.md` (§16) e sui CSV di
`../stampa/sorgenti/dati/`. Solo libreria standard di Python 3.

```sh
# dalla radice del repository
python3 v7/simulatore/sim_v7.py --partite 2000 --seme 1                 # base v7
python3 v7/simulatore/sim_v7.py --partite 2000 --seme 1 --op1           # un'opzione di R 7.12
python3 v7/simulatore/sim_v7.py --partite 500 --giocatori 4 --uscita /tmp/r.txt
```

`--partite N` vale per ogni numero di giocatori (default 2, 3 e 4, come il simulatore v6; la v6 faceva in media
circa 10,6 round sulle tre tavolate). 2000 partite per tavolata girano in pochi secondi con `multiprocessing`.

## Opzioni

| Flag | Cosa cambia |
|---|---|
| `--op1` | OP-1: l'eroe attacca sempre per primo, contro ogni creatura (anche boss e custode) |
| `--op2` | OP-2: il danno del mostro è il suo ATT, senza dado (il tiro per colpire resta 2D6 + ATT ≥ AR) |
| `--op5` | OP-5: Duello, pari all'iniziativa: MOV più alto, poi si ritira (invece di «vince lo sfidante») |
| `--ar-v6` | confronto: AR dei mostri della v6 (8–11) invece di D19 (⌈AR × 0,75⌉, 6–9) |
| `--indizio-lv` | confronto: Indizio con D6 ≤ LV (v6) invece di D18 (D6 ≤ LV + 1) |
| `--dado-sommato` | N6: il «dado in più» si somma invece di tenere il migliore |
| `--chi-tira-non-risponde` | N1: chi tira non risponde al proprio tiro |
| `--penalita-meno` | N2: la penalità dei ritiri è sempre −n |

OP-3 e OP-4 sono diventate regole base (D19 e D18): restano solo come confronto (`--ar-v6`, `--indizio-lv`).
Se `carte_mostro.csv` avesse ancora le AR v6, il simulatore applica D19 da sé e lo scrive nel rapporto.

## File

| File | Contenuto |
|---|---|
| `sim_v7.py` | riga di comando, partite in parallelo, rapporto |
| `regole.py` | preparazione (§3), turno, movimento, esplorazione, Imprevisti, rifornimento delle «?», Fine |
| `stato.py` | eroe, mano massima (D8), pesca e riciclo, Stati, slot e PL, D6 della perdita (D7), sconfitta, Indizi e tesoro |
| `catena.py` | catene (D4/D9): giro orario, 1 carta per giocatore per catena, 2 per periodo, LIFO, tiri che aprono catene, momenti M0–M6 |
| `tiri.py` | tiri, ritiri con penalità cumulativa (D1), vantaggio, dado in più, Profezie (R 13.5) |
| `scontro.py` | iniziativa, colpo e danno, fuga, ricompense (D11), custode, Duello |
| `mostri.py` | abilità dei mostri: un aggancio per momento dello scontro (inizio, colpo, mancato, sconfitta, fuga, fine) |
| `effetti.py` | motore delle formule del §14.5, una funzione per codice di `effetti.csv` |
| `effetti.csv` | id carta → codice effetto + parametri (`k=v;k2`) |
| `abilita_mostri.csv` | id mostro → codice abilità + parametri; un mostro senza riga è `info` (contato nel rapporto) |
| `carte.py` | lettura dei CSV, valore delle carte per l'IA |
| `mappa.py` | plancia §17 (`python3 mappa.py` ricontrolla 64 esagoni, 115 collegamenti, Partenza→Cripta 4–8 passi) |
| `ia.py`, `ia_carte.py` | IA: preparazione, movimento, fuga, Duello, effetti automatici, poteri; carte da aprire e risposte |

Una carta nuova si aggiunge con una riga in `effetti.csv` usando un codice esistente; un codice nuovo va scritto in
`effetti.py` (funzione `f_<codice>`). Le carte senza riga valgono `info`: si giocano ma non fanno niente e si contano.
Lo stesso per i mostri con `abilita_mostri.csv` e `mostri.py`.

Revisione a occhio della mappatura (id, nome, testo stampato, codice usato), poi esce:

```sh
python3 v7/simulatore/sim_v7.py --verifica-mostri
python3 v7/simulatore/sim_v7.py --verifica-carte
```

## Cosa non è modellato (o è semplificato)

- IA semplice a punteggi: non bluffa, non conta le carte, risponde solo con annulla, parate, ritiri e (+N)/(−N).
  Le risposte vanno quasi tutte sui tiri (colpo, Indizio, danno, Trappola); il budget di 2 carte per periodo
  si spende soprattutto nel proprio turno.
- Effetti `info` (contati): CG-09 «guarda la mano» (la carta presa è a caso), CR-08 ripiego (scry del mazzo
  comune), CR-01 scry del mazzo comune, TI-29 riga del Duello; CR-04 e CR-06 hanno l'effetto «una volta per turno»
  solo informativo (mai usato).
- Effetti automatici (Forte Volontà, potere dello Stregone, CS-10, TE-10) si usano a pila vuota, prima di applicare
  il risultato del tiro, non a metà del giro delle risposte.
- Il potere del Ricercatore guarda il mazzetto Mostri del proprio PL quando si ferma su una «?»; CR-02/CR-05
  mettono le Trappole in fondo alle carte guardate. Lo scry si fa sempre a proprio vantaggio.
- Il 2° Equipaggiamento si gioca solo nel proprio turno al momento M0/M1/M5/M6; non si sostituisce un oggetto
  con uno di PL uguale o minore.
- Le Profezie si scelgono a caso (Alto sui propri tiri, valore esatto nel 15 % dei casi).
- Il tiro per piazzare o spostare MIMI non verifica le Profezie.
- Partita in stallo dopo 60 round (il regolamento non ha fine per tempo).
- Abilità dei mostri con una scelta (nota in `abilita_mostri.csv`): Borseggio galante (NE-13) scarta se ha una
  carta di valore basso o se il colpo diventerebbe letale; Elemosina (NE-40) paga con 2 carte di valore basso;
  Marca da bollo (NE-38) scarta sempre per tirare; Pedaggio reale (NE-28) scarta se la carta peggiore vale poco,
  altrimenti (+2) ATT. Gambe in spalla (NE-29) scatta solo se il colpo lo lascia a 1 PV esatto. Ninnananna (NE-34)
  dà Fermo anche all'eroe sconfitto. «Ogni avversario guarda la tua mano» (NE-35) è `info`. Il 1° attacco che
  colpisce il Conte Nebbiolo (NE-20) è quello di un eroe, non le carte di danno. Il rapporto segnala i codici che il
  motore non conosce.
