import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build
from svg import *
from parts import *
S=build.STYLE.replace('@page { size: 154mm 216mm; margin: 0 }','@page { size: 216mm 303mm; margin: 0 }').replace('.page{width:154mm;height:216mm','.page{width:216mm;height:303mm')
S+=f"""
body{{font-size:11.5pt}}
.in{{left:18mm;right:18mm;top:17mm;bottom:17mm}}
.frame{{left:10mm;right:10mm;top:10mm;bottom:10mm}}
h1{{font-size:26pt;text-align:center;margin-bottom:1mm}}
.sub{{text-align:center;font-family:'Cinzel';font-weight:600;color:{BROWN};font-size:11pt;margin-bottom:5mm}}
.steps{{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm 6mm}}
.st2{{display:flex;gap:3mm;align-items:flex-start;background:#fffaf0;border:0.4mm solid {BROWN};border-radius:2.5mm;padding:3mm}}
.st2 .n{{flex:none;width:10mm;height:10mm;border-radius:50%;background:{RED};color:#fff;font-family:'Cinzel';font-weight:800;font-size:15pt;line-height:10mm;text-align:center}}
.st2 h3{{font-family:'Cinzel';font-weight:800;font-size:12pt;margin:0 0 1mm;color:{INK}}}
.st2 p{{margin:0;font-size:10.6pt;line-height:1.35}}
.bigbox{{background:#fffaf0;border:0.5mm solid {RED};border-radius:3mm;padding:4mm 5mm;margin:4mm 0}}
.bigbox h2{{margin-top:0;color:{RED};font-size:14pt}}
"""
pg=[]
pg.append(f'''<section class="page"><div class="frame"></div><div class="in">
<h1>Inizia subito</h1><div class="sub">Leggimi per primo · in 5 minuti siete in gioco</div>
<div class="cols" style="align-items:center;margin-bottom:4mm"><div style="flex:1.15">{board(W=18,heroes=[(2,0,BLUE),(7,9,RED)])}</div>
<div style="flex:1"><p class="lead"><b>Lo scopo:</b> esplora la mappa, raccogli <b>3 Indizi</b>, scopri in quale Cripta è nascosto il forziere MIMI e sconfiggi il suo <b>Guardiano</b>.</p><p>Il tavolo pronto per due giocatori è così: i due eroi partono da punti di partenza tirati con il D6, le caselle «?» stampate sulla mappa (i segnalini si pescano dal sacchetto), i mostri che aspettano nella Sala del Tesoro.</p></div></div>
<div class="steps">
<div class="st2"><div class="n">1</div><div><h3>Apri la plancia</h3><p>Al centro del tavolo, con la Sala del Tesoro verso chi la sa raggiungere.</p></div></div>
<div class="st2"><div class="n">2</div><div><h3>Prepara il sacchetto</h3><p>Metti i 30 segnalini Esplorazione nel sacchetto e mescolali. Guardiano, MIMI e i 4 mini-boss vanno sulle loro sagome. Un cubetto giallo sul giro 1, l’altro sul 14 dei PV del Guardiano.</p></div></div>
<div class="st2"><div class="n">3</div><div><h3>Scegli il tuo eroe</h3><p>Dalla Galleria: Guerriero, Ladro, Mago o Chierico, con il mazzetto dello stesso colore (non guardare le carte). Poi una Tessera Razza: Umano, Elfo, Nano o Orco.</p></div></div>
<div class="st2"><div class="n">4</div><div><h3>Prepara la scheda</h3><p>Incastra la Tessera Razza. Cubetti rosso e nero su PV 10; gli altri su ATT 1, MOV 1, AR 1, PE 0. Aggiungi il bonus della razza. Infila la Carta Classe nel primo slot.</p></div></div>
<div class="st2"><div class="n">5</div><div><h3>Tira il D6</h3><p>Metti l’eroe sul punto di partenza con quel numero. Occupato o accanto a un altro eroe? Ritira.</p></div></div>
<div class="st2"><div class="n">6</div><div><h3>Pesca la mano coperta</h3><p>5 carte della tua classe + 5 comuni, coperte. Solo ora guardate le vostre 10 carte e, tutti insieme, equipaggiate subito un oggetto. Chi ha visto per ultimo un goblin prende Geronimo e comincia. Gira il foglio!</p></div></div>
</div></div></section>''')
pg.append(f'''<section class="page"><div class="frame"></div><div class="in">
<h1>Il tuo primo turno</h1><div class="sub">Sempre 5 passi, sempre in quest’ordine</div>
{turn_strip(big=True)}
<div class="bigbox"><h2>Hai trovato un mostro?</h2>
<div class="cols" style="align-items:center"><div style="flex:none">{token('Lupo grigio',5,'+3',10,'D6−1',120)}</div><div>
<p><b>1.</b> Tira il <b>D20 + il tuo ATT</b>. Se arrivi alla <b>Difesa</b> del mostro (qui 10) lo colpisci: tira il danno (D6 − 1 a mani nude, minimo 1; D6 con un’arma, D6+1 con un’arma a due mani).</p>
<p><b>2.</b> Ora l’avversario tira per il mostro: D20 + ATT del mostro contro la tua Difesa. Se ti colpisce, tira il suo danno.</p>
<p><b>3.</b> Avanti così finché qualcuno arriva a 0 PV. Il dado rosso conta i PV del mostro.</p>
<p style="margin:0"><b>Vinci?</b> Prendi 1 Indizio e 1 PE. <b>Perdi?</b> Tiri il D6 e riparti da quel punto con i PV pieni e tiri il D6 per vedere cosa perdi.</p></div></div></div>
<div class="cols">
<div class="box"><h3>Le altre caselle</h3><p style="margin:0">{build.I('casa',LOC)}<b>Locanda</b>: +1 PE e +2 PV<br>{build.I('goccia',FON)}<b>Fonte</b>: riprendi 2 carte dagli scarti<br>{build.I('martello',FAB)}<b>Fabbro</b>: riprendi 1 equipaggiamento<br><i>Ogni edificio funziona una volta per eroe.</i><br>{build.I('trappola')}<b>Trappola</b>: perdi D6 − 1 PV<br><b>«?»</b>: pesca un segnalino dal sacchetto</p></div>
<div class="box red"><h3>Come si vince</h3><p style="margin:0">Al <b>terzo Indizio</b> ogni altro eroe prende 1 Indizio e tu tiri il D6 (con 5 o 6 ritira): MIMI e il Guardiano vanno nella Cripta con quel numero. Raggiungila, sconfiggi il Guardiano (14 PV, ATT +4, Difesa 13) e hai vinto! Se perdi, le sue ferite restano.<br><b>Dal giro 8</b> chi non ha 3 Indizi tira il D6 a inizio turno: con il numero del tracciato prende 1 Indizio.</p></div>
</div>
<p class="tip" style="text-align:center;font-size:10.5pt;margin-top:4mm">Tutto il resto lo trovi nel regolamento quando ti serve. Buona caccia!</p>
</div></section>''')
html=f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Il Tesoro del Goblin – Inizia subito</title><style>{S}</style></head><body>{"".join(pg)}</body></html>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'inizia.html'),'w').write(html)
