import re,sys
s=open('book/regolamento.html').read()
DD='<span class="dd">'
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]); s=s.replace(a,b)
# specie
rep('<tr><td><b>Nano</b></td><td>+1 a due statistiche diverse a scelta</td></tr>\n','')
rep('<tr><td><b>Orco</b></td><td>+2 ATT</td></tr>\n','')
rep('<tr><td><b>Sanguar</b></td><td>+2 MOV (sono non morti)</td></tr></table>',
    '<tr><td><b>Sanguar</b></td><td>+2 MOV (sono non morti)</td></tr>\n<tr><td><b>Yumaniano</b></td><td><span class="dd">Da decidere: bonus della specie.</span></td></tr></table>')
rep('<div><b>10</b> Tessere Specie</div>','<div><b>8</b> Tessere Specie <span class="dd">(2 per specie: da confermare)</span></div>')
# primo attacco
rep('<li><b>Attacchi tu per primo.</b> Tiro per colpire: 2D6 + il tuo ATT. Se il totale arriva alla <b>Difesa</b> del nemico (8 + la sua AR), lo colpisci e tiri il danno.</li>',
    '<li><b>Chi attacca per primo.</b> Tu e il nemico tirate 1 D6 a testa: chi fa di più attacca per primo. Per il mostro tira il giocatore alla tua destra. <span class="dd">Da decidere: in caso di pareggio (proposta: si ritira).</span></li>\n<li><b>Il tiro per colpire.</b> 2D6 + ATT di chi attacca. Se il totale arriva alla <b>Difesa</b> dell’altro (8 + la sua AR), lo colpisce e tira il danno.</li>')
rep('<li><b>Poi attacca il nemico.</b> Per lui tira l’avversario (con più giocatori, chi ti siede a destra): 2D6 + ATT del nemico contro la tua Difesa (8 + la tua AR), poi il suo danno.</li>',
    '<li><b>Poi attacca l’altro.</b> Per il mostro tira sempre il giocatore alla tua destra: 2D6 + ATT del mostro contro la tua Difesa (8 + la tua AR), poi il suo danno.</li>')
rep('Per il lupo tira Marco.','Per il lupo tira Marco, seduto alla destra di Lia. Prima tirano 1 D6 a testa per vedere chi attacca per primo: Lia fa 5, Marco per il lupo fa 2, quindi comincia Lia.')
rep('<li>Attacca per primo chi ha mosso; ognuno tira i propri dadi.</li>','<li>Chi attacca per primo si decide con 1 D6 a testa, come negli scontri; ognuno tira i propri dadi.</li>')
rep('Per il mostro tira l’avversario.<br>','Chi attacca per primo: 1 D6 a testa, vince il più alto.<br>Per il mostro tira chi ti siede a destra.<br>')
# mano: nota draft
rep('passa le altre a destra finché finiscono.','passa le altre a destra finché finiscono. <span class="dd">Da decidere: sempre a destra o alternando destra e sinistra.</span>')
rep('(il Mago le sue 4 e 1 comune in più)','(il Mago le sue 4 e 1 comune in più <span class="dd">da confermare</span>)')
# classi
for a,b in [('Guerriero','Assaltatore'),('Mago','Stregone'),('Ladro','Ricercatore')]:
    s=re.sub(r'\b'+a+r'\b',b,s)
s=s.replace('il Stregone','lo Stregone').replace('Il Stregone','Lo Stregone')
open('docx/reg_docx.html','w').write(s)
print('ok', s.count('class="dd"'))
s=open('docx/reg_docx.html').read()
s=s.replace('il Assaltatore','l’Assaltatore').replace('Il Assaltatore','L’Assaltatore')
a='<i>Da decidere: il mazzetto'; assert s.count(a)==1
s=s.replace(a,'<span class="dd">Da decidere: il mazzetto'); s=s.replace('2: mazzetto 3).</i>','2: mazzetto 3).</span>')
open('docx/reg_docx.html','w').write(s); print('ok2', s.count('class="dd"'))
