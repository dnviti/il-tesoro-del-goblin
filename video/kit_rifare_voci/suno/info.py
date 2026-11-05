import mido,sys,glob,collections
import mido.midifiles.meta as MM
_o=MM.MetaSpec_key_signature.decode
def _d(self,msg,data):
    try: _o(self,msg,data)
    except Exception: msg.key="C"
MM.MetaSpec_key_signature.decode=_d
for d in ['tav','mimi']:
    print('==',d)
    for f in sorted(glob.glob(d+'/*.mid')):
        m=mido.MidiFile(f); notes=0; progs=set(); chans=set(); tempos=[]; ts=[]; pitches=[]
        for tr in m.tracks:
            t=0
            for msg in tr:
                t+=msg.time
                if msg.type=='set_tempo': tempos.append((t,round(mido.tempo2bpm(msg.tempo),2)))
                if msg.type=='time_signature': ts.append((t,msg.numerator,msg.denominator))
                if msg.type=='program_change': progs.add(msg.program); chans.add(msg.channel)
                if msg.type=='note_on' and msg.velocity>0: notes+=1; chans.add(msg.channel); pitches.append(msg.note)
        print(f.split('(')[1][:-5].ljust(11),'len %.1fs'%m.length,'tpb',m.ticks_per_beat,'notes',notes,'prog',sorted(progs),'ch',sorted(chans),'tempo',tempos[:3],len(tempos),'ts',ts[:2],'range',(min(pitches),max(pitches)) if pitches else None)
