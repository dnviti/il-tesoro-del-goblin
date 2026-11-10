"""Abilità dei mostri (testo della colonna `abilita` di carte_mostro.csv, codici in abilita_mostri.csv).
Ogni funzione è un punto d'aggancio chiamato da scontro.py (o da catena/tiri per i divieti)."""
import carte as K
import stato as S
import ia


def vietato(g, codice):
    """NE-47 nessun ritiro, NE-49 nessun Incanto: valgono per tutti finché lo scontro è aperto."""
    sc = g.scontro
    return sc is not None and not sc.finito and sc.ab(codice) is not None


def chi_tira_per_lui(g, e):
    """R 7.2: il giocatore alla destra dell'eroe (in 2 giocatori l'avversario)."""
    return g.eroi[(e.idx - 1) % len(g.eroi)]


def inizio(g, sc):
    """Abilità d'inizio scontro. Ritorna True se il mostro è sconfitto subito senza Indizio (NE-40)."""
    e, m = sc.eroe, sc.nemico
    el = sc.ab('elemosina')
    if el is not None:
        junk = [c for c in e.mano if ia._val_mano(e, c) <= 2]
        if len(junk) >= el['n']:
            for c in junk[:el['n']]:
                S.scarta(g, e, c)
            g.st['elemosine'] += 1
            return True
    if sc.ab('inizio_togli_piu') is not None:
        S.togli_stati_piu(e)
    pr = sc.ab('pedaggio_reale')
    if pr is not None:
        if e.mano and ia._val_mano(e, ia.da_scartare(g, e)) <= 4:
            S.scarta(g, e, ia.da_scartare(g, e))
        else:
            sc.mod_att += pr['n']
    if sc.ab('televoto') is not None:
        d = g.rng.randint(1, 6)
        if d <= 4:
            S.danneggia(g, e, 2 if d <= 2 else 1, m)
        else:
            danni_creatura(g, sc, 2, attacco=False)
    return False


def att(g, sc, a):
    m, e = sc.nemico, sc.eroe
    mp = sc.ab('meta_pv_att')
    if mp is not None and m.pv * 2 <= m.pv0:
        a += mp['n']
    co = sc.ab('coro')
    if co is not None:
        altre = sum(1 for h, t in g.tessere.items() if t == 'scoperta' and h != e.pos)
        a += min(co['max'], altre)
    pi = sc.ab('picchiata')
    if pi is not None and sc.eroe_primo and sc.attacchi_mostro == 1:
        a += pi['n']
    if sc.ab('imitazione') is not None:
        a = max(a, e.stat(g, 'att'))
    return a


def ar(g, sc, a):
    gu = sc.ab('guscio')
    if gu is not None and sc.nemico.pv >= sc.nemico.pv0:
        a += gu['n']
    return a


def vant_eroe(sc, primo):
    v = 0
    if primo and sc.ab('svant_primo') is not None:
        v -= 1
    if primo and sc.ab('letargo') is not None:
        v += 1
    return v


def eroe_manca(g, sc, x, primo):
    if sc.ab('manca_stato') is not None:
        S.dai_stato(g, x, sc.ab('manca_stato')['s'])
    if sc.ab('manca_danno') is not None:
        S.danneggia(g, x, sc.ab('manca_danno')['n'], sc.nemico)
    if primo and sc.ab('letargo') is not None:
        sc.mod_att += sc.ab('letargo')['n']


def danni_creatura(g, sc, n, attacco=True, diretto=False):
    """Danni alla creatura: Nebbia, Coriaceo, Si ricompone, Gambe in spalla, Svegliato male, Botto finale."""
    m = sc.nemico
    if attacco and sc.ab('nebbia') is not None and not sc.nebbia_usata and n > 0:
        sc.nebbia_usata = True
        g.st['nebbia'] += 1
        return
    if sc.ab('coriaceo') is not None and not diretto and n > 0:
        n = max(1, n - sc.ab('coriaceo')['n'])
    prima = m.pv
    m.pv -= n
    sc.ferita = sc.ferita or n > 0
    if m.pv <= 0 and sc.ab('ricompone') is not None and not sc.ricomposto and not diretto:
        sc.ricomposto = True
        m.pv = sc.ab('ricompone')['n']
    if m.pv <= 0:
        bo = sc.ab('botto')
        if bo is not None and sc.eroe.pv > 1:
            sc.eroe.pv = max(1, sc.eroe.pv - bo['n'])
        return
    if sc.ab('scappa') is not None and m.pv <= sc.ab('scappa')['n'] < prima:
        sc.scappato = sc.finito = True
        g.st['mostri_scappati'] += 1
    if sc.ab('svegliato') is not None and not sc.svegliato and m.pv * 2 <= m.pv0 < prima * 2:
        sc.svegliato = True
        sc.attacco_extra = True


def danno_extra(g, sc, faccia):
    """Danni in più del colpo del mostro (prima delle riduzioni)."""
    e = sc.eroe
    x = 0
    mi = sc.ab('mira')
    if mi is not None and faccia <= 2:
        x += mi['n'] - faccia
    x += (sc.ab('monologo') or {}).get('n', 0)
    if sc.colpi_mostro == 1:
        x += (sc.ab('primo_colpo_danni') or {}).get('n', 0)
        ga = sc.ab('galante')
        if ga is not None:
            peggiore = ia.da_scartare(g, e) if e.mano else None
            if peggiore and (ia._val_mano(e, peggiore) <= 3 or e.pv <= 3 + ga['n']):
                S.scarta(g, e, peggiore)
            else:
                x += ga['n']
    return x


def dopo_colpo(g, sc, d, sei):
    """L'eroe è stato colpito e non è sconfitto."""
    m, e = sc.nemico, sc.eroe
    if d and sc.ab('succhia') is not None:
        m.pv = min(m.pv0, m.pv + 1)
    if sc.ab('colpo_stato') is not None:
        S.dai_stato(g, e, sc.ab('colpo_stato')['s'])
    if sc.colpi_mostro == 1:
        ps = sc.ab('primo_colpo_slot')
        if ps is not None and ps['s'] in e.slot and 'mai_perso' not in K.CARTE[e.slot[ps['s']]].p:
            S.lascia_slot(g, e, ps['s'])
            g.st['elmi_collezionati'] += 1
        if sc.ab('primo_colpo_togli_fv') is not None:
            e.fv = False
        if sc.ab('primo_colpo_ruba') is not None:
            S.ruba(g, chi_tira_per_lui(g, e), e)
        if sc.ab('primo_colpo_stato') is not None:
            S.dai_stato(g, e, sc.ab('primo_colpo_stato')['s'])
    if sei and sc.ab('sei_stato') is not None:
        S.dai_stato(g, e, sc.ab('sei_stato')['s'])
    if sei and sc.ab('sei_perdita') is not None:
        S.perdita(g, e)


def sconfigge(g, sc, e):
    """Il mostro ha sconfitto l'eroe (dopo la sconfitta normale)."""
    if sc.ab('sconfigge_stato') is not None:
        S.dai_stato(g, e, sc.ab('sconfigge_stato')['s'])
    if sc.ab('sconfigge_scarta') is not None and e.mano:
        S.scarta(g, e, g.rng.choice(e.mano))
    if sc.ab('sconfigge_stato_avv') is not None:
        S.dai_stato(g, chi_tira_per_lui(g, e), sc.ab('sconfigge_stato_avv')['s'])
    if sc.ab('sconfigge_tesoro') is not None and not S.sposta_tesoro(g):
        g.st['info_mostri'] += 1        # «ogni avversario guarda la tua mano»


def fuga(g, sc, e):
    fs = sc.ab('fuga_scarta')
    if fs is not None:
        for _ in range(min(fs['n'], len(e.mano))):
            S.scarta(g, e, ia.da_scartare(g, e))
    if sc.ab('permaloso') is not None:
        g.in_cima = True


def fine(g, sc, e, esito):
    if esito != 'perso' and sc.colpito and sc.ab('morso') is not None and e.pv > 1:
        e.pv -= sc.ab('morso')['n']
    if sc.ab('fine_stato') is not None:
        S.dai_stato(g, e, sc.ab('fine_stato')['s'])


def tira_indizio(g, sc, e):
    """NE-38 Marca da bollo: per tirare si scarta 1 carta (l'IA lo fa se ha una carta)."""
    mb = sc.ab('marca_bollo')
    if mb is None:
        return True
    if len(e.mano) < mb['n']:
        return False
    for _ in range(mb['n']):
        S.scarta(g, e, ia.da_scartare(g, e))
    return True
