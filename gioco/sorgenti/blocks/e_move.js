function moveTreasure() {
  // MIMI va sulla plancia solo quando qualcuno individua il tesoro: prima la Mappa non sposta niente
  if (BAL.moveKeepClues && !G.players.some(p => p.located)) { log('MIMI non è ancora sulla plancia: il tesoro resta nascosto.'); return; }
  const cand = physBoard() ? PHYS.cripta.map(([c, r]) => ({ c, r })).filter(h => !same(h, G.treasure)) : allHexes().filter(h => tileAt(h).type !== 'start' && !same(h, G.treasure) && G.players.every(p => hexDist(h, p.pos) >= 2));
  G.treasure = pick(cand); G.moves = (G.moves || 0) + 1;
  if (BAL.moveKeepClues) { log('Il tesoro cambia Cripta! Gli Indizi restano: chi ne ha 3 sa già dove andare.', 'gold'); return; }
  log('Il tesoro cambia posizione! Chi l\'aveva individuato deve trovare un altro indizio.', 'gold');
  for (const p of G.players) { if (p.located) { p.located = false; p.clues = Math.min(p.clues, 2); } p.tempLocated = 0; }
}
