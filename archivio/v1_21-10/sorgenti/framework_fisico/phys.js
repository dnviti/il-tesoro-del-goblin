// Modello della scatola fisica: 4 classi, 4 razze, niente D4, creature fisse, plancia stampata con Cripte.
CLASSES.splice(0, CLASSES.length, 'Guerriero', 'Ladro', 'Mago', 'Chierico');
for (const k of ['Sanguar', 'Yumaniani', 'Halfling', 'Tiefling']) delete RACES[k];
Object.assign(BAL, { noD4: true }, JSON.parse(process.env.BALX || '{}'));
makeCreature = function (def) { return { ...def, isCreature: true, pv: def.pv, maxpv: def.pv }; };
const rot = ([c, r]) => [[c, r], [9 - c, 9 - r]];
const both = L => L.flatMap(rot);
const H = ([c, r]) => ({ c, r });
const KEY = h => h.c + ',' + h.r;
const BASEB = {
  loc: both([[1, 4]]), fon: both([[4, 1]]), fab: both([[8, 1]]),
  caos: both([[4, 0], [3, 2], [7, 4], [4, 4], [9, 2]]),
  qs: both([[6, 0], [8, 0], [1, 1], [3, 1], [6, 1], [2, 2], [5, 2], [8, 2], [9, 1], [4, 3], [7, 3], [8, 3], [0, 3], [2, 4], [5, 4]]),
  crypts: [[3, 3], [6, 3], [3, 6], [6, 6]], block: [], slow: [], portals: [], bag: Object.assign({ creatura: 13, miniboss: 4, trappola: 5, indizio: 4, vuota: 4 }, JSON.parse(process.env.BAG || '{}')),
};
const VARIANTS = eval(require('fs').readFileSync(__dirname + '/boards.js', 'utf8'));
const BOARD = Object.assign({}, BASEB, VARIANTS[process.env.BOARD || 'base'] || {});
if (BOARD.mod) BOARD.mod(BOARD);
// NOCAOS=1: scatola base senza Caos del Goblin (le 10 caselle tornano sentiero); CAOSQ=1: diventano caselle «?»
if (process.env.NOCAOS) { if (process.env.CAOSQ) BOARD.qs = BOARD.qs.concat(BOARD.caos); BOARD.caos = []; }
if (process.env.CAOSX) BOARD.caos = BOARD.caos.slice(0, +process.env.CAOSX);
let COST = {}, EDGES = [], DIST = null; const DCACHE = {};
for (let i = COMMON.length - 1; i >= 0; i--) if (C(COMMON[i]).tipo === 'TM') COMMON.splice(i, 1);
function rebuild() {
  EDGES = (BOARD.activePortals ? BOARD.activePortals() : BOARD.portals);
  const sig = JSON.stringify([BOARD.block, BOARD.slow, EDGES]);
  if (DCACHE[sig]) { [COST, DIST, globalThis.IDX] = DCACHE[sig]; return; }
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
  globalThis.IDX = idx; DCACHE[sig] = [COST, DIST, idx];
}
moveDist = (a, b) => DIST[IDX[KEY(a)]][IDX[KEY(b)]];
canStop = h => COST[KEY(h)] !== Infinity;
newBoard = function () {
  const tiles = [];
  for (let r = 0; r < ROWS; r++) { tiles.push([]); for (let c = 0; c < COLS; c++) tiles[r].push({ type: 'vuota', revealed: true, done: true }); }
  SPAWNS.forEach((h, i) => { tiles[h.r][h.c] = { type: 'start', revealed: true, done: true, spawn: i + 1 }; });
  const put = (L, type) => L.forEach(([c, r]) => tiles[r][c] = { type, revealed: true, done: false });
  put(BOARD.loc, 'locanda'); put(BOARD.fon, 'fonte'); put(BOARD.fab, 'fabbro'); put(BOARD.caos, 'evento');
  const bag = []; for (const k in BOARD.bag) for (let i = 0; i < BOARD.bag[k]; i++) bag.push(k);
  shuffle(bag); BOARD.qs.forEach(([c, r], i) => tiles[r][c] = { type: bag[i % bag.length], revealed: false, done: false });
  return tiles;
};
const CRY = () => BOARD.crypts.map(H);
moveTreasure = function () {
  G.treasure = pick(CRY().filter(h => !same(h, G.treasure))); G.moves = (G.moves || 0) + 1;
  for (const p of G.players) { if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0; }
};
const _cg = createGame;
createGame = function (list, fast, rules) { _cg(list, fast, rules); G.treasure = pick(CRY()); rebuild(); };
// Regole del regolamento stampato (FIS=1): il Caos resta e scatta a ogni sosta, gli edifici valgono una volta per eroe
if (process.env.FIS) { const _ra = resolveArrival; const BLD = ['locanda', 'fonte', 'fabbro'];
  resolveArrival = async function (p) { const t = tileAt(p.pos); const k = p.pos.c + ',' + p.pos.r; p.usedB = p.usedB || {};
    if (BLD.includes(t.type)) { const was = t.done; t.done = !!p.usedB[k]; await _ra(p); if (!p.usedB[k] && t.done) p.usedB[k] = true; t.done = was || false; return; }
    if (t.type === 'evento') { t.done = false; await _ra(p); t.done = false; return; }
    return _ra(p); }; }

if (process.env.TEMPOX) Object.assign(TEMPO, JSON.parse(process.env.TEMPOX));
// BAGDRAW=1: i segnalini «?» non si piazzano a inizio partita, si pescano dal sacchetto quando ci si ferma
if (process.env.BAGDRAW) { const _ra2 = resolveArrival;
  resolveArrival = async function (p) { const t = tileAt(p.pos);
    if (t.qcell && !t.revealed && !t.done) { t.type = G.qbag.length ? G.qbag.pop() : 'vuota'; await _ra2(p); if (t.done && G.qbag.length) { t.type = 'vuota'; t.revealed = false; t.done = false; } return; }
    return _ra2(p); };
  const _nb = newBoard; newBoard = function () { const tiles = _nb(); const bag = []; for (const k in BOARD.bag) for (let i = 0; i < BOARD.bag[k]; i++) bag.push(k); shuffle(bag); globalThis.__qbag = bag;
    BOARD.qs.forEach(([c, r]) => { tiles[r][c].qcell = true; tiles[r][c].type = 'vuota'; }); return tiles; };
  const _cg2 = createGame; createGame = function (...a) { _cg2(...a); G.qbag = globalThis.__qbag; };
}
// ---- giocatore di prova (posto 0): effetti da misurare ----
const EFF = process.env.EFF || 'ctrl', WHEN = +(process.env.WHEN || 0);
const opp0 = p => others2(p).filter(x => !x.out);
async function applyEff(p) {
  const os = opp0(p), o = os[0];
  for (const e of EFF.split('+')) switch (e) {
    case 'ctrl': break;
    case 'att': p.base.att++; break; case 'ar': p.base.ar++; break; case 'mov': p.base.mov++; break;
    case 'pv': p.base.pv++; p.pv++; break;
    case 'clue': await addClue(p, 1); break;
    case 'card': { const used = new Set(G.players.flatMap(x => [...x.hand, ...x.discard])); const c = shuffle(COMMON.filter(id => !used.has(id) && C(id).tipo !== 'TM'))[0]; if (c) p.hand.push(c); break; }
    case 'nocard': randomDiscard(p, 1); break;
    case 'insp': p.insp = true; break;
    case 'pe': await addPE(p, 1); break;
    case 'skip': p.skip += 1; break;
    case 'oskip': loseTurns(o, 1); break;
    case 'oskipall': for (const x of os) loseTurns(x, 1); break;
    case 'heal3': heal(p, 3); break;
    case 'dmg2self': await harm(p, 2); break;
    case 'odmg3': await harm(o, 3); break;
    case 'odmg3all': for (const x of os) await harm(x, 3); break;
    case 'att3c': addMod(p, { label: 'x', att: 3, kind: 'scontri', n: 1 }); break;
    case 'adv1c': addMod(p, { label: 'x', adv: true, kind: 'scontri', n: 1 }); break;
    case 'ar2c': addMod(p, { label: 'x', ar: 2, kind: 'scontri', n: 1 }); break;
    case 'mov3t': addMod(p, { label: 'x', mov: 3, kind: 'turn' }); break;
    case 'recover': await recover(p, 1); break;
    case 'odisc': randomDiscard(o, 1); break;
    case 'oclue': if (o.clues > 0 && !o.located) { o.clues--; } break;
    case 'extra': gainTurns(p, 1); break;
    default: if (e.startsWith('give:')) p.hand.push(e.slice(5));
  }
}
const _ic = initClasses;
initClasses = async function () { await _ic(); for (const p of G.players) { const i = SPAWNS.findIndex(s => same(s, p.pos)); p.spawn0 = i + 1; } if (WHEN === 0 && EFF !== 'ctrl') await applyEff(G.players[0]); };
onTurnStart = async p => { if (BOARD.onTurn) BOARD.onTurn(p); if (WHEN > 0 && p.id === 0 && p.ownTurns === WHEN) await applyEff(p); };
{ const g = (EFF.match(/give:[A-Z]+-\d+/g) || []).map(t => t.slice(5)); for (const id of g) { let k = COMMON.indexOf(id); if (k >= 0) COMMON.splice(k, 1); for (const c in DECK) { k = DECK[c].indexOf(id); if (k >= 0) DECK[c].splice(k, 1); } } }
if (process.env.CLS0) { const _rp = randomPlayers; randomPlayers = function (n) { const l = _rp(n); const j = l.findIndex(x => x.cls === process.env.CLS0); if (j > 0) { [l[0].cls, l[j].cls] = [l[j].cls, l[0].cls]; } else if (j < 0) l[0].cls = process.env.CLS0; dealList(l); return l; }; }
// ---- risultati ----
const _sc = simCore;
globalThis.AFTER = r => {
  const byG = {}; r.rows.forEach(x => (byG[x.game] = byG[x.game] || []).push(x));
  const t0 = Object.values(byG).map(rs => rs[0]); const n = t0.length;
  const w = t0.reduce((a, x) => a + x.win, 0) / n; const exp = t0.reduce((a, x) => a + 1 / x.n, 0) / n;
  const tm = r.games.reduce((a, g) => a + g.time.tot, 0) / r.games.length / 60;
  const turns = r.games.reduce((a, g) => a + g.perPlayer, 0) / r.games.length;
  const sp = {}; r.rows.forEach(x => { const k = x.spawn0; sp[k] = sp[k] || [0, 0, 0]; sp[k][0] += x.win; sp[k][1] += 1 / x.n; sp[k][2]++; });
  const cl = {}; r.rows.forEach(x => { cl[x.cls] = cl[x.cls] || [0, 0]; cl[x.cls][0] += x.win; cl[x.cls][1] += 1 / x.n; });
  const tl = r.games.map(g => g.time.tot / 60).sort((a, b) => a - b);
  console.log('RES ' + JSON.stringify({ board: process.env.BOARD || 'base', eff: EFF, cls0: process.env.CLS0 || '', when: WHEN, n, win0: +(w * 100).toFixed(2), exp0: +(exp * 100).toFixed(2), delta: +((w - exp) * 100).toFixed(2), min: +tm.toFixed(2), ph: ['early','mid','late'].map(k => +(r.games.reduce((a, g) => a + g.time[k], 0) / r.games.length / 60).toFixed(1)), turns: +turns.toFixed(2), p10: +tl[Math.floor(tl.length * .1)].toFixed(1), p90: +tl[Math.floor(tl.length * .9)].toFixed(1), cls: Object.fromEntries(Object.entries(cl).map(([k, v]) => [k, +(v[0] / v[1]).toFixed(3)])), spawn: Object.fromEntries(Object.entries(sp).map(([k, v]) => [k, +(v[0] / v[1]).toFixed(3)])) }));
};
