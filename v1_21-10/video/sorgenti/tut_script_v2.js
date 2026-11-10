// ---------------- tutorial: Lia e Marco spiegano il gioco a Giulia (regolamento v5, Carte Trama v2) ----------------
S0.H.S.name='Giulia';S0.H.S.race='Umana';
const LUPO={name:'Lupo grigio',short:'Lupo',pv:3,att:3,dif:14,dmg:'D6 − 1'};
const COB={name:'Coboldo',short:'Coboldo',pv:2,att:1,dif:14,dmg:'D6 − 1'};
const ORSO={name:'Orso delle caverne',short:'Orso',pv:7,att:3,dif:14,dmg:'D6 + 1'};
const SCH={name:'Scheletro',short:'Scheletro',pv:2,att:2,dif:15,dmg:'D6 − 1'};
const GOB={name:'Goblin predone',short:'Goblin',pv:2,att:2,dif:15,dmg:'D6 − 1'};
const GU={name:'Guardiano di MIMI',short:'Guardiano',pv:9,att:4,dif:17,dmg:'D6 + 1',icon:'forziere'};
const NC=(o)=>({lv:1,ab:'',rew:['1 Indizio','1 PE'],...o});
const NL=10;
const DUR=[];const SAYT=[];
function say(who,text,fn,adv=0,extra=0){const w=text.replace(/<[^>]+>/g,'').split(/\s+/).length;const i=SAYT.length;const d=Math.max(clamp(w/3.0+1.2,3.0,8.5)+extra,(DUR[i]||0)+0.15+0.75);const bb=beat(d,who+'|'+text,fn,adv);SAYT.push(bb.t0);return bb}
const les=(b,n,name)=>b.at(0,s=>{s.les=[n,name]});
const hl=(b,dt,cells,col,d)=>b.item(dt,d,'hl',{cells,col});
const hlr=(b,dt,r,d)=>b.item(dt,d,'hlrect',r);
const both=L=>L.flatMap(p=>[[p[0],p[1]],[9-p[0],9-p[1]]]);
const QS=both([[6,0],[8,0],[1,1],[3,1],[6,1],[2,2],[5,2],[8,2],[9,1],[4,3],[7,3],[8,3],[0,3],[2,4],[5,4]]);
const EDI=both([[1,4],[4,1],[8,1]]);
const W_=GEOM.W, SALA={x:6,y:4,w:GEOM.bw-12,h:W_*4.05};
const PROM={x:10,y:GEOM.Y0+9*GEOM.step+2*GEOM.R+W_*0.2,w:GEOM.bw-20,h:W_*2.3};
const PVT={x:SALA.x,y:GEOM.pvt.ty-W_*0.3,w:SALA.w,h:W_*1.2};
const SCHEDA=()=>`<div class="ctr" style="padding:6px">${ART.scheda.replace('<svg ','<svg style="height:380px;width:auto" ')}</div>`;

// COPERTINA
beat(6.5,'',b=>{b.item(0,6.5,'cover',{a:'IL TESORO DEL GOBLIN',b:'Impariamo<br>a giocare',c:'Lia e Marco spiegano il gioco a Giulia, alla sua prima partita',d:'Un gioco di Alessandro De Simone · scatola base · regolamento v5'})});

// 1 OBIETTIVO
say('G','Allora, ragazzi, come si vince a questo gioco?',b=>{les(b,1,'Lo scopo del gioco');st(b,0,{title:'Lo scopo',sub:'chi vince e come'});b.at(0,s=>s.boardOn=b.t0);
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:12px"><svg viewBox="0 0 24 24" width="120" height="120">${ICONS.forziere}</svg><div class="big">Ritrova MIMI</div></div>`})});
say('M','Raccogli <b>2 Indizi</b>, scopri in quale <b>Cripta</b> è nascosto MIMI, il forziere di Geronimo, e sconfiggi il <b>boss</b> che lo custodisce. Chi ci riesce per primo vince.',b=>{hl(b,0.3,CRIP,'#b8862b');
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:22px"><span class="chip">${IC('pergamena',34)} 2 Indizi</span><span style="font-size:40px;color:#b8862b">→</span><span class="chip">${IC('cripta',34)} la Cripta giusta</span><span style="font-size:40px;color:#b8862b">→</span><span class="chip">${IC('forziere',34)} batti il boss</span></div>`})});
say('L','Gli Indizi si prendono in un modo solo: vincendo uno scontro su una casella col punto di domanda, oppure un Duello.',b=>{hl(b,0.2,QS,'#2a2118')});

// 2 PLANCIA
say('M','Questa è la plancia: 10 × 10 esagoni. I numeri viola sul bordo sono le <b>6 partenze</b>.',b=>{les(b,2,'La plancia');st(b,0,{title:'La plancia',sub:'«Le Terre di Hande»'});hl(b,0.3,SPAWN,'#7a4f86')});
say('L','Le caselle col <b>punto di domanda</b> si esplorano: quando ti fermi lì, peschi un segnalino dal sacchetto.',b=>{hl(b,0.2,QS,'#2a2118')});
say('L','<b>Locanda, Fonte e Fabbro</b> ti aiutano. Ognuno di noi li può usare una volta sola a partita.',b=>{hl(b,0.2,EDI,'#c0662b');
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:22px"><span class="chip">${IC('casa',30)} Locanda: +1 PE, +2 PV</span><span class="chip">${IC('goccia',30)} Fonte: 2 carte dagli scarti</span><span class="chip">${IC('martello',30)} Fabbro: 1 oggetto dagli scarti</span></div>`})});
say('G','E i quattro esagoni dorati con i numeri?',b=>{hl(b,0.2,CRIP,'#b8862b')});
say('M','Sono le <b>Cripte</b>. MIMI è in una di queste, ma si scopre quale solo quando qualcuno arriva a 2 Indizi.',b=>{hl(b,0,CRIP,'#b8862b')});
say('L','In alto c’è la <b>Sala del Tesoro</b>, dove aspettano il boss e MIMI. In basso il <b>promemoria</b> del turno.',b=>{b.at(0,s=>{s.salaOn=b.t0});hlr(b,0.2,SALA,2.6);hlr(b,2.8,PROM,null)});

// 3 PREPARAZIONE
say('L','Prepariamo. I <b>30 segnalini</b> vanno tutti nel sacchetto, mescolati. Sulla mappa non si mette niente.',b=>{les(b,3,'La preparazione');st(b,0,{title:'Preparazione',sub:'circa 5 minuti'});
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:40px">${bagSVG()}<div style="display:flex;flex-direction:column;gap:12px;align-items:flex-start"><span class="chip">${IC('spade',28)} 19 Nemico I</span><span class="chip">${IC('teschio',28)} 6 Nemico II</span><span class="chip">${IC('trappola',28)} 5 Trappole</span></div></div>`})});
say('M','Accanto, coperti, i due mazzetti dei <b>Nemici</b>: nel mazzetto I i nemici di livello 1 e 2, nel mazzetto II quelli di livello 3 e 4.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:60px">${[['#5b4a36','I','LV 1 e 2'],['#3e2c1f','II','LV 3 e 4']].map(([c,n,l])=>`<div style="text-align:center"><div class="back" style="background:${c};font-family:Cinzel">${n}</div><div class="lbl" style="margin-top:14px">Mazzetto ${n}<br>${l}</div></div>`).join('')}</div>`})});
say('L','Poi si pesca a caso uno dei <b>3 Boss</b>. Oggi c’è il <b>Guardiano di MIMI</b>: 9 PV. Il cubetto giallo va sui suoi PV.',b=>{
  b.item(0,null,'ncard',{c:NC({name:'Guardiano di MIMI',letter:'G',lv:5,pv:9,att:4,ar:3,dmg:'D6 + 1',ab:'Colpo del custode: se ti colpisce con un 6 al dado del danno, fai subito il tiro di perdita.',rew:['MIMI: vinci la partita'],tipo:'Boss'})});
  b.at(2.4,s=>{s.cubesOn=true;s.gpv=9});hlr(b,2.2,PVT,null)});

// 4 CLASSI E SPECIE
say('L','Adesso scegli una classe. Nella scatola base ci sono Guerriero, Ladro, Mago e Oracolo.',b=>{les(b,4,'Classi e specie');st(b,0,{title:'Classe e specie',sub:'chi sei in questa partita'});
  b.item(0,null,'cards',{stag:.25,cards:[{name:'Guerriero',col:'#a8352a',slot:'Classe',text:'+2 PV. Vinci uno scontro: Ispirazione.',w:200},{name:'Ladro',col:'#3d7a3f',slot:'Classe',text:'+2 MOV. Fugge da ogni scontro senza arretrare.',w:200},{name:'Mago',col:'#2f5d9c',slot:'Classe',text:'Ritira i suoi dadi fino a 2 volte per turno.',w:200},{name:'Oracolo',col:'#b8862b',slot:'Classe',text:'A 0 PV torna in vita con 3 PV. Si ricarica in Locanda.',w:200}]})});
say('G','Prendo il <b>Ladro</b>, mi piace l’idea di poter scappare!',b=>{set(b,0.4,'S',{on:true,mov:3})});
say('M','Ottima scelta per iniziare: <b>+2 MOV</b>, e puoi fuggire da qualsiasi scontro, anche dal boss, senza tornare indietro.',b=>{b.item(0,null,'cards',{cards:[{name:'Classe: Ladro',col:'#3d7a3f',slot:'Carta Classe',text:'+2 MOV. Puoi fuggire da ogni scontro e fuggendo non arretri.',w:300}],side:`<div class="lbl" style="text-align:left;color:#2a2118">La Carta Classe si infila nella scheda e vale per tutta la partita.</div>`})});
say('L','Poi la <b>specie</b>. Ognuna dà dei bonus da aggiungere subito alla scheda.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr"><table style="font-family:'Alegreya Sans';font-size:25px;border-collapse:collapse;width:640px">${[['Umano','+1 MOV e +1 a una statistica'],['Elfo','+2 a una statistica'],['Nano','+1 a due statistiche diverse'],['Orco','+2 ATT'],['Sanguar','+2 MOV']].map(r=>`<tr><td style="padding:7px 12px;border-bottom:2px solid #b9a582;font-weight:800">${r[0]}</td><td style="padding:7px 12px;border-bottom:2px solid #b9a582">${r[1]}</td></tr>`).join('')}</table></div>`})});
say('G','Umana, allora: +1 MOV e +1 all’AR.',b=>{set(b,0.6,'S',{mov:4,ar:2})});
say('L','Io gioco il Guerriero orco, Marco il Mago elfo. Ognuno prende la miniatura e il mazzetto del suo colore.',b=>{set(b,0.3,'L',{on:true,pv:7,pvm:7,att:3});set(b,1.3,'M',{on:true,att:3})});

// 5 SCHEDA
say('M','Questa è la tua <b>scheda</b>. Tutti partono da <b>5 PV</b>, e ATT, MOV e AR a 1. I cubetti mostrano sempre il valore finale.',b=>{les(b,5,'La scheda eroe');st(b,0,{title:'La scheda',sub:'tiene il conto al posto tuo'});b.item(0,null,'html',{h:SCHEDA()})});
say('M','La <b>Difesa</b> è 14 più l’AR, ed è già stampata sotto la casella. È il numero che i nemici devono raggiungere per colpirti.',b=>{b.item(0,null,'html',{h:SCHEDA()})});
say('L','I PV crescono solo salendo di livello. A destra ci sono gli Indizi, le Clessidre, l’Ispirazione e gli edifici già usati.',b=>{b.item(0,null,'html',{h:SCHEDA()});b.item(0,null,'hlhero',{})});

// 6 PARTENZA E MANO
say('M','Ognuno tira il D6 per la partenza. Se il posto è occupato o è accanto a un altro eroe, si ritira.',b=>{les(b,6,'Partenza e carte');st(b,0,{title:'Partenza e carte',sub:''});
  dice(b,0.3,[{t:'D6',v:1,l:'Lia → 1',sz:100},{t:'D6',v:4,l:'Marco → 4',sz:100,dt:0.6},{t:'D6',v:1,l:'Giulia → 1, occupata',sz:100,dt:1.6,dim:1},{t:'D6',v:6,l:'ritira → 6',sz:100,dt:3}],'','',null);
  place(b,1,'L',...SPAWN[0]);place(b,1.6,'M',...SPAWN[3]);b.item(2.5,1.2,'ring',{c:2,r:0,col:'#9c2f24'});place(b,3.8,'S',...SPAWN[5])});
say('L','Ora la mano: <b>5 carte della tua classe e 5 comuni</b>, pescate coperte. Per tutta la partita non se ne pescano altre.',b=>{
  const backs=(col,lab)=>`<div style="text-align:center"><div style="display:flex">${[0,1,2,3,4].map(i=>`<div class="back" style="background:${col};margin-left:${i?-62:0}px;transform:rotate(${(i-2)*6}deg) translateY(${Math.abs(i-2)*6}px)">?</div>`).join('')}</div><div class="lbl" style="margin-top:18px">${lab}</div></div>`;
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:70px">${backs('#3d7a3f','5 dal mazzetto del Ladro')}${backs('#4a3a2a','5 dal mazzo comune')}</div>`});
  ['L','M','S'].forEach((k,i)=>set(b,1+i*0.3,k,{hand:10}))});
say('M','Se volete potete fare anche il <b>draft</b>: scegli 3 carte della tua classe, poi peschi 7 comuni, ne tieni una e passi le altre a sinistra.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:26px"><span class="chip">${IC('stella',30)} 3 di classe, a scelta</span><span style="font-size:40px;color:#b8862b">+</span><span class="chip">${IC('pergamena',30)} 7 comuni, tienine 1 e passa</span></div>`})});
say('G','Solo dieci carte? Allora devo usarle bene.',b=>{});
say('L','Prima di cominciare indossiamo tutti subito <b>un oggetto</b>. Io la Spada del Custode, Marco il Bastone del Corvo.',b=>{
  b.item(0,null,'cards',{cards:[{name:'Spada del Custode',slot:'Arma DX / Scudo',text:'+1 ATT',who:'Lia',w:240},{name:'Bastone del Corvo',slot:'Arma DX / Scudo',text:'+1 ATT. Una volta per turno ritiri un D6.',who:'Marco',deck:'Mago',w:240,col:'#2f5d9c'},{name:'Pugnale Sottile',slot:'Arma SX',text:'Se attacchi per primo: +1 ATT.',who:'Giulia',deck:'Ladro',w:240,col:'#3d7a3f'}]});
  set(b,1,'L',{arma:'Spada del Custode',hand:9,att:4});set(b,1.4,'M',{arma:'Bastone del Corvo',hand:9,att:4});set(b,1.8,'S',{arma:'Pugnale Sottile',hand:9})});
say('M','La carta si infila sotto il bordo della scheda, nel suo slot: <b>Elmo, Arma destra o Scudo, Arma sinistra, Armatura</b>.',b=>{b.item(0,null,'html',{h:`<div class="ctr" style="padding:6px">${ART.anatomy.replace('<svg ','<svg style="height:370px;width:auto" ')}</div>`})});
say('M','Chi ha visto per ultimo un goblin prende <b>Geronimo</b> e comincia. Lia?',b=>{});
say('L','Io! Stamattina, nello specchio.',b=>{set(b,0.4,'L',{ger:true})});

// 7 TURNO
say('M','Il turno ha sempre <b>5 passi</b>. Li trovi sulla plancia e sulla Carta Aiuto.',b=>{les(b,7,'Il turno in 5 passi');st(b,0,{title:'Il turno',sub:'sempre gli stessi 5 passi'});b.item(0,9999,'strip',{})});
say('L','Uno: se hai una <b>Clessidra</b>, la togli e salti il turno. Te la danno alcuni nemici, per esempio lo Gnomo schiavista.',b=>{b.at(0.3,s=>s.phase=0)});
say('L','Due: le <b>carte</b>. Puoi giocarne fino a 2 nel turno: adesso, durante uno scontro o alla fine. Gli <b>equipaggiamenti</b> solo adesso, uno al massimo.',b=>{b.at(0.2,s=>s.phase=1)});
say('L','Tre: ti <b>muovi</b>. Quattro: <b>esplori</b> dove ti sei fermata. Cinque: <b>fine</b>, passi i dadi a sinistra.',b=>{b.at(0.2,s=>s.phase=2);b.at(1.6,s=>s.phase=3);b.at(3.2,s=>s.phase=4);b.at(beatEnd(b),s=>s.phase=-1)});
ITEMS.forEach(i=>{if(i.kind==='strip'&&i.t1>T)i.t1=T});

// 8 MUOVERSI
say('L','Comincio io. Tiro il D6: 3, più il mio MOV 1. Posso fare fino a 4 esagoni.',b=>{les(b,8,'Muoversi ed esplorare');banner(b,'Giro 1');st(b,0,{title:'Giro 1 · Lia',sub:'muoversi'});b.at(0,s=>{s.playing=true;s.giro=1});act(b,'L',2);
  dice(b,0.4,[{t:'D6',v:3,l:'3 + MOV 1 = 4'}],'','fino a 4 esagoni, almeno 1')});
say('G','Puoi passare sopra le caselle col punto di domanda?',b=>{b.item(0,null,'html',{h:`<div class="ctr">${ART.move.replace('<svg ','<svg style="width:900px;height:auto" ')}</div>`})});
say('L','Sì, puoi passare sopra a tutto. Conta solo l’esagono dove <b>ti fermi</b>. Mi fermo qui, dopo 2.',b=>{b.item(0,null,'html',{h:`<div class="ctr">${ART.move.replace('<svg ','<svg style="width:900px;height:auto" ')}</div>`});move(b,1.6,'L',[2,2])});
say('L','Casella «?»: pesco un segnalino dal sacchetto… <b>Nemico I</b>. Giro la prima carta del mazzetto I: un <b>Lupo grigio</b>!',b=>{phase(b,0,3);draw(b,0.4,{name:'Nemico I',icon:'spade',kind:'Segnalino',title:'Nemico I',desc:'Gira la prima carta del mazzetto I'},2.6);
  b.item(3,null,'ncard',{c:NC({name:'Lupo grigio',letter:'L',pv:3,att:3,ar:0,dmg:'D6 − 1',ab:'Inseguitore: se fuggi, ti attacca un’ultima volta prima che tu arretri.'})})});
say('M','La carta dice tutto: <b>3 PV, ATT 3, AR 0</b>, quindi Difesa 14. È di livello 1, e il livello dice quanto fa male: D6 meno 1.',b=>{});

// 9 SCONTRO
{const lines=[];
 say('M','Lo scontro sono <b>due tiri</b>. Per colpire tiri il <b>D20 e aggiungi l’ATT</b>: se arrivi alla Difesa, colpisci. Poi tiri il <b>danno</b>, col D6.',b=>{les(b,9,'Lo scontro');st(b,0,{title:'Giro 1 · Lia',sub:'lo scontro'});combat(b,0,'L',LUPO,lines,40)});
 say('L','12 più 4 fa 16: almeno 14, colpito! Danno: D6, esce 2.',b=>{atk(lines,b,0.2,{who:'Lia',col:'#a8352a',d20:12,mod:4,vs:14,hit:true,dmg:{die:'D6',v:2,total:2},target:'foe'})});
 say('M','Il <b>dado rosso</b> tiene il conto dei PV del lupo: da 3 scende a 1.',b=>{});
 say('G','E per il lupo chi tira?',b=>{});
 say('M','Il giocatore alla destra di chi combatte. Tocca a te, Giulia: D20 più l’ATT del lupo, contro la Difesa di Lia, 15.',b=>{});
 say('G','13 più 3, 16… l’ho presa! Danno: 4 meno 1, 3. Scusa, Lia!',b=>{atk(lines,b,0.1,{who:'Lupo',roller:'Giulia',d20:13,mod:3,vs:15,hit:true,dmg:{die:'D6 − 1',v:4,expr:'4 − 1 ',total:3},target:'L'})});
 say('L','Tranquilla! Secondo round: 15 più 4, colpito. Danno 5: il lupo è finito.',b=>{atk(lines,b,0.1,{who:'Lia',col:'#a8352a',d20:15,mod:4,vs:14,hit:true,dmg:{die:'D6',v:5,total:5},target:'foe'})});
 say('M','Ricorda: con <b>20 sul dado</b> colpisci sempre e il danno raddoppia, con <b>1</b> manchi sempre.',b=>{});
}
say('L','Vinto! Prendo <b>1 Indizio e 1 PE</b>. Da Guerriero guadagno anche l’<b>Ispirazione</b>. Un solo scontro per turno: ho finito.',b=>{phase(b,0,4);clue(b,0.6,'L');add(b,1.2,'L',{pe:1});set(b,1.8,'L',{insp:true});
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:30px"><span class="chip">${IC('pergamena',34)} +1 Indizio</span><span class="chip">${IC('stella',34)} +1 PE</span><span class="chip">${IC('stella',34)} Ispirazione</span></div>`})});

// 10 TRAPPOLE
say('M','Tocca a me. 2 più 1: mi fermo su un «?»… <b>Trappola</b>.',b=>{les(b,10,'Trappole');st(b,0,{title:'Giro 1 · Marco',sub:'trappole'});act(b,'M',2);
  dice(b,0,[{t:'D6',v:2,l:'2 + 1 = 3',sz:90}],'','',1.6);move(b,0.5,'M',[7,7],1);b.at(1.6,s=>s.phase=3);draw(b,1.6,{name:'Trappola',icon:'trappola',kind:'Segnalino',title:'Trappola',desc:'Perdi D6 − 1 PV e tira la perdita.'})});
say('M','Perdo D6 meno 1 PV, poi tiro la <b>perdita</b>: 1 tutto, 2 l’elmo, 3 l’arma destra, 4 la sinistra, 5 l’armatura, 6 niente.',b=>{hlr(b,0.3,PROM,null);
  dice(b,0.3,[{t:'D6',v:3,l:'danno: 3 − 1 = 2',sz:96},{t:'D6',v:6,l:'perdita: 6 = niente',sz:96,dt:2.6}],'Trappola','',null);add(b,1.2,'M',{pv:-2})});

// 11 QUANDO GIOCARE LE CARTE
say('M','Sono a 3 PV. <b>A fine turno</b> gioco una carta: <b>Scudo di Cenere</b>, +2 AR fino alla fine del mio prossimo scontro.',b=>{les(b,11,'Quando giocare le carte');st(b,0,{title:'Giro 1 · Marco',sub:'una carta a fine turno'});phase(b,0,4);
  b.item(0,null,'cards',{cards:[{name:'Scudo di Cenere',slot:'Incantesimo',text:'Fino alla fine del tuo prossimo scontro ottieni +2 AR.',who:'Marco',w:280}],side:`<div class="lbl" style="text-align:left;color:#2a2118">Le carte giocate vanno negli scarti, a faccia in su.</div>`});add(b,1.4,'M',{hand:-1,arTmp:2})});
say('G','Il mio turno! 4 più MOV 4… posso fare 8 esagoni?',b=>{st(b,0,{title:'Giro 1 · Giulia',sub:'una carta in scontro'});act(b,'S',2);dice(b,0,[{t:'D6',v:4,l:'4 + MOV 4 = 8'}],'','fino a 8 esagoni')});
say('L','Sì, il Ladro corre! Prova quel «?» al centro.',b=>{move(b,0.3,'S',[4,5],1.2)});
say('G','Nemico I… un <b>Coboldo</b>: 2 PV, Difesa 14.',b=>{phase(b,0,3);b.item(0,null,'ncard',{c:NC({name:'Coboldo',letter:'C',pv:2,att:1,ar:0,dmg:'D6 − 1',ab:'Codardo: con metà PV o meno ha −2 ATT.'})})});
{const lines=[];
 say('M','Hai una carta da giocare <b>nello scontro</b>? Prima di tirare, per esempio.',b=>{combat(b,0,'S',COB,lines,16)});
 say('G','<b>Colpo alle Spalle</b>: se attacco per primo faccio 2 danni in più. E il Pugnale mi dà +1 ATT.',b=>{
  lines.push({dt:b.t0+0.4,who:'Giulia',col:'#3d7a3f',text:'<span class="note">gioca Colpo alle Spalle: +2 danni</span>'});add(b,0.4,'S',{hand:-1})});
 say('G','14 più 2, 16: colpito! Danno 1 più 2, 3. Il Coboldo è battuto!',b=>{atk(lines,b,0.2,{who:'Giulia',col:'#3d7a3f',d20:14,mod:2,vs:14,hit:true,dmg:{die:'D6',v:1,expr:'1 + 2 ',total:3},target:'foe'});clue(b,2.4,'S');add(b,2.6,'S',{pe:1})});
}

// 12 NEMICO II E SCONFITTA
{const lines=[];
 say('L','<b>Giro 2.</b> Mi fermo su un altro «?»: <b>Nemico II</b>. Dal mazzetto II esce un <b>Orso delle caverne</b>.',b=>{les(b,12,'Nemico II e sconfitta');banner(b,'Giro 2');st(b,0,{title:'Giro 2 · Lia',sub:'Nemico II'});b.at(0,s=>s.giro=2);act(b,'L',2);move(b,0.2,'L',[2,4],0.8);
  b.at(1,s=>s.phase=3);b.item(1,null,'ncard',{c:NC({name:'Orso delle caverne',letter:'O',lv:3,pv:7,att:3,ar:0,dmg:'D6 + 1',ab:'Furia: con metà PV o meno ha +2 ATT.',rew:['1 Indizio','1 PE','Ispirazione'],tipo:'Nemico II'})})});
 say('M','Livello 3: il suo danno è <b>D6 più 1</b>. Lia ha 4 PV… Prima di ogni tuo attacco puoi sempre <b>fuggire</b>, senza ricompensa.',b=>{});
 say('L','Ci provo! 10 più 4, 14: colpito. Danno 5, l’Orso scende a 2.',b=>{combat(b,0,'L',ORSO,lines,30);atk(lines,b,0.6,{who:'Lia',col:'#a8352a',d20:10,mod:4,vs:14,hit:true,dmg:{die:'D6',v:5,total:5},target:'foe'})},0,0.6);
 say('G','Tiro io per l’Orso. Con metà PV va in <b>furia</b>: +2 ATT. 12 più 5, 17… colpita. 3 più 1: 4 danni.',b=>{atk(lines,b,0.2,{who:'Orso',roller:'Giulia',d20:12,mod:5,vs:15,hit:true,dmg:{die:'D6 + 1',v:3,expr:'3 + 1 ',total:4},target:'L'})});
}
say('L','Zero PV: <b>sconfitta</b>. Non sei eliminata: tiri il D6 per ripartire e torni ai PV massimi. Gli Indizi restano tuoi.',b=>{b.at(0,s=>{s.H.L.down=true});
  dice(b,0.3,[{t:'D6',v:2,l:'ripartenza → 2 (H1)',sz:100}],'Sconfitta','',null);
  b.at(1.3,s=>{const h=s.H.L;h.down=false;s.anim.L={p:[[7,0]],t0:b.t0+1.3,dur:.01,drop:true};h.c=7;h.r=0;h.pv=h.pvm;s.tok.push({id:'orso',c:2,r:4,kind:'crea',label:'Orso'})});b.item(1.3,2,'ring',{c:7,r:0,col:'#a8352a'})});
say('M','Poi la perdita: 3, la Spada va negli scarti. E l’Orso resta lì, scoperto e con tutti i PV, per il prossimo che passa.',b=>{
  dice(b,0.2,[{t:'D6',v:3,l:'perdita: 3 = Arma DX',sz:100}],'','',null);set(b,1,'L',{arma:'—',att:3})});

// 13 DUELLO
{const lines=[];
 say('M','Io vado su un «?»: uno <b>Scheletro</b>. Con lo Scudo di Cenere la mia Difesa è 17.',b=>{les(b,13,'Il Mago e il Duello');st(b,0,{title:'Giro 2 · Marco',sub:'ritirare i dadi'});act(b,'M',2);move(b,0,'M',[5,6],1);b.at(1.1,s=>s.phase=3);
  b.item(1.1,null,'ncard',{c:NC({name:'Scheletro',letter:'S',pv:2,att:2,ar:1,dmg:'D6 − 1',ab:'Non morto. Si ricompone: la prima volta che va a 0 PV torna a 2 PV.'})})});
 say('M','Tiro: 6, mancato. Ma il <b>Mago ritira</b> i suoi dadi fino a 2 volte per turno… 13 più 4, 17! Danno 4.',b=>{combat(b,0,'M',SCH,lines,22);
  atk(lines,b,0.4,{who:'Marco',col:'#2f5d9c',d20:6,reroll:13,mod:4,vs:15,hit:true,dmg:{die:'D6',v:4,total:4},target:'foe'})},0,0.6);
 say('L','Lo Scheletro però <b>si ricompone</b>: torna a 2 PV. Per lui tiro 12 più 2, 14: contro 17 non basta.',b=>{b.at(0.2,s=>{s.foe.pv=2});atk(lines,b,1.6,{who:'Scheletro',roller:'Lia',d20:12,mod:2,vs:17,hit:false})});
 say('M','11 più 4, 15: colpito. Questa volta resta giù. <b>1 Indizio e 1 PE</b>, e lo Scudo di Cenere finisce.',b=>{atk(lines,b,0.2,{who:'Marco',col:'#2f5d9c',d20:11,mod:4,vs:15,hit:true,dmg:{die:'D6',v:2,total:2},target:'foe'});clue(b,2.4,'M');add(b,2.6,'M',{pe:1,arTmp:-2})});
}
say('G','Io sono già accanto a Marco. Mi sposto di uno e resto vicina a lui.',b=>{st(b,0,{title:'Giro 2 · Giulia',sub:'il Duello'});act(b,'S',2);move(b,0.2,'S',[4,6],0.6);b.at(1,s=>s.phase=3);b.item(1,3,'ring',{c:5,r:6,col:'#2f5d9c'})});
say('L','Allora c’è il <b>Duello</b>! Se finisci accanto a un eroe e non hai avuto altri scontri, lo sfidi.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:50px"><div class="big" style="width:280px">Duello!</div><div class="lbl" style="width:520px;text-align:left;color:#2a2118;font-size:24px">Chi vince prende <b>1 Indizio</b> allo sconfitto, <b>1 carta</b> dai suoi scarti, <b>1 PE</b> e l’<b>Ispirazione</b>. Chi perde subisce una sconfitta normale.</div></div>`})});
say('M','Con 3 PV rifiuto: in cambio peschi <b>1 carta a caso</b> dalla mia mano. Ecco, tienila.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:50px"><div style="text-align:center"><div class="back" style="background:#2f5d9c;margin:auto">?</div><div class="lbl" style="margin-top:12px">1 carta a caso<br>da Marco a Giulia</div></div></div>`});add(b,1.6,'M',{hand:-1});add(b,1.9,'S',{hand:1})});

// 14 EDIFICI E LIVELLI
say('L','<b>Giro 3.</b> Io passo dal <b>Fabbro</b>: mi riprendo in mano la Spada. La rimetto a inizio del prossimo turno.',b=>{les(b,14,'Edifici e livelli');banner(b,'Giro 3');st(b,0,{title:'Giro 3 · Lia',sub:'il Fabbro'});b.at(0,s=>s.giro=3);act(b,'L',2);
  move(b,0.2,'L',[8,1],0.8);b.at(1.1,s=>s.phase=3);b.at(1.6,s=>s.H.L.used.push('martello'));add(b,1.6,'L',{hand:1})});
say('M','Io vado alla <b>Locanda</b>: +1 PE e 2 PV. Con 2 PE arrivo alla casella dorata e salgo al <b>livello 2</b>.',b=>{st(b,0,{title:'Giro 3 · Marco',sub:'salire di livello'});act(b,'M',2);
  dice(b,0,[{t:'D6',v:3,l:'3 + 1 = 4',sz:90}],'','',1.4);move(b,0.4,'M',[8,5],1.2);b.at(1.6,s=>s.phase=3);add(b,2,'M',{pe:1,pv:2});b.at(2,s=>s.H.M.used.push('casa'))});
say('L','A ogni livello scegli: <b>+1 a ATT, MOV o AR</b>, oppure <b>+2 PV</b>. È l’unico modo di avere più PV.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:28px"><span class="chip">${IC('stella',34)} PE 2 · 4 · 6 · 8 = livello</span><span class="chip">${IC('spade',34)} +1 ATT, MOV o AR</span><span class="chip">${IC('cuore',34)} oppure +2 PV</span></div>`})});
say('M','Prendo i 2 PV: sono a <b>7 su 7</b>.',b=>{set(b,0.3,'M',{lv:2,pe:0});add(b,0.3,'M',{pv:2,pvm:2})});

// 15 IL TESORO
{const lines=[];
 say('G','Io esploro il «?» qui accanto: un <b>Goblin predone</b>. 15 più 2, colpito, 3 danni: battuto!',b=>{les(b,15,'Il tesoro');st(b,0,{title:'Giro 3 · Giulia',sub:'il secondo Indizio'});act(b,'S',2);move(b,0.2,'S',[4,7],0.5);b.at(0.8,s=>s.phase=3);
  combat(b,0.8,'S',GOB,lines,null);atk(lines,b,1.4,{who:'Giulia',col:'#3d7a3f',d20:15,mod:2,vs:15,hit:true,dmg:{die:'D6',v:3,total:3},target:'foe'});clue(b,4.6,'S');add(b,4.8,'S',{pe:1})},0,1);
}
say('M','È il tuo <b>secondo Indizio</b>: hai individuato il tesoro! E allora <b>la voce si sparge</b>: io e Lia prendiamo subito 1 Indizio a testa.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:22px"><div class="big">La voce si sparge</div><div style="display:flex;gap:40px"><span class="chip" style="border-color:#a8352a">${IC('pergamena',34)} Lia +1</span><span class="chip" style="border-color:#2f5d9c">${IC('pergamena',34)} Marco +1</span></div></div>`});
  clue(b,2.4,'L');clue(b,2.8,'M')});
say('L','Ora il D6 dice dov’è MIMI. Con 5 o 6 si ritira… 6, ritiro. <b>2!</b> MIMI e il Guardiano vanno sulla Cripta 2.',b=>{
  dice(b,0,[{t:'D6',v:6,l:'6 → si ritira',sz:100,dim:1},{t:'D6',v:2,l:'Cripta 2',sz:100,dt:2.2}],'Dov’è MIMI?','',null);
  b.at(3.6,s=>{s.sala.Boss=false;s.sala.MIMI=false;s.tok.push({id:'guard',c:6,r:3,kind:'guard',from:salaPos(0),t0:b.t0+3.6,dur:1.3});s.tok.push({id:'mimi',c:6,r:3,kind:'mimi',from:salaPos(1),t0:b.t0+3.8,dur:1.3})});
  b.item(3.6,4,'ring',{c:6,r:3,col:'#b8862b',delay:1.3})});
say('G','Quindi adesso abbiamo tutti 2 Indizi e sappiamo dov’è il tesoro?',b=>{});
say('M','Sì: vince chi arriva per primo alla Cripta e batte il boss. Attenta solo alle <b>Mappe</b>: chi ne gioca una fa cambiare Cripta al tesoro.',b=>{
  b.item(0,null,'cards',{cards:[{name:'Miraggio del Tesoro',slot:'Mappa · carta comune',text:'Il tesoro cambia Cripta. Gli Indizi restano a tutti.',w:280}],side:`<div class="lbl" style="text-align:left;color:#2a2118">Il tesoro si sposta al massimo 2 volte per partita.</div>`})});

// 16 BOSS E VITTORIA
say('L','<b>Giro 4.</b> A inizio turno rimetto la Spada. Poi 2 più 1: arrivo giusta alla Cripta 2.',b=>{les(b,16,'Il boss e la vittoria');banner(b,'Giro 4');st(b,0,{title:'Giro 4 · Lia',sub:'il Guardiano di MIMI'});b.at(0,s=>{s.giro=4});act(b,'L',1);
  set(b,0.6,'L',{arma:'Spada del Custode',att:4});add(b,0.6,'L',{hand:-1});b.at(1.4,s=>s.phase=2);dice(b,1.4,[{t:'D6',v:2,l:'2 + 1 = 3',sz:90}],'','',1.6);move(b,2,'L',[6,3],1)});
{const lines=[];
 say('M','Il Guardiano: <b>9 PV, ATT 4, Difesa 17</b>, danno D6 più 1.',b=>{phase(b,0,3);combat(b,0,'L',GU,lines,null)});
 say('L','Spendo l’<b>Ispirazione</b> del Guerriero: −2 AR, la sua Difesa scende a 15. 14 più 4, colpito! Danno 4.',b=>{b.at(0.4,s=>{s.foe.dif0=17;s.foe.dif=15;s.H.L.insp=false});lines.push({dt:b.t0+0.4,who:'Lia',col:'#a8352a',text:'<span class="note">Ispirazione: Difesa del Guardiano −2</span>'});
  atk(lines,b,1.4,{who:'Lia',col:'#a8352a',d20:14,mod:4,vs:15,hit:true,dmg:{die:'D6',v:4,total:4},target:'foe'})},0,0.6);
 say('M','Tiro io per il Guardiano: 15 più 4, colpita. 4 più 1, 5 danni. Sei a 2 PV.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Marco',d20:15,mod:4,vs:15,hit:true,dmg:{die:'D6 + 1',v:4,expr:'4 + 1 ',total:5},target:'L'})});
 say('G','E adesso scappi?',b=>{});
 say('L','Dal boss può fuggire <b>solo il Ladro</b>. Io devo continuare… 8 più 4, mancato.',b=>{atk(lines,b,1.6,{who:'Lia',col:'#a8352a',d20:8,mod:4,vs:15,hit:false})});
 say('M','E il Guardiano fa 11 più 4, 15: colpita. Lia, sei a terra.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Marco',d20:11,mod:4,vs:15,hit:true,dmg:{die:'D6 + 1',v:2,expr:'2 + 1 ',total:3},target:'L'})});
}
say('L','Però le <b>ferite del boss restano</b>: il cubetto giallo scende a 5. Io riparto da C1 con i PV pieni e tengo i miei Indizi.',b=>{
  b.at(0.3,s=>{s.gpvAnim={from:9,to:5,t0:b.t0+0.3,dur:1.6};s.gpv=5});hlr(b,0.2,PVT,3);
  dice(b,2,[{t:'D6',v:1,l:'ripartenza → 1 (C1)',sz:96},{t:'D6',v:6,l:'perdita: 6 = niente',sz:96,dt:0.8}],'','',null);
  b.at(2.8,s=>{const h=s.H.L;s.anim.L={p:[[2,0]],t0:b.t0+2.8,dur:.01,drop:true};h.c=2;h.r=0;h.pv=h.pvm});b.item(2.8,2,'ring',{c:2,r:0,col:'#a8352a'})});
say('M','Io tiro 1 più 1: la Cripta è a 3 esagoni, non ci arrivo. Mi sposto e aspetto.',b=>{act(b,'M',2);dice(b,0,[{t:'D6',v:1,l:'1 + 1 = 2'}],'','',null);move(b,1,'M',[8,4],0.6)});
say('G','Tocca a me. 3 più 4, 7: arrivo alla Cripta. Il Guardiano ha ancora le ferite di Lia: <b>5 PV</b>.',b=>{act(b,'S',2);dice(b,0,[{t:'D6',v:3,l:'3 + MOV 4 = 7'}],'','',null);move(b,1,'S',[6,3],1.2)});
{const lines=[];
 say('G','Attacco per prima, col Pugnale: 9 più 2, 11. Mancato…',b=>{phase(b,0,3);combat(b,0,'S',{...GU,pv0:5},lines,40);atk(lines,b,1,{who:'Giulia',col:'#3d7a3f',d20:9,mod:2,vs:17,hit:false})});
 say('L','Tiro io per il Guardiano: 13 più 4, 17 contro la tua Difesa 16. Colpita: 3 danni, sei a 2 PV.',b=>{atk(lines,b,0.2,{who:'Guardiano',roller:'Lia',d20:13,mod:4,vs:16,hit:true,dmg:{die:'D6 + 1',v:2,expr:'2 + 1 ',total:3},target:'S'})});
 say('M','Tu sei il Ladro: potresti fuggire anche adesso. Ma il boss ha solo 5 PV…',b=>{});
 say('G','Resto! Tiro… <b>20!</b> Colpo sicuro e danno doppio: 3 per 2, 6. Il Guardiano è a zero!',b=>{atk(lines,b,0.6,{who:'Giulia',col:'#3d7a3f',d20:20,mod:1,vs:17,hit:true,dmg:{die:'D6',v:3,expr:'3 × 2 ',total:6},target:'foe'})},0,0.6);
}
say('L','Giulia riporta MIMI a Geronimo e <b>vince</b>. Alla prima partita!',b=>{st(b,0,{title:'Vittoria!',sub:'Giulia · Ladro umana'});b.at(0,s=>{s.phase=-1;s.gpv=0;s.gpvAnim=null;s.tok=s.tok.filter(k=>k.kind!=='guard')});
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:10px"><svg viewBox="0 0 24 24" width="150" height="150">${ICONS.forziere}</svg><div class="big" style="font-size:52px">Giulia vince!</div></div>`})});
say('M','Fortuna del principiante. Rivincita?',b=>{});
beat(10,'',b=>{b.item(0,10,'recap',{})});
