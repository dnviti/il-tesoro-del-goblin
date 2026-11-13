#!/usr/bin/env python3
"""Mappa 12×12 a fiori da 7 esagoni: progetto, simulazione, preset, cambi delle carte Mappa, tempi e dati del kit.

Uso (dalla radice del repo):
  python3 v7/idee/mappa_tessere/12x12/mappa12.py                  # pezzi, simulazione, preset, tempi (Markdown)
  python3 v7/idee/mappa_tessere/12x12/mappa12.py --veloce         # meno prove
  python3 v7/idee/mappa_tessere/12x12/mappa12.py --partenze       # rifà la scelta delle 6 Partenze
  python3 v7/idee/mappa_tessere/12x12/mappa12.py --scrivi-preset  # rifà la ricerca dei preset e dei 3 fiori di cambio
  python3 v7/idee/mappa_tessere/12x12/mappa12.py --scrivi-dati    # scrive i CSV del kit in v7/stampa/sorgenti/dati/
  python3 v7/idee/mappa_tessere/12x12/mappa12.py --verifica-csv   # rimonta i 10 preset dai CSV e li controlla

Regole (Daniele, 12/11; terreno dalle 19:01):
- griglia 12×12 con la punta in alto, righe dispari spostate a sinistra di mezzo esagono; coordinate x = colonna 1-12,
  y = riga 1-12; esagono 25,2 mm; niente muri;
- terreno in 3 categorie: LIBERO (prato, mattonato, pavimento, sentiero, guado, ponte; si entra con 1 passo), ACCIDENTATO
  (acqua; entrarci costa 1 MOV in più) e OSTACOLO (bosco, rocce, case; non si entra). Il sottotipo è solo grafico;
- reticolo dei fiori (q + 5r + 1) mod 7: 14 spazi da 7 esagoni, identico girato di 180° (lo spazio s girato è il 15 − s);
  i 46 esagoni di bordo sono sulla BASE (2 fogli A4): terreno libero, le 6 Partenze, 4 ostacoli singoli;
- 14 fiori a due facce. Regola di disegno (garanzia di collegamento): centro percorribile e sull'anello al massimo 3
  ostacoli mai vicini, oppure centro ostacolo e sull'anello al massimo 1 ostacolo.
"""
import collections
import csv
import itertools
import math
import os
import random
import statistics
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.normpath(os.path.join(QUI, '..', '..', '..'))
DATI = os.path.join(V7, 'stampa', 'sorgenti', 'dati')
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(QUI, '..'))
import modello_tempi as ts  # noqa: E402  modello dei tempi della proposta del 12/11

N = 12
CELLE = [(c, r) for r in range(1, N + 1) for c in range(1, N + 1)]
AX = {(c, r): (c - 1 - (r - 1) // 2, r - 1) for c, r in CELLE}
HX = {v: k for k, v in AX.items()}
DIR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]   # anello: 1 E, 2 NE, 3 NO, 4 O, 5 SO, 6 SE (antiorario)
NOMI_DIR = ['E', 'NE', 'NO', 'O', 'SO', 'SE']
LIBERI = ('prato', 'mattonato', 'pavimento', 'sentiero', 'guado', 'ponte', 'partenza')
ACCIDENTATI = ('acqua',)
OSTACOLI = ('bosco', 'rocce', 'case')


def categoria(x):
    return 'ostacolo' if x in OSTACOLI else 'accidentato' if x in ACCIDENTATI else 'libero'


def percorribile(x):
    return x not in OSTACOLI


def costo(x):
    """passi per entrare nell'esagono (R 8.4 nuova): libero 1, accidentato 2."""
    return 2 if x in ACCIDENTATI else 1


def vicini(h):
    q, r = AX[h]
    return [HX[(q + a, r + b)] for a, b in DIR if (q + a, r + b) in HX]


def gira(h):
    return N + 1 - h[0], N + 1 - h[1]


def dist(a, b):
    (q1, r1), (q2, r2) = AX[a], AX[b]
    return max(abs(q1 - q2), abs(r1 - r2), abs(q1 - q2 + r1 - r2))


def bordo(h):
    return h[0] in (1, N) or h[1] in (1, N)


# ------------------------------------------------------------------ reticolo dei fiori, spazi e base
def reticolo(a=1, b=5, off=1):
    g = collections.defaultdict(set)
    for h, (q, r) in AX.items():
        f = lambda qq, rr: (a * qq + b * rr + off) % 7  # noqa: E731
        c = (q, r) if f(q, r) == 0 else next((q + x, r + y) for x, y in DIR if f(q + x, r + y) == 0)
        g[c].add(h)
    return g


_G = reticolo()
_CENTRI = sorted((c for c, s in _G.items() if len(s) == 7), key=lambda c: (c[1], c[0]))
SPAZI = {i: HX[c] for i, c in enumerate(_CENTRI, 1)}             # spazio -> esagono centrale
BASE = sorted(set(CELLE) - {h for c in _CENTRI for h in _G[c]}, key=lambda h: (h[1], h[0]))
assert len(SPAZI) == 14 and len(BASE) == 46
assert all(gira(SPAZI[s]) == SPAZI[15 - s] for s in SPAZI)


def anello(s, k):
    """esagono in direzione k (0-5, cioè 1-6) attorno al centro dello spazio s."""
    q, r = AX[SPAZI[s]]
    return HX[(q + DIR[k][0], r + DIR[k][1])]


def spazio_di(h):
    for s, c in SPAZI.items():
        if h == c or h in {anello(s, k) for k in range(6)}:
            return s
    return None


# ------------------------------------------------------------------ i 14 fiori (faccia A | faccia B)
def faccia(nome, fondo, centro, ost, tipo=None, tipi=None, acqua=()):
    """fondo: sottotipo del terreno libero; centro: tipo del centro (None = fondo); ost: posizioni 0-5 dell'anello con
    un ostacolo, di tipo `tipo` (o `tipi`, uno per posizione); acqua: posizioni dell'anello d'acqua. Controlla la regola."""
    anl = [fondo] * 6
    for k in acqua:
        anl[k] = 'acqua'
    for k, x in zip(ost, tipi or [tipo] * len(ost)):
        anl[k] = x
    c = centro or fondo
    ob = [k for k in range(6) if anl[k] in OSTACOLI]
    if c in OSTACOLI:
        assert len(ob) <= 1, nome
    else:
        assert len(ob) <= 3 and all((k + 1) % 6 not in ob for k in ob), nome
    return {'nome': nome, 'centro': c, 'anello': anl}


S3, S2A, S2B = (0, 2, 4), (0, 2), (0, 3)
FIORI = [
    (faccia('Tre boschi', 'prato', None, S3, 'bosco'), faccia('Tre massi', 'pavimento', None, S3, 'rocce')),
    (faccia('Bosco a tre punte', 'prato', None, S3, 'bosco'), faccia('Pietraia', 'pavimento', None, S3, 'rocce')),
    (faccia('Crocevia nel bosco', 'sentiero', None, S3, 'bosco'), faccia('Borgo a stella', 'mattonato', None, S3, 'case')),
    (faccia('Boschi e massi', 'prato', None, S3, tipi=['bosco', 'rocce', 'bosco']), faccia('Tre cascine', 'mattonato', None, S3, 'case')),
    (faccia('Due boschetti', 'prato', None, S2A, 'bosco'), faccia('Cava', 'pavimento', None, S3, 'rocce')),
    (faccia('Bosco e bosco', 'sentiero', None, S2A, 'bosco'), faccia('Villaggio', 'mattonato', None, S3, 'case')),
    (faccia('Strettoia nel bosco', 'sentiero', None, S2B, 'bosco'), faccia('Due massi', 'pavimento', None, S2A, 'rocce')),
    (faccia('Varco', 'prato', None, S2B, tipi=['bosco', 'rocce']), faccia('Due case', 'mattonato', None, S2A, 'case')),
    (faccia('Ruscello col guado', 'prato', 'guado', (1, 4), 'bosco', acqua=(0, 3)), faccia('Massi sparsi', 'pavimento', None, S2A, 'rocce')),
    (faccia('Ruscello col ponte', 'prato', 'ponte', (1, 4), 'rocce', acqua=(0, 3)), faccia('Case sparse', 'mattonato', None, S2A, 'case')),
    (faccia('Mulino sul fiume', 'mattonato', 'guado', (2, 5), 'case', acqua=(0, 3)), faccia('Rupe', 'pavimento', 'rocce', (0,), 'rocce')),
    (faccia('Fiume col ponte', 'prato', 'ponte', (2, 5), 'bosco', acqua=(0, 3)), faccia('Piazza', 'mattonato', 'case', (0,), 'case')),
    (faccia('Lago nel bosco', 'prato', 'acqua', (2, 4), 'bosco', acqua=(0,)), faccia('Miniera', 'pavimento', None, S3, 'rocce')),
    (faccia('Laghetto tra i massi', 'prato', 'acqua', (1, 3, 5), tipi=['rocce', 'bosco', 'rocce']), faccia('Mercato', 'mattonato', None, S3, 'case')),
]
assert len(FIORI) == 14

# base: 46 esagoni di bordo, prato. Partenze P1-P6 in senso orario (ottimizza_partenze: non simmetriche, bilanciate)
PARTENZE = [(5, 1), (11, 2), (12, 8), (9, 12), (2, 10), (1, 4)]
OSTACOLI_BASE = {(7, 2): 'bosco', (6, 11): 'bosco', (2, 9): 'rocce', (11, 4): 'rocce'}


def base(partenze=PARTENZE):
    t = {h: 'prato' for h in BASE}
    t.update(OSTACOLI_BASE)
    for h in partenze:
        assert h in BASE and t[h] == 'prato', h
        t[h] = 'partenza'
    return t


# ------------------------------------------------------------------ montaggio
def posa(t, s, f, rot):
    """posa la faccia f nello spazio s con la freccia (esagono 1 dell'anello) verso il numero rot + 1."""
    t[SPAZI[s]] = f['centro']
    for k in range(6):
        t[anello(s, (k + rot) % 6)] = f['anello'][k]


def mappa(disp, partenze=PARTENZE):
    """disp: {spazio: (fiore 0-13, faccia 0=A|1=B, rotazione 0-5)} -> terreno di ogni esagono."""
    t = base(partenze)
    for s, (i, lato, rot) in disp.items():
        posa(t, s, FIORI[i][lato], rot)
    assert len(t) == N * N
    return t


def draft_casuale(rnd):
    pezzi = list(range(14))
    rnd.shuffle(pezzi)
    return {s: (pezzi[s - 1], rnd.randrange(2), rnd.randrange(6)) for s in SPAZI}


def applica_cambio(disp, cambio):
    """carta Mappa (R 8.12 nuova): per ognuna delle 3 righe (spazio, fiore, faccia, rotazione), in ordine: se il fiore
    sta in un altro spazio, si scambia con quello che occupa lo spazio indicato (il fiore tolto va nello spazio liberato
    con la sua faccia e la sua rotazione); poi si mette la faccia e la rotazione indicate."""
    d = dict(disp)
    for s, (i, lato, rot) in cambio:
        dove = next(x for x, v in d.items() if v[0] == i)
        if dove != s:
            d[dove] = d[s]
        d[s] = (i, lato, rot)
    return d


# ------------------------------------------------------------------ controlli
def componenti(t):
    s = {h for h in CELLE if percorribile(t[h])}
    comp, visti = [], set()
    for h in s:
        if h not in visti:
            c, pila = {h}, [h]
            while pila:
                for v in vicini(pila.pop()):
                    if v in s and v not in c:
                        c.add(v)
                        pila.append(v)
            visti |= c
            comp.append(c)
    return comp


def passi(t, da):
    """costo minimo (passi di MOV) da `da` a ogni esagono percorribile: libero 1, accidentato 2 (Dijkstra)."""
    import heapq
    d, coda = {da: 0}, [(0, da)]
    while coda:
        c, h = heapq.heappop(coda)
        if c > d[h]:
            continue
        for v in vicini(h):
            if percorribile(t[v]):
                nc = c + costo(t[v])
                if nc < d.get(v, 1e9):
                    d[v] = nc
                    heapq.heappush(coda, (nc, v))
    return d


def ammassi(t):
    visti, out = set(), []
    for h in CELLE:
        if t[h] in OSTACOLI and h not in visti:
            c, pila = {h}, [h]
            while pila:
                for v in vicini(pila.pop()):
                    if t[v] in OSTACOLI and v not in c:
                        c.add(v)
                        pila.append(v)
            visti |= c
            out.append(len(c))
    return out


def misure(t):
    comp = componenti(t)
    ost = [h for h in CELLE if t[h] in OSTACOLI]
    am = ammassi(t)
    return {'collegata': len(comp) == 1, 'ostacoli': len(ost) / (N * N),
            'accidentati': sum(t[h] in ACCIDENTATI for h in CELLE) / (N * N),
            'ostacoli_bordo': sum(bordo(h) for h in ost) / sum(bordo(h) for h in CELLE),
            'ostacoli_centro': sum(1 for h in ost if 4 <= h[0] <= 9 and 4 <= h[1] <= 9) / 36,
            'ciechi': sum(1 for h in CELLE if percorribile(t[h]) and sum(percorribile(t[v]) for v in vicini(h)) <= 1),
            'ammasso_max': max(am, default=0)}


# ------------------------------------------------------------------ Tessere Esplorazione coperte e Cripta (D29: niente segnaposto «?»)
N_TESSERE = 24     # tessere Esplorazione coperte posate sugli esagoni al montaggio; le altre 12 restano nella riserva
P2D6 = {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}
# per ogni punto tirabile, tutti gli esagoni in ordine di ricerca: distanza, poi y, poi x
ORDINE = {(x, y): sorted(CELLE, key=lambda h: (dist(h, (x, y)), h[1], h[0])) for x in range(2, 13) for y in range(2, 13)}


def idonei_tessera(t, partenze=PARTENZE):
    """Tessera coperta: su qualsiasi esagono percorribile (anche acqua), non Partenza, ad almeno 2 esagoni da ogni Partenza;
    una sola tessera per esagono."""
    return [h for h in CELLE if percorribile(t[h]) and t[h] != 'partenza' and all(dist(h, p) >= 2 for p in partenze)]


def posa_tessere(t, rnd, n=N_TESSERE, partenze=PARTENZE):
    return set(rnd.sample(idonei_tessera(t, partenze), n))


def cripta(t, x, y, tessere=frozenset()):
    """Cripta su (x, y) tirato con 2D6 + 2D6. Su un esagono con una tessera coperta resta lì (la tessera torna coperta nella
    riserva); sull'acqua resta. Si sposta solo da un ostacolo o da una Partenza: va sull'esagono percorribile più vicino che
    non sia una Partenza, non abbia una tessera e non stia in riga o colonna 1; a pari distanza y più piccola, poi x più
    piccola. La Cripta sbarra il passaggio come un mostro scoperto."""
    if percorribile(t[(x, y)]) and t[(x, y)] != 'partenza':
        return (x, y), 0
    for h in ORDINE[(x, y)]:
        if percorribile(t[h]) and t[h] != 'partenza' and h not in tessere and h[0] >= 2 and h[1] >= 2:
            return h, dist(h, (x, y))


def attese_partenze(t, partenze=PARTENZE):
    """per ogni Partenza: passi di MOV attesi fino alla Cripta (2D6 + 2D6 esatti, spostamento compreso)."""
    d = [passi(t, p) for p in partenze]
    att = [0.0] * len(partenze)
    for x, px in P2D6.items():
        for y, py in P2D6.items():
            c, _ = cripta(t, x, y)
            for i in range(len(partenze)):
                att[i] += px * py * d[i].get(c, 99)
    return att


# ------------------------------------------------------------------ simulazione dei draft
def simula(prove, seme=12):
    rnd = random.Random(seme)
    m = collections.defaultdict(list)
    spost, perp, calore = [], [[] for _ in PARTENZE], collections.Counter()
    su_tessera = 0
    for _ in range(prove):
        t = mappa(draft_casuale(rnd))
        for k, v in misure(t).items():
            m[k].append(v)
        tess = posa_tessere(t, rnd)
        x, y = sum(rnd.randint(1, 6) for _ in range(2)), sum(rnd.randint(1, 6) for _ in range(2))
        c, s = cripta(t, x, y, tess)
        su_tessera += c in tess
        spost.append(s)
        calore[c] += 1
        for i, p in enumerate(PARTENZE):
            perp[i].append(passi(t, p).get(c, 99))
    return m, spost, perp, calore, su_tessera


def avversario(rnd, giri, passi_):
    """ricerca locale che prova a spezzare la mappa (più parti percorribili staccate, poi più esagoni fuori)."""
    def valuta(disp):
        comp = componenti(mappa(disp))
        return (len(comp), sum(map(len, comp)) - max(map(len, comp)))
    peggio = (1, 0)
    for _ in range(giri):
        d = draft_casuale(rnd)
        c = valuta(d)
        for _ in range(passi_):
            n = mossa(d, rnd)
            cn = valuta(n)
            if cn >= c:
                d, c = n, cn
        peggio = max(peggio, c)
    return peggio


def mossa(d, rnd):
    n = dict(d)
    s1 = rnd.choice(list(SPAZI))
    m = rnd.randrange(3)
    if m == 0:
        s2 = rnd.choice(list(SPAZI))
        n[s1], n[s2] = n[s2], n[s1]
    elif m == 1:
        n[s1] = (n[s1][0], n[s1][1], rnd.randrange(6))
    else:
        n[s1] = (n[s1][0], 1 - n[s1][1], n[s1][2])
    return n


# ------------------------------------------------------------------ Partenze bilanciate
def ottimizza_partenze(prove=300, seme=5):
    """6 Partenze sulla base (non simmetriche), a distanza >= 5 tra loro, che rendono più simili i passi attesi fino
    alla Cripta su `prove` draft casuali (2D6 esatti, spostamento compreso, acqua che costa 2)."""
    rnd = random.Random(seme)
    cand = [h for h in BASE if h not in OSTACOLI_BASE]
    att = collections.defaultdict(float)
    for _ in range(prove):
        t = mappa(draft_casuale(rnd), partenze=[])
        cr = collections.Counter()
        for x, px in P2D6.items():
            for y, py in P2D6.items():
                cr[cripta(t, x, y)[0]] += px * py
        for c, w in cr.items():
            d = passi(t, c)
            for h in cand:
                att[h] += w * d.get(h, 99) / prove

    def valuta(sei):
        v = [att[h] for h in sei]
        return max(v) - min(v), statistics.mean(v)
    # finestre di valori: per ogni Partenza «più bassa» si cercano 5 compagne entro lo scarto migliore trovato finora,
    # tutte a >= 5 esagoni tra loro; a pari scarto vince la media più vicina a quella di tutti i candidati
    ordine = sorted(cand, key=lambda h: att[h])
    media_tutti = statistics.mean(att[h] for h in cand)
    best = None
    for i, h0 in enumerate(ordine):
        lim = att[h0] + (best[0][0] if best else 99)
        fin = [h for h in ordine[i + 1:] if att[h] <= lim and dist(h, h0) >= 5]
        for cinque in itertools.combinations(fin, 5):
            sei = [h0, *cinque]
            if min(dist(a, b) for a, b in itertools.combinations(cinque, 2)) < 5:
                continue
            v = valuta(sei)
            k = (round(v[0], 3), abs(v[1] - media_tutti))
            if best is None or k < (round(best[0][0], 3), abs(best[0][1] - media_tutti)):
                best = (v, sei)
        if best and len(fin) > 18:   # finestre troppo larghe: lo scarto migliore è già piccolo, si stringe da solo
            continue
    return best, att


# ------------------------------------------------------------------ preset e cambi delle carte Mappa
def acqua_lunga(t, righe=(1, N)):
    """colonne attraversate dal corso d'acqua più lungo (acqua, guado, ponte) tra le righe date."""
    w = {h for h in CELLE if t[h] in ('acqua', 'guado', 'ponte') and righe[0] <= h[1] <= righe[1]}
    best, visti = 0, set()
    for h in w:
        if h not in visti:
            c, pila = {h}, [h]
            while pila:
                for v in vicini(pila.pop()):
                    if v in w and v not in c:
                        c.add(v)
                        pila.append(v)
            visti |= c
            best = max(best, len({x for x, _ in c}))
    return best


def conta(t, tipo, zona=lambda h: True):
    return sum(1 for h in CELLE if t[h] == tipo and zona(h))


def coppie_ost(t):
    return sum(1 for h in CELLE if t[h] in OSTACOLI for v in vicini(h) if t[v] in OSTACOLI) / 2


def articolazioni(t, zona):
    s = [h for h in CELLE if percorribile(t[h])]
    n = 0
    for b in s:
        if not zona(b):
            continue
        da = next(h for h in s if h != b)
        visti, pila = {da, b}, [da]
        while pila:
            for v in vicini(pila.pop()):
                if percorribile(t[v]) and v not in visti:
                    visti.add(v)
                    pila.append(v)
        n += len(visti) - 1 < len(s) - 1
    return n


def centro(h):
    return 4 <= h[0] <= 9 and 4 <= h[1] <= 9


def lati(h):
    return h[0] <= 4 or h[0] >= 9


# carattere di ogni preset (dal §17 della Spec): punteggio da massimizzare, oltre a fiume centrale ed equilibrio
TEMI = {
    'Strettoie': ('', 'strettoie davanti al centro; i guadi laterali sono da contendersi',
                  lambda t: 3 * articolazioni(t, centro) + 0.5 * sum(1 for h in CELLE if t[h] in OSTACOLI and centro(h))),
    'TM-01 Forziere': ('TM-01', 'oasi del miraggio: un palmeto al centro nord e al centro sud',
                       lambda t: 2 * conta(t, 'bosco', lambda h: 4 <= h[0] <= 9 and (h[1] <= 4 or h[1] >= 9)) - conta(t, 'case')),
    'TM-02 Città': ('TM-02', 'quartieri: isolati di case e vicoli stretti', lambda t: 2 * conta(t, 'case') + coppie_ost(t)),
    'TM-03 Foresta': ('TM-03', 'bosco fitto ma tanti sentieri', lambda t: 2 * conta(t, 'bosco') - conta(t, 'case')),
    'TM-04 Tundra': ('TM-04', 'distesa aperta di ghiaccio e massi: vince chi corre',
                     lambda t: conta(t, 'rocce') - 1.5 * sum(1 for h in CELLE if t[h] in OSTACOLI) - 2 * coppie_ost(t)),
    'TM-05 Sottovelo': ('TM-05', 'viali del cimitero: file di cipressi e lapidi chiudono nord e sud',
                        lambda t: 2 * sum(1 for h in CELLE if t[h] in ('bosco', 'case') and (2 <= h[1] <= 4 or 9 <= h[1] <= 11))),
    'TM-06 Miniera': ('TM-06', 'ammassi di roccia ai lati', lambda t: 2 * conta(t, 'rocce', lati) + coppie_ost(t) - conta(t, 'case')),
    'TM-07 Yuma': ('TM-07', 'il lago è il cuore della mappa', lambda t: 4 * conta(t, 'acqua', centro) + conta(t, 'bosco')),
    'TM-08 Flegias': ('TM-08', 'villaggio in fiamme al centro nord e al centro sud',
                      lambda t: 2 * conta(t, 'case', lambda h: 4 <= h[0] <= 9 and (h[1] <= 5 or h[1] >= 8))),
    'TM-09 MIMI': ('TM-09', 'caccia: ostacoli sparsi, sbarramenti leggeri', lambda t: -3 * coppie_ost(t) - articolazioni(t, lambda h: True)),
}


def punteggio(disp, tema):
    t = mappa(disp)
    att = attese_partenze(t)
    fiume = acqua_lunga(t, (4, 9))          # fiume centrale: righe 4-9
    return TEMI[tema][2](t) + 4 * min(fiume, 12) - 8 * (max(att) - min(att))


def cerca_preset(tema, seme, passi_):
    """ricerca locale (ricottura, 3 ripartenze) su spazio, faccia e rotazione di ogni fiore."""
    rnd = random.Random(seme)
    best = None
    for _ in range(3):
        d = draft_casuale(rnd)
        p = punteggio(d, tema)
        temp = 3.0
        for _ in range(passi_):
            nd = mossa(d, rnd)
            pn = punteggio(nd, tema)
            if pn >= p or rnd.random() < math.exp((pn - p) / max(temp, 1e-3)):
                d, p = nd, pn
            temp *= 0.997
            if best is None or p > best[0]:
                best = (p, dict(d))
    return best[1]


def cerca_cambio(tema, preset, partenze_da, seme=1):
    """i 3 fiori (righe del preset) che, messi con applica_cambio su una mappa in gioco, danno di più il carattere del
    preset: media del punteggio del tema su `partenze_da` (gli altri preset e alcuni draft). Ordine di applicazione:
    quello che migliora di più per primo."""
    f = TEMI[tema][2]
    righe = sorted(preset.items())
    best = None
    for tre in itertools.combinations(righe, 3):
        v = statistics.mean(f(mappa(applica_cambio(d, tre))) for d in partenze_da)
        if best is None or v > best[0]:
            best = (v, tre)
    tre = list(best[1])
    singolo = {r: statistics.mean(f(mappa(applica_cambio(d, [r]))) for d in partenze_da) for r in tre}
    return sorted(tre, key=lambda r: -singolo[r])


# ------------------------------------------------------------------ tempi
def tempi(p, giocatori=None):
    """secondi per montare la mappa: giocatori = 2, 3, 4 (draft), None (preset) o 'cambio' (carta Mappa: 3 fiori).
    Costanti di tempo_setup.py più stime nuove [INFERENZA]: decidere un fiore (spazio, rotazione, faccia) 3 / 6 / 12 s,
    una tessera Esplorazione coperta 1 / 2,5 / 5 s; pescare un fiore 1 s; con 3 e 4 giocatori si vede l'85 % e il 75 % della decisione."""
    k = ts.k
    sovrap = {None: 0.85, 'cambio': 1.0, 2: 1.0, 3: 0.85, 4: 0.75}[giocatori]
    dec_fiore = {'veloce': 3, 'tipico': 6, 'lento': 12}[p] * sovrap
    dec_tess = {'veloce': 1, 'tipico': 2.5, 'lento': 5}[p] * sovrap
    base_ = 2 * (k('presa_grande', p) + k('posa_grande', p) + k('orienta_grande', p))
    girare = {'veloce': 0.4, 'tipico': 0.6, 'lento': 0.9}[p]
    posa_fiore = k('presa_medio', p) + ts.fitts(p, 'toll_toppa') + k('orienta_multi', p) + k('urti_medio', p)
    posa_tess = k('presa_tile', p) + ts.fitts(p, 'toll_toppa')
    fisso = k('apertura', p) + k('sala', p)
    tess = N_TESSERE * (dec_tess + posa_tess) + 0.5 * N_TESSERE
    cerca = k('confronto', p) * (14 + 3) / 4
    da_foglio = k('lettura_pezzo', p) + cerca + girare + posa_fiore
    if giocatori == 'cambio':
        # 3 righe; in media 2,5 fiori si scambiano (togli + rimetti); le tessere di quei fiori (~4) tornano nella riserva e
        # chi ha giocato la carta le rimette sui fiori nuovi (decisione + posa); Cripta: 2D6 + 2D6 e posa
        return 3 * da_foglio + 2.5 * (k('togli', p) + posa_fiore) + 4 * (k('togli', p) + dec_tess + posa_tess) + 6 + 6
    if giocatori is None:
        return fisso + base_ + 14 * da_foglio + tess
    return fisso + base_ + 14 * 1.0 + 0.5 * (14 + N_TESSERE) + 14 * (dec_fiore + girare + posa_fiore) + tess


# ------------------------------------------------------------------ dati del kit (CSV)
def carica_preset():
    f = os.path.join(QUI, 'preset12.py')
    if not os.path.exists(f):
        return None, None
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    if 'CAMBIO' not in ns:
        return None, None
    return ns['PRESET'], ns['CAMBIO']


def scrivi_dati(preset, cambio):
    """fiori.csv, base12.csv, preset12.csv in v7/stampa/sorgenti/dati/ (formato in progetto.md §8)."""
    with open(os.path.join(DATI, 'fiori.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['fiore', 'faccia', 'nome', 'posizione', 'direzione', 'terreno', 'categoria', 'accidentato'])
        for i, fa in enumerate(FIORI, 1):
            for lato, f in zip('AB', fa):
                w.writerow([i, lato, f['nome'], 0, 'centro', f['centro'], categoria(f['centro']), int(f['centro'] in ACCIDENTATI)])
                for k in range(6):
                    x = f['anello'][k]
                    w.writerow([i, lato, f['nome'], k + 1, NOMI_DIR[k], x, categoria(x), int(x in ACCIDENTATI)])
    t = base()
    num = {h: i for i, h in enumerate(PARTENZE, 1)}
    with open(os.path.join(DATI, 'base12.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['x', 'y', 'parte', 'spazio', 'posizione', 'terreno', 'categoria', 'accidentato', 'partenza'])
        for h in CELLE:
            s = spazio_di(h)
            if s is None:
                x = 'prato' if t[h] == 'partenza' else t[h]
                w.writerow([h[0], h[1], 'base', '', '', x, categoria(x), 0, num.get(h, '')])
            else:
                pos = 0 if h == SPAZI[s] else next(k + 1 for k in range(6) if anello(s, k) == h)
                w.writerow([h[0], h[1], 'spazio', s, pos, '', '', '', ''])
    with open(os.path.join(DATI, 'preset12.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['preset', 'carta', 'spazio', 'fiore', 'faccia', 'freccia', 'cambio'])
        for tema, d in preset.items():
            ordine = {s: n for n, (s, _) in enumerate(cambio[tema], 1)}
            for s, (i, lato, rot) in sorted(d.items()):
                w.writerow([tema, TEMI[tema][0], s, i + 1, 'AB'[lato], rot + 1, ordine.get(s, '')])


def leggi_csv():
    """(fiori, base, preset, cambio) letti dai CSV del kit, nello stesso formato interno."""
    righe = list(csv.DictReader(open(os.path.join(DATI, 'fiori.csv'), encoding='utf-8')))
    fiori = {}
    for r in righe:
        f = fiori.setdefault((int(r['fiore']), r['faccia']), {'nome': r['nome'], 'centro': None, 'anello': [None] * 6})
        if int(r['posizione']) == 0:
            f['centro'] = r['terreno']
        else:
            f['anello'][int(r['posizione']) - 1] = r['terreno']
    b = {}
    for r in csv.DictReader(open(os.path.join(DATI, 'base12.csv'), encoding='utf-8')):
        if r['parte'] == 'base':
            b[(int(r['x']), int(r['y']))] = 'partenza' if r['partenza'] else r['terreno']
    preset, cambio = collections.defaultdict(dict), collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(DATI, 'preset12.csv'), encoding='utf-8')):
        v = (int(r['fiore']) - 1, 'AB'.index(r['faccia']), int(r['freccia']) - 1)
        preset[r['preset']][int(r['spazio'])] = v
        if r['cambio']:
            cambio[r['preset']].append((int(r['cambio']), (int(r['spazio']), v)))
    return fiori, b, dict(preset), {k: [x for _, x in sorted(v)] for k, v in cambio.items()}


def verifica_csv():
    fiori, b, preset, cambio = leggi_csv()
    assert all(fiori[(i, l)] == FIORI[i - 1]['AB'.index(l)] | {'nome': fiori[(i, l)]['nome']} for i, l in fiori), 'fiori.csv'
    assert b == base(), 'base12.csv'
    righe = []
    for tema, d in preset.items():
        t = mappa(d)
        mm = misure(t)
        att = attese_partenze(t)
        tutti = all(misure(mappa(applica_cambio(x, cambio[tema])))['collegata'] for x in preset.values())
        righe.append((tema, 'sì' if mm['collegata'] else 'NO', f"{100 * mm['ostacoli']:.0f} %", f"{100 * mm['accidentati']:.0f} %",
                      f'{min(att):.1f}–{max(att):.1f}', len(cambio[tema]), 'sì' if tutti else 'NO'))
    tab(righe, ('preset (dai CSV)', 'collegata', 'ostacoli', 'accidentato', 'passi attesi Partenza→Cripta',
                'fiori di cambio', 'collegata dopo il cambio da ogni preset'))


# ------------------------------------------------------------------ uscita
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
    veloce = '--veloce' in sys.argv
    if '--verifica-csv' in sys.argv:
        verifica_csv()
        return
    print('## Pezzi\n')
    nost = [sum(x in OSTACOLI for x in [f['centro']] + f['anello']) for fa in FIORI for f in fa]
    tipi = collections.Counter(x for fa in FIORI for f in fa for x in [f['centro']] + f['anello'] if x not in ('prato', 'mattonato', 'pavimento', 'sentiero'))
    print(f'14 fiori, 28 facce; ostacoli per faccia: media {statistics.mean(nost):.2f} (min {min(nost)}, max {max(nost)}). '
          f'Esagoni speciali sulle 28 facce: {dict(tipi)}. Base: 46 esagoni, 6 Partenze, {len(OSTACOLI_BASE)} ostacoli singoli.\n')

    if '--partenze' in sys.argv:
        ((scarto, media), sei), att = ottimizza_partenze(prove=100 if veloce else 300)
        print(f'Partenze: {sei} (scarto {scarto:.2f} passi, media {media:.2f})\n')

    print('## Simulazione dei draft casuali\n')
    prove = 1000 if veloce else 5000
    m, spost, perp, calore, sutess = simula(prove)
    righe = [('mappa tutta collegata (tutte le Partenze, nessuna sacca)', f"{100 * statistics.mean(m['collegata']):.1f} %"),
             ('ostacoli (bosco, rocce, case): media, min–max', f"{100 * statistics.mean(m['ostacoli']):.1f} % ({100 * min(m['ostacoli']):.0f}–{100 * max(m['ostacoli']):.0f} %)"),
             ('terreno accidentato (acqua): media', f"{100 * statistics.mean(m['accidentati']):.1f} %"),
             ('ostacoli sugli esagoni di bordo / nel centro 6×6', f"{100 * statistics.mean(m['ostacoli_bordo']):.1f} % / {100 * statistics.mean(m['ostacoli_centro']):.1f} %"),
             ('ammasso di ostacoli più grande: media (max)', f"{statistics.mean(m['ammasso_max']):.1f} ({max(m['ammasso_max'])})"),
             ('vicoli ciechi per mappa: media', f"{statistics.mean(m['ciechi']):.1f}"),
             ('Cripta spostata (da ostacolo o Partenza)', f"{100 * sum(s > 0 for s in spost) / len(spost):.1f} % (max {max(spost)} esagoni)"),
             ('Cripta su una tessera coperta (resta lì; la tessera torna nella riserva)', f'{100 * sutess / prove:.1f} %')]
    tab(righe, ('misura', f'su {prove} draft'))
    medie = [statistics.mean(v) for v in perp]
    print('Passi di MOV dalla Partenza alla Cripta (acqua = 2), media per Partenza: '
          + ', '.join(f'P{i + 1} {p} {v:.2f}' for i, (p, v) in enumerate(zip(PARTENZE, medie)))
          + f'; scarto {max(medie) - min(medie):.2f}.\n')
    peggio = avversario(random.Random(3), 20 if veloce else 60, 150 if veloce else 300)
    print(f'Ricerca del caso peggiore: {peggio[0]} parte/i percorribili, {peggio[1]} esagoni fuori.\n')

    print('## Preset\n')
    pr, cb = carica_preset()
    if pr is None or '--scrivi-preset' in sys.argv:
        pr = {tema: cerca_preset(tema, 7 + i, 400 if veloce else 2500) for i, tema in enumerate(TEMI)}
        rnd = random.Random(99)
        cb = {}
        for tema in TEMI:
            da = [d for x, d in pr.items() if x != tema] + [draft_casuale(rnd) for _ in range(6)]
            cb[tema] = cerca_cambio(tema, pr[tema], da)
        with open(os.path.join(QUI, 'preset12.py'), 'w', encoding='utf-8') as fh:
            fh.write('"""Preset 12×12 e 3 fiori di cambio trovati da mappa12.py --scrivi-preset (semi fissi).\n'
                     'PRESET = {tema: {spazio: (fiore 0-13, faccia 0=A 1=B, rotazione 0-5)}}; CAMBIO = {tema: [(spazio, (fiore, faccia, rotazione)) ×3]}."""\n')
            fh.write('PRESET = {\n' + ''.join(f'    {t!r}: {dict(sorted(d.items()))!r},\n' for t, d in pr.items()) + '}\n')
            fh.write('CAMBIO = {\n' + ''.join(f'    {t!r}: {c!r},\n' for t, c in cb.items()) + '}\n')
    righe = []
    for tema, d in pr.items():
        t = mappa(d)
        mm = misure(t)
        att = attese_partenze(t)
        f = TEMI[tema][2]
        prima = statistics.mean(f(mappa(x)) for k, x in pr.items() if k != tema)
        dopo = statistics.mean(f(mappa(applica_cambio(x, cb[tema]))) for k, x in pr.items() if k != tema)
        righe.append((tema, TEMI[tema][1], 'sì' if mm['collegata'] else 'NO', f"{100 * mm['ostacoli']:.0f} %",
                      f"{100 * mm['accidentati']:.0f} %", conta(t, 'bosco'), conta(t, 'rocce'), conta(t, 'case'),
                      acqua_lunga(t, (4, 9)), f'{min(att):.1f}–{max(att):.1f}',
                      ' '.join(f'S{s}:{i + 1}{"AB"[l]}·{r + 1}' for s, (i, l, r) in cb[tema]),
                      f'{100 * (dopo - prima) / max(1e-9, f(t) - prima):.0f} %'))
    tab(righe, ('preset', 'carattere', 'collegata', 'ostacoli', 'accidentato', 'bosco', 'rocce', 'case',
                'colonne del fiume (righe 4-9)', 'passi attesi Partenza→Cripta', 'cambio (3 fiori, in ordine)',
                'carattere ottenuto col cambio, partendo dagli altri preset'))
    if '--scrivi-dati' in sys.argv:
        scrivi_dati(pr, cb)
        print('CSV scritti in', DATI, '\n')

    print('## Tempi\n')
    righe = [(f'draft, {g} giocatori', *(mm_ss(tempi(p, g)) for p in ts.PROFILI)) for g in (2, 3, 4)]
    righe.append(('preset', *(mm_ss(tempi(p)) for p in ts.PROFILI)))
    righe.append(('carta Mappa a metà partita (3 fiori, Cripta di nuovo)', *(mm_ss(tempi(p, 'cambio')) for p in ts.PROFILI)))
    tab(righe, ('', 'veloce', 'tipico', 'lento'))


if __name__ == '__main__':
    main()
