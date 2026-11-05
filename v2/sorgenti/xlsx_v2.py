# Catalogo Excel v2: carte Trama v2 adattate alla scatola + carte Nemico + bilanciamento
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
cards = json.load(open('cards_v2.json')); nem = json.load(open('nemici_v2.json'))
out = sys.argv[1]
wb = Workbook()
H = Font(bold=True, color='FFFFFF'); HF = PatternFill('solid', fgColor='3B2A1A')
COL = {'TM': 'F6D5D1', 'TE': 'D6EED8', 'TI': 'D5DEF5', 'TC': 'E6D8F2', 'NE': 'F3E7C9'}
thin = Side(style='thin', color='BBBBBB'); B = Border(top=thin, bottom=thin, left=thin, right=thin)
W = Alignment(wrap_text=True, vertical='top')
def sheet(ws, head, rows, widths, fill=None, changed_col=None):
    ws.append(head)
    for c in ws[1]: c.font = H; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical='center')
    for r in rows: ws.append(r)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = W; c.border = B
            if fill: c.fill = PatternFill('solid', fgColor=fill)
        if changed_col is not None and row[changed_col].value:
            row[changed_col].font = Font(bold=True, color='8A2B0E')
    ws.freeze_panes = 'C2'; ws.auto_filter.ref = ws.dimensions

ws = wb.active; ws.title = 'Leggimi'
L = [
 ['Il Tesoro del Goblin · un gioco di Alessandro De Simone · Catalogo v2 (27/10/2026)'],
 ['Base: i file delle Carte Trama v2 di Alessandro De Simone, autore del gioco, caricati il 27/10 (Carte_Trama_Il_Tesoro_del_Goblin_v2.pptx, Carte_Trama_Elenco_v2.xlsx, Layout_Carta_Nemico_Canva.pptx). Le 68 carte nuove sostituiscono le 108 della versione del 21/10.'],
 [''],
 ['Scelte confermate da Daniele (27/10 ore 18:29)'],
 ['1. Mazzo: 8 Mappe, 20 Equipaggiamenti, 40 Incantesimi + 4 carte Classe (Guerriero, Ladro, Mago, Oracolo).'],
 ["2. L'Oracolo prende il posto del Chierico (torna in vita in scontro, dal 2/11 si ricarica pescando una Locanda dal sacchetto)."],
 ['3. Combattimento in due tiri: per colpire D20 + ATT ≥ 14 + AR (anche i nemici; 20 naturale critico, 1 naturale mancato; dal 27/10 colpire è il 20% più difficile: era 10 + AR); poi il danno: eroi D6 + bonus delle carte, nemici D6 − 1 al LV 1, D6 al LV 2, D6 + 1 dal LV 3.'],
 ['4. Niente D4: 1D4 → 1D6 − 1 (minimo 1).'],
 ['5. 4 slot: Elmo, Arma DX / Scudo, Arma SX, Armatura. Perdita D6: 1 tutto, 2 Elmo, 3 Arma DX, 4 Arma SX, 5 Armatura, 6 niente.'],
 ['6. Mappe: il tesoro cambia Cripta ma gli Indizi restano; al massimo 2 volte per partita; una sola Mappa attiva.'],
 [''],
 ['Regole e ritocchi del 27/10 (Indizi, mano, nemici e punti vita decisi da Daniele; ritocchi delle classi da confermare)'],
 ['• Indizi solo vincendo uno scontro su una casella esplorazione o un Duello; nessuno parte con un Indizio (Daniele 27/10). Servono 2 Indizi per individuare il tesoro e resta «la voce si sparge» (scelta di Daniele 27/10). Sacchetto: 19 Nemico I, 6 Nemico II, 5 Trappole. Niente Presagio. Con 3 Indizi la partita durava 33/44/54 minuti.'],
 ['• Punti vita (Daniele 27/10): si parte da 5 PV e crescono solo salendo di livello (+1 ad ATT, MOV o AR oppure +2 PV); il Guerriero ha +2 PV. Le specie non danno più PV (Orco +2 ATT, Sanguar +2 MOV, Yumaniani +1 AR e +1 a scelta). Per tenere la durata (5 PV e colpi più difficili): nemici I, II e mini-boss −2 PV (minimo 1), boss −5 PV.'],
 ['• Sacchetto a due colori (Daniele 2/11): 25 tessere rosse (Mostro) e 11 blu (Imprevisto), 36 caselle «?» (Locanda, Fonte e Fabbro non sono più stampati sulla plancia). Rossa: si gira la prima carta del mazzetto Mostri del livello dell’eroe (livello 1-2 → mazzetto 1, LV 1-2; 3-4 → mazzetto 2, LV 3-4; 5 → mazzetto 3, i boss). Blu: si gira la prima carta del mazzetto Imprevisti (5 Trappole, 2 Locande, 2 Fonti, 2 Fabbri), che poi va in fondo. Niente mini-boss. Uno dei 3 boss, pescato a inizio partita, custodisce MIMI.'],
 ['• Carte (Daniele 27/10): massimo 2 per turno, a inizio turno, durante uno scontro o a fine turno; equipaggiamenti solo a inizio turno, uno per turno.'],
 ['• Ladro +2 MOV (era +3) e senza vantaggio nel primo round (tiene la fuga senza arretrare); Mago ritira 2 dadi per turno (era 1); Oracolo torna in vita con 3 PV.'],
 ['• Mano, due modalità a scelta dei giocatori (Daniele 27/10): pescata casuale 5 di classe + 5 comuni (il Mago ha solo 4 carte sue e pesca 6 comuni), oppure 3 carte di classe scelte + 7 comuni draftate (pescane 7, tienine 1, passa a sinistra).'],
 [''],
 ['Risultati con 5 PV di partenza e Difesa 14 + AR (simulatore IA, 10.000 partite per numero di giocatori e per modalità della mano, tempi a ritmo da tavolo)'],
 ['Pescata casuale 5 + 5 · 2 giocatori: 22,9 min · Guerriero 1,04 | Mago 1,02 | Oracolo 1,01 | Ladro 0,93'],
 ['Pescata casuale 5 + 5 · 3 giocatori: 27,0 min · Guerriero 1,04 | Ladro 0,99 | Mago 0,99 | Oracolo 0,98'],
 ['Pescata casuale 5 + 5 · 4 giocatori: 30,8 min · Ladro 1,03 | Guerriero 1,01 | Oracolo 1,00 | Mago 0,96'],
 ['Scelta e draft 3 + 7 · 2 giocatori: 22,2 min · Guerriero 1,04 | Oracolo 1,03 | Mago 1,00 | Ladro 0,92'],
 ['Scelta e draft 3 + 7 · 3 giocatori: 26,1 min · Oracolo 1,05 | Guerriero 1,02 | Mago 0,97 | Ladro 0,95'],
 ['Scelta e draft 3 + 7 · 4 giocatori: 29,2 min · Oracolo 1,09 | Guerriero 1,00 | Ladro 0,99 | Mago 0,92'],
 ['Pescata casuale, con i mini-boss · 2 giocatori: 23,2 min · Guerriero 1,02 | Oracolo 1,02 | Mago 1,00 | Ladro 0,96'],
 ['Pescata casuale, con i mini-boss · 3 giocatori: 27,5 min · Guerriero 1,02 | Oracolo 1,02 | Ladro 0,99 | Mago 0,98'],
 ['Pescata casuale, con i mini-boss · 4 giocatori: 31,2 min · Ladro 1,05 | Guerriero 1,02 | Oracolo 1,00 | Mago 0,93'],
 ['Il draft aggiunge circa 2 minuti di preparazione. Le differenze di ±0,04 rientrano nel margine statistico.'],
 ['(1,00 = vince quanto atteso. Specie tra 0,93 e 1,06; Sanguar arriva a 1,14 con i mini-boss in 4.)'],
 [''],
 ['Colonne: «Testo originale» = testo dell’autore, Alessandro De Simone; «Testo scatola» = testo proposto; «Modifica» in rosso = perché è cambiato. Tutti gli effetti restano DA APPROVARE come nel file originale.'],
]
for r in L: ws.append(r)
ws.column_dimensions['A'].width = 150
for r in (1, 4, 12, 17): ws.cell(r, 1).font = Font(bold=True, size=13 if r == 1 else 11)
for row in ws.iter_rows(): row[0].alignment = Alignment(wrap_text=True)

head = ['ID', 'Nome', 'Rarità', 'Classe', 'Slot', 'Testo scatola', 'Testo originale (A. De Simone)', 'Modifica', 'Origine']
for tipo, title in (('TM', 'Mappe'), ('TE', 'Equipaggiamento'), ('TI', 'Incantesimi'), ('TC', 'Classi')):
    rows = [[c['id'], c['nome'], c['rarita'], c['classe'], c['slot'], c['testo'], c['testo_originale'], c['modifica'] if c['testo'] != c['testo_originale'] or c['tipo'] == 'TC' else '', c['origine']] for c in cards if c['tipo'] == tipo]
    sheet(wb.create_sheet(title), head, rows, [8, 24, 11, 18, 15, 55, 55, 40, 18], COL[tipo], changed_col=7)
TIPO2 = {'Nemico I': 'Mazzetto 1', 'Nemico II': 'Mazzetto 2', 'Boss': 'Boss (custode o mazzetto 3)'}
rows = [[n['id'], n['lettera'], n['nome'], TIPO2.get(n['tipo'], n['tipo']), n['lv'], n['pv'], n['att'], n['ar'], n['difesa'], n['danno'], n['abilita'], n['ricompense'].replace('\n', ' · '), n['origine']] for n in nem if n['tipo'] != 'Mini-boss']
sheet(wb.create_sheet('Nemici'), ['ID', 'Simbolo', 'Nome', 'Tipo', 'LV', 'PV', 'ATT', 'AR', 'Difesa (10+AR)', 'Danno (dal LV)', 'Abilità speciali', 'Ricompense', 'Origine'], rows, [8, 8, 22, 11, 5, 5, 5, 5, 9, 10, 30, 32, 20], COL['NE'])
ws = wb['Nemici']; ws.append([]); ws.append(['', '', 'Mostri a livelli (Daniele 2/11): la tessera rossa fa girare la prima carta del mazzetto del livello dell’eroe. Mazzetto 1 = LV 1-2 (13 carte), mazzetto 2 = LV 3-4 (8 carte, danno anche l’Ispirazione), mazzetto 3 = i 2 boss che non custodiscono MIMI (LV 5; vinci: 1 Indizio, sali di livello, Ispirazione). I 4 mini-boss sono stati tolti.'])
IMP = [('IM-01', 'Trappola', 5, 'Perdi D6 − 1 PV (minimo 1), poi tira il D6 della perdita di equipaggiamento.'), ('IM-02', 'Locanda', 2, '+1 PE e recuperi 2 PV. L’Oracolo ricarica il ritorno in vita.'), ('IM-03', 'Fonte', 2, 'Riprendi in mano fino a 2 carte dai tuoi scarti.'), ('IM-04', 'Fabbro', 2, 'Riprendi 1 equipaggiamento dai tuoi scarti.')]
sheet(wb.create_sheet('Imprevisti'), ['ID', 'Nome', 'Copie', 'Effetto'], [list(x) for x in IMP], [8, 16, 8, 70], COL['TM'])
ws = wb['Imprevisti']; ws.append([]); ws.append(['', 'Mazzetto Imprevisti (Daniele 2/11): si gira la prima carta quando si pesca una tessera blu; dopo l’effetto va in fondo al mazzetto.'])
wb.save(out)
print('ok')
