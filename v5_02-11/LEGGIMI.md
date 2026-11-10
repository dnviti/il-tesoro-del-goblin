# v5 — regolamento v5 (2/11/2026) e playtest del 5/11

**Archivio.** Regolamento v5 con le Carte Trama v2: soli D6, sacchetto a due colori (25 tessere rosse Mostro, 11 blu Imprevisto), mostri in 3 mazzetti per livello, mano di 5 carte di classe + 5 comuni, Difesa. Contiene anche la bozza Word del 3/11 con i commenti dell'autore e il kit di playtest del 5/11. È stato sostituito dal playtest v6 dell'8/11 (`../v6_08-11/`).

| Percorso | Cosa è |
|---|---|
| `regolamento/Regolamento_base_v5_stampa_regolamento_errato.pdf`, `regolamento/Inizia_subito_v5_stampa.pdf` | Regolamento base v5 (A5) e «Inizia subito» impaginati; hanno ancora Guerriero, Mago, Ladro: non distribuirli al tavolo |
| `regolamento/Regolamento_Tesoro_del_Goblin_bozza.docx` | Bozza Word del 3/11: testo del 2/11 più note e commenti dell'autore (Assaltatore, Stregone, Ricercatore, Oracolo; specie Yumaniano; iniziativa a 1D6); punti aperti in giallo |
| `regolamento/sorgenti/` | Sorgenti del regolamento: `book/` (Python → HTML → PDF, anche il libretto del Caos), `docx/` (HTML → Word), `fonts/`. Vedi `regolamento/sorgenti/LEGGIMI.md` |
| `playtest_05-11/regolamento/` | Regolamento di playtest del 5/11 (docx e pdf) |
| `playtest_05-11/stampa/playtest_v5/`, `playtest_05-11/stampa/playtest_v5_A3/` | Kit v5 in A4 (12 PDF) e A3 (10 PDF) con le istruzioni di stampa; in A3 c'è anche `gioco-da-tavolo.zip` (non nel repository: `*.zip` è in `.gitignore`) |
| `patch_applicate/regolamento/` | `patch_v2_regole.py`, `patch_mano_reg.py`, `patch_2d6_reg.py`: patch ai sorgenti del regolamento già applicate; rilanciate falliscono sugli assert. Solo documentazione |
| `simulazioni/playtest_2026-11-05.txt` | Collaudo del kit del 5/11 (regole v5) |
| `video/lavoro_tutorial_v5/` | Istruzioni per finire le voci del tutorial v5 (29/10) |

## Come si rigenera

Da `v5_02-11/regolamento/sorgenti/book/`:

```
python3 build.py && python3 inizia.py && python3 caos.py
./mkpdf.sh regolamento.html $PWD/../../Regolamento_base_v5_stampa_regolamento_errato.pdf 154mm 216mm
./mkpdf.sh inizia.html $PWD/../../Inizia_subito_v5_stampa.pdf 216mm 303mm
./mkpdf.sh caos.html $PWD/../../../../v1_21-10/espansioni/caos/Il_Caos_del_Goblin_stampa.pdf 154mm 216mm
```

Servono Python 3, Node con Playwright e pypdf. Bozza Word: `regolamento/sorgenti/LEGGIMI.md` (la pipeline non rifà la copia del 3/11 con i commenti dell'autore).

## Percorsi noti rotti (non corretti, versione archiviata)

- I PDF del kit v5 si possono rifare solo dal commit precedente alla v6: i sorgenti del kit sono stati modificati sul posto e oggi sono in `../v6_08-11/stampa/sorgenti/`.
- `playtest_05-11/stampa/playtest_v5/ISTRUZIONI_DI_STAMPA.md` e `playtest_v5_A3/ISTRUZIONI_DI_STAMPA_A3.md`: i link al regolamento (`../../regolamento/playtest/…`, ora `../../regolamento/`), a `../3d/LEGGIMI.md` (ora `../v6_08-11/stampa/3d/`) e i comandi di rigenerazione (`stampa/sorgenti/…`) puntano ai percorsi di prima.
- `simulazioni/playtest_2026-11-05.txt` cita `stampa/sorgenti/dati/*.csv` e non si riproduce più con il simulatore attuale (`../v6_08-11/simulatore/sim_playtest.py`).
