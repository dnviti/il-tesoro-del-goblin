exec(open('info.py').read().split("for d in")[0])
import numpy as np,wave,glob,json
SR=48000
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    return x.reshape(-1,2).T
CFG={'tav':dict(fb=960,bb=3840,skip=[]),'mimi':dict(fb=480,bb=1920,skip=['Vocals'])}
out={}
for d,c in CFG.items():
    m=mido.MidiFile(glob.glob(d+'/*Drums*.mid')[0])
    # tempo map
    tm=[]; 
    for tr in m.tracks:
        t=0
        for msg in tr:
            t+=msg.time
            if msg.type=='set_tempo': tm.append((t,msg.tempo))
    tm=sorted(set(tm)); tpb=m.ticks_per_beat
    def t2s(tick):
        s=0; last_t=0; last_tempo=500000
        for tt,te in tm:
            if tt>=tick: break
            s+=(tt-last_t)*last_tempo/tpb/1e6; last_t=tt; last_tempo=te
        return s+(tick-last_t)*last_tempo/tpb/1e6
    L=m.length; nb=int(L/ (c['bb']/tpb*0.6))+4
    beats=[];k=0
    while True:
        s=t2s(k*c['fb'])
        if s>L+0.5: break
        beats.append(s);k+=1
    st=[rd(f) for f in sorted(glob.glob(f'wav/{d}_*.wav')) if not any(x in f for x in c['skip'])]
    n=max(x.shape[1] for x in st); mix=np.zeros((2,n),np.float32)
    for x in st: mix[:,:x.shape[1]]+=x
    np.save(f'{d}_mix.npy',mix)
    bpb=c['bb']//c['fb']; bars=beats[::bpb]
    rms=[20*np.log10(np.sqrt(np.mean(mix[:,int(a*SR):int(b*SR)]**2))+1e-9) for a,b in zip(bars,bars[1:])]
    first_note=min(min((i for i in range(0,n,480) if abs(mix[0,i])>1e-3),default=0) for _ in [0])/SR
    print(d,'beats',len(beats),'beat s %.3f'%np.mean(np.diff(beats)),'bars',len(bars),'len',n/SR,'first sound %.2f'%first_note)
    print(' bar rms',' '.join('%d'%r for r in rms))
    out[d]=dict(beats=beats,bpb=bpb,len=n/SR)
json.dump(out,open('grid.json','w'))
