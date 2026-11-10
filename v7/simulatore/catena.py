"""Catene (D4, D9): giro delle risposte in senso orario, pila LIFO, tiri che aprono catene, momenti M0-M6."""
import carte as K
import stato as S
import effetti
import ia
import mostri as AB


class Voce:
    __slots__ = ('eroe', 'cid', 'ctx', 'annullata')

    def __init__(self, eroe, cid, ctx):
        self.eroe, self.cid, self.ctx, self.annullata = eroe, cid, ctx, False


def puo_giocare(g, e, cid, risposta):
    """Limite D9 (2 per periodo; 1 per catena è controllato dal chiamante), Silenzio, Equipaggiamenti (R 4.2)."""
    c = K.CARTE[cid]
    if e.giocate >= g.opz.limite:
        return False
    if c.tipo == 'TI' and ('Silenzio' in e.stati or AB.vietato(g, 'nessun_incanto')):
        return False
    if c.equip:
        return not risposta and g.eroi[g.attivo] is e and not e.equip_turno and not g.in_catena
    return True


def _gioca(g, e, cid, ctx, pila):
    e.mano.remove(cid)
    e.giocate += 1
    c = K.CARTE[cid]
    if c.equip:
        e.equip_turno = True
    else:
        e.zona.append(cid)
    g.uso[cid] += 1
    g.st['carte_giocate'] += 1
    g.giocate_eroe[e.idx] += 1
    if g.eroi[g.attivo] is not e:
        g.st['carte_fuori_turno'] += 1
    effetti.paga(g, e, cid, ctx)
    pila.append(Voce(e, cid, ctx))


def _risposte(g, ordine, pila, tiro):
    giocato = {v.eroe.idx for v in pila}
    for p in ordine:
        if p.idx in giocato or g.finita:
            continue
        r = ia.rispondi(g, p, pila, tiro)
        if r and r[0] in p.mano and puo_giocare(g, p, r[0], True):
            _gioca(g, p, r[0], r[1], pila)
            giocato.add(p.idx)
            g.st['risposte'] += 1


def _risolvi(g, pila, tiro):
    g.in_catena = True
    for v in reversed(pila):            # R 4.8: LIFO
        if v.annullata:
            g.st['carte_annullate'] += 1
            continue
        effetti.risolvi(g, v, pila, tiro)
    g.in_catena = False
    if tiro is not None:
        tiro.pend = 0


def catena_carta(g, e, cid, ctx):
    """Apre una catena con una carta: rispondono gli altri, da sinistra di chi l'ha aperta (R 4.6)."""
    pila = []
    _gioca(g, e, cid, ctx, pila)
    g.st['catene_carta'] += 1
    g.in_risposte = True
    _risposte(g, S.giro(g, e.idx, False), pila, None)
    g.in_risposte = False
    if len(pila) > 1:
        g.st['catene_carta_risposte'] += 1
    g.st['lunghezza_catene'] += len(pila)
    _risolvi(g, pila, None)


def catena_tiro(g, t):
    """R 4.7: il tiro apre una catena; chi tira risponde per primo (N1), per una creatura comincia chi ha il turno.
    Durante la risoluzione di un'altra pila il tiro non apre catene (R 4.9). Poi gli effetti automatici."""
    if not (g.in_catena or g.in_risposte or g.finita):
        if isinstance(t.chi, S.Eroe):
            ordine = S.giro(g, t.chi.idx, not g.opz.chi_tira_non_risponde)
        else:
            ordine = S.giro(g, g.attivo, True)
        pila = []
        g.st['catene_tiro'] += 1
        g.in_risposte = True
        _risposte(g, ordine, pila, t)
        g.in_risposte = False
        if pila:
            g.st['catene_tiro_risposte'] += 1
            g.st['lunghezza_catene'] += len(pila)
            _risolvi(g, pila, t)
    ia.automatici(g, t)
    return t


def momento(g, nome):
    """R 4.16: si offre di aprire una catena a chi ha il turno, poi in senso orario; dopo ogni catena si
    ricomincia da chi ha il turno; il momento finisce quando tutti passano."""
    for p in S.giro(g, g.attivo, True):
        ia.poteri(g, p, nome)
    while not (g.finita or (g.turno_finito and nome != 'M6')):
        for p in S.giro(g, g.attivo, True):
            if p.giocate >= g.opz.limite:
                continue
            s = ia.apri(g, p, nome)
            if s and s[0] in p.mano and puo_giocare(g, p, s[0], False):
                catena_carta(g, p, s[0], s[1])
                break
        else:
            return
