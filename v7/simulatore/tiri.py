"""Tiri di dado (R 4.7, §5 ritiri D1, R 7.6 vantaggio) e Profezie dell'Oracolo (R 13.5)."""
import stato as S
import ia
import mostri as AB


class Tiro:
    """tipo: mov, iniz, colpo, danno, indizio, perdita, trappola, carta (tiro fatto mentre una carta si risolve).
    chi: Eroe o Creatura per cui si tira. basso=True se serve un numero basso (Indizio, Trappola: R 5.3)."""

    def __init__(self, g, chi, tipo, n=1, base=0, soglia=None, basso=False, vant=0, bersaglio=None):
        self.g, self.chi, self.tipo, self.n = g, chi, tipo, n
        self.base, self.soglia, self.basso, self.vant = base, soglia, basso, vant
        self.bersaglio = bersaglio
        self.mod = 0          # (+N)/(-N) giocati: restano anche se si ritira (R 5.5)
        self.rit = 0          # numero di ritiri: penalità n al ritiro n (R 5.1)
        self.pend = 0         # modificatori già in pila e non ancora risolti (stima per l'IA)
        self.annulla_danni = False
        self.riduzione = 0
        self.danni_extra = 0  # «(+N) Danni se il tiro colpisce» (CA-01, CG-05)
        self.no_indizio = False
        self.facce = self._lancia()
        if n:
            verifica_profezie(g, self)

    def _due(self):
        r = self.g.rng
        return [r.randint(1, 6) for _ in range(self.n)]

    def _lancia(self):
        f = self._due()
        if self.vant:
            f2 = self._due()
            if (sum(f2) > sum(f)) == (self.vant > 0) and sum(f2) != sum(f):
                f = f2
        return f

    def valore(self, extra=0):
        s = sum(self.facce)
        pen = self.rit
        if self.basso and not self.g.opz.penalita_meno:
            s += pen
        else:
            s -= pen
        if self.n == 1:
            s = max(1, s)     # R 5.4
        return s + self.base + self.mod + extra

    def ok(self, extra=0):
        if self.soglia is None:
            return None
        v = self.valore(extra)
        return v <= self.soglia if self.basso else v >= self.soglia

    def ritira(self, un_dado=False, alza=True):
        """Ritiro (D1). un_dado: si ritira 1 D6 (il più basso se si vuole alzare, il più alto altrimenti)."""
        if AB.vietato(self.g, 'nessun_ritiro'):     # NE-47 Timbro: il ritiro non avviene
            self.g.st['ritiri_vietati'] += 1
            return
        self.rit += 1
        self.g.st['ritiri'] += 1
        if un_dado and self.n > 1:
            i = self.facce.index(min(self.facce) if alza else max(self.facce))
            self.facce[i] = self.g.rng.randint(1, 6)
        else:
            self.facce = self._lancia()
        verifica_profezie(self.g, self)


def dado(g, espr, chi=None, extra_die=False):
    """Tiro fatto mentre una carta si risolve (R 4.9): «D6», «D6-1», «D6+2» o un numero fisso."""
    if isinstance(espr, int):
        return espr
    t = Tiro(g, chi, 'carta', 1)
    v = t.facce[0]
    if extra_die:                           # «dado in più»: tieni il migliore (N6) o somma (opzione)
        x = g.rng.randint(1, 6)
        v = v + x if g.opz.dado_sommato else max(v, x)
        g.st['dado_in_piu'] += 1
    e = espr.replace(' ', '').replace('−', '-')
    if e.startswith('D6+'):
        return v + int(e[3:])
    if e.startswith('D6-'):
        return max(1, v - int(e[3:]))
    return v


def d6_tra(g, ammessi):
    while True:
        r = g.rng.randint(1, 6)
        if r in ammessi:
            return r


# --- Profezie -----------------------------------------------------------------------------------------

def indovina(scelta, facce):
    s, n = sum(facce), len(facce)
    if isinstance(scelta, int):
        return scelta in facce          # su 2D6 basta un dado (N5)
    if scelta == 'Pari':
        return s % 2 == 0
    if scelta == 'Dispari':
        return s % 2 == 1
    if scelta == 'Alto':
        return s >= (4 if n == 1 else 8)
    return s <= (3 if n == 1 else 6)


def nuova_profezia(g, o, cid, tipo, chiave):
    g.profezie[o.idx] = {'cid': cid, 'tipo': tipo, 'chiave': chiave, 'scelta': ia.scegli_profezia(g, o, tipo)}
    g.st['profezie'] += 1


def verifica_profezie(g, t):
    if not g.profezie:
        return
    attive, g.profezie = g.profezie, {}
    for idx, pr in attive.items():
        o = g.eroi[idx]
        tipo_ok = (t.chi is o) == (pr['tipo'] == 'mio')
        if not tipo_ok:
            g.st['profezie_tipo_sbagliato'] += 1
            continue
        giusta = indovina(pr['scelta'], t.facce)
        grande = isinstance(pr['scelta'], int)
        if not giusta and pr['tipo'] == 'altrui' and pr['scelta'] in ('Alto', 'Basso') and o.ha('prof_largo'):
            giusta = sum(t.facce) in ((7,) if len(t.facce) == 2 else (3, 4))      # CO-18
        if not giusta and pr['tipo'] == 'mio':
            for c in o.equip():
                if c.id in o.usati:
                    continue
                if 'prof_riprova' in c.p:       # CO-14: il nuovo D6 vale solo per la Profezia (approssimato)
                    o.usati.add(c.id)
                    giusta = indovina(pr['scelta'], [g.rng.randint(1, 6)] + list(t.facce[1:]))
                    break
                if 'prof_paga' in c.p and o.pv > c.p['prof_paga'] + 1:     # CO-15: perdi N PV, solo premio piccolo
                    o.usati.add(c.id)
                    S.danneggia(g, o, c.p['prof_paga'])
                    giusta, grande = True, False
                    break
        if not giusta and o.classe == 'Oracolo' and o.potere:
            o.potere = False                # TC-04: una volta per partita
            g.st['potere_Oracolo'] += 1
            giusta = True
        if not giusta:
            if pr['tipo'] == 'altrui' and not pr.get('resta') and o.ha('prof_resta'):
                pr['resta'] = True          # CO-20: vale anche sul prossimo tiro altrui in questo turno
                g.profezie.setdefault(idx, pr)
            continue
        g.st['profezie_indovinate'] += 1
        _premio(g, o, pr['chiave'], grande, t)
        for c in o.equip():
            if pr['tipo'] == 'mio' and 'prof_cura' in c.p:
                S.cura(g, o, 1, carta=False)
            if pr['tipo'] == 'altrui' and 'prof_danno' in c.p:
                S.ferisci(g, t.chi, 1, o)
            if pr['tipo'] == 'altrui' and 'prof_scarta' in c.p:
                if isinstance(t.chi, S.Eroe):
                    _scarta_peggiore(g, t.chi, 1)
                else:
                    S.ferisci(g, t.chi, 1, o)
            if pr['tipo'] == 'altrui' and 'prof_stati' in c.p and c.id not in o.usati:     # CO-19
                o.usati.add(c.id)
                if isinstance(t.chi, S.Eroe):
                    S.togli_stati_piu(t.chi)
                elif g.scontro is not None and not g.scontro.finito:
                    g.scontro.mod_ar -= 1


def _scarta_peggiore(g, x, n):
    for _ in range(min(n, len(x.mano))):
        S.scarta(g, x, ia.da_scartare(g, x))
    g.st['scarti_mill'] += n


def _premio(g, o, k, grande, t):
    if k == 'mod':
        t.mod += 2 if grande else 1
    elif k == 'cura':
        S.cura(g, o, 2 if grande else 1)
        if grande:
            S.pesca(g, o)
    elif k == 'cura_fede':
        S.cura(g, o, 2 if grande else 1)
        if grande:
            S.dai_stato(g, o, 'Fede')
    elif k == 'riflesso':
        S.dai_stato(g, o, 'Riflesso')
        if grande:
            o.tmp['ar'] += 2
    elif k == 'danno_altrui':
        S.ferisci(g, t.chi, 2 if grande else 1, o)
        if grande and isinstance(t.chi, S.Eroe):
            S.togli_stati_piu(t.chi)
    elif k == 'scarta_altrui':
        if isinstance(t.chi, S.Eroe):
            _scarta_peggiore(g, t.chi, 2 if grande else 1)
            if grande and t.tipo == 'indizio':
                t.no_indizio = True
    elif k == 'danno_perdita_altrui':
        S.ferisci(g, t.chi, 3 if grande else 2, o)
        if grande and isinstance(t.chi, S.Eroe):
            S.perdita(g, t.chi)
    elif k == 'cura2_pila':                 # CO-11
        if grande:
            S.pesca(g, o, dalla_pila=True)
        else:
            S.cura(g, o, 2)
    elif k == 'ar_fede':                    # CO-12: Stato Fede; valore esatto anche (+2) AR in questo turno
        S.dai_stato(g, o, 'Fede')
        if grande:
            o.tmp['ar'] += 2
    elif k == 'dmg_turno':                  # CO-13
        o.tmp['dmg'] += 2 if grande else 1
        if grande:
            S.cura(g, o, 1)
    elif k == 'meno_altrui':                # CO-16
        t.mod -= 2 if grande else 1
        if grande:
            S.ferisci(g, t.chi, 1, o)
    elif k == 'scarta_fermo_altrui':        # CO-17
        if grande:
            S.ferisci(g, t.chi, 2, o)
            if isinstance(t.chi, S.Eroe):
                S.dai_stato(g, t.chi, 'Fermo')
        elif isinstance(t.chi, S.Eroe):
            _scarta_peggiore(g, t.chi, 1)
