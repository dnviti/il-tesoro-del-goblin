import sys, json, re
sys.path.insert(0,'/mnt/project-files/tesoro-goblin/sorgenti/regolamento_stampa/book')
from parts import scheda, move_example, card_anatomy
src=open('index.html').read()  # built by gen.py (board + GEOM + ICONS)
a=src.index('// ---------------- the game ----------------'); b=src.index('const TOTAL=T;')
tut=open('tut_script.js').read().replace('const NL=10;','const NL=16;').replace('const DUR=[];','const DUR='+open('../tts/durs.json').read()+';')
src=src[:a]+tut+'\nmusicEnd();\n'+src[b:]
src=re.sub(r'const MG=.*?;/\*MG\*/',lambda m:'const MG='+open('../suno/mg_tav.json').read()+';/*MG*/',src,count=1)
art={'scheda':scheda(),'move':move_example(),'anatomy':card_anatomy()}
def rep(x,y):
    global src
    assert x in src, x[:70]; src=src.replace(x,y,1)
rep('const $=id=>', 'const ART='+json.dumps(art)+';\nconst $=id=>')
rep("const b={t0,dur,", "const b={t0,dur,")
rep("const ART=", "const beatEnd=b=>b.dur-0.05;\nconst ART=")
# lesson box instead of clock
rep("const ts=Math.round(tableAt(t));$('clk').textContent=Math.floor(ts/60)+':'+String(ts%60).padStart(2,'0');",
    "document.querySelector('.clock .l').textContent='LEZIONE';$('clk').textContent=s.les?s.les[0]+' / '+NL:'';")
rep("$('giro').textContent=s.playing?`Giro ${s.giro}${s.giro>=8?' · Presagio attivo':''}`:'preparazione';",
    "$('giro').textContent=s.les?s.les[1]:'';")
# stage: only the most recent active item
rep("let st='';for(const it of ITEMS){if(t<it.t0||t>=it.t1||!R[it.kind])continue;",
    "let st='';const act=ITEMS.filter(it=>t>=it.t0&&R[it.kind]&&(it.t1-it.t0<9000||t<it.t1));const top=act.length?act.reduce((a,b)=>b.t0>=a.t0?b:a):null;for(const it of ITEMS){if(it!==top)continue;it.t1=Math.max(it.t1,1e9);")
# speaker captions
rep("const c=CAPS.filter(c=>t>=c.t0&&t<c.t1).pop();$('cap').innerHTML=c?`<span style=\"opacity:${fade(t-c.t0,c.t1-c.t0,.2,.15)}\">${c.text}</span>`:'';",
    "const c=CAPS.filter(c=>t>=c.t0&&t<c.t1).pop();$('cap').innerHTML=c?capHTML(c,t):'';")
rep("function render(t){", """const SPK={L:['Lia','#a8352a','#ff9c8c','gioca da anni'],M:['Marco','#2f5d9c','#9cc2ff','spiega le regole'],G:['Giulia','#3d7a3f','#9fe0a0','alla prima partita']};
function capHTML(c,t){const i=c.text.indexOf('|');const w=c.text.slice(0,i),tx=c.text.slice(i+1);const p=SPK[w];const op=fade(t-c.t0,c.t1-c.t0,.15,.12);
  return `<div style="display:flex;gap:22px;align-items:center;width:100%;opacity:${op}"><div style="flex:none;width:92px;height:92px;border-radius:50%;background:${p[1]};border:4px solid #f4ead5;display:flex;align-items:center;justify-content:center;font-family:Cinzel;font-weight:800;font-size:46px;color:#fff">${p[0][0]}</div><div><div style="font-family:Cinzel;font-weight:800;font-size:22px;color:${p[2]};letter-spacing:1px">${p[0]} <span style="font-family:'Alegreya Sans';font-weight:700;font-size:17px;color:#cbb88e;letter-spacing:0">· ${p[3]}</span></div><div style="font-size:30px;line-height:1.25">«${tx}»</div></div></div>`}
function render(t){""")
# overlay highlights
rep("  // sala figures", """  for(const it of ITEMS){if(t<it.t0||t>it.t1)continue;const l=t-it.t0,op=fade(l,it.t1-it.t0,.3,.3);
    if(it.kind==='hl'){for(const [c,r] of it.data.cells){const x=hx(c,r),y=hy(c,r),rr=Rr*0.97;const pts=[-90,-30,30,90,150,210].map(a=>(x+rr*Math.cos(a*Math.PI/180))+','+(y+rr*Math.sin(a*Math.PI/180))).join(' ');
      o+=`<polygon points="${pts}" fill="${it.data.col}" fill-opacity="${(0.18+0.12*Math.sin(l*5))*op}" stroke="${it.data.col}" stroke-width="2.4" stroke-opacity="${op}"/>`}}
    if(it.kind==='hlrect'){const d=it.data;o+=`<rect x="${d.x}" y="${d.y}" width="${d.w}" height="${d.h}" rx="8" fill="#f2c230" fill-opacity="${0.12*op}" stroke="#d98a1c" stroke-width="${2.5+Math.sin(l*5)}" opacity="${op}"/>`}}
  // sala figures""")
rep("return `<div class=\"hero ${h.on?'':'hide'} ${s.active===k?'act':''}\">", "const glow=ITEMS.some(i=>i.kind==='hlhero'&&t>=i.t0&&t<i.t1);return `<div class=\"hero ${h.on?'':'hide'} ${s.active===k||(glow&&h.on)?'act':''}\">")
rep("const FULL={", """const FULL={
 recap(d,lt,dur){const L=[['Scopo','3 Indizi → la Cripta di MIMI → batti il Guardiano'],['Turno','Clessidre · Carte · Muovi · Esplora · Fine'],['Movimento','D6 + MOV, conta solo dove ti fermi'],['Scontro','D20 + ATT ≥ Difesa (10 + AR), 20 doppio, 1 mancato'],['Carte','10 per tutta la partita, max 2 a turno, 1 equipaggiamento'],['Sconfitta','D6 per ripartire, PV pieni, perdita col D6'],['Dal giro 8','Presagio: D6 per un Indizio']];
  return `<div class="cover" style="opacity:${fade(lt,dur,.5,.8)}"><div class="a">IN BREVE</div><div style="margin-top:26px;display:grid;grid-template-columns:auto auto;gap:14px 34px;text-align:left;font-family:'Alegreya Sans';font-size:34px;color:#efe2c2">${L.map(r=>`<b style="font-family:Cinzel;color:#f6d68b">${r[0]}</b><span>${r[1]}</span>`).join('')}</div><div class="d" style="margin-top:40px">Il regolamento completo è nella scatola · foglio «Inizia subito» per la prima partita</div></div>`},""")
open('tut.html','w').write(src)
print('ok')
