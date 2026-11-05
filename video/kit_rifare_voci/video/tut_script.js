// ---------------- tutorial: Lia e Marco spiegano il gioco a Giulia ----------------
S0.H.S.name='Giulia';
const LUPO={name:'Lupo grigio',short:'Lupo',pv:5,att:3,dif:10,dmg:'D6 − 1',kind:'Creatura'};
const GU={name:'Guardiano di MIMI',short:'Guardiano',pv:14,att:4,dif:13,dmg:'D6 + 1',icon:'forziere'};
const NL=10;
const DUR=[];const SAYT=[];
function say(who,text,fn,adv=0,extra=0){const w=text.replace(/<[^>]+>/g,'').split(/\s+/).length;const i=SAYT.length;const d=Math.max(clamp(w/3.0+1.2,3.0,8.5)+extra,(DUR[i]||0)+0.15+0.75);const bb=beat(d,who+'|'+text,fn,adv);SAYT.push(bb.t0);return bb}
const les=(b,n,name)=>b.at(0,s=>{s.les=[n,name]});
const hl=(b,dt,cells,col,d)=>b.item(dt,d,'hl',{cells,col});
const hlr=(b,dt,r,d)=>b.item(dt,d,'hlrect',r);
const both=L=>L.flatMap(p=>[[p[0],p[1]],[9-p[0],9-p[1]]]);
const QS=both([[6,0],[8,0],[1,1],[3,1],[6,1],[2,2],[5,2],[8,2],[9,1],[4,3],[7,3],[8,3],[0,3],[2,4],[5,4]]);
const CAOS=both([[4,0],[3,2],[7,4],[4,4],[9,2]]);
const EDI=both([[1,4],[4,1],[8,1]]);
const W_=GEOM.W, SALA={x:6,y:4,w:GEOM.bw-12,h:W_*4.05}, GIRO={x:GEOM.giro.g0-W_*1.3,y:GEOM.giro.gy-W_*0.25,w:20*GEOM.giro.gx+W_*1.5,h:GEOM.giro.gx*2};
const PROM={x:10,y:GEOM.Y0+9*GEOM.step+2*GEOM.R+W_*0.2,w:GEOM.bw-20,h:W_*2.3};

// COPERTINA
beat(6.5,'',b=>{b.item(0,6.5,'cover',{a:'IL TESORO DEL GOBLIN',b:'Impariamo<br>a giocare',c:'Lia e Marco spiegano il gioco a Giulia, alla sua prima partita',d:'Scatola base · regolamento v4.0 da tavolo'})});

// 1 OBIETTIVO
say('G','Allora, ragazzi, come si vince a questo gioco?',b=>{les(b,1,'Lo scopo del gioco');st(b,0,{title:'Lo scopo',sub:'chi vince e come'});b.at(0,s=>s.boardOn=b.t0);
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:12px"><svg viewBox="0 0 24 24" width="120" height="120">${ICONS.forziere}</svg><div class="big">Ritrova MIMI</div></div>`})});
say('M','Raccogli <b>3 Indizi</b>, scopri in quale <b>Cripta</b> è nascosto MIMI, il forziere di Geronimo, e sconfiggi il suo <b>Guardiano</b>. Chi ci riesce per primo vince.',b=>{hl(b,0.3,CRIP,'#b8862b');
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:22px"><span class="chip">${IC('pergamena',34)} 3 Indizi</span><span style="font-size:40px;color:#b8862b">→</span><span class="chip">${IC('cripta',34)} la Cripta giusta</span><span style="font-size:40px;color:#b8862b">→</span><span class="chip">${IC('forziere',34)} batti il Guardiano</span></div>`})});
say('L','Gli Indizi li trovi battendo i mostri, sui Caos del Goblin e in altri modi che vedrai giocando.',b=>{hl(b,0.2,CAOS,'#7a3e8e')});

// 2 PLANCIA
say('M','Questa è la plancia: 10 × 10 esagoni. I numeri viola sul bordo sono le <b>6 partenze</b>.',b=>{les(b,2,'La plancia');st(b,0,{title:'La plancia',sub:'«Le Terre di Hande»'});hl(b,0.3,SPAWN,'#7a4f86')});
say('L','Le caselle col <b>punto di domanda</b> si esplorano: quando ti fermi lì, peschi un segnalino dal sacchetto.',b=>{hl(b,0.2,QS,'#2a2118')});
say('M','Il dado viola è il <b>Caos del Goblin</b>: tiri il D6 e succede qualcosa, nel bene o nel male.',b=>{hl(b,0.2,CAOS,'#7a3e8e')});
say('L','<b>Locanda, Fonte e Fabbro</b> ti aiutano. Ognuno di noi li può usare una volta sola a partita.',b=>{hl(b,0.2,EDI,'#c0662b');
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:22px"><span class="chip">${IC('casa',30)} Locanda: +1 PE, +2 PV</span><span class="chip">${IC('goccia',30)} Fonte: 2 carte dagli scarti</span><span class="chip">${IC('martello',30)} Fabbro: 1 oggetto dagli scarti</span></div>`})});
say('G','E i quattro esagoni dorati con i numeri?',b=>{hl(b,0.2,CRIP,'#b8862b')});
say('M','Sono le <b>Cripte</b>. MIMI è in una di queste, ma si scopre quale solo quando qualcuno arriva a 3 Indizi.',b=>{hl(b,0,CRIP,'#b8862b')});
say('L','In alto c’è la <b>Sala del Tesoro</b>, con il Guardiano e i mini-boss. In basso il promemoria e il <b>tracciato dei giri</b>.',b=>{b.at(0,s=>{s.salaOn=b.t0});hlr(b,0.2,SALA,2.6);hlr(b,2.8,GIRO,null)});

// 3 PREPARAZIONE
say('L','Prepariamo. I <b>30 segnalini</b> vanno tutti nel sacchetto, mescolati. Sulla mappa non si mette niente.',b=>{les(b,3,'La preparazione');st(b,0,{title:'Preparazione',sub:'circa 5 minuti'});
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:40px">${bagSVG()}<div style="display:flex;flex-direction:column;gap:12px;align-items:flex-start"><span class="chip">${IC('spade',28)} 13 Creature</span><span class="chip">${IC('teschio',28)} 4 Mini-boss</span><span class="chip">${IC('trappola',28)} 5 Trappole</span><span class="chip">${IC('piedi',28)} 8 Sentieri tranquilli</span></div></div>`})});
say('M','Un cubetto giallo va sul giro 1, l’altro sui <b>14 PV</b> del Guardiano.',b=>{b.at(0.6,s=>{s.cubesOn=true;s.giro=1;s.gpv=14});hlr(b,0.4,{x:SALA.x,y:GEOM.pvt.ty-W_*0.3,w:SALA.w,h:W_*1.2},null)});
say('L','Adesso scegli una classe. Nella scatola base ci sono Guerriero, Ladro, Mago e Chierico.',b=>{
  b.item(0,null,'cards',{stag:.25,cards:[{name:'Guerriero',col:'#a8352a',slot:'Classe',text:'+2 PV. Vinci uno scontro: Ispirazione.',w:200},{name:'Ladro',col:'#3d7a3f',slot:'Classe',text:'+3 MOV, +1 PV. Fuga gratis, vantaggio al primo round.',w:200},{name:'Mago',col:'#2f5d9c',slot:'Classe',text:'Ritira un tuo dado una volta per turno.',w:200},{name:'Chierico',col:'#b8862b',slot:'Classe',text:'A 0 PV torni in vita con 3 PV. Si ricarica in Locanda.',w:200}]})});
say('G','Prendo il <b>Ladro</b>, mi piace l’idea di poter scappare!',b=>{set(b,0.4,'S',{on:true,pv:11,pvm:11,mov:4})});
say('M','Ottima scelta per iniziare: <b>+3 MOV e +1 PV</b>, fuggire non ti costa niente e nel primo round di ogni scontro hai il <b>vantaggio</b>.',b=>{b.item(0,null,'cards',{cards:[{name:'Classe: Ladro',col:'#3d7a3f',slot:'Carta Classe',text:'+3 MOV, +1 PV. Fuggire non ha conseguenze; vantaggio nel primo round di ogni scontro.',w:300}],side:`<div class="lbl" style="text-align:left;color:#2a2118">Vantaggio: tiri due D20 e tieni il migliore.</div>`})});
say('L','Poi la <b>razza</b>. Ognuna dà dei bonus da aggiungere subito alla scheda.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr"><table style="font-family:'Alegreya Sans';font-size:25px;border-collapse:collapse;width:640px">${[['Umano','+1 MOV e +1 a una statistica'],['Elfo','+2 a una statistica'],['Nano','+1 a due statistiche diverse'],['Orco','+2 ATT e +1 PV']].map(r=>`<tr><td style="padding:7px 12px;border-bottom:2px solid #b9a582;font-weight:800">${r[0]}</td><td style="padding:7px 12px;border-bottom:2px solid #b9a582">${r[1]}</td></tr>`).join('')}</table></div>`})});
say('G','Umana, allora: +1 MOV e +1 all’AR.',b=>{set(b,0.6,'S',{mov:5,ar:2})});
say('L','Io gioco il Guerriero orco, Marco il Mago elfo. Ognuno prende la miniatura e il mazzetto del suo colore.',b=>{set(b,0.3,'L',{on:true,pv:13,pvm:13,att:3});set(b,1.3,'M',{on:true,att:3})});

// 4 SCHEDA
say('M','Questa è la tua <b>scheda</b>. I cubetti mostrano sempre il valore finale: PV, ATT, MOV e AR, oggetti compresi.',b=>{les(b,4,'La scheda eroe');st(b,0,{title:'La scheda',sub:'tiene il conto al posto tuo'});
  b.item(0,null,'html',{h:`<div class="ctr" style="padding:6px">${ART.scheda.replace('<svg ','<svg style="height:380px;width:auto" ')}</div>`})});
say('M','La <b>Difesa</b> è 10 più l’AR, ed è già stampata sotto la casella. È il numero che i mostri devono raggiungere per colpirti.',b=>{b.item(0,null,'html',{h:`<div class="ctr" style="padding:6px">${ART.scheda.replace('<svg ','<svg style="height:380px;width:auto" ')}</div>`})});
say('L','A destra ci sono gli Indizi, le Clessidre, l’Ispirazione e gli edifici che hai già usato. Li vedi anche qui sopra, nelle nostre schede.',b=>{b.item(0,null,'html',{h:`<div class="ctr" style="padding:6px">${ART.scheda.replace('<svg ','<svg style="height:380px;width:auto" ')}</div>`});b.item(0,null,'hlhero',{})});

// 5 PARTENZA E MANO
say('M','Ognuno tira il D6 per la partenza. Se il posto è occupato o è accanto a un altro eroe, si ritira.',b=>{les(b,5,'Partenza e carte');st(b,0,{title:'Partenza e carte',sub:''});
  dice(b,0.3,[{t:'D6',v:1,l:'Lia → 1',sz:100},{t:'D6',v:4,l:'Marco → 4',sz:100,dt:0.6},{t:'D6',v:1,l:'Giulia → 1, occupata',sz:100,dt:1.6,dim:1},{t:'D6',v:6,l:'ritira → 6',sz:100,dt:3}],'','',null);
  place(b,1,'L',...SPAWN[0]);place(b,1.6,'M',...SPAWN[3]);b.item(2.5,1.2,'ring',{c:2,r:0,col:'#9c2f24'});place(b,3.8,'S',...SPAWN[5])});
say('L','Ora la mano: <b>5 carte della tua classe e 5 del mazzo comune</b>, coperte. Guardale solo adesso: per tutta la partita non se ne pescano altre.',b=>{
  const backs=(col,lab)=>`<div style="text-align:center"><div style="display:flex">${[0,1,2,3,4].map(i=>`<div class="back" style="background:${col};margin-left:${i?-62:0}px;transform:rotate(${(i-2)*6}deg) translateY(${Math.abs(i-2)*6}px)">?</div>`).join('')}</div><div class="lbl" style="margin-top:18px">${lab}</div></div>`;
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:70px">${backs('#3d7a3f','5 dal mazzetto del Ladro')}${backs('#4a3a2a','5 dal mazzo comune')}</div>`});
  ['L','M','S'].forEach((k,i)=>set(b,1+i*0.3,k,{hand:10}))});
say('G','Solo dieci carte? Allora devo usarle bene.',b=>{});
say('M','Esatto. Puoi giocarne <b>fino a 2 per turno</b>, quando vuoi. E prima di cominciare equipaggiamo tutti subito un oggetto.',b=>{
  b.item(0,null,'cards',{cards:[{name:'Arco da guerra',slot:'Arma a due mani',text:'Danno D6 + 1',who:'Lia',w:240},{name:'Bacchetta nuova di zecca',slot:'Arma a una mano',text:'ATT +2<br>Danno D6',who:'Marco',deck:'Mago',w:240,col:'#2f5d9c'},{name:'Daga strana',slot:'Arma a una mano',text:'ATT +1<br>Danno D6',who:'Giulia',deck:'Ladro',w:240,col:'#3d7a3f'}]});
  set(b,1,'L',{arma:'Arco da guerra',hand:9});set(b,1.4,'M',{arma:'Bacchetta',hand:9,att:5});set(b,1.8,'S',{arma:'Daga strana',hand:9,att:2})});
say('L','La carta si infila sotto il bordo della scheda, nello slot giusto: <b>Elmo, Arma o Corpo</b>. Al massimo un equipaggiamento per turno.',b=>{b.item(0,null,'html',{h:`<div class="ctr" style="padding:6px">${ART.anatomy.replace('<svg ','<svg style="height:370px;width:auto" ')}</div>`})});
say('M','Chi ha visto per ultimo un goblin prende <b>Geronimo</b> e comincia. Lia?',b=>{});
say('L','Io! Stamattina, nello specchio.',b=>{set(b,0.4,'L',{ger:true})});

// 6 TURNO
say('M','Il turno ha sempre <b>5 passi</b>. Li trovi sulla plancia e sulla Carta Aiuto.',b=>{les(b,6,'Il turno in 5 passi');st(b,0,{title:'Il turno',sub:'sempre gli stessi 5 passi'});b.item(0,9999,'strip',{})});
say('L','Uno: se hai una <b>Clessidra</b>, la togli e salti il turno. Due: giochi le <b>carte</b> che vuoi, fino a 2.',b=>{b.at(0.3,s=>s.phase=0);b.at(2.6,s=>s.phase=1)});
say('L','Tre: ti <b>muovi</b>. Quattro: <b>esplori</b> dove ti sei fermata. Cinque: <b>fine</b>, passi i dadi a sinistra.',b=>{b.at(0.2,s=>s.phase=2);b.at(1.6,s=>s.phase=3);b.at(3.2,s=>s.phase=4);b.at(beatEnd(b),s=>s.phase=-1)});
ITEMS.forEach(i=>{if(i.kind==='strip'&&i.t1>T)i.t1=T});

// 7 MUOVERSI
say('L','Comincio io. Tiro il D6: 3, più il mio MOV 1. Posso fare fino a 4 esagoni.',b=>{les(b,7,'Muoversi ed esplorare');banner(b,'Giro 1');st(b,0,{title:'Giro 1 · Lia',sub:'muoversi'});b.at(0,s=>{s.playing=true});act(b,'L',2);
  dice(b,0.4,[{t:'D6',v:3,l:'3 + MOV 1 = 4'}],'','fino a 4 esagoni, almeno 1')});
say('G','Puoi passare sopra le caselle col punto di domanda?',b=>{b.item(0,null,'html',{h:`<div class="ctr">${ART.move.replace('<svg ','<svg style="width:900px;height:auto" ')}</div>`})});
say('L','Sì, puoi passare sopra a tutto. Conta solo l’esagono dove <b>ti fermi</b>. Mi fermo qui, dopo 2.',b=>{b.item(0,null,'html',{h:`<div class="ctr">${ART.move.replace('<svg ','<svg style="width:900px;height:auto" ')}</div>`});move(b,1.6,'L',[2,2])});
say('L','Casella «?»: pesco un segnalino dal sacchetto… un <b>Lupo grigio</b>!',b=>{phase(b,0,3);draw(b,0.6,{...LUPO,kind:'Creatura',desc:'5 PV · ATT +3 · Difesa 10'})});

// 8 SCONTRO
{const lines=[];
 say('M','Lo scontro: tiri il <b>D20 e aggiungi l’ATT</b>. Se arrivi alla Difesa del mostro, lo colpisci e tiri il danno.',b=>{les(b,8,'Lo scontro');st(b,0,{title:'Giro 1 · Lia',sub:'lo scontro'});combat(b,0,'L',LUPO,lines,40)});
 say('L','9 più 3 fa 12: almeno 10, colpito! Con l’Arco faccio D6 + 1: 3 danni.',b=>{atk(lines,b,0.2,{who:'Lia',col:'#a8352a',d20:9,mod:3,vs:10,hit:true,dmg:{die:'D6',v:2,expr:'2 + 1 ',total:3},target:'foe'})});
 say('M','Il <b>dado rosso</b> tiene il conto dei PV del lupo: da 5 scende a 2.',b=>{});
 say('G','E per il lupo chi tira?',b=>{});
 say('M','Il giocatore alla destra di chi combatte. Tocca a te, Giulia: D20 più l’ATT del lupo, contro la Difesa di Lia, 11.',b=>{});
 say('G','10 più 3, 13… l’ho presa! Danno: 4 meno 1, 3. Scusa, Lia!',b=>{atk(lines,b,0.1,{who:'Lupo',roller:'Giulia',d20:10,mod:3,vs:11,hit:true,dmg:{die:'D6',v:4,expr:'4 − 1 ',total:3},target:'L'})});
 say('L','Tranquilla! Secondo round: 15 più 3, colpito. 5 più 1 fa 6: il lupo è finito.',b=>{atk(lines,b,0.1,{who:'Lia',col:'#a8352a',d20:15,mod:3,vs:10,hit:true,dmg:{die:'D6',v:5,expr:'5 + 1 ',total:6},target:'foe'})});
 say('M','Ricorda: con <b>20 sul dado</b> colpisci sempre e il danno raddoppia, con <b>1</b> manchi sempre.',b=>{});
}
say('L','Vinto! Prendo <b>1 Indizio e 1 PE</b>. Da Guerriero guadagno anche l’<b>Ispirazione</b>. Un solo scontro per turno: ho finito.',b=>{phase(b,0,4);clue(b,0.6,'L');add(b,1.2,'L',{pe:1});set(b,1.8,'L',{insp:true});
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:30px"><span class="chip">${IC('pergamena',34)} +1 Indizio</span><span class="chip">${IC('stella',34)} +1 PE</span><span class="chip">${IC('stella',34)} Ispirazione</span></div>`})});

// 9 TRAPPOLE E CAOS
say('M','Tocca a me. 2 più 1: mi fermo su un «?»… <b>Trappola</b>.',b=>{les(b,9,'Trappole e Caos');st(b,0,{title:'Giro 1 · Marco',sub:'trappole'});act(b,'M',2);
  dice(b,0,[{t:'D6',v:2,l:'2 + 1 = 3',sz:90}],'','',1.6);move(b,0.5,'M',[7,7],1);b.at(1.6,s=>s.phase=3);draw(b,1.6,{name:'Trappola',icon:'trappola',kind:'Segnalino',title:'Trappola',desc:'Perdi D6 − 1 PV e tira la perdita.'})});
say('M','Perdo D6 meno 1 PV, poi tiro la <b>perdita</b>: 1 perdo tutto, 2 l’elmo, 3 l’arma, 4 il corpo, 5 o 6 niente.',b=>{hlr(b,0.3,PROM,null);
  dice(b,0.3,[{t:'D6',v:4,l:'danno: 4 − 1 = 3',sz:96},{t:'D6',v:5,l:'perdita: 5 = niente',sz:96,dt:2.6}],'Trappola','',null);add(b,1.2,'M',{pv:-3})});
say('G','Il mio turno! 4 più MOV 5… posso fare 9 esagoni?',b=>{st(b,0,{title:'Giro 1 · Giulia',sub:'il Caos del Goblin'});act(b,'S',2);dice(b,0,[{t:'D6',v:4,l:'4 + MOV 5 = 9'}],'','fino a 9 esagoni')});
say('L','Sì, il Ladro corre! Prova quel <b>Caos del Goblin</b> al centro.',b=>{move(b,0.3,'S',[4,4],1.4)});
say('M','Sul Caos tiri il D6. Ecco cosa può succedere.',b=>{phase(b,0,3);
  b.item(0,null,'html',{h:`<div class="it" style="padding:22px 30px;font-family:'Alegreya Sans';font-size:24px;line-height:1.5;color:#2a2118">${[['1','Crollo','perdi 2 PV'],['2','Imboscata','combatti un Coboldo'],['3','Vento del Goblin','muovi subito di altri D6 esagoni'],['4','Bottega','riprendi 1 carta dai tuoi scarti'],['5','Mappa perduta','prendi 1 Indizio'],['6','Scambio','se vuoi, scambiati di posto con un eroe']].map(r=>`<div style="display:flex;gap:14px;align-items:center;margin-bottom:6px">${die('D6',+r[0],0,-9,0,44)}<b style="min-width:220px">${r[1]}</b><span>${r[2]}</span></div>`).join('')}</div>`})});
say('G','Tiro… 5! <b>Mappa perduta</b>: il mio primo Indizio!',b=>{dice(b,0.2,[{t:'D6',v:5,l:'Caos del Goblin'}],'','5 · Mappa perduta: +1 Indizio');clue(b,1.4,'S')});
say('M','E la casella resta lì: chi si ferma dopo di te tira di nuovo.',b=>{phase(b,0,4)});

// 10 CARTE E DUELLO
{const lines=[];
 say('M','<b>Giro 2.</b> Mi fermo su uno Scheletro. Ti faccio vedere come si gioca una carta: <b>Dardo magico</b>.',b=>{les(b,10,'Carte e Duello');banner(b,'Giro 2');st(b,0,{title:'Giro 2 · Marco',sub:'giocare una carta'});b.at(0,s=>s.giro=2);act(b,'M',2);move(b,0.2,'M',[5,6],1);b.at(1.2,s=>s.phase=3);
  const SK={name:'Scheletro',pv:5,att:2,dif:11,dmg:'D6 − 1'};combat(b,1.2,'M',SK,lines,13);
  lines.push({dt:b.t0+2.6,who:'Marco',col:'#2f5d9c',text:'<span class="note">gioca Dardo magico: 2 danni, Difesa −1</span>'});b.at(2.8,s=>{s.foe.pv-=2;s.foe.dif0=11;s.foe.dif=10});add(b,2.8,'M',{hand:-1})});
 say('M','Il nemico subisce 2 danni e la sua Difesa scende a 10. La carta poi va nei miei <b>scarti</b>, a faccia in su.',b=>{});
 say('L','Per lo Scheletro tiro io, che siedo alla destra di Marco.',b=>{atk(lines,b,0.3,{who:'Marco',col:'#2f5d9c',d20:12,mod:5,vs:10,hit:true,dmg:{die:'D6',v:3,expr:'',total:3},target:'foe'})},0,0.8);
 say('M','Colpito, ed è già finito: secondo Indizio della partita, il mio primo.',b=>{clue(b,0.6,'M');add(b,0.6,'M',{pe:1})});
}
say('G','Mi muovo… e mi fermo proprio accanto a Marco.',b=>{st(b,0,{title:'Giro 2 · Giulia',sub:'il Duello'});act(b,'S',2);move(b,0.2,'S',[4,6],1);b.at(1.2,s=>s.phase=3);b.item(1.2,3,'ring',{c:5,r:6,col:'#2f5d9c'})});
say('L','Allora c’è il <b>Duello</b>! Se finisci accanto a un eroe e non hai avuto altri scontri, lo sfidi.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:50px"><div class="big" style="width:280px">Duello!</div><div class="lbl" style="width:520px;text-align:left;color:#2a2118;font-size:24px">Chi vince prende <b>1 Indizio</b> allo sconfitto, <b>1 carta</b> dai suoi scarti, <b>1 PE</b> e l’<b>Ispirazione</b>. Chi perde subisce una sconfitta normale.</div></div>`})});
say('M','Rifiuto: in cambio peschi <b>1 carta a caso</b> dalla mia mano. Ecco, tienila.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:50px"><div style="text-align:center"><div class="back" style="background:#2f5d9c;margin:auto">?</div><div class="lbl" style="margin-top:12px">1 carta a caso<br>da Marco a Giulia</div></div></div>`});add(b,1.6,'M',{hand:-1});add(b,1.9,'S',{hand:1})});

// 11 SCONFITTA
{const lines=[];const OG={name:'Ogre delle paludi',short:'Ogre',pv:12,att:3,dif:11,dmg:'D6 + 1',icon:'teschio'};
 say('L','<b>Giro 3.</b> Che sfortuna: un <b>Mini-boss</b>! Prendo l’Ogre dalla Sala del Tesoro e lo metto qui.',b=>{les(b,11,'Mini-boss e sconfitta');banner(b,'Giro 3');st(b,0,{title:'Giro 3 · Lia',sub:'mini-boss'});b.at(0,s=>s.giro=3);act(b,'L',2);move(b,0.2,'L',[5,4],0.8);
  b.at(1,s=>s.phase=3);draw(b,1,{name:'Mini-boss',icon:'teschio',kind:'Segnalino',title:'Ogre delle paludi',desc:'12 PV · ATT +3 · Difesa 11 · danno D6 + 1'});
  b.at(2.6,s=>{s.sala.Ogre=false;s.tok.push({id:'ogre',c:5,r:4,kind:'boss',label:'Ogre',from:salaPos(2),t0:b.t0+2.6,dur:1.2})})});
 say('L','Uso l’Ispirazione del Guerriero: la sua Difesa scende di 2. Colpito, 6 danni!',b=>{combat(b,0,'L',OG,lines,22);b.at(0.4,s=>{s.foe.dif0=11;s.foe.dif=9;s.H.L.insp=false});lines.push({dt:b.t0+0.4,who:'Lia',col:'#a8352a',text:'<span class="note">Ispirazione: Difesa dell’Ogre −2</span>'});
  atk(lines,b,1.4,{who:'Lia',col:'#a8352a',d20:13,mod:3,vs:9,hit:true,dmg:{die:'D6',v:5,expr:'5 + 1 ',total:6},target:'foe'})},0,0.6);
 say('G','Tiro io per l’Ogre: 14 più 3, colpita… 5 danni.',b=>{atk(lines,b,0.2,{who:'Ogre',roller:'Giulia',d20:14,mod:3,vs:11,hit:true,dmg:{die:'D6',v:4,expr:'4 + 1 ',total:5},target:'L'})});
 say('G','Lia, sei a 5 PV. Non conviene scappare?',b=>{});
 say('M','Prima di ogni tuo attacco puoi <b>fuggire</b>: torni da dove sei arrivata, senza ricompensa, e il turno finisce.',b=>{});
 say('L','Ci provo lo stesso… 4 più 3, mancato.',b=>{atk(lines,b,0.2,{who:'Lia',col:'#a8352a',d20:4,mod:3,vs:9,hit:false})});
 say('G','E l’Ogre fa 9 più 3, 12… colpita di nuovo. 6 danni.',b=>{atk(lines,b,0.2,{who:'Ogre',roller:'Giulia',d20:9,mod:3,vs:11,hit:true,dmg:{die:'D6',v:5,expr:'5 + 1 ',total:6},target:'L'})});
}
say('L','Zero PV: <b>sconfitta</b>. Non sei eliminata: tiri il D6 per ripartire e torni ai PV massimi. Gli Indizi restano tuoi.',b=>{b.at(0,s=>{s.H.L.down=true});
  dice(b,0.3,[{t:'D6',v:3,l:'ripartenza → 3 (J5)',sz:100}],'Sconfitta','',null);
  b.at(1.3,s=>{const h=s.H.L;h.down=false;s.anim.L={p:[[9,4]],t0:b.t0+1.3,dur:.01,drop:true};h.c=9;h.r=4;h.pv=13});b.item(1.3,2,'ring',{c:9,r:4,col:'#a8352a'})});
say('M','Poi tiri la perdita: 3, l’Arco va negli scarti. E l’Ogre resta lì, con tutti i suoi PV, per il prossimo che passa.',b=>{
  dice(b,0.2,[{t:'D6',v:3,l:'perdita: 3 = Arma',sz:100}],'','',null);set(b,1,'L',{arma:'—'})});

// 12 LIVELLI E FUGA
say('M','Io vado alla <b>Locanda</b>: +1 PE e 2 PV. Con 2 PE arrivo alla casella dorata e salgo al <b>livello 2</b>.',b=>{les(b,12,'Livelli e fuga');st(b,0,{title:'Giro 3 · Marco',sub:'salire di livello'});act(b,'M',2);
  dice(b,0,[{t:'D6',v:4,l:'4 + 1 = 5',sz:90}],'','',1.4);move(b,0.4,'M',[1,4],1.2);b.at(1.6,s=>s.phase=3);add(b,2,'M',{pe:1});
  b.at(2.6,s=>{const h=s.H.M;h.lv=2;h.pvm+=1;h.pv+=1;h.mov+=1;h.used.push('casa')});add(b,3.2,'M',{pv:2})});
say('L','A ogni livello: <b>+1 ai PV massimi</b> e +1 a ATT, MOV o AR, a scelta. Il livello massimo è 5.',b=>{b.item(0,null,'html',{h:`<div class="ctr" style="gap:28px"><span class="chip">${IC('stella',34)} PE 2 · 4 · 6 · 8 = livello</span><span class="chip">${IC('cuore',34)} +1 PV max</span><span class="chip">${IC('spade',34)} +1 ATT, MOV o AR</span></div>`})});
say('G','Io trovo un <b>Ragno delle grotte</b>… e scappo! Il Ladro fugge gratis.',b=>{st(b,0,{title:'Giro 3 · Giulia',sub:'la fuga'});act(b,'S',2);move(b,0,'S',[1,7],1);b.at(1,s=>s.phase=3);
  draw(b,1,{name:'Ragno delle grotte',pv:5,att:'+3',dif:11,dmg:'D6 − 1',kind:'Creatura',desc:'Giulia fugge: torna indietro di un esagono.'});
  b.at(3,s=>{const p=s.anim.S.p;const back=p[p.length-2];s.anim.S={p:[[1,7],back],t0:b.t0+3,dur:0.6};s.H.S.c=back[0];s.H.S.r=back[1];s.tok.push({id:'ragno',c:1,r:7,kind:'crea',label:'Ragno'})})});
say('M','Il ragno resta scoperto sulla mappa. Chi si ferma lì dopo lo dovrà affrontare.',b=>{});

// 13 AVANTI VELOCE
say('L','Facciamo un salto in avanti. Io passo dal <b>Fabbro</b> e mi riprendo l’Arco, Marco batte un Orchetto e arriva a 2 Indizi.',b=>{les(b,13,'Il tesoro');banner(b,'Giri 4 e 5','avanti veloce',2.4);st(b,0,{title:'Giri 4 e 5',sub:'avanti veloce'});b.at(0,s=>{s.giro=4;s.active=null;s.phase=-1});
  move(b,0.4,'L',[8,1],1);b.at(1.4,s=>{s.H.L.arma='Arco da guerra';s.H.L.used.push('martello')});
  move(b,1.6,'M',[2,4],0.6);b.at(2.4,s=>{const h=s.H.M;h.ind=2;h.newInd=b.t0+2.4;h.pe=3});
  move(b,2.8,'S',[3,8],1);b.at(3.8,s=>s.giro=5);move(b,4.2,'L',[7,3],0.8)},0,0.6);
{const lines=[];
 say('M','<b>Giro 5.</b> Batto un Ratto gigante: è il mio <b>terzo Indizio</b>! E con 4 PE salgo anche al livello 3.',b=>{act(b,'M',2);move(b,0,'M',[2,2],0.6);b.at(0.7,s=>s.phase=3);
  const RA={name:'Ratto gigante',short:'Ratto',pv:3,att:2,dif:10,dmg:'D6 − 1'};combat(b,0.7,'M',RA,lines,null);
  atk(lines,b,0.8,{who:'Marco',col:'#2f5d9c',d20:6,mod:5,vs:10,hit:true,dmg:{die:'D6',v:1,expr:'',total:1},target:'foe'});
  atk(lines,b,1.8,{who:'Ratto',roller:'Lia',d20:14,mod:2,vs:11,hit:true,dmg:{die:'D6',v:3,expr:'3 − 1 ',total:2},target:'M'});
  atk(lines,b,2.8,{who:'Marco',col:'#2f5d9c',d20:17,mod:5,vs:10,hit:true,dmg:{die:'D6',v:4,expr:'',total:4},target:'foe'});
  clue(b,4,'M');add(b,4,'M',{pe:1});b.at(4.6,s=>{const h=s.H.M;h.lv=3;h.pvm+=1;h.pv+=1;h.att+=1})},0,1.5);}
say('L','Marco ha individuato il tesoro. E allora <b>la voce si sparge</b>: io e Giulia prendiamo subito 1 Indizio a testa.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:22px"><div class="big">La voce si sparge</div><div style="display:flex;gap:40px"><span class="chip" style="border-color:#a8352a">${IC('pergamena',34)} Lia +1</span><span class="chip" style="border-color:#3d7a3f">${IC('pergamena',34)} Giulia +1</span></div></div>`});
  clue(b,1.4,'L');clue(b,1.8,'S')});
say('M','Ora il D6 dice dov’è MIMI. Con 5 o 6 si ritira… 5, ritiro. <b>3!</b> MIMI e il Guardiano vanno sulla Cripta 3.',b=>{
  dice(b,0,[{t:'D6',v:5,l:'5 → si ritira',sz:100,dim:1},{t:'D6',v:3,l:'Cripta 3',sz:100,dt:2.2}],'Dov’è MIMI?','',null);
  b.at(3.6,s=>{s.sala.Guardiano=false;s.sala.MIMI=false;s.tok.push({id:'guard',c:3,r:6,kind:'guard',from:salaPos(0),t0:b.t0+3.6,dur:1.3});s.tok.push({id:'mimi',c:3,r:6,kind:'mimi',from:salaPos(1),t0:b.t0+3.8,dur:1.3})});
  b.item(3.6,4,'ring',{c:3,r:6,col:'#b8862b',delay:1.3})});
say('G','Quindi adesso lo sappiamo tutti dov’è il tesoro?',b=>{});
say('M','Sì, ma solo chi ha <b>3 Indizi</b> può sfidare il Guardiano. Voi due ne avete 2.',b=>{});

// 14 GUARDIANO
{const lines=[];
 say('M','<b>Giro 6.</b> Raggiungo la Cripta 3 e sfido il Guardiano: <b>14 PV, ATT +4, Difesa 13</b>, danno D6 + 1.',b=>{les(b,14,'Il Guardiano');banner(b,'Giro 6');st(b,0,{title:'Giro 6 · Marco',sub:'il Guardiano di MIMI'});
  b.at(0,s=>{s.giro=6;s.H.S.c=1;s.H.S.r=4;s.anim.S={p:[[3,8],[2,7],[2,6],[1,5],[1,4]],t0:b.t0,dur:1};s.H.S.pe=1;s.H.S.used.push('casa')});
  act(b,'M',2);dice(b,0,[{t:'D6',v:2,l:'2 + MOV 2 = 4',sz:90}],'','',1.4);move(b,0.4,'M',[3,6],1.1);b.at(1.5,s=>s.phase=3);combat(b,1.5,'M',GU,lines,null)},0,0.6);
 say('M','4 più 6, mancato. Ma il <b>Mago può ritirare</b> un suo dado una volta per turno… 15: colpito!',b=>{
  atk(lines,b,0.3,{who:'Marco',col:'#2f5d9c',d20:4,reroll:15,mod:6,vs:13,hit:true,dmg:{die:'D6',v:4,expr:'',total:4},target:'foe'})},0,0.8);
 say('L','Tiro io per il Guardiano: 16 più 4, colpito. 6 danni, Marco.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Lia',d20:16,mod:4,vs:11,hit:true,dmg:{die:'D6',v:5,expr:'5 + 1 ',total:6},target:'M'})});
 say('G','E adesso scappi?',b=>{});
 say('M','Dal Guardiano può fuggire <b>solo il Ladro</b>. Io devo continuare.',b=>{});
 say('M','11 più 6, colpito: lo porto a 8 PV…',b=>{atk(lines,b,0.2,{who:'Marco',col:'#2f5d9c',d20:11,mod:6,vs:13,hit:true,dmg:{die:'D6',v:2,expr:'',total:2},target:'foe'})});
 say('L','…e il Guardiano fa 12 più 4, colpito di nuovo. Marco, sei a terra.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Lia',d20:12,mod:4,vs:11,hit:true,dmg:{die:'D6',v:3,expr:'3 + 1 ',total:4},target:'M'})});
}
say('M','Però le <b>ferite del Guardiano restano</b>: il cubetto giallo scende a 8. Io riparto da H1 e tengo i miei 3 Indizi.',b=>{
  b.at(0.3,s=>{s.gpvAnim={from:14,to:8,t0:b.t0+0.3,dur:1.6};s.gpv=8});hlr(b,0.2,{x:SALA.x,y:GEOM.pvt.ty-W_*0.3,w:SALA.w,h:W_*1.2},3);
  dice(b,2,[{t:'D6',v:2,l:'ripartenza → 2 (H1)',sz:96},{t:'D6',v:6,l:'perdita: 6 = niente',sz:96,dt:0.8}],'','',null);
  b.at(2.8,s=>{const h=s.H.M;s.anim.M={p:[[7,0]],t0:b.t0+2.8,dur:.01,drop:true};h.c=7;h.r=0;h.pv=h.pvm});b.item(2.8,2,'ring',{c:7,r:0,col:'#2f5d9c'})});
say('G','Allora io mi metto qui, accanto alla Cripta, e aspetto il terzo Indizio. Ahi, un Caos: <b>Crollo</b>, −2 PV.',b=>{act(b,'S',2);move(b,0,'S',[2,5],0.9);b.at(0.9,s=>s.phase=3);
  dice(b,1.4,[{t:'D6',v:1,l:'Caos → 1 Crollo: −2 PV'}],'','',null);add(b,2.4,'S',{pv:-2})});

// 15 CLESSIDRE
say('L','<b>Giro 7.</b> Bevo la <b>Pozione del tempo</b>: ogni avversario perde 1 turno.',b=>{les(b,15,'Clessidre');banner(b,'Giro 7');st(b,0,{title:'Giro 7 · Lia',sub:'le Clessidre'});b.at(0,s=>{s.giro=7;s.H.L.c=7;s.H.L.r=5;s.anim.L={p:[[7,3],[7,4],[7,5]],t0:b.t0,dur:.8}});act(b,'L',1);
  b.item(0.3,null,'cards',{cards:[{name:'Pozione del tempo',slot:'Pozione · carta comune',text:'Recuperi 2 turni oppure ogni avversario perde 1 turno.',w:250}]});add(b,1.4,'L',{hand:-1})});
say('M','Ognuno di noi due mette una <b>Clessidra</b> sulla scheda. Al nostro turno la togliamo e saltiamo tutto, fino al passo 5.',b=>{set(b,0.4,'M',{cless:1});set(b,0.8,'S',{cless:1});
  b.at(1.4,s=>s.phase=2);move(b,1.4,'L',[5,6],1);b.at(3,s=>{s.active='M';s.phase=0});set(b,3.6,'M',{cless:0});b.at(4.4,s=>{s.active='S';s.phase=0});set(b,5,'S',{cless:0});b.at(5.6,s=>s.phase=4)});
say('L','Per colpa degli avversari non puoi avere più di <b>3 Clessidre</b>. Quelle in più non si mettono.',b=>{});

// 16 PRESAGIO E VITTORIA
say('M','<b>Giro 8.</b> Da qui parte il <b>Presagio del Goblin</b>: a inizio turno, chi non ha 3 Indizi tira il D6. Con 6 prende un Indizio.',b=>{les(b,16,'Presagio e vittoria');banner(b,'Giro 8','Presagio del Goblin',2.4);st(b,0,{title:'Giro 8',sub:'Presagio del Goblin'});b.at(0,s=>{s.giro=8;s.active='L';s.phase=0});hlr(b,0.3,GIRO,null)});
say('L','Più passano i giri, più è facile: dal giro 11 basta un 5, poi un 4… Io faccio 4: niente.',b=>{hlr(b,0,GIRO,null);dice(b,1.6,[{t:'D6',v:4,l:'Presagio: serve 6'}],'','niente Indizio');b.at(3.4,s=>s.phase=2);move(b,3.6,'L',[4,6],0.7)});
say('M','Io tiro 1 più 2: la Cripta è troppo lontana.',b=>{act(b,'M',2);dice(b,0,[{t:'D6',v:1,l:'1 + 2 = 3'}],'','',null);move(b,1,'M',[5,3],1)});
say('G','Tocca a me, ho 2 Indizi. Presagio… <b>6!</b> Terzo Indizio!',b=>{act(b,'S',0);dice(b,0.3,[{t:'D6',v:6,l:'Presagio: serve 6',dur:1.4}],'','6! +1 Indizio');clue(b,2,'S')});
{const lines=[];
 say('L','E sei proprio accanto alla Cripta. Il Guardiano ha ancora le ferite di Marco: <b>8 PV</b>.',b=>{phase(b,0,2);move(b,0.2,'S',[3,6],0.6);b.at(0.9,s=>s.phase=3);combat(b,1,'S',{...GU,pv0:8},lines,40)});
 say('M','Primo round: hai il <b>vantaggio del Ladro</b>. Tira due D20 e tieni il migliore.',b=>{});
 say('G','7 e 17: tengo il 17. Più 2, 19: colpito! Con la Daga, 4 danni.',b=>{atk(lines,b,0.2,{who:'Giulia',col:'#3d7a3f',d20:17,adv:[7,17],mod:2,vs:13,hit:true,dmg:{die:'D6',v:4,expr:'',total:4},target:'foe'})});
 say('M','Tiro io per il Guardiano: 15 più 4. Colpita, 6 danni. Sei a 3 PV.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Marco',d20:15,mod:4,vs:12,hit:true,dmg:{die:'D6',v:5,expr:'5 + 1 ',total:6},target:'S'})});
 say('G','Secondo round… 9 più 2, mancato. E tu?',b=>{atk(lines,b,0.2,{who:'Giulia',col:'#3d7a3f',d20:9,mod:2,vs:13,hit:false})});
 say('M','6 più 4, 10: mancato anch’io. Dai, tira!',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Marco',d20:6,mod:4,vs:12,hit:false})});
 say('G','<b>20!</b> Colpo sicuro e danno doppio: 3 per 2, 6. Il Guardiano è a zero!',b=>{atk(lines,b,0.2,{who:'Giulia',col:'#3d7a3f',d20:20,mod:2,vs:13,hit:true,dmg:{die:'D6',v:3,expr:'3 × 2 ',total:6},target:'foe'})},0,0.6);
}
say('L','Giulia riporta MIMI a Geronimo e <b>vince</b>. Alla prima partita!',b=>{st(b,0,{title:'Vittoria!',sub:'Giulia · Ladro umana'});b.at(0,s=>{s.phase=-1;s.tok=s.tok.filter(k=>k.kind!=='guard')});
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:10px"><svg viewBox="0 0 24 24" width="150" height="150">${ICONS.forziere}</svg><div class="big" style="font-size:52px">Giulia vince!</div></div>`})});
say('M','Fortuna del principiante. Rivincita?',b=>{});
beat(10,'',b=>{b.item(0,10,'recap',{})});
