// segnalino Nemico I → mazzetto LV 1-2; segnalino Nemico II → mazzetto LV 3-4 (con i mini-boss LV 4,5 se la regola facoltativa è attiva)
const deckII = () => [...MAZZO_II, ...(BAL.miniBoss ? MINIBOSS : [])];
async function meetCreature(p, kind) {
  if (p.challenge) { kind = 'miniboss'; log('Sfidare i potenti: al posto della creatura appare un nemico del mazzetto II!', 'gold'); }
  const deckK = kind === 'miniboss' ? 'mb' : 'cr';
  if (!G.nem[deckK].length) G.nem[deckK] = shuffle(kind === 'miniboss' ? deckII() : [...BESTIARIO]);
  const foe = makeCreature(G.nem[deckK].pop(), p.level);
  kind = foe.tipo === 'Mini-boss' ? 'miniboss' : 'creatura';
  const st = `${foe.name} (LV ${String(foe.lv).replace('.', ',')}): PV ${foe.pv}, ATT ${fmt(foe.att)}, AR ${foe.ar} (Difesa ${DIFESA(foe.ar)}), danno ${dmgLabel(foe)}. ${foe.abil || ''}`;
  const opts = [{ label: 'Affronta lo scontro', value: 'f' }];
  if (!noFlee(foe)) opts.push({ label: foe.fx === 'lento' || isC(p, 'Ladro') ? 'Fuggi (resti dove sei)' : 'Fuggi (arretri di una casella)', value: 'r' });
  const ch = await ask(p, `Incontri ${kind === 'miniboss' ? 'un mini-boss' : foe.lv >= 3 ? 'un nemico del mazzetto II' : 'un nemico'}! ${st}`, opts, { ai: () => (opts.length > 1 && power(foe) > power(p) * 1.6 && p.pv <= 4 ? 'r' : 'f') });
  if (ch === 'r') {
    log(`${p.name} dichiara la fuga.`);
    if (foe.fx === 'inseguitore') {
      const c = { p, foe, kind, round: 0, berserk: {}, carica: {}, mods: {}, reflect: {}, spinato: {}, chierico: {}, daga: {}, petrified: {}, dis: {}, used: {}, defCards: 0, noCards: true };
      G.combat = c; log(`${foe.name} ti insegue e attacca!`, 'bad'); await attack(foe, p, c); G.combat = null;
      if (dead(p)) { await defeat(p, `da ${foe.name}`); return; }
    }
    if (isC(p, 'Ladro') || foe.fx === 'lento') log(isC(p, 'Ladro') ? 'Ladro: fugge senza arretrare.' : `${foe.name} è lento: non arretri.`); else retreat(p, p.turnStart);
    return;
  }
  await scontro(p, foe, kind);
}
