CLASSES.splice(0,CLASSES.length,'Guerriero','Ladro','Mago','Chierico');
for (let i = COMMON.length - 1; i >= 0; i--) if (COMMON[i].startsWith('TM-')) COMMON.splice(i, 1); // scatola base: niente carte Terreno (espansioni)
Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
if (process.env.REP) eval(require('fs').readFileSync(__dirname + '/report.js', 'utf8'));
for (const id of (process.env.ABL || '').split(',').filter(Boolean)) DEF[id].ai = () => -99;
if (process.env.FORCE) { const _rp = randomPlayers; randomPlayers = function (n) { const cls = shuffle(CLASSES.filter(c => c !== process.env.FORCE)).slice(0, n - 1); cls.unshift(process.env.FORCE); shuffle(cls); const races = Object.keys(RACES); const list = cls.map((c, i) => ({ name: `IA ${i + 1}`, ai: true, cls: c, race: pick(races), free: [pick(['att', 'mov', 'ar', 'pv']), pick(['att', 'mov', 'ar', 'pv'])], deck: [] })); dealList(list); return list; }; }
if (process.env.ONLY) { globalThis.AFTER = r => { const rs = r.rows.filter(x => x.cls === process.env.ONLY); console.log('RATE', process.env.ONLY, process.env.ABL || '-', (rs.reduce((a, x) => a + x.win, 0) / rs.length * 100).toFixed(1)); }; }
