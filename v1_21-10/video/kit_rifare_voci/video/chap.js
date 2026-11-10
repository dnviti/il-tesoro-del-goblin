const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/index.html');
  console.log(JSON.stringify(await p.evaluate(() => ({ban: ITEMS.filter(i=>i.kind==='banner').map(i=>[i.t0,i.data.x]), caps: CAPS.map(c=>[c.t0,c.t1,c.text]), clk: CLK}))));
  await b.close(); })();
