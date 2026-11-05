// ---- harness main ----
(async () => {
  const A = process.argv; const N = +A[2] || 2000, pm = A[3] || 'rand', rm = A[4] || 'std';
  if (A[5]) eval(require('fs').readFileSync(A[5], 'utf8'));
  SIM = { running: true, stop: false };
  const t0 = Date.now();
  const r = await simCore(N, pm, rm, null);
  const b = balanceOf(r.games, r.rows);
  const f = v => typeof v === 'number' ? +v.toFixed(3) : v;
  console.log(JSON.stringify({ secs: (Date.now() - t0) / 1000, errors: r.errors, score: b.score, parts: b.parts, mean: b.ds.mean, sd: b.ds.sd, skew: b.ds.skew, kurt: b.ds.kurt, r2: b.ds.r2, first: b.firstIdx, draws: b.draws }, (k, v) => f(v)));
  const show = (t, g) => console.log(t + ': ' + g.sort((a, b) => b.idx - a.idx).map(s => `${s.k} ${s.idx.toFixed(2)}`).join(' | '));
  show('CLS', groupStats(r.rows, x => x.cls));
  show('RACE', groupStats(r.rows, x => x.race));
  const reasons = {}; r.games.forEach(g => reasons[g.reason] = (reasons[g.reason] || 0) + 1); console.log('reasons', JSON.stringify(reasons));
  { const tm = gs => { const k = gs.length || 1, m = f => gs.reduce((a, g) => a + f(g), 0) / k / 60; const tot = gs.map(g => g.time.tot / 60).sort((a, b) => a - b); return `${m(g => g.time.tot).toFixed(1)} min (mediana ${tot[Math.floor(tot.length / 2)].toFixed(1)}, 10-90% ${tot[Math.floor(tot.length * .1)].toFixed(0)}-${tot[Math.floor(tot.length * .9)].toFixed(0)}) · inizio ${m(g => g.time.early).toFixed(1)} · centro ${m(g => g.time.mid).toFixed(1)} · finale ${m(g => g.time.late).toFixed(1)} · giri ${(gs.reduce((a, g) => a + g.perPlayer, 0) / k).toFixed(1)}`; };
    console.log('TIME all: ' + tm(r.games)); for (const n of [2, 3, 4]) { const gs = r.games.filter(g => g.n === n); if (gs.length) console.log(`TIME ${n}p: ` + tm(gs)); }
    console.log('DIGITALE ' + [2, 3, 4].map(n => { const gs = r.games.filter(g => g.n === n); return gs.length ? `${n}p ${(gs.reduce((a, g) => a + timeWith(g.time, TEMPI.digitale).tot, 0) / gs.length / 60).toFixed(1)}` : ''; }).filter(Boolean).join(' · ') + ' min'); }
  if (globalThis.AFTER) AFTER(r);
  if (process.env.DUMP) require('fs').writeFileSync(process.env.DUMP, JSON.stringify({ games: r.games, rows: r.rows.map(x => ({ ...x })) }));
})();
