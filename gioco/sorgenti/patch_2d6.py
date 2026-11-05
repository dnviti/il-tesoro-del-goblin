#!/usr/bin/env python3
# Colpire con 2D6 (Daniele, 2/11): in scatola solo 4 D6, movimento 1D6 + MOV, tiro per colpire 2D6 + ATT ≥ Difesa.
# Doppio 6 = colpo critico (danno doppio), doppio 1 = mancato. BAL.hit2d6 = true; la Difesa base (BAL.defBase) è ritarata col simulatore.
# Da applicare dopo patch_colori.py.  Uso: python3 patch_2d6.py game.js
import sys
f = sys.argv[1]; s = open(f).read()
def rep(old, new, n=1):
    global s
    if s.count(old) != n: raise SystemExit(f'trovato {s.count(old)} volte: ' + old[:90])
    s = s.replace(old, new)
rep("const HIT_DIE = () => BAL.hitDie || 20;",
    "const HIT_DIE = () => BAL.hit2d6 ? 12 : (BAL.hitDie || 20);\nconst HIT_MIN = () => BAL.hit2d6 ? 2 : 1;\nconst dieName = s => s === 12 && BAL.hit2d6 ? '2D6' : 'D' + s;\n"
    "// probabilità di arrivare a k con il dado per colpire (per le stime dell'IA)\nconst hitP = k => { const H = HIT_DIE(); if (BAL.hit2d6) { let n = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (a + b >= k) n++; return Math.min(35, Math.max(1, n)) / 36; } return Math.min(H - 1, Math.max(1, H + 1 - k)) / H; };")
rep("function rollRaw(s, adv = 0, uni = false) { if (s === 4) return d4(uni); const a = rnd(s);",
    "function rollRaw(s, adv = 0, uni = false) { if (s === 4) return d4(uni); if (s === 12 && BAL.hit2d6) { const a = rnd(6) + rnd(6); if (!adv) return a; const b = rnd(6) + rnd(6); return adv > 0 ? Math.max(a, b) : Math.min(a, b); } const a = rnd(s);")
rep("log(`${p ? p.name + ' · ' : ''}${label}: D${sides}${adv > 0", "log(`${p ? p.name + ' · ' : ''}${label}: ${dieName(sides)}${adv > 0")
rep("  const hit = v => v === HD || (v !== 1 && v + bonus >= need);", "  const hit = v => v === HD || (v !== HIT_MIN() && v + bonus >= need);")
rep("  tick('attacco'); const HD = HIT_DIE(), v = rnd(HD), need = DIFESA(arOf(foe, c));\n  if (v === HD || (v !== 1 && v + s.att >= need))",
    "  tick('attacco'); const HD = HIT_DIE(), v = rollRaw(HD), need = DIFESA(arOf(foe, c));\n  if (v === HD || (v !== HIT_MIN() && v + s.att >= need))")
rep("`Attacca (D${HIT_DIE()}${fmt(atkOf(x, c))}", "`Attacca (${dieName(HIT_DIE())}${fmt(atkOf(x, c))}")
rep("return pv * (s / 2 + b) * (atkOf(x, c) + HIT_DIE() + 1 - (BAL.defBase ?? 14)) / HIT_DIE(); }",
    "return pv * (s / 2 + b) * hitP((BAL.defBase ?? 14) - atkOf(x, c)); }")
rep("  monLv: true, ", "  hit2d6: true,                 // colpire con 2D6 (Daniele, 2/11): solo D6 in scatola\n  monLv: true, ")
open(f, 'w').write(s)
print('ok')
