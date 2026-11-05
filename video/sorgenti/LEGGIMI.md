Sorgenti del video «partita al tavolo» (21/10/2026).
- page.html: motore di animazione + copione (funzioni beat()).
- gen.py: crea index.html inserendo la plancia da ../../regolamento/sorgenti/book/svg.py (serve la cartella fonts/ di regolamento/sorgenti accanto). Attenzione: i percorsi scritti in gen.py:2 e gen_tut.py:2 sono assoluti e già rotti (`/tmp/claude-0/…/scratchpad/reg/book` e `/mnt/project-files/tesoro-goblin/v2/regolamento_stampa/book`): vanno puntati a `regolamento/sorgenti/book` prima di usarli (non corretti nella ristrutturazione).
- render.js: NODE_PATH=$(npm root -g) node render.js 0 1 out.mp4 (Playwright -> ffmpeg, 25 fps). Si può dividere in 4 parti (0 .25, .25 .5 ...) e unire con ffmpeg concat.
- snap.js: fotogrammi di controllo (node snap.js 40 75 ...).
- Tutorial: python3 gen.py && python3 gen_tut.py (crea tut.html), poi PAGE=tut.html node render.js 0 1 tutorial.mp4. Per la pagina serve una copia sotto 20 MB (crf 27).
- Il primo fotogramma deve mostrare la copertina; aggiungere traccia audio muta (anullsrc) e -movflags +faststart.

Aggiornamento 27/10/2026 (regolamento v5, Carte Trama v2)
- Partita: copione in copione_v2.js (patch_page_v2.py lo inserisce in page.html). gen.py usa la plancia di regolamento/sorgenti/book. Musica: musica_suno/mix_mimi.py somma gli stem di «In cerca di MIMI» (zip in project files), poi build.py con taglio e durata letti da MG.cut e TOTAL (cuts_v2.sh).
- Tutorial: tut_script_v2.js (16 lezioni, 94 battute) e gen_tut.py (usa ../tts/durs_v2.json se c'è). Le righe parlate sono in lines_v2.json. Il testo per la voce sta in audio/tutorial_v2/norm.json, e le battute da generare sono in new_idx.json. Le altre riusano clips_elevenlabs con lo stesso testo.
