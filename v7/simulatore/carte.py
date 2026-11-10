"""Dati del kit v7 letti dai CSV (Spec_v7.md §14.1) e tabella degli effetti (effetti.csv)."""
import csv
import os
from dataclasses import dataclass, field

QUI = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.join(os.path.dirname(QUI), 'stampa', 'sorgenti', 'dati')
CLASSI = ('Assaltatore', 'Ricercatore', 'Stregone', 'Oracolo', 'Giullare')
SLOT = ('Elmo', 'Arma DX / Scudo', 'Arma SX', 'Armatura')


def _righe(nome):
    with open(os.path.join(DATI, nome), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _num(v):
    try:
        return int(v)
    except ValueError:
        return v


def parametri(s):
    out = {}
    for pezzo in filter(None, (x.strip() for x in s.split(';'))):
        k, _, v = pezzo.partition('=')
        out[k] = _num(v) if v else True
    return out


@dataclass
class Carta:
    id: str
    tipo: str          # TE, TI, TM
    nome: str
    classe: str        # '' per il mazzo comune
    direzione: str
    pl: int
    slot: str
    codice: str = 'info'
    p: dict = field(default_factory=dict)

    @property
    def equip(self):
        return self.tipo == 'TE'


@dataclass
class Mostro:
    id: str
    nome: str
    tier: int
    lv: int
    pv: int
    att: int
    ar: int


def _carica_effetti():
    eff = {}
    for r in csv.DictReader(open(os.path.join(QUI, 'effetti.csv'), encoding='utf-8')):
        eff[r['id']] = (r['codice'], parametri(r['parametri']))
    return eff


EFFETTI = _carica_effetti()
CARTE = {}
COMUNI = []
CARTE_CLASSE = {c: [] for c in CLASSI}
TESTI = {}                                     # id -> riga CSV (testo stampato, per --verifica-carte)
for _r in _righe('carte_comuni.csv') + [r for c in CLASSI for r in _righe(os.path.join('classi', c.lower() + '.csv'))]:
    _cod, _p = EFFETTI.get(_r['id'], ('info', {}))
    _c = Carta(_r['id'], _r['tipo'], _r['nome'], '' if _r['classe'] in ('Tutte le classi', 'Comune') else _r['classe'],
               _r['direzione'], int(_r['pl'] or 0), _r['slot'], _cod, _p)
    CARTE[_c.id] = _c
    (CARTE_CLASSE[_c.classe] if _c.classe else COMUNI).append(_c.id)
    TESTI[_c.id] = _r

MANCANTI = sorted(set(CARTE) - set(EFFETTI))   # carte senza riga in effetti.csv: trattate come 'info'

MOSTRI = {}
for _r in _righe('carte_mostro.csv'):
    MOSTRI[_r['id']] = Mostro(_r['id'], _r['nome'], int(_r['mazzetto'][0]), int(_r['lv']), int(_r['pv']),
                              int(_r['att']), int(_r['ar']))
MAZZETTI = {t: [m for m, x in MOSTRI.items() if x.tier == t] for t in (1, 2, 3)}
# D19: AR dei mostri = ceil(AR v6 x 0,75), scritta nel CSV (8->6 ... 11->9). Se il CSV ha ancora le AR v6 (8-11),
# il simulatore applica D19 da sé e lo dice nel rapporto (AR_CSV_V7 = False).
AR_CSV_V7 = max(m.ar for m in MOSTRI.values()) <= 9
AR_V7_A_V6 = {6: 8, 7: 9, 8: 10, 9: 11}
if not AR_CSV_V7:
    for _m in MOSTRI.values():
        _m.ar = -(-_m.ar * 3 // 4)

IMPREVISTI = []
for _r in _righe('carte_imprevisto.csv'):
    IMPREVISTI.append(_r['nome'])
TESSERE = [r['colore'] for r in _righe('tessere_esplorazione.csv')]     # 'rossa' / 'blu'
SPECIE = [r['specie'] for r in _righe('carte_specie.csv')]               # 8 carte, 2 per specie

# Scelte «a scelta» delle Carte Specie fatte dall'IA (R 3.5): ATT, poi MOV.
BONUS_SPECIE = {
    'Umano': {'mov': 1, 'att': 1},
    'Elfo': {'att': 2},
    'Sanguar': {'mov': 2},
    'Yumaniano': {'ar': 1, 'att': 1},
}

# Abilità dei mostri: abilita_mostri.csv (id -> codici con parametri, separati da «+»); senza riga = 'info'.
ABILITA = {m: [('info', {})] for m in MOSTRI}
for _r in csv.DictReader(open(os.path.join(QUI, 'abilita_mostri.csv'), encoding='utf-8')):
    if _r['id'] in MOSTRI:
        _pp = _r['parametri'].split('+')
        ABILITA[_r['id']] = [(c.strip(), parametri(_pp[i] if i < len(_pp) else ''))
                             for i, c in enumerate(_r['codice'].split('+'))]

# Valore indicativo per l'IA: quanto vale tenere una carta in mano (più alto = si scarta per ultima).
VALORE_CODICE = {
    'equip': 5, 'danno': 4, 'mod_tiro': 4, 'ritira': 4, 'parata': 4, 'buff': 3, 'cura': 3, 'mappa': 3,
    'annulla': 3, 'malus': 3, 'fv': 3, 'riduzione': 3, 'stato': 2, 'recupera': 2, 'nani': 3, 'velo': 2,
    'stato_avv': 2, 'mill': 2, 'ruba': 2, 'scambia': 1, 'speziale': 2, 'torna_partenza': 2, 'perdita_tutti': 1,
    'vera_volonta': 3, 'tempo_scaduto': 1, 'ristom': 2, 'maledizione': 2, 'amisal': 1, 'scry_imp': 1, 'info': 0,
}


def valore(cid):
    c = CARTE[cid]
    return VALORE_CODICE.get(c.codice, 1) + (c.pl if c.equip else 0) + (1 if c.classe else 0)


if __name__ == '__main__':
    from collections import Counter
    print(len(COMUNI), 'comuni', {k: len(v) for k, v in CARTE_CLASSE.items()}, 'senza effetto:', MANCANTI)
    print({t: len(v) for t, v in MAZZETTI.items()}, Counter(IMPREVISTI), Counter(TESSERE), Counter(SPECIE))
    print('AR mostri v7 nel CSV:', AR_CSV_V7, sorted({m.ar for m in MOSTRI.values()}))
