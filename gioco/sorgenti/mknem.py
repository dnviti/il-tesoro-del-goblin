# Carte Nemico v2 nel layout Canva della carta Nemico: slide 1 = template, poi una carta per nemico
import copy, json, sys
from pptx import Presentation
src, nemj, out = sys.argv[1:4]
nem = json.load(open(nemj))
prs = Presentation(src)
tpl, fol = prs.slides[0], prs.slides[1]

def set_text(shape, lines):
    tf = shape.text_frame
    paras = tf.paragraphs
    while len(paras) < len(lines):
        p_new = copy.deepcopy(paras[-1]._p); paras[-1]._p.addnext(p_new); paras = tf.paragraphs
    for i, p in enumerate(paras):
        if i >= len(lines):
            p._p.getparent().remove(p._p); continue
        runs = p.runs
        if not runs:
            r = p.add_run(); r.text = lines[i]; continue
        runs[0].text = lines[i]
        for r in runs[1:]: r._r.getparent().remove(r._r)

def fill(slide, n):
    for sh in slide.shapes:
        if not sh.has_text_frame: continue
        nm = sh.name
        if nm == 'TITOLO': set_text(sh, [n['nome'].upper()])
        elif nm == 'SIMBOLO MEDAGLIONE': set_text(sh, [n['lettera']])
        elif nm == 'LIVELLO': set_text(sh, [f"LV. {str(n['lv']).replace('.', ',')}"])
        elif nm == 'VALORE PV': set_text(sh, [str(n['pv'])])
        elif nm == 'VALORE ATT': set_text(sh, [str(n['att'])])
        elif nm == 'VALORE AR': set_text(sh, [str(n['ar'])])
        elif nm == 'TESTO ABILITÀ': set_text(sh, [n['abilita']] if n['abilita'] else [''])
        elif nm == 'TESTO RICOMPENSE': set_text(sh, n['ricompense'].split('\n'))
        elif nm == 'Testo segnaposto illustrazione': set_text(sh, ['ILLUSTRAZIONE DA INSERIRE', n['nome']])

def dup(slide):
    new = prs.slides.add_slide(slide.slide_layout)
    for sh in list(new.shapes): sh._element.getparent().remove(sh._element)
    for el in slide.shapes._spTree.iterchildren():
        if el.tag.endswith('}sp') or el.tag.endswith('}pic') or el.tag.endswith('}grpSp') or el.tag.endswith('}cxnSp'):
            new.shapes._spTree.append(copy.deepcopy(el))
    if slide.background.fill.type is not None:
        new.background._cSld.insert(0, copy.deepcopy(slide.background._cSld.bg)) if slide.background._cSld.bg is not None else None
    return new

for n in nem:
    if n['id'] == 'NE-01': fill(fol, n); continue
    fill(dup(tpl), n)
prs.save(out)
print('slide', len(prs.slides))
