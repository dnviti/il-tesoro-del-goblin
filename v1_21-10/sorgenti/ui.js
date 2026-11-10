// ===================== Interfaccia =====================
let view = 'setup';
const TIPO = { TI: 'Trama Incantesimo', TE: 'Trama Equipaggiamento', TC: 'Trama Classe', TM: 'Trama Mappa' };
const HEX_R = 30, HW = Math.sqrt(3) * HEX_R, PAD = 6;
function hexXY(h) { return { x: PAD + HW / 2 + HW * (h.c + 0.5 * (h.r & 1)), y: PAD + HEX_R + h.r * HEX_R * 1.5 }; }
function hexPoints(x, y, r) { const o = []; for (let i = 0; i < 6; i++) { const a = Math.PI / 180 * (60 * i - 30); o.push((x + r * Math.cos(a)).toFixed(1) + ',' + (y + r * Math.sin(a)).toFixed(1)); } return o.join(' '); }

function showDie(sides, v) { if (G) { G.lastDie = { sides, v, k: (G.lastDie ? G.lastDie.k : 0) + 1 }; } }

function render() {
  if (G && G.fast) return;
  for (const v of ['setup', 'game', 'rules', 'cards', 'sim']) document.getElementById('view-' + v).hidden = (view !== v);
  document.querySelectorAll('[data-nav]').forEach(b => b.setAttribute('aria-current', b.dataset.nav === view ? 'page' : 'false'));
  document.querySelector('[data-nav="game"]').hidden = !G;
  if (view === 'setup') renderSetup();
  if (view === 'game' && G) renderGame();
}

// ---------- Setup ----------
function renderSetup() {
  const el = document.getElementById('setup-players');
  el.innerHTML = S.players.slice(0, S.n).map((sp, i) => {
    const R = RACES[sp.race];
    const free = Array.from({ length: R.free }, (_, j) => `
      <label class="fld"><span>Bonus a scelta ${R.free > 1 ? j + 1 : ''}</span>
        <select id="free-${i}-${j}" data-free="${i}-${j}">${['att', 'mov', 'ar', 'pv'].map(k => `<option value="${k}" ${sp.free[j] === k ? 'selected' : ''}>+1 ${STATN[k]}</option>`).join('')}</select></label>`).join('');
    return `<article class="pset p${i}">
      <h3><span class="dot"></span>Giocatore ${i + 1}</h3>
      <div class="fields">
        <label class="fld"><span>Nome</span><input id="name-${i}" data-name="${i}" value="${esc(sp.name)}" maxlength="24"></label>
        <label class="fld"><span>Chi gioca</span><select id="ai-${i}" data-ai="${i}"><option value="0" ${!sp.ai ? 'selected' : ''}>Persona</option><option value="1" ${sp.ai ? 'selected' : ''}>Computer (IA)</option></select></label>
        <label class="fld"><span>Classe</span><select id="cls-${i}" data-cls="${i}">${CLASSES.map(c => `<option ${sp.cls === c ? 'selected' : ''} ${S.players.slice(0, S.n).some((x, j) => j !== i && x.cls === c) ? 'disabled' : ''}>${c}</option>`).join('')}</select></label>
        <label class="fld"><span>Razza</span><select id="race-${i}" data-race="${i}">${Object.keys(RACES).map(r => `<option ${sp.race === r ? 'selected' : ''}>${r}</option>`).join('')}</select></label>
        ${free}
      </div>
      <p class="raceinfo">${esc(R.info)}</p>
      <p class="clsinfo"><b>${esc(CARD[CLASS_CARD[sp.cls]].nome)}</b> (giocata a inizio partita): ${esc(CARD[CLASS_CARD[sp.cls]].testo)}</p>
      <p class="deckhint">Mano iniziale: 5 carte a caso dal mazzetto ${esc(sp.cls)} e 5 dal mazzo comune. Le vedrai solo quando la partita inizia.</p>
    </article>`;
  }).join('');
}

// ---------- Partita ----------
function handOwner() {
  if (pending && !pending.p.ai) return pending.p;
  const cur = G.players[G.cur];
  if (!cur.ai) return cur;
  return G.players.find(p => !p.ai) || cur;
}
function renderGame() {
  for (const x of G.players) clamp(x);
  renderBoard();
  renderStatus();
  renderAction();
  renderSheets();
  renderHand();
  document.getElementById('log').innerHTML = G.log.map(l => `<li class="${l.cls}">${esc(l.t)}</li>`).join('');
}
function renderStatus() {
  const cur = G.players[G.cur];
  const map = G.map ? `<span class="chip map">Mappa: ${esc(C(G.map.id).nome)}</span>` : '<span class="chip">Nessuna mappa attiva</span>';
  const d = G.lastDie ? `<span class="die" data-k="${G.lastDie.k}"><small>D${G.lastDie.sides}</small>${G.lastDie.v}</span>` : '';
  const giro = Math.floor(G.round / G.players.length) + 1;
  const omen = BAL.omen && giro >= BAL.omen[0] ? `<span class="chip gold" title="Presagio del Goblin: chi non ha individuato il tesoro tira un D6 a inizio turno">Presagio: ${Math.max(2, 6 - Math.floor((giro - BAL.omen[0]) / BAL.omen[1]))}+</span>` : '';
  const boss = G.bossWounds ? (() => { const mx = G.beholder ? (BAL.behPV || BEHOLDER.pv) : BAL.bossPV; return `<span class="chip bad">${G.beholder ? 'Beholder' : 'Guardiano'} ferito: PV ${mx - G.bossWounds}/${mx}</span>`; })() : '';
  const extra = [`<span class="chip">Giro ${giro}</span>`, omen, boss, G.stop ? `<span class="chip">Stop: ${G.stop} scontri</span>` : '', G.beholder ? '<span class="chip bad">Beholder a guardia</span>' : '', G.swap ? '<span class="chip">Gatto Ciclone attivo</span>' : ''].join('');
  document.getElementById('status').innerHTML = `<div class="turnline"><span class="pdot p${cur.id}"></span><b>${G.over ? 'Partita finita' : 'Turno di ' + esc(cur.name)}</b>${map}${extra}</div>${d}`;
}
function renderBoard() {
  const svg = document.getElementById('board');
  const W = PAD * 2 + HW * (COLS + 0.5), H = PAD * 2 + HEX_R * 2 + HEX_R * 1.5 * (ROWS - 1);
  svg.setAttribute('viewBox', `0 0 ${W.toFixed(0)} ${H.toFixed(0)}`);
  const reach = G.reach ? new Set(G.reach.map(h => h.c + ',' + h.r)) : null;
  const showT = G.players.some(isLocated);
  let s = '';
  for (const h of allHexes()) {
    const t = tileAt(h), { x, y } = hexXY(h);
    const isT = showT && same(h, G.treasure);
    const tok = !t.revealed && physBoard();
    const cls = ['hex', t.revealed ? 'rv ty-' + t.type : 'hid' + (tok ? ' tok' : ''), t.done ? 'done' : '', reach && reach.has(h.c + ',' + h.r) ? 'reach' : '', isT ? 'treasure' : ''].join(' ');
    const glyph = isT ? '◆' : t.spawn ? String(t.spawn) : tok ? '?' : (t.revealed && !(t.done && ['creatura', 'miniboss', 'trappola', 'indizio'].includes(t.type)) ? TILE[t.type].g : '');
    const name = isT ? 'Nascondiglio di MIMI (boss)' : t.spawn ? 'Punto di spawn ' + t.spawn : (t.revealed ? TILE[t.type].n + (t.done ? ' (risolta)' : '') : tok ? 'Segnalino Esplorazione coperto' : 'Casella inesplorata');
    s += `<g class="${cls}" data-hex="${h.c},${h.r}"><title>${name}</title><polygon points="${hexPoints(x, y, HEX_R - 1.5)}"/>${glyph ? `<text x="${x}" y="${y + 1}" class="glyph">${glyph}</text>` : ''}</g>`;
  }
  for (const p of G.players) {
    const { x, y } = hexXY(p.pos.c < 0 ? { c: 0, r: 0 } : p.pos);
    if (p.out || p.pos.c < 0) continue;
    const mates = G.players.filter(x => !x.out && same(x.pos, p.pos));
    const k = mates.indexOf(p), off = mates.length > 1 ? (k - (mates.length - 1) / 2) * 10 : 0;
    s += `<g class="token p${p.id}${p.id === G.cur && !G.over ? ' active' : ''}"><circle cx="${x + off}" cy="${y}" r="13"/><text x="${x + off}" y="${y + 1}">${esc(p.name.trim()[0] || 'P').toUpperCase()}</text></g>`;
  }
  svg.innerHTML = s;
}
function statLine(p, k) {
  const v = k === 'pv' ? maxPV(p) : stat(p, k), b = p.base[k];
  return `<div class="st"><span>${STATN[k]}</span><b>${k === 'pv' ? p.pv + '/' + v : fmt(v)}</b>${k !== 'pv' && v !== b ? `<small>base ${fmt(b)}</small>` : ''}</div>`;
}
function renderSheets() {
  document.getElementById('sheets').innerHTML = G.players.map(p => {
    const adv = advOf(p, G.combat);
    const badges = [
      p.insp ? '<span class="chip gold">Ispirazione</span>' : '',
      isLocated(p) ? '<span class="chip gold">Tesoro individuato</span>' : '',
      p.skip ? `<span class="chip bad">Turni persi: ${p.skip}</span>` : '',
      p.extra ? `<span class="chip good">Turni extra: ${p.extra}</span>` : '',
      adv > 0 ? '<span class="chip good">Vantaggio</span>' : adv < 0 ? '<span class="chip bad">Svantaggio</span>' : '',
      p.magoRerolls ? `<span class="chip">Ritiri Mago: ${p.magoRerolls}</span>` : '',
      p.palHeals ? `<span class="chip">Cure Paladino: ${p.palHeals}</span>` : '',
      p.destino ? `<span class="chip">Destino: ${p.destino}</span>` : '',
      p.ashafe ? `<span class="chip good">Ashafe: ${p.ashafe} turni</span>` : '',
      p.curse ? '<span class="chip bad">Maledetto</span>' : '',
      p.burattinato ? '<span class="chip bad">Burattinaio</span>' : '',
      p.challenge ? `<span class="chip">Sfida: ${p.challenge.bet} turni</span>` : '',
      p.zarko ? `<span class="chip bad">Zarko: ${p.zarko} turni per vincere</span>` : '',
      p.ritual ? `<span class="chip bad">Rituale di Zarko: ${p.skip} turni</span>` : '',
      p.portal ? '<span class="chip good">Portale arcano</span>' : '',
      BAL.chierico === 'locanda' && isC(p, 'Chierico') ? (p.flags.revived ? '<span class="chip">Ritorno in vita usato: ricarica in locanda</span>' : '<span class="chip good">Ritorno in vita pronto</span>') : '',
      BAL.furyMov && fury(p) ? '<span class="chip bad">Furia</span>' : '',
    ].join('');
    const eq = Object.keys(SLOTN).map(k => `<div class="slot${p.equip[k] ? ' full' : ''}"><span>${SLOTN[k]}</span>${p.equip[k] ? `<b title="${esc(C(p.equip[k]).testo)}">${esc(C(p.equip[k]).nome)}</b>` : '<i>vuoto</i>'}</div>`).join('');
    const pct = Math.max(0, Math.min(100, p.pv / maxPV(p) * 100));
    const mods = p.mods.map(m => `<li>${esc(m.label)}${m.kind === 'scontri' ? ` · ${m.n} scontr${m.n === 1 ? 'o' : 'i'}` : m.kind === 'turni' ? ` · ${m.n} turn${m.n === 1 ? 'o' : 'i'}` : m.kind === 'turn' ? ' · questo turno' : ''}</li>`).join('');
    const serv = p.servants.map(s => `<li>${esc(s.name)} · PV ${s.pv}/${s.maxpv} · ATT ${fmt(s.att)} · ${s.dmg || (s.name === 'Imp' ? BAL.impDmg : BAL.servDmg)} danni</li>`).join('');
    return `<article class="sheet p${p.id}${p.id === G.cur ? ' cur' : ''}">
      <header><span class="pdot p${p.id}"></span><h3>${esc(p.name)}</h3><span class="who">${p.ai ? 'IA' : ''}</span></header>
      <p class="sub">${esc(p.race)} · ${p.classes.length ? esc(p.classes.join(' / ')) : 'senza classe'} · Livello ${p.level} · PE ${p.pe}/2</p>
      <div class="pvbar"><i style="width:${pct}%"></i></div>
      <div class="stats">${['pv', 'att', 'mov', 'ar'].map(k => statLine(p, k)).join('')}</div>
      <div class="clues" aria-label="Indizi ${p.clues} su 3">Indizi ${[0, 1, 2].map(i => `<span class="pip${i < p.clues ? ' on' : ''}"></span>`).join('')}${p.clues > 3 ? ` +${p.clues - 3}` : ''}</div>
      <div class="badges">${badges}</div>
      <div class="equip">${eq}</div>
      ${serv ? `<ul class="mini"><li class="h">Servitori</li>${serv}</ul>` : ''}
      ${mods ? `<ul class="mini"><li class="h">Effetti attivi</li>${mods}</ul>` : ''}
      <p class="counts">Mano ${p.hand.length} · Scarti ${p.discard.length}</p>
    </article>`;
  }).join('');
}
function combatBox() {
  const c = G.combat; if (!c) return '';
  const side = (x) => {
    const isP = !x.isCreature, mx = isP ? maxPV(x) : x.maxpv;
    const a = advOf(x, c);
    return `<div class="cside ${isP ? 'p' + x.id : 'foe'}"><b>${esc(x.name)}</b>
      <div class="pvbar"><i style="width:${Math.max(0, x.pv) / mx * 100}%"></i></div>
      <small>PV ${Math.max(0, x.pv)}/${mx} · ATT ${fmt(atkOf(x, c))} · AR ${arOf(x, c)} · ${dmgLabel(x)}${a > 0 ? ' · vantaggio' : a < 0 ? ' · svantaggio' : ''}</small></div>`;
  };
  return `<div class="combat"><div class="ctitle">${c.kind === 'boss' ? 'Scontro con il boss' : c.kind === 'pvp' ? 'Combattimento PvP' : c.kind === 'miniboss' ? 'Scontro con mini-boss' : 'Scontro'} · round ${c.round || 1}</div><div class="cgrid">${side(c.p)}<span class="vs">contro</span>${side(c.foe)}</div></div>`;
}
function renderAction() {
  const el = document.getElementById('action');
  let h = combatBox();
  if (G.over) {
    h += `<div class="over"><h2>${G.over.winner ? esc(G.over.winner.name) + ' vince!' : 'Partita conclusa'}</h2><p>${esc(G.over.why)}</p><div class="opts"><button class="btn" data-act="restart">Nuova partita con le stesse impostazioni</button><button class="btn ghost" data-nav="setup">Torna alla preparazione</button></div></div>`;
  } else if (pending && !pending.p.ai && isHidden(pending.p)) {
    h += `<div class="prompt"><p class="whose"><span class="pdot p${pending.p.id}"></span>Tocca a ${esc(pending.p.name)}</p><h2>Passa il dispositivo a ${esc(pending.p.name)}</h2><p>Le sue carte restano coperte finché non le mostra.</p><div class="opts"><button class="btn" data-act="reveal">Mostra la mia mano</button></div></div>`;
  } else if (pending && !pending.p.ai) {
    const multi = G.players.every(p => !p.ai);
    h += `<div class="prompt">${multi || pending.p.id !== G.cur ? `<p class="whose"><span class="pdot p${pending.p.id}"></span>Tocca a ${esc(pending.p.name)}</p>` : ''}<h2>${esc(pending.title)}</h2>${pending.text ? `<p>${esc(pending.text)}</p>` : ''}
      ${pending.hex ? '<p class="hint">Tocca una casella evidenziata sulla mappa.</p>' : ''}
      <div class="opts">${pending.options.map((o, i) => `<button class="btn${i ? ' ghost' : ''}" data-opt="${i}" ${o.disabled ? 'disabled' : ''} ${o.hint ? `title="${esc(o.hint)}"` : ''}>${esc(o.label)}</button>`).join('')}</div>
      ${pending.cards ? '<p class="hint">Oppure gioca una carta dalla tua mano qui sotto.</p>' : ''}</div>`;
  } else {
    h += `<div class="prompt think"><p>${esc(G.thinking || '…')}</p></div>`;
  }
  if (flashMsg) h += `<p class="flash" role="alert">${esc(flashMsg)}</p>`;
  el.innerHTML = h;
}
function cardHTML(id, { playable = null, reason = '' } = {}) {
  const c = C(id), d = DEF[baseId(id)];
  const slot = SLOT[baseId(id)] ? `<span class="slotl">${SLOT_LABEL[SLOT[baseId(id)]]}</span>` : '';
  return `<div class="card t-${c.tipo}${playable === false ? ' off' : ''}">
    <div class="ctop"><span>${c.tipo} · ${TIPO[c.tipo].replace('Trama ', '')}</span>${slot}</div>
    <div class="cdeck${c.cls ? ' cl' : ''}">${c.tipo === 'TC' ? 'Carta classe · si gioca a inizio partita' : c.cls ? 'Mazzetto ' + esc(c.cls) : 'Mazzo comune'}</div>
    <div class="cname">${esc(c.nome)}${id.includes('~') ? ' <small>(copia)</small>' : ''}</div>
    <div class="ctext">${esc(c.testo)}</div>
    ${c.orig && showOrig ? `<div class="corig"><b>Testo originale:</b> ${esc(c.orig)}</div>` : ''}
    ${d && d.nota ? `<div class="cnote"><b>Nel gioco:</b> ${esc(d.nota)}</div>` : ''}
    ${playable === true ? `<button class="btn sm" data-play="${id}">Gioca</button>` : playable === false && reason ? `<div class="why">${esc(reason)}</div>` : ''}
  </div>`;
}
function isHidden(p) { return G.players.every(x => !x.ai) && G.revealedFor !== p.id; }
function renderHand() {
  const p = handOwner();
  if (isHidden(p)) {
    document.getElementById('handtitle').innerHTML = `Mano di <b>${esc(p.name)}</b> <small>coperta</small>`;
    document.getElementById('hand').innerHTML = `<p class="empty">Le carte sono coperte. Passa il dispositivo a ${esc(p.name)}, poi tocca «Mostra la mia mano» qui sopra.</p>`;
    document.getElementById('discard').innerHTML = `<summary>Pila degli scarti di ${esc(p.name)} (${p.discard.length})</summary><div class="hand small">${p.discard.map(id => cardHTML(id)).join('') || '<p class="empty">Vuota.</p>'}</div>`;
    return;
  }
  const active = pending && pending.cards && pending.p === p && !p.ai;
  document.getElementById('handtitle').innerHTML = `Mano di <b>${esc(p.name)}</b> <small>${active ? `carte giocate ${G.combat && G.combat.foe === p ? G.combat.defCards + '/1 in difesa' : p.played + '/' + p.limit}` : ''}</small>`;
  document.getElementById('hand').innerHTML = p.hand.length ? p.hand.map(id => {
    if (!active) return cardHTML(id);
    const r = canPlay(p, id);
    return cardHTML(id, { playable: r === true, reason: r === true ? '' : r });
  }).join('') : '<p class="empty">Nessuna carta in mano.</p>';
  document.getElementById('discard').innerHTML = `<summary>Pila degli scarti di ${esc(p.name)} (${p.discard.length})</summary><div class="hand small">${p.discard.map(id => cardHTML(id)).join('') || '<p class="empty">Vuota.</p>'}</div>`;
}

// ---------- Catalogo ----------
let cardFilter = 'tutte', deckFilter = 'tutti', showOrig = false;
function renderCatalog() {
  const list = CARDS.filter(c => (cardFilter === 'tutte' || c.tipo === cardFilter) && (deckFilter === 'tutti' || (deckFilter === 'Caos' ? c.id.startsWith('CA-') : deckFilter === 'Comune' ? (!c.cls && c.tipo !== 'TC' && !c.id.startsWith('CA-')) : (c.cls === deckFilter || (c.tipo === 'TC' && CLASS_CARD[deckFilter] === c.id)))));
  showOrig = true;
  document.getElementById('catalog').innerHTML = list.map(c => cardHTML(c.id)).join('') || '<p class="empty">Nessuna carta.</p>';
  showOrig = false;
  document.getElementById('deckcount').textContent = `${list.length} carte`;
  document.querySelectorAll('[data-filter]').forEach(b => b.setAttribute('aria-pressed', b.dataset.filter === cardFilter));
}

// ---------- Eventi ----------
document.addEventListener('click', e => {
  const t = e.target.closest('button, [data-hex]');
  if (!t) return;
  if (t.dataset.nav) { view = t.dataset.nav; flashMsg = ''; render(); window.scrollTo(0, 0); return; }
  if (t.dataset.filter) { cardFilter = t.dataset.filter; renderCatalog(); return; }
  if (t.dataset.act === 'reveal' && pending) { G.revealedFor = pending.p.id; render(); return; }
  if (t.id === 'start') { if (G) G.over = G.over || { winner: null, why: 'abbandonata' }; dealDecks(); startGame(); return; }
  if (t.dataset.act === 'restart') { dealDecks(); startGame(); return; }
  if (t.dataset.opt !== undefined && pending) { flashMsg = ''; resolvePending(pending.options[+t.dataset.opt].value); return; }
  if (t.dataset.play && pending && pending.cards) { flashMsg = ''; resolvePending({ card: t.dataset.play }); return; }
  if (t.dataset.hex && pending && pending.hex && G.reach) {
    const [c, r] = t.dataset.hex.split(',').map(Number);
    if (G.reach.some(h => h.c === c && h.r === r)) { flashMsg = ''; resolvePending({ c, r }); }
    return;
  }
});
document.addEventListener('change', e => {
  const t = e.target;
  if (t.dataset.ai !== undefined) S.players[+t.dataset.ai].ai = t.value === '1';
  if (t.dataset.cls !== undefined) { const i = +t.dataset.cls; S.players[i].cls = t.value; renderSetup(); }
  if (t.dataset.race !== undefined) { S.players[+t.dataset.race].race = t.value; renderSetup(); }
  if (t.dataset.free !== undefined) { const [i, j] = t.dataset.free.split('-').map(Number); S.players[i].free[j] = t.value; }
  if (t.id === 'deckfilter') { deckFilter = t.value; renderCatalog(); }
  if (t.id === 'opt-speed') S.speed = +t.value;
  if (t.classList && t.classList.contains('opt-caos')) { BAL.caos = t.checked; document.querySelectorAll('.opt-caos').forEach(x => { x.checked = BAL.caos; }); }
  if (t.id === 'opt-n') {
    S.n = +t.value;
    const used = new Set();
    for (const sp of S.players.slice(0, S.n)) { if (used.has(sp.cls)) sp.cls = CLASSES.find(c => !used.has(c) && !S.players.slice(0, S.n).some(x => x.cls === c)); used.add(sp.cls); }
    renderSetup();
  }
});
document.addEventListener('input', e => { const t = e.target; if (t.dataset.name !== undefined) S.players[+t.dataset.name].name = t.value; });

// ---------- Simulazione di bilanciamento ----------
const SIM_DOMAIN = { size: [8, 10, 12, 14], spawns: [6, 8, 10, 12], die: [4, 6, 8] };
let SIM = { running: false, stop: false, rows: [], games: [] };
const ruleKey = r => `${r.size}×${r.size} · ${r.spawns} spawn · D${r.die}`;
const isStd = r => r.size === RULES_STD.size && r.spawns === RULES_STD.spawns && r.die === RULES_STD.die;
function randomPlayers(n) {
  const cls = shuffle([...CLASSES]).slice(0, n);
  const races = Object.keys(RACES);
  const list = cls.map((c, i) => ({ name: `IA ${i + 1}`, ai: true, cls: c, race: pick(races), free: [pick(['att', 'mov', 'ar', 'pv']), pick(['att', 'mov', 'ar', 'pv'])], deck: [] }));
  dealList(list);
  return list;
}
// Motore della simulazione: nessun disegno, nessuna attesa
async function simCore(N, playersMode, rulesMode, onProgress) {
  const res = { games: [], rows: [], errors: 0 };
  for (let g = 0; g < N && !SIM.stop; g++) {
    const n = playersMode === 'rand' ? 2 + Math.floor(Math.random() * 3) : +playersMode;
    const rules = rulesMode === 'rand' ? { size: pick(SIM_DOMAIN.size), spawns: pick(SIM_DOMAIN.spawns), die: pick(SIM_DOMAIN.die) } : { ...RULES_STD };
    const list = randomPlayers(n);
    createGame(list, true, rules);
    const game = G;
    try { await initClasses(); await gameLoop(); }
    catch (e) { res.errors++; console.error(e); game.over = { winner: null, why: 'errore', reason: 'errore' }; }
    const w = game.over && game.over.winner;
    const reason = (game.over && game.over.reason) || 'limite';
    const perPlayer = game.round / n;
    res.games.push({ n, rules, key: ruleKey(rules), rounds: game.round, perPlayer, reason, time: game.time, draw: !w, firstWins: !!w && w.id === game.first, winCls: w ? w.startCls : null });
    game.players.forEach((p, i) => res.rows.push({
      game: g + 1, n, key: ruleKey(rules), size: rules.size, spawns: rules.spawns, die: rules.die,
      seat: (i - game.first + n) % n + 1, cls: p.startCls, race: p.race, bonus: list[i].free.slice(0, RACES[p.race].free).join('+'),
      win: w === p ? 1 : 0, draw: w ? 0 : 1, rounds: game.round, perPlayer, level: p.level, clues: p.clues, out: p.out ? 1 : 0, cards: game.stats.played[i], reason,
    }));
    G = null;
    if (onProgress && (g % 20 === 19 || g === N - 1)) { onProgress(g + 1, N); await sleep(0); }
  }
  applyRules(RULES_STD);
  return res;
}
const TEMPO_N = { turno: 'Passaggio del turno', dado: 'Tiro di dado', carta: 'Carta giocata', movimento: 'Movimento della pedina', casella: 'Casella scoperta', scontro: 'Inizio di uno scontro', attacco: 'Attacco e danni', livello: 'Salita di livello', sconfitta: 'Sconfitta e respawn' };
function renderTempo() {
  const el = document.getElementById('sim-tempo'); if (!el || el.dataset.ok) return; el.dataset.ok = 1;
  el.innerHTML = `<summary>Tempo di gioco umano: secondi per azione</summary><p class="hint">La simulazione somma questi tempi per stimare quanto dura una partita. «Al tavolo» è il ritmo del gioco da tavolo; «Digitale» è il ritmo di questa pagina, dove dadi e conti li fa il computer, quindi la partita dura meno. Puoi anche cambiare i singoli tempi.</p><label class="fld"><span>Ritmo</span><select id="tempo-preset"><option value="tavolo" selected>Al tavolo</option><option value="digitale">Digitale</option><option value="custom">Personalizzato</option></select></label><div class="tempogrid">${Object.keys(TEMPO).map(k => `<label class="fld"><span>${TEMPO_N[k]}</span><input type="number" min="0" max="300" step="1" data-tempo="${k}" value="${TEMPO[k]}"></label>`).join('')}</div>`;
  const sel = el.querySelector('#tempo-preset');
  sel.addEventListener('change', () => { const T = TEMPI[sel.value]; if (T) el.querySelectorAll('[data-tempo]').forEach(i => { i.value = T[i.dataset.tempo]; }); });
  el.querySelectorAll('[data-tempo]').forEach(i => i.addEventListener('input', () => { sel.value = 'custom'; }));
}
async function runSim() {
  document.querySelectorAll('[data-tempo]').forEach(i => { const v = +i.value; if (isFinite(v) && v >= 0) TEMPO[i.dataset.tempo] = v; });
  const tp = document.getElementById('tempo-preset'); const tKey = tp ? tp.value : 'tavolo'; const tLabel = { tavolo: 'al tavolo', digitale: 'digitale', custom: 'personalizzato' }[tKey];
  const N = Math.max(1, Math.min(50000, +document.getElementById('sim-n').value || 100));
  SIM = { running: true, stop: false, rows: [], games: [], errors: 0, t0: Date.now(), rulesMode: document.getElementById('sim-rules').value, tempoKey: tKey, tempoLabel: tLabel };
  pending = null; GEN++; G = null;
  document.querySelector('[data-nav="game"]').hidden = true;
  simUI(0, N);
  const r = await simCore(N, document.getElementById('sim-players').value, SIM.rulesMode, simUI);
  Object.assign(SIM, r, { running: false });
  simUI(SIM.games.length, N);
  renderSimResults();
}
function simUI(done = 0, total = 0) {
  const b = document.getElementById('sim-run'); b.textContent = SIM.running ? 'Ferma la simulazione' : 'Avvia la simulazione';
  const pr = document.getElementById('sim-progress');
  pr.hidden = !SIM.running && !done;
  pr.innerHTML = `<div class="pvbar"><i style="width:${total ? done / total * 100 : 0}%"></i></div><small>${done} / ${total} partite${SIM.running ? '…' : ' completate'} · ${((Date.now() - SIM.t0) / 1000).toFixed(1)} s${SIM.errors ? ` · ${SIM.errors} errori` : ''}</small>`;
}
const pct = x => (x * 100).toFixed(1).replace('.', ',') + '%';
const num = (x, d = 2) => (isFinite(x) ? x : 0).toFixed(d).replace('.', ',');
function groupStats(rows, keyFn) {
  const m = new Map();
  for (const r of rows) {
    const k = keyFn(r); if (k == null) continue;
    const s = m.get(k) || { k, games: 0, wins: 0, exp: 0 };
    s.games++; s.wins += r.win; s.exp += r.draw ? 0 : 1 / r.n; m.set(k, s);
  }
  return [...m.values()].map(s => ({ ...s, rate: s.wins / s.games, idx: s.exp ? s.wins / s.exp : 0 }));
}
// Statistiche della distribuzione: media, deviazione, asimmetria, curtosi, aderenza alla gaussiana
function distStats(vals) {
  const n = vals.length; if (n < 3) return null;
  const mean = vals.reduce((a, v) => a + v, 0) / n;
  const sd = Math.sqrt(vals.reduce((a, v) => a + (v - mean) ** 2, 0) / (n - 1)) || 1e-9;
  const skew = vals.reduce((a, v) => a + ((v - mean) / sd) ** 3, 0) / n;
  const kurt = vals.reduce((a, v) => a + ((v - mean) / sd) ** 4, 0) / n - 3;
  const sorted = [...vals].sort((a, b) => a - b);
  // classi larghe un numero intero di turni: i turni a testa sono frazioni (k/2, k/3, k/4) e classi intere non creano picchi finti
  const lo = Math.floor(sorted[0]), hi = sorted[n - 1];
  const nb = Math.max(6, Math.min(30, Math.round(Math.sqrt(n))));
  const w = Math.max(1, Math.round((hi - lo) / nb));
  const bins = Array.from({ length: Math.ceil((hi - lo) / w) + 1 }, (_, i) => ({ x0: lo + i * w, x1: lo + (i + 1) * w, c: 0 }));
  for (const v of vals) bins[Math.min(bins.length - 1, Math.floor((v - lo) / w))].c++;
  const cdf = x => 0.5 * (1 + erf((x - mean) / (sd * Math.SQRT2)));
  let ssr = 0, sst = 0; const meanC = n / bins.length;
  for (const b of bins) { b.e = n * (cdf(b.x1) - cdf(b.x0)); ssr += (b.c - b.e) ** 2; sst += (b.c - meanC) ** 2; }
  const r2 = sst ? Math.max(0, 1 - ssr / sst) : 0;
  return { n, mean, sd, skew, kurt, bins, w, lo, r2 };
}
function erf(x) { const s = Math.sign(x); x = Math.abs(x); const t = 1 / (1 + 0.3275911 * x); const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
// Punteggio di equilibrio di un gruppo di partite (0-100)
function balanceOf(games, rows) {
  const ds = distStats(games.map(g => g.perPlayer));
  const cl = groupStats(rows, r => r.cls).filter(s => s.games >= 5);
  const sdIdx = cl.length > 1 ? Math.sqrt(cl.reduce((a, s) => a + (s.idx - 1) ** 2, 0) / cl.length) : 1;
  const firstIdx = games.reduce((a, g) => a + (g.firstWins ? g.n : 0), 0) / Math.max(1, games.filter(g => !g.draw).length);
  const draws = games.filter(g => g.draw).length / games.length;
  const parts = { classi: Math.max(0, 1 - sdIdx), gauss: ds ? ds.r2 : 0, turno: Math.max(0, 1 - Math.abs(firstIdx - 1)), finite: 1 - draws };
  const score = 100 * (0.35 * parts.classi + 0.25 * parts.gauss + 0.25 * parts.turno + 0.15 * parts.finite);
  return { score, parts, ds, sdIdx, firstIdx, draws };
}
function idxCell(s, min) {
  const cls = s.games < min ? 'muted' : s.idx >= 1.25 ? 'hi' : s.idx <= 0.8 ? 'lo' : '';
  return `<td class="num ${cls}">${num(s.idx)}</td>`;
}
function statTable(title, list, label, min = 1, note = '') {
  return `<section class="stbox"><h3>${title}</h3>${note ? `<p class="hint">${note}</p>` : ''}<div class="tablewrap"><table><thead><tr><th>${label}</th><th class="num">Partite</th><th class="num">Vittorie</th><th class="num">% vittorie</th><th class="num">Indice</th></tr></thead><tbody>${list.map(s => `<tr><td>${esc(s.k)}</td><td class="num">${s.games}</td><td class="num">${s.wins}</td><td class="num">${pct(s.rate)}</td>${idxCell(s, min)}</tr>`).join('')}</tbody></table></div></section>`;
}
// Grafico a punti: ogni punto è una partita (o un gruppo di partite), con la gaussiana di riferimento
function dotChart(ds) {
  const W = 760, H = 300, L = 44, R = 16, T = 16, B = 44;
  const maxC = Math.max(...ds.bins.map(b => Math.max(b.c, b.e)));
  const per = Math.max(1, Math.ceil(maxC / 24));
  const rows = Math.ceil(maxC / per);
  const x0 = ds.lo, x1 = ds.lo + ds.bins.length * ds.w;
  const X = v => L + (v - x0) / (x1 - x0) * (W - L - R);
  const bw = (W - L - R) / ds.bins.length;
  const step = (H - T - B) / Math.max(rows, 1);
  const rad = Math.max(2.2, Math.min(bw / 2 - 1.5, step / 2 - 1, 7));
  const Y = c => H - B - c / per * step;
  let dots = '';
  ds.bins.forEach((b, i) => {
    const k = Math.round(b.c / per);
    const cx = L + bw * (i + 0.5);
    for (let j = 0; j < k; j++) dots += `<circle cx="${cx.toFixed(1)}" cy="${(H - B - step * (j + 0.5)).toFixed(1)}" r="${rad.toFixed(1)}" class="dot"/>`;
    dots += `<rect x="${(L + bw * i).toFixed(1)}" y="${T}" width="${bw.toFixed(1)}" height="${H - T - B}" class="hit"><title>${num(b.x0, 1)}–${num(b.x1, 1)} turni a testa: ${b.c} partite (la gaussiana ne prevede ${num(b.e, 1)})</title></rect>`;
  });
  let path = '';
  for (let i = 0; i <= 120; i++) {
    const v = x0 + (x1 - x0) * i / 120;
    const e = ds.n * ds.w * Math.exp(-0.5 * ((v - ds.mean) / ds.sd) ** 2) / (ds.sd * Math.sqrt(2 * Math.PI));
    path += (i ? 'L' : 'M') + X(v).toFixed(1) + ',' + Math.max(T, Y(e)).toFixed(1);
  }
  const ticks = []; const tStep = Math.max(1, Math.round((x1 - x0) / 8));
  for (let v = Math.ceil(x0); v <= x1; v += tStep) ticks.push(v);
  return `<svg viewBox="0 0 ${W} ${H}" class="dotchart" role="img" aria-label="Distribuzione della durata delle partite con curva gaussiana di riferimento">
    <line x1="${L}" y1="${H - B}" x2="${W - R}" y2="${H - B}" class="axis"/>
    ${ticks.map(v => `<line x1="${X(v)}" y1="${H - B}" x2="${X(v)}" y2="${H - B + 4}" class="axis"/><text x="${X(v)}" y="${H - B + 17}" class="tick">${v}</text>`).join('')}
    <text x="${(L + W - R) / 2}" y="${H - 6}" class="tick">turni giocati da ciascun giocatore</text>
    <line x1="${X(ds.mean)}" y1="${T}" x2="${X(ds.mean)}" y2="${H - B}" class="meanline"/><text x="${X(ds.mean) + 4}" y="${T + 10}" class="tick start">media ${num(ds.mean, 1)}</text>
    ${dots}
    <path d="${path}" class="curve"/>
  </svg>
  <div class="chartlegend"><span><i class="lg-dot"></i>partite (ogni punto = ${per} ${per === 1 ? 'partita' : 'partite'})</span><span><i class="lg-line"></i>curva gaussiana con stessa media e deviazione</span></div>`;
}
function distBlock(games, rows, label) {
  const bal = balanceOf(games, rows), ds = bal.ds;
  if (!ds) return '<p class="hint">Servono almeno 3 partite.</p>';
  const shape = Math.abs(ds.skew) < 0.3 ? 'quasi simmetrica' : ds.skew > 0 ? 'con una coda di partite lunghe' : 'con una coda di partite brevi';
  return `<div class="distgrid"><div class="chartwrap">${dotChart(ds)}</div>
    <div class="distfacts">
      <div class="fact"><b>${num(ds.r2 * 100, 0)}%</b><span>aderenza alla gaussiana (R² tra punti e curva)</span></div>
      <div class="fact"><b>${num(ds.mean, 1)} ± ${num(ds.sd, 1)}</b><span>turni a testa, media e deviazione</span></div>
      <div class="fact"><b>${num(ds.skew, 2)}</b><span>asimmetria: ${shape} (0 = gaussiana)</span></div>
      <div class="fact"><b>${num(ds.kurt, 2)}</b><span>curtosi in eccesso (0 = gaussiana, sopra 0 = troppe partite estreme)</span></div>
      <div class="fact"><b>${num(bal.score, 0)}</b><span>punteggio di equilibrio di ${esc(label)}</span></div>
    </div></div>`;
}
function renderSimResults() {
  const rows = SIM.rows, games = SIM.games;
  if (!games.length) return;
  const out = document.getElementById('sim-results');
  const byN = [2, 3, 4].map(n => { const gs = games.filter(g => g.n === n); return { n, count: gs.length, avg: gs.length ? gs.reduce((a, g) => a + g.perPlayer, 0) / gs.length : 0, first: gs.length ? gs.filter(g => g.firstWins).length / gs.length : 0 }; }).filter(x => x.count);
  const reasons = {}; for (const g of games) reasons[g.reason] = (reasons[g.reason] || 0) + 1;
  const RN = { boss: 'Boss sconfitto', beholder: 'Beholder sconfitto', zarko: 'Ultimo rimasto (Zarko)', limite: 'Interrotta per troppi turni', errore: 'Errore' };
  const cls = groupStats(rows, r => r.cls).sort((a, b) => b.idx - a.idx);
  const race = groupStats(rows, r => r.race).sort((a, b) => b.idx - a.idx);
  const pairs = groupStats(rows, r => r.cls + ' · ' + r.race).filter(s => s.games >= 8).sort((a, b) => b.idx - a.idx);
  const seat = groupStats(rows, r => r.seat + '° di turno').sort((a, b) => a.k.localeCompare(b.k));
  const cardRows = [];
  for (const r of rows) for (const id of new Set(r.cards)) cardRows.push({ ...r, card: id });
  const cards = groupStats(cardRows, r => r.card).map(s => ({ ...s, k: s.k + ' · ' + CARD[s.k].nome }));
  const plays = {}; for (const r of rows) for (const id of r.cards) plays[id] = (plays[id] || 0) + 1;
  const minC = Math.max(10, Math.round(games.length * 0.03));
  const cardsOk = cards.filter(s => s.games >= minC).sort((a, b) => b.idx - a.idx);
  const never = CARDS.filter(c => c.tipo !== 'TC' && !plays[c.id]).map(c => c.nome);
  const avg = games.reduce((a, g) => a + g.perPlayer, 0) / games.length;
  // combinazioni di regole
  const combos = [];
  const keys = [...new Set(games.map(g => g.key))];
  for (const k of keys) {
    const gs = games.filter(g => g.key === k), rs = rows.filter(r => r.key === k);
    const b = balanceOf(gs, rs);
    combos.push({ k, rules: gs[0].rules, games: gs.length, b, avg: gs.reduce((a, g) => a + g.perPlayer, 0) / gs.length });
  }
  const minG = Math.max(20, Math.round(games.length / Math.max(1, keys.length) * 0.5));
  const ranked = combos.filter(c => c.games >= minG).sort((a, b) => b.b.score - a.b.score);
  const best = ranked[0];
  const param = (name, fn, vals, fmtv) => `<section class="stbox"><h3>${name}</h3><div class="tablewrap"><table><thead><tr><th>Valore</th><th class="num">Partite</th><th class="num">Turni a testa</th><th class="num">Gaussiana</th><th class="num">Equilibrio</th></tr></thead><tbody>${vals.map(v => { const gs = games.filter(g => fn(g) === v); if (!gs.length) return ''; const rs = rows.filter(r => fn(r) === v); const b = balanceOf(gs, rs); return `<tr><td>${fmtv(v)}</td><td class="num">${gs.length}</td><td class="num">${num(gs.reduce((a, g) => a + g.perPlayer, 0) / gs.length, 1)}</td><td class="num">${num(b.ds ? b.ds.r2 * 100 : 0, 0)}%</td><td class="num">${num(b.score, 0)}</td></tr>`; }).join('')}</tbody></table></div></section>`;
  const multi = keys.length > 1;
  out.innerHTML = `
    <div class="tiles">
      <div class="tile"><b>${games.length}</b><span>partite simulate</span></div>
      <div class="tile"><b>${num(avg, 1)}</b><span>turni medi a testa</span></div>
      <div class="tile"><b>${pct((reasons.limite || 0) / games.length)}</b><span>interrotte senza vincitore</span></div>
      <div class="tile"><b>${SIM.errors}</b><span>errori del motore</span></div>
      <div class="tile"><b>${num(games.reduce((a, g) => a + (g.time ? g.time.tot : 0), 0) / games.length / 60, 0)} min</b><span>durata media stimata (${esc(SIM.tempoLabel || 'al tavolo')})</span></div>
    </div>
    ${games[0].time ? `<section class="stbox"><h3>Tempo di gioco stimato</h3><p class="hint">Minuti con il ritmo «${esc(SIM.tempoLabel || 'al tavolo')}», preparazione esclusa. <b>Inizio</b>: finché nessuno ha un indizio. <b>Centro</b>: dal primo indizio a quando qualcuno individua il tesoro. <b>Finale</b>: da lì alla vittoria.</p><div class="tablewrap"><table><thead><tr><th>Giocatori</th><th class="num">Partite</th><th class="num">Media</th><th class="num">Mediana</th><th class="num">10% / 90%</th><th class="num">Inizio</th><th class="num">Centro</th><th class="num">Finale</th></tr></thead><tbody>${[2, 3, 4].map(n => { const gs = games.filter(g => g.n === n && g.time); if (!gs.length) return ''; const m = f => num(gs.reduce((a, g) => a + f(g), 0) / gs.length / 60, 1); const t = gs.map(g => g.time.tot / 60).sort((a, b) => a - b); const q = x => num(t[Math.min(t.length - 1, Math.floor(t.length * x))], 0); return `<tr><td>${n}</td><td class="num">${gs.length}</td><td class="num">${m(g => g.time.tot)}</td><td class="num">${q(.5)}</td><td class="num">${q(.1)} / ${q(.9)}</td><td class="num">${m(g => g.time.early)}</td><td class="num">${m(g => g.time.mid)}</td><td class="num">${m(g => g.time.late)}</td></tr>`; }).join('')}</tbody></table></div><p class="hint">${(() => { const alt = SIM.tempoKey === 'digitale' ? ['al tavolo', TEMPI.tavolo] : ['digitale', TEMPI.digitale]; const r = [2, 3, 4].map(n => { const gs = games.filter(g => g.n === n && g.time && g.time.n); return gs.length ? `${num(gs.reduce((a, g) => a + timeWith(g.time, alt[1]).tot, 0) / gs.length / 60, 1)} min in ${n}` : ''; }).filter(Boolean); return r.length ? `Con il ritmo ${alt[0]}: ${r.join(', ')}. La versione digitale dura meno del gioco da tavolo perché dadi, conti e segnalini li gestisce il computer.` : ''; })()}</p></section>` : ''}
    ${multi && best ? `<section class="stbox bestbox"><h3>Impostazione più bilanciata: ${esc(best.k)}</h3><p>Punteggio di equilibrio ${num(best.b.score, 0)} su 100, su ${best.games} partite. Aderenza alla gaussiana ${num(best.b.ds.r2 * 100, 0)}%, durata media ${num(best.avg, 1)} turni a testa, vantaggio di chi inizia ${num(best.b.firstIdx, 2)} (1,00 = nessuno).${isStd(best.rules) ? ' Coincide con le regole attuali.' : ` Le regole attuali (${ruleKey(RULES_STD)}) sono ${(() => { const i = ranked.findIndex(c => isStd(c.rules)); return i >= 0 ? `al ${i + 1}° posto su ${ranked.length}` : 'fuori classifica per pochi dati'; })()}.`}</p></section>` : ''}
    <section class="stbox"><h3>Distribuzione delle partite</h3>
      <p class="hint">Ogni punto è una partita, posizionata secondo quanti turni ha giocato ciascun giocatore prima della fine. Uso la durata a testa perché è confrontabile tra partite a 2, 3 e 4 giocatori ed è quello che decide se una partita sembra troppo corta o troppo lunga. Più i punti seguono la curva, più le partite hanno una durata prevedibile, con poche partite lampo e poche infinite.</p>
      ${multi ? `<label class="hint">Mostra <select id="dist-sel"><option value="">Tutte le partite</option>${combos.slice().sort((a, b) => b.b.score - a.b.score).map(c => `<option value="${esc(c.k)}">${esc(c.k)} (${c.games})</option>`).join('')}</select></label>` : ''}
      <div id="dist-box">${distBlock(games, rows, 'tutte le partite')}</div>
    </section>
    <p class="hint">L'<b>indice</b> confronta le vittorie con quelle attese se tutto fosse bilanciato (1 su 2, 3 o 4 giocatori secondo la partita). 1,00 = in equilibrio, sopra 1,25 vince troppo (verde), sotto 0,80 vince troppo poco (rosso). Le righe grigie hanno pochi dati. Il <b>punteggio di equilibrio</b> (0-100) pesa per il 35% quanto le classi sono alla pari, per il 25% l'aderenza alla gaussiana, per il 25% l'assenza di vantaggio per chi inizia e per il 15% le partite concluse con un vincitore.</p>
    ${multi ? `<section class="stbox"><h3>Tutte le combinazioni di regole</h3><p class="hint">Ordinate per punteggio di equilibrio. Solo combinazioni con almeno ${minG} partite.</p><div class="tablewrap"><table><thead><tr><th>Regole</th><th class="num">Partite</th><th class="num">Turni a testa</th><th class="num">Classi alla pari</th><th class="num">Gaussiana</th><th class="num">Chi inizia</th><th class="num">Equilibrio</th></tr></thead><tbody>${ranked.map(c => `<tr${isStd(c.rules) ? ' class="std"' : ''}><td>${esc(c.k)}${isStd(c.rules) ? ' (attuali)' : ''}</td><td class="num">${c.games}</td><td class="num">${num(c.avg, 1)}</td><td class="num">${num(c.b.parts.classi * 100, 0)}%</td><td class="num">${num(c.b.ds ? c.b.ds.r2 * 100 : 0, 0)}%</td><td class="num">${num(c.b.firstIdx, 2)}</td><td class="num"><b>${num(c.b.score, 0)}</b></td></tr>`).join('')}</tbody></table></div></section>
    <div class="stgrid">${param('Dimensione della plancia', g => g.size || g.rules.size, SIM_DOMAIN.size, v => `${v}×${v}`)}${param('Punti di spawn', g => g.spawns || g.rules.spawns, SIM_DOMAIN.spawns, v => `${v} (D${v})`)}${param('Dado di movimento', g => g.die || g.rules.die, SIM_DOMAIN.die, v => `D${v} + MOV`)}</div>` : ''}
    <div class="stgrid">
      ${statTable('Classi', cls, 'Classe', 30)}
      ${statTable('Razze', race, 'Razza', 30)}
      <section class="stbox"><h3>Numero di giocatori</h3><div class="tablewrap"><table><thead><tr><th>Giocatori</th><th class="num">Partite</th><th class="num">Turni a testa</th><th class="num">Vince chi inizia</th><th class="num">Atteso</th></tr></thead><tbody>${byN.map(x => `<tr><td>${x.n}</td><td class="num">${x.count}</td><td class="num">${num(x.avg, 1)}</td><td class="num">${pct(x.first)}</td><td class="num">${pct(1 / x.n)}</td></tr>`).join('')}</tbody></table></div></section>
      ${statTable('Ordine di turno', seat, 'Posizione', 30)}
      <section class="stbox"><h3>Come finiscono le partite</h3><div class="tablewrap"><table><tbody>${Object.entries(reasons).sort((a, b) => b[1] - a[1]).map(([k, v]) => `<tr><td>${RN[k] || k}</td><td class="num">${v}</td><td class="num">${pct(v / games.length)}</td></tr>`).join('')}</tbody></table></div></section>
      ${statTable('Coppie classe e razza: le più forti', pairs.slice(0, 10), 'Coppia', 8, 'Solo coppie con almeno 8 partite.')}
      ${statTable('Coppie classe e razza: le più deboli', pairs.slice(-10).reverse(), 'Coppia', 8)}
      ${statTable('Carte più decisive', cardsOk.slice(0, 12), 'Carta', minC, `Vittorie di chi ha giocato la carta almeno una volta. Solo carte giocate in almeno ${minC} partite.`)}
      ${statTable('Carte meno decisive', cardsOk.slice(-12).reverse(), 'Carta', minC)}
    </div>
    ${never.length ? `<p class="hint">Mai giocate dall'IA: ${esc(never.join(', '))}.</p>` : ''}
    <section class="stbox"><h3>Esporta i dati in CSV</h3><p class="hint">Una riga per giocatore per partita, separatore punto e virgola (si apre in Excel). Copia il testo e incollalo in un file .csv.</p>
      <div class="opts row"><button class="btn" data-act="copycsv">Copia CSV</button><span id="copyok" class="hint"></span></div>
      <textarea id="sim-csv" readonly rows="6"></textarea></section>`;
  const head = 'partita;giocatori;plancia;spawn;dado_movimento;ordine_turno;classe;razza;bonus_scelti;vittoria;pareggio;turni_partita;turni_a_testa;livello_finale;indizi;eliminato;fine_partita;carte_giocate';
  document.getElementById('sim-csv').value = [head, ...rows.map(r => [r.game, r.n, r.size, r.spawns, r.die, r.seat, r.cls, r.race, r.bonus, r.win, r.draw, r.rounds, num(r.perPlayer, 2), r.level, r.clues, r.out, r.reason, r.cards.join('|')].join(';'))].join('\n');
}
document.addEventListener('change', e => {
  if (e.target.id !== 'dist-sel') return;
  const k = e.target.value;
  const gs = k ? SIM.games.filter(g => g.key === k) : SIM.games, rs = k ? SIM.rows.filter(r => r.key === k) : SIM.rows;
  document.getElementById('dist-box').innerHTML = distBlock(gs, rs, k || 'tutte le partite');
});
document.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  if (t.id === 'sim-run') { if (SIM.running) SIM.stop = true; else runSim(); }
  if (t.dataset.act === 'copycsv') {
    const ta = document.getElementById('sim-csv');
    const ok = () => { document.getElementById('copyok').textContent = 'Copiato.'; };
    try { navigator.clipboard.writeText(ta.value).then(ok, () => { ta.select(); document.getElementById('copyok').textContent = 'Testo selezionato: copialo con Ctrl+C.'; }); }
    catch (err) { ta.select(); }
  }
});

renderTempo();
dealDecks();
renderCatalog();
render();
