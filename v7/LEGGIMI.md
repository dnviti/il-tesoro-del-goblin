# v7 — in progettazione e in produzione (dal 10/11/2026)

La v7 rivede il gioco a partire dal playtest v6 (`../v6_08-11/`) e dai commenti di Desy del 9/11: power level dalle carte, 5 classi (nuovo Giullare), catene di risposta, perdita di equipaggiamento con il D6, mano massima di 10 carte, nuova mappa, integrazione delle 98 carte nuove di Desy.

| Percorso | Cosa è |
|---|---|
| `idee/v7_piano_TEMP.docx` | Piano della v7 (documento di lavoro con i commenti di Desy) |
| `idee/` | Appunti e materiale di partenza: `idee-08-11-26.txt`, bozza della mappa `v7_bozza_mappa.svg`, nota vocale del 9/11 |
| `desy/` | File di Desy da integrare: `Carte_nuove_2026-11-05.xlsx` (98 carte, scala D20 da riportare ai 2D6) e `Il_Tesoro_del_Goblin_Analisi_Bilanciamento_Mostri_v4 test.xlsx` (workbook di bilanciamento dei mostri) |

Il playtest v7 è in produzione in `regolamento/` (specifica delle regole: `regolamento/Spec_v7.md`), `stampa/` (kit di stampa) e `simulatore/` (simulatore aggiornato alla v7).

**Desy:** i file nuovi vanno in `desy/`.

## Stato all'11/11 (sera): cosa è fatto e cosa resta

**Fatto**
- **Carte di Desy (D22):** le idee di `desy/Idee desi carte classi.ods` sono riscritte col tono goliardico. Ogni classe passa a 20 carte (XX-11…20) e il mazzetto è di 10 carte su 20. Il mazzo comune passa a 81 carte (TM-09, TE-26…31, TI-31…41). L'Oracolo ha 10 carte nuove. I nuovi Equipaggiamenti non hanno più la riga fissa «+1 AR finché…». La revisione ha aggiornato le formule del §14.5 e le tessere Stato (31).
- **Mappe:** la plancia base è la «Strettoie», con gli ostacoli spostati dai bordi verso le vie per le Cripte. Ogni carta Mappa ha la sua configurazione (`simulatore/plance/`). La regola R 8.12 dice: si gioca una Mappa, cambia la mappa e tutti tornano alla propria Partenza.
- **Mappa a tile (D23, 11/11, richiesta di Daniele):** la mappa si compone con tile esagonali generiche stampate a parte (25,2 mm, una linea di taglio per tile), più listelli per i muri e un pezzo a parte per la Sala del Tesoro. Le 10 configurazioni (base «Strettoie» + TM-01…09) sono preset con un foglio di istruzioni ciascuno; in playtest la mappa si può anche comporre liberamente, con i controlli del §17 come consiglio. Nel cambio di mappa (R 8.12) si sostituiscono solo le tile che differiscono. Le regole sono in `regolamento/Spec_v7.md` (D23, R 2.5, R 8.1, R 8.2, R 8.12, §17, §18, §19 N25–N26); regolamento e partita rapida sono aggiornati. Aperto: se comporre la mappa diventa regola ufficiale (N25) e se il cambio a metà partita è praticabile (N26). Il kit di stampa (tile, listelli, Sala del Tesoro, fogli dei preset) è un lavoro separato in `stampa/`.
- **Simulatore:** gestisce il cambio di plancia e il mazzetto 10 su 20, e ha gli effetti di tutte le carte nuove (`--verifica-carte` è pulito). Bilanciamento dell'11/11: gli Equipaggiamenti di classe nuovi danno difese a tema (AR contro LV 3+ o contro i boss); partita a 11,1/10,5/10,2 round (2/3/4 giocatori), scontri persi 23 % (dettagli in `simulatore/LEGGIMI.md`).
- **Docx:** regolamento e partita rapida sono aggiornati.
- **Illustrazioni (11/11):** tutte rifatte nello stile semplice (`stampa/sorgenti/arte/STILE.md`): tratto a mano sgangherato, pochi oggetti, sfondo di scena semplice, un tocco di steampunk medievale con alta magia. L'immagine fa capire cosa fa la carta ed è facile da ridisegnare per un illustratore. Ogni immagine passa da PhotoCraft (`arte/elabora.py`: grezza → `.pcraft` → PNG a 300 ppi, senza profilo ICC). Le carte sono impaginate «alla Magic»: immagine 54,5 × 38,1 mm con cornice, regole in corpo 7,8, battuta in corsivo in fondo sotto un filetto. La grafica vettoriale è leggera, con un tocco steampunk (bordi, retri, pedine, plance).
- **Tessere 3D (11/11):** `stampa/3d/`, esagoni incastrabili a passo reale 25,2 mm, muri con perni, STL e 3MF (tessera, muro, prova 3×3, piatto 20 + 8). Da provare in stampa; la carta va stampata al 90 % per entrare nella tasca.

**Da fare (in ordine)**
1. **Prova al tavolo:**
   - il bilanciamento: le righe «Se… LV 3 o più: AR» potrebbero rendere i mazzetti 2–3 troppo sicuri;
   - il cambio di mappa a metà partita (N26);
   - la composizione libera della mappa (N25).
2. **Tessere 3D:** stampare 3–4 tessere di prova e regolare `GIOCO` in `stampa/3d/genera_3d.py`. Se servono, aggiungere un PDF delle tessere al 90 % per le tasche.
3. **Terreni a tema:** le tessere PT-<TEMA>/PS-<TEMA> sono nel vecchio stile e non sono usate (la mappa usa le tessere generiche). Rifarle solo se si vogliono set a tema.
4. **Da confermare:**
   - TM-09 (Indizio con D6 ≤ LV + 2);
   - CS-19 conta come ritiro (lo blocca NE-47);
   - la chiusura senza vincitore di uno scontro durante un cambio di mappa;
   - le tessere Stato, una per fonte?
