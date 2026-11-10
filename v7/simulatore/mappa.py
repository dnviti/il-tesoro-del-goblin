"""Plancia base del playtest v7, «Strettoie» (Spec_v7.md §17), e plance delle 9 Mappe (R 8.12, plance/<tema>.py,
stessi campi dati): grafo delle strade, muri, distanze, movimento. La plancia in uso è `g.plancia` (Plancia)."""
import os
import runpy
from collections import deque

COLONNE = 'ABCDEFGHIJ'

_STRADA = """A1 B1 C1 H1 I1 J1 A2 C2 H2 I2 J2 A3 D3 E3 G3 H3 J3 A4 B4 C4 D4 E4 F4 G4 H4 J4 G5 H5 I5 J5 A6 B6 C6 D6 A7 C7 D7
E7 F7 G7 H7 I7 J7 A8 C8 D8 F8 G8 J8 A9 B9 C9 H9 J9 A10 B10 C10 H10 I10 J10"""
_GUADI = "D5 F5 E6 G6"

# Parti fisse, uguali su tutte le plance (R 8.12): le plance/ le ripetono e Plancia() le controlla.
PARTENZE = {1: 'C1', 2: 'H1', 3: 'J5', 4: 'H10', 5: 'C10', 6: 'A6'}
CRIPTE = {1: 'D4', 2: 'G4', 3: 'D7', 4: 'G7'}
DOMANDE = tuple("A1 A9 B6 B9 B10 C2 C7 D3 D6 E3 F8 G5 G8 H4 H9 I1 I2 I5 J2 J10".split())

_MURI = """D3|D4 D4|E3 G4|H3 G4|H4 G4|H5 C6|D7 C7|D7 C8|D7 F8|G7 G7|G8
A9|B9 B6|C7 C6|D6 G5|H5 H4|I5 I2|J2"""

BOSCO = "F1 G1 F2 G2 I3 I4 B7 B8 D9 E9 D10 E10"
CASE = "D1 E1 D2 G9 F10 G10"
ROCCE = "B2 E2 B3 C3 F3 E8 H8 I8 F9 I9"
ACQUA = "A5 B5 C5 E5 F6 H6 I6 J6"

# Mappa -> file della sua plancia in plance/ (R 8.12, tabella del §17).
TEMI = {'TM-01': 'forziere', 'TM-02': 'citta', 'TM-03': 'foresta', 'TM-04': 'tundra', 'TM-05': 'sottovelo',
        'TM-06': 'miniera', 'TM-07': 'yuma', 'TM-08': 'flegias', 'TM-09': 'mimi'}


def _cr(h):
    return COLONNE.index(h[0]), int(h[1:])


def _nome(c, r):
    return f"{COLONNE[c]}{r}"


def _vicini_geo(h):
    c, r = _cr(h)
    out = [(c - 1, r), (c + 1, r)]
    dc = (-1, 0) if r % 2 else (0, 1)
    for rr in (r - 1, r + 1):
        out += [(c + dc[0], rr), (c + dc[1], rr)]
    return [_nome(a, b) for a, b in out if 0 <= a < 10 and 1 <= b <= 10]


class Plancia:
    """Grafo di una plancia: strada (+ guadi), muri, vicini, distanze."""

    def __init__(self, nome, d):
        self.nome = nome
        assert (d['PARTENZE'], d['CRIPTE'], tuple(d['DOMANDE'])) == (PARTENZE, CRIPTE, DOMANDE), nome
        self.strada = frozenset(d['_STRADA'].split() + d['_GUADI'].split())
        self.muri = frozenset(frozenset(m.split('|')) for m in d['_MURI'].split())
        self.vicini = {h: tuple(v for v in _vicini_geo(h) if v in self.strada and frozenset((h, v)) not in self.muri)
                       for h in self.strada}
        self.dist = {h: self._bfs(h) for h in self.strada}

    def _bfs(self, da, bloccati=frozenset()):
        dist = {da: 0}
        coda = deque([da])
        while coda:
            h = coda.popleft()
            if h != da and h in bloccati:
                continue  # ci si ferma, non si attraversa (R 8.5)
            for v in self.vicini[h]:
                if v not in dist:
                    dist[v] = dist[h] + 1
                    coda.append(v)
        return dist

    def accanto(self, a, b):
        """R 8.7: lato in comune senza muro (tra due esagoni di strada)."""
        return b in self.vicini.get(a, ())

    def raggiungibili(self, da, passi, bloccati, occupati):
        """Esagoni dove ci si può fermare con 1..passi passi (R 8.4, R 8.5): si passa sugli eroi ma non ci si
        ferma; i mostri scoperti e la Cripta di MIMI fermano. Senza mete possibili si resta su `da`."""
        dist = self._bfs(da, bloccati)
        mete = {h: d for h, d in dist.items() if 1 <= d <= passi and h not in occupati}
        return mete or {da: 0}

    def controlla(self):
        link = sum(len(v) for v in self.vicini.values()) // 2
        dd = [self.dist[p][c] for p in PARTENZE.values() for c in CRIPTE.values()]
        return {'strada': len(self.strada), 'collegamenti': link, 'partenza_cripta_min': min(dd),
                'partenza_cripta_max': max(dd), 'partenza_cripta_media': round(sum(dd) / len(dd), 2)}


BASE = Plancia('base', globals())
_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plance')
PLANCE = {tm: Plancia(tema, runpy.run_path(os.path.join(_DIR, tema + '.py'))) for tm, tema in TEMI.items()}


if __name__ == '__main__':
    for nome, p in [('base', BASE)] + [(f"{tm} {p.nome}", p) for tm, p in PLANCE.items()]:
        print(nome, p.controlla())
