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
