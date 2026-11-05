import json,sys,math,collections
prefs=sys.argv[1].split(',');pref=prefs[-1]+'c' if len(prefs)>1 else prefs[0]
G=[];R=[]
for p in prefs:
  for i in range(1,5):
    d=json.load(open(f'runs/{p}_{i}.json')); off=len(G); G+=d['games']; R+=d['rows']
def stats(xs):
    n=len(xs); m=sum(xs)/n; sd=(sum((x-m)**2 for x in xs)/n)**.5
    sk=sum((x-m)**3 for x in xs)/n/sd**3; ku=sum((x-m)**4 for x in xs)/n/sd**4-3
    lo=math.floor(min(xs)); hi=max(xs); nb=max(1,int(hi-lo)+1)
    h=[0]*nb
    for x in xs: h[min(nb-1,int(x-lo))]+=1
    exp=[n*(0.5*(1+math.erf((lo+k+1-m)/(sd*2**.5)))-0.5*(1+math.erf((lo+k-m)/(sd*2**.5)))) for k in range(nb)]
    mh=sum(h)/nb; sst=sum((a-mh)**2 for a in h); sse=sum((a-b)**2 for a,b in zip(h,exp))
    return m,sd,sk,ku,1-sse/sst if sst else 0
by=collections.defaultdict(list)
for g in G: by[g['key']].append(g)
cl=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0.0]))
fs=collections.defaultdict(lambda:[0,0.0])
for r in R:
    c=cl[r['key']][r['cls']]; c[0]+=r['win']; c[1]+=1/r['n']
    if r['seat']==1: f=fs[r['key']]; f[0]+=r['win']; f[1]+=1/r['n']
out=[]
for k,gs in by.items():
    m,sd,sk,ku,r2=stats([g['perPlayer'] for g in gs])
    idx={c:w/e for c,(w,e) in cl[k].items()}
    rms=(sum((v-1)**2 for v in idx.values())/len(idx))**.5
    first=fs[k][0]/fs[k][1]
    # score: class rms, shape, first-player, length 8-13 target
    lenpen=max(0,8-m)+max(0,m-13)
    score=100-100*rms-20*abs(sk)-8*abs(ku)-50*(1-r2)-30*abs(first-1)-4*lenpen
    out.append((score,k,len(gs),m,sd,sk,ku,r2,rms,min(idx.values()),max(idx.values()),first,gs[0]['rules']))
out.sort(reverse=True)
print(f"{'impostazione':24}{'part':>6}{'score':>7}{'turni':>7}{'sd':>6}{'skew':>6}{'kurt':>6}{'R2':>6}{'rmsCl':>7}{'min':>6}{'max':>6}{'primo':>6}")
for s,k,n,m,sd,sk,ku,r2,rms,mi,ma,f,_ in out:
    print(f"{k:24}{n:6}{s:7.1f}{m:7.1f}{sd:6.1f}{sk:6.2f}{ku:6.2f}{r2:6.3f}{rms:7.3f}{mi:6.2f}{ma:6.2f}{f:6.2f}")
json.dump([dict(score=s,key=k,games=n,mean=m,sd=sd,skew=sk,kurt=ku,r2=r2,rms=rms,min=mi,max=ma,first=f,rules=ru) for s,k,n,m,sd,sk,ku,r2,rms,mi,ma,f,ru in out],open(f'runs/{pref}_combos.json','w'),ensure_ascii=False)
for dim in ['size','spawns','die']:
    agg=collections.defaultdict(list)
    for o in out: agg[o[12][dim]].append(o)
    print(dim, {v:round(sum(x[0] for x in L)/len(L),1) for v,L in sorted(agg.items())})
