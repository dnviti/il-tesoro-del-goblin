"""Stato della partita: eroi, mano (D8), scarti, slot e PL, Stati, Indizi e tesoro, danni, sconfitta (D7)."""
from collections import Counter

import carte as K
import mappa as M
import catena
import ia
import tiri

STATI_PIU = {'Occhio', 'Sussurro', 'Riflesso', 'Fede', 'Vantaggio'}
LOOT = 3              # carte rivelate al bottino di un mostro dei mazzetti 1-2 (tiene 1, le altre in fondo al mazzo)


PV_INIZIO = 5          # D30 (rivisto): PV totali di partenza; gli Equipaggiamenti «(+N) PV» li alzano finché equipaggiati


class Eroe:
    def __init__(self, idx, classe, specie, direzione):
        self.idx, self.classe, self.specie, self.direzione = idx, classe, specie, direzione
        self.base = {'att': 1, 'mov': 1, 'ar': 9}
        for k, v in K.BONUS_SPECIE[specie].items():
            self.base[k] += v
        self.slot = {}                      # nome slot -> id carta
        self.mano, self.pila, self.scarti, self.zona = [], [], [], []     # pila = pila di classe (le 15 carte non scelte)
        self.danni = 0                      # Danni subiti: sconfitto quando danni >= PV totali; dopo la sconfitta 0
        self.fv = False
        self.indizi = 0
        self.pos = self.partenza = self.pos_inizio = None
        self.stati = {}                     # nome -> True se orizzontale (di traverso, R 9.1), False se verticale (dritto)
        self.potere = True                  # Carta Classe: una volta per partita
        self.giocate = 0                    # carte giocate dalla propria ultima Fine (D9)
        self.equip_turno = False
        self.usati = set()                  # «una volta per turno» (R 4.15)
        self.tmp = Counter()                # effetti «in questo turno»
        self.mosso = False
        self.scontri = 0
        self.morti = 0

    def __repr__(self):
        return f"{self.classe}{self.idx}"

    def equip(self):
        return [K.CARTE[c] for c in self.slot.values()]

    def ha(self, chiave):
        return any(chiave in c.p for c in self.equip())

    def pl(self):
        return sum(c.pl for c in self.equip())

    @property
    def pv_tot(self):
        """PV totali: 5 + gli (+N) PV degli Equipaggiamenti (la Specie non ne dà)."""
        return PV_INIZIO + sum(c.p.get('pv', 0) for c in self.equip())

    @property
    def pv(self):
        """PV rimasti = PV totali - Danni (le soglie dell'IA e del regolamento «N PV o meno» valgono su questo)."""
        return self.pv_tot - self.danni

    @pv.setter
    def pv(self, v):
        self.danni = max(0, self.pv_tot - v)

    def stat(self, g, k):
        v = self.base[k] + sum(c.p.get(k, 0) for c in self.equip()) + self.tmp[k]
        if k == 'ar' and 'Fede' in self.stati:
            v += 1
        if k == 'ar' and self.pv <= 2:      # «Se hai 2 PV o meno: (+N) AR»
            v += sum(c.p.get('ar_pv2', 0) for c in self.equip())
        if g.mappa and k in ('att', 'ar', 'mov'):
            p = K.CARTE[g.mappa].p
            v += p.get(k, 0)
            if k == 'mov' and g.mappa_mov_avv and g.mappa_di is not self:
                v += p.get('mov_avv', 0)
        return v


def giro(g, da, compreso=True):
    """Ordine orario (a sinistra) a partire da `da`."""
    n = len(g.eroi)
    return [g.eroi[(da + i) % n] for i in range(0 if compreso else 1, n)]


def avversari(g, e):
    return [x for x in g.eroi if x is not e]


def leader(g, e):
    """L'avversario più vicino alla vittoria (per le scelte «un avversario» dell'IA)."""
    return max(avversari(g, e), key=lambda x: (x.indizi, x.pl(), len(x.mano)))


# --- mano, pesca, scarti (R 12.3-12.6) --------------------------------------------------------------

def _prendi_in_mano(g, e, cid):
    if len(e.mano) >= g.opz.mano_max:       # D8: prima scarti, poi prendi
        scarta(g, e, ia.da_scartare(g, e))
        g.st['scarti_mano_max'] += 1
    e.mano.append(cid)


def _riciclo(g):
    """R 12.6: le carte comuni degli scarti di tutti, rimescolate, vanno in fondo al mazzo comune."""
    nuove = []
    for x in g.eroi:
        nuove += [c for c in x.scarti if not K.CARTE[c].classe]
        x.scarti = [c for c in x.scarti if K.CARTE[c].classe]
    g.rng.shuffle(nuove)
    g.mazzo[0:0] = nuove                    # la cima del mazzo è la fine della lista
    g.st['ricicli'] += 1


def pesca(g, e, dalla_pila=False):
    """«Pesca 1 carta» = dal mazzo comune. `dalla_pila`: solo i testi che dicono «pila di classe» (CO-11); pila di
    classe vuota → mazzo comune (R 12.6). Nessuna pesca automatica dalla pila."""
    if dalla_pila and e.pila:
        _prendi_in_mano(g, e, e.pila.pop())
        return True
    if not g.mazzo:
        _riciclo(g)
    if not g.mazzo:
        return False
    _prendi_in_mano(g, e, g.mazzo.pop())
    return True


def loot(g, e):
    """Bottino (regola del 13/11): chi sconfigge un mostro dei mazzetti 1-2 rivela le prime LOOT carte del mazzo comune, ne tiene 1
    (l'IA la migliore) e rimette le altre in fondo, coperte. Con meno carte si rimescolano gli scarti comuni (R 12.6);
    se ne restano ancora meno si guarda quel che c'è. Mano massima: R 12.4 (prima scarti, poi prendi)."""
    if len(g.mazzo) < LOOT:
        _riciclo(g)
    viste = [g.mazzo.pop() for _ in range(min(LOOT, len(g.mazzo)))]
    if not viste:
        return
    scelta = max(viste, key=lambda c: ia._val_mano(e, c))
    viste.remove(scelta)
    g.mazzo[0:0] = viste                    # in fondo al mazzo comune
    _prendi_in_mano(g, e, scelta)
    g.st['loot'] += 1
    g.st['loot_scartate'] += len(viste)


def scarta(g, e, cid):
    e.mano.remove(cid)
    agli_scarti(g, e, cid)
    for c in e.equip():
        if 'palline' in c.p and c.id not in e.usati:
            _palline(g, e, c)


def _palline(g, e, c):
    """CG-12: una volta per turno, quando scarti, puoi tirare 1 D6 (l'IA tira con 3 PV o più e un bersaglio)."""
    sc = g.scontro
    creatura = sc is not None and not sc.finito and not sc.duello and sc.eroe is e and sc.nemico.pv > 0
    vicini = [x for x in avversari(g, e) if x.pv > 0 and g.plancia.accanto(e.pos, x.pos)]
    if e.pv < 3 or not (creatura or vicini):
        return
    e.usati.add(c.id)
    d = tiri.dado(g, 'D6', e)
    if d <= 2:
        danneggia(g, e, 1)
    elif creatura:
        sc.danni_creatura(1 if d <= 4 else 2)
    elif d >= 5:
        danneggia(g, max(vicini, key=lambda x: x.indizi), 2, e)


def riprendi(g, e, n=1, filtro=None, escludi=()):
    for _ in range(n):
        ok = [c for c in e.scarti if c not in escludi and (filtro is None or filtro(K.CARTE[c]))]
        if not ok:
            return
        cid = max(ok, key=K.valore)
        e.scarti.remove(cid)
        _prendi_in_mano(g, e, cid)
        g.st['riprese'] += 1


def ricevi(g, e, cid):
    _prendi_in_mano(g, e, cid)


# --- Stati (§9) ---------------------------------------------------------------------------------------

def dai_stato(g, e, s):
    e.stati[s] = g.eroi[g.attivo] is e      # nel proprio turno orizzontale (di traverso), altrimenti verticale (dritto)
    g.st['stati_' + s] += 1


def togli_stati_piu(e):
    for s in [s for s in e.stati if s in STATI_PIU]:
        del e.stati[s]


def annulla(g, v):
    """Una carta nella catena è annullata (R 4.11). CS-18: una volta per turno, Forte Volontà a chi ha giocato
    l'Incanto annullato."""
    v.annullata = True
    x = v.eroe
    if K.CARTE[v.cid].tipo == 'TI':
        for c in x.equip():
            if 'incanto_annullato_fv' in c.p and c.id not in x.usati:
                x.usati.add(c.id)
                x.fv = True


# --- Equipaggiamenti (R 4.2, R 11.1, §14.5) ---------------------------------------------------------

def equipaggia(g, e, cid):
    c = K.CARTE[cid]
    if c.slot in e.slot:
        lascia_slot(g, e, c.slot)
    e.slot[c.slot] = cid
    p = c.p
    if 'fv_entra' in p:
        if e.fv and 'fv_gia_stato' in p:
            dai_stato(g, e, p['fv_gia_stato'])
        e.fv = True
    if 'cura_entra' in p:
        cura(g, e, tiri.dado(g, p['cura_entra']), carta=False)
    if 'recupera_entra_indizi2' in p and e.indizi >= 2:
        riprendi(g, e, 1)
    if 'recupera_incanto_entra' in p:
        riprendi(g, e, 1, filtro=lambda x: x.tipo == 'TI')
    if 'scry_mostri_entra' in p:
        ia.scry_mostri(g, e, p['scry_mostri_entra'])
    if 'distruggi_entra' in p:
        bersagli = [(x, s) for x in avversari(g, e) for s in ('Arma DX / Scudo', 'Arma SX')
                    if s in x.slot and 'mai_perso' not in K.CARTE[x.slot[s]].p]
        if bersagli:
            x, s = max(bersagli, key=lambda t: (K.CARTE[t[0].slot[t[1]]].pl, t[0].indizi))
            lascia_slot(g, x, s)
            g.st['distrutti'] += 1
    if 'ruba_entra' in p:
        ruba(g, e, leader(g, e))


def agli_scarti(g, e, cid):
    """Ogni carta che va negli scarti (giocata, che lascia lo slot, scartata dalla mano per costo, mano massima, mill...)
    entra negli scarti di chi la possiede; se l'aveva presa dalla pila di classe di un avversario (TI-28), negli scarti
    di quell'avversario."""
    (g.origine.pop(cid, None) or e).scarti.append(cid)


def lascia_slot(g, e, s):
    cid = e.slot.pop(s)
    agli_scarti(g, e, cid)
    p = K.CARTE[cid].p
    if 'lascia_stato' in p:
        dai_stato(g, e, p['lascia_stato'])
    if 'lascia_recupera' in p:
        riprendi(g, e, p['lascia_recupera'], escludi=(cid,))
    e.danni = min(e.danni, e.pv_tot - 1)    # un Equipaggiamento con (+N) PV che esce: i PV calano, i Danni restano ma non uccidono


def sacrifica(g, e, s):
    lascia_slot(g, e, s)
    g.st['sacrifici'] += 1
    for c in e.equip():                     # CA-13: quando sacrifichi un altro tuo Equipaggiamento
        e.tmp['danno_next'] += c.p.get('sac_danno', 0)


def perdita(g, e):
    """D6 della perdita (R 11.1): tiro che apre una catena."""
    t = tiri.Tiro(g, e, 'perdita', 1)
    catena.catena_tiro(g, t)
    r = t.valore()
    persi = []
    if r == 1:
        persi = [s for s, c in e.slot.items() if 'mai_perso' not in K.CARTE[c].p]
    elif r <= 5:
        s = K.SLOT[r - 2]
        if s in e.slot and 'mai_perso' not in K.CARTE[e.slot[s]].p:
            persi = [s]
    for s in persi:
        lascia_slot(g, e, s)
    g.st['oggetti_persi'] += len(persi)


# --- PV, danni, sconfitta (§11) -----------------------------------------------------------------------

def cura(g, e, n, carta=True):
    if carta:
        n += sum(c.p.get('cura_carte', 0) for c in e.equip())
        if g.mappa and 'cura_carte' in K.CARTE[g.mappa].p:
            n += 1
    e.danni = max(0, e.danni - n)           # «togli N Danni» (ex «recuperi N PV»): mai sotto 0


def danneggia(g, e, n, fonte=None):
    """Danni a un eroe. `fonte`: Eroe, creatura o None. Riflesso: chi fa Danni ne subisce 1."""
    if n <= 0 or e.pv <= 0:
        return
    e.pv -= n
    e.tmp['ferito'] += n
    if 'Riflesso' in e.stati and fonte is not None and fonte is not e:
        ferisci(g, fonte, 1, None)
    if e.pv <= 0:
        sconfitta(g, e)


def ferisci(g, bersaglio, n, fonte):
    """Danni a un eroe o alla creatura dello scontro."""
    if isinstance(bersaglio, Eroe):
        danneggia(g, bersaglio, n, fonte)
    elif g.scontro and bersaglio is g.scontro.nemico:
        g.scontro.danni_creatura(n)


def sconfitta(g, e):
    e.morti += 1
    g.st['morti'] += 1
    if e.classe == 'Assaltatore' and e.potere and e.pl() >= 2:
        e.potere = False                    # TC-01: non tira il D6 della perdita
        g.st['potere_Assaltatore'] += 1
    else:
        perdita(g, e)
    occ = {x.pos for x in g.eroi if x is not e}
    if e.partenza in occ:
        liberi = [h for h in g.plancia.vicini[e.partenza] if h not in occ]
        e.pos = g.rng.choice(liberi) if liberi else e.partenza
    else:
        e.pos = e.partenza
    e.danni = 0
    pesca(g, e)
    if g.scontro and e in g.scontro.lati():
        g.scontro.finito = True
    if g.eroi[g.attivo] is e:
        g.turno_finito = True


def tessera_dalla_riserva(g):
    """Una tessera Esplorazione coperta: prima dalla riserva, poi dalle usate mescolate (R 8.11); None se finite."""
    if not g.riserva and g.usate:
        g.riserva, g.usate = g.usate, []
        g.rng.shuffle(g.riserva)
    return g.riserva.pop() if g.riserva else None


def togli_tessera(g, h):
    """La tessera su `h` torna coperta nella riserva."""
    t = g.tessere.pop(h)
    g.riserva.append('rossa' if t == 'scoperta' else t)


def posa_tessere(g, n, chi, zona=None, a_turno=True):
    """D29, N39: posa fino a `n` tessere coperte (prima la riserva, poi le usate mescolate), una per esagono, su esagoni
    percorribili a >= 2 dalle Partenze, senza eroi, Cripta o altre tessere (`zona`: solo quegli esagoni). Le posano a turno
    i giocatori a partire da `chi`, ognuno col proprio `ia.posto_tessera`; con `a_turno=False` le posa tutte `chi` (carta
    Mappa). Ritorna quante ne ha posate."""
    occupati = set(g.tessere) | {x.pos for x in g.eroi}
    if g.mimi:
        occupati.add(g.mimi)
    liberi = [h for h in g.plancia.idonee_tessera(occupati) if zona is None or h in zona]
    ordine = giro(g, chi.idx) if a_turno else [chi]
    posate = 0
    while posate < n and liberi:
        t = tessera_dalla_riserva(g)
        if t is None:
            break
        h = ia.posto_tessera(g, ordine[posate % len(ordine)], liberi)
        liberi.remove(h)
        g.tessere[h] = t
        posate += 1
    return posate


def cambia_plancia(g, mappa, chi):
    """R 8.12 (D24): la Mappa `mappa` (None = nessuna Mappa in gioco) cambia solo i suoi 3 fiori del montaggio; le tessere
    Esplorazione su quei fiori tornano nella riserva e `chi` (ha giocato la carta) ne posa altrettante sui fiori nuovi. La Cripta
    si sposta (con lo stesso punto 2D6) solo se ora è su un ostacolo. Ogni eroe torna sulla sua Partenza iniziale (non
    è una sconfitta); uno scontro o un Duello in corso finisce senza vincitore."""
    if mappa == g.cambi:
        return
    vecchia = M.disposizione(g.montaggio, g.cambi)
    nuova = M.disposizione(g.montaggio, mappa)
    g.cambi = mappa
    g.st['cambi_plancia' if mappa else 'cambi_plancia_base'] += 1
    sc = g.scontro
    if sc is not None and not sc.finito:
        sc.finito = sc.annullato = True
        g.st['duelli_annullati' if sc.duello else 'scontri_annullati'] += 1
        g.st['custode_annullato'] += sc.custode
    for x in g.eroi:
        x.pos = x.pos_inizio = x.partenza
    cambiati = [s for s in nuova if nuova[s] != vecchia[s]]
    zona = M.esagoni_fiori(cambiati)
    g.plancia = M.Plancia(M.terreno(nuova))
    levati = [h for h in g.tessere if h in zona]
    for h in levati:
        togli_tessera(g, h)
    if g.mimi and g.mimi not in g.plancia.libero:
        posa_cripta(g, g.cripta_xy)
    posa_tessere(g, len(levati), chi, zona, a_turno=False)


# --- Indizi e tesoro (§10) ----------------------------------------------------------------------------

def prendi_indizio(g, e, fonte):
    e.indizi += 1
    g.st['indizi_' + fonte] += 1
    if e.indizi >= 3 and not g.tesoro_trovato:
        g.tesoro_trovato = True
        g.round_tesoro = g.round
        for x in avversari(g, e):           # «la voce si sparge» (R 10.6)
            x.indizi += 1
            g.st['indizi_voce'] += 1
        if g.mimi is None:
            posa_cripta(g, tira_cripta(g))
    g.max_indizi = max(g.max_indizi, sum(x.indizi for x in g.eroi))


def ruba(g, e, x):
    if x.mano:
        cid = g.rng.choice(x.mano)
        x.mano.remove(cid)
        ricevi(g, e, cid)


def tira_cripta(g):
    """D24: 2D6 per la colonna e 2D6 per la riga (2-12)."""
    return tuple(g.rng.randint(1, 6) + g.rng.randint(1, 6) for _ in range(2))


def posa_cripta(g, xy):
    """Metti la Cripta (con MIMI e il custode) sul punto tirato `xy`. Se cade su una tessera Esplorazione, la tessera
    torna coperta nella riserva e la Cripta resta lì."""
    g.cripta_xy = xy
    g.mimi = g.plancia.cripta(*xy, g.tessere)
    if g.mimi in g.tessere:
        togli_tessera(g, g.mimi)
        g.st['cripta_su_tessera'] += 1
    g.st['cripta_tirata'] += 1
    g.st['cripta_spostata'] += g.mimi != xy


def sposta_tesoro(g):
    if g.mimi is None:
        return False
    posa_cripta(g, tira_cripta(g))
    g.st['tesoro_spostato'] += 1
    return True
