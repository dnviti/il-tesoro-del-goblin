#!/usr/bin/env python3
# Locanda, Fonte e Fabbro diventano segnalini del sacchetto (Daniele, 2/11): eventi pescati a caso, una volta sola, poi il segnalino torna nella scatola.
# Le loro 6 caselle della plancia diventano caselle «?».  Uso: python3 patch_eventi.py game.js
import sys
f = sys.argv[1]; s = open(f).read()
def rep(old, new):
    global s
    if old not in s: raise SystemExit('manca: ' + old[:90])
    s = s.replace(old, new, 1)
rep("  mbClues: 1,\n};", "  mbClues: 1,\n  bldBag: true,                 // Locanda, Fonte e Fabbro sono segnalini del sacchetto (Daniele, 2/11), non edifici stampati\n  bldTok: { locanda: 2, fonte: 2, fabbro: 2 },\n};")
rep("    for (const k of [...BUILDINGS, ...(BAL.caos ? ['evento'] : [])]) for (const [c, r] of PHYS[k])",
    "    for (const k of [...(BAL.bldBag ? [] : BUILDINGS), ...(BAL.caos ? ['evento'] : [])]) for (const [c, r] of PHYS[k])")
rep("    const bag = shuffle(Object.entries(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens).flatMap(([k, n]) => Array(n).fill(k)));\n    if (BAL.bagDraw) { tiles.bag = bag; PHYS.q.forEach(",
    "    const bag = shuffle(Object.entries({ ...(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens), ...(BAL.bldBag ? BAL.bldTok : {}) }).flatMap(([k, n]) => Array(n).fill(k)));\n    const qHex = BAL.bldBag && BAL.bldHexQ !== false ? [...PHYS.q, ...BUILDINGS.flatMap(k => PHYS[k]).filter(h => !PHYS.q.some(x => x[0] === h[0] && x[1] === h[1]))] : PHYS.q;\n    if (qHex !== PHYS.q) qHex.sort((a, b) => a[1] - b[1] || a[0] - b[0]);\n    if (BAL.bagDraw) { tiles.bag = bag; qHex.forEach(")
rep("    else PHYS.q.forEach(([c, r], i) =>", "    else qHex.forEach(([c, r], i) =>")
rep("Si ricarica fermandosi in una Locanda.' });", "Si ricarica quando peschi una Locanda dal sacchetto.' });")
open(f, 'w').write(s)
print('ok')
