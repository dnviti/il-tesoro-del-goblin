# Mix: voci del tutorial alle partenze delle battute + musica in loop abbassata sotto le voci
import numpy as np, wave, json, sys
SR=48000
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
    return x.reshape(-1,w.getnchannels()).T
def wr(p,a):
    pcm=(np.clip(a.T,-1,1)*32767).astype('<i2'); w=wave.open(p,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
def music(total,src):
    m=rd(src); n=int(total*SR)
    if m.shape[1]<n: m=np.pad(m,((0,0),(0,n-m.shape[1])))
    return m[:,:n],n
mode=sys.argv[1]
if mode=='tut':
    T=json.load(open('../video/sayt.json')); total=T['total']; st=T['sayt']
    names=json.load(open('../tts/norm.json'))
    m,n=music(total,'../suno/tav_arr.wav'); v=np.zeros((2,n)); act=np.zeros(n)
    PAN={'L':-0.22,'M':0.0,'G':0.22}
    for i,(sp,_) in enumerate(names):
        c=rd(f'../tts/clips/v{i:03d}.wav')[0]; s=int((st[i]+0.15)*SR); e=min(n,s+len(c))
        p=PAN[sp]; v[0,s:e]+=c[:e-s]*np.sqrt(0.5*(1-p))*1.25; v[1,s:e]+=c[:e-s]*np.sqrt(0.5*(1+p))*1.25
        act[max(0,s-int(0.3*SR)):min(n,e+int(0.4*SR))]=1
    # envelope liscio: −14,5 dB sotto le voci, −8,5 dB nelle pause
    k=int(0.35*SR); cs=np.concatenate(([0],np.cumsum(act))); i=np.arange(n); lo=np.clip(i-k//2,0,n); hi=np.clip(i+k//2,0,n); a=(cs[hi]-cs[lo])/k
    gdb=-8.5-6.0*a; g=10**(gdb/20)
else:
    total=float(sys.argv[2]); m,n=music(total,'../suno/mimi_arr.wav'); v=np.zeros((2,n)); g=np.full(n,10**(-2.5/20))
fi=int(0.05*SR); fo=int(0.3*SR); env=np.ones(n); env[:fi]=np.linspace(0,1,fi); env[-fo:]=np.linspace(1,0,fo)**1.5
out=m*g*env+v
pk=np.max(np.abs(out)); print('peak',pk)
if pk>0.97: out*=0.97/pk
wr(sys.argv[-1],out)
