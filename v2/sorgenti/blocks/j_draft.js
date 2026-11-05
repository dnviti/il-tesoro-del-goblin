// ===================== Mano: carte di classe scelte, carte comuni draftate (Daniele, 27/10) =====================
// valore di partenza di ogni carta per l'IA (vittorie di chi l'aveva in mano / attese, da partite simulate con mani casuali)
const DRAFT_VAL = /*DRAFT_VAL*/{};
const draftVal = id => DRAFT_VAL[baseId(id)] || 1;
function aiPickScore(hand, id) {
  let s = draftVal(id) - 1;
  const sl = SLOT[baseId(id)];
  if (sl && sl !== 'pozione' && hand.some(x => SLOT[baseId(x)] === sl)) s -= 0.5 * Math.max(0, s) + 0.02; // stesso slot: vale meno
  return s + (Math.random() - 0.5) * (BAL.draftNoise || 0);
}
const aiPick = (hand, opts) => opts.slice().sort((a, b) => aiPickScore(hand, b) - aiPickScore(hand, a))[0];
const cardLabel = id => { const t = C(id).testo; return `${C(id).nome}: ${t.length > 110 ? t.slice(0, 107) + '…' : t}`; };
async function pickCard(p, title, opts) {
  if (p.ai || G.fast) return aiPick(p.hand, opts);
  return ask(p, title, opts.map(id => ({ label: cardLabel(id), value: id })), { ai: () => aiPick(p.hand, opts) });
}
async function buildHands() {
  const myGame = G, ps = G.players, n = ps.length;
  // 1. ognuno sceglie BAL.handCls carte tra quelle della sua classe (le carte con due classi sono stampate in due copie)
  for (const p of ps) {
    let pool = (DECK[p.startCls] || []).slice();
    for (let k = 0; k < BAL.handCls && pool.length; k++) {
      const ch = await pickCard(p, `Scegli le tue carte ${p.startCls} (${k + 1} di ${BAL.handCls})`, pool);
      if (G !== myGame) return new Promise(() => {});
      p.hand.push(ch); pool = pool.filter(x => x !== ch);
    }
    if (!p.ai) log(`${p.name} ha scelto le sue carte di classe.`); else log(`${p.name} sceglie le sue carte di classe.`);
  }
  // 2. draft delle carte comuni: un pacchetto coperto a testa, scegli una carta e passa il resto a sinistra
  const size = BAL.handTot - BAL.handCls;
  const deck = shuffle(commonPool().slice());
  const packs = ps.map(() => deck.splice(0, size + (BAL.draftExtra || 0)));
  log(`Draft delle carte comuni: ${size} giri, si passa a sinistra.`, 'turn');
  for (let r = 0; r < size; r++) {
    for (let i = 0; i < n; i++) {
      const p = ps[i], pack = packs[(i + r) % n];
      const ch = await pickCard(p, `Draft delle carte comuni, giro ${r + 1} di ${size}: prendi una carta e passa le altre`, pack);
      if (G !== myGame) return new Promise(() => {});
      p.hand.push(ch); pack.splice(pack.indexOf(ch), 1);
    }
  }
  for (const p of ps) p.startHand = [...p.hand];
  render();
}
