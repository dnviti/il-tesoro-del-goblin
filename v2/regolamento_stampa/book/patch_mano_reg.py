def rep(s,a,b):
    assert s.count(a)==1,a[:60]; return s.replace(a,b)
s=open('build.py').read()
s=rep(s,"la miniatura e il mazzetto dello stesso colore, senza guardarne le carte.","la miniatura e il mazzetto dello stesso colore.")
s=rep(s,"<i>Casuale</i>: pesca coperte 5 carte della tua classe (il Mago le sue 4) e le altre comuni. <i>Draft</i>: tieni 3 carte della tua classe; poi pesca 7 comuni, tienine 1 e passa le altre a sinistra fino ad averne 7.",
"In entrambi i modi <b>scegli 5 carte</b> dal mazzetto della tua classe (il Mago ha solo le sue 4 e prende 1 comune in più). <i>Casual</i>: pesca 5 carte dal mazzo comune. <i>Draft</i>: ognuno riceve 5 carte del mazzo comune, ne tiene 1 e passa le altre a destra, finché non finiscono.")
open('build.py','w').write(s)
t=open('inizia.py').read()
t=rep(t,"con il mazzetto dello stesso colore (non guardare le carte).","con il mazzetto dello stesso colore.")
t=rep(t,"Casuale: 5 carte della tua classe + 5 comuni, coperte (il Mago 4 + 6). Oppure draft: tieni 3 carte della tua classe, poi pesca 7 comuni, tienine 1 e passa a sinistra fino a 7.",
"Scegli 5 carte della tua classe (il Mago le sue 4 + 1 comune). Casual: pesca 5 comuni. Draft: 5 comuni a testa, tienine 1 e passa a destra finché finiscono.")
open('inizia.py','w').write(t)
print('ok')
