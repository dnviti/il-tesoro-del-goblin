#!/usr/bin/env python3
"""Genera le pagine (SVG in mm) dei componenti non-carta del playtest v7, tutti SOLO FRONTE.

Uso: python3 gen.py <cartella_uscita> [--formato A3]
Scrive <cartella_uscita>/<componente>/pagina_NN.svg (poi importate in VectorCraft e esportate in PDF da build.sh).
A4: plancia (4 fogli), plance_eroe (4, A4 orizzontale), rotelle_eroe (2), tessere_esplorazione (1), segnalini (2),
pedine (2), prova_stampa (1). A3: plancia (2), plance_eroe (2), rotelle_eroe (1), tessere_esplorazione (1, con le
tessere Stato e la Rotella della Profezia), componenti_misti (1, pedine e segnalini), prova_stampa (1).
v7: plance eroe neutre (D14: niente classe né specie stampate), rotella PL 0-12 al posto di PE/livello (D2), pedina del
Giullare (5 classi), plancia = bozza v7/idee/v7_bozza_mappa.svg (D16, vedi svg.board()).
Dipende da svg.py + parts_stampa.py (plancia, icone, corone delle rotelle), dai CSV in dati/ e, per l'elenco dei file
della prova di stampa, da ../carte/genera_carte.py (conta i fogli delle carte). Prima di scrivere controlla che ogni
finestra delle rotelle mostri un solo valore (verifica_rotella).
"""
import csv, math, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import ImageFont
from parts_stampa import *   # icon, board, dial_ring, colori INK/BROWN/RED/GOLD/BLUE/PAPER...

OUT = sys.argv[1]
# --dati CARTELLA: CSV da un'altra cartella (vale anche per genera_carte.py, che la prova di stampa importa per contare i fogli)
DATI = sys.argv[sys.argv.index('--dati') + 1] if '--dati' in sys.argv else os.path.join(HERE, '..', 'dati')
SERIF = 'Liberation Serif'          # al posto di Cinzel (titoli): ha >= e -> e pesi veri
SANS = 'Liberation Sans Narrow'     # al posto di Alegreya Sans (etichette)
FDIR = {'Liberation Serif': '/usr/share/fonts/liberation-serif-fonts/LiberationSerif-%s.ttf',
        'Liberation Sans Narrow': '/usr/share/fonts/liberation-narrow/LiberationSansNarrow-%s.ttf'}
_fc = {}
def tw(text, size_mm, fam=SANS, bold=False):
    """larghezza in mm del testo (misurata sul font vero)."""
    key = (fam, bold)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FDIR[fam] % ('Bold' if bold else 'Regular'), 100)
    return _fc[key].getlength(text) * size_mm / 100.0

def wrap(text, size_mm, maxw, fam=SANS, bold=False):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tw(t, size_mm, fam, bold) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    assert ' '.join(lines) == text
    return lines

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def fonts(s):
    return (s.replace('font-family="Cinzel"', f'font-family="{SERIF}"')
             .replace('font-family="Alegreya Sans"', f'font-family="{SANS}"')
             .replace('font-weight="800"', 'font-weight="bold"').replace('font-weight="700"', 'font-weight="bold"'))

def inner(svg):
    return re.sub(r'^<svg[^>]*>', '', svg.strip()).rsplit('</svg>', 1)[0]

def page(body, w=210, h=297):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" '
            f'font-family="{SANS}">\n{body}\n</svg>\n')

def text(x, y, s, size, fill=INK, anchor='start', bold=False, fam=SANS, italic=False, extra=''):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size:.2f}" fill="{fill}" '
            f'text-anchor="{anchor}"{" font-weight=\"bold\"" if bold else ""}{" font-style=\"italic\"" if italic else ""} {extra}>{esc(s)}</text>')

def line(x1, y1, x2, y2, sw=0.15, col='#000', dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="{sw}"{d}/>'

def crop_marks(x0, y0, x1, y1, gap=4, ln=3.5):
    o = []
    for x in (x0, x1):
        o.append(line(x, y0 - gap - ln, x, y0 - gap)); o.append(line(x, y1 + gap, x, y1 + gap + ln))
    for y in (y0, y1):
        o.append(line(x0 - gap - ln, y, x0 - gap, y)); o.append(line(x1 + gap, y, x1 + gap + ln, y))
    return '<g id="crop-marks">' + ''.join(o) + '</g>'

def edge_ticks(xs, ys, bbox, gap=4, ln=3.5):
    """tacche di taglio fuori dal rettangolo bbox per ogni coordinata di taglio."""
    x0, y0, x1, y1 = bbox
    o = []
    for x in xs:
        o.append(line(x, y0 - gap - ln, x, y0 - gap)); o.append(line(x, y1 + gap, x, y1 + gap + ln))
    for y in ys:
        o.append(line(x0 - gap - ln, y, x0 - gap, y)); o.append(line(x1 + gap, y, x1 + gap + ln, y))
    return '<g id="tacche-di-taglio">' + ''.join(o) + '</g>'

BLEED = 3.0
CUT = '#222222'
_puliti = set()
def write(comp, n, svg):
    d = os.path.join(OUT, comp); os.makedirs(d, exist_ok=True)
    if d not in _puliti:   # alla prima pagina del componente: via le pagine vecchie (build.sh prende tutte le pagina_*.svg)
        _puliti.add(d)
        for f in os.listdir(d):
            if f.startswith('pagina_') and f.endswith(('.svg', '.vectorcraft')): os.remove(os.path.join(d, f))
    p = os.path.join(d, f'pagina_{n:02d}.svg'); open(p, 'w', encoding='utf-8').write(svg); return p

def hdr(title, sub, y=11):
    return text(105, y, title, 4.2, INK, 'middle', True, SERIF) + text(105, y + 5, sub, 2.9, BROWN, 'middle')
def ftr(lines, y=283):
    return ''.join(text(105, y + i * 3.6, l, 2.8, BROWN, 'middle') for i, l in enumerate(lines))

def read(name): return list(csv.DictReader(open(os.path.join(DATI, name), encoding='utf-8')))

def mix(h, f):  # schiarisce un esadecimale mescolando col bianco
    r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    r, g, b = [round(v + (255 - v) * f) for v in (r, g, b)]
    return f'#{r:02x}{g:02x}{b:02x}'

# ------------------------------------------------------------------ pezzi tondi
def disc_piece(cx, cy, R, fill, ic, label, icol, lcol, ks=1.0):
    """tessera/segnalino tondo, come color_token()/simple_token() ma in mm; R = raggio di taglio."""
    s = 2 * R; k = 0.9 * s / 46 * ks
    sw = 0.043 * s
    o = []
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R - sw / 2:.2f}" fill="{fill}" stroke="{BROWN}" stroke-width="{sw:.2f}"/>')
    o.append(icon(ic, cx, cy - R + R * 0.85, k, icol))
    fs = 0.15 * s
    while tw(label, fs, SANS, True) > 0.66 * s: fs -= 0.05
    o.append(text(cx, cy - R + 0.86 * s, label, fs, lcol, 'middle', True))
    return ''.join(o)

def bleed_disc(cx, cy, R, fill): return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R + BLEED:.2f}" fill="{fill}"/>'
def cut_disc(cx, cy, R): return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="none" stroke="{CUT}" stroke-width="0.12" opacity="0.7"/>'

def disc_grid(n, cols, d, page_h=297):
    """posizioni dei centri: pitch d+2*BLEED, griglia centrata nella pagina; ritorna (centri, bbox, pitch)."""
    pitch = d + 2 * BLEED
    rows = math.ceil(n / cols)
    gw, gh = (cols - 1) * pitch + d, (rows - 1) * pitch + d
    x0 = (210 - gw) / 2; y0 = (page_h - gh) / 2
    cs = [(x0 + d / 2 + (i % cols) * pitch, y0 + d / 2 + (i // cols) * pitch) for i in range(n)]
    return cs, (x0, y0, x0 + gw, y0 + gh), pitch

# ------------------------------------------------------------------ TESSERE ESPLORAZIONE
def esplorazione_pezzi(cs, rows, D):
    R = D / 2
    b = [bleed_disc(x, y, R, r['colore_esadecimale']) for (x, y), r in zip(cs, rows)]
    b += [disc_piece(x, y, R, r['colore_esadecimale'], r['icona'], r['etichetta_fronte'], '#ffffff', '#ffffff') for (x, y), r in zip(cs, rows)]
    b += [cut_disc(x, y, R) for x, y in cs]
    return b

ESPL_NOTE = ['Retro bianco, niente sacchetto: le tessere stanno coperte sulle «?» e nella riserva; la tessera rossa rimasta sulla plancia sta a faccia in su.',
             'Ordine: le prime 25 (righe 1-4 e la prima della riga 5) sono rosse, le altre 11 blu.']
def esplorazione():
    """36 tessere Ø 24 su un foglio A4, solo fronte (retro bianco)."""
    rows = read('tessere_esplorazione.csv')
    assert len(rows) == 36
    D = 24; n = len(rows); cols = 6       # esagono della plancia = 25,2 mm da lato a lato: la tessera ci sta dentro
    cs, bbox, pitch = disc_grid(n, cols, D)
    rws = math.ceil(n / cols)
    b = esplorazione_pezzi(cs, rows, D)
    xs = sorted({bbox[0] + i * pitch + o for i in range(cols) for o in (0, D)})
    ys = sorted({bbox[1] + i * pitch + o for i in range(rws) for o in (0, D)})
    b.append(edge_ticks(xs, ys, bbox))
    b.insert(0, hdr(f'Tessere Esplorazione · 25 rosse (Mostro) + 11 blu (Imprevisto) · Ø {D} mm', 'Solo fronte: un foglio, retro bianco.'))
    b.append(ftr(['Stampa su A4 al 100% (nessun adattamento alla pagina), solo fronte. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.'] + ESPL_NOTE))
    write('tessere_esplorazione', 1, page(fonts('\n'.join(b))))
    return dict(Counter(r['colore'] for r in rows))

# ------------------------------------------------------------------ SEGNALINI (Ø 20) E TESSERE STATO (26 x 18)
SEGN = {'Indizio': ('pergamena', INK, '#efe1c3', 'Indizio'),
        'Forte Volontà': ('stella', GOLD, '#efe1c3', 'Forte Volontà'),
        'Usato': ('spunta', '#2f6b3f', '#dcebd8', 'USATO')}
def gettoni(cols, x0, y0, per_tipo=True):
    """segnalini tondi Ø 20 a partire da (x0, y0); per_tipo: ogni tipo comincia una riga nuova. Ritorna (svg, conteggi, bbox)."""
    rows = read('segnalini.csv')
    items = [r['nome'] for r in rows for _ in range(int(r['copie']))]
    assert set(items) == set(SEGN)
    D = 20; R = D / 2; pitch = D + 2 * BLEED
    layout = []
    if per_tipo:
        row = 0
        for r in rows:
            n = int(r['copie'])
            layout += [(r['nome'], row + i // cols, i % cols) for i in range(n)]
            row += math.ceil(n / cols)
    else:
        layout = [(nm, i // cols, i % cols) for i, nm in enumerate(items)]
    nrows = max(rr for _, rr, _ in layout) + 1
    gw = (cols - 1) * pitch + D; gh = (nrows - 1) * pitch + D
    pos = [(nm, x0 + R + cc * pitch, y0 + R + rr * pitch) for nm, rr, cc in layout]
    b = [bleed_disc(x, y, R, SEGN[nm][2]) for nm, x, y in pos]
    for nm, x, y in pos:
        ic, col, fill, lab = SEGN[nm]
        b.append(disc_piece(x, y, R, fill, ic, lab, col, INK, 1.2))
    b += [cut_disc(x, y, R) for _, x, y in pos]
    xs = sorted({x0 + i * pitch + o for i in range(cols) for o in (0, D)}); ys = sorted({y0 + i * pitch + o for i in range(nrows) for o in (0, D)})
    bb = (x0, y0, x0 + gw, y0 + gh)
    b.append(edge_ticks(xs, ys, bb))
    return b, dict(Counter(items)), bb

STATO_COL = {'+': '#3b7d4f', '−': '#9c2f24'}
ST_W, ST_H = 26.0, 18.0
def stati(cols, x0, y0):
    """tessere Stato 26 x 18 (bandella verde = +, rossa = −; freccia ↑ per leggere dritto/di traverso). Ritorna (svg, conteggi, bbox)."""
    rows = read('stati.csv')
    items = [r for r in rows for _ in range(int(r['copie']))]
    assert items
    px, py = ST_W + 2 * BLEED, ST_H + 2 * BLEED
    nr = math.ceil(len(items) / cols)
    gw, gh = (cols - 1) * px + ST_W, (nr - 1) * py + ST_H
    pcs = [(x0 + (i % cols) * px, y0 + (i // cols) * py, r) for i, r in enumerate(items)]
    b = []
    for x, y, r in pcs:
        c = STATO_COL[r['segno']]
        b.append(f'<rect x="{x - BLEED:.2f}" y="{y - BLEED:.2f}" width="{ST_W + 2 * BLEED}" height="{ST_H + 2 * BLEED}" fill="{mix(c, 0.86)}"/>')
        b.append(f'<rect x="{x - BLEED:.2f}" y="{y - BLEED:.2f}" width="{ST_W + 2 * BLEED}" height="{BLEED + 6.2}" fill="{c}"/>')
        b.append(text(x + 2.4, y + 4.9, r['segno'], 4.2, '#ffffff', 'middle', True))
        fs = 3.4
        while tw(r['nome'], fs, SANS, True) > 15.5: fs -= 0.1
        b.append(text(x + ST_W / 2, y + 4.6, r['nome'], fs, '#ffffff', 'middle', True))
        ax = x + ST_W - 2.4   # freccia ↑: la tessera è dritta quando punta in alto
        b.append(f'<path d="M{ax:.2f} {y + 5.3:.2f}V{y + 1.3:.2f}M{ax - 1.2:.2f} {y + 2.6:.2f}L{ax:.2f} {y + 1.2:.2f}L{ax + 1.2:.2f} {y + 2.6:.2f}" fill="none" stroke="#ffffff" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round"/>')
        fs = 2.8   # testo grande quanto entra in 3 righe, senza una parola sola sull'ultima riga
        ls = wrap(r['testo'], fs, ST_W - 2.6)
        while len(ls) > 3 or (len(ls) > 1 and len(ls[-1]) < 4): fs -= 0.05; ls = wrap(r['testo'], fs, ST_W - 2.6)
        for j, l in enumerate(ls):
            b.append(text(x + ST_W / 2, y + 9.7 + j * fs * 1.18, l, fs, INK, 'middle'))
        b.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{ST_W}" height="{ST_H}" rx="1.2" fill="none" stroke="{CUT}" stroke-width="0.12" opacity="0.8"/>')
    xs = sorted({x0 + i * px + o for i in range(cols) for o in (0, ST_W)}); ys = sorted({y0 + i * py + o for i in range(nr) for o in (0, ST_H)})
    bb = (x0, y0, x0 + gw, y0 + gh)
    b.append(edge_ticks(xs, ys, bb).replace('tacche-di-taglio', 'tacche-stati'))
    return b, dict(Counter(r['nome'] for r in items)), bb

# ------------------------------------------------------------------ ROTELLE (volvelle)
# Corona dei valori stampata sulla plancia (svg.dial_ring), disco Ø 52 stampato a parte con una finestra a RING_R dal
# centro: girando il disco la finestra mostra un solo valore. Ogni rotella: (chiave, nome sul disco, sotto, icona,
# colore sulla plancia, valori, finestra (larga lungo la corona, alta lungo il raggio), altezza delle cifre, dorati, rossi).
# PL (D2, Spec R 2.3): somma dei PL degli Equipaggiamenti negli slot, 0-12, senza scritte di livello né di mazzetto.
# PV max (Spec R 2.3): ogni valore da 5 a 13, perché le carte cambiano i PV massimi di 1 alla volta.
ROTELLE = [
    ('PV', 'PV', 'attuali', 'cuore', RED, [(str(v), ()) for v in range(14)], (9.0, 9.0), 4.0, (), (0,)),
    ('PVM', 'PV max', 'massimi', 'cuore', INK, [(str(v), ()) for v in range(5, 14)], (11.0, 9.0), 4.5, (), ()),
    ('ATT', 'ATT', 'attacco', 'spade', INK, [(str(v), ()) for v in range(1, 9)], (11.0, 9.0), 4.5, (), ()),
    ('MOV', 'MOV', 'movimento', 'stivale', BROWN, [('−1' if v < 0 else str(v), ()) for v in range(-1, 9)], (11.0, 9.0), 4.5, (), ()),
    ('AR', 'AR', 'armatura', 'scudo', BLUE, [(str(v), ()) for v in range(9, 21)], (11.0, 9.0), 4.5, (), ()),
    ('PL', 'PL', 'power level', 'stella', GOLD, [(str(v), ()) for v in range(13)], (9.0, 9.0), 4.2, (), ())]
R_TAVOLO = [('scontro', 'PV del mostro', 'Rotella dello scontro', 'teschio', '#a8352a'),
            ('custode', 'PV del custode', 'le ferite restano', 'scudo', '#6b4a2b')]
TAVOLO_VALORI = [(str(v), ()) for v in range(10)]; TAVOLO_FIN = (11.0, 9.0)   # corona 0-9 di svg.board()
SF, GAP = 2.0, 0.6   # righe piccole della corona (corpo, interlinea): come i default di svg.dial_block

GOLD_R = 4.8   # raggio del cerchio dorato dietro alle etichette «dorate» (svg.dial_ring)
RAGGIO = {}   # corone con un raggio diverso da RING_R (v6: PE a 19 mm; nella v7 nessuna)
# Rotella della Profezia (Spec R 2.5, R 13.5): 10 posizioni 1-6, Pari, Dispari, Alto, Basso. Le parole non entrano in una
# finestra della corona Ø 52: lettera grande e parola piccola sotto. Corona su una base quadrata, disco Ø 52 come le altre.
PROFEZIA_VALORI = [(str(v), ()) for v in range(1, 7)] + [('P', ('pari',)), ('D', ('dispari',)), ('A', ('alto',)), ('B', ('basso',))]
PROFEZIA_FIN, PROFEZIA_MH, COL_PROF = (10.0, 9.0), 4.0, '#b8862b'
BASE_PROF = 58.0   # lato della base della Profezia (taglio sul bordo sottile, fondo chiaro senza abbondanza)
def verifica_rotella(nome, vals, win, mh, gold=(), marg=0.5, rr=RING_R):
    """Per ogni posizione: la finestra contiene tutta l'etichetta (>= marg mm dal bordo) e nessun pezzo delle altre
    (separazione >= marg mm, test degli assi separatori tra rettangoli; cerchi dorati come cerchi). Ritorna
    (margine proprio, distanza dai vicini)."""
    n = len(vals); ww, wh = win
    def lab(i):
        a = math.radians(dial_angle(i, n)); x, y = rr * math.sin(a), -rr * math.cos(a)
        main, smalls = vals[i]
        w = max([tw(main, mh / CAP, SANS, True)] + [tw(s, SF, SANS) for s in smalls])
        _, h = dial_block(main, smalls, mh, SF, GAP)
        return x, y, w, h
    def corners(x, y, w, h): return [(x + sx * w / 2, y + sy * h / 2) for sx in (-1, 1) for sy in (-1, 1)]
    own = nb = 99.0
    for i in range(n):
        a = math.radians(dial_angle(i, n))
        c = (rr * math.sin(a), -rr * math.cos(a)); u = (math.cos(a), math.sin(a)); v = (math.sin(a), -math.cos(a))
        wpts = [(c[0] + su * ww / 2 * u[0] + sv * wh / 2 * v[0], c[1] + su * ww / 2 * u[1] + sv * wh / 2 * v[1]) for su in (-1, 1) for sv in (-1, 1)]
        loc = lambda px, py: (abs((px - c[0]) * u[0] + (py - c[1]) * u[1]), abs((px - c[0]) * v[0] + (py - c[1]) * v[1]))
        for j in range(n):
            x, y, w, h = lab(j)
            if j == i:
                own = min(own, min(min(ww / 2 - du, wh / 2 - dv) for du, dv in map(lambda p: loc(*p), corners(x, y, w, h))))
                if j in gold: own = min(own, min(ww, wh) / 2 - GOLD_R)
                continue
            lp = corners(x, y, w, h); gap_max = -99.0
            for ax in ((1, 0), (0, 1), u, v):
                p1 = [px * ax[0] + py * ax[1] for px, py in wpts]; p2 = [px * ax[0] + py * ax[1] for px, py in lp]
                gap_max = max(gap_max, max(min(p2) - max(p1), min(p1) - max(p2)))
            nb = min(nb, gap_max)
            if j in gold:
                du, dv = loc(x, y)
                nb = min(nb, math.hypot(max(du - ww / 2, 0), max(dv - wh / 2, 0)) - GOLD_R)
    assert own >= marg and nb >= marg, f'rotella {nome}: finestra {win} margine {own:.2f} mm, vicini a {nb:.2f} mm'
    return round(own, 2), round(nb, 2)

def rotella_disco(cx, cy, fill, nome, sotto, ic, win, riga='', rr=RING_R):
    """disco Ø 52 da ritagliare: colore pieno con 3 mm di abbondanza più chiara (il cambio di colore è il taglio),
    finestra bianca da ritagliare a rr mm dal centro (in alto), tacche indice, foro del fermacampioni, frecce «gira»."""
    ww, wh = win; R = DISC_R
    o = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R + BLEED:.2f}" fill="{mix(fill, 0.45)}"/>',
         f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="{fill}"/>',
         f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R - 1.4:.2f}" fill="none" stroke="#ffffff" stroke-width="0.3" opacity="0.55"/>']
    assert rr + wh / 2 <= R - 1.2, f'{nome}: bordo del disco fuori dalla finestra < 1,2 mm'
    wx, wy = cx - ww / 2, cy - rr - wh / 2
    o.append(f'<rect x="{wx:.2f}" y="{wy:.2f}" width="{ww}" height="{wh}" fill="#ffffff" stroke="{CUT}" stroke-width="0.25"/>')
    o.append(line(wx + 1.2, wy + 1.2, wx + ww - 1.2, wy + wh - 1.2, 0.15, '#bbbbbb') + line(wx + ww - 1.2, wy + 1.2, wx + 1.2, wy + wh - 1.2, 0.15, '#bbbbbb'))
    for s in (-1, 1):   # tacche indice ai lati della finestra
        tx = cx + s * (ww / 2 + 0.7); ty = cy - rr
        o.append(f'<path d="M{tx:.2f} {ty:.2f}L{tx + s * 2.4:.2f} {ty - 1.4:.2f}L{tx + s * 2.4:.2f} {ty + 1.4:.2f}Z" fill="#ffffff"/>')
    for s in (-1, 1):   # frecce «gira»
        r = 22.6; a0, a1 = math.radians(s * 36), math.radians(s * 74)
        p0 = (cx + r * math.sin(a0), cy - r * math.cos(a0)); p1 = (cx + r * math.sin(a1), cy - r * math.cos(a1))
        o.append(f'<path d="M{p0[0]:.2f} {p0[1]:.2f}A{r} {r} 0 0 {1 if s > 0 else 0} {p1[0]:.2f} {p1[1]:.2f}" fill="none" stroke="#ffffff" stroke-width="0.55" stroke-linecap="round"/>')
        t = (math.cos(a1) * s, math.sin(a1) * s)   # tangente nel verso della freccia
        nrm = (math.sin(a1), -math.cos(a1))
        h1 = (p1[0] - 1.8 * t[0] + 1.1 * nrm[0], p1[1] - 1.8 * t[1] + 1.1 * nrm[1]); h2 = (p1[0] - 1.8 * t[0] - 1.1 * nrm[0], p1[1] - 1.8 * t[1] - 1.1 * nrm[1])
        o.append(f'<path d="M{h1[0]:.2f} {h1[1]:.2f}L{p1[0]:.2f} {p1[1]:.2f}L{h2[0]:.2f} {h2[1]:.2f}" fill="none" stroke="#ffffff" stroke-width="0.55" stroke-linecap="round" stroke-linejoin="round"/>')
        am = math.radians(s * 55)
        o.append(text(cx + 16.6 * math.sin(am), cy - 16.6 * math.cos(am) + 0.8, 'gira', 2.4, '#ffffff', 'middle', True))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="5" fill="none" stroke="#ffffff" stroke-width="0.25" stroke-dasharray="0.9 0.7"/>')
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="1.1" fill="#ffffff"/>' + line(cx - 1.6, cy, cx + 1.6, cy, 0.18, INK) + line(cx, cy - 1.6, cx, cy + 1.6, 0.18, INK))
    if riga: o.append(text(cx, cy - 7.6, riga, 2.3, '#ffffff', 'middle'))
    fs = 6.0
    while tw(nome, fs, SANS, True) > 30: fs -= 0.1
    o.append(text(cx, cy + 11.2, nome, fs, '#ffffff', 'middle', True))
    fs = 2.6
    while tw(sotto, fs, SANS) > 32: fs -= 0.1
    o.append(text(cx, cy + 15.4, sotto, fs, '#ffffff', 'middle'))
    o.append(icon(ic, cx, cy + 20.4, 4.0 / 24, '#ffffff'))
    return ''.join(o)

def profezia_base(cx, cy):
    """base 58 x 58 mm della Rotella della Profezia: corona di PROFEZIA_VALORI e, negli angoli (fuori dal disco), la legenda."""
    s = BASE_PROF / 2
    o = [f'<rect x="{cx - s:.2f}" y="{cy - s:.2f}" width="{BASE_PROF}" height="{BASE_PROF}" rx="1.5" fill="#f7efdc" stroke="{CUT}" stroke-width="0.25"/>',
         dial_ring(cx, cy, PROFEZIA_VALORI, mh=PROFEZIA_MH, sf=SF, gap=GAP)]
    for dx, dy, t, anc, bold in ((-1, -1, 'PROFEZIA', 'start', True), (1, -1, 'Oracolo', 'end', True),
                                 (-1, 1, 'Alto: 4+ · 8+', 'start', False), (1, 1, 'Basso: 3− · 6−', 'end', False)):
        o.append(text(cx + dx * (s - 1.6), cy + dy * (s - 1.6) + (2.2 if dy < 0 else 0), t, 2.4, BROWN if not bold else INK, anc, bold))
    return ''.join(o)

def profezia_disco(cx, cy):
    return rotella_disco(cx, cy, COL_PROF, 'Profezia', 'Oracolo', 'occhio', PROFEZIA_FIN, 'rotella della Profezia')

# ------------------------------------------------------------------ PLANCE EROE (280 x 194, A4 orizzontale)
PLANCE = 4                # plance eroe neutre (D14), al massimo 4 giocatori: ogni plancia va bene per ogni eroe
COL_PB = BROWN            # colore unico di plance e dischi (prima: il colore della classe)
PB_W, PB_H = 280.0, 194.0
FESSURE = [(5.5, 'Elmo', 'elmo'), (72.5, 'Arma DX / Scudo', 'spade'), (139.5, 'Arma SX', 'spade'), (206.5, 'Armatura', 'scudo')]
FESS_Y, FESS_L = 14.0, 65.0
CARTE_PB = [(4.0, 'Carta Classe'), (75.0, 'Carta Specie')]   # riquadri 63 x 88 da y 20
CELLE = {'PV': (142, 18), 'PVM': (209, 18), 'ATT': (142, 76), 'MOV': (209, 76), 'AR': (142, 134), 'PL': (209, 134)}
TAGLIO = '#d0312d'   # linee da incidere
NOTE_ROT = {'PV': ['attuali', '0 = sconfitto'], 'PVM': ['massimi'], 'ATT': ['attacco', '2D6 + ATT'],
            'MOV': ['movimento', 'D6 + MOV'], 'AR': ['armatura', 'ti colpisce chi fa 2D6 + ATT ≥ AR'], 'PL': ['power level', 'somma dei PL negli slot']}
MONTAGGIO = {
    'Carta Classe': ['1 · Incidi col taglierino le linee rosse: 4 fessure in alto e i tagli ai 4 angoli dei due riquadri.',
                     '2 · Fora con un punteruolo il centro segnato delle 6 rotelle.',
                     '3 · Monta i 6 dischi (rotelle_eroe.pdf): disco sopra la corona col suo nome, fermacampioni dal davanti, gambe aperte in orizzontale sul retro.',
                     '4 · Infila i 4 angoli della Carta Classe nei tagli: resta lì per tutta la partita.'],
    'Carta Specie': ['Infila i 4 angoli della Carta Specie nei tagli e gira subito le rotelle del suo bonus.',
                     'Equipaggiamenti: infila la carta nella fessura dal davanti, con il nome in alto: il fondo passa sotto la plancia, il resto sporge sopra il bordo.',
                     'Le rotelle mostrano sempre il valore finale, equipaggiamento compreso.']}

def taglio_angolo(X, Y, sx, sy):
    """taglio diagonale a 45° lungo 10 mm sull'angolo (X, Y) di un riquadro 63 x 88 (sx, sy = verso l'interno):
    incrocia i lati della carta a 6 mm dall'angolo e sporge 0,5 mm fuori da ciascun lato."""
    h = 5 / math.sqrt(2)
    p = (X + sx * (3 + h), Y + sy * (3 - h)); q = (X + sx * (3 - h), Y + sy * (3 + h))
    return line(p[0], p[1], q[0], q[1], 0.4, TAGLIO)

def plancia_eroe():
    """una plancia eroe neutra in coordinate della plancia (mm, angolo alto-sinistro = 0,0); il bordo esterno è il taglio."""
    col = COL_PB
    o = [f'<rect x="-1.5" y="-1.5" width="{PB_W + 3}" height="{FESS_Y + 1.5}" fill="{mix(col, 0.8)}"/>']
    for x0, lab, ic in FESSURE:   # fasce degli slot Equipaggiamento (coperte dalla carta) e fessure
        o.append(icon(ic, x0 + 7, 7.2, 5.2 / 24, col))
        o.append(text(x0 + FESS_L / 2 + 3, 8.7, lab, 3.6, INK, 'middle', True))
        o.append(line(x0, FESS_Y, x0 + FESS_L, FESS_Y, 0.45, TAGLIO) + line(x0, FESS_Y - 0.9, x0, FESS_Y + 0.9, 0.3, TAGLIO) + line(x0 + FESS_L, FESS_Y - 0.9, x0 + FESS_L, FESS_Y + 0.9, 0.3, TAGLIO))
        o.append(text(x0 + FESS_L / 2, 16.9, 'incidi la fessura (65 mm)', 2.0, TAGLIO, 'middle'))
    o.append(line(140, 19, 140, PB_H - 2, 0.3, LINE))
    for x0, lab in CARTE_PB:   # riquadri Carta Classe / Carta Specie 63 x 88 con i tagli d'angolo
        y0 = 20.0
        o.append(f'<rect x="{x0}" y="{y0}" width="63" height="88" rx="3" fill="#fbf6ea" stroke="{BROWN}" stroke-width="0.3" stroke-dasharray="1.6 1.2"/>')
        o.append(text(x0 + 31.5, y0 + 13, lab, 4.6, col, 'middle', True, SERIF))
        o.append(text(x0 + 31.5, y0 + 18, '63 × 88 mm · infila i 4 angoli nei tagli', 2.3, BROWN, 'middle'))
        yy = y0 + 26
        for par in MONTAGGIO[lab]:
            for l in wrap(par, 2.5, 55):
                o.append(text(x0 + 4, yy, l, 2.5, INK)); yy += 3.2
            yy += 1.4
        assert yy < y0 + 86, lab
        for (X, sx) in ((x0, 1), (x0 + 63, -1)):
            for (Y, sy) in ((y0, 1), (y0 + 88, -1)):
                o.append(taglio_angolo(X, Y, sx, sy))
    # Indizi (3 cerchi) e Forte Volontà (1 cerchio): Ø 22 per segnalini Ø 20, centri a y 128
    o.append(text(4, 115.6, 'Indizi', 3.4, INK, 'start', True))
    o.append(text(4 + tw('Indizi', 3.4, SANS, True) + 2, 115.6, 'al 3°: tesoro!', 2.8, BROWN, 'start', italic=True))
    for x in (16, 42, 68):
        o.append(f'<circle cx="{x}" cy="128" r="11" fill="#fbf6ea" stroke="{BROWN}" stroke-width="0.3" stroke-dasharray="1.6 1.2"/>' + icon('pergamena', x, 128, 9 / 24, mix(INK, 0.75)))
    o.append(text(104, 115.6, 'Forte Volontà', 3.4, INK, 'middle', True))
    o.append(f'<circle cx="104" cy="128" r="11" fill="#fbf6ea" stroke="{BROWN}" stroke-width="0.3" stroke-dasharray="1.6 1.2"/>' + icon('stella', 104, 128, 9 / 24, mix(GOLD, 0.6)))
    for j, l in enumerate(['ritira 1 D6', 'appena tirato;', 'non si accumula']):
        o.append(text(117.5, 124.5 + j * 3.3, l, 2.5, BROWN))
    # riquadro Stati: 4 posti da 30 x 32 (tessera 26 x 18 dritta o 18 x 26 di traverso)
    o.append(f'<rect x="4" y="144" width="134" height="32" rx="3" fill="#fbf6ea" stroke="{BROWN}" stroke-width="0.3"/>')
    o.append(text(5.8, 151.5, 'Stati', 3.6, INK, 'start', True))
    yy = 156.0
    for par in ['dritto: toglilo alla tua Fine', 'di traverso: raddrizzalo alla tua Fine']:
        for l in wrap(par, 2.1, 11.6):
            o.append(text(5.8, yy, l, 2.1, BROWN)); yy += 2.6
        yy += 0.8
    assert yy < 176
    for i in range(4):
        cx, cy = 33 + 30 * i, 160
        o.append(f'<rect x="{cx - 13}" y="{cy - 9}" width="26" height="18" rx="1.2" fill="none" stroke="{LINE}" stroke-width="0.3" stroke-dasharray="1.2 1"/>')
        o.append(f'<rect x="{cx - 9}" y="{cy - 13}" width="18" height="26" rx="1.2" fill="none" stroke="{LINE}" stroke-width="0.3" stroke-dasharray="0.5 1"/>')
    # promemoria
    prom = ['Si parte da PV 5 · PV max 5 · ATT 1 · MOV 1 · AR 9 · PL 0, poi aggiungi il bonus della Carta Specie.',
            'Le statistiche cambiano solo con carte, Equipaggiamenti e Stati. Equipaggi o perdi un oggetto: gira subito le rotelle, PL compreso.',
            'Fine del turno: togli gli stati dritti, raddrizza quelli di traverso, togli gli Usato «una volta per turno» e i segnaposto.']
    for j, l in enumerate(prom):
        fs = 2.5
        while tw(l, fs) > 133: fs -= 0.05
        o.append(text(4.5, 181.6 + j * 3.6, l, fs, INK))
    # 6 rotelle: corona sulla plancia, centro a x_cella + 40, y_cella + 29; etichetta nei 13 mm a sinistra del disco
    for key, nm, sotto, ic, icol, vals, win, mh, gold, red in ROTELLE:
        xc, yc = CELLE[key]; cx, cy = xc + 40, yc + 29
        o.append(dial_ring(cx, cy, vals, mh=mh, sf=SF, gap=GAP, gold=gold, red=red, rr=RAGGIO.get(key, RING_R)))
        o.append(icon(ic, xc + 7, yc + 9, 6 / 24, icol))
        fs = 3.8
        while tw(nm, fs, SANS, True) > 12.5: fs -= 0.1
        o.append(text(xc + 7, yc + 18, nm, fs, INK, 'middle', True))
        yy = yc + 22
        for par in NOTE_ROT[key]:
            for l in wrap(par, 2.1, 12.5):
                o.append(text(xc + 7, yy, l, 2.1, BROWN, 'middle')); yy += 2.6
        o.append(text(xc + 7, yc + 47, 'fermacampioni', 1.8, BROWN, 'middle'))
        o.append(text(xc + 7, yc + 49.4, 'al centro', 1.8, BROWN, 'middle'))
    o.append(text(142, 192.4, 'Il Tesoro del Goblin · playtest v7', 2.4, BROWN))
    o.append(text(276, 192.6, 'Plancia eroe', 3.4, col, 'end', True, SERIF))
    o.append(f'<rect x="0" y="0" width="{PB_W}" height="{PB_H}" rx="2" fill="none" stroke="{CUT}" stroke-width="0.25"/>')
    return ''.join(o)

def plance_eroe():
    """4 plance neutre 280 x 194 mm, una per foglio A4 orizzontale, taglio a 8,5 / 8 mm dal bordo del foglio."""
    for i in range(PLANCE):
        write('plance_eroe', i + 1, page(fonts(f'<g id="plancia-eroe-{i + 1}" transform="translate(8.5,8)">{plancia_eroe()}</g>'), 297, 210))
    return PLANCE, PB_W, PB_H

def dischi_eroe(serie, x0, y0, cols, pitch=DISC_R * 2 + 2 * BLEED, per_colonna=False):
    """dischi delle 6 rotelle per `serie` plance; per_colonna: una plancia per colonna (A3), altrimenti 6 di fila."""
    b = []
    for h in range(serie):
        for k, (key, nm, sotto, ic, icol, vals, win, mh, gold, red) in enumerate(ROTELLE):
            i = h + k * cols if per_colonna else h * 6 + k
            b.append(rotella_disco(x0 + DISC_R + (i % cols) * pitch, y0 + DISC_R + (i // cols) * pitch, COL_PB, nm, sotto, ic, win, 'plancia eroe', RAGGIO.get(key, RING_R)))
    return b

def rotelle_eroe():
    """24 dischi Ø 52 (6 per plancia) su 2 fogli A4: 12 per foglio, 3 x 4, 2 plance per foglio."""
    pitch = DISC_R * 2 + 2 * BLEED; x0 = (210 - (2 * pitch + 2 * DISC_R)) / 2; y0 = 27.0
    for p in range(2):
        b = [hdr(f'Rotelle delle plance eroe · foglio {p + 1} di 2',
                 f'plancia {2 * p + 1} (righe 1-2) · plancia {2 * p + 2} (righe 3-4) · 12 dischi Ø 52 mm · solo fronte')]
        b += dischi_eroe(2, x0, y0, 3)
        assert y0 + 3 * pitch + 2 * DISC_R + BLEED < 262
        b.append(ftr(['Stampa su A4 al 100%, solo fronte (meglio carta 160-200 g, o incolla il foglio su un cartoncino prima di ritagliare).',
                      'Ritaglia ogni disco dove cambia il colore; ritaglia la finestra bianca col taglierino; fora il centro con un punteruolo.',
                      'Monta il disco sopra la corona con lo stesso nome della plancia eroe: fermacampioni dal davanti, gambe aperte in orizzontale dietro.',
                      'Girando il disco la finestra mostra un solo valore. 6 dischi e 6 fermacampioni per plancia.'], y=266))
        write('rotelle_eroe', p + 1, page(fonts('\n'.join(b))))
    return 6 * PLANCE

def conta(c):
    return ' · '.join(f'{n} {nome}' for nome, n in c.items())

def segnalini():
    """segnalini.pdf A4: foglio 1 = segnalini Ø 20; foglio 2 = tessere Stato e i 2 dischi delle rotelle del tavolo (la Rotella
    della Profezia è sul foglio 2 delle pedine)."""
    cols = 6; pitch = 26
    rows = read('segnalini.csv'); nrows = sum(math.ceil(int(r['copie']) / cols) for r in rows)
    gw, gh = (cols - 1) * pitch + 20, (nrows - 1) * pitch + 20
    b, gc, _ = gettoni(cols, (210 - gw) / 2, (297 - gh) / 2)
    b.insert(0, hdr('Segnalini · foglio 1 di 2', f"{gc['Indizio']} Indizi · {gc['Forte Volontà']} Forte Volontà · {gc['Usato']} Usato  ·  Ø 20 mm  ·  solo fronte"))
    b.append(ftr(['Stampa su A4 al 100%, solo fronte. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                  'Righe 1-3 Indizi, riga 4 Forte Volontà, poi Usato: Carta Classe, «una volta per turno», «la prima volta» dei mostri,',
                  '«Spostamenti del tesoro» e segnaposto delle carte giocate che lasciano la zona (Equipaggiamenti e Mappe).']))
    write('segnalini', 1, page(fonts('\n'.join(b))))
    sc_ = 5; sx0 = (210 - ((sc_ - 1) * (ST_W + 2 * BLEED) + ST_W)) / 2
    b, sc, sbb = stati(sc_, sx0, 28.0)
    b.insert(0, hdr('Tessere Stato e rotelle del tavolo · foglio 2 di 2',
                    f'{sum(sc.values())} tessere Stato 26 × 18 mm · 2 dischi Ø 52 mm · solo fronte'))
    pitch = DISC_R * 2 + 2 * BLEED; dy = sbb[3] + 18 + DISC_R
    for j, (key, nm, sotto, ic, col) in enumerate(R_TAVOLO):
        b.append(rotella_disco(105 + (j - 0.5) * pitch, dy, col, nm, sotto, ic, TAVOLO_FIN, 'plancia di gioco'))
    assert dy + DISC_R + BLEED < 262
    b.append(ftr(['Stampa su A4 al 100%, solo fronte. Tessere Stato: taglia sul bordo sottile (3 mm di abbondanza).',
                  f'Righe: {conta(sc)}.',
                  'Uno stato vale un turno: preso nel tuo turno va di traverso, nel turno di un altro dritto (freccia ↑ in alto).',
                  'Dischi: ritaglia dove cambia il colore e la finestra bianca, fora il centro. «PV del mostro» e «PV del custode» vanno sulle corone 0-9',
                  'della Sala del Tesoro, con un fermacampioni. La Rotella della Profezia è sul foglio 2 delle pedine (pedine.pdf).'], y=266))
    write('segnalini', 2, page(fonts('\n'.join(b))))
    return dict(gettoni=gc, stati=sc, dischi_tavolo=len(R_TAVOLO))

# ------------------------------------------------------------------ PLANCIA
def plancia():
    S = 0.97
    bs = board(W=26)
    m = re.match(r'<svg viewBox="0 0 ([\d.]+) ([\d.]+)"', bs); bw, bh = float(m.group(1)), float(m.group(2))
    Wb, Hb = bw * S, bh * S
    WIN_W, WIN_H = 184.0, 230.0   # finestra di stampa per foglio: lascia >= 6,5 mm per le tacche prima del bordo foglio
    PX, PY = 13.0, 13.0
    bd = fonts(inner(bs)).replace('rx="13.0"', 'rx="0"', 1)
    ox = Wb - WIN_W; oy = Hb - WIN_H      # inizio finestra destra / bassa
    ovx, ovy = WIN_W - ox, WIN_H - oy
    names = {(0, 0): ('1 di 4', 'alto a sinistra'), (1, 0): ('2 di 4', 'alto a destra'), (0, 1): ('3 di 4', 'basso a sinistra'), (1, 1): ('4 di 4', 'basso a destra')}
    ctr = (Wb / 2, Hb / 2)
    marks_board = [(Wb / 2, 8), (Wb / 2, Hb - 8), (8, Hb / 2), (Wb - 8, Hb / 2), (Wb / 2, Hb / 2)]
    # i marchi V stanno al centro della fascia di sovrapposizione: x = (ox+WIN_W)/2 ; y = (oy+WIN_H)/2
    mx, my = (ox + WIN_W) / 2, (oy + WIN_H) / 2
    marks_board = [(mx, 8), (mx, Hb - 8), (8, my), (Wb - 8, my), (mx, my)]
    info = {}
    for (c, r), (num, pos) in names.items():
        wx0 = 0 if c == 0 else ox; wy0 = 0 if r == 0 else oy
        cx0 = PX - (BLEED if c == 0 else 0); cx1 = PX + WIN_W + (BLEED if c == 1 else 0)
        cy0 = PY - (BLEED if r == 0 else 0); cy1 = PY + WIN_H + (BLEED if r == 1 else 0)
        cid = f'clip{c}{r}'
        b = [f'<defs><clipPath id="{cid}"><rect x="{cx0}" y="{cy0}" width="{cx1 - cx0}" height="{cy1 - cy0}"/></clipPath></defs>',
             f'<rect id="abbondanza" x="{cx0}" y="{cy0}" width="{cx1 - cx0}" height="{cy1 - cy0}" fill="#efe1c3"/>',
             f'<g id="plancia-{num.replace(" ", "")}" clip-path="url(#{cid})"><g transform="translate({PX - wx0:.3f},{PY - wy0:.3f}) scale({S})" font-family="{SANS}">{bd}</g></g>']
        for (bx, by) in marks_board:
            if wx0 <= bx <= wx0 + WIN_W and wy0 <= by <= wy0 + WIN_H:
                px, py = PX + bx - wx0, PY + by - wy0
                b.append(f'<g id="croce-di-allineamento"><circle cx="{px:.2f}" cy="{py:.2f}" r="1.9" fill="none" stroke="#c0392b" stroke-width="0.2"/>{line(px - 3.5, py, px + 3.5, py, 0.2, "#c0392b")}{line(px, py - 3.5, px, py + 3.5, 0.2, "#c0392b")}</g>')
        b.append(crop_marks(PX, PY, PX + WIN_W, PY + WIN_H, gap=3.5, ln=3.0))
        # tacche di taglio sui bordi interni
        cut_l = c == 1; cut_t = r == 1
        yf = PY + WIN_H + 9
        b.append(text(105, yf, f'PLANCIA «Le Terre di Hande» v7 · foglio {num} ({pos})', 4.0, INK, 'middle', True, SERIF))
        ins = []
        if (c, r) == (0, 0):
            ins.append('Foglio base: non si taglia. Gli altri fogli si sovrappongono alle sue fasce di destra e di sotto.')
        if (c, r) == (1, 0):
            ins.append(f'Taglia il margine bianco a SINISTRA lungo le tacche (x = {PX:.0f} mm). Sovrapponi il foglio sulla fascia di {ovx:.1f} mm a destra del foglio 1.')
            ins.append('Fai coincidere le croci rosse e il disegno; incolla.')
        if (c, r) == (0, 1):
            ins.append(f'Taglia il margine bianco in ALTO lungo le tacche (y = {PY:.0f} mm). Sovrapponi il foglio sulla fascia di {ovy:.1f} mm in basso del foglio 1.')
            ins.append('Fai coincidere le croci rosse e il disegno; incolla.')
        if (c, r) == (1, 1):
            ins.append('Taglia i margini bianchi a SINISTRA e in ALTO lungo le tacche. Sovrapponilo agli angoli dei fogli 2 (fascia in basso) e 3 (fascia a destra).')
            ins.append('Fai coincidere le croci rosse (la croce centrale è su tutti e 4 i fogli); incolla per ultimo.')
        for j, l in enumerate(ins): b.append(text(105, yf + 6 + j * 4.2, l, 2.8, INK, 'middle'))
        b.append(text(105, yf + 17, f'A4 verticale, stampa al 100%. Plancia finita {Wb:.1f} × {Hb:.1f} mm (1 unità del disegno = {S} mm), esagono {26 * S:.1f} mm.', 2.6, BROWN, 'middle'))
        b.append(text(105, yf + 21, f'Sovrapposizione: orizzontale {ovx:.1f} mm, verticale {ovy:.1f} mm.', 2.6, BROWN, 'middle'))
        b.append(text(105, yf + 25, 'Una plancia in 4 fogli A4. Mappa: bozza v7 per il playtest (10 × 10 esagoni, girata di 180° è identica).', 2.6, BROWN, 'middle'))
        write('plancia', c + 2 * r + 1, page('\n'.join(b)))
    return dict(W=Wb, H=Hb, win=(WIN_W, WIN_H), ox=ox, oy=oy, ovx=ovx, ovy=ovy)

# ------------------------------------------------------------------ PEDINE
PAWNS = {  # nome: (icona, colore, tipo)
    'Assaltatore': ('spade', '#9c2f24', 'eroe'), 'Ricercatore': ('occhio', '#3b7d4f', 'eroe'),
    'Stregone': ('stella', '#5b4a9c', 'eroe'), 'Oracolo': ('cuore', '#b8862b', 'eroe'), 'Giullare': ('carte', '#a8407e', 'eroe'),
    'MIMI': ('forziere', '#6b4a2b', 'forziere'), 'Geronimo': ('bandiera', '#4a6a2f', 'primo giocatore'),
    'Buttafuori di MIMI': ('scudo', '#2b1d14', 'boss'), 'Mimic della Bisnonna': ('forziere', '#2b1d14', 'boss'),
    'Re Goblin Grugno': ('teschio', '#2b1d14', 'boss'), 'Soprano Stonata': ('stella', '#2b1d14', 'boss'),
    'Presentatore del Sabato': ('occhio', '#2b1d14', 'boss'), 'Lord Spiegone': ('pergamena', '#2b1d14', 'boss')}
GEO = {'eroe': dict(w=24.0, ph=34.0, fh=7.0), 'boss': dict(w=40.0, ph=44.0, fh=8.0)}   # pedine piccole (24 mm) e sagome dei Boss
EROI = ['Assaltatore', 'Ricercatore', 'Stregone', 'Oracolo', 'Giullare', 'MIMI']
BOSS = ['Buttafuori di MIMI', 'Mimic della Bisnonna', 'Re Goblin Grugno', 'Soprano Stonata', 'Presentatore del Sabato', 'Lord Spiegone']   # D20: 6 boss
def pedine(gruppi=None):
    """gruppi = [(nomi, geometria, x0, y)]: un gruppo è una fila con le sue tacche di taglio. Dati i gruppi (foglio misto A3)
    ritorna solo (svg, pezzi). Senza: 2 fogli A4, foglio 1 con 5 eroi + MIMI nella prima fila e i primi 3 Boss + Geronimo
    (gruppo a parte) nella seconda; foglio 2 con gli altri 3 Boss e, sotto, la Rotella della Profezia (disco + base)."""
    rows = {r['nome']: r for r in read('pedine.csv')}; assert len(rows) == 13 and set(rows) == set(PAWNS)
    if gruppi is not None:
        return pedine_pezzi(rows, gruppi)
    e = GEO['eroe']; xe = (210 - ((len(EROI) - 1) * (e['w'] + 2 * BLEED) + e['w'])) / 2
    gb = 2 * (GEO['boss']['w'] + 2 * BLEED) + GEO['boss']['w']; sep = 16.0   # 3 Boss; 16 mm: tacche dei due gruppi
    xb = (210 - (gb + sep + e['w'])) / 2
    y2 = 28.0 + 2 * (e['fh'] + e['ph']) + 2 * BLEED + 8
    fogli = [([(EROI, 'eroe', xe, 28.0), (BOSS[:3], 'boss', xb, y2), (['Geronimo'], 'eroe', xb + gb + sep, y2)],
              '5 eroi · MIMI · Geronimo · 3 Boss'),
             ([(BOSS[3:], 'boss', (210 - gb) / 2, 28.0)], 'altri 3 Boss (6 in tutto: 1 custode + 5 del mazzetto 3) · Rotella della Profezia')]
    out = []
    for p, (gr, sub) in enumerate(fogli):
        b, pz = pedine_pezzi(rows, gr)
        b.insert(0, hdr(f'Pedine e sagome · foglio {p + 1} di 2', f'{sub}  ·  pieghevoli fronte/retro  ·  solo fronte, A4 verticale'))
        note = ['Stampa su A4 al 100%. Ritaglia il rettangolo di ogni pedina. Piega sulla linea tratteggiata bianca (al centro) e incolla fronte e retro.',
                'Piega le due linguette chiare (tratteggio grigio) una in avanti e una indietro: ottieni un piede a T per far stare in piedi la sagoma.',
                'Eroi, MIMI e Geronimo: larghezza 24 mm (stanno in un esagono). Boss: 40 mm (stanno nei cerchi della Sala del Tesoro). Colori degli eroi = colori dei dorsi di classe.']
        if p == 1:   # sotto i Boss: Rotella della Profezia
            py = 28.0 + 2 * (GEO['boss']['fh'] + GEO['boss']['ph']) + 7.5 + 6 + BASE_PROF / 2
            b.append(profezia_disco(105 - 35, py))
            b.append(profezia_base(105 + 35, py))
            assert py + BASE_PROF / 2 < 262
            note.append('Rotella della Profezia (Oracolo): ritaglia il disco e la finestra, taglia la base sul bordo sottile; disco sulla base col fermacampioni.')
            note.append('P pari · D dispari · A alto (4+ su un D6, 8+ su 2D6) · B basso (3− su un D6, 6− su 2D6).')
        b.append(ftr(note, y=283 - 3.6 * (len(note) - 3)))
        write('pedine', p + 1, page(fonts('\n'.join(b))))
        out += pz
    return out

def pedine_pezzi(rows, gruppi):
    """svg e pezzi [(nome, x, y, w, h)] delle file `gruppi` (una fila per gruppo, con le sue tacche di taglio)."""
    b = []
    out = []
    for k, (nomi, gk, x0, y) in enumerate(gruppi):
        g = GEO[gk]; w, ph, fh = g['w'], g['ph'], g['fh']; H = 2 * (fh + ph)
        n = len(nomi); pitch = w + 2 * BLEED
        gw = (n - 1) * pitch + w
        for i, nm in enumerate(nomi):
            r = rows[nm]
            ic, col, tipo = PAWNS[nm]
            x = x0 + i * pitch
            tint = mix(col, 0.62)
            # abbondanza laterale + sopra/sotto
            b.append(f'<rect x="{x - BLEED}" y="{y - BLEED}" width="{w + 2 * BLEED}" height="{H + 2 * BLEED}" fill="{col}"/>')
            # linguette (piede), chiare
            b.append(f'<rect x="{x - BLEED}" y="{y - BLEED}" width="{w + 2 * BLEED}" height="{fh + BLEED}" fill="{tint}"/>')
            b.append(f'<rect x="{x - BLEED}" y="{y + H - fh}" width="{w + 2 * BLEED}" height="{fh + BLEED}" fill="{tint}"/>')
            for part in (0, 1):  # 0 retro (ruotato) 1 fronte
                py = y + fh if part == 0 else y + fh + ph
                cx, cy = x + w / 2, py + ph / 2
                rot = f' transform="rotate(180 {cx:.2f} {cy:.2f})"' if part == 0 else ''
                p = [f'<rect x="{x + 1.3:.2f}" y="{py + 1.3:.2f}" width="{w - 2.6:.2f}" height="{ph - 2.6:.2f}" rx="1.6" fill="none" stroke="#f4ead5" stroke-width="0.35"/>']
                mr = min(w * 0.31, ph * 0.26) if gk == 'eroe' else 8.6
                my = py + 4.2 + mr if gk == 'eroe' else py + 5 + mr
                p.append(f'<circle cx="{cx:.2f}" cy="{my:.2f}" r="{mr:.2f}" fill="#f4ead5"/>')
                p.append(icon(ic, cx, my, mr * 1.3 / 24 * 1.0, col))
                fs = 3.6 if gk == 'eroe' else 4.6
                maxw = w - 4.4
                lines = wrap(nm, fs, maxw, SERIF, True)
                while any(tw(l, fs, SERIF, True) > maxw for l in lines) and fs > 2.0: fs -= 0.1
                ty = my + mr + 1.0 + fs * 1.05
                for j, l in enumerate(lines):
                    p.append(text(cx, ty + j * fs * 1.12, l, fs, '#ffffff' if col != '#b8862b' else '#2a2118', 'middle', True, SERIF))
                cap = {'eroe': 'Eroe', 'forziere': 'il forziere', 'primo giocatore': 'primo giocatore', 'boss (sagoma)': 'Boss'}[r['tipo']]
                p.append(text(cx, py + ph - 2.6, cap, 2.3, '#f4ead5' if col != '#b8862b' else '#2a2118', 'middle', False, SANS))
                b.append(f'<g{rot}>' + ''.join(p) + '</g>')
            # linee di piega (tratteggiate) e di taglio
            b.append(line(x, y + fh + ph, x + w, y + fh + ph, 0.25, '#ffffff', '1.2 0.8'))
            b.append(line(x, y + fh, x + w, y + fh, 0.2, '#555', '1 1'))
            b.append(line(x, y + H - fh, x + w, y + H - fh, 0.2, '#555', '1 1'))
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{H}" fill="none" stroke="#f4ead5" stroke-width="0.4"/>')
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{H}" fill="none" stroke="{CUT}" stroke-width="0.12" opacity="0.8"/>')
            out.append((nm, x, y, w, H))
        xs = sorted({x0 + i * pitch + o for i in range(n) for o in (0, w)})
        b.append(edge_ticks(xs, [y, y + H], (x0, y, x0 + gw, y + H), gap=3.5, ln=3.0).replace('tacche-di-taglio', f'tacche-gruppo{k + 1}'))   # 6,5 mm: i 6 Boss in fila sull'A3
    return b, out

# ------------------------------------------------------------------ PROVA DI STAMPA
KIT_A4 = [('tessere_esplorazione.pdf', 1), ('segnalini.pdf (segnalini, Stati, dischi del tavolo)', 2),
          ('rotelle_eroe.pdf (24 dischi)', 2), ('plance_eroe.pdf (A4 orizzontale)', 4), ('pedine.pdf (6 Boss, Profezia)', 2), ('plancia.pdf (4 fogli da unire)', 4)]
KIT_A3 = [('plancia.pdf (2 fogli da unire)', 2), ('plance_eroe.pdf (2 plance per foglio)', 2), ('rotelle_eroe.pdf (24 + 2 dischi)', 1),
          ('componenti_misti.pdf (pedine con 6 Boss, segnalini)', 1), ('tessere_esplorazione.pdf (e tessere Stato, Profezia)', 1)]
def fogli_carte():
    """[(file, fogli in parole, fogli)] dei PDF delle carte, contati con genera_carte.mazzi() (stessi CSV e stesso formato)."""
    sys.path.insert(0, os.path.join(HERE, '..', 'carte'))
    import genera_carte as gc
    out = []
    for nome, (_, carte) in gc.mazzi().items():
        n = -(-len(carte) // gc.PER_FOGLIO)
        nr = len(gc.fogli_dorsi(carte))          # fogli dei retri: solo quelli con almeno un dorso
        if nr:
            out.append((f'{nome}.pdf + {nome}_retri.pdf', f'{n} + {nr}', n + nr))
        else:
            out.append((f'{nome}.pdf', str(n), n))
    return out

def prova(PW=210, PH=297, formato='A4'):
    """00_prova_stampa.pdf: un foglio solo fronte con righello 100 mm, quadrato 50 mm, riquadro a 6,5 mm dal bordo
    e l'elenco dei file del kit (tutto solo fronte)."""
    K = '#000000'; FR = 6.5; cx = PW / 2; tw_ = PW - 40
    def par(x, y, s, size=3.5, bold=False, gap=1.25):
        ls = wrap(s, size, tw_, SANS, bold)
        return ''.join(text(x, y + j * size * gap, l, size, K, 'start', bold) for j, l in enumerate(ls)), y + len(ls) * size * gap
    b = [f'<rect x="{FR}" y="{FR}" width="{PW - 2 * FR}" height="{PH - 2 * FR}" fill="none" stroke="{K}" stroke-width="0.25"/>',
         text(cx, FR + 4.5, '↑ alto (lato corto di ingresso)', 3.0, BROWN, 'middle'),
         text(cx, 21, f'Prova di stampa {formato} · Il Tesoro del Goblin', 6.0, K, 'middle', True, SERIF),
         text(cx, 27, f'Un solo foglio {formato}, SOLO FRONTE: tutto il kit v7 si stampa solo fronte', 3.2, BROWN, 'middle')]
    rx, ry = 20, 58
    b.append(text(rx, ry - 9, 'Righello: 100 mm esatti tra lo 0 e il 10', 3.2, K, 'start', True))
    b.append(line(rx, ry, rx + 100, ry, 0.25, K))
    for i in range(101):
        ln = 5 if i % 10 == 0 else (3.2 if i % 5 == 0 else 1.8)
        b.append(line(rx + i, ry, rx + i, ry + ln, 0.2, K))
        if i % 10 == 0: b.append(text(rx + i, ry + 9, str(i // 10), 3.2, K, 'middle'))
    b.append(text(rx + 50, ry + 14, 'centimetri', 2.8, BROWN, 'middle'))
    qx, qy = PW - 65, 35
    b.append(f'<rect x="{qx}" y="{qy}" width="50" height="50" fill="none" stroke="{K}" stroke-width="0.4"/>')
    b.append(text(qx + 25, qy + 26, '50 × 50 mm', 3.6, K, 'middle', True))
    b.append(text(qx + 25, qy + 32, 'misura i lati', 2.8, BROWN, 'middle'))
    y = 104
    for p in [f'1. Stampa al 100% («Dimensioni effettive», MAI «Adatta alla pagina»), carta {formato}, SOLO FRONTE (niente fronte-retro, nemmeno manuale).',
              '2. Scala: misura il righello (100 mm tra 0 e 10) e il quadrato (50 mm). Va bene entro ±1 mm. Se no, disattiva «adatta/riduci» e ristampa.',
              '3. Margini: il riquadro sottile a 6,5 mm dal bordo deve vedersi su tutti e 4 i lati. Se manca un lato la stampante taglia il margine: carte, plance e tacche stanno oltre i 6,5 mm.',
              'Se tutto torna, stampa il resto del kit nell’ordine dell’elenco qui sotto. Le carte e i loro dorsi sono su fogli separati: si uniscono a mano (colla stick o bustina).']:
        t, y = par(20, y, p); b.append(t); y += 2.2
    y += 6
    kit = [('00_prova_stampa.pdf', '1', 1)] + fogli_carte() + [(f, str(n), n) for f, n in (KIT_A4 if formato == 'A4' else KIT_A3)]
    b.append(text(20, y, f'File del kit {formato} (fogli, tutti solo fronte)', 3.4, K, 'start', True)); y += 6
    for f, s, _ in kit:
        b.append(text(24, y, f, 3.2, K) + text(PW - 24, y, s, 3.2, K, 'end')); b.append(line(24, y + 1.3, PW - 24, y + 1.3, 0.1, '#999999')); y += 5.2
    b.append(text(PW - 24, y + 1.5, f'Totale: {sum(n for _, _, n in kit)} fogli {formato}', 3.4, K, 'end', True))
    assert y + 8 < PH - FR - 4
    write('prova_stampa', 1, page(fonts('\n'.join(b)), PW, PH))

# ================================================================== FORMATO A3 (--formato A3)
# Stesse regole dell'A4: tutto a >= 6 mm dal bordo, tutto solo fronte.
A3W, A3H = 297, 420
def hdr3(title, sub, y=11):
    return text(A3W / 2, y, title, 4.2, INK, 'middle', True, SERIF) + text(A3W / 2, y + 5, sub, 2.9, BROWN, 'middle')
def ftr3(lines, y=392):
    return ''.join(text(A3W / 2, y + i * 3.6, l, 2.8, BROWN, 'middle') for i, l in enumerate(lines))

def plancia_a3():
    """Plancia su 2 fogli A3 orizzontali (420 x 297 mm): metà alta e metà bassa a tutta larghezza, sovrapposte
    in una fascia orizzontale con 5 croci di allineamento. Sovrapposizione = 2 x WIN_H - Hb."""
    S = 0.97
    bs = board(W=26)
    m = re.match(r'<svg viewBox="0 0 ([\d.]+) ([\d.]+)"', bs); bw, bh = float(m.group(1)), float(m.group(2))
    Wb, Hb = bw * S, bh * S
    PW, PH = 420, 297
    WIN_W, WIN_H = Wb, 236.0          # finestra per foglio: tutta la larghezza; 236 mm lasciano 38 mm sotto per tacche e note
    PX, PY = (PW - WIN_W) / 2, 13.0
    assert PX - 6.5 >= 6.5 and Hb < 2 * WIN_H
    bd = fonts(inner(bs)).replace('rx="13.0"', 'rx="0"', 1)
    oy = Hb - WIN_H; ovy = WIN_H - oy
    my = (oy + WIN_H) / 2              # croci al centro della fascia di sovrapposizione
    marks_board = [(8, my), (Wb / 4, my), (Wb / 2, my), (3 * Wb / 4, my), (Wb - 8, my)]
    for r, (num, pos) in enumerate((('1 di 2', 'metà alta'), ('2 di 2', 'metà bassa'))):
        wy0 = 0 if r == 0 else oy
        cx0, cx1 = PX - BLEED, PX + WIN_W + BLEED
        cy0 = PY - (BLEED if r == 0 else 0); cy1 = PY + WIN_H + (BLEED if r == 1 else 0)
        cid = f'clip{r}'
        b = [f'<defs><clipPath id="{cid}"><rect x="{cx0}" y="{cy0}" width="{cx1 - cx0}" height="{cy1 - cy0}"/></clipPath></defs>',
             f'<rect id="abbondanza" x="{cx0}" y="{cy0}" width="{cx1 - cx0}" height="{cy1 - cy0}" fill="#efe1c3"/>',
             f'<g id="plancia-{r + 1}di2" clip-path="url(#{cid})"><g transform="translate({PX:.3f},{PY - wy0:.3f}) scale({S})" font-family="{SANS}">{bd}</g></g>']
        for (bx, by) in marks_board:
            if wy0 <= by <= wy0 + WIN_H:
                px, py = PX + bx, PY + by - wy0
                b.append(f'<g id="croce-di-allineamento"><circle cx="{px:.2f}" cy="{py:.2f}" r="1.9" fill="none" stroke="#c0392b" stroke-width="0.2"/>{line(px - 3.5, py, px + 3.5, py, 0.2, "#c0392b")}{line(px, py - 3.5, px, py + 3.5, 0.2, "#c0392b")}</g>')
        b.append(crop_marks(PX, PY, PX + WIN_W, PY + WIN_H, gap=3.5, ln=3.0))
        yf = PY + WIN_H + 9
        b.append(text(PW / 2, yf, f'PLANCIA «Le Terre di Hande» v7 · foglio {num} ({pos}) · A3', 4.0, INK, 'middle', True, SERIF))
        if r == 0:
            ins = ['Foglio base: non si taglia (solo il bianco esterno). Il foglio 2 si sovrappone alla sua fascia in basso.']
        else:
            ins = [f'Taglia il margine bianco in ALTO lungo le tacche (y = {PY:.0f} mm). Sovrapponi il foglio sulla fascia di {ovy:.1f} mm in basso del foglio 1.',
                   'Fai coincidere le 5 croci rosse e il disegno; incolla.']
        for j, l in enumerate(ins): b.append(text(PW / 2, yf + 6 + j * 4.2, l, 2.8, INK, 'middle'))
        b.append(text(PW / 2, yf + 17, f'A3 orizzontale, stampa al 100%. Plancia finita {Wb:.1f} × {Hb:.1f} mm (1 unità del disegno = {S} mm), esagono {26 * S:.1f} mm.', 2.6, BROWN, 'middle'))
        b.append(text(PW / 2, yf + 21, f'Sovrapposizione verticale: 2 × {WIN_H:.0f} − {Hb:.1f} = {ovy:.1f} mm (foglio 1: plancia 0–{WIN_H:.0f} mm; foglio 2: {oy:.1f}–{Hb:.1f} mm).', 2.6, BROWN, 'middle'))
        b.append(text(PW / 2, yf + 25, 'Una plancia in 2 fogli A3. Mappa: bozza v7 per il playtest (10 × 10 esagoni, girata di 180° è identica).', 2.6, BROWN, 'middle'))
        write('plancia', r + 1, page('\n'.join(b), PW, PH))
    return dict(W=Wb, H=Hb, win=(WIN_W, WIN_H), oy=oy, ovy=ovy)

def plance_eroe_a3():
    """4 plance eroe neutre 280 x 194 su 2 fogli A3 verticali, una sopra l'altra: y 13-207 e 219-413."""
    for p in range(2):
        b = [f'<g id="plancia-eroe-{2 * p + j + 1}" transform="translate({(A3W - PB_W) / 2},{13 + j * 206})">{plancia_eroe()}</g>' for j in range(2)]
        write('plance_eroe', p + 1, page(fonts('\n'.join(b)), A3W, A3H))
    return PLANCE, PB_W, PB_H

def rotelle_a3():
    """24 dischi delle plance eroe (una plancia per colonna, una rotella per riga) + i 2 dischi del tavolo, un foglio A3."""
    pitch = DISC_R * 2 + 2 * BLEED; x0 = (A3W - (3 * pitch + 2 * DISC_R)) / 2; y0 = 10.0
    b = dischi_eroe(PLANCE, x0, y0, 4, per_colonna=True)
    ty = y0 + 6 * pitch
    for j, (key, nm, sotto, ic, col) in enumerate(R_TAVOLO):
        b.append(rotella_disco(x0 + DISC_R + j * pitch, ty + DISC_R, col, nm, sotto, ic, TAVOLO_FIN, 'plancia di gioco'))
    tx = x0 + 2 * pitch; yy = ty + 6
    b.append(text(tx, yy, 'Rotelle · A3 · foglio 1 di 1 · solo fronte', 4.0, INK, 'start', True, SERIF)); yy += 6
    for par in ['Colonne: le 4 plance eroe (dischi identici); righe: PV, PV max, ATT, MOV, AR, PL. In basso a sinistra i 2 dischi del tavolo.',
                'Stampa al 100%. Ritaglia ogni disco dove cambia il colore e la finestra bianca; fora il centro con un punteruolo.',
                'Disco sopra la corona con lo stesso nome (plancia eroe o Sala del Tesoro), fermacampioni dal davanti, gambe aperte in orizzontale dietro. 27 fermacampioni con la Rotella della Profezia (foglio delle tessere).']:
        for l in wrap(par, 2.6, 2 * pitch - 8):
            b.append(text(tx, yy, l, 2.6, BROWN)); yy += 3.3
        yy += 1.0
    assert yy < ty + 2 * DISC_R + BLEED
    write('rotelle_eroe', 1, page(fonts('\n'.join(b)), A3W, A3H))
    return 26

def esplorazione_a3():
    """Un foglio A3 solo fronte: in alto le tessere Stato (8 per riga), poi le 36 tessere Esplorazione (Ø 24 mm, 6 x 6,
    retro bianco) e sotto la Rotella della Profezia (disco + base)."""
    rows = read('tessere_esplorazione.csv'); assert len(rows) == 36
    sc_ = 8; sb, sc, sbox = stati(sc_, (A3W - ((sc_ - 1) * (ST_W + 2 * BLEED) + ST_W)) / 2, 28.0)
    D = 24; R = D / 2; cols = 6; pitch = D + 2 * BLEED
    rws = math.ceil(len(rows) / cols)
    gw, gh = (cols - 1) * pitch + D, (rws - 1) * pitch + D
    x0, y0 = (A3W - gw) / 2, sbox[3] + 2 * BLEED + 8
    cs = [(x0 + R + (i % cols) * pitch, y0 + R + (i // cols) * pitch) for i in range(len(rows))]
    b = sb + esplorazione_pezzi(cs, rows, D)
    bb = (x0, y0, x0 + gw, y0 + gh)
    xs = sorted({bb[0] + i * pitch + o for i in range(cols) for o in (0, D)})
    ys = sorted({bb[1] + i * pitch + o for i in range(rws) for o in (0, D)})
    b.append(edge_ticks(xs, ys, bb))
    py = bb[3] + 7.5 + 6 + BASE_PROF / 2
    b.append(profezia_disco(A3W / 2 - 35, py))
    b.append(profezia_base(A3W / 2 + 35, py))
    assert sbox[2] + 7.5 <= A3W - 6.5 and py + BASE_PROF / 2 < 385
    b.insert(0, hdr3('Tessere Stato · Tessere Esplorazione · Rotella della Profezia',
                     f'{sum(sc.values())} tessere Stato 26 × 18 mm · 25 rosse (Mostro) + 11 blu (Imprevisto) Ø {D} mm  ·  foglio 1 di 1  ·  solo fronte, retro bianco'))
    b.append(ftr3(['Stampa su A3 al 100% (nessun adattamento alla pagina), solo fronte. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.'] + ESPL_NOTE +
                  [f'Tessere Stato (in alto): {conta(sc)} (freccia ↑ in alto = dritto).',
                   'Rotella della Profezia (Oracolo): disco sulla base quadrata col fermacampioni. P pari · D dispari · A alto (4+ su D6, 8+ su 2D6) · B basso (3− / 6−).']))
    write('tessere_esplorazione', 1, page(fonts('\n'.join(b)), A3W, A3H))
    return dict(esplorazione=dict(Counter(r['colore'] for r in rows)), stati=sc)

def misti_a3():
    """Un foglio A3 solo fronte: pedine (eroi, MIMI e Geronimo in alto; i 6 Boss nella seconda fila) e segnalini (sotto)."""
    bw = (len(BOSS) - 1) * (GEO['boss']['w'] + 2 * BLEED) + GEO['boss']['w']
    pb, pz = pedine([(EROI + ['Geronimo'], 'eroe', (A3W - (6 * 30 + 24)) / 2, 28.0), (BOSS, 'boss', (A3W - bw) / 2, 124.0)])
    gb, gc, gbox = gettoni(10, (A3W - (9 * 26 + 20)) / 2, 248.0, per_tipo=False)
    assert (A3W - bw) / 2 - BLEED >= 6.5 and 124.0 + 2 * (GEO['boss']['fh'] + GEO['boss']['ph']) + 7.5 < gbox[1] - 7.5 and gbox[3] + 7.5 < 385
    b = [hdr3('Pedine · Segnalini', f'{len(pz)} pedine pieghevoli (6 Boss) · {sum(gc.values())} segnalini Ø 20 mm  ·  foglio 1 di 1  ·  solo fronte, A3 verticale')]
    b += pb + gb
    b.append(ftr3(['Stampa su A3 al 100%, solo fronte. Taglia sul bordo/cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                   'Pedine: piega sulla linea tratteggiata bianca (al centro) e incolla fronte e retro; le linguette chiare fanno da piede a T. Eroi 24 mm, Boss 40 mm.',
                   'Le tessere Stato sono sul foglio delle tessere Esplorazione (tessere_esplorazione.pdf).',
                   f"Segnalini: {gc['Indizio']} Indizi (prima riga e inizio della seconda), {gc['Forte Volontà']} Forte Volontà (fine della seconda), {gc['Usato']} Usato (righe 3-4)."]))
    write('componenti_misti', 1, page(fonts('\n'.join(b)), A3W, A3H))
    return dict(pedine=len(pz), segnalini=gc)

if __name__ == '__main__':
    res = {'rotelle': {k: verifica_rotella(k, vals, win, mh, gold, rr=RAGGIO.get(k, RING_R)) for k, _, _, _, _, vals, win, mh, gold, _ in ROTELLE}}
    res['rotelle']['tavolo'] = verifica_rotella('tavolo', TAVOLO_VALORI, TAVOLO_FIN, 4.5)
    res['rotelle']['Profezia'] = verifica_rotella('Profezia', PROFEZIA_VALORI, PROFEZIA_FIN, PROFEZIA_MH)
    if '--formato' in sys.argv and sys.argv[sys.argv.index('--formato') + 1].upper() == 'A3':
        res['plancia'] = plancia_a3()
        res['plance_eroe'] = plance_eroe_a3()
        res['rotelle_eroe'] = rotelle_a3()
        res['esplorazione'] = esplorazione_a3()
        res['misti'] = misti_a3()
        prova(A3W, A3H, 'A3')
        print(res)
        sys.exit(0)
    res['esplorazione'] = esplorazione()
    res['segnalini'] = segnalini()
    res['plance_eroe'] = plance_eroe()
    res['rotelle_eroe'] = rotelle_eroe()
    res['plancia'] = plancia()
    res['pedine'] = [(n, round(w, 1), round(h, 1)) for n, x, y, w, h in pedine()]
    prova()
    print(res)
