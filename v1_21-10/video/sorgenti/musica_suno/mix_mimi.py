import numpy as np, wave, glob, sys
SR=48000
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768; return x.reshape(-1,2).T
st=[rd(f) for f in sorted(glob.glob(sys.argv[1]+'/*.wav'))]
L=max(x.shape[1] for x in st); m=np.zeros((2,L),np.float32)
for x in st: m[:,:x.shape[1]]+=x
m=m[:,int(round(0.433*SR)):]; pk=np.abs(m).max(); print(len(st),'stem picco',pk)
m=m*(0.95/pk if pk>0.95 else 1)
pcm=(np.clip(m.T,-1,1)*32767).astype('<i2'); w=wave.open(sys.argv[2],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
