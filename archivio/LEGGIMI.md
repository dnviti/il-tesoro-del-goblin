# Archivio

Materiale non più attuale, tenuto per consultazione e per la storia del progetto. Non fa parte del gioco, del regolamento o dei materiali di stampa correnti.

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
