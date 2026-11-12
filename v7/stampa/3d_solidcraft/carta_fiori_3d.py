"""Carta dei fiori per la versione 3D: facce A e B stampate separatamente, solo fronte, con la linea di taglio spostata
verso l'interno del contorno ideale di `rientro` mm (gioco del fiore + bordino + gioco della carta), così ogni faccia entra
nella tasca del fiore 3D (una sopra, una sotto).

Riusa il disegno del kit (v7/stampa/sorgenti/componenti_gen/fiori12.py): vettoriale, oppure l'arte generata di
arte/png/MF-*.png se c'è (GOBLIN_ARTE_MAPPA=CARTELLA per un'altra cartella di png). Senza arte il PDF resta com'era.
Si lancia da genera_3d_solidcraft.py; da solo: python3 v7/stampa/3d_solidcraft/carta_fiori_3d.py
"""
import os
import subprocess
import sys

from shapely import set_precision
from shapely.geometry import Polygon
from shapely.ops import unary_union

QUI = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(QUI, '..', 'sorgenti', 'componenti_gen')
DATI = os.path.join(QUI, '..', 'sorgenti', 'dati')
sys.dont_write_bytecode = True
sys.path.insert(0, GEN)
import fiori12 as F12  # noqa: E402  disegno delle facce dei fiori (lo stesso di mappa_fiori.pdf)

POSTI = [(63.0, 58.0), (147.0, 58.0), (63.0, 140.0), (147.0, 140.0), (63.0, 222.0), (147.0, 222.0)]   # come mappa_fiori.pdf
INK, BROWN, BRASS, PLATE = F12.INK, F12.BROWN, F12.BRASS, F12.PLATE


def text(x, y, s, size, fill=INK, anchor='middle', bold=False, fam=F12.SANS):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size:.2f}" fill="{fill}" text-anchor="{anchor}"'
            f'{" font-weight=\"bold\"" if bold else ""}>{s}</text>')


def linea_taglio(x0, y0, rientro):
    """contorno del fiore centrato in (x0, y0) spostato di rientro mm verso l'interno."""
    celle = [set_precision(Polygon(F12.vertici(x0 + cx, y0 + cy)), 1e-6) for p in range(7) for cx, cy in [F12.centro_locale(p, 0)]]
    return unary_union(celle).buffer(-rientro, join_style='mitre', mitre_limit=10)


def faccia(f, chiave, x0, y0, rientro, cid, arte=None):
    """una faccia: disegno del kit fino al contorno ideale (oltre la linea di taglio resta rientro mm di abbondanza),
    linea di taglio rientrata e id piccolo dentro la linea. arte: cartella dell'svg; se c'è l'arte generata della faccia
    (arte/png/MF-<id>.png, vedi fiori12.ARTE_MAPPA) riempie l'esagono al posto del vettoriale."""
    o = [F12.fiore(f, x0, y0, 0, cid, 0.0, False, None, False, arte)]
    t = linea_taglio(x0, y0, rientro)
    # freccia d'ottone verso il lato esterno dell'esagono 1 (come nel kit), con la punta 0,3 mm dentro la linea di taglio
    ux, uy = F12.centro_locale(1, 0)
    n = (ux * ux + uy * uy) ** 0.5
    ux, uy = ux / n, uy / n
    d = F12.W / 2 - rientro - 0.3 - 1.8
    px, py = x0 + ux * (F12.W + d), y0 + uy * (F12.W + d)
    freccia = [(px + ux * 1.8, py + uy * 1.8), (px - uy * 1.9, py + ux * 1.9), (px + uy * 1.9, py - ux * 1.9)]
    assert t.contains(Polygon(freccia)), 'freccia fuori dalla linea di taglio'
    o.append(f'<polygon points="{F12.pts(freccia)}" fill="{F12.BRASS_L}" stroke="{BRASS}" stroke-width="0.3"/>')
    o.append(f'<path d="M{" L".join(f"{x:.3f} {y:.3f}" for x, y in t.exterior.coords)} Z" fill="none" stroke="#222222" stroke-width="0.25"/>')
    # id nell'esagono più in basso a destra, come nel kit ma spostato dentro la linea di taglio
    x, y = max(((x0 + cx, y0 + cy) for p in range(7) for cx, cy in [F12.centro_locale(p, 0)]), key=lambda c: c[0] + c[1])
    lw = len(chiave) * 1.15 + 1.6
    x1, y1 = x + F12.W / 2 - 1.0 - rientro - lw, y + F12.R / 2 - 3.4 - rientro
    assert t.contains(Polygon([(x1, y1), (x1 + lw, y1), (x1 + lw, y1 + 2.9), (x1, y1 + 2.9)])), 'id fuori dalla linea di taglio'
    o.append(f'<rect x="{x1:.2f}" y="{y1:.2f}" width="{lw:.2f}" height="2.9" rx="0.6" fill="{PLATE}" stroke="{BRASS}" stroke-width="0.2"/>'
             + text(x1 + lw - 0.8, y1 + 2.2, chiave, 2.2, INK, 'end', True))
    return ''.join(o), t


def genera(path, rientro, tmp):
    fiori = F12.leggi(DATI)[0]
    facce = sorted(fiori, key=lambda k: (k[0], k[1]))           # 1A, 1B, 2A, ... 14B
    pagine = [facce[i:i + len(POSTI)] for i in range(0, len(facce), len(POSTI))]
    pdfs, aree = [], []
    for n, blocco in enumerate(pagine, 1):
        b = [text(105, 11, f'Mappa 12×12 · fiori 3D, da applicare sulla plastica 3D · foglio {n} di {len(pagine)}', 4.2, INK, 'middle', True, F12.SERIF),
             text(105, 16.5, 'Cartoncino 160-250 g, SOLO FRONTE, al 100% («Dimensioni effettive»). Ogni faccia è un pezzo a sé.', 2.6, BROWN)]
        for j, (i, lato) in enumerate(blocco):
            x, y = POSTI[j]
            svg, t = faccia(fiori[(i, lato)], f'{i}{lato}', x, y, rientro, f'f3d{n}{j}', tmp)
            b.append(svg)
            aree.append(t.bounds)
        piede = [f'Taglia sulla linea scura: è {rientro:.2f} mm dentro il contorno dell\'esagono, così la faccia entra nella tasca del fiore 3D.'.replace('.', ',', 1),
                 'Incolla la faccia nella tasca sopra del fiore 3D (colla stick): il fondo del fiore è piatto.',
                 'La freccia d\'ottone indica l\'esagono 1 dell\'anello (preset). Le due facce si incollano in qualsiasi rotazione.']
        b += [text(105, 270 + k * 4, l, 2.6, BROWN) for k, l in enumerate(piede)]
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297" '
               f'font-family="{F12.SANS}">\n' + '\n'.join(b) + '\n</svg>\n')
        sp = os.path.join(tmp, f'carta3d_{n:02d}.svg')
        open(sp, 'w', encoding='utf-8').write(svg)
        vc, pdf = sp[:-4] + '.vectorcraft', sp[:-4] + '.pdf'
        for a, z in ((sp, vc), (vc, pdf)):
            subprocess.run(['vectorcraft-cli', 'convert', a, z], check=True, capture_output=True, timeout=600)
        pdfs.append(pdf)
    subprocess.run(['pdfcraft-cli', 'combine', *pdfs, '--out', path], check=True, capture_output=True, timeout=600)
    w = max(a[2] - a[0] for a in aree)
    h = max(a[3] - a[1] for a in aree)
    return {'pdf': os.path.basename(path), 'fogli': len(pagine), 'facce': len(facce), 'rientro_taglio_mm': round(rientro, 3),
            'carta_tagliata_mm': [round(w, 2), round(h, 2)]}


if __name__ == '__main__':
    import json
    import tempfile
    sys.path.insert(0, QUI)
    import genera_3d_solidcraft as G
    d = tempfile.mkdtemp(prefix='carta3d-')
    try:
        os.makedirs(G.OUT, exist_ok=True)
        print(json.dumps(genera(os.path.join(G.OUT, 'carta_fiori_3d.pdf'), G.P['gioco_fiore'] + G.P['bordino'] + G.P['gioco_carta'], d)))
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
