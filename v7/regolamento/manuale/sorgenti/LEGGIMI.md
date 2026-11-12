# Rigenerare il manuale

1. Il testo viene da `../testo_manuale.md` (sezioni «Pagina 1–5»), gli schemi da `../schemi/`, le illustrazioni grezze da `../immagini/grezze/`; servono `designcraft-cli`, `photocraft-cli`, `python3` e `jq`.
2. `./measure.sh` misura i blocchi di testo e aggiorna `heights.json`; se il testo cambia molto, lancialo due volte.
3. `./images.sh` ritaglia le illustrazioni alle misure dell'impaginato in `../immagini/png/` (260 ppi).
4. `./publish.sh` ricostruisce `../Manuale_Il_Tesoro_del_Goblin.designcraft`, fa il preflight, esporta `_PDFX1a.pdf` (tipografia, validato) e `_stampa_A4.pdf` (casa) e aggiorna `../anteprime/`.
5. L'impaginazione (griglia, stili, posizioni) sta tutta in `genera.py`; le pagine sono le funzioni `page1()`…`page5()`.
