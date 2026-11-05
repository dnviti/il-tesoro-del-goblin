# Carte Trama v2 (file di Daniele del 27/10/2026) adattate alle regole della scatola.
# testo_originale = testo di Daniele; testo = proposta per la scatola; modifica = perché è cambiato.
import json

MAPPE = [
    # id, rarità, nome, testo originale, testo scatola, modifica
    ('TM-01', 'Comune', 'Miraggio del Tesoro',
     "Il tesoro cambia posizione: i giocatori che lo avevano individuato ne perdono la posizione, ma conservano i propri indizi.",
     "Il tesoro cambia Cripta. Gli Indizi restano a tutti.",
     "Sulla plancia MIMI si sposta in un'altra Cripta e tutti lo vedono: chi ha 3 Indizi lo ritrova subito. Nessun terreno."),
    ('TM-02', 'Comune', 'Città Avanzata',
     "Il tesoro cambia posizione, il tabellone diventa una “Città Avanzata”: tutti (+2) MOV",
     "Il tesoro cambia Cripta. Il tabellone diventa la «Città Avanzata»: tutti (+2) MOV.",
     "Indizi conservati (non azzerati)."),
    ('TM-03', 'Comune', 'Foresta Antica',
     "Il tesoro cambia posizione, il tabellone diventa una “Foresta Antica”: Elfi hanno vantaggio , tutti (-1) MOV",
     "Il tesoro cambia Cripta. Il tabellone diventa la «Foresta Antica»: tutti (-1) MOV; gli Elfi hanno vantaggio negli scontri.",
     "Indizi conservati; «vantaggio» precisato: negli scontri."),
    ('TM-04', 'Comune', 'Tundra invernale',
     "Il tesoro cambia posizione, il tabellone diventa una “Tundra invernale ”: tutti (-1) MOV",
     "Il tesoro cambia Cripta. Il tabellone diventa la «Tundra invernale»: tutti (-1) MOV.",
     "Indizi conservati."),
    ('TM-05', 'Rara', 'Cimitero dei Maghi',
     "Il tesoro cambia posizione, il tabellone diventa il  “Cimitero dei maghi”: Sanguar hanno vantaggio  tutti -1 MOV",
     "Il tesoro cambia Cripta. Il tabellone diventa il «Cimitero dei Maghi»: tutti (-1) MOV; i Sanguar hanno vantaggio negli scontri.",
     "Indizi conservati; «vantaggio» precisato: negli scontri."),
    ('TM-06', 'Leggendaria', 'Miniera di Uhul',
     "Il tesoro cambia posizione, il tabellone diventa la “Miniera di Uhul”:  tutti i giocatori recuperano 1 dalla rispettiva pila degli scarti se la giocano nel turno che si attiva questo effetto ne possono prendere un’altra ( eccetto la carta appena giocata ) ",
     "Il tesoro cambia Cripta. Il tabellone diventa la «Miniera di Uhul»: ogni eroe recupera (1) carta dalla sua pila degli scarti; chi gioca questa carta ne recupera (1) in più (non questa).",
     "Indizi conservati; testo accorciato."),
    ('TM-07', 'Rara', 'Yuma',
     "Il tesoro cambia posizione, il tabellone diventa  “Yuma”: per il resto della partita +1 agli incantesimi Oracolo recupera 1 carta dalla pila degli scarti ",
     "Il tesoro cambia Cripta. Il tabellone diventa «Yuma», il Paradiso: gli Incantesimi che infliggono Danni o fanno recuperare PV ne danno (+1). L'Oracolo recupera (1) carta dalla sua pila degli scarti.",
     "Indizi conservati; «+1 agli incantesimi» precisato; vale finché Yuma resta (una sola Mappa attiva)."),
    ('TM-08', 'Rara', 'Flegias',
     "Il tesoro cambia posizione, il tabellone diventa  “Flegias”: per il resto della partita  le trappole fanno il doppio del loro effetto ",
     "Il tesoro cambia Cripta. Il tabellone diventa «Flegias», gli Inferi: le Trappole fanno perdere il doppio dei PV.",
     "Indizi conservati; «doppio effetto» = doppi PV persi (la perdita di equipaggiamento resta una)."),
]

EQUIP = [
    # id, rarità, nome, testo originale, slot, classe, origine, testo scatola, modifica
    ('TE-01', 'Comune', 'Elmo sorgisogno', "Finché è equipaggiato ottieni (+1) AR e Individui le caselle trappola.", 'Elmo', 'Guerriero - Oracolo', 'Tua carta',
     "Finché è equipaggiato ottieni (+1) AR. Quando peschi una Trappola dal sacchetto la vedi in tempo: non ha effetto su di te.",
     "Con il sacchetto le Trappole non stanno sulla mappa: «individuare» diventa evitarle quando le peschi."),
    ('TE-02', 'Comune', 'Elmo del Cacciatore', "Finché è equipaggiato ottieni (+1) ATT contro le creature.", 'Elmo', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-03', 'Rara', 'Cappello del Taumaturgo', "Finché è equipaggiato, la prima volta che sconfiggi una creatura in un turno recuperi (1) carta dalla pila degli scarti.", 'Elmo', 'Mago', 'Nuova proposta', None, None),
    ('TE-04', 'Comune', 'Diadema della Veggenza', "Finché è equipaggiato ottieni (+1) AR e una volta per turno puoi ritirare un D6 di un incantesimo di Danno o di cura.", 'Elmo', 'Mago - Oracolo', 'Nuova proposta', None, None),
    ('TE-05', 'Comune', 'Scudo di Quercia Antica', "Finché è equipaggiato ottieni (+2) AR e (-1) MOV.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-06', 'Comune', 'Piccolo Scudo Borchiato', "Finché è equipaggiato ottieni (+1) AR.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-07', 'Rara', 'Scudo Specchiante', "Finché è equipaggiato ottieni (+1) AR; quando un attacco contro di te fallisce, l'attaccante subisce (1) Danno.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-08', 'Comune', 'Targa del Custode', "Finché è equipaggiato ottieni (+1) AR e una volta per partita annulli i Danni di un attacco subito.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta',
     "Finché è equipaggiato ottieni (+1) AR. Una volta per partita annulli i Danni di un attacco subito: metti un cubetto Durata sulla carta.", "Cubetto Durata per ricordare l'uso."),
    ('TE-09', 'Rara', 'Scudo del Goblin', "Finché è equipaggiato ottieni (+1) AR; se la tabella di perdita ti fa perdere l'arma destra, tira di nuovo il D6.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta',
     "Finché è equipaggiato ottieni (+1) AR. Se il D6 della perdita di equipaggiamento ti fa perdere l'Arma DX, ritiralo.", None),
    ('TE-10', 'Comune', 'Spada del Custode', "Finché è equipaggiata ottieni (+1) ATT.", 'Arma DX / Scudo', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-11', 'Comune', 'Bastone del Corvo', "Finché è equipaggiato ottieni (+1) ATT e una volta per turno puoi ritirare un D6.", 'Arma DX / Scudo', 'Mago', 'Proposta già impaginata', None, None),
    ('TE-12', 'Comune', 'Mazza Benedetta', "Finché è equipaggiata ottieni (+1) ATT, e (+1) Danno contro i non morti.", 'Arma DX / Scudo', 'Oracolo', 'Nuova proposta', None,
     "Non morti: Scheletro, Zombi e gli eroi Sanguar."),
    ('TE-13', 'Rara', 'Libro di Rune', "Finché è equipaggiato, una volta per turno un tuo incantesimo infligge (+1) Danno.", 'Arma SX', 'Mago', 'Nuova proposta', None, None),
    ('TE-14', 'Comune', 'Simbolo Sacro', "Finché è equipaggiato, quando recuperi PF con un incantesimo ne recuperi (1) in più.", 'Arma SX', 'Oracolo', 'Nuova proposta',
     "Finché è equipaggiato, quando recuperi PV con un incantesimo ne recuperi (1) in più.", "PF → PV."),
    ('TE-15', 'Comune', 'Pugnale Sottile', "Finché è equipaggiato, se attacchi per primo ottieni (+1) ATT.", 'Arma SX', 'Ladro', 'Nuova proposta', None,
     "Contro le creature attacchi sempre per primo (tranne con l'Agguato); nel Duello chi lo provoca."),
    ('TE-16', 'Leggendaria', 'Mantello delle Braci', "Finché è equipaggiato ottieni (+1) AR e subisci (1) PF in meno dalle trappole.", 'Armatura', 'Tutte le classi', 'Proposta già impaginata',
     "Finché è equipaggiato ottieni (+1) AR e perdi (1) PV in meno dalle Trappole.", "PF → PV."),
    ('TE-17', 'Rara', 'Cotta di Maglia', "Finché è equipaggiata ottieni (+2) AR e (-1) MOV.", 'Armatura', 'Tutte le classi', 'Nuova proposta', None, None),
    ('TE-18', 'Comune', 'Veste del Pellegrino', "Finché è equipaggiata ottieni (+1) MOV; quando termini il movimento in una Locanda recuperi (1) PF in più.", 'Armatura', 'Tutte le classi', 'Nuova proposta',
     "Finché è equipaggiata ottieni (+1) MOV; quando termini il movimento in una Locanda recuperi (1) PV in più.", "PF → PV."),
    ('TE-19', 'Rara', 'Corazza Runica', "Finché è equipaggiata ottieni (+1) AR, e (+2) AR contro un mini-boss.", 'Armatura', 'Tutte le classi', 'Nuova proposta',
     "Finché è equipaggiata ottieni (+1) AR, e (+2) AR in più contro i nemici di LV 3 o più.", "I mini-boss sono una regola facoltativa: il bonus vale contro il mazzetto II, i mini-boss e i boss."),
    ('TE-20', 'Leggendaria', 'Tunica del Viandante', "Finché è equipaggiata ottieni (+1) AR; quando termini il movimento in una Fonte recuperi anche (1) PF.", 'Armatura', 'Tutte le classi', 'Nuova proposta',
     "Finché è equipaggiata ottieni (+1) AR; quando termini il movimento in una Fonte recuperi anche (1) PV.", "PF → PV."),
]

INC = [
    # n, nome, testo originale, classe, origine, testo scatola, modifica
    (1, 'Flusso di volontà', "Infliggi (+1) Danno aggiuntivo con il prossimo incantesimo.", 'Tutte le classi', 'Tua carta', None, None),
    (2, 'Dardo Arcano', "Durante uno scontro infliggi 1D6 Danni alla creatura.", 'Tutte le classi', 'Proposta già impaginata', None, None),
    (3, 'Scudo di Cenere', "Fino alla fine del tuo prossimo scontro ottieni (+2) AR.", 'Tutte le classi', 'Proposta già impaginata', None, None),
    (4, 'Sguardo Spezzaossa', "Sconfiggi una creatura con (1) PV senza tirare per colpire.", 'Tutte le classi', 'Proposta già impaginata', None, None),
    (5, 'Passo del Folletto', "Aggiungi (+3) al tiro di Movimento di questo turno.", 'Tutte le classi', 'Proposta già impaginata', None, None),
    (6, 'Occhio dello Stregone', "Individui le caselle trappola entro (2) caselle da te.", 'Tutte le classi', 'Proposta già impaginata',
     "La prossima Trappola che peschi dal sacchetto non ha effetto su di te: tieni questa carta davanti a te finché succede.",
     "Con il sacchetto le Trappole non stanno sulla mappa: «individuarle» diventa evitarne una."),
    (7, 'Richiamo dal Sepolcro', "Recupera (1) carta dalla tua pila degli scarti.", 'Tutte le classi', 'Proposta già impaginata', None, None),
    (8, "Scintilla d'Ispirazione", "Se il tuo slot è vuoto, ottieni (1) Ispirazione.", 'Tutte le classi', 'Proposta già impaginata',
     "Se non hai l'Ispirazione, la ottieni.", "Lo «slot» è la casella Ispirazione della scheda."),
    (9, 'Palla di Fuoco', "Infliggi 1D6 Danni, più (+1) se il bersaglio ha già subito Danni.", 'Tutte le classi', 'Nuova proposta',
     "Durante uno scontro infliggi 1D6 Danni al nemico, più (+1) se ha già subito Danni.", "Precisato: in scontro."),
    (10, 'Raggio Gelido', "Infliggi 1D4 Danni; il bersaglio ha (-1) ATT fino alla fine dello scontro.", 'Tutte le classi', 'Nuova proposta',
     "Durante uno scontro infliggi 1D6 − 1 Danni (minimo 1) al nemico; ha (-1) ATT fino alla fine dello scontro.", "Niente D4: D6 − 1."),
    (11, 'Catena di Fulmini', "Infliggi 1D4 Danni; se ottieni 4, tira di nuovo 1D4 e infliggi altri Danni.", 'Tutte le classi', 'Nuova proposta',
     "Durante uno scontro infliggi 1D6 − 1 Danni (minimo 1) al nemico; se sul dado esce 6, tira di nuovo e infliggi altri Danni.", "Niente D4: D6 − 1, si ritira col 6."),
    (12, 'Parola di Confusione', "La creatura ritira il suo prossimo tiro per colpire e vale il risultato peggiore.", 'Tutte le classi', 'Nuova proposta',
     "Il prossimo tiro per colpire della creatura si fa con svantaggio (tira due D20 e vale il peggiore).", "Detto con lo svantaggio, che c'è già nel regolamento."),
    (13, "Velo d'Ombra", "Dichiari la fuga restando nella tua casella: lo scontro si annulla, senza ricompense.", 'Tutte le classi', 'Nuova proposta', None, None),
    (14, 'Teletrasporto Breve', "Prima di muoverti sposta la tua pedina di (1) casella in qualsiasi direzione.", 'Tutte le classi', 'Nuova proposta', None, None),
    (15, 'Mappa Sussurrata', "Se possiedi almeno (2) indizi, scopri se il tesoro è entro (4) caselle da te.", 'Tutte le classi', 'Nuova proposta',
     "Il prossimo scontro che vinci su una casella esplorazione ti dà (1) Indizio in più.",
     "Gli Indizi si prendono solo vincendo uno scontro su una casella esplorazione (Daniele, 27/10): la mappa aiuta a leggere quello che trovi."),
    (16, 'Fiamma Persistente', "Infliggi 1D4 Danni; la creatura subisce altri (1) Danni a ogni turno dello scontro.", 'Tutte le classi', 'Nuova proposta',
     "Durante uno scontro infliggi 1D6 − 1 Danni (minimo 1) alla creatura; subisce altri (1) Danni all'inizio di ogni round seguente.", "Niente D4; «turno» → round."),
    (17, 'Barriera Runica', "Annulla i Danni di una Trappola.", 'Tutte le classi', 'Nuova proposta', None, None),
    (18, 'Riflesso Speculare', "Fino al tuo prossimo turno, quando un avversario ti infligge Danni, subisce (1) Danno.", 'Tutte le classi', 'Nuova proposta', None, None),
    (19, 'Tocco Gelido', "Infliggi 1D6 Danni a un avversario a una casella di distanza.", 'Tutte le classi', 'Nuova proposta', None, None),
    (20, 'Furto di Memoria', "Ruba (1) carta dalla pila degli scarti di un avversario a una casella di distanza.", 'Tutte le classi', 'Nuova proposta', None, None),
    (21, 'Specchio dei Tesori', "Se sconfiggi una creatura in questo turno, ottieni (1) Ispirazione.", 'Tutte le classi', 'Nuova proposta', None, None),
    (22, 'Fulmine Rapido', "Giocala prima del tiro per colpire: aggiungi (+3) al tiro.", 'Tutte le classi', 'Nuova proposta', None, None),
    (23, 'Sigillo del Silenzio', "Un avversario a una casella di distanza non può giocare carte Incantesimo fino al tuo prossimo turno.", 'Tutte le classi', 'Nuova proposta', None, None),
    (24, 'Metamorfosi in Ratto', "La ATT della creatura diventa (1) fino alla fine dello scontro.", 'Tutte le classi', 'Nuova proposta',
     "L'ATT della creatura diventa (1) fino alla fine dello scontro.", None),
    (25, 'Benedizione', "Recupera 1D4 PF.", 'Oracolo', 'Nuova proposta', "Recuperi 1D6 − 1 PV (minimo 1).", "Niente D4; PF → PV."),
    (26, 'Mano Guaritrice', "Recupera 1D6 PF, fino ai PF massimi.", 'Oracolo', 'Nuova proposta', "Recuperi 1D6 PV, fino ai PV massimi.", "PF → PV."),
    (27, 'Scudo della Fede', "Ottieni (+1) AR fino al tuo prossimo turno.", 'Oracolo', 'Nuova proposta', None, None),
    (28, 'Colpo Poderoso', "Il tuo prossimo attacco infligge (+2) Danni.", 'Guerriero', 'Nuova proposta', None, None),
    (29, 'Grido di Battaglia', "Ottieni (+2) al prossimo tiro per colpire.", 'Guerriero', 'Nuova proposta', None, None),
    (30, 'Parata Perfetta', "Annulla i Danni di un attacco subito.", 'Guerriero - Oracolo', 'Nuova proposta', None, None),
    (31, 'Carica Impetuosa', "Aggiungi (+2) al tiro di Movimento; il tuo primo attacco di questo turno infligge (+1) Danno.", 'Guerriero', 'Nuova proposta', None, None),
    (32, 'Preghiera della Fonte', "Recupera (1) carta dalla pila degli scarti e (1) PF.", 'Oracolo', 'Nuova proposta',
     "Recupera (1) carta dalla tua pila degli scarti e (1) PV.", "PF → PV."),
    (33, "Sguardo dell'Oracolo", "Ritira un tiro di dado a tua scelta e tieni il nuovo risultato.", 'Oracolo', 'Nuova proposta', None, None),
    (34, 'Egida Sacra', "Se hai uno scudo equipaggiato, ottieni (+2) AR fino alla fine dello scontro.", 'Guerriero - Oracolo', 'Nuova proposta', None, None),
    (35, 'Fendente Radioso', "Infliggi 1D6 Danni alla creatura, (+2) se è un non morto.", 'Guerriero - Oracolo', 'Nuova proposta', None,
     "Non morti: Scheletro, Zombi e gli eroi Sanguar."),
    (36, 'Giuramento di Ferro', "Il prossimo Danno che subiresti è ridotto di (2).", 'Guerriero', 'Nuova proposta', None, None),
    (37, 'Colpo alle Spalle', "Se attacchi per primo, il tuo attacco infligge (+2) Danni.", 'Ladro', 'Nuova proposta', None, None),
    (38, 'Fortuna del Furfante', "Scarta questa carta per ritirare un tuo tiro per colpire.", 'Ladro', 'Nuova proposta', None, None),
    (39, 'Passo Felpato', "Ignori gli effetti della casella trappola in cui termini il movimento.", 'Ladro', 'Nuova proposta',
     "Ignori gli effetti della Trappola che peschi in questo turno.", "Con il sacchetto la Trappola si pesca quando ti fermi."),
    (40, 'Lancio di Coltello', "Prima dello scontro infliggi 1D4 Danni alla creatura.", 'Ladro', 'Nuova proposta',
     "All'inizio di uno scontro, prima del primo attacco, infliggi 1D6 − 1 Danni (minimo 1) alla creatura.", "Niente D4: D6 − 1."),
]

CLASSI = [
    ('TC-01', 'Guerriero', "La tua pedina è un Guerriero fino alla fine della partita. (+2) PV. Ogni scontro vinto ti dà l'Ispirazione; in scontro puoi spenderla per dare (-2) AR al nemico.", '+2 PV (regola di Daniele del 27/10: si parte da 5 PV)'),
    ('TC-02', 'Ladro', "La tua pedina è un Ladro fino alla fine della partita. (+2) MOV. Puoi fuggire da ogni scontro e fuggendo non arretri.", 'Bilanciamento v2: +2 MOV (era +3) e niente vantaggio nel primo round'),
    ('TC-03', 'Mago', "La tua pedina è un Mago fino alla fine della partita. Puoi ritirare i tuoi dadi fino a (2) volte per turno.", 'Bilanciamento v2: 2 ritiri per turno (era 1)'),
    ('TC-04', 'Oracolo', "La tua pedina è un Oracolo fino alla fine della partita. Quando vieni sconfitto in uno scontro torni in vita con (3) PV e continui lo scontro. Il potere si ricarica quando ti fermi in una Locanda.", 'Prende il posto del Chierico; bilanciamento v2: 3 PV (con 5 PV di partenza)'),
]

# Nemici: danno dal livello (LV 1 → D6 − 1, LV 2 → D6, LV 3 e oltre → D6 + 1); Difesa = 14 + AR (Daniele 27/10: colpire il 20% più difficile)
NEMICI = [
    # id, nome, tipo (mazzetto), lv, pv, att, ar, chiave effetto, effetto stampato
    # Mazzetto I: LV 1-2
    ('NE-01', 'Folletto Ingannatore', 'Nemico I', 1, 1, 2, 2, 'illusione', "Illusione: il tuo primo tiro per colpire si fa con svantaggio."),
    ('NE-02', 'Ratto gigante', 'Nemico I', 1, 1, 2, 0, 'veleno', "Morso infetto: se ti ha colpito almeno una volta, a fine scontro perdi 1 PV (non scendi sotto 1)."),
    ('NE-03', 'Pipistrello vampiro', 'Nemico I', 1, 1, 2, 1, 'succhia', "Succhiasangue: ogni volta che ti colpisce recupera 1 PV."),
    ('NE-04', 'Coboldo', 'Nemico I', 1, 2, 1, 0, 'codardo', "Codardo: con metà PV o meno ha −2 ATT."),
    ('NE-05', 'Gnomo schiavista', 'Nemico I', 1, 2, 2, 2, 'catene', "Catene: se ti sconfigge prendi 1 Clessidra."),
    ('NE-06', 'Goblin predone', 'Nemico I', 1, 2, 2, 1, 'saccheggio', "Saccheggio: se ti sconfigge scarti 1 carta a caso dalla mano."),
    ('NE-07', 'Scheletro', 'Nemico I', 1, 2, 2, 1, 'ricompone', "Non morto. Si ricompone: la prima volta che va a 0 PV torna a 2 PV."),
    ('NE-08', 'Lupo grigio', 'Nemico I', 1, 3, 3, 0, 'inseguitore', "Inseguitore: se fuggi, ti attacca un'ultima volta prima che tu arretri."),
    ('NE-09', 'Ragno delle grotte', 'Nemico I', 1, 3, 3, 1, 'ragnatela', "Ragnatela: non puoi fuggire."),
    ('NE-10', 'Orchetto predone', 'Nemico I', 2, 4, 2, 1, 'furia', "Furia: con metà PV o meno ha +2 ATT."),
    ('NE-11', 'Melma acida', 'Nemico I', 2, 5, 1, 0, 'acido', "Acido: quando ti attacca la tua AR conta 1 in meno."),
    ('NE-12', 'Zombi', 'Nemico I', 2, 4, 2, 0, 'lento', "Non morto. Lento: se fuggi non arretri."),
    ('NE-13', 'Bandito della strada', 'Nemico I', 2, 3, 3, 1, 'borseggio', "Borseggio: la prima volta che ti colpisce scarti 1 carta a caso dalla mano."),
    # Mazzetto II: LV 3-4
    ('NE-14', 'Gnoll cacciatore', 'Nemico II', 3, 5, 3, 1, 'agguato', "Agguato: attacca per primo."),
    ('NE-15', 'Orso delle caverne', 'Nemico II', 3, 7, 3, 0, 'furia', "Furia: con metà PV o meno ha +2 ATT."),
    ('NE-16', 'Arpia', 'Nemico II', 3, 4, 4, 1, 'illusione', "Picchiata: il tuo primo tiro per colpire si fa con svantaggio."),
    ('NE-17', 'Spettro', 'Nemico II', 3, 4, 3, 2, 'gelo', "Non morto. Gelo: hai −1 ATT per tutto lo scontro."),
    ('NE-18', 'Minotauro', 'Nemico II', 4, 8, 4, 1, 'carica', "Carica: il suo primo colpo fa +2 danni."),
    ('NE-19', 'Golem di fango', 'Nemico II', 4, 9, 3, 2, 'coriaceo', "Coriaceo: i danni che subisce sono ridotti di 1 (minimo 1)."),
    ('NE-20', 'Vampiro', 'Nemico II', 4, 7, 4, 2, 'succhia', "Non morto. Succhiasangue: ogni volta che ti colpisce recupera 1 PV."),
    ('NE-21', 'Basilisco', 'Nemico II', 4, 7, 4, 1, 'pietrifica', "Pietrifica: se ti colpisce con un 6 al dado del danno, prendi 1 Clessidra."),
    # Mini-boss LV 4,5: regola facoltativa, si mescolano nel mazzetto II
    ('NE-22', 'Ogre delle paludi', 'Mini-boss', 4.5, 10, 4, 1, 'rompiscudo', "Rompiscudo: se ti colpisce con un 6 al dado del danno, fai subito il tiro di perdita."),
    ('NE-23', 'Troll di fiume', 'Mini-boss', 4.5, 9, 4, 2, 'rigenera', "Rigenera: all'inizio di ogni suo attacco recupera 1 PV."),
    ('NE-24', 'Capitano goliath', 'Mini-boss', 4.5, 8, 5, 2, 'agguato', "Agguato: attacca per primo."),
    ('NE-25', 'Strega del vischio', 'Mini-boss', 4.5, 8, 5, 1, 'vischio', "Vischio: non puoi fuggire e hai −1 ATT per tutto lo scontro."),
    # Boss LV 5: se ne pesca uno a inizio partita; le ferite dei boss restano
    ('NE-26', 'Guardiano di MIMI', 'Boss', 5, 9, 4, 3, 'rompiscudo', "Colpo del custode: se ti colpisce con un 6 al dado del danno, fai subito il tiro di perdita."),
    ('NE-27', 'Mimic ancestrale', 'Boss', 5, 7, 5, 2, 'agguato', "Fauci: attacca per primo."),
    ('NE-28', 'Re Goblin Grugno', 'Boss', 5, 9, 4, 2, 'furia', "Furia: con metà PV o meno ha +2 ATT."),
]
DANNO = {1: 'D6 − 1', 2: 'D6', 3: 'D6 + 1', 4: 'D6 + 1', 4.5: 'D6 + 1', 5: 'D6 + 1'}
RICOMPENSE = {'Nemico I': '1 indizio\n1 punto esperienza', 'Nemico II': '1 indizio\n1 punto esperienza\nIspirazione', 'Mini-boss': '1 indizio\nsali di livello\nIspirazione', 'Boss': 'MIMI: vinci la partita'}
NOTA_BOSS = ' Le sue ferite restano tra uno scontro e l\'altro.'

def build():
    cards = []
    for i, r, n, o, t, m in MAPPE:
        cards.append(dict(id=i, tipo='TM', nome=n, rarita=r, classe='Tutte le classi', slot='', testo_originale=o, testo=t, modifica=m, origine='Tua carta' if n == 'Città Avanzata' else ('Proposta già impaginata' if i == 'TM-01' else 'Elenco v2')))
    for i, r, n, o, s, cl, org, t, m in EQUIP:
        cards.append(dict(id=i, tipo='TE', nome=n, rarita=r, classe=cl, slot=s, testo_originale=o, testo=t or o, modifica=m or '', origine=org))
    for k, n, o, cl, org, t, m in INC:
        cards.append(dict(id=f'TI-{k:02d}', tipo='TI', nome=n, rarita='', classe=cl, slot='', testo_originale=o, testo=t or o, modifica=m or '', origine=org))
    for i, n, t, m in CLASSI:
        cards.append(dict(id=i, tipo='TC', nome='Classe: ' + n, rarita='', classe=n, slot='', testo_originale='', testo=t, modifica=m, origine='Scatola base 21/10'))
    nem = []
    for i, n, tp, lv, pv, att, ar, fx, ab in NEMICI:
        nem.append(dict(id=i, lettera=n[0], nome=n, tipo=tp, lv=lv, pv=pv, att=att, ar=ar, difesa=14 + ar, danno=DANNO[lv], fx=fx, abilita=ab + (NOTA_BOSS if tp == 'Boss' else ''), ricompense=RICOMPENSE[tp], origine='Tua carta (effetto nuovo)' if i == 'NE-01' else 'Nemici a livelli 27/10'))
    return cards, nem

if __name__ == '__main__':
    c, n = build()
    json.dump(c, open('cards_v2.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(n, open('nemici_v2.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(x['tipo'] for x in c), len(n))
