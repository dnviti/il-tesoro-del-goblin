# Sequenza musicale: brano intero fino a E, poi loop [LOOP0,E) ripetuto, finale [E,N) + coda. Griglia in tempo video.
import json
G=json.load(open('grid.json'))
CFG={'tav':dict(E=57,L0=4,tol=0.3,need=1000),'mimi':dict(E=71,L0=4,tol=0.02,need=420)}
TAIL=1.5
out={}
for d,c in CFG.items():
    beats=G[d]['beats']; bpb=G[d]['bpb']; bars=beats[::bpb]; N=len(bars)-1
    segs=[(0,c['E'])]; t=bars[c['E']]-bars[0]
    while t<c['need']: segs.append((c['L0'],c['E'])); t+=bars[c['E']]-bars[c['L0']]
    gb=[];gbar=[];off=0;plan=[]
    for s,e in segs:
        a,b=bars[s],bars[e]
        gb+= [x-a+off for x in beats if a-1e-6<=x<b-1e-6]; gbar+=[x-a+off for x in bars[s:e]]
        plan.append([s,e,off]); off+=b-a
    gb.append(off); gbar.append(off)
    outro=bars[N]-bars[c['E']]+TAIL
    out[d]=dict(beats=[round(x,4) for x in gb],bars=[round(x,4) for x in gbar],outro=round(outro,4),tol=c['tol'],cut=None)
    json.dump(dict(plan=plan,E=c['E'],N=N,tail=TAIL),open(f'plan_{d}.json','w'))
    json.dump(out[d],open(f'mg_{d}.json','w'))
    print(d,len(gb),len(gbar),'outro',outro,'segs',len(segs))
