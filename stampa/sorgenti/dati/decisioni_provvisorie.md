# Decisioni provvisorie per il kit di playtest

Regole di riferimento: bozza Word `Regolamento_Tesoro_del_Goblin_bozza.docx` (2/11/2026 22:06), letta dal commit `2aa7f84` (`v2/Regolamento_Tesoro_del_Goblin_bozza.docx`). Le citazioni sono copiate dal documento. Il confronto con il PDF v5 (`v2/Regolamento_base_v5_stampa.pdf`) è stato fatto sul testo del PDF e sullo script `v2/regolamento_stampa/docx/edit_html.py`, che elenca tutte le modifiche applicate al regolamento v5 per ottenere la bozza.

Aggiornamento: la bozza del **3/11** (stesso corpo del testo, più le note e i 14 commenti dell'autore) sostituisce quella del 2/11 in `regolamento/`. Dal 3/11 il kit adotta solo le regole che l'autore ha deciso: pareggio dell'iniziativa (D-4), mazzetto per livello (D-3), 3 Indizi, Forte Volontà al posto di Ispirazione, Incanto al posto di Incantesimo, niente critici. Tutte le modifiche ai testi stampati sono nella sezione 3. Le altre proposte dell'autore (5 classi, plancia 12 × 12, nuova formula del danno, `carte nuove.xlsx`, bestiario) non sono nel kit.

Nella bozza i punti con evidenziatore giallo sono 6 run: i 4 «Da decidere» e due «da confermare» (8 Tessere Specie; Stregone con 1 comune in più). Qui sotto: i 4 «Da decidere» (sezione 1), tutto il resto che cambia la stampa (sezione 2) e le modifiche ai testi stampati dovute alla bozza del 3/11 (sezione 3).

## 1. I 4 punti «Da decidere»

Marcatore da stampare dove la scelta compare su un componente: la parola **PROVVISORIO** (maiuscolo, tra parentesi o dopo il testo, come indicato sotto). Nel regolamento si usa lo stesso marcatore; sui componenti serve solo dove il testo è stampato (tessera Yumaniano). Dal 3/11 D-3 e D-4 non sono più provvisori: le ha decise l'autore.

### D-1 Direzione del draft

- **Passo della bozza** (Preparazione, punto 6): «Draft: ognuno riceve 5 comuni, ne tiene 1 e passa le altre a destra finché finiscono. Da decidere: sempre a destra o alternando destra e sinistra.»
- **Elenco «Punti da decidere»**: «Draft: si passa sempre a destra o si alterna destra e sinistra come in Magic?»
- **Opzioni offerte dalla bozza**: (a) sempre a destra; (b) alternando destra e sinistra (come in Magic).
- **Scelta: (a) sempre a destra.** Perché: è già scritto nel testo, non serve un promemoria sul giro dei passaggi.
- **Bozza del 3/11**: l'autore scrive «le carte generiche vengono scelte in senso orario ogni giocatore vede un pull di 5 carte e ne sceglie 1 passando il mazzetto delle restanti al suo giocatore alla sua destra finché non avranno tutti 10 carte in mano». Conferma una direzione fissa (niente alternanza), ma il testo è ambiguo: nella bozza «in senso orario» vuol dire passare a **sinistra** («Tocca al giocatore a sinistra»), mentre l'autore scrive «alla sua destra». Resta PROVVISORIO «a destra» finché l'autore non chiarisce.
- **Dove compare in stampa**: solo nel regolamento. Nessuna carta, tessera o Carta Aiuto riporta la direzione.
- **Testo da stampare** (regolamento, passo 6): «Draft: ognuno riceve 5 comuni, ne tiene 1 e passa le altre a destra finché finiscono. (PROVVISORIO: sempre a destra.)»

### D-2 Bonus del Yumaniano

- **Passo della bozza** (tabella «Le specie»): «Yumaniano | Da decidere: bonus della specie.» Elenco: «Yumaniano: manca il bonus della specie. Nano e Orco sono stati tolti; le Tessere Specie passano da 10 a 8 (2 per specie)?»
- **Opzioni offerte dalla bozza**: nessuna. Valori già scritti nel repo (commit `2aa7f84`):
  - (a) **+1 AR e +1 a una statistica a scelta**. È il valore di `v2/Il_Tesoro_del_Goblin_gioco_v2.html` riga 438 (`Yumaniani: { tag: 'Aasimar', fixed: { ar: 1 }, free: 1 …`, «+1 AR e +1 a una statistica a scelta»), di `officina/motore.js` riga 21 e del Leggimi del catalogo v2 («Yumaniani +1 AR e +1 a scelta», 27/10). Compatibile con le altre specie: Umano +1 MOV e +1 a scelta, Elfo +2 a scelta.
  - (b) +1 PV e +1 a scelta (solo nel gioco v1 del 21/10): incompatibile con le regole attuali, perché i PV crescono solo con i livelli.
  - (c) +2 a una statistica a scelta, come l'Elfo: identico all'Elfo, quindi la specie sarebbe senza identità.
- **Scelta: (a) +1 AR e +1 a una statistica a scelta.** Perché: è l'unico valore già presente nel gioco/simulatore attuale, non cambia nessuna regola e non richiede un nuovo bilanciamento.
- **Dove compare in stampa**: 2 Tessere Specie Yumaniano (`tessere_specie.csv`, SP-07 e SP-08) e la tabella «Le specie» del regolamento.
- **Testo da stampare**: «+1 AR e +1 a una statistica a scelta (PROVVISORIO)».

### D-3 Mazzetto dei mostri: per livello o per Indizi (DECISO il 3/11)

- **Passo della bozza** (Esplorare, riga «Tessera rossa: Mostro»): «Gira la prima carta del mazzetto del tuo livello (livello 1-2: mazzetto 1; 3-4: mazzetto 2; 5: mazzetto 3, i boss). […] Da decidere: il mazzetto si sceglie dal livello o dagli Indizi (0: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3).»
- **Elenco «Punti da decidere»**: «Mazzetto dei mostri: si sceglie dal livello dell'eroe (com'è scritto ora) o dagli Indizi che ha (0 Indizi: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3)? Con il livello il mazzetto 2 non esce quasi mai.»
- **Opzioni offerte dalla bozza**: (a) dal livello dell'eroe (1-2 → mazzetto 1; 3-4 → mazzetto 2; 5 → mazzetto 3); (b) dagli Indizi (0 → 1; 1 → 2; 2 → 3).
- **Scelta: (a) dal livello, come scritto ora.** Perché: è già il testo di regolamento, Carta Aiuto, tessera «?» e carte Mostro («LV 1-2», «LV 3-4», boss); il problema («il mazzetto 2 non esce quasi mai») si valuta al tavolo senza stampare nulla di diverso.
- **Bozza del 3/11**: l'autore conferma il livello: «il giocatore che incontra un nemico gira la carta mostro dalla lista dei mostri di fascia 1+livello del giocatore». Non è più PROVVISORIO. La formula «fascia 1+livello» non coincide alla lettera con le fasce 1-2 / 3-4 / 5 della bozza: il kit tiene le fasce stampate.
- **Dove compare in stampa**: Carta Aiuto (retro, riga «Rossa: mazzetto del tuo livello (1-2 · 3-4 · 5)»), identica alla bozza; nessun'altra modifica. Le 24 carte Mostro restano divise in mazzetto 1 (13), mazzetto 2 (8), boss (3).
- **Testo da stampare** (regolamento): «Gira la prima carta del mazzetto del tuo livello (livello 1-2: mazzetto 1; 3-4: mazzetto 2; 5: mazzetto 3, i boss). Scontro, oppure fuga (pagina 10).» Senza marcatore.

### D-4 Pareggio dell'iniziativa (DECISO il 3/11)

- **Passo della bozza** (Lo scontro, punto 1): «Chi attacca per primo. Tu e il nemico tirate 1 D6 a testa: chi fa di più attacca per primo. Per il mostro tira il giocatore alla tua destra. Da decidere: in caso di pareggio (proposta: si ritira).»
- **Elenco «Punti da decidere»**: «Chi attacca per primo: se il tiro di 1 D6 è pari? Proposta: si ritira.»
- **Scelta fino al 2/11**: si ritira (PROVVISORIO), la sola proposta della bozza.
- **Decisione dell'autore** (commento alla bozza del 3/11): «in caso di pareggio contro i nemici vince l’attaccante - contro il boss in caso di pareggio il boss avrà priorità contro altro giocatore si veda il valore MOV più alto se anche questo si trovasse in pareggio inizia il giocatore che aveva il turno (l’attaccante)». «Attaccante» = il giocatore che ha il turno (definizione dell'autore nella parte sui giocatori); contro un mostro è quindi l'eroe. Vale anche per il Duello (tra giocatori).
- **Dove compare in stampa**: regolamento (scontro e Duello) e Carta Aiuto, retro, sezione Scontro: due righe sotto «Per il mostro tira chi ti siede a destra» (campo `retro_scontro` in `carte_aiuto.csv`; il campo separato `retro_pareggio`, stampato in rosso, è stato tolto).
- **Testo da stampare** (Carta Aiuto): «Pareggio: col mostro vince chi attacca, col boss il boss.» / «Tra giocatori vince il MOV più alto, poi chi ha il turno.» Nel regolamento: «In caso di pareggio: contro un mostro vince chi attacca, contro il boss vince il boss; tra giocatori vince chi ha il MOV più alto e, se anche questo è pari, chi ha il turno.»

## 2. Altre differenze tra bozza e PDF v5 rilevanti per la stampa

Fonte: `edit_html.py` (elenco completo delle sostituzioni) più confronto del testo.

| Tema | PDF v5 | Bozza (da seguire) | Effetto sulla stampa |
|---|---|---|---|
| Nomi delle classi | Guerriero, Ladro, Mago, Oracolo | **Assaltatore** (ex Guerriero), **Ricercatore** (ex Ladro), **Stregone** (ex Mago), Oracolo invariato | Nome sulle 4 Carte Classe («Classe: Assaltatore»…), riga delle classi in fondo a ogni carta di classe («Assaltatore - Oracolo»), miniature, dorsi, Divisori. Articolo: «un Assaltatore, un Ricercatore, uno Stregone, un Oracolo». Fatto in `carte_classe*.csv`. |
| Specie | 5 specie: Umano, Elfo, Nano, Orco, Sanguar | 4 specie: Umano, Elfo, Sanguar, **Yumaniano** (Nano e Orco tolti) | Tessere Specie |
| Tessere Specie | 10 | **8** (2 per specie, «da confermare») | `tessere_specie.csv` (8 righe) |
| Bonus specie | Umano +1 MOV e +1 a scelta; Elfo +2 a scelta; Nano +1 a due statistiche diverse a scelta; Orco +2 ATT; Sanguar +2 MOV (sono non morti) | Umano +1 MOV e +1 a una statistica a scelta; Elfo +2 a una statistica a scelta; Sanguar +2 MOV (sono non morti); Yumaniano: da decidere (vedi D-2). Nota invariata: «Bonus a scelta: ATT, MOV o AR. I PV crescono solo con i livelli.» | Testo sulle tessere |
| Chi attacca per primo | «Attacchi tu per primo»; Duello: «Attacca per primo chi ha mosso» | 1 D6 a testa, vince il più alto; per il mostro tira il giocatore alla destra; Duello: stessa regola | Carta Aiuto (retro: «Chi attacca per primo: 1 D6 a testa, vince il più alto. Per il mostro tira chi ti siede a destra.»). Le abilità «Agguato: attacca per primo» (NE-14 Gnoll cacciatore, NE-27 Mimic ancestrale) restano sulle carte; come si combinano con il tiro di iniziativa non è scritto nella bozza. |
| Fuga dal boss | «Dal boss fugge solo il Ladro» | «Dal boss fugge solo il Ricercatore» | Solo regolamento; la Carta Classe del Ricercatore («Puoi fuggire da ogni scontro e fuggendo non arretri») invariata |
| Carte Classe: Assaltatore | PV 6 all'inizio (Inizia subito: «Guerriero 6»); la carta TC-01 nel JSON ha ancora «(+2) PV» e «(-2) AR» | La bozza: «nel regolamento ha +1 PV (parte con 6) e la sua Ispirazione toglie 1 AR al nemico invece di 2 […] da confermare» e tra i «da correggere dopo»: «la Carta Classe dell'Assaltatore (PV e Ispirazione)» | **TC-01 stampata con «(+1) PV» e «(-1) AR»** (`carte_classe_ritratto.csv`, colonna `corretto_dalla_bozza`) |
| TI-12 Parola di Confusione | «(tira due D20 e vale il peggiore)» | Tra i «da correggere dopo»: «la TI-12 Parola di Confusione («tira due D20»)» | **Stampata con** «svantaggio (tira due volte i 2D6 e vale il totale peggiore)»: formula presa dal paragrafo «Vantaggio e svantaggio» della bozza. Corretto in `carte_comuni.csv`. |
| Stregone | «il Mago le sue 4 e 1 comune in più» | «lo Stregone le sue 4 e 1 comune in più da confermare» | Solo regolamento (il mazzo Stregone ha 4 carte; non cambia le carte da stampare) |
| Oracolo e Locanda | Carta Classe TC-04: «Il potere si ricarica quando ti fermi in una Locanda.» | «Lo togli, e il potere torna pronto, quando peschi una Locanda dal sacchetto» e «metti un cubetto Durata sulla Carta Classe» | TC-04 allineata («quando peschi una Locanda dal sacchetto»). Aggiunta non richiesta dalla bozza nei «da correggere»: da confermare. |
| Esempio di scontro | Lia gioca il Guerriero | Lia gioca l'Assaltatore; esempio con il lancio di iniziativa | Solo regolamento |
| Conteggi | 121 carte | Invariati, tranne Tessere Specie 10→8 | Vedi `dati_stampa.md`, sezione 1 |

### Incoerenze trovate, non risolte (nessuna istruzione nella bozza)

- **TE-18 Veste del Pellegrino** e **TE-20 Tunica del Viandante**: i testi v2 parlavano di Locanda/Fonte come caselle, ma ora sono carte Imprevisto. Corretti dal collaudo del 5/11 (sezione 5, C-1 e C-2); TE-20 è una scelta di playtest ([PLAYTEST]).
- **Inizia subito v5** (`Inizia_subito_v5_stampa.pdf`) ha ancora Guerriero/Ladro/Mago, 5 specie e «Guerriero 6» PV: non è allineato alla bozza. Se si distribuisce nel playtest, correggerlo o non darlo.
- **Catalogo xlsx v2** (`Catalogo_carte_v2.xlsx`): Leggimi e colonna Difesa sulla scala D20; non usarlo per la stampa.
- **Carte Imprevisto**: `xlsx_v2.py` dice «L'Oracolo ricarica il ritorno in vita», bozza/PDF v5 «L'Oracolo ricarica il suo potere», e «Riprendi 1 equipaggiamento» contro «Riprendi in mano 1 equipaggiamento». In `carte_imprevisto.csv`: `testo` = `IMP` (come richiesto), `testo_bozza` = versione della bozza. Usarne una sola.
- **Divisori**: nessun file ne definisce il contenuto (vedi `dati_stampa.md`, sezione 2).
- **Carte Nemico** `Carte_Nemico_v2.pptx`: le carte Boss riportano solo «MIMI: vinci la partita»; la ricompensa del mazzetto 3 (1 indizio, sali di livello, Ispirazione; dal 3/11 stampata «1 indizio · +1 livello · Forte Volontà») è nella colonna `ricompensa_se_mazzetto_3`.
- **Nome «Occhio dello Stregone»** (TI-06) coincide con la nuova classe; **«Cimitero dei Maghi»** (TM-05) è un nome di luogo: non rinominare.

## 3. Modifiche dalla bozza del 3/11

Fonte: commenti di «Ale Desi» e blocco «MODIFICHE FATTE DAL DESI» nella bozza del 3/11. Regole adottate:

- **Pareggio dell'iniziativa**: vedi D-4.
- **Mazzetto per livello**: vedi D-3 (nessun testo stampato cambia).
- **3 Indizi** per trovare il tesoro («Gli indizi devono essere 3 per poter scoprire e raggiungere il tesoro»). Segnalini Indizio: 16 (erano 12; vedi C-5 nella sezione 5).
- **Forte Volontà** al posto di Ispirazione («Sostituire a ispirazione»): «Non può accumularsi - permette di ritirare 1D6». Il nome cambia ovunque; dove una carta dà un uso diverso (TC-01) il testo della carta resta.
- **Incanto** al posto di Incantesimo («sostituisce la parola incantesimo»), anche al plurale («Incanti») e in minuscolo dentro i testi. Nessun nome proprio conteneva la parola.
- **Niente critici** («No niente critici»): tolta la regola del doppio 6 / doppio 1. Le abilità e le carte che parlano di un 6 sul dado (NE-21, NE-26, TI-11) non sono critici e restano.

Testi stampati cambiati (vecchio → nuovo):

| File | Righe | Campo | Vecchio → nuovo |
|---|---|---|---|
| `carte_comuni.csv` | 24 (TI-01…24) | `tipo_nome` | «Incantesimo» → «Incanto» |
| `carte_comuni.csv` | TM-07 | `testo` | «gli Incantesimi che infliggono Danni» → «gli Incanti che infliggono Danni» |
| `carte_comuni.csv` | TI-01 | `testo` | «con il prossimo incantesimo» → «con il prossimo incanto» |
| `carte_comuni.csv` | TI-08 | `nome` | «Scintilla d'Ispirazione» → «Scintilla di Volontà» (nome scelto per la stampa: «Scintilla di Forte Volontà» va su due righe e non entra nel titolo) |
| `carte_comuni.csv` | TI-08 | `testo` | «Se non hai l'Ispirazione, la ottieni.» → «Se non hai la Forte Volontà, la ottieni.» |
| `carte_comuni.csv` | TI-21 | `testo` | «ottieni (1) Ispirazione» → «ottieni la Forte Volontà» (non si accumula: niente «(1)») |
| `carte_comuni.csv` | TI-23 | `testo` | «non può giocare carte Incantesimo» → «non può giocare carte Incanto» |
| `carte_classe.csv` | 19 (TI-25…40, con le doppie) | `tipo_nome` | «Incantesimo» → «Incanto» |
| `carte_classe.csv` | TE-04 (×2) | `testo` | «un D6 di un incantesimo di Danno o di cura» → «un D6 di un incanto di Danno o di cura» |
| `carte_classe.csv` | TE-13 | `testo` | «un tuo incantesimo infligge» → «un tuo incanto infligge» |
| `carte_classe.csv` | TE-14 | `testo` | «con un incantesimo» → «con un incanto» |
| `carte_classe_ritratto.csv` | TC-01 | `testo` | «ti dà l'Ispirazione» → «ti dà la Forte Volontà» |
| `carte_mostro.csv` | NE-14…21 (8) | `ricompense` | «1 indizio · 1 punto esperienza · Ispirazione» → «… · Forte Volontà» |
| `carte_mostro.csv` | NE-26…28 (3) | `ricompensa_se_mazzetto_3` | «1 indizio · sali di livello · Ispirazione» → «1 indizio · +1 livello · Forte Volontà» («sali di livello» accorciato: con «Forte Volontà» la riga andava a capo e usciva dal riquadro) |
| `carte_aiuto.csv` | AI-01…04 | `retro_scontro` | tolta «Doppio 6 = colpo doppio · doppio 1 = mancato.»; aggiunte, dopo «Per il mostro tira chi ti siede a destra.», «Pareggio: col mostro vince chi attacca, col boss il boss.» e «Tra giocatori vince il MOV più alto, poi chi ha il turno.» |
| `carte_aiuto.csv` | AI-01…04 | `retro_pareggio` | «Pareggio: si ritira (PROVVISORIO).» → colonna tolta (la regola è in `retro_scontro`) |
| `carte_aiuto.csv` | AI-01…04 | `retro_ricompense` | «Mazzetto 2: + Ispirazione», «… + livello + Ispirazione», «Duello: … + Ispirazione» → «Forte Volontà» |
| `carte_aiuto.csv` | AI-01…04 | `retro_vittoria` | «2 Indizi → gli altri prendono 1 Indizio …» → «3 Indizi → gli altri prendono 1 Indizio …» |
| `divisori.csv` | DV-02 | `titolo`, `contenuto_playtest` | «INCANTESIMO», «Incantesimi comuni» → «INCANTO», «Incanti comuni» |
| `segnalini.csv` | SG-03 | `nome` | «Ispirazione» → «Forte Volontà» (etichetta dei 4 segnalini) |
| `segnalini.csv` | SG-01 | `note` | «2 caselle «al 2°: tesoro!»» → «3 caselle «al 3°: tesoro!»» |
| `componenti_gen/parts_stampa.py` | scheda eroe | caselle | Indizi: 2 caselle «al 2°: tesoro!» → 3 caselle «al 3°: tesoro!»; «Ispirazione» → «Forte Volontà» (1 casella, «una sola») |
| `componenti_gen/gen.py` | segnalini | intestazione e piè | «4 Ispirazione», «1 di Ispirazione» → «4 Forte Volontà», «1 di Forte Volontà» |
| `carte/genera_carte.py` | Carta Aiuto | stile | tolto lo stile rosso `RiepProvv` del pareggio; colore del tipo rinominato «Incanto» |

Carta Aiuto, retro: tolta la riga dei critici e la riga rossa «si ritira», aggiunte le due righe del pareggio: il numero di righe resta 7 nella sezione Scontro, il testo resta a 6,1 pt e il preflight di DesignCraft non segnala testo in eccesso.

## 4. Proposte dell'autore non ancora in stampa (5/11)

Fonte: `carte/originali/Carte_nuove_2026-11-05.xlsx`, foglio `Foglio5` («Classi»), aggiunto dall'autore la sera del 5/11 (file «carte nuove_aggiornate sulla base del nuovo regolamento semi ufficiale.xlsx»; gli altri 4 fogli sono identici a «carte nuove.xlsx» del mattino). Testi copiati come sono. Nessuno è stampato: le Carte Classe TC-01…04 restano quelle del kit.

| Classe (Foglio5) | Effetto (testo dell'autore) | Differenza dalla carta stampata |
|---|---|---|
| «Assaltatore ( guerriero )» | «La tua pedina è un Assaltatore per il resto della partita  una sola volta per partita morire non ti costa equipaggiamento» | TC-01 dà (+1) PV e la Forte Volontà a ogni scontro vinto, da spendere per (-1) AR al nemico; la proposta toglie entrambe e protegge l'equipaggiamento dal tiro di perdita, una volta per partita. |
| «Stregone (mago)» | «La tua pedina è uno Stregone per il resto della partita  puoi ritirare  1d6 o scegliere ti farlo ri tirare ad un avversario  in tutta la partita» | TC-03 permette di ritirare i propri dadi fino a (2) volte **per turno**; la proposta è 1 D6, anche di un avversario, e sembra **una volta per partita** («in tutta la partita», formulazione da chiarire). |
| «Oracolo (chirico / sacerdote )» | «La tua pedina è un Oracolo per il resto della partita  se sconfitto invece di morire resti con 1pv ( si può usare una sola volta per partita )» | TC-04 fa tornare in vita con (3) PV continuando lo scontro e si ricarica con la Locanda; la proposta resta a 1 PV, una sola volta per partita, senza ricarica. |
| «Ricercatore ( una sorta di artefice )» | «La tua pedina è un Ricercatore  per il resto della partita  puoi rivelare una carta imprevisto sul tabellone visibile solo a te» | TC-02 dà (+2) MOV e la fuga da ogni scontro senza arretrare; la proposta è un potere di informazione. Nel kit gli Imprevisti non stanno sul tabellone (si pescano dopo una tessera blu dal sacchetto): così com'è scritto non si applica. |

Punto aperto: il Ricercatore come «artefice» (anche nel commento alla bozza del 3/11, dove l'Impostore/Fuggiasco «corrisponde al ladro») non corrisponde più al mazzo di classe stampato, che è quello dell'ex Ladro: TE-15 Pugnale Sottile, TI-37 Colpo alle Spalle, TI-38 Fortuna del Furfante, TI-39 Passo Felpato, TI-40 Lancio di Coltello. Da chiarire con l'autore prima di cambiare TC-01…04 o il mazzo del Ricercatore.

## 5. Correzioni del collaudo 5/11

Fonte: prova di gioco a tavolino sul kit (agente «Collaudo», `local://collaudo.md`). Le correzioni sono già in `sorgenti/dati/*.csv` e nei PDF rigenerati. Marcate **[PLAYTEST]** le scelte non dedotte da un testo dell'autore.

| ID | File | Carta/campo | Vecchio → nuovo |
|---|---|---|---|
| C-1 | `carte_comuni.csv` | TE-18 Veste del Pellegrino, `testo` | «Finché è equipaggiata ottieni (+1) MOV; quando termini il movimento in una Locanda recuperi (1) PV in più.» → «Finché è equipaggiata ottieni (+1) AR e (+1) MOV.» (testo dell'autore, `Carte_nuove_2026-11-05.xlsx`, foglio Equipaggiamento: la Locanda non è più una casella) |
| C-2 | `carte_comuni.csv` | TE-20 Tunica del Viandante, `testo` | «…; quando termini il movimento in una Fonte recuperi anche (1) PV.» → «Finché è equipaggiata ottieni (+1) AR; quando peschi una Fonte dal sacchetto recuperi anche (1) PV.» **[PLAYTEST]**: stessa formula di TC-04, non è nel file dell'autore; la carta porta il segno PROVVISORIO |
| C-3 | `carte_comuni.csv` | TI-15 Mappa Sussurrata, `testo` | «…su una casella esplorazione…» → «…su una casella «?»…» («casella esplorazione» non esiste: sulla plancia e sulla Carta Aiuto si chiama «?») |
| C-4 | `carte_aiuto.csv` | AI-01…04, `passo5_testo` | «Puoi giocare carte. Togli un cubetto dalle clessidre. Tocca a sinistra.» → «Puoi giocare carte, non equipaggiamenti. Tocca a sinistra.» (nessuna carta stampata ha l'icona clessidra della durata, quindi «dalle clessidre» si confondeva con i segnalini Clessidre del passo 1; «non equipaggiamenti» è il testo della bozza) |
| C-5 | `segnalini.csv` | SG-01 Indizio, SG-02 Clessidra, `copie` | Indizi 12 → 16, Clessidre 12 → 8 (restano 28 pezzi su un foglio; simulazione 30.000 partite: a 4 giocatori il 5,6 % supera 12 Indizi in gioco, massimo 15; le Clessidre in gioco insieme non superano 1 perché le danno solo Gnomo e Basilisco). Aggiornati `LEGGIMI`, `dati_stampa.md`, intestazione e piè del foglio |
| C-6 | `LEGGIMI.md`, `ISTRUZIONI_DI_STAMPA.md` | «Da procurarsi» | «4 dadi D6» → «4 dadi D6 (meglio 8: 2 per giocatore, come vuole l'autore)» |
| S-1 | `parts_stampa.py` | scheda eroe, casella Forte Volontà | nota «una sola» → «ritira 1 D6, non cumulabile» (promemoria dell'effetto) |

## 6. Scelte [PLAYTEST] del regolamento per il playtest

Fonte: `regolamento/playtest/Regolamento_playtest.pdf` (agente RegolamentoPlaytest, 5/11); elenco completo e motivazioni in `regolamento/playtest/LEGGIMI.md`, sezione «Regole provvisorie». Dove la bozza tace si è scelta l'opzione più semplice. Nessun testo stampato sulle carte cambia (i testi della Carta Aiuto sono copiati com'erano). Da confermare con l'autore:

1. **[PLAYTEST]** «Attacca per primo» (Agguato, Fauci): niente tiro di iniziativa.
2. **[PLAYTEST]** Al 3° Indizio gli altri prendono 1 Indizio solo la prima volta, quando compare MIMI.
3. **[PLAYTEST]** La casella «?» resta e si pesca di nuovo.
4. **[PLAYTEST]** Dopo una fuga o una sconfitta la tessera rossa resta e la carta Mostro va in fondo al mazzetto.
5. **[PLAYTEST]** Una Trappola che porta a 0 PV, o una carta avversaria fuori dal Duello: sconfitta normale, nessuna ricompensa.
6. **[PLAYTEST]** «Creatura» = mostro o boss.
7. **[PLAYTEST]** I boss del mazzetto 3 non tengono le ferite; al livello 5 il «+1 livello» non dà niente.
8. **[PLAYTEST]** Il Cuore della plancia non ha effetti; oltre la fine della traccia si conta a mente.
9. **[PLAYTEST]** Duello: con lo stesso MOV vince lo sfidante.
10. **[PLAYTEST]** Forte Volontà: nel tiro per colpire si ritira 1 solo dei 2 dadi.
