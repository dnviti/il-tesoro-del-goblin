// ----- Carte dell'espansione del Caos (nel mazzo comune solo con l'espansione) -----
T({ id: 'CA-01', when: 'fuori', fx: async p => { log('Biglia del nulla: frughi in una Crepa da dove sei.'); await frugare(p, isC(p, 'Mago')); }, ai: p => isLocated(p) ? 0.8 : 2.2, nota: 'Mago: tira due D6 e scegli.' });
T({ id: 'CA-02', when: 'sempre', fx: async p => { const v = await roll(p, 6, 'Pagina strappata'); if (v >= (isC(p, 'Mago') ? 4 : 5)) await addClue(p); else drawCard(p); }, ai: p => isLocated(p) ? 0.5 : 3, nota: 'Mago: basta un 4.' });
T({ id: 'CA-03', when: 'scontro', fx: async p => { const f = foeOf(p); if (f) { log('Un Coboldo pentito ti aiuta!'); await hurt(f, 3, G.combat); } }, ai: () => 3 });
DEF['CA-04'] = te(null, { nota: 'Elmo. +1 AR (Chierico: anche +1 ATT). Sulle Crepe tiri due D6 e scegli.' });
T({ id: 'CA-05', when: 'fuori', fx: async (p, o) => { o.slowNext = true; log(`Vento di nulla: nel suo prossimo turno ${o.name} muove di 1 esagono soltanto.`, 'bad'); }, ai: (p, o) => isLocated(o) ? 3 : 1.5 });
T({ id: 'CA-06', when: 'sempre', fx: async p => { const rs = []; for (const x of G.players.filter(x => !x.out)) { let v = await roll(x, 6, 'Risata del Goblin'); if (x === p) v = Math.max(v, await roll(x, 6, 'Risata del Goblin')); rs.push([x, v]); }
  const m = Math.max(...rs.map(r => r[1])), top = rs.filter(r => r[1] === m); if (top.length === 1) { log(`${top[0][0].name} ride più forte di tutti!`, 'gold'); if (!top[0][0].located) await addClue(top[0][0]); } else log('Pari merito: nessuno prende l\'indizio.'); }, ai: p => isLocated(p) ? 0 : 2.5 });
