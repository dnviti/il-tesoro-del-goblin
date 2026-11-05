import sys
p='page.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:80]
    s=s.replace(a,b)
i=s.index('// ---------------- the game ----------------'); j=s.index('musicEnd();\nconst TOTAL=T;')
s=s[:i]+open('copione_v2.js').read().rstrip()+'\n'+s[j:]
rep("const HERO0={on:false,c:null,r:null,pv:10,pvm:10,att:1,mov:1,ar:1,","const HERO0={on:false,c:null,r:null,pv:5,pvm:5,att:1,mov:1,ar:1,arTmp:0,")
rep("sala:{Guardiano:true,MIMI:true,Ogre:true,Troll:true,Goliath:true,Strega:true},","sala:{Boss:true,MIMI:true,Ogre:false,Troll:false,Goliath:false,Strega:false},")
rep("const nms=['Guardiano','MIMI','Ogre','Troll','Goliath','Strega'];","const nms=['Boss','MIMI','Ogre','Troll','Goliath','Strega'];")
# niente tracciato dei giri; PV del boss su 9 caselle
rep("if(s.cubesOn){const g=GEOM.giro;const gi=s.giro-1;o+=`<rect x=\"${g.g0+gi*g.gx+g.gx*0.15}\" y=\"${g.gy+g.gx*0.15}\" width=\"${g.gx*0.6}\" height=\"${g.gx*0.6}\" rx=\"1.5\" fill=\"#f2c230\" stroke=\"#6b4a2b\" stroke-width=\"0.8\"/>`;",
    "if(s.cubesOn&&s.gpv>0){")
rep("const p=GEOM.pvt;const pi=14-pv;","const p=GEOM.pvt;const pi=9-pv;")
# combattimento e scheda: Difesa 14 + AR
rep("const hd=10+h.ar;","const hd=14+h.ar+(h.arTmp||0);")
rep("<span class=\"k\">DIFESA</span>${10+h.ar}</div>","<span class=\"k\">DIFESA</span>${14+h.ar+(h.arTmp||0)}</div>")
rep("const ind=[0,1,2].map(","const ind=[0,1].map(")
rep("const pe=[...Array(9)].map((_,i)=>`<span class=\"${[2,4,6,8].includes(i)?'g':''} ${i===h.pe?'c':''}\">${i}</span>`).join('');",
    "const pe=[...Array(3)].map((_,i)=>`<span class=\"${i===2?'g':''} ${i===h.pe?'c':''}\">${i}</span>`).join('');")
rep("$('giro').textContent=s.playing?`Giro ${s.giro}${s.giro>=8?' · Presagio attivo':''}`:'preparazione';","$('giro').textContent=s.playing?`Giro ${s.giro}`:'preparazione';")
rep("['carte','Carte','Fino a 2 nel turno, quando vuoi. Max 1 equipaggiamento.']","['carte','Carte','Fino a 2: a inizio turno, in scontro o a fine turno. Equipaggiamenti solo ora, max 1.']")
rep("['bandiera','Fine','Togli i cubetti Durata. Passa i dadi.']","['bandiera','Fine','Puoi ancora giocare carte. Togli i cubetti Durata, passa i dadi.']")
# carta Nemico
rep(" strip(d,lt){",""" ncard(d,lt){const c=d.c;const a=ease(lt/.35);const col=c.tipo==='Boss'?'#7a2a1c':c.tipo==='Nemico II'?'#5a3a6e':'#3b4a2a';
   const stat=(ic,k,v)=>`<div style="display:flex;flex-direction:column;align-items:center;gap:2px">${IC(ic,30)}<div style="font-size:13px;color:#6b4a2b;font-weight:800">${k}</div><div style="font-family:Cinzel;font-weight:800;font-size:30px">${v}</div></div>`;
   return `<div class="ctr" style="gap:36px"><div style="width:300px;height:420px;border-radius:18px;background:#fffaf0;border:4px solid ${col};box-shadow:0 10px 30px #0006;display:flex;flex-direction:column;overflow:hidden;transform:translateY(${(1-a)*60}px) rotate(${(1-a)*-6}deg);opacity:${a}">
   <div style="background:${col};color:#fff;padding:10px 14px;display:flex;align-items:center;gap:10px"><div style="width:44px;height:44px;border-radius:50%;background:#fffaf0;color:${col};font-family:Cinzel;font-weight:800;font-size:26px;display:flex;align-items:center;justify-content:center">${c.letter}</div><div style="font-family:Cinzel;font-weight:800;font-size:${c.name.length>15?19:23}px;line-height:1.05">${c.name}</div></div>
   <div style="display:flex;justify-content:space-between;padding:6px 14px;font-size:14px;font-weight:800;color:#6b4a2b"><span>${c.tipo||'Nemico I'}</span><span>LV ${String(c.lv).replace('.',',')}</span></div>
   <div style="display:flex;justify-content:space-around;padding:4px 10px 8px;border-bottom:2px solid #e3d3b0">${stat('cuore','PV',c.pv)}${stat('spade','ATT','+'+c.att)}${stat('scudo','DIFESA',14+c.ar)}</div>
   <div style="padding:8px 14px;font-size:15px;color:#9c2f24;font-weight:800">Danno ${c.dmg}</div>
   <div style="padding:0 14px;font-size:16px;line-height:1.3;flex:1;color:#2a2118">${c.ab}</div>
   <div style="background:#f3e6c8;padding:8px 14px;font-size:14px;font-weight:700;color:#2a2118">Ricompensa: ${c.rew.join(' · ')}</div></div>
   <div style="width:300px;opacity:${ease((lt-0.5)/.3)}"><div class="lbl" style="text-align:left;font-size:18px">Difesa = 14 + AR ${c.ar}</div><div class="lbl" style="text-align:left;font-size:18px;margin-top:8px">Si colpisce con D20 + ATT ≥ Difesa</div></div></div>`},
 strip(d,lt){""")
# tutte le D20 vs: niente da cambiare (i valori sono nel copione)
open(p,'w').write(s)
print('ok')
