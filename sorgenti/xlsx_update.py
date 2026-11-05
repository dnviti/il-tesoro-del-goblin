import json,openpyxl,copy
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.datavalidation import DataValidation
SRC='/mnt/project-files/tesoro-goblin/Catalogo_carte_Tesoro_del_Goblin.xlsx'
OUT='Catalogo_carte_Tesoro_del_Goblin.xlsx'
cards=json.load(open('cards.json')); before=json.load(open('before_texts.json'))
inuse=lambda k: k['testo_rimodulato'] or k['testo']
wb=openpyxl.load_workbook(SRC)
ws=wb['Carte']
hdr=[c.value for c in ws[1]]
ws['N1']='Testo in uso (dopo il bilanciamento del 21/10)'
ws['O1']='Bilanciamento 21/10 (motivo)'
for a in ['font','fill','alignment','border']: setattr(ws['O1'],a,copy.copy(getattr(ws['N1'],a)))
ws.column_dimensions['O'].width=60
rowof={ws.cell(r,1).value:r for r in range(2,ws.max_row+1)}
tmpl=2
keys=['id','nome','tipo','categoria','testo','requisito','razze_classi','slot','statistiche','foto','refusi','note','mazzo']
for k in cards:
    r=rowof.get(k['id'])
    if r is None:
        r=ws.max_row+1; rowof[k['id']]=r
        for col in range(1,16):
            s=ws.cell(tmpl,col); d=ws.cell(r,col)
            for a in ['font','fill','alignment','border','number_format']: setattr(d,a,copy.copy(getattr(s,a)))
    for i,key in enumerate(keys,1): ws.cell(r,i).value=k.get(key) or None
    ws.cell(r,14).value=k['testo_rimodulato'] or None
    ws.cell(r,15).value=k.get('bilanciamento') or None
    ws.cell(r,15).alignment=copy.copy(ws.cell(r,14).alignment)
last=ws.max_row
if ws.auto_filter.ref: ws.auto_filter.ref=f"A1:O{last}"
# Riepilogo / Mazzo formulas
for name in ['Riepilogo','Mazzo']:
    for row in wb[name].iter_rows():
        for c in row:
            if isinstance(c.value,str) and '$99' in c.value: c.value=c.value.replace('$99',f'${last}')
dvs=wb['Mazzo'].data_validations.dataValidation
for dv in dvs: dv.formula1=f'=Carte!$B$2:$B${last}'
# Mazzi sheet: rebuild body
wm=wb['Mazzi']
st={col:{a:copy.copy(getattr(wm.cell(5,col),a)) for a in ['font','fill','alignment','border']} for col in range(1,6)}
for row in wm.iter_rows(min_row=5,max_row=wm.max_row):
    for c in row: c.value=None
wm['A2']="Ogni giocatore gioca la sua carta Classe a inizio partita, poi pesca 5 carte a caso dal mazzetto della sua classe (7 carte, compresa la carta leggendaria) e 5 dal mazzo comune."
groups={}
for k in cards:
    if k['tipo']=='TC': continue
    groups.setdefault(k['mazzo'],[]).append(k)
order=sorted([g for g in groups if g.startswith('Classe')])+['Comune']
r=5
for g in order:
    for i,k in enumerate(groups[g]):
        vals=[g if i==0 else None, len(groups[g]) if i==0 else None, k['id'], k['nome'], inuse(k)]
        for col,v in enumerate(vals,1):
            c=wm.cell(r,col); c.value=v
            for a,s in st[col].items(): setattr(c,a,copy.copy(s))
        r+=1
# Prima e dopo
if 'Prima e dopo' in wb.sheetnames: del wb['Prima e dopo']
wp=wb.create_sheet('Prima e dopo', 2)
wp.append(['ID','Nome','Mazzo','Prima','Dopo','Motivo'])
for c in wp[1]:
    for a in ['font','fill','alignment','border']: setattr(c,a,copy.copy(getattr(ws['A1'],a)))
for k in cards:
    if not k.get('bilanciamento'): continue
    new = k['tipo']=='TI' and k['id']>='TI-57'
    wp.append([k['id'],k['nome'],k['mazzo'].replace('Carta classe (si gioca a inizio partita)','Carta classe'),'(carta nuova)' if new else before.get(k['id'],''),inuse(k),k['bilanciamento']])
for col,w in zip('ABCDEF',[8,26,18,60,60,55]): wp.column_dimensions[col].width=w
for row in wp.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
wp.freeze_panes='C2'; wp.auto_filter.ref=f"A1:F{wp.max_row}"
# Legenda
wl=wb['Legenda']
wl['B8']='10 foto (1000065148–157) + Regolamento v3. 98 carte trascritte + 10 carte leggendarie nuove (TI-57…TI-66) del 21/10/2026.'
nr=wl.max_row+1
have=any(wl.cell(r,1).value=='Bilanciamento 21/10' for r in range(1,wl.max_row+1))
for i,(a,b) in enumerate([] if have else [('Bilanciamento 21/10','Motivo della modifica decisa dopo migliaia di partite simulate. Il foglio «Prima e dopo» mostra il testo precedente e quello nuovo.'),('Carta leggendaria','Una per classe (TI-57…TI-66): carta molto forte e specifica della classe, una sola copia nel mazzetto.')]):
    wl.cell(nr+i,1).value=a; wl.cell(nr+i,2).value=b
    for col in (1,2):
        for at in ['font','fill','alignment','border']: setattr(wl.cell(nr+i,col),at,copy.copy(getattr(wl.cell(nr-1,col),at)))
wb.save(OUT)
print('saved',last,wp.max_row-1)
