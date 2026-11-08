# Istruzioni di stampa A3 — kit di playtest «Il Tesoro del Goblin» (v6, 8/11)

Stesso kit di `../playtest_v6/` (stessi testi, stesse misure dei pezzi), impaginato su **A3 verticale (297 × 420 mm)**; solo la plancia è su A3 orizzontale. Per cosa comprare, carta, taglio e unione delle carte, montaggio di plance eroe e rotelle, controlli e problemi valgono le istruzioni A4: [`../playtest_v6/ISTRUZIONI_DI_STAMPA.md`](../playtest_v6/ISTRUZIONI_DI_STAMPA.md). Qui solo le differenze.

Impostazioni come per l'A4: **scala 100 %**, **carta A3**, **solo fronte** (stampa su due lati disattivata), tipo carta «cartoncino» per carte, plance eroe, dischi e segnalini. Tutto il contenuto e tutte le tacche stanno ad almeno 6 mm dal bordo del foglio, tranne i fogli delle carte: l'abbondanza di colore del blocco di carte arriva a 10,5 mm dai lati lunghi e a 22 mm dall'alto e dal basso, le linee di rifilo a più di 13 mm.

## File, in ordine di stampa (28 fogli A3)

| File | Contenuto | Pezzi | Fogli A3 |
|---|---|---|---|
| `00_prova_stampa.pdf` | Righello 100 mm, quadrato 50 mm, riquadro a 6,5 mm | – | 1 |
| `carte_comuni.pdf` + `carte_comuni_retri.pdf` | 8 Mappe, 12 Equipaggiamenti, 24 Incanti + i loro dorsi | 44 + 44 | 3 + 3 |
| `carte_classe.pdf` + `carte_classe_retri.pdf` | 4 mazzi di classe + 4 Carte Classe TC-01…04 + 29 dorsi (le Carte Classe non hanno dorso) | 33 + 29 | 3 + 3 |
| `carte_specie.pdf` | 8 Carte Specie, un lato | 8 | 1 |
| `carte_mostro.pdf` + `carte_mostro_retri.pdf` | Mazzetti 1, 2 e boss + dorsi | 24 + 24 | 2 + 2 |
| `carte_imprevisto.pdf` + `carte_imprevisto_retri.pdf` | Trappola, Locanda, Fonte, Fabbro + dorsi | 11 + 11 | 1 + 1 |
| `carte_aiuto_divisori.pdf` | 8 Carte Aiuto («Il turno» e «Riepilogo») + 5 Divisori, un lato | 13 | 1 |
| `plance_eroe.pdf` | 4 plance eroe 280 × 194 mm, 2 per foglio, una sopra l'altra | 4 | 2 |
| `rotelle_eroe.pdf` | 24 dischi Ø 52 mm delle plance eroe + i 2 dischi della plancia («PV del mostro», «PV del custode») | 26 | 1 |
| `componenti_misti.pdf` | 9 pedine, 32 segnalini Ø 20 mm (16 Indizi, 4 Forte Volontà, 12 Usato), 14 tessere Stato 26 × 18 mm | 9 + 32 + 14 | 1 |
| `tessere_esplorazione.pdf` | 25 rosse Mostro, 11 blu Imprevisto, un lato | 36 (Ø 24 mm) | 1 |
| `plancia.pdf` | Plancia «Le Terre di Hande» in 2 fogli A3 orizzontali | 1 (355,6 × 447,7 mm) | 2 |

Totale kit: **28 fogli A3**. Regolamento e partita rapida restano in A4: [`../../regolamento/playtest/Regolamento_playtest_v6.pdf`](../../regolamento/playtest/Regolamento_playtest_v6.pdf) (11 fogli) e [`../../regolamento/playtest/Partita_rapida_v6.pdf`](../../regolamento/playtest/Partita_rapida_v6.pdf) (2 fogli), solo fronte.

**Carte:** 16 per foglio (4 × 4), **ognuna separata con la sua abbondanza di 3 mm** oltre il rifilo 63 × 88 mm: celle di 69 × 94 mm che si toccano senza sovrapporsi, blocco 276 × 376 mm centrato. Sul foglio: tacche d'angolo nere nei quattro margini, filetti bianchi sottilissimi in ogni angolo di ogni carta dentro l'abbondanza (finiscono a 0,3 mm dal rifilo), etichetta «FRONTI», «RETRI · … coi fronti del foglio k» o «SOLO FRONTE» in alto e nome file in basso. Il dorso nella posizione p del foglio k di `*_retri.pdf` va con il fronte nella stessa posizione del foglio k (non specchiato); l'etichetta minuscola nell'abbondanza in basso del dorso riporta mazzo e ID del fronte e sparisce col taglio. Taglio e unione come nelle istruzioni A4 (sezione 4); qui l'abbondanza è 3 mm invece di 2,5 e le carte esterne non perdono colore nella zona non stampabile.

## Montaggio della plancia (2 fogli)

Ogni foglio stampa tutta la larghezza della plancia (355,6 mm) e una finestra alta 236 mm: foglio 1 = plancia da 0 a 236 mm, foglio 2 = da 211,7 a 447,7 mm. **Sovrapposizione = 2 × 236 − 447,7 = 24,3 mm**, con 5 croci rosse al centro della fascia (y = 223,8 mm della plancia).

1. Foglio 1: rifila solo il bianco esterno sulle tacche (sinistra, destra, alto).
2. Foglio 2: taglia il margine bianco in ALTO lungo le tacche, poi sinistra, destra e basso.
3. Appoggia il foglio 2 sulla fascia bassa del foglio 1 (24,3 mm), fai coincidere le 5 croci rosse e il disegno, incolla.
4. Incolla su cartoncino 1-2 mm di almeno 36 × 45 cm (come per l'A4).
5. Fora i 2 centri segnati nella Sala del Tesoro e fissa con 2 fermacampioni i dischi «PV del mostro» e «PV del custode» (da `rotelle_eroe.pdf`), dopo averne ritagliato la finestra.

## Rigenerare

- Carte: `python3 stampa/sorgenti/carte/genera_carte.py --formato A3` (progetti DesignCraft in `stampa/sorgenti/carte/A3/`).
- Componenti: `bash stampa/sorgenti/componenti_gen/build.sh stampa/sorgenti/A3 stampa/playtest_v6_A3 A3`.
- Controlli: `python3 stampa/sorgenti/verifica_pdf.py --formato A3`.
