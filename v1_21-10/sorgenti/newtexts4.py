# Allineamento al gioco fisico del 21/10 pomeriggio (niente D4, 3 slot, plancia stampata): testo in uso + motivo
import json
NEW4 = {
 'TC-02': ("La tua pedina è un Bardo fino alla fine della partita. Tutte le tue statistiche aumentano di (1)", "Con la plancia stampata il Bardo tornava avanti: di nuovo +1 a tutto, MOV compreso"),
 'TC-05': ("La tua pedina è un Guerriero fino alla fine della partita. (+1) PF. Ogni scontro vinto ti dà Ispirazione; se hai Ispirazione puoi usarla per ridurre di (2) la CA di un nemico", "Con 3 slot il Guerriero teneva insieme arma, armatura ed elmo: Ispirazione torna a −2 CA come sulla carta originale"),
 'TI-42': ("Ottieni l'aspetto di una bestia che hai incontrato: (+2) a tutte le statistiche per (3) turni (l'equipaggiamento torna nella tua mano)", "Con la plancia stampata il Druido era la classe più debole: 3 turni invece di 2"),
 'TI-60': ("Il tuo Fuoco fatuo diventa un Lupo (3/3/0/0) che infligge (1) danno a ogni colpo. Se non hai il Fuoco fatuo, il Lupo arriva comunque", "Druido: il Lupo attacca con +3 invece di +2"),
 'TE-23': ("(+3) CA. Si impugna: occupa lo slot Arma. Guerriero: il primo colpo che subisci in ogni scontro è dimezzato", "Con 3 slot lo scudo nel Corpo si sommava all'arma a due mani e il Guerriero dominava: lo scudo si impugna"),
 'TE-25': ("(+5) Att (-1) CA. Tiefling: subisce D6 − 1 danni (minimo 1) quando la impugna", "Niente D4 nella scatola: D6 − 1"),
 'TI-35': ("Tira un D6 (con 5 o 6 ritira) e a seconda del risultato: 1 perdi (1) PF; 2 la tua CA (-1) permanente; 3 (+2) MOV permanente; 4 il tuo avversario perde (2) PF", "Niente D4 nella scatola: D6 ritirando 5 e 6"),
 'TI-38': ("Tira un D6: 1-3 non succede niente, 4-6 ti curi di (4) PF. Puoi ritirare il dado una volta", "Niente D4 nella scatola: D6 con metà delle facce buone"),
}
cards = json.load(open('cards.json')); before = json.load(open('before_texts.json'))
for c in cards:
    if c['id'] in NEW4:
        t, why = NEW4[c['id']]
        if c['id'] not in before: before[c['id']] = c.get('testo_rimodulato') or c['testo']
        c['testo_rimodulato'] = t
        c['bilanciamento'] = why
        if c['id'] == 'TE-23': c['slot'] = 'Arma (scudo)'
json.dump(cards, open('cards.json', 'w'), ensure_ascii=False, indent=1)
json.dump(before, open('before_texts.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(NEW4))
