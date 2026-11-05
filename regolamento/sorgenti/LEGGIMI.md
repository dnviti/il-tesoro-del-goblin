# Sorgenti del regolamento (v5, Carte Trama v2)

Risultati, un livello sopra: `../Regolamento_base_v5_stampa.pdf` (A5 154×216 mm, 16 pagine), `../Inizia_subito_v5_stampa.pdf` (216×303 mm, 2 pagine), `../Regolamento_Tesoro_del_Goblin_bozza.docx` (bozza Word del 3/11/2026). Il libretto dell'espansione Caos si genera da qui ma finisce in `../../espansioni/caos/`.

Contenuto: `book/` (Python → HTML → PDF), `docx/` (HTML → Word), `fonts/` (Alegreya e Cinzel, con `fonts.css`).

I PDF riflettono **la v5 impaginata**, con i nomi di classe precedenti (Guerriero, Mago, Ladro). La bozza Word contiene i cambiamenti successivi (Assaltatore, Stregone, Ricercatore; specie Yumaniano; iniziativa a 1D6), ma **non è stata riportata in `book/`**: i sorgenti `book/*.py` e gli HTML generati sono ancora quelli v5.

## PDF (regolamento, Inizia subito, Caos)

Da `book/`:

```
python3 build.py && python3 inizia.py && python3 caos.py     # scrivono regolamento.html, inizia.html, caos.html
./mkpdf.sh regolamento.html $PWD/../../Regolamento_base_v5_stampa.pdf 154mm 216mm
./mkpdf.sh inizia.html $PWD/../../Inizia_subito_v5_stampa.pdf 216mm 303mm
./mkpdf.sh caos.html $PWD/../../../espansioni/caos/Il_Caos_del_Goblin_stampa.pdf 154mm 216mm
```

- `mkpdf.sh <html> <pdf con percorso assoluto> <larghezza> <altezza>` stampa con Playwright (`render.js`, serve `NODE_PATH=$(npm root -g)`, già impostato dallo script) e imposta i box TrimBox a 3 mm con pypdf.
- Gli HTML sono tracciati e coincidono con quanto rigenerano i tre script (verificato il 5/11/2026).
- `parts.py` (componenti: schede eroe, tessere, striscia del turno…) e `svg.py` (plancia, icone) sono usati da tutti e tre, e anche dagli script dei video.
- `caos_misure.json`: testi delle carte, Coboldi, FAQ e numeri del libretto Caos.

Nota sui font: in `fonts/` `Alegreya-normal-700` è uguale a `-400` e `Cinzel-normal-800` a `-600`. Non esistono file bold veri, quindi il grassetto nei PDF è sintetizzato.

## Bozza Word

Pipeline, da lanciare nell'ordine indicato (serve Node con Playwright e il pacchetto `docx`, più Python 3):

1. Da questa cartella (`regolamento/sorgenti/`): `python3 docx/edit_html.py` legge `book/regolamento.html`, applica le modifiche della bozza e scrive `docx/reg_docx.html`.
2. Da `docx/`: `mkdir -p img && node extract.js` apre `reg_docx.html`, salva le figure in `img/` e il testo in `blocks.json`.
3. Da `docx/`: `node build.js` scrive `docx/Regolamento_Tesoro_del_Goblin_bozza.docx` (con la pagina dei punti da confermare). Per aggiornare il risultato si copia il file in `../` (cioè `regolamento/`).

La copia in `regolamento/` è la bozza del **3/11**: il file prodotto da questa pipeline (2/11) con le note e i 14 commenti aggiunti a mano dall'autore. La pipeline non la rigenera: rilanciarla e copiare il risultato cancellerebbe le note dell'autore.

`reg_docx.html`, `blocks.json` e `img/` sono intermedi, esclusi da `.gitignore`. `edit_html.py` parte sempre da `book/regolamento.html` (v5) e fallisce sugli assert se quel testo è cambiato.

## Patch già applicate

`patch_v2_regole.py`, `patch_mano_reg.py` e `patch_2d6_reg.py`, che avevano modificato `book/build.py`, `inizia.py` e `parts.py`, sono in `../../archivio/patch_applicate/regolamento/`. Falliscono se rilanciate (le modifiche sono già nel codice).
