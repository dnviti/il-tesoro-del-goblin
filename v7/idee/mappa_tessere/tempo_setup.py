#!/usr/bin/env python3
"""Analisi dei 10 preset di mappa del playtest v7 e modello del tempo di montaggio per pezzi di mappa più grandi.

Uso (dalla radice del repo):  python3 v7/idee/mappa_tessere/tempo_setup.py  [--dettagli]

Legge i dati veri dei 10 preset 10×10 (v7/simulatore/mappa.py e plance/*.py com'erano al commit af65ff0, prima della
mappa 12×12: se il simulatore è già passato al 12×12, li estrae da git in una cartella temporanea) e stampa in Markdown:
  1. analisi dei preset: esagoni, tile, muri, parti comuni e parti che cambiano, differenze tra preset;
  2. le opzioni di pezzo (tile singole di oggi, tri-esagoni, fiori da 7, quadranti, fasce, plancia neutra + toppe):
     pezzi per partita, disegni distinti, pezzi da stampare, fogli, muri a parte;
  3. le combinazioni libere di fasce e quadranti controllate come i preset (strada collegata, >= 2 uscite, nessun
     esagono che isola una zona, 3 ingressi per Cripta, Partenza->Cripta);
  4. il modello del tempo (montaggio e cambio di mappa a metà partita, R 8.12) con giocatore veloce/tipico/lento,
     1 o 2 persone.
Ogni costante del modello sta in COSTANTI con la sua fonte. Niente viene scritto su disco.
"""
import collections
import functools
import itertools
import math
import os
import runpy
import statistics
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.normpath(os.path.join(QUI, '..', '..'))
sys.dont_write_bytecode = True
sys.path.insert(0, QUI)
REVISIONE_10X10 = 'af65ff0'   # ultimo commit con la mappa 10×10 nel simulatore (11/11/2026)


def _simulatore_10x10():
    """cartella con il simulatore della mappa 10×10: quello del repo se è ancora 10×10, altrimenti estratto da git."""
    sim = os.path.join(V7, 'simulatore')
    if '_STRADA' in open(os.path.join(sim, 'mappa.py'), encoding='utf-8').read():
        return sim
    import subprocess
    import tempfile
    import atexit
    import shutil
    dove = tempfile.mkdtemp(prefix='goblin_mappa10x10_')
    atexit.register(shutil.rmtree, dove, True)
    os.makedirs(os.path.join(dove, 'plance'))
    radice = subprocess.run(['git', '-C', V7, 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()
    nomi = subprocess.run(['git', '-C', radice, 'ls-tree', '--name-only', REVISIONE_10X10, 'v7/simulatore/plance/'],
                          capture_output=True, text=True, check=True).stdout.split()
    for f in ['v7/simulatore/mappa.py'] + nomi:
        testo = subprocess.run(['git', '-C', radice, 'show', f'{REVISIONE_10X10}:{f}'], capture_output=True, text=True, check=True).stdout
        with open(os.path.join(dove, f.split('v7/simulatore/', 1)[1]), 'w', encoding='utf-8') as fh:
            fh.write(testo)
    return dove


SIMULATORE_10X10 = _simulatore_10x10()
sys.path.insert(0, SIMULATORE_10X10)
import mappa  # noqa: E402  geometria (_vicini_geo), Partenze, Cripte, «?», elenco dei temi (mappa 10×10)

COL = 'ABCDEFGHIJ'
TUTTI = [f'{c}{r}' for r in range(1, 11) for c in COL]
STRADE = {'strada', 'guado', 'ponte', '?'}
PONTI = {'F5', 'E6'}   # il Ponte del lago F5–E6 (R 8.2); D5 e G6 sono guadi


# ------------------------------------------------------------------ dati dei preset
def carica(path):
    d = runpy.run_path(path)
    t = {h: 'strada' for h in d['_STRADA'].split()}
    t.update({h: ('ponte' if h in PONTI else 'guado') for h in d['_GUADI'].split()})
    for k in ('BOSCO', 'CASE', 'ROCCE', 'ACQUA'):
        t.update({h: k.lower() for h in d[k].split()})
    t.update({h: '?' for h in d['DOMANDE']})
    t.update({h: f'P{n}' for n, h in d['PARTENZE'].items()})
    t.update({h: f'C{n}' for n, h in d['CRIPTE'].items()})
    assert set(t) == set(TUTTI), path
    return t, {frozenset(m.split('|')) for m in d['_MURI'].split()}


PRESET = {'base': carica(os.path.join(SIMULATORE_10X10, 'mappa.py'))}
PRESET.update({tm: carica(os.path.join(SIMULATORE_10X10, 'plance', te + '.py')) for tm, te in mappa.TEMI.items()})
NOMI = list(PRESET)
TERRA = ('bosco', 'case', 'rocce')


def strada(t):
    return t in STRADE or t[0] in 'PC'


def ruota(h):
    """esagono girato di 180° (i preset sono identici così, R 8.2)."""
    c, r = COL.index(h[0]), int(h[1:])
    return f'{COL[9 - c]}{11 - r}'


# coordinate assiali: q = colonna - floor((riga-1)/2), r = riga-1 (righe dispari spostate a sinistra, Spec §17)
AX = {h: (COL.index(h[0]) - (int(h[1:]) - 1) // 2, int(h[1:]) - 1) for h in TUTTI}
HX = {v: k for k, v in AX.items()}
D6 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
for _h in TUTTI:   # le coordinate assiali danno gli stessi vicini di mappa._vicini_geo
    assert {HX[(AX[_h][0] + a, AX[_h][1] + b)] for a, b in D6 if (AX[_h][0] + a, AX[_h][1] + b) in HX} == set(mappa._vicini_geo(_h))


def vicini(h):
    return mappa._vicini_geo(h)


# ------------------------------------------------------------------ controlli (gli stessi del §17)
def controlla(t, muri):
    s = {h for h in TUTTI if strada(t[h])}
    vic = {h: [v for v in vicini(h) if v in s and frozenset((h, v)) not in muri] for h in s}

    def bfs(da, tolto=None):
        dist = {da: 0}
        coda = collections.deque([da])
        while coda:
            x = coda.popleft()
            for v in vic[x]:
                if v != tolto and v not in dist:
                    dist[v] = dist[x] + 1
                    coda.append(v)
        return dist

    tagli = sum(1 for b in s if len(bfs(next(x for x in s if x != b), b)) < len(s) - 1)
    part, cri = list(mappa.PARTENZE.values()), list(mappa.CRIPTE.values())
    dist = {p: bfs(p) for p in part}
    dd = [dist[p].get(c, 99) for p in part for c in cri]
    return {'collegata': len(bfs(next(iter(s)))) == len(s), 'uscite_min': min(map(len, vic.values())),
            'tagli': tagli, 'ingressi': [len(vic[c]) for c in cri], 'pc_min': min(dd), 'pc_max': max(dd),
            'vicina': {min(dist[p].get(c, 99) for c in cri) for p in part}}


def valida(c):
    return c['collegata'] and c['uscite_min'] >= 2 and c['tagli'] == 0 and c['ingressi'] == [3, 3, 3, 3]


# ------------------------------------------------------------------ 1. analisi dei preset
FISSI = [h for h in TUTTI if len({PRESET[k][0][h] for k in NOMI}) == 1]
VARIABILI = [h for h in TUTTI if h not in FISSI]
MURI_FISSI = set.intersection(*[m for _, m in PRESET.values()])
MURI_TUTTI = set.union(*[m for _, m in PRESET.values()])


def differenze(a, b):
    ta, tb = PRESET[a][0], PRESET[b][0]
    celle = [h for h in TUTTI if ta[h] != tb[h]]
    return {'celle': len(celle), 'muri_via': len(PRESET[a][1] - PRESET[b][1]), 'muri_su': len(PRESET[b][1] - PRESET[a][1]),
            'aggiungi': sum(strada(ta[h]) for h in celle), 'togli': sum(strada(tb[h]) for h in celle),
            'scambia': sum(not strada(ta[h]) and not strada(tb[h]) for h in celle)}


# ------------------------------------------------------------------ 2. opzioni di pezzo
def ruota60(p):
    """rotazione di 60° in coordinate assiali: cubo (x, y, z) -> (-z, -x, -y), con (q, r) = (x, z)."""
    q, r = p
    return -r, q + r



def canonico(celle):
    """contenuto di un pezzo a meno di traslazioni e rotazioni di 60°: due pezzi uguali sono lo stesso disegno."""
    best, cur = None, celle
    for _ in range(6):
        q0, r0 = min(p for p, _ in cur)
        n = tuple(sorted(((p[0] - q0, p[1] - r0), lab) for p, lab in cur))
        best = n if best is None or n < best else best
        cur = [(ruota60(p), lab) for p, lab in cur]
    return best


def tri(off):
    """tassellatura in tri-esagoni a triangolo (3 esagoni attorno a un vertice); ai bordi restano pezzi da 1-2."""
    g = collections.defaultdict(list)
    for h, (q, r) in AX.items():
        m = (q - r + off) % 3
        g[{0: (q, r), 1: (q - 1, r), 2: (q, r - 1)}[m]].append(h)
    return list(g.values())


def fiori(off, segno):
    """tassellatura in fiori da 7 (centro + 6): (q + 3r) mod 7 distingue un esagono e i suoi 6 vicini."""
    g = collections.defaultdict(list)
    for h, (q, r) in AX.items():
        f = lambda a, b: ((a + 3 * b) * segno + off) % 7  # noqa: E731
        g[(q, r) if f(q, r) == 0 else next((q + a, r + b) for a, b in D6 if f(q + a, r + b) == 0)].append(h)
    return list(g.values())


def disegni(partizione):
    """(pezzi per partita, disegni distinti, pezzi da stampare): per ogni disegno il massimo di copie in un preset."""
    copie = collections.defaultdict(int)
    for k in NOMI:
        c = collections.Counter(canonico([(AX[h], PRESET[k][0][h]) for h in pezzo]) for pezzo in partizione)
        for d, n in c.items():
            copie[d] = max(copie[d], n)
    return len(partizione), len(copie), sum(copie.values())


def migliore(partizioni):
    return min(partizioni, key=lambda p: (disegni(p)[1], len(p)))


REG_FASCE = {h: 'N' if int(h[1:]) <= 4 else 'C' if int(h[1:]) <= 6 else 'S' for h in TUTTI}
REG_QUAD = {h: ('N' if int(h[1:]) <= 5 else 'S') + ('O' if COL.index(h[0]) <= 4 else 'E') for h in TUTTI}


def padrone_fasce(w):
    s = {REG_FASCE[h] for h in w}
    return 'N' if 'N' in s else 'S' if 'S' in s else 'C'   # un muro sul taglio si stampa sulla fascia


def padrone_quad(w):
    s = {REG_QUAD[h] for h in w}
    return s.pop() if len(s) == 1 else ('NO' if 'NO' in s else 'SE' if 'SE' in s else sorted(s)[0])


def componi(reg, padrone, scelta):
    """mappa fatta di pezzi presi da preset diversi: ogni zona `reg` viene dal preset scelta[zona]."""
    t = {h: PRESET[scelta[reg[h]]][0][h] for h in TUTTI}
    return t, {w for w in MURI_TUTTI if w in PRESET[scelta[padrone(w)]][1]}


def toppe(t, massimo=3):
    """minimo numero di toppe (pezzi da 1..massimo esagoni dello stesso terreno, collegati) che coprono la terra."""
    def migliore_copertura(celle):
        @functools.lru_cache(None)
        def vai(resto):
            if not resto:
                return 0, ()
            h, best = min(resto), None
            sotto, fronte = {frozenset([h])}, {frozenset([h])}
            for _ in range(massimo - 1):
                fronte = {s | {v} for s in fronte for x in s for v in vicini(x) if v in resto and v not in s}
                sotto |= fronte
            for s in sorted(sotto, key=sorted):   # ordine fisso: stesso risultato a ogni esecuzione
                n, pz = vai(resto - s)
                if best is None or n + 1 < best[0]:
                    best = (n + 1, pz + (tuple(sorted(s)),))
            return best
        return vai(frozenset(celle))
    out = []
    for terr in TERRA:
        out += [(terr, forma(p)) for p in migliore_copertura([h for h in TUTTI if t[h] == terr])[1]]
    return out


def forma(celle):
    """nome della forma di una toppa da 1-3 esagoni."""
    if len(celle) < 3:
        return ('singola', 'doppia')[len(celle) - 1]
    lati = sum(b in vicini(a) for a, b in itertools.combinations(celle, 2))
    if lati == 3:
        return 'triangolo'
    mezzo = next(h for h in celle if sum(v in celle for v in vicini(h)) == 2)
    (qa, ra), (qb, rb) = (AX[h] for h in celle if h != mezzo)
    qm, rm = AX[mezzo]
    return 'dritta' if (qm - qa, rm - ra) == (qb - qm, rb - rm) else 'curva'


# ------------------------------------------------------------------ 3. modello del tempo (modello_tempi.py)
from modello_tempi import COSTANTI, PROFILI, k, fitts, hick, ricerca_unici, pezzo, montaggio  # noqa: E402,F401


# ------------------------------------------------------------------ le opzioni
def opzioni():
    """[(sigla, nome, dati)] con le voci di montaggio e di cambio mappa per ogni opzione."""
    muri = len(PRESET['base'][1])
    out = []
    # 0. tile singole di oggi
    dif = [differenze('base', x) for x in NOMI[1:]]
    cambio0 = statistics.mean(d['celle'] for d in dif)
    muri0 = statistics.mean(d['muri_via'] + d['muri_su'] for d in dif)
    out.append(('0', 'Tile singole (oggi)', dict(
        pezzi=100, muri=muri, disegni=18, stampa=162, fogli_a4=3, fogli_a3=2, mm='25,2 (esagono)', preset='tutti, esatti',
        voci=[('tile', 100, {'pile': 10}), ('muro', muri, {})],
        cambio=lambda p: cambio0 * (k('togli', p) + pezzo('tile', p, pile=10)) + muri0 * k('togli', p) / 2
        + muri0 / 2 * pezzo('muro', p))))
    # A. tri-esagoni esatti (con i muri a parte, come oggi)
    pa = migliore([tri(o) for o in range(3)])
    n, d, st = disegni(pa)
    camb = statistics.mean(sum(any(PRESET['base'][0][h] != PRESET[x][0][h] for h in pz) for pz in pa) for x in NOMI[1:])
    gett = statistics.mean(sum(1 for pz in pa if any(PRESET['base'][0][h] != PRESET[x][0][h] for h in pz)
                               for h in pz if PRESET['base'][0][h] == '?') for x in NOMI[1:])
    out.append(('A', 'Tri-esagoni (triangolo di 3)', dict(
        pezzi=n, muri=muri, disegni=d, stampa=st, fogli_a4=math.ceil(st * 3 / 45), fogli_a3=math.ceil(st * 3 / 100),
        mm='50 × 51', preset='tutti, esatti (ma ogni preset ha i suoi pezzi)',
        voci=[('medio', n, {'unici': n}), ('muro', muri, {})],
        cambio=lambda p, c=camb, g=gett: c * (k('togli', p) + pezzo('medio', p, unici=c)) + g * k('gettone', p)
        + muri0 * (k('togli', p) / 2 + pezzo('muro', p) / 2))))
    # B. fiori da 7
    pb = migliore([fiori(o, s) for o in range(7) for s in (1, -1)])
    n, d, st = disegni(pb)
    camb = statistics.mean(sum(any(PRESET['base'][0][h] != PRESET[x][0][h] for h in pz) for pz in pb) for x in NOMI[1:])
    gett = statistics.mean(sum(1 for pz in pb if any(PRESET['base'][0][h] != PRESET[x][0][h] for h in pz)
                               for h in pz if PRESET['base'][0][h] == '?') for x in NOMI[1:])
    out.append(('B', 'Fiori da 7 (+ pezzi di bordo)', dict(
        pezzi=n, muri=muri, disegni=d, stampa=st, fogli_a4=math.ceil(st * 4.6 / 42), fogli_a3=math.ceil(st * 4.6 / 95),
        mm='76 × 73 (fiore intero)', preset='tutti, esatti (ma ogni preset ha i suoi pezzi)',
        voci=[('medio', n, {'unici': n}), ('muro', muri, {})],
        cambio=lambda p, c=camb, g=gett: c * (k('togli', p) + pezzo('medio', p, unici=c)) + g * k('gettone', p)
        + muri0 * (k('togli', p) / 2 + pezzo('muro', p) / 2))))
    # C. quadranti 5 × 5 (muri stampati)
    out.append(('C', 'Quadranti 5 × 5 (25 esagoni)', dict(
        pezzi=4, muri=0, disegni=20, stampa=40, fogli_a4=20, fogli_a3=7, mm='139 × 116', preset='tutti, esatti',
        voci=[('grande', 4, {'pile': 20})],
        cambio=lambda p: 4 * (k('togli', p) + pezzo('grande', p, pile=20)) + 20 * k('gettone', p))))
    # D. fasce: nord (righe 1-4) + fiume (5-6) + sud (7-10) = nord girata
    gett_d = sum(1 for h in mappa.DOMANDE if REG_FASCE[h] != 'C')
    out.append(('D', 'Fasce: 2 fasce del preset + fiume', dict(
        pezzi=3, muri=0, disegni=12, stampa=22, fogli_a4=11, fogli_a3=6, mm='fascia 265 × 95; fiume 265 × 51',
        preset='tutti, esatti',
        voci=[('grande', 3, {'pile': 11})],
        cambio=lambda p: 2 * (k('togli', p) + pezzo('grande', p, pile=11)) + gett_d * k('gettone', p))))
    # E1. plancia neutra (fasce con le 44 caselle variabili stampate come strada, fiume senza mura libere) + i 28 ostacoli
    #     di terra come toppe = le tile singole che ci sono già + 6 mura libere a listello
    libere = len(PRESET['base'][1] - MURI_FISSI)
    dif = [differenze('base', x) for x in NOMI[1:]]
    agg, tog, sca = (statistics.mean(d[c] for d in dif) for c in ('aggiungi', 'togli', 'scambia'))
    mur = statistics.mean(d['muri_via'] for d in dif)
    out.append(('E1', 'Plancia neutra + tile di oggi come toppe', dict(
        pezzi=3 + 28, muri=libere, disegni='2 + tile di oggi', stampa='3 + tile di oggi', fogli_a4=2, fogli_a3=1,
        mm='plancia come D; toppe 25,2', preset='tutti, esatti',
        voci=[('grande', 3, {'pile': 2}), ('toppa', 28, {'pile': 3}), ('muro', libere, {})],
        cambio=lambda p: (agg + sca) * pezzo('toppa', p, pile=3) + (tog + sca) * k('togli', p)
        + mur * (k('togli', p) + pezzo('muro', p)))))
    # E2. come E1 ma con toppe sagomate da 1-3 esagoni dello stesso terreno (meno pezzi, più forme)
    tp = {x: toppe(PRESET[x][0]) for x in NOMI}
    ntop = statistics.mean(len(v) for v in tp.values())
    inv = collections.defaultdict(int)
    for v in tp.values():
        for key, c in collections.Counter(v).items():
            inv[key] = max(inv[key], c)
    out.append(('E2', 'Plancia neutra + toppe sagomate 1-3 esagoni', dict(
        pezzi=3 + round(ntop), muri=libere, disegni=2 + len(inv), stampa=3 + sum(inv.values()), fogli_a4=2 + 2,
        fogli_a3=1 + 1, mm='plancia come D; toppe 25-51', preset='tutti, esatti',
        toppe=(min(len(v) for v in tp.values()), max(len(v) for v in tp.values()), dict(inv)),
        voci=[('grande', 3, {'pile': 2}), ('toppa', round(ntop), {'pile': len(inv)}), ('muro', libere, {})],
        cambio=lambda p: round(ntop) * (k('togli', p) + pezzo('toppa', p, pile=len(inv)))
        + mur * (k('togli', p) + pezzo('muro', p)))))
    return out


# ------------------------------------------------------------------ stampa
def mm_ss(s):
    s = round(s)
    return f'{s // 60}:{s % 60:02d}'


def tab(righe, intest):
    print('| ' + ' | '.join(intest) + ' |')
    print('|' + '---|' * len(intest))
    for r in righe:
        print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print()


def main():
    dettagli = '--dettagli' in sys.argv
    print('## 1. I 10 preset\n')
    righe = []
    for x in NOMI:
        t, m = PRESET[x]
        c = collections.Counter(t.values())
        righe.append((x, 100, sum(strada(v) for v in t.values()), c['bosco'], c['case'], c['rocce'], c['acqua'], len(m),
                      len(m - MURI_FISSI), 'sì' if valida(controlla(t, m)) else 'NO'))
    tab(righe, ('preset', 'esagoni = tile', 'strada', 'bosco', 'case', 'rocce', 'acqua', 'muri', 'di cui mura libere', 'controlli §17'))
    print(f'Esagoni uguali in tutti i 10 preset: **{len(FISSI)}**; che cambiano in almeno un preset: **{len(VARIABILI)}** '
          f'({len([h for h in VARIABILI if int(h[1:]) <= 4])} nelle righe 1-4, {len([h for h in VARIABILI if int(h[1:]) >= 7])} '
          f'nelle righe 7-10, {len([h for h in VARIABILI if 5 <= int(h[1:]) <= 6])} nelle righe 5-6).')
    print(f'Muri: {len(MURI_FISSI)} uguali dappertutto (Cripte), {len(MURI_TUTTI - MURI_FISSI)} posizioni diverse di mura libere nei 10 preset.\n')
    print('```')
    for r in range(1, 11):
        print(('  ' if r % 2 == 0 else '') + '   '.join(('X' if h in VARIABILI else '·') for h in [f'{c}{r}' for c in COL]))
    print('```\n')
    righe = []
    for x in NOMI[1:]:
        d = differenze('base', x)
        righe.append((x, d['celle'], d['aggiungi'], d['togli'], d['scambia'], d['muri_via'], d['muri_su']))
    tab(righe, ('base →', 'esagoni diversi', 'strada→ostacolo', 'ostacolo→strada', 'ostacolo→altro ostacolo', 'mura via', 'mura su'))
    cop = [differenze(a, b)['celle'] for a, b in itertools.permutations(NOMI, 2)]
    print(f'Tra due preset qualsiasi cambiano da {min(cop)} a {max(cop)} esagoni (media {statistics.mean(cop):.1f}).\n')

    print('## 2. Combinazioni libere\n')
    ok = collections.Counter()
    for a, b in itertools.product(NOMI, repeat=2):
        for centro in ('base', 'TM-08'):
            c = controlla(*componi(REG_FASCE, padrone_fasce, {'N': a, 'S': b, 'C': centro}))
            ok[(valida(c), c['vicina'] == {4} and (c['pc_min'], c['pc_max']) == (4, 8))] += 1
    print(f'Fasce (nord di un preset, sud di un altro, fiume con o senza le 2 mura): {sum(v for (x, _), v in ok.items() if x)} '
          f'valide su {sum(ok.values())}; di queste {ok[(True, True)]} hanno anche la Cripta più vicina a 4 passi da ogni '
          'Partenza e Partenza→Cripta da 4 a 8, come i preset.')
    ok = collections.Counter()
    for a, b, c, d in itertools.product(NOMI, repeat=4):
        ok[valida(controlla(*componi(REG_QUAD, padrone_quad, {'NO': a, 'NE': b, 'SO': c, 'SE': d})))] += 1
    print(f'Quadranti (4 quadranti da preset qualsiasi): {ok[True]} valide su {sum(ok.values())}.\n')

    print('## 3. Opzioni e tempi\n')
    ops = opzioni()
    righe = []
    for s, nome, o in ops:
        tm = [montaggio(o['voci'], p) for p in PROFILI]
        t2 = [montaggio(o['voci'], p, 2) for p in PROFILI]
        cm = [o['cambio'](p) for p in PROFILI]
        rd = [(o['pezzi'] + o['muri']) * k('togli', p) for p in PROFILI]
        righe.append((s, nome, o['pezzi'], o['muri'], o['disegni'], o['stampa'], f"{o['fogli_a4']} / {o['fogli_a3']}", o['mm'],
                      f'{mm_ss(tm[0])}–**{mm_ss(tm[1])}**–{mm_ss(tm[2])}', f'{mm_ss(t2[0])}–**{mm_ss(t2[1])}**–{mm_ss(t2[2])}',
                      f'{mm_ss(cm[0])}–**{mm_ss(cm[1])}**–{mm_ss(cm[2])}', f'{mm_ss(rd[0])}–**{mm_ss(rd[1])}**–{mm_ss(rd[2])}'))
    tab(righe, ('', 'opzione', 'pezzi/partita', 'muri a parte', 'disegni', 'pezzi da stampare', 'fogli A4 / A3', 'misura mm',
                'montaggio 1 persona (veloce–tipico–lento)', '2 persone', 'cambio mappa R 8.12 (base→TM, media)',
                'riordino a fine partita'))
    seg = COSTANTI['segnalini'][0]
    print(f'Esclusi da tutte le righe (uguali per ogni opzione): tessere Esplorazione sulle 20 «?» {seg[0]}–{seg[1]}–{seg[2]} s; '
          'pedine degli eroi.')
    e = next(o for s, _, o in ops if s == 'E2')
    print(f"Toppe per preset (opzione E2): da {e['toppe'][0]} a {e['toppe'][1]}; scorta = massimo per tipo: {e['toppe'][2]}.\n")
    if dettagli:
        print('## 4. Costanti\n')
        tab([(n, ' / '.join(str(v) for v in val), f) for n, (val, f) in COSTANTI.items()], ('costante', 'veloce / tipico / lento', 'fonte'))
        for s, nome, o in ops:
            print(f'- {s} {nome}: ' + ', '.join(f'{t} ×{n} = {pezzo(t, "tipico", **kw):.1f} s' for t, n, kw in o['voci']))


if __name__ == '__main__':
    main()
