// ===================== Dati =====================
const CARD = Object.fromEntries(CARDS.map(c => [c.id, c]));
const baseId = id => id.split('~')[0];
const C = id => CARD[baseId(id)];
const rnd = n => 1 + Math.floor(Math.random() * n);
const pick = a => a[Math.floor(Math.random() * a.length)];
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const sleep = ms => new Promise(r => setTimeout(r, ms));
const fmt = n => (n >= 0 ? '+' : '') + n;
const esc = s => String(s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));

const RACES = {
  Umani: { tag: 'Umano', fixed: { mov: 1 }, free: 1, info: '+1 MOV e +1 a una statistica a scelta' },
  Sanguar: { tag: 'Sanguar', fixed: { mov: 2, pv: 1 }, free: 0, info: '+2 MOV e +1 PV. Razza di non morti' },
  Nani: { tag: 'Nano', fixed: {}, free: 2, info: '+1 a due statistiche a scelta' },
  Yumaniani: { tag: 'Aasimar', fixed: { pv: 1 }, free: 1, info: '+1 PV e +1 a una statistica a scelta. Valgono come Aasimar per le carte' },
  Orchi: { tag: 'Orco', fixed: { att: 2, pv: 1 }, free: 0, info: '+2 ATT e +1 PV' },
  Elfi: { tag: 'Elfo', fixed: {}, free: 2, info: '+2 a statistiche a scelta' },
  Halfling: { tag: 'Halfling', fixed: { mov: 1, ar: 1 }, free: 0, info: 'Razza aggiunta (citata dalle carte): +1 MOV e +1 AR' },
  Tiefling: { tag: 'Tiefling', fixed: { att: 1 }, free: 1, info: 'Razza aggiunta (citata dalle carte): +1 ATT e +1 a scelta' },
};
const STATN = { pv: 'PV', att: 'ATT', mov: 'MOV', ar: 'AR' };
const CLASSES = ['Barbaro', 'Bardo', 'Chierico', 'Druido', 'Guerriero', 'Ladro', 'Mago', 'Paladino', 'Stregone', 'Warlock'];
const CLASS_CARD = Object.fromEntries(CLASSES.map((c, i) => [c, 'TC-' + String(i + 1).padStart(2, '0')]));

const SLOT = {};
['TE-02', 'TE-03', 'TE-05', 'TE-26'].forEach(i => SLOT[i] = '2h');
['TE-06', 'TE-07', 'TE-08', 'TE-11', 'TE-24', 'TE-25'].forEach(i => SLOT[i] = '1h');
['TE-12', 'TE-13', 'TE-14'].forEach(i => SLOT[i] = 'elmo');
['TE-04', 'TE-09', 'TE-10', 'TE-15'].forEach(i => SLOT[i] = 'armatura');
SLOT['TE-23'] = 'scudo';
SLOT['CA-04'] = 'elmo';
['TE-01', 'TE-22', 'TE-27'].forEach(i => SLOT[i] = 'accessorio');
['TE-16', 'TE-17', 'TE-18', 'TE-19', 'TE-20', 'TE-21'].forEach(i => SLOT[i] = 'pozione');
const POTIONS = ['TE-16', 'TE-17', 'TE-18', 'TE-19', 'TE-20', 'TE-21'];
const SLOTN_5 = { elmo: 'Elmo', dx: 'Arma DX / Scudo', sx: 'Arma SX', armatura: 'Armatura', accessorio: 'Accessorio' };
const SLOTN_3 = { elmo: 'Elmo', dx: 'Arma', armatura: 'Corpo' };
let SLOTN = SLOTN_5;
const SLOT_LABEL = { '2h': 'Arma a due mani', '1h': 'Arma a una mano', elmo: 'Elmo', armatura: 'Armatura', scudo: 'Scudo (slot Arma DX)', accessorio: 'Accessorio', pozione: 'Pozione (consumabile)' };

const BESTIARIO = [
  { name: 'Coboldo', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Ratto gigante', pv: 3, att: 2, ar: 0, dmg: [4, 0] },
  { name: 'Scheletro', pv: 5, att: 2, ar: 1, dmg: [4, 0] },
  { name: 'Lupo grigio', pv: 5, att: 3, ar: 0, dmg: [4, 0] },
  { name: 'Orchetto predone', pv: 6, att: 2, ar: 1, dmg: [6, 0] },
  { name: 'Ragno delle grotte', pv: 5, att: 3, ar: 1, dmg: [4, 0] },
  { name: 'Melma acida', pv: 7, att: 1, ar: 0, dmg: [6, 0] },
  { name: 'Gnomo schiavista', pv: 4, att: 2, ar: 2, dmg: [4, 0] },
];
const MINIBOSS = [
  { name: 'Ogre delle paludi', pv: 12, att: 3, ar: 1, dmg: [6, 1] },
  { name: 'Troll di fiume', pv: 11, att: 3, ar: 2, dmg: [6, 0] },
  { name: 'Capitano goliath', pv: 10, att: 4, ar: 2, dmg: [6, 0] },
  { name: 'Strega del vischio', pv: 9, att: 4, ar: 1, dmg: [6, 1] },
];
const BOSS = { name: 'Guardiano di MIMI', pv: 14, att: 4, ar: 3, dmg: [6, 1] };
const BEHOLDER = { name: 'Beholder', pv: 15, att: 3, ar: 2, dmg: [6, 1], beholder: true };

const TILE = {
  start: { n: 'Punto di spawn', g: '' },
  vuota: { n: 'Sentiero tranquillo', g: '' },
  q: { n: 'Segnalino Esplorazione', g: '?' },
  creatura: { n: 'Creatura', g: '⚔' },
  miniboss: { n: 'Mini-boss', g: '♛' },
  locanda: { n: 'Locanda', g: '⌂' },
  fonte: { n: 'Fonte', g: '≈' },
  fabbro: { n: 'Fabbro', g: '⚒' },
  trappola: { n: 'Trappola', g: '✕' },
  indizio: { n: 'Mappa strappata (indizio)', g: '✦' },
  evento: { n: 'Crepa del Caos', g: '✷' },
  cripta: { n: 'Cripta', g: '⚱' },
};
// Regole standard (Daniele): plancia 10×10, 6 partenze tirate con D6, movimento D6 + MOV
const RULES_STD = { size: 10, spawns: 6, die: 6 };
// Tabella di bilanciamento delle classi (tarata con il simulatore)
const BAL = { caos: false, te18: 'cless', ti45: 'dietroPV', te21: 4, tm05: 'mov1', board: 'fisica', buildings: 'once', bagDraw: true, slots3: true, scudoArma: true, chierRev: 3, clsPV: {}, creatureFixed: true, bottega: 'recover', imbCoboldo: true, locCatch: true, skipCapFoe: 3, behPV: 12, setupEquip: true, ti54: 'clue', noD4: true, tempesta: 2, strBonus: 1, ti22: 2, fatuo: [2, 2], imp: [3, 2], magoPerTurn: true, magoRerolls: 2, palHeals: 5, palPerTurn: false, furyAtt: 3, furyDmg: 1, ladroDiscard: false, ladroAdv: true, chierico: 'locanda', guerInsp: true, te25: 'ar', ti46: 'assorbi', te10: 2, mutaClue: false, ti12: 2, ashafe: [0, 1], arconte: 'clues2', zarkoAI: true, dragoAI: true, te22ar: false, ti30: 1, ti32: 1, ladroMov: 3, mimik: 'stay', dardo: 2, zarko: [10, 4], drago: [8, 4], te27: 3, muta: 3, ti23att: 0, te11: 1, te09mov: 1, te25ar: 1, te22att: false, ti39: true, te07: 2, zarkoRitual: true, servDmg: 1, impDmg: 3, allOpp: true, servPvP: true, ti52: 'all', pvpLevel: false, lupo: [3, 1], colpoRange: 2, canzoneMax: 1, ti15: 2, arconteAll: true, skipCap: 99, defeatPE: 0, tiles: { evento: 10 }, bossPV: 14, clock: 0, clockEvery: 2, pity: 0, maxMoves: 2, omen: [8, 3], foesOff: ['TE-14', 'TI-39', 'TI-22'], forgiatore: [0, 2], barbHeal: 0, patto: 'half', pvpFlee: 1.2, pattoOscuro: 1, ti01dmg: 1, ti20: 1, arconteClue: 'lead', arconteDmg: 3, punizione: 5, luce: 3, guerAR: 2, guerPV: 2, clsMov: { Stregone: 2 }, furyMov: 2, ti19mov: 2 };
// Tempo di gioco umano stimato: secondi a tavolo per ogni azione (regolabili nel simulatore)
// secondi per azione: «Al tavolo» (gioco da tavolo, misurato dal thread del gioco fisico) e «Digitale» (ritmo da app)
const TEMPI = {
  tavolo: { turno: 25, dado: 6, carta: 35, movimento: 18, casella: 12, scontro: 20, attacco: 12, livello: 20, sconfitta: 40 },
  digitale: { turno: 15, dado: 4, carta: 25, movimento: 12, casella: 8, scontro: 15, attacco: 8, livello: 15, sconfitta: 20 },
};
const TEMPO = { ...TEMPI.tavolo };
// ricalcola i secondi di una partita con un altro ritmo, dai conteggi delle azioni
function timeWith(t, T) { const o = { tot: 0 }; for (const st of ['early', 'mid', 'late']) { o[st] = 0; for (const k in t.n[st]) o[st] += t.n[st][k] * (T[k] || 0); o.tot += o[st]; } return o; }
// fasi: inizio fino al primo indizio di qualcuno, centro fino a quando qualcuno individua il tesoro, finale fino alla vittoria
function tick(k, n = 1) { if (!G || !G.time || G.setup) return; const s = TEMPO[k] * n; G.time.tot += s; G.time[G.stage] += s; const c = G.time.n[G.stage]; c[k] = (c[k] || 0) + n; }
function mark(k) { if (G && G.time && G.time.m[k] === undefined) G.time.m[k] = G.time.tot; }
function stageUp(st) { const o = ['early', 'mid', 'late']; if (o.indexOf(st) > o.indexOf(G.stage)) { G.stage = st; G.time.at[st] = G.round; } }
const movesLeft = () => (G.moves || 0) < BAL.maxMoves;
// con 3-4 giocatori le carte che rallentano colpiscono ogni avversario (stesso peso che in 2)
const FOES = new Set(['TE-14', 'TE-18', 'TI-10', 'TI-12', 'TI-16', 'TI-28', 'TI-37', 'TI-22', 'TI-39']);
const foes = (p, o) => BAL.allOpp && FOES.has(G.curCard) && !BAL.foesOff.includes(G.curCard) ? others2(p) : [o];
let COLS = 10, ROWS = 10, SPAWNS = [];
// 10×10 con 10 spawn: disposizione fissa condivisa con la plancia fisica (B1, E1, H1, J4, J7, I10, F10, C10, A7, A4)
const SPAWNS_STD = [
  ...[1, 4, 7].map(c => ({ c, r: 0 })),
  ...[3, 6].map(r => ({ c: 9, r })),
  ...[8, 5, 2].map(c => ({ c, r: 9 })),
  ...[6, 3].map(r => ({ c: 0, r })),
];
// 6 partenze (plancia fisica): C1, H1, J5, H10, C10, A6, in senso orario e simmetriche a mezzo giro
const SPAWNS_6 = [{ c: 2, r: 0 }, { c: 7, r: 0 }, { c: 9, r: 4 }, { c: 7, r: 9 }, { c: 2, r: 9 }, { c: 0, r: 5 }];
function perimeter(n) {
  const o = [];
  for (let c = 0; c < n; c++) o.push({ c, r: 0 });
  for (let r = 1; r < n; r++) o.push({ c: n - 1, r });
  for (let c = n - 2; c >= 0; c--) o.push({ c, r: n - 1 });
  for (let r = n - 2; r >= 1; r--) o.push({ c: 0, r });
  return o;
}
function makeSpawns(n, k) {
  if (n === 10 && k === 10) return SPAWNS_STD.map(h => ({ ...h }));
  if (n === 10 && k === 6) return SPAWNS_6.map(h => ({ ...h }));
  const per = perimeter(n), P = per.length, out = [];
  for (let i = 0; i < k; i++) { const h = per[Math.floor((i + 0.5) * P / k) % P]; if (!out.some(x => x.c === h.c && x.r === h.r)) out.push(h); }
  return out;
}
function applyRules(r) { COLS = ROWS = r.size; SPAWNS = makeSpawns(r.size, r.spawns); }
applyRules(RULES_STD);

// ===================== Stato =====================
let G = null;
let pending = null;
let flashMsg = '';
let GEN = 0;
const S = {
  die: 6, speed: 650,
  n: 2,
  players: [
    { name: 'Giocatore 1', ai: false, race: 'Umani', cls: 'Guerriero', free: ['att', 'att'], deck: [] },
    { name: 'Geronimo (IA)', ai: true, race: 'Orchi', cls: 'Barbaro', free: ['att', 'att'], deck: [] },
    { name: 'Mimì (IA)', ai: true, race: 'Elfi', cls: 'Druido', free: ['att', 'ar'], deck: [] },
    { name: 'Gnomo (IA)', ai: true, race: 'Nani', cls: 'Mago', free: ['ar', 'pv'], deck: [] },
  ],
};

const live = () => G.players.filter(x => !x.out);
const others2 = p => live().filter(x => x !== p);
function defaultOpp(p) {
  const os = others2(p);
  if (!os.length) return G.players.find(x => x !== p);
  return os.slice().sort((a, b) => (isLocated(b) - isLocated(a)) || (b.clues - a.clues) || (b.level - a.level) || (a.id - b.id))[0];
}
const opp = p => (p._target && !p._target.out && p._target !== p) ? p._target : defaultOpp(p);
// carte che colpiscono «l'avversario»: con più di 2 giocatori chi gioca sceglie il bersaglio
const TARG = new Set(['TE-08', 'TE-14', 'TE-18', 'TI-04', 'TI-10', 'TI-11', 'TI-12', 'TI-14', 'TI-16', 'TI-21', 'TI-22', 'TI-24', 'TI-25', 'TI-26', 'TI-28', 'TI-29', 'TI-30', 'TI-35', 'TI-37', 'TI-41', 'TI-45']);
const TARG_LOCATED = new Set(['TI-04', 'TI-41']);
const isR = (p, ...t) => t.includes(RACES[p.race].tag);
const isC = (p, ...c) => c.some(x => p.classes.includes(x));
const equipped = p => [...new Set(Object.values(p.equip).filter(Boolean))];
const weapons = p => equipped(p).filter(id => ['1h', '2h'].includes(SLOT[baseId(id)]));
const has = (p, bid) => equipped(p).some(id => baseId(id) === bid);
const same = (a, b) => a.c === b.c && a.r === b.r;
const sb = p => isC(p, 'Stregone') ? BAL.strBonus : 0;

function log(t, cls = '') { if (!G) return; G.log.unshift({ t, cls }); if (G.log.length > 160) G.log.pop(); }

// ===================== Esagoni =====================
function cube(h) { const x = h.c - (h.r - (h.r & 1)) / 2; const z = h.r; return [x, -x - z, z]; }
function hexDist(a, b) { const A = cube(a), B = cube(b); return Math.max(Math.abs(A[0] - B[0]), Math.abs(A[1] - B[1]), Math.abs(A[2] - B[2])); }
function allHexes() { const o = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) o.push({ c, r }); return o; }
function neighbors(h) { return allHexes().filter(x => hexDist(x, h) === 1); }
const tileAt = h => G.tiles[h.r][h.c];

// ===================== Statistiche =====================
function eqBonus(p) {
  const b = { att: 0, mov: 0, ar: 0, pv: 0, adv: 0, dis: 0 };
  for (const id of equipped(p)) {
    switch (baseId(id)) {
      case 'TE-01': b.mov += isR(p, 'Aasimar', 'Tiefling') ? 2 : 1; break;
      case 'TE-02': b.att += 2; if (isR(p, 'Elfo')) b.adv++; break;
      case 'TE-03': b.mov += 1; b.att += isR(p, 'Elfo') ? 3 : 2; break;
      case 'TE-04': b.ar += 2; if (isC(p, 'Paladino')) b.pv += 2; if (isC(p, 'Guerriero')) { b.adv++; if (BAL.te04mov !== false) b.mov++; } break;
      case 'TE-05': b.att += 3; if (isC(p, 'Barbaro')) b.ar++; break;
      case 'TE-06': b.att += 1; break;
      case 'TE-07': b.att += isC(p, 'Mago') ? BAL.te07 : 1; break;
      case 'TE-11': b.att += isC(p, 'Ladro') ? BAL.te11 : 1; break;
      case 'TE-08': b.att += 2; b.dis++; break;
      case 'TE-09': b.ar += isC(p, 'Ladro', 'Bardo') ? 2 : 1; if (isC(p, 'Ladro')) b.mov += BAL.te09mov; break;
      case 'TE-10': b.ar += 2; break;
      case 'CA-04': b.ar += 1; if (isC(p, 'Chierico')) b.att++; break;
      case 'TE-12': b.ar += 2; if (isR(p, 'Nano')) b.adv++; if (isC(p, 'Guerriero')) b.att++; break;
      case 'TE-13': b.ar += 2; if (isC(p, 'Guerriero') && BAL.te13mov !== false) b.mov++; break;
      case 'TE-14': b.ar += 1; break;
      case 'TE-15': b.ar += isC(p, 'Warlock') ? 4 : 2; break;
      case 'TE-22': b.mov += isR(p, 'Elfo') ? 2 : 1; if (isC(p, 'Druido')) { if (BAL.te22att) b.att++; if (BAL.te22ar) b.ar++; } break;
      case 'TE-23': b.ar += 3; break;
      case 'TE-25': b.att += 5; if (BAL.te25 === 'ar') b.ar -= BAL.te25ar; break;
      case 'TE-27': b.mov += isC(p, 'Druido') ? BAL.te27 : 1; break;
    }
  }
  if (p.flags.fabbro) b.att += p.flags.fabbro * weapons(p).length;
  if (p.flags.clanG && weapons(p).some(id => SLOT[baseId(id)] === '2h')) b.att++;
  return b;
}
function mapBonus(p, mapId = G.map && G.map.id) {
  const b = { att: 0, mov: 0, ar: 0, pv: 0, adv: 0, dis: 0 };
  switch (mapId) {
    case 'TM-01': if (isR(p, 'Nano')) b.adv++; break;
    case 'TM-02': if (!(isC(p, 'Warlock') || isR(p, 'Tiefling'))) b.dis++; break;
    case 'TM-03': if (isR(p, 'Aasimar')) { b.adv++; b.mov++; } break;
    case 'TM-04': b.mov += isR(p, 'Umano', 'Halfling') ? 2 : -2; break;
    case 'TM-05': if (BAL.tm05 === 'mov1') { if (isR(p, 'Elfo') || isC(p, 'Druido')) b.mov++; } else if (isR(p, 'Elfo')) { b.att++; b.mov += 3; } else { b.att--; b.mov--; b.ar--; } break;
  }
  return b;
}
function stat(p, k) {
  let v = p.base[k] + (isC(p, 'Bardo') && (!BAL.bardoStats || BAL.bardoStats.includes(k)) ? 1 : 0) + eqBonus(p)[k] + mapBonus(p)[k];
  for (const m of p.mods) v += m[k] || 0;
  if (k === 'mov' && BAL.furyMov && fury(p)) v += BAL.furyMov;
  if (k === 'mov' && BAL.locMov && isLocated(p)) v += BAL.locMov;
  return v;
}
const maxPV = p => Math.max(1, stat(p, 'pv'));
function clamp(p) { const m = maxPV(p); if (p.pv > m) p.pv = m; }
function advOf(x, c) {
  if (x.isCreature) { const d = c && c.dis[key(x)] ? 1 : 0; return d ? -1 : 0; }
  const e = eqBonus(x), m = mapBonus(x);
  let a = e.adv + m.adv, d = e.dis + m.dis;
  for (const md of x.mods) { if (md.adv) a++; if (md.dis) d++; }
  if (c && c.dis[key(x)]) d++;
  if (c && BAL.ladroAdv && c.round === 1 && isC(x, 'Ladro')) a++;
  return a > 0 && d === 0 ? 1 : (d > 0 && a === 0 ? -1 : 0);
}
function isLocated(p) { return p.located || p.tempLocated > 0 || p.zarko > 0; }

function addMod(p, m) { p.mods.push(m); if (m.pv > 0) p.pv += m.pv; }
function heal(p, n) { const before = p.pv; p.pv = Math.min(maxPV(p), p.pv + n); if (p.pv > before) log(`${p.name} recupera ${p.pv - before} PV (${p.pv}/${maxPV(p)}).`, 'good'); }
function loseTurns(p, n) { if (n <= 0) return; if (BAL.skipCapFoe && p !== G.players[G.cur] && !p.ritual && p.skip + n > BAL.skipCapFoe) n = Math.max(0, BAL.skipCapFoe - p.skip); if (n <= 0) { log(`${p.name} non può perdere altri turni.`); return; } if (p.skip + n > BAL.skipCap && !p.ritual) n = Math.max(0, BAL.skipCap - p.skip); if (n <= 0) { log(`${p.name} ha già il massimo di turni persi.`); return; } p.skip += n; log(`${p.name} perde ${n} turn${n === 1 ? 'o' : 'i'}.`, 'bad'); }
function gainTurns(p, n) { const c = Math.min(p.skip, n); p.skip -= c; p.extra += n - c; log(`${p.name} guadagna ${n} turn${n === 1 ? 'o' : 'i'}${c ? ` (${c} annullano turni persi)` : ''}.`, 'good'); }
function giveInsp(p, why) { if (p.insp) { log(`${p.name} ha già l'Ispirazione (non si accumula).`); return; } p.insp = true; log(`${p.name} ottiene Ispirazione${why ? ' (' + why + ')' : ''}.`, 'good'); }

// ===================== Dadi =====================
// noD4: niente D4 nella scatola, al suo posto D6 − 1 (minimo 1); uni = D6 ritirando 5 e 6
const d4 = (uni = false) => !BAL.noD4 ? rnd(4) : uni ? rnd(4) : Math.max(1, rnd(6) - 1);
function rollRaw(s, adv = 0, uni = false) { if (s === 4) return d4(uni); const a = rnd(s); if (!adv) return a; const b = rnd(s); return adv > 0 ? Math.max(a, b) : Math.min(a, b); }
function rerollOpts(p) {
  const o = [];
  if (p.insp) o.push({ label: 'Ritira con Ispirazione', value: 'insp' });
  if (p.magoRerolls > 0) o.push({ label: `Ritira (Mago, ${p.magoRerolls} rimasti)`, value: 'mago' });
  if (p.destino > 0) o.push({ label: `Ritira (Destino obbligato, ${p.destino})`, value: 'destino' });
  return o;
}
// IA: non sprecare i ritiri sul movimento; il Guerriero tiene l'Ispirazione per il −2 AR
function aiReroll(p, label, opts) {
  if (label === 'Movimento' || label.startsWith('Punto di')) return 'keep';
  const o = opts.filter(x => !(x.value === 'insp' && isC(p, 'Guerriero')));
  return o.length ? o[0].value : 'keep';
}
function spendReroll(p, v) { if (v === 'insp') p.insp = false; else if (v === 'mago') p.magoRerolls--; else if (v === 'destino') p.destino--; }
async function roll(p, sides, label, { bad = null, adv = 0, uni = false } = {}) {
  tick('dado'); let v = rollRaw(sides, adv, uni);
  log(`${p ? p.name + ' · ' : ''}${label}: D${sides}${adv > 0 ? ' con vantaggio' : adv < 0 ? ' con svantaggio' : ''} → ${v}`, 'dice');
  showDie(sides, v);
  while (p && !p.isCreature && bad && bad(v)) {
    const opts = rerollOpts(p); if (!opts.length) break;
    const ch = await ask(p, `${label}: è uscito ${v}`, [{ label: 'Tieni il risultato', value: 'keep' }, ...opts], { ai: () => aiReroll(p, label, opts) });
    if (ch === 'keep') break;
    spendReroll(p, ch); tick('dado'); v = rollRaw(sides, adv, uni);
    log(`${p.name} ritira: ${label} → ${v}`, 'dice'); showDie(sides, v);
  }
  return v;
}

// ===================== Interazione =====================
function ask(p, title, options, { text = '', cards = false, ai = null } = {}) {
  if (G && G.fast) return Promise.resolve(ai ? ai() : (options.find(o => !o.disabled) || options[0]).value);
  if (p.ai) {
    return (async () => {
      const gen = GEN;
      G.thinking = `${p.name}: ${title}`; render();
      await sleep(S.speed);
      if (gen !== GEN) return new Promise(() => {});
      G.thinking = '';
      const v = ai ? ai() : (options.find(o => !o.disabled) || options[0]).value;
      return v;
    })();
  }
  return new Promise(res => { pending = { p, title, text, options, cards, res }; render(); });
}
function pickHex(p, hexes, title) {
  if (G && G.fast) return Promise.resolve(aiMove(p, hexes));
  if (p.ai) {
    return (async () => { const gen = GEN; G.thinking = `${p.name} sceglie dove muoversi`; G.reach = hexes; render(); await sleep(S.speed); if (gen !== GEN) return new Promise(() => {}); G.thinking = ''; const h = aiMove(p, hexes); G.reach = null; return h; })();
  }
  return new Promise(res => { G.reach = hexes; pending = { p, title, options: [], hex: true, res: h => { G.reach = null; res(h); } }; render(); });
}
function resolvePending(v) { const pd = pending; if (!pd) return; pending = null; pd.res(v); render(); }

async function chooseFrom(p, ids, title, { optional = false, ai = null } = {}) {
  if (!ids.length) return null;
  const opts = ids.map(id => ({ label: C(id).nome + (id.includes('~') ? ' (copia)' : ''), value: id, hint: C(id).testo }));
  if (optional) opts.push({ label: 'Nessuna', value: null });
  return await ask(p, title, opts, { ai: ai || (() => aiPickBest(p, ids)) });
}
async function recover(p, n, { except = null, filter = null, from = null, title = null } = {}) {
  const pile = from || p.discard;
  let got = 0;
  for (let i = 0; i < n; i++) {
    const cand = [...new Set(pile.filter(id => id !== except && (!filter || filter(id))))];
    if (!cand.length) { if (!got) log(`${p.name}: nessuna carta da recuperare.`); break; }
    const id = await chooseFrom(p, cand, title || `Scegli una carta da riprendere (${i + 1}/${n})`);
    if (!id) break;
    pile.splice(pile.indexOf(id), 1); p.hand.push(id); got++;
    log(`${p.name} riprende «${C(id).nome}» in mano.`);
  }
  return got;
}
async function discardN(p, n, except) {
  for (let i = 0; i < n; i++) {
    const cand = p.hand.filter(id => id !== except);
    if (!cand.length) return;
    const id = await chooseFrom(p, cand, `Scegli una carta da scartare (${i + 1}/${n})`, { ai: () => aiPickWorst(p, cand) });
    p.hand.splice(p.hand.indexOf(id), 1); if (!id.includes('~')) p.discard.push(id);
    log(`${p.name} scarta «${C(id).nome}».`);
  }
}
function randomDiscard(p, n) {
  for (let i = 0; i < n && p.hand.length; i++) {
    const id = pick(p.hand); p.hand.splice(p.hand.indexOf(id), 1); if (!id.includes('~')) p.discard.push(id);
    log(`${p.name} scarta «${C(id).nome}».`, 'bad');
  }
}
function givePotions(p, n) {
  for (let i = 0; i < n; i++) { const id = pick(POTIONS) + '~' + (++G.copy); p.hand.push(id); log(`${p.name} ottiene ${C(id).nome}.`, 'good'); }
}
async function harm(p, n) { await hurt(p, n, G.combat); if (p.pv <= 0 && !G.combat) await defeat(p); }

// ===================== Tesoro, indizi, livelli =====================
async function rollSpawn(p, why) {
  for (let k = 0; k < 50; k++) {
    const v = await roll(p, SPAWNS.length, why === 'respawn' ? 'Punto di respawn' : 'Punto di partenza');
    const h = SPAWNS[v - 1];
    const o = others2(p).find(x => x.pos.c >= 0 && hexDist(h, x.pos) <= 1);
    if (o) { log(`Lo spawn ${v} è occupato o accanto a ${o.name}: si ritira.`); continue; }
    log(`${p.name} ${why === 'respawn' ? 'ricompare' : 'parte'} dallo spawn ${v}.`);
    return { ...h };
  }
  return { ...SPAWNS[0] };
}
function locate(p) {
  if (p.located) return;
  p.located = true; stageUp('late'); log(`${p.name} individua il tesoro! La casella viene rivelata.`, 'gold');
  if (BAL.locCatch && !G.catching) { G.catching = true; log('La voce si sparge: ogni altro eroe ottiene un indizio.', 'gold'); for (const x of others2(p)) if (!x.located) { x.clues++; if (x.clues >= 3) { x.located = true; log(`${x.name} individua il tesoro!`, 'gold'); } } G.catching = false; }
}
async function addClue(p, n = 1) {
  for (let i = 0; i < n && !p.located; i++) {
    p.clues++; p.dry = 0; stageUp('mid'); mark('clue' + p.clues); log(`${p.name} ottiene un indizio (${p.clues}/3).`, 'gold');
    if (p.clues >= 3) locate(p);
  }
}
function moveTreasure() {
  const cand = physBoard() ? PHYS.cripta.map(([c, r]) => ({ c, r })).filter(h => !same(h, G.treasure)) : allHexes().filter(h => tileAt(h).type !== 'start' && !same(h, G.treasure) && G.players.every(p => hexDist(h, p.pos) >= 2));
  G.treasure = pick(cand); G.moves = (G.moves || 0) + 1;
  log('Il tesoro cambia posizione! Chi l\'aveva individuato deve trovare un altro indizio.', 'gold');
  for (const p of G.players) {
    if (p.located && BAL.moveKeep) { tick('dado'); const v = rnd(6); if (v >= BAL.moveKeep) { log(`${p.name} tira ${v}: ritrova subito la pista!`, 'gold'); continue; } log(`${p.name} tira ${v}: pista persa.`); }
    if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0;
  }
}
async function addPE(p, n) {
  p.pe += n; log(`${p.name} guadagna ${n} PE.`);
  while (p.pe >= 2) { p.pe -= 2; await levelUp(p); }
}
async function levelUp(p) {
  if (p.level >= 5) { log(`${p.name} è già al livello massimo.`); return; }
  tick('livello'); mark('lvl' + (p.level + 1)); p.level++; p.base.pv++; p.pv++;
  log(`${p.name} sale al livello ${p.level}! +1 PV.`, 'good');
  const k = await ask(p, `Livello ${p.level}: scegli la statistica da aumentare`, ['att', 'mov', 'ar', 'pv'].map(s => ({ label: `+1 ${STATN[s]} (ora ${s === 'pv' ? maxPV(p) : stat(p, s)})`, value: s })), { ai: () => (p.level % 2 ? 'att' : 'ar') });
  p.base[k]++; if (k === 'pv') p.pv++;
  log(`${p.name} aumenta ${STATN[k]}.`);
}

// ===================== Equipaggiamento =====================
function unequip(p, id, toDiscardOf = p) {
  const mBefore = maxPV(p);
  for (const k in p.equip) if (p.equip[k] === id) p.equip[k] = null;
  p.servants = p.servants.filter(s => s.src !== id);
  if (!id.includes('~')) toDiscardOf.discard.push(id);
  clamp(p);
  return mBefore;
}
async function equip(p, id) {
  const s = SLOT[baseId(id)];
  let slots;
  if (BAL.slots3) slots = [slots3Of(s)];
  else if (s === '2h') slots = ['dx', 'sx'];
  else if (s === '1h') {
    if (!p.equip.dx) slots = ['dx'];
    else if (!p.equip.sx) slots = ['sx'];
    else {
      const ch = await ask(p, `Dove impugni ${C(id).nome}?`, [
        { label: `Mano destra (al posto di ${C(p.equip.dx).nome})`, value: 'dx' },
        { label: `Mano sinistra (al posto di ${C(p.equip.sx).nome})`, value: 'sx' }], { ai: () => 'sx' });
      slots = [ch];
    }
  } else if (s === 'scudo') slots = p.equip.dx && SLOT[baseId(p.equip.dx)] === '1h' && !p.equip.sx ? ['sx'] : ['dx'];
  else slots = [s];
  const before = maxPV(p);
  for (const k of slots) if (p.equip[k]) { log(`${C(p.equip[k]).nome} torna nella pila degli scarti.`); unequip(p, p.equip[k]); }
  for (const k of slots) p.equip[k] = id;
  const after = maxPV(p); if (after > before) p.pv += after - before;
  if (baseId(id) === 'TE-22') p.servants.push({ name: 'Cervo (Principe della foresta)', pv: 1, maxpv: 1, att: 1, ar: 0, src: id });
  if (baseId(id) === 'TE-27') p.servants.push({ name: 'Rospo (Zampa della palude)', pv: 1, maxpv: 1, att: 1, ar: 0, src: id });
  log(`${p.name} equipaggia ${C(id).nome}.`);
}
// 3 slot della scatola (Elmo, Arma, Corpo): scudi e accessori vanno nel Corpo
function slots3Of(s) { return s === 'elmo' ? 'elmo' : (s === '1h' || s === '2h' || (s === 'scudo' && BAL.scudoArma)) ? 'dx' : 'armatura'; }
function loseSlot(p, s) {
  const id = p.equip[s]; if (!id) return;
  unequip(p, id); p.lost.push(id);
  log(`${p.name} perde ${C(id).nome}.`, 'bad');
}
async function lossRoll(p) {
  if (!equipped(p).length) { log(`${p.name} non ha equipaggiamento da perdere.`); return; }
  const v = await roll(p, 6, 'Perdita di equipaggiamento', { bad: v => v < 6 });
  const map = BAL.slots3 ? { 2: 'elmo', 3: 'dx', 4: 'armatura' } : { 2: 'elmo', 3: 'dx', 4: 'armatura', 5: 'sx' };
  if (v === 1) { log('Perde tutto l\'equipaggiamento!', 'bad'); for (const s of Object.keys(p.equip)) loseSlot(p, s); }
  else if (v === 6 || !map[v]) log('Nessuna perdita.', 'good');
  else if (p.equip[map[v]]) loseSlot(p, map[v]);
  else log(`Lo slot ${SLOTN[map[v]]} era già vuoto: nessuna perdita.`);
}
async function defeat(p, why = '', near = false) {
  log(`${p.name} è sconfitto${why ? ' (' + why + ')' : ''} e deve ricomparire in un punto di spawn.`, 'bad');
  tick('sconfitta'); p.defeated = true;
  if (near) { const h = SPAWNS.slice().sort((a, b) => hexDist(a, G.treasure) - hexDist(b, G.treasure)).find(h => others2(p).every(x => hexDist(h, x.pos) > 1)); if (h) { p.pos = { ...h }; log(`${p.name} ricompare alla partenza più vicina al tesoro.`); } else p.pos = await rollSpawn(p, 'respawn'); }
  else p.pos = await rollSpawn(p, 'respawn');
  if (p.ritual) { p.ritual = false; p.skip = 0; log(`Il rituale di Zarko di ${p.name} è interrotto!`, 'gold'); }
  if (isC(p, 'Barbaro')) log('Barbaro: non perde l\'equipaggiamento.');
  else await lossRoll(p);
  p.pv = maxPV(p);
}

// ===================== Classi e mappe =====================
async function setClass(p, cls, id, { add = false } = {}) {
  if (!add && p.classes.length) {
    for (const cc of p.classCards) p.discard.push(cc);
    p.servants = p.servants.filter(s => !s.cls);
    log(`${p.name} lascia la classe ${p.classes.join(' / ')}.`);
    p.classes = []; p.classCards = [];
  }
  p.classes.push(cls); if (id) p.classCards.push(id);
  log(`${p.name} ora è ${cls}.`, 'good');
  if (cls === 'Druido') p.servants.push({ name: 'Fuoco fatuo', pv: BAL.fatuo[0], maxpv: BAL.fatuo[0], att: BAL.fatuo[1], ar: 0, cls: true });
  if (cls === 'Warlock') p.servants.push({ name: 'Imp', pv: BAL.imp[0], maxpv: BAL.imp[0], att: BAL.imp[1], ar: 0, cls: true });
  if (cls === 'Mago') p.magoRerolls = BAL.magoPerTurn ? 1 : BAL.magoRerolls;
  if (cls === 'Paladino') p.palHeals = BAL.palPerTurn ? 1 : BAL.palHeals;
  if (cls === 'Bardo') p.pv += 1;
}
async function setMap(p, id) {
  if (G.map) { G.players[G.map.owner].discard.push(G.map.id); log(`La mappa «${C(G.map.id).nome}» lascia il posto alla nuova.`); }
  G.map = { id, owner: p.id };
  log(`Il terreno diventa «${C(id).nome}».`, 'gold');
  if (movesLeft()) moveTreasure(); else log(`Il tesoro si è già spostato ${BAL.maxMoves} volte: resta dov'è.`);
  if (id === 'TM-01') { log('L\'aria è avvelenata: tutti −1 PV.', 'bad'); for (const x of G.players) await harm(x, 1); }
}

// ===================== Scontri =====================
const key = x => x.isCreature ? 'F' : 'P' + x.id;
const cmod = (c, x, k) => (c && c.mods[key(x)] && c.mods[key(x)][k]) || 0;
function addCmod(c, x, k, v) { const kk = key(x); c.mods[kk] = c.mods[kk] || {}; c.mods[kk][k] = (c.mods[kk][k] || 0) + v; }
const fury = x => !x.isCreature && BAL.furyAtt + BAL.furyDmg > 0 && isC(x, 'Barbaro') && x.pv <= maxPV(x) / 2;
const atkOf = (x, c) => (x.isCreature ? x.att : stat(x, 'att') + (fury(x) ? BAL.furyAtt : 0)) + cmod(c, x, 'att');
const arOf = (x, c) => (x.isCreature ? x.ar : stat(x, 'ar')) + cmod(c, x, 'ar');
function dmgDice(x) {
  if (x.isCreature) return x.dmg;
  const w = weapons(x);
  const f = fury(x) ? BAL.furyDmg : 0;
  if (w.some(id => SLOT[baseId(id)] === '2h')) return [6, 1 + f];
  return w.length ? [6, f] : [4, f];
}
const dmgLabel = x => { const [s, b] = dmgDice(x); return `${s === 4 && BAL.noD4 ? 'D6−1' : 'D' + s}${b ? '+' + b : ''}`; };
const dead = x => x.pv <= 0;
function foeOf(p) { const c = G.combat; if (!c) return null; return c.p === p ? c.foe : (c.foe === p ? c.p : null); }
function makeCreature(def, lvl = 1) { const extra = BAL.creatureFixed ? 0 : Math.max(0, lvl - 1); return { ...def, isCreature: true, pv: def.pv + extra, maxpv: def.pv + extra }; }

async function hurt(t, n, c = null) {
  if (n <= 0) return 0;
  if (t.isCreature) { t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${t.maxpv}).`); return n; }
  const tf = t.turnFlags;
  if (tf.immune) { log(`${t.name} è immune ai danni (Scudo magico).`, 'good'); return 0; }
  if (tf.absorb) { log(`${t.name} assorbe il colpo con lo Scudo magico.`, 'good'); heal(t, n); return 0; }
  if (tf.half) n = Math.ceil(n / 2);
  if (has(t, 'TE-25') && BAL.te25 === 'doppio') n *= 2;
  if (c && has(t, 'TE-23') && (BAL.te23g === false || isC(t, 'Guerriero')) && !c.spinato[t.id]) { c.spinato[t.id] = true; n = Math.ceil(n / 2); log('Lo Scudo spinato dimezza il primo colpo.'); }
  if (c && t.flags.patto && t.servants.length) {
    const s = t.servants[0]; s.pv -= n; log(`${s.name} subisce ${n} danni al posto di ${t.name}.`);
    if (s.pv <= 0) { t.servants.shift(); log(`${s.name} è distrutto.`, 'bad'); }
    return n;
  }
  if (t.pv - n <= 0 && t.ashafe > 0) { t.ashafe = 0; log('Ashafe si sacrifica e assorbe il colpo letale!', 'good'); return 0; }
  t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${maxPV(t)}).`, 'bad');
  if (c && c.foe && c.foe.borseggio && t === c.p && !c.stole && t.hand.length) { c.stole = true; log(`${c.foe.name} ti ruba una carta: ne scarti una a caso.`, 'bad'); randomDiscard(t, 1); }
  if (t.pv <= 0 && c && isC(t, 'Chierico') && !c.chierico[t.id] && (BAL.chierico === 'scontro' || (BAL.chierico === 'boss' && c.kind === 'boss') || (BAL.chierico === 'locanda' && !t.flags.revived))) { c.chierico[t.id] = true; t.flags.revived = true; t.pv = BAL.chierRev || 1; log(`Chierico: torna in vita con ${t.pv} PV!`, 'good'); }
  return n;
}

async function attack(a, d, c) {
  if (c.petrified[key(a)]) { c.petrified[key(a)] = false; log(`${a.name} è pietrificato e salta l'attacco.`); return; }
  const adv = advOf(a, c), bonus = atkOf(a, c), need = 10 + arOf(d, c);
  const hit = v => v === 20 || (v !== 1 && v + bonus >= need);
  let v = await roll(a.isCreature ? null : a, 20, `${a.name} attacca ${d.name} (serve ${need}, ATT ${fmt(bonus)})`, { adv, bad: v => !hit(v) });
  if (hit(v) && !d.isCreature && d.destino > 0) {
    const ch = await ask(d, `${a.name} ti colpisce (${v}${fmt(bonus)}). Usi Destino obbligato per fargli ritirare il dado?`, [{ label: 'Sì, obbliga a ritirare', value: 'y' }, { label: 'No', value: 'n' }], { ai: () => 'y' });
    if (ch === 'y') { d.destino--; v = rollRaw(20, adv); log(`${a.name} è costretto a ritirare → ${v}`, 'dice'); }
  }
  tick('attacco');
  if (!hit(v)) { log(`${a.name} manca il colpo.`); return; }
  const [s, b] = dmgDice(a);
  let dmg = (s === 4 ? d4() : rnd(s)) + b;
  if (!a.isCreature && c.berserk[a.id]) dmg += 2;
  if (v === 20) { dmg *= 2; log('Colpo critico! Danni raddoppiati.', 'gold'); }
  if (!d.isCreature && c.reflect[d.id]) {
    const r = c.reflect[d.id]; c.reflect[d.id] = null;
    const x = await roll(d, 6, 'Danno riflesso', { adv: r.adv ? 1 : 0 });
    if (x >= 4) { log(`Il danno rimbalza su ${a.name}!`, 'good'); await hurt(a, dmg, c); return; }
  }
  const dealt = await hurt(d, dmg, c);
  if (dealt > 0 && !a.isCreature) {
    if (has(a, 'TE-11') && !c.daga[a.id]) { c.daga[a.id] = true; addCmod(c, d, 'ar', -2); log(`Corrosione: ${d.name} ha −2 AR per questo scontro.`); }
    if (has(a, 'TE-24')) { const h = Math.floor(dealt / 2); if (h > 0) heal(a, h); }
  }
  if (dealt > 0 && a.beholder) {
    if (rnd(6) <= 3) { c.petrified[key(d)] = true; log(`${d.name} è pietrificato: salterà il prossimo attacco.`, 'bad'); }
    else { addCmod(c, d, 'att', -2); log(`${d.name} è colto dalla paura: −2 ATT per questo scontro.`, 'bad'); }
  }
}
async function servantAttack(owner, s, foe, c) {
  tick('attacco'); const v = rnd(20), need = 10 + arOf(foe, c);
  if (v === 20 || (v !== 1 && v + s.att >= need)) {
    const base = s.dmg || (BAL.servDmg === 'd4' ? rnd(4) : (s.name === 'Imp' ? BAL.impDmg : BAL.servDmg));
    const dmg = base + (owner.flags.pattoW ? 1 : 0);
    log(`${s.name} colpisce (${v}${fmt(s.att)}).`); await hurt(foe, dmg, c);
  } else log(`${s.name} manca (${v}${fmt(s.att)}).`);
}

function canFlee(x, c) {
  if (c.berserk[x.id]) return false;
  if (c.kind === 'creatura' || c.kind === 'miniboss') return c.p === x;
  return isC(x, 'Ladro');
}
async function combatTurn(x, c, attacker) {
  while (true) {
    if (dead(c.p) || dead(c.foe)) return 'none';
    const o = [{ label: `Attacca (D20${fmt(atkOf(x, c))} contro AR ${10 + arOf(attacker ? c.foe : c.p, c)})`, value: 'attacca' }];
    if (canFlee(x, c)) o.push({ label: 'Fuggi', value: 'fuga' });
    if (isC(x, 'Paladino') && x.palHeals > 0 && x.pv < maxPV(x)) o.push({ label: `Paladino: cura 2 PV (${x.palHeals} rimaste)`, value: 'pal' });
    if (isC(x, 'Guerriero') && x.insp) o.push({ label: `Guerriero: usa Ispirazione (−${BAL.guerAR} AR al nemico)`, value: 'guer' });
    const a = await ask(x, attacker ? 'Il tuo round di attacco' : `${c.p.name} ti attacca: il tuo round`, o, { cards: true, ai: () => aiCombat(x, c, o) });
    if (a && a.card) { await playCard(x, a.card); continue; }
    if (a === 'pal') { x.palHeals--; heal(x, 2); continue; }
    if (a === 'guer') { x.insp = false; addCmod(c, x === c.p ? c.foe : c.p, 'ar', -BAL.guerAR); log(`${x.name} usa l'Ispirazione: −${BAL.guerAR} AR al nemico.`); continue; }
    return a;
  }
}

async function scontro(p, foe, kind) {
  const c = { p, foe, kind, round: 0, berserk: {}, carica: {}, mods: {}, reflect: {}, spinato: {}, chierico: {}, daga: {}, petrified: {}, dis: {}, used: {}, defCards: 0, noCards: false };
  G.combat = c; tick('scontro'); if (p.turnFlags) p.turnFlags.fought = true;
  log(`Scontro: ${p.name} contro ${foe.name}${kind === 'boss' ? ' (BOSS)' : kind === 'miniboss' ? ' (mini-boss)' : ''}.`, 'turn');
  if (G.stop > 0) { G.stop--; c.noCards = true; log('Stop: in questo scontro nessuno può giocare carte.'); }
  let res = null;
  if (p.diss > 0) { p.diss--; c.dis[key(p)] = true; }
  if (kind === 'pvp' && foe.diss > 0) { foe.diss--; c.dis[key(foe)] = true; }
  if (p.curse) {
    p.curse = false;
    const x = await roll(p, 6, 'Maledizione del caduto');
    if (x <= 3) { log(`${p.name} è costretto a fuggire!`, 'bad'); res = 'fuga'; }
    else { addCmod(c, p, 'att', 1); log('La maledizione non attecchisce: +1 ATT in questo scontro.'); }
  }
  if (!res && p.flags.assassinio && (kind === 'creatura' || kind === 'miniboss')) { p.flags.assassinio = false; foe.pv = 0; log('Assassinio nelle ombre: la creatura viene eliminata.', 'good'); res = 'win'; }
  if (p.flags.doppio) { p.flags.doppio = false; c.doppio = true; }
  // fuga del difensore dal PvP: cede una carta a caso a chi attacca
  if (!res && kind === 'pvp' && BAL.pvpFlee && foe.hand.length && !foe.ritual) {
    const ch = await ask(foe, `${p.name} ti attacca. Combatti o fuggi cedendogli una carta a caso dalla tua mano?`, [{ label: 'Combatti', value: 'f' }, { label: 'Fuggi (cedi 1 carta a caso)', value: 'r' }], { ai: () => (power(p, c) > power(foe, c) * BAL.pvpFlee ? 'r' : 'f') });
    if (ch === 'r') {
      const k = Math.floor(Math.random() * foe.hand.length); const id = foe.hand.splice(k, 1)[0]; p.hand.push(id);
      log(`${foe.name} fugge e cede «${C(id).nome}» a ${p.name}.`, 'bad'); retreatFrom(foe, p.pos);
      G.combat = null; return;
    }
  }
  render();
  if (!res && foe.agguato) { log(`${foe.name}: agguato! Attacca per primo.`, 'bad'); await attack(foe, p, c); if (dead(p)) res = 'lose'; }
  while (!res) {
    c.round++;
    const act = await combatTurn(p, c, true);
    if (G.over) return;
    if (act === 'fuga') { res = 'fuga'; break; }
    if (dead(foe)) { res = 'win'; break; } if (dead(p)) { res = 'lose'; break; }
    if (act === 'attacca') {
      await attack(p, foe, c);
      if (c.carica[p.id] && !dead(foe)) { log('Carica eroica: secondo attacco!'); await attack(p, foe, c); }
      if (c.doppio && c.round === 1 && !dead(foe)) { log('Arco da guerra: secondo attacco!'); await attack(p, foe, c); }
      if (BAL.servPvP || kind !== 'pvp') for (const s of [...p.servants]) { if (dead(foe)) break; await servantAttack(p, s, foe, c); }
    }
    if (dead(foe)) { res = 'win'; break; } if (dead(p)) { res = 'lose'; break; }
    if (kind === 'pvp') {
      const a2 = await combatTurn(foe, c, false);
      if (a2 === 'fuga') { res = 'fugaDif'; break; }
      if (dead(foe)) { res = 'win'; break; } if (dead(p)) { res = 'lose'; break; }
      if (a2 === 'attacca') { await attack(foe, p, c); if (c.carica[foe.id] && !dead(p)) { log('Carica eroica: secondo attacco!'); await attack(foe, p, c); } if (BAL.servPvP) for (const s of [...foe.servants]) { if (dead(p)) break; await servantAttack(foe, s, p, c); } }
    } else await attack(foe, p, c);
    if (dead(p)) { res = 'lose'; break; } if (dead(foe)) { res = 'win'; break; }
    render();
  }
  G.combat = null;
  for (const x of kind === 'pvp' ? [p, foe] : [p]) if (c.berserk[x.id] && x.pv > 0) { const l = Math.min(2, x.pv - 1); if (l > 0) { x.pv -= l; log(`La furia si spegne: ${x.name} perde ${l} PV.`, 'bad'); } }
  for (const x of kind === 'pvp' ? [p, foe] : [p]) {
    x.mods = x.mods.filter(m => { if (m.kind === 'scontri') { m.n--; return m.n > 0; } return true; });
    clamp(x);
  }
  // sfida dei potenti
  const ch = p.challenge && (kind === 'miniboss') ? p.challenge : null;
  if (ch) p.challenge = null;
  if (res === 'win') {
    if (kind === 'boss') { G.over = { winner: p, why: `${p.name} sconfigge ${foe.name} e ritrova MIMI, la cassa di Geronimo!`, reason: foe.beholder ? 'beholder' : 'boss' }; return; }
    if (kind === 'pvp') { await pvpReward(p, foe); return; }
    log(`${p.name} sconfigge ${foe.name}!`, 'good');
    if (BAL.barbHeal && isC(p, 'Barbaro')) heal(p, BAL.barbHeal);
    if (!foe.cob) tileAt(p.pos).done = true;
    if (foe.cob) { log('I Coboldi non hanno pagine della mappa: peschi una carta.'); drawCard(p); if (foe.borseggio) drawCard(p); } else await addClue(p);
    if (kind === 'miniboss') { await levelUp(p); giveInsp(p, 'mini-boss'); } else await addPE(p, 1);
    if (BAL.guerInsp && isC(p, 'Guerriero')) giveInsp(p, 'Guerriero vittorioso');
    if (ch) {
      if (!c.used[p.id]) { log('Sfida vinta senza usare carte!', 'good'); gainTurns(p, ch.bet); await recover(p, 1, { except: 'TI-49' }); }
      else log('Sfida vinta, ma sono state usate carte: nessun premio extra.');
    }
  } else if (res === 'lose') {
    if (kind === 'pvp') { await pvpReward(foe, p); return; }
    if (ch) { log('Sfida persa: si perdono i turni scommessi.', 'bad'); loseTurns(p, ch.bet); }
    await defeat(p, `da ${foe.name}`, kind === 'boss' && BAL.bossNear);
    if (BAL.defeatPE && kind !== 'boss') { log(`${p.name} impara dalla sconfitta.`); await addPE(p, BAL.defeatPE); }
  } else if (res === 'fuga') {
    log(`${p.name} fugge: nessuna ricompensa.`);
    if (isC(p, 'Ladro')) log('Ladro: fugge senza arretrare.'); else retreat(p, p.turnStart);
  } else if (res === 'fugaDif') {
    log(`${foe.name} fugge dal combattimento.`); retreatFrom(foe, p.pos);
  }
}
async function pvpReward(w, l) {
  log(`${w.name} vince il combattimento PvP contro ${l.name}!`, 'good');
  if (l.discard.length) { await recover(w, 1, { from: l.discard, title: `Prendi una carta dalla pila degli scarti di ${l.name}` }); }
  if (l.clues > 0) { l.clues--; log(`${w.name} sottrae un indizio a ${l.name}.`, 'gold'); await addClue(w); }
  if (BAL.pvpLevel) await levelUp(w); else await addPE(w, 1);
  giveInsp(w, 'vittoria PvP');
  await defeat(l, `da ${w.name}`);
}
function retreat(p, toward) {
  const cand = neighbors(p.pos).filter(h => others2(p).every(o => !same(h, o.pos))).sort((a, b) => hexDist(a, toward) - hexDist(b, toward));
  const safe = cand.find(h => { const t = tileAt(h); return t.done || t.type === 'vuota' || t.type === 'start'; }) || cand[0];
  if (safe) { p.pos = { ...safe }; log(`${p.name} arretra di una casella.`); }
}
function retreatFrom(p, from) {
  const cand = neighbors(p.pos).sort((a, b) => hexDist(b, from) - hexDist(a, from));
  if (cand[0]) { p.pos = { ...cand[0] }; log(`${p.name} arretra di una casella.`); }
}

// ===================== Carte: definizioni =====================
const others = (p, id) => p.hand.filter(x => x !== id);
const DEF = {};
function tc(cls, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { if (extra.pre) await extra.pre(p, o, id); await setClass(p, cls, id); return 'keep'; }, ai: p => p.classes.length ? 0 : 6 };
}
DEF['TC-01'] = tc('Barbaro', { nota: 'Non perde equipaggiamento quando è sconfitto (le Trappole sì). Furia: con metà dei PV o meno +3 ATT, +1 ai danni e +2 MOV.' });
DEF['TC-02'] = tc('Bardo', { nota: '+1 a PV, ATT, AR e MOV finché sei Bardo.' });
DEF['TC-03'] = tc('Chierico', { nota: 'Se scendi a 0 PV in uno scontro torni a 3 PV e continui a combattere. Si usa una volta e si ricarica fermandosi in una locanda.' });
DEF['TC-04'] = tc('Druido', { nota: 'Evoca il Fuoco fatuo (PV 2, ATT 2): attacca dopo di te e infligge 1 danno a colpo.' });
DEF['TC-05'] = tc('Guerriero', { nota: '+2 PV. Ogni scontro vinto dà Ispirazione. In scontro puoi spenderla per dare −2 AR al nemico.' });
DEF['TC-06'] = tc('Ladro', { need: (p, o, id) => !BAL.ladroDiscard || others(p, id).length >= 1 || 'Serve un\'altra carta in mano da scartare', pre: async (p, o, id) => { if (BAL.ladroDiscard) await discardN(p, 1, id); }, nota: '+3 MOV. Puoi fuggire anche da PvP e boss, e fuggendo non arretri. Vantaggio nel primo round di ogni scontro.' });
DEF['TC-07'] = tc('Mago', { nota: 'Puoi ritirare un tuo dado una volta per turno.' });
DEF['TC-08'] = tc('Paladino', { nota: 'Cura 2 PV, 5 volte per partita (pulsante nel turno o in scontro).' });
DEF['TC-09'] = tc('Stregone', { nota: '+2 MOV. Le carte Incantesimo che infliggono danni o curano danno 1 punto in più.' });
DEF['TC-10'] = tc('Warlock', { nota: 'Evoca l\'Imp (PV 3, ATT 2): attacca dopo di te e infligge 3 danni a colpo.' });

function aiMapScore(p, o, id) {
  if (p.located && !o.located) return -5;
  const sum = (x) => { const b = mapBonus(x, id); return b.att + b.mov * 0.3 + b.ar + b.adv * 2 - b.dis * 2; };
  return (o.located && movesLeft() ? 6 : 0) + sum(p) - sum(o) + (G.map ? 0 : 0.5);
}
for (const id of ['TM-01', 'TM-02', 'TM-03', 'TM-04', 'TM-05']) DEF[id] = { when: 'fuori', fx: async (p, o, cid) => { await setMap(p, cid); return 'keep'; }, ai: (p, o) => aiMapScore(p, o, id), nota: 'Resta attiva finché un\'altra mappa non la sostituisce. Il tesoro cambia posizione. I bonus valgono per i giocatori, non per le creature.' };
DEF['TM-01'].nota = 'All\'ingresso tutti perdono 1 PV (una volta). Nani: vantaggio negli scontri. Il tesoro cambia posizione.';
DEF['TM-02'].nota = 'Chi non è Warlock o Tiefling ha svantaggio negli scontri. Il tesoro cambia posizione.';

function eqValue(p, id) {
  const fake = { ...p, equip: { elmo: null, dx: id, sx: null, armatura: null, accessorio: null }, flags: {} };
  const b = eqBonus(fake); return b.att * 1.2 + b.ar + b.mov * 0.3 + b.pv * 0.5 + b.adv * 2 - b.dis * 3;
}
function aiEquipScore(p, id) {
  const s = SLOT[baseId(id)];
  const slots = BAL.slots3 ? [slots3Of(s)] : s === '2h' ? ['dx', 'sx'] : s === '1h' ? (p.equip.dx ? ['sx'] : ['dx']) : s === 'scudo' ? ['dx'] : [s];
  const cur = [...new Set(slots.map(k => p.equip[k]).filter(Boolean))];
  const old = cur.reduce((a, x) => a + eqValue(p, x), 0);
  return eqValue(p, id) - old + (cur.length ? 0 : 2);
}
function te(on, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { await equip(p, id); if (on) await on(p, o, id); return 'keep'; }, ai: (p, o, id) => aiEquipScore(p, id) };
}
DEF['TE-01'] = te(null, { nota: 'Occupa lo slot Accessorio.' });
DEF['TE-02'] = te(async p => { if (isC(p, 'Guerriero')) { p.flags.doppio = true; log('Guerriero: nel prossimo scontro attacchi due volte nel primo round.'); } }, { nota: 'Elfo: vantaggio finché equipaggiato. Guerriero: un attacco in più nel primo round del prossimo scontro.' });
DEF['TE-03'] = te(null);
DEF['TE-04'] = te(null, { nota: 'Bonus di classe validi finché equipaggiata.' });
DEF['TE-05'] = te(async p => { if (isC(p, 'Guerriero')) giveInsp(p, 'Ascia Bipenne'); });
DEF['TE-06'] = te(async (p, o, id) => {
  if (!isC(p, 'Mago', 'Stregone')) return;
  const cand = p.discard.filter(x => x !== id);
  const pk = await chooseFrom(p, cand, 'Bacchetta di Lupres: scegli una carta dagli scarti da giocare subito', { optional: true });
  if (pk) { p.discard.splice(p.discard.indexOf(pk), 1); p.hand.push(pk); if (!(await playCard(p, pk, { free: true, immediate: true }))) log('La carta non si può giocare ora: resta in mano.'); }
}, { nota: 'Mago o Stregone: riprendi una carta dagli scarti e giocala subito (gratis).' });
DEF['TE-07'] = te(async p => { if (isC(p, 'Mago', 'Stregone')) giveInsp(p, 'Bacchetta'); });
DEF['TE-08'] = {
  when: 'fuori', nota: 'Si gioca sull\'avversario: le sue armi vanno nei suoi scarti e lui impugna il Calice (+2 ATT, svantaggio finché lo tiene).',
  fx: async (p, o, id) => {
    for (const w of weapons(o)) { log(`${C(w).nome} di ${o.name} viene distrutta.`, 'bad'); unequip(o, w); }
    const slot = o.equip.dx ? 'sx' : 'dx';
    if (o.equip[slot]) unequip(o, o.equip[slot]);
    o.equip[slot] = id; log(`${o.name} è costretto a impugnare il Calice sangue infetto.`, 'bad');
    return 'keep';
  }, ai: (p, o) => weapons(o).length ? 4 : 1,
};
DEF['TE-09'] = te(null);
DEF['TE-10'] = te(async p => { if (isC(p, 'Stregone', 'Mago', 'Chierico')) addMod(p, { label: 'Cappa mistica: vantaggio', adv: true, kind: 'scontri', n: BAL.te10 }); }, { nota: 'Stregone, Mago o Chierico: vantaggio nei prossimi 2 scontri.' });
DEF['TE-11'] = te(async p => { if (isC(p, 'Ladro')) giveInsp(p, 'Daga strana'); }, { nota: 'Corrosione: il primo colpo a segno in ogni scontro dà −2 AR al nemico per quello scontro.' });
DEF['TE-12'] = te(null, { nota: 'Guerriero: la «terza arma» non ha uno slot sulla scheda, quindi diventa +1 ATT.' });
DEF['TE-13'] = te(async p => { if (isR(p, 'Umano', 'Nano')) giveInsp(p, 'Elmo del generale'); });
DEF['TE-14'] = te(async (p, o) => { if (isC(p, 'Bardo')) for (const x of foes(p, o)) loseTurns(x, 1); });
DEF['TE-15'] = te(async p => { if (isC(p, 'Warlock')) { log('Necro armatura: il Warlock perde 2 PV.'); await harm(p, 2); } }, { nota: 'Warlock: perde 2 PV una volta, quando la equipaggia.' });
DEF['TE-16'] = { when: 'scontro', fx: async p => { const f = foeOf(p); addCmod(G.combat, f, 'ar', -2); log(`${f.name} ha −2 AR per questo scontro.`); }, ai: () => 3, nota: 'Solo in scontro: −2 AR al nemico fino alla fine dello scontro.' };
DEF['TE-17'] = { when: 'sempre', need: (p, o, id) => p.discard.some(x => x !== id) || 'La pila degli scarti è vuota', fx: async (p, o, id) => { await recover(p, 1, { except: id }); }, ai: p => p.discard.length ? 2 : 0 };
DEF['TE-18'] = { when: 'fuori', fx: async (p, o) => { if (BAL.te18 === 'cless') { const c = Math.min(2, p.skip); p.skip -= c; log(`${p.name} toglie ${c} Clessidr${c === 1 ? 'a' : 'e'}.`, 'good'); return; } const ch = await ask(p, 'Pozione del tempo', [{ label: 'Recuperi 2 turni', value: 'g' }, { label: BAL.allOpp && others2(p).length > 1 ? 'Ogni avversario perde 1 turno' : `${o.name} perde 1 turno`, value: 'l' }], { ai: () => p.skip ? 'g' : 'l' }); if (ch === 'g') gainTurns(p, 2); else for (const x of foes(p, o)) loseTurns(x, 1); }, ai: p => BAL.te18 === 'cless' ? (p.skip > 0 ? 4 : 0) : 3, nota: 'Togli fino a 2 tue Clessidre (turni da perdere).' };
DEF['TE-19'] = { when: 'fuori', fx: async p => addMod(p, { label: 'Pozione del vigore', mov: 3, kind: 'turn' }), ai: () => (G.phase === 'prima' ? 1 : -1) };
DEF['TE-20'] = { when: 'sempre', fx: async p => addMod(p, { label: 'Pozione della forza', att: 3, kind: 'turn' }), ai: () => (G.combat ? 3 : -1) };
DEF['TE-21'] = { when: 'sempre', need: p => p.pv < maxPV(p) || 'Hai già tutti i PV', fx: async p => heal(p, BAL.te21 || 2), ai: p => maxPV(p) - p.pv >= 2 ? 3 : 0 };
DEF['TE-22'] = te(null, { nota: 'Occupa lo slot Accessorio. Il cervo (1/1/0/0) combatte al tuo fianco (PV 1, ATT 1, 1 danno).' });
DEF['TE-23'] = te(null, { nota: 'Si impugna: occupa lo slot Arma. Guerriero: il primo colpo subito in ogni scontro è dimezzato.' });
DEF['TE-24'] = te(null, { need: p => isR(p, 'Aasimar') || isC(p, 'Paladino') || 'Serve una pedina Aasimar (Yumaniani) o classe Paladino', nota: 'Ogni colpo a segno ti cura della metà dei danni inflitti (per difetto).' });
DEF['TE-25'] = te(async p => { if (isR(p, 'Tiefling')) { const d = d4(); log(`La luce brucia il Tiefling: ${d} danni.`); await harm(p, d); } }, { nota: '+5 ATT e −1 AR finché la impugni. Tiefling: subisce D6 − 1 danni (minimo 1) quando la equipaggia.' });
DEF['TE-26'] = te(async p => givePotions(p, 2), { nota: 'Ricevi 2 pozioni casuali (copie extra che spariscono dopo l\'uso).' });
DEF['TE-27'] = te(null, { nota: 'Occupa lo slot Accessorio. Il blocco 1/1/0/0 è un Rospo che combatte al tuo fianco (PV 1, ATT 1).' });

const T = (o) => DEF[o.id] = o;
T({ id: 'TI-01', when: 'sempre', need: p => p.servants.length > 0 || 'Non hai servitori', fx: async p => { for (const s of p.servants) { s.pv++; s.maxpv++; s.att++; s.ar++; if (BAL.ti01dmg) s.dmg = (s.dmg || (s.name === 'Imp' ? BAL.impDmg : BAL.servDmg)) + BAL.ti01dmg; } log('I servitori ottengono +1 a tutte le statistiche.'); }, ai: () => 3, nota: 'Vale per tutti i tuoi servitori, in modo permanente.' });
T({ id: 'TI-02', when: 'sempre', fx: async (p, o, id) => { heal(p, 2 + sb(p)); if (isC(p, 'Paladino', 'Chierico', 'Druido')) await recover(p, 1, { except: id }); }, ai: p => maxPV(p) - p.pv >= 2 ? 3 : 0 });
T({ id: 'TI-03', when: 'fuori', need: p => isR(p, 'Aasimar') || 'Serve una pedina Aasimar (Yumaniani)', fx: async p => { addMod(p, { label: 'Angelo della morte (+8)', att: 8, mov: 8, ar: 8, pv: 8, kind: 'turni', n: 1, onExpire: 'angelo' }); }, ai: (p) => isLocated(p) ? 4 : 0, nota: '+8 a tutto per questo turno. A fine turno muori e rinasci alla partenza come Angelo della morte: ATT, MOV e AR base diventano almeno 2. Tieni indizi ed equipaggiamento.' });
T({ id: 'TI-04', when: 'fuori', need: (p, o) => (BAL.arconte === 'clues2' ? (isLocated(o) || o.clues >= 2) : isLocated(o)) || 'L\'avversario non ha individuato il tesoro', fx: async (p, o) => { const ok = x => BAL.arconte === 'clues2' ? (isLocated(x) || x.clues >= 2) : isLocated(x); const ts = BAL.arconteAll ? others2(p).filter(ok) : [o]; for (const x of ts) { await harm(x, BAL.arconteDmg + sb(p)); if (BAL.arconteClue && x.clues > 0 && !x.located && (BAL.arconteClue !== 'lead' || x.clues > p.clues)) { x.clues--; log(`${x.name} perde un indizio.`, 'bad'); } } }, ai: () => 5 });
T({ id: 'TI-05', when: 'fuori', need: (p, o, id) => (isC(p, 'Chierico', 'Paladino') || 'Serve classe Chierico o Paladino') && (others(p, id).length >= BAL.ashafe[1] || `Servono ${BAL.ashafe[1]} altre carte da scartare`), fx: async (p, o, id) => { await discardN(p, BAL.ashafe[1], id); loseTurns(p, BAL.ashafe[0]); p.ashafe = 4; log('Ashafe è al tuo fianco per 4 turni.', 'good'); }, ai: p => p.pv <= 3 ? 2 : 0, nota: 'Dura 4 dei tuoi turni (anche quelli persi): cura 1 PV a ogni tuo turno e assorbe un colpo letale.' });
T({ id: 'TI-06', when: 'sempre', fx: async p => addMod(p, { label: 'Assalto preparato', adv: true, att: isC(p, 'Ladro', 'Guerriero') ? 1 : 0, kind: 'scontri', n: 1 }), ai: () => G.combat ? 3 : 1, nota: 'Vale per il prossimo scontro (o quello in corso).' });
T({ id: 'TI-07', when: 'sempre', fx: async p => { addMod(p, { label: 'Assalto violento', att: 5, ar: -1, adv: isR(p, 'Orco'), kind: 'scontri', n: 1 }); await harm(p, 1); }, ai: p => (G.combat && p.pv > 2) ? 4 : 0, nota: '+5 ATT e −1 AR per il prossimo scontro (o quello in corso); perdi 1 PV subito.' });
T({ id: 'TI-08', when: 'sempre', need: p => isC(p, 'Ladro') || 'Serve classe Ladro', fx: async (p, o) => { const c = G.combat; if (c && c.foe.isCreature && c.kind !== 'boss') { c.foe.pv = 0; log('La creatura viene eliminata nell\'ombra.', 'good'); } else { p.flags.assassinio = true; log('Il prossimo scontro con una creatura o un mini-boss è vinto subito.'); } giveInsp(o, 'Assassinio nelle ombre'); }, ai: () => 3, nota: 'Non funziona su boss e PvP.' });
T({ id: 'TI-09', when: 'fuori', need: (p, o) => (isLocated(o) || 'L\'avversario non ha individuato il tesoro') && (!G.beholder || 'Il Beholder è già in campo'), fx: async () => { G.beholder = true; G.bossWounds = 0; log(`Un Beholder ora difende il forziere (PV ${BAL.behPV || BEHOLDER.pv}, ATT 3, AR 2). Ogni suo colpo pietrifica o spaventa.`, 'bad'); }, ai: () => 5, nota: 'Sostituisce il boss del tesoro. Ordine statistiche letto come PV/ATT/MOV/AR. Pietrificazione: salti il prossimo attacco. Paura: −2 ATT per lo scontro.' });
T({ id: 'TI-10', when: 'fuori', need: p => isC(p, 'Bardo') || 'Serve classe Bardo', fx: async (p, o) => { for (const x of foes(p, o)) { x.burattinato = 'pending'; log(`La prima carta che ${x.name} giocherà nel suo prossimo turno verrà scartata.`); } }, ai: () => 2, nota: 'Agisce sul prossimo turno dell\'avversario: la sua prima carta viene scartata e conta come giocata.' });
T({ id: 'TI-11', when: 'fuori', need: p => isR(p, 'Nano') || 'Serve una pedina Nano', fx: async (p, o) => { let any = false; if (isC(p, 'Chierico')) { heal(p, 1 + sb(p)); any = true; } if (isC(p, 'Guerriero')) { p.flags.clanG = true; log('Le armi a due mani ti danno +1 ATT per il resto della partita.'); any = true; } if (isC(p, 'Mago')) { addMod(o, { label: 'Clan riunito: −1 AR', ar: -1, kind: 'game' }); any = true; } if (!any) log('Nessuna classe corrispondente: la carta non ha effetto.'); }, ai: p => isC(p, 'Chierico', 'Guerriero', 'Mago') ? 3 : 0, nota: 'Guerriero: +1 ATT permanente se impugni un\'arma a due mani. Mago: −1 AR permanente all\'avversario.' });
T({ id: 'TI-12', when: 'fuori', fx: async (p, o) => { for (const x of foes(p, o)) { if (isR(x, 'Orco', 'Tiefling')) log(`${x.name} non subisce l'effetto.`); else loseTurns(x, BAL.ti12); } }, ai: (p, o) => isR(o, 'Orco', 'Tiefling') ? 0 : 6 });
T({ id: 'TI-13', when: 'scontro', fx: async p => { G.combat.reflect[p.id] = { adv: isC(p, 'Paladino', 'Chierico') }; log('Il prossimo colpo che subisci in questo scontro può rimbalzare (D6: 4-6).'); }, ai: () => 2, nota: 'Vale per il prossimo colpo subito nello scontro in corso. Rimbalza sull\'attaccante.' });
T({ id: 'TI-14', when: 'sempre', fx: async (p, o) => { const f = foeOf(p) || o; await hurt(f, BAL.dardo + sb(p), G.combat); if (isC(p, 'Mago', 'Stregone')) { if (G.combat) addCmod(G.combat, f, 'ar', -1); else addMod(f, { label: 'Dardo magico: −1 AR', ar: -1, kind: 'scontri', n: 1 }); log(`${f.name}: −1 AR.`); } if (!G.combat && !f.isCreature && f.pv <= 0) await defeat(f); }, ai: () => G.combat ? 3 : 1, nota: 'In scontro colpisce il nemico, fuori dallo scontro l\'avversario.' });
T({ id: 'TI-15', when: 'sempre', fx: async p => { p.destino += BAL.ti15; log('Potrai ritirare un tuo dado o far ritirare un colpo che ti colpisce.'); }, ai: () => 2 });
T({ id: 'TI-16', when: 'sempre', fx: async (p, o) => { let any = false; if (isR(p, 'Halfling', 'Umano')) { addMod(p, { label: 'Diamoci dentro: vantaggio', adv: true, kind: 'scontri', n: 2 }); any = true; } if (isC(p, 'Bardo')) { for (const x of foes(p, o)) { x.diss = (x.diss || 0) + 1; log(`${x.name} avrà svantaggio nel prossimo scontro.`); } any = true; } if (!any) log('Nessun effetto per la tua razza o classe.'); }, ai: p => (isR(p, 'Halfling', 'Umano') || isC(p, 'Bardo')) ? 3 : 0 });
T({ id: 'TI-17', when: 'sempre', need: p => p.pv < 2 || 'Puoi giocarla solo con meno di 2 PV', fx: async (p, o, id) => { await addClue(p); await recover(p, 1, { except: id }); if (isC(p, 'Paladino', 'Chierico')) heal(p, 5 + sb(p)); }, ai: () => 8 });
T({ id: 'TI-18', when: 'fuori', need: p => isR(p, 'Nano') || 'Serve una pedina Nano', fx: async p => { addMod(p, { label: 'Esercito nanico (+3)', att: 3, mov: 3, ar: 3, adv: true, kind: 'scontri', n: 3 }); p.noCardsFrom = p.ownTurns + 1; p.noCardsTo = p.ownTurns + 3; log('Non potrai giocare carte Trama per i prossimi 3 turni.'); }, ai: () => 4, nota: '+3 ATT, MOV, AR e vantaggio per 3 scontri; niente carte nei tuoi 3 turni successivi.' });
T({ id: 'TI-19', when: 'fuori', fx: async (p, o) => { addMod(p, { label: 'Esplorare il dungeon', mov: BAL.ti19mov, kind: 'turn' }); addMod(p, { label: 'Esplorare: +2 AR', ar: 2, kind: 'scontri', n: 1 }); }, ai: () => G.phase === 'prima' ? 2 : 0 });
T({ id: 'TI-20', when: 'fuori', need: (p) => isC(p, 'Chierico', 'Stregone', 'Mago') || 'Serve classe Chierico, Stregone o Mago', fx: async p => { await addClue(p, 2); loseTurns(p, BAL.ti20); }, ai: p => p.located ? 0 : 2, nota: 'Ottieni 2 indizi e perdi alcuni turni.' });
T({ id: 'TI-21', when: 'fuori', need: (p, o, id) => true, fx: async (p, o, id) => { const isTE = x => C(x).tipo === 'TE'; let from = p.discard; if (isR(p, 'Nano') && o.discard.some(isTE)) { const ch = await ask(p, 'Forgiatore esperto: da quale pila?', [{ label: 'I miei scarti', value: 'm' }, { label: `Scarti di ${o.name}`, value: 'o' }], { ai: () => 'o' }); if (ch === 'o') from = o.discard; } await recover(p, 1, { from, filter: isTE, title: 'Scegli un equipaggiamento da riprendere' }); if (isC(p, 'Guerriero', 'Barbaro')) addMod(p, { label: 'Forgiatore esperto', mov: BAL.forgiatore[0], att: BAL.forgiatore[1], kind: 'game' }); }, ai: (p, o) => (p.discard.some(x => C(x).tipo === 'TE') || isC(p, 'Guerriero', 'Barbaro')) ? 2 : 0, nota: 'Guerriero/Barbaro: +2 ATT permanenti.' });
T({ id: 'TI-22', when: 'sempre', need: (p, o, id) => others(p, id).length >= 1 || 'Serve almeno 1 altra carta da scartare', fx: async (p, o, id) => { const n = others(p, id).length; const opts = [{ label: 'Scarta 1: +1 MOV e +1 ATT (questo turno)', value: 1 }, { label: `Scarta 2: ${o.name} perde ${BAL.ti22} turni`, value: 2, disabled: n < 2 }, { label: `Scarta 4: 3 danni a ${o.name}`, value: 4, disabled: n < 4 }]; const ch = await ask(p, 'Fuori dai ranghi: scegli', opts, { ai: () => n >= 2 ? 2 : 1 }); await discardN(p, ch, id); if (ch === 1) addMod(p, { label: 'Fuori dai ranghi', mov: 1, att: 1, kind: 'turn' }); if (ch === 2) for (const x of foes(p, o)) loseTurns(x, BAL.ti22); if (ch === 4) await harm(o, 3 + sb(p)); }, ai: (p, o, id) => others(p, id).length >= 3 ? 3 : 0 });
T({ id: 'TI-23', when: 'fuori', fx: async p => { if (G.map && G.map.id === 'TM-05') addMod(p, { label: 'Furia della natura', mov: 5, att: 3, adv: true, kind: 'game' }); else { log('Selva non attiva: +2 MOV +1 ATT per questo turno.'); addMod(p, { label: 'Furia della natura', mov: 2, att: BAL.ti23att, kind: 'turn' }); } }, ai: () => (G.map && G.map.id === 'TM-05') ? 6 : (G.phase === 'prima' ? 1 : -1) });
T({ id: 'TI-24', when: 'fuori', need: (p, o) => o.discard.length > 0 || 'Gli scarti dell\'avversario sono vuoti', fx: async (p, o) => { const pk = await chooseFrom(p, [...o.discard], `Prendi una carta dagli scarti di ${o.name}: va giocata subito`); o.discard.splice(o.discard.indexOf(pk), 1); p.hand.push(pk); if (!(await playCard(p, pk, { free: true, immediate: true }))) { p.hand.splice(p.hand.indexOf(pk), 1); o.discard.push(pk); log('Non si può giocare: torna negli scarti e l\'avversario riprende una carta.'); if (o.discard.length) { const r = pick(o.discard.filter(x => x !== pk).length ? o.discard.filter(x => x !== pk) : o.discard); o.discard.splice(o.discard.indexOf(r), 1); o.hand.push(r); log(`${o.name} riprende «${C(r).nome}».`); } } }, ai: (p, o) => o.discard.length ? 2 : 0 });
T({ id: 'TI-25', when: 'fuori', fx: async (p, o) => { if (G.swap) { swapHands(); log('Il Gatto Ciclone precedente finisce.'); } G.swap = { owner: p.id, a: p.id, b: o.id, left: 3 }; swapHands(); log(`${p.name} e ${o.name} si scambiano mano e pila degli scarti per 3 turni.`, 'gold'); }, ai: (p, o, id) => o.hand.length > others(p, id).length + 2 ? 2 : 0, nota: 'Dopo 3 turni di chi l\'ha giocata, mani e scarti tornano a scambiarsi.' });
T({ id: 'TI-26', when: 'sempre', fx: async (p, o) => { const f = foeOf(p); const tgt = f && !f.isCreature ? f : o; let kind = 'scontri'; if (isC(p, 'Warlock')) { const ch = await ask(p, 'Guardiano di Dorko: sacrifichi 3 PV per renderlo permanente?', [{ label: 'Sì, sacrifica 3 PV', value: 'y' }, { label: 'No', value: 'n' }], { ai: () => p.pv > 6 ? 'y' : 'n' }); if (ch === 'y') { await harm(p, 3); kind = 'game'; } } addMod(tgt, { label: 'Guardiano di Dorko', att: -2, ar: -2, kind, n: 1 }); log(`${tgt.name}: −2 ATT e −2 AR ${kind === 'game' ? 'fino alla fine della partita' : 'nel prossimo scontro'}.`); }, ai: () => 2, nota: 'Se non sacrifichi i PV dura il prossimo scontro dell\'avversario (o quello in corso).' });
T({ id: 'TI-27', when: 'fuori', fx: async p => { p.flags.fabbro = (p.flags.fabbro || 0) + 1; log('Ogni arma che impugni dà +1 ATT per il resto della partita.'); }, ai: p => weapons(p).length ? 3 : 0, nota: '+1 ATT per ogni arma impugnata, per tutta la partita.' });
T({ id: 'TI-28', when: 'fuori', need: (p, o, id) => others(p, id).length >= 1 || 'Serve un\'altra carta da scartare', fx: async (p, o, id) => { await discardN(p, 1, id); for (const x of foes(p, o)) loseTurns(x, 2); }, ai: () => 4 });
T({ id: 'TI-29', when: 'fuori', need: (p, o) => o.discard.length > 0 || 'Gli scarti dell\'avversario sono vuoti', fx: async (p, o) => { const pk = await chooseFrom(p, [...o.discard], `Prendi una carta dagli scarti di ${o.name}: va giocata subito`); o.discard.splice(o.discard.indexOf(pk), 1); p.hand.push(pk); if (!(await playCard(p, pk, { free: true, immediate: true }))) { p.hand.splice(p.hand.indexOf(pk), 1); o.discard.push(pk); log('Non si può giocare: torna negli scarti dell\'avversario.'); } if (isC(p, 'Bardo')) giveInsp(p); }, ai: (p, o) => o.discard.length ? 2 : 0 });
T({ id: 'TI-30', when: 'fuori', fx: async (p, o) => { if (G.map && G.map.id === 'TM-05') { const d = await roll(p, 6, 'Impero silvano'); for (const x of foes(p, o)) loseTurns(x, d); } else if (BAL.ti30 === 1) for (const x of foes(p, o)) loseTurns(x, 1); else for (const x of foes(p, o)) { addMod(x, { label: 'Impero silvano: −2 MOV', mov: -2, kind: 'turni', n: 1 }); log(`${x.name}: −2 MOV nel suo prossimo turno.`); } }, ai: () => (G.map && G.map.id === 'TM-05') ? 6 : 3 });
T({ id: 'TI-31', when: 'sempre', need: (p, o, id) => p.discard.length > 0 || 'La pila degli scarti è vuota', fx: async (p, o, id) => { await recover(p, 1, { except: id }); }, ai: p => p.discard.length ? 2 : 0 });
T({ id: 'TI-32', when: 'sempre', fx: async p => givePotions(p, isC(p, 'Druido') ? BAL.ti32 : 1), ai: () => 2, nota: 'Le pozioni arrivano come copie extra delle carte Pozione e spariscono dopo l\'uso.' });
T({ id: 'TI-33', when: 'fuori', fx: async () => { for (const x of G.players) for (const s of Object.keys(x.equip)) if (x.equip[s]) { log(`${x.name} perde ${C(x.equip[s]).nome}.`); unequip(x, x.equip[s]); } }, ai: (p, o) => equipped(o).length - equipped(p).length - 1 });
T({ id: 'TI-34', when: 'scontro', need: () => (G.combat.foe.isCreature && G.combat.kind !== 'boss') || 'Solo contro creature e mini-boss (non boss né avversario)', fx: async p => { const ch = await ask(p, 'La Morte sopraggiunge: scegli il prezzo', [{ label: 'Subisci 3 danni', value: 'd', disabled: p.pv <= 3 }, { label: 'Perdi 4 turni', value: 't' }], { ai: () => p.pv > 5 ? 'd' : 't' }); if (ch === 'd') await hurt(p, 3, G.combat); else loseTurns(p, 4); G.combat.foe.pv = 0; log('Il nemico viene eliminato.', 'good'); }, ai: (p) => G.combat && G.combat.foe.pv > 4 && p.pv > 5 ? 4 : 0, nota: 'Conta come vittoria: ottieni indizio e PE.' });
T({ id: 'TI-35', when: 'fuori', fx: async (p, o) => { let d = await roll(p, BAL.noD4 ? 6 : 4, 'Lo speziale', { bad: v => v <= 2 }); while (d > 4) { log('Con 5 o 6 si ritira.'); d = await roll(p, 6, 'Lo speziale (ritiro)', { bad: v => v <= 2 }); } if (d === 1) await harm(p, 1); if (d === 2) { p.base.ar--; log(`${p.name}: −1 AR permanente.`, 'bad'); } if (d === 3) { p.base.mov += 2; log(`${p.name}: +2 MOV permanente.`, 'good'); } if (d === 4) await harm(o, 2); }, ai: () => 1 });
T({ id: 'TI-36', when: 'scontro', fx: async (p, o, id) => { await hurt(foeOf(p), BAL.luce + sb(p), G.combat); if (isR(p, 'Aasimar')) heal(p, 2 + sb(p)); if (isC(p, 'Paladino')) await recover(p, 1, { except: id }); }, ai: () => 3 });
T({ id: 'TI-37', when: 'fuori', fx: async (p, o) => { for (const x of foes(p, o)) { x.curse = true; log(`Nel prossimo scontro ${x.name} dovrà tirare D6: con 1-3 è costretto a fuggire.`); } }, ai: () => 2, nota: 'Si gioca nel tuo turno e colpisce il prossimo scontro dell\'avversario. Con 4-6 lui ottiene +1 ATT per quello scontro.' });
T({ id: 'TI-38', when: 'sempre', nota: 'Il ritiro gratuito era del Mago: ora è della carta stessa (mazzetto Chierico).', fx: async p => { const S6 = BAL.noD4 ? 6 : 4, ok = BAL.noD4 ? 4 : 3; let d = await roll(p, S6, 'Medico del villaggio'); if (d < ok) { const ch = await ask(p, `Medico del villaggio: è uscito ${d}. Puoi ritirare il dado una volta.`, [{ label: 'Ritira', value: 'y' }, { label: 'Tieni', value: 'n' }], { ai: () => 'y' }); if (ch === 'y') d = await roll(p, S6, 'Medico del villaggio (ritiro)'); } if (d >= ok) heal(p, 4 + sb(p)); else log('Non succede niente.'); }, ai: p => maxPV(p) - p.pv >= 3 ? 2 : 0 });
T({ id: 'TI-39', when: 'fuori', need: () => BAL.ti39 || !!G.map || 'Nessuna mappa attiva', fx: async (p, o) => { if (!G.map) { for (const x of foes(p, o)) { log(`Il terreno frana sotto i piedi di ${x.name}.`); loseTurns(x, 1); } return; } G.players[G.map.owner].discard.push(G.map.id); log(`La mappa «${C(G.map.id).nome}» viene distrutta. Il tesoro resta dov'è.`); G.map = null; }, ai: (p, o) => { if (!G.map) return BAL.ti39 ? 2 : 0; const s = x => { const b = mapBonus(x); return b.att + b.ar + b.adv - b.dis; }; return s(o) - s(p); } });
T({ id: 'TI-40', when: 'scontro', need: () => G.combat.foe.isCreature || 'Non si può usare sull\'avversario', fx: async p => { let d = 3; if (isC(p, 'Mago', 'Stregone')) { const x = await roll(p, 6, 'Meteora di fuoco'); d = x <= 3 ? 4 : 8; } await hurt(G.combat.foe, d + sb(p), G.combat); }, ai: () => 4 });
T({ id: 'TI-41', when: 'fuori', need: (p, o) => isLocated(o) || 'L\'avversario non ha individuato il tesoro', fx: async (p, o) => { log('Il forziere era un Mimik!', 'gold'); randomDiscard(o, 2); await harm(o, 1); moveTreasure(); if (BAL.mimik === 'relocate') locate(o); }, ai: () => 6, nota: 'Il tesoro si sposta: chi aveva individuato il tesoro lo perde, ma l\'avversario lo individua di nuovo subito.' });
T({ id: 'TI-42', when: 'fuori', need: p => isC(p, 'Druido') || 'Serve classe Druido', fx: async p => { addMod(p, { label: 'Mutaforma (+2)', att: 2, mov: 2, ar: 2, pv: 2, kind: 'turni', n: BAL.muta }); if (BAL.mutaClue) await addClue(p); for (const id of equipped(p)) { for (const k in p.equip) if (p.equip[k] === id) p.equip[k] = null; p.servants = p.servants.filter(s => s.src !== id); p.hand.push(id); } clamp(p); log(BAL.mutaClue ? 'La bestia fiuta la pista: +1 indizio. L\'equipaggiamento torna nella tua mano.' : 'L\'equipaggiamento torna nella tua mano.'); }, ai: p => p.located ? 1 : 3, nota: '+2 a tutto per 3 turni. L\'equipaggiamento torna in mano.' });
T({ id: 'TI-43', when: 'sempre', need: p => p.servants.length > 0 || 'Serve un servitore', fx: async p => { const half = BAL.patto === 'half' ? Math.floor(p.pv / 2) : Math.min(BAL.patto, p.pv - 1); const s = p.servants[0]; p.pv -= half; s.pv += half; s.maxpv += half; p.flags.patto = true; log(`${p.name} cede ${half} PV a ${s.name}, che subirà i danni al posto suo.`); if (isC(p, 'Warlock')) { p.flags.pattoW = true; if (G.combat) await hurt(foeOf(p), 1, G.combat); } }, ai: p => p.pv >= 6 ? 2 : 0, nota: 'Il primo servitore riceve metà dei tuoi PV e in scontro subisce i colpi al tuo posto. Warlock: 1 danno subito e i servitori fanno +1 danno.' });
T({ id: 'TI-44', when: 'sempre', fx: async p => { addMod(p, { label: 'Potere controllato', att: 1, kind: 'turn' }); if (true) { p.limit++; log('Puoi giocare una carta in più in questo turno.'); } }, ai: () => G.combat ? 2 : 0, nota: 'Una carta in più in questo turno (in hot-seat sostituisce «giocare nel turno dell\'avversario»).' });
T({ id: 'TI-45', when: 'fuori', fx: async (p, o) => { if (BAL.ti45 === 'dietroPV') { if (o.clues > p.clues) { if (o.located) { o.located = false; o.clues = 2; } else o.clues--; log(`${o.name} perde 1 Indizio.`, 'bad'); } await harm(p, 2); return; } log(`${o.name} torna a un punto di spawn.`, 'bad'); o.pos = await rollSpawn(o, 'respawn'); p.pv = Math.min(p.pv, 1); log(`${p.name} resta con 1 PV.`, 'bad'); }, ai: (p, o) => BAL.ti45 === 'dietroPV' ? (o.clues > p.clues && p.pv > 2 ? 4 : 0) : isLocated(o) && p.pv > 1 ? 4 : 0, nota: 'Se l\'avversario ha individuato il tesoro torna a 2 indizi.' });
T({ id: 'TI-46', when: 'sempre', fx: async p => { if (isC(p, 'Chierico') && BAL.ti46 === 'assorbi') { p.turnFlags.absorb = true; log('I danni di questo turno ti curano.'); } else { p.turnFlags.half = true; log('Subisci metà dei danni per questo turno.'); } }, ai: p => G.combat && p.pv <= maxPV(p) / 2 ? 4 : 0, nota: 'Dura fino alla fine del turno in corso.' });
T({ id: 'TI-47', when: 'fuori', fx: async (p, o, id) => { loseTurns(p, 2); heal(p, 5 + sb(p)); await recover(p, isC(p, 'Bardo') ? 2 : 1, { except: id }); }, ai: p => p.pv <= maxPV(p) / 2 ? 2 : 0 });
T({ id: 'TI-48', when: 'fuori', fx: async (p, o, id) => { addMod(p, { label: 'Seguire il fiume', mov: 2, kind: 'turn' }); await recover(p, 1, { except: id }); }, ai: p => p.discard.length ? 2 : 0 });
T({ id: 'TI-49', when: 'fuori', fx: async p => { for (const x of G.players) randomDiscard(x, 2); const bet = await ask(p, 'Sfidare i potenti: quanti turni si mettono in palio?', [1, 2, 3].map(n => ({ label: `${n} turn${n === 1 ? 'o' : 'i'}`, value: n })), { ai: () => 1 }); for (const x of G.players) x.challenge = { bet }; log(`Il prossimo scontro di ciascuno sarà contro un mini-boss: ${bet} turni in palio.`, 'gold'); }, ai: () => 0, nota: 'Il prossimo scontro di ogni giocatore diventa un mini-boss. Vinto senza carte: guadagni i turni e riprendi 1 carta. Perso: perdi i turni scommessi.' });
T({ id: 'TI-50', when: 'fuori', fx: async p => { const st = isC(p, 'Stregone'); addMod(p, { label: 'Forma di drago', pv: st ? BAL.drago[0] : 10, ar: st ? BAL.drago[1] : 10, mov: st ? 2 : 1, kind: 'turni', n: 2, onExpire: 'drago' }); }, ai: p => BAL.dragoAI && G.phase === 'prima' && isLocated(p) && hexDist(p.pos, G.treasure) <= stat(p, 'mov') + 2 ? 7 : 0, nota: '+8 PV, +4 AR e +2 MOV per 2 turni. I PV extra si perdono quando torni normale; poi perdi 10 turni.' });
T({ id: 'TI-51', when: 'fuori', fx: async p => { G.stop = isR(p, 'Halfling') ? 1 : 2; log(`Nei prossimi ${G.stop} scontri nessuno può giocare carte.`); }, ai: () => 0 });
T({ id: 'TI-52', when: 'fuori', fx: async p => { await addClue(p, 2); if (BAL.ti52 === 'all') { for (const x of others2(p)) await addClue(x, 1); return; } const cand = others2(p).filter(x => !x.located); if (!cand.length) return; const t = cand.length > 1 ? await ask(p, 'Studiare la mappa: quale avversario ottiene 1 indizio?', cand.map(x => ({ label: `${x.name} (${x.clues} indizi)`, value: x.id })), { ai: () => cand.slice().sort((a, b) => a.clues - b.clues)[0].id }) : cand[0].id; await addClue(G.players[t], 1); }, ai: p => !p.located ? 3 : 0, nota: 'Tu ottieni 2 indizi, ogni avversario 1.' });
T({ id: 'TI-53', when: 'fuori', need: (p, o, id) => others(p, id).length >= 1 || 'Serve un\'altra carta da scartare', fx: async (p, o, id) => { await discardN(p, 1, id); const a = await chooseFrom(p, p.discard.filter(x => x !== id), 'Stupido rituale: carta da giocare subito'); if (!a) return; p.discard.splice(p.discard.indexOf(a), 1); const b = await chooseFrom(p, p.discard.filter(x => x !== id), isR(p, 'Halfling', 'Umano') ? 'Seconda carta: la tieni in mano' : 'Seconda carta: torna negli scarti'); p.hand.push(a); if (!(await playCard(p, a, { free: true, immediate: true }))) { p.hand.splice(p.hand.indexOf(a), 1); p.discard.push(a); log('La carta non si può giocare: torna negli scarti.'); } if (b && isR(p, 'Halfling', 'Umano')) { p.discard.splice(p.discard.indexOf(b), 1); p.hand.push(b); log(`${p.name} tiene «${C(b).nome}» in mano.`); } }, ai: p => p.discard.length >= 2 ? 1 : 0 });
T({ id: 'TI-54', when: 'fuori', fx: async p => { if (BAL.ti54 === 'clue') { for (const x of G.players) if (!x.out) await addClue(x); } else for (const x of G.players) loseTurns(x, 4); }, ai: p => BAL.ti54 === 'clue' ? (p.clues === 2 && !p.located ? 3 : others2(p).some(o => o.clues === 2 && !o.located) ? -1 : p.clues >= 1 ? 1 : 0.2) : 0 });
T({ id: 'TI-55', when: 'fuori', need: p => isR(p, 'Umano') || 'Serve una pedina Umano', fx: async p => { const cand = CLASSES.filter(c => !p.classes.includes(c)); const cls = await ask(p, 'Vera forma: scegli una classe', cand.map(c => ({ label: c, value: c, hint: CARD[CLASS_CARD[c]].testo })), { ai: () => pick(['Bardo', 'Guerriero', 'Chierico']) }); await setClass(p, cls, null, { add: true }); }, ai: p => p.classes.length < 2 ? 3 : 0, nota: 'Puoi scegliere qualsiasi classe; se ne hai già una le tieni entrambe.' });
T({ id: 'TI-56', when: 'fuori', need: (p, o, id) => (isC(p, 'Warlock') || 'Serve classe Warlock') && (others(p, id).length >= 5 || 'Servono 5 altre carte da scartare'), fx: async (p, o, id) => { await discardN(p, 5, id); loseTurns(p, BAL.zarko[1]); p.stopTurn = true; if (BAL.zarkoRitual) { p.ritual = true; log(`${p.name} inizia il rituale di Zarko: il turno finisce subito. Se viene sconfitto prima del risveglio, il rituale fallisce.`, 'gold'); return; } zarkoWake(p); log('La trasformazione richiede tempo: il turno finisce subito.'); }, ai: (p, o, id) => BAL.zarkoAI && !isLocated(p) && p.ownTurns >= 3 ? 3 : 0, nota: 'Il turno finisce subito. Durante il rituale (4 turni persi) la pedina resta sulla plancia: se viene sconfitta il rituale fallisce. Al risveglio +10 a tutto e tesoro individuato (Zarko lo vede anche se si sposta); se non vinci nei 2 turni successivi perdi.' });

// ----- Carte dell'espansione del Caos (nel mazzo comune solo con l'espansione) -----
T({ id: 'CA-01', when: 'fuori', fx: async p => { log('Biglia del nulla: frughi in una Crepa da dove sei.'); await frugare(p, isC(p, 'Mago')); }, ai: p => isLocated(p) ? 0.8 : 2.2, nota: 'Mago: tira due D6 e scegli.' });
T({ id: 'CA-02', when: 'sempre', fx: async p => { const v = await roll(p, 6, 'Pagina strappata'); if (v >= (isC(p, 'Mago') ? 4 : 5)) await addClue(p); else drawCard(p); }, ai: p => isLocated(p) ? 0.5 : 3, nota: 'Mago: basta un 4.' });
T({ id: 'CA-03', when: 'scontro', fx: async p => { const f = foeOf(p); if (f) { log('Un Coboldo pentito ti aiuta!'); await hurt(f, 3, G.combat); } }, ai: () => 3 });
DEF['CA-04'] = te(null, { nota: 'Elmo. +1 AR (Chierico: anche +1 ATT). Sulle Crepe tiri due D6 e scegli.' });
T({ id: 'CA-05', when: 'fuori', fx: async (p, o) => { o.slowNext = true; log(`Vento di nulla: nel suo prossimo turno ${o.name} muove di 1 esagono soltanto.`, 'bad'); }, ai: (p, o) => isLocated(o) ? 3 : 1.5 });
T({ id: 'CA-06', when: 'sempre', fx: async p => { const rs = []; for (const x of G.players.filter(x => !x.out)) { let v = await roll(x, 6, 'Risata del Goblin'); if (x === p) v = Math.max(v, await roll(x, 6, 'Risata del Goblin')); rs.push([x, v]); }
  const m = Math.max(...rs.map(r => r[1])), top = rs.filter(r => r[1] === m); if (top.length === 1) { log(`${top[0][0].name} ride più forte di tutti!`, 'gold'); if (!top[0][0].located) await addClue(top[0][0]); } else log('Pari merito: nessuno prende l\'indizio.'); }, ai: p => isLocated(p) ? 0 : 2.5 });
// ----- Carte leggendarie (nuove, una per classe) -----
const cluesOf = x => x.located ? 3 : x.clues;
T({ id: 'TI-57', when: 'scontro', fx: async p => { const c = G.combat; c.berserk[p.id] = true; addCmod(c, p, 'att', 3); log(`${p.name} entra in furia: +3 ATT e +2 danni a colpo, niente fuga.`); }, ai: p => { const c = G.combat; return c && (c.kind !== 'creatura' || c.foe.pv >= 6) && p.pv > 3 ? 5 : 0; }, nota: 'Dura tutto lo scontro in corso. A fine scontro perdi 2 PV, ma non scendi sotto 1.' });
T({ id: 'TI-58', when: 'fuori', fx: async p => { const n = Math.min(BAL.canzoneMax, others2(p).filter(x => cluesOf(x) > cluesOf(p)).length); if (n && !p.located) await addClue(p, n); else giveInsp(p, 'Canzone della fama'); }, ai: p => { const n = Math.min(BAL.canzoneMax, others2(p).filter(x => cluesOf(x) > cluesOf(p)).length); return n && !p.located ? 3 + n : 0; }, nota: 'Carta di rimonta: conta chi è davanti a te negli indizi (chi ha individuato il tesoro vale 3).' });
T({ id: 'TI-59', when: 'sempre', fx: async p => { heal(p, maxPV(p)); if (p.skip) { log(`${p.name} annulla ${p.skip} turni persi.`, 'good'); p.skip = 0; } }, ai: p => (maxPV(p) - p.pv >= 6 || (G.combat && p.pv <= 3)) ? 6 : 0 });
T({ id: 'TI-60', when: 'fuori', fx: async p => { const i = p.servants.findIndex(s => s.cls && s.name === 'Fuoco fatuo'); const lupo = { name: 'Lupo', pv: 3, maxpv: 3, att: BAL.lupo[0], ar: 0, dmg: BAL.lupo[1], cls: true }; if (i >= 0) p.servants[i] = lupo; else p.servants.push(lupo); log(`Un Lupo si unisce a te (PV 3, ATT ${BAL.lupo[0]}, ${BAL.lupo[1]} danni a colpo).`, 'good'); }, ai: () => 4 });
T({ id: 'TI-61', when: 'scontro', fx: async p => { G.combat.carica[p.id] = true; log(`${p.name} carica: due attacchi per round in questo scontro.`); }, ai: () => { const c = G.combat; return c && (c.kind !== 'creatura' || c.foe.pv >= 6) ? 5 : 0; } });
const ladroTargets = p => others2(p).filter(x => cluesOf(x) > 0 && x.pos.c >= 0 && hexDist(x.pos, p.pos) <= BAL.colpoRange);
T({ id: 'TI-62', when: 'fuori', need: p => ladroTargets(p).length > 0 || `Nessun avversario con indizi entro ${BAL.colpoRange} caselle`, fx: async p => { const cand = ladroTargets(p); const t = cand.length > 1 ? G.players[await ask(p, 'Colpo grosso: a chi rubi un indizio?', cand.map(x => ({ label: `${x.name} (${cluesOf(x)} indizi)`, value: x.id })), { ai: () => cand.slice().sort((a, b) => cluesOf(b) - cluesOf(a))[0].id })] : cand[0]; if (t.located) { t.located = false; t.clues = 2; } else t.clues--; log(`${p.name} ruba un indizio a ${t.name}!`, 'gold'); await addClue(p); }, ai: p => !p.located ? 6 : 0, nota: 'Se l\'avversario aveva individuato il tesoro, torna a 2 indizi.' });
T({ id: 'TI-63', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima di muoverti', fx: async p => { p.portal = 8; log('Il portale si apre: questo turno ti sposti fino a 8 caselle senza tirare.'); }, ai: p => isLocated(p) && hexDist(p.pos, G.treasure) > stat(p, 'mov') + 2 && hexDist(p.pos, G.treasure) <= 8 ? 6 : 0 });
T({ id: 'TI-64', when: 'scontro', need: () => G.combat.foe.isCreature || 'Solo contro creature, mini-boss e boss', fx: async p => { await hurt(G.combat.foe, BAL.punizione + sb(p), G.combat); }, ai: () => { const c = G.combat; return c && c.foe.isCreature && (c.kind !== 'creatura' || c.foe.pv >= 5) ? 5 : 0; } });
T({ id: 'TI-65', when: 'fuori', fx: async p => { for (const x of others2(p)) await harm(x, BAL.tempesta + sb(p)); }, ai: p => others2(p).some(x => x.pv <= BAL.tempesta + sb(p)) ? 5 : 2 });
T({ id: 'TI-66', when: 'fuori', need: p => (p.pv > BAL.pattoOscuro || `Servono più di ${BAL.pattoOscuro} PV`) && (p.servants.some(s => s.name === 'Imp') || 'Serve l\'Imp'), fx: async p => { p.pv -= BAL.pattoOscuro; if (BAL.pattoOscuro) log(`${p.name} paga ${BAL.pattoOscuro} PV.`, 'bad'); const i = p.servants.findIndex(s => s.name === 'Imp'); const s0 = p.servants[i]; p.servants[i] = { name: 'Demone', pv: 6, maxpv: 6, att: 4 + (s0.att - 2), ar: s0.ar, dmg: 3, cls: true }; log('L\'Imp diventa un Demone (PV 6, ATT 4, 3 danni a colpo).', 'good'); }, ai: p => p.pv > 6 ? 4 : 0 });

// ===================== Gioco delle carte =====================
function zarkoWake(p) {
  p.ritual = false;
  addMod(p, { label: 'Zarko predatore della vita', att: BAL.zarko[0], mov: BAL.zarko[0], ar: BAL.zarko[2] ?? BAL.zarko[0], pv: BAL.zarko[3] ?? BAL.zarko[0], kind: 'game' });
  locate(p); p.zarko = 2; p.zarkoStart = p.ownTurns;
  log(`${p.name} diventa Zarko predatore della vita! Se non vince entro 2 turni, perde la partita.`, 'bad');
}
const isGear = id => C(id).tipo === 'TE' && SLOT[baseId(id)] !== 'pozione';
function canPlay(p, id, { free = false } = {}) {
  const d = DEF[baseId(id)]; const c = G.combat; const o = opp(p);
  if (!d) return 'Carta sconosciuta';
  if (isGear(id) && p.eqTurn) return 'Puoi equipaggiare un solo oggetto per turno';
  if (C(id).cls && !isC(p, C(id).cls)) return `Carta di classe ${C(id).cls}: la può giocare solo un ${C(id).cls}`;
  if (G.over) return 'Partita finita';
  if (p.noCardsFrom && p.ownTurns >= p.noCardsFrom && p.ownTurns <= p.noCardsTo) return 'Esercito nanico: niente carte Trama in questo turno';
  if (c) {
    if (c.noCards) return 'Stop: nessuna carta in questo scontro';
    if (d.when === 'fuori') return 'Non si gioca durante uno scontro';
    if (!free) {
      if (c.p === p) { if (p.played >= p.limit) return `Hai già giocato ${p.limit} carte in questo turno`; }
      else if (c.foe === p) { if (c.defCards >= 1) return 'In difesa puoi giocare 1 sola carta per scontro'; }
      else return 'Non sei nello scontro';
    }
  } else {
    if (d.when === 'scontro') return 'Si gioca solo durante uno scontro';
    if (!free && p.played >= p.limit) return `Hai già giocato ${p.limit} carte in questo turno`;
  }
  const r = d.need ? d.need(p, o, id) : true;
  return (r === true || r === undefined) ? true : r;
}
async function playCard(p, id, { free = false, immediate = false } = {}) {
  const why = canPlay(p, id, { free });
  if (why !== true) { if (!immediate) { flashMsg = why; render(); } return false; }
  tick('carta'); const hi = p.hand.indexOf(id); if (hi >= 0) p.hand.splice(hi, 1);
  if (isGear(id)) p.eqTurn = true;
  if (!free) { if (G.combat && G.combat.foe === p) G.combat.defCards++; else p.played++; }
  if (G.combat) G.combat.used[p.id] = true;
  if (p.burattinato === 'active' && !free) {
    p.burattinato = null; if (!id.includes('~')) p.discard.push(id);
    log(`Burattinaio oscuro: «${C(id).nome}» viene scartata senza effetto.`, 'bad'); render(); return true;
  }
  log(`${p.name} gioca «${C(id).nome}».`, 'play');
  if (G.stats && !id.includes('~') && C(id).tipo !== 'TC') G.stats.played[p.id].push(baseId(id));
  const prevT = p._target;
  const cf = foeOf(p);
  if (cf && !cf.isCreature) p._target = cf;
  else if (TARG.has(baseId(id)) && others2(p).length > 1 && !(BAL.allOpp && FOES.has(baseId(id)) && !BAL.foesOff.includes(baseId(id)) && baseId(id) !== 'TI-22' && baseId(id) !== 'TE-18')) {
    let cand = others2(p);
    if (TARG_LOCATED.has(baseId(id))) cand = cand.filter(x => DEF[baseId(id)].need(p, x, id) === true);
    if (cand.length > 1) { const t = await ask(p, `«${C(id).nome}»: contro quale avversario?`, cand.map(x => ({ label: x.name, value: x.id })), { ai: () => defaultOpp(p).id }); p._target = G.players[t]; }
    else if (cand.length) p._target = cand[0];
  }
  let keep; const prevC = G.curCard; G.curCard = baseId(id);
  try { keep = await DEF[baseId(id)].fx(p, opp(p), id); } finally { p._target = prevT; G.curCard = prevC; }
  if (keep !== 'keep' && !id.includes('~')) p.discard.push(id);
  for (const x of G.players) clamp(x);
  render();
  return true;
}
function swapHands(a = G.players[G.swap.a], b = G.players[G.swap.b]) { [a.hand, b.hand] = [b.hand, a.hand];[a.discard, b.discard] = [b.discard, a.discard]; }

// ===================== IA =====================
function aiScore(p, id) {
  if (canPlay(p, id) !== true) return -99;
  const d = DEF[baseId(id)];
  return (d.ai ? d.ai(p, opp(p), id) : 0) + Math.random() * 0.5;
}
function aiPickBest(p, ids) { let best = ids[0], bs = -1e9; for (const id of ids) { const d = DEF[baseId(id)]; const s = (d && d.ai ? d.ai(p, opp(p), id) : 0) + Math.random(); if (s > bs) { bs = s; best = id; } } return best; }
function aiPickWorst(p, ids) { let w = ids[0], ws = 1e9; for (const id of ids) { const d = DEF[baseId(id)]; const s = (d && d.ai ? d.ai(p, opp(p), id) : 0) + Math.random(); if (s < ws) { ws = s; w = id; } } return w; }
function aiBestCard(p, min) {
  let best = null, bs = min;
  for (const id of p.hand) { const s = aiScore(p, id); if (s > bs) { bs = s; best = id; } }
  return best;
}
function power(x, c) { const pv = x.pv; const [s, b] = dmgDice(x); return pv * (s / 2 + b) * (atkOf(x, c) + 11) / 20; }
function aiCombat(x, c, opts) {
  const foe = x === c.p ? c.foe : c.p;
  if (opts.some(o => o.value === 'pal') && x.pv <= maxPV(x) / 2) return 'pal';
  const card = aiBestCard(x, 1.5);
  if (card) return { card };
  if (opts.some(o => o.value === 'guer')) return 'guer';
  if (opts.some(o => o.value === 'fuga') && x.pv <= 3 && power(foe, c) > power(x, c) * 1.3 && c.kind !== 'boss') return 'fuga';
  return 'attacca';
}
function aiMove(p, hexes) {
  const o = opp(p);
  const rit = others2(p).find(x => x.ritual && power(p) >= power(x) * 0.8);
  if (rit && !isLocated(p)) { const adj = hexes.filter(h => hexDist(h, rit.pos) <= 1); if (adj.length) return pick(adj); }
  if (isLocated(p)) {
    // con l'espansione del Caos una Crepa vale quanto la sua gemella, se attraversare fa guadagnare almeno 2 esagoni
    const sc = h => { const d = hexDist(h, G.treasure); if (!BAL.caos || !crepaAttiva(h)) return d; const tw = twinOf(h), dt = hexDist(tw, G.treasure); return freeHex(tw, p) && dt <= d - 2 ? Math.min(d, dt + 0.5) : d; };
    return hexes.slice().sort((a, b) => sc(a) - sc(b))[0];
  }
  if (power(p) > power(o) * 1.4 && o.clues > 0) { const adj = hexes.filter(h => hexDist(h, o.pos) <= 1); if (adj.length) return pick(adj); }
  const fresh = hexes.filter(h => !tileAt(h).done && tileAt(h).type !== 'start' && !(bOnce() && tileAt(h).used && BUILDINGS.includes(tileAt(h).type) && tileAt(h).used.includes(p.id)) && others2(p).every(x => hexDist(h, x.pos) > 1));
  const weak = p.pv <= 3;
  const pool = fresh.filter(h => { const t = tileAt(h); if (!t.revealed) return true; if (weak) return ['locanda', 'fonte', 'fabbro', 'indizio'].includes(t.type); return t.type !== 'trappola'; });
  return pick(pool.length ? pool : (fresh.length ? fresh : hexes));
}

// ===================== Turno =====================
async function playTurn(p) {
  tick('turno'); p.ownTurns++; p.played = 0; p.limit = 2; p.eqTurn = false;
  if (BAL.magoPerTurn && isC(p, 'Mago')) p.magoRerolls = 1;
  if (BAL.palPerTurn && isC(p, 'Paladino')) p.palHeals = 1; p.turnStart = { ...p.pos }; p.defeated = false;
  if (p.burattinato === 'pending') p.burattinato = 'active';
  G.phase = 'inizio';
  log(`Turno di ${p.name}`, 'turn');
  if (p.skip > 0) {
    p.skip--; log(`${p.name} perde questo turno${p.skip ? ` (ne restano ${p.skip})` : ''}.`);
    if (!p.skip && p.ritual) zarkoWake(p);
    if (!G.fast) { render(); await sleep(Math.min(S.speed, 400)); } await endOfTurn(p, true); return;
  }
  if (p.ashafe > 0) heal(p, 1);
  const gt = Math.floor(G.round / G.players.length) + 1;
  if (BAL.clock && gt >= BAL.clock && (gt - BAL.clock) % BAL.clockEvery === 0 && !p.located) { log(`Il Goblin si agita (giro ${gt}): la pista si fa più chiara.`, 'gold'); await addClue(p); }
  if (BAL.omen && !p.located && gt >= BAL.omen[0]) { const need = Math.max(2, 6 - Math.floor((gt - BAL.omen[0]) / BAL.omen[1])); const v = await roll(p, 6, `Presagio (serve ${need}+)`); if (v >= need) { log('Il presagio indica la strada.', 'gold'); await addClue(p); } }
  if (BAL.pity && !p.located) { p.dry = (p.dry || 0) + 1; if (p.dry >= BAL.pity) { log(`${p.name}: dopo ${BAL.pity} turni senza indizi la pista si fa chiara.`, 'gold'); await addClue(p); } }
  G.phase = 'prima';
  while (true) {
    const o = [{ label: `Tira il dado di movimento (D${G.rules.die}${fmt(stat(p, 'mov'))})`, value: 'move' }];
    if (isC(p, 'Paladino') && p.palHeals > 0 && p.pv < maxPV(p)) o.push({ label: `Paladino: cura 2 PV (${p.palHeals} rimaste)`, value: 'pal' });
    const a = await ask(p, 'Gioca fino a 2 carte, poi muoviti', o, { cards: true, ai: () => { const c = aiBestCard(p, 1); if (c) return { card: c }; if (o[1] && p.pv <= maxPV(p) - 2) return 'pal'; return 'move'; } });
    if (G.over) return;
    if (a && a.card) { await playCard(p, a.card); if (G.over) return; if (p.stopTurn) break; continue; }
    if (a === 'pal') { p.palHeals--; heal(p, 2); continue; }
    break;
  }
  if (p.stopTurn) { p.stopTurn = false; await endOfTurn(p, false); return; }
  if (!p.defeated) {
    G.phase = 'movimento';
    let n;
    if (p.portal) { n = p.portal; p.portal = 0; log(`Portale arcano: ${p.name} si sposta fino a ${n} caselle senza tirare il dado.`); }
    else if (p.slowNext) { p.slowNext = false; n = 1; log(`Vento di nulla: ${p.name} muove di 1 esagono soltanto.`, 'bad'); }
    else { const v = await roll(p, G.rules.die, 'Movimento', { bad: v => v <= 1 }); n = Math.max(1, v + stat(p, 'mov')); }
    tick('movimento'); log(`${p.name} può muoversi fino a ${n} caselle.`);
    const hexes = allHexes().filter(h => { const d = hexDist(h, p.pos); return d >= 1 && d <= n; });
    const dest = await pickHex(p, hexes, `Scegli dove andare (fino a ${n} caselle)`);
    p.prev = { ...p.pos }; p.pos = { ...dest };
    await resolveArrival(p);
    if (G.over) return;
  }
  G.phase = 'dopo';
  while (true) {
    const o = [{ label: 'Fine turno', value: 'end' }];
    if (isC(p, 'Paladino') && p.palHeals > 0 && p.pv < maxPV(p)) o.push({ label: `Paladino: cura 2 PV (${p.palHeals} rimaste)`, value: 'pal' });
    const a = await ask(p, 'Puoi ancora giocare carte, poi chiudi il turno', o, { cards: true, ai: () => { const c = aiBestCard(p, 2.5); return c ? { card: c } : 'end'; } });
    if (G.over) return;
    if (a && a.card) { await playCard(p, a.card); if (G.over) return; continue; }
    if (a === 'pal') { p.palHeals--; heal(p, 2); continue; }
    break;
  }
  await endOfTurn(p, false);
}
async function meetCreature(p, kind) {
  if (p.challenge) { kind = 'miniboss'; log('Sfidare i potenti: al posto della creatura appare un mini-boss!', 'gold'); }
  const foe = kind === 'miniboss' ? makeCreature(pick(MINIBOSS), p.level) : makeCreature(pick(BESTIARIO), p.level);
  const st = `${foe.name}: PV ${foe.pv}, ATT ${fmt(foe.att)}, AR ${foe.ar}, danni ${dmgLabel(foe)}`;
  const ch = await ask(p, `Incontri ${kind === 'miniboss' ? 'un mini-boss' : 'una creatura'}! ${st}`, [{ label: 'Affronta lo scontro', value: 'f' }, { label: 'Fuggi (arretri di una casella)', value: 'r' }], { ai: () => (power(foe) > power(p) * 1.6 && p.pv <= 4 ? 'r' : 'f') });
  if (ch === 'r') { log(`${p.name} dichiara la fuga.`); if (isC(p, 'Ladro')) log('Ladro: fugge senza arretrare.'); else retreat(p, p.turnStart); return; }
  await scontro(p, foe, kind);
}
// Espansione «Il Caos del Goblin · Le Crepe di MIMI»: Crepe gemelle a mezzo giro, frugare (D6) o attraversare
const COBOLDI = [
  { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Coboldo di MIMI', pv: 4, att: 1, ar: 0, dmg: [4, 0] },
  { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true },
  { name: 'Coboldo fromboliere', pv: 3, att: 2, ar: 0, dmg: [4, 0], agguato: true },
  { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true },
  { name: 'Coboldo borseggiatore', pv: 4, att: 1, ar: 1, dmg: [4, 0], borseggio: true },
];
const CHAOS_TAB = { 1: 'Crollo', 2: 'Imboscata', 3: 'Vento del Goblin', 4: 'Bottega del Goblin', 5: 'Mappa perduta', 6: 'Scambio' };
const CHAOS_RANK = { 1: 0, 2: 4, 3: 2, 4: 3, 5: 6, 6: 1 };
const twinOf = h => ({ c: COLS - 1 - h.c, r: ROWS - 1 - h.r });
const freeHex = (h, p) => G.players.every(x => x === p || x.out || hexDist(x.pos, h) > 1);
// con una carta Terreno (Mappa) in gioco restano solo le coppie E1·F10 e J3·A8
const crepaAttiva = h => tileAt(h).type === 'evento' && (!G.map || [[4, 0], [5, 9], [9, 2], [0, 7]].some(([c, r]) => h.c === c && h.r === r));
const commonPool = () => COMMON.filter(id => BAL.caos || !id.startsWith('CA-'));
// pesca una carta comune che nessuno ha (né in mano, né negli scarti, né equipaggiata)
function drawCard(p) {
  const used = new Set(G.players.flatMap(x => [...x.hand, ...x.discard, ...equipped(x)].map(baseId)));
  const id = shuffle(commonPool().filter(id => !used.has(id) && C(id).tipo !== 'TM'))[0];
  if (id) { p.hand.push(id); log(`${p.name} pesca «${C(id).nome}».`, 'good'); } else log('Non ci sono carte da pescare.');
}
async function chaosEvent(p) {
  const tw = twinOf(p.pos);
  if (!crepaAttiva(p.pos)) { log('Il Terreno ha sepolto questa Crepa: non succede niente.'); return; }
  if (crepaAttiva(tw) && freeHex(tw, p)) {
    const gain = hexDist(p.pos, G.treasure) - hexDist(tw, G.treasure);
    const ch = await ask(p, 'Sei su una Crepa: frughi o attraversi fino alla Crepa gemella? Attraversando, il turno finisce lì.', [{ label: 'Fruga (tira il D6)', value: 'f' }, { label: 'Attraversa', value: 't' }], { ai: () => (isLocated(p) && gain >= 2 ? 't' : 'f') });
    if (ch === 't') { tick('movimento'); p.prev = { ...p.pos }; p.pos = { ...tw }; log(`${p.name} attraversa il fondo del baule ed esce dalla Crepa gemella.`, 'gold'); return; }
  }
  await frugare(p);
}
async function frugare(p, two = false) {
  let v = await roll(p, 6, 'Crepa');
  if (two || has(p, 'CA-04')) {
    const w = await roll(p, 6, 'Crepa (secondo dado)');
    if (w !== v) v = await ask(p, `Quale dado tieni? ${v} = ${CHAOS_TAB[v]}, ${w} = ${CHAOS_TAB[w]}`, [{ label: `${v} · ${CHAOS_TAB[v]}`, value: v }, { label: `${w} · ${CHAOS_TAB[w]}`, value: w }], { ai: () => (CHAOS_RANK[w] > CHAOS_RANK[v] ? w : v) });
  }
  switch (v) {
    case 1: log('Crollo! Massi dal soffitto: 2 danni.', 'bad'); await harm(p, 2); break;
    case 2: {
      if (p.turnFlags && p.turnFlags.fought) { log('Imboscata! Ma il Coboldo vede che hai già combattuto in questo turno e scappa.'); break; }
      if (!G.cob || !G.cob.length) G.cob = shuffle([...COBOLDI]);
      const d = G.cob.pop(); log(`Imboscata dei Coboldi di MIMI: ${d.name}!`, 'bad');
      const foe = makeCreature(d, 1); foe.cob = true; foe.agguato = !!d.agguato; foe.borseggio = !!d.borseggio;
      await scontro(p, foe, 'creatura'); break;
    }
    case 3: {
      log('Vento del Goblin: ti muovi subito di nuovo.', 'good');
      const d = await roll(p, 6, 'Vento del Goblin');
      const hexes = allHexes().filter(h => { const x = hexDist(h, p.pos); return x >= 1 && x <= d; });
      const dest = await pickHex(p, hexes, `Vento del Goblin: scegli dove andare (fino a ${d} caselle)`);
      p.prev = { ...p.pos }; p.pos = { ...dest }; await resolveArrival(p); break;
    }
    case 4: log('Bottega del Goblin: riprendi una carta dai tuoi scarti.', 'good'); await recover(p, 1); break;
    case 5: log('Mappa perduta: un indizio!', 'gold'); await addClue(p); break;
    case 6: {
      const os = others2(p).filter(o => !o.out);
      const dT = x => hexDist(x.pos, G.treasure);
      const ch = await ask(p, 'Scambio del Goblin: puoi scambiarti di posto con un eroe', [...os.map(o => ({ label: `Scambia con ${o.name}`, value: o.id })), { label: 'Nessuno scambio', value: 'no' }], { ai: () => {
        const best = os.filter(o => isLocated(p) ? dT(o) < dT(p) - 1 : isLocated(o) && dT(o) < dT(p) - 1).sort((a, b) => dT(a) - dT(b))[0];
        return best ? best.id : 'no'; } });
      if (ch !== 'no') { const o = G.players[ch]; [p.pos, o.pos] = [o.pos, p.pos]; log(`${p.name} e ${o.name} si scambiano di posto!`, 'gold'); }
      else log('Nessuno scambio.');
      break;
    }
  }
}
async function resolveArrival(p) {
  const t = tileAt(p.pos);
  log(`${p.name} arriva su ${t.revealed || t.type === 'start' ? TILE[t.type].n.toLowerCase() : 'una casella inesplorata'}.`);
  const o = others2(p).filter(x => hexDist(p.pos, x.pos) <= 1).sort((a, b) => hexDist(p.pos, a.pos) - hexDist(p.pos, b.pos))[0];
  if (o) {
    log(`${p.name} e ${o.name} sono vicini: combattimento PvP!`, 'turn');
    await scontro(p, o, 'pvp');
    if (G.over || p.defeated) return;
  }
  if (p.defeated) return;
  if (isLocated(p) && same(p.pos, G.treasure)) {
    stageUp('late'); mark('boss');
    const foe = makeCreature(G.beholder ? { ...BEHOLDER, pv: BAL.behPV || BEHOLDER.pv } : { ...BOSS, pv: BAL.bossPV });
    if (G.bossWounds) { foe.pv = Math.max(1, foe.pv - G.bossWounds); log(`${foe.name} porta ancora le ferite degli scontri precedenti (PV ${foe.pv}/${foe.maxpv}).`); }
    log(`${p.name} raggiunge il nascondiglio di MIMI! ${foe.name} lo difende.`, 'gold');
    await scontro(p, foe, 'boss');
    if (!G.over) G.bossWounds = foe.maxpv - Math.max(1, foe.pv);
    return;
  }
  const tl = tileAt(p.pos);
  if (tl.done || tl.type === 'start') return;
  let again = false;
  if (tl.used && BUILDINGS.includes(tl.type)) {
    again = tl.used.includes(p.id);
    if (again && bOnce()) {
      if (tl.type === 'locanda' && p.flags.revived && isC(p, 'Chierico')) { p.flags.revived = false; log(`${p.name} ha già usato questa Locanda, ma il Chierico ricarica la sua resurrezione.`, 'good'); return; }
      log(`${p.name} ha già usato questo edificio.`); return;
    }
    if (!again) tl.used.push(p.id);
  }
  if (tl.q && !tl.revealed) {
    const bag = G.tiles.bag;
    if (!bag.length) { tl.type = 'vuota'; tl.revealed = true; tl.done = true; tl.q = false; log('Il sacchetto è vuoto: la casella resta tranquilla.'); return; }
    tl.type = bag.pop(); log(`${p.name} pesca dal sacchetto: ${TILE[tl.type].n} (ne restano ${bag.length}).`);
  }
  tl.revealed = true; tick('casella');
  switch (tl.type) {
    case 'vuota': log('Niente da segnalare.'); tl.done = true; break;
    case 'creatura': case 'miniboss': await meetCreature(p, tl.type); break;
    case 'evento': if (!tl.used) tl.done = true; await chaosEvent(p); break;
    case 'locanda': { const pe = !(again && BAL.buildings === 'pe-once'); log(pe ? 'Locanda: si guadagna metà livello (1 PE) e si recuperano 2 PV.' : 'Locanda: si recuperano 2 PV (il PE si prende solo la prima volta).', 'good'); if (!tl.used) tl.done = true; p.flags.revived = false; heal(p, 2); if (pe) await addPE(p, 1); break; }
    case 'fonte': log('Fonte: puoi recuperare fino a 2 carte dagli scarti.', 'good'); if (!tl.used) tl.done = true; await recover(p, 2); break;
    case 'fabbro': {
      if (!tl.used) tl.done = true;
      const cand = p.lost.filter(id => p.discard.includes(id) && !equipped(p).includes(id));
      if (!cand.length) { log('Fabbro: nessun equipaggiamento perso da riparare.'); break; }
      const id = await chooseFrom(p, [...new Set(cand)], 'Fabbro: scegli l\'equipaggiamento da riparare');
      p.discard.splice(p.discard.indexOf(id), 1); p.lost.splice(p.lost.indexOf(id), 1);
      log(`Il fabbro ripara ${C(id).nome}.`, 'good'); await equip(p, id); break;
    }
    case 'trappola': {
      tl.done = true; log('Trappola!', 'bad');
      const d = BAL.noD4 ? Math.max(1, await roll(p, 6, 'Danni della trappola (D6 − 1, minimo 1)') - 1) : await roll(p, 4, 'Danni della trappola');
      await hurt(p, d);
      if (p.pv <= 0) { await defeat(p, 'trappola'); break; }
      await lossRoll(p); break;
    }
    case 'indizio': tl.done = true; log('Una mappa strappata con un segno sopra!'); await addClue(p); break;
  }
  // sacchetto: il segnalino risolto torna nella scatola e la casella torna «?» (una creatura non sconfitta resta scoperta)
  if (tl.q && tl.done) { if (G.tiles.bag.length) { tl.type = 'q'; tl.revealed = false; tl.done = false; } else tl.type = 'vuota'; }
}
async function endOfTurn(p, skipped) {
  for (const x of G.players) { x.mods = x.mods.filter(m => m.kind !== 'turn'); x.turnFlags = {}; clamp(x); }
  const exp = [];
  p.mods = p.mods.filter(m => { if (m.kind === 'turni') { m.n--; if (m.n <= 0) { exp.push(m); return false; } } return true; });
  clamp(p);
  for (const m of exp) {
    log(`Finisce l'effetto «${m.label}».`);
    if (m.onExpire === 'drago') loseTurns(p, 10);
    if (m.onExpire === 'angelo') { log(`${p.name} muore e rinasce come Angelo della morte.`, 'gold'); p.pos = await rollSpawn(p, 'respawn'); for (const k of ['att', 'mov', 'ar']) p.base[k] = Math.max(p.base[k], 2); p.pv = maxPV(p); }
  }
  if (p.pv <= 0 && !G.over) await defeat(p);
  if (p.ashafe > 0) { if (skipped) heal(p, 1); p.ashafe--; if (!p.ashafe) log('Ashafe se ne va.'); }
  if (p.tempLocated > 0) p.tempLocated--;
  if (G.swap && G.swap.owner === p.id) { G.swap.left--; if (G.swap.left <= 0) { swapHands(); G.swap = null; log('Gatto Ciclone finisce: mani e scarti tornano ai proprietari.'); } }
  if (p.burattinato === 'active') p.burattinato = null;
  if (p.zarko && !skipped && p.skip === 0 && p.ownTurns > p.zarkoStart) {
    p.zarko--;
    if (p.zarko <= 0) {
      p.out = true; p.zarko = 0; log(`${p.name} non è riuscito a vincere da Zarko ed è eliminato.`, 'bad');
      if (live().length === 1) G.over = { winner: live()[0], why: `${p.name} non è riuscito a vincere da Zarko: ${live()[0].name} resta l'unico in gioco.`, reason: 'zarko' };
    }
  }
}
async function gameLoop() {
  const myGame = G;
  while (!G.over && G === myGame) {
    const p = G.players[G.cur];
    if (p.out) { G.cur = (G.cur + 1) % G.players.length; continue; }
    await playTurn(p);
    if (G !== myGame) return;
    for (const x of G.players) clamp(x);
    if (G.over) break;
    if (p.extra > 0 && p.skip === 0) { p.extra--; log(`${p.name} gioca un turno extra.`, 'good'); }
    else { let n = G.cur; do { n = (n + 1) % G.players.length; } while (G.players[n].out && n !== G.cur); G.cur = n; }
    G.round++;
    if (G.round > 600 * G.players.length / 2) { G.over = { winner: null, why: 'Partita interrotta: troppi turni.', reason: 'limite' }; }
    render();
  }
  render();
}

// ===================== Avvio =====================
const DECK = {};
for (const c of CARDS) if (c.cls) (DECK[c.cls] = DECK[c.cls] || []).push(c.id);
const COMMON = CARDS.filter(c => c.tipo !== 'TC' && !c.cls).map(c => c.id);
function dealList(list) {
  const used = new Set();
  for (const sp of list) {
    sp.deck = [...shuffle([...DECK[sp.cls]]).slice(0, 5), ...shuffle(commonPool().filter(id => !used.has(id))).slice(0, 5)];
    sp.deck.forEach(id => used.add(id));
  }
}
function dealDecks() { dealList(S.players.slice(0, S.n)); }
function newPlayer(i, sp) {
  const R = RACES[sp.race];
  const base = { pv: 10 + (sp.cls === 'Guerriero' ? BAL.guerPV : 0) + ((BAL.clsPV || {})[sp.cls] || 0), att: 1, mov: 1 + (sp.cls === 'Ladro' ? BAL.ladroMov : 0) + (BAL.clsMov[sp.cls] || 0), ar: 1 };
  for (const k in R.fixed) base[k] += R.fixed[k];
  for (let j = 0; j < R.free; j++) base[sp.free[j] || 'att']++;
  return {
    id: i, name: sp.name.trim() || `Giocatore ${i + 1}`, ai: sp.ai, race: sp.race, base, pv: base.pv, level: 1, pe: 0, clues: 0, located: false, tempLocated: 0, insp: false,
    hand: [...sp.deck], discard: [], equip: { elmo: null, dx: null, sx: null, armatura: null, accessorio: null }, lost: [], classes: [], classCards: [],
    pos: { c: -9, r: -9 }, prev: { c: -9, r: -9 }, turnStart: { c: -9, r: -9 }, skip: 0, extra: 0, servants: [], mods: [], flags: {}, turnFlags: {},
    played: 0, limit: 2, magoRerolls: 0, palHeals: 0, destino: 0, ashafe: 0, ownTurns: 0, diss: 0, startCls: sp.cls, out: false,
  };
}
// Plancia della scatola (thread del gioco fisico): coordinate (col,riga), simmetria a mezzo giro
const PHYS = {
  locanda: [[1, 4], [8, 5]], fonte: [[4, 1], [5, 8]], fabbro: [[8, 1], [1, 8]],
  cripta: [[3, 3], [6, 3], [3, 6], [6, 6]],
  evento: [[4, 0], [5, 9], [3, 2], [6, 7], [7, 4], [2, 5], [4, 4], [5, 5], [9, 2], [0, 7]],
  q: [[6, 0], [3, 9], [8, 0], [1, 9], [1, 1], [8, 8], [3, 1], [6, 8], [6, 1], [3, 8], [2, 2], [7, 7], [5, 2], [4, 7], [8, 2], [1, 7], [9, 1], [0, 8], [4, 3], [5, 6], [7, 3], [2, 6], [8, 3], [1, 6], [0, 3], [9, 6], [2, 4], [7, 5], [5, 4], [4, 5]],
  tokens: { creatura: 13, miniboss: 4, trappola: 5, indizio: 4, vuota: 4 },
  tokensBag: { creatura: 13, miniboss: 4, trappola: 5, vuota: 8 },
};
const physBoard = () => BAL.board === 'fisica' && COLS === 10 && ROWS === 10 && SPAWNS.length === 6;
const bOnce = () => (BAL.buildings || 'once') === 'once';
const BUILDINGS = ['locanda', 'fonte', 'fabbro'];
function newBoard() {
  if (physBoard()) {
    const tiles = [];
    for (let r = 0; r < ROWS; r++) { tiles.push([]); for (let c = 0; c < COLS; c++) tiles[r].push({ type: 'vuota', revealed: true, done: true }); }
    SPAWNS.forEach((h, i) => { tiles[h.r][h.c] = { type: 'start', revealed: true, done: true, spawn: i + 1 }; });
    for (const k of [...BUILDINGS, ...(BAL.caos ? ['evento'] : [])]) for (const [c, r] of PHYS[k]) tiles[r][c] = { type: k, revealed: true, done: false, used: [] };
    PHYS.cripta.forEach(([c, r], i) => { tiles[r][c] = { type: 'cripta', revealed: true, done: true, crypt: i + 1 }; });
    const bag = shuffle(Object.entries(BAL.bagDraw ? PHYS.tokensBag : PHYS.tokens).flatMap(([k, n]) => Array(n).fill(k)));
    if (BAL.bagDraw) { tiles.bag = bag; PHYS.q.forEach(([c, r]) => { tiles[r][c] = { type: 'q', revealed: false, done: false, q: true }; }); }
    else PHYS.q.forEach(([c, r], i) => { tiles[r][c] = { type: bag[i], revealed: false, done: false }; });
    return tiles;
  }
  const tiles = [];
  for (let r = 0; r < ROWS; r++) { tiles.push([]); for (let c = 0; c < COLS; c++) tiles[r].push({ type: 'vuota', revealed: false, done: false }); }
  SPAWNS.forEach((h, i) => { tiles[h.r][h.c] = { type: 'start', revealed: true, done: true, spawn: i + 1 }; });
  const bag = [];
  // proporzioni della plancia standard 10×10 (90 caselle libere), scalate sulla plancia in uso
  const nFree = COLS * ROWS - SPAWNS.length;
  const base = { creatura: 26, miniboss: 6, locanda: 6, fonte: 6, fabbro: 4, trappola: 10, indizio: 6, evento: 0 };
  Object.assign(base, BAL.tiles);
  if (!BAL.caos) delete base.evento;
  const counts = {}; for (const k in base) counts[k] = Math.max(1, Math.round(base[k] * nFree / 90));
  for (const k in counts) for (let i = 0; i < counts[k]; i++) bag.push(k);
  const free = shuffle(allHexes().filter(h => tiles[h.r][h.c].type !== 'start'));
  free.forEach((h, i) => { if (bag[i]) tiles[h.r][h.c].type = bag[i]; });
  // i mini-boss lontano dalle partenze
  return tiles;
}
async function initClasses() {
  const myGame = G;
  for (const p of G.players) {
    p.pos = await rollSpawn(p, 'start'); p.prev = { ...p.pos }; p.turnStart = { ...p.pos };
    if (G !== myGame) return new Promise(() => {});
    render();
  }
  for (const p of G.players) {
    const tc = CLASS_CARD[p.startCls];
    log(`${p.name} gioca la sua carta classe «${C(tc).nome}».`, 'play');
    await DEF[tc].fx(p, opp(p), tc);
    if (G !== myGame) return new Promise(() => {});
  }
  // equipaggiamento iniziale: tutti insieme prima del primo turno, non conta come carta del turno
  if (BAL.setupEquip) for (const p of G.players) {
    const gear = p.hand.filter(id => isGear(id) && canPlay(p, id, { free: true }) === true);
    if (!gear.length) continue;
    const ch = await ask(p, 'Equipaggiamento iniziale: puoi indossare subito un oggetto dalla mano', [...gear.map(id => ({ label: C(id).nome, value: id })), { label: 'Nessuno', value: 'no' }], { ai: () => gear.slice().sort((a, b) => aiEquipScore(p, b) - aiEquipScore(p, a))[0] });
    if (G !== myGame) return new Promise(() => {});
    if (ch !== 'no') { G.setup = true; try { await playCard(p, ch, { free: true, immediate: true }); } finally { G.setup = false; } p.eqTurn = false; }
  }
  render();
}
function createGame(list, fast = false, rules = RULES_STD) {
  SLOTN = BAL.slots3 ? SLOTN_3 : SLOTN_5;
  applyRules(rules);
  G = { stage: 'early', time: { tot: 0, early: 0, mid: 0, late: 0, at: {}, n: { early: {}, mid: {}, late: {} }, m: {} }, players: [], cur: 0, tiles: newBoard(), map: null, treasure: null, log: [], combat: null, phase: 'inizio', stop: 0, copy: 0, round: 0, beholder: false, bossWounds: 0, swap: null, over: null, reach: null, thinking: '', revealedFor: null, fast, rules };
  G.players = list.map((sp, i) => newPlayer(i, sp));
  G.stats = { played: G.players.map(() => []) };
  const minD = Math.max(2, Math.round(COLS * 0.3));
  let cand = allHexes().filter(h => tileAt(h).type !== 'start' && SPAWNS.every(s => hexDist(h, s) >= minD));
  if (!cand.length) cand = allHexes().filter(h => tileAt(h).type !== 'start' && SPAWNS.every(s => hexDist(h, s) >= 2));
  G.treasure = physBoard() ? (([c, r]) => ({ c, r }))(pick(PHYS.cripta)) : pick(cand);
  G.cur = Math.floor(Math.random() * G.players.length); G.first = G.cur;
  log(`Inizia la partita. Comincia ${G.players[G.cur].name}.`, 'turn');
}
function startGame() {
  pending = null; GEN++;
  createGame(S.players.slice(0, S.n));
  view = 'game';
  render();
  initClasses().then(gameLoop).catch(e => { console.error(e); log('Errore: ' + e.message, 'bad'); render(); });
}
