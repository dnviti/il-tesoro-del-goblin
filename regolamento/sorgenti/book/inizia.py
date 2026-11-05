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
<div style="flex:1"><p class="lead"><b>Lo scopo:</b> esplora la mappa, raccogli <b>2 Indizi</b>, scopri in quale Cripta è nascosto il forziere MIMI e sconfiggi il <b>boss</b> che lo custodisce.</p><p>Il tavolo pronto per due giocatori è così: i due eroi partono da punti di partenza tirati con il D6, le caselle «?» stampate sulla mappa (le tessere rosse e blu si pescano dal sacchetto), i boss che aspettano nella Sala del Tesoro.</p></div></div>
<div class="steps">
<div class="st2"><div class="n">1</div><div><h3>Apri la plancia</h3><p>Al centro del tavolo, con la Sala del Tesoro verso chi la sa raggiungere.</p></div></div>
<div class="st2"><div class="n">2</div><div><h3>Prepara il sacchetto</h3><p>Metti le 36 tessere Esplorazione nel sacchetto e mescolale. Mescola il mazzetto Imprevisti e i mazzetti Mostri 1 e 2. Pesca 1 dei 3 Boss: custodisce MIMI, gli altri 2 sono il mazzetto 3. Boss e MIMI sulle sagome, cubetto giallo sui PV del boss.</p></div></div>
<div class="st2"><div class="n">3</div><div><h3>Scegli il tuo eroe</h3><p>Dalla Galleria: Guerriero, Ladro, Mago o Oracolo, con il mazzetto dello stesso colore. Poi una Tessera Specie: Umano, Elfo, Nano, Orco o Sanguar.</p></div></div>
<div class="st2"><div class="n">4</div><div><h3>Prepara la scheda</h3><p>Incastra la Tessera Specie. Cubetti rosso e nero su PV 5 (Guerriero 6); gli altri su ATT 1, MOV 1, AR 1, PE 0. Aggiungi il bonus della specie. Infila la Carta Classe nel primo slot. Si parte senza Indizi.</p></div></div>
<div class="st2"><div class="n">5</div><div><h3>Tira il D6</h3><p>Metti l’eroe sul punto di partenza con quel numero. Occupato o accanto a un altro eroe? Ritira.</p></div></div>
<div class="st2"><div class="n">6</div><div><h3>Fai la mano</h3><p>Scegli 5 carte della tua classe (il Mago le sue 4 + 1 comune). Casual: pesca 5 comuni. Draft: 5 comuni a testa, tienine 1 e passa a destra finché finiscono. Tutti insieme equipaggiate subito un oggetto. Chi ha visto per ultimo un goblin prende Geronimo e comincia. Gira il foglio!</p></div></div>
</div></div></section>''')
pg.append(f'''<section class="page"><div class="frame"></div><div class="in">
<h1>Il tuo primo turno</h1><div class="sub">Sempre 5 passi, sempre in quest’ordine</div>
{turn_strip(big=True)}
<div class="bigbox"><h2>Hai trovato un mostro?</h2>
<div class="cols" style="align-items:center"><div style="flex:none">{enemy_card('Lupo grigio','L',1,3,3,0,['1 indizio','1 punto esperienza'],w=260)}</div><div>
<p>Pesca la tessera: è <b>rossa</b>? È un Mostro. Sei di livello 1, quindi gira la prima carta del <b>mazzetto 1</b>.</p>
<p><b>1.</b> <b>Tiro per colpire</b>: <b>2D6</b> (il tuo dado e quello del vicino) + il tuo ATT. Se arrivi alla <b>Difesa</b> del mostro (8 + AR, qui 8) lo colpisci. <b>Tiro per il danno</b>: D6, più i bonus delle tue carte.</p>
<p><b>2.</b> Ora l’avversario tira per il mostro: 2D6 + ATT del mostro contro la tua Difesa. Se ti colpisce, tira il suo danno: D6 − 1 al LV 1, D6 al LV 2, D6 + 1 dal LV 3.</p>
<p><b>3.</b> Avanti così finché qualcuno arriva a 0 PV. Un cubetto Durata sulla carta per ogni PV del mostro: ogni danno ne toglie uno.</p>
<p style="margin:0"><b>Vinci?</b> Prendi 1 Indizio e 1 PE. <b>Perdi?</b> Tiri il D6 e riparti da quel punto con i PV pieni e tiri il D6 per vedere cosa perdi.</p></div></div></div>
<div class="cols">
<div class="box"><h3>Tessera blu: Imprevisto</h3><p style="margin:0">Gira la prima carta del mazzetto Imprevisti:<br>{build.I('casa',LOC)}<b>Locanda</b>: +1 PE e +2 PV<br>{build.I('goccia',FON)}<b>Fonte</b>: riprendi 2 carte dagli scarti<br>{build.I('martello',FAB)}<b>Fabbro</b>: riprendi 1 equipaggiamento<br>{build.I('trappola')}<b>Trappola</b>: perdi D6 − 1 PV<br><i>Vale per chi la gira; poi la carta va in fondo.</i></p></div>
<div class="box red"><h3>Come si vince</h3><p style="margin:0">Al <b>secondo Indizio</b> ogni altro eroe prende 1 Indizio e tu tiri il D6 (con 5 o 6 ritira): MIMI e il boss vanno nella Cripta con quel numero. Raggiungila, sconfiggi il boss e hai vinto! Se perdi, le sue ferite restano.<br>Gli Indizi si prendono <b>solo vincendo uno scontro</b> su una casella «?» (o un Duello).</p></div>
</div>
<p class="tip" style="text-align:center;font-size:10.5pt;margin-top:4mm">Tutto il resto lo trovi nel regolamento quando ti serve. Buona caccia!<br><span style="font-size:8.5pt;color:#6b4a2b">Il Tesoro del Goblin · un gioco di Alessandro De Simone</span></p>
</div></section>''')
html=f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Il Tesoro del Goblin – Inizia subito</title><style>{S}</style></head><body>{"".join(pg)}</body></html>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'inizia.html'),'w').write(html)
