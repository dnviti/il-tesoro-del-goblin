# Voci ElevenLabs v4 via OpenRouter: chiave in OPENROUTER_API_KEY (mai su file)
import json,subprocess,os,sys,urllib.request,concurrent.futures as cf
KEY=os.environ['OPENROUTER_API_KEY']
VOICE=json.loads(os.environ.get('VOICES','{"L":"matilda","M":"brian","G":"jessica"}'))
MODEL=os.environ.get('MODEL','elevenlabs/eleven-v4')
d=json.load(open('norm.json'))
only=[int(x) for x in sys.argv[1:]] or range(len(d))
def tts(i):
    sp,tx=d[i]; mp=f'clips/el{i:03d}.mp3'; out=f'clips/v{i:03d}.wav'
    if not os.path.exists(mp) or os.environ.get('FORCE'):
        body=json.dumps({'model':MODEL,'input':tx,'voice':VOICE[sp],'response_format':'mp3'}).encode()
        for k in range(4):
            try:
                r=urllib.request.urlopen(urllib.request.Request('https://openrouter.ai/api/v1/audio/speech',body,{'Authorization':'Bearer '+KEY,'Content-Type':'application/json'}),timeout=120)
                open(mp,'wb').write(r.read()); break
            except Exception as e: print('retry',i,e); import time; time.sleep(2**k)
    subprocess.run(['ffmpeg','-v','error','-y','-i',mp,'-af','silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,aresample=48000,loudnorm=I=-18:TP=-2:LRA=7','-ar','48000','-ac','1',out],check=True)
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True)
    return i,round(float(p.stdout),3)
with cf.ThreadPoolExecutor(6) as ex: res=dict(ex.map(tts,only))
if len(res)==len(d):
    durs=[res[i] for i in range(len(d))]; json.dump(durs,open('durs.json','w')); print(len(durs),sum(durs),max(durs))
else: print(res)
