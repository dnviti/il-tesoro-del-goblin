# Rifare le voci del tutorial

Nota (ristrutturazione): gen.py:2 e gen_tut.py:2 in video/ puntano a `/mnt/project-files/tesoro-goblin/sorgenti/regolamento_stampa/book`, percorso assoluto già rotto. Gli stessi sorgenti ora sono in `v1_21-10/sorgenti/regolamento_stampa/book` (non corretti).

Le cartelle replicano lo scratchpad del thread "Video partita al tavolo": video/ tts/ music/ suno/ devono stare affiancate (gli script usano ../tts, ../music, ../suno).

1. tts/norm.json = 102 battute [chi, testo] in ordine (L Lia, M Marco, G Giulia), già normalizzate per la lettura (D20 "di venti", PV "pi vu"...). Il testo originale con <b> è in video/tut_script.js (say()).
2. Genera le clip in tts/clips/v000.wav ... v101.wav (mono 48 kHz, loudnorm -18 LUFS come in tts/gen.py) e scrivi tts/durs.json = lista delle durate in secondi.
3. cd video && python3 gen.py && python3 gen_tut.py  (gen_tut inietta DUR e la griglia musicale suno/mg_tav.json; ogni battuta dura almeno voce + 0,9 s e finisce sul battito).
4. PAGE=tut.html NODE_PATH=$(npm root -g) node mgdump.js > sayt.json  (total, cut, sayt = partenze delle battute).
5. cd ../suno && python3 build.py tav <cut> <total> tav_arr.wav  (servono i wav degli stem: fluidsynth -ni -g 0.6 -r 48000 -F wav/tav_<Stem>.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 midi/tav/*.mid; apt fluidsynth fluid-soundfont-gm; pip mido)
6. cd ../music && python3 mix.py tut tut_audio.wav  (voci a sayt+0,15 s, musica abbassata sotto le voci)
7. Render: 4 worker `PAGE=tut.html NODE_PATH=$(npm root -g) node render.js <a> <b> tsegN.mp4`, concat, mux con tut_audio.wav. Se le durate non cambiano, il video senza audio attuale è tcat_tutorial_video_senza_audio.mp4 (tutorial 12:54).
8. Web: 720p 2 passate (~145k video + 56k aac) per stare sotto i 20 MiB; asset sull'artifact https://claude.ai/artifact/EFwVcGkSa4y46rLnLruHAj, aggiornare <source src="/_blob/..."> e la lista CH dei capitoli (les.js) in pagina_tut_index.html.
Attenzione: pkill/pgrep -f con un testo presente nel proprio comando colpisce la shell stessa.
