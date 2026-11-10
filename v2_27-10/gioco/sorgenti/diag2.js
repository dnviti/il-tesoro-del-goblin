Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
const PAT = { turno: /^Turno di /, pvp: /combattimento PvP/, salta: /salta|perde il turno|Clessidr/i, pesca: /pesca dal sacchetto: (.*) \(/, scontro: /^Scontro: /, vince: /vince lo scontro|è sconfitt[oa]!|sconfigge/, fuga: /fugge|fuga/i, sconfitta: /viene sconfitt|ricompare|respawn/i, indizio: /ottiene un indizio/, presagio: /presagio indica/, voce: /voce si sparge/i, trappola: /^Trappola!/, mappa: /mappa strappata/i };
const CNT = {}; const _log = log;
log = function (t, c) { for (const k in PAT) { const m = PAT[k].exec(t); if (m) { const key = k === 'pesca' ? 'pesca:' + m[1] : k; CNT[key] = (CNT[key] || 0) + 1; } } return _log(t, c); };
globalThis.AFTER = r => { const N = r.games.length; console.log('DIAG ' + Object.entries(CNT).sort().map(([k, v]) => `${k}=${(v / N).toFixed(2)}`).join(' | ')); };
