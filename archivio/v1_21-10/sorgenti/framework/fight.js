const r = n => 1 + Math.floor(Math.random() * n);
const dmg = t => t === 'm1' ? Math.max(1, r(6) - 1) : t === 'p1' ? r(6) + 1 : r(6);
function fight(h, c, N = 40000) {
  let win = 0, lost = 0, rounds = 0, lostW = 0;
  for (let i = 0; i < N; i++) {
    let hp = h.pv, cp = c.pv, k = 0;
    while (hp > 0 && cp > 0) {
      k++;
      let d = r(20); if (d !== 1 && (d === 20 || d + h.att >= 10 + c.ar)) cp -= dmg(h.d) * (d === 20 ? 2 : 1);
      if (cp <= 0) break;
      d = r(20); if (d !== 1 && (d === 20 || d + c.att >= 10 + h.ar)) hp -= dmg(c.d) * (d === 20 ? 2 : 1);
    }
    rounds += k; const l = h.pv - Math.max(0, hp); lost += l; if (cp <= 0) { win++; lostW += l; }
  }
  return { win: win / N, lost: lost / N, lostW: lostW / Math.max(1, win), rounds: rounds / N };
}
module.exports = { fight };
if (require.main === module) {
  const H = { L1: { pv: 10, att: 2, ar: 1, d: 'd6' }, L3: { pv: 12, att: 3, ar: 2, d: 'd6' }, L1nudo: { pv: 10, att: 2, ar: 1, d: 'm1' } };
  const M = [
    ['Coboldo', 4, 1, 0, 'm1'], ['Ratto gigante', 3, 2, 0, 'm1'], ['Scheletro', 5, 2, 1, 'm1'], ['Lupo grigio', 5, 3, 0, 'm1'], ['Orchetto predone', 6, 2, 1, 'd6'],
    ['Ragno delle grotte', 5, 3, 1, 'm1'], ['Melma acida', 7, 1, 0, 'd6'], ['Gnomo schiavista', 4, 2, 2, 'm1'],
    ['Ogre delle paludi', 12, 3, 1, 'p1'], ['Troll di fiume', 11, 3, 2, 'd6'], ['Capitano goliath', 10, 4, 2, 'd6'], ['Strega del vischio', 9, 4, 1, 'p1'],
    ['Guardiano di MIMI', 12, 4, 3, 'p1']];
  for (const [n, pv, att, ar, d] of M) {
    const o = [n, `${pv}/${att}/${10 + ar}/${d}`];
    for (const k in H) { const f = fight(H[k], { pv, att, ar, d }); o.push(`${k}: win ${(f.win * 100).toFixed(0)}% lost ${f.lost.toFixed(1)} rnd ${f.rounds.toFixed(1)}`); }
    console.log(o.join(' | '));
  }
}
