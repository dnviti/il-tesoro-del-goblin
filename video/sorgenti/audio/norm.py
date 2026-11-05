import re, json, html
def norm(t):
    t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    R=[('«?»','punto di domanda'),('«','"'),('»','"'),('…',', '),('10 × 10','dieci per dieci'),('3 × 2','tre per due'),('×','per'),
       ('D6 + 1','di sei più uno'),('D6 − 1','di sei meno uno'),('D6 meno 1','di sei meno uno'),('D6 + MOV','di sei più movimento'),('D20 + ATT','di venti più attacco'),
       ('D20','di venti'),('D6','di sei'),('MIMI','Mimi'),('Caos','Càos'),('PV','punti vita'),('PE','punti esperienza'),(' ATT',' attacco'),(' MOV',' movimento'),('l’AR','l\'armatura'),('all’AR','all\'armatura'),(' AR',' armatura'),
       ('−','meno'),(' + ',' più '),('’',"'"),('H1','acca uno'),('J5','i lunga cinque'),('Ok','okay'),(' a attacco'," all'attacco")]
    for a,b in R: t=t.replace(a,b)
    t=re.sub(r'\+(\d)',r'più \1',t); t=re.sub(r'meno(\d)',r'meno \1',t); t=re.sub(r'\b1 punti (esperienza|vita)',r'1 punto \1',t)
    return t.strip()
L=json.load(open('../video/lines.json'))
out=[(x[0],norm(x[2:])) for x in L]
json.dump(out,open('norm.json','w'),ensure_ascii=False,indent=0)
for w,t in out[:6]: print(w,t)
