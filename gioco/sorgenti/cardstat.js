globalThis.AFTER = r => {
  const pl = {}, win = {}; const base = r.rows.reduce((a, x) => a + x.win, 0) / r.rows.length;
  for (const x of r.rows) for (const id of new Set(x.cards)) { pl[id] = (pl[id] || 0) + 1; win[id] = (win[id] || 0) + x.win; }
  const N = r.games.length;
  console.log('CARDS ' + Object.keys(CARD).filter(id => !id.startsWith('TC')).map(id => `${id} ${CARD[id].nome.slice(0, 14)}: ${((pl[id] || 0) / N).toFixed(2)} g/partita, vince ${pl[id] ? (win[id] / pl[id] / base).toFixed(2) : '-'}`).join('\n'));
};
