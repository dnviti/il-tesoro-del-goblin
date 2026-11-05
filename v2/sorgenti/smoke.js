const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1300, height: 900 } });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('file://' + process.cwd() + '/tesoro_del_goblin.html');
  await pg.screenshot({ path: 'shot_setup.png' });
  // tutti IA, 4 giocatori, veloce
  await pg.selectOption('#opt-n', '4'); await pg.selectOption('#opt-speed', '200');
  const n = await pg.$$eval('[id^="ai-"], select[data-ai], input[type=checkbox][data-ai]', x => x.length).catch(() => 0);
  console.log('ai controls', n);
  await pg.evaluate(() => { S.players.forEach(p => p.ai = true); renderSetup && renderSetup(); });
  await pg.click('#start');
  await pg.waitForTimeout(1500); await pg.screenshot({ path: 'shot_game.png' });
  await pg.evaluate(() => { window.__fast = true; });
  for (let i = 0; i < 60; i++) { await pg.waitForTimeout(2000); const over = await pg.evaluate(() => G && (G.over || G.winner != null)); if (over) { console.log('finita al ciclo', i); break; } }
  console.log('log tail', await pg.evaluate(() => G.log.slice(-4).map(l => l.t)));
  await pg.screenshot({ path: 'shot_end.png' });
  await pg.click('[data-nav="cards"]'); await pg.click('[data-filter="NE"]'); await pg.screenshot({ path: 'shot_nem.png' });
  await pg.click('[data-filter="tutte"]'); await pg.selectOption('#deckfilter', 'Oracolo'); console.log(await pg.textContent('#deckcount'));
  await pg.selectOption('#deckfilter', 'Comune'); console.log(await pg.textContent('#deckcount'));
  await pg.click('[data-nav="rules"]'); await pg.screenshot({ path: 'shot_rules.png' });
  console.log('errors', errs);
  await b.close();
})();
