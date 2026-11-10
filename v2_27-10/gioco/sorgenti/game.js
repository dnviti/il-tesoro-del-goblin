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
  Sanguar: { tag: 'Sanguar', fixed: { mov: 2 }, free: 0, info: '+2 MOV. Specie di non morti' },
  Nani: { tag: 'Nano', fixed: {}, free: 2, info: '+1 a due statistiche a scelta' },
  Yumaniani: { tag: 'Aasimar', fixed: { ar: 1 }, free: 1, info: '+1 AR e +1 a una statistica a scelta. Valgono come Aasimar per le carte' },
  Orchi: { tag: 'Orco', fixed: { att: 2 }, free: 0, info: '+2 ATT' },
  Elfi: { tag: 'Elfo', fixed: {}, free: 2, info: '+2 a statistiche a scelta' },
  Halfling: { tag: 'Halfling', fixed: { mov: 1, ar: 1 }, free: 0, info: 'Specie aggiunta (citata dalle carte): +1 MOV e +1 AR' },
  Tiefling: { tag: 'Tiefling', fixed: { att: 1 }, free: 1, info: 'Specie aggiunta (citata dalle carte): +1 ATT e +1 a scelta' },
};
const STATN = { pv: 'PV', att: 'ATT', mov: 'MOV', ar: 'AR' };
// Scatola base v2 (Carte Trama v2 di Alessandro De Simone, 27/10/2026): 4 classi, Oracolo al posto del Chierico
const CLASSES = ['Guerriero', 'Ladro', 'Mago', 'Oracolo'];
const CLASS_CARD = { Guerriero: 'TC-01', Ladro: 'TC-02', Mago: 'TC-03', Oracolo: 'TC-04' };
// 4 slot della scheda: Elmo, Arma DX / Scudo, Arma SX, Armatura
const SLOT = {};
['TE-01', 'TE-02', 'TE-03', 'TE-04'].forEach(i => SLOT[i] = 'elmo');
['TE-05', 'TE-06', 'TE-07', 'TE-08', 'TE-09', 'TE-10', 'TE-11', 'TE-12'].forEach(i => SLOT[i] = 'dx');
['TE-13', 'TE-14', 'TE-15'].forEach(i => SLOT[i] = 'sx');
['TE-16', 'TE-17', 'TE-18', 'TE-19', 'TE-20'].forEach(i => SLOT[i] = 'armatura');
SLOT['CA-04'] = 'elmo';
const SHIELDS = ['TE-05', 'TE-06', 'TE-07', 'TE-08', 'TE-09'];
const POTIONS = [];
const SLOTN_5 = { elmo: 'Elmo', dx: 'Arma DX / Scudo', sx: 'Arma SX', armatura: 'Armatura' };
const SLOTN_3 = SLOTN_5;
let SLOTN = SLOTN_5;
const SLOT_LABEL = { elmo: 'Elmo', dx: 'Arma DX / Scudo', sx: 'Arma SX', armatura: 'Armatura' };

// Carte Nemico a livelli (Daniele, 27/10): mazzetto I = LV 1-2, mazzetto II = LV 3-4 (+ mini-boss LV 4,5 facoltativi), boss LV 5.
// Danno dal livello (LV 1 → D6 − 1, LV 2 → D6, LV 3 e oltre → D6 + 1); tiro per colpire D20 + ATT ≥ Difesa = 14 + AR (Daniele 27/10: colpire è il 20% più difficile, +4); ogni nemico ha un effetto (fx)
const HIT_DIE = () => BAL.hitDie || 20;
const DIFESA = x => (BAL.defBase ?? 14) + x;
const DMG_LV = lv => BAL.dmgLv[Math.min(Math.ceil(lv), BAL.dmgLv.length) - 1];
const NEMICI = (typeof NEMICI_JSON !== 'undefined' ? NEMICI_JSON : []).map(n => ({ id: n.id, name: n.nome, lv: n.lv, pv: n.pv, att: n.att, ar: n.ar, tipo: n.tipo, fx: n.fx, abil: n.abilita, nonMorto: /Non morto/.test(n.abilita), agguato: n.fx === 'agguato', borseggio: n.fx === 'borseggio' }));
const BESTIARIO = NEMICI.filter(n => n.tipo === 'Nemico I');
const MAZZO_II = NEMICI.filter(n => n.tipo === 'Nemico II');
const MINIBOSS = NEMICI.filter(n => n.tipo === 'Mini-boss');
const BOSSES = NEMICI.filter(n => n.tipo === 'Boss');
const BOSS = BOSSES[0] || { name: 'Guardiano di MIMI', lv: 5, pv: 14, att: 4, ar: 3 };
const BEHOLDER = { name: 'Beholder', lv: 4, pv: 15, att: 3, ar: 2, beholder: true };

const TILE = {
  start: { n: 'Punto di spawn', g: '' },
  vuota: { n: 'Sentiero tranquillo', g: '' },
  q: { n: 'Segnalino Esplorazione', g: '?' },
  creatura: { n: 'Mostro', g: '⚔' },
  imprevisto: { n: 'Imprevisto', g: '!' },
  miniboss: { n: 'Nemico II', g: '♛' },
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
const BAL = {
  // regole della scatola (confermate il 21/10) che restano
  caos: false, board: 'fisica', buildings: 'once', bagDraw: true, slots3: false, chierRev: 3, clsPV: {}, clsMov: {}, creatureFixed: true, locCatch: true, skipCapFoe: 3, skipCap: 99, setupEquip: true, noD4: true,
  magoPerTurn: true, magoRerolls: 2, ladroAdv: false, ladroMov: 2, chierico: 'locanda', guerInsp: true, guerAR: 2, guerPV: 2, hitDie: 20, defBase: 14, gearStart: true, basePV: 5, lvPV: 2, aiPVmin: 9, pvpFlee: 1.2, pvpLevel: false, defeatPE: 0,
  tiles: { evento: 10 }, bossPV: 14, behPV: 12, clock: 0, clockEvery: 2, pity: 0, maxMoves: 2, omen: 0, servPvP: true, servDmg: 1, impDmg: 3, allOpp: false, foesOff: [], furyAtt: 0, furyDmg: 0, furyMov: 0,
  // v2: combattimento in due tiri e carte nuove
  heroDmg: [6, 0],              // danno degli eroi: D6 (+ bonus delle carte)
  dmgLv: [[4, 0], [6, 0], [6, 1], [6, 1], [6, 1]], // danno dei nemici per livello: D6−1, D6, poi D6+1
  handCls: 3,                   // modalità draft: Classe + 3 carte della tua classe scelte + 7 comuni draftate
  handClsRnd: 5,                // modalità casuale (Daniele, 27/10): Classe + 5 carte di classe a caso + 5 comuni a caso
  handTot: 10,
  handMode: 'random',            // i giocatori scelgono: 'random' = pescata casuale, 'draft' = carte di classe scelte e comuni draftate (Daniele, 27/10)
  draftNoise: 0.04,             // l'IA non sceglie sempre la stessa carta
  moveKeepClues: true,          // quando il tesoro cambia Cripta gli Indizi restano
  trapDmg: 'd6-1',
  // ritmo v2 (27/10): senza le vecchie carte Indizio servono altre fonti di Indizi
  // Indizi solo vincendo uno scontro su una casella esplorazione (Daniele, 27/10): niente Indizio iniziale, niente Mappe strappate, niente Presagio
  startClues: 0,
  bag: { creatura: 19, miniboss: 6, trappola: 5, indizio: 0, vuota: 0 }, // «?»: Nemico I (mazzetto LV 1-2), Nemico II (mazzetto LV 3-4), Trappole
  miniBoss: false,              // regola facoltativa: i mini-boss LV 4,5 si mescolano nel mazzetto II
  bossDeck: true,               // il boss si pesca a caso tra i 3 boss LV 5
  cluesNeed: 2,                 // 2 Indizi per individuare il tesoro (scelta di Daniele, 27/10)
  mbClues: 1,
  bldBag: true,                 // Locanda, Fonte e Fabbro sono segnalini del sacchetto (Daniele, 2/11), non edifici stampati
  bldTok: { locanda: 2, fonte: 2, fabbro: 2 },
  colorBag: true,               // sacchetto a due colori (Daniele, 2/11): rosse = Mostro, blu = Imprevisto
  bagColor: { creatura: 25, imprevisto: 11 },
  impDeck: { trappola: 5, locanda: 2, fonte: 2, fabbro: 2 }, // mazzetto Imprevisti: la carta girata va in fondo
  monLv: true,                  // il Mostro viene dal mazzetto del livello dell'eroe: LV 1-2 → 1, LV 3-4 → 2, LV 5+ → 3
};
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
const FOES = new Set([]); const _OLDFOES = (['TE-14', 'TE-18', 'TI-10', 'TI-12', 'TI-16', 'TI-28', 'TI-37', 'TI-22', 'TI-39']);
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
    { name: 'Geronimo (IA)', ai: true, race: 'Orchi', cls: 'Ladro', free: ['att', 'att'], deck: [] },
    { name: 'Mimì (IA)', ai: true, race: 'Elfi', cls: 'Oracolo', free: ['att', 'ar'], deck: [] },
    { name: 'Gnomo (IA)', ai: true, race: 'Nani', cls: 'Mago', free: ['ar', 'mov'], deck: [] },
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
const TARG = new Set([]); const _OLDTARG = (['TE-08', 'TE-14', 'TE-18', 'TI-04', 'TI-10', 'TI-11', 'TI-12', 'TI-14', 'TI-16', 'TI-21', 'TI-22', 'TI-24', 'TI-25', 'TI-26', 'TI-28', 'TI-29', 'TI-30', 'TI-35', 'TI-37', 'TI-41', 'TI-45']);
const TARG_LOCATED = new Set([]);
const isR = (p, ...t) => t.includes(RACES[p.race].tag);
const isC = (p, ...c) => c.some(x => p.classes.includes(x));
const equipped = p => [...new Set(Object.values(p.equip).filter(Boolean))];
const weapons = p => equipped(p).filter(id => SLOT[baseId(id)] === 'dx' && !SHIELDS.includes(baseId(id)));
const has = (p, bid) => equipped(p).some(id => baseId(id) === bid);
const same = (a, b) => a.c === b.c && a.r === b.r;
// Yuma (Paradiso): gli incantesimi di danno e di cura danno +1
const sb = p => (G && G.map && G.map.id === 'TM-07') ? 1 : 0;

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
      case 'TE-01': b.ar += 1; break;
      case 'TE-04': b.ar += 1; break;
      case 'TE-05': b.ar += 2; b.mov -= 1; break;
      case 'TE-06': case 'TE-07': case 'TE-08': case 'TE-09': b.ar += 1; break;
      case 'TE-10': case 'TE-11': case 'TE-12': b.att += 1; break;
      case 'TE-16': b.ar += 1; break;
      case 'TE-17': b.ar += 2; b.mov -= 1; break;
      case 'TE-18': b.mov += 1; break;
      case 'TE-19': case 'TE-20': b.ar += 1; break;
      case 'CA-04': b.ar += 1; if (isC(p, 'Oracolo')) b.att++; break;
    }
  }
  return b;
}
// Mappe v2: il tabellone cambia (una sola Mappa attiva); Miraggio del Tesoro sposta solo il tesoro
function mapBonus(p, mapId = G.map && G.map.id) {
  const b = { att: 0, mov: 0, ar: 0, pv: 0, adv: 0, dis: 0 };
  switch (mapId) {
    case 'TM-02': b.mov += 2; break;
    case 'TM-03': b.mov -= 1; if (isR(p, 'Elfo')) b.adv++; break;
    case 'TM-04': b.mov -= 1; break;
    case 'TM-05': b.mov -= 1; if (isR(p, 'Sanguar')) b.adv++; break;
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
// ritiri: Mago (1 a turno), Bastone del Corvo (un D6 a turno), Diadema (un D6 di incantesimo a turno),
// Ispirazione, Fortuna del Furfante (solo tiro per colpire, si scarta), Sguardo dell'Oracolo (carta)
const handHas = (p, bid) => p.hand.find(id => baseId(id) === bid);
function rerollOpts(p, sides = 20, kind = '') {
  const o = [];
  if (p.magoRerolls > 0) o.push({ label: `Ritira (Mago, ${p.magoRerolls} rimasti)`, value: 'mago' });
  if (sides === 6 && has(p, 'TE-11') && !p.turnFlags.corvo) o.push({ label: 'Ritira il D6 (Bastone del Corvo)', value: 'corvo' });
  if (sides === 6 && kind === 'spell' && has(p, 'TE-04') && !p.turnFlags.diadema) o.push({ label: 'Ritira il D6 (Diadema della Veggenza)', value: 'diadema' });
  if (p.insp) o.push({ label: 'Ritira con Ispirazione', value: 'insp' });
  if (kind === 'hit' && handHas(p, 'TI-38')) o.push({ label: 'Scarta Fortuna del Furfante e ritira', value: 'fortuna' });
  if (handHas(p, 'TI-33') && canPlay(p, handHas(p, 'TI-33'), { react: true }) === true) o.push({ label: "Gioca Sguardo dell'Oracolo e ritira", value: 'sguardo' });
  return o;
}
// IA: non sprecare i ritiri sul movimento; il Guerriero tiene l'Ispirazione per il −2 AR
function aiReroll(p, label, opts, kind) {
  if (kind === 'move' || label === 'Movimento' || label.startsWith('Punto di')) return 'keep';
  const o = opts.filter(x => !(x.value === 'insp' && isC(p, 'Guerriero')) && !(x.value === 'sguardo' && kind !== 'hit'));
  return o.length ? o[0].value : 'keep';
}
async function spendReroll(p, v) {
  if (v === 'insp') p.insp = false; else if (v === 'mago') p.magoRerolls--; else if (v === 'corvo') p.turnFlags.corvo = true; else if (v === 'diadema') p.turnFlags.diadema = true;
  else if (v === 'fortuna') { const id = handHas(p, 'TI-38'); p.hand.splice(p.hand.indexOf(id), 1); p.discard.push(id); if (G.stats) G.stats.played[p.id].push('TI-38'); log(`${p.name} scarta Fortuna del Furfante.`, 'play'); }
  else if (v === 'sguardo') { const id = handHas(p, 'TI-33'); await playCard(p, id, { react: true }); }
}
async function roll(p, sides, label, { bad = null, adv = 0, uni = false, kind = '', notick = false } = {}) {
  if (!notick) tick('dado'); let v = rollRaw(sides, adv, uni);
  log(`${p ? p.name + ' · ' : ''}${label}: D${sides}${adv > 0 ? ' con vantaggio' : adv < 0 ? ' con svantaggio' : ''} → ${v}`, 'dice');
  showDie(sides, v);
  while (p && !p.isCreature && bad && bad(v)) {
    const opts = rerollOpts(p, sides, kind); if (!opts.length) break;
    const ch = await ask(p, `${label}: è uscito ${v}`, [{ label: 'Tieni il risultato', value: 'keep' }, ...opts], { ai: () => aiReroll(p, label, opts, kind) });
    if (ch === 'keep') break;
    await spendReroll(p, ch); tick('dado'); v = rollRaw(sides, adv, uni);
    log(`${p.name} ritira: ${label} → ${v}`, 'dice'); showDie(sides, v);
  }
  return v;
}
// dado di un incantesimo (D6 o D6 − 1) con i bonus di Yuma, Flusso di volontà, Libro di Rune / Simbolo Sacro
async function spellDie(p, label, minus = 0) {
  const v = await roll(p, 6, label, { bad: x => x <= 2, kind: 'spell', notick: true });
  return { v, n: Math.max(1, v - minus) };
}
function spellDmgBonus(p) {
  let b = sb(p);
  if (p.flags.flusso) { b += p.flags.flusso; p.flags.flusso = 0; log('Flusso di volontà: +1 Danno.'); }
  if (has(p, 'TE-13') && !p.turnFlags.libro) { p.turnFlags.libro = true; b += 1; log('Libro di Rune: +1 Danno.'); }
  return b;
}
const spellHealBonus = p => sb(p) + (has(p, 'TE-14') ? 1 : 0);
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
  if (BAL.locCatch && !G.catching) { G.catching = true; log('La voce si sparge: ogni altro eroe ottiene un indizio.', 'gold'); for (const x of others2(p)) if (!x.located) { x.clues++; if (x.clues >= (BAL.cluesNeed || 3)) { x.located = true; log(`${x.name} individua il tesoro!`, 'gold'); } } G.catching = false; }
}
async function addClue(p, n = 1) {
  for (let i = 0; i < n && !p.located; i++) {
    p.clues++; p.dry = 0; stageUp('mid'); mark('clue' + p.clues); log(`${p.name} ottiene un indizio (${p.clues}/${BAL.cluesNeed || 3}).`, 'gold');
    if (p.clues >= (BAL.cluesNeed || 3)) locate(p);
  }
}
function moveTreasure() {
  // MIMI va sulla plancia solo quando qualcuno individua il tesoro: prima la Mappa non sposta niente
  if (BAL.moveKeepClues && !G.players.some(p => p.located)) { log('MIMI non è ancora sulla plancia: il tesoro resta nascosto.'); return; }
  const cand = physBoard() ? PHYS.cripta.map(([c, r]) => ({ c, r })).filter(h => !same(h, G.treasure)) : allHexes().filter(h => tileAt(h).type !== 'start' && !same(h, G.treasure) && G.players.every(p => hexDist(h, p.pos) >= 2));
  G.treasure = pick(cand); G.moves = (G.moves || 0) + 1;
  if (BAL.moveKeepClues) { log('Il tesoro cambia Cripta! Gli Indizi restano: chi ne ha 3 sa già dove andare.', 'gold'); return; }
  log('Il tesoro cambia posizione! Chi l\'aveva individuato deve trovare un altro indizio.', 'gold');
  for (const p of G.players) { if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0; }
}
async function addPE(p, n) {
  p.pe += n; log(`${p.name} guadagna ${n} PE.`);
  const k = BAL.pePerLv || 2; while (p.pe >= k) { p.pe -= k; await levelUp(p); }
}
async function levelUp(p) {
  if (p.level >= 5) { log(`${p.name} è già al livello massimo.`); return; }
  tick('livello'); mark('lvl' + (p.level + 1)); p.level++;
  log(`${p.name} sale al livello ${p.level}!`, 'good');
  const lvPV = BAL.lvPV || 2;
  const k = await ask(p, `Livello ${p.level}: +1 a una statistica oppure +${lvPV} PV`, ['att', 'mov', 'ar', 'pv'].map(s => ({ label: s === 'pv' ? `+${lvPV} PV (ora ${maxPV(p)})` : `+1 ${STATN[s]} (ora ${stat(p, s)})`, value: s })), { ai: () => (maxPV(p) < (BAL.aiPVmin || 9) ? 'pv' : (p.level % 2 ? 'att' : 'ar')) });
  if (k === 'pv') { p.base.pv += lvPV; p.pv += lvPV; } else p.base[k]++;
  log(`${p.name} aumenta ${k === 'pv' ? 'i PV di ' + lvPV : STATN[k]}.`);
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
  const slots = [SLOT[baseId(id)]];
  const before = maxPV(p);
  for (const k of slots) if (p.equip[k]) { log(`${C(p.equip[k]).nome} torna nella pila degli scarti.`); unequip(p, p.equip[k]); }
  for (const k of slots) p.equip[k] = id;
  const after = maxPV(p); if (after > before) p.pv += after - before;
  log(`${p.name} equipaggia ${C(id).nome}.`);
}
function slots3Of(s) { return s; }
function loseSlot(p, s) {
  const id = p.equip[s]; if (!id) return;
  unequip(p, id); p.lost.push(id);
  log(`${p.name} perde ${C(id).nome}.`, 'bad');
}
// D6: 1 tutto · 2 Elmo · 3 Arma DX · 4 Arma SX · 5 Armatura · 6 niente
async function lossRoll(p) {
  if (!equipped(p).length) { log(`${p.name} non ha equipaggiamento da perdere.`); return; }
  let v = await roll(p, 6, 'Perdita di equipaggiamento', { bad: v => v < 5 });
  if (v === 3 && has(p, 'TE-09')) { log('Scudo del Goblin: si ritira il D6.'); v = await roll(p, 6, 'Perdita di equipaggiamento (Scudo del Goblin)'); }
  const map = { 2: 'elmo', 3: 'dx', 4: 'sx', 5: 'armatura' };
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
  if (cls === 'Mago') p.magoRerolls = BAL.magoRerolls;
  if (cls === 'Paladino') p.palHeals = BAL.palPerTurn ? 1 : BAL.palHeals;
  if (cls === 'Bardo') p.pv += 1;
}
async function setMap(p, id) {
  if (movesLeft()) moveTreasure(); else log(`Il tesoro si è già spostato ${BAL.maxMoves} volte: resta dov'è.`);
  if (id === 'TM-01') return; // Miraggio del Tesoro: niente terreno
  if (G.map) { G.players[G.map.owner].discard.push(G.map.id); log(`La mappa «${C(G.map.id).nome}» lascia il posto alla nuova.`); }
  G.map = { id, owner: p.id };
  log(`Il tabellone diventa «${C(id).nome}».`, 'gold');
  if (id === 'TM-06') { for (const x of live()) await recover(x, x === p ? 2 : 1, { except: id }); }
  if (id === 'TM-07') { for (const x of live()) if (isC(x, 'Oracolo')) await recover(x, 1, { except: id }); }
}
// ===================== Scontri =====================
const key = x => x.isCreature ? 'F' : 'P' + x.id;
const cmod = (c, x, k) => (c && c.mods[key(x)] && c.mods[key(x)][k]) || 0;
function addCmod(c, x, k, v) { const kk = key(x); c.mods[kk] = c.mods[kk] || {}; c.mods[kk][k] = (c.mods[kk][k] || 0) + v; }
const fury = x => !x.isCreature && BAL.furyAtt + BAL.furyDmg > 0 && isC(x, 'Barbaro') && x.pv <= maxPV(x) / 2;
const atkOf = (x, c) => (x.isCreature ? x.att : stat(x, 'att') + (fury(x) ? BAL.furyAtt : 0)) + cmod(c, x, 'att');
const arOf = (x, c) => (x.isCreature ? x.ar : stat(x, 'ar') + (c && c.foe && c.foe.isCreature && (c.foe.lv || 0) >= 3 && has(x, 'TE-19') ? 2 : 0)) + cmod(c, x, 'ar');
// Combattimento in due tiri: 1) per colpire D20 + ATT ≥ 14 + AR (20 naturale = critico, 1 naturale = mancato); 2) danno: eroi D6 (+ bonus), nemici dal livello
function dmgDice(x) {
  if (x.isCreature) return x.dmg || DMG_LV(x.lv || 1);
  return BAL.heroDmg;
}
const dmgLabel = x => { const [s, b] = dmgDice(x); return `${s === 4 && BAL.noD4 ? 'D6−1' : 'D' + s}${b ? '+' + b : ''}`; };
const dead = x => x.pv <= 0;
function foeOf(p) { const c = G.combat; if (!c) return null; return c.p === p ? c.foe : (c.foe === p ? c.p : null); }
function makeCreature(def, lvl = 1) { const t = (BAL.nemD || {})[def.tipo] || {}; const pv = Math.max(1, def.pv + (t.pv || 0)); return { ...def, isCreature: true, pv, maxpv: pv, att: def.att + (t.att || 0), dmg: DMG_LV(def.lv || 1) }; }
const half = x => x.pv <= x.maxpv / 2;
// un nemico che non lascia fuggire (Ragnatela, Vischio)
const noFlee = f => f && (f.fx === 'ragnatela' || f.fx === 'vischio');
const isUndead = x => x.isCreature ? !!x.nonMorto : isR(x, 'Sanguar');
// carte che si giocano in risposta (fuori dal limite di 2 solo se lo dice la carta)
async function reactCard(p, bid, why) {
  const id = handHas(p, bid); if (!id || p.isCreature) return false;
  if (canPlay(p, id, { react: true }) !== true) return false;
  const ok = await ask(p, `${why}: giochi «${C(id).nome}»?`, [{ label: 'Sì', value: 'y' }, { label: 'No', value: 'n' }], { ai: () => 'y' });
  if (ok !== 'y') return false;
  return await playCard(p, id, { react: true });
}

async function hurt(t, n, c = null, src = null) {
  if (n <= 0) return 0;
  if (t.isCreature) {
    if (t.fx === 'coriaceo' && n > 1) { n -= 1; log(`${t.name} è coriaceo: 1 danno in meno.`); }
    t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${t.maxpv}).`);
    if (t.pv <= 0 && t.fx === 'ricompone' && !t.reformed) { t.reformed = true; t.pv = 2; log(`${t.name} si ricompone: torna a 2 PV!`, 'bad'); }
    return n;
  }
  if (t.flags.giuramento) { const r = Math.min(n, t.flags.giuramento); t.flags.giuramento = 0; n -= r; log(`Giuramento di Ferro: ${r} danni in meno.`, 'good'); if (n <= 0) return 0; }
  if (src) {
    const big = n >= 3 || n >= t.pv;
    if (has(t, 'TE-08') && !t.flags.targa && big) { t.flags.targa = true; log('Targa del Custode: il colpo non fa danni (una volta per partita).', 'good'); return 0; }
    if (big && handHas(t, 'TI-30') && await reactCard(t, 'TI-30', `${src.name} ti colpisce per ${n}`)) { log('Parata perfetta: nessun danno.', 'good'); return 0; }
    if (!src.isCreature && t.flags.riflesso) { log(`Riflesso Speculare: ${src.name} subisce 1 danno.`); src.pv -= 1; }
  }
  if (c && t.flags.patto && t.servants.length) {
    const s = t.servants[0]; s.pv -= n; log(`${s.name} subisce ${n} danni al posto di ${t.name}.`);
    if (s.pv <= 0) { t.servants.shift(); log(`${s.name} è distrutto.`, 'bad'); }
    return n;
  }
  t.pv -= n; log(`${t.name} subisce ${n} danni (PV ${Math.max(0, t.pv)}/${maxPV(t)}).`, 'bad');
  if (c && c.foe && c.foe.borseggio && t === c.p && !c.stole && t.hand.length) { c.stole = true; log(`${c.foe.name} ti ruba una carta: ne scarti una a caso.`, 'bad'); randomDiscard(t, 1); }
  if (t.pv <= 0 && c && isC(t, 'Oracolo') && !c.chierico[t.id] && (BAL.chierico === 'scontro' || (BAL.chierico === 'boss' && c.kind === 'boss') || (BAL.chierico === 'locanda' && !t.flags.revived))) { c.chierico[t.id] = true; t.flags.revived = true; t.pv = BAL.chierRev || 1; log(`Oracolo: torna in vita con ${t.pv} PV!`, 'good'); }
  return n;
}

async function attack(a, d, c) {
  if (c.petrified[key(a)]) { c.petrified[key(a)] = false; log(`${a.name} è pietrificato e salta l'attacco.`); return; }
  let adv = advOf(a, c);
  if (a.isCreature && c.confuse) { c.confuse = false; adv = adv > 0 ? 0 : -1; log('Parola di Confusione: la creatura tira con svantaggio.'); }
  if (!a.isCreature && d.isCreature && d.fx === 'illusione' && !c.illu) { c.illu = true; adv = adv > 0 ? 0 : -1; log(`${d.name}: il tuo primo tiro per colpire ha svantaggio.`, 'bad'); }
  let bonus = atkOf(a, c);
  if (a.isCreature) {
    if (a.fx === 'rigenera' && a.pv < a.maxpv) { a.pv++; log(`${a.name} si rigenera: PV ${a.pv}/${a.maxpv}.`); }
    if (a.fx === 'furia' && half(a)) bonus += 2;
    if (a.fx === 'codardo' && half(a)) bonus -= 2;
  }
  if (!a.isCreature) {
    if (a.flags.nextHit) { bonus += a.flags.nextHit; log(`+${a.flags.nextHit} al tiro per colpire.`); a.flags.nextHit = 0; }
    if (has(a, 'TE-02') && d.isCreature) bonus += 1;
    if (has(a, 'TE-15') && c.p === a && !c.foeFirst) bonus += 1;
  }
  const need = DIFESA(arOf(d, c)) - (a.isCreature && a.fx === 'acido' ? 1 : 0), HD = HIT_DIE();
  const hit = v => v === HD || (v !== 1 && v + bonus >= need);
  const v = await roll(a.isCreature ? null : a, HD, `${a.name} attacca ${d.name} (serve ${need}, ATT ${fmt(bonus)})`, { adv, bad: v => !hit(v), kind: 'hit' });
  tick('attacco'); c.attacks = (c.attacks || 0) + 1;
  const first = !a.isCreature && !a.turnFlags.attacked; if (!a.isCreature) a.turnFlags.attacked = true;
  if (!hit(v)) {
    log(`${a.name} manca il colpo.`);
    if (!d.isCreature && has(d, 'TE-07')) { log(`Scudo Specchiante: ${a.name} subisce 1 danno.`); await hurt(a, 1, c); }
    return;
  }
  // secondo tiro: il danno
  const [s, b] = dmgDice(a);
  let dmg, face = 0;
  if (a.isCreature) {
    face = rnd(6); dmg = (s === 4 && BAL.noD4 ? Math.max(1, face - 1) : s === 4 ? rnd(4) : face) + b;
    if (a.fx === 'carica' && !c.caricaFoe) { c.caricaFoe = true; dmg += 2; log(`${a.name} carica: +2 danni.`, 'bad'); }
  }
  else {
    const x = await roll(a, s, `Danno di ${a.name}`, { bad: x => x <= 2, kind: 'dmg', notick: true });
    dmg = x + b;
    if (a.flags.nextDmg) { dmg += a.flags.nextDmg; log(`+${a.flags.nextDmg} Danni.`); a.flags.nextDmg = 0; }
    if (first && a.turnFlags.carica) { dmg += 1; log('Carica Impetuosa: +1 Danno.'); }
    if (has(a, 'TE-12') && isUndead(d)) dmg += 1;
  }
  if (v === HD) { dmg *= 2; log('Colpo critico! Danni raddoppiati.', 'gold'); }
  const done = await hurt(d, dmg, c, a);
  if (a.isCreature && !d.isCreature) {
    if (done > 0) c.hitBy = true;
    if (a.fx === 'succhia' && done > 0 && a.pv < a.maxpv) { a.pv++; log(`${a.name} succhia il sangue: PV ${a.pv}/${a.maxpv}.`); }
    if (face === 6 && d.pv > 0 && (a.fx === 'rompiscudo')) { log(`${a.name}: colpo devastante, tiro di perdita!`, 'bad'); await lossRoll(d); }
    if (face === 6 && d.pv > 0 && a.fx === 'pietrifica') { log(`${a.name}: lo sguardo ti pietrifica, prendi 1 Clessidra.`, 'bad'); loseTurns(d, 1); }
  }
  if (a.beholder) {
    if (rnd(6) <= 3) { c.petrified[key(d)] = true; log(`${d.name} è pietrificato: salterà il prossimo attacco.`, 'bad'); }
    else { addCmod(c, d, 'att', -2); log(`${d.name} è colto dalla paura: −2 ATT per questo scontro.`, 'bad'); }
  }
}
async function servantAttack(owner, s, foe, c) {
  tick('attacco'); const HD = HIT_DIE(), v = rnd(HD), need = DIFESA(arOf(foe, c));
  if (v === HD || (v !== 1 && v + s.att >= need)) { log(`${s.name} colpisce (${v}${fmt(s.att)}).`); await hurt(foe, s.dmg || BAL.servDmg, c); }
  else log(`${s.name} manca (${v}${fmt(s.att)}).`);
}

function canFlee(x, c) {
  if (noFlee(c.foe) && c.p === x) return false;
  if (c.kind === 'creatura' || c.kind === 'miniboss') return c.p === x;
  return isC(x, 'Ladro');
}
async function combatTurn(x, c, attacker) {
  while (true) {
    if (dead(c.p) || dead(c.foe)) return 'none';
    if (c.velo === x) return 'velo';
    const o = [{ label: `Attacca (D${HIT_DIE()}${fmt(atkOf(x, c))} contro Difesa ${DIFESA(arOf(attacker ? c.foe : c.p, c))}, poi danno ${dmgLabel(x)})`, value: 'attacca' }];
    if (canFlee(x, c)) o.push({ label: 'Fuggi', value: 'fuga' });
    if (isC(x, 'Guerriero') && x.insp) o.push({ label: `Guerriero: usa Ispirazione (−${BAL.guerAR} AR al nemico)`, value: 'guer' });
    const a = await ask(x, attacker ? 'Il tuo round di attacco' : `${c.p.name} ti attacca: il tuo round`, o, { cards: true, ai: () => aiCombat(x, c, o) });
    if (a && a.card) { await playCard(x, a.card); continue; }
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
  if (false && p.flags.assassinio && (kind === 'creatura' || kind === 'miniboss')) { p.flags.assassinio = false; foe.pv = 0; log('Assassinio nelle ombre: la creatura viene eliminata.', 'good'); res = 'win'; }
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
  if (!res && foe.isCreature && (foe.fx === 'gelo' || foe.fx === 'vischio')) { addCmod(c, p, 'att', -1); log(`${foe.name}: hai −1 ATT per tutto lo scontro.`, 'bad'); }
  if (!res && foe.agguato) { c.foeFirst = true; log(`${foe.name}: agguato! Attacca per primo.`, 'bad'); await attack(foe, p, c); if (dead(p)) res = 'lose'; }
  while (!res) {
    c.round++;
    if (c.burn && c.round > 1 && c.foe.isCreature) { log('Fiamma Persistente brucia ancora.'); await hurt(c.foe, c.burn, c); if (dead(foe)) { res = 'win'; break; } }
    const act = await combatTurn(p, c, true);
    if (G.over) return;
    if (act === 'fuga') { if (foe.fx === 'inseguitore') { log(`${foe.name} ti insegue e attacca!`, 'bad'); await attack(foe, p, c); if (dead(p)) { res = 'lose'; break; } } res = 'fuga'; break; }
    if (act === 'velo') { res = 'velo'; break; }
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
      if (a2 === 'fuga' || a2 === 'velo') { res = 'fugaDif'; break; }
      if (dead(foe)) { res = 'win'; break; } if (dead(p)) { res = 'lose'; break; }
      if (a2 === 'attacca') { await attack(foe, p, c); if (c.carica[foe.id] && !dead(p)) { log('Carica eroica: secondo attacco!'); await attack(foe, p, c); } if (BAL.servPvP) for (const s of [...foe.servants]) { if (dead(p)) break; await servantAttack(foe, s, p, c); } }
    } else await attack(foe, p, c);
    if (dead(p)) { res = 'lose'; break; } if (dead(foe)) { res = 'win'; break; }
    render();
  }
  G.combat = null;
  if (res !== 'lose' && c.hitBy && foe.fx === 'veleno' && p.pv > 1) { p.pv--; log(`Morso infetto: ${p.name} perde 1 PV (PV ${p.pv}).`, 'bad'); }
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
    if (foe.cob) { log('I Coboldi non hanno pagine della mappa: peschi una carta.'); drawCard(p); if (foe.borseggio) drawCard(p); } else { const sus = p.flags.sussurro ? 1 : 0; p.flags.sussurro = false; await addClue(p, (kind === 'miniboss' ? (BAL.mbClues || 1) : 1) + sus); }
    if (kind === 'miniboss') { await levelUp(p); giveInsp(p, 'mini-boss'); } else { await addPE(p, 1); if (foe.lv >= 3) giveInsp(p, 'nemico del mazzetto II'); }
    if (BAL.guerInsp && isC(p, 'Guerriero')) giveInsp(p, 'Guerriero vittorioso');
    if (p.turnFlags.specchio) giveInsp(p, 'Specchio dei Tesori');
    if (has(p, 'TE-03') && !p.turnFlags.cappello) { p.turnFlags.cappello = true; log('Cappello del Taumaturgo: riprendi una carta.'); await recover(p, 1); }
    if (ch) {
      if (!c.used[p.id]) { log('Sfida vinta senza usare carte!', 'good'); gainTurns(p, ch.bet); await recover(p, 1, { except: 'TI-49' }); }
      else log('Sfida vinta, ma sono state usate carte: nessun premio extra.');
    }
  } else if (res === 'lose') {
    if (kind === 'pvp') { await pvpReward(foe, p); return; }
    if (foe.fx === 'catene') { log(`${foe.name}: catene, prendi 1 Clessidra.`, 'bad'); loseTurns(p, 1); }
    if (foe.fx === 'saccheggio' && p.hand.length) { log(`${foe.name} ti saccheggia: scarti 1 carta a caso.`, 'bad'); randomDiscard(p, 1); }
    if (ch) { log('Sfida persa: si perdono i turni scommessi.', 'bad'); loseTurns(p, ch.bet); }
    await defeat(p, `da ${foe.name}`, kind === 'boss' && BAL.bossNear);
    if (BAL.defeatPE && kind !== 'boss') { log(`${p.name} impara dalla sconfitta.`); await addPE(p, BAL.defeatPE); }
  } else if (res === 'fuga') {
    log(`${p.name} fugge: nessuna ricompensa.`);
    if (isC(p, 'Ladro') || foe.fx === 'lento') log(isC(p, 'Ladro') ? 'Ladro: fugge senza arretrare.' : `${foe.name} è lento: non arretri.`); else retreat(p, p.turnStart);
  } else if (res === 'velo') {
    log(`${p.name} si dilegua: nessuna ricompensa, ma resta dov'è.`);
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

// ===================== Carte: definizioni (Carte Trama v2) =====================
const others = (p, id) => p.hand.filter(x => x !== id);
const DEF = {};
function tc(cls, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { await setClass(p, cls, id); return 'keep'; }, ai: p => p.classes.length ? 0 : 6 };
}
DEF['TC-01'] = tc('Guerriero', { nota: '+2 PV. Ogni scontro vinto dà Ispirazione. In scontro puoi spenderla per dare −2 AR al nemico.' });
DEF['TC-02'] = tc('Ladro', { nota: '+2 MOV. Puoi fuggire anche dal Duello e dal Guardiano, e fuggendo non arretri.' });
DEF['TC-03'] = tc('Mago', { nota: 'Puoi ritirare i tuoi dadi fino a 2 volte per turno.' });
DEF['TC-04'] = tc('Oracolo', { nota: 'Se scendi a 0 PV in uno scontro torni a 3 PV e continui a combattere. Si ricarica quando peschi una Locanda dal sacchetto.' });

// --- Mappe ---
const nearestCripta = p => Math.min(...PHYS.cripta.map(([c, r]) => hexDist(p.pos, { c, r })));
function aiMapScore(p, o, id) {
  const sum = x => { const b = mapBonus(x, id); return b.mov * 0.4 + b.adv * 1.5; };
  const foesSum = others2(p).reduce((a, x) => a + sum(x), 0) / Math.max(1, others2(p).length);
  // spostare il tesoro conviene se un avversario lo ha individuato e io no (o se sono più lontano)
  const lead = others2(p).some(x => x.located && (!p.located || hexDist(x.pos, G.treasure) < hexDist(p.pos, G.treasure)));
  let s = (lead && movesLeft() ? 5 : 0) - (p.located && !lead && movesLeft() ? 4 : 0) + sum(p) - foesSum;
  if (id === 'TM-06') s += Math.min(2, p.discard.length) * 1.2;
  if (id === 'TM-07') s += (isC(p, 'Oracolo') && p.discard.length ? 1.2 : 0) + 0.5;
  if (id === 'TM-08') s += 0.3;
  if (G.map && G.map.id === id) s -= 3;
  return s;
}
for (const id of ['TM-01', 'TM-02', 'TM-03', 'TM-04', 'TM-05', 'TM-06', 'TM-07', 'TM-08']) DEF[id] = { when: 'fuori', fx: async (p, o, cid) => { await setMap(p, cid); return cid === 'TM-01' ? undefined : 'keep'; }, ai: (p, o) => aiMapScore(p, o, id), nota: 'Il tesoro cambia Cripta (se è già sulla plancia, al massimo 2 volte per partita); gli Indizi restano. Una sola Mappa attiva: la nuova sostituisce la vecchia.' };
DEF['TM-01'].nota = 'Sposta solo il tesoro: il tabellone resta com\'è.';

// --- Equipaggiamento ---
function eqValue(p, id) {
  const fake = { ...p, equip: { elmo: id, dx: null, sx: null, armatura: null }, flags: {} };
  const b = eqBonus(fake); let v = b.att * 1.2 + b.ar + b.mov * 0.3 + b.pv * 0.5 + b.adv * 2 - b.dis * 3;
  switch (baseId(id)) { case 'TE-01': v += 0.6; break; case 'TE-02': v += 1; break; case 'TE-03': v += 0.8; break; case 'TE-07': v += 0.4; break; case 'TE-08': v += 0.8; break; case 'TE-09': v += 0.3; break; case 'TE-11': v += 0.6; break; case 'TE-12': v += 0.3; break; case 'TE-13': v += 0.6; break; case 'TE-14': v += 0.4; break; case 'TE-15': v += 1; break; case 'TE-16': v += 0.3; break; case 'TE-18': v += 0.3; break; case 'TE-19': v += 0.4; break; case 'TE-20': v += 0.3; break; }
  return v;
}
function aiEquipScore(p, id) {
  const s = SLOT[baseId(id)]; const cur = p.equip[s];
  return eqValue(p, id) - (cur ? eqValue(p, cur) : 0) + (cur ? 0 : 2);
}
function te(on, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { await equip(p, id); if (on) await on(p, o, id); return 'keep'; }, ai: (p, o, id) => aiEquipScore(p, id) };
}
const NOTE_TE = {
  'TE-01': 'Le Trappole pescate dal sacchetto non hanno effetto su di te.', 'TE-02': '+1 ATT solo contro creature, mini-boss e Guardiano.',
  'TE-03': 'La prima creatura che sconfiggi in ogni turno ti fa riprendere 1 carta dagli scarti.', 'TE-04': '+1 AR. Ritiri un D6 di un tuo incantesimo una volta per turno.',
  'TE-07': 'Quando un nemico ti manca subisce 1 danno.', 'TE-08': 'Una volta per partita annulli i danni di un colpo (l\'IA lo usa sui colpi da 3 o più).',
  'TE-09': 'Se il D6 della perdita dice Arma DX, si ritira.', 'TE-11': '+1 ATT. Ritiri un D6 una volta per turno.', 'TE-12': '+1 ATT, +1 danno ai non morti (Scheletro, Zombi, eroi Sanguar).',
  'TE-13': '+1 danno al primo incantesimo di danno di ogni turno.', 'TE-14': '+1 PV quando ti curi con un incantesimo.', 'TE-15': '+1 ATT negli scontri che inizi tu (contro le creature quasi sempre).',
  'TE-16': '+1 AR, 1 PV in meno dalle Trappole.', 'TE-18': '+1 MOV, +1 PV in Locanda.', 'TE-19': '+1 AR, +2 AR in più contro i nemici di LV 3 o più (mazzetto II, mini-boss e boss).', 'TE-20': '+1 AR, +1 PV alla Fonte.',
};
for (let i = 1; i <= 20; i++) { const id = 'TE-' + String(i).padStart(2, '0'); DEF[id] = te(null, { nota: NOTE_TE[id] }); }

// --- Incantesimi ---
const T = (o) => DEF[o.id] = o;
const inCombat = () => !!G.combat;
const creatureFoe = p => { const f = foeOf(p); return f && f.isCreature ? f : null; };
const missing = p => maxPV(p) - p.pv;
const adjFoes = p => { const f = foeOf(p); if (f && !f.isCreature) return [f]; return others2(p).filter(x => x.pos.c >= 0 && hexDist(x.pos, p.pos) <= 1); };
async function pickAdj(p, title, filter = () => true) { const cand = adjFoes(p).filter(filter); if (cand.length <= 1) return cand[0]; return G.players[await ask(p, title, cand.map(x => ({ label: x.name, value: x.id })), { ai: () => cand.slice().sort((a, b) => b.clues - a.clues)[0].id })]; }
const DMG_SPELLS = ['TI-02', 'TI-09', 'TI-10', 'TI-11', 'TI-16', 'TI-19', 'TI-35', 'TI-40'];
async function spellHit(p, f, n, label) { const b = spellDmgBonus(p); log(`${label}: ${n + b} danni a ${f.name}.`); await hurt(f, n + b, G.combat); if (!G.combat && !f.isCreature && f.pv <= 0) await defeat(f, `da ${p.name}`); }
async function spellHeal(p, n) { heal(p, n + spellHealBonus(p)); }
const aiDmg = (p, ev) => { const f = foeOf(p); if (!f) return 0; return f.pv <= ev + 1 ? 4 : (G.combat.kind !== 'creatura' ? 3.5 : 2.2); };

T({ id: 'TI-01', when: 'sempre', fx: async p => { p.flags.flusso = (p.flags.flusso || 0) + 1; log('Il prossimo incantesimo di danno infligge +1.'); }, ai: p => p.hand.some(x => DMG_SPELLS.includes(baseId(x))) ? 1.2 : 0.2 });
T({ id: 'TI-02', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const { n } = await spellDie(p, 'Dardo Arcano'); await spellHit(p, creatureFoe(p), n, 'Dardo Arcano'); }, ai: p => aiDmg(p, 3.5) });
T({ id: 'TI-03', when: 'sempre', fx: async p => addMod(p, { label: 'Scudo di Cenere: +2 AR', ar: 2, kind: 'scontri', n: 1 }), ai: () => inCombat() ? 2.5 : 1, nota: 'Dura fino alla fine del prossimo scontro (o di quello in corso).' });
T({ id: 'TI-04', when: 'scontro', need: p => { const f = creatureFoe(p); return (f && f.pv === 1 && G.combat.kind !== 'boss') || 'Serve una creatura con 1 PV'; }, fx: async p => { const f = creatureFoe(p); f.pv = 0; log(`${f.name} viene spezzato con lo sguardo.`, 'good'); }, ai: () => 5 });
T({ id: 'TI-05', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima del tiro di Movimento', fx: async p => addMod(p, { label: 'Passo del Folletto', mov: 3, kind: 'turn' }), ai: p => G.phase === 'prima' ? (isLocated(p) ? 3 : 1.2) : -1 });
T({ id: 'TI-06', when: 'fuori', need: p => !p.flags.trapWard || 'Hai già una protezione dalle Trappole', fx: async p => { p.flags.trapWard = true; log('La prossima Trappola che peschi non avrà effetto.'); }, ai: p => p.flags.trapWard || isLocated(p) ? -1 : 0.6, nota: 'Resta davanti a te finché non peschi una Trappola.' });
T({ id: 'TI-07', when: 'sempre', need: (p, o, id) => p.discard.some(x => x !== id) || 'La pila degli scarti è vuota', fx: async (p, o, id) => { await recover(p, 1, { except: id }); }, ai: p => p.discard.length ? 2 : 0 });
T({ id: 'TI-08', when: 'sempre', need: p => !p.insp || 'Hai già l\'Ispirazione', fx: async p => giveInsp(p, 'Scintilla'), ai: () => 1.3 });
T({ id: 'TI-09', when: 'scontro', fx: async p => { const f = foeOf(p); const { n } = await spellDie(p, 'Palla di Fuoco'); await spellHit(p, f, n + (f.pv < (f.isCreature ? f.maxpv : maxPV(f)) ? 1 : 0), 'Palla di Fuoco'); }, ai: p => aiDmg(p, 4) });
T({ id: 'TI-10', when: 'scontro', fx: async p => { const f = foeOf(p); const { n } = await spellDie(p, 'Raggio Gelido', 1); await spellHit(p, f, n, 'Raggio Gelido'); addCmod(G.combat, f, 'att', -1); log(`${f.name}: −1 ATT per questo scontro.`); }, ai: p => aiDmg(p, 3) });
T({ id: 'TI-11', when: 'scontro', fx: async p => { const f = foeOf(p); let tot = 0, v; do { v = (await spellDie(p, 'Catena di Fulmini', 1)).v; tot += Math.max(1, v - 1); } while (v === 6); await spellHit(p, f, tot, 'Catena di Fulmini'); }, ai: p => aiDmg(p, 3.2) });
T({ id: 'TI-12', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { G.combat.confuse = true; log('Il prossimo tiro per colpire della creatura sarà con svantaggio.'); }, ai: p => { const f = creatureFoe(p); return f && G.combat.kind !== 'creatura' ? 2.2 : 1; } });
T({ id: 'TI-13', when: 'scontro', fx: async p => { G.combat.velo = p; log(`${p.name} svanisce nell'ombra: lo scontro si annulla.`); }, ai: p => { const f = foeOf(p); return f && p.pv <= 4 && power(f, G.combat) > power(p, G.combat) * 1.2 ? 5 : -1; }, nota: 'Lo scontro finisce senza ricompense e senza arretrare.' });
T({ id: 'TI-14', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima di muoverti', fx: async p => addMod(p, { label: 'Teletrasporto Breve', mov: 1, kind: 'turn' }), ai: p => G.phase === 'prima' && isLocated(p) ? 1.5 : 0.3, nota: 'Nel simulatore vale come +1 casella di movimento.' });
T({ id: 'TI-15', when: 'fuori', need: p => !p.located || 'Hai già individuato il tesoro', fx: async p => { p.flags.sussurro = true; log('Mappa Sussurrata: il prossimo scontro vinto su una casella esplorazione dà 1 Indizio in più.'); }, ai: p => p.flags.sussurro ? -1 : (p.clues >= 1 ? 4 : 2.5), nota: 'Vale fino al prossimo scontro vinto contro una creatura o un mini-boss.' });
T({ id: 'TI-16', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Fiamma Persistente', 1); await spellHit(p, f, n, 'Fiamma Persistente'); G.combat.burn = (G.combat.burn || 0) + 1; }, ai: p => aiDmg(p, 3) + (G.combat && G.combat.foe.pv > 4 ? 0.5 : 0), nota: 'Poi 1 danno all\'inizio di ogni round seguente.' });
T({ id: 'TI-17', when: 'trappola', fx: async p => { p.turnFlags.barriera = true; }, ai: () => -1, nota: 'Si gioca quando peschi una Trappola: non perdi PV (l\'equipaggiamento sì).' });
T({ id: 'TI-18', when: 'sempre', fx: async p => { p.flags.riflesso = true; log('Fino al tuo prossimo turno chi ti ferisce subisce 1 danno.'); }, ai: p => { const f = foeOf(p); return f && !f.isCreature ? 2 : 0.2; } });
T({ id: 'TI-19', when: 'sempre', need: p => adjFoes(p).length > 0 || 'Nessun avversario a una casella', fx: async p => { const t = await pickAdj(p, 'Tocco Gelido: su chi?'); const { n } = await spellDie(p, 'Tocco Gelido'); await spellHit(p, t, n, 'Tocco Gelido'); }, ai: () => 3 });
T({ id: 'TI-20', when: 'sempre', need: p => adjFoes(p).some(x => x.discard.length) || 'Nessun avversario a una casella con carte negli scarti', fx: async p => { const t = await pickAdj(p, 'Furto di Memoria: a chi?', x => x.discard.length); await recover(p, 1, { from: t.discard, title: `Prendi una carta dagli scarti di ${t.name}` }); }, ai: () => 2.2 });
T({ id: 'TI-21', when: 'sempre', fx: async p => { p.turnFlags.specchio = true; }, ai: p => { const f = creatureFoe(p); return f ? 1.6 : 0.2; }, nota: 'Se in questo turno sconfiggi una creatura prendi l\'Ispirazione.' });
T({ id: 'TI-22', when: 'scontro', fx: async p => { p.flags.nextHit = (p.flags.nextHit || 0) + 3; }, ai: () => 2.3 });
T({ id: 'TI-23', when: 'sempre', need: p => adjFoes(p).length > 0 || 'Nessun avversario a una casella', fx: async p => { const t = await pickAdj(p, 'Sigillo del Silenzio: su chi?'); t.silenced = p.id; log(`${t.name} non può giocare Incantesimi fino al prossimo turno di ${p.name}.`); }, ai: p => { const f = foeOf(p); return f && !f.isCreature ? 2.5 : 0.5; } });
T({ id: 'TI-24', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); addCmod(G.combat, f, 'att', 1 - atkOf(f, G.combat)); log(`${f.name} diventa un ratto: ATT 1.`); }, ai: p => { const f = creatureFoe(p); return f ? (f.att >= 3 ? (G.combat.kind !== 'creatura' ? 4 : 2.5) : 1) : 0; } });
T({ id: 'TI-25', when: 'sempre', need: p => p.pv < maxPV(p) || 'Hai già tutti i PV', fx: async p => { const { n } = await spellDie(p, 'Benedizione', 1); await spellHeal(p, n); }, ai: p => missing(p) >= 3 || (G.combat && p.pv <= 3) ? 2.5 : 0 });
T({ id: 'TI-26', when: 'sempre', need: p => p.pv < maxPV(p) || 'Hai già tutti i PV', fx: async p => { const { n } = await spellDie(p, 'Mano Guaritrice'); await spellHeal(p, n); }, ai: p => missing(p) >= 4 || (G.combat && p.pv <= 3) ? 3 : 0 });
T({ id: 'TI-27', when: 'sempre', fx: async p => addMod(p, { label: 'Scudo della Fede: +1 AR', ar: 1, kind: 'untilNext' }), ai: () => inCombat() ? 1.8 : 0.6 });
T({ id: 'TI-28', when: 'sempre', fx: async p => { p.flags.nextDmg = (p.flags.nextDmg || 0) + 2; }, ai: () => inCombat() ? 2.2 : 0.8, nota: 'Vale per il prossimo colpo che va a segno.' });
T({ id: 'TI-29', when: 'sempre', fx: async p => { p.flags.nextHit = (p.flags.nextHit || 0) + 2; }, ai: () => inCombat() ? 1.8 : 0.6 });
T({ id: 'TI-30', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si gioca quando un colpo ti ferisce (l\'IA la usa sui colpi da 3 o più o letali).' });
T({ id: 'TI-31', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima del tiro di Movimento', fx: async p => { addMod(p, { label: 'Carica Impetuosa', mov: 2, kind: 'turn' }); p.turnFlags.carica = true; }, ai: p => G.phase === 'prima' ? (isLocated(p) ? 2.5 : 1.3) : -1 });
T({ id: 'TI-32', when: 'sempre', need: (p, o, id) => p.discard.some(x => x !== id) || p.pv < maxPV(p) || 'Niente da recuperare', fx: async (p, o, id) => { await recover(p, 1, { except: id }); await spellHeal(p, 1); }, ai: p => p.discard.length ? 2.2 : 0 });
T({ id: 'TI-33', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si gioca subito dopo un tuo tiro: lo ritiri.' });
T({ id: 'TI-34', when: 'scontro', need: p => equipped(p).some(id => SHIELDS.includes(baseId(id))) || 'Serve uno scudo equipaggiato', fx: async p => { addCmod(G.combat, p, 'ar', 2); log(`${p.name}: +2 AR per questo scontro.`); }, ai: () => G.combat && G.combat.kind !== 'creatura' ? 3 : 1.8 });
T({ id: 'TI-35', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Fendente Radioso'); await spellHit(p, f, n + (isUndead(f) ? 2 : 0), 'Fendente Radioso'); }, ai: p => aiDmg(p, 3.5) });
T({ id: 'TI-36', when: 'sempre', fx: async p => { p.flags.giuramento = 2; }, ai: () => inCombat() ? 1.8 : 0.5 });
T({ id: 'TI-37', when: 'scontro', need: p => (G.combat.p === p && !G.combat.foeFirst) || 'Solo negli scontri in cui attacchi per primo', fx: async p => { p.flags.nextDmg = (p.flags.nextDmg || 0) + 2; }, ai: () => 2.2, nota: 'Vale per il prossimo colpo a segno.' });
T({ id: 'TI-38', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si scarta (non conta come carta giocata) per ritirare un tuo tiro per colpire.' });
T({ id: 'TI-39', when: 'trappola', fx: async p => { p.turnFlags.felpato = true; }, ai: () => -1, nota: 'Si gioca quando peschi una Trappola: la ignori del tutto.' });
T({ id: 'TI-40', when: 'scontro', need: p => (G.combat.p === p && !G.combat.attacks && !!creatureFoe(p)) || 'Solo all\'inizio di uno scontro contro una creatura, prima del primo attacco', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Lancio di Coltello', 1); await spellHit(p, f, n, 'Lancio di Coltello'); }, ai: p => aiDmg(p, 3) });

// ===================== Gioco delle carte =====================
function zarkoWake(p) {
  p.ritual = false;
  addMod(p, { label: 'Zarko predatore della vita', att: BAL.zarko[0], mov: BAL.zarko[0], ar: BAL.zarko[2] ?? BAL.zarko[0], pv: BAL.zarko[3] ?? BAL.zarko[0], kind: 'game' });
  locate(p); p.zarko = 2; p.zarkoStart = p.ownTurns;
  log(`${p.name} diventa Zarko predatore della vita! Se non vince entro 2 turni, perde la partita.`, 'bad');
}
const isGear = id => C(id).tipo === 'TE' && SLOT[baseId(id)] !== 'pozione';
function canPlay(p, id, { free = false, react = false } = {}) {
  const d = DEF[baseId(id)]; const c = G.combat; const o = opp(p);
  if (!d) return 'Carta sconosciuta';
  if (isGear(id) && p.eqTurn) return 'Puoi equipaggiare un solo oggetto per turno';
  if (isGear(id) && BAL.gearStart !== false && !free && !react && (G.combat || (G.phase !== 'prima' && G.phase !== 'inizio'))) return 'Gli equipaggiamenti si indossano solo a inizio turno';
  if (C(id).cls && !C(id).cls.some(k => isC(p, k))) return `Carta di classe ${C(id).cls.join(' o ')}`;
  if (p.silenced !== undefined && p.silenced !== null && C(id).tipo === 'TI') return 'Sigillo del Silenzio: niente Incantesimi fino al prossimo turno di chi l\'ha giocato';
  if (!react && (d.when === 'reazione' || d.when === 'trappola')) return d.when === 'trappola' ? 'Si gioca quando peschi una Trappola' : 'Si gioca in risposta (a un colpo o a un tuo tiro)';
  if (G.over) return 'Partita finita';
  if (p.noCardsFrom && p.ownTurns >= p.noCardsFrom && p.ownTurns <= p.noCardsTo) return 'Esercito nanico: niente carte Trama in questo turno';
  if (react) { if (free) return true; if (G.combat && G.combat.foe === p) return G.combat.defCards >= 1 ? 'In difesa puoi giocare 1 sola carta per scontro' : true; if (G.players[G.cur] !== p) return 'Non è il tuo turno'; return p.played >= p.limit ? `Hai già giocato ${p.limit} carte in questo turno` : true; }
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
async function playCard(p, id, { free = false, immediate = false, react = false } = {}) {
  const why = canPlay(p, id, { free, react });
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
function power(x, c) { const pv = x.pv; const [s, b] = dmgDice(x); return pv * (s / 2 + b) * (atkOf(x, c) + HIT_DIE() + 1 - (BAL.defBase ?? 14)) / HIT_DIE(); }
function aiCombat(x, c, opts) {
  const foe = x === c.p ? c.foe : c.p;
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
  p.mods = p.mods.filter(m => m.kind !== 'untilNext'); p.flags.riflesso = false; for (const x of G.players) if (x.silenced === p.id) x.silenced = null;
  if (BAL.magoPerTurn && isC(p, 'Mago')) p.magoRerolls = BAL.magoRerolls;
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
    const a = await ask(p, 'Inizio turno: gioca fino a 2 carte (gli equipaggiamenti solo ora), poi muoviti', o, { cards: true, ai: () => { const c = aiBestCard(p, 1); if (c) return { card: c }; if (o[1] && p.pv <= maxPV(p) - 2) return 'pal'; return 'move'; } });
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
    const a = await ask(p, 'Fine turno: puoi ancora giocare carte (non equipaggiamenti), poi chiudi il turno', o, { cards: true, ai: () => { const c = aiBestCard(p, 2.5); return c ? { card: c } : 'end'; } });
    if (G.over) return;
    if (a && a.card) { await playCard(p, a.card); if (G.over) return; continue; }
    if (a === 'pal') { p.palHeals--; heal(p, 2); continue; }
    break;
  }
  await endOfTurn(p, false);
}
// segnalino Nemico I → mazzetto LV 1-2; segnalino Nemico II → mazzetto LV 3-4 (con i mini-boss LV 4,5 se la regola facoltativa è attiva)
const deckII = () => [...MAZZO_II, ...(BAL.miniBoss && !BAL.monLv ? MINIBOSS : [])];
const deckIII = () => BOSSES.filter(b => !G.boss || b.name !== G.boss.name); // mazzetto 3 = boss LV 5 (Daniele, 2/11, niente mini-boss); quello pescato a inizio partita custodisce MIMI
const monTier = p => { if (BAL.monBy === 'clues') return Math.min(3, 1 + (p.clues || 0)); if (BAL.monBy === 'pe') return Math.min(3, 1 + Math.floor(((p.level - 1) * 2 + p.pe) / 2)); const t = BAL.monTh || [3, 5]; return p.level >= t[1] ? 3 : p.level >= t[0] ? 2 : 1; };
async function meetCreature(p, kind) {
  let tier = BAL.monLv ? monTier(p) : (kind === 'miniboss' ? 2 : 1);
  if (p.challenge && tier < 2) { tier = 2; log('Sfidare i potenti: al posto della creatura appare un nemico del mazzetto II!', 'gold'); }
  const deckK = ['cr', 'mb', 't3'][tier - 1];
  if (!G.nem[deckK] || !G.nem[deckK].length) G.nem[deckK] = shuffle(tier === 3 ? deckIII() : tier === 2 ? deckII() : [...BESTIARIO]);
  if (BAL.monLv) log(`${p.name} è di livello ${p.level}: gira la prima carta del mazzetto Mostri ${tier}.`);
  const foe = makeCreature(G.nem[deckK].pop(), p.level);
  kind = foe.tipo === 'Mini-boss' || foe.tipo === 'Boss' ? 'miniboss' : 'creatura';
  const st = `${foe.name} (LV ${String(foe.lv).replace('.', ',')}): PV ${foe.pv}, ATT ${fmt(foe.att)}, AR ${foe.ar} (Difesa ${DIFESA(foe.ar)}), danno ${dmgLabel(foe)}. ${foe.abil || ''}`;
  const opts = [{ label: 'Affronta lo scontro', value: 'f' }];
  if (!noFlee(foe)) opts.push({ label: foe.fx === 'lento' || isC(p, 'Ladro') ? 'Fuggi (resti dove sei)' : 'Fuggi (arretri di una casella)', value: 'r' });
  const ch = await ask(p, `Incontri ${kind === 'miniboss' ? 'un mini-boss' : foe.lv >= 3 ? 'un nemico del mazzetto II' : 'un nemico'}! ${st}`, opts, { ai: () => (opts.length > 1 && power(foe) > power(p) * 1.6 && p.pv <= 4 ? 'r' : 'f') });
  if (ch === 'r') {
    log(`${p.name} dichiara la fuga.`);
    if (foe.fx === 'inseguitore') {
      const c = { p, foe, kind, round: 0, berserk: {}, carica: {}, mods: {}, reflect: {}, spinato: {}, chierico: {}, daga: {}, petrified: {}, dis: {}, used: {}, defCards: 0, noCards: true };
      G.combat = c; log(`${foe.name} ti insegue e attacca!`, 'bad'); await attack(foe, p, c); G.combat = null;
      if (dead(p)) { await defeat(p, `da ${foe.name}`); return; }
    }
    if (isC(p, 'Ladro') || foe.fx === 'lento') log(isC(p, 'Ladro') ? 'Ladro: fugge senza arretrare.' : `${foe.name} è lento: non arretri.`); else retreat(p, p.turnStart);
    return;
  }
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
      const foe = makeCreature(G.beholder ? { ...BEHOLDER, pv: BAL.behPV || BEHOLDER.pv } : { ...G.boss });
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
      if (tl.type === 'locanda' && p.flags.revived && isC(p, 'Oracolo')) { p.flags.revived = false; log(`${p.name} ha già usato questa Locanda, ma l'Oracolo ricarica la sua resurrezione.`, 'good'); return; }
      log(`${p.name} ha già usato questo edificio.`); return;
    }
    if (!again) tl.used.push(p.id);
  }
  if (tl.q && !tl.revealed) {
    const bag = G.tiles.bag;
    if (!bag.length) { tl.type = 'vuota'; tl.revealed = true; tl.done = true; tl.q = false; log('Il sacchetto è vuoto: la casella resta tranquilla.'); return; }
    tl.type = bag.pop(); log(`${p.name} pesca dal sacchetto: ${TILE[tl.type].n} (ne restano ${bag.length}).`);
  }
  if (tl.type === 'imprevisto') { const card = drawImp(); log(`${p.name} gira la prima carta Imprevisto: ${TILE[card].n}.`); tl.type = card; }
  tl.revealed = true; tick('casella');
  switch (tl.type) {
    case 'vuota': log('Niente da segnalare.'); tl.done = true; break;
    case 'creatura': case 'miniboss': await meetCreature(p, tl.type); break;
    case 'evento': if (!tl.used) tl.done = true; await chaosEvent(p); break;
    case 'locanda': { const pe = !(again && BAL.buildings === 'pe-once'); log(pe ? 'Locanda: si guadagna metà livello (1 PE) e si recuperano 2 PV.' : 'Locanda: si recuperano 2 PV (il PE si prende solo la prima volta).', 'good'); if (!tl.used) tl.done = true; p.flags.revived = false; heal(p, (BAL.locHeal || 2) + (has(p, 'TE-18') ? 1 : 0)); if (pe) await addPE(p, 1); break; }
    case 'fonte': log('Fonte: puoi recuperare fino a 2 carte dagli scarti.', 'good'); if (!tl.used) tl.done = true; await recover(p, 2); if (has(p, 'TE-20')) heal(p, 1); break;
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
      if (has(p, 'TE-01')) { log('Elmo sorgisogno: vedi la Trappola in tempo, nessun effetto.', 'good'); break; }
      if (p.flags.trapWard) { p.flags.trapWard = false; log('Occhio dello Stregone: la Trappola non ha effetto.', 'good'); break; }
      if (await reactCard(p, 'TI-39', 'Trappola')) { log('Passo Felpato: ignori la Trappola.', 'good'); break; }
      let d = Math.max(1, await roll(p, 6, 'Danni della trappola (D6 − 1, minimo 1)') - 1);
      if (G.map && G.map.id === 'TM-08') { d *= 2; log('Flegias: la Trappola fa il doppio dei danni.', 'bad'); }
      if (has(p, 'TE-16')) d = Math.max(0, d - 1);
      if (d >= 2 && await reactCard(p, 'TI-17', `Trappola da ${d} danni`)) { log('Barriera Runica: nessun danno.', 'good'); d = 0; }
      await hurt(p, d);
      if (p.pv <= 0) { await defeat(p, 'trappola'); break; }
      await lossRoll(p); break;
    }
    case 'indizio': tl.done = true; log('Una mappa strappata con un segno sopra!'); await addClue(p); break;
  }
  // sacchetto: il segnalino risolto torna nella scatola e la casella torna «?» (una creatura non sconfitta resta scoperta)
  if (BAL.bagRecycle && tl.q && tl.done && TILE[tl.type]) { const b = G.tiles.bag; b.splice(Math.floor(Math.random() * (b.length + 1)), 0, tl.type); }
  if (tl.q && tl.done) { if (G.tiles.bag.length) { tl.type = 'q'; tl.revealed = false; tl.done = false; } else tl.type = 'vuota'; }
}
function drawImp() {
  if (!G.imp || !G.imp.length) G.imp = shuffle(Object.entries(BAL.impDeck).flatMap(([k, n]) => Array(n).fill(k)));
  const c = G.imp.pop(); G.imp.unshift(c); return c;
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
for (const c of CARDS) if (c.cls && c.tipo !== 'TC') for (const k of c.cls) (DECK[k] = DECK[k] || []).push(c.id);
const COMMON = CARDS.filter(c => c.tipo !== 'TC' && !c.cls).map(c => c.id);
// mano: Carta Classe + BAL.handCls carte della tua classe + il resto dal mazzo comune (10 in tutto)
function dealList(list) {
  const used = new Set();
  for (const sp of list) {
    const mine = shuffle((DECK[sp.cls] || []).filter(id => !used.has(id))).slice(0, BAL.handClsRnd);
    mine.forEach(id => used.add(id));
    const com = shuffle(commonPool().filter(id => !used.has(id))).slice(0, BAL.handTot - mine.length);
    com.forEach(id => used.add(id));
    sp.deck = BAL.handMode === 'draft' ? [] : [...mine, ...com];
  }
}
function dealDecks() { dealList(S.players.slice(0, S.n)); }
function newPlayer(i, sp) {
  const R = RACES[sp.race];
  const base = { pv: (BAL.basePV || 5) + (sp.cls === 'Guerriero' ? BAL.guerPV : 0) + ((BAL.clsPV || {})[sp.cls] || 0), att: 1, mov: 1 + (sp.cls === 'Ladro' ? BAL.ladroMov : 0) + (BAL.clsMov[sp.cls] || 0), ar: 1 };
  for (const k in R.fixed) base[k] += R.fixed[k];
  for (let j = 0; j < R.free; j++) { const k = sp.free[j] && sp.free[j] !== 'pv' ? sp.free[j] : 'att'; base[k]++; }
  return {
    id: i, name: sp.name.trim() || `Giocatore ${i + 1}`, ai: sp.ai, race: sp.race, base, pv: base.pv, level: 1, pe: 0, clues: BAL.startClues || 0, located: false, tempLocated: 0, insp: false,
    hand: [...sp.deck], discard: [], equip: { elmo: null, dx: null, sx: null, armatura: null }, lost: [], classes: [], classCards: [],
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
    for (const k of [...(BAL.bldBag ? [] : BUILDINGS), ...(BAL.caos ? ['evento'] : [])]) for (const [c, r] of PHYS[k]) tiles[r][c] = { type: k, revealed: true, done: false, used: [] };
    PHYS.cripta.forEach(([c, r], i) => { tiles[r][c] = { type: 'cripta', revealed: true, done: true, crypt: i + 1 }; });
    const bag = shuffle(Object.entries(BAL.colorBag ? BAL.bagColor : { ...(BAL.bagDraw ? (BAL.bag || PHYS.tokensBag) : PHYS.tokens), ...(BAL.bldBag ? BAL.bldTok : {}) }).flatMap(([k, n]) => Array(n).fill(k)));
    const qHex = BAL.bldBag && BAL.bldHexQ !== false ? [...PHYS.q, ...BUILDINGS.flatMap(k => PHYS[k]).filter(h => !PHYS.q.some(x => x[0] === h[0] && x[1] === h[1]))] : PHYS.q;
    if (qHex !== PHYS.q) qHex.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    if (BAL.bagDraw) { tiles.bag = bag; qHex.forEach(([c, r]) => { tiles[r][c] = { type: 'q', revealed: false, done: false, q: true }; }); }
    else qHex.forEach(([c, r], i) => { tiles[r][c] = { type: bag[i], revealed: false, done: false }; });
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
// ===================== Mano: carte di classe scelte, carte comuni draftate (Daniele, 27/10) =====================
// valore di partenza di ogni carta per l'IA (vittorie di chi l'aveva in mano / attese, da partite simulate con mani casuali)
const DRAFT_VAL = {"TE-14": 0.957, "TE-04": 1.008, "TI-34": 0.989, "TI-07": 0.969, "TM-04": 0.964, "TE-10": 0.971, "TI-14": 0.97, "TE-19": 0.99, "TI-21": 0.979, "TI-20": 0.978, "TE-03": 0.995, "TE-11": 1.009, "TE-13": 0.996, "TM-07": 0.977, "TE-20": 0.991, "TI-17": 0.979, "TI-12": 0.963, "TI-22": 0.999, "TE-06": 0.981, "TM-03": 0.984, "TI-37": 1.002, "TI-38": 1.024, "TI-40": 1.001, "TE-07": 1.074, "TE-17": 0.968, "TI-23": 0.962, "TM-06": 0.964, "TI-16": 1.103, "TI-10": 1.039, "TI-02": 1.063, "TI-35": 1.014, "TI-31": 1.001, "TE-18": 0.993, "TI-08": 1.031, "TE-08": 1.163, "TE-01": 0.997, "TI-33": 1.018, "TI-30": 1.018, "TE-16": 0.982, "TM-08": 0.974, "TM-05": 0.99, "TI-09": 1.07, "TI-18": 0.948, "TI-05": 0.969, "TI-06": 0.993, "TI-04": 0.966, "TI-03": 0.969, "TI-11": 1.047, "TE-09": 0.968, "TI-25": 0.975, "TI-15": 1.286, "TM-02": 0.998, "TI-13": 0.919, "TI-19": 0.978, "TI-39": 0.983, "TE-05": 0.93, "TI-29": 1.022, "TI-01": 0.954, "TE-02": 1.027, "TE-15": 0.989, "TI-32": 0.988, "TM-01": 0.981, "TI-28": 0.971, "TI-27": 0.978, "TI-36": 1.007, "TI-24": 0.989, "TI-26": 0.998, "TE-12": 1.023};
const draftVal = id => DRAFT_VAL[baseId(id)] || 1;
function aiPickScore(hand, id) {
  let s = draftVal(id) - 1;
  const sl = SLOT[baseId(id)];
  if (sl && sl !== 'pozione' && hand.some(x => SLOT[baseId(x)] === sl)) s -= 0.5 * Math.max(0, s) + 0.02; // stesso slot: vale meno
  return s + (Math.random() - 0.5) * (BAL.draftNoise || 0);
}
const aiPick = (hand, opts) => opts.slice().sort((a, b) => aiPickScore(hand, b) - aiPickScore(hand, a))[0];
const cardLabel = id => { const t = C(id).testo; return `${C(id).nome}: ${t.length > 110 ? t.slice(0, 107) + '…' : t}`; };
async function pickCard(p, title, opts) {
  if (p.ai || G.fast) return aiPick(p.hand, opts);
  return ask(p, title, opts.map(id => ({ label: cardLabel(id), value: id })), { ai: () => aiPick(p.hand, opts) });
}
async function buildHands() {
  const myGame = G, ps = G.players, n = ps.length;
  // 1. ognuno sceglie BAL.handCls carte tra quelle della sua classe (le carte con due classi sono stampate in due copie)
  for (const p of ps) {
    let pool = (DECK[p.startCls] || []).slice();
    for (let k = 0; k < BAL.handCls && pool.length; k++) {
      const ch = await pickCard(p, `Scegli le tue carte ${p.startCls} (${k + 1} di ${BAL.handCls})`, pool);
      if (G !== myGame) return new Promise(() => {});
      p.hand.push(ch); pool = pool.filter(x => x !== ch);
    }
    if (!p.ai) log(`${p.name} ha scelto le sue carte di classe.`); else log(`${p.name} sceglie le sue carte di classe.`);
  }
  // 2. draft delle carte comuni: un pacchetto coperto a testa, scegli una carta e passa il resto a sinistra
  const size = BAL.handTot - BAL.handCls;
  const deck = shuffle(commonPool().slice());
  const packs = ps.map(() => deck.splice(0, size + (BAL.draftExtra || 0)));
  log(`Draft delle carte comuni: ${size} giri, si passa a sinistra.`, 'turn');
  for (let r = 0; r < size; r++) {
    for (let i = 0; i < n; i++) {
      const p = ps[i], pack = packs[(i + r) % n];
      const ch = await pickCard(p, `Draft delle carte comuni, giro ${r + 1} di ${size}: prendi una carta e passa le altre`, pack);
      if (G !== myGame) return new Promise(() => {});
      p.hand.push(ch); pack.splice(pack.indexOf(ch), 1);
    }
  }
  for (const p of ps) p.startHand = [...p.hand];
  render();
}
async function initClasses() {
  const myGame = G;
  if (BAL.handMode === 'draft') { await buildHands(); if (G !== myGame) return new Promise(() => {}); } else for (const p of G.players) p.startHand = [...p.hand];
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
  G = { nem: { cr: [], mb: [] }, stage: 'early', time: { tot: 0, early: 0, mid: 0, late: 0, at: {}, n: { early: {}, mid: {}, late: {} }, m: {} }, players: [], cur: 0, tiles: newBoard(), map: null, treasure: null, log: [], combat: null, phase: 'inizio', stop: 0, copy: 0, round: 0, beholder: false, bossWounds: 0, swap: null, over: null, reach: null, thinking: '', revealedFor: null, fast, rules };
  G.players = list.map((sp, i) => newPlayer(i, sp));
  G.stats = { played: G.players.map(() => []) };
  const minD = Math.max(2, Math.round(COLS * 0.3));
  let cand = allHexes().filter(h => tileAt(h).type !== 'start' && SPAWNS.every(s => hexDist(h, s) >= minD));
  if (!cand.length) cand = allHexes().filter(h => tileAt(h).type !== 'start' && SPAWNS.every(s => hexDist(h, s) >= 2));
  G.treasure = physBoard() ? (([c, r]) => ({ c, r }))(pick(PHYS.cripta)) : pick(cand);
  G.boss = BAL.bossDeck && BOSSES.length ? pick(BOSSES) : { ...BOSS, pv: BAL.bossPV };
  G.cur = Math.floor(Math.random() * G.players.length); G.first = G.cur;
  log(`Inizia la partita. Comincia ${G.players[G.cur].name}.`, 'turn');
  log(`A custodire MIMI c'è ${G.boss.name}${G.boss.abil ? ': ' + G.boss.abil : ''}`, 'gold');
}
function startGame() {
  pending = null; GEN++;
  createGame(S.players.slice(0, S.n));
  view = 'game';
  render();
  initClasses().then(gameLoop).catch(e => { console.error(e); log('Errore: ' + e.message, 'bad'); render(); });
}
