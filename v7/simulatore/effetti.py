"""Motore degli effetti delle carte (formule di Spec_v7.md §14.5), guidato da effetti.csv.
Ogni codice ha una funzione f(g, e, c, p, ctx, pila, tiro, voce). ctx: scelte fatte dall'IA quando gioca la carta
('bers' = 'creatura' o un Eroe, 'sac' = slot da sacrificare, 'scarta' = carta da scartare come costo, 'scelta', 'voce')."""
import carte as K
import mappa as M
import stato as S
import tiri
import ia


def paga(g, e, cid, ctx):
    """Costi pagati quando si gioca la carta (R 13.2, R 13.6): restano pagati anche se la carta non fa niente."""
    if ctx.get('sac') in e.slot:
        S.sacrifica(g, e, ctx['sac'])
        ctx['sacrificato'] = True
    if ctx.get('scarta') in e.mano:
        S.scarta(g, e, ctx['scarta'])
        ctx['scartato'] = True


def risolvi(g, v, pila, tiro):
    c = K.CARTE[v.cid]
    F.get(c.codice, f_info)(g, v.eroe, c, c.p, v.ctx, pila, tiro, v)
    if 'prof' in c.p:
        tipo = 'altrui' if c.p['prof'].endswith('altrui') else 'mio'
        if c.codice != 'ritira':         # CO-01 sceglie la Profezia prima del ritiro (in f_ritira)
            tiri.nuova_profezia(g, v.eroe, v.cid, tipo, c.p['prof'])


def info(g, cid):
    g.st['info'] += 1
    g.info[cid] += 1


def f_info(g, e, c, p, ctx, pila, tiro, voce):
    info(g, c.id)


def _creatura_viva(g):
    sc = g.scontro
    return sc is not None and not sc.finito and not sc.duello and sc.nemico.pv > 0


def _eroe_valido(g, e, x, accanto=True):
    return isinstance(x, S.Eroe) and x.pv > 0 and (not accanto or M.accanto(e.pos, x.pos))


# --- equipaggiamenti e mappe ---------------------------------------------------------------------------

def f_equip(g, e, c, p, ctx, pila, tiro, voce):
    S.equipaggia(g, e, c.id)
    g.st['equipaggiati'] += 1


def f_mappa(g, e, c, p, ctx, pila, tiro, voce):
    if c.id in e.zona:
        e.zona.remove(c.id)
    if g.mappa:
        g.mappa_di.scarti.append(g.mappa)
    g.mappa, g.mappa_di, g.mappa_mov_avv = c.id, e, False
    S.sposta_tesoro(g)
    g.st['mappe'] += 1
    if 'fv' in p:
        e.fv = True
    if 'recupera' in p and e.scarti:
        S.riprendi(g, e, 1)
        g.mappa_mov_avv = True
    if 'pesca_tutti' in p:
        for x in S.giro(g, e.idx):
            S.pesca(g, x)
        S.pesca(g, e)
    if 'cura' in p:
        S.cura(g, e, tiri.dado(g, p['cura'], e))


# --- danni, parate, scontro ----------------------------------------------------------------------------

def bonus_incanto(g, e, attacco):
    """Bonus degli Incanti d'attacco (R 13.4): CS-02, CS-03, CS-05."""
    b = 0
    if not attacco:
        return b
    b += e.tmp.pop('incanto_dopo', 0)
    for x in e.equip():
        if 'danni_incanto_turno' in x.p and 'CS-03' not in e.usati:
            e.usati.add('CS-03')
            b += x.p['danni_incanto_turno']
        if 'danni_incanto_indizi2' in x.p and e.indizi >= 2:
            b += 1
    return b


def f_danno(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if ctx.get('parato'):
        g.st['parate'] += 1
        return
    n = p['n']
    if b == 'creatura':
        if not _creatura_viva(g):
            g.st['bersaglio_sparito'] += 1
            return
        bers = g.scontro.nemico
        gia = g.scontro.ferita
    else:
        if not _eroe_valido(g, e, b):
            g.st['bersaglio_sparito'] += 1
            return
        bers = b
        gia = b.tmp['ferito'] > 0
        if 'indizi3' in p and b.indizi >= 3:
            n = p['indizi3']
    if ctx.get('sacrificato') and 'sacrifica_pl2' in p:
        n = p['sacrifica_pl2']
    attacco = isinstance(n, str)
    extra = attacco and ('dado_in_piu' in p or e.ha('dado_in_piu'))
    d = tiri.dado(g, n, e, extra) + bonus_incanto(g, e, attacco)
    if gia and ('se_ferito' in p or 'ferito_turno' in p):
        d += p.get('se_ferito', 0) + p.get('ferito_turno', 0)
    S.ferisci(g, bers, d, e)
    g.st['danni_da_carte'] += d
    if attacco:
        for x in e.equip():
            if 'colpo_dopo_incanto' in x.p and 'CS-04' not in e.usati:
                e.usati.add('CS-04')
                e.tmp['colpo_next'] += 1
    if 'uccidi' in p and b == 'creatura' and _creatura_viva(g) and not g.scontro.boss \
            and g.scontro.nemico.pv <= p['uccidi']:
        g.scontro.danni_creatura(99, diretto=True)
        g.st['uccisi_da_carta'] += 1


def f_parata(g, e, c, p, ctx, pila, tiro, voce):
    tipo = p['tipo']
    if tipo == 'attacco' and tiro is not None and tiro.tipo == 'danno' and tiro.bersaglio is e:
        if 'solo_sac' in p and not ctx.get('sacrificato'):     # CA-06: senza sacrificio solo (-N) ai Danni
            tiro.riduzione += p['rid']
            return
        tiro.annulla_danni = True
        g.st['parate'] += 1
        if ctx.get('sacrificato') and 'sacrifica_danni' in p:
            S.ferisci(g, tiro.chi, p['sacrifica_danni'], e)
        return
    if tipo == 'trappola_incanto':
        if tiro is not None and tiro.tipo == 'trappola' and tiro.chi is e:
            tiro.annulla_danni = True
            g.st['parate'] += 1
            return
        bersaglio = ctx.get('voce')
        if bersaglio is not None and not bersaglio.annullata:
            bersaglio.ctx['parato'] = True
            return
        S.dai_stato(g, e, p['ripiego'])
        return
    e.tmp['ar'] += p.get('ripiego_ar', 0)


def f_riduzione(g, e, c, p, ctx, pila, tiro, voce):
    if tiro is not None and tiro.tipo == 'danno' and tiro.bersaglio is e:
        tiro.riduzione += p['n']
    else:
        e.tmp['rid_next'] = max(e.tmp['rid_next'], p['n'])
    if ctx.get('sacrificato'):
        e.tmp['rid_tutti'] = p['n']


def f_buff(g, e, c, p, ctx, pila, tiro, voce):
    k = 2 if 'equip3' in p and len(e.slot) >= 3 else 1
    for s in ('att', 'ar', 'mov', 'dmg'):
        if s in p:
            e.tmp[s] += p[s] * (k if p[s] == 1 else 1)
    e.tmp['danno_next'] += p.get('danno_next', 0)
    if ctx.get('sacrificato') and 'att_sac' in p:
        e.tmp['att'] += p['att_sac']
    if 'perdita_fine' in p:
        e.tmp['perdita_fine'] = 1


def f_malus(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if b == 'creatura':
        if 'creature_svant_turno' in p:
            g.creature_svant = True
        elif not _creatura_viva(g):
            g.st['bersaglio_sparito'] += 1
        elif 'creatura_att1' in p:
            g.scontro.att_fisso = 1
        else:
            g.scontro.svant_next = True
    elif isinstance(b, S.Eroe):
        S.dai_stato(g, b, p['avv_stato'])


def f_ristom(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if isinstance(b, S.Eroe):
        S.dai_stato(g, b, 'Svantaggio')
        sc = g.scontro
        if sc and sc.custode and sc.eroe is b and not sc.finito:
            sc.mod_att += 3
            sc.mod_ar += 3
            g.st['ristom_custode'] += 1


def f_velo(g, e, c, p, ctx, pila, tiro, voce):
    if ctx.get('fuga') and _creatura_viva(g) and g.scontro.eroe is e:
        g.scontro.fuga_sul_posto = True
    else:
        e.tmp['mov'] += p['mov']


# --- Stati, Forte Volontà, cure, carte -----------------------------------------------------------------

def f_stato(g, e, c, p, ctx, pila, tiro, voce):
    S.dai_stato(g, e, p['s'])
    e.tmp['colpo_next'] += p.get('colpo', 0)


def f_stato_avv(g, e, c, p, ctx, pila, tiro, voce):
    bers = S.avversari(g, e) if 'tutti' in p else [ctx.get('bers')]
    for b in bers:
        if isinstance(b, S.Eroe):
            S.dai_stato(g, b, p['s'])
            if 'risposta_fv' in p and any(K.CARTE[v.cid].tipo == 'TI' and v.eroe is b for v in pila[:-1]):
                e.fv = True


def f_fv(g, e, c, p, ctx, pila, tiro, voce):
    if e.fv:
        e.tmp['colpo_next'] += p.get('colpo_se_gia', 0)
    e.fv = True


def f_cura(g, e, c, p, ctx, pila, tiro, voce):
    n = p['n']
    if 'basso2' in p and e.pv <= 2:
        n = p['basso2']
    if 'indizi3' in p and e.indizi >= 3:
        n = p['indizi3']
        S.dai_stato(g, e, p['indizi3_stato'])
    S.cura(g, e, tiri.dado(g, n, e))
    if 'recupera' in p:
        S.riprendi(g, e, p['recupera'])
    if 's' in p:
        S.dai_stato(g, e, p['s'])


def f_recupera(g, e, c, p, ctx, pila, tiro, voce):
    cinque = len(e.scarti) >= 5
    S.riprendi(g, e, p['scarti5'] if 'scarti5' in p and cinque else p['n'], escludi=(c.id,))
    if 'scarti5_fv' in p and cinque:
        e.fv = True
    if ctx.get('sacrificato') and 'sacrifica_equip' in p:
        S.riprendi(g, e, 1, filtro=lambda x: x.equip)


def f_nani(g, e, c, p, ctx, pila, tiro, voce):
    if g.scontro and e in g.scontro.lati():
        e.tmp['ar'] += p['ar']
    elif not e.fv:
        e.fv = True
    else:
        S.riprendi(g, e, 1, filtro=lambda x: x.equip)


def f_speziale(g, e, c, p, ctx, pila, tiro, voce):
    d = tiri.dado(g, 'D6', e)
    if d <= 2:
        e.tmp['ar'] -= 1
        e.pv -= 1
        if e.pv <= 0:
            S.sconfitta(g, e)
    elif d <= 4:
        e.tmp['mov'] += 2
    else:
        e.tmp['att'] += 1
        S.cura(g, e, 1)


def f_mill(g, e, c, p, ctx, pila, tiro, voce):
    bers = S.avversari(g, e) if 'tutti' in p else [ctx.get('bers')]
    for b in bers:
        if not isinstance(b, S.Eroe):
            continue
        for _ in range(min(p['n'], len(b.mano))):
            S.scarta(g, b, g.rng.choice(b.mano) if 'caso' in p else ia.da_scartare(g, b))
            g.st['scarti_mill'] += 1
        if 'indizi3' in p and b.indizi >= 3:
            S.danneggia(g, b, tiri.dado(g, p['indizi3'], e), e)
            S.sposta_tesoro(g)
    if 'tutti' in p and ctx.get('duello'):
        info(g, c.id)


def f_maledizione(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if not isinstance(b, S.Eroe):
        return
    if len(b.mano) >= 5:
        for _ in range(2):
            S.scarta(g, b, ia.da_scartare(g, b))
        g.st['scarti_mill'] += 2
    else:
        S.dai_stato(g, b, 'Fermo')


def f_ruba(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if isinstance(b, S.Eroe) and b.mano:
        cid = max(b.mano, key=K.valore) if len(b.mano) > len(e.mano) else g.rng.choice(b.mano)
        b.mano.remove(cid)
        S.ricevi(g, e, cid)
        g.st['furti'] += 1


def f_scambia(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if not isinstance(b, S.Eroe):
        return
    piu = len(b.mano) > len(e.mano)
    n = p.get('piu_carte', 1) if piu else p['n']
    for _ in range(n):
        if not e.mano or not b.mano:
            break
        mia = ia.da_scartare(g, e)
        sua = g.rng.choice(b.mano)          # «guarda la mano» non modellato: la scelta è a caso
        e.mano.remove(mia)
        b.mano.remove(sua)
        e.mano.append(sua)
        b.mano.append(mia)
        g.st['scambi'] += 1
    if 'piu_carte_stato' in p:
        if piu:
            S.dai_stato(g, b, p['piu_carte_stato'])
        info(g, c.id)


def f_tempo_scaduto(g, e, c, p, ctx, pila, tiro, voce):
    for x in S.giro(g, e.idx):
        com = [k for k in x.mano if not K.CARTE[k].classe]
        for k in com:
            S.scarta(g, x, k)
        for _ in range(len(com) - (0 if x is e else 1)):
            S.pesca(g, x)


def f_vera_volonta(g, e, c, p, ctx, pila, tiro, voce):
    altre = [k for k, v in g.scatola.items() if k != e.classe and v]
    if not altre:
        return
    box = g.scatola[g.rng.choice(altre)]
    for _ in range(min(p['n'], len(box))):
        S.ricevi(g, e, box.pop(g.rng.randrange(len(box))))


def f_perdita_tutti(g, e, c, p, ctx, pila, tiro, voce):
    for x in S.giro(g, e.idx):
        S.perdita(g, x)


def f_torna_partenza(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if isinstance(b, S.Eroe):
        occ = {x.pos for x in g.eroi if x is not b}
        if b.partenza in occ:
            liberi = [h for h in M.VICINI[b.partenza] if h not in occ]
            b.pos = liberi[0] if liberi else b.pos
        else:
            b.pos = b.partenza
        g.st['torna_partenza'] += 1
    e.pv = 1


def f_amisal(g, e, c, p, ctx, pila, tiro, voce):
    if g.eroi[g.attivo] is e and not e.mosso:
        e.tmp['mov'] += p['mov']
    else:
        info(g, c.id)                       # scry del mazzo comune


def f_scry_imp(g, e, c, p, ctx, pila, tiro, voce):
    S.dai_stato(g, e, p['s'])
    ia.scry_imprevisti(g, e, p['n'])
    if g.eroi[g.attivo] is e and not e.mosso:
        e.tmp['mov'] += p['mov_fermo']


# --- tiri e catena -------------------------------------------------------------------------------------

def f_mod_tiro(g, e, c, p, ctx, pila, tiro, voce):
    if tiro is None:
        g.st['bersaglio_sparito'] += 1
        return
    if 'qualsiasi' in p:
        tiro.mod += ctx.get('segno', 1) * p['n']
        if 'nega_indizio' in p and tiro.tipo == 'indizio' and tiro.chi is not e and isinstance(tiro.chi, S.Eroe):
            tiro.no_indizio = True
        return
    n = p['n']
    if ctx.get('sacrificato') and 'n_sac' in p:
        n = p['n_sac']
        tiro.danni_extra += p.get('danni_sac', 0)
    if ctx.get('scartato') and 'scarta_n' in p:
        n = p['scarta_n']
    if 'scarti5_danni' in p and len(e.scarti) >= 5:
        tiro.danni_extra += 1
    tiro.mod += n
    if 'scontro_creatura' in p and _creatura_viva(g):
        g.scontro.mod_att -= 1
        g.scontro.mod_ar -= 1
    if 'incanto_dopo' in p:
        e.tmp['incanto_dopo'] = p['incanto_dopo']


def f_ritira(g, e, c, p, ctx, pila, tiro, voce):
    if 'prof' in p:
        tiri.nuova_profezia(g, e, c.id, 'mio', p['prof'])
    if tiro is None or ('proprio' in p and tiro.chi is not e):
        if p.get('ripiego') == 'fv':
            e.fv = True
        else:
            info(g, c.id)
        return
    if 'avv_bonus' in p and isinstance(tiro.bersaglio, S.Eroe):
        tiro.mod += p['avv_bonus']
    tiro.ritira(un_dado='un_dado' in p, alza=ctx.get('alza', True))


def f_annulla(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('voce')
    if b is not None and K.CARTE[b.cid].tipo == p['tipo'] and not b.annullata:
        b.annullata = True
        return
    if p['tipo'] == 'TM' and ctx.get('togli_mappa') and g.mappa:
        g.mappa_di.scarti.append(g.mappa)
        g.mappa = g.mappa_di = None
        return
    if p['ripiego'] == 'fv':
        e.fv = True
    elif isinstance(ctx.get('bers'), S.Eroe):
        S.dai_stato(g, ctx['bers'], p['ripiego'])


F = {k[2:]: v for k, v in globals().items() if k.startswith('f_')}
