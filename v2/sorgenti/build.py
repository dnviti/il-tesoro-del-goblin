# Build della versione giocabile v2 (Carte Trama v2): tesoro_del_goblin.html + check.js per il simulatore
import json
cards = json.load(open('cards_v2.json')); nem = json.load(open('nemici_v2.json'))
slim = []
for c in cards:
    d = {'id': c['id'], 'nome': c['nome'], 'tipo': c['tipo'], 'testo': c['testo']}
    if c['testo'] != c['testo_originale'] and c['testo_originale']: d['orig'] = c['testo_originale']
    if c['tipo'] != 'TC' and c['classe'] != 'Tutte le classi': d['cls'] = [k.strip() for k in c['classe'].split('-')]
    if c.get('rarita'): d['rarita'] = c['rarita']
    if c.get('slot'): d['slot'] = c['slot']
    slim.append(d)
pre = 'const NEMICI_JSON=' + json.dumps(nem, ensure_ascii=False) + ';\n'
t = open('template.html').read()
t = t.replace('/*CARDS_JSON*/', json.dumps(slim, ensure_ascii=False) + ';\n' + pre.replace(';\n', '')).replace('/*GAME_JS*/', open('game.js').read()).replace('/*UI_JS*/', open('ui.js').read())
open('tesoro_del_goblin.html', 'w').write(t)
open('check.js', 'w').write('const CARDS=' + json.dumps(slim, ensure_ascii=False) + ';\n' + pre + open('game.js').read() + '\n' + open('ui.js').read())
