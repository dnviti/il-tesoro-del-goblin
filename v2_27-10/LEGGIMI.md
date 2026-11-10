# v2 — Carte Trama v2 (27/10/2026)

**Archivio.** Le 72 Carte Trama v2 dell'autore con il gioco giocabile in HTML, l'«Officina del Goblin» (strumento per progettare carte ed espansioni con il motore del simulatore) e il sito pubblicato il 27/10. Gioco HTML, Officina e catalogo sono ancora sulla scala D20 (la patch `gioco/sorgenti/patch_2d6.py` non è stata applicata): per le regole fanno fede il regolamento v5 (`../v5_02-11/`) e il playtest v6 (`../v6_08-11/`).

| Percorso | Cosa è |
|---|---|
| `gioco/Il_Tesoro_del_Goblin_gioco_v2.html` | Gioco giocabile in un solo file HTML |
| `gioco/sorgenti/` | Motore, interfaccia, dati delle carte (`cards_v2.json`, `nemici_v2.json`), patch, simulatore D20. Vedi `gioco/sorgenti/LEGGIMI.md` |
| `officina/` | Officina del Goblin (`Officina_del_Goblin.html`, `motore.js`, `sorgenti/`). Vedi `officina/LEGGIMI.md` |
| `carte/` | Catalogo carte v2 (xlsx), Carte Nemico v2 (pptx); `originali/` con i file dell'autore: Carte Trama v2 (pptx), elenco (xlsx), layout Nemico (pptx), `Bestiario_test_2026-10-28.xlsx` (bestiario di prova sulla scala D20) |
| `pubblicazione/` | Pagina d'ingresso e istruzioni del sito pubblicato su golgari |
| `simulazioni/` | Risultati delle simulazioni di bilanciamento sulle Carte Trama v2 (27/10 e prove su Difesa 14 e PV 5) |

## Come si rigenera (dalla radice del repository)

| Risultato | Comando | Strumenti |
|---|---|---|
| Gioco HTML | `cd v2_27-10/gioco/sorgenti && python3 build.py && mv tesoro_del_goblin.html ../Il_Tesoro_del_Goblin_gioco_v2.html` | Python 3 |
| Dati delle carte | `cd v2_27-10/gioco/sorgenti && python3 dati_v2.py` | Python 3 |
| Catalogo carte v2 | `cd v2_27-10/gioco/sorgenti && python3 xlsx_v2.py ../../carte/Catalogo_carte_v2.xlsx` | Python 3, openpyxl |
| Carte Nemico | `cd v2_27-10/gioco/sorgenti && python3 mknem.py <layout.pptx> <nemici.json> ../../carte/Carte_Nemico_v2.pptx` (vedi `gioco/sorgenti/LEGGIMI.md`) | Python 3, python-pptx |
| Motore dell'Officina | `cd v2_27-10/officina/sorgenti && python3 build_motore_v2.py` | Python 3 |

I percorsi relativi tra `gioco/`, `officina/` e `carte/` sono rimasti quelli di prima: i comandi funzionano dalla cartella indicata.
