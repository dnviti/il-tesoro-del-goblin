# v7 — in progettazione e in produzione (dal 10/11/2026)

La v7 rivede il gioco a partire dal playtest v6 (`../v6_08-11/`) e dai commenti di Desy del 9/11: power level dalle carte, 5 classi (nuovo Giullare), catene di risposta, perdita di equipaggiamento con il D6, mano massima di 10 carte, nuova mappa, integrazione delle 98 carte nuove di Desy.

| Percorso | Cosa è |
|---|---|
| `idee/v7_piano_TEMP.docx` | Piano della v7 (documento di lavoro con i commenti di Desy) |
| `idee/` | Appunti e materiale di partenza: `idee-08-11-26.txt`, bozza della mappa `v7_bozza_mappa.svg`, nota vocale del 9/11 |
| `desy/` | File di Desy da integrare: `Carte_nuove_2026-11-05.xlsx` (98 carte, scala D20 da riportare ai 2D6) e `Il_Tesoro_del_Goblin_Analisi_Bilanciamento_Mostri_v4 test.xlsx` (workbook di bilanciamento dei mostri) |

Il playtest v7 è in produzione in `regolamento/` (specifica delle regole: `regolamento/Spec_v7.md`), `stampa/` (kit di stampa) e `simulatore/` (simulatore aggiornato alla v7).

**Desy:** i file nuovi vanno in `desy/`.

## Stato al 10–11/11 (sera): cosa è fatto e cosa resta

**Fatto**
- **Carte di Desy (D22):** le idee di `desy/Idee desi carte classi.ods` sono riscritte col tono goliardico. Ogni classe passa a 20 carte (XX-11…20) e il mazzetto è di 10 carte su 20. Il mazzo comune passa a 81 carte (TM-09, TE-26…31, TI-31…41). L'Oracolo ha 10 carte nuove. I nuovi Equipaggiamenti non hanno più la riga fissa «+1 AR finché…». La revisione ha aggiornato le formule del §14.5 e le tessere Stato (31).
- **Mappe:** la plancia base è la «Strettoie», con gli ostacoli spostati dai bordi verso le vie per le Cripte. Ogni carta Mappa ha la sua plancia (`simulatore/plance/`). La regola R 8.12 dice: si gioca una Mappa, cambia la plancia e tutti tornano alla propria Partenza.
- **Simulatore:** gestisce il cambio di plancia e il mazzetto 10 su 20, e ha gli effetti di tutte le carte nuove (`--verifica-carte` è pulito).
- **Docx:** regolamento e partita rapida sono aggiornati.
- **Illustrazioni:** lo stile e le cartelle sono descritti in `stampa/sorgenti/arte/STILE.md`. Ogni immagine passa da PhotoCraft con `arte/elabora.py` (grezza → `.pcraft` → PNG a 300 ppi). `genera_carte.py` stampa l'immagine nel riquadro, con la battuta su una fascetta. Le plance si generano con `idee/genera_bozza_mappa.py --tema … --senza-linee`.

**Da fare (in ordine)**
1. **Bilanciamento (decisione di Daniele):** sistemare gli effetti dei nuovi Equipaggiamenti di classe perché siano bilanciati ma restino interessanti e divertenti. Il simulatore mostra la partita più lunga di circa 4 round (14,6/13,9/14,1 contro 10,3/9,3/9,1): questi oggetti alzano il PL senza dare ATT/AR, e gli eroi arrivano prima al mazzetto 3. Dettagli in `simulatore/LEGGIMI.md`.
2. **Immagini mancanti (82 carte):** TM-09, TE-09, TE-10, TE-26…31, TI-22, TI-26…41, CA-09…20, CG-11…20, CO-11…20, CR-07…09, CR-11…20, CS-10…20. I prompt sono in `arte/prompt/*.csv` (`nuove.csv` per le carte del 10/11; da riallineare ai testi rivisti di CG-14, CG-17, CA-19, CO-12 e TM-09). Da rifare 18 immagini comuni con scritte o bordi: TE-02, TE-03, TE-05, TE-06, TE-07, TE-13, TE-14, TE-15, TE-22, TE-23, TI-07, TI-14, TI-15, TI-17, TI-19, TI-21, TM-05, TM-08. Il credito OpenRouter è finito; `openai-codex/gpt-image-2` funziona solo dal dispositivo `generate_image` della sessione principale, circa 4–5 minuti a immagine, 8 in parallelo.
3. **Terreni delle plance:** ci sono solo BASE e TUNDRA. Gli altri 8 temi (FORZIERE, CITTA, FORESTA, SOTTOVELO, MINIERA, YUMA, FLEGIAS, MIMI) hanno i prompt in `arte/prompt/terreni.csv`. Tundra è poco contrastata; in BASE bosco e rocce si somigliano.
4. **PDF/X-4:** le PNG in `arte/png` hanno un profilo ICC che DesignCraft scarta, e i PDF con immagini non passano `validate-pdf`. Va tolto il profilo in `elabora.py` (le immagini sono sRGB).
5. **Kit di stampa:** rigenerare carte e componenti, A4 e A3, con le immagini e le 10 plance (stasera non è stato rigenerato). Poi `verifica_pdf.py`.
6. **Da confermare:**
   - TM-09 nuovo (Indizio con D6 ≤ LV + 2);
   - CS-19 conta come ritiro (lo blocca NE-47);
   - la chiusura senza vincitore di uno scontro durante un cambio di plancia;
   - le tessere Stato, una per fonte?
