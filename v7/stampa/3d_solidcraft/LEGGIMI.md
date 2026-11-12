# Mappa 12×12 in 3D con SolidCraft (12/11)

Daniele ha deciso che i pezzi 3D si fanno con **SolidCraft**, non più con Blender. La vecchia pipeline Blender (tessere singole con muri, D23) è stata tolta.

La mappa è quella a fiori 12×12. Le posizioni vengono da `v7/stampa/sorgenti/dati/base12.csv`: spazi 1-14, posizioni 0-6, esagoni di bordo. Le carte vengono dal kit: `playtest_v7/mappa_base.pdf` e `mappa_fiori.pdf`.

## Pezzi

| Pezzo | Quanti | Ingombro (mm) | PLA |
|---|---|---|---|
| `vassoio_NO`, `vassoio_NE`, `vassoio_SO`, `vassoio_SE` | 1 per tipo | 174,4 × 144,9 × 3,2 al massimo, code comprese | 49-56 g l'uno, 210 g in tutto |
| `fiore` | 14 | 75,2 × 72,3 × 3 | 9,6 g |
| `segnaposto_domanda` («?») | 24 | Ø 22,2 × 2 | 0,7 g |
| `segnalino_cripta` | 1 | 27,4 × 31,6 × 2 (esagono) | 1,2 g |

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
- **Segnaposto «?»** e **segnalino Cripta**:
  - hanno la tasca sopra per le carte del foglio 3 di `mappa_fiori.pdf` («?» Ø 20, Cripta esagono da 25,2);
  - le due facce di quelle carte sono uguali, quindi basta una tasca.
  - La Cripta sporge di 1,1 mm per lato oltre l'esagono della mappa: è un segnalino che si appoggia sopra.

## Perché un vassoio e non pezzi a incastro

Prima ho fatto e controllato pezzi a incastro, con una coda e un incavo su ogni lato, che funzionavano in qualunque rotazione. Il vassoio però è migliore:
- i fiori si voltano, e un incastro che regge anche voltato complicherebbe tutti i pezzi;
- gli spazi tengono i fiori al loro posto;
- i fiori si prendono e si rimettono facilmente durante il draft;
- l'unico incastro rimasto è quello tra le 4 parti del vassoio, che serve solo per il piatto della stampante.

## Carta

- **Base**: `mappa_base.pdf` così com'è, 2 metà da 326 × 280,2 mm in tutto.
  - Si taglia sulla linea esterna e sulla giunzione.
  - Poi si ritagliano i 14 spazi lungo il contorno d'ottone. Se proprio si sbaglia, meglio un filo dentro lo spazio.
  - La carta si posa nella tasca del vassoio montato. La tasca misura 326,5 × 280,7, con 0,25 mm di gioco per lato, ed è profonda 0,5.
  - Non si incolla: le due metà passano sopra i tagli del vassoio, che così resta smontabile.
- **Fiori**: `out/carta_fiori_3d.pdf`, 5 fogli A4, **solo fronte**, 28 facce, una per pezzo.
  - La **linea di taglio è 1,3 mm dentro il contorno ideale**: 0,2 di gioco del fiore, 0,85 di bordino e 0,25 di gioco della carta.
  - La faccia tagliata misura 73,0 × 69,7 mm.
  - La freccia d'ottone e l'id piccolo sono spostati dentro la linea di taglio.
  - Si incolla una faccia nella tasca sopra del fiore 3D. Per avere anche le facce B servono altri 14 fiori 3D.
  - Il PDF usa il disegno di `sorgenti/componenti_gen/fiori12.py`: vettoriale, oppure l'arte generata `sorgenti/arte/png/MF-<NN><A|B>.png` se c'è (`GOBLIN_ARTE_MAPPA=CARTELLA` per un'altra cartella). Senza arte `mappa_fiori.pdf` e `carta_fiori_3d.pdf` restano uguali.
- **«?» e Cripta**: le carte di `mappa_fiori.pdf`, foglio 3, tagliate sulla loro linea. Tasca Ø 20,5 per il «?» ed esagono da 25,7 per la Cripta, profonde 0,5.

## File

Sono tutti in `out/`:
- `*.solidcraft`: **documenti parametrici**. Ogni coordinata è un'espressione dei parametri. In SolidCraft, nella tabella dei parametri, se ne cambia uno e il pezzo si ricostruisce. L'ho provato su un vassoio con `passo` 26, `margine` 9, `gioco` 0,25 e `fondo` 1,6, e sul «?» con carta da 24: nessun errore.
- **`mappa_completa.3mf`: il file da stampare.** Contiene tutti i pezzi nella quantità giusta (4 quarti, 14 fiori, 24 «?», 1 Cripta) su 9 piatti da 220 × 220 affiancati lungo X ogni 230 mm: 1 quarto per piatto (1-4), 4 + 4 + 4 + 2 fiori (5-8), «?» e Cripta (9). I pezzi distano almeno 5 mm e stanno tutti a z = 0. Un oggetto per tipo di pezzo, un'istanza per copia, nomi «Piatto N · pezzo». È un 3MF standard, senza i metadati di piatto di Bambu Studio / OrcaSlicer: nello slicer si separano i piatti a mano o si usa «disponi». Lo rifà anche `genera_3d_solidcraft.py --solo-3mf`, dagli STL già in `out/`.
- `*.stl`: un pezzo per file, in mm. Le parti del vassoio sono nella loro posizione sulla mappa, con l'origine al centro della mappa: lo slicer le porta al centro del piatto.
- `*.png`: le anteprime. `verifica_vassoio_fiori*.png` mostra il vassoio montato con i 14 fiori.
- `verifica_vassoio_fiori.solidcraft`: la prova di montaggio. I fiori sono girati di (spazio mod 6) × 60°.
- `carta_fiori_3d.pdf`: le facce dei fiori per la versione 3D.
- `risultati.json`: tutte le misure.

## Come si rigenera

```
python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py
```

Ci vogliono circa 75 s. Servono:
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
| `carta_domanda` | 20 | diametro della carta «?» |
| `segnalino_spessore` | 2 | spessore di «?» e Cripta |
| `smusso` | 0,4 | smusso degli spigoli di fiore e segnalini |
| `raggio_angolo` | 3 | angoli esterni del vassoio |
| `coda_collo`, `coda_testa`, `coda_lunga` | 2,6 / 4 / 3,9 | coda a pomello tra le parti, come nella versione Blender |
| `numero_alto`, `cifra_alta`, `incisione` | 8 / 4 / 0,5 | numeri incisi sul fondo |

## Controlli (ultimo giro)

- **Volumi**: in SolidCraft sono uguali a quelli calcolati, con un errore relativo tra 1e-13 e 1e-7. Gli ingombri coincidono. STL chiusi (0 lati aperti). Ogni 3MF è in mm, con un oggetto.
- **Vassoio montato con i 14 fiori**: 0 intersezioni (`inspect.interference`). Giochi misurati faccia contro faccia, lato per lato:
  - tra le parti del vassoio: **0,30 mm** su 45 tagli;
  - tra coda e incavo: **0,30 mm** su 45 code. Qui contano raggi e assi dei cilindri, perché la distanza tra facce curve SolidCraft la misura sulla mesh e darebbe 0,284;
  - tra due fiori vicini: **0,40 mm** su 81 lati, con i fiori girati di 0-300°;
  - tra fiore e parete dell'alloggio: **0,20 mm** su 86 lati. Su 4 lati la parete cade su un taglio del vassoio, che la arretra di 0,15 mm, e il gioco è 0,35 mm.
- **Presa delle code**: tirando una parte di 0,6 mm le code urtano (3,6-4,1 mm³ di intersezione; 0,2 mm³ tra NO e SE, che hanno un solo lato in comune). Il gioco a trazione è 0,30-0,33 mm.
- **Fondo piatto**: fiore, «?» e Cripta hanno una sola faccia rivolta verso il basso, a z = 0. Sotto la tasca restano 2,5 mm (fiore) e 1,5 mm (segnalini). Il vassoio ha il fondo pieno: sotto la tasca della carta 2,7 mm, sotto l'alloggio 1,2 mm (0,7 sotto i numeri incisi). Gli incavi delle code sono tacche aperte sul bordo del taglio.
- **Parete minima**: la coda ha un collo da 2,3 mm. Il ponte sopra l'incavo è largo al massimo 4,3 mm.

## Stampa (FDM, ugello 0,4)

- **Materiale:** PLA, strato 0,2 mm, 3 perimetri, 4 strati sopra e sotto, riempimento 15-20 %. Non servono supporti.
- **Piatto:** ho ipotizzato un piatto da **220 × 220 mm**. Ogni parte del vassoio, 174,4 × 144,9 al massimo, entra anche in uno da 180 × 180.
- **Vassoio:**
  - si stampa col fondo sul piatto;
  - l'incavo delle code è aperto sotto, con un ponte di 4,3 mm al massimo sopra;
  - attiva la compensazione del «piede d'elefante» (0,1-0,15 mm).
- **Fiori:** si stampano su una faccia qualsiasi. In un piatto da 220 ne entrano 4 in fila (2 × 2) e fino a 6 se lo slicer li incastra tra loro: per 14 fiori servono 3-4 piatti.
- **Segnalini:** con la tasca in alto. I 24 «?» e la Cripta stanno in un piatto.
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
