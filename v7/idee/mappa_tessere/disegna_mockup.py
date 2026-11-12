#!/usr/bin/env python3
"""Mock-up delle proposte di proposte.md (solo idee, non il kit): SVG in scala 1:1 in mm, poi PNG con ImageMagick.

Uso (dalla radice del repo):  python3 v7/idee/mappa_tessere/disegna_mockup.py

Scrive in questa cartella:
  mockup_fasce_base.svg/.png      preset base «Strettoie» montato con 3 pezzi (opzione D), pezzi staccati di 8 mm;
  mockup_fasce_miste.svg/.png     composizione libera: fascia nord di TM-03 Foresta + fiume + fascia sud di TM-06 Miniera;
  mockup_neutra_toppe.svg/.png    opzione E: fasce neutre, a nord le toppe di terreno del preset base posate sopra.
Disegno piatto come v7/idee/genera_bozza_mappa.py (stessi colori e icone), esagono 25,2 mm da lato a lato.
"""
import os
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(QUI, '..'))
sys.path.insert(0, QUI)
import genera_bozza_mappa as g   # noqa: E402  geometria, colori e icone della bozza (unità: esagono W = 26)
import tempo_setup as ts          # noqa: E402  dati dei 10 preset, fasce e composizione mista

K = 25.2 / g.W                    # mm per unità del disegno
GAP = 8 / K                       # 8 mm tra un pezzo e l'altro
CONTORNO = '#3a2a1c'
RAME = '#a65a32'
FASCE = (('N', 'Fascia nord · righe 1-4'), ('C', 'Fiume · righe 5-6 (uguale per tutti)'), ('S', 'Fascia sud · righe 7-10'))


def scosta(regione):
    return {'N': 0, 'C': GAP, 'S': 2 * GAP}[regione]


def cella(h, t, dy, neutra=False):
    """esagono h di tipo t (come tempo_setup.carica), spostato in basso di dy."""
    x, y = g.centro(h)
    y += dy
    s = g.R * 0.97
    if neutra and not ts.strada(t) and t != 'acqua':
        t = 'strada'
    col = (g.STRADA_COL if t in ('strada', '?') or t[0] in 'PC' else g.GUADO_COL if t in ('guado', 'ponte')
           else g.TIPI[t][1])
    o = [f'<polygon points="{g.punti(x, y, s)}" fill="{col}" stroke="{g.BORDO}" stroke-width="0.8"/>']
    if t in g.TIPI:
        o.append(g.TIPI[t][2](x, y))
    elif t in ('guado', 'ponte'):
        o.append(g.ic_guado(x, y))
    elif t == '?':
        o.append(g.q_mark(x, y, g.R * 0.42))
    elif t[0] == 'P':
        o.append(f'<polygon points="{g.punti(x, y, s)}" fill="#7a4f86" fill-opacity="0.85"/>'
                 f'<text x="{x:.2f}" y="{y + g.R * 0.33:.2f}" text-anchor="middle" font-weight="800" font-size="{g.R * 0.9:.2f}" fill="#fff">{t[1]}</text>')
    elif t[0] == 'C':
        o.append(f'<polygon points="{g.punti(x, y, s)}" fill="#d9b45a" stroke="#b8862b" stroke-width="1.6"/>'
                 f'<text x="{x:.2f}" y="{y + g.R * 0.35:.2f}" text-anchor="middle" font-family="serif" font-weight="800" font-size="{g.R * 0.95:.2f}" fill="{g.INK}">{t[1]}</text>')
    return o


def toppa(h, t, dy):
    """toppa di terreno appoggiata sopra la plancia neutra: ombra, bordo d'ottone, icona."""
    x, y = g.centro(h)
    y += dy
    return [f'<polygon points="{g.punti(x + 1.2, y + 1.6, g.R)}" fill="#000" fill-opacity="0.25"/>',
            f'<polygon points="{g.punti(x, y, g.R)}" fill="{g.TIPI[t][1]}" stroke="#a8823a" stroke-width="1.2"/>',
            g.TIPI[t][2](x, y)]


def pezzo(celle, dy):
    """contorno di taglio del pezzo: ogni esagono con un bordo spesso sotto, i riempimenti sopra coprono quelli interni."""
    return [f'<polygon points="{g.punti(*_su(h, dy), g.R)}" fill="{CONTORNO}" stroke="{CONTORNO}" stroke-width="3.2" stroke-linejoin="round"/>'
            for h in celle]


def _su(h, dy):
    x, y = g.centro(h)
    return x, y + dy


def muro(m, dy):
    (x1, y1), (x2, y2) = g.lato_comune(*sorted(m, key=g.TUTTI.index))
    return f'<line x1="{x1:.2f}" y1="{y1 + dy:.2f}" x2="{x2:.2f}" y2="{y2 + dy:.2f}" {g.MURO}/>'


def disegna(titolo, sottotitolo, scelta, etichette, neutra=False, toppe_da=None):
    """scelta: {'N': preset, 'C': preset (mura del fiume), 'S': preset}; etichette: {'N': testo, ...}."""
    t, muri = ts.componi(ts.REG_FASCE, ts.padrone_fasce, scelta)
    if neutra:
        # stampati sulla plancia neutra solo i muri delle Cripte; con le toppe a nord anche le mura libere di quella fascia
        muri = {m for m in muri if m in ts.MURI_FISSI or (toppe_da and ts.padrone_fasce(m) == 'N')}
    x0 = g.PAD - g.W * 0.9
    alto = g.TOP - g.W * 1.6
    w = g.W * 10.5 + 2 * g.PAD - 2 * x0 + g.W * 5.2
    h = g.centro('A10')[1] + g.R + 2 * GAP + g.W * 1.2 - alto
    o = [f'<rect x="{x0:.1f}" y="{alto:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#f7eedb"/>',
         f'<text x="{x0 + 8:.1f}" y="{alto + 15:.1f}" font-family="serif" font-weight="800" font-size="12" fill="{g.BROWN}">{titolo}</text>',
         f'<text x="{x0 + 8:.1f}" y="{alto + 27:.1f}" font-size="7" font-style="italic" fill="{g.BROWN}">{sottotitolo}</text>']
    for reg, _ in FASCE:
        celle = [c for c in g.TUTTI if ts.REG_FASCE[c] == reg]
        dy = scosta(reg)
        o += pezzo(celle, dy)
        for c in celle:
            o += cella(c, t[c], dy, neutra and reg != 'C')
        o += [muro(m, dy) for m in muri if ts.padrone_fasce(m) == reg]
        if toppe_da and reg == 'N':   # toppe solo a nord: prima/dopo
            o += [x for c in celle if not ts.strada(ts.PRESET[toppe_da][0][c]) and ts.PRESET[toppe_da][0][c] != 'acqua'
                  for x in toppa(c, ts.PRESET[toppe_da][0][c], dy)]
        ys = [g.centro(c)[1] + dy for c in celle]
        xe = g.PAD + g.W * 10.5 + 10
        ym = (min(ys) + max(ys)) / 2
        o.append(f'<line x1="{xe - 6:.1f}" y1="{min(ys) - g.R:.1f}" x2="{xe - 6:.1f}" y2="{max(ys) + g.R:.1f}" stroke="{RAME}" stroke-width="1"/>')
        for i, riga in enumerate(etichette[reg].split('\n')):
            o.append(f'<text x="{xe:.1f}" y="{ym - 3 + i * 9:.1f}" font-size="{7.5 if i == 0 else 6.2}" '
                     f'font-weight="{700 if i == 0 else 400}" fill="{g.INK}">{riga}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * K:.1f}mm" height="{h * K:.1f}mm" '
            f'viewBox="{x0:.1f} {alto:.1f} {w:.1f} {h:.1f}" font-family="sans-serif">' + ''.join(o) + '</svg>')


def scrivi(nome, svg):
    f = os.path.join(QUI, nome)
    with open(f + '.svg', 'w', encoding='utf-8') as fh:
        fh.write(svg)
    subprocess.run(['magick', '-density', '200', f + '.svg', '-background', '#f7eedb', '-flatten', f + '.png'], check=True)
    print(f + '.png')


def main():
    lato = 25.2 / 3 ** 0.5
    mm = f'fascia {g.num(10.5 * 25.2)} × {g.num((2 + 3 * 1.5) * lato)} mm; fiume {g.num(10.5 * 25.2)} × {g.num((2 + 1.5) * lato)} mm'
    scrivi('mockup_fasce_base', disegna(
        'Preset base «Strettoie» con 3 pezzi (opzione D)', f'Pezzi staccati di 8 mm per vederli; {mm}. Muri stampati, nessun listello.',
        {'N': 'base', 'C': 'base', 'S': 'base'},
        {'N': 'Strettoie · NORD\n40 esagoni, 8 «?»\nPartenze 1-2, Cripte 1-2',
         'C': 'Fiume\nuguale per tutti\nretro senza le 2 mura (Flegias)',
         'S': 'Strettoie · SUD\nè la fascia nord girata\ndi 180° (stesso disegno)'}))
    scrivi('mockup_fasce_miste', disegna(
        'Composizione libera: nord TM-03 Foresta + sud TM-06 Miniera', 'Ogni fascia si attacca al fiume: le 100 coppie nord/sud passano i controlli del §17.',
        {'N': 'TM-03', 'C': 'base', 'S': 'TM-06'},
        {'N': 'TM-03 Foresta · NORD', 'C': 'Fiume', 'S': 'TM-06 Miniera · SUD'}))
    svg = disegna('Plancia neutra + toppe (opzione E)',
                  'Nord: toppe del preset base posate (ombra = pezzo sopra). Sud: fascia neutra ancora vuota.',
                  {'N': 'base', 'C': 'base', 'S': 'base'},
                  {'N': 'Fascia NEUTRA\n+ 14 toppe del preset base', 'C': 'Fiume', 'S': 'Fascia NEUTRA\nancora senza toppe'},
                  neutra=True, toppe_da='base')
    scrivi('mockup_neutra_toppe', svg)


if __name__ == '__main__':
    main()
