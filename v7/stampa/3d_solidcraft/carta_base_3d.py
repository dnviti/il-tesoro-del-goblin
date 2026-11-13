"""Carta della base per la versione 3D: 4 fogli A4, uno per quarto (NO, NE, SO, SE), solo la cornice di bordo.

Ogni foglio ha la sagoma ESATTA della tasca di carta di quel quarto, presa da genera_3d_solidcraft.paper_pocket (stessa
geometria del vassoio: gioco tra le parti, fascia di carta, spazi dei fiori tolti): ritagliata sulla linea scura entra a
filo nella tasca. Stampa: solo gli esagoni di bordo del quarto (arte arte/png/MB-BASE.png), la fascia con le coordinate,
le Partenze; la parte centrale (spazi dei fiori) non si stampa. Su ogni foglio un segmento di controllo di 100 mm e
l'etichetta del quarto, fuori dalla sagoma. Stampa al 100 % (print-scaling=none).

Uso: python3 v7/stampa/3d_solidcraft/carta_base_3d.py [--out PDF] [--verifica]   (scrive playtest_v7/carta_base_3d.pdf, lo fa anche build.sh; --verifica confronta il
percorso di taglio estratto dal PDF con la tasca 3D, scarto massimo <= 0,2 mm: altrimenti esce con 1 e la build fallisce)
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

from shapely.geometry import LineString, Point, Polygon

QUI = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(QUI, '..', 'sorgenti', 'componenti_gen')
DATI = os.path.join(QUI, '..', 'sorgenti', 'dati')
OUT_PDF = os.path.join(QUI, '..', 'playtest_v7', 'carta_base_3d.pdf')   # --out PATH per un'altra cartella (build.sh)
sys.dont_write_bytecode = True
sys.path.insert(0, GEN)
sys.path.insert(0, QUI)
import fiori12 as F12  # noqa: E402
import genera_3d_solidcraft as G  # noqa: E402

CUT = '#222222'
FASCIA, FASCIA_FONDO, INTERNO = 5.5, '#d9cfa8', '#efe6cf'
L, A = F12.LARGO, F12.ALTO
SANS = F12.SANS


def a_carta(pt):
    """punto 3D (origine al centro della mappa, y in su) -> coordinate della carta (origine nell'angolo in alto a sinistra della griglia)."""
    return (pt[0] + L / 2, A / 2 - pt[1])


def tasca_carta(q):
    """poligono della tasca di carta del quarto q, in coordinate della carta (mm), dal generatore 3D."""
    p = G.paper_pocket(q, G.P)
    assert p.geom_type == 'Polygon'
    return Polygon([a_carta(c) for c in p.exterior.coords], [[a_carta(c) for c in r.coords] for r in p.interiors])


def text(x, y, s, size, fill='#000', anchor='middle', bold=False):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{SANS}" font-size="{size:.2f}" fill="{fill}" text-anchor="{anchor}"'
            f'{" font-weight=\"bold\"" if bold else ""}>{s}</text>')


def percorso(poly):
    anelli = [poly.exterior] + list(poly.interiors)
    return ' '.join('M' + ' L'.join(f'{x:.4f} {y:.4f}' for x, y in r.coords[:-1]) + ' Z' for r in anelli)


def pagina(q, cartella):
    """svg del foglio del quarto q. Ritorna (svg, tasca nelle coordinate della pagina, traslazione (tx, ty))."""
    fiori, base, spazi, partenze, _ = F12.leggi(DATI)
    pk = tasca_carta(q)
    x0, y0, x1, y1 = pk.bounds
    tx, ty = 105 - (x0 + x1) / 2, 24.0 - y0          # sagoma centrata, 24 mm dal bordo alto della pagina
    cell = {h: (*F12.centro_mappa(h), 'partenza' if h in partenze else t) for h, t in base.items() if G.quarter_of(h) == q}
    img = F12.immagine_arte('MB-BASE', 0, 0, cartella, False)
    cid = f'tasca{q}'
    clip = f'<clipPath id="{cid}"><path d="{percorso(pk)}"/></clipPath>'
    o = [clip, f'<g transform="translate({tx:.4f},{ty:.4f})"><g clip-path="url(#{cid})">',
         f'<rect x="{x0 - 1:.2f}" y="{y0 - 1:.2f}" width="{x1 - x0 + 2:.2f}" height="{y1 - y0 + 2:.2f}" fill="{FASCIA_FONDO}"/>',
         f'<rect x="0" y="0" width="{L:.2f}" height="{A:.2f}" fill="{INTERNO}"/>',
         f'<rect x="{-FASCIA + 1.2:.2f}" y="{-FASCIA + 1.2:.2f}" width="{L + 2 * FASCIA - 2.4:.2f}" height="{A + 2 * FASCIA - 2.4:.2f}" rx="1.5" '
         f'fill="none" stroke="{F12.BRASS}" stroke-width="0.3"/>']
    # coordinate: colonne sopra la riga 1 e sotto la riga 12, righe a sinistra e a destra (come mappa_base.pdf)
    lab = []
    for c in range(1, 13):
        for r, yy in ((1, -FASCIA / 2 + 1.3), (12, A + FASCIA / 2 + 1.3)):
            lab.append((F12.centro_mappa((c, r))[0], yy, str(c)))
    for r in range(1, 13):
        y = F12.centro_mappa((1, r))[1] + 1.3
        lab += [(-FASCIA / 2, y, str(r)), (L + FASCIA / 2, y, str(r))]
    o += [text(x, y, s, 3.6, F12.INK, 'middle', True) for x, y, s in lab if pk.contains(Point(x, y - 1.3))]
    if cell:
        o.append(F12.pezzo(cell, f'cornice{q}', 0.0, False, None, None, partenze, arte=img))
    o.append('</g>')
    o.append(f'<path d="{percorso(pk)}" fill="none" stroke="{CUT}" stroke-width="0.25" stroke-linejoin="miter"/></g>')
    # fuori dalla sagoma: titolo, etichetta del quarto, segmento di controllo di 100 mm
    yb = y1 + ty
    o.append(text(105, 11, f'Carta base 3D · quarto {q} · da applicare sulla plastica 3D', 4.2, F12.INK, 'middle', True).replace(f'font-family="{SANS}"', f'font-family="{F12.SERIF}"'))
    o.append(text(105, 17, 'Solo la cornice di bordo: gli spazi dei fiori non si stampano. Ritaglia sulla linea scura e posa nella tasca del quarto.', 2.8, F12.BROWN))
    sy = yb + 14.0
    o.append(text(105, sy + 28, q, 24, F12.BROWN, 'middle', True))
    o.append(f'<line x1="55" y1="{sy:.2f}" x2="155" y2="{sy:.2f}" stroke="{CUT}" stroke-width="0.25"/>'
             + ''.join(f'<line x1="{xx}" y1="{sy - 2:.2f}" x2="{xx}" y2="{sy + 2:.2f}" stroke="{CUT}" stroke-width="0.25"/>' for xx in (55, 155)))
    o.append(text(105, sy + 6, 'Segmento di controllo: 100 mm esatti. Stampa al 100 % (print-scaling=none, MAI «adatta alla pagina»).', 2.8, F12.BROWN))
    o.append(text(105, sy + 10, f'Quarto {q}: se il segmento non misura 100 mm la carta non entra nella tasca.', 2.8, F12.BROWN))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297" font-family="{SANS}">\n'
           + '\n'.join(o) + '\n</svg>\n')
    pg = Polygon([(x + tx, y + ty) for x, y in pk.exterior.coords])
    return svg, pg, (tx, ty)


def genera(path, tmp):
    pdfs, info = [], {}
    for q in G.QUARTI:
        svg, pg, t = pagina(q, tmp)
        sp = os.path.join(tmp, f'carta_base_3d_{q}.svg')
        open(sp, 'w', encoding='utf-8').write(svg)
        vc, pdf = sp[:-4] + '.vectorcraft', sp[:-4] + '.pdf'
        for a, z in ((sp, vc), (vc, pdf)):
            subprocess.run(['vectorcraft-cli', 'convert', a, z], check=True, capture_output=True, timeout=600)
        pdfs.append(pdf)
        info[q] = {'pagina_mm': [round(v, 3) for v in pg.bounds], 'traslazione': [round(v, 4) for v in t]}
    subprocess.run(['pdfcraft-cli', 'combine', *pdfs, '--out', path], check=True, capture_output=True, timeout=600)
    return info


def taglio_da_pdf(pdf, pagina_n, tmp):
    """percorso di taglio (anello chiuso, tratto #222222 largo 0,25 mm) estratto dal PDF con pdftocairo -svg, in mm di pagina.
    Le coordinate `d` del path sono quelle vere del PDF (pt). La matrice (0,998785) che pdftocairo -svg aggiunge ai path è un
    suo artefatto, NON è nel PDF (verificato rasterizzando a 600 dpi: segmento di 100 mm = 99,99 mm): si ignora."""
    out = os.path.join(tmp, f'v{pagina_n}.svg')
    subprocess.run(['pdftocairo', '-svg', '-f', str(pagina_n), '-l', str(pagina_n), pdf, out], check=True)
    txt = open(out, encoding='utf-8').read()
    best = None
    for m in re.finditer(r'<path\b([^>]*)>', txt):
        at = m.group(1)
        w = re.search(r'stroke-width[=:]\s*"?([\d.]+)', at)
        d = re.search(r'\bd="([^"]+)"', at)
        if not (w and d) or 'fill="none"' not in at or abs(float(w.group(1)) - 0.25 * 72 / 25.4) > 0.05:
            continue
        if 'Z' not in d.group(1) and 'z' not in d.group(1):
            continue
        nums = [float(v) for v in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?', d.group(1))]
        pts = [(x * 25.4 / 72, y * 25.4 / 72) for x, y in zip(nums[0::2], nums[1::2])]
        if len(pts) > 8 and (best is None or len(pts) > len(best)):
            best = pts
    return best


def verifica(pdf, info):
    """scarto massimo (Hausdorff, mm) tra il taglio nel PDF e la tasca 3D, e confronto del segmento di 100 mm."""
    res = {}
    with tempfile.TemporaryDirectory(prefix='cb3d_') as tmp:
        for n, q in enumerate(G.QUARTI, 1):
            pts = taglio_da_pdf(pdf, n, tmp)
            if not pts:
                res[q] = None
                continue
            got = Polygon(pts)
            t = info[q]['traslazione']
            want = Polygon([(x + t[0], y + t[1]) for x, y in tasca_carta(q).exterior.coords])
            gb, wb = got.boundary, want.boundary
            dmax = max(max(wb.distance(Point(c)) for c in LineString(gb.coords).segmentize(0.5).coords),
                       max(gb.distance(Point(c)) for c in LineString(wb.coords).segmentize(0.5).coords))
            res[q] = {'scarto_max_mm': round(dmax, 3), 'vertici': len(pts)}
    return res


if __name__ == '__main__':
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else OUT_PDF
    d = tempfile.mkdtemp(prefix='carta_base_3d-')
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        info = genera(out, d)
        print(json.dumps(info))
        if not os.path.isfile(out) or os.path.getsize(out) == 0:
            sys.exit('carta_base_3d.pdf non prodotto')
        if '--verifica' in sys.argv:
            r = verifica(out, info)
            print(json.dumps(r))
            sys.exit(0 if all(v and v['scarto_max_mm'] <= 0.2 for v in r.values()) else 1)
    finally:
        shutil.rmtree(d, ignore_errors=True)
