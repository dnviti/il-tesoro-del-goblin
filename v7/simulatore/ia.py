"""IA semplice (10 profili: classe x direzione). Scelte di preparazione, movimento, fuga, Duello, effetti
automatici e poteri. Le carte da aprire e le risposte sono in ia_carte.py."""
import carte as K
import mappa as M
import stato as S
import tiri
from ia_carte import apri, rispondi      # noqa: F401  (interfaccia usata da catena.py)


def _val_mano(e, cid):
    c = K.CARTE[cid]
    v = K.valore(cid)
    if c.equip and c.slot in e.slot and K.CARTE[e.slot[c.slot]].pl >= c.pl:
        v -= 4
    return v


def da_scartare(g, e):
    return min(e.mano, key=lambda c: _val_mano(e, c))


MAZZETTO = 10          # D22: mazzetto di classe = 10 carte scelte tra quelle della classe (le altre in scatola)
DA_DIREZIONE = 7       # quante ne prende al massimo dalla propria direzione; il resto dall'altra


def mazzetto_classe(g, e):
    tutte = K.CARTE_CLASSE[e.classe]
    if len(tutte) <= MAZZETTO:
        return list(tutte)

    def ordina(cs):       # per valore, a parità a caso
        return sorted(cs, key=lambda c: (-K.valore(c), g.rng.random()))
    mie = ordina(c for c in tutte if K.CARTE[c].direzione == e.direzione)
    altre = ordina(c for c in tutte if K.CARTE[c].direzione != e.direzione)
    scelte = mie[:DA_DIREZIONE]
    scelte += altre[:MAZZETTO - len(scelte)]
    resto = ordina(c for c in tutte if c not in scelte)      # se un lato è corto, completa con l'altro
    return scelte + resto[:MAZZETTO - len(scelte)]


def mano_iniziale(g, e, mazzetto):
    return sorted(mazzetto, key=lambda c: (-K.valore(c), g.rng.random()))[:3]


def equip_iniziale(g, e):
    eq = [c for c in e.mano if K.CARTE[c].equip]
    return max(eq, key=lambda c: (K.CARTE[c].pl, g.rng.random())) if eq else None


def pesca_da_pila(g, e):
    return bool(e.pila) and sum(1 for c in e.mano if K.CARTE[c].classe) < 3


def scry_mostri(g, e, n):
    tier = 1 if e.pl() <= 3 else (2 if e.pl() <= 7 else 3)
    mz = g.mazzetti[tier]
    testa = sorted(mz[:n], key=lambda m: K.MOSTRI[m].pv + 2 * K.MOSTRI[m].att + K.MOSTRI[m].ar)
    mz[:n] = testa


def scry_imprevisti(g, e, n):
    testa = sorted(g.imprevisti[:n], key=lambda x: x == 'Trappola')
    g.imprevisti[:n] = testa


def scegli_profezia(g, o, tipo):
    if g.rng.random() < 0.15:
        return g.rng.randint(1, 6)
    return 'Alto' if tipo == 'mio' else g.rng.choice(('Pari', 'Dispari', 'Alto', 'Basso'))


# --- stime ---------------------------------------------------------------------------------------------

P2D6 = {k: sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= k) / 36 for k in range(-10, 20)}


def p_colpo(att, ar):
    return P2D6[max(-10, min(19, ar - att))]


def p_duello(g, a, b):
    """Stima grezza della probabilità che l'eroe a vinca un Duello contro b (colpi necessari a testa)."""
    da = p_colpo(a.stat(g, 'att'), b.stat(g, 'ar')) * 3.5
    db = p_colpo(b.stat(g, 'att'), a.stat(g, 'ar')) * 3.5
    ta = b.pv / max(da, 0.1)
    tb = a.pv / max(db, 0.1)
    return tb / (ta + tb)


# --- movimento, fuga, Duello ------------------------------------------------------------------------------

def destinazione(g, e, mete):
    pronto = e.pv >= min(4, e.pvmax(g))
    if e.indizi >= 3 and g.mimi:
        if g.mimi in mete and pronto:
            return g.mimi
        if pronto or g.mimi not in mete:
            return min(mete, key=lambda h: (g.plancia.dist[h][g.mimi], g.tessere.get(h) not in ('rossa', 'blu'),
                                            g.rng.random()))
    coperte = [q for q, t in g.tessere.items() if t in ('rossa', 'blu')]
    scoperte = [q for q, t in g.tessere.items() if t == 'scoperta']

    def punti(h):
        t = g.tessere.get(h)
        if t in ('rossa', 'blu'):
            return 10 if e.pv >= 3 else 3
        if t == 'scoperta':
            return 8 if e.pv >= 4 else -5
        if e.pv >= 4 and any(g.plancia.accanto(h, x.pos) and x.indizi and p_duello(g, e, x) >= 0.6
                             for x in S.avversari(g, e)):
            return 6
        mete_lontane = coperte or scoperte
        return -min((g.plancia.dist[h][q] for q in mete_lontane), default=0)
    return max(mete, key=lambda h: (punti(h), g.rng.random()))


def fuggire(g, e, sc):
    m = sc.nemico
    if sc.duello:
        return False
    rischio = p_colpo(sc.att_nemico(), e.stat(g, 'ar')) * (2.5 + min(m.lv, 3) - 1)
    return e.pv <= rischio + 0.5 and m.pv > 3


def sfida(g, e, vicini):
    ok = [x for x in vicini if x.indizi > 0 and e.pv >= 3 and p_duello(g, e, x) >= 0.55]
    return max(ok, key=lambda x: x.indizi) if ok else None


def rifiuta(g, x, e):
    """Rifiutare costa 1 carta a caso; accettare e perdere costa 1 Indizio e la sconfitta."""
    return p_duello(g, x, e) < 0.35


# --- effetti automatici (R 4.12) e poteri --------------------------------------------------------------

def _vuole_alzare(g, p, t):
    """True se p vuole che il tiro t salga, False se vuole che scenda, None se indifferente."""
    mio = t.chi is p
    if t.tipo in ('colpo', 'danno', 'iniz'):
        if mio:
            return True
        return False if t.bersaglio is p or _pericoloso(g, p, t.chi, t.bersaglio) else None
    if t.tipo in ('indizio', 'trappola'):
        return (False if mio else (True if isinstance(t.chi, S.Eroe) and t.chi.indizi >= 1 else None))
    return None


def _pericoloso(g, p, chi, bersaglio):
    """Un avversario vicino alla vittoria che attacca il custode."""
    sc = g.scontro
    return (sc is not None and sc.custode and chi is sc.eroe and chi is not p) or \
        (isinstance(chi, S.Eroe) and chi.indizi >= 3 and chi is not p and isinstance(bersaglio, S.Eroe) is False)



def automatici(g, t):
    if (t.soglia is None and t.tipo != 'perdita') or g.scontro is not None and g.scontro.ab('nessun_ritiro') is not None:
        return
    for p in S.giro(g, g.attivo):
        alza = _vuole_alzare(g, p, t)
        mio = t.chi is p
        if t.tipo == 'perdita' and mio:
            r = t.valore()
            perdo = (r == 1 and p.slot) or (2 <= r <= 5 and K.SLOT[r - 2] in p.slot
                                            and K.CARTE[p.slot[K.SLOT[r - 2]]].pl >= 2)
            if perdo and p.fv:
                p.fv = False
                g.st['fv_usate'] += 1
                t.ritira()
            elif perdo and r in (1, 3) and p.ha('perdita_ritira'):
                t.ritira()
            continue
        if alza is None or t.soglia is None:
            continue
        if not (not t.ok() if mio else t.ok()):
            continue
        verso = mio != t.basso            # True = si ritira il dado più basso per alzare
        if mio and t.tipo == 'colpo' and p.ha('archibugio') and 'CA-15' not in p.usati \
                and t.soglia - t.valore() <= 3:
            p.usati.add('CA-15')                # CA-15: (-2) AR in questo turno e (+3) al tiro per colpire
            p.tmp['ar'] -= 2
            t.mod += 3
        elif mio and p.fv and t.tipo in ('colpo', 'indizio'):
            p.fv = False
            g.st['fv_usate'] += 1
            t.ritira(un_dado=True, alza=verso)
            if t.tipo == 'colpo':
                for c in p.equip():
                    if 'fv_colpo' in c.p:
                        t.mod += c.p['fv_colpo']
                        t.danni_extra += c.p['fv_colpo_danni']
        elif p.classe == 'Stregone' and p.potere and (g.scontro and g.scontro.custode or t.tipo == 'indizio'):
            p.potere = False
            g.st['potere_Stregone'] += 1
            t.ritira(un_dado=True, alza=verso)
        elif mio and (g.scontro and g.scontro.custode or t.tipo == 'indizio') and p.ha('sac_ritira'):
            s = next(s for s, c in p.slot.items() if 'sac_ritira' in K.CARTE[c].p)
            S.sacrifica(g, p, s)                # TE-27: ritira, poi ottieni la Forte Volontà
            t.ritira(alza=verso)
            p.fv = True
        elif p.ha('ritira_turno') and 'CS-10' not in p.usati and isinstance(t.chi, S.Eroe):
            p.usati.add('CS-10')
            t.ritira(un_dado=True, alza=verso)


def para_con_equip(g, x, d):
    """TE-08 / CA-10: sacrifica lo Scudo per annullare i Danni, se il colpo è pesante o letale."""
    for s, cid in list(x.slot.items()):
        if 'parata_sacrifica' in K.CARTE[cid].p and (d >= x.pv or d >= 4):
            S.sacrifica(g, x, s)
            g.st['parate'] += 1
            return True
    return False


def poteri(g, p, momento):
    mio = g.eroi[g.attivo] is p
    if not mio:
        return
    if momento == 'M0':
        if p.classe == 'Giullare' and p.potere and g.round >= 2:
            scarto = [c for c in p.mano if _val_mano(p, c) <= 3]
            if len(scarto) >= 2 or len(p.mano) <= 2:
                p.potere = False
                g.st['potere_Giullare'] += 1
                for c in scarto:
                    S.scarta(g, p, c)
                for _ in range(len(scarto) + 1):
                    S.pesca(g, p)
        for c in p.equip():
            junk = [k for k in p.mano if _val_mano(p, k) <= 2]
            if junk and 'scarta_pesca' in c.p:
                S.scarta(g, p, junk[0])
                S.pesca(g, p)
            elif junk and 'scarta_prendi_avv' in c.p:
                pool = [(x, k) for x in S.avversari(g, p) for k in x.scarti]
                if pool:
                    S.scarta(g, p, junk[0])
                    x, k = max(pool, key=lambda t: K.valore(t[1]))
                    x.scarti.remove(k)
                    S.ricevi(g, p, k)
            elif junk and 'scarta_riprendi_equip' in c.p:    # TE-29
                if any(K.CARTE[k].equip and K.valore(k) >= 6 for k in p.scarti):
                    S.scarta(g, p, junk[0])
                    S.riprendi(g, p, 1, filtro=lambda x: x.equip)
            elif junk and 'scambia_turno' in c.p:             # CG-16: la carta presa è a caso (o la migliore)
                x = max(S.avversari(g, p), key=lambda x: len(x.mano))
                if x.mano:
                    sua = max(x.mano, key=K.valore) if len(x.mano) > len(p.mano) else g.rng.choice(x.mano)
                    p.mano.remove(junk[0])
                    x.mano.remove(sua)
                    p.mano.append(sua)
                    x.mano.append(junk[0])
                    g.st['scambi'] += 1
    elif momento == 'M1':
        for c in p.equip():
            junk = [k for k in p.mano if _val_mano(p, k) <= 2]
            if junk and 'jetpack' in c.p and not p.mosso:              # CG-18: (+2) MOV, poi scarta 1
                p.tmp['mov'] += c.p['jetpack']
                S.scarta(g, p, junk[0])
    elif momento == 'M2':
        t = g.tessere.get(p.pos)
        if t in ('rossa', 'blu', 'scoperta'):
            if p.classe == 'Ricercatore' and p.potere:
                p.potere = False
                g.st['potere_Ricercatore'] += 1
                scry_mostri(g, p, 3)
            for c in p.equip():
                if 'scry_imp_turno' in c.p:
                    scry_imprevisti(g, p, c.p['scry_imp_turno'])
                if 'scry_mostri_turno' in c.p and t != 'blu':       # CR-12
                    scry_mostri(g, p, c.p['scry_mostri_turno'])
    elif momento == 'M4' and g.scontro and g.scontro.eroe is p and not g.scontro.duello:
        sc = g.scontro
        for s, cid in list(p.slot.items()):
            if sc.custode and 'sacrifica_att' in K.CARTE[cid].p:
                S.sacrifica(g, p, s)
                p.tmp['att'] += K.CARTE[cid].p['sacrifica_att']
        for c in p.equip():                 # CS-12: una volta per turno scarta 1 carta: 1 Danno
            junk = [k for k in p.mano if _val_mano(p, k) <= 2]
            if 'cartucciera' in c.p and c.id not in p.usati and junk and sc.nemico.pv > 0:
                p.usati.add(c.id)
                S.scarta(g, p, junk[0])
                sc.danni_creatura(c.p['cartucciera'])
    elif momento == 'M6':
        x = S.leader(g, p)
        for s, cid in list(p.slot.items()):     # CG-17: sacrifica, Silenzio e scarti a caso al leader
            if 'sac_silenzio' in K.CARTE[cid].p and x.indizi >= 2 and x.mano:
                n = 2 if len(x.mano) > len(p.mano) else 1
                S.sacrifica(g, p, s)
                S.dai_stato(g, x, 'Silenzio')
                for _ in range(min(n, len(x.mano))):
                    S.scarta(g, x, g.rng.choice(x.mano))
                g.st['scarti_mill'] += n
