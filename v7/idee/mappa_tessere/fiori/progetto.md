# Mappa a «fiori» da 7 esagoni: progetto (fase 1)

12/11/2026. Daniele ha scelto l'opzione B (`../proposte.md`): pezzi a fiore, cioè rosette da 7 esagoni, generici e componibili. Le sue indicazioni:
- stampa su A4 (la stampante non fa l'A3), cartoncino da 250-300 g oppure incollata su cartone;
- il fiume è un pezzo unico fronte/retro: Flegias usa il fiume senza mura;
- i lati esterni si tagliano dritti dove si può.

Questa è la fase 1: progetto e mock-up. Spec, carte e kit di stampa non sono stati toccati.

File di questa cartella:
- `fiori.py`: legge i 10 preset veri, sceglie la griglia, conta disegni e pezzi fronte/retro, rimonta e controlla ogni preset, prova le composizioni libere e calcola i tempi con il modello di `../tempo_setup.py`. Si lancia con `python3 v7/idee/mappa_tessere/fiori/fiori.py` (con `--catalogo` stampa anche l'elenco dei 60 pezzi). Tutti i numeri di questo documento sono il suo output.
- `disegna_fiori.py`: genera `fiori_strettoie.svg/.png` (il preset base montato con 18 pezzi, staccati di qualche mm) e `fiori_campioni.svg/.png` (4 pezzi del preset base più il retro del fiume). Gli SVG sono in mm, scala 1:1.

## In breve

| | Fiori (questa proposta) | Oggi (tile singole) |
|---|---|---|
| Pezzi a partita | **18** (8 fiori, 2 fiori di riva da 8 esagoni, 8 pezzi di bordo da 2-5) | 100 tile + 16 muri |
| Disegni (facce diverse) | **56** | 18 tipi |
| Pezzi fisici da tagliare | **60**: 52 fronte/retro, 8 con il retro libero per fiori extra | 162 + 24 muri |
| Fogli A4 | **16-18**: 8-9 di fronti e 8-9 di retri, 6-7 pezzi a foglio | 3 + 1 |
| Muri | **tutti stampati sui pezzi**, nessun listello | 16 listelli |
| Preset riprodotti esatti | **tutti e 10**: rimontati identici, strade continue, controlli del §17 passati | tutti |
| Montaggio, 1 persona (veloce / tipico / lento) | **1:18 / 2:06 / 3:32** | 7:00 / 11:13 / 17:57 |
| Montaggio, 2 persone | 0:49 / 1:24 / 2:31 | 3:59 / 6:46 / 11:31 |
| Cambio di mappa a metà partita (R 8.12) | 1:32 / 2:17 / 3:36 | 2:09 / 3:21 / 5:06 |
| Composizione libera valida | guidata 83-100 %, casuale 17 % (dettagli al §5) | – |

Per tutte le opzioni vanno aggiunti 40-55-80 s per mettere le tessere Esplorazione sulle 20 «?». Per confronto, le fasce dell'opzione D montano in 0:48 tipico.

## 1. Partizione

**Griglia.** Esistono 14 modi di posare la griglia dei fiori sulla mappa: 7 spostamenti per 2 versi di rotazione (`(a·q + b·r + spostamento) mod 7`, con (a, b) = (1, 3) o (1, 5)). Con ciascuno si ottengono 19-21 pezzi. **Solo 2 sono identici girati di 180°**, come i preset: (1,3)+5 e (1,5)+3. Con quelle due griglie il pezzo sud è il pezzo nord girato e usa lo stesso disegno. Con le altre 12 i disegni raddoppierebbero.

Ho scelto **(1,3)+5**: dà 10 fiori interi invece di 8. Ho poi unito al fiore vicino l'unico esagono rimasto da solo sul bordo, l'acqua A5 (e J6 al sud): il fiume continua dentro un pezzo solo e i pezzi scendono da 20 a 18.

Ho provato anche a unire i pezzi di bordo più piccoli, cioè E1-F1 alla striscia B1-D1. Il pezzo che ne esce non è uguale al suo specchio, quindi non può avere un retro: costa 6 pezzi fisici in più. Restano separati.

| Partizione (strade come area, muri stampati) | Pezzi a partita | Disegni | Pezzi fisici | Di cui con retro libero |
|---|---|---|---|---|
| (1,3)+5 senza unioni | 20 | 57 | 62 | 10 |
| **(1,3)+5 con A5 e J6 uniti ai fiori (scelta)** | **18** | **56** | **60** | 8 |
| (1,3)+5 con A5 e con E1-F1 unito alla striscia | 16 | 51 | 66 | 30 |
| (1,5)+3 senza unioni | 20 | 55 | 60 | 10 |

Numeri dei pezzi (sono gli stessi delle targhette nei mock-up). Ogni pezzo del nord, girato di 180°, è il suo compagno del sud: le coppie sono nella tabella qui sotto (0/14, 1/16, …).

```
      A    B    C    D    E    F    G    H    I    J
  1    0    1    1    1    2    2    3    3    4    4
  2      0    1    1    5    5    3    3    3    4    4
  3    0    6    6    5    5    5    3    3    7    7
  4      6    6    6    5    5    8    8    7    7    7
  5    6    6    6    9    9    8    8    8    7    7
  6     10   10    9    9    9    8    8   11   11   11
  7   10   10   10    9    9   12   12   11   11   11
  8     10   10   13   13   12   12   12   11   11   14
  9   15   15   13   13   13   12   12   16   16   14
 10     15   15   13   13   17   17   16   16   16   14
```

| Posizioni nord/sud | Esagoni | Forma | Esagoni che cambiano tra i preset | Disegni | Facce stampate |
|---|---|---|---|---|---|
| 0/14 | 3 | bordo (A1-A3) | 1 | 3 | 6 |
| 1/16 | 5 | bordo (B1-D1, B2-C2) | 2 | 8 | 16 |
| 2/17 | 2 | bordo (E1-F1) | 2 | 6 | 12 |
| 3/13 | 7 | fiore (Partenza 2) | 5 | 8 | 16 |
| 4/15 | 4 | bordo (I1-J2) | 1 | 4 | 8 |
| 5/12 | 7 | fiore (Cripta 1) | 3 | 7 | 14 |
| 6/11 | 8 | fiore di riva (fiume ovest) | 4 | 8 | 16 |
| 7/10 | 7 | fiore (Partenza 3) | 4 | 9 | 18 |
| 8/9 | 7 | fiore del fiume (ponte, guado, Cripta 2) | 0 | 3 | 6 |

**Misure.**
- Un fiore intero misura 75,6 × 72,8 mm: l'esagono resta di 25,2 mm, così la tessera Esplorazione da Ø 24 mm e le pedine ci stanno.
- I pezzi di bordo hanno il lato esterno dritto. Il triangolino tra gli esagoni e il bordo della mappa è una fascia «fuori mappa» color pergamena scura: non è un esagono e non conta.
- La mappa montata è di 265 × 226 mm, come oggi.

## 2. Meno disegni: parti comuni, simmetria, fronte e retro

1. **Simmetria.** Ogni disegno serve per il pezzo nord e per il pezzo sud girato, quindi si stampa in 2 copie. Bastano 56 disegni per 112 facce, invece di 112 disegni.
2. **Parti comuni.** Un pezzo ha lo stesso disegno in tutti i preset in cui ha gli stessi esagoni e gli stessi muri. Il fiore del fiume 8/9, per esempio, è uguale in 8 preset su 10. Le varianti per posizione vanno da 3 a 9.
3. **Strada come terreno.** Il disegno di un esagono dipende solo dal suo tipo e non dai vicini. Con la prima bozza (un sentiero che esce dal pezzo solo se il vicino è strada) servivano 65 disegni e 68 pezzi; ora ne bastano 56 e 60.
4. **Fronte e retro.** Due facce stanno sullo stesso pezzo solo se nessun preset le usa tutte e due insieme, e se la forma del retro (che è specchiata) va bene per l'altra posizione. Tutte le forme scelte sono uguali al loro specchio. Lo script accoppia prima due disegni della stessa posizione (per esempio «base | TM-08», ×2), poi fa l'accoppiamento migliore tra i disegni avanzati. Risultato: **60 pezzi fisici per 112 facce**. Il minimo teorico è 56.
5. **Fiume fronte/retro (richiesta di Daniele).** Il fiume del ponte (8/9) ha 3 disegni, che si distinguono per le mura vicino al ponte (qui per il pezzo 8; il 9 è lo stesso girato): G5|H5 in 8 preset; F4|G5 al posto di G5|H5 in Flegias; G5|H5 e F4|G5 insieme in Yuma (TM-07). Il conteggio dei pezzi resta lo stesso se il retro del fiume «degli 8 preset» è Flegias. In fase 2 imposto così l'accoppiamento, come chiesto.
6. **Fiori extra per il playtest.** Gli 8 retri liberi diventano fiori generici senza costo in più, cioè senza nuovi pezzi:
   - 4 fiori interi (retri dei pezzi 5/12 e 7/10), per esempio «Crocevia» (tutta strada con una «?»), «Boschetto», «Cava», «Borgo»;
   - 2 fiori del fiume (retri di 8/9), per esempio un fiume con il solo guado e un laghetto;
   - 2 pezzi di bordo da 3 esagoni (retri di 0/14).
   Se ne servono altri, ogni pezzo fronte/retro in più dà 2 fiori extra.

**Stampa e taglio (stima, l'impaginazione vera è in fase 2).**
- In un A4 orizzontale entrano 7 fiori a nido d'ape con 1,5 mm di abbondanza a testa, o 6 con 2,5 mm. I pezzi di bordo valgono 0,2-0,8 posti, i fiori di riva 1,25. I 60 pezzi occupano 52,9 posti: **8-9 fogli di fronti e 8-9 di retri, 16-18 A4 in tutto.**
- I retri si stampano con il foglio specchiato e con 2,5 mm di abbondanza, così 1-2 mm di scarto tra fronte e retro non lasciano bianco. Si taglia seguendo il fronte.
- Per tenerli piatti, conviene stampare su carta da 120-160 g e incollare fronte e retro sui due lati di un cartone da 1 mm. In alternativa si incollano dorso contro dorso due cartoncini da 160 g. I lati dei pezzi sono tutti segmenti dritti, quindi si tagliano bene con cutter e righello.

## 3. Regole di bordo: le zone hanno senso quando si uniscono

1. **La strada è un terreno, non un sentiero.** Nei preset ogni esagono di strada è percorribile verso tutti i vicini di strada (R 8.3-8.4). Il disegno lo dice così: ogni esagono di strada è terra battuta (`#e8cd8f`, con chiazze di pergamena) fino ai suoi lati, e si fonde con gli esagoni di strada vicini. Due esagoni di strada si toccano su tutto il lato, anche se stanno su pezzi diversi, quindi **la strada combacia sempre tra un pezzo e l'altro** senza regole sui punti di uscita. Dove la strada incontra un ostacolo, finisce sul lato. Dentro un pezzo c'è al massimo un filo di traccia tratteggiato, ad albero (senza triangoli), che non esce dal pezzo: suggerisce un percorso senza far credere che il movimento segua le linee.
2. **Nessun «prato vuoto».** Ho controllato i dati: nei 10 preset tutti i 100 esagoni sono strada (64, contando «?», Partenze, Cripte, guadi e ponti) oppure ostacolo (36: bosco, case, rocce, acqua). Nessun esagono è vuoto. Il verde chiaro della prima bozza era solo lo sfondo degli esagoni di strada ed è stato tolto. Ora ogni ostacolo riempie tutto l'esagono:
   - bosco: fondo verde pieno, macchia scura e alberi;
   - rocce: fondo grigio pieno e massi;
   - case: fondo di coppi e un borgo di 3 casette;
   - acqua: azzurro pieno.
3. **Acqua.** Acqua, guadi e ponti sono una macchia unica dentro il pezzo, con le rive arrotondate. Il fiume attraversa i pezzi sempre sulle stesse caselle (righe 5-6, uguali in tutti i preset), quindi continua da un pezzo all'altro. Il ponte (assi di legno) e il guado (sassi) puntano solo verso caselle di strada che sono uguali in tutti i preset, quindi anche loro combaciano sempre.
4. **Bosco, rocce e case.** Ogni macchia sta dentro i suoi esagoni e si unisce solo agli esagoni dello stesso tipo dentro lo stesso pezzo; tra due pezzi si incontrano sul lato.
5. **Muri.** Sono stampati: una striscia di pietra con 2 rivetti d'ottone sul lato tra due esagoni. Un muro che sta sul taglio tra due pezzi è stampato su uno solo dei due: lo script prova tutte le scelte, simmetriche nord/sud, e tiene quella con meno disegni.
6. **Bordi d'esagono** sottili ma leggibili (0,3 mm, inchiostro al 50 %), sopra il terreno e sotto le icone: servono a contare i passi.
7. **Icone:**
   - «?»: tondo chiaro con il punto di domanda nero (la tessera Esplorazione lo copre);
   - Partenza: tondo viola con il numero e una bandierina di rame;
   - Cripta: arco di pietra, ingranaggio d'ottone e tondo d'oro con il numero.
8. **Targhetta:** piccola (1,45 mm), nell'angolo in basso a destra di un esagono senza icone. Riporta la posizione e i preset che usano quella faccia, per esempio «7 · base 07» (07 = TM-07). Serve a trovare il pezzo nella pila.

**Verifica dello script (le 10 righe sono tutte uguali):** ogni preset rimontato dalle sue facce ha **terreno e muri identici all'originale**, **0 lati** con la strada che non combacia, **controlli del §17 passati**, Partenza→Cripta da 4 a 8 passi e Cripta più vicina a 4 passi da ogni Partenza.

## 4. Muri: decisione

**Tutti stampati.**

| Strade come area | Disegni | Pezzi fisici | Listelli da posare a partita |
|---|---|---|---|
| Muri stampati | 56 | 60 | 0 |
| Solo i muri delle Cripte stampati, le mura libere a listello | 52 | 58 | 6 |

Stampare anche le mura libere costa 2 pezzi in più, ma ogni partita risparmia 6 listelli: circa 35 s di montaggio, e nessun listello che si sposta o si perde. I 24 listelli del kit di oggi restano utili per la composizione libera.

## 5. Composizione libera: quante combinazioni restano valide

Le combinazioni sono estratte a caso con seme fisso. Dato che la strada è un terreno, ogni combinazione ha anche le strade continue: resta da controllare solo il §17.

| Come si compone | Mappe provate | Valide §17 |
|---|---|---|
| Guidata: metà nord di un preset e metà sud di un altro | 90 | **100 %** |
| Guidata: un preset con una coppia di pezzi (nord e sud) presa da un altro preset | 470 | **83,2 %** |
| Casuale per posizione: ogni pezzo da un preset a caso, Partenze, Cripte e fiume restano al loro posto | 20.000 | 17,3 % |
| Casuale, fiori ovunque: fiori interi di qualsiasi posizione, girati a caso | 5.000 | 2,6 % con grafo valido; 0 % con Partenze 1-6 e Cripte 1-4 una volta ciascuna |

Che cosa vuol dire:
- I pezzi dei preset si combinano bene se si scambiano poco alla volta, cioè mezza mappa o una coppia di pezzi.
- A caso, il §17 si rompe quasi sempre: o un esagono blocca una zona, o le Cripte non hanno più 3 ingressi.
- I fiori interi messi ovunque spostano Partenze e Cripte, quindi servono solo come varianti locali.
- Per la composizione libera vera servono i fiori extra generici del §2 e la regola del playtest «controlla il §17 dopo aver composto» (R 8.1).

## 6. Tempi di montaggio

Il modello è quello di `../tempo_setup.py`, con le stesse costanti e le stesse fonti (KLM, Hick-Hyman, Fitts, stime da tavolo). Per ogni posizione:
- si legge il numero sullo schema del preset;
- si sceglie la pila della posizione (9 pile: Hick);
- nella pila si cerca la faccia del preset leggendo la targhetta, in media guardando metà dei pezzi e girandone alcuni;
- si prende il pezzo e lo si accosta ai vicini (Fitts, 2 mm);
- lo si orienta e si mettono a posto gli urti.

A questo si aggiungono il controllo finale e il tempo fisso (tirare fuori i pezzi, Sala del Tesoro).

| | Veloce | Tipico | Lento |
|---|---|---|---|
| Montaggio, 1 persona | 1:18 | **2:06** | 3:32 |
| Montaggio, 2 persone | 0:49 | 1:24 | 2:31 |
| Cambio di mappa a metà partita, base → TM (R 8.12) | 1:32 | 2:17 | 3:36 |
| Riordino a fine partita (pezzi nelle 9 pile) | 0:18 | 0:27 | 0:40 |

Il montaggio è 5 volte più veloce di oggi (11:13). Resta circa 2,5 volte più lento delle fasce D (0:48), perché i pezzi sono 18 e quasi ognuno va cercato nella sua pila tra 4-9 pezzi a due facce.

Il cambio di mappa cambia in media quasi tutti i pezzi tranne il fiume. In più le tessere Esplorazione vanno spostate dalle «?» dei pezzi tolti ai pezzi nuovi.

## 7. Catalogo dei 60 pezzi fisici

L'elenco completo, un pezzo per riga, si ottiene con `fiori.py --catalogo`. In sintesi (01 = TM-01; «×2» vuol dire due pezzi uguali, uno per il nord e uno per il sud):

| Posizioni | Pezzi fronte \| retro |
|---|---|
| 0/14 | (07 \| base 02 05 08) ×2; (01 03 04 06 09 \| libero) ×2 |
| 1/16 | (base \| 08) ×2; (06 \| 04) ×2; (02 \| 01) ×2; (05 09 \| 03 07) ×2 |
| 2/17 | (base \| 07) ×2; (04 \| 01) ×2; (03 05 09 \| 02 06 08) ×2 |
| 3/13 | (09 \| 08) ×2; (06 \| 05) ×2; (04 \| 03) ×2; (02 \| base 01 07) ×2 |
| 4/15 | (base \| 09) ×2; (02 05 06 \| 01 03 04 07 08) ×2 |
| 5/12 | (09 \| 05) ×2; (04 \| 03) ×2; (01 \| 06 08) ×2; (base 02 07 \| libero) ×2 |
| 6/11 | (base \| 08) ×2; (07 \| 06) ×2; (04 \| 01) ×2; (03 09 \| 02 05) ×2 |
| 7/10 | (09 \| 08) ×2; (06 \| 05) ×2; (04 \| 03) ×2; (02 \| 01) ×2; (base 07 \| libero) ×2 |
| 8/9 (fiume) | (08 \| 07) ×2; (base 01 02 03 04 05 06 09 \| libero) ×2. In fase 2: (con mura \| Flegias) ×2 e (Yuma \| libero) ×2, stesso numero |

## 8. Per la fase 2 (dopo il via di Main)

1. Impaginare i 60 pezzi sui fogli A4 di fronti e retri (retri specchiati, con le crocette per allinearli) e decidere i disegni dei fiori extra.
2. Fare lo schema di montaggio di ogni preset: 18 numeri di posizione, nessuna coordinata.
3. Stampare una prova di un foglio per misurare il disallineamento tra fronte e retro sulla stampante di Daniele.
4. Aggiornare la Spec (D23, R 8.1, R 8.12, §2, §17) e il kit (`componenti_gen`, `verifica_pdf.py`, `LEGGIMI.md`).
5. Cronometrare un montaggio vero e correggere le costanti del modello.
