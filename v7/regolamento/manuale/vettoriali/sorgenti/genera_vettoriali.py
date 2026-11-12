#!/usr/bin/env python3
"""Kit vettoriale del regolamento «Il Tesoro del Goblin» (A4, <=5 pagine).

Genera gli SVG di partenza (sorgenti geometrici con la linea «ballerina» a mano libera), poi li passa a
vectorcraft-cli: SVG -> .vectorcraft (sorgente modificabile, in sorgenti/) -> SVG pulito + PDF vettoriale
(in vettoriali/). Nessun testo nelle decorazioni; solo i numeri dei passi (Noto Serif Bold) sono
convertiti in tracciati con type.createOutlines.

Uso:  python3 genera_vettoriali.py [cartella_temporanea]
"""
import math, os, random, re, subprocess, sys, json, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)            # .../vettoriali
TMP = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix='vk_')
os.makedirs(TMP, exist_ok=True)

# ---- palette esistente (identica a carte/componenti) ----
INK = '#2a2118'; BROWN = '#6b4a2b'; RED = '#9c2f24'; BLUE = '#2f5d7c'; GOLD = '#b8862b'; GOLDL = '#f6d68b'
BRASS = '#a8823a'; BRASSL = '#e8cd8f'; COPPER = '#a65a32'; PAPER = '#f9f2e0'; PARCH = '#f1dcae'
RETRO = '#3b2a1c'; GREEN = '#3d6f45'; VIOLET = '#7a4f86'

FONT_LABEL = os.popen('fc-match -f %{file} "Liberation Sans"').read()   # solo per le etichette dell'anteprima
R = random.Random()
def J(a): return R.uniform(-a, a)

# ---------------------------------------------------------------- geometria «ballerina»
# punto = (x, y, corner). corner=True: la curva ha uno spigolo; False: passa liscia.
def C(*p): return [(x, y, True) for x, y in p]
def S(*p): return [(x, y, False) for x, y in p]

def rot(pts, deg, cx, cy):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    return [((cx + (x - cx) * ca - (y - cy) * sa), (cy + (x - cx) * sa + (y - cy) * ca), c) for x, y, c in pts]

def mv(pts, dx, dy): return [(x + dx, y + dy, c) for x, y, c in pts]

def sc(pts, k, cx, cy): return [(cx + (x - cx) * k, cy + (y - cy) * k, c) for x, y, c in pts]

def edge_pts(a, b, amp, step):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    n = max(1, round(L / step))
    if L == 0: return []
    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
    out = []
    for i in range(1, n):
        t = i / n; o = J(amp)
        out.append((a[0] + (b[0] - a[0]) * t + nx * o, a[1] + (b[1] - a[1]) * t + ny * o, False))
    return out

def wob(vs, amp=0.6, step=9, closed=True):
    """vs: punti (x,y,corner); sposta un poco ogni vertice e aggiunge punti intermedi ballerini sui lati lunghi."""
    vs = [(x + J(amp * .5), y + J(amp * .5), c) for x, y, c in vs]
    out = []
    n = len(vs)
    for i in range(n if closed else n - 1):
        a = vs[i]; b = vs[(i + 1) % n]
        out.append(a)
        out += edge_pts(a, b, amp, step)
    if not closed: out.append(vs[-1])
    return out

def ell(cx, cy, rx, ry=None, amp=0.5, n=None, rot_deg=0, rev=False):
    ry = rx if ry is None else ry
    n = n or max(8, int(2 * math.pi * max(rx, ry) / 8))
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + J(amp) / max(rx, ry)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a), False))
    if rot_deg: pts = rot(pts, rot_deg, cx, cy)
    return pts[::-1] if rev else pts

def arcpts(cx, cy, r, a0, a1, amp=0.5, step=9):
    n = max(3, int(abs(math.radians(a1 - a0)) * r / step))
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        k = r + (J(amp) if 0 < i < n else 0)
        pts.append((cx + k * math.cos(a), cy + k * math.sin(a), False))
    return pts

def rr(x, y, w, h, r, amp=0.5, step=9):
    """rettangolo con angoli arrotondati ballerino."""
    r = min(r, w / 2, h / 2)
    if r < 1.5:
        return wob(C((x, y), (x + w, y), (x + w, y + h), (x, y + h)), amp, step)
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for k in (0, .5, 1):
            a = math.radians(a0 + 90 * k)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a), False))
    return wob(pts, amp, step)

def cog(cx, cy, r, n=8, prof=0.28, amp=0.15):
    ri = r * (1 - prof); s = 2 * math.pi / n; p = []
    for k in range(n):
        a = k * s - math.pi / 2
        for da, rr_ in ((-0.27, ri), (-0.15, r), (0.15, r), (0.27, ri)):
            p.append((cx + rr_ * math.cos(a + da * s), cy + rr_ * math.sin(a + da * s), True))
    return [(x + J(amp), y + J(amp), c) for x, y, c in p]

def star4(cx, cy, r, ratio=.38):
    return [(cx + (r if k % 2 == 0 else r * ratio) * math.cos(math.pi * k / 4 - math.pi / 2),
             cy + (r if k % 2 == 0 else r * ratio) * math.sin(math.pi * k / 4 - math.pi / 2), True) for k in range(8)]

def lozenge(cx, cy, w, h): return C((cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy))

# ---------------------------------------------------------------- emissione SVG
def f(v): return ('%.2f' % v).rstrip('0').rstrip('.')

def bez(pts, closed=True):
    n = len(pts)
    def P(i): return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    def tan(i):
        a, b = P(i - 1), P(i + 1)
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        return dx / L, dy / L
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n if closed else n - 1):
        a, b = P(i), P(i + 1)
        L = math.hypot(b[0] - a[0], b[1] - a[1]) / 3
        if a[2] or (not closed and i == 0): h1 = (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3)
        else:
            t = tan(i); h1 = (a[0] + t[0] * L, a[1] + t[1] * L)
        if b[2] or (not closed and i + 1 == n - 1): h2 = (b[0] - (b[0] - a[0]) / 3, b[1] - (b[1] - a[1]) / 3)
        else:
            t = tan(i + 1); h2 = (b[0] - t[0] * L, b[1] - t[1] * L)
        d += f'C{f(h1[0])} {f(h1[1])} {f(h2[0])} {f(h2[1])} {f(b[0])} {f(b[1])}'
    return d + ('Z' if closed else '')

def P(pts, closed=True, fill='none', stroke=INK, sw=2.5, extra=''):
    st = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round" stroke-linecap="round"' if stroke != 'none' else ' stroke="none"'
    return f'<path d="{bez(pts, closed)}" fill="{fill}"{st}{extra}/>'

def poly(vs, **k):   # tracciato ballerino chiuso con riempimento
    amp = k.pop('amp', .6); step = k.pop('step', 9)
    return P(wob(vs, amp, step), True, **k)

def line(a, b, stroke=INK, sw=2.5, amp=.4, **k):
    return P(wob(C(a, b), amp, 9, closed=False), False, 'none', stroke, sw, **k)

def disc(cx, cy, r, fill, stroke=INK, sw=2.5, amp=.4, **k):
    return P(ell(cx, cy, r, amp=amp), True, fill, stroke, sw, **k)

def G(name, *els): return f'<g id="{name}">' + ''.join(els) + '</g>'

def svg_doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}pt" height="{f(h)}pt" viewBox="0 0 {f(w)} {f(h)}">{body}</svg>')

# ---------------------------------------------------------------- elementi del kit steampunk
def gear(cx, cy, r, n=8, fill=BRASSL, stroke=BRASS, sw=1.0, hub=True, ring=True, hubcol=BRASS, prof=.28, amp=.15):
    o = [P(cog(cx, cy, r, n, prof, amp), True, fill, stroke, sw)]
    if ring: o.append(P(ell(cx, cy, r * .56, amp=.15, n=12), True, 'none', stroke, sw * .8))
    if hub: o.append(P(ell(cx, cy, r * .22, amp=.1, n=8), True, hubcol, 'none'))
    return ''.join(o)

def rivet(cx, cy, r=1.7, fill=BRASSL, stroke=BRASS, sw=.8):
    return P(ell(cx, cy, r, amp=.08, n=8), True, fill, stroke, sw)

# ---------------------------------------------------------------- 1. cornici pagina
W_A4, H_A4 = 595.28, 841.89

def cornice(rich):
    R.seed(11 if not rich else 12)
    W, H = W_A4, H_A4
    m1, m2 = 18, 23.5
    o = [P(rr(m1, m1, W - 2 * m1, H - 2 * m1, 5, .6, 34), True, 'none', BRASS, 1.6),
         P(rr(m2, m2, W - 2 * m2, H - 2 * m2, 3, .5, 34), True, 'none', BRASS, .7)]
    mm = (m1 + m2) / 2
    cr = 12 if rich else 9.5
    cc = m1 + 3.5
    for (x, y, sx, sy) in ((cc, cc, 1, 1), (W - cc, cc, -1, 1), (cc, H - cc, 1, -1), (W - cc, H - cc, -1, -1)):
        if rich:   # corona piu' ricca: ingranaggio grande + piccolo ingranaggio ingranato verso l'interno
            o.append(gear(x + sx * 11.3, y + sy * 11.3, 5.5, 8))
        o.append(gear(x, y, cr, 10 if rich else 8))
        dist = (46, 62) if not rich else (50, 66, 82)
        for d_ in dist:
            o.append(rivet(x + sx * (d_ - 3.5 + (cr - 9.5) * 1.0), mm, 1.6 if not rich else 1.7))
            o.append(rivet(mm, y + sy * (d_ - 3.5 + (cr - 9.5) * 1.0), 1.6 if not rich else 1.7))
    if rich:       # losanga di rame a meta' di ogni lato, con due rivetti a fianco
        for (x, y, ang) in ((W / 2, mm, 0), (W / 2, H - mm, 0), (mm, H / 2, 90), (W - mm, H / 2, 90)):
            l = rot(lozenge(x, y, 20, 9), ang, x, y)
            o.append(P(wob(l, .1, 20), True, COPPER, BRASS, 1.0))
            for s_ in (-17, 17):
                o.append(rivet(*((x + s_, y) if ang == 0 else (x, y + s_)), 1.5))
    return svg_doc(W, H, G('cornice_pagina_copertina' if rich else 'cornice_pagina', *o))

# ---------------------------------------------------------------- 2. testate (nastro) e filetto
def nastro(name, w, h, cogr, seed, n=12):
    R.seed(seed)
    cy = h / 2
    inset = cogr * .55
    bt = h * .18
    body = P(rr(cogr, bt, w - 2 * cogr, h - 2 * bt, 3, .6, 28), True, PARCH, BRASS, 1.6)
    inner = P(rr(cogr + inset * .55, bt + h * .12, w - 2 * cogr - inset * 1.1, h - 2 * bt - h * .24, 2, .4, 28), True, 'none', BRASS, .7)
    o = [body, inner]
    # linguette: due rivetti per estremita'
    for x in (cogr, w - cogr):
        o.append(gear(x, cy, cogr, n, prof=.22, sw=1.5))
    return svg_doc(w, h, G(name, *o))

def filetto():
    R.seed(31)
    W, H = 400, 14; cy = 7
    o = []
    for x0, x1 in ((10, 172), (228, 390)):
        o.append(P(wob(C((x0, cy), (x1, cy)), .5, 16, False), False, 'none', BRASS, 1.4))
        o.append(P(wob(C((x0 + (8 if x0 < 100 else 0), cy + 3.2), (x1 - (0 if x0 < 100 else 8), cy + 3.2)), .35, 16, False), False, 'none', BRASS, .6))
    for x in (4, 396): o.append(P(ell(x, cy, 2.2, amp=.1, n=8), True, COPPER, 'none'))
    for x in (186, 214): o.append(P(lozenge(x, cy, 9, 7), True, COPPER, BRASS, .9))
    o.append(gear(200, cy, 6.5, 8, sw=1.1, ring=False))
    return svg_doc(W, H, G('filetto', *o))

# ---------------------------------------------------------------- 4. riquadro nota
def riquadro(name, border, seed):
    R.seed(seed)
    W, H = 240, 140
    o = [P(rr(3, 3, W - 6, H - 6, 10, .7, 30), True, PARCH, border, 3.0),
         P(rr(9, 9, W - 18, H - 18, 6, .5, 30), True, 'none', BRASS, .8)]
    for x, y in ((15, 15), (W - 15, 15), (15, H - 15), (W - 15, H - 15)):
        o.append(rivet(x, y, 3.2, BRASSL, BRASS, 1.0))
    return svg_doc(W, H, G(name, *o))

# ---------------------------------------------------------------- 6. numeri passo
def numero(n):
    R.seed(60 + n)
    s = 40
    o = [P(cog(20, 20, 19.2, 10, .2, .15), True, BRASSL, BRASS, 1.6),
         P(ell(20, 20, 13, amp=.15, n=14), True, GOLDL, BRASS, 1.2)]
    txt = f'<text id="numero" x="20" y="26.4" text-anchor="middle" font-family="Noto Serif" font-weight="700" font-size="18" fill="{INK}">{n}</text>'
    return svg_doc(s, s, G(f'numeri_passo_{n}', *o) + txt)

# ---------------------------------------------------------------- 5. icone 64x64
def ring_arrow(cx, cy, r, a0, a1, col, band=8, inner=3, hw=8.5, hl=12):
    pts = arcpts(cx, cy, r, a0, a1, .45, 8)
    th = math.radians(a1)
    ex, ey = cx + r * math.cos(th), cy + r * math.sin(th)
    tx, ty = -math.sin(th), math.cos(th); nx, ny = math.cos(th), math.sin(th)
    head = C((ex + tx * hl, ey + ty * hl), (ex + nx * hw - tx * 2, ey + ny * hw - ty * 2), (ex - nx * hw - tx * 2, ey - ny * hw - ty * 2))
    return (P(pts, False, 'none', INK, band) + P(pts, False, 'none', col, inner) + P(wob(head, .3, 20), True, col, INK, 2.5))

def ic_d6():
    sh = rot(rr(14, 14, 40, 40, 8, .3, 12), -8, 32, 32)
    fr = rot(rr(9, 9, 40, 40, 8, .3, 12), -8, 32, 32)
    o = [P(sh, True, PARCH, INK, 2.5), P(fr, True, PAPER, INK, 2.5)]
    for dx, dy, col in ((-10, -10, INK), (10, -10, INK), (0, 0, RED), (-10, 10, INK), (10, 10, INK)):
        x, y = 29 + dx, 29 + dy
        (x, y, _), = rot([(x, y, False)], -8, 29 + 3, 29 + 3)
        o.append(disc(x, y, 3.8, col, INK, 1.2, .2))
    return G('ic_d6', *o)

def ic_ar():
    shield = [(11, 9, True), (32, 13, False), (53, 9, True), (54, 30, False), (47, 45, False), (32, 59, True), (17, 45, False), (10, 30, False)]
    inner = sc(shield, .74, 32, 33)
    o = [poly(shield, fill=BLUE, amp=.6, step=10), P(wob(inner, .4, 10), True, 'none', GOLDL, 2.2)]
    o.append(P(lozenge(32, 33, 14, 18), True, GOLDL, INK, 2.2))
    for x, y in ((17, 17), (47, 17), (14, 33), (50, 33)):
        o.append(disc(x, y, 2.4, GOLDL, INK, 1.4, .1))
    return G('ic_ar', *o)

def ic_indizio():
    # il rotolo: foglio di pergamena con i due rulli ai lati
    o = [poly(C((9, 14), (47, 14), (47, 50), (9, 50)), fill=PARCH, amp=.6, step=10),
         poly(S((3, 12), (9, 9), (15, 12), (15, 52), (9, 55), (3, 52)), fill=BRASSL, amp=.4, step=10),
         poly(S((41, 12), (47, 9), (53, 12), (53, 52), (47, 55), (41, 52)), fill=BRASSL, amp=.4, step=10),
         line((20, 25), (40, 25)), line((20, 35), (36, 35)), line((20, 44), (40, 44))]
    o.append(disc(39, 34, 12, PAPER, INK, 2.5))
    o.append(line((47.5, 43), (58, 55), INK, 8)); o.append(line((47.5, 43), (58, 55), BROWN, 3))
    o.append(line((34, 29), (44, 39), RED, 2.5)); o.append(line((44, 29), (34, 39), RED, 2.5))
    return G('ic_indizio', *o)

def ic_carta():
    card = rot(rr(16, 7, 32, 50, 4.5, .5, 10), 7, 32, 32)
    rule = rot(rr(20.5, 11.5, 23, 41, 2.5, .3, 10), 7, 32, 32)
    (cx, cy, _), = rot([(32, 32, False)], 7, 32, 32)
    o = [P(card, True, BLUE, INK, 2.5), P(rule, True, 'none', GOLDL, 1.6),
         P(cog(cx, cy, 10, 8, .28, .2), True, GOLDL, INK, 2.2), disc(cx, cy, 3, INK, 'none', 0, .1)]
    return G('ic_carta', *o)

def ic_mano10():
    cols = (RED, BLUE, GREEN, VIOLET, GOLD)
    o = []
    for k, ang in enumerate((-28, -14, 0, 14, 28)):
        card = rot(rr(23.5, 18, 17, 36, 3, .3, 14), ang, 32, 62)
        o.append(P(card, True, PAPER, INK, 2.5))
        o.append(P(rot(lozenge(27.5, 26, 4.5, 7), ang, 32, 62), True, cols[k], INK, 1.3))
    o.append(disc(32, 59, 3.6, GOLDL, INK, 2.2, .1))
    return G('ic_mano10', *o)

def ic_teschio():
    sk = [(32, 6, False), (47, 11, False), (53, 25, False), (47, 38, False), (45, 43, True), (44, 56, True),
          (20, 56, True), (19, 43, True), (17, 38, False), (11, 25, False), (17, 11, False)]
    o = [poly(sk, fill=PAPER, amp=.6, step=10),
         disc(23, 28, 7, INK, 'none', 0, .3), disc(41, 27, 5, INK, 'none', 0, .3),
         disc(21, 25.5, 1.8, PAPER, 'none', 0, .1), disc(39.5, 25.5, 1.3, PAPER, 'none', 0, .1),
         P(C((32, 34), (28.5, 41), (35.5, 41)), True, INK, INK, 1.5),
         poly(C((32, 49), (38, 49), (38, 56), (32, 56)), fill=GOLD, stroke='none', sw=0, amp=.1)]
    o.append(line((26, 49), (26, 56), INK, 2.5)); o.append(line((32, 49), (32, 56), INK, 2.5)); o.append(line((38, 49), (38, 56), INK, 2.5))
    o.append(line((44, 11), (40, 17), INK, 2)); o.append(line((40, 17), (43, 21), INK, 2))
    return G('ic_teschio', *o)

def ic_respawn():
    o = [ring_arrow(32, 33, 24, -60, 215, BLUE)]
    o.append(P(wob(S((21, 47), (29, 49), (38, 47), (29, 45)), .3, 10), True, GREEN, INK, 2.5))
    o.append(line((29, 47), (29, 19), INK, 2.5))
    o.append(poly(C((29.5, 19), (46, 25), (29.5, 32)), fill=RED, amp=.3, step=20))
    return G('ic_respawn', *o)

def ic_rotella():
    o = [P(cog(32, 34, 27, 24, .07, .25), True, PARCH, INK, 2.5)]
    for k in range(7):
        a = math.radians(45 + 45 * k)
        o.append(disc(32 + 18 * math.sin(a), 34 - 18 * math.cos(a), 1.9, INK, 'none', 0, .1))
    o.append(P(rr(24.5, 8.5, 15, 11, 2.5, .3, 10), True, PAPER, INK, 2.5))
    o.append(P(wob(lozenge(32, 14, 6, 6), .2, 10), True, RED, 'none', 0))
    o.append(disc(32, 36, 6, GOLDL, INK, 2.5, .15))
    return G('ic_rotella', *o)

def ic_segnalino():
    back = disc(37, 37, 22, BLUE, INK, 2.5, .5)
    front = disc(27, 27, 22, PARCH, INK, 2.5, .5)
    ring = P(ell(27, 27, 16, amp=.3), True, 'none', BROWN, 1.8, ' stroke-dasharray="3 3.6"')
    star = P(wob(star4(27, 27, 11, .4), .2, 20), True, RED, INK, 2.2)
    return G('ic_segnalino', back, front, ring, star)

def ic_mostro():
    head = [(32, 11, False), (47, 16, False), (55, 32, False), (52, 48, False), (40, 57, False), (24, 57, False),
            (12, 48, False), (9, 32, False), (17, 16, False)]
    horns = [poly(C((15, 24), (8, 5), (28, 15)), fill=PARCH, amp=.3, step=20),
             poly(C((49, 24), (56, 5), (36, 15)), fill=PARCH, amp=.3, step=20)]
    mouth = [(16, 42, True), (32, 45, False), (48, 42, True), (45, 51, False), (32, 56, False), (19, 51, False)]
    o = horns + [poly(head, fill=GREEN, amp=.6, step=10),
                 disc(24, 30, 7.5, PAPER, INK, 2.5, .2), disc(25.5, 31.5, 3.2, INK, 'none', 0, .1),
                 disc(41, 28, 4.8, PAPER, INK, 2.2, .1), disc(41.5, 28.5, 2, INK, 'none', 0, .1),
                 poly(mouth, fill=INK, stroke=INK, amp=.4, step=10),
                 P(C((21, 43), (26, 43), (23.5, 49)), True, PAPER, 'none', 0),
                 P(C((29, 44.5), (35, 44.5), (32, 50.5)), True, PAPER, 'none', 0),
                 P(C((38, 43), (43, 43), (40.5, 49)), True, PAPER, 'none', 0),
                 P(C((26, 56), (31, 51.5), (35, 56)), True, RED, 'none', 0)]
    return G('ic_mostro', *o)

def ic_tesoro():
    body = poly(C((8, 30), (50, 30), (50, 54), (8, 54)), fill=BROWN, amp=.5, step=10)
    lid = poly([(8, 30, True), (10, 20, False), (18, 13, False), (29, 10, False), (40, 13, False), (48, 20, False), (50, 30, True)], fill=COPPER, amp=.5, step=10)
    o = [body, lid,
         poly(C((8, 28), (50, 28), (50, 34), (8, 34)), fill=GOLD, amp=.2, step=12),
         poly(C((23, 28), (35, 28), (35, 42), (23, 42)), fill=GOLD, amp=.2, step=12),
         disc(29, 36, 2.6, INK, 'none', 0, .1), line((29, 36), (29, 40), INK, 2.5),
         disc(54, 51, 6.5, GOLDL, INK, 2.5, .3), P(wob(star4(54, 51, 3.2, .45), .1, 20), True, GOLD, 'none', 0)]
    return G('ic_tesoro', *o)

def ic_movimento():
    boot = [(20, 7, True), (37, 7, True), (37, 32, False), (50, 38, False), (57, 44, False), (57, 54, True), (17, 54, True), (17, 40, False), (20, 30, False)]
    o = [poly(boot, fill=COPPER, amp=.5, step=10),
         poly(C((20, 7), (37, 7), (37, 16), (20, 16)), fill=BRASSL, amp=.3, step=12),
         poly(C((17, 48), (57, 48), (57, 56), (17, 56)), fill=BROWN, amp=.3, step=12),
         line((37, 22), (30, 24)), line((37, 29), (30, 31))]
    for y in (22, 32, 42): o.append(line((3, y), (11, y), INK, 2.5))
    return G('ic_movimento', *o)

def ic_esagono():
    hx = [(32 + 28 * math.cos(math.radians(a)), 32 + 28 * math.sin(math.radians(a)), True) for a in (-90, -30, 30, 90, 150, 210)]
    inner = sc(hx, .76, 32, 32)
    o = [poly(hx, fill=PARCH, amp=.5, step=12), P(wob(inner, .3, 12), True, 'none', BRASS, 1.6),
         poly(C((18, 43), (31, 16), (44, 43)), fill=BROWN, amp=.4, step=12),
         poly(C((26, 28), (31, 16), (36, 28), (33, 26), (30, 29)), fill=PAPER, stroke='none', sw=0, amp=.1, step=20),
         disc(47, 45, 4.8, GREEN, INK, 2, .2)]
    return G('ic_esagono', *o)

def ic_oracolo():
    o = [disc(32, 28, 21, VIOLET, INK, 2.5, .4)]
    o.append(P(wob(C((17, 58), (47, 58), (42, 46), (22, 46)), .3, 12), True, GOLD, INK, 2.5))
    o.append(P(wob(star4(30, 29, 8, .35), .15, 20), True, GOLDL, INK, 1.6))
    o.append(P(wob(star4(42, 18, 4, .4), .1, 20), True, GOLDL, 'none', 0))
    o.append(P(arcpts(32, 28, 15, 195, 255, .2, 6), False, 'none', PAPER, 2.5))
    return G('ic_oracolo', *o)

def ic_equip():
    # spada disegnata in orizzontale (impugnatura a sinistra) poi ruotata quasi in verticale
    ang, tx, ty = -80, 49, 49
    def T(p): return mv(rot(p, ang, 0, 0), tx, ty)
    o = [poly(T(C((8, -4.5), (40, -4.5), (48, 0), (40, 4.5), (8, 4.5))), fill=PAPER, amp=.3, step=14),
         poly(T(C((6, -11), (10.5, -11), (10.5, 11), (6, 11))), fill=GOLD, amp=.25, step=14),
         poly(T(C((-5, -2.6), (6, -2.6), (6, 2.6), (-5, 2.6))), fill=BROWN, amp=.25, step=14)]
    (px, py, _), = T([(-8, 0, False)])
    o.append(disc(px, py, 3.4, GOLD, INK, 2.2, .1))
    helm = [(4, 58, True), (4, 40, False), (9, 29, False), (20, 24, False), (31, 29, False), (36, 40, False), (36, 58, True)]
    o += [poly(helm, fill=BLUE, amp=.5, step=10),
          poly(C((4, 49), (36, 49), (36, 58), (4, 58)), fill=BRASSL, amp=.3, step=12),
          line((9, 38), (31, 38), INK, 2.5), line((20, 38), (20, 49), INK, 2.5)]
    o += [disc(x, 53.5, 1.4, INK, 'none', 0, .05) for x in (10, 20, 30)]
    o.append(P(wob(S((20, 24), (20, 17), (27, 12), (33, 14), (28, 19), (27, 26)), .3, 12), True, RED, INK, 2.2))
    return G('ic_equip', *o)

def ic_stack():
    cards = []
    for y, col, tilt in ((41, GREEN, -5), (34, VIOLET, 4), (27, BLUE, -1)):
        cards.append(P(rot(rr(8, y, 44, 21, 3.5, .3, 14), tilt, 30, y + 10.5), True, col, INK, 2.5))
    o = cards + [gear(30, 37.5, 5.5, 8, GOLDL, INK, 1.6, ring=False, hubcol=INK)]
    # frecce: una entra (rosso) e una esce (verde) dalla cima della pila: ultima entrata, prima uscita
    o += [line((17, 4), (17, 18), INK, 2.5), poly(C((10.5, 15), (23.5, 15), (17, 24)), fill=RED, amp=.2, step=20),
          line((43, 24), (43, 10), INK, 2.5), poly(C((36.5, 13), (49.5, 13), (43, 4)), fill=GREEN, amp=.2, step=20)]
    return G('ic_stack', *o)

def ic_turno():
    o = [ring_arrow(32, 32, 25.5, -72, 218, BRASS)]
    o.append(disc(32, 32, 7.5, COPPER, INK, 2.5, .2))
    for a, col in ((45, BLUE), (135, RED), (225, GREEN), (315, VIOLET)):
        r_ = math.radians(a)
        o.append(disc(32 + 14.5 * math.cos(r_), 32 + 14.5 * math.sin(r_), 4.8, col, INK, 2.2, .1))
    return G('ic_turno', *o)

ICONS = ['ic_d6', 'ic_ar', 'ic_indizio', 'ic_carta', 'ic_mano10', 'ic_teschio', 'ic_respawn', 'ic_rotella', 'ic_segnalino',
         'ic_mostro', 'ic_tesoro', 'ic_movimento', 'ic_esagono', 'ic_oracolo', 'ic_equip', 'ic_stack', 'ic_turno']

# ---------------------------------------------------------------- pipeline VectorCraft
def vc(*args):
    r = subprocess.run(['vectorcraft-cli', *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'vectorcraft-cli {" ".join(args)}\n{r.stdout}\n{r.stderr}')
    return r.stdout

def build():
    jobs = {}   # nome -> (w, h, svg)
    jobs['cornice_pagina'] = (W_A4, H_A4, cornice(False))
    jobs['cornice_pagina_copertina'] = (W_A4, H_A4, cornice(True))
    jobs['testata'] = (480, 50, nastro('testata', 480, 50, 20, 21, 12))
    jobs['testatina'] = (260, 32, nastro('testatina', 260, 32, 13, 22, 10))
    jobs['filetto'] = (400, 14, filetto())
    jobs['riquadro_nota_esempio'] = (240, 140, riquadro('riquadro_nota_esempio', BRASS, 41))
    jobs['riquadro_nota_attenzione'] = (240, 140, riquadro('riquadro_nota_attenzione', RED, 42))
    for i, fn in enumerate(ICONS):
        R.seed(100 + i)
        body = globals()[fn]()
        jobs[fn] = (64, 64, svg_doc(64, 64, body))
    for n in range(1, 9):
        jobs[f'numeri_passo_{n}'] = (40, 40, numero(n))
    return jobs

def main():
    os.makedirs(os.path.join(OUT, 'sorgenti'), exist_ok=True)
    jobs = build()
    for name, (w, h, svg) in jobs.items():
        src = os.path.join(TMP, name + '.svg'); open(src, 'w').write(svg)
        vcs = os.path.join(HERE, name + '.vectorcraft')
        if name.startswith('numeri_passo'):   # i numeri diventano tracciati (Noto Serif Bold) prima di salvare
            vc('run', '--in', src, '--cmd', 'select.all', '--cmd', 'type.createOutlines', '--export', vcs)
        else:
            vc('convert', src, vcs)
        dst = os.path.join(OUT, name + '.svg')
        vc('convert', vcs, dst, '--outline-text', '--decimals', '2')
        t = open(dst).read()   # unita' esplicite in pt (altrimenti 1 unita' = 1 px = 0,75 pt in DesignCraft)
        t = re.sub(r'<svg ([^>]*?)width="([\d.]+)" height="([\d.]+)"', r'<svg \1width="\2pt" height="\3pt"', t, count=1)
        open(dst, 'w').write(t)
        vc('convert', vcs, os.path.join(OUT, name + '.pdf'))
        print(name, w, h)

def anteprima():
    """anteprima.png: tutto su fondo Carta, renderizzato da VectorCraft dagli SVG finali."""
    png = os.path.join(TMP, 'png'); os.makedirs(png, exist_ok=True)
    def img(name, scale):
        p = os.path.join(png, f'{name}.png')
        vc('convert', os.path.join(OUT, name + '.svg'), p, '--scale', str(scale))
        return p
    cmd = ['magick', '-size', '1500x1080', f'xc:{PAPER}', '-font', FONT_LABEL, '-pointsize', '13', '-fill', INK]
    def put(name, scale, x, y, label=True):
        cmd.extend(['(', img(name, scale), ')', '-geometry', f'+{x}+{y}', '-composite'])
    put('cornice_pagina', .5, 30, 40); put('cornice_pagina_copertina', .5, 350, 40)
    put('testata', 1, 700, 40); put('testatina', 1, 700, 110); put('filetto', 1, 700, 160)
    put('riquadro_nota_esempio', 1, 700, 200); put('riquadro_nota_attenzione', 1, 960, 200)
    for n in range(1, 9): put(f'numeri_passo_{n}', 2, 700 + (n - 1) * 95, 370)
    for i, fn in enumerate(ICONS):
        x, y = 30 + (i % 7) * 200, 500 + (i // 7) * 180
        put(fn, 2.5, x, y)
        cmd.extend(['-annotate', f'+{x}+{y + 172}', fn])
    cmd.append(os.path.join(OUT, 'anteprima.png'))
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()
    anteprima()
