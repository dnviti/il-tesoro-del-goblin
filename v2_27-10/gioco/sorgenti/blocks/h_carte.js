// ===================== Carte: definizioni (Carte Trama v2) =====================
const others = (p, id) => p.hand.filter(x => x !== id);
const DEF = {};
function tc(cls, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { await setClass(p, cls, id); return 'keep'; }, ai: p => p.classes.length ? 0 : 6 };
}
DEF['TC-01'] = tc('Guerriero', { nota: '+2 PV. Ogni scontro vinto dà Ispirazione. In scontro puoi spenderla per dare −2 AR al nemico.' });
DEF['TC-02'] = tc('Ladro', { nota: '+2 MOV. Puoi fuggire anche dal Duello e dal Guardiano, e fuggendo non arretri.' });
DEF['TC-03'] = tc('Mago', { nota: 'Puoi ritirare i tuoi dadi fino a 2 volte per turno.' });
DEF['TC-04'] = tc('Oracolo', { nota: 'Se scendi a 0 PV in uno scontro torni a 3 PV e continui a combattere. Si ricarica fermandosi in una Locanda.' });

// --- Mappe ---
const nearestCripta = p => Math.min(...PHYS.cripta.map(([c, r]) => hexDist(p.pos, { c, r })));
function aiMapScore(p, o, id) {
  const sum = x => { const b = mapBonus(x, id); return b.mov * 0.4 + b.adv * 1.5; };
  const foesSum = others2(p).reduce((a, x) => a + sum(x), 0) / Math.max(1, others2(p).length);
  // spostare il tesoro conviene se un avversario lo ha individuato e io no (o se sono più lontano)
  const lead = others2(p).some(x => x.located && (!p.located || hexDist(x.pos, G.treasure) < hexDist(p.pos, G.treasure)));
  let s = (lead && movesLeft() ? 5 : 0) - (p.located && !lead && movesLeft() ? 4 : 0) + sum(p) - foesSum;
  if (id === 'TM-06') s += Math.min(2, p.discard.length) * 1.2;
  if (id === 'TM-07') s += (isC(p, 'Oracolo') && p.discard.length ? 1.2 : 0) + 0.5;
  if (id === 'TM-08') s += 0.3;
  if (G.map && G.map.id === id) s -= 3;
  return s;
}
for (const id of ['TM-01', 'TM-02', 'TM-03', 'TM-04', 'TM-05', 'TM-06', 'TM-07', 'TM-08']) DEF[id] = { when: 'fuori', fx: async (p, o, cid) => { await setMap(p, cid); return cid === 'TM-01' ? undefined : 'keep'; }, ai: (p, o) => aiMapScore(p, o, id), nota: 'Il tesoro cambia Cripta (se è già sulla plancia, al massimo 2 volte per partita); gli Indizi restano. Una sola Mappa attiva: la nuova sostituisce la vecchia.' };
DEF['TM-01'].nota = 'Sposta solo il tesoro: il tabellone resta com\'è.';

// --- Equipaggiamento ---
function eqValue(p, id) {
  const fake = { ...p, equip: { elmo: id, dx: null, sx: null, armatura: null }, flags: {} };
  const b = eqBonus(fake); let v = b.att * 1.2 + b.ar + b.mov * 0.3 + b.pv * 0.5 + b.adv * 2 - b.dis * 3;
  switch (baseId(id)) { case 'TE-01': v += 0.6; break; case 'TE-02': v += 1; break; case 'TE-03': v += 0.8; break; case 'TE-07': v += 0.4; break; case 'TE-08': v += 0.8; break; case 'TE-09': v += 0.3; break; case 'TE-11': v += 0.6; break; case 'TE-12': v += 0.3; break; case 'TE-13': v += 0.6; break; case 'TE-14': v += 0.4; break; case 'TE-15': v += 1; break; case 'TE-16': v += 0.3; break; case 'TE-18': v += 0.3; break; case 'TE-19': v += 0.4; break; case 'TE-20': v += 0.3; break; }
  return v;
}
function aiEquipScore(p, id) {
  const s = SLOT[baseId(id)]; const cur = p.equip[s];
  return eqValue(p, id) - (cur ? eqValue(p, cur) : 0) + (cur ? 0 : 2);
}
function te(on, extra = {}) {
  return { when: 'fuori', need: extra.need, nota: extra.nota, fx: async (p, o, id) => { await equip(p, id); if (on) await on(p, o, id); return 'keep'; }, ai: (p, o, id) => aiEquipScore(p, id) };
}
const NOTE_TE = {
  'TE-01': 'Le Trappole pescate dal sacchetto non hanno effetto su di te.', 'TE-02': '+1 ATT solo contro creature, mini-boss e Guardiano.',
  'TE-03': 'La prima creatura che sconfiggi in ogni turno ti fa riprendere 1 carta dagli scarti.', 'TE-04': '+1 AR. Ritiri un D6 di un tuo incantesimo una volta per turno.',
  'TE-07': 'Quando un nemico ti manca subisce 1 danno.', 'TE-08': 'Una volta per partita annulli i danni di un colpo (l\'IA lo usa sui colpi da 3 o più).',
  'TE-09': 'Se il D6 della perdita dice Arma DX, si ritira.', 'TE-11': '+1 ATT. Ritiri un D6 una volta per turno.', 'TE-12': '+1 ATT, +1 danno ai non morti (Scheletro, Zombi, eroi Sanguar).',
  'TE-13': '+1 danno al primo incantesimo di danno di ogni turno.', 'TE-14': '+1 PV quando ti curi con un incantesimo.', 'TE-15': '+1 ATT negli scontri che inizi tu (contro le creature quasi sempre).',
  'TE-16': '+1 AR, 1 PV in meno dalle Trappole.', 'TE-18': '+1 MOV, +1 PV in Locanda.', 'TE-19': '+1 AR, +2 AR in più contro i nemici di LV 3 o più (mazzetto II, mini-boss e boss).', 'TE-20': '+1 AR, +1 PV alla Fonte.',
};
for (let i = 1; i <= 20; i++) { const id = 'TE-' + String(i).padStart(2, '0'); DEF[id] = te(null, { nota: NOTE_TE[id] }); }

// --- Incantesimi ---
const T = (o) => DEF[o.id] = o;
const inCombat = () => !!G.combat;
const creatureFoe = p => { const f = foeOf(p); return f && f.isCreature ? f : null; };
const missing = p => maxPV(p) - p.pv;
const adjFoes = p => { const f = foeOf(p); if (f && !f.isCreature) return [f]; return others2(p).filter(x => x.pos.c >= 0 && hexDist(x.pos, p.pos) <= 1); };
async function pickAdj(p, title, filter = () => true) { const cand = adjFoes(p).filter(filter); if (cand.length <= 1) return cand[0]; return G.players[await ask(p, title, cand.map(x => ({ label: x.name, value: x.id })), { ai: () => cand.slice().sort((a, b) => b.clues - a.clues)[0].id })]; }
const DMG_SPELLS = ['TI-02', 'TI-09', 'TI-10', 'TI-11', 'TI-16', 'TI-19', 'TI-35', 'TI-40'];
async function spellHit(p, f, n, label) { const b = spellDmgBonus(p); log(`${label}: ${n + b} danni a ${f.name}.`); await hurt(f, n + b, G.combat); if (!G.combat && !f.isCreature && f.pv <= 0) await defeat(f, `da ${p.name}`); }
async function spellHeal(p, n) { heal(p, n + spellHealBonus(p)); }
const aiDmg = (p, ev) => { const f = foeOf(p); if (!f) return 0; return f.pv <= ev + 1 ? 4 : (G.combat.kind !== 'creatura' ? 3.5 : 2.2); };

T({ id: 'TI-01', when: 'sempre', fx: async p => { p.flags.flusso = (p.flags.flusso || 0) + 1; log('Il prossimo incantesimo di danno infligge +1.'); }, ai: p => p.hand.some(x => DMG_SPELLS.includes(baseId(x))) ? 1.2 : 0.2 });
T({ id: 'TI-02', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const { n } = await spellDie(p, 'Dardo Arcano'); await spellHit(p, creatureFoe(p), n, 'Dardo Arcano'); }, ai: p => aiDmg(p, 3.5) });
T({ id: 'TI-03', when: 'sempre', fx: async p => addMod(p, { label: 'Scudo di Cenere: +2 AR', ar: 2, kind: 'scontri', n: 1 }), ai: () => inCombat() ? 2.5 : 1, nota: 'Dura fino alla fine del prossimo scontro (o di quello in corso).' });
T({ id: 'TI-04', when: 'scontro', need: p => { const f = creatureFoe(p); return (f && f.pv === 1 && G.combat.kind !== 'boss') || 'Serve una creatura con 1 PV'; }, fx: async p => { const f = creatureFoe(p); f.pv = 0; log(`${f.name} viene spezzato con lo sguardo.`, 'good'); }, ai: () => 5 });
T({ id: 'TI-05', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima del tiro di Movimento', fx: async p => addMod(p, { label: 'Passo del Folletto', mov: 3, kind: 'turn' }), ai: p => G.phase === 'prima' ? (isLocated(p) ? 3 : 1.2) : -1 });
T({ id: 'TI-06', when: 'fuori', need: p => !p.flags.trapWard || 'Hai già una protezione dalle Trappole', fx: async p => { p.flags.trapWard = true; log('La prossima Trappola che peschi non avrà effetto.'); }, ai: p => p.flags.trapWard || isLocated(p) ? -1 : 0.6, nota: 'Resta davanti a te finché non peschi una Trappola.' });
T({ id: 'TI-07', when: 'sempre', need: (p, o, id) => p.discard.some(x => x !== id) || 'La pila degli scarti è vuota', fx: async (p, o, id) => { await recover(p, 1, { except: id }); }, ai: p => p.discard.length ? 2 : 0 });
T({ id: 'TI-08', when: 'sempre', need: p => !p.insp || 'Hai già l\'Ispirazione', fx: async p => giveInsp(p, 'Scintilla'), ai: () => 1.3 });
T({ id: 'TI-09', when: 'scontro', fx: async p => { const f = foeOf(p); const { n } = await spellDie(p, 'Palla di Fuoco'); await spellHit(p, f, n + (f.pv < (f.isCreature ? f.maxpv : maxPV(f)) ? 1 : 0), 'Palla di Fuoco'); }, ai: p => aiDmg(p, 4) });
T({ id: 'TI-10', when: 'scontro', fx: async p => { const f = foeOf(p); const { n } = await spellDie(p, 'Raggio Gelido', 1); await spellHit(p, f, n, 'Raggio Gelido'); addCmod(G.combat, f, 'att', -1); log(`${f.name}: −1 ATT per questo scontro.`); }, ai: p => aiDmg(p, 3) });
T({ id: 'TI-11', when: 'scontro', fx: async p => { const f = foeOf(p); let tot = 0, v; do { v = (await spellDie(p, 'Catena di Fulmini', 1)).v; tot += Math.max(1, v - 1); } while (v === 6); await spellHit(p, f, tot, 'Catena di Fulmini'); }, ai: p => aiDmg(p, 3.2) });
T({ id: 'TI-12', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { G.combat.confuse = true; log('Il prossimo tiro per colpire della creatura sarà con svantaggio.'); }, ai: p => { const f = creatureFoe(p); return f && G.combat.kind !== 'creatura' ? 2.2 : 1; } });
T({ id: 'TI-13', when: 'scontro', fx: async p => { G.combat.velo = p; log(`${p.name} svanisce nell'ombra: lo scontro si annulla.`); }, ai: p => { const f = foeOf(p); return f && p.pv <= 4 && power(f, G.combat) > power(p, G.combat) * 1.2 ? 5 : -1; }, nota: 'Lo scontro finisce senza ricompense e senza arretrare.' });
T({ id: 'TI-14', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima di muoverti', fx: async p => addMod(p, { label: 'Teletrasporto Breve', mov: 1, kind: 'turn' }), ai: p => G.phase === 'prima' && isLocated(p) ? 1.5 : 0.3, nota: 'Nel simulatore vale come +1 casella di movimento.' });
T({ id: 'TI-15', when: 'fuori', need: p => !p.located || 'Hai già individuato il tesoro', fx: async p => { p.flags.sussurro = true; log('Mappa Sussurrata: il prossimo scontro vinto su una casella esplorazione dà 1 Indizio in più.'); }, ai: p => p.flags.sussurro ? -1 : (p.clues >= 1 ? 4 : 2.5), nota: 'Vale fino al prossimo scontro vinto contro una creatura o un mini-boss.' });
T({ id: 'TI-16', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Fiamma Persistente', 1); await spellHit(p, f, n, 'Fiamma Persistente'); G.combat.burn = (G.combat.burn || 0) + 1; }, ai: p => aiDmg(p, 3) + (G.combat && G.combat.foe.pv > 4 ? 0.5 : 0), nota: 'Poi 1 danno all\'inizio di ogni round seguente.' });
T({ id: 'TI-17', when: 'trappola', fx: async p => { p.turnFlags.barriera = true; }, ai: () => -1, nota: 'Si gioca quando peschi una Trappola: non perdi PV (l\'equipaggiamento sì).' });
T({ id: 'TI-18', when: 'sempre', fx: async p => { p.flags.riflesso = true; log('Fino al tuo prossimo turno chi ti ferisce subisce 1 danno.'); }, ai: p => { const f = foeOf(p); return f && !f.isCreature ? 2 : 0.2; } });
T({ id: 'TI-19', when: 'sempre', need: p => adjFoes(p).length > 0 || 'Nessun avversario a una casella', fx: async p => { const t = await pickAdj(p, 'Tocco Gelido: su chi?'); const { n } = await spellDie(p, 'Tocco Gelido'); await spellHit(p, t, n, 'Tocco Gelido'); }, ai: () => 3 });
T({ id: 'TI-20', when: 'sempre', need: p => adjFoes(p).some(x => x.discard.length) || 'Nessun avversario a una casella con carte negli scarti', fx: async p => { const t = await pickAdj(p, 'Furto di Memoria: a chi?', x => x.discard.length); await recover(p, 1, { from: t.discard, title: `Prendi una carta dagli scarti di ${t.name}` }); }, ai: () => 2.2 });
T({ id: 'TI-21', when: 'sempre', fx: async p => { p.turnFlags.specchio = true; }, ai: p => { const f = creatureFoe(p); return f ? 1.6 : 0.2; }, nota: 'Se in questo turno sconfiggi una creatura prendi l\'Ispirazione.' });
T({ id: 'TI-22', when: 'scontro', fx: async p => { p.flags.nextHit = (p.flags.nextHit || 0) + 3; }, ai: () => 2.3 });
T({ id: 'TI-23', when: 'sempre', need: p => adjFoes(p).length > 0 || 'Nessun avversario a una casella', fx: async p => { const t = await pickAdj(p, 'Sigillo del Silenzio: su chi?'); t.silenced = p.id; log(`${t.name} non può giocare Incantesimi fino al prossimo turno di ${p.name}.`); }, ai: p => { const f = foeOf(p); return f && !f.isCreature ? 2.5 : 0.5; } });
T({ id: 'TI-24', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); addCmod(G.combat, f, 'att', 1 - atkOf(f, G.combat)); log(`${f.name} diventa un ratto: ATT 1.`); }, ai: p => { const f = creatureFoe(p); return f ? (f.att >= 3 ? (G.combat.kind !== 'creatura' ? 4 : 2.5) : 1) : 0; } });
T({ id: 'TI-25', when: 'sempre', need: p => p.pv < maxPV(p) || 'Hai già tutti i PV', fx: async p => { const { n } = await spellDie(p, 'Benedizione', 1); await spellHeal(p, n); }, ai: p => missing(p) >= 3 || (G.combat && p.pv <= 3) ? 2.5 : 0 });
T({ id: 'TI-26', when: 'sempre', need: p => p.pv < maxPV(p) || 'Hai già tutti i PV', fx: async p => { const { n } = await spellDie(p, 'Mano Guaritrice'); await spellHeal(p, n); }, ai: p => missing(p) >= 4 || (G.combat && p.pv <= 3) ? 3 : 0 });
T({ id: 'TI-27', when: 'sempre', fx: async p => addMod(p, { label: 'Scudo della Fede: +1 AR', ar: 1, kind: 'untilNext' }), ai: () => inCombat() ? 1.8 : 0.6 });
T({ id: 'TI-28', when: 'sempre', fx: async p => { p.flags.nextDmg = (p.flags.nextDmg || 0) + 2; }, ai: () => inCombat() ? 2.2 : 0.8, nota: 'Vale per il prossimo colpo che va a segno.' });
T({ id: 'TI-29', when: 'sempre', fx: async p => { p.flags.nextHit = (p.flags.nextHit || 0) + 2; }, ai: () => inCombat() ? 1.8 : 0.6 });
T({ id: 'TI-30', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si gioca quando un colpo ti ferisce (l\'IA la usa sui colpi da 3 o più o letali).' });
T({ id: 'TI-31', when: 'fuori', need: () => G.phase === 'prima' || 'Si gioca prima del tiro di Movimento', fx: async p => { addMod(p, { label: 'Carica Impetuosa', mov: 2, kind: 'turn' }); p.turnFlags.carica = true; }, ai: p => G.phase === 'prima' ? (isLocated(p) ? 2.5 : 1.3) : -1 });
T({ id: 'TI-32', when: 'sempre', need: (p, o, id) => p.discard.some(x => x !== id) || p.pv < maxPV(p) || 'Niente da recuperare', fx: async (p, o, id) => { await recover(p, 1, { except: id }); await spellHeal(p, 1); }, ai: p => p.discard.length ? 2.2 : 0 });
T({ id: 'TI-33', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si gioca subito dopo un tuo tiro: lo ritiri.' });
T({ id: 'TI-34', when: 'scontro', need: p => equipped(p).some(id => SHIELDS.includes(baseId(id))) || 'Serve uno scudo equipaggiato', fx: async p => { addCmod(G.combat, p, 'ar', 2); log(`${p.name}: +2 AR per questo scontro.`); }, ai: () => G.combat && G.combat.kind !== 'creatura' ? 3 : 1.8 });
T({ id: 'TI-35', when: 'scontro', need: p => !!creatureFoe(p) || 'Solo contro una creatura', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Fendente Radioso'); await spellHit(p, f, n + (isUndead(f) ? 2 : 0), 'Fendente Radioso'); }, ai: p => aiDmg(p, 3.5) });
T({ id: 'TI-36', when: 'sempre', fx: async p => { p.flags.giuramento = 2; }, ai: () => inCombat() ? 1.8 : 0.5 });
T({ id: 'TI-37', when: 'scontro', need: p => (G.combat.p === p && !G.combat.foeFirst) || 'Solo negli scontri in cui attacchi per primo', fx: async p => { p.flags.nextDmg = (p.flags.nextDmg || 0) + 2; }, ai: () => 2.2, nota: 'Vale per il prossimo colpo a segno.' });
T({ id: 'TI-38', when: 'reazione', fx: async () => {}, ai: () => -1, nota: 'Si scarta (non conta come carta giocata) per ritirare un tuo tiro per colpire.' });
T({ id: 'TI-39', when: 'trappola', fx: async p => { p.turnFlags.felpato = true; }, ai: () => -1, nota: 'Si gioca quando peschi una Trappola: la ignori del tutto.' });
T({ id: 'TI-40', when: 'scontro', need: p => (G.combat.p === p && !G.combat.attacks && !!creatureFoe(p)) || 'Solo all\'inizio di uno scontro contro una creatura, prima del primo attacco', fx: async p => { const f = creatureFoe(p); const { n } = await spellDie(p, 'Lancio di Coltello', 1); await spellHit(p, f, n, 'Lancio di Coltello'); }, ai: p => aiDmg(p, 3) });
