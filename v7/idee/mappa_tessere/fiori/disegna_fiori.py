#!/usr/bin/env python3
"""Mock-up dei fiori (fase 1, solo idea): SVG in mm 1:1 e PNG (ImageMagick) in questa cartella.

Uso (dalla radice del repo):  python3 v7/idee/mappa_tessere/fiori/disegna_fiori.py

  fiori_campioni.svg/.png      4 pezzi del preset base (striscia di Partenza 2 e bosco, fiore della Cripta 1, riva
                               del guado ovest, fiume del ponte) più il retro del fiume (Flegias, senza le 2 mura);
  fiori_strettoie.svg/.png     il preset base «Strettoie» montato con i suoi 18 pezzi, staccati di qualche mm.

Ogni pezzo è una scena unica vista dall'alto. La strada è un TERRENO: ogni esagono di strada è terra battuta fino ai
suoi lati, fusa con gli esagoni di strada vicini (anche sul pezzo accanto), con al massimo un filo di traccia ad albero
dentro il pezzo. Ogni altro esagono è pieno del suo ostacolo: acqua fusa in un fiume, bosco a macchia, rocce a gruppi,
case a borgo; non esiste prato vuoto. Bordi d'esagono sottili per contare i passi; icone di «?», Partenze e Cripte;
targhetta piccola in un angolo (posizione · preset, 01 = TM-01). Palette del gioco (componenti_gen/svg.py) e colori
naturali. Lato esterno della mappa tagliato dritto.
"""
import math
import os
import subprocess
import sys
import zlib

QUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, QUI)
import fiori as F  # noqa: E402

ts = F.ts
W, R = F.W, F.R
COL = 'ABCDEFGHIJ'
# palette del gioco (stampa/sorgenti/componenti_gen/svg.py) + terreni naturali
INK, BROWN, GOLD, PAPER = '#2a2118', '#6b4a2b', '#b8862b', '#f4ead5'
BRASS, BRASS_L, COPPER, PLATE = '#a8823a', '#e8cd8f', '#a65a32', '#f7eedb'
FUORI = '#d9cfa8'                     # fuori dalla mappa (lati dritti)
SABBIA, SENTIERO_BORDO = BRASS_L, '#a9834f'   # strada = terra battuta (#e8cd8f), traccia sottile
ACQUA, ACQUA_RIVA, ONDA = '#8cc0dc', '#5b93b8', '#e8f4fa'
BOSCO_SOTTO, CHIOMA, CHIOMA_LUCE, TRONCO = '#4f7a3a', '#6a9a48', '#8dbb63', '#6b4a2b'
ROCCIA_SOTTO, ROCCIA, ROCCIA_LUCE = '#9a9389', '#b4ada2', '#d2ccc2'
TETTO, MURO_CASA, SELCIATO = '#9c4a2b', '#f4ead5', '#c79e80'
# fondo pieno di ogni esagono: nessun esagono è «prato vuoto» (nei preset ogni esagono è strada o un ostacolo)
BASE = {'strada': SABBIA, 'bosco': '#7da45a', 'rocce': '#c2baac', 'case': '#dbb9a0',
        'acqua': ACQUA_RIVA, 'guado': ACQUA_RIVA, 'ponte': ACQUA_RIVA}
VIOLA, ORO = '#7a4f86', '#d9b45a'
X0, Y0 = 0.0, 0.0


def centro(h):
    c, r = COL.index(h[0]), int(h[1:])
    return X0 + W * (c + 0.5 + (0.5 if r % 2 == 0 else 0)), Y0 + R + (r - 1) * 1.5 * R


def vertici(x, y, s=R):
    return [(x + s * math.cos(math.radians(a)), y + s * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]


def pts(pp):
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pp)


def lato(a, b):
    """punto medio del lato in comune tra a e b."""
    (xa, ya), (xb, yb) = centro(a), centro(b)
    return (xa + xb) / 2, (ya + yb) / 2


def vertici_lato(a, b):
    va = vertici(*centro(a))
    return [p for p in vertici(*centro(b)) if any(math.dist(p, q) < 1e-6 for q in va)]


def rnd(*chiave):
    """numero «a caso» in [0, 1) fisso per chiave: il disegno è uguale a ogni esecuzione."""
    return (zlib.crc32('|'.join(map(str, chiave)).encode()) % 10007) / 10007


# ------------------------------------------------------------------ contorno: esagoni + riempimenti fino al bordo dritto
TOP, BOT = Y0, Y0 + R * (2 + 9 * 1.5)
SX, DX = X0, X0 + 10.5 * W


def regioni(h):
    """poligoni dell'esagono h e dei pezzetti tra l'esagono e il bordo dritto della mappa."""
    x, y = centro(h)
    c, r = COL.index(h[0]), int(h[1:])
    out = [vertici(x, y)]
    if r == 1:
        out.append([(x - W / 2, y - R / 2), (x, y - R), (x + W / 2, y - R / 2), (x + W / 2, TOP), (x - W / 2, TOP)])
    if r == 10:
        out.append([(x - W / 2, y + R / 2), (x, y + R), (x + W / 2, y + R / 2), (x + W / 2, BOT), (x - W / 2, BOT)])
    if c == 0 and r % 2 == 0:
        out.append([(SX, y - R), (x - W / 2, y - R / 2), (x - W / 2, y + R / 2), (SX, y + R)])
    if c == 9 and r % 2 == 1:
        out.append([(DX, y - R), (x + W / 2, y - R / 2), (x + W / 2, y + R / 2), (DX, y + R)])
    if r == 1 and c == 9:    # angolo in alto a destra: triangolo tra il riempimento sopra e quello a destra
        out.append([(x + W / 2, TOP), (DX, TOP), (x + W / 2, y - R / 2)])
    if r == 10 and c == 0:   # angolo in basso a sinistra
        out.append([(SX, BOT), (x - W / 2, y + R / 2), (x - W / 2, BOT)])
    return out


def contorno(celle):
    """lati esterni del pezzo (linea di taglio): i lati che compaiono una volta sola tra tutti i poligoni."""
    conta = {}
    for h in celle:
        for poly in regioni(h):
            for i in range(len(poly)):
                a, b = poly[i], poly[(i + 1) % len(poly)]
                if math.dist(a, b) < 0.01:
                    continue
                k = tuple(sorted(((round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1)))))
                conta[k] = conta.get(k, 0) + 1
    return [k for k, n in conta.items() if n == 1]


# ------------------------------------------------------------------ scena di un pezzo
def curva(a, b, chiave, ampiezza=1.0):
    """tratto un po' sgangherato da a a b: quadratica con il punto di controllo spostato di lato."""
    (x1, y1), (x2, y2) = a, b
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d = math.dist(a, b) or 1
    k = (rnd(*chiave) - 0.5) * 2 * ampiezza
    cx, cy = mx - (y2 - y1) / d * k, my + (x2 - x1) / d * k
    return f'M{x1:.2f} {y1:.2f} Q{cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}'


def macchia(celle, colore, larghezza, raggio, vicini_di):
    """forme fuse: un cerchio per esagono e un tratto spesso tra esagoni vicini dello stesso tipo."""
    o = [f'<circle cx="{centro(h)[0]:.2f}" cy="{centro(h)[1]:.2f}" r="{raggio:.2f}" fill="{colore}"/>' for h in celle]
    o += [f'<path d="{curva(centro(a), centro(b), (a, b, colore), 0.8)}" stroke="{colore}" stroke-width="{larghezza:.2f}" '
          f'stroke-linecap="round" fill="none"/>' for a in celle for b in vicini_di(a) if b in celle and a < b]
    return o


def albero(x, y, s, chiave):
    j = rnd(chiave) * 0.6
    return (f'<rect x="{x - 0.5 * s:.2f}" y="{y + 1.2 * s:.2f}" width="{s:.2f}" height="{1.8 * s:.2f}" fill="{TRONCO}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{2.6 * s + j:.2f}" fill="{CHIOMA}" stroke="{BOSCO_SOTTO}" stroke-width="0.35"/>'
            f'<circle cx="{x - 0.8 * s:.2f}" cy="{y - 0.9 * s:.2f}" r="{0.9 * s:.2f}" fill="{CHIOMA_LUCE}"/>')


def masso(x, y, s, chiave):
    j = [(rnd(chiave, i) - 0.5) * 0.8 * s for i in range(6)]
    p = [(x - 3 * s + j[0], y + 2 * s), (x - 2 * s + j[1], y - 1.5 * s), (x + 0.5 * s + j[2], y - 2.6 * s),
         (x + 2.8 * s + j[3], y - 0.5 * s), (x + 3 * s + j[4], y + 2 * s)]
    return (f'<polygon points="{pts(p)}" fill="{ROCCIA}" stroke="#6e685f" stroke-width="0.35" stroke-linejoin="round"/>'
            f'<polyline points="{pts([p[1], (x - 0.3 * s, y - 0.2 * s), p[2]])}" fill="{ROCCIA_LUCE}" stroke="none"/>'
            f'<path d="M{x - 0.4 * s:.2f} {y - 0.4 * s:.2f} L{x + 0.6 * s:.2f} {y + 1.6 * s:.2f}" stroke="#6e685f" stroke-width="0.3"/>')


def casa(x, y, s, chiave):
    t = (rnd(chiave) - 0.5) * 0.8
    return (f'<g transform="rotate({t * 8:.1f} {x:.2f} {y:.2f})">'
            f'<rect x="{x - 2.4 * s:.2f}" y="{y - 0.6 * s:.2f}" width="{4.8 * s:.2f}" height="{3.4 * s:.2f}" fill="{MURO_CASA}" stroke="{BROWN}" stroke-width="0.35"/>'
            f'<polygon points="{pts([(x - 3.1 * s, y - 0.4 * s), (x + 0.2 * s, y - 3.6 * s), (x + 3.1 * s, y - 0.4 * s)])}" fill="{TETTO}" stroke="{BROWN}" stroke-width="0.35" stroke-linejoin="round"/>'
            f'<rect x="{x - 0.6 * s:.2f}" y="{y + 1.0 * s:.2f}" width="{1.2 * s:.2f}" height="{1.8 * s:.2f}" fill="{BROWN}"/>'
            f'<circle cx="{x + 1.4 * s:.2f}" cy="{y - 1.6 * s:.2f}" r="{0.45 * s:.2f}" fill="{BRASS_L}" stroke="{BRASS}" stroke-width="0.2"/></g>')


def ingranaggio(x, y, r, n=8):
    p = []
    for i in range(2 * n):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * 0.78
        p += [(x + rr * math.cos(a - 0.12), y + rr * math.sin(a - 0.12)), (x + rr * math.cos(a + 0.12), y + rr * math.sin(a + 0.12))]
    return f'<polygon points="{pts(p)}" fill="{BRASS_L}" stroke="{BRASS}" stroke-width="0.25"/>'


def icona(h, t):
    x, y = centro(h)
    if t == '?':
        return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.6" fill="#fffaf0" stroke="{INK}" stroke-width="0.6"/>'
                f'<text x="{x:.2f}" y="{y + 2.6:.2f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="7.6" fill="{INK}">?</text>')
    if t[0] == 'P':
        return (f'<path d="M{x + 3.2:.2f} {y - 9.2:.2f} v6.5" stroke="{BROWN}" stroke-width="0.5"/>'
                f'<path d="M{x + 3.4:.2f} {y - 9.2:.2f} l4 1.3 l-4 1.3 z" fill="{COPPER}"/>'
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.8" fill="{VIOLA}" stroke="#fffaf0" stroke-width="0.7"/>'
                f'<text x="{x:.2f}" y="{y + 2.8:.2f}" text-anchor="middle" font-weight="800" font-size="8" fill="#fff">{t[1]}</text>')
    if t[0] == 'C':
        return (f'<path d="M{x - 8:.2f} {y + 6.5:.2f} v-7 a8 8 0 0 1 16 0 v7 z" fill="#8f877c" stroke="#5e5950" stroke-width="0.4"/>'
                f'{ingranaggio(x, y - 1, 6.6, 10)}'
                f'<circle cx="{x:.2f}" cy="{y - 1:.2f}" r="5.2" fill="{ORO}" stroke="#7a5a1c" stroke-width="0.6"/>'
                f'<text x="{x:.2f}" y="{y + 1.9:.2f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="8" fill="{INK}">{t[1]}</text>')
    return ''


def muro(a, b):
    """muro sul lato tra a e b: listello di pietra con 2 rivetti d'ottone, un po' storto."""
    (x1, y1), (x2, y2) = vertici_lato(a, b)
    k = 0.08
    x1, y1, x2, y2 = x1 + (x2 - x1) * k, y1 + (y2 - y1) * k, x2 - (x2 - x1) * k, y2 - (y2 - y1) * k
    rv = ''.join(f'<circle cx="{x1 + (x2 - x1) * f:.2f}" cy="{y1 + (y2 - y1) * f:.2f}" r="0.55" fill="{BRASS_L}" stroke="{BRASS}" stroke-width="0.2"/>'
                 for f in (0.25, 0.75))
    return (f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#4a3a2a" stroke-width="3.0" stroke-linecap="round"/>'
            f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#8a7a66" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="2.2 0.7"/>' + rv)


def scena(part, i, k, cid, codice=True):
    """svg del pezzo i con la faccia del preset k, ritagliato al suo contorno."""
    celle, mozz, muri = part.faccia(i, k)
    t = dict(celle)
    p = part.pezzi[i]

    def vic(h):
        return [v for v in ts.vicini(h) if v in p]
    acque = [h for h in p if t[h] in ('acqua', 'guado', 'ponte')]
    strade = [h for h in p if F.strada(t[h])]
    o = [f'<clipPath id="{cid}">' + ''.join(f'<polygon points="{pts(poly)}"/>' for h in p for poly in regioni(h)) + '</clipPath>',
         f'<g clip-path="url(#{cid})">']
    o += [f'<polygon points="{pts(poly)}" fill="{FUORI}"/>' for h in p for poly in regioni(h)[1:]]
    # ogni esagono pieno del suo terreno: strada = terra battuta, ostacoli = bosco, rocce, borgo (niente prato vuoto)
    o += [f'<polygon points="{pts(vertici(*centro(h), R + 0.05))}" fill="{BASE[t[h] if t[h] in BASE else "strada"]}"/>' for h in p]
    # strada: chiazze di pergamena e sassolini, fuse tra esagoni vicini perché ogni esagono arriva fino ai lati
    for h in strade:
        x, y = centro(h)
        o += [f'<ellipse cx="{x + (rnd(h, n, "x") - 0.5) * 14:.2f}" cy="{y + (rnd(h, n, "y") - 0.5) * 14:.2f}" rx="{2.5 + rnd(h, n) * 2.5:.2f}" '
              f'ry="{1.5 + rnd(h, n, "r") * 1.5:.2f}" fill="{PAPER}" opacity="0.7"/>' for n in range(2)]
        o += [f'<circle cx="{x + (rnd(h, n, "a") - 0.5) * 18:.2f}" cy="{y + (rnd(h, n, "b") - 0.5) * 18:.2f}" r="0.45" fill="{SENTIERO_BORDO}" opacity="0.7"/>' for n in range(5)]
    # traccia: un solo filo ad albero tra i centri degli esagoni di strada del pezzo (niente triangoli, non esce dal pezzo)
    if strade:
        bx, by = baricentro(strade)
        radice = min(strade, key=lambda h: math.dist(centro(h), (bx, by)))
        visti, coda, rami = {radice}, [radice], []
        while coda:
            a = coda.pop(0)
            for b in vic(a):
                if b in strade and b not in visti and (a, b) not in muri and (b, a) not in muri and t[b] not in ('guado', 'ponte'):
                    visti.add(b)
                    coda.append(b)
                    rami.append((a, b))
        o += [f'<path d="{curva(centro(a), centro(b), (a, b), 1.2)}" stroke="{SENTIERO_BORDO}" stroke-width="0.6" '
              f'stroke-dasharray="1.6 1.1" stroke-linecap="round" fill="none" opacity="0.75"/>' for a, b in rami]
    # acqua fusa
    o += macchia(acque, ACQUA_RIVA, W * 0.98, R * 0.98, vic)
    o += macchia(acque, ACQUA, W * 0.84, R * 0.86, vic)
    o += [f'<path d="M{centro(h)[0] - 5:.2f} {centro(h)[1] + dy:.2f} q2.5 -1.8 5 0 t5 0" stroke="{ONDA}" stroke-width="0.5" fill="none"/>'
          for h in acque if t[h] == 'acqua' for dy in (-3, 3)]
    # bosco, rocce, case: macchie fuse più scure sopra il fondo pieno, poi gli oggetti
    for terr, sotto, larg in (('bosco', BOSCO_SOTTO, W * 0.75), ('rocce', ROCCIA_SOTTO, W * 0.55), ('case', SELCIATO, W * 0.6)):
        cc = [h for h in p if t[h] == terr]
        o += macchia(cc, sotto, larg, R * 0.8, vic)
    # ponte (assi) e guado (sassi): verso gli esagoni di strada del pezzo e verso quelli fissi (uguali in tutti i preset)
    for a in (h for h in p if t[h] in ('ponte', 'guado')):
        for b in ts.vicini(a):
            if not (F.strada(t[b]) if b in p else (b in ts.FISSI and F.strada(ts.PRESET['base'][0][b]))):
                continue
            (x1, y1), (x2, y2) = centro(a), lato(a, b)
            if t[a] == 'ponte':
                o.append(f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#8a5a2b" stroke-width="7" stroke-linecap="butt"/>'
                         f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#c49a5e" stroke-width="5.6" stroke-dasharray="1.6 0.6"/>')
            else:
                o += [f'<ellipse cx="{x1 + (x2 - x1) * f:.2f}" cy="{y1 + (y2 - y1) * f:.2f}" rx="1.6" ry="1.1" fill="{ROCCIA_LUCE}" '
                      f'stroke="#6e685f" stroke-width="0.25"/>' for f in (0.2, 0.5, 0.8)]
    # oggetti sopra le macchie
    for h in p:
        x, y = centro(h)
        if t[h] == 'bosco':
            o += [albero(x + dx, y + dy, 1.05, (h, dx)) for dx, dy in ((-4.5, -3.5), (4.2, -2.8), (-0.5, 3.5), (5, 4.5), (-6, 3))]
        elif t[h] == 'rocce':
            o += [masso(x + dx, y + dy, s, (h, dx)) for dx, dy, s in ((-3.2, 0.5, 1.3), (3.6, 1.8, 1.0), (1.5, -4.5, 0.8))]
        elif t[h] == 'case':
            o += [casa(x + dx, y + dy, s, (h, dx)) for dx, dy, s in ((-3.6, -1.6, 0.95), (3.6, 1.6, 0.85), (2.5, -5.5, 0.7))]
    # bordi d'esagono sottili ma leggibili (per contare i passi)
    o += [f'<polygon points="{pts(vertici(*centro(h)))}" fill="none" stroke="{INK}" stroke-opacity="0.5" stroke-width="0.3"/>' for h in p]
    o += [muro(*m) for m in muri]
    o += [icona(h, t[h]) for h in p]
    if codice:   # targhetta piccola nell'angolo in basso a destra di un esagono senza icone: posizione · preset
        libere = [h for h in p if t[h] not in ('?',) and t[h][0] not in 'PC'] or list(p)
        h = max(libere, key=lambda h: (centro(h)[0] + centro(h)[1]))
        x, y = centro(h)
        tag = f'{i} · ' + ' '.join(n.replace('TM-', '') for n in part.disegni(i)[part.faccia(i, k)])   # 01 = TM-01
        lw = len(tag) * 0.78 + 1.2
        x1, y1 = x + W / 2 - 0.9 - lw, y + R / 2 - 2.9
        o.append(f'<rect x="{x1:.2f}" y="{y1:.2f}" width="{lw:.2f}" height="2.3" rx="0.6" fill="{PLATE}" stroke="{BRASS}" stroke-width="0.2" opacity="0.9"/>'
                 f'<text x="{x1 + lw / 2:.2f}" y="{y1 + 1.7:.2f}" text-anchor="middle" font-size="1.45" fill="{INK}">{tag}</text>')
    o.append('</g>')
    o += [f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{INK}" stroke-width="0.45" stroke-linecap="round"/>' for a, b in contorno(p)]
    return ''.join(o)


def baricentro(celle):
    xs = [centro(h) for h in celle]
    return sum(x for x, _ in xs) / len(xs), sum(y for _, y in xs) / len(xs)


def documento(w, h, corpo, titolo, sotto):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}mm" height="{h:.1f}mm" viewBox="-12 -24 {w:.1f} {h:.1f}" '
            f'font-family="sans-serif"><rect x="-12" y="-24" width="{w:.1f}" height="{h:.1f}" fill="{PLATE}"/>'
            f'<text x="-4" y="-14" font-family="serif" font-weight="800" font-size="7" fill="{BROWN}">{titolo}</text>'
            f'<text x="-4" y="-8" font-size="3.4" font-style="italic" fill="{BROWN}">{sotto}</text>{corpo}</svg>')


def scrivi(nome, svg):
    f = os.path.join(QUI, nome)
    with open(f + '.svg', 'w', encoding='utf-8') as fh:
        fh.write(svg)
    subprocess.run(['magick', '-density', '254', f + '.svg', '-background', PLATE, '-flatten', f + '.png'], check=True)
    print(f + '.png')


def main():
    part = F.scelta()
    # 1. preset base montato, pezzi staccati
    cx, cy = (SX + DX) / 2, (TOP + BOT) / 2
    corpo = []
    for i, p in enumerate(part.pezzi):
        bx, by = baricentro(p)
        dx, dy = (bx - cx) * 0.035, (by - cy) * 0.035
        corpo.append(f'<g transform="translate({dx:.2f} {dy:.2f})">{scena(part, i, "base", f"m{i}")}</g>')
    scrivi('fiori_strettoie', documento(DX - SX + 24, BOT - TOP + 38, ''.join(corpo),
                                        'Preset base «Strettoie» con 18 pezzi a fiore',
                                        'Pezzi staccati di qualche mm per vederli. Esagono 25,2 mm; mappa 265 × 226 mm; lati esterni tagliati dritti.'))
    # 2. campioni: 4 pezzi del preset base + il retro del fiume
    scelti = [(3, 'base', 'Partenza 2 e bosco (fiore)'), (5, 'base', 'Cripta 1 con i muri (fiore)'),
              (6, 'base', 'Riva ovest del fiume (8 esagoni)'), (8, 'base', 'Fiume del ponte, fronte'),
              (8, 'TM-08', 'Lo stesso fiume, retro (Flegias)')]
    corpo, x = [], 0
    for n, (i, k, nome) in enumerate(scelti):
        p = part.pezzi[i]
        xs = [v[0] for h in p for poly in regioni(h) for v in poly]
        ys = [v[1] for h in p for poly in regioni(h) for v in poly]
        ox, oy = x - min(xs), -min(ys)
        corpo.append(f'<g transform="translate({ox:.2f} {oy:.2f})">{scena(part, i, k, f"c{n}")}</g>'
                     f'<text x="{x + (max(xs) - min(xs)) / 2:.2f}" y="{max(ys) - min(ys) + 7:.2f}" text-anchor="middle" font-size="3.6" fill="{INK}">{nome}</text>')
        x += max(xs) - min(xs) + 10
    scrivi('fiori_campioni', documento(x + 14, 125, ''.join(corpo), 'Fiori del preset base (e un retro)',
                                       'Strada = terra battuta fusa tra esagoni; ostacoli pieni; acqua fusa; muri stampati; targhetta: posizione · preset.'))


if __name__ == '__main__':
    main()
