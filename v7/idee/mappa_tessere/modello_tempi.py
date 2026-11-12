"""Modello del tempo di montaggio della mappa (proposte del 12/11): costanti con le fonti e operatori per pezzo.
Lo usano tempo_setup.py (mappa 10×10, opzioni), fiori/fiori.py e 12x12/mappa12.py."""
import math


# ------------------------------------------------------------------ 3. modello del tempo
# (veloce, tipico, lento) in secondi. Fonti: KLM = Card, Moran & Newell, «The Psychology of Human-Computer Interaction»
# (1983), operatore M (atto mentale) = 1,35 s; Hick-Hyman: tempo di scelta = a + b·log2(n+1), b ≈ 0,15 s/bit (Hick 1952,
# Hyman 1953); Fitts: MT = a + b·log2(D/W + 1) con a ≈ 0,2 s, b ≈ 0,1-0,2 s/bit per movimenti della mano (MacKenzie
# 1992); MTM-1: raggiungere ~30 cm + afferrare + portare un oggetto piccolo ~1,5-2,5 s; fissazione dell'occhio in una
# scena 0,2-0,35 s (Rayner 1998). Le costanti «di tavolo» (presa di un cartoncino piatto, urti, controllo) sono stime
# [INFERENZA] tarate sul riferimento «Catan base: 5-8 minuti» (settlersboard.com/catan-setup-checklist, ~60 pezzi tra
# esagoni, cornice, gettoni e porti, cioè ~5-8 s a pezzo): il modello dà ~5 s a tile per la mappa di oggi.
COSTANTI = {
    'apertura':      ((10, 20, 40), 'tirare fuori i pezzi, aprire il foglio del preset: stima'),
    'sala':          ((3, 5, 8), 'posare la Sala del Tesoro (1 pezzo grande): come un settore'),
    'lettura':       ((0.8, 1.35, 2.2), 'leggere sul foglio la prossima casella e trovarla sul tavolo: operatore M del KLM (1,35 s)'),
    'lettura_muro':  ((1.5, 2.2, 3.5), 'un muro è una coppia di coordinate (lato tra due caselle): ~1,5 M'),
    'lettura_pezzo': ((1.0, 1.5, 2.5), 'pezzo grande con nome stampato («TM-03 nord»): leggere l’etichetta e lo slot'),
    'hick_a':        ((0.15, 0.2, 0.3), 'Hick-Hyman, costante: individuare una pila tra n pile ordinate per tipo'),
    'hick_b':        ((0.10, 0.15, 0.25), 'Hick-Hyman, s/bit'),
    'confronto':     ((0.35, 0.5, 0.8), 'confrontare un pezzo «unico» (tri-esagono, fiore) col disegno: 1-2 fissazioni (Rayner)'),
    'presa_tile':    ((0.6, 0.9, 1.3), 'raggiungere e afferrare un cartoncino da 25 mm piatto sul tavolo (MTM-1 + stima)'),
    'presa_medio':   ((0.5, 0.8, 1.1), 'pezzo da 50-80 mm: più facile da prendere'),
    'presa_grande':  ((0.6, 0.8, 1.2), 'pezzo da 130-265 mm: si prende col bordo, a due mani'),
    'presa_muro':    ((1.2, 2.0, 3.0), 'listello 14,5 × 3 mm piatto: va fatto scivolare o pizzicato'),
    'fitts_a':       ((0.15, 0.2, 0.3), 'Fitts, costante'),
    'fitts_b':       ((0.10, 0.15, 0.2), 'Fitts, s/bit (mano)'),
    'distanza':      ((300, 300, 300), 'mm dalla riserva al punto della mappa'),
    'toll_tile':     ((2.0, 2.0, 2.0), 'mm di tolleranza per accostare una tile ai vicini'),
    'toll_toppa':    ((3.0, 3.0, 3.0), 'mm: toppa su un esagono già stampato (bersaglio visibile)'),
    'toll_muro':     ((1.0, 1.0, 1.0), 'mm: listello sul lato tra due esagoni'),
    'posa_grande':   ((2.0, 3.5, 6.0), 'accostare un pezzo grande lungo il taglio a zig-zag, a due mani: stima'),
    'orienta_tile':  ((0.2, 0.3, 0.5), 'girare la tile con la scritta in basso'),
    'orienta_multi': ((0.5, 0.9, 1.5), 'scegliere 1 di 6 rotazioni di un pezzo da 3-7 esagoni confrontandolo col foglio'),
    'orienta_toppa': ((0.3, 0.6, 1.0), 'girare una toppa da 2-3 esagoni sulle caselle giuste'),
    'orienta_grande':((0.3, 0.5, 1.0), 'pezzo grande: il nome dice il verso'),
    'urti_tile':     ((0.1, 0.3, 0.6), 'tile leggere: ~10-20 % delle pose sposta un vicino, ~2-3 s per rimetterlo'),
    'urti_medio':    ((0.1, 0.25, 0.5), 'pezzi medi: un po’ meno'),
    'urti_toppa':    ((0.05, 0.15, 0.3), 'toppa sopra la plancia: non spinge i vicini'),
    'controllo':     ((0.3, 0.5, 0.8), 'controllo finale col foglio, per pezzo'),
    'errori':        ((0.005, 0.01, 0.03), 'probabilità di sbagliare un pezzo, trovato al controllo'),
    'correggi':      ((6, 8, 12), 's per correggere un errore'),
    'togli':         ((1.0, 1.5, 2.2), 'togliere un pezzo dalla mappa e rimetterlo nella sua pila (cambio di mappa)'),
    'gettone':       ((1.5, 2.0, 3.0), 'alzare una tessera Esplorazione da una «?» e rimetterla uguale (coperta/scoperta) sul pezzo nuovo'),
    'segnalini':     ((40, 55, 80), 'mescolare 20 tessere Esplorazione e metterne una su ogni «?»: uguale per tutte le opzioni'),
    'efficienza2':   ((0.8, 0.7, 0.6), 'seconda persona: frazione di lavoro utile (intralcio, un solo foglio) [INFERENZA]'),
}
PROFILI = ('veloce', 'tipico', 'lento')


def k(nome, p):
    return COSTANTI[nome][0][PROFILI.index(p)]


def fitts(p, toll):
    return k('fitts_a', p) + k('fitts_b', p) * math.log2(k('distanza', p) / k(toll, p) + 1)


def hick(p, n):
    return k('hick_a', p) + k('hick_b', p) * math.log2(n + 1)


def ricerca_unici(p, n):
    """pezzi tutti diversi sparsi sul tavolo: in media si guardano (n_rimasti+1)/2 candidati; media su n_rimasti=n..1."""
    return k('confronto', p) * (n + 3) / 4


def pezzo(tipo, p, pile=10, unici=0):
    """tempo di un pezzo: lettura + ricerca + presa + posa + orientamento + urti."""
    if tipo == 'tile':
        return k('lettura', p) + hick(p, pile) + k('presa_tile', p) + fitts(p, 'toll_tile') + k('orienta_tile', p) + k('urti_tile', p)
    if tipo == 'medio':   # tri-esagono, fiore: disegni quasi tutti unici
        return k('lettura', p) + ricerca_unici(p, unici) + k('presa_medio', p) + fitts(p, 'toll_tile') + k('orienta_multi', p) + k('urti_medio', p)
    if tipo == 'toppa':
        return k('lettura', p) + hick(p, pile) + k('presa_tile', p) + fitts(p, 'toll_toppa') + k('orienta_toppa', p) + k('urti_toppa', p)
    if tipo == 'grande':
        return k('lettura_pezzo', p) + hick(p, pile) + k('presa_grande', p) + k('posa_grande', p) + k('orienta_grande', p)
    if tipo == 'muro':
        return k('lettura_muro', p) + k('presa_muro', p) + fitts(p, 'toll_muro') + k('orienta_tile', p)
    raise ValueError(tipo)


def montaggio(voci, p, persone=1):
    """voci: [(tipo, quanti, kwargs)]. Ritorna i secondi per montare la mappa (senza le tessere Esplorazione)."""
    lavoro = sum(n * pezzo(t, p, **kw) for t, n, kw in voci)
    n = sum(n for _, n, _ in voci)
    lavoro += n * (k('controllo', p) + k('errori', p) * k('correggi', p))
    fisso = k('apertura', p) + k('sala', p)
    return fisso + (lavoro if persone == 1 else lavoro / (1 + k('efficienza2', p)))
