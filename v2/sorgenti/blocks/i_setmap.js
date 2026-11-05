async function setMap(p, id) {
  if (movesLeft()) moveTreasure(); else log(`Il tesoro si è già spostato ${BAL.maxMoves} volte: resta dov'è.`);
  if (id === 'TM-01') return; // Miraggio del Tesoro: niente terreno
  if (G.map) { G.players[G.map.owner].discard.push(G.map.id); log(`La mappa «${C(G.map.id).nome}» lascia il posto alla nuova.`); }
  G.map = { id, owner: p.id };
  log(`Il tabellone diventa «${C(id).nome}».`, 'gold');
  if (id === 'TM-06') { for (const x of live()) await recover(x, x === p ? 2 : 1, { except: id }); }
  if (id === 'TM-07') { for (const x of live()) if (isC(x, 'Oracolo')) await recover(x, 1, { except: id }); }
}
