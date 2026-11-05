import re
def rep(s,a,b):
    assert s.count(a)==1, ('miss' if a not in s else 'multi', a[:80]); return s.replace(a,b)
s=open('build.py').read()
R=[
("25–30 minuti · sistema D20","25–30 minuti · solo dadi a 6 facce"),
("<div><b>5</b> Dadi: 2 D20, 2 D6, 1 D20 rosso</div>","<div><b>4</b> Dadi a 6 facce (D6), uno per giocatore</div>"),
("<b>Il dado rosso</b> non si tira: segna i PV del mostro.","<b>I PV del mostro</b>: mettigli sopra un cubetto Durata per ogni PV."),
("Si somma al D20 quando attacchi.","Si somma ai 2D6 quando attacchi."),
("Ti dà la <b>Difesa</b> (14 + AR)","Ti dà la <b>Difesa</b> (8 + AR)"),
("prima il <b>tiro per colpire</b> con il D20, poi","prima il <b>tiro per colpire</b> con <b>2D6</b> (il tuo dado e quello del vicino), poi"),
("Tiro per colpire: D20 + il tuo ATT. Se il totale arriva alla <b>Difesa</b> del nemico (14 + la sua AR)","Tiro per colpire: 2D6 + il tuo ATT. Se il totale arriva alla <b>Difesa</b> del nemico (8 + la sua AR)"),
("D20 + ATT del nemico contro la tua Difesa (14 + la tua AR)","2D6 + ATT del nemico contro la tua Difesa (8 + la tua AR)"),
("I PV del nemico si contano con il dado rosso; i tuoi con il cubetto rosso.","Ogni danno al nemico toglie un cubetto Durata dalla sua carta; i tuoi PV li segna il cubetto rosso."),
("<h3>20 sul dado</h3><p style=\"margin:0\">Colpisci sempre e il danno raddoppia.</p>","<h3>Doppio 6</h3><p style=\"margin:0\">Colpisci sempre e il danno raddoppia.</p>"),
("<h3>1 sul dado</h3><p style=\"margin:0\">Manchi sempre, qualunque sia il totale.</p>","<h3>Doppio 1</h3><p style=\"margin:0\">Manchi sempre, qualunque sia il totale.</p>"),
("AR 1 quindi Difesa 15, PV 7.","AR 1 quindi Difesa 9, PV 6."),
("AR 0 quindi Difesa 14. È di LV 1: il suo danno è D6 − 1. Lia gira il dado rosso sul 3.","AR 0 quindi Difesa 8. È di LV 1: il suo danno è D6 − 1. Lia mette 3 cubetti Durata sulla carta."),
("<td>12 + 3 = 15</td><td>15 ≥ 14: colpito! Tiro per il danno: D6 = 2. Dado rosso: da 3 a 1.</td>","<td>4 + 2 + 3 = 9</td><td>9 ≥ 8: colpito! Tiro per il danno: D6 = 2. Toglie 2 cubetti: ne resta 1.</td>"),
("<td>13 + 3 = 16</td><td>16 ≥ 15: colpita. Danno: esce 4, meno 1 = 3. Lia scende a 4 PV.</td>","<td>5 + 3 + 3 = 11</td><td>11 ≥ 9: colpita. Danno: esce 4, meno 1 = 3. Lia scende a 3 PV.</td>"),
("<td>6 + 3 = 9</td><td>9 &lt; 14: mancato.</td>","<td>1 + 3 + 3 = 7</td><td>7 &lt; 8: mancato.</td>"),
("<td>4 + 3 = 7</td><td>7 &lt; 15: mancato.</td>","<td>2 + 1 + 3 = 6</td><td>6 &lt; 9: mancato.</td>"),
("<td>15 + 3 = 18</td><td>Colpito! Danno: D6 = 5. Il lupo è a 0.</td>","<td>5 + 4 + 3 = 12</td><td>Colpito! Danno: D6 = 5. Il lupo è a 0.</td>"),
("tiri due D20 e tieni il migliore; con lo <b>svantaggio</b> il peggiore.","tiri due volte i 2D6 e tieni il totale migliore; con lo <b>svantaggio</b> il peggiore."),
("<b>9 PV, ATT +4, Difesa 17</b>","<b>9 PV, ATT +4, Difesa 11</b>"),
("colpisci se <b>D20 + ATT ≥ 14 + AR</b>.","colpisci se <b>2D6 + ATT ≥ 8 + AR</b>."),
("20 = colpo doppio · 1 = mancato.","Doppio 6 = colpo doppio · doppio 1 = mancato."),
("Se fuggi o perdi, resta scoperta: chi si ferma lì gira la carta del suo mazzetto. La carta va in fondo.</td></tr>",
 "Se fuggi o perdi, resta scoperta: chi si ferma lì gira la carta del suo mazzetto. La carta va in fondo.<br><i>Da decidere: il mazzetto si sceglie dal livello o dagli Indizi (0: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3).</i></td></tr>"),
]
for a,b in R: s=rep(s,a,b)
open('build.py','w').write(s)
t=open('inizia.py').read()
for a,b in [("PV 5 (Guerriero 7)","PV 5 (Guerriero 6)"),
("D20 + il tuo ATT. Se arrivi alla <b>Difesa</b> del mostro (14 + AR, qui 14)","<b>2D6</b> (il tuo dado e quello del vicino) + il tuo ATT. Se arrivi alla <b>Difesa</b> del mostro (8 + AR, qui 8)"),
("D20 + ATT del mostro contro la tua Difesa.","2D6 + ATT del mostro contro la tua Difesa."),
("Il dado rosso conta i PV del mostro.","Un cubetto Durata sulla carta per ogni PV del mostro: ogni danno ne toglie uno.")]: t=rep(t,a,b)
open('inizia.py','w').write(t)
p=open('parts.py').read()
p=rep(p,"fill=\"{BLUE}\">{14+i}</text>","fill=\"{BLUE}\">{8+i}</text>")
p=rep(p,"Difesa (14 + AR): già stampata","Difesa (8 + AR): già stampata")
open('parts.py','w').write(p)
print('ok')
