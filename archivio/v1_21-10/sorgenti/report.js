globalThis.AFTER = (r) => {
  // card impact
  const cs = new Map();
  for (const row of r.rows) { if (row.draw) continue; for (const id of new Set(row.cards)) { const s = cs.get(id) || { id, n: 0, w: 0, e: 0 }; s.n++; s.w += row.win; s.e += 1 / row.n; cs.set(id, s); } }
  const arr = [...cs.values()].filter(s => s.n >= 40).map(s => ({ ...s, idx: s.w / s.e })).sort((a, b) => b.idx - a.idx);
  console.log('CARDS top:', arr.slice(0, 14).map(s => `${s.id}(${CARD[s.id].cls ? CARD[s.id].cls.slice(0, 4) : 'com'}) ${s.idx.toFixed(2)}/${s.n}`).join(' '));
  console.log('CARDS low:', arr.slice(-14).map(s => `${s.id}(${CARD[s.id].cls ? CARD[s.id].cls.slice(0, 4) : 'com'}) ${s.idx.toFixed(2)}/${s.n}`).join(' '));
  const all = CARDS.filter(c => c.tipo !== 'TC').map(c => c.id); console.log('rarely played:', all.filter(id => !cs.has(id) || cs.get(id).n < 40).join(' '));
  // matchup 2p
  if (process.env.MU) {
    const m = {}; for (const g of r.games.keys()) { } 
    const byGame = {}; r.rows.forEach(x => (byGame[x.game] = byGame[x.game] || []).push(x));
    for (const k in byGame) { const rs = byGame[k]; if (rs.length !== 2) continue; const [a, b] = rs; for (const [x, y] of [[a, b], [b, a]]) { const key = x.cls + '>' + y.cls; m[key] = m[key] || { n: 0, w: 0 }; m[key].n++; m[key].w += x.win; } }
    const cl = CLASSES; let worst = [];
    console.log('MU     ' + cl.map(c => c.slice(0, 5).padStart(6)).join(''));
    for (const a of cl) console.log(a.slice(0, 6).padEnd(7) + cl.map(b => { const s = m[a + '>' + b]; if (!s || a === b) return '     -'; const v = s.w / s.n; worst.push([a, b, v, s.n]); return (v * 100).toFixed(0).padStart(6); }).join(''));
    worst.sort((x, y) => y[2] - x[2]); console.log('worst MU:', worst.slice(0, 8).map(w => `${w[0]}>${w[1]} ${(w[2] * 100).toFixed(0)}%(${w[3]})`).join(' '));
  }
};
globalThis.AFTER0 = globalThis.AFTER;
globalThis.AFTER = (r) => {
  AFTER0(r);
  // within-class lift: win rate of class players who played card vs who did not
  const out = [];
  for (const cl of CLASSES) {
    const rs = r.rows.filter(x => x.cls === cl && !x.draw); if (!rs.length) continue;
    const ids = CARDS.filter(c => c.cls === cl).map(c => c.id);
    const parts = ids.map(id => { const a = rs.filter(x => x.cards.includes(id)), b = rs.filter(x => !x.cards.includes(id)); const wa = a.reduce((s, x) => s + x.win, 0) / (a.length || 1), wb = b.reduce((s, x) => s + x.win, 0) / (b.length || 1); return `${id} ${(wa * 100).toFixed(0)}/${(wb * 100).toFixed(0)}(${a.length})`; });
    out.push(cl.padEnd(10) + parts.join('  '));
  }
  console.log(out.join('\n'));
};
