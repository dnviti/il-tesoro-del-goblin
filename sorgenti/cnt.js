CLASSES.splice(0,CLASSES.length,'Guerriero','Ladro','Mago','Chierico');
for (let i = COMMON.length - 1; i >= 0; i--) if (COMMON[i].startsWith('TM-')) COMMON.splice(i, 1);
Object.assign(BAL, JSON.parse(process.env.BALX || '{}'));
const CN = { fr: 0, tr: 0, draw: 0, agg: 0, bors: 0, play: {} };
{ const f = frugare; frugare = async (p, t) => { CN.fr++; return f(p, t); }; const d = drawCard; drawCard = p => { CN.draw++; return d(p); };
  const l = log; log = (m, k) => { if (/attraversa il fondo/.test(m)) CN.tr++; if (/agguato/.test(m)) CN.agg++; if (/ti ruba/.test(m)) CN.bors++; return l(m, k); };
  const pc = playCard; playCard = async (p, id, o) => { const r = await pc(p, id, o); if (baseId(id).startsWith('CA-')) CN.play[baseId(id)] = (CN.play[baseId(id)] || 0) + 1; return r; }; }
process.on('exit', () => console.log('CN', JSON.stringify(CN)));
