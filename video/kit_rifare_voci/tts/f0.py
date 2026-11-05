import numpy as np,wave,json
def f0(p):
    w=wave.open(p);x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float);sr=w.getframerate()
    fs=[]
    for i in range(0,len(x)-2048,1024):
        fr=x[i:i+2048]
        if np.sqrt(np.mean(fr**2))<1500: continue
        ac=np.correlate(fr,fr,'full')[2047:]; lo,hi=int(sr/400),int(sr/70)
        k=lo+np.argmax(ac[lo:hi])
        if ac[k]>0.5*ac[0]: fs.append(sr/k)
    return np.median(fs)
d=json.load(open('norm.json'))
for sp in 'LMG':
    ids=[i for i,(s,_) in enumerate(d) if s==sp][:4]
    print(sp,[round(f0(f'clips/v{i:03d}.wav')) for i in ids], 'raw',[round(f0(f'clips/raw{i:03d}.wav')) for i in ids[:2]])
