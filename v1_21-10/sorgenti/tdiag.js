Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
globalThis.AFTER = r => {
  for (const n of [2, 3, 4]) {
    const gs = r.games.filter(g => g.n === n), k = gs.length;
    const out = {};
    for (const st of ['early', 'mid', 'late']) { const c = {}; gs.forEach(g => { for (const x in g.time.n[st]) c[x] = (c[x] || 0) + g.time.n[st][x] / k; }); out[st] = Object.entries(c).map(([x, v]) => `${x} ${v.toFixed(1)}`).join(', '); }
    const mk = {}; gs.forEach(g => { for (const x in g.time.m) (mk[x] = mk[x] || []).push(g.time.m[x] / 60); });
    console.log(`${n}p`, JSON.stringify(out));
    console.log('  marks(min, % games):', Object.entries(mk).sort().map(([x, v]) => `${x} ${(v.reduce((a, b) => a + b, 0) / v.length).toFixed(1)} (${Math.round(v.length / k * 100)}%)`).join(' | '));
  }
};
