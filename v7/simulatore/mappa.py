"""Plancia del playtest v7 (Spec_v7.md §17): grafo delle strade, muri, distanze, movimento."""
from collections import deque

COLONNE = 'ABCDEFGHIJ'

_STRADA = """C1 D1 G1 H1 I1 B2 C2 D2 F2 H2 B3 C3 D3 E3 G3 H3 I3 B4 C4 D4 E4 F4 G4 H4 I4 J4
G5 H5 I5 J5 A6 B6 C6 D6 A7 B7 C7 D7 E7 F7 G7 H7 I7 B8 C8 D8 F8 G8 H8 I8 C9 E9 G9 H9 I9
B10 C10 D10 G10 H10"""
_GUADI = "D5 F5 E6 G6"
STRADA = frozenset(_STRADA.split() + _GUADI.split())

PARTENZE = {1: 'C1', 2: 'H1', 3: 'J5', 4: 'H10', 5: 'C10', 6: 'A6'}
CRIPTE = {1: 'D4', 2: 'G4', 3: 'D7', 4: 'G7'}
DOMANDE = tuple("B3 B7 C4 C6 C8 C9 D1 E3 E7 E9 F2 F4 F8 G10 H2 H3 H5 H7 I4 I8".split())

_MURI = """D3|D4 D4|E3 G4|H3 G4|H4 G4|H5 C6|D7 C7|D7 C8|D7 F8|G7 G7|G8
C8|C9 D2|D3 D2|E3 F8|G9 G8|G9 H2|H3"""
MURI = frozenset(frozenset(m.split('|')) for m in _MURI.split())


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


VICINI = {h: tuple(v for v in _vicini_geo(h) if v in STRADA and frozenset((h, v)) not in MURI)
          for h in STRADA}


def _bfs(da, bloccati=frozenset()):
    dist = {da: 0}
    coda = deque([da])
    while coda:
        h = coda.popleft()
        if h != da and h in bloccati:
            continue  # ci si ferma, non si attraversa (R 8.5)
        for v in VICINI[h]:
            if v not in dist:
                dist[v] = dist[h] + 1
                coda.append(v)
    return dist


DIST = {h: _bfs(h) for h in STRADA}


def accanto(a, b):
    """R 8.7: lato in comune senza muro (tra due esagoni di strada)."""
    return b in VICINI.get(a, ())


def raggiungibili(da, passi, bloccati, occupati):
    """Esagoni dove ci si può fermare con 1..passi passi (R 8.4, R 8.5): si passa sugli eroi ma non ci si
    ferma; i mostri scoperti e la Cripta di MIMI fermano. Senza mete possibili si resta su `da`."""
    dist = _bfs(da, bloccati)
    mete = {h: d for h, d in dist.items() if 1 <= d <= passi and h not in occupati}
    return mete or {da: 0}


def controlla():
    link = sum(len(v) for v in VICINI.values()) // 2
    dd = [DIST[p][c] for p in PARTENZE.values() for c in CRIPTE.values()]
    return {'strada': len(STRADA), 'collegamenti': link, 'partenza_cripta_min': min(dd),
            'partenza_cripta_max': max(dd), 'partenza_cripta_media': sum(dd) / len(dd)}


if __name__ == '__main__':
    print(controlla())
