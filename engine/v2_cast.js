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

/* ---------- REELS cast (7 vertical reels, Nov 2026): new characters only; EP6 specs above are untouched ---------- */
const FIREHALO={r:104,col:['#fff2a0','#ffb030','#e8501a','#8a1a0a'],rgb:'255,140,60',rgb2:'255,215,150',petal:'rgba(255,215,150,.45)',g:.8};
Object.assign(CAST,{
 // Rudra: Shiva newly born from Brahma's anger (ash-blue skin, jata + crescent, third eye, tiger skin) with a FIRE halo; no Vasuki, no trishul. Also the unit of the eleven Rudras.
 rudra:skinSet('#88a4c4',{skinH:'#c2d6ec',skinD:'#506c90',skinM:'#7492b6',hair:{type:'shiva'},tripundra:true,third:true,brow:'#141020',lower:{type:'tiger',col:'#f09a30',colL:'#ffc060',colD:'#a84a0c',trim:'#5a3a22'},
   neck:['rudraksha'],ashBands:true,armlet:'#e0b04a',bangle:'rudraksha',muscle:.85,halo:FIREHALO,lip:'#7a3a5e',kgem:'#ff7a1a'}),
 // Kamadeva: god of love: parrot-green uttariya, rose dhoti, flower garland, sugarcane bow
 kama:skinSet('#eaa878',{hair:{type:'cap',col:'#16121a'},crown:'raja',mustache:'#2a1a14',lower:L_('#d83a74','#f2c14e','dhoti',{pleat:true,fan:'#f27aa6',dots:'#f2c14e'}),uttariya:'#7cc840',neck:['hara','garland'],armlet:'#e0b040',muscle:.7,kgem:'#e0407a',lip:'#c23a5a',prop:'kamabow'}),
 // Prakriti: Mother Nature: leaf-green sari, gold choli, flower garland, lotus in hand, green-gold halo
 prakriti:skinSet('#e2a878',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:L_('#1f8a44','#f2c14e','sari'),upper:{type:'choli',col:'#f2c14e'},pallu:'#6ac24a',build:.84,neck:['necklace','garland'],armlet:'#e0b04a',bangle:'glass',muscle:0,prop:'lotus2',
   halo:{r:100,col:['#ffffff','#effac8','#7cc858','#2a6a2a'],rgb:'170,230,130',rgb2:'230,250,200',petal:'rgba(240,255,220,.45)',g:.7}}),
 // Swaha: the young goddess who carries the offerings: flame-orange sari, gold choli, small crown, small fire halo
 swaha:skinSet('#f2b88c',{female:true,bindi:true,hair:{type:'long',col:'#16101a'},crown:'small',lower:L_('#e04a1a','#ffd34a','sari'),upper:{type:'choli',col:'#ffd34a'},pallu:'#ff9a2a',build:.8,neck:['necklace'],armlet:'#ffd34a',bangle:'glass',muscle:0,kgem:'#ff7a1a',
   halo:Object.assign({},FIREHALO,{r:84,g:.55})}),
 // Yoga Nidra devi (the sleep that holds Vishnu): indigo skin and sari, silver trim, moon-silver halo
 nidra:skinSet('#7c6cae',{skinH:'#aa9cd8',skinD:'#40326c',skinM:'#6c5c9c',female:true,bindi:true,hair:{type:'long',col:'#0c0814'},crown:'devi',lower:L_('#2c2270','#d8e0f2','sari'),upper:{type:'choli',col:'#d8e0f2'},pallu:'#5a48b0',build:.82,neck:['pearls'],armlet:'#d8e0f2',bangle:'glass',muscle:0,kgem:'#b8a8ff',
   halo:{r:96,col:['#ffffff','#e2deff','#8a7ad0','#2a1e5a'],rgb:'170,160,255',rgb2:'225,220,255',petal:'rgba(240,236,255,.45)',g:.6}}),
 // the young woman at the river (Reel 4), later Narada's wife: rose sari, marigold choli
 kanya:skinSet('#ecb48a',{female:true,bindi:true,hair:{type:'long',col:'#16101a'},lower:L_('#d8406e','#f2c14e','sari'),upper:{type:'choli',col:'#f6b030'},pallu:'#f070a0',build:.8,neck:['necklace'],bangle:'glass',muscle:0}),
 // children (Narada's children / grandchildren): big head, small body
 balak:skinSet('#e2a878',{hair:{type:'topknot',col:'#16121a'},lower:L_('#f4eedc','#e07a2a','short',{len:.25,fan:'#f6c070'}),sash:'#e07a2a',neck:['tulsi'],tilak:'dot',muscle:0,build:.8,hs:1.36}),
 balika:skinSet('#eab08a',{female:true,bindi:true,hair:{type:'long',col:'#16121a'},lower:L_('#2a9a6a','#f2c14e','sari'),upper:{type:'choli',col:'#f2a03a'},pallu:'#f6d860',build:.78,neck:['necklace'],bangle:'glass',muscle:0,hs:1.32}),
 // the starving gods (Reel 6): thin, faded cloth; plus a thin Indra (same crown + vajra)
 deva_thin:skinSet('#d8b088',{hair:{type:'cap',col:'#1c1820'},crown:'small',lower:L_('#c8b47a','#a08040','dhoti',{fan:'#ddd0a0'}),uttariya:'#ece2c8',thread:true,neck:['pearls'],armlet:'#c8a050',muscle:0,build:.76,kgem:'#c8a050'}),
 deva_thin2:skinSet('#cfa27a',{hair:{type:'cap',col:'#1c1820'},crown:'small',mustache:'#2a2228',lower:L_('#8a9ec0','#c8a050','dhoti',{fan:'#b4c4dc'}),uttariya:'#e4e8f0',thread:true,neck:['pearls'],armlet:'#c8a050',muscle:0,build:.76,kgem:'#8a9ec0'}),
 indra_thin:Object.assign({},CAST.indra,{build:.8,muscle:0,halo:Object.assign({},CAST.indra.halo,{g:.25})}),
 // Daksha's sons: Haryashvas (green-gold princes) and Shavalashvas (spotted violet princes); crowd units
 haryashva:skinSet('#d8a070',{hair:{type:'cap',col:'#1a141c'},crown:'small',lower:L_('#2f9a5a','#f2c14e','dhoti',{pleat:true,fan:'#5ac07a'}),uttariya:'#f2c14e',thread:true,neck:['hara'],armlet:'#e0b040',muscle:.55,build:.94,kgem:'#18a57a'}),
 shavalashva:skinSet('#c89060',{hair:{type:'cap',col:'#1a141c'},crown:'small',lower:L_('#7a4ab0','#f2c14e','dhoti',{pleat:true,fan:'#a07ad8',dots:'#f6f0e0'}),uttariya:'#f6f0e0',thread:true,neck:['hara'],armlet:'#e0b040',muscle:.55,build:.94,kgem:'#7a4ab0'}),
 // Narada as a householder (no veena) and as an old grandfather (white jata + beard)
 narada_g:Object.assign({},CAST.narada,{prop:null,uttariya:'#f6d860'}),
 narada_old:Object.assign({},CAST.narada,{prop:null,skin:'#dca474',skinM:shade('#dca474',.86),skinD:shade('#dca474',.6),skinH:shade('#dca474',1.3),hair:{type:'jata',col:'#ece8e2',small:true},beard:'#ece8e2',beardLen:30,mustache:'#ece8e2',brow:'#9a9490',build:.88})
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
PZ.run={...PZ.flee};  // reels: running (humans = flee stride; animals cow/mare/duck/doe gallop)
// reels 15/09/10: Garuda (wing / flap ride on the pose and can be blended with acts), Indra, Bhasmasura, Mohini, Diti
PZ.carry={hL:[-46,-302],hR:[46,-302],wing:.3};                       // both hands hold the Amrut pot at the chest (prop:'amrut')
PZ.fly={hL:[-46,-302],hR:[46,-302],kL:[-46,-150],kR:[46,-150],fL:[-58,-70],fR:[58,-70],hem:120,wing:1,flap:1};   // flying, wings beating, legs tucked
PZ.glide={hL:[-128,-312],hR:[128,-312],kL:[-40,-140],kR:[40,-140],fL:[-50,-56],fR:[50,-56],hem:120,wing:1,flap:.25};
PZ.spread={hL:[-176,-392],hR:[176,-392],wing:1};                      // power pose: arms and wings wide
PZ.sneak={ph:[0,-212],ch:[0,-338],nk:[0,-378],hd:[0,-428],sL:[-64,-352],sR:[64,-352],hipL:[-24,-208],hipR:[24,-208],kL:[-66,-108],kR:[62,-104],fL:[-84,0],fR:[76,0],hL:[-58,-236],hR:[118,-262],lean:.2,sway:0};  // creeping forward, weapon low
PZ.throw={...PZ.lunge,hR:[112,-566],hL:[-140,-360],grip:1};          // weapon raised to throw (Indra + vajra)
PZ.headtouch={hR:[26,-530],hL:[-132,-322],hRt:'rest',hRa:-1.75};                          // hand on top of one's own head (Mohini's trick)
PZ.dance={ph:[14,-262],ch:[-4,-388],nk:[-10,-428],hd:[-16,-476],sL:[-68,-398],sR:[60,-406],hL:[-150,-470],hR:[124,-322],hipL:[-10,-258],hipR:[38,-258],kL:[-24,-130],kR:[50,-128],fL:[-36,0],fR:[30,-22],sway:2};
PZ.dance2={ph:[-14,-262],ch:[4,-388],nk:[10,-428],hd:[16,-476],sL:[-60,-406],sR:[68,-398],hL:[-124,-322],hR:[150,-470],hipL:[-38,-258],hipR:[10,-258],kL:[-50,-128],kR:[24,-130],fL:[-30,-22],fR:[36,0],sway:-2};
PZ.selfcut={...PZ.sit,hR:[44,-236],grip:1,gripA:-1.5708};             // seated ascetic, sword held level at his own neck (no blood)
PZ.sleep={hL:[-62,-300],hR:[26,-290],kL:[-18,-130],kR:[74,-146],fL:[-24,0],fR:[22,-22],hem:200,sway:0,lieDown:1};   // lying on her back (rig is laid on the ground)
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
  else{PK.hairCap(c,H.col);if(H.type==='topknot'){PK.cut(c,PK.P.ell(0,-62,17,17),PK.lg(c,-17,0,17,0,[PK.shade(H.col,H.bunHi||1.5),H.col]),{lw:2,sh:0});PK.cut(c,cc=>cc.roundRect(-11,-49,22,6,2),PK.goldG(c,-11,11),{lw:1.2,sh:0})}}
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
  if(S.hairFlower)hairFlowers(c,S.hairFlower);
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
  const shin=(g,sd)=>{const sl=S.legSk||sk;PK.limbOutline(c,g.k,[g.f[0],g.f[1]-14],21*bw,12*bw);PK.limb(c,sl,g.k,[g.f[0],g.f[1]-14],21*bw,12*bw,{lw:0,sh:0});if(S.talons){legScales(c,g.k,[g.f[0],g.f[1]-14]);talonFoot(c,sl,g.f[0],g.f[1]-4,sd,t)}else PK.footF(c,sk,g.f[0],g.f[1]-4,sd,{anklet:S.anklet||(S.female||S.halo||S.crown?GOLD:false),alta:S.female||!!S.halo});if(S.claws)footClaws(c,g.f[0],g.f[1]-4,sd);if(S.dust)footDust(c,g.f[0],g.f[1]-4,sd)};
  const thigh=(g)=>{PK.limbOutline(c,g.h,g.k,29*bw,22*bw);PK.limb(c,sk,g.h,g.k,29*bw,22*bw,{lw:0,sh:0})};
  const clothTube=(a,b,ra,rb)=>{const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;PK.cut(c,PK.P.caps(a,b,ra,rb),PK.lg(c,a[0]+nx*ra,a[1]+ny*ra,a[0]-nx*ra,a[1]-ny*ra,[L.colL,L.col,L.colD]),{lw:2.2,sh:0});
    [-.45,0,.45].forEach(f=>PK.stroke(c,cc=>{cc.moveTo(a[0]+nx*ra*f,a[1]+ny*ra*f);cc.quadraticCurveTo((a[0]+b[0])/2+nx*ra*(f+.15),(a[1]+b[1])/2+ny*ra*(f+.15),b[0]+nx*rb*f,b[1]+ny*rb*f)},'rgba(40,10,20,.2)',1.4))};
  const hemBand=(a,b,rb)=>{const an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.save();c.translate(b[0],b[1]);c.rotate(an);PK.cut(c,cc=>cc.roundRect(-9,-rb-1,10,2*rb+2,3),L.trim,{lw:1.4,sh:0});if(L.dots)for(let k=-1;k<=1;k++)PK.cut(c,PK.P.ell(-15,k*rb*.55,2.2,2.2),L.dots,{sh:0,lw:.6});c.restore()};
  if(P.kneel){ // EP07 kneeling (both knees down, front view): folded cloth from the waist to the knees, soles tucked behind
    const kx=44*bw,gy=-4,lc=ty==='tiger'?{colL:'#ffc060',col:'#f09a30',colD:'#a84a0c',trim:'#5a3a22'}:L;
    [-1,1].forEach(sd=>{c.save();c.translate(sd*(kx+20),gy-8);c.scale(sd,1);PK.cut(c,cc=>{cc.moveTo(-8,-6);cc.quadraticCurveTo(14,-14,22,-2);cc.quadraticCurveTo(10,6,-8,4);cc.closePath()},PK.lg(c,0,-14,0,6,[sk.h,sk.b,sk.d]),{lw:1.6,sh:0});c.restore()});
    const kp=[[-topW,wy],[topW,wy],[topW+16,wy+(gy-wy)*.45],[kx+34,gy-26],[kx+28,gy],[0,gy-6],[-kx-28,gy],[-kx-34,gy-26],[-topW-16,wy+(gy-wy)*.45]];
    PK.cut(c,PK.P.smooth(kp),PK.lg(c,-kx-34,0,kx+34,0,[lc.colL,lc.col,lc.colD]),{lw:2.2});
    [-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*kx*.62,gy-20,28,18),PK.lg(c,0,gy-38,0,gy,[lc.colL,lc.col]),{lw:1.8,sh:0}));
    c.save();c.beginPath();PK.P.smooth(kp)(c);c.clip();for(let k=-3;k<=3;k++)PK.stroke(c,cc=>{cc.moveTo(k*topW/4,wy+8);cc.quadraticCurveTo(k*topW/3.4+sw*2,(wy+gy)/2,k*kx/2.6,gy-8)},'rgba(30,10,20,.22)',1.5);c.restore();
    PK.stroke(c,cc=>{cc.moveTo(-kx-30,gy-6);cc.quadraticCurveTo(0,gy+2,kx+30,gy-6)},lc.trim,4);return}
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
  c.save();c.translate(W0[0],W0[1]);c.rotate(ta);PK.torso(c,sk,h,tsw,ww,0,{fem:fem,muscle:S.muscle});if(S.underDress)S.underDress(c,S,sk,h,tsw,ww,t,P);torsoDress(c,S,sk,h,tsw,ww,0,t);c.restore();
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
  const sl=fem&&S.upper?S.upper.col:(S.sleeve||null),dL=Math.hypot(P.hL[0]-P.hR[0],P.hL[1]-P.hR[1]),join=dL<60&&!P.sit,joinSit=dL<60&&P.sit;
  const typ=(s,hh,sd)=>{if(join||joinSit)return'pray';if(hh[1]<s[1]-40)return'abhaya';const ext=Math.abs(hh[0]-s[0])>92&&hh[1]<s[1]+50;if(ext)return'ext';if(P.sit)return'jnana';return'rest'};
  const tl=typ(P.sL,P.hL,-1),tr=typ(P.sR,P.hR,1),both=tl==='ext'&&tr==='ext';
  const aL=armX(c,S,sk,P.sL,P.hL,1,{w,sleeve:sl}),aR=armX(c,S,sk,P.sR,P.hR,-1,{w,sleeve:sl});
  if(S.wristThread)wristCord(c,aR,w[2],S.wristThread,t);
  const pr=S.prop||o.prop;
  const hand=(a,ty,sd)=>{const dir=Math.atan2(a.t[0]-a.e[0],-(a.t[1]-a.e[1]));
    if(ty==='pray'){PK.hand(c,sk,[a.t[0]-sd*2,a.t[1]+6],sd*-.08,'rest',sd>0?-1:1);return}
    if(ty==='abhaya'){PK.hand(c,sk,a.t,sd*.12,'abhaya');return}
    if(ty==='ext'){if(both||sd<0)PK.hand(c,sk,a.t,dir*.55,'abhaya');else PK.hand(c,sk,a.t,dir,'point');return}
    if(ty==='jnana'){PK.hand(c,sk,a.t,sd*-2.6,'jnana',sd>0?-1:1);return}
    PK.hand(c,sk,a.t,dir,'rest')};
  if(HPROP[pr]&&!S.arms4){const d=Math.atan2(aR.t[0]-aR.e[0],-(aR.t[1]-aR.e[1]));if(P.hLt)PK.hand(c,sk,aL.t,P.hLa||0,P.hLt,-1);else hand(aL,tl,-1);HPROP[pr](c,aR.t,t,o.f||{});PK.hand(c,sk,aR.t,P.hRt?(P.hRa||0):d,P.hRt||'hold');return}
  if(P.hLt){PK.hand(c,sk,aL.t,P.hLa||0,P.hLt,-1);if(P.hRt)PK.hand(c,sk,aR.t,P.hRa||0,P.hRt);else hand(aR,tr,1);return}
  if(P.hRt){hand(aL,tl,-1);PK.hand(c,sk,aR.t,P.hRa||0,P.hRt);return}
  if(P.grip&&(pr==='sword'||pr==='vajra')){const d=P.gripA!=null?P.gripA:Math.atan2(aR.t[0]-aR.e[0],-(aR.t[1]-aR.e[1]));if(pr==='sword')PK.sword(c,aR.t[0],aR.t[1]+4,d,1.1);else PK.vajra(c,aR.t[0],aR.t[1],d,1.05);hand(aL,tl,-1);PK.hand(c,sk,aR.t,d,'hold');return}
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


/* ---------- REELS: hand props, Kapali, five-headed Brahma, Shatarupa animal forms ---------- */
// where drawHuman's IK puts a hand (same maths as armX; side -1 = left hand)
function handAt(S,P0,t,side){const br=Math.sin(t*1.7)*2.2,bw=S.build||1,L=side<0,s=L?[P0.sL[0]*bw,P0.sL[1]+br]:[P0.sR[0]*bw,P0.sR[1]+br],tg=L?[P0.hL[0],P0.hL[1]+br*.6]:[P0.hR[0],P0.hR[1]+br*.6];return PK.ik(s,tg,66,64,L?1:-1).t}
function leanAt(c,P){if(P.lean){c.translate(0,P.ph[1]);c.rotate(P.lean);c.translate(0,-P.ph[1])}}
// Kamadeva's sugarcane bow, held at its middle, flower tips, string on the body side
function kamaBow(c,x,y){c.save();c.translate(x,y);const top=[8,-160],bot=[8,150],cp=[-78,-4],q=(u,i)=>(1-u)*(1-u)*top[i]+2*(1-u)*u*cp[i]+u*u*bot[i];
  PK.stroke(c,cc=>{cc.moveTo(top[0],top[1]);cc.lineTo(bot[0],bot[1])},'#f6d0e0',2.2);
  const arc=cc=>{cc.moveTo(top[0],top[1]);cc.quadraticCurveTo(cp[0],cp[1],bot[0],bot[1])};PK.stroke(c,arc,INKC,13);PK.stroke(c,arc,'#62a436',9);PK.stroke(c,arc,'rgba(200,240,150,.7)',2.4,{dash:[16,6]});
  for(let k=1;k<10;k++){const u=k/10,px=q(u,0),py=q(u,1);PK.stroke(c,cc=>{cc.moveTo(px-7,py);cc.lineTo(px+7,py)},'#2e5a14',2.2)}
  [top,bot].forEach(p=>{for(let i=0;i<5;i++){const a=i*1.2566;PK.cut(c,PK.P.ell(p[0]+Math.cos(a)*7,p[1]+Math.sin(a)*7,6,4.2,a),'#f47aa8',{lw:1,sh:0})}PK.cut(c,PK.P.ell(p[0],p[1],3.4,3.4),'#ffd34a',{lw:.8,sh:0})});
  c.restore()}
// kapala: a stylised ivory skull resting in the palm (no gore)
function kapala(c,x,y,s){c.save();c.translate(x,y-20*s);c.scale(s,s);const ink='#5a4632';
  PK.glow(c,0,-6,46,'255,235,190',.35);
  PK.cut(c,PK.P.smooth([[-24,-4],[-22,-30],[0,-40],[22,-30],[24,-4],[16,10],[12,22],[-12,22],[-16,10]]),PK.lg(c,-24,-40,24,22,['#fffaf0','#efe4c8','#bfae88']),{lw:2,ink:ink});
  [-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*10,-6,6.5,7.5,sd*.2),'#5a4634',{lw:1.2,ink:ink,sh:0}));
  PK.cut(c,PK.P.poly([[0,2],[-3.5,9],[3.5,9]]),'#6a5640',{lw:0,sh:0});
  PK.stroke(c,cc=>{cc.moveTo(-9,16);cc.lineTo(9,16)},ink,1.4);for(let k=-2;k<=2;k++)PK.stroke(c,cc=>{cc.moveTo(k*3.6,13);cc.lineTo(k*3.6,19)},ink,1);
  c.restore()}
// Brahma's fifth head as Shiva carries it: serene, eyes closed, crowned, soft golden glow (no blood)
function brahmaHead(c,x,y,t,s){c.save();c.translate(x,y-62*s);c.scale(s,s);PK.glow(c,0,-20,110,'255,220,150',.45);
  drawHead(c,0,0,{expr:'closed',k:0,S:BRAHMA,t:t,mood:{smile:.05,sad:.3}});PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);c.restore()}
// Kapali: Shiva wandering with the skull (default) or Brahma's head (prop:'head') stuck to his LEFT hand
function drawKapali(c,o,t,kk,face){const S=CAST.shiva,P=shivaPose(o.pose);drawHuman(c,S,P,{t:t,k:kk,expr:face==='closed'?'closed':'calm',mood:o.mood,tilt:o.tilt});
  const it=o.prop||'skull';if(it==='none')return;c.save();leanAt(c,P);const h=handAt(S,P,t,-1);if(it==='head')brahmaHead(c,h[0],h[1]+4,t,.74);else kapala(c,h[0],h[1]+2,1.45);c.restore()}
function drawKama(c,o,t,kk,face){const S=CAST.kama,P=poseOf(o.pose,'kama');drawHuman(c,S,P,{t:t,k:o.k!=null?o.k:kk,expr:face,mood:o.mood,tilt:o.tilt,turn:o.mood&&o.mood.turn!=null?o.mood.turn:undefined});
  c.save();leanAt(c,P);const h=handAt(S,P,t,-1);kamaBow(c,h[0]-2,h[1]-4);c.restore()}
// Brahma with the FIFTH head on top (Reel 2): seated or standing; hd:{l,r,b,t} still grows the heads one by one (default: all five)
function topHead(c,x,y,s,t,k,face){c.save();c.translate(x,y);c.scale(s,s);drawHead(c,0,0,{expr:face||'calm',k:k,S:BRAHMA,t:t+.7,mood:{smile:.3,ly:-.2}});PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);c.restore()}
function drawBrahma5(c,o,t,kk,face){const H=o.hd||{l:1,r:1,b:1,t:1},P=poseOf(o.pose||'stand','brahma'),sit=P.sit||(o.lotus!==false&&(!o.pose||o.pose==='stand'));
  drawBrahmaRig(c,{t:t,k:kk,expr:face,hd:H,mood:o.mood,P:sit?(P.sit?P:null):P,lotus:o.lotus,tilt:o.tilt});
  if(!sit){const u=H.t==null?0:H.t,e=u*u*(3-2*u);if(e<.02)return;c.save();leanAt(c,P);c.translate(P.hd[0],P.hd[1]+40);c.rotate(o.tilt||0);topHead(c,0,-168+30*(1-e),.74*e,t,kk,face);c.restore()}}
/* Shatarupa: Brahmi's animal forms (cow, mare, duck, doe), paper-cut, facing right, feet at y=0.  Each wears Brahmi's gold
   necklace with the green gem so the viewer knows it is her.  pose: stand | walk | run | bow (head lowered); mood.blink/lx work. */
const AINK='#4a3424';
function aEye(c,x,y,r,M,t){const bl=Math.min(1,Math.max(M.blink||0,((t*.37)%1)<.03?1:0)),ry=r*(1-bl*.85);
  PK.cut(c,PK.P.ell(x,y,r*1.25,ry),'#fffaf0',{lw:1.6,ink:AINK,sh:0});
  if(bl<.7){c.save();c.beginPath();c.ellipse(x,y,r*1.25,ry,0,0,7);c.clip();const ix=x+r*.2+(M.lx||0)*r*.3;c.fillStyle='#4a2810';c.beginPath();c.arc(ix,y,r*.88,0,7);c.fill();c.fillStyle='#0c0604';c.beginPath();c.arc(ix+r*.08,y,r*.48,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ix-r*.25,y-r*.35,r*.26,0,7);c.fill();c.restore()}
  PK.stroke(c,cc=>{cc.moveTo(x-r*1.35,y+r*.15);cc.quadraticCurveTo(x,y-r*1.45*(1-bl)-r*.2,x+r*1.35,y-r*.05)},AINK,2.6);
  for(let i=0;i<3;i++){const a=x+r*(.25+i*.38),b=y-r*(1.02-i*.12)*(1-bl)-r*.12;PK.stroke(c,cc=>{cc.moveTo(a,b);cc.lineTo(a+r*.38,b-r*.42)},AINK,1.7)}}
function aBand(c,a,m,b){const f=cc=>{cc.moveTo(a[0],a[1]);cc.quadraticCurveTo(m[0],m[1],b[0],b[1])};PK.stroke(c,f,AINK,9);PK.stroke(c,f,'#e6b84a',6);PK.stroke(c,f,'rgba(255,240,180,.8)',1.6,{dash:[4,5]});
  const g=[.25*a[0]+.5*m[0]+.25*b[0],.25*a[1]+.5*m[1]+.25*b[1]];PK.cut(c,PK.P.ell(g[0],g[1]+6,5,6.5),'#e6b84a',{lw:1.2,ink:AINK,sh:0});PK.gem(c,g[0],g[1]+7,3.6,'#18a57a')}
function aLeg(c,x,top,len,w,ang,C,hoof,far,hind){c.save();c.translate(x,top);c.rotate(ang);const col=far?[shade(C.b,.82),shade(C.d,.78)]:[C.h,C.b,C.d];
  const hk=hind?-w*.55:w*.15,kn=hind?.46:.52; // hind legs: hock bends back; fore legs: straight knee
  PK.cut(c,cc=>{cc.moveTo(-w*1.1,-14);cc.quadraticCurveTo(-w*1.25,len*.22,-w*.55+hk,len*kn);cc.quadraticCurveTo(-w*.36,len*.75,-w*.34,len-10);cc.lineTo(w*.34,len-10);cc.quadraticCurveTo(w*.36,len*.75,w*.45+hk,len*kn);cc.quadraticCurveTo(w*1.3,len*.2,w*1.1,-14);cc.closePath()},PK.lg(c,-w,0,w,0,col),{lw:2,ink:AINK,sh:0});
  PK.cut(c,PK.P.ell(hk*.6,len*kn,w*.42,w*.3),'rgba(60,30,10,.12)',{lw:0,sh:0});
  if(hoof)PK.cut(c,cc=>{cc.moveTo(-w*.5,len-12);cc.lineTo(w*.55,len-12);cc.lineTo(w*.72,len);cc.lineTo(-w*.62,len);cc.closePath()},far?shade(hoof,.8):hoof,{lw:1.6,ink:AINK,sh:0});
  c.restore()}
function aMove(o,t){const p=(o.pose&&typeof o.pose==='object')?'walk':(o.pose||'stand'),run=p==='run'?1:(p==='walk'?.5:0),bow=(p==='bow'||p==='graze')?1:0,f=run>.5?7:4;
  return{run:run,bow:bow,bob:Math.sin(t*1.6)*2-(run?Math.abs(Math.sin(t*f))*8*run:0),sw:k=>run?Math.sin(t*f+k)*.42*run:0,M:o.mood||{}}}
function aShadow(c,w){c.fillStyle='rgba(30,16,8,.2)';c.beginPath();c.ellipse(0,2,w,14,0,0,7);c.fill()}
function drawCow(c,o,t){const A=aMove(o,t),b=A.bob,C={b:'#f8f2e6',d:'#d2c2a4',h:'#ffffff'},hoof='#6a5440',body=PK.lg(c,0,-340,0,-190,[C.h,C.b,C.d]);aShadow(c,210);
  aLeg(c,-120,-206+b,206,22,A.sw(0),C,hoof,1,1);aLeg(c,106,-206+b,206,22,A.sw(2),C,hoof,1);aLeg(c,-98,-210+b,210,24,A.sw(1),C,hoof,0,1);aLeg(c,128,-210+b,210,24,A.sw(3),C,hoof,0);
  const tl=cc=>{cc.moveTo(-182,-286+b);cc.quadraticCurveTo(-214,-220+Math.sin(t*2)*6,-200,-128)};PK.stroke(c,tl,AINK,9);PK.stroke(c,tl,C.d,6);PK.cut(c,PK.P.ell(-200,-118,9,20,.1),'#a88a62',{lw:1.6,ink:AINK,sh:0});
  const bp=PK.P.smooth([[-188,-300+b],[-120,-334+b],[0,-326+b],[84,-350+b],[128,-326+b],[162,-282+b],[152,-212+b],[90,-190+b],[0,-196+b],[-120,-188+b],[-182,-214+b],[-200,-262+b]]);
  PK.cut(c,bp,body,{lw:2.4,ink:AINK});c.save();c.beginPath();bp(c);c.clip();c.fillStyle='rgba(226,180,118,.55)';[[-96,-282,48,30],[22,-246,34,22],[-30,-312,26,14]].forEach(([x,y,rx,ry])=>{c.beginPath();c.ellipse(x,y+b,rx,ry,.2,0,7);c.fill()});
    c.fillStyle='rgba(255,255,255,.35)';c.beginPath();c.ellipse(-30,-316+b,120,12,0,0,7);c.fill();c.restore();
  const hy=-300+b+A.bow*80,hx=226-A.bow*10;
  PK.cut(c,PK.P.smooth([[104,-326+b],[170,-338+b],[hx,hy-8],[hx+4,hy+44],[178,-208+b],[150,-182+b],[126,-232+b]]),body,{lw:2.2,ink:AINK});
  aBand(c,[168,-336+b],[204,-270+b+A.bow*30],[178,-226+b+A.bow*20]);
  c.save();c.translate(hx,hy);c.rotate(.32+A.bow*.55);
  const horn=(x0,lean)=>{PK.cut(c,cc=>{cc.moveTo(x0-7,-30);cc.quadraticCurveTo(x0-12+lean,-62,x0+lean*2,-86);cc.quadraticCurveTo(x0+6+lean,-60,x0+7,-30);cc.closePath()},PK.lg(c,0,-86,0,-30,['#fff6e0','#e8dcc0','#b8a888']),{lw:1.8,ink:AINK,sh:0});PK.cut(c,PK.P.ell(x0+lean*2,-84,4.6,6),PK.goldG(c,x0-5,x0+5),{lw:1.2,ink:AINK,sh:0})};
  horn(-20,-6);
  PK.cut(c,cc=>{cc.moveTo(-26,-18);cc.quadraticCurveTo(-60,-30,-82,-10+Math.sin(t*1.3)*3);cc.quadraticCurveTo(-56,4,-24,0);cc.closePath()},PK.lg(c,-80,0,-24,0,[C.d,C.b]),{lw:1.8,ink:AINK,sh:0});
  PK.cut(c,PK.P.smooth([[-36,-32],[10,-42],[50,-22],[80,14],[82,42],[58,54],[20,46],[-14,26],[-38,2]]),PK.lg(c,-36,-42,40,54,[C.h,C.b,C.d]),{lw:2.2,ink:AINK});
  PK.cut(c,PK.P.ell(66,38,22,17,.2),PK.lg(c,50,24,86,56,['#f8d4c4','#e6a898']),{lw:1.8,ink:AINK,sh:0});PK.cut(c,PK.P.ell(76,32,3.6,5.6,.3),'#5a3a2a',{lw:0,sh:0});PK.stroke(c,cc=>{cc.moveTo(52,50);cc.quadraticCurveTo(64,56,78,50)},AINK,1.6);
  aEye(c,16,-6,7.5,A.M,t);PK.cut(c,PK.P.ell(32,-30,3.4,4.4),'#d0243a',{lw:.8,ink:AINK,sh:0});horn(-2,6);
  c.restore()}
function drawMare(c,o,t){const A=aMove(o,t),b=A.bob,C=o.C||{b:'#e8c48a',d:'#b48450',h:'#fae4bc'},MN=o.MN||{b:'#fbf6e8',d:'#d8ccb0',h:'#ffffff'},hoof='#4a3a2a',body=PK.lg(c,0,-335,0,-210,[C.h,C.b,C.d]),mane=PK.lg(c,0,-480,0,-300,[MN.h,MN.b,MN.d]);aShadow(c,210);
  aLeg(c,-124,-222+b,222,17,A.sw(0),C,hoof,1,1);aLeg(c,100,-222+b,222,17,A.sw(2),C,hoof,1);aLeg(c,-102,-226+b,226,19,A.sw(1),C,hoof,0,1);aLeg(c,122,-226+b,226,19,A.sw(3),C,hoof,0);
  const ts=Math.sin(t*1.8)*8+(A.run?14:0);PK.cut(c,cc=>{cc.moveTo(-176,-312+b);cc.bezierCurveTo(-226,-300+b,-232+ts,-220,-246+ts,-112);cc.bezierCurveTo(-226+ts,-150,-210,-230,-172,-282+b);cc.closePath()},mane,{lw:2,ink:AINK,sh:0});
  const bp=PK.P.smooth([[-182,-302+b],[-110,-334+b],[30,-326+b],[118,-326+b],[160,-286+b],[144,-226+b],[60,-212+b],[-60,-216+b],[-160,-222+b],[-198,-264+b]]);
  PK.cut(c,bp,body,{lw:2.4,ink:AINK});c.save();c.beginPath();bp(c);c.clip();c.fillStyle='rgba(255,255,255,.3)';c.beginPath();c.ellipse(-30,-318+b,130,12,0,0,7);c.fill();c.restore();
  const hx=214+A.bow*20,hy=-462+b+A.bow*120;
  PK.cut(c,PK.P.smooth([[86,-318+b],[140,-420+b+A.bow*60],[hx-10,hy-14],[hx+26,hy+10],[196,-380+b+A.bow*70],[170,-264+b],[122,-226+b]]),body,{lw:2.2,ink:AINK});
  {const A0=[hx-4,hy-22],B0=[80,-326+b],dx=B0[0]-A0[0],dy=B0[1]-A0[1],d=Math.hypot(dx,dy),nx=-dy/d,ny=dx/d,pts=[];for(let i=0;i<=8;i++){const u=i/8;pts.push([A0[0]+dx*u-nx*12,A0[1]+dy*u-ny*12])}
    for(let i=8;i>=0;i--){const u=i/8,j=(i%2?40:24)+Math.sin(t*2+i)*3;pts.push([A0[0]+dx*u+nx*j,A0[1]+dy*u+ny*j])}
    PK.cut(c,PK.P.smooth(pts),mane,{lw:1.8,ink:AINK,sh:0});for(let i=1;i<8;i++){const u=i/8;PK.stroke(c,cc=>{cc.moveTo(A0[0]+dx*u-nx*6,A0[1]+dy*u-ny*6);cc.lineTo(A0[0]+dx*u+nx*24,A0[1]+dy*u+ny*24)},'rgba(150,130,90,.45)',1.4)}}
  if(!o.noBand)aBand(c,[150,-404+b+A.bow*60],[176,-350+b+A.bow*70],[196,-372+b+A.bow*70]);
  c.save();c.translate(hx,hy);c.rotate(.98+A.bow*.4);
  PK.cut(c,cc=>{cc.moveTo(-22,-18);cc.lineTo(-14,-62);cc.lineTo(0,-20);cc.closePath()},PK.lg(c,0,-62,0,-18,[C.h,C.d]),{lw:1.8,ink:AINK,sh:0});
  PK.cut(c,PK.P.smooth([[-32,-24],[20,-30],[92,-18],[124,2],[122,24],[92,32],[20,28],[-32,16]]),PK.lg(c,-30,-30,120,30,[C.h,C.b,C.d]),{lw:2.2,ink:AINK});
  PK.cut(c,cc=>{cc.moveTo(30,-30);cc.quadraticCurveTo(80,-26,118,-4);cc.quadraticCurveTo(80,-14,30,-18);cc.closePath()},'rgba(255,250,236,.85)',{lw:0,sh:0});
  PK.cut(c,PK.P.ell(112,8,4,6,.4),'#3a2a1a',{lw:0,sh:0});PK.stroke(c,cc=>{cc.moveTo(98,26);cc.quadraticCurveTo(110,28,120,20)},AINK,1.6);
  PK.cut(c,cc=>{cc.moveTo(-26,-26);cc.quadraticCurveTo(0,-44,24,-26);cc.quadraticCurveTo(10,-10,30,4);cc.quadraticCurveTo(-4,-6,-20,-8);cc.closePath()},mane,{lw:1.6,ink:AINK,sh:0});
  aEye(c,8,-2,7.5,A.M,t);c.restore()}
function drawDoe(c,o,t){const A=aMove(o,t),b=A.bob,C=o.C||{b:'#d0905a',d:'#9a6034',h:'#eab886'},hoof='#3a2a1a',body=PK.lg(c,0,-262,0,-172,[C.h,C.b,C.d]);aShadow(c,160);
  aLeg(c,-104,-182+b,182,12,A.sw(0),C,hoof,1,1);aLeg(c,84,-182+b,182,12,A.sw(2),C,hoof,1);aLeg(c,-86,-186+b,186,13,A.sw(1),C,hoof,0,1);aLeg(c,102,-186+b,186,13,A.sw(3),C,hoof,0);
  PK.cut(c,cc=>{cc.moveTo(-136,-246+b);cc.quadraticCurveTo(-170,-262+b+Math.sin(t*3)*5,-162,-230+b);cc.quadraticCurveTo(-150,-224+b,-132,-232+b);cc.closePath()},'#fbf4e6',{lw:1.6,ink:AINK,sh:0});
  const bp=PK.P.smooth([[-142,-236+b],[-60,-262+b],[40,-258+b],[108,-252+b],[132,-212+b],[100,-180+b],[0,-172+b],[-100,-176+b],[-150,-200+b]]);
  PK.cut(c,bp,body,{lw:2.4,ink:AINK});c.save();c.beginPath();bp(c);c.clip();c.fillStyle='#f6ead4';c.beginPath();c.ellipse(-10,-162+b,140,26,0,0,7);c.fill();
    c.fillStyle='rgba(255,248,232,.92)';for(let r=0;r<3;r++)for(let i=0;i<8;i++){const x=-118+i*30+(r%2)*14,y=-244+r*18+b;if(x<120)c.beginPath(),c.ellipse(x,y,4.6,3.4,0,0,7),c.fill()}c.restore();
  const hx=150+A.bow*16,hy=-350+b+A.bow*120;
  PK.cut(c,PK.P.smooth([[78,-252+b],[112,-318+b+A.bow*60],[hx-6,hy-6],[hx+16,hy+16],[134,-262+b+A.bow*40],[118,-196+b],[96,-190+b]]),body,{lw:2.2,ink:AINK});
  if(!o.noBand)aBand(c,[110,-310+b+A.bow*60],[132,-276+b+A.bow*50],[148,-300+b+A.bow*50]);
  c.save();c.translate(hx,hy);c.rotate(.42+A.bow*.7);
  const ear=(a,l)=>{c.save();c.rotate(a);PK.cut(c,cc=>{cc.moveTo(-4,-10);cc.quadraticCurveTo(-30,-l*.5,-12,-l);cc.quadraticCurveTo(10,-l*.55,8,-8);cc.closePath()},PK.lg(c,-20,0,10,0,[C.d,C.b]),{lw:1.8,ink:AINK,sh:0});
    PK.cut(c,cc=>{cc.moveTo(-2,-14);cc.quadraticCurveTo(-18,-l*.5,-10,-l*.86);cc.quadraticCurveTo(4,-l*.5,4,-14);cc.closePath()},'#f2c8b0',{lw:0,sh:0});c.restore()};
  ear(-.9,50);
  PK.cut(c,PK.P.smooth([[-24,-20],[14,-24],[52,-8],[70,10],[62,22],[30,22],[-6,18],[-26,4]]),PK.lg(c,-24,-24,60,22,[C.h,C.b,C.d]),{lw:2.2,ink:AINK});
  PK.cut(c,PK.P.ell(14,16,22,6),'#f6ead4',{lw:0,sh:0});PK.cut(c,PK.P.ell(66,10,5.4,4.6),'#2a1a12',{lw:1,ink:AINK,sh:0});
  aEye(c,12,-6,8,A.M,t);ear(-.45,56);c.restore()}
function drawDuck(c,o,t){const A=aMove(o,t),b=A.bob*.6,C={b:'#fbf6ea',d:'#d8ccb0',h:'#ffffff'},W=['#fbe6a8','#e8c070','#b88a3a'];aShadow(c,100);
  [[-14,A.sw(0)],[14,A.sw(2)]].forEach(([x,a],i)=>{c.save();c.translate(x,-36+b);c.rotate(a*.6);PK.stroke(c,cc=>{cc.moveTo(0,0);cc.lineTo(0,32)},AINK,7);PK.stroke(c,cc=>{cc.moveTo(0,0);cc.lineTo(0,32)},'#f0902a',4.4);
    PK.cut(c,cc=>{cc.moveTo(-6,32);cc.lineTo(26,34);cc.lineTo(-4,40);cc.closePath()},'#f0902a',{lw:1.4,ink:AINK,sh:0});c.restore()});
  const bp=PK.P.smooth([[-112,-118+b],[-66,-98+b],[0,-104+b],[56,-112+b],[86,-90+b],[74,-48+b],[20,-28+b],[-54,-32+b],[-96,-58+b]]);
  PK.cut(c,bp,PK.lg(c,0,-118,0,-28,[C.h,C.b,C.d]),{lw:2.2,ink:AINK});
  const hx=86,hy=-176+b+A.bow*50;
  PK.cut(c,PK.P.smooth([[38,-104+b],[56,-150+b+A.bow*30],[hx-14,hy+4],[hx+16,hy+6],[92,-138+b+A.bow*30],[84,-92+b]]),PK.lg(c,40,-170,90,-90,[C.h,C.b]),{lw:2,ink:AINK});
  aBand(c,[54,-124+b+A.bow*20],[70,-110+b+A.bow*20],[90,-120+b+A.bow*20]);
  const wp=PK.P.smooth([[-84,-94+b],[-20,-108+b+Math.sin(t*2)*2],[40,-98+b],[30,-66+b],[-30,-56+b],[-86,-72+b]]);PK.cut(c,wp,PK.lg(c,0,-108,0,-56,W),{lw:2,ink:AINK,sh:0});
  c.save();c.beginPath();wp(c);c.clip();for(let i=0;i<6;i++)PK.stroke(c,cc=>cc.arc(-70+i*20,-62+b,12,Math.PI*1.1,Math.PI*1.9),'rgba(120,80,20,.45)',1.6);c.restore();
  c.save();c.translate(hx,hy);c.rotate(A.bow*.5);
  PK.cut(c,PK.P.ell(0,0,27,23),PK.lg(c,-27,-23,27,23,[C.h,C.b,C.d]),{lw:2,ink:AINK});
  PK.cut(c,cc=>{cc.moveTo(18,-8);cc.quadraticCurveTo(44,-10,54,2);cc.quadraticCurveTo(40,12,18,8);cc.closePath()},PK.lg(c,18,-10,54,12,['#ffc060','#f0902a','#c8641a']),{lw:1.6,ink:AINK,sh:0});
  aEye(c,4,-6,5.4,A.M,t);c.restore()}
const ANIMAL={cow:drawCow,mare:drawMare,doe:drawDoe,duck:drawDuck};
const ANIMAL_HEAD={cow:[232,-300,1.3],mare:[244,-440,1.15],doe:[156,-344,1.6],duck:[80,-150,2.0]};
// Hayagriva for the reels: a real paper-cut horse head (front view, white with soft blue shading), gold kirita, vaishnava tilak,
// expressive eyes (anger = red irises + lowered brows), flowing mane behind; body = Vishnu's 4-armed rig.  (EP6 'hayagriva' untouched.)
CAST.hayagriva2=Object.assign({},CAST.hayagriva,{halo:{r:112}});
function horseHead2(c,k,t,M){M=M||{};const ink='#3a3a5a',an=Math.max(k||0,M.anger||0),bl=Math.min(1,Math.max(M.blink||0,((t*.37)%1)<.03?1:0)),sw=Math.sin(t*1.6)*3;
  // mane behind the head, flowing down to the shoulders
  for(let i=-3;i<=3;i++){if(!i)continue;const sd=Math.sign(i),x0=i*9;PK.cut(c,cc=>{cc.moveTo(x0,-70);cc.bezierCurveTo(x0+sd*40+sw,-40,x0+sd*44-sw,40,x0+sd*(30+Math.abs(i)*6),96+Math.abs(i)*6);cc.bezierCurveTo(x0+sd*18,40,x0+sd*12,-20,x0-sd*6,-66);cc.closePath()},PK.lg(c,-60,0,60,0,['#e8ecf8','#fbfcff','#d8deee']),{lw:1.6,ink:ink,sh:0})}
  [-1,1].forEach(sd=>PK.cut(c,cc=>{cc.moveTo(sd*16,-56);cc.quadraticCurveTo(sd*30,-104,sd*42,-112);cc.quadraticCurveTo(sd*46,-80,sd*36,-48);cc.closePath()},PK.lg(c,0,-112,0,-48,['#ffffff','#dfe4f2']),{lw:1.8,ink:ink,sh:0}));
  [-1,1].forEach(sd=>PK.cut(c,cc=>{cc.moveTo(sd*22,-62);cc.quadraticCurveTo(sd*32,-92,sd*38,-100);cc.quadraticCurveTo(sd*38,-78,sd*32,-56);cc.closePath()},'#f2c0c8',{lw:0,sh:0}));
  const hp=PK.P.smooth([[-36,-64],[0,-74],[36,-64],[44,-20],[36,22],[28,64],[24,92],[0,102],[-24,92],[-28,64],[-36,22],[-44,-20]]);
  PK.cut(c,hp,PK.lg(c,-44,0,44,0,['#c8d0e6','#ffffff','#f4f6fc','#b8c0da']),{lw:2.4,ink:ink});
  c.save();c.beginPath();hp(c);c.clip();c.fillStyle='rgba(120,140,200,.16)';c.beginPath();c.ellipse(0,40,16,60,0,0,7);c.fill();c.restore();
  PK.cut(c,PK.P.ell(0,76,25,22),PK.lg(c,0,54,0,98,['#eef0f6','#c8c6d8']),{lw:1.8,ink:ink,sh:0});
  [-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*10,80,4.4,7,sd*.35),'#4a3a4a',{lw:0,sh:0}));PK.stroke(c,cc=>{cc.moveTo(-10,95);cc.quadraticCurveTo(0,99-(M.smile||0)*4+an*3,10,95)},ink,1.6);
  // eyes + brows (anger: red iris, brows lowered toward the centre)
  [-1,1].forEach(sd=>{const ex=sd*27,ey=-14,ry=7*(1-bl*.85);PK.cut(c,PK.P.ell(ex,ey,9,ry,sd*.25),'#fffaf0',{lw:1.6,ink:ink,sh:0});
    if(bl<.7){c.save();c.beginPath();c.ellipse(ex,ey,9,ry,sd*.25,0,7);c.clip();const ix=ex+(M.lx||0)*3-sd*1.5;c.fillStyle=an>.35?'#c81e14':'#3a2414';c.beginPath();c.arc(ix,ey+(M.ly||0)*2,5.6,0,7);c.fill();c.fillStyle='#0c0604';c.beginPath();c.arc(ix,ey,2.8,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ix-1.6,ey-2,1.4,0,7);c.fill();c.restore();if(an>.35)PK.glow(c,ex,ey,14,'255,60,40',.35*an)}
    const bi=ey-12+an*6-(M.sad||0)*-0+(M.surp||0)*-4,bo=ey-14-an*2+(M.sad||0)*4-(M.surp||0)*3;PK.stroke(c,cc=>{cc.moveTo(sd*16,bi);cc.quadraticCurveTo(sd*27,Math.min(bi,bo)-3,sd*38,bo)},ink,2.6+an*1.4)});
  // vaishnava tilak + kirita
  PK.cut(c,cc=>{cc.moveTo(-9,-58);cc.lineTo(-3,-30);cc.lineTo(3,-30);cc.lineTo(9,-58);cc.lineTo(5,-58);cc.lineTo(0,-38);cc.lineTo(-5,-58);cc.closePath()},'#fff6dc',{lw:1,ink:'#a08040',sh:0});PK.cut(c,cc=>cc.roundRect(-1.6,-56,3.2,24,1.5),'#d0243a',{lw:0,sh:0});
  c.save();c.translate(0,-34);c.scale(.9,.9);PK.kirita(c,60);c.restore()}
function drawHayagriva2(c,o,t,kk,face){const S=CAST.hayagriva2,P=poseOf(o.pose,'hayagriva'),br=Math.sin(t*1.7)*2.2;drawHuman(c,S,P,{t:t,k:kk,expr:face,noHead:true});
  c.save();leanAt(c,P);const hx=P.hd[0],hy=P.hd[1]+br;c.translate(hx,hy+40);c.rotate(o.tilt||0);c.scale(1.0,1.0);c.translate(0,-58);horseHead2(c,kk,t,o.mood);c.restore()}
const XFIG={kapali:drawKapali,kama:drawKama,brahma5:drawBrahma5,hayagriva2:drawHayagriva2};

/* ---------- REELS 15 / 09 / 10: Garuda, Vinata, nagas, Vrikasura/Bhasmasura, Mohini, Parvati, pregnant Diti, Marutas ----------
   New specs only; EP6 and reels 1-7 specs are untouched.  Figure keys read from the figure dict (o.f):
   garuda wing:0..1 (folded..spread) flap:0..1 (beat speed), prop:'amrut' (pot in both hands)
   bhasmasura hand:0..1 (glowing boon hand, default 1), ash:0..1 or ashc:<cue>+ashd (turns grey, crumbles top-down into a pile)
   mohini spin:<turns per s> (+ spinc cue to start), any figure in pose 'sleep' lies on a mat (mat:false hides it). */
const GLEG={h:'#ffe48a',b:'#f2b630',d:'#b8761a',m:'#e0a028'};
const STORMHALO={r:84,col:['#ffffff','#dff0ff','#6aa8f0','#24448a'],rgb:'150,200,255',rgb2:'225,240,255',petal:'rgba(235,245,255,.5)',g:.6};
Object.assign(CAST,{
 // Garuda: half bird, half man. Gilded body, white eagle face with golden hooked beak, red/gold wings, crest + small crown, Vaishnava tilak, talons
 garuda:skinSet('#e8a838',{skinH:'#ffd878',skinD:'#a8621a',skinM:'#d8922c',hair:{type:'none'},lower:L_('#c42b3a','#f2c14e','short',{len:.28,fan:'#e8503a',dots:'#f2c14e'}),neck:['hara'],armlet:'#f2c14e',muscle:.95,build:1.1,
   talons:true,legSk:GLEG,underDress:garudaBib,kgem:'#e0234a',brow:'#2a0e08'}),
 // Vinata: Garuda's mother, a slave of the snakes: faded brown sari, plain choli, no jewellery but glass bangles, hair tied back
 vinata:skinSet('#c8905e',{female:true,bindi:true,hair:{type:'long',col:'#2a2024'},lower:L_('#a87a52','#7a5434','sari'),upper:{type:'choli',col:'#8a6a4e'},pallu:'#c4a27a',build:.82,neck:[],bangle:'glass',muscle:0,kgem:'#8a6a4e'}),
 // Parvati: red sari, green choli, small crown, lotus in hand
 parvati:skinSet('#f2c08e',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:L_('#c8102e','#f2c14e','sari'),upper:{type:'choli',col:'#1f8a54'},pallu:'#e02a3a',build:.82,neck:['necklace'],armlet:'#e0b04a',bangle:'glass',muscle:0,kgem:'#18a57a',prop:'lotus2'}),
 // Mohini: Vishnu as an enchantress: Vishnu-blue skin, red sari with Vishnu's yellow pallu, gold choli, flower garland, crown
 mohini:skinSet('#5a8ad8',{skinH:'#90b8f2',skinD:'#2c5098',skinM:'#4a7ac8',female:true,bindi:true,hair:{type:'long',col:'#0c0a18'},crown:'devi',lower:L_('#d8203a','#f2c14e','sari'),upper:{type:'choli',col:'#f2c14e'},pallu:'#f6b81e',build:.8,neck:['necklace','garland'],armlet:'#e6b84a',bangle:'glass',muscle:0,kgem:'#18a57a',lip:'#c23a5a'}),
 // Vrikasura: the asura as Shiva's devotee: dark red-brown skin, small horns, matted jata, ash tripundra, rudraksha, saffron cloth (prop:'sword' when needed)
 vrikasura:skinSet('#6a3e32',{skinH:'#9a6450',skinD:'#3a1e18',skinM:'#5a342a',hair:{type:'jata',col:'#120c10'},horns:'#e8dcc0',beard:'#120c10',beardLen:12,mustache:'#120c10',brow:'#08060c',tilak:'ash',lower:L_('#d8701e','#8a3a12','short',{len:.35,fan:'#f09a40'}),neck:['rudraksha'],bangle:'rudraksha',muscle:.55,build:1.04}),
 // Bhasmasura: the same face after the boon: asura crown + horns, red eyes, ash streaks, black-red cloth, glowing right hand
 bhasmasura:skinSet('#6a3e32',{skinH:'#9a6450',skinD:'#3a1e18',skinM:'#5a342a',hair:{type:'wild',col:'#0c0a10'},horns:'#e8dcc0',crown:'asura',crownCol:'#2a1414',beard:'#0c0a10',beardLen:12,mustache:'#0c0a10',brow:'#08060c',eyeRed:true,tilak:'ash',
   lower:L_('#2a1418','#d8402a','short',{fan:'#5a2028'}),ashBands:true,neck:['rudraksha'],armlet:'#c9a24a',muscle:1,build:1.2,kdef:.3,underDress:ashStreaks}),
 // Diti late in pregnancy: same look as diti, round belly, dusty unwashed feet; pose 'sleep' lays her down
 diti_p:Object.assign({},CAST.diti,{underDress:bellyBump,dust:true}),
 // a grown Maruta (storm god): sky-blue cloth, white wind scarf, fan crest, storm halo
 maruta:skinSet('#e8b478',{hair:{type:'cap',col:'#1a1828'},crown:'vayu',lower:L_('#2f6ac8','#e8f0ff','short',{len:.3,fan:'#7ab0ee',dots:'#e8f0ff'}),uttariya:'#f0f6ff',neck:['pearls'],armlet:'#c8d8f0',muscle:.8,build:.92,kgem:'#7ac8f0',halo:STORMHALO})
});
const BABY=skinSet('#f2c49a',{hair:{type:'cap',col:'#1a1418'},kgem:'#7ac8f0'});
// small helpers used by the rigs above
function legScales(c,a,b){for(let i=1;i<6;i++){const p=PK.L2(a,b,i/6),an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.save();c.translate(p[0],p[1]);c.rotate(an);PK.stroke(c,cc=>{cc.moveTo(-4,-9);cc.quadraticCurveTo(4,0,-4,9)},'rgba(120,60,10,.55)',1.5);c.restore()}}
function talonFoot(c,sk,x,y,sd,t){c.save();c.translate(x,y);c.scale(sd,1);const ink='#3a1a08';
  [[-.25,30],[.35,34],[.9,28]].forEach(([a,L])=>{c.save();c.rotate(a);PK.cut(c,PK.P.caps([0,-6],[0,L-8],8,6),PK.lg(c,-8,0,8,0,[sk.h,sk.b,sk.d]),{lw:1.6,ink:ink,sh:0});
    PK.cut(c,cc=>{cc.moveTo(-5,L-10);cc.quadraticCurveTo(-4,L+6,6,L+10);cc.quadraticCurveTo(1,L+2,5,L-10);cc.closePath()},'#1e1410',{lw:1,ink:ink,sh:0});c.restore()});
  PK.cut(c,PK.P.ell(-10,-10,9,7),PK.lg(c,-18,0,0,0,[sk.b,sk.d]),{lw:1.4,ink:ink,sh:0});PK.cut(c,cc=>{cc.moveTo(-16,-12);cc.quadraticCurveTo(-30,-14,-30,-2);cc.quadraticCurveTo(-24,-8,-14,-6);cc.closePath()},'#1e1410',{lw:1,ink:ink,sh:0});c.restore()}
function footDust(c,x,y,sd){c.save();c.fillStyle='rgba(120,84,50,.55)';for(let i=0;i<9;i++){c.beginPath();c.arc(x+sd*(i*3.2-6),y-2-((i*7)%5)*2.2,1.6+(i%3)*.6,0,7);c.fill()}c.restore()}
function gFeather(c,L,w,cols,ink){PK.cut(c,cc=>{cc.moveTo(0,-w*.45);cc.bezierCurveTo(L*.35,-w*1.0,L*.8,-w*.75,L,0);cc.bezierCurveTo(L*.8,w*.55,L*.35,w*.9,0,w*.45);cc.closePath()},PK.lg(c,0,0,L,0,cols),{lw:1.5,ink:ink||'#5a1a10',sh:0});
  PK.stroke(c,cc=>{cc.moveTo(2,0);cc.quadraticCurveTo(L*.5,-w*.1,L*.9,0)},'rgba(90,30,10,.45)',1.3)}
const GF={p:['#fff4c0','#f2c14e','#c8861a'],s:['#ffc878','#ee7b22','#a8441a'],r:['#ff8a70','#d8283a','#8a1420'],g:['#ffe08a','#f2c14e','#c8861a']};
// one wing, root at the origin, spreading toward +x (sd=-1 mirrors it). open 0 = folded down the back, 1 = spread and raised; flap = extra angle (down-stroke > 0)
function garudaWing(c,sd,open,flap,sc){c.save();c.scale(sd*(sc||1),sc||1);c.rotate(PK.lerp(1.22,-.5,open)+flap);c.scale(PK.lerp(.74,1,open)*.86,.86);
  for(let i=6;i>=0;i--){c.save();c.translate(204-i*7,4+i*4);c.rotate(.04+i*.21);gFeather(c,152-i*7,27,GF.p);c.restore()}
  for(let i=8;i>=0;i--){const u=i/8;c.save();c.translate(18+u*182,PK.lerp(-6,2,u));c.rotate(1.56-u*.4);gFeather(c,PK.lerp(108,138,u),30,GF.s);c.restore()}
  [[62,46,GF.r,0],[34,28,GF.g,-6]].forEach(([L,wd,cols,dy])=>{for(let i=10;i>=0;i--){const u=i/10;c.save();c.translate(8+u*200,dy-4);c.rotate(1.5-u*.32);gFeather(c,L,wd,cols);c.restore()}});
  PK.cut(c,cc=>{cc.moveTo(-12,-16);cc.quadraticCurveTo(110,-42,224,-8);cc.quadraticCurveTo(230,8,214,16);cc.quadraticCurveTo(110,-4,-8,18);cc.closePath()},PK.lg(c,0,-34,0,18,['#ffe08a','#e8a838','#a8621a']),{lw:2,ink:'#5a1a10'});
  for(let i=0;i<8;i++)PK.cut(c,PK.P.ell(14+i*26,-10-Math.sin(i/7*Math.PI)*12,3,3),i%2?'#e0234a':'#fff0b0',{lw:.8,sh:0});c.restore()}
// cream feathered chest under the necklace (torso frame: waist at 0, shoulders at -h)
function garudaBib(c,S,sk,h,sw,ww,t){const bp=PK.P.smooth([[-sw*.66,-h+4],[0,-h+18],[sw*.66,-h+4],[sw*.52,-h*.72],[sw*.2,-h*.5],[0,-h*.44],[-sw*.2,-h*.5],[-sw*.52,-h*.72]]);
  PK.cut(c,bp,PK.lg(c,-sw,0,sw,0,['#fffaf0','#f6ead0','#d8c49a']),{lw:2,sh:0});c.save();c.beginPath();bp(c);c.clip();
  for(let r=0;r<5;r++)for(let i=-4;i<=4;i++)PK.stroke(c,cc=>cc.arc(i*16+(r%2)*8,-h+30+r*16,9,.25,Math.PI-.25),'rgba(170,120,50,.45)',1.4);c.restore()}
// Diti's pregnant belly (sari-wrapped bump); lying down it swells toward the sky
function bellyBump(c,S,sk,h,sw,ww,t,P){const ly=P&&P.lieDown,cx=ly?20:0,rx=ww+(ly?20:12),ry=h*.3,cy=-h*.24;
  PK.cut(c,PK.P.ell(cx,cy,rx,ry),PK.lg(c,cx-rx,0,cx+rx,0,[sk.h,sk.b,sk.d]),{lw:2.2});PK.glow(c,cx,cy,rx*1.1,'255,210,150',.18);
  PK.stroke(c,cc=>cc.ellipse(cx-rx*.3,cy-ry*.35,rx*.35,ry*.25,-.4,Math.PI*1.1,Math.PI*1.6),'rgba(255,255,255,.35)',3)}
// grey-white ash smeared on the arms and torso (Bhasmasura)
function ashStreaks(c,S,sk,h,sw,ww,t){[[-sw*.6,-h*.82,.3],[sw*.55,-h*.78,-.2],[-ww*.5,-h*.3,.15],[ww*.55,-h*.36,-.3]].forEach(([x,y,a])=>{c.save();c.translate(x,y);c.rotate(a);PK.cut(c,cc=>{cc.moveTo(-14,-3);cc.quadraticCurveTo(0,-7,14,-2);cc.quadraticCurveTo(0,4,-14,3);cc.closePath()},'rgba(232,228,236,.75)',{lw:0,sh:0});c.restore()})}

/* ---- Garuda ---- */
function garudaHead(c,k,t,M){M=M||{};const ink='#3a160c',an=Math.max(k||0,M.anger||0),sad=M.sad||0,su=M.surp||0,sm=(M.smile==null?.25:M.smile)*(1-Math.min(1,an+sad)),mo=Math.max(M.mouth||0,su*.6),
  bl=Math.min(1,Math.max(M.blink||0,((t*.37)%1)<.03?1:0)),lx=M.lx||0,ly=M.ly||0;
  // crest of red/gold feathers behind, cheek ruffs at the sides
  for(let i=-3;i<=3;i++){c.save();c.translate(i*9,-34);c.rotate(-Math.PI/2+i*.34+Math.sin(t*1.3+i)*.04);gFeather(c,66-Math.abs(i)*7,22,i%2?GF.g:GF.r);c.restore()}
  [-1,1].forEach(sd=>{for(let j=2;j>=0;j--){c.save();c.translate(sd*30,4+j*13);c.rotate(sd>0?.5+j*.32:Math.PI-.5-j*.32);gFeather(c,44,18,j%2?GF.s:GF.r);c.restore()}});
  const hp=PK.P.smooth([[-34,-30],[-20,-50],[0,-54],[20,-50],[34,-30],[40,-4],[36,22],[22,40],[0,48],[-22,40],[-36,22],[-40,-4]]);
  PK.cut(c,hp,PK.lg(c,-40,0,40,0,['#fffaf0','#fbf2de','#d8c49a']),{lw:2.4,ink:ink});
  c.save();c.beginPath();hp(c);c.clip();for(let r=0;r<3;r++)for(let i=-3;i<=3;i++)if(Math.abs(i)>1)PK.stroke(c,cc=>cc.arc(i*12+(r%2)*6,16+r*11,7,.3,Math.PI-.3),'rgba(170,120,50,.4)',1.3);
  // golden mask around the eyes (raptor look)
  [-1,1].forEach(sd=>PK.cut(c,cc=>{cc.moveTo(sd*30,-8);cc.quadraticCurveTo(sd*40,-4,sd*44,6);cc.quadraticCurveTo(sd*36,4,sd*28,-2);cc.closePath()},'#d8283a',{lw:0,sh:0}));c.restore();
  // vaishnava tilak (Garuda serves Vishnu)
  PK.cut(c,cc=>{cc.moveTo(-7,-44);cc.lineTo(-3,-22);cc.lineTo(3,-22);cc.lineTo(7,-44);cc.lineTo(3.5,-44);cc.lineTo(0,-28);cc.lineTo(-3.5,-44);cc.closePath()},'#fff6dc',{lw:1,ink:'#a08040',sh:0});PK.cut(c,cc=>cc.roundRect(-1.5,-42,3,18,1.5),'#d0243a',{lw:0,sh:0});
  // eyes: big amber raptor eyes (red irises in anger), heavy brows
  [-1,1].forEach(sd=>{const ex=sd*20,ey=-8,ry=10.5*(1+su*.35)*(1-bl*.9);const eye=cc=>{cc.moveTo(ex-sd*13,ey+2);cc.quadraticCurveTo(ex,ey-ry*1.45,ex+sd*14,ey-3);cc.quadraticCurveTo(ex,ey+ry*1.15,ex-sd*13,ey+2);cc.closePath()};
    PK.cut(c,eye,'#fffaf0',{lw:1.8,ink:ink,sh:0});
    if(bl<.8){c.save();c.beginPath();eye(c);c.clip();const ix=ex+lx*4-sd*1,iy=ey-1+ly*2;c.fillStyle=PK.rg(c,ix,iy,0,7,an>.35?[[0,'#ff7a40'],[.55,'#c81e14'],[1,'#3a0404']]:[[0,'#ffe080'],[.6,'#e89a1a'],[1,'#6a3408']]);c.beginPath();c.arc(ix,iy,8,0,7);c.fill();
      c.fillStyle='#0a0404';c.beginPath();c.arc(ix,iy,3.8,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ix-2,iy-2.4,1.6,0,7);c.fill();c.restore();if(an>.35)PK.glow(c,ex,ey,16,'255,60,40',.4*an)}
    const bi=ey-15+an*8-su*5,bo=ey-18-an*3+sad*7-su*4,th=4.5+an*2.6;
    PK.cut(c,cc=>{cc.moveTo(ex-sd*13,bi);cc.quadraticCurveTo(ex,Math.min(bi,bo)-5,ex+sd*17,bo);cc.quadraticCurveTo(ex,Math.min(bi,bo)-5+th,ex-sd*13,bi+th*.7);cc.closePath()},'#2a0e08',{lw:0,sh:0});
    if(sad>.45){PK.cut(c,cc=>{cc.moveTo(ex+sd*4,ey+8);cc.quadraticCurveTo(ex+sd*8,ey+18,ex+sd*4,ey+21);cc.quadraticCurveTo(ex,ey+18,ex+sd*4,ey+8)},'rgba(150,200,255,.85)',{lw:1,ink:'#4a6a9a',sh:0})}});
  // beak: golden hooked beak; the lower beak shows when he speaks / is surprised; gape line curves with the mood
  const gy=20,curve=sm*6-an*4-sad*5;[-1,1].forEach(sd=>PK.stroke(c,cc=>{cc.moveTo(sd*12,gy);cc.quadraticCurveTo(sd*20,gy+2-curve*.4,sd*27,gy-curve)},ink,2.2));
  if(mo>.05){PK.cut(c,cc=>{cc.moveTo(-10,24);cc.quadraticCurveTo(0,30+mo*18,10,24);cc.quadraticCurveTo(0,24+mo*30,-10,24)},'#6a1a20',{lw:1.4,ink:ink,sh:0});PK.cut(c,cc=>{cc.moveTo(-9,28+mo*14);cc.quadraticCurveTo(0,40+mo*26,9,28+mo*14);cc.quadraticCurveTo(0,32+mo*18,-9,28+mo*14)},PK.lg(c,0,28,0,50,['#f2c14e','#b8761a']),{lw:1.4,ink:ink,sh:0})}
  const bk=cc=>{cc.moveTo(-14,-6);cc.bezierCurveTo(-17,12,-9,28,0,46);cc.bezierCurveTo(9,28,17,12,14,-6);cc.quadraticCurveTo(0,-12,-14,-6);cc.closePath()};
  PK.cut(c,bk,PK.lg(c,-16,0,16,0,['#fff0a0','#f2c14e','#b8761a']),{lw:2,ink:ink});PK.stroke(c,cc=>{cc.moveTo(-2,-6);cc.quadraticCurveTo(-4,18,0,40)},'rgba(255,250,220,.75)',2.2);
  [-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*6,4,2.2,1.4,sd*.4),'#5a2a08',{lw:0,sh:0}));
  c.save();c.translate(0,-22);c.scale(.74,.74);PK.kirita(c,54);c.restore()}
function garudaPot(c,S,P,t){c.save();leanAt(c,P);const a=handAt(S,P,t,-1),b=handAt(S,P,t,1);amrutPot(c,(a[0]+b[0])/2,(a[1]+b[1])/2+14,.6,t);c.restore()}
function drawGaruda(c,o,t,kk,face){const S=CAST.garuda,P=poseOf(o.pose,'garuda'),f=o.f||{},bw=S.build,br=Math.sin(t*1.7)*2.2;
  const wing=f.wing!=null?f.wing:(P.wing!=null?P.wing:.3),fl=f.flap!=null?f.flap:(P.flap||0),fa=fl?Math.sin(t*(4+fl*3))*.42*Math.min(1,fl*1.4):Math.sin(t*1.2)*.03;
  c.save();leanAt(c,P);[[-1,P.sL],[1,P.sR]].forEach(([sd,s])=>{c.save();c.translate(s[0]*bw*.8,s[1]+br+8);garudaWing(c,sd,wing,fa,1);c.restore()});c.restore();
  drawHuman(c,S,P,{t:t,k:kk,expr:face,noHead:true});
  c.save();leanAt(c,P);c.translate(P.hd[0],P.hd[1]+br+40);c.rotate(o.tilt||0);c.scale(1.12,1.12);c.translate(0,-40);garudaHead(c,kk,t,o.mood);c.restore();
  if(o.prop==='amrut')garudaPot(c,S,P,t)}

/* ---- nagas: coiled cobras with raised hoods (front view), forked tongue flicks; pose stand(rise) | sit(coil low) | bow | point/lunge (strike) ---- */
const NAGA={naga:{s:1,C:{b:'#2a8a7a',d:'#145048',l:'#7ad8c4',belly:'#f2e2a0',bellyD:'#b8984a'}},naga2:{s:1,C:{b:'#3e3e52',d:'#18181f',l:'#8a8aa8',belly:'#ecd48a',bellyD:'#a8883a'}},
  naga_guard:{s:1.45,C:{b:'#2a5a3a',d:'#0e2a18',l:'#6ab07a',belly:'#f0b840',bellyD:'#a86a1a'},fierce:.85,gem:true}};
function nagaFig(c,o,t,kk,N){const pose=typeof o.pose==='string'?o.pose:'stand',M=o.mood||{},an=Math.max(kk||0,M.anger||0,N.fierce||0),C=N.C,ph=(o.f&&o.f.x||0)*.013;c.save();c.scale(N.s,N.s);
  let hx=0,hy=-330,ang=0,hs=1.9;if(pose==='bow'){hx=70;hy=-196;ang=.75}else if(pose==='point'||pose==='lunge'||pose==='rpoint'){hx=96;hy=-262;ang=.3;hs=2.05}else if(pose==='sit'||pose==='sitpray'){hy=-214;hs=1.65}
  hx+=Math.sin(t*1.3+ph)*6;hy+=Math.sin(t*1.7+ph)*3;
  c.fillStyle='rgba(20,30,20,.22)';c.beginPath();c.ellipse(0,4,150,18,0,0,7);c.fill();
  PK.tube(c,PK.ellPts(0,-36,118,30,Math.PI,Math.PI*2,24),28,28,C,{});
  const p0=[-20,-50],c1=[-110,-150],c2=[hx+50,hy+170],p1=[hx,hy+52*hs],pts=[];for(let i=0;i<=18;i++){const u=i/18,v=1-u;pts.push([v*v*v*p0[0]+3*v*v*u*c1[0]+3*v*u*u*c2[0]+u*u*u*p1[0],v*v*v*p0[1]+3*v*v*u*c1[1]+3*v*u*u*c2[1]+u*u*u*p1[1]])}
  PK.tube(c,pts,30,22,C,{belly:1});
  PK.tube(c,PK.ellPts(0,-36,118,30,0,Math.PI,24),30,30,C,{belly:1});
  const tl=[];for(let k=0;k<=10;k++){const u=k/10;tl.push([118+u*70,-36+Math.sin(u*3+t)*8-u*20])}PK.tube(c,tl,26,4,C,{});
  PK.tube(c,PK.ellPts(-6,-18,78,18,.1,Math.PI-.1,16),24,24,C,{belly:1});
  PK.hood(c,hx,hy,ang,hs,t+ph,C,{eye:an>.45?'#ff3a20':'#ffd34a',ph:ph*7});
  c.save();c.translate(hx,hy);c.rotate(ang);c.scale(hs,hs);
  if(an>.45)[-1,1].forEach(sd=>{PK.glow(c,sd*11.5,-61,9,'255,60,30',.45*an);PK.cut(c,cc=>{cc.moveTo(sd*4,-70+an*2);cc.lineTo(sd*18,-74);cc.lineTo(sd*17,-70);cc.closePath()},'#0e0a08',{lw:1,sh:0})});
  if(N.gem){c.translate(0,-62);c.scale(.5,.5);PK.crownK(c,40,{gem:'#e0234a'})}c.restore();
  c.restore()}

/* ---- Bhasmasura: glowing boon hand, turning to ash ---- */
function ashPile(c,w,h,t){const H=w*.3*h;if(H<1)return;const mp=PK.P.smooth([[-w/2,0],[-w*.34,-H*.55],[-w*.12,-H*.95],[w*.08,-H],[w*.3,-H*.62],[w/2,0]]);
  PK.cut(c,mp,PK.lg(c,0,-H,0,0,['#e2deda','#aaa6a2','#6a6662']),{lw:1.8,ink:'#4a4644'});c.save();c.beginPath();mp(c);c.clip();for(let i=0;i<40;i++){const x=(Math.sin(i*12.9)*.5)*w,y=-Math.abs(Math.sin(i*7.3))*H;c.fillStyle=i%5?'rgba(70,66,64,.35)':'rgba(255,140,60,.8)';c.beginPath();c.arc(x,y,i%5?2:1.6,0,7);c.fill()}c.restore();
  for(let i=0;i<14;i++){const u=(t*.25+i/14)%1,x=Math.sin(i*3.7+t*.4)*w*.4,y=-H-u*w*.5;c.fillStyle=`rgba(200,196,192,${.55*(1-u)})`;c.beginPath();c.arc(x,y,2+i%3,0,7);c.fill()}}
function drawBhasma(c,o,t,kk,face){const S=CAST.bhasmasura,P=poseOf(o.pose,'bhasmasura'),f=o.f||{},ash=f.ashc!=null&&o.q?o.q(f.ashc,f.ashd||2.5):(f.ash||0),hg=f.hand!=null?f.hand:1;
  c.save();if(ash>0)c.filter=`grayscale(${Math.min(1,ash*2.2)}) brightness(${1+ash*.35})`;
  drawHuman(c,S,P,{t:t,k:o.k!=null?o.k:(S.kdef||kk),expr:face,prop:o.prop,mood:o.mood,tilt:o.tilt});c.filter='none';
  if(hg>0&&ash<.3){c.save();leanAt(c,P);const h=handAt(S,P,t,1),pu=.8+.2*Math.sin(t*5);PK.glow(c,h[0],h[1]-6,110*hg,'255,130,50',.7*hg*pu);PK.glow(c,h[0],h[1]-6,46*hg,'255,240,210',.85*hg);
    for(let i=0;i<6;i++){const u=(t*.6+i/6)%1;c.fillStyle=`rgba(190,184,180,${.5*(1-u)*hg})`;c.beginPath();c.arc(h[0]+Math.sin(i*2.1+t)*16,h[1]-14-u*60,3+u*4,0,7);c.fill()}c.restore()}
  if(ash>0){const u=Math.max(0,Math.min(1,(ash-.3)/.7)),yc=PK.lerp(-640,10,u);c.save();c.globalCompositeOperation='destination-out';c.fillStyle='#000';c.globalAlpha=1;c.beginPath();c.moveTo(-420,-920);c.lineTo(420,-920);c.lineTo(420,yc);
      for(let i=20;i>=0;i--){const x=-420+i*42;c.lineTo(x,yc+Math.sin(i*2.7+t*3)*14+(i%2?10:-6))}c.closePath();c.fill();c.restore();
    if(u>0&&u<1)for(let i=0;i<40;i++){const v=(t*.5+i/40)%1,x=Math.sin(i*5.3)*110+Math.sin(t+i)*20,y=yc-v*120+v*v*200;c.fillStyle=`rgba(210,206,200,${.7*(1-v)})`;c.beginPath();c.arc(x,y,2+(i%3),0,7);c.fill()}
    ashPile(c,300,Math.min(1,ash*1.1),t)}
  c.restore()}
/* ---- Mohini: spin ---- */
function drawMohini(c,o,t,kk,face){const f=o.f||{},on=f.spin&&(f.spinc==null||!o.q||o.q(f.spinc,.01)>0);if(on){let sx=Math.cos(t*f.spin*Math.PI*2);if(Math.abs(sx)<.08)sx=.08*(sx<0?-1:1);c.scale(sx,1)}
  drawHuman(c,CAST.mohini,poseOf(o.pose,'mohini'),{t:t,k:kk,expr:face,mood:o.mood,tilt:o.tilt,turn:o.mood&&o.mood.turn!=null?o.mood.turn:undefined})}
/* ---- pregnant Diti: generic rig, eyes closed while asleep ---- */
function drawDitiP(c,o,t,kk,face){const P=poseOf(o.pose,'diti_p');drawHuman(c,CAST.diti_p,P,{t:t,k:kk,expr:P.lieDown?'closed':face,mood:o.mood,tilt:o.tilt})}
const isLying=p=>!!(p&&(typeof p==='string'?(PZ[p]&&PZ[p].lieDown):p.lieDown));
function layDown(c,o){if(!(o.f&&o.f.mat===false)){PK.cut(c,cc=>cc.roundRect(-290*.62/.62,-14,600,22,6),PK.lg(c,0,-14,0,8,['#e8cc8a','#c8a058','#8a6a30']),{lw:2});for(let x=-280;x<300;x+=16)PK.stroke(c,cc=>{cc.moveTo(x,-12);cc.lineTo(x+6,6)},'rgba(110,80,30,.4)',1.4)}
  c.translate(250,-60);c.rotate(-Math.PI/2)}
/* ---- Marutas: storm-god babies (crowd unit) and curled unborn pieces ---- */
function babyFace(c,M,t){const ink='#4a2a1a',sk=skinPK(BABY),an=M.anger||0,sad=M.sad||0,su=M.surp||0,sm=(M.smile==null?.4:M.smile)*(1-Math.min(1,an+sad)),mo=Math.max(M.mouth||0,su*.6),bl=Math.min(1,Math.max(M.blink||0,((t*.37)%1)<.03?1:0)),cry=sad>.45;
  PK.cut(c,PK.P.ell(0,0,50,47),PK.lg(c,-50,0,50,0,[sk.h,sk.b,sk.d]),{lw:2.4,ink:ink});[-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*49,4,8,12),sk.b,{lw:1.8,ink:ink,sh:0}));
  PK.cut(c,PK.P.ell(0,0,50,47),'rgba(0,0,0,0)',{lw:0,sh:0});c.fillStyle='rgba(255,110,110,.25)';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*26,16,10,7,0,0,7);c.fill()});
  PK.cut(c,cc=>{cc.moveTo(-6,-46);cc.quadraticCurveTo(4,-62,14,-50);cc.quadraticCurveTo(4,-56,2,-44);cc.closePath()},'#1a1418',{lw:1,sh:0});
  [-1,1].forEach(sd=>{const ex=sd*17,ey=-2;
    if(cry||bl>.6){PK.stroke(c,cc=>{cc.moveTo(ex-9,ey+(cry?-2:1));cc.quadraticCurveTo(ex,ey+(cry?5:4),ex+9,ey+(cry?-2:1))},ink,2.6)}
    else{PK.cut(c,PK.P.ell(ex,ey,8,9),'#fffaf0',{lw:1.6,ink:ink,sh:0});c.fillStyle=an>.35?'#c81e14':'#3a2414';c.beginPath();c.arc(ex+(M.lx||0)*2,ey+1,5.6,0,7);c.fill();c.fillStyle='#0a0604';c.beginPath();c.arc(ex+(M.lx||0)*2,ey+1,2.6,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ex-1.6,ey-1.8,1.6,0,7);c.fill()}
    const bi=ey-14+an*6+(cry?-4:0)-su*3,bo=ey-15-an*2+(sad*5)-su*3;PK.stroke(c,cc=>{cc.moveTo(ex-sd*8,bi);cc.quadraticCurveTo(ex,Math.min(bi,bo)-3,ex+sd*8,bo)},ink,2+an*1.5);
    if(cry)PK.cut(c,cc=>{cc.moveTo(ex+sd*6,ey+4);cc.quadraticCurveTo(ex+sd*10,ey+16,ex+sd*6,ey+19);cc.quadraticCurveTo(ex+sd*2,ey+16,ex+sd*6,ey+4)},'rgba(150,200,255,.9)',{lw:1,ink:'#4a6a9a',sh:0})});
  PK.cut(c,PK.P.ell(0,10,4,3),sk.d,{lw:0,sh:0});
  if(mo>.15||cry){const h=cry?8+mo*8:mo*12;PK.cut(c,PK.P.ell(0,25,cry?10:7,h*.7),'#8a1a24',{lw:1.4,ink:ink,sh:0});PK.cut(c,PK.P.ell(0,25+h*.35,cry?6:4,h*.25),'#e86a7a',{lw:0,sh:0})}
  else PK.stroke(c,cc=>{cc.moveTo(-8,23);cc.quadraticCurveTo(0,23+sm*8-an*6,8,23)},ink,2)}
function babyFig(c,o,t){const M=Object.assign({},o.mood||{}),cry=Math.max(M.sad||0,M.mouth||0)>.45,sk=skinPK(BABY);c.save();
  PK.glow(c,0,-120,150,'150,200,255',.45);PK.stroke(c,cc=>cc.arc(0,-178,74,0,7),'rgba(200,225,255,.9)',3);PK.stroke(c,cc=>cc.arc(0,-178,80,0,7),'rgba(120,170,240,.5)',2,{dash:[3,6]});
  [-1,1].forEach(sd=>{PK.cut(c,PK.P.ell(sd*30,-24,34,22,sd*.15),PK.lg(c,0,-46,0,-2,[sk.h,sk.b,sk.d]),{lw:2});PK.cut(c,PK.P.ell(sd*56,-8,16,10,sd*.25),PK.lg(c,0,-18,0,2,[sk.h,sk.b]),{lw:1.8,sh:0});PK.beadArc(c,sd*44,-18,sd*44,0,3,5,1.8,GOLD)});
  PK.cut(c,PK.P.smooth([[-38,-34],[-42,-78],[-26,-112],[0,-118],[26,-112],[42,-78],[38,-34],[0,-26]]),PK.lg(c,-42,0,42,0,[sk.h,sk.b,sk.d]),{lw:2.2});
  PK.cut(c,PK.P.ell(0,-70,2.6,3),'rgba(80,40,20,.45)',{lw:0,sh:0});
  PK.cut(c,cc=>{cc.moveTo(-30,-44);cc.quadraticCurveTo(0,-32,30,-44);cc.lineTo(18,-20);cc.quadraticCurveTo(0,-14,-18,-20);cc.closePath()},PK.lg(c,-30,0,30,0,['#eef6ff','#a8cef2']),{lw:1.6,sh:0});
  PK.beadArc(c,-18,-110,18,-110,10,9,2.4,'#fff7e8');
  [-1,1].forEach(sd=>{const s0=[sd*30,-104],e=cry?[sd*48,-140]:[sd*44,-70],h=cry?[sd*28,-176]:[sd*16,-64];PK.limbOutline(c,s0,e,14,12);PK.limb(c,sk,s0,e,14,12,{lw:0,sh:0});PK.limbOutline(c,e,h,12,10);PK.limb(c,sk,e,h,12,10,{lw:0,sh:0});PK.cut(c,PK.P.ell(h[0],h[1],10,10),PK.lg(c,h[0]-10,0,h[0]+10,0,[sk.h,sk.b]),{lw:1.6,sh:0})});
  c.save();c.translate(0,-170);if(cry)c.translate(0,0);babyFace(c,M,t);c.save();c.translate(0,-30);c.scale(.62,.62);PK.kirita(c,30);c.restore();c.restore();
  if(cry)[-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*28,-176,10,10),PK.lg(c,sd*28-10,0,sd*28+10,0,[sk.h,sk.b]),{lw:1.6,sh:0}));c.restore()}
function embryo(c,x,y,r,t,cry,seed){seed=seed||0;c.save();c.translate(x,y);const b=1+.03*Math.sin(t*2.4+seed);c.scale(b,b);PK.glow(c,0,0,r*1.9,'255,215,140',.45);PK.glow(c,0,0,r*1.3,'160,200,255',.25);
  PK.cut(c,PK.P.ell(0,0,r,r),'rgba(255,236,200,.42)',{lw:1.4,ink:'rgba(200,120,60,.7)',sh:0});const k=r/40,sk=skinPK(BABY);c.scale(k,k);c.rotate(Math.sin(t*.8+seed)*.15);
  PK.cut(c,cc=>{cc.moveTo(-6,-10);cc.bezierCurveTo(-30,-4,-30,28,-6,30);cc.bezierCurveTo(14,32,26,18,20,2);cc.bezierCurveTo(16,-8,6,-12,-6,-10);cc.closePath()},PK.lg(c,-30,0,26,0,[sk.h,sk.b,sk.d]),{lw:1.6,sh:0});
  PK.cut(c,PK.P.ell(14,22,10,7,.4),sk.b,{lw:1.2,sh:0});
  PK.cut(c,PK.P.ell(-2,-18,15,14),PK.lg(c,-15,0,15,0,[sk.h,sk.b,sk.d]),{lw:1.6,sh:0});
  if(cry>.2){[-1,1].forEach(sd=>PK.stroke(c,cc=>{cc.moveTo(-2+sd*3,-21);cc.lineTo(-2+sd*8,-19);cc.moveTo(-2+sd*3,-21);cc.lineTo(-2+sd*8,-23)},'#3a1a10',1.4));PK.cut(c,PK.P.ell(-2,-10,3.4+cry*2,2+cry*3),'#8a1a24',{lw:.8,sh:0});
    PK.cut(c,PK.P.ell(-11,-14,1.6,2.6),'rgba(150,200,255,.9)',{lw:0,sh:0})}
  else[-1,1].forEach(sd=>PK.stroke(c,cc=>cc.arc(-2+sd*6,-20,3,.2,Math.PI-.2),'#3a1a10',1.4));
  PK.cut(c,PK.P.ell(2,-4,5,4),sk.b,{lw:1,sh:0});c.restore()}
function hexPts(n,D){const P=[[0,0]];for(let i=0;i<6;i++){const a=i/6*Math.PI*2-Math.PI/2;P.push([Math.cos(a)*D,Math.sin(a)*D])}return P.slice(0,n)}
function marutaPieces(c,w,t,F){const n=F.n||7,sp=F.spread==null?1:F.spread,cry=F.cry==null?1:F.cry,r=n>7?w*.045:w*.1,pts=[];
  if(F.born){const cols=Math.min(7,n),rows=Math.ceil(n/cols),cell=w/cols;for(let i=0;i<n;i++){const cx=(i%cols-(cols-1)/2)*cell*Math.max(.2,sp),cy=(Math.floor(i/cols)-(rows-1)/2)*cell*1.25*Math.max(.2,sp);
    c.save();c.translate(cx+(Math.floor(i/cols)%2)*cell*.12,cy+cell*.62);c.scale(cell/190,cell/190);babyFig(c,{mood:cry>.3?{sad:.9,mouth:.5+.3*Math.abs(Math.sin(t*6+i))}:{smile:.5}},t+i*.3);c.restore()}return}
  if(n<=7)hexPts(n,w*.28*sp).forEach(p=>pts.push(p));else hexPts(7,w*.36*sp).forEach(g=>hexPts(7,w*.105*Math.max(.15,sp)).forEach(p=>pts.push([g[0]+p[0],g[1]+p[1]])));
  pts.forEach((p,i)=>{if(F.born){c.save();c.translate(p[0],p[1]+r*1.2);c.scale(r/70,r/70);babyFig(c,{mood:cry>.3?{sad:.9,mouth:.5+.3*Math.abs(Math.sin(t*6+i))}:{smile:.5}},t+i*.3);c.restore()}
    else embryo(c,p[0],p[1],r,t,cry*(.6+.4*Math.abs(Math.sin(t*5+i))),i)})}
function wombView(c,w,t,F){const R=w/2,pu=1+.02*Math.sin(t*2.4);c.save();c.scale(pu,pu);PK.glow(c,0,0,R*1.5,'255,170,120',.4);
  PK.cut(c,PK.P.ell(0,0,R,R*.92),PK.rg(c,-R*.2,-R*.25,R*.1,R,[[0,'rgba(255,240,214,.97)'],[.6,'rgba(250,186,140,.95)'],[1,'rgba(196,84,72,.95)']]),{lw:2.6,ink:'#7a2a24'});
  for(let i=1;i<4;i++)PK.stroke(c,cc=>cc.ellipse(0,0,R*(1-i*.08),R*.92*(1-i*.08),0,Math.PI*(.9+i*.2),Math.PI*(1.5+i*.2)),'rgba(255,240,220,.35)',2);
  const n=F.n==null?1:F.n;if(n===1)embryo(c,0,0,R*.42,t,F.cry||0,0);else if(n>1)marutaPieces(c,w*.9,t,F);
  if(F.flash){c.save();c.globalAlpha*=Math.min(1,F.flash);[[-.7,-.5,.7,.6],[-.6,.5,.6,-.6]].forEach(([a,b,cc_,d])=>{PK.glow(c,0,0,R*.6,'220,235,255',.5);PK.stroke(c,cc=>{cc.moveTo(a*R,b*R);cc.lineTo(cc_*R,d*R)},'#ffffff',6);PK.stroke(c,cc=>{cc.moveTo(a*R,b*R);cc.lineTo(cc_*R,d*R)},'rgba(150,190,255,.7)',16)});c.restore()}
  c.restore()}

/* ---- props: Amrut pot, ring of fire, spinning blades, golden feather, thrown Vajra ---- */
function amrutPot(c,x,y,s,t){c.save();c.translate(x,y);c.scale(s,s);const pu=.75+.25*Math.sin(t*3);PK.glow(c,0,-80,130,'255,244,200',.55*pu);
  const body=PK.P.smooth([[-28,-6],[-50,-30],[-54,-62],[-38,-90],[-18,-98],[18,-98],[38,-90],[54,-62],[50,-30],[28,-6]]);
  PK.cut(c,body,PK.lg(c,-54,0,54,0,['#fff0b0','#f2c14e','#d89a2a','#8a5410']),{lw:2.2});
  c.save();c.beginPath();body(c);c.clip();PK.stroke(c,cc=>cc.ellipse(0,-58,60,12,0,0,Math.PI),'#b8761a',6);PK.stroke(c,cc=>cc.ellipse(0,-58,60,12,0,0,Math.PI),'rgba(255,240,180,.6)',1.6,{dash:[3,4]});
    PK.cut(c,PK.P.ell(-22,-66,8,20,.3),'rgba(255,255,255,.5)',{lw:0,sh:0});c.restore();
  [-30,-10,10,30].forEach((gx,i)=>PK.gem(c,gx,-48+Math.abs(gx)*.12,3.6,i%2?'#18a57a':'#e0234a'));
  PK.cut(c,cc=>cc.roundRect(-26,-10,52,10,4),PK.goldG(c,-26,26),{lw:1.6,sh:0});
  PK.cut(c,PK.P.poly([[-16,-96],[16,-96],[12,-112],[-12,-112]]),PK.goldG(c,-16,16),{lw:1.6,sh:0});
  PK.cut(c,PK.P.ell(0,-114,25,6),PK.goldG(c,-25,25),{lw:1.6,sh:0});PK.cut(c,PK.P.ell(0,-116,18,3.5),'#fffef2',{lw:0,sh:0});
  PK.cut(c,cc=>{cc.moveTo(-22,-118);cc.quadraticCurveTo(-20,-146,0,-150);cc.quadraticCurveTo(20,-146,22,-118);cc.closePath()},PK.lg(c,-22,0,22,0,['#fff0b0','#f2c14e','#b8761a']),{lw:1.8});
  for(let i=0;i<5;i++){c.save();c.translate(0,-150);c.rotate(-Math.PI/2+(i-2)*.38);PK.cut(c,cc=>{cc.moveTo(0,0);cc.quadraticCurveTo(7,-6,16,0);cc.quadraticCurveTo(7,6,0,0)},'#f6b0c8',{lw:1,sh:0});c.restore()}
  PK.cut(c,PK.P.ell(0,-160,5,7),'#fffaf0',{lw:1,sh:0});PK.glow(c,0,-160,26,'255,255,230',.7*pu);
  for(let i=0;i<4;i++){const u=(t*.35+i/4)%1;c.fillStyle=`rgba(255,252,235,${.8*Math.sin(u*Math.PI)})`;c.beginPath();c.arc(Math.sin(i*2.3+t)*22,-120-u*70,2.6,0,7);c.fill()}c.restore()}
function flameT(c,x,y,h,w,t,i){const s=Math.sin(t*7+i*1.7)*w*.35,hh=h*(.8+.25*Math.sin(t*9+i*2.3));c.save();c.translate(x,y);
  PK.cut(c,cc=>{cc.moveTo(-w,0);cc.bezierCurveTo(-w*1.1,-hh*.4,-w*.2+s*.3,-hh*.6,s,-hh);cc.bezierCurveTo(w*.3+s*.3,-hh*.55,w*1.1,-hh*.4,w,0);cc.closePath()},PK.lg(c,0,0,0,-hh,['#ff9a2a','#e8501a','#b8180e']),{lw:1.6,ink:'#6a0e06',sh:0});
  PK.cut(c,cc=>{cc.moveTo(-w*.5,0);cc.bezierCurveTo(-w*.55,-hh*.3,-w*.1+s*.2,-hh*.4,s*.6,-hh*.62);cc.bezierCurveTo(w*.2,-hh*.35,w*.55,-hh*.3,w*.5,0);cc.closePath()},PK.lg(c,0,0,0,-hh*.6,['#fff6b0','#ffd34a','#ffb030']),{lw:0,sh:0});c.restore()}
function fireRing(c,w,t,F){const rx=w/2,ry=w*.17,n=26,h=w*.24,part=F&&F.part;PK.glow(c,0,-h*.4,w*.62,'255,130,40',.35);
  const T=[];for(let i=0;i<n;i++){const a=i/n*Math.PI*2,sy=Math.sin(a);T.push([a,sy])}T.sort((p,q)=>p[1]-q[1]);
  if(part!=='front'){PK.stroke(c,cc=>cc.ellipse(0,0,rx,ry,0,Math.PI,Math.PI*2),'#5a1008',10);PK.stroke(c,cc=>cc.ellipse(0,0,rx,ry,0,Math.PI,Math.PI*2),'#ff7a1a',4)}
  T.forEach(([a,sy],i)=>{if((part==='back'&&sy>0)||(part==='front'&&sy<=0))return;const k=.8+.2*(sy+1)/2;flameT(c,Math.cos(a)*rx,sy*ry,h*k,w*.055*k,t,i)});
  if(part!=='back'){PK.stroke(c,cc=>cc.ellipse(0,0,rx,ry,0,0,Math.PI),'#5a1008',10);PK.stroke(c,cc=>cc.ellipse(0,0,rx,ry,0,0,Math.PI),'#ffb030',4)}}
function bladeWheel(c,w,t,F){const R=w/2,sp=F&&F.sp!=null?F.sp:7;c.save();
  for(let k=0;k<3;k++)PK.stroke(c,cc=>cc.arc(0,0,R*(.62+k*.15),0,Math.PI*2),'rgba(220,230,245,.22)',R*.1);c.rotate(t*sp);
  for(let i=0;i<10;i++){c.save();c.rotate(i/10*Math.PI*2);PK.cut(c,cc=>{cc.moveTo(-R*.08,-R*.22);cc.quadraticCurveTo(R*.2,-R*.6,R*.06,-R);cc.quadraticCurveTo(-R*.02,-R*.6,-R*.2,-R*.3);cc.closePath()},PK.lg(c,-R*.2,0,R*.2,0,['#ffffff','#c8d0dc','#6a7484']),{lw:1.8,ink:'#2a3040',sh:0});
    PK.stroke(c,cc=>{cc.moveTo(-R*.02,-R*.3);cc.quadraticCurveTo(R*.12,-R*.6,R*.05,-R*.92)},'rgba(255,255,255,.8)',1.4);c.restore()}
  PK.cut(c,PK.P.ell(0,0,R*.26,R*.26),PK.goldG(c,-R*.26,R*.26),{lw:2});for(let i=0;i<8;i++){const a=i/8*Math.PI*2;PK.gem(c,Math.cos(a)*R*.17,Math.sin(a)*R*.17,R*.025,i%2?'#18a57a':'#e0234a')}PK.gem(c,0,0,R*.06,'#3b7cf0');c.restore()}
function goldFeather(c,w,t,F){const L=w;c.save();if(F&&F.fall)c.rotate(Math.sin(t*2.2)*.5);PK.glow(c,0,0,L*.6,'255,220,120',.35);c.rotate(-.5);
  const vp=cc=>{cc.moveTo(-L/2,0);cc.bezierCurveTo(-L*.2,-L*.2,L*.3,-L*.16,L/2,0);cc.bezierCurveTo(L*.3,L*.13,-L*.2,L*.16,-L/2,0);cc.closePath()};
  PK.cut(c,vp,PK.lg(c,0,-L*.18,0,L*.15,['#fff4c0','#f2c14e','#c8861a']),{lw:1.8,ink:'#6a3a08'});c.save();c.beginPath();vp(c);c.clip();for(let i=-8;i<=8;i++)PK.stroke(c,cc=>{cc.moveTo(i*L*.055,0);cc.lineTo(i*L*.055+L*.06,-L*.2);cc.moveTo(i*L*.055,0);cc.lineTo(i*L*.055+L*.06,L*.2)},'rgba(140,80,10,.4)',1.1);c.restore();
  PK.stroke(c,cc=>{cc.moveTo(-L*.6,2);cc.quadraticCurveTo(0,-4,L*.48,0)},'#fff8d8',2.4);PK.stroke(c,cc=>{cc.moveTo(-L*.6,2);cc.lineTo(-L*.45,1)},'#c8861a',3);c.restore()}
function vajraThrown(c,w,t,F){const s=w/260,fr=Math.floor(t*12);c.save();PK.glow(c,0,0,w*.5,'170,200,255',.4);
  for(let k=0;k<2;k++){const P=[[0,0]];let y=0;for(let i=1;i<=9;i++){y=Math.sin(fr*7.1+i*3.3+k*5)*w*.06;P.push([-i/9*w,y])}const f=cc=>{P.forEach((p,i)=>i?cc.lineTo(p[0],p[1]):cc.moveTo(p[0],p[1]))};PK.stroke(c,f,'rgba(150,180,255,.45)',10-k*3);PK.stroke(c,f,'#fffbe8',2.6-k)}
  c.rotate(Math.PI/2);PK.vajra(c,0,0,0,s*1.6);c.restore()}
const REELFX={amrut_pot:(c,w,t)=>amrutPot(c,0,w*.62,w/110,t),fire_ring:fireRing,spinning_blades:bladeWheel,golden_feather:goldFeather,vajra_thrown:vajraThrown,
  ash_pile:(c,w,t,F)=>ashPile(c,w,F.h==null?1:F.h,t),embryo:(c,w,t,F)=>embryo(c,0,0,w/2,t,F.cry||0,0),womb_view:wombView,maruta_pieces:marutaPieces};

/* ---- dispatch ---- */
Object.assign(XFIG,{garuda:drawGaruda,bhasmasura:drawBhasma,mohini:drawMohini,diti_p:drawDitiP,maruta_baby:(c,o,t)=>babyFig(c,o,t),
  naga:(c,o,t,kk)=>nagaFig(c,o,t,kk,NAGA.naga),naga2:(c,o,t,kk)=>nagaFig(c,o,t,kk,NAGA.naga2),naga_guard:(c,o,t,kk)=>nagaFig(c,o,t,kk,NAGA.naga_guard)});
const XHEAD={
 garuda:(c,o,t,kk,face,M)=>{const S=CAST.garuda;[-1,1].forEach(sd=>{c.save();c.translate(sd*104,92);garudaWing(c,sd,.42,Math.sin(t*1.2)*.03,1.05);c.restore()});bust(c,S,{t:t});c.save();c.translate(0,-8);c.scale(1.25,1.25);garudaHead(c,kk,t,M);c.restore()},
 maruta_baby:(c,o,t)=>{c.translate(0,250);c.scale(1.5,1.5);babyFig(c,o,t)},
 naga:(c,o,t,kk)=>{c.scale(1.25,1.25);c.translate(0,322);nagaFig(c,o,t,kk,NAGA.naga)},naga2:(c,o,t,kk)=>{c.scale(1.25,1.25);c.translate(0,322);nagaFig(c,o,t,kk,NAGA.naga2)},
 naga_guard:(c,o,t,kk)=>{c.scale(1.25/1.45,1.25/1.45);c.translate(0,322*1.45);nagaFig(c,o,t,kk,NAGA.naga_guard)}
};

/* ---------- engine glue ---------- */
const V2NAMES=new Set(['kacha','devayani','shukracharya','brihaspati','asura1','asura2','asura3','horse','deer','narada','kumara','jaya','vijaya','villager','villager_w','prasuti','sati','diti','danu','asikli','kashyapa','indra','surya','chandra','agni','vayu','hiranyaksha','hiranyakashipu','ravana','harihara','shiva','vishnu','hayagriva','daksha','manu','adishakti','brahmi','madhu','kaitabha','ardha','brahma','vishnu_rest','rudra','kapali','brahma5','kama','prakriti','swaha','nidra','kanya','balak','balika','deva_thin','deva_thin2','indra_thin','haryashva','shavalashva','narada_g','narada_old','cow','mare','doe','duck','hayagriva2','garuda','vinata','naga','naga2','naga_guard','vrikasura','bhasmasura','mohini','parvati','diti_p','maruta','maruta_baby','parashurama','rama','krishna','kalki','yama','ashwatthama','kumbhakarna','meghanada','bala','mahabali','vibhishana','markandeya','lakshmi','sita','arjuna','hanuman','sugriva','ravana10',...[0,1,2,3,4,5,6].map(i=>'rishi'+i)]);
const SCALE={shiva:.62,kumara:.5,default:.62};
Object.assign(SCALE,{balak:.42,balika:.42});
/* ---------- EP07 (Kacha and Devayani, dark cinematic look, Nov 2026): new specs, poses, hand props, Shukracharya's tearing / rising rig.
   Every hook used by older characters is inert unless a spec or figure sets the new key (EP6 + reels render byte-identical).
   Spec keys: wristThread (raksha cord on the right wrist), hairFlower (jasmine in the hair), sleeve (robe sleeve colour), claws (clawed feet).
   Figure prop (right hand): cup (wine cup, ash swirl with f.ash) | cloth (burnt cloth) | leaf (mantra palm leaf, f.glow) | flowers (wild flowers) | veda (book).
   shukracharya keys: tear 0..1 (or tearc cue + teard s): the body cracks with light from inside (eye, navel, chest, skull);
                      rise 0..1 (or risec + rised): the body splits like a cocoon and Kacha rises out of it (kpose, kmood for Kacha), dark-red paper splashes. */
const ROBE='#3a2026';
Object.assign(CAST,{
 // Kacha: Brihaspati's son, the clever young student: black topknot, unbleached dhoti, saffron uttariya, sacred thread, red raksha cord on the right wrist, no beard
 kacha:skinSet('#d49c6c',{skinH:'#f0c494',skinD:'#9a6438',skinM:'#c08a5c',hair:{type:'topknot',col:'#1a1216',bunHi:1.18},lower:L_('#d8c8a0','#b8641e','dhoti',{fan:'#e4d6b0'}),uttariya:'#c8641e',thread:true,neck:['rudraksha'],tilak:'ash',
   muscle:.55,build:.96,wristThread:'#c42820',lip:'#a0404a',kgem:'#c8641e',brow:'#120c10'}),
 // Devayani: Shukracharya's daughter: deep rose-maroon sari, ochre choli, jasmine in her hair, simple gold
 devayani:skinSet('#e2a678',{female:true,bindi:true,hair:{type:'long',col:'#120c12'},lower:L_('#8a2430','#c89a3a','sari'),upper:{type:'choli',col:'#c07a2a'},pallu:'#a8323a',build:.82,neck:['necklace'],bangle:'glass',muscle:0,
   hairFlower:'#f4ecd8',kgem:'#c8862a'}),
 // Shukracharya: the old guru of the asuras: long white jata + beard, dark maroon robe over both shoulders with sleeves, rudraksha, ash tripundra, kamandalu
 shukracharya:skinSet('#b8845c',{skinH:'#d8a47a',skinD:'#7a5236',skinM:'#a67650',hair:{type:'jata',col:'#ece6dc'},beard:'#ece6dc',beardLen:52,mustache:'#ece6dc',brow:'#d8d2c8',tilak:'ash',
   lower:L_('#4a1e24','#8a6a3a','dhoti',{fan:'#5c2a30',len:.85}),uttariya:'#2e1a20',robe:ROBE,sleeve:ROBE,underDress:guruRobe,neck:['rudraksha','rudraksha2'],bangle:'rudraksha',muscle:.25,build:.97,prop:'kamandalu',lip:'#8a4048',kgem:'#7a3a1a'}),
 // Brihaspati: guru of the gods, grave: golden skin, grey jata + beard, turmeric-yellow dhoti, gold uttariya, sacred thread, palm-leaf book, a dim gold halo
 brihaspati:skinSet('#b67e52',{skinH:'#d8a272',skinD:'#7a4e2c',skinM:'#a06c44',hair:{type:'jata',col:'#7a7476'},beard:'#8a8486',beardLen:34,mustache:'#8a8486',brow:'#4a4446',tilak:'vaishnava',
   lower:L_('#d89a10','#7a2a12','dhoti',{pleat:true,fan:'#eab030'}),uttariya:'#e8c040',thread:true,neck:['rudraksha','pearls'],bangle:'rudraksha',muscle:.4,build:.96,prop:'veda',kgem:'#c8901a',
   halo:{r:88,col:['#f4e2b0','#c89a48','#8a5a24','#3a2410'],rgb:'200,150,80',rgb2:'230,200,150',petal:'rgba(240,220,170,.3)',g:.25}}),
 // asuras (generic, matte): brute with mace, lean swordsman, heavy feaster with a wine cup; all horned, red eyes, clawed feet
 asura1:skinSet('#7a4030',{skinH:'#a8644c',skinD:'#44221a',skinM:'#6a382a',hair:{type:'wild',col:'#0c0a0c'},horns:'#d8ccb0',beard:'#0c0a0c',beardLen:14,mustache:'#0c0a0c',brow:'#060406',eyeRed:true,
   lower:L_('#3a2420','#8a6a32','short',{fan:'#4a2e26'}),armor:'#5a4a30',armlet:'#8a6a32',muscle:1,build:1.3,kdef:.45,prop:'gada',claws:true,kgem:'#8a2a1a'}),
 asura2:skinSet('#4e665a',{skinH:'#76907e',skinD:'#283a32',skinM:'#44584e',hair:{type:'wild',col:'#08080a'},horns:'#c8bca0',crown:'asura',crownCol:'#2a2a2a',mustache:'#08080a',brow:'#040406',eyeRed:true,
   lower:L_('#5a1a1a','#7a6a3a','short',{fan:'#6a2424'}),armlet:'#7a6a3a',muscle:.9,build:1.08,kdef:.4,prop:'sword',claws:true,kgem:'#5a1a1a'}),
 asura3:skinSet('#7a4a66',{skinH:'#a2708c',skinD:'#44263a',skinM:'#6a3e58',hair:{type:'wild',col:'#0a080c'},horns:'#e0d0b0',beard:'#0a080c',beardLen:22,mustache:'#0a080c',brow:'#060406',eyeRed:true,
   lower:L_('#2a2634','#8a6a3a','short',{fan:'#3a3444'}),gamcha:'#6a2a20',neck:['rudraksha'],armlet:'#8a6a3a',muscle:.6,build:1.24,kdef:.35,prop:'cup',claws:true,kgem:'#6a2a20'})
});
SCALE.asura1=.64;
// poses (EP07)
PZ.kneel={kneel:1,ph:[0,-150],ch:[0,-276],nk:[0,-316],hd:[0,-366],sL:[-64,-290],sR:[64,-290],hipL:[-24,-146],hipR:[24,-146],fL:[-96,-8],fR:[70,0],hL:[-58,-130],hR:[62,-150],hem:120,sway:0};
PZ.sing={hL:[-28,-318],hR:[112,-462]};
PZ.collapse={kneel:1,ph:[0,-112],ch:[10,-230],nk:[16,-266],hd:[24,-312],sL:[-54,-246],sR:[72,-240],hipL:[-24,-108],hipR:[24,-108],fL:[-92,-4],fR:[96,-4],hL:[-86,-40],hR:[112,-36],lean:.3,hem:100,sway:0};
PZ.hug={hL:[96,-338],hR:[150,-326],hLt:'rest',hLa:1.75,hRt:'rest',hRa:1.9,lean:.06};
PZ.grasp={hL:[118,-404],hR:[184,-372],hLt:'rest',hLa:1.4,hRt:'rest',hRa:1.5,lean:.08,kL:[-40,-128],fL:[-60,0],fR:[56,0]};
PZ.catch={hR:[128,-520],hRt:'hold',hRa:.35};
PZ.fall={lean:-.32,ch:[-8,-384],nk:[-14,-422],hd:[-22,-470],hL:[-176,-470],hR:[150,-462],fL:[-40,0],fR:[74,-46],hem:150,sway:0};
PZ.rise={hL:[-150,-520],hR:[150,-520]};   // arms opening upward (Kacha out of the cocoon)
// --- small rig parts ---
function footClaws(c,x,y,sd){c.save();c.translate(x,y);c.scale(sd,1);for(let k=0;k<4;k++){const tx=27-k*5.5+2,ty=1+k*.6;PK.cut(c,cc=>{cc.moveTo(tx-1.5,ty-2.4);cc.quadraticCurveTo(tx+6,ty-1,tx+6.5,ty+5);cc.quadraticCurveTo(tx+2.5,ty+1.5,tx-1,ty+2);cc.closePath()},'#e8dcc0',{lw:.9,ink:'#1a0c08',sh:0})}c.restore()}
function hairFlowers(c,col){for(let i=0;i<7;i++){const a=PK.lerp(-2.5,-1.55,i/6),x=Math.cos(a)*40-6,y=Math.sin(a)*40+6;PK.cut(c,PK.P.ell(x,y,4.2,4.2),col,{lw:.9,ink:'#6a5a40',sh:0});c.fillStyle='#d8b040';c.beginPath();c.arc(x,y,1.3,0,7);c.fill()}
  PK.cut(c,PK.P.ell(-34,-20,6,6),'#c8282a',{lw:1,ink:'#4a1010',sh:0})}
function wristCord(c,r,w,col,t){const p=PK.L2(r.e,r.t,.84),an=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);c.save();c.translate(p[0],p[1]);c.rotate(an);
  PK.cut(c,cc=>cc.roundRect(-3.2,-w-2.6,6.4,2*w+5.2,3),col,{lw:1.2,sh:0});for(let k=-2;k<=2;k++)PK.stroke(c,cc=>{cc.moveTo(-3,k*w*.42-2);cc.lineTo(3,k*w*.42+2)},'#e8b040',1.3);
  const sw=Math.sin(t*2)*2;[[-1,6],[1,9]].forEach(([s2,L])=>PK.stroke(c,cc=>{cc.moveTo(0,w*s2+s2*2);cc.quadraticCurveTo(-6+sw,w*s2+s2*L*.6,-10+sw,w*s2+s2*L)},col,2));c.restore()}
function guruRobe(c,S,sk,h,sw,ww,t){const R0=S.robe,sh=[[-sw+2,-h+10],[-sw*.36,-h+4],[0,-h*.52],[sw*.36,-h+4],[sw-2,-h+10],[sw*.86,-h*.5],[ww+8,-2],[0,4],[-ww-8,-2],[-sw*.86,-h*.5]];
  const p=PK.P.poly(sh);PK.cut(c,p,PK.lg(c,-sw,0,sw,0,[shade(R0,1.5),R0,shade(R0,.6)]),{lw:2.2,sh:1});
  c.save();c.beginPath();p(c);c.clip();for(let i=-3;i<=3;i++)if(i)PK.stroke(c,cc=>{cc.moveTo(i*sw*.2,-h*.6);cc.quadraticCurveTo(i*sw*.26,-h*.3,i*ww*.3,0)},'rgba(10,2,6,.35)',1.6);c.restore();
  PK.stroke(c,cc=>{cc.moveTo(-sw*.36,-h+4);cc.lineTo(0,-h*.52);cc.lineTo(sw*.36,-h+4)},'#8a6a3a',3)}
// hand props, drawn in the world frame at the right hand (stem / handle in the fist); F = figure dict
function wineCup(c,x,y,s,t,ash){c.save();c.translate(x,y);c.scale(s,s);
  PK.cut(c,PK.P.ell(0,12,13,4),PK.lg(c,-13,0,13,0,['#c89858','#8a5a2a','#4a2a14']),{lw:1.4,sh:0});PK.cut(c,cc=>cc.roundRect(-3,-16,6,28,2),PK.lg(c,-3,0,3,0,['#c89858','#8a5a2a']),{lw:1.3,sh:0});
  const bowl=cc=>{cc.moveTo(-23,-46);cc.bezierCurveTo(-22,-22,-10,-16,0,-16);cc.bezierCurveTo(10,-16,22,-22,23,-46);cc.closePath()};PK.cut(c,bowl,PK.lg(c,-23,0,23,0,['#d0a060','#9a6a32','#5a3416']),{lw:1.8});
  PK.stroke(c,cc=>{cc.moveTo(-20,-36);cc.quadraticCurveTo(0,-30,20,-36)},'rgba(40,16,6,.5)',1.4);
  PK.cut(c,PK.P.ell(0,-46,23,5.5),PK.lg(c,0,-51,0,-41,['#6a1018','#3a060c']),{lw:1.6,sh:0});
  if(ash>0){c.save();c.beginPath();c.ellipse(0,-46,21,4.6,0,0,7);c.clip();for(let k=0;k<3;k++){PK.stroke(c,cc=>{for(let i=0;i<=24;i++){const u=i/24,a=u*7+t*1.4+k*2.1,r=u*19;i?cc.lineTo(Math.cos(a)*r,-46+Math.sin(a)*r*.24):cc.moveTo(0,-46)}},`rgba(170,164,160,${.75*ash})`,1.6-k*.3)}
    for(let i=0;i<9;i++){c.fillStyle=`rgba(30,26,26,${.8*ash})`;c.beginPath();c.arc(Math.sin(i*2.3+t)*15,-46+Math.cos(i*1.7)*3,1.2,0,7);c.fill()}c.restore()}
  c.restore()}
function burntCloth(c,x,y,s,t){c.save();c.translate(x,y);c.scale(s,s);const sw=Math.sin(t*1.6)*3;
  const p=cc=>{cc.moveTo(-14,-4);cc.lineTo(14,-6);cc.quadraticCurveTo(24,30,30+sw,62);for(let i=0;i<=8;i++){const u=i/8;cc.lineTo(PK.lerp(30,-26,u)+sw,66+(i%2?-10:6)+Math.sin(i*2.7)*5)}cc.quadraticCurveTo(-22,30,-14,-4);cc.closePath()};
  PK.cut(c,p,PK.lg(c,0,-6,0,70,['#d8c8a0','#a88a5e','#3a2414','#120806']),{lw:1.8,ink:'#1a0c06'});
  c.save();c.beginPath();p(c);c.clip();PK.stroke(c,cc=>{cc.moveTo(-6,0);cc.quadraticCurveTo(-4,30,-10+sw,60)},'rgba(60,30,10,.35)',1.4);PK.stroke(c,cc=>{cc.moveTo(6,0);cc.quadraticCurveTo(10,32,10+sw,62)},'rgba(60,30,10,.35)',1.4);
    [[8,28,5],[-12,44,4],[14,52,3.4]].forEach(([hx,hy,r])=>{PK.cut(c,PK.P.ell(hx+sw*.5,hy,r,r*.8),'#0c0604',{lw:0,sh:0});PK.stroke(c,cc=>cc.ellipse(hx+sw*.5,hy,r+1.2,r*.8+1.2,0,0,7),'rgba(255,120,40,.6)',1)});c.restore();
  for(let i=0;i<4;i++){const u=(t*.4+i/4)%1;c.fillStyle=`rgba(255,${130+i*20},50,${.8*(1-u)})`;c.beginPath();c.arc(-18+i*14+sw,66-u*30,1.4,0,7);c.fill()}c.restore()}
function palmLeaf(c,x,y,s,t,gl,rot){c.save();c.translate(x,y);c.rotate(rot==null?-.18:rot);c.scale(s,s);if(gl)PK.glow(c,0,0,70,'255,190,90',.35*gl);
  const p=cc=>{cc.moveTo(-60,-8);cc.quadraticCurveTo(0,-11,60,-8);cc.quadraticCurveTo(64,0,60,8);cc.quadraticCurveTo(0,11,-60,8);cc.quadraticCurveTo(-64,0,-60,-8);cc.closePath()};
  PK.cut(c,p,PK.lg(c,0,-10,0,10,['#ead2a0','#c8a868','#8a6a38']),{lw:1.6,ink:'#3a2410'});
  for(let r=-1;r<=1;r++)for(let i=0;i<9;i++){const x0=-50+i*11.5+(r%2?4:0);PK.stroke(c,cc=>{cc.moveTo(x0,r*4.2);cc.quadraticCurveTo(x0+3,r*4.2-2,x0+7,r*4.2)},gl?`rgba(150,40,10,${.6+.4*gl})`:'rgba(60,30,10,.7)',1.3)}
  PK.cut(c,PK.P.ell(-44,0,2.4,2.4),'#3a2410',{lw:0,sh:0});PK.stroke(c,cc=>{cc.moveTo(-44,0);cc.quadraticCurveTo(-56,14,-50,26)},'#8a2a1a',1.6);c.restore()}
function wildFlowers(c,x,y,s,t){c.save();c.translate(x,y);c.scale(s,s);const F=[[-14,-58,'#c83a2a'],[0,-70,'#efe6d0'],[14,-60,'#d8a030'],[-6,-46,'#efe6d0'],[9,-44,'#c83a2a']];
  F.forEach(([fx,fy],i)=>PK.stroke(c,cc=>{cc.moveTo(0,4);cc.quadraticCurveTo(fx*.4,fy*.5,fx,fy)},'#3a5a2a',2));
  [[-10,-24,-.6],[10,-30,.6]].forEach(([lx,ly,a])=>{c.save();c.translate(lx,ly);c.rotate(a);PK.cut(c,PK.P.ell(0,0,4,10),'#4a6a32',{lw:1,sh:0});c.restore()});
  F.forEach(([fx,fy,col],i)=>{const sw=Math.sin(t*1.5+i)*1.5;for(let k=0;k<5;k++){const a=k/5*Math.PI*2+i;PK.cut(c,PK.P.ell(fx+sw+Math.cos(a)*5,fy+Math.sin(a)*5,4.2,2.8,a),col,{lw:.8,ink:'#3a2414',sh:0})}PK.cut(c,PK.P.ell(fx+sw,fy,2.6,2.6),'#e8c040',{lw:.6,sh:0})});c.restore()}
const HPROP={cup:(c,p,t,F)=>wineCup(c,p[0],p[1]-6,.8,t,F.ash||0),cloth:(c,p,t)=>burntCloth(c,p[0],p[1]+4,.9,t),leaf:(c,p,t,F)=>palmLeaf(c,p[0]+4,p[1]-12,.9,t,F.glow||0),
  flowers:(c,p,t)=>wildFlowers(c,p[0],p[1]-4,.9,t),veda:(c,p)=>PK.veda(c,p[0]+2,p[1]-26,-.12)};
// dark-red paper splashes (no gore realism): a burst of drops + a pool; w = size
function bloodSplash(c,w,t,F){const n=F&&F.n||14,s=w/200;c.save();c.scale(s,s);const sp=F&&F.spread!=null?F.spread:1;
  const pool=[];for(let i=0;i<16;i++){const a=i/16*Math.PI*2,rr=(i%2?46:58)+Math.sin(i*3.1)*8;pool.push([Math.cos(a)*rr,Math.sin(a)*rr*.42+12])}PK.cut(c,PK.P.smooth(pool),PK.lg(c,0,-14,0,40,['#7a1018','#4a0810','#2a0408']),{lw:1.6,ink:'#1a0206'});
  for(let i=0;i<n;i++){const a=-Math.PI*.95+i/(n-1)*Math.PI*.9+Math.sin(i*5.3)*.12,d=(70+((i*37)%50))*sp,x=Math.cos(a)*d,y=Math.sin(a)*d*.8,rr=4+((i*13)%7);c.save();c.translate(x,y);c.rotate(a+Math.PI/2);
    PK.cut(c,cc=>{cc.moveTo(0,-rr*2.4);cc.quadraticCurveTo(rr,0,0,rr);cc.quadraticCurveTo(-rr,0,0,-rr*2.4)},PK.lg(c,0,-rr*2,0,rr,['#6a1018','#3a060c']),{lw:1,ink:'#1a0206',sh:0});c.restore()}
  c.restore()}
// Shukracharya: cracks of light (tear) and the cocoon split with Kacha rising (rise)
const SHUKRA_CR=[[[.95,0],0,.32],[[0,1],.24,.56],[[0,.62],.48,.8],[[.3,-1.2],.72,1]];   // [anchor, start, end]
function crackPath(seed,len,g){let x=0,y=0;const P=[[0,0]];for(let i=1;i<=8;i++){x+=Math.sin(seed*7.1+i*2.3)*len*.09;y+=len/8*g;P.push([x,y])}return P}
function drawCracks(c,P,tear,t,HS){const hx=P.hd[0],hy=P.hd[1],an=[[hx+16*HS,hy-2],[P.ph[0],P.ph[1]-34],[P.ch[0],P.ch[1]+26],[hx,hy-40*HS]];
  c.save();c.globalCompositeOperation='source-atop';
  an.forEach((a,k)=>{const sg=SHUKRA_CR[k],u=PK.clamp((tear-sg[1])/(sg[2]-sg[1]));if(u<=0)return;
    for(let j=0;j<5;j++){const ang=j/5*Math.PI*2+k,len=(k===1||k===2?150:70)*u,P2=crackPath(k*5+j,len,1);c.save();c.translate(a[0],a[1]);c.rotate(ang);
      const f=cc=>{P2.forEach((p,i)=>i?cc.lineTo(p[0],p[1]):cc.moveTo(p[0],p[1]))};PK.stroke(c,f,'#2a0408',7*u+2);PK.stroke(c,f,'#ff9a3a',3*u+1);PK.stroke(c,f,'#fff0c0',1.2);c.restore()}});
  c.restore();an.forEach((a,k)=>{const sg=SHUKRA_CR[k],u=PK.clamp((tear-sg[1])/(sg[2]-sg[1]));if(u>0)PK.glow(c,a[0],a[1],40+60*u,'255,160,70',.35*u)})}
function drawShukra(c,o,t,kk,face){const S=CAST.shukracharya,P=poseOf(o.pose||'stand','shukracharya'),f=o.f||{},Q=(k,d,v)=>f[k+'c']!=null&&o.q?o.q(f[k+'c'],f[k+'d']||d):(f[k]||v||0);
  const tear=Q('tear',3),rise=Q('rise',3),lying=isLying(o.pose),HS=S.hs||1.12;
  const body=()=>drawHuman(c,S,P,{t:t,k:o.k!=null?o.k:kk,expr:lying?'closed':face,mood:o.mood,tilt:o.tilt,turn:o.mood&&o.mood.turn!=null?o.mood.turn:undefined});
  if(lying&&rise>0){// the torn body lies on the ground (cracks of light, dark-red paper) and Kacha rises straight up out of the chest
    const e=rise*rise*(3-2*rise);c.save();layDown(c,o);body();c.save();leanAt(c,P);drawCracks(c,P,1,t,HS);c.restore();c.restore();
    [[-200,-20,1],[120,-10,.9],[-60,-40,.7]].forEach(([x,y,s2])=>{c.save();c.translate(x,y);bloodSplash(c,150*s2,t,{spread:.5+e*.5,n:8});c.restore()});
    const K=CAST.kacha,KP=poseOf(f.kpose||'rise','kacha'),ky=(1-e)*560;c.save();c.beginPath();c.rect(-700,-1200,1400,1200-30);c.clip();c.translate(-40,ky-20);PK.glow(c,0,-380,260*e,'255,170,90',.4*e);
    drawHuman(c,K,KP,{t:t,k:0,expr:'calm',mood:f.kmood||{blink:.2,smile:.05}});c.globalCompositeOperation='source-atop';c.fillStyle='rgba(90,8,16,.55)';
    [[-50,-400,26,70],[44,-380,22,90],[-10,-300,30,40],[0,-470,24,20]].forEach(([x,y,rx,ry])=>{c.beginPath();c.ellipse(x,y,rx,ry,0,0,7);c.fill()});c.restore();return}
  if(lying)layDown(c,o);
  if(rise<=0){c.save();if(tear>0)c.translate(Math.sin(t*37)*tear*3,Math.cos(t*29)*tear*2);body();if(tear>0){c.save();leanAt(c,P);drawCracks(c,P,tear,t,HS);c.restore()}c.restore();return}
  const e=rise*rise*(3-2*rise),seam=sd=>cc=>{cc.moveTo(0,-900);for(let i=0;i<=18;i++){const y=-760+i*42;cc.lineTo(Math.sin(i*2.7)*14+(i%2?8:-8),y)}cc.lineTo(sd*600,40);cc.lineTo(sd*600,-900);cc.closePath()};
  [-1,1].forEach(sd=>{c.save();c.translate(sd*e*70,0);c.translate(sd*40,0);c.rotate(sd*e*.42);c.translate(-sd*40,0);c.beginPath();seam(sd)(c);c.clip();body();drawCracks(c,P,1,t,HS);
    c.restore()});
  // Kacha rises out of the opened body; below the torn line he is still inside
  const K=CAST.kacha,KP=poseOf(f.kpose||'rise','kacha'),ky=(1-e)*360,floor=P.ph[1]+30+e*400;
  c.save();c.beginPath();c.rect(-600,-1000,1200,floor+1000);c.clip();c.translate(0,ky);PK.glow(c,0,-380,260*e,'255,170,90',.4*e);
  drawHuman(c,K,KP,{t:t,k:0,expr:'calm',mood:f.kmood||{blink:.2,smile:.05}});
  c.globalCompositeOperation='source-atop';c.fillStyle='rgba(90,8,16,.55)';[[-50,-400,26,70],[44,-380,22,90],[-10,-300,30,40],[0,-470,24,20],[-120,-470,14,40],[120,-470,14,40]].forEach(([x,y,rx,ry])=>{c.beginPath();c.ellipse(x,y,rx,ry,0,0,7);c.fill()});c.restore();
  [[-140,-300,1],[150,-260,.8],[-60,-120,.7],[90,-80,.9]].forEach(([x,y,s2],i)=>{c.save();c.translate(x*(.6+e*.6),y+20*(1-e));bloodSplash(c,120*s2*e,t,{spread:.6+e*.6,n:9});c.restore()})}
Object.assign(XFIG,{shukracharya:drawShukra,
  horse:(c,o,t)=>drawMare(c,Object.assign({},o,{C:{b:'#7a4a2a',d:'#4a2a16',h:'#a06a40'},MN:{b:'#2a1a14',d:'#140c08',h:'#4a3428'},noBand:1}),t),
  deer:(c,o,t)=>drawDoe(c,Object.assign({},o,{noBand:1}),t)});
Object.assign(ANIMAL_HEAD,{horse:ANIMAL_HEAD.mare,deer:ANIMAL_HEAD.doe});
XHEAD.horse=(c,o,t)=>{const H=ANIMAL_HEAD.mare;c.translate(0,40);c.scale(H[2],H[2]);c.translate(-H[0],-H[1]);XFIG.horse(c,o,t)};
XHEAD.deer=(c,o,t)=>{const H=ANIMAL_HEAD.doe;c.translate(0,40);c.scale(H[2],H[2]);c.translate(-H[0],-H[1]);XFIG.deer(c,o,t)};
Object.assign(REELFX,{wine_cup:(c,w,t,F)=>wineCup(c,0,w*.5,w/52,t,F.ash==null?1:F.ash),burnt_cloth:(c,w,t)=>burntCloth(c,0,-w*.45,w/70,t),palm_leaf:(c,w,t,F)=>palmLeaf(c,0,0,w/130,t,F.glow||0,F.rot||0),
  blood_splash:bloodSplash,wild_flowers:(c,w,t)=>wildFlowers(c,0,w*.5,w/40,t)});

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
  if(isLying(o.pose)&&CAST[who]&&!XFIG[who]||isLying(o.pose)&&(who==='diti_p'||who==='mohini'||who==='bhasmasura'))layDown(c,o);
  if(who==='shiva'){const P=shivaPose(o.pose);drawShiva(c,{P:P,t:t,rage:kk>.5,k:kk,expr:face==='closed'?'closed':undefined,imp:o.imp||0,mood:o.mood,tilt:o.tilt})}
  else if(who==='brahma'){const P=poseOf(o.pose||'stand','brahma'),sit=P.sit||(o.lotus!==false&&(!o.pose||o.pose==='stand'));drawBrahmaRig(c,{t:t,k:kk,expr:face,hd:o.hd,mood:o.mood,P:sit?(P.sit?P:null):P,lotus:o.lotus,tilt:o.tilt})}
  else if(who==='vishnu_rest')drawReclineVishnu(c,{t:t});
  else if(who==='ardha')drawArdha(c,{t:t});
  else if(who==='harihara')drawHarihara(c,{t:t});
  else if(XFIG[who])XFIG[who](c,o,t,kk,face);
  else if(ANIMAL[who])ANIMAL[who](c,o,t);
  else drawHuman(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:(CAST[who].kdef||kk),expr:face,prop:o.prop,mood:o.mood,tilt:o.tilt,f:o.f,turn:o.mood&&o.mood.turn!=null?o.mood.turn:undefined});
  figFinish(c,o,x,y,s,FR,OY,RG,.22,.3,true)}
// head close-up: shoulders, chest, garments and jewellery under the head (Opus torso), so heads never float like masks
function bust(c,S,o){const sk=skinPK(S),t=o.t||0,bw=Math.min(S.build||1,1.2);c.save();c.translate(0,-10);
  const sh=[[-122*bw,96],[122*bw,96]];[-1,1].forEach((sd,i)=>{const a=sh[i],b=[sd*156*bw,330];PK.limbOutline(c,a,b,34*bw,28*bw);PK.limb(c,sk,a,b,34*bw,28*bw,{lw:0,sh:0});if(S.armlet)PK.band(c,a,b,.55,30*bw,S.armlet);if(S.female&&S.upper)PK.cut(c,PK.P.caps(a,PK.L2(a,b,.32),36*bw,34*bw),S.upper.col,{lw:1.8,sh:0})});
  c.save();c.translate(0,340);PK.torso(c,sk,262,134*bw,100*bw,0,{fem:!!S.female,muscle:S.muscle});
  const S2=Object.assign({},S);c.scale(1.7,1.7);torsoDress(c,S2,sk,153,72*bw,56*bw,0,t);c.restore();
  if(S.vasuki){const vp=PK.ellPts(0,70,64,30,Math.PI*1.02,-.1,14);for(let i=1;i<=8;i++){const u=i/8;vp.push([64+u*60,70-u*130+Math.sin(u*Math.PI)*10])}PK.tube(c,vp,12,10,VSK,{scales:false,belly:1});PK.hood(c,128,-40,.22+Math.sin(t*1.4)*.1,.68,t,VSK,{ph:2,eye:o.k>.5?'#ff5a3a':'#ffd34a'})}
  PK.cut(c,PK.P.caps([0,88],[0,40],26*(o.nk||1),23*(o.nk||1)),S.skinM,{lw:2,sh:0});c.restore()}
function v2head(who,x,y,s,t,o){ // close-up of the head with neck, shoulders and garments
  const OYH=1300,FR=clamp(s*SC_,2,3.9),RG=[-300,-330,600,640];const c=figBegin(FR,OYH,RG);PK.setDPR(FR);const ex=o.expr||{},kk=ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0,face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(o.flip<0)c.scale(-1,1);c.scale(1.32,1.32);const M=o.mood,turn=o.tilt?0:.06;
  const who0=who;if(who==='kapali')who='shiva';if(who==='brahma5')who='brahma';
  if(XHEAD[who])XHEAD[who](c,o,t,kk,face,M);
  else if(who==='hayagriva2'){const S=CAST.hayagriva2;PK.halo(c,0,-40,108,t,{g:.5,n:26});bust(c,S,{t:t});c.save();c.translate(0,-6);horseHead2(c,kk,t,M);c.restore()}
  else if(ANIMAL[who]){const H=ANIMAL_HEAD[who];c.translate(0,40);c.scale(H[2],H[2]);c.translate(-H[0],-H[1]);ANIMAL[who](c,o,t)}
  else   if(who==='shiva'){const S=CAST.shiva;c.translate(0,-6);c.scale(.86,.86);PK.halo(c,0,-30,112,t,Object.assign({g:.55,n:26},S.halo));c.save();c.translate(0,48);c.scale(1.95,1.95);hairBack(c,S,{hd:[0,0],ph:[0,200]},t);c.restore();c.save();c.translate(0,126);c.scale(.72,.88);bust(c,S,{t:t,k:kk,nk:1.9});c.restore();c.save();c.translate(0,48);c.scale(2.25,2.25);drawHead(c,0,0,{expr:face==='closed'?'closed':'calm',k:kk,S:S,t:t,mood:M,turn:turn});hairFront(c,S,0,0,t);c.restore()}
  else if(who==='brahma'){const S=BRAHMA;PK.halo(c,0,-40,108,t,{g:.5,n:26});bust(c,S,{t:t});
    const side=(x2,tn)=>{c.save();c.translate(x2,12);c.scale(.8,.8);c.filter='brightness(.8)';drawHead(c,0,0,{expr:face,k:kk*.8,S:S,t:t+x2*.01,mood:Object.assign({smile:.2},M&&M.sad?{sad:M.sad*.8}:{}),turn:tn});c.save();c.scale(1-Math.abs(tn)*.3,1);PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);c.restore();c.filter='none';c.restore()};
    side(-62,-.6);side(62,.6);drawHead(c,0,0,{expr:face,k:kk,S:S,t:t,mood:M,turn:turn});PK.hairCap(c,'#e6e0da');PK.jataMukuta(c);if(who0==='brahma5')topHead(c,0,-150,.68,t,kk,face)}
  else if(who==='ardha'||who==='harihara'){const A=CAST[who==='ardha'?'adishakti':'vishnu'],Sh=CAST.shiva;
    halfHead(c,()=>{bust(c,A,{t:t});if(A.hair&&A.hair.type==='long')hairBack(c,A,{hd:[0,0],ph:[0,200]},t);drawHead(c,0,0,{expr:face,k:0,S:A,t:t});hairFront(c,A,0,0,t);headgear(c,A,0,0)},()=>{bust(c,Sh,{t:t});drawHead(c,0,0,{expr:face==='closed'?'closed':'calm',k:0,S:Sh,t:t});hairFront(c,Sh,0,0,t)})}
  else{const S=CAST[who];if(S.halo)PK.halo(c,0,-34,S.halo.r*.95,t,Object.assign({n:26},S.halo,{g:(S.halo.g==null?.8:S.halo.g)*.7}));if(S.sun)PK.sunDisk(c,0,-30,108,t);
    if(S.headType==='horse'){bust(c,S,{t:t});horseHead(c,0,10,kk,t)}else{
      hairBack(c,S,{hd:[0,0],ph:[0,200]},t);bust(c,S,{t:t,k:kk});drawHead(c,0,0,{expr:face,k:o.k!=null?o.k:(S.kdef||kk),S:S,t:t,mood:M,turn:turn});hairFront(c,S,0,0,t);headgear(c,S,0,0)}}
  figFinish(c,o,x,y,s,FR,OYH,RG,.22,.3,false)}

/* ---------- REELS 17,8,16,18-28: cloned and tweaked cast (owner: reuse existing characters) + Hanuman/Sugriva vanara head, axe and bow props ---------- */
Object.assign(CAST,{
 parashurama:Object.assign({},CAST.kashyapa,{hair:{type:'jata',col:'#2a1a14'},beard:'#2a1a14',mustache:'#2a1a14',brow:'#2a1a14',lower:L_('#7a2a14','#4a1a0a','dhoti',{fan:'#a04020'}),muscle:.95,build:1.08,prop:'axe'}),
 rama:Object.assign({},CAST.vishnu,{arms4:false,crown:'small',skin:'#4a86d0',kaustubha:false,halo:{r:92},prop:'bow',tilak:'vaishnava'}),
 krishna:Object.assign({},CAST.vishnu,{arms4:false,crown:'small',skin:'#2a58a8',halo:{r:92},prop:null}),
 kalki:Object.assign({},CAST.vishnu,{arms4:false,crown:'helmet',prop:'sword',armor:'#c9a24a'}),
 yama:Object.assign({},CAST.asura1,{skin:'#2e4a44',skinH:'#5a8a80',skinD:'#14241f',skinM:'#27403a',crown:'asura',lower:L_('#1a1424','#c9a24a','short'),armor:'#3a3040',armlet:'#c9a24a',build:1.22,prop:'gada'}),
 ashwatthama:Object.assign({},CAST.deva_thin2,{skin:'#b0805a',lower:L_('#7a2a2a','#c8a050','dhoti',{fan:'#a04040'}),uttariya:'#5a1a1a',kgem:'#2ad0a0',muscle:.8,build:1.04,prop:'sword'}),
 kumbhakarna:Object.assign({},CAST.asura1,{skin:'#5a3a2e',skinH:'#8a5a46',skinD:'#2a1a14',skinM:'#4a2e24',build:1.5,horns:'#c8b890',lower:L_('#3a1a1a','#c9a24a','short'),armor:'#6a4a3a',prop:'gada'}),
 meghanada:Object.assign({},CAST.ravana,{skin:'#2a2a50',skinH:'#4a4a80',skinD:'#12122a',skinM:'#22223e',build:1.12,crown:'asura',lower:L_('#2a1a4a','#c9a24a','short'),armor:'#c9a24a'}),
 bala:Object.assign({},CAST.deva_thin2,{skin:'#c08848',skinH:'#e0a868',skinD:'#7a4a24',crown:'asura',horns:'#d8ccb0',eyeRed:true,mustache:'#1a0c08',brow:'#0a0606',lower:L_('#8a1a1a','#e0b040','dhoti',{pleat:true,fan:'#c04030'}),uttariya:'#c9a24a',armor:'#e0b040',armlet:'#e0b040',neck:['hara','pearls'],muscle:1,build:1.2,prop:'sword'}),
 ravana10:Object.assign({},CAST.ravana,{skin:'#4a3a34',skinH:'#7a5a50',skinD:'#241a18',crown:'asura',horns:null,build:1.3,lower:L_('#a8182a','#e8c050','dhoti',{pleat:true,fan:'#d04030',dots:'#e8c050'}),uttariya:'#2a1a50',armor:'#e8c050',armlet:'#e8c050',neck:['hara','pearls','garland'],bangle:'#e8c050',muscle:1.1,prop:'sword'}),
 mahabali:Object.assign({},CAST.asura1,{skin:'#b07a4a',crown:'asura',build:1.15,eyeRed:false,lower:L_('#f0e8d8','#e0b040','dhoti'),armor:'#e0b040',armlet:'#e0b040',prop:null}),
 vibhishana:Object.assign({},CAST.deva_thin,{skin:'#7a5a44',crown:'asura',lower:L_('#2a4a7a','#c9a24a','dhoti'),prop:null}),
 markandeya:Object.assign({},CAST.balak,{hs:1.22,build:.92,tilak:'ash'}),
 lakshmi:Object.assign({},CAST.parvati,{lower:L_('#e8a020','#c8102e','sari'),upper:{type:'choli',col:'#c8102e'},pallu:'#f2c14e',prop:'lotus2'}),
 sita:Object.assign({},CAST.parvati,{lower:L_('#e8c040','#2a8a54','sari'),upper:{type:'choli',col:'#2a8a54'},pallu:'#e8e0a0',crown:null,prop:null}),
 arjuna:Object.assign({},CAST.deva_thin2,{skin:'#9a6a44',crown:'small',lower:L_('#2a3a7a','#c8a050','dhoti'),uttariya:'#d8a830',muscle:.9,prop:'bow'}),
 hanuman:skinSet('#d2682c',{skinH:'#f08a4a',skinD:'#8a3a14',skinM:'#b8561e',hair:{type:'none'},crown:'small',lower:L_('#d02a2a','#f0c048','short'),armlet:'#e0b040',muscle:1.4,build:1.48,brow:'#4a1a08',prop:'gada'}),
 sugriva:skinSet('#c8903c',{skinH:'#e8b060',skinD:'#7a5418',skinM:'#a87430',hair:{type:'none'},crown:'small',lower:L_('#2a5a9a','#f0c048','short'),armlet:'#e0b040',muscle:.95,build:1.1,brow:'#3a2408'})
});
HPROP.axe=(c,p)=>{c.save();c.translate(p[0],p[1]);PK.stroke(c,cc=>{cc.moveTo(0,34);cc.lineTo(2,-118)},'#2a1a10',7);PK.stroke(c,cc=>{cc.moveTo(0,34);cc.lineTo(2,-118)},'#7a4a24',4.6);
  PK.cut(c,cc=>{cc.moveTo(3,-112);cc.quadraticCurveTo(46,-120,50,-80);cc.quadraticCurveTo(46,-44,3,-60);cc.quadraticCurveTo(14,-86,3,-112);cc.closePath()},PK.lg(c,0,-110,50,-50,['#f4f6fa','#a8b0c0','#6a7284']),{lw:2,ink:'#2a2a3a'});c.restore()};
HPROP.bow=(c,p)=>{c.save();c.translate(p[0],p[1]);PK.stroke(c,cc=>{cc.moveTo(10,-96);cc.quadraticCurveTo(-34,0,10,96)},'#2a1a10',7);PK.stroke(c,cc=>{cc.moveTo(10,-96);cc.quadraticCurveTo(-34,0,10,96)},'#9a6a2a',4.2);PK.stroke(c,cc=>{cc.moveTo(10,-96);cc.lineTo(10,96)},'rgba(240,232,210,.9)',1.4);c.restore()};
function monkeyHead(c,S,k,t,M){M=M||{};const ink='#3a1a10',an=Math.max(k||0,M.anger||0),bl=Math.min(1,Math.max(M.blink||0,((t*.37)%1)<.03?1:0));
  [-1,1].forEach(sd=>{PK.cut(c,PK.P.ell(sd*40,-6,13,17,sd*.2),PK.lg(c,sd*30,-20,sd*52,10,[S.skinH,S.skin,S.skinD]),{lw:2,ink:ink,sh:0});PK.cut(c,PK.P.ell(sd*40,-6,6,10,sd*.2),'#f0b0a0',{lw:0,sh:0})});
  PK.cut(c,PK.P.ell(0,0,38,36),PK.lg(c,-38,-34,38,36,[S.skinH,S.skin,S.skinD]),{lw:2.4,ink:ink});
  PK.cut(c,PK.P.smooth([[-30,2],[-22,-10],[0,-14],[22,-10],[30,2],[24,34],[0,44],[-24,34]]),PK.lg(c,0,-10,0,44,['#f6c8a0','#e8a878','#c88a5a']),{lw:1.8,ink:ink,sh:0});
  [-1,1].forEach(sd=>{const ex=sd*14,ey=-6,ry=7.5*(1-bl*.85);PK.cut(c,PK.P.ell(ex,ey,9,ry,sd*.2),'#fffaf0',{lw:1.6,ink:ink,sh:0});
    if(bl<.7){c.save();c.beginPath();c.ellipse(ex,ey,9,ry,sd*.2,0,7);c.clip();const ix=ex+(M.lx||0)*3-sd*1.2;c.fillStyle=an>.35?'#c81e14':'#3a2010';c.beginPath();c.arc(ix,ey+(M.ly||0)*2,5.4,0,7);c.fill();c.fillStyle='#0c0604';c.beginPath();c.arc(ix,ey,2.7,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ix-1.5,ey-2,1.3,0,7);c.fill();c.restore()}
    const bi=ey-11+an*6+(M.surp||0)*-4,bo=ey-13-an*2+(M.sad||0)*4;PK.stroke(c,cc=>{cc.moveTo(sd*5,bi);cc.quadraticCurveTo(sd*14,Math.min(bi,bo)-3,sd*25,bo)},ink,3+an*1.2)});
  [-1,1].forEach(sd=>PK.cut(c,PK.P.ell(sd*4,20,2.6,3.6),'#4a2a20',{lw:0,sh:0}));
  const sm=(M.smile||0)*4-an*3;PK.stroke(c,cc=>{cc.moveTo(-14,32);cc.quadraticCurveTo(0,36+sm,14,32)},ink,2);
  PK.cut(c,cc=>{cc.moveTo(-24,-26);cc.quadraticCurveTo(0,-50,24,-26);cc.quadraticCurveTo(0,-34,-24,-26)},'#c9a24a',{lw:1.6,ink:ink,sh:0})}
const mkVanara=who=>function(c,o,t,kk,face){const S=CAST[who],P=poseOf(o.pose||'stand','hayagriva');
  c.save();c.translate(-34,-170);PK.stroke(c,cc=>{cc.moveTo(0,40);cc.bezierCurveTo(-60,60,-90,-20,-60,-90)},ink0,9);PK.stroke(c,cc=>{cc.moveTo(0,40);cc.bezierCurveTo(-60,60,-90,-20,-60,-90)},S.skin,6);c.restore();
  drawHuman(c,S,P,{t:t,k:kk,expr:face,noHead:true,prop:o.prop,mood:o.mood});
  c.save();leanAt(c,P);const hx=P.hd[0],hy=P.hd[1]+Math.sin(t*1.7)*2;c.translate(hx,hy+40);c.rotate(o.tilt||0);c.translate(0,-50);monkeyHead(c,S,kk,t,o.mood);c.restore()};
const ink0='#3a1a10';
Object.assign(XFIG,{hanuman:mkVanara('hanuman'),sugriva:mkVanara('sugriva')});
function drawRavana10(c,o,t,kk,face){const S=CAST.ravana10,P=poseOf(o.pose||'stand','ravana'),hx=P.hd[0],hy=P.hd[1];
  drawHuman(c,S,P,{t:t,k:kk,expr:face,noHead:true,prop:o.prop,mood:o.mood});
  c.save();leanAt(c,P);const sm=[[-74,-26],[74,-26],[-106,-64],[106,-64],[-58,-84],[58,-84],[-26,-118],[26,-118],[0,-152]];sm.forEach(([dx,dy],i)=>{c.save();c.translate(hx+dx,hy+dy);c.scale(.56,.56);drawHead(c,0,0,{expr:i%2?'anger':'calm',k:kk,S:S,t:t+i,mood:o.mood,turn:.1});hairFront(c,S,0,0,t);headgear(c,S,0,0);c.restore()});
  drawHead(c,hx,hy,{expr:face,k:kk,S:S,t:t,mood:o.mood,turn:.1});hairFront(c,S,hx,hy,t);headgear(c,S,hx,hy);c.restore()}
XFIG.ravana10=drawRavana10;
['parashurama','rama','krishna','kalki','yama','ashwatthama','kumbhakarna','meghanada','bala','mahabali','vibhishana','markandeya','lakshmi','sita','arjuna','hanuman','sugriva','ravana10'].forEach(n=>V2NAMES.add(n));
return {PK:PK,has:w=>V2NAMES.has(w),fig:v2fig,head:v2head,CAST:CAST,poseOf:poseOf,drawHuman:drawHuman,drawBrahmaRig:drawBrahmaRig,drawReclineVishnu:drawReclineVishnu,drawArdha:drawArdha,drawShiva:drawShiva,drawHead:drawHead,FX:REELFX,drawJata:drawJata,POSES:POSES,mixPose:mixPose,SH:SH};
