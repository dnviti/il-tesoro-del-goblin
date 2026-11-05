from svg import *

def token(name,pv,att,dif,dmg,size=70):
    s=size; c=s/2
    return f'''<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" xmlns="http://www.w3.org/2000/svg">
<circle cx="{c}" cy="{c}" r="{c-1.5}" fill="#efe1c3" stroke="{BROWN}" stroke-width="2"/>
<circle cx="{c}" cy="{c}" r="{c-6}" fill="none" stroke="{GOLD}" stroke-width="0.8"/>
<text x="{c}" y="{s*0.33}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{s*0.105}" fill="{INK}">{name}</text>
{icon('cuore',s*0.3,s*0.52,0.42,RED)}<text x="{s*0.3}" y="{s*0.74}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{pv}</text>
{icon('spade',s*0.5,s*0.52,0.42,INK)}<text x="{s*0.5}" y="{s*0.74}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{att}</text>
{icon('scudo',s*0.7,s*0.52,0.42,BLUE)}<text x="{s*0.7}" y="{s*0.74}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.14}" fill="{INK}">{dif}</text>
<text x="{c}" y="{s*0.88}" text-anchor="middle" font-family="Alegreya Sans" font-weight="700" font-size="{s*0.1}" fill="{RED}">danno {dmg}</text>
</svg>'''

def back_token(size=46):
    s=size;c=s/2
    return f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}"><circle cx="{c}" cy="{c}" r="{c-1.5}" fill="#3b2a1c" stroke="{GOLD}" stroke-width="2"/><text x="{c}" y="{c+s*0.17}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{s*0.5}" fill="{GOLD}">?</text></svg>'

def simple_token(ic,label,col,size=46):
    s=size;c=s/2
    return f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}"><circle cx="{c}" cy="{c}" r="{c-1.5}" fill="#efe1c3" stroke="{BROWN}" stroke-width="2"/>{icon(ic,c,c*0.85,s/46*0.9,col)}<text x="{c}" y="{s*0.86}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.15}" fill="{INK}">{label}</text></svg>'

def scheda(w=460):
    # 260x180 mm scheda drawn in 520x420 units
    o=['<svg viewBox="0 0 540 430" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">']
    slots=[('Carta Classe',20),('Elmo',150),('Arma',280),('Corpo',410)]
    for nm,x in slots:
        o.append(f'<rect x="{x}" y="6" width="105" height="40" rx="5" fill="#fffaf0" stroke="{BROWN}" stroke-width="1.5"/>')
        o.append(f'<text x="{x+52.5}" y="31" text-anchor="middle" font-weight="800" font-size="14" fill="{INK}">{nm}</text>')
        o.append(f'<rect x="{x}" y="46" width="105" height="26" fill="none" stroke="{BROWN}" stroke-dasharray="3 3"/>')
    o.append(f'<rect x="6" y="46" width="528" height="340" rx="10" fill="#e9d8b4" stroke="{BROWN}" stroke-width="2.5"/>')
    for nm,x in slots: o.append(f'<rect x="{x}" y="47" width="105" height="25" fill="#e2cfa6" stroke="{BROWN}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    # razza
    o.append(f'<rect x="20" y="90" width="110" height="56" rx="6" fill="#fffaf0" stroke="{BROWN}" stroke-dasharray="5 3"/><text x="75" y="115" text-anchor="middle" font-weight="800" font-size="13" fill="{INK}">Tessera Razza</text><text x="75" y="133" text-anchor="middle" font-size="11" fill="{BROWN}">si incastra qui</text>')
    o.append(f'<text x="20" y="176" font-weight="800" font-size="12" fill="{INK}">Si parte da:</text><text x="20" y="193" font-size="12" fill="{INK}">PV 10 · ATT 1</text><text x="20" y="209" font-size="12" fill="{INK}">MOV 1 · AR 1</text>')
    o.append(f'<text x="20" y="240" font-weight="800" font-size="12" fill="{INK}">Livello su:</text><text x="20" y="257" font-size="12" fill="{INK}">+1 PV massimi</text><text x="20" y="273" font-size="12" fill="{INK}">+1 ATT, MOV o AR</text>')
    # tracks
    def trk(y,label,n,ic,col,cubes,hi=()):
        s=[icon(ic,160,y,0.75,col),f'<text x="176" y="{y+5}" font-weight="800" font-size="13" fill="{INK}">{label}</text>']
        bw=10.5 if n>12 else 22; gap=1 if n>12 else 3
        x0=214
        for i in range(n):
            x=x0+i*(bw+gap)
            s.append(f'<rect x="{x}" y="{y-11}" width="{bw}" height="22" rx="2.5" fill="#fffaf0" stroke="{GOLD if i in hi else BROWN}" stroke-width="{2 if i in hi else 0.8}"/>')
            if n<=12: s.append(f'<text x="{x+bw/2}" y="{y+4}" text-anchor="middle" font-size="9.5" fill="{BROWN}">{i}</text>')
        for i,cc in cubes:
            x=x0+i*(bw+gap)+bw/2
            s.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" rx="1.5" fill="{cc}" stroke="#00000055"/>')
        return ''.join(s)
    o.append(trk(100,'PV',20,'cuore',RED,[(6,RED),(9,'#222')]))
    o.append(f'<text x="214" y="126" font-size="10.5" fill="{BROWN}">caselle 1–20 · rosso = PV attuali · nero = PV massimi</text>')
    o.append(trk(152,'ATT',9,'spade',INK,[(1,'#c9a875')]))
    o.append(trk(194,'MOV',7,'stivale',BROWN,[(1,'#c9a875')]))
    o.append(trk(236,'AR',9,'scudo',BLUE,[(1,'#c9a875')]))
    for i in range(9):
        o.append(f'<text x="{214+i*25+11}" y="{262}" text-anchor="middle" font-size="9.5" font-weight="700" fill="{BLUE}">{10+i}</text>')
    o.append(f'<text x="214" y="276" font-size="10.5" fill="{BLUE}">Difesa (10 + AR): già stampata sotto ogni casella</text>')
    o.append(trk(310,'PE',9,'stella',GOLD,[(0,'#c9a875')],hi=(2,4,6,8)))
    o.append(f'<text x="214" y="336" font-size="10.5" fill="{BROWN}">caselle dorate = Livello 2, 3, 4, 5</text>')
    # right column
    def boxes(y,label,n,ic,col,note):
        s=[f'<text x="{456}" y="{y-8}" font-weight="800" font-size="12" fill="{INK}">{label}</text>']
        for i in range(n): s.append(f'<rect x="{456+i*24}" y="{y}" width="20" height="20" rx="3" fill="#fffaf0" stroke="{BROWN}"/>'+icon(ic,456+i*24+10,y+10,0.6,col+'66'))
        s.append(f'<text x="456" y="{y+35}" font-size="10" fill="{BROWN}">{note}</text>')
        return ''.join(s)
    o.append(boxes(100,'Indizi',3,'pergamena',INK,'al 3°: tesoro!'))
    o.append(boxes(175,'Clessidre',3,'clessidra',INK,'mai più di 3'))
    o.append(boxes(250,'Ispirazione',1,'stella',GOLD,'una sola'))
    o.append(f'<text x="456" y="317" font-weight="800" font-size="12" fill="{INK}">Edifici usati</text>')
    for i,(ic,col) in enumerate([('casa',LOC),('goccia',FON),('martello',FAB)]): o.append(f'<rect x="{456+i*24}" y="325" width="20" height="20" rx="3" fill="#fffaf0" stroke="{BROWN}"/>'+icon(ic,456+i*24+10,335,0.6,col+'66'))
    o.append(f'<text x="456" y="360" font-size="10" fill="{BROWN}">1 volta ciascuno</text>')
    o.append(f'<text x="270" y="372" text-anchor="middle" font-size="11.5" font-style="italic" fill="{INK}">I cubetti mostrano sempre il valore finale, equipaggiamento compreso.</text>')
    o.append(f'<rect x="6" y="396" width="340" height="30" rx="6" fill="none" stroke="{BROWN}" stroke-dasharray="5 3"/><text x="18" y="416" font-weight="800" font-size="12" fill="{INK}">Effetti in corso</text><text x="122" y="416" font-size="10.5" fill="{BROWN}">carte con i cubetti Durata</text>')
    o.append(f'<rect x="356" y="396" width="178" height="30" rx="6" fill="none" stroke="{BROWN}" stroke-dasharray="5 3"/><text x="368" y="416" font-weight="800" font-size="12" fill="{INK}">Scarti</text><text x="412" y="416" font-size="10.5" fill="{BROWN}">a faccia in su</text>')
    o.append('</svg>')
    return '\n'.join(o)

def move_example():
    W=40; R=W/math.sqrt(3)
    o=['<svg viewBox="0 0 520 120" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">']
    xs=[30+i*W for i in range(12)]; y=62
    for i,x in enumerate(xs):
        o.append(f'<polygon points="{hexpts(x,y,R*0.97)}" fill="{"#efe1c3" if i>4 else "#f7efdc"}" stroke="{LINE}"/>')
    # path
    o.append(f'<path d="M{xs[0]} {y} L{xs[4]} {y}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4" fill="none"/>')
    o.append(f'<circle cx="{xs[0]}" cy="{y}" r="11" fill="{BLUE}" stroke="{PAPER}" stroke-width="2"/>')
    o.append(q_mark(xs[2],y,9)); o.append(q_mark(xs[4],y,9))
    o.append(f'<circle cx="{xs[4]}" cy="{y}" r="15" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    for i in (1,2,3,4): o.append(f'<text x="{xs[i]}" y="{y-26}" text-anchor="middle" font-weight="800" font-size="13" fill="{RED}">{i}</text>')
    o.append(f'<text x="{xs[2]}" y="{y+36}" text-anchor="middle" font-size="11.5" fill="{BROWN}">ci passi sopra:</text><text x="{xs[2]}" y="{y+50}" text-anchor="middle" font-size="11.5" fill="{BROWN}">non succede niente</text>')
    o.append(f'<text x="{xs[4]}" y="{y+36}" text-anchor="middle" font-size="11.5" font-weight="700" fill="{RED}">ti fermi qui:</text><text x="{xs[4]}" y="{y+50}" text-anchor="middle" font-size="11.5" font-weight="700" fill="{RED}">giri il segnalino</text>')
    o.append(f'<g transform="translate(330,24)"><rect width="180" height="76" rx="8" fill="#fffaf0" stroke="{BROWN}"/><text x="90" y="24" text-anchor="middle" font-weight="800" font-size="13" fill="{INK}">D6 = 3, MOV = 1</text><text x="90" y="46" text-anchor="middle" font-size="12.5" fill="{INK}">ti muovi fino a 4 esagoni</text><text x="90" y="65" text-anchor="middle" font-size="11.5" fill="{BROWN}">(anche meno, ma almeno 1)</text></g>')
    o.append('</svg>')
    return '\n'.join(o)

def card_anatomy():
    o=['<svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">']
    cx,cy,cw,ch=150,10,180,252
    o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="#fffaf0" stroke="{BROWN}" stroke-width="2"/>')
    o.append(f'<rect x="{cx+6}" y="{cy+6}" width="{cw-12}" height="40" rx="6" fill="#ead7ae"/>')
    o.append(icon('elmo',cx+22,cy+26,0.8,BROWN))
    o.append(f'<text x="{cx+40}" y="{cy+24}" font-family="Cinzel" font-weight="800" font-size="13" fill="{INK}">Elmo araldico</text><text x="{cx+40}" y="{cy+40}" font-weight="800" font-size="12" fill="{RED}">AR +2 · ATT +1</text>')
    o.append(f'<rect x="{cx+12}" y="{cy+56}" width="{cw-24}" height="90" rx="4" fill="#e9dcc0"/><text x="{cx+cw/2}" y="{cy+106}" text-anchor="middle" font-size="11" fill="{BROWN}">illustrazione</text>')
    o.append(f'<text x="{cx+14}" y="{cy+170}" font-size="11.5" fill="{INK}">Nano: vantaggio nel</text><text x="{cx+14}" y="{cy+185}" font-size="11.5" fill="{INK}">prossimo scontro.</text>')
    o.append(f'<circle cx="{cx+cw-30}" cy="{cy+178}" r="15" fill="none" stroke="{INK}" stroke-width="1.5"/>'+icon('spade',cx+cw-30,cy+178,0.6,INK)+f'<text x="{cx+cw-12}" y="{cy+170}" font-weight="800" font-size="12" fill="{INK}">1</text>')
    o.append(f'<text x="{cx+14}" y="{cy+ch-12}" font-size="10" fill="{BROWN}">Guerriero</text><text x="{cx+cw-14}" y="{cy+ch-12}" text-anchor="end" font-size="10" fill="{BROWN}">● Base 08/48</text>')
    # tuck line
    o.append(f'<line x1="{cx-10}" y1="{cy+50}" x2="{cx+cw+10}" y2="{cy+50}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    def lab(x,y,tx,ty,lines,anchor='end'):
        s=f'<path d="M{x} {y} L{tx} {ty}" stroke="{INK}" stroke-width="0.8" fill="none"/><circle cx="{x}" cy="{y}" r="2.2" fill="{INK}"/>'
        for i,l in enumerate(lines): s+=f'<text x="{tx+(-4 if anchor=="end" else 4)}" y="{ty+4+i*14}" text-anchor="{anchor}" font-size="11.5" fill="{INK}" {"font-weight=\"800\"" if i==0 else ""}>{l}</text>'
        return s
    o.append(lab(cx+22,cy+26,cx-20,cy+20,['Slot','Elmo, Arma o Corpo']))
    o.append(lab(cx+70,cy+40,cx-20,cy+70,['Nome e bonus','restano visibili quando','infili la carta nella scheda']))
    o.append(lab(cx+cw+10,cy+50,cx+cw+20,cy+56,['Linea di infilata','sotto: nascosto'],'start'))
    o.append(lab(cx+cw-30,cy+178,cx+cw+20,cy+150,['Durata','spade = scontri','clessidra = turni','numero = cubetti'],'start'))
    o.append(lab(cx+14,cy+ch-14,cx-20,cy+ch-40,['Mazzetto','colore della classe']))
    o.append(lab(cx+cw-60,cy+ch-14,cx+cw+20,cy+ch-30,['Scatola e numero'],'start'))
    o.append('</svg>')
    return '\n'.join(o)

def turn_strip(big=False):
    steps=[('clessidra','Clessidre','Ne hai una? Toglila e salta al passo 5.'),
           ('carte','Carte','Fino a 2 in tutto il turno, quando vuoi. Max 1 equipaggiamento.'),
           ('piedi','Muovi','Tira D6 + MOV. Muovi fino a quel numero (almeno 1).'),
           ('occhio','Esplora','Dove ti fermi succede qualcosa. Un solo scontro per turno.'),
           ('bandiera','Fine','Togli un cubetto dalle carte a clessidra. Passa i dadi.')]
    h=[]
    for i,(ic,t,d) in enumerate(steps):
        h.append(f'<div class="step"><div class="num">{i+1}</div><svg viewBox="0 0 24 24" class="sic">{icon(ic,12,12,1,BROWN)}</svg><div class="st">{t}</div><div class="sd">{d}</div></div>')
    return '<div class="strip'+(' big' if big else '')+'">'+''.join(h)+'</div>'

def cover_art():
    return f'''<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="gl" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#f6d68b" stop-opacity="0.9"/><stop offset="1" stop-color="#f6d68b" stop-opacity="0"/></radialGradient></defs>
<circle cx="150" cy="120" r="110" fill="url(#gl)"/>
<g transform="translate(150 130)">
<path d="M-80 -10 a80 50 0 0 1 160 0 z" fill="#7a4a24" stroke="#3b2414" stroke-width="3"/>
<rect x="-80" y="-10" width="160" height="78" rx="6" fill="#8a5428" stroke="#3b2414" stroke-width="3"/>
<rect x="-80" y="-4" width="160" height="14" fill="{GOLD}" stroke="#3b2414" stroke-width="2"/>
<rect x="-80" y="44" width="160" height="10" fill="{GOLD}" stroke="#3b2414" stroke-width="2"/>
<rect x="-14" y="-12" width="28" height="36" rx="4" fill="{GOLD}" stroke="#3b2414" stroke-width="2.5"/>
<circle cx="0" cy="4" r="5" fill="#3b2414"/><rect x="-2" y="4" width="4" height="10" fill="#3b2414"/>
<path d="M-60 -38 q-6 -16 -22 -18 M60 -38 q6 -16 22 -18" stroke="#3b2414" stroke-width="3" fill="none"/>
<circle cx="-30" cy="-30" r="7" fill="#fff" stroke="#3b2414" stroke-width="2"/><circle cx="30" cy="-30" r="7" fill="#fff" stroke="#3b2414" stroke-width="2"/>
<circle cx="-28" cy="-29" r="3" fill="#3b2414"/><circle cx="28" cy="-29" r="3" fill="#3b2414"/>
</g>
<g fill="{GOLD}" stroke="#7a5a1c" stroke-width="1.5"><ellipse cx="70" cy="200" rx="14" ry="6"/><ellipse cx="88" cy="194" rx="14" ry="6"/><ellipse cx="226" cy="200" rx="14" ry="6"/><ellipse cx="240" cy="192" rx="14" ry="6"/><ellipse cx="208" cy="206" rx="14" ry="6"/></g>
</svg>'''
