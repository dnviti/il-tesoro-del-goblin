"""Mappa 12×12 del playtest v7 (D24, D25): base stampata (46 esagoni di bordo, 6 Partenze, 4 ostacoli singoli) e
14 fiori a due facce posati nei 14 spazi, con un draft o con un preset (Strettoie + uno per Mappa TM). Niente muri:
si cammina ovunque non ci sia un ostacolo; un terreno accidentato costa passi in più (`TERRENI`).
La mappa in uso è `g.plancia` (Plancia). Dati dei pezzi: `DATI_FIORI` (v. sotto)."""
import csv
import heapq
import os
import random

N = 12
CELLE = [(c, r) for r in range(1, N + 1) for c in range(1, N + 1)]
AX = {(c, r): (c - 1 - (r - 1) // 2, r - 1) for c, r in CELLE}     # righe dispari a sinistra di mezzo esagono
HX = {v: k for k, v in AX.items()}
DIR = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]          # anello di un fiore, antiorario: 0 = E

def vicini_geo(h):
    q, r = AX[h]
    return [HX[(q + a, r + b)] for a, b in DIR if (q + a, r + b) in HX]


def distanza(a, b):
    (q1, r1), (q2, r2) = AX[a], AX[b]
    return max(abs(q1 - q2), abs(r1 - r2), abs(q1 - q2 + r1 - r2))


# --- spazi dei fiori e base ---------------------------------------------------------------------------------

def _spazi():
    """Reticolo (q + 5r + 1) mod 7: 14 fiori interi, 46 esagoni sulla base; lo spazio s girato di 180° è 15 − s."""
    g = {}
    for h, (q, r) in AX.items():
        f = lambda qq, rr: (qq + 5 * rr + 1) % 7        # noqa: E731
        c = (q, r) if f(q, r) == 0 else next((q + x, r + y) for x, y in DIR if f(q + x, r + y) == 0)
        g.setdefault(c, set()).add(h)
    centri = sorted((c for c, s in g.items() if len(s) == 7), key=lambda c: (c[1], c[0]))
    spazi = {i: HX[c] for i, c in enumerate(centri, 1)}
    base = sorted(set(CELLE) - {h for c in centri for h in g[c]}, key=lambda h: (h[1], h[0]))
    assert len(spazi) == 14 and len(base) == 46
    return spazi, base


SPAZI, BASE_ESAGONI = _spazi()


def anello(s, k):
    """Esagono in direzione k (0-5) attorno al centro dello spazio s."""
    q, r = AX[SPAZI[s]]
    return HX[(q + DIR[k][0], r + DIR[k][1])]


# --- dati dei pezzi (v7/stampa/sorgenti/dati: fiori.csv, base12.csv, preset12.csv) ---------------------------------

DATI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stampa', 'sorgenti', 'dati')
BASE = 'Strettoie'          # preset del montaggio veloce senza carta Mappa
N_TESSERE = 24        # D29: tessere Esplorazione sulla mappa (le altre 12 in riserva)


def _csv(nome):
    with open(os.path.join(DATI, nome), encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def _carica():
    """Legge i pezzi dai CSV del kit. Terreno: ostacolo (non ci si entra) o percorribile; `accidentato` = 1 passo in
    più per entrarci (D25): il costo di ogni terreno viene dai dati, l'IA non conosce l'acqua."""
    terreni = {}                      # nome -> (ostacolo, extra)
    fiori = {}                        # (fiore 0-13, faccia 0|1) -> (centro, anello[6])
    for r in _csv('fiori.csv'):
        terreni[r['terreno']] = (r['categoria'] == 'ostacolo', int(r['accidentato']))
        f = fiori.setdefault((int(r['fiore']) - 1, 'AB'.index(r['faccia'])), [None, [None] * 6])
        if int(r['posizione']) == 0:
            f[0] = r['terreno']
        else:
            f[1][int(r['posizione']) - 1] = r['terreno']
    base, partenze = {}, {}
    for r in _csv('base12.csv'):
        if r['parte'] == 'base':
            h = (int(r['x']), int(r['y']))
            terreni[r['terreno']] = (r['categoria'] == 'ostacolo', int(r['accidentato']))
            base[h] = r['terreno']
            if r['partenza']:
                partenze[int(r['partenza'])] = h
    preset, cambio = {}, {}
    for r in _csv('preset12.csv'):
        v = (int(r['fiore']) - 1, 'AB'.index(r['faccia']), int(r['freccia']) - 1)
        preset.setdefault(r['preset'], {})[int(r['spazio'])] = v
        if r['cambio'] and r['carta']:
            cambio.setdefault(r['carta'], []).append((int(r['cambio']), (int(r['spazio']), v)))
    fiori = {k: (v[0], tuple(v[1])) for k, v in fiori.items()}
    cambi = {c: [x for _, x in sorted(v)] for c, v in cambio.items()}
    assert len(fiori) == 28 and len(base) == 46 and len(partenze) == 6 and len(preset) == 10, 'CSV dei pezzi incompleti'
    return terreni, fiori, base, [partenze[i] for i in range(1, 7)], preset, cambi


TERRENI, FIORI, BASE_TERRENO, PARTENZE, PRESET, CAMBI = _carica()


class Plancia:
    """Una mappa montata: terreno di ogni esagono, vicini percorribili, distanze in passi (con i costi del terreno)."""

    def __init__(self, terreno):
        self.terr = terreno
        self.libero = frozenset(h for h in CELLE if not TERRENI[terreno[h]][0])
        self.uscita = {h: TERRENI[terreno[h]][1] for h in self.libero}      # D25: costo in più per uscirne      # passi per entrarci
        self.vicini = {h: tuple(v for v in vicini_geo(h) if v in self.libero) for h in self.libero}
        self._dist = {}

    @property
    def dist(self):
        return self

    def __getitem__(self, da):
        """dist[da][h]: passi minimi da `da` a `h` (ostacoli esclusi, costi del terreno compresi)."""
        d = self._dist.get(da)
        if d is None:
            d = self._dist[da] = self._dijkstra(da)
        return d

    def _dijkstra(self, da, bloccati=frozenset(), limite=None):
        dist = {da: 0}
        coda = [(0, da)]
        while coda:
            c, h = heapq.heappop(coda)
            if c > dist[h] or (h != da and h in bloccati):
                continue                                   # ci si ferma, non si attraversa (R 8.5)
            for v in self.vicini[h]:
                n = c + 1 + self.uscita[h]
                if (limite is None or n <= limite) and n < dist.get(v, 1 << 30):
                    dist[v] = n
                    heapq.heappush(coda, (n, v))
        return dist

    def accanto(self, a, b):
        """R 8.7: lato in comune (tra due esagoni percorribili)."""
        return b in self.vicini.get(a, ())

    def raggiungibili(self, da, passi, bloccati, occupati):
        """Esagoni dove ci si può fermare spendendo al massimo `passi` (R 8.4, R 8.5): si passa sugli eroi ma non ci si
        ferma; i mostri scoperti e la Cripta di MIMI fermano; entrare in un terreno accidentato costa di più. Senza
        mete possibili si resta su `da`."""
        dist = self._dijkstra(da, bloccati, passi)
        mete = {h: d for h, d in dist.items() if h != da and h not in occupati}
        return mete or {da: 0}

    def cripta(self, x, y, tessere=()):
        """D24: Cripta sul punto (x, y) tirato con 2D6 + 2D6. Sull'acqua o su una tessera Esplorazione (`tessere`: esagoni
        con una tessera) resta lì. Su un ostacolo o su una Partenza va sull'esagono percorribile più vicino (si contano
        anche gli ostacoli) che non sia Partenza, senza tessera, riga o colonna 1; a pari distanza più in alto, poi più a
        sinistra."""
        h = (x, y)
        if h in self.libero and h not in PARTENZE:
            return h
        return min((v for v in self.libero if v not in PARTENZE and v not in tessere and v[0] > 1 and v[1] > 1),
                   key=lambda v: (distanza(v, h), v[1], v[0]))

    def idonee_tessera(self, occupate):
        """D29: esagoni percorribili ad almeno 2 esagoni da ogni Partenza e non in `occupate` (un'altra tessera, un eroe,
        la Cripta)."""
        return [h for h in CELLE if h in self.libero and h not in occupate and h not in PARTENZE
                and all(distanza(h, p) >= 2 for p in PARTENZE)]


def terreno(disposizione):
    """disposizione: {spazio: (fiore 0-13, faccia 0|1, rotazione 0-5)} -> terreno di ogni esagono."""
    t = dict(BASE_TERRENO)
    for s, (i, lato, rot) in disposizione.items():
        centro, anl = FIORI[i, lato]
        t[SPAZI[s]] = centro
        for k in range(6):
            t[anello(s, (k + rot) % 6)] = anl[k]
    assert len(t) == N * N
    return t


def draft(n, rng):
    """Draft con n giocatori (2: 7 fiori a testa; 3: 4; 4: 3; gli avanzi li posano l'ultimo e il penultimo): ognuno posa i
    suoi fiori in turno, in uno spazio libero a caso, con faccia e rotazione a caso. Ritorna la disposizione."""
    fiori = list(range(14))
    rng.shuffle(fiori)
    a_testa = 14 // n
    mani = [fiori[i * a_testa:(i + 1) * a_testa] for i in range(n)]
    avanzi = fiori[n * a_testa:]
    ordine = [i for _ in range(a_testa) for i in range(n)] + [n - 1, n - 2][:len(avanzi)]
    pezzi = [m.pop() for m in (mani[i] for i in ordine[:n * a_testa])] + avanzi
    spazi = list(SPAZI)
    rng.shuffle(spazi)
    return {s: (f, rng.randrange(2), rng.randrange(6)) for s, f in zip(spazi, pezzi)}


def disposizione_preset(nome):
    return dict(PRESET[nome])


def disposizione(montaggio, mappa):
    """Montaggio con i 3 fiori della carta Mappa `mappa` (None: il montaggio com'è). Per ognuna delle 3 righe, in ordine:
    se il fiore sta in un altro spazio, si scambia con quello che occupa lo spazio indicato (il fiore tolto va nello
    spazio liberato con la sua faccia e rotazione); poi si mette la faccia e la rotazione indicate."""
    d = dict(montaggio)
    for s, (i, lato, rot) in CAMBI[mappa] if mappa else ():
        dove = next(x for x, v in d.items() if v[0] == i)
        if dove != s:
            d[dove] = d[s]
        d[s] = (i, lato, rot)
    return d


def esagoni_fiori(spazi):
    return {h for s in spazi for h in [SPAZI[s]] + [anello(s, k) for k in range(6)]}


def controlla(t):
    """Collegamento: tutti gli esagoni percorribili formano un solo pezzo (ostacoli esclusi, acqua compresa)."""
    p = Plancia(t)
    da = next(iter(p.libero))
    return len(p._dijkstra(da)) == len(p.libero), len(p.libero)


if __name__ == '__main__':
    rng = random.Random(1)
    for nome in PRESET:
        ok, lib = controlla(terreno(PRESET[nome]))
        print(nome, 'collegata' if ok else 'NON collegata', f'percorribili {lib}')
    cattive = sum(not controlla(terreno(draft(rng.choice((2, 3, 4)), rng)))[0] for _ in range(2000))
    print('draft a caso non collegati su 2000:', cattive)
