const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror',e=>console.error('ERR',e.message));
  await p.goto('file://' + __dirname + '/tut.html');
  console.log(JSON.stringify(await p.evaluate(() => ({sayt:SAYT,total:TOTAL}))));
  await b.close(); })();
