# Riverbero di sala unico per tutta la musica (gli stem sono resi a secco): IR sintetica stereo decorrelata
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR=48000
def ir(rt60=2.2,pre=0.018,seed=7):
    n=int(rt60*1.2*SR); t=np.arange(n)/SR; rng=np.random.default_rng(seed); out=[]
    for c in range(2):
        x=rng.standard_normal(n)*np.exp(-6.9*t/rt60)
        # smorzamento delle alte nel tempo: due bande con decadimenti diversi
        lo=sosfilt(butter(2,3500,'low',fs=SR,output='sos'),x); hi=(x-lo)*np.exp(-6.9*t/(rt60*0.45))
        y=lo+hi; y=sosfilt(butter(1,180,'high',fs=SR,output='sos'),y)
        y[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
        out.append(np.concatenate([np.zeros(int(pre*SR)),y]))
    h=np.array(out); return h/np.sqrt(np.sum(h**2)/2)
def apply(x,wet_db=-14.0,rt60=2.2):
    h=ir(rt60); w=np.array([fftconvolve(x[c],h[c])[:x.shape[1]] for c in range(2)])
    return x+w*10**(wet_db/20)
