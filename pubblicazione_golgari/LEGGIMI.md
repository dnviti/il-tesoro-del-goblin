# Il Tesoro del Goblin su golgari

Indirizzo pubblico: https://snz82syu.fn.oyd.ovh (pubblicato il 27/10/2026)

- Cliente golgari «Daniele Viti» (id 5, interno: costi non fatturati), namespace cust-daniele-viti.
- Servizio serverless `tesoro-goblin`, scala a zero (0–1 istanze), 100m CPU, 128 MiB, immagine pubblica `sigoden/dufs:v0.46.0` (server di file statici), porta 5000.
- Volume HDD 1 GiB `tesoro-goblin-data` montato in /data: contiene i file del sito. Stima 0,12 €/mese.
- Ora in **sola lettura** (env solo `DUFS_RENDER_TRY_INDEX=true`).

## Struttura
- `index.html` (pagina d'ingresso, sorgente in questa cartella)
- `gioco/index.html` = v2/Il_Tesoro_del_Goblin_gioco_v2.html
- `officina/index.html` + `motore.js` = officina/
- `regolamenti/` Regolamento_base_v5.pdf, Inizia_subito_v5.pdf, Il_Caos_del_Goblin.pdf
- `risorse/` Catalogo_carte_v2.xlsx, Carte_Trama_Il_Tesoro_del_Goblin_v2.pptx, Carte_Trama_Elenco_v2.xlsx, Carte_Nemico_v2.pptx
- `video/` partita_al_tavolo.mp4, tutorial_come_si_gioca.mp4

## Aggiornare i file
1. function_preview su tesoro-goblin con env in più: `DUFS_ALLOW_UPLOAD=true`, `DUFS_ALLOW_DELETE=true`,
   `DUFS_AUTH=caricatore:<password nuova casuale>@/:rw|@/`; mostrare l'anteprima a Daniele, poi plan_apply.
2. `curl -u caricatore:<pw> -T file https://snz82syu.fn.oyd.ovh/<percorso>` (cartelle nuove con `-X MKCOL`).
3. Di nuovo function_preview con env solo `DUFS_RENDER_TRY_INDEX=true` (sola lettura), anteprima, plan_apply.

## Storico
- 27/10 22:28: prima pubblicazione (revisioni 1–2).
- 27/10 23:40: ricaricati gioco v2, Officina v2, regolamenti v5, catalogo, Carte Nemico e video della partita rifatto (revisioni 3–4). Il tutorial è ancora quello del 21/10: da ricaricare quando il thread delle Carte Trama lo rifà.
- Ogni ciclo scrittura/sola lettura crea 2 revisioni e usa Service della quota (30 su 40 dopo il secondo ciclo); Knative elimina le revisioni vecchie dopo 48 ore.
- 29/10 10:30: autore corretto in Alessandro De Simone (pagina d'ingresso, gioco, motore dell'Officina, 3 PDF, catalogo, video della partita), revisioni 5–6. La revisione 5 al primo colpo ha avuto un errore 500 di Docker Hub nello scaricare l'immagine, poi è partita da sola.
