const { chromium } = require('playwright');
(async () => {
  const [,, inp, out, w, h] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, width: w, height: h, printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
