# dopo xlsx_update.py: formule estese alle righe delle carte Caos e blocco del mazzo dell'espansione nel foglio Mazzi
import openpyxl, json, re, copy
P = 'Catalogo_carte_Tesoro_del_Goblin.xlsx'
wb = openpyxl.load_workbook(P)
last = wb['Carte'].max_row
for n in wb.sheetnames:
    if n == 'Carte': continue
    for row in wb[n].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='): c.value = re.sub(r'\$(\d{3})\b', lambda m: '$%d' % last if int(m.group(1)) >= 100 else m.group(0), c.value)
for dv in wb['Mazzo'].data_validations.dataValidation:
    if dv.formula1: dv.formula1 = re.sub(r'\$(\d{3})\b', lambda m: '$%d' % last if int(m.group(1)) >= 100 else m.group(0), dv.formula1)
ws = wb['Mazzi']
if not any(ws.cell(r, 1).value == 'Comune (espansione Caos)' for r in range(1, ws.max_row + 1)):
    cards = [c for c in json.load(open('cards.json')) if c['id'].startswith('CA-')]
    src = ws.max_row
    for i, c in enumerate(cards):
        r = ws.max_row + 1
        vals = ['Comune (espansione Caos)' if i == 0 else None, len(cards) if i == 0 else None, c['id'], c['nome'], c['testo']]
        for j, v in enumerate(vals, 1):
            ws.cell(r, j, v); ws.cell(r, j)._style = copy.copy(ws.cell(src, j)._style)
wb.save(P); print('ok', last)
