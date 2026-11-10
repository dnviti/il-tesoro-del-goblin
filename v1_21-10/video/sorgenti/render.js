const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const [,, a, bnd, out] = process.argv; const FPS = 25;
  const br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + __dirname + '/'+(process.env.PAGE||'index.html')); await p.evaluate(() => document.fonts.ready);
  const total = await p.evaluate(() => window.TOTAL); const N = Math.ceil(total * FPS);
  const f0 = Math.floor(N * +a), f1 = Math.floor(N * +bnd);
  const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',''+FPS,'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',out]);
  for (let f = f0; f < f1; f++) {
    await p.evaluate(t => render(t), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 500 === 0) console.log(out, f, '/', f1);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close();
})();
