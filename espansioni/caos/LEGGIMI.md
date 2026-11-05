# Il Caos del Goblin · Le Crepe di MIMI (espansione v2.0, 21/10 sera)

Busta senza classi nuove, esce dopo La Cittadella Bianca (scelta di Daniele) e funziona con ogni scatola.

- `Il_Caos_del_Goblin_stampa.pdf`: libretto A5 di 8 pagine con 3 mm di abbondanza (TrimBox impostato): copertina, storia, preparazione con la plancia e le coppie, Frugare o Attraversare con la tabella D6, i Coboldi di MIMI, le 6 carte Caos, domande frequenti con la Carta Aiuto, «Il Caos in numeri».
- Sorgente: `../../regolamento/sorgenti/book/caos.py` + `caos_misure.json` (testi delle carte, Coboldi, FAQ e numeri), poi, da `regolamento/sorgenti/book/`: `./mkpdf.sh caos.html $PWD/../../../espansioni/caos/Il_Caos_del_Goblin_stampa.pdf 154mm 216mm`.

## Componenti
- 10 tessere Crepa in 5 coppie gemelle (simmetriche a mezzo giro): A E1·F10, B J3·A8, C D3·G8, D H5·C6, E E5·F6. Con un Terreno restano solo A e B.
- 6 segnalini Coboldo di MIMI: 2 Coboldi (4 PV, +1, Difesa 10, Minaccia 9), 2 Frombolieri (3 PV, +2, Difesa 10, Agguato, 10), 2 Borseggiatori (4 PV, +1, Difesa 11, Borseggio, 11). Tutti D6 − 1.
- 6 carte Caos per il mazzo comune (CA-01…CA-06), 4 Carte Aiuto del Caos.

## Regole
- Su una Crepa: **frugare** (D6: 1 Crollo −2 PV, 2 Imboscata = gira un Coboldo, 3 Vento muovi ancora D6, 4 Bottega riprendi 1 carta, 5 Mappa perduta 1 Indizio, 6 Scambio) oppure **attraversare**: vai sulla Crepa gemella se è libera; il turno finisce lì.
- Chi batte un Coboldo prende 1 PE e pesca 1 carta, niente Indizio (i Coboldi non hanno pagine della mappa). Agguato: attacca per primo nel primo round. Borseggio: la prima volta che ti colpisce scarti 1 carta a caso; se lo batti peschi 1 carta in più.

| Carta | Testo | PP (2 giocatori) |
|---|---|---|
| CA-01 Biglia del nulla (Incantesimo) | Fruga in una Crepa da dove sei. Mago: tira due D6 e scegli. | +1,7 |
| CA-02 Pagina strappata (Incantesimo) | D6: con 5+ prendi 1 Indizio, altrimenti peschi 1 carta. Mago: basta un 4. | +3,1 |
| CA-03 Coboldo pentito (Incantesimo, scontro) | 3 danni al nemico. | +1,0 |
| CA-04 Lanterna dei Coboldi (Elmo) | +1 AR (Chierico: anche +1 ATT); frugando tiri due D6 e scegli. | +1,6 |
| CA-05 Vento di nulla (Incantesimo) | Un avversario a scelta, nel suo prossimo turno, muove di 1 esagono soltanto. | +2,7 |
| CA-06 Risata del Goblin (Incantesimo) | Tutti tirano il D6, tu due e tieni il più alto: il più alto prende 1 Indizio. | +2,9 |

## Misure (simulatore fisico, tempi da tavolo)
- Base senza Caos: 26,2 / 29,6 / 30,2 min con 2/3/4, classi 0,945–1,055.
- Con l'espansione: 25,9 / 29,5 / 30,7 min, classi 0,96–1,05 (2p 0,97–1,01; 3p 0,97–1,04; 4p, 70.000 partite, Guerriero 1,05, Ladro 1,02, Mago 0,97, Chierico 0,96).
- Dettagli e varianti scartate: `../../archivio/v1_21-10/simulazioni/espansione_caos.txt`. Modello: `../../archivio/v1_21-10/sorgenti/framework_fisico/caos_add.js` (`./caos.sh`).
