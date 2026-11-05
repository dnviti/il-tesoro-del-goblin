#!/usr/bin/env python3
"""Collaudo del kit di playtest del 5/11/2026 («Il Tesoro del Goblin»).

Legge i dati stampati (stampa/sorgenti/dati/*.csv) e fa due cose:
  --esatto      probabilità esatte degli scontri eroe contro mostro (2D6 + ATT >= 8 + AR,
                tabella dei danni per LV, iniziativa 1 D6 con i pareggi decisi dall'autore)
  --partite N   Monte Carlo di N partite intere per ogni numero di giocatori (2, 3, 4)
  --senza-carte / --danno autore   varianti di sensibilità (mani vuote; danno D6 + ATT - AR dell'autore)

Comandi usati per simulazioni/playtest_2026-11-05.txt (dalla radice del repository):
  python3 gioco/sorgenti/sim_playtest.py --esatto --partite 10000 --uscita simulazioni/playtest_2026-11-05.txt
  python3 gioco/sorgenti/sim_playtest.py --partite 10000 --senza-carte >> simulazioni/playtest_2026-11-05.txt
  python3 gioco/sorgenti/sim_playtest.py --partite 10000 --danno autore >> simulazioni/playtest_2026-11-05.txt

Solo libreria standard. Le regole e le approssimazioni sono elencate in REGOLE e APPROSSIMAZIONI.
"""
import argparse
import csv
import os
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATI = os.path.join(RADICE, 'stampa', 'sorgenti', 'dati')

VARIANTE = {'senza_carte': False, 'danno': 'tabella'}

REGOLE = """Regole simulate (bozza del 3/11 + decisioni dell'autore + D-1/D-2 provvisorie):
- Eroe: PV 5, ATT 1, MOV 1, AR 1 (scheda). Assaltatore +1 PV e Forte Volontà a ogni scontro vinto,
  spesa per -1 AR al nemico; Ricercatore +2 MOV; Stregone 2 rilanci dei propri dadi per turno;
  Oracolo torna in vita con 3 PV, si ricarica con la Locanda.
- Specie a caso tra le 8 tessere: Umano +1 MOV +1 ATT; Elfo +1 ATT +1 AR; Sanguar +2 MOV;
  Yumaniano +1 AR +1 ATT (scelte a scelta fatte dall'IA).
- Livelli a PE 2/4/6/8 (massimo 5): +1 ATT, +2 PV, +1 AR, +2 PV in quest'ordine.
- Turno: Clessidra (salta) -> carte (max 2, equip solo a inizio turno, max 1) -> D6 + MOV (min 1)
  -> esplora -> fine. Plancia 10 x 10 di svg.py: 6 partenze, 4 Cripte, 36 caselle «?».
- «?»: si pesca dal sacchetto (25 rosse, 11 blu); a sacchetto vuoto non succede niente; la casella resta «?».
  Rossa: mostro del mazzetto del livello (1-2 / 3-4 / 5); se perdi la tessera resta scoperta e chi si
  ferma lì gira la carta del suo mazzetto; la carta va in fondo. Blu: mazzetto Imprevisti (11 carte).
- Scontro: iniziativa 1 D6 a testa; pareggio: col mostro vince l'eroe, col boss il boss;
  Agguato/Fauci = il mostro attacca per primo senza tiro. Colpo se 2D6 + ATT >= 8 + AR, nessun critico.
  Danni: eroe D6 + bonus; mostro LV1 D6-1 (min 1), LV2 D6, LV3+ D6+1. Abilità dei mostri applicate.
- Ricompense: mazzetto 1 = 1 Indizio + 1 PE; mazzetto 2 = + Forte Volontà; boss del mazzetto 3 =
  1 Indizio + livello + Forte Volontà. Forte Volontà (max 1): ritira 1 D6 del tiro per colpire mancato.
- Al 3° Indizio (solo la prima volta) MIMI va sulla Cripta del D6 (5-6 si ritira) e gli altri prendono
  1 Indizio. Il boss si sfida con 3 Indizi fermandosi sulla Cripta; le sue ferite restano.
- Sconfitta: ripartenza D6 (ritira se occupata o accanto a un eroe), PV al massimo, tiro di perdita
  equipaggiamento; Indizi tenuti.
- Duello se finisci accanto a un eroe senza aver avuto scontri: lo sfidato può rifiutare dando 1 carta;
  chi vince prende 1 Indizio, 1 PE e la Forte Volontà; pareggio di iniziativa: MOV più alto, poi lo sfidante."""

APPROSSIMAZIONI = """Approssimazioni del Monte Carlo:
- Nessuna fuga (morire riporta i PV al massimo e tiene gli Indizi, quindi fuggire non conviene quasi mai).
- Mappe (TM-01..08), TI-01, TI-05, TI-13, TI-14, TI-18, TI-19, TI-20, TI-21, TI-23 e TI-31 (movimento)
  restano in mano senza effetto; le Mappe quindi non spostano mai il tesoro.
- Equipaggiamenti: solo i bonus a ATT/AR/MOV letti dal testo stampato, più Elmo sorgisogno, Mantello
  delle Braci, Corazza Runica (+2 AR contro LV 3+), Mazza Benedetta, Pugnale Sottile, Bastone del Corvo
  (1 rilancio), Scudo del Goblin; gli altri effetti degli equipaggiamenti sono ignorati.
- Incanti giocati dall'IA: danni (TI-02/09/10/11/16/35/40), +colpire (TI-22/29), +danni (TI-28/37),
  Parata Perfetta, Giuramento di Ferro, +AR (TI-03/27/34), cure (TI-25/26/32), Sguardo Spezzaossa,
  Metamorfosi in Ratto, Parola di Confusione, carte contro le Trappole (TI-06/17/39), Mappa Sussurrata,
  Scintilla di Volontà, rilanci (TI-33/38), Richiamo dal Sepolcro. Contro i mostri normali l'IA gioca
  incanti di danno solo se è in pericolo (PV <= 3) o contro il mazzetto 2; contro il boss gioca tutto.
- Mano: modalità Casual (5 comuni pescate; lo Stregone 4 di classe + 6 comuni). Draft non simulato.
- Nei Duelli niente carte; lo sfidato rifiuta se ha Indizi, carte in mano ed è più debole.
- Tempo reale stimato: 25 s per turno, 15 s per tessera pescata, 30 s per preparare uno scontro,
  12 s per attacco, 10 s per carta giocata, 40 s per sconfitta (ripartenza e tiro di perdita).
- Partita interrotta a 120 round (stallo)."""

# ---------------------------------------------------------------- dati stampati


def leggi(nome):
    with open(os.path.join(DATI, nome), encoding='utf-8') as f:
        return list(csv.DictReader(f))


ABILITA = [('Illusione', 'svantaggio_primo'), ('Picchiata', 'svantaggio_primo'), ('Morso infetto', 'morso'),
           ('Succhiasangue', 'succhia'), ('Codardo', 'codardo'), ('Catene', 'catene'), ('Saccheggio', 'saccheggio'),
           ('Si ricompone', 'ricompone'), ('Inseguitore', 'inseguitore'), ('Ragnatela', 'ragnatela'),
           ('Furia', 'furia'), ('Acido', 'acido'), ('Lento', 'lento'), ('Borseggio', 'borseggio'),
           ('Agguato', 'primo'), ('Fauci', 'primo'), ('Gelo', 'gelo'), ('Carica', 'carica'),
           ('Coriaceo', 'coriaceo'), ('Pietrifica', 'pietrifica'), ('Colpo del custode', 'custode'),
           ('Non morto', 'nonmorto')]


class Mostro:
    def __init__(self, r):
        self.id, self.nome = r['id'], r['nome']
        self.mazzetto = int(r['mazzetto'][0])
        self.lv, self.pv, self.att, self.ar = int(r['lv']), int(r['pv']), int(r['att']), int(r['ar'])
        if int(r['difesa']) != 8 + self.ar:
            raise ValueError(f"{self.id}: difesa {r['difesa']} diversa da 8 + AR")
        d = r['danno'].replace('−', '-').replace(' ', '')
        self.dmod = 0 if d == 'D6' else int(d[2:])
        self.fx = {k for t, k in ABILITA if t in r['abilita']}
        self.boss = self.mazzetto == 3


MOSTRI = [Mostro(r) for r in leggi('carte_mostro.csv')]
SLOT = {'Elmo': 'Elmo', 'Arma DX / Scudo': 'DX', 'Arma SX': 'SX', 'Armatura': 'Armatura'}


def leggi_equip():
    eq = {}
    for r in leggi('carte_comuni.csv') + leggi('carte_classe.csv'):
        if r['tipo'] != 'TE':
            continue
        val = {}
        for segno, stat in re.findall(r'\(([+-]\d)\) (ATT|AR|MOV)', r['testo']):
            val.setdefault(stat, int(segno))
        eq[r['id']] = (SLOT[r['slot']], val.get('ATT', 0), val.get('AR', 0), val.get('MOV', 0))
    return eq


EQUIP = leggi_equip()
COMUNI = [r['id'] for r in leggi('carte_comuni.csv')]
MAZZI_CLASSE = defaultdict(list)
for _r in leggi('carte_classe.csv'):
    MAZZI_CLASSE[_r['mazzo']].append(_r['id'])
IMPREVISTI = [r['nome'] for r in leggi('carte_imprevisto.csv')]
TESSERE = [r['colore'] for r in leggi('tessere_esplorazione.csv')]
SEGNALINI = {r['nome']: int(r['copie']) for r in leggi('segnalini.csv')}
CLASSI = ['Assaltatore', 'Ricercatore', 'Stregone', 'Oracolo']
SPECIE = {'Umano': (1, 0, 1), 'Elfo': (1, 1, 0), 'Sanguar': (0, 0, 2), 'Yumaniano': (1, 1, 0)}  # ATT, AR, MOV
SPECIE_TESSERE = [r['specie'] for r in leggi('tessere_specie.csv')]
SALITE = ['att', 'pv', 'ar', 'pv']
# carte di classe scelte dall'IA (le 5 più utili in scontro) quando il mazzo ne ha più di 5
PREF_CLASSE = {'Assaltatore': ['TI-35', 'TI-30', 'TE-01', 'TI-28', 'TI-29'],
               'Oracolo': ['TE-12', 'TE-04', 'TI-26', 'TI-35', 'TI-30']}

# ---------------------------------------------------------------- dadi e calcolo esatto

P2 = [0.0] * 13
for _a in range(1, 7):
    for _b in range(1, 7):
        P2[_a + _b] += 1 / 36


def p_colpo(bonus, difesa):
    """P(2D6 + bonus >= difesa), senza critici."""
    return sum(P2[s] for s in range(2, 13) if s + bonus >= difesa)


def danno_mostro(m, d, att, ar_bersaglio):
    """Danno del mostro: tabella per LV (kit) oppure D6 + ATT - AR del bersaglio (commento 7 dell'autore), minimo 1."""
    if VARIANTE['danno'] == 'autore':
        return max(1, d + att - ar_bersaglio)
    return max(1, d + m.dmod)


def danno_eroe(d, att, ar_bersaglio):
    """Danno dell'eroe senza bonus delle carte: D6 (kit) oppure D6 + ATT - AR del bersaglio, minimo 1."""
    if VARIANTE['danno'] == 'autore':
        return max(1, d + att - ar_bersaglio)
    return d


def eroe_tipo(classe, livello, equip_att=0, equip_ar=0):
    """Eroe di riferimento: specie +1 ATT +1 AR, salite di livello in ordine SALITE."""
    s = {'pv': 5 + (1 if classe == 'Assaltatore' else 0), 'att': 2, 'ar': 2}
    for k in range(livello - 1):
        s[SALITE[k]] += 2 if SALITE[k] == 'pv' else 1
    s['att'] += equip_att
    s['ar'] += equip_ar
    s['rilanci'] = 2 if classe == 'Stregone' else 0
    s['rinascita'] = 1 if classe == 'Oracolo' else 0
    return s


def scontro_esatto(e, m, passi=600):
    """Distribuzione esatta dello scontro (propagazione in avanti, resto < 1e-12).
    Ritorna p_vince, p_muore, attacchi attesi, p_colpo eroe, p_colpo mostro, danno medio per attacco (eroe, mostro)."""
    if 'primo' in m.fx:
        p_primo = 0.0
    elif m.boss:
        p_primo = 15 / 36
    else:
        p_primo = 21 / 36
    dist = defaultdict(float)
    if p_primo:
        dist[(e['pv'], m.pv, 1, 0, 0, 0, e['rilanci'], e['rinascita'])] += p_primo
    if p_primo < 1:
        dist[(e['pv'], m.pv, 0, 0, 0, 0, e['rilanci'], e['rinascita'])] += 1 - p_primo
    vince = muore = att_attesi = 0.0
    for passo in range(1, passi + 1):
        nuovo = defaultdict(float)
        for (pe, pm, tocca_eroe, primo_fatto, colpo_fatto, ricomposto, ril, rin), p in dist.items():
            if tocca_eroe:
                q = p_colpo(e['att'] - (1 if 'gelo' in m.fx else 0), 8 + m.ar)
                if not primo_fatto and 'svantaggio_primo' in m.fx:
                    q = q * q
                esiti, manca = [], 1.0
                for k in range(ril + 1):
                    esiti.append((manca * q, ril - k))
                    manca *= 1 - q
                for pc, ril2 in esiti:
                    for d in range(1, 7):
                        dan = danno_eroe(d, e['att'] - (1 if 'gelo' in m.fx else 0), m.ar)
                        if 'coriaceo' in m.fx:
                            dan = max(1, dan - 1)
                        pm2, ric2 = pm - dan, ricomposto
                        if pm2 <= 0 and 'ricompone' in m.fx and not ricomposto:
                            pm2, ric2 = 2, 1
                        pp = p * pc / 6
                        if pm2 <= 0:
                            vince += pp
                            att_attesi += pp * passo
                        else:
                            nuovo[(pe, pm2, 0, 1, colpo_fatto, ric2, ril2, rin)] += pp
                if manca > 0:
                    nuovo[(pe, pm, 0, 1, colpo_fatto, ricomposto, 0, rin)] += p * manca
            else:
                am = m.att
                if 'furia' in m.fx and 2 * pm <= m.pv:
                    am += 2
                if 'codardo' in m.fx and 2 * pm <= m.pv:
                    am -= 2
                q = p_colpo(am, 8 + e['ar'] - (1 if 'acido' in m.fx else 0))
                for d in range(1, 7):
                    dan = danno_mostro(m, d, am, e['ar'] - (1 if 'acido' in m.fx else 0)) + (2 if 'carica' in m.fx and not colpo_fatto else 0)
                    pe2, rin2 = pe - dan, rin
                    pm2 = min(m.pv, pm + 1) if 'succhia' in m.fx else pm
                    if pe2 <= 0 and rin:
                        pe2, rin2 = 3, 0
                    pp = p * q / 6
                    if pe2 <= 0:
                        muore += pp
                        att_attesi += pp * passo
                    else:
                        nuovo[(pe2, pm2, 1, primo_fatto, 1, ricomposto, ril, rin2)] += pp
                nuovo[(pe, pm, 1, primo_fatto, colpo_fatto, ricomposto, ril, rin)] += p * (1 - q)
        dist = nuovo
        if sum(dist.values()) < 1e-12:
            break
    pe_h = p_colpo(e['att'] - (1 if 'gelo' in m.fx else 0), 8 + m.ar)
    pe_m = p_colpo(m.att, 8 + e['ar'] - (1 if 'acido' in m.fx else 0))
    d_eroe = sum(max(1, x - 1) if 'coriaceo' in m.fx else x
                 for x in (danno_eroe(d, e['att'] - (1 if 'gelo' in m.fx else 0), m.ar) for d in range(1, 7))) / 6
    d_mostro = sum(danno_mostro(m, d, m.att, e['ar'] - (1 if 'acido' in m.fx else 0)) for d in range(1, 7)) / 6
    return vince, muore, att_attesi, pe_h, pe_m, d_eroe, d_mostro


def rapporto_esatto():
    righe = ["CALCOLO ESATTO DEGLI SCONTRI (eroe di riferimento: specie +1 ATT +1 AR, nessun equipaggiamento;",
             "salite: L2 +1 ATT, L3 +2 PV, L4 +1 AR, L5 +2 PV; Stregone 2 rilanci dei tiri per colpire mancati;",
             "Oracolo 1 rinascita a 3 PV; Assaltatore +1 PV; senza carte e senza Forte Volontà).",
             "Colonne: P(colpo) eroe->mostro, mostro->eroe al primo tiro; danno atteso per round",
             "(P(colpo) x danno medio); round attesi; P(vittoria eroe). Fascia: mazzetto 1 = L1-2, mazzetto 2 = L3-4, boss = L5.", ""]
    for classe in CLASSI:
        righe.append(f"== {classe} ==")
        hdr = f"{'mostro':<24}{'mz':>3}{'PV':>4}{'ATT':>4}{'DIF':>4} |" + ''.join(f"   L{l}: colpo e/m  dan e/m  round  P(vince)" for l in (1, 3, 5))
        righe.append(hdr)
        for m in MOSTRI:
            cel = []
            for l in (1, 3, 5):
                e = eroe_tipo(classe, l)
                v, mu, at, pe, pm_, de, dm = scontro_esatto(e, m)
                cel.append(f"   {pe:5.0%} {pm_:4.0%}  {pe*de:4.1f} {pm_*dm:4.1f}  {at/2:5.1f}   {v:6.1%}")
            righe.append(f"{m.nome:<24}{m.mazzetto:>3}{m.pv:>4}{m.att:>4}{8+m.ar:>4} |" + ''.join(cel))
        righe.append("")
    # matrice compatta P(vittoria) per livello e segnalazioni di fascia
    righe.append("P(vittoria eroe) per livello 1..5 (stesso eroe di riferimento):")
    righe.append(f"{'mostro':<24}{'mz':>3} | " + ' | '.join(f"{c[:11]:>11} L1  L2  L3  L4  L5" for c in CLASSI))
    segnala = []
    for m in MOSTRI:
        parti = []
        for classe in CLASSI:
            ps = [scontro_esatto(eroe_tipo(classe, l), m)[0] for l in range(1, 6)]
            parti.append(' ' * 12 + ' '.join(f"{p*100:3.0f}" for p in ps))
            fascia = {1: (1, 2), 2: (3, 4), 3: (5,)}[m.mazzetto]
            for l in fascia:
                p = ps[l - 1]
                if p < 0.35:
                    segnala.append((m.nome, classe, l, p, 'troppo forte'))
                elif p > 0.95:
                    segnala.append((m.nome, classe, l, p, 'banale'))
        righe.append(f"{m.nome:<24}{m.mazzetto:>3} | " + ' | '.join(parti))
    righe.append("")
    righe.append("Segnalazioni di fascia (P(vittoria) < 35 % = troppo forte, > 95 % = banale, ai livelli che pescano quel mazzetto):")
    for nome, classe, l, p, tipo in segnala:
        righe.append(f"  {nome:<22} {classe:<12} L{l}: {p:6.1%}  {tipo}")
    righe.append("")
    righe.append("Il boss custode si affronta con 3 Indizi, quindi di solito a livello 2-3 (vedi Monte Carlo):")
    righe.append(f"{'boss':<20}{'classe':<13}" + ''.join(f"{'L'+str(l)+' nudo':>10}{'L'+str(l)+' +1/+1':>10}" for l in (2, 3, 4, 5)))
    for m in [x for x in MOSTRI if x.boss]:
        for classe in CLASSI:
            cel = ''
            for l in (2, 3, 4, 5):
                cel += f"{scontro_esatto(eroe_tipo(classe, l), m)[0]:>10.1%}{scontro_esatto(eroe_tipo(classe, l, 1, 1), m)[0]:>10.1%}"
            righe.append(f"{m.nome:<20}{classe:<13}{cel}")
    righe.append("(+1/+1 = con un'arma +1 ATT e uno scudo o armatura +1 AR)")
    return '\n'.join(righe)

# ---------------------------------------------------------------- plancia


def _vicini(c, r):
    d = [(-1, 0), (1, 0), (-1, -1), (0, -1), (-1, 1), (0, 1)] if r % 2 == 0 else [(-1, 0), (1, 0), (0, -1), (1, -1), (0, 1), (1, 1)]
    return [(c + dc, r + dr) for dc, dr in d if 0 <= c + dc < 10 and 0 <= r + dr < 10]


CELLE = [(c, r) for r in range(10) for c in range(10)]
IDX = {x: i for i, x in enumerate(CELLE)}
VICINI = [[IDX[n] for n in _vicini(*x)] for x in CELLE]
DIST = []
for _i in range(100):
    _d = [-1] * 100
    _d[_i] = 0
    _coda = [_i]
    for _x in _coda:
        for _n in VICINI[_x]:
            if _d[_n] < 0:
                _d[_n] = _d[_x] + 1
                _coda.append(_n)
    DIST.append(_d)


def _entrambe(lista):
    return [q for (c, r) in lista for q in ((c, r), (9 - c, 9 - r))]


PARTENZE = [IDX[p] for p in [(2, 0), (7, 0), (9, 4), (7, 9), (2, 9), (0, 5)]]
CRIPTE = [IDX[p] for p in [(3, 3), (6, 3), (3, 6), (6, 6)]]
CASELLE_Q = frozenset(IDX[p] for p in _entrambe([(6, 0), (8, 0), (1, 1), (3, 1), (6, 1), (2, 2), (5, 2), (8, 2), (9, 1), (4, 3),
                                                (7, 3), (8, 3), (0, 3), (2, 4), (5, 4), (1, 4), (4, 1), (8, 1)]))
assert len(CASELLE_Q) == 36 and not CASELLE_Q & set(PARTENZE + CRIPTE)
ADIAC = [set(v) for v in VICINI]

# ---------------------------------------------------------------- Monte Carlo


class Eroe:
    def __init__(self, g, classe, specie):
        self.g, self.classe, self.specie = g, classe, specie
        a, r, mv = SPECIE[specie]
        self.base = {'att': 1 + a, 'ar': 1 + r, 'mov': 1 + mv + (2 if classe == 'Ricercatore' else 0)}
        self.pvmax = 5 + (1 if classe == 'Assaltatore' else 0)
        self.pv = self.pvmax
        self.pe = 0
        self.livello = 1
        self.indizi = 0
        self.fv = False
        self.clessidre = 0
        self.slot = {}
        self.mano = []
        self.scarti = []
        self.rinascita = classe == 'Oracolo'
        self.mappa_sussurrata = False
        self.trappola_parata = False
        self.pos = None
        self.morti = 0
        self.budget = 2
        self.scontro_turno = False

    def stat(self, k):
        return self.base[k] + sum(EQUIP[c][{'att': 1, 'ar': 2, 'mov': 3}[k]] for c in self.slot.values())

    def ha(self, carta):
        return carta in self.slot.values()

    def gioca(self, carta):
        self.mano.remove(carta)
        self.scarti.append(carta)
        self.budget -= 1
        self.g.n_carte += 1

    def guadagna_pe(self, n=1):
        for _ in range(n):
            if self.livello >= 5:
                return
            self.pe += 1
            if self.pe % 2 == 0:
                self.sali()

    def sali(self):
        k = SALITE[self.livello - 1]
        self.livello += 1
        if k == 'pv':
            self.pvmax += 2
            self.pv += 2
        else:
            self.base[k] += 1

    def prossimo_livello(self):
        if self.livello < 5:
            self.pe = 2 * self.livello
            self.sali()


def valore_equip(c, eroe):
    _, a, r, mv = EQUIP[c]
    return 1.2 * a + r + 0.3 * mv + (0.5 if c in ('TE-01', 'TE-12', 'TE-11') else 0)


class Partita:
    def __init__(self, n, rng):
        self.rng = rng
        self.n_carte = 0
        classi = rng.sample(CLASSI, n)
        specie = rng.sample(SPECIE_TESSERE, n)
        self.eroi = [Eroe(self, c, s) for c, s in zip(classi, specie)]
        self.sacchetto = TESSERE[:]
        rng.shuffle(self.sacchetto)
        self.imprevisti = IMPREVISTI[:]
        rng.shuffle(self.imprevisti)
        boss = [m for m in MOSTRI if m.boss]
        self.custode = rng.choice(boss)
        self.boss_pv = self.custode.pv
        self.mazzi = {1: [m for m in MOSTRI if m.mazzetto == 1], 2: [m for m in MOSTRI if m.mazzetto == 2],
                      3: [m for m in boss if m is not self.custode]}
        for v in self.mazzi.values():
            rng.shuffle(v)
        self.mimi = None
        self.primo_tesoro = None
        self.scoperte = set()
        self.vincitore = None
        self.stat = Counter()
        comuni = COMUNI[:]
        rng.shuffle(comuni)
        for e in self.eroi:
            mazzo = MAZZI_CLASSE[e.classe]
            classe = PREF_CLASSE.get(e.classe, mazzo)[:5]
            e.mano = [] if VARIANTE['senza_carte'] else list(classe) + [comuni.pop() for _ in range(10 - len(classe))]
            self.equipaggia(e, iniziale=True)
            e.pos = self.ripartenza(e)
        self.primo = rng.randrange(n)
        self.max_indizi = 0
        self.max_clessidre = 0

    def d6(self):
        return self.rng.randint(1, 6)

    def ripartenza(self, e):
        occ = [x.pos for x in self.eroi if x is not e and x.pos is not None]
        for _ in range(50):
            p = PARTENZE[self.d6() - 1]
            if p not in occ and not any(o in ADIAC[p] for o in occ):
                return p
        return min(PARTENZE, key=lambda p: (p in occ, -min([DIST[p][o] for o in occ] or [9])))

    def equipaggia(self, e, iniziale=False):
        best = None
        for c in e.mano:
            if c in EQUIP:
                sl = EQUIP[c][0]
                gain = valore_equip(c, e) - (valore_equip(e.slot[sl], e) if sl in e.slot else 0)
                if gain > 0.1 and (best is None or gain > best[0]):
                    best = (gain, c)
        if best:
            c = best[1]
            sl = EQUIP[c][0]
            if sl in e.slot:
                e.scarti.append(e.slot[sl])
            e.mano.remove(c)
            e.slot[sl] = c
            if not iniziale:
                e.budget -= 1
                self.n_carte += 1

    # ---------------- scontri

    def tiro_colpire(self, e, bonus, difesa, svantaggio, ril):
        """Tiro per colpire dell'eroe con rilanci (Stregone, Bastone, Forte Volontà, carte)."""
        r = self.rng
        def tira():
            a, b = r.randint(1, 6), r.randint(1, 6)
            if svantaggio:
                c, d = r.randint(1, 6), r.randint(1, 6)
                if c + d < a + b:
                    a, b = c, d
            return a, b
        a, b = tira()
        while a + b + bonus < difesa and ril[0] > 0:
            ril[0] -= 1
            a, b = tira()
        if a + b + bonus < difesa and e.fv and max(a, b) + 6 + bonus >= difesa:
            e.fv = False
            if a < b:
                a = r.randint(1, 6)
            else:
                b = r.randint(1, 6)
        if a + b + bonus < difesa:
            for c in ('TI-38', 'TI-33'):
                if c in e.mano and e.budget > 0 and self.in_boss:
                    e.gioca(c)
                    a, b = tira()
                    break
        return a + b + bonus >= difesa

    def danno_incanto(self, e, m, pm):
        """Gioca il miglior incanto di danno; ritorna i danni."""
        for c, dado, mod in (('TI-35', 6, 0), ('TI-09', 6, 0), ('TI-02', 6, 0), ('TI-16', 6, -1),
                             ('TI-11', 6, -1), ('TI-10', 6, -1)):
            if c in e.mano and e.budget > 0:
                e.gioca(c)
                d = self.d6()
                dan = max(1, d + mod)
                if c == 'TI-35' and 'nonmorto' in m.fx:
                    dan += 2
                if c == 'TI-09' and pm < m.pv:
                    dan += 1
                if c == 'TI-11':
                    while d == 6:
                        d = self.d6()
                        dan += max(1, d - 1)
                if c == 'TI-16':
                    self._fiamma = True
                if c == 'TI-10':
                    self._gelido = True
                return dan
        return 0

    def scontro(self, e, m, pm_iniziale=None):
        """Ritorna (vinto, pv rimasti del mostro)."""
        self.stat['scontri'] += 1
        self.stat[f'scontri_mazzetto_{m.mazzetto}'] += 1
        self.in_boss = m.boss
        self._fiamma = self._gelido = False
        pm = m.pv if pm_iniziale is None else pm_iniziale
        attacchi = 0
        ar_meno = 0
        if e.classe == 'Assaltatore' and e.fv:
            e.fv = False
            ar_meno = 1
        ar_extra = 2 if (e.ha('TE-19') and m.lv >= 3) else 0
        att_extra = 0
        ratto = confusione = False
        dbonus_prossimo = 0
        pericolo = lambda: e.pv <= 3 or m.mazzetto >= 2
        if m.boss:
            for c, v in (('TI-03', 2), ('TI-34', 2), ('TI-27', 1)):
                if c in e.mano and e.budget > 0 and (c != 'TI-34' or 'DX' in e.slot):
                    e.gioca(c)
                    ar_extra += v
                    break
            if 'TI-24' in e.mano and e.budget > 0:
                e.gioca('TI-24')
                ratto = True
        ril = [(2 if e.classe == 'Stregone' else 0) + (1 if e.ha('TE-11') else 0)]
        if 'primo' in m.fx:
            eroe_primo = False
        else:
            a, b = self.d6(), self.d6()
            eroe_primo = a > b or (a == b and not m.boss)
        if 'TI-40' in e.mano and e.budget > 0 and (m.boss or pericolo()):
            e.gioca('TI-40')
            dan = max(1, self.d6() - 1)
            pm -= max(1, dan - 1) if 'coriaceo' in m.fx else dan
        tocca_eroe = eroe_primo
        primo_att = True
        primo_colpo_m = True
        ricomposto = False
        colpito = False
        while True:
            if pm <= 0:
                if 'ricompone' in m.fx and not ricomposto:
                    ricomposto, pm = True, 2
                else:
                    break
            if tocca_eroe:
                if self._fiamma and not primo_att:
                    pm -= 1
                    if pm <= 0:
                        continue
                if pm == 1 and 'TI-04' in e.mano and e.budget > 0:
                    e.gioca('TI-04')
                    pm = 0
                    continue
                if m.boss or pericolo():
                    dan = self.danno_incanto(e, m, pm)
                    if dan:
                        pm -= max(1, dan - 1) if 'coriaceo' in m.fx else dan
                        if pm <= 0:
                            continue
                bonus = e.stat('att') + att_extra - (1 if 'gelo' in m.fx else 0)
                if e.ha('TE-15') and eroe_primo:
                    bonus += 1
                att_val = bonus  # ATT vero, senza i +colpire delle carte (conta per il danno dell'autore)
                if m.boss:
                    for c, v in (('TI-22', 3), ('TI-29', 2)):
                        if c in e.mano and e.budget > 0 and p_colpo(bonus, 8 + m.ar - ar_meno) < 0.6:
                            e.gioca(c)
                            bonus += v
                            break
                    for c, v in (('TI-28', 2),):
                        if c in e.mano and e.budget > 0:
                            e.gioca(c)
                            dbonus_prossimo += v
                if 'TI-37' in e.mano and e.budget > 0 and eroe_primo and primo_att and (m.boss or pericolo()):
                    e.gioca('TI-37')
                    dbonus_prossimo += 2
                colpo = self.tiro_colpire(e, bonus, 8 + m.ar - ar_meno, primo_att and 'svantaggio_primo' in m.fx, ril)
                attacchi += 1
                if colpo:
                    dan = danno_eroe(self.d6(), att_val, m.ar - ar_meno) + dbonus_prossimo + (1 if e.ha('TE-12') and 'nonmorto' in m.fx else 0)
                    dbonus_prossimo = 0
                    pm -= max(1, dan - 1) if 'coriaceo' in m.fx else dan
                primo_att = False
                tocca_eroe = False
            else:
                am = 1 if ratto else m.att
                if 'furia' in m.fx and 2 * pm <= m.pv:
                    am += 2
                if 'codardo' in m.fx and 2 * pm <= m.pv:
                    am -= 2
                if self._gelido:
                    am -= 1
                if m.boss and not confusione and 'TI-12' in e.mano and e.budget > 0:
                    e.gioca('TI-12')
                    confusione = True
                    s = min(self.d6() + self.d6(), self.d6() + self.d6())
                else:
                    s = self.d6() + self.d6()
                attacchi += 1
                if s + am >= 8 + e.stat('ar') + ar_extra - (1 if 'acido' in m.fx else 0):
                    d = self.d6()
                    dan = danno_mostro(m, d, am, e.stat('ar') + ar_extra - (1 if 'acido' in m.fx else 0)) + (2 if 'carica' in m.fx and primo_colpo_m else 0)
                    if primo_colpo_m and 'borseggio' in m.fx and e.mano:
                        e.scarti.append(e.mano.pop(self.rng.randrange(len(e.mano))))
                    primo_colpo_m = False
                    colpito = True
                    if dan >= e.pv:
                        for c in ('TI-30', 'TI-36'):
                            if c in e.mano and e.budget > 0:
                                e.gioca(c)
                                dan = 0 if c == 'TI-30' else max(0, dan - 2)
                                break
                    if dan >= e.pv and e.ha('TE-08') and not getattr(e, 'targa_usata', False):
                        e.targa_usata = True
                        dan = 0
                    if dan > 0 and 'succhia' in m.fx:
                        pm = min(m.pv, pm + 1)
                    e.pv -= dan
                    if dan > 0 and d == 6 and 'pietrifica' in m.fx:
                        self.clessidra(e)
                    if dan > 0 and d == 6 and 'custode' in m.fx:
                        self.perdita(e)
                    if e.pv <= 0 and e.rinascita:
                        e.rinascita = False
                        e.pv = 3
                        self.stat['rinascite'] += 1
                    if e.pv <= 0:
                        self.stat['attacchi'] += attacchi
                        return False, pm
                tocca_eroe = True
        self.stat['attacchi'] += attacchi
        if 'morso' in m.fx and colpito:
            e.pv = max(1, e.pv - 1)
        return True, 0

    def clessidra(self, e):
        if e.clessidre < 3:
            e.clessidre += 1
        self.max_clessidre = max(self.max_clessidre, sum(x.clessidre for x in self.eroi))

    def perdita(self, e):
        d = self.d6()
        perse = []
        if d == 1:
            perse = list(e.slot)
        elif d in (2, 3, 4, 5):
            sl = {2: 'Elmo', 3: 'DX', 4: 'SX', 5: 'Armatura'}[d]
            if sl == 'DX' and e.ha('TE-09'):
                return self.perdita(e)
            if sl in e.slot:
                perse = [sl]
        for sl in perse:
            e.scarti.append(e.slot.pop(sl))

    def sconfitta(self, e):
        e.morti += 1
        self.stat['sconfitte'] += 1
        e.pv = e.pvmax
        e.pos = None
        e.pos = self.ripartenza(e)
        self.perdita(e)

    def prendi_indizio(self, e, n=1):
        e.indizi += n
        if e.indizi >= 3 and self.mimi is None:
            d = self.d6()
            while d > 4:
                d = self.d6()
            self.mimi = CRIPTE[d - 1]
            self.stat['round_tesoro'] = self.round
            self.primo_tesoro = e
            for x in self.eroi:
                if x is not e:
                    x.indizi += 1
        self.max_indizi = max(self.max_indizi, sum(x.indizi for x in self.eroi))

    def vittoria_mostro(self, e, m):
        if m.mazzetto == 3:
            self.prendi_indizio(e)
            e.prossimo_livello()
            e.fv = True
        else:
            n = 1 + (1 if e.mappa_sussurrata else 0)
            e.mappa_sussurrata = False
            self.prendi_indizio(e, n)
            e.guadagna_pe()
            if m.mazzetto == 2:
                e.fv = True
        if e.classe == 'Assaltatore':
            e.fv = True

    def mostro_su_casella(self, e, cella):
        mz = 1 if e.livello <= 2 else (2 if e.livello <= 4 else 3)
        m = self.mazzi[mz].pop(0)
        self.mazzi[mz].append(m)
        e.scontro_turno = True
        vinto, _ = self.scontro(e, m)
        if vinto:
            self.scoperte.discard(cella)
            self.stat['vittorie_mostri'] += 1
            self.vittoria_mostro(e, m)
        else:
            self.scoperte.add(cella)
            if 'catene' in m.fx:
                self.clessidra(e)
            if 'saccheggio' in m.fx and e.mano:
                e.scarti.append(e.mano.pop(self.rng.randrange(len(e.mano))))
            self.sconfitta(e)

    def imprevisto(self, e):
        c = self.imprevisti.pop(0)
        self.imprevisti.append(c)
        self.stat['imprevisto_' + c] += 1
        if c == 'Trappola':
            if e.ha('TE-01') or e.trappola_parata:
                e.trappola_parata = False
                return
            for k in ('TI-39', 'TI-06', 'TI-17'):
                if k in e.mano and e.budget > 0:
                    e.gioca(k)
                    if k != 'TI-17':
                        return
                    self.perdita(e)
                    return
            dan = max(1, self.d6() - 1) - (1 if e.ha('TE-16') else 0)
            e.pv -= max(0, dan)
            self.perdita(e)
            if e.pv <= 0:
                self.stat['morti_trappola'] += 1
                self.sconfitta(e)
        elif c == 'Locanda':
            e.guadagna_pe()
            e.pv = min(e.pvmax, e.pv + 2)
            if e.classe == 'Oracolo':
                e.rinascita = True
        elif c == 'Fonte':
            for _ in range(2):
                buone = [x for x in e.scarti if x not in EQUIP]
                if buone:
                    x = buone[0]
                    e.scarti.remove(x)
                    e.mano.append(x)
            if e.ha('TE-20'):
                e.pv = min(e.pvmax, e.pv + 1)
        elif c == 'Fabbro':
            eq = [x for x in e.scarti if x in EQUIP]
            if eq:
                x = max(eq, key=lambda c: valore_equip(c, e))
                e.scarti.remove(x)
                e.mano.append(x)

    def forza(self, e, x):
        return p_colpo(e.stat('att'), 8 + x.stat('ar')) * 3.5 / max(1, x.pv)

    def duello(self, e, t):
        if t.indizi and t.mano and self.forza(t, e) < self.forza(e, t):
            e.mano.append(t.mano.pop(self.rng.randrange(len(t.mano))))
            self.stat['duelli_rifiutati'] += 1
            return
        self.stat['duelli'] += 1
        a, b = self.d6(), self.d6()
        primo = e if (a > b or (a == b and e.stat('mov') >= t.stat('mov'))) else t
        if a == b and t.stat('mov') > e.stat('mov'):
            primo = t
        att, dif = primo, (t if primo is e else e)
        ril = {id(e): [2 if e.classe == 'Stregone' else 0], id(t): [2 if t.classe == 'Stregone' else 0]}
        self.in_boss = False
        while True:
            if self.tiro_colpire(att, att.stat('att'), 8 + dif.stat('ar'), False, ril[id(att)]):
                dif.pv -= danno_eroe(self.d6(), att.stat('att'), dif.stat('ar'))
                if dif.pv <= 0 and dif.rinascita:
                    dif.rinascita = False
                    dif.pv = 3
                if dif.pv <= 0:
                    break
            att, dif = dif, att
        vinc, perd = att, dif
        if perd.indizi:
            perd.indizi -= 1
            self.prendi_indizio(vinc)
        vinc.guadagna_pe()
        vinc.fv = True
        self.sconfitta(perd)

    def scegli_meta(self, e, r):
        occ = {x.pos for x in self.eroi if x is not e}
        vicino_altri = lambda c: any(o in ADIAC[c] for o in occ)
        cand = [c for c in range(100) if 1 <= DIST[e.pos][c] <= r and c not in occ]
        if e.indizi >= 3 and self.mimi is not None:
            if self.mimi in cand:
                return self.mimi
            return min(cand, key=lambda c: (DIST[c][self.mimi], c in CASELLE_Q, vicino_altri(c)))
        utili = [c for c in CASELLE_Q if (self.sacchetto or c in self.scoperte) and c not in occ]
        q = [c for c in cand if c in utili]
        if q:
            return min(q, key=lambda c: (vicino_altri(c), self.rng.random()))
        prede = [x for x in self.eroi if x is not e and x.indizi > 0 and self.forza(e, x) >= self.forza(x, e)]
        if not utili and prede:
            mire = [c for c in cand if any(x.pos in ADIAC[c] for x in prede)]
            if mire:
                return mire[0]
            return min(cand, key=lambda c: min(DIST[c][x.pos] for x in prede))
        if utili:
            return min(cand, key=lambda c: (min(DIST[c][t] for t in utili), vicino_altri(c)))
        return min(cand, key=lambda c: (vicino_altri(c), self.rng.random()))

    def turno(self, e):
        self.stat['turni'] += 1
        if e.clessidre:
            e.clessidre -= 1
            self.stat['turni_saltati'] += 1
            return
        e.budget = 2
        e.scontro_turno = False
        self.equipaggia(e)
        if 'TI-15' in e.mano and e.budget > 1 and e.indizi < 3 and self.sacchetto:
            e.gioca('TI-15')
            e.mappa_sussurrata = True
        r = max(1, self.d6() + e.stat('mov'))
        e.pos = self.scegli_meta(e, r)
        if e.pos == self.mimi and e.indizi >= 3:
            self.stat['tentativi_boss'] += 1
            for k, v in (('att', e.stat('att')), ('ar', e.stat('ar')), ('liv', e.livello), ('equip', len(e.slot)), ('pv', e.pv)):
                self.stat['boss_' + k] += v
            e.scontro_turno = True
            vinto, pm = self.scontro(e, self.custode, self.boss_pv)
            if vinto:
                self.vincitore = e
                return
            self.boss_pv = pm
            self.sconfitta(e)
        elif e.pos in CASELLE_Q:
            if e.pos in self.scoperte:
                self.mostro_su_casella(e, e.pos)
            elif self.sacchetto:
                self.stat['tessere_pescate'] += 1
                if self.sacchetto.pop() == 'rossa':
                    self.mostro_su_casella(e, e.pos)
                else:
                    self.imprevisto(e)
        if not e.scontro_turno and e.pos is not None:
            vicini = [x for x in self.eroi if x is not e and x.pos in ADIAC[e.pos]]
            if vicini:
                self.duello(e, vicini[0])
        # fine turno: cure e carte utili
        if e.pv <= e.pvmax - 3 or (e.pv <= 2):
            for c, mod in (('TI-26', 0), ('TI-25', -1), ('TI-32', None)):
                if c in e.mano and e.budget > 0:
                    e.gioca(c)
                    e.pv = min(e.pvmax, e.pv + (1 if mod is None else max(1, self.d6() + mod)) + (1 if e.ha('TE-14') else 0))
                    break
        if not e.fv and 'TI-08' in e.mano and e.budget > 0:
            e.gioca('TI-08')
            e.fv = True
        if 'TI-07' in e.mano and e.budget > 0:
            buone = [x for x in e.scarti if x in ('TI-35', 'TI-02', 'TI-09', 'TI-30', 'TI-26')]
            if buone:
                e.gioca('TI-07')
                e.scarti.remove(buone[0])
                e.mano.append(buone[0])

    def gioca(self, max_round=120):
        n = len(self.eroi)
        self.round = 0
        for self.round in range(1, max_round + 1):
            for k in range(n):
                e = self.eroi[(self.primo + k) % n]
                self.turno(e)
                if self.vincitore:
                    return self.vincitore
        return None


def una_partita(arg):
    n, seme, variante = arg
    VARIANTE.update(variante)  # i processi figli (forkserver) non ereditano il globale
    rng = random.Random(seme)
    g = Partita(n, rng)
    v = g.gioca()
    s = g.stat
    minuti = (25 * s['turni'] + 15 * s['tessere_pescate'] + 30 * s['scontri'] + 12 * s['attacchi'] + 10 * g.n_carte
              + 40 * s['sconfitte'] + 30 * s['duelli']) / 60
    return {
        'n': n, 'fine': 'boss' if v else 'stallo', 'round': g.round, 'minuti': minuti,
        'vincitore': v.classe if v else None, 'specie_vinc': v.specie if v else None,
        'classi': [e.classe for e in g.eroi], 'morti': sum(e.morti for e in g.eroi),
        'morti_classe': {e.classe: e.morti for e in g.eroi},
        'liv_vinc': v.livello if v else None, 'liv_medio': sum(e.livello for e in g.eroi) / n,
        'liv_max': max(e.livello for e in g.eroi),
        'max_indizi': g.max_indizi, 'max_clessidre': g.max_clessidre,
        'sacchetto_vuoto': not g.sacchetto, 'tentativi_boss': s['tentativi_boss'],
        'round_tesoro': s.get('round_tesoro'), 'custode': g.custode.nome,
        'scontri': s['scontri'], 'mz1': s['scontri_mazzetto_1'], 'mz2': s['scontri_mazzetto_2'], 'mz3': s['scontri_mazzetto_3'],
        'duelli': s['duelli'], 'rifiuti': s['duelli_rifiutati'], 'turni_saltati': s['turni_saltati'],
        'carte': g.n_carte, 'morti_trappola': s['morti_trappola'],
        'boss_eroe': {k: s['boss_' + k] for k in ('att', 'ar', 'liv', 'equip', 'pv')},
        'vince_chi_trova': v is not None and v is g.primo_tesoro,
    }


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def rapporto_partite(n_partite, seme, processi):
    righe = [f"MONTE CARLO: {n_partite} partite per numero di giocatori, seme {seme}"
             + (", VARIANTE SENZA CARTE (mani vuote: niente equipaggiamenti né incanti)" if VARIANTE['senza_carte'] else "")
             + (", DANNO DELL'AUTORE (D6 + ATT - AR del bersaglio, minimo 1, al posto della tabella)." if VARIANTE['danno'] == 'autore' else "."),
             "", REGOLE, "", APPROSSIMAZIONI, ""]
    sintesi = {}
    with Pool(processi) as pool:
        for n in (2, 3, 4):
            ris = pool.map(una_partita, [(n, seme * 1000003 + n * 100000 + i, dict(VARIANTE))
                                         for i in range(n_partite)], chunksize=200)
            fin = [r for r in ris if r['fine'] == 'boss']
            rr = [r['round'] for r in fin]
            mm = [r['minuti'] for r in fin]
            righe.append(f"=== {n} giocatori ===")
            righe.append(f"Finite col boss: {len(fin)/len(ris):.1%}; in stallo a 120 round: {1-len(fin)/len(ris):.1%} "
                         "(nel regolamento non c'è fine per Clessidre o per tempo).")
            if fin:
                righe.append(f"Round (giro di tavolo) delle partite finite: media {statistics.mean(rr):.1f}, mediana {statistics.median(rr)}, "
                             f"10°-90° percentile {pct(rr, .1)}-{pct(rr, .9)}")
                righe.append(f"Minuti stimati: media {statistics.mean(mm):.0f}, mediana {statistics.median(mm):.0f}, "
                             f"10°-90° percentile {pct(mm, .1):.0f}-{pct(mm, .9):.0f} (scatola: 25-30 minuti)")
                rt = [r['round_tesoro'] for r in fin if r['round_tesoro']]
                righe.append(f"Round in cui qualcuno trova il tesoro (3° Indizio): media {statistics.mean(rt):.1f}; "
                             f"da lì alla vittoria: media {statistics.mean(r['round'] - r['round_tesoro'] for r in fin if r['round_tesoro']):.1f} round")
                righe.append(f"Tentativi sul boss per partita: media {statistics.mean(r['tentativi_boss'] for r in fin):.1f}, "
                             f"90° percentile {pct([r['tentativi_boss'] for r in fin], .9)}; "
                             f"vittorie per tentativo {len(fin)/sum(r['tentativi_boss'] for r in ris):.1%}")
                tb = sum(r['tentativi_boss'] for r in ris)
                righe.append("Eroe medio quando sfida il boss: " + ', '.join(
                    f"{k.upper()} {sum(r['boss_eroe'][k] for r in ris)/tb:.2f}" for k in ('liv', 'pv', 'att', 'ar', 'equip'))
                    + " (EQUIP = oggetti equipaggiati)")
            vit = Counter(r['vincitore'] for r in fin)
            pres = Counter(c for r in ris for c in r['classi'])
            righe.append("Vittorie per classe (sulle partite in cui la classe gioca): " + ', '.join(
                f"{c} {vit[c]/pres[c]:.1%}" for c in CLASSI) + f" (equo: {1/n:.1%})")
            vs = Counter(r['specie_vinc'] for r in fin)
            righe.append("Specie dei vincitori: " + ', '.join(f"{k} {v/len(fin):.1%}" for k, v in vs.most_common()))
            righe.append(f"Vince chi trova per primo il tesoro (3° Indizio): {sum(r['vince_chi_trova'] for r in fin)/len(fin):.1%}")
            vc = Counter(r['custode'] for r in fin)
            cc = Counter(r['custode'] for r in ris)
            righe.append("Stallo per boss custode: " + ', '.join(f"{k} {1 - vc[k]/cc[k]:.1%}" for k in sorted(cc)))
            righe.append(f"Sconfitte (morti) per partita: media {statistics.mean(r['morti'] for r in ris):.2f}; per classe: " + ', '.join(
                f"{c} {sum(r['morti_classe'].get(c, 0) for r in ris)/pres[c]:.2f}" for c in CLASSI))
            righe.append(f"Livello del vincitore: " + ', '.join(f"L{k} {v/len(fin):.1%}" for k, v in sorted(Counter(r['liv_vinc'] for r in fin).items()))
                         + f"; livello medio a fine partita {statistics.mean(r['liv_medio'] for r in ris):.2f}; "
                         f"partite con almeno un eroe a L5: {sum(r['liv_max'] == 5 for r in ris)/len(ris):.1%}")
            tot = sum(r['scontri'] for r in ris)
            righe.append(f"Scontri per partita {tot/len(ris):.1f}: mazzetto 1 {sum(r['mz1'] for r in ris)/tot:.1%}, "
                         f"mazzetto 2 {sum(r['mz2'] for r in ris)/tot:.1%}, boss (mazzetto 3 e custode) {sum(r['mz3'] for r in ris)/tot:.1%}")
            righe.append(f"Duelli per partita {statistics.mean(r['duelli'] for r in ris):.2f}, rifiutati {statistics.mean(r['rifiuti'] for r in ris):.2f}; "
                         f"turni saltati per Clessidra {statistics.mean(r['turni_saltati'] for r in ris):.2f}; carte giocate {statistics.mean(r['carte'] for r in ris):.1f}")
            righe.append(f"Sacchetto svuotato: {sum(r['sacchetto_vuoto'] for r in ris)/len(ris):.1%} delle partite; "
                         f"sconfitte per Trappola per partita {statistics.mean(r['morti_trappola'] for r in ris):.2f}")
            mi = [r['max_indizi'] for r in ris]
            righe.append(f"Indizi in gioco contemporaneamente: massimo {max(mi)}, 99° percentile {pct(mi, .99)} "
                         f"(segnalini stampati: {SEGNALINI['Indizio']}); partite oltre i segnalini: {sum(x > SEGNALINI['Indizio'] for x in mi)/len(mi):.2%}")
            mc = [r['max_clessidre'] for r in ris]
            righe.append(f"Clessidre in gioco contemporaneamente: massimo {max(mc)} (segnalini stampati: {SEGNALINI['Clessidra']})")
            righe.append("")
            sintesi[n] = {'fin': len(fin) / len(ris), 'round': statistics.mean(rr) if rr else None,
                          'minuti': statistics.mean(mm) if mm else None}
    return '\n'.join(righe), sintesi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--esatto', action='store_true')
    ap.add_argument('--partite', type=int, default=0)
    ap.add_argument('--seme', type=int, default=20261105)
    ap.add_argument('--processi', type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument('--uscita')
    ap.add_argument('--senza-carte', action='store_true', help='mani vuote (sensibilità: quanto contano le carte)')
    ap.add_argument('--danno', choices=('tabella', 'autore'), default='tabella',
                    help="tabella = danni per LV (kit); autore = D6 + ATT - AR del bersaglio (commento 7 alla bozza del 3/11)")
    a = ap.parse_args()
    VARIANTE['senza_carte'] = a.senza_carte
    VARIANTE['danno'] = a.danno
    parti = [f"Collaudo del kit di playtest - dati: {os.path.relpath(DATI, RADICE)}/*.csv", ""]
    # controllo della plancia contro il regolamento («Cripta più vicina a 3 esagoni, la più lontana a 7»)
    dd = [sorted(DIST[p][c] for c in CRIPTE) for p in PARTENZE]
    parti.append("Plancia: distanze partenza -> Cripte (vicina..lontana): " + '; '.join(f"P{i+1} {d}" for i, d in enumerate(dd)))
    parti.append(f"Componenti letti: {len(MOSTRI)} mostri, {len(COMUNI)} comuni, {sum(len(v) for v in MAZZI_CLASSE.values())} di classe, "
                 f"{len(IMPREVISTI)} Imprevisti {dict(Counter(IMPREVISTI))}, tessere {dict(Counter(TESSERE))}, segnalini {SEGNALINI}")
    parti.append("")
    if a.esatto:
        parti.append(rapporto_esatto())
        parti.append("")
    if a.partite:
        testo, sintesi = rapporto_partite(a.partite, a.seme, a.processi)
        parti.append(testo)
    out = '\n'.join(parti) + '\n'
    if a.uscita:
        with open(a.uscita, 'w', encoding='utf-8') as f:
            f.write(out)
    sys.stdout.write(out)


if __name__ == '__main__':
    main()
