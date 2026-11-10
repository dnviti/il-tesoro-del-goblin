const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror',e=>console.error('ERR',e.message));
  await p.goto('file://' + __dirname + '/' + (process.env.PAGE||'index.html'));
  console.log(JSON.stringify(await p.evaluate(() => ({total:TOTAL,cut:MG&&MG.cut,sayt:typeof SAYT!=='undefined'?SAYT:null}))));
  await b.close(); })();
