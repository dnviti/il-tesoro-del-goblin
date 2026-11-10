const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ deviceScaleFactor: 2 });
  await pg.goto('file://' + __dirname + '/reg_docx.html'); await pg.waitForTimeout(1500);
  // mark figure elements
  const n = await pg.evaluate(() => {
    let k = 0;
    const isFig = el => el.matches('.fig,.tokens,.art') || (el.tagName === 'DIV' && el.style.flex.startsWith('none') && el.querySelector('svg')) || (el.tagName==='svg');
    document.querySelectorAll('section.page .in, section.page.cover').forEach(root => {
      root.querySelectorAll('*').forEach(el => { if (isFig(el) && !el.closest('[data-fig]')) { el.setAttribute('data-fig', 'f' + (k++)); } });
    });
    return k;
  });
  for (let i = 0; i < n; i++) { const el = await pg.$(`[data-fig="f${i}"]`); await el.screenshot({ path: `img/f${i}.png`, omitBackground: false }); }
  const blocks = await pg.evaluate(() => {
    const out = [];
    const runs = (el) => { const r = []; const walk = (node, st) => {
        if (node.nodeType === 3) { const t = node.textContent.replace(/\s+/g, ' '); if (t) r.push({ t, ...st }); return; }
        if (node.nodeType !== 1) return; const tg = node.tagName.toLowerCase();
        if (tg === 'svg' || node.classList.contains('ic')) return;
        if (tg === 'br') { r.push({ br: true }); return; }
        const s2 = { ...st }; if (tg === 'b' || tg === 'strong') s2.b = true; if (tg === 'i' || tg === 'em') s2.i = true; if (node.classList.contains('dd')) s2.dd = true;
        node.childNodes.forEach(c => walk(c, s2)); };
      walk(el, {}); return r; };
    const visit = (el) => {
      const tg = el.tagName.toLowerCase(); const cl = el.classList;
      if (el.dataset.fig) { out.push({ k: 'img', f: el.dataset.fig, w: el.getBoundingClientRect().width, h: el.getBoundingClientRect().height }); return; }
      if (cl.contains('folio') || cl.contains('frame')) return;
      if (/^h[1-3]$/.test(tg)) { out.push({ k: tg, r: runs(el) }); return; }
      if (tg === 'p') { out.push({ k: 'p', cls: el.className, r: runs(el) }); return; }
      if (tg === 'ul' || tg === 'ol') { el.querySelectorAll(':scope > li').forEach(li => out.push({ k: tg, r: runs(li) })); out.push({ k: 'endlist' }); return; }
      if (tg === 'table') { const rows = []; el.querySelectorAll('tr').forEach(tr => rows.push([...tr.children].map(td => ({ h: td.tagName === 'TH', r: runs(td) })))); out.push({ k: 'table', rows }); return; }
      if (cl.contains('box')) { const ps = []; el.querySelectorAll('h3,p').forEach(p => ps.push({ h: p.tagName === 'H3', r: runs(p) })); out.push({ k: 'box', red: cl.contains('red'), ps }); return; }
      if (cl.contains('comp')) { out.push({ k: 'comp', items: [...el.children].map(d => runs(d)) }); return; }
      if (cl.contains('strip')) { out.push({ k: 'steps', items: [...el.querySelectorAll('.step')].map(s => ({ n: s.querySelector('.num')?.textContent, t: s.querySelector('.st')?.textContent, d: s.querySelector('.sd')?.textContent })) }); return; }
      if (cl.contains('lg')) { out.push({ k: 'p', cls: 'legend', r: runs(el) }); return; }
      if (el.textContent.trim() && !el.querySelector('div,p,table,ul,ol,h1,h2,h3,svg')) { out.push({ k: 'p', cls: el.className, r: runs(el) }); return; }
      [...el.children].forEach(visit);
    };
    document.querySelectorAll('section.page').forEach((sec, i) => { out.push({ k: 'page', i }); if (sec.classList.contains('cover')) [...sec.children].forEach(visit); else visit(sec.querySelector('.in')); });
    return out;
  });
  require('fs').writeFileSync('blocks.json', JSON.stringify(blocks, null, 1));
  console.log(n, 'figs', blocks.length, 'blocks'); await b.close();
})();
