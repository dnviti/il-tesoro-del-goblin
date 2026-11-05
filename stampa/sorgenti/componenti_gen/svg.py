import math
INK='#2a2118'; BROWN='#6b4a2b'; RED='#9c2f24'; GOLD='#b8862b'; BLUE='#2f5d7c'
EDIFICI=False  # True = vecchia plancia con gli edifici stampati
CAMP='#7a4f86'; LOC='#c0662b'; FON='#2f7a8a'; FAB='#4a5568'; CUORE='#e6d6b4'; LINE='#b9a582'; PAPER='#f4ead5'

def hexpts(x,y,s):
    return ' '.join(f'{x+s*math.cos(math.radians(a)):.2f},{y+s*math.sin(math.radians(a)):.2f}' for a in (-90,-30,30,90,150,210))

# ---------- icons (drawn in a 24x24 box centred on x,y, scaled by k) ----------
def icon(name,x,y,k=1,col=INK):
    t=f'transform="translate({x-12*k:.2f},{y-12*k:.2f}) scale({k})"'
    s={
    'clessidra':f'<g {t} fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"><path d="M6 3h12M6 21h12M7 3c0 6 10 6 10 9s-10 3-10 9M17 3c0 6-10 6-10 9s10 3 10 9"/><path d="M9 19h6l-3-3z" fill="{col}"/></g>',
    'spade':f'<g {t} fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"><path d="M4 4l12 12M20 4L8 16M14 18l4 2 2-4M10 18l-4 2-2-4"/></g>',
    'cuore':f'<g {t}><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z" fill="{col}"/></g>',
    'scudo':f'<g {t}><path d="M12 2l8 3v6c0 5.5-3.6 9.3-8 11-4.4-1.7-8-5.5-8-11V5z" fill="{col}"/></g>',
    'stivale':f'<g {t}><path d="M7 2h7v10l6 3v5H5v-5l2-1z" fill="{col}"/></g>',
    'stella':f'<g {t}><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7L12 17.2 5.8 20.9l1.6-7L2 9.2l7.1-.6z" fill="{col}"/></g>',
    'pergamena':f'<g {t} fill="none" stroke="{col}" stroke-width="2"><path d="M6 4h11a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M9 9h7M9 13h7M9 17h4" /><path d="M14 10l2 2-2 2" stroke="{RED}"/></g>',
    'forziere':f'<g {t}><path d="M3 10a9 6 0 0 1 18 0z" fill="{BROWN}"/><rect x="3" y="10" width="18" height="10" rx="1.5" fill="{BROWN}"/><rect x="3" y="11" width="18" height="2.5" fill="{GOLD}"/><rect x="10.5" y="10" width="3" height="5" rx="1" fill="{GOLD}"/></g>',
    'casa':f'<g {t}><path d="M3 11l9-8 9 8v10H3z" fill="{col}"/><rect x="10" y="14" width="4" height="7" fill="{PAPER}"/></g>',
    'goccia':f'<g {t}><path d="M12 2s7 8 7 12.5A7 7 0 0 1 5 14.5C5 10 12 2 12 2z" fill="{col}"/></g>',
    'martello':f'<g {t}><rect x="4" y="4" width="11" height="6" rx="1" fill="{col}"/><rect x="9" y="9" width="3" height="13" rx="1" fill="{col}"/></g>',
    'teschio':f'<g {t}><path d="M12 3a8 8 0 0 0-8 8c0 3 1.5 4.5 3 5.5V20h10v-3.5c1.5-1 3-2.5 3-5.5a8 8 0 0 0-8-8z" fill="{col}"/><circle cx="9" cy="11" r="2" fill="{PAPER}"/><circle cx="15" cy="11" r="2" fill="{PAPER}"/></g>',
    'trappola':f'<g {t} fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round"><path d="M3 18h18M5 18l2-8 2 8 2-8 2 8 2-8 2 8 2-8"/></g>',
    'occhio':f'<g {t} fill="none" stroke="{col}" stroke-width="2"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3" fill="{col}"/></g>',
    'dado':f'<g {t}><rect x="3" y="3" width="18" height="18" rx="4" fill="none" stroke="{col}" stroke-width="2"/><circle cx="8" cy="8" r="1.6" fill="{col}"/><circle cx="16" cy="16" r="1.6" fill="{col}"/><circle cx="12" cy="12" r="1.6" fill="{col}"/></g>',
    'carte':f'<g {t} fill="none" stroke="{col}" stroke-width="2"><rect x="3" y="5" width="11" height="15" rx="2" transform="rotate(-10 8 12)"/><rect x="10" y="4" width="11" height="15" rx="2" fill="{PAPER}"/></g>',
    'freccia':f'<g {t} fill="none" stroke="{col}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></g>',
    'piedi':f'<g {t}><ellipse cx="8" cy="9" rx="3" ry="5" fill="{col}"/><ellipse cx="16" cy="15" rx="3" ry="5" fill="{col}"/></g>',
    'bandiera':f'<g {t}><rect x="5" y="3" width="2" height="18" fill="{col}"/><path d="M7 4h12l-3 4 3 4H7z" fill="{col}"/></g>',
    'elmo':f'<g {t}><path d="M4 14a8 8 0 0 1 16 0v6h-5v-4H9v4H4z" fill="{col}"/><rect x="11" y="2" width="2" height="5" fill="{col}"/></g>',
    'cripta':f'<g {t}><path d="M4 21V10a8 8 0 0 1 16 0v11z" fill="{GOLD}"/><path d="M9 21v-7a3 3 0 0 1 6 0v7z" fill="{PAPER}"/></g>',
    }[name]
    return s

def q_mark(x,y,r=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><text x="{x:.1f}" y="{y+r*0.55:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{r*1.5:.1f}" fill="{INK}">?</text>'

# ---------- Crepe del Caos (espansione) ----------
CAOS='#7a3e8e'
CREPE=[(4,0),(3,2),(7,4),(4,4),(9,2)]  # + le stesse ruotate di 180°: 10 tessere
def crepa_tile(x,y,R):
    # tessera esagonale viola con la crepa luminosa di MIMI
    k=R/15
    return (f'<polygon points="{hexpts(x,y,R*0.93)}" fill="{CAOS}" stroke="#4b2259" stroke-width="1.2"/>'
            f'<path d="M{x-6*k:.1f} {y-10*k:.1f} L{x-1*k:.1f} {y-3*k:.1f} L{x-5*k:.1f} {y+1*k:.1f} L{x+2*k:.1f} {y+10*k:.1f} L{x+1*k:.1f} {y+2*k:.1f} L{x+6*k:.1f} {y-1*k:.1f} Z" fill="#f6d68b"/>')

# ---------- board ----------
def board(W=26, full=True, show_bands=True, label=True, heroes=None, scale_note=False, caos_tiles=False):
    R=W/math.sqrt(3); step=1.5*R
    mapw=W*10.5; maph=9*step+2*R
    pad=W*1.8
    top=W*4.5 if show_bands else pad; bottom=W*4.3 if show_bands else pad
    bw=mapw+2*pad; bh=maph+top+bottom
    X0=pad; Y0=top
    hx=lambda c,r: X0+W*(c+0.5+(r%2)*0.5)
    hy=lambda c,r: Y0+R+r*step
    rot=lambda p:[(p[0],p[1]),(9-p[0],9-p[1])]
    both=lambda L:[q for p in L for q in rot(p)]
    spawns=[(2,0),(7,0),(9,4),(7,9),(2,9),(0,5)]; loc=both([(1,4)]); fon=both([(4,1)]); fab=both([(8,1)])
    # scatola base senza Caos: le 10 Crepe stanno nell'espansione «Il Caos del Goblin» (caos_tiles=True le mostra posate)
    caos=both(CREPE) if caos_tiles else []
    qs=both([(6,0),(8,0),(1,1),(3,1),(6,1),(2,2),(5,2),(8,2),(9,1),(4,3),(7,3),(8,3),(0,3),(2,4),(5,4)]); crip=[(3,3),(6,3),(3,6),(6,6)]
    # Locanda, Fonte e Fabbro sono segnalini del sacchetto (Daniele, 2/11): le loro 6 caselle diventano «?»
    if not EDIFICI: qs+=loc+fon+fab; loc=fon=fab=[]
    o=[f'<svg viewBox="0 0 {bw:.1f} {bh:.1f}" xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans">']
    o.append(f'<rect x="1" y="1" width="{bw-2:.1f}" height="{bh-2:.1f}" rx="{W*0.5}" fill="#efe1c3" stroke="{BROWN}" stroke-width="2"/>')
    for r in range(10):
        for c in range(10):
            inC=2<=c<=7 and 2<=r<=7
            o.append(f'<polygon points="{hexpts(hx(c,r),hy(c,r),R*0.97)}" fill="{CUORE if inC else "#f7efdc"}" stroke="{LINE}" stroke-width="0.8"/>')
    # cuore border
    o.append(f'<rect x="{hx(2,2)-W*0.75:.1f}" y="{hy(2,2)-R*1.05:.1f}" width="{W*6.75:.1f}" height="{5*step+2.1*R:.1f}" rx="6" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    for i,(c,r) in enumerate(spawns):
        o.append(f'<polygon points="{hexpts(hx(c,r),hy(c,r),R*0.97)}" fill="{CAMP}" fill-opacity="0.75" stroke="{CAMP}" stroke-width="1.2"/>')
        o.append(f'<text x="{hx(c,r):.1f}" y="{hy(c,r)+R*0.33:.1f}" text-anchor="middle" font-family="Alegreya Sans" font-weight="800" font-size="{R*0.9:.1f}" fill="#fff">{i+1}</text>')
    for (c,r) in crip: o.append(f'<polygon points="{hexpts(hx(c,r),hy(c,r),R*0.97)}" fill="{GOLD}" fill-opacity="0.45" stroke="{GOLD}" stroke-width="1.6"/>')
    k=W/26*0.62
    for (c,r) in loc: o.append(icon('casa',hx(c,r),hy(c,r),k,LOC))
    for (c,r) in fon: o.append(icon('goccia',hx(c,r),hy(c,r),k,FON))
    for (c,r) in fab: o.append(icon('martello',hx(c,r),hy(c,r),k,FAB))
    for (c,r) in qs: o.append(q_mark(hx(c,r),hy(c,r),R*0.42))
    for (c,r) in caos:
        o.append(crepa_tile(hx(c,r),hy(c,r),R))
        if caos_tiles=='coppie':  # lettera della coppia di Crepe gemelle (A-E), in basso a destra
            k=[x for x in CREPE if x in ((c,r),(9-c,9-r))][0]; L='ACDEB'[CREPE.index(k)]
            o.append(f'<circle cx="{hx(c,r)+R*0.55:.1f}" cy="{hy(c,r)+R*0.5:.1f}" r="{R*0.42:.1f}" fill="#fff" stroke="{CAOS}" stroke-width="0.8"/><text x="{hx(c,r)+R*0.55:.1f}" y="{hy(c,r)+R*0.5+R*0.19:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{R*0.56:.1f}" fill="{CAOS}">{L}</text>')
    for n,(c,r) in zip('1234',crip):
        o.append(f'<text x="{hx(c,r):.1f}" y="{hy(c,r)+R*0.35:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{R*0.95:.1f}" fill="{INK}">{n}</text>')
    if label:
        cols='ABCDEFGHIJ'
        for c in range(10):
            o.append(f'<text x="{hx(c,0)-W*0.25:.1f}" y="{Y0-4:.1f}" text-anchor="middle" font-size="{W*0.32:.1f}" fill="{BROWN}">{cols[c]}</text>')
        for r in range(10):
            o.append(f'<text x="{X0-6:.1f}" y="{hy(0,r)+3:.1f}" text-anchor="end" font-size="{W*0.32:.1f}" fill="{BROWN}">{r+1}</text>')
    if show_bands:
        # sala del tesoro
        o.append(f'<text x="{bw/2:.1f}" y="{W*0.95:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{W*0.55:.1f}" fill="{BROWN}">Sala del Tesoro</text>')
        cy=W*1.75
        # niente mini-boss (Daniele, 2/11): il boss custode, MIMI e i 2 boss del mazzetto 3
        spots=[('Custode',W*0.75,True),('MIMI',W*0.55,False),('Boss',W*0.6,False),('Boss',W*0.6,False)]
        xs=[bw/2+(i-1.5)*W*2.3 for i in range(4)]
        for (nm,rad,big),x in zip(spots,xs):
            o.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="{GOLD if big else "#f7efdc"}" fill-opacity="{0.5 if big else 1}" stroke="{BROWN}" stroke-width="1.2"/>')
            o.append(f'<text x="{x:.1f}" y="{cy+rad+W*0.42:.1f}" text-anchor="middle" font-size="{W*0.34:.1f}" fill="{INK}">{nm}</text>')
        # tracciato PV del Guardiano
        bx=W*0.62; ty=W*3.25; x0=bw/2-4.5*bx+W*1.3
        o.append(f'<text x="{x0-W*0.2:.1f}" y="{ty+bx*0.68:.1f}" text-anchor="end" font-size="{W*0.32:.1f}" font-weight="700" fill="{INK}">PV del boss</text>')
        for i in range(9):
            v=9-i
            o.append(f'<rect x="{x0+i*bx:.1f}" y="{ty:.1f}" width="{bx*0.9:.1f}" height="{bx*0.9:.1f}" rx="2" fill="{"#e9c9a8" if v<=4 else "#f7efdc"}" stroke="{BROWN}" stroke-width="0.8"/>')
            o.append(f'<text x="{x0+i*bx+bx*0.45:.1f}" y="{ty+bx*0.62:.1f}" text-anchor="middle" font-size="{W*0.27:.1f}" fill="{INK}">{v}</text>')
        yb=Y0+maph+W*0.9
        o.append(f'<text x="{bw/2:.1f}" y="{yb:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{W*0.5:.1f}" fill="{BROWN}">Promemoria</text>')
        o.append(f'<text x="{bw/2:.1f}" y="{yb+W*0.75:.1f}" text-anchor="middle" font-size="{W*0.38:.1f}" fill="{INK}">Turno: Clessidre · Carte · Muovi · Esplora · Fine</text>')
        o.append(f'<text x="{bw/2:.1f}" y="{yb+W*1.35:.1f}" text-anchor="middle" font-size="{W*0.38:.1f}" fill="{INK}">Perdita D6: 1 tutto · 2 elmo · 3 arma DX · 4 arma SX · 5 armatura · 6 niente</text>')
        # tracciato dei giri e Presagio (tolto il 27/10: Indizi solo dagli scontri)
        if False:
            gx=W*0.6; gy=yb+W*1.85; g0=bw/2-10*gx+W*0.6
            o.append(f'<text x="{g0-W*0.2:.1f}" y="{gy+gx*0.66:.1f}" text-anchor="end" font-size="{W*0.32:.1f}" font-weight="700" fill="{INK}">Giro</text>')
            band={8:'#efd9a6',9:'#efd9a6',10:'#efd9a6',11:'#e9c58e',12:'#e9c58e',13:'#e9c58e',14:'#e2b077',15:'#e2b077',16:'#e2b077',17:'#d99a62',18:'#d99a62',19:'#d99a62',20:'#cf834e'}
            for i in range(20):
                n=i+1
                o.append(f'<rect x="{g0+i*gx:.1f}" y="{gy:.1f}" width="{gx*0.9:.1f}" height="{gx*0.9:.1f}" rx="2" fill="{band.get(n,"#f7efdc")}" stroke="{BROWN}" stroke-width="0.8"/>')
                o.append(f'<text x="{g0+i*gx+gx*0.45:.1f}" y="{gy+gx*0.62:.1f}" text-anchor="middle" font-size="{W*0.26:.1f}" fill="{INK}">{n}</text>')
            for lab,a0,a1 in [('D6: 6',8,10),('5+',11,13),('4+',14,16),('3+',17,19),('2+',20,20)]:
                cx=g0+((a0+a1)/2-1)*gx+gx*0.45
                o.append(f'<text x="{cx:.1f}" y="{gy+gx*1.45:.1f}" text-anchor="middle" font-size="{W*0.27:.1f}" font-weight="700" fill="{BROWN}">{lab}</text>')
            o.append(f'<text x="{g0+3*gx:.1f}" y="{gy+gx*1.45:.1f}" text-anchor="middle" font-size="{W*0.27:.1f}" fill="{BROWN}">Presagio del Goblin →</text>')
    if heroes:
        for (c,r,col) in heroes:
            o.append(f'<circle cx="{hx(c,r):.1f}" cy="{hy(c,r):.1f}" r="{R*0.6:.1f}" fill="{col}" stroke="{PAPER}" stroke-width="1.5"/>')
    o.append('</svg>')
    return '\n'.join(o)

def legend_item(ic,label,col=INK):
    return f'<div class="lg"><svg viewBox="0 0 24 24" width="16" height="16">{ic}</svg><span>{label}</span></div>'
