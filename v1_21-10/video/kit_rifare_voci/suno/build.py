# Mix degli stem (gain per strumento) e montaggio sul piano: segmenti a battute intere fino al taglio, poi finale.
import numpy as np, wave, glob, json, sys, os
WAV=os.environ.get('WAVDIR','wav')  # cartella degli stem resi (un banco di suoni per cartella)
SR=48000
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    return x.reshape(-1,2).T
def wr(p,a):
    pcm=(np.clip(a.T,-1,1)*32767).astype('<i2'); w=wave.open(p,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
ROLE={'Woodwinds':-1,'Guitar':-1,'Brass':-2,'Strings':-4,'Keyboard':-5,'Synth':-5,'Bass':-3,'Drums':-4,'Percussion':-5,'FX':-9}
def stemmix(d,skip):
    mix=None
    for f in sorted(glob.glob(f'{WAV}/{d}_*.wav')):
        name=os.path.basename(f).split('_',1)[1][:-4]
        if name in skip: continue
        x=rd(f)
        if name=='Mix':  # brano intero già mixato (stem WAV di Suno sommati): niente riequilibrio
            mix=np.zeros((2,max(x.shape[1],200*SR)),np.float32); mix[:,:x.shape[1]]+=x; continue
        act=x[:, np.abs(x).max(0)>1e-3]
        r=20*np.log10(np.sqrt(np.mean(act**2))+1e-9) if act.size else -99
        g=np.clip(-20-r+ROLE[name],-8,8)   # livello «quando suona» verso −20 dB + ruolo, entro ±8 dB
        print(' ',name,'rms %.1f gain %.1f'%(r,g))
        x=x*10**(g/20)
        if mix is None: mix=np.zeros((2,max(x.shape[1],200*SR)),np.float32)
        x=x[:,:mix.shape[1]]; mix[:,:x.shape[1]]+=x
    return mix
def arrange(d,cut,total,skip=()):
    G=json.load(open('grid.json'))[d]; P=json.load(open(f'plan_{d}.json'))
    bars=G['beats'][::G['bpb']]; mix=stemmix(d,set(skip))
    if os.environ.get('REVERB')=='1':  # stem resi a secco: un'unica sala per tutto il brano
        sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'hq')); import reverb; mix=reverb.apply(mix).astype(np.float32)
    n=int(round(total*SR))+SR; out=np.zeros((2,n),np.float32); X=int(0.02*SR)
    def put(a,b,at,fade_out=0):
        s0,s1=int(round(a*SR)),int(round(b*SR)); seg=mix[:,s0:s1+X].copy(); L=seg.shape[1]
        seg[:,:X]*=np.linspace(0,1,X); seg[:,-X:]*=np.linspace(1,0,X)
        if fade_out: k=int(fade_out*SR); seg[:,-k:]*=np.linspace(1,0,k)**1.5
        i=int(round(at*SR)); e=min(n,i+L); out[:,i:e]+=seg[:,:e-i]
    for s,e,off in P['plan']:
        if off>=cut-1e-6: break
        endt=min(bars[e]-bars[s]+off,cut); put(bars[s],bars[s]+(endt-off),off)
        if endt>=cut-1e-6: break
    E,N,tail=P['E'],P['N'],P['tail']
    put(bars[E],bars[N]+tail,cut,fade_out=tail)
    return out[:,:int(round(total*SR))]
if __name__=='__main__':
    d,cut,total,dst=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
    o=arrange(d,cut,total,skip=['Vocals']); o/=np.max(np.abs(o))*1.05; wr(dst,o)
