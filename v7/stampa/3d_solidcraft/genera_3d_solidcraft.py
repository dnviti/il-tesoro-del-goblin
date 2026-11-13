#!/usr/bin/env python3
"""Mappa 12×12 e segnalini in 3D, costruiti in SolidCraft (12/11, decisione di Daniele: niente Blender).

Uso (dalla radice del repo):  python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py
Serve: python3 con shapely >= 2.1 e numpy, `solidcraft-cli` (SolidCraft >= 0.40) nel PATH.

Pezzi (mappa da v7/stampa/sorgenti/dati/base12.csv: spazi dei fiori, posizioni 0-6, esagoni di bordo):
- VASSOIO in 4 parti (NO, NE, SO, SE): fondo, alloggio unico per i 14 fiori, tasca per la carta della base del kit
  (mappa_base.pdf, con le coordinate, ritagliata lungo i contorni d'ottone degli spazi), numeri degli spazi e cifre 1-6
  dell'anello incisi sul fondo dell'alloggio. Le 4 parti si uniscono con code a pomello nel fondo.
- FIORE da 7 esagoni senza incastri, fondo piatto e tasca per la carta sopra (carta: out/carta_fiori_3d.pdf).
- SEGNALINO CRIPTA (esagono) con la tasca per la carta di mappa_fiori.pdf.
- SEGNALINI DEL KIT IN 3D (D29, 13/11): Tessere Esplorazione (36), segnalini tondi Indizio / Forte Volontà / Usato
  (segnalini.csv), tessere Stato (stati.csv) e i dischi delle rotelle (6 per plancia eroe, scontro, custode, Profezia).
  Ogni pezzo ha il contorno ESATTO del pezzo di carta del kit, fondo piatto, bordino in rilievo e tasca sopra per
  l'adesivo di segnalini_3d.pdf (tasca = contorno - bordino, adesivo = tasca - gioco_carta). Le rotelle hanno la
  finestra passante e un mozzo pieno al centro.
- PERNO delle rotelle in 2 pezzi a scatto: perno con la testa sotto la plancia e la gola in cima, fermo piatto con 2
  ganasce a sbalzo che si aprono nel piano e si chiudono nella gola. Tutti e due si stampano piatti senza supporti.
Quantità dai CSV del kit; 4 file 3MF in out/ (mappa, rotelle_fulcri, segnalini, tessere_esplorazione) su piatti da 220 × 220.

Lo script calcola la geometria in pianta con shapely, la rende parametrica (ogni coordinata del documento SolidCraft
è un'espressione lineare dei parametri: passo, margine, gioco, bordino...; i coefficienti si ricavano per differenze
finite e si controllano), scrive gli script SolidCraft, li fa girare con `solidcraft-cli run` (salva .solidcraft
parametrici, STL e 3MF), confronta volumi e ingombri con quelli calcolati, monta le prove d'incastro e d'alloggio,
scrive le anteprime PNG e out/risultati.json.
"""
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import types
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from shapely import affinity, set_precision
from shapely.geometry import LineString, MultiLineString, Point, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import split, unary_union

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'out')
DATI = os.path.join(QUI, '..', 'sorgenti', 'dati')
BASE12 = os.path.join(DATI, 'base12.csv')
sys.dont_write_bytecode = True
sys.path.insert(0, QUI)
import carta_fiori_3d  # noqa: E402  PDF delle facce dei fiori per la versione 3D


def leggi_mappa(path):
    """mappa 12×12 da base12.csv: x = colonna, y = riga (righe dispari a sinistra, pari spostate di mezzo esagono a
    destra), parte base/spazio, spazio 1-14, posizione 0 (centro) e 1-6 (anello, antiorario da E)."""
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    m = types.SimpleNamespace()
    m.CELLE = [(int(r['x']), int(r['y'])) for r in rows]
    m.N = max(max(h) for h in m.CELLE)
    assert len(m.CELLE) == m.N * m.N
    m.AX = {(c, r): (c - 1 - (r - 1) // 2, r - 1) for c, r in m.CELLE}
    m.HX = {v: k for k, v in m.AX.items()}
    m.DIR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    pos = {(int(r['spazio']), int(r['posizione'])): (int(r['x']), int(r['y'])) for r in rows if r['parte'] == 'spazio'}
    m.SPAZI = {s: h for (s, p), h in sorted(pos.items()) if p == 0}
    m.BASE = [(int(r['x']), int(r['y'])) for r in rows if r['parte'] == 'base']
    m.vicini = lambda h: [m.HX[(m.AX[h][0] + a, m.AX[h][1] + b)] for a, b in m.DIR if (m.AX[h][0] + a, m.AX[h][1] + b) in m.HX]
    m.anello = lambda s, k: pos[(s, k + 1)]
    for s, c in m.SPAZI.items():      # le posizioni 1-6 del CSV sono i vicini in direzione E, NE, NO, O, SO, SE
        q, r = m.AX[c]
        assert all(pos[(s, k + 1)] == m.HX[(q + a, r + b)] for k, (a, b) in enumerate(m.DIR)), s
    return m


M = leggi_mappa(BASE12)

# ---- parametri del documento SolidCraft (mm) -------------------------------------------------------------------
PARAMETRI = [
    ('passo', 25.2, 'esagono da lato a lato = distanza tra i centri (mappa 25,2; 20-30)'),
    ('margine', 7.0, 'bordo del vassoio oltre la mappa: contiene la fascia della carta della base (>= fascia_carta + gioco_carta + 0,8)'),
    ('gioco', 0.15, 'gioco per lato tra le parti del vassoio e sulle code (0,1-0,25)'),
    ('gioco_fiore', 0.2, 'gioco per lato tra fiore e alloggio: tra due fiori il doppio (0,1-0,35)'),
    ('fondo', 1.2, 'spessore del fondo del vassoio = altezza delle code (1-2); sotto i numeri incisi restano fondo - incisione = 0,8'),
    ('alloggio_prof', 2.0, 'profondità dell alloggio dei fiori (1,5 ... fiore_spessore)'),
    ('fiore_spessore', 3.0, 'spessore del fiore (2,5-4): sporge di fiore_spessore - alloggio_prof'),
    ('tasca_prof', 0.5, 'profondità delle tasche per la carta (cartoncino 0,3-0,4; 0,3-1)'),
    ('bordino', 0.85, 'bordino tra contorno e tasca della carta (0,6-1,5)'),
    ('gioco_carta', 0.25, 'gioco per lato tra carta ritagliata e tasca (0,15-0,4)'),
    ('fascia_carta', 5.5, 'fascia delle coordinate della carta della base (mappa_base.pdf: FASCIA12 = 5,5; < margine - gioco_carta - 0,8)'),
    ('segnalino_spessore', 2.0, 'spessore di Cripta, tessere, segnalini e Stati (1,5-3)'),
    ('tessera_d', 24.0, 'diametro delle Tessere Esplorazione (tessere_esplorazione.pdf: Ø 24)'),
    ('gettone_d', 20.0, 'diametro dei segnalini Indizio, Forte Volontà e Usato (segnalini.pdf: Ø 20)'),
    ('stato_l', 26.0, 'lato lungo della tessera Stato (segnalini.pdf: 26 × 18)'),
    ('stato_a', 18.0, 'lato corto della tessera Stato'),
    ('stato_r', 1.2, 'raggio degli angoli della tessera Stato (> bordino)'),
    ('rotella_d', 52.0, 'diametro dei dischi delle rotelle (rotelle_eroe.pdf: Ø 52)'),
    ('corona_r', 20.0, 'distanza della finestra dal centro della rotella (corona della plancia, RING_R)'),
    ('rotella_spessore', 2.0, 'spessore dei dischi delle rotelle (1,6-2,5)'),
    ('mozzo_r', 6.25, 'raggio del mozzo pieno al centro della rotella, dove appoggia il fermo (>= fermo_d/2)'),
    ('foro_perno', 3.8, 'diametro del foro delle rotelle (perno_d + 2 × 0,2 di gioco)'),
    ('perno_d', 3.4, 'diametro del perno e del suo dente (3-4)'),
    ('collo_d', 2.9, 'diametro della gola del perno, dove si chiudono le ganasce del fermo (perno_d - 0,5)'),
    ('testa_d', 10.0, 'diametro della testa del perno, sotto la plancia (copre il foro Ø 4 della plancia)'),
    ('testa_h', 0.8, 'spessore della testa del perno (0,6-1,2)'),
    ('carta_plancia', 0.3, 'spessore della plancia di cartoncino (0,25-0,4)'),
    ('fermo_d', 12.0, 'diametro del fermo (sta sul mozzo: <= 2 × mozzo_r)'),
    ('fermo_h', 1.2, 'spessore del fermo e delle sue ganasce (1-1,6)'),
    ('gioco_assiale', 0.15, 'aria tra il fermo e il dente del perno, con la plancia da carta_plancia'),
    ('smusso', 0.4, 'smusso degli spigoli di fiore e segnalini, sopra e sotto (0,2-0,6; < bordino)'),
    ('raggio_angolo', 3.0, 'raggio degli angoli esterni del vassoio (0,5-6)'),
    ('coda_collo', 2.6, 'larghezza del collo della coda a pomello (2-3)'),
    ('coda_testa', 4.0, 'diametro del pomello (coda_collo + 1 ... 5)'),
    ('coda_lunga', 3.9, 'quanto la coda entra nella parte vicina (3,5-4,5; > coda_testa/2)'),
    ('numero_alto', 8.0, 'altezza del numero dello spazio inciso sul fondo (5-10)'),
    ('cifra_alta', 4.0, 'altezza delle cifre 1-6 dell anello incise sul fondo (3-5)'),
    ('incisione', 0.4, 'profondità delle incisioni (0,4-0,8; fondo: lascia fondo - incisione = 0,8)'),
]
P = {n: v for n, v, _ in PARAMETRI}
DENTRO = 0.5            # di quanto collo di coda e incavo sconfinano oltre il lato (sovrapposizione, mm)
GIOCO_Z = 0.3           # aria sopra la coda, sotto il tetto dell'incavo
SPOSTA_PROVA = 0.6      # prova di presa: tirando una parte di 0,6 mm le code devono toccarsi
PIATTO = 220.0          # piatto di stampa ipotizzato (mm)
QUARTI = ['NO', 'NE', 'SO', 'SE']   # anche ordine di montaggio: la coda sta sempre sulla parte posata prima

S3 = math.sqrt(3)
RU = 1 / S3


# ---- espressioni lineari nei parametri --------------------------------------------------------------------------
class Lin(dict):
    """combinazione lineare {parametro: coefficiente}; la chiave '' è la costante in mm."""

    def __add__(self, o):
        r = Lin(self)
        for k, v in o.items():
            r[k] = r.get(k, 0.0) + v
        return r

    def __sub__(self, o):
        return self + o * -1

    def __mul__(self, s):
        return Lin({k: v * s for k, v in self.items()})

    def val(self, vals=None):
        vals = vals or P
        return sum(v * (1.0 if k == '' else vals[k]) for k, v in self.items())

    def expr(self):
        terms = [f'{self[k]:.12g}' if k == '' else f'{self[k]:.12g}*{k}'
                 for k in sorted(self, key=lambda k: (k == '', k)) if abs(self[k]) >= 1e-12]
        if not any(k and abs(c) >= 1e-12 for k, c in self.items()):
            terms.append('0*passo')          # una coordinata senza parametri non sarebbe fissa nello schizzo
        return ' + '.join(terms).replace('+ -', '- ')


def L(name, c=1.0):
    return Lin({name: c})


class V2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, o):
        return V2(self.x + o.x, self.y + o.y)

    def val(self, vals=None):
        return (self.x.val(vals), self.y.val(vals))

    def expr(self):
        return [self.x.expr(), self.y.expr()]


def vdir(d, lin):
    return V2(lin * d[0], lin * d[1])


def rings_of(g):
    polys = [g] if g.geom_type == 'Polygon' else [p for p in g.geoms if p.area > 1e-6]
    out = []
    for p in polys:
        p = orient(p.simplify(1e-6), 1.0)        # toglie i vertici allineati e le fessure da arrotondamento
        out.append(list(p.exterior.coords)[:-1])
        out += [list(i.coords)[:-1] for i in p.interiors]
    return out


def linearize(fn, names):
    """fn(vals) -> geometria shapely in mm, lineare e omogenea nei parametri `names`. Restituisce gli anelli come
    liste di V2 con i coefficienti trovati per differenze finite, controllati su un secondo punto."""
    base = rings_of(fn(P))
    d = 0.5          # la geometria è esattamente lineare: un passo grande evita gli errori di arrotondamento
    pert = {}
    for n in names:
        v = dict(P)
        v[n] += d
        pert[n] = rings_of(fn(v))

    def match(ring, cand):
        c = np.mean(ring, axis=0)
        best = min((r for r in cand if len(r) == len(ring)), key=lambda r: np.linalg.norm(np.mean(r, axis=0) - c))
        b = np.array(best)
        return [b[np.argmin(np.linalg.norm(b - np.array(p), axis=1))] for p in ring]

    out = []
    for ring in base:
        cols = {n: match(ring, pert[n]) for n in names}
        pts = []
        for i, p in enumerate(ring):
            cx = Lin({n: (cols[n][i][0] - p[0]) / d for n in names})
            cy = Lin({n: (cols[n][i][1] - p[1]) / d for n in names})
            assert abs(cx.val() - p[0]) < 1e-4 and abs(cy.val() - p[1]) < 1e-4, 'geometria non omogenea nei parametri'
            pts.append(V2(cx, cy))
        out.append(pts)
    # controllo: con tutti i parametri cambiati del 3-7 % le espressioni danno la geometria ricalcolata
    v2 = {k: P[k] * (1.03 + 0.01 * i) for i, k in enumerate(P)}
    chk = fn(v2)
    pred = unary_union([Polygon([p.val(v2) for p in r]) for r in out]) if len(out) == 1 else None
    if pred is not None:
        assert pred.symmetric_difference(chk).area < 1e-4 * max(chk.area, 1), 'espressioni non coerenti'
    return out


# ---- reticolo e mappa (passo 1 -> mm con i parametri) ------------------------------------------------------------
def centre_u(h):
    """centro dell'esagono (colonna, riga) di mappa12, a passo 1, riga 1 in alto."""
    q, r = M.AX[h]
    return (q + r / 2, -r * S3 / 2)


FRAME_U = {'O': -0.5, 'E': M.N, 'N': RU, 'S': -(M.N - 1) * S3 / 2 - RU}
C0 = ((FRAME_U['O'] + FRAME_U['E']) / 2, (FRAME_U['N'] + FRAME_U['S']) / 2)   # origine: centro della mappa


def xy(pu, vals):
    return ((pu[0] - C0[0]) * vals['passo'], (pu[1] - C0[1]) * vals['passo'])


def hexagon(h, vals, grow=0.0):
    cx, cy = xy(centre_u(h), vals)
    r = vals['passo'] * RU + grow / math.cos(math.radians(30))
    return Polygon([(cx + r * math.cos(math.radians(90 + 60 * k)), cy + r * math.sin(math.radians(90 + 60 * k))) for k in range(6)])


def outer(vals):
    x0, y0 = xy((FRAME_U['O'], FRAME_U['S']), vals)
    x1, y1 = xy((FRAME_U['E'], FRAME_U['N']), vals)
    m = vals['margine']
    return box(x0 - m, y0 - m, x1 + m, y1 + m)


def quarter_of(h):
    x, y = centre_u(h)
    return ('N' if y > C0[1] else 'S') + ('O' if x < C0[0] else 'E')


CELLE_Q = {q: [h for h in M.CELLE if quarter_of(h) == q] for q in QUARTI}
SPAZIO_CELLE = {s: [M.SPAZI[s]] + [M.anello(s, k) for k in range(6)] for s in M.SPAZI}
CELLE_SPAZI = {h for s in SPAZIO_CELLE for h in SPAZIO_CELLE[s]}
assert len(CELLE_SPAZI) == 98 and set(M.BASE) == set(M.CELLE) - CELLE_SPAZI


def quarter_ideal(q, vals):
    """parte q del vassoio: i suoi esagoni, più la sua fetta di fascia e di triangoli di bordo. Fuori dalla mappa il
    taglio prosegue dritto, perpendicolare al bordo, dal punto in cui il taglio tra gli esagoni esce dalla mappa."""
    cells = {h: set_precision(hexagon(h, vals), 1e-9) for h in M.CELLE}
    union = {k: unary_union([cells[h] for h in M.CELLE if k in quarter_of(h)]) for k in 'NSOE'}
    mapu = unary_union(list(cells.values()))
    o = outer(vals)
    x0, y0, x1, y1 = o.bounds
    cuts = []
    for a, b in (('N', 'S'), ('O', 'E')):
        seam = union[a].boundary.intersection(union[b].boundary)
        ends = [p for p in (Point(c) for ln in getattr(seam, 'geoms', [seam]) for c in ln.coords)
                if p.distance(mapu.exterior) < 1e-5]
        for p in {(round(e.x, 6), round(e.y, 6)) for e in ends}:
            ex, ey = p
            # il taglio parte 1 mm dentro l'esagono, così attraversa sicuramente tutta la fascia
            if a == 'N':      # taglio orizzontale: esce a sinistra o a destra
                sx = -1 if ex < 0 else 1
                cuts.append(LineString([(ex - sx, ey), (x0 - 1 if sx < 0 else x1 + 1, ey)]))
            else:             # taglio verticale: esce in alto o in basso
                sy = 1 if ey > 0 else -1
                cuts.append(LineString([(ex, ey - sy), (ex, y1 + 1 if sy > 0 else y0 - 1)]))
    assert len(cuts) == 4, cuts
    fuori = split(o.difference(mapu), MultiLineString(cuts))
    qcells = {k: unary_union([cells[h] for h in CELLE_Q[k]]) for k in QUARTI}

    def contatto(p, k):
        return p.buffer(1e-5).intersection(qcells[k].boundary).length

    mine = qcells[q]
    pieces = [p for p in fuori.geoms if max(QUARTI, key=lambda k: contatto(p, k)) == q]
    g = unary_union([mine] + [set_precision(p, 1e-9) for p in pieces]).simplify(1e-6)   # via i doppioni da arrotondamento
    assert g.geom_type == 'Polygon' and not g.interiors
    return g


def quarter_shape(q, vals):
    return quarter_ideal(q, vals).buffer(-vals['gioco'], join_style='mitre', mitre_limit=10)


def recess(vals):
    return unary_union([set_precision(hexagon(h, vals), 1e-9) for h in CELLE_SPAZI])


def paper_pocket(q, vals):
    """tasca per la carta della base (mappa_base.pdf: mappa + fascia_carta, gli spazi ritagliati sul contorno d'ottone,
    cioè sul contorno ideale): rettangolo della carta + gioco_carta, meno l'alloggio dei fiori, nella parte q."""
    x0, y0 = xy((FRAME_U['O'], FRAME_U['S']), vals)
    x1, y1 = xy((FRAME_U['E'], FRAME_U['N']), vals)
    f = vals['fascia_carta'] + vals['gioco_carta']
    return quarter_shape(q, vals).intersection(box(x0 - f, y0 - f, x1 + f, y1 + f)).difference(recess(vals))


def flower_ideal(vals):
    return unary_union([set_precision(hexagon(h, vals), 1e-9) for h in SPAZIO_CELLE[1]])


def flower_local(vals, d):
    """fiore centrato nell'origine, contorno spostato di d verso l'interno."""
    cx, cy = xy(centre_u(M.SPAZI[1]), vals)
    g = affinity.translate(flower_ideal(vals), -cx, -cy)
    return g.buffer(-d, join_style='mitre', mitre_limit=10)


# ---- solidcraft-cli ---------------------------------------------------------------------------------------------
def run_sc(cmds, tmp, name, extra=()):
    sp = os.path.join(tmp, name + '.json')
    with open(sp, 'w') as f:
        json.dump({'commands': cmds}, f)
    jo = os.path.join(tmp, name + '.out.json')
    r = subprocess.run(['solidcraft-cli', 'run', sp, '--results', '--quiet', '--json-out', jo, *extra],
                       capture_output=True, text=True, timeout=3600)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f'SolidCraft: errore in {name}')
    with open(jo) as f:
        return json.load(f)


def snapshot(design, png, view='iso', w=1000, h=800, extra=()):
    """view: nome della vista (iso, top, front...) o dict della camera ({target, yaw, pitch, distance})."""
    vista = ['--camera', json.dumps(view)] if isinstance(view, dict) else ['--view', view]
    r = subprocess.run(['solidcraft-cli', 'snapshot', design, '--out', png, *vista, '--width', str(w), '--height', str(h),
                        '--no-grid', '--no-axes', *extra], capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit(f'snapshot fallito: {png}')


def measures(results):
    return [r for r in results if isinstance(r, dict) and 'body_count' in r and 'total' in r]


def body_of(meas, name):
    return next(b for b in meas['bodies'] if b['name'] == name)


def warnings(results):
    return [{'feature': r.get('name'), 'warning': r.get('warning')} for r in results
            if isinstance(r, dict) and 'feature' in r and r.get('warning')]


def text_metrics(tmp, strings):
    """estensione orizzontale di ogni scritta (in altezze) nel carattere di SolidCraft."""
    cmds = [{'command': 'sketch.create', 'params': {'plane': 'XY'}}]
    for s in strings:
        cmds.append({'command': 'sketch.text', 'params': {'text': s, 'at': [0, 0], 'height': 10}})
    cmds.append({'command': 'sketch.inspect', 'params': {}})
    out = run_sc(cmds, tmp, 'metriche_testo')
    curves = {c['id']: c for c in out[-1]['curves']}
    res = {}
    for s, r in zip(strings, out[1:-1]):
        xs = [p[0] for cid in r['created']['curves'] for p in (curves[cid].get('start_at'), curves[cid].get('end_at')) if p]
        res[s] = ((min(xs) + max(xs)) / 20, (max(xs) - min(xs)) / 10)    # centro e larghezza, in altezze
    return res


def sketch_poly(pts):
    return {'command': 'sketch.line', 'params': {'points': [p.expr() for p in pts], 'closed': True}}


def params_cmds():
    return [{'command': 'parameters.add', 'params': {'name': n, 'expression': f'{v} mm', 'comment': c}} for n, v, c in PARAMETRI]


# ---- controlli indipendenti dei file ----------------------------------------------------------------------------
def read_stl(path):
    data = open(path, 'rb').read()
    n = int.from_bytes(data[80:84], 'little')
    a = np.frombuffer(data, dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n, offset=84)
    return a['v'].astype(np.float64)


def mesh_stats(tri):
    pts = np.round(tri.reshape(-1, 3), 4)
    _, idx = np.unique(pts, axis=0, return_inverse=True)
    f = idx.reshape(-1, 3)
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    _, cnt = np.unique(np.sort(e, axis=1), axis=0, return_counts=True)
    v = np.einsum('ij,ij->i', tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6
    return {'triangoli': len(tri), 'bordi_non_manifold': int((cnt != 2).sum()), 'volume_mm3': round(float(v), 2),
            'ingombro_mm': [round(float(x), 3) for x in (tri.reshape(-1, 3).max(0) - tri.reshape(-1, 3).min(0))]}


def check_3mf(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.model'))))
    ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    objs = [o for o in root.findall('.//m:object', ns) if o.find('m:mesh', ns) is not None]
    return {'unita': root.get('unit', 'millimeter'), 'oggetti_mesh': len(objs),
            'triangoli': sum(len(o.findall('.//m:triangle', ns)) for o in objs)}


def check_files(nome, atteso_mm3):
    s = mesh_stats(read_stl(os.path.join(OUT, nome + '.stl')))
    s['3mf'] = check_3mf(os.path.join(OUT, nome + '.3mf'))
    ok = (s['bordi_non_manifold'] == 0 and s['3mf']['unita'] == 'millimeter' and s['3mf']['oggetti_mesh'] == 1
          and abs(s['volume_mm3'] - atteso_mm3) / atteso_mm3 < 2e-3)
    return s, ok


# ---- fiore -------------------------------------------------------------------------------------------------------
class Fiore:
    nome = 'fiore'

    def __init__(self):
        self.contorno = linearize(lambda v: flower_local(v, v['gioco_fiore']), ['passo', 'gioco_fiore'])[0]
        self.tasca = linearize(lambda v: flower_local(v, v['gioco_fiore'] + v['bordino']), ['passo', 'gioco_fiore', 'bordino'])[0]

    def expected(self):
        F = flower_local(P, P['gioco_fiore'])
        T = flower_local(P, P['gioco_fiore'] + P['bordino'])
        H = P['fiore_spessore']
        vol = chamfered_volume(F, P['smusso'], H) - T.area * P['tasca_prof']
        b = F.bounds
        return vol, [round(b[2] - b[0], 4), round(b[3] - b[1], 4), H]

    def commands(self, body='fiore'):
        F = flower_local(P, P['gioco_fiore'])
        H = P['fiore_spessore']
        cs = list(F.exterior.coords)
        mids = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(cs, cs[1:])]
        return [
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Contorno'}}, sketch_poly(self.contorno),
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'fiore_spessore', 'operation': 'new', 'name': 'Fiore', 'body_name': body}},
            {'command': 'solid.chamfer', 'params': {'edges': [[x, y, z] for z in (0.0, H) for x, y in mids], 'distance': 'smusso',
                                                    'tangent_chain': False, 'body': body, 'name': 'Smussi'}},
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'fiore_spessore', 'name': 'Tasca sopra'}}, sketch_poly(self.tasca),
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'direction': 'negative', 'operation': 'cut',
                                                    'name': 'Tasca sopra', 'targets': [body]}},
        ]


    def carta(self):
        taglio = flower_local(P, P['gioco_fiore'] + P['bordino'] + P['gioco_carta'])
        return {'tasche': 'solo sopra, fondo piatto', 'pdf': 'carta_fiori_3d.pdf',
                'taglio_dentro_il_contorno_ideale_mm': round(P['gioco_fiore'] + P['bordino'] + P['gioco_carta'], 3),
                'ingombro_carta_mm': [round(taglio.bounds[2] - taglio.bounds[0], 2), round(taglio.bounds[3] - taglio.bounds[1], 2)]}


def chamfered_volume(F, c, H):
    """prisma di pianta F e altezza H con smusso c sugli spigoli sopra e sotto (area(d) quadratica: Simpson esatto)."""
    a = [F.buffer(-d, join_style='mitre', mitre_limit=10, quad_segs=1024).area for d in (c, c / 2, 0)]
    return F.area * (H - 2 * c) + 2 * c * (a[0] + 4 * a[1] + a[2]) / 6


def ev(e, vals=None):
    """valore in mm di un'espressione dei parametri (la stessa stringa che va nel documento SolidCraft)."""
    return eval(e, {'__builtins__': {}}, dict(vals or P))


def disco(r, x=0.0, y=0.0):
    return Point(x, y).buffer(r, quad_segs=2048)


def rett_tondo(l, a, r):
    """rettangolo l × a centrato nell'origine con gli angoli di raggio r."""
    return box(-l / 2 + r, -a / 2 + r, l / 2 - r, a / 2 - r).buffer(r, quad_segs=2048) if r > 0 else box(-l / 2, -a / 2, l / 2, a / 2)


def copie_csv(nome):
    return sum(int(r['copie']) for r in csv.DictReader(open(os.path.join(DATI, nome), encoding='utf-8')))


class Piatto:
    """pezzo piatto col contorno ESATTO del pezzo di carta del kit (fondo piatto, smusso sopra e sotto): bordino in rilievo
    e tasca sopra per l'adesivo di segnalini_3d.pdf. Tasca = contorno - bordino; adesivo = tasca - gioco_carta. Le
    sottoclassi danno il contorno (schizzo e shapely, spostato di d verso l'interno), i punti degli spigoli da smussare,
    l'eventuale mozzo pieno al centro e i fori passanti."""
    spessore = 'segnalino_spessore'
    spess_min = 1.2           # pieno minimo sotto la tasca
    facce_giu = 1             # facce rivolte in giù: solo il fondo
    mozzo = None              # raggio (espressione) del mozzo pieno, alto quanto il pezzo

    def fori(self):
        """fori passanti: [(comandi dello schizzo, poligono shapely)]."""
        return []

    def commands(self, body=None):
        body = body or self.nome
        H = ev(self.spessore)
        c = [{'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Contorno'}}, *self.schizzo('0*bordino'),
             {'command': 'sketch.finish', 'params': {}},
             {'command': 'solid.extrude', 'params': {'distance': self.spessore, 'operation': 'new', 'name': 'Pezzo', 'body_name': body}},
             {'command': 'solid.chamfer', 'params': {'edges': self.spigoli(H), 'distance': 'smusso', 'body': body, 'name': 'Smussi'}},
             {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': self.spessore, 'name': 'Tasca'}}, *self.schizzo('bordino'),
             {'command': 'sketch.finish', 'params': {}},
             {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'direction': 'negative', 'operation': 'cut', 'name': 'Tasca',
                                                     'targets': [body]}}]
        if self.mozzo:
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': f'{self.spessore} - tasca_prof', 'name': 'Mozzo'}},
                  {'command': 'sketch.circle.center', 'params': {'center': ['0*mozzo_r', '0*mozzo_r'], 'radius': self.mozzo}},
                  {'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'operation': 'join', 'name': 'Mozzo', 'targets': [body]}}]
        for k, (sk, _) in enumerate(self.fori()):
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': self.spessore, 'name': f'Foro {k + 1}'}}, *sk,
                  {'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.extrude', 'params': {'distance': self.spessore, 'direction': 'negative', 'operation': 'cut',
                                                          'name': f'Foro {k + 1}', 'targets': [body]}}]
        return c

    def tasca(self):
        t = self.forma(P['bordino'])
        return t.difference(disco(ev(self.mozzo))) if self.mozzo else t

    def adesivo(self):
        """sagoma dell'adesivo (taglio di segnalini_3d.pdf), y in su, origine al centro del pezzo."""
        a = self.forma(P['bordino'] + P['gioco_carta'])
        return a.difference(disco(ev(self.mozzo) + P['gioco_carta'])) if self.mozzo else a

    def expected(self):
        H, d = ev(self.spessore), P['tasca_prof']
        F, T = self.forma(0.0), self.tasca()
        vol = chamfered_volume(F, P['smusso'], H) - T.area * d
        for _, g in self.fori():
            vol -= g.intersection(T).area * (H - d) + g.difference(T).area * H
        b = F.bounds
        return vol, [round(b[2] - b[0], 4), round(b[3] - b[1], 4), H]

    def carta(self):
        ba, bt = self.adesivo().bounds, self.tasca().bounds
        return {'tasca': 'sopra', 'pdf': 'segnalini_3d.pdf', 'contorno_come_la_carta_mm': self.misura_carta(),
                'tasca_mm': [round(bt[2] - bt[0], 3), round(bt[3] - bt[1], 3)], 'adesivo_mm': [round(ba[2] - ba[0], 3), round(ba[3] - ba[1], 3)],
                'gioco_adesivo_tasca_mm': round(((bt[2] - bt[0]) - (ba[2] - ba[0])) / 2, 3)}


class Tondo(Piatto):
    """disco di diametro `dpar` (Tessere Esplorazione Ø 24, segnalini Ø 20)."""

    def __init__(self, nome, dpar):
        self.nome, self.dpar = nome, dpar

    def schizzo(self, d):
        return [{'command': 'sketch.circle.center', 'params': {'center': [f'0*{self.dpar}', f'0*{self.dpar}'], 'radius': f'{self.dpar}/2 - {d}'}}]

    def forma(self, d):
        return disco(P[self.dpar] / 2 - d)

    def spigoli(self, H):
        R = P[self.dpar] / 2
        return [[R, 0, 0], [R, 0, H]]

    def misura_carta(self):
        return [P[self.dpar]] * 2


class Stato(Piatto):
    """tessera Stato 26 × 18 con gli angoli da 1,2: rettangolare come la carta, così si vede se è verticale o orizzontale."""
    nome = 'tessera_stato'

    def schizzo(self, d):
        return [{'command': 'sketch.rectangle.rounded', 'params': {'p0': [f'-stato_l/2 + {d}', f'-stato_a/2 + {d}'],
                                                                   'p1': [f'stato_l/2 - {d}', f'stato_a/2 - {d}'], 'radius': f'stato_r - {d}'}}]

    def forma(self, d):
        return rett_tondo(P['stato_l'] - 2 * d, P['stato_a'] - 2 * d, P['stato_r'] - d)

    def spigoli(self, H):
        return [[0, -P['stato_a'] / 2, 0], [0, -P['stato_a'] / 2, H]]

    def misura_carta(self):
        return [P['stato_l'], P['stato_a']]


class Rotella(Tondo):
    """disco Ø 52 della rotella: finestra passante a corona_r dal centro (in alto, +y), larga e alta come quella del disco
    di carta + gioco_carta per lato (l'adesivo, intagliato sulla finestra di carta, copre il bordo della plastica); mozzo
    pieno al centro col foro del perno. L'adesivo è una corona con l'intaglio della finestra aperto verso il bordo."""
    spessore = 'rotella_spessore'
    mozzo = 'mozzo_r'

    def __init__(self, finestra):
        self.ww, self.wh = finestra
        self.nome, self.dpar = f'rotella_finestra_{finestra[0]:g}x{finestra[1]:g}', 'rotella_d'

    def fori(self):
        ww, wh = f'{self.ww:g}/2 + gioco_carta', f'{self.wh:g}/2 + gioco_carta'
        fin = box(-ev(ww), P['corona_r'] - ev(wh), ev(ww), P['corona_r'] + ev(wh))
        return [([{'command': 'sketch.circle.center', 'params': {'center': ['0*foro_perno', '0*foro_perno'], 'radius': 'foro_perno/2'}}],
                 disco(P['foro_perno'] / 2)),
                ([{'command': 'sketch.rectangle.two_point', 'params': {'p0': [f'-({ww})', f'corona_r - ({wh})'], 'p1': [ww, f'corona_r + {wh}']}}], fin)]

    def adesivo(self):
        a = super().adesivo()
        ww, wh = self.ww / 2, self.wh / 2
        return a.difference(box(-ww, P['corona_r'] - wh, ww, P['rotella_d']))

    def carta(self):
        c = super().carta()
        c.update({'finestra_carta_mm': [self.ww, self.wh], 'finestra_plastica_mm': [self.ww + 2 * P['gioco_carta'], self.wh + 2 * P['gioco_carta']],
                  'foro_adesivo_mm': round(2 * (P['mozzo_r'] + P['gioco_carta']), 3), 'foro_perno_mm': P['foro_perno']})
        return c


# rotelle (gen.py: ROTELLE, R_TAVOLO, profezia_disco): oggetto del 3MF, finestra del disco di carta (larga, alta), copie
PLANCE = 4
ROTELLE_3D = [('rotella_PV', (11, 9), PLANCE), ('rotella_Danni', (9, 9), PLANCE), ('rotella_ATT', (11, 9), PLANCE),
              ('rotella_MOV', (11, 9), PLANCE), ('rotella_AR', (11, 9), PLANCE), ('rotella_PL', (9, 9), PLANCE),
              ('rotella_scontro', (11, 9), 1), ('rotella_custode', (11, 9), 1), ('rotella_Profezia', (10, 9), 1)]


def quote_perno():
    """quote (espressioni, z in su dal piano di stampa = sotto della testa) del perno, montato con la testa sotto la plancia."""
    zh = 'testa_h + carta_plancia + rotella_spessore'           # sopra del mozzo della rotella: lì appoggia il fermo
    zn = f'{zh} - 0.2'                                          # inizio della gola (0,2 sotto: margine per la carta più sottile)
    zl = f'{zh} + fermo_h + gioco_assiale'                      # dente: le ganasce si chiudono sotto di lui
    zb = f'{zl} + 0.4'
    zt = f'{zb} + 0.7'                                          # punta a cono a 45°: apre le ganasce
    return {'mozzo': zh, 'gola': zn, 'dente': zl, 'dente_alto': zb, 'punta': zt}


class Perno:
    """perno della rotella, stampato in piedi sulla testa: testa Ø testa_d sotto la plancia, fusto Ø perno_d nel foro di
    plancia e rotella, gola Ø collo_d dove si chiude il fermo, dente e punta a cono. Unico sbalzo: il dente, (perno_d -
    collo_d)/2 = 0,25 mm in orizzontale."""
    nome = 'perno'
    spess_min = 0.8
    facce_giu = 2             # fondo e sotto del dente (sbalzo di 0,25 mm)

    def profilo(self):
        q = quote_perno()
        return [('0*perno_d', '0*perno_d'), ('testa_d/2', '0*perno_d'), ('testa_d/2', 'testa_h - 0.3'), ('testa_d/2 - 0.3', 'testa_h'),
                ('perno_d/2 + 0.3', 'testa_h'), ('perno_d/2', 'testa_h + 0.3'), ('perno_d/2', f'{q["gola"]} - (perno_d - collo_d)/2'),
                ('collo_d/2', q['gola']), ('collo_d/2', q['dente']), ('perno_d/2', q['dente']), ('perno_d/2', q['dente_alto']),
                ('perno_d/2 - 0.7', q['punta']), ('0*perno_d', q['punta'])]

    def commands(self, body=None):
        body = body or self.nome
        return [{'command': 'sketch.create', 'params': {'plane': 'XZ', 'name': 'Profilo'}},     # schizzo XZ: y = -Z
                {'command': 'sketch.line', 'params': {'points': [[r, f'-({z})'] for r, z in self.profilo()], 'closed': True}},
                {'command': 'sketch.finish', 'params': {}},
                {'command': 'solid.revolve', 'params': {'axis': 'Z', 'operation': 'new', 'name': 'Perno', 'body_name': body}}]

    def expected(self):
        p = Polygon([(ev(r), ev(z)) for r, z in self.profilo()])
        vol = 2 * math.pi * p.area * p.centroid.x             # Pappo
        R = P['testa_d'] / 2
        return vol, [2 * R, 2 * R, round(p.bounds[3], 4)]

    def carta(self):
        q = {k: round(ev(v), 3) for k, v in quote_perno().items()}
        return {'quote_z_mm': q, 'gioco_radiale_nel_foro_mm': round((P['foro_perno'] - P['perno_d']) / 2, 3),
                'foro_plancia_mm': 4.0, 'interferenza_ganasce_mm': round(P['perno_d'] / 2 - (P['collo_d'] / 2 + 0.05), 3)}


# fermo: ganasce a sbalzo parallele all'asse y (radice a y = FERMO_Y0, punta a FERMO_Y1), sede tonda per la gola al centro
FERMO_Y0, FERMO_Y1, FERMO_FESSURA = -4.2, 2.0, 0.7


class Fermo:
    """fermo del perno, piatto (si stampa su una faccia qualsiasi): disco Ø fermo_d con 2 ganasce a sbalzo che si aprono
    nel piano quando la punta del perno ci passa in mezzo e si richiudono nella gola. Fessure da FERMO_FESSURA mm."""
    nome = 'fermo'
    spess_min = 1.2
    facce_giu = 1

    def tagli(self):
        """[(comandi dello schizzo, poligono)]: sede, fessura centrale, 2 fessure esterne, fessura in punta."""
        s, y0, y1 = FERMO_FESSURA, FERMO_Y0, FERMO_Y1
        xi, xe = 'perno_d/2 - 0.5', 'perno_d/2 + 0.5'           # bordo interno della ganascia e bordo esterno (radice larga 1)
        xf = f'{xe} + {s}'

        def rect(xa, ya, xb, yb):
            return ([{'command': 'sketch.rectangle.two_point', 'params': {'p0': [xa, ya], 'p1': [xb, yb]}}],
                    box(ev(xa), ev(ya), ev(xb), ev(yb)))
        yy0, yy1, yt = f'{y0} + 0*perno_d', f'{y1 + s} + 0*perno_d', f'{y1} + 0*perno_d'
        return [([{'command': 'sketch.circle.center', 'params': {'center': ['0*collo_d', '0*collo_d'], 'radius': 'collo_d/2 + 0.05'}}],
                 disco(P['collo_d'] / 2 + 0.05)),
                rect(f'-({xi})', yy0, xi, yy1), rect(xe, yy0, xf, yy1), rect(f'-({xf})', yy0, f'-({xe})', yy1), rect(f'-({xf})', yt, xf, yy1)]

    def commands(self, body=None):
        body = body or self.nome
        c = [{'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Disco'}},
             {'command': 'sketch.circle.center', 'params': {'center': ['0*fermo_d', '0*fermo_d'], 'radius': 'fermo_d/2'}},
             {'command': 'sketch.finish', 'params': {}},
             {'command': 'solid.extrude', 'params': {'distance': 'fermo_h', 'operation': 'new', 'name': 'Fermo', 'body_name': body}}]
        for k, (sk, _) in enumerate(self.tagli()):
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'fermo_h', 'name': f'Taglio {k + 1}'}}, *sk,
                  {'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.extrude', 'params': {'distance': 'fermo_h', 'direction': 'negative', 'operation': 'cut',
                                                          'name': f'Taglio {k + 1}', 'targets': [body]}}]
        return c

    def forma(self):
        return disco(P['fermo_d'] / 2).difference(unary_union([g for _, g in self.tagli()]))

    def expected(self):
        return self.forma().area * P['fermo_h'], [P['fermo_d'], P['fermo_d'], P['fermo_h']]

    def carta(self):
        L = -FERMO_Y0                                          # sbalzo dalla radice alla gola
        w = 1.0                                                # larghezza della ganascia alla radice
        d = P['perno_d'] / 2 - (P['collo_d'] / 2 + 0.05)       # quanto si apre ogni ganascia al passaggio del dente
        return {'ganasce': 2, 'sbalzo_mm': L, 'larghezza_radice_mm': w, 'apertura_per_ganascia_mm': round(d, 3),
                'deformazione_alla_radice_pct': round(150 * d * w / L ** 2, 2), 'fessure_mm': FERMO_FESSURA,
                'gioco_gola_sede_mm': 0.05}


def hex_local(vals, apotema):
    r = apotema / math.cos(math.radians(30))
    return Polygon([(r * math.cos(math.radians(90 + 60 * k)), r * math.sin(math.radians(90 + 60 * k))) for k in range(6)])


class Cripta:
    """segnalino Cripta: esagono con la tasca sopra per la carta esagonale da passo (mappa_fiori.pdf, foglio 3). Sporge
    di gioco_carta + bordino oltre l'esagono della mappa: è un segnalino che si appoggia sopra."""
    nome = 'segnalino_cripta'

    def __init__(self):
        self.contorno = linearize(lambda v: hex_local(v, v['passo'] / 2 + v['gioco_carta'] + v['bordino']), ['passo', 'gioco_carta', 'bordino'])[0]
        self.tasca = linearize(lambda v: hex_local(v, v['passo'] / 2 + v['gioco_carta']), ['passo', 'gioco_carta'])[0]

    def expected(self):
        F = hex_local(P, P['passo'] / 2 + P['gioco_carta'] + P['bordino'])
        T = hex_local(P, P['passo'] / 2 + P['gioco_carta'])
        H = P['segnalino_spessore']
        b = F.bounds
        return chamfered_volume(F, P['smusso'], H) - T.area * P['tasca_prof'], [round(b[2] - b[0], 4), round(b[3] - b[1], 4), H]

    def commands(self, body=None):
        body = body or self.nome
        H = P['segnalino_spessore']
        cs = list(hex_local(P, P['passo'] / 2 + P['gioco_carta'] + P['bordino']).exterior.coords)
        mids = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(cs, cs[1:])]
        return [
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Esagono'}}, sketch_poly(self.contorno),
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'segnalino_spessore', 'operation': 'new', 'name': 'Esagono', 'body_name': body}},
            {'command': 'solid.chamfer', 'params': {'edges': [[x, y, z] for z in (0.0, H) for x, y in mids], 'distance': 'smusso',
                                                    'tangent_chain': False, 'body': body, 'name': 'Smussi'}},
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'segnalino_spessore', 'name': 'Tasca'}}, sketch_poly(self.tasca),
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'direction': 'negative', 'operation': 'cut', 'name': 'Tasca',
                                                    'targets': [body]}},
        ]

    def carta(self):
        return {'tasca': 'sopra', 'pdf': 'mappa_fiori.pdf (foglio 3)', 'carta_da_lato_a_lato_mm': P['passo'],
                'tasca_da_lato_a_lato_mm': round(P['passo'] + 2 * P['gioco_carta'], 3)}


# ---- vassoio -----------------------------------------------------------------------------------------------------
def seam_edges(q):
    """lati del reticolo tra un esagono della parte q e uno di un'altra parte: (a, b) a passo 1 con la parte q a
    sinistra, e la parte vicina."""
    out = []
    for h in CELLE_Q[q]:
        for nb in M.vicini(h):
            q2 = quarter_of(nb)
            if q2 == q:
                continue
            (x1, y1), (x2, y2) = centre_u(h), centre_u(nb)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ux, uy = (x2 - x1), (y2 - y1)          # verso il vicino, lungo 1
            tx, ty = -uy, ux                        # tangente con h a sinistra
            a = (mx - tx * RU / 2, my - ty * RU / 2)
            b = (mx + tx * RU / 2, my + ty * RU / 2)
            out.append((a, b, q2))
    return out


class Quarto:
    def __init__(self, q, metr):
        self.q, self.nome = q, f'vassoio_{q}'
        self.contorno = linearize(lambda v: quarter_shape(q, v), ['passo', 'margine', 'gioco'])[0]
        self.alloggio = linearize(recess, ['passo'])
        self.tasche = linearize(lambda v: paper_pocket(q, v), ['passo', 'margine', 'gioco', 'fascia_carta', 'gioco_carta'])
        self.code, self.incavi, self.vicini = [], [], {}
        hw_c, hw_i = L('coda_collo', .5) - L('gioco'), L('coda_collo', .5) + L('gioco')
        depth = L('coda_lunga') - L('coda_testa', .5)
        for a, b, q2 in seam_edges(q):
            a, b = np.array(a) - C0, np.array(b) - C0
            t = (b - a) / np.linalg.norm(b - a)
            n = np.array([t[1], -t[0]])                    # verso la parte vicina
            Mid = V2(L('passo', (a[0] + b[0]) / 2), L('passo', (a[1] + b[1]) / 2))
            self.vicini[q2] = self.vicini.get(q2, 0) + 1
            if QUARTI.index(q) < QUARTI.index(q2):         # coda sulla parte posata prima
                p_in, p_out = Mid + vdir(n, Lin({'': -DENTRO})), Mid + vdir(n, depth)
                self.code.append({'rect': [p_in + vdir(t, hw_c * -1), p_out + vdir(t, hw_c * -1), p_out + vdir(t, hw_c), p_in + vdir(t, hw_c)],
                                  'centro': p_out, 'raggio': L('coda_testa', .5) - L('gioco')})
            else:
                q_out, q_in = Mid + vdir(n, Lin({'': DENTRO})), Mid + vdir(n, depth * -1)
                self.incavi.append({'rect': [q_out + vdir(t, hw_i * -1), q_in + vdir(t, hw_i * -1), q_in + vdir(t, hw_i), q_out + vdir(t, hw_i)],
                                    'centro': q_in, 'raggio': L('coda_testa', .5) + L('gioco')})
        self.testi_fondo = self.texts(metr)

    def texts(self, metr):
        """sul fondo dell'alloggio: numero dello spazio e cifre 1-6 dell'anello (come sulla carta della base, che lì
        viene ritagliata), solo quelli che cadono in questa parte. Le coordinate stanno sulla carta della base."""
        Q = quarter_shape(self.q, P)
        fondo = []

        def add(s, pu, hname):
            c, w = metr[s]
            cx, cy = (pu[0] - C0[0]) * P['passo'], (pu[1] - C0[1]) * P['passo']
            hgt = P[hname]
            bb = box(cx - w * hgt / 2, cy - hgt / 2, cx + w * hgt / 2, cy + hgt / 2)
            if Q.contains(Point(cx, cy)):
                assert Q.buffer(-0.5).contains(bb), f'la scritta {s} cade sul taglio tra due parti'
                fondo.append({'text': s, 'at': V2(L('passo', pu[0] - C0[0]) - L(hname, c), L('passo', pu[1] - C0[1]) - L(hname, 0.5)),
                              'height': hname})

        for s in M.SPAZI:
            add(str(s), centre_u(M.SPAZI[s]), 'numero_alto')
            for k in range(6):
                add(str(k + 1), centre_u(M.anello(s, k)), 'cifra_alta')
        return fondo

    def H(self):
        return P['fondo'] + P['alloggio_prof']

    def knob_shapes(self, ks):
        return [Polygon([p.val() for p in k['rect']]).union(Point(k['centro'].val()).buffer(k['raggio'].val(), quad_segs=256)) for k in ks]

    def corner(self):
        """angolo esterno della parte (sulla fascia) e area tolta dal raccordo."""
        Q = quarter_shape(self.q, P)
        x = Q.bounds[0] if 'O' in self.q else Q.bounds[2]
        y = Q.bounds[3] if 'N' in self.q else Q.bounds[1]
        r = P['raggio_angolo']
        sx, sy = (1 if 'O' in self.q else -1), (-1 if 'N' in self.q else 1)
        cut = box(min(x, x + sx * r), min(y, y + sy * r), max(x, x + sx * r), max(y, y + sy * r)).difference(
            Point(x + sx * r, y + sy * r).buffer(r, quad_segs=256))
        return (x, y), cut

    def expected(self):
        Q = quarter_shape(self.q, P)
        _, cut = self.corner()
        Q = Q.difference(cut)
        tabs, slots = unary_union(self.knob_shapes(self.code)), unary_union(self.knob_shapes(self.incavi))
        R, T = recess(P), unary_union([paper_pocket(self.q, P)])
        f, H = P['fondo'], self.H()
        zs = sorted({0.0, f, f + GIOCO_Z, H - P['tasca_prof'], H})
        vol = 0.0
        for z0, z1 in zip(zs, zs[1:]):
            zm = (z0 + z1) / 2
            g = Q.union(tabs) if zm < f else Q
            if zm < f + GIOCO_Z:
                g = g.difference(slots)
            if zm > f:
                g = g.difference(R)
            if zm > H - P['tasca_prof']:
                g = g.difference(T)
            vol += g.area * (z1 - z0)
        b = Q.union(tabs).bounds
        assert tabs.intersection(slots).area < 1e-9
        return vol, [round(b[2] - b[0], 4), round(b[3] - b[1], 4), round(H, 4)]

    def commands(self, solo_solido=False):
        body = self.nome

        def knobs(ks):
            out = []
            for k in ks:
                out.append(sketch_poly(k['rect']))
                out.append({'command': 'sketch.circle.center', 'params': {'center': k['centro'].expr(), 'radius': k['raggio'].expr()}})
            return out

        (cx, cy), _ = self.corner()
        c = [{'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Contorno'}}, sketch_poly(self.contorno),
             {'command': 'sketch.finish', 'params': {}},
             {'command': 'solid.extrude', 'params': {'distance': 'fondo + alloggio_prof', 'operation': 'new', 'name': 'Vassoio', 'body_name': body}},
             {'command': 'solid.fillet', 'params': {'edges': [[cx, cy, self.H() / 2]], 'radius': 'raggio_angolo', 'body': body, 'name': 'Angolo'}}]
        if self.code:
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Code'}}] + knobs(self.code) + \
                 [{'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.extrude', 'params': {'distance': 'fondo', 'operation': 'join', 'name': 'Code', 'targets': [body]}}]
        if self.incavi:
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Incavi'}}] + knobs(self.incavi) + \
                 [{'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.extrude', 'params': {'distance': f'fondo + {GIOCO_Z}', 'operation': 'cut', 'name': 'Incavi', 'targets': [body]}}]
        c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'fondo + alloggio_prof', 'name': 'Alloggio fiori'}}] + \
             [sketch_poly(r) for r in self.alloggio] + [{'command': 'sketch.finish', 'params': {}},
                                                         {'command': 'solid.extrude', 'params': {'distance': 'alloggio_prof', 'direction': 'negative',
                                                                                                 'operation': 'cut', 'name': 'Alloggio fiori', 'targets': [body]}}]
        c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'fondo + alloggio_prof', 'name': 'Tasche carta'}}] + \
             [sketch_poly(r) for r in self.tasche] + [{'command': 'sketch.finish', 'params': {}},
                                                       {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'direction': 'negative',
                                                                                               'operation': 'cut', 'name': 'Tasche carta', 'targets': [body]}}]
        if solo_solido:
            return c
        c += [{'command': 'inspect.measure', 'params': {'bodies': [body]}}]
        if self.testi_fondo:
            c += [{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'fondo', 'name': 'Numeri spazi'}}]
            c += [{'command': 'sketch.text', 'params': {'text': t['text'], 'at': t['at'].expr(), 'height': t['height']}} for t in self.testi_fondo]
            c += [{'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.emboss', 'params': {'sketch': 'Numeri spazi', 'depth': 'incisione', 'mode': 'deboss', 'targets': [body],
                                                         'name': 'Numeri spazi'}}]
        return c


# ---- prove -------------------------------------------------------------------------------------------------------
def lock_play(A, B, ux, uy):
    lo, hi = 0.0, 3.0
    for _ in range(30):
        m = (lo + hi) / 2
        if affinity.translate(B, m * ux, m * uy).intersection(A).area > 1e-7:
            hi = m
        else:
            lo = m
    return hi


def costruisci(pz, tmp):
    """costruisce un pezzo in SolidCraft (.solidcraft, STL, 3MF in out/) e lo confronta col calcolo. Ritorna (risultati, ok)."""
    vol, bb = pz.expected()
    sc = os.path.join(OUT, pz.nome + '.solidcraft')
    out = run_sc(params_cmds() + pz.commands() + [{'command': 'model.faces', 'params': {'body': pz.nome}},
                                                  {'command': 'inspect.measure', 'params': {}}], tmp, pz.nome,
                 ['--save', sc, '--out', os.path.join(OUT, pz.nome + '.stl'), '--out', os.path.join(OUT, pz.nome + '.3mf')])
    m = body_of(measures(out)[-1], pz.nome)
    files, fok = check_files(pz.nome, m['volume_mm3'])
    fc = out[-2]['faces']
    giu = [f for f in fc if f.get('plane_normal') and f['plane_normal'][2] < -0.999]
    # fondo piatto: una sola faccia verso il basso a z = 0 (il perno ha in più il sotto del dente, sbalzo di 0,25 mm)
    fondo_piatto = (len(giu) == getattr(pz, 'facce_giu', 1) and sum(abs(f['centroid'][2]) < 1e-6 for f in giu) == 1)
    spess = min(f['centroid'][2] for f in fc if f.get('plane_normal') and f['plane_normal'][2] > 0.999)   # fondo della tasca
    r = {'volume_atteso_mm3': round(vol, 3), 'volume_mm3': round(m['volume_mm3'], 3),
         'errore_volume_rel': abs(m['volume_mm3'] - vol) / vol, 'massa_pla_g': round(m['volume_mm3'] * 1.24e-3, 2),
         'ingombro_atteso_mm': bb, 'ingombro_mm': [round(m['bbox']['max'][i] - m['bbox']['min'][i], 4) for i in range(3)],
         'avvisi': warnings(out), 'file': files, 'carta': pz.carta(),
         'facce_verso_il_basso': len(giu), 'fondo_piatto': fondo_piatto, 'spessore_sotto_la_tasca_mm': round(spess, 4)}
    r['ok'] = bool(r['errore_volume_rel'] < 1e-4 and not r['avvisi'] and fok and fondo_piatto
                   and spess >= getattr(pz, 'spess_min', 1.2) - 1e-9 and abs(m['bbox']['min'][2]) < 1e-6
                   and all(abs(a - b) < 2e-3 for a, b in zip(bb, r['ingombro_mm'])))
    if isinstance(pz, Piatto):   # tasca misurata sull'STL: ingombro delle pareti verticali alte tasca_prof sotto la faccia di sopra
        tri = read_stl(os.path.join(OUT, pz.nome + '.stl'))
        c = (tri.reshape(-1, 3).max(0) + tri.reshape(-1, 3).min(0)) / 2
        H, d = tri[:, :, 2].max(), P['tasca_prof']
        nz = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nz = np.abs(nz[:, 2]) / np.linalg.norm(nz, axis=1)
        pareti = tri[(nz < 1e-3) & (tri[:, :, 2].min(1) > H - d - 1e-4)]     # pareti della tasca (e del mozzo, che sta dentro)
        w = pareti.reshape(-1, 3)[:, :2] - c[:2]
        t = [round(float(w[:, i].max() - w[:, i].min()), 4) for i in (0, 1)]
        a = pz.adesivo().bounds
        g = [round((t[0] - (a[2] - a[0])) / 2, 4), round((t[1] - (a[3] - a[1])) / 2, 4) if not isinstance(pz, Rotella) else None]
        r['carta'].update({'tasca_misurata_stl_mm': t, 'gioco_adesivo_tasca_misurato_mm': g})   # rotelle: in y c'è l'intaglio
        r['ok'] &= all(abs(x - P['gioco_carta']) <= 0.2 for x in g if x is not None)
    print('PEZZO', pz.nome, json.dumps({k: r[k] for k in r if k != 'file'}, ensure_ascii=False))
    snapshot(sc, os.path.join(OUT, pz.nome + '.png'), w=800, h=600)
    return r, r['ok']


def segnalini_3d():
    """i pezzi 3D dei segnalini del kit (D29): un pezzo per geometria; quantità e nomi nel 3MF da oggetti_3mf()."""
    return ([Tondo('tessera_esplorazione', 'tessera_d'), Tondo('segnalino_tondo', 'gettone_d'), Stato()]
            + [Rotella(f) for f in dict.fromkeys(f for _, f, _ in ROTELLE_3D)] + [Perno(), Fermo()])


def prova_perno(tmp):
    """montaggio perno + plancia (lastra da carta_plancia col foro Ø 4) + rotella + fermo: niente intersezioni, giochi
    misurati faccia contro faccia, presa del dente (il fermo alzato sul dente deve urtare le ganasce), sezione in PNG."""
    q = {k: ev(v) for k, v in quote_perno().items()}
    rot = Rotella((11, 9))
    cmds = params_cmds() + rot.commands('rotella') + Perno().commands('perno') + Fermo().commands('fermo') + [
        {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'testa_h', 'name': 'Plancia'}},
        {'command': 'sketch.rectangle.two_point', 'params': {'p0': ['-32 + 0*testa_h', '-32 + 0*testa_h'], 'p1': ['32 + 0*testa_h', '32 + 0*testa_h']}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 'carta_plancia', 'operation': 'new', 'name': 'Plancia', 'body_name': 'plancia'}},
        {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'testa_h + carta_plancia', 'name': 'Foro plancia'}},
        {'command': 'sketch.circle.center', 'params': {'center': ['0*testa_h', '0*testa_h'], 'radius': '2 + 0*testa_h'}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 'carta_plancia', 'direction': 'negative', 'operation': 'cut', 'name': 'Foro plancia',
                                                'targets': ['plancia']}},
        {'command': 'solid.move', 'params': {'bodies': ['rotella'], 'translate': [0, 0, 'testa_h + carta_plancia']}},
        {'command': 'solid.move', 'params': {'bodies': ['fermo'], 'translate': [0, 0, quote_perno()['mozzo']]}}]
    n_build = len(cmds)
    zr = P['testa_h'] + P['carta_plancia'] + P['rotella_spessore'] / 2

    def fc(body, p):
        return {'type': 'face', 'body': body, 'point': [float(c) for c in p]}
    misure = [('fusto-foro della rotella', fc('perno', (P['perno_d'] / 2, 0, zr)), fc('rotella', (P['foro_perno'] / 2, 0, zr)),
               (P['foro_perno'] - P['perno_d']) / 2, True),
              # nella plancia (z da testa_h a testa_h + carta_plancia) c'è il raccordo a 45° del fusto, da Ø 4,0 a 3,4: la
              # plancia (foro Ø 4) appoggia sulla testa centrata dal raccordo, quindi lì non c'è un gioco da misurare
              ('gola-sede del fermo', fc('perno', (P['collo_d'] / 2, 0, q['mozzo'] + P['fermo_h'] / 2)),
               fc('fermo', (P['collo_d'] / 2 + 0.05, 0, q['mozzo'] + P['fermo_h'] / 2)), 0.05, True),
              ('dente-fermo (gioco assiale)', fc('perno', (P['perno_d'] / 2 - 0.1, 0, q['dente'])),
               fc('fermo', (P['perno_d'] / 2 - 0.1, 0, q['mozzo'] + P['fermo_h'])), P['gioco_assiale'], False)]
    cmds += [{'command': 'inspect.interference', 'params': {'bodies': ['plancia', 'rotella', 'perno', 'fermo']}}]
    cmds += [{'command': 'inspect.measure', 'params': {'items': [a, b]}} for _, a, b, _, _ in misure]
    va = os.path.join(OUT, 'verifica_perno.solidcraft')
    out = run_sc(cmds, tmp, 'verifica_perno', ['--save', va])
    inter = [i for i in out[n_build]['interferences'] if i.get('volume_mm3', 0) > 1e-6]
    res = {'intersezioni': inter, 'giochi': {}}
    ok = not inter
    for (nome, _, _, att, cil), r in zip(misure, out[n_build + 1:]):
        d = r['distance_mm']
        if cil:   # tra cilindri coassiali contano raggi e assi (la distanza tra facce curve è misurata sulla mesh)
            i1, i2 = r['items']
            d = abs(i2['radius'] - i1['radius']) - math.dist(i1['center'][:2], i2['center'][:2])
        res['giochi'][nome] = {'atteso_mm': round(att, 3), 'misura_mm': round(d, 4)}
        ok &= abs(d - att) < 2e-3
    # presa: il fermo alzato di fermo_h + gioco_assiale + 0,2 mm sta all'altezza del dente: deve urtare le ganasce
    alza = P['fermo_h'] + P['gioco_assiale'] + 0.2
    out = run_sc([{'command': 'solid.move', 'params': {'bodies': ['fermo'], 'translate': [0, 0, alza]}},
                  {'command': 'inspect.interference', 'params': {'bodies': ['perno', 'fermo']}}], tmp, 'presa_perno', ['--in', va])
    v = sum(i.get('volume_mm3', 0) for i in out[-1]['interferences'])
    res['presa_dente_ganasce_mm3'] = round(v, 4)
    ok &= v > 1e-3
    res['quote_z_mm'] = {k: round(v_, 3) for k, v_ in q.items()}
    res['ok'] = bool(ok)
    colori = ['--body', 'rotella:color=#c89a50', '--body', 'plancia:color=#e8dcc0', '--body', 'perno:color=#3060a0', '--body', 'fermo:color=#a03030']
    snapshot(va, os.path.join(OUT, 'verifica_perno_sezione.png'), {'target': [0, 0, 3], 'yaw': math.pi, 'pitch': 0.25, 'distance': 24},
             1200, 800, ['--section', 'y=0', *colori])
    snapshot(va, os.path.join(OUT, 'verifica_perno.png'), {'target': [0, 0, 2], 'yaw': 0.6, 'pitch': 0.6, 'distance': 90}, 1200, 800, colori)
    print('PROVA perno', json.dumps(res, ensure_ascii=False))
    return res, ok


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='mappa3d-sc-')
    ris = {'parametri': P, 'gioco_carta_mm': P['gioco_carta'], 'piatto_ipotizzato_mm': PIATTO, 'pezzi': {}, 'prove': {}}
    ok = True
    try:
        # 1. segnalini del kit, rotelle e perni (D29)
        for pz in segnalini_3d():
            ris['pezzi'][pz.nome], k = costruisci(pz, tmp)
            ok &= k
        ris['prove']['perno'], k = prova_perno(tmp)
        ok &= k
        # 2. fiore e Cripta
        fi = Fiore()
        for pz in (fi, Cripta()):
            ris['pezzi'][pz.nome], k = costruisci(pz, tmp)
            ok &= k

        # carta delle facce dei fiori per la versione 3D (facce A e B separate, taglio dentro il contorno ideale)
        rientro = P['gioco_fiore'] + P['bordino'] + P['gioco_carta']
        ris['carta_fiori_3d'] = carta_fiori_3d.genera(os.path.join(OUT, 'carta_fiori_3d.pdf'), rientro, tmp)
        print('CARTA', json.dumps(ris['carta_fiori_3d'], ensure_ascii=False))

        # 2. le 4 parti del vassoio
        strings = [str(i) for i in range(1, len(M.SPAZI) + 1)]
        metr = text_metrics(tmp, strings)
        quarti = [Quarto(q, metr) for q in QUARTI]
        for qt in quarti:
            vol, bb = qt.expected()
            sc = os.path.join(OUT, qt.nome + '.solidcraft')
            out = run_sc(params_cmds() + qt.commands() + [{'command': 'inspect.measure', 'params': {}}], tmp, qt.nome,
                         ['--save', sc, '--out', os.path.join(OUT, qt.nome + '.stl'), '--out', os.path.join(OUT, qt.nome + '.3mf')])
            ms = measures(out)
            m0, m1 = body_of(ms[0], qt.nome), body_of(ms[-1], qt.nome)
            files, fok = check_files(qt.nome, m1['volume_mm3'])
            ing = [round(m1['bbox']['max'][i] - m1['bbox']['min'][i], 4) for i in range(3)]
            r = {'volume_atteso_senza_scritte_mm3': round(vol, 2), 'volume_senza_scritte_mm3': round(m0['volume_mm3'], 2),
                 'errore_volume_rel': abs(m0['volume_mm3'] - vol) / vol, 'volume_mm3': round(m1['volume_mm3'], 2),
                 'incisioni_mm3': round(m0['volume_mm3'] - m1['volume_mm3'], 2), 'massa_pla_g': round(m1['volume_mm3'] * 1.24e-3, 1),
                 'ingombro_atteso_mm': bb, 'ingombro_mm': ing, 'code': len(qt.code), 'incavi': len(qt.incavi),
                 'lati_in_comune': qt.vicini, 'scritte_fondo': len(qt.testi_fondo),
                 'avvisi': warnings(out), 'file': files, 'entra_nel_piatto': ing[0] <= PIATTO - 10 and ing[1] <= PIATTO - 10}
            r['ok'] = bool(r['errore_volume_rel'] < 1e-4 and not r['avvisi'] and fok and r['incisioni_mm3'] > 1 and r['entra_nel_piatto']
                           and all(abs(a - b) < 2e-3 for a, b in zip(bb, ing)))
            ok &= r['ok']
            ris['pezzi'][qt.nome] = r
            print('PEZZO', qt.nome, json.dumps({k: r[k] for k in r if k != 'file'}, ensure_ascii=False))
            snapshot(sc, os.path.join(OUT, qt.nome + '.png'))

        # 3. vassoio montato + 14 fiori negli spazi (girati di (s mod 6)·60°, voltati negli spazi dispari).
        #    Intersezioni: inspect.interference. Giochi: distanza tra le due facce affacciate (inspect.measure), lato per lato.
        cmds = params_cmds()
        for qt in quarti:
            cmds += qt.commands(solo_solido=True)
        cmds += fi.commands('Fiore')
        for s in M.SPAZI:
            x, y = xy(centre_u(M.SPAZI[s]), P)
            cmds += [{'command': 'solid.move', 'params': {'bodies': ['Fiore'], 'copy': True, 'axis': [0, 0, 1], 'angle': f'{60 * (s % 6)} deg'}}]
            if False:   # i fiori non si voltano più: fondo piatto
                cmds += [{'command': 'solid.move', 'params': {'bodies': ['Fiore (2)'], 'axis': [1, 0, 0], 'angle': '180 deg',
                                                              'translate': [0, 0, P['fiore_spessore']]}}]
            cmds += [{'command': 'solid.move', 'params': {'bodies': ['Fiore (2)'], 'translate': [x, y, P['fondo']]}},
                     {'command': 'body.rename', 'params': {'body': 'Fiore (2)', 'name': f'Fiore_S{s}'}}]
        cmds += [{'command': 'solid.move', 'params': {'bodies': ['Fiore'], 'translate': [0, 0, -50]}},   # il fiore di partenza, sotto
                 {'command': 'body.rename', 'params': {'body': 'Fiore', 'name': 'Fiore_sotto'}}]
        n_build = len(cmds)
        cmds += [{'command': 'inspect.interference', 'params': {'bodies': [qt.nome for qt in quarti] + [f'Fiore_S{s}' for s in M.SPAZI]}}]
        coppie = []      # (tipo, corpo a, punto a, corpo b, punto b, atteso)

        def face(body, p, z):
            return {'type': 'face', 'body': body, 'point': [float(p[0]), float(p[1]), float(z)]}

        for qt in quarti:     # tagli del vassoio: lato del taglio (lontano dalla coda) e pomello nel suo incavo
            for (a, b_, q2) in seam_edges(qt.q):
                if QUARTI.index(qt.q) > QUARTI.index(q2):
                    continue
                a, b_ = (np.array(a) - C0) * P['passo'], (np.array(b_) - C0) * P['passo']
                t = (b_ - a) / np.linalg.norm(b_ - a)
                n = np.array([t[1], -t[0]])
                mid = (a + b_) / 2
                zf = P['fondo'] / 2
                coppie.append(('taglio', qt.nome, mid + 5 * t - n * P['gioco'], f'vassoio_{q2}', mid + 5 * t + n * P['gioco'], zf, 2 * P['gioco']))
                c = mid + n * (P['coda_lunga'] - P['coda_testa'] / 2)
                coppie.append(('pomello', qt.nome, c + n * (P['coda_testa'] / 2 - P['gioco']), f'vassoio_{q2}',
                               c + n * (P['coda_testa'] / 2 + P['gioco']), zf, 2 * P['gioco']))   # cilindri: raggi e assi
        visti = set()
        for s in M.SPAZI:     # fiori: ogni lato del contorno contro la parete dell'alloggio o contro il fiore vicino
            for h in SPAZIO_CELLE[s]:
                q0, r0 = M.AX[h]
                for dq, dr in M.DIR:
                    nbax = (q0 + dq, r0 + dr)
                    nb = M.HX.get(nbax)
                    if nb in SPAZIO_CELLE[s]:
                        continue
                    (x1, y1) = xy(centre_u(h), P)
                    cx2, cy2 = centre_u(h)[0] + dq + dr / 2, centre_u(h)[1] - dr * S3 / 2
                    x2, y2 = xy((cx2, cy2), P)
                    mid = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
                    n = np.array([x2 - x1, y2 - y1]) / P['passo']
                    zf = P['fondo'] + P['fiore_spessore'] / 2
                    other = next((t2 for t2 in M.SPAZI if nb in SPAZIO_CELLE[t2]), None)
                    if other is not None:
                        key = frozenset((h, nb))
                        if key in visti:
                            continue
                        visti.add(key)
                        coppie.append(('fiore-fiore', f'Fiore_S{s}', mid - n * P['gioco_fiore'], f'Fiore_S{other}',
                                       mid + n * P['gioco_fiore'], zf, 2 * P['gioco_fiore']))
                    else:
                        qw = next(qt.q for qt in quarti if quarter_shape(qt.q, P).contains(Point(*(mid + n * 1.0))))
                        sul_taglio = qw != quarter_of(h)     # parete sul taglio tra due parti: arretrata di gioco
                        coppie.append(('fiore-alloggio sul taglio' if sul_taglio else 'fiore-alloggio', f'Fiore_S{s}',
                                       mid - n * P['gioco_fiore'], f'vassoio_{qw}', mid + n * (P['gioco'] if sul_taglio else 0),
                                       P['fondo'] + P['alloggio_prof'] / 2, P['gioco_fiore'] + (P['gioco'] if sul_taglio else 0)))
        for tipo, ba, pa, bb, pb, z, att in coppie:
            za = P['fondo'] + P['fiore_spessore'] / 2 if ba.startswith('Fiore') else z
            cmds.append({'command': 'inspect.measure', 'params': {'items': [face(ba, pa, za), face(bb, pb, z)]}})
        va = os.path.join(OUT, 'verifica_vassoio_fiori.solidcraft')
        out = run_sc(cmds, tmp, 'montaggio', ['--save', va])
        inter = out[n_build]['interferences']
        dist, fuori = {}, []
        for (tipo, ba, pa, bb, pb, z, att), r in zip(coppie, out[n_build + 1:]):
            d = r['distance_mm']
            if tipo == 'pomello':   # la distanza tra facce curve è misurata sulla mesh: per i cilindri valgono raggi e assi
                i1, i2 = r['items']
                d = i2['radius'] - i1['radius'] - math.dist(i1['center'][:2], i2['center'][:2])
            dist.setdefault(tipo, []).append(d)
            if abs(d - att) >= 2e-3:
                fuori.append({'tipo': tipo, 'a': ba, 'b': bb, 'punto_a': [round(float(c), 3) for c in pa], 'atteso_mm': att,
                              'misura_mm': round(d, 4), 'da': r.get('from'), 'a_punto': r.get('to'),
                              'facce': [i.get('round') or ('piana' if i.get('planar') else '?') for i in r.get('items', [])]})
        ok &= not fuori
        prova = {'intersezioni': inter, 'misure_lato_per_lato': {k: {'misure': len(v), 'min_mm': round(min(v), 4), 'max_mm': round(max(v), 4)}
                                                                for k, v in dist.items()},
                 'fuori_tolleranza': fuori, 'rotazioni_usate_gradi': sorted({60 * (s % 6) for s in M.SPAZI})}
        ris['prove']['montaggio'] = prova
        ok &= not inter and len(dist.get('fiore-fiore', [])) > 0 and len(dist.get('taglio', [])) > 0
        print('PROVA montaggio', json.dumps(prova, ensure_ascii=False))
        snapshot(va, os.path.join(OUT, 'verifica_vassoio_fiori.png'), 'iso', 1400, 1000)
        snapshot(va, os.path.join(OUT, 'verifica_vassoio_fiori_alto.png'), 'top', 1400, 1200)

        # 4. presa delle code: ogni coppia di parti vicine, la seconda tirata via di SPOSTA_PROVA mm, deve urtare
        presa = []
        for i, a in enumerate(quarti):
            for b in quarti[i + 1:]:
                if b.q not in a.vicini:
                    continue
                ca = quarter_ideal(a.q, P).centroid
                cb = quarter_ideal(b.q, P).centroid
                ux, uy = cb.x - ca.x, cb.y - ca.y
                n = math.hypot(ux, uy)
                ux, uy = ux / n, uy / n
                cmds = params_cmds() + a.commands(solo_solido=True) + b.commands(solo_solido=True) + [
                    {'command': 'solid.move', 'params': {'bodies': [b.nome], 'translate': [ux * SPOSTA_PROVA, uy * SPOSTA_PROVA, 0]}},
                    {'command': 'inspect.interference', 'params': {'bodies': [a.nome, b.nome]}}]
                out = run_sc(cmds, tmp, f'presa_{a.q}_{b.q}')
                v = sum(o['volume_mm3'] for o in out[-1]['interferences'])
                low_a = quarter_shape(a.q, P).union(unary_union(a.knob_shapes(a.code))).difference(unary_union(a.knob_shapes(a.incavi)))
                low_b = quarter_shape(b.q, P).union(unary_union(b.knob_shapes(b.code))).difference(unary_union(b.knob_shapes(b.incavi)))
                play = lock_play(low_a, low_b, ux, uy)
                presa.append({'a': a.nome, 'b': b.nome, 'lati_con_coda': a.vicini[b.q], 'urto_tirando_0_6mm_mm3': round(v, 3),
                              'presa_a_trazione_mm': round(play, 3)})
                ok &= v > 0.01 and play < SPOSTA_PROVA
        ris['prove']['presa_code'] = presa
        print('PROVA presa', json.dumps(presa, ensure_ascii=False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if ok:
        ris['file_3mf'] = tremf()
        print('3MF', json.dumps(ris['file_3mf'], ensure_ascii=False))
    ris['ok'] = bool(ok)
    with open(os.path.join(OUT, 'risultati.json'), 'w') as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)
    if not ok:
        sys.exit('CONTROLLI FALLITI: vedi out/risultati.json')
    print('TUTTO OK')


# ---- 4 file 3MF, uno per tipo di pezzo, ognuno sui suoi piatti da PIATTO mm (Daniele, 13/11 18:18) -------------------
def oggetti_3mf():
    """[(oggetto del 3MF, STL in out/, copie)]: tutto il gioco in 3D. Quantità dai CSV del kit (segnalini.csv, stati.csv,
    tessere_esplorazione.csv), dalla mappa (14 fiori) e dalle rotelle (6 per plancia × PLANCE, scontro, custode, Profezia:
    un perno e un fermo per rotella). Lo stesso STL può dare più oggetti, con nomi diversi per assegnare i colori."""
    seg = {r['nome']: int(r['copie']) for r in csv.DictReader(open(os.path.join(DATI, 'segnalini.csv'), encoding='utf-8'))}
    tessere = list(csv.DictReader(open(os.path.join(DATI, 'tessere_esplorazione.csv'), encoding='utf-8')))
    n_rot = sum(c for _, _, c in ROTELLE_3D)
    return ([(f'vassoio_{q}', f'vassoio_{q}', 1) for q in QUARTI] + [('fiore', 'fiore', len(M.SPAZI))]
            + [(n, f'rotella_finestra_{w:g}x{h:g}', c) for n, (w, h), c in ROTELLE_3D]
            + [('perno', 'perno', n_rot), ('fermo', 'fermo', n_rot),
               ('tessera_stato', 'tessera_stato', copie_csv('stati.csv')),
               ('segnalino_indizio', 'segnalino_tondo', seg['Indizio']), ('segnalino_forte_volonta', 'segnalino_tondo', seg['Forte Volontà']),
               ('segnalino_usato', 'segnalino_tondo', seg['Usato']), ('segnalino_cripta', 'segnalino_cripta', 1),
               ('tessera_esplorazione', 'tessera_esplorazione', len(tessere))])


def file_3mf(o):
    """il file 3MF (in out/) dove va l'oggetto o."""
    if o.startswith('vassoio_') or o == 'fiore':
        return 'mappa.3mf'
    if o.startswith('rotella_') or o in ('perno', 'fermo'):
        return 'rotelle_fulcri.3mf'
    if o == 'tessera_esplorazione':
        return 'tessere_esplorazione.3mf'
    return 'segnalini.3mf'


FILE_3MF = {'mappa.3mf': 'mappa 12x12 (4 quarti del vassoio, 14 fiori)', 'rotelle_fulcri.3mf': 'rotelle, perni e fermi',
            'segnalini.3mf': 'tessere Stato, Indizi, Forte Volonta, Usato, Cripta', 'tessere_esplorazione.3mf': 'Tessere Esplorazione'}


def leggi_mesh(stl):
    tri = read_stl(os.path.join(OUT, stl + '.stl'))
    v, idx = np.unique(np.round(tri.reshape(-1, 3), 5), axis=0, return_inverse=True)
    v = v - [(v[:, 0].min() + v[:, 0].max()) / 2, (v[:, 1].min() + v[:, 1].max()) / 2, v[:, 2].min()]   # centro xy, fondo a z=0
    return v, idx.reshape(-1, 3), v[:, 0].max() * 2, v[:, 1].max() * 2


def disponi(oggetti, mesh, distanza):
    """piatti: [[(oggetto, x, y)]] (centri, origine al centro del piatto). 4 piatti con un quarto, i fiori in griglia, poi
    gli altri pezzi a file (nell'ordine di oggetti_3mf) dall'alto a sinistra, a distanza mm tra loro e dal bordo."""
    dim = {o: mesh[s][2:] for o, s, _ in oggetti}
    piatti = [[(o, 0.0, 0.0)] for o, _, c in oggetti if o.startswith('vassoio_')]
    if 'fiore' in dim:
        fw, fh = dim['fiore']
        cols = int((PIATTO - distanza) // (fw + distanza))
        rows = int((PIATTO - distanza) // (fh + distanza))
        posti = [(-(cols - 1) / 2 * (fw + distanza) + c * (fw + distanza), (rows - 1) / 2 * (fh + distanza) - r * (fh + distanza))
                 for r in range(rows) for c in range(cols)]
        resto = next(c for o, _, c in oggetti if o == 'fiore')
        while resto:
            piatti.append([('fiore', x, y) for x, y in posti[:resto]])
            resto -= len(posti[:resto])
    lim = PIATTO / 2 - distanza
    pl, x, y, hr = [], -lim, lim, 0.0
    for o, _, c in oggetti:
        if o.startswith('vassoio_') or o == 'fiore':
            continue
        w, h = dim[o]
        for _ in range(c):
            if x + w > lim + 1e-9:                     # fila nuova
                x, y, hr = -lim, y - hr - distanza, 0.0
            if y - h < -lim - 1e-9:                    # piatto nuovo
                piatti.append(pl)
                pl, x, y, hr = [], -lim, lim, 0.0
            pl.append((o, x + w / 2, y - h / 2))
            x, hr = x + w + distanza, max(hr, h)
    if pl:
        piatti.append(pl)
    return piatti


def scrivi_3mf(path, oggetti, mesh, piatti, titolo, passo_piatti=230.0):
    """3MF standard (core 2015/02, mm): un oggetto per nome con la mesh del suo STL, un'istanza per copia; piatti affiancati
    lungo X ogni passo_piatti mm, istanze chiamate «Piatto N · oggetto»."""
    usati = list(dict.fromkeys(o for p in piatti for o, _, _ in p))
    stl = {o: s for o, s, _ in oggetti}
    ids = {o: i + 1 for i, o in enumerate(usati)}
    res, items = [], []
    for o in usati:
        v, f, _, _ = mesh[stl[o]]
        vs = ''.join(f'<vertex x="{a:.5f}" y="{b:.5f}" z="{c:.5f}"/>' for a, b, c in v)
        ts = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f)
        res.append(f'<object id="{ids[o]}" type="model" name="{o}"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>')
    for k, pl in enumerate(piatti):
        cx = k * passo_piatti + PIATTO / 2
        for o, x, y in pl:
            items.append(f'<item objectid="{ids[o]}" transform="1 0 0 0 1 0 0 0 1 {cx + x:.4f} {PIATTO / 2 + y:.4f} 0" '
                         f'name="Piatto {k + 1} · {o}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="it-IT" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<metadata name="Title">{titolo}</metadata>'
             f'<resources>{"".join(res)}</resources><build>{"".join(items)}</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', model)
    return len(items)


def un_3mf(nome, oggetti, distanza=5.0):
    """scrive out/<nome> con gli `oggetti` nella quantità giusta su piatti da PIATTO mm (disponi()): controlla ingombri
    dentro il piatto, distanze e quantità, poi rilegge il file e riconta le istanze per oggetto."""
    path = os.path.join(OUT, nome)
    mesh = {s: leggi_mesh(s) for s in dict.fromkeys(s for _, s, _ in oggetti)}
    piatti = disponi(oggetti, mesh, distanza)
    stl = {o: s for o, s, _ in oggetti}
    conta = {}
    for k, pl in enumerate(piatti):
        rect = []
        for o, x, y in pl:
            w, h = mesh[stl[o]][2:]
            rect.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2))
            conta[o] = conta.get(o, 0) + 1
        for a in rect:
            assert a[0] >= -PIATTO / 2 and a[2] <= PIATTO / 2 and a[1] >= -PIATTO / 2 and a[3] <= PIATTO / 2, f'{nome} piatto {k + 1}: pezzo fuori'
        for i, a in enumerate(rect):
            for b in rect[i + 1:]:
                assert a[2] + distanza <= b[0] + 1e-6 or b[2] + distanza <= a[0] + 1e-6 or a[3] + distanza <= b[1] + 1e-6 or b[3] + distanza <= a[1] + 1e-6, \
                    f'{nome} piatto {k + 1}: pezzi a meno di {distanza} mm'
    assert conta == {o: c for o, _, c in oggetti}, conta
    n = scrivi_3mf(path, oggetti, mesh, piatti, f'Il Tesoro del Goblin - {FILE_3MF[nome]}')
    with zipfile.ZipFile(path) as z:      # controllo indipendente: rilegge il file e conta le istanze per oggetto
        root = ET.fromstring(z.read('3D/3dmodel.model'))
    ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    nomi = {o.get('id'): o.get('name') for o in root.findall('.//m:object', ns)}
    letti = {}
    for it in root.findall('.//m:item', ns):
        letti[nomi[it.get('objectid')]] = letti.get(nomi[it.get('objectid')], 0) + 1
    assert letti == conta and root.get('unit') == 'millimeter', letti
    tabella = {o: {'copie': c, 'stl': s, 'piatti': sorted({k + 1 for k, pl in enumerate(piatti) for o2, _, _ in pl if o2 == o})}
               for o, s, c in oggetti}
    return {'piatti': len(piatti), 'istanze': n, 'pezzi': tabella,
            'per_piatto': [dict(sorted({o: sum(1 for o2, _, _ in pl if o2 == o) for o, _, _ in pl}.items())) for pl in piatti],
            '_piatti': piatti, '_oggetti': oggetti, '_mesh': mesh}


def anteprima_piatto(info, k, png, tmp):
    """PNG dall'alto del piatto k (1...) di un 3MF: un 3MF col solo quel piatto, inserito in SolidCraft."""
    p3 = os.path.join(tmp, f'piatto_{k}.3mf')
    scrivi_3mf(p3, info['_oggetti'], info['_mesh'], [info['_piatti'][k - 1]], f'piatto {k}')
    sp = os.path.join(tmp, f'piatto_{k}.json')
    with open(sp, 'w') as f:
        json.dump({'commands': [{'command': 'file.insert_mesh', 'params': {'path': p3}}]}, f)
    snapshot(sp, png, {'target': [PIATTO / 2, PIATTO / 2, 0], 'yaw': 0.0, 'pitch': 1.0, 'distance': 330}, 1400, 1100)


def tremf():
    """scrive i 4 file 3MF di FILE_3MF in out/ (e toglie i 3MF di un pezzo solo che SolidCraft lascia accanto agli STL),
    controlla che ogni oggetto stia in un solo file con tutte le sue copie, e scrive l'anteprima del piatto 1 di
    segnalini.3mf (out/piatto_segnalini.png)."""
    oggetti = oggetti_3mf()
    res, infos = {}, {}
    for nome in FILE_3MF:
        infos[nome] = un_3mf(nome, [t for t in oggetti if file_3mf(t[0]) == nome])
        res[nome] = {c: v for c, v in infos[nome].items() if not c.startswith('_')}
    assert sum(len(i['_oggetti']) for i in infos.values()) == len(oggetti)
    for s in dict.fromkeys(s for _, s, _ in oggetti):
        p = os.path.join(OUT, s + '.3mf')
        if os.path.exists(p):
            os.remove(p)
    tmp = tempfile.mkdtemp(prefix='mappa3d-piatto-')
    try:
        anteprima_piatto(infos['segnalini.3mf'], 1, os.path.join(OUT, 'piatto_segnalini.png'), tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    res['anteprima'] = {'png': 'piatto_segnalini.png', 'file': 'segnalini.3mf', 'piatto': 1}
    return res


# ---- controllo degli adesivi (segnalini_3d.pdf del kit) contro le tasche ----------------------------------------------
def anelli_pdf(pdf, n, tmp, larghezza=0.2):
    """percorsi chiusi tracciati con il tratto da `larghezza` mm (i tagli degli adesivi) nella pagina n del PDF: per ogni
    percorso la lista degli anelli in mm, y in giù. Coordinate vere del PDF (pdftocairo -svg; la sua matrice 0,998785 è un
    artefatto, vedi carta_base_3d.py). Curve di Bézier campionate."""
    import re
    out = os.path.join(tmp, f'a{n}.svg')
    subprocess.run(['pdftocairo', '-svg', '-f', str(n), '-l', str(n), pdf, out], check=True)
    k = 25.4 / 72
    res = []
    for m in re.finditer(r'<path\b([^>]*)>', open(out, encoding='utf-8').read()):
        at = m.group(1)
        w = re.search(r'stroke-width="([\d.]+)"', at)
        d = re.search(r'\bd="([^"]+)"', at)
        if not (w and d) or 'fill="none"' not in at or abs(float(w.group(1)) - larghezza / k) > 0.01:
            continue
        tok = re.findall(r'[MLCZ]|-?\d+\.?\d*(?:e-?\d+)?', d.group(1))
        anelli, cur, i, cmd = [], [], 0, None
        while i < len(tok):
            t = tok[i]
            if t in 'MLCZ':
                cmd = t
                i += 1
                if t == 'Z':
                    if len(cur) > 2:
                        anelli.append(cur)
                    cur = []
                elif t == 'M':
                    if len(cur) > 2:
                        anelli.append(cur)
                    cur = []
                continue
            if cmd in 'ML':
                cur.append((float(tok[i]) * k, float(tok[i + 1]) * k))
                i += 2
            elif cmd == 'C':
                p0 = np.array(cur[-1])
                c = [np.array((float(tok[i + 2 * j]) * k, float(tok[i + 2 * j + 1]) * k)) for j in range(3)]
                for t_ in np.linspace(0, 1, 17)[1:]:
                    cur.append(tuple((1 - t_) ** 3 * p0 + 3 * (1 - t_) ** 2 * t_ * c[0] + 3 * (1 - t_) * t_ ** 2 * c[1] + t_ ** 3 * c[2]))
                i += 6
        if len(cur) > 2:
            anelli.append(cur)
        if anelli:
            res.append(anelli)
    return res


def verifica_adesivi(pdf):
    """ogni taglio da 0,2 mm di segnalini_3d.pdf confrontato con l'adesivo atteso (scarto di Hausdorff) e con la tasca del
    pezzo 3D (gioco per lato = (tasca - adesivo misurato) / 2, atteso gioco_carta); conteggi per tipo; scala del segmento
    di 100 mm misurata a 600 dpi (verifica_pdf.lunghezza_segmento)."""
    sys.path.insert(0, os.path.join(QUI, '..', 'sorgenti'))
    import verifica_pdf  # noqa: E402
    cripta = hex_local(P, P['passo'] / 2)                 # la carta della Cripta (25,2), tasca = + gioco_carta
    n = {o: c for o, _, c in oggetti_3mf()}
    tipi = {'tessera (fronte e dorso)': (Tondo('t', 'tessera_d'), 2 * n['tessera_esplorazione']),
            'segnalino tondo': (Tondo('s', 'gettone_d'), n['segnalino_indizio'] + n['segnalino_forte_volonta'] + n['segnalino_usato']),
            'tessera Stato': (Stato(), n['tessera_stato'])}
    for f in dict.fromkeys(f for _, f, _ in ROTELLE_3D):
        tipi[f'rotella {f[0]}x{f[1]}'] = (Rotella(f), sum(c for _, f2, c in ROTELLE_3D if f2 == f))
    attesi = {t: (pz.adesivo(), pz.tasca()) for t, (pz, _) in tipi.items()}
    attesi['Cripta'] = (cripta, hex_local(P, P['passo'] / 2 + P['gioco_carta']))
    dims = {t: (a.bounds[2] - a.bounds[0], a.bounds[3] - a.bounds[1], len(a.interiors) > 0) for t, (a, _) in attesi.items()}
    conta = {t: 0 for t in attesi}
    peggio = {t: {'scarto_max_mm': 0.0, 'gioco_min_mm': 9.0, 'gioco_max_mm': 0.0} for t in attesi}
    scala = []
    pagine = int(next(l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')).split()[1])
    with tempfile.TemporaryDirectory(prefix='adesivi3d_') as tmp:
        for n in range(1, pagine + 1):
            subprocess.run(['pdftoppm', '-r', '600', '-gray', '-f', str(n), '-l', str(n), '-png', pdf, f'{tmp}/s{n}'], check=True)
            png = next(p for p in os.listdir(tmp) if p.startswith(f's{n}-'))
            scala.append(verifica_pdf.lunghezza_segmento(os.path.join(tmp, png)))
            os.remove(os.path.join(tmp, png))
            for anelli in anelli_pdf(pdf, n, tmp):
                pol = sorted((Polygon([(x, -y) for x, y in a]) for a in anelli), key=lambda p: -p.area)
                est = pol[0]
                w = est.bounds[2] - est.bounds[0]
                h = est.bounds[3] - est.bounds[1]
                t = min((t for t in attesi if dims[t][2] == (len(pol) > 1)), key=lambda t: abs(dims[t][0] - w) + abs(dims[t][1] - h))
                ad, ta = attesi[t]
                if len(pol) > 1:              # rotella: si allinea sul foro del mozzo
                    c, c0 = pol[1].centroid, Point(0, 0)
                else:
                    c, c0 = est.centroid, ad.centroid
                g = affinity.translate(Polygon(est.exterior.coords, [p.exterior.coords for p in pol[1:]]), c0.x - c.x, c0.y - c.y)
                sc = g.boundary.hausdorff_distance(ad.boundary)
                gx = ((ta.bounds[2] - ta.bounds[0]) - (g.bounds[2] - g.bounds[0])) / 2
                conta[t] += 1
                p = peggio[t]
                p['scarto_max_mm'] = round(max(p['scarto_max_mm'], sc), 4)
                p['gioco_min_mm'], p['gioco_max_mm'] = round(min(p['gioco_min_mm'], gx), 4), round(max(p['gioco_max_mm'], gx), 4)
    attesi_n = {t: c for t, (_, c) in tipi.items()} | {'Cripta': 1}
    ok = (conta == attesi_n and all(v is not None and abs(v / 100 - 1) <= 5e-4 for v in scala)
          and all(p['scarto_max_mm'] <= 0.2 and abs(p['gioco_min_mm'] - P['gioco_carta']) <= 0.2 and abs(p['gioco_max_mm'] - P['gioco_carta']) <= 0.2
                  for p in peggio.values()))
    return {'pdf': os.path.basename(pdf), 'pagine': pagine, 'segmento_100mm_misurato': [round(v, 3) if v else None for v in scala],
            'adesivi': {t: {'trovati': conta[t], 'attesi': attesi_n[t], **peggio[t]} for t in attesi}, 'gioco_carta_atteso_mm': P['gioco_carta'], 'ok': bool(ok)}


if __name__ == '__main__':
    if '--solo-3mf' in sys.argv:          # rifà solo i 4 file 3MF dagli STL già in out/
        print(json.dumps(tremf(), ensure_ascii=False))
    elif '--verifica-adesivi' in sys.argv:   # segnalini_3d.pdf del kit contro le tasche: python3 ... --verifica-adesivi PDF
        r = verifica_adesivi(sys.argv[sys.argv.index('--verifica-adesivi') + 1])
        print(json.dumps(r, ensure_ascii=False, indent=1))
        sys.exit(0 if r['ok'] else 'ADESIVI FUORI TOLLERANZA')
    else:
        main()
