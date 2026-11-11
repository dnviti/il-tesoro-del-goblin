#!/usr/bin/env python3
"""Tessere esagonali 3D incastrabili, muri con pioli, piatti di stampa (Spec D23, R 8.1/8.2).

Uso (dalla radice del repo):  python3 v7/stampa/3d/genera_3d.py
Serve: python3 con shapely >= 2.1 e Blender >= 4.5 (headless, `blender -b`).

Qui si calcola tutta la geometria 2D (shapely) e si fanno i controlli di incastro in pianta; Blender (blender_3d.py)
estrude i profili, fa le booleane (Manifold per costruire, esatte per le intersezioni di controllo), controlla le mesh
(chiuse, volume, ingombri, passo, intersezioni),
scrive STL e 3MF e le anteprime PNG in questa cartella.
"""
import json, math, os, shutil, subprocess, sys, tempfile, zipfile
import xml.etree.ElementTree as ET

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union

QUI = os.path.dirname(os.path.abspath(__file__))

# ---- parametri (mm) -------------------------------------------------------------------------------------------
PASSO = 25.2          # esagono da lato a lato = distanza tra i centri di due tessere vicine (Spec R 8.2)
SPESSORE = 3.0        # spessore della tessera
GIOCO = 0.15          # gioco per lato su tutto il contorno (FDM, ugello 0,4: 0,15-0,2)
R_SPIGOLI = 0.15      # raggio degli spigoli vivi esterni in pianta (più grande = più gioco a trazione)
CODA_COLLO = 2.6     # linguetta a pomello (come un puzzle): larghezza del collo
CODA_TESTA = 4.0     # diametro del pomello
CODA_LUNGA = 3.9     # quanto entra nella tessera vicina (punta del pomello dal lato)
CODA_ALTA = 2.0       # altezza della linguetta (sotto il fondo della tasca: non solleva la carta del vicino)
TASCA_LL = 23.2       # tasca per la carta: esagono da lato a lato (bordino di (PASSO - 2 GIOCO - TASCA_LL)/2)
TASCA_PROF = 0.5      # profondità della tasca (cartoncino 0,3-0,4)
CARTA_SCALA = 0.90    # stampa di tessere_mappa.pdf per le tessere 3D: esagono di carta = PASSO * scala
FORO_T = 4.5          # centro dei due mezzi fori per lato, dalla metà del lato
PIOLO_L, PIOLO_W = 3.0, 1.8   # piolo del muro (asola): lunghezza lungo il lato, larghezza
GIOCO_PIOLO = 0.2     # gioco per lato tra piolo e foro
FORO_PROF = 2.3       # profondità del foro dal piano della tessera
PIOLO_H = 2.0         # altezza del piolo sotto il muro
PIOLO_SMUSSO = (0.3, 0.25)   # invito in punta al piolo: altezza, rientro
MURO_W, MURO_H = 3.0, 7.0    # larghezza e altezza del muro (lunghezza: da vertice a vertice del lato, punte a 120°)
GIOCO_MURI = 0.2      # gioco tra due muri che si toccano in un vertice
PIATTO = 220.0        # piatto di stampa
PIATTO_PASSO = 31.0   # distanza tra i centri delle tessere sul piatto (staccate)
N_TESSERE, N_MURI = 20, 8
QS = 8               # segmenti per quarto di cerchio

AP = PASSO / 2                     # apotema
LATO = PASSO / math.sqrt(3)        # lato = raggio = 14,55
TAB = [i % 2 == 0 for i in range(6)]   # lato i (normale a 60*i gradi): linguetta sui pari, incavo sui dispari


def hexagon(apotema, cx=0.0, cy=0.0):
    r = apotema / math.cos(math.radians(30))
    return Polygon([(cx + r * math.cos(math.radians(90 + 60 * k)), cy + r * math.sin(math.radians(90 + 60 * k)))
                    for k in range(6)])


def edge_pt(i, t, n):
    """punto (t lungo il lato, n verso fuori) nel riferimento del lato i della tessera centrata nell'origine."""
    th = math.radians(60 * i)
    return (AP * math.cos(th) - t * math.sin(th) + n * math.cos(th), AP * math.sin(th) + t * math.cos(th) + n * math.sin(th))


def dovetail(i, sign):
    """linguetta ideale sul lato i (collo + pomello tondo): sign=+1 sporge fuori, -1 entra (incavo, specchio sul lato).
    Le spalle del pomello sono quasi perpendicolari al lato: il gioco a trazione resta ~2 GIOCO / cos."""
    r = CODA_TESTA / 2
    g = box(-0.5, -CODA_COLLO / 2, CODA_LUNGA - r, CODA_COLLO / 2).union(Point(CODA_LUNGA - r, 0).buffer(r, quad_segs=QS))
    g = affinity.translate(affinity.scale(g, sign, 1, origin=(0, 0)), AP, 0)
    return affinity.rotate(g, 60 * i, origin=(0, 0))


def stadium(cx, cy, length, width, ang_deg):
    r = width / 2
    s = LineString([(-(length / 2 - r), 0), (length / 2 - r, 0)]).buffer(r, quad_segs=QS)
    return affinity.translate(affinity.rotate(s, ang_deg, origin=(0, 0)), cx, cy)


def clean(p):
    """gioco uniforme verso l'interno e spigoli esterni arrotondati."""
    return p.buffer(-(GIOCO + R_SPIGOLI), join_style='mitre').buffer(R_SPIGOLI, quad_segs=QS)


H = hexagon(AP)
TABS = unary_union([dovetail(i, 1) for i in range(6) if TAB[i]])
SLOTS = unary_union([dovetail(i, -1) for i in range(6) if not TAB[i]])
CELL = H.union(TABS).difference(SLOTS)          # cella ideale: tassella il piano senza buchi
F_LOW = clean(CELL)                             # pianta della tessera fino a CODA_ALTA
F_UP = clean(H.difference(SLOTS))               # pianta sopra le linguette
POCKET = hexagon(TASCA_LL / 2)


def hole_centres():
    out = []
    for i in range(6):
        th = 60 * i
        for t in (-FORO_T, FORO_T):
            out.append((edge_pt(i, t, 0), th + 90))
    return out


HOLES = unary_union([stadium(x, y, PIOLO_L + 2 * GIOCO_PIOLO, PIOLO_W + 2 * GIOCO_PIOLO, a) for (x, y), a in hole_centres()])
Z_HOLE = SPESSORE - FORO_PROF
Z_POCKET = SPESSORE - TASCA_PROF


def tile_slabs():
    """fette a sezione costante (z0, z1, pianta) per il volume atteso."""
    zs = sorted({0.0, Z_HOLE, CODA_ALTA, Z_POCKET, SPESSORE})
    out = []
    for z0, z1 in zip(zs, zs[1:]):
        zm = (z0 + z1) / 2
        p = F_LOW if zm < CODA_ALTA else F_UP
        if zm > Z_HOLE:
            p = p.difference(HOLES)
        if zm > Z_POCKET:
            p = p.difference(POCKET)
        out.append((z0, z1, p))
    return out


def wall_foot():
    """muro ideale da vertice a vertice del lato, punte a 120° (tre muri in un vertice si chiudono a Y), poi il gioco."""
    h = MURO_W / 2 + GIOCO_MURI / 2
    e = LATO / 2
    s = h * math.tan(math.radians(30))
    p = Polygon([(e, 0), (e - s, h), (-(e - s), h), (-e, 0), (-(e - s), -h), (e - s, -h)])
    return p.buffer(-GIOCO_MURI / 2, join_style='mitre')


W_FOOT = wall_foot()
PEGS = unary_union([stadium(x, 0, PIOLO_L, PIOLO_W, 0) for x in (-FORO_T, FORO_T)])
PEGS_TIP = PEGS.buffer(-PIOLO_SMUSSO[1], join_style='mitre')


def coords(p):
    p = p.simplify(0)
    assert p.geom_type == 'Polygon' and len(p.interiors) == 0, p.geom_type
    c = list(p.exterior.coords)[:-1]
    if Polygon(c).exterior.is_ccw is False:
        c = c[::-1]
    return [[round(x, 6), round(y, 6)] for x, y in c]


def parts(g):
    return [g] if g.geom_type == 'Polygon' else list(g.geoms)


# ---- solidi come operazioni su prismi (Blender) --------------------------------------------------------------
def tile_spec():
    """prisma della pianta bassa alto quanto la tessera, poi si tolgono: la cima delle linguette sopra CODA_ALTA (un utensile
    che taglia dentro il solido lungo il lato, senza facce complanari), la tasca e i mezzi fori."""
    tips = [p.buffer(0.3, join_style='mitre').difference(F_UP) for p in parts(F_LOW.difference(F_UP)) if p.area > 0.01]
    cuts = [(t, CODA_ALTA) for t in tips] + [(POCKET, Z_POCKET)] + [(h, Z_HOLE) for h in parts(HOLES)]
    ops = [{'op': 'base', 'poly': coords(F_LOW), 'z0': 0, 'z1': SPESSORE},
           {'op': 'diff', 'polys': [coords(p) for p, _ in cuts], 'z0s': [z for _, z in cuts], 'z1': SPESSORE + 0.2}]
    vol = sum(p.area * (z1 - z0) for z0, z1, p in tile_slabs())
    return {'ops': ops, 'volume': vol}


def wall_spec():
    """muro nel riferimento di montaggio: base a z=0, pioli sotto (z negativa), lunghezza lungo x."""
    hs, ri = PIOLO_SMUSSO
    ops = [{'op': 'base', 'poly': coords(W_FOOT), 'z0': 0, 'z1': MURO_H}]
    for p in parts(PEGS):
        ops.append({'op': 'union', 'poly': coords(p), 'z0': -(PIOLO_H - hs), 'z1': 0.5})
    for p in parts(PEGS_TIP):
        ops.append({'op': 'union', 'poly': coords(p), 'z0': -PIOLO_H, 'z1': -(PIOLO_H - hs) + 0.1})
    vol = W_FOOT.area * MURO_H + PEGS.area * (PIOLO_H - hs) + PEGS_TIP.area * hs
    return {'ops': ops, 'volume': vol}


# ---- disposizioni ----------------------------------------------------------------------------------------------
def rot_poly(p, deg, x, y):
    return affinity.translate(affinity.rotate(p, deg, origin=(0, 0)), x, y)


def patch_layout():
    """3 x 3 a nido d'ape (file dispari spostate di mezzo passo), rotazioni miste 0/120/240."""
    out = []
    for r in range(3):
        for q in range(3):
            out.append({'obj': 'tessera', 'x': q * PASSO + (r % 2) * PASSO / 2, 'y': r * PASSO * math.sin(math.radians(60)),
                        'z': 0.0, 'rot': 120 * ((q + 2 * r) % 3)})
    return out


def neighbours(items):
    return [(a, b) for a in range(len(items)) for b in range(a + 1, len(items))
            if abs(math.hypot(items[a]['x'] - items[b]['x'], items[a]['y'] - items[b]['y']) - PASSO) < 1e-6]


def walls_on_patch(items):
    """due muri sulla tessera centrale (indice 4): lato destro (0°) e lato a 60°, che si toccano nel vertice a 30°."""
    c = items[4]
    out = []
    for th in (0, 60):
        mx, my = c['x'] + AP * math.cos(math.radians(th)), c['y'] + AP * math.sin(math.radians(th))
        out.append({'obj': 'muro', 'x': mx, 'y': my, 'z': SPESSORE, 'rot': th + 90})
    return out


def plate_layout():
    """N_TESSERE staccate a nido d'ape (passo PIATTO_PASSO) e sotto N_MURI capovolti (cima sul piatto, pioli in alto)."""
    cols, rows = 5, 4
    rs = PIATTO_PASSO * math.sin(math.radians(60))
    pts = [(q * PIATTO_PASSO + (r % 2) * PIATTO_PASSO / 2, r * rs) for r in range(rows) for q in range(cols)][:N_TESSERE]
    tiles = [{'obj': 'tessera', 'x': x, 'y': y, 'z': 0.0, 'rot': 0} for x, y in pts]
    wy = -LATO - 6.0
    wx0 = ((cols - 1) * PIATTO_PASSO + PIATTO_PASSO / 2) / 2 - (N_MURI - 1) * 18.0 / 2
    walls = [{'obj': 'muro_stampa', 'x': wx0 + k * 18.0, 'y': wy, 'z': 0.0, 'rot': 0} for k in range(N_MURI)]
    items = tiles + walls
    # centra sul piatto
    fp = unary_union([placed_foot(it) for it in items])
    minx, miny, maxx, maxy = fp.bounds
    dx, dy = PIATTO / 2 - (minx + maxx) / 2, PIATTO / 2 - (miny + maxy) / 2
    for it in items:
        it['x'] += dx; it['y'] += dy
    return items


def placed_foot(it):
    base = F_LOW if it['obj'] == 'tessera' else W_FOOT
    return rot_poly(base, it['rot'], it['x'], it['y'])


# ---- controlli 2D -----------------------------------------------------------------------------------------------
def checks_2d(patch, walls):
    res, ok = {}, True
    # 1. le celle ideali tassellano: centrale + 6 vicine, nessuna sovrapposizione, nessun buco
    cells = [CELL] + [rot_poly(CELL, 0, PASSO * math.cos(math.radians(60 * i)), PASSO * math.sin(math.radians(60 * i))) for i in range(6)]
    ov = sum(cells[a].intersection(cells[b]).area for a in range(7) for b in range(a + 1, 7))
    res['celle_ideali_sovrapposizione_mm2'] = round(ov, 9)
    res['celle_ideali_area_vs_esagoni'] = round(unary_union(cells).area - 7 * H.area, 9)
    ok &= ov < 1e-6 and abs(res['celle_ideali_area_vs_esagoni']) < 1e-6
    # 2. vicini nella 3x3 (con rotazioni): nessuna sovrapposizione, gioco minimo, incastro (tirando via il vicino urta)
    feet = [placed_foot(it) for it in patch]
    tops = [rot_poly(F_UP, it['rot'], it['x'], it['y']) for it in patch]
    gaps, locks, inter = [], [], 0.0
    for a, b in neighbours(patch):
        inter += feet[a].intersection(feet[b]).area + tops[a].intersection(tops[b]).area
        gaps.append(feet[a].distance(feet[b]))
        ux, uy = patch[a]['x'] - patch[b]['x'], patch[a]['y'] - patch[b]['y']
        L = math.hypot(ux, uy)
        lo, hi = 0.0, 3.0      # gioco a trazione: di quanto si allontana A da B prima che le linguette urtino
        for _ in range(30):
            m = (lo + hi) / 2
            if affinity.translate(feet[a], m * ux / L, m * uy / L).intersection(feet[b]).area > 1e-7:
                hi = m
            else:
                lo = m
        locks.append(hi)
    res['coppie_vicine_3x3'] = len(gaps)
    res['intersezione_vicini_mm2'] = round(inter, 9)
    res['gioco_minimo_tra_vicini_mm'] = round(min(gaps), 4)
    res['gioco_a_trazione_max_mm'] = round(max(locks), 3)
    ok &= inter < 1e-9 and min(gaps) >= 2 * GIOCO - 1e-6 and max(locks) < 0.5 and len(gaps) == 16
    # 3. muri: pioli dentro i mezzi fori col gioco, appoggio sui bordini, muri che si toccano in un vertice
    tile_hole_layers = [rot_poly(F_LOW.difference(HOLES), it['rot'], it['x'], it['y']) for it in patch] + \
                       [rot_poly(F_UP.difference(HOLES), it['rot'], it['x'], it['y']) for it in patch]
    rims = [rot_poly(F_UP.difference(HOLES).difference(POCKET), it['rot'], it['x'], it['y']) for it in patch]
    pd, sup = [], []
    for w in walls:
        pegs = rot_poly(PEGS, w['rot'], w['x'], w['y'])
        foot = rot_poly(W_FOOT, w['rot'], w['x'], w['y'])
        assert all(pegs.intersection(t).area < 1e-9 for t in tile_hole_layers)
        pd.append(min(pegs.distance(t) for t in tile_hole_layers))
        sup.append(sorted((foot.intersection(r).area for r in rims), reverse=True)[:2])
    res['gioco_minimo_piolo_foro_mm'] = round(min(pd), 4)
    res['appoggio_muro_sui_bordini_mm2'] = [[round(x, 2) for x in s] for s in sup]
    res['piolo_fondo_foro_mm'] = round((SPESSORE - PIOLO_H) - Z_HOLE, 3)
    ok &= min(pd) >= GIOCO_PIOLO - 0.01 and all(min(s) > 2 for s in sup) and res['piolo_fondo_foro_mm'] > 0
    v = (LATO * math.cos(math.radians(30)), LATO * math.sin(math.radians(30)))   # vertice a 30°: tre lati a 30, 150, 270°
    wy = [rot_poly(W_FOOT, a, v[0] + LATO / 2 * math.cos(math.radians(a)), v[1] + LATO / 2 * math.sin(math.radians(a)))
          for a in (30, 150, 270)]
    yov = sum(wy[a].intersection(wy[b]).area for a in range(3) for b in range(a + 1, 3))
    res['tre_muri_a_Y_sovrapposizione_mm2'] = round(yov, 9)
    res['tre_muri_a_Y_gioco_min_mm'] = round(min(wy[a].distance(wy[b]) for a in range(3) for b in range(a + 1, 3)), 4)
    ok &= yov < 1e-9
    # 4. carta e fori: la carta (tessere_mappa.pdf in scala) entra nella tasca e non copre i fori
    carta = hexagon(PASSO * CARTA_SCALA / 2)
    res['carta_ll_mm'] = round(PASSO * CARTA_SCALA, 3)
    res['carta_gioco_tasca_per_lato_mm'] = round((TASCA_LL - PASSO * CARTA_SCALA) / 2, 3)
    res['carta_sui_fori_mm2'] = round(carta.intersection(HOLES).area, 6)
    res['bordino_tasca_mm'] = round((PASSO - 2 * GIOCO - TASCA_LL) / 2, 3)
    ok &= POCKET.contains(carta) and carta.intersection(HOLES).area < 1e-9
    return ok, res


def min_wall_around_holes():
    """materiale minimo tra un mezzo foro e la coda di rondine del suo lato o il lato vicino (verso il vertice)."""
    out = []
    for i in range(6):
        coda = dovetail(i, 1 if TAB[i] else -1).buffer(GIOCO, join_style='mitre')
        for t in (-FORO_T, FORO_T):
            x, y = edge_pt(i, t, 0)
            h = stadium(x, y, PIOLO_L + 2 * GIOCO_PIOLO, PIOLO_W + 2 * GIOCO_PIOLO, 60 * i + 90)
            near = (i + (1 if t > 0 else -1)) % 6
            lato = LineString([edge_pt(near, -LATO / 2, -GIOCO), edge_pt(near, LATO / 2, -GIOCO)])
            out.append(min(h.distance(coda), h.distance(lato)))
    return min(out)


def main():
    patch = patch_layout()
    walls = walls_on_patch(patch)
    ok, res = checks_2d(patch, walls)
    res['parete_minima_intorno_ai_fori_mm'] = round(min_wall_around_holes(), 3)
    plate = plate_layout()
    pf = [placed_foot(it) for it in plate]
    res['piatto_ingombro_mm'] = [round(v, 2) for v in unary_union(pf).bounds]
    res['piatto_distanza_min_tra_pezzi_mm'] = round(min(pf[a].distance(pf[b]) for a in range(len(pf)) for b in range(a + 1, len(pf))), 3)
    ok &= res['piatto_distanza_min_tra_pezzi_mm'] >= 1.5 and box(0, 0, PIATTO, PIATTO).contains(unary_union(pf))
    print('CONTROLLI_2D', json.dumps(res, ensure_ascii=False))
    if not ok:
        sys.exit('controlli 2D falliti')

    spec = {
        'out': QUI,
        'solids': {'tessera': tile_spec(), 'muro': wall_spec()},
        'params': {'passo': PASSO, 'spessore': SPESSORE, 'z_pocket': Z_POCKET, 'muro_h': MURO_H, 'piolo_h': PIOLO_H},
        'patch': patch, 'walls': walls, 'pairs': neighbours(patch), 'plate': plate,
    }
    tmp = tempfile.mkdtemp(prefix='tessere3d-')
    try:
        sp = os.path.join(tmp, 'spec.json')
        with open(sp, 'w') as f:
            json.dump(spec, f)
        r = subprocess.run(['blender', '-b', '--factory-startup', '--python', os.path.join(QUI, 'blender_3d.py'), '--', sp],
                           capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l.startswith(('RESULT', 'SAVED', 'ERRORE')) or 'Error' in l or 'Traceback' in l]
        print('\n'.join(lines))
        if r.returncode != 0 or any(l.startswith('ERRORE') for l in lines):
            print(r.stderr[-3000:])
            sys.exit('Blender: errore')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    verify_files()


# ---- controllo indipendente dei file scritti ------------------------------------------------------------------
def read_stl(path):
    data = open(path, 'rb').read()
    n = int.from_bytes(data[80:84], 'little')
    a = np.frombuffer(data, dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n, offset=84)
    return a['v'].astype(np.float64)


def mesh_stats(tri):
    """tri: (n,3,3). Saldatura dei vertici, bordi usati esattamente 2 volte con versi opposti, volume, ingombro."""
    pts = np.round(tri.reshape(-1, 3), 4)
    _, idx = np.unique(pts, axis=0, return_inverse=True)
    f = idx.reshape(-1, 3)
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    und = np.sort(e, axis=1)
    _, cnt = np.unique(und, axis=0, return_counts=True)
    _, dcnt = np.unique(e, axis=0, return_counts=True)
    v = np.einsum('ij,ij->i', tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6
    return {'triangoli': len(tri), 'bordi_non_manifold': int((cnt != 2).sum()), 'bordi_orientati_doppi': int((dcnt != 1).sum()),
            'volume_mm3': round(v, 3), 'ingombro_mm': [round(x, 3) for x in (tri.reshape(-1, 3).max(0) - tri.reshape(-1, 3).min(0))]}


def verify_files():
    ok = True
    for name in ('tessera', 'muro', 'prova_3x3', 'piatto_20_tessere_8_muri'):
        s = mesh_stats(read_stl(os.path.join(QUI, name + '.stl')))
        with zipfile.ZipFile(os.path.join(QUI, name + '.3mf')) as z:
            root = ET.fromstring(z.read('3D/3dmodel.model'))
        ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        objs = root.findall('.//m:object', ns)
        ntri = sum(len(o.findall('.//m:triangle', ns)) for o in objs)
        s['3mf_oggetti'], s['3mf_triangoli'], s['3mf_unita'] = len(objs), ntri, root.get('unit')
        ok &= s['bordi_non_manifold'] == 0 and s['bordi_orientati_doppi'] == 0 and ntri == s['triangoli'] and s['volume_mm3'] > 0
        print('FILE', name, json.dumps(s, ensure_ascii=False))
    if not ok:
        sys.exit('controllo dei file fallito')
    print('TUTTO OK')


if __name__ == '__main__':
    main()
