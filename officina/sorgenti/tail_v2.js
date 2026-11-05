// ===================== Officina del Goblin: modello della scatola fisica (Web Worker) =====================
const BASE4 = ['Guerriero', 'Ladro', 'Mago', 'Oracolo'];
for (const k of ['Yumaniani', 'Halfling', 'Tiefling']) delete RACES[k]; // nella scatola base: Umani, Elfi, Nani, Orchi, Sanguar
// game.js è il gioco v2 (Carte Trama v2, 27/10): BAL è già quello della scatola base (5 PV, Difesa 14 + AR, 2 Indizi, nemici a livelli).
// Il Caos del Goblin è un'espansione: la plancia base non ha Crepe, RUN.caos le aggiunge.
const rotH = ([c, r]) => [[c, r], [9 - c, 9 - r]];
const bothH = L => L.flatMap(rotH);
const HX = ([c, r]) => ({ c, r });
const KEY = h => h.c + ',' + h.r;
const inCuore = ([c, r]) => c >= 2 && c <= 7 && r >= 2 && r <= 7;
const BASEB = {
  loc: bothH([[1, 4]]), fon: bothH([[4, 1]]), fab: bothH([[8, 1]]),
  caos: [],
  qs: bothH([[6, 0], [8, 0], [1, 1], [3, 1], [6, 1], [2, 2], [5, 2], [8, 2], [9, 1], [4, 3], [7, 3], [8, 3], [0, 3], [2, 4], [5, 4]]),
  crypts: [[3, 3], [6, 3], [3, 6], [6, 6]], block: [], slow: [], portals: [],
};
const CREPE = bothH([[4, 0], [3, 2], [7, 4], [4, 4], [9, 2]]); // espansione «Il Caos del Goblin»: 10 Crepe (da rifare sul mazzo v2)
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
const _nb = newBoard;
newBoard = function () {
  PHYS.q = BOARD.qs.map(h => [...h]); PHYS.cripta = BOARD.crypts.map(h => [...h]);
  const tiles = _nb();
  BOARD.caos.forEach(([c, r]) => tiles[r][c] = { type: 'evento', revealed: true, done: false, used: [] });
  return tiles;
};
const CRY = () => BOARD.crypts.map(HX);
moveTreasure = function () {
  const cand = CRY().filter(h => !same(h, G.treasure));
  if (cand.length) G.treasure = pick(cand); G.moves = (G.moves || 0) + 1;
  for (const p of G.players) { if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0; }
};
const _cg = createGame;
createGame = function (list, fast, rules) { rebuild(); _cg(list, fast, rules); };
// ---- carta nuova ----
randomPlayers = function (n) {
  const cls = shuffle([...BASE4]);
  if (RUN.cls0) { const j = cls.indexOf(RUN.cls0); if (j >= 0) [cls[0], cls[j]] = [cls[j], cls[0]]; else cls[0] = RUN.cls0; }
  const races = Object.keys(RACES);
  const list = cls.slice(0, n).map((c, i) => ({ name: `IA ${i + 1}`, ai: true, cls: c, race: pick(races), free: [pick(['att', 'mov', 'ar']), pick(['att', 'mov', 'ar'])], deck: [] }));
  dealList(list); return list;
};
const _ic = initClasses;
initClasses = async function () { await _ic(); for (const p of G.players) p.spawn0 = SPAWNS.findIndex(s => same(s, p.pos)) + 1; if (RUN.give) G.players[0].hand.push(RUN.give); };
const CUSTOM_EQ = {};
const _eqb = eqBonus;
eqBonus = function (p) { const b = _eqb(p); for (const id of equipped(p)) { const e = CUSTOM_EQ[baseId(id)]; if (e) for (const k in e) b[k] += e[k]; } return b; };
const RACE_TAG = { Umano: 'Umano', Elfo: 'Elfo', Nano: 'Nano', Orco: 'Orco', Sanguar: 'Sanguar' };
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
  if (card.cls && BASE4.includes(card.cls)) CARD[id].cls = card.cls; // classe di un'espansione: la prova un eroe della base
  delete CUSTOM_EQ[id];
  const fxs = (card.effects || []).filter(e => e.k !== 'libero');
  const reqOK = p => {
    if (card.req === 'pvBassi' && p.pv > 3) return 'Serve avere 3 PV o meno';
    if (card.req && card.req.startsWith('razza:') && !isR(p, RACE_TAG[card.req.slice(6)])) return 'Specie sbagliata';
    if (card.when === 'prima' && G.phase !== 'prima') return 'Si gioca prima di muoverti';
    return true;
  };
  const aiv = Math.max(1.6, Math.min(6, card.pp || 2));
  if (card.kind === 'equip') {
    SLOT[id] = { 'Elmo': 'elmo', 'Arma a una mano': 'dx', 'Scudo': 'dx', 'Arma a due mani': 'dx', 'Arma SX': 'sx', 'Corpo': 'armatura', 'Armatura': 'armatura' }[card.slot] || 'armatura';
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

// ---- espansione «Il Caos del Goblin · Le Crepe di MIMI»: è già nel gioco v2 (BAL.caos: Crepe gemelle, Coboldi, carte CA-01…06) ----
function setCaos(on) { RUN.caos = !!on; BAL.caos = RUN.caos; }
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
      const id = registerCard(m.card); RUN.cls0 = BASE4.includes(m.card.cls) ? m.card.cls : null; setCaos(m.caos); BOARD = baseBoard();
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
