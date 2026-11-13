"""Partita v7: preparazione (§3), turno (§4.0), movimento ed esplorazione (§8), Imprevisti, rifornimento delle tessere Esplorazione,
Fine del turno. Le catene stanno in catena.py, gli scontri in scontro.py, le scelte in ia.py."""
import random
from collections import Counter

import carte as K
import mappa as M
import stato as S
import catena as C
import scontro as X
import tiri
import ia

ROUND_MAX = 60


class Opzioni:
    def __init__(self, **kw):
        self.limite, self.mano_max, self.soglia = 2, 10, 6
        self.op1 = self.op2 = self.op5 = False
        self.ar_v6 = self.indizio_lv = self.preset = False
        self.dado_sommato = self.chi_tira_non_risponde = self.penalita_meno = False
        self.mano_ia = False                 # --mano-ia: l'IA sceglie le 5 carte iniziali invece della mano predefinita
        self.__dict__.update(kw)


class Partita:
    def __init__(self, n, seme, opz):
        self.rng = random.Random(seme)
        self.opz = opz
        self.st = Counter()
        self.uso = Counter()                # carte giocate per id
        self.info = Counter()               # effetti non modellati per id
        self.giocate_eroe = Counter()
        self.pl_round = []                  # PL medio degli eroi alla fine di ogni round
        self.mano_fine = []                 # carte in mano alla propria Fine
        self.pv_fine = []                   # PV alla propria Fine
        self.max_indizi = 0
        self.profezie = {}
        self.origine = {}                   # TI-28: carta presa dalla pila di classe di un avversario -> quell'avversario
        self.ristoro = {}                   # D32: eroe -> cosa ha fatto negli scontri del turno (stato.ristoro_segna)
        self.in_catena = self.in_risposte = False
        self.scontro = None
        self.in_cima = False                # NE-44: la carta Mostro torna in cima al mazzetto
        self.turno_finito = self.finita = False
        self.vincitore = None
        self.round, self.attivo = 1, 0
        self.round_tesoro = None
        self.creature_svant = False
        self.mappa = self.mappa_di = None
        self.cambi = None                   # R 8.12: Mappa che ha cambiato 3 fiori (None = disposizione di montaggio)
        self.cripta_xy = None               # il punto tirato con 2D6 + 2D6 per la Cripta
        self.mappa_mov_avv = False
        self.mimi, self.tesoro_trovato = None, False
        r = self.rng
        # D24: draft (o preset «Strettoie») dei 14 fiori sulla base; la mappa in uso è `plancia`
        self.montaggio = M.disposizione_preset(M.BASE) if opz.preset else M.draft(n, r)
        self.plancia = M.Plancia(M.terreno(self.montaggio))
        classi = r.sample(K.CLASSI, n)
        specie = r.sample(K.SPECIE, n)
        self.eroi = [S.Eroe(i, classi[i], specie[i], r.choice('AB')) for i in range(n)]
        self.mazzo = K.COMUNI[:]
        r.shuffle(self.mazzo)
        boss = K.MAZZETTI[3][:]                  # D31: i 6 boss sono tutti il mazzetto 3; il custode si pesca quando compare la Cripta
        r.shuffle(boss)
        self.custode = None
        self.mazzetti = {1: K.MAZZETTI[1][:], 2: K.MAZZETTI[2][:], 3: boss}
        for t in (1, 2):
            r.shuffle(self.mazzetti[t])
        self.imprevisti = K.IMPREVISTI[:]
        r.shuffle(self.imprevisti)
        tessere = K.TESSERE[:]
        r.shuffle(tessere)
        # D29: 24 tessere coperte posate a turno su esagoni percorribili a >= 2 esagoni dalle Partenze, una per esagono
        # (qui: a caso); le altre 12 in riserva
        posti = r.sample(self.plancia.idonee_tessera(()), M.N_TESSERE)
        self.tessere = {q: tessere.pop() for q in posti}         # esagono -> 'rossa'/'blu' coperta, 'scoperta'
        self.riserva, self.usate = tessere, []
        self.scatola = {c: K.CARTE_CLASSE[c][:] for c in K.CLASSI if c not in classi}
        for e in self.eroi:
            # 13/11: mano = 5 carte di classe (predefinita o scelta dall'IA); le altre 15, mescolate, sono la pila di classe
            e.mano = ia.mano_iniziale(self, e)
            e.pila = [c for c in K.CARTE_CLASSE[e.classe] if c not in e.mano]
            r.shuffle(e.pila)
        for e in self.eroi:                       # R 3.9
            while True:
                h = M.PARTENZE[r.randrange(6)]
                if all(x.pos != h and not self.plancia.accanto(x.pos, h) for x in self.eroi if x.pos):
                    break
            e.pos = e.partenza = h
        self.attivo = r.randrange(n)              # R 3.10
        self.primo = self.attivo

    # --- svolgimento ---------------------------------------------------------------------------------

    def gioca(self):
        while not self.finita and self.round <= ROUND_MAX:
            turno(self, self.eroi[self.attivo])
            if self.finita:
                break
            self.attivo = (self.attivo + 1) % len(self.eroi)
            if self.attivo == self.primo:
                self.pl_round.append(sum(e.pl() for e in self.eroi) / len(self.eroi))
                self.round += 1
        return self.vincitore


def turno(g, e):
    g.turno_finito = False
    e.mosso, e.scontri, e.pos_inizio = False, 0, e.pos
    g.st['turni'] += 1
    # niente pesca a inizio turno (13/11, nemmeno al primo): le carte arrivano dal bottino dei mostri (stato.loot)
    C.momento(g, 'M0')
    C.momento(g, 'M1')
    if not g.turno_finito:
        muovi(g, e)
        C.momento(g, 'M2')
    if not g.turno_finito:
        esplora(g, e)
    if not (g.turno_finito or g.finita) and e.scontri == 0 and g.round > 1:     # primo giro: niente Duelli
        vicini = [x for x in S.avversari(g, e) if g.plancia.accanto(e.pos, x.pos)]
        x = ia.sfida(g, e, vicini)
        if x is not None:
            if ia.rifiuta(g, x, e):
                g.st['duelli_rifiutati'] += 1
                S.ruba(g, e, x)
            else:
                X.duello(g, e, x)
    if not g.finita:
        C.momento(g, 'M6')
        fine(g, e)


def muovi(g, e):
    if 'Fermo' in e.stati:
        passi = 0
    elif 'Rallentato' in e.stati:
        passi = 1
        g.st['turni_rallentato'] += 1
    else:
        t = C.catena_tiro(g, tiri.Tiro(g, e, 'mov', 1, e.stat(g, 'mov')))
        if t.facce[0] <= 2 and e.ha('ritira_mov') and 'TE-30' not in e.usati:
            e.usati.add('TE-30')                    # TE-30: una volta per turno ritira il movimento
            t.ritira()
        passi = max(1, t.valore())
    bloccati = {h for h, t in g.tessere.items() if t == 'scoperta' and not e.tmp['parkour']}     # TI-40
    if g.mimi:
        bloccati.add(g.mimi)
    occupati = {x.pos for x in g.eroi if x is not e}
    mete = g.plancia.raggiungibili(e.pos, passi, bloccati, occupati) if passi else {e.pos: 0}
    dest = ia.destinazione(g, e, mete)
    g.st['mov_tirato'] += passi
    g.st['mov_speso'] += mete[dest]
    e.pos = dest
    e.mosso = True


def esplora(g, e):
    h = e.pos
    if h == g.mimi:
        if e.indizi >= 3:
            g.st['tentativi_custode'] += 1
            X.scontro(g, e, custode=True)
        return
    t = g.tessere.get(h)
    if t == 'blu':
        g.usate.append(g.tessere.pop(h))
        C.momento(g, 'M3')
        if not g.turno_finito:
            imprevisto(g, e)
    elif t in ('rossa', 'scoperta'):
        g.tessere[h] = 'scoperta'
        tier = 1 if e.pl() <= 3 else (2 if e.pl() <= 7 else 3)       # R 6.4
        mz = g.mazzetti[tier]
        mid = mz.pop(0)
        g.in_cima = False
        esito = X.scontro(g, e, mid)
        if g.in_cima:
            mz.insert(0, mid)                        # NE-44 Permaloso: in cima
        else:
            mz.append(mid)                           # in fondo al suo mazzetto
        if esito in ('vinto', 'sparito', 'fuga_mostro') and not g.finita:      # TI-41: la tessera va tra le usate
            if h in g.tessere:                       # (una carta Mappa può averla già rimandata nella riserva)
                del g.tessere[h]
                g.usate.append('rossa')
    if not g.finita:
        C.momento(g, 'M5')


def imprevisto(g, e):
    nome = g.imprevisti.pop(0)
    g.imprevisti.append(nome)
    g.st['imprevisto_' + nome] += 1
    if nome == 'Trappola':
        if 'Occhio' in e.stati:
            del e.stati['Occhio']
            g.st['trappole_evitate'] += 1
            return
        extra = K.CARTE[g.mappa].p.get('trappola', 0) if g.mappa else 0
        t = C.catena_tiro(g, tiri.Tiro(g, e, 'trappola', 1, -1 + extra, basso=True))
        if not t.annulla_danni:
            e.pv -= max(1, t.valore())
        if e.pv <= 0:
            g.st['morti_trappola'] += 1
            S.sconfitta(g, e)                        # R 11.5: un solo tiro di perdita
        else:
            S.perdita(g, e)
    elif nome == 'Locanda':
        S.cura(g, e, 2, carta=False)
        S.riprendi(g, e, 1)
    elif nome == 'Fonte':
        S.riprendi(g, e, 2)
    elif nome == 'Fabbro':
        S.riprendi(g, e, 1, filtro=lambda c: c.equip)


def fine(g, e):
    """§4.0 Fine: (a) è il momento M6 già giocato; poi (b)-(f)."""
    if e.tmp['perdita_fine']:                        # TI-26: «Alla Fine del turno» = punto (a)
        S.perdita(g, e)
    S.ristoro(g, e)                                  # D32: Ristoro di chi ha combattuto, alla Fine del turno
    if e.ha('pigiama') and not e.tmp['incanti']:     # TE-31: nessun Incanto giocato in questo turno
        S.cura(g, e, 1, carta=False)
    for x in g.eroi:                                 # (b) effetti «in questo turno» di tutti, Profezie
        x.tmp.clear()
    g.profezie.clear()
    g.creature_svant = False
    e.stati = {s: False for s, trav in e.stati.items() if trav}   # (c)
    e.usati.clear()                                  # (d)
    for cid in e.zona:
        S.agli_scarti(g, e, cid)                     # (e)
    e.zona = []
    e.giocate = 0
    e.equip_turno = False
    g.mano_fine.append(len(e.mano))
    g.pv_fine.append(e.pv)
    coperte = sum(1 for t in g.tessere.values() if t in ('rossa', 'blu'))
    if coperte <= g.opz.soglia:                      # (f) D29: chi chiude il turno posa tessere fino a 24 sulla mappa
        g.st['rifornimenti'] += 1
        g.st['tessere_rifornite'] += S.posa_tessere(g, M.N_TESSERE - len(g.tessere), e)
