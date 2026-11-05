const BAL = {
  // regole della scatola (confermate il 21/10) che restano
  caos: false, board: 'fisica', buildings: 'once', bagDraw: true, slots3: false, chierRev: 3, clsPV: {}, clsMov: {}, creatureFixed: true, locCatch: true, skipCapFoe: 3, skipCap: 99, setupEquip: true, noD4: true,
  magoPerTurn: true, magoRerolls: 2, ladroAdv: false, ladroMov: 2, chierico: 'locanda', guerInsp: true, guerAR: 2, guerPV: 2, hitDie: 20, defBase: 14, gearStart: true, basePV: 5, lvPV: 2, aiPVmin: 9, pvpFlee: 1.2, pvpLevel: false, defeatPE: 0,
  tiles: { evento: 10 }, bossPV: 14, behPV: 12, clock: 0, clockEvery: 2, pity: 0, maxMoves: 2, omen: 0, servPvP: true, servDmg: 1, impDmg: 3, allOpp: false, foesOff: [], furyAtt: 0, furyDmg: 0, furyMov: 0,
  // v2: combattimento in due tiri e carte nuove
  heroDmg: [6, 0],              // danno degli eroi: D6 (+ bonus delle carte)
  dmgLv: [[4, 0], [6, 0], [6, 1], [6, 1], [6, 1]], // danno dei nemici per livello: D6−1, D6, poi D6+1
  handCls: 3,                   // modalità draft: Classe + 3 carte della tua classe scelte + 7 comuni draftate
  handClsRnd: 5,                // modalità casuale (Daniele, 27/10): Classe + 5 carte di classe a caso + 5 comuni a caso
  handTot: 10,
  handMode: 'random',            // i giocatori scelgono: 'random' = pescata casuale, 'draft' = carte di classe scelte e comuni draftate (Daniele, 27/10)
  draftNoise: 0.04,             // l'IA non sceglie sempre la stessa carta
  moveKeepClues: true,          // quando il tesoro cambia Cripta gli Indizi restano
  trapDmg: 'd6-1',
  // ritmo v2 (27/10): senza le vecchie carte Indizio servono altre fonti di Indizi
  // Indizi solo vincendo uno scontro su una casella esplorazione (Daniele, 27/10): niente Indizio iniziale, niente Mappe strappate, niente Presagio
  startClues: 0,
  bag: { creatura: 19, miniboss: 6, trappola: 5, indizio: 0, vuota: 0 }, // «?»: Nemico I (mazzetto LV 1-2), Nemico II (mazzetto LV 3-4), Trappole
  miniBoss: false,              // regola facoltativa: i mini-boss LV 4,5 si mescolano nel mazzetto II
  bossDeck: true,               // il boss si pesca a caso tra i 3 boss LV 5
  cluesNeed: 2,                 // 2 Indizi per individuare il tesoro (scelta di Daniele, 27/10)
  mbClues: 1,
  bldBag: true,                 // Locanda, Fonte e Fabbro sono segnalini del sacchetto (Daniele, 2/11), non edifici stampati
  bldTok: { locanda: 2, fonte: 2, fabbro: 2 },
};
