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

Fonte: `regolamento/playtest/Regolamento_playtest.pdf` del 5/11 (ora `archivio/v5_05-11/regolamento/`; agente RegolamentoPlaytest, 5/11); elenco completo e motivazioni in `regolamento/playtest/LEGGIMI.md`, sezione «Regole provvisorie». Dove la bozza tace si è scelta l'opzione più semplice. Nessun testo stampato sulle carte cambia (i testi della Carta Aiuto sono copiati com'erano). Da confermare con l'autore (i punti 3 e 4 sono confermati nella v6, sezione 7):

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

## 7. Versione 6 (8/11)

Fonte: `Il_Tesoro_del_Goblin_Regolamento_corretto.docx` di Desy (6/11; § = sua sezione). Nella v6 entrano **solo le parti chiare**; tutto ciò che è incerto (carte nel turno dell'avversario, poteri di classe del 5/11, Difesa, danno, ricompense di Desy, Clessidre, ecc.) è nel documento di lavoro `regolamento/da_discutere/Punti_aperti_v6.docx` e per ora resta la regola del kit. Regolamento: `regolamento/playtest/Regolamento_playtest_v6.docx`. Kit: `stampa/playtest_v6/` e `stampa/playtest_v6_A3/`; il kit e il regolamento del 5/11 sono in `archivio/v5_05-11/`. Niente matita e foglio: tutto si segna con oggetti (decisione dell'utente).

| ID | Regola | Desy | Cosa cambia in stampa |
|---|---|---|---|
| A1 | **Turno in 4 passi:** 1 Clessidre · 2 Muovi · 3 Esplora · 4 Fine; sparisce il passo «Carte». «salta al passo 5» → «salta al passo 4». Il passo Clessidre resta (le Clessidre sono un punto aperto, non tolte) | §5 (turno in 3 passaggi), §4.1 («senza una fase dedicata») | `carte_aiuto.csv` AI-01…04: `fronte_titolo` «Il turno in 4 passi», `passo1…4_*`, colonna `riquadro_carte` al posto di `passo5_*`; `genera_carte.py` `carta_aiuto_fronte()`: 4 passi e riquadro senza numero; `componenti_gen/svg.py` promemoria della plancia «Turno: Clessidre · Muovi · Esplora · Fine» (A4 e A3); `parts_stampa.py` `turn_strip()` |
| A2 | **Carte:** nel proprio turno, in qualsiasi momento, fino a 2 in tutto, comprese quelle in risposta. Il Duello non cambia (chi si difende gioca 1 carta) | §4.1, §13 | Carta Aiuto, riquadro: «Carte: nel tuo turno, in qualsiasi momento, fino a 2 (anche in risposta).» |
| A3 | **Equipaggiamenti:** in qualsiasi momento del proprio turno, anche in scontro, al massimo 1; mai nel turno di un avversario | §4.1, §13 | Carta Aiuto, riquadro: «Equipaggiamenti: 1, solo nel tuo turno.» (sparisce «Equip solo ora») |
| A4 | Casella «?» riesplorabile: tolto il marcatore (PLAYTEST) | §6 | Solo regolamento |
| A5 | Tessera rossa che resta scoperta dopo fuga o sconfitta: tolto il marcatore (PLAYTEST) | §6, §11.4 | Solo regolamento |

**Incoerenze del kit corrette** (vale il kit stampato):
- **Passo Fine:** il regolamento v5 diceva «Puoi giocare carte. Togli un cubetto dalle clessidre. Tocca a sinistra.», la Carta Aiuto (correzione C-4) «Puoi giocare carte, non equipaggiamenti. Tocca a sinistra.». Ora regolamento, Carta Aiuto e plancia dicono lo stesso: «Togli un cubetto Durata da ogni tua carta con la clessidra. Tocca a sinistra.». La regola dei cubetti Durata esiste nel regolamento, quindi torna sulla Carta Aiuto, con «cubetto Durata» e «tua carta» per non confonderla con i segnalini Clessidra del passo 1 (il motivo di C-4); «Puoi giocare carte» non serve più (riquadro Carte).
- **Segnalini:** il regolamento v5 diceva «28 Segnalini: 12 Indizi, 12 Clessidre, 4 Forte Volontà»; il kit stampa 16 Indizi + 8 Clessidre + 4 Forte Volontà (`segnalini.csv`, C-5). Corretto il regolamento.
- **Dadi:** il regolamento v5 diceva «4 dadi D6 (uno per giocatore)»; le istruzioni di stampa «4, meglio 8» (C-6). Corretto il regolamento.

**Decisione dell'utente 8/11 — Indizio dai mostri con il D6.** Chi vince contro un mostro tira 1 D6 e prende 1 Indizio solo se il risultato è ≤ LV stampato sulla carta (LV 1: 1; LV 2: 1-2; LV 3: 1-3; LV 4: 1-4; boss LV 5 del mazzetto 3 su una tessera rossa: 1-5). Il resto delle ricompense non cambia (PE, Forte Volontà del mazzetto 2, «+1 livello» e Forte Volontà del boss del mazzetto 3). Lo scontro con il custode (MIMI) è la vittoria e non cambia; il Duello non cambia. È una scelta dell'utente, non una regola del documento di Desy (che al §9 propone altre ricompense: punto aperto nel documento di lavoro).

| File | Righe | Campo | Vecchio → nuovo |
|---|---|---|---|
| `carte_mostro.csv` | NE-01…13 (13) | `ricompense` | «1 indizio · 1 punto esperienza» → «Indizio se D6 ≤ LV · 1 PE» con il LV della carta (NE-01…09 «≤ 1», NE-10…13 «≤ 2»). «1 PE» invece di «1 punto esperienza»: con la condizione la riga deve stare su una riga sola |
| `carte_mostro.csv` | NE-14…21 (8) | `ricompense` | «1 indizio · 1 punto esperienza · Forte Volontà» → «Indizio se D6 ≤ 3 · 1 PE · Forte Volontà» (NE-14…17) e «… ≤ 4 …» (NE-18…21) |
| `carte_mostro.csv` | NE-26…28 (3) | `ricompensa_se_mazzetto_3` | «1 indizio · +1 livello · Forte Volontà» → «Indizio se D6 ≤ 5 · +1 livello · Forte Volontà»; `ricompense` «MIMI: vinci la partita» invariato |
| `carte/genera_carte.py` | carte boss | impaginazione | il riquadro Ricompense dei boss passa da 2 a 3 righe (la riga «Mazzetto 3» va a capo prima di «Forte Volontà», con spazio unificatore); il testo delle abilità resta intero (NE-26, 5 righe) |
| `carte_aiuto.csv` | AI-01…04 | `retro_ricompense` | «Mazzetto 1: 1 Indizio + 1 PE» / «Mazzetto 2: + Forte Volontà» / «Boss del mazzetto 3: 1 Indizio + livello + Forte Volontà» → «Mostro vinto: D6 ≤ LV del mostro → 1 Indizio» / «Mazzetto 1: 1 PE · Mazzetto 2: 1 PE + Forte Volontà» / «Boss del mazzetto 3: livello + Forte Volontà» (stesse parole del Riepilogo del regolamento v6; mazzetti 1 e 2 su una riga perché il retro resti di 5 righe in Ricompense) |
| `carte_aiuto.csv` | AI-01…04 | `retro_vittoria` | «Indizi solo vincendo scontri sulle caselle «?» e Duelli.» → «Indizi solo dai mostri (D6 ≤ LV) e dai Duelli.» |

Simulatore: `gioco/sorgenti/sim_playtest.py` applica le ricompense nel codice, non legge il testo dei CSV. Dall'8/11 tira il D6 ≤ LV dopo ogni mostro vinto (boss del mazzetto 3 compresi). Risultati: `simulazioni/ricompense_regolamento_corretto_2026-11-08.txt`, sezione 2 (variante F: 10,35 round in media contro 4,4 del kit 5/11); le tarature H/I/J sono nella sezione 3 e nel documento dei punti aperti.

Le decisioni dell'8/11 sui punti aperti (B1–B21, T1, T2) e la stampa solo fronte sono nella sezione 8 («v6-bis»), che completa questa versione.

## 8. Versione 6-bis (8/11)

Fonte: spec v6-bis dell'8/11 (approvata dall'utente), §0, §3, §4, §10. Vincoli dell'utente: **stampa solo fronte**, **niente cubetti**, **niente Clessidre**, carte Classe e Specie dedicate, statistiche sulle rotelle di carta, durate come stati di 1 turno.

### Decisioni (una riga per punto del documento di lavoro)

| Punto | Decisione |
|---|---|
| B1 | Carte solo nel proprio turno, max 2 comprese le risposte; Equipaggiamenti max 1; unica eccezione: chi si difende nel Duello gioca 1 carta. |
| B2 | Poteri di Desy §19 per Assaltatore, Stregone, Oracolo, una volta per partita, segnati con la tessera Usato; nessuna Carta Classe dà statistiche. |
| B3 | Ricercatore: una volta per partita, prima di muoverti, guardi la prima carta Imprevisti e puoi metterla in fondo; tiene il mazzetto ex Ladro. |
| B4 | Locanda: «+1 PE e recuperi 2 PV.» (IM-02 ×2, `testo` e `testo_bozza`). |
| B5 | Colpisci con 2D6 + ATT pari o superiore all'AR del bersaglio (dalla sera dell'8/11 la Difesa non esiste più: vedi «Decisione dell'utente 8/11 sera» qui sotto). |
| B6 | Danno con la tabella del kit. La variante «D6 + ATT − AR» per una seconda partita è stata tolta la sera dell'8/11 insieme alla Difesa (con l'AR della nuova scala non funzionerebbe più). |
| B7 | Indizio con D6 ≤ LV per tutti i mostri, boss del mazzetto 3 compresi; lo stallo del sacchetto si risolve con le «Tessere usate». |
| B8 | Forte Volontà da mazzetto 2, boss del mazzetto 3, Duello vinto, TI-08, TI-21; non più dalla Carta Classe. |
| B9 | Dal boss custode non fugge nessuno; da tutti gli altri mostri sì, salvo chi lo vieta. |
| B10 | La Mappa sposta il tesoro in un'altra Cripta; max 2 spostamenti segnati con tessere Usato. |
| B11 | Per il mostro tira il giocatore alla tua destra. |
| B12 | «Attacca per primo» senza tiro di iniziativa, nessun segnalino. |
| B13 | Variante «In famiglia» tolta. |
| B14 | 16 Indizi, 4 Forte Volontà, 0 Clessidre; in più 12 Usato e 14 Stati. |
| B15 / T1 | Solo oggetti: rotelle, Rotella dello scontro e del custode, tessere Stato e Usato, carte giocate davanti a sé fino alla Fine; niente cubetti, niente foglio. |
| B16 / T2 | Clessidre, turni persi e turni extra tolti; durate = stati di 1 turno; NE-05 e NE-21 danno lo stato Rallentato. |
| B17 | Rifiuto del Duello: lo sfidante pesca 1 carta a caso dalla mano dello sfidato e la tiene. |
| B18 | Lo Stregone pesca a caso la 6ª comune dalle comuni avanzate, dopo il draft. |
| B19 | Partita rapida da rifare dalla v6-bis, in A4, dopo l'approvazione. |
| B20 | Il workbook v4 non entra nel kit: valori di `carte_mostro.csv`. |
| B21 | Solo forma: da segnalare a Desy per la sua copia. |
| F1 | I file di Desy restano nella radice finché non si chiude la discussione con lei. |
| Stampa | **Kit solo fronte:** carte e dorsi su fogli separati (`<nome>.pdf` + `<nome>_retri.pdf`, dorsi non specchiati, stessa posizione del fronte), fustellati uno per uno e uniti con colla stick o bustina; Carte Classe, Specie, Aiuto e Divisori a un lato. |

### Testi delle carte cambiati (spec §3, §4)

| File | Righe | Campo | Vecchio → nuovo |
|---|---|---|---|
| `carte_mostro.csv` | NE-05 | `abilita` | «Catene: se ti sconfigge prendi 1 Clessidra.» → «Catene: se ti sconfigge prendi lo stato Rallentato.» |
| `carte_mostro.csv` | NE-21 | `abilita` | «… prendi 1 Clessidra.» → «… prendi lo stato Rallentato.» |
| `carte_comuni.csv` | TI-03 | `testo` | «Fino alla fine del tuo prossimo scontro ottieni (+2) AR.» → «Fino alla fine del turno ottieni (+2) AR.» |
| `carte_comuni.csv` | TI-06 | `testo` | «La prossima Trappola … tieni questa carta davanti a te finché succede.» → «Prendi lo stato Occhio: la prossima Trappola che peschi non ha effetto su di te.» |
| `carte_comuni.csv` | TI-15 | `testo` | «Il prossimo scontro che vinci …» → «Prendi lo stato Sussurro: il prossimo scontro che vinci su una casella «?» ti dà (1) Indizio in più.» |
| `carte_comuni.csv` | TI-18 | `testo` | «Fino al tuo prossimo turno, quando …» → «Prendi lo stato Riflesso: quando un avversario ti infligge Danni, subisce (1) Danno.» |
| `carte_comuni.csv` | TI-23 | `testo` | «… non può giocare carte Incanto fino al tuo prossimo turno.» → «Un avversario a una casella di distanza prende lo stato Silenzio: non può giocare carte Incanto.» |
| `carte_classe.csv` | TI-27 | `testo` | «Ottieni (+1) AR fino al tuo prossimo turno.» → «Prendi lo stato Fede: (+1) AR.» |
| `carte_comuni.csv` | TE-08 | `testo` | «Finché è equipaggiato … Una volta per partita annulli i Danni di un attacco subito: metti un cubetto Durata sulla carta.» → «Finché è equipaggiata ottieni (+1) AR. Puoi scartarla per annullare i Danni di un attacco subito.» |
| `carte_imprevisto.csv` | IM-02 ×2 | `testo`, `testo_bozza` | «… L'Oracolo ricarica il ritorno in vita.» / «… il suo potere.» → «+1 PE e recuperi 2 PV.»; `testo_bozza` vuoto |
| `carte_classe_ritratto.csv` | TC-01…04 | `testo`, nuova colonna `classe_riga`, `corretto_dalla_bozza` | testi della spec §4.1 (poteri una volta per partita, tessera Usato); in fondo la mano («Mano: 5 delle 8 carte di classe + 5 comuni», ecc.); `corretto_dalla_bozza` vuoto. **TC-03 accorciato**: tolto «(dei 2D6 per colpire se ne ritira uno)», perché il testo usciva dalla carta (ripiego previsto dalla spec; la precisazione resta nel regolamento) |
| `carte_specie.csv` (nuovo) | TS-01…04 ×2 | tutte | 8 Carte Specie della spec §4.2 (bonus e nota, Yumaniano PROVVISORIO), compresi i promemoria facoltativi di Elfo e Sanguar (ci stanno); `tessere_specie.csv` tolto (`git rm`) |
| `divisori.csv` | DV-04 | `contenuto_playtest`, `carte_del_tipo` | «Carte Classe», 4 → «Carte Classe e Carte Specie», 12 |
| `carte_aiuto.csv` | AI-01…04 | struttura e testi | ogni riga stampa 2 carte a un lato: «Il turno in 3 passi» (Muovi, Esplora, Fine con gli stati; colonne `passo4_*` tolte; riquadro «Carte … restano davanti a te fino alla Fine») e «Riepilogo» (fuga «mai dal custode», tessere con «Sacchetto vuoto: rimetti dentro le tessere usate.», Vittoria con la Rotella del custode); testi della spec §3.1, entrano senza accorciamenti |

### Stampa solo fronte (spec §0)

- `genera_carte.py` scrive un PDF di fronti e, per i mazzi coperti, un PDF di dorsi: `carte_comuni`, `carte_classe` (le 4 Carte Classe non hanno dorso: cella vuota), `carte_mostro`, `carte_imprevisto` + `_retri`; `carte_specie.pdf` e `carte_aiuto_divisori.pdf` senza dorsi. Nessuna pagina specchiata o interlacciata; il dorso sta nella stessa cella del suo fronte.
- Ogni dorso porta nell'abbondanza in basso (sparisce col taglio) il mazzo e l'ID del fronte, es. «Mostro 2 · NE-19»; nel margine: «RETRI · foglio k di n · coi fronti del foglio k». I fronti portano «FRONTI» (o «SOLO FRONTE») e il numero del foglio.
- `verifica_pdf.py` segnala ERRORE se una pagina è un «RETRO» di un vecchio fronte-retro, se un `_retri.pdf` non ha lo stesso numero di pagine dei fronti o se l'ID di un dorso non coincide con quello del fronte nella stessa cella (controllo dello specchio).
- Fogli carte A4: 5 + 5, 4 + 4, 1, 3 + 3, 2 + 2, 2 = 31 (A3: 3 + 3, 3 + 3, 1, 2 + 2, 1 + 1, 1 = 20).
- Kit completo: **46 fogli A4** (carte 31 + plance eroe 4 + rotelle 2 + segnalini 2 + plancia 4 + esplorazione 1 + pedine 1 + prova 1) e **28 fogli A3**; regolamento (11) e partita rapida (2) in A4. Elenco in `stampa/playtest_v6/ordine_di_stampa.txt`.

### Rotelle: finestre diverse dalla spec (§5.2)

| Rotella | Spec | Stampato | Perché |
|---|---|---|---|
| PV (0–13, 14 settori) | 11 × 9 mm | **9 × 9 mm** (cifre 4,0 mm) | con 14 settori sull'anello a 20 mm dal centro, una finestra larga 11 mm lasciava vedere il numero vicino (0 mm di margine) |
| AR (9–20) | 11 × 9 mm | 11 × 9 mm | come la spec. Fino alla sera dell'8/11 era 9,5 × 9,5 mm, con sotto il numero una riga per la Difesa, tolta con la decisione dell'utente qui sotto |
| PE (0–8, con livello e mazzetto) | 14 × 11 mm | **13 × 11 mm**, anello dei numeri a 19 mm dal centro (cifre 4,0 mm) | a 14 mm la finestra arrivava a 0,5 mm dal bordo del disco Ø 52 |
| PV massimi, ATT, MOV, rotelle della plancia | 11 × 9 mm | 11 × 9 mm (cifre 4,5 mm) | come la spec |

Verifica (KitComponenti, 8/11): `componenti_gen/gen.py` controlla ogni rotella prima di scrivere e si ferma se una finestra può mostrare un valore vicino; il disco stampato è stato provato sulla plancia stampata in tutte le 58 posizioni: ogni finestra mostra un solo valore. Le finestre sono disegnate sui dischi, quindi non serve misurarle.

### Decisione dell'utente 8/11 sera: niente Difesa, si colpisce contro l'AR

Regola: **colpisci se 2D6 + ATT ≥ AR del bersaglio.** La parola «Difesa» e la formula che la calcolava dall'AR non esistono più. Trasformazione equivalente, il bilanciamento non cambia:
- **mostri**: AR statica = la Difesa stampata prima (es. Folletto Ingannatore AR 2, Difesa 10 → AR 10); il riquadro DIFESA sparisce dalle carte, che hanno 3 riquadri: PV, ATT, AR;
- **eroi**: AR di partenza 9 (prima AR 1, Difesa 9); ogni bonus (+N) AR di specie, equipaggiamenti, Incanti, stati e livelli resta (+N). Le abilità che tolgono AR (Melma acida: «la tua AR conta 1 in meno») restano uguali.

| File | Cosa cambia |
|---|---|
| `carte_mostro.csv` | `ar` := la vecchia `difesa` (NE-01…28: 8-11); colonna `difesa` tolta; `nota` aggiornata (riporta il valore AR di prima) |
| `carte/genera_carte.py` | carta Mostro con 3 riquadri (PV, ATT, AR) larghi un terzo invece di 4 |
| `carte_aiuto.csv` | AI-01…04, carta «Riepilogo», Scontro: «1° tiro: colpisci se 2D6 + ATT ≥ AR del bersaglio.» |
| `gioco/sorgenti/sim_playtest.py` | AR dei mostri letta dal CSV, AR base dell'eroe 9, colpo se 2D6 + bonus ≥ AR; **tolta la variante di danno `--danno autore`** (D6 + ATT − AR del bersaglio), che usava l'AR della vecchia scala e apparteneva alla stessa famiglia di formule tolta dall'utente |
| Plance eroe e dischi AR (KitComponenti) | anello AR 9-20, niente riga della Difesa, finestra AR 11 × 9 mm |

Nessun altro testo di carta cambia: le Carte Specie e Classe non scrivono l'AR di partenza; i (+N) AR degli equipaggiamenti, di TI-03/27/34 e dello stato Fede restano. Verifica: `sim_playtest.py --esatto --partite 10000` dà gli stessi numeri di prima, partita per partita (stesso seme: 12,3 / 10,3 / 9,2 round a 2 / 3 / 4 giocatori, media 10,6), perché la trasformazione è esatta.
