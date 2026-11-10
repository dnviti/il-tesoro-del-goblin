# Musica «alta qualità»: ogni canale di ogni stem MIDI Suno viene reso col suono migliore disponibile
# (librerie Sonatina per archi/legni/ottoni/arpa, il miglior banco GM per il resto), a secco;
# ogni canale è riportato al livello che aveva nella resa GM, poi gli stem passano a build.py (WAVDIR=wav_hq).
import mido, os, sys, glob, subprocess, wave, numpy as np, concurrent.futures as cf
import mido.midifiles.meta as MM
_o=MM.MetaSpec_key_signature.decode
def _d(self,msg,data):
    try: _o(self,msg,data)
    except Exception: msg.key="C"
MM.MetaSpec_key_signature.decode=_d
SFD='/tmp/claude-0/sf'; SSO=SFD+'/sso/'; SR=48000
GM={'musyng':SFD+'/musyng.sf2','sgm':SFD+'/sgm.sf2','gu':SFD+'/gu.sf2','toh':SFD+'/toh.sf2','fr3':SFD+'/fr3.sf2'}
# banco GM per stem (confronto alla cieca, a parità vince il banco più grande)
BASE={'tav':dict(Bass='musyng',Drums='toh',Guitar='musyng',Keyboard='fr3',Percussion='sgm',Strings='sgm',Synth='gu',Woodwinds='sgm',FX='fr3'),
      'mimi':dict(Bass='fr3',Brass='gu',Drums='toh',Guitar='sgm',Keyboard='gu',Percussion='fr3',Strings='gu',Synth='gu',Woodwinds='fr3',FX='gu')}
def S(n): return SSO+n+'.sf2'
STR=[(60,128,'Strings - 1st Violins Sustain'),(48,60,'Strings - Violas Sustain'),(36,48,'Strings - Celli Sustain'),(0,36,'Strings - Basses Sustain')]
FL=os.environ.get('FLUTE','Woodwinds - Flute Solo')  # 'gm' = flauto del banco GM
ONLY=os.environ.get('ONLY')  # es. 'tav' per rifare un solo brano
WW=[(67,128,FL),(50,67,'Woodwinds - Clarinet Solo'),(0,50,'Woodwinds - Bassoon Solo')]
BR=[(55,128,'Brass - Horns Sustain'),(0,55,'Brass - Trombones Sustain')]
def plan(d,stem,ch,prog):
    """lista di (sf, programma GM o None, nota_min, nota_max)"""
    if ch==9: return None
    if prog==46: return [(S('Concert Harp'),None,0,128)]
    if stem=='Strings':
        if prog==40: return [(S('Strings - Violin Solo'),None,0,128)]
        if prog in (49,48,89,54,107): return [(S(n),None,a,b) for a,b,n in STR]
    if stem=='Woodwinds': return [((S(n) if n!='gm' else None),None,a,b) for a,b,n in WW]
    if stem=='Brass' and prog in (61,65,1): return [(S(n),None,a,b) for a,b,n in BR]
    if prog==73: return None if FL=='gm' else [(S(FL),None,0,128)]
    if stem=='Bass' and prog==32 and d=='tav': return [(S('Strings - Basses Pizzicato'),None,0,128)]
    return None
CFG=SFD+'/interp.cfg'
def render(mid,sf,out,dry=True):
    subprocess.run(['fluidsynth','-ni','-q','-g','0.5','-r',str(SR),'-o','synth.polyphony=1024','-o','synth.reverb.active='+('0' if dry else '1'),'-o','synth.chorus.active=0','-f',CFG,'-F',out,sf,mid],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768; return x.reshape(-1,2).T
def wr(p,a):
    pcm=(np.clip(a.T,-1,1)*32767).astype('<i2'); w=wave.open(p,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
def rms(x):
    a=x[:,np.abs(x).max(0)>1e-3]; return np.sqrt(np.mean(a**2)) if a.size else 0
def split(m,ch,lo=0,hi=128,prog=None):
    """copia del MIDI con solo il canale ch (note in [lo,hi)), programma forzato a prog (o 0 per Sonatina)"""
    o=mido.MidiFile(ticks_per_beat=m.ticks_per_beat,type=1)
    for tr in m.tracks:
        t=mido.MidiTrack(); acc=0; first=True
        for msg in tr:
            acc+=msg.time
            keep=msg.is_meta and msg.type in ('set_tempo','time_signature','end_of_track')
            if not msg.is_meta and getattr(msg,'channel',None)==ch:
                if msg.type in ('note_on','note_off'): keep=lo<=msg.note<hi
                elif msg.type=='program_change': keep=False
                else: keep=True
            if keep:
                if first and not msg.is_meta:
                    t.append(mido.Message('program_change',channel=ch,program=prog or 0,time=0)); first=False
                t.append(msg.copy(time=acc)); acc=0
        o.tracks.append(t)
    return o
TMP='/tmp/claude-0/sf/hq_tmp_'+os.environ.get('OUT','wav_hq'); os.makedirs(TMP,exist_ok=True)
def job(args):
    d,f=args; stem=f.split('(')[1][:-5]
    if stem=='Vocals': return
    m=mido.MidiFile(f); base=GM[BASE[d][stem]]
    # canali e programmi
    prog={}; chans={}
    for tr in m.tracks:
        for msg in tr:
            if msg.type=='program_change': prog[msg.channel]=msg.program
            if msg.type=='note_on' and msg.velocity>0: chans.setdefault(msg.channel,prog.get(msg.channel,0))
    total=None; parts=[]
    for ch,pg in sorted(chans.items()):
        # resa di riferimento GM del canale (programma originale)
        ref=f'{TMP}/{d}_{stem}_{ch}_ref.wav'; mf=f'{TMP}/{d}_{stem}_{ch}.mid'
        o=split(m,ch,prog=pg); o.save(mf); render(mf,base,ref)
        x=rd(ref); p=plan(d,stem,ch,pg)
        if p:
            y=None
            for k,(sf,gp,lo,hi) in enumerate(p):
                mk=f'{TMP}/{d}_{stem}_{ch}_{k}.mid'; ok=f'{TMP}/{d}_{stem}_{ch}_{k}.wav'
                oo=split(m,ch,lo,hi,prog=(gp if sf else pg)); oo.save(mk); render(mk,sf or base,ok); z=rd(ok)
                y=z if y is None else (np.pad(y,((0,0),(0,max(0,z.shape[1]-y.shape[1]))))+np.pad(z,((0,0),(0,max(0,y.shape[1]-z.shape[1])))))
            r0,r1=rms(x),rms(y)
            if r1>0: x=y*(r0/r1)
            parts.append(f'{ch}:{pg}->'+'+'.join(os.path.basename(q[0] or 'GM.sf2')[:-4] for q in p))
        total=x if total is None else (np.pad(total,((0,0),(0,max(0,x.shape[1]-total.shape[1]))))+np.pad(x,((0,0),(0,max(0,total.shape[1]-x.shape[1])))))
    OUT=os.environ.get('OUT','wav_hq'); os.makedirs(f'{SFD}/{OUT}',exist_ok=True); wr(f'{SFD}/{OUT}/{d}_{stem}.wav',total*0.9/max(1e-9,np.abs(total).max()))
    return f'{d} {stem} [{BASE[d][stem]}] '+'; '.join(parts)
J=[(d,f) for d in (['tav','mimi'] if not ONLY else [ONLY]) for f in sorted(glob.glob(f'/tmp/claude-0/work/suno/{d}/*.mid'))]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(job,J):
        if r: print(r,flush=True)
