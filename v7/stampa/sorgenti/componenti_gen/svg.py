import math
INK='#2a2118'; BROWN='#6b4a2b'; RED='#9c2f24'; GOLD='#b8862b'; BLUE='#2f5d7c'
LINE='#b9a582'; PAPER='#f4ead5'

# ---------- kit dei motivi (Daniele, 11/11: «leggero flavour steampunk medieval high magic, minimale, bordo leggero») ----------
# Lo stesso delle carte (carte/genera_carte.py, «kit dei motivi»), descritto in stampa/LEGGIMI.md: ottone scuro sui fondi
# chiari, ottone chiaro sui fondi colorati, rame per gli accenti; filetto doppio, piccoli ingranaggi agli angoli, rivetti,
# losanghe e stelle arcane. Solo tratti sottili sui bordi: le misure dei contenuti non cambiano.
BRASS='#a8823a'; BRASS_L='#e8cd8f'; COPPER='#a65a32'; PLATE='#f7eedb'

def cog_pts(cx,cy,r,n,prof=0.28):
    """punti di un ingranaggio di raggio esterno r: n denti trapezi profondi prof*r, il primo in alto."""
    ri=r*(1-prof); s=2*math.pi/n; p=[]
    for k in range(n):
        a=k*s-math.pi/2
        for da,rr in ((-0.27,ri),(-0.15,r),(0.15,r),(0.27,ri)):
            p.append(f'{cx+rr*math.cos(a+da*s):.3f},{cy+rr*math.sin(a+da*s):.3f}')
    return ' '.join(p)

def cog(cx,cy,r,n=8,fill=BRASS_L,hole=None,prof=0.28,stroke=None,sw=0.2):
    """ingranaggio pieno; hole: colore del tondo al centro (quello del fondo)."""
    st=f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
    o=f'<polygon points="{cog_pts(cx,cy,r,n,prof)}" fill="{fill}"{st}/>'
    if hole: o+=f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{0.3*r:.3f}" fill="{hole}"/>'
    return o

def rivet(cx,cy,r,fill=BRASS_L,edge=BRASS,sw=0.1):
    st=f' stroke="{edge}" stroke-width="{sw}"' if edge else ''
    return f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="{fill}"{st}/>'

def lozenge(cx,cy,w,h,fill=COPPER,edge=None,sw=0.1):
    st=f' stroke="{edge}" stroke-width="{sw}" stroke-linejoin="round"' if edge else ''
    return f'<polygon points="{cx:.3f},{cy-h/2:.3f} {cx+w/2:.3f},{cy:.3f} {cx:.3f},{cy+h/2:.3f} {cx-w/2:.3f},{cy:.3f}" fill="{fill}"{st}/>'

def star(cx,cy,r,n=4,ratio=0.4,fill=COPPER):
    """stella arcana a n punte, la prima in alto."""
    p=' '.join(f'{cx+(r if k%2==0 else r*ratio)*math.cos(math.pi*k/n-math.pi/2):.3f},{cy+(r if k%2==0 else r*ratio)*math.sin(math.pi*k/n-math.pi/2):.3f}' for k in range(2*n))
    return f'<polygon points="{p}" fill="{fill}"/>'

def brass_frame(x0,y0,x1,y1,gap=0.8,sw=0.35,sw2=0.15,col=BRASS,cog_r=2.0,holes=('#ffffff',)*4,rx=1.0):
    """filetto doppio d'ottone (esterno sw sul rettangolo, interno sw2 a gap dentro) e un ingranaggio su ogni angolo
    dell'esterno; holes: colore del foro dei 4 ingranaggi (alto-sinistra, alto-destra, basso-sinistra, basso-destra)."""
    o=[f'<rect x="{x0:.3f}" y="{y0:.3f}" width="{x1-x0:.3f}" height="{y1-y0:.3f}" rx="{rx}" fill="none" stroke="{col}" stroke-width="{sw}"/>',
       f'<rect x="{x0+gap:.3f}" y="{y0+gap:.3f}" width="{x1-x0-2*gap:.3f}" height="{y1-y0-2*gap:.3f}" rx="{max(rx-gap,0.2):.3f}" fill="none" stroke="{col}" stroke-width="{sw2}"/>']
    for (x,y),h in zip(((x0,y0),(x1,y0),(x0,y1),(x1,y1)),holes):
        o.append(cog(x,y,cog_r,8,BRASS_L,h,stroke=col,sw=0.12))
    return ''.join(o)

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
    'spunta':f'<g {t} fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6"/></g>',
    }[name]
    return s

def q_mark(x,y,r=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><text x="{x:.1f}" y="{y+r*0.55:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{r*1.5:.1f}" fill="{INK}">?</text>'

# ---------- rotelle (volvelle): corona di valori stampata sotto un disco Ø 52 mm con una finestra ----------
# Misure in mm. La corona sta a RING_R dal centro (rr per rotella); il disco (pezzo a parte, fermacampioni al centro)
# la copre e mostra un solo valore nella finestra. Le etichette restano dritte: la finestra le contiene a ogni angolo.
CAP=0.716            # altezza delle cifre / corpo (Liberation Sans Narrow)
RING_R=20.0; DISC_R=26.0
def dial_block(main, smalls=(), mh=4.5, sf=2.0, gap=0.6):
    """righe di un'etichetta centrata in (0,0): [(testo, corpo, baseline, grassetto)] e altezza del blocco."""
    h=mh+len(smalls)*(gap+sf*CAP)
    y=-h/2+mh; out=[(main,mh/CAP,y,True)]
    for s in smalls:
        y+=gap+sf*CAP; out.append((s,sf,y,False))
    return out,h

def dial_angle(i,n): return i*360.0/n   # gradi, 0 = in alto, senso orario

def dial_ring(cx,cy,vals,k=1.0,mh=4.5,sf=2.0,gap=0.6,gold=(),red=(),col=INK,hole=True,footprint=True,rr=RING_R):
    """corona di N valori (il primo in alto, poi in senso orario) a rr mm da (cx, cy); k = unità del disegno per mm.
    vals: [(testo grande, (righe piccole...))]; gold: indici con il cerchio dorato; red: indici in rosso."""
    o=[f'<g transform="translate({cx:.3f},{cy:.3f}) scale({k:.5f})">']
    if footprint:   # kit dei motivi: piatto chiaro col bordo a ingranaggio (36 denti) che sporge di 0,9 mm dal disco
        o.append(cog(0,0,DISC_R+0.9,36,PLATE,prof=0.026,stroke=BRASS,sw=0.25))
    n=len(vals)
    for i,(main,smalls) in enumerate(vals):
        a=math.radians(dial_angle(i,n)); x=rr*math.sin(a); y=-rr*math.cos(a)
        if i in gold: o.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="4.8" fill="#ecd7a6"/>')
        rows,_=dial_block(main,smalls,mh,sf,gap)
        for t,fs,by,b in rows:
            c=RED if i in red else col
            o.append(f'<text x="{x:.3f}" y="{y+by:.3f}" text-anchor="middle" font-family="Alegreya Sans"{" font-weight=\"800\"" if b else ""} font-size="{fs:.3f}" fill="{c}">{t}</text>')
    if hole:   # foro: punteruolo al centro per il fermacampioni, cerchio Ø 4 per il perno della rotella 3D (3d_solidcraft)
        o.append(f'<circle cx="0" cy="0" r="2" fill="none" stroke="{INK}" stroke-width="0.25"/><path d="M-3 0H3M0 -3V3" stroke="{INK}" stroke-width="0.2"/>')
    o.append('</g>')
    return ''.join(o)

# ---------- Sala del Tesoro ----------
def sala_tesoro(bw, W=26, mm=0.97):
    """elementi della fascia della Sala del Tesoro (larga bw unità del disegno, alta circa 104): titolo, cerchi di Custode,
    MIMI e Boss, corone 0-9 delle rotelle del tavolo e cerchi «Spostamenti del tesoro». La disegna gen.py sala_disegno()
    (la Sala come pezzo a parte, accanto alla mappa)."""
    o=[]
    o.append(f'<text x="{bw/2:.1f}" y="{W*0.95:.1f}" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="{W*0.55:.1f}" fill="{BROWN}">Sala del Tesoro</text>')
    cy=W*1.75
    # niente mini-boss (Daniele, 2/11): il boss custode, MIMI e i 2 boss del mazzetto 3
    spots=[('Custode',W*0.75,True),('MIMI',W*0.55,False),('Boss',W*0.6,False),('Boss',W*0.6,False)]
    xs=[bw/2+(i-1.5)*W*2.3 for i in range(4)]
    for (nm,rad,big),x in zip(spots,xs):
        o.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="{GOLD if big else "#f7efdc"}" fill-opacity="{0.5 if big else 1}" stroke="{BROWN}" stroke-width="1.2"/>')
        o.append(f'<text x="{x:.1f}" y="{cy+rad+W*0.42:.1f}" text-anchor="middle" font-size="{W*0.34:.1f}" fill="{INK}">{nm}</text>')
    # Rotella dello scontro (sinistra) e Rotella del custode (destra): corona 0-9 sotto un disco Ø 52 col fermacampioni
    u=1/mm; ry=55*u
    for rx,t1,t2 in ((40*u,'PV del mostro','Rotella dello scontro'),(316*u,'PV del custode','le ferite restano')):
        o.append(dial_ring(rx,ry,[(str(v),()) for v in range(10)],k=u))
        o.append(f'<text x="{rx:.1f}" y="{ry+(DISC_R+4.6)*u:.1f}" text-anchor="middle" font-weight="800" font-size="{3.6*u:.2f}" fill="{INK}">{t1}</text>')
        o.append(f'<text x="{rx:.1f}" y="{ry+(DISC_R+8.6)*u:.1f}" text-anchor="middle" font-size="{2.9*u:.2f}" fill="{BROWN}">{t2}</text>')
    # Spostamenti del tesoro: 2 cerchi Ø 22 per le tessere Usato, sotto Custode e MIMI
    sy=89.5*u
    for sx in (105*u,131*u):
        o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{11*u:.2f}" fill="#f7efdc" stroke="{BROWN}" stroke-width="{0.35*u:.2f}" stroke-dasharray="{1.5*u:.2f} {1*u:.2f}"/>')
    for j,(t,fs,wt,col) in enumerate((('Spostamenti',3.4,' font-weight="800"',INK),('del tesoro (max 2)',3.4,' font-weight="800"',INK),('1 tessera Usato ogni',2.8,'',BROWN),('volta che cambia Cripta',2.8,'',BROWN))):
        o.append(f'<text x="{91.5*u:.1f}" y="{(83.6+j*4.1)*u:.1f}" text-anchor="end"{wt} font-size="{fs*u:.2f}" fill="{col}">{t}</text>')
    return o

def legend_item(ic,label,col=INK):
    return f'<div class="lg"><svg viewBox="0 0 24 24" width="16" height="16">{ic}</svg><span>{label}</span></div>'
