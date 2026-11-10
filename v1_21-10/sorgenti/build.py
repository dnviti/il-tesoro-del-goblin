import json
cards=json.load(open('cards.json'))
slim=[]
for c in cards:
    d={'id':c['id'],'nome':c['nome'],'tipo':c['tipo'],'testo':c['testo_rimodulato'] or c['testo']}
    if c['testo_rimodulato']: d['orig']=c['testo']
    if c['mazzo'].startswith('Classe: '): d['cls']=c['mazzo'][8:]
    slim.append(d)
t=open('template.html').read()
t=t.replace('/*CARDS_JSON*/',json.dumps(slim,ensure_ascii=False)).replace('/*GAME_JS*/',open('game.js').read()).replace('/*UI_JS*/',open('ui.js').read())
open('tesoro_del_goblin.html','w').write(t)
# standalone check file
open('check.js','w').write('const CARDS='+json.dumps(slim,ensure_ascii=False)+';\n'+open('game.js').read()+'\n'+open('ui.js').read())
