# Mappa 12×12, segnalini e rotelle in 3D con SolidCraft (12-13/11)

Daniele ha deciso che i pezzi 3D si fanno con **SolidCraft**, non più con Blender. La vecchia pipeline Blender (tessere singole con muri, D23) è stata tolta.

La mappa è quella a fiori 12×12. Le posizioni vengono da `v7/stampa/sorgenti/dati/base12.csv`: spazi 1-14, posizioni 0-6, esagoni di bordo. Le carte vengono dal kit: `playtest_v7/mappa_base.pdf` e `mappa_fiori.pdf`.

Dal 13/11 (D29: i 24 segnaposto «?» non ci sono più) sono in 3D anche **tutti i segnalini e le tessere del kit e le rotelle**, con gli adesivi in `playtest_v7/segnalini_3d.pdf`. Le quantità vengono dai CSV del kit (`tessere_esplorazione.csv`, `segnalini.csv`, `stati.csv`) e dalle rotelle di `gen.py`.

## Pezzi

| Pezzo | Quanti | Ingombro (mm) | PLA |
|---|---|---|---|
| `vassoio_NO`, `vassoio_NE`, `vassoio_SO`, `vassoio_SE` | 1 per tipo | 174,4 × 144,9 × 3,2 al massimo, code comprese | 49-56 g l'uno, 210 g in tutto |
| `fiore` | 14 | 75,2 × 72,3 × 3 | 9,6 g |
| `segnalino_cripta` | 1 | 27,4 × 31,6 × 2 (esagono) | 1,2 g |
| `tessera_esplorazione` | 36 | Ø 24 × 2 | 0,9 g |
| `segnalino_tondo` (oggetti `segnalino_indizio`, `segnalino_forte_volonta`, `segnalino_usato`) | 16 + 4 + 20 | Ø 20 × 2 | 0,6 g |
| `tessera_stato` | 31 | 26 × 18 × 2 | 0,9 g |
| `rotella_finestra_11x9` (oggetti `rotella_PV`, `_ATT`, `_MOV`, `_AR`, `_scontro`, `_custode`) | 4 + 4 + 4 + 4 + 1 + 1 | Ø 52 × 2 | 3,9 g |
| `rotella_finestra_9x9` (oggetti `rotella_Danni`, `rotella_PL`) | 4 + 4 | Ø 52 × 2 | 3,9 g |
| `rotella_finestra_10x9` (oggetto `rotella_Profezia`) | 1 | Ø 52 × 2 | 3,9 g |
| `perno` | 27 | Ø 10 × 5,55 | 0,12 g |
| `fermo` | 27 | Ø 12 × 1,2 | 0,13 g |

- **Vassoio**: montato misura 329 × 283 mm.
  - Ha un fondo da 1,2 mm.
  - Ha un **alloggio unico per i 14 fiori**, profondo 2 mm.
  - Sopra ha una **tasca per la carta della base**: è `mappa_base.pdf` con le coordinate, ritagliata lungo il contorno d'ottone degli spazi.
  - Sul fondo dell'alloggio sono **incisi il numero di ogni spazio e le cifre 1-6 dell'anello**, come sulla carta della base, che lì viene tolta. Servono per la freccia dei preset.
  - Le 4 parti si uniscono con **code a pomello** nel fondo, lungo i lati degli esagoni. Una coda per lato del taglio: 23 tra NO e le altre, 11 tra NE e SE, 11 tra SO e SE.
- **Fiore**: rosetta **senza incastri**, spessa 3 mm. Sporge 1 mm dal vassoio, così si prende con le dita.
  - **Fondo piatto** (12/11, Daniele dopo la prima stampa): la tasca per la carta c'è **solo sopra**, profonda 0,5, con 2,5 mm di pieno sotto. Il fiore 3D quindi non si volta: porta una sola faccia.
  - Entra in qualsiasi spazio, girato di 60° in 60°.
  - Gli spigoli sono smussati di 0,4 mm, sopra e sotto.
- **Segnalino Cripta**: tasca sopra per la carta del foglio 3 di `mappa_fiori.pdf` (esagono da 25,2; le due facce sono uguali). Sporge di 1,1 mm per lato oltre l'esagono della mappa: è un segnalino che si appoggia sopra.
- **Segnalini del kit in 3D** (tessere Esplorazione, Indizio, Forte Volontà, Usato, tessere Stato, dischi delle rotelle):
  - il **contorno è esattamente quello del pezzo di carta** (Ø 24, Ø 20, 26 × 18 con angoli da 1,2, Ø 52), così il pezzo 3D sta negli stessi posti della carta: esagono della mappa, cerchi Ø 22 e riquadri degli Stati della plancia, corone delle rotelle;
  - fondo piatto, smusso di 0,4 sopra e sotto, **bordino da 0,85 e tasca sopra profonda 0,5** (stessa regola dei fiori): l'adesivo è la tasca meno 0,25 per lato, cioè 2,2 mm più piccolo del pezzo di carta (Ø 21,8, Ø 17,8, 23,8 × 15,8, corona Ø 49,8);
  - la **tessera Stato è rettangolare** come la carta: si vede se è verticale o orizzontale;
  - la **tessera Esplorazione** porta il fronte nella tasca sopra e il **dorso incollato sul fondo piatto** (adesivo Ø 21,8 al centro, 1,1 mm di margine): coperta mostra il dorso;
  - la **rotella** ha la **finestra passante** a 20 mm dal centro, grande quanto quella del disco di carta + 0,25 per lato (l'adesivo, intagliato sulla finestra di carta, copre il bordo della plastica), e un **mozzo pieno** di raggio 6,25 al centro col foro Ø 3,8 del perno: l'adesivo è una corona con il foro Ø 13 e l'intaglio della finestra aperto verso il bordo.
- **Perno della rotella** in 2 pezzi a scatto (uno per rotella, 27):
  - **perno**: testa Ø 10 × 0,8 **sotto la plancia**, fusto Ø 3,4 che passa nel foro Ø 4 della plancia e nel foro Ø 3,8 della rotella, **gola** Ø 2,9 sopra il mozzo, **dente** Ø 3,4 e punta a cono a 45°. Si stampa in piedi sulla testa; l'unico sbalzo è il sotto del dente, 0,25 mm in orizzontale;
  - **fermo**: disco Ø 12 × 1,2 con **2 ganasce a sbalzo** (lunghe 4,2, larghe 1 alla radice, fessure da 0,7) che si aprono **nel piano** quando la punta ci passa in mezzo e si richiudono nella gola. Si stampa piatto, su una faccia qualsiasi;
  - montaggio: perno dal retro della plancia, rotella sopra la corona, fermo premuto sulla punta finché scatta. Si smonta allargando le ganasce con un'unghia o un cacciavite piccolo.

## Perché un vassoio e non pezzi a incastro

Prima ho fatto e controllato pezzi a incastro, con una coda e un incavo su ogni lato, che funzionavano in qualunque rotazione. Il vassoio però è migliore:
- i fiori si voltano, e un incastro che regge anche voltato complicherebbe tutti i pezzi;
- gli spazi tengono i fiori al loro posto;
- i fiori si prendono e si rimettono facilmente durante il draft;
- l'unico incastro rimasto è quello tra le 4 parti del vassoio, che serve solo per il piatto della stampante.

## Carta

- **Base**: `playtest_v7/carta_base_3d.pdf`, 4 fogli A4, uno per quarto (NO, NE, SO, SE), generato da `carta_base_3d.py` (`python3 v7/stampa/3d_solidcraft/carta_base_3d.py --verifica`).
  - Ogni foglio ha la **sagoma esatta della tasca di carta di quel quarto** (`paper_pocket()` del generatore: gioco di 0,15 mm tra le parti, fascia di carta da 5,5 + 0,25, spazi dei fiori tolti). Si ritaglia sulla linea scura e si posa a filo nella tasca del quarto corrispondente.
  - Stampa solo la cornice: gli esagoni di bordo (arte `MB-BASE.png`), le Partenze e le coordinate. Gli spazi dei fiori non si stampano.
  - Su ogni foglio: segmento di controllo di 100 mm ed etichetta del quarto. Stampa al 100 % con `print-scaling=none`.
  - Perché non più `mappa_base.pdf`: le sue 2 metà hanno un taglio dritto sulla giunzione e coprono tutta l'altezza, mentre i quarti del vassoio seguono i lati degli esagoni (il NO misura 169,4 × 143,8 mm). Passo, origine ed esagoni coincidono (scarto < 1e-13 mm), ma il profilo della carta no.
  - **Sempre generata**: `build.sh` (rigenerazione normale del kit A4) lancia `carta_base_3d.py --verifica`; se il PDF manca o il taglio si scosta più di 0,2 mm dalla tasca la build fallisce. Scarto misurato: 0,001 mm.
  - **Scala**: `verifica_pdf.py` misura a 600 dpi il segmento di 100 mm di ogni foglio (errore oltre lo 0,05 %). I PDF di `vectorcraft-cli` sono esatti (100 mm = 100,00 mm): lo 0,12 % che si vedeva con `pdftocairo -svg` era un artefatto di quello strumento (aggiunge una matrice 0,998785 che nel PDF non c'è).
  - Il vassoio non è cambiato. `mappa_base.pdf` (base intera con l'interno, con segmento di controllo di 100 mm) si genera sempre e serve per la versione carta e per i test.
- **Fiori**: `out/carta_fiori_3d.pdf`, 5 fogli A4, **solo fronte**, 28 facce, una per pezzo.
  - La **linea di taglio è 1,3 mm dentro il contorno ideale**: 0,2 di gioco del fiore, 0,85 di bordino e 0,25 di gioco della carta.
  - La faccia tagliata misura 73,0 × 69,7 mm.
  - La freccia d'ottone e l'id piccolo sono spostati dentro la linea di taglio.
  - Si incolla una faccia nella tasca sopra del fiore 3D. Per avere anche le facce B servono altri 14 fiori 3D.
  - Il PDF usa il disegno di `sorgenti/componenti_gen/fiori12.py`: vettoriale, oppure l'arte generata `sorgenti/arte/png/MF-<NN><A|B>.png` se c'è (`GOBLIN_ARTE_MAPPA=CARTELLA` per un'altra cartella). Senza arte `mappa_fiori.pdf` e `carta_fiori_3d.pdf` restano uguali.
- **Cripta**: la carta di `mappa_fiori.pdf`, foglio 3 (anche in `segnalini_3d.pdf`), tagliata sulla sua linea. Tasca esagonale da 25,7, profonda 0,5.
- **Adesivi dei segnalini e delle rotelle**: `playtest_v7/segnalini_3d.pdf`, 6 fogli A4 solo fronte, ognuno col segmento di controllo di 100 mm. Lo genera `gen.py segnalini_3d()` dentro `build.sh` (misure delle tasche lette da questo script, `G3.P`):
  1. fronti delle 36 Tessere Esplorazione (Ø 21,8) e la carta della Cripta;
  2. dorsi delle 36 tessere (Ø 21,8, da incollare sul fondo piatto);
  3. 31 tessere Stato (23,8 × 15,8) e 40 segnalini tondi (Ø 17,8: 16 Indizio, 4 Forte Volontà, 20 Usato);
  4. e 5. le 6 rotelle di 2 plance per foglio (PV, Danni, ATT, MOV, AR, PL), corone Ø 49,8 col foro Ø 13 e l'intaglio della finestra;
  6. rotelle dello scontro, del custode e della Profezia.
  - L'arte è quella dei pezzi di carta: tessere e segnalini in scala uniforme (0,908 e 0,89), Stati in scala 23,8/26 × 15,8/18 (la larghezza cresce del 4 % rispetto all'altezza), rotelle in scala 1 (la finestra deve stare sulla corona della plancia) tagliate sulla corona dell'adesivo.
  - **Controllo**: `python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py --verifica-adesivi playtest_v7/segnalini_3d.pdf` legge ogni linea di taglio (tratto da 0,2 mm) dal PDF, la confronta con l'adesivo atteso (scarto di Hausdorff), misura il gioco per lato verso la tasca, conta gli adesivi per tipo e misura a 600 dpi il segmento di 100 mm di ogni foglio. Esce con errore oltre 0,2 mm o con conteggi sbagliati.
- **Plancia eroe e basi delle rotelle** (svg.py `dial_ring`): al centro di ogni corona c'è il cerchio **Ø 4** del foro per il perno 3D (col punteruolo al centro resta buono per il fermacampioni). Il foro Ø 4 si fa con una fustella da pelle o un punteruolo largo; la testa Ø 10 del perno lo copre.

## File

Sono tutti in `out/`:
- `*.solidcraft`: **documenti parametrici**. Ogni coordinata è un'espressione dei parametri. In SolidCraft, nella tabella dei parametri, se ne cambia uno e il pezzo si ricostruisce. L'ho provato su un vassoio con `passo` 26, `margine` 9, `gioco` 0,25 e `fondo` 1,6: nessun errore. Segnalini, rotelle, perno e fermo usano gli stessi parametri (`tessera_d`, `gettone_d`, `stato_l`, `rotella_d`, `perno_d`...).
- **I file da stampare: 4 file 3MF, uno per tipo di pezzo** (Daniele, 13/11 18:18; il vecchio `mappa_completa.3mf` non c'è più). Ognuno ha i suoi piatti da 220 × 220, affiancati lungo X ogni 230 mm:

  | File | Pezzi | Piatti |
  |---|---|---|
  | `mappa.3mf` | 4 quarti del vassoio + 14 fiori | 8: un quarto per piatto (1-4), fiori 4 + 4 + 4 + 2 (5-8) |
  | `rotelle_fulcri.3mf` | 27 rotelle (4 × PV, Danni, ATT, MOV, AR, PL; scontro, custode, Profezia) + 27 perni + 27 fermi | 4 |
  | `segnalini.3mf` | 31 tessere Stato, 16 Indizi, 4 Forte Volontà, 20 Usato, 1 Cripta | 2 |
  | `tessere_esplorazione.3mf` | 36 Tessere Esplorazione | 1 |

  I pezzi distano almeno 5 mm tra loro e dal bordo e stanno tutti a z = 0. Un oggetto per nome (lo stesso STL può dare più oggetti: `rotella_PV`, `rotella_ATT`, `segnalino_indizio`... per assegnare i colori), un'istanza per copia, nomi «Piatto N · oggetto»; lo script rilegge ogni file e ricontrolla le quantità. Sono 3MF standard, senza i metadati di piatto di Bambu Studio / OrcaSlicer: nello slicer si separano i piatti a mano o si usa «disponi». Li rifà anche `genera_3d_solidcraft.py --solo-3mf`, dagli STL già in `out/`.
- `*.stl`: un pezzo per file, in mm. Le parti del vassoio sono nella loro posizione sulla mappa, con l'origine al centro della mappa: lo slicer le porta al centro del piatto.
- `*.png`: le anteprime. `verifica_vassoio_fiori*.png` mostra il vassoio montato con i 14 fiori; `piatto_segnalini.png` il piatto 1 di `segnalini.3mf`; `verifica_perno_sezione.png` la sezione di perno, plancia, rotella e fermo montati.
- `verifica_perno.solidcraft`: la prova di montaggio del perno (plancia da 0,3 col foro Ø 4, rotella, perno, fermo).
- `verifica_vassoio_fiori.solidcraft`: la prova di montaggio. I fiori sono girati di (spazio mod 6) × 60°.
- `carta_fiori_3d.pdf`: le facce dei fiori per la versione 3D.
- `risultati.json`: tutte le misure.

## Come si rigenera

```
python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py
```

Ci vogliono circa 2 minuti. Servono:
- python3 con shapely ≥ 2.1 e numpy;
- `solidcraft-cli` (SolidCraft ≥ 0.40);
- per il PDF, `vectorcraft-cli` e `pdfcraft-cli`, gli stessi del kit.

Lo script:
- calcola la pianta;
- scrive gli script SolidCraft;
- costruisce ed esporta i pezzi;
- confronta volume e ingombro misurati in SolidCraft con quelli calcolati;
- monta le prove;
- scrive anteprime, PDF e `risultati.json`.

Se un controllo non passa, si ferma con `CONTROLLI FALLITI`.

I parametri sono in cima a `genera_3d_solidcraft.py` (`PARAMETRI`, in mm): si cambiano lì e si rilancia, così si rifanno anche le prove.

| Parametro | Valore | Che cosa è |
|---|---|---|
| `passo` | 25,2 | esagono da lato a lato, cioè la distanza tra i centri |
| `margine` | 7 | bordo del vassoio oltre la mappa: la carta ha 5,5 di fascia, poi 1,1 mm di bordino |
| `gioco` | 0,15 | gioco per lato tra le parti del vassoio e sulle code (0,3 in tutto) |
| `gioco_fiore` | 0,2 | gioco per lato tra fiore e alloggio (0,4 tra due fiori) |
| `fondo` | 1,2 | fondo del vassoio, che è anche l'altezza delle code |
| `alloggio_prof` | 2 | profondità dell'alloggio dei fiori |
| `fiore_spessore` | 3 | spessore del fiore |
| `tasca_prof` | 0,5 | profondità delle tasche per la carta |
| `bordino` | 0,85 | bordino tra contorno e tasca |
| `gioco_carta` | 0,25 | gioco per lato tra carta e tasca |
| `fascia_carta` | 5,5 | fascia della carta della base (`FASCIA12` del kit) |
| `segnalino_spessore` | 2 | spessore di Cripta, tessere, segnalini e Stati |
| `tessera_d`, `gettone_d` | 24 / 20 | diametro delle Tessere Esplorazione e dei segnalini tondi (come la carta) |
| `stato_l`, `stato_a`, `stato_r` | 26 / 18 / 1,2 | tessera Stato e raggio degli angoli (come la carta) |
| `rotella_d`, `corona_r`, `rotella_spessore` | 52 / 20 / 2 | disco della rotella, distanza della finestra dal centro, spessore |
| `mozzo_r` | 6,25 | mozzo pieno al centro della rotella, dove appoggia il fermo |
| `foro_perno`, `perno_d`, `collo_d` | 3,8 / 3,4 / 2,9 | foro della rotella, fusto e dente del perno, gola |
| `testa_d`, `testa_h` | 10 / 0,8 | testa del perno, sotto la plancia |
| `carta_plancia` | 0,3 | spessore della plancia di cartoncino: con 0,1-0,45 il fermo scatta ancora |
| `fermo_d`, `fermo_h` | 12 / 1,2 | fermo del perno |
| `gioco_assiale` | 0,15 | aria tra fermo e dente con la plancia da 0,3 |
| `smusso` | 0,4 | smusso degli spigoli di fiore e segnalini |
| `raggio_angolo` | 3 | angoli esterni del vassoio |
| `coda_collo`, `coda_testa`, `coda_lunga` | 2,6 / 4 / 3,9 | coda a pomello tra le parti, come nella versione Blender |
| `numero_alto`, `cifra_alta`, `incisione` | 8 / 4 / 0,4 | numeri incisi sul fondo: 0,4 mm di profondità, sotto restano 0,8 mm di fondo (13/11, scelta di Daniele: prima 0,5 e 0,7 mm) |

## Controlli (ultimo giro)

- **Volumi**: in SolidCraft sono uguali a quelli calcolati, con un errore relativo tra 1e-13 e 1e-7. Gli ingombri coincidono. STL chiusi (0 lati aperti). Ogni 3MF è in mm, con un oggetto.
- **Vassoio montato con i 14 fiori**: 0 intersezioni (`inspect.interference`). Giochi misurati faccia contro faccia, lato per lato:
  - tra le parti del vassoio: **0,30 mm** su 45 tagli;
  - tra coda e incavo: **0,30 mm** su 45 code. Qui contano raggi e assi dei cilindri, perché la distanza tra facce curve SolidCraft la misura sulla mesh e darebbe 0,284;
  - tra due fiori vicini: **0,40 mm** su 81 lati, con i fiori girati di 0-300°;
  - tra fiore e parete dell'alloggio: **0,20 mm** su 86 lati. Su 4 lati la parete cade su un taglio del vassoio, che la arretra di 0,15 mm, e il gioco è 0,35 mm.
- **Presa delle code**: tirando una parte di 0,6 mm le code urtano (3,6-4,1 mm³ di intersezione; 0,2 mm³ tra NO e SE, che hanno un solo lato in comune). Il gioco a trazione è 0,30-0,33 mm.
- **Fondo piatto**: fiore, Cripta, tessere, segnalini, Stati, rotelle e fermo hanno una sola faccia rivolta verso il basso, a z = 0 (il perno ha in più il sotto del dente, sbalzo di 0,25 mm). Sotto la tasca restano 2,5 mm (fiore) e 1,5 mm (segnalini e rotelle). Il vassoio ha il fondo pieno: sotto la tasca della carta 2,7 mm, sotto l'alloggio 1,2 mm, **0,8 mm sotto i numeri incisi** (misurato sul 3MF: facce rivolte in su a z = 0,8 / 1,2 / 2,7 / 3,2; prima l'incisione era 0,5 mm e sotto i numeri restavano 0,7 mm). Gli incavi delle code sono tacche aperte sul bordo del taglio.
- **Tasche dei segnalini misurate sull'STL** (vertici della faccia di sopra): tessera Ø 22,3, segnalino Ø 18,3, Stato 24,3 × 16,3, rotella Ø 50,3; con gli adesivi di `segnalini_3d.pdf` il gioco misurato è 0,249-0,252 mm per lato (atteso 0,25).
- **Perno montato** (`verifica_perno.solidcraft`, plancia da 0,3): 0 intersezioni; gioco fusto-foro della rotella **0,20 mm**, gola-sede del fermo **0,05 mm**, dente-fermo **0,15 mm** in altezza (raggi e assi dei cilindri). Alzando il fermo all'altezza del dente le ganasce lo urtano (0,27 mm³): il dente tiene. Ogni ganascia si apre di 0,20 mm quando passa il dente: deformazione alla radice ≈ 1,7 % (PLA: ~3 % al limite elastico).
- **Parete minima**: la coda ha un collo da 2,3 mm. Il ponte sopra l'incavo è largo al massimo 4,3 mm.

## Stampa (FDM, ugello 0,4)

- **Materiale:** PLA, strato 0,2 mm, 3 perimetri, 4 strati sopra e sotto, riempimento 15-20 %. Non servono supporti.
- **Piatto:** ho ipotizzato un piatto da **220 × 220 mm**. Ogni parte del vassoio, 174,4 × 144,9 al massimo, entra anche in uno da 180 × 180.
- **Vassoio:**
  - si stampa col fondo sul piatto;
  - l'incavo delle code è aperto sotto, con un ponte di 4,3 mm al massimo sopra;
  - attiva la compensazione del «piede d'elefante» (0,1-0,15 mm).
- **Fiori:** si stampano su una faccia qualsiasi. In un piatto da 220 ne entrano 4 in fila (2 × 2) e fino a 6 se lo slicer li incastra tra loro: per 14 fiori servono 3-4 piatti.
- **Segnalini, tessere, Stati e rotelle:** con la tasca in alto.
- **Perni:** in piedi sulla testa, senza supporti (il dente sporge di 0,25 mm). **Fermi:** piatti; le fessure da 0,7 mm devono restare aperte (se si chiudono, ugello 0,4 e niente «ironing»).
- **Prima prova del perno:** stampa 2 perni, 2 fermi e una rotella. Se il fermo non scatta o si spezza porta `collo_d` a 3,0 (ganasce che si aprono di meno); se scatta ma il dente non tiene porta `collo_d` a 2,8. Se la rotella gira dura porta `gioco_assiale` a 0,25.
- **Montaggio del vassoio** (la coda sta sempre sulla parte posata prima):
  1. posa NO;
  2. cala NE e SO dall'alto, con i loro incavi sulle code di NO;
  3. cala SE per ultima.
- **Prima prova:**
  - stampa un fiore e una sola parte del vassoio;
  - se il fiore entra duro porta `gioco_fiore` a 0,25, se balla a 0,15;
  - per le code fai lo stesso con `gioco`;
  - poi rilancia lo script.

## Che cosa faceva Blender e qui non c'è più

La pipeline Blender (`v7/stampa/3d/`, tolta il 12/11) faceva:
- tessere singole a incastro (a pomello, girate di 0, 120 o 240°);
- muri a pioli con i loro fori;
- una prova 3 × 3 montata;
- un piatto di stampa con 20 tessere e 8 muri.

Nella mappa 12×12 i muri non ci sono più, e tessere e prova 3 × 3 sono sostituite dal vassoio e dai fiori. Il piatto di stampa già composto non c'è: i pezzi si dispongono nello slicer.
