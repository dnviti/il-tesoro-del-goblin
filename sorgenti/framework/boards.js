(() => {
  const inC = ([c, r]) => c >= 2 && c <= 7 && r >= 2 && r <= 7;
  const rot = ([c, r]) => [[c, r], [9 - c, 9 - r]];
  const both = L => L.flatMap(rot);
  // toglie il contenuto del Cuore e mette quello della plancia Terreno
  const overlay = o => B => {
    B.qs = B.qs.filter(h => !inC(h)).concat(both(o.qs));
    B.caos = B.caos.filter(h => !inC(h)).concat(both(o.caos || []));
    B.crypts = both(o.crypts);
    B.block = both(o.block || []); B.slow = both(o.slow || []);
    B.portals = o.portals || [];
    if (o.activePortals) B.activePortals = o.activePortals;
    if (o.onTurn) B.onTurn = o.onTurn;
  };
  const V = {};
  V.base = {};
  // Scatola base ridisegnata come Terreno vuoto (controllo: stessa disposizione)
  V.cuore = { mod: overlay({ qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [5, 4]], caos: [[3, 2], [7, 4], [4, 4]], crypts: [[3, 3], [6, 3]] }) };
  // ESP. 1 La Selva: solo forma. Stagno di 4 esagoni al centro, Cripte spostate sui lati
  V.selva = { mod: overlay({ block: [[4, 4], [5, 4]], qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [6, 4]], caos: [[3, 2], [7, 4], [3, 4]], crypts: [[3, 3], [6, 3]] }) };
  V.selva6 = { mod: overlay({ block: [[4, 4], [5, 4], [3, 4]], qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [6, 4]], caos: [[3, 2], [7, 4], [6, 2]], crypts: [[3, 3], [6, 3]] }) };
  // variante: Bosco fitto (entrarci costa 2 di movimento) al posto dello stagno
  V.selvaFitto = { mod: overlay({ slow: [[4, 4], [5, 4], [3, 4], [6, 4], [4, 3], [5, 3]], qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [6, 4]], caos: [[3, 2], [7, 4], [3, 4]], crypts: [[3, 3], [6, 3]] }) };
  // ESP. 2 Il Cimitero: due coppie di Tombe gemelle (portali) agli angoli del Cuore
  V.cimitero = { mod: overlay({ qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [5, 4]], caos: [[3, 2], [7, 4], [4, 4]], crypts: [[3, 3], [6, 3]], portals: [[[2, 2], [7, 7]], [[7, 2], [2, 7]]] }) };
  // variante peggiore: portali dalle partenze al centro (da evitare)
  V.cimiteroCentro = { mod: overlay({ qs: [[2, 2], [5, 2], [4, 3], [7, 3], [2, 4], [5, 4]], caos: [[3, 2], [7, 4], [4, 4]], crypts: [[3, 3], [6, 3]], portals: [[[2, 1], [4, 4]], [[7, 8], [5, 5]]] }) };
  // ESP. 3 La Cittadella Bianca: mura su tutto il bordo del Cuore, 4 ponti levatoi.
  // Ponti A (nord e sud) abbassati nei giri dispari, ponti B (ovest ed est) nei giri pari.
  const ring = []; for (let c = 2; c <= 7; c++) for (let r = 2; r <= 7; r++) if (c === 2 || c === 7 || r === 2 || r === 7) ring.push([c, r]);
  const eq = (a, b) => a[0] === b[0] && a[1] === b[1];
  const gatesA = [[4, 2], [5, 7]], gatesB = [[2, 4], [7, 5]];
  const wall = ring.filter(h => ![...gatesA, ...gatesB].some(g => eq(g, h)));
  const inner = { qs: [[4, 3], [5, 3], [3, 4], [4, 4], [5, 4], [6, 4]], caos: [], crypts: [[3, 3], [6, 3]] };
  V.cittadella = { mod: B => {
    overlay(inner)(B); B.block = wall.concat(gatesB);
    B.onTurn = p => { const gt = Math.floor(G.round / G.players.length) + 1; const nb = wall.concat(gt % 2 ? gatesB : gatesA); if (JSON.stringify(nb) !== JSON.stringify(B.block)) { B.block = nb; rebuild(); } };
  } };
  // versione corretta: ponti A sempre abbassati, ponti B abbassati solo nei giri pari
  V.cittadella2 = { mod: B => {
    overlay(inner)(B); B.block = wall.concat(gatesB);
    B.onTurn = p => { const gt = Math.floor(G.round / G.players.length) + 1; const nb = gt % 2 ? wall.concat(gatesB) : wall; if (JSON.stringify(nb) !== JSON.stringify(B.block)) { B.block = nb; rebuild(); } };
  } };
  // versione a 3 coppie di ponti: ogni giro se ne alza una coppia sola, a rotazione (giro 1: coppia 1, giro 2: coppia 2, ...)
  const pairs3 = [[[3, 2], [6, 7]], [[6, 2], [3, 7]], [[7, 4], [2, 5]]];
  const wall3 = ring.filter(h => !pairs3.flat().some(g => eq(g, h)));
  V.cittadella3 = { mod: B => {
    overlay(inner)(B); B.block = wall3.concat(pairs3[0]);
    B.onTurn = p => { const gt = Math.floor(G.round / G.players.length) + 1; const nb = wall3.concat(pairs3[(gt - 1) % 3]); if (JSON.stringify(nb) !== JSON.stringify(B.block)) { B.block = nb; rebuild(); } };
  } };
  V.c3s1 = { mod: B => { overlay(inner)(B); B.block = wall3.concat(pairs3[0]); } };
  V.c3s2 = { mod: B => { overlay(inner)(B); B.block = wall3.concat(pairs3[1]); } };
  V.c3s3 = { mod: B => { overlay(inner)(B); B.block = wall3.concat(pairs3[2]); } };
  V.c3open = { mod: B => { overlay(inner)(B); B.block = wall3; } };
  V.cittadellaA = { mod: B => { overlay(inner)(B); B.block = wall.concat(gatesB); } };
  V.cittadellaB = { mod: B => { overlay(inner)(B); B.block = wall.concat(gatesA); } };
  V.cittadellaFissa = { mod: B => { overlay(inner)(B); B.block = wall; } };
  return V;
})()
