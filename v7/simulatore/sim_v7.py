#!/usr/bin/env python3
"""Simulatore del playtest v7 («Il Tesoro del Goblin»): Monte Carlo di partite intere su Spec_v7.md.

Uso (dalla radice del repository):
  python3 v7/simulatore/sim_v7.py --partite 2000 --seme 1            # base v7 (D18, D19)
  python3 v7/simulatore/sim_v7.py --partite 2000 --seme 1 --op1      # una opzione di R 7.12
Opzioni: --op1 --op2 --op5 (R 7.12); confronti con la v6: --ar-v6 (AR dei mostri v6), --indizio-lv (D6 <= LV);
montaggio: --preset (preset «Strettoie» invece del draft, D24); --mano-ia (l'IA sceglie le 5 carte iniziali di classe invece
della mano predefinita K.MANI_INIZIALI); varianti del §16: --dado-sommato (N6), --chi-tira-non-risponde (N1), --penalita-meno (N2).
--giocatori 2,3,4 (default: tutti e tre, come il simulatore v6), --processi N.
Solo libreria standard."""
import argparse
import os
import statistics
import sys
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carte as K          # noqa: E402
import regole as R         # noqa: E402

FLAG = ('op1', 'op2', 'op5', 'preset', 'ar_v6', 'indizio_lv', 'dado_sommato', 'chi_tira_non_risponde', 'penalita_meno',
        'mano_ia')


def una_partita(arg):
    n, seme, flag = arg
    g = R.Partita(n, seme, R.Opzioni(**flag))
    v = g.gioca()
    return {
        'n': n, 'finita': v is not None, 'round': g.round,
        'vincitore': (v.classe, v.direzione) if v else None,
        'eroi': [(e.classe, e.direzione) for e in g.eroi],
        'morti': sum(e.morti for e in g.eroi),
        'mano': g.mano_fine, 'pv': g.pv_fine, 'pl': g.pl_round, 'st': g.st, 'uso': g.uso, 'info': g.info,
        'giocate_eroe': sum(g.giocate_eroe.values()), 'max_indizi': g.max_indizi,
        'round_tesoro': g.round_tesoro,
    }


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0


def _media(xs):
    return statistics.mean(xs) if xs else 0.0


def rapporto_n(n, ris):
    r = []
    fin = [x for x in ris if x['finita']]
    rr = [x['round'] for x in fin]
    st = Counter()
    for x in ris:
        st.update(x['st'])
    N = len(ris)
    r.append(f"=== {n} giocatori ({N} partite) ===")
    r.append(f"Finite col custode: {len(fin) / N:.1%} (le altre in stallo a {R.ROUND_MAX} round)")
    if rr:
        r.append(f"Round: media {_media(rr):.1f}, mediana {statistics.median(rr)}, 10°-90° percentile "
                 f"{pct(rr, .1)}-{pct(rr, .9)}")
        fasce = [(1, 5), (6, 8), (9, 11), (12, 15), (16, 20), (21, R.ROUND_MAX)]
        r.append("Distribuzione dei round: " + ', '.join(
            f"{a}-{b} {sum(a <= y <= b for y in rr) / len(rr):.0%}" for a, b in fasce))
        rt = [x['round_tesoro'] for x in fin if x['round_tesoro']]
        r.append(f"Round del 3° Indizio (tesoro individuato): media {_media(rt):.1f}; tentativi sul custode per "
                 f"partita {st['tentativi_custode'] / N:.2f}")
    r.append(f"Movimento per turno: tirato {st['mov_tirato'] / st['turni']:.2f}, speso (passi fatti, con i costi) "
             f"{st['mov_speso'] / st['turni']:.2f}")
    pres, vit, presd, vitd = Counter(), Counter(), Counter(), Counter()
    for x in ris:
        for c, d in x['eroi']:
            pres[c] += 1
            presd[c + ' ' + d] += 1
        if x['vincitore']:
            vit[x['vincitore'][0]] += 1
            vitd[' '.join(x['vincitore'])] += 1
    r.append("Vittorie per classe (sulle partite in cui gioca; equo " + f"{1 / n:.0%}): " + ', '.join(
        f"{c} {vit[c] / pres[c]:.1%}" for c in K.CLASSI if pres[c]))
    r.append("Vittorie per direzione: " + ', '.join(
        f"{k} {vitd[k] / presd[k]:.1%}" for k in sorted(presd)))
    r.append(f"Sconfitte (morti) per partita: {_media([x['morti'] for x in ris]):.2f}; per Trappola "
             f"{st['morti_trappola'] / N:.2f}; oggetti persi col D6 {st['oggetti_persi'] / N:.2f}; "
             f"sacrifici {st['sacrifici'] / N:.2f}")
    mani = [m for x in ris for m in x['mano']]
    r.append(f"Mano alla propria Fine: media {_media(mani):.2f}; a 10 nel {sum(m >= 10 for m in mani) / len(mani):.1%} "
             f"dei turni; vuota nel {sum(m == 0 for m in mani) / len(mani):.1%}; scarti per la mano massima "
             f"{st['scarti_mano_max'] / N:.2f} a partita")
    pvs = [v for x in ris for v in x['pv']]
    r.append(f"PV rimasti (totali - Danni) alla propria Fine: media {_media(pvs):.2f}, mediana {statistics.median(pvs)}, "
             f"massimo {max(pvs)}; 6 o più nel {sum(v >= 6 for v in pvs) / len(pvs):.1%} dei turni")
    r.append(f"Bottino (mostri dei mazzetti 1-2 sconfitti, 1 carta tenuta su 3 rivelate): {st['loot'] / N:.2f} a partita; "
             f"riciclo degli scarti comuni {st['ricicli'] / N:.2f} a partita")
    giri = sum(x['round'] for x in ris)
    r.append(f"Carte giocate: {st['carte_giocate'] / giri:.2f} per round (tavolo), "
             f"{st['carte_giocate'] / giri / n:.2f} per giocatore per round; fuori turno "
             f"{st['carte_fuori_turno'] / max(1, st['carte_giocate']):.1%}; annullate {st['carte_annullate'] / N:.2f}, "
             f"bersaglio sparito {st['bersaglio_sparito'] / N:.2f} a partita")
    lun = max(len(x['pl']) for x in ris)
    pl = [_media([x['pl'][i] for x in ris if len(x['pl']) > i]) for i in range(min(lun, 15))]
    r.append("PL medio a fine round: " + ' '.join(f"R{i + 1} {v:.1f}" for i, v in enumerate(pl)))
    sc = st['scontri']
    r.append(f"Scontri per partita {sc / N:.1f}: mazzetto 1 {st['scontri_mazzetto_1'] / sc:.1%}, mazzetto 2 "
             f"{st['scontri_mazzetto_2'] / sc:.1%}, mazzetto 3 {st['scontri_mazzetto_3'] / sc:.1%}, custode "
             f"{st['scontri_custode'] / sc:.1%}; vinti {st['esito_vinto'] / sc:.1%}, persi {st['esito_perso'] / sc:.1%}, "
             f"fughe {st['esito_fuga'] / sc:.1%}, il mostro scappa dopo il 3° attacco {st['esito_fuga_mostro'] / sc:.1%} (fughe comprese quelle del mostro, NE-29: {st['mostri_scappati'] / sc:.1%})")
    r.append(f"Catene: aperte da carte {st['catene_carta'] / N:.1f} a partita, con risposte "
             f"{st['catene_carta_risposte'] / max(1, st['catene_carta']):.1%}; aperte da tiri {st['catene_tiro'] / N:.1f}, "
             f"con risposte {st['catene_tiro_risposte'] / max(1, st['catene_tiro']):.1%}; in tutto "
             f"{(st['catene_carta_risposte'] + st['catene_tiro_risposte']) / max(1, st['catene_carta'] + st['catene_tiro']):.1%}"
             f"; carte per catena con risposte {st['lunghezza_catene'] / max(1, st['catene_carta'] + st['catene_tiro_risposte']):.2f}")
    r.append(f"Indizi a partita: da mostri {st['indizi_mostri'] / N:.2f} (tiri {st['tiri_indizio'] / N:.1f}, negati "
             f"{st['indizi_negati'] / N:.2f}), da Duelli {st['indizi_duelli'] / N:.2f}, voce {st['indizi_voce'] / N:.2f}, "
             f"Sussurro {st['indizi_sussurro'] / N:.2f}")
    mi = [x['max_indizi'] for x in ris]
    r.append(f"Segnalini Indizio in gioco insieme: massimo {max(mi)}, 99° percentile {pct(mi, .99)}, media del "
             f"massimo {_media(mi):.1f}; partite oltre i 16 stampati {sum(m > 16 for m in mi) / N:.2%}")
    r.append(f"Duelli {st['duelli'] / N:.2f} a partita, rifiutati {st['duelli_rifiutati'] / N:.2f}; rifornimenti delle tessere "
             f"{st['rifornimenti'] / N:.2f} ({st['tessere_rifornite'] / N:.2f} tessere posate); tesoro spostato {st['tesoro_spostato'] / N:.2f}; Profezie "
             f"{st['profezie'] / N:.2f} (indovinate {st['profezie_indovinate'] / max(1, st['profezie']):.0%})")
    cambi = [x['st']['cambi_plancia'] + x['st']['cambi_plancia_base'] for x in ris]
    r.append(f"Cambi di plancia (R 8.12) {_media(cambi):.2f} a partita (verso una Mappa {st['cambi_plancia'] / N:.2f}, "
             f"ritorni al montaggio con TI-22/TI-33/CR-15 {st['cambi_plancia_base'] / N:.2f}); partite con almeno un cambio "
             f"{sum(c > 0 for c in cambi) / N:.0%}; scontri annullati {st['scontri_annullati'] / N:.2f} "
             f"(col custode {st['custode_annullato'] / N:.2f}), Duelli annullati {st['duelli_annullati'] / N:.2f}")
    r.append(f"Cripta (D24): {st['cripta_tirata'] / N:.2f} tiri a partita; spostata dal punto tirato (ostacolo o Partenza) "
             f"{st['cripta_spostata'] / max(1, st['cripta_tirata']):.0%}; caduta su una tessera (resta, la tessera va in riserva) "
             f"{st['cripta_su_tessera'] / N:.2f} a partita")
    r.append(f"Sconfitta con Indizio (D31): {(st['indizi_persi_riserva'] + st['indizi_persi_eroe']) / N:.2f} Indizi persi a partita "
             f"(alla riserva {st['indizi_persi_riserva'] / N:.2f}, a un eroe {st['indizi_persi_eroe'] / N:.2f}, ripresi dal vincitore "
             f"di un Duello {st['indizi_duelli'] / N:.2f}); Cripta tolta {st['cripta_tolta'] / N:.2f} volte a partita")
    r.append("Poteri usati per partita in cui la classe gioca: " + ', '.join(
        f"{c} {st['potere_' + c] / pres[c]:.2f}" for c in K.CLASSI if pres[c]))
    r.append(f"Giocate di carte con effetto non modellato (info): {st['info'] / N:.2f} a partita "
             f"({st['info'] / max(1, st['carte_giocate']):.1%} delle carte giocate)")
    return r, (_media(rr) if rr else None, len(fin) / N)


def rapporto_carte(tutte):
    uso, info = Counter(), Counter()
    for x in tutte:
        uso.update(x['uso'])
        info.update(x['info'])
    N = len(tutte)
    mai = [c for c in K.CARTE if not uso[c]]
    r = ["=== Carte (tutte le partite) ==="]
    r.append(f"Mai giocate ({len(mai)}): " + (', '.join(f"{c} {K.CARTE[c].nome}" for c in mai) or 'nessuna'))
    poco = sorted((c for c in K.CARTE if uso[c]), key=lambda c: uso[c])[:10]
    r.append("Meno giocate: " + ', '.join(f"{c} {uso[c] / N:.3f}" for c in poco))
    r.append("Più giocate (a partita): " + ', '.join(f"{c} {K.CARTE[c].nome} {v / N:.2f}" for c, v in uso.most_common(12)))
    if info:
        r.append("Effetti info (non modellati) per carta: " + ', '.join(f"{c} {v / N:.3f}" for c, v in info.most_common()))
    st = Counter()
    for x in tutte:
        st.update({k: v for k, v in x['st'].items() if k.startswith('mx_')})
    tasso = {m: st['mx_p:' + m] / st['mx_n:' + m] for m in K.MOSTRI if st['mx_n:' + m] >= 30}
    ordine = sorted(tasso, key=tasso.get)
    fmt = lambda m: f"{m} {K.MOSTRI[m].nome} (mz{K.MOSTRI[m].tier}) {tasso[m]:.0%}"   # noqa: E731
    r.append("=== Mostri: sconfitte dell'eroe per scontro (custode compreso, minimo 30 scontri) ===")
    r.append("Più letali: " + ', '.join(fmt(m) for m in reversed(ordine[-8:])))
    r.append("Più facili: " + ', '.join(fmt(m) for m in ordine[:8]))
    for t in (1, 2, 3):
        r.append(f"Mazzetto {t}: " + ', '.join(f"{m} {tasso[m]:.0%}" for m in K.MAZZETTI[t] if m in tasso))
    return r


def abilita_ignote():
    """Codici di abilita_mostri.csv che il motore non conosce (farebbero niente senza dirlo)."""
    qui = os.path.dirname(os.path.abspath(__file__))
    src = ''.join(open(os.path.join(qui, f), encoding='utf-8').read()
                  for f in ('scontro.py', 'mostri.py', 'catena.py', 'tiri.py', 'ia.py', 'ia_carte.py'))
    return sorted({f"{m}:{c}" for m, v in K.ABILITA.items() for c, _ in v if c != 'info' and f"'{c}'" not in src})


def verifica(cosa):
    """--verifica-mostri / --verifica-carte: id, nome, testo stampato e codice usato, per la revisione a occhio."""
    righe = []
    if cosa == 'mostri':
        for r in K._righe('carte_mostro.csv'):
            cod = ' + '.join(c + (f" {p}" if p else '') for c, p in K.ABILITA.get(r['id'], [('info', {})]))
            righe.append(f"{r['id']} [mz{r['mazzetto'][0]}] {r['nome']} | {r['abilita']} | => {cod}")
    else:
        for cid, c in K.CARTE.items():
            r = K.TESTI[cid]
            sit = f" / {r['testo_situazionale']}" if r['testo_situazionale'] else ''
            righe.append(f"{cid} {c.nome} | {r['testo']}{sit} | => {c.codice} {c.p or ''}")
    return righe


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--partite', type=int, default=2000, help='partite per ogni numero di giocatori')
    ap.add_argument('--seme', type=int, default=1)
    ap.add_argument('--giocatori', default='2,3,4')
    ap.add_argument('--processi', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--uscita')
    ap.add_argument('--verifica-mostri', action='store_true', help='stampa abilità dei mostri e codici, poi esce')
    ap.add_argument('--verifica-carte', action='store_true', help='stampa testi delle carte e codici, poi esce')
    for f in FLAG:
        ap.add_argument('--' + f.replace('_', '-'), action='store_true')
    a = ap.parse_args()
    if a.verifica_mostri or a.verifica_carte:
        print('\n'.join(verifica('mostri' if a.verifica_mostri else 'carte')))
        if abilita_ignote():
            print('Codici sconosciuti:', abilita_ignote())
        return
    flag = {f: getattr(a, f) for f in FLAG}
    nn = [int(x) for x in a.giocatori.split(',')]
    accese = [f for f in FLAG if flag[f]] or ['nessuna (base v7: D18 Indizio D6 <= LV+1, D19 AR x 0,75)']
    out = [f"Simulatore v7: {a.partite} partite per numero di giocatori, seme {a.seme}; opzioni: {', '.join(accese)}",
           f"Dati: {len(K.COMUNI)} comuni, {sum(len(v) for v in K.CARTE_CLASSE.values())} di classe, mostri per mazzetto "
           f"{ {t: len(v) for t, v in K.MAZZETTI.items()} } (custode pescato dal mazzetto 3 quando compare la Cripta), abilità dei mostri info: "
           f"{[m for m, v in K.ABILITA.items() if v[0][0] == 'info'] or 'nessuna'}; codici sconosciuti: "
           f"{abilita_ignote() or 'nessuno'}"]
    out.append("Mano iniziale: 5 carte di classe, nessuna comune; " + ("scelte dall'IA (--mano-ia)" if a.mano_ia else
               "predefinita per classe (K.MANI_INIZIALI)") + "; le altre 15 sono la pila di classe")
    if not K.AR_CSV_V7:
        out.append("ATTENZIONE: carte_mostro.csv ha ancora le AR v6 (8-11): il simulatore applica D19 da sé.")
    out.append('')
    sintesi, tutte = {}, []
    with Pool(a.processi) as pool:
        for n in nn:
            ris = pool.map(una_partita, [(n, a.seme * 1000003 + n * 100000 + i, flag) for i in range(a.partite)],
                           chunksize=50)
            righe, sintesi[n] = rapporto_n(n, ris)
            out += righe + ['']
            tutte += ris
    out += rapporto_carte(tutte) + ['']
    medie = [s[0] for s in sintesi.values() if s[0]]
    out.append("SINTESI round medi: " + ', '.join(f"{n}g {s[0]:.1f} (finite {s[1]:.0%})" for n, s in sintesi.items())
               + (f"; media {statistics.mean(medie):.1f} (v6: circa 10,6)" if medie else ''))
    testo = '\n'.join(out) + '\n'
    if a.uscita:
        with open(a.uscita, 'w', encoding='utf-8') as f:
            f.write(testo)
    sys.stdout.write(testo)


if __name__ == '__main__':
    main()
