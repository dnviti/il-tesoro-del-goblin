#!/usr/bin/env python3
"""Genera le pagine (SVG in mm) dei componenti non-carta del playtest v7. Tutto SOLO FRONTE, tranne i fiori della
mappa (mappa_fiori: fronte/retro manuale, retro specchiato sul lato lungo).

Uso: python3 gen.py <cartella_uscita> [--formato A3] [--dati CARTELLA] [--arte-mappa CARTELLA]
Scrive <cartella_uscita>/<componente>/pagina_NN.svg (poi importate in VectorCraft e esportate in PDF da build.sh).
A4: mappa_base (2, la base 12×12 in due metà), mappa_fiori (6 pagine = 3 fogli fronte/retro: 14 fiori e la Cripta;
niente segnaposto «?», D29), mappa_preset (10, carta comune), sala_tesoro (1), plance_eroe (4, A4 orizzontale), rotelle_eroe (2),
tessere_esplorazione (1), segnalini (2), pedine (2), prova_stampa (1). A3: sala_tesoro (1, A3 orizzontale), plance_eroe
(2), rotelle_eroe (1), tessere_esplorazione (1, con le tessere Stato e la Rotella della Profezia), componenti_misti (1,
pedine e segnalini), prova_stampa (1); la mappa A3 non c'è (si stampano i PDF A4 della mappa).
Mappa 12×12 a fiori (12/11, D24, D25): dati in dati/fiori.csv, base12.csv, preset12.csv (scritti da
../../../idee/mappa_tessere/12x12/mappa12.py --scrivi-dati), disegno dei pezzi in fiori12.py.
v7: plance eroe neutre (D14: niente classe né specie stampate), rotella PL 0-12 al posto di PE/livello (D2), pedina del
Giullare (5 classi).
Dipende da svg.py + parts_stampa.py (icone, Sala del Tesoro, corone delle rotelle), fiori12.py, dai CSV in dati/, dalle
illustrazioni arte/png/PD-* e PS-BASE e, per l'elenco dei file della prova di stampa, da ../carte/genera_carte.py (conta
i fogli delle carte). Prima di scrivere controlla che ogni finestra delle rotelle mostri un solo valore (verifica_rotella).
"""
import csv, math, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True     # niente __pycache__ accanto a gen.py e a carte/
sys.path.insert(0, HERE)
from PIL import ImageFont
from parts_stampa import *   # icon, dial_ring, colori INK/BROWN/RED/GOLD/BLUE/PAPER...

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

def fregio(cx, y, title, size, half):
    """kit dei motivi: filetto d'ottone con una losanga di rame ai due lati di un titolo (corpo size, centrato su cx);
    half = mezza larghezza del foglio: il fregio resta a >= 8 mm dal bordo (se non c'è posto, niente fregio)."""
    a = tw(title, size, SERIF, True) / 2 + size * 0.9; yy = y - size * 0.34
    lung = min(18.0, half - 8 - a - 3)
    if lung < 4: return ''
    return ''.join(line(cx + s * a, yy, cx + s * (a + lung), yy, 0.25, BRASS) + lozenge(cx + s * (a + lung + 1.5), yy, 3.0, 1.5, COPPER)
                   for s in (-1, 1))

def hdr(title, sub, y=11):
    return text(105, y, title, 4.2, INK, 'middle', True, SERIF) + fregio(105, y, title, 4.2, 105) + text(105, y + 5, sub, 2.9, BROWN, 'middle')
def ftr(lines, y=283):
    return ''.join(text(105, y + i * 3.6, l, 2.8, BROWN, 'middle') for i, l in enumerate(lines))

def read(name): return list(csv.DictReader(open(os.path.join(DATI, name), encoding='utf-8')))

def mix(h, f):  # schiarisce un esadecimale mescolando col bianco
    r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    r, g, b = [round(v + (255 - v) * f) for v in (r, g, b)]
    return f'#{r:02x}{g:02x}{b:02x}'

# ------------------------------------------------------------------ pezzi tondi
def arco_manometro(cx, cy, r, col, a=115):
    """kit dei motivi sui pezzi tondi: arco sottile «a manometro» da -a a +a gradi (0 = in alto) con un rivetto a ogni
    estremità; la parte bassa resta libera per la scritta."""
    p = [(cx + r * math.sin(math.radians(s * a)), cy - r * math.cos(math.radians(s * a))) for s in (-1, 1)]
    return (f'<path d="M{p[0][0]:.3f} {p[0][1]:.3f}A{r:.3f} {r:.3f} 0 1 1 {p[1][0]:.3f} {p[1][1]:.3f}" fill="none" stroke="{col}" stroke-width="0.2"/>'
            + ''.join(rivet(x, y, 0.35, col, None) for x, y in p))

def disc_piece(cx, cy, R, fill, ic, label, icol, lcol, ks=1.0, filo=BRASS_L):
    """tessera/segnalino tondo, come color_token()/simple_token() ma in mm; R = raggio di taglio; filo: colore dell'arco
    d'ottone dentro il bordo (chiaro sui fondi colorati, scuro sui fondi chiari)."""
    s = 2 * R; k = 0.9 * s / 46 * ks
    sw = 0.043 * s
    o = []
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R - sw / 2:.2f}" fill="{fill}" stroke="{BROWN}" stroke-width="{sw:.2f}"/>')
    o.append(arco_manometro(cx, cy, R - sw - 0.8, filo))
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
def disco_arte(nome, x, y, R, cart, label=None, lcol=None):
    """disco con l'arte generata (arte/png/<nome>.png, vedi mappa_compone.py): immagine tagliata sul cerchio R + BLEED, anello
    d'ottone sul taglio e, se label, la scritta in basso con contorno pergamena. None se manca il png (si usa il vettoriale)."""
    img = F12.immagine_arte(nome, x, y, cart)
    if not img:
        return None
    cid = f'da{abs(hash((nome, round(x), round(y)))) % 10**8}'
    o = [f'<clipPath id="{cid}"><circle cx="{x:.2f}" cy="{y:.2f}" r="{R + BLEED:.2f}"/></clipPath><g clip-path="url(#{cid})">{img}</g>',
         f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{R - 0.3:.2f}" fill="none" stroke="{BRASS}" stroke-width="0.5"/>']
    if label:
        o.append(f'<text x="{x:.2f}" y="{y + R * 0.78:.2f}" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-size="{R * 0.3:.2f}" '
                 f'fill="{lcol or INK}" stroke="#fffaf0" stroke-width="{R * 0.07:.2f}" stroke-linejoin="round" paint-order="stroke">{esc(label)}</text>')
    return ''.join(o)

def esplorazione_pezzi(cs, rows, D, cart=None):
    R = D / 2
    b = [bleed_disc(x, y, R, r['colore_esadecimale']) for (x, y), r in zip(cs, rows)]
    arte = {'rossa': 'TX-ROSSA', 'blu': 'TX-BLU'}
    for (x, y), r in zip(cs, rows):
        d = cart and disco_arte(arte.get(r['colore'], ''), x, y, R, cart, r['etichetta_fronte'], INK)
        b.append(d or disc_piece(x, y, R, r['colore_esadecimale'], r['icona'], r['etichetta_fronte'], '#ffffff', '#ffffff'))
    b += [cut_disc(x, y, R) for x, y in cs]
    return b

ESPL_NOTE = ['Dorso coperto alla pagina 2 (fronte/retro a mano, lato lungo): le tessere stanno coperte sulla mappa (24) e nella riserva (12); la rossa rimasta sta a faccia in su.',
             'Ordine: le prime 25 (righe 1-4 e la prima della riga 5) sono rosse, le altre 11 blu.']
def esplorazione():
    """36 tessere Ø 24 su un foglio A4, solo fronte (retro bianco)."""
    rows = read('tessere_esplorazione.csv')
    assert len(rows) == 36
    D = 24; n = len(rows); cols = 6       # esagono della plancia = 25,2 mm da lato a lato: la tessera ci sta dentro
    cs, bbox, pitch = disc_grid(n, cols, D)
    rws = math.ceil(n / cols)
    b = esplorazione_pezzi(cs, rows, D, os.path.join(OUT, 'tessere_esplorazione'))
    xs = sorted({bbox[0] + i * pitch + o for i in range(cols) for o in (0, D)})
    ys = sorted({bbox[1] + i * pitch + o for i in range(rws) for o in (0, D)})
    b.append(edge_ticks(xs, ys, bbox))
    b.insert(0, hdr(f'Tessere Esplorazione · 25 rosse (Mostro) + 11 blu (Imprevisto) · Ø {D} mm', 'Pagina 1 di 2: fronti · il dorso coperto è alla pagina 2, fronte/retro sul lato lungo.'))
    b.append(ftr(['Stampa su A4 al 100% (nessun adattamento alla pagina), solo fronte. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.'] + ESPL_NOTE))
    write('tessere_esplorazione', 1, page(fonts('\n'.join(b))))
    # dorso (TX-RETRO) sull'altra pagina, specchiato sul lato lungo come i fiori: il dorso del posto (x, y) sta in (210 - x, y)
    cart = os.path.join(OUT, 'tessere_esplorazione')
    r_ = [f'<circle cx="{210 - x:.2f}" cy="{y:.2f}" r="{D / 2 + BLEED:.2f}" fill="#8a5a33"/>' for x, y in cs]
    r_ += [disco_arte('TX-RETRO', 210 - x, y, D / 2, cart) or '' for x, y in cs]
    r_.insert(0, hdr('Tessere Esplorazione · dorso (coperte)', 'Pagina 2: dorso coperto, specchiato sul LATO LUNGO per il fronte/retro manuale · senza linee di taglio'))
    r_.append(ftr(['Stampa la pagina 1, rimetti il foglio nel cassetto girato sul LATO LUNGO e stampa questa pagina; poi taglia sul cerchio del fronte.',
                   'Controlla in controluce: il cerchio del fronte deve cadere dentro l’abbondanza del dorso. Senza fronte-retro: stampa solo la pagina 1 (dorso bianco).']))
    write('tessere_esplorazione', 2, page(fonts('\n'.join(r_))))
    return dict(Counter(r['colore'] for r in rows))

# ------------------------------------------------------------------ SEGNALINI (Ø 20) E TESSERE STATO (26 x 18)
SEGN = {'Indizio': ('pergamena', INK, '#efe1c3', 'Indizio'),
        'Forte Volontà': ('stella', GOLD, '#efe1c3', 'Forte Volontà'),
        'Usato': ('spunta', '#2f6b3f', '#dcebd8', 'USATO')}
SEGN_ARTE = {'Indizio': 'SG-01', 'Forte Volontà': 'SG-03', 'Usato': 'SG-04'}
def gettoni(cols, x0, y0, per_tipo=True, cart=None):
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
        d = cart and disco_arte(SEGN_ARTE[nm], x, y, R, cart, lab.upper() if len(lab) < 8 else lab, INK)
        b.append(d or disc_piece(x, y, R, fill, ic, lab, col, INK, 1.2, BRASS))
    b += [cut_disc(x, y, R) for _, x, y in pos]
    xs = sorted({x0 + i * pitch + o for i in range(cols) for o in (0, D)}); ys = sorted({y0 + i * pitch + o for i in range(nrows) for o in (0, D)})
    bb = (x0, y0, x0 + gw, y0 + gh)
    b.append(edge_ticks(xs, ys, bb))
    return b, dict(Counter(items)), bb

STATO_COL = {'+': '#3b7d4f', '−': '#9c2f24'}
ST_W, ST_H = 26.0, 18.0
ST_BANDA = 7.0       # bandella del nome, in alto
ST_NOME_MIN = 3.2    # corpo minimo del nome in mm (9 pt, il minimo delle etichette del kit)
def stati(cols, x0, y0, cart=None):
    """tessere Stato 26 x 18 (D27, 13/11): solo nome, icona e segno. Bandella in alto nel colore del segno (verde = +,
    aiuta; rossa = −, ostacola) col nome grande; sotto, il segno grande in un tondo, l'illustrazione ST-xx e la freccia ↑
    (punta in alto: tessera verticale; di lato: orizzontale, R 9.1). Gli effetti stanno sulle Carte Aiuto. Ritorna (svg,
    conteggi, bbox)."""
    rows = read('stati.csv')
    items = [r for r in rows for _ in range(int(r['copie']))]
    assert items
    px, py = ST_W + 2 * BLEED, ST_H + 2 * BLEED
    nr = math.ceil(len(items) / cols)
    gw, gh = (cols - 1) * px + ST_W, (nr - 1) * py + ST_H
    pcs = [(x0 + (i % cols) * px, y0 + (i // cols) * py, r) for i, r in enumerate(items)]
    b = []
    for n, (x, y, r) in enumerate(pcs):
        c = STATO_COL[r['segno']]
        b.append(f'<rect x="{x - BLEED:.2f}" y="{y - BLEED:.2f}" width="{ST_W + 2 * BLEED}" height="{ST_H + 2 * BLEED}" fill="#fffaf0"/>')
        b.append(f'<rect x="{x - BLEED:.2f}" y="{y - BLEED:.2f}" width="{ST_W + 2 * BLEED}" height="{BLEED + ST_BANDA}" fill="{c}"/>')
        # kit dei motivi: filetto doppio d'ottone sotto la bandella
        b.append(line(x - BLEED, y + ST_BANDA, x + ST_W + BLEED, y + ST_BANDA, 0.35, BRASS)
                 + line(x - BLEED, y + ST_BANDA + 0.65, x + ST_W + BLEED, y + ST_BANDA + 0.65, 0.12, BRASS))
        fs = 4.4
        while tw(r['nome'], fs, SANS, True) > ST_W - 2.4: fs -= 0.1
        assert fs >= ST_NOME_MIN, f"{r['nome']}: nome della tessera Stato sotto {ST_NOME_MIN} mm"
        b.append(text(x + ST_W / 2, y + ST_BANDA / 2 + fs * 0.36, r['nome'], fs, '#ffffff', 'middle', True))
        ym = y + ST_BANDA + (ST_H - ST_BANDA) / 2 + 0.3            # asse della parte sotto la bandella
        b.append(f'<circle cx="{x + 4.4:.2f}" cy="{ym:.2f}" r="3.4" fill="{c}" stroke="{BRASS}" stroke-width="0.3"/>'
                 + text(x + 4.4, ym + 2.2, r['segno'], 6.2, '#ffffff', 'middle', True))
        isz = ST_H - ST_BANDA - 1.6
        ix, iy = x + ST_W / 2 - isz / 2, ym - isz / 2
        if cart and os.path.isfile(os.path.join(F12.ARTE_MAPPA, r['id'] + '.png')):   # illustrazione 30 mm a 300 ppi, ridotta
            b.append(f'<clipPath id="stc{n}"><rect x="{ix:.2f}" y="{iy:.2f}" width="{isz:.2f}" height="{isz:.2f}" rx="0.8"/></clipPath>'
                     f'<g clip-path="url(#stc{n})"><image href="{os.path.relpath(os.path.join(F12.ARTE_MAPPA, r["id"] + ".png"), cart).replace("&", "&amp;")}" '
                     f'x="{ix:.3f}" y="{iy:.3f}" width="{isz:.2f}" height="{isz:.2f}" preserveAspectRatio="none"/></g>'
                     f'<rect x="{ix:.2f}" y="{iy:.2f}" width="{isz:.2f}" height="{isz:.2f}" rx="0.8" fill="none" stroke="{BRASS}" stroke-width="0.3"/>')
        ax = x + ST_W - 3.6   # freccia ↑: la tessera è verticale quando punta in alto
        b.append(f'<path d="M{ax:.2f} {ym + 3.2:.2f}V{ym - 3.2:.2f}M{ax - 1.6:.2f} {ym - 1.4:.2f}L{ax:.2f} {ym - 3.3:.2f}L{ax + 1.6:.2f} {ym - 1.4:.2f}" fill="none" stroke="{c}" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/>')
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
# PV (Spec R 2.3): punti vita dell'eroe, ogni valore da 5 a 13, perché le carte li cambiano di 1 alla volta (la vecchia
# rotella dei PV massimi). Danni (13/11, Daniele): i danni subiti, contati in su da 0 a 13 (la vecchia rotella dei PV attuali).
ROTELLE = [
    ('PV', 'PV', 'punti vita', 'cuore', RED, [(str(v), ()) for v in range(5, 14)], (11.0, 9.0), 4.5, (), ()),
    ('DANNI', 'Danni', 'danni subiti', 'teschio', INK, [(str(v), ()) for v in range(14)], (9.0, 9.0), 4.0, (), ()),
    ('ATT', 'ATT', 'attacco', 'spade', INK, [(str(v), ()) for v in range(1, 9)], (11.0, 9.0), 4.5, (), ()),
    ('MOV', 'MOV', 'movimento', 'stivale', BROWN, [('−1' if v < 0 else str(v), ()) for v in range(-1, 9)], (11.0, 9.0), 4.5, (), ()),
    ('AR', 'AR', 'armatura', 'scudo', BLUE, [(str(v), ()) for v in range(9, 21)], (11.0, 9.0), 4.5, (), ()),
    ('PL', 'PL', 'power level', 'stella', GOLD, [(str(v), ()) for v in range(13)], (9.0, 9.0), 4.2, (), ())]
R_TAVOLO = [('scontro', 'PV del mostro', 'Rotella dello scontro', 'teschio', '#a8352a'),
            ('custode', 'PV del custode', 'le ferite restano', 'scudo', '#6b4a2b')]
TAVOLO_VALORI = [(str(v), ()) for v in range(10)]; TAVOLO_FIN = (11.0, 9.0)   # corona 0-9 di svg.sala_tesoro()
SF, GAP = 2.0, 0.6   # righe piccole della corona (corpo, interlinea): come i default di svg.dial_block

GOLD_R = 4.8   # raggio del cerchio dorato dietro alle etichette «dorate» (svg.dial_ring)
RAGGIO = {}   # corone con un raggio diverso da RING_R (v6: PE a 19 mm; nella v7 nessuna)
FORO_ADESIVO_R = 6.5   # raggio del foro al centro dell'adesivo delle rotelle 3D (segnalini_3d.pdf): mozzo_r 6,25 + gioco_carta 0,25
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
         f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R - 1.4:.2f}" fill="none" stroke="{BRASS_L}" stroke-width="0.3" opacity="0.9"/>']
    # kit dei motivi: rivetti sull'anello, tranne in alto (la finestra)
    o += [rivet(cx + (R - 1.4) * math.sin(math.radians(a)), cy - (R - 1.4) * math.cos(math.radians(a)), 0.45, BRASS_L, None) for a in range(60, 360, 60)]
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
    # cerchio tratteggiato = foro dell'adesivo della rotella 3D (mozzo_r + gioco_carta di 3d_solidcraft: lì sta il fermo del perno)
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{FORO_ADESIVO_R}" fill="none" stroke="#ffffff" stroke-width="0.25" stroke-dasharray="0.9 0.7"/>')
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
CELLE = {'PV': (142, 18), 'DANNI': (209, 18), 'ATT': (142, 76), 'MOV': (209, 76), 'AR': (142, 134), 'PL': (209, 134)}
TAGLIO = '#d0312d'   # linee da incidere
NOTE_ROT = {'PV': ['punti vita'], 'DANNI': ['danni subiti', 'Danni = PV: sconfitto'], 'ATT': ['attacco', '2D6 + ATT'],
            'MOV': ['movimento', 'D6 + MOV'], 'AR': ['armatura', 'ti colpisce chi fa 2D6 + ATT ≥ AR'], 'PL': ['power level', 'somma dei PL negli slot']}
MONTAGGIO = {
    'Carta Classe': ['1 · Incidi col taglierino le linee rosse: 4 fessure in alto e i tagli ai 4 angoli dei due riquadri.',
                     '2 · Fora il centro segnato delle 6 rotelle: col punteruolo per il fermacampioni, Ø 4 mm per il perno 3D.',
                     '3 · Monta i 6 dischi (rotelle_eroe.pdf) sopra la corona col loro nome, fermacampioni dal davanti e gambe aperte sul retro, o perno 3D dal retro e fermo davanti.',
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
    o.append(line(140, 19, 140, PB_H - 3, 0.3, LINE))
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
    # riquadro Stati: 4 posti da 30 x 32 (tessera 26 x 18 verticale o 18 x 26 orizzontale)
    o.append(f'<rect x="4" y="144" width="134" height="32" rx="3" fill="#fbf6ea" stroke="{BROWN}" stroke-width="0.3"/>')
    o.append(text(5.8, 151.5, 'Stati', 3.6, INK, 'start', True))
    yy = 156.0
    for par in ['verticale: toglilo alla tua Fine', 'orizzontale: giralo in verticale alla tua Fine']:
        for l in wrap(par, 2.1, 11.6):
            o.append(text(5.8, yy, l, 2.1, BROWN)); yy += 2.6
        yy += 0.8
    assert yy < 176
    for i in range(4):
        cx, cy = 33 + 30 * i, 160
        o.append(f'<rect x="{cx - 13}" y="{cy - 9}" width="26" height="18" rx="1.2" fill="none" stroke="{LINE}" stroke-width="0.3" stroke-dasharray="1.2 1"/>')
        o.append(f'<rect x="{cx - 9}" y="{cy - 13}" width="18" height="26" rx="1.2" fill="none" stroke="{LINE}" stroke-width="0.3" stroke-dasharray="0.5 1"/>')
    # promemoria
    prom = ['Si parte da PV 5 · Danni 0 · ATT 1 · MOV 1 · AR 9 · PL 0, poi aggiungi il bonus della Carta Specie.',
            'Le statistiche cambiano solo con carte, Equipaggiamenti e Stati. Equipaggi o perdi un oggetto: gira subito le rotelle, PL compreso.',
            'Fine del turno: togli gli Stati verticali, gira in verticale gli orizzontali, togli gli Usato «una volta per turno» e i segnaposto.']
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
        o.append(text(xc + 7, yc + 47, 'foro al centro', 1.8, BROWN, 'middle'))
        o.append(text(xc + 7, yc + 49.4, 'Ø 4 per il perno 3D', 1.8, BROWN, 'middle'))
    o.append(text(142, 191.0, 'Il Tesoro del Goblin · playtest v7', 2.4, BROWN))
    o.append(text(274.5, 191.0, 'Plancia eroe', 2.8, col, 'end', True, SERIF))
    # kit dei motivi: filetto doppio d'ottone a 1,2 / 2 mm dal taglio, ingranaggi agli angoli
    o.append(brass_frame(1.2, 1.2, PB_W - 1.2, PB_H - 1.2, holes=(mix(col, 0.8),) * 2 + ('#ffffff',) * 2))
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
                      'Ritaglia ogni disco dove cambia il colore; ritaglia la finestra bianca col taglierino; fora il centro (punteruolo, o Ø 4 mm per il perno 3D).',
                      'Monta il disco sopra la corona con lo stesso nome della plancia eroe: fermacampioni dal davanti, gambe aperte in orizzontale dietro.',
                      'Girando il disco la finestra mostra un solo valore. 6 dischi e 6 fermacampioni per plancia (PV, Danni, ATT, MOV, AR, PL).'], y=266))
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
    b, gc, _ = gettoni(cols, (210 - gw) / 2, (297 - gh) / 2, cart=os.path.join(OUT, 'segnalini'))
    b.insert(0, hdr('Segnalini · foglio 1 di 2', f"{gc['Indizio']} Indizi · {gc['Forte Volontà']} Forte Volontà · {gc['Usato']} Usato  ·  Ø 20 mm  ·  solo fronte"))
    b.append(ftr(['Stampa su A4 al 100%, solo fronte. Taglia sul cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                  'Righe 1-3 Indizi, riga 4 Forte Volontà, poi Usato: Carta Classe, «una volta per turno», «la prima volta» dei mostri,',
                  '«Spostamenti del tesoro» e segnaposto delle carte giocate che lasciano la zona (Equipaggiamenti e Mappe).']))
    write('segnalini', 1, page(fonts('\n'.join(b))))
    sc_ = 5; sx0 = (210 - ((sc_ - 1) * (ST_W + 2 * BLEED) + ST_W)) / 2
    b, sc, sbb = stati(sc_, sx0, 26.0, os.path.join(OUT, 'segnalini'))   # 31 tessere Stato = 7 righe: y0 26 (non 28) perché il disco del tavolo entri sopra il piede
    b.insert(0, hdr('Tessere Stato e rotelle del tavolo · foglio 2 di 2',
                    f'{sum(sc.values())} tessere Stato 26 × 18 mm · 2 dischi Ø 52 mm · solo fronte'))
    pitch = DISC_R * 2 + 2 * BLEED; dy = sbb[3] + 18 + DISC_R
    for j, (key, nm, sotto, ic, col) in enumerate(R_TAVOLO):
        b.append(rotella_disco(105 + (j - 0.5) * pitch, dy, col, nm, sotto, ic, TAVOLO_FIN, 'plancia di gioco'))
    assert dy + DISC_R + BLEED < 262
    b.append(ftr(['Stampa su A4 al 100%, solo fronte. Tessere Stato: taglia sul bordo sottile (3 mm di abbondanza).',
                  f'Righe: {conta(sc)}.',
                  'Uno Stato vale il tuo prossimo turno: preso nel tuo turno va orizzontale, nel turno di un altro verticale (freccia ↑ in alto). Gli effetti sono sulle Carte Aiuto.',
                  'Dischi: ritaglia dove cambia il colore e la finestra bianca, fora il centro. «PV del mostro» e «PV del custode» vanno sulle corone 0-9',
                  'della Sala del Tesoro, con un fermacampioni. La Rotella della Profezia è sul foglio 2 delle pedine (pedine.pdf).'], y=266))
    write('segnalini', 2, page(fonts('\n'.join(b))))
    return dict(gettoni=gc, stati=sc, dischi_tavolo=len(R_TAVOLO))

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
                # kit dei motivi: l'illustrazione PD-xx (arte/png, nativa a 300 ppi: w x ph mm) riempie la faccia dentro un
                # filetto d'ottone chiaro (1,3 mm dal taglio) con un ingranaggio su ogni angolo; il nome sta su una targhetta
                # del colore della pedina in basso, con il filetto d'ottone sopra
                cid = f'pd-{r["id"]}-{part}'
                href = esc(os.path.relpath(os.path.join(ARTE_PNG, f'{r["id"]}.png'), os.path.join(OUT, 'x')))
                fx, fy, fw, fh_ = x + 1.3, py + 1.3, w - 2.6, ph - 2.6
                p = [f'<clipPath id="{cid}"><rect x="{fx:.2f}" y="{fy:.2f}" width="{fw:.2f}" height="{fh_:.2f}" rx="1.6"/></clipPath>',
                     f'<image href="{href}" x="{x:.2f}" y="{py:.2f}" width="{w:.2f}" height="{ph:.2f}" clip-path="url(#{cid})"/>']
                fs = 3.6 if gk == 'eroe' else 3.9
                maxw = w - 4.4
                lines = wrap(nm, fs, maxw, SERIF, True)
                while any(tw(l, fs, SERIF, True) > maxw for l in lines) and fs > 2.0: fs -= 0.1
                cap = 'primo giocatore' if r['tipo'] == 'primo giocatore' else ''   # la didascalia solo dove serve: libera l'illustrazione
                tl = fs * 1.12 * len(lines)                      # altezza delle righe del nome
                th = 1.0 + tl + 0.9 + (2.3 + 0.4 if cap else 0)   # targhetta: nome (+ didascalia)
                ty0 = fy + fh_ - th                              # bordo alto della targhetta
                tcol = '#ffffff' if col != '#b8862b' else '#2a2118'
                p.append(f'<clipPath id="{cid}t"><rect x="{fx:.2f}" y="{ty0:.2f}" width="{fw:.2f}" height="{th:.2f}" rx="1.6"/></clipPath>')
                p.append(f'<rect x="{fx:.2f}" y="{ty0:.2f}" width="{fw:.2f}" height="{th + 1.6:.2f}" fill="{col}" clip-path="url(#{cid}t)"/>')
                p.append(line(fx, ty0, fx + fw, ty0, 0.35, BRASS_L))
                p.append(f'<rect x="{fx:.2f}" y="{fy:.2f}" width="{fw:.2f}" height="{fh_:.2f}" rx="1.6" fill="none" stroke="{BRASS_L}" stroke-width="0.35"/>')
                p += [cog(xx, yy, 1.1, 8, BRASS_L, col) for xx in (fx, fx + fw) for yy in (fy, fy + fh_)]
                ty = ty0 + 1.0 + fs * 0.92
                for j, l in enumerate(lines):
                    p.append(text(cx, ty + j * fs * 1.12, l, fs, tcol, 'middle', True, SERIF))
                if cap: p.append(text(cx, ty0 + th - 0.9 - 0.2, cap, 2.3, '#f4ead5' if col != '#b8862b' else '#2a2118', 'middle', False, SANS))
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

# ------------------------------------------------------------------ MAPPA 12×12 A FIORI (Daniele, 12/11: D24, D25)
# Base in 2 fogli A4 (bordo con le 6 Partenze, coordinate, 14 spazi numerati), 14 fiori a due facce stampati fronte/retro
# (retro specchiato per il fronte-retro manuale sul lato lungo), segnalino Cripta, 10 fogli dei preset. Niente segnaposto «?»
# (D29, 13/11): le tessere Esplorazione stanno coperte sugli esagoni.
# Dati: dati/fiori.csv, base12.csv, preset12.csv; disegno dei pezzi: fiori12.py. La Sala del Tesoro resta un pezzo a parte.
import fiori12 as F12              # noqa: E402
# --arte-mappa CARTELLA: png dell'arte generata della mappa (MF-<NN><A|B>.png, MB-BASE.png; default arte/png o GOBLIN_ARTE_MAPPA);
# se mancano si usa il disegno vettoriale di fiori12.py
if '--arte-mappa' in sys.argv:
    F12.ARTE_MAPPA = sys.argv[sys.argv.index('--arte-mappa') + 1]
ARTE_PNG = os.path.join(HERE, '..', 'arte', 'png')
ABB12 = 2.0                         # abbondanza di base, fiori e Cripta (fronte e retro): 1-2 mm di scarto non si vedono
FASCIA12 = 5.5                      # fascia delle coordinate attorno alla base
SALA_BW = 26 * 10.5 + 2 * 26 * 1.8  # la Sala del Tesoro è la fascia alta della vecchia plancia (unità del disegno, W = 26)
SALA_BH = SALA_BW * 1191 / 4200     # proporzioni di PS-BASE.png
SALA_S = 0.97                       # la Sala si stampa in scala 0,97: corone 0-9 in mm veri (dischi del tavolo)

def num(x): return f'{x:.2f}'.rstrip('0').rstrip('.').replace('.', ',')

def note(righe, x, y, size, maxw, col=BROWN, anchor='middle', passo=1.27):
    """righe di nota a capo entro maxw; ritorna (svg, y della riga dopo)."""
    o = []
    for r in righe:
        for l in wrap(r, size, maxw):
            o.append(text(x, y, l, size, col, anchor)); y += size * passo
    return ''.join(o), y

def sala_disegno(cartella):
    """la Sala del Tesoro come pezzo a parte (unità del disegno, SALA_BW x SALA_BH): PS-BASE sotto, schiarita, cornice
    marrone sul bordo (si taglia sul suo bordo esterno) e svg.sala_tesoro(). Ritorna (svg, larghezza e altezza in mm)."""
    href = esc(os.path.relpath(os.path.join(ARTE_PNG, 'PS-BASE.png'), cartella))
    bw, bh = SALA_BW, SALA_BH
    o = [f'<image href="{href}" x="0" y="0" width="{bw:.2f}" height="{bh:.2f}"/>',
         f'<rect x="0" y="0" width="{bw:.2f}" height="{bh:.2f}" fill="#f4ead5" fill-opacity="0.55"/>',
         f'<rect x="0.6" y="0.6" width="{bw - 1.2:.2f}" height="{bh - 1.2:.2f}" fill="none" stroke="{BROWN}" stroke-width="1.2"/>']
    o.append(f'<rect x="1.9" y="1.9" width="{bw - 3.8:.2f}" height="{bh - 3.8:.2f}" fill="none" stroke="{BRASS}" stroke-width="0.4"/>')
    o += [cog(x, y, 2.8, 8, BRASS_L, BROWN, stroke=BRASS, sw=0.15) for x in (1.9, bw - 1.9) for y in (1.9, bh - 1.9)]
    o += sala_tesoro(bw)
    W = 26; a = tw('Sala del Tesoro', W * 0.55, SERIF, True) / 2 + 7; yy = W * 0.95 - W * 0.55 * 0.33
    o += [line(bw / 2 + s * a, yy, bw / 2 + s * (a + 30), yy, 0.6, BRASS) + star(bw / 2 + s * (a + 33.5), yy, 3.0) for s in (-1, 1)]
    return fonts('\n'.join(o)), bw * SALA_S, bh * SALA_S

def croce(px, py):
    return f'<g id="croce-di-allineamento"><circle cx="{px:.2f}" cy="{py:.2f}" r="1.9" fill="none" stroke="#c0392b" stroke-width="0.2"/>{line(px - 3.5, py, px + 3.5, py, 0.2, "#c0392b")}{line(px, py - 3.5, px, py + 3.5, 0.2, "#c0392b")}</g>'

def sala_a4():
    """sala_tesoro: la Sala del Tesoro (355,6 mm) in 2 pezzi sovrapposti (croci rosse nella fascia comune), un foglio A4."""
    comp = 'sala_tesoro'
    band, Wb, Hb = sala_disegno(os.path.join(OUT, comp))
    WIN, PX = 184.0, 13.0
    ox = Wb - WIN; ov = WIN - ox; mx = (ox + WIN) / 2
    croci = [(mx, 8.0), (mx, Hb / 2), (mx, Hb - 8.0)]
    b = [hdr('Sala del Tesoro', f'in 2 pezzi da unire (finita {num(Wb)} × {num(Hb)} mm)  ·  solo fronte, cartoncino')]
    for c, PY, testo in ((0, 24.0, 'Pezzo 1 (sinistra): taglia sul bordo esterno della cornice marrone in alto, a sinistra e in basso; a destra lungo le tacche.'),
                         (1, 142.0, 'Pezzo 2 (destra): cornice marrone in alto, a destra e in basso; a SINISTRA taglia il margine bianco lungo le tacche.')):
        wx0 = 0 if c == 0 else ox
        cx0 = PX - (BLEED if c == 0 else 0); cx1 = PX + WIN + (BLEED if c == 1 else 0)
        clip = f'x="{cx0}" y="{PY - BLEED}" width="{cx1 - cx0}" height="{Hb + 2 * BLEED:.3f}"'
        b += [f'<defs><clipPath id="sala{c}"><rect {clip}/></clipPath></defs>', f'<rect id="abbondanza" {clip} fill="#efe1c3"/>',
              f'<g id="sala-{c + 1}di2" clip-path="url(#sala{c})"><g transform="translate({PX - wx0:.3f},{PY}) scale({SALA_S})">{band}</g></g>']
        b += [croce(PX + bx - wx0, PY + by) for bx, by in croci if wx0 <= bx <= wx0 + WIN]
        b.append(crop_marks(PX, PY, PX + WIN, PY + Hb, gap=3.5, ln=3.0))
        b.append(text(105, PY + Hb + 9.5, testo, 2.7, INK, 'middle'))
    t, y = note([f'Stampa su A4 al 100%, solo fronte, su cartoncino. Unisci la Sala: sovrapponi il pezzo 2 alla fascia di {num(ov)} mm a destra del pezzo 1, fai coincidere le 3 croci rosse e incolla.',
                 'La Sala va accanto alla mappa. Dischi «PV del mostro» e «PV del custode» (segnalini.pdf, foglio 2) sulle corone 0-9, col fermacampioni.'],
                105, 262, 2.6, 186)
    assert y - 2.6 * 1.27 < 290, 'sala_tesoro: note oltre il margine'
    b.append(t)
    write(comp, 1, page('\n'.join(b)))
    return dict(W=round(Wb, 1), H=round(Hb, 1), sovrapposizione=round(ov, 1))

def sala_a3():
    """sala_tesoro A3: la Sala del Tesoro in un pezzo solo, su un A3 orizzontale."""
    comp = 'sala_tesoro'
    band, Wb, Hb = sala_disegno(os.path.join(OUT, comp))
    PX, PY = (A3H - Wb) / 2, 40.0
    clip = f'x="{PX - BLEED:.3f}" y="{PY - BLEED}" width="{Wb + 2 * BLEED:.3f}" height="{Hb + 2 * BLEED:.3f}"'
    b = [text(A3H / 2, 16, 'Sala del Tesoro', 4.6, INK, 'middle', True, SERIF),
         text(A3H / 2, 22, f'un pezzo solo, {num(Wb)} × {num(Hb)} mm  ·  solo fronte, cartoncino, A3 orizzontale', 2.9, BROWN, 'middle'),
         f'<defs><clipPath id="sala"><rect {clip}/></clipPath></defs>', f'<rect id="abbondanza" {clip} fill="#efe1c3"/>',
         f'<g id="sala-del-tesoro" clip-path="url(#sala)"><g transform="translate({PX:.3f},{PY}) scale({SALA_S})">{band}</g></g>',
         crop_marks(PX, PY, PX + Wb, PY + Hb, gap=3.5, ln=3.0)]
    t, y = note(['Stampa su A3 al 100%, solo fronte. Taglia sul bordo esterno della cornice marrone. Dischi «PV del mostro» e «PV del custode» sulle corone 0-9, col fermacampioni.',
                 'La mappa 12×12 (base, fiori, preset) si stampa dai PDF A4 di playtest_v7: mappa_base.pdf, mappa_fiori.pdf, mappa_preset.pdf.'],
                A3H / 2, PY + Hb + 14, 3.0, A3H - 40)
    b.append(t)
    write(comp, 1, page(fonts('\n'.join(b)), A3H, A3W))
    return dict(W=round(Wb, 1), H=round(Hb, 1))

# ---------- dati e mappa
_M12 = None
def dati12():
    global _M12
    if _M12 is None:
        _M12 = F12.leggi(DATI)
    return _M12

def terreno12(righe):
    """{(x, y): terreno} della mappa montata con le righe di un preset {spazio: (fiore, faccia, freccia)}."""
    fiori, base, spazi, partenze, _ = dati12()
    t = {h: ('partenza' if h in partenze else x) for h, x in base.items()}
    for s, (i, lato, fr) in righe.items():
        for p, x in fiori[(i, lato)]['celle'].items():
            t[spazi[s][0 if p == 0 else (p - 1 + fr - 1) % 6 + 1]] = x
    assert len(t) == 144
    return t

def nomi_carte():
    return {r['id']: r['nome'] for r in read('carte_comuni.csv') if r['id'].startswith('TM-')}

# ---------- base (2 fogli A4)
def base12_svg():
    """la base nelle coordinate della mappa (0,0 = angolo della griglia): fascia con le coordinate, spazi vuoti numerati,
    esagoni di bordo, rombi di giunzione sulla metà."""
    fiori, base, spazi, partenze, _ = dati12()
    f, L, A = FASCIA12, F12.LARGO, F12.ALTO
    o = [f'<rect x="{-f - ABB12:.2f}" y="{-f - ABB12:.2f}" width="{L + 2 * (f + ABB12):.2f}" height="{A + 2 * (f + ABB12):.2f}" fill="#d9cfa8"/>',
         f'<rect x="{-f + 1.2:.2f}" y="{-f + 1.2:.2f}" width="{L + 2 * f - 2.4:.2f}" height="{A + 2 * f - 2.4:.2f}" rx="1.5" fill="none" stroke="{BRASS}" stroke-width="0.3"/>',
         f'<rect x="0" y="0" width="{L:.2f}" height="{A:.2f}" fill="#efe6cf"/>']
    for c in range(1, 13):   # numeri di colonna: sopra la riga 1 (dispari) e sotto la riga 12 (pari)
        for r, yy in ((1, -f / 2 + 1.3), (12, A + f / 2 + 1.3)):
            o.append(text(F12.centro_mappa((c, r))[0], yy, str(c), 3.6, INK, 'middle', True))
    for r in range(1, 13):
        y = F12.centro_mappa((1, r))[1] + 1.3
        o += [text(-f / 2, y, str(r), 3.6, INK, 'middle', True), text(L + f / 2, y, str(r), 3.6, INK, 'middle', True)]
    for s, pos in spazi.items():   # spazi vuoti: contorno d'ottone, numero dello spazio, numeri 1-6 dell'anello
        cc = [F12.centro_mappa(h) for h in pos.values()]
        o += [f'<polygon points="{F12.pts(F12.vertici(x, y))}" fill="#efe6cf" stroke="{BRASS}" stroke-opacity="0.55" stroke-width="0.3"/>' for x, y in cc]
        x0, y0 = F12.centro_mappa(pos[0])
        o.append(text(x0, y0 + 4, str(s), 11, BRASS, 'middle', True, SERIF))
        o += [text(*F12.centro_mappa(pos[p]), str(p), 3.4, BRASS, 'middle') for p in range(1, 7)]
        o.append(F12.contorno(cc, BRASS, 0.4))
    celle = {h: (*F12.centro_mappa(h), 'partenza' if h in partenze else x) for h, x in base.items()}
    o.append(F12.pezzo(celle, 'base12', partenze=partenze, arte=F12.immagine_arte('MB-BASE', 0, 0, os.path.join(OUT, 'mappa_base'), False)))
    return '\n'.join(o)

def mappa_base():
    """mappa_base: la base 12×12 su 2 fogli A4 verticali (metà sinistra, metà destra), con la linea di giunzione e 5 rombi
    di rame a cavallo della giunzione. Solo fronte, cartoncino."""
    comp = 'mappa_base'
    f, L, A = FASCIA12, F12.LARGO, F12.ALTO
    corpo = base12_svg()
    m = L / 2                                   # giunzione: a metà larghezza
    larg = f + m + 2 * ABB12                    # 167 mm per metà
    ty = (297 - (A + 2 * f + 2 * ABB12)) / 2 + f + ABB12
    giunz = ''.join(lozenge(m, y, 5.0, 7.0, COPPER, PLATE, 0.3) for y in (A * 0.1, A * 0.3, A * 0.5, A * 0.7, A * 0.9))
    for n, (x0, x1, nome) in enumerate(((-f - ABB12, m + ABB12, 'metà sinistra'), (m - ABB12, L + f + ABB12, 'metà destra')), 1):
        tx = (210 - larg) / 2 - x0
        clip = f'x="{x0:.2f}" y="{-f - ABB12:.2f}" width="{x1 - x0:.2f}" height="{A + 2 * (f + ABB12):.2f}"'
        taglio = (f'<rect x="{-f:.2f}" y="{-f:.2f}" width="{L + 2 * f:.2f}" height="{A + 2 * f:.2f}" fill="none" stroke="#222222" stroke-width="0.25"/>'
                  f'{line(m, -f - ABB12, m, A + f + ABB12, 0.25, "#222222")}')
        xr = (210 - larg) / 4 if n == 1 else 210 - (210 - larg) / 4    # metà del margine esterno (21,5 mm)
        b = [f'<defs><clipPath id="meta{n}"><rect {clip}/></clipPath></defs>',
             f'<g transform="translate({tx:.3f},{ty:.3f})"><g clip-path="url(#meta{n})">{corpo}{giunz}{taglio}</g></g>',
             # niente riquadri sulla mappa: solo una riga piccola nel margine esterno del foglio, fuori dall'area di taglio
             f'<g transform="rotate(-90 {xr:.2f} 200)">' + text(xr, 200 + 0.9, f'Base 12×12 · {nome} · cartoncino, 100%', 2.6, BROWN, 'middle') + '</g>',
             # segmento di controllo di 100 mm (verticale, nel margine esterno, fuori dal taglio): a 100 % deve misurare 100 mm;
             # verifica_pdf.py lo misura sul PDF (errore oltre lo 0,05 %)
             f'<line x1="{xr:.2f}" y1="20" x2="{xr:.2f}" y2="120" stroke="{CUT}" stroke-width="0.25"/>'
             + ''.join(f'<line x1="{xr - 2:.2f}" y1="{yy}" x2="{xr + 2:.2f}" y2="{yy}" stroke="{CUT}" stroke-width="0.25"/>' for yy in (20, 120))
             + f'<g transform="rotate(-90 {xr + 4.2:.2f} 70)">' + text(xr + 4.2, 70, 'controllo 100 mm', 2.4, BROWN, 'middle') + '</g>']
        write(comp, n, page(fonts('\n'.join(b))))
    return dict(fogli=2, base_mm=(round(L + 2 * f, 1), round(A + 2 * f, 1)))

# ---------- fiori fronte/retro (3 fogli = 6 pagine) e Cripta
FIORI_POS = [(63.0, 58.0), (147.0, 58.0), (63.0, 140.0), (147.0, 140.0), (63.0, 222.0), (147.0, 222.0)]   # centri dei fiori sul fronte
def mappa_fiori():
    """mappa_fiori: pagine dispari = fronti (facce A, linee di taglio), pagine pari = retri (facce B, specchiati sul lato
    lungo: il retro del pezzo in x sta in 210 - x). Foglio 3: 2 fiori e il segnalino Cripta (due facce uguali); i 24
    segnaposto «?» sono tolti (D29: le tessere Esplorazione stanno coperte sugli esagoni). Retri senza linee di taglio;
    abbondanza ABB12 su tutte e due le facce."""
    comp = 'mappa_fiori'
    fiori = dati12()[0]
    blocchi = [list(range(1, 7)), list(range(7, 13)), [13, 14]]
    cri = (147.0, 194.0)
    pagina = 0
    for k, blocco in enumerate(blocchi, 1):
        for lato in 'AB':
            fronte = lato == 'A'
            sx = (lambda x: x) if fronte else (lambda x: 210 - x)
            b = [text(105, 11, f'Mappa 12×12 · fiori · foglio {k} di 3 · {"fronte" if fronte else "retro"}', 4.2, INK, 'middle', True, SERIF)]
            sub = ('Cartoncino 250-300 g. Stampa questa pagina, poi rimetti il foglio nel cassetto girato sul LATO LUNGO e stampa la pagina dopo.'
                   if fronte else f'Questa pagina va sul retro del foglio {k}: foglio già stampato girato sul lato lungo. Niente linee di taglio: si taglia sul fronte.')
            b.append(text(105, 16.5, sub, 2.6, BROWN, 'middle'))
            for j, i in enumerate(blocco):
                x, y = FIORI_POS[j]
                b.append(F12.fiore(fiori[(i, lato)], sx(x), y, 0, f'f{k}{lato}{j}', ABB12, fronte, f'{i}{lato}', arte=os.path.join(OUT, comp)))
            if k == 3:
                cx, cy = sx(cri[0]), cri[1]
                img = F12.immagine_arte('SG-CRIPTA', cx, cy, os.path.join(OUT, comp))
                if img:   # arte generata: tagliata sull'esagono + abbondanza
                    img = (f'<clipPath id="cr{lato}"><polygon points="{F12.pts(F12.vertici(cx, cy, F12.R + ABB12 / math.cos(math.radians(30))))}"/></clipPath>'
                           f'<g clip-path="url(#cr{lato})">{img}</g>')
                b.append(f'<polygon points="{F12.pts(F12.vertici(cx, cy, F12.R + ABB12 / math.cos(math.radians(30))))}" fill="#8f877c"/>' + F12.segnalino_cripta(cx, cy, img)
                         + (F12.contorno([(cx, cy)], '#222222', 0.25) if fronte else ''))
                b.append(text(sx(147.0), 218, 'Cripta', 3.0, BROWN, 'middle', True))
            pie = (['Ogni fiore: taglia sulla linea sottile del contorno; l’abbondanza di 2 mm copre lo scarto tra fronte e retro.',
                    'Id piccolo nell’angolo: numero del fiore e faccia (A sul fronte, B sul retro). La freccia d’ottone indica l’esagono 1 dell’anello.']
                   if fronte else ['Retro: faccia B dei fiori, nella stessa posizione del fronte una volta girato il foglio sul lato lungo.',
                                   'Controlla con la luce: il contorno del fronte deve cadere dentro l’abbondanza del retro.'])
            b += [text(105, 270 + j * 4, l, 2.6, BROWN, 'middle') for j, l in enumerate(pie)]
            pagina += 1
            write(comp, pagina, page(fonts('\n'.join(b))))
    return dict(fogli=3, pagine=pagina, fiori=14, cripta=1)

# ---------- fogli dei preset (10, carta comune)
def mappa_preset():
    """mappa_preset: un foglio per preset: schema della mappa con, in ogni spazio, fiore e faccia in grande e il numero
    della freccia; i 3 spazi del cambio (carta Mappa a metà partita) evidenziati in rame e numerati 1-3."""
    comp = 'mappa_preset'
    fiori, base, spazi, partenze, preset = dati12()
    nomi = nomi_carte()
    k = 182 / (F12.LARGO + 2 * FASCIA12)
    for n, (tema, p) in enumerate(preset.items(), 1):
        titolo = 'Preset «Strettoie»' if not p['carta'] else f'{p["carta"]} {nomi.get(p["carta"], tema)}'
        b = [text(105, 13, f'Mappa 12×12 · {titolo}', 5.0, INK, 'middle', True, SERIF), fregio(105, 13, f'Mappa 12×12 · {titolo}', 5.0, 105),
             text(105, 19, f'Foglio dei preset {n} di {len(preset)} · carta comune', 2.8, BROWN, 'middle')]
        t = terreno12(p['righe'])
        o = [f'<rect x="{-FASCIA12:.2f}" y="{-FASCIA12:.2f}" width="{F12.LARGO + 2 * FASCIA12:.2f}" height="{F12.ALTO + 2 * FASCIA12:.2f}" rx="2" fill="#d9cfa8"/>']
        o += [f'<polygon points="{F12.pts(F12.vertici(*F12.centro_mappa(h)))}" fill="{F12.FONDO[x]}" stroke="{INK}" stroke-opacity="0.35" stroke-width="0.3"/>' for h, x in t.items()]
        o += [f'<circle cx="{F12.centro_mappa(h)[0] + F12.R * 0.48:.2f}" cy="{F12.centro_mappa(h)[1] + F12.R * 0.42:.2f}" r="2" fill="#fffaf0"/>' for h, x in t.items() if x == 'acqua']
        o += [F12.icona_partenza(*F12.centro_mappa(h), m) for h, m in partenze.items()]
        for c in range(1, 13):
            o.append(text(F12.centro_mappa((c, 1))[0], -FASCIA12 / 2 + 1.3, str(c), 3.6, INK, 'middle', True))
        for r in range(1, 13):
            o.append(text(-FASCIA12 / 2, F12.centro_mappa((1, r))[1] + 1.3, str(r), 3.6, INK, 'middle', True))
        for s, (i, lato, fr) in p['righe'].items():
            cc = [F12.centro_mappa(h) for h in spazi[s].values()]
            cambio = p['cambio'].get(s)
            o.append(F12.contorno(cc, COPPER if cambio else BROWN, 1.6 if cambio else 0.9))
            x0, y0 = F12.centro_mappa(spazi[s][0])
            xa, ya = F12.centro_mappa(spazi[s][fr])
            o.append(f'<path d="M{x0 + (xa - x0) * 0.35:.2f} {y0 + (ya - y0) * 0.35:.2f} L{x0 + (xa - x0) * 0.95:.2f} {y0 + (ya - y0) * 0.95:.2f}" '
                     f'stroke="{BRASS}" stroke-width="2.2" marker-end="url(#punta)"/>')
            o.append(f'<rect x="{x0 - 13:.2f}" y="{y0 - 8:.2f}" width="26" height="13.5" rx="2.5" fill="#fffaf0" stroke="{COPPER if cambio else BRASS}" stroke-width="{0.9 if cambio else 0.5}" opacity="0.94"/>')
            o.append(text(x0, y0 + 2.6, f'{i}{lato}', 10, INK, 'middle', True))
            o.append(text(xa, ya + 2.4, str(fr), 6.5, INK, 'middle', True))
            if cambio:
                o.append(f'<circle cx="{x0 + 14:.2f}" cy="{y0 - 9:.2f}" r="4.2" fill="{COPPER}" stroke="#fffaf0" stroke-width="0.6"/>'
                         + text(x0 + 14, y0 - 7.4, str(cambio), 5, '#fffaf0', 'middle', True))
        defs = (f'<defs><marker id="punta" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3" markerHeight="3" orient="auto">'
                f'<path d="M0 0 L10 5 L0 10 z" fill="{BRASS}"/></marker></defs>')
        y0 = 25.0
        b.append(f'{defs}<g transform="translate({14 + FASCIA12 * k:.3f},{y0 + FASCIA12 * k:.3f}) scale({k:.5f})">{"".join(o)}</g>')
        y = y0 + (F12.ALTO + 2 * FASCIA12) * k + 7
        righe = sorted(p['righe'].items())
        b.append(text(14, y, 'Montaggio: per ogni spazio, il fiore con la faccia in grande; la freccia d’ottone del fiore verso il numero 1-6 indicato dalla freccia.', 3.0, INK, 'start', True)); y += 5
        for j, (s, (i, lato, fr)) in enumerate(righe):
            cx, cy = 14 + (j % 7) * 26.5, y + (j // 7) * 5.2
            b.append(text(cx, cy, f'S{s}: {i}{lato} → {fr}', 3.4, INK))
        y += 13
        cam = sorted(p['cambio'].items(), key=lambda kv: kv[1])
        b.append(text(14, y, 'Carta Mappa a metà partita (bordi di rame): cambia solo questi 3 fiori, in ordine', 3.2, COPPER, 'start', True)); y += 5
        b.append(text(14, y, '   ·   '.join(f'{c}) spazio {s} ← {p["righe"][s][0]}{p["righe"][s][1]}, freccia {p["righe"][s][2]}' for s, c in cam), 3.4, INK, 'start', True)); y += 6
        regole = ['Se il fiore indicato sta in un altro spazio, scambialo con quello dello spazio indicato: il fiore tolto va nello spazio liberato con la sua faccia e la sua freccia. Poi metti faccia e freccia indicate. Vale anche dopo un draft.',
                  'Prima del cambio: le tessere sui fiori che si muovono tornano coperte nella riserva; chi ha giocato la carta ne rimette altrettante coperte dalla riserva sui fiori nuovi, una per esagono, su esagoni percorribili ad almeno 2 esagoni dalle Partenze. Poi la Cripta si ritira con 2D6 + 2D6.']
        if not p['carta']:
            regole.append('Una Mappa lascia il gioco senza sostituta (TI-22): si applicano le 3 righe di Strettoie.')
        t_, y = note(regole, 14, y, 2.8, 182, BROWN, 'start')
        b.append(t_)
        assert y < 290, f'mappa_preset: il foglio {n} non entra'
        write(comp, n, page(fonts('\n'.join(b))))
    return len(preset)

# ------------------------------------------------------------------ PROVA DI STAMPA
KIT_A4 = [('tessere_esplorazione.pdf', 1), ('segnalini.pdf (segnalini, Stati, dischi del tavolo)', 2),
          ('rotelle_eroe.pdf (24 dischi)', 2), ('plance_eroe.pdf (A4 orizzontale)', 4), ('pedine.pdf (6 Boss, Profezia)', 2)]
KIT_A3 = [('plance_eroe.pdf (2 plance per foglio)', 2), ('rotelle_eroe.pdf (24 + 2 dischi)', 1),
          ('componenti_misti.pdf (pedine con 6 Boss, segnalini)', 1), ('tessere_esplorazione.pdf (e tessere Stato, Profezia)', 1)]
# poi i pezzi della mappa (contati da chi li genera): in prova()
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

def prova(PW=210, PH=297, formato='A4', mappa=()):
    """00_prova_stampa.pdf: un foglio solo fronte con righello 100 mm, quadrato 50 mm, riquadro a 6,5 mm dal bordo
    e l'elenco dei file del kit (solo fronte, tranne mappa_fiori.pdf). mappa: [(file, fogli)] della mappa."""
    K = '#000000'; FR = 6.5; cx = PW / 2; tw_ = PW - 40
    def par(x, y, s, size=3.5, bold=False, gap=1.25):
        ls = wrap(s, size, tw_, SANS, bold)
        return ''.join(text(x, y + j * size * gap, l, size, K, 'start', bold) for j, l in enumerate(ls)), y + len(ls) * size * gap
    b = [f'<rect x="{FR}" y="{FR}" width="{PW - 2 * FR}" height="{PH - 2 * FR}" fill="none" stroke="{K}" stroke-width="0.25"/>',
         text(cx, FR + 4.5, '↑ alto (lato corto di ingresso)', 3.0, BROWN, 'middle'),
         text(cx, 21, f'Prova di stampa {formato} · Il Tesoro del Goblin', 6.0, K, 'middle', True, SERIF),
         text(cx, 27, f'Un solo foglio {formato}, SOLO FRONTE: il kit v7 è solo fronte, tranne i fiori della mappa (mappa_fiori.pdf)', 3.2, BROWN, 'middle')]
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
    for p in [f'1. Stampa al 100% («Dimensioni effettive», MAI «Adatta alla pagina»), carta {formato}, SOLO FRONTE. Unica eccezione: mappa_fiori.pdf, fronte e retro a mano (le istruzioni sono sui fogli).',
              '2. Scala: misura il righello (100 mm tra 0 e 10) e il quadrato (50 mm). Va bene entro ±1 mm. Se no, disattiva «adatta/riduci» e ristampa.',
              '3. Margini: il riquadro sottile a 6,5 mm dal bordo deve vedersi su tutti e 4 i lati. Se manca un lato la stampante taglia il margine: carte, plance e tacche stanno oltre i 6,5 mm.',
              'Se tutto torna, stampa il resto del kit nell’ordine dell’elenco qui sotto. Le carte e i loro dorsi sono su fogli separati: si uniscono a mano (colla stick o bustina).']:
        t, y = par(20, y, p); b.append(t); y += 2.2
    y += 6
    kit = [('00_prova_stampa.pdf', '1', 1)] + fogli_carte() + [(f, str(n), n) for f, n in list(KIT_A4 if formato == 'A4' else KIT_A3) + list(mappa)]
    b.append(text(20, y, f'File del kit {formato} (fogli)', 3.4, K, 'start', True)); y += 6
    for f, s, _ in kit:
        b.append(text(24, y, f, 3.2, K) + text(PW - 24, y, s, 3.2, K, 'end')); b.append(line(24, y + 1.3, PW - 24, y + 1.3, 0.1, '#999999')); y += 5.2
    b.append(text(PW - 24, y + 1.5, f'Totale: {sum(n for _, _, n in kit)} fogli {formato}', 3.4, K, 'end', True))
    assert y + 8 < PH - FR - 4
    write('prova_stampa', 1, page(fonts('\n'.join(b)), PW, PH))

# ================================================================== FORMATO A3 (--formato A3)
# Stesse regole dell'A4: tutto a >= 6 mm dal bordo, tutto solo fronte.
A3W, A3H = 297, 420
def hdr3(title, sub, y=11):
    return (text(A3W / 2, y, title, 4.2, INK, 'middle', True, SERIF) + fregio(A3W / 2, y, title, 4.2, A3W / 2)
            + text(A3W / 2, y + 5, sub, 2.9, BROWN, 'middle'))
def ftr3(lines, y=392):
    return ''.join(text(A3W / 2, y + i * 3.6, l, 2.8, BROWN, 'middle') for i, l in enumerate(lines))

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
    for par in ['Colonne: le 4 plance eroe (dischi identici); righe: PV, Danni, ATT, MOV, AR, PL. In basso a sinistra i 2 dischi del tavolo.',
                'Stampa al 100%. Ritaglia ogni disco dove cambia il colore e la finestra bianca; fora il centro (punteruolo, o Ø 4 mm per il perno 3D).',
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
    sc_ = 8; sb, sc, sbox = stati(sc_, (A3W - ((sc_ - 1) * (ST_W + 2 * BLEED) + ST_W)) / 2, 28.0, os.path.join(OUT, 'tessere_esplorazione'))
    D = 24; R = D / 2; cols = 6; pitch = D + 2 * BLEED
    rws = math.ceil(len(rows) / cols)
    gw, gh = (cols - 1) * pitch + D, (rws - 1) * pitch + D
    x0, y0 = (A3W - gw) / 2, sbox[3] + 2 * BLEED + 8
    cs = [(x0 + R + (i % cols) * pitch, y0 + R + (i // cols) * pitch) for i in range(len(rows))]
    b = sb + esplorazione_pezzi(cs, rows, D, os.path.join(OUT, 'tessere_esplorazione'))
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
                  [f'Tessere Stato (in alto): {conta(sc)} (freccia ↑ in alto = verticale; gli effetti sono sulle Carte Aiuto).',
                   'Rotella della Profezia (Oracolo): disco sulla base quadrata col fermacampioni. P pari · D dispari · A alto (4+ su D6, 8+ su 2D6) · B basso (3− / 6−).']))
    write('tessere_esplorazione', 1, page(fonts('\n'.join(b)), A3W, A3H))
    return dict(esplorazione=dict(Counter(r['colore'] for r in rows)), stati=sc)

def misti_a3():
    """Un foglio A3 solo fronte: pedine (eroi, MIMI e Geronimo in alto; i 6 Boss nella seconda fila) e segnalini (sotto)."""
    bw = (len(BOSS) - 1) * (GEO['boss']['w'] + 2 * BLEED) + GEO['boss']['w']
    pb, pz = pedine([(EROI + ['Geronimo'], 'eroe', (A3W - (6 * 30 + 24)) / 2, 28.0), (BOSS, 'boss', (A3W - bw) / 2, 124.0)])
    gb, gc, gbox = gettoni(10, (A3W - (9 * 26 + 20)) / 2, 248.0, per_tipo=False, cart=os.path.join(OUT, 'componenti_misti'))
    assert (A3W - bw) / 2 - BLEED >= 6.5 and 124.0 + 2 * (GEO['boss']['fh'] + GEO['boss']['ph']) + 7.5 < gbox[1] - 7.5 and gbox[3] + 7.5 < 385
    b = [hdr3('Pedine · Segnalini', f'{len(pz)} pedine pieghevoli (6 Boss) · {sum(gc.values())} segnalini Ø 20 mm  ·  foglio 1 di 1  ·  solo fronte, A3 verticale')]
    b += pb + gb
    b.append(ftr3(['Stampa su A3 al 100%, solo fronte. Taglia sul bordo/cerchio sottile; l’abbondanza di 3 mm esce dal taglio.',
                   'Pedine: piega sulla linea tratteggiata bianca (al centro) e incolla fronte e retro; le linguette chiare fanno da piede a T. Eroi 24 mm, Boss 40 mm.',
                   'Le tessere Stato sono sul foglio delle tessere Esplorazione (tessere_esplorazione.pdf).',
                   f"Segnalini: {gc['Indizio']} Indizi (prima riga e inizio della seconda), {gc['Forte Volontà']} Forte Volontà (fine della seconda), {gc['Usato']} Usato (righe 3-4)."]))
    write('componenti_misti', 1, page(fonts('\n'.join(b)), A3W, A3H))
    return dict(pedine=len(pz), segnalini=gc)

# ---------- segnalini 3D (D29): adesivi da applicare sui pezzi 3D di 3d_solidcraft/genera_3d_solidcraft.py. Ogni pezzo 3D
# ha il contorno del pezzo di carta; l'adesivo è la tasca meno il gioco (contorno - bordino - gioco_carta): si usa l'arte
# del pezzo di carta in scala (tessere e segnalini tondi in scala uniforme, Stati 26 × 18 → 23,8 × 15,8 in x e y, cioè
# +4 % di larghezza), le rotelle in scala 1 (la finestra deve stare sulla corona della plancia) tagliate sulla corona
# dell'adesivo con l'intaglio della finestra. Cripta: la carta esagonale da 25,2 nella tasca del segnalino (come prima).
def segmento_100(y):
    """segmento di controllo di 100 mm (lo stesso di carta_base_3d.py, misurato da verifica_pdf.py)."""
    return (f'<line x1="55" y1="{y:.2f}" x2="155" y2="{y:.2f}" stroke="{CUT}" stroke-width="0.25"/>'
            + ''.join(f'<line x1="{x}" y1="{y - 2:.2f}" x2="{x}" y2="{y + 2:.2f}" stroke="{CUT}" stroke-width="0.25"/>' for x in (55, 155))
            + text(105, y + 5, 'Segmento di controllo: 100 mm esatti. Stampa al 100 % (print-scaling=none, MAI «adatta alla pagina»).', 2.6, BROWN, 'middle'))

def taglio_cerchio(x, y, r):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="none" stroke="{CUT}" stroke-width="0.2"/>'

def senza_tacche(b):
    return [e for e in b if 'id="tacche' not in e]

def segnalini_3d():
    comp = 'segnalini_3d'
    d = os.path.join(OUT, comp)
    os.makedirs(d, exist_ok=True)
    sys.path.insert(0, os.path.join(HERE, '..', '..', '3d_solidcraft'))
    import genera_3d_solidcraft as G3   # noqa: E402  misure delle tasche dal generatore 3D
    P3 = G3.P
    rientro = P3['bordino'] + P3['gioco_carta']
    Ro = P3['rotella_d'] / 2 - rientro                  # corona dell'adesivo delle rotelle
    Ri = P3['mozzo_r'] + P3['gioco_carta']
    assert abs(Ri - FORO_ADESIVO_R) < 1e-9 and abs(P3['rotella_d'] / 2 - DISC_R) < 1e-9 and abs(P3['corona_r'] - RING_R) < 1e-9
    finestre = {n: f for n, f, _ in G3.ROTELLE_3D}
    assert all(finestre['rotella_' + nm] == win for _, nm, _, _, _, _, win, _, _, _ in ROTELLE), 'finestre 3D diverse da ROTELLE'
    assert finestre['rotella_scontro'] == finestre['rotella_custode'] == TAVOLO_FIN and finestre['rotella_Profezia'] == PROFEZIA_FIN
    assert G3.PLANCE == PLANCE
    note_base = ['Stampa su A4 al 100%, solo fronte, carta adesiva o cartoncino sottile 160 g. Taglia sulla linea scura (linea spessa = taglio dell’adesivo).']
    pagine = []

    # pagina 1: fronti delle Tessere Esplorazione + Cripta; pagina 2: dorsi delle tessere
    rows = read('tessere_esplorazione.csv')
    D = P3['tessera_d']; s = (D - 2 * rientro) / D; pp = 28.0; cols = 6
    cs = [(D / 2 + (i % cols) * pp, D / 2 + (i // cols) * pp) for i in range(len(rows))]
    gw = ((cols - 1) * pp + D) * s; X0, Y0 = (210 - gw) / 2, 25.0
    tr = lambda x, y: (X0 + x * s, Y0 + y * s)
    b = [f'<g transform="translate({X0:.4f},{Y0:.4f}) scale({s:.6f})">' + ''.join(esplorazione_pezzi(cs, rows, D, d)) + '</g>']
    b += [taglio_cerchio(*tr(x, y), D / 2 * s) for x, y in cs]
    cx, cy = 105.0, Y0 + gw + 26.0
    img = F12.immagine_arte('SG-CRIPTA', cx, cy, d)
    ra = F12.R + 1.5 / math.cos(math.radians(30))
    if img:
        img = f'<clipPath id="s3c"><polygon points="{F12.pts(F12.vertici(cx, cy, ra))}"/></clipPath><g clip-path="url(#s3c)">{img}</g>'
    else:
        b.append(f'<polygon points="{F12.pts(F12.vertici(cx, cy, ra))}" fill="#8f877c"/>')
    b.append(F12.segnalino_cripta(cx, cy, img) + f'<polygon points="{F12.pts(F12.vertici(cx, cy))}" fill="none" stroke="{CUT}" stroke-width="0.2"/>')
    b.append(text(cx, cy + F12.R + 5, 'Cripta (carta da 25,2: tasca del segnalino 3D 25,7)', 2.8, BROWN, 'middle', True))
    pagine.append(('Tessere Esplorazione · fronti', f'{len(rows)} adesivi Ø {D * s:.1f} mm per la tasca sopra (Ø {D - 2 * P3["bordino"]:.1f}) + la Cripta', b,
                   ['Fronte nella tasca sopra della tessera 3D; il dorso (pagina 2) si incolla sul fondo piatto.']))
    b = [f'<g transform="translate({X0:.4f},{Y0:.4f}) scale({s:.6f})">'
         + ''.join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{D / 2 + BLEED:.2f}" fill="#8a5a33"/>' + (disco_arte('TX-RETRO', x, y, D / 2, d) or '') for x, y in cs) + '</g>']
    b += [taglio_cerchio(*tr(x, y), D / 2 * s) for x, y in cs]
    pagine.append(('Tessere Esplorazione · dorsi', f'{len(rows)} adesivi Ø {D * s:.1f} mm da incollare sul fondo piatto della tessera 3D', b,
                   ['Il dorso si incolla al centro del fondo piatto (1,1 mm di margine): coperta, la tessera mostra il dorso e tiene il fronte nella tasca.']))

    # pagina 3: tessere Stato (in scala 23,8/26 × 15,8/18) e segnalini tondi Ø 20 → 17,8
    sw, sh = P3['stato_l'] - 2 * rientro, P3['stato_a'] - 2 * rientro
    sx, sy = sw / ST_W, sh / ST_H
    sc_ = 6; X0 = (210 - ((sc_ - 1) * (ST_W + 2 * BLEED) + ST_W) * sx) / 2; Y0 = 24.0
    sb, sconta, sbb = stati(sc_, 0.0, 0.0, d)
    n_st = sum(sconta.values())
    b = [f'<g transform="translate({X0:.4f},{Y0:.4f}) scale({sx:.6f},{sy:.6f})">' + ''.join(senza_tacche(sb)) + '</g>']
    r_ad = P3['stato_r'] - rientro if P3['stato_r'] > rientro else 0.0
    pxs, pys, nr = (ST_W + 2 * BLEED) * sx, (ST_H + 2 * BLEED) * sy, math.ceil(n_st / sc_)
    # tra un adesivo e l'altro resta 1 mm di abbondanza, il resto è bianco: le bandelle non fanno righe scure lunghe (il
    # segmento di 100 mm di verifica_pdf.py deve essere l'unico tratto scuro lungo 97-103 mm)
    for j in range(sc_ - 1):
        b.append(f'<rect x="{X0 + j * pxs + sw + 1:.3f}" y="{Y0 - BLEED:.3f}" width="{pxs - sw - 2:.3f}" height="{nr * pys + BLEED:.3f}" fill="#ffffff"/>')
    for j in range(nr - 1):
        b.append(f'<rect x="{X0 - BLEED:.3f}" y="{Y0 + j * pys + sh + 1:.3f}" width="{sc_ * pxs + BLEED:.3f}" height="{pys - sh - 2:.3f}" fill="#ffffff"/>')
    for i in range(n_st):
        x, y = X0 + (i % sc_) * pxs, Y0 + (i // sc_) * pys
        b.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{sw:.3f}" height="{sh:.3f}" rx="{max(r_ad, 0.0):.3f}" fill="none" stroke="{CUT}" stroke-width="0.2"/>')
    Yg = Y0 + sbb[3] * sy + 5.0
    G = P3['gettone_d']; sg = (G - 2 * rientro) / G; gc_ = 8
    gb, gconta, gbb = gettoni(gc_, 0.0, 0.0, per_tipo=False, cart=d)
    Xg = (210 - gbb[2] * sg) / 2
    b.append(f'<g transform="translate({Xg:.4f},{Yg:.4f}) scale({sg:.6f})">' + ''.join(senza_tacche(gb)) + '</g>')
    n_g = sum(gconta.values()); pg = G + 2 * BLEED
    b += [taglio_cerchio(Xg + (G / 2 + (i % gc_) * pg) * sg, Yg + (G / 2 + (i // gc_) * pg) * sg, G / 2 * sg) for i in range(n_g)]
    assert Yg + gbb[3] * sg < 262, Yg + gbb[3] * sg
    pagine.append(('Tessere Stato e segnalini', f'{n_st} Stati {sw:.1f} × {sh:.1f} mm · {conta(gconta)} Ø {G * sg:.1f} mm · nella tasca sopra del pezzo 3D', b,
                   [f'Stati: {conta(sconta)}.', 'Segnalini: Indizi, poi Forte Volontà, poi Usato (in ordine di riga).']))

    # pagine 4-6: rotelle (scala 1), 12 per foglio (3 × 4), passo 54
    def adesivo_rotella(cx, cy, disco, win, k):
        a, ri = win[0] / 2, RING_R - win[1] / 2
        yo = math.sqrt(Ro ** 2 - a ** 2)
        est = (f'M{cx + a:.3f} {cy - yo:.3f}A{Ro:.3f} {Ro:.3f} 0 1 1 {cx - a:.3f} {cy - yo:.3f}'
               f'L{cx - a:.3f} {cy - ri:.3f}L{cx + a:.3f} {cy - ri:.3f}Z')
        foro = f'M{cx + Ri:.3f} {cy:.3f}A{Ri:.3f} {Ri:.3f} 0 1 0 {cx - Ri:.3f} {cy:.3f}A{Ri:.3f} {Ri:.3f} 0 1 0 {cx + Ri:.3f} {cy:.3f}Z'
        return (f'<clipPath id="ar{k}"><path d="{est}"/></clipPath><g clip-path="url(#ar{k})">{disco}</g>'
                f'<path d="{est} {foro}" fill="none" stroke="{CUT}" stroke-width="0.2"/>')
    passo = 54.0; X0 = (210 - (2 * passo + 2 * DISC_R)) / 2 + DISC_R; Y0 = 25.0 + DISC_R
    eroe = [(nm, sotto, ic, win) for _, nm, sotto, ic, _, _, win, _, _, _ in ROTELLE]
    for f in range(PLANCE // 2):
        b = []
        for h in range(2):
            for k, (nm, sotto, ic, win) in enumerate(eroe):
                i = h * len(eroe) + k
                x, y = X0 + (i % 3) * passo, Y0 + (i // 3) * passo
                b.append(adesivo_rotella(x, y, rotella_disco(x, y, COL_PB, nm, sotto, ic, win, 'plancia eroe'), win, f'{f}{i}'))
        assert Y0 + 3 * passo + DISC_R < 262
        pagine.append((f'Rotelle delle plance eroe · plance {2 * f + 1} e {2 * f + 2}',
                       f'12 adesivi a corona Ø {2 * Ro:.1f} mm, foro Ø {2 * Ri:.1f}, intaglio sulla finestra · righe 1-2 plancia {2 * f + 1}, righe 3-4 plancia {2 * f + 2}', b,
                       ['Taglia anche il foro al centro e l’intaglio della finestra (si apre verso il bordo). La finestra dell’adesivo combacia con quella del disco 3D.']))
    tav = [(nm, sotto, ic, TAVOLO_FIN, col) for _, nm, sotto, ic, col in R_TAVOLO] + [('Profezia', 'Oracolo', 'occhio', PROFEZIA_FIN, COL_PROF)]
    b = []
    for i, (nm, sotto, ic, win, col) in enumerate(tav):
        x, y = X0 + i * passo, Y0
        riga = 'rotella della Profezia' if nm == 'Profezia' else 'plancia di gioco'
        b.append(adesivo_rotella(x, y, rotella_disco(x, y, col, nm, sotto, ic, win, riga), win, f't{i}'))
    pagine.append(('Rotelle del tavolo', f'scontro, custode (Sala del Tesoro) e Profezia · adesivi a corona Ø {2 * Ro:.1f} mm', b,
                   ['La base della Profezia resta di carta (pedine.pdf, foglio 2): il perno 3D passa nel foro Ø 4 della base.']))

    for n, (tit, sub, corpo, note_) in enumerate(pagine, 1):
        bb = [hdr(f'Adesivi per i pezzi 3D · {tit} · foglio {n} di {len(pagine)}', sub)] + corpo + [segmento_100(266.0)]
        bb.append(ftr(note_base + note_, y=277))
        write(comp, n, page(fonts('\n'.join(bb))))
    return dict(fogli=len(pagine), tessere_fronti=len(rows), tessere_dorsi=len(rows), stati=n_st, segnalini=gconta,
                rotelle=PLANCE * len(eroe) + len(tav), cripta=1)

# ---------- guida al montaggio della mappa (2 pagine A4): mappa montata col preset Strettoie, cosa stampare, come si monta
def guida_montaggio_mappa():
    comp = 'guida_montaggio_mappa'
    fiori, base, spazi, partenze, preset = dati12()
    righe = preset['Strettoie']['righe']
    d = os.path.join(OUT, comp)
    os.makedirs(d, exist_ok=True)
    sc = 190 / (F12.LARGO + 2 * FASCIA12)
    ox, oy = 10 + FASCIA12 * sc, 21 + FASCIA12 * sc
    o = [f'<g transform="translate({ox:.3f},{oy:.3f}) scale({sc:.5f})">', base12_svg()]
    for s_, (i, lato, fr) in sorted(righe.items()):
        cx, cy = F12.centro_mappa(spazi[s_][0])
        # il fiore si disegna con la freccia a est e si ruota: posizione p -> anello (p - 1 + fr - 1) % 6 + 1, antiorario
        o.append(f'<g transform="rotate({-60 * (fr - 1)} {cx:.3f} {cy:.3f})">'
                 + F12.fiore(fiori[(i, lato)], cx, cy, 0, f'g{s_}', 0.0, False, None, True, d) + '</g>')
    terr = terreno12(righe)
    liberi = [h for h in sorted(terr) if terr[h] in ('prato', 'mattonato', 'pavimento', 'sentiero') and h not in partenze and h not in base]
    if liberi:
        h = [c for c in liberi if c[0] in (7, 8) and c[1] in (9, 10)][:1] or liberi[:1]
        x, y = F12.centro_mappa(h[0])
        img = F12.immagine_arte('SG-CRIPTA', x, y, d)
        if img:
            img = f'<clipPath id="gcr"><polygon points="{F12.pts(F12.vertici(x, y))}"/></clipPath><g clip-path="url(#gcr)">{img}</g>'
        o.append(F12.segnalino_cripta(x, y, img))
    o.append('</g>')
    ymap = oy + F12.ALTO * sc
    b = [hdr('Mappa 12×12 · guida al montaggio', 'esempio montato (versione carta normale): base + 14 fiori nel preset «Strettoie» e la Cripta  ·  pagina 1 di 2')] + o
    b.append(text(105, ymap + FASCIA12 * sc + 5, 'Le frecce d’ottone dei fiori puntano al numero dell’anello indicato dal preset (mappa_preset.pdf); la Cripta è solo un esempio di posizione.', 2.6, BROWN, 'middle'))
    # tabella «Cosa stampare»
    y = ymap + FASCIA12 * sc + 14
    b.append(text(10, y, 'Cosa stampare', 4.0, INK, 'start', True, SERIF)); y += 4
    cols = [10, 62, 108, 150]
    def tabella(titolo, righe_, y):
        b.append(text(10, y + 3.4, titolo, 3.4, COPPER, 'start', True)); y += 5.2
        b.append(f'<rect x="10" y="{y:.2f}" width="190" height="5.2" rx="1" fill="{PLATE}" stroke="{BRASS}" stroke-width="0.25"/>')
        b.append(text(12, y + 3.6, 'file', 3.0, BROWN, 'start', True))
        for x, t in zip(cols[1:], ('carta', 'fronte / retro', 'quantità')):
            b.append(text(x, y + 3.6, t, 2.8, BROWN, 'start', True))
        y += 5.2
        for r in righe_:
            n = max(len(wrap(c, 2.6, w - 2)) for c, w in zip(r, (50, 44, 40, 48)))
            for c, x, w in zip(r, cols, (50, 44, 40, 48)):
                for j, l in enumerate(wrap(c, 2.6, w - 2)):
                    b.append(text(x + 2, y + 3.4 + j * 3.1, l, 2.6, INK))
            y += n * 3.1 + 1.6
            b.append(line(10, y, 200, y, 0.15, '#c9b98f'))
        return y + 3
    y = tabella('VERSIONE CARTA NORMALE (niente plastica)', [
        ('mappa_base.pdf', 'cartoncino 250-300 g', 'solo fronte', '2 fogli (metà sinistra e destra)'),
        ('mappa_fiori.pdf', 'cartoncino 250-300 g', 'fronte/retro a mano, girando sul LATO LUNGO', '3 fogli = 6 pagine: 14 fiori, Cripta'),
        ('mappa_preset.pdf', 'carta normale', 'solo fronte', '10 fogli, uno per preset')], y)
    y = tabella('VERSIONE 3D: carta DA APPLICARE SULLA PLASTICA 3D', [
        ('3d_solidcraft/out/mappa.3mf', 'filamento PLA (stampante 3D)', 'n.a.', '8 piatti: 4 quarti del vassoio, 14 fiori'),
        ('3d_solidcraft/out/rotelle_fulcri.3mf', 'filamento PLA (stampante 3D)', 'n.a.', '4 piatti: 27 rotelle, 27 perni, 27 fermi'),
        ('3d_solidcraft/out/segnalini.3mf', 'filamento PLA (stampante 3D)', 'n.a.', '2 piatti: 31 Stati, 16 Indizi, 4 Forte Volontà, 20 Usato, Cripta'),
        ('3d_solidcraft/out/tessere_esplorazione.3mf', 'filamento PLA (stampante 3D)', 'n.a.', '1 piatto: 36 Tessere Esplorazione'),
        ('3d_solidcraft/out/carta_fiori_3d.pdf', 'cartoncino 160-250 g', 'solo fronte', '5 fogli, 28 facce (una per fiore 3D)'),
        ('carta_base_3d.pdf', 'cartoncino 250-300 g', 'solo fronte, 100% (print-scaling=none)', '4 fogli: un quarto ciascuno (NO, NE, SO, SE), solo cornice di bordo'),
        ('segnalini_3d.pdf', 'carta adesiva o cartoncino 160 g', 'solo fronte, 100% (print-scaling=none)', '6 fogli: fronti e dorsi delle 36 tessere, Cripta, 31 Stati, 40 segnalini, 27 rotelle')], y)
    assert y < 292, y
    write(comp, 1, page(fonts('\n'.join(b))))

    P = [hdr('Mappa 12×12 · come si monta', 'pagina 2 di 2')]
    y = 26.0
    def sezione(titolo, passi, y):
        P.append(text(10, y, titolo, 4.0, INK, 'start', True, SERIF)); y += 3
        P.append(line(10, y, 200, y, 0.3, BRASS)); y += 5.5
        for n, t in enumerate(passi, 1):
            P.append(f'<circle cx="13.2" cy="{y - 1.0:.2f}" r="2.6" fill="{COPPER}"/>' + text(13.2, y, str(n), 3.0, '#fff', 'middle', True))
            for j, l in enumerate(wrap(t, 3.1, 176)):
                P.append(text(19, y + j * 3.9, l, 3.1, INK))
            y += len(wrap(t, 3.1, 176)) * 3.9 + 2.6
        return y + 4
    y = sezione('VERSIONE CARTA NORMALE (mappa_base.pdf + mappa_fiori.pdf)', [
        'Stampa mappa_base.pdf (2 fogli, cartoncino) e taglia ogni metà sulla linea scura esterna e sulla linea di giunzione al centro.',
        'Unisci le due metà da dietro con il nastro adesivo: i rombi di rame sulla giunzione devono combaciare.',
        'Stampa mappa_fiori.pdf fronte/retro: stampa la pagina 1, rimetti il foglio nel cassetto girato sul LATO LUNGO, stampa la pagina 2 (poi 3-4 e 5-6). Prova prima con carta comune e controlla in controluce che il contorno del fronte cada dentro l’abbondanza di 2 mm del retro.',
        'Ritaglia i 14 fiori sulla linea sottile del contorno e la Cripta sulla sua linea (foglio 3 di mappa_fiori.pdf). Segnalini, Stati e tessere Esplorazione: segnalini.pdf e tessere_esplorazione.pdf.',
        'Posa i fiori negli spazi numerati della base, con la freccia d’ottone rivolta al numero 1-6 indicato dal preset (mappa_preset.pdf), oppure scegli posto e rotazione col draft.'], y)
    y = sezione('VERSIONE 3D (carta da applicare sulla plastica: carta_base_3d.pdf + carta_fiori_3d.pdf + segnalini)', [
        'Stampa i 4 file 3MF da 3d_solidcraft/out/ (mappa.3mf 8 piatti, rotelle_fulcri.3mf 4, segnalini.3mf 2, tessere_esplorazione.3mf 1; piatti da 220 × 220 mm). Sono 3MF standard senza metadati di piatto: nello slicer separa i piatti a mano o usa «disponi».',
        'Incastra i 4 quarti del vassoio nell’ordine NO → NE → SO → SE con le code a pomello (23 tra NO e gli altri due, 11 tra NE e SE, 11 tra SO e SE). Da verificare con la prima stampa: tenuta delle code e gioco.',
        'Stampa carta_base_3d.pdf: 4 fogli, uno per quarto (NO, NE, SO, SE), solo la cornice di bordo, al 100% con print-scaling=none (controlla il segmento di 100 mm). Ritaglia ogni foglio sulla linea scura (contorno esterno e interno) e posalo nella tasca del quarto corrispondente del vassoio: non si incolla.',
        'Stampa carta_fiori_3d.pdf, taglia ogni faccia sulla linea scura (1,3 mm dentro il contorno) e incolla una faccia nella tasca sopra di ogni fiore 3D con la colla stick. Il fiore 3D porta una sola faccia (altre 14 facce = altri 14 fiori 3D).',
        'Stampa segnalini_3d.pdf al 100% (controlla il segmento di 100 mm), ritaglia gli adesivi sulla linea scura e incollali nella tasca sopra di ogni pezzo 3D; il dorso delle tessere Esplorazione va sul fondo piatto. Rotelle: perno dal retro della plancia (foro Ø 4), disco sopra la corona, fermo premuto sulla punta finché scatta.',
        'Posa i fiori negli alloggiamenti del vassoio (si girano di 60° in 60°) con la freccia verso il numero 1-6 inciso sul fondo dello spazio, come da preset o draft.'], y)
    assert y < 292, y
    write(comp, 2, page(fonts('\n'.join(P))))

if __name__ == '__main__':
    res = {'rotelle': {k: verifica_rotella(k, vals, win, mh, gold, rr=RAGGIO.get(k, RING_R)) for k, _, _, _, _, vals, win, mh, gold, _ in ROTELLE}}
    res['rotelle']['tavolo'] = verifica_rotella('tavolo', TAVOLO_VALORI, TAVOLO_FIN, 4.5)
    res['rotelle']['Profezia'] = verifica_rotella('Profezia', PROFEZIA_VALORI, PROFEZIA_FIN, PROFEZIA_MH)
    if '--formato' in sys.argv and sys.argv[sys.argv.index('--formato') + 1].upper() == 'A3':
        res['sala_tesoro'] = sala_a3()
        res['plance_eroe'] = plance_eroe_a3()
        res['rotelle_eroe'] = rotelle_a3()
        res['esplorazione'] = esplorazione_a3()
        res['misti'] = misti_a3()
        prova(A3W, A3H, 'A3', [('sala_tesoro.pdf (Sala del Tesoro, A3 orizzontale)', 1),
                               ('mappa 12×12: si stampa dai PDF A4 (mappa_base, mappa_fiori, mappa_preset)', 0)])
        print(res)
        sys.exit(0)
    res['mappa_base'] = mappa_base()
    res['mappa_fiori'] = mf = mappa_fiori()
    res['mappa_preset'] = npr = mappa_preset()
    res['segnalini_3d'] = segnalini_3d()
    guida_montaggio_mappa()
    res['sala_tesoro'] = sala_a4()
    res['esplorazione'] = esplorazione()
    res['segnalini'] = segnalini()
    res['plance_eroe'] = plance_eroe()
    res['rotelle_eroe'] = rotelle_eroe()
    res['pedine'] = [(n, round(w, 1), round(h, 1)) for n, x, y, w, h in pedine()]
    prova(mappa=[('mappa_base.pdf (base 12×12 in 2 metà da unire)', 2),
                 (f"mappa_fiori.pdf (14 fiori, Cripta: {mf['fogli']} fogli fronte/retro)", mf['fogli']),
                 (f'mappa_preset.pdf ({npr} schemi, carta comune)', npr),
                 ('sala_tesoro.pdf (Sala del Tesoro in 2 pezzi)', 1)])
    print(res)
