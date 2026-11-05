#!/usr/bin/env python3
# Crea il motore v2 (Carte Trama v2) a partire da game.js della scatola del 21/10.
import sys, re
src = open(sys.argv[1]).read()
out = sys.argv[2]
B = lambda n: open('blocks/' + n).read()

def between(s, start, end, new, keep_end=True):
    i = s.index(start); j = s.index(end, i + len(start))
    return s[:i] + new + (s[j:] if keep_end else s[j + len(end):])

def rep(s, old, new, count=1):
    if s.count(old) < 1: raise SystemExit('manca: ' + old[:80])
    return s.replace(old, new, count)

s = src
s = between(s, "const CLASSES = [", "\nconst TILE = {", B('a_dati.js'))
s = between(s, "const BAL = {", "\n// Tempo di gioco umano", B('b_bal.js').rstrip('\n'))
s = rep(s, "const FOES = new Set([", "const FOES = new Set([]); const _OLDFOES = ([")
s = rep(s, "const TARG = new Set([", "const TARG = new Set([]); const _OLDTARG = ([")
s = rep(s, "const TARG_LOCATED = new Set(['TI-04', 'TI-41']);", "const TARG_LOCATED = new Set([]);")
s = rep(s, "const weapons = p => equipped(p).filter(id => ['1h', '2h'].includes(SLOT[baseId(id)]));", "const weapons = p => equipped(p).filter(id => SLOT[baseId(id)] === 'dx' && !SHIELDS.includes(baseId(id)));")
s = rep(s, "const sb = p => isC(p, 'Stregone') ? BAL.strBonus : 0;", "// Yuma (Paradiso): gli incantesimi di danno e di cura danno +1\nconst sb = p => (G && G.map && G.map.id === 'TM-07') ? 1 : 0;")
s = between(s, "function eqBonus(p) {", "function stat(p, k) {", B('c_bonus.js'))
s = between(s, "function rerollOpts(p) {", "\n// ===================== Interazione", B('d_roll.js').rstrip('\n'))
s = between(s, "function moveTreasure() {", "async function addPE(p, n) {", B('e_move.js'))
s = between(s, "async function equip(p, id) {", "async function defeat(", B('f_equip.js'))
s = between(s, "async function setMap(p, id) {", "\n// ===================== Scontri", B('i_setmap.js').rstrip('\n'))
s = rep(s, "const arOf = (x, c) => (x.isCreature ? x.ar : stat(x, 'ar')) + cmod(c, x, 'ar');",
        "const arOf = (x, c) => (x.isCreature ? x.ar : stat(x, 'ar') + (c && c.kind === 'miniboss' && has(x, 'TE-19') ? 2 : 0)) + cmod(c, x, 'ar');")
s = between(s, "function dmgDice(x) {", "async function scontro(p, foe, kind) {", B('g_combat.js'))

# --- scontro ---
s = rep(s, "if (!res && p.flags.assassinio", "if (false && p.flags.assassinio")
s = rep(s, "if (!res && foe.agguato) {", "if (!res && foe.agguato) { c.foeFirst = true;")
s = rep(s, """    c.round++;
    const act = await combatTurn(p, c, true);
    if (G.over) return;
    if (act === 'fuga') { res = 'fuga'; break; }""",
"""    c.round++;
    if (c.burn && c.round > 1 && c.foe.isCreature) { log('Fiamma Persistente brucia ancora.'); await hurt(c.foe, c.burn, c); if (dead(foe)) { res = 'win'; break; } }
    const act = await combatTurn(p, c, true);
    if (G.over) return;
    if (act === 'fuga') { res = 'fuga'; break; }
    if (act === 'velo') { res = 'velo'; break; }""")
s = rep(s, "      if (a2 === 'fuga') { res = 'fugaDif'; break; }", "      if (a2 === 'fuga' || a2 === 'velo') { res = 'fugaDif'; break; }")
s = rep(s, "    if (BAL.guerInsp && isC(p, 'Guerriero')) giveInsp(p, 'Guerriero vittorioso');",
"""    if (BAL.guerInsp && isC(p, 'Guerriero')) giveInsp(p, 'Guerriero vittorioso');
    if (p.turnFlags.specchio) giveInsp(p, 'Specchio dei Tesori');
    if (has(p, 'TE-03') && !p.turnFlags.cappello) { p.turnFlags.cappello = true; log('Cappello del Taumaturgo: riprendi una carta.'); await recover(p, 1); }""")
s = rep(s, "  } else if (res === 'fugaDif') {", "  } else if (res === 'velo') {\n    log(`${p.name} si dilegua: nessuna ricompensa, ma resta dov'è.`);\n  } else if (res === 'fugaDif') {")

# --- canPlay / playCard: classi multiple, reazioni, trappole, Sigillo ---
s = rep(s, "function canPlay(p, id, { free = false } = {}) {", "function canPlay(p, id, { free = false, react = false } = {}) {")
s = rep(s, "  if (C(id).cls && !isC(p, C(id).cls)) return `Carta di classe ${C(id).cls}: la può giocare solo un ${C(id).cls}`;",
"""  if (C(id).cls && !C(id).cls.some(k => isC(p, k))) return `Carta di classe ${C(id).cls.join(' o ')}`;
  if (p.silenced !== undefined && p.silenced !== null && C(id).tipo === 'TI') return 'Sigillo del Silenzio: niente Incantesimi fino al prossimo turno di chi l\\'ha giocato';
  if (!react && (d.when === 'reazione' || d.when === 'trappola')) return d.when === 'trappola' ? 'Si gioca quando peschi una Trappola' : 'Si gioca in risposta (a un colpo o a un tuo tiro)';""")
s = rep(s, "  if (c) {\n    if (c.noCards) return 'Stop: nessuna carta in questo scontro';",
          "  if (react) { if (free) return true; if (G.combat && G.combat.foe === p) return G.combat.defCards >= 1 ? 'In difesa puoi giocare 1 sola carta per scontro' : true; if (G.players[G.cur] !== p) return 'Non è il tuo turno'; return p.played >= p.limit ? `Hai già giocato ${p.limit} carte in questo turno` : true; }\n  if (c) {\n    if (c.noCards) return 'Stop: nessuna carta in questo scontro';")
s = rep(s, "async function playCard(p, id, { free = false, immediate = false } = {}) {\n  const why = canPlay(p, id, { free });",
          "async function playCard(p, id, { free = false, immediate = false, react = false } = {}) {\n  const why = canPlay(p, id, { free, react });")

# --- IA in scontro: niente cure Paladino ---
s = rep(s, "  if (opts.some(o => o.value === 'pal') && x.pv <= maxPV(x) / 2) return 'pal';\n", "")

# --- turno: effetti «fino al tuo prossimo turno» ---
s = rep(s, "  tick('turno'); p.ownTurns++; p.played = 0; p.limit = 2; p.eqTurn = false;",
"""  tick('turno'); p.ownTurns++; p.played = 0; p.limit = 2; p.eqTurn = false;
  p.mods = p.mods.filter(m => m.kind !== 'untilNext'); p.flags.riflesso = false; for (const x of G.players) if (x.silenced === p.id) x.silenced = null;""")

# --- creature dal mazzo Nemici ---
s = rep(s, "  const foe = kind === 'miniboss' ? makeCreature(pick(MINIBOSS), p.level) : makeCreature(pick(BESTIARIO), p.level);",
"""  const deckK = kind === 'miniboss' ? 'mb' : 'cr';
  if (!G.nem[deckK].length) G.nem[deckK] = shuffle([...(kind === 'miniboss' ? MINIBOSS : BESTIARIO)]);
  const foe = makeCreature(G.nem[deckK].pop(), p.level);""")
s = rep(s, "const st = `${foe.name}: PV ${foe.pv}, ATT ${fmt(foe.att)}, AR ${foe.ar}, danni ${dmgLabel(foe)}`;",
          "const st = `${foe.name} (LV ${foe.lv}): PV ${foe.pv}, ATT ${fmt(foe.att)}, AR ${foe.ar} (Difesa ${10 + foe.ar}), danno ${dmgLabel(foe)}`;")

# --- caselle: Trappola, Locanda, Fonte ---
s = rep(s, """      tl.done = true; log('Trappola!', 'bad');
      const d = BAL.noD4 ? Math.max(1, await roll(p, 6, 'Danni della trappola (D6 − 1, minimo 1)') - 1) : await roll(p, 4, 'Danni della trappola');
      await hurt(p, d);""",
"""      tl.done = true; log('Trappola!', 'bad');
      if (has(p, 'TE-01')) { log('Elmo sorgisogno: vedi la Trappola in tempo, nessun effetto.', 'good'); break; }
      if (p.flags.trapWard) { p.flags.trapWard = false; log('Occhio dello Stregone: la Trappola non ha effetto.', 'good'); break; }
      if (await reactCard(p, 'TI-39', 'Trappola')) { log('Passo Felpato: ignori la Trappola.', 'good'); break; }
      let d = Math.max(1, await roll(p, 6, 'Danni della trappola (D6 − 1, minimo 1)') - 1);
      if (G.map && G.map.id === 'TM-08') { d *= 2; log('Flegias: la Trappola fa il doppio dei danni.', 'bad'); }
      if (has(p, 'TE-16')) d = Math.max(0, d - 1);
      if (d >= 2 && await reactCard(p, 'TI-17', `Trappola da ${d} danni`)) { log('Barriera Runica: nessun danno.', 'good'); d = 0; }
      await hurt(p, d);""")
s = rep(s, "if (!tl.used) tl.done = true; p.flags.revived = false; heal(p, 2);", "if (!tl.used) tl.done = true; p.flags.revived = false; heal(p, (BAL.locHeal || 2) + (has(p, 'TE-18') ? 1 : 0));")
s = rep(s, "case 'fonte': log('Fonte: puoi recuperare fino a 2 carte dagli scarti.', 'good'); if (!tl.used) tl.done = true; await recover(p, 2); break;",
          "case 'fonte': log('Fonte: puoi recuperare fino a 2 carte dagli scarti.', 'good'); if (!tl.used) tl.done = true; await recover(p, 2); if (has(p, 'TE-20')) heal(p, 1); break;")

# --- carte del mazzo e mani ---
s = between(s, "const DECK = {};", "function dealDecks() {",
"""const DECK = {};
for (const c of CARDS) if (c.cls && c.tipo !== 'TC') for (const k of c.cls) (DECK[k] = DECK[k] || []).push(c.id);
const COMMON = CARDS.filter(c => c.tipo !== 'TC' && !c.cls).map(c => c.id);
// mano: Carta Classe + BAL.handCls carte della tua classe + il resto dal mazzo comune (10 in tutto)
function dealList(list) {
  const used = new Set();
  for (const sp of list) {
    const mine = shuffle((DECK[sp.cls] || []).filter(id => !used.has(id))).slice(0, BAL.handCls);
    mine.forEach(id => used.add(id));
    const com = shuffle(commonPool().filter(id => !used.has(id))).slice(0, BAL.handTot - mine.length);
    com.forEach(id => used.add(id));
    sp.deck = [...mine, ...com];
  }
}
""")
s = rep(s, "equip: { elmo: null, dx: null, sx: null, armatura: null, accessorio: null }", "equip: { elmo: null, dx: null, sx: null, armatura: null }")
s = rep(s, "G = { stage: 'early',", "G = { nem: { cr: [], mb: [] }, stage: 'early',")
s = rep(s, "  const foe = makeCreature(G.beholder ? { ...BEHOLDER, pv: BAL.behPV || BEHOLDER.pv } : { ...BOSS, pv: BAL.bossPV });",
          "    const foe = makeCreature(G.beholder ? { ...BEHOLDER, pv: BAL.behPV || BEHOLDER.pv } : { ...BOSS, pv: BAL.bossPV });") if "  const foe = makeCreature(G.beholder" in s else s

s = rep(s, "Object.entries(BAL.bagDraw ? PHYS.tokensBag : PHYS.tokens)", "Object.entries(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens)")
s = rep(s, "level: 1, pe: 0, clues: 0,", "level: 1, pe: 0, clues: BAL.startClues || 0,")
s = rep(s, "if (BAL.magoPerTurn && isC(p, 'Mago')) p.magoRerolls = 1;", "if (BAL.magoPerTurn && isC(p, 'Mago')) p.magoRerolls = BAL.magoRerolls;")
s = rep(s, "if (cls === 'Mago') p.magoRerolls = BAL.magoPerTurn ? 1 : BAL.magoRerolls;", "if (cls === 'Mago') p.magoRerolls = BAL.magoRerolls;")
# --- carte: definizioni ---
s = between(s, "// ===================== Carte: definizioni =====================", "// ===================== Gioco delle carte =====================", B('h_carte.js') + "\n")

# mano: carte di classe scelte e carte comuni draftate
import json as _json, os as _os
_dv = _json.load(open('draft_val.json')) if _os.path.exists('draft_val.json') else {}
s = rep(s, "async function initClasses() {\n  const myGame = G;\n", B('j_draft.js').replace('/*DRAFT_VAL*/{}', _json.dumps(_dv)) + "async function initClasses() {\n  const myGame = G;\n  if (BAL.handMode === 'draft') { await buildHands(); if (G !== myGame) return new Promise(() => {}); } else for (const p of G.players) p.startHand = [...p.hand];\n")
s = rep(s, "    sp.deck = [...mine, ...com];", "    sp.deck = BAL.handMode === 'draft' ? [] : [...mine, ...com];")
s = rep(s, ".filter(id => !used.has(id))).slice(0, BAL.handCls);", ".filter(id => !used.has(id))).slice(0, BAL.handClsRnd);")
# sacchetto: con BAL.bagRecycle il segnalino risolto torna nel sacchetto invece che nella scatola
s = rep(s, "  if (tl.q && tl.done) { if (G.tiles.bag.length) {", "  if (BAL.bagRecycle && tl.q && tl.done && TILE[tl.type]) { const b = G.tiles.bag; b.splice(Math.floor(Math.random() * (b.length + 1)), 0, tl.type); }\n  if (tl.q && tl.done) { if (G.tiles.bag.length) {")
# Indizi necessari (BAL.cluesNeed) e Indizi del mini-boss (BAL.mbClues), per le prove di durata
s = rep(s, "log(`${p.name} ottiene un indizio (${p.clues}/3).`, 'gold');\n    if (p.clues >= 3) locate(p);", "log(`${p.name} ottiene un indizio (${p.clues}/${BAL.cluesNeed || 3}).`, 'gold');\n    if (p.clues >= (BAL.cluesNeed || 3)) locate(p);")
s = rep(s, "if (x.clues >= 3) { x.located = true;", "if (x.clues >= (BAL.cluesNeed || 3)) { x.located = true;")
s = rep(s, "drawCard(p); if (foe.borseggio) drawCard(p); } else await addClue(p);", "drawCard(p); if (foe.borseggio) drawCard(p); } else { const sus = p.flags.sussurro ? 1 : 0; p.flags.sussurro = false; await addClue(p, (kind === 'miniboss' ? (BAL.mbClues || 1) : 1) + sus); }")
# Nemici a livelli con effetti (Daniele, 27/10)
s = between(s, "async function meetCreature(p, kind) {", "// Espansione «Il Caos del Goblin", B('k_nemici.js'))
s = rep(s, "  render();\n  if (!res && foe.agguato) {", "  render();\n  if (!res && foe.isCreature && (foe.fx === 'gelo' || foe.fx === 'vischio')) { addCmod(c, p, 'att', -1); log(`${foe.name}: hai −1 ATT per tutto lo scontro.`, 'bad'); }\n  if (!res && foe.agguato) {")
s = rep(s, "    if (act === 'fuga') { res = 'fuga'; break; }", "    if (act === 'fuga') { if (foe.fx === 'inseguitore') { log(`${foe.name} ti insegue e attacca!`, 'bad'); await attack(foe, p, c); if (dead(p)) { res = 'lose'; break; } } res = 'fuga'; break; }")
s = rep(s, "  G.combat = null;\n  for (const x of kind === 'pvp' ? [p, foe] : [p]) if (c.berserk[x.id]", "  G.combat = null;\n  if (res !== 'lose' && c.hitBy && foe.fx === 'veleno' && p.pv > 1) { p.pv--; log(`Morso infetto: ${p.name} perde 1 PV (PV ${p.pv}).`, 'bad'); }\n  for (const x of kind === 'pvp' ? [p, foe] : [p]) if (c.berserk[x.id]")
s = rep(s, "    if (kind === 'pvp') { await pvpReward(foe, p); return; }\n", "    if (kind === 'pvp') { await pvpReward(foe, p); return; }\n    if (foe.fx === 'catene') { log(`${foe.name}: catene, prendi 1 Clessidra.`, 'bad'); loseTurns(p, 1); }\n    if (foe.fx === 'saccheggio' && p.hand.length) { log(`${foe.name} ti saccheggia: scarti 1 carta a caso.`, 'bad'); randomDiscard(p, 1); }\n")
s = rep(s, "    log(`${p.name} fugge: nessuna ricompensa.`);\n    if (isC(p, 'Ladro')) log('Ladro: fugge senza arretrare.'); else retreat(p, p.turnStart);", "    log(`${p.name} fugge: nessuna ricompensa.`);\n    if (isC(p, 'Ladro') || foe.fx === 'lento') log(isC(p, 'Ladro') ? 'Ladro: fugge senza arretrare.' : `${foe.name} è lento: non arretri.`); else retreat(p, p.turnStart);")
# ricompense: il mazzetto II dà anche l'Ispirazione
s = rep(s, "    if (kind === 'miniboss') { await levelUp(p); giveInsp(p, 'mini-boss'); } else await addPE(p, 1);", "    if (kind === 'miniboss') { await levelUp(p); giveInsp(p, 'mini-boss'); } else { await addPE(p, 1); if (foe.lv >= 3) giveInsp(p, 'nemico del mazzetto II'); }")
# boss: uno dei 3 boss LV 5, pescato a inizio partita
s = rep(s, "{ ...BOSS, pv: BAL.bossPV }", "{ ...G.boss }")
s = rep(s, "G.cur = Math.floor(Math.random() * G.players.length); G.first = G.cur;", "G.boss = BAL.bossDeck && BOSSES.length ? pick(BOSSES) : { ...BOSS, pv: BAL.bossPV };\n  G.cur = Math.floor(Math.random() * G.players.length); G.first = G.cur;")
s = rep(s, "  log(`Inizia la partita. Comincia ${G.players[G.cur].name}.`, 'turn');", "  log(`Inizia la partita. Comincia ${G.players[G.cur].name}.`, 'turn');\n  log(`A custodire MIMI c'è ${G.boss.name}${G.boss.abil ? ': ' + G.boss.abil : ''}`, 'gold');")
# segnalini: Nemico I e Nemico II
s = rep(s, "  creatura: { n: 'Creatura', g: '⚔' },\n  miniboss: { n: 'Mini-boss', g: '♛' },", "  creatura: { n: 'Nemico I', g: '⚔' },\n  miniboss: { n: 'Nemico II', g: '♛' },")
# Corazza Runica: +2 AR contro i nemici di LV 3 o più
s = rep(s, "(c && c.kind === 'miniboss' && has(x, 'TE-19') ? 2 : 0)", "(c && c.foe && c.foe.isCreature && (c.foe.lv || 0) >= 3 && has(x, 'TE-19') ? 2 : 0)")
# preparazione predefinita con le 4 classi della scatola
s = rep(s, "race: 'Orchi', cls: 'Barbaro',", "race: 'Orchi', cls: 'Ladro',")
s = rep(s, "race: 'Elfi', cls: 'Druido',", "race: 'Elfi', cls: 'Oracolo',")
# Punti vita (Daniele, 27/10): si parte da 5 PV, crescono solo salendo di livello (+1 a una statistica oppure +2 PV); il Guerriero ha +2 PV
s = rep(s, "  Sanguar: { tag: 'Sanguar', fixed: { mov: 2, pv: 1 }, free: 0, info: '+2 MOV e +1 PV. Razza di non morti' },", "  Sanguar: { tag: 'Sanguar', fixed: { mov: 2 }, free: 0, info: '+2 MOV. Specie di non morti' },")
s = rep(s, "  Yumaniani: { tag: 'Aasimar', fixed: { pv: 1 }, free: 1, info: '+1 PV e +1 a una statistica a scelta. Valgono come Aasimar per le carte' },", "  Yumaniani: { tag: 'Aasimar', fixed: { ar: 1 }, free: 1, info: '+1 AR e +1 a una statistica a scelta. Valgono come Aasimar per le carte' },")
s = rep(s, "  Orchi: { tag: 'Orco', fixed: { att: 2, pv: 1 }, free: 0, info: '+2 ATT e +1 PV' },", "  Orchi: { tag: 'Orco', fixed: { att: 2 }, free: 0, info: '+2 ATT' },")
s = rep(s, "free: ['ar', 'pv'], deck: []", "free: ['ar', 'mov'], deck: []")
s = rep(s, "const base = { pv: 10 + ", "const base = { pv: (BAL.basePV || 5) + ")
s = rep(s, "for (let j = 0; j < R.free; j++) base[sp.free[j] || 'att']++;", "for (let j = 0; j < R.free; j++) { const k = sp.free[j] && sp.free[j] !== 'pv' ? sp.free[j] : 'att'; base[k]++; }")
s = rep(s, """  tick('livello'); mark('lvl' + (p.level + 1)); p.level++; p.base.pv++; p.pv++;
  log(`${p.name} sale al livello ${p.level}! +1 PV.`, 'good');
  const k = await ask(p, `Livello ${p.level}: scegli la statistica da aumentare`, ['att', 'mov', 'ar', 'pv'].map(s => ({ label: `+1 ${STATN[s]} (ora ${s === 'pv' ? maxPV(p) : stat(p, s)})`, value: s })), { ai: () => (p.level % 2 ? 'att' : 'ar') });
  p.base[k]++; if (k === 'pv') p.pv++;
  log(`${p.name} aumenta ${STATN[k]}.`);""", """  tick('livello'); mark('lvl' + (p.level + 1)); p.level++;
  log(`${p.name} sale al livello ${p.level}!`, 'good');
  const lvPV = BAL.lvPV || 2;
  const k = await ask(p, `Livello ${p.level}: +1 a una statistica oppure +${lvPV} PV`, ['att', 'mov', 'ar', 'pv'].map(s => ({ label: s === 'pv' ? `+${lvPV} PV (ora ${maxPV(p)})` : `+1 ${STATN[s]} (ora ${stat(p, s)})`, value: s })), { ai: () => (maxPV(p) < (BAL.aiPVmin || 9) ? 'pv' : (p.level % 2 ? 'att' : 'ar')) });
  if (k === 'pv') { p.base.pv += lvPV; p.pv += lvPV; } else p.base[k]++;
  log(`${p.name} aumenta ${k === 'pv' ? 'i PV di ' + lvPV : STATN[k]}.`);""")
# Colpire più difficile (Difesa 14 + AR) e fasi delle carte (Daniele, 27/10 sera): carte a inizio turno, in scontro o a fine turno; equipaggiamento solo a inizio turno
s = rep(s, "  if (isGear(id) && p.eqTurn) return 'Puoi equipaggiare un solo oggetto per turno';", "  if (isGear(id) && p.eqTurn) return 'Puoi equipaggiare un solo oggetto per turno';\n  if (isGear(id) && BAL.gearStart !== false && !free && !react && (G.combat || (G.phase !== 'prima' && G.phase !== 'inizio'))) return 'Gli equipaggiamenti si indossano solo a inizio turno';")
s = rep(s, "(atkOf(x, c) + 11) / 20", "(atkOf(x, c) + HIT_DIE() + 1 - (BAL.defBase ?? 14)) / HIT_DIE()")
s = rep(s, "await ask(p, 'Gioca fino a 2 carte, poi muoviti', o,", "await ask(p, 'Inizio turno: gioca fino a 2 carte (gli equipaggiamenti solo ora), poi muoviti', o,")
s = rep(s, "await ask(p, 'Puoi ancora giocare carte, poi chiudi il turno', o,", "await ask(p, 'Fine turno: puoi ancora giocare carte (non equipaggiamenti), poi chiudi il turno', o,")
# Chierico → Oracolo ovunque rimasto
s = s.replace("'Chierico'", "'Oracolo'").replace("Chierico:", "Oracolo:").replace("il Chierico", "l'Oracolo")
# «razza» diventa «specie» (Daniele, 27/10)
import re as _re
_M = {'razza': 'specie', 'razze': 'specie', 'Razza': 'Specie', 'Razze': 'Specie', 'RAZZA': 'SPECIE', 'RAZZE': 'SPECIE'}
s = _re.sub(r'\b(razz[ae]|Razz[ae]|RAZZ[AE])\b', lambda m: _M[m.group(1)], s)
open(out, 'w').write(s)
print('ok', len(src), '->', len(s))
