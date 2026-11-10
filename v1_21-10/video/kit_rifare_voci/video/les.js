const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/tut.html');
  console.log(JSON.stringify(await p.evaluate(() => { const out=[];let last=null;for(let t=0;t<TOTAL;t+=0.25){const s=stateAt(t);const k=s.les?s.les[0]:0;if(k!==last){out.push([+t.toFixed(2),k,s.les?s.les[1]:'Copertina']);last=k}} return {out,total:TOTAL}; })));
  await b.close(); })();
