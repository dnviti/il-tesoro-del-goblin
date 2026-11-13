# Mappa 12×12, segnalini e rotelle in 3D con SolidCraft (12-13/11)

Daniele ha deciso che i pezzi 3D si fanno con **SolidCraft**, non più con Blender. La vecchia pipeline Blender (tessere singole con muri, D23) è stata tolta.

La mappa è quella a fiori 12×12. Le posizioni vengono da `v7/stampa/sorgenti/dati/base12.csv`: spazi 1-14, posizioni 0-6, esagoni di bordo. Le carte vengono dal kit: `playtest_v7/mappa_base.pdf` e `mappa_fiori.pdf`.

Dal 13/11 (D29: i 24 segnaposto «?» non ci sono più) sono in 3D anche **tutti i segnalini e le tessere del kit e le rotelle**, con gli adesivi in `playtest_v7/segnalini_3d.pdf`. Le quantità vengono dai CSV del kit (`tessere_esplorazione.csv`, `segnalini.csv`, `stati.csv`) e dalle rotelle di `gen.py`.

## Pezzi

| Pezzo | Quanti | Ingombro (mm) | PLA |
|---|---|---|---|
| `vassoio_NO`, `vassoio_NE`, `vassoio_SO`, `vassoio_SE` | 1 per tipo | 174,4 × 144,9 × 3,2 al massimo, code comprese | 49-56 g l'uno, 210 g in tutto |
| `fiore` | 14 | 75,2 × 72,3 × 1,5 | 7,0 g |
| `segnalino_cripta` | 1 | 25,6 × 29,6 × 2 (esagono) | 1,4 g |
| `tessera_esplorazione` | 36 | Ø 24 × 2 | 1,1 g |
| `segnalino_tondo` (oggetti `segnalino_indizio`, `segnalino_forte_volonta`, `segnalino_usato`) | 16 + 4 + 20 | Ø 20 × 2 | 0,8 g |
| `tessera_stato` | 31 | 26 × 18 × 2 | 1,1 g |
| `rotella_tacca_11x9` (oggetti `rotella_PV`, `_ATT`, `_MOV`, `_AR`, `_scontro`, `_custode`) | 4 + 4 + 4 + 4 + 1 + 1 | Ø 52 × 2 (51,4 in y: la tacca) | 4,9 g |
| `rotella_tacca_9x9` (oggetti `rotella_Danni`, `rotella_PL`) | 4 + 4 | Ø 52 × 2 | 4,9 g |
| `rotella_tacca_10x9` (oggetto `rotella_Profezia`) | 1 | Ø 52 × 2 | 4,9 g |
| `rivetto_maschio` | 27 | Ø 10 × 5,45 | 0,17 g |
| `rivetto_femmina` | 27 | Ø 10 × 4,15 | 0,18 g |

- **Vassoio**: montato misura 329 × 283 mm.
  - Ha un fondo da 1,2 mm.
  - Ha un **alloggio unico per i 14 fiori**, profondo 2 mm.
  - Sopra ha una **tasca per la carta della base**: è `mappa_base.pdf` con le coordinate, ritagliata lungo il contorno d'ottone degli spazi.
  - Sul fondo dell'alloggio sono **incisi il numero di ogni spazio e le cifre 1-6 dell'anello**, come sulla carta della base, che lì viene tolta. Servono per la freccia dei preset.
  - Le 4 parti si uniscono con **code a pomello** nel fondo, lungo i lati degli esagoni. Una coda per lato del taglio: 23 tra NO e le altre, 11 tra NE e SE, 11 tra SO e SE.
- **Pezzi lisci sopra** (Daniele, 13/11 21:28: supera la regola «bordino + tasca sopra»): fiori, tessere, Stati, segnalini, Cripta e rotelle hanno la **faccia di sopra liscia fino al bordo**, senza bordino, senza tasca e senza smusso; l'adesivo si incolla sopra ed è **0,2 mm più piccolo per lato** (`margine_adesivo`, tolleranza di incollaggio). Sotto: fondo piatto con smusso di 0,4. Solo il vassoio ha ancora la tasca per la carta.
- **Fiore**: rosetta **senza incastri**, spessa **1,5 mm = `alloggio_prof` − `tasca_prof`**: posato sul fondo dell'alloggio (z = 1,2) ha il sopra a z = 2,7, **la stessa quota del fondo della tasca della carta della base**. Con la faccia del fiore e la carta della base dello stesso cartoncino, la mappa stampata è in piano. Gioco laterale 0,2 per lato, nessun gioco in altezza (il fiore appoggia sul fondo).
  - Porta una sola faccia (sopra). Entra in qualsiasi spazio, girato di 60° in 60°.
  - Si prende spingendo su un lato o capovolgendo il vassoio: non sporge più.
- **Segnalino Cripta**: esagono da 25,6 da lato a lato, liscio sopra; si incolla sopra la carta esagonale da 25,2 (`mappa_fiori.pdf`, foglio 3, o `segnalini_3d.pdf`). Sporge 0,2 per lato oltre l'esagono della mappa.
- **Segnalini del kit in 3D** (tessere Esplorazione, Indizio, Forte Volontà, Usato, tessere Stato, dischi delle rotelle):
  - il **contorno è esattamente quello del pezzo di carta** (Ø 24, Ø 20, 26 × 18 con angoli da 1,2, Ø 52), così il pezzo 3D sta negli stessi posti della carta: esagono della mappa, cerchi Ø 22 e riquadri degli Stati della plancia, corone delle rotelle;
  - adesivi: Ø 23,6, Ø 19,6, 25,6 × 17,6, corona Ø 51,6;
  - la **tessera Stato è rettangolare** come la carta: si vede se è verticale o orizzontale;
  - la **tessera Esplorazione** porta il fronte sopra e il **dorso incollato sul fondo piatto** (adesivo Ø 23,6: sul fondo sporge 0,2 mm sullo smusso di 0,4, quindi va incollato bene al centro): coperta mostra il dorso;
  - la **rotella è il disco di sopra, come in Unmatched** (Daniele, 14/11 00:01): la plancia eroe (o la base di carta di scontro, custode e Profezia) è il disco di sotto, coi valori stampati sulla corona a 20 mm dal centro. La rotella ha la **tacca aperta sul bordo**, in alto: larga quanto la finestra del disco di carta + 0,25 per lato (11,5 / 9,5 / 10,5), dal bordo fino a 15,25 mm dal centro (finestra di carta 9 mm alta centrata a 20 mm, meno 0,25). Nella tacca si legge un solo valore della corona: `gen.py` lo controlla con `verifica_rotella(..., tacca=True)` (stessi margini della finestra di carta: 0,77-1,9 mm sull'etichetta, 0,89-6,04 mm dai vicini). Al centro il **foro Ø 6,4** della manica del rivetto. L'adesivo è una corona con il foro Ø 13 (lì la testa della femmina appoggia sulla plastica) e l'intaglio della tacca, largo come la finestra di carta (copre di 0,25 il bordo della plastica).
- **Rivetto della rotella** in 2 pezzi a pressione, come quello nero di Unmatched (uno per rotella, 27 + 27):
  - **maschio**: testa a **cupola bassa Ø 10 × 2** col sotto piatto, **sotto la plancia**; **gambo** Ø 3,0 lungo 3,45 con la punta smussata e **4 costole di schiacciamento** (larghe 0,6, sporgono 0,25: Ø 3,5 sulle costole, passa nel foro Ø 4 della plancia con 0,25 per lato), che finiscono 0,6 sotto la punta;
  - **femmina**: la stessa testa, **sopra la rotella**, con la **manica** Ø 6,0 lunga 2,15 (= rotella 2,0 + gioco_assiale 0,15) e il **foro cieco** Ø 3,2 profondo 3,55 con l'invito a 45° di 0,3. La rotella gira sulla manica (0,2 per lato) e ha 0,15 in altezza sotto la testa;
  - **presa**: le costole entrano nel foro con **0,15 mm di interferenza** per costola (il gambo tra le costole ha 0,1 per lato): pressione e attrito, come in Unmatched. La manica poggia sulla plancia, quindi il gioco della rotella non dipende dallo spessore della plancia: con 0,1-0,45 mm cambia solo quanto entra il gambo (costole nel foro 2,75-2,4 mm, punta 0,2-0,55 sotto il fondo del foro);
  - **stampa**: tutti e due con la cima della cupola sul piatto (cima piatta Ø 6,4, poi la cupola sale a 45° e più ripida verso il bordo): niente supporti, niente sbalzi;
  - **montaggio**: maschio dal retro nel foro Ø 4, rotella sopra la corona, femmina dal davanti sul gambo, premi le due teste tra pollice e indice finché la manica tocca la plancia. Si smonta tirando le teste (le costole si schiacciano: dopo molti smontaggi il rivetto tiene meno).

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
  - La **linea di taglio è 0,4 mm dentro il contorno ideale**: 0,2 di gioco del fiore e 0,2 di `margine_adesivo`.
  - La freccia d'ottone e l'id piccolo sono spostati dentro la linea di taglio.
  - Si incolla una faccia sopra il fiore 3D (liscio). Per avere anche le facce B servono altri 14 fiori 3D.
  - Il PDF usa il disegno di `sorgenti/componenti_gen/fiori12.py`: vettoriale, oppure l'arte generata `sorgenti/arte/png/MF-<NN><A|B>.png` se c'è (`GOBLIN_ARTE_MAPPA=CARTELLA` per un'altra cartella). Senza arte `mappa_fiori.pdf` e `carta_fiori_3d.pdf` restano uguali.
- **Cripta**: la carta di `mappa_fiori.pdf`, foglio 3 (anche in `segnalini_3d.pdf`), tagliata sulla sua linea (25,2) e incollata sopra il segnalino 3D da 25,6.
- **Adesivi dei segnalini e delle rotelle**: `playtest_v7/segnalini_3d.pdf`, 9 fogli A4 solo fronte, ognuno col segmento di controllo di 100 mm. Lo genera `gen.py segnalini_3d()` dentro `build.sh` (misure lette da questo script, `G3.P`). Ogni adesivo è il contorno del pezzo 3D meno `margine_adesivo` (0,2) per lato. **Indizi, Forte Volontà, Usato, Stati e Cripta sono a doppia faccia** (Daniele 13/11 22:36): un adesivo sopra e uno uguale sul fondo piatto (Stati con la stessa orientazione):
  1. fronti delle 36 Tessere Esplorazione (Ø 23,6) e la carta della Cripta (sopra);
  2. dorsi delle 36 tessere (Ø 23,6, da incollare sul fondo piatto) e la Cripta per il fondo;
  3. 31 tessere Stato (25,6 × 17,6), sopra;
  4. le stesse 31 tessere Stato per il fondo;
  5. 40 segnalini tondi (Ø 19,6: 16 Indizio, 4 Forte Volontà, 20 Usato), sopra;
  6. gli stessi 40 segnalini per il fondo;
  7. e 8. le 6 rotelle di 2 plance per foglio (PV, Danni, ATT, MOV, AR, PL), corone Ø 51,6 col foro Ø 13 e l'intaglio della tacca;
  9. rotelle dello scontro, del custode e della Profezia.
  - L'arte è quella dei pezzi di carta: tessere e segnalini in scala uniforme (0,983 e 0,98), Stati in scala 25,6/26 × 17,6/18, rotelle in scala 1 (la tacca deve stare sulla corona della plancia) tagliate sulla corona dell'adesivo.
  - **Controllo**: `python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py --verifica-adesivi playtest_v7/segnalini_3d.pdf` legge ogni linea di taglio (tratto da 0,2 mm) dal PDF, la confronta con l'adesivo atteso (scarto di Hausdorff), misura il margine per lato verso il contorno del pezzo (atteso 0,2), conta gli adesivi per tipo e misura a 600 dpi il segmento di 100 mm di ogni foglio. Esce con errore oltre 0,2 mm o con conteggi sbagliati.
- **Plancia eroe e basi delle rotelle** (svg.py `dial_ring`): sono il **disco di sotto** del quadrante, coi valori sulla corona; al centro di ogni corona c'è il cerchio **Ø 4** del foro per il rivetto 3D (col punteruolo al centro resta buono per il fermacampioni). Il foro Ø 4 si fa con una fustella da pelle o un punteruolo largo; la testa Ø 10 del maschio lo copre da dietro, la manica Ø 6 della femmina poggia sul bordo da davanti.

## File

Sono tutti in `out/`:
- `*.solidcraft`: **documenti parametrici**. Ogni coordinata è un'espressione dei parametri. In SolidCraft, nella tabella dei parametri, se ne cambia uno e il pezzo si ricostruisce. L'ho provato su un vassoio con `passo` 26, `margine` 9, `gioco` 0,25 e `fondo` 1,6: nessun errore. Segnalini, rotelle e rivetti usano gli stessi parametri (`tessera_d`, `gettone_d`, `stato_l`, `rotella_d`, `testa_d`, `gambo_d`...).
- **I file da stampare: 4 file 3MF, uno per tipo di pezzo** (Daniele, 13/11 18:18; il vecchio `mappa_completa.3mf` non c'è più). Ognuno ha i suoi piatti da 220 × 220, affiancati lungo X ogni 230 mm:

  | File | Pezzi | Piatti |
  |---|---|---|
  | `mappa.3mf` | 4 quarti del vassoio + 14 fiori | 8: un quarto per piatto (1-4), fiori 4 + 4 + 4 + 2 (5-8) |
  | `rotelle_rivetti.3mf` | 27 rotelle (4 × PV, Danni, ATT, MOV, AR, PL; scontro, custode, Profezia) + 27 rivetti maschio + 27 femmina | 4 |
  | `segnalini.3mf` | 31 tessere Stato, 16 Indizi, 4 Forte Volontà, 20 Usato, 1 Cripta | 2 |
  | `tessere_esplorazione.3mf` | 36 Tessere Esplorazione | 1 |

  I pezzi distano almeno 5 mm tra loro e dal bordo e stanno tutti a z = 0. Un oggetto per nome (lo stesso STL può dare più oggetti: `rotella_PV`, `rotella_ATT`, `segnalino_indizio`... per assegnare i colori), un'istanza per copia, nomi «Piatto N · oggetto»; lo script rilegge ogni file e ricontrolla le quantità. Sono 3MF standard, senza i metadati di piatto di Bambu Studio / OrcaSlicer: nello slicer si separano i piatti a mano o si usa «disponi». Li rifà anche `genera_3d_solidcraft.py --solo-3mf`, dagli STL già in `out/`.
- `*.stl`: un pezzo per file, in mm. Le parti del vassoio sono nella loro posizione sulla mappa, con l'origine al centro della mappa: lo slicer le porta al centro del piatto.
- `*.png`: le anteprime. `verifica_vassoio_fiori*.png` mostra il vassoio montato con i 14 fiori; `verifica_rivetto_sezione.png` la sezione di rivetto (nero), plancia, rotella montati; `verifica_rivetto.png` la vista.
- **Render con le texture della carta** (13/11, `render_3d.py`): `render_montata.png` (vassoio, 14 fiori del preset «Strettoie», 4 tessere coperte, una scoperta e la Cripta), `render_montata_alto.png` (la stessa, dall'alto, nord in alto), `render_esplosa.png` (quarti aperti, fiori alzati), `render_plancia.png` (plancia eroe 1 con le 6 rotelle 3D ai valori di partenza, letti nella tacca, e i rivetti), `render_segnalini.png` (tessere, Stati, segnalini, Cripta, rotella dello scontro) e `piatto_segnalini.png` (piatto 1 di `segnalini.3mf`).
- `verifica_rivetto.solidcraft`: la prova di montaggio del rivetto (plancia da 0,3 col foro Ø 4, rotella, maschio, femmina girata).
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

### Render con le texture

```
python3 v7/stampa/3d_solidcraft/render_3d.py [segnalini|piatto|plancia|mappa ...]
```

Da lanciare dopo `genera_3d_solidcraft.py` e la build A4 del kit (usa `playtest_v7/segnalini_3d.pdf`, `carta_base_3d.pdf`, `plance_eroe.pdf` e `out/carta_fiori_3d.pdf`). Circa 2 minuti. Solo SolidCraft: la scena si costruisce con le classi del generatore, ogni corpo riceve una texture «base color» proiettata dall'alto (`render.surface.import`, frame in mm del mondo) e `solidcraft-cli render` fa il ray tracing CPU.
- La texture di un pezzo è grande quanto il suo ingombro: colore del filamento, con l'arte della carta esattamente dove sta la carta. Adesivi ritagliati da `segnalini_3d.pdf` (300 dpi) sulla loro linea di taglio letta dal PDF e centrati sulla faccia di sopra; facce dei fiori da `carta_fiori_3d.pdf`, girate come nel preset (60° × (freccia − 1)); cornice della base dal foglio del quarto di `carta_base_3d.pdf`, con la sua traslazione; plancia da `plance_eroe.pdf`, in 4 pezzi. Carta a faccia in su: niente specchi.
- Le tessere coperte sono capovolte e mostrano il dorso incollato sul fondo piatto.
- **Limiti di SolidCraft** (0.41): al massimo 32 immagini diverse per scena (le copie dello stesso adesivo usano la stessa immagine), 1024 × 1024 px l'una e un tetto di memoria del ray tracing: lo script riduce tutte le texture in proporzione fino a 6 milioni di pixel per scena. Sul vassoio e sui fiori la carta resta a circa 4-5 px/mm: si legge nei render, non negli ingrandimenti. La proiezione è dall'alto: i fianchi dei pezzi prendono il colore del filamento.

I parametri sono in cima a `genera_3d_solidcraft.py` (`PARAMETRI`, in mm): si cambiano lì e si rilancia, così si rifanno anche le prove.

| Parametro | Valore | Che cosa è |
|---|---|---|
| `passo` | 25,2 | esagono da lato a lato, cioè la distanza tra i centri |
| `margine` | 7 | bordo del vassoio oltre la mappa: la carta ha 5,5 di fascia, poi 1,1 mm di bordino |
| `gioco` | 0,15 | gioco per lato tra le parti del vassoio e sulle code (0,3 in tutto) |
| `gioco_fiore` | 0,2 | gioco per lato tra fiore e alloggio (0,4 tra due fiori) |
| `fondo` | 1,2 | fondo del vassoio, che è anche l'altezza delle code |
| `alloggio_prof` | 2 | profondità dell'alloggio dei fiori |
| `fiore_spessore` | 1,5 | spessore del fiore = `alloggio_prof` − `tasca_prof` (lo script lo controlla): sopra del fiore alla quota del fondo della tasca della carta |
| `tasca_prof` | 0,5 | profondità della tasca per la carta della base (solo nel vassoio) |
| `bordino` | 0,85 | bordino del vassoio oltre la tasca della carta della base |
| `gioco_carta` | 0,25 | gioco per lato tra carta e tasca del vassoio, e tra finestra di carta e tacca della rotella |
| `margine_adesivo` | 0,2 | margine per lato tra il contorno dei pezzi lisci e l'adesivo incollato sopra |
| `fascia_carta` | 5,5 | fascia della carta della base (`FASCIA12` del kit) |
| `segnalino_spessore` | 2 | spessore di Cripta, tessere, segnalini e Stati |
| `tessera_d`, `gettone_d` | 24 / 20 | diametro delle Tessere Esplorazione e dei segnalini tondi (come la carta) |
| `stato_l`, `stato_a`, `stato_r` | 26 / 18 / 1,2 | tessera Stato e raggio degli angoli (come la carta) |
| `rotella_d`, `corona_r`, `rotella_spessore` | 52 / 20 / 2 | disco della rotella, distanza dal centro dei valori letti nella tacca, spessore |
| `mozzo_r` | 6,25 | zona al centro della rotella senza adesivo, dove la testa della femmina appoggia sulla plastica |
| `foro_rotella` | 6,4 | foro della rotella: gira sulla manica della femmina (0,2 per lato) |
| `testa_d`, `testa_h` | 10 / 2 | teste a cupola bassa del rivetto (maschio e femmina) |
| `gambo_d`, `costola` | 3,0 / 0,25 | gambo del maschio e sporgenza delle 4 costole (Ø 3,5 sulle costole) |
| `foro_femmina`, `manica_d`, `fondo_femmina` | 3,2 / 6,0 / 0,6 | foro e manica della femmina, fondo del foro sotto la cima della cupola |
| `carta_plancia`, `carta_min` | 0,3 / 0,1 | plancia della prova di montaggio; plancia più sottile (la lunghezza del gambo: 3,45) |
| `gioco_assiale` | 0,15 | aria in altezza per la rotella (manica = rotella + 0,15), con ogni plancia |
| `smusso` | 0,4 | smusso dello spigolo sotto di fiori e segnalini (sopra sono lisci fino al bordo) |
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
- **Fondo piatto e sopra liscio**: fiore, Cripta, tessere, segnalini, Stati, rotelle e i due pezzi del rivetto hanno una sola faccia rivolta verso il basso, a z = 0 (per i rivetti la cima piatta della cupola), e fiore e segnalini una sola faccia rivolta verso l'alto, a z = spessore (controllato sul modello SolidCraft). Il vassoio ha il fondo pieno: sotto la tasca della carta 2,7 mm, sotto l'alloggio 1,2 mm, **0,8 mm sotto i numeri incisi**. Gli incavi delle code sono tacche aperte sul bordo del taglio.
- **Mappa in piano** (misurato sugli STL): facce in su dei quarti a z = 0,8 / 1,2 / 2,7 / 3,2 (numeri incisi, fondo dell'alloggio, fondo della tasca della carta, cornice); fiore spesso 1,5 posato sul fondo dell'alloggio → sopra del fiore a **2,7 = fondo della tasca della carta, differenza 0,000 mm**. Con la faccia del fiore e la carta della base dello stesso cartoncino le due superfici stampate sono alla stessa quota. Sezione: `out/verifica_fiore_cornice_sezione.png` (fiore verde, vassoio marrone).
- **Faccia di sopra misurata sull'STL**: tessera Ø 24, segnalino Ø 20, Stato 26 × 18, rotella Ø 52; con gli adesivi di `segnalini_3d.pdf` il margine misurato è 0,2 mm per lato (atteso 0,2).
- **Rivetto montato** (`verifica_rivetto.solidcraft`; la prova si rifà con la plancia da **0,1, 0,3 e 0,45**): 0 intersezioni tra plancia, rotella, maschio e femmina, tranne la pressione voluta delle costole nel foro della femmina (0,97 / 0,89 / 0,83 mm³, uguale al calcolo); giochi (raggi e assi dei cilindri, facce piane): manica-foro della rotella **0,20 mm**, testa della femmina-rotella **0,15 mm** in altezza con ogni plancia, gambo-foro della femmina tra le costole 0,10 mm, punta del gambo-fondo del foro **0,20 / 0,40 / 0,55 mm**. Costole nel foro per 2,75-2,4 mm.
- **Parete minima**: la coda ha un collo da 2,3 mm. Il ponte sopra l'incavo è largo al massimo 4,3 mm.

## Stampa (FDM, ugello 0,4)

- **Materiale:** PLA, strato 0,2 mm, 3 perimetri, 4 strati sopra e sotto, riempimento 15-20 %. Non servono supporti.
- **Piatto:** ho ipotizzato un piatto da **220 × 220 mm**. Ogni parte del vassoio, 174,4 × 144,9 al massimo, entra anche in uno da 180 × 180.
- **Vassoio:**
  - si stampa col fondo sul piatto;
  - l'incavo delle code è aperto sotto, con un ponte di 4,3 mm al massimo sopra;
  - attiva la compensazione del «piede d'elefante» (0,1-0,15 mm).
- **Fiori:** si stampano su una faccia qualsiasi. In un piatto da 220 ne entrano 4 in fila (2 × 2) e fino a 6 se lo slicer li incastra tra loro: per 14 fiori servono 3-4 piatti.
- **Fiori, segnalini, tessere, Stati e rotelle:** col fondo (smussato) sul piatto, la faccia liscia in alto.
- **Rivetti:** con la cima della cupola sul piatto, gambo o manica in su, senza supporti. Sono piccoli: rallenta lo strato (tempo minimo 8-10 s) o stampali in tanti per piatto.
- **Prima prova del rivetto:** stampa 2 maschi, 2 femmine e una rotella. Se il maschio non entra o la femmina si spacca porta `costola` a 0,2 (o `foro_femmina` a 3,25); se il rivetto si sfila porta `costola` a 0,3. Se la rotella gira dura porta `foro_rotella` a 6,5 o `gioco_assiale` a 0,25.
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
