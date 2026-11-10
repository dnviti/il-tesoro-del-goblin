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

def color_token(ic,label,fill,size=46):
    # tessera Esplorazione colorata (Daniele, 2/11): rossa = Mostro, blu = Imprevisto
    s=size;c=s/2
    return f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}"><circle cx="{c}" cy="{c}" r="{c-1.5}" fill="{fill}" stroke="{BROWN}" stroke-width="2"/>{icon(ic,c,c*0.85,s/46*0.9,"#fff")}<text x="{c}" y="{s*0.86}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.15}" fill="#fff">{label}</text></svg>'

def simple_token(ic,label,col,size=46):
    s=size;c=s/2
    return f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}"><circle cx="{c}" cy="{c}" r="{c-1.5}" fill="#efe1c3" stroke="{BROWN}" stroke-width="2"/>{icon(ic,c,c*0.85,s/46*0.9,col)}<text x="{c}" y="{s*0.86}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{s*0.15}" fill="{INK}">{label}</text></svg>'

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
    o.append(f'<text x="{xs[4]}" y="{y+36}" text-anchor="middle" font-size="11.5" font-weight="700" fill="{RED}">ti fermi qui:</text><text x="{xs[4]}" y="{y+50}" text-anchor="middle" font-size="11.5" font-weight="700" fill="{RED}">peschi una tessera</text>')
    o.append(f'<g transform="translate(330,24)"><rect width="180" height="76" rx="8" fill="#fffaf0" stroke="{BROWN}"/><text x="90" y="24" text-anchor="middle" font-weight="800" font-size="13" fill="{INK}">D6 = 3, MOV = 1</text><text x="90" y="46" text-anchor="middle" font-size="12.5" fill="{INK}">ti muovi fino a 4 esagoni</text><text x="90" y="65" text-anchor="middle" font-size="11.5" fill="{BROWN}">(anche meno, ma almeno 1)</text></g>')
    o.append('</svg>')
    return '\n'.join(o)

def turn_strip(big=False):
    steps=[('piedi','Muovi','Tira D6 + MOV. Muovi fino a quel numero (almeno 1).'),
           ('occhio','Esplora','Dove ti fermi succede qualcosa. Un solo scontro per turno.'),
           ('bandiera','Fine','Togli gli stati dritti, raddrizza quelli di traverso. Carte giocate negli scarti. Tocca a sinistra.')]
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


def enemy_card(name, letter, lv, pv, att, ar, rewards, abil='', w=300):
    """Carta Nemico come nel layout Canva della carta Nemico (orizzontale 3:2)."""
    NAV='#0c1631'; G='#d8a53a'; P='#f1dcae'
    o=[f'<svg viewBox="0 0 450 300" width="{w}" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">']
    o.append(f'<rect x="2" y="2" width="446" height="296" rx="12" fill="{NAV}" stroke="{G}" stroke-width="3"/>')
    o.append(f'<circle cx="46" cy="40" r="30" fill="#2a1350" stroke="{G}" stroke-width="2.5"/><text x="46" y="52" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="32" fill="#c9a5f0">{letter}</text>')
    o.append(f'<rect x="88" y="10" width="270" height="44" rx="5" fill="{NAV}" stroke="{G}" stroke-width="1.6"/><text x="223" y="40" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{19 if len(name)<18 else 15}" fill="#f2cf73">{name.upper()}</text>')
    o.append(f'<rect x="366" y="10" width="72" height="44" rx="5" fill="{NAV}" stroke="{G}" stroke-width="1.6"/><text x="402" y="40" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="18" fill="#f2cf73">LV. {lv}</text>')
    o.append(f'<rect x="16" y="64" width="222" height="150" rx="4" fill="#1d2a4d" stroke="{G}" stroke-width="1"/><text x="127" y="144" text-anchor="middle" font-size="12" fill="#8fa0c8">illustrazione</text>')
    for i,(lab,v,ic,col) in enumerate((('PV',pv,'cuore',RED),('ATT',att,'spade',INK),('AR',ar,'scudo',BLUE))):
        y=64+i*51
        o.append(f'<rect x="250" y="{y}" width="188" height="45" rx="5" fill="{P}" stroke="{G}" stroke-width="1.5"/><circle cx="275" cy="{y+22.5}" r="14" fill="{NAV}"/>'+icon(ic,275,y+22.5,0.62,'#f2cf73' if ic!='cuore' else '#e04a4a')+f'<text x="298" y="{y+29}" font-family="Cinzel" font-weight="800" font-size="15" fill="{NAV}">{lab}</text><text x="425" y="{y+34}" text-anchor="end" font-family="Cinzel" font-weight="800" font-size="30" fill="{NAV}">{v}</text>')
    o.append(f'<rect x="16" y="222" width="208" height="68" rx="5" fill="{P}" stroke="{G}" stroke-width="1.5"/><text x="26" y="240" font-family="Cinzel" font-weight="800" font-size="11" fill="{NAV}">ABILITÀ SPECIALI</text><line x1="26" y1="245" x2="214" y2="245" stroke="{NAV}" stroke-width="0.8"/><text x="26" y="262" font-size="11" fill="{NAV}">{abil}</text>')
    o.append(f'<rect x="232" y="222" width="206" height="68" rx="5" fill="{P}" stroke="{G}" stroke-width="1.5"/><text x="242" y="240" font-family="Cinzel" font-weight="800" font-size="11" fill="{NAV}">RICOMPENSE</text><line x1="242" y1="245" x2="428" y2="245" stroke="{NAV}" stroke-width="0.8"/>')
    for i,r in enumerate(rewards): o.append(f'<text x="242" y="{262+i*13}" font-weight="800" font-size="11" fill="{NAV}">{r}</text>')
    o.append('</svg>')
    return ''.join(o)
