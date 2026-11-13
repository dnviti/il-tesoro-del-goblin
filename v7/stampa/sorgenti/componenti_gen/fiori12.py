"""Mappa 12×12 a fiori (D24, D25): dati dai CSV di ../dati/ e disegno dei pezzi (SVG in mm). Le pagine le impagina gen.py.

Dati (scritti da v7/idee/mappa_tessere/12x12/mappa12.py --scrivi-dati):
- fiori.csv: fiore (1-14), faccia (A|B), nome, posizione (0 = centro, 1-6 = anello antiorario da E: 1 è l'esagono della
  freccia d'ottone), direzione, terreno, categoria (libero|accidentato|ostacolo), accidentato (0|1);
- base12.csv: un esagono per riga, x, y (1-12), parte (base|spazio), spazio (1-14) e posizione nello spazio, terreno,
  categoria e accidentato degli esagoni di base, partenza (1-6);
- preset12.csv: preset, carta, spazio, fiore, faccia, freccia (1-6: il numero dell'anello dove punta la freccia),
  cambio (1-3: le righe della carta Mappa a metà partita, in ordine).

Stile (approvato il 12/11, terreno dalle 19:01): ogni esagono pieno del suo terreno; il terreno libero ha più aspetti
(prato, mattonato, pavimento, sentiero, guado, ponte) ma è chiaro e senza bordo; gli ostacoli (bosco, rocce, case) sono
scuri, con il bordo netto e gli oggetti sopra; l'acqua (accidentata) è un'unica macchia azzurra con un piccolo «+1» in
un angolo; bordi d'esagono sottili per contare i passi; id piccolo in un angolo.
"""
import csv
import math
import os
import struct
import zlib

from svg import INK, BROWN, GOLD, PAPER, BRASS, BRASS_L, COPPER, PLATE, cog

# Arte generata (arte/mappa_compone.py): png/MF-<NN><A|B>.png (fiore + abbondanza di 2 mm, 300 ppi, centrato sul fiore) e
# png/MB-BASE.png (griglia intera 315 × 269,16 mm, 300 ppi, origine nell'angolo in alto a sinistra) e png/SG-CRIPTA.png
# (segnalino Cripta + abbondanza, centrato sul segnalino). Se un png manca si
# usa il disegno vettoriale. Cartella: variabile GOBLIN_ARTE_MAPPA, oppure gen.py --arte-mappa, altrimenti arte/png.
ARTE_MAPPA = os.environ.get('GOBLIN_ARTE_MAPPA') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'arte', 'png')
PPM_ARTE = 300 / 25.4

W = 25.2                       # esagono da lato a lato
R = W / math.sqrt(3)           # lato = raggio
N = 12
DIR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]   # anello 1-6 antiorario da E (assiali q, r)
SANS, SERIF = 'Liberation Sans Narrow', 'Liberation Serif'
LIBERI = ('prato', 'mattonato', 'pavimento', 'sentiero', 'guado', 'ponte', 'partenza')
OSTACOLI = ('bosco', 'rocce', 'case')

# fondo pieno di ogni terreno; ostacoli scuri con il loro bordo; liberi chiari
FONDO = {'prato': '#d3df9f', 'sentiero': '#ecd5a3', 'mattonato': '#ecd3b8', 'pavimento': '#e1dbce', 'partenza': '#d3df9f',
         'acqua': '#5b93b8', 'guado': '#5b93b8', 'ponte': '#5b93b8',
         'bosco': '#4d7d38', 'rocce': '#8d867b', 'case': '#b47a5c'}
BORDO_OST = {'bosco': '#24401a', 'rocce': '#47423b', 'case': '#5e3220'}
MACCHIA = {'bosco': '#3a6229', 'rocce': '#77706a', 'case': '#9c6247'}
ACQUA, ONDA = '#8cc0dc', '#e8f4fa'
VIOLA, ORO = '#7a4f86', '#d9b45a'


# ------------------------------------------------------------------ dati
def leggi(dati):
    fiori = {}
    for r in csv.DictReader(open(os.path.join(dati, 'fiori.csv'), encoding='utf-8')):
        f = fiori.setdefault((int(r['fiore']), r['faccia']), {'nome': r['nome'], 'celle': {}, 'id': f"MF-{int(r['fiore']):02d}{r['faccia']}"})
        f['celle'][int(r['posizione'])] = r['terreno']
    base, spazi, partenze = {}, {}, {}
    for r in csv.DictReader(open(os.path.join(dati, 'base12.csv'), encoding='utf-8')):
        h = (int(r['x']), int(r['y']))
        if r['parte'] == 'base':
            base[h] = r['terreno']
            if r['partenza']:
                partenze[h] = int(r['partenza'])
        else:
            spazi.setdefault(int(r['spazio']), {})[int(r['posizione'])] = h
    preset = {}
    for r in csv.DictReader(open(os.path.join(dati, 'preset12.csv'), encoding='utf-8')):
        p = preset.setdefault(r['preset'], {'carta': r['carta'], 'righe': {}, 'cambio': {}})
        p['righe'][int(r['spazio'])] = (int(r['fiore']), r['faccia'], int(r['freccia']))
        if r['cambio']:
            p['cambio'][int(r['spazio'])] = int(r['cambio'])
    assert len(fiori) == 28 and len(base) == 46 and len(spazi) == 14 and len(partenze) == 6 and len(preset) == 10
    return fiori, base, spazi, partenze, preset


# ------------------------------------------------------------------ geometria
def centro_mappa(h):
    """centro in mm dell'esagono (x, y) della mappa, con l'origine nell'angolo in alto a sinistra della griglia."""
    c, r = h
    return W * (c - 0.5 + (0.5 if r % 2 == 0 else 0)), R + (r - 1) * 1.5 * R


LARGO, ALTO = 12.5 * W, R * (2 + 11 * 1.5)    # 315 × 269,2 mm


def centro_locale(pos, rot=0):
    """centro in mm, rispetto al centro del fiore, della posizione 0-6 con la freccia verso il numero rot + 1."""
    if pos == 0:
        return 0.0, 0.0
    q, r = DIR[(pos - 1 + rot) % 6]
    return W * (q + r / 2), 1.5 * R * r


def immagine_arte(nome, x, y, cartella, centrata=True):
    """<image> del png arte/png/<nome>.png posato con il centro in (x, y) mm (centrata) o con l'angolo in alto a sinistra
    in (x, y); href relativo alla cartella dove verrà scritto l'svg. None se il png non c'è (si usa il vettoriale)."""
    path = os.path.join(ARTE_MAPPA, nome + '.png')
    if not cartella or not os.path.isfile(path):
        return None
    with open(path, 'rb') as fh:
        testa = fh.read(24)
    pw, ph = struct.unpack('>II', testa[16:24])
    w, h = pw / PPM_ARTE, ph / PPM_ARTE
    if centrata:
        x, y = x - w / 2, y - h / 2
    href = os.path.relpath(path, cartella).replace('&', '&amp;')
    return f'<image href="{href}" x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" preserveAspectRatio="none"/>'


def vertici(x, y, s=R):
    return [(x + s * math.cos(math.radians(a)), y + s * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]


def pts(pp):
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pp)


def rnd(*k):
    return (zlib.crc32('|'.join(map(str, k)).encode()) % 10007) / 10007


def curva(a, b, chiave, amp=1.0):
    (x1, y1), (x2, y2) = a, b
    d = math.dist(a, b) or 1
    k = (rnd(*chiave) - 0.5) * 2 * amp
    mx, my = (x1 + x2) / 2 - (y2 - y1) / d * k, (y1 + y2) / 2 + (x2 - x1) / d * k
    return f'M{x1:.2f} {y1:.2f} Q{mx:.2f} {my:.2f} {x2:.2f} {y2:.2f}'


# ------------------------------------------------------------------ oggetti (stile sgangherato, minimale)
def albero(x, y, s, k):
    j = rnd(k) * 0.6
    return (f'<rect x="{x - 0.5 * s:.2f}" y="{y + 1.2 * s:.2f}" width="{s:.2f}" height="{1.8 * s:.2f}" fill="{BROWN}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{2.6 * s + j:.2f}" fill="#5f9442" stroke="#24401a" stroke-width="0.35"/>'
            f'<circle cx="{x - 0.8 * s:.2f}" cy="{y - 0.9 * s:.2f}" r="{0.9 * s:.2f}" fill="#86b660"/>')


def masso(x, y, s, k):
    j = [(rnd(k, i) - 0.5) * 0.8 * s for i in range(5)]
    p = [(x - 3 * s + j[0], y + 2 * s), (x - 2 * s + j[1], y - 1.5 * s), (x + 0.5 * s + j[2], y - 2.6 * s),
         (x + 2.8 * s + j[3], y - 0.5 * s), (x + 3 * s + j[4], y + 2 * s)]
    return (f'<polygon points="{pts(p)}" fill="#b0a99d" stroke="#47423b" stroke-width="0.4" stroke-linejoin="round"/>'
            f'<polyline points="{pts([p[1], (x - 0.3 * s, y - 0.2 * s), p[2]])}" fill="#d2ccc2"/>'
            f'<path d="M{x - 0.4 * s:.2f} {y - 0.4 * s:.2f} L{x + 0.6 * s:.2f} {y + 1.6 * s:.2f}" stroke="#47423b" stroke-width="0.3"/>')


def casa(x, y, s, k):
    t = (rnd(k) - 0.5) * 6
    return (f'<g transform="rotate({t:.1f} {x:.2f} {y:.2f})">'
            f'<rect x="{x - 2.4 * s:.2f}" y="{y - 0.6 * s:.2f}" width="{4.8 * s:.2f}" height="{3.4 * s:.2f}" fill="{PAPER}" stroke="#5e3220" stroke-width="0.35"/>'
            f'<polygon points="{pts([(x - 3.1 * s, y - 0.4 * s), (x + 0.2 * s, y - 3.6 * s), (x + 3.1 * s, y - 0.4 * s)])}" fill="#9c3f22" stroke="#5e3220" stroke-width="0.35" stroke-linejoin="round"/>'
            f'<rect x="{x - 0.6 * s:.2f}" y="{y + 1.0 * s:.2f}" width="{1.2 * s:.2f}" height="{1.8 * s:.2f}" fill="#5e3220"/>'
            f'<circle cx="{x + 1.4 * s:.2f}" cy="{y - 1.6 * s:.2f}" r="{0.45 * s:.2f}" fill="{BRASS_L}" stroke="{BRASS}" stroke-width="0.2"/></g>')


def icona_partenza(x, y, n):
    return (f'<path d="M{x + 3.2:.2f} {y - 9.2:.2f} v6.5" stroke="{BROWN}" stroke-width="0.5"/>'
            f'<path d="M{x + 3.4:.2f} {y - 9.2:.2f} l4 1.3 l-4 1.3 z" fill="{COPPER}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.8" fill="{VIOLA}" stroke="#fffaf0" stroke-width="0.7"/>'
            f'<text x="{x:.2f}" y="{y + 2.8:.2f}" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-size="8" fill="#fff">{n}</text>')


def segnalino_cripta(x, y, arte=None):
    """segnalino Cripta: un esagono di pietra con l'arco, l'ingranaggio d'ottone e la scritta. arte: <image> di
    arte/png/SG-CRIPTA.png (vedi immagine_arte) al posto del disegno; la scritta CRIPTA resta, chiara con contorno scuro."""
    scritta = (f'<text x="{x:.2f}" y="{y + 9.2:.2f}" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="3.6" fill="#fffaf0"'
               + (f' stroke="{INK}" stroke-width="0.7" stroke-linejoin="round" paint-order="stroke"' if arte else '') + '>CRIPTA</text>')
    if arte:
        return arte + scritta
    return (f'<polygon points="{pts(vertici(x, y))}" fill="#8f877c"/>'
            f'<path d="M{x - 8:.2f} {y + 7:.2f} v-6 a8 8 0 0 1 16 0 v6 z" fill="#6e675d" stroke="#47423b" stroke-width="0.4"/>'
            f'{cog(x, y - 1, 6.8, 10, BRASS_L, None, stroke=BRASS, sw=0.25)}'
            f'<circle cx="{x:.2f}" cy="{y - 1:.2f}" r="5.2" fill="{ORO}" stroke="#7a5a1c" stroke-width="0.6"/>' + scritta)


def fondo_vettoriale(celle, vic, abb, ra):
    """il fondo disegnato a vettori (colori, tessiture, macchie, oggetti): è quello di default e il ripiego se manca l'arte generata."""
    o = []
    if abb:   # abbondanza: ogni esagono allargato col suo fondo, poi i fondi veri sopra
        o += [f'<polygon points="{pts(vertici(x, y, ra))}" fill="{FONDO[t]}"/>' for x, y, t in celle.values()]
    o += [f'<polygon points="{pts(vertici(x, y, R + 0.05))}" fill="{FONDO[t]}"/>' for x, y, t in celle.values()]
    for k, (x, y, t) in celle.items():   # tessitura dei terreni liberi
        if t in ('prato', 'partenza'):
            o += [f'<path d="M{x + dx - 0.9:.2f} {y + dy:.2f} l0.9 -1.6 l0.9 1.6" stroke="#93ab55" stroke-width="0.35" fill="none"/>'
                  for dx, dy in ((-6 + rnd(k, 1) * 3, -5), (4 + rnd(k, 2) * 2, -3), (-3, 5 + rnd(k, 3) * 2), (6, 4))]
        elif t == 'sentiero':
            o += [f'<ellipse cx="{x + (rnd(k, n, "x") - 0.5) * 14:.2f}" cy="{y + (rnd(k, n, "y") - 0.5) * 14:.2f}" rx="{2.5 + rnd(k, n) * 2:.2f}" '
                  f'ry="{1.4 + rnd(k, n, "r"):.2f}" fill="{PAPER}" opacity="0.75"/>' for n in range(2)]
        elif t == 'mattonato':
            for j, dy in enumerate((-6, -2, 2, 6)):
                o.append(f'<path d="M{x - 9:.2f} {y + dy:.2f} h18" stroke="#cfa985" stroke-width="0.3"/>')
                o += [f'<path d="M{x + bx:.2f} {y + dy:.2f} v4" stroke="#cfa985" stroke-width="0.3"/>'
                      for bx in ((-6, -1, 4) if j % 2 else (-3.5, 1.5, 6.5)) if dy < 6]
        elif t == 'pavimento':
            o += [f'<polygon points="{pts([(x + a, y + b), (x + a + 6, y + b + 0.6), (x + a + 5.4, y + b + 5.5), (x + a - 0.4, y + b + 5)])}" '
                  f'fill="none" stroke="#bdb3a2" stroke-width="0.3"/>' for a, b in ((-8, -6), (-1, -5), (-5, 1), (2, 2))]
    sent = [k for k, (_, _, t) in celle.items() if t == 'sentiero']   # traccia ad albero sui soli esagoni di sentiero
    if sent:
        visti, coda = {sent[0]}, [sent[0]]
        while coda:
            a = coda.pop(0)
            for b in vic[a]:
                if b in sent and b not in visti:
                    visti.add(b)
                    coda.append(b)
                    o.append(f'<path d="{curva(celle[a][:2], celle[b][:2], (a, b), 1.2)}" stroke="#a9834f" stroke-width="0.6" '
                             f'stroke-dasharray="1.6 1.1" stroke-linecap="round" fill="none" opacity="0.8"/>')
    acque = [k for k, (_, _, t) in celle.items() if t in ('acqua', 'guado', 'ponte')]
    o += macchia(celle, vic, acque, ACQUA, W * 0.84, R * 0.86)
    o += [f'<path d="M{celle[k][0] - 5:.2f} {celle[k][1] + dy:.2f} q2.5 -1.8 5 0 t5 0" stroke="{ONDA}" stroke-width="0.5" fill="none"/>'
          for k in acque if celle[k][2] == 'acqua' for dy in (-3, 3)]
    for k in acque:   # guado (sassi) e ponte (assi): verso gli esagoni liberi vicini del pezzo
        x1, y1, t = celle[k]
        if t == 'acqua':
            continue
        for b in vic[k]:
            if celle[b][2] in ('acqua',) + OSTACOLI:
                continue
            x2, y2 = (x1 + celle[b][0]) / 2, (y1 + celle[b][1]) / 2
            if t == 'ponte':
                o.append(f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#7a4f2b" stroke-width="7"/>'
                         f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#c49a5e" stroke-width="5.6" stroke-dasharray="1.6 0.6"/>')
            else:
                o += [f'<ellipse cx="{x1 + (x2 - x1) * f:.2f}" cy="{y1 + (y2 - y1) * f:.2f}" rx="1.6" ry="1.1" fill="#d2ccc2" stroke="#6e685f" stroke-width="0.25"/>'
                      for f in (0.2, 0.55, 0.9)]
    for terr in OSTACOLI:
        o += macchia(celle, vic, [k for k, (_, _, t) in celle.items() if t == terr], MACCHIA[terr], W * 0.6, R * 0.8)
    for k, (x, y, t) in celle.items():
        if t == 'bosco':
            o += [albero(x + dx, y + dy, 1.05, (k, dx)) for dx, dy in ((-4.5, -3.5), (4.2, -2.8), (-0.5, 3.5), (5, 4.5), (-6, 3))]
        elif t == 'rocce':
            o += [masso(x + dx, y + dy, s, (k, dx)) for dx, dy, s in ((-3.2, 0.5, 1.3), (3.6, 1.8, 1.0), (1.5, -4.5, 0.8))]
        elif t == 'case':
            o += [casa(x + dx, y + dy, s, (k, dx)) for dx, dy, s in ((-3.6, -1.6, 0.95), (3.6, 1.6, 0.85), (2.5, -5.5, 0.7))]
    return o


# ------------------------------------------------------------------ un pezzo (fiore o base)
def pezzo(celle, cid, abb=0.0, taglio=False, etichetta=None, freccia=None, partenze=None, arte=None):
    """celle: {chiave: (x, y, terreno)} in mm. abb: abbondanza (mm) oltre il contorno; taglio: linea di taglio sul
    contorno (solo sul fronte); etichetta: id piccolo; freccia: (x, y, dx, dy) dell'esagono 1 dell'anello; arte: svg di
    un <image> (vedi immagine_arte) che sostituisce il fondo vettoriale: restano sopra bordi, +1, Partenze, freccia, id."""
    vic = {a: [b for b, (xb, yb, _) in celle.items() if b != a and abs(math.dist((xa, ya), (xb, yb)) - W) < 0.5]
           for a, (xa, ya, _) in celle.items()}
    ra = R + abb / math.cos(math.radians(30))
    o = [f'<clipPath id="{cid}">' + ''.join(f'<polygon points="{pts(vertici(x, y, ra + 0.05))}"/>' for x, y, _ in celle.values()) + '</clipPath>',
         f'<g clip-path="url(#{cid})">']
    if arte:   # arte generata (png a 300 ppi): sostituisce fondi, tessiture, acqua e oggetti; sopra restano i segni di gioco
        o.append(arte)
    else:
        o += fondo_vettoriale(celle, vic, abb, ra)
    # bordo netto degli ostacoli (dentro l'esagono) e bordi sottili di tutti gli esagoni
    o += [f'<polygon points="{pts(vertici(x, y, R - 0.5))}" fill="none" stroke="{BORDO_OST[t]}" stroke-width="{0.6 if arte else 1.0}"/>'
          for x, y, t in celle.values() if t in OSTACOLI]
    o += [f'<polygon points="{pts(vertici(x, y))}" fill="none" stroke="{INK}" stroke-opacity="{0.8 if arte else 0.5}" stroke-width="{0.35 if arte else 0.3}"/>' for x, y, _ in celle.values()]   # con l'arte il bordo scuro del modello non c'è più: la linea è l'unico contorno
    for x, y, t in celle.values():   # acqua: «+1» discreto nell'angolo in basso a destra
        if t == 'acqua':
            bx, by = x + R * 0.48, y + R * 0.42
            o.append(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="2.3" fill="#fffaf0" stroke="#2f5d7c" stroke-width="0.3"/>'
                     f'<text x="{bx:.2f}" y="{by + 0.95:.2f}" text-anchor="middle" font-family="{SANS}" font-weight="bold" font-size="2.6" fill="#2f5d7c">+1</text>')
    for k, (x, y, t) in celle.items():
        if t == 'partenza':
            o.append(icona_partenza(x, y, partenze[k]))
    if freccia:   # freccia d'ottone sul lato esterno dell'esagono 1 dell'anello
        x, y, dx, dy = freccia
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        px, py = x + ux * (W / 2 - 1.4), y + uy * (W / 2 - 1.4)
        o.append(f'<polygon points="{pts([(px + ux * 1.8, py + uy * 1.8), (px - uy * 1.9, py + ux * 1.9), (px + uy * 1.9, py - ux * 1.9)])}" '
                 f'fill="{BRASS_L}" stroke="{BRASS}" stroke-width="0.3"/>')
    if etichetta:   # id piccolo nell'angolo in basso a destra dell'esagono più in basso a destra
        x, y, _ = max(celle.values(), key=lambda c: c[0] + c[1])
        lw = len(etichetta) * 1.15 + 1.6
        x1, y1 = x + W / 2 - 1.0 - lw, y + R / 2 - 3.4
        o.append(f'<rect x="{x1:.2f}" y="{y1:.2f}" width="{lw:.2f}" height="2.9" rx="0.6" fill="{PLATE}" stroke="{BRASS}" stroke-width="0.2"/>'
                 f'<text x="{x1 + lw - 0.8:.2f}" y="{y1 + 2.2:.2f}" text-anchor="end" font-family="{SANS}" font-weight="bold" font-size="2.2" fill="{INK}">{etichetta}</text>')
    o.append('</g>')
    if taglio:
        o.append(contorno([(x, y) for x, y, _ in celle.values()], '#222222', 0.25))
    return ''.join(o)


def macchia(celle, vic, chiavi, colore, largo, raggio):
    o = [f'<circle cx="{celle[k][0]:.2f}" cy="{celle[k][1]:.2f}" r="{raggio:.2f}" fill="{colore}"/>' for k in chiavi]
    o += [f'<path d="{curva(celle[a][:2], celle[b][:2], (a, b, colore), 0.8)}" stroke="{colore}" stroke-width="{largo:.2f}" stroke-linecap="round" fill="none"/>'
          for a in chiavi for b in vic[a] if b in chiavi and str(a) < str(b)]
    return o


def contorno(centri, col, sw):
    """lati esterni dell'unione degli esagoni (linea di taglio o contorno)."""
    conta = {}
    for x, y in centri:
        v = vertici(x, y)
        for i in range(6):
            k = tuple(sorted(((round(v[i][0], 1), round(v[i][1], 1)), (round(v[(i + 1) % 6][0], 1), round(v[(i + 1) % 6][1], 1)))))
            conta[k] = conta.get(k, 0) + 1
    return ''.join(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
                   for (a, b), n in conta.items() if n == 1)


def fiore(f, x0, y0, rot=0, cid='f', abb=0.0, taglio=False, etichetta=None, freccia=True, arte=None):
    """una faccia di fiore col centro in (x0, y0). arte: cartella dove verrà scritto l'svg; se c'è arte/png/MF-<id>.png
    (rot deve essere 0: l'arte è disegnata con la freccia a est) il png sostituisce il fondo vettoriale."""
    img = immagine_arte(f['id'], x0, y0, arte) if arte and rot == 0 else None
    celle = {p: (x0 + cx, y0 + cy, t) for p, t in f['celle'].items() for cx, cy in [centro_locale(p, rot)]}
    fr = None
    if freccia:
        x1, y1, _ = celle[1]
        fr = (x1, y1, x1 - x0, y1 - y0)
    return pezzo(celle, cid, abb, taglio, etichetta, fr, arte=img)
