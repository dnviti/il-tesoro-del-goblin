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
| `--preset` | montaggio: preset «Strettoie» invece del draft |
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
| `mappa.py` | mappa 12×12 (D24, D25): geometria, base e fiori letti da `../stampa/sorgenti/dati/` (`fiori.csv`, `base12.csv`, `preset12.csv`), draft, preset, costi del terreno, movimento, Cripta. `python3 mappa.py` controlla che i 10 preset e 2000 draft a caso restino collegati |
| `ia.py`, `ia_carte.py` | IA: preparazione, movimento, fuga, Duello, effetti automatici, poteri; carte da aprire e risposte |

Una carta nuova si aggiunge con una riga in `effetti.csv` usando un codice esistente; un codice nuovo va scritto in
`effetti.py` (funzione `f_<codice>`). Le carte senza riga valgono `info`: si giocano ma non fanno niente e si contano.
Lo stesso per i mostri con `abilita_mostri.csv` e `mostri.py`.

## Mappa 12×12 (D24, D25, R 8.12)

La mappa in uso è `g.plancia` (`mappa.Plancia`), montata da `g.montaggio` ({spazio: (fiore, faccia, rotazione)}).
Default: **draft** (i 14 fiori divisi a caso, 7/4/3 a testa con 2/3/4 giocatori, gli avanzi li posano l'ultimo e il
penultimo; ognuno posa in turno in uno spazio libero, con faccia e rotazione a caso). `--preset` monta invece
«Strettoie». I 24 «?» vanno a caso su esagoni percorribili a ≥ 2 esagoni da ogni Partenza.

- **Niente muri.** Si cammina ovunque non ci sia un ostacolo (bosco, rocce, case). Entrare costa sempre 1; uscire da un
  terreno accidentato (`accidentato` in `fiori.csv`/`base12.csv`, per ora l'acqua) costa 1 in più: con 1 MOV si entra in
  acqua, per uscirne ne servono 2. Mostri scoperti e Cripta con MIMI fermano come prima.
- **Cripta.** Al 3° Indizio e a ogni «Il tesoro cambia Cripta» (senza limite; ogni carta Mappa la ritira dopo il cambio) si tira 2D6 per la
  colonna e 2D6 per la riga. Su acqua resta; su un «?» resta e il «?» con la sua tessera va nella riserva; su un ostacolo
  o una Partenza va sull'esagono percorribile più vicino senza Partenza, senza «?» e fuori da riga e colonna 1 (a pari
  distanza il più alto, poi il più a sinistra).
- **Carta Mappa.** Cambia solo i suoi 3 fiori (righe `cambio` di `preset12.csv`, con lo scambio se il fiore sta già in
  un altro spazio). I «?» (con le tessere) sugli spazi cambiati tornano nella riserva e se ne rimettono altrettanti sui
  fiori nuovi, su esagoni percorribili a ≥ 2 dalle Partenze (a caso, tessera nuova dalla riserva). Gli eroi tornano
  sulla Partenza iniziale (niente D6 della perdita); la Cripta si sposta (stesso punto tirato) solo se ora è su un
  ostacolo. Uno scontro o un Duello in corso finisce senza vincitore né ricompense (esito `annullato`). Se TI-22
  (o TI-33, CR-15) toglie la Mappa in gioco, i 3 fiori tornano come nel montaggio.

IA: non gioca una Mappa durante il proprio scontro; la gioca (o toglie quella in gioco con TI-22/TI-33/CR-15) per
chiudere lo scontro di un avversario col custode, oppure a M2 se l'avversario di turno con 3 Indizi è sulla Cripta di
MIMI. Il rapporto conta movimento tirato e speso per turno, Cripta (tiri, spostamenti, «?»), cambi di mappa e scontri
annullati.

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
- Carte nuove del 10/11 (D22: classi XX-11..20, TM-09, TE-26..31, TI-31..41), approssimazioni (dettaglio nella
  colonna `nota` di `effetti.csv`):
  - «Guarda la mano / il mazzo comune / le tessere» è informativo: CG-11, CR-11 (N + 1), CR-14 (tessere), CR-16,
    CR-18 (la carta presa è a caso), CR-19, CR-20, CS-17.
  - Sacrifici non usati dall'IA: CA-15 (3 Danni), CA-17 (3 Danni), CA-20 (prenderne 2), CS-12 (D6 + 2 Danni), TE-30
    (fuga). TE-27 si sacrifica solo sul tiro d'Indizio o contro il custode; CG-17 a M6 contro il leader con 2 Indizi;
    CS-16 solo contro un Incanto che ha te come bersaglio.
  - Scelte fisse: CG-15 scarta se ha una carta di poco valore (altrimenti perde 2 PV); CG-18 scarta sempre; CG-19
    non rifà su di sé; CG-20 l'avversario scarta solo con 6 carte o più, altrimenti dà la peggiore; TI-35 senza
    lo scambio; TI-38 ognuno passa le sue 2 carte peggiori; CS-19 mette 6 (o 1) sul dado peggiore.
  - Equipaggiamenti «quando…»: CG-12 tira solo con 3 PV o più e un bersaglio; CO-14 il D6 ritirato vale solo per la
    Profezia (il tiro resta); TE-26 al posto del tiro solo se per colpire serve 8 o più su 2D6; CA-13 e TE-28
    mettono i Danni sul prossimo attacco del turno; CA-15 usa il (+3) quando basta a colpire e paga la AR del
    parametro `archibugio=N`; CO-15 paga `prof_paga=N` PV solo se ne ha più di N + 1.
  - Effetti «una volta per turno» degli Equipaggiamenti valgono fino alla propria Fine (come CS-10).
- Righe «Se» degli Equipaggiamenti con una statistica (§14.5, bilanciamento dell'11/11): `ar_lv3=N` (AR contro gli
  attacchi delle creature di LV 3 o più, come TE-22), `ar_boss=N` (contro boss e custode), `ar_pv2=N` (AR con 2 PV
  o meno, vale anche nel Duello), `dmg_lv3=N` (Danni ai tuoi attacchi contro le creature di LV 3 o più).

## Risultati (11/11, 500 partite per tavolata, seme 1)

Gli Equipaggiamenti di classe nuovi (XX-11..20) alzavano il PL senza dare difese: gli eroi arrivavano prima al
mazzetto 3 e la partita si allungava di circa 4 round. Senza di loro la partita tornava a circa 11,0/10,4/10,2
round. Tolti uno alla volta (2000 partite), solo i PL 3 pesavano da soli (CA-15 −0,6 round, CO-15 −0,5): il peso
veniva dall'insieme. Una (+1) ATT su tutti quasi non cambiava niente; una (+1) AR sì. Gli effetti sono stati
rivisti di conseguenza (elenco in Spec §19).

| | Round 2/3/4 giocatori | Scontri persi | Mazzetto 3 | Morti a partita (4 g.) | Vittorie per classe (quota equa = 1) |
|---|---|---|---|---|---|
| Prima (carte di D22) | 14,6 / 13,9 / 14,1 | 32 % | 22–23 % | 12,8 | da 0,75 (Oracolo) a 1,15 |
| Dopo il bilanciamento | 11,1 / 10,5 / 10,2 | 22–24 % | 19–21 % | 7,2 | da 0,89 a 1,11 (2000 partite) |

## Regole del 12/11 sera

Nessun Equipaggiamento gratis a inizio partita. Primo giro (round 1): niente Duelli e l'IA non gioca carte contro un
avversario. Nello scontro con un mostro l'eroe ha al massimo 3 attacchi: se il mostro è vivo il suo turno lo fa
scappare (niente premi, tessera tra le usate, carta in fondo; le abilità «a fine scontro» non scattano; il custode non
scappa mai).
