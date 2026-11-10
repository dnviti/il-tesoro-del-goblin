const cube = h => { const x = h.c - (h.r - (h.r & 1)) / 2; const z = h.r; return [x, -x - z, z]; };
const hd = (a, b) => { const A = cube(a), B = cube(b); return Math.max(...[0, 1, 2].map(i => Math.abs(A[i] - B[i]))); };
const all = []; for (let r = 0; r < 10; r++) for (let c = 0; c < 10; c++) all.push({ c, r });
const SP = [[2, 0], [7, 0], [9, 4], [7, 9], [2, 9], [0, 5]];
const BASEB = { crypts: [[3, 3], [6, 3], [3, 6], [6, 6]], block: [], slow: [], portals: [], qs: [], caos: [] };
globalThis.G = { round: 0, players: [{}] }; globalThis.rebuild = () => {};
const V = eval(require('fs').readFileSync(__dirname + '/boards.js', 'utf8'));
for (const name of process.argv.slice(2)) {
  const B = JSON.parse(JSON.stringify(BASEB)); if (V[name].mod) V[name].mod(B);
  const blocked = new Set(B.block.map(h => h.join(',')));
  const K = h => h.c + ',' + h.r;
  const bfs = s => { const d = {}; d[K(s)] = 0; const q = [s]; while (q.length) { const u = q.shift(); const nb = all.filter(x => hd(x, u) === 1); for (const [a, b] of B.portals) { if (a[0] === u.c && a[1] === u.r) nb.push({ c: b[0], r: b[1] }); if (b[0] === u.c && b[1] === u.r) nb.push({ c: a[0], r: a[1] }); } for (const v of nb) { if (blocked.has(K(v)) || d[K(v)] !== undefined) continue; d[K(v)] = d[K(u)] + 1; q.push(v); } } return d; };
  const rows = SP.map(([c, r], i) => { const d = bfs({ c, r }); const cr = B.crypts.map(([a, b]) => d[a + ',' + b]); return `P${i + 1}: cripte ${cr.join('/')} (min ${Math.min(...cr)} max ${Math.max(...cr)} media ${(cr.reduce((x, y) => x + y, 0) / 4).toFixed(2)})`; });
  const reach = all.filter(h => !blocked.has(K(h))).length;
  console.log(name, '| esagoni usabili', reach, '| bloccati', blocked.size); rows.forEach(x => console.log('  ' + x));
}
