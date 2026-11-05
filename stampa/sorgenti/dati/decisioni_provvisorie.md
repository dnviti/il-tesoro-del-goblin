# Decisioni provvisorie per il kit di playtest

Regole di riferimento: bozza Word `Regolamento_Tesoro_del_Goblin_bozza.docx` (2/11/2026 22:06), letta dal commit `2aa7f84` (`v2/Regolamento_Tesoro_del_Goblin_bozza.docx`). Le citazioni sono copiate dal documento. Il confronto con il PDF v5 (`v2/Regolamento_base_v5_stampa.pdf`) è stato fatto sul testo del PDF e sullo script `v2/regolamento_stampa/docx/edit_html.py`, che elenca tutte le modifiche applicate al regolamento v5 per ottenere la bozza.

Nella bozza i punti con evidenziatore giallo sono 6 run: i 4 «Da decidere» e due «da confermare» (8 Tessere Specie; Stregone con 1 comune in più). Qui sotto: i 4 «Da decidere» (sezione 1) e tutto il resto che cambia la stampa (sezione 2).

## 1. I 4 punti «Da decidere»

Marcatore da stampare dove la scelta compare su un componente: la parola **PROVVISORIO** (maiuscolo, tra parentesi o dopo il testo, come indicato sotto). Nel regolamento si usa lo stesso marcatore; sui componenti serve solo dove il testo è stampato (tessera Yumaniano, Carta Aiuto).

### D-1 Direzione del draft

- **Passo della bozza** (Preparazione, punto 6): «Draft: ognuno riceve 5 comuni, ne tiene 1 e passa le altre a destra finché finiscono. Da decidere: sempre a destra o alternando destra e sinistra.»
- **Elenco «Punti da decidere»**: «Draft: si passa sempre a destra o si alterna destra e sinistra come in Magic?»
- **Opzioni offerte dalla bozza**: (a) sempre a destra; (b) alternando destra e sinistra (come in Magic).
- **Scelta: (a) sempre a destra.** Perché: è già scritto nel testo, non serve un promemoria sul giro dei passaggi.
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

### D-3 Mazzetto dei mostri: per livello o per Indizi

- **Passo della bozza** (Esplorare, riga «Tessera rossa: Mostro»): «Gira la prima carta del mazzetto del tuo livello (livello 1-2: mazzetto 1; 3-4: mazzetto 2; 5: mazzetto 3, i boss). […] Da decidere: il mazzetto si sceglie dal livello o dagli Indizi (0: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3).»
- **Elenco «Punti da decidere»**: «Mazzetto dei mostri: si sceglie dal livello dell'eroe (com'è scritto ora) o dagli Indizi che ha (0 Indizi: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3)? Con il livello il mazzetto 2 non esce quasi mai.»
- **Opzioni offerte dalla bozza**: (a) dal livello dell'eroe (1-2 → mazzetto 1; 3-4 → mazzetto 2; 5 → mazzetto 3); (b) dagli Indizi (0 → 1; 1 → 2; 2 → 3).
- **Scelta: (a) dal livello, come scritto ora.** Perché: è già il testo di regolamento, Carta Aiuto, tessera «?» e carte Mostro («LV 1-2», «LV 3-4», boss); il problema («il mazzetto 2 non esce quasi mai») si valuta al tavolo senza stampare nulla di diverso.
- **Dove compare in stampa**: Carta Aiuto (retro, riga «Rossa: mazzetto del tuo livello (1-2 · 3-4 · 5)»), identica alla bozza; nessun'altra modifica. Le 24 carte Mostro restano divise in mazzetto 1 (13), mazzetto 2 (8), boss (3).
- **Testo da stampare** (regolamento): «Gira la prima carta del mazzetto del tuo livello (livello 1-2: mazzetto 1; 3-4: mazzetto 2; 5: mazzetto 3, i boss). Scontro, oppure fuga (pagina 10). […] (PROVVISORIO: il mazzetto si sceglie dal livello.)»

### D-4 Pareggio dell'iniziativa

- **Passo della bozza** (Lo scontro, punto 1): «Chi attacca per primo. Tu e il nemico tirate 1 D6 a testa: chi fa di più attacca per primo. Per il mostro tira il giocatore alla tua destra. Da decidere: in caso di pareggio (proposta: si ritira).»
- **Elenco «Punti da decidere»**: «Chi attacca per primo: se il tiro di 1 D6 è pari? Proposta: si ritira.»
- **Opzioni offerte dalla bozza**: la sola proposta, si ritira (l'alternativa non è scritta; il pareggio si risolve con un nuovo tiro di 1 D6 per parte).
- **Scelta: si ritira.** Perché: è la proposta della bozza, non richiede regole nuove e si applica uguale al Duello («Chi attacca per primo si decide con 1 D6 a testa, come negli scontri»).
- **Dove compare in stampa**: regolamento (scontro e Duello) e Carta Aiuto, retro, riga aggiunta sotto «Chi attacca per primo» (campo `retro_pareggio` in `carte_aiuto.csv`; è l'unica riga delle Carte Aiuto non copiata dalla bozza).
- **Testo da stampare**: «Pareggio: si ritira (PROVVISORIO).» Nel regolamento: «In caso di pareggio si ritira. (PROVVISORIO)».

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

- **TE-18 Veste del Pellegrino** («quando termini il movimento in una Locanda recuperi (1) PV in più») e **TE-20 Tunica del Viandante** («quando termini il movimento in una Fonte recuperi anche (1) PV»): Locanda, Fonte e Fabbro non sono più stampati sulla plancia, sono carte Imprevisto. Il testo è copiato com'è in `carte_comuni.csv` (nota APERTO). Da decidere con l'autore prima della stampa definitiva.
- **Inizia subito v5** (`Inizia_subito_v5_stampa.pdf`) ha ancora Guerriero/Ladro/Mago, 5 specie e «Guerriero 6» PV: non è allineato alla bozza. Se si distribuisce nel playtest, correggerlo o non darlo.
- **Catalogo xlsx v2** (`Catalogo_carte_v2.xlsx`): Leggimi e colonna Difesa sulla scala D20; non usarlo per la stampa.
- **Carte Imprevisto**: `xlsx_v2.py` dice «L'Oracolo ricarica il ritorno in vita», bozza/PDF v5 «L'Oracolo ricarica il suo potere», e «Riprendi 1 equipaggiamento» contro «Riprendi in mano 1 equipaggiamento». In `carte_imprevisto.csv`: `testo` = `IMP` (come richiesto), `testo_bozza` = versione della bozza. Usarne una sola.
- **Divisori**: nessun file ne definisce il contenuto (vedi `dati_stampa.md`, sezione 2).
- **Carte Nemico** `Carte_Nemico_v2.pptx`: le carte Boss riportano solo «MIMI: vinci la partita»; la ricompensa del mazzetto 3 (1 indizio, sali di livello, Ispirazione) è nella colonna `ricompensa_se_mazzetto_3`.
- **Nome «Occhio dello Stregone»** (TI-06) coincide con la nuova classe; **«Cimitero dei Maghi»** (TM-05) è un nome di luogo: non rinominare.
