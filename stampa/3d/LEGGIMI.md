# Il Tesoro del Goblin — materiali da stampare in 3D

Al posto di comprarli puoi stampare in 3D i cubetti, i dadi e un contenitore che sostituisce il sacchetto
delle 36 Tessere Esplorazione. Tutti i pezzi entrano in un piano da **180 × 180 mm** e si stampano **senza supporti**.

## Cartelle

- `sorgenti/` — file SolidCraft parametrici (`cubetto.solidcraft`, `dado.solidcraft`, `contenitore.solidcraft` con bicchiere e coperchio).
- `stl/` — un STL per ogni tipo di pezzo (mm, già orientato per la stampa).
- `piatti/` — piatti 3MF pronti, raggruppati per colore del filamento (pezzi a ≥ 5 mm di distanza, centrati su un piano 180 × 180).

## Stampa notturna su 2 stampanti (tutto in 2 file)

| File | Contenuto | Piano minimo | Tempo stimato* |
|---|---|---|---|
| `piatti/stampante1_cubetti_pedine.3mf` | 61 pezzi: 57 cubetti (32 Durata + 24 statistiche + 1 boss), 4 pedine (i dadi non si stampano: si usano dadi comprati) | 180 × 180 mm | ~2-3 h |
| `piatti/stampante2_contenitore.3mf` | bicchiere + coperchio, in diagonale (14,8 mm di spazio tra i due) | 180 × 180 mm | ~6 h |

- **Un solo filamento** per stampante. Su una stampante monocolore stampa il piatto 1 in bianco, poi colora i cubetti delle statistiche e il cubetto del boss con pennarelli indelebili o colore acrilico. Gli oggetti hanno il nome del colore previsto (`cubetto_rosso_PV`, `cubetto_nero_PVmax`, `cubetto_arancio_ATT`, `cubetto_verde_MOV`, `cubetto_blu_AR`, `cubetto_viola_PE`, `cubetto_giallo_boss`, 4 per colore): con un sistema multicolore (AMS/MMU) puoi assegnare il colore a ogni oggetto nello slicer.
- Riempimento: nello slicer imposta 100 % (o 4 perimetri) per cubetti e dadi; per pedine e contenitore va bene il 15 %. Se lo slicer non permette impostazioni per oggetto, usa 4 perimetri e il 20 % per tutto il piatto 1.
- I file sono stati scritti dallo script dagli STL di `stl/` (stesse forme dei piatti separati) e non sono ancora stati aperti in uno slicer: aprili, controlla che stiano nel piano e affetta prima di lanciare.

## Pezzi

| Pezzo | Qtà | Misure | Filamento | Piatto | Peso stimato | Tempo stimato* |
|---|---|---|---|---|---|---|
| Cubetto Durata | 32 | 7 × 7 × 7 mm, smusso 0,6 mm | bianco | `piatti/bianco_32_cubetti.3mf` (32 pezzi) | 13 g | 1 h (0,5 h) |
| Cubetto statistica | 24 = 6 colori × 4 | 7 × 7 × 7 mm | 6 colori, uno per statistica | `piatti/colorati_4_cubetti.3mf` (4 pezzi): **stampalo 6 volte**, una per colore | 1,6 g a piatto (10 g in tutto) | 10 min a piatto |
| Cubetto boss | 1 | 7 × 7 × 7 mm | giallo | `piatti/giallo_1_cubetto.3mf` (1 pezzo) | 0,4 g | 5 min |
| Dado D6 | 8 | 16 mm, spigoli raggiati R 1,5, punti incassati Ø 3 × 0,9 mm | a scelta (chiaro, per dipingere i punti) | `piatti/dadi_8.3mf` (8 pezzi) | 38 g (4,8 g l'uno) | 2,5 h (1,2 h) |
| Contenitore: bicchiere | 1 | Ø 90 × 85 mm, interno Ø 86 × 83 mm | a scelta, coprente (non trasparente) | `piatti/contenitore_bicchiere.3mf` | 72 g | 4,5 h (2 h) |
| Contenitore: coperchio | 1 | Ø 94,6 × 32 mm, foro mano Ø 65 mm | stesso del bicchiere | `piatti/contenitore_coperchio.3mf` | 29 g | 2 h (0,8 h) |

Totale circa **165 g** di PLA.

\* Nessuno slicer era installato quando sono stati preparati i file: pesi calcolati dal volume dei modelli
(PLA 1,24 g/cm³, pieni al 100 %; il contenitore ha pareti da 2 mm, quindi anche al 15 % di riempimento è quasi tutto perimetro).
I tempi sono stime grezze (±50 %): stampante tipo Prusa MK3/Ender, tra parentesi una stampante veloce (Bambu, Prusa MK4/Core One).
Lo slicer ti darà i valori veri.

**Colori dei cubetti statistica.** Il regolamento vuole 4 set da 6 cubetti, uno per giocatore, e in ogni set
un colore per statistica: **PV attuali rosso, PV massimi nero**, poi ATT, MOV, AR e PE. Per questi quattro il regolamento
non fissa il colore: per esempio ATT arancione, MOV verde, AR blu, PE viola (meglio non giallo, che è il boss).
Quindi stampa il piatto da 4 cubetti 6 volte, cambiando filamento: alla fine hai 4 cubetti per colore, uno per giocatore.
Il cubetto giallo ha un piatto suo, perché ogni piatto è di un colore solo. Con una stampante multicolore puoi invece aggiungerlo a un altro piatto e assegnargli il giallo.

## Impostazioni di stampa

- PLA, ugello 0,4 mm, strato 0,2 mm, piano liscio o PEI, niente supporti, niente brim (skirt va bene).
- **Cubetti e dadi: riempimento 100 %** (oppure 4 perimetri e 4-5 strati sopra/sotto): stesso peso per tutti, e un dado pieno è equilibrato.
- **Contenitore: riempimento 15 %**, 3 perimetri.
- Compensazione dell'elephant foot attiva se lo slicer ce l'ha (i bordi in basso sono già smussati).

## Orientamento (già giusto negli STL e nei 3MF)

- **Cubetti**: una faccia qualsiasi sul piano.
- **Dadi**: faccia **1** sul piano, **6** in alto. Le facce opposte sommano 7; 1-2-3 attorno allo stesso vertice in senso antiorario, come i dadi occidentali. I punti sui lati sono fori orizzontali di 3 mm profondi 0,9 mm: escono bene senza supporti.
- **Bicchiere**: fondo sul piano, apertura in alto.
- **Coperchio**: si stampa **capovolto**, col piano forato sul piatto e gonna e collare verso l'alto. Da usare girato: il piano forato sta in alto, la gonna calza sopra il bordo del bicchiere (0,3 mm di gioco per lato) e il collare (Ø 68,2 esterno, lungo 30 mm) pende dentro il bicchiere e copre la vista delle tessere.

## Dopo la stampa

- Dadi (facoltativo): riempi i punti con colore acrilico (pennello fine o stuzzicadenti) e togli il colore in eccesso dalla faccia con un panno umido o carta abrasiva fine (grana 400) quando è asciutto.
- Togli eventuali sbavature del primo strato con un cutter.
- Contenitore: metti dentro le 36 tessere, chiudi, scuoti. Per pescare infila la mano nel foro senza guardare dentro (tieni il contenitore all'altezza del petto). Se il coperchio è troppo lento, aggiungi un giro di nastro adesivo sul bordo del bicchiere o ristampalo con `gioco = 0.2 mm`.

## Prova di misura (cubetto nella casella)

Le caselle delle statistiche (ATT, MOV, AR, PE) sulla scheda eroe stampata al 100 % sono quadrati di **9,0 mm**
(22 unità × scala 0,4111 nel file `stampa/sorgenti/schede_eroe/pagina_01.svg`). Il cubetto da **7 mm** ci sta con
**1,0 mm di margine per lato**. Le caselle PV del boss sulla plancia sono di 14,1 mm: c'è spazio in abbondanza.

Attenzione: le caselle della fila **PV** della scheda eroe sono strette, **4,3 × 9,0 mm** (passo 4,7 mm): lì nessun
cubetto ci sta dentro. Il cubetto da 7 mm va messo **centrato sulla casella** e copre anche metà delle vicine; quando
PV attuali e PV massimi coincidono, il cubetto rosso va sopra il nero.

Prima di stampare tutti i 32 cubetti bianchi, stampa il piatto giallo (1 cubetto) e appoggialo su una casella
ATT della scheda stampata: deve starci dentro con un po' d'aria tutto attorno.

## Pedine (4 classi)

Quattro pedine generiche, una per classe, tutte con base tonda **Ø 20 mm × 3 mm** (smusso 0,5 mm sotto, quindi entrano nell'esagono da 25,2 mm della plancia con 2,6 mm di margine per lato) e altezza **30 mm**. Si stampano in piedi, senza supporti.

| Classe | Forma | Colore filamento | Volume | PLA (1,24 g/cm³) |
|---|---|---|---|---|
| Assaltatore | pedone classico con testa a sfera (collo Ø 6,4 mm) | rosso `#9c2f24` | 2205 mm³ | ≈ 2,7 g |
| Stregone | cono alto (Ø 13 mm alla base, Ø 4 mm in punta) | viola `#5b4a9c` | 2610 mm³ | ≈ 3,2 g |
| Ricercatore | cilindro Ø 10 mm con cima tagliata inclinata | verde `#3b7d4f` | 2859 mm³ | ≈ 3,5 g |
| Oracolo | torre a prisma esagonale (Ø 11 mm tra gli spigoli) | oro `#b8862b` | 3057 mm³ | ≈ 3,8 g |

File: `stl/pedina_<classe>.stl` (una per file, centrata sull'origine) e `piatti/pedine_4.3mf` (le 4 pedine insieme su un piatto 180 × 180, centrate, distanza tra le basi 10 mm). Totale circa 13,3 g e 1,5-2 h di stampa (0,2 mm, 15 % riempimento; stima, non misurata). Colori: usa quello della classe, oppure un colore per giocatore se due giocatori hanno la stessa classe. Sezione minima 4 mm (punta dello Stregone; collo dell'Assaltatore 6,4 mm).

## Modificare i pezzi

Apri il file in `sorgenti/` con SolidCraft e cambia i parametri (il modello si ricostruisce):

- `cubetto.solidcraft`: `lato` (7 mm), `smusso` (0,6 mm).
- `dado.solidcraft`: `lato` (16 mm), `raggio` (1,5 mm), `pip_d` (3 mm), `pip_p` (0,9 mm), `pip_off` (= lato × 0,27).
- `pedine.solidcraft`: `base_d` (20 mm), `h` (30 mm), `base_h` (3 mm), `ch` (0,5 mm); le 4 pedine sono corpi separati.
- `contenitore.solidcraft`: `d_int` (86 mm), `parete` (2 mm), `fondo` (2 mm), `h_cup` (85 mm), `gioco` (0,3 mm), `h_gonna` (10 mm), `piano` (2 mm), `foro_mano` (65 mm), `spess_collare` (1,6 mm), `h_collare` (30 mm), `smusso_base` (1 mm).

Poi esporta di nuovo l'STL (File → Esporta) e rifai il piatto nello slicer.

## Controlli fatti

- Volumi misurati in SolidCraft uguali a quelli calcolati a mano: cubetto 329,18 mm³, dado 3874,2 mm³, bicchiere 58 469 mm³, coperchio 23 133 mm³.
- Tutti gli STL sono chiusi (ogni spigolo condiviso da 2 triangoli, orientamento coerente).
- Capienza: 36 tessere Ø 24 × 2 mm occupano 32,6 cm³; il bicchiere ha 482 cm³ interni (307 cm³ sotto il collare): circa 9 volte la pila, quindi si mescolano bene.
