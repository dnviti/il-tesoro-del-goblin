// valore delle carte in mano all'inizio: vittorie / attese (1/n), carte di classe rispetto alla loro classe
globalThis.AFTER = r => {
  const fs = require('fs'); const by = {}, cls = {};
  for (const x of r.rows) { const c = cls[x.cls] = cls[x.cls] || [0, 0]; c[0] += x.win; c[1] += 1 / x.n; }
  for (const x of r.rows) {
    const cf = cls[x.cls][0] / cls[x.cls][1];
    for (const id of new Set(x.hand0)) { const b = by[id] = by[id] || [0, 0, 0]; b[0] += x.win; b[1] += cf / x.n; b[2]++; }
  }
  const out = {}; for (const id in by) out[id] = +(by[id][0] / by[id][1]).toFixed(3);
  fs.writeFileSync(process.env.OUTV || 'draft_val.json', JSON.stringify(out));
  console.log(Object.entries(out).sort((a, b) => b[1] - a[1]).map(([id, v]) => `${id} ${CARD[id].nome.slice(0, 18)} ${v} (${by[id][2]})`).join('\n'));
};
Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
