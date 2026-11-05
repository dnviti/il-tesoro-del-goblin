# Costruisce ../motore.js (il motore del simulatore che gira nel browser dell'Officina)
# a partire dai sorgenti del gioco in ../../sorgenti (game.js, ui.js, cards.json) e da tail.js.
# Uso: cd officina/sorgenti && python3 build_motore.py
import json, os
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, '..', '..', 'sorgenti')
g = open(os.path.join(src, 'game.js')).read()
reps = [  # stessi agganci di sorgenti/framework/build_x.py: movimento su percorso, esagoni bloccati, inizio turno
 ("const hexes = allHexes().filter(h => { const d = hexDist(h, p.pos); return d >= 1 && d <= n; });",
  "const hexes = allHexes().filter(h => { const d = moveDist(p.pos, h); return d >= 1 && d <= n && canStop(h); });"),
 ("const hexes = allHexes().filter(h => { const x = hexDist(h, p.pos); return x >= 1 && x <= d; });",
  "const hexes = allHexes().filter(h => { const x = moveDist(p.pos, h); return x >= 1 && x <= d && canStop(h); });"),
 ("if (isLocated(p)) { return hexes.slice().sort((a, b) => hexDist(a, G.treasure) - hexDist(b, G.treasure))[0]; }",
  "if (isLocated(p)) { return hexes.slice().sort((a, b) => moveDist(a, G.treasure) - moveDist(b, G.treasure))[0]; }"),
 ("function hexDist(a, b) {", "let moveDist = (a, b) => hexDist(a, b); let canStop = h => true; let onTurnStart = null;\nfunction hexDist(a, b) {"),
 ("  if (p.ashafe > 0) heal(p, 1);\n  const gt", "  if (p.ashafe > 0) heal(p, 1);\n  if (onTurnStart) await onTurnStart(p);\n  const gt"),
]
for a, b in reps:
    assert g.count(a) == 1, a[:60]
    g = g.replace(a, b)
# manopole chierRev e clsPV del pacchetto di equilibrio: si aggiungono solo se game.js non le ha ancora
if 'chierRev' not in g:
    a = "t.flags.revived = true; t.pv = 1; log('Chierico: torna in vita con 1 PV!', 'good');"; assert g.count(a) == 1
    g = g.replace(a, "t.flags.revived = true; t.pv = BAL.chierRev || 1; log(`Chierico: torna in vita con ${t.pv} PV!`, 'good');")
if 'clsPV' not in g:
    a = "const base = { pv: 10 + (sp.cls === 'Guerriero' ? BAL.guerPV : 0),"; assert g.count(a) == 1
    g = g.replace(a, "const base = { pv: 10 + (sp.cls === 'Guerriero' ? BAL.guerPV : 0) + ((BAL.clsPV || {})[sp.cls] || 0),")
cards = json.load(open(os.path.join(src, 'cards.json')))
slim = []
for c in cards:
    d = {'id': c['id'], 'nome': c['nome'], 'tipo': c['tipo'], 'testo': c['testo_rimodulato'] or c['testo']}
    if c['mazzo'].startswith('Classe: '): d['cls'] = c['mazzo'][8:]
    slim.append(d)
ui = open(os.path.join(src, 'ui.js')).read()
a = "cls: p.startCls, race: p.race,"; assert ui.count(a) == 1; ui = ui.replace(a, "cls: p.startCls, spawn0: p.spawn0, race: p.race,")
tailre = '\nrenderTempo();\ndealDecks();\nrenderCatalog();\nrender();'
assert ui.rstrip().endswith(tailre.strip()), ui[-200:]
ui = ui.rstrip()[:-len(tailre.strip())]
pre = """// Motore del Tesoro del Goblin per l'Officina (Web Worker). Generato da build_motore.py.
const noop=()=>{};const el=new Proxy({}, { get: (t, k) => k === 'value' ? '' : (typeof k === 'string' ? (t[k] ?? (() => el)) : undefined), set: () => true });
const document={addEventListener:noop,getElementById:()=>el,querySelector:()=>el,querySelectorAll:()=>[]};const window={};const localStorage={getItem:()=>null,setItem:noop};
"""
out = pre + 'const CARDS=' + json.dumps(slim, ensure_ascii=False) + ';\n' + g + '\n' + ui + '\n' + open(os.path.join(here, 'tail.js')).read()
open(os.path.join(here, '..', 'motore.js'), 'w').write(out)
print('motore.js', len(out), 'byte')
