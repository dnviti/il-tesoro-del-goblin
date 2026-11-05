# Carte della scatola base corrette il 21/10/2026 (decisione di Daniele nel thread del framework).
# Aggiunge 4 manopole in BAL con i valori nuovi come default (i vecchi restano raggiungibili con BALX):
#   te18 'cless'    Pozione del tempo: «Togli fino a 2 tue Clessidre.»          (vecchio: 'vecchio')
#   ti45 'dietroPV' Ritardare l'inevitabile: «Un avversario con più Indizi di te perde 1 Indizio. Tu perdi 2 PV.»  (vecchio: 'vecchio')
#   te21 4          Pozione della salute: «Recuperi 4 PV.»                        (vecchio: 2)
#   tm05 'mov1'     Selva: «Elfo e Druido: +1 MOV finché la Selva resta.»         (vecchio: 'vecchio')
# Uso: python3 patch_carte_21-10.py ../game.js   (si applica una volta sola; poi ricostruire)
import sys
p = sys.argv[1] if len(sys.argv) > 1 else '../game.js'
s = open(p).read()
if 'te18:' in s and 'tm05:' in s:
    sys.exit('già applicata')
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep("const BAL = { ", "const BAL = { te18: 'cless', ti45: 'dietroPV', te21: 4, tm05: 'mov1', ")
rep("DEF['TE-18'] = { when: 'fuori', fx: async (p, o) => {",
    "DEF['TE-18'] = { when: 'fuori', fx: async (p, o) => { if (BAL.te18 === 'cless') { const c = Math.min(2, p.skip); p.skip -= c; log(`${p.name} toglie ${c} Clessidr${c === 1 ? 'a' : 'e'}.`, 'good'); return; }")
rep("}, ai: () => 3, nota: '«Recuperare turni»", "}, ai: p => BAL.te18 === 'cless' ? (p.skip > 0 ? 4 : 0) : 3, nota: '«Recuperare turni»")
rep("T({ id: 'TI-45', when: 'fuori', fx: async (p, o) => {",
    "T({ id: 'TI-45', when: 'fuori', fx: async (p, o) => { if (BAL.ti45 === 'dietroPV') { if (o.clues > p.clues) { if (o.located) { o.located = false; o.clues = 2; } else o.clues--; log(`${o.name} perde 1 Indizio.`, 'bad'); } await harm(p, 2); return; }")
rep("ai: (p, o) => isLocated(o) && p.pv > 1 ? 4 : 0,", "ai: (p, o) => BAL.ti45 === 'dietroPV' ? (o.clues > p.clues && p.pv > 2 ? 4 : 0) : isLocated(o) && p.pv > 1 ? 4 : 0,")
rep("fx: async p => heal(p, 2), ai: p => maxPV(p) - p.pv >= 2 ? 3 : 0 };", "fx: async p => heal(p, BAL.te21 || 2), ai: p => maxPV(p) - p.pv >= 2 ? 3 : 0 };")
rep("case 'TM-05': if (isR(p, 'Elfo')) {", "case 'TM-05': if (BAL.tm05 === 'mov1') { if (isR(p, 'Elfo') || isC(p, 'Druido')) b.mov++; } else if (isR(p, 'Elfo')) {")
open(p, 'w').write(s)
print('applicata a', p)
