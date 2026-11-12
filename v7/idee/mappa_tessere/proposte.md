# Mappa a pezzi grandi: proposte e tempi di montaggio

12/11/2026 · richiesta di Daniele: oggi montare la mappa richiede troppo tempo (100 tile da 25,2 mm più 16 muri). Si vogliono pezzi più grandi, con più zone ciascuno, senza perdere i 10 preset del §17 (base «Strettoie» e TM-01…09, D23). Questo documento contiene solo idee: non cambia regole, carte né kit di stampa.

File in questa cartella:
- `tempo_setup.py`: estrae i preset dai dati veri (`v7/simulatore/mappa.py`, `v7/simulatore/plance/*.py`), conta pezzi e disegni di ogni opzione, controlla le combinazioni libere e calcola i tempi. Si lancia con `python3 v7/idee/mappa_tessere/tempo_setup.py` (con `--dettagli` stampa anche tutte le costanti). Le tabelle qui sotto sono il suo output.
- `disegna_mockup.py`: genera `mockup_fasce_base.png`, `mockup_fasce_miste.png` e `mockup_neutra_toppe.png`, con i loro SVG in scala 1:1.

## In breve

| | Opzione | Pezzi a partita | Disegni | Misura del pezzo | Montaggio (veloce–**tipico**–lento) | Preset |
|---|---|---|---|---|---|---|
| 0 | Oggi: tile singole + muri | 100 + 16 muri | 18 | esagono 25,2 | 7:00–**11:13**–17:57 | tutti, esatti |
| A | Tri-esagoni | 38 + 16 muri | 75 | 50 × 51 | 5:35–**8:40**–13:53 | esatti, ma un puzzle per preset |
| B | Fiori da 7 | 20 + 16 muri | 85 | 76 × 73 | 3:03–**4:50**–7:46 | esatti, ma un puzzle per preset |
| C | Quadranti 5 × 5 | 4 | 20 | 139 × 116 | 0:32–**0:56**–1:41 | tutti, esatti |
| **D** | **Fasce: nord + fiume + sud** | **3** | **12** | **265 × 95 e 265 × 51** | **0:27–0:48–1:27** | **tutti, esatti** |
| E1 | Plancia neutra + le tile di oggi come toppe | 3 + 28 + 6 muri | 2 nuovi | come D | 2:23–**3:54**–6:21 | tutti, esatti |
| E2 | Plancia neutra + toppe sagomate da 1-3 esagoni | 3 + 12-16 + 6 muri | 16 | come D | 1:40–**2:44**–4:30 | tutti, esatti |

I tempi sono per una persona e riguardano solo la mappa. Per tutte le opzioni vanno aggiunti 40–55–80 s per mettere le tessere Esplorazione sulle 20 «?».

**Raccomandazione: D + E1.** I preset si montano con 3 fasce stampate: in tempo tipico 48 s invece di 11 minuti, e il cambio di mappa a metà partita (R 8.12) scende da 3:21 a 0:49. Per la composizione libera restano tre strade: mescolare le fasce (le 100 coppie nord/sud passano tutti i controlli del §17), posare le tile di oggi come toppe su una fascia neutra, oppure usare solo le tile come adesso. In più vanno stampati 12 fogli A4 (o 6 A3) di cartoncino.

## 1. Cosa dicono i 10 preset

| Preset | Esagoni = tile | Strada | Bosco | Case | Rocce | Acqua | Muri | Di cui mura libere | Controlli §17 |
|---|---|---|---|---|---|---|---|---|---|
| base | 100 | 64 | 12 | 6 | 10 | 8 | 16 | 6 | sì |
| TM-01 | 100 | 64 | 12 | 6 | 10 | 8 | 16 | 6 | sì |
| TM-02 | 100 | 64 | 6 | 14 | 8 | 8 | 16 | 6 | sì |
| TM-03 | 100 | 64 | 18 | 2 | 8 | 8 | 16 | 6 | sì |
| TM-04 | 100 | 64 | 8 | 4 | 16 | 8 | 16 | 6 | sì |
| TM-05 | 100 | 64 | 10 | 8 | 10 | 8 | 16 | 6 | sì |
| TM-06 | 100 | 64 | 4 | 6 | 18 | 8 | 16 | 6 | sì |
| TM-07 | 100 | 64 | 14 | 6 | 8 | 8 | 16 | 6 | sì |
| TM-08 | 100 | 64 | 8 | 12 | 8 | 8 | 16 | 6 | sì |
| TM-09 | 100 | 64 | 12 | 6 | 10 | 8 | 16 | 6 | sì |

Ogni preset usa 100 tile (6 Partenze, 4 Cripte, 20 «?», 2 guadi, 2 ponti, 30 di strada semplice, 28 ostacoli di terra e 8 di acqua) e 16 listelli di muro.

**56 esagoni sono uguali in tutti i preset** (Partenze, Cripte con i loro ingressi, 20 «?», tutto il fiume) e **44 cambiano**: 22 nelle righe 1-4, 22 nelle righe 7-10 e **nessuno nelle righe 5-6**. Ecco dove stanno (X = cambia in almeno un preset):

```
·   ·   ·   X   X   X   X   ·   ·   X        riga 1
  ·   X   ·   X   X   X   X   X   ·   ·      riga 2
X   X   X   ·   ·   X   ·   X   X   X        riga 3
  X   X   ·   ·   ·   ·   ·   ·   X   X      riga 4
·   ·   ·   ·   ·   ·   ·   ·   ·   ·        riga 5  (fiume: sempre uguale)
  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·      riga 6  (fiume: sempre uguale)
X   X   ·   ·   ·   ·   ·   ·   X   X        riga 7
  X   X   X   ·   X   ·   ·   X   X   X      riga 8
·   ·   X   X   X   X   X   ·   X   ·        riga 9
  X   ·   ·   X   X   X   X   ·   ·   ·      riga 10
```

Dei muri, 10 sono uguali dappertutto (chiudono le Cripte). Le 6 mura libere di ogni preset occupano in tutto 26 posizioni diverse. Le uniche mura libere dentro le righe 5-6 sono C6|D6 e G5|H5: ci sono in 9 preset su 10 e mancano solo in TM-08 Flegias.

Esagoni da cambiare per passare dalla base a una Mappa (R 8.12):

| base → | Esagoni diversi | Strada → ostacolo | Ostacolo → strada | Ostacolo → altro ostacolo | Mura da togliere | Mura da mettere |
|---|---|---|---|---|---|---|
| TM-01 | 26 | 6 | 6 | 14 | 4 | 4 |
| TM-02 | 22 | 4 | 4 | 14 | 4 | 4 |
| TM-03 | 28 | 10 | 10 | 8 | 4 | 4 |
| TM-04 | 32 | 8 | 8 | 16 | 4 | 4 |
| TM-05 | 26 | 4 | 4 | 18 | 4 | 4 |
| TM-06 | 34 | 10 | 10 | 14 | 4 | 4 |
| TM-07 | 10 | 4 | 4 | 2 | 2 | 2 |
| TM-08 | 30 | 4 | 4 | 22 | 6 | 6 |
| TM-09 | 34 | 10 | 10 | 14 | 4 | 4 |

Tra due preset qualsiasi cambiano da 10 a 38 esagoni, 29,2 in media.

**Che cosa ne segue.** Le differenze tra i preset stanno tutte in due fasce, nord e sud, e la fascia sud è la nord girata di 180°, perché ogni preset è identico girato. Il fiume in mezzo non cambia mai. Basta un taglio lungo i lati tra le righe 4 e 5 e uno tra le righe 6 e 7 per dividere ogni preset in 3 pezzi, e il pezzo centrale è uguale per tutti.

## 2. Il modello dei tempi

Per ogni pezzo il tempo è la somma di sei passi:

`lettura + ricerca + presa + posa + orientamento + urti`

A questo si aggiungono, per ogni pezzo, il controllo finale e la correzione di un errore ogni tanto, più un tempo fisso (tirare fuori i pezzi, Sala del Tesoro). I valori sono in `COSTANTI` dentro lo script, ciascuno con la sua fonte; questi sono i principali.

| Passo | Veloce / tipico / lento | Da dove viene |
|---|---|---|
| Leggere la prossima casella sul foglio | 0,8 / 1,35 / 2,2 s | Operatore M (atto mentale) del modello KLM, Card, Moran e Newell 1983: 1,35 s |
| Leggere un muro (coppia di coordinate) | 1,5 / 2,2 / 3,5 s | circa 1,5 M: bisogna trovare il lato tra due caselle |
| Trovare la pila giusta tra n pile per tipo | 0,2 + 0,15·log2(n+1) s | Legge di Hick-Hyman (Hick 1952, Hyman 1953), circa 0,15 s/bit |
| Trovare un pezzo «unico» tra n sparsi (tri-esagoni, fiori) | 0,5 s × (n+3)/4 | Ricerca seriale: in media si guarda metà dei pezzi rimasti, 1-2 fissazioni da 0,2-0,35 s per confrontarne uno (Rayner 1998) |
| Prendere una tile da 25 mm piatta sul tavolo | 0,6 / 0,9 / 1,3 s | Ordine di grandezza MTM-1 (raggiungere, afferrare) più la difficoltà del cartoncino piatto: stima |
| Prendere un listello di muro 14,5 × 3 mm | 1,2 / 2,0 / 3,0 s | Va fatto scivolare o pizzicato: stima |
| Portarla e accostarla | 0,2 + 0,15·log2(300/2 + 1) ≈ 1,3 s | Legge di Fitts (MacKenzie 1992): 300 mm di distanza, 2 mm di tolleranza; 1 mm per i muri, 3 mm per una toppa su un esagono già stampato |
| Accostare un pezzo grande lungo il taglio a zig-zag | 2 / 3,5 / 6 s | A due mani: stima |
| Orientare | tile 0,3 s; pezzo da 3-7 esagoni 0,9 s; pezzo grande 0,5 s | Scegliere 1 di 6 rotazioni confrontando col foglio: stima |
| Urti (tile leggere che spostano le vicine) | 0,1 / 0,3 / 0,6 s a tile | Una posa su 10-20 sposta una vicina, 2-3 s per rimetterla: stima |
| Controllo finale | 0,3 / 0,5 / 0,8 s a pezzo, più l'1 % di errori da 8 s | stima |
| Seconda persona | rende 0,8 / 0,7 / 0,6 | Intralcio e un solo foglio: [INFERENZA] |

**Taratura.** Con questi valori il modello dà circa 5 s per tile, cioè 11 minuti per la mappa di oggi. Come riferimento, una guida a Catan stima 5-8 minuti per il montaggio del gioco base, con circa 60 pezzi tra esagoni, cornice, gettoni e porti, quindi 5-8 s a pezzo ([settlersboard.com](https://settlersboard.com/catan-setup-checklist)). È un solo riferimento esterno: le costanti «da tavolo» restano stime. Conviene cronometrare un montaggio vero con le tile di oggi e correggere `COSTANTI`; il confronto tra le opzioni dipende poco da questi valori, perché la differenza la fa il numero di pezzi.

**Ipotesi:**
- Oggi le tile sono già divise per tipo (10 pile). Se escono mescolate dalla scatola, il tempo sale di circa 1 s a tile, cioè 2 minuti in più per ogni opzione con tile singole [INFERENZA].
- Il «cambio mappa» è la media dei 9 passaggi base → TM-xx. Gli eroi da riportare alle Partenze si spostano allo stesso modo in tutte le opzioni e non sono contati.
- «Riordino» vuol dire togliere i pezzi e rimetterli nelle pile; il riordino per tipo nella scatola non è contato.

### Tutti i risultati

| | Opzione | Pezzi a partita | Muri a parte | Disegni | Pezzi da stampare | Fogli A4 / A3 | Montaggio, 1 persona | 2 persone | Cambio mappa R 8.12 | Riordino |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Tile singole (oggi) | 100 | 16 | 18 | 162 | 3 / 2 | 7:00–**11:13**–17:57 | 3:59–**6:46**–11:31 | 2:09–**3:21**–5:06 | 1:56–**2:54**–4:15 |
| A | Tri-esagoni | 38 | 16 | 75 | 94 | ~7 / ~3 | 5:35–**8:40**–13:53 | 3:12–**5:16**–8:59 | 1:56–**2:58**–4:32 | 0:54–**1:21**–1:59 |
| B | Fiori da 7 | 20 | 16 | 85 | 104 | ~12 / ~6 | 3:03–**4:50**–7:46 | 1:47–**3:01**–5:09 | 1:46–**2:41**–4:06 | 0:36–**0:54**–1:19 |
| C | Quadranti 5 × 5 | 4 | 0 | 20 | 40 | 20 / 7 | 0:32–**0:56**–1:41 | 0:24–**0:43**–1:21 | 0:52–**1:15**–1:57 | 0:04–**0:06**–0:09 |
| D | Fasce | 3 | 0 | 12 | 22 | 11 / 6 | 0:27–**0:48**–1:27 | 0:21–**0:38**–1:12 | 0:35–**0:49**–1:16 | 0:03–**0:04**–0:07 |
| E1 | Neutra + tile di oggi | 31 | 6 | 2 + tile di oggi | 3 + tile di oggi | 2 / 1 | 2:23–**3:54**–6:21 | 1:25–**2:28**–4:16 | 1:39–**2:35**–3:55 | 0:37–**0:56**–1:21 |
| E2 | Neutra + toppe sagomate | 17 | 6 | 16 | 47 | 4 / 2 | 1:40–**2:44**–4:30 | 1:01–**1:47**–3:07 | 1:17–**2:01**–3:03 | 0:23–**0:34**–0:51 |

## 3. Misura dell'esagono: resta 25,2 mm

- La tessera Esplorazione (Ø 24 mm) e le pedine devono entrare in un esagono (R 8.2). Sotto i 25,2 mm non ci stanno più.
- Una fascia da 25,2 mm è larga 264,6 mm: 267,6 mm con l'abbondanza, che entra in un A4 orizzontale (297 mm, circa 291 mm stampabili su una Epson di casa). Con 28 mm la fascia diventerebbe larga 294 mm: non entrerebbe più nell'A4 e servirebbero l'A3 o fasce tagliate in due, cioè più pezzi.
- La mappa montata resta di 265 × 226 mm, come oggi.

## 4. Le opzioni

### A. Tri-esagoni (3 esagoni a triangolo)

- **Misura:** 50 × 51 mm. Con la migliore delle 6 tassellature a triangolo la mappa ha 27 triangoli più 11 pezzi di bordo da 1-2 esagoni: 38 pezzi.
- **Preset:** riprodotti esattamente, ma servono **75 disegni** diversi per 94 pezzi stampati. Gli ostacoli che cambiano sono sparsi in 44 caselle, quindi quasi ogni triangolo cambia da un preset all'altro. Ogni preset diventa un puzzle a sé e trovare il pezzo giusto è una ricerca tra pezzi tutti diversi.
- **Muri:** restano 16 listelli.
- **Bordi:** i tri-esagoni combaciano sempre per forma; per il contenuto valgono le regole della mappa (un esagono intero per terreno).
- **Composizione libera:** debole, perché ogni pezzo porta una combinazione fissa di 3 terreni.
- **Pro:** pezzi piccoli e facili da stampare. **Contro:** risparmia solo il 23 % del tempo, i disegni sono tanti e il cambio di mappa resta lento.

### B. Fiori da 7 esagoni

- **Misura:** 76 × 73 mm. Con la migliore delle 14 tassellature ci sono 20 pezzi: 10 fiori interi e 10 pezzi di bordo da 1 a 5 esagoni, perché un rettangolo 10 × 10 non si copre con i fiori.
- **Preset:** esatti, ma servono **85 disegni**: è lo stesso problema di A, peggiorato.
- **Muri:** restano 16 listelli.
- **Pro:** più che dimezza il tempo di oggi (−57 %). **Contro:** è un puzzle diverso per ogni preset, servono 12 fogli A4 e la composizione libera è quasi nulla.

### C. Quadranti 5 × 5 (25 esagoni)

- **Misura:** 139 × 116 mm, 2 per foglio A4.
- **Preset:** esatti. 4 pezzi a partita: il quadrante nord-ovest girato di 180° fa il sud-est, il nord-est fa il sud-ovest. Servono 20 disegni (10 nord-ovest e 10 nord-est) e 40 pezzi.
- **Muri:** tutti stampati. Un muro sul taglio sta sul pezzo nord-ovest o sud-est.
- **Bordi:** il taglio verticale tra le colonne E ed F passa in mezzo alle caselle che cambiano, quindi i bordi non sono standard. Mescolando 4 quadranti di preset diversi, **8.281 combinazioni su 10.000** (83 %) passano i controlli del §17; le altre hanno vicoli ciechi, Cripte con meno di 3 ingressi o esagoni che, se bloccati, isolano una zona.
- **Pro:** veloce (0:56). **Contro:** 20 fogli A4, bordi da controllare e composizione libera solo parziale.

### D. Fasce: fascia nord + fiume + fascia sud (consigliata)

Mock-up: `mockup_fasce_base.png` (preset base) e `mockup_fasce_miste.png` (nord di TM-03 con sud di TM-06).

- **Pezzi:**
  - **Fascia del preset:** righe 1-4, 40 esagoni, 264,6 × 94,6 mm. La stessa fascia girata di 180° fa le righe 7-10, quindi ogni preset è **una fascia stampata due volte**.
  - **Fiume:** righe 5-6, 20 esagoni, 264,6 × 50,9 mm, uguale per tutti. Se ne stampano due versioni: una con le mura C6|D6 e G5|H5 (9 preset) e una senza (Flegias).
  - Ogni pezzo ha il nome stampato vicino al bordo esterno, per esempio «TM-03 Foresta · nord». Per montare la mappa non serve il foglio del preset.
- **Disegni e stampa:** 10 fasce e 2 fiumi, 22 pezzi. In A4 orizzontale entrano 2 fasce per foglio (2 × 97,6 = 195 mm di 210): 10 fogli per le fasce e 1 per i due fiumi, **11 fogli A4**. In A3 entrano 4 fasce per foglio: **6 fogli A3**.
- **Muri:** tutti e 16 stampati. I muri sul taglio (G4|H5, H4|I5, F4|G5, I4|J5, C6|D7, B6|C7, A6|B7, D6|E7) stanno sulla fascia, così viaggiano con il loro preset. **Nessun listello da posare.**
- **Preset:** **tutti e 10 esatti**, senza nessuna differenza.
- **Bordi:** la fascia si attacca solo al fiume e il bordo del fiume è lo stesso per tutti. Il «connettore» di ogni fascia sono 18 esagoni fissi: A1 B1 C1 H1 I1 A2 C2 I2 J2 D3 E3 G3 C4 D4 E4 F4 G4 H4 (Partenze 1-2, Cripte 1-2 con i loro muri e ingressi, le «?»). Una fascia nuova, per esempio per una carta Mappa futura, cambia solo le altre 22 caselle (D1 E1 F1 G1 J1 B2 D2 E2 F2 G2 H2 A3 B3 C3 F3 H3 I3 J3 A4 B4 I4 J4) e le mura libere, e si attacca da sola. Ogni esagono è disegnato fino al proprio contorno, come le tile di oggi, quindi due terreni diversi accanto restano leggibili. Dentro una fascia gli ostacoli vicini dello stesso tipo si possono disegnare come un'unica macchia (un bosco di 4 esagoni), mai attraverso il taglio. Il fiume è un pezzo unico, quindi l'acqua è sempre continua.
- **Composizione libera:**
  1. Si combinano la fascia nord di un preset e la sud di un altro, con il fiume con o senza mura: **tutte le 200 combinazioni passano i controlli del §17** (strada collegata, almeno 2 uscite, nessun esagono che isola una zona, 3 ingressi per Cripta, Cripta più vicina a 4 passi da ogni Partenza, Partenza→Cripta da 4 a 8). Queste mappe non sono più identiche girate di 180°.
  2. Si appoggiano le tile di oggi sopra una fascia come toppe.
  3. Si usano solo le tile, come adesso (vedi E1).
- **Cambio di mappa a metà partita (R 8.12):** si mettono accanto alla mappa le 2 fasce nuove. Le 16 tessere Esplorazione che stanno sulle «?» delle fasce passano sulle stesse caselle delle fasce nuove, coperte o scoperte come erano. Poi si sfilano le fasce vecchie e si infilano le nuove (il fiume si gira solo da o verso Flegias). Il modello dà **0:49 contro 3:21**: aiuta il punto aperto N26.
- **Fronte e retro:** si può incollare un preset sul retro di un altro (10 pezzi invece di 20), ma il taglio a zig-zag del retro si sposta di circa 1 mm rispetto al fronte. Per ora conviene stampare solo il fronte, come tutto il kit.
- **Pro:**
  - montaggio in 48 s, 14 volte più veloce di oggi;
  - zero muri da posare;
  - niente foglio da leggere;
  - cambio di mappa rapido;
  - preset esatti;
  - una carta Mappa nuova costa 1 foglio A4.
- **Contro:**
  - le fasce non sono generiche, ogni fascia è un preset (vedi le domande);
  - pezzi grandi e sottili possono incurvarsi: serve cartoncino pesante o un supporto rigido;
  - il taglio a zig-zag sul lato verso il fiume richiede un po' di pazienza. I lati esterni si possono tagliare dritti.

### E. Plancia neutra con toppe di terreno (E1 consigliata insieme a D)

Mock-up: `mockup_neutra_toppe.png`.

- **Plancia:** due fasce «neutre» (le 22 caselle che cambiano sono stampate come strada; muri delle Cripte stampati) e il fiume senza mura. Sopra si posano i 28 ostacoli di terra del preset e le 6 mura libere a listello.
- **E1:** le toppe sono le **tile di oggi**. Il kit ne ha già abbastanza: bosco 23, case 18 e rocce 23, contro un massimo di 18, 14 e 18 nei preset. Si stampano solo le 2 fasce neutre: **1 foglio A4**, mentre il fiume è quello di D. Montaggio in 3:54 tipico.
- **E2:** toppe sagomate da 1-3 esagoni dello stesso terreno (singola, doppia, tre in fila, a curva, a triangolo), da 12 a 16 per preset. Servono 44 toppe di 14 forme × terreno, 16 disegni in tutto con la plancia. Montaggio in 2:44: guadagna un minuto su E1 ma aggiunge 14 forme da cercare e 2-3 fogli da stampare, quindi non vale la pena per ora.
- **Preset:** esatti.
- **Composizione libera:** completa. Qualsiasi ostacolo va su qualsiasi casella e anche Partenze, Cripte e «?» si possono coprire con una tile.
- **Pro:** generica come vuole D23 e costa 1 foglio. **Contro:** restano 28 + 6 pezzi piccoli, quindi è 4-5 volte più lenta di D.

## 5. Raccomandazione

**D per i preset, E1 per provare, le tile di oggi per tutto il resto.**

1. **Preset (base e TM-01…09): fasce D.** Sono 3 pezzi senza muri da posare e senza foglio da leggere, montati in 0:27–0:48–1:27 invece di 7:00–11:13–17:57; con due persone 0:38 invece di 6:46. Il cambio di mappa scende da 3:21 a 0:49. Tutti i preset sono riprodotti esattamente.
2. **Varianti in playtest:** si combinano le fasce di preset diversi (100 combinazioni, tutte valide), oppure si parte dalla fascia neutra con le tile di oggi come toppe (E1, 3:54).
3. **Composizione del tutto libera:** restano le 162 tile di oggi (D23).

Stampa nuova: 10 fogli di fasce, 1 di fiumi e 1 di fasce neutre, cioè **12 fogli A4** di cartoncino (o 6 A3). Non serve ristampare le tile né i 10 fogli dei preset, che restano utili come riferimento.

Le opzioni A e B sono state scartate: con le caselle che cambiano sparse in 44 punti, i pezzi piccoli diventano un puzzle diverso per ogni preset (75-85 disegni) e il tempo scende poco. C ha la stessa velocità di D ma il doppio dei fogli e bordi non standard (83 % di combinazioni valide).

**Se si adotta D**, vanno aggiornati in un lavoro a parte:
- nella Spec: D23, R 8.1, R 8.12 e §2/§17 (le fasce come componente; il cambio di mappa con le fasce);
- `v7/stampa/LEGGIMI.md` e `componenti_gen/gen.py` (nuovo componente «fasce_mappa»), più `verifica_pdf.py`.

Qui non è stato toccato niente di tutto questo.

## 6. Domande aperte per Daniele

1. **Fasce legate a un preset e D23.** D23 vuole tile generiche. Le fasce D sono ciascuna un preset; la parte generica resta nelle tile e nella fascia neutra. Va bene così, o la parte generica deve essere quella principale (cioè E1 come sistema base)?
2. **Stampante:** che modello di Epson è? Stampa A3 e quale grammatura massima? Per fasce lunghe 265 mm conviene un cartoncino da 250-300 g o incollare il foglio su un cartone da 1 mm, altrimenti si incurvano.
3. **Fiume:** due pezzi separati (con le mura e senza, per Flegias) o uno solo stampato fronte e retro?
4. **Bordo esterno:** si tagliano dritti i lati esterni della mappa (più veloce, rimane un triangolino di sfondo) o si segue il contorno degli esagoni?
5. **Mappe miste:** in playtest si possono combinare il nord di un preset e il sud di un altro? Le mappe che ne escono non sono più identiche girate di 180°, quindi le Partenze non sono più perfettamente pari, anche se tutti i controlli del §17 restano rispettati.
6. **Tile di oggi:** restano tutte e 162 nel kit, o si tengono solo gli ostacoli (bosco, case, rocce, acqua) come toppe?
7. **Cambio a metà partita:** spostare 16 tessere Esplorazione sulle fasce nuove (circa 30 s) va bene, o si preferisce un altro modo?
8. **Taratura:** possiamo cronometrare un montaggio vero con le tile di oggi? Servirebbe a correggere le costanti del modello, che ora sono stimate.
