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
