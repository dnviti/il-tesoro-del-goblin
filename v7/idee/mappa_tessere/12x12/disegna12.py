#!/usr/bin/env python3
"""Mock-up della mappa 12×12 a fiori con il disegno del kit (v7/stampa/sorgenti/componenti_gen/fiori12.py) e i dati di
mappa12.py: SVG in mm 1:1 e PNG (ImageMagick) in questa cartella.

Uso (dalla radice del repo):  python3 v7/idee/mappa_tessere/12x12/disegna12.py

  m12_pezzi.svg/.png       i 14 fiori, faccia A sopra e faccia B sotto, con id e freccia;
  m12_draft.svg/.png       una mappa da draft casuale (seme fisso): base, 14 fiori, 24 «?» con la tessera, Cripta tirata;
  m12_strettoie.svg/.png   il preset «Strettoie», pezzi staccati di qualche mm.
Terreno dalle 19:01: libero (prato, mattonato, pavimento, sentiero, guado, ponte), accidentato (acqua, «+1»), ostacoli
(bosco, rocce, case: scuri e col bordo netto).
"""
import math
import os
import random
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.normpath(os.path.join(QUI, '..', '..', '..', 'stampa', 'sorgenti', 'componenti_gen')))
import mappa12 as M  # noqa: E402
import fiori12 as F  # noqa: E402

FASCIA = 5.5
PLATE, BROWN, BRASS = F.PLATE, F.BROWN, F.BRASS


def faccia_kit(i, lato):
    f = M.FIORI[i][lato]
    return {'nome': f['nome'], 'celle': {0: f['centro'], **{k + 1: f['anello'][k] for k in range(6)}}}


def documento(w, h, corpo, titolo, sotto, x0=-14, y0=-24):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}mm" height="{h:.1f}mm" viewBox="{x0} {y0} {w:.1f} {h:.1f}" '
            f'font-family="{F.SANS}"><rect x="{x0}" y="{y0}" width="{w:.1f}" height="{h:.1f}" fill="{PLATE}"/>'
            f'<text x="{x0 + 6}" y="{y0 + 10}" font-family="{F.SERIF}" font-weight="bold" font-size="7" fill="{BROWN}">{titolo}</text>'
            f'<text x="{x0 + 6}" y="{y0 + 16}" font-size="3.4" font-style="italic" fill="{BROWN}">{sotto}</text>{corpo}</svg>')


def pezzi_svg():
    o, px, py = [], 3 * F.W + 10, 5 * F.R + 16
    for i in range(14):
        for lato in (0, 1):
            x = 10 + 1.5 * F.W + (i % 7) * px
            y = 10 + 2.5 * F.R + (2 * (i // 7) + lato) * py
            f = faccia_kit(i, lato)
            nost = sum(t in M.OSTACOLI for t in f['celle'].values())
            o.append(F.fiore(f, x, y, 0, f'p{i}{lato}', 0, True, f'{i + 1}{"AB"[lato]}'))
            o.append(f'<text x="{x:.1f}" y="{y + 2.5 * F.R + 5:.1f}" text-anchor="middle" font-size="3.6" fill="{F.INK}">'
                     f'{i + 1}{"AB"[lato]} · {f["nome"]} ({nost} ost.)</text>')
    return documento(20 + 7 * px, 30 + 4 * py, ''.join(o), 'I 14 fiori a due facce (A sopra, B sotto)',
                     'Terreno libero chiaro (prato, sentiero, mattonato, pavimento), acqua accidentata con «+1», ostacoli scuri col bordo netto.', 0, -14)


def mappa_svg(disp, titolo, sotto, domande=(), cripta=None, staccati=0.0, cid='m'):
    t = M.mappa(disp)
    L, A = F.LARGO, F.ALTO
    num = {h: i for i, h in enumerate(M.PARTENZE, 1)}
    o = [f'<rect x="{-FASCIA:.2f}" y="{-FASCIA:.2f}" width="{L + 2 * FASCIA:.2f}" height="{A + 2 * FASCIA:.2f}" rx="1.5" fill="#d9cfa8"/>']
    for c in range(1, 13):
        o += [f'<text x="{F.centro_mappa((c, r))[0]:.2f}" y="{yy:.2f}" text-anchor="middle" font-weight="bold" font-size="3.6" fill="{F.INK}">{c}</text>'
              for r, yy in ((1, -FASCIA / 2 + 1.3), (12, A + FASCIA / 2 + 1.3))]
    for r in range(1, 13):
        y = F.centro_mappa((1, r))[1] + 1.3
        o += [f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-weight="bold" font-size="3.6" fill="{F.INK}">{r}</text>' for x in (-FASCIA / 2, L + FASCIA / 2)]
    base = {h: (*F.centro_mappa(h), t[h]) for h in M.BASE}
    o.append(F.pezzo(base, cid + 'b', partenze={h: num[h] for h in M.PARTENZE}))
    cx, cy = L / 2, A / 2
    for s, (i, lato, rot) in sorted(disp.items()):
        x0, y0 = F.centro_mappa(M.SPAZI[s])
        dx, dy = (x0 - cx) * staccati, (y0 - cy) * staccati
        o.append(f'<g transform="translate({dx:.2f} {dy:.2f})">' + F.fiore(faccia_kit(i, lato), x0, y0, rot, f'{cid}{s}', 0, True, f'{i + 1}{"AB"[lato]}') + '</g>')
    for h in domande:   # segnaposto «?» con la tessera Esplorazione coperta sopra (Ø 24)
        x, y = F.centro_mappa(h)
        o.append(f'<circle cx="{x + 0.5:.2f}" cy="{y + 0.8:.2f}" r="11.6" fill="#000" opacity="0.25"/>'
                 f'<circle cx="{x:.2f}" cy="{y:.2f}" r="11.6" fill="#3b2a1c" stroke="{BRASS}" stroke-width="0.8"/>'
                 f'<text x="{x:.2f}" y="{y + 4.6:.2f}" text-anchor="middle" font-family="{F.SERIF}" font-weight="bold" font-size="13" fill="#b8862b">?</text>')
    if cripta:
        o.append(F.segnalino_cripta(*F.centro_mappa(cripta)))
    return documento(L + 2 * FASCIA + 28, A + 2 * FASCIA + 36, ''.join(o), titolo, sotto)


def scrivi(nome, svg, dpi=200):
    f = os.path.join(QUI, nome)
    with open(f + '.svg', 'w', encoding='utf-8') as fh:
        fh.write(svg)
    subprocess.run(['magick', '-density', str(dpi), f + '.svg', '-background', PLATE, '-flatten', f + '.png'], check=True)
    print(f + '.png')


def main():
    scrivi('m12_pezzi', pezzi_svg(), 150)
    rnd = random.Random(2026)
    d = M.draft_casuale(rnd)
    t = M.mappa(d)
    dom = M.posa_domande(t, rnd)
    x, y = sum(rnd.randint(1, 6) for _ in range(2)), sum(rnd.randint(1, 6) for _ in range(2))
    c, sp = M.cripta(t, x, y, dom)
    nota = f'spostata di {sp} esagon{"o" if sp == 1 else "i"}' if sp else ('sulla «?»: «?» e tessera tornano nella riserva' if c in dom else 'nessuno spostamento')
    scrivi('m12_draft', mappa_svg(d, 'Mappa 12×12 da draft casuale',
                                  f'Base con le 6 Partenze, 14 fiori posati a caso, 24 «?» coperte; Cripta tirata in ({x}, {y}): {nota}.',
                                  dom - {c}, c, cid='d'))
    pr, _ = M.carica_preset()
    scrivi('m12_strettoie', mappa_svg(pr['Strettoie'], 'Preset «Strettoie» 12×12',
                                      'Stessi 14 fiori in spazio, faccia e rotazione fissi (freccia d\'ottone); pezzi staccati di qualche mm.',
                                      staccati=0.03, cid='s'))


if __name__ == '__main__':
    main()
