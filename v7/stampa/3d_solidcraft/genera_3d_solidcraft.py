#!/usr/bin/env python3
"""Mappa 12×12 in 3D, costruita in SolidCraft (12/11, decisione di Daniele: niente Blender).

Uso (dalla radice del repo):  python3 v7/stampa/3d_solidcraft/genera_3d_solidcraft.py
Serve: python3 con shapely >= 2.1 e numpy, `solidcraft-cli` (SolidCraft >= 0.40) nel PATH.

Pezzi (mappa da v7/stampa/sorgenti/dati/base12.csv: spazi dei fiori, posizioni 0-6, esagoni di bordo):
- VASSOIO in 4 parti (NO, NE, SO, SE): fondo, alloggio unico per i 14 fiori, tasca per la carta della base del kit
  (mappa_base.pdf, con le coordinate, ritagliata lungo i contorni d'ottone degli spazi), numeri degli spazi e cifre 1-6
  dell'anello incisi sul fondo dell'alloggio. Le 4 parti si uniscono con code a pomello nel fondo.
- FIORE da 7 esagoni senza incastri, tasca per la carta su tutte e due le facce (carta: out/carta_fiori_3d.pdf, facce A
  e B separate): entra nell'alloggio girato e voltato in qualsiasi modo.
- SEGNAPOSTO «?» (disco) e SEGNALINO CRIPTA (esagono) con la tasca per le carte di mappa_fiori.pdf.

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
BASE12 = os.path.join(QUI, '..', 'sorgenti', 'dati', 'base12.csv')
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
    ('fondo', 1.2, 'spessore del fondo del vassoio = altezza delle code (1-2)'),
    ('alloggio_prof', 2.0, 'profondità dell alloggio dei fiori (1,5 ... fiore_spessore)'),
    ('fiore_spessore', 3.0, 'spessore del fiore (2,5-4): sporge di fiore_spessore - alloggio_prof'),
    ('tasca_prof', 0.5, 'profondità delle tasche per la carta (cartoncino 0,3-0,4; 0,3-1)'),
    ('bordino', 0.85, 'bordino tra contorno e tasca della carta (0,6-1,5)'),
    ('gioco_carta', 0.25, 'gioco per lato tra carta ritagliata e tasca (0,15-0,4)'),
    ('fascia_carta', 5.5, 'fascia delle coordinate della carta della base (mappa_base.pdf: FASCIA12 = 5,5; < margine - gioco_carta - 0,8)'),
    ('carta_domanda', 20.0, 'diametro della carta del segnaposto «?» (mappa_fiori.pdf: Ø 20)'),
    ('segnalino_spessore', 2.0, 'spessore di segnaposto «?» e segnalino Cripta (1,5-3)'),
    ('smusso', 0.4, 'smusso degli spigoli del fiore, sopra e sotto (0,2-0,6; < bordino)'),
    ('raggio_angolo', 3.0, 'raggio degli angoli esterni del vassoio (0,5-6)'),
    ('coda_collo', 2.6, 'larghezza del collo della coda a pomello (2-3)'),
    ('coda_testa', 4.0, 'diametro del pomello (coda_collo + 1 ... 5)'),
    ('coda_lunga', 3.9, 'quanto la coda entra nella parte vicina (3,5-4,5; > coda_testa/2)'),
    ('numero_alto', 8.0, 'altezza del numero dello spazio inciso sul fondo (5-10)'),
    ('cifra_alta', 4.0, 'altezza delle cifre 1-6 dell anello incise sul fondo (3-5)'),
    ('incisione', 0.5, 'profondità delle incisioni (0,4-0,8; fondo: lascia almeno 0,6)'),
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


def snapshot(design, png, view='iso', w=1000, h=800):
    r = subprocess.run(['solidcraft-cli', 'snapshot', design, '--out', png, '--view', view, '--width', str(w), '--height', str(h),
                        '--no-grid', '--no-axes'], capture_output=True, text=True, timeout=900)
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


class Segnaposto:
    """segnaposto «?»: disco con la tasca sopra per la carta Ø carta_domanda di mappa_fiori.pdf (le due facce della carta
    sono uguali)."""
    nome = 'segnaposto_domanda'

    def r(self, extra):
        return P['carta_domanda'] / 2 + P['gioco_carta'] + extra

    def expected(self):
        H = P['segnalino_spessore']
        R, c = self.r(P['bordino']), P['smusso']      # disco smussato: cilindro + due tronchi di cono
        cono = math.pi * c / 3 * ((R - c) ** 2 + (R - c) * R + R ** 2)
        vol = math.pi * R ** 2 * (H - 2 * c) + 2 * cono - math.pi * self.r(0) ** 2 * P['tasca_prof']
        return vol, [round(2 * R, 4), round(2 * R, 4), H]

    def commands(self, body=None):
        body = body or self.nome
        H = P['segnalino_spessore']
        R = self.r(P['bordino'])
        return [
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'name': 'Disco'}},
            {'command': 'sketch.circle.center', 'params': {'center': ['0*passo', '0*passo'], 'radius': 'carta_domanda/2 + gioco_carta + bordino'}},
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'segnalino_spessore', 'operation': 'new', 'name': 'Disco', 'body_name': body}},
            {'command': 'solid.chamfer', 'params': {'edges': [[R, 0, 0], [R, 0, H]], 'distance': 'smusso', 'body': body, 'name': 'Smussi'}},
            {'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'segnalino_spessore', 'name': 'Tasca'}},
            {'command': 'sketch.circle.center', 'params': {'center': ['0*passo', '0*passo'], 'radius': 'carta_domanda/2 + gioco_carta'}},
            {'command': 'sketch.finish', 'params': {}},
            {'command': 'solid.extrude', 'params': {'distance': 'tasca_prof', 'direction': 'negative', 'operation': 'cut', 'name': 'Tasca',
                                                    'targets': [body]}},
        ]

    def carta(self):
        return {'tasca': 'sopra', 'pdf': 'mappa_fiori.pdf (foglio 3)', 'carta_mm': P['carta_domanda'],
                'tasca_mm': round(2 * self.r(0), 3)}


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


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='mappa3d-sc-')
    ris = {'parametri': P, 'gioco_carta_mm': P['gioco_carta'], 'piatto_ipotizzato_mm': PIATTO, 'pezzi': {}, 'prove': {}}
    ok = True
    try:
        # 1. fiore e segnalini
        fi = Fiore()
        for pz in (fi, Segnaposto(), Cripta()):
            vol, bb = pz.expected()
            sc = os.path.join(OUT, pz.nome + '.solidcraft')
            out = run_sc(params_cmds() + pz.commands() + [{'command': 'model.faces', 'params': {'body': pz.nome}},
                                                          {'command': 'inspect.measure', 'params': {}}], tmp, pz.nome,
                         ['--save', sc, '--out', os.path.join(OUT, pz.nome + '.stl'), '--out', os.path.join(OUT, pz.nome + '.3mf')])
            m = body_of(measures(out)[-1], pz.nome)
            files, fok = check_files(pz.nome, m['volume_mm3'])
            fc = out[-2]['faces']
            giu = [f for f in fc if f.get('plane_normal') and f['plane_normal'][2] < -0.999]
            fondo_piatto = len(giu) == 1 and abs(giu[0]['centroid'][2]) < 1e-6      # una sola faccia verso il basso, a z = 0
            spess = min(f['centroid'][2] for f in fc if f.get('plane_normal') and f['plane_normal'][2] > 0.999)   # fondo della tasca
            ok &= fondo_piatto and spess >= 1.2 - 1e-9
            r = {'volume_atteso_mm3': round(vol, 3), 'volume_mm3': round(m['volume_mm3'], 3),
                 'errore_volume_rel': abs(m['volume_mm3'] - vol) / vol, 'massa_pla_g': round(m['volume_mm3'] * 1.24e-3, 2),
                 'ingombro_atteso_mm': bb, 'ingombro_mm': [round(m['bbox']['max'][i] - m['bbox']['min'][i], 4) for i in range(3)],
                 'avvisi': warnings(out), 'file': files, 'carta': pz.carta(),
                 'facce_verso_il_basso': len(giu), 'fondo_piatto': fondo_piatto, 'spessore_sotto_la_tasca_mm': round(spess, 4)}
            r['ok'] = bool(r['errore_volume_rel'] < 1e-4 and not r['avvisi'] and fok
                           and all(abs(a - b) < 2e-3 for a, b in zip(bb, r['ingombro_mm'])))
            ok &= r['ok']
            ris['pezzi'][pz.nome] = r
            print('PEZZO', pz.nome, json.dumps({k: r[k] for k in r if k != 'file'}, ensure_ascii=False))
            snapshot(sc, os.path.join(OUT, pz.nome + '.png'), w=800, h=600)

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
        ris['mappa_completa'] = mappa_completa(os.path.join(OUT, 'mappa_completa.3mf'))
        print('3MF', json.dumps(ris['mappa_completa'], ensure_ascii=False))
    ris['ok'] = bool(ok)
    with open(os.path.join(OUT, 'risultati.json'), 'w') as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)
    if not ok:
        sys.exit('CONTROLLI FALLITI: vedi out/risultati.json')
    print('TUTTO OK')


# ---- 3MF unico con tutti i pezzi su piatti da PIATTO mm --------------------------------------------------------------
def mappa_completa(path, distanza=5.0, passo_piatti=230.0):
    """un 3MF con un oggetto per tipo di pezzo (mesh dagli STL di out/) e un'istanza per copia: 4 piatti con un quarto,
    piatti di fiori, un piatto con i 24 «?» e la Cripta; piatti affiancati lungo X ogni passo_piatti mm."""
    pezzi = ['vassoio_NO', 'vassoio_NE', 'vassoio_SO', 'vassoio_SE', 'fiore', 'segnaposto_domanda', 'segnalino_cripta']
    mesh = {}
    for n in pezzi:
        tri = read_stl(os.path.join(OUT, n + '.stl'))
        v, idx = np.unique(np.round(tri.reshape(-1, 3), 5), axis=0, return_inverse=True)
        v = v - [(v[:, 0].min() + v[:, 0].max()) / 2, (v[:, 1].min() + v[:, 1].max()) / 2, v[:, 2].min()]   # centro xy, fondo a z=0
        mesh[n] = (v, idx.reshape(-1, 3), v[:, 0].max() * 2, v[:, 1].max() * 2)
    piatti = [[(f'vassoio {q}', 'vassoio_' + q, 0.0, 0.0)] for q in QUARTI]

    def griglia(nome, n, w, h, quanti, x0=None):
        cols = int((PIATTO - 2 * distanza + distanza) // (w + distanza))
        rows = int((PIATTO - 2 * distanza + distanza) // (h + distanza))
        posti = [(-(cols - 1) / 2 * (w + distanza) + c * (w + distanza), (rows - 1) / 2 * (h + distanza) - r * (h + distanza))
                 for r in range(rows) for c in range(cols)]
        return posti[:quanti], cols * rows
    _, _, fw, fh = mesh['fiore']
    resto = 14
    while resto:
        posti, cap = griglia('fiore', 0, fw, fh, resto)
        piatti.append([('fiore', 'fiore', x, y) for x, y in posti])
        resto -= len(posti)
    _, _, dw, dh = mesh['segnaposto_domanda']
    _, _, cw, ch = mesh['segnalino_cripta']
    passo = max(dw, cw) + distanza
    posti = [(-3 * passo + (k % 7) * passo, 2 * passo - (k // 7) * passo) for k in range(25)]
    piatti.append([('«?»', 'segnaposto_domanda', x, y) for x, y in posti[:24]] + [('Cripta', 'segnalino_cripta', *posti[24])])
    # controlli: ingombri (rettangoli) dentro il piatto e distanti almeno `distanza`
    conta = {}
    for k, pl in enumerate(piatti):
        rect = []
        for _, n, x, y in pl:
            w, h = mesh[n][2], mesh[n][3]
            rect.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2))
            conta[n] = conta.get(n, 0) + 1
        for a in rect:
            assert a[0] >= -PIATTO / 2 and a[2] <= PIATTO / 2 and a[1] >= -PIATTO / 2 and a[3] <= PIATTO / 2, f'piatto {k + 1}: pezzo fuori'
        for i, a in enumerate(rect):
            for b in rect[i + 1:]:
                assert a[2] + distanza <= b[0] + 1e-6 or b[2] + distanza <= a[0] + 1e-6 or a[3] + distanza <= b[1] + 1e-6 or b[3] + distanza <= a[1] + 1e-6, \
                    f'piatto {k + 1}: pezzi a meno di {distanza} mm'
    assert conta == {'vassoio_NO': 1, 'vassoio_NE': 1, 'vassoio_SO': 1, 'vassoio_SE': 1, 'fiore': 14, 'segnaposto_domanda': 24, 'segnalino_cripta': 1}, conta
    res, items = [], []
    ids = {n: i + 1 for i, n in enumerate(pezzi)}
    for n in pezzi:
        v, f, _, _ = mesh[n]
        vs = ''.join(f'<vertex x="{a:.5f}" y="{b:.5f}" z="{c:.5f}"/>' for a, b, c in v)
        ts = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f)
        res.append(f'<object id="{ids[n]}" type="model" name="{n}"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>')
    for k, pl in enumerate(piatti):
        cx = k * passo_piatti + PIATTO / 2
        for etichetta, n, x, y in pl:
            items.append(f'<item objectid="{ids[n]}" transform="1 0 0 0 1 0 0 0 1 {cx + x:.4f} {PIATTO / 2 + y:.4f} 0" '
                         f'name="Piatto {k + 1} · {etichetta}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="it-IT" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<metadata name="Title">Il Tesoro del Goblin - mappa 12x12 completa</metadata>'
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
    for n in pezzi:            # i 3MF singoli non servono più: resta il 3MF unico (gli STL e i .solidcraft restano)
        p = os.path.join(OUT, n + '.3mf')
        if os.path.exists(p):
            os.remove(p)
    return {'file': os.path.basename(path), 'piatti': len(piatti), 'pezzi': conta, 'istanze': len(items),
            'per_piatto': [len(p) for p in piatti]}


if __name__ == '__main__':
    if '--solo-3mf' in sys.argv:          # rifà solo il 3MF unico dagli STL già in out/
        print(json.dumps(mappa_completa(os.path.join(OUT, 'mappa_completa.3mf')), ensure_ascii=False))
    else:
        main()
