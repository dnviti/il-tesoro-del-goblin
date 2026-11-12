"""IA delle carte: quali carte aprono una catena nei momenti M0-M6 (R 4.16) e quali rispondono (D4).
Punteggi semplici: nel proprio turno si gioca da 3 in su (da 2 alla Fine), fuori turno solo da 6 in su e con
almeno 1 carta del periodo ancora libera. Le risposte servono a: annullare, parare, ritirare, (+N)/(-N)."""
import carte as K
import mappa as M
import stato as S
import ia

DANNOSI = {'danno', 'stato_avv', 'malus', 'mill', 'maledizione', 'ruba', 'torna_partenza', 'ristom', 'scambia'}


def _minaccia(g, x):
    sc = g.scontro
    return (x.indizi >= 3 and g.mimi is not None and g.plancia.dist[x.pos][g.mimi] <= 7) or \
        (sc is not None and sc.custode and sc.eroe is x and not sc.finito)


def _junk(p, esclusa):
    altre = [c for c in p.mano if c != esclusa]
    return min(altre, key=lambda c: ia._val_mano(p, c)) if altre else None


def _punti(g, p, cid, mom, mio, mio_sc):
    c = K.CARTE[cid]
    q, k = c.p, c.codice
    sc = g.scontro
    att = g.eroi[g.attivo]
    ld = S.leader(g, p)
    custode_altrui = sc is not None and sc.custode and sc.eroe is not p and not sc.finito
    vivo = mio_sc and sc.nemico.pv > 0
    if k == 'equip':
        if not mio or mom not in ('M0', 'M1', 'M5', 'M6'):
            return None
        old = p.slot.get(c.slot)
        if old is None:
            return 10 + c.pl, {}
        return (8 + c.pl, {}) if K.CARTE[old].pl < c.pl else None
    if k == 'mappa':
        if custode_altrui:
            return 9, {}                    # R 8.12: il cambio di mappa chiude lo scontro col custode
        if not mio:
            if mom == 'M2' and att.pos == g.mimi and att.indizi >= 3:
                return 9, {}                # R 8.12: torna sulla Partenza prima del custode
            return None
        if p.indizi >= 3 and g.mimi or (sc is not None and not sc.finito):
            return None                     # R 8.12: il cambio chiuderebbe il proprio scontro senza ricompense
        v = 2
        if 'fv' in q and not p.fv:
            v = 4
        if 'pesca_tutti' in q or ('recupera' in q and p.scarti) or ('cura' in q and p.pv <= p.pvmax(g) - 3):
            v = 5
        if ld.indizi >= 3 and g.mimi:
            v = max(v, 6)                   # il tesoro cambia Cripta e il leader torna sulla Partenza
        return v, {}
    if k == 'annulla' and 'TM' in q['tipo'].split('|') and g.mappa and custode_altrui:
        return 9, {'togli_mappa': True}     # TI-22: i 3 fiori tornano come prima e lo scontro col custode finisce
    if k == 'danno':
        if vivo and mom in ('M3', 'M4'):
            ctx = {'bers': 'creatura'}
            j = _junk(p, cid)
            if 'scarta_dmg' in q and j and ia._val_mano(p, j) <= 2:
                ctx['scarta'] = j
            if 'sacrifica_pl2' in q and sc.boss:
                s = [s for s, x in p.slot.items() if K.CARTE[x].pl >= 2]
                if s:
                    ctx['sac'] = s[0]
            return 7, ctx
        if 'avv' in q:
            bers = [x for x in S.avversari(g, p) if g.plancia.accanto(p.pos, x.pos)]
            if bers:
                x = max(bers, key=lambda x: x.indizi)
                if _minaccia(g, x):
                    return 7, {'bers': x}
                if mio and mom == 'M6' and (x.indizi >= 2 or x.pv <= 2):
                    return 4, {'bers': x}
        return None
    if k == 'buff':
        if vivo and mom == 'M4' and p.tmp['att'] < 2:
            if 'perdita_fine' in q:
                return (8, {}) if sc.boss or sc.nemico.tier >= 2 else None
            ctx = {}
            if 'att_sac' in q and sc.custode and 'Elmo' in p.slot:
                ctx['sac'] = 'Elmo'
            return 6, ctx
        return None
    if k == 'malus':
        if vivo and mom in ('M3', 'M4') and not ('non_boss' in q and sc.boss):
            return (8 if sc.boss else 6), {'bers': 'creatura'}
        if custode_altrui and mom in ('M3', 'M4'):
            return 8, {'bers': sc.eroe}
        if mio and mom == 'M6' and ld.indizi >= 2:
            return 3, {'bers': ld}
        return None
    if k == 'ristom':
        j = _junk(p, cid)
        if custode_altrui and mom in ('M3', 'M4') and j:
            return 9, {'bers': sc.eroe, 'scarta': j}
        return None
    if k == 'velo':
        if vivo and mom == 'M4' and 'parkour' not in q and not sc.boss and ia.fuggire(g, p, sc):
            return 7, {'fuga': True}
        if mio and mom == 'M1' and p.indizi >= 3 and g.mimi and g.plancia.dist[p.pos][g.mimi] > 3 + p.stat(g, 'mov'):
            return 4, {}
        return None
    if k == 'stato':
        s = q['s']
        if s == 'Sussurro':
            if mio and mom == 'M2' and g.tessere.get(p.pos) in ('rossa', 'blu', 'scoperta'):
                return 5, {}
            return (3, {}) if mio and mom == 'M6' else None
        if vivo and mom == 'M3' and s not in p.stati:
            return 6, {}
        return (4, {}) if mio and mom == 'M6' and s not in p.stati else None
    if k == 'stato_avv':
        if 'schiocco' in q and vivo and mom == 'M4' and not sc.custode and ia.fuggire(g, p, sc):
            return 7, {'bers': ld}          # TI-41: il mostro sparisce invece della fuga
        if 'tutti' in q:
            return (3, {}) if mio and mom == 'M6' else None
        if not mio and mom in ('M0', 'M1') and att is not p and _minaccia(g, att) and q['s'] == 'Rallentato':
            return 8, {'bers': att}
        if mio and mom == 'M6' and ld.indizi >= 2:
            return (4 if ld.indizi >= 3 else 3), {'bers': ld}
        return None
    if k == 'fv':
        return (4, {}) if mio and not p.fv else None
    if k == 'cura':
        if p.pv <= 2 or (mio_sc and p.pv <= 3):
            return 7, {}
        return (5, {}) if mio and p.pv <= p.pvmax(g) - 2 else None
    if k == 'recupera':
        buone = [x for x in p.scarti if K.valore(x) >= 4]
        if not mio or not buone or len(p.mano) > 8:
            return None
        if 'costo_scarta' in q:
            j = _junk(p, cid)
            return (3, {'scarta': j}) if j and ia._val_mano(p, j) <= 2 else None
        return 3, {}
    if k == 'nani':
        if vivo:
            return 4, {}
        return (3, {}) if mio and not p.fv else None
    if k == 'speziale':
        return (3, {}) if mio and mom == 'M1' else None
    if k in ('mill', 'maledizione', 'ruba', 'scambia', 'tempo_scaduto'):
        if not mio or mom != 'M6':
            return None
        if k == 'mill' and 'indizi3' in q:
            return (7 if ld.indizi >= 3 else 3), {'bers': ld}
        if k == 'scambia' or k == 'tempo_scaduto':
            return (2, {'bers': max(S.avversari(g, p), key=lambda x: len(x.mano))}) \
                if sum(1 for x in p.mano if ia._val_mano(p, x) <= 3) >= 2 else None
        bers = max(S.avversari(g, p), key=lambda x: (x.indizi >= 2, len(x.mano)))
        return (3, {'bers': bers}) if bers.mano else None
    if k == 'vera_volonta':
        return (4, {}) if mio and len(p.mano) <= 8 else None
    if k == 'perdita_tutti':
        alto = max(x.pl() for x in S.avversari(g, p))
        return (4, {}) if mio and p.pl() <= 1 and alto >= 4 else None
    if k == 'torna_partenza':
        bers = [x for x in S.avversari(g, p) if _minaccia(g, x) and x.pos != x.partenza]
        return (7, {'bers': bers[0]}) if bers and not (mio_sc or (sc and sc.eroe is p)) else None
    if k == 'prendi_scarti':
        ok = [c for x in S.avversari(g, p) for c in x.scarti if K.CARTE[c].equip or 'equip' not in q]
        return (4, {}) if mio and mom in ('M1', 'M6') and ok and max(map(K.valore, ok)) >= 5 else None
    if k == 'ricambia':
        if 'scontro_att' in q and vivo and mom == 'M3':
            return 6, {}
        junk = [c for c in p.mano if c != cid and ia._val_mano(p, c) <= 2]
        return (3, {}) if mio and mom in ('M1', 'M6') and len(junk) >= 2 else None
    if k == 'tributo':
        return (4, {}) if mio and mom == 'M6' and sum(len(x.mano) for x in S.avversari(g, p)) >= 3 else None
    if k == 'togli_mappa':
        if custode_altrui and g.mappa:
            return 9, {}
        return (5 if g.mappa and ld.indizi >= 3 else 2, {}) if mio and mom == 'M6' and g.mimi else None
    if k == 'dirigibile':
        if vivo and mom in ('M3', 'M4') and p.pv >= 6:
            return 5, {}
        return (3, {}) if mio and mom == 'M6' and p.pv >= 5 and ld.pv <= 3 else None
    if k == 'passa':
        junk = [c for c in p.mano if c != cid and ia._val_mano(p, c) <= 2]
        return (2, {}) if mio and mom == 'M6' and len(junk) >= 2 else None
    if k == 'gamba':
        return (3, {}) if mio and mom == 'M1' else None
    if k == 'pietraluce':
        return (3, {'bers': ld}) if mio and mom == 'M6' and ld.indizi >= 2 else None
    if k in ('amisal', 'scry_imp'):
        return (3, {}) if mio and mom == 'M1' else None
    if mio and mom == 'M6' and len(p.mano) >= 8:     # risposte giocate per il ripiego
        rip = q.get('ripiego')
        if rip == 'fv' and not p.fv:
            return 2, {}
        if rip == 'Fede':
            return 2, {}
        if rip in ('Rallentato', 'Silenzio'):
            return 2, {'bers': ld}
    return None


def apri(g, p, mom):
    att = g.eroi[g.attivo]
    mio = att is p
    sc = g.scontro
    mio_sc = sc is not None and not sc.finito and sc.eroe is p and not sc.duello
    if mio:
        if mom in ('M0', 'M1', 'M2') and p.giocate >= 1:
            return None
        if mom in ('M3', 'M4') and p.giocate >= 1 and any(
                K.CARTE[c].codice in ('mod_tiro', 'ritira', 'parata', 'riduzione') for c in p.mano):
            return None
        soglia = 2 if mom == 'M6' else 3
    else:
        if p.giocate >= 1:
            return None
        soglia = 6
    best = None
    for cid in dict.fromkeys(p.mano):        # ordine stabile: con set() il seme non bastava (hash casuale)
        c = K.CARTE[cid]
        if c.tipo == 'TI' and 'Silenzio' in p.stati:
            continue
        r = _punti(g, p, cid, mom, mio, mio_sc)
        if r and g.round == 1 and ('tutti' in c.p or (isinstance(r[1].get('bers'), S.Eroe) and r[1]['bers'] is not p)):
            continue                         # primo giro: nessuna carta contro un avversario
        if r and r[0] >= soglia and (best is None or r[0] > best[0]):
            best = (r[0], cid, r[1])
    return (best[1], best[2]) if best else None


# --- risposte ------------------------------------------------------------------------------------------

def _in_mano(p, pred):
    for cid in p.mano:
        c = K.CARTE[cid]
        if (c.tipo != 'TI' or 'Silenzio' not in p.stati) and not c.equip and pred(c):
            return cid
    return None


def _dannosa(g, p, v):
    c = K.CARTE[v.cid]
    if v.eroe is p or v.annullata:
        return False
    if c.codice in DANNOSI and (v.ctx.get('bers') is p or 'tutti' in c.p):
        return True
    if c.tipo == 'TM' and p.indizi >= 3 and g.mimi is not None:
        return True
    sc = g.scontro
    return sc is not None and sc.custode and sc.eroe is v.eroe and c.codice in ('buff', 'danno', 'malus')


def _risposta_carta(g, p, pila):
    for v in reversed(pila):
        if not _dannosa(g, p, v):
            continue
        tipo = K.CARTE[v.cid].tipo
        cid = _in_mano(p, lambda c: c.codice == 'annulla' and tipo in c.p['tipo'].split('|'))
        if cid:
            return cid, {'voce': v}
        if tipo == 'TI' and v.ctx.get('bers') is p:
            for s, x in list(p.slot.items()):          # CG-17 / CS-16: sacrifica e annulla l'Incanto
                if 'sac_annulla_ti' in K.CARTE[x].p:
                    S.sacrifica(g, p, s)
                    S.annulla(g, v)
                    S.dai_stato(g, v.eroe, 'Silenzio')
                    g.st['annullate_da_equip'] += 1
                    return None
        cid = _in_mano(p, lambda c: c.codice == 'devia')
        if cid and v.ctx.get('bers') is p:
            return cid, {'voce': v}
        if K.CARTE[v.cid].codice == 'danno':
            cid = _in_mano(p, lambda c: c.codice == 'parata' and c.p['tipo'] == 'trappola_incanto')
            if cid:
                return cid, {'voce': v}
        if tipo == 'TI':
            cid = _in_mano(p, lambda c: c.codice == 'stato_avv' and 'risposta_fv' in c.p)
            if cid:
                return cid, {'bers': v.eroe}
    return None


def _mod(p, t, verso, deficit):
    """Carta (+N)/(-N) che basta a coprire il deficit. verso +1 alza, -1 abbassa."""
    for cid in sorted(p.mano, key=K.valore):
        c = K.CARTE[cid]
        if c.codice != 'mod_tiro' or (c.tipo == 'TI' and 'Silenzio' in p.stati):
            continue
        if 'qualsiasi' in c.p:
            if c.p['n'] >= deficit:
                return cid, {'segno': verso}, verso * c.p['n']
        elif t.chi is p and verso > 0:
            if c.p['n'] >= deficit:
                return cid, {}, c.p['n']
            if 'n_sac' in c.p and c.p['n_sac'] >= deficit and c.p['sacrifica'] in p.slot:
                return cid, {'sac': c.p['sacrifica']}, c.p['n_sac']
            if 'scarta_n' in c.p and c.p['scarta_n'] >= deficit and _junk(p, cid):
                return cid, {'scarta': _junk(p, cid)}, c.p['scarta_n']
    return None


def _ritiro(p, t, mio):
    sc = t.g.scontro
    if sc is not None and sc.ab('nessun_ritiro') is not None:
        return None
    def ok(c):
        if c.codice != 'ritira':
            return False
        return ('proprio' in c.p) == mio or 'qualsiasi' in c.p
    cid = _in_mano(p, ok)
    if cid is None:
        return None
    return cid, {'alza': mio != t.basso}


def rispondi(g, p, pila, t):
    if p.giocate >= g.opz.limite:
        return None
    mio_turno = g.eroi[g.attivo] is p
    if t is None:
        return _risposta_carta(g, p, pila) if (mio_turno or p.giocate == 0) else None
    if t.soglia is None and t.tipo not in ('danno', 'trappola'):
        return None
    mio = t.chi is p
    val = t.valore() + t.pend
    r = None
    if mio and t.soglia is not None and t.tipo in ('colpo', 'indizio'):
        deficit = (t.soglia - val) if not t.basso else (val - t.soglia)
        if deficit <= 0:
            return None
        m = _mod(p, t, -1 if t.basso else 1, deficit)
        if m:
            t.pend += m[2]
            return m[0], m[1]
        if t.tipo == 'colpo':
            pr = ia.P2D6[max(-10, min(19, t.soglia - (t.base + t.mod - t.rit - 1)))]
        else:
            pr = max(0, t.soglia - t.rit - 1) / 6
        return _ritiro(p, t, True) if pr >= 0.3 else None
    if mio and t.tipo == 'trappola':
        if val >= 2 or val >= p.pv:
            cid = _in_mano(p, lambda c: c.codice == 'parata' and c.p['tipo'] == 'trappola_incanto')
            return (cid, {}) if cid else None
        return None
    if mio:
        return None
    critico = t.bersaglio is p or (isinstance(t.chi, S.Eroe) and t.chi.indizi >= 2) or \
        (g.scontro is not None and g.scontro.custode)
    if not (mio_turno or p.giocate == 0 or critico):
        return None
    if t.tipo == 'danno' and t.bersaglio is p:
        if val >= 2:
            cid = _in_mano(p, lambda c: c.codice == 'parata' and c.p['tipo'] == 'attacco')
            if cid:
                ctx = {}
                if val >= p.pv and len(p.slot) >= 2:
                    ctx['sac'] = min(p.slot, key=lambda s: K.CARTE[p.slot[s]].pl)
                return cid, ctx
            cid = _in_mano(p, lambda c: c.codice == 'riduzione')
            if cid and val >= p.pv:
                return cid, {}
        return None
    if t.soglia is None:
        return None
    contro = t.bersaglio is p or (isinstance(t.chi, S.Eroe) and (t.tipo == 'indizio' or _minaccia(g, t.chi)))
    if contro and t.tipo in ('colpo', 'indizio'):
        ok = val <= t.soglia if t.basso else val >= t.soglia
        if not ok:
            return None
        if t.tipo == 'indizio':
            cid = _in_mano(p, lambda c: 'nega_indizio' in c.p)
            if cid:
                return cid, {'segno': 1}
        margine = (t.soglia - val + 1) if t.basso else (val - t.soglia + 1)
        m = _mod(p, t, 1 if t.basso else -1, margine)
        if m:
            t.pend += m[2]
            return m[0], m[1]
        return _ritiro(p, t, False)
    sc = g.scontro
    if sc is not None and sc.custode and t.chi is sc.nemico and sc.eroe is not p and t.tipo == 'colpo':
        if val < t.soglia:                  # aiuta il custode contro chi sta per vincere
            m = _mod(p, t, 1, t.soglia - val)
            if m:
                t.pend += m[2]
                return m[0], m[1]
    return r
