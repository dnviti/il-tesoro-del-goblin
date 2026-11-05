const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1300, height: 950 } });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('file://' + process.cwd() + '/tesoro_del_goblin.html');
  await pg.selectOption('#opt-n', '3'); await pg.selectOption('#opt-speed', '200'); await pg.selectOption('#opt-hand', 'draft');
  console.log('hint:', (await pg.textContent('.deckhint')).trim());
  await pg.click('#start');
  let shot = false;
  for (let k = 0; k < 40; k++) {
    await pg.waitForTimeout(400);
    const t = await pg.evaluate(() => pending && pending.title);
    if (!t) continue;
    if (!/carte|Draft/.test(t)) { console.log('dopo la mano:', t); break; }
    if (!shot && /Draft/.test(t)) { await pg.screenshot({ path: 'shot_draft.png' }); shot = true; }
    await pg.click('[data-opt="0"]');
  }
  console.log('mani', await pg.evaluate(() => G.players.map(p => p.name + ' ' + (p.hand.length + Object.values(p.equip).filter(Boolean).length) + ' ' + p.startHand.length)));
  // partita tutta IA in draft
  await pg.evaluate(() => { S.players.forEach(p => p.ai = true); });
  await pg.click('[data-nav="setup"]'); await pg.click('#start');
  for (let i = 0; i < 90; i++) { await pg.waitForTimeout(2000); if (await pg.evaluate(() => G && G.over)) { console.log('IA finita', i); break; } }
  console.log('errors', errs); await b.close();
})();
