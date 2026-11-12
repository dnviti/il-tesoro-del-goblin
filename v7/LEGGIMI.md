# v7 — in progettazione e in produzione (dal 10/11/2026)

La v7 rivede il gioco a partire dal playtest v6 (`../v6_08-11/`) e dai commenti di Desy del 9/11: power level dalle carte, 5 classi (nuovo Giullare), catene di risposta, perdita di equipaggiamento con il D6, mano massima di 10 carte, nuova mappa, integrazione delle 98 carte nuove di Desy.

| Percorso | Cosa è |
|---|---|
| `idee/v7_piano_TEMP.docx` | Piano della v7 (documento di lavoro con i commenti di Desy) |
| `idee/` | Appunti e materiale di partenza: `idee-08-11-26.txt`, bozza della mappa `v7_bozza_mappa.svg`, nota vocale del 9/11 |
| `desy_design carte/` | File di Desy (cartella rinominata da Desy l'11/11): `Carte_nuove_2026-11-05.xlsx` (98 carte, scala D20 da riportare ai 2D6), `Idee desi carte classi.ods`, `Idee del Desy per mostri .docx`, il workbook di bilanciamento dei mostri e le prove di design delle carte (`Nome carta.pptx/png`, `Scheletro_Canva_editabile.pptx`) |

Il playtest v7 è in produzione in `regolamento/` (specifica delle regole: `regolamento/Spec_v7.md`), `stampa/` (kit di stampa) e `simulatore/` (simulatore aggiornato alla v7).

**Desy:** i file nuovi vanno in `desy_design carte/`.

## Stato al 12/11 (sera): cosa è fatto e cosa resta

**Fatto**
- **Carte di Desy (D22):** le idee di `desy_design carte/Idee desi carte classi.ods` sono riscritte col tono goliardico. Ogni classe passa a 20 carte (XX-11…20) e il mazzetto è di 10 carte su 20. Il mazzo comune passa a 81 carte (TM-09, TE-26…31, TI-31…41). L'Oracolo ha 10 carte nuove. I nuovi Equipaggiamenti non hanno più la riga fissa «+1 AR finché…». La revisione ha aggiornato le formule del §14.5 e le tessere Stato (31).
- **Manuale (12/11):** il regolamento per i giocatori è il manuale in `regolamento/manuale/`: 5 pagine impaginate con DesignCraft (`Manuale_Il_Tesoro_del_Goblin.designcraft`), in PDF/X-1a per la tipografia (`Manuale_Il_Tesoro_del_Goblin_PDFX1a.pdf`) e in A4 da stampare a casa (`Manuale_Il_Tesoro_del_Goblin_stampa_A4.pdf`). Testo in `testo_manuale.md`, generatore in `manuale/sorgenti/`. `Regolamento_playtest_v7.docx` e `Partita_rapida_v7.docx` sono superati dal manuale: non sono più aggiornati e restano com'erano, con le annotazioni di Desy.
- **Mappa 12×12 a fiori (D24 e D25, 12/11, decisioni di Daniele):** supera la mappa a tile del D23 e le plance 10 × 10. La mappa è una base stampata su 2 A4 (coordinate 1–12, 46 esagoni di bordo con le 6 Partenze, 14 spazi numerati) più 14 fiori di 7 esagoni a due facce, montati col draft o con uno dei 10 preset (base «Strettoie» + TM-01…09). Niente muri. Si cammina ovunque tranne su bosco, rocce e case; l'acqua è terreno accidentato (1 MOV in più). La Cripta non è stampata: si tira con 2D6 per la colonna e 2D6 per la riga. Una carta Mappa cambia solo 3 fiori. Regole in `regolamento/Spec_v7.md` (D24, D25, R 3.1, R 8.1–8.12, R 10.6, R 10.11, §17); progetto e numeri in `idee/mappa_tessere/12x12/progetto.md`.
- **D26 (12/11 sera, Daniele):** niente Equipaggiamento gratis in preparazione; nel primo giro gli eroi non si attaccano tra loro (niente Duello); contro un mostro l'eroe fa al massimo 3 attacchi, poi il mostro scappa senza ricompense (il custode mai). Regole in `regolamento/Spec_v7.md` (R 3.8, R 7.5, R 7.9, R 10.8); punti aperti N30–N32. Simulatore e Carte Aiuto non sono ancora aggiornati.
- **Kit della mappa 12×12:** rigenerato. In A4: `mappa_base.pdf` (2 fogli), `mappa_fiori.pdf` (3 fogli fronte/retro su cartoncino da 250–300 g, retro specchiato per il duplex manuale sul lato lungo) e `mappa_preset.pdf` (10 fogli su carta normale); in A3: `sala_tesoro.pdf`. Non ci sono più tessere singole, listelli dei muri né preset 10×10. I dati stanno in `stampa/sorgenti/dati/fiori.csv`, `base12.csv` e `preset12.csv`. Comandi: `python3 idee/mappa_tessere/12x12/mappa12.py --scrivi-dati` (rigenera i CSV), `… --verifica-csv` (rimonta e controlla i 10 preset), `stampa/sorgenti/componenti_gen/build.sh stampa/sorgenti stampa/playtest_v7`, `python3 stampa/sorgenti/verifica_pdf.py`.
- **Arte della mappa (12/11):** i 28 lati dei fiori e la base sono illustrati con gpt-image-2. Le immagini partono dalle guide di planimetria in `stampa/sorgenti/arte/mappa_guide/` (`genera_guide.py`, `prompt.csv`); le grezze sono in `arte/grezze/MF-*.webp` e `MB-*.webp`. `python3 stampa/sorgenti/arte/mappa_compone.py --verifica` controlla esagono per esagono che il terreno dipinto corrisponda ai dati; senza `--verifica` scrive `arte/png/MF-*.png` e `MB-BASE.png`, che kit e carta 3D usano al posto del vettoriale. Le linee degli esagoni, gli id, le frecce, il «+1» e le coordinate restano vettoriali, sovrapposti all'immagine. Peso: `mappa_fiori.pdf` e `carta_fiori_3d.pdf` circa 43 MB ciascuno.
- **Simulatore (12/11):** lavora sulla mappa 12×12 letta dai CSV, con draft o preset (`--preset`), costi di terreno presi dai dati, Cripta a coordinate e cambio di 3 fiori; `plance/` è stato tolto. 1000 partite: 11,8/11,3/11,1 turni (2/3/4 giocatori); `--verifica-carte` e `--verifica-mostri` sono puliti (dettagli in `simulatore/LEGGIMI.md`).
- **Docx:** superati dal manuale (vedi sopra).
- **Illustrazioni (11/11):** tutte rifatte nello stile semplice (`stampa/sorgenti/arte/STILE.md`): tratto a mano sgangherato, pochi oggetti, sfondo di scena semplice, un tocco di steampunk medievale con alta magia. L'immagine fa capire cosa fa la carta ed è facile da ridisegnare per un illustratore. Ogni immagine passa da PhotoCraft (`arte/elabora.py`: grezza → `.pcraft` → PNG a 300 ppi, senza profilo ICC). Le carte sono impaginate «alla Magic»: immagine 54,5 × 38,1 mm con cornice, regole in corpo 7,8, battuta in corsivo in fondo sotto un filetto. La grafica vettoriale è leggera, con un tocco steampunk (bordi, retri, pedine, plance).
- **Tessere 3D (12/11):** si fanno con SolidCraft, non più con Blender: `python3 stampa/3d_solidcraft/genera_3d_solidcraft.py` (circa 75 s, legge `base12.csv`). Escono il vassoio in 4 quarti (ognuno ≤ 175×145 mm, montato 329×283, con le cavità dei fiori e la carta della base in una tasca), 14 fiori con tasche su entrambe le facce, 24 dischi «?» e il segnalino Cripta, in STL e 3MF. La carta dei fiori per la versione 3D è in `out/carta_fiori_3d.pdf` (facce separate, taglio 1,3 mm più interno). Giochi: 0,30 mm tra i quarti, 0,40 mm tra i fiori, 0,20 mm nella cavità. La vecchia `stampa/3d/` (Blender, D23) è stata tolta.

**Da fare (in ordine)**
0. **Segnalini illustrati (fatto 13/11, 00:25):** 15 immagini gpt-image-2 (`arte/grezze/SG-*`, `ST-*`, `TX-*`) in `segnalini.pdf`, `tessere_esplorazione.pdf` (pagina 2 = dorsi in fronte/retro) e nuovo `segnalini_3d.pdf`. **Problema aperto:** sugli Stati l'immagine è un quadrato di 8,4 mm e le regole lunghe scendono a circa 2,4 pt, illeggibili: ingrandire le tessere Stato o accorciare i testi (decisione di Daniele). Altri punti aperti: texture nei render 3D, 14 o 28 fiori 3D, fondo del vassoio sotto i numeri, 3 interpretazioni del simulatore, riquadro 4 di S4.
0. **Guida di montaggio:** fatta il 12/11 sera: `stampa/playtest_v7/guida_montaggio_mappa.pdf` (2 pagine) e render 3D `stampa/3d_solidcraft/out/render_montata.png` / `render_esplosa.png` (colori pieni, senza texture: da migliorare). Da verificare alla prima stampa: tenuta delle code tra i quarti del vassoio.
1. **Prova al tavolo:**
   - il bilanciamento: le righe «Se… LV 3 o più: AR» potrebbero rendere i mazzetti 2–3 troppo sicuri;
   - il draft della mappa e il cambio di mappa a 3 fiori (N26);
   - il terreno accidentato (N29).
2. **3D:** fondo piatto applicato il 12/11 alle 23:21: tutti i pezzi hanno la tasca per la carta solo sopra, il fiore 3D ha una faccia sola. Da decidere: stampare 28 fiori (uno per faccia) o 14 con la carta da scambiare. Ristampare un fiore di prova. Nel vassoio, sotto i numeri incisi degli spazi restano solo 0,7 mm: valutare numeri meno profondi o un fondo più spesso.
3. **Carte Aiuto:** AI-01…04 dicono ancora «solo su strada» e «D6 per la Cripta» (N27).
4. **Da confermare:**
   - la carta Mappa ritira la Cripta anche oltre i limiti di R 10.11? (N28);
   - TM-09 (Indizio con D6 ≤ LV + 2);
   - CS-19 conta come ritiro (lo blocca NE-47);
   - la chiusura senza vincitore di uno scontro durante un cambio di mappa;
   - le tessere Stato, una per fonte?
