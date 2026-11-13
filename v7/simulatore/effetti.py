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
    if K.CARTE[cid].tipo == 'TI':
        incanto_giocato(g, e)


def incanto_giocato(g, e):
    """Equipaggiamenti «quando giochi un Incanto» (TE-28, CS-17) e conto per TE-31 (anche se poi è annullato)."""
    e.tmp['incanti'] += 1
    for x in e.equip():
        if 'incanto_danno_next' in x.p and g.eroi[g.attivo] is e:
            e.tmp['danno_next'] += x.p['incanto_danno_next']
        if 'incanto_ricambia' in x.p and x.id not in e.usati:
            j = ia.da_scartare(g, e) if e.mano else None
            if j is not None and ia._val_mano(e, j) <= 2:
                e.usati.add(x.id)
                S.scarta(g, e, j)
                S.pesca(g, e)


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
    return isinstance(x, S.Eroe) and x.pv > 0 and (not accanto or g.plancia.accanto(e.pos, x.pos))


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
    S.cambia_plancia(g, c.id, e)               # R 8.12: prima il testo della Mappa, poi i suoi fiori
    S.sposta_tesoro(g)                      # ogni Mappa ritira la Cripta (sulla mappa nuova, senza limite)


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
    e.tmp['ar'] += p.get('ar_turno', 0)
    if 'tutti_stato' in p:
        for x in S.avversari(g, e):
            S.dai_stato(g, x, p['tutti_stato'])
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
    if ctx.get('scartato') and 'scarta_dmg' in p:
        d += p['scarta_dmg']
    if 'se_mappa' in p and g.mappa == p['se_mappa']:
        d += p['se_mappa_dmg']
    if 'sei' in p and tiri.dado(g, 'D6', e) == 6:
        d += p['sei']
    S.ferisci(g, bers, d, e)
    g.st['danni_da_carte'] += d
    if 'stato_bers' in p and isinstance(bers, S.Eroe) and bers.pv > 0:
        S.dai_stato(g, bers, p['stato_bers'])
    if 'splash' in p:
        for x in S.avversari(g, e):
            if x is not bers and _eroe_valido(g, e, x):
                S.danneggia(g, x, p['splash'], e)
    morta = b == 'creatura' and g.scontro is not None and g.scontro.nemico.pv <= 0
    if morta and 'uccisa_mill' in p and not g.scontro.boss:
        for x in S.avversari(g, e):
            if x.mano:
                S.scarta(g, x, ia.da_scartare(g, x))
                g.st['scarti_mill'] += 1
    if morta and 'uccisa_pesca' in p and e.mano:
        S.scarta(g, e, ia.da_scartare(g, e))
        S.pesca(g, e)
        S.pesca(g, e)
    if d > 0 and c.tipo == 'TI':
        _dopo_danni_incanto(g, e, b, bers, attacco)
    if attacco:
        for x in e.equip():
            if 'colpo_dopo_incanto' in x.p and 'CS-04' not in e.usati:
                e.usati.add('CS-04')
                e.tmp['colpo_next'] += 1
    if 'uccidi' in p and b == 'creatura' and _creatura_viva(g) and not g.scontro.boss \
            and g.scontro.nemico.pv <= p['uccidi']:
        g.scontro.danni_creatura(99, diretto=True)
        g.st['uccisi_da_carta'] += 1


def _dopo_danni_incanto(g, e, b, bers, attacco):
    """Una volta per turno, quando un tuo Incanto infligge Danni: CS-11 (1 Danno a un altro bersaglio), CS-13 (Forte
    Volontà; se l'avevi già (+2) AR in questo turno, solo Incanti d'attacco)."""
    for x in e.equip():
        if x.id in e.usati:
            continue
        if 'incanto_extra' in x.p:
            altri = [y for y in S.avversari(g, e) if y is not bers and _eroe_valido(g, e, y)]
            if b != 'creatura' and _creatura_viva(g):
                e.usati.add(x.id)
                g.scontro.danni_creatura(x.p['incanto_extra'])
            elif altri:
                e.usati.add(x.id)
                S.danneggia(g, max(altri, key=lambda y: (y.indizi, -y.pv)), x.p['incanto_extra'], e)
        if 'incanto_fv' in x.p and attacco:
            e.usati.add(x.id)
            if e.fv:
                e.tmp['ar'] += 2
            e.fv = True


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
    if 'equip3_danno' in p and len(e.slot) >= 3:
        e.tmp['danno_next'] += p['equip3_danno']
    if 'scarti5_danno' in p and len(e.scarti) >= 5:
        e.tmp['danno_next'] += p['scarti5_danno']
    if ctx.get('sacrificato') and 'att_sac' in p:
        e.tmp['att'] += p['att_sac']
    if 'perdita_fine' in p:
        e.tmp['perdita_fine'] = 1
    if 'fv' in p:
        e.fv = True
    if 'stato' in p:
        S.dai_stato(g, e, p['stato'])
    if 'pesca_senza_armatura' in p and 'Armatura' not in e.slot:
        S.pesca(g, e)
    if 'costo_pv_o_scarta' in p:            # CG-15: «perdi 2 PV, oppure scarta 1 carta»
        j = ia.da_scartare(g, e) if e.mano else None
        if j is not None and (ia._val_mano(e, j) <= 3 or e.pv <= 2):
            S.scarta(g, e, j)
        else:
            S.danneggia(g, e, p['costo_pv_o_scarta'])


def f_malus(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if b == 'creatura':
        if 'creature_svant_turno' in p:
            g.creature_svant = True
        elif not _creatura_viva(g) or ('non_boss' in p and g.scontro.boss):
            g.st['bersaglio_sparito'] += 1
        elif 'creatura_att1' in p:
            g.scontro.att_fisso = 1
            g.scontro.mod_ar += p.get('creatura_ar', 0)
        else:
            g.scontro.svant_next = True
    elif isinstance(b, S.Eroe):
        S.dai_stato(g, b, p['avv_stato'])
        if 'avv_stato2' in p:
            S.dai_stato(g, b, p['avv_stato2'])


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
    if ctx.get('fuga') and 'parkour' not in p and _creatura_viva(g) and g.scontro.eroe is e:
        g.scontro.fuga_sul_posto = True
    else:
        e.tmp['mov'] += p['mov']
        e.tmp['parkour'] = 1 if 'parkour' in p else e.tmp['parkour']


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
    sc = g.scontro
    if 'schiocco' in p and _creatura_viva(g) and sc.eroe is e and not sc.custode:
        sc.finito = sc.annullato = sc.sparito = True     # TI-41: il mostro sparisce, senza ricompense
        g.st['mostri_spariti'] += 1


def f_fv(g, e, c, p, ctx, pila, tiro, voce):
    if e.fv:
        e.tmp['colpo_next'] += p.get('colpo_se_gia', 0)
    e.fv = True


def f_cura(g, e, c, p, ctx, pila, tiro, voce):
    n = p['n']
    if 'basso2' in p and e.pv <= 2:
        n = p['basso2']
    if 'basso3' in p and e.pv <= 3:
        n = p['basso3']
    e.tmp['ar'] += p.get('ar_turno', 0)
    if 'fv' in p:
        e.fv = True
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


def f_gamba(g, e, c, p, ctx, pila, tiro, voce):
    """CR-13: D6. 1-2: perdi 1 PV e (+1) MOV; 3-4: (+2) MOV; 5-6: (+2) MOV e Stato Occhio."""
    d = tiri.dado(g, 'D6', e)
    e.tmp['mov'] += 1 if d <= 2 else 2
    if d >= 5:
        S.dai_stato(g, e, 'Occhio')
    elif d <= 2:
        S.danneggia(g, e, 1)


def f_pietraluce(g, e, c, p, ctx, pila, tiro, voce):
    """CR-19: D6. 1-2: prendi Rallentato; 3-4: un avversario Rallentato; 5-6: ogni avversario Rallentato.
    «Guarda la mano di ogni avversario»: info."""
    d = tiri.dado(g, 'D6', e)
    bers = [e] if d <= 2 else ([ctx.get('bers') or S.leader(g, e)] if d <= 4 else S.avversari(g, e))
    for b in bers:
        S.dai_stato(g, b, 'Rallentato')


def f_mill(g, e, c, p, ctx, pila, tiro, voce):
    bers = S.avversari(g, e) if 'tutti' in p else [ctx.get('bers')]
    for b in bers:
        if not isinstance(b, S.Eroe):
            continue
        piu = len(b.mano) > len(e.mano)
        for _ in range(min(p['n'], len(b.mano))):
            S.scarta(g, b, g.rng.choice(b.mano) if 'caso' in p else ia.da_scartare(g, b))
            g.st['scarti_mill'] += 1
        if 'pesca_dopo' in p and not piu:   # CG-19: chi aveva più carte di te non pesca
            S.pesca(g, b)
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
    if not isinstance(b, S.Eroe) or b is e:     # TI-36 può deviare la carta su chi l'ha giocata
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
    """TI-28 (13/11, Daniele): `n` carte, ognuna a caso e indipendente dalle altre, dalla scatola di una classe che nessuno
    gioca oppure dalla pila di classe di un avversario (una fonte con meno carte dà quel che ha). L'IA sceglie per ogni
    carta la fonte col valore medio più alto, a pari valore a caso. Una carta tolta alla pila di un avversario, quando
    viene giocata, va negli scarti di quell'avversario (g.origine, S.agli_scarti); dalla scatola, nei propri."""
    for _ in range(p['n']):
        fonti = [(box, None) for k, box in g.scatola.items() if k != e.classe and box]
        fonti += [(x.pila, x) for x in S.avversari(g, e) if x.pila]
        if not fonti:
            return
        fonte, di = max(fonti, key=lambda f: (sum(map(K.valore, f[0])) / len(f[0]), g.rng.random()))
        cid = fonte.pop(g.rng.randrange(len(fonte)))
        if di is not None:
            g.origine[cid] = di
        S.ricevi(g, e, cid)
        g.st['vera_volonta_scatola' if di is None else 'vera_volonta_pila'] += 1


def f_perdita_tutti(g, e, c, p, ctx, pila, tiro, voce):
    for x in S.giro(g, e.idx):
        S.perdita(g, x)


def f_dirigibile(g, e, c, p, ctx, pila, tiro, voce):
    """TI-32: ogni eroe, tu compreso, subisce D6 Danni (un tiro solo); in uno scontro anche la creatura."""
    d = tiri.dado(g, p['n'], e)
    viva = _creatura_viva(g)
    for x in S.giro(g, e.idx):
        S.danneggia(g, x, d, e if x is not e else None)
    if viva and _creatura_viva(g):
        g.scontro.danni_creatura(d)


def f_passa(g, e, c, p, ctx, pila, tiro, voce):
    """TI-38: ogni eroe sceglie N carte della sua mano (le peggiori) e le dà al giocatore alla sua destra."""
    scelte = {}
    for x in g.eroi:
        scelte[x.idx] = []
        for _ in range(min(p['n'], len(x.mano))):
            k = ia.da_scartare(g, x)
            x.mano.remove(k)
            scelte[x.idx].append(k)
    n = len(g.eroi)
    for x in g.eroi:
        destra = g.eroi[(x.idx - 1) % n]    # il giro è orario verso sinistra (S.giro): a destra è idx - 1
        for k in scelte[x.idx]:
            S.ricevi(g, destra, k)


def f_torna_partenza(g, e, c, p, ctx, pila, tiro, voce):
    b = ctx.get('bers')
    if isinstance(b, S.Eroe):
        occ = {x.pos for x in g.eroi if x is not b}
        if b.partenza in occ:
            liberi = [h for h in g.plancia.vicini[b.partenza] if h not in occ]
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
    if 's' in p:
        S.dai_stato(g, e, p['s'])
    ia.scry_imprevisti(g, e, p['n'])
    if g.eroi[g.attivo] is e and not e.mosso:
        e.tmp['mov'] += p.get('mov_fermo', 0)


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
    if 'scegli' in p:                       # CS-19: scegli il risultato di 1 D6, poi perdi 2 PV
        alza = ctx.get('alza', True)
        i = tiro.facce.index(min(tiro.facce) if alza else max(tiro.facce))
        tiro.facce[i] = 6 if alza else 1
        tiro.rit += 1                       # conta come un ritiro, con la sua penalità (D1)
        g.st['ritiri'] += 1
        S.danneggia(g, e, p['scegli'])
        return
    tiro.ritira(un_dado='un_dado' in p, alza=ctx.get('alza', True))


def _togli_mappa(g, e):
    """TI-22 / CR-15: la Mappa in gioco va negli scarti di chi l'ha giocata; i 3 fiori tornano come nel montaggio (R 8.12)."""
    g.mappa_di.scarti.append(g.mappa)
    g.mappa = g.mappa_di = None
    S.cambia_plancia(g, None, e)


def f_annulla(g, e, c, p, ctx, pila, tiro, voce):
    tipi = p['tipo'].split('|')
    if 'ogni' in p:                         # TI-34: ogni carta dei tipi indicati sotto di lei nella catena
        bersagli = [v for v in pila[:pila.index(voce)] if not v.annullata and K.CARTE[v.cid].tipo in tipi]
    else:
        b = ctx.get('voce')
        bersagli = [b] if b is not None and K.CARTE[b.cid].tipo in tipi and not b.annullata else []
    for b in bersagli:
        S.annulla(g, b)
    if bersagli:
        return
    if 'TM' in tipi and ctx.get('togli_mappa') and g.mappa:
        _togli_mappa(g, e)
        return
    meno = [s for s in e.stati if s not in S.STATI_PIU]
    if 'togli_meno' in p and meno:          # CR-20: oppure togli i tuoi Stati (−)
        for s in meno:
            del e.stati[s]
        return
    rip = p.get('ripiego')
    if rip == 'fv':
        e.fv = True
    elif rip and isinstance(ctx.get('bers'), S.Eroe):
        S.dai_stato(g, ctx['bers'], rip)


def f_togli_mappa(g, e, c, p, ctx, pila, tiro, voce):
    """CR-15: togli la Mappa in gioco, poi il tesoro cambia Cripta; prendi lo Stato indicato."""
    if g.mappa:
        _togli_mappa(g, e)
    S.sposta_tesoro(g)
    S.dai_stato(g, e, p['s'])


def f_devia(g, e, c, p, ctx, pila, tiro, voce):
    """TI-36: una carta con un solo eroe come bersaglio passa all'eroe alla sinistra di quello; se no: Stato."""
    b = ctx.get('voce')
    if b is not None and not b.annullata and isinstance(b.ctx.get('bers'), S.Eroe):
        b.ctx['bers'] = S.giro(g, b.ctx['bers'].idx)[1]
        g.st['deviate'] += 1
        return
    S.dai_stato(g, e, p['s'])


def f_prendi_scarti(g, e, c, p, ctx, pila, tiro, voce):
    """TI-39 / CA-20: prendi in mano carte a scelta dagli scarti di un avversario (solo Equipaggiamenti con
    `equip`); se non ce n'è: ripiego."""
    n = p['n_sac'] if ctx.get('sacrificato') and 'n_sac' in p else p['n']
    ok = (lambda k: K.CARTE[k].equip) if 'equip' in p else (lambda k: True)
    pool = sorted(((x, k) for x in S.avversari(g, e) for k in x.scarti if ok(k)), key=lambda t: -K.valore(t[1]))
    if not pool:
        if p.get('ripiego') == 'fv':
            e.fv = True
        return
    x = pool[0][0]                          # «gli scarti di un avversario»: tutte dallo stesso
    for k in [k for y, k in pool if y is x][:n]:
        x.scarti.remove(k)
        S.ricevi(g, e, k)
        g.st['prese_dagli_scarti'] += 1


def f_ricambia(g, e, c, p, ctx, pila, tiro, voce):
    """CG-14 / TI-35: scarta fino a `max` carte (quelle di poco valore) e pescane altrettante."""
    junk = [k for k in e.mano if k != c.id and ia._val_mano(e, k) <= 2][:p.get('max', 10)]
    for k in junk:
        S.scarta(g, e, k)
    for _ in junk:
        S.pesca(g, e)
    if 'scontro_att' in p and _creatura_viva(g) and g.scontro.eroe is e:
        g.scontro.mod_att += p['scontro_att']
    for x in S.avversari(g, e):
        if 'accanto_stato' in p and g.plancia.accanto(e.pos, x.pos):
            S.dai_stato(g, x, p['accanto_stato'])
    if 'avv_uno' in p:                      # TI-35: ogni avversario può scartare 1 carta e pescarne 1
        for x in S.avversari(g, e):
            j = ia.da_scartare(g, x) if x.mano else None
            if j is not None and ia._val_mano(x, j) <= 2:
                S.scarta(g, x, j)
                S.pesca(g, x)


def f_tributo(g, e, c, p, ctx, pila, tiro, voce):
    """CG-20: ogni avversario ti dà 1 carta a sua scelta (la peggiore), oppure ne scarta n (con 2 Indizi: n2).
    L'IA dell'avversario scarta solo se ha almeno 6 carte."""
    n = p['n2'] if e.indizi >= 2 else p['n']
    for x in S.avversari(g, e):
        if not x.mano:
            continue
        if len(x.mano) >= 6:
            for _ in range(n):
                S.scarta(g, x, ia.da_scartare(g, x))
            g.st['scarti_mill'] += n
        else:
            k = ia.da_scartare(g, x)
            x.mano.remove(k)
            S.ricevi(g, e, k)
            g.st['furti'] += 1


F = {k[2:]: v for k, v in globals().items() if k.startswith('f_')}
