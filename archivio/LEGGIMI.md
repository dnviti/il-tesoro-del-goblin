# Archivio

Materiale non più attuale, tenuto per consultazione e per la storia del progetto. Non fa parte del gioco, del regolamento o dei materiali di stampa correnti.

## v5_05-11/: kit e regolamento di playtest del 5/11/2026

Il kit di stampa v5 e il regolamento breve di playtest del 5/11 (con le correzioni del collaudo e lo schema delle carte con abbondanza del 6/11). Sono stati **sostituiti dalla v6 dell'8/11/2026**: `../regolamento/playtest/Regolamento_playtest_v6.docx` e il kit `../stampa/playtest_v6/` (A4) e `../stampa/playtest_v6_A3/` (A3). Cosa cambia nella v6: `../stampa/sorgenti/dati/decisioni_provvisorie.md`, sezione 7 (turno in 4 passi senza il passo «Carte», carte ed Equipaggiamenti in qualsiasi momento del proprio turno, Indizio dei mostri solo con D6 ≤ LV del mostro).

| Percorso | Cosa è |
|---|---|
| `regolamento/Regolamento_playtest.docx`, `regolamento/Regolamento_playtest.pdf` | Regolamento di playtest del 5/11 (prima in `regolamento/playtest/`) |
| `stampa/playtest_v5/` | Kit v5 A4: 12 PDF (carte, plancia, schede, tessere, segnalini, pedine, prova di stampa) e `ISTRUZIONI_DI_STAMPA.md` |
| `stampa/playtest_v5_A3/` | Lo stesso kit su A3: 10 PDF e `ISTRUZIONI_DI_STAMPA_A3.md`; c'è anche `gioco-da-tavolo.zip` (non nel repository: `*.zip` è in `.gitignore`) |

I sorgenti non sono stati copiati: i PDF v5 si possono rifare solo dal commit precedente alla v6 (i sorgenti in `../stampa/sorgenti/` sono stati modificati sul posto). Cose note, non corrette perché archiviate: i link relativi dentro le istruzioni di stampa (regolamento, `../3d/LEGGIMI.md`, comandi di rigenerazione) puntano ancora ai percorsi di prima dello spostamento.

## v1_21-10/: la prima versione (21/10/2026)

È la prima versione giocabile del gioco: **regole con il D20**, catalogo di 108 carte (più 6 carte Caos), Difesa 10 + AR, regolamento v4.1 «da tavolo». È stata sostituita dalle 72 Carte Trama v2 (27/10) e dal regolamento v5 con i soli D6 (2/11). Si conserva perché è il modello dell'espansione Caos (`sorgenti/framework_fisico/caos_add.js`) e dei suoi risultati.

| Percorso | Cosa è |
|---|---|
| `Il_Tesoro_del_Goblin_gioco_v1.html` | Gioco HTML v1 (uscita di `sorgenti/build.py`, identica byte per byte) |
| `Regolamento_base_v4.1_stampa.pdf`, `Inizia_subito_v4.1_stampa.pdf` | Regolamento e «Inizia subito» v4.1 (D20), sostituiti dai PDF v5 in `../regolamento/` |
| `Catalogo_carte_Tesoro_del_Goblin.xlsx`, `carte_tesoro_goblin.csv` | Catalogo carte v1 (sostituito da `../carte/Catalogo_carte_v2.xlsx`) |
| `sorgenti/` | Motore, interfaccia, `cards.json` (108 carte), `build.py`, simulatori, script una tantum (`newtexts*.py`, `caos_patch.py`), `framework/` e `framework_fisico/` (modello della scatola fisica e dell'espansione Caos), `regolamento_stampa/` (sorgenti del regolamento v4.1). Vedi `sorgenti/LEGGIMI.md` |
| `simulazioni/` | Risultati delle simulazioni v1, tra cui `partite_20000_regole_standard.csv` (dati grezzi, 664 KB) |
| `officina/sorgenti/` | `build_motore.py` e `tail.js`: il motore dell'Officina del 21/10, sostituito da `build_motore_v2.py` |

Tutto parte da `sorgenti/`: i percorsi relativi dentro ogni cartella restano validi (`python3 build.py` in `sorgenti/` ricostruisce il gioco v1). I comandi scritti nei file di questa cartella (per esempio `cd sorgenti/framework_fisico` nelle simulazioni) sono relativi a `archivio/v1_21-10/`.

Cose note, non corrette perché archiviate:
- `sorgenti/xlsx_update.py:4` e `sorgenti/xlsx_caos.py` usano percorsi assoluti vecchi (`/mnt/project-files/…`) o il nome del file nella cartella corrente.
- `officina/sorgenti/build_motore.py` fallisce già sul commit precedente alla ristrutturazione (un assert sul game.js v1 non trova più il testo da sostituire).
- `officina/sorgenti/tail.js` e `sorgenti/regolamento_stampa/book/caos.py` hanno commenti con i percorsi della struttura vecchia.
- `sorgenti/newtexts*.py`, `caos_patch.py` e `framework/patch_carte_21-10.py` sono script una tantum già applicati: non idempotenti.

## patch_applicate/regolamento/

`patch_v2_regole.py`, `patch_mano_reg.py`, `patch_2d6_reg.py`: patch ai sorgenti del regolamento (`regolamento/sorgenti/book/`: build.py, inizia.py, parts.py) già applicate sul posto. Il codice attuale le contiene già; rilanciate falliscono sugli assert. Si conservano come documentazione di cosa è cambiato.
