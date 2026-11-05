import json,math,sys
d=json.load(open(sys.argv[1])); xs=[g['perPlayer'] for g in d['games']]
n=len(xs); m=sum(xs)/n; sd=(sum((x-m)**2 for x in xs)/n)**.5
lo=math.floor(min(xs)); hi=math.floor(max(xs))
cnt={}
for x in xs: cnt[math.floor(x)]=cnt.get(math.floor(x),0)+1
Phi=lambda z:0.5*(1+math.erf(z/2**.5))
rows=[{'turni':k,'partite':cnt.get(k,0),'attese':round(n*(Phi((k+1-m)/sd)-Phi((k-m)/sd)),1)} for k in range(lo,hi+1)]
print(n, round(m,2), round(sd,2), lo, hi)
print(json.dumps(rows,separators=(',',':')))
short=sum(1 for x in xs if x<3)/n; long=sum(1 for x in xs if x>=20)/n
print('short<3',round(short*100,2),'long>=20',round(long*100,2), 'p10',sorted(xs)[n//10],'p90',sorted(xs)[9*n//10])
