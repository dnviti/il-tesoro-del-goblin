# Officina del Goblin

Pagina web per creare i pezzi delle espansioni con le regole del framework di design
(https://claude.ai/artifact/1hHwQUccdsdVdJYvLzL4Y2).

- Versione pubblicata (con collezione condivisa e download): https://claude.ai/artifact/7spxxpK2XdGLC4ah9T33Dv
- `Officina_del_Goblin.html` + `motore.js`: copia locale. Il simulatore gira in un Web Worker, quindi la pagina va
  servita da un server (per esempio `python3 -m http.server` in questa cartella, poi http://localhost:8000/Officina_del_Goblin.html).
  Aperta con doppio clic funziona tutto tranne «Prova nel simulatore»; la collezione resta solo nel browser.

## Cosa fa
- **Carte**: prezzo in PP dal listino, budget per rarità, testo standard (schema Requisito · Quando · Effetto · Bersaglio · Durata · Specie),
  checklist, identità della classe; prova nel simulatore (2 giocatori, 4 classi della base, carta in mano all'eroe 1).
- **Nemici**: Minaccia, fascia, tratti, confronto con i 28 nemici della base, 20.000 scontri contro eroi di livello 1 e 3.
- **Eventi**: tabella D6 o set di segnalini «?», media in PP, esito peggiore, Indizi in giro, tempo al tavolo.
- **Terreni**: editor del Cuore 6×6 con specchio a mezzo giro (?, Cripta, Caos, bloccato, difficile, portali), distanze dalle 6 partenze,
  regole di bilanciamento; prova nel simulatore in 2 e 4 giocatori (durata, partenze, indice del Ladro).
  I ponti che cambiano a ogni giro non si provano qui: servono phys.js e boards.js in ../../v1_21-10/sorgenti/framework.
- **Collezione**: salvata nella pagina pubblicata; esporta carte nelle colonne del catalogo (CSV ;) e in formato cards.json
  (con gli effetti nel campo `officina`), nemici ed eventi in CSV, tutto in JSON (reimportabile).

## Ricostruire il motore
Dal 27/10 il motore è il gioco **Carte Trama v2**: `sorgenti/build_motore_v2.py` prende game.js, ui.js, cards_v2.json e nemici_v2.json
da ../gioco/sorgenti e aggiunge `sorgenti/tail_v2.js` (plancia con Terreno, carta nuova, API del worker). Se cambiano le regole del gioco:
`cd v2_27-10/officina/sorgenti && python3 build_motore_v2.py`, poi ripubblicare la pagina con il nuovo motore.js.
`sorgenti/wrun.js` esegue il motore in node (`node wrun.js '<messaggio JSON>' ../motore.js`), utile per misurare il listino.
I vecchi build_motore.py e tail.js (gioco del 21/10) restano solo come riferimento, in `../../v1_21-10/officina/sorgenti/`.

## Caos del Goblin come espansione (21/10 sera)
La plancia base non ha più Crepe. Nella scheda Terreni la casella «Con il Caos del Goblin» mostra le 4 Crepe esterne e le passa al simulatore
(`caos: true` nel messaggio al worker, `RUN.caos` in v1_21-10/officina/sorgenti/tail.js); sotto un Terreno le 6 Crepe del Cuore restano nella scatola.
Lo strumento «Caos o evento» ora si chiama «Evento del Terreno». Sacchetto base aggiornato: 13 creature, 4 mini-boss, 5 trappole, 8 sentieri (17 segnalini con Indizio).

## Il Caos del Goblin v2.0 (21/10 sera, versione 7 della pagina)
- Con la casella «Con il Caos del Goblin» (Terreni) o con una carta della serie «Il Caos del Goblin» (Carte) il simulatore usa l'espansione completa: Crepe gemelle (frugare o attraversare), 6 Coboldi di MIMI (chi li batte pesca 1 carta, niente Indizio), 6 carte Caos CA-01…CA-06 nel mazzo comune (`setCaos` in v1_21-10/officina/sorgenti/tail.js, stesso modello di v1_21-10/sorgenti/framework_fisico/caos_add.js).
- Eventi: esito nuovo «Scontro con un Coboldo di MIMI» (+1,5 PP, stima); riferimento delle Crepe +1,9 PP.

## Allineamento alle Carte Trama v2 (27/10)
- Regole del motore: per colpire D20 + ATT ≥ Difesa = 14 + AR (colpire è il 20% più difficile), danno D6 per gli eroi e dal livello per i nemici,
  5 PV di partenza (+2 PV o +1 statistica a ogni livello, Guerriero +2 PV), carte a inizio turno, in scontro e a fine turno, equipaggiamenti solo a inizio turno,
  4 classi base Guerriero, Ladro, Mago, Oracolo; specie Umano, Elfo, Nano, Orco, Sanguar.
- **Listino rimisurato** (8.000 + 8.000 partite in 2 giocatori per voce, rumore ±0,8 PP; elenco e risultati in sorgenti/pp/):
  Indizio 4 · prendi 1 Indizio a un avversario 4,5 · togli Indizio 0,5 · ogni avversario perde 1 turno 7 · turno extra 7,5 ·
  +1 ATT 5 (+2 ATT 8,6) · +1 AR 2,4 · +1 MOV 1,7 · +2 ATT o AR per uno scontro 0,4 · vantaggio 0,5 · PE 4 · Ispirazione 0,7 ·
  2 danni a un avversario 3,5 (1,7 a danno) · 2 danni al nemico 1 · perdi 1 turno −9,5 · perdi 1 PV −1,8.
  Ancora stime: +MOV per il turno, riprendere carte, cure, −AR al nemico (l'IA le usa male, la misura esce sotto zero).
- Nemici: Minaccia = 2·PV + ATT + 2·(Difesa − 14) + danno; fasce Nemico I LV 1 (4–11), Nemico I LV 2 (12–18), Nemico II (20–33),
  mini-boss (30–38), boss di MIMI (31–40). Scontri simulati contro eroi di livello 1 (6 PV, ATT 2, AR 1) e 3 (8 PV, ATT 3, AR 2).
- Eventi: sacchetto base 19 Nemici I, 6 Nemici II, 5 Trappole (25 segnalini con Indizio), media stimata +3,0 PP.
- Una carta di classe di un'espansione (Druido, Barbaro…) la prova un eroe della base: il motore v2 ha solo le 4 classi base.
