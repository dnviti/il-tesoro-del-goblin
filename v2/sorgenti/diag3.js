Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
const PAT = { ricompone: /si ricompone/, insegue: /ti insegue/, catene: /catene, prendi/, sacch: /ti saccheggia/, succhia: /succhia il sangue/, coriaceo: /è coriaceo/, carica: /carica: \+2/, rigenera: /si rigenera/, illus: /primo tiro per colpire ha svantaggio/, veleno: /Morso infetto/, pietr: /ti pietrifica/, rompi: /colpo devastante/, gelo: /−1 ATT per tutto lo scontro/, lento: /è lento/, borse: /ti ruba una carta/, agguato: /agguato!/, mb: /\(mini-boss\)/, boss: /\(BOSS\)/ };
const CNT = {}; const _log = log;
log = function (t, c) { for (const k in PAT) if (PAT[k].test(t)) CNT[k] = (CNT[k] || 0) + 1; return _log(t, c); };
const BW = {}; const _sc = scontro;
globalThis.AFTER = r => { const N = r.games.length; console.log('FX ' + Object.entries(CNT).sort().map(([k, v]) => `${k}=${(v / N).toFixed(2)}`).join(' | ')); };
