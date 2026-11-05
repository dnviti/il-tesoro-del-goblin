# Libretto dell'espansione «Il Caos del Goblin» (A5, 8 pagine con 3 mm di abbondanza, come il regolamento base)
# Uso: python3 caos.py && ./mkpdf.sh caos.html $PWD/Espansione_Caos_stampa.pdf 154mm 216mm
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build
from svg import *
from parts import *
I=build.I
# numeri misurati col simulatore fisico (sorgenti/framework/caos_add.js), aggiornati da caos_misure.json
M=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caos_misure.json')))
VER=M.get('ver','2.0')
S=build.STYLE+f"""
.cover.caos{{background:#24142b}}
.cover.caos::before{{background:radial-gradient(ellipse at 50% 48%,rgba(186,120,220,.35),rgba(0,0,0,0) 62%)}}
.cover.caos .t2{{color:#e9c8f5}}
.box.viola{{border-color:{CAOS};background:#f6eef8}}
.box.viola h3{{color:{CAOS}}}
h1.v{{color:{CAOS}}}
.d6 td:first-child{{width:9mm;text-align:center;font-family:'Cinzel';font-weight:800;font-size:12pt;color:{CAOS}}}
.d6 td{{font-size:9.4pt;padding:1.2mm 1.2mm}}
.lore p{{font-size:10.4pt}}
.lore p:first-child::first-letter{{font-family:'Cinzel';font-weight:800;font-size:22pt;float:left;line-height:.9;margin:1mm 1.5mm 0 0;color:{CAOS}}}
.two{{display:flex;gap:3mm;margin:2mm 0}} .two>div{{flex:1}}
.cards{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.4mm 2.4mm;justify-items:center}}
.cards .cap{{margin-top:.4mm}}
.cob{{display:flex;gap:3mm;align-items:flex-start;margin:1.6mm 0}} .cob .tx{{flex:1;font-size:9.6pt}}
.cob .tx b.n{{font-family:'Cinzel';color:{CAOS};font-size:10pt}}
"""
pages=[]
def page(body,n=None,cls=''):
    folio=f'<div class="folio">{n}</div>' if n else ''
    pages.append(f'<section class="page {cls}"><div class="frame"></div><div class="in">{body}</div>{folio}</section>')

def cover_art_caos():
    # MIMI che fluttua sopra la Crepa da cui esce il Caos, con un Coboldo che sbircia
    return f'''<svg viewBox="0 0 300 230" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="gv" cx="50%" cy="72%" r="55%"><stop offset="0" stop-color="#d9a8f0" stop-opacity="0.95"/><stop offset="1" stop-color="#7a3e8e" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="150" cy="175" rx="140" ry="70" fill="url(#gv)"/>
<path d="M60 190 L110 178 L128 186 L150 168 L170 184 L196 176 L240 190 L196 198 L170 192 L150 206 L128 194 L110 200 Z" fill="#1a0d20" stroke="#f6d68b" stroke-width="2.5"/>
<path d="M118 188 L150 178 L182 188 L150 198 Z" fill="#f6d68b" opacity=".85"/>
<g fill="#f6d68b"><circle cx="96" cy="150" r="3"/><circle cx="210" cy="140" r="2.5"/><circle cx="132" cy="128" r="2"/><circle cx="178" cy="120" r="2.2"/><circle cx="70" cy="120" r="1.8"/><circle cx="236" cy="112" r="1.6"/></g>
<g transform="translate(150 78) rotate(-8) scale(.62)">
<path d="M-80 -10 a80 50 0 0 1 160 0 z" fill="#7a4a24" stroke="#3b2414" stroke-width="3"/>
<rect x="-80" y="-10" width="160" height="78" rx="6" fill="#8a5428" stroke="#3b2414" stroke-width="3"/>
<rect x="-80" y="-4" width="160" height="14" fill="{GOLD}" stroke="#3b2414" stroke-width="2"/>
<rect x="-80" y="44" width="160" height="10" fill="{GOLD}" stroke="#3b2414" stroke-width="2"/>
<rect x="-14" y="-12" width="28" height="36" rx="4" fill="{GOLD}" stroke="#3b2414" stroke-width="2.5"/>
<circle cx="-30" cy="-30" r="7" fill="#fff" stroke="#3b2414" stroke-width="2"/><circle cx="30" cy="-30" r="7" fill="#fff" stroke="#3b2414" stroke-width="2"/>
<circle cx="-27" cy="-28" r="3" fill="#3b2414"/><circle cx="33" cy="-28" r="3" fill="#3b2414"/>
</g>
<path d="M150 118 q-10 25 0 50" stroke="#d9a8f0" stroke-width="3" fill="none" stroke-dasharray="4 5"/>
<g transform="translate(206 176)">
<path d="M-14 4 q0 -18 14 -18 q14 0 14 18 z" fill="#6f7d3c" stroke="#2c3315" stroke-width="2"/>
<path d="M-12 -6 l-10 -8 l6 12 z M12 -6 l10 -8 l-6 12 z" fill="#6f7d3c" stroke="#2c3315" stroke-width="2"/>
<circle cx="-5" cy="-4" r="2.6" fill="#f6d68b"/><circle cx="5" cy="-4" r="2.6" fill="#f6d68b"/>
</g>
</svg>'''

def cob_token(nome,pv,att,dif,tratto,size=74):
    # segnalino Coboldo: tondo viola con i valori come le creature della base
    s=size; c=s/2
    return f'''<svg viewBox="0 0 {s} {s}" width="{s*0.29:.0f}mm" xmlns="http://www.w3.org/2000/svg">
<circle cx="{c}" cy="{c}" r="{c-1.5}" fill="#f1e4f5" stroke="{CAOS}" stroke-width="2.2"/>
<circle cx="{c}" cy="{c}" r="{c-6}" fill="none" stroke="{GOLD}" stroke-width="0.8"/>
<text x="{c}" y="{s*0.27}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{s*(0.1 if len(nome)<9 else 0.075)}" fill="{INK}">{nome}</text>
{icon('cuore',s*0.3,s*0.46,0.4,RED)}<text x="{s*0.3}" y="{s*0.67}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{pv}</text>
{icon('spade',s*0.5,s*0.46,0.4,INK)}<text x="{s*0.5}" y="{s*0.67}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{att}</text>
{icon('scudo',s*0.7,s*0.46,0.4,BLUE)}<text x="{s*0.7}" y="{s*0.67}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{dif}</text>
<text x="{c}" y="{s*0.82}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.095}" fill="{CAOS}">{tratto}</text>
</svg>'''

def caos_card(nome,tipo,righe,w=126):
    # carta Caos (63 x 88 mm): fascia viola, tipo, testo
    h=w*88/63
    o=[f'<svg viewBox="0 0 {w} {h:.1f}" width="{w*0.27:.1f}mm" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">',
       f'<rect x="1" y="1" width="{w-2}" height="{h-2:.1f}" rx="7" fill="#fffaf0" stroke="{CAOS}" stroke-width="2"/>',
       f'<rect x="5" y="5" width="{w-10}" height="26" rx="5" fill="{CAOS}"/>',
       f'<text x="{w/2}" y="22.5" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{11 if len(nome)<18 else 9.6}" fill="#f6d68b">{nome}</text>',
       f'<rect x="10" y="36" width="{w-20}" height="44" rx="4" fill="#efe2f3"/>',crepa_tile(w/2,58,15),
       f'<text x="{w/2}" y="93" text-anchor="middle" font-size="8.6" font-weight="800" fill="{CAOS}">{tipo}</text>']
    for i,r in enumerate(righe): o.append(f'<text x="{w/2}" y="{107+i*11.2:.1f}" text-anchor="middle" font-size="9.4" fill="{INK}">{r}</text>')
    o.append(f'<text x="{w-10}" y="{h-8:.1f}" text-anchor="end" font-size="7" fill="{BROWN}">✷ Caos</text></svg>')
    return ''.join(o)

def aid_card(w=150):
    # Carta Aiuto del Caos, 63 x 88 mm
    h=w*88/63; L=[(n,t,d) for n,t,d in M['aiuto']]
    o=[f'<svg viewBox="0 0 {w} {h:.1f}" width="{w*0.22:.0f}mm" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">',
       f'<rect x="1" y="1" width="{w-2}" height="{h-2:.1f}" rx="8" fill="#f6eef8" stroke="{CAOS}" stroke-width="2"/>',
       f'<rect x="1" y="1" width="{w-2}" height="34" rx="8" fill="{CAOS}"/>',
       f'<text x="{w/2}" y="23" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="13" fill="#f6d68b">Su una Crepa</text>',
       f'<text x="{w/2}" y="50" text-anchor="middle" font-size="9" font-weight="800" fill="{INK}">Fruga (D6) oppure</text>',
       f'<text x="{w/2}" y="61" text-anchor="middle" font-size="9" font-weight="800" fill="{INK}">attraversa: vai sulla gemella</text>']
    for i,(n,t,d) in enumerate(L):
        y=82+i*18
        o.append(f'<text x="12" y="{y}" font-family="Cinzel" font-weight="800" font-size="13" fill="{CAOS}">{n}</text><text x="28" y="{y}" font-size="9.5" font-weight="700" fill="{INK}">{t}</text><text x="28" y="{y+9}" font-size="8" fill="{BROWN}">{d}</text>')
    o.append(f'<text x="{w/2}" y="{h-8:.1f}" text-anchor="middle" font-size="7.5" fill="{BROWN}">La Crepa resta: vale ogni volta, per tutti</text></svg>')
    return ''.join(o)

# 1 copertina
pages.append(f'''<section class="page cover caos"><div class="frame"></div>
<div class="t1">ESPANSIONE</div><div class="t2">Il Caos<br>del Goblin</div>
<div class="art" style="top:76mm">{cover_art_caos()}</div>
<div class="t3">«Le Crepe di MIMI»</div>
<div style="position:absolute;bottom:31mm;left:0;right:0;text-align:center;font-family:'Alegreya Sans';font-size:10pt;color:#efe2c2;letter-spacing:.5px">un gioco di <b>Alessandro De Simone</b></div><div class="t4">SERVE LA SCATOLA BASE</div><div class="t5">2–4 giocatori · 10 Crepe · 6 Coboldi di MIMI · 6 carte Caos</div></section>''')

# 2 storia e contenuto
page(f'''<h1 class="v">Le Crepe di MIMI</h1>
<div class="lore">
<p>Quando l’incantesimo di Geronimo fece sparire MIMI, il forziere non se ne andò tutto intero. Una cassa senza fondo non si chiude come un cassetto: il suo <b>fondo</b> rimase aperto, strappato in dieci punti delle Terre di Hande. La gente le chiama <b>Crepe</b>.</p>
<p>Dalle Crepe esce di tutto: le cianfrusaglie che Geronimo ci ha infilato in cent’anni di avventure, le pagine strappate della sua mappa, folate del vento del nulla. E i <b>Coboldi di MIMI</b>, che vivevano là dentro per tenere in ordine il tesoro (senza riuscirci mai) e ora difendono la loro casa a morsi, a sassate o rubando dalle tasche.</p>
<p>Le Crepe sono nate a coppie: ognuna ha una <b>gemella</b> dall’altra parte delle Terre di Hande, perché il fondo di MIMI è uno solo. Chi ha fegato ci si tuffa e riemerge lontano. Geronimo lo chiama <b>il Caos</b>; i Coboldi lo chiamano casa. Le Crepe si richiuderanno solo quando MIMI tornerà dal suo padrone.</p>
</div>
<div class="box viola"><h3>Il Caos in una frase</h3><p style="margin:0">Dieci <b>Crepe</b> si posano sulla plancia: chi si ferma su una Crepa <b>fruga</b> (tira il D6 e succede qualcosa di inatteso) oppure la <b>attraversa</b> e salta sulla sua gemella.</p></div>
<h2>Cosa c’è nell’espansione</h2>
<div class="comp">
<div><b>10</b> Tessere Crepa (5 coppie)</div><div><b>6</b> Segnalini Coboldo di MIMI</div>
<div><b>6</b> Carte Caos</div><div><b>4</b> Carte Aiuto del Caos</div>
<div><b>1</b> Questo libretto</div><div></div>
</div>
<p class="tip" style="margin-top:2mm">Il Caos si aggiunge alla scatola base e a ogni espansione. Non serve nessun dado nuovo: si usa il D6.</p>''',2)

# 3 preparazione
page(f'''<h1 class="v">Preparazione</h1>
<p>Prepara la scatola base come al solito, poi:</p>
<ol>
<li><b>Posa le 10 Crepe</b> sui loro esagoni, che sulla plancia sono sentieri vuoti. Ogni Crepa porta la lettera della sua coppia (A–E): la gemella è sempre quella opposta, girando la plancia di 180°.</li>
<li><b>Mescola le 6 carte Caos</b> nel mazzo comune prima di distribuire le carte.</li>
<li>Metti i <b>6 Coboldi</b> coperti in una pila accanto alla plancia e dai a ognuno una Carta Aiuto del Caos.</li>
</ol>
<div class="fig" style="width:66%;margin-left:auto;margin-right:auto">{board(W=20,show_bands=False,caos_tiles='coppie')}</div>
<table><tr><th>Coppia</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr>
<tr><td><b>Crepe</b></td><td>E1 · F10</td><td>J3 · A8</td><td>D3 · G8</td><td>H5 · C6</td><td>E5 · F6</td></tr></table>
<div class="box viola"><h3>Con una plancia Terreno</h3><p style="margin:0">Il Terreno copre il Cuore: le Crepe del Cuore (coppie C, D ed E) restano nella scatola. Le caselle evento del Terreno usano la tabella del Terreno. Restano le coppie A e B, le 4 Crepe esterne.</p></div>''',3)

# 4 fermarsi su una Crepa
rows=M['tabella']
page(f'''<h1 class="v">Fermarsi su una Crepa</h1>
<p class="lead">Quando finisci il movimento su una Crepa scegli una delle due cose.</p>
<div class="two">
<div class="box viola" style="margin:0"><h3>Frugare</h3><p style="margin:0">Tira il D6 e guarda la tabella qui sotto (è anche sulla Carta Aiuto).</p></div>
<div class="box viola" style="margin:0"><h3>Attraversare il fondo</h3><p style="margin:0">Metti subito il tuo eroe sulla <b>Crepa gemella</b>, se non c’è un eroe sopra o accanto. Il turno finisce lì: non si fruga.</p></div>
</div>
<table class="d6">{''.join(f'<tr><td>{n}</td><td><b>{t}</b>: {d}</td></tr>' for n,t,d in rows)}</table>
<ul>
<li><b>La Crepa resta</b>: è stampata sulla tessera, non è un segnalino del sacchetto. Vale ogni volta, per tutti.</li>
<li>Se ti fermi su una Crepa accanto a un altro eroe, prima fai il Duello, poi scegli se frugare o attraversare.</li>
</ul>''',4)

# 5 i Coboldi
cobs=M['coboldi']
page(f'''<h1 class="v">I Coboldi di MIMI</h1>
<p class="lead">Quando frugando esce l’<b>Imboscata</b>, gira il primo Coboldo della pila e combatti come con una creatura. Se vinci prendi 1 PE e <b>peschi 1 carta</b> dal mazzo comune: i Coboldi non hanno pagine della mappa, quindi niente Indizio. Il Coboldo, vinto o no, torna sotto la pila.</p>
{''.join(f'<div class="cob"><div style="flex:none">{cob_token(c["nome_corto"],c["pv"],c["att"],c["dif"],c["tratto"])}</div><div class="tx"><b class="n">{c["nome"]}</b> ×2<br>{c["testo"]}</div></div>' for c in cobs)}
<p class="tip">Tutti i Coboldi fanno D6 − 1 danni (minimo 1), come le creature deboli della base. Se in questo turno hai già combattuto, il Coboldo scappa e non succede niente.</p>
<p class="tip">Minaccia (vedi il framework di design): {M["minaccia"]}, tutti nella fascia Debole.</p>''',5)

# 6 le carte Caos
cards=M['carte']
page(f'''<h1 class="v">Le carte Caos</h1>
<p>Sei carte nuove entrano nel mazzo comune. Si giocano come tutte le altre: fino a 2 carte per turno, al massimo 1 equipaggiamento.</p>
<div class="cards">{''.join(f'<div>{caos_card(c["nome"],c["tipo"],c["righe"])}</div>' for c in cards)}</div>
<p class="tip" style="margin-top:2mm">Le carte che parlano di Crepe non fanno niente se le Crepe non sono sulla plancia: con una plancia Terreno usate le 4 Crepe esterne.</p>''',6)

# 7 domande frequenti + Carta Aiuto
page(f'''<h1 class="v">Domande frequenti</h1>
<div class="qa">
{''.join(f'<p><b>{q}</b>{a}</p>' for q,a in M['faq'])}
</div>
<div class="cols" style="align-items:center;margin-top:1mm"><div style="flex:none">{aid_card()}</div><div><p class="cap" style="text-align:left">La Carta Aiuto del Caos (63 × 88 mm), una per giocatore.</p></div></div>''',7)

# 8 retro: il Caos in numeri
page(f'''<h1 class="v">Il Caos in numeri</h1>
<p>Ogni pezzo di questa espansione è stato provato con il simulatore della scatola fisica, {M["partite"]} partite per numero di giocatori, con i tempi di un tavolo vero.</p>
<table><tr><th></th><th>2 giocatori</th><th>3 giocatori</th><th>4 giocatori</th></tr>
<tr><td><b>Scatola base</b></td>{''.join(f'<td>{x} min</td>' for x in M['base_min'])}</tr>
<tr><td><b>Con il Caos</b></td>{''.join(f'<td>{x} min</td>' for x in M['caos_min'])}</tr></table>
<p>{M["equilibrio"]}</p>
<div class="box viola"><h3>Perché le Crepe gemelle</h3><p style="margin:0">{M["perche_gemelle"]}</p></div>
<p class="tip" style="text-align:center;margin-top:5mm">Il Tesoro del Goblin · Espansione «Il Caos del Goblin · Le Crepe di MIMI» · v{VER}<br>Esce dopo La Cittadella Bianca e funziona con ogni scatola.</p>''',8)

html=f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Il Caos del Goblin – Espansione</title><style>{S}</style></head><body>{"".join(pages)}</body></html>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'caos.html'),'w').write(html)
print('pagine',len(pages))
