import json,subprocess,os
d=json.load(open('norm.json'))
FX={'L':'rubberband=pitch=0.95:formant=preserved,equalizer=f=250:t=q:w=1:g=2',
    'G':'rubberband=pitch=1.07:tempo=1.04:formant=preserved',
    'M':'rubberband=pitch=0.75:formant=preserved:tempo=1.19,asetrate=14080,aresample=16000,equalizer=f=150:t=q:w=1:g=3'}
durs=[]
for i,(sp,tx) in enumerate(d):
    raw=f'clips/raw{i:03d}.wav'; out=f'clips/v{i:03d}.wav'
    subprocess.run(['pico2wave','-l','it-IT','-w',raw,tx],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af',FX[sp]+',silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,aresample=48000,loudnorm=I=-18:TP=-2:LRA=7','-ar','48000','-ac','1',out],check=True)
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True)
    durs.append(round(float(p.stdout),3))
json.dump(durs,open('durs.json','w'))
print(len(durs),sum(durs),max(durs))
