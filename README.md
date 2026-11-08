# Il Tesoro del Goblin

Gioco da tavolo fantasy in italiano di **Alessandro De Simone**: un gioco fisico in scatola, da 2 a 4 giocatori, con partite da 25–30 minuti. I giocatori esplorano le Terre di Hande (plancia a 10×10 esagoni), combattono mostri con soli dadi a 6 facce e cercano il forziere di MIMI.

## Versione attuale

- **Regole:** Regolamento **v5** (2/11/2026, Carte Trama v2): soli D6, sacchetto a due colori (25 tessere rosse Mostro, 11 blu Imprevisto), mostri in 3 mazzetti per livello, mano di 5 carte di classe + 5 comuni. Nel playtest v6 (sotto) si colpisce con 2D6 + ATT ≥ AR del bersaglio: la Difesa del v5 non esiste più.
- **Testo più recente:** `regolamento/Regolamento_Tesoro_del_Goblin_bozza.docx` (bozza Word del 3/11/2026: il testo del 2/11 più le note e i commenti dell'autore): classi Assaltatore, Stregone, Ricercatore, Oracolo; specie Umano, Elfo, Sanguar, Yumaniano (8 tessere); iniziativa a 1D6. I punti ancora aperti sono evidenziati in giallo nel documento; le regole decise nei commenti (pareggio, 3 Indizi, Forte Volontà, Incanto, niente critici) sono già nel kit di `stampa/`. Il PDF `Regolamento_base_v5_stampa_regolamento_errato.pdf` è l'ultima versione impaginata e conserva i nomi precedenti (Guerriero, Mago, Ladro).
- **Playtest v6 (8/11/2026):** regolamento breve `regolamento/playtest/Regolamento_playtest_v6.pdf` (11 pagine), partita rapida `regolamento/playtest/Partita_rapida_v6.pdf` e kit `stampa/playtest_v6/` (A4, 46 fogli) e `stampa/playtest_v6_A3/` (28 fogli), **tutto solo fronte**. Contiene le parti chiare del regolamento corretto di Desy del 6/11 e le decisioni dell'8/11: turno in 3 passi (Muovi · Esplora · Fine), carte in qualsiasi momento del proprio turno, Indizio dei mostri con il D6 (≤ LV del mostro), statistiche sulle rotelle di carta delle plance eroe (niente cubetti), tessere Stato e Usato (niente Clessidre), Carte Classe e Carte Specie. Le domande ancora aperte sono in `regolamento/da_discutere/Punti_aperti_v6.docx`; il kit e il regolamento playtest del 5/11 sono in `archivio/v5_05-11/`.
- **Attenzione:** il gioco HTML (`gioco/`) e il motore dell'Officina sono ancora fermi alle regole con il D20: la patch `gioco/sorgenti/patch_2d6.py` non è stata applicata. Lo stesso vale per il foglio «Leggimi» del catalogo carte e per la colonna `difesa` di `nemici_v2.json`. Per le regole fa fede il regolamento, non il gioco HTML.
- La prima versione (21/10/2026, regole con il D20) è in `archivio/`.

## Cosa c'è qui

| Cartella | Contenuto | Stato |
|---|---|---|
| `regolamento/` | Regolamento di playtest v6 e partita rapida v6 (`playtest/`), documento dei punti aperti (`da_discutere/`), regolamento base v5 e «Inizia subito» v5 in PDF, bozza Word del 3/11. `sorgenti/` = come si generano (book/, docx/, fonts/) | attuale (playtest v6) |
| `carte/` | Catalogo carte v2 (xlsx), Carte Nemico v2 (pptx), `originali/` con i file dell'autore (Carte Trama, elenco, layout Nemico; `Carte_nuove_2026-11-05.xlsx`, nuovo elenco delle carte comuni, aggiornato 5/11 sera: aggiunto foglio poteri di classe; `Bestiario_test_2026-10-28.xlsx`, bestiario di prova sulla scala D20). I due xlsx nuovi sono proposte: non sono nel kit di stampa | attuale |
| `gioco/` | Gioco giocabile in un solo file HTML (`Il_Tesoro_del_Goblin_gioco_v2.html`). `sorgenti/` = motore, dati delle carte, strumenti | attuale (regole D20, vedi sopra) |
| `officina/` | «Officina del Goblin», strumento per progettare carte ed espansioni, con il motore del simulatore | attuale |
| `simulazioni/` | Risultati delle simulazioni di bilanciamento sulle Carte Trama v2 (27/10) | attuale |
| `espansioni/caos/` | Espansione «Il Caos del Goblin» (Le Crepe di MIMI): libretto PDF e LEGGIMI | pensata sulle regole del 21/10 |
| `stampa/` | Materiali stampabili per il playtest (vedi `stampa/LEGGIMI.md`; come stampare: `stampa/playtest_v6/ISTRUZIONI_DI_STAMPA.md`; elenco da stampare: `stampa/playtest_v6/ordine_di_stampa.txt`; prova di stampa: `stampa/playtest_v6/00_prova_stampa.pdf`) | pronto per la stampa (playtest v6) |
| `pubblicazione/` | Pagina d'ingresso e istruzioni del sito pubblicato | attuale |
| `video/` | Script e pagine per i video (senza audio e video finiti) | misto |
| `archivio/` | Prima versione (21/10, `v1_21-10/`), kit e regolamento playtest del 5/11 (`v5_05-11/`, sostituiti dalla v6 dell'8/11) e patch già applicate (`patch_applicate/`). Vedi `archivio/LEGGIMI.md` | archivio |

La radice contiene solo questo file e `.gitignore`.

I file audio e video pesanti (wav, mp4, archivi) non sono nel repository: restano nella cartella del progetto.

## Come si rigenera ogni file

Ogni area tiene i risultati in cima e i sorgenti in `sorgenti/`. Dettagli nei LEGGIMI delle singole cartelle.

| Risultato | Comando (dalla radice del repo) | Strumenti |
|---|---|---|
| Gioco HTML | `cd gioco/sorgenti && python3 build.py && mv tesoro_del_goblin.html ../Il_Tesoro_del_Goblin_gioco_v2.html` | Python 3 |
| Dati delle carte (`cards_v2.json`, `nemici_v2.json`) | `cd gioco/sorgenti && python3 dati_v2.py` | Python 3 |
| Catalogo carte v2 | `cd gioco/sorgenti && python3 xlsx_v2.py ../../carte/Catalogo_carte_v2.xlsx` | Python 3, openpyxl |
| Carte Nemico | `cd gioco/sorgenti && python3 mknem.py <layout.pptx> <nemici.json> ../../carte/Carte_Nemico_v2.pptx` (vedi `gioco/sorgenti/LEGGIMI.md`) | Python 3, python-pptx |
| Motore dell'Officina | `cd officina/sorgenti && python3 build_motore_v2.py` | Python 3 |
| HTML del regolamento e di «Inizia subito» | `cd regolamento/sorgenti/book && python3 build.py && python3 inizia.py` | Python 3 |
| PDF del regolamento (A5) e «Inizia subito» | `./mkpdf.sh regolamento.html $PWD/../../Regolamento_base_v5_stampa_regolamento_errato.pdf 154mm 216mm` e `./mkpdf.sh inizia.html $PWD/../../Inizia_subito_v5_stampa.pdf 216mm 303mm` (da `regolamento/sorgenti/book`) | Node, Playwright, Python 3, pypdf |
| Bozza Word | vedi `regolamento/sorgenti/LEGGIMI.md` | Node, Playwright, docx, Python 3 |
| Libretto del Caos | `cd regolamento/sorgenti/book && python3 caos.py && ./mkpdf.sh caos.html $PWD/../../../espansioni/caos/Il_Caos_del_Goblin_stampa.pdf 154mm 216mm` | come sopra |

I file intermedi (`tesoro_del_goblin.html`, `check.js`, `*.tmp.pdf`, ecc.) sono esclusi da `.gitignore`.

## Formato di stampa

Materiali di playtest in `stampa/` in A4 (`playtest_v6/`) e A3 (`playtest_v6_A3/`), da stampare al 100 % e **solo fronte**, un foglio per pagina; le carte coperte hanno i dorsi in PDF separati (`carte_*_retri.pdf`), da ritagliare e incollare o imbustare con i fronti. Carte 63×88 mm (formato Magic) separate, ognuna con la sua abbondanza (2,5 mm in A4, 3 mm in A3), per tagliarle con la dima: linee di taglio a ≥ 5,5 mm dal bordo del foglio. Gli altri componenti hanno contenuto e tacche a ≥ 6 mm dal bordo. Il regolamento base v5 impaginato è A5 (154×216 mm con 3 mm di abbondanza, TrimBox impostato) e «Inizia subito» 216×303 mm; regolamento e partita rapida del playtest sono A4.
