import sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from svg import *
from parts import *

CSS = open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','fonts','fonts.css')).read().replace("url(", "url(../fonts/")
STYLE = CSS + f"""
@page {{ size: 154mm 216mm; margin: 0 }}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:'Alegreya',serif;color:{INK};font-size:10.4pt;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:154mm;height:216mm;position:relative;overflow:hidden;background:{PAPER};page-break-after:always;break-after:page}}
.page::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.35),rgba(0,0,0,0) 60%),radial-gradient(ellipse at 50% 120%,rgba(107,74,43,.18),rgba(0,0,0,0) 60%);pointer-events:none}}
.frame{{position:absolute;left:9mm;right:9mm;top:9mm;bottom:9mm;border:0.5mm solid {GOLD};border-radius:2mm;opacity:.55}}
.in{{position:absolute;left:15mm;right:15mm;top:14mm;bottom:15mm}}
.folio{{position:absolute;bottom:10.5mm;left:0;right:0;text-align:center;font-family:'Cinzel';font-weight:600;font-size:7.5pt;color:{BROWN}}}
h1{{font-family:'Cinzel';font-weight:800;font-size:17pt;margin:0 0 2.5mm;color:{RED};letter-spacing:.3px;line-height:1.1}}
h2{{font-family:'Cinzel';font-weight:800;font-size:11pt;margin:3.5mm 0 1.5mm;color:{BROWN}}}
p{{margin:0 0 2mm}}
.lead{{font-size:11.3pt;line-height:1.35;margin-bottom:3mm}}
.sans{{font-family:'Alegreya Sans',sans-serif}}
ol,ul{{margin:0 0 2mm;padding-left:5mm}} li{{margin-bottom:1.2mm}}
b{{font-weight:700}}
.box{{background:#fffaf0;border:0.35mm solid {BROWN};border-radius:2mm;padding:2.5mm 3.2mm;margin:2.5mm 0}}
.box.red{{border-color:{RED};background:#fbefe6}}
.box h3{{font-family:'Cinzel';font-weight:800;font-size:9.5pt;margin:0 0 1.2mm;color:{RED}}}
.tip{{font-family:'Alegreya Sans';font-size:9.1pt;color:{BROWN};font-style:normal}}
table{{border-collapse:collapse;width:100%;font-family:'Alegreya Sans';font-size:9.4pt;margin:1.5mm 0 2.5mm}}
th{{text-align:left;font-weight:800;color:{BROWN};border-bottom:0.4mm solid {BROWN};padding:1mm 1.2mm}}
td{{border-bottom:0.2mm solid {LINE};padding:1.05mm 1.2mm;vertical-align:top}}
.ic{{width:5mm;height:5mm;vertical-align:-1.3mm;margin-right:1mm}}
.strip{{display:flex;gap:1.6mm;margin:2mm 0}}
.step{{flex:1;background:#fffaf0;border:0.35mm solid {BROWN};border-radius:2mm;padding:2mm 1.4mm 2mm;text-align:center;position:relative}}
.step .num{{position:absolute;top:-2.6mm;left:50%;transform:translateX(-50%);width:5.2mm;height:5.2mm;border-radius:50%;background:{RED};color:#fff;font-family:'Cinzel';font-weight:800;font-size:8pt;line-height:5.2mm}}
.step .sic{{width:8mm;height:8mm;margin-top:1.4mm}}
.step .st{{font-family:'Cinzel';font-weight:800;font-size:8pt;color:{INK};margin:.6mm 0 .8mm}}
.step .sd{{font-family:'Alegreya Sans';font-size:8pt;line-height:1.25}}
.strip.big .step .sd{{font-size:9.2pt}} .strip.big .step .st{{font-size:10pt}} .strip.big .step .sic{{width:11mm;height:11mm}}
.cols{{display:flex;gap:5mm}} .cols>div{{flex:1}}
.comp{{display:grid;grid-template-columns:1fr 1fr;gap:1.3mm 4mm;font-family:'Alegreya Sans';font-size:9.3pt}}
.comp div{{border-bottom:0.2mm solid {LINE};padding:.6mm 0}}
.comp b{{color:{RED};font-family:'Cinzel';font-size:9pt;display:inline-block;min-width:8mm}}
.tokens{{display:flex;flex-wrap:wrap;gap:2mm;justify-content:center;align-items:center;margin:2mm 0}}
.tokens .t{{text-align:center;font-family:'Alegreya Sans';font-size:7.6pt;color:{BROWN}}}
.ex td{{font-size:9.2pt}}
.hit{{color:#3d6b3f}}
.cover{{background:#2b1d14}}
.cover::before{{background:radial-gradient(ellipse at 50% 42%,rgba(246,214,139,.25),rgba(0,0,0,0) 60%)}}
.cover .t1{{position:absolute;top:24mm;left:0;right:0;text-align:center;font-family:'Cinzel';font-weight:600;font-size:12pt;color:{GOLD};letter-spacing:3px}}
.cover .t2{{position:absolute;top:31mm;left:0;right:0;text-align:center;font-family:'Cinzel';font-weight:800;font-size:31pt;line-height:1.02;color:#f6d68b;text-shadow:0 1mm 0 #00000088}}
.cover .art{{position:absolute;top:80mm;left:22mm;right:22mm}}
.cover .t3{{position:absolute;top:162mm;left:0;right:0;text-align:center;font-family:'Alegreya';font-style:italic;font-size:11pt;color:#efe2c2}}
.cover .t4{{position:absolute;bottom:22mm;left:0;right:0;text-align:center;font-family:'Cinzel';font-weight:600;font-size:9pt;color:{GOLD};letter-spacing:1px}}
.cover .t5{{position:absolute;bottom:15mm;left:0;right:0;text-align:center;font-family:'Alegreya Sans';font-size:8pt;color:#cbb88e}}
.cover .frame{{border-color:{GOLD};opacity:.8}}
.lg{{display:inline-flex;align-items:center;gap:1.2mm;margin-right:3mm;font-family:'Alegreya Sans';font-size:9.2pt}}
.fig{{text-align:center;margin:2mm 0}}
.fig svg{{max-width:100%}}
.cap{{font-family:'Alegreya Sans';font-size:7.8pt;color:{BROWN};text-align:center;margin-top:1mm}}
.qa b{{display:block;font-family:'Alegreya Sans';font-weight:800;color:{RED};font-size:8.8pt}}
.qa p{{margin-bottom:2.2mm}}
""".replace('{GREEN}','#3d6b3f')

def I(name,col=INK): return f'<svg class="ic" viewBox="0 0 24 24">{icon(name,12,12,1,col)}</svg>'

pages=[]
def page(body, n=None, cls=''):
    folio=f'<div class="folio">{n}</div>' if n else ''
    pages.append(f'<section class="page {cls}"><div class="frame"></div><div class="in">{body}</div>{folio}</section>')

# 1 cover
pages.append(f'''<section class="page cover"><div class="frame"></div>
<div class="t1">REGOLAMENTO</div><div class="t2">Il Tesoro<br>del Goblin</div>
<div class="art">{cover_art()}</div>
<div class="t3">«Un’avventura tra tesori, alleati e trappole.»</div>
<div class="t4">SCATOLA BASE</div><div class="t5">2–4 giocatori · dai 10 anni · 25–30 minuti · sistema D20</div></section>''')

# 2 storia
page(f'''<h1>La storia di Geronimo</h1>
<p class="lead">Nelle terre del Piano Materiale di Hande vive Geronimo, un goblin che ne ha viste di tutti i colori. È stato rapito dagli umani, schiavizzato dagli gnomi e persino scambiato per una gallina dai Goliath.</p>
<p>Eppure Geronimo ha sempre trovato oggetti preziosi, rari e persino <b>leggendari</b>. Li metteva tutti nella sua inseparabile cassa senza fondo, che chiamava affettuosamente <b>MIMI</b>.</p>
<p>Un giorno, per proteggere il suo forziere, decise di imparare la magia. Combinò un piccolo… insignificante pasticcio: <b>MIMI scomparve nel nulla</b>, e con lei un Guardiano che non fa avvicinare nessuno.</p>
<p>Ora Geronimo cerca avventurieri coraggiosi (e possibilmente competenti) che lo aiutino a ritrovarla. Naturalmente, pagherà il giusto prezzo.</p>
<div class="box red"><h3>Il gioco in una frase</h3>
<p style="margin:0;font-size:10.5pt">Esplora la mappa, raccogli <b>3 Indizi</b>, scopri in quale Cripta si nasconde MIMI e sconfiggi il suo <b>Guardiano</b>. Chi ci riesce per primo vince.</p></div>
<h2>Come leggere questo libretto</h2>
<p>Se è la vostra prima partita, usate il foglio <b>Inizia subito</b>: in 5 minuti siete al tavolo. Questo regolamento serve quando nasce una domanda. I nomi in <b>grassetto</b> sono gli stessi stampati sulla scatola, sulla plancia e sulle carte.</p>
<p class="tip">Nelle carte trovi a volte PF e CA: sono i PV e l’AR della scheda.</p>''', 2)

# 3 contenuto
page(f'''<h1>Cosa c’è nella scatola</h1>
<div class="comp">
<div><b>1</b> Plancia «Le Terre di Hande»</div><div><b>4</b> Schede eroe a doppio strato</div>
<div><b>4</b> Miniature eroe: Guerriero, Ladro, Mago, Chierico</div><div><b>1</b> Guardiano di MIMI (il boss)</div>
<div><b>1</b> MIMI, il forziere</div><div><b>4</b> Mini-boss</div>
<div><b>1</b> Geronimo (primo giocatore)</div><div><b>4</b> Carte Classe</div>
<div><b>28</b> Carte di classe (7 per classe)</div><div><b>20</b> Carte comuni</div>
<div><b>4</b> Carte Aiuto</div><div><b>5</b> Divisori per i mazzi</div>
<div><b>30</b> Segnalini Esplorazione</div><div><b>8</b> Tessere Razza</div>
<div><b>12</b> Indizi</div><div><b>12</b> Clessidre</div>
<div><b>4</b> Ispirazione</div><div><b>32</b> Cubetti Durata (bianchi)</div>
<div><b>24</b> Cubetti statistica (4 set)</div><div><b>2</b> Cubetti Giro e Guardiano (gialli)</div><div><b>5</b> Dadi: 2 D20, 2 D6, 1 D20 rosso</div><div><b>1</b> Sacchetto dei segnalini</div>
</div>
<h2>I segnalini Esplorazione</h2>
<p>Hanno tutti lo stesso dorso «?». Sotto può esserci:</p>
<div class="tokens">
<div class="t">{back_token(56)}<br>dorso</div>
<div class="t">{token('Lupo grigio',5,'+3',10,'D6−1',92)}<br>13 Creature</div>
<div class="t">{simple_token('teschio','Mini-boss',RED,60)}<br>4 Mini-boss</div>
<div class="t">{simple_token('trappola','Trappola',INK,60)}<br>5 Trappole</div>
<div class="t">{simple_token('piedi','Sentiero',BROWN,60)}<br>8 Sentieri tranquilli</div>
</div>
<p class="tip" style="text-align:center">Sulle creature leggi: {I('cuore',RED)}PV · {I('spade')}ATT · {I('scudo',BLUE)}Difesa · danno</p>
<div class="box"><h3>Il dado rosso</h3><p style="margin:0">Non si tira: serve a contare i PV del mostro che stai combattendo. Giralo sul numero dei suoi PV e abbassalo a ogni colpo.</p></div>''', 3)

# 4 plancia
page(f'''<h1>La plancia</h1>
<p>La mappa ha 10 × 10 esagoni. Girata di 180° è identica: ogni partenza ha di fronte quella con il numero più 3. In alto c’è la <b>Sala del Tesoro</b>, dove aspettano i mostri; in basso il <b>Promemoria</b>.</p>
<div class="fig" style="width:84%;margin-left:auto;margin-right:auto">{board(W=20)}</div>
<div style="margin-top:1mm">
{legend_item(f'<polygon points="{hexpts(12,12,11)}" fill="{CAMP}" fill-opacity=".55"/>','Partenze 1–6: si tira il D6')}<br>
{legend_item(icon('casa',12,12,1,LOC),'Locanda')}{legend_item(icon('goccia',12,12,1,FON),'Fonte')}{legend_item(icon('martello',12,12,1,FAB),'Fabbro')}{legend_item(q_mark(12,12,9),'Casella ?')}<br>
{legend_item(f'<polygon points="{hexpts(12,12,11)}" fill="{GOLD}" fill-opacity=".5" stroke="{GOLD}"/>','Cripte 1–4: una nasconde MIMI')}{legend_item(f'<rect x="2" y="5" width="20" height="14" fill="{CUORE}" stroke="{GOLD}" stroke-dasharray="3 2"/>','Il Cuore')}
</div>''', 4)

# 5 preparazione
page(f'''<h1>Preparazione</h1>
<ol>
<li><b>Apri la plancia</b> al centro del tavolo.</li>
<li><b>Prepara il sacchetto.</b> Metti i 30 segnalini Esplorazione nel sacchetto e mescolali: sulla mappa non si piazza niente. Metti Guardiano, MIMI e i 4 mini-boss sulle loro sagome nella Sala del Tesoro. Un cubetto giallo va sul giro 1, l’altro sul 14 dei PV del Guardiano.</li>
<li><b>Scegli il tuo eroe.</b> Ognuno prende una classe diversa: la miniatura e il mazzetto dello stesso colore, senza guardarne le carte. Poi sceglie una Tessera Razza.</li>
<li><b>Prepara la scheda</b> (pagina accanto). Incastra la Tessera Razza e infila la Carta Classe nel primo slot in alto: il suo effetto vale da subito e per tutta la partita.</li>
<li><b>Tira il D6</b> e metti la miniatura sul punto di partenza con quel numero. Se è occupato o è accanto a un altro eroe, ritira.</li>
<li><b>Pesca la mano coperta.</b> Mescola le 7 carte della tua classe e pescane 5 coperte; le altre 2 tornano nella scatola senza che nessuno le veda. Mescolate le 20 carte comuni e pescatene 5 coperte a testa. <b>Solo adesso</b> ognuno guarda le sue 10 carte: non ne pescherà altre. Tutti insieme potete equipaggiare subito un oggetto dalla mano: non conta come quello del primo turno. Chi ha visto per ultimo un goblin prende Geronimo e gioca per primo; poi si va in senso orario.</li>
</ol>
<h2>Le razze</h2>
<table><tr><th>Razza</th><th>Bonus da aggiungere subito</th></tr>
<tr><td><b>Umano</b></td><td>+1 MOV e +1 a una statistica a scelta</td></tr>
<tr><td><b>Elfo</b></td><td>+2 a una statistica a scelta</td></tr>
<tr><td><b>Nano</b></td><td>+1 a due statistiche diverse a scelta</td></tr>
<tr><td><b>Orco</b></td><td>+2 ATT e +1 PV</td></tr></table>
<p class="tip">Statistiche a scelta: PV, ATT, MOV o AR. Un +1 ai PV sposta sia il cubetto rosso sia quello nero.</p>
<div class="box"><h3>In 3 o 4 giocatori</h3><p style="margin:0">Ognuno tira il D6 per la sua partenza, con la stessa regola. Se una carta dice «un avversario» o «l’avversario», scegli tu quale giocatore; se dice «ogni avversario» o «entrambi i giocatori», vale per tutti.</p></div>''', 5)

# 6 scheda
page(f'''<h1>La tua scheda eroe</h1>
<p>La scheda tiene il conto al posto tuo. Ogni cubetto mostra il valore <b>finale</b>: quando equipaggi un oggetto o sali di livello, sposti subito il cubetto. Durante lo scontro leggi solo numeri già pronti.</p>
<div class="fig" style="margin:1mm 0">{scheda()}</div>
<table><tr><th>Statistica</th><th>Serve a</th></tr>
<tr><td>{I('cuore',RED)}<b>PV</b></td><td><b>Punti Vita.</b> Quanti colpi reggi. A 0 sei sconfitto.</td></tr>
<tr><td>{I('spade')}<b>ATT</b></td><td><b>Attacco.</b> Si somma al D20 quando attacchi.</td></tr>
<tr><td>{I('stivale',BROWN)}<b>MOV</b></td><td><b>Movimento.</b> Si somma al D6 quando ti muovi.</td></tr>
<tr><td>{I('scudo',BLUE)}<b>AR</b></td><td><b>Armatura.</b> Ti dà la <b>Difesa</b> (10 + AR), il numero che i nemici devono raggiungere.</td></tr>
<tr><td>{I('stella',GOLD)}<b>PE</b></td><td><b>Esperienza.</b> Ti fa salire di livello.</td></tr></table>
''', 6)

# 7 turno
page(f'''<h1>Il turno in 5 passi</h1>
<p class="lead">Al tuo turno fai sempre questi 5 passi, in quest’ordine. Li trovi anche sulla plancia e sulla tua Carta Aiuto.</p>
{turn_strip(big=True)}
<h2>1 · Clessidre</h2>
<p>Se sulla tua scheda c’è almeno una Clessidra, toglila: salti il turno e fai solo il passo 5.</p>
<h2>2 · Carte</h2>
<p>In tutto il turno puoi giocare <b>fino a 2 carte</b>, quando vuoi: prima di muoverti, dopo, o durante uno scontro. Al massimo <b>una</b> può essere un equipaggiamento. Le pozioni contano come carte. Le carte giocate vanno nei tuoi <b>scarti</b>, a faccia in su, a meno che restino in gioco (equipaggiamenti ed effetti che durano).</p>
<h2>3 · Muovi</h2>
<p>Tira il D6 e aggiungi il tuo MOV. Ti muovi di quel numero di esagoni o meno, ma almeno di 1, in qualsiasi direzione.</p>
<h2>4 · Esplora</h2>
<p>Guarda dove ti sei fermato e risolvi quello che c’è (pagina 9). C’è al massimo <b>uno scontro per turno</b>.</p>
<h2>5 · Fine</h2>
<p>Togli un cubetto Durata da ogni tua carta con la clessidra. Una carta senza cubetti va negli scarti. Passa i dadi al giocatore a sinistra.</p>''', 7)

# 8 movimento
page(f'''<h1>Muoversi</h1>
<p class="lead">Conta solo l’esagono dove ti fermi. Puoi passare sopra a tutto: caselle «?», edifici, mostri, altri eroi.</p>
<div class="fig">{move_example()}</div>
<ul>
<li>Ti muovi di un esagono alla volta, in qualsiasi direzione, e puoi cambiare direzione quando vuoi.</li>
<li>Non puoi fermarti sull’esagono di un altro eroe.</li>
<li>Ti devi muovere ogni turno: per questo non puoi usare lo stesso edificio due turni di fila.</li>
<li>Se una carta ti dà MOV in più «fino alla fine del turno», sommalo al tiro senza spostare cubetti.</li>
</ul>
<div class="box"><h3>Quanto è grande la mappa?</h3><p style="margin:0">Da ogni punto di partenza la Cripta più vicina è a 3 esagoni, la più lontana a 7: 1 o 2 turni di cammino con D6 + MOV 1. Ma lungo la strada ci sono caselle «?» che conviene esplorare: servono Indizi!</p></div>
<h2>Turni extra</h2>
<p>Se una carta ti fa «recuperare» o «guadagnare» turni, prima togli le tue Clessidre. Ogni turno che avanza lo giochi subito dopo quello in corso.</p>''', 8)

# 9 esplorare
page(f'''<h1>Esplorare</h1>
<p class="lead">Quando ti fermi, guarda l’esagono e fai quello che dice la tabella.</p>
<table>
<tr><th style="width:36%">Dove ti fermi</th><th>Cosa succede</th></tr>
<tr><td><b>Casella «?»</b></td><td>Pesca un segnalino dal sacchetto e risolvilo. A sacchetto vuoto non succede niente.</td></tr>
<tr><td>{I('spade')}<b>Creatura</b></td><td>Scontro, oppure fuga (pagina 10). Se vinci il segnalino si toglie; se fuggi o perdi lo lasci scoperto su quella casella.</td></tr>
<tr><td>{I('teschio',RED)}<b>Mini-boss</b></td><td>Metti sulla casella la sua miniatura, presa dalla Sala del Tesoro (statistiche sulla sagoma). Poi scontro o fuga.</td></tr>
<tr><td>{I('trappola')}<b>Trappola</b></td><td>Perdi D6 − 1 PV (minimo 1) e tira il D6 della perdita di equipaggiamento. Togli il segnalino.</td></tr>
<tr><td>{I('piedi',BROWN)}<b>Sentiero tranquillo</b></td><td>Non succede niente. Togli il segnalino.</td></tr>
<tr><td>{I('casa',LOC)}<b>Locanda</b></td><td>+1 PE e recuperi 2 PV.</td></tr>
<tr><td>{I('goccia',FON)}<b>Fonte</b></td><td>Riprendi in mano fino a 2 carte dai tuoi scarti.</td></tr>
<tr><td>{I('martello',FAB)}<b>Fabbro</b></td><td>Riprendi in mano 1 equipaggiamento dai tuoi scarti.</td></tr>
<tr><td>{I('cripta')}<b>Cripta con MIMI</b></td><td>Se hai individuato il tesoro: scontro con il Guardiano (pagina 15).</td></tr>
<tr><td>{I('freccia',RED)}<b>Accanto a un altro eroe</b></td><td>Se in questo turno non hai avuto altri scontri: Duello (pagina 12).</td></tr>
</table>
<p class="tip">I segnalini risolti tornano nella scatola. <b>Locanda, Fonte e Fabbro</b> valgono una volta per eroe: segnali con un cubetto Durata sulla scheda. Il Chierico ricarica comunque in Locanda.</p>
<div class="box"><h3>Le caselle senza simbolo</h3><p style="margin:0">Sono sentieri: se ti fermi lì non succede niente, a meno che tu sia accanto a un altro eroe. Servono a muoversi e a scegliere dove fermarsi.</p></div></div>''', 9)

# 10 scontro
page(f'''<h1>Lo scontro</h1>
<p class="lead">Una sola regola per colpire: tira il <b>D20</b>, aggiungi il tuo <b>ATT</b>. Se arrivi alla <b>Difesa</b> del bersaglio, lo colpisci.</p>
<ol>
<li><b>Attacchi tu per primo.</b> D20 + ATT. Se il totale è uguale o maggiore della Difesa stampata sul nemico, tira il danno.</li>
<li><b>Poi attacca il nemico.</b> Per lui tira l’avversario (con più giocatori, chi ti siede a destra): D20 + ATT del nemico contro la tua Difesa, poi il danno stampato sul segnalino.</li>
<li><b>Avanti così</b>, un attacco a testa, finché qualcuno arriva a 0 PV. I PV del nemico si contano con il dado rosso; i tuoi con il cubetto rosso.</li>
</ol>
<table><tr><th>Il tuo danno</th><th></th></tr>
<tr><td>A mani nude</td><td><b>D6 − 1</b> (minimo 1)</td></tr>
<tr><td>Arma a una mano</td><td><b>D6</b></td></tr>
<tr><td>Arma a due mani</td><td><b>D6 + 1</b></td></tr></table>
<div class="cols"><div class="box"><h3>20 sul dado</h3><p style="margin:0">Colpisci sempre e il danno raddoppia.</p></div><div class="box"><h3>1 sul dado</h3><p style="margin:0">Manchi sempre, qualunque sia il totale.</p></div></div>
<h2>Fuggire</h2>
<p>Prima di ogni tuo attacco puoi fuggire: torni sull’esagono da cui sei arrivato, senza ricompense, e il turno finisce. Dal Guardiano di MIMI può fuggire solo il Ladro. Per evitare un Duello leggi pagina 12.</p>
<h2>Chi vince prende</h2>
<table><tr><td>{I('spade')}<b>Creatura</b></td><td>1 Indizio e 1 PE</td></tr>
<tr><td>{I('teschio',RED)}<b>Mini-boss</b></td><td>1 Indizio, sali subito di livello e prendi l’Ispirazione</td></tr>
<tr><td>{I('forziere')}<b>Guardiano di MIMI</b></td><td>La partita!</td></tr></table>''', 10)

# 11 esempio
page(f'''<h1>Un esempio di scontro</h1>
<p><b>Lia</b> gioca il Guerriero: ATT 3, Difesa 11, PV 10, e ha equipaggiato l’Arco da guerra (arma a due mani: danno D6 + 1). Si ferma su una casella «?» e la gira:</p>
<div class="tokens">{token('Lupo grigio',5,'+3',10,'D6−1',110)}</div>
<p>Il Lupo grigio ha 5 PV, ATT +3, Difesa 10, danno D6 − 1. Lia gira il dado rosso sul 5. Per il lupo tira Marco.</p>
<table class="ex"><tr><th>Round</th><th>Chi tira</th><th>Tiro</th><th>Risultato</th></tr>
<tr><td>1</td><td>Lia</td><td>9 + 3 = 12</td><td>12 ≥ 10: colpito! Danno 2 + 1 = 3. Dado rosso: da 5 a 2.</td></tr>
<tr><td>1</td><td>Marco per il lupo</td><td>10 + 3 = 13</td><td>13 ≥ 11: colpita. Danno: esce 4, meno 1 = 3. Lia scende a 7 PV.</td></tr>
<tr><td>2</td><td>Lia</td><td>6 + 3 = 9</td><td>9 &lt; 10: mancato.</td></tr>
<tr><td>2</td><td>Marco per il lupo</td><td>4 + 3 = 7</td><td>7 &lt; 11: mancato.</td></tr>
<tr><td>3</td><td>Lia</td><td>15 + 3 = 18</td><td>Colpito! Danno 5 + 1 = 6. Il lupo è a 0.</td></tr></table>
<div class="box red"><h3>Lia vince</h3><p style="margin:0">Prende 1 Indizio e lo mette sulla scheda, sposta il cubetto PE di una casella e rimette il segnalino del lupo nella scatola. Il suo turno finisce.</p></div>
<p class="tip">Prima del round 2 Lia poteva anche giocare una carta, per esempio una Pozione della forza, oppure fuggire.</p>''', 11)

# 12 sconfitta e duello
page(f'''<h1>Sconfitta e Duello</h1>
<h2>Quando arrivi a 0 PV</h2>
<ol><li><b>Tira il D6</b>: la tua miniatura riparte dal punto di partenza con quel numero (ritira se è occupato o è accanto a un altro eroe).</li>
<li>I tuoi PV tornano al massimo. Gli Indizi restano tuoi.</li>
<li>Tira il D6 della <b>perdita di equipaggiamento</b>.</li></ol>
<p>Il nemico resta sulla mappa, scoperto e con tutti i suoi PV: aspetta il prossimo che si ferma lì.</p>
<table><tr><th>D6</th><th>Perdi</th></tr>
<tr><td><b>1</b></td><td>Tutto l’equipaggiamento</td></tr><tr><td><b>2</b></td><td>L’Elmo</td></tr><tr><td><b>3</b></td><td>L’Arma</td></tr><tr><td><b>4</b></td><td>Il Corpo</td></tr><tr><td><b>5–6</b></td><td>Niente, che fortuna!</td></tr></table>
<p class="tip">Le carte perse vanno nei tuoi scarti (il Fabbro te le può restituire). Ricordati di spostare i cubetti.</p>
<h2>Il Duello tra eroi</h2>
<p>Se finisci il movimento accanto a un altro eroe, e in questo turno non hai avuto altri scontri, lo sfidi.</p>
<ul><li><b>Vuoi evitarlo?</b> Chi viene sfidato può rifiutare: lo sfidante gli pesca <b>1 carta a caso</b> dalla mano e la tiene. Il Duello non si fa.</li>
<li>Attacca per primo chi ha mosso; ognuno tira i propri dadi.</li>
<li>Chi si difende può giocare <b>1 carta</b> durante il Duello, anche se non è il suo turno.</li>
<li>Chi vince prende <b>1 Indizio</b> allo sconfitto (se ne ha), riprende in mano <b>1 carta</b> dagli scarti dello sconfitto, prende <b>1 PE</b> (mezzo livello) e l’<b>Ispirazione</b>.</li>
<li>Chi perde subisce la sconfitta normale.</li></ul>
<p class="tip">Chierico: a 0 PV torna in vita con 3 PV e continua lo scontro. Quando usa questo potere, metti un cubetto Durata sulla Carta Classe. Lo togli, e il potere torna pronto, quando ti fermi in una Locanda.</p>''', 12)

# 13 carte
page(f'''<h1>Le carte</h1>
<p class="lead">Hai 10 carte per tutta la partita: non se ne pescano altre. Alcune carte e la Fonte ti fanno riprendere carte dagli scarti.</p>
<div class="fig">{card_anatomy()}</div>
<h2>Equipaggiare</h2>
<p>Infila la carta sotto il bordo alto della scheda, nello slot della sua icona (<b>Elmo</b>, <b>Arma</b> o <b>Corpo</b>): resta fuori solo la fascia con nome e bonus. Sposta subito i cubetti. Se lo slot era già occupato, il vecchio oggetto va negli scarti. Massimo 1 equipaggiamento per turno. Gli scudi si impugnano: vanno nello slot <b>Arma</b>.</p>
<h2>Le carte di classe</h2>
<p>Le può giocare solo l’eroe di quella classe; si riconoscono dal dorso colorato. Le carte comuni le può giocare chiunque. Se una carta ha un requisito («solo se la tua pedina è un Nano»), senza requisito non si gioca.</p>''', 13)

# 14 durate etc
page(f'''<h1>Effetti, Clessidre e livelli</h1>
<h2>{I('spade')} {I('clessidra')} Effetti che durano</h2>
<p>Se una carta ha l’icona di durata, mettila in <b>Effetti in corso</b> accanto alla scheda, con sopra tanti cubetti Durata quanti dice il numero.</p>
<table><tr><td>{I('clessidra')} <b>Clessidra</b></td><td>Togli un cubetto alla fine di ogni tuo turno.</td></tr>
<tr><td>{I('spade')} <b>Spade</b></td><td>Togli un cubetto alla fine di ogni tuo scontro.</td></tr></table>
<p>Quando non ci sono più cubetti, la carta va negli scarti. «Fino alla fine del turno» non usa cubetti.</p>
<h2>{I('clessidra')} Turni persi</h2>
<p>«Perdi 2 turni» vuol dire: metti 2 Clessidre sulla tua scheda. Per colpa degli avversari non ne puoi avere più di 3: quelle in più non si mettono. Se invece perdi turni per una tua scelta (una tua carta), li perdi tutti: le Clessidre in più vanno accanto alla scheda.</p>
<h2>{I('stella',GOLD)} Ispirazione</h2>
<p>Ne puoi avere una sola. Scartala per ritirare un dado che hai appena tirato.</p>
<h2>Vantaggio e svantaggio</h2>
<p>Con il <b>vantaggio</b> tiri due D20 e tieni il migliore; con lo <b>svantaggio</b> il peggiore. Se hai entrambi, si annullano.</p>
<h2>{I('stella',GOLD)} Salire di livello</h2>
<p>Ogni PE sposta il cubetto di una casella. Quando arriva su una casella dorata (2, 4, 6, 8) sali di livello: <b>+1 ai PV massimi</b> (sposti rosso e nero) e <b>+1 a ATT, MOV o AR</b>, a scelta. Un mini-boss sconfitto porta il cubetto direttamente alla prossima casella dorata; un Duello vinto vale 1 PE. Il livello massimo è 5.</p>''', 14)

# 15 tesoro
page(f'''<h1>Il tesoro e la vittoria</h1>
<div class="cols"><div>
<h2>{I('pergamena')} Individuare il tesoro</h2>
<p>Appena metti il <b>terzo Indizio</b> sulla scheda hai individuato il tesoro. <b>La voce si sparge</b>: ogni altro eroe prende subito 1 Indizio.</p>
<p>Se MIMI non è ancora sulla mappa, <b>tira il D6</b> (con 5 o 6 ritira): metti MIMI e il Guardiano sulla Cripta con quel numero. Se l’ha già individuato qualcun altro, MIMI è già lì e lo sai anche tu.</p>
</div><div>
<h2>{I('forziere')} Sconfiggere il Guardiano</h2>
<p>Raggiungi la Cripta e fermati lì: inizia lo scontro. Il Guardiano ha <b>14 PV, ATT +4, Difesa 13</b>, danno <b>D6 + 1</b>.</p>
<p>Solo chi ha 3 Indizi può sfidarlo. Se perdi, <b>le sue ferite restano</b>: segna i suoi PV con il cubetto giallo nella Sala del Tesoro. Il prossimo lo trova già ferito.</p>
</div></div>
<div class="box red"><h3>Vittoria!</h3><p style="margin:0;font-size:10.5pt">Chi sconfigge il Guardiano di MIMI riporta il forziere a Geronimo e vince la partita.</p></div>
<h2>Da sapere</h2>
<ul>
<li>Se in un Duello perdi un Indizio e ne restano 2, non puoi sfidare il Guardiano finché non ne trovi un altro.</li>
<li>Nessuna carta fa individuare il tesoro di colpo: le carte danno Indizi.</li>
<li>Se una carta fa «cambiare posizione» al tesoro, ritira il D6 finché esce un’altra Cripta (5 e 6 si ritirano) e spostaci MIMI e il Guardiano. Succede al massimo 2 volte per partita; solo il Mimik lo sposta sempre.</li>
</ul>
<div class="box"><h3>Il Presagio del Goblin</h3><p style="margin:0">Chi ha Geronimo sposta il cubetto Giro all’inizio di ogni suo turno. <b>Dal giro 8</b>, all’inizio del tuo turno, se non hai ancora 3 Indizi tira il D6: se fai il numero stampato sul tracciato prendi 1 Indizio. Giri 8–10: 6 · 11–13: 5+ · 14–16: 4+ · 17–19: 3+ · dal 20: 2+.</p></div>
<p style="margin-top:2mm"><b>Varianti.</b> <i>Partita lampo</i>: ogni eroe parte con 1 Indizio. <i>In famiglia</i>: niente Duelli.</p>''', 15)

# 16 back: riepilogo
page(f'''<h1 style="text-align:center">Riepilogo</h1>
{turn_strip()}
<div class="cols"><div>
<h2>Scontro</h2>
<p class="sans" style="font-size:9.8pt">Colpisci se <b>D20 + ATT ≥ Difesa</b>.<br>Danno: D6 − 1 mani nude · D6 una mano · D6+1 due mani.<br>20 = colpo doppio · 1 = mancato.<br>Per il mostro tira l’avversario.<br>Prima di attaccare puoi fuggire.</p>
<h2>Ricompense</h2>
<p class="sans" style="font-size:9.8pt">Creatura: 1 Indizio + 1 PE<br>Mini-boss: 1 Indizio + livello + Ispirazione<br>Duello: Indizio + carta + 1 PE + Ispirazione<br>Rifiuti il Duello: dai 1 carta a caso</p>
</div><div>
<h2>Edifici</h2>
<p class="sans" style="font-size:9.8pt">{I('casa',LOC)}Locanda: +1 PE, +2 PV<br>{I('goccia',FON)}Fonte: 2 carte dagli scarti<br>{I('martello',FAB)}Fabbro: 1 equipaggiamento dagli scarti<br>Edifici: 1 volta ciascuno</p>
<h2>Sconfitta</h2>
<p class="sans" style="font-size:9.8pt">Tira il D6 per ripartire, PV al massimo.<br>D6: 1 tutto · 2 elmo · 3 arma · 4 corpo · 5–6 niente</p>
<h2>Vittoria</h2>
<p class="sans" style="font-size:9.8pt">3 Indizi → gli altri prendono 1 Indizio → D6 per la Cripta → batti il Guardiano (14 PV). Le sue ferite restano.<br>Dal giro 8: Presagio, D6 per 1 Indizio.</p>
</div></div>
<p class="tip" style="text-align:center;margin-top:3mm">Il Tesoro del Goblin · Scatola base · Regolamento v4.1 da tavolo</p>''', None)

html = f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Il Tesoro del Goblin – Regolamento</title><style>{STYLE}</style></head><body>{"".join(pages)}</body></html>'
out=__import__('os').path.join(__import__('os').path.dirname(__file__),'regolamento.html')
open(out,'w').write(html)
print('pages',len(pages))
