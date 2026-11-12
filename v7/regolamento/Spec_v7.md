# Il Tesoro del Goblin — Spec v7 delle regole (playtest)

Bozza del 10/11/2026. Destinazione nel repo: `v7/regolamento/Spec_v7.md`.

È il contratto interno per quattro lavori: chi scrive le carte (fase 3), il simulatore v7 (fase 4, `v7/simulatore/`), i generatori del kit (fase 5, `v7/stampa/`) e chi scrive il regolamento v7 per i giocatori (fase 6). Non è il regolamento: il testo per i giocatori sarà più corto e più semplice (D17).

Fonti, in ordine di precedenza:
1. le decisioni D1–D23 del 9-11/11 (§1);
2. il piano `v7/idee/v7_piano_TEMP.docx` aggiornato il 10/11, con i commenti di Desy e le risposte di Daniele;
3. per tutto quello che la v7 non cambia, il regolamento playtest v6 (`v6_08-11/regolamento/Regolamento_playtest_v6.pdf`) e i CSV v6 (`v6_08-11/stampa/sorgenti/dati/`);
4. le carte di Desy (`v7/desy_design carte/Carte_nuove_2026-11-05.xlsx`), solo per sapere quali meccaniche esistono; per le carte di classe nuove anche `v7/desy_design carte/Idee desi carte classi.ods` (D22).

## 0. Convenzioni

- **R n.m**: regola numerata, da citare così («R 4.7»). Ogni regola dice chi fa cosa e quando, così si può provare al tavolo o nel simulatore.
- **[PLAYTEST]**: valore o scelta di partenza, da provare e tarare col simulatore. Il piano §11 dice: «si produce il playtest v7 con le proposte del piano come valori di partenza». L'elenco completo è nel §18.
- **(Dn)**: decisione presa (§1). **(v6)**: regola della v6 che la v7 non cambia.
- **OP-n**: opzione di playtest NON decisa (idee del piano §5). Non è la regola di base: il simulatore deve poterla accendere (§16). OP-3 e OP-4 sono diventate regola di base il 10/11 (D19, D18).
- **N-n**: punto aperto nato scrivendo questa spec. I punti aperti, con il default scelto, sono nel §19, l'ultima sezione.
- I numeri tra parentesi sulle carte sono valori: «(+1) AR» vuol dire 1 in più di AR (v6).

## 1. Decisioni D1–D26 e dove stanno

| # | Decisione (testo) | Regole |
|---|---|---|
| D1 | Ritiri: ogni nuovo ritiro dello stesso tiro ha −1 cumulativo per ogni ritiro precedente: −1 al primo ritiro, −2 al secondo, e così via. Vale per carte, Forte Volontà, potere dello Stregone, Equipaggiamenti. | §5 |
| D2 | Power level (PL) dalle carte al posto di PE e livello. Le statistiche non crescono al passaggio di livello: cambiano solo con le carte. Il PL sceglie il mazzetto dei mostri. | §6 |
| D3 | 5 classi. Arriva il Giullare (scarta e pesca, mill). L'Oracolo passa alle Profezie: indovina il tiro, con un effetto semplice più un extra se indovina. | §13 |
| D4 | Equipaggiamenti solo nel proprio turno e solo per aprire una catena. La catena fa un giro in senso orario e si chiude con l'ultimo giocatore. Si risolve LIFO. Durante una catena non se ne apre un'altra. | R 4.2, R 4.5–4.9 |
| D5 | Il simulatore si aggiorna alla v7. | §16, §17 |
| D6 | Sacchetto, strade bloccate e ostacoli si risolvono con la nuova mappa (§8 del piano). | §8 |
| D7 | Ogni «perdi l'equipaggiamento» si risolve col D6 della perdita: 1 tutto, 2 Elmo, 3 Arma DX/Scudo, 4 Arma SX, 5 Armatura (slot vuoto = niente), 6 niente. Costi scelti (sacrificio dell'Assaltatore) ed effetti su un oggetto preciso seguono il testo della carta (da confermare). Morte (0 PV): D6 della perdita (l'Assaltatore può saltarlo col potere); si torna sulla PROPRIA Partenza iniziale, senza tiro; PV al massimo; Indizi tenuti; si pesca 1 carta dal mazzo comune. | §11 |
| D8 | Mano massima 10, mai superata in nessun momento. Se una carta deve entrare in una mano che ne ha già 10, PRIMA si scarta 1 carta (9) e POI si prende (10). Vale per pesca, ricompensa, carta presa a un avversario o ripresa dagli scarti, ogni carta di «pesca 2», il +1 del Giullare. | R 12.4 |
| D9 | Regola magna: tutte le carte tranne gli Equipaggiamenti si giocano in qualsiasi fase, nel proprio turno e in quello degli altri, anche in risposta. Ogni giocatore gioca AL MASSIMO 2 CARTE tra una sua Fine del turno e la successiva, contando insieme il proprio turno e quelli degli altri. Resta 1 carta per giocatore in ogni catena. | R 4.1, R 4.3 |
| D10 | Le Mappe si giocano anche in risposta, anche per spostare il tesoro mentre un eroe arriva sulla Cripta. | R 10.11 |
| D11 | Pescare carte come premio è molto forte: si tara col simulatore, sempre col tetto 10. I mostri del mazzetto 3 non danno premio, solo il tiro per l'Indizio. La partita finisce solo sconfiggendo il custode di MIMI. Proposta da tarare: mazzetto 1 = tiro Indizio; mazzetto 2 = Forte Volontà + tiro Indizio; mazzetto 3 = solo tiro Indizio; la pesca resta 1 carta a inizio turno, più quella alla morte. | §10, R 12.3 |
| D12 | «Potere» = l'effetto della Carta Classe, una volta per partita (non un hero power usato ogni turno). Ricercatore: guarda le prime 3 carte (al massimo) del mazzo Mostri o del mazzo Imprevisti e le rimette nell'ordine che preferisce. | R 13.1, R 13.3 |
| D13 | Il potere del Giullare pesca dal mazzo delle carte generiche (comuni), col tetto 10. | R 13.6 |
| D14 | Plance eroe neutre: niente nome di classe e niente specie stampati. Classe e specie stanno solo sulle loro carte, infilate negli angoli. | R 2.2 |
| D15 | Ombra deforme (e Discesa Yumaniana, commento 8 di Desy): troppo complesse, fuori dalla v7. Restano tra le idee future. | V12 (§14.2) |
| D16 | La bozza `v7/idee/v7_bozza_mappa.svg` resta un esempio per il playtest, linee di strada comprese (servono solo al playtest). La mappa definitiva (ostacoli rivisti, senza linee) si progetta in un lavoro a parte. Il regolamento non dipende dalle linee. | R 8.1 |
| D17 | Il testo del timing per i giocatori va riscritto più semplice: frasi brevi, un esempio. Le regole non cambiano. | §4.2 |
| D18 | Indizio dai mostri: alla sconfitta del mostro si prende l'Indizio se D6 ≤ LV del mostro + 1 (LV 1 → 1–2, LV 2 → 1–3, LV 3 → 1–4, LV 4 → 1–5, LV 5 → sempre). Era OP-4 (idea del 9/11): regola di base dal 10/11. Daniele l'ha confermata il 12/11: vale «≤ LV + 1», non la nota più vecchia «≤ LV». | R 10.2 |
| D19 | AR di tutti i mostri (mazzetti 1–3, boss e custode) ridotta del 25 % e arrotondata per eccesso: AR nuova = ⌈AR × 0,75⌉, cioè 8 → 6, 9 → 7, 10 → 8, 11 → 9. L'AR degli eroi non cambia (parte da 9). Era OP-3: regola di base dal 10/11. | R 6.8, R 7.3 |
| D20 | Mostri raddoppiati: ogni mostro ha un effetto unico, bilanciato sul suo livello. | §7, §15 |
| D21 | Tono goliardico alla Munchkin nei nomi delle carte e nelle battute (colonna `battuta`); il testo delle regole resta fatto di formule esatte. | §14.1 |
| D22 | Le carte di classe passano da 10 a 20 per classe: 10 per direzione. Id nuovi: 11–15 direzione A, 16–20 direzione B; gli id esistenti non cambiano. Le carte nuove vengono dalle idee di Desy (`v7/desy_design carte/Idee desi carte classi.ods`: 34 Equipaggiamenti e 43 Incanti, quasi tutti di classe), riscritte con il tono di D21. L'Oracolo non ha carte di Desy: ne riceve 10 tutte nuove. Le carte di Desy «tutti» (senza classe) vanno nel mazzo comune. Il mazzetto di classe è di 10 carte su 20 [PLAYTEST]: 3 in mano e 7 nella pila di classe. Gli Equipaggiamenti di Desy sono diversificati: niente riga fissa «+1 AR / +1 AT finché resta equipaggiato», l'effetto nasce dal secondo effetto (quello di colore) della carta di Desy. Il numero di carte non ha un tetto: si aggiungono quante servono. | R 3.6, R 3.7, R 13.1, §14 |
| D23 | **Superata da D24 (12/11)** per mappa, tile, muri, Cripte e preset: resta qui come storia. [PLAYTEST] La mappa si compone con tile esagonali generiche, stampate separatamente, per costruirla dal vivo durante i playtest e provare molti casi senza stampare la plancia intera (richiesta di Daniele, 11/11). La tile ha le misure dell'esagono di prima (25,2 mm da lato a lato, punta in alto) e la sua linea di taglio; i tipi sono Strada, «?», Guado, Ponte, Partenza 1–6, Cripta 1–4, Bosco, Case, Rocce, Acqua. I muri sono listelli a parte, uno per lato (compresi i 10 che chiudono le Cripte). La Sala del Tesoro è un pezzo a parte. Le 10 configurazioni del §17 (base «Strettoie» e una per Mappa TM-01…09) sono preset di costruzione, ognuno con il suo foglio di istruzioni. In playtest la mappa si può anche comporre liberamente, per provare casi diversi: i controlli che i preset rispettano restano come consiglio, non come obbligo. Se comporre la mappa in partita diventi una regola ufficiale è un punto aperto (§19, N25). | D24 |
| D24 | [PLAYTEST] **Mappa 12×12 a fiori in draft, Cripta a coordinate, niente muri** (Daniele, 12/11; supera D23). La mappa è di 12 × 12 esagoni da 25,2 mm. Pezzi: la **base** stampata su 2 fogli A4 (coordinate 1–12 su tutti i lati; i 46 esagoni di bordo con le 6 Partenze, non simmetriche ma bilanciate, e 4 ostacoli singoli; i 14 spazi numerati per i fiori), **14 fiori** di 7 esagoni a due facce, 24 segnaposto «?» e 1 segnalino Cripta. Spariscono le 100 tile, i listelli dei muri e i preset 10 × 10. **I muri non esistono più:** gli ostacoli sono solo quelli stampati sui pezzi. Si monta col **draft**: ognuno riceve dei fiori e li posa a turno in uno spazio libero, con la faccia e la rotazione che vuole; poi si dividono le «?» e si posano a turno. I **10 preset** (base «Strettoie» e uno per Mappa TM-01…09) restano come montaggio veloce, con gli stessi 14 fiori in spazio, faccia e rotazione fissi. **Le Cripte non sono stampate:** la Cripta si tira con 2D6 per la colonna e 2D6 per la riga quando il tesoro viene individuato e a ogni «Il tesoro cambia Cripta». Una carta Mappa cambia solo **3 fiori**, indicati sul suo foglio. Accettati: circa il 26 % di ostacoli e qualche vicolo cieco. Le tessere 3D si fanno con SolidCraft. Progetto e numeri: `v7/idee/mappa_tessere/12x12/progetto.md`. | R 2.5, R 3.1, R 3.3, R 3.9, R 8.1, R 8.2, R 8.8, R 8.11, R 8.12, R 10.6, R 10.11, §17 |
| D25 | [PLAYTEST] **Terreni: si cammina ovunque non ci sia un ostacolo** (Daniele, 12/11). Gli esagoni liberi (strada, erba, mattonato, pavimento, guado, ponte…) sono tutti uguali per le regole: il movimento non è più «solo su strada». Gli **ostacoli** sono bosco, rocce e case. Nuova parola chiave **accidentato**: entrare in un esagono accidentato costa 1 MOV normale, **uscirne costa 1 MOV in più** (Daniele, 12/11 22:55, al posto del «+1 all'entrata»): con 1 MOV entri in acqua, per uscirne servono almeno 2 MOV. Per ora l'unico terreno accidentato è l'**acqua** senza ponte né guado, che quindi non è più un ostacolo; in futuro potranno esserci altri terreni accidentati. La Cripta si sposta solo da un ostacolo o da una Partenza (sull'acqua resta). Le «?» vanno su qualsiasi esagono percorribile, ad almeno 2 esagoni da ogni Partenza. | R 8.3, R 8.4, R 8.7, R 8.8, R 8.11, §15, §17 |
| D26 | [PLAYTEST] **Inizio più tranquillo e scontri più corti** (Daniele, 12/11 sera). (1) Niente Equipaggiamento gratis in preparazione: la regola v6 è tolta. (2) Primo giro: finché tutti non hanno fatto il loro primo turno, niente Duello e nessuna carta giocata contro un avversario (22:55). (3) In uno scontro con un mostro l'eroe fa al massimo 3 attacchi: se dopo il 3° il mostro è ancora vivo, quando toccherebbe a lui attaccare scappa, senza ricompense; la tessera rossa va tra le usate e la carta Mostro in fondo al suo mazzetto; le sue abilità «a fine scontro» non scattano (22:55). Il custode di MIMI non scappa mai. Il Duello non ha questo limite. (4) Il tesoro non ha più un limite di spostamenti: ogni «Il tesoro cambia Cripta» rifà il tiro della Cripta (22:55). | R 2.5, R 3.1, R 3.8, R 4.3, R 7.5, R 7.9, R 8.11, R 8.12, R 10.8, R 10.11 |

### 1.1 Cosa cambia rispetto alla v6, in breve

- Le carte si giocano anche nel turno degli altri, con il limite di 2 tra le proprie Fini; catena e pila LIFO (D4, D9). Sparisce l'eccezione del Duello: chi si difende non ha più bisogno di una regola speciale.
- Non ci sono più PE, livelli, tabella dei livelli né «+1 al livello»: il PL degli Equipaggiamenti sceglie il mazzetto (D2).
- La mano non è più fissa: mazzetto di classe di 10 carte su 20, mano iniziale 3 + 3, pesca 1 a inizio turno, massimo 10 (D8, D22).
- Muori → torni sulla tua Partenza iniziale e peschi 1 carta comune (D7).
- 5 classi con 20 carte ciascuna (10 + 10 direzioni, D22); nuove TC-02, TC-04, TC-05 (D3, D12, D13).
- Carte di classe nuove da Desy, con tono goliardico e senza la riga fissa «+1 AR / +1 AT finché resta equipaggiato»; Oracolo con 10 carte nuove (D22).
- Nuova mappa 12 × 12: una base stampata e 14 fiori a due facce posati in draft (o con un preset), niente muri; si cammina ovunque tranne che sugli ostacoli e l'acqua è accidentata; la Cripta si tira sulle coordinate; «?» consumabili; niente sacchetto [PLAYTEST] (D6, D16, D24, D25).
- Ritiri con penalità (D1). Ricompense senza PE (D11). Plance eroe neutre (D14).
- Mostri più facili: AR −25 %, da 8–11 a 6–9 (D19); Indizio con D6 ≤ LV + 1, garantito con LV 5 (D18).
- Mostri raddoppiati: 48 carte (26 nel mazzetto 1, 16 nel mazzetto 2, 6 boss), ognuna con un'abilità che nessun altro mostro ha (D20).

## 2. Componenti del playtest v7

**R 2.1** Niente cubetti, niente carta e matita. Ogni stato di gioco si segna con rotelle di carta (dischi con fermacampioni), tessere, pedine e con la posizione delle carte.

**R 2.2 Plance eroe neutre (D14).** 4 plance uguali, senza nome di classe e senza specie stampati: ogni plancia va bene per ogni eroe. Su ogni plancia:
- 2 riquadri 63 × 88 mm negli angoli, per la Carta Classe e la Carta Specie;
- 4 fessure per gli Equipaggiamenti: Elmo, Arma DX / Scudo, Arma SX, Armatura;
- 6 rotelle: PV, PV massimi, ATT, MOV, AR, PL;
- 3 cerchi Indizi, 1 cerchio Forte Volontà, il riquadro Stati;
- il promemoria, da riscrivere: niente PE né livelli.

**R 2.3 Rotelle.** Intervalli stampati nella v6 (verificati in `v6_08-11/stampa/sorgenti/componenti_gen/gen.py`): PV 0–13, PV massimi 5/7/9/11/13, ATT 1–8, MOV −1…8, AR 9–20, PE 0–8. Nella v7:
- la rotella PL (0–12) prende il posto della rotella PE/livello, senza le scritte di livello e di mazzetto;
- la rotella dei PV massimi deve mostrare ogni valore da 5 a 13: nella v7 le carte cambiano i PV massimi di 1 alla volta. Controllo per la fase 5;
- la Rotella dello scontro e la Rotella del custode restano 0–9 (v6).

**R 2.4 Carte.** Tutte le carte hanno il formato Magic 63 × 88 mm con abbondanza propria e si tagliano una alla volta con la dima. La stampa è solo fronte: fronti e dorsi su fogli separati, dorsi non specchiati (v6).

**R 2.5 Elenco.**

| Componente | v7 | Note |
|---|---|---|
| Base della mappa | 1, stampata su 2 fogli A4 da unire al centro (333 × 283 mm con la fascia) | D24. Fascia con le coordinate 1–12 su tutti i lati; i 46 esagoni di bordo con le 6 Partenze e 4 ostacoli singoli (gli altri sono liberi); i 14 spazi numerati dove vanno i fiori, con i numeri 1–6 sull'anello per la rotazione dei preset |
| Fiori | 14, da 7 esagoni (76 × 73 mm), a due facce: A «verde e acqua», B «pietra e case» | D24. Ogni faccia rispetta la regola di disegno del §17, che tiene la mappa collegata con qualunque posa. Una freccia d'ottone segna la rotazione |
| Segnaposto «?» | 24 | D24. Si posano sulla mappa al montaggio (R 3.1); sopra va una Tessera Esplorazione (R 3.3) |
| Segnalino Cripta | 1 | D24. Le Cripte non sono stampate: il segnalino va sulla mappa quando il tesoro viene individuato (R 8.8, R 10.6) |
| Sala del Tesoro | 1 pezzo a parte | D23. Rotelle del custode e dello scontro, cerchi di custode, MIMI e boss: prima era la fascia in alto della plancia. Le 2 caselle «Spostamenti del tesoro» della v6 non servono più (D26) |
| Fogli dei preset | 10 (A4) | D24. Base «Strettoie» e TM-01…09: per ogni spazio il fiore, la faccia e il numero verso cui va la freccia (§17). Il foglio di una Mappa dice anche i 3 fiori del cambio di mappa (R 8.12) |
| Plance eroe | 4 neutre | D14 |
| Rotelle eroe | 24 dischi (6 per eroe) | PL al posto di PE |
| Rotelle del tavolo | 2 | Scontro e custode (v6) |
| Rotella della Profezia | 1 | Nuova, per l'Oracolo (R 13.5): corona e disco, da tenere davanti all'Oracolo |
| Pedine | 13 | 5 eroi (nuova: Giullare), MIMI, Geronimo, 6 sagome dei boss (D20: una per boss, R 3.2) |
| Carte Classe | 5 | TC-01…TC-05 (§13) |
| Carte di classe | 100 | 5 classi × 20 (10 + 10 direzioni, D22): id 01–10 esistenti, 11–20 nuovi |
| Mazzo comune | 81 [PLAYTEST]: 31 Equipaggiamenti (TE-01…31), 41 Incanti (TI-01…41), 9 Mappe (TM-01…09) | Catalogo della fase 2 (piano §7) più le carte comuni nuove di D22 (63 prima di D22). Un foglio di preset per ogni Mappa (R 8.12, §17) |
| Carte Mostro | 48 (D20) | Mazzetto 1 (26), mazzetto 2 (16), boss (6): R 6.8. AR −25 % (D19), riga delle ricompense (R 10.2–10.3, D18) |
| Carte Imprevisto | 11 | 5 Trappole, 2 Locande, 2 Fonti, 2 Fabbri. Cambia il testo della Locanda (R 8.10) |
| Carte Specie | 8 | TS-01…04, 2 copie per specie (v6) |
| Carte Aiuto e Divisori | 8 Aiuto (4 «Il turno» + 4 «Riepilogo») e i Divisori | Testi da rifare in fase 6 |
| Tessere Esplorazione | 36 (25 rosse, 11 blu) | Retro bianco, nessun sacchetto (R 8.11) |
| Indizi, Forte Volontà | 16, 4 | v6 |
| Tessere Usato | 20 [PLAYTEST] | v6: 12. In più ora servono come segnaposto (R 4.4) |
| Tessere Stato | 31 [PLAYTEST] | Una copia per fonte (carte e mostri), al massimo 4 (gli eroi): Rallentato 4, Silenzio 4, Fede 4, Vantaggio 4, Fermo 4, Occhio 3, Riflesso 3, Svantaggio 3, Sussurro 2 (`stati.csv`, R 9.7) |
| Dadi | 4 D6 (meglio 8) | v6. Solo dadi a 6 facce |
| Fermacampioni | 27 | 24 eroe + 2 tavolo + 1 Profezia |

**R 2.6 Componenti tolti:** il sacchetto, la rotella PE/livello, le plance con il nome di classe, il Cuore della plancia (R 8.12) e il draft delle carte comuni (R 3.7).

## 3. Preparazione

**R 3.1 Mappa [PLAYTEST] (D24, D25).** Metti la base della mappa al centro del tavolo. Accanto metti il pezzo della Sala del Tesoro, con la Rotella del custode e la Rotella dello scontro. Decidete il primo giocatore (R 3.10), poi montate la mappa in uno dei due modi.
- **Draft.**
  1. Mescola i 14 fiori senza guardarli (in un sacchetto o nella scatola). Ognuno ne pesca 7 con 2 giocatori, 4 con 3 giocatori, 3 con 4 giocatori. Con 3 o 4 giocatori ne avanzano 2: restano scoperti accanto alla base.
  2. A turno, dal primo giocatore in senso orario, posa uno dei tuoi fiori in uno spazio libero, con la faccia e la rotazione che vuoi. Quando tutti hanno finito, l'ultimo giocatore del giro posa un avanzo e il penultimo posa l'altro.
  3. Dividete i 24 segnaposto «?»: 12 a testa con 2 giocatori, 8 con 3, 6 con 4. A turno posane uno su un esagono percorribile (R 8.3: anche acqua, guado o ponte, mai una Partenza) ad almeno 2 esagoni da ogni Partenza, uno per esagono.
- **Preset.** Al posto dei passi 1 e 2 segui il foglio di un preset (§17), di solito la base «Strettoie»: per ogni spazio dice quale fiore mettere, con quale faccia e verso quale numero 1–6 dello spazio va la freccia d'ottone (per esempio «S7: 9A·5» = nello spazio 7 il fiore 9, faccia A, freccia verso il 5). Poi fai il passo 3.

La Cripta non si mette al montaggio: arriva quando il tesoro viene individuato (R 8.8, R 10.6).

**R 3.2 Mostri e boss (v6; 6 boss dal 10/11, D20).** Mescola i mazzetti Mostro 1 e 2. Pesca a caso 1 dei 6 boss: è il custode di MIMI. Gli altri 5, mescolati, formano il mazzetto 3. Metti custode e MIMI nella Sala del Tesoro e gira la Rotella del custode sui PV del custode.

**R 3.3 Tessere (opzione A) [PLAYTEST].** Mescola le 36 Tessere Esplorazione a faccia in giù e mettine 1 coperta su ognuno dei 24 segnaposto «?». Le altre 12, coperte, formano la riserva. Accanto alla mappa lascia lo spazio per le «tessere usate».

**R 3.4** Mescola il mazzo Imprevisti e il mazzo comune e mettili coperti accanto alla plancia.

**R 3.5 Eroe.** Ognuno sceglie una classe diversa e prende una plancia eroe, la pedina e la Carta Classe della sua classe, poi sceglie una Carta Specie. Infila le due carte negli angoli della plancia. Gira le rotelle su PV 5, PV massimi 5, ATT 1, MOV 1, AR 9, PL 0, poi aggiungi il bonus della Carta Specie (v6). Le Carte Classe non danno statistiche (v6).

**R 3.6 Mazzetto di classe [PLAYTEST] (D22).** Scegli 10 delle tue 20 carte di classe, mescolando come vuoi le due direzioni. Le altre 10 tornano nella scatola e restano fuori dalla partita.

**R 3.7 Mano iniziale [PLAYTEST].** Prendi in mano 3 carte del tuo mazzetto di classe, a scelta, e 3 carte del mazzo comune, a caso. Le altre 7 carte di classe, mescolate e coperte, sono la tua pila di classe. Niente draft.

**R 3.8 Niente Equipaggiamento iniziale (D26).** In preparazione nessuno equipaggia carte: il primo Equipaggiamento si gioca nel proprio turno, con le regole di R 4.2. La regola v6 dell'Equipaggiamento gratis è tolta il 12/11.

**R 3.9 Partenza (v6).** Tira il D6 e metti la pedina sulla Partenza con quel numero. Se è occupata o accanto a un altro eroe, ritira. Quella è la tua **Partenza iniziale** per tutta la partita (D7). Le 6 Partenze sono stampate sulla base, numerate da 1 a 6 in senso orario (coordinate nel §17).

**R 3.10 Primo giocatore (v6).** Chi ha visto per ultimo un goblin prende la pedina di Geronimo e gioca per primo. Poi si va in senso orario (tocca a sinistra).

**R 3.11 In 3–4 giocatori (v6).** «Un avversario» o «l'avversario»: scegli tu quale. «Ogni avversario» o «entrambi»: tutti gli avversari.

## 4. Il turno, la regola magna e la catena

### 4.0 Il turno

| Momento | Cosa fai |
|---|---|
| Inizio | Peschi 1 carta: dal mazzo comune oppure dalla tua pila di classe (R 12.3) [PLAYTEST]. Vale la mano massima (R 12.4). |
| 1 · Muovi | Tiri D6 + MOV: il tiro apre una catena (R 4.7). Poi ti muovi fino a quel numero di esagoni, almeno 1 (R 8.4). |
| 2 · Esplora | Risolvi l'esagono dove ti sei fermato (R 8.9). Al massimo uno scontro per turno (v6). |
| 3 · Fine | Nell'ordine: (a) ultimo momento per giocare carte; (b) finiscono gli effetti «in questo turno» e «prossimo…» di tutti, e le Profezie non ancora verificate; (c) togli i tuoi Stati dritti e raddrizza quelli di traverso (R 9.1); (d) togli le tue tessere Usato dei poteri «una volta per turno» (R 4.15); (e) le carte nella tua zona delle carte giocate vanno nei tuoi scarti e togli i tuoi segnaposto Usato (R 4.4): qui si chiude il tuo periodo di 2 carte; (f) rifornimento delle «?» (R 8.11); (g) tocca al giocatore alla tua sinistra. |

### 4.1 Regole complete (per carte e simulatore)

**R 4.1 Regola magna (D9).** Tutte le carte tranne gli Equipaggiamenti si giocano in qualsiasi fase, nel tuo turno e in quello degli altri, anche in risposta.

**R 4.2 Equipaggiamenti (D4).** Solo nel tuo turno e solo per aprire una catena: mai in risposta, mai mentre una catena è aperta. Al massimo 1 per turno (v6) [PLAYTEST] (N3). Quando l'Equipaggiamento si risolve, lo infili nello slot del suo tipo. Se lo slot è occupato, il vecchio oggetto va nei tuoi scarti (v6). Poi giri subito le rotelle, PL compreso.

**R 4.3 Limite di carte (D9).**
- Ogni giocatore gioca al massimo 2 carte tra una sua Fine del turno e la successiva.
- Ogni giocatore gioca al massimo 1 carta in ogni catena.
- Contano tutte le carte giocate dalla mano: Incanti, Equipaggiamenti, Mappe, anche quelle annullate o rimaste senza bersaglio.
- Non contano: i poteri delle Carte Classe, la Forte Volontà, gli effetti degli Equipaggiamenti già in gioco e le carte scartate come costo o per la mano massima. Scartare una carta non è giocarla.

**R 4.4 Zona delle carte giocate.**
- Ogni carta che giochi resta davanti a te fino alla TUA Fine: scoperta finché il suo effetto dura, poi a faccia in giù. Alla tua Fine va nei tuoi scarti (v6, esteso ai turni degli altri).
- Un Equipaggiamento finisce nello slot e una Mappa accanto alla plancia. Al loro posto metti davanti a te una tessera Usato, che togli alla tua Fine [PLAYTEST] (N4).
- Così, in ogni momento, carte + segnaposto davanti a te = carte giocate nel periodo (massimo 2).

**R 4.5 Aprire una catena.**
- Si apre una catena giocando una carta quando non c'è nessuna catena aperta.
- Se più giocatori vogliono aprirne una nello stesso momento, comincia chi ha il turno, poi gli altri in senso orario [PLAYTEST] (N13).

**R 4.6 Il giro delle risposte (D4).**
- Dopo la carta che apre la catena rispondono gli altri, uno alla volta, in senso orario, cominciando da chi siede a sinistra di chi l'ha aperta.
- Ognuno, una volta sola, gioca 1 carta sopra la pila oppure passa.
- Il giro si chiude con il giocatore alla destra di chi ha aperto la catena. Chi l'ha aperta non aggiunge altre carte.

**R 4.7 La catena di un tiro.**
- Un tiro fatto fuori da una catena apre una catena come se fosse una carta. Vale per iniziativa, tiro per colpire, danno, movimento, Indizio, D6 della perdita e D6 della Trappola.
- Il tiro non è una carta: chi ha tirato non ha ancora giocato in quella catena, quindi risponde per primo (1 carta o passa). Poi rispondono gli altri in senso orario; il giro si chiude con il giocatore alla destra di chi ha tirato [PLAYTEST] (N1).
- Per i tiri fatti per un mostro il giro comincia da chi ha il turno.
- Il tiro resta «aperto» finché la sua pila non è vuota; poi si applica il risultato: colpito o mancato, passi, danni, Indizio, slot perso.

**R 4.8 Risoluzione LIFO (D4).** Chiuso il giro, si risolve prima l'ultima carta giocata e poi le altre, andando indietro fino alla prima. Se la catena l'ha aperta un tiro, alla fine resta il tiro con il suo valore finale.

**R 4.9 Una catena alla volta (D4).**
- Durante il giro delle risposte e mentre la pila si risolve non si apre un'altra catena. Le carte si giocano solo come risposte nel giro.
- I tiri fatti mentre la pila si risolve (per esempio il D6 di danno di un Incanto) non aprono catene: si possono cambiare solo con effetti automatici (R 4.12).

**R 4.10 Bersaglio sparito.** Se, quando la carta si risolve, il suo bersaglio non c'è più (mostro a 0 PV, eroe sconfitto o fuggito, carta annullata), la carta non fa niente. Resta nella tua zona delle carte giocate (conta per il limite) e va negli scarti alla tua Fine. Quello che hai pagato per giocarla resta pagato.

**R 4.11 Annullare.** «Annulla una carta» colpisce una carta che sta sotto di lei nella stessa pila. Quando l'annullamento si risolve, la carta annullata si gira a faccia in giù e non si risolverà. Resta nella zona delle carte giocate del suo giocatore e conta per il suo limite.

**R 4.12 Effetti automatici.**
- Sono effetti automatici: i poteri delle Carte Classe, gli effetti degli Equipaggiamenti già in gioco, la Forte Volontà, le abilità dei mostri e gli Stati.
- Si applicano subito quando succede il loro evento, anche durante il giro delle risposte o mentre la pila si risolve. Stanno fuori dalla pila, nessuno può rispondere, non aprono catene e non contano per il limite.
- Quelli volontari si usano quando il loro testo lo permette. «Un D6 appena tirato» vuol dire: finché quel tiro è aperto (R 4.7).

**R 4.13 Chi vince le ricompense [PLAYTEST] (N11).** Le ricompense di uno scontro vanno sempre all'eroe che lo combatte, anche se il colpo finale l'ha dato la carta di un altro giocatore.

**R 4.14 Durate.**
- «In questo turno», «prossimo…» e «fino alla fine del turno» finiscono alla Fine del turno in corso, chiunque abbia il turno.
- Ciò che dura di più è uno Stato di 1 turno (§9) oppure l'effetto di un Equipaggiamento («finché è equipaggiato»).
- Le Mappe valgono finché restano in gioco (R 10.11); le Profezie scadono come dice R 13.5.

**R 4.15 «Una volta per turno»** (Equipaggiamenti) vuol dire una volta tra una tua Fine e la successiva. Quando lo usi metti una tessera Usato sulla carta; la togli alla tua Fine.

**R 4.16 Momenti di gioco (modello del simulatore).** Al tavolo «in qualsiasi momento» vuol dire: quando non c'è una catena aperta. Il simulatore usa questi momenti fissi del turno attivo:
- M0 dopo la pesca;
- M1 prima del tiro di movimento;
- M2 arrivo: la pedina si è fermata e non ha ancora esplorato (è il momento di D10);
- M3 dopo aver girato tessera e carta, prima di risolverle o prima dell'iniziativa;
- M4 prima di ogni attacco, prima di decidere la fuga;
- M5 dopo lo scontro;
- M6 Fine (a).

In ogni momento si offre di aprire una catena prima a chi ha il turno, poi in senso orario. Dopo ogni catena si ricomincia da chi ha il turno. Il momento finisce quando tutti passano di seguito. In più ogni tiro apre la sua catena (R 4.7).

### 4.2 Testo per i giocatori (D17)

Da usare nel regolamento v7 (fase 6). È il §2.1 del piano, riscritto, con la regola R 4.7 sui tiri.

> - **Quando giochi.** Puoi giocare una carta quando vuoi, anche nel turno di un altro. Gli Equipaggiamenti no: solo nel tuo turno, e mai per rispondere.
> - **Quante carte.** Al massimo 2 tra la fine di un tuo turno e la fine del successivo. Le carte giocate restano davanti a te fino alla tua Fine: così le conti.
> - **Le risposte.** Quando qualcuno gioca una carta, gli altri possono rispondere, uno alla volta, in senso orario. Ognuno gioca 1 carta oppure passa. Il giro finisce con chi sta a destra di chi ha cominciato.
> - **Si risolve dall'ultima.** Finito il giro, si risolve prima l'ultima carta giocata, poi le altre, fino alla prima.
> - **Un giro alla volta.** Mentre le carte si risolvono non se ne gioca nessuna.
> - **I tiri.** Quando tiri i dadi parte un giro di risposte. Comincia da te: puoi giocare 1 carta sul tuo tiro, poi tocca agli altri.
> - **Bersaglio sparito.** Se il bersaglio non c'è più, la carta non fa niente. Quello che hai pagato resta pagato.
> - **Effetti automatici.** Carta Classe, Equipaggiamenti in gioco, Forte Volontà, mostri e Stati scattano subito. Nessuno risponde.
>
> **Esempio.** Anna tira 2D6 per colpire un mostro e fa 9: le basta 8. Anna passa. Bruno, alla sua sinistra, gioca una carta che le fa ritirare i dadi. Carla passa. Dario gioca una carta che annulla quella di Bruno. Il giro è finito: si risolve prima la carta di Dario, che annulla quella di Bruno. Anna tiene il 9 e colpisce. Senza Dario, Anna avrebbe ritirato con −1.

## 5. Ritiri (D1) e Forte Volontà

**R 5.1 Penalità.** Il ritiro numero n dello stesso tiro ha una penalità di n: −1 al primo ritiro, −2 al secondo, e così via. Vale per tutti i ritiri: carte, Forte Volontà, potere dello Stregone, Equipaggiamenti. «Stesso tiro» vuol dire il tiro aperto (R 4.7), chiunque faccia ritirare.

**R 5.2 Su 2D6** la penalità si toglie dal totale, anche se si ritira un dado solo. Forte Volontà e potere dello Stregone ritirano 1 dado.

**R 5.3 Verso della penalità [PLAYTEST] (N2).** La penalità peggiora sempre il risultato per chi ha fatto il tiro. Nei tiri in cui serve un numero basso si somma (+n) invece di togliersi: il D6 dell'Indizio (riesce se è ≤ LV + 1, D18; con LV 5 non si tira) e il D6 dei PV persi per una Trappola.

**R 5.4 Minimo [PLAYTEST].** Il risultato di un D6 singolo con la penalità non scende sotto 1. Esempio: il D6 della perdita ritirato con lo Scudo del Goblin (TE-10) vale almeno 1.

**R 5.5 Modificatori [PLAYTEST].** I (+N)/(−N) giocati su un tiro restano sul tiro anche se i dadi si ritirano.

**R 5.6 Profezie [PLAYTEST].** Le Profezie guardano le facce dei dadi, non il risultato con penalità e modificatori (R 13.5).

**R 5.7 Esempio.** ATT 2 contro un mostro con AR 8. Esce 3 + 2 = 5, totale 7: mancato. Con la Forte Volontà ritiri il 2 ed esce 5: 3 + 5 + 2 − 1 = 9, colpito. Se poi un avversario ti fa ritirare di nuovo, il nuovo totale ha −2.

**R 5.8 Forte Volontà (v6).**
- È un segnalino nel cerchio della plancia eroe. Ne hai al massimo 1: un'altra non si accumula.
- Scartala per ritirare 1 D6 che hai appena tirato. In un tiro di 2D6 ne ritiri uno solo.
- Si ottiene vincendo contro il mazzetto 2 (D11), vincendo un Duello (R 10.10) e con le carte che lo dicono (per esempio TI-10 Caffè Doppio Ristretto, TE-01 Maschera carbonifera e il ripiego di CS-06 Ehm, tecnicamente no).
- È un effetto automatico (R 4.12).

## 6. Power level e mazzetti dei mostri (D2)

**R 6.1 PL degli Equipaggiamenti [PLAYTEST].** Comune 1, Rara 2, Leggendaria 3. Il PL è stampato sulla carta.

**R 6.2** Incanti, Mappe, Carte Classe e Carte Specie non hanno PL. Gli Incanti durano poco; le Mappe non vanno negli slot.

**R 6.3 PL dell'eroe.** È la somma dei PL degli Equipaggiamenti negli slot: da 0 a 12 (4 slot da 3). Sta sulla rotella PL; giri la rotella quando equipaggi o perdi un oggetto.

**R 6.4 Mazzetto [PLAYTEST].** PL 0–3 → mazzetto 1; PL 4–7 → mazzetto 2; PL 8 o più → mazzetto 3. Il PL si legge quando giri la carta Mostro: se cambia durante lo scontro, il mostro resta quello.

**R 6.5 Le statistiche non crescono mai da sole.**
- Partono da PV 5, PV massimi 5, ATT 1, MOV 1, AR 9, più la Carta Specie.
- Cambiano solo con gli Equipaggiamenti (finché sono equipaggiati), gli Stati (1 turno) e le carte giocate (per la loro durata).
- Non esistono PE, livelli, tabella dei livelli, «+1/+2 al passaggio di livello», né bonus permanenti dagli Incanti.

**R 6.6 Rotelle (v6).** Le rotelle mostrano sempre il valore finale con l'equipaggiamento. I bonus temporanei (Incanti, Stati, Mappe) non girano le rotelle: li sommi quando servono.

**R 6.7** Chi viene sconfitto perde Equipaggiamenti col D6 della perdita (§11), quindi perde PL e torna a mazzetti più facili. Non esce dal gioco.

**R 6.8 Mazzetti (v6 raddoppiati il 10/11, D20; AR con D19).**
- Mazzetto 1: 26 mostri di LV 1–2 (NE-01…13 della v6, NE-29…41 nuovi).
- Mazzetto 2: 16 mostri di LV 3–4 (NE-14…21 della v6, NE-42…49 nuovi).
- Boss: 6 di LV 5 (NE-26…28 della v6, NE-50…52 nuovi). Uno fa da custode (R 3.2); gli altri 5 sono il mazzetto 3.
- Abilità (D20): ogni mostro ha un'abilità che nessun altro dei 48 ha, pesata sul suo LV. Le abilità v6 che erano doppioni sono state cambiate (NE-10, NE-13, NE-15, NE-16, NE-20, NE-27, NE-28; la `nota` della carta dice com'era); le altre restano quelle della v6, alcune con un nome nuovo. Le formule delle abilità sono nel §14.5 («Abilità dei mostri»).
- Statistiche: i 24 mostri della v6 tengono PV, ATT e LV della v6 (salvo NE-20, ATT 4 → 3 per la sua Nebbia); i 24 nuovi hanno PV, ATT e AR dentro la fascia dei mostri v6 del loro LV [PLAYTEST].
- L'AR, statica e scritta sulla carta di ogni mostro, è quella della v6 ridotta del 25 % e arrotondata per eccesso (D19): 8 → 6, 9 → 7, 10 → 8, 11 → 9, boss e custode compresi; i mostri nuovi sono nati con l'AR già ridotta. Va da 6 a 9. L'AR degli eroi non cambia (parte da 9).

## 7. Scontro con i mostri

**R 7.1 Inizio.** Gira la prima carta del mazzetto del tuo PL (R 6.4) e metti la Rotella dello scontro sui suoi PV.

**R 7.2 Chi attacca per primo (v6).**
- Tu e il mostro tirate 1 D6 a testa e attacca per primo il più alto. Per il mostro tira il giocatore alla tua destra; in 2 giocatori, l'avversario.
- Pareggio: contro un mostro vince l'eroe; contro un boss (del mazzetto 3 o il custode) vince il boss.
- Senza tiro: Agguato (NE-14, «attacca per primo») fa attaccare per primo il mostro; Monologo (NE-52, «attacchi sempre per primo tu, senza tiro») fa attaccare per primo l'eroe, anche se è un boss e anche da custode. Nessun altro mostro salta il tiro.
- Metti la carta Mostro dritta se attacchi per primo tu, di traverso se attacca per primo il mostro.
- Opzione: OP-1.

**R 7.3 Tiro per colpire.** Chi attacca colpisce se 2D6 + il suo ATT è uguale o maggiore dell'AR del bersaglio. Non esistono Difesa né «8 + AR». L'AR del mostro è sulla carta (da 6 a 9, D19); quella dell'eroe è sulla rotella (parte da 9).

**R 7.4 Danno (v6), solo se colpisci.**
- Eroe: D6 più i «(+N) Danni» delle carte. ATT serve solo per colpire.
- Mostro: LV 1 → D6 − 1 (minimo 1); LV 2 → D6; LV 3 e oltre → D6 + 1.
- Non ci sono colpi critici. Opzione: OP-2.

**R 7.5 Turni d'attacco e limite di 3 attacchi [PLAYTEST] (D26).**
- Si attacca una volta a testa, a turno, finché qualcuno arriva a 0 PV. Ogni danno fa scendere la Rotella dello scontro o la rotella PV.
- Contro un mostro l'eroe fa al massimo **3 attacchi** (conta ogni attacco, anche quello senza tiro di TE-26). Se dopo il 3° attacco dell'eroe il mostro è ancora vivo, quando toccherebbe a lui attaccare invece **scappa**: lo scontro finisce senza ricompense, la tessera rossa va tra le usate (lascia la «?») e la carta Mostro va in fondo al suo mazzetto. L'eroe resta dove si è fermato.
- Il custode di MIMI non scappa mai: lo scontro col custode va avanti senza limite e le sue ferite restano sulla Rotella del custode (R 10.7). I boss del mazzetto 3 invece scappano come gli altri mostri.
- Il Duello non ha questo limite (R 10.9).

**R 7.6 Vantaggio e svantaggio (v6).** Tiri due volte i 2D6 e tieni il totale migliore (vantaggio) o il peggiore (svantaggio). Se li hai tutti e due, si annullano.

**R 7.7 Abilità «la prima volta» (v6).** Quando scatta, metti una tessera Usato sulla carta Mostro; la togli a fine scontro.

**R 7.8 Fuga (v6).**
- Prima di ogni tuo attacco contro un mostro puoi fuggire: torni sull'esagono dove eri a inizio turno, senza ricompense, e passi alla Fine.
- La tessera rossa resta scoperta (R 8.5) e la carta Mostro va in fondo al suo mazzetto.
- Non si fugge dal custode né dai mostri che lo vietano (NE-09). Dal Duello non si fugge. Alcune abilità cambiano la fuga: NE-08, NE-12, NE-30, NE-44; con NE-29 è il mostro che scappa (§14.5).

**R 7.9 Fine dello scontro.**
- Se vinci: ricompense (R 10.3); la tessera va tra le usate; la carta Mostro va in fondo al suo mazzetto.
- Se il mostro scappa dopo il tuo 3° attacco (R 7.5): niente ricompense; la tessera va tra le usate; la carta Mostro va in fondo al suo mazzetto.
- Se perdi: §11.
- I boss del mazzetto 3 non tengono le ferite. Il custode sì, sulla Rotella del custode (v6): per questo le carte dei boss dicono «Da custode, le sue ferite restano tra uno scontro e l'altro.»
- Se un'abilità del mostro gli toglie PV (Televoto di NE-51) e lo porta a 0, lo scontro è vinto come con un attacco; se è il custode, vinci la partita (R 10.12).

**R 7.10 Uno scontro per turno (v6).** Contano gli scontri con un mostro, con il custode e il Duello.

**R 7.11** I danni dati dalle carte fuori da uno scontro possono portare un eroe a 0 PV: è una sconfitta (§11).

**R 7.12 Opzioni di playtest (piano §5).** Sono proposte del 9/11. OP-3 e OP-4 sono state adottate il 10/11 (D19, D18) e ora sono regola di base (R 6.8, R 10.2). OP-1, OP-2 e OP-5 restano non decise: la regola di base è quella sopra e il simulatore le prova una alla volta e insieme.

| Opzione | Regola | Cosa cambia se si adotta |
|---|---|---|
| OP-1 | Contro i mostri l'eroe attacca sempre per primo: niente iniziativa. | Nessuna carta comune o di classe v7 dice «se attacchi per primo» (le v6 TE-15 e TI-37 sono state riscritte in CR-07 e CR-10). Tra i mostri: da riscrivere Agguato (NE-14); Picchiata (NE-16) scatterebbe sempre; a Monologo (NE-52) resterebbe solo il (+1) Danni. Da decidere se vale anche contro i boss. |
| OP-2 | Il mostro colpisce se 2D6 + ATT ≥ AR dell'eroe; il danno è pari al suo ATT, senza dado. | Riga «Danno» delle 48 carte Mostro; le abilità legate al dado del danno del mostro (NE-21, NE-26, NE-43); Carte Aiuto. |
| OP-3 | Adottata il 10/11 (D19): AR dei mostri −25 % arrotondata per eccesso, da 8–11 a 6–9. | Fatto: AR delle carte Mostro (R 6.8). |
| OP-4 | Adottata il 10/11 (D18): Indizio con D6 ≤ LV del mostro + 1; con LV 5 è garantito. | Fatto: riga delle ricompense delle carte Mostro (R 10.2). |
| OP-5 | Duello: in caso di pari vince il MOV più alto, poi si ritira (invece di «vince lo sfidante»). | Testo del Duello. |

Il danno degli eroi resta comunque quello della v6. Nel Duello restano i dadi per colpire e per il danno.

## 8. Mappa, movimento ed esplorazione (D6, D16, D24, D25)

**R 8.1 Mappa a fiori (D24) [PLAYTEST].**
- La mappa è la base stampata (R 2.5) più i 14 fiori, montati col draft o con un preset (R 3.1). Gli stessi pezzi servono a tutte le mappe: nessun pezzo appartiene a un tema.
- Ogni fiore va dentro uno spazio disegnato sulla base, mai a cavallo di due spazi.
- Con qualunque posa (spazio, faccia, rotazione) gli esagoni percorribili restano tutti collegati, grazie alla regola di disegno dei fiori (§17).
- I **preset** sono le 10 mappe del §17: la base «Strettoie» e una per ogni Mappa TM-01…09 (R 8.12). Si montano con gli stessi 14 fiori, ognuno in uno spazio, faccia e rotazione fissi.
- Le tile del D23, i loro preset 10 × 10 e la composizione libera con le tile non si usano più: il draft prende il posto della composizione libera.
- Il regolamento non dipende mai da linee di strada disegnate: dove si passa lo dice il tipo di esagono (R 8.3).

**R 8.2 Geometria e coordinate (D24).**
- 12 × 12 esagoni con la punta in alto; le righe dispari sono spostate a sinistra di mezzo esagono. Esagono di 25,2 mm da lato a lato (circa 29,1 mm da punta a punta): ci stanno le Tessere Esplorazione da Ø 24 mm e le pedine. Montata, la mappa misura circa 315 × 269 mm (333 × 283 mm con la fascia delle coordinate).
- Coordinate (x, y): x è la colonna (1–12), y la riga (1–12). Sono stampate sui quattro lati della base. Per trovare (x, y) scendi fino alla riga y e conta x esagoni lungo la riga.
- 144 esagoni: i 46 di bordo stampati sulla base (6 Partenze, 4 ostacoli singoli, gli altri liberi) e i 98 dei 14 fiori.
- Ostacoli e acqua coprono in media circa il 26 % della mappa (24–28 % nei draft simulati), quasi tutti lontano dal bordo.
- Non c'è un fiume fisso. L'acqua sta solo nei fiori (laghi e tratti di fiume con il loro guado o ponte); se due fiori d'acqua si toccano, il fiume continua.
- Elenco dei fiori, delle Partenze e dei preset nel §17.

**R 8.3 Tipi di esagono (D25) [PLAYTEST].**
- **Libero:** ogni esagono che non è un ostacolo né accidentato: strada, erba, mattonato, pavimento, guado, ponte, Partenza. Per le regole sono tutti uguali; il disegno è solo ambientazione.
- **Ostacolo:** bosco, rocce, case. Non ci entri e non li attraversi.
- **Accidentato** (parola chiave): ci entri e ti ci fermi; entrarci costa 1 passo normale, uscirne costa 1 passo in più (R 8.4). Per ora l'unico terreno accidentato è l'acqua senza ponte né guado. In futuro ci potranno essere altri terreni accidentati.
- **Percorribile** vuol dire libero o accidentato.
- Tutti i lati tra due esagoni sono aperti: i muri del D23 non esistono più (D24).

**R 8.4 Movimento [PLAYTEST] (D25).**
- Muovi fino a D6 + MOV passi, almeno 1, un esagono alla volta sugli esagoni percorribili, cambiando direzione quando vuoi.
- Entrare in un esagono costa 1 passo. Uscire da un esagono accidentato costa 1 passo in più: il passo che ti porta fuori dall'acqua (anche in altra acqua) costa 2. Con 1 passo entri in acqua; per uscirne servono almeno 2 passi.
- Non entri negli ostacoli.
- Passi sopra agli altri eroi, ma non ti fermi sul loro esagono.
- Se non puoi muoverti di almeno 1 esagono, resti fermo ed esplori dove sei.
- Conta solo l'esagono dove ti fermi: passare su una «?» non la gira.
- I MOV in più «in questo turno» e quelli di una Mappa si sommano al tiro, senza girare la rotella (v6).

**R 8.5 Sbarramenti [PLAYTEST: fermata].**
- Un mostro scoperto (tessera rossa a faccia in su) sbarra il passaggio: non puoi attraversare il suo esagono. Puoi fermarti lì anche se ti avanzano dei passi, e lo affronti.
- Vale lo stesso per la Cripta con MIMI e il custode.
- Gli eroi non sbarrano mai il passaggio.

**R 8.6 Effetti che spostano una pedina** (per esempio TI-25 Ritardare l'inevitabile): non possono farla finire su un ostacolo né sull'esagono di un altro eroe. Su un esagono accidentato sì: lo spostamento di una carta non conta i passi.

**R 8.7 «Accanto» e «a una casella di distanza» [PLAYTEST] (piano §11).** Due esagoni sono accanto se hanno un lato in comune. Vale per il Duello e per le carte che colpiscono «un avversario accanto» (per esempio TI-01, CA-03, CS-01; nella v6 dicevano «a una casella di distanza»). Gli ostacoli non contano: due eroi accanto stanno sempre su due esagoni percorribili, anche d'acqua.

**R 8.8 Partenze e Cripta (D24, D25) [PLAYTEST].**
- Le 6 **Partenze** sono esagoni liberi stampati sulla base (coordinate nel §17): ci si passa e ci si ferma.
- La **Cripta** è un segnalino: non è stampata. Si mette quando il tesoro viene individuato (R 10.6) e si sposta quando il tesoro cambia Cripta (R 10.11). Ci si passa e ci si ferma, salvo quando c'è MIMI (R 8.5).
- **Tiro della Cripta:** tira 2D6 per la colonna x e 2D6 per la riga y e metti la Cripta su (x, y). Il risultato va da 2 a 12, quindi la riga 1 e la colonna 1 non hanno mai la Cripta.
- Se (x, y) è un **ostacolo** o una **Partenza**, la Cripta va sull'esagono percorribile più vicino che non sia una Partenza, non abbia una «?» e non stia in riga o colonna 1. Le distanze si contano in esagoni, ostacoli compresi. A pari distanza vince quello più in alto (y più piccola), poi quello più a sinistra (x più piccola).
- Sull'**acqua** la Cripta resta lì.
- Su una **«?»** la Cripta resta lì: il segnaposto «?» e la sua tessera (coperta o scoperta) vanno nella riserva, coperti.
- La Cripta con MIMI sbarra il passaggio come un mostro scoperto (R 8.5).

**R 8.9 Esplora: dove ti fermi.**

| Esagono | Cosa succede |
|---|---|
| «?» con tessera coperta | Gira la tessera. **Blu:** gira la prima carta Imprevisti, fai quello che dice, mettila in fondo al mazzo; la tessera va tra le usate. **Rossa:** scontro con la prima carta del mazzetto del tuo PL (§7). |
| «?» senza tessera | Esagono percorribile: non succede niente. |
| Tessera rossa scoperta | Scontro con la prima carta del mazzetto del TUO PL (v6). |
| Cripta con MIMI | Con 3 Indizi o più: scontro con il custode (R 10.7). Con meno: non succede niente. |
| Accanto a un altro eroe (R 8.7) | Se in questo turno non hai avuto scontri, puoi sfidarlo a Duello (R 10.8). |
| Altro esagono percorribile, Partenza, Cripta senza MIMI | Niente (salvo il Duello). |

**R 8.10 Carte Imprevisto v7.**

| Imprevisto | Testo |
|---|---|
| Trappola (5) | Perdi D6 − 1 PV (minimo 1), poi tira il D6 della perdita di equipaggiamento. (v6; D7) |
| Locanda (2) | Recuperi 2 PV e riprendi in mano 1 carta dai tuoi scarti. [PLAYTEST] (piano §3, al posto del PE) |
| Fonte (2) | Riprendi in mano fino a 2 carte dai tuoi scarti. (v6) |
| Fabbro (2) | Riprendi in mano 1 Equipaggiamento dai tuoi scarti. (v6) |

La mano massima vale per Locanda, Fonte e Fabbro (R 12.4). Nessun testo v7 parla del «sacchetto» (piano §8.4, V10): le v6 TE-01 Elmo sorgisogno e TE-20 Tunica del Viandante sono diventate CR-05 e parte di TE-25, e la Carta Aiuto è rifatta.

**R 8.11 Tessere «?» consumabili (opzione A) [PLAYTEST].**
- Chi si ferma su una «?» con la tessera coperta la gira (R 8.9).
- Una tessera blu, dopo l'Imprevisto, va tra le usate. Una tessera rossa va tra le usate se l'eroe vince o se il mostro scappa dopo 3 attacchi (R 7.5). Se l'eroe fugge o perde, resta scoperta sulla «?» e sbarra il passaggio (R 8.5).
- Rifornimento, alla Fine di ogni turno: se sulla mappa restano 6 tessere coperte o meno [PLAYTEST: soglia 6], metti una tessera coperta su ogni «?» vuota. Le tessere scoperte non contano come vuote. Prendi prima dalla riserva, poi dalle usate mescolate a faccia in giù. Se finiscono, le «?» restanti restano vuote.
- I segnaposto «?» non si spostano durante la partita, salvo con la Cripta (R 8.8) e con il cambio di mappa (R 8.12).

**R 8.12 Cambio di mappa: 3 fiori per Mappa [PLAYTEST] (D24).**
- Il Cuore della v6 non c'è più (R 2.6).
- Il foglio di ogni Mappa (§17) ha 3 righe «spazio · fiore e faccia · freccia 1–6». Quando una Mappa si risolve, prima fai il suo testo (R 10.11), poi cambi i 3 fiori del foglio. Vale allo stesso modo se la mappa in gioco viene da un draft o da un preset. Quando una Mappa lascia il gioco e nessun'altra la sostituisce (TI-22), applichi le 3 righe del foglio «Strettoie».
- Il cambio, in ordine:
  1. Alza le pedine degli eroi. Togli i segnaposto «?» dagli spazi che cambiano (i 3 spazi indicati e quelli che ricevono un fiore con uno scambio): i segnaposto e le loro tessere, coperte o scoperte, tornano nella riserva, coperti. Contali.
  2. Applica le 3 righe, una dopo l'altra. Se il fiore indicato sta in un altro spazio, scambialo con quello che occupa lo spazio indicato: il fiore tolto va nello spazio liberato con la sua faccia e la sua freccia. Poi gira il fiore indicato sulla faccia e sulla freccia della riga.
  3. Chi ha giocato la carta rimette altrettanti segnaposto «?» sugli spazi cambiati, su esagoni percorribili ad almeno 2 esagoni da ogni Partenza, uno per esagono. Le «?» nuove sono vuote: le tessere arrivano col rifornimento normale (R 8.11).
  4. Il tesoro cambia Cripta (R 10.11): tiro della Cripta di R 8.8. Prima del 3° Indizio non c'è Cripta e non si tira.
- A ogni cambio di mappa ogni eroe, anche chi ha giocato la carta, torna sulla sua Partenza iniziale (R 3.9). Non è una sconfitta: niente D6 della perdita; PV, mano, Indizi, Stati ed Equipaggiamenti restano.
- Se la mappa cambia durante uno scontro o un Duello, questo finisce subito senza vincitore e senza ricompense: la tessera resta scoperta (salvo che il suo spazio cambi: passo 1), la carta Mostro va in fondo al suo mazzetto e il custode tiene le ferite.
- Non cambiano: la base (Partenze e ostacoli singoli), i fiori degli altri spazi, le «?» sugli altri esagoni con le loro tessere, MIMI e il custode (che seguono la Cripta).
- Se il cambio a metà partita sia praticabile al tavolo si prova nei playtest (§19, N26).

## 9. Stati e tessere

**R 9.1 Durata di uno Stato (v6).** Uno Stato vale esattamente un tuo turno intero, il prossimo. Se lo prendi nel tuo turno mettilo di traverso; se lo prendi nel turno di un altro, mettilo dritto. Alla tua Fine togli gli Stati dritti, poi raddrizza quelli di traverso.

**R 9.2** Non puoi avere due Stati uguali: se ne prendi uno che hai già, rimettilo come se lo prendessi ora (v6).

**R 9.3** Uno Stato che dice «poi toglilo» si toglie anche appena lo usi (v6).

**R 9.4** Gli Stati non girano le rotelle: sommi il loro bonus quando serve (v6).

**R 9.5** Non esistono clessidre, turni persi né turni extra.

**R 9.6 Stati v6 (restano):** Rallentato (−), Occhio (+), Sussurro (+), Riflesso (+), Silenzio (−), Fede (+), con i testi di `stati.csv`.

**R 9.7 Stati nuovi [PLAYTEST] (piano §7).**
- Vantaggio (+): «I tuoi tiri per colpire si fanno con vantaggio.»
- Svantaggio (−): «I tuoi tiri per colpire si fanno con svantaggio.»
- Fermo (−): «Muovi: non ti muovi; esplori dove sei.»

Il catalogo (fase 2) può aggiungerne altri con un testo di massimo 3 righe sulla tessera 26 × 18 mm. Le durate lunghe delle carte di Desy si convertono in Stati di 1 turno.

**R 9.8 Tessera Usato.** Si usa per:
- i poteri delle Carte Classe: resta fino alla fine della partita;
- gli effetti «una volta per turno» (R 4.15);
- le abilità «la prima volta» dei mostri (R 7.7);
- i segnaposto delle carte giocate (R 4.4).

## 10. Indizi, ricompense, Duello, tesoro e vittoria (D10, D11)

**R 10.1 Da dove arrivano gli Indizi (v6).**
- Dai mostri sconfitti (R 10.2), dai Duelli vinti, dalle carte che lo dicono (per esempio lo Stato Sussurro) e dalla regola del tesoro individuato (R 10.6).
- Locanda, Fonte, Fabbro e Trappole non danno Indizi. Nessuno parte con un Indizio. Non c'è un massimo per giocatore.

**R 10.2 Tiro per l'Indizio (D18).** Quando sconfiggi un mostro tira 1 D6: prendi 1 Indizio se il risultato è uguale o minore del LV stampato sulla carta + 1 (LV 1 → 1–2, LV 2 → 1–3, LV 3 → 1–4, LV 4 → 1–5). Con LV 5 (i boss del mazzetto 3) l'Indizio è garantito e non si tira. La carta Mostro stampa la soglia («Indizio se D6 ≤ 2») oppure «Indizio garantito». Era OP-4.

**R 10.3 Ricompense (D11) [PLAYTEST].**

| Vinci contro | Prendi |
|---|---|
| Mazzetto 1 | solo il tiro per l'Indizio |
| Mazzetto 2 | Forte Volontà + il tiro per l'Indizio |
| Mazzetto 3 | nessun altro premio: solo l'Indizio, garantito con LV 5 (R 10.2) |
| Custode di MIMI | la partita (R 10.12) |
| Un eroe in Duello | R 10.8–10.10 |

Nessuna ricompensa fa pescare carte: ogni premio che fa pescare va prima pesato col simulatore, sempre col tetto di 10 (D11). Le carte Mostro v7 non stampano più «1 PE» né «+1 livello».

**R 10.4** Se un eroe va a 0 PV per una carta giocata da un avversario fuori da un Duello, è una sconfitta normale e chi ha giocato la carta non prende ricompense (v6, [PLAYTEST]).

**R 10.5 Ricompense e carte altrui.** Vedi R 4.13 [PLAYTEST].

**R 10.6 Individuare il tesoro (v6, [PLAYTEST]).**
- Appena metti il 3° Indizio sulla plancia eroe hai individuato il tesoro.
- Ogni altro eroe prende subito 1 Indizio. Succede solo la prima volta, quando MIMI compare.
- Se MIMI non è ancora sulla mappa, fai il tiro della Cripta (R 8.8: 2D6 per la colonna, 2D6 per la riga) e metti la Cripta, MIMI e il custode su quell'esagono.

**R 10.7 Affrontare il custode (v6).**
- Solo chi ha 3 Indizi o più, fermandosi sulla Cripta di MIMI nel proprio turno. Con meno di 3 Indizi fermarsi lì non fa niente.
- Pareggio dell'iniziativa: attacca prima il custode (salvo Monologo, NE-52: R 7.2). Dal custode non si fugge.
- Le sue ferite restano sulla Rotella del custode: il prossimo lo trova già ferito.
- Chi perde un Indizio e scende a 2 non può sfidarlo finché non ne trova un altro.

**R 10.8 Il Duello: la sfida e il rifiuto (v6).**
- Se finisci il movimento accanto a un altro eroe (R 8.7) e in questo turno non hai avuto scontri, puoi sfidarlo.
- **Primo giro (D26):** finché tutti non hanno fatto il loro primo turno, non si sfida a Duello e nessuno gioca carte contro un avversario (Daniele, 12/11 22:55).
- Lo sfidato può rifiutare: lo sfidante prende 1 carta a caso dalla mano dello sfidato e la tiene (vale R 12.4 per lo sfidante). Il Duello non si fa.

**R 10.9 Svolgimento del Duello (v6).**
- Si decide chi attacca per primo con 1 D6 a testa. Pareggio: vince il MOV più alto; se è pari anche quello, vince chi ha il turno (lo sfidante). Opzione: OP-5.
- Ognuno tira i propri dadi: per colpire 2D6 + ATT ≥ AR, danno D6 + bonus.
- Dal Duello non si fugge. Gli Stati valgono anche nel Duello.
- L'eccezione v6 «chi si difende gioca 1 carta» non serve più: vale la regola magna (R 4.1).

**R 10.10 Esito del Duello [PLAYTEST] (D11).** Chi vince prende 1 Indizio dallo sconfitto (se ne ha), riprende in mano 1 carta a scelta dagli scarti dello sconfitto (vale R 12.4) e prende la Forte Volontà. Il PE della v6 sparisce. Chi perde subisce la sconfitta normale (§11).

**R 10.11 Mappe (v6 + D10).**
- Una Mappa cambia la mappa per tutti (R 8.12). Resta accanto alla mappa finché un'altra Mappa la sostituisce; quella vecchia va negli scarti di chi l'aveva giocata.
- Se MIMI è sulla mappa, il tesoro cambia Cripta: togli la Cripta e rifai il tiro della Cripta (R 8.8); se la Cripta finisce sullo stesso esagono, ritira. MIMI e il custode si spostano con la Cripta e con le ferite. Gli Indizi restano a tutti. Prima che qualcuno abbia individuato il tesoro non c'è la Cripta e il tesoro non si sposta.
- Le Mappe si giocano anche in risposta (D10), anche per spostare il tesoro mentre un eroe arriva sulla Cripta: nel momento M2 (R 4.16), prima che l'eroe esplori. La mappa cambia e ogni eroe torna sulla sua Partenza iniziale (R 8.12): l'eroe non è più sulla Cripta, non esplora e non affronta il custode, anche se il tesoro non si è spostato.
- Il MOV di una Mappa vale per tutti finché è in gioco.

**R 10.12 Vittoria (D11).** La partita finisce solo quando un eroe sconfigge il custode di MIMI: quell'eroe riporta il forziere a Geronimo e vince. Nessun altro effetto fa vincere o perdere la partita.

## 11. Perdita dell'equipaggiamento e sconfitta (D7)

**R 11.1 D6 della perdita.**

| D6 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Perdi | tutti gli Equipaggiamenti | l'Elmo | l'Arma DX o lo Scudo | l'Arma SX | l'Armatura | niente |

Con 2–5, se lo slot è vuoto non perdi niente. Le carte perse vanno nei tuoi scarti; giri le rotelle, PL compreso.

**R 11.2** Ogni effetto che dice «perdi l'equipaggiamento» si risolve con questo D6 (D7). Per esempio la Trappola, e L'inizio del viaggio di Desy riscritta: «ogni eroe tira il D6 della perdita».

**R 11.3 Fuori dal D6 [PLAYTEST] (piano §11).**
- I costi scelti da te (per esempio «Sacrifica un tuo Equipaggiamento», R 13.2) e gli effetti su un oggetto preciso (per esempio Calice del sangue acido) seguono il testo della carta.
- Sulle carte «distruggi un Equipaggiamento» vuol dire: mettilo negli scarti del suo proprietario.

**R 11.4 Sconfitta (0 PV), in quest'ordine.**
1. Tira il D6 della perdita. L'Assaltatore può saltarlo con il potere di TC-01.
2. Torna sulla tua Partenza iniziale (R 3.9), senza tiro. Se è occupata da un altro eroe, vai su un esagono percorribile libero accanto a lei, a tua scelta [PLAYTEST].
3. Gira i PV sui PV massimi. Tieni gli Indizi, la mano e gli Stati.
4. Pesca 1 carta dal mazzo comune (vale R 12.4).
5. Se ti ha sconfitto un mostro, la sua tessera rossa resta scoperta sulla «?» e la carta Mostro va in fondo al suo mazzetto. Se ti ha sconfitto il custode, il custode tiene le ferite.
6. Se era il tuo turno, passi alla Fine.

**R 11.5** Se una Trappola ti porta a 0 PV, fai la sconfitta normale con un solo tiro di perdita (v6, [PLAYTEST]).

**R 11.6** Chi perde un Duello subisce la sconfitta normale. Il vincitore prende quello che dice R 10.10.

## 12. Mano, pesca e riciclo (D8)

**R 12.1 Mazzetto di classe:** 10 carte su 20 (R 3.6) [PLAYTEST].

**R 12.2 Mano iniziale:** 3 carte di classe a scelta + 3 comuni a caso (R 3.7) [PLAYTEST].

**R 12.3 Pesca [PLAYTEST].**
- All'inizio di ogni tuo turno, anche il primo, peschi 1 carta: dal mazzo comune oppure dalla tua pila di classe, a scelta.
- Alla morte peschi 1 carta dal mazzo comune (D7).
- Altre pesche solo dalle carte e dal potere del Giullare.

**R 12.4 Mano massima (D8).**
- Non hai mai più di 10 carte in mano, in nessun momento.
- Ogni volta che una carta deve entrarti in mano e ne hai già 10, PRIMA scarti 1 carta a scelta dalla mano (scendi a 9) e POI la prendi (torni a 10).
- Vale per: pesca a inizio turno, pesca alla morte, ricompense, carte prese a un avversario, carte riprese dagli scarti, carte ricevute da un altro giocatore, il +1 del Giullare.
- Con «pesca 2» (o più) lo fai per ogni carta, una alla volta.
- La carta scartata va nei tuoi scarti.

**R 12.5 Parole delle carte.**
- «Pesca» senza altro vuol dire: dal mazzo comune. Per pescare dalla pila di classe la carta lo deve dire.
- «Riprendi» e «recupera» vogliono dire: dai tuoi scarti in mano.
- «Ruba» vuol dire: da un avversario alla tua mano.

**R 12.6 Riciclo (piano §4).**
- Quando devi pescare dal mazzo comune e il mazzo è finito, si prendono le carte comuni dagli scarti di tutti, si mescolano e formano il nuovo mazzo comune.
- Le carte di classe restano negli scarti: tornano solo con gli effetti di recupero (Fonte, Locanda, carte).
- Se la tua pila di classe è finita, peschi dal mazzo comune. Se non ci sono carte comuni né nel mazzo né negli scarti, non peschi.

**R 12.7** Ogni giocatore ha la sua pila degli scarti, a faccia in su (v6). La tua mano è segreta; il numero di carte che hai in mano è pubblico [PLAYTEST]: serve alle carte del tipo «se l'avversario ha più carte di te».

## 13. Le classi (D3, D12, D13)

**R 13.1 Regole comuni.**
- Il «potere» è l'effetto della Carta Classe, che si usa una volta per partita (D12). Dopo l'uso ci metti sopra una tessera Usato.
- È un effetto automatico (R 4.12): non è una carta, non conta per il limite e nessuno risponde.
- Le Carte Classe non danno statistiche (v6).
- Ogni classe ha esattamente 20 carte di classe: 10 verso la direzione A e 10 verso la direzione B (D22).
- In fondo alla Carta Classe, al posto della riga «Mano» della v6, si stampa «Mazzetto: 10 delle 20 carte di classe · Mano: 3 + 3» [PLAYTEST].

| Classe | Carta Classe (testo) | Meccanica | Direzione A | Direzione B |
|---|---|---|---|---|
| Assaltatore | TC-01 (v6, invariata): «La tua pedina è un Assaltatore fino alla fine della partita. Una volta per partita, quando vieni sconfitto, puoi non tirare il D6 della perdita di equipaggiamento: non perdi niente. Poi metti una tessera Usato su questa carta.» | Sacrificio (R 13.2) | A «Spaccatutto»: sacrifica armatura ed equipaggiamento per avere più ATT e Danni | B «Armadio a due ante»: AR, parate, meno Danni, Equipaggiamenti che tornano in gioco |
| Ricercatore | TC-02 (D12): «La tua pedina è un Ricercatore fino alla fine della partita. Una volta per partita guarda fino a 3 carte in cima a un mazzetto Mostri o al mazzo Imprevisti e rimettile nell'ordine che preferisci. Poi metti una tessera Usato su questa carta.» | Scry (R 13.3) | A «Ficcanaso»: scry sui mazzi (mostri, imprevisti, comune), movimento, trappole | B «Mani lunghe»: guarda la mano degli altri, ruba, sceglie cosa pescheranno |
| Stregone | TC-03 (v6, invariata): «La tua pedina è uno Stregone fino alla fine della partita. Una volta per partita, anche nel turno di un altro, puoi far ritirare 1 D6 appena tirato: tuo, di un avversario o tirato per un mostro. Vale il nuovo risultato. Poi metti una tessera Usato su questa carta.» | Incanti propri (R 13.4) | A «Fumo e fiamme»: Incanti d'attacco con il dado in più | B «So tutto io»: contromagia, ritiri, Silenzio |
| Oracolo | TC-04 nuova [PLAYTEST] (piano §11): «La tua pedina è un Oracolo fino alla fine della partita. Una volta per partita, quando sbagli una Profezia, considerala indovinata. Poi metti una tessera Usato su questa carta.» | Profezie (R 13.5) | A «Ci ho preso!»: Profezie sui tuoi tiri; se indovini ti curi, peschi, prendi ATT o AR | B «Malocchio»: Profezie sui tiri degli altri e dei mostri; se indovini, chi ha tirato subisce Danni, scarta o perde l'effetto |
| Giullare | TC-05 (D13): «La tua pedina è un Giullare fino alla fine della partita. Una volta per partita scarta quante carte vuoi dalla mano, poi pesca dal mazzo comune altrettante carte più 1 (mai più di 10 in mano). Poi metti una tessera Usato su questa carta.» | Scarto come risorsa, mill (R 13.6) | A «Gioco di mano»: consuma il proprio mazzo, scarta e pesca, recupera dagli scarti, più effetti quante più carte ha scartato | B «Carta nella manica»: fa scartare gli altri, scambia mani e carte, regala carte inutili |

I testi delle Carte Classe vanno da 176 a 264 caratteri; TC-03 è già stampata così nella v6.

**R 13.2 Assaltatore: il sacrificio.**
- «Sacrifica un tuo Equipaggiamento» (oppure «la tua Armatura», «il tuo Elmo»…) è un costo. Scegli un Equipaggiamento nei tuoi slot, mettilo nei tuoi scarti e gira le rotelle, PL compreso.
- Il costo si paga quando giochi la carta e resta pagato anche se la carta non fa niente (R 4.10). Non è il D6 della perdita (R 11.3).
- Se non hai l'oggetto, il costo non si può pagare e vale solo l'effetto base.
- Il sacrificio alza il tetto dei numeri: il bonus pagato con un sacrificio può arrivare a (+3) anche su una Comune o una Rara [PLAYTEST] (N14, §14.4).
- Esempio del piano (A), scritto con le formule del §14.5: «Via la corazza, fa caldo!: (+1) a un tuo tiro. Se sacrifichi la tua Armatura: (+3) invece, e (+2) Danni se il tiro colpisce.»

**R 13.3 Ricercatore: lo scry.**
- «Guarda le prime N carte di un mazzo e rimettile nell'ordine che vuoi»: le guardi solo tu [PLAYTEST], poi le rimetti in cima nell'ordine che scegli.
- Mazzi ammessi: un mazzetto Mostri a scelta (1, 2 o 3) [PLAYTEST], il mazzo Imprevisti, il mazzo comune. «Al massimo» N: se il mazzo ne ha meno, le guardi tutte.
- Potere TC-02: si usa in qualsiasi momento in cui si potrebbe aprire una catena, anche nel turno di un altro [PLAYTEST] (N7).

**R 13.4 Stregone: gli Incanti e il dado in più.**
- Il potere TC-03 è un ritiro: ha la penalità di D1 (R 5.1). In un tiro di 2D6 ritira 1 dado (v6).
- Incanto d'attacco: un Incanto che infligge Danni con un tiro di dado.
- «Dado in più» (direzione A «Fumo e fiamme»): quando un tuo Incanto d'attacco tira i dadi del danno, tiri 1 D6 in più e scarti il più basso [PLAYTEST] (N6; variante da simulare: lo sommi). Vale solo per le carte che lo dicono.

**R 13.5 Oracolo: le Profezie.**
- **Rotella della Profezia:** 10 posizioni: 1, 2, 3, 4, 5, 6, Pari, Dispari, Alto, Basso.
- **Come si gioca:** la carta Profezia è un Incanto: si gioca come le altre carte (limite, catena). Quando si risolve, ottieni subito l'effetto base. Poi giri la rotella sulla Profezia scelta e lasci la carta scoperta davanti a te.
- **Verifica [PLAYTEST] (piano §6.5):** la verifica il primo tiro di dadi fatto dopo che la carta si è risolta, di chiunque, anche di un mostro, ritiri compresi.
  - Si guardano le facce, senza ATT, bonus o penalità (R 5.6).
  - Su un D6: la faccia. Alto = 4+, Basso = 3− [PLAYTEST].
  - Su 2D6: la somma delle facce. Alto = 8+, Basso = 6− [PLAYTEST]; Pari e Dispari sulla somma.
  - Valore esatto su 2D6: indovini se almeno un dado mostra quel valore [PLAYTEST] (N5).
- **Esito:** se indovini, ottieni il bonus: piccolo per Pari, Dispari, Alto, Basso; grande per il valore esatto. Se sbagli, niente; TC-04 può trasformare una volta per partita una Profezia sbagliata in indovinata.
- **Scadenza:** la Profezia scade quando viene verificata o, al più tardi, alla Fine del turno in corso. Poi la carta si gira a faccia in giù (resta nella zona delle carte giocate).
- **Una alla volta:** ogni Oracolo ha una sola Profezia attiva. Una nuova sostituisce la vecchia, che scade senza bonus [PLAYTEST].
- **Probabilità** (per chi scrive le carte e per il simulatore):
  - D6: Pari, Dispari, Alto e Basso 1/2; valore esatto 1/6.
  - 2D6: Pari 1/2, Dispari 1/2, Alto 15/36 (42 %), Basso 15/36 (42 %); valore esatto (un dado) 11/36 (31 %).
- Le vecchie carte di cura e difesa dell'Oracolo (Benedizione del Parroco, Bacino sulla Bua, Fede Incrollabile (Quasi), Preghiera Fatta di Fretta) passano al mazzo comune (piano §6.5).
- Esempio del piano (A): «Presagio di luce: recuperi 2 PV. Profezia: se indovini, recuperi altri 2 PV (Pari/Dispari/Alto/Basso) oppure tutti i PV (valore esatto).»

**R 13.6 Giullare: scarta e pesca, mill.**
- Potere TC-05 (D13): scarti k carte (k da 0 a quante ne hai) e poi peschi k + 1 carte dal mazzo comune, una alla volta, con la mano massima (R 12.4). Se arrivi a 10 prima di aver pescato tutto, per ogni carta che manca prima ne scarti 1 e poi peschi.
- «Scarta 1 carta: …» è un costo: dalla tua mano, a scelta, nei tuoi scarti. Si paga quando giochi la carta.
- **Mill** (direzione B «Carta nella manica»): fai scartare carte dalla mano di un avversario (a sua scelta, oppure «a caso» se la carta lo dice), scambi carte tra le mani, dai carte a un avversario. Per chi riceve vale R 12.4.
- «Scambia» vuol dire: 1 carta contro 1 carta, salvo che la carta dica un numero.
- Esempio del piano (B): «Barare al tavolo: scambia 1 carta della tua mano con 1 carta a caso della mano di un avversario. Se l'avversario ha più carte di te: scambiane 2.»

## 14. Contratto per le carte

Vale per le 100 carte di classe (`v7/stampa/sorgenti/dati/classi/<classe>.csv`, un file per classe) e per le 81 carte del mazzo comune (`v7/stampa/sorgenti/dati/carte_comuni.csv`: 31 TE, 41 TI, 9 TM; 63 prima di D22). Il simulatore (`v7/simulatore/effetti.csv`) e i generatori leggono solo questi campi. Le Carte Classe (TC), le Specie (TS), i Mostri (NE), gli Imprevisti (IM) e gli Stati (ST) restano nei loro CSV.

### 14.1 Campi (una riga CSV per carta)

Intestazione, uguale in tutti i file: `id,tipo,nome,classe,direzione,pl,rarita,slot,testo,testo_situazionale,nota,battuta`. Non c'è una colonna `fonte`: la provenienza sta in `nota`. L'ultima colonna `battuta` è facoltativa.

| Campo | Valori ammessi | Note |
|---|---|---|
| `id` | Mazzo comune: `TE-nn` Equipaggiamento, `TI-nn` Incanto, `TM-nn` Mappa. Carte di classe: `CA-nn` Assaltatore, `CR-nn` Ricercatore, `CS-nn` Stregone, `CO-nn` Oracolo, `CG-nn` Giullare, da 01 a 20 (01–05 e 11–15 direzione A; 06–10 e 16–20 direzione B, D22). | Gli id sono stabili: il simulatore e il regolamento li citano. Non si rinumera: si cambiano testo, rarità e PL. Il mazzo comune è numerato da 01 per tipo (10/11); l'id v6 da cui viene una carta sta in `nota`. |
| `tipo` | `TE`, `TI`, `TM` | `genera_carte.py` accetta anche `Equipaggiamento`, `Incanto`, `Mappa`. Nel mazzo comune il prefisso dell'`id` è il `tipo`. |
| `nome` | testo | Una riga sola: al massimo circa 26 caratteri [INFERENZA: titolo a 10,5 pt su circa 152 pt in `genera_carte.py`; i nomi più lunghi si controllano col generatore]. |
| `classe` | `Tutte le classi` nel mazzo comune; `Assaltatore`, `Ricercatore`, `Stregone`, `Oracolo`, `Giullare` nei file di classe | Una sola, uguale al file. Niente carte con due classi (piano §7). Il generatore accetta anche `Comune` al posto di `Tutte le classi`. |
| `direzione` | `A` o `B` per le carte di classe; vuoto nel mazzo comune | Il nome della direzione viene dalla tabella di R 13.1 e si stampa nella riga del tipo, con la lettera nel tondo del colore della classe. |
| `pl` | `1`, `2`, `3` per gli Equipaggiamenti; vuoto per Incanti e Mappe | Uguale alla rarità: Comune 1, Rara 2, Leggendaria 3 (R 6.1). Si stampa nel riquadro dell'illustrazione. |
| `rarita` | `Comune`, `Rara`, `Leggendaria` | Sempre piena: si stampa in fondo alla carta. |
| `slot` | `Elmo`, `Arma DX / Scudo`, `Arma SX`, `Armatura` | Solo per gli Equipaggiamenti. Un solo slot per carta. |
| `testo` | testo | Effetto base, usabile in ogni situazione. |
| `testo_situazionale` | testo o vuoto | Una sola frase: «Se …: …» oppure, per l'Oracolo, «Profezia: se indovini …». Si stampa in corsivo sotto il testo. |
| `nota` | testo libero, non si stampa | Provenienza (v6 con il vecchio id, Desy, nuova), riscalatura, motivazioni, revisioni. Se contiene la parola «segnaposto», la carta porta la scritta rossa SEGNAPOSTO. |
| `battuta` | testo o vuoto (ultima colonna, facoltativa) | Al massimo 70 caratteri. Solo colore: mai regole. Si stampa in corsivo nel riquadro dell'illustrazione. |

**Tono.** Nomi e battute hanno il tono goliardico alla Munchkin: si ride, mai solenne. Il testo delle regole resta invece fatto di formule esatte, senza scherzi (D21).

### 14.2 Controlli (validazione meccanica)

- **V1** `id` unico in tutti i file del §14.1. Il prefisso corrisponde al `tipo` nel mazzo comune (TE, TI, TM) e alla classe nei file di classe (CA, CR, CS, CO, CG).
- **V2** Per ogni classe: esattamente 20 carte, 10 con `direzione` A e 10 con B (vincolo, D22). Nel mazzo comune `direzione` è vuota.
- **V3** `pl` è pieno solo per gli Equipaggiamenti ed è uguale al valore della rarità.
- **V4** `slot` è pieno se e solo se il `tipo` è TE.
- **V5** `testo` non è vuoto e non comincia con «Se», «Giocabile solo» o «Solo se». Deve fare qualcosa in ogni situazione (vincolo: effetto generico sempre usabile).
- **V6** Le carte che agiscono in risposta (annullare, parare, ritirare) hanno il ripiego dentro `testo`. Il ripiego non fa pescare (Desy: la pesca è fortissima): Forte Volontà, uno Stato, (+N) a un prossimo tiro o uno scry. Esempio (CS-06): «Annulla un Incanto nella catena. Se non c'è nessun Incanto da annullare: ottieni la Forte Volontà.» (piano §6.1). Gli Incanti di danno non hanno ripiego: aspettano un bersaglio, come TI-01 e TI-02.
- **V7** `testo_situazionale` è vuoto oppure è una sola frase che comincia con «Se » o con «Profezia». Non esiste mai senza `testo`.
- **V8** Lunghezza di `testo` + `testo_situazionale` ≤ 260 caratteri (circa 9 righe nel riquadro). Decide `genera_carte.py`, che si ferma se un testo non entra nel riquadro: si accorcia il testo, mai il corpo.
- **V9** Numeri entro il tetto di rarità (§14.4). Il vantaggio di carte netto (carte che entrano in mano, meno la carta giocata, meno le carte scartate come costo) è al massimo +1 per Comune e Rara e +2 per Leggendaria [PLAYTEST]. Un effetto che si ripete («una volta per turno», un oggetto che torna in mano) non dà carte nette: al massimo uno scambio alla pari, come «scarta 1 carta: pesca 1 carta».
- **V10** Parole vietate: «D20», «d20», «D4», «1d4», «Difesa», «PE», «livello» riferito all'eroe (il «LV» dei mostri va bene), «clessidra», «cubetto», «sacchetto», «Ispirazione», «PF».
- **V11** Durate vietate: «per N turni», «per 1d6 turni», «perdi N turni», «turno extra», «permanente», «per il resto della partita». Si usano gli Stati di 1 turno (§9) oppure «finché è equipaggiato».
- **V12** Vietati «vinci la partita» e «perdi la partita» (D11), boss nuovi, alleati e pedine nuove nelle carte comuni e di classe: Ombra deforme e Discesa Yumaniana sono fuori dalla v7 (D15); Ristom e Ammondius! sono state ripensate (TI-30, TI-26). I 3 boss nuovi del mazzo Mostri (NE-50…52) vengono da D20 e hanno la loro sagoma (R 2.5).
- **V13** Ogni Profezia ha: effetto base in `testo`; in `testo_situazionale` il bonus piccolo (Pari/Dispari/Alto/Basso) e il bonus grande (valore esatto).
- **V14** Mappe solo nel mazzo comune [PLAYTEST]. Il testo di ogni Mappa comincia con «Il tesoro cambia Cripta.», come le Mappe v6 e quelle di Desy.
- **V15** Composizione consigliata di ogni direzione (10 carte) [PLAYTEST, D22]: da 4 a 8 Equipaggiamenti e almeno 2 Incanti; al massimo 2 Leggendarie. Per i nuovi id 11–20, in ogni gruppo di 5 carte (11–15 o 16–20): da 2 a 4 Equipaggiamenti, almeno 1 Incanto, al massimo 1 Leggendaria.
- **V16** Ogni carta usa solo le formule e le condizioni del §14.5. Una formula nuova va aggiunta prima al §14.5, perché il simulatore deve implementarla.

### 14.3 Regole di scrittura (piano §6.1)

- Prima l'effetto base, che funziona sempre: +N a un tiro, ritiro, pesca o scarto, cura, danno a un bersaglio qualsiasi, annullare una carta. Poi, al massimo, una riga «Se…» con il bonus situazionale.
- Le carte v6 e quelle di Desy che oggi sono solo situazionali ricevono un effetto generico (elenco nel piano §7).
- Gli Equipaggiamenti con effetti continui cominciano con «Finché è equipaggiato…», concordato col nome: equipaggiata, equipaggiati, equipaggiate (v6). «Una volta per turno» segue R 4.15.
- Si scrive per 2–4 giocatori: «un avversario» (scegli tu) e «ogni avversario» (tutti), non «l'avversario» o «entrambi» (R 3.11). «Quell'avversario» rimanda a quello già scelto.
- «Creatura» vuol dire un mostro o un boss, mai un eroe (v6, [PLAYTEST]).
- Parole fisse (revisione del 10/11): «in questo turno», mai «fino a fine turno»; «lo Stato X» con la maiuscola, solo con gli Stati di `stati.csv`; i numeri che cambiano statistiche, tiri e Danni tra parentesi, (+N) e (-N), anche sulle carte Mostro; «Danno» e «Danni» con la maiuscola quando sono la quantità («1 Danno», «(+1) Danni»), mentre «il dado del danno» resta minuscolo; «tira il D6 della perdita»; «sacrifica» per ogni Equipaggiamento che il proprietario mette negli scarti come costo.

### 14.4 Riscalatura dal D20 ai 2D6 [PLAYTEST]

Desy ha scritto i numeri per un D20, dove +1 vale il 5 %. Sui 2D6, a metà scala, +1 vale circa il 15 %. I valori piccoli restano uguali; quelli grandi si comprimono.

| Desy (scala D20) | v7 (2D6) |
|---|---|
| (±1) o (±2) a ATT («AT»), AR o tiro per colpire («tiri per colpire») | uguale |
| da (±3) a (±5) | (±2) |
| (±6) o più, «2d6 a una statistica», «+1d6 a una statistica» | (±3) solo su una Leggendaria, altrimenti (±2) |
| «+1 a tutte le statistiche» | solo su una Leggendaria: (+1) ATT, MOV e AR |
| MOV ±N (il MOV è già su D6) | uguale, entro il tetto |
| PV massimi +N | (+1) per Comune e Rara, (+2) per Leggendaria |
| Danni «1d6» | D6 |
| Danni «2d6» | D6 + 2, solo su Rara o Leggendaria |
| Danni «1d6 + AT» | D6 (D6 + 1 su una Rara): l'ATT serve solo per colpire |
| «1d4» | D6 − 1 (minimo 1): nel kit ci sono solo D6 |
| Cure «1d6» / «2d6» / «tutti i PV» | D6 / D6 + 2 / «tutti i PV» solo su una Leggendaria |
| Vantaggio o Svantaggio «per il resto della partita» | Stato di 1 turno; «finché è equipaggiato» solo su una Leggendaria |
| «Distruggi» un Equipaggiamento | mettilo negli scarti del proprietario (R 11.3) |
| «Uccidi / distruggi un nemico» | mai contro il custode (R 10.12) |

**Tetto per rarità** (per ogni numero fisso sulla carta): Comune e Rara al massimo 2, Leggendaria al massimo 3. Eccezione: il bonus pagato con un sacrificio (R 13.2) può arrivare a 3 anche su Comune e Rara [PLAYTEST] (N14).

### 14.5 Formule ammesse

Ogni effetto delle carte usa una di queste formule (V16). Tra parentesi, per le formule aggiunte il 10/11, le carte che le usano.

**Tiri**

| Formula sulla carta | Significato |
|---|---|
| «(+N) a un tiro» / «(+N) a un tuo tiro» / «(+N) o (-N) a un tiro» | Modificatore su un tiro aperto: si gioca nella sua catena (R 4.7). «Un tiro» è di chiunque, anche di una creatura. |
| «(+N) al tuo prossimo tiro per colpire» | Vale per il prossimo tiro di quel tipo, entro la Fine del turno in corso. |
| «(+N) ATT / AR / MOV in questo turno» | Bonus temporaneo; non gira le rotelle. |
| «Ritira il tiro» / «Ritira un tuo tiro» / «Fai ritirare 1 D6 di un tiro aperto» / «puoi ritirare il tuo tiro di movimento» | Ritiro con la penalità di D1 (§5). Nessuna carta toglie la penalità. (TE-27, TE-30, CO-14) |
| «Gira 1 D6 di un tiro aperto sulla faccia che vuoi. Conta come un ritiro, con la sua penalità» | Il dado mostra la faccia scelta (vale anche per le Profezie, R 5.6); per il resto è un ritiro: penalità di R 5.1 e divieti dei ritiri (NE-47). (CS-19) |
| «Con vantaggio» / «con svantaggio» | R 7.6. «Le creature tirano per colpire con svantaggio»: ogni loro tiro per colpire, per la durata scritta (CS-09, TM-05). |
| «Dado in più» | R 13.4; al massimo 1 per tiro (§15). |
| «Tira 1 D6. Con 1–2: …; con 3–4: …; con 5–6: …» / «Poi tira 1 D6. Con 6: …» | Tiro fatto mentre la carta si risolve: non apre una catena (R 4.9). Le fasce che non sono scritte non fanno niente. (TI-20, CA-12, CA-14, CG-12, CR-13, CR-19) |
| «Il tiro per l'Indizio riesce con D6 ≤ LV + N» | Cambia la soglia di R 10.2 finché la carta è in gioco; con LV 5 l'Indizio resta garantito. (TM-09) |

**Danni e cure**

| Formula sulla carta | Significato |
|---|---|
| «(+N) Danni» / «(+N) Danni ai tuoi attacchi» / «(+N) Danni al tuo prossimo attacco» | Si somma al danno se il tiro colpisce. «Al tuo prossimo attacco»: il prossimo entro la Fine del turno; se manca, il bonus è perso. |
| «(-N) ai Danni del prossimo attacco che subisci» / «… di ogni attacco che subisci in questo turno» / «(-N) ai Danni di un attacco contro di te» | Riduzione del danno di quel colpo, dopo il tiro: minimo 0, entro la Fine del turno. La stessa formula vale per le creature: «(-1) ai Danni che subisce (minimo 1)» (NE-19). (CA-07, CA-06, CA-16, CA-17, CA-18) |
| «Infliggi N Danni / D6 Danni a una creatura / a un avversario accanto» / «… anche a un altro bersaglio» / «… a ogni altro avversario accanto» | Danno diretto, senza tiro per colpire. «Un altro bersaglio»: diverso dal primo. (CS-11, CS-12, CS-14, CA-12) |
| «Invece di tirare per colpire puoi infliggere N Danni a chi stai attaccando» | Al posto del tiro per colpire di quell'attacco: niente tiro, niente catena del tiro, niente «(+N) Danni ai tuoi attacchi»; poi lo scontro prosegue. (TE-26) |
| «Ogni eroe, tu compreso, …» | Ogni eroe al tavolo, anche chi gioca la carta; con un solo tiro per tutti se la carta lo dice. (TI-32, TI-38) |
| «Subisci N Danni» / «l'attaccante subisce N Danni» / «chi ha tirato subisce N Danni» | Danno diretto senza tiro a chi dice la carta, anche se non è accanto. (CA-06, CA-17, TE-09, Oracolo direzione B) |
| «Annulla i Danni di un attacco contro di te / di una Trappola / di un Incanto» | Parata: quel danno diventa 0. Per la Trappola: niente PV persi, il D6 della perdita si tira lo stesso. |
| «Recuperi N PV» | PV su, mai oltre i PV massimi. |
| «Perdi N PV» | La rotella PV scende di N. Non sono Danni di un attacco: niente parata, niente Riflesso. (TI-20) |
| «Chi recupera PV con una carta ne recupera (+N)» / «le Trappole fanno perdere N PV in più» | Cambia quel risultato finché la carta è in gioco o equipaggiata. (TE-05, TM-07, TM-08) |
| «Scendi a 1 PV» | Giri la rotella PV su 1; non è una sconfitta. (TI-25) |

**Carte**

| Formula sulla carta | Significato |
|---|---|
| «Pesca N carte» / «Pesca 1 carta dalla tua pila di classe» | R 12.4–12.5. |
| «Scarta N carte» / «Scarta 1 carta: …» | Dalla tua mano, a scelta (oppure «a caso»); come costo si paga quando giochi la carta. |
| «Un avversario / ogni avversario scarta N carte» (a sua scelta, «a caso») | Dalla sua mano: sceglie lui, salvo «a caso». «Un avversario sceglie: A oppure B»: sceglie lui. (TI-29, CO-07, CO-08, CG-10) |
| «Riprendi N carte [N Incanti / N Equipaggiamenti] dai tuoi scarti» | In mano; vale R 12.4. Con il tipo scritto, solo carte di quel tipo. (CS-18, TE-29) |
| «Prendi in mano 1 carta [1 Equipaggiamento] a scelta dagli scarti di un avversario» | Come il premio del Duello (R 10.10); vale R 12.4. (CG-08, TI-39, CA-20) |
| «Ruba 1 carta a caso dalla mano di un avversario» / «… prima guarda la sua mano e scegli tu la carta» | Va nella tua mano; vale R 12.4. (CR-07, CR-09, CR-17) |
| «Guarda la mano di un avversario / di ogni avversario» / «Guarda N carte a caso della mano di un avversario» | Solo informazione: le vedi solo tu e restano nella sua mano. (CR-06, CR-09, CG-09, CR-18, CR-19, CR-20) |
| «Scambia N carte della tua mano con N carte (a caso / a scelta / di quelle N) della mano di un avversario» | Prima scegli le tue, poi prendi le sue; il numero di carte in mano non cambia (R 13.6). (CG-06, CG-09, CG-16, CR-18, TI-35) |
| «Dai N carte della tua mano a un avversario / al giocatore alla tua destra» / «un avversario ti dà 1 carta a sua scelta dalla sua mano» | Sceglie chi dà; chi riceve segue R 12.4. Se tutti danno insieme, prima ognuno sceglie le sue, poi si passano. (CG-18, CG-20, TI-38) |
| «Scarta fino a N carte e pescane altrettante» / «Scarta tutte le carte comuni che hai in mano e pescane altrettante» | Prima scarti, poi peschi una alla volta (R 12.4). Con «tutte le carte comuni» le carte di classe restano in mano. (CG-07, CG-14, TI-35) |
| «Prendi in mano N carte a caso tra le carte di classe rimaste nella scatola di una classe che non è la tua» | Carte fuori dalla partita (R 3.6): le giochi come le altre, poi vanno nei tuoi scarti. (TI-28) |
| «Guarda le prime N carte di un mazzo e rimettile nell'ordine che vuoi» / «guarda la prima carta e lasciala in cima oppure mettila in fondo al mazzo» | Scry (R 13.3). «Quando una tua carta Incanto o Equipaggiamento ti fa guardare le prime N carte … ne guardi N + 1»: vale solo per lo scry delle carte, non per il potere TC-02. (CG-11, CR-11, CR-12, CR-14, CR-16, CS-17) |
| «Guarda N tessere coperte su N «?» e rimettile coperte: al loro posto oppure scambiate tra loro» | Le vedi solo tu (R 8.9); nessuna tessera si gira. (CR-14) |

**Stati e segnalini**

| Formula sulla carta | Significato |
|---|---|
| «Prendi lo Stato X» / «Un avversario / ogni avversario [accanto] prende lo Stato X» | §9. Gli Stati sono quelli di `stati.csv`. (CG-14, CR-19, CS-15 e altre) |
| «Toglie i suoi Stati (+)» / «Togli i tuoi Stati (−)» | Rimette nella riserva le tessere Stato con quel segno. (CO-06, CO-19, CR-20) |
| «Ottieni la Forte Volontà» | Se non ce l'hai già (R 5.8). |

**Equipaggiamenti**

| Formula sulla carta | Significato |
|---|---|
| «Finché è equipaggiato ottieni (+N) …» (equipaggiata, equipaggiati, equipaggiate secondo il nome) | Bonus dell'Equipaggiamento: gira la rotella quando entra o esce dallo slot. Le altre righe della carta valgono anche loro solo finché è equipaggiato. |
| «Quando lo equipaggi: …» | Una volta, quando l'Equipaggiamento si risolve ed entra nello slot. (TE-01…05, TE-17, CR-07) |
| «Una volta per turno: …» | R 4.15. |
| «Quando lascia il tuo slot: …» | Effetto automatico (R 4.12) quando l'Equipaggiamento va negli scarti per qualsiasi motivo: sostituito, perso (D6 della perdita, sconfitta), sacrificato o distrutto. (TE-18, TE-25, CG-02) |
| «Quando colpisci…», «quando un attacco contro di te fallisce…», «ogni volta che infliggi Danni con un attacco…», «ogni volta che un attacco contro di te ti fa Danni…», «quando usi la Forte Volontà…», «se indovini una Profezia…», «quando sbagli una Profezia…», «quando giochi un Incanto [nel tuo turno]…», «quando un tuo Incanto infligge Danni…», «quando un tuo Incanto viene annullato…», «quando scarti una carta…», «quando sconfiggi una creatura…», «quando sacrifichi un altro tuo Equipaggiamento…», «quando inizi uno scontro con un mostro, prima di girarne la carta…» | Inneschi degli Equipaggiamenti in gioco: effetti automatici (R 4.12) al momento dell'evento; con «una volta per turno», R 4.15. «Quando giochi un Incanto»: appena entra nella catena, anche se poi viene annullato. (CA-13, CA-14, CA-17, CG-11, CG-12, CO-14, CO-15, CO-20, CR-12, CR-17, CS-11, CS-13, CS-17, CS-18, TE-28) |
| «Alla Fine di ogni tuo turno in cui non hai giocato carte Incanto: …» | Al punto (a) della tua Fine (§4.0), se in quel turno non hai giocato Incanti, nemmeno annullati. (TE-31) |
| «Sacrifica un tuo Equipaggiamento [con PL N o più] / la tua Armatura / il tuo Elmo: …» | Costo della carta (R 13.2). (CA-03 con PL 2 o più, CA-20) |
| «Sacrifica questo Scudo / questa Targa / questo Cesto / questo Gilet …: …» | Effetto automatico dell'Equipaggiamento in gioco (R 4.12), anche nel turno degli altri e mentre la pila si risolve; il costo è metterlo nei tuoi scarti. «Oppure N se sacrifichi questo X»: il sacrificio alza il numero (tetto di R 13.2). (CA-04, CA-05, CA-10, TE-08, TE-27, TE-30, CA-15, CA-17, CG-17, CS-12, CS-16) |
| «Tira il D6 della perdita» / «perdi l'equipaggiamento» | D6 della perdita (R 11.1). |
| «Non lo perdi mai per il D6 della perdita né per gli effetti degli avversari» | Il D6 della perdita lo salta, anche con 1; le carte degli avversari non lo toccano. Tu puoi sempre sacrificarlo o sostituirlo. (TE-14, CA-09) |
| «Un avversario mette nei suoi scarti un Equipaggiamento a tua scelta dai suoi slot …» | Distruzione (R 11.3), non è il D6 della perdita. (TE-17) |

**Mappe e tabellone**

| Formula sulla carta | Significato |
|---|---|
| «Il tesoro cambia Cripta» | R 10.11: si rifà il tiro della Cripta (R 8.8). Su una Mappa cambiano i suoi 3 fiori anche se il tesoro non si sposta (R 8.12). Fuori da una Mappa la mappa non cambia. (CR-15, CG-10) |
| «Finché è in gioco: …» (Mappe) | Vale finché la Mappa resta in gioco (R 10.11) e non gira le rotelle. «Tutti» = tutti gli eroi; «le creature» = mostri e boss; «ogni avversario» = gli avversari di chi l'ha giocata. |
| «Gli Elfi / i Sanguar tirano per colpire con vantaggio» | Gli eroi con quella Carta Specie (v6). |
| «Metti negli scarti di chi l'ha giocata la Mappa in gioco» | Si applicano le 3 righe del foglio «Strettoie» e ogni eroe torna sulla sua Partenza iniziale (R 8.12); il tesoro non si sposta, salvo che la carta lo dica. (TI-22, CR-15) |
| «Un avversario torna sulla sua Partenza iniziale» | Sposti la sua pedina sulla sua Partenza iniziale (R 3.9; se è occupata, R 11.4 punto 2). Non è una sconfitta. (TI-25) |
| «In questo turno i mostri scoperti non ti sbarrano la strada» | Passi sulle tessere rosse scoperte senza fermarti (R 8.5); la Cripta con MIMI sbarra ancora. (TI-40) |
| «Se è in gioco la Mappa X» | Condizione della riga «Se»: vale se quella Mappa è la Mappa in gioco. (CS-15) |

**Catena, scelte e durate**

| Formula sulla carta | Significato |
|---|---|
| «Annulla una carta / un Incanto / una Mappa nella catena» / «Annulla ogni Incanto nella catena» | R 4.11; serve il ripiego (V6). «Ogni»: tutti gli Incanti nella pila sotto questa carta, anche i tuoi. (TI-33, TI-34, CR-20) |
| «… un Incanto nella catena che ha come bersaglio solo te» / «una carta nella catena che ha come bersaglio un solo eroe cambia bersaglio: ora è l'eroe alla sinistra di quello» | Solo carte con un bersaglio scelto, che è un eroe; non le carte su «ogni avversario», su più eroi o sulle creature. Il nuovo bersaglio vale anche se non è accanto. (CS-16, TI-36) |
| «Scegli: A, oppure B» | Scegli quando la carta si risolve. |
| «In questo turno» / «in questo scontro» / «fino alla fine dello scontro» | R 4.14: finiscono alla Fine del turno in corso; quelle dello scontro anche prima, quando lo scontro finisce. |

**Scontro e creature**

| Formula sulla carta | Significato |
|---|---|
| «La creatura ha (±N) ATT / AR …» / «le creature hanno (-N) AR» / «una creatura ha ATT N» | Cambia le statistiche della creatura per la durata scritta; «ha ATT N»: l'ATT diventa N. (CR-03, TI-04, TI-30, TM-02) |
| «È sconfitta» (mai un boss né il custode) | La creatura va a 0 PV: lo scontro finisce come una vittoria dell'eroe che combatte (R 4.13, R 7.9). (TI-03) |
| «Invece fuggi e resti sul tuo esagono, senza ricompense» / «così fuggi e resti sul tuo esagono, senza ricompense» | Fuga (R 7.8) senza arretrare. (TI-08, TE-30) |
| «Sparisce, senza ricompense; la sua tessera va tra le usate e la carta in fondo al suo mazzetto» (mai il custode) | Lo scontro finisce come una fuga, ma la tessera rossa lascia la «?» (R 8.11) e tu resti dove sei. (TI-41) |
| «Non prende l'Indizio» | Il tiro per l'Indizio non dà l'Indizio, qualunque sia il risultato. (TI-19, CO-07) |
| «Alla Fine del turno …» | Si fa al punto (a) della Fine del turno in corso (§4.0). (TI-26) |

**Abilità dei mostri (D20, 10/11).** Le carte Mostro usano le formule sopra («(+N) Danni», «prendi lo Stato X», «scarti 1 carta», «il tesoro cambia Cripta», «tira 1 D6. Con 1–2: …»…) e queste. Un'abilità del mostro è un effetto automatico (R 4.12): non apre una catena. «Scegli» e «puoi» sulla carta Mostro sono dell'eroe che combatte.

| Formula sulla carta Mostro | Significato |
|---|---|
| «A inizio scontro …» / «appena lo giri …» | Dopo aver girato la carta e la Rotella dello scontro (R 7.1), prima di decidere chi attacca per primo (R 7.2). (NE-28, NE-40, NE-42, NE-51) |
| «… scegli: A, oppure B» | Sceglie l'eroe che combatte, quando l'abilità scatta. (NE-13, NE-28) |
| «Il giocatore che tira per lui / per lei (R 7.2)» | Il giocatore alla destra di chi combatte (in 2 giocatori, l'avversario), anche quando l'iniziativa non si tira. Lo Stato o la carta vanno a lui; la carta rubata vale R 12.4. (NE-32, NE-36) |
| «Ti attacca un'ultima volta» / «ti attacca subito una volta in più» | Un attacco del mostro in più (tiro per colpire e danno), fuori dal giro di R 7.5; poi lo scontro riprende da dov'era. (NE-08, NE-15) |
| «Quando va a 0 PV …» | Scatta appena la Rotella dello scontro arriva a 0, prima delle ricompense. «Non scendi sotto 1»: quei Danni non ti sconfiggono. (NE-07, NE-48) |
| «Quando scende a 1 PV scappa: è come se fuggissi tu (R 7.8), ma resti sul tuo esagono, senza ricompense» | Lo scontro finisce come una fuga: tessera rossa scoperta, carta in fondo al mazzetto, niente ricompense; tu non arretri. Un colpo che lo porta da 2 o più direttamente a 0 lo sconfigge [PLAYTEST]. (NE-29) |
| «Un 1 o un 2 al dado del suo danno vale 3» / «con un 6 al dado del danno» | Si guarda la faccia del dado del danno del mostro, dopo i ritiri; «vale N» cambia quel dado prima dei modificatori. Le Profezie si verificano sempre sulla faccia uscita (R 13.5) [PLAYTEST]. (NE-21, NE-26, NE-43) |
| «Ogni volta che lo manchi» / «ogni volta che un tuo tiro per colpire lo manca» / «se manca» | Scatta quando il tuo tiro per colpire contro quel mostro è risolto (catena chiusa, ritiri compresi) e non arriva alla sua AR. (NE-27, NE-37, NE-41) |
| «Perdi la Forte Volontà» / «se hai la Forte Volontà la perdi» | Il segnalino torna nella riserva; se non ce l'hai, niente. (NE-33) |
| «In questo scontro nessun tiro si può ritirare, né con le carte né con la Forte Volontà» | Vale per tutti i giocatori e per tutti i tiri, dal momento in cui giri la carta alla fine dello scontro: carte, Equipaggiamenti, potere dello Stregone e Forte Volontà. (NE-47) |
| «In questo scontro nessuno può giocare carte Incanto» | Vale per tutti i giocatori, dal momento in cui giri la carta alla fine dello scontro, anche per Incanti che non riguardano lo scontro; quelli già nella pila si risolvono [PLAYTEST]. (NE-49) |
| Danni che il mostro subisce dalla sua abilità («con 5–6: 2 Danni a lui») | Scendono sulla Rotella dello scontro o del custode. Se arriva a 0 PV lo scontro è vinto (R 7.9); se è il custode, vinci la partita (R 10.12). (NE-51) |
| «A fine scontro» | Quando lo scontro finisce con vittoria, sconfitta o fuga. Non scatta quando il mostro scappa dopo il 3° attacco dell'eroe (R 7.5, D26). (NE-02, NE-34) |
| «Finché ha tutti i suoi PV» / «con metà PV o meno» | Si legge sulla Rotella dello scontro. (NE-04, NE-15, NE-46) |
| «Ha (+N) ATT per ogni altra tessera rossa scoperta sulla plancia» | Contano le tessere rosse a faccia in su sulla plancia (R 8.5), non quella dello scontro. (NE-39) |
| «Per fare il tiro per l'Indizio devi prima scartare 1 carta a scelta» | Costo pagato dopo la vittoria; se non scarti, niente tiro e niente Indizio. (NE-38) |
| «La sua carta va in cima al mazzetto invece che in fondo» | Il prossimo che pesca da quel mazzetto lo ritrova. (NE-44) |
| «Attacchi sempre per primo tu, senza tiro» / «attacca per primo» | R 7.2. (NE-14, NE-52) |
| «Da custode, le sue ferite restano tra uno scontro e l'altro» | R 7.9, R 10.7: solo il custode; i boss del mazzetto 3 ripartono dai PV pieni. (NE-26…28, NE-50…52) |

**Profezie (Oracolo)**

| Formula sulla carta | Significato |
|---|---|
| «Profezia: se indovini un tuo tiro / un tiro altrui, … (Pari/Dispari/Alto/Basso) oppure … (valore esatto)» | R 13.5. «Tuo tiro» e «tiro altrui»: §15. Con vantaggio o svantaggio si verifica il tiro tenuto (§15). |
| «Chi ha tirato subisce / scarta / tira il D6 della perdita / non prende l'Indizio» | «Chi ha tirato» è l'avversario o la creatura del tiro altrui. Una creatura applica solo i Danni (§15), salvo che la carta dica cosa fa (CO-10). |
| «Scegli la Profezia, poi …» | Eccezione scritta sulla carta (CO-01): la Profezia si sceglie prima dell'effetto base e verifica il tiro ritirato. |
| «Considerala indovinata, solo per il premio piccolo (Pari/Dispari/Alto/Basso)» | Dai il premio piccolo della Profezia sbagliata, mai quello del valore esatto. Il potere TC-04 dà invece il premio che hai scelto. (CO-15) |
| «La Profezia vale sul nuovo tiro» / «la Profezia non scade: verifica anche il prossimo tiro altrui in questo turno» | Eccezioni scritte sulla carta alla scadenza di R 13.5; resta una sola Profezia attiva. (CO-14, CO-20) |
| «Il 7 su 2D6, e il 3 o il 4 su un D6, contano sia Alto sia Basso» | Allarga le soglie di R 13.5 solo per chi porta la carta. (CO-18) |

**Condizioni della riga «Se»** (`testo_situazionale`). Si controllano quando la carta si risolve; per un Equipaggiamento, quando succede l'evento. Sono ammesse:
- Indizi: «se hai N Indizi o più», «se quell'avversario ha N Indizi o più»;
- PV: «se hai N PV o meno»;
- carte: «se quell'avversario ha più carte di te» / «se un avversario ha più carte di te» (R 12.7), «se nei tuoi scarti ci sono N carte o più»;
- slot: «se hai N Equipaggiamenti o più negli slot», «se lo slot … è vuoto», «se sacrifichi …», «se hai 2 Indizi o più quando lo equipaggi»;
- scontro: «se sei in uno scontro / in un Duello / in uno scontro con un mostro [che non è il custode]», «se combatti un boss / una creatura di LV N o più», «se il bersaglio ha già subito Danni in questo scontro / in questo turno», «se dopo i Danni [il bersaglio] ha N PV o meno [e non è un boss]», «se sta affrontando il custode di MIMI», «se il tiro è contro un avversario»;
- Mappe: «se è in gioco la Mappa X»;
- tempo: «se è il tuo turno e non ti sei ancora mosso», «se lo giochi in risposta a un Incanto di quell'avversario», «se poi giochi un Incanto d'attacco in questo turno»;
- tiri: «se è il tiro per l'Indizio di un avversario»;
- «se l'avevi già» (la Forte Volontà).

Su un Equipaggiamento, una riga «Se» che dà una statistica vale finché è equipaggiato, quando la condizione è vera (TE-22). Bilanciamento dell'11/11 degli Equipaggiamenti di classe nuovi: «se combatti una creatura di LV 3 o più: (+N) AR» (CA-13, CA-15, CO-14, CO-15, CO-18, CO-20, CR-12, CS-11, CS-12, CS-17, CS-18) e «… (+1) Danni ai tuoi attacchi» (CR-17); «se combatti un boss: (+2) AR», custode compreso (CO-19, CR-16, CS-16); «se hai 2 PV o meno: (+2) AR» (CG-18).

### 14.6 Esempio di righe

Note accorciate.

```csv
id,tipo,nome,classe,direzione,pl,rarita,slot,testo,testo_situazionale,nota,battuta
CS-06,TI,"Ehm, tecnicamente no",Stregone,B,,Comune,,Annulla un Incanto nella catena. Se non c'è nessun Incanto da annullare: ottieni la Forte Volontà.,,"Desy: Assorbi la volontà («Annulla una carta Incanto»), con il ripiego del piano §6.4 (V6).",
TE-10,TE,Scudo del Goblin,Tutte le classi,,2,Rara,Arma DX / Scudo,"Finché è equipaggiato ottieni (+1) AR. Quando il D6 della perdita ti farebbe perdere questo Scudo (con 1 o 3), puoi ritirare quel D6.",,"v6: TE-09 (esempio di R 5.4: ritiro con penalità, minimo 1)."
```

## 15. Glossario

| Parola | Significato |
|---|---|
| Catena | Un giro di risposte, aperto da una carta o da un tiro (R 4.5–4.7). |
| Pila | Le carte di una catena, una sopra l'altra; si risolvono dall'ultima (LIFO). |
| Risposta | La carta giocata nel giro di una catena (al massimo 1 per giocatore). |
| Zona delle carte giocate | Le carte e i segnaposto Usato davanti a te, dalla tua ultima Fine (massimo 2). |
| Effetto automatico | Potere della Carta Classe, Equipaggiamento in gioco, Forte Volontà, mostro, Stato: fuori dalla pila, senza risposte. |
| Potere | L'effetto della Carta Classe: una volta per partita, tessera Usato (D12). |
| Tiro aperto | Un tiro la cui catena non si è ancora risolta. |
| Tuo tiro | Un tiro per il tuo eroe: movimento, iniziativa, per colpire, danno, Indizio, D6 della perdita, D6 della Trappola. |
| Tiro altrui | Un tiro di un avversario per il suo eroe, oppure un tiro fatto per una creatura, anche se i dadi li tiri tu. Mai un tiro per il tuo eroe. «Chi ha tirato» è quell'avversario o quella creatura. Una Profezia «su un tuo tiro» o «su un tiro altrui» dà il premio solo se il tiro che la verifica (R 13.5) è di quel tipo [PLAYTEST]. |
| Ritiro / penalità | Nuovo tiro degli stessi dadi; il ritiro n ha penalità n (D1). Anche girare un dado sulla faccia scelta (CS-19) conta come un ritiro. Nessuna carta toglie la penalità. |
| Dado in più | Tiri 1 D6 in più e tieni il migliore (R 13.4). Al massimo 1 dado in più per tiro: due fonti (per esempio CS-05 Rune per principianti e CS-01 Dardo di fuoco (o quasi)) non si sommano [PLAYTEST]. |
| PL | Power level: somma dei PL degli Equipaggiamenti negli slot (0–12). |
| Mazzetto | Mazzo Mostri del tuo PL: 1 (PL 0–3), 2 (PL 4–7), 3 (PL 8+). |
| LV | Livello del mostro, stampato sulla carta: danno e Indizio. |
| Creatura | Mostro o boss, mai un eroe. |
| Creatura ed effetti per eroi | Una creatura non ha mano, Stati, Indizi né slot: ignora «scarta», «prende lo Stato», «non prende l'Indizio» e «tira il D6 della perdita» e applica solo i Danni [PLAYTEST]. Salvo che la carta dica cosa fa la creatura (CO-10). |
| Avversario | Un altro eroe. |
| Custode | Il boss che sta con MIMI; sconfiggerlo fa vincere. |
| Indizio | Segnalino; con 3 si individua il tesoro e si può sfidare il custode. |
| Forte Volontà | Segnalino unico: scartalo per ritirare 1 D6. |
| Stato | Tessera di 1 turno (dritta o di traverso). Segno (+): aiuta chi lo ha; segno (−): lo ostacola. |
| Usato | Tessera che segna un uso o una carta giocata fuori dalla zona. |
| Profezia | Previsione sul prossimo tiro, verificata sulle facce dei dadi (R 13.5). |
| Profezia con vantaggio o svantaggio | Con due tiri di 2D6 si verifica il tiro tenuto, quello che conta [PLAYTEST]. |
| Profezia su un tiro aperto | La Profezia si verifica appena escono i dadi, quando il tiro è ancora aperto: un premio «(+N) a quel tiro» si somma a quel tiro (CO-01). |
| Profezia scelta prima | Solo se la carta lo dice (CO-01): la Profezia si sceglie prima dell'effetto base e verifica il tiro ritirato, non quello dopo. |
| Sacrificio | Costo: metti un tuo Equipaggiamento dallo slot nei tuoi scarti e giri le rotelle (R 13.2). Non è il D6 della perdita. |
| Lasciare lo slot | L'Equipaggiamento va negli scarti per qualsiasi motivo: sostituito, perso, sacrificato o distrutto (§14.5). |
| Distruggere | Mettere un Equipaggiamento negli scarti del suo proprietario (R 11.3). |
| Ripiego | La parte «Se non c'è …:» dell'effetto base di una risposta (V6). Non fa mai pescare. |
| Scry | Guardare le prime carte di un mazzo e riordinarle (R 13.3). |
| Mill | Far scartare carte agli altri (R 13.6). |
| Scartare | Dalla mano agli scarti. Non è giocare una carta. |
| Pescare | Dal mazzo comune alla mano, salvo che la carta dica la pila di classe. |
| Riprendere / recuperare | Dai tuoi scarti alla mano. |
| D6 della perdita | Il tiro di R 11.1. |
| Tutti (Mappe) | Tutti gli eroi. Per mostri e boss la carta dice «le creature». |
| Libero / ostacolo / accidentato | Esagono dove si cammina normalmente / esagono dove non si entra (bosco, rocce, case) / esagono da cui uscire costa 1 MOV in più (per ora l'acqua senza ponte né guado). Percorribile = libero o accidentato (R 8.3, D25). |
| Mostro scoperto | Tessera rossa a faccia in su: sbarra il passaggio (R 8.5). |
| Accanto | Esagoni con un lato in comune (R 8.7). |
| Riserva / tessere usate | Le tessere fuori dalla mappa: da usare per il rifornimento delle «?» (R 8.11). |

## 16. Simulatore v7 (D5): parametri, opzioni, misure

Il simulatore va in `v7/simulatore/` (piano §9). Prende le regole da questa spec, la plancia dal §17 e le carte dai CSV del §14.

**Parametri, con il valore di partenza [PLAYTEST]:**

| Parametro | Partenza |
|---|---|
| Limite di carte tra due proprie Fini / per catena | 2 / 1 (D9) |
| Equipaggiamenti per turno | 1 (v6, N3) |
| Mano massima | 10 (D8) |
| Mazzetto di classe | 10 su 20 (D22) |
| Mano iniziale | 3 di classe + 3 comuni |
| Pesca a inizio turno | 1, dal comune o dalla pila di classe |
| PL per rarità | 1 / 2 / 3 |
| Soglie dei mazzetti | PL 0–3 / 4–7 / 8+ |
| Ricompense | mazzetto 1 tiro per l'Indizio; mazzetto 2 Forte Volontà + tiro per l'Indizio; mazzetto 3 Indizio garantito |
| Locanda | 2 PV + 1 carta dagli scarti |
| Soglia di rifornimento delle «?» | 6 |
| Composizione del mazzo comune | circa 25 E / 30 I / 8 M, più le carte comuni nuove di Desy (D22) |
| AR dei mostri | AR v6 −25 % per eccesso: da 6 a 9 (D19) |
| Indizio | D6 ≤ LV + 1; con LV 5 garantito (D18) |

**Opzioni da accendere:**
- OP-1, OP-2, OP-5 (R 7.12); OP-3 e OP-4 sono regola di base (D19, D18): il simulatore le spegne solo per confrontare con la v6;
- dado in più sommato invece di «tieni il migliore» (N6);
- chi tira non risponde al proprio tiro (variante letterale del piano, N1);
- verso della penalità sempre −n (N2).

**Motore:** a eventi, con catena oraria, pila LIFO, bersagli che spariscono, nessuna catena nuova durante una catena, tiri che aprono una catena e i momenti M0–M6 (R 4.16). Una IA per classe e direzione (10 profili), che risponde anche nei turni degli altri.

**Misure (piano §9):**
- lunghezza media delle catene, carte giocate fuori turno, mani vuote, mani a 10;
- equilibrio tra le 5 classi e tra le 2 direzioni;
- PL medio nel tempo e uso dei mazzetti;
- durata della partita (v6: circa 10,6 round);
- rifornimenti delle «?», sconfitte, Indizi da mostri e da Duelli.

## 17. Mappa 12×12: base, fiori e preset (D24, D25)

Fonte di regole e numeri: `v7/idee/mappa_tessere/12x12/progetto.md`, con lo script `mappa12.py` che li calcola. Dati di riferimento del kit: `v7/stampa/sorgenti/dati/` (`fiori.csv`, `base12.csv`, `preset12.csv`). I preset 10 × 10 del D23 (tile e muri) sono superati: restano nella storia git e in `v7/simulatore/mappa.py` e `v7/simulatore/plance/`.

**Coordinate.** (x, y): x colonna 1–12, y riga 1–12, esagoni con la punta in alto, righe dispari spostate a sinistra di mezzo esagono rispetto alle pari (R 8.2). Vicini di (x, y): nella stessa riga (x−1, y) e (x+1, y); se y è dispari (x−1, y±1) e (x, y±1); se y è pari (x, y±1) e (x+1, y±1).

**Base (2 fogli A4).**
- Fascia delle coordinate su tutti e quattro i lati: i numeri di colonna sopra la riga 1 e sotto la riga 12, i numeri di riga a sinistra e a destra.
- 46 esagoni di bordo. **Partenze** (in senso orario, non simmetriche ma bilanciate): P1 (5,1) · P2 (11,2) · P3 (12,8) · P4 (9,12) · P5 (2,10) · P6 (1,4). **Ostacoli singoli:** bosco (7,2) e (6,11), rocce (2,9) e (11,4). Gli altri esagoni di bordo sono liberi.
- 14 spazi numerati per i fiori (S1–S14), con i numeri 1–6 sull'anello per la freccia dei preset.

**I 14 fiori.** Faccia A «verde e acqua», faccia B «pietra e case». Guado e ponte sono liberi; l'acqua è accidentata (R 8.3).

| Fiore | Faccia A | Faccia B |
|---|---|---|
| 1, 2 | tre boschi a stella | tre massi a stella |
| 3 | tre boschi a stella | borgo a stella (3 case) |
| 4 | boschi e massi a stella | tre cascine |
| 5, 6 | due boschetti | cava (3 rocce) / villaggio (3 case) |
| 7, 8 | strettoia (2 ostacoli opposti: bosco; bosco e rocce) | 2 massi / 2 case |
| 9, 11 | ruscello o fiume col guado (acqua – guado – acqua) | 2 massi / rupe (rocce al centro e 1 sull'anello) |
| 10, 12 | ruscello o fiume col ponte | 2 case / piazza (case al centro e 1 sull'anello) |
| 13 | lago (acqua al centro e 1 sull'anello) | miniera (3 rocce) |
| 14 | laghetto (acqua al centro) | mercato (3 case) |

**Regola di disegno dei fiori** (tiene la mappa collegata con qualunque posa). Ogni faccia è in una di due forme:
- (a) il centro è libero e sull'anello ci sono al massimo 3 ostacoli, mai due vicini;
- (b) il centro è un ostacolo e sull'anello ce n'è al massimo 1.

Così due fiori vicini restano sempre collegati da almeno un lato e nessun gruppo di fiori resta chiuso. Verifica di progetto.md, fatta con l'acqua ancora ostacolo, cioè nel caso più stretto: su 5.000 draft casuali la mappa è sempre collegata e la ricerca del caso peggiore non trova nessuna posa che la spezzi. Con D25 l'acqua diventa percorribile, quindi i collegamenti possono solo aumentare.

**Numeri dei draft simulati** (progetto.md, 5.000 draft): ostacoli e acqua 26 % in media (24–28 %); sul bordo l'8,5 % contro il 34,9 % del centro 6 × 6; 1,5 vicoli ciechi per mappa (accettati da Daniele il 12/11). Montaggio tipico: draft 4:38–5:14, preset 4:11 (tile del D23: 11:13).

**Preset.** Gli stessi 14 fiori in spazio, faccia e rotazione fissi: base «Strettoie» (strettoie davanti al centro, guadi da contendersi) e TM-01 Forziere, TM-02 Città, TM-03 Foresta, TM-04 Tundra, TM-05 Sottovelo, TM-06 Miniera, TM-07 Yuma, TM-08 Flegias, TM-09 MIMI. Il foglio di ogni preset scrive per ogni spazio «S7: 9A·5» (spazio 7: fiore 9, faccia A, freccia verso il 5) e, per il cambio di mappa (R 8.12), le sue 3 righe di cambio. Le posizioni stanno in `preset12.csv` (e in `v7/idee/mappa_tessere/12x12/preset12.py`). Ogni preset ha un fiume centrale fatto dai fiori d'acqua e passi attesi simili da tutte le Partenze.

**Controlli** (per i preset e per i draft): esagoni percorribili tutti collegati; 6 Partenze sulla base; «?» ad almeno 2 esagoni da ogni Partenza; passi attesi Partenza → Cripta simili tra le Partenze (scarto atteso 0,93 passi, con l'acqua che costa 2 passi). I vicoli ciechi sono ammessi.

## 18. Valori [PLAYTEST]

| Tema | Valore di partenza | Regola |
|---|---|---|
| Mazzetto di classe | 10 su 20 (D22; prima 6 su 10) | R 3.6 |
| Mano iniziale | 3 di classe + 3 comuni | R 3.7 |
| Pesca | 1 a inizio turno (comune o classe), anche nel primo turno | R 12.3 |
| PL per rarità | 1 / 2 / 3 | R 6.1 |
| Soglie dei mazzetti | PL 0–3 / 4–7 / 8+ | R 6.4 |
| Ricompense | mazzetto 1 Indizio; mazzetto 2 Forte Volontà + Indizio; mazzetto 3 Indizio garantito | R 10.3 |
| Indizio | D6 ≤ LV + 1, garantito con LV 5 (D18, deciso il 10/11) | R 10.2 |
| AR dei mostri | AR v6 −25 % arrotondata per eccesso: da 6 a 9 (D19, deciso il 10/11) | R 6.8 |
| Locanda | 2 PV + 1 carta dagli scarti | R 8.10 |
| Duello | Indizio + 1 carta dagli scarti dello sconfitto + Forte Volontà | R 10.10 |
| Tessere | opzione A: 24 «?», 12 tessere in riserva, rifornimento con 6 coperte o meno | R 3.3, R 8.11 |
| Movimento | su ogni esagono percorribile; uscire dall'acqua (accidentata) costa 1 MOV in più; fermata sul mostro scoperto | D25, R 8.3–8.5 |
| Accanto | lato in comune | R 8.7 |
| Mappa 12×12 a fiori | base + 14 fiori a due facce; draft (7/4/3 fiori a testa con 2/3/4 giocatori) o uno dei 10 preset; 24 «?» posate a turno ad almeno 2 esagoni dalle Partenze; ostacoli e acqua circa 26 % | D24, R 3.1, R 8.1, §17 |
| Cripta e cambio di mappa | Cripta col 2D6 + 2D6 al 3° Indizio e a ogni «Il tesoro cambia Cripta»; una Mappa cambia 3 fiori; a ogni cambio tutti tornano sulla Partenza iniziale; Cuore tolto | R 8.8, R 8.12, R 10.11 |
| Partenza occupata alla morte | esagono libero accanto, a scelta | R 11.4 |
| Costi scelti, oggetti precisi | seguono il testo della carta | R 11.3 |
| Penalità | verso peggiorativo (+n dove serve un numero basso); minimo 1; i modificatori restano | R 5.3–5.5 |
| Chi tira | risponde per primo al proprio tiro | R 4.7 |
| Precedenza delle catene | chi ha il turno, poi in senso orario | R 4.5 |
| Segnaposto | tessera Usato per Equipaggiamenti e Mappe; 20 tessere Usato | R 4.4 |
| Ricompense e carte altrui | all'eroe che combatte | R 4.13 |
| Equipaggiamenti | 1 per turno; niente Equipaggiamento gratis in preparazione (D26) | R 4.2, R 3.8 |
| Scontro con un mostro | al massimo 3 attacchi dell'eroe, poi il mostro scappa (mai il custode); nel primo giro niente attacchi tra eroi | D26, R 7.5, R 10.8 |
| Oracolo | TC-04 nuova; Profezie sulle facce; Alto 4+/8+, Basso 3−/6−; valore esatto su 2D6 = un dado; una Profezia alla volta; con vantaggio o svantaggio conta il tiro tenuto; tiro altrui = di un avversario o per una creatura | R 13.5, §15 |
| Ricercatore | in segreto, mazzetto a scelta, in qualsiasi momento senza catena aperta | R 13.3 |
| Stregone | dado in più: tieni il migliore; al massimo 1 dado in più per tiro, le fonti non si sommano | R 13.4, §15 |
| Mano pubblica | il numero di carte in mano è pubblico | R 12.7 |
| Stati nuovi e tessere | Vantaggio, Svantaggio, Fermo; 31 tessere Stato in tutto, una per fonte (carte e mostri) e al massimo 4: Rallentato, Silenzio, Fede, Vantaggio e Fermo 4; Occhio, Riflesso e Svantaggio 3; Sussurro 2 | R 9.7, R 2.5, `stati.csv` |
| Riga in fondo alla Carta Classe | «Mazzetto: 10 delle 20 carte di classe · Mano: 3 + 3» | R 13.1 |
| Riscalatura e tetti | tabella §14.4; tetto 2 / 2 / 3; vantaggio di carte +1 / +1 / +2 | §14.4, V9 |
| Sacrificio | il bonus pagato con un sacrificio arriva a +3 anche su Comune e Rara | R 13.2, §14.4 |
| Composizione delle classi | per direzione (10 carte): da 4 a 8 Equipaggiamenti, almeno 2 Incanti, massimo 2 Leggendarie; niente Mappe (D22) | V14, V15 |
| Mazzo comune | 81 carte: 31 Equipaggiamenti, 41 Incanti, 9 Mappe (63 prima di D22) | R 2.5 |
| Dalla v6 restano provvisorie | Trappola a 0 PV con un solo tiro di perdita; «la voce si sparge» (+1 Indizio agli altri); niente ricompense a chi sconfigge un eroe con una carta; «creatura»; bonus dello Yumaniano | R 11.5, R 10.6, R 10.4, §14.3 |
| Ripieghi delle risposte | mai la pesca: Forte Volontà, uno Stato, (+N) a un prossimo tiro o uno scry | V6 |
| Riduzione dei Danni | dopo il tiro del danno, minimo 0 | §14.5 |
| Creature ed effetti per eroi | applicano solo i Danni | §15 |
| «Quando lascia il tuo slot» | scatta anche quando lo sostituisci tu | §14.5 |
| Effetti ripetibili | niente vantaggio di carte netto per uso | V9 |
| Equipaggiamenti di classe nuovi (XX-11…20) | niente bonus fisso di serie; per difendersi una riga «Se» con (+1)/(+2) AR (creature di LV 3 o più, boss, 2 PV o meno) o una parata dell'Assaltatore; CG-16 e CG-17 Comuni (PL 1) (11/11) | §14.5 |

## 19. Punti aperti

Da definire con Desy al telefono o su Discord (commento 10). Intanto il playtest usa questi default.

**Dal piano §11:**

| # | Punto | Default per il playtest |
|---|---|---|
| 1 | Le Profezie si verificano sulle facce dei dadi o sul risultato con la penalità? | Sulle facce (R 5.6, R 13.5) |
| 2 | Mappe in risposta | Deciso (D10) |
| 3 | Costruzione 10 su 20 (D22; era 6 su 10), mano 3 + 3, pesca 1 a turno | Sì (R 3.6, R 3.7, R 12.3) |
| 4 | Soglie PL 0–3, 4–7, 8+ e PL 1/2/3 per rarità | Sì (R 6.1, R 6.4) |
| 5 | Potere dell'Oracolo: le Profezie al posto di «resti a 1 PV» | Sì, TC-04 nuova (R 13.1) |
| 6 | Plance eroe neutre | Deciso (D14) |
| 7 | Movimento solo su strada e fermata sul mostro scoperto | Superato da D25: si cammina su ogni esagono percorribile e l'acqua costa 1 MOV in più; resta la fermata sul mostro scoperto (R 8.4, R 8.5) |
| 8 | Sacchetto: A, B o C; soglia di rifornimento | A, soglia 6 (R 8.11) |
| 9 | «A una casella di distanza» e Duello attraverso muri e acqua | Accanto = lato in comune; i muri non esistono più (D24) e gli ostacoli non contano (R 8.7) |
| 10 | Togliere il Cuore; Mappe che cambiano il terreno | Cuore tolto; ogni Mappa cambia 3 fiori e riporta tutti alla Partenza iniziale (R 8.12) |
| 11 | Simulazione prima della plancia definitiva | Sì, sulla bozza 10 × 10; la mappa definitiva è la 12 × 12 a fiori (D16, D24, R 8.1) |
| 12 | Morte: D6 della perdita, propria Partenza, 1 carta comune | Deciso (D7) |
| 13 | Partenza occupata alla morte | Esagono percorribile libero accanto, a scelta (R 11.4) |
| 14 | Costi scelti ed effetti su un oggetto preciso fuori dal D6 | Sì, segue il testo della carta (R 11.3) |
| 15 | Scudo del Goblin con la penalità: risultato almeno 1 | Sì (R 5.4) |

**Dal piano §5 (combattimento):** OP-3 e OP-4 sono adottate il 10/11 (D19, D18). OP-1, OP-2 e OP-5 non sono adottate: base v6, il simulatore le confronta (R 7.12).

**Nati scrivendo la spec:**

| # | Punto | Default |
|---|---|---|
| N1 | Il piano dice che ai tiri rispondono «gli altri». Così nessuno potrebbe usare dalla mano le carte che ritirano il proprio tiro (Fortuna del Furfante, Sguardo dell'Oracolo, Destino obbligato). | Chi tira risponde per primo (R 4.7) |
| N2 | Nei tiri dove serve un numero basso (Indizio, PV persi per la Trappola) un −1 aiuterebbe chi ritira. | La penalità peggiora sempre: lì si somma (R 5.3) |
| N3 | Il limite v6 di 1 Equipaggiamento per turno resta? | Sì (R 4.2) |
| N4 | Come si contano le carte che lasciano la zona (Equipaggiamenti, Mappe)? | Segnaposto Usato; 20 tessere Usato (R 4.4, R 2.5) |
| N5 | Profezia sul valore esatto in un tiro di 2D6 | Basta un dado (31 %) (R 13.5) |
| N6 | «Dado in più» dello Stregone: si somma o si tiene il migliore? | Si tiene il migliore (R 13.4) |
| N7 | Potere del Ricercatore: quando si usa, quale mazzo Mostri, in segreto? | In qualsiasi momento senza catena aperta; mazzetto a scelta; in segreto (R 13.3) |
| N8 | Equipaggiamento iniziale gratis (v6) | Tolto il 12/11 (D26, R 3.8) |
| N9 | Pesca nel primo turno | Sì, per tutti (R 12.3) |
| N10 | Premi del Duello sotto D11 (Indizio + 1 carta dagli scarti + Forte Volontà) | Come la v6 senza PE (R 10.10) |
| N11 | Chi prende le ricompense se il colpo finale lo dà la carta di un altro | L'eroe che combatte (R 4.13) |
| N12 | Il numero di carte in mano è pubblico? | Sì (R 12.7) |
| N13 | Precedenza se più giocatori vogliono aprire una catena insieme | Chi ha il turno, poi in senso orario (R 4.5) |
| N14 | Con il tetto di +2 su Comune e Rara il sacrificio dell'Assaltatore non darebbe un effetto «molto più forte»: l'esempio del piano §6.2 usa (+3). | Il bonus pagato con un sacrificio arriva a +3 anche su Comune e Rara (R 13.2, §14.4) |
| N15 | Sottovelo (Mappa di Desy) è il Cimitero dei Maghi della v6? | Sì: TM-05 Sottovelo tiene il vantaggio dei Sanguar del Cimitero dei Maghi, e la Carta Specie Sanguar rimanda a Sottovelo |
| N16 | CG-10 Nooh! MiMi! (Giullare, Leggendaria): con la riga «Se» infligge D6 + 2 Danni a un avversario che può non essere accanto (le altre carte dicono «un avversario accanto») e sposta il tesoro senza una Mappa. | Com'è stampata: il bersaglio può essere lontano; lo spostamento segue R 10.11 (senza limite di spostamenti dal 12/11, D26) |
| N17 | 6 carte della v6 non stanno in nessun mazzo v7: Lancio di Coltello, Fendente Radioso, Grido di Battaglia, Colpo Poderoso, Mazza Benedetta, Simbolo Sacro. Rientrano, nel mazzo comune o in una classe? | Fuori dalla v7; il ruolo di Grido di Battaglia e Colpo Poderoso sta in CA-01 Via la corazza, fa caldo! |
| N18 | Mostri raddoppiati (D20): bilanciamento dei 24 mostri nuovi e delle 7 abilità v6 cambiate perché doppioni | Statistiche nella fascia v6 del loro LV (R 6.8); da misurare col simulatore |
| N19 | Monologo (NE-52) contro la regola del pareggio dei boss e OP-1 | Vince la carta: l'eroe attacca per primo senza tiro, anche col custode (R 7.2). Con OP-1 resta solo il (+1) Danni |
| N20 | Televoto (NE-51) da custode: con 5–6 i 2 Danni possono finire il custode prima di ogni attacco | Sì: se arriva a 0 PV vinci la partita (R 7.9, R 10.12) |
| N21 | Divieti di scontro di NE-47 (ritiri) e NE-49 (Incanti): valgono anche per i giocatori che non combattono e per carte che non riguardano lo scontro? | Sì, per tutti e per tutto lo scontro (§14.5) |
| N22 | Tessere Stato finite (31 tessere, una per fonte, al massimo 4): può servirne una in più in casi rari a 4 giocatori | Lo Stato non si prende; se succede al tavolo, annotarlo per il conteggio delle copie |
| N23 | Mazzetto di 10 carte su 20 (D22): con la pila di classe di 7 carte invece di 3, la pesca dalla pila (R 12.3) e la scelta delle carte pesano di più; con 20 carte per classe l'equilibrio tra le classi e tra le direzioni può cambiare. | Default 10 su 20 (R 3.6). Da misurare col simulatore, che oggi costruisce il mazzetto con le 5 carte della propria direzione più 1 (`ia.mazzetto_classe`) e va aggiornato |
| N24 | Totale del mazzo comune dopo D22 (63 prima): le carte di Desy «tutti» e quelle che le classi non assorbono (overflow) vanno nel mazzo comune. | Fissato il 10/11: 81 carte (31 TE, 41 TI, 9 TM), R 2.5 e §18 |
| N25 | Comporre la mappa a tile in partita (D23): resta solo uno strumento da playtest o diventa regola ufficiale? Chi la compone, con quali vincoli, e quanto cambia l'equilibrio? | Chiuso il 12/11 da D24: la mappa si monta col draft dei fiori o con un preset (R 3.1); le tile non si usano più |
| N26 | Cambio di mappa a metà partita (R 8.12): è praticabile al tavolo? | D24: una Mappa cambia solo 3 fiori, le «?» di quegli spazi si rimettono e la Cripta si ritira (R 8.12). Si prova nei playtest se è abbastanza rapido |
| N27 | Carte Aiuto da aggiornare: AI-01…04 dicono «Muovi fino a quel numero (almeno 1), solo su strada» (contro D25) e il Riepilogo dice «D6 per la Cripta» (contro D24). | Vale la Spec (R 8.4, R 8.8). Daniele (22:55): le Carte Aiuto si aggiornano il 12/11 sera |
| N28 | Una carta Mappa ritira la Cripta, ma R 10.11 limitava il tesoro a 2 spostamenti per partita. | Chiuso il 12/11 (Daniele, 22:55): il limite è tolto, ogni «Il tesoro cambia Cripta» ritira la Cripta (R 10.11, D26) |
| N29 | Terreno accidentato (D25): con 1 solo passo si entra nell'acqua? Gli effetti che spostano una pedina pagano il MOV in più? | Chiuso il 12/11 (Daniele, 22:55): entrare costa 1, uscire 1 in più; con 1 passo entri, per uscire servono 2 (R 8.4). Lo spostamento di una carta non conta i passi (R 8.6) |
| N30 | Primo giro (D26): quali carte contro un avversario sono «attacchi»? | Chiuso il 12/11 (Daniele, 22:55): nel primo giro nessuna carta contro un avversario, oltre al divieto di Duello (R 10.8) |
| N31 | Mostro che scappa (D26): le abilità «a fine scontro» (NE-02, NE-34) scattano? L'attacco in più di NE-15 conta? | Chiuso il 12/11 (Daniele, 22:55): «a fine scontro» non scatta quando il mostro scappa (§14.5). Il limite conta solo gli attacchi dell'eroe, quindi NE-15 non lo cambia. Con la fuga dell'eroe e con NE-29 la tessera resta scoperta; quando il mostro scappa va tra le usate |
| N32 | Carte Aiuto: non conoscono ancora D26 (Equipaggiamento iniziale, primo giro, 3 attacchi). Il simulatore sì (12/11 sera): 1000 partite → 13,2/12,5/12,3 turni (2/3/4 giocatori, prima 11,8/11,3/11,1), il mostro scappa nel 5,3–5,5 % degli scontri, rifornimenti «?» quasi spariti, Giullare 52→57 % a 2 giocatori. | Carte Aiuto da aggiornare in un lavoro a parte; partite più lunghe di ~1,2 turni: da provare al tavolo |

**Decisi nella revisione delle carte del 10/11, da misurare col simulatore:**
- CA-09 Elmo a prova di testata non torna più in mano quando lo sacrifichi (con CA-08 dava carte oltre V9 e un sacrificio gratis ogni turno): ora (+1) AR e non si perde.
- Bilanciamento col simulatore (10/11, 4 giocatori: Assaltatore B 41 % → 28–29,5 %, Stregone 17,5–18 % → 24–25 %): CA-09 e CA-10 da (+2) a (+1) AR; CA-06 para gratis solo (-1) ai Danni, annulla tutto e rimanda 2 Danni solo col sacrificio; CA-05 Cesto (+1) ATT e «Sacrifica questo Cesto: (+3) ATT in questo turno»; CS-05 Rune per principianti dà anche (+1) AR.
- CR-07 Tagliacarte impiccione ruba 1 carta una volta sola, quando lo equipaggi (prima: ogni turno in cui colpivi un avversario).
- CA-03 Te lo tiro in testa!: i 3 Danni senza tiro chiedono il sacrificio di un Equipaggiamento con PL 2 o più.
- Ripieghi senza pesca (V6): TM-01, TI-10, TI-22, CS-06, CS-07, CS-08, CO-01; CS-01 non ha più ripiego.
- La parata degli attacchi è dell'Assaltatore (CA-06 senza costo, CA-10) e della Targa «Vietato Colpire» (TE-08); TI-06 Barriera Antisfiga para Trappole e Incanti.
- Da misurare: il sacrificio abbassa il PL e porta a mazzetti più facili; la pesca che resta (TM-06, CG-01, CG-07, il premio grande di CO-02); TI-03 Uccisi molto male e gli altri danni diretti contro il mazzetto 1.
- Carte nuove di D22 (revisione del 10/11 sera): TM-09 ora rende più facile il tiro per l'Indizio (il ritorno alla Partenza lo fa già R 8.12); CS-19 Il Dado è Truccato conta come un ritiro (penalità, e NE-47 la ferma); TI-34 NO! come ripiego dà Silenzio a un solo avversario; CO-15 dà solo il premio piccolo; CR-11 non potenzia il potere TC-02; TE-27 non toglie più la penalità del ritiro; CG-14 e CG-17 non sono più doppioni (di TC-05/TI-35 e di CS-16); CO-12 non riduce più i Danni (resta all'Assaltatore, CA-07) ma dà AR; CA-19 non costa più (-2) AR (era peggiore di TI-12). Da misurare: i danni diretti ripetibili (TE-26, CS-12), la pesca di TI-37 e CG-13, CO-15 contro il potere TC-04.
- Bilanciamento dell'11/11 degli Equipaggiamenti di classe nuovi (decisione di Daniele: sistemare gli effetti, non le regole del PL). Con le carte di D22 la partita durava 14,6/13,9/14,1 round (2/3/4 giocatori, 500 partite, seme 1), perché questi oggetti alzavano il PL senza dare difese: mazzetto 3 nel 23 % degli scontri e scontri persi nel 32 %. Ora 11,1/10,5/10,2 round, scontri persi 23,5/22,3/22,8 %, mazzetto 3 nel 20 %; vittorie per classe tra 0,89 e 1,11 della quota equa (2000 partite; prima tra 0,75 e 1,15). Cambi: riga «Se» con AR (§14.5) su 15 oggetti e (+1) Danni su CR-17; CA-15 (-1) AR invece di (-2); CO-15 costa 1 PV invece di 2; CA-17 para (-1) una volta per turno; CA-18 non costa più AR; CG-16 e CG-17 da Rare a Comuni. Da misurare al tavolo: se le righe «Se» contro LV 3 o più rendono troppo sicuro il mazzetto 2–3.
