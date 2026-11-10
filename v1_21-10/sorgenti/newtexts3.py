# Ritocchi del 21/10 mattina (ritmo e caos): testo in uso + motivo
import json
NEW3 = {
 'TC-02': ("La tua pedina è un Bardo fino alla fine della partita. Tutte le tue statistiche aumentano di (1), il MOV di (2)", "Con le partite più corte il Bardo restava indietro in due giocatori: +1 MOV in più"),
 'TC-05': ("La tua pedina è un Guerriero fino alla fine della partita. (+1) PF. Ogni scontro vinto ti dà Ispirazione; se hai Ispirazione puoi usarla per ridurre di (3) la CA di un nemico", "Ispirazione a ogni scontro vinto e −3 CA (era −2); dopo i ritocchi al ritmo anche +1 PF"),
 'TC-09': ("La tua pedina è uno Stregone fino alla fine della partita. Le carte incantesimo che lanci ottengono (+1). (+2) MOV", "Con le partite più corte lo Stregone era la classe più debole: +2 MOV"),
 'TI-09': ("Puoi giocare questa carta solo se il tuo avversario ha trovato il tesoro. Un beholder appare a difesa del forziere 12/3/0/2, ogni volta che colpisce infligge pietrificazione o paura. È un Boss", "Boss più rapidi per accorciare il finale: 12 PV invece di 15"),
 'TI-20': ("Ottieni (2) indizi ma perdi (1) turno", "Nessuna carta individua più il tesoro di colpo; ora si perde 1 turno invece di 2"),
 'TI-22': ("Scegli uno dei seguenti effetti - scarta (1) carta (+1) MOV (+1) ATT - scarta (2) carte: ogni avversario perde (2) turni - scarta (4) carte: infliggi (3) danni a un avversario", "Con 3-4 giocatori colpisce ogni avversario: 2 turni invece di 3 per non tenere fermi tre giocatori"),
 'TI-54': ("Ogni eroe ottiene (1) indizio", "Far perdere 4 turni a tutti allungava solo la partita: ora accelera la corsa al tesoro"),
}
cards = json.load(open('cards.json')); before = json.load(open('before_texts.json'))
for c in cards:
    if c['id'] in NEW3:
        t, why = NEW3[c['id']]
        if c['id'] not in before: before[c['id']] = c.get('testo_rimodulato') or c['testo']
        c['testo_rimodulato'] = t
        c['bilanciamento'] = (c.get('bilanciamento') + '. ' if c.get('bilanciamento') and c['id'] in ('TC-05','TI-20','TI-22') else '') + why if c['id'] not in ('TC-05','TI-20','TI-22') else why
        if c['id'] == 'TI-09': c['statistiche'] = '12/3/0/2 (Boss*)'
json.dump(cards, open('cards.json', 'w'), ensure_ascii=False, indent=1)
json.dump(before, open('before_texts.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(NEW3))
