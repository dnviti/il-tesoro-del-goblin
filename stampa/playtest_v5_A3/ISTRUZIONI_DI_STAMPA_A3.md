# Istruzioni di stampa A3 — kit di playtest «Il Tesoro del Goblin»

Stesso kit di `../playtest_v5/` (stessi testi, stesse misure dei pezzi), impaginato su **A3 verticale (297 × 420 mm)**; solo la plancia è su A3 orizzontale. Per carta, grammature, cosa comprare, taglio delle carte, controlli e problemi valgono le istruzioni A4: [`../playtest_v5/ISTRUZIONI_DI_STAMPA.md`](../playtest_v5/ISTRUZIONI_DI_STAMPA.md). Qui solo le differenze.

Impostazioni come per l'A4: **scala 100 %**, **carta A3**, fronte-retro con ribaltamento sul **LATO LUNGO**; nei PDF fronte-retro le facciate sono già in ordine F1, R1, F2, R2, … (dispari = fronti, pari = retro). Tutto il contenuto e tutte le tacche stanno ad almeno 6,5 mm dal bordo del foglio, tranne i fogli delle carte: l'abbondanza di colore del blocco di carte arriva a 10,5 mm dai lati lunghi e a 22 mm dall'alto e dal basso, le linee di rifilo a più di 13 mm.

## File, in ordine di stampa

| File | Contenuto | Pezzi | Facciate (fogli A3) | Stampa |
|---|---|---|---|---|
| `00_prova_stampa.pdf` | Righello 100 mm, quadrato 50 mm, riquadro a 6,5 mm, bersagli fronte-retro | – | 2 (1) | Fronte-retro, lato lungo |
| `carte_comuni.pdf` | 8 Mappe, 12 Equipaggiamenti, 24 Incanti | 44 | 6 (3) | Fronte-retro, lato lungo |
| `carte_classe.pdf` | 4 mazzi di classe + 4 ritratti TC-01…04 | 33 | 6 (3) | Fronte-retro, lato lungo |
| `carte_mostro.pdf` | Mazzetti 1, 2 e boss | 24 | 4 (2) | Fronte-retro, lato lungo |
| `carte_imprevisto.pdf` | Trappola, Locanda, Fonte, Fabbro | 11 | 2 (1) | Fronte-retro, lato lungo |
| `carte_aiuto_divisori.pdf` | 4 Carte Aiuto + 5 Divisori | 9 | 2 (1) | Fronte-retro, lato lungo |
| `plancia.pdf` | Plancia «Le Terre di Hande» in 2 fogli A3 orizzontali | 1 (355,6 × 447,7 mm) | 2 (2) | Solo fronte |
| `schede_eroe.pdf` | Assaltatore + Ricercatore, Stregone + Oracolo | 4 (222 × 176,8 mm) | 2 (2) | Solo fronte, 2 schede per foglio |
| `tessere_esplorazione.pdf` | 25 rosse Mostro, 11 blu Imprevisto | 36 (Ø 24 mm) | 2 (1) | Fronte-retro, lato lungo (retro uguale al fronte) |
| `componenti_misti.pdf` | 9 pedine, 8 tessere specie, 16 Indizi + 8 Clessidre + 4 Forte Volontà | 9 + 8 + 28 | 1 (1) | Solo fronte |

**Carte:** 16 per foglio (4 × 4), **ognuna separata con la sua abbondanza di 3 mm** oltre il rifilo 63 × 88 mm: celle di 69 × 94 mm che si toccano senza sovrapporsi, blocco 276 × 376 mm centrato. Sul foglio: tacche d'angolo nere nei quattro margini (in alto e in basso per i rifili verticali, a sinistra e a destra per quelli orizzontali), filetti bianchi sottilissimi in ogni angolo di ogni carta dentro l'abbondanza (finiscono a 0,3 mm dal rifilo), etichetta «FRONTE/RETRO · foglio N di M» in alto e nome file in basso. Taglio: **1.** taglio grossolano lungo i confini tra le celle (a 3 mm dal rifilo di ogni carta; tra carte dello stesso colore a metà dei segmenti bianchi che uniscono i filetti), tolleranza ±1 mm; **2.** metti ogni carta nella dima MTG (63 × 88 mm) con i filetti bianchi che arrivano al bordo della finestra su tutti e 4 i lati; **3.** taglio finale lungo il bordo della dima. Dettagli, carta e consigli: sezione «Taglio delle carte» delle istruzioni A4 (qui l'abbondanza è 3 mm invece di 2,5 e le carte esterne non perdono colore nella zona non stampabile). Carta consigliata 160-200 g/m² opaca (80 g solo in bustina con una carta vecchia dietro).

**Totali:** 121 carte, 36 tessere esplorazione, 8 tessere specie, 28 segnalini, 9 pedine, 4 schede eroe, 1 plancia. **17 fogli A3** (29 facciate: 12 fronte-retro + 5 solo fronte) contro **28 fogli A4** (45 facciate) del kit A4. Il regolamento resta in A4 (`../regolamento/playtest/Regolamento_playtest.pdf`).

## Montaggio della plancia (2 fogli)

Ogni foglio stampa tutta la larghezza della plancia (355,6 mm) e una finestra alta 236 mm: foglio 1 = plancia da 0 a 236 mm, foglio 2 = da 211,7 a 447,7 mm. **Sovrapposizione = 2 × 236 − 447,7 = 24,3 mm**, con 5 croci rosse al centro della fascia (y = 223,8 mm della plancia).

1. Foglio 1: rifila solo il bianco esterno sulle tacche (sinistra, destra, alto).
2. Foglio 2: taglia il margine bianco in ALTO lungo le tacche, poi sinistra, destra e basso.
3. Appoggia il foglio 2 sulla fascia bassa del foglio 1 (24,3 mm), fai coincidere le 5 croci rosse e il disegno, incolla.
4. Incolla su cartoncino 1-2 mm di almeno 36 × 45 cm (come per l'A4).

## Rigenerare

- Carte: `python3 stampa/sorgenti/carte/genera_carte.py --formato A3` (progetti DesignCraft in `stampa/sorgenti/carte/A3/`).
- Componenti: `bash stampa/sorgenti/componenti_gen/build.sh stampa/sorgenti/A3 stampa/playtest_v5_A3 A3`.
- Controlli: `python3 stampa/sorgenti/verifica_pdf.py --formato A3`.
