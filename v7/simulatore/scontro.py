"""Scontri (§7): iniziativa, tiri per colpire e danno con le loro catene, fuga, ricompense (D11, D18), custode di
MIMI, Duello (R 10.8-10.10). Le abilità dei mostri sono in mostri.py."""
import carte as K
import stato as S
import catena as C
import mostri as AB
import tiri
import ia


MAX_ATTACCHI = 3


class Creatura:
    def __init__(self, g, mid):
        m = K.MOSTRI[mid]
        self.id, self.nome, self.lv, self.tier = m.id, m.nome, m.lv, m.tier
        self.pv = self.pv0 = m.pv
        self.att = m.att
        self.ar = K.AR_V7_A_V6.get(m.ar, m.ar) if g.opz.ar_v6 else m.ar
        self.ab = {c: p for c, p in K.ABILITA[mid]}

    def __repr__(self):
        return self.nome


class Scontro:
    def __init__(self, g, eroe, nemico, custode=False, duello=False):
        self.g, self.eroe, self.nemico = g, eroe, nemico
        self.custode, self.duello = custode, duello
        self.boss = not duello and (custode or nemico.tier == 3)
        self.finito = self.fuga_sul_posto = self.ferita = self.colpito = False
        self.annullato = self.sparito = False
        self.attacchi_eroe = 0                  # al 3° attacco senza vincere il mostro scappa (mai il custode)   # R 8.12 cambio di mappa; TI-41 il mostro sparisce
        self.mod_att = self.mod_ar = 0
        self.att_fisso = None
        self.svant_next = False
        self.primo_tiro = True
        self.eroe_primo = False
        self.colpi_mostro = self.attacchi_mostro = 0
        self.ricomposto = self.nebbia_usata = self.svegliato = self.attacco_extra = self.scappato = False

    def lati(self):
        return [self.eroe, self.nemico] if self.duello else [self.eroe]

    def ab(self, k):
        return None if self.duello else self.nemico.ab.get(k)

    def danni_creatura(self, n, diretto=False, attacco=False):
        AB.danni_creatura(self.g, self, n, attacco=attacco, diretto=diretto)

    def att_nemico(self):
        if self.att_fisso is not None:
            return self.att_fisso
        return AB.att(self.g, self, self.nemico.att + self.mod_att)

    def ar_nemico(self):
        a = self.nemico.ar + self.mod_ar
        if self.g.mappa:
            a += K.CARTE[self.g.mappa].p.get('creature_ar', 0)
        return AB.ar(self.g, self, a)


def _vant_eroe(g, e, sc, primo):
    v = 0
    if 'Vantaggio' in e.stati or e.ha('vant') or (sc.boss and e.ha('vant_boss')):
        v += 1
    if g.mappa and K.CARTE[g.mappa].p.get('vant_specie') == e.specie:
        v += 1
    v = min(v, 1)
    if 'Svantaggio' in e.stati:
        v -= 1
    return max(-1, min(1, v + AB.vant_eroe(sc, primo))) if not sc.duello else v


def _danni_bonus(g, e):
    b = sum(c.p.get('dmg', 0) for c in e.equip()) + e.tmp['dmg'] + e.tmp.pop('danno_next', 0)
    if 'Arma DX / Scudo' not in e.slot:
        b += sum(c.p.get('dmg_dx_vuoto', 0) for c in e.equip())
    sc = g.scontro
    if sc is not None and not sc.duello and sc.nemico.lv >= 3:      # «Se combatti una creatura di LV 3 o più»
        b += sum(c.p.get('dmg_lv3', 0) for c in e.equip())
    return b


def _danno_finale(g, td, x, extra=0):
    """Riduzioni e parate (§14.5): dopo il tiro, minimo 0."""
    d = td.valore() + extra
    d -= td.riduzione + x.tmp.pop('rid_next', 0) + x.tmp['rid_tutti']
    if td.annulla_danni:
        return 0
    d = max(0, d)
    for c in x.equip():                     # CA-16, CA-17, CA-18: una volta per turno (-N) ai Danni di un attacco
        if d and 'rid_turno' in c.p and c.id not in x.usati:
            x.usati.add(c.id)
            d = max(0, d - c.p['rid_turno'])
    if d and ia.para_con_equip(g, x, d):
        return 0
    return d


def attacco_eroe(g, sc, x, y):
    """x attacca y (y = creatura, oppure eroe nel Duello)."""
    primo = sc.primo_tiro and x is sc.eroe
    if x is sc.eroe and not sc.duello:
        sc.attacchi_eroe += 1
    sc.primo_tiro = sc.primo_tiro and x is not sc.eroe
    base = x.stat(g, 'att') + x.tmp.pop('colpo_next', 0) + (sc.ab('att_eroe') or {}).get('n', 0)
    soglia = y.stat(g, 'ar') if sc.duello else sc.ar_nemico()
    sicuro = [c.p['colpo_sicuro'] for c in x.equip() if 'colpo_sicuro' in c.p]
    if sicuro and 'TE-26' not in x.usati and soglia - base >= 8:     # TE-26: 2 Danni senza tiro se si colpisce poco
        x.usati.add('TE-26')
        x.tmp['ar'] -= 1
        g.st['colpi_sicuri'] += 1
        if isinstance(y, S.Eroe):
            S.danneggia(g, y, sicuro[0], x)
        else:
            sc.danni_creatura(sicuro[0])
        return
    t = C.catena_tiro(g, tiri.Tiro(g, x, 'colpo', 2, base, soglia, vant=_vant_eroe(g, x, sc, primo), bersaglio=y))
    g.st['attacchi_eroe'] += 1
    if sc.finito:
        return
    if not t.ok():
        if isinstance(y, S.Eroe) and y.ha('specchio'):
            S.danneggia(g, x, 1, y)
        if not sc.duello:
            AB.eroe_manca(g, sc, x, primo)
        return
    g.st['colpi_eroe'] += 1
    td = C.catena_tiro(g, tiri.Tiro(g, x, 'danno', 1, _danni_bonus(g, x), bersaglio=y))
    if sc.finito:
        return
    extra = t.danni_extra + (sum(c.p.get('dmg_sei', 0) for c in x.equip()) if td.facce[0] == 6 else 0)
    for c in x.equip():
        if 'pistola' in c.p:                # CA-14: D6, 1-2 subisci 1 Danno, 3-4 (+1), 5-6 (+2)
            r = tiri.dado(g, 'D6', x)
            if r <= 2:
                S.danneggia(g, x, 1)
            else:
                extra += 1 if r <= 4 else 2
    if sc.finito:
        return
    if isinstance(y, S.Eroe):
        d = _danno_finale(g, td, y, extra)
        S.danneggia(g, y, d, x)
        if d and y.ha('molla') and x.pv > 0:
            S.danneggia(g, x, 1, y)         # CA-17
    else:
        d = 0 if td.annulla_danni else max(0, td.valore() + extra - td.riduzione)
        sc.danni_creatura(d, attacco=True)
    if not sc.finito and x.pv > 0:
        for c in x.equip():
            if x.pv <= 0:
                break
            if 'cura_colpo' in c.p and not sc.duello and 'TE-13' not in x.usati:
                x.usati.add('TE-13')
                S.cura(g, x, 1, carta=False)
            if 'autolesione' in c.p:
                S.danneggia(g, x, c.p['autolesione'], None)
    if sc.attacco_extra and not sc.finito and y.pv > 0:
        sc.attacco_extra = False            # NE-15 Svegliato male
        attacco_mostro(g, sc)


def attacco_mostro(g, sc):
    m, e = sc.nemico, sc.eroe
    sc.attacchi_mostro += 1
    ar = e.stat(g, 'ar') + (sc.ab('ar_eroe_attacco') or {}).get('n', 0)
    if m.lv >= 3:                           # TE-22 e Equipaggiamenti di classe: «Se combatti una creatura di LV 3 o più»
        ar += sum(c.p.get('ar_lv3', 0) for c in e.equip())
    if sc.boss:                             # «Se combatti un boss» (custode compreso)
        ar += sum(c.p.get('ar_boss', 0) for c in e.equip())
    sv = g.creature_svant or sc.svant_next or (g.mappa and 'creature_svant' in K.CARTE[g.mappa].p)
    sc.svant_next = False
    t = C.catena_tiro(g, tiri.Tiro(g, m, 'colpo', 2, sc.att_nemico(), ar, vant=-1 if sv else 0, bersaglio=e))
    if sc.finito or m.pv <= 0:
        return
    if not t.ok():
        if e.ha('specchio'):
            sc.danni_creatura(1)
        return
    if g.opz.op2:
        td = C.catena_tiro(g, tiri.Tiro(g, m, 'danno', 0, sc.att_nemico(), bersaglio=e))
    else:
        td = C.catena_tiro(g, tiri.Tiro(g, m, 'danno', 1, {1: -1, 2: 0}.get(m.lv, 1), bersaglio=e))
    if sc.finito:
        return
    sc.colpi_mostro += 1
    faccia = td.facce[0] if td.facce else 0
    extra = AB.danno_extra(g, sc, faccia) if faccia else (sc.ab('monologo') or {}).get('n', 0)
    if m.lv == 1 and not g.opz.op2:
        extra += max(1, td.valore() + extra) - (td.valore() + extra)     # D6 − 1, minimo 1
    d = _danno_finale(g, td, e, extra)
    if d:
        sc.colpito = True
    morti = e.morti
    S.danneggia(g, e, d, m)
    if e.morti > morti:
        AB.sconfigge(g, sc, e)
    elif d:
        if e.ha('molla'):
            sc.danni_creatura(1)            # CA-17: l'attaccante subisce 1 Danno
        AB.dopo_colpo(g, sc, d, faccia == 6)


def _iniziativa(g, sc):
    """R 7.2 (OP-1: l'eroe attacca sempre per primo contro ogni creatura, boss e custode compresi)."""
    if g.opz.op1 or sc.ab('monologo') is not None:
        return True
    if sc.ab('primo') is not None:
        return False
    te = C.catena_tiro(g, tiri.Tiro(g, sc.eroe, 'iniz', 1))
    tm = C.catena_tiro(g, tiri.Tiro(g, sc.nemico, 'iniz', 1))
    a, b = te.valore(), tm.valore()
    return a > b or (a == b and not sc.boss)


def tiro_indizio(g, e, lv):
    """R 10.2 con D18: Indizio se D6 <= LV + 1 (opzione --indizio-lv: D6 <= LV, v6)."""
    soglia = lv if g.opz.indizio_lv else lv + 1
    if g.mappa:
        soglia += K.CARTE[g.mappa].p.get('indizio', 0)     # TM-09: D6 <= LV + 2
    t = C.catena_tiro(g, tiri.Tiro(g, e, 'indizio', 1, soglia=soglia, basso=True))
    g.st['tiri_indizio'] += 1
    if t.ok() and not t.no_indizio:
        S.prendi_indizio(g, e, 'mostri')
    elif t.ok():
        g.st['indizi_negati'] += 1


def scontro(g, e, mid=None, custode=False):
    """Scontro con una creatura. Ritorna 'vinto', 'perso', 'fuga', 'fuga_mostro' (scappa dopo il 3° attacco) o 'annullato' (cambio di mappa, R 8.12)."""
    nemico = g.custode if custode else Creatura(g, mid)
    sc = Scontro(g, e, nemico, custode=custode)
    g.scontro = sc
    e.scontri += 1
    g.st['scontri'] += 1
    g.st['scontri_custode' if custode else f'scontri_mazzetto_{nemico.tier}'] += 1
    esito = None
    senza_indizio = AB.inizio(g, sc)
    if senza_indizio:
        esito = 'vinto'
    elif not sc.finito and nemico.pv > 0:
        C.momento(g, 'M3')
    turno_eroe = sc.finito or nemico.pv <= 0 or _iniziativa(g, sc)
    sc.eroe_primo = turno_eroe
    passi = 0
    while esito is None and not (sc.finito or g.finita) and nemico.pv > 0 and passi < 80:
        passi += 1
        if turno_eroe:
            C.momento(g, 'M4')
            if sc.finito or nemico.pv <= 0:
                break
            if sc.fuga_sul_posto:
                esito = 'fuga'
                break
            puo = not custode and sc.ab('nofuga') is None
            if puo and ia.fuggire(g, e, sc):
                if sc.ab('inseguitore') is not None:
                    attacco_mostro(g, sc)
                if not sc.finito:
                    AB.fuga(g, sc, e)
                    if sc.ab('lento') is None:
                        e.pos = e.pos_inizio
                esito = 'fuga'
                break
            attacco_eroe(g, sc, e, nemico)
        elif sc.attacchi_eroe >= MAX_ATTACCHI and not custode:
            esito = 'fuga_mostro'           # dopo il 3° attacco il mostro vivo scappa: niente premi
            break
        else:
            attacco_mostro(g, sc)
        turno_eroe = not turno_eroe
    if esito is None:
        if sc.annullato:
            esito = 'sparito' if sc.sparito else 'annullato'    # nessun vincitore, nessuna ricompensa
        elif sc.scappato:
            esito = 'fuga'                  # NE-29: come una fuga, resti sul tuo esagono
        else:
            esito = 'vinto' if nemico.pv <= 0 and not sc.finito else 'perso'
    sc.finito = True
    if esito not in ('annullato', 'sparito', 'fuga_mostro') and not sc.scappato:     # il mostro che scappa: niente «a fine scontro»
        AB.fine(g, sc, e, esito)
    g.st['esito_' + esito] += 1
    g.st['mx_n:' + nemico.id] += 1
    if esito == 'perso':
        g.st['mx_p:' + nemico.id] += 1
    g.scontro = None
    if esito == 'vinto':
        if custode:
            g.finita, g.vincitore = True, e
        else:
            if nemico.tier == 2:
                e.fv = True                 # D11
            if e.ha('motosega') and e.mano and ia._val_mano(e, ia.da_scartare(g, e)) <= 3:
                S.scarta(g, e, ia.da_scartare(g, e))      # CR-17: scarta 1, ruba 1 carta a un avversario
                S.ruba(g, e, S.leader(g, e))
            if not senza_indizio and AB.tira_indizio(g, sc, e):
                tiro_indizio(g, e, nemico.lv)
            if 'Sussurro' in e.stati and not senza_indizio:     # Mostro vinto su «?»
                del e.stati['Sussurro']
                S.prendi_indizio(g, e, 'sussurro')
    elif esito == 'fuga':
        g.st['fughe'] += 1
    elif esito == 'fuga_mostro':
        g.st['fughe_mostro'] += 1
    if custode and nemico.pv <= 0:
        g.finita, g.vincitore = True, e
    return esito


def duello(g, a, b):
    """R 10.8-10.10: a sfida b (b ha già accettato)."""
    sc = Scontro(g, a, b, duello=True)
    g.scontro = sc
    a.scontri += 1
    g.st['duelli'] += 1
    ta = C.catena_tiro(g, tiri.Tiro(g, a, 'iniz', 1)).valore()
    tb = C.catena_tiro(g, tiri.Tiro(g, b, 'iniz', 1)).valore()
    while ta == tb:
        ma, mb = a.stat(g, 'mov'), b.stat(g, 'mov')
        if ma != mb:
            ta, tb = ma, mb
        elif g.opz.op5:
            ta, tb = g.rng.randint(1, 6), g.rng.randint(1, 6)
        else:
            ta, tb = 1, 0                   # vince chi ha il turno (lo sfidante)
    x, y = (a, b) if ta > tb else (b, a)
    morti = {a.idx: a.morti, b.idx: b.morti}
    passi = 0
    while not (sc.finito or g.finita) and passi < 80:
        passi += 1
        if x is a:
            C.momento(g, 'M4')
            if sc.finito:
                break
        attacco_eroe(g, sc, x, y)
        x, y = y, x
    g.scontro = None
    perde = a if a.morti > morti[a.idx] else (b if b.morti > morti[b.idx] else None)
    if perde is None or sc.annullato:
        return
    vince = b if perde is a else a
    g.st['duelli_vinti_sfidante' if vince is a else 'duelli_vinti_sfidato'] += 1
    if perde.indizi:
        perde.indizi -= 1
        S.prendi_indizio(g, vince, 'duelli')
    if perde.scarti:
        cid = max(perde.scarti, key=K.valore)
        perde.scarti.remove(cid)
        S.ricevi(g, vince, cid)
    vince.fv = True
