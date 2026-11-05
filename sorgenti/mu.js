Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
globalThis.AFTER = (r) => {
  const m = {}; const byGame = {}; r.rows.forEach(x => (byGame[x.game] = byGame[x.game] || []).push(x));
  for (const k in byGame) { const rs = byGame[k]; if (rs.length !== 2) continue; const [a, b] = rs; for (const [x, y] of [[a, b], [b, a]]) { const key = x.cls + '>' + y.cls; m[key] = m[key] || { n: 0, w: 0 }; m[key].n++; m[key].w += x.win; } }
  require('fs').writeFileSync(process.env.MUOUT, JSON.stringify(m));
};
