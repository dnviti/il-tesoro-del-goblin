const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/tut.html');
  console.log(JSON.stringify(await p.evaluate(() => CAPS.map(c=>c.text))));
  await b.close(); })();
