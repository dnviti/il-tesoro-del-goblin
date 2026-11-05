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
