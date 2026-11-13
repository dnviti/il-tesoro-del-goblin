#!/usr/bin/env python3
"""Schemi complessi del regolamento «Il Tesoro del Goblin»: S1-tavolo, S3-mappa, S6-catena.

Genera gli SVG di partenza (linea «ballerina» del kit vettoriale, helper presi da
vettoriali/sorgenti/genera_vettoriali.py), poi con vectorcraft-cli:
  SVG -> sorgenti/<id>.vectorcraft (testo ancora modificabile)
      -> <id>.svg (testo in tracciati, unita' in pt) -> <id>.pdf + <id>.png (200 ppi).

Uso:  python3 genera_schemi_complessi.py S3 [S1 S6 ...]
"""
import math, os, re, subprocess, sys, tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))          # .../manuale/schemi/sorgenti
OUT = os.path.dirname(HERE)                                  # .../manuale/schemi
KIT = os.path.join(os.path.dirname(OUT), 'vettoriali', 'sorgenti')
_argv = sys.argv
TMP = tempfile.mkdtemp(prefix='schemi_')
sys.argv = [_argv[0], TMP]
sys.path.insert(0, KIT)
import genera_vettoriali as gv                               # noqa: E402
sys.argv = _argv
from genera_vettoriali import (INK, BROWN, RED, BLUE, GOLD, GOLDL, BRASS, BRASSL, COPPER, PAPER, PARCH,
                               GREEN, VIOLET, C, S, f, P, poly, line, disc, ell, rr, wob, arcpts, G)
from PIL import ImageFont                                    # noqa: E402

R = gv.R
J = gv.J
SANS = 'IBM Plex Sans Condensed'

# ---------------------------------------------------------------- testo
_fonts = {}
_W = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'}
def tw(s, size=9.5, weight=500):
    k = weight
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(f'/usr/share/fonts/ibm-plex-sans-fonts/IBMPlexSansCondensed-{_W[k]}.otf', 100)
    return _fonts[k].getlength(s) * size / 100

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')

def T(x, y, s, size=9.5, weight=500, anchor='middle', fill=INK, rot=None, serif=False):
    fam = 'Noto Serif' if serif else SANS
    tr = f' transform="rotate({f(rot)} {f(x)} {f(y)})"' if rot else ''
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="{fam}" font-weight="{weight}" '
            f'font-size="{f(size)}" fill="{fill}"{tr}>{esc(s)}</text>')

def TL(x, y, lines, size=9.5, lh=None, **k):
    lh = lh or size * 1.12
    return ''.join(T(x, y + i * lh, s, size, **k) for i, s in enumerate(lines))

def tag(cx, cy, s, size=9.5, weight=500, pad=4.5, fill=PAPER, stroke=BRASS, col=INK, h=None, sw=1):
    w = tw(s, size, weight) + 2 * pad
    h = h or size + 5
    box = P(gv.rr(cx - w / 2, cy - h / 2, w, h, h / 2.6, .2, 14), True, fill, stroke, sw)
    return box + T(cx, cy + size * .34, s, size, weight, fill=col)

# ---------------------------------------------------------------- pezzi riusabili
def strip_svg(s): return re.sub(r'^<svg[^>]*>|</svg>$', '', s.strip())

def numgear(n, cx, cy, d=22):
    inner = strip_svg(gv.numero(n))
    k = d / 40
    return f'<g transform="translate({f(cx - d / 2)} {f(cy - d / 2)}) scale({f(k)})">{inner}</g>'

def icon(name, cx, cy, d):
    R.seed(7)
    body = getattr(gv, name)()
    k = d / 64
    return f'<g transform="translate({f(cx - d / 2)} {f(cy - d / 2)}) scale({f(k)})">{body}</g>'

def die(cx, cy, s, n, rot=0, fill=PAPER, pip=INK):
    pos = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    pts = rr(cx - s / 2, cy - s / 2, s, s, s * .2, .25, 12)
    d = P(pts, True, fill, INK, 1.6)
    k = s * .27
    pips = ''.join(P(ell(cx + a * k, cy + b * k, s * .075, amp=.05, n=8), True, pip, 'none') for a, b in pos)
    g = d + pips
    if rot: return f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">{g}</g>'
    return g

def xmark(cx, cy, s, sw=3.2, col=RED):
    a = [(cx - s, cy - s), (cx + s, cy + s)]; b = [(cx + s, cy - s), (cx - s, cy + s)]
    o = ''
    for w_, c_ in ((sw + 2.6, PAPER), (sw, col)):
        for p, q in (a, b):
            o += f'<path d="M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}" stroke="{c_}" stroke-width="{f(w_)}" stroke-linecap="round" fill="none"/>'
    return o

def tick(cx, cy, s, col=GREEN, sw=3):
    pts = [(cx - s, cy), (cx - s * .3, cy + s * .75), (cx + s, cy - s * .8)]
    d = f'M{f(pts[0][0])} {f(pts[0][1])}L{f(pts[1][0])} {f(pts[1][1])}L{f(pts[2][0])} {f(pts[2][1])}'
    return (f'<path d="{d}" stroke="{PAPER}" stroke-width="{f(sw + 2.4)}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

def pawn(cx, by, h, col, shadow=True):
    o = ''
    if shadow:
        o += P(ell(cx, by, h * .4, h * .1, amp=.1, n=10), True, INK, 'none', extra=' fill-opacity=".22"')
    body = [(cx - .36 * h, by, True), (cx - .27 * h, by - .16 * h, False), (cx - .11 * h, by - .5 * h, False),
            (cx + .11 * h, by - .5 * h, False), (cx + .27 * h, by - .16 * h, False), (cx + .36 * h, by, True)]
    o += P(wob(body, .2, 14), True, col, INK, 1.5)
    o += P(ell(cx, by - .66 * h, .2 * h, amp=.15, n=12), True, col, INK, 1.5)
    o += P(ell(cx - .06 * h, by - .71 * h, .05 * h, amp=0, n=6), True, PAPER, 'none', extra=' fill-opacity=".7"')
    return o

def arrow(pts, col=BLUE, band=5.2, inner=2.4, head=9, hw=5.6, dash=None, amp=.35):
    """freccia a spezzata: contorno inchiostro + anima colorata + punta."""
    ex, ey = pts[-1]; px, py = pts[-2]
    L = math.hypot(ex - px, ey - py); ux, uy = (ex - px) / L, (ey - py) / L
    bx, by = ex - ux * head, ey - uy * head
    path = list(pts[:-1]) + [(bx + ux * 1.2, by + uy * 1.2)]
    wp = wob(C(*path), amp, 14, closed=False)
    if dash:
        o = P(wp, False, 'none', INK, inner, extra=f' stroke-dasharray="{dash}"')
        hc = INK
    else:
        o = P(wp, False, 'none', INK, band) + P(wp, False, 'none', col, inner)
        hc = col
    tri = [(ex, ey), (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)]
    o += P(wob(C(*tri), .1, 20), True, hc, INK, 1.8)
    return o

def leader(a, b, dot=True):
    o = P(wob(C(a, b), .25, 12, closed=False), False, 'none', INK, .9, extra=' stroke-dasharray="1.8 2.6"')
    if dot: o += P(ell(b[0], b[1], 2.1, amp=0, n=8), True, INK, 'none')
    return o

def hexv(cx, cy, r):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)), True) for a in (-90, -30, 30, 90, 150, 210)]

def panel(w, h, body, rivets=True):
    bg = P(rr(.8, .8, w - 1.6, h - 1.6, 9, .25, 14), True, PARCH, BRASS, 1.5)
    rv = ''.join(gv.rivet(x, y, 2) for x, y in ((7.5, 7.5), (w - 7.5, 7.5), (7.5, h - 7.5), (w - 7.5, h - 7.5))) if rivets else ''
    return bg + rv + body

# ---------------------------------------------------------------- pipeline VectorCraft
def vc(*args):
    r = subprocess.run(['vectorcraft-cli', *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'vectorcraft-cli {" ".join(args)}\n{r.stdout}\n{r.stderr}')
    return r.stdout

def emit(name, w, h, svg_body):
    os.makedirs(os.path.join(OUT, 'sorgenti'), exist_ok=True)
    src = os.path.join(TMP, name + '.svg')
    open(src, 'w').write(gv.svg_doc(w, h, G(name, svg_body)))
    vcs = os.path.join(OUT, 'sorgenti', name + '.vectorcraft')
    vc('convert', src, vcs)
    dst = os.path.join(OUT, name + '.svg')
    vc('convert', vcs, dst, '--outline-text', '--decimals', '2')
    t = open(dst).read()
    t = re.sub(r'<svg ([^>]*?)width="([\d.]+)" height="([\d.]+)"', r'<svg \1width="\2pt" height="\3pt"', t, count=1)
    open(dst, 'w').write(t)
    vc('convert', dst, os.path.join(OUT, name + '.pdf'))
    vc('convert', dst, os.path.join(OUT, name + '.png'), '--ppi', '200')
    print(name, w, h)

# ================================================================ S3 · mappa
def s3():
    R.seed(303)
    W, H = 515, 235
    r = 30; w = math.sqrt(3) * r; x0 = 116; y0 = 52
    def ctr(row, col):
        return (x0 + w / 2 + col * w + (w / 2 if row == 1 else 0), y0 + r + row * 1.5 * r)
    grid = [[('Partenza 1', 'start'), ('Prato', 'prato'), ('Bosco', 'wood'), ('Rocce', 'rock'), ('Prato', 'prato')],
            [('Mattonato', 'matt'), ('Acqua', 'water'), ('Prato', 'prato'), ('Prato', 'red'), ('Ponte', 'bridge')],
            [('Case', 'house'), ('Prato', 'prato'), ('Prato', 'covered'), ('Mattonato', 'matt'), ('Acqua', 'water')]]
    FILL = {'start': '#e8cf9a', 'prato': '#c7df8c', 'matt': '#e8cf9a', 'wood': '#3f6f3a', 'rock': '#bdb6ab', 'water': '#a6d0e2',
            'bridge': '#a6d0e2', 'house': '#dcb08f', 'red': '#c7df8c', 'covered': '#c7df8c'}
    hexes = []; glyphs = []; labels = []
    for ri, row in enumerate(grid):
        for ci, (lab, kind) in enumerate(row):
            cx, cy = ctr(ri, ci)
            obst = kind in ('wood', 'rock', 'house')
            hexes.append(poly(hexv(cx, cy, r), fill=FILL[kind], stroke=INK, sw=1.6, amp=.35, step=15))
            if obst:
                hexes.append(P(wob(hexv(cx, cy, r - 3.2), .2, 15), True, 'none', '#2a2118' if kind == 'wood' else '#6b6358', 1.3, extra=' stroke-opacity=".55"'))
            gy = cy - 4
            if kind == 'wood':
                for dx, dy, s in ((-11, 3, 1), (11, 2, 1.05), (0, -8, 1.15)):
                    glyphs.append(P(wob(C((cx + dx - 1.8, gy + dy + 5), (cx + dx + 1.8, gy + dy + 5), (cx + dx + 1.8, gy + dy + 11), (cx + dx - 1.8, gy + dy + 11)), .1, 9), True, BROWN, INK, 1))
                    glyphs.append(P(ell(cx + dx, gy + dy - 1, 8.5 * s, 9 * s, amp=.3, n=12), True, '#25512a', INK, 1.3))
                    glyphs.append(P(ell(cx + dx - 2.5, gy + dy - 3.5, 2.6 * s, amp=0, n=6), True, '#6fa05a', 'none'))
            elif kind == 'rock':
                glyphs.append(P(wob(C((cx - 17, gy + 11), (cx - 14, gy - 2), (cx - 4, gy - 7), (cx + 2, gy + 2), (cx + 4, gy + 11)), .3, 9), True, '#8f8a82', INK, 1.4))
                glyphs.append(P(wob(C((cx - 2, gy + 11), (cx + 3, gy - 4), (cx + 11, gy - 6), (cx + 17, gy + 3), (cx + 17, gy + 11)), .3, 9), True, '#a39d94', INK, 1.4))
            elif kind in ('water', 'bridge'):
                for k, dy in enumerate((-1, 7) if kind == 'water' else (-17, 13)):
                    pts = [(cx - 17 + i * 4.25, cy + dy + (-2.4 if i % 2 else 2.4), False) for i in range(9)]
                    glyphs.append(P(pts, False, 'none', BLUE, 1.7))
                if kind == 'bridge':
                    for k in range(5):
                        px = cx - 18 + k * 9
                        glyphs.append(P(wob(C((px, cy - 14), (px + 7, cy - 14), (px + 7, cy + 5), (px, cy + 5)), .1, 9), True, '#c79a5a', INK, 1.1))
                    glyphs.append(P(wob(C((cx - 21, cy - 15), (cx + 21, cy - 15)), .1, 12, closed=False), False, 'none', BROWN, 1.6))
                    glyphs.append(P(wob(C((cx - 21, cy + 6), (cx + 21, cy + 6)), .1, 12, closed=False), False, 'none', BROWN, 1.6))
            elif kind == 'house':
                for dx, dy, s in ((-8, 4, .9), (9, 2, 1)):
                    glyphs.append(P(wob(C((cx + dx - 8 * s, gy + dy + 9 * s), (cx + dx + 8 * s, gy + dy + 9 * s), (cx + dx + 8 * s, gy + dy), (cx + dx - 8 * s, gy + dy)), .12, 9), True, PAPER, INK, 1.3))
                    glyphs.append(P(wob(C((cx + dx - 11 * s, gy + dy), (cx + dx, gy + dy - 11 * s), (cx + dx + 11 * s, gy + dy)), .12, 9), True, RED, INK, 1.3))
                    glyphs.append(P(wob(C((cx + dx - 2 * s, gy + dy + 9 * s), (cx + dx + 2 * s, gy + dy + 9 * s), (cx + dx + 2 * s, gy + dy + 3 * s), (cx + dx - 2 * s, gy + dy + 3 * s)), .05, 9), True, BROWN, INK, .8))
            elif kind == 'start':
                glyphs.append(P(ell(cx, cy + 4, 16, 7.5, amp=.2, n=16), True, BRASSL, BRASS, 1.2, extra=' fill-opacity=".8"'))
            elif kind == 'prato':
                for tx_, ty_ in ((-14, -10), (12, -12), (-4, 8), (14, 7)):
                    glyphs.append(P(C((cx + tx_ - 3, cy + ty_), (cx + tx_ - 1, cy + ty_ - 5), (cx + tx_, cy + ty_ - 1), (cx + tx_ + 1.5, cy + ty_ - 6), (cx + tx_ + 3, cy + ty_)), False, 'none', '#7fa84c', 1.3))
                glyphs.append(P(ell(cx + 6, cy - 3, 1.4, amp=0, n=6), True, PAPER, 'none') + P(ell(cx - 11, cy + 2, 1.4, amp=0, n=6), True, GOLDL, 'none'))
            elif kind == 'matt':
                for k, yy in enumerate((-12, -4, 4, 12)):
                    glyphs.append(f'<path d="M{f(cx - 22)} {f(cy + yy)}H{f(cx + 22)}" stroke="#bb9a62" stroke-width=".9" fill="none"/>')
                    for bx_ in range(-3, 4):
                        xx = cx + bx_ * 9 + (4.5 if k % 2 else 0)
                        if abs(xx - cx) < 21:
                            glyphs.append(f'<path d="M{f(xx)} {f(cy + yy)}v8" stroke="#bb9a62" stroke-width=".9" fill="none"/>')
            elif kind == 'red':
                glyphs.append(P(rr(cx - 12, gy - 11, 24, 24, 4, .2, 12), True, RED, INK, 1.6))
                for ex in (-5.5, 5.5):
                    glyphs.append(P(ell(cx + ex, gy - 4, 3.6, amp=0, n=8), True, PAPER, INK, .9))
                    glyphs.append(P(ell(cx + ex * .8, gy - 3.6, 1.4, amp=0, n=6), True, INK, 'none'))
                glyphs.append(P(wob(C((cx - 7, gy + 6), (cx - 3.5, gy + 10), (cx, gy + 6), (cx + 3.5, gy + 10), (cx + 7, gy + 6)), .1, 9, closed=False), False, 'none', PAPER, 1.6))
            elif kind == 'covered':
                tx, ty = cx + 9, gy
                glyphs.append(P(rr(tx - 12, ty - 11, 24, 24, 4, .2, 12), True, BROWN, INK, 1.6))
                glyphs.append(P(ell(tx, ty + 1, 6, amp=.1, n=10), True, BRASSL, BRASS, 1.2))
                glyphs.append(P(ell(tx, ty + 1, 2, amp=0, n=6), True, BRASS, 'none'))
            ldx = {(0, 1): -13, (1, 1): -10, (2, 2): -2, (1, 3): 0}.get((ri, ci), 0)
            ly = cy + 15.5
            if (ri, ci) == (1, 1): ly = cy + 19
            if kind in ('wood', 'rock', 'house', 'water', 'bridge'): ly = cy + 19
            col_ = '#f4f0e0' if kind == 'wood' else INK
            labels.append(T(cx + ldx, ly, lab, 9.5, 500, fill=col_))
    c = {k: ctr(*v) for k, v in {1: (0, 1), 2: (1, 1), 3: (1, 1), 4: (2, 2)}.items()}
    cp = {1: (c[1][0] + 2, c[1][1] + 2), 2: (c[2][0] - 8, c[2][1] - 6), 3: (c[3][0] + 12, c[3][1] - 6), 4: (c[4][0] - 14, c[4][1] - 8)}
    start = ctr(0, 0); m = ctr(1, 3); ponte = ctr(1, 4)
    c3 = ctr(1, 2)
    dashed = arrow([(c3[0] + 14, m[1] - 4), (ponte[0] + 12, m[1] - 4)], dash='5 4', inner=2.3, head=8, hw=5)
    o = [''.join(hexes), ''.join(glyphs), dashed, ''.join(labels)]
    path = [(start[0] + 14, cp[1][1]), cp[1], cp[2], cp[3], cp[4]]
    dx, dy = cp[4][0] - cp[3][0], cp[4][1] - cp[3][1]; L = math.hypot(dx, dy)
    path[-1] = (cp[4][0] - dx / L * 11, cp[4][1] - dy / L * 11)
    o.append(arrow(path, BLUE, band=6.2, inner=3, head=10, hw=6.4))
    o.append(xmark(m[0], m[1] - 3, 6, 2.8))
    for n in (1, 2, 3, 4):
        o.append(numgear(n, cp[n][0], cp[n][1], 20))
    # bollino +1
    bx_, by_ = (cp[3][0] + cp[4][0]) / 2 + 13, (cp[3][1] + cp[4][1]) / 2 + 1
    o.append(P(ell(bx_, by_, 6.8, amp=.1, n=10), True, GOLDL, BRASS, 1.3) + T(bx_, by_ + 3.3, '+1', 9, 700))
    # pedine
    o.append(pawn(start[0] - 8, start[1] + 8, 23, BLUE))
    a2 = ctr(0, 1)
    o.append(pawn(a2[0] - 17, a2[1] - 1, 16, COPPER))
    bw = ctr(0, 2)
    o.append(xmark(bw[0] + 13, bw[1] - 14, 5.5, 2.6))
    # titolo, dado
    o.append(T(W / 2, 13, 'Si cammina ovunque, tranne sugli ostacoli · almeno 1 passo', 10, 700))
    o.append(die(26, 34, 22, 3, rot=-6))
    o.append(TL(44, 31, ['Dado 3 + MOV 1 = 4:', 'uscire dall\'acqua costa 2'], 9.5, lh=11, anchor='start', weight=600))
    # didascalie
    o.append(TL(a2[0] + 6, 33, ['Ci passi sopra,', 'ma non ti fermi'], 9.5, lh=10.4, anchor='start', weight=600))
    o.append(leader((a2[0] + 4, 38), (a2[0] - 15, a2[1] - 15)))
    o.append(TL(bw[0] + 52, 33, ['Bosco, rocce, case:', 'non ci entri'], 9.5, lh=10.4, anchor='start', weight=600))
    o.append(leader((bw[0] + 50, 36), (bw[0] + 16, bw[1] - 17)))
    b3 = ctr(2, 2)
    o.append(T(b3[0] + 70, 220, 'Conta solo dove ti fermi: gira la tessera', 9.5, 600))
    o.append(leader((b3[0] + 14, 210), (b3[0] + 10, b3[1] + 12)))
    mx = x0 + 5.5 * w + 6
    o.append(TL(mx, m[1] - 62, ['Mostro scoperto:', 'non lo attraversi,', 'ma puoi fermarti', 'e affrontarlo'], 9.5, anchor='start', weight=600))
    o.append(leader((mx - 2, m[1] - 40), (m[0] + 10, m[1] - 14)))
    o.append(TL(mx, m[1] + 28, ['Ponte e guado:', 'passo normale'], 9.5, anchor='start', weight=600))
    o.append(leader((mx - 2, m[1] + 25), (ponte[0] + 16, ponte[1] + 8)))
    ac = ctr(1, 1)
    o.append(TL(8, ac[1] - 6, ['Acqua: entri con 1 passo,', 'uscire ne costa 1 in più'], 9.5, anchor='start', weight=600))
    o.append(leader((70, ac[1] + 9), (ac[0] - 17, ac[1] + 2)))
    lx, ly2 = 8, 152
    sw1 = poly(hexv(lx + 8, ly2 + 8, 8), fill='#c7df8c', stroke=INK, sw=1.1, amp=.15, step=20)
    sw2 = poly(hexv(lx + 24, ly2 + 8, 8), fill='#e8cf9a', stroke=INK, sw=1.1, amp=.15, step=20)
    o.append(sw1 + sw2)
    o.append(TL(lx, ly2 + 28, ['Prato, mattonato,', 'strada: terreno', 'libero'], 9.5, lh=10.4, anchor='start', weight=600))
    emit('S3-mappa', W, H, panel(W, H, ''.join(o)))

# ================================================================ pezzi per S6
SKIN = '#ecc49a'

def bust(cx, cy, col, hat):
    """avventuriero a mezzo busto (cartoon, di fronte): mantello, testa, cappello."""
    o = P(wob([(cx - 19, cy + 22, True), (cx - 17, cy + 12, False), (cx - 8, cy + 8, False), (cx + 8, cy + 8, False),
               (cx + 17, cy + 12, False), (cx + 19, cy + 22, True)], .25, 10), True, col, INK, 1.6)
    if hat == 'wizard':
        o += P(wob(C((cx - 15, cy - 6), (cx + 15, cy - 6), (cx + 2, cy - 30)), .15, 10), True, col, INK, 1.6)
    o += P(ell(cx, cy, 11, 11.5, amp=.2, n=14), True, SKIN, INK, 1.6)
    if hat == 'wizard':
        o += P(wob(C((cx - 17, cy - 6), (cx + 17, cy - 6), (cx + 15, cy - 9), (cx - 15, cy - 9)), .1, 10), True, col, INK, 1.6)
    elif hat == 'helm':
        o += P([(cx - 12, cy - 1, True), (cx - 11, cy - 10, False), (cx, cy - 15, False), (cx + 11, cy - 10, False), (cx + 12, cy - 1, True)], True, '#9a948a', INK, 1.6)
        o += P(wob(C((cx - 1.6, cy - 12), (cx + 1.6, cy - 12), (cx + 1.6, cy + 4), (cx - 1.6, cy + 4)), .05, 10), True, '#9a948a', INK, 1.2)
    elif hat == 'hood':
        o += P([(cx - 13, cy + 6, True), (cx - 13, cy - 8, False), (cx, cy - 15, False), (cx + 13, cy - 8, False), (cx + 13, cy + 6, True),
                (cx + 8, cy - 2, False), (cx, cy - 6, False), (cx - 8, cy - 2, False)], True, col, INK, 1.6)
    elif hat == 'horns':
        o += P([(cx - 12, cy - 2, True), (cx - 11, cy - 9, False), (cx, cy - 13, False), (cx + 11, cy - 9, False), (cx + 12, cy - 2, True)], True, COPPER, INK, 1.6)
        for sx in (-1, 1):
            o += P(wob(C((cx + sx * 9, cy - 10), (cx + sx * 16, cy - 20), (cx + sx * 13, cy - 8)), .1, 10), True, PAPER, INK, 1.3)
    for ex in (-4, 4):
        o += P(ell(cx + ex, cy + 1.5, 1.5, amp=0, n=6), True, INK, 'none')
    o += P(wob(C((cx - 4, cy + 6), (cx, cy + 8.2), (cx + 4, cy + 6)), .05, 10, closed=False), False, 'none', INK, 1.1)
    return o

def bubble(x, y, w, h, lines, tail, size=9.5, weight=600, fill=PAPER):
    """fumetto con coda verso tail=(tx,ty); testo centrato."""
    cx = x + w / 2; cy = y + h / 2
    tx, ty = tail
    dx, dy = tx - cx, ty - cy; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    bx, by = cx + dx * 0.0, cy + dy * 0.0
    # la coda parte dal bordo piu' vicino
    if abs(dx) / w > abs(dy) / h:
        ex = x + w if dx > 0 else x; ey = min(max(ty, y + 6), y + h - 6); base = [(ex, ey - 4), (ex, ey + 4)]
    else:
        ey = y + h if dy > 0 else y; ex = min(max(tx, x + 8), x + w - 8); base = [(ex - 4, ey), (ex + 4, ey)]
    tail_p = P(C(base[0], (tx, ty), base[1]), True, fill, INK, 1.4)
    box = P(rr(x, y, w, h, 6, .25, 14), True, fill, INK, 1.4)
    cover = P(C((base[0][0] + (.8 if base[0][1] == base[1][1] else 0), base[0][1] + (.8 if base[0][0] == base[1][0] else 0)),
                (base[1][0], base[1][1])), False, 'none', fill, 2.4)
    lh = size * 1.12
    y0_ = cy - (len(lines) - 1) * lh / 2 + size * .34
    txt = ''.join(T(cx, y0_ + i * lh, ln, size, weight) for i, ln in enumerate(lines))
    return tail_p + box + cover + txt

def cartel(cx, cy, lines, size=9.5, rot=-2, w=None):
    w = w or max(tw(ln, size, 600) for ln in lines) + 14
    h = len(lines) * size * 1.12 + 7
    g = P(rr(cx - w / 2, cy - h / 2, w, h, 4, .2, 14), True, GOLDL, BRASS, 1.3)
    g += gv.rivet(cx - w / 2 + 3.4, cy - h / 2 + 3.4, 1.4) + gv.rivet(cx + w / 2 - 3.4, cy - h / 2 + 3.4, 1.4)
    lh = size * 1.12
    g += ''.join(T(cx, cy - (len(lines) - 1) * lh / 2 + size * .34 + i * lh + 1, ln, size, 600) for i, ln in enumerate(lines))
    return f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">{g}</g>'

def card(cx, cy, w, h, rot=0, back=False, fill=PAPER):
    g = P(rr(cx - w / 2, cy - h / 2, w, h, 3, .2, 12), True, BROWN if back else fill, INK, 1.5)
    if back:
        g += P(ell(cx, cy, min(w, h) * .26, amp=.05, n=10), True, BRASSL, BRASS, 1)
    else:
        g += P(wob(C((cx - w / 2 + 3, cy - h / 2 + 3), (cx + w / 2 - 3, cy - h / 2 + 3)), .1, 12, closed=False), False, 'none', BRASS, 1.2)
    return f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">{g}</g>' if rot else g

def arc_arrow(cx, cy, r, a0, a1, col=BLUE):
    pts = arcpts(cx, cy, r, a0, a1, .3, 8)
    ex, ey = pts[-1][0], pts[-1][1]
    hl = 10; hw = 6.2
    ang = math.radians(a1); tx, ty = -math.sin(ang), math.cos(ang)    # tangente (senso orario sullo schermo)
    bx, by = ex - tx * hl, ey - ty * hl
    body = arcpts(cx, cy, r, a0, a1 - math.degrees(hl / r) * .8, .3, 8)
    o = P(body, False, 'none', INK, 6) + P(body, False, 'none', col, 3)
    nx, ny = -ty, tx
    o += P(C((ex, ey), (bx + nx * hw, by + ny * hw), (bx - nx * hw, by - ny * hw)), True, col, INK, 1.8)
    return o

# ================================================================ S6 · catena
def s6():
    R.seed(606)
    W, H = 515, 280
    o = []
    tc = (134, 108); tr = 56
    # tavolo tondo
    o.append(P(ell(tc[0], tc[1], tr + 5, amp=.5, n=40), True, BROWN, INK, 1.8))
    o.append(P(ell(tc[0], tc[1], tr, amp=.5, n=40), True, BRASSL, INK, 1.6))
    # frecce 1-2-3 in senso orario: Anna(90) -> Bruno(180) -> Carla(270) -> Dario(360)
    ra = 42
    arcs = [(1, 106, 166), (2, 196, 256), (3, 286, 346)]
    for n, a0, a1 in arcs:
        o.append(arc_arrow(tc[0], tc[1], ra, a0, a1))
    for n, a0, a1 in arcs:
        am = math.radians((a0 + a1) / 2 - 4)
        o.append(numgear(n, tc[0] + ra * math.cos(am), tc[1] + ra * math.sin(am), 22))
    # carte sul tavolo (Bruno e Dario giocano una carta), dadi + bollino di Anna
    o.append(card(tc[0] - 25, tc[1] - 4, 15, 21, -12))
    o.append(card(tc[0] + 25, tc[1] - 6, 15, 21, 10))
    o.append(die(tc[0] - 18, tc[1] + 20, 18, 4, rot=-8))
    o.append(die(tc[0] + 4, tc[1] + 24, 18, 3, rot=9))
    bx, by = tc[0] + 31, tc[1] + 26
    o.append(P(ell(bx, by, 14.5, amp=.2, n=14), True, GOLDL, BRASS, 1.5))
    o.append(T(bx, by - 1.5, 'ATT', 9, 700) + T(bx, by + 9.5, '2', 10, 700))
    # avventurieri
    o.append(bust(tc[0], 32, VIOLET, 'hood') + T(tc[0] - 22, 38, 'Carla', 10.5, 700, 'end'))
    o.append(bust(34, tc[1] + 4, COPPER, 'helm') + T(34, tc[1] + 44, 'Bruno', 10.5, 700))
    o.append(bust(tc[0] + 102, tc[1] + 4, '#8a6a2f', 'horns') + T(tc[0] + 102, tc[1] + 44, 'Dario', 10.5, 700))
    o.append(bust(tc[0], 186, BLUE, 'wizard') + T(tc[0], 222, 'Anna', 10.5, 700))
    # fumetti
    o.append(bubble(tc[0] + 30, 8, 60, 22, ['Passo.'], (tc[0] + 12, 30)))
    o.append(bubble(4, 50, 76, 22, ['Ritira i dadi!'], (30, tc[1] - 14)))
    o.append(bubble(tc[0] + 56, 50, 80, 22, ['Annullo Bruno!'], (tc[0] + 98, tc[1] - 14)))
    o.append(bubble(4, 182, 104, 42, ['Tiro per colpire: 9.', 'Rispondo per prima:', 'passo.'], (tc[0] - 12, 192)))
    # cartellini
    o.append(cartel(tc[0] + 94, tc[1] + 64, ['Il giro si chiude', "con l'ultimo"], rot=-3))
    o.append(cartel(tc[0] + 72, 208, ['Sul tuo tiro rispondi', 'per primo tu'], rot=-2))
    # ---- la pila a destra
    ax = 278
    o.append(arrow([(ax, 10), (ax, 214)], GOLD, band=11, inner=6.4, head=20, hw=11.5, amp=.4))
    o.append(T(ax + 18, 112, "Si risolve dall'ultima alla prima", 11, 700, rot=90))
    sx, sw_ = 314, 100
    items = [(10, 52), (78, 52), (146, 52)]
    # 3 in cima
    for k, (y, h) in enumerate(items[:2]):
        o.append(P(rr(sx + 3, y + 3, sw_, h, 5, .2, 14), True, INK, 'none', extra=' fill-opacity=".18"'))
        o.append(card(sx + sw_ / 2, y + h / 2, sw_, h, 0))
        o.append(P(rr(sx + 4, y + 4, 9, h - 8, 3, .1, 12), True, BRASSL if k else GOLDL, BRASS, 1))
    o.append(TL(sx + 56, 28, ['3 · Dario:', 'annulla Bruno'], 10.5, anchor='middle', weight=700))
    o.append(TL(sx + 56, 96, ['2 · Bruno:', 'ritira'], 10.5, anchor='middle', weight=700))
    y1 = items[2][0]
    o.append(P(rr(sx + 3, y1 + 3, sw_, 52, 5, .2, 14), True, INK, 'none', extra=' fill-opacity=".18"'))
    o.append(P(rr(sx, y1, sw_, 52, 5, .2, 14), True, PAPER, INK, 1.5))
    o.append(die(sx + 14, y1 + 26, 17, 4, rot=-8) + die(sx + 32, y1 + 28, 17, 3, rot=7))
    o.append(TL(sx + 46, y1 + 22, ['1 · Tiro di', 'Anna: 9'], 10.5, anchor='start', weight=700))
    # esiti
    ox = 430
    def link(y): return arrow([(sx + sw_ + 3, y), (ox - 3, y)], dash='3 3', inner=1.8, head=6, hw=3.6)
    for y in (36, 104, 172): o.append(link(y))
    o.append(xmark(ox + 8, 24, 4.5, 2.4))
    o.append(TL(ox + 20, 22, ['Dario: Bruno', 'è annullato'], 9.5, anchor='start', weight=600))
    o.append(card(ox + 7, 100, 12, 17, 0, back=True))
    o.append(TL(ox + 20, 92, ['Annullata:', 'non fa niente,', 'ma conta'], 9.5, anchor='start', weight=600))
    o.append(tick(ox + 8, 160, 5.5, GREEN, 2.8))
    o.append(TL(ox + 20, 156, ['Il tiro vale', 'alla fine:', 'Anna tiene', 'il 9, colpito!'], 9.5, anchor='start', weight=700, fill=GREEN))
    # didascalia e riquadro
    o.append(T(W / 2, 236, '1 carta a testa per giro · nessun altro giro finché la pila non è vuota · Bersaglio sparito: la carta non fa niente, ma conta', 9.5, 600))
    bxy = (10, 244, 495, 28)
    o.append(P(rr(bxy[0], bxy[1], bxy[2], bxy[3], 6, .25, 14), True, PAPER, BRASS, 1.4))
    o.append(T(bxy[0] + 10, 256, 'Effetti automatici:', 9.5, 700, 'start'))
    o.append(T(bxy[0] + 10 + tw('Effetti automatici: ', 9.5, 700), 256, 'potere della Carta Classe, Equipaggiamenti in gioco, Forte Volontà, mostri, Stati.', 9.5, 500, 'start'))
    o.append(T(bxy[0] + 10, 267, 'Scattano subito, nessuno risponde, non contano come carte.', 9.5, 500, 'start'))
    emit('S6-catena', W, H, panel(W, H, ''.join(o)))

# ================================================================ pezzi per S1
def sub(x, y, body): return f'<g transform="translate({f(x)} {f(y)})">{body}</g>'

def plancia(x, y, w, h, label=None, vertical=0, size=9):
    g = P(rr(x, y, w, h, 3.5, .25, 12), True, BRASSL, INK, 1.4)
    if label:
        if vertical:
            g += T(x + w / 2 + (3.2 if vertical < 0 else -3.2), y + h / 2, label, size, 700, rot=vertical, anchor='middle')
        else:
            g += T(x + w / 2, y + h / 2 + 3.2, label, size, 700)
    return g

def rotella(cx, cy, r, value=None, win=True):
    g = P(ell(cx, cy, r, amp=.3, n=18), True, PAPER, INK, 1.6)
    g += P(ell(cx, cy, r - 3, amp=.1, n=16), True, 'none', BRASS, .8)
    if win:
        g += P(rr(cx - r * .5, cy - r * .86, r, r * .72, 2, .1, 12), True, PARCH, INK, 1)
        if value is not None: g += T(cx, cy - r * .86 + r * .6, str(value), 10, 700)
    g += P(ell(cx, cy + r * .28, 2.6, amp=0, n=8), True, BRASSL, BRASS, 1)
    return g

def moneta(cx, cy, r, fill=BLUE):
    return P(ell(cx, cy, r, amp=.15, n=12), True, fill, INK, 1.2) + P(ell(cx, cy, r * .45, amp=0, n=8), True, 'none', PAPER, .9)

def mazzo(cx, cy, w, h, col, n=3):
    g = ''
    for i in range(n, 0, -1):
        g += P(rr(cx - w / 2 + i * .9, cy - h / 2 - i * .9, w, h, 2.5, .15, 12), True, PAPER, INK, 1.1)
    g += P(rr(cx - w / 2, cy - h / 2, w, h, 2.5, .15, 12), True, col, INK, 1.4)
    g += P(ell(cx, cy, w * .22, amp=.05, n=8), True, BRASSL, BRASS, .9)
    return g

def slot_icon(kind, cx, cy):
    g = ''
    if kind == 'elmo':
        g += P([(cx - 9, cy + 7, True), (cx - 9, cy - 2, False), (cx - 5, cy - 8, False), (cx + 5, cy - 8, False), (cx + 9, cy - 2, False), (cx + 9, cy + 7, True)], True, '#a7a196', INK, 1.4)
        g += P(wob(C((cx - 9, cy + 1), (cx + 9, cy + 1), (cx + 9, cy + 3.5), (cx - 9, cy + 3.5)), .05, 12), True, INK, 'none')
        g += P(wob(C((cx, cy - 10), (cx, cy - 4)), .05, 12, closed=False), False, 'none', RED, 2)
    elif kind == 'spada':
        g += P(wob(C((cx - 1.8, cy - 11), (cx + 1.8, cy - 11), (cx + 1.8, cy + 4), (cx - 1.8, cy + 4)), .05, 12), True, '#d8d4cc', INK, 1.2)
        g += P(wob(C((cx - 6, cy + 4), (cx + 6, cy + 4), (cx + 6, cy + 6.4), (cx - 6, cy + 6.4)), .05, 12), True, BRASS, INK, 1.2)
        g += P(wob(C((cx - 1.4, cy + 6.4), (cx + 1.4, cy + 6.4), (cx + 1.4, cy + 11), (cx - 1.4, cy + 11)), .05, 12), True, BROWN, INK, 1)
    elif kind == 'scudo':
        g += P([(cx - 9, cy - 9, True), (cx + 9, cy - 9, True), (cx + 9, cy + 1, False), (cx, cy + 11, True), (cx - 9, cy + 1, False)], True, BLUE, INK, 1.4)
        g += P(wob(C((cx, cy - 9), (cx, cy + 10)), .05, 12, closed=False), False, 'none', PAPER, 1.4)
    elif kind == 'armatura':
        g += P([(cx - 10, cy - 8, True), (cx - 4, cy - 10, False), (cx + 4, cy - 10, False), (cx + 10, cy - 8, True), (cx + 8, cy + 10, True), (cx - 8, cy + 10, True)], True, '#a7a196', INK, 1.4)
        g += P(wob(C((cx - 4, cy - 10), (cx, cy - 4), (cx + 4, cy - 10)), .05, 12, closed=False), False, 'none', INK, 1.1)
        g += P(wob(C((cx - 8, cy + 3), (cx + 8, cy + 3)), .05, 12, closed=False), False, 'none', INK, 1)
    return g

def slot(x, y, w, h, kinds):
    g = P(rr(x, y, w, h, 4, .2, 12), True, BROWN, INK, 1.4)
    g += P(rr(x + 2.2, y + 2.2, w - 4.4, h - 4.4, 3, .1, 12), True, '#c9ae78', 'none')
    n = len(kinds)
    for i, k in enumerate(kinds):
        g += slot_icon(k, x + w * (i + .5) / n, y + h / 2)
    return g

def tile_stato(cx, cy, w, h, rot, col):
    g = P(rr(cx - w / 2, cy - h / 2, w, h, 2.5, .1, 12), True, col, INK, 1.3)
    g += P(ell(cx, cy, min(w, h) * .26, amp=0, n=8), True, PAPER, 'none')
    return f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">{g}</g>' if rot else g

def mini_arrow(x0_, y0_, x1_, y1_, col=BLUE):
    return arrow([(x0_, y0_), (x1_, y1_)], col, band=4.2, inner=1.9, head=7, hw=4.2, amp=.15)

# ================================================================ S1 · tavolo
# ---- mappa 12x12 schematica (dati veri da v7/idee/mappa_tessere/12x12/mappa12.py)
_M12 = os.path.normpath(os.path.join(KIT, '..', '..', '..', '..', 'idee', 'mappa_tessere', '12x12'))
TERR = {'prato': '#c7df8c', 'mattonato': '#e8cf9a', 'pavimento': '#d9c08a', 'sentiero': '#e8cf9a', 'guado': '#a6d0e2',
        'ponte': '#b58a52', 'acqua': '#a6d0e2', 'bosco': '#3f6f3a', 'rocce': '#a39d94', 'case': '#d49a78', 'partenza': '#e8cf9a'}

def _m12():
    sys.path.insert(0, _M12)
    import mappa12 as m
    sys.path.remove(_M12)
    return m

def map12(x0, y0, rad, placed, hand=None):
    """base 12x12 con coordinate sopra e a sinistra, Partenze, spazi dei fiori numerati e alcuni fiori posati."""
    m = _m12()
    w = math.sqrt(3) * rad
    def pos(c, r): return (x0 + w / 2 + (c - 1) * w + (w / 2 if r % 2 == 0 else 0), y0 + rad + (r - 1) * 1.5 * rad)
    flower_of = {}
    for s in m.SPAZI:
        flower_of[m.SPAZI[s]] = s
        for k in range(6): flower_of[m.anello(s, k)] = s
    terr = {}
    for s, (i, lato, rot) in placed.items():
        t = {}
        m.posa(t, s, m.FIORI[i][lato], rot)
        terr.update(t)
    o = []
    for (c, r) in m.CELLE:
        cx, cy = pos(c, r)
        s = flower_of.get((c, r))
        if (c, r) in terr:
            fill = TERR[terr[(c, r)]]
        elif s is None:
            fill = '#ecd9a3'
        else:
            fill = '#fbf1cf'
        o.append(P(hexv(cx, cy, rad), True, fill, INK, .6, extra=' stroke-opacity=".7"'))
        if s is None and (c, r) in m.OSTACOLI_BASE:
            o[-1] = P(hexv(cx, cy, rad), True, TERR[m.OSTACOLI_BASE[(c, r)]], INK, .6)
    # contorni dei fiori
    for s in m.SPAZI:
        cells = {m.SPAZI[s]} | {m.anello(s, k) for k in range(6)}
        full = s in placed
        for h in cells:
            cx, cy = pos(*h)
            for k, (a, b) in enumerate(((-30, 30), (-90, -30), (-150, -90), (150, 210), (90, 150), (30, 90))):
                q, r0 = m.AX[h]; dq, dr = m.DIR[k]
                nb = m.HX.get((q + dq, r0 + dr))
                if nb in cells: continue
                p1 = (cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a)))
                p2 = (cx + rad * math.cos(math.radians(b)), cy + rad * math.sin(math.radians(b)))
                o.append(f'<path d="M{f(p1[0])} {f(p1[1])}L{f(p2[0])} {f(p2[1])}" stroke="{INK if full else BRASS}" stroke-width="{1.5 if full else 1.3}" stroke-linecap="round"/>')
    for s in m.SPAZI:
        if s in placed: continue
        cx, cy = pos(*m.SPAZI[s])
        o.append(T(cx, cy + 3.1, str(s), 9, 700, fill=BROWN))
    for i, h in enumerate(m.PARTENZE, 1):
        cx, cy = pos(*h)
        o.append(P(ell(cx, cy, rad - .7, amp=0, n=10), True, VIOLET, 'none'))
        o.append(T(cx, cy + 3.1, str(i), 9, 700, fill=PAPER))
    for c in range(1, 13):
        o.append(T(pos(c, 1)[0], y0 - (11 if c == 11 else 3), str(c), 9, 500))
    for r in range(1, 13):
        o.append(T(x0 - 2.5, pos(1, r)[1] + 3.1, str(r), 9, 600, 'end'))
    return ''.join(o), pos, m

def s1_left():
    W, H = 275, 265
    R.seed(101)
    o = [T(W / 2, 11, 'Il tavolo pronto', 11, 700, serif=True)]
    o.append(P(rr(14, 26, 247, 225, 16, .5, 14), True, PAPER, BROWN, 2.4))
    o.append(plancia(100, 13, 75, 12, 'Plancia eroe'))
    o.append(plancia(2, 70, 12, 110, 'Plancia eroe', vertical=-90))
    o.append(plancia(261, 70, 12, 110, 'Plancia eroe', vertical=90))
    o.append(plancia(14, 253, 166, 12))
    o.append(T(18, 253 + 9.2, 'Plancia eroe', 9, 700, 'start'))
    o.append(T(128, 253 + 9.2, 'Primo giocatore', 9, 700, 'middle'))
    o.append(pawn(204, 265, 22, '#6f9a4a'))
    for sx in (-1, 1):
        o.append(P(C((204 + sx * 3, 254), (204 + sx * 10, 249), (204 + sx * 6, 256)), True, '#6f9a4a', INK, 1.1))
    o.append(P(rr(19, 31, 237, 216, 12, .3, 16), True, 'none', BLUE, 2.2, extra=' stroke-opacity=".9"'))
    def head(x, y, ang):
        a = math.radians(ang); ux, uy = math.cos(a), math.sin(a)
        return P(C((x + ux * 6, y + uy * 6), (x - ux * 4 - uy * 5, y - uy * 4 + ux * 5), (x - ux * 4 + uy * 5, y - uy * 4 - ux * 5)), True, BLUE, INK, 1.2)
    o.append(head(215, 31, 0) + head(256, 150, 90) + head(120, 247, 180) + head(19, 120, 270))
    o.append(tag(100, 31, 'Senso orario: tocca a sinistra', 9, 600, pad=4, stroke=BLUE))
    # mappa
    o.append(T(24, 44, 'Mappa: base + 14 fiori', 9.5, 700, 'start'))
    rad = 5.4
    placed = {2: (0, 0, 1), 4: (4, 0, 0), 8: (6, 1, 3), 11: (12, 0, 2)}
    body, pos, m = map12(28, 55, rad, placed)
    o.append(body)
    # fiore in mano: sopra lo spazio 7, sollevato, con la manina
    hx, hy = pos(*m.SPAZI[5]); hx += 4; hy -= 7
    hand = ''
    for h in [(0, 0)] + [m.DIR[k] for k in range(6)]:
        q, r0 = h
        cx = hx + rad * math.sqrt(3) * (q + r0 / 2); cy = hy + rad * 1.5 * r0
        t = ('bosco' if h != (0, 0) and m.DIR.index(h) % 2 == 0 else 'prato')
        hand += P(hexv(cx, cy, rad), True, TERR[t], INK, 1.2)
    hand += T(hx, hy - 12, '', 9)
    hand = f'<g transform="rotate(-14 {f(hx)} {f(hy)})"><g opacity=".25" transform="translate(1.5 2)">{hand}</g>{hand}</g>'
    hand += P(ell(hx + 14, hy - 10, 4.6, 3.6, amp=0, n=10, rot_deg=-30), True, '#f3d3b0', INK, 1) + P(C((hx + 17, hy - 12), (hx + 24, hy - 17), (hx + 21, hy - 9)), True, '#f3d3b0', INK, 1)
    o.append(hand)
    # Sala del Tesoro
    sx0, sy0, sw2, sh2 = 148, 38, 109, 110
    o.append(P(rr(sx0, sy0, sw2, sh2, 6, .3, 14), True, '#e3dac8', INK, 1.6))
    o.append(T(sx0 + sw2 / 2, sy0 + 11, 'Sala del Tesoro', 9.5, 700))
    for cxr, lines in ((sx0 + 28, ['Rotella del', 'custode (sui', 'suoi PV)']), (sx0 + 82, ['Rotella dello', 'scontro'])):
        o.append(rotella(cxr, sy0 + 25, 7.5, None, win=False))
        o.append(TL(cxr, sy0 + 42, lines, 9, lh=9.2, weight=500))
    ry = sy0 + 78
    o.append(icon('ic_tesoro', sx0 + 28, ry, 22) + T(sx0 + 28, ry + 19, 'MIMI', 9, 700))
    cx_, cy_ = sx0 + 82, ry
    o.append(P(ell(cx_, cy_ + 1, 6.5, 7, amp=.2, n=12), True, INK, 'none'))
    for sx in (-1, 1):
        o.append(P(wob(C((cx_ + sx * 4, cy_ - 3), (cx_ + sx * 9, cy_ - 9), (cx_ + sx * 7.5, cy_ - 1.5)), .1, 10), True, INK, 'none'))
        o.append(P(ell(cx_ + sx * 2.8, cy_ + .5, 1.4, amp=0, n=6), True, GOLDL, 'none'))
    o.append(P(wob(C((cx_ - 3, cy_ + 7), (cx_ + 3, cy_ + 7), (cx_ + 8, cy_ + 13), (cx_ - 8, cy_ + 13)), .1, 10), True, INK, 'none'))
    o.append(TL(cx_, ry + 19, ['Custode:', 'con la Cripta'], 9, lh=9.2, weight=700))   # D31: si pesca dal mazzetto 3 quando compare la Cripta
    # cartellini
    o.append(P(rr(22, 160, 120, 85, 5, .25, 14), True, GOLDL, BRASS, 1.3))
    lines = [('Fiori a testa: 7 · 4 · 3', 700), ('(con 2 · 3 · 4 giocatori)', 500),
             ('Tessere a testa: 12 · 8 · 6', 700), ('ad almeno 2 esagoni', 500), ('da ogni Partenza', 500),
             ('Avanzano 2 fiori:', 700), ('ultimo e penultimo', 500), ('Faccia e verso liberi', 700)]
    for s_, wt in lines: pass
    for (s_, wt), yy in zip(lines, (170, 179, 190, 199, 208, 219, 228, 238)):
        o.append(T(28, yy, s_, 9, wt, 'start'))
    # mazzetti, mucchietti e Cripta
    items = [('Mazzetto 1', COPPER, ['Mazzetto', '1']), ('Mazzetto 2', BLUE, ['Mazzetto', '2']), ('Mazzetto 3', VIOLET, ['Mazzetto', '3']),
             ('Imprevisti', '#c7a64a', ['Imprevisti']), ('Mazzo comune', BRASS, ['Mazzo', 'comune']), ('Riserva', None, ['Riserva']),
             ('Tessere usate', None, ['Tessere', 'usate']), ('Cripta', None, ['Cripta:', 'arriva al', '3° Indizio'])]
    ys = [151, 173, 195, 217]
    for i, (nm, col, lines) in enumerate(items):
        gx_ = 151 + (i % 2) * 55; gy_ = ys[i // 2] + 10
        if nm == 'Riserva':
            for j, c_ in enumerate((BLUE, RED, BLUE)): o.append(moneta(gx_ + 6 + j * 2.4, gy_ + 3 - j * 1.8, 5, c_))
        elif nm == 'Tessere usate':
            for j, c_ in enumerate(('#9a948a', '#b0aaa0', '#9a948a')): o.append(moneta(gx_ + 6 + j * 2.4, gy_ + 3 - j * 1.8, 5, c_))
        elif nm == 'Cripta':
            o.append(poly(hexv(gx_ + 7, gy_ + 1, 8), fill='#9a9288', stroke=INK, sw=1.2, amp=.1, step=20))
            o.append(P(gv.cog(gx_ + 7, gy_ + 1, 5, 8, .3, .05), True, GOLDL, BRASS, .8))
        else:
            o.append(mazzo(gx_ + 6, gy_, 11, 16, col, 2))
        o.append(TL(gx_ + (17 if nm in ('Riserva', 'Tessere usate') else 15), gy_ + (-4 if len(lines) == 3 else (0 if len(lines) == 2 else 3)) - (1 if len(lines) == 3 else 0) - (0 if len(lines) != 2 else 3) + (4 if len(lines) == 2 else 0) - (4 if len(lines) == 2 else 0), lines, 9, lh=9.4, anchor='start', weight=600 if nm != 'Cripta' else 700))
    return W, H, ''.join(o)

def s1_right():
    W, H = 234, 265
    R.seed(102)
    o = [T(W / 2, 12, 'La plancia eroe', 11, 700, serif=True)]
    for x, col in ((6, VIOLET), (182, BRASS)):
        o.append(P(rr(x, 5, 46, 62, 4, .25, 12), True, PAPER, INK, 1.6))
        o.append(P(rr(x + 3, 8, 40, 5, 2, .1, 12), True, col, 'none'))
    o.append(P(rr(3, 34, 228, 195, 10, .35, 14), True, BRASSL, INK, 1.8))
    for x in (6, 180):
        o.append(P(rr(x, 32, 50, 5, 2, .1, 12), True, BROWN, INK, 1.2))
    for x, lines in ((29, ['Carta', 'Classe']), (205, ['Carta', 'Specie'])):
        o.append(TL(x, 21, lines, 9.5, lh=10, weight=700))
    o.append(T(117, 27, 'Infilale negli angoli', 9.5, 700))
    o.append(mini_arrow(76, 22, 58, 22) + mini_arrow(158, 22, 176, 22))
    o.append(rotella(14, 54, 8, win=False))
    o.append(TL(26, 45, ['Rotella della', 'Profezia', '(solo Oracolo)'], 9, lh=9.4, anchor='start', weight=500))
    for i in range(3):
        o.append(P(ell(92 + i * 12, 50, 5, amp=.1, n=10), True, GOLDL, BRASS, 1.3) + P(ell(92 + i * 12, 50, 1.8, amp=0, n=6), True, BRASS, 'none'))
    o.append(T(104, 66, 'Indizi', 9, 700))
    o.append(P(ell(144, 50, 6, amp=.1, n=10), True, VIOLET, INK, 1.3) + P(ell(144, 50, 2.2, amp=0, n=6), True, PAPER, 'none'))
    o.append(T(144, 66, 'Forte Volontà', 9, 700))
    # Stati: verticale (preso nel turno di un altro) e orizzontale (preso nel tuo turno)
    o.append(P(rr(171, 38, 59.5, 40, 4, .2, 12), True, PARCH, INK, 1.3))
    o.append(T(200.75, 47, 'Stati', 9, 700))
    o.append(tile_stato(178, 57, 6.5, 12, 0, BLUE) + T(185, 60.5, 'verticale', 9, 500, 'start'))
    o.append(tile_stato(178.5, 70.5, 6.5, 12, 90, COPPER) + T(186.5, 74, 'orizzontale', 9, 500, 'start'))
    o.append(T(117, 85, 'Le statistiche stanno solo sulle rotelle · valori di partenza', 9, 700))
    # D30: PV (5–13) e Danni (0–13), una rotella ciascuno
    vals = [('PV', 5), ('Danni', 0), ('ATT', 1), ('MOV', 1), ('AR', 9), ('PL', 0)]
    for i, (nm, v) in enumerate(vals):
        cx = 24 + i * 37.5
        o.append(rotella(cx, 105, 12, v))
        o.append(T(cx, 126, nm, 9.5, 700))
    o.append(T(24, 136, 'da 5 a 13', 9, 500))
    o.append(T(61.5, 136, 'da 0 a 13', 9, 500))
    o.append(TL(227, 136, ['somma dei PL degli', 'Equipaggiamenti'], 9, lh=9.2, anchor='end', weight=500))
    o.append(T(117, 155, 'Bonus di Incanti, Stati e Mappe: non girano le rotelle', 9, 500))
    specs = [(['elmo'], ['Elmo']), (['spada', 'scudo'], ['Arma DX /', 'Scudo']), (['spada'], ['Arma SX']), (['armatura'], ['Armatura'])]
    for i, (kinds, lab) in enumerate(specs):
        x = 8 + i * 55
        o.append(slot(x, 161, 44, 20, kinds))
        o.append(TL(x + 22, 192, lab, 9, lh=9.2, weight=500))
    o.append(cartel(117, 216, ['Nuovo Equipaggiamento: il vecchio va negli scarti.', 'Gira subito le rotelle, PL compreso'], 9, rot=-.6, w=214))
    cy = 241
    for ang in (-26, -9, 9, 26):
        o.append(f'<g transform="rotate({ang} 36 {cy + 17})">' + card(36, cy, 16, 20, 0) + '</g>')
    o.append(T(36.5, 260, 'Mano (max 10)', 9, 500))
    o.append(mazzo(91.5, cy, 16, 20, BROWN) + T(91.5, 260, 'Pila di classe', 9, 500))
    o.append(mazzo(131, cy, 16, 20, PAPER, 3).replace(BRASSL, PARCH) + T(131, 260, 'Scarti', 9, 500))
    o.append(card(178, cy, 16, 20, -5) + card(196, cy + 1, 16, 20, 5) + T(186, 260, 'Carte giocate (max 2)', 9, 500))
    return W, H, ''.join(o)

def s1():
    W, H = 515, 265
    lw, lh, lbody = s1_left()
    parts = [subpanel(0, 0, lw, H, lbody)]
    if 's1_right' in globals():
        rw, rh, rbody = s1_right()
        parts.append(subpanel(lw + 6, 0, W - lw - 6, H, rbody))
    emit('S1-tavolo', W, H, ''.join(parts))

def subpanel(x, y, w, h, body):
    bg = P(rr(x + .8, y + .8, w - 1.6, h - 1.6, 9, .25, 14), True, PARCH, BRASS, 1.5)
    rv = ''.join(gv.rivet(x + dx, y + dy, 2) for dx, dy in ((7, 7), (w - 7, 7), (7, h - 7), (w - 7, h - 7)))
    return bg + sub(x, y, body) + rv

# ================================================================ main
if __name__ == '__main__':
    todo = [a.upper() for a in sys.argv[1:]] or ['S1', 'S3', 'S6']
    for t in todo:
        {'S1': s1, 'S3': s3, 'S6': s6}[t]()
    import shutil; shutil.rmtree(TMP, ignore_errors=True)
