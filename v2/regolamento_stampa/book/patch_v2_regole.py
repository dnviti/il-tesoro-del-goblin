# Regolamento v5 (Carte Trama v2, 27/10/2026): patch di build.py e inizia.py del regolamento v4.1
import re
def rep(s, a, b):
    if a not in s: raise SystemExit('manca: ' + a[:90])
    return s.replace(a, b)

s = open('build.py').read()
LUPO = "enemy_card('Lupo grigio','L',1,5,3,0,['1 indizio','1 punto esperienza'],w={w})"
# p2
s = rep(s, '<p class="tip">Nelle carte trovi a volte PF e CA: sono i PV e l’AR della scheda.</p>',
        '<p class="tip">Sulle carte i numeri tra parentesi sono valori: «(+1) AR» vuol dire 1 in più di AR.</p>')
# p3 componenti
s = rep(s, '<div><b>4</b> Miniature eroe: Guerriero, Ladro, Mago, Chierico</div>', '<div><b>4</b> Miniature eroe: Guerriero, Ladro, Mago, Oracolo</div>')
s = rep(s, '<div><b>28</b> Carte di classe (7 per classe)</div><div><b>20</b> Carte comuni</div>',
        '<div><b>29</b> Carte di classe (dorso colorato)</div><div><b>44</b> Carte comuni: 8 Mappe, 12 Equipaggiamenti, 24 Incantesimi</div>')
s = rep(s, '<div><b>4</b> Carte Aiuto</div><div><b>5</b> Divisori per i mazzi</div>',
        '<div><b>13</b> Carte Creatura e <b>4</b> carte Mini-boss</div><div><b>4</b> Carte Aiuto · <b>5</b> Divisori</div>')
s = rep(s, '<div><b>8</b> Tessere Specie</div>', '<div><b>10</b> Tessere Specie</div>')
s = rep(s, """<div class="t">{token('Lupo grigio',5,'+3',10,'D6−1',92)}<br>13 Creature</div>""", """<div class="t">{simple_token('spade','Creatura',INK,60)}<br>13 Creature</div>""")
s = rep(s, """<div class="t">{simple_token('piedi','Sentiero',BROWN,60)}<br>8 Sentieri tranquilli</div>""",
        """<div class="t">{simple_token('pergamena','Mappa',GOLD,60)}<br>2 Mappe strappate</div>
<div class="t">{simple_token('piedi','Sentiero',BROWN,60)}<br>6 Sentieri tranquilli</div>""")
s = rep(s, """<p class="tip" style="text-align:center">Sulle creature leggi: {I('cuore',RED)}PV · {I('spade')}ATT · {I('scudo',BLUE)}Difesa · danno</p>""",
        """<h2>Le carte Nemico</h2>
<div class="cols" style="align-items:center"><div style="flex:none">{""" + LUPO.format(w=230) + """}</div>
<div><p style="margin:0">Il segnalino dice solo <b>Creatura</b> o <b>Mini-boss</b>: chi è lo dice la carta in cima al suo mazzo. Leggi {I('cuore',RED)}PV, {I('spade')}ATT e {I('scudo',BLUE)}AR; il <b>livello</b> (LV) dice quanto fa male.</p></div></div>""")
# p5 preparazione
s = rep(s, "Metti Guardiano, MIMI e i 4 mini-boss sulle loro sagome nella Sala del Tesoro.",
        "Mescola le 13 carte Creatura e le 4 carte Mini-boss in due mazzi coperti accanto alla plancia. Metti Guardiano, MIMI e i 4 mini-boss sulle loro sagome nella Sala del Tesoro.")
s = rep(s, "Incastra la Tessera Specie e infila la Carta Classe nel primo slot in alto: il suo effetto vale da subito e per tutta la partita.</li>",
        "Incastra la Tessera Specie e infila la Carta Classe nel primo slot in alto: il suo effetto vale da subito e per tutta la partita. Metti <b>1 Indizio</b> sulla scheda: tutti partono con un Indizio.</li>")
s = rep(s, "Mescola le 7 carte della tua classe e pescane 5 coperte; le altre 2 tornano nella scatola senza che nessuno le veda. Mescolate le 20 carte comuni e pescatene 5 coperte a testa.",
        "Mescola le carte della tua classe e pescane 3 coperte; le altre tornano nella scatola senza che nessuno le veda. Mescolate le 44 carte comuni e pescatene 7 coperte a testa.")
s = rep(s, "<tr><td><b>Orco</b></td><td>+2 ATT e +1 PV</td></tr></table>",
        "<tr><td><b>Orco</b></td><td>+2 ATT e +1 PV</td></tr>\n<tr><td><b>Sanguar</b></td><td>+2 MOV e +1 PV (sono non morti)</td></tr></table>")
# p7 turno
s = rep(s, "Al massimo <b>una</b> può essere un equipaggiamento. Le pozioni contano come carte. Le carte giocate",
        "Al massimo <b>una</b> può essere un equipaggiamento. Anche le carte che giochi in risposta (per esempio Parata Perfetta) contano tra le 2. Le carte giocate")
# p9 esplorare
s = rep(s, "<tr><td>{I('spade')}<b>Creatura</b></td><td>Scontro, oppure fuga (pagina 10). Se vinci il segnalino si toglie; se fuggi o perdi lo lasci scoperto su quella casella.</td></tr>",
        "<tr><td>{I('spade')}<b>Creatura</b></td><td>Gira la prima carta Creatura: scontro, oppure fuga (pagina 10). Se vinci togli il segnalino. Se fuggi o perdi, il segnalino resta scoperto: chi si ferma lì gira una nuova carta. La carta va in fondo al mazzo.</td></tr>")
s = rep(s, "<tr><td>{I('teschio',RED)}<b>Mini-boss</b></td><td>Metti sulla casella la sua miniatura, presa dalla Sala del Tesoro (statistiche sulla sagoma). Poi scontro o fuga.</td></tr>",
        "<tr><td>{I('teschio',RED)}<b>Mini-boss</b></td><td>Gira la prima carta Mini-boss e metti sulla casella la miniatura con quel nome, presa dalla Sala del Tesoro. Poi scontro o fuga.</td></tr>")
s = rep(s, "<tr><td>{I('piedi',BROWN)}<b>Sentiero tranquillo</b></td><td>Non succede niente. Togli il segnalino.</td></tr>",
        "<tr><td>{I('pergamena',GOLD)}<b>Mappa strappata</b></td><td>Prendi 1 Indizio. Togli il segnalino.</td></tr>\n<tr><td>{I('piedi',BROWN)}<b>Sentiero tranquillo</b></td><td>Non succede niente. Togli il segnalino.</td></tr>")
s = rep(s, "Il Chierico ricarica comunque in Locanda.", "L’Oracolo ricarica comunque in Locanda.")
# p10 scontro
s = rep(s, """<p class="lead">Una sola regola per colpire: tira il <b>D20</b>, aggiungi il tuo <b>ATT</b>. Se arrivi alla <b>Difesa</b> del bersaglio, lo colpisci.</p>
<ol>
<li><b>Attacchi tu per primo.</b> D20 + ATT. Se il totale è uguale o maggiore della Difesa stampata sul nemico, tira il danno.</li>
<li><b>Poi attacca il nemico.</b> Per lui tira l’avversario (con più giocatori, chi ti siede a destra): D20 + ATT del nemico contro la tua Difesa, poi il danno stampato sul segnalino.</li>""",
"""<p class="lead">Ogni attacco sono <b>due tiri</b>: prima il <b>tiro per colpire</b> con il D20, poi, se colpisci, il <b>tiro per il danno</b> con il D6.</p>
<ol>
<li><b>Attacchi tu per primo.</b> Tiro per colpire: D20 + il tuo ATT. Se il totale arriva alla <b>Difesa</b> del nemico (10 + la sua AR), lo colpisci e tiri il danno.</li>
<li><b>Poi attacca il nemico.</b> Per lui tira l’avversario (con più giocatori, chi ti siede a destra): D20 + ATT del nemico contro la tua Difesa (10 + la tua AR), poi il suo danno.</li>""")
s = rep(s, """<table><tr><th>Il tuo danno</th><th></th></tr>
<tr><td>A mani nude</td><td><b>D6 − 1</b> (minimo 1)</td></tr>
<tr><td>Arma a una mano</td><td><b>D6</b></td></tr>
<tr><td>Arma a due mani</td><td><b>D6 + 1</b></td></tr></table>""",
"""<table><tr><th>Tiro per il danno</th><th></th></tr>
<tr><td>Ogni eroe</td><td><b>D6</b>, più i bonus delle carte</td></tr>
<tr><td>Nemico di LV 1</td><td><b>D6 − 1</b> (minimo 1)</td></tr>
<tr><td>Nemico di LV 2</td><td><b>D6</b></td></tr>
<tr><td>LV 3 e oltre: mini-boss e Guardiano</td><td><b>D6 + 1</b></td></tr></table>""")
# p11 esempio
s = rep(s, "<p><b>Lia</b> gioca il Guerriero: ATT 3, Difesa 11, PV 10, e ha equipaggiato l’Arco da guerra (arma a due mani: danno D6 + 1). Si ferma su una casella «?» e la gira:</p>\n<div class=\"tokens\">{token('Lupo grigio',5,'+3',10,'D6−1',110)}</div>\n<p>Il Lupo grigio ha 5 PV, ATT +3, Difesa 10, danno D6 − 1. Lia gira il dado rosso sul 5. Per il lupo tira Marco.</p>",
        "<p><b>Lia</b> gioca il Guerriero: ATT 3 (con la Spada del Custode), AR 1 quindi Difesa 11, PV 13. Si ferma su una casella «?», pesca il segnalino Creatura e gira la prima carta:</p>\n<div class=\"tokens\">{" + LUPO.format(w=250) + "}</div>\n<p>Il Lupo grigio ha 5 PV, ATT 3, AR 0 quindi Difesa 10. È di LV 1: il suo danno è D6 − 1. Lia gira il dado rosso sul 5. Per il lupo tira Marco.</p>")
s = rep(s, "<tr><td>1</td><td>Lia</td><td>9 + 3 = 12</td><td>12 ≥ 10: colpito! Danno 2 + 1 = 3. Dado rosso: da 5 a 2.</td></tr>",
        "<tr><td>1</td><td>Lia</td><td>9 + 3 = 12</td><td>12 ≥ 10: colpito! Tiro per il danno: D6 = 3. Dado rosso: da 5 a 2.</td></tr>")
s = rep(s, "<td>13 ≥ 11: colpita. Danno: esce 4, meno 1 = 3. Lia scende a 7 PV.</td>", "<td>13 ≥ 11: colpita. Danno: esce 4, meno 1 = 3. Lia scende a 10 PV.</td>")
s = rep(s, "<td>Colpito! Danno 5 + 1 = 6. Il lupo è a 0.</td>", "<td>Colpito! Danno: D6 = 5. Il lupo è a 0.</td>")
s = rep(s, "rimette il segnalino del lupo nella scatola. Il suo turno finisce.", "rimette il segnalino nella scatola; la carta del lupo va in fondo al mazzo Creature. Il suo turno finisce.")
s = rep(s, "Prima del round 2 Lia poteva anche giocare una carta, per esempio una Pozione della forza, oppure fuggire.", "Prima del round 2 Lia poteva anche giocare una carta, per esempio Grido di Battaglia (+2 al prossimo tiro per colpire), oppure fuggire.")
# p12
s = rep(s, "<tr><td><b>1</b></td><td>Tutto l’equipaggiamento</td></tr><tr><td><b>2</b></td><td>L’Elmo</td></tr><tr><td><b>3</b></td><td>L’Arma</td></tr><tr><td><b>4</b></td><td>Il Corpo</td></tr><tr><td><b>5–6</b></td><td>Niente, che fortuna!</td></tr></table>",
        "<tr><td><b>1</b></td><td>Tutto l’equipaggiamento</td></tr><tr><td><b>2</b></td><td>L’Elmo</td></tr><tr><td><b>3</b></td><td>L’Arma DX o lo Scudo</td></tr><tr><td><b>4</b></td><td>L’Arma SX</td></tr><tr><td><b>5</b></td><td>L’Armatura</td></tr><tr><td><b>6</b></td><td>Niente, che fortuna!</td></tr></table>")
s = rep(s, "<p class=\"tip\">Chierico: a 0 PV torna in vita con 3 PV e continua lo scontro.", "<p class=\"tip\">Oracolo: a 0 PV torna in vita con 4 PV e continua lo scontro.")
# p13 carte
s = rep(s, "nello slot della sua icona (<b>Elmo</b>, <b>Arma</b> o <b>Corpo</b>): resta fuori solo la fascia con nome e bonus. Sposta subito i cubetti. Se lo slot era già occupato, il vecchio oggetto va negli scarti. Massimo 1 equipaggiamento per turno. Gli scudi si impugnano: vanno nello slot <b>Arma</b>.</p>",
        "nello slot scritto sulla carta (<b>Elmo</b>, <b>Arma DX / Scudo</b>, <b>Arma SX</b> o <b>Armatura</b>): resta fuori solo la fascia con nome e bonus. Sposta subito i cubetti. Se lo slot era già occupato, il vecchio oggetto va negli scarti. Massimo 1 equipaggiamento per turno.</p>\n<h2>Le Mappe</h2>\n<p>Quando giochi una Mappa il tabellone cambia: mettila accanto alla plancia, vale per tutti finché un’altra Mappa non la sostituisce (la vecchia va negli scarti di chi l’aveva giocata). Se MIMI è già sulla plancia, <b>il tesoro cambia Cripta</b>: tira il D6 finché esce un’altra Cripta (5 e 6 si ritirano). Gli Indizi restano a tutti. Il tesoro si sposta al massimo 2 volte per partita.</p>")
s = rep(s, "<p>Le può giocare solo l’eroe di quella classe; si riconoscono dal dorso colorato. Le carte comuni le può giocare chiunque. Se una carta ha un requisito («solo se la tua pedina è un Nano»), senza requisito non si gioca.</p>",
        "<p>Le può giocare solo l’eroe della classe scritta in basso; si riconoscono dal dorso colorato. Le carte con due classi (per esempio «Guerriero - Oracolo») sono stampate in due copie, una per mazzetto. Le carte comuni («Tutte le classi») le può giocare chiunque.</p>\n<p class=\"tip\">«1D6 − 1»: tira il D6 e togli 1, minimo 1.</p>")
# p15
s = rep(s, "<li>Se una carta fa «cambiare posizione» al tesoro, ritira il D6 finché esce un’altra Cripta (5 e 6 si ritirano) e spostaci MIMI e il Guardiano. Succede al massimo 2 volte per partita; solo il Mimik lo sposta sempre.</li>",
        "<li>Se una Mappa fa cambiare Cripta al tesoro, MIMI e il Guardiano (con le sue ferite) si spostano; gli Indizi restano. Al massimo 2 volte per partita. Prima che qualcuno l’abbia individuato, il tesoro non si sposta.</li>")
s = rep(s, "<p style=\"margin-top:2mm\"><b>Varianti.</b> <i>Partita lampo</i>: ogni eroe parte con 1 Indizio. <i>In famiglia</i>: niente Duelli.</p>",
        "<p style=\"margin-top:2mm\"><b>Varianti.</b> <i>Partita lunga</i>: nessuno parte con l’Indizio. <i>In famiglia</i>: niente Duelli.</p>")
# p16 riepilogo
s = rep(s, "Colpisci se <b>D20 + ATT ≥ Difesa</b>.<br>Danno: D6 − 1 mani nude · D6 una mano · D6+1 due mani.<br>",
        "1° tiro: colpisci se <b>D20 + ATT ≥ 10 + AR</b>.<br>2° tiro, il danno: eroe D6 + bonus · nemico LV 1 D6 − 1 · LV 2 D6 · LV 3+ D6 + 1.<br>")
s = rep(s, "D6: 1 tutto · 2 elmo · 3 arma · 4 corpo · 5–6 niente", "D6: 1 tutto · 2 elmo · 3 arma DX · 4 arma SX · 5 armatura · 6 niente")
s = rep(s, "Regolamento v4.1 da tavolo", "Regolamento v5 · Carte Trama v2")
open('build.py', 'w').write(s)

t = open('inizia.py').read()
t = rep(t, "Metti i 30 segnalini Esplorazione nel sacchetto e mescolali. Guardiano, MIMI e i 4 mini-boss vanno sulle loro sagome.",
        "Metti i 30 segnalini Esplorazione nel sacchetto e mescolali. Mescola i mazzi Creatura e Mini-boss. Guardiano, MIMI e i 4 mini-boss vanno sulle loro sagome.")
t = rep(t, "Dalla Galleria: Guerriero, Ladro, Mago o Chierico, con il mazzetto dello stesso colore (non guardare le carte). Poi una Tessera Specie: Umano, Elfo, Nano o Orco.",
        "Dalla Galleria: Guerriero, Ladro, Mago o Oracolo, con il mazzetto dello stesso colore (non guardare le carte). Poi una Tessera Specie: Umano, Elfo, Nano, Orco o Sanguar.")
t = rep(t, "Aggiungi il bonus della specie. Infila la Carta Classe nel primo slot.", "Aggiungi il bonus della specie. Infila la Carta Classe nel primo slot e metti 1 Indizio sulla scheda.")
t = rep(t, "5 carte della tua classe + 5 comuni, coperte.", "3 carte della tua classe + 7 comuni, coperte.")
t = rep(t, "{token('Lupo grigio',5,'+3',10,'D6−1',120)}", "{enemy_card('Lupo grigio','L',1,5,3,0,['1 indizio','1 punto esperienza'],w=260)}")
t = rep(t, "<p><b>1.</b> Tira il <b>D20 + il tuo ATT</b>. Se arrivi alla <b>Difesa</b> del mostro (qui 10) lo colpisci: tira il danno (D6 − 1 a mani nude, minimo 1; D6 con un’arma, D6+1 con un’arma a due mani).</p>\n<p><b>2.</b> Ora l’avversario tira per il mostro: D20 + ATT del mostro contro la tua Difesa. Se ti colpisce, tira il suo danno.</p>",
        "<p>Pesca il segnalino: dice <b>Creatura</b>? Gira la prima carta Creatura.</p>\n<p><b>1.</b> <b>Tiro per colpire</b>: D20 + il tuo ATT. Se arrivi alla <b>Difesa</b> del mostro (10 + AR, qui 10) lo colpisci. <b>Tiro per il danno</b>: D6, più i bonus delle tue carte.</p>\n<p><b>2.</b> Ora l’avversario tira per il mostro: D20 + ATT del mostro contro la tua Difesa. Se ti colpisce, tira il suo danno: D6 − 1 al LV 1, D6 al LV 2, D6 + 1 dal LV 3.</p>")
open('inizia.py', 'w').write(t)
print('ok')
