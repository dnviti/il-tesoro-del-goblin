# Espansione «Il Caos del Goblin · Le Crepe di MIMI» (21/10 sera) applicata a game.js
s=open('game.js').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
start=s.index("// Caos del Goblin: D6 sulla tabella degli eventi\nasync function chaosEvent(p) {")
end=s.index("async function resolveArrival(p) {")
assert start<end
new_body = open('caos_body.js').read()
s=s[:start]+new_body+s[end:]
rep("  render();\n  while (!res) {\n    c.round++;","  render();\n  if (!res && foe.agguato) { log(`${foe.name}: agguato! Attacca per primo.`, 'bad'); await attack(foe, p, c); if (dead(p)) res = 'lose'; }\n  while (!res) {\n    c.round++;")
rep("  t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${maxPV(t)}).`, 'bad');\n",
    "  t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${maxPV(t)}).`, 'bad');\n  if (c && c.foe && c.foe.borseggio && t === c.p && !c.stole && t.hand.length) { c.stole = true; log(`${c.foe.name} ti ruba una carta: ne scarti una a caso.`, 'bad'); randomDiscard(t, 1); }\n")
rep("    tileAt(p.pos).done = true;\n    await addClue(p);\n    if (kind === 'miniboss')",
    "    if (!foe.cob) tileAt(p.pos).done = true;\n    if (foe.cob) { log('I Coboldi non hanno pagine della mappa: peschi una carta.'); drawCard(p); if (foe.borseggio) drawCard(p); } else await addClue(p);\n    if (kind === 'miniboss')")
rep("    else { const v = await roll(p, G.rules.die, 'Movimento', { bad: v => v <= 1 }); n = Math.max(1, v + stat(p, 'mov')); }",
    "    else if (p.slowNext) { p.slowNext = false; n = 1; log(`Vento di nulla: ${p.name} muove di 1 esagono soltanto.`, 'bad'); }\n    else { const v = await roll(p, G.rules.die, 'Movimento', { bad: v => v <= 1 }); n = Math.max(1, v + stat(p, 'mov')); }")
rep("      case 'TE-12': b.ar += 2;","      case 'CA-04': b.ar += 1; if (isC(p, 'Chierico')) b.att++; break;\n      case 'TE-12': b.ar += 2;")
rep("...shuffle(COMMON.filter(id => !used.has(id))).slice(0, 5)]","...shuffle(commonPool().filter(id => !used.has(id))).slice(0, 5)]")
rep("SLOT['TE-23'] = 'scudo';","SLOT['TE-23'] = 'scudo';\nSLOT['CA-04'] = 'elmo';")
rep("// ----- Carte leggendarie (nuove, una per classe) -----",open('caos_cards.js').read()+"// ----- Carte leggendarie (nuove, una per classe) -----")
open('game.js','w').write(s)
print('ok')
