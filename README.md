# Il Tesoro del Goblin

Gioco da tavolo fantasy in italiano di **Alessandro De Simone**: un gioco fisico in scatola, da 2 a 4 giocatori, con partite da 25–30 minuti. I giocatori esplorano le Terre di Hande (plancia a 10×10 esagoni), combattono mostri con soli dadi a 6 facce e cercano il forziere di MIMI.

## Versioni

Una cartella per ogni versione del gioco; ognuna ha il suo `LEGGIMI.md` con il contenuto e i comandi per rigenerare i file.

| Cartella | Data | Cosa è | Stato |
|---|---|---|---|
| `v1_21-10/` | 21/10/2026 | Prima versione con il D20: gioco HTML v1, regolamento v4.1, catalogo di 108 carte, simulazioni, espansione «Il Caos del Goblin», video «partita al tavolo» | archivio |
| `v2_27-10/` | 27/10/2026 | Carte Trama v2: gioco HTML v2, Officina del Goblin, catalogo e Carte Nemico, file originali dell'autore, sito pubblicato, simulazioni del 27/10 | archivio |
| `v5_02-11/` | 2/11/2026 | Regolamento v5 (soli D6) con sorgenti, bozza Word del 3/11, kit e regolamento del playtest del 5/11, patch applicate | archivio |
| `v6_08-11/` | 8/11/2026 | Playtest v6: regolamento e partita rapida, kit di stampa solo fronte A4 e A3, simulatore, punti aperti, file di Desy del 6/11 | playtest v6 attuale |
| `v7/` | dal 10/11/2026 | Piano della v7 (`v7/idee/v7_piano_TEMP.docx`), idee, file di Desy; playtest v7 in `v7/regolamento/`, `v7/stampa/`, `v7/simulatore/` | v7 in produzione |

**Desy:** i file nuovi (docx, xlsx…) vanno in `v7/desy/`.

La radice contiene solo questo file, `.gitignore` e le cartelle delle versioni. I file audio e video pesanti (wav, mp4, archivi) non sono nel repository: restano nella cartella del progetto.

## Come si rigenera (dalla radice del repo)

| Risultato | Comando | Strumenti |
|---|---|---|
| Carte del playtest v6 | `python3 v6_08-11/stampa/sorgenti/carte/genera_carte.py` (`--formato A3` per l'A3) | Python 3, designcraft-cli |
| Componenti del playtest v6 | `v6_08-11/stampa/sorgenti/componenti_gen/build.sh v6_08-11/stampa/sorgenti v6_08-11/stampa/playtest_v6` (A3: `… v6_08-11/stampa/sorgenti/A3 v6_08-11/stampa/playtest_v6_A3 A3`) | Python 3, vectorcraft-cli, pdfcraft-cli |
| Controllo dei PDF v6 | `python3 v6_08-11/stampa/sorgenti/verifica_pdf.py` (`--formato A3`) | Python 3, numpy, Pillow, poppler |
| Simulazione del playtest v6 | `python3 v6_08-11/simulatore/sim_playtest.py --esatto --partite 10000` | Python 3 |
| Gioco HTML v2 | `cd v2_27-10/gioco/sorgenti && python3 build.py && mv tesoro_del_goblin.html ../Il_Tesoro_del_Goblin_gioco_v2.html` | Python 3 |
| Motore dell'Officina | `cd v2_27-10/officina/sorgenti && python3 build_motore_v2.py` | Python 3 |
| Regolamento v5, «Inizia subito», libretto del Caos | da `v5_02-11/regolamento/sorgenti/book/`: vedi `v5_02-11/LEGGIMI.md` | Python 3, Node, Playwright, pypdf |

I file intermedi (`tesoro_del_goblin.html`, `check.js`, `*.tmp.pdf`, ecc.) sono esclusi da `.gitignore`.

## Formato di stampa

Il kit del playtest v6 si stampa al 100 % e **solo fronte**, un foglio per pagina, in A4 (`v6_08-11/stampa/playtest_v6/`) o A3 (`v6_08-11/stampa/playtest_v6_A3/`). Carte 63×88 mm (formato Magic) separate, ognuna con la sua abbondanza (2,5 mm in A4, 3 mm in A3), per tagliarle una alla volta con la dima. Come stampare: `v6_08-11/stampa/playtest_v6/ISTRUZIONI_DI_STAMPA.md`.
