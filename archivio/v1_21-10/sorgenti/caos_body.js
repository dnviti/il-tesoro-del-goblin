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
const commonPool = () => COMMON.filter(id => BAL.caos || !id.startsWith('CA-'));
// pesca una carta comune che nessuno ha (né in mano, né negli scarti, né equipaggiata)
function drawCard(p) {
  const used = new Set(G.players.flatMap(x => [...x.hand, ...x.discard, ...equipped(x)].map(baseId)));
  const id = shuffle(commonPool().filter(id => !used.has(id) && C(id).tipo !== 'TM'))[0];
  if (id) { p.hand.push(id); log(`${p.name} pesca «${C(id).nome}».`, 'good'); } else log('Non ci sono carte da pescare.');
}
async function chaosEvent(p) {
  const tw = twinOf(p.pos);
  if (tileAt(tw).type === 'evento' && freeHex(tw, p)) {
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
