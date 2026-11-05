
// ===================== Espansione «Il Caos del Goblin · Le Crepe di MIMI» =====================
// Si accoda a physF.js (cat physF.js caos_add.js > physC.js). CX = JSON con le parti accese:
//  trav: 'any' | 'twin'  Attraversare il fondo (invece di tirare il D6 vai su un'altra Crepa / sulla gemella)
//  travMin: guadagno minimo in esagoni perché l'IA attraversi (default 2)
//  cob: true             Imboscata = pesca un segnalino Coboldo di MIMI (6: 2 Coboldi, 2 Frombolieri, 2 Borseggiatori)
//  cards: ['CA-01', ...] | 'all'   carte Caos nel mazzo comune
//  table: { 1: 'crollo', ... }      ritocchi della tabella D6 (vedi CASE)
const CX = JSON.parse(process.env.CX || '{}');
const CXN = { trav: 0, frug: 0, cob: 0, play: {} };
const CREP = () => BOARD.caos.map(H);
const twinOf = h => ({ c: 9 - h.c, r: 9 - h.r });
const freeHex = (h, p) => G.players.every(x => x === p || x.out || hexDist(x.pos, h) > 1);
const COBOLDI = [
  { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true },
  { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true },
  { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true },
  { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true },
];
if (CX.cobDef) Object.assign(COBOLDI, JSON.parse(JSON.stringify(CX.cobDef)));
function drawCard(p) {
  const used = new Set(G.players.flatMap(x => [...x.hand, ...x.discard, ...equipped(x)].map(baseId)));
  const c = shuffle(COMMON.filter(id => !used.has(id) && C(id).tipo !== 'TM'))[0];
  if (c) { p.hand.push(c); log(`${p.name} pesca «${C(c).nome}».`); }
}
// ---- Coboldi: Agguato (attacca per primo) e Borseggio (se ti colpisce scarti 1 carta a caso; se lo sconfiggi peschi 1 carta)
{ const _ct = combatTurn;
  combatTurn = async function (x, c, attacker) {
    if (attacker && c.round === 1 && c.foe.agguato && !c.agg) { c.agg = true; log(`${c.foe.name}: agguato! Attacca per primo.`, 'bad'); await attack(c.foe, c.p, c); if (dead(c.p)) return 'attacca'; }
    return _ct(x, c, attacker); };
  const _h = hurt;
  hurt = async function (t, n, c = null) { const d = await _h(t, n, c);
    if (d > 0 && c && c.foe && c.foe.borseggio && t === c.p && !c.stole && t.hand.length) { c.stole = true; log(`${c.foe.name} ti ruba una carta!`, 'bad'); randomDiscard(t, 1); }
    return d; };
  const _sc = scontro;
  scontro = async function (p, foe, kind) { await _sc(p, foe, kind); if (foe.borseggio && dead(foe) && !G.over) drawCard(p); };
}
// cobNoClue: chi batte un Coboldo pesca 1 carta invece di prendere l'Indizio (1 PE resta)
{ const _ac = addClue; addClue = async function (p, n = 1) { if (G.cobFight) { G.cobFight = false; drawCard(p); return; } return _ac(p, n); }; }
// ---- tabella D6 delle Crepe (con Attraversare il fondo e la Lanterna dei Coboldi)
const CASE = {
  crollo: async p => { log('Crollo! 2 danni.', 'bad'); await harm(p, 2); },
  imboscata: async p => { log('Imboscata dei Coboldi di MIMI!', 'bad');
    if (CX.cob) { G.cob = G.cob && G.cob.length ? G.cob : shuffle([...COBOLDI]); const d = G.cob.pop(); CXN.cob++; G.cobFight = !!CX.cobNoClue; try { await scontro(p, makeCreature(d, 1), 'creatura'); } finally { G.cobFight = false; } }
    else await scontro(p, makeCreature(BESTIARIO[0], 1), 'creatura'); },
  vento: async p => { const d = await roll(p, 6, 'Vento del Goblin');
    const hexes = allHexes().filter(h => { const x = hexDist(h, p.pos); return x >= 1 && x <= d && canStop(h); });
    const dest = await pickHex(p, hexes, `Vento del Goblin: fino a ${d} caselle`); p.prev = { ...p.pos }; p.pos = { ...dest }; await resolveArrival(p); },
  bottega: async p => { log('Bottega del Goblin: riprendi una carta dai tuoi scarti.', 'good'); await recover(p, 1); },
  mappa: async p => { log('Mappa perduta: un indizio!', 'gold'); await addClue(p); },
  scambio: async p => { const os = others2(p).filter(o => !o.out); const dT = x => hexDist(x.pos, G.treasure);
    const best = os.filter(o => isLocated(p) ? dT(o) < dT(p) - 1 : isLocated(o) && dT(o) < dT(p) - 1).sort((a, b) => dT(a) - dT(b))[0];
    if (best) { [p.pos, best.pos] = [best.pos, p.pos]; log(`${p.name} e ${best.name} si scambiano di posto!`, 'gold'); } },
  carta: async p => { log('Cianfrusaglia: peschi 1 carta.', 'good'); drawCard(p); },
  pe: async p => { log('Lezione del Caos: 1 PE.', 'good'); await addPE(p, 1); },
};
const TAB = Object.assign({ 1: 'crollo', 2: 'imboscata', 3: 'vento', 4: 'bottega', 5: 'mappa', 6: 'scambio' }, CX.table || {});
const RANK = { mappa: 6, imboscata: 4, bottega: 3, carta: 2.5, pe: 2.5, vento: 2, scambio: 1, crollo: 0 };
chaosEvent = async function (p) {
  if (CX.trav && isLocated(p)) {
    const cand = (CX.trav === 'twin' ? [twinOf(p.pos)] : CREP().filter(h => !same(h, p.pos))).filter(h => freeHex(h, p));
    const d0 = moveDist(p.pos, G.treasure), best = cand.sort((a, b) => moveDist(a, G.treasure) - moveDist(b, G.treasure))[0];
    if (best && moveDist(best, G.treasure) <= d0 - (CX.travMin || 2)) { tick('movimento'); p.prev = { ...p.pos }; p.pos = { ...best }; log(`${p.name} attraversa il fondo del baule.`, 'gold'); CXN.trav++; return; }
  }
  await frugare(p);
};
async function frugare(p, two = false) {
  CXN.frug++; let v = await roll(p, 6, 'Crepa');
  if (two || has(p, 'CA-04')) { const w = await roll(p, 6, 'Crepa (secondo dado)'); if (RANK[TAB[w]] > RANK[TAB[v]]) v = w; }
  await CASE[TAB[v]](p);
}
// IA da individuato: una Crepa raggiungibile vale quanto la Crepa d'arrivo più vicina al tesoro
if (CX.trav) { const _am = aiMove;
  aiMove = function (p, hexes) {
    if (!isLocated(p) || others2(p).some(x => x.ritual)) return _am(p, hexes);
    const cs = CREP(), sc = h => { let d = moveDist(h, G.treasure);
      if (cs.some(k => same(k, h))) { const o = (CX.trav === 'twin' ? [twinOf(h)] : cs.filter(k => !same(k, h))).filter(k => freeHex(k, p)); for (const k of o) { const dk = moveDist(k, G.treasure); if (dk <= moveDist(h, G.treasure) - (CX.travMin || 2)) d = Math.min(d, dk + 0.5); } }
      return d; };
    return hexes.slice().filter(canStop).sort((a, b) => sc(a) - sc(b))[0] || _am(p, hexes); };
}
// ---- carte Caos (mazzo comune)
const CA = {
  'CA-01': { nome: 'Biglia del nulla', tipo: 'TI', testo: 'Fruga in una Crepa da dove sei: tira il D6 sulla tabella del Caos. Mago: tira due D6 e scegli.' },
  'CA-02': { nome: 'Pagina strappata', tipo: 'TI', testo: 'Tira il D6: con 5 o 6 prendi 1 Indizio, altrimenti peschi 1 carta.' },
  'CA-03': { nome: 'Coboldo pentito', tipo: 'TI', testo: 'Durante uno scontro: un Coboldo di MIMI ti aiuta e infligge 3 danni al nemico.' },
  'CA-04': { nome: 'Lanterna dei Coboldi', tipo: 'TE', testo: 'Elmo. +1 AR. Sulle Crepe tiri due D6 e scegli quale tenere.' },
  'CA-05': { nome: 'Vento di nulla', tipo: 'TI', testo: 'Un avversario a tua scelta, nel suo prossimo turno, muove di 1 esagono soltanto.' },
  'CA-06': { nome: 'Risata del Goblin', tipo: 'TI', testo: 'Tutti tirano il D6, tu ne tiri due e tieni il più alto: chi fa il risultato più alto prende 1 Indizio (a pari merito nessuno).' },
};
for (const id in CA) CARD[id] = { id, ...CA[id] };
SLOT['CA-04'] = 'elmo';
{ const _eb = eqBonus; eqBonus = function (p) { const b = _eb(p); if (equipped(p).some(id => baseId(id) === 'CA-04')) { b.ar += 1; if (CX.chiLan && isC(p, 'Chierico')) b[CX.chiLan] += 1; } return b; }; }
DEF['CA-01'] = { when: 'fuori', need: p => CREP().length > 0 || 'Nessuna Crepa', fx: async p => { await frugare(p, isC(p, 'Mago')); }, ai: p => isLocated(p) ? 0.8 : 2.2 };
DEF['CA-02'] = { when: 'sempre', fx: async p => { const v = await roll(p, 6, 'Pagina strappata'); if (v >= (CX.magoPag && isC(p, 'Mago') ? 4 : 5)) await addClue(p); else drawCard(p); }, ai: p => isLocated(p) ? 0.5 : 3 };
DEF['CA-03'] = { when: 'scontro', fx: async p => { const f = foeOf(p); if (f) await hurt(f, CX.cob3 || 3, G.combat); if (CX.chiCob && isC(p, 'Chierico')) heal(p, CX.chiCob); }, ai: () => 3 };
DEF['CA-04'] = te(null);
DEF['CA-05'] = { when: 'fuori', fx: async p => { const o = defaultOpp(p); if (o) { o.slowNext = (o.slowNext || 0) + (CX.vento || 3); log(`Vento di nulla: ${o.name} muoverà di ${CX.vento || 3} in meno.`, 'bad'); } },
  ai: p => others2(p).some(o => !o.out && isLocated(o)) ? 3 : 1.5 };
{ const _r = roll; roll = async function (p, sides, label, o) { let v = await _r(p, sides, label, o); if (label === 'Movimento' && p && p.slowNext) { v -= p.slowNext; p.slowNext = 0; } return v; }; }
DEF['CA-06'] = { when: 'sempre', fx: async p => { const rs = []; for (const x of G.players.filter(x => !x.out)) { let v = await roll(x, 6, 'Risata del Goblin'); if (x === p) v = Math.max(v, await roll(x, 6, 'Risata del Goblin')); rs.push([x, v]); }
    const m = Math.max(...rs.map(r => r[1])), top = rs.filter(r => r[1] === m); if (top.length === 1 && !top[0][0].located) await addClue(top[0][0]); },
  ai: p => isLocated(p) ? 0 : 2.5 };
{ const given = new Set((EFF.match(/give:[A-Z]+-\d+/g) || []).map(t => t.slice(5)));
  const list = CX.cards === 'all' ? Object.keys(CA) : (CX.cards || []);
  for (const id of list) if (!given.has(id)) COMMON.push(id); }
// conteggi per il rapporto
{ const _pc = playCard; playCard = async function (p, id, o) { const ok = await _pc(p, id, o); if (ok && baseId(id).startsWith('CA-')) CXN.play[baseId(id)] = (CXN.play[baseId(id)] || 0) + 1; return ok; }; }
{ const _A = globalThis.AFTER; globalThis.AFTER = r => { _A(r); const g = r.games.length; console.log('CXSTAT ' + JSON.stringify({ trav: +(CXN.trav / g).toFixed(2), frug: +(CXN.frug / g).toFixed(2), cob: +(CXN.cob / g).toFixed(2), play: Object.fromEntries(Object.entries(CXN.play).map(([k, v]) => [k, +(v / g).toFixed(2)])) })); }; }
