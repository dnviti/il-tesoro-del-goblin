// ===================== Officina del Goblin: modello della scatola fisica (Web Worker) =====================
const BASE4 = ['Guerriero', 'Ladro', 'Mago', 'Chierico'];
for (const k of ['Sanguar', 'Yumaniani', 'Halfling', 'Tiefling']) delete RACES[k];
// game.js è già allineato alla scatola (BAL: niente D4, creature fisse, 3 slot, edifici una volta per eroe).
// Il Caos del Goblin è un'espansione dal 21/10 sera: la plancia base non ha Crepe, RUN.caos le aggiunge.
Object.assign(BAL, { board: 'fisica', noD4: true, creatureFixed: true, buildings: 'once', slots3: true });
// pacchetto di equilibrio della scatola base (thread del gioco fisico, 21/10 ore 13): Ladro +3 MOV, Guerriero +2 PV,
// Chierico torna in vita con 3 PV, TI-39 e TI-22 su un solo avversario, TI-52 = 2 Indizi a te e 1 a ogni avversario
Object.assign(BAL, { ladroMov: 3, chierRev: 3, foesOff: ['TE-14', 'TI-39', 'TI-22'], ti52: 'all', guerPV: 2, clsPV: {} }); // Ladro senza +1 PV (Daniele, 21/10 ore 14:57)
for (let i = COMMON.length - 1; i >= 0; i--) if (C(COMMON[i]).tipo === 'TM') COMMON.splice(i, 1);
const rotH = ([c, r]) => [[c, r], [9 - c, 9 - r]];
const bothH = L => L.flatMap(rotH);
const HX = ([c, r]) => ({ c, r });
const KEY = h => h.c + ',' + h.r;
const inCuore = ([c, r]) => c >= 2 && c <= 7 && r >= 2 && r <= 7;
const BASEB = {
  loc: bothH([[1, 4]]), fon: bothH([[4, 1]]), fab: bothH([[8, 1]]),
  caos: [],
  qs: bothH([[6, 0], [8, 0], [1, 1], [3, 1], [6, 1], [2, 2], [5, 2], [8, 2], [9, 1], [4, 3], [7, 3], [8, 3], [0, 3], [2, 4], [5, 4]]),
  crypts: [[3, 3], [6, 3], [3, 6], [6, 6]], block: [], slow: [], portals: [], bag: { creatura: 13, miniboss: 4, trappola: 5, indizio: 0, vuota: 8 },
};
const CREPE = bothH([[4, 0], [3, 2], [7, 4], [4, 4], [9, 2]]); // espansione «Il Caos del Goblin»: 10 Crepe
const RUN = { cls0: null, give: null, caos: false };
const baseBoard = () => RUN.caos ? Object.assign({}, BASEB, { caos: CREPE }) : BASEB;
let BOARD = BASEB;
function boardFrom(t) {
  const B0 = baseBoard();
  if (!t) return B0;
  return Object.assign({}, B0, {
    qs: BASEB.qs.filter(h => !inCuore(h)).concat(t.qs || []),
    caos: B0.caos.filter(h => !inCuore(h)).concat(t.caos || []), // sotto il Terreno le Crepe del Cuore restano nella scatola
    crypts: t.crypts || [], block: t.block || [], slow: t.slow || [], portals: t.portals || [],
  });
}
let COST = {}, DIST = null, IDX = {}; const DCACHE = {};
function rebuild() {
  const EDGES = BOARD.portals;
  const sig = JSON.stringify([BOARD.block, BOARD.slow, EDGES]);
  if (DCACHE[sig]) { [COST, DIST, IDX] = DCACHE[sig]; return; }
  COST = {}; for (const h of allHexes()) COST[KEY(h)] = 1;
  for (const b of BOARD.block) COST[b.join(',')] = Infinity;
  for (const b of BOARD.slow) COST[b.join(',')] = 2;
  const hs = allHexes(), idx = {}; hs.forEach((h, i) => idx[KEY(h)] = i);
  const nb = hs.map(h => neighbors(h).map(x => idx[KEY(x)]));
  for (const [a, b] of EDGES) { nb[idx[a.join(',')]].push(idx[b.join(',')]); nb[idx[b.join(',')]].push(idx[a.join(',')]); }
  const cost = hs.map(h => COST[KEY(h)]);
  DIST = hs.map((_, s) => { const d = hs.map(() => Infinity); d[s] = 0; const q = [s]; const seen = new Set();
    while (q.length) { q.sort((a, b) => d[a] - d[b]); const u = q.shift(); if (seen.has(u)) continue; seen.add(u);
      for (const v of nb[u]) { if (cost[v] === Infinity) continue; const nd = d[u] + cost[v]; if (nd < d[v]) { d[v] = nd; q.push(v); } } }
    return d; });
  IDX = idx; DCACHE[sig] = [COST, DIST, idx];
}
moveDist = (a, b) => { const v = DIST[IDX[KEY(a)]][IDX[KEY(b)]]; return v === undefined ? Infinity : v; };
canStop = h => COST[KEY(h)] !== Infinity;
newBoard = function () {
  const tiles = [];
  for (let r = 0; r < ROWS; r++) { tiles.push([]); for (let c = 0; c < COLS; c++) tiles[r].push({ type: 'vuota', revealed: true, done: true }); }
  SPAWNS.forEach((h, i) => { tiles[h.r][h.c] = { type: 'start', revealed: true, done: true, spawn: i + 1 }; });
  const put = (L, type) => L.forEach(([c, r]) => tiles[r][c] = { type, revealed: true, done: false, used: [] });
  put(BOARD.loc, 'locanda'); put(BOARD.fon, 'fonte'); put(BOARD.fab, 'fabbro'); put(BOARD.caos, 'evento');
  BOARD.crypts.forEach(([c, r], i) => tiles[r][c] = { type: 'cripta', revealed: true, done: true, crypt: i + 1 });
  const bag = []; for (const k in BOARD.bag) for (let i = 0; i < BOARD.bag[k]; i++) bag.push(k);
  shuffle(bag); BOARD.qs.forEach(([c, r], i) => tiles[r][c] = { type: bag[i % bag.length], revealed: false, done: false });
  return tiles;
};
const CRY = () => BOARD.crypts.map(HX);
moveTreasure = function () {
  const cand = CRY().filter(h => !same(h, G.treasure));
  if (cand.length) G.treasure = pick(cand); G.moves = (G.moves || 0) + 1;
  for (const p of G.players) { if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0; }
};
const _cg = createGame;
createGame = function (list, fast, rules) { _cg(list, fast, rules); rebuild(); G.treasure = pick(CRY()); };
// ---- carta nuova ----
randomPlayers = function (n) {
  const cls = shuffle([...BASE4]);
  if (RUN.cls0) { const j = cls.indexOf(RUN.cls0); if (j >= 0) [cls[0], cls[j]] = [cls[j], cls[0]]; else cls[0] = RUN.cls0; }
  const races = Object.keys(RACES);
  const list = cls.slice(0, n).map((c, i) => ({ name: `IA ${i + 1}`, ai: true, cls: c, race: pick(races), free: [pick(['att', 'mov', 'ar', 'pv']), pick(['att', 'mov', 'ar', 'pv'])], deck: [] }));
  dealList(list); return list;
};
const _ic = initClasses;
initClasses = async function () { await _ic(); for (const p of G.players) p.spawn0 = SPAWNS.findIndex(s => same(s, p.pos)) + 1; if (RUN.give) G.players[0].hand.push(RUN.give); };
const CUSTOM_EQ = {};
const _eqb = eqBonus;
eqBonus = function (p) { const b = _eqb(p); for (const id of equipped(p)) { const e = CUSTOM_EQ[baseId(id)]; if (e) for (const k in e) b[k] += e[k]; } return b; };
const RACE_TAG = { Umano: 'Umano', Elfo: 'Elfo', Nano: 'Nano', Orco: 'Orco' };
async function applyE(p, e, id) {
  const opps = others2(p).filter(x => !x.out);
  const lead = () => opps.slice().sort((a, b) => b.clues - a.clues)[0];
  switch (e.k) {
    case 'indizio': await addClue(p, e.n); break;
    case 'togliIndizio': for (const x of (e.t === 'ogni' ? opps : [lead()].filter(Boolean))) if (x.clues > 0 && !x.located) x.clues = Math.max(0, x.clues - e.n); break;
    case 'rubaIndizio': { const x = opps.filter(y => y.clues > 0 && !y.located).sort((a, b) => b.clues - a.clues)[0]; if (x) { x.clues--; await addClue(p, 1); } break; }
    case 'turnoAvv': for (const x of opps) loseTurns(x, e.n); break;
    case 'turnoExtra': gainTurns(p, e.n); break;
    case 'perdiTurno': p.skip += e.n; break;
    case 'statPerm': addMod(p, { label: 'carta', [e.s]: e.n }); break;
    case 'statScontri': addMod(p, { label: 'carta', [e.s]: e.n, kind: 'scontri', n: e.d }); break;
    case 'vantaggio': addMod(p, { label: 'carta', adv: true, kind: 'scontri', n: e.d }); break;
    case 'movTurno': addMod(p, { label: 'carta', mov: e.n, kind: 'turn' }); break;
    case 'riprendi': await recover(p, e.n, { except: id }); break;
    case 'scartaAvv': for (const x of opps) randomDiscard(x, e.n); break;
    case 'ispirazione': giveInsp(p, 'carta'); break;
    case 'pe': await addPE(p, e.n); break;
    case 'danniAvv': for (const x of (e.t === 'ogni' ? opps : [opps[0]].filter(Boolean))) await harm(x, e.n); break;
    case 'danniNemico': { const f = foeOf(p); if (f) await hurt(f, e.n, G.combat); break; }
    case 'malusNemico': { const f = foeOf(p); if (f) addCmod(G.combat, f, 'ar', -e.n); break; }
    case 'cura': heal(p, e.n); break;
    case 'perdiPV': await harm(p, e.n); break;
  }
}
function registerCard(card) {
  const id = 'NEW-01';
  const tipo = card.kind === 'incantesimo' ? 'TI' : 'TE';
  CARD[id] = { id, nome: card.nome || 'Carta nuova', tipo, testo: card.testo || '' };
  if (card.cls) CARD[id].cls = card.cls;
  delete CUSTOM_EQ[id];
  const fxs = (card.effects || []).filter(e => e.k !== 'libero');
  const reqOK = p => {
    if (card.req === 'pvBassi' && p.pv > 3) return 'Serve avere 3 PV o meno';
    if (card.req && card.req.startsWith('razza:') && !isR(p, RACE_TAG[card.req.slice(6)])) return 'Razza sbagliata';
    if (card.when === 'prima' && G.phase !== 'prima') return 'Si gioca prima di muoverti';
    return true;
  };
  const aiv = Math.max(1.6, Math.min(6, card.pp || 2));
  if (card.kind === 'equip') {
    SLOT[id] = { 'Elmo': 'elmo', 'Arma a una mano': '1h', 'Arma a due mani': '2h', 'Corpo': 'armatura' }[card.slot] || 'armatura';
    const eq = { att: 0, mov: 0, ar: 0, pv: 0 }; const once = [];
    for (const e of fxs) { if (e.k === 'statPerm') eq[e.s] += e.n; else once.push(e); }
    CUSTOM_EQ[id] = eq;
    DEF[id] = te(async (p, o, cid) => { for (const e of once) await applyE(p, e, cid); }, { need: p => reqOK(p) });
  } else {
    SLOT[id] = card.kind === 'pozione' ? 'pozione' : undefined;
    if (SLOT[id] === undefined) delete SLOT[id];
    DEF[id] = { when: card.when === 'scontro' ? 'scontro' : card.when === 'prima' ? 'fuori' : 'sempre', need: p => reqOK(p),
      fx: async (p, o, cid) => { for (const e of fxs) await applyE(p, e, cid); }, ai: () => aiv };
  }
  return id;
}

// ---- espansione «Il Caos del Goblin · Le Crepe di MIMI» (v2.0, 21/10 sera): attiva con RUN.caos ----
// Crepe gemelle (si fruga col D6 o si salta sulla gemella), 6 Coboldi di MIMI (chi li batte pesca 1 carta, niente Indizio), 6 carte Caos nel mazzo comune.
// Stesso modello di sorgenti/framework/caos_add.js.
const twinOf = h => ({ c: 9 - h.c, r: 9 - h.r });
const CREPH = () => RUN.caos ? CREPE.filter(k => BOARD.caos.some(b => b[0] === k[0] && b[1] === k[1])).map(HX) : []; // solo le Crepe, non gli Eventi del Terreno
const freeHex = (h, p) => G.players.every(x => x === p || x.out || hexDist(x.pos, h) > 1);
const COBOLDI = [
  { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] }, { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true }, { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true },
  { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true }, { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true },
];
function drawCard(p) {
  const used = new Set(G.players.flatMap(x => [...x.hand, ...x.discard, ...equipped(x)].map(baseId)));
  const c = shuffle(COMMON.filter(id => !used.has(id) && C(id).tipo !== 'TM'))[0]; if (c) p.hand.push(c);
}
{ const _ct = combatTurn;
  combatTurn = async function (x, c, attacker) {
    if (attacker && c.round === 1 && c.foe.agguato && !c.agg) { c.agg = true; await attack(c.foe, c.p, c); if (dead(c.p)) return 'attacca'; }
    return _ct(x, c, attacker); };
  const _h = hurt;
  hurt = async function (t, n, c = null) { const d = await _h(t, n, c);
    if (d > 0 && c && c.foe && c.foe.borseggio && t === c.p && !c.stole && t.hand.length) { c.stole = true; randomDiscard(t, 1); }
    return d; };
  const _sc = scontro;
  scontro = async function (p, foe, kind) { await _sc(p, foe, kind); if (foe.borseggio && dead(foe) && !G.over) drawCard(p); };
}
{ const _ac = addClue; addClue = async function (p, n = 1) { if (G.cobFight) { G.cobFight = false; drawCard(p); return; } return _ac(p, n); }; } // i Coboldi non danno Indizi: chi li batte pesca 1 carta
const CRANK = [0, 0, 4, 2, 3, 6, 1]; // valore per l'IA dei risultati 1-6 (per la Lanterna dei Coboldi)
chaosEvent = async function (p) {
  if (RUN.caos && isLocated(p) && CREPH().some(k => same(k, p.pos))) { const t = twinOf(p.pos);
    if (freeHex(t, p) && moveDist(t, G.treasure) <= moveDist(p.pos, G.treasure) - 2) { p.prev = { ...p.pos }; p.pos = t; log(`${p.name} attraversa il fondo del baule.`, 'gold'); return; } }
  await frugare(p);
};
async function frugare(p, two = false) {
  let v = await roll(p, 6, 'Crepa');
  if (two || equipped(p).some(id => baseId(id) === 'CA-04')) { const w = await roll(p, 6, 'Crepa (secondo dado)'); if (CRANK[w] > CRANK[v]) v = w; }
  switch (v) {
    case 1: await harm(p, 2); break;
    case 2: { if (!RUN.caos) { await scontro(p, makeCreature(BESTIARIO[0], 1), 'creatura'); break; }
      G.cob = G.cob && G.cob.length ? G.cob : shuffle([...COBOLDI]); G.cobFight = true; try { await scontro(p, makeCreature(G.cob.pop(), 1), 'creatura'); } finally { G.cobFight = false; } break; }
    case 3: { const d = await roll(p, 6, 'Vento del Goblin'); const hexes = allHexes().filter(h => { const x = moveDist(p.pos, h); return x >= 1 && x <= d && canStop(h); });
      const dest = await pickHex(p, hexes, 'Vento del Goblin'); p.prev = { ...p.pos }; p.pos = { ...dest }; await resolveArrival(p); break; }
    case 4: await recover(p, 1); break;
    case 5: await addClue(p); break;
    case 6: { const os = others2(p).filter(o => !o.out); const dT = x => hexDist(x.pos, G.treasure);
      const best = os.filter(o => isLocated(p) ? dT(o) < dT(p) - 1 : isLocated(o) && dT(o) < dT(p) - 1).sort((a, b) => dT(a) - dT(b))[0];
      if (best) [p.pos, best.pos] = [best.pos, p.pos]; break; }
  }
}
{ const _am = aiMove;
  aiMove = function (p, hexes) {
    if (!RUN.caos || !isLocated(p) || others2(p).some(x => x.ritual)) return _am(p, hexes);
    const cs = CREPH(), sc = h => { const d = moveDist(h, G.treasure);
      if (cs.some(k => same(k, h))) { const t = twinOf(h); const dt = moveDist(t, G.treasure); if (freeHex(t, p) && dt <= d - 2) return dt + 0.5; }
      return d; };
    return hexes.slice().filter(canStop).sort((a, b) => sc(a) - sc(b))[0] || _am(p, hexes); };
}
const CA = {
  'CA-01': { nome: 'Biglia del nulla', tipo: 'TI', testo: 'Fruga in una Crepa da dove sei: tira il D6 sulla tabella del Caos. Mago: tira due D6 e scegli.' },
  'CA-02': { nome: 'Pagina strappata', tipo: 'TI', testo: 'Tira il D6: con 5 o 6 prendi 1 Indizio, altrimenti peschi 1 carta. Mago: basta un 4.' },
  'CA-03': { nome: 'Coboldo pentito', tipo: 'TI', testo: 'Durante uno scontro: un Coboldo di MIMI infligge 3 danni al nemico.' },
  'CA-04': { nome: 'Lanterna dei Coboldi', tipo: 'TE', testo: 'Elmo. +1 AR (Chierico: anche +1 ATT). Quando frughi in una Crepa tira due D6 e scegli quale tenere.' },
  'CA-05': { nome: 'Vento di nulla', tipo: 'TI', testo: 'Un avversario a tua scelta, nel suo prossimo turno, muove di 1 esagono soltanto.' },
  'CA-06': { nome: 'Risata del Goblin', tipo: 'TI', testo: 'Tutti tirano il D6, tu due e tieni il più alto: il risultato più alto prende 1 Indizio (a pari merito nessuno).' },
};
for (const id in CA) CARD[id] = { id, ...CA[id] };
SLOT['CA-04'] = 'elmo';
{ const _eb = eqBonus; eqBonus = function (p) { const b = _eb(p); if (equipped(p).some(id => baseId(id) === 'CA-04')) { b.ar += 1; if (isC(p, 'Chierico')) b.att += 1; } return b; }; }
DEF['CA-01'] = { when: 'fuori', need: p => CREPH().length > 0 || 'Nessuna Crepa', fx: async p => { await frugare(p, isC(p, 'Mago')); }, ai: p => isLocated(p) ? 0.8 : 2.2 };
DEF['CA-02'] = { when: 'sempre', fx: async p => { const v = await roll(p, 6, 'Pagina strappata'); if (v >= (isC(p, 'Mago') ? 4 : 5)) await addClue(p); else drawCard(p); }, ai: p => isLocated(p) ? 0.5 : 3 };
DEF['CA-03'] = { when: 'scontro', fx: async p => { const f = foeOf(p); if (f) await hurt(f, 3, G.combat); }, ai: () => 3 };
DEF['CA-04'] = te(null);
DEF['CA-05'] = { when: 'fuori', fx: async p => { const o = defaultOpp(p); if (o) o.slowNext = 1; }, ai: p => others2(p).some(o => !o.out && isLocated(o)) ? 3 : 1.5 };
{ const _r = roll; roll = async function (p, sides, label, o) { let v = await _r(p, sides, label, o); if (label === 'Movimento' && p && p.slowNext) { v = -99; p.slowNext = 0; } return v; }; } // Vento di nulla: muove di 1 soltanto
DEF['CA-06'] = { when: 'sempre', fx: async p => { const rs = []; for (const x of G.players.filter(x => !x.out)) { let v = await roll(x, 6, 'Risata del Goblin'); if (x === p) v = Math.max(v, await roll(x, 6, 'Risata del Goblin')); rs.push([x, v]); }
    const m = Math.max(...rs.map(r => r[1])), top = rs.filter(r => r[1] === m); if (top.length === 1 && !top[0][0].located) await addClue(top[0][0]); },
  ai: p => isLocated(p) ? 0 : 2.5 };
function setCaos(on) { RUN.caos = !!on; for (const id in CA) { const k = COMMON.indexOf(id); if (k >= 0) COMMON.splice(k, 1); } if (RUN.caos) COMMON.push(...Object.keys(CA)); }
function summarize(r) {
  const byG = {}; r.rows.forEach(x => (byG[x.game] = byG[x.game] || []).push(x));
  const t0 = Object.values(byG).map(rs => rs[0]); const n = t0.length;
  const w = t0.reduce((a, x) => a + x.win, 0) / n, exp = t0.reduce((a, x) => a + 1 / x.n, 0) / n;
  const min = r.games.reduce((a, g) => a + g.time.tot, 0) / r.games.length / 60;
  const cl = {}; r.rows.forEach(x => { cl[x.cls] = cl[x.cls] || [0, 0]; cl[x.cls][0] += x.win; cl[x.cls][1] += 1 / x.n; });
  const sp = {}; r.rows.forEach(x => { const k = x.spawn0; sp[k] = sp[k] || [0, 0]; sp[k][0] += x.win; sp[k][1] += 1 / x.n; });
  const idx = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, v[0] / v[1]]));
  return { n, win0: w * 100, exp0: exp * 100, min, turns: r.games.reduce((a, g) => a + g.perPlayer, 0) / r.games.length, cls: idx(cl), spawn: idx(sp) };
}
async function arm(n, np, label, step, steps) {
  SIM = { running: true, stop: false };
  const r = await simCore(n, String(np), 'std', (i, N) => postMessage({ type: 'progress', label, done: (step + i / N) / steps }));
  return summarize(r);
}
onmessage = async ev => {
  const m = ev.data;
  try {
    if (m.cmd === 'card') {
      const id = registerCard(m.card); RUN.cls0 = m.card.cls || null; setCaos(m.caos); BOARD = baseBoard();
      RUN.give = null; const ctrl = await arm(m.n, 2, 'Partite senza la carta', 0, 2);
      RUN.give = id; const test = await arm(m.n, 2, 'Partite con la carta', 1, 2);
      RUN.give = null;
      postMessage({ type: 'result', cmd: 'card', ctrl, test });
    } else if (m.cmd === 'board') {
      RUN.cls0 = null; RUN.give = null; setCaos(m.caos); const out = {};
      let step = 0; const steps = m.nps.length * 2;
      for (const np of m.nps) {
        BOARD = baseBoard(); const base = await arm(m.n, np, `Plancia base${RUN.caos ? ' con il Caos' : ''}, ${np} giocatori`, step++, steps);
        BOARD = boardFrom(m.terreno); const test = await arm(m.n, np, `Il tuo Terreno, ${np} giocatori`, step++, steps);
        out[np] = { base, test };
      }
      BOARD = BASEB;
      postMessage({ type: 'result', cmd: 'board', out });
    }
  } catch (err) { postMessage({ type: 'error', message: String(err && err.message || err) }); }
};
postMessage({ type: 'ready' });
