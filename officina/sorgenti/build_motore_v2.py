# Costruisce ../motore.js (il motore del simulatore che gira nel browser dell'Officina)
# a partire dal gioco v2 in ../../v2/sorgenti (game.js, ui.js, cards_v2.json, nemici_v2.json) e da tail_v2.js.
# Uso: cd officina/sorgenti && python3 build_motore_v2.py [cartella dei sorgenti v2]
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', '..', 'v2', 'sorgenti')
g = open(os.path.join(src, 'game.js')).read()
reps = [  # agganci per i Terreni: movimento su percorso, esagoni bloccati, inizio turno
 ("const hexes = allHexes().filter(h => { const d = hexDist(h, p.pos); return d >= 1 && d <= n; });",
  "const hexes = allHexes().filter(h => { const d = moveDist(p.pos, h); return d >= 1 && d <= n && canStop(h); });"),
 ("const hexes = allHexes().filter(h => { const x = hexDist(h, p.pos); return x >= 1 && x <= d; });",
  "const hexes = allHexes().filter(h => { const x = moveDist(p.pos, h); return x >= 1 && x <= d && canStop(h); });"),
 ("const sc = h => { const d = hexDist(h, G.treasure);", "const sc = h => { const d = moveDist(h, G.treasure);"),
 ("function hexDist(a, b) {", "let moveDist = (a, b) => hexDist(a, b); let canStop = h => true; let onTurnStart = null;\nfunction hexDist(a, b) {"),
 ("  if (p.ashafe > 0) heal(p, 1);\n  const gt", "  if (p.ashafe > 0) heal(p, 1);\n  if (onTurnStart) await onTurnStart(p);\n  const gt"),
]
for a, b in reps:
    assert g.count(a) == 1, a[:60]
    g = g.replace(a, b)
cards = json.load(open(os.path.join(src, 'cards_v2.json'))); nem = json.load(open(os.path.join(src, 'nemici_v2.json')))
slim = []
for c in cards:
    d = {'id': c['id'], 'nome': c['nome'], 'tipo': c['tipo'], 'testo': c['testo']}
    if c['tipo'] != 'TC' and c['classe'] != 'Tutte le classi': d['cls'] = [k.strip() for k in c['classe'].split('-')]
    if c.get('rarita'): d['rarita'] = c['rarita']
    if c.get('slot'): d['slot'] = c['slot']
    slim.append(d)
ui = open(os.path.join(src, 'ui.js')).read()
a = "cls: p.startCls, race: p.race,"; assert ui.count(a) == 1; ui = ui.replace(a, "cls: p.startCls, spawn0: p.spawn0, race: p.race,")
tailre = '\nrenderTempo();\ndealDecks();\nrenderCatalog();\nrender();'
assert ui.rstrip().endswith(tailre.strip()), ui[-200:]
ui = ui.rstrip()[:-len(tailre.strip())]
pre = """// Motore del Tesoro del Goblin (gioco v2, Carte Trama v2) per l'Officina (Web Worker). Generato da build_motore_v2.py.
const noop=()=>{};const el=new Proxy({}, { get: (t, k) => k === 'value' ? '' : (typeof k === 'string' ? (t[k] ?? (() => el)) : undefined), set: () => true });
const document={addEventListener:noop,getElementById:()=>el,querySelector:()=>el,querySelectorAll:()=>[]};const window={};const localStorage={getItem:()=>null,setItem:noop};
"""
out = pre + 'const CARDS=' + json.dumps(slim, ensure_ascii=False) + ';\nconst NEMICI_JSON=' + json.dumps(nem, ensure_ascii=False) + ';\n' + g + '\n' + ui + '\n' + open(os.path.join(here, 'tail_v2.js')).read()
open(os.path.join(here, '..', 'motore.js') if len(sys.argv) < 3 else sys.argv[2], 'w').write(out)
print('motore.js', len(out), 'byte')
