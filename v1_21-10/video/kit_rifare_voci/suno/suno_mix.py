# Somma degli stem WAV di Suno (= il brano originale) e allineamento alla griglia MIDI:
# l'audio Suno arriva più tardi dei MIDI di un ritardo costante (misurato sulla batteria).
import numpy as np, wave, glob, sys, os
SR=48000
OFF={'tav':0.144,'mimi':0.433}   # secondi: mediana su ~700-1000 colpi di batteria MIDI vs WAV, nessuna deriva
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768; return x.reshape(-1,2).T
def wr(p,a):
    pcm=(np.clip(a.T,-1,1)*32767).astype('<i2'); w=wave.open(p,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
src,dst=sys.argv[1],sys.argv[2]; os.makedirs(dst,exist_ok=True)
for d in OFF:
    st=[rd(f) for f in sorted(glob.glob(f'{src}/{d}/*.wav'))]
    m=np.sum([x for x in st],axis=0); m=m[:,int(round(OFF[d]*SR)):]
    pk=np.abs(m).max(); print(d,len(st),'stem, picco %.3f'%pk)
    wr(f'{dst}/{d}_Mix.wav',m*(0.95/pk if pk>0.95 else 1))
