#!/usr/bin/env python3
"""Genera lo script DesignCraft del regolamento «Il Tesoro del Goblin» (vedi LEGGIMI.md).

Uso: python3 genera.py measure|final > script.txt   (file di lavoro in $WORK)"""
import json, re, sys, os

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
WORK = os.environ.get('WORK', SRC)
VET = ROOT + '/vettoriali'
PNG = ROOT + '/immagini/png'
DER = ROOT + '/immagini/derivati'
SCH = ROOT + '/schemi'
W, H = 595.28, 841.89
L, R = 40.0, 555.28
C1 = (40.0, 290.0)
C2 = (305.28, 555.28)

cmds = []
def cmd(cid, params=None):
    cmds.append(cid + (' ' + json.dumps(params, ensure_ascii=False) if params is not None else ''))
    return len(cmds) - 1

# ---------------------------------------------------------------- text source
def inline(s):
    s = s.replace("'", '’')
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: '⟪' + m.group(1) + '⟫', s)
    s = s.replace('`', '')
    return s

def parse():
    t = open(ROOT + '/testo_manuale.md', encoding='utf-8').read()
    pages = {}
    cur = None
    for line in t.splitlines():
        m = re.match(r'^## Pagina (\d)', line)
        if m:
            cur = int(m.group(1)); pages[cur] = []; continue
        if line.startswith('## '):
            cur = None; continue
        if cur is None: continue
        pages[cur].append(line)
    out = {}
    for p, lines in pages.items():
        blocks = []
        i = 0
        while i < len(lines):
            l = lines[i].rstrip()
            if not l.strip(): i += 1; continue
            if l.startswith('### '):
                blocks.append(('h3', inline(l[4:]))); i += 1; continue
            if l.startswith('# '):
                blocks.append(('h1', inline(l[2:]))); i += 1; continue
            if l.startswith('['):
                blocks.append(('marker', l)); i += 1; continue
            if re.match(r'^\*[^*].*[^*]\*$', l):
                blocks.append(('italic', inline(l[1:-1]))); i += 1; continue
            if l.startswith('> '):
                blocks.append(('quote', inline(l[2:]))); i += 1; continue
            if l.startswith('|'):
                rows = []
                while i < len(lines) and lines[i].startswith('|'):
                    if not re.match(r'^\|[-| ]+\|$', lines[i]):
                        rows.append([inline(c.strip()) for c in lines[i].strip().strip('|').split('|')])
                    i += 1
                blocks.append(('table', rows)); continue
            if re.match(r'^\d+\. ', l):
                items = []
                while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                    items.append(inline(re.sub(r'^\d+\. ', '', lines[i]))); i += 1
                blocks.append(('ol', items)); continue
            if l.startswith('- '):
                items = []
                while i < len(lines) and lines[i].startswith('- '):
                    items.append(inline(lines[i][2:])); i += 1
                blocks.append(('ul', items)); continue
            blocks.append(('p', inline(l))); i += 1
        out[p] = blocks
    return out

TXT = parse()


def section(page, heading):
    """Blocks from ### heading up to the next ### (heading included)."""
    bl = TXT[page]
    for k, b in enumerate(bl):
        if b[0] == 'h3' and b[1] == heading:
            res = [b]
            for b2 in bl[k + 1:]:
                if b2[0] == 'h3': break
                res.append(b2)
            return res
    raise KeyError((page, heading))

def strip_markers(blocks):
    return [b for b in blocks if b[0] != 'marker']

# ---------------------------------------------------------------- document
ACC = {1: 'Rosso', 2: 'Oro', 3: 'Rosso', 4: 'Blu', 5: 'Verde'}

def setup():
    cmd('file.new', {"preset": "A4", "pages": 5, "facingPages": False, "margins": {"top": 40, "bottom": 40, "inside": 40, "outside": 40},
                     "columns": 2, "gutter": 15.28, "bleed": 9, "intent": "print", "title": "Il Tesoro del Goblin – Regolamento"})
    sw = dict(Carta='#f9f2e0', Inchiostro='#2a2118', Ottone='#a8823a', Rosso='#9c2f24', Marrone='#6b4a2b', Oro='#b8862b',
              OroChiaro='#f6d68b', OttoneChiaro='#e8cd8f', Pergamena='#f1dcae', Blu='#2f5d7c', Verde='#3d6f45', Viola='#7a4f86')
    for k, v in sw.items():
        cmd('swatch.create', {"name": k, "color": v})
    # character styles
    cmd('style.character.create', {"name": "Forte", "chars": {"fontStyle": "Bold"}})
    cmd('style.character.create', {"name": "Simboli", "chars": {"fontFamily": "IBM Plex Sans Condensed"}})
    cmd('style.character.create', {"name": "Punto elenco", "chars": {"fontFamily": "Noto Serif", "fontStyle": "Bold", "fill": "Ottone"}})
    cmd('style.character.create', {"name": "Etichetta consiglio", "chars": {"fontFamily": "IBM Plex Sans Condensed", "fontStyle": "Bold", "fill": "Rosso", "tracking": 20}})
    cmd('style.character.create', {"name": "Accento copertina", "chars": {"fontFamily": "IBM Plex Sans Condensed", "fontStyle": "Bold", "fill": "Rosso"}})
    grep = [{"style": "Simboli", "pattern": "[→≥≤]"}]
    body = {"language": "Italian", "fontFamily": "Noto Serif", "fontStyle": "Regular", "size": 12, "leading": {"kind": "points", "value": 15.5}, "fill": "Inchiostro"}
    cmd('style.paragraph.create', {"name": "Corpo", "para": {"align": "left", "hyphenate": True, "spaceAfter": 4, "keepFirst": 2, "keepLast": 2, "grepStyles": grep}, "chars": body})
    cmd('style.paragraph.create', {"name": "Elenco", "basedOn": "Corpo", "para": {"listType": "bullets", "bulletChar": "•", "bulletCharStyle": "Punto elenco", "hyphenate": False,
                                   "leftIndent": 14, "firstLineIndent": -14, "spaceAfter": 3, "listTab": 14}})
    cmd('style.paragraph.create', {"name": "Passo", "basedOn": "Corpo", "para": {"leftIndent": 30, "spaceAfter": 3}})
    cmd('style.paragraph.create', {"name": "Sottotitolo", "basedOn": "Corpo",
                                   "para": {"spaceBefore": 9, "spaceAfter": 4, "keepWithNext": 2, "leftIndent": 28, "hyphenate": False},
                                   "chars": {"fontStyle": "Bold", "size": 15.5, "leading": {"kind": "points", "value": 18}, "tracking": -5}})
    cmd('style.paragraph.create', {"name": "Testata", "basedOn": "Corpo", "para": {"align": "center", "spaceAfter": 0, "hyphenate": False},
                                   "chars": {"fontStyle": "Bold", "size": 23, "leading": {"kind": "points", "value": 26}, "tracking": -10}})
    for a in sorted(set(ACC.values())):
        cmd('style.paragraph.create', {"name": "Sottotitolo " + a, "basedOn": "Sottotitolo", "chars": {"fill": a}})
        cmd('style.paragraph.create', {"name": "Testata " + a, "basedOn": "Testata", "chars": {"fill": a}})
    cmd('style.paragraph.create', {"name": "Testatina corrente", "para": {"align": "center", "hyphenate": False},
                                   "chars": {"fontFamily": "IBM Plex Sans Condensed", "fontStyle": "Medium", "size": 9.5, "leading": {"kind": "points", "value": 12},
                                             "tracking": 80, "fill": "Marrone", "capitalization": "allCaps"}})
    cmd('style.paragraph.create', {"name": "Folio", "para": {"align": "center", "hyphenate": False},
                                   "chars": {"fontFamily": "Noto Serif", "fontStyle": "Bold", "size": 10.5, "leading": {"kind": "points", "value": 12}, "fill": "Inchiostro"}})
    cmd('style.paragraph.create', {"name": "Titolo copertina", "para": {"align": "center", "hyphenate": False},
                                   "chars": {"fontFamily": "Noto Serif", "fontStyle": "Bold", "size": 60, "leading": {"kind": "points", "value": 60}, "tracking": -15, "fill": "Inchiostro"}})
    cmd('style.paragraph.create', {"name": "Sottotitolo copertina", "para": {"align": "center", "hyphenate": False},
                                   "chars": {"fontFamily": "IBM Plex Sans Condensed", "fontStyle": "Regular", "size": 13.5, "leading": {"kind": "points", "value": 17}, "fill": "Marrone", "tracking": 10}})
    cmd('style.paragraph.create', {"name": "Consiglio", "basedOn": "Corpo", "para": {"spaceAfter": 0, "hyphenate": False},
                                   "chars": {"fontStyle": "Italic", "size": 14, "leading": {"kind": "points", "value": 17.5}}})
    cmd('style.paragraph.create', {"name": "Aggancio", "basedOn": "Corpo", "para": {"spaceBefore": 4},
                                   "chars": {"fontStyle": "Italic", "fill": "Marrone"}})
    cmd('style.paragraph.create', {"name": "Chiusura", "basedOn": "Corpo", "para": {"align": "center", "spaceAfter": 0, "hyphenate": False},
                                   "chars": {"fontStyle": "Italic", "size": 14, "leading": {"kind": "points", "value": 18}, "fill": "Verde"}})
    for w in ("Indizi", "Indizio"):
        cmd('hyphenation.addException', {"word": w})
    cmd('style.paragraph.create', {"name": "Tabella", "para": {"align": "left", "hyphenate": False, "grepStyles": []},
                                   "chars": {"language": "Italian", "fontFamily": "IBM Plex Sans Condensed", "fontStyle": "Regular", "size": 11, "leading": {"kind": "points", "value": 13.5}, "fill": "Inchiostro"}})
    cmd('style.paragraph.create', {"name": "Tabella voce", "basedOn": "Tabella", "chars": {"fontStyle": "Bold"}})
    cmd('style.paragraph.create', {"name": "Tabella intestazione", "basedOn": "Tabella",
                                   "chars": {"fontStyle": "SemiBold", "fill": "Marrone", "capitalization": "allCaps", "tracking": 40}})
    cmd('style.paragraph.create', {"name": "Tabella contenitore", "basedOn": "Corpo", "para": {"spaceBefore": 2, "spaceAfter": 2},
                                   "chars": {"size": 2, "leading": {"kind": "points", "value": 2}}})
    stroke = {"weight": 0.6, "color": "Ottone"}
    cmd('style.cell.create', {"name": "Cella intestazione", "fill": "Pergamena", "insets": [3, 6, 2.5, 6], "vj": "center", "stroke": stroke, "paragraphStyle": "Tabella intestazione"})
    cmd('style.cell.create', {"name": "Cella", "insets": [3, 6, 2.5, 6], "vj": "center", "stroke": stroke, "paragraphStyle": "Tabella"})
    cmd('style.cell.create', {"name": "Cella voce", "basedOn": "Cella", "paragraphStyle": "Tabella voce"})
    cmd('style.table.create', {"name": "Tabella ottone", "header": "Cella intestazione", "body": "Cella", "leftColumn": "Cella voce",
                               "border": {"weight": 1.2, "color": "Ottone"}, "spaceBefore": 0, "spaceAfter": 0})

def place(path, rect, spread, fit='fitContentToFrame', label=None, stroke=None):
    i = cmd('frame.create', {"spread": spread, "rect": rect, "shape": "rectangle", "content": "graphic"})
    if path:
        cmd('file.place', {"path": path, "frame": "$%d.id" % i})
        cmd('object.fit', {"mode": fit, "ids": ["$%d.id" % i]})
    if label:
        cmd('object.label', {"label": label, "ids": ["$%d.id" % i]})
    if stroke:
        cmd('object.stroke', dict(stroke, ids=["$%d.id" % i]))
    else:
        cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % i]})
    return i

def parents():
    PA = {"kind": "parent", "index": 0}
    r = cmd('frame.create', {"spread": PA, "rect": [-9, -9, W + 9, H + 9], "shape": "rectangle", "content": "graphic"})
    cmd('object.fill', {"swatch": "Carta", "ids": ["$%d.id" % r]})
    cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % r]})
    place(VET + '/cornice_pagina.pdf', [0, 0, W, H], PA)
    t = cmd('frame.create', {"spread": PA, "rect": [L, 40, R, 53], "content": "text", "text": "Il Tesoro del Goblin  ·  Regolamento"})
    cmd('selection.set', {"ids": ["$%d.id" % t]}); cmd('style.paragraph.apply', {"name": "Testatina corrente"})
    cx = W / 2
    place(DER + '/ingranaggio_vuoto.svg', [cx - 15, 771, cx + 15, 801], PA)
    f = cmd('frame.create', {"spread": PA, "rect": [cx - 15, 771, cx + 15, 801], "content": "text", "text": "\ue000"})
    cmd('selection.set', {"ids": ["$%d.id" % f]}); cmd('style.paragraph.apply', {"name": "Folio"})
    cmd('object.textFrameOptions', {"verticalJustification": "center", "inset": 0, "ids": ["$%d.id" % f]})
    # cover parent
    cmd('layout.parents.new', {"prefix": "B", "name": "Copertina"})
    PB = {"kind": "parent", "index": 1}
    r = cmd('frame.create', {"spread": PB, "rect": [-9, -9, W + 9, H + 9], "shape": "rectangle", "content": "graphic"})
    cmd('object.fill', {"swatch": "Carta", "ids": ["$%d.id" % r]})
    cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % r]})
    place(VET + '/cornice_pagina_copertina.pdf', [0, 0, W, H], PB)
    cmd('layout.pages.applyParent', {"pages": [1, 2, 3, 4], "parent": "A-Parent"})
    cmd('layout.pages.applyParent', {"pages": [0], "parent": "B-Copertina"})

ICON = {}
def badge(n, spread):
    """Return command index of an item to anchor as step badge n (24 pt)."""
    if n <= 8:
        i = cmd('frame.create', {"spread": spread, "rect": [0, 0, 24, 24], "shape": "rectangle", "content": "graphic"})
        cmd('file.place', {"path": VET + '/numeri_passo_%d.pdf' % n, "frame": "$%d.id" % i})
        cmd('object.fit', {"mode": "fitContentToFrame", "ids": ["$%d.id" % i]})
        cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % i]})
        return i, 'id'
    g = cmd('frame.create', {"spread": spread, "rect": [0, 0, 24, 24], "shape": "rectangle", "content": "graphic"})
    cmd('file.place', {"path": DER + '/ingranaggio_vuoto.svg', "frame": "$%d.id" % g})
    cmd('object.fit', {"mode": "fitContentToFrame", "ids": ["$%d.id" % g]})
    cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % g]})
    t = cmd('frame.create', {"spread": spread, "rect": [0, 4, 24, 20], "content": "text", "text": str(n)})
    cmd('selection.set', {"ids": ["$%d.id" % t]})
    cmd('type.char', {"attrs": {"fontFamily": "Noto Serif", "fontStyle": "Bold", "size": 10, "tracking": -40, "fill": "Inchiostro"}})
    cmd('type.para', {"attrs": {"align": "center"}})
    cmd('object.textFrameOptions', {"verticalJustification": "center", "inset": 0, "ids": ["$%d.id" % t]})
    o = cmd('type.createOutlines', {"ids": ["$%d.id" % t]})
    cmd('selection.set', {"ids": ["$%d.id" % g, "$%d.ids.0" % o]})
    gi = cmd('object.group', {})
    return gi, 'id'

def icon(name, spread):
    i = cmd('frame.create', {"spread": spread, "rect": [0, 0, 22, 22], "shape": "rectangle", "content": "graphic"})
    cmd('file.place', {"path": VET + '/ic_%s.pdf' % name, "frame": "$%d.id" % i})
    cmd('object.fit', {"mode": "fitContentToFrame", "ids": ["$%d.id" % i]})
    cmd('object.stroke', {"swatch": "[None]", "ids": ["$%d.id" % i]})
    return i

def textframe(spread, rect, blocks, acc, icons=None, cols=None, label=None):
    """blocks -> one story. icons: {heading: icon name}. cols: table column widths."""
    icons = icons or {}
    paras = []   # (style, text, extra)
    for b in blocks:
        k = b[0]
        if k == 'h3':
            paras.append(('Sottotitolo ' + acc, b[1], ('icon', icons.get(b[1]))))
        elif k == 'p':
            paras.append(('Corpo', b[1], None))
        elif k == 'ul':
            for it in b[1]: paras.append(('Elenco', it, None))
        elif k == 'ol':
            for n, it in enumerate(b[1], 1): paras.append(('Passo', it, ('badge', n)))
        elif k == 'table':
            paras.append(('Tabella contenitore', '', ('table', b[1])))
        elif k == 'quote':
            paras.append(('Consiglio', b[1], None))
        elif k == 'italic':
            paras.append(('Aggancio', b[1], None))
        elif k == 'raw':
            paras.append((b[1], b[2], None))
    text = '\n'.join(p[1] for p in paras)
    f = cmd('frame.create', {"spread": spread, "rect": rect, "content": "text", "text": text})
    if label:
        cmd('object.label', {"label": label, "ids": ["$%d.id" % f]})
    st = "$%d.story" % f
    offs = []
    pos = 0
    for p in paras:
        n = len(p[1].encode('utf-8'))
        offs.append((pos, pos + n))
        pos += n + 1
    for (a, b_), p in zip(offs, paras):
        cmd('text.select', {"story": st, "anchor": a, "focus": b_})
        cmd('style.paragraph.apply', {"name": p[0], "clearOverrides": True})
    # inserts from last to first so offsets stay valid
    for (a, b_), p in reversed(list(zip(offs, paras))):
        ex = p[2]
        if not ex: continue
        if ex[0] == 'table':
            rows = ex[1]
            cmd('text.select', {"story": st, "anchor": a, "focus": a})
            ti = cmd('table.insert', {"rows": len(rows) - 1, "cols": len(rows[0]), "headerRows": 1, "tableStyle": "Tabella ottone"})
            for r, row in enumerate(rows):
                for c, cell in enumerate(row):
                    cmd('table.setCell', {"story": st, "table": "$%d.table" % ti, "row": r, "col": c, "text": cell})
            if cols:
                for c, wdt in enumerate(cols):
                    cmd('table.setColumnWidth', {"story": st, "table": "$%d.table" % ti, "col": c, "width": wdt})
        elif ex[0] == 'badge':
            gi, key = badge(ex[1], spread)
            cmd('anchored.insert', {"ids": ["$%d.%s" % (gi, key)], "story": st, "pos": a, "position": "custom", "xRelative": "textFrame",
                                    "xOffset": 0, "yRelative": "anchor", "yOffset": -17, "refPoint": 0, "objectPoint": 0})
        elif ex[0] == 'icon' and ex[1]:
            ii = icon(ex[1], spread)
            cmd('anchored.insert', {"ids": ["$%d.id" % ii], "story": st, "pos": a, "position": "custom", "xRelative": "textFrame",
                                    "xOffset": 0, "yRelative": "anchor", "yOffset": -18, "refPoint": 0, "objectPoint": 0})
    return f

def simple(spread, rect, style, text, label=None, vj=None):
    f = cmd('frame.create', {"spread": spread, "rect": rect, "content": "text", "text": text})
    cmd('selection.set', {"ids": ["$%d.id" % f]})
    cmd('style.paragraph.apply', {"name": style, "clearOverrides": True})
    if vj:
        cmd('object.textFrameOptions', {"verticalJustification": vj, "inset": 0, "ids": ["$%d.id" % f]})
    if label:
        cmd('object.label', {"label": label, "ids": ["$%d.id" % f]})
    return f

def banner(spread, title, acc):
    x0 = (W - 480) / 2
    place(VET + '/testata.pdf', [x0, 60, x0 + 480, 110], spread)
    simple(spread, [x0 + 50, 60, x0 + 430, 110], 'Testata ' + acc, title, vj='center')

def schema(spread, sid, rect):
    base = SCH + '/' + sid
    path = None
    for ext in ('.pdf', '.svg', '.png'):
        if os.path.exists(base + ext): path = base + ext; break
    stroke = None if path else {"swatch": "Ottone", "weight": 0.75, "type": {"kind": "dashed", "pattern": [4, 3]}}
    return place(path, rect, spread, fit='fitProportionally', label='schema-' + sid, stroke=stroke)

ILL = {}
def illus(spread, name, rect, border=True):
    ILL[name] = [round(rect[2] - rect[0], 2), round(rect[3] - rect[1], 2)]
    stroke = {"swatch": "Ottone", "weight": 1.2} if border else None
    return place(PNG + '/' + name + '.png', rect, spread, fit='fillProportionally', label='illustrazione-' + name, stroke=stroke)


# ---------------------------------------------------------------- pages
HFILE = os.path.join(SRC, 'heights.json')
MEAS = json.load(open(HFILE)) if os.path.exists(HFILE) else {}
MODE = sys.argv[1] if len(sys.argv) > 1 else 'final'
LABELS = {}
TOP, BOT = 116, 768

def hgt(label, default=100):
    return MEAS.get(label, default)

def tf(spread, x0, y0, x1, blocks, acc, label, icons=None, cols=None, extra=0, vj=None, thread=None, h=None):
    if h is None or MODE == 'measure':
        h = hgt(label) + extra
    if blocks and blocks[0][0] == 'h3':
        y0 -= 9   # the subhead's space before is not wanted at the top of a frame
    f = textframe(spread, [x0, y0, x1, y0 + h], blocks, acc, icons=icons, cols=cols, label=label)
    LABELS[label] = f
    if MODE == 'measure':
        cmd('object.textFrameOptions', {"autoSize": "heightOnly", "autoSizeReference": "topLeft", "ids": ["$%d.id" % f]})
    if vj:
        cmd('object.textFrameOptions', {"verticalJustification": vj, "ids": ["$%d.id" % f]})
    if thread and MODE != 'measure':
        cmd('text.thread', {"from": "$%d.id" % f, "rect": thread, "spread": spread})
    return y0 + h

AGREED = {'S1-tavolo': (515, 265), 'S2-turno': (250, 195), 'S3-mappa': (515, 235), 'S4-scontro': (515, 170),
          'S5-indizio': (250, 195), 'S6-catena': (515, 280), 'S7-perdita': (515, 220)}
def svg_size(sid, default):
    return AGREED[sid]
def page_title(p):
    t = open(ROOT + '/testo_manuale.md', encoding='utf-8').read()
    m = re.search(r'^## Pagina %d — (.+)$' % p, t, re.M)
    return inline(m.group(1))

def first(page, kind, pred=lambda b: True):
    return next(b for b in TXT[page] if b[0] == kind and pred(b))

def page1():
    s = 0
    title = first(1, 'h1')[1]
    deck = first(1, 'p')[1]
    simple(s, [L, 46, R, 176], 'Titolo copertina', title.replace(' del ', '\u2028del '))
    simple(s, [L, 184, R, 202], 'Sottotitolo copertina', deck)
    hy0, hy1 = 210, 210 + 272
    illus(s, 'copertina', [L, hy0, R, hy1])
    top = hy1 + 16
    scat = [b for b in section(1, 'Nella scatola') if b[0] not in ('marker', 'quote')]
    yl = tf(s, C1[0], top, C1[1], strip_markers(section(1, 'La storia')) + scat, 'Rosso', 'p1-sinistra',
            icons={'La storia': 'tesoro', 'Nella scatola': 'stack'})
    yr = tf(s, C2[0], top, C2[1], strip_markers(section(1, 'Come si vince')), 'Rosso', 'p1-destra',
            icons={'Come si vince': 'indizio'})
    # Geronimo + speech bubble close the right column, bottom aligned with the left column
    gs = min(118, yl - yr - 6)
    gx, gy = C2[0] - 8, yl - gs
    illus(s, 'geronimo', [gx, gy, gx + gs, yl], border=False)
    q = first(1, 'quote')[1]
    bx0 = gx + gs - 2
    qh = hgt('p1-consiglio', 90)
    by0 = gy + 4
    tail = cmd('frame.create', {"spread": s, "rect": [bx0 - 12, by0 + 18, bx0 + 8, by0 + 34], "shape": "polygon", "sides": 3, "content": "graphic"})
    cmd('transform.rotate', {"angle": 90, "ids": ["$%d.id" % tail]})
    cmd('object.fill', {"swatch": "Pergamena", "ids": ["$%d.id" % tail]})
    cmd('object.stroke', {"swatch": "Ottone", "weight": 1.2, "ids": ["$%d.id" % tail]})
    bub = cmd('frame.create', {"spread": s, "rect": [bx0, by0, C2[1], by0 + qh + 18], "shape": "rectangle", "content": "graphic"})
    cmd('object.fill', {"swatch": "Pergamena", "ids": ["$%d.id" % bub]})
    cmd('object.stroke', {"swatch": "Ottone", "weight": 1.2, "ids": ["$%d.id" % bub]})
    cmd('object.cornerOptions', {"shape": "rounded", "size": 12, "ids": ["$%d.id" % bub]})
    tf(s, bx0 + 11, by0 + 9, C2[1] - 9, [('raw', 'Consiglio', q)], 'Rosso', 'p1-consiglio')

def page2():
    s = 1
    banner(s, page_title(2), 'Oro')
    s1w, s1h = svg_size('S1-tavolo', (515, 300))
    prep = [b for b in section(2, 'Preparazione') if b[0] in ('h3', 'ol')]
    y1 = tf(s, C1[0], TOP, C1[1], prep, 'Oro', 'p2-preparazione', icons={'Preparazione': 'esagono'})
    s2w, s2h = svg_size('S2-turno', (250, 185))
    schema(s, 'S2-turno', [C2[0], TOP + 4, C2[0] + s2w, TOP + 4 + s2h])
    tabs = {b[1][0][0]: b[1] for b in TXT[2] if b[0] == 'table'}
    y2 = tf(s, C2[0], TOP + 4 + s2h + 6, C2[1], [('table', tabs['Classe'])], 'Oro', 'p2-mano-pronta', cols=[82, 168])
    trans = [list(r) for r in zip(*tabs['Rotella'])]
    yt = tf(s, L, max(y1, y2) + 2, R, [('table', trans)], 'Oro', 'p2-rotelle', cols=[70] + [(R - L - 70) / 6] * 6)
    schema(s, "S1-tavolo", [L, yt + 4, L + s1w, yt + 4 + s1h])

def page3():
    s = 2
    banner(s, page_title(3), 'Rosso')
    y = tf(s, L, TOP, R, strip_markers(section(3, '1 · Muovi')), 'Rosso', 'p3-muovi', icons={'1 · Muovi': 'movimento'})
    s3w, s3h = svg_size('S3-mappa', (515, 270))
    schema(s, 'S3-mappa', [L, y + 2, L + s3w, y + 2 + s3h])
    y += 2 + s3h + 6
    ex = strip_markers(section(3, '2 · Esplora'))
    tabi = [b for b in ex if b[0] == 'table']
    rest = [b for b in ex if b[0] != 'table']
    y1 = tf(s, C1[0], y, C1[1], [ex[0]] + tabi, 'Rosso', 'p3-esplora', icons={'2 · Esplora': 'segnalino'}, cols=[98, 152])
    y2 = tf(s, C2[0], y + 22, C2[1], rest[1:], 'Rosso', 'p3-esplora-testo')
    s4w, s4h = svg_size('S4-scontro', (515, 230))
    y = max(y1, y2) + 2
    s4y = BOT - s4h
    hs = hgt('p3-scontro')
    sc = strip_markers(section(3, 'Lo scontro'))
    ys = tf(s, C1[0], max(y, s4y - 6 - hs + 9), C1[1], [b for b in sc if b[0] != 'ul'], 'Rosso', 'p3-scontro', icons={'Lo scontro': 'mostro'})
    # ritiri e Forte Volontà nella colonna destra, allineati in basso con «Lo scontro»
    yr = tf(s, C2[0], max(y2 + 4, ys - hgt('p3-ritiri')), C2[1], [b for b in sc if b[0] == 'ul'], 'Rosso', 'p3-ritiri')
    s4y = max(ys + 6, yr + 6, s4y)
    schema(s, 'S4-scontro', [L, s4y, L + s4w, s4y + s4h])

def page4():
    s = 3
    banner(s, page_title(4), 'Blu')
    s5w, s5h = svg_size('S5-indizio', (250, 200))
    schema(s, 'S5-indizio', [C2[0], TOP, C2[0] + s5w, TOP + s5h])
    flow = strip_markers(section(4, 'Le carte'))
    yf = tf(s, C1[0], TOP, C1[1], flow, 'Blu', 'p4-flusso', icons={'Le carte': 'carta'})
    s6w, s6h = svg_size('S6-catena', (515, 280))
    y = max(yf, TOP + s5h) + 4
    schema(s, 'S6-catena', [L, y, L + s6w, y + s6h])
    y += s6h + 12
    mr = strip_markers(section(4, 'Mano e Stati'))
    ul = mr[1][1]
    tf(s, C1[0], y, C1[1], [mr[0], ('ul', ul[:3])], 'Blu', 'p4-mano-1', icons={'Mano e Stati': 'mano10'})
    tf(s, C2[0], y + 22, C2[1], [('ul', ul[3:])], 'Blu', 'p4-mano-2')

def page5():
    s = 4
    banner(s, page_title(5), 'Verde')
    s7w, s7h = svg_size('S7-perdita', (515, 220))
    schema(s, 'S7-perdita', [L, TOP, L + s7w, TOP + s7h])
    y = TOP + s7h + 14
    mimi = [b for b in strip_markers(section(5, 'MIMI e la vittoria')) if b[0] != 'italic']
    k = next(i for i, b in enumerate(mimi) if b[0] == 'ul')   # ultimo punto, Mappe, Classi, Oracolo: colonna destra
    ul = mimi[k][1]
    y1 = tf(s, C1[0], y, C1[1], strip_markers(section(5, 'Il Duello')) + mimi[:k] + [('ul', ul[:-1])], 'Verde', 'p5-sinistra',
            icons={'Il Duello': 'ar', 'MIMI e la vittoria': 'tesoro'})
    y2 = tf(s, C2[0], y + 22, C2[1], [('ul', ul[-1:])] + mimi[k + 1:], 'Verde', 'p5-destra')
    vt = max(y1, y2) + 8
    hv = min(BOT - vt, 112)
    wv = hv * 1.5
    illus(s, 'morte', [L, BOT - hv, L + wv, BOT])
    illus(s, 'vittoria', [R - wv, BOT - hv, R, BOT])
    simple(s, [L + wv + 12, BOT - hv, R - wv - 12, BOT], 'Chiusura', first(5, 'italic')[1], vj='center', label='p5-chiusura')

setup()
parents()
page1(); page2(); page3(); page4(); page5()
cmd('find.change', {"find": "⟪([^⟫]*)⟫", "change": "$$1", "grep": True, "scope": "document", "charStyle": "Forte"})
cmd('find.change', {"find": "Consiglio del goblin:", "change": "", "scope": "document", "charStyle": "Etichetta consiglio"})
cmd('find.change', {"find": "Il regolamento", "change": "", "scope": "document", "charStyle": "Accento copertina"})
if MODE == 'measure':
    cmd('document.inspect', {})
    json.dump(LABELS, open(os.path.join(WORK, 'labels.json'), 'w'))

json.dump(ILL, open(os.path.join(WORK, 'ill_%s.json' % MODE), 'w'))
print('\n'.join(cmds))
