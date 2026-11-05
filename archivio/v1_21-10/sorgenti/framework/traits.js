const r = n => 1 + Math.floor(Math.random() * n);
const dmg = t => t === 'm1' ? Math.max(1, r(6) - 1) : t === 'p1' ? r(6) + 1 : r(6);
const atk = (att, def, adv) => { let d = r(20); if (adv) d = Math.max(d, r(20)); return d !== 1 && (d === 20 || d + att >= def) ? (d === 20 ? 2 : 1) : 0; };
function fight(h, c, N = 60000) {
  let win = 0, lost = 0;
  for (let i = 0; i < N; i++) {
    let hp = h.pv, cp = c.pv, k = 0, first = true;
    while (hp > 0 && cp > 0) {
      k++;
      let m = atk(h.att, 10 + c.ar, false);
      if (m) { let d = dmg(h.d) * m; if (c.half && first) { d = Math.ceil(d / 2); } first = first && !m; cp -= d; }
      if (cp <= 0) break;
      const na = c.twice ? 2 : 1;
      for (let j = 0; j < na && hp > 0; j++) { m = atk(c.att, 10 + h.ar, c.adv1 && k === 1); if (m) hp -= (dmg(c.d) + (c.plus || 0)) * m; }
      if (c.regen && cp > 0) cp = Math.min(c.pv, cp + c.regen);
    }
    if (cp <= 0) { if (c.poison) hp -= c.poison; win++; }
    lost += h.pv - Math.max(0, hp);
  }
  return { win: win / N, lost: lost / N };
}
const M = c => 2 * c.pv + c.att + 2 * c.ar + (c.d === 'd6' ? 4 : c.d === 'p1' ? 8 : 0);
const h = { pv: 10, att: 2, ar: 1, d: 'd6' };
// fit logit(lose) = a*M + b on plain creatures
const pts = [];
for (const pv of [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) for (const att of [1, 2, 3, 4]) for (const ar of [0, 1, 2, 3]) for (const d of ['m1', 'd6', 'p1']) {
  const c = { pv, att, ar, d }; const f = fight(h, c, 8000); if (f.win > 0.02 && f.win < 0.98) pts.push([M(c), Math.log((1 - f.win) / f.win)]); }
const n = pts.length, sx = pts.reduce((a, p) => a + p[0], 0), sy = pts.reduce((a, p) => a + p[1], 0), sxx = pts.reduce((a, p) => a + p[0] * p[0], 0), sxy = pts.reduce((a, p) => a + p[0] * p[1], 0);
const a = (n * sxy - sx * sy) / (n * sxx - sx * sx), b = (sy - a * sx) / n;
const ss = pts.reduce((acc, p) => acc + (p[1] - a * p[0] - b) ** 2, 0), st = pts.reduce((acc, p) => acc + (p[1] - sy / n) ** 2, 0);
console.log('fit a', a.toFixed(4), 'b', b.toFixed(3), 'R2', (1 - ss / st).toFixed(3));
const lose = m => 1 / (1 + Math.exp(-(a * m + b)));
for (const m of [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44]) console.log('M', m, 'lose L1', (lose(m) * 100).toFixed(0) + '%');
const base = [{ pv: 5, att: 3, ar: 0, d: 'm1' }, { pv: 10, att: 4, ar: 2, d: 'd6' }];
const T = { adv1: { adv1: true }, regen1: { regen: 1 }, half: { half: true }, poison1: { poison: 1 }, poison2: { poison: 2 }, plus1: { plus: 1 }, twice: { twice: true } };
for (const bc of base) {
  const f0 = fight(h, bc); const l0 = Math.log((1 - f0.win) / f0.win);
  const out = [`base ${JSON.stringify(bc)} M ${M(bc)} lose ${(100 - f0.win * 100).toFixed(1)}% lost ${f0.lost.toFixed(2)}`];
  for (const k in T) { const f = fight(h, { ...bc, ...T[k] }); const l = Math.log((1 - f.win) / f.win); out.push(`${k}: lose ${(100 - f.win * 100).toFixed(1)}% lost ${f.lost.toFixed(2)} dM ${((l - l0) / a).toFixed(1)}`); }
  console.log(out.join('\n  '));
}
