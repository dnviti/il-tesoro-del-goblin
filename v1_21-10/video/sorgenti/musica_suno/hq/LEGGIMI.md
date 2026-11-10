Musica con strumenti campionati (22/10/2026)

Banchi usati (scaricati da archive.org, non copiati qui per il peso):
- Sonatina Symphonic Orchestra SF2 (archive.org/details/SonatinaSymphonicOrchestraSF2): archi per registro, arpa, flauto/clarinetto/fagotto, corni/tromboni.
- Musyng Kite, SGM-V2.01, Timbres of Heaven 4.00, GeneralUser GS, FluidR3_GM: banco GM scelto stem per stem (tabella BASE in render_hq.py, da confronto alla cieca).
Passi: mettere i banchi in /tmp/claude-0/sf (musyng.sf2, sgm.sf2, gu.sf2, toh.sf2, fr3.sf2, sso/), poi
  ONLY=tav FLUTE=gm OUT=wav_final python3 hq/render_hq.py   (Taverna: flauto del banco GM, preferito alla cieca)
  ONLY=mimi OUT=wav_final python3 hq/render_hq.py           (MIMI: flauto Sonatina)
  WAVDIR=/tmp/claude-0/sf/wav_final REVERB=1 python3 build.py tav <cut> <total> tav_arr.wav  (idem mimi)
Gli stem sono resi a secco e build.py aggiunge un'unica sala (hq/reverb.py).

AGGIORNAMENTO 22/10 ore 8:55: ora i video usano gli stem WAV originali di Suno (zip caricati da Daniele in /mnt/project-files/).
  python3 suno_mix.py <cartella con tav/ e mimi/ estratti dagli zip> /tmp/claude-0/sf/wav_suno   (somma gli stem e toglie il ritardo: 144 ms Taverna, 433 ms MIMI)
  WAVDIR=/tmp/claude-0/sf/wav_suno python3 build.py tav 743.4703 756.5128 tav_arr.wav ; idem mimi 309.2801 317.7763
La resa con strumenti campionati (questa cartella hq/) resta come ripiego.
