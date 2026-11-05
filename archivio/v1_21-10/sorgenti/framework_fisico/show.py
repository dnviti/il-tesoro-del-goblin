import json,sys
for l in open(sys.argv[1]):
    a=l.split(' ',2)
    try: d=json.loads(a[2])
    except: print(l); continue
    print(a[0],a[1],d['min'],d['ph'],d['p10'],d['p90'],{k[:3]:d['cls'][k] for k in ['Guerriero','Ladro','Mago','Chierico']})
