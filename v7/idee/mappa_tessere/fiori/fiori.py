#!/usr/bin/env python3
"""Mappa a «fiori» da 7 esagoni (opzione B scelta da Daniele il 12/11): partizione, disegni, pezzi fronte/retro,
controlli dei bordi e tempi. Solo progetto (fase 1): non tocca Spec né kit.

Uso (dalla radice del repo):  python3 v7/idee/mappa_tessere/fiori/fiori.py [--catalogo]

Dati: i 10 preset veri (v7/simulatore/mappa.py e plance/*.py) letti da ../tempo_setup.py, che dà anche il modello dei
tempi (COSTANTI). Stampa in Markdown: le 14 griglie di fiori possibili, la partizione scelta, i disegni per posizione,
i pezzi fisici fronte/retro, i controlli (ogni preset rimontato dai suoi pezzi è identico all'originale, strade che
proseguono su ogni bordo, controlli del §17), le composizioni libere casuali e i tempi. Con --catalogo stampa anche
l'elenco di tutti i pezzi fisici con le due facce (serve alla fase 2).

Regole di disegno che contano per i disegni (vedi progetto.md, §3):
- strada: è un TERRENO (12/11, Main): ogni esagono di strada è un'area di terra battuta che arriva fino ai suoi lati,
  fusa con gli esagoni di strada vicini; al massimo un filo di traccia dentro il pezzo, ad albero (niente triangoli), che
  non esce dal pezzo. Così il disegno di un esagono dipende solo dal suo tipo: due esagoni di strada vicini combaciano
  sempre, anche tra pezzi diversi, e una strada contro un ostacolo finisce sul lato. Per confronto resta la regola
  'sentiero' della prima bozza (sentiero dal centro al punto medio dei lati, mozzicone sul bordo se il vicino è strada
  nel preset): fa dipendere il pezzo dai vicini e costa più disegni;
- muri: stampati, tutti; un muro sul taglio tra due pezzi sta su uno solo dei due, scelto per avere meno disegni;
- un pezzo è uguale in tutti i preset dove ha gli stessi esagoni e gli stessi muri (con 'sentiero' anche gli stessi mozziconi).
"""
import collections
import functools
import itertools
import math
import os
import random
import statistics
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(QUI, '..'))
import tempo_setup as ts  # noqa: E402  preset, geometria, controlli §17, modello dei tempi

TUTTI, PRESET, NOMI, AX, HX = ts.TUTTI, ts.PRESET, ts.NOMI, ts.AX, ts.HX
D6 = ts.D6
W = 25.2                       # esagono da lato a lato (R 8.2)
R = W / math.sqrt(3)           # lato = raggio = 14,55 mm


def strada(t):
    return ts.strada(t)


# ------------------------------------------------------------------ 1. griglie di fiori
def griglia(a, b, off):
    """partizione in fiori: (a·q + b·r + off) mod 7 è diverso su un esagono e sui suoi 6 vicini se {a, b, b−a} = {±1, ±2,
    ±3}; i centri dei fiori sono gli esagoni con resto 0. (a, b) = (1, 3) e (1, 5) sono le due chiralità."""
    g = collections.defaultdict(set)
    for h, (q, r) in AX.items():
        f = lambda qq, rr: (a * qq + b * rr + off) % 7  # noqa: E731
        c = (q, r) if f(q, r) == 0 else next((q + x, r + y) for x, y in D6 if f(q + x, r + y) == 0)
        g[c].add(h)
    return [frozenset(s) for s in g.values()]


def simmetrica(pezzi):
    s = set(pezzi)
    return all(frozenset(ts.ruota(h) for h in p) in s for p in pezzi)


def unisci(pezzi, fusioni):
    """fonde i pezzi che contengono le coppie di esagoni date (e le loro girate di 180°, per restare simmetrici)."""
    pz = [set(p) for p in pezzi]
    for a, b in fusioni + [(ts.ruota(a), ts.ruota(b)) for a, b in fusioni]:
        ia = next(i for i, p in enumerate(pz) if a in p)
        ib = next(i for i, p in enumerate(pz) if b in p)
        if ia != ib:
            pz[ia] |= pz[ib]
            del pz[ib]
    return sorted((frozenset(p) for p in pz), key=lambda p: min(map(TUTTI.index, p)))


def forma(p):
    return ts.canonico([(AX[h], 'x') for h in p])


def specchio(p):
    """forma vista dal retro: riflessione (q, r) -> (q + r, −r)."""
    return ts.canonico([((AX[h][0] + AX[h][1], -AX[h][1]), 'x') for h in p])


# ------------------------------------------------------------------ 2. disegni
class Partizione:
    """strade: 'area' (terreno, il disegno non dipende dai vicini) o 'sentiero' (mozzicone sul bordo se il vicino è
    strada nel preset); muri: 'stampati' (tutti sui pezzi) o 'listelli' (stampati solo i 10 delle Cripte, le mura libere a parte)."""

    def __init__(self, pezzi, mozziconi='area', muri='stampati'):
        self.mozziconi, self.muri = mozziconi, muri
        self.pezzi = pezzi
        self.di = {h: i for i, p in enumerate(pezzi) for h in p}
        self.giro = {i: self.di[ts.ruota(next(iter(p)))] for i, p in enumerate(pezzi)}
        assert all(frozenset(ts.ruota(h) for h in pezzi[i]) == pezzi[j] for i, j in self.giro.items())
        self.coppie = sorted({tuple(sorted((i, j))) for i, j in self.giro.items()})
        liberi = sorted({m for m in ts.MURI_TUTTI if len({self.di[h] for h in m}) == 2},
                        key=lambda m: sorted(map(TUTTI.index, m)))
        self.muri_taglio = liberi                # muri (anche delle Cripte) sul taglio tra due pezzi
        self.padrone = self._padroni()

    def _padroni(self, scelta=None):
        """muro sul taglio -> pezzo che lo stampa. scelta: per ogni classe di muri (muro e muro girato) quale dei due
        esagoni lo porta; senza scelta prova tutte le combinazioni e tiene quella con meno disegni."""
        classi, visti = [], set()
        for m in self.muri_taglio:
            if m not in visti:
                mr = frozenset(ts.ruota(h) for h in m)
                visti |= {m, mr}
                classi.append((m, mr))
        if scelta is not None:
            pad = {}
            for (m, mr), b in zip(classi, scelta):
                a = sorted(m, key=TUTTI.index)[b]
                pad[m], pad[mr] = self.di[a], self.di[ts.ruota(a)]
            return pad
        migliore = None
        for scelta in itertools.product((0, 1), repeat=len(classi)):
            self.padrone = self._padroni(scelta)
            n = sum(len(self.disegni(i)) for i, _ in self.coppie)
            if migliore is None or n < migliore[0]:
                migliore = (n, scelta)
        return self._padroni(migliore[1])

    def muri_di(self, i, k):
        return tuple(sorted(tuple(sorted(m, key=TUTTI.index)) for m in PRESET[k][1]
                            if (self.muri == 'stampati' or m in ts.MURI_FISSI)
                            and (self.padrone.get(m) if m in self.padrone else self.di[next(iter(m))]) == i))

    def faccia(self, i, k):
        """disegno del pezzo i nel preset k: esagoni, mozziconi di strada sul bordo, muri stampati."""
        t = PRESET[k][0]
        p = self.pezzi[i]
        celle = tuple((h, t[h]) for h in sorted(p, key=TUTTI.index))
        mozz = () if self.mozziconi == 'area' else \
            tuple(sorted((h, v) for h in p if strada(t[h]) for v in ts.vicini(h) if v not in p and strada(t[v])))
        return celle, mozz, self.muri_di(i, k)

    def disegni(self, i):
        """{disegno: preset che lo usano} per la posizione i."""
        d = collections.defaultdict(list)
        for k in NOMI:
            d[self.faccia(i, k)].append(k)
        return dict(d)


# ------------------------------------------------------------------ 3. pezzi fisici fronte/retro
def pezzi_fisici(part):
    """[(fronte, retro)] dove una faccia è (coppia di posizioni, disegno, preset) o None (retro libero).
    Ogni disegno serve in 2 copie (posizione nord e sud, girata di 180°). Due facce stanno sullo stesso pezzo se nessun
    preset le usa insieme e se la forma del retro (specchiata) è quella dell'altra posizione. Prima si accoppiano i
    disegni della stessa posizione (d1|d2 ×2), poi gli avanzi tra posizioni diverse (accoppiamento massimo, a forza bruta)."""
    out, avanzi = [], []
    for i, j in part.coppie:
        dd = sorted(part.disegni(i).items(), key=lambda kv: (-len(kv[1]), kv[1]))
        while len(dd) >= 2 and forma(part.pezzi[i]) == specchio(part.pezzi[i]):
            (d1, u1), (d2, u2) = dd.pop(), dd.pop()
            out += [(((i, j), d1, u1), ((i, j), d2, u2))] * 2
        avanzi += [((i, j), d, u) for d, u in dd]

    def compatibili(a, b):
        return (not set(a[2]) & set(b[2])) and forma(part.pezzi[a[0][0]]) == specchio(part.pezzi[b[0][0]])

    @functools.lru_cache(None)
    def migliore(resto):
        if not resto:
            return ()
        a, r = resto[0], resto[1:]
        best = migliore(r)
        for x in r:
            if compatibili(avanzi[a], avanzi[x]):
                m = ((a, x),) + migliore(tuple(y for y in r if y != x))
                if len(m) > len(best):
                    best = m
        return best

    coppie = migliore(tuple(range(len(avanzi))))
    usati = {x for c in coppie for x in c}
    out += [(avanzi[a], avanzi[b]) for a, b in coppie for _ in range(2)]
    out += [(avanzi[a], None) for a in range(len(avanzi)) if a not in usati for _ in range(2)]
    return out


# ------------------------------------------------------------------ 4. controlli
def rimonta(part, k):
    """rimonta il preset k dalle sue facce: (terreno, muri) e mozziconi per esagono."""
    t, muri, mozz = {}, set(), set()
    for i, p in enumerate(part.pezzi):
        celle, mz, mu = part.faccia(i, k)
        t.update(celle)
        mozz |= set(mz)
        muri |= {frozenset(m) for m in mu}
    return t, muri, mozz


def strade_continue(part, t, mozz, solo_mancanti=False):
    """lati tra due pezzi dove il disegno della strada non torna. Severo: mozzicone da una parte se e solo se c'è
    dall'altra, e solo tra due esagoni di strada. Con solo_mancanti conta solo i passaggi tra due esagoni di strada senza
    il sentiero da tutte e due le parti (un mozzicone che finisce contro un bosco qui è ammesso: è un vicolo disegnato)."""
    if part.mozziconi == 'area':
        return 0   # ogni esagono di strada è disegnato come area fino ai lati: due esagoni di strada combaciano sempre
    errori = 0
    for h in TUTTI:
        for v in ts.vicini(h):
            if part.di[h] != part.di[v] and TUTTI.index(h) < TUTTI.index(v):
                a, b = (h, v) in mozz, (v, h) in mozz
                passa = strada(t[h]) and strada(t[v])
                errori += (passa and not (a and b)) if solo_mancanti else ((a != b) or (a != passa))
    return errori


def monta(part, scelta):
    """mappa fatta con la faccia del preset scelta[i] in ogni posizione i: (terreno, muri, mozziconi)."""
    t, muri, mozz = {}, set(), set()
    for i in range(len(part.pezzi)):
        celle, mz, mu = part.faccia(i, scelta[i])
        t.update(celle)
        mozz |= set(mz)
        muri |= {frozenset(m) for m in mu}
    return t, muri, mozz


def varianti_guidate(part):
    """composizione libera «guidata», come si farebbe al tavolo: (a) un preset con una coppia di posizioni (nord e sud)
    presa da un altro preset; (b) la metà nord di un preset e la metà sud di un altro. Per ognuna: quante combinazioni
    diverse, % validi §17, % senza passaggi non disegnati, % con le strade del tutto continue."""
    def misura(scelte):
        visti, out = set(), [0, 0, 0]
        for sc in scelte:
            t, muri, mozz = monta(part, sc)
            chiave = (tuple(sorted(t.items())), frozenset(muri))
            if chiave in visti:
                continue
            visti.add(chiave)
            ok = ts.valida(ts.controlla(t, muri))
            out[0] += ok
            out[1] += ok and strade_continue(part, t, mozz, True) == 0
            out[2] += ok and strade_continue(part, t, mozz) == 0
        n = len(visti)
        return n, *(100 * x / n for x in out)
    n = len(part.pezzi)
    singoli = []
    for k in NOMI:
        for i, j in part.coppie:
            for d, usa in part.disegni(i).items():
                if k not in usa:
                    sc = {x: k for x in range(n)}
                    sc[i] = sc[j] = usa[0]
                    singoli.append(sc)
    nord = {i for i, _ in part.coppie}
    meta = [{x: (a if x in nord else b) for x in range(n)} for a in NOMI for b in NOMI if a != b]
    return misura(singoli), misura(meta)


def controlli_preset(part):
    righe = []
    for k in NOMI:
        t, muri, mozz = rimonta(part, k)
        uguale = t == PRESET[k][0] and muri == PRESET[k][1]
        c = ts.controlla(t, muri)
        righe.append((k, 'sì' if uguale else 'NO', strade_continue(part, t, mozz), 'sì' if ts.valida(c) else 'NO',
                      f"{c['pc_min']}–{c['pc_max']}", ' '.join(map(str, sorted(c['vicina'])))))
    return righe


def ruota_faccia(part, i, j, faccia):
    """la stessa faccia posata sulla posizione girata j (180°)."""
    celle, mozz, muri = faccia
    rc = tuple(sorted(((ts.ruota(h), x) for h, x in celle), key=lambda c: TUTTI.index(c[0])))
    return rc, tuple(sorted((ts.ruota(a), ts.ruota(b)) for a, b in mozz)), \
        tuple(sorted(tuple(sorted((ts.ruota(a), ts.ruota(b)), key=TUTTI.index)) for a, b in muri))


def valida_libera(t, muri):
    """controlli del §17 senza posizioni fisse: (grafo: strada collegata, almeno 2 uscite, nessun esagono che isola una
    zona; completa: in più Partenze 1-6 e Cripte 1-4 una volta ciascuna, ogni Cripta con 3 ingressi)."""
    s = {h for h in TUTTI if strada(t[h])}
    vic = {h: [v for v in ts.vicini(h) if v in s and frozenset((h, v)) not in muri] for h in s}

    def raggiunti(da, tolto=None):
        visti, pila = {da}, [da]
        while pila:
            for v in vic[pila.pop()]:
                if v != tolto and v not in visti:
                    visti.add(v)
                    pila.append(v)
        return len(visti)
    grafo = raggiunti(next(iter(s))) == len(s) and min(map(len, vic.values())) >= 2 and \
        all(raggiunti(next(x for x in s if x != b), b) == len(s) - 1 for b in s)
    pc = collections.Counter(t[h] for h in s if t[h][0] in 'PC')
    completa = grafo and all(pc[f'P{n}'] == 1 for n in range(1, 7)) and all(pc[f'C{n}'] == 1 for n in range(1, 5)) \
        and sum(pc.values()) == 10 and all(len(vic[h]) == 3 for h in s if t[h][0] == 'C')
    return grafo, completa


def combinazioni_libere(part, prove=20000, seme=11):
    """Composizione libera, due modi (seme fisso, risultati in %):
    (1) per posizione: ogni posizione (nord e sud separate) prende a caso uno dei disegni fatti per lei, da qualsiasi
        preset; Partenze, Cripte, «?» e fiume restano dove sono. -> (validi §17, + senza passaggi non disegnati, + con
        le strade del tutto continue);
    (2) fiori ovunque: ogni posizione di fiore intero prende a caso una faccia di fiore intero di qualsiasi posizione e
        preset, girata a caso di 60°·n; i pezzi di bordo vengono da un preset a caso. -> (grafo valido, §17 completo con
        Partenze 1-6 e Cripte 1-4, completo e senza passaggi non disegnati)."""
    rnd = random.Random(seme)
    disegni = {i: list(part.disegni(i)) for i, _ in part.coppie}
    for i, j in part.coppie:
        disegni[j] = [ruota_faccia(part, i, j, f) for f in disegni[i]]
    v = c1 = c2 = 0
    for _ in range(prove):
        t, muri, mozz = {}, set(), set()
        for i in range(len(part.pezzi)):
            celle, mz, mu = rnd.choice(disegni[i])
            t.update(celle)
            mozz |= set(mz)
            muri |= {frozenset(m) for m in mu}
        ok = ts.valida(ts.controlla(t, muri))
        v += ok
        c1 += ok and strade_continue(part, t, mozz, True) == 0
        c2 += ok and strade_continue(part, t, mozz) == 0
    uno = (100 * v / prove, 100 * c1 / prove, 100 * c2 / prove)
    fiori = [i for i, p in enumerate(part.pezzi) if forma(p) == forma(FIORE)]
    facce = [(i, f) for i in fiori for f in disegni[i]]
    g = c = c3 = 0
    n2 = prove // 4
    for _ in range(n2):
        k = rnd.choice(NOMI)
        t, muri, mozz = rimonta(part, k)
        for pos in fiori:
            src, (celle, mz, mu) = rnd.choice(facce)
            n = rnd.randrange(6)
            mappa = trasporta(part.pezzi[src], part.pezzi[pos], n)
            vecchi = {frozenset(m) for m in part.faccia(pos, k)[2]}
            mozz = {x for x in mozz if x[0] not in part.pezzi[pos]}
            t.update({mappa[h]: x for h, x in celle})
            mozz |= {(mappa[a], _vicino_ruotato(a, b, mappa, n)) for a, b in mz}
            nuovi = {frozenset((mappa[a], mappa[b] if b in mappa else _vicino_ruotato(a, b, mappa, n)))
                     for a, b in (m if m[0] in mappa else m[::-1] for m in mu)}
            muri = (muri - vecchi) | {m for m in nuovi if all(h in AX for h in m)}
        gr, co = valida_libera(t, muri)
        g += gr
        c += co
        c3 += co and strade_continue(part, t, mozz, True) == 0
    return uno, (100 * g / n2, 100 * c / n2, 100 * c3 / n2)


FIORE = frozenset(HX[(3 + a, 3 + b)] for a, b in [(0, 0)] + D6)


def _r60(q, r, n):
    for _ in range(n):
        q, r = -r, q + r
    return q, r


def _centro(p):
    return next(h for h in p if all(HX.get((AX[h][0] + a, AX[h][1] + b)) in p for a, b in D6))


def trasporta(da, a, n):
    """esagono del fiore `da` -> esagono del fiore `a`, girando di 60°·n attorno al centro."""
    cd, ca = AX[_centro(da)], AX[_centro(a)]
    out = {}
    for h in da:
        q, r = _r60(AX[h][0] - cd[0], AX[h][1] - cd[1], n)
        out[h] = HX[(ca[0] + q, ca[1] + r)]
    return out


def _vicino_ruotato(a, b, mappa, n):
    """mozzicone (a -> b fuori dal fiore): stessa direzione, girata di 60°·n, a partire dall'esagono nuovo di a."""
    dq, dr = AX[b][0] - AX[a][0], AX[b][1] - AX[a][1]
    q, r = _r60(dq, dr, n)
    na = AX[mappa[a]]
    return HX.get((na[0] + q, na[1] + r), ('fuori', mappa[a], q, r))


# ------------------------------------------------------------------ 5. stampa: quanti pezzi in un foglio A4
def per_foglio(pagina=(297, 210), margine=6, testata=12, piede=8, abb=1.5, spazio=0.6):
    """fiori interi a nido d'ape (reticolo dei fiori allargato finché tra due abbondanze restano `spazio` mm)."""
    def centro(q, r):
        return W * (q + r / 2), 1.5 * R * r

    def vertici(x, y):
        return [(x + R * math.cos(math.radians(a)), y + R * math.sin(math.radians(a))) for a in range(-90, 270, 60)]

    def punti(ox, oy):
        return [p for q, r in [(0, 0)] + D6 for p in vertici(ox + centro(q, r)[0], oy + centro(q, r)[1])]

    def lati(ox, oy):
        out = []
        for q, r in [(0, 0)] + D6:
            v = vertici(ox + centro(q, r)[0], oy + centro(q, r)[1])
            out += [(v[i], v[(i + 1) % 6]) for i in range(6)]
        return out

    def dist(p, a, b):
        (px, py), (ax, ay), (bx, by) = p, a, b
        dx, dy = bx - ax, by - ay
        u = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - ax - u * dx, py - ay - u * dy)

    s = 1.0
    while True:
        v1 = tuple(c * s for c in centro(2, 1))
        v2 = tuple(c * s for c in centro(-1, 3))
        vv = [v1, v2, (v1[0] - v2[0], v1[1] - v2[1])]
        if min(dist(p, a, b) for v in vv for p in punti(0, 0) for a, b in lati(*v)) >= 2 * abb + spazio:
            break
        s += 0.005
    xs = [p[0] for p in punti(0, 0)]
    ys = [p[1] for p in punti(0, 0)]
    x0, x1, y0, y1 = min(xs) - abb, max(xs) + abb, min(ys) - abb, max(ys) + abb
    pw, ph = pagina
    best = 0
    for ox in range(0, 80, 2):
        for oy in range(0, 80, 2):
            n = sum(1 for i in range(-6, 8) for j in range(-6, 8)
                    if margine <= ox + i * v1[0] + j * v2[0] + x0 and ox + i * v1[0] + j * v2[0] + x1 <= pw - margine
                    and margine + testata <= oy + i * v1[1] + j * v2[1] + y0 and oy + i * v1[1] + j * v2[1] + y1 <= ph - margine - piede)
            best = max(best, n)
    return best


# ------------------------------------------------------------------ 6. tempi
def tempo_fiori(part, fisici, p, persone=1):
    """montaggio di un preset: per posizione leggi il codice sullo schema, trova la pila della posizione (Hick sulle
    pile), cerca nella pila la faccia del preset (in media metà dei pezzi, a volte girandoli), prendi, accosta ai vicini
    (Fitts, 2 mm), orienta (freccia «nord» stampata), urti dei pezzi medi; poi controllo e tempo fisso del modello."""
    k = ts.k
    pile = collections.Counter(f[0][0] for f, _ in fisici)          # pezzi per coppia di posizioni
    giro = 0.5 * {'veloce': 0.4, 'tipico': 0.6, 'lento': 0.9}[p]    # metà dei pezzi va girata per vedere l'altra faccia
    lavoro = 0
    for i, j in part.coppie:
        n = pile[(i, j)]
        cerca = k('confronto', p) * (n + 1) / 2 + giro * (n + 1) / 2 if n > 2 else 0
        uno = (k('lettura_pezzo', p) + ts.hick(p, len(part.coppie)) + cerca + k('presa_medio', p)
               + ts.fitts(p, 'toll_tile') + k('orienta_grande', p) + k('urti_medio', p))
        lavoro += 2 * uno
    n = len(part.pezzi)
    lavoro += n * (k('controllo', p) + k('errori', p) * k('correggi', p))
    fisso = k('apertura', p) + k('sala', p)
    return fisso + (lavoro if persone == 1 else lavoro / (1 + k('efficienza2', p)))


def cambio_fiori(part, fisici, p):
    """cambio di mappa a metà partita base -> TM (R 8.12): si cambiano solo i pezzi con la faccia diversa; le tessere
    Esplorazione sulle «?» di quei pezzi passano sul pezzo nuovo."""
    k = ts.k
    tot = []
    for x in NOMI[1:]:
        cambia = [i for i in range(len(part.pezzi)) if part.faccia(i, 'base') != part.faccia(i, x)]
        dom = sum(1 for i in cambia for h in part.pezzi[i] if h in ts.mappa.DOMANDE)
        posa = tempo_fiori(part, fisici, p) - k('apertura', p) - k('sala', p)     # posa di tutti i pezzi
        tot.append(len(cambia) / len(part.pezzi) * posa + len(cambia) * k('togli', p) + dom * k('gettone', p))
    return statistics.mean(tot)


def mm_ss(s):
    s = round(s)
    return f'{s // 60}:{s % 60:02d}'


def tab(righe, intest):
    print('| ' + ' | '.join(intest) + ' |')
    print('|' + '---|' * len(intest))
    for r in righe:
        print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print()


# ------------------------------------------------------------------ scelta
FUSIONI = [('A5', 'B4')]   # l'acqua A5 (un esagono da solo sul bordo) va sul fiore del guado ovest; J6 su quello di I7
# posti in un foglio A4 (in fiori interi) per forma: stima per pezzi di bordo che si incastrano tra i fiori
POSTI = {1: 0.2, 2: 0.35, 3: 0.5, 4: 0.6, 5: 0.8, 7: 1.0, 8: 1.25}


def scelta():
    return Partizione(unisci(griglia(1, 3, 5), FUSIONI))


def main():
    print('## Griglie di fiori\n')
    righe = []
    for a, b in ((1, 3), (1, 5)):
        for off in range(7):
            g = griglia(a, b, off)
            sz = collections.Counter(len(p) for p in g)
            righe.append((f'({a},{b}) +{off}', len(g), sz[7], len(g) - sz[7], ' '.join(f'{n}×{c}' for n, c in sorted(sz.items(), reverse=True) if n < 7),
                          'sì' if simmetrica(g) else ''))
    tab(righe, ('griglia', 'pezzi', 'fiori interi', 'pezzi di bordo', 'misure dei pezzi di bordo', 'identica girata di 180°'))
    varianti = []
    for nome, (a, b, off), fus in [('(1,3)+5 senza fusioni', (1, 3, 5), []), ('(1,3)+5 + E1-F1 sulla striscia B1-D1', (1, 3, 5), [('E1', 'D1')]),
                                   ('(1,3)+5 + A5 sul fiore vicino (scelta)', (1, 3, 5), FUSIONI),
                                   ('(1,3)+5 + A5 + E1-F1', (1, 3, 5), FUSIONI + [('E1', 'D1')]), ('(1,5)+3 senza fusioni', (1, 5, 3), [])]:
        for mz, mu in (('area', 'stampati'), ('area', 'listelli'), ('sentiero', 'stampati'), ('sentiero', 'listelli')):
            if mz != 'area' and 'scelta' not in nome:
                continue
            pt = Partizione(unisci(griglia(a, b, off), fus), mz, mu)
            fis = pezzi_fisici(pt)
            nd = sum(len(pt.disegni(i)) for i, _ in pt.coppie)
            varianti.append((nome, f'{mz}, {mu}', len(pt.pezzi), nd, len(fis), sum(1 for _, r in fis if r is None)))
    tab(varianti, ('partizione', 'strade, muri', 'pezzi a partita', 'disegni (facce)', 'pezzi fisici', 'di cui con retro libero'))

    part = scelta()
    fis = pezzi_fisici(part)
    print('## Partizione scelta\n')
    righe = []
    for i, j in part.coppie:
        p = part.pezzi[i]
        dd = part.disegni(i)
        righe.append((f'{i}/{j}', len(p), ' '.join(sorted(p, key=TUTTI.index)), ' '.join(sorted(part.pezzi[j], key=TUTTI.index)),
                      len([h for h in p if h in ts.VARIABILI]), len(dd), sum(1 for f, _ in fis if f[0] == (i, j))
                      + sum(1 for _, r in fis if r and r[0] == (i, j)),
                      'sì' if forma(p) == specchio(p) else 'no'))
    tab(righe, ('posizioni N/S', 'esagoni', 'esagoni (nord)', 'esagoni (sud)', 'che cambiano', 'disegni', 'facce stampate', 'retro possibile'))
    nd = sum(len(part.disegni(i)) for i, _ in part.coppie)
    liberi = [f[0] for f, r in fis if r is None]
    pf = per_foglio()
    posti = sum(POSTI[len(part.pezzi[f[0][0]])] for f, _ in fis)
    print(f'Pezzi a partita: {len(part.pezzi)}. Disegni (facce diverse): {nd}, ognuno in 2 copie (nord e sud) = {2 * nd} facce. '
          f'Pezzi fisici: {len(fis)} ({len(fis) - len(liberi)} fronte/retro, {len(liberi)} col retro libero, posizioni '
          f'{", ".join(f"{i}/{j}" for i, j in liberi)}). Muri sul taglio: {len(part.muri_taglio)}.')
    print(f'Fiori interi per foglio A4 orizzontale (abbondanza 1,5 mm, 0,6 mm tra due abbondanze): {pf}. '
          f'Pezzi fisici in «posti da fiore»: {posti:.1f} -> {math.ceil(posti / pf)} fogli di fronti + '
          f'{math.ceil(posti / pf)} di retri (stima).\n')

    print('## Controlli dei preset rimontati\n')
    tab(controlli_preset(part), ('preset', 'identico all\'originale', 'lati con strada che non prosegue', 'controlli §17', 'Partenza→Cripta', 'Cripta più vicina'))

    print('## Composizione libera\n')
    (v1, m1, c1), (g2, v2, c2) = combinazioni_libere(part)
    print(f'Casuale per posizione (ogni pezzo da un preset a caso): {v1:.1f} % validi §17, {m1:.1f} % anche senza passaggi '
          f'non disegnati, {c1:.1f} % con le strade del tutto continue.')
    print(f'Casuale, fiori ovunque (fiori interi a caso, girati a caso): {g2:.1f} % con il grafo valido, {v2:.1f} % validi §17 '
          f'(Partenze 1-6 e Cripte 1-4 una volta), {c2:.1f} % anche senza passaggi non disegnati.')

    (n1, a1, b1, c1), (n2, a2, b2, c2) = varianti_guidate(part)
    print(f'Guidata, una coppia di pezzi (nord e sud) da un altro preset: {n1} mappe diverse, {a1:.1f} % validi §17, '
          f'{b1:.1f} % senza passaggi non disegnati, {c1:.1f} % con le strade del tutto continue.')
    print(f'Guidata, metà nord di un preset e metà sud di un altro: {n2} mappe, {a2:.1f} % validi §17, {b2:.1f} % senza '
          f'passaggi non disegnati, {c2:.1f} % con le strade del tutto continue.\n')

    print('## Tempi\n')
    righe = []
    for nome, f in (('montaggio, 1 persona', lambda p: tempo_fiori(part, fis, p)), ('montaggio, 2 persone', lambda p: tempo_fiori(part, fis, p, 2)),
                    ('cambio mappa R 8.12', lambda p: cambio_fiori(part, fis, p)),
                    ('riordino', lambda p: len(part.pezzi) * ts.k('togli', p))):
        righe.append((nome,) + tuple(mm_ss(f(p)) for p in ts.PROFILI))
    tab(righe, ('', 'veloce', 'tipico', 'lento'))
    if '--catalogo' in sys.argv:
        print('## Catalogo dei pezzi fisici\n')
        righe = []
        for n, (f, r) in enumerate(fis, 1):
            righe.append((n, f'{f[0][0]}/{f[0][1]}', ' '.join(f[2]), f'{r[0][0]}/{r[0][1]}' if r else '—', ' '.join(r[2]) if r else 'libero'))
        tab(righe, ('pezzo', 'fronte: posizioni', 'fronte: preset', 'retro: posizioni', 'retro: preset'))


if __name__ == '__main__':
    main()
