/* v2 cast + engine glue (paper-cut rig, same look as the Opus Trimurti showcase). Concatenated INSIDE the same function
   scope as engine/paper_kit.js (PK) and library/characters/shiva/shiva_v2.js (see studio/build.py), so tapered(), elbow(),
   drawHead(), drawJata(), POSES, mixPose(), SH, lerp, INKC, skinPK are in scope.
   Engine globals used: clamp, ctx, glow, lotus, figBegin, figFinish, OY, SC_.
   Every character = one spec in CAST drawn by drawHuman() from the same kit: Opus torso, ink-outlined IK arms with gold
   bands and real hands, cloth-covered legs with front-view feet and anklets, draped lower garments (dhoti / short dhoti /
   sari / tiger skin) with pleat fans and borders, necklaces (hara, rudraksha, vanamala), crowns, halos and props.
   Owner design rules: identity cues readable at a glance; anger = red eyes + heavy brows + frown (NO fangs, NO face lines);
   sadness = raised inner brows, drooping lids, tear, downturned mouth; Vishnu's kirita has NO horns; NO stream from
   Shiva's hair; costume always covers the body. */
const hexRgb=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
const toHex=a=>'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
const shade=(h,f)=>toHex(hexRgb(h).map(v=>f<1?v*f:v+(255-v)*(f-1)));
function skinSet(base,extra){const e=extra||{};return Object.assign({browGap:8,skin:base,skinM:shade(base,.86),skinD:shade(base,.6),skinH:shade(base,1.3),gold:'#e0b04a',ash:'#e8e4ee',red:'#d03a2a',tripundra:false,third:false,brow:'#14101a'},e)}
const clothSet=(c,trim)=>({col:c,colL:shade(c,1.25),colD:shade(c,.6),trim:trim||'#d9a441'});
const L_=(c,trim,type,o)=>Object.assign(clothSet(c,trim),{type:type},o||{});

/* ---------- cast ---------- */
const CAST={
 vishnu:skinSet('#3f74c8',{skinH:'#7cabee',skinD:'#22448a',skinM:'#3568b8',hair:{type:'cap',col:'#10101c'},crown:'vishnu',lower:L_('#f6b81e','#c42b3a','dhoti',{pleat:true,dots:'#c42b3a'}),thread:true,uttariya:'#f6e7a8',
   neck:['hara','garland'],kaustubha:true,tilak:'vaishnava',arms4:'vishnu',armlet:'#e6b84a',muscle:.7,halo:{r:104},lip:'#c23a5a',kgem:'#18a57a'}),
 hayagriva:skinSet('#3f74c8',{skinH:'#7cabee',skinD:'#22448a',hair:{type:'none'},headType:'horse',crown:null,lower:L_('#f6b81e','#c42b3a','dhoti',{pleat:true}),uttariya:'#f6e7a8',neck:['garland'],arms4:'vishnu',armlet:'#e6b84a',muscle:.9}),
 brahma:skinSet('#eea466',{skinH:'#ffd6a4',skinD:'#b86a3a',skinM:'#dc8c52',beard:'#f5f1ea',beardLen:40,mustache:'#f5f1ea',tilak:'brahma',brow:'#6a5a54',hair:{type:'cap',col:'#e6e0da'},crown:'brahma',heads3:true,
   lower:L_('#d23a2a','#f2c14e','dhoti',{pleat:true,fan:'#f6a640'}),sash:'#fbf4e4',neck:['hara'],arms4:'brahma',armlet:'#e6b84a',muscle:.45,halo:{r:118},lip:'#b23a3e'}),
 shiva:skinSet('#88a4c4',{skinH:'#c2d6ec',skinD:'#506c90',skinM:'#7492b6',hair:{type:'shiva'},tripundra:true,third:true,brow:'#141020',lower:{type:'tiger',col:'#f09a30',colL:'#ffc060',colD:'#a84a0c',trim:'#5a3a22'},
   neck:['rudraksha'],ashBands:true,vasuki:true,prop:'trishul',armlet:'#e0b04a',bangle:'snake',muscle:.85,halo:{r:108,col:['#f4f8ff','#a8c8f2','#4c5cc4','#d89a3a'],rgb:'130,170,255',rgb2:'210,230,255',petal:'rgba(235,244,255,.45)'},lip:'#7a3a5e',kgem:'#3b7cf0'}),
 daksha:skinSet('#d09868',{hair:{type:'cap',col:'#26262c'},crown:'raja',beard:'#2e2a30',beardLen:16,mustache:'#2e2a30',lower:L_('#9a1c34','#f2c14e','dhoti',{pleat:true,fan:'#c8364e'}),uttariya:'#f2c14e',thread:true,neck:['hara'],tilak:'dot',armlet:'#e0b04a',muscle:.55}),
 manu:skinSet('#d39a68',{hair:{type:'cap',col:'#18141c'},lower:L_('#efe6cc','#b8862a','dhoti'),sash:'#f4efe0',tilak:'dot',muscle:.7,build:.95}),
 adishakti:skinSet('#f0b98a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:L_('#b4182a','#e0b04a','sari'),upper:{type:'choli',col:'#e0b04a'},pallu:'#d8283a',build:.82,neck:['necklace'],armlet:'#e0b04a',bangle:'glass',muscle:0}),
 brahmi:skinSet('#e8b080',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:L_('#d8a040','#b8742e','sari'),upper:{type:'choli',col:'#e8d8a8'},pallu:'#f0e4c0',build:.82,neck:['necklace'],bangle:'glass',muscle:0}),
 madhu:skinSet('#5c5488',{hair:{type:'wild',col:'#0c0a14'},horns:'#e8dcc0',crown:'asura',crownCol:'#2a2440',build:1.28,brow:'#08060c',eyeRed:true,mustache:'#0c0a14',lower:L_('#7a1c1c','#c9a24a','short'),armor:'#7a6a3a',armlet:'#c9a24a',muscle:1,kdef:.55,prop:'sword'}),
 kaitabha:skinSet('#9a4438',{hair:{type:'wild',col:'#140a0a'},horns:'#f0e2c4',crown:'asura',crownCol:'#3a1a14',build:1.16,brow:'#08060c',eyeRed:true,beard:'#140a0a',beardLen:14,mustache:'#140a0a',lower:L_('#2a2a64','#c9a24a','short'),armor:'#6a5a6a',armlet:'#c9a24a',muscle:1,kdef:.55,prop:'gada'})
};
// the seven sages: distinct skin, hair, beard and cloth so each can be told apart
[['vasishtha','#c78a5a','#f0ece4','#e8962a'],['marichi','#b9794a','#2a2430','#efe6cc'],['atri','#cf9566','#e8e4de','#caa040'],['angirasa','#b4784c','#8a8a92','#e8b060'],
 ['pulastya','#c28a5c','#241e2a','#f0e8d0'],['pulaha','#d0986a','#eeeae2','#8aa070'],['kratu','#bc7e50','#5a4434','#e0a040']].forEach(([n,sk,hc,cl],i)=>{
  CAST['rishi'+i]=skinSet(sk,{hair:{type:'jata',col:hc},beard:hc,beardLen:[38,22,34,26,24,40,18][i],mustache:hc,brow:shade(hc,.7),
  lower:L_(cl,'#b8862a','short',{len:.35}),thread:true,neck:['rudraksha'],tilak:'ash',ash:'#efeae4',bangle:'rudraksha',muscle:.4,build:.92,prop:i%2?'mala':'kamandalu',name:n})});

Object.assign(CAST,{
 narada:skinSet('#e6b080',{hair:{type:'jata',col:'#1a1418',small:true},lower:L_('#f2eee4','#e8962a','dhoti',{fan:'#f6d8a0'}),sash:'#ee7b22',thread:true,neck:['tulsi'],tilak:'vaishnava',bangle:'rudraksha',muscle:.35,build:.9,prop:'veena'}),
 kumara:skinSet('#f0b888',{hair:{type:'jata',col:'#16121a',small:true},lower:L_('#f6f2ea','#c9a24a','short',{len:.2}),thread:true,neck:['rudraksha'],tilak:'ash',muscle:.05,build:.8,hs:1.36}),
 jaya:skinSet('#46b0a4',{hair:{type:'none'},crown:'helmet',lower:L_('#e8b838','#b8862a','short'),armor:'#c9a24a',armlet:'#e0b040',muscle:1,build:1.18,brow:'#10202a',prop:'gada'}),
 vijaya:skinSet('#46b0a4',{hair:{type:'none'},crown:'helmet',plume:'#d02a2a',lower:L_('#f6f2ea','#e0b040','short'),armor:'#c9a24a',armlet:'#e0b040',muscle:1,build:1.12,brow:'#10202a',prop:'gada'}),
 villager:skinSet('#b98052',{hair:{type:'turban',col:'#f0e6c8'},beard:'#1e1a1a',beardLen:10,mustache:'#1e1a1a',lower:L_('#f1ead8','#8a6a3a','short',{len:.45}),gamcha:'#c8402a',muscle:.35,build:.95,kundala:'plain'}),
 villager_w:skinSet('#c8905e',{female:true,bindi:true,hair:{type:'long',col:'#1a1416'},lower:L_('#2f86c0','#e8b040','sari'),upper:{type:'choli',col:'#d8402a'},pallu:'#2a78b0',build:.84,neck:['necklace'],bangle:'glass',muscle:0}),
 prasuti:skinSet('#d9a070',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:L_('#a8182a','#e0b04a','sari'),upper:{type:'choli',col:'#e0b04a'},pallu:'#d8283a',build:.82,neck:['necklace'],bangle:'glass',muscle:0}),
 sati:skinSet('#f0b98a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:L_('#f4f0e6','#ef9a1f','sari'),upper:{type:'choli',col:'#ef9a1f'},pallu:'#ef9a1f',build:.8,neck:['necklace'],armlet:'#e0b04a',bangle:'glass',muscle:0}),
 diti:skinSet('#a8704a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},lower:L_('#8a1a3a','#e0b04a','sari'),upper:{type:'choli',col:'#e0b04a'},pallu:'#a8284a',build:.84,neck:['necklace'],bangle:'glass',muscle:0}),
 danu:skinSet('#b87a52',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},lower:L_('#1f7a4a','#e0b04a','sari'),upper:{type:'choli',col:'#e0b04a'},pallu:'#2a9a5a',build:.84,neck:['necklace'],bangle:'glass',muscle:0}),
 asikli:skinSet('#c8905e',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:L_('#3a8fc8','#e0b04a','sari'),upper:{type:'choli',col:'#e8d8a8'},pallu:'#2a78b0',build:.82,neck:['necklace'],bangle:'glass',muscle:0}),
 kashyapa:skinSet('#c8905e',{hair:{type:'jata',col:'#ece8e2'},beard:'#ece8e2',beardLen:46,mustache:'#ece8e2',brow:'#9a9490',lower:L_('#e8862a','#8a3a12','dhoti',{fan:'#f4a850'}),deerskin:true,thread:true,neck:['rudraksha','rudraksha2'],tilak:'ash',bangle:'rudraksha',muscle:.4,build:.94,prop:'kamandalu'}),
 indra:skinSet('#e8b064',{hair:{type:'cap',col:'#18141c'},crown:'indra',mustache:'#2a1a14',lower:L_('#2a52b8','#f2c14e','dhoti',{pleat:true,fan:'#4a78e0',dots:'#f2c14e'}),uttariya:'#f2c14e',neck:['hara'],armlet:'#e0b040',muscle:.85,prop:'vajra',halo:{r:96,col:['#ffffff','#bcd8ff','#5a8ae0','#2a3a8a'],rgb:'150,190,255',rgb2:'220,235,255',petal:'rgba(240,248,255,.45)',g:.55}}),
 surya:skinSet('#f4a848',{hair:{type:'cap',col:'#4a2410'},crown:'raja',lower:L_('#e0501e','#ffd34a','dhoti',{pleat:true,fan:'#ff8a3a'}),uttariya:'#ffd34a',neck:['hara'],armlet:'#ffd34a',muscle:.75,prop:'lotus2',sun:true,kgem:'#ff7a1a'}),
 // EP6 devas crowd: Agni (fire god: ember skin, flame crest, fire halo) and Vayu (wind god: sky-blue cloth, long wind-blown scarf)
 agni:skinSet('#e07a4a',{skinH:'#ffb084',skinD:'#a23e1c',hair:{type:'cap',col:'#5a1a0c'},crown:'agni',beard:'#6a200e',beardLen:14,mustache:'#6a200e',brow:'#4a120a',lower:L_('#b8241a','#ffd34a','dhoti',{pleat:true,fan:'#f27a1e'}),uttariya:'#ffb02a',thread:true,neck:['hara'],armlet:'#ffd34a',muscle:.7,lip:'#9a2a2a',kgem:'#ff7a1a',halo:{r:96,col:['#fff2a0','#ffb030','#e8501a','#8a1a0a'],rgb:'255,150,60',rgb2:'255,220,150',petal:'rgba(255,220,150,.45)',g:.7}}),
 vayu:skinSet('#e2b48a',{hair:{type:'cap',col:'#1c1a24'},crown:'vayu',mustache:'#1c1a24',lower:L_('#3a9ad8','#f2f6ff','dhoti',{pleat:true,fan:'#8ccaf2'}),uttariya:'#eef6ff',sash:'#bfe2fa',neck:['pearls'],armlet:'#e0b040',muscle:.65,kgem:'#7ac8f0',halo:{r:94,col:['#ffffff','#d8f0ff','#7ac0ee','#2a6aa8'],rgb:'160,210,255',rgb2:'230,245,255',petal:'rgba(240,250,255,.5)',g:.55}}),
 chandra:skinSet('#e4ecf6',{skinD:'#98a8c8',hair:{type:'cap',col:'#202838'},crown:'chandra',lower:L_('#f4f6fc','#9ab0d8','dhoti',{pleat:true,fan:'#dce6f8'}),uttariya:'#cfd8ee',neck:['pearls'],armlet:'#c8d4ea',muscle:.5,lip:'#a8506e',kgem:'#dfe8ff',halo:{r:96,col:['#ffffff','#e4ecff','#a8b8e8','#5a6aa8'],rgb:'200,215,255',rgb2:'240,245,255',petal:'rgba(255,255,255,.5)',g:.6}}),
 hiranyaksha:skinSet('#6e3030',{hair:{type:'wild',col:'#0c0a14'},horns:'#e8dcc0',crown:'asura',crownCol:'#4a3418',build:1.3,brow:'#08060c',eyeRed:true,mustache:'#0c0a14',beard:'#0c0a14',beardLen:10,lower:L_('#1e1418','#e0b040','short',{fan:'#3a2a30'}),armor:'#c9a24a',armlet:'#e0b040',muscle:1,kdef:.55,prop:'gada'}),
 hiranyakashipu:skinSet('#8a4a2a',{hair:{type:'wild',col:'#0c0a14'},horns:'#e8c050',crown:'asura',build:1.25,brow:'#08060c',eyeRed:true,mustache:'#0c0a14',lower:L_('#c8282a','#e0b040','short'),armor:'#e0b040',armlet:'#e0b040',muscle:1,kdef:.5,prop:'gada'}),
 ravana:skinSet('#4a3028',{hair:{type:'wild',col:'#0c0a14'},crown:'asura',build:1.28,brow:'#08060c',eyeRed:true,mustache:'#0c0a14',lower:L_('#a8182a','#e0b040','short'),armor:'#e0b040',armlet:'#e0b040',muscle:1,kdef:.45,prop:'sword'})
});

/* ---------- poses (joints in rig units; feet at 0, +y down) ---------- */
const BASE=JSON.parse(JSON.stringify(POSES.calm));delete BASE.tri;BASE.hL=[-86,-262];BASE.hR=[86,-262];
const PZ={
 stand:{},
 namaste:{hL:[-9,-336],hR:[9,-336],ef:1},
 open:{hL:[-150,-348],hR:[150,-348]},
 point:{hR:[178,-410]},
 raise:{hR:[118,-570]},
 plead:{hL:[-20,-304],hR:[20,-304],lean:.10,ef:1},
 bow:{hL:[-20,-296],hR:[20,-296],lean:.34,ef:1},
 hold:{hL:[-80,-262],hR:[90,-330]},
 flee:{lean:.24,kL:[-26,-126],kR:[46,-176],fL:[-66,0],fR:[88,-54],hL:[-125,-336],hR:[100,-300],hem:200,sway:3},
 lunge:{ph:[6,-250],ch:[-4,-372],nk:[-8,-410],hd:[-10,-458],hL:[-135,-385],hR:[150,-330],hipL:[-26,-248],hipR:[34,-246],kL:[-74,-128],kR:[80,-120],fL:[-110,0],fR:[118,0],lean:-.05,sway:3},
 sit:{sit:true,ph:[0,-58],ch:[0,-186],nk:[0,-230],hd:[0,-282],sL:[-62,-212],sR:[62,-212],hL:[-104,-70],hR:[104,-70],hipL:[-28,-62],hipR:[28,-62],kL:[-122,-34],kR:[122,-34],fL:[-38,-12],fR:[38,-12],hem:0}
};
PZ.vstand={hL:[-96,-292],hR:[98,-256]};
PZ.lie2={hL:[-98,-262],hR:[84,-196],kL:[-22,-128],kR:[70,-176],fL:[-34,0],fR:[30,-40],hem:200,sway:0};
PZ.lie={hL:[-70,-486],hR:[64,-232],kL:[-24,-130],kR:[22,-130],fL:[-30,0],fR:[18,0],hem:200,sway:0};
PZ.sitpray={...PZ.sit,hL:[-8,-222],hR:[8,-222],ef:1};
PZ.calm={};PZ.rage={...PZ.lunge};
PZ.rpoint={...PZ.lunge,hR:[196,-440]};  // furious accusing point (Shiva: left hand, trishul stays in the right)
BASE.pointL=false;
const poseOf=(n,who)=>(n&&typeof n==='object')?n:who==='shiva'?shivaPose(n):((who==='vishnu'||who==='hayagriva')&&(!n||n==='stand')?poseOf0('vstand'):poseOf0(n));
const poseOf0=(n)=>Object.assign(JSON.parse(JSON.stringify(BASE)),JSON.parse(JSON.stringify(PZ[n]||PZ[{tri:'hold',rest:'stand',cross:'sit',fist:'hold',cup:'open'}[n]]||{})));

/* ---------- small helpers kept for the recline / ardha rigs ---------- */
function limbS(c,S,A,T,l1,l2,side,w){const r=elbow(A,T,l1,l2,side),E=r.e;inkCap(c,A,E,w[0],w[1]);inkCap(c,E,r.t,w[1],w[2]);tapered(c,A,E,w[0],w[1],S.skin);tapered(c,E,r.t,w[1],w[2],S.skin);r.s=A;return r}
function handS(c,S,p,grip,ang=0){PK.hand(c,skinPK(S),p,ang+Math.PI,grip?'hold':'rest')}
function armband(c,r,w,col){PK.band(c,r.s,r.e,.46,w*.9,col)}
function glow2(c,x,y,r,rgb,a){const g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(1,`rgba(${rgb},0)`);c.fillStyle=g;c.beginPath();c.arc(x,y,r,0,7);c.fill()}
function gada(c,x,y){c.save();c.translate(x,y+70);c.rotate(-Math.PI/2);PK.gada(c,[0,0],[110,0]);c.restore()}
function lotusFlower(c,x,y,s=1){PK.padma(c,x,y+20*s,s*.9,1,0)}

/* ---------- hair & head-dress ---------- */
function hairBack(c,S,P,t){const H=S.hair;if(!H)return;const hx=P.hd[0],hy=P.hd[1];c.save();c.translate(hx,hy);
  if(H.type==='long')PK.hairBack(c,H.col,t,Math.max(120,(P.ph[1]-30)-hy+8));
  else if(H.type==='jata'){if(H.small){c.scale(.8,.8);c.translate(0,-8)}PK.rishiJata(c,H.col)}
  else if(H.type==='wild'){const pts=[];for(let i=0;i<=16;i++){const a=Math.PI*(.78+i/16*1.44),rr=i%2?48:66+Math.sin(i*2.3+t)*3;pts.push([Math.cos(a)*rr,-8+Math.sin(a)*rr*.95])}pts.push([34,30],[0,20],[-34,30]);
    PK.cut(c,PK.P.poly(pts),PK.lg(c,-60,-60,60,30,[PK.shade(H.col,2.6),H.col,'#000000']),{lw:2.2,sh:0});for(let i=1;i<16;i+=2){const a=Math.PI*(.78+i/16*1.44);PK.stroke(c,cc=>{cc.moveTo(Math.cos(a)*22,-8+Math.sin(a)*20);cc.lineTo(Math.cos(a)*56,-8+Math.sin(a)*52)},'rgba(160,140,200,.3)',1.6)}}
  else if(H.type==='shiva'){const sw=(k)=>Math.sin(t*1.1+k*.7)*4;for(let i=0;i<12;i++){const sd=i<6?-1:1,k=i%6,x0=sd*(10+k*4),y0=-52,x1=sd*(44+k*9)+sw(i),y1=70+k*8,x2=sd*(58+k*12)+sw(i)*1.6,y2=142+k*10;
    const f=cc=>{cc.moveTo(x0,y0);cc.bezierCurveTo(sd*40,-42,x1,y1,x2,y2)};PK.stroke(c,f,INKC,14-k);PK.stroke(c,f,k%2?'#3a2c4e':'#2a2038',10-k);PK.stroke(c,f,'rgba(190,170,230,.25)',2,{dash:[6,8]})}}
  c.restore()}
function hairFront(c,S,hx,hy,t){const H=S.hair;if(!H||H.type==='none'||S.headType==='horse')return;c.save();c.translate(hx,hy);
  if(H.type==='turban'){PK.hairCap(c,'#1a1414');PK.turban(c,H.col)}
  else if(H.type==='shiva'){PK.hairCap(c,'#241a30');shivaBun(c,t||0)}
  else{PK.hairCap(c,H.col);if(H.type==='topknot'){PK.cut(c,PK.P.ell(0,-62,17,17),PK.lg(c,-17,0,17,0,[PK.shade(H.col,1.5),H.col]),{lw:2,sh:0});PK.cut(c,cc=>cc.roundRect(-11,-49,22,6,2),PK.goldG(c,-11,11),{lw:1.2,sh:0})}}
  c.restore()}
// Shiva's coiled jata bun with rudraksha band and crescent moon (no water stream)
function shivaBun(c,t){[-1,1].forEach(sd=>{const lp=cc=>{cc.moveTo(sd*20,-60);cc.bezierCurveTo(sd*66,-70,sd*62,-128,sd*26,-118)};PK.stroke(c,lp,INKC,17);PK.stroke(c,lp,'#2c2240',12);PK.stroke(c,lp,'rgba(190,170,240,.3)',2.5,{dash:[5,6]})});
  const bun=[[-30,-48],[-42,-82],[-36,-120],[-16,-146],[14,-148],[36,-124],[42,-84],[30,-48]];PK.cut(c,PK.P.smooth(bun),PK.lg(c,-42,0,42,0,['#55446e','#2c2242','#140e20']),{lw:2.4});
  c.save();c.beginPath();PK.P.smooth(bun)(c);c.clip();for(let i=0;i<8;i++){PK.stroke(c,cc=>cc.ellipse(0,-96+i*2,40-i*5,54-i*6.5,0,Math.PI*(1.1+i*.13),Math.PI*(2.6+i*.13)),i%2?'rgba(190,170,240,.35)':'rgba(6,4,14,.6)',3)}c.restore();
  const tk=cc=>{cc.moveTo(0,-140);cc.bezierCurveTo(-20,-168,18,-178,8,-150)};PK.stroke(c,tk,INKC,14);PK.stroke(c,tk,'#2c2240',9);
  PK.beadArc(c,-31,-56,31,-56,5,11,3.8,'#7a3a1a','rgba(255,200,160,.5)');
  PK.glow(c,-34,-102,60,'230,240,255',.5);PK.cut(c,cc=>{cc.arc(-34,-102,17,Math.PI*.35,Math.PI*1.75);cc.arc(-28,-106,13,Math.PI*1.62,Math.PI*.45,true);cc.closePath()},PK.lg(c,-50,-120,-20,-86,['#ffffff','#f4ecc8']),{lw:1.6,sh:0});
  PK.cut(c,cc=>cc.roundRect(-33,-44,66,8,4),PK.goldG(c,-33,33),{lw:1.4,sh:0})}
function headgear(c,S,hx,hy){c.save();c.translate(hx,hy);
  if(S.horns)[-1,1].forEach(sd=>PK.cut(c,cc=>{cc.moveTo(sd*22,-38);cc.bezierCurveTo(sd*40,-60,sd*58,-70,sd*56,-102);cc.bezierCurveTo(sd*50,-80,sd*34,-62,sd*14,-44);cc.closePath()},PK.lg(c,0,-104,0,-40,['#fff6e0',S.horns,PK.shade(S.horns,.62)]),{lw:2}));
  const cr=S.crown;
  if(cr==='vishnu')PK.kirita(c,66);else if(cr==='devi')PK.kirita(c,58);else if(cr==='small')PK.kirita(c,34);
  else if(cr==='raja')PK.crownK(c,44,{gem:'#18a57a'});else if(cr==='indra')PK.crownK(c,70,{crest:'fan',gem:'#3b7cf0'});else if(cr==='chandra')PK.crownK(c,46,{crest:'moon',gem:'#dfe8ff'});else if(cr==='agni')PK.crownK(c,44,{crest:'flame',gem:'#ff7a1a'});else if(cr==='vayu')PK.crownK(c,40,{crest:'fan',gem:'#7ac8f0'});
  else if(cr==='brahma')PK.jataMukuta(c);else if(cr==='asura')PK.asuraCrown(c,S.crownCol);
  else if(cr==='helmet'){PK.cut(c,cc=>{cc.moveTo(-35,-14);cc.bezierCurveTo(-38,-66,38,-66,35,-14);cc.lineTo(22,-22);cc.lineTo(-22,-22);cc.closePath()},PK.goldG(c,-35,35),{lw:2.2});
    PK.cut(c,cc=>cc.roundRect(-35,-32,70,10,3),PK.goldG(c,-35,35),{lw:1.6,sh:0});for(let k=-2;k<=2;k++)PK.gem(c,k*13,-27,2.6,k%2?'#18a57a':'#e0234a');
    if(S.plume)PK.cut(c,cc=>{cc.moveTo(0,-58);cc.bezierCurveTo(-16,-86,10,-104,24,-98);cc.bezierCurveTo(10,-86,8,-68,6,-56)},S.plume,{lw:1.6,sh:0})}
  c.restore()}
function horseHead(c,hx,hy,k,t){c.save();c.translate(hx,hy);const sw=Math.sin(t*2)*3;
  c.fillStyle='rgba(255,236,176,.5)';for(let i=-3;i<=3;i++){c.beginPath();c.moveTo(i*6,-60);c.bezierCurveTo(i*14+sw,-20,i*17-sw,40,i*15,100+Math.abs(i)*8);c.bezierCurveTo(i*9,40,i*8,-10,i*6+5,-60);c.fill()}
  const g=c.createLinearGradient(-40,0,40,0);g.addColorStop(0,'#fbf8ee');g.addColorStop(.6,'#e8e2d4');g.addColorStop(1,'#a8a2b4');c.fillStyle=g;
  c.beginPath();c.moveTo(-26,-62);c.bezierCurveTo(-46,-30,-40,20,-24,66);c.bezierCurveTo(-12,82,12,82,24,66);c.bezierCurveTo(40,20,46,-30,26,-62);c.bezierCurveTo(12,-72,-12,-72,-26,-62);c.fill();
  c.fillStyle='#1a1018';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*20,-16,6,4.6,sd*-.3,0,7);c.fill()});c.fillStyle=k>.3?'#ff3a20':'#ffe08a';[-1,1].forEach(sd=>{c.beginPath();c.arc(sd*20,-16,2.2,0,7);c.fill()});c.restore()}

/* ---------- body parts ---------- */
const GOLD='#f2c14e';
// one IK arm in the Opus style: outlined limb, elbow crease, armlet + bangles, hand
function armX(c,S,sk,s,tg,bend,o){const w=o.w,r=PK.ik(s,tg,o.l1||66,o.l2||64,bend);
  PK.limbOutline(c,s,r.e,w[0],w[1]*1.05,true);PK.limbOutline(c,r.e,r.t,w[1],w[2]);PK.limb(c,sk,s,r.e,w[0],w[1]*1.05,{lw:0,sh:0});PK.limb(c,sk,r.e,r.t,w[1],w[2],{lw:0,sh:0});
  PK.stroke(c,cc=>{const a=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);cc.arc(r.e[0],r.e[1],w[1]*.6,a+.6,a+2.2)},'rgba(30,10,40,.3)',1.4);
  if(o.sleeve){const m=PK.L2(s,r.e,.42);PK.cut(c,PK.P.caps(s,m,w[0]+2,w[0]),o.sleeve,{lw:1.8,sh:0});PK.stroke(c,cc=>{cc.moveTo(m[0]-(w[0]),m[1]);cc.lineTo(m[0]+w[0],m[1])},GOLD,2)}
  if(S.armlet)PK.band(c,s,r.e,.5,w[0]*.92,S.armlet);
  const bg=S.bangle||(S.armlet?'gold':null);
  if(bg==='gold'){PK.band(c,r.e,r.t,.84,w[2]*1.1,GOLD);PK.band(c,r.e,r.t,.72,w[2]*1.2,GOLD)}
  else if(bg==='glass'){['#d8283a','#f2c14e','#18a57a','#d8283a'].forEach((col,i)=>{const p=PK.L2(r.e,r.t,.66+i*.07),an=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);c.save();c.translate(p[0],p[1]);c.rotate(an);PK.cut(c,cc=>cc.roundRect(-2,-w[2]-2,4,2*w[2]+4,2),col,{sh:0,lw:1});c.restore()})}
  else if(bg==='rudraksha'){const p=PK.L2(r.e,r.t,.8),an=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);c.save();c.translate(p[0],p[1]);c.rotate(an);for(let k=-2;k<=2;k++)PK.cut(c,PK.P.ell(0,k*w[2]*.45,3,3),'#7a3a1a',{sh:0,lw:.8});c.restore()}
  else if(bg==='snake'){const p=PK.L2(r.e,r.t,.78),an=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);c.save();c.translate(p[0],p[1]);c.rotate(an);PK.cut(c,cc=>cc.roundRect(-4,-w[2]-3,8,2*w[2]+6,4),'#3c9a4c',{sh:0,lw:1.2});PK.stroke(c,cc=>{cc.moveTo(0,-w[2]);cc.lineTo(0,w[2])},'#9ce68a',1.2);c.restore()}
  return r}
function handOf(c,sk,r,type,ang,fl){const dir=Math.atan2(r.t[0]-r.e[0],-(r.t[1]-r.e[1]));PK.hand(c,sk,r.t,ang!=null?ang:dir,type,fl)}

// legs + lower garment.  Lower spec L.type: dhoti (to mid-shin) | short (to the knee) | sari (to the ankle) | tiger (Shiva's tiger skin)
function lowerBody(c,S,sk,P,sw,t){const L=S.lower||{type:'short',col:'#f1ead8',colL:'#fff',colD:'#a89878',trim:'#b8862a'},wy=P.ph[1]-4,bw=S.build||1,fem=!!S.female;
  const topW=(fem?40:46)*bw,ty=L.type;
  const leg=(h,f,side)=>{const r=elbow(h,f,86,92,side),k=r.e;return{h,k,f}};
  const lg_=[leg(P.hipL,P.fL,-1),leg(P.hipR,P.fR,1)];
  const shin=(g,sd)=>{PK.limbOutline(c,g.k,[g.f[0],g.f[1]-14],21*bw,12*bw);PK.limb(c,sk,g.k,[g.f[0],g.f[1]-14],21*bw,12*bw,{lw:0,sh:0});PK.footF(c,sk,g.f[0],g.f[1]-4,sd,{anklet:S.anklet||(S.female||S.halo||S.crown?GOLD:false),alta:S.female||!!S.halo})};
  const thigh=(g)=>{PK.limbOutline(c,g.h,g.k,29*bw,22*bw);PK.limb(c,sk,g.h,g.k,29*bw,22*bw,{lw:0,sh:0})};
  const clothTube=(a,b,ra,rb)=>{const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;PK.cut(c,PK.P.caps(a,b,ra,rb),PK.lg(c,a[0]+nx*ra,a[1]+ny*ra,a[0]-nx*ra,a[1]-ny*ra,[L.colL,L.col,L.colD]),{lw:2.2,sh:0});
    [-.45,0,.45].forEach(f=>PK.stroke(c,cc=>{cc.moveTo(a[0]+nx*ra*f,a[1]+ny*ra*f);cc.quadraticCurveTo((a[0]+b[0])/2+nx*ra*(f+.15),(a[1]+b[1])/2+ny*ra*(f+.15),b[0]+nx*rb*f,b[1]+ny*rb*f)},'rgba(40,10,20,.2)',1.4))};
  const hemBand=(a,b,rb)=>{const an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.save();c.translate(b[0],b[1]);c.rotate(an);PK.cut(c,cc=>cc.roundRect(-9,-rb-1,10,2*rb+2,3),L.trim,{lw:1.4,sh:0});if(L.dots)for(let k=-1;k<=1;k++)PK.cut(c,PK.P.ell(-15,k*rb*.55,2.2,2.2),L.dots,{sh:0,lw:.6});c.restore()};
  if(P.sit){ // crossed legs (Opus): a cloth mound with both feet resting on top
    c.save();c.translate(P.ph[0],P.ph[1]+104);
    const lp=[[-172,-96],[-162,-134],[-98,-162],[0,-152],[98,-162],[162,-134],[172,-96],[110,-84],[0,-92],[-110,-84]];
    const legCol=ty==='tiger'?[sk.h,sk.b,sk.d]:(ty==='sari'?[L.colL,L.col,L.colD]:[L.colL,L.col,L.colD]);
    PK.cut(c,PK.P.smooth(lp),PK.lg(c,0,-162,0,-84,legCol),{lw:2.4});PK.stroke(c,cc=>{cc.moveTo(-120,-100);cc.quadraticCurveTo(-30,-124,60,-100)},'rgba(30,20,60,.35)',2);PK.stroke(c,cc=>{cc.moveTo(120,-104);cc.quadraticCurveTo(40,-128,-50,-110)},'rgba(30,20,60,.3)',2);
    if(ty!=='tiger')PK.stroke(c,cc=>{cc.moveTo(-170,-92);cc.quadraticCurveTo(0,-74,170,-92)},L.trim,4);
    [-1,1].forEach(sd=>{if(ty==='sari')return;PK.foot(c,sk,[sd*58,-146],sd*.2,{flip:sd<0,anklet:S.anklet||(S.halo?GOLD:false),alta:!!S.halo})});
    const lc=[[-60,-178],[60,-178],[96,-128],[66,-104],[30,-114],[0,-98],[-30,-114],[-66,-104],[-96,-128]];
    if(ty==='tiger'){PK.cut(c,PK.P.smooth(lc),PK.lg(c,0,-178,0,-100,['#f09a30','#d86a14','#a84a0c']),{lw:2});PK.tigerStripes(c,PK.P.smooth(lc),[-96,-178,96,-98],9,3)}
    else{PK.cut(c,PK.P.smooth(lc),PK.lg(c,0,-178,0,-100,[L.fan||L.colL,L.col]),{lw:2});for(let k=-2;k<=2;k++)PK.stroke(c,cc=>{cc.moveTo(k*8,-176);cc.lineTo(k*16,-104)},'rgba(60,20,10,.3)',1.3)}
    c.restore();return}
  // standing / walking
  lg_.forEach((g,i)=>{const sd=i?1:-1;shin(g,sd);thigh(g)});
  if(ty==='sari'){const fx=Math.max(Math.abs(P.fL[0]),Math.abs(P.fR[0]))+30,hy=Math.min(P.fL[1],P.fR[1])-14,hm=Math.max(-6,hy);
    const sk_=cc=>{cc.moveTo(-topW,wy);cc.lineTo(topW,wy);cc.bezierCurveTo(topW+26,wy+90,fx-6,hm-80,fx+4+sw*2,hm);for(let i=0;i<=10;i++){const u=i/10;cc.lineTo(lerp(fx+4,-fx-4,u)+sw*2,hm+Math.sin(u*9+sw)*3)}cc.bezierCurveTo(-fx+6,hm-80,-topW-26,wy+90,-topW,wy);cc.closePath()};
    PK.cut(c,sk_,PK.lg(c,-fx,0,fx,0,[L.colL,L.col,L.colD]),{lw:2.4});
    c.save();c.beginPath();sk_(c);c.clip();for(let i=-4;i<=4;i++)PK.stroke(c,cc=>{cc.moveTo(i*topW/5,wy+8);cc.quadraticCurveTo(i*fx/4+sw*2,(wy+hm)/2,i*fx/3.6+sw*3,hm)},'rgba(30,10,20,.2)',1.6);
    c.fillStyle=L.trim;c.fillRect(-fx-20,hm-16,2*fx+40,12);c.fillStyle='rgba(255,240,190,.5)';for(let i=0;i<14;i++){c.beginPath();c.arc(-fx+i*fx/6.5,hm-10,2,0,7);c.fill()}c.restore();
    const pf=cc=>{cc.moveTo(-14,wy+4);cc.lineTo(14,wy+4);cc.lineTo(34+sw*2,hm-2);cc.lineTo(-30+sw*2,hm-2);cc.closePath()};PK.cut(c,pf,PK.lg(c,-30,0,34,0,[L.colL,shade(L.col,1.1),L.colD]),{lw:1.8,sh:0});
    for(let k=-3;k<=3;k++)PK.stroke(c,cc=>{cc.moveTo(k*4,wy+8);cc.lineTo(k*9+sw*2,hm-6)},'rgba(40,10,20,.35)',1.3);PK.stroke(c,cc=>{cc.moveTo(-30+sw*2,hm-8);cc.lineTo(34+sw*2,hm-8)},L.trim,6);
  }else if(ty==='tiger'){const tp=[[-topW-6,wy-6],[0,wy-10],[topW+6,wy-6],[topW+16,wy+40],[P.hipR[0]+30,wy+96],[P.hipR[0]+6,wy+84],[P.hipR[0]-10,wy+108],[10,wy+88],[0,wy+102],[-14,wy+86],[P.hipL[0]+8,wy+110],[P.hipL[0]-8,wy+86],[P.hipL[0]-32,wy+98],[-topW-16,wy+40]];
    PK.cut(c,PK.P.smooth(tp),PK.lg(c,0,wy-10,0,wy+110,['#f09a30','#d86a14','#a84a0c']),{lw:2.2});PK.tigerStripes(c,PK.P.smooth(tp),[-topW-16,wy-10,topW+30,wy+110],14,7);
    PK.cut(c,PK.P.smooth([[P.hipL[0]-24,wy+76],[P.hipL[0]-14,wy+84],[P.hipL[0]-18,wy+120],[P.hipL[0]-27,wy+128],[P.hipL[0]-36,wy+120],[P.hipL[0]-34,wy+92]]),PK.lg(c,0,wy+70,0,wy+130,['#f09a30','#d86a14','#a84a0c']),{lw:1.8});
    for(let k=0;k<3;k++)PK.cut(c,PK.P.ell(P.hipL[0]-36+k*7,wy+128,2.4,3),'#f4ead8',{sh:0,lw:.8});
    PK.cut(c,cc=>cc.roundRect(-topW-4,wy-10,2*topW+8,12,5),'#5a3a22',{lw:1.6,sh:0});for(let i=-4;i<=4;i++)PK.stroke(c,cc=>{cc.moveTo(i*11-3,wy-9);cc.lineTo(i*11+3,wy+1)},'rgba(255,220,160,.4)',1.3);
  }else{const len=L.len!=null?L.len:(ty==='dhoti'?.6:.12);
    lg_.forEach(g=>{const e=PK.L2(g.k,g.f,len),ra=31*bw,rk=25*bw,rb=(ty==='dhoti'?24:25)*bw;clothTube([g.h[0],wy+10],g.k,ra,rk);clothTube(g.k,e,rk,rb);hemBand(g.k,e,rb)});
    const ky=Math.min(lg_[0].k[1],lg_[1].k[1]),panel=[[-topW,wy-2],[topW,wy-2],[topW+8,wy+46],[lg_[1].k[0]-12,ky-26],[0,ky-6],[lg_[0].k[0]+12,ky-26],[-topW-8,wy+46]];
    PK.cut(c,PK.P.smooth(panel),PK.lg(c,-topW,0,topW,0,[L.colL,L.col,L.colD]),{lw:2.2,sh:0});
    PK.stroke(c,cc=>{cc.moveTo(-topW*.6,wy+20);cc.quadraticCurveTo(0,ky-40,topW*.7,wy+30)},'rgba(40,10,20,.22)',1.6);
    // front pleat fan
    const fb=ty==='dhoti'?Math.min(lg_[0].f[1],lg_[1].f[1])-64:ky+18,fw=ty==='dhoti'?30:24;
    const pf=cc=>{cc.moveTo(-12,wy+4);cc.lineTo(12,wy+4);cc.quadraticCurveTo(16,(wy+fb)/2,fw+sw*2,fb);cc.lineTo(-fw+sw*2,fb+4);cc.quadraticCurveTo(-16,(wy+fb)/2,-12,wy+4);cc.closePath()};
    PK.cut(c,pf,PK.lg(c,-fw,0,fw,0,[L.fan||L.colL,shade(L.fan||L.col,1.08),shade(L.fan||L.col,.75)]),{lw:1.8,sh:1});
    for(let k=-3;k<=3;k++)PK.stroke(c,cc=>{cc.moveTo(k*3.4,wy+8);cc.lineTo(k*fw/3.4+sw*2,fb-2)},'rgba(60,20,10,.35)',1.3);
    PK.stroke(c,cc=>{cc.moveTo(-fw+sw*2,fb);cc.lineTo(fw+sw*2,fb-4)},L.trim,5)}
}

// torso garments, jewellery and armour (drawn in the torso frame: waist at 0, shoulders at -h)
function torsoDress(c,S,sk,h,sw,ww,b,t){const fem=!!S.female,N=S.neck||[];
  if(S.armor){const A=S.armor;PK.cut(c,cc=>{cc.moveTo(-sw+10,-h+16+b);cc.quadraticCurveTo(0,-h+4+b,sw-10,-h+16+b);cc.lineTo(ww+6,-6);cc.quadraticCurveTo(0,6,-ww-6,-6);cc.closePath()},PK.lg(c,-sw,0,sw,0,[shade(A,1.4),A,shade(A,.55)]),{lw:2.4});
    c.save();c.beginPath();c.moveTo(-sw+10,-h+16+b);c.quadraticCurveTo(0,-h+4+b,sw-10,-h+16+b);c.lineTo(ww+6,-6);c.quadraticCurveTo(0,6,-ww-6,-6);c.closePath();c.clip();
    for(let y=-h*.5;y<0;y+=12)for(let x=-sw;x<sw;x+=16)PK.stroke(c,cc=>cc.arc(x+((y/12)%2?8:0),y,8,.2,Math.PI-.2),'rgba(40,20,10,.4)',1.4);
    PK.stroke(c,cc=>{cc.moveTo(0,-h+10);cc.lineTo(0,-h*.55)},'rgba(40,20,10,.4)',2);c.restore();
    [-h*.62,-h*.4,-h*.2].forEach(y=>PK.stroke(c,cc=>{cc.moveTo(-ww-4,y+6);cc.quadraticCurveTo(0,y-4,ww+4,y+6)},shade(A,1.5),3));
    PK.stroke(c,cc=>{cc.moveTo(-sw+10,-h+16+b);cc.quadraticCurveTo(0,-h+4+b,sw-10,-h+16+b)},PK.PAL.gold,4);
    PK.cut(c,PK.P.ell(0,-h*.62,11,11),PK.goldG(c,-11,11),{lw:1.6,sh:0});PK.gem(c,0,-h*.62,5,'#e0234a')}
  if(fem&&S.upper){const ch=cc=>{cc.moveTo(-sw+4,-h+10+b);cc.quadraticCurveTo(-sw*.4,-h+2+b,0,-h+16+b);cc.quadraticCurveTo(sw*.4,-h+2+b,sw-4,-h+10+b);cc.lineTo(sw-12,-h*.56);cc.quadraticCurveTo(0,-h*.48,-sw+12,-h*.56);cc.closePath()};
    PK.cut(c,ch,PK.lg(c,-sw,0,sw,0,[shade(S.upper.col,1.3),S.upper.col,shade(S.upper.col,.6)]),{lw:2});PK.stroke(c,cc=>{cc.moveTo(-sw+12,-h*.56);cc.quadraticCurveTo(0,-h*.48,sw-12,-h*.56)},GOLD,3)}
  if(S.ashBands)[-104,-96,-88].forEach((y,i)=>PK.stroke(c,cc=>{cc.moveTo(-40+i,y*h/160+b*.5);cc.quadraticCurveTo(0,y*h/160-6+b*.5,40-i,y*h/160+b*.5)},'rgba(250,250,245,.85)',3));
  if(S.deerskin)PK.cut(c,cc=>{cc.moveTo(-sw+6,-h+8+b);cc.bezierCurveTo(-sw*.2,-h*.7,ww*.4,-h*.4,ww+4,-h*.12);cc.lineTo(ww-10,-h*.02);cc.bezierCurveTo(0,-h*.34,-sw*.5,-h*.6,-sw+18,-h+4+b);cc.closePath()},PK.lg(c,-sw,0,ww,0,['#d8b080','#b07a48','#7a4a28']),{lw:1.8,sh:0});
  if(S.sash){PK.ribbon(c,[[-sw+8,-h+8+b],[-sw*.3,-h*.62],[ww*.3,-h*.3],[ww-2,-6]],8,9,PK.lg(c,-sw,0,ww,0,[shade(S.sash,1.1),S.sash,shade(S.sash,.75)]),{edge:GOLD,ew:2,sh:1})}
  if(S.thread){const f=cc=>{cc.moveTo(-sw+12,-h+6+b);cc.quadraticCurveTo(-4,-h*.48,ww-4,-8)};PK.stroke(c,f,INKC,3.4);PK.stroke(c,f,'#fff4dc',1.8)}
  if(S.pallu){PK.ribbon(c,[[sw-6,-h+6+b],[sw*.3,-h*.66],[-ww*.4,-h*.3],[-ww-6,-4],[-ww-14,40]],13,15,PK.lg(c,-sw,0,sw,0,[shade(S.pallu,1.25),S.pallu,shade(S.pallu,.65)]),{edge:GOLD,ew:3,folds:1,sh:1})}
  if(S.gamcha)PK.ribbon(c,[[-sw+2,-h+2+b],[-sw*.2,-h+14+b],[sw*.2,-h+14+b],[sw-2,-h+2+b]],7,7,PK.lg(c,0,-h,0,-h+20,[shade(S.gamcha,1.2),S.gamcha]),{edge:'#f4e8c8',ew:1.6});
  // belt
  if(S.lower&&S.lower.type!=='tiger'&&S.lower.type!=='sari'){if(S.halo||S.crown||S.armor){PK.cut(c,cc=>cc.roundRect(-ww-3,-12,2*ww+6,16,6),PK.goldG(c,-ww,ww),{lw:2,sh:0});for(let k=-3;k<=3;k++)if(Math.abs(k*12)<ww)PK.gem(c,k*12,-4,2.6,k%2?'#18a57a':'#e0234a')}
    else{const bc=S.sash||S.lower.trim;PK.cut(c,cc=>cc.roundRect(-ww-3,-11,2*ww+6,12,5),PK.lg(c,0,-11,0,1,[shade(bc,1.2),bc,shade(bc,.7)]),{lw:1.8,sh:0});PK.cut(c,PK.P.ell(ww*.5,-5,6,6),shade(bc,.85),{lw:1.4,sh:0})}}
  // necklaces
  N.forEach(n=>{if(n==='hara')PK.hara(c,-h+12,30,[12,22,34],b);
    else if(n==='pearls')PK.hara(c,-h+12,30,[12,22,32],b,{cols:['#fff7e8','#dfe8ff'],gem:'#dfe8ff'});
    else if(n==='necklace')PK.hara(c,-h+12,24,[10,20],b,{gem:'#18a57a'});
    else if(n==='rudraksha')PK.beadArc(c,-34,-h+14+b,34,-h+14+b,58,17,4.2,'#7a3a1a','rgba(255,200,160,.5)');
    else if(n==='rudraksha2')PK.beadArc(c,-28,-h+12+b,28,-h+12+b,90,19,3.8,'#6a2e14','rgba(255,200,160,.5)');
    else if(n==='tulsi')PK.beadArc(c,-30,-h+12+b,30,-h+12+b,46,16,3.2,'#e8d8a0','rgba(255,255,255,.6)');
    else if(n==='garland')PK.garland(c,-sw*.6,-h+10+b,sw*.6,-h+10+b,h+86,58,t)});
  if(S.kaustubha){PK.glow(c,0,-h*.6,22,'255,70,60',.7);PK.gem(c,0,-h*.6,6,'#e0234a')}}

/* ---------- the generic paper-cut human ---------- */
function drawHuman(c,S,P0,o){
  const t=o.t||0,k=o.k!=null?o.k:(S.kdef||0),br=Math.sin(t*1.7)*2.2,sw=Math.sin(t*1.5)*.6+(P0.sway||0)*.3,P=JSON.parse(JSON.stringify(P0)),bw=S.build||1,fem=!!S.female,sk=skinPK(S);
  ['ch','nk','hd','sL','sR'].forEach(a=>{P[a][1]+=br});P.hL[1]+=br*.6;P.hR[1]+=br*.6;P.sL[0]*=bw;P.sR[0]*=bw;
  const HS=S.hs||(fem?1.06:1.12);c.save();
  // halo / sun disk behind the head
  const hcy=P.hd[1]-(S.heads3?18:10);
  // halo, sun disk and back hair lean WITH the torso (bow / plead), so they stay centred behind the head
  const leanT=()=>{if(P.lean){c.translate(0,P.ph[1]);c.rotate(P.lean);c.translate(0,-P.ph[1])}};
  c.save();leanT();
  if(S.halo&&o.halo!==false){const Hh=S.halo;PK.halo(c,P.hd[0],hcy,Hh.r*(P.sit?.92:1),t,Object.assign({g:Hh.g==null?.8:Hh.g,n:26},Hh))}
  if(S.sun&&o.halo!==false)PK.sunDisk(c,P.hd[0],hcy,92,t);
  c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);hairBack(c,S,P,t);c.restore();
  // Shiva's trishul stands behind the right hand
  const tri=S.prop==='trishul'?(P.tri||{x:P.hR[0],top:-640,bot:0}):null;
  if(tri){c.save();if(tri.rot){c.translate(P.hR[0],-300);c.rotate(tri.rot);c.translate(-P.hR[0],300)}PK.trishul(c,P.hR[0],tri.bot||0,(tri.bot||0)-tri.top,t,0);c.restore()}
  lowerBody(c,S,sk,P,sw,t);
  c.save();if(P.lean){c.translate(0,P.ph[1]);c.rotate(P.lean);c.translate(0,-P.ph[1])}
  // torso frame
  const W0=[P.ph[0],P.ph[1]-4],h=W0[1]-Math.min(P.sL[1],P.sR[1])+8,tsw=(fem?50:64)*bw,ww=(fem?36:42)*bw,ta=Math.atan2(P.nk[0]-P.ph[0],P.ph[1]-P.nk[1]);
  // uttariya ends hang behind the arms
  if(S.uttariya){[[P.sL,P.hL,1,-1],[P.sR,P.hR,-1,1]].forEach(([s0,h0,bd,sd])=>{const r=PK.ik(s0,h0,66,64,bd),e=r.e,fl=Math.sin(t*1.8+sd)*5+sw*4,ub=PK.lg(c,e[0]-14,0,e[0]+14,0,[shade(S.uttariya,1.15),S.uttariya,shade(S.uttariya,.7)]);
    PK.ribbon(c,[[s0[0]-sd*10,s0[1]-6],[e[0]+sd*16,e[1]-6],[e[0]+sd*(22+fl),e[1]+60],[e[0]+sd*(16+fl*1.4),e[1]+130]],6,10,ub,{folds:1,lw:1.6,edge:GOLD,ew:1.6})})}
  const sk4=S.arms4;if(sk4)backArms(c,S,sk,P,t);
  // Narada's veena rests across the body, behind the arms
  c.save();c.translate(W0[0],W0[1]);c.rotate(ta);PK.torso(c,sk,h,tsw,ww,0,{fem:fem,muscle:S.muscle});torsoDress(c,S,sk,h,tsw,ww,0,t);c.restore();
  if(S.prop==='veena')PK.veena(c,P.ph[0]+30,P.ph[1]-(P.sit?40:60),-.62,1.0);
  // neck + head
  PK.cut(c,PK.P.caps([P.nk[0],P.nk[1]+12],[P.hd[0],P.hd[1]+30],15*Math.min(bw,1.15),14*Math.min(bw,1.15)),S.skinM,{lw:2,sh:0});
  if(S.vasuki)vasuki(c,P,t,k);
  if(!o.noHead){c.save();c.translate(P.hd[0],P.hd[1]+40);c.rotate(o.tilt||0);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);
    if(S.headType==='horse')horseHead(c,P.hd[0],P.hd[1]+10,k,t);
    else{if(S.heads3)sideHeads(c,S,P.hd[0],P.hd[1],o,k,t);const turn=o.turn!=null?o.turn:.1;drawHead(c,P.hd[0],P.hd[1],{expr:o.expr||'calm',k:k,S:S,t:t,mood:o.mood,turn:turn});hairFront(c,S,P.hd[0],P.hd[1],t);headgear(c,S,P.hd[0],P.hd[1])}
    c.restore()}
  if(S.vasuki)PK.hood(c,P.sR[0]+30,P.sR[1]-66,.22+Math.sin(t*1.4)*.1,.62,t,VSK,{ph:2,eye:k>.5?'#ff5a3a':'#ffd34a'});
  frontArms(c,S,sk,P,o,t,k);
  if(S.armor)[P.sL,P.sR].forEach((s,i)=>{const sd=i?1:-1;PK.cut(c,cc=>{cc.moveTo(s[0]-sd*14,s[1]-14);cc.quadraticCurveTo(s[0]+sd*24,s[1]-24,s[0]+sd*30,s[1]+12);cc.quadraticCurveTo(s[0]+sd*10,s[1]+18,s[0]-sd*12,s[1]+8);cc.closePath()},PK.lg(c,s[0]-20,0,s[0]+30,0,[shade(S.armor,1.5),S.armor,shade(S.armor,.6)]),{lw:2,sh:0});PK.gem(c,s[0]+sd*8,s[1]-4,3,'#e0234a')});
  c.restore();c.restore()}
const VSK={b:'#3c9a4c',d:'#1c5a2c',l:'#9ce68a',belly:'#f6e48e',bellyD:'#c8a040'};
function vasuki(c,P,t,k){const nx=P.nk[0],ny=P.nk[1]+10,vp=PK.ellPts(nx,ny,40,22,Math.PI*1.02,-.1,14);for(let i=1;i<=8;i++){const u=i/8;vp.push([nx+PK.lerp(40,P.sR[0]+30-nx,u)+Math.sin(u*Math.PI)*8,ny-u*(ny-(P.sR[1]-30))+Math.sin(u*Math.PI)*6])}PK.tube(c,vp,8,7,VSK,{scales:false,belly:1})}
function sideHeads(c,S,hx,hy,o,k,t){const H=o.hd,ez=v=>v*v*(3-2*v);const one=(dx,dy,s,turn)=>{c.save();c.translate(hx+dx,hy+dy);c.scale(s,s);c.filter='brightness(.82)';drawHead(c,0,0,{expr:o.expr||'calm',k:k,S:S,t:t+dx*.01,mood:{smile:.25},turn:turn});PK.hairCap(c,S.hair.col);PK.jataMukuta(c);c.filter='none';c.restore()};
  const l=H?ez(H.l||0):1,r=H?ez(H.r||0):1;if(l>.02)one(-18-26*l,8,.8*l,-.6);if(r>.02)one(18+26*r,8,.8*r,.6)}
function frontArms(c,S,sk,P,o,t,k){const fem=!!S.female,bw=S.build||1,w=[(fem?14:17)*Math.min(bw,1.25),(fem?11:13.5)*Math.min(bw,1.25),(fem?8.5:10.5)*Math.min(bw,1.2)];
  const sl=fem&&S.upper?S.upper.col:null,dL=Math.hypot(P.hL[0]-P.hR[0],P.hL[1]-P.hR[1]),join=dL<60&&!P.sit,joinSit=dL<60&&P.sit;
  const typ=(s,hh,sd)=>{if(join||joinSit)return'pray';if(hh[1]<s[1]-40)return'abhaya';const ext=Math.abs(hh[0]-s[0])>92&&hh[1]<s[1]+50;if(ext)return'ext';if(P.sit)return'jnana';return'rest'};
  const tl=typ(P.sL,P.hL,-1),tr=typ(P.sR,P.hR,1),both=tl==='ext'&&tr==='ext';
  const aL=armX(c,S,sk,P.sL,P.hL,1,{w,sleeve:sl}),aR=armX(c,S,sk,P.sR,P.hR,-1,{w,sleeve:sl});
  const pr=S.prop||o.prop;
  const hand=(a,ty,sd)=>{const dir=Math.atan2(a.t[0]-a.e[0],-(a.t[1]-a.e[1]));
    if(ty==='pray'){PK.hand(c,sk,[a.t[0]-sd*2,a.t[1]+6],sd*-.08,'rest',sd>0?-1:1);return}
    if(ty==='abhaya'){PK.hand(c,sk,a.t,sd*.12,'abhaya');return}
    if(ty==='ext'){if(both||sd<0)PK.hand(c,sk,a.t,dir*.55,'abhaya');else PK.hand(c,sk,a.t,dir,'point');return}
    if(ty==='jnana'){PK.hand(c,sk,a.t,sd*-2.6,'jnana',sd>0?-1:1);return}
    PK.hand(c,sk,a.t,dir,'rest')};
  // props carried in a lowered hand
  const holdR=tr==='rest'&&!S.arms4,holdL=tl==='rest'&&!S.arms4;let usedR=false,usedL=false;
  if(S.prop==='trishul'){const dL=Math.atan2(aL.t[0]-aL.e[0],-(aL.t[1]-aL.e[1]));if(P.pointL)PK.hand(c,sk,aL.t,dL,'point',-1);else PK.hand(c,sk,aL.t,dL,tl==='abhaya'?'abhaya':(tl==='ext'?'abhaya':'rest'));PK.hand(c,sk,aR.t,0,'hold');return}
  if(holdR&&(pr==='gada'))PK.gada(c,[aR.t[0]+4,aR.t[1]+70],[aR.t[0]+4,aR.t[1]-60]);
  if(holdR&&pr==='sword')PK.sword(c,aR.t[0]+2,aR.t[1]+8,.35,1.1);
  if(holdR&&pr==='vajra')PK.vajra(c,aR.t[0]+2,aR.t[1]-30,.4,.9);
  if(holdR&&pr==='mala'){PK.mala(c,aR.t[0],aR.t[1]-6,t);}
  if(holdL&&pr==='kamandalu'){c.save();c.translate(aL.t[0]-4,aL.t[1]+30);c.scale(.8,.8);PK.kamandalu(c,0,0);c.restore()}
  if(pr==='lotus2'){if(holdR||tr==='abhaya'){PK.padma(c,aR.t[0],aR.t[1]-22,.9,1,t);usedR=true}if(holdL||tl==='abhaya'){PK.padma(c,aL.t[0],aL.t[1]-22,.9,1,t);usedL=true}}
  const grip=x=>x&&(pr==='gada'||pr==='sword'||pr==='vajra'||pr==='lotus2');
  hand(aL,tl,-1);if(holdR&&grip(true))PK.hand(c,sk,aR.t,0,'hold');else hand(aR,tr,1);
  if(S.arms4==='vishnu'&&!P.sit){if(tr==='rest')PK.gada(c,[aR.t[0]+4,aR.t[1]+90],[aR.t[0]+4,aR.t[1]-50]);if(tl==='rest')PK.padma(c,aL.t[0],aL.t[1]-18,1,1,t)}
  if(S.arms4==='brahma'&&tl==='rest'){c.save();c.translate(aL.t[0]-4,aL.t[1]+34);c.scale(.85,.85);PK.kamandalu(c,0,0);c.restore()}}
function backArms(c,S,sk,P,t){const sd2=[-1,1],w=[15,12,9.5];sd2.forEach(sd=>{const A=[P.sL[0]*(sd<0?1:0)+P.sR[0]*(sd>0?1:0)-sd*8,(sd<0?P.sL[1]:P.sR[1])+4],T=[sd*140,P.hd[1]+8];
  const r=armX(c,S,sk,A,T,sd<0?-1:1,{w,l1:64,l2:62});PK.hand(c,sk,r.t,sd*.2,S.arms4==='vishnu'?'hold':'hold');
  if(S.arms4==='vishnu'){if(sd<0)PK.chakra(c,r.t[0]-2,r.t[1]-48,24,t,1);else PK.shankha(c,r.t[0]+4,r.t[1]-28,.35,.95)}
  else{if(sd<0)PK.veda(c,r.t[0]+2,r.t[1]-26,-.12);else PK.mala(c,r.t[0],r.t[1]-6,t)}})}

/* ---------- Brahma: seated on the lotus (the Opus hero) or standing with the generic rig ---------- */
const BRAHMA=CAST.brahma;
const BFX=[{smile:.45},{smile:.2,lx:.6},{blink:1,smile:.3},{smile:.3,lx:-.6,blink:.35}];
function drawBrahmaRig(c,o){const P0=o.P;if(P0&&!P0.sit){drawHuman(c,BRAHMA,P0,{t:o.t,k:o.k,expr:o.expr,mood:o.mood,hd:o.hd,tilt:o.tilt,halo:o.halo});return}
  const t=o.t||0,k=o.k||0,by=Math.sin(t*1.4)*2.2,SKB=skinPK(BRAHMA),M=o.mood||{},H=o.hd,ez=v=>v*v*(3-2*v);c.save();c.scale(.86,.86);
  const bless=P0&&P0.hR&&P0.hR[1]<-400?1:(M.bless!=null?M.bless:.5),open=P0&&P0.hL&&P0.hL[0]<-130?1:0,pray=P0&&P0.hL&&Math.abs(P0.hL[0]-P0.hR[0])<60;
  if(o.halo!==false)PK.halo(c,0,-376+by*.4,148,t,{g:.85});
  if(o.lotus!==false)PK.lotusSeat(c,t,'back',1);
  const bL=[-50,-288+by],bR=[50,-288+by],sw=Math.sin(t*1.1)*3;
  const aBL=PK.arm(c,SKB,bL,[-166,-386+sw-open*20],{bend:-1,w:[14,11,9],l1:70,l2:66});PK.veda(c,aBL.t[0]+2,aBL.t[1]-28,-.12);
  const aBR=PK.arm(c,SKB,bR,[166,-386-sw-open*20],{bend:1,w:[14,11,9],l1:70,l2:66});PK.mala(c,aBR.t[0],aBR.t[1]-6,t);
  const lp=[[-160,-72],[-168,-104],[-128,-140],[-60,-150],[0,-144],[60,-150],[128,-140],[168,-104],[160,-72],[80,-60],[0,-64],[-80,-60]];
  PK.cut(c,PK.P.smooth(lp),PK.lg(c,0,-150,0,-60,['#f07a40','#d23a2a','#8e1a1c']),{lw:2.4});
  [-110,-70,70,110].forEach(x=>PK.stroke(c,cc=>{cc.moveTo(x*.7,-140);cc.quadraticCurveTo(x,-110,x*1.2,-72)},'rgba(80,10,10,.35)',1.6));
  PK.stroke(c,cc=>{cc.moveTo(-162,-78);cc.quadraticCurveTo(-80,-54,0,-60);cc.quadraticCurveTo(80,-54,162,-78)},PK.PAL.gold,5);
  [-1,1].forEach(sd=>PK.foot(c,SKB,[sd*62,-138],sd*.18,{flip:sd<0}));
  PK.cut(c,PK.P.poly([[-16,-142],[16,-142],[30,-62],[-30,-62]]),PK.lg(c,-30,0,30,0,['#ffd08a','#f6a640','#c66a20']),{lw:1.8});for(let q=-2;q<=2;q++)PK.stroke(c,cc=>{cc.moveTo(q*5,-140);cc.lineTo(q*11,-64)},'rgba(120,50,0,.45)',1.3);PK.stroke(c,cc=>{cc.moveTo(-30,-66);cc.lineTo(30,-66)},PK.PAL.gold,4);
  if(o.lotus!==false)PK.lotusSeat(c,t,'front',1);
  c.save();c.translate(0,-138);PK.torso(c,SKB,152,68,44,by,{muscle:.45});
  PK.cut(c,cc=>{cc.moveTo(-64,-146+by);cc.quadraticCurveTo(-20,-110,44,-8);cc.lineTo(26,2);cc.quadraticCurveTo(-30,-86,-62,-120+by);cc.closePath()},PK.lg(c,-60,-140,40,0,['#fffaf0','#e8dcc4']),{lw:1.8});
  PK.stroke(c,cc=>{cc.moveTo(-60,-142+by);cc.quadraticCurveTo(-18,-108,40,-6)},PK.PAL.gold,2.4);
  PK.cut(c,cc=>cc.roundRect(-44,-12,88,16,6),PK.goldG(c,-44,44),{lw:2,sh:0});for(let q=-3;q<=3;q++)PK.gem(c,q*12,-4,2.6,q%2?PK.PAL.emer:PK.PAL.ruby);
  PK.hara(c,-150,30,[12,22,34],by);c.restore();
  // heads: back face peeks above, side faces turned, then the front face
  const hc=[0,-366+by];PK.cut(c,PK.P.caps([0,-292+by],[0,-336+by],13,13),SKB.m,{lw:2});
  const head=(x,y,s,turn,E,dark,front)=>{c.save();c.translate(x,y);c.scale(s,s);if(dark)c.filter='brightness(.82)';
    drawHead(c,0,0,{expr:front?(o.expr||'calm'):'calm',k:front?k:k*.8,S:BRAHMA,t:t+x*.01,mood:front?M:Object.assign({},E,{sad:(M.sad||0)*.8}),turn:turn});
    c.save();c.scale(1-Math.abs(turn)*.3,1);c.translate(turn*5,0);PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);c.restore();c.filter='none';c.restore()};
  const sB=H?ez(H.b||0):1,sLft=H?ez(H.l||0):1,sRt=H?ez(H.r||0):1;
  if(sB>.02)head(0,hc[1]-30*sB,.62*sB,0,BFX[2],true,false);
  if(sLft>.02)head(-44*sLft,hc[1]+6,.84*sLft,-.62,BFX[1],true,false);
  if(sRt>.02)head(44*sRt,hc[1]+6,.84*sRt,.62,BFX[3],true,false);
  head(0,hc[1]+4,1,0,BFX[0],false,true);
  if(H&&H.t>.01)head(0,hc[1]-120+20*(1-ez(H.t)),.7*ez(H.t),0,BFX[0],false,false);
  // front arms: kamandalu on the knee (or both hands joined), right hand blessing
  if(pray){PK.arm(c,SKB,[-64,-284+by],[-6,-206],{bend:1,w:[16,13,10],cap:1,hand:'rest',ang:.08,flip:-1});PK.arm(c,SKB,[64,-284+by],[6,-206],{bend:-1,w:[16,13,10],cap:1,hand:'rest',ang:-.08})}
  else if(open){PK.arm(c,SKB,[-64,-284+by],[-150,-250],{bend:1,w:[16,13,10],cap:1,hand:'abhaya',ang:-.7});PK.arm(c,SKB,[64,-284+by],[150,-250],{bend:-1,w:[16,13,10],cap:1,hand:'abhaya',ang:.7})}
  else{PK.kamandalu(c,-112,-136);PK.arm(c,SKB,[-64,-284+by],[-104,-170],{bend:1,w:[16,13,10],cap:1});
    PK.arm(c,SKB,[64,-284+by],PK.L2([96,-196],[110,-292],bless),{bend:-1,w:[16,13,10],cap:1,hand:'abhaya',ang:PK.lerp(.5,.12,bless)})}
  c.restore()}

/* ---------- Shesha: olive-khaki serpent coiled into a nest, five real snake heads rising behind Vishnu ---------- */
const SN={base:'#a39a6c',mid:'#8a8158',dark:'#5c553a',ink:'#3e3a28',light:'#cfc496',belly:'#e0d6aa'};
function snakeTube(c,pts,w0,w1){ // thick tube along a polyline of points with outline, body, highlight and belly ticks
  const n=pts.length;const W=k=>lerp(w0,w1,k/(n-1));
  const pass=(col,wm,off)=>{c.strokeStyle=col;c.lineCap='round';c.lineJoin='round';for(let k=0;k<n-1;k++){const a=pts[k],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;c.lineWidth=W(k)*wm;c.beginPath();c.moveTo(a[0]+nx*off*W(k),a[1]+ny*off*W(k));c.lineTo(b[0]+nx*off*W(k+1),b[1]+ny*off*W(k+1));c.stroke()}};
  pass(SN.ink,1.1,0);pass(SN.base,1,0);pass(SN.mid,.55,.22);pass(SN.light,.34,-.22);
  c.strokeStyle='rgba(60,54,34,.42)';c.lineWidth=2;for(let k=1;k<n-1;k+=1){const a=pts[k-1],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d,w=W(k)*.46;c.beginPath();c.moveTo(pts[k][0]+nx*w,pts[k][1]+ny*w);c.lineTo(pts[k][0]-nx*w,pts[k][1]-ny*w);c.stroke()}}
function ellPts(cx,cy,rx,ry,a0,a1,N){const p=[];for(let k=0;k<=N;k++){const a=lerp(a0,a1,k/N);p.push([cx+Math.cos(a)*rx,cy+Math.sin(a)*ry])}return p}
function snakeHead(c,x,y,dir,s,t,open){c.save();c.translate(x,y);c.scale(dir*s,s);const g=c.createLinearGradient(0,-34,0,26);g.addColorStop(0,SN.light);g.addColorStop(.55,SN.base);g.addColorStop(1,SN.mid);
  const gap=3+open*7;
  // tongue
  const tg=Math.sin(t*5)*3;c.strokeStyle='#c02a3a';c.lineWidth=3.2;c.lineCap='round';c.beginPath();c.moveTo(66,6+gap*.4);c.lineTo(104,8+gap*.4+tg);c.moveTo(104,8+gap*.4+tg);c.lineTo(118,1+gap*.4+tg);c.moveTo(104,8+gap*.4+tg);c.lineTo(118,16+gap*.4+tg);c.stroke();
  // lower jaw (thin, slightly open) and the dark mouth between the jaws
  c.fillStyle='#6a1a28';c.beginPath();c.moveTo(-6,8);c.lineTo(72,4);c.lineTo(66,4+gap);c.lineTo(-6,16);c.closePath();c.fill();
  c.fillStyle=SN.belly;c.strokeStyle=SN.ink;c.lineWidth=3;c.beginPath();c.moveTo(-6,14);c.lineTo(66,4+gap);c.bezierCurveTo(58,16+gap,24,22+gap,-8,22);c.closePath();c.fill();c.stroke();
  // skull
  c.fillStyle=g;c.beginPath();c.moveTo(-46,8);c.bezierCurveTo(-44,-34,-6,-42,24,-32);c.bezierCurveTo(52,-24,72,-14,80,-2);c.bezierCurveTo(76,6,50,6,28,8);c.bezierCurveTo(10,8,-10,14,-46,8);c.closePath();c.fill();c.strokeStyle=SN.ink;c.lineWidth=3.4;c.stroke();
  c.strokeStyle='rgba(60,54,34,.4)';c.lineWidth=2;for(let r=0;r<3;r++)for(let q=0;q<5;q++){c.beginPath();c.arc(-24+q*14+(r%2)*7,-24+r*10,6,.2,Math.PI-.2);c.stroke()}
  c.fillStyle='#f0d860';c.beginPath();c.ellipse(26,-14,6.4,5.4,0,0,7);c.fill();c.fillStyle='#16100a';c.fillRect(25,-19,2.4,10);c.strokeStyle=SN.ink;c.lineWidth=3;c.beginPath();c.moveTo(16,-22);c.quadraticCurveTo(28,-28,40,-18);c.stroke();
  c.fillStyle=SN.ink;c.beginPath();c.arc(70,-7,2.4,0,7);c.fill();c.restore()}
function drawShesha(c,t){c.save();
  // five heads on thick necks, fanned behind where Vishnu lies
  const base=[-150,-170],Hd=[[-345,-362,-1,.9],[-262,-466,-1,1],[-140,-504,1,1.05],[-12,-462,1,1],[70,-372,1,.9]];
  Hd.forEach(([hx,hy,dir,sz],i)=>{const sw=Math.sin(t*1.2+i)*4,bob=Math.sin(t*1.6+i*1.3)*3,ex=hx+sw,ey=hy+bob;
    const pts=[];for(let k=0;k<=16;k++){const u=k/16,x=lerp(base[0],ex-dir*30,u)+Math.sin(u*Math.PI)*(ex-base[0])*.18*(i%2?1:-1)*.5,y=lerp(base[1],ey+36,u)-Math.sin(u*Math.PI)*70;pts.push([x,y])}
    snakeTube(c,pts,56*sz,42*sz);snakeHead(c,ex,ey,dir,sz*1.05,t+i,.3+.5*Math.sin(t*1.5+i))});
  // the coiled nest: back ring (the couch surface), then two front rings
  c.fillStyle=SN.mid;c.beginPath();c.ellipse(-10,-168,290,52,0,0,7);c.fill();
  snakeTube(c,ellPts(-10,-168,290,52,0,Math.PI*2,44),78,78);
  c.fillStyle=SN.base;c.beginPath();c.ellipse(-10,-170,262,38,0,0,7);c.fill();c.fillStyle='rgba(255,240,180,.12)';c.beginPath();c.ellipse(-60,-182,170,14,-.05,0,7);c.fill();
  snakeTube(c,ellPts(10,-104,345,62,0,Math.PI,40),96,96);
  snakeTube(c,ellPts(-6,-46,395,66,.05,Math.PI-.05,40),104,104);
  // tail tip curling out at the right
  const tail=[];for(let k=0;k<=14;k++){const u=k/14;tail.push([380+u*130,-46+Math.sin(u*3.4)*30-u*22])}snakeTube(c,tail,70,10);
  c.restore()}

/* ---------- Vishnu in yoganidra on Shesha: hand-posed (NOT a rotated standing rig) ----------
   Torso leans back at ~22 deg, near knee raised with the forearm resting on it, far leg extended, two raised upper hands. */
function drawReclineVishnu(c,o){const t=o.t||0,S=CAST.vishnu,br=Math.sin(t*1.2)*1.4,L=S.lower;c.save();
  drawShesha(c,t);
  const N=[-196,-330+br],TL=205,d=[.375,.927],nn=[-.927,.375],P=(u,v)=>[N[0]+d[0]*TL*u+nn[0]*v,N[1]+d[1]*TL*u+nn[1]*v];
  const skin=S.skin,ad=(a,b)=>[a[0]+b[0],a[1]+b[1]];
  const lim=(a,b,wa,wb)=>{tapered(c,a,b,wa,wb,skin);c.globalAlpha=.38;const dx=b[0]-a[0],dy=b[1]-a[1],dd=Math.hypot(dx,dy)||1,nx=-dy/dd,ny=dx/dd;tapered(c,[a[0]+nx*wa*.5,a[1]+ny*wa*.5],[b[0]+nx*wb*.5,b[1]+ny*wb*.5],wa*.5,wb*.5,S.skinD);c.globalAlpha=.22;tapered(c,[a[0]-nx*wa*.4,a[1]-ny*wa*.4],[b[0]-nx*wb*.4,b[1]-ny*wb*.4],wa*.3,wb*.3,S.skinH);c.globalAlpha=1};
  const cloth=(a,b,wa,wb)=>{const g=c.createLinearGradient(a[0],a[1]-40,a[0],a[1]+40);g.addColorStop(0,L.colL);g.addColorStop(1,L.colD);tapered(c,a,b,wa,wb,g);c.strokeStyle='rgba(120,70,0,.4)';c.lineWidth=2;const dx=b[0]-a[0],dy=b[1]-a[1],dd=Math.hypot(dx,dy)||1,nx=-dy/dd,ny=dx/dd;[-.6,-.2,.2,.6].forEach(f=>{c.beginPath();c.moveTo(a[0]+nx*wa*f,a[1]+ny*wa*f);c.lineTo(b[0]+nx*wb*f,b[1]+ny*wb*f);c.stroke()})};
  const foot=(p,ang)=>{c.save();c.translate(p[0],p[1]);c.rotate(ang);c.fillStyle=S.skinM;c.beginPath();c.ellipse(10,0,26,11,0,0,7);c.fill();c.fillStyle=skin;[0,1,2,3,4].forEach(k=>{c.beginPath();c.ellipse(32,-6+k*3.4,4.2,2.8,0,0,7);c.fill()});c.fillStyle='rgba(15,20,70,.3)';c.beginPath();c.ellipse(8,4,20,5,0,0,7);c.fill();c.restore()};
  const PV=P(1,0),Ls=P(.1,60),Rs=P(.1,-60);
  // --- raised upper hands (behind the body): chakra on the left, conch on the right
  const raise=(sh,sd2,hand)=>{const el=ad(sh,[sd2*40,-66]),hd=ad(sh,[sd2*36,-146]);lim(sh,el,15,12);lim(el,hd,12,9);armband(c,{s:sh,e:el,t:hd},13,S.armlet);handS(c,S,hd,false);return hd};
  const hL=raise(Ls,-1),hR=raise(Rs,1);
  c.save();c.translate(hL[0],hL[1]-26);glow2(c,0,0,44,'255,225,120',.5);c.rotate(t*2.2);c.strokeStyle='#f6d870';c.lineWidth=5;c.beginPath();c.arc(0,0,23,0,7);c.stroke();c.lineWidth=2;for(let k=0;k<8;k++){const a=k*.785;c.beginPath();c.moveTo(0,0);c.lineTo(Math.cos(a)*23,Math.sin(a)*23);c.stroke()}c.restore();
  c.save();c.translate(hR[0]+2,hR[1]-22);c.rotate(.2);const cg=c.createLinearGradient(-12,0,12,0);cg.addColorStop(0,'#fffaf0');cg.addColorStop(1,'#cfc3a2');c.fillStyle=cg;c.beginPath();c.moveTo(0,22);c.bezierCurveTo(-21,6,-17,-26,0,-32);c.bezierCurveTo(17,-26,21,6,0,22);c.fill();c.restore();
  // --- far leg: extended along the coil
  const KF=ad(PV,[122,10]),AF=ad(PV,[236,-8]);lim(KF,AF,22,13);foot(ad(AF,[4,-8]),-.28);lim(ad(PV,[6,12]),KF,32,24);cloth(ad(PV,[6,12]),ad(KF,[-6,0]),36,30);
  // --- torso
  const half=[[0,34],[.1,64],[.4,52],[.7,42],[1,50]],up=half.map(([u,w])=>P(u,-w)),lo=half.map(([u,w])=>P(u,w));
  const tg=c.createLinearGradient(P(.5,-56)[0],P(.5,-56)[1],P(.5,56)[0],P(.5,56)[1]);tg.addColorStop(0,S.skinD);tg.addColorStop(.35,skin);tg.addColorStop(.7,skin);tg.addColorStop(1,S.skinH);c.fillStyle=tg;
  c.beginPath();c.moveTo(up[0][0],up[0][1]);for(let k=1;k<up.length;k++){const m=[(up[k-1][0]+up[k][0])/2,(up[k-1][1]+up[k][1])/2];c.quadraticCurveTo(up[k-1][0],up[k-1][1],m[0],m[1])}c.lineTo(up[up.length-1][0],up[up.length-1][1]);c.lineTo(lo[lo.length-1][0],lo[lo.length-1][1]);for(let k=lo.length-2;k>=0;k--){const m=[(lo[k+1][0]+lo[k][0])/2,(lo[k+1][1]+lo[k][1])/2];c.quadraticCurveTo(lo[k+1][0],lo[k+1][1],m[0],m[1])}c.closePath();c.fill();c.strokeStyle=INKC;c.lineWidth=2.6;c.lineJoin='round';c.stroke();
  c.strokeStyle='rgba(15,20,70,.3)';c.lineWidth=2.2;c.lineCap='round';[[.16,-.03],[.16,.03]].forEach(([u,sgn],i)=>{const a=P(u,sgn>0?8:-8),b=P(u+.17,sgn>0?34:-34);c.beginPath();c.moveTo(a[0],a[1]);c.quadraticCurveTo(P(u+.1,sgn>0?8:-8)[0],P(u+.1,sgn>0?8:-8)[1],b[0],b[1]);c.stroke()});
  c.beginPath();const a0=P(.16,0),a1=P(.72,0);c.moveTo(a0[0],a0[1]);c.lineTo(a1[0],a1[1]);c.stroke();[.32,.44,.56].forEach(u=>{const a=P(u,-14),b=P(u,14);c.beginPath();c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.stroke()});
  // red uttariya from the left shoulder, draping down onto the coil; plus a sash across the chest
  c.fillStyle='#c4283a';c.beginPath();const u0=P(.06,66),u1=P(.5,70);c.moveTo(u0[0]+10,u0[1]-10);c.bezierCurveTo(u0[0]-26,u0[1]+40,u1[0]-46,u1[1]+30,u1[0]-70,u1[1]+104);c.lineTo(u1[0]-24,u1[1]+112);c.bezierCurveTo(u1[0]-6,u1[1]+50,u0[0]+34,u0[1]+30,u0[0]+44,u0[1]);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.2)';c.lineWidth=2;c.beginPath();c.moveTo(u0[0]+16,u0[1]);c.bezierCurveTo(u0[0]-10,u0[1]+50,u1[0]-30,u1[1]+40,u1[0]-48,u1[1]+104);c.stroke();
  c.strokeStyle='#c4283a';c.lineWidth=15;c.lineCap='butt';const s0=P(.08,52),s1=P(.9,-30);c.beginPath();c.moveTo(s0[0],s0[1]);c.quadraticCurveTo(P(.5,40)[0],P(.5,40)[1],s1[0],s1[1]);c.stroke();
  // garland + Kaustubha
  for(let k=0;k<15;k++){const u=k/14,q=[P(.08+u*.1,-44+u*0)[0],0];const a=P(.06,-44),b=P(.34,0),e=P(.06,44),pt=[(1-u)*(1-u)*a[0]+2*(1-u)*u*b[0]+u*u*e[0],(1-u)*(1-u)*a[1]+2*(1-u)*u*b[1]+u*u*e[1]];c.fillStyle=k%2?'#f08ab0':'#ffd0e0';c.beginPath();c.arc(pt[0],pt[1],5,0,7);c.fill()}
  const kg=P(.3,0);glow2(c,kg[0],kg[1],16,'255,70,60',.8);c.fillStyle='#e0302a';c.beginPath();c.arc(kg[0],kg[1],6,0,7);c.fill();
  // waist band + dhoti top
  c.fillStyle=L.trim;c.beginPath();const w0=P(.94,-52),w1=P(.94,52),w2=P(1.1,52),w3=P(1.1,-52);c.moveTo(w0[0],w0[1]);c.lineTo(w1[0],w1[1]);c.lineTo(w2[0],w2[1]);c.lineTo(w3[0],w3[1]);c.closePath();c.fill();
  // --- near leg: knee raised, bare calf, foot on the coil, dhoti over the thigh
  const HN=ad(PV,[-10,6]),KN=ad(PV,[122,-84]),AN=ad(PV,[178,18]);lim(KN,AN,26,14);foot(ad(AN,[8,4]),.12);lim(HN,KN,38,30);cloth(HN,ad(KN,[4,-2]),42,34);c.fillStyle=L.trim;c.beginPath();c.ellipse(KN[0]+2,KN[1]+4,36,10,-.5,0,7);c.fill();
  // --- lower arms: left relaxed on the coil, right forearm resting on the knee
  const Le=ad(Ls,[-34,62]),Lh=ad(Ls,[-52,128]);lim(Ls,Le,17,14);lim(Le,Lh,14,11);armband(c,{s:Ls,e:Le,t:Lh},13,S.armlet);handS(c,S,Lh,false,-.2);
  const Re=ad(Rs,[56,64]),Rh=ad(KN,[-6,-16]);lim(Rs,Re,17,14);lim(Re,Rh,14,11);armband(c,{s:Rs,e:Re,t:Rh},13,S.armlet);handS(c,S,Rh,false,.5);
  [Ls,Rs].forEach((sp,i)=>{c.fillStyle=skin;c.beginPath();c.arc(sp[0],sp[1],19,0,7);c.fill();c.fillStyle='rgba(255,255,255,.14)';c.beginPath();c.arc(sp[0]+(i?-4:4),sp[1]-5,10,0,7);c.fill()});
  // --- neck + head, gently tilted, crown on
  c.fillStyle=S.skinM;c.beginPath();c.roundRect(N[0]-15,N[1]-48,30,56,8);c.fill();
  c.save();c.translate(N[0]-6,N[1]-66);c.rotate(-.22);c.scale(1.12,1.12);drawHead(c,0,0,{expr:'closed',k:0,S:S,t:t});hairFront(c,S,0,0);headgear(c,S,0,0);c.restore();
  c.restore()}

/* ---------- Ardhanarishwara: Shiva (right half) joined to Adishakti (left half) ---------- */
function drawArdha(c,o){const t=o.t||0;c.save();c.beginPath();c.rect(0,-900,600,1000);c.clip();drawShiva(c,{P:POSES.calm,t:t,rage:false,k:0,pose:'calm'});c.restore();
  c.save();c.beginPath();c.rect(-600,-900,600,1000);c.clip();drawHuman(c,Object.assign({},CAST.adishakti,{build:1.0}),Object.assign(poseOf('stand'),{}),{t:t,expr:'calm'});c.restore()}

function drawHarihara(c,o){const t=o.t||0;c.save();c.beginPath();c.rect(0,-900,600,1000);c.clip();drawShiva(c,{P:POSES.calm,t:t,rage:false,k:0,pose:'calm'});c.restore();
  c.save();c.beginPath();c.rect(-600,-900,600,1000);c.clip();drawHuman(c,Object.assign({},CAST.vishnu,{arms4:false}),poseOf('stand','vishnu'),{t:t,expr:'calm'});c.restore()}
function halfHead(c,leftFn,rightFn){c.save();c.beginPath();c.rect(0,-400,400,800);c.clip();rightFn();c.restore();c.save();c.beginPath();c.rect(-400,-400,400,800);c.clip();leftFn();c.restore()}


/* ---------- engine glue ---------- */
const V2NAMES=new Set(['narada','kumara','jaya','vijaya','villager','villager_w','prasuti','sati','diti','danu','asikli','kashyapa','indra','surya','chandra','agni','vayu','hiranyaksha','hiranyakashipu','ravana','harihara','shiva','vishnu','hayagriva','daksha','manu','adishakti','brahmi','madhu','kaitabha','ardha','brahma','vishnu_rest',...[0,1,2,3,4,5,6].map(i=>'rishi'+i)]);
const SCALE={shiva:.62,kumara:.5,default:.62};
const shivaPose=(p)=>{const r=shivaPose0(p);if(r.pointL==null)r.pointL=false;return r};
const shivaPose0=(p)=>{if(p&&typeof p==='object'){const q=JSON.parse(JSON.stringify(p));if(!q.tri)q.tri=Object.assign({},POSES.calm.tri);return q}
  if(p==='point')return Object.assign(JSON.parse(JSON.stringify(POSES.calm)),{hL:[-182,-412],pointL:true});
  if(p==='rpoint')return Object.assign(JSON.parse(JSON.stringify(POSES.rage)),{hL:[-196,-440],pointL:true});
  return JSON.parse(JSON.stringify(p==='rage'||p==='lunge'?POSES.rage:(PZ[p]&&p!=='stand'&&p!=='calm'?Object.assign({},POSES.calm,PZ[p]):POSES.calm)))};
function v2fig(who,x,y,s,t,o){
  const sc=SCALE[who]||SCALE.default,FR=clamp(o.res||s*SC_,1.4,3.9),RG=[-260,-560,520,620];
  if(who==='vishnu_rest'){glow(x-70*sc*s,y-330*sc*s,420*sc*s,'255,205,100',.30);glow(x-70*sc*s,y-330*sc*s,230*sc*s,'255,232,160',.26)}
  const c=figBegin(FR,OY,RG);PK.setDPR(FR);if(o.flip<0)c.scale(-1,1);c.scale(sc,sc);
  const ex=o.expr||{},kk=o.k!=null?o.k:(ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0),face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(who==='shiva'){const P=shivaPose(o.pose);drawShiva(c,{P:P,t:t,rage:kk>.5,k:kk,expr:face==='closed'?'closed':undefined,imp:o.imp||0,mood:o.mood,tilt:o.tilt})}
  else if(who==='brahma'){const P=poseOf(o.pose||'stand','brahma'),sit=P.sit||(o.lotus!==false&&(!o.pose||o.pose==='stand'));drawBrahmaRig(c,{t:t,k:kk,expr:face,hd:o.hd,mood:o.mood,P:sit?(P.sit?P:null):P,lotus:o.lotus,tilt:o.tilt})}
  else if(who==='vishnu_rest')drawReclineVishnu(c,{t:t});
  else if(who==='ardha')drawArdha(c,{t:t});
  else if(who==='harihara')drawHarihara(c,{t:t});
  else drawHuman(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:(CAST[who].kdef||kk),expr:face,prop:o.prop,mood:o.mood,tilt:o.tilt,turn:o.mood&&o.mood.turn!=null?o.mood.turn:undefined});
  figFinish(c,o,x,y,s,FR,OY,RG,.22,.3,true)}
// head close-up: shoulders, chest, garments and jewellery under the head (Opus torso), so heads never float like masks
function bust(c,S,o){const sk=skinPK(S),t=o.t||0,bw=Math.min(S.build||1,1.2);c.save();c.translate(0,-10);
  const sh=[[-122*bw,96],[122*bw,96]];[-1,1].forEach((sd,i)=>{const a=sh[i],b=[sd*156*bw,330];PK.limbOutline(c,a,b,34*bw,28*bw);PK.limb(c,sk,a,b,34*bw,28*bw,{lw:0,sh:0});if(S.armlet)PK.band(c,a,b,.55,30*bw,S.armlet);if(S.female&&S.upper)PK.cut(c,PK.P.caps(a,PK.L2(a,b,.32),36*bw,34*bw),S.upper.col,{lw:1.8,sh:0})});
  c.save();c.translate(0,340);PK.torso(c,sk,262,134*bw,100*bw,0,{fem:!!S.female,muscle:S.muscle});
  const S2=Object.assign({},S);c.scale(1.7,1.7);torsoDress(c,S2,sk,153,72*bw,56*bw,0,t);c.restore();
  if(S.vasuki){const vp=PK.ellPts(0,70,64,30,Math.PI*1.02,-.1,14);for(let i=1;i<=8;i++){const u=i/8;vp.push([64+u*60,70-u*130+Math.sin(u*Math.PI)*10])}PK.tube(c,vp,12,10,VSK,{scales:false,belly:1});PK.hood(c,128,-40,.22+Math.sin(t*1.4)*.1,.68,t,VSK,{ph:2,eye:o.k>.5?'#ff5a3a':'#ffd34a'})}
  PK.cut(c,PK.P.caps([0,88],[0,40],26,23),S.skinM,{lw:2,sh:0});c.restore()}
function v2head(who,x,y,s,t,o){ // close-up of the head with neck, shoulders and garments
  const OYH=1300,FR=clamp(s*SC_,2,3.9),RG=[-300,-330,600,640];const c=figBegin(FR,OYH,RG);PK.setDPR(FR);const ex=o.expr||{},kk=ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0,face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(o.flip<0)c.scale(-1,1);c.scale(1.32,1.32);const M=o.mood,turn=o.tilt?0:.06;
  if(who==='shiva'){const S=CAST.shiva;c.translate(0,-6);c.scale(.86,.86);PK.halo(c,0,-30,112,t,Object.assign({g:.55,n:26},S.halo));c.save();c.scale(1.1,1.1);hairBack(c,S,{hd:[0,0],ph:[0,200]},t);c.restore();bust(c,S,{t:t,k:kk});c.save();c.scale(1.1,1.1);drawHead(c,0,0,{expr:face==='closed'?'closed':'calm',k:kk,S:S,t:t,mood:M,turn:turn});hairFront(c,S,0,0,t);c.restore()}
  else if(who==='brahma'){const S=BRAHMA;PK.halo(c,0,-40,108,t,{g:.5,n:26});bust(c,S,{t:t});
    const side=(x2,tn)=>{c.save();c.translate(x2,12);c.scale(.8,.8);c.filter='brightness(.8)';drawHead(c,0,0,{expr:face,k:kk*.8,S:S,t:t+x2*.01,mood:Object.assign({smile:.2},M&&M.sad?{sad:M.sad*.8}:{}),turn:tn});c.save();c.scale(1-Math.abs(tn)*.3,1);PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);c.restore();c.filter='none';c.restore()};
    side(-62,-.6);side(62,.6);drawHead(c,0,0,{expr:face,k:kk,S:S,t:t,mood:M,turn:turn});PK.hairCap(c,'#e6e0da');PK.jataMukuta(c)}
  else if(who==='ardha'||who==='harihara'){const A=CAST[who==='ardha'?'adishakti':'vishnu'],Sh=CAST.shiva;
    halfHead(c,()=>{bust(c,A,{t:t});if(A.hair&&A.hair.type==='long')hairBack(c,A,{hd:[0,0],ph:[0,200]},t);drawHead(c,0,0,{expr:face,k:0,S:A,t:t});hairFront(c,A,0,0,t);headgear(c,A,0,0)},()=>{bust(c,Sh,{t:t});drawHead(c,0,0,{expr:face==='closed'?'closed':'calm',k:0,S:Sh,t:t});hairFront(c,Sh,0,0,t)})}
  else{const S=CAST[who];if(S.halo)PK.halo(c,0,-34,S.halo.r*.95,t,Object.assign({n:26},S.halo,{g:(S.halo.g==null?.8:S.halo.g)*.7}));if(S.sun)PK.sunDisk(c,0,-30,108,t);
    if(S.headType==='horse'){bust(c,S,{t:t});horseHead(c,0,10,kk,t)}else{
      hairBack(c,S,{hd:[0,0],ph:[0,200]},t);bust(c,S,{t:t,k:kk});drawHead(c,0,0,{expr:face,k:o.k!=null?o.k:(S.kdef||kk),S:S,t:t,mood:M,turn:turn});hairFront(c,S,0,0,t);headgear(c,S,0,0)}}
  figFinish(c,o,x,y,s,FR,OYH,RG,.22,.3,false)}
return {PK:PK,has:w=>V2NAMES.has(w),fig:v2fig,head:v2head,CAST:CAST,poseOf:poseOf,drawHuman:drawHuman,drawBrahmaRig:drawBrahmaRig,drawReclineVishnu:drawReclineVishnu,drawArdha:drawArdha,drawShiva:drawShiva,drawHead:drawHead,drawJata:drawJata,POSES:POSES,mixPose:mixPose,SH:SH};
