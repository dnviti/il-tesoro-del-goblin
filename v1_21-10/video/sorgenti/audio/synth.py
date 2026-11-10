# Musica originale «taverna» in Re dorico, 84 bpm, loop di 32 battute (circa 91 s), sintetizzata da zero.
import numpy as np, wave, sys
SR=48000; BPM=84; BEAT=60/BPM; BAR=4*BEAT
rng=np.random.default_rng(7)
def mtof(m): return 440*2**((m-69)/12)
NB=32; L=int(round(NB*BAR*SR)); out=np.zeros((2,L))
def add(sig,t,pan=0.0,gain=1.0):
    i=int(round(t*SR))%L; n=len(sig)
    l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    idx=(np.arange(n)+i)%L
    np.add.at(out[0],idx,sig*gain*l); np.add.at(out[1],idx,sig*gain*r)
# Karplus-Strong a blocchi, una volta per altezza
cache={}
def pluck(m,dur=2.2):
    if m in cache: return cache[m]
    f=mtof(m); N=int(SR/f); n=int(dur*SR)
    y=np.zeros(n+N); y[:N]=rng.uniform(-1,1,N); y[:N]=np.convolve(y[:N],np.ones(3)/3,'same')
    dec=0.996 if m<60 else 0.993
    for s in range(N,n+N,N):
        e=min(s+N,n+N); prev=y[s-N:e-N]; prev1=np.concatenate(([y[s-N-1]],prev[:-1])) if s-N-1>=0 else prev
        y[s:e]=dec*0.5*(prev+prev1)
    y=y[N:]; env=np.minimum(1,np.arange(n)/(0.002*SR)); y*=env
    y*=np.linspace(1,0,n)**0.5
    cache[m]=y/np.max(np.abs(y)); return cache[m]
def pad(ms,dur):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for m in ms:
        f=mtof(m)
        for det in (-0.12,0.12):
            ff=f*2**(det/12)
            s+=np.sin(2*np.pi*ff*t)+0.35*np.sin(4*np.pi*ff*t+1)+0.12*np.sin(6*np.pi*ff*t+2)
    a=int(0.8*SR); r=int(1.2*SR); env=np.ones(n); env[:a]=np.linspace(0,1,a)**2; env[-r:]=np.linspace(1,0,r)**2
    return s*env*(1+0.06*np.sin(2*np.pi*0.25*t))/ (len(ms)*2)
def flute(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m)
    vib=1+0.004*np.sin(2*np.pi*5.2*t)*np.minimum(1,t/0.4)
    ph=2*np.pi*np.cumsum(f*vib)/SR
    s=np.sin(ph)+0.18*np.sin(2*ph)+0.05*np.sin(3*ph)+0.02*rng.standard_normal(n)
    a=int(0.06*SR); r=int(min(0.25,dur/3)*SR); env=np.ones(n); env[:a]=np.linspace(0,1,a); env[-r:]=np.linspace(1,0,r)
    return s*env
def drum(acc=1.0):
    n=int(0.5*SR); t=np.arange(n)/SR
    f=70+60*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)*np.exp(-t*9)+0.25*rng.standard_normal(n)*np.exp(-t*60)
    return s*acc
# accordi (MIDI): Dm C Bb C | Dm C Bb A
D=[50,57,62,65,69]; C=[48,55,60,64,67]; Bb=[46,53,58,62,65]; A=[45,52,57,61,64]; F=[41,53,57,60,65]
PROG=[D,C,Bb,C, D,C,Bb,A, D,F,C,D, Bb,C,A,D]   # 16 accordi da 2 battute
ARP=[0,2,3,4,3,2,1,2]                          # crome sugli indici dell'accordo
for k,ch in enumerate(PROG):
    t0=k*2*BAR
    add(pad([ch[1],ch[2],ch[3]],2*BAR+1.0),t0,0,0.22)
    add(pluck(ch[0]-0),t0,-0.1,0.30); add(pluck(ch[0]),t0+BAR,-0.1,0.22)
    for bar in range(2):
        for j,ai in enumerate(ARP):
            if bar==1 and j>=6 and k%2==1: continue
            add(pluck(ch[ai]+12),t0+bar*BAR+j*BEAT/2,0.35 if j%2 else 0.15,0.16 if j%2 else 0.2)
        add(drum(0.55),t0+bar*BAR,0,0.5); add(drum(0.3),t0+bar*BAR+2*BEAT,0,0.5)
        add(drum(0.18),t0+bar*BAR+3.5*BEAT,0,0.5)
# melodia nelle battute 17-32 (accordi 8-15), altezze in MIDI e durate in tempi
MEL=[(74,2),(76,1),(77,1),(76,2),(74,2), (72,3),(74,1),(77,4), (76,2),(72,2),(67,2),(72,1),(74,1), (76,3),(73,1),(74,4),
     (77,2),(79,1),(77,1),(74,2),(70,2), (72,2),(74,1),(76,1),(79,4), (76,2),(73,1),(74,1),(76,2),(69,2), (73,2),(76,2),(74,4)]
t=16*BAR
for m,d in MEL:
    add(flute(m,d*BEAT*0.95),t,-0.25,0.10); t+=d*BEAT
# riverbero: convoluzione circolare con risposta all'impulso a decadimento esponenziale (il loop resta continuo)
ir_n=int(2.4*SR); ti=np.arange(ir_n)/SR
for c in range(2):
    ir=rng.standard_normal(ir_n)*np.exp(-ti*2.6); ir[:int(0.012*SR)]=0; ir/=np.sqrt(np.sum(ir**2))
    irf=np.zeros(L); irf[:ir_n]=ir
    wet=np.fft.irfft(np.fft.rfft(out[c])*np.fft.rfft(irf),L)
    out[c]=out[c]+0.35*wet
# filtro dolce (passa basso a un polo) per togliere asprezza
a=np.exp(-2*np.pi*5500/SR)
for c in range(2):
    X=np.fft.rfft(out[c]); fr=np.fft.rfftfreq(L,1/SR); X/=np.sqrt(1+(fr/5500)**2); out[c]=np.fft.irfft(X,L)
out/=np.max(np.abs(out))*1.12
pcm=(np.clip(out.T,-1,1)*32767).astype('<i2')
w=wave.open('loop.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('loop s',L/SR)
