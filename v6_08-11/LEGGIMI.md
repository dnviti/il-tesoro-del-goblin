# v6 — playtest v6 (8/11/2026, «v6-bis»)

**Playtest attuale.** Regolamento breve, partita rapida e kit di stampa **solo fronte** (A4 e A3) con le parti chiare del regolamento corretto di Desy del 6/11 e le decisioni dell'utente dell'8/11: turno in 3 passi (Muovi · Esplora · Fine), carte in qualsiasi momento del proprio turno, si colpisce con 2D6 + ATT ≥ AR del bersaglio (niente Difesa), Indizio dei mostri con il D6 ≤ LV, statistiche sulle rotelle di carta delle plance eroe (niente cubetti), tessere Stato e Usato (niente Clessidre), Carte Classe e Carte Specie.

| Percorso | Cosa è |
|---|---|
| `regolamento/` | `Regolamento_playtest_v6` e `Partita_rapida_v6` (docx sorgente e pdf da stampare). Vedi `regolamento/LEGGIMI.md` |
| `da_discutere/` | `Punti_aperti_v6` (docx e pdf): documento di lavoro con Desy, cartella temporanea |
| `stampa/` | Kit `playtest_v6/` (A4, 46 fogli) e `playtest_v6_A3/` (A3, 28 fogli) con istruzioni e ordine di stampa; `sorgenti/` (dati CSV, carte, componenti, controlli); `3d/` (dadi, pedine, contenitore). Vedi `stampa/LEGGIMI.md` |
| `simulatore/sim_playtest.py` | Collaudo del kit: probabilità esatte degli scontri e partite Monte Carlo; legge i CSV di `stampa/sorgenti/dati/` |
| `simulazioni/` | Risultati del simulatore dell'8/11 (`playtest_v6_2026-11-08.txt`, `ricompense_regolamento_corretto_2026-11-08.txt`) |
| `desy/` | File di Desy del 6/11: `Il_Tesoro_del_Goblin_Regolamento_corretto.docx` e `Partita_rapida_Il_Tesoro_del_Goblin.docx` |

## Come si rigenera (dalla radice del repository)

| Risultato | Comando | Strumenti |
|---|---|---|
| Carte | `python3 v6_08-11/stampa/sorgenti/carte/genera_carte.py` (A4), `... --formato A3` | Python 3, `designcraft-cli` |
| Componenti e prova di stampa | `v6_08-11/stampa/sorgenti/componenti_gen/build.sh v6_08-11/stampa/sorgenti v6_08-11/stampa/playtest_v6` (A4), `v6_08-11/stampa/sorgenti/componenti_gen/build.sh v6_08-11/stampa/sorgenti/A3 v6_08-11/stampa/playtest_v6_A3 A3` | Python 3, Pillow, `vectorcraft-cli`, `pdfcraft-cli` |
| Controllo dei PDF | `python3 v6_08-11/stampa/sorgenti/verifica_pdf.py` (A4), `... --formato A3` | Python 3, numpy, Pillow, poppler |
| Simulazione | `python3 v6_08-11/simulatore/sim_playtest.py --esatto --partite 10000 --uscita v6_08-11/simulazioni/<nome>.txt` | Python 3 |
| Regolamento e partita rapida | modificare il docx in `regolamento/` e riesportare il PDF dallo stesso file | WordCraft / Word |

Gli script trovano dati e cartelle di uscita dalla propria posizione; solo gli argomenti di `build.sh` e `--uscita` sono relativi alla cartella corrente.

## Percorsi di prima nei documenti di lavoro

I registri `stampa/sorgenti/dati/decisioni_provvisorie.md` e `dati_stampa.md`, la colonna `nota` dei CSV e i file in `simulazioni/` sono storici e citano i percorsi di prima del 10/11/2026 (non corretti). Corrispondenze:

| Prima | Ora |
|---|---|
| `stampa/` | `v6_08-11/stampa/` |
| `regolamento/playtest/`, `regolamento/da_discutere/` | `v6_08-11/regolamento/`, `v6_08-11/da_discutere/` |
| `gioco/sorgenti/sim_playtest.py` | `v6_08-11/simulatore/sim_playtest.py` |
| `simulazioni/…_2026-11-08.txt` | `v6_08-11/simulazioni/` |
| `regolamento/` (PDF v5, bozza del 3/11), `regolamento/sorgenti/` | `v5_02-11/regolamento/` |
| `archivio/v5_05-11/` | `v5_02-11/playtest_05-11/` |
| `carte/`, `gioco/`, `officina/` | `v2_27-10/` (`Carte_nuove_2026-11-05.xlsx` in `v7/desy/`) |
| file di Desy nella radice | `v6_08-11/desy/` (il workbook v4 in `v7/desy/`) |
