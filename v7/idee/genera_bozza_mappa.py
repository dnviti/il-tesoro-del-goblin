#!/usr/bin/env python3
"""Genera la bozza della plancia v7 (v7/idee/v7_bozza_mappa.svg) dai dati della plancia.

I dati vengono da un modulo Python (di default v7/simulatore/mappa.py, l'unica fonte dei dati) che definisce:
  _STRADA, _GUADI           stringhe di coordinate separate da spazi ("C1 D1 ..."): strada e guadi/ponti
  BOSCO, CASE, ROCCE, ACQUA stringhe di coordinate separate da spazi: i quattro tipi di ostacolo
  _MURI                     stringa di coppie "D3|D4 D4|E3 ...": un muro sul lato comune delle due caselle
  PARTENZE, CRIPTE          dict numero -> casella
  DOMANDE                   sequenza delle caselle «?»
Vicini (Spec_v7.md §17) da mappa._vicini_geo; i muri chiudono il lato su cui stanno. Legenda e «Controlli calcolati»
si calcolano dai dati. Prima di scrivere controlla che ogni casella sia una sola tra strada, guado e ostacolo e che la
plancia girata di 180° sia identica.

Con --tema TEMA ogni esagono è riempito dalla sua tessera illustrata (arte/png/PT-<TEMA>-<TERRENO>-<n>.png, 360 px
= 30,48 mm a 300 ppi sulla plancia in scala 0,97, ritagliata a esagono; la variante -1/-2 dipende dalla coordinata;
se la -2 manca si usa la -1 specchiata) e la fascia della Sala del Tesoro ha sotto PS-<TEMA>.png schiarita; senza
--tema l'aspetto è quello piatto. Le immagini sono collegate con un percorso relativo alla cartella dell'SVG scritto
(svg.py board() le riporta alla cartella delle pagine di stampa); --arte CARTELLA le prende da un'altra cartella.
--senza-linee toglie le linee di strada tra le caselle collegate.

Uso: python3 genera_bozza_mappa.py [--dati FILE.py] [--out FILE.svg] [--tema TEMA] [--arte CARTELLA] [--senza-linee]
"""
import argparse
import importlib.util
import math
import os
import sys
import zlib
from collections import deque
from html import escape

QUI = os.path.dirname(os.path.abspath(__file__))
SIMULATORE = os.path.join(QUI, '..', 'simulatore')
sys.dont_write_bytecode = True   # niente __pycache__ in simulatore/
sys.path.insert(0, SIMULATORE)
from mappa import _cr, _nome, _vicini_geo  # noqa: E402  geometria della griglia (Spec_v7.md §17)

DATI = os.path.join(SIMULATORE, 'mappa.py')
OUT = os.path.join(QUI, 'v7_bozza_mappa.svg')
CAMPI = ('_STRADA', '_GUADI', '_MURI', 'BOSCO', 'CASE', 'ROCCE', 'ACQUA', 'PARTENZE', 'CRIPTE', 'DOMANDE')
TUTTI = [_nome(c, r) for r in range(1, 11) for c in range(10)]

# griglia e cornice della plancia v6 (come svg.py board()): 10 x 10 esagoni, W = 26
W = 26.0
R = W / math.sqrt(3)
PASSO = 1.5 * R
PAD, TOP, BOTTOM = W * 1.8, W * 4.5, W * 4.3
BW = W * 10.5 + 2 * PAD
BH = 9 * PASSO + 2 * R + TOP + BOTTOM
LX = BW + 10   # legenda a destra: x del riquadro

# tessere illustrate (--tema): PhotoCraft, 360 x 360 px = 30,48 mm a 300 ppi; la plancia si stampa in scala 0,97
ARTE = os.path.join(QUI, '..', 'stampa', 'sorgenti', 'arte', 'png')
TESSERA = 30.48 / 0.97          # lato della tessera in unità del disegno: copre l'esagono (2R = 30,0) a 300 ppi
VARIANTI = {'STRADA': 2, 'BOSCO': 2, 'CASE': 2, 'ROCCE': 2, 'ACQUA': 1, 'GUADO': 1, 'PARTENZA': 1, 'CRIPTA': 1}
SALA_PX = (4200, 1191)          # PS-<TEMA>.png: fascia della Sala del Tesoro, tutta la larghezza della plancia
SALA_H = BW * SALA_PX[1] / SALA_PX[0]

INK, BROWN = '#2a2118', '#6b4a2b'
STRADA_COL, GUADO_COL, BORDO = '#f5e9c9', '#cfe2ee', '#b9a582'
LINEA = '#c9a26a'
MURO = 'stroke="#3a2a1c" stroke-width="3.2" stroke-linecap="round"'
GRIGLIA = f'fill="none" stroke="{INK}" stroke-opacity="0.45" stroke-width="0.5"'   # contorno sottile delle tessere
ALONE = '#fffaf0'   # alone chiaro sotto muri e scritte sopra le tessere


def carica_dati(path):
    spec = importlib.util.spec_from_file_location('dati_plancia', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    manca = [c for c in CAMPI if not hasattr(mod, c)]
    if manca:
        sys.exit(f'{path}: mancano {", ".join(manca)} (servono {", ".join(CAMPI)})')
    return mod


# ---------- geometria ----------
def centro(h):
    c, r = _cr(h)
    return PAD + W * (c + 0.5 + (0.5 if r % 2 == 0 else 0)), TOP + R + (r - 1) * PASSO


def vertici(x, y, s):
    return [(x + s * math.cos(math.radians(a)), y + s * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]


def punti(x, y, s):
    return ' '.join(f'{px:.2f},{py:.2f}' for px, py in vertici(x, y, s))


def pp(x, y, off):
    return ' '.join(f'{x + dx:.2f},{y + dy:.2f}' for dx, dy in off)


def simmetrico(h):
    c, r = _cr(h)
    return _nome(9 - c, 11 - r)


def lato_comune(a, b):
    va = vertici(*centro(a), R)
    comuni = [p for p in vertici(*centro(b), R) if any(math.dist(p, q) < 1e-6 for q in va)]
    assert len(comuni) == 2, f'muro {a}|{b}: le caselle non sono vicine'
    return comuni


# ---------- icone dei terreni (centrate in x, y) ----------
def ic_bosco(x, y):
    return ''.join(f'<rect x="{tx - 0.8:.2f}" y="{ty + 1:.2f}" width="1.60" height="3.00" fill="#6b4a2b"/>'
                   f'<circle cx="{tx:.2f}" cy="{ty:.2f}" r="3.60" fill="#4f7a3a"/>'
                   for tx, ty in ((x - 5, y - 3), (x + 5, y - 3), (x, y + 4)))


def ic_case(x, y):
    return (f'<rect x="{x - 5:.2f}" y="{y - 1:.2f}" width="10.00" height="7.00" fill="#f4ead5" stroke="#7a3b22" stroke-width="0.8"/>'
            f'<polygon points="{pp(x, y, ((-7, -1), (0, -8), (7, -1)))}" fill="#9c4a2b"/>'
            f'<rect x="{x - 1.5:.2f}" y="{y + 2:.2f}" width="3.00" height="4.00" fill="#7a3b22"/>')


def ic_rocce(x, y):
    return (f'<polygon points="{pp(x, y, ((-9, 5), (-5, -4), (1, -6), (3, 5)))}" fill="#8a847a" stroke="#5e5950" stroke-width="0.6"/>'
            f'<polygon points="{pp(x, y, ((1, 6), (5, -1), (9, 1), (9, 6)))}" fill="#a29c92" stroke="#5e5950" stroke-width="0.6"/>')


def ic_acqua(x, y):
    return ''.join(f'<path d="M{x - 8:.2f} {y + dy:.2f} q2 -2.5 4 0 t4 0 t4 0 t4 0" fill="none" stroke="#3d6f96" stroke-width="1"/>'
                   for dy in (-4, 2))


def ic_guado(x, y):
    return ''.join(f'<rect x="{x + dx:.2f}" y="{y - 7:.2f}" width="3" height="14" fill="#a07a4a" stroke="#6b4a2b" stroke-width="0.4"/>'
                   for dx in (-7.5, -3.5, 0.5, 4.5))


def q_mark(x, y, r):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fffaf0" stroke="{INK}" stroke-width="1.3"/>'
            f'<text x="{x:.2f}" y="{y + r * 0.55:.2f}" text-anchor="middle" font-weight="800" font-size="{r * 1.5:.2f}" fill="{INK}">?</text>')


# tipo: (campo del modulo dati, colore, icona, titolo in legenda, riga di spiegazione)
TIPI = {
    'bosco': ('BOSCO', '#a9c98f', ic_bosco, 'Bosco', 'Impraticabile: non ci si entra e non si attraversa.'),
    'case': ('CASE', '#e2cfb2', ic_case, 'Case del villaggio', 'Impraticabili.'),
    'rocce': ('ROCCE', '#cfcac1', ic_rocce, 'Rocce', 'Impraticabili.'),
    'acqua': ('ACQUA', '#a7cbe3', ic_acqua, 'Acqua: fiume e lago', 'Impraticabile; divide la plancia in metà nord e sud.'),
}


# ---------- dati e controlli ----------
def prepara(d):
    strada, guadi = d._STRADA.split(), d._GUADI.split()
    tipo = {}
    for t, (campo, *_) in TIPI.items():
        for h in getattr(d, campo).split():
            assert h not in tipo, f'{h} ha due tipi di ostacolo ({tipo[h]}, {t})'
            tipo[h] = t
    caselle = strada + guadi + list(tipo)
    assert set(caselle) <= set(TUTTI), f'caselle fuori plancia: {sorted(set(caselle) - set(TUTTI))}'
    doppie = sorted({h for h in caselle if caselle.count(h) > 1})
    assert not doppie, f'caselle con più di un tipo tra strada, guado e ostacolo: {doppie}'
    mancanti = sorted(set(TUTTI) - set(caselle), key=TUTTI.index)
    assert not mancanti, f'caselle senza tipo (gli ostacoli devono coprire tutto ciò che non è strada): {mancanti}'

    strada_tutta = frozenset(strada + guadi)
    muri = [frozenset(m.split('|')) for m in d._MURI.split()]
    assert len(set(muri)) == len(muri), 'muri ripetuti'
    for m in muri:
        lato_comune(*m)
    vicini = {h: tuple(v for v in _vicini_geo(h) if v in strada_tutta and frozenset((h, v)) not in muri)
              for h in strada_tutta}
    partenze, cripte, domande = dict(sorted(d.PARTENZE.items())), dict(sorted(d.CRIPTE.items())), tuple(d.DOMANDE)
    for nome, hh in (('Partenze', partenze.values()), ('Cripte', cripte.values()), ('«?»', domande)):
        assert set(hh) <= strada_tutta, f'{nome} fuori strada: {sorted(set(hh) - strada_tutta)}'
    assert len(set(domande)) == len(domande), 'caselle «?» ripetute'

    def gira(hh):
        return {simmetrico(h) for h in hh}
    for nome, hh in [('strada', strada), ('guadi', guadi), ('Partenze', partenze.values()),
                     ('Cripte', cripte.values()), ('«?»', domande)] + \
            [(t, [h for h in tipo if tipo[h] == t]) for t in TIPI]:
        assert gira(hh) == set(hh), f'{nome}: la plancia girata di 180° non è identica'
    assert {frozenset(gira(m)) for m in muri} == set(muri), 'muri: la plancia girata di 180° non è identica'
    assert len(bfs(vicini, strada[0])) == len(strada_tutta), 'la strada non è tutta collegata'
    return dict(strada=strada_tutta, guadi=frozenset(guadi), tipo=tipo, muri=muri, vicini=vicini,
                partenze=partenze, cripte=cripte, domande=domande)


def bfs(vicini, da, tolti=frozenset()):
    dist = {da: 0}
    coda = deque([da])
    while coda:
        h = coda.popleft()
        for v in vicini[h]:
            if v not in dist and v not in tolti:
                dist[v] = dist[h] + 1
                coda.append(v)
    return dist


def num(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.').replace('.', ',')


def intervallo(vv):
    return str(min(vv)) if min(vv) == max(vv) else f'{min(vv)}–{max(vv)}'


def controlli(p):
    """righe dei «Controlli calcolati su questa bozza»."""
    strada, vicini = p['strada'], p['vicini']
    dist = {h: bfs(vicini, h) for h in strada}
    ciechi = [h for h in TUTTI if h in strada and len(vicini[h]) <= 1]
    articolazioni = [b for b in TUTTI if b in strada
                     and len(bfs(vicini, next(iter(strada - {b})), {b})) < len(strada) - 1]
    # deviazione: passi in più da una Partenza a una Cripta con un mostro scoperto su un'altra casella di strada
    deviazione, isolate = 0, False
    for a in p['partenze'].values():
        for b in strada - {a}:
            da = bfs(vicini, a, {b})
            for c in p['cripte'].values():
                if c != b and c not in da:
                    isolate = True
                elif c != b:
                    deviazione = max(deviazione, da[c] - dist[a][c])
    if not ciechi and not articolazioni:
        righe = ['• Nessun vicolo cieco; nessuna casella che, occupata da un',
                 '  mostro, isoli una zona (grafo senza punti di articolazione).']
    else:
        righe = ['• Vicoli ciechi: ' + (', '.join(ciechi) or 'nessuno') + '.',
                 '• Caselle che isolano una zona: ' + (', '.join(articolazioni) or 'nessuna') + '.']
    righe.append(f'• Deviazione massima con 1 mostro sulla strada: +{deviazione} esagoni'
                 + ('; a volte una Cripta resta isolata.' if isolate else '.'))
    pc = [dist[a][c] for a in p['partenze'].values() for c in p['cripte'].values()]
    righe.append(f'• Partenza → Cripta: più vicina {min(pc)} (v6: 3), media {num(sum(pc) / len(pc))} (v6: 5,25).')
    entro = {k: [sum(1 for q in p['domande'] if 1 <= dist[a].get(q, k + 1) <= k) for a in p['partenze'].values()]
             for k in (1, 3, 5)}
    righe.append(f'• Ogni Partenza: {intervallo(entro[1])} «?» a 1 passo, {intervallo(entro[3])} entro 3, '
                 f'{intervallo(entro[5])} entro 5.')
    righe += ['• Le Mappe (Città, Foresta, Tundra…) cambiano MOV ed effetti,',
              '  non la geometria: la plancia resta la stessa.']
    return righe


def passaggi(p):
    """guadi e ponti raggruppati in passaggi (caselle di guado collegate tra loro), da ovest a est."""
    resto, gruppi = set(p['guadi']), []
    while resto:
        g, coda = set(), [resto.pop()]
        while coda:
            h = coda.pop()
            g.add(h)
            for v in p['vicini'][h]:
                if v in resto:
                    resto.discard(v)
                    coda.append(v)
        gruppi.append(sorted(g, key=TUTTI.index))
    gruppi.sort(key=lambda g: sum(_cr(h)[0] for h in g) / len(g))
    nomi = []
    for g in gruppi:
        mc = sum(_cr(h)[0] for h in g) / len(g)
        if len(g) == 1:
            nomi.append(f'Guado {"ovest" if mc < 4.5 else "est" if mc > 4.5 else "centrale"} {g[0]}')
        else:
            nomi.append(f'Ponte {"ovest" if mc < 4.5 else "est" if mc > 4.5 else "del lago"} {"–".join(g)}')
    return gruppi, nomi


# ---------- tessere illustrate (--tema) ----------
def terreno(p, h):
    """terreno della tessera di h: PT-<TEMA>-<TERRENO>-<n>.png."""
    if h in p['partenze'].values():
        return 'PARTENZA'
    if h in p['cripte'].values():
        return 'CRIPTA'
    if h in p['guadi']:
        return 'GUADO'
    return 'STRADA' if h in p['strada'] else p['tipo'][h].upper()


def variante(h, terr):
    """«TERRENO-n»: la variante dipende solo dalla coordinata (crc32, uguale a ogni esecuzione)."""
    return f'{terr}-{zlib.crc32(h.encode()) % VARIANTI[terr] + 1}'


def tessere(p, tema, cartella, arte=ARTE):
    """{«TERRENO-n» o «SALA»: (href relativo a `cartella`, specchiata)} delle immagini usate da plancia e legenda (la
    legenda usa le varianti -1 di tutti i terreni). Una variante -n che manca usa la -1 specchiata; se manca una -1 o
    PS-<TEMA> esce con l'elenco degli id mancanti."""
    chiavi = {variante(h, terreno(p, h)) for h in TUTTI} | {f'{t}-1' for t in VARIANTI}
    file = {k: os.path.join(arte, f'PT-{tema}-{k}.png') for k in chiavi}
    file['SALA'] = os.path.join(arte, f'PS-{tema}.png')
    specchio = {k for k, f in file.items() if not k.endswith('-1') and k != 'SALA' and not os.path.isfile(f)}
    for k in specchio:
        file[k] = file[k.rsplit('-', 1)[0] + '-1']
    manca = sorted({os.path.basename(f)[:-4] for f in file.values() if not os.path.isfile(f)})
    if manca:
        sys.exit(f'tema {tema}: mancano {len(manca)} immagini in {os.path.normpath(arte)}: {", ".join(manca)}')
    if specchio:
        print(f'tema {tema}: mancano {", ".join(f"PT-{tema}-{k}" for k in sorted(specchio))}, uso la -1 specchiata')
    return {k: (os.path.relpath(f, cartella), k in specchio) for k, f in file.items()}


def tessera(img, x, y, cid, k=1.0):
    """tessera img = (href, specchiata) ritagliata a esagono (raggio R*k) centrata in (x, y): clipPath e immagine sulla
    stessa riga. Specchiata: girata attorno alla verticale per x (l'esagono è simmetrico, il ritaglio non cambia)."""
    href, specchiata = img
    t = TESSERA * k
    giro = f' transform="matrix(-1 0 0 1 {2 * x:.2f} 0)"' if specchiata else ''
    return (f'<clipPath id="{cid}"><polygon points="{punti(x, y, R * k)}"/></clipPath>'
            f'<image href="{escape(href)}" x="{x - t / 2:.2f}" y="{y - t / 2:.2f}" width="{t:.2f}" height="{t:.2f}" clip-path="url(#{cid})"{giro}/>')


def fondo_sala(img):
    """PS-<TEMA> sotto la fascia della Sala del Tesoro (a 300 ppi su tutta la larghezza), schiarita da un velo."""
    return (f'<clipPath id="fondo-sala"><rect x="2" y="2" width="{BW - 4:.2f}" height="{SALA_H - 2:.2f}"/></clipPath>'
            f'<image href="{escape(img[0])}" x="0" y="0" width="{BW:.2f}" height="{SALA_H:.2f}" clip-path="url(#fondo-sala)"/>'
            f'<rect x="2" y="2" width="{BW - 4:.2f}" height="{SALA_H - 2:.2f}" fill="#f4ead5" fill-opacity="0.55"/>')


def numero_partenza(x, y, n, k=1.0):
    """Partenza su tessera: numero bianco in un tondo viola, sotto il centro (il centro resta all'illustrazione)."""
    r = R * 0.38 * k
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#7a4f86" stroke="{ALONE}" stroke-width="{0.8 * k:.2f}"/>'
            f'<text x="{x:.2f}" y="{y + r * 0.5:.2f}" text-anchor="middle" font-weight="800" font-size="{r * 1.45:.2f}" fill="#fff">{n}</text>')


def numero_cripta(x, y, n, k=1.0):
    """Cripta su tessera: numero nero in un tondo d'oro."""
    r = R * 0.38 * k
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#d9b45a" stroke="#7a5a1c" stroke-width="{0.9 * k:.2f}"/>'
            f'<text x="{x:.2f}" y="{y + r * 0.5:.2f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="{r * 1.45:.2f}" fill="{INK}">{n}</text>')


# ---------- disegno ----------
def plancia(p, arte=None, linee=True):
    """elementi del gruppo «plancia-v7», uno per riga (svg.py mappa_bozza li legge riga per riga). arte: hrefs di
    tessere() o None (aspetto piatto); linee: linee di strada tra le caselle collegate."""
    o = [f'<rect x="1" y="1" width="{BW - 2:.1f}" height="{BH - 2:.1f}" rx="{W * 0.5:g}" fill="#efe1c3" stroke="{BROWN}" stroke-width="2"/>']
    s = R * 0.97
    if arte:
        o.append(fondo_sala(arte['SALA']))
        o += [tessera(arte[variante(h, terreno(p, h))], *centro(h), f'es-{h}') for h in TUTTI]
        o += [f'<polygon points="{punti(*centro(h), R)}" {GRIGLIA}/>' for h in TUTTI]
    for h in [] if arte else TUTTI:
        col = STRADA_COL if h in p['strada'] and h not in p['guadi'] else GUADO_COL if h in p['guadi'] else TIPI[p['tipo'][h]][1]
        o.append(f'<polygon points="{punti(*centro(h), s)}" fill="{col}" stroke="{BORDO}" stroke-width="0.8"/>')
    for h in TUTTI if linee else ():   # linee di strada: ogni collegamento una volta (verso est, sud-ovest, sud-est)
        for v in p['vicini'].get(h, ()):
            if TUTTI.index(v) > TUTTI.index(h):
                (x1, y1), (x2, y2) = centro(h), centro(v)
                o.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{LINEA}" stroke-width="2.4" stroke-linecap="round" opacity="0.6"/>')
    if not arte:   # con le tessere il terreno è nell'illustrazione
        for t, (_, _, icona, *_) in TIPI.items():
            o += [icona(*centro(h)) for h in TUTTI if p['tipo'].get(h) == t]
        o += [ic_guado(*centro(h)) for h in TUTTI if h in p['guadi']]
    for n, h in p['partenze'].items():
        x, y = centro(h)
        if arte:
            o.append(f'<polygon points="{punti(x, y, R * 0.94)}" fill="none" stroke="#7a4f86" stroke-width="1.4"/>'
                     + numero_partenza(x, y + R * 0.45, n))
            continue
        o.append(f'<polygon points="{punti(x, y, s)}" fill="#7a4f86" fill-opacity="0.85" stroke="#7a4f86" stroke-width="1.2"/>')
        o.append(f'<text x="{x:.2f}" y="{y + R * 0.33:.2f}" text-anchor="middle" font-weight="800" font-size="{R * 0.9:.2f}" fill="#fff">{n}</text>')
    for n, h in p['cripte'].items():
        x, y = centro(h)
        if arte:
            o.append(f'<polygon points="{punti(x, y, R * 0.94)}" fill="none" stroke="#b8862b" stroke-width="1.4"/>'
                     + numero_cripta(x, y + R * 0.45, n))
            continue
        o.append(f'<polygon points="{punti(x, y, s)}" fill="#d9b45a" stroke="#b8862b" stroke-width="1.6"/>')
        o.append(f'<text x="{x:.2f}" y="{y + R * 0.35:.2f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="{R * 0.95:.2f}" fill="{INK}">{n}</text>')
    o += [q_mark(*centro(h), R * 0.42) for h in p['domande']]
    for m in sorted(p['muri'], key=lambda m: sorted(map(TUTTI.index, m))):
        (x1, y1), (x2, y2) = lato_comune(*sorted(m, key=TUTTI.index))
        xy = f'x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"'
        alone = f'<line {xy} stroke="{ALONE}" stroke-width="5" stroke-linecap="round" stroke-opacity="0.8"/>' if arte else ''
        o.append(f'{alone}<line {xy} {MURO}/>')
    gruppi, _ = passaggi(p)
    for g in gruppi:
        for h in g:
            x, y = centro(h)
            scritta = f'x="{x:.2f}" y="{y + R * 0.78:.2f}" text-anchor="middle" font-size="4" font-weight="700"'
            nome = "guado" if len(g) == 1 else "ponte"
            alone = f'<text {scritta} fill="{ALONE}" stroke="{ALONE}" stroke-width="1.2" stroke-linejoin="round">{nome}</text>' if arte else ''
            o.append(f'{alone}<text {scritta} fill="{INK}">{nome}</text>')
    for c in range(10):
        o.append(f'<text x="{PAD + W * (c + 0.25):.1f}" y="{TOP - 4:.1f}" text-anchor="middle" font-size="{W * 0.32:.1f}" fill="{BROWN}">{"ABCDEFGHIJ"[c]}</text>')
    for r in range(1, 11):
        o.append(f'<text x="{PAD - 6:.1f}" y="{centro(_nome(0, r))[1] + 3:.1f}" text-anchor="end" font-size="{W * 0.32:.1f}" fill="{BROWN}">{r}</text>')
    # fascia della Sala del Tesoro: segnaposto (svg.py board() la ridisegna come nella v6)
    o.append(f'<text x="{BW / 2:.1f}" y="{W * 0.95:.1f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="{W * 0.55:.1f}" fill="{BROWN}">Sala del Tesoro</text>')
    cy = W * 1.75
    for i, (nm, rad, big) in enumerate((('Custode', W * 0.75, True), ('MIMI', W * 0.55, False), ('Boss', W * 0.6, False), ('Boss', W * 0.6, False))):
        x = BW / 2 + (i - 1.5) * W * 2.3
        o.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="{"#b8862b" if big else "#f7efdc"}" fill-opacity="{0.5 if big else 1}" stroke="{BROWN}" stroke-width="1.2"/>'
                 f'<text x="{x:.1f}" y="{cy + rad + W * 0.42:.1f}" text-anchor="middle" font-size="{W * 0.34:.1f}" fill="{INK}">{nm}</text>')
    u = 1 / 0.97   # rotelle in mm veri (plancia stampata in scala 0,97), disco Ø 52
    for rx, nm in ((40 * u, 'Rotella dello scontro'), (316 * u, 'Rotella del custode')):
        o.append(f'<circle cx="{rx:.1f}" cy="{55 * u:.1f}" r="{26 * u:.1f}" fill="none" stroke="{BROWN}" stroke-width="0.8" stroke-dasharray="3 2"/>'
                 f'<text x="{rx:.1f}" y="{55 * u + 2:.1f}" text-anchor="middle" font-size="5" fill="{BROWN}">{nm}</text>')
    o.append(f'<text x="{BW / 2:.1f}" y="{TOP - 14:.1f}" text-anchor="middle" font-size="5.5" font-style="italic" fill="{BROWN}">'
             '(fascia alta e Rotelle invariate rispetto alla v6; spostamenti del tesoro come v6)</text>')
    y0 = TOP + 9 * PASSO + 2 * R + W * 0.9
    o.append(f'<text x="{BW / 2:.1f}" y="{y0:.1f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="{W * 0.5:.1f}" fill="{BROWN}">Promemoria</text>')
    for i, t in enumerate(('Turno: Muovi · Esplora · Fine',
                           'Muovi solo sulla strada: ostacoli e muri non si attraversano · eroi sì',
                           'Mostro scoperto: sbarra la strada, fermati lì per affrontarlo',
                           '«?» coperta: girala e toglila · 6 o meno «?» coperte: rifornisci a fine turno',
                           'Perdita D6: 1 tutto · 2 elmo · 3 arma DX · 4 arma SX · 5 armatura · 6 niente')):
        o.append(f'<text x="{BW / 2:.1f}" y="{y0 + W * 0.7 + i * W * 0.55:.1f}" text-anchor="middle" font-size="{W * 0.285:.1f}" fill="{INK}">{escape(t, False)}</text>')
    return o


def testo(x, y, size, weight, fill, t, extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="start"{extra}>'
            f'{escape(t, False)}</text>')


def legenda(p, arte=None, linee=True):
    x0, ix, tx = LX + 6, LX + 15, LX + 32
    o = [f'<rect x="{LX:.1f}" y="1" width="272" height="{BH - 2:.1f}" rx="8" fill="#fffaf0" stroke="{BROWN}" stroke-width="1"/>',
         testo(x0, 16, '10', 800, BROWN, 'Il Tesoro del Goblin · BOZZA plancia v7'),
         testo(x0, 25, '6', 400, BROWN, 'Proposta di lavoro del 9/11/2026, non è il file di stampa', ' font-style="italic"'),
         testo(x0, 35, '6', 400, INK, 'Stessa griglia e stesso formato della v6: 10 × 10 esagoni,'),
         testo(x0, 42.5, '6', 400, INK, 'esagono 25,2 mm, plancia 355,6 × 447,7 mm (4 fogli A4 o 2 A3).'),
         testo(x0, 50, '6', 400, INK, 'Partenze e Cripte nelle stesse caselle. Girata di 180° è identica.'),
         testo(x0, 61.5, '8', 800, BROWN, 'Legenda')]
    s = R * 0.62

    def esagono(y, col, extra=f' stroke="{BORDO}" stroke-width="0.8"', terr=None):
        if arte and terr:   # con --tema: la tessera -1 del terreno
            return tessera(arte[f'{terr}-1'], ix, y, f'lg-{y * 10:.0f}', 0.62) + f'<polygon points="{punti(ix, y, s)}" {GRIGLIA}/>'
        return f'<polygon points="{punti(ix, y, s)}" fill="{col}"{extra}/>'

    def piccola(icona, y):
        return f'<g transform="translate({ix:.1f},{y:.1f}) scale(0.62) translate({-ix:.1f},{-y:.1f})">{icona(ix, y)}</g>'

    conta = {t: sum(1 for v in p['tipo'].values() if v == t) for t in TIPI}
    cripte = set(p['cripte'].values())
    muri_cripte = sum(1 for m in p['muri'] if m & cripte)
    gruppi, nomi = passaggi(p)
    ingressi = sorted({len(p['vicini'][c]) for c in p['cripte'].values()})
    voci = [
        (lambda y: esagono(y, STRADA_COL, terr='STRADA') + (f'<line x1="{ix - 9:.1f}" y1="{y:.1f}" x2="{ix + 9:.1f}" y2="{y:.1f}" stroke="{LINEA}" stroke-width="3" stroke-linecap="round"/>' if linee else ''),
         f'Strada: {len(p["strada"])} esagoni percorribili',
         ['Le linee chiare uniscono le caselle collegate. 1 esagono = 1 passo.' if linee else
          'Caselle di strada accanto (senza muro) collegate. 1 esagono = 1 passo.']),
    ] + [
        (lambda y, t=t: esagono(y, TIPI[t][1], terr=t.upper()) + ('' if arte else piccola(TIPI[t][2], y)), f'{TIPI[t][3]} ({conta[t]})', [TIPI[t][4]])
        for t in TIPI
    ] + [
        (lambda y: esagono(y, GUADO_COL, terr='GUADO') + ('' if arte else piccola(ic_guado, y)),
         f'Guado e Ponte ({len(p["guadi"])} caselle, {len(gruppi)} passaggi)',
         ["Strada sull'acqua: gli unici passaggi nord–sud.", ', '.join(nomi) + '.']),
        (lambda y: esagono(y, STRADA_COL, terr='STRADA') + f'<line x1="{ix - 6:.1f}" y1="{y + 5:.1f}" x2="{ix + 6:.1f}" y2="{y - 5:.1f}" {MURO}/>',
         f'Muro ({len(p["muri"])} tratti)',
         ['Il bordo spesso non si attraversa; niente Duello attraverso',
          f'un muro. {muri_cripte} tratti chiudono le Cripte, {len(p["muri"]) - muri_cripte} sono mura.']),
        (lambda y: esagono(y, '', terr='PARTENZA') + numero_partenza(ix, y + 3, 1, 0.8) if arte else
         esagono(y, '#7a4f86', '') + f'<text x="{ix:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-size="8" font-weight="800" fill="#fff">1</text>',
         f'Partenze 1–{len(p["partenze"])}',
         [f'Stesse caselle della v6 ({", ".join(p["partenze"].values())}).']),
        (lambda y: esagono(y, '', terr='CRIPTA') + numero_cripta(ix, y + 3, 1, 0.8) if arte else
         esagono(y, '#d9b45a', ' stroke="#b8862b" stroke-width="1.2"') + f'<text x="{ix:.1f}" y="{y + 3:.1f}" text-anchor="middle" font-family="serif" font-size="8" font-weight="800" fill="{INK}">1</text>',
         f'Cripte 1–{len(p["cripte"])}',
         [f'Stesse caselle della v6; {"/".join(map(str, ingressi))} ingressi ciascuna. La Cripta',
          'con MIMI e il custode non si attraversa.']),
        (lambda y: q_mark(ix, y, 6),
         f'Casella «?» ({len(p["domande"])}; v6: 36)',
         ['A inizio partita 1 tessera coperta (senza sacchetto).',
          'Chi si ferma la gira e la toglie: il «?» si consuma.']),
        (lambda y: esagono(y, STRADA_COL, terr='STRADA') + f'<circle cx="{ix:.1f}" cy="{y:.1f}" r="6.5" fill="#a8352a" stroke="#fff" stroke-width="0.8"/>'
                   f'<path d="M{ix - 3.5:.1f} {y - 3.5:.1f}l7 7M{ix + 3.5:.1f} {y - 3.5:.1f}l-7 7" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/>',
         'Mostro scoperto = ostacolo',
         ['Tessera rossa rimasta a faccia in su (fuga o sconfitta):',
          'sbarra la strada. Non si attraversa; ti fermi lì e lo affronti.']),
    ]
    y = 73.5
    for disegno, titolo, righe in voci:
        o.append(disegno(y))
        o.append(testo(tx, y - 2, '6.6', 700, INK, titolo))
        o += [testo(tx, y + 5 + 6.6 * j, '5.6', 400, '#3c3226', r) for j, r in enumerate(righe)]
        y += 20.6 + 6.6 * (len(righe) - 1)
    y -= 4
    o.append(testo(x0, y, '5.6', 400, INK, 'Locanda, Fonte e Fabbro non sono caselle: restano Carte Imprevisto', ' font-style="italic"'))
    o.append(testo(x0, y + 6.5, '5.6', 400, INK, '(tessera blu), come dalla decisione del 2/11.', ' font-style="italic"'))
    y += 18.5
    o.append(testo(x0, y, '7.4', 800, BROWN, 'Controlli calcolati su questa bozza'))
    o += [testo(x0, y + 8 + 7 * j, '5.8', 400, INK, r) for j, r in enumerate(controlli(p))]
    return o


def svg(p, arte=None, linee=True):
    return '\n'.join(
        [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LX + 278:.1f} {BH:.1f}" font-family="Liberation Sans Narrow, Arial Narrow, sans-serif">',
         '<title>Il Tesoro del Goblin - bozza plancia v7 (proposta)</title>',
         '<g id="plancia-v7">'] + plancia(p, arte, linee) + ['</g>', '<g id="legenda">'] + legenda(p, arte, linee) + ['</g>', '</svg>']) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--dati', default=DATI, help='modulo Python con i dati della plancia (default: simulatore/mappa.py)')
    ap.add_argument('--out', default=OUT, help='SVG da scrivere (default: idee/v7_bozza_mappa.svg)')
    ap.add_argument('--tema', help='tessere illustrate arte/png/PT-<TEMA>-*.png e PS-<TEMA>.png (es. BASE, TUNDRA); '
                                   'default: aspetto piatto senza immagini')
    ap.add_argument('--arte', default=ARTE, help='cartella delle immagini di --tema (default: stampa/sorgenti/arte/png)')
    ap.add_argument('--senza-linee', action='store_true', help='niente linee di strada tra le caselle collegate')
    a = ap.parse_args()
    p = prepara(carica_dati(a.dati))
    arte = tessere(p, a.tema.upper(), os.path.dirname(os.path.abspath(a.out)), a.arte) if a.tema else None
    s = svg(p, arte, not a.senza_linee)
    with open(a.out, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'scritto {a.out}')


if __name__ == '__main__':
    main()
