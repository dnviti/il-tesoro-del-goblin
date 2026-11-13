#!/usr/bin/env python3
"""Schemi S2-turno, S4-scontro, S5-indizio, S7-perdita del regolamento «Il Tesoro del Goblin».

Riusa gli aiuti geometrici e le icone di ../../vettoriali/sorgenti/genera_vettoriali.py (senza modificarlo).
Per ogni schema: SVG sorgente -> .vectorcraft (testo vivo, modificabile) -> <id>.svg (testo in tracciati, unita' in pt)
-> <id>.pdf e <id>.png a 200 ppi. Uso: genera_schemi_semplici.py [S2-turno S4-scontro ...]
"""
import math, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)                                   # .../schemi
KIT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'vettoriali', 'sorgenti')
TMP = tempfile.mkdtemp(prefix='schemi_')
_argv = sys.argv[1:]
sys.argv = [sys.argv[0], TMP]                                  # il kit usa argv[1] come cartella temporanea
sys.path.insert(0, KIT)
import genera_vettoriali as g
from genera_vettoriali import (INK, BROWN, RED, BLUE, GOLD, GOLDL, BRASS, BRASSL, COPPER, PAPER, PARCH, GREEN, VIOLET,
                               C, S, rot, mv, sc, wob, ell, arcpts, rr, cog, star4, lozenge, f, P, poly, line, disc, G,
                               gear, rivet)
from PIL import ImageFont

GREY = '#bdb5a3'; GREYT = '#5c5446'; SAND = '#d8bf86'; WOODG = '#7fa56b'

# ---------------------------------------------------------------- misura del testo (IBM Plex Sans Condensed)
_FD = '/usr/share/fonts/ibm-plex-sans-fonts/IBMPlexSansCondensed-%s.otf'
_WN = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'}
_fc = {}
def tw(s, size, w=400):
    if w not in _fc: _fc[w] = ImageFont.truetype(_FD % _WN[w], 100)
    return _fc[w].getlength(s) * size / 100

TXT = []   # (x0, y0, x1, y1, testo) per i controlli di sovrapposizione
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def T(x, y, s, size=10, w=400, fill=INK, anchor='middle', serif=False, track=True):
    """Testo a baseline y. Plex Condensed per le etichette, Noto Serif Bold per i titoli/numeri."""
    if serif:
        fam, wt = 'Noto Serif', 700; width = tw(s, size, 700) * 1.18
    else:
        fam, wt = 'IBM Plex Sans Condensed', w; width = tw(s, size, w)
    x0 = x - width / 2 if anchor == 'middle' else (x if anchor == 'start' else x - width)
    if track: TXT.append((x0, y - size * .74, x0 + width, y + size * .2, s))
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="{fam}" font-weight="{wt}" '
            f'font-size="{f(size)}" fill="{fill}">{esc(s)}</text>')

# ---------------------------------------------------------------- elementi
def panel(w, h, corners=(1, 1, 1, 1), inner=True):
    o = [P(rr(1.5, 1.5, w - 3, h - 3, 9, .5, 12), True, PARCH, BRASS, 1.8)]
    if inner: o.append(P(rr(5, 5, w - 10, h - 10, 6, .3, 12), True, 'none', BRASSL, 0.9))
    for on, (x, y) in zip(corners, ((8, 8), (w - 8, 8), (8, h - 8), (w - 8, h - 8))):
        if on: o.append(rivet(x, y, 2.3))
    return ''.join(o)

def box(x, y, w, h, fill=PAPER, stroke=BRASS, sw=1.8, r=6):
    return P(rr(x, y, w, h, r, .4, 12), True, fill, stroke, sw)

def pips(v, s):
    d = s * .25
    L = {1: [(0, 0)], 2: [(-d, -d), (d, d)], 3: [(-d, -d), (0, 0), (d, d)], 4: [(-d, -d), (d, -d), (-d, d), (d, d)],
         5: [(-d, -d), (d, -d), (0, 0), (-d, d), (d, d)], 6: [(-d, -d), (d, -d), (-d, 0), (d, 0), (-d, d), (d, d)]}
    return L[v]

def die(cx, cy, s, v, fill=PAPER, pip=INK, tilt=0, sw=1.8, onepip=RED):
    r = max(2.2, s * .26)
    face = rot(rr(cx - s / 2, cy - s / 2, s, s, s * .22, .25, 12), tilt, cx, cy)
    o = [P(face, True, fill, INK, sw)]
    pr = s * .085 if s > 20 else s * .09
    for dx, dy in pips(v, s):
        (x, y, _), = rot([(cx + dx, cy + dy, False)], tilt, cx, cy)
        o.append(disc(x, y, max(1.7, pr), onepip if (v == 1 and pip == INK) else pip, 'none', 0, .1))
    return G('dado', *o)

def tick(cx, cy, k, col=GREEN, sw=2.4):
    return P(wob(C((cx - k * .9, cy), (cx - k * .25, cy + k * .65), (cx + k, cy - k * .7)), .15, 20, closed=False), False, 'none', col, sw)

def cross(cx, cy, k, col=RED, sw=3.0, halo=True):
    a, b, c, d = (cx - k, cy - k), (cx + k, cy + k), (cx + k, cy - k), (cx - k, cy + k)
    o = []
    if halo:
        o += [line(a, b, PAPER, sw + 2.6, .1), line(c, d, PAPER, sw + 2.6, .1)]
    o += [line(a, b, col, sw, .15), line(c, d, col, sw, .15)]
    return ''.join(o)

def slash(cx, cy, k, col=RED, sw=3.0):
    a, b = (cx - k, cy - k), (cx + k, cy + k)
    return line(a, b, PAPER, sw + 2.6, .1) + line(a, b, col, sw, .15)

def arrow(pts, col=INK, sw=2.2, hl=7.5, hw=5.8, dash=None, fill=None, amp=.25):
    """Freccia ballerina: pts = punti (x, y) del corpo; la punta sta nell'ultimo punto."""
    pts = list(pts); (x1, y1), (x2, y2) = pts[-2], pts[-1]
    L = math.hypot(x2 - x1, y2 - y1) or 1; ux, uy = (x2 - x1) / L, (y2 - y1) / L
    pts[-1] = (x2 - ux * hl * .8, y2 - uy * hl * .8)
    body = wob(S(*pts), amp, 14, closed=False) if len(pts) == 2 else [(x, y, False) for x, y in pts]
    ex = ' stroke-dasharray="%s"' % dash if dash else ''
    head = C((x2, y2), (x2 - ux * hl + uy * hw, y2 - uy * hl - ux * hw), (x2 - ux * hl - uy * hw, y2 - uy * hl + ux * hw))
    return P(body, False, 'none', col, sw, ex) + P(wob(head, .1, 30), True, fill or col, col, 1.0)

def pawn(cx, by, h, col=BLUE):
    """pedina: base, corpo a cono, testa. by = linea di base, h = altezza totale."""
    w = h * .62
    body = [(cx - w / 2, by, True), (cx - w * .17, by - h * .55, False), (cx + w * .17, by - h * .55, False), (cx + w / 2, by, True)]
    o = [poly(body, fill=col, amp=.25, step=8),
         P(ell(cx, by - .5, w * .55, h * .1, .1, 12), True, col, INK, 1.6),
         disc(cx, by - h * .72, h * .19, col, INK, 1.8, .1),
         disc(cx - h * .06, by - h * .78, h * .04, PAPER, 'none', 0, .02)]
    return G('pedina', P(wob(body, .25, 8), True, col, INK, 1.8), *o[1:])

def icon(fn, cx, cy, size, seed=1):
    g.R.seed(seed)
    body = (fn if callable(fn) else getattr(g, fn))()
    body = re.sub(r'<g id="[^"]*">', '<g>', body, count=1)
    k = size / 64
    return f'<g transform="translate({f(cx - size / 2)} {f(cy - size / 2)}) scale({f(k)})">{body}</g>'

def heart(cx, cy, s, fill):
    k = s / 2
    pts = [(cx, cy + k * .95, True), (cx - k * .95, cy - k * .05, False), (cx - k * .75, cy - k * .7, False), (cx - k * .3, cy - k * .85, False),
           (cx, cy - k * .45, True), (cx + k * .3, cy - k * .85, False), (cx + k * .75, cy - k * .7, False), (cx + k * .95, cy - k * .05, False)]
    return P(wob(pts, .25, 10), True, fill, INK, 1.9)

def rotella(cx, cy, r, n, seed=3):
    g.R.seed(seed)
    o = [P(cog(cx, cy, r, 20, .09, .15), True, PARCH, INK, 1.6)]
    for k in range(7):
        a = math.radians(45 + 45 * k)
        o.append(disc(cx + (r * .72) * math.sin(a), cy - (r * .72) * math.cos(a), r * .06 + .3, INK, 'none', 0, .05))
    w, h = r * .95, r * .78
    o.append(P(rr(cx - w / 2, cy - r * .5 - h / 2 + r * .22, w, h, 2, .2, 10), True, PAPER, INK, 1.4))
    o.append(T(cx, cy - r * .5 + r * .22 + h * .34, str(n), max(9, r * .8), 700, INK, serif=False))
    o.append(disc(cx, cy + r * .28, r * .24, GOLDL, INK, 1.4, .1))
    return G('rotella', *o)

def dline(a, b, col=BRASS, sw=1.2): return line(a, b, col, sw, .15, extra=' stroke-dasharray="3 3"')

def ic_occhio():
    almond = [(5, 32, True), (18, 18, False), (32, 13, False), (46, 18, False), (59, 32, True), (46, 46, False), (32, 51, False), (18, 46, False)]
    o = [poly(almond, fill=PAPER, amp=.4, step=10), disc(32, 32, 12.5, BLUE, INK, 2.2, .2), disc(32, 32, 5.5, INK, 'none', 0, .1),
         disc(28.5, 28.5, 2.6, PAPER, 'none', 0, .05)]
    for x1, y1, x2, y2 in ((18, 11, 15, 5), (32, 8, 32, 1.5), (46, 11, 49, 5)):
        o.append(line((x1, y1), (x2, y2), INK, 2.5))
    return G('ic_occhio', *o)

def ic_bandiera():
    flag = [(24, 10, True), (36, 8, False), (48, 13, False), (57, 12, True), (50, 21, False), (57, 30, True), (46, 31, False), (35, 28, False), (24, 31, True)]
    o = [P(wob(S((9, 56), (24, 52), (42, 54), (54, 57), (38, 59), (20, 59)), .3, 12), True, GREEN, INK, 2.2),
         line((24, 8), (24, 54), INK, 3),
         poly(flag, fill=RED, amp=.3, step=12), disc(24, 7, 3.2, GOLDL, INK, 1.8, .1)]
    return G('ic_bandiera', *o)

def ic_elmo():
    helm = mv([(4, 58, True), (4, 40, False), (9, 29, False), (20, 24, False), (31, 29, False), (36, 40, False), (36, 58, True)], 12, -2)
    o = [poly(helm, fill=BLUE, amp=.5, step=10),
         poly(mv(C((4, 49), (36, 49), (36, 58), (4, 58)), 12, -2), fill=BRASSL, amp=.3, step=12),
         line((21, 36), (43, 36), INK, 2.5), line((32, 36), (32, 47), INK, 2.5)]
    o += [disc(x, 51.5, 1.4, INK, 'none', 0, .05) for x in (22, 32, 42)]
    o.append(P(wob(S((32, 22), (32, 15), (39, 10), (45, 12), (40, 17), (39, 24)), .3, 12), True, RED, INK, 2.2))
    return G('ic_elmo', *o)

def ic_spada():
    blade = [(29, 50, True), (29, 14, False), (32, 4, True), (35, 14, False), (35, 50, True)]
    o = [poly(blade, fill=PAPER, amp=.3, step=12), line((32, 12), (32, 46), GREYT, 1.2),
         poly(C((20, 50), (44, 50), (44, 56), (20, 56)), fill=GOLD, amp=.25, step=12),
         poly(C((29.5, 56), (34.5, 56), (34.5, 62), (29.5, 62)), fill=BROWN, amp=.2, step=12),
         disc(32, 62.5, 3.2, GOLD, INK, 2.0, .1)]
    return G('ic_spada', G('x', *o))

def ic_corazza():
    body = [(7, 14, True), (22, 8, True), (32, 22, False), (42, 8, True), (57, 14, True), (53, 29, True), (46, 35, False),
            (48, 56, True), (32, 61, False), (16, 56, True), (18, 35, False), (11, 29, True)]
    o = [poly(body, fill=BRASS, amp=.4, step=10), P(wob(sc(body, .78, 32, 38), .3, 10), True, 'none', BRASSL, 1.5),
         P(lozenge(32, 40, 12, 16), True, RED, INK, 2.0), line((18, 51), (46, 51), BRASSL, 2),
         disc(14, 17, 1.6, INK, 'none', 0, .05), disc(50, 17, 1.6, INK, 'none', 0, .05)]
    return G('ic_corazza', *o)

def ic_pollice():
    o = [poly(S((26, 6), (35, 4), (42, 8), (42, 30), (28, 30), (27, 14)), fill=GOLDL, amp=.3, step=12),
         P(rr(18, 28, 38, 30, 8, .3, 12), True, GOLDL, INK, 2.5),
         poly(C((29.5, 25), (40.5, 25), (40.5, 33), (29.5, 33)), fill=GOLDL, stroke='none', sw=0, amp=0.05, step=30),
         line((44, 38), (54, 38), INK, 2), line((44, 46), (54, 46), INK, 2),
         P(rr(3, 28, 14, 30, 3, .3, 12), True, GREEN, INK, 2.5)]
    return G('ic_pollice', *o)

# ---------------------------------------------------------------- pipeline
def vc(*args):
    r = subprocess.run(['vectorcraft-cli', *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'vectorcraft-cli {" ".join(args)}\n{r.stdout}\n{r.stderr}')
    return r.stdout

def check(name, w, h):
    bad = 0
    for i, a in enumerate(TXT):
        if a[0] < 2 or a[2] > w - 2 or a[1] < 2 or a[3] > h - 2:
            print(f'  ! {name}: fuori dal bordo: {a[4]!r} {tuple(round(v, 1) for v in a[:4])}'); bad += 1
        for b in TXT[i + 1:]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                print(f'  ! {name}: sovrapposti: {a[4]!r} / {b[4]!r}'); bad += 1
    return bad

def export(name, w, h, body):
    os.makedirs(os.path.join(HERE), exist_ok=True)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" viewBox="0 0 {w} {h}">{body}</svg>'
    src = os.path.join(TMP, name + '.svg'); open(src, 'w').write(svg)
    vcs = os.path.join(HERE, name + '.vectorcraft')
    vc('convert', src, vcs)
    dst = os.path.join(OUT, name + '.svg')
    vc('convert', vcs, dst, '--outline-text', '--decimals', '2')
    t = open(dst).read()
    t = re.sub(r'<svg ([^>]*?)width="([\d.]+)" height="([\d.]+)"', r'<svg \1width="\2pt" height="\3pt"', t, count=1)
    open(dst, 'w').write(t)
    vc('convert', dst, os.path.join(OUT, name + '.pdf'))
    vc('convert', dst, os.path.join(OUT, name + '.png'), '--ppi', '200')
    print(name, w, h, 'testi:', len(TXT), 'avvisi:', check(name, w, h))

def kit_num(n, cx, cy, size):
    g.R.seed(60 + n)
    svg = g.numero(n)
    inner = re.sub(r'^<svg[^>]*>|</svg>$', '', svg)
    inner = re.sub(r'<g id="[^"]*">', '<g>', inner, count=1).replace(' id="numero"', '')
    k = size / 40
    return f'<g transform="translate({f(cx - size / 2)} {f(cy - size / 2)}) scale({f(k)})">{inner}</g>'

def pill(x, y, w, h, text, size=9.5, wt=700, fill=GOLDL, stroke=BRASS, col=INK):
    return P(rr(x, y, w, h, h / 2, .2, 10), True, fill, stroke, 1.4) + T(x + w / 2, y + h / 2 + size * .34, text, size, wt, col)

def tag(x, y, w, h, text, notch=None, lead=None, size=9.5, fill=GOLDL):
    """Cartellino: rettangolo con (facoltativa) tacca verso l'alto in `notch` (x) e icona/spunta a sinistra."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if notch is not None:
        pts = [(x, y), (notch - 5, y), (notch, y - 5), (notch + 5, y), (x + w, y), (x + w, y + h), (x, y + h)]
    return P(wob(C(*pts), .25, 12), True, fill, BRASS, 1.5)

LQ, RQ = '«', '»'

# ================================================================ S7-perdita  515 x 220
def s7():
    g.R.seed(7); TXT.clear()
    W, H = 515, 220
    o = [panel(W, H)]
    X0, X1 = 14, 501
    cw = (X1 - X0) / 6
    o.append(box(X0, 8, X1 - X0, 76, PAPER, BRASS, 1.8, 7))
    for i in range(1, 6):
        o.append(line((X0 + cw * i, 14), (X0 + cw * i, 78), BRASSL, 1.2, .2, extra=' stroke-dasharray="3 3"'))
    labels = ['Tutto!', 'Elmo', 'Arma DX o Scudo', 'Arma SX', 'Armatura', 'Niente!']
    for i in range(6):
        cx = X0 + cw * (i + .5)
        yes = (i == 5)
        o.append(die(cx, 19, 18, i + 1, GREEN if yes else PAPER, PAPER if yes else INK, 0, 1.5))
        iy = 46
        if i == 0:
            for k, (fn, dx, dy) in enumerate((('ic_elmo', -9, -9), ('ic_spada', 9, -9), ('ic_ar', -9, 9), ('ic_corazza', 9, 9))):
                fnc = fn if fn == 'ic_ar' else globals()[fn]
                o.append(icon(fnc, cx + dx, iy + dy, 17, 40 + k))
            o.append(cross(cx, iy, 15, RED, 2.6, False))
        elif i == 1:
            o.append(icon(ic_elmo, cx, iy, 32, 41)); o.append(slash(cx, iy, 13))
        elif i == 2:
            o.append(icon(ic_spada, cx - 11, iy, 26, 42)); o.append(icon('ic_ar', cx + 10, iy, 24, 43)); o.append(slash(cx, iy, 14))
        elif i == 3:
            o.append(icon(ic_spada, cx, iy, 32, 44)); o.append(slash(cx, iy, 13))
        elif i == 4:
            o.append(icon(ic_corazza, cx, iy, 32, 45)); o.append(slash(cx, iy, 13))
        else:
            o.append(icon(ic_pollice, cx, iy, 32, 46))
        o.append(T(cx, 78, labels[i], 10, 700, GREEN if yes else INK))
    o.append(T(W / 2, 95, f'Slot vuoto? Non perdi niente. · Ogni {LQ}perdi l\'equipaggiamento{RQ} usa questo D6', 9.5, 400, BROWN))
    # i 5 passi (R 11.4; D31: -1 Indizio)
    bw, bh, by = 84, 74, 100
    pitch = (X1 - X0 - bw) / 4
    steps = ['Danni = PV', 'Partenza iniziale', 'Perdi 1 Indizio', 'Danni a 0', ('Ristoro', 'D6 + 1 carta')]   # D32: il D6 e la carta sono il Ristoro, a fine turno
    for i, st in enumerate(steps):
        x = X0 + pitch * i; cx = x + bw / 2; cy = by + 19
        o.append(box(x, by, bw, bh, PAPER, BRASS, 1.8, 7))
        if i == 0:
            o.append(heart(cx, cy, 29, PAPER))
        elif i == 1:
            hx = [(cx + 16 * math.cos(math.radians(a)), cy + 16 * math.sin(math.radians(a)), True) for a in (-90, -30, 30, 90, 150, 210)]
            o.append(poly(hx, fill=SAND, amp=.4, step=12)); o.append(P(wob(sc(hx, .82, cx, cy), .2, 12), True, 'none', BRASS, 1.2))
            o.append(pawn(cx - 4, cy + 6, 18, BLUE)); o.append(T(cx + 8, cy + 8, '1', 11, 700, INK, serif=True))
        elif i == 2:
            o.append(icon('ic_indizio', cx - 9, cy, 30, 49)); o.append(T(cx + 17, cy + 5, '−1', 13, 700, RED, serif=True))
        elif i == 3:
            o.append(heart(cx, cy, 29, RED))
        else:
            o.append(die(cx - 17, cy, 24, 3, PAPER, INK, 8, 1.8))
            o.append(icon('ic_carta', cx + 16, cy, 30, 47))
        small = {1: ('occupata? Esagono', 'libero accanto'), 2: (f'all\'eroe che ti batte,', 'se no nella riserva')}
        if i in small:
            o.append(T(cx, by + 44, st, 10.5, 700))
            o.append(T(cx, by + 55, small[i][0], 9.5, 400, BROWN)); o.append(T(cx, by + 65, small[i][1], 9.5, 400, BROWN))
        elif isinstance(st, tuple):
            o.append(T(cx, by + 49, st[0], 10.5, 700)); o.append(T(cx, by + 61, st[1], 10.5, 700))
        else:
            o.append(T(cx, by + 55, st, 10.5, 700))
        if i < 4:
            o.append(arrow([(x + bw + 2, cy), (x + pitch - 2, cy)], BROWN, 2.6, 6, 5, fill=COPPER))
    # cartellini: Cripta sotto il passo dell'Indizio, «Tieni» sotto l'ultimo, poi la Fine
    tr = X1 - 6; ya = by + bh + 5; yb = ya + 17
    ta, tb = 'Tieni mano e Stati', 'Era il tuo turno? Vai alla Fine'
    tc = 'Nessuno ha più 3 Indizi? La Cripta esce con MIMI; il custode torna nel mazzetto 3'
    td = 'Al prossimo 3° Indizio: nuovo tiro e nuovo custode'
    wa = tw(ta, 9.5, 700) + 34; wb = tw(tb, 9.5, 700) + 34; wc = tw(tc, 9.5, 700) + 34
    o.append(tag(tr - wa, ya, wa, 14, ta, notch=X0 + pitch * 4 + bw / 2))
    o.append(disc(tr - wa + 10, ya + 7, 5.3, PAPER, GREEN, 1.3, .1)); o.append(tick(tr - wa + 10, ya + 7.2, 3, GREEN, 1.9))
    o.append(T(tr - wa + 19, ya + 10.6, ta, 9.5, 700, INK, 'start'))
    xc1 = tr - wa - 8; xc0 = xc1 - wc
    assert xc0 >= X0 + 6, 'cartellino della Cripta troppo largo'
    o.append(tag(xc0, ya, wc, 14, tc, notch=X0 + pitch * 2 + bw / 2))
    o.append(icon('ic_tesoro', xc0 + 10, ya + 7, 14, 50))
    o.append(T(xc0 + 19, ya + 10.6, tc, 9.5, 700, INK, 'start'))
    wd = tw(td, 9.5, 700) + 34
    assert xc0 + wd <= tr - wb - 8, 'secondo cartellino della Cripta troppo largo'
    o.append(tag(xc0, yb, wd, 14, td))
    o.append(icon('ic_tesoro', xc0 + 10, yb + 7, 14, 51))
    o.append(T(xc0 + 19, yb + 10.6, td, 9.5, 700, INK, 'start'))
    o.append(tag(tr - wb, yb, wb, 14, tb))
    o.append(icon(ic_bandiera, tr - wb + 10, yb + 7, 15, 48))
    o.append(T(tr - wb + 19, yb + 10.6, tb, 9.5, 700, INK, 'start'))
    export('S7-perdita', W, H, ''.join(o))

# ================================================================ S5-indizio  250 x 195
def s5():
    g.R.seed(5); TXT.clear()
    W, H = 250, 195
    o = [panel(W, H, inner=False)]
    o.append(T(125, 17, 'Hai vinto lo scontro?', 11, serif=True))
    o.append(T(125, 31, 'Indizio se il D6 è pari o meno di LV + 1', 9.5, 700))
    cx, cy = 27, 56
    card = rot(rr(cx - 13, cy - 18, 26, 36, 3.5, .3, 10), -9, cx, cy)
    o.append(P(card, True, PAPER, INK, 1.7))
    o.append(P(rot(rr(cx - 10, cy - 15, 20, 30, 2, .2, 10), -9, cx, cy), True, 'none', BRASS, 0.9))
    o.append(f'<g transform="rotate(-9 {cx} {cy})">' + icon('ic_mostro', cx, cy - 7, 18, 7) + '</g>')
    (bx, by, _), = rot([(cx, cy + 10, False)], -9, cx, cy)
    o.append(disc(bx, by, 11, GOLDL, INK, 1.6, .2)); o.append(T(bx, by + 3.3, 'LV 3', 9.5, 700, INK, serif=True))
    xs = [68 + 30 * i for i in range(6)]; dy = 47; s = 21
    for i, x in enumerate(xs):
        v = i + 1
        if v <= 4:
            o.append(die(x, dy, s, v, GREEN, PAPER, 0, 1.6))
            o.append(disc(x, dy + 11, 4.7, PAPER, GREEN, 1.3, .1)); o.append(tick(x, dy + 11.2, 2.5, GREEN, 1.7))
        else:
            o.append(die(x, dy, s, v, GREY, INK, 0, 1.6))
    def bracket(xa, xb, col):
        y = dy + 18
        return P(C((xa, y), (xa, y + 4), (xb, y + 4), (xb, y)), False, 'none', col, 1.6)
    o.append(bracket(xs[0] - 12, xs[3] + 12, GREEN)); o.append(bracket(xs[4] - 12, xs[5] + 12, GREYT))
    gx = (xs[0] + xs[3]) / 2; ty = dy + 35
    wl = tw('Indizio!', 10, 700); x0 = gx - (17 + 4 + wl) / 2
    o.append(icon('ic_segnalino', x0 + 8.5, ty, 19, 9))
    o.append(T(x0 + 21, ty + 3.6, 'Indizio!', 10, 700, GREEN, 'start'))
    o.append(T((xs[4] + xs[5]) / 2, ty + 3.6, 'Niente', 10, 700, GREYT))
    o.append(T(125, 101, 'LV 1: 1–2 · LV 2: 1–3 · LV 3: 1–4 · LV 4: 1–5 · LV 5: sempre', 9, 400))
    o.append(dline((14, 107), (236, 107)))
    # il bottino (D32: si prende al Ristoro): 3 carte del mazzo comune, ne tieni 1, le altre 2 coperte in fondo
    o.append(T(125, 120, 'Mazzetto 1 o 2: bottino al Ristoro!', 10, 700, BROWN))
    for k in (2, 1, 0):
        o.append(box(13 + k * 1.4, 124 - k * 1.4, 17, 24, GOLDL if k == 0 else PAPER, INK, 1.3, 2.5))
    o.append(P(wob(star4(21.5, 136, 4.5, .45), .05, 20), True, BRASS, 'none', 0))
    o.append(arrow([(35, 136), (47, 136)], BROWN, 2.2, 6, 4.5, fill=COPPER))
    for k, x in enumerate((58, 76, 94)):
        keep = (k == 0)
        y = 121 if keep else 126
        o.append(box(x - 7.5, y, 15, 21, PAPER if keep else GREY, GREEN if keep else INK, 1.8 if keep else 1.3, 2.5))
        if keep:
            o.append(tick(x, y + 10.5, 4, GREEN, 2.2))
    o.append(T(85, 156, 'in fondo', 9, 400, GREYT))
    lines = ['Prendi le prime 3 carte', 'del mazzo comune: tienine 1,', 'le altre 2 coperte in fondo.']
    for k, t in enumerate(lines):
        o.append(T(110, 131 + 11 * k, t, 9, 400, INK, 'start'))
    prem = ['Mazzetto 3: niente bottino', 'Ristoro: D6 della perdita sempre, anche se vinci', 'Non vinto (sconfitta, fuga): pesca 1 carta']
    for k, t in enumerate(prem):
        yy = 167 + 11 * k
        if k == 0: o.append(cross(14, yy - 3, 2.8, RED, 1.6, False))
        elif k == 1: o.append(die(14, yy - 3.2, 9, 5, PAPER, INK, 0, 1.0))
        else: o.append(P(rot(rr(10.5, yy - 6, 7, 6, 1, .05, 10), -8, 14, yy - 3), True, BLUE, INK, 1.0))
        o.append(T(24, yy, t, 9, 400, INK, 'start'))
    export('S5-indizio', W, H, ''.join(o))

# ================================================================ S2-turno  250 x 195
def s2():
    g.R.seed(2); TXT.clear()
    W, H = 250, 195
    o = [panel(W, H, (1, 1, 0, 0))]
    o.append(T(125, 15, 'Carte e risposte: in ogni momento', 9, 400, BROWN))
    rm, cy = 26, 47
    cs = [42, 125, 208]
    seq = [('ic_movimento', '1 · Muovi', 'D6 + MOV'), (ic_occhio, '2 · Esplora', 'Dove ti fermi'), (ic_bandiera, '3 · Fine', None)]
    ar = lambda pts: arrow(pts, BROWN, 3.0, 9, 7, fill=COPPER)
    o.append(ar([(72, cy), (95, cy)])); o.append(ar([(155, cy), (178, cy)]))
    for i, (x, (ic, l1, l2)) in enumerate(zip(cs, seq)):
        g.R.seed(21 + i)
        o.append(P(cog(x, cy, rm, 22, .06, .12), True, BRASS, INK, 2.0))
        o.append(disc(x, cy, rm - 3, BRASSL, 'none', 0, .1))
        o.append(P(ell(x, cy, rm - 3, amp=.1, n=22), True, 'none', GOLD, 1.0))
        o.append(icon(ic, x, cy, 30, 31 + i))
        o.append(T(x, cy + rm + 14, l1, 10, 700))
        if l2:
            o.append(T(x, cy + rm + 26, l2, 9.5, 400))
    # i passi della Fine + pedina
    o.append(box(12, 104, 226, 82, PAPER, BRASS, 1.6, 6))
    px = 210
    o.append(arrow([(px, 92), (px, 117)], BROWN, 3.0, 8, 6.5, fill=COPPER))
    o.append(pawn(px, 146, 24, BLUE))
    o.append(T(px, 158, 'Tocca a', 9.5, 700)); o.append(T(px, 168, 'sinistra', 9.5, 700))
    items = ['Ultime carte', 'Ristoro se hai combattuto', f'Finiscono gli effetti {LQ}in questo turno{RQ}', ('Togli i tuoi Stati verticali,', 'poi gira in verticale gli orizzontali'),
             'Carte giocate negli scarti', 'Rifornisci le tessere']
    yy = 114
    for t in items:
        o.append(disc(20, yy - 3, 2.3, COPPER, INK, .8, .05))
        for part in (t if isinstance(t, tuple) else (t,)):
            o.append(T(27, yy, part, 9.5, 400, INK, 'start')); yy += 10.8
    export('S2-turno', W, H, ''.join(o))

# ================================================================ S4-scontro  515 x 170
def s4():
    g.R.seed(4); TXT.clear()
    W, H = 515, 170
    o = [panel(W, H, (1, 0, 1, 1), inner=False)]
    Ay, Ah, By, Bh = 17, 56, 83, 48
    wa = [184, 168, 135]; ga = (W - 12 - sum(wa)) / 2
    xa_ = [6, 6 + wa[0] + ga, 6 + wa[0] + wa[1] + 2 * ga]
    wbl = [130, 187, 170]; gb = (W - 12 - sum(wbl)) / 2
    xb_ = [6, 6 + wbl[0] + gb, 6 + wbl[0] + wbl[1] + 2 * gb]
    for i in range(3): o.append(box(xa_[i], Ay, wa[i], Ah, PAPER, BRASS, 1.7, 6))
    o.append(box(xb_[0], By, wbl[0], Bh, GOLDL, BRASS, 1.5, 6))
    for i in (1, 2): o.append(box(xb_[i], By, wbl[i], Bh, PAPER, BRASS, 1.7, 6))
    ar = lambda pts: arrow(pts, BROWN, 2.4, 6.5, 5.2, fill=COPPER)
    for i in range(2): o.append(ar([(xa_[i] + wa[i] - 1, Ay + 28), (xa_[i + 1] + 1, Ay + 28)]))
    # 0 quale mostro
    x = xa_[0]; y = Ay
    o.append(T(x + 24, y + 14, 'Quale mostro?', 10, 700, INK, 'start'))
    for k, t in enumerate(('PL 0–3 → mazzetto 1', 'PL 4–7 → mazzetto 2', 'PL 8+ → mazzetto 3')):
        o.append(pill(x + 6, y + 19 + 12 * k, 94, 11.5, t, 9, 700))
    for k, t in enumerate(('Gira la prima carta ·', 'Rotella dello scontro', 'sui suoi PV ·', 'leggi la sua abilità')):
        o.append(T(x + 105, y + 22 + 10 * k, t, 9, 400, INK, 'start'))
    # 1 chi attacca per primo
    x = xa_[1]; w = wa[1]
    o.append(T(x + 24, y + 13, 'Chi attacca per primo?', 10, 700, INK, 'start'))
    o.append(pawn(x + 18, y + 33, 16, BLUE)); o.append(die(x + 18, y + 44, 15, 5, PAPER, INK, -4, 1.5))
    o.append(icon('ic_mostro', x + 50, y + 26, 17, 11)); o.append(die(x + 50, y + 44, 15, 2, PAPER, INK, 4, 1.5))
    for k, (t, wt, col) in enumerate((('5 contro 2:', 700, INK), ("comincia l'eroe", 700, INK), ("Pari: vince l'eroe ·", 400, BROWN), ('col custode, il custode', 400, BROWN))):
        o.append(T(x + 79, y + 23.5 + 9 * k, t, 9.5 if wt == 700 else 9, wt, col, 'start'))
    # 2 per colpire
    x = xa_[2]; w = wa[2]
    o.append(T(x + 22, y + 13, 'Per colpire: 2D6 + ATT ≥ AR', 9, 700, INK, 'start'))
    o.append(die(x + 14, y + 29, 16, 4, PAPER, INK, -4, 1.5)); o.append(die(x + 33, y + 29, 16, 2, PAPER, INK, 4, 1.5))
    o.append(T(x + 45, y + 33, '+ ATT 3 = 9', 10, 700, INK, 'start'))
    o.append(P(rr(x + w - 28, y + 16, 20, 25, 3, .2, 10), True, PAPER, INK, 1.5))
    o.append(icon('ic_mostro', x + w - 18, y + 23, 14, 12))
    o.append(disc(x + w - 17, y + 32, 9, GOLDL, INK, 1.4, .12)); o.append(T(x + w - 17, y + 35.2, 'AR 6', 9, 700))
    o.append(T(x + 6, y + 52, '9 ≥ 6: colpito!', 10, 700, GREEN, 'start'))
    o.append(T(x + w - 4, y + 53, 'AR: sulla carta', 9, 400, BROWN, 'end'))
    # fila B: danno del mostro | 3 danno | 4 ora attacca
    x = xb_[0]; y = By
    o.append(T(x + 6, y + 11, 'Danno del mostro:', 9.5, 700, INK, 'start'))
    o.append(pill(x + 6, y + 15, 118, 12, 'LV 1 → D6 − 1 (minimo 1)', 9, 700))
    o.append(pill(x + 6, y + 30, 50, 12, 'LV 2 → D6', 9, 700)); o.append(pill(x + 60, y + 30, 64, 12, 'LV 3+ → D6 + 1', 9, 700))
    x = xb_[1]; w = wbl[1]
    o.append(T(x + 24, y + 10, 'Danno (solo se colpisci):', 9, 700, INK, 'start')); o.append(T(x + 24, y + 20, 'D6 + (+N) Danni delle carte', 9, 700, INK, 'start'))
    o.append(die(x + 15, y + 35, 16, 2, PAPER, INK, -4, 1.5))
    o.append(rotella(x + 46, y + 35, 11, 3, 13)); o.append(rotella(x + 82, y + 35, 11, 1, 14))
    o.append(arrow([(x + 59, y + 35), (x + 69, y + 35)], COPPER, 2.2, 6, 4.8, fill=COPPER))
    o.append(T(x + 98, y + 38.5, 'PV del mostro: 3 → 1', 9.5, 700, INK, 'start'))
    x = xb_[2]; w = wbl[2]
    o.append(T(x + 24, y + 11.5, 'Ora attacca il mostro', 10, 700, INK, 'start'))
    o.append(icon('ic_mostro', x + 140, y + 11, 18, 15))
    for k, t in enumerate(('A turno, fino alla sconfitta.', 'Dopo 3 attacchi tuoi il mostro', 'scappa (il custode no)')):
        o.append(T(x + 8, y + 25.5 + 9.3 * k, t, 9.5, 400 if k else 700, INK, 'start'))
    # frecce tra i riquadri
    o.append(arrow([(xa_[2] + 20, Ay + Ah - 1), (xa_[2] + 14, Ay + Ah + 6), (xb_[1] + wbl[1] - 12, Ay + Ah + 6), (xb_[1] + wbl[1] - 8, By + 1.5)],
                   BROWN, 2.4, 6.5, 5.2, fill=COPPER))
    o.append(arrow([(xb_[1] + wbl[1] - 1, By + 38), (xb_[2] + 2, By + 38)], BROWN, 2.4, 6, 5, fill=COPPER))
    xr = xb_[2] + 156
    o.append(arrow([(xr, By + 1), (xr, Ay + Ah - 1)], COPPER, 2.6, 6.5, 5.2, fill=COPPER))
    for i in range(3): o.append(kit_num(i, xa_[i] + 11, Ay + 11, 20))
    o.append(kit_num(3, xb_[1] + 11, By + 11, 20)); o.append(kit_num(4, xb_[2] + 11, By + 11, 20))
    # banner
    bn = 'Per il mostro tira chi ti siede a destra'
    bw_ = tw(bn, 9.5, 700) + 14
    o.append(tag(W - 6 - bw_, 2.5, bw_, 12, bn)); o.append(T(W - 6 - bw_ / 2, 11.6, bn, 9.5, 700))
    # due righe finali
    ry = By + Bh + 4
    def row(items, lead=None, icon_fn=None, size=9):
        nonlocal ry
        parts = []
        if icon_fn: parts.append(('i', 14))
        for it in items: parts.append(('p', tw(it[0], size, it[1]) + 12))
        total = sum(p[1] for p in parts) + 4 * (len(parts) - 1)
        x_ = (W - total) / 2; k = 0
        for kind, wd in parts:
            if kind == 'i': o.append(icon(icon_fn, x_ + 7, ry + 7, 15, 60))
            else:
                it = items[k]; k += 1
                o.append(pill(x_, ry, wd, 13.5, it[0], size, it[1], it[2], it[3]))
            x_ += wd + 4
        ry += 16
    row([('Vantaggio: tira due volte i 2D6, tieni il migliore', 400, PAPER, GREEN), ('Svantaggio: il peggiore', 400, PAPER, RED),
         ('Tutti e due: si annullano', 400, PAPER, BRASS)])
    row([('Fuga: prima di ogni tuo attacco torni dove eri a inizio turno, senza premi, e vai alla Fine', 400, PAPER, BRASS),
         ('Mai dal custode di MIMI', 700, PAPER, RED)], None, 'ic_movimento')
    export('S4-scontro', W, H, ''.join(o))

BUILD = {'S2-turno': s2, 'S4-scontro': s4, 'S5-indizio': s5, 'S7-perdita': s7}
if __name__ == '__main__':
    for n in (_argv or BUILD):
        BUILD[n]()
    print('tmp:', TMP)
