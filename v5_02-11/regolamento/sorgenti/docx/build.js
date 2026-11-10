const fs = require('fs');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, ImageRun, AlignmentType, Footer, Header, PageNumber, LevelFormat, PageBreak } = D;
const B = JSON.parse(fs.readFileSync('blocks.json'));
const W = 9638; // A4, margini 2 cm
const INK = '3A2A1A', RED = '8E2A1F', GOLD = 'A5772A';
const run = (x, o = {}) => x.br ? new TextRun({ break: 1 }) : new TextRun({ text: x.t, bold: x.b || o.b, italics: x.i || o.i, highlight: x.dd ? 'yellow' : undefined, size: o.size, color: o.color });
const trimRuns = r => { r = r.slice(); while (r.length && r[0].t !== undefined && !r[0].t.trim()) r.shift(); if (r.length && r[0].t) r[0] = { ...r[0], t: r[0].t.replace(/^\s+/, '') }; const l = r.length - 1; if (l >= 0 && r[l].t) r[l] = { ...r[l], t: r[l].t.replace(/\s+$/, '') }; return r; };
const runs = (r, o) => trimRuns(r).map(x => run(x, o));
const P = (r, o = {}) => new Paragraph({ children: runs(r, o), spacing: { after: o.after ?? 120 }, alignment: o.align, ...(o.p || {}) });
const border = { style: BorderStyle.SINGLE, size: 4, color: 'C9B48A' };
const borders = { top: border, bottom: border, left: border, right: border };
const cell = (children, w, shade) => new TableCell({ children, width: { size: w, type: WidthType.DXA }, borders, shading: shade ? { fill: shade, type: ShadingType.CLEAR, color: 'auto' } : undefined, margins: { top: 60, bottom: 60, left: 110, right: 110 } });
const table = (rows, widths) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: rows.map(cs => new TableRow({ children: cs.map((c, j) => cell(c.ch, widths[j], c.shade)) })) });
const widthsFor = n => n === 2 ? [3300, W - 3300] : n === 4 ? [900, 1900, 2000, W - 4800] : n === 3 ? [700, 2200, W - 2900] : Array(n).fill(Math.floor(W / n)).map((v, i, a) => i === n - 1 ? W - v * (n - 1) : v);
const body = []; let listInst = 0, curList = null, firstH1 = true;
const OPEN = [
  ['Mazzetto dei mostri', 'si sceglie dal livello dell’eroe (com’è scritto ora) o dagli Indizi che ha (0 Indizi: mazzetto 1; 1: mazzetto 2; 2: mazzetto 3)? Con il livello il mazzetto 2 non esce quasi mai.'],
  ['Specie e classi', 'Umano, Elfo, Sanguar, Yumaniano e Assaltatore, Stregone, Oracolo, Ricercatore: qui le ho messe nella scatola base. Il tuo messaggio diceva «prima espansione»: confermi che è la scatola base?'],
  ['Nomi delle classi', 'ho letto Assaltatore = ex Guerriero, Stregone = ex Mago, Ricercatore = ex Ladro (con gli stessi poteri, per esempio solo il Ricercatore fugge dal boss). Da confermare.'],
  ['Yumaniano', 'manca il bonus della specie. Nano e Orco sono stati tolti; le Tessere Specie passano da 10 a 8 (2 per specie)?'],
  ['Assaltatore con i 2D6', 'nel regolamento ha +1 PV (parte con 6) e la sua Ispirazione toglie 1 AR al nemico invece di 2: è la ritaratura del simulatore, da confermare.'],
  ['Chi attacca per primo', 'se il tiro di 1 D6 è pari? Proposta: si ritira.'],
  ['Draft', 'si passa sempre a destra o si alterna destra e sinistra come in Magic?'],
  ['Stregone', 'ha solo 4 carte di classe: prende 1 carta comune in più?'],
  ['Carte da correggere dopo', 'la Carta Classe dell’Assaltatore (PV e Ispirazione), la TI-12 Parola di Confusione («tira due D20») e i nomi delle classi sulle carte.'],
];
const addOpen = () => {
  body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun('Punti da decidere')] }));
  body.push(P([{ t: 'Nel testo i punti aperti sono evidenziati in giallo. Questa pagina non fa parte del regolamento: toglila nella versione definitiva.', i: true }]));
  OPEN.forEach(([a, b]) => body.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: a + ': ', bold: true }), new TextRun({ text: b })] })));
};
for (const b of B) {
  if (b.k !== 'ol' && b.k !== 'ul') curList = null;
  switch (b.k) {
    case 'page': if (b.i === 1) addOpen(); break;
    case 'h1': body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: !firstH1 || true, children: runs(b.r) })); firstH1 = false; break;
    case 'h2': body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(b.r) })); break;
    case 'h3': body.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(b.r) })); break;
    case 'p': {
      const c = b.cls || '';
      if (c === 't1') body.push(P(b.r, { align: AlignmentType.CENTER, color: GOLD, b: true, size: 24, p: { spacing: { before: 1200, after: 120 } } }));
      else if (c === 't2') body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'Il Tesoro del Goblin', bold: true, size: 64, color: RED, font: 'Georgia' })] }));
      else if (/^t\d/.test(c)) body.push(P(b.r, { align: AlignmentType.CENTER, size: c === 't4' ? 26 : 22 }));
      else if (c.includes('lead')) body.push(P(b.r, { size: 24 }));
      else if (c.includes('tip')) body.push(P(b.r, { i: true, size: 19, color: '6B4A2B' }));
      else if (c === 'legend') body.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 40 }, children: runs(b.r, { size: 20 }) }));
      else body.push(P(b.r));
      break; }
    case 'ol': case 'ul': {
      if (!curList) { curList = { k: b.k, inst: ++listInst }; }
      body.push(new Paragraph({ numbering: b.k === 'ol' ? { reference: 'num', level: 0, instance: curList.inst } : { reference: 'bul', level: 0 }, spacing: { after: 80 }, children: runs(b.r) }));
      break; }
    case 'endlist': curList = null; break;
    case 'table': {
      const n = Math.max(...b.rows.map(r => r.length)); const w = widthsFor(n);
      body.push(table(b.rows.map(r => r.map(c => ({ ch: [P(c.r, { b: c.h, after: 0, size: 20 })], shade: c.h ? 'EADBB8' : undefined }))), w));
      body.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break; }
    case 'box': {
      const ch = b.ps.map(p => p.h ? P(p.r, { b: true, color: RED, after: 60 }) : P(p.r, { after: 60 }));
      body.push(table([[{ ch, shade: b.red ? 'FBEAE6' : 'FBF5E8' }]], [W])); body.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break; }
    case 'comp': {
      const it = b.items; const rows = []; for (let i = 0; i < it.length; i += 2) rows.push([it[i], it[i + 1] || []].map(r => ({ ch: [P(r, { after: 0, size: 20 })] })));
      body.push(table(rows, [W / 2, W / 2])); body.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break; }
    case 'steps': {
      const rows = [[{ ch: [P([{ t: 'Passo', b: true }], { after: 0, size: 20 })], shade: 'EADBB8' }, { ch: [P([{ t: 'Nome', b: true }], { after: 0, size: 20 })], shade: 'EADBB8' }, { ch: [P([{ t: 'Cosa fai', b: true }], { after: 0, size: 20 })], shade: 'EADBB8' }]];
      b.items.forEach(s => rows.push([{ ch: [P([{ t: s.n }], { after: 0, size: 20 })] }, { ch: [P([{ t: s.t, b: true }], { after: 0, size: 20 })] }, { ch: [P([{ t: s.d }], { after: 0, size: 20 })] }]));
      body.push(table(rows, [700, 2000, W - 2700])); body.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break; }
    case 'img': {
      const sc = Math.min(1.25, 600 / b.w); const w = Math.round(b.w * sc), h = Math.round(b.h * sc);
      body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 160 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(`img/${b.f}.png`), transformation: { width: w, height: h }, altText: { title: 'Figura', description: 'Figura del regolamento', name: b.f } })] }));
      break; }
  }
}
const doc = new Document({
  creator: 'Il Tesoro del Goblin', title: 'Il Tesoro del Goblin – Regolamento (bozza)',
  styles: {
    default: { document: { run: { font: 'Georgia', size: 21, color: INK } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 36, bold: true, color: RED, font: 'Georgia' }, paragraph: { spacing: { before: 0, after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 26, bold: true, color: '6B4A2B', font: 'Georgia' }, paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 22, bold: true, color: RED, font: 'Georgia' }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
    ] },
  numbering: { config: [
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 300 } } } }] },
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 300 } } } }] } ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Il Tesoro del Goblin · Regolamento, bozza del 2 novembre 2026', size: 16, color: '8A7A66' })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '8A7A66' })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync('Regolamento_Tesoro_del_Goblin_bozza.docx', buf); console.log('ok', body.length); });
