# Carte della scatola base corrette il 21/10 (thread del framework): testo in uso + motivo, e categorie
import json
NEW6 = {
 'TE-21': ("Recuperi (4) PF", "Con le partite più corte 2 PF valevano poco: ora 4"),
 'TM-05': ("Il terreno diventa una Foresta e il tesoro cambia posizione. Elfo e Druido: (+1) MOV finché la Selva resta", "Bonus più semplice da ricordare al tavolo e niente malus alle altre razze"),
}
CAT = {
 'TI-52': ('Carta Trama (leggendaria)', "Diventa la carta leggendaria del Mago al posto di Portale arcano; il testo non cambia"),
 'TI-63': ('Carta Trama (nuova)', "Non è più la leggendaria del Mago: resta una carta di classe normale"),
}
cards = json.load(open('cards.json')); before = json.load(open('before_texts.json'))
for c in cards:
    if c['id'] in NEW6:
        t, why = NEW6[c['id']]
        if c['id'] not in before: before[c['id']] = c.get('testo_rimodulato') or c['testo']
        c['testo_rimodulato'] = t; c['bilanciamento'] = why
    if c['id'] in CAT:
        c['categoria'], why = CAT[c['id']]
        c['bilanciamento'] = (c['bilanciamento'] + '. ' if c.get('bilanciamento') else '') + why
json.dump(cards, open('cards.json', 'w'), ensure_ascii=False, indent=1)
json.dump(before, open('before_texts.json', 'w'), ensure_ascii=False, indent=1)
print('ok')
