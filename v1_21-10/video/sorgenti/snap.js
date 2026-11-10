const { chromium } = require('playwright');
(async () => {
  const ts = process.argv.slice(2).map(Number);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file://' + __dirname + '/'+(process.env.PAGE||'index.html'));
  await p.evaluate(() => document.fonts.ready);
  console.log('TOTAL', await p.evaluate(() => window.TOTAL));
  for (const t of ts) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `${process.env.PAGE?'t':''}snap_${t}.png` }); }
  console.log(errs.join('\n'));
  await b.close();
})();
