# Tutorial v5: come finire le voci (29/10/2026)

Serve una sessione con OPENROUTER_API_KEY nell'ambiente. La chiave non va mai scritta su file.

1. Estrai il pacchetto: `mkdir -p $SP && tar -xzf vid.tgz -C $SP/vid`, dove $SP è la tua cartella di lavoro.
2. In run_tut.sh correggi la variabile S, che deve puntare a $SP/vid.
3. Il mix della Taverna: estrai /mnt/project-files/«Taverna del Goblin Stems.zip» in una cartella vuota. Poi lancia `python3 -I mix_tav.py <cartella> $SP/vid/wavmix/tav_Mix.wav`.
4. Le clip ElevenLabs riusate (28) sono già in tts2/clips. Le 66 battute nuove sono elencate in tts2/new_idx.json.
5. Lancia `bash run_tut.sh`. Fa le voci (el.py, voci laura/brian/lily), poi durs_v2.json, tut.html, sayt.json, la musica tav_arr.wav e l'audio del tutorial.
6. Rendering: `PAGE=tut.html node render.js i/4 (i+1)/4 out/segI.mp4` per 4 segmenti, poi concat e mux con l'audio (AAC, loudnorm −18).
7. Copia per il web sotto i 20 MiB (720p). Aggiorna gli artefatti EFwVcGkSa4y46rLnLruHAj e HGeMCHTkz8CWw6GbmRqfqs; il video va caricato come asset.
8. Sostituisci video/tutorial_come_si_gioca.mp4 e avvisa il thread «Pubblicare il gioco su golgari».

Nota 29/10 ore 13: la chiave è un segreto di rete iniettato dal proxy, non una variabile. Lancia run_tut.sh con `OPENROUTER_API_KEY=sk-or-v1-dummy` (valore fittizio, il proxy mette quello vero). Funziona solo se tra i percorsi consentiti c'è /api/v1/audio/speech: prova prima con una battuta.
