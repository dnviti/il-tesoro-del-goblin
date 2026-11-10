// ---------------- the game ----------------
// Partita al tavolo con le regole della scatola base v5 (Carte Trama v2, 27/10/2026)
const LUPO={name:'Lupo grigio',short:'Lupo',pv:3,att:3,dif:14,dmg:'D6 − 1',kind:'Nemico I'};
const COB={name:'Coboldo',short:'Coboldo',pv:2,att:1,dif:14,dmg:'D6 − 1'};
const SCH={name:'Scheletro',short:'Scheletro',pv:2,att:2,dif:15,dmg:'D6 − 1'};
const ORSO={name:'Orso delle caverne',short:'Orso',pv:7,att:3,dif:14,dmg:'D6 + 1'};
const RE={name:'Re Goblin Grugno',short:'Re Goblin',pv:9,att:4,dif:16,dmg:'D6 + 1',icon:'forziere'};
const NOP=()=>{};
const NC=(o)=>({lv:1,ab:'',rew:['1 Indizio','1 PE'],...o});
// INTRO
beat(6,'',b=>{b.item(0,6,'cover',{a:'IL TESORO DEL GOBLIN',b:'Una partita<br>al tavolo',c:'Dalla scatola aperta alla vittoria',d:'Un gioco di Alessandro De Simone · scatola base · 3 giocatori · regolamento v5'})});
// SETUP
beat(4.5,'Si apre la <b>plancia</b> al centro del tavolo: 10 × 10 esagoni, identica se la giri di 180°.',b=>{st(b,0,{title:'Preparazione',sub:'circa 5 minuti, una volta sola'});b.at(0,s=>s.boardOn=b.t0)},30);
beat(5.5,'I <b>30 segnalini Esplorazione</b> vanno tutti nel <b>sacchetto</b>, mescolati. Accanto, coperti, i due mazzetti dei <b>Nemici</b>.',b=>{
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:40px">${bagSVG()}<div style="display:flex;flex-direction:column;gap:12px;align-items:flex-start"><span class="chip">${IC('spade',28)} 19 Nemico I</span><span class="chip">${IC('teschio',28)} 6 Nemico II</span><span class="chip">${IC('trappola',28)} 5 Trappole</span><span class="lbl" style="text-align:left;margin-top:6px">Mazzetto I: nemici di LV 1-2<br>Mazzetto II: nemici di LV 3-4</span></div></div>`})},35);
beat(6,'Si pesca uno dei <b>3 Boss</b>: esce il <b>Re Goblin Grugno</b>. Va nella Sala del Tesoro con MIMI, e il cubetto giallo sui suoi <b>9 PV</b>.',b=>{
  b.item(0,null,'ncard',{c:NC({name:'Re Goblin Grugno',letter:'R',lv:5,pv:9,att:4,ar:2,dmg:'D6 + 1',ab:'Furia: con metà PV o meno ha +2 ATT.',rew:['La partita!'],tipo:'Boss'})});
  b.at(1.2,s=>{s.salaOn=b.t0+1.2});b.at(2.6,s=>{s.cubesOn=true;s.gpv=9})},25);
beat(6.5,'Ognuno sceglie <b>classe</b> e <b>specie</b>: Lia gioca il Guerriero (Orco), Marco il Mago (Elfo), Sara il Ladro (Umana).',b=>{
  set(b,0.2,'L',{on:true,pv:7,pvm:7,att:3});set(b,1.6,'M',{on:true,att:3});set(b,3,'S',{on:true,mov:4,ar:2});
  b.item(0,null,'cards',{stag:1.4,cards:[{name:'Lia',col:'#a8352a',slot:'Guerriero · Orco',text:'Si parte da 5 PV<br>Orco: +2 ATT<br>Guerriero: +2 PV',w:270},{name:'Marco',col:'#2f5d9c',slot:'Mago · Elfo',text:'Si parte da 5 PV<br>Elfo: +2 a una statistica (sceglie ATT)',w:270},{name:'Sara',col:'#3d7a3f',slot:'Ladro · Umana',text:'Si parte da 5 PV<br>Umana: +1 MOV e +1 AR<br>Ladro: +2 MOV',w:270}]})},50);
beat(6.5,'La <b>Carta Classe</b> si infila nella scheda e vale per tutta la partita. I PV crescono solo salendo di livello.',b=>{
  b.item(0,null,'cards',{cards:[{name:'Classe: Guerriero',col:'#a8352a',slot:'Carta Classe',text:'+2 PV. Ogni scontro vinto ti dà l’Ispirazione: spendila per dare −2 AR al nemico.',w:290},{name:'Classe: Mago',col:'#2f5d9c',slot:'Carta Classe',text:'Puoi ritirare i tuoi dadi fino a 2 volte per turno.',w:290},{name:'Classe: Ladro',col:'#3d7a3f',slot:'Carta Classe',text:'+2 MOV. Puoi fuggire da ogni scontro e fuggendo non arretri.',w:290}]})},25);
beat(6.5,'Ognuno tira il <b>D6</b> per la partenza. Sara fa 1, già presa da Lia: <b>ritira</b> e fa 3.',b=>{
  dice(b,0,[{t:'D6',v:1,l:'Lia → 1',sz:100},{t:'D6',v:4,l:'Marco → 4',sz:100,dt:0.5},{t:'D6',v:1,l:'Sara → 1 occupata',sz:100,dt:1.6,dim:1},{t:'D6',v:3,l:'Sara ritira → 3',sz:100,dt:3.2}],'Partenze: D6, si ritira se occupata o accanto a un eroe','',null);
  place(b,0.8,'L',...SPAWN[0]);place(b,1.3,'M',...SPAWN[3]);place(b,4,'S',...SPAWN[2]);
  b.item(2.4,1.2,'ring',{c:2,r:0,col:'#9c2f24'})},35);
beat(6.5,'Mano coperta: <b>5 carte della propria classe e 5 comuni</b>. Oppure il <b>draft</b>: 3 carte di classe scelte e 7 comuni passate a sinistra.',b=>{
  const backs=(col,lab)=>`<div style="text-align:center"><div style="display:flex;gap:0">${[0,1,2,3,4].map(i=>`<div class="back" style="background:${col};margin-left:${i?-62:0}px;transform:rotate(${(i-2)*6}deg) translateY(${Math.abs(i-2)*6}px)">?</div>`).join('')}</div><div class="lbl" style="margin-top:18px">${lab}</div></div>`;
  b.item(0,null,'html',{h:`<div class="ctr" style="gap:70px">${backs('#7a3a2e','5 dal mazzetto di classe')}${backs('#4a3a2a','5 dal mazzo comune')}</div>`});
  ['L','M','S'].forEach((k,i)=>set(b,1+i*0.3,k,{hand:10}))},45);
beat(6.5,'Tutti insieme indossano subito <b>un oggetto</b>: Lia la Spada del Custode, Marco il Bastone del Corvo, Sara il Pugnale Sottile.',b=>{
  b.item(0,null,'cards',{cards:[{name:'Spada del Custode',slot:'Arma DX / Scudo',text:'+1 ATT',who:'Lia',w:250},{name:'Bastone del Corvo',slot:'Arma DX / Scudo',text:'+1 ATT. Una volta per turno ritiri un D6.',who:'Marco',deck:'Mago',w:250,col:'#2f5d9c'},{name:'Pugnale Sottile',slot:'Arma SX',text:'Se attacchi per primo: +1 ATT.',who:'Sara',deck:'Ladro',w:250,col:'#3d7a3f'}]});
  set(b,0.4,'L',{arma:'Spada del Custode',hand:9,att:4});set(b,0.75,'M',{arma:'Bastone del Corvo',hand:9,att:4});set(b,1.1,'S',{arma:'Pugnale Sottile',hand:9})},35);
beat(4.5,'Chi ha visto per ultimo un goblin prende <b>Geronimo</b> e comincia: tocca a Lia. Poi si va in senso orario.',b=>{set(b,0.3,'L',{ger:true});
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column"><div class="big">Pronti in circa 5 minuti</div><div class="lbl">Ordine di turno: Lia → Marco → Sara</div></div>`})},25);
// TURN
beat(6.5,'Ogni turno ha <b>5 passi</b>. Fino a <b>2 carte</b>: a inizio turno, durante uno scontro o a fine turno. Gli equipaggiamenti solo a inizio turno.',b=>{st(b,0,{title:'Il turno',sub:'stampato sulla plancia e sulla Carta Aiuto'});b.item(0,null,'strip',{})},0);
// GIRO 1 · LIA
beat(5,'Lia tira il D6: 3, più MOV 1. Può fare fino a 4 esagoni, ma le basta fermarsi dopo 2, su una casella <b>«?»</b>.',b=>{banner(b,'Giro 1');b.at(0,s=>{s.playing=true;s.giro=1});st(b,0,{title:'Giro 1 · Lia',sub:'Guerriero · parte da C1'});act(b,'L',2);
  dice(b,0.4,[{t:'D6',v:3,l:'3 + MOV 1 = 4'}],'Movimento','',null);move(b,2.2,'L',[2,2],1)},20);
beat(5.5,'Pesca dal sacchetto: <b>Nemico I</b>. Gira la prima carta del mazzetto I: un <b>Lupo grigio</b>, 3 PV, ATT +3, Difesa 14.',b=>{phase(b,0,3);draw(b,0,{name:'Nemico I',icon:'spade',kind:'Segnalino',title:'Nemico I',desc:'Gira la prima carta del mazzetto I'},2.4);
  b.item(2.4,null,'ncard',{c:NC({name:'Lupo grigio',letter:'L',pv:3,att:3,ar:0,dmg:'D6 − 1',ab:'Inseguitore: se fuggi, ti attacca un’ultima volta prima che tu arretri.'})})},15);
{const lines=[];beat(6,'Lo scontro: <b>D20 + ATT</b> contro la Difesa, cioè <b>14 + AR</b>. Lia attacca per prima; per il lupo tira Sara.',b=>{
  combat(b,0,'L',LUPO,lines,17.4);
  atk(lines,b,1.0,{who:'Lia',col:'#a8352a',d20:11,mod:4,vs:14,hit:true,dmg:{die:'D6',v:2,total:2},target:'foe'});
  atk(lines,b,3.4,{who:'Lupo',roller:'Sara',d20:13,mod:3,vs:15,hit:true,dmg:{die:'D6 − 1',v:4,expr:'4 − 1 ',total:3},target:'L'})},25);
 beat(5.5,'Il dado rosso tiene il conto dei PV del lupo. Secondo round: 15 + 4 = 19, danno 5. Lupo sconfitto!',b=>{
  atk(lines,b,0.4,{who:'Lia',col:'#a8352a',d20:15,mod:4,vs:14,hit:true,dmg:{die:'D6',v:5,total:5},target:'foe'})},45);}
beat(5,'Ricompensa: <b>1 Indizio e 1 PE</b>. Da Guerriero, Lia prende anche l’<b>Ispirazione</b>. Fine del turno.',b=>{phase(b,0,4);clue(b,0.3,'L');add(b,0.6,'L',{pe:1});set(b,0.9,'L',{insp:true})},10);
// GIRO 1 · MARCO
beat(5.5,'Marco tira 2 + 1 e si ferma su «?»: è una <b>Trappola</b>. Perde D6 − 1 = 2 PV, poi tira la perdita: 6, niente.',b=>{st(b,0,{title:'Giro 1 · Marco',sub:'Mago · parte da H10'});act(b,'M',2);move(b,0,'M',[7,7],0.9);b.at(1,s=>s.phase=3);
  draw(b,1,{name:'Trappola',icon:'trappola',kind:'Segnalino',title:'Trappola',desc:'D6 − 1 PV, poi tiro di perdita'},2.6);dice(b,3.6,[{t:'D6',v:3,l:'3 − 1 = 2 PV'},{t:'D6',v:6,l:'perdita: 6, niente',dt:0.5}],'','',null);add(b,4,'M',{pv:-2})},40);
beat(5.5,'<b>A fine turno</b> Marco gioca <b>Scudo di Cenere</b>: +2 AR fino alla fine del suo prossimo scontro.',b=>{phase(b,0,4);
  b.item(0,null,'cards',{cards:[{name:'Scudo di Cenere',slot:'Incantesimo',text:'Fino alla fine del tuo prossimo scontro ottieni +2 AR.',who:'Marco',w:280}],side:`<div class="lbl" style="text-align:left;color:#2a2118">Le carte si giocano a inizio turno, in scontro o a fine turno.</div>`});add(b,0.6,'M',{hand:-1,arTmp:2})},20);
// GIRO 1 · SARA
beat(5.5,'Sara ha <b>MOV 4</b>: tira 4 e può fare 8 esagoni. Si ferma su un «?»: Nemico I, un <b>Coboldo</b>.',b=>{st(b,0,{title:'Giro 1 · Sara',sub:'Ladro · parte da J5'});act(b,'S',2);dice(b,0,[{t:'D6',v:4,l:'4 + MOV 4 = 8'}],'Movimento','',null);move(b,1.6,'S',[5,4],1.4);
  b.at(3.1,s=>s.phase=3);b.item(3.1,null,'ncard',{c:NC({name:'Coboldo',letter:'C',pv:2,att:1,ar:0,dmg:'D6 − 1',ab:'Codardo: con metà PV o meno ha −2 ATT.'})})},20);
{const lines=[];beat(5.5,'Il <b>Pugnale Sottile</b> le dà +1 ATT quando attacca per prima: 16 + 2 = 18, danno 3. Coboldo battuto: 1 Indizio e 1 PE.',b=>{combat(b,0,'S',COB,lines,5.5);
  atk(lines,b,0.8,{who:'Sara',col:'#3d7a3f',d20:16,mod:2,vs:14,hit:true,dmg:{die:'D6',v:3,total:3},target:'foe'});clue(b,3.6,'S');add(b,3.9,'S',{pe:1})},40);}
// GIRO 2
beat(6,'<b>Giro 2.</b> Lia va alla <b>Locanda</b>: +1 PE e +2 PV. Con 2 PE sale al <b>livello 2</b> e sceglie <b>+2 PV</b> (oppure +1 ATT, MOV o AR).',b=>{banner(b,'Giro 2');st(b,0,{title:'Giro 2',sub:''});b.at(0,s=>{s.giro=2});act(b,'L',2);move(b,0.2,'L',[1,4],0.8);
  b.at(1.1,s=>s.phase=3);add(b,1.3,'L',{pe:1,pv:2});b.at(1.3,s=>s.H.L.used.push('casa'));set(b,2.6,'L',{lv:2,pe:0});add(b,2.6,'L',{pv:2,pvm:2});
  b.item(1.2,null,'html',{h:`<div class="ctr" style="gap:26px"><span class="chip">${IC('casa',30)} Locanda: +1 PE, +2 PV</span><span class="chip">${IC('stella',30)} Livello 2: +2 PV</span></div>`})},45);
{const lines=[];beat(5.5,'Marco va su un «?»: Nemico I, uno <b>Scheletro</b>. Con lo Scudo di Cenere la sua Difesa è 17.',b=>{act(b,'M',2);move(b,0,'M',[5,6],0.9);b.at(1,s=>s.phase=3);
  b.item(1,2.6,'ncard',{c:NC({name:'Scheletro',letter:'S',pv:2,att:2,ar:1,dmg:'D6 − 1',ab:'Non morto. Si ricompone: la prima volta che va a 0 PV torna a 2 PV.'})});combat(b,3.6,'M',SCH,lines,14.2)},10);
 beat(6,'Marco fa 6 e manca, ma il <b>Mago ritira</b>: 13 + 4 = 17, danno 4. Lo Scheletro va a 0… e <b>si ricompone</b> a 2 PV!',b=>{
  atk(lines,b,0.2,{who:'Marco',col:'#2f5d9c',d20:6,reroll:13,mod:4,vs:15,hit:true,dmg:{die:'D6',v:4,total:4},target:'foe'});
  b.at(4,s=>{s.foe.pv=2})},30);
 beat(5.5,'Lo Scheletro manca la Difesa 17. Secondo round: 11 + 4 = 15, colpito. Questa volta resta giù: 1 Indizio e 1 PE.',b=>{
  atk(lines,b,0.2,{who:'Scheletro',roller:'Lia',d20:12,mod:2,vs:17,hit:false});
  atk(lines,b,1.6,{who:'Marco',col:'#2f5d9c',d20:11,mod:4,vs:15,hit:true,dmg:{die:'D6',v:2,total:2},target:'foe'});clue(b,4.2,'M');add(b,4.4,'M',{pe:1,arTmp:-2})},45);}
beat(6,'Sara pesca un <b>Nemico II</b>: un’<b>Arpia</b> di LV 3, danno D6 + 1. Troppo forte: <b>fugge</b>, e da Ladro non arretra.',b=>{act(b,'S',2);move(b,0,'S',[4,3],0.6);b.at(0.7,s=>s.phase=3);
  b.item(0.7,null,'ncard',{c:NC({name:'Arpia',letter:'A',lv:3,pv:4,att:4,ar:1,dmg:'D6 + 1',ab:'Picchiata: il tuo primo tiro per colpire si fa con svantaggio.',rew:['1 Indizio','1 PE','Ispirazione'],tipo:'Nemico II'})})},30);
// GIRO 3
beat(5.5,'<b>Giro 3.</b> Lia esplora l’esagono accanto: Nemico II, un <b>Orso delle caverne</b>. 7 PV, Difesa 14, danno D6 + 1.',b=>{banner(b,'Giro 3');st(b,0,{title:'Giro 3',sub:''});b.at(0,s=>{s.giro=3});act(b,'L',2);move(b,0.2,'L',[2,4],0.6);
  b.at(0.9,s=>s.phase=3);b.item(0.9,null,'ncard',{c:NC({name:'Orso delle caverne',letter:'O',lv:3,pv:7,att:3,ar:0,dmg:'D6 + 1',ab:'Furia: con metà PV o meno ha +2 ATT.',rew:['1 Indizio','1 PE','Ispirazione'],tipo:'Nemico II'})})},15);
{const lines=[];beat(6.5,'<b>Nello scontro</b> Lia gioca <b>Colpo Poderoso</b>: +2 danni. 12 + 4 = 16, danno 4 + 2 = 6. L’Orso, ferito, va in <b>furia</b>: 19, 4 danni.',b=>{combat(b,0,'L',ORSO,lines,13.4);add(b,0.3,'L',{hand:-1});
  atk(lines,b,0.8,{who:'Lia',col:'#a8352a',d20:12,mod:4,vs:14,hit:true,dmg:{die:'D6',v:4,expr:'4 + 2 ',total:6},target:'foe'});
  atk(lines,b,3.4,{who:'Orso',roller:'Sara',d20:14,mod:5,vs:15,hit:true,dmg:{die:'D6 + 1',v:3,expr:'3 + 1 ',total:4},target:'L'})},45);
 beat(6,'Lia spende l’<b>Ispirazione</b> del Guerriero: −2 AR all’Orso, Difesa 12. Fa 9 + 4 = 13: colpito, e l’Orso cade.',b=>{set(b,0.3,'L',{insp:false});b.at(0.3,s=>{s.foe.dif0=14;s.foe.dif=12});
  atk(lines,b,1.2,{who:'Lia',col:'#a8352a',d20:9,mod:4,vs:12,hit:true,dmg:{die:'D6',v:2,total:2},target:'foe'})},40);}
beat(6,'Ricompensa del mazzetto II: Indizio, PE e Ispirazione. È il <b>secondo Indizio</b>: Lia ha <b>individuato il tesoro</b>!',b=>{phase(b,0,4);clue(b,0.3,'L');add(b,0.6,'L',{pe:1});set(b,0.9,'L',{insp:true});
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:10px"><div class="big">2 Indizi</div><div class="lbl">Il tesoro è individuato</div></div>`})},10);
beat(6,'<b>La voce si sparge</b>: ogni altro eroe prende subito 1 Indizio. Anche Marco e Sara arrivano a 2!',b=>{clue(b,0.8,'M');clue(b,1.4,'S')},5);
beat(6,'Ora il D6 dice dov’è MIMI: 5, si ritira. <b>4!</b> MIMI e il Re Goblin vanno sulla <b>Cripta 4</b>.',b=>{
  dice(b,0,[{t:'D6',v:5,l:'5 → si ritira',dim:1},{t:'D6',v:4,l:'Cripta 4',dt:1.2}],'Dov’è MIMI?','',null);
  b.at(2.8,s=>{s.sala.Boss=false;s.sala.MIMI=false;const [x0,y0]=salaPos(0),[x1,y1]=salaPos(1);s.tok.push({kind:'guard',c:6,r:6,from:[x0,y0],t0:b.t0+2.8,dur:1.2},{kind:'mimi',c:6,r:6,from:[x1,y1],t0:b.t0+2.8,dur:1.2})});
  b.item(4,1.8,'ring',{c:6,r:6,col:'#b8862b'})},20);
beat(6.5,'Marco, a 3 PV, <b>a inizio turno</b> indossa il Diadema della Veggenza (+1 AR). Poi va alla <b>Locanda</b>: sale al livello 2 e torna a 7 PV.',b=>{act(b,'M',1);
  b.item(0,2.6,'cards',{cards:[{name:'Diadema della Veggenza',slot:'Elmo',text:'+1 AR. Una volta per turno ritiri un D6 di un incantesimo.',who:'Marco',deck:'Mago',w:280,col:'#2f5d9c'}],side:`<div class="lbl" style="text-align:left;color:#2a2118">Gli equipaggiamenti si indossano solo a inizio turno.</div>`});
  add(b,0.6,'M',{ar:1,hand:-1});b.at(2.6,s=>s.phase=2);move(b,2.6,'M',[8,5],1);b.at(3.7,s=>{s.phase=3;s.H.M.used.push('casa')});add(b,3.8,'M',{pv:2,pe:1});set(b,4.6,'M',{lv:2,pe:0});add(b,4.6,'M',{pv:2,pvm:2})},45);
{const lines=[];beat(6,'Sara corre alla Cripta e sfida il <b>Re Goblin</b>: 9 PV, ATT +4, Difesa 16. Prima del primo attacco gioca <b>Lancio di Coltello</b>: 2 danni.',b=>{act(b,'S',2);move(b,0,'S',[6,6],0.9);b.at(1,s=>s.phase=3);
  combat(b,1.2,'S',RE,lines,11.9);add(b,2.2,'S',{hand:-1});b.at(3,s=>{s.foe.pv=7});
  b.item(1.6,1.4,'cards',{cards:[{name:'Lancio di Coltello',slot:'Incantesimo · Ladro',text:'All’inizio di uno scontro infliggi 1D6 − 1 danni.',who:'Sara',w:260,col:'#3d7a3f'}]})},40);
 beat(6.5,'Poi colpisce: 17 + 2 = 19, danno 4. Il Re è a 3 PV e va in <b>furia</b>: +2 ATT. Risponde 12 + 6 = 18, danno 4 + 1 = 5. Sara cade.',b=>{
  atk(lines,b,0.2,{who:'Sara',col:'#3d7a3f',d20:17,mod:2,vs:16,hit:true,dmg:{die:'D6',v:4,total:4},target:'foe'});
  atk(lines,b,2.8,{who:'Re Goblin',roller:'Lia',d20:12,mod:6,vs:16,hit:true,dmg:{die:'D6 + 1',v:4,expr:'4 + 1 ',total:5},target:'S'})},50);}
beat(6.5,'Le <b>ferite del boss restano</b>: il cubetto giallo scende a 3. Sara riparte dal D6 (A6) con i PV pieni e tiene i suoi 2 Indizi.',b=>{
  b.at(0.4,s=>{s.gpvAnim={from:9,to:3,t0:b.t0+0.4,dur:1.2};s.gpv=3});set(b,1.8,'S',{down:true});
  dice(b,2,[{t:'D6',v:6,l:'partenza A6'},{t:'D6',v:2,l:'perdita: Elmo (non c’è)',dt:0.5}],'Sconfitta','',null);set(b,3.4,'S',{down:false,pv:5});place(b,3.4,'S',...SPAWN[5])},25);
// GIRO 4
beat(5.5,'<b>Giro 4.</b> Lia tira 4 + 1 = 5: proprio la distanza della <b>Cripta 4</b>. Il Re Goblin è ancora ferito: <b>3 PV</b>.',b=>{banner(b,'Giro 4');st(b,0,{title:'Giro 4',sub:''});b.at(0,s=>{s.giro=4});act(b,'L',2);
  dice(b,0.4,[{t:'D6',v:4,l:'4 + MOV 1 = 5'}],'Movimento','',null);move(b,2.2,'L',[6,6],1.3)},20);
{const lines=[];beat(6,'Il Re è in furia, ma Lia attacca per prima: 14 + 4 = 18 contro Difesa 16. Danno 3… <b>il Re Goblin cade!</b>',b=>{b.at(0,s=>s.phase=3);combat(b,0,'L',{...RE,pv:3,att:6},lines,6);
  atk(lines,b,0.9,{who:'Lia',col:'#a8352a',d20:14,mod:4,vs:16,hit:true,dmg:{die:'D6',v:3,total:3},target:'foe'});b.at(3.4,s=>{s.guardDead=true;s.gpv=0})},40);}
beat(6,'<b>Lia riporta MIMI a Geronimo e vince la partita.</b>',b=>{st(b,0,{title:'Vittoria!',sub:'Lia · Guerriero orco'});b.at(0,s=>{s.phase=-1;s.tok=s.tok.filter(k=>k.kind!=='guard')});
  b.item(0,null,'html',{h:`<div class="ctr" style="flex-direction:column;gap:14px"><svg viewBox="0 0 24 24" width="130" height="130">${ICONS.forziere}</svg><div class="big">Vince Lia!</div></div>`})},10);
beat(9,'',b=>{b.item(0,9,'cover',{a:'COM’È ANDATA',b:'Circa 18 minuti<br>al tavolo',c:'5 di preparazione + 13 di gioco: una partita veloce, chiusa al giro 4',d:'In media il simulatore stima 23 minuti in 2, 27 in 3, 31 in 4 · da verificare con una partita cronometrata'})});
