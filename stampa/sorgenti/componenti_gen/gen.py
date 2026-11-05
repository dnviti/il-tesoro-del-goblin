#!/usr/bin/env python3
"""Genera le pagine A4 (SVG in mm) dei componenti non-carta del playtest v5.

Uso: python3 gen.py <cartella_uscita>
Scrive <cartella_uscita>/<componente>/pagina_NN.svg (poi importate in VectorCraft e
esportate in PDF).  Dipende da svg.py + parts_stampa.py (copie dei generatori del repo
regolamento/sorgenti/book, con 2 ritocchi alla scheda: cifre 1-20 sulla traccia PV e
slot Tessera Specie piu' grande) e dai CSV in dati/.
"""
import csv, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import ImageFont
from parts_stampa import *   # icon, board, scheda, colori INK/BROWN/RED/GOLD/BLUE/PAPER...

OUT = sys.argv[1]
DATI = next(p for p in (os.path.join(HERE, 'dati'), os.path.join(HERE, '..', 'dati')) if os.path.isdir(p))
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
def write(comp, n, svg):
    d = os.path.join(OUT, comp); os.makedirs(d, exist_ok=True)
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
def esplorazione():
    rows = read('tessere_esplorazione.csv')
    assert len(rows) == 36
    D = 24; R = D / 2          # esagono della plancia = 25,2 mm da lato a lato: la tessera ci sta dentro
    n = len(rows); cols = 6
    cs, bbox, pitch = disc_grid(n, cols, D)
    rws = math.ceil(n / cols)
    counts = {}
    for r in rows: counts[r['colore']] = counts.get(r['colore'], 0) + 1
    for pn, side in ((1, 'fronte'), (2, 'retro')):
        # retro: stesso disegno (il colore deve restare visibile qualunque faccia esca dal sacchetto),
        # posizioni specchiate sul lato lungo (x -> 210-x): il retro cade dietro al fronte.
        pos = cs if side == 'fronte' else [(210 - x, y) for x, y in cs]
        b = [bleed_disc(x, y, R, r['colore_esadecimale']) for (x, y), r in zip(pos, rows)]
        b += [disc_piece(x, y, R, r['colore_esadecimale'], r['icona'], r['etichetta_fronte'], '#ffffff', '#ffffff') for (x, y), r in zip(pos, rows)]
        b += [cut_disc(x, y, R) for x, y in pos]
        bb = (210 - bbox[2], bbox[1], 210 - bbox[0], bbox[3]) if side == 'retro' else bbox
        xs = sorted({bb[0] + i * pitch + o for i in range(cols) for o in (0, D)})
        ys = sorted({bb[1] + i * pitch + o for i in range(rws) for o in (0, D)})
        b.append(edge_ticks(xs, ys, bb))
        t = f'Tessere Esplorazione · 25 rosse (Mostro) + 11 blu (Imprevisto) · Ø {D} mm'
        st = ('FRONTE. Stampa fronte-retro: ribaltamento sul lato LUNGO (pagina 2 = retro).' if side == 'fronte'
              else 'RETRO, già specchiato sul lato lungo: dietro a ogni tessera c’è la stessa tessera.')
        b.insert(0, hdr(t, st))
        b.append(ftr(['Stampa su A4 al 100% (nessun adattamento alla pagina). Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                      'Retro identico al fronte: le tessere escono dal sacchetto e il colore (rosso = Mostro, blu = Imprevisto) si legge da ogni lato.',
                      'Ordine: le prime 25 (righe 1-4 e la prima della riga 5) sono rosse, le altre 11 blu.']))
        write('tessere_esplorazione', pn, page(fonts('\n'.join(b))))
    return counts

# ------------------------------------------------------------------ SEGNALINI
def segnalini():
    rows = read('segnalini.csv')
    D = 20; R = D / 2
    spec = {'Indizio': ('pergamena', INK, '#efe1c3'), 'Clessidra': ('clessidra', INK, '#efe1c3'), 'Forte Volontà': ('stella', GOLD, '#efe1c3')}
    items = []
    for r in rows:
        ic, col, fill = spec[r['nome']]
        items += [(r['nome'], ic, col, fill)] * int(r['copie'])
    assert len(items) == 28
    cols = 6
    # una riga (6 pezzi) per tipo: 12 = 2 righe, 12 = 2 righe, 4 = 1 riga -> 5 righe
    pitch = D + 2 * BLEED
    # righe per tipo
    layout = []; row = 0
    for r in rows:
        n = int(r['copie'])
        for i in range(n):
            layout.append((r['nome'], row + i // cols, i % cols))
        row += math.ceil(n / cols)
    nrows = row
    gw = (cols - 1) * pitch + D; gh = (nrows - 1) * pitch + D
    x0 = (210 - gw) / 2; y0 = (297 - gh) / 2
    b = []; pos = []
    for nome, rr, cc in layout: pos.append((nome, x0 + R + cc * pitch, y0 + R + rr * pitch))
    b += [bleed_disc(x, y, R, spec[nome][2]) for nome, x, y in pos]
    for nome, x, y in pos:
        ic, col, fill = spec[nome]
        b.append(disc_piece(x, y, R, fill, ic, nome, col, INK, 1.2))
    b += [cut_disc(x, y, R) for _, x, y in pos]
    bb = (x0, y0, x0 + gw, y0 + gh)
    xs = sorted({x0 + i * pitch + o for i in range(cols) for o in (0, D)}); ys = sorted({y0 + i * pitch + o for i in range(nrows) for o in (0, D)})
    b.append(edge_ticks(xs, ys, bb))
    b.insert(0, hdr('Segnalini', f'12 Indizi · 12 Clessidre · 4 Forte Volontà  ·  Ø {D} mm  ·  solo fronte'))
    b.append(ftr(['Stampa su A4 al 100%. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                  'Prima 2 righe di Indizi, poi 2 di Clessidre, poi 1 di Forte Volontà.']))
    write('segnalini', 1, page(fonts('\n'.join(b))))
    from collections import Counter
    return dict(Counter(n for n, _, _ in pos))

# ------------------------------------------------------------------ TESSERE SPECIE
SPECIE_COL = {'Umano': '#4a5568', 'Elfo': '#2f7a8a', 'Sanguar': '#7a2f4f', 'Yumaniano': '#8a6a1c'}
def specie():
    rows = read('tessere_specie.csv'); assert len(rows) == 8
    W, H = 50, 25
    pitchx, pitchy = W + 2 * BLEED + 2, H + 2 * BLEED + 2
    cols, nr = 2, 4
    gw, gh = (cols - 1) * pitchx + W, (nr - 1) * pitchy + H
    x0, y0 = (210 - gw) / 2, (297 - gh) / 2
    b = [hdr('Tessere Specie', f'8 pezzi (2 per specie)  ·  {W} × {H} mm  ·  solo fronte'),]
    pcs = []
    for i, r in enumerate(rows):
        x = x0 + (i % cols) * pitchx; y = y0 + (i // cols) * pitchy
        pcs.append((x, y, r))
    for x, y, r in pcs:   # abbondanza
        b.append(f'<rect x="{x - BLEED}" y="{y - BLEED}" width="{W + 2 * BLEED}" height="{H + 2 * BLEED}" fill="{mix(SPECIE_COL[r["specie"]], 0.6)}"/>')
    for x, y, r in pcs:
        c = SPECIE_COL[r['specie']]
        b.append(f'<rect x="{x + 0.3}" y="{y + 0.3}" width="{W - 0.6}" height="{H - 0.6}" rx="2" fill="#fffaf0" stroke="{c}" stroke-width="0.6"/>')
        b.append(f'<path d="M{x + 0.3} {y + 7.4} V{y + 2.3} a2 2 0 0 1 2 -2 H{x + W - 2.3} a2 2 0 0 1 2 2 V{y + 7.4} Z" fill="{c}"/>')
        b.append(text(x + W / 2, y + 5.6, r['specie'], 4.2, '#ffffff', 'middle', True, SERIF))
        bonus = r['bonus']; prov = r['provvisorio'] == 'PROVVISORIO'
        fs = 3.0
        lines = wrap(bonus, fs, W - 5, SERIF)
        for j, l in enumerate(lines):
            if prov and l.endswith('(PROVVISORIO)'):
                head = l[:-len('(PROVVISORIO)')]
                t = text(x + 2.5, y + 12.3 + j * 3.3, head, fs, INK, 'start', False, SERIF)
                wd = tw(head, fs, SERIF)
                t += text(x + 2.5 + wd, y + 12.3 + j * 3.3, '(PROVVISORIO)', fs - 0.2, RED, 'start', True, SERIF)
                b.append(t)
            else:
                b.append(text(x + 2.5, y + 12.3 + j * 3.3, l, fs, INK, 'start', False, SERIF))
        fl = wrap(r['nota_a_piè'], 2.0, W - 5, SANS)
        for j, l in enumerate(fl):
            b.append(text(x + 2.5, y + 20.2 + j * 2.4, l, 2.0, BROWN, 'start', False, SANS, italic=True))
        b.append(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="2.3" fill="none" stroke="{CUT}" stroke-width="0.12" opacity="0.7"/>')
    xs = sorted({x0 + i * pitchx + o for i in range(cols) for o in (0, W)}); ys = sorted({y0 + i * pitchy + o for i in range(nr) for o in (0, H)})
    b.append(edge_ticks(xs, ys, (x0, y0, x0 + gw, y0 + gh)))
    b.append(ftr(['Stampa su A4 al 100%. Taglia sul bordo sottile; l’abbondanza di 3 mm esce dal taglio.',
                  'La tessera si appoggia nello slot «Tessera Specie» della scheda eroe (slot 52,6 × 26,3 mm; tessera 50 × 25 mm).',
                  'Il bonus dello Yumaniano è PROVVISORIO (la bozza dice «Da decidere»).']))
    write('tessere_specie', 1, page(fonts('\n'.join(b))))
    from collections import Counter
    return dict(Counter(r['specie'] for r in rows))

# ------------------------------------------------------------------ SCHEDE EROE
CLASSI = [('Assaltatore', '#9c2f24'), ('Ricercatore', '#3b7d4f'), ('Stregone', '#5b4a9c'), ('Oracolo', '#b8862b')]
def schede():
    sv = fonts(inner(scheda()))
    SW = 222.0; k = SW / 540; SHH = 430 * k
    x0 = (297 - SW) / 2; y0 = 25.0
    for i, (nome, col) in enumerate(CLASSI):
        b = [text(x0, 14, f'Scheda eroe · {nome}', 7.0, col, 'start', True, SERIF),
             text(x0 + SW, 14, 'A4 orizzontale · stampa al 100% · solo fronte', 3.0, BROWN, 'end'),
             f'<rect x="{x0}" y="16" width="{SW}" height="1.2" fill="{col}"/>',
             f'<g id="scheda" font-family="{SANS}" transform="translate({x0:.3f},{y0}) scale({k:.5f})">{sv}</g>',
             f'<rect x="{x0}" y="{y0}" width="{SW}" height="{SHH:.2f}" fill="none" stroke="{CUT}" stroke-width="0.12" opacity="0.5"/>',
             crop_marks(x0, y0, x0 + SW, y0 + SHH, gap=3, ln=3.5)]
        write('schede_eroe', i + 1, page('\n'.join(b), 297, 210))
    return len(CLASSI), SW, SHH

# ------------------------------------------------------------------ PLANCIA
def plancia():
    S = 0.97
    bs = board(W=26)
    m = re.match(r'<svg viewBox="0 0 ([\d.]+) ([\d.]+)"', bs); bw, bh = float(m.group(1)), float(m.group(2))
    Wb, Hb = bw * S, bh * S
    WIN_W, WIN_H = 186.0, 232.0
    PX, PY = 12.0, 12.0
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
        b.append(crop_marks(PX, PY, PX + WIN_W, PY + WIN_H, gap=4, ln=3.5))
        # tacche di taglio sui bordi interni
        cut_l = c == 1; cut_t = r == 1
        yf = PY + WIN_H + 9
        b.append(text(105, yf, f'PLANCIA «Le Terre di Hande» · foglio {num} ({pos})', 4.0, INK, 'middle', True, SERIF))
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
        b.append(text(105, yf + 25, 'Una plancia stampata in 4 fogli A4; il disegno è un 10 × 10 di esagoni, girato di 180° è identico.', 2.6, BROWN, 'middle'))
        write('plancia', c + 2 * r + 1, page('\n'.join(b)))
    return dict(W=Wb, H=Hb, win=(WIN_W, WIN_H), ox=ox, oy=oy, ovx=ovx, ovy=ovy)

# ------------------------------------------------------------------ PEDINE
PAWNS = {  # nome: (icona, colore, tipo, riga)
    'Assaltatore': ('spade', '#9c2f24', 'eroe', 0), 'Ricercatore': ('occhio', '#3b7d4f', 'eroe', 0),
    'Stregone': ('stella', '#5b4a9c', 'eroe', 0), 'Oracolo': ('cuore', '#b8862b', 'eroe', 0),
    'MIMI': ('forziere', '#6b4a2b', 'forziere', 0), 'Geronimo': ('bandiera', '#4a6a2f', 'primo giocatore', 0),
    'Guardiano di MIMI': ('scudo', '#2b1d14', 'boss', 1), 'Mimic ancestrale': ('forziere', '#2b1d14', 'boss', 1),
    'Re Goblin Grugno': ('teschio', '#2b1d14', 'boss', 1)}
def pedine():
    rows = read('pedine.csv'); assert len(rows) == 9
    b = [hdr('Pedine e sagome', '4 eroi · MIMI · Geronimo · 3 Boss  ·  pieghevoli fronte/retro  ·  solo fronte, A4 verticale')]
    geo = {0: dict(w=24.0, ph=34.0, fh=7.0), 1: dict(w=40.0, ph=44.0, fh=8.0)}
    rows_by = {0: [], 1: []}
    for r in rows: rows_by[PAWNS[r['nome']][3]].append(r)
    y = 28.0; out = []
    allx = []; ally = []
    for rr in (0, 1):
        g = geo[rr]; w, ph, fh = g['w'], g['ph'], g['fh']; H = 2 * (fh + ph)
        n = len(rows_by[rr]); pitch = w + 2 * BLEED
        gw = (n - 1) * pitch + w; x0 = (210 - gw) / 2
        for i, r in enumerate(rows_by[rr]):
            ic, col, tipo, _ = PAWNS[r['nome']]
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
                mr = min(w * 0.31, ph * 0.26) if rr == 0 else 8.6
                my = py + 4.2 + mr if rr == 0 else py + 5 + mr
                p.append(f'<circle cx="{cx:.2f}" cy="{my:.2f}" r="{mr:.2f}" fill="#f4ead5"/>')
                p.append(icon(ic, cx, my, mr * 1.3 / 24 * 1.0, col))
                nm = r['nome']
                fs = 3.6 if rr == 0 else 4.6
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
            out.append((r['nome'], x, y, w, H))
            allx += [x, x + w]
        ally += [y, y + H]
        row_box = (x0, y, x0 + gw, y + H)
        xs = sorted({x0 + i * pitch + o for i in range(n) for o in (0, w)})
        b.append(edge_ticks(xs, [y, y + H], row_box, gap=4, ln=3.5).replace('tacche-di-taglio', f'tacche-riga{rr + 1}'))
        y += H + 2 * BLEED + 8
    b.append(ftr(['Stampa su A4 al 100%. Ritaglia il rettangolo di ogni pedina. Piega sulla linea tratteggiata bianca (al centro) e incolla fronte e retro.',
                  'Piega le due linguette chiare (tratteggio grigio) una in avanti e una indietro: ottieni un piede a T per far stare in piedi la sagoma.',
                  'Eroi, MIMI e Geronimo: larghezza 24 mm (stanno in un esagono). Boss: 40 mm (stanno nei cerchi della Sala del Tesoro). Colori degli eroi = colori dei dorsi di classe.']))
    write('pedine', 1, page(fonts('\n'.join(b))))
    return out

if __name__ == '__main__':
    res = {}
    res['esplorazione'] = esplorazione()
    res['segnalini'] = segnalini()
    res['specie'] = specie()
    res['schede'] = schede()
    res['plancia'] = plancia()
    res['pedine'] = [(n, round(w, 1), round(h, 1)) for n, x, y, w, h in pedine()]
    print(res)
