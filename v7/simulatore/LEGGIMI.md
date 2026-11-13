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
| `--mano-ia` | 13/11: l'IA sceglie le 5 carte iniziali di classe invece della mano predefinita (`carte.MANI_INIZIALI`) |

OP-3 e OP-4 sono diventate regole base (D19 e D18): restano solo come confronto (`--ar-v6`, `--indizio-lv`).
Se `carte_mostro.csv` avesse ancora le AR v6, il simulatore applica D19 da sé e lo scrive nel rapporto.

## File

| File | Contenuto |
|---|---|
| `sim_v7.py` | riga di comando, partite in parallelo, rapporto |
| `regole.py` | preparazione (§3), turno, movimento, esplorazione, Imprevisti, rifornimento delle tessere Esplorazione, Fine |
| `stato.py` | eroe, mano massima (D8), pesca e riciclo, bottino dei mostri, Stati, slot e PL, D6 della perdita (D7), sconfitta, Ristoro (D32), Indizi e tesoro |
| `catena.py` | catene (D4/D9): giro orario, 1 carta per giocatore per catena, 2 per periodo, LIFO, tiri che aprono catene, momenti M0–M6 |
| `tiri.py` | tiri, ritiri con penalità cumulativa (D1), vantaggio, dado in più, Profezie (R 13.5) |
| `scontro.py` | iniziativa, colpo e danno, fuga, ricompense (D11: bottino, Indizio), custode, Duello |
| `mostri.py` | abilità dei mostri: un aggancio per momento dello scontro (inizio, colpo, mancato, sconfitta, fuga, fine) |
| `effetti.py` | motore delle formule del §14.5, una funzione per codice di `effetti.csv` |
| `effetti.csv` | id carta → codice effetto + parametri (`k=v;k2`) |
| `abilita_mostri.csv` | id mostro → codice abilità + parametri; un mostro senza riga è `info` (contato nel rapporto) |
| `carte.py` | lettura dei CSV, valore delle carte per l'IA, mani iniziali predefinite (`MANI_INIZIALI`) |
| `mappa.py` | mappa 12×12 (D24, D25): geometria, base e fiori letti da `../stampa/sorgenti/dati/` (`fiori.csv`, `base12.csv`, `preset12.csv`), draft, preset, costi del terreno, movimento, Cripta. `python3 mappa.py` controlla che i 10 preset e 2000 draft a caso restino collegati |
| `ia.py`, `ia_carte.py` | IA: preparazione, movimento, fuga, Duello, effetti automatici, poteri; carte da aprire e risposte |

Una carta nuova si aggiunge con una riga in `effetti.csv` usando un codice esistente; un codice nuovo va scritto in
`effetti.py` (funzione `f_<codice>`). Le carte senza riga valgono `info`: si giocano ma non fanno niente e si contano.
Lo stesso per i mostri con `abilita_mostri.csv` e `mostri.py`.

## Mappa 12×12 (D24, D25, R 8.12)

La mappa in uso è `g.plancia` (`mappa.Plancia`), montata da `g.montaggio` ({spazio: (fiore, faccia, rotazione)}).
Default: **draft** (i 14 fiori divisi a caso, 7/4/3 a testa con 2/3/4 giocatori, gli avanzi li posano l'ultimo e il
penultimo; ognuno posa in turno in uno spazio libero, con faccia e rotazione a caso). `--preset` monta invece
«Strettoie». Le tessere Esplorazione (D29) stanno coperte direttamente sugli esagoni, senza segnaposto: 24 sulla mappa, a caso su
esagoni percorribili a ≥ 2 esagoni da ogni Partenza, una per esagono, e 12 in riserva. Alla Fine del turno, se sulla
mappa restano al massimo 6 tessere coperte, chi chiude il turno ne posa (prima la riserva, poi le usate rimescolate)
finché non ce ne sono 24 sulla mappa (contando anche quelle scoperte), con le stesse regole di posa e senza eroi, Cripta
o altre tessere sull'esagono.

- **Niente muri.** Si cammina ovunque non ci sia un ostacolo (bosco, rocce, case). Entrare costa sempre 1; uscire da un
  terreno accidentato (`accidentato` in `fiori.csv`/`base12.csv`, per ora l'acqua) costa 1 in più: con 1 MOV si entra in
  acqua, per uscirne ne servono 2. Mostri scoperti e Cripta con MIMI fermano come prima.
- **Cripta.** Al 3° Indizio e a ogni «Il tesoro cambia Cripta» (senza limite; ogni carta Mappa la ritira dopo il cambio) si tira 2D6 per la
  colonna e 2D6 per la riga. Su acqua resta; su una tessera Esplorazione resta e la tessera torna coperta nella riserva; su un ostacolo
  o una Partenza va sull'esagono percorribile più vicino senza Partenza, senza tessera e fuori da riga e colonna 1 (a pari
  distanza il più alto, poi il più a sinistra).
  Con D31 (13/11) la Cripta può anche essere tolta e rimessa e il custode si pesca dal mazzetto 3 quando compare: vedi «D31».
- **Carta Mappa.** Cambia solo i suoi 3 fiori (righe `cambio` di `preset12.csv`, con lo scambio se il fiore sta già in
  un altro spazio). Le tessere sugli spazi cambiati tornano nella riserva e chi ha giocato la carta ne posa altrettante dalla
  riserva sui fiori nuovi, su esagoni percorribili a ≥ 2 dalle Partenze (a caso, una per esagono). Gli eroi tornano
  sulla Partenza iniziale (niente D6 della perdita); la Cripta si sposta (stesso punto tirato) solo se ora è su un
  ostacolo. Uno scontro o un Duello in corso finisce senza vincitore né ricompense (esito `annullato`). Se TI-22
  (o TI-33, CR-15) toglie la Mappa in gioco, i 3 fiori tornano come nel montaggio.

IA: non gioca una Mappa durante il proprio scontro; la gioca (o toglie quella in gioco con TI-22/TI-33/CR-15) per
chiudere lo scontro di un avversario col custode, oppure a M2 se l'avversario di turno con 3 Indizi è sulla Cripta di
MIMI. Il rapporto conta movimento tirato e speso per turno, Cripta (tiri, spostamenti, tessere), rifornimenti delle tessere, cambi di mappa e scontri
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
- Il potere del Ricercatore guarda il mazzetto Mostri del proprio PL quando si ferma su una tessera Esplorazione; CR-02/CR-05
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

## Regole del 13/11 (mano, bottino, niente pesca)

Sostituiscono la parte mano/mazzetto di D22, R 3.6, R 3.7, R 12.1–12.3 e le ricompense di D11.

- **Mano iniziale**: 5 carte di classe scelte liberamente tra le 20; niente carte comuni. Le altre 15, mescolate e
  coperte, sono la **pila di classe** del giocatore (`Eroe.pila`; non tornano nella scatola). Non esiste più il
  mazzetto di classe da 10. TI-28 (`vera_volonta`, decisione del 13/11) prende 2 carte a caso, ognuna per conto suo,
  dalla scatola di una classe che nessuno gioca oppure dalla pila di classe di un avversario (una fonte con meno carte
  dà quel che ha); l'IA sceglie per ogni carta la fonte col valore medio più alto. Una carta tolta alla pila di un
  avversario finisce sempre negli scarti di quell'avversario, giocata o no (zona alla Fine, Equipaggiamento che lascia lo
  slot, scarto dalla mano per costo, mano massima o mill: `stato.agli_scarti`, memoria in `g.origine`); una dalla
  scatola, negli scarti di chi la possiede. Il testo stampato della carta è ancora da aggiornare. La mano predefinita per
  classe sta in **`carte.MANI_INIZIALI`** (classe → 5 id, controllati all'avvio: 5 carte distinte della classe;
  scelta approvata da Daniele). `--mano-ia` ignora la tabella e fa scegliere le 5 carte all'IA (`ia.mano_iniziale`:
  per valore, al massimo 4 della propria direzione); una classe senza voce nella tabella fa lo stesso.
- **Niente pesca a inizio turno**, nemmeno al primo, e niente pesca automatica dalla pila di classe. Le carte
  arrivano dal bottino, dalle carte che dicono «pesca» (dal mazzo comune) e dal Ristoro (D32: pesca 1 carta dopo ogni
  esito non vinto, sconfitta compresa). Dalla pila di classe pesca solo un testo che lo dice (CO-11, valore esatto della Profezia):
  `S.pesca(..., dalla_pila=True)`, con pila vuota → mazzo comune (R 12.6).
- **Bottino** (`stato.loot`): chi sconfigge un mostro dei mazzetti 1 e 2 rivela le prime 3 carte del mazzo comune, ne
  tiene 1 (l'IA la migliore, `ia._val_mano`) e mette le altre 2 coperte in fondo al mazzo comune. Niente bottino per
  boss (mazzetto 3), custode, mostro scappato o sparito (TI-41), scontro annullato, Duello. Vale anche per il mostro
  «sconfitto» senza Indizio da Elemosina (NE-40). Mano massima 10 (R 12.4): se è piena si scarta 1 prima di prendere.
  Se il mazzo ha meno di 3 carte si rimescolano in fondo le carte comuni di tutti gli scarti (R 12.6, le carte
  rimaste restano in cima); se ne restano ancora meno si guarda quel che c'è.
- **Forte Volontà** non è più una ricompensa dei mostri (nemmeno del mazzetto 2): si ottiene solo vincendo un Duello e
  con le carte che lo dicono. Il tiro Indizio alla vittoria (D6 ≤ LV + 1) è invariato.
- Stati: stessa meccanica; nei commenti «verticale» = dritto, «orizzontale» = di traverso.

Confronto (13/11, 1000 partite per tavolata, seme 1; «dopo» con le mani predefinite):

| | Round 2/3/4 giocatori | Turni a partita (≈ round × giocatori) | Mano alla Fine | Mano a 10 | Scontri vinti |
|---|---|---|---|---|---|
| Prima (3 di classe + 3 comuni, pesca a inizio turno, FV dal mazzetto 2) | 13,2 / 12,6 / 11,9 | 25,8 / 36,9 / 46,2 | 6,2–6,4 | 3,4–4,3 % dei turni | 49–50 % |
| Dopo (mani predefinite, bottino, niente pesca) | 13,8 / 12,1 / 11,1 | ≈ 27,6 / 36,3 / 44,4 | 2,5–2,6 | 0 % | 58–62 % |
| Dopo con `--mano-ia` | 16,8 / 14,6 / 13,7 | ≈ 33,6 / 43,8 / 54,8 | 3,1 | 0 % | 40–41 % |

Vittorie per classe, prima → dopo con le mani predefinite (2 / 3 / 4 giocatori): Assaltatore 53→57 / 36→42 / 26→32 %,
Ricercatore 46→42 / 32→30 / 21→22 %, Stregone 51→52 / 37→33 / 28→27 %, Oracolo 45→52 / 28→33 / 23→24 %,
Giullare 54→47 / 34→28 / 27→21 %. Con le mani predefinite il mazzetto 3 è il 3–5 % degli scontri (prima 22 %: il PL
resta basso, quindi si combattono soprattutto mostri dei mazzetti 1–2);
senza pesca la mano resta a 2–3 carte (vuota nell'8 % dei turni) e si gioca circa 0,9 carte per giocatore per round
(prima 1,2). L'Assaltatore è la classe avvantaggiata, il Giullare la più debole.

## D29 e D30 (13/11)

- **D29, tessere Esplorazione**: niente segnaposto «?»; le tessere stanno coperte direttamente sugli esagoni (24 sulla
  mappa, 12 in riserva), vedi «Mappa 12×12». Rifornimento alla Fine: con al massimo 6 tessere coperte si posano tessere
  fino a 24 sulla mappa (`stato.posa_tessere`).
- **D30 rivisto (13/11), PV e Danni**: l'eroe ha PV totali (5 di partenza, la Specie non ne dà, `Eroe.pv_tot` = 5 + gli
  «(+N) PV» degli Equipaggiamenti finché equipaggiati, per ora solo TE-23: `pv=1` in `effetti.csv`) e Danni subiti
  (`Eroe.danni`, partono da 0). È sconfitto quando i Danni raggiungono i PV totali e dopo la sconfitta i Danni tornano a
  0. «Togli N Danni» (le cure, ex «recuperi N PV») non scendono sotto 0, quindi i PV rimasti non superano i totali.
  Equipaggiare TE-23 alza i PV senza toccare i Danni (come curare 1); se l'oggetto esce dallo slot i PV calano, i Danni
  restano ma si fermano a PV − 1 (mai una sconfitta per aver perso un oggetto). `Eroe.pv` è la proprietà «PV rimasti»
  (PV totali − Danni): su di essa valgono le soglie «N PV o meno» delle carte e dell'IA. Il rapporto stampa i PV rimasti
  medi alla propria Fine.
- **N39, rifornimento delle tessere**: le tessere si posano a turno a partire da chi chiude il turno
  (`stato.posa_tessere`, ognuno con `ia.posto_tessera`, per ora a caso come al montaggio), solo su esagoni liberi
  percorribili a ≥ 2 dalle Partenze, senza eroi, Cripta o altre tessere. Dopo una carta Mappa le tessere tolte le posa
  per intero chi ha giocato la carta.

## D31, la sconfitta costa 1 Indizio (13/11, Daniele)

- **Regola**: chi è sconfitto (Danni = PV) perde anche 1 Indizio, se ne ha. Se è sconfitto da una creatura, dal custode, da
  una Trappola o da un effetto o un costo proprio, l'Indizio torna nella riserva; se è sconfitto da un altro eroe (una sua
  carta o un suo attacco fuori dal Duello) lo prende quell'eroe (limiti di mano e altri limiti invariati). Duello: lo
  sconfitto perde in tutto 1 solo Indizio, quello che il vincitore già prende (R 10.10), niente doppia perdita.
  Il D6 della perdita e il potere TC-01 dell'Assaltatore non cambiano.
- **Cripta e custode**: se dopo la perdita nessun eroe ha più 3 Indizi, la Cripta (con MIMI e custode) lascia la mappa;
  ritorna con un nuovo tiro 2D6 + 2D6 quando un eroe torna a 3 Indizi. La voce (R 10.6, +1 Indizio a ognuno degli altri)
  si sparge solo la prima volta (`g.tesoro_trovato`). **Il custode non si pesca più al montaggio**: i 6 boss sono tutti il
  mazzetto 3 (`g.custode` parte `None`). Quando compare la Cripta (`stato.prendi_indizio`) si pesca a caso 1 boss dal
  mazzetto 3 e diventa il custode a PV pieni (nuova `Creatura`); quando la Cripta se ne va (`stato.cripta_via`) il custode
  guarisce del tutto e torna nel mazzetto 3, che si rimescola; alla Cripta successiva se ne pesca uno nuovo. Mentre il
  custode è fuori, il mazzetto 3 ha 5 boss. Le ferite del custode restano solo tra uno scontro e l'altro con la stessa
  Cripta (anche quando il tesoro cambia Cripta).
- **Codice**: `stato.sconfitta(g, e, fonte)` (la `fonte` arriva da `danneggia`; Trappola e Speziale sono senza fonte),
  `stato.indizio_perso`, `stato.cripta_via` (anche da `scontro.duello` dopo il passaggio dell'Indizio) e il nuovo ramo di
  `stato.prendi_indizio`. Nel Duello `indizio_perso` non fa nulla (sconfitto e `scontro.duello`). Il rapporto stampa
  «Sconfitta con Indizio (D31)»: Indizi persi a partita (riserva / a un eroe) e Cripta tolta a partita. L'IA non conosce il
  nuovo rischio: non rinuncia al custode né evita le sconfitte per tenersi gli Indizi.
- **Risposte di Daniele (13/11)**: se un altro eroe tiene ancora 3 Indizi la Cripta resta; nel Duello il vincitore che
  arriva a 3 grazie all'Indizio preso tiene la Cripta; niente nuova voce quando la Cripta ritorna; se lo sconfitto è
  l'attaccante colpito dal Riflesso di un eroe (`danneggia(..., riflesso=False)`), l'Indizio va a chi ha il Riflesso (se
  il Riflesso colpisce una creatura nessun Indizio cambia). Nessun caso aperto.

Confronto (13/11, 1000 partite per tavolata, seme 1, mani predefinite; prima di D31 → con D31 e il custode pescato alla Cripta):

| | 2 / 3 / 4 giocatori |
|---|---|
| Round (partite finite) | 13,9 / 12,1 / 11,0 → 22,7 / 19,7 / 16,9 |
| Finite col custode (le altre in stallo a 60 round) | 99,9 / 100 / 100 % → 84,4 / 94,6 / 98,8 % |
| Round del 3° Indizio | 9,8 / 8,3 / 7,4 → 13,6 / 10,9 / 9,5 |
| Tiri della Cripta a partita | 1,31 / 1,61 / 1,85 → 2,11 / 2,72 / 2,96 |
| Cripta tolta a partita | 0 → 0,89 / 0,80 / 0,49 |
| Indizi persi a partita (riserva + eroe) | 0 → 6,80 / 7,60 / 7,70 (all'eroe 0,08 / 0,19 / 0,25) |

Vittorie per classe, prima → dopo (2 / 3 / 4 giocatori): Assaltatore 55→53 / 42→43 / 34→35 %, Ricercatore 45→37 / 29→28 /
20→22 %, Stregone 56→39 / 32→30 / 26→24 %, Oracolo 49→48 / 33→33 / 24→24 %, Giullare 46→35 / 31→24 / 21→19 %. Gli
Indizi persi sono quasi tutti alla riserva (sconfitte per creature e Trappole), quindi la partita si allunga di circa
9 / 8 / 6 round.

## D32, il Ristoro (13/11, Daniele)

- **Regola**: alla **Fine** del turno di ogni eroe che ha combattuto (mostro o Duello, qualunque esito) c'è il **Ristoro**.
  Si tira **sempre** il D6 della perdita (un Equipaggiamento può rompersi): vittoria, sconfitta, fuga dell'eroe, fuga del
  mostro. Poi: vinto un mostro dei mazzetti 1–2 → bottino (prime 3 carte comuni, ne tiene 1, 2 in fondo, come prima);
  ogni esito non vinto (sconfitta, fuga dell'eroe, il mostro scappa dopo 3 attacchi o sparisce) → pesca 1 carta comune.
  La sconfitta aggiunge: Partenza, Danni a 0, perde 1 Indizio (D31). Il vecchio D6 e la pesca della sconfitta **sono** il
  Ristoro: niente doppio tiro né doppia carta. Boss, custode e Duello vinti: solo il D6.
- **Duello**: il vincitore prende **1 carta a caso, coperta, dalla mano dello sconfitto** (mano massima 10; se la mano è
  vuota niente) più l'Indizio e la Forte Volontà (prima: la carta migliore dagli scarti). Lo sconfitto è sconfitto
  (Partenza, Indizio al vincitore); tutti e due fanno il Ristoro (D6), lo sconfitto pesca anche 1 carta.
- **Codice**: `stato.ristoro_segna(g, eroe, cosa, senza_d6)` (chiamata da `scontro.scontro`/`scontro.duello` e da
  `stato.sconfitta` quando l'eroe è in uno scontro) annota in `g.ristoro`; `stato.ristoro(g, eroe)`, chiamata da
  `regole.fine` dopo l'eventuale D6 di TI-26, tira il D6, fa il bottino e pesca. Il bottino non è più immediato.
  Anche lo sfidato di un Duello fa il Ristoro nella Fine del turno dello sfidante, **sfidante per primo** (confermato).
  Una sconfitta fuori da uno scontro (Trappola, carte, effetti) è anch'essa un Ristoro (D6 + pesca 1): alla tua Fine se
  è il tuo turno, subito (`stato.ristoro_di`) se è il turno di un altro eroe. Uno scontro o Duello chiuso dal cambio di
  mappa conta come non vinto: Ristoro con D6 + pesca 1 (per il Duello, a entrambi). Il mostro sparito (TI-41) vale come
  mostro scappato. TC-01 (Assaltatore) salta solo il D6 del Ristoro dopo una sconfitta (una volta per partita); la carta
  dice «puoi non tirare il D6 del Ristoro dopo una sconfitta». Il bottino si prende al Ristoro, a fine turno. Il
  rapporto stampa i Ristori, gli oggetti persi e le carte pescate nel Ristoro a partita.

Confronto (13/11, 1000 partite per tavolata, seme 1, mani predefinite; prima di D32 → con D32 prima dei casi chiusi):

| | 2 / 3 / 4 giocatori |
|---|---|
| Round (partite finite) | 22,7 / 19,7 / 16,9 → 24,8 / 22,4 / 19,8 |
| Finite col custode (le altre in stallo a 60 round) | 84,4 / 94,6 / 98,8 % → 83,9 / 92,6 / 97,3 % |
| Round del 3° Indizio | 13,6 / 10,9 / 9,5 → 13,9 / 11,0 / 9,3 |
| Ristori a partita | – → 37,1 / 44,8 / 49,0 (oggetti persi 23,3 / 28,5 / 31,1) |

Vittorie per classe, prima → dopo (2 / 3 / 4 giocatori): Assaltatore 53→47 / 43→37 / 35→31 %, Ricercatore 37→42 / 28→31 /
22→21 %, Stregone 39→39 / 30→27 / 24→21 %, Oracolo 48→46 / 33→33 / 24→26 %, Giullare 35→36 / 24→26 / 19→23 %. Il D6
a ogni scontro rompe molti oggetti (circa 23–31 per partita) e la partita si allunga di circa 2–3 round; il calo
dell'Assaltatore è probabilmente dovuto agli Equipaggiamenti persi (ipotesi, non misurata).

Dopo i casi chiusi (13/11 23:52; 500 partite per tavolata, seme 1): round 25,2 / 22,5 / 20,4 (finite col custode
79,6 / 93,2 / 98,4 %), Ristori 41,8 / 47,3 / 52,7 a partita (oggetti persi 24,9 / 28,4 / 31,6), 3° Indizio al round
14,2 / 11,2 / 9,6; Assaltatore 44,6 / 38,4 / 27,5 %.
