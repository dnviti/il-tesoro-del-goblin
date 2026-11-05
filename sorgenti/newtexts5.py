# Equilibrio della scatola base, 21/10 (pacchetto del thread del gioco fisico): testo in uso + motivo
import json
NEW5 = {
 'TC-03': ("La tua pedina è un Chierico fino alla fine della partita. Quando vieni sconfitto in battaglia ritorni in vita con (3) PF e continui lo scontro. Il potere si ricarica ogni volta che ti fermi in una locanda", "Scatola base in quattro: il Chierico restava indietro (0,89), ora torna in vita con 3 PF invece di 1"),
 'TC-05': ("La tua pedina è un Guerriero fino alla fine della partita. (+2) PF. Ogni scontro vinto ti dà Ispirazione; se hai Ispirazione puoi usarla per ridurre di (2) la CA di un nemico", "Scatola base: +2 PF invece di +1 (con −2 CA all'Ispirazione dal pomeriggio del 21)"),
 'TC-06': ("La tua pedina è un Ladro fino alla fine della partita. (+3) MOV e (+1) PF. Fuggire dalle battaglie non ha conseguenze e nel primo round di ogni scontro hai vantaggio", "Scatola base in quattro: il Ladro era il più debole (0,81), ora +3 MOV e +1 PF"),
 'TI-22': ("Scegli uno dei seguenti effetti - scarta (1) carta (+1) MOV (+1) ATT - scarta (2) carte: un avversario perde (2) turni - scarta (4) carte: infliggi (3) danni a un avversario", "Con 3-4 giocatori fermare tutti gli avversari era troppo forte: ora un avversario a scelta"),
 'TI-39': ("Distruggi la mappa attiva. Se non c'è una mappa attiva, un avversario perde (1) turno", "Senza mappe in gioco era una carta morta; ora colpisce un avversario a scelta, non tutti"),
 'TI-52': ("Ottieni (2) indizi; ogni avversario ne ottiene (1)", "Più semplice al tavolo e accorcia la partita con 3-4 giocatori"),
}
cards = json.load(open('cards.json')); before = json.load(open('before_texts.json'))
for c in cards:
    if c['id'] in NEW5:
        t, why = NEW5[c['id']]
        if c['id'] not in before: before[c['id']] = c.get('testo_rimodulato') or c['testo']
        c['testo_rimodulato'] = t; c['bilanciamento'] = why
json.dump(cards, open('cards.json', 'w'), ensure_ascii=False, indent=1)
json.dump(before, open('before_texts.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(NEW5))
