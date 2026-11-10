#!/usr/bin/env python3
# Sacchetto a due colori (Daniele, 2/11): tessere blu = Imprevisto (si gira la prima carta del mazzetto Imprevisti:
# Trappole, Locande, Fonti, Fabbri), tessere rosse = Mostro (prima carta del mazzetto del livello dell'eroe:
# LV 1-2 mazzetto 1, LV 3-4 mazzetto 2, LV 5+ mazzetto 3 = boss LV 5; uno dei boss, pescato a inizio partita, custodisce MIMI; niente mini-boss).
# Da applicare dopo patch_eventi.py.  Uso: python3 patch_colori.py game.js
import sys
f = sys.argv[1]; s = open(f).read()
def rep(old, new):
    global s
    if s.count(old) != 1: raise SystemExit('manca o doppio: ' + old[:90])
    s = s.replace(old, new, 1)
rep("  bldTok: { locanda: 2, fonte: 2, fabbro: 2 },\n};",
    "  bldTok: { locanda: 2, fonte: 2, fabbro: 2 },\n"
    "  colorBag: true,               // sacchetto a due colori (Daniele, 2/11): rosse = Mostro, blu = Imprevisto\n"
    "  bagColor: { creatura: 25, imprevisto: 11 },\n"
    "  impDeck: { trappola: 5, locanda: 2, fonte: 2, fabbro: 2 }, // mazzetto Imprevisti: la carta girata va in fondo\n"
    "  monLv: true,                  // il Mostro viene dal mazzetto del livello dell'eroe: LV 1-2 → 1, LV 3-4 → 2, LV 5+ → 3\n};")
rep("  creatura: { n: 'Nemico I', g: '⚔' },", "  creatura: { n: 'Mostro', g: '⚔' },\n  imprevisto: { n: 'Imprevisto', g: '!' },")
rep("Object.entries({ ...(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens), ...(BAL.bldBag ? BAL.bldTok : {}) })",
    "Object.entries(BAL.colorBag ? BAL.bagColor : { ...(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens), ...(BAL.bldBag ? BAL.bldTok : {}) })")
rep("  tl.revealed = true; tick('casella');\n  switch (tl.type) {",
    "  if (tl.type === 'imprevisto') { const card = drawImp(); log(`${p.name} gira la prima carta Imprevisto: ${TILE[card].n}.`); tl.type = card; }\n"
    "  tl.revealed = true; tick('casella');\n  switch (tl.type) {")
rep("async function endOfTurn(p, skipped) {",
    "function drawImp() {\n  if (!G.imp || !G.imp.length) G.imp = shuffle(Object.entries(BAL.impDeck).flatMap(([k, n]) => Array(n).fill(k)));\n  const c = G.imp.pop(); G.imp.unshift(c); return c;\n}\n"
    "async function endOfTurn(p, skipped) {")
rep("const deckII = () => [...MAZZO_II, ...(BAL.miniBoss ? MINIBOSS : [])];",
    "const deckII = () => [...MAZZO_II, ...(BAL.miniBoss && !BAL.monLv ? MINIBOSS : [])];\n"
    "const deckIII = () => BOSSES.filter(b => !G.boss || b.name !== G.boss.name); // mazzetto 3 = boss LV 5 (Daniele, 2/11, niente mini-boss); quello pescato a inizio partita custodisce MIMI\n"
    "const monTier = p => { const t = BAL.monTh || [3, 5]; return p.level >= t[1] ? 3 : p.level >= t[0] ? 2 : 1; };")
rep("  if (p.challenge) { kind = 'miniboss'; log('Sfidare i potenti: al posto della creatura appare un nemico del mazzetto II!', 'gold'); }\n"
    "  const deckK = kind === 'miniboss' ? 'mb' : 'cr';\n"
    "  if (!G.nem[deckK].length) G.nem[deckK] = shuffle(kind === 'miniboss' ? deckII() : [...BESTIARIO]);\n"
    "  const foe = makeCreature(G.nem[deckK].pop(), p.level);\n"
    "  kind = foe.tipo === 'Mini-boss' ? 'miniboss' : 'creatura';",
    "  let tier = BAL.monLv ? monTier(p) : (kind === 'miniboss' ? 2 : 1);\n"
    "  if (p.challenge && tier < 2) { tier = 2; log('Sfidare i potenti: al posto della creatura appare un nemico del mazzetto II!', 'gold'); }\n"
    "  const deckK = ['cr', 'mb', 't3'][tier - 1];\n"
    "  if (!G.nem[deckK] || !G.nem[deckK].length) G.nem[deckK] = shuffle(tier === 3 ? deckIII() : tier === 2 ? deckII() : [...BESTIARIO]);\n"
    "  if (BAL.monLv) log(`${p.name} è di livello ${p.level}: gira la prima carta del mazzetto Mostri ${tier}.`);\n"
    "  const foe = makeCreature(G.nem[deckK].pop(), p.level);\n"
    "  kind = foe.tipo === 'Mini-boss' || foe.tipo === 'Boss' ? 'miniboss' : 'creatura';")
open(f, 'w').write(s)
print('ok')
