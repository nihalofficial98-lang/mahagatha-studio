/* v2 cast + engine glue. Concatenated INSIDE the same function scope as library/characters/shiva/shiva_v2.js
   (see studio/build.py), so tapered(), elbow(), drawHead(), drawShiva(), POSES, mixPose(), SH, lerp are in scope.
   Engine globals used: clamp, ctx, glow, lotus, figBegin, figFinish, OY, SC_.
   Owner design rules baked in: identity cues readable at a glance; anger = glowing red eyes + heavy brows + plain
   frown of the same width as the smile (NO fangs, NO face lines); calm natural hair; costume always covers the body. */
const hexRgb=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
const toHex=a=>'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
const shade=(h,f)=>toHex(hexRgb(h).map(v=>f<1?v*f:v+(255-v)*(f-1)));
function skinSet(base,extra){return Object.assign({browGap:8,skin:base,skinM:shade(base,.84),skinD:shade(base,.55),skinH:shade(base,1.22),gold:'#e0b04a',ash:'#e8e4ee',red:'#d03a2a',tripundra:false,third:false,brow:'#14101a'},extra||{})}
const clothSet=(c,trim)=>({col:c,colL:shade(c,1.25),colD:shade(c,.6),trim:trim||'#d9a441'});

/* ---------- cast ---------- */
const CAST={
 vishnu:skinSet('#4f7fd6',{hair:{type:'cap',col:'#10101c'},crown:'vishnu',lower:Object.assign(clothSet('#f2c230','#d9822a'),{type:'dhoti',pleat:true}),sash:'#f6ecc8',uttariya:'#f6e7a8',garland:true,tilak:'vaishnava',arms4:true,armlet:'#e6b84a',muscle:.8,browGap:9}),
 hayagriva:skinSet('#4f7fd6',{hair:{type:'none'},headType:'horse',crown:null,lower:Object.assign(clothSet('#f2c230','#d9822a'),{type:'dhoti',pleat:true}),sash:'#f6ecc8',uttariya:'#f6e7a8',garland:true,arms4:true,armlet:'#e6b84a',muscle:.9}),
 daksha:skinSet('#c9915f',{hair:{type:'cap',col:'#26262c'},crown:'small',beard:'#3a3a42',beardLen:18,lower:Object.assign(clothSet('#e9dfc2','#b8862a'),{type:'dhoti'}),sash:'#f4efe0',beads:true,tilak:'dot',armlet:'#c9a24a',muscle:.6}),
 manu:skinSet('#d39a68',{hair:{type:'cap',col:'#18141c'},lower:Object.assign(clothSet('#efe6cc','#b8862a'),{type:'dhoti'}),sash:'#f4efe0',tilak:'dot',muscle:.7,build:.95}),
 adishakti:skinSet('#f0b98a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:Object.assign(clothSet('#b4182a','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e0b04a'},pallu:'#d8283a',build:.82,necklace:'#e0b04a',armlet:'#e0b04a',muscle:0}),
 brahmi:skinSet('#e8b080',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:Object.assign(clothSet('#d8a040','#b8742e'),{type:'sari'}),upper:{type:'choli',col:'#e8d8a8'},pallu:'#f0e4c0',build:.82,necklace:'#c9a24a',muscle:0}),
 madhu:skinSet('#55507a',{hair:{type:'topknot',col:'#0c0a14'},horns:'#e8dcc0',build:1.3,brow:'#08060c',eyeRed:true,lower:Object.assign(clothSet('#7a1c1c','#c9a24a'),{type:'dhoti'}),sash:'#c9a24a',armor:true,armlet:'#c9a24a',muscle:1,kdef:.55}),
 kaitabha:skinSet('#8a3a34',{hair:{type:'cap',col:'#0c0a14'},horns:'#e8dcc0',build:1.15,brow:'#08060c',eyeRed:true,lower:Object.assign(clothSet('#2a2a54','#c9a24a'),{type:'dhoti'}),sash:'#d9a441',armor:true,armlet:'#c9a24a',muscle:1,kdef:.55})
};
// the seven sages: distinct skin, hair, beard and cloth so each can be told apart
[['vasishtha','#c78a5a','white','#f0ece4','#e8962a'],['marichi','#b9794a','dark','#2a2430','#efe6cc'],['atri','#cf9566','white','#e8e4de','#caa040'],['angirasa','#b4784c','grey','#8a8a92','#e8b060'],
 ['pulastya','#c28a5c','dark','#241e2a','#f0e8d0'],['pulaha','#d0986a','white','#eeeae2','#8aa070'],['kratu','#bc7e50','none','#1c1620','#e0a040']].forEach(([n,sk,hair,bc,cl],i)=>{
  CAST['rishi'+i]=skinSet(sk,{hair:{type:hair==='white'||hair==='grey'?'long':'topknot',col:hair==='white'?'#f0ece4':(hair==='grey'?'#9a9aa2':'#1a1620')},beard:hair==='none'?null:bc,beardLen:hair==='white'?38:22,mustache:hair==='none'?null:bc,
  lower:Object.assign(clothSet(cl,'#b8862a'),{type:'dhoti'}),sash:'#f6f0e0',beads:true,tilak:'ash',ash:'#efeae4',armlet:null,muscle:.45,build:.92,name:n})});


/* ---- coded replacements for the painted cut-outs: every one has joints, head, eyes and expression ---- */
Object.assign(CAST,{
 narada:skinSet('#a86a40',{hair:{type:'topknot',col:'#16121a'},lower:Object.assign(clothSet('#f2eee4','#c9a24a'),{type:'dhoti'}),sash:'#e8962a',beads:true,tilak:'vaishnava',muscle:.4,build:.9}),
 kumara:skinSet('#e0a878',{hair:{type:'topknot',col:'#16121a'},lower:Object.assign(clothSet('#f6f2ea','#c9a24a'),{type:'dhoti'}),sash:'#f6f0e0',beads:true,tilak:'ash',muscle:.05,build:.78,hs:1.42}),
 jaya:skinSet('#46b0a4',{hair:{type:'none'},crown:'helmet',lower:Object.assign(clothSet('#e8b838','#b8862a'),{type:'dhoti'}),armor:true,armlet:'#e0b040',muscle:1,build:1.18,brow:'#10202a'}),
 vijaya:skinSet('#46b0a4',{hair:{type:'none'},crown:'helmet',plume:'#d02a2a',lower:Object.assign(clothSet('#f6f2ea','#e0b040'),{type:'dhoti'}),armor:true,armlet:'#e0b040',muscle:1,build:1.12,brow:'#10202a'}),
 villager:skinSet('#c08a5a',{hair:{type:'cap',col:'#1a1616'},beard:'#1e1a1a',beardLen:12,lower:Object.assign(clothSet('#f1ead8','#b8862a'),{type:'dhoti'}),sash:'#f4efe0',muscle:.3,build:.95}),
 villager_w:skinSet('#c8905e',{female:true,bindi:true,hair:{type:'long',col:'#1a1416'},lower:Object.assign(clothSet('#3a8fc8','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e8d8a8'},pallu:'#2a78b0',build:.82,muscle:0}),
 prasuti:skinSet('#d9a070',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:Object.assign(clothSet('#a8182a','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e0b04a'},pallu:'#d8283a',build:.82,necklace:'#e0b04a',muscle:0}),
 sati:skinSet('#f0b98a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},crown:'devi',lower:Object.assign(clothSet('#f4f0e6','#ef9a1f'),{type:'sari'}),upper:{type:'choli',col:'#ef9a1f'},pallu:'#ef9a1f',build:.8,necklace:'#e0b04a',armlet:'#e0b04a',muscle:0}),
 diti:skinSet('#a8704a',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},lower:Object.assign(clothSet('#8a1a3a','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e0b04a'},pallu:'#a8284a',build:.84,muscle:0}),
 danu:skinSet('#b87a52',{female:true,bindi:true,hair:{type:'long',col:'#14101a'},lower:Object.assign(clothSet('#1f7a4a','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e0b04a'},pallu:'#2a9a5a',build:.84,muscle:0}),
 asikli:skinSet('#c8905e',{female:true,bindi:true,hair:{type:'long',col:'#18121c'},lower:Object.assign(clothSet('#3a8fc8','#e0b04a'),{type:'sari'}),upper:{type:'choli',col:'#e8d8a8'},pallu:'#2a78b0',build:.82,muscle:0}),
 kashyapa:skinSet('#c28a5c',{hair:{type:'long',col:'#e8e4de'},beard:'#e8e4de',beardLen:30,mustache:'#e8e4de',lower:Object.assign(clothSet('#e8962a','#b8862a'),{type:'dhoti'}),sash:'#f6f0e0',beads:true,tilak:'ash',muscle:.4,build:.92}),
 indra:skinSet('#d9a35a',{hair:{type:'cap',col:'#18141c'},crown:'vishnu',lower:Object.assign(clothSet('#f2eee4','#e0b040'),{type:'dhoti'}),sash:'#3a6ad0',armlet:'#e0b040',muscle:.85}),
 surya:skinSet('#f0a040',{hair:{type:'cap',col:'#241810'},crown:'small',lower:Object.assign(clothSet('#e8602a','#e0b040'),{type:'dhoti'}),sash:'#f6c040',armlet:'#e0b040',muscle:.8}),
 chandra:skinSet('#dfe8f4',{hair:{type:'cap',col:'#202838'},crown:'small',lower:Object.assign(clothSet('#f2f4fa','#a8b8d8'),{type:'dhoti'}),sash:'#cfd8ee',armlet:'#a8b8d8',muscle:.55}),
 hiranyaksha:skinSet('#6a2f2a',{hair:{type:'topknot',col:'#0c0a14'},horns:'#e8dcc0',build:1.3,brow:'#08060c',eyeRed:true,lower:Object.assign(clothSet('#2a1a1a','#c9a24a'),{type:'dhoti'}),sash:'#c9a24a',armor:true,armlet:'#c9a24a',muscle:1,kdef:.55}),
 hiranyakashipu:skinSet('#8a4a2a',{hair:{type:'topknot',col:'#0c0a14'},horns:'#e8c050',crown:null,build:1.25,brow:'#08060c',eyeRed:true,lower:Object.assign(clothSet('#c8282a','#e0b040'),{type:'dhoti'}),sash:'#e0b040',armor:true,armlet:'#e0b040',muscle:1,kdef:.5}),
 ravana:skinSet('#4a3028',{hair:{type:'topknot',col:'#0c0a14'},crown:'small',build:1.28,brow:'#08060c',eyeRed:true,lower:Object.assign(clothSet('#a8182a','#e0b040'),{type:'dhoti'}),sash:'#e0b040',armor:true,armlet:'#e0b040',muscle:1,kdef:.45})
});

/* ---------- poses (joints in rig units; feet at 0, +y down) ---------- */
const BASE=JSON.parse(JSON.stringify(POSES.calm));delete BASE.tri;
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
const poseOf=(n,who)=>V3.has(who)?poseOf3(n,who):(n&&typeof n==='object')?n:((who==='vishnu'||who==='hayagriva')&&(!n||n==='stand')?poseOf0('vstand'):poseOf0(n));
const poseOf0=(n)=>Object.assign(JSON.parse(JSON.stringify(BASE)),JSON.parse(JSON.stringify(PZ[n]||PZ[{tri:'hold',rest:'stand',cross:'sit',fist:'hold',cup:'open'}[n]]||{})));

/* ---------- generic body parts (colour-spec driven) ---------- */
function limbS(c,S,A,T,l1,l2,side,w){const r=elbow(A,T,l1,l2,side),E=r.e;tapered(c,A,E,w[0],w[1],S.skin);tapered(c,E,r.t,w[1],w[2],S.skin);
  c.globalAlpha=.42;const sd=(p,q,wa,wb)=>{const dx=q[0]-p[0],dy=q[1]-p[1],d=Math.hypot(dx,dy)||1,nx=-dy/d*side,ny=dx/d*side;c.fillStyle=S.skinD;c.beginPath();c.moveTo(p[0]+nx*wa*.1,p[1]+ny*wa*.1);c.lineTo(q[0]+nx*wb*.1,q[1]+ny*wb*.1);c.lineTo(q[0]+nx*wb,q[1]+ny*wb);c.lineTo(p[0]+nx*wa,p[1]+ny*wa);c.fill()};
  sd(A,E,w[0],w[1]);sd(E,r.t,w[1],w[2]);c.globalAlpha=(S.muscle??.5)*.3;c.fillStyle=S.skinH;c.beginPath();c.ellipse(lerp(A[0],E[0],.4),lerp(A[1],E[1],.4),w[0]*.45,w[0]*.9,Math.atan2(E[1]-A[1],E[0]-A[0])+1.57,0,7);c.fill();c.globalAlpha=1;r.s=A;return r}
function handS(c,S,p,grip,ang=0){c.save();c.translate(p[0],p[1]);c.rotate(ang);c.fillStyle=S.skinM;c.beginPath();c.ellipse(0,0,10,12,0,0,7);c.fill();
  if(!grip){c.fillStyle=S.skin;[-6,-2,2,6].forEach(x=>{c.beginPath();c.ellipse(x,11+Math.abs(x)*.1,3,8,0,0,7);c.fill()})}c.fillStyle=S.skinD;c.globalAlpha=.4;c.beginPath();c.ellipse(4,2,6,9,0,0,7);c.fill();c.globalAlpha=1;c.restore()}
function armband(c,r,w,col){const E=r.e,A=r.s,x=lerp(A[0],E[0],.46),y=lerp(A[1],E[1],.46);c.save();c.translate(x,y);c.rotate(Math.atan2(E[1]-A[1],E[0]-A[0])+1.57);c.fillStyle=col;c.beginPath();c.roundRect(-w-2,-9,2*w+4,18,3);c.fill();c.strokeStyle='rgba(60,30,0,.45)';c.lineWidth=1.6;c.stroke();c.fillStyle='rgba(255,255,255,.28)';c.fillRect(-w,-7,2*w,3);c.fillStyle='#d8342a';c.beginPath();c.arc(0,0,3.2,0,7);c.fill();c.restore()}

function legsS(c,S,P,sp){
  if(P.sit){ // crossed legs under a cloth mound
    c.fillStyle=S.skinD;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*46,-14,52,16,sd*-.08,0,7);c.fill()});return}
  const st=(h,f,side)=>{const r=elbow(h,f,86,92,side);tapered(c,h,r.e,31,23,S.skin);tapered(c,r.e,f,23,14,S.skin);
    c.globalAlpha=.4;tapered(c,[h[0]+side*10,h[1]],[r.e[0]+side*8,r.e[1]],9,8,S.skinD);tapered(c,[r.e[0]+side*7,r.e[1]],[f[0]+side*6,f[1]-6],8,6,S.skinD);c.globalAlpha=1;
    c.fillStyle=S.skinM;c.beginPath();c.ellipse(f[0]+side*4,f[1]-3,19,8,0,0,7);c.fill()};
  st(P.hipL,P.fL,-1);st(P.hipR,P.fR,1)}

function clothS(c,S,P,sw,sp){ // lower garment: dhoti / sari / seated mound
  const L=S.lower;if(!L)return;const wy=P.ph[1]-4;
  if(P.sit){const g=c.createLinearGradient(-170,0,170,0);g.addColorStop(0,L.colL);g.addColorStop(.5,L.col);g.addColorStop(1,L.colD);c.fillStyle=g;
    c.beginPath();c.moveTo(-38,wy+6);c.bezierCurveTo(-96,wy-6,-178,-62,-172,-14);c.bezierCurveTo(-170,6,-120,8,0,8);c.bezierCurveTo(120,8,170,6,172,-14);c.bezierCurveTo(178,-62,96,wy-6,38,wy+6);c.closePath();c.fill();
    c.strokeStyle='rgba(0,0,0,.22)';c.lineWidth=2.2;[-110,-60,-20,20,60,110].forEach(x=>{c.beginPath();c.moveTo(x*.35,wy+10);c.quadraticCurveTo(x*1.1,-48,x*1.45,-6);c.stroke()});
    c.fillStyle='rgba(255,240,200,.16)';c.beginPath();c.ellipse(-110,-40,40,16,-.25,0,7);c.fill();c.fillStyle='rgba(0,0,0,.18)';c.beginPath();c.ellipse(110,-36,40,14,.25,0,7);c.fill();
    c.fillStyle=L.trim;c.fillRect(-170,-4,340,7);c.fillStyle=S.skin;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*30,-6,24,9,sd*-.15,0,7);c.fill()});return}
  const hem=(-wy-12)*(L.len||1),topW=(S.female?44:52)+sp*.22,botW=(S.female?(S.lower.type==='sari'?74:62):60)+sw*4+sp*.7;
  c.save();c.beginPath();c.moveTo(-topW,wy);c.lineTo(topW,wy);c.lineTo(botW,wy+hem*.55);
  for(let i=0;i<=8;i++){const u=i/8,x=lerp(botW,-botW,u),y=wy+hem+Math.sin(u*6+sw)*3;c.lineTo(x,y)}c.lineTo(-botW,wy+hem*.55);c.closePath();
  const g=c.createLinearGradient(-botW,0,botW,0);g.addColorStop(0,L.colL);g.addColorStop(.5,L.col);g.addColorStop(1,L.colD);c.fillStyle=g;c.fill();c.clip();
  c.strokeStyle='rgba(0,0,0,.2)';c.lineWidth=2.2;for(let i=-5;i<=5;i++){c.beginPath();c.moveTo(i*topW/5.5,wy+8);c.quadraticCurveTo(i*botW/4.2+sw*2,wy+hem*.5,i*botW/3.4+sw*3,wy+hem)};c.stroke();
  c.fillStyle='rgba(255,240,200,.14)';c.beginPath();c.moveTo(-topW,wy);c.lineTo(-14,wy);c.quadraticCurveTo(-30,wy+hem*.5,-botW,wy+hem);c.closePath();c.fill();
  c.fillStyle=L.trim;c.fillRect(-botW-4,wy+hem-14,2*botW+8,10);
  if(L.pleat){const pw=30;c.fillStyle=L.colL;c.beginPath();c.moveTo(-pw*.5,wy+6);c.lineTo(pw*.5,wy+6);c.lineTo(pw+8+sw*2,wy+hem-8);c.lineTo(-pw-8+sw*2,wy+hem-8);c.closePath();c.fill();c.strokeStyle=L.colD;c.lineWidth=2;for(let i=-3;i<=3;i++){c.beginPath();c.moveTo(i*pw/6,wy+8);c.lineTo(i*(pw+8)/3.2+sw*2,wy+hem-10);c.stroke()}c.fillStyle=L.trim;c.beginPath();c.moveTo(-pw-8+sw*2,wy+hem-14);c.lineTo(pw+8+sw*2,wy+hem-14);c.lineTo(pw+8+sw*2,wy+hem-6);c.lineTo(-pw-8+sw*2,wy+hem-6);c.fill()}
  if(L.type==='sari'){c.fillStyle='rgba(255,230,160,.5)';for(let i=0;i<6;i++){c.beginPath();c.arc(-botW+i*botW/2.5+10,wy+hem-40-(i%2)*30,3.4,0,7);c.fill()}}
  c.restore();
  c.fillStyle=L.trim;c.beginPath();c.roundRect(-topW-3,wy-7,2*topW+6,11,5);c.fill();c.fillStyle='rgba(0,0,0,.25)';c.fillRect(-topW,wy+2,2*topW,2)}

function hairBack(c,S,P,t){const H=S.hair;if(!H||H.type==='none')return;
  if(H.type==='long'){const hx=P.hd[0],hy=P.hd[1],sw=Math.sin(t*1.5)*2;c.fillStyle=H.col;c.beginPath();c.moveTo(hx-36,hy-6);c.bezierCurveTo(hx-62,hy+50,hx-58+sw,hy+160,hx-40,P.ph[1]-30);c.lineTo(hx+40,P.ph[1]-30);c.bezierCurveTo(hx+58+sw,hy+160,hx+62,hy+50,hx+36,hy-6);c.closePath();c.fill();
    c.fillStyle='rgba(255,255,255,.12)';c.beginPath();c.ellipse(hx-24,hy+80,6,50,.1,0,7);c.fill()}}
function hairFront(c,S,hx,hy){const H=S.hair;if(!H||H.type==='none'||S.headType==='horse')return;c.save();c.translate(hx,hy);c.fillStyle=H.col;
  c.beginPath();c.moveTo(-36,-8);c.bezierCurveTo(-42,-56,42,-56,36,-8);c.bezierCurveTo(26,-30,-26,-30,-36,-8);c.closePath();c.fill();
  c.fillStyle='rgba(255,255,255,.10)';c.beginPath();c.ellipse(-12,-40,14,5,-.3,0,7);c.fill();
  if(H.type==='topknot'){c.fillStyle=H.col;c.beginPath();c.ellipse(0,-58,17,17,0,0,7);c.fill();c.fillStyle=S.gold;c.fillRect(-10,-44,20,5)}
  if(H.type==='long'){c.strokeStyle='rgba(0,0,0,.35)';c.lineWidth=2;c.beginPath();c.moveTo(0,-45);c.quadraticCurveTo(-3,-30,-6,-14);c.stroke()}
  c.restore()}
function headgear(c,S,hx,hy){c.save();c.translate(hx,hy);const g='#e6b84a',gd='#c4882a';
  if(S.crown==='vishnu'){c.fillStyle=g;c.beginPath();c.moveTo(-28,-22);c.lineTo(-22,-74);c.lineTo(-10,-62);c.lineTo(0,-118);c.lineTo(10,-62);c.lineTo(22,-74);c.lineTo(28,-22);c.closePath();c.fill();c.fillStyle=gd;c.fillRect(-28,-30,56,8);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-40,4.4,0,7);c.fill();c.fillStyle='#6ac0e8';c.beginPath();c.arc(0,-74,3.6,0,7);c.fill()}
  if(S.crown==='small'){c.fillStyle=g;c.beginPath();c.moveTo(-26,-24);c.lineTo(-21,-52);c.lineTo(-10,-40);c.lineTo(0,-62);c.lineTo(10,-40);c.lineTo(21,-52);c.lineTo(26,-24);c.closePath();c.fill();c.fillStyle=gd;c.fillRect(-26,-29,52,6);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-35,3.4,0,7);c.fill()}
  if(S.crown==='devi'){c.fillStyle=g;c.beginPath();c.moveTo(-30,-22);c.lineTo(-26,-60);c.lineTo(-14,-48);c.lineTo(-7,-84);c.lineTo(0,-104);c.lineTo(7,-84);c.lineTo(14,-48);c.lineTo(26,-60);c.lineTo(30,-22);c.closePath();c.fill();c.fillStyle=gd;c.fillRect(-30,-30,60,8);c.fillStyle='#e0302a';[[0,-45],[-16,-39],[16,-39]].forEach(([x,y])=>{c.beginPath();c.arc(x,y,3.4,0,7);c.fill()})}
  if(S.crown==='helmet'){c.fillStyle=g;c.beginPath();c.moveTo(-34,-14);c.bezierCurveTo(-36,-58,36,-58,34,-14);c.lineTo(22,-20);c.lineTo(-22,-20);c.closePath();c.fill();c.fillStyle=gd;c.fillRect(-34,-26,68,7);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-36,3.6,0,7);c.fill();c.fillStyle=g;c.beginPath();c.moveTo(-34,-14);c.lineTo(-36,22);c.lineTo(-26,22);c.lineTo(-22,-12);c.closePath();c.fill();c.beginPath();c.moveTo(34,-14);c.lineTo(36,22);c.lineTo(26,22);c.lineTo(22,-12);c.closePath();c.fill();if(S.plume){c.fillStyle=S.plume;c.beginPath();c.moveTo(0,-56);c.bezierCurveTo(18,-84,48,-80,60,-60);c.bezierCurveTo(44,-66,22,-66,6,-46);c.closePath();c.fill()}}
  if(S.horns){c.fillStyle=S.horns;[-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*22,-38);c.bezierCurveTo(sd*40,-60,sd*58,-70,sd*56,-102);c.bezierCurveTo(sd*50,-80,sd*34,-62,sd*14,-44);c.closePath();c.fill();c.fillStyle='rgba(0,0,0,.25)';c.beginPath();c.moveTo(sd*24,-40);c.bezierCurveTo(sd*40,-58,sd*52,-66,sd*54,-90);c.bezierCurveTo(sd*44,-70,sd*34,-58,sd*18,-44);c.fill();c.fillStyle=S.horns})}
  c.restore()}
function horseHead(c,hx,hy,k,t){c.save();c.translate(hx,hy);const sw=Math.sin(t*2)*3;
  // glowing mane
  c.fillStyle='rgba(255,236,176,.5)';for(let i=-3;i<=3;i++){c.beginPath();c.moveTo(i*6,-60);c.bezierCurveTo(i*14+sw,-20,i*17-sw,40,i*15,100+Math.abs(i)*8);c.bezierCurveTo(i*9,40,i*8,-10,i*6+5,-60);c.fill()}
  const g=c.createLinearGradient(-40,0,40,0);g.addColorStop(0,'#fbf8ee');g.addColorStop(.6,'#e8e2d4');g.addColorStop(1,'#a8a2b4');c.fillStyle=g;
  c.beginPath();c.moveTo(-26,-62);c.bezierCurveTo(-46,-30,-40,20,-24,66);c.bezierCurveTo(-12,82,12,82,24,66);c.bezierCurveTo(40,20,46,-30,26,-62);c.bezierCurveTo(12,-72,-12,-72,-26,-62);c.fill();
  c.fillStyle='#e8e2d4';[-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*18,-62);c.lineTo(sd*30,-98);c.lineTo(sd*34,-58);c.closePath();c.fill();c.fillStyle='#e8a8b0';c.beginPath();c.moveTo(sd*21,-64);c.lineTo(sd*29,-90);c.lineTo(sd*31,-62);c.fill();c.fillStyle='#e8e2d4'});
  c.fillStyle='rgba(30,30,70,.3)';c.beginPath();c.ellipse(24,10,10,48,0,0,7);c.fill();
  c.fillStyle='#1a1018';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*8,66,3,5,sd*.4,0,7);c.fill();c.beginPath();c.ellipse(sd*20,-16,6,4.6,sd*-.3,0,7);c.fill()});
  c.fillStyle=k>.3?'#ff3a20':'#ffe08a';[-1,1].forEach(sd=>{c.beginPath();c.arc(sd*20,-16,2.2,0,7);c.fill()});
  c.strokeStyle='#14040a';c.lineWidth=2.4;c.lineCap='round';c.beginPath();c.moveTo(-14,76);c.quadraticCurveTo(0,k>.3?72:79,14,76);c.stroke();
  c.strokeStyle='#14040a';c.lineWidth=5;[-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*8,-30);c.lineTo(sd*30,-26-k*8);c.stroke()});
  c.restore()}

/* four-armed Vishnu: back hands hold the Sudarshana chakra (left) and the shankha (right) at head height */
function extraArms(c,S,P,t){const T=[[-134,-466],[134,-466]];[-1,1].forEach((sd,i)=>{const A=[sd*58,-404],r=limbS(c,S,A,T[i],64,62,sd,[16,13,10]);armband(c,r,14,S.armlet||S.gold);handS(c,S,r.t,false,sd*-.3)});
  c.save();c.translate(T[0][0]-4,T[0][1]-30);glow2(c,0,0,54,'255,225,120',.45);c.rotate(t*2.4);c.strokeStyle='#f6d870';c.lineWidth=6;c.beginPath();c.arc(0,0,27,0,7);c.stroke();c.lineWidth=2.4;for(let i=0;i<8;i++){const a=i*.785;c.beginPath();c.moveTo(0,0);c.lineTo(Math.cos(a)*27,Math.sin(a)*27);c.stroke();c.beginPath();c.moveTo(Math.cos(a)*27,Math.sin(a)*27);c.lineTo(Math.cos(a)*36,Math.sin(a)*36);c.stroke()}c.restore();
  c.save();c.translate(T[1][0]+2,T[1][1]-16);c.rotate(.25);const cg=c.createLinearGradient(-14,0,14,0);cg.addColorStop(0,'#fffaf0');cg.addColorStop(1,'#cfc3a2');c.fillStyle=cg;c.beginPath();c.moveTo(0,22);c.bezierCurveTo(-22,6,-18,-26,0,-34);c.bezierCurveTo(18,-26,22,6,0,22);c.fill();c.strokeStyle='#cbb98a';c.lineWidth=2;for(let i=-2;i<=2;i++){c.beginPath();c.moveTo(i*3,18);c.quadraticCurveTo(i*5,-4,i*2.6,-30);c.stroke()}c.fillStyle='#e8d8b0';c.beginPath();c.ellipse(0,-34,5,3,0,0,7);c.fill();c.restore()}
function lotusFlower(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);c.strokeStyle='#4a7a3a';c.lineWidth=4;c.beginPath();c.moveTo(0,30);c.lineTo(0,2);c.stroke();[[-1,-.5],[1,.5],[-.5,-.25],[.5,.25],[0,0]].forEach(([d,r],i)=>{c.fillStyle=i===4?'#ffc8da':(i>1?'#f8a4c0':'#f08ab0');c.beginPath();c.moveTo(0,2);c.bezierCurveTo(d*20,-4,d*22,-30,r*10,-34);c.bezierCurveTo(-d*2,-22,-d*6,-10,0,2);c.fill()});c.fillStyle='#ffe28a';c.beginPath();c.ellipse(0,-4,5,3,0,0,7);c.fill();c.restore()}
function glow2(c,x,y,r,rgb,a){const g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(1,`rgba(${rgb},0)`);c.fillStyle=g;c.beginPath();c.arc(x,y,r,0,7);c.fill()}
function gada(c,x,y){c.save();c.translate(x,y);c.strokeStyle='#8a6a2a';c.lineWidth=7;c.lineCap='round';c.beginPath();c.moveTo(0,70);c.lineTo(0,-40);c.stroke();
  const g=c.createRadialGradient(-6,-70,4,0,-66,30);g.addColorStop(0,'#fff0b0');g.addColorStop(.6,'#e0b04a');g.addColorStop(1,'#8a6a1a');c.fillStyle=g;c.beginPath();c.ellipse(0,-66,24,32,0,0,7);c.fill();
  c.strokeStyle='#8a6a1a';c.lineWidth=2.4;[-14,0,14].forEach(dy=>{c.beginPath();c.ellipse(0,-66+dy*.3,22-Math.abs(dy)*.4,6,0,0,7);c.stroke()});c.fillStyle='#e0b04a';c.beginPath();c.moveTo(-6,-96);c.lineTo(0,-114);c.lineTo(6,-96);c.fill();c.restore()}

/* ---------- the generic human ---------- */
function drawHuman(c,S,P0,o){
  const t=o.t||0,k=o.k!=null?o.k:(S.kdef||0),br=Math.sin(t*1.7)*2.2,sw=Math.sin(t*1.5)+(P0.sway||0),P=JSON.parse(JSON.stringify(P0)),bw=S.build||1;
  ['ch','nk','hd','sL','sR'].forEach(a=>{P[a][1]+=br});P.hL[1]+=br*.6;P.hR[1]+=br*.6;P.sL[0]*=bw;P.sR[0]*=bw;
  const sp=Math.max(0,(P.kR[0]-P.kL[0])/2-24),HS=S.hs||(S.female?1.06:1.14),fem=!!S.female;c.save();
  hairBack(c,S,P,t);legsS(c,S,P,sp);clothS(c,S,P,sw,sp);
  c.save();if(P.lean){c.translate(0,P.ph[1]);c.rotate(P.lean);c.translate(0,-P.ph[1])}
  if(S.arms4)extraArms(c,S,P,t);
  // torso
  const tg=c.createLinearGradient(-60,0,60,0);tg.addColorStop(0,S.skinH);tg.addColorStop(.3,S.skin);tg.addColorStop(1,S.skinD);c.fillStyle=tg;
  const w1=fem?.82:1,sx=a=>a*w1*bw;
  c.beginPath();c.moveTo(P.sL[0]-6,P.sL[1]+4);c.bezierCurveTo(sx(-52),P.sL[1]+34,sx(fem?-36:-46),P.ch[1]+64,sx(fem?-30:-36),P.ph[1]-6);c.lineTo(sx(fem?30:36),P.ph[1]-6);c.bezierCurveTo(sx(fem?36:46),P.ch[1]+64,sx(52),P.sR[1]+34,P.sR[0]+6,P.sR[1]+4);c.bezierCurveTo(30,P.nk[1]+4,-30,P.nk[1]+4,P.sL[0]-6,P.sL[1]+4);c.fill();
  if(!fem&&(S.muscle||0)>.1){c.strokeStyle=`rgba(20,24,70,${.38*S.muscle})`;c.lineWidth=2.4;c.lineCap='round';c.beginPath();c.moveTo(0,P.nk[1]+24);c.lineTo(0,P.ph[1]-18);c.stroke();
    [-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*5,P.ch[1]+2);c.bezierCurveTo(sd*26,P.ch[1]+22,sd*44,P.ch[1]+10,sd*46,P.ch[1]-14);c.stroke();if(!P.sit)for(let i=0;i<3;i++){c.beginPath();c.moveTo(sd*4,P.ph[1]-86+i*22);c.quadraticCurveTo(sd*18,P.ph[1]-80+i*22,sd*26,P.ph[1]-86+i*22);c.stroke()}});
    c.fillStyle=`rgba(255,255,255,${.12*S.muscle})`;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*22,P.ch[1]+6,20,14,sd*-.2,0,7);c.fill()})}
  if(S.upper&&S.upper.type==='choli'){c.fillStyle=S.upper.col;c.beginPath();c.moveTo(P.sL[0]+4,P.sL[1]+6);c.quadraticCurveTo(0,P.sL[1]+30,P.sR[0]-4,P.sR[1]+6);c.lineTo(sx(34),P.ch[1]+64);c.quadraticCurveTo(0,P.ch[1]+80,sx(-34),P.ch[1]+64);c.closePath();c.fill();c.strokeStyle='#b8862a';c.lineWidth=3;c.beginPath();c.moveTo(sx(-34),P.ch[1]+64);c.quadraticCurveTo(0,P.ch[1]+80,sx(34),P.ch[1]+64);c.stroke()}
  if(S.armor){c.fillStyle='#b8862a';c.beginPath();c.moveTo(sx(-40),P.ch[1]-6);c.lineTo(sx(40),P.ch[1]-6);c.lineTo(sx(34),P.ch[1]+60);c.lineTo(sx(-34),P.ch[1]+60);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.35)';c.lineWidth=2.4;[0,1,2].forEach(i=>{c.beginPath();c.moveTo(sx(-38+i*3),P.ch[1]+8+i*17);c.lineTo(sx(38-i*3),P.ch[1]+8+i*17);c.stroke()});c.fillStyle='#e8c860';c.beginPath();c.arc(0,P.ch[1]+22,6,0,7);c.fill()}
  if(S.sash&&!fem){c.strokeStyle=S.sash;c.lineWidth=13;c.lineCap='butt';c.beginPath();c.moveTo(P.sL[0]-2,P.sL[1]+2);c.quadraticCurveTo(-6,P.ch[1]+10,sx(30),P.ph[1]-4);c.stroke();c.strokeStyle='rgba(0,0,0,.16)';c.lineWidth=2;c.beginPath();c.moveTo(P.sL[0]+4,P.sL[1]+6);c.quadraticCurveTo(0,P.ch[1]+10,sx(34),P.ph[1]-2);c.stroke()}
  if(S.pallu){c.strokeStyle=S.pallu;c.lineWidth=15;c.lineCap='butt';c.beginPath();c.moveTo(P.sR[0]+2,P.sR[1]+2);c.quadraticCurveTo(10,P.ch[1]+8,sx(-30),P.ph[1]-10);c.stroke();c.strokeStyle='rgba(255,230,160,.6)';c.lineWidth=2.4;c.beginPath();c.moveTo(P.sR[0]-4,P.sR[1]+4);c.quadraticCurveTo(8,P.ch[1]+8,sx(-34),P.ph[1]-8);c.stroke()}
  if(S.beads){c.fillStyle='#6a3a20';for(let i=0;i<15;i++){const u=i/14,bx=-34+u*68,by=P.nk[1]+16+Math.sin(u*3.14)*46;c.beginPath();c.arc(bx,by,4.4,0,7);c.fill()}}
  if(S.garland){for(let i=0;i<16;i++){const u=i/15,bx=-36+u*72,by=P.nk[1]+14+Math.sin(u*3.14)*50;c.fillStyle=i%2?'#f08ab0':'#ffd0e0';c.beginPath();c.arc(bx,by,4.8,0,7);c.fill()}c.fillStyle='#e0302a';c.beginPath();c.arc(0,P.ch[1]+6,5.6,0,7);c.fill();c.fillStyle='#ffd0d0';c.beginPath();c.arc(-1.4,P.ch[1]+4.6,1.6,0,7);c.fill()}
  if(S.necklace){c.strokeStyle=S.necklace;c.lineWidth=4;c.beginPath();c.moveTo(-30,P.nk[1]+10);c.quadraticCurveTo(0,P.nk[1]+60,30,P.nk[1]+10);c.stroke();c.fillStyle=S.necklace;c.beginPath();c.arc(0,P.nk[1]+40,5,0,7);c.fill()}
  if(S.uttariya){[-1,1].forEach(sd=>{const x0=sd*(P.sR[0]*.92),y0=P.sR[1]+4,fl=Math.sin(t*1.8+sd)*5+sw*2;const gx=c.createLinearGradient(x0-12,0,x0+12,0);gx.addColorStop(0,S.uttariya);gx.addColorStop(1,shade(S.uttariya,.72));c.fillStyle=gx;c.beginPath();c.moveTo(x0-sd*8,y0);c.bezierCurveTo(x0+sd*14,y0+50,x0+sd*(34+fl),y0+110,x0+sd*(24+fl*1.6),P.ph[1]+60);c.lineTo(x0+sd*(2+fl),P.ph[1]+70);c.bezierCurveTo(x0-sd*4,y0+110,x0-sd*8,y0+50,x0+sd*6,y0);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.16)';c.lineWidth=2;c.beginPath();c.moveTo(x0+sd*2,y0+10);c.bezierCurveTo(x0+sd*12,y0+60,x0+sd*(22+fl),y0+110,x0+sd*(14+fl*1.4),P.ph[1]+62);c.stroke()})}
  // neck + head
  c.fillStyle=S.skinM;c.beginPath();c.roundRect(P.nk[0]-15,P.hd[1]+28,30,P.nk[1]-P.hd[1]+6,8);c.fill();
  if(!o.noHead){c.save();c.translate(P.hd[0],P.hd[1]+40);c.rotate(o.tilt||0);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);
  if(S.headType==='horse')horseHead(c,P.hd[0],P.hd[1]+10,k,t);
  else{drawHead(c,P.hd[0],P.hd[1],{expr:o.expr||'calm',k:k,S:S,t:t,mood:o.mood});hairFront(c,S,P.hd[0],P.hd[1]);headgear(c,S,P.hd[0],P.hd[1])}
  c.restore()}
  // arms
  const arm=(sh,hd,sd)=>limbS(c,S,sh,hd,64,62,sd,[fem?15:19,fem?11:15,fem?9:12]);
  const ef=P.ef?-1:1,aL=arm(P.sL,P.hL,-ef),aR=arm(P.sR,P.hR,ef);
  if(S.armlet){armband(c,aL,fem?13:17,S.armlet);armband(c,aR,fem?13:17,S.armlet)}
  [P.sL,P.sR].forEach((s,i)=>{c.fillStyle=S.skin;c.beginPath();c.arc(s[0],s[1],fem?16:21,0,7);c.fill();c.fillStyle='rgba(255,255,255,.14)';c.beginPath();c.arc(s[0]+(i?-4:4),s[1]-6,fem?9:12,0,7);c.fill()});
  if(o.prop==='veena'){const hx=aR.t[0],hy=aR.t[1];c.save();c.translate(hx,hy);c.rotate(-.5);c.fillStyle='#8a4a22';c.beginPath();c.ellipse(0,40,26,30,0,0,7);c.fill();c.fillStyle='#e0b04a';c.fillRect(-4,-150,8,196);c.fillStyle='#b8742e';c.beginPath();c.ellipse(0,-152,16,12,0,0,7);c.fill();c.strokeStyle='rgba(255,230,160,.8)';c.lineWidth=1.6;c.beginPath();c.moveTo(-1,-140);c.lineTo(-1,44);c.moveTo(2,-140);c.lineTo(2,44);c.stroke();c.restore()}
  const holdR=o.prop==='gada'||P.hold;if(o.prop==='gada')gada(c,aR.t[0],aR.t[1]-6);
  if(S.arms4&&!P.sit){gada(c,aR.t[0],aR.t[1]-6);lotusFlower(c,aL.t[0],aL.t[1]-16,1.05)}
  handS(c,S,aL.t,!!S.arms4);handS(c,S,aR.t,!!o.prop||!!S.arms4);
  if(S.female){c.strokeStyle='#e0b04a';c.lineWidth=3;[aL,aR].forEach(r=>{c.beginPath();c.arc(r.t[0],r.t[1]-9,9,0,7);c.stroke()})}
  c.restore();c.restore()}

/* ---------- Brahma: three faces, four arms, white beards, tall crowns, seated on a lotus ---------- */
const BRAHMA=skinSet('#d98f4e',{beard:'#f2eee6',beardLen:40,mustache:'#f2eee6',tilak:'dot',brow:'#3a2a20'});
function drawBrahmaRig(c,o){const t=o.t||0,k=o.k||0,br=Math.sin(t*1.7)*2,S=BRAHMA,sw=Math.sin(t*1.4);c.save();
  // folded legs under a red dhoti
  const g=c.createLinearGradient(-130,0,130,0);g.addColorStop(0,'#e8586a');g.addColorStop(.5,'#c83a50');g.addColorStop(1,'#8a2038');c.fillStyle=g;
  c.beginPath();c.moveTo(-40,-96);c.bezierCurveTo(-86,-100,-134,-70,-130,-16);c.bezierCurveTo(-128,0,-70,4,0,4);c.bezierCurveTo(70,4,128,0,130,-16);c.bezierCurveTo(134,-70,86,-100,40,-96);c.closePath();c.fill();
  c.strokeStyle='rgba(0,0,0,.2)';c.lineWidth=2;[-80,-40,0,40,80].forEach(x=>{c.beginPath();c.moveTo(x*.4,-92);c.quadraticCurveTo(x*1.1,-60,x*1.3,-6);c.stroke()});c.fillStyle='#e0b04a';c.fillRect(-130,-8,260,6);
  c.fillStyle=S.skin;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*26,-8,22,8,sd*-.15,0,7);c.fill()});
  // torso
  const tg=c.createLinearGradient(-54,0,54,0);tg.addColorStop(0,S.skinH);tg.addColorStop(.35,S.skin);tg.addColorStop(1,S.skinD);c.fillStyle=tg;
  c.beginPath();c.moveTo(-58,-228+br);c.bezierCurveTo(-52,-190,-42,-130,-34,-90);c.lineTo(34,-90);c.bezierCurveTo(42,-130,52,-190,58,-228+br);c.bezierCurveTo(34,-252,-34,-252,-58,-228+br);c.fill();
  c.strokeStyle='rgba(20,10,40,.3)';c.lineWidth=2.2;c.beginPath();c.moveTo(0,-226);c.lineTo(0,-100);c.stroke();
  c.strokeStyle='#f6f0e0';c.lineWidth=9;c.beginPath();c.moveTo(-50,-232+br);c.quadraticCurveTo(-6,-176,32,-98);c.stroke();
  c.fillStyle='#e0b04a';c.beginPath();c.arc(0,-168,5,0,7);c.fill();
  c.fillStyle='#d4342a';c.beginPath();c.moveTo(48,-240+br);c.bezierCurveTo(100,-230,150,-190+sw*6,170+sw*10,-120);c.bezierCurveTo(130,-150+sw*4,96,-172,40,-196+br);c.closePath();c.fill();c.fillStyle='rgba(0,0,0,.2)';c.beginPath();c.moveTo(60,-226);c.bezierCurveTo(100,-214,140,-186,164,-130);c.lineTo(150,-136);c.bezierCurveTo(124,-176,92,-198,52,-206);c.fill();
  // four arms: upper pair holds Veda + mala, lower pair kamandalu + blessing
  const arm=(sx,sy,tx,ty,sd,w)=>{const r=limbS(c,S,[sx,sy],[tx,ty],62,60,sd,w);armband(c,r,13,'#e0b04a');return r};
  const uL=arm(-52,-232+br,-150,-300+br,-1,[15,12,10]),uR=arm(52,-232+br,150,-300+br,1,[15,12,10]),lL=arm(-48,-212+br,-118,-150,-1,[16,13,11]),lR=arm(48,-212+br,118,-150,1,[16,13,11]);
  // props
  c.save();c.translate(uL.t[0]-6,uL.t[1]-12);c.fillStyle='#f2e8c8';c.fillRect(-26,-10,52,22);c.strokeStyle='#8a6a2a';c.lineWidth=3;c.strokeRect(-26,-10,52,22);c.strokeStyle='#b8a070';c.lineWidth=1.6;[-14,0,14].forEach(x=>{c.beginPath();c.moveTo(x,-8);c.lineTo(x,10);c.stroke()});c.restore();
  c.strokeStyle='#6a3a20';c.lineWidth=4;c.setLineDash([2,6]);c.beginPath();c.arc(uR.t[0]+12,uR.t[1]+4,20,0,7);c.stroke();c.setLineDash([]);c.fillStyle='#6a3a20';for(let i=0;i<10;i++){const a=i*.628;c.beginPath();c.arc(uR.t[0]+12+Math.cos(a)*20,uR.t[1]+4+Math.sin(a)*20,4,0,7);c.fill()}
  c.fillStyle='#b8742e';c.beginPath();c.ellipse(lL.t[0]-8,lL.t[1]-6,16,20,0,0,7);c.fill();c.fillStyle='#8a5a22';c.fillRect(lL.t[0]-14,lL.t[1]-30,12,12);
  [uL,uR,lL,lR].forEach((r,i)=>handS(c,S,r.t,i<3));
  [[-52,-232],[52,-232]].forEach(([x,y])=>{c.fillStyle=S.skin;c.beginPath();c.arc(x,y+br,19,0,7);c.fill()});
  // three heads: the two side faces sit behind, the front face in front
  const head=(x,y,s,dark)=>{c.save();c.translate(x,y);c.scale(s,s);if(dark){c.filter='brightness(.8)'}drawHead(c,0,0,{expr:o.expr||'calm',k:k,S:S,t:t});
    c.fillStyle='#e6b84a';c.beginPath();c.moveTo(-26,-24);c.lineTo(-22,-52);c.lineTo(-10,-58);c.lineTo(-5,-96);c.lineTo(0,-128);c.lineTo(5,-96);c.lineTo(10,-58);c.lineTo(22,-52);c.lineTo(26,-24);c.closePath();c.fill();c.fillStyle='#c4882a';c.fillRect(-26,-30,52,7);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-40,4,0,7);c.fill();c.filter='none';c.restore()};
  c.fillStyle=S.skinM;c.fillRect(-14,-290+br,28,50);
  const H=o.hd,ez=v=>v*v*(3-2*v);
  if(!H){head(0,-352+br,.7,true);head(-62,-286+br,.84,true);head(62,-286+br,.84,true);head(0,-292+br,1.04,false)}   // four-faced: back face peeks above, two side faces, front face
  else{ // faces sprout one by one: back, left, right, then a fifth on top; the front face is always there
    if(H.b>.01)head(0,-300+br,.9*ez(H.b),true);
    if(H.l>.01)head(-22-40*ez(H.l),-286+br,.84*ez(H.l),true);
    if(H.r>.01)head(22+40*ez(H.r),-286+br,.84*ez(H.r),true);
    head(0,-292+br,1.04,false);
    if(H.t>.01)head(0,-396+br-20*(1-ez(H.t)),.74*ez(H.t),false)}
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
  c.beginPath();c.moveTo(up[0][0],up[0][1]);for(let k=1;k<up.length;k++){const m=[(up[k-1][0]+up[k][0])/2,(up[k-1][1]+up[k][1])/2];c.quadraticCurveTo(up[k-1][0],up[k-1][1],m[0],m[1])}c.lineTo(up[up.length-1][0],up[up.length-1][1]);c.lineTo(lo[lo.length-1][0],lo[lo.length-1][1]);for(let k=lo.length-2;k>=0;k--){const m=[(lo[k+1][0]+lo[k][0])/2,(lo[k+1][1]+lo[k][1])/2];c.quadraticCurveTo(lo[k+1][0],lo[k+1][1],m[0],m[1])}c.closePath();c.fill();
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

/*V3BEGIN*/
/* ===================== v3 heroes: vishnu3, brahma3, narada3 =====================
   A separate drawing path (head3 / hand3 / drawHero3). Nothing below runs for any older cast member.
   Face: per-character spec S.f3 (eye shape, lids, brows, nose, jaw, lips, age) driven by mood {smile,sad,surp,mouth,lx,ly,blink} + k (anger).
   Hands: real gestures (relax, open, point, fist, grip, abhaya blessing, namaste, holding props).
   Gestures come from the pose: poseOf() attaches P.g={L,R} for these three only. */
const V3=new Set(['vishnu3','brahma3','narada3']);
const rgbaH=(h,a)=>{const v=hexRgb(h);return `rgba(${v[0]},${v[1]},${v[2]},${a})`};
const mixc=(a,b,u)=>{const A=hexRgb(a),B=hexRgb(b);return toHex(A.map((v,i)=>v+(B[i]-v)*u))};
const PZ3={bstand:{hL:[-104,-286],hR:[122,-380]},nstand:{hL:[-14,-306],hR:[96,-440],veena:'play',eL:1},bless:{hR:[108,-404]},
  vnam:{hL:[-7,-358],hR:[7,-358]},vbow:{hL:[-7,-356],hR:[7,-356],lean:.34}};
const G3={vishnu3:{stand:['lotus','gada']},brahma3:{stand:['kamandalu','abhaya']},narada3:{stand:['pluck','veena']}};
const G3D={namaste:['namaste','namaste'],plead:['namaste','namaste'],bow:['namaste','namaste'],sitpray:['namaste','namaste'],open:['open','open'],cup:['open','open'],point:['relax','point'],
  raise:['relax','abhaya'],bless:['relax','abhaya'],hold:['relax','grip'],fist:['fist','fist'],flee:['open','open'],lunge:['fist','point'],sit:['relax','relax']};
function poseOf3(n,who){if(n&&typeof n==='object')return n;n=n||'stand';
  const base=n==='stand'?(who==='vishnu3'?'vstand':who==='brahma3'?'bstand':'nstand'):(n==='namaste'?'vnam':n==='bow'?'vbow':n);
  const P=poseOf0(PZ[base]?base:(PZ3[base]?'stand':n));Object.assign(P,JSON.parse(JSON.stringify(PZ3[base]||{})));
  const g=(G3[who]||{})[n]||G3D[n]||['relax','relax'];P.g={L:g[0],R:g[1]};if(!P.veena)P.veena='back';if(P.eL==null)P.eL=0;return P}

/* ---------- capsule path (finger/limb with an outline) ---------- */
function capP(c,a,b,ra,rb){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d,an=Math.atan2(ny,nx);c.beginPath();c.moveTo(a[0]+nx*ra,a[1]+ny*ra);c.lineTo(b[0]+nx*rb,b[1]+ny*rb);c.arc(b[0],b[1],rb,an,an-Math.PI,true);c.lineTo(a[0]-nx*ra,a[1]-ny*ra);c.arc(a[0],a[1],ra,an+Math.PI,an,true);c.closePath()}

/* ---------- the face ---------- */
function head3(c,S,o){const F=S.f3,M=o.mood||{},t=o.t||0,k=clamp(o.k||0,0,1),sad=clamp(M.sad||0,0,1),sp=clamp(M.surp||0,0,1),mo=clamp(M.mouth||0,0,1);
  const lx=clamp(M.lx||0,-1,1),ly=clamp(M.ly||0,-1,1),yw=o.yaw!=null?o.yaw:lx*.2;
  const bl=Math.max(M.blink||0,((t*.29+F.blinkPh)%1)<.022?1:0,o.expr==='closed'?1:0);
  const sm=clamp((M.smile||0)+F.smile0*(1-k)*(1-sad)*(1-sp*.7),0,1.3),smk=(F.smirk||0)*(1-k)*(1-sad)*(1-sp);
  const W=F.faceW,J=F.jaw,C=F.chin,X=x=>x*(1-.2*Math.abs(yw))+yw*11,cx=yw*8;c.save();
  // ears (behind the face)
  [-1,1].forEach(sd=>{if(sd*yw>.42)return;const ex=sd*(W+.5)+yw*(sd<0?9:3);c.fillStyle=S.skinM;c.beginPath();c.ellipse(ex,3,7.5,13.5,sd*-.12,0,7);c.fill();c.strokeStyle=rgbaH(S.skinD,.7);c.lineWidth=1.3;c.stroke();
    c.strokeStyle=rgbaH(S.skinD,.6);c.lineWidth=1.5;c.beginPath();c.arc(ex+sd*1,2,5,-1.4,1.4*1);c.stroke()});
  const face=()=>{c.beginPath();c.moveTo(-W,-10);c.bezierCurveTo(-W-1,-50,W+1,-50,W,-10);c.bezierCurveTo(W+1,12,J+7+cx*.4,C-14,J*.42+cx,C-1.5);c.quadraticCurveTo(cx,C+2.5,-J*.42+cx,C-1.5);c.bezierCurveTo(-J-7+cx*.4,C-14,-W-1,12,-W,-10);c.closePath()};
  face();let g=c.createRadialGradient(-12+yw*8,-6,4,0,6,64);g.addColorStop(0,S.skinH);g.addColorStop(.5,S.skin);g.addColorStop(1,S.skinM);c.fillStyle=g;c.fill();
  c.save();face();c.clip();
  g=c.createLinearGradient(W*.15+yw*8,0,W+2,0);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,rgbaH(S.skinD,.5));c.fillStyle=g;c.fillRect(-W,-60,2*W+6,130);
  c.fillStyle=rgbaH(S.skinD,.32);c.beginPath();c.ellipse(cx,C+9,J*.95,12,0,0,7);c.fill();
  c.fillStyle=rgbaH(S.skinD,.13);[-1,1].forEach(sd=>{c.beginPath();c.ellipse(X(sd*F.eyeX),F.eyeY-3,F.eyeW+5,8.5,0,0,7);c.fill()});
  [-1,1].forEach(sd=>{const bx=X(sd*17.5),by=18-sm*2.8,bg=c.createRadialGradient(bx,by,0,bx,by,13);bg.addColorStop(0,`rgba(${F.blush},${.18+sm*.16})`);bg.addColorStop(1,`rgba(${F.blush},0)`);c.fillStyle=bg;c.beginPath();c.arc(bx,by,13,0,7);c.fill();
    c.fillStyle=rgbaH(S.skinH,.16+sm*.14);c.beginPath();c.ellipse(bx-2,by-3,6,3.4,-.3,0,7);c.fill()});
  c.fillStyle=rgbaH(S.skinH,.3);c.beginPath();c.ellipse(X(-7),-24,13,6,-.2,0,7);c.fill();
  c.restore();c.strokeStyle=rgbaH(S.skinD,.75);c.lineWidth=1.4;face();c.stroke();
  // forehead mark
  const tx=X(0);if(F.tilak==='vaishnava'){c.strokeStyle='#f6f0e2';c.lineWidth=2.6;c.lineCap='round';c.beginPath();c.moveTo(tx-5.5,-34);c.lineTo(tx-5,-12);c.quadraticCurveTo(tx,-6,tx+5,-12);c.lineTo(tx+5.5,-34);c.stroke();c.fillStyle='#d8262a';c.beginPath();c.moveTo(tx,-34);c.quadraticCurveTo(tx+2.2,-22,tx,-11);c.quadraticCurveTo(tx-2.2,-22,tx,-34);c.fill()}
  if(F.tilak==='flame'){c.fillStyle='#d8402a';c.beginPath();c.moveTo(tx,-33);c.quadraticCurveTo(tx+3.6,-20,tx,-12);c.quadraticCurveTo(tx-3.6,-20,tx,-33);c.fill();c.fillStyle='#f0c040';c.beginPath();c.arc(tx,-10.5,1.8,0,7);c.fill()}
  // brows
  [-1,1].forEach(sd=>{const asy=(F.asym||0)*(sd<0?1:0)*(1-k)*(1-sad),th=F.browTh*(1+k*.35);
    const i=[X(sd*(F.browIn-k*1.6)),F.browY+3-sp*7-sad*7+k*5-asy],a=[X(sd*(F.eyeX+1)),F.browY-F.arch-sp*7.5-sad*1.5+k*1.5-asy],e=[X(sd*(F.eyeX+F.eyeW+4.5)),F.browY+2.5-sp*5+sad*4.5-k*1.2-asy*.5];
    c.fillStyle=F.brow;c.beginPath();c.moveTo(i[0],i[1]-th*.5);c.quadraticCurveTo(a[0],a[1]-th*.4,e[0],e[1]);c.quadraticCurveTo(a[0],a[1]+th*.6,i[0],i[1]+th*.5);c.closePath();c.fill();
    if(F.bushy){c.strokeStyle=F.browEdge;c.lineWidth=1;c.stroke();c.strokeStyle=F.brow;c.lineWidth=1.6;c.lineCap='round';for(let q=0;q<4;q++){const u=.3+q*.2,px=lerp(i[0],e[0],u),py=lerp(i[1],e[1],u)-F.arch*.6;c.beginPath();c.moveTo(px,py+1);c.quadraticCurveTo(px+sd*3,py+4,px+sd*4.5,py+7);c.stroke()}}});
  // eyes
  [-1,1].forEach(sd=>{const far=sd*yw>0?Math.abs(yw):0,cs=1-far*.5,ex=X(sd*F.eyeX),ey=F.eyeY,ew=F.eyeW*cs;
    const ix=ex-sd*ew,ox=ex+sd*ew,iy=ey+1,oy=ey-F.lift+sad*1.8,h=F.eyeH*(1+sp*.5)*(1-sm*.1);
    const uc=[ex-sd*ew*.12,ey-h*1.9],lc=[ex+sd*ew*.08,ey+h*1.05*(1-sm*.42)];
    const lid=bl>.5?1:clamp(F.lid-sp*.45+sad*.2+k*.14+sm*.1,0,.92);
    if(F.age){c.strokeStyle=rgbaH(S.skinD,.55);c.lineWidth=1.2;c.beginPath();c.moveTo(ix+sd*2,iy+4.5);c.quadraticCurveTo(ex,ey+h*1.05+6,ox,oy+4);c.stroke();
      for(let q=0;q<3;q++){c.beginPath();c.moveTo(ox+sd*3,oy-1+q*3);c.lineTo(ox+sd*8,oy-3+q*4.2);c.stroke()}}
    const crease=(off)=>{c.strokeStyle=rgbaH(S.skinD,.6);c.lineWidth=1.3;c.lineCap='round';c.beginPath();c.moveTo(ix+sd*1.5,iy-4);c.quadraticCurveTo(uc[0],uc[1]-off,ox+sd*1.5,oy-3.5);c.stroke()};
    if(lid>=.98){c.strokeStyle=F.lash;c.lineWidth=2.5;c.lineCap='round';c.beginPath();c.moveTo(ix,iy);c.quadraticCurveTo(ex,ey+(sm>.5?-3.5:3),ox,oy);c.stroke();crease(1.5);return}
    if(k>.05){const eg=c.createRadialGradient(ex,ey-2,1,ex,ey-2,20);eg.addColorStop(0,`rgba(255,70,40,${.38*k})`);eg.addColorStop(1,'rgba(255,70,40,0)');c.fillStyle=eg;c.beginPath();c.arc(ex,ey-2,20,0,7);c.fill()}
    const eyeP=()=>{c.beginPath();c.moveTo(ix,iy);c.quadraticCurveTo(uc[0],uc[1],ox,oy);c.quadraticCurveTo(lc[0],lc[1],ix,iy);c.closePath()};
    eyeP();c.fillStyle=F.white||'#f7f1e8';c.fill();c.save();eyeP();c.clip();
    c.fillStyle='rgba(60,40,60,.18)';c.fillRect(ex-ew-2,ey-h*2,2*ew+4,h*.9);
    const ir=F.irisR,irx=ex+lx*ew*.42,iry=ey-h*.22+ly*h*.55,ic=k>.25?mixc(F.iris,'#d8281a',k):F.iris;
    const ig=c.createRadialGradient(irx,iry+ir*.3,0,irx,iry,ir);ig.addColorStop(0,shade(ic,1.7));ig.addColorStop(.6,ic);ig.addColorStop(1,shade(ic,.45));c.fillStyle=ig;c.beginPath();c.ellipse(irx,iry,ir*(.75+.25*cs),ir,0,0,7);c.fill();
    c.fillStyle='#050306';c.beginPath();c.ellipse(irx,iry,ir*.42*(.75+.25*cs),ir*.46,0,0,7);c.fill();
    c.fillStyle='#fff';c.beginPath();c.arc(irx-ir*.36,iry-ir*.38,ir*(F.twinkle?.38:.3),0,7);c.fill();c.globalAlpha=.8;c.beginPath();c.arc(irx+ir*.32,iry+ir*.3,ir*(F.twinkle?.2:.14),0,7);c.fill();c.globalAlpha=1;
    const uy=uc[1]+lid*(lc[1]-uc[1])*.9;c.fillStyle=F.lidCol||S.skinM;c.beginPath();c.moveTo(ix-2,iy);c.quadraticCurveTo(uc[0],uy,ox+sd*2,oy);c.lineTo(ox+sd*2,ey-h*2.4);c.lineTo(ix-sd*2,ey-h*2.4);c.closePath();c.fill();
    c.strokeStyle='rgba(20,10,20,.28)';c.lineWidth=3;c.beginPath();c.moveTo(ix,iy+.6);c.quadraticCurveTo(uc[0],uy+1.4,ox,oy+.6);c.stroke();c.restore();
    c.strokeStyle=F.lash;c.lineWidth=2.6;c.lineCap='round';c.beginPath();c.moveTo(ix,iy);c.quadraticCurveTo(uc[0],uy,ox,oy);if(F.wing)c.quadraticCurveTo(ox+sd*F.wing*.7,oy-F.wing*.1,ox+sd*F.wing*1.3,oy-F.wing*.75);c.stroke();
    c.strokeStyle=rgbaH(F.lash,.5);c.lineWidth=1.2;c.beginPath();c.moveTo(ix+sd*1.5,iy+.8);c.quadraticCurveTo(lc[0],lc[1],ox,oy+.4);c.stroke();
    crease(4.5+(1-lid)*1.5);
    if(sm>.95&&F.age){c.strokeStyle=rgbaH(S.skinD,(sm-.95)*.8);c.lineWidth=1.1;c.beginPath();c.moveTo(ex-sd*ew*.4,ey+h*1.1+3);c.quadraticCurveTo(ex,ey+h*1.1+5,ex+sd*ew*.6,ey+h*.9+3);c.stroke()}});
  // nose
  const N=F.nose,nx=X(0)+yw*5,nt=N.tip;
  c.strokeStyle=rgbaH(S.skinH,.6);c.lineWidth=2.2;c.lineCap='round';c.beginPath();c.moveTo(nx-2.2,3);c.quadraticCurveTo(nx-2.8-(N.hook||0)*.4,12,nx-1.6,nt-5);c.stroke();
  c.fillStyle=rgbaH(S.skinD,.4);c.beginPath();c.moveTo(nx+2,-1);c.quadraticCurveTo(nx+3.5+(N.hook||0),nt*.5,nx+N.w*.75,nt-1.5);c.quadraticCurveTo(nx+3,nt+1.5,nx+.8,nt-4);c.quadraticCurveTo(nx+1.6,nt*.5,nx+2,-1);c.fill();
  c.strokeStyle=rgbaH(S.skinD,.9);c.lineWidth=1.7;c.beginPath();c.moveTo(nx-N.w,nt-1.2);c.quadraticCurveTo(nx-N.w-1.8,nt+3.6,nx-N.w*.4,nt+3.2);c.moveTo(nx+N.w,nt-1.2);c.quadraticCurveTo(nx+N.w+1.8,nt+3.6,nx+N.w*.4,nt+3.2);c.stroke();
  c.lineWidth=1.4;c.beginPath();c.moveTo(nx-N.w*.42,nt+3.6);c.quadraticCurveTo(nx,nt+5.2-(N.up||0),nx+N.w*.42,nt+3.6);c.stroke();
  c.fillStyle=rgbaH(S.skinD,.95);[-1,1].forEach(sd=>{c.beginPath();c.ellipse(nx+sd*N.w*.45,nt+2.4,1.9,1.1,sd*.3,0,7);c.fill()});
  c.fillStyle=rgbaH(S.skinH,.55);c.beginPath();c.ellipse(nx-1,nt-1.2-(N.up||0),2.6,1.9,0,0,7);c.fill();
  // mouth
  const my=F.mouthY,mx=X(0)+yw*4,mw=F.mouthW*(1+sm*.22-sp*.38),cyL=my-sm*3.6+sad*3.8+k*2.6-smk*.4,cyR=my-sm*3.6+sad*3.8+k*2.6-smk*2.8;
  const op=Math.max(mo*7.5,sp*7,sm>1.05?(sm-1.05)*16:0),lc2=my+sm*4.6-sad*2.6-k*3.4-smk*.6;
  if(sm>.6||F.age){c.strokeStyle=rgbaH(S.skinD,F.age?.4:(sm-.6)*.35);c.lineWidth=1.3;[-1,1].forEach(sd=>{c.beginPath();c.moveTo(nx+sd*(N.w+3),nt+1);c.quadraticCurveTo(mx+sd*(mw+5),my-4,mx+sd*(mw+3.5),(sd<0?cyL:cyR)+2.5);c.stroke()})}
  if(op<1.2){c.fillStyle=F.lip;c.beginPath();c.moveTo(mx-mw,cyL);c.quadraticCurveTo(mx,my+5.6+sm*1.2-k*1.4,mx+mw,cyR);c.quadraticCurveTo(mx,lc2,mx-mw,cyL);c.fill();
    c.fillStyle=shade(F.lip,.82);c.beginPath();c.moveTo(mx-mw,cyL);c.quadraticCurveTo(mx-mw*.45,my-3.4,mx-1.3,my-2.4);c.lineTo(mx,my-1.6);c.lineTo(mx+1.3,my-2.4);c.quadraticCurveTo(mx+mw*.45,my-3.4,mx+mw,cyR);c.quadraticCurveTo(mx,lc2,mx-mw,cyL);c.fill();
    c.strokeStyle=F.lipD;c.lineWidth=1.9;c.lineCap='round';c.beginPath();c.moveTo(mx-mw-.5,cyL);c.quadraticCurveTo(mx,lc2,mx+mw+.5,cyR);c.stroke();
    if(sm>.15){c.lineWidth=1.2;c.strokeStyle=rgbaH(F.lipD,sm*.8);[[-1,cyL],[1,cyR]].forEach(([sd,y])=>{c.beginPath();c.moveTo(mx+sd*(mw-.5),y-1.4);c.quadraticCurveTo(mx+sd*(mw+2.2),y,mx+sd*(mw+.5),y+1.8);c.stroke()})}
    c.fillStyle='rgba(255,255,255,.22)';c.beginPath();c.ellipse(mx-1,my+3.4,mw*.34,1.1,0,0,7);c.fill()}
  else{const mp=()=>{c.beginPath();c.moveTo(mx-mw,cyL);c.quadraticCurveTo(mx,my-1.8+sm*1.4,mx+mw,cyR);c.quadraticCurveTo(mx,my+op*1.55+sm*2.4,mx-mw,cyL);c.closePath()};
    mp();c.fillStyle='#3a0c16';c.fill();c.save();mp();c.clip();if(sp<.6||mo>.3||sm>.3){c.fillStyle='#f3ece2';c.fillRect(mx-mw,my-5,2*mw,3.6+op*.12)}c.fillStyle='#b4485a';c.beginPath();c.ellipse(mx,my+op*1.35,mw*.62,op*.42,0,0,7);c.fill();c.restore();
    c.strokeStyle=shade(F.lip,.85);c.lineWidth=2.3;c.lineCap='round';c.beginPath();c.moveTo(mx-mw,cyL);c.quadraticCurveTo(mx,my-1.8+sm*1.4,mx+mw,cyR);c.stroke();
    c.strokeStyle=F.lip;c.lineWidth=3.2;c.beginPath();c.moveTo(mx-mw*.8,cyL+1.2);c.quadraticCurveTo(mx,my+op*1.55+sm*2.4+1.4,mx+mw*.8,cyR+1.2);c.stroke()}
  c.fillStyle=rgbaH(S.skinH,.22);c.beginPath();c.ellipse(mx,my+12+op*.6,5,2.4,0,0,7);c.fill();
  // beard + moustache (drawn around the mouth so the expression still reads)
  if(F.beard){const B=F.beard,swb=Math.sin(t*1.3)*3,bL=F.beardLen,ow=mw+5;
    const bp=()=>{c.beginPath();c.moveTo(-W+1,-4);c.bezierCurveTo(-W-5,18,-J-12,C-4,-J*.7,C+bL*.55);c.quadraticCurveTo(-8+swb,C+bL,swb*1.4,C+bL+8);c.quadraticCurveTo(8+swb,C+bL,J*.7,C+bL*.55);c.bezierCurveTo(J+12,C-4,W+5,18,W-1,-4);
      c.lineTo(W-5,4);c.quadraticCurveTo(W-6,22,mx+ow+3,my+3);c.quadraticCurveTo(mx,my+11+op*1.6,mx-ow-3,my+3);c.quadraticCurveTo(-W+6,22,-W+5,4);c.closePath()};
    bp();g=c.createLinearGradient(0,0,0,C+bL);g.addColorStop(0,B);g.addColorStop(1,shade(B,.82));c.fillStyle=g;c.fill();c.strokeStyle=F.browEdge;c.lineWidth=1;c.stroke();
    c.save();bp();c.clip();c.strokeStyle='rgba(120,110,100,.42)';c.lineWidth=1.3;for(let q=-6;q<=6;q++){c.beginPath();c.moveTo(q*5.5,my+6);c.bezierCurveTo(q*6.5,C+10,q*4+swb*.5,C+bL*.6,q*2+swb,C+bL+4);c.stroke()}
    c.fillStyle='rgba(255,255,255,.35)';c.beginPath();c.ellipse(-14,C+10,4,16,.25,0,7);c.fill();c.restore();
    [-1,1].forEach(sd=>{c.fillStyle=B;c.beginPath();c.moveTo(mx,nt+5);c.bezierCurveTo(mx+sd*(mw*.6),nt+3,mx+sd*(mw+5),my-5,mx+sd*(mw+7),my+9+sad*2);c.quadraticCurveTo(mx+sd*(mw+1),my-1.5,mx+sd*1,my-2.6);c.closePath();c.fill();c.strokeStyle=F.browEdge;c.lineWidth=.9;c.stroke();
      c.strokeStyle='rgba(120,110,100,.45)';c.lineWidth=1;c.beginPath();c.moveTo(mx+sd*3,nt+6);c.quadraticCurveTo(mx+sd*(mw+2),my-3,mx+sd*(mw+5),my+6);c.stroke()})}
  // earrings
  [-1,1].forEach(sd=>{if(sd*yw>.42)return;const ex=sd*(W+1)+yw*(sd<0?9:3),ey=17,sw=Math.sin(t*1.9+sd)*.14;c.save();c.translate(ex,ey);c.rotate(sw);
    if(F.ear==='makara'){g=c.createLinearGradient(-8,0,8,0);g.addColorStop(0,'#fff1b0');g.addColorStop(.5,'#e4b244');g.addColorStop(1,'#9a6a18');c.fillStyle=g;c.beginPath();c.arc(0,9,8.5,0,7);c.fill();c.strokeStyle='#7a5010';c.lineWidth=1;c.stroke();
      c.strokeStyle='#a87018';c.lineWidth=1;c.beginPath();c.arc(0,9,5.6,0,7);c.stroke();gem(c,0,9,3,'#d02a2a');c.fillStyle='#e4b244';c.beginPath();c.moveTo(-3,17);c.lineTo(3,17);c.lineTo(0,27);c.closePath();c.fill();gem(c,0,27,2.2,'#2aa070')}
    else if(F.ear==='hoop'){c.strokeStyle='#e0b04a';c.lineWidth=3;c.beginPath();c.arc(0,9,8,0,7);c.stroke();c.strokeStyle='#8a6018';c.lineWidth=.8;c.stroke();c.fillStyle='#c82a2a';c.beginPath();c.arc(0,17,2.6,0,7);c.fill()}
    else{c.fillStyle='#6a3418';c.beginPath();c.arc(0,4,3.2,0,7);c.fill();c.strokeStyle='#e0b04a';c.lineWidth=1.8;c.beginPath();c.arc(0,9,4.5,0,7);c.stroke()}
    c.restore()});
  c.restore()}

/* ---------- hair, crowns ---------- */
function goldG(c,x0,x1){const g=c.createLinearGradient(x0,0,x1,0);g.addColorStop(0,'#fff2b8');g.addColorStop(.35,'#eec258');g.addColorStop(.75,'#c99230');g.addColorStop(1,'#8e5e16');return g}
function gem(c,x,y,r,col){c.fillStyle=col;c.beginPath();c.arc(x,y,r,0,7);c.fill();c.fillStyle='rgba(255,255,255,.55)';c.beginPath();c.arc(x-r*.35,y-r*.35,r*.35,0,7);c.fill();c.strokeStyle='rgba(90,50,0,.6)';c.lineWidth=.8;c.beginPath();c.arc(x,y,r,0,7);c.stroke()}
function hairBack3(c,S,t,who){const sw=Math.sin(t*1.4)*2.5;
  if(who==='vishnu3'){c.fillStyle='#0c0c1a';c.beginPath();c.ellipse(0,-6,40,36,0,0,7);c.fill();
    [-1,1].forEach(sd=>{for(let i=3;i>=0;i--){const x0=sd*(18+i*6),x1=sd*(40+i*9)+sw*(1+i*.3),y1=46+i*10,w=8-i*.6;c.fillStyle=i%2?'#14142a':'#0c0c1a';c.beginPath();c.moveTo(x0-w,0);c.bezierCurveTo(x0+sd*14-w,20,x1-sd*6-w,y1-20,x1-w*.6,y1);c.arc(x1,y1,w*.9,Math.PI,0,sd<0);c.bezierCurveTo(x1-sd*4+w,y1-22,x0+sd*16+w,18,x0+w,0);c.closePath();c.fill();
      c.strokeStyle='rgba(120,130,210,.3)';c.lineWidth=1.4;c.beginPath();c.moveTo(x0,4);c.bezierCurveTo(x0+sd*14,22,x1-sd*6,y1-18,x1,y1-2);c.stroke()}})}
  if(who==='brahma3'){c.fillStyle='#e4e0d8';c.beginPath();c.moveTo(-34,-20);c.bezierCurveTo(-56,10,-58+sw,70,-46+sw,110);c.lineTo(46+sw,110);c.bezierCurveTo(58+sw,70,56,10,34,-20);c.closePath();c.fill();c.strokeStyle='rgba(140,130,120,.4)';c.lineWidth=1.4;for(let i=-4;i<=4;i++){c.beginPath();c.moveTo(i*8,-10);c.bezierCurveTo(i*12,30,i*11+sw,70,i*10+sw,108);c.stroke()}}
  if(who==='narada3'){c.fillStyle='#0e0a0a';c.beginPath();c.moveTo(-31,-10);c.bezierCurveTo(-40,10,-38,26,-28,34);c.lineTo(28,34);c.bezierCurveTo(38,26,40,10,31,-10);c.closePath();c.fill()}}
function hairFront3(c,S,t,who){const F=S.f3,sw=Math.sin(t*1.6)*2;
  if(who==='vishnu3'){c.fillStyle='#0c0c1a';c.beginPath();c.moveTo(-36,-6);c.bezierCurveTo(-40,-40,40,-40,36,-6);c.bezierCurveTo(30,-22,14,-26,0,-24);c.bezierCurveTo(-14,-26,-30,-22,-36,-6);c.fill();
    [-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*33,-18);c.bezierCurveTo(sd*40,-6,sd*41,6,sd*37,12);c.bezierCurveTo(sd*33,8,sd*35,-4,sd*30,-12);c.fill();c.beginPath();c.arc(sd*36.5,12,3.4,0,7);c.fill()})}
  if(who==='brahma3'){c.fillStyle='#ece8e0';c.beginPath();c.moveTo(-36,-4);c.bezierCurveTo(-40,-40,40,-40,36,-4);c.bezierCurveTo(30,-22,14,-27,0,-26);c.bezierCurveTo(-14,-27,-30,-22,-36,-4);c.fill();c.strokeStyle='#a8a094';c.lineWidth=1;c.stroke()}
  if(who==='narada3'){c.fillStyle='#0e0a0a';c.beginPath();c.moveTo(-33,-2);c.bezierCurveTo(-38,-52,38,-52,33,-2);c.bezierCurveTo(30,-20,24,-28,10,-30);c.quadraticCurveTo(0,-26,-10,-30);c.bezierCurveTo(-24,-28,-30,-20,-33,-2);c.fill();
    c.strokeStyle='rgba(160,140,130,.3)';c.lineWidth=1.4;[-16,-6,6,16].forEach(x=>{c.beginPath();c.moveTo(x*.6,-30);c.quadraticCurveTo(x,-40,x*.3,-48);c.stroke()});
    // shikha topknot with a rudraksha strand wound round it, and a loose lock that sways
    c.fillStyle='#0e0a0a';c.beginPath();c.ellipse(2,-50,16,15,.1,0,7);c.fill();c.beginPath();c.ellipse(4,-65,8.5,8.5,.2,0,7);c.fill();
    c.strokeStyle='#0e0a0a';c.lineWidth=4;c.lineCap='round';c.beginPath();c.moveTo(12,-58);c.bezierCurveTo(26,-62,30+sw*2,-48,27+sw*3,-32);c.stroke();
    c.fillStyle='rgba(170,150,140,.35)';c.beginPath();c.ellipse(-4,-55,5,7,-.4,0,7);c.fill();
    c.fillStyle='#7a3c1c';for(let i=0;i<9;i++){const a=-2.6+i*.55;c.beginPath();c.arc(2+Math.cos(a)*16,-43+Math.sin(a)*4.5,2.6,0,7);c.fill()}
    c.fillStyle='#f4f0e6';c.beginPath();c.arc(-13,-53,3.4,0,7);c.fill();c.fillStyle='#f0c040';c.beginPath();c.arc(-13,-53,1.4,0,7);c.fill()}}
function crownV3(c,t){c.save();const sw=Math.sin(t*1.7)*.12;
  // pearl strings hanging at the sides (sway)
  [-1,1].forEach(sd=>{c.save();c.translate(sd*35,-24);c.rotate(sw*sd*.5+sw);c.fillStyle='#f4eee0';for(let i=0;i<7;i++){c.beginPath();c.arc(0,i*4.6,1.9,0,7);c.fill()}c.fillStyle='#d02a2a';c.beginPath();c.arc(0,33,2.6,0,7);c.fill();c.restore()});
  // side wings
  [-1,1].forEach(sd=>{c.fillStyle=goldG(c,-44,44);c.beginPath();c.moveTo(sd*24,-30);c.lineTo(sd*24,-50);c.quadraticCurveTo(sd*40,-62,sd*46,-46);c.quadraticCurveTo(sd*48,-34,sd*36,-28);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1;c.stroke();c.strokeStyle='rgba(122,80,16,.6)';for(let q=0;q<3;q++){c.beginPath();c.moveTo(sd*27,-34);c.lineTo(sd*(38+q*3),-56+q*9);c.stroke()}gem(c,sd*30,-40,2.6,'#2a9a6a')});
  // tall kirita: tapering tiers
  c.fillStyle=goldG(c,-28,28);c.beginPath();c.moveTo(-28,-30);c.bezierCurveTo(-26,-60,-21,-90,-17,-112);c.lineTo(17,-112);c.bezierCurveTo(21,-90,26,-60,28,-30);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.3;c.stroke();
  c.strokeStyle='rgba(120,70,10,.55)';c.lineWidth=1;for(let x=-16;x<=16;x+=8){c.beginPath();c.moveTo(x*1.4,-36);c.lineTo(x*.95,-110);c.stroke()}
  [-58,-82,-104].forEach((y,i)=>{const w=27-i*3.6-(y+58)*-.02;c.fillStyle=goldG(c,-w,w);c.beginPath();c.roundRect(-w-1,y-4,2*w+2,7,3);c.fill();c.strokeStyle='#7a5010';c.lineWidth=.9;c.stroke();for(let q=-2;q<=2;q++)gem(c,q*w*.4,y-.5,1.7,q%2?'#2a9a6a':'#d02a2a')});
  [-1,1].forEach(sd=>{c.strokeStyle='#a87018';c.lineWidth=1.2;for(let i=0;i<3;i++){c.beginPath();c.arc(sd*(10+i*4.5),-70+i*7,3.4,0,Math.PI);c.stroke()}});
  // finial
  c.fillStyle=goldG(c,-16,16);c.beginPath();c.moveTo(-16,-112);c.bezierCurveTo(-18,-126,-7,-130,0,-146);c.bezierCurveTo(7,-130,18,-126,16,-112);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.2;c.stroke();gem(c,0,-124,4.2,'#d02a2a');
  // diadem band across the forehead
  c.fillStyle=goldG(c,-36,36);c.beginPath();c.moveTo(-36,-18);c.quadraticCurveTo(0,-31,36,-18);c.lineTo(36,-28);c.quadraticCurveTo(0,-41,-36,-28);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.2;c.stroke();
  [-24,-12,12,24].forEach((x,i)=>gem(c,x,-25-(1-Math.abs(x)/36)*5.5,2.3,i%2?'#2a9a6a':'#d02a2a'));gem(c,0,-31,4,'#d02a2a');
  c.fillStyle='#fff2c8';c.beginPath();c.moveTo(-4,-36);c.lineTo(0,-46);c.lineTo(4,-36);c.fill();
  c.restore()}
function crownB3(c,t,h){c.save();h=h||1;
  c.fillStyle=goldG(c,-26,26);c.beginPath();c.moveTo(-27,-28);c.bezierCurveTo(-28,-50*h,-18,-74*h,-9,-88*h);c.quadraticCurveTo(0,-104*h,9,-88*h);c.bezierCurveTo(18,-74*h,28,-50*h,27,-28);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.2;c.stroke();
  c.strokeStyle='rgba(122,80,16,.5)';c.lineWidth=1;for(let x=-16;x<=16;x+=8){c.beginPath();c.moveTo(x*1.4,-34);c.quadraticCurveTo(x*1.1,-60*h,x*.4,-88*h);c.stroke()}
  [-48,-68].forEach((y,i)=>{const w=25-i*7;c.fillStyle=goldG(c,-w,w);c.beginPath();c.roundRect(-w,y*h-3.5,2*w,7,3);c.fill();c.strokeStyle='#7a5010';c.lineWidth=.9;c.stroke();for(let q=-1;q<=1;q++)gem(c,q*w*.5,y*h,1.8,q?'#2a9a6a':'#d02a2a')});
  c.fillStyle=goldG(c,-14,14);c.beginPath();c.moveTo(-6,-92*h);c.quadraticCurveTo(0,-110*h,6,-92*h);c.fill();gem(c,0,-96*h,3,'#d02a2a');
  c.fillStyle=goldG(c,-36,36);c.beginPath();c.moveTo(-35,-18);c.quadraticCurveTo(0,-31,35,-18);c.lineTo(35,-27);c.quadraticCurveTo(0,-40,-35,-27);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.1;c.stroke();
  gem(c,0,-30,3.6,'#d02a2a');[-20,20].forEach(x=>gem(c,x,-27,2.2,'#2a9a6a'));c.restore()}
function headFull3(c,S,o,who){const t=o.t||0;
  if(who==='brahma3'){const M=o.mood||{};
    // the fourth face is behind: only its crown shows; two side faces turned outward; the front face
    c.save();c.translate(0,-12);c.scale(.8,.8);crownB3(c,t,1.05);c.restore();
    [-1,1].forEach(sd=>{c.save();c.translate(sd*50,-2);c.scale(.8,.8);c.filter='brightness(.84)';hairFront3(c,S,t,who);head3(c,S,Object.assign({},o,{yaw:sd*.62,mood:Object.assign({},M,{lx:sd*.5}),t:t+sd*.7}));hairFront3(c,S,t,who);crownB3(c,t,.9);c.filter='none';c.restore()});
    head3(c,S,o);hairFront3(c,S,t,who);crownB3(c,t,1);return}
  head3(c,S,o);hairFront3(c,S,t,who);if(who==='vishnu3')crownV3(c,t)}

/* ---------- hands ---------- */
function hand3(c,S,p,ang,kind,sd,t){c.save();c.translate(p[0],p[1]);const sk=S.skin,ed=rgbaH(S.skinD,.8);let th=-sd;
  const fs=(f)=>{f();c.fillStyle=sk;c.fill();c.strokeStyle=ed;c.lineWidth=1.1;c.stroke()};
  const palm=(w,l)=>fs(()=>{c.beginPath();c.moveTo(-w*.75,0);c.bezierCurveTo(-w*1.1,l*.3,-w*1.1,l*.8,-w*.92,l);c.quadraticCurveTo(0,l+2.5,w*.92,l);c.bezierCurveTo(w*1.1,l*.8,w*1.1,l*.3,w*.75,0);c.closePath()});
  const fingers=(spread,len,yb)=>{const xs=[6.3,2.1,-2.1,-6.3],L=[14,16.5,15.5,12],R=[2.5,2.7,2.55,2.2];for(let i=3;i>=0;i--){const a=spread[i]*th,x=xs[i]*th,l=L[i]*(len[i]||len[0]||1);fs(()=>capP(c,[x,yb],[x+Math.sin(a)*l,yb+Math.cos(a)*l],R[i],R[i]*.82))}};
  const knuck=(yb)=>{[6.3,2.1,-2.1,-6.3].forEach((x,i)=>fs(()=>capP(c,[x*th,yb-2],[x*th,yb+3.5],2.8,2.7)))};
  const thumbAcross=()=>fs(()=>capP(c,[th*9,7],[-th*1.5,15],3.3,2.8));
  if(kind==='namaste'){c.rotate(ang);const pal=(s)=>fs(()=>{c.beginPath();c.moveTo(0,10);c.bezierCurveTo(s*14,6,s*13,-18,s*1.2,-36);c.lineTo(0,-36);c.closePath()});pal(-1);pal(1);
    c.strokeStyle=ed;c.lineWidth=1;[-1,1].forEach(s=>{[-26,-20].forEach(y=>{c.beginPath();c.moveTo(s*2,y);c.lineTo(s*8.5,y+4);c.stroke()})});
    [-1,1].forEach(s=>fs(()=>capP(c,[s*4,8],[s*2.2,-9],3,2.4)));c.fillStyle='#e0b04a';c.fillRect(-12,8,24,3.4);c.restore();return}
  if(kind==='grip'||kind==='veena'||kind==='gada'||kind==='lotus'||kind==='kamandalu'){const ga=kind==='veena'?ang:0;c.rotate(ga);
    fs(()=>{c.beginPath();c.ellipse(0,0,10.5,11.5,0,0,7)});for(let i=0;i<4;i++)fs(()=>{c.beginPath();c.roundRect(-12,-8+i*4.6,24,4.8,2.4)});
    fs(()=>capP(c,[th*6,-9],[th*-6,-11],3.2,2.8));c.restore();return}
  if(kind==='abhaya'||kind==='chakra'||kind==='book'||kind==='conch'){c.rotate(Math.PI+sd*.12);th=sd;palm(9.5,19);
    c.fillStyle=rgbaH(S.skinH,.35);c.beginPath();c.ellipse(0,10,5.5,6,0,0,7);c.fill();c.strokeStyle=rgbaH(S.skinD,.45);c.lineWidth=.9;c.beginPath();c.moveTo(-6,8);c.quadraticCurveTo(0,11,6,7);c.moveTo(-5,13);c.quadraticCurveTo(0,12,5,15);c.stroke();
    if(kind==='chakra'){fingers([0,.0,-.05,-.1],[1.05,.5,.45,.42],18)}else fingers([.08,0,-.05,-.11],[1],18);fs(()=>capP(c,[th*8.5,5],[th*15,13],3.4,2.8));c.restore();return}
  // forearm-aligned hands
  let a2=ang-Math.PI/2;if(kind==='open')a2-=sd*.55;if(kind==='point')a2+=0;c.rotate(a2);
  if(kind==='open'){fingers([.42,.13,-.12,-.38],[1],18);palm(9.5,19.5);c.fillStyle=rgbaH(S.skinH,.3);c.beginPath();c.ellipse(0,10,5,6,0,0,7);c.fill();fs(()=>capP(c,[th*8,6],[th*17,12],3.4,2.8))}
  else if(kind==='point'){knuck(20);palm(9.5,19);fingers([.02,0,0,0],[1.08,0,0,0].map((v,i)=>i?0.0001:v),18);thumbAcross()}
  else if(kind==='fist'){palm(10,17);knuck(18);thumbAcross()}
  else if(kind==='mala'){fingers([.1,.04,-.02,-.08],[.8],18);palm(9.5,19);fs(()=>capP(c,[th*8,5],[th*10.5,15],3.3,2.7))}
  else{fingers([.1,.04,-.03,-.09],[.88],18);palm(9.5,19);fs(()=>capP(c,[th*8,5],[th*10.5,15.5],3.3,2.7))}
  c.restore()}

/* ---------- props ---------- */
function chakra3(c,x,y,t,r){c.save();c.translate(x,y);glow2(c,0,0,r*2,'255,200,90',.42);c.rotate(t*2.6);
  c.fillStyle='#f4c850';for(let i=0;i<16;i++){const a=i*Math.PI/8;c.beginPath();c.moveTo(Math.cos(a-.12)*r,Math.sin(a-.12)*r);c.lineTo(Math.cos(a)*r*1.32,Math.sin(a)*r*1.32);c.lineTo(Math.cos(a+.12)*r,Math.sin(a+.12)*r);c.fill()}
  c.strokeStyle='#f8d870';c.lineWidth=r*.22;c.beginPath();c.arc(0,0,r*.9,0,7);c.stroke();c.strokeStyle='#a8741a';c.lineWidth=1.2;c.beginPath();c.arc(0,0,r*1.01,0,7);c.stroke();c.beginPath();c.arc(0,0,r*.78,0,7);c.stroke();
  c.strokeStyle='#e8b848';c.lineWidth=2.2;for(let i=0;i<8;i++){const a=i*.785;c.beginPath();c.moveTo(Math.cos(a)*r*.22,Math.sin(a)*r*.22);c.lineTo(Math.cos(a)*r*.8,Math.sin(a)*r*.8);c.stroke()}
  gem(c,0,0,r*.22,'#d8302a');c.restore()}
function conch3(c,x,y,a){c.save();c.translate(x,y);c.rotate(a);const g=c.createLinearGradient(-14,0,16,0);g.addColorStop(0,'#fffdf6');g.addColorStop(.6,'#efe6d2');g.addColorStop(1,'#bfb092');c.fillStyle=g;
  c.beginPath();c.moveTo(0,20);c.bezierCurveTo(-18,12,-19,-14,-4,-30);c.quadraticCurveTo(2,-38,6,-30);c.bezierCurveTo(18,-16,16,10,0,20);c.closePath();c.fill();c.strokeStyle='#9a8a6a';c.lineWidth=1.2;c.stroke();
  c.strokeStyle='#b8a888';c.lineWidth=1.3;for(let i=0;i<4;i++){c.beginPath();c.moveTo(-12+i*2,-6-i*6);c.quadraticCurveTo(0,-2-i*6,12-i*2.6,-8-i*6);c.stroke()}
  c.fillStyle='#e8b848';c.beginPath();c.ellipse(1,19,6,3,0,0,7);c.fill();c.fillStyle='#f6c2b0';c.beginPath();c.ellipse(4,4,3.4,8,.2,0,7);c.fill();c.restore()}
function gada3(c,x,y,t){c.save();c.translate(x,y);c.strokeStyle='#6a4a1a';c.lineWidth=8;c.lineCap='round';c.beginPath();c.moveTo(0,-30);c.lineTo(0,240);c.stroke();c.strokeStyle='#e0b04a';c.lineWidth=3;for(let i=0;i<4;i++){c.beginPath();c.moveTo(-4.5,40+i*48);c.lineTo(4.5,46+i*48);c.stroke()}
  c.fillStyle=goldG(c,-26,26);c.beginPath();c.ellipse(0,-60,24,30,0,0,7);c.fill();c.strokeStyle='#7a5010';c.lineWidth=1.3;c.stroke();
  c.strokeStyle='rgba(122,80,16,.7)';c.lineWidth=1.4;[-12,0,12].forEach(dx=>{c.beginPath();c.ellipse(dx*.9,-60,4+Math.abs(dx)*.0,28,0,0,7);c.stroke()});c.beginPath();c.ellipse(0,-60,23,6,0,0,7);c.stroke();
  gem(c,0,-60,4,'#d02a2a');c.fillStyle=goldG(c,-8,8);c.beginPath();c.moveTo(-7,-88);c.lineTo(0,-108);c.lineTo(7,-88);c.closePath();c.fill();c.beginPath();c.roundRect(-9,-34,18,8,3);c.fill();c.restore()}
function lotus3(c,x,y,s,t){c.save();c.translate(x,y);c.scale(s,s);c.strokeStyle='#3e6e2e';c.lineWidth=3.4;c.lineCap='round';c.beginPath();c.moveTo(0,46);c.quadraticCurveTo(-4,24,0,4);c.stroke();
  const pet=(a,l,w,c1,c2)=>{c.save();c.rotate(a);const g=c.createLinearGradient(0,0,0,-l);g.addColorStop(0,c1);g.addColorStop(1,c2);c.fillStyle=g;c.beginPath();c.moveTo(0,0);c.bezierCurveTo(-w,-l*.35,-w*.6,-l*.85,0,-l);c.bezierCurveTo(w*.6,-l*.85,w,-l*.35,0,0);c.fill();c.strokeStyle='rgba(170,60,100,.5)';c.lineWidth=.9;c.stroke();c.restore()};
  [-1.1,1.1].forEach(a=>pet(a,24,10,'#e87aa4','#fbd0de'));[-.6,.6].forEach(a=>pet(a,30,11,'#ee8ab0','#fde0ea'));pet(0,34,12,'#f29ab8','#fff0f5');c.fillStyle='#f2c84a';c.beginPath();c.ellipse(0,-3,6,3,0,0,7);c.fill();c.restore()}
function kamandalu3(c,x,y){c.save();c.translate(x,y);c.strokeStyle='#8a4a1a';c.lineWidth=3.4;c.beginPath();c.arc(0,10,12,Math.PI,0);c.stroke();
  const g=c.createRadialGradient(-8,26,2,0,32,26);g.addColorStop(0,'#f0a868');g.addColorStop(.6,'#c06a2a');g.addColorStop(1,'#7a3a14');c.fillStyle=g;c.beginPath();c.ellipse(0,34,22,20,0,0,7);c.fill();c.strokeStyle='#5a2a0c';c.lineWidth=1.2;c.stroke();
  c.fillStyle='#a8561e';c.beginPath();c.roundRect(-9,10,18,8,3);c.fill();c.strokeStyle='#e0b04a';c.lineWidth=2;c.beginPath();c.ellipse(0,34,22,5,0,0,Math.PI);c.stroke();
  c.fillStyle='#b8601e';c.beginPath();c.moveTo(18,26);c.quadraticCurveTo(32,20,36,10);c.lineTo(38,13);c.quadraticCurveTo(34,26,20,34);c.fill();c.restore()}
function mala3(c,x,y,t){c.save();c.translate(x,y);const sw=Math.sin(t*1.5)*3;for(let i=0;i<22;i++){const u=i/21,a=u*Math.PI*2,bx=Math.sin(a)*12+sw*Math.sin(u*Math.PI),by=6+(1-Math.cos(a))*18;c.fillStyle=i===0?'#e0b04a':'#7a3a1c';c.beginPath();c.arc(bx,by,2.8,0,7);c.fill()}
  c.fillStyle='#e0b04a';c.beginPath();c.arc(sw,44,3.4,0,7);c.fill();c.strokeStyle='#c8862a';c.lineWidth=1.5;c.beginPath();c.moveTo(sw,46);c.lineTo(sw-2,56);c.moveTo(sw,46);c.lineTo(sw+2,56);c.stroke();c.restore()}
function veda3(c,x,y,a){c.save();c.translate(x,y);c.rotate(a);c.fillStyle='#7a4a22';c.beginPath();c.roundRect(-30,-9,60,18,3);c.fill();c.fillStyle='#efe0b0';c.fillRect(-27,-6,54,12);c.strokeStyle='#b8a070';c.lineWidth=.9;for(let i=-2;i<=2;i++){c.beginPath();c.moveTo(-27,i*2.2);c.lineTo(27,i*2.2);c.stroke()}
  c.fillStyle='#7a4a22';c.fillRect(-30,-9,60,3.5);c.strokeStyle='#c8282a';c.lineWidth=2;[-14,14].forEach(x2=>{c.beginPath();c.moveTo(x2,-10);c.lineTo(x2,10);c.stroke()});c.restore()}
function veena3(c,A,T,t){const dx=T[0]-A[0],dy=T[1]-A[1],L=Math.hypot(dx,dy),an=Math.atan2(dy,dx);c.save();c.translate(A[0],A[1]);c.rotate(an);
  // upper gourd (behind the neck near the top)
  let g=c.createRadialGradient(L*.8-6,-14,2,L*.8,-8,24);g.addColorStop(0,'#e8b070');g.addColorStop(1,'#8a4a1a');c.fillStyle=g;c.beginPath();c.ellipse(L*.8,-12,20,18,0,0,7);c.fill();c.strokeStyle='#4a2410';c.lineWidth=1.2;c.stroke();
  // neck with frets
  g=c.createLinearGradient(0,-7,0,7);g.addColorStop(0,'#a8682a');g.addColorStop(1,'#5a3010');c.fillStyle=g;c.beginPath();c.roundRect(0,-6.5,L,13,5);c.fill();c.strokeStyle='#3a1c08';c.lineWidth=1;c.stroke();
  c.strokeStyle='#e8c060';c.lineWidth=1.6;for(let i=0;i<14;i++){const x=40+i*(L*.62/14);c.beginPath();c.moveTo(x,-6);c.lineTo(x,6);c.stroke()}
  c.strokeStyle='rgba(255,240,200,.85)';c.lineWidth=.8;[-2.5,0,2.5].forEach(y=>{c.beginPath();c.moveTo(-10,y);c.lineTo(L-6,y);c.stroke()});
  // carved head with tassel
  c.fillStyle=goldG(c,L-10,L+18);c.beginPath();c.moveTo(L-4,-8);c.quadraticCurveTo(L+16,-22,L+24,-8);c.quadraticCurveTo(L+26,6,L+14,6);c.quadraticCurveTo(L+8,6,L+10,0);c.quadraticCurveTo(L+4,6,L-4,8);c.closePath();c.fill();c.strokeStyle='#7a5010';c.lineWidth=1;c.stroke();gem(c,L+16,-6,2.6,'#d02a2a');
  const ts=Math.sin(t*2.2)*3;c.save();c.translate(L+2,6);c.rotate(-an);c.strokeStyle='#c8302a';c.lineWidth=2;c.beginPath();c.moveTo(0,0);c.quadraticCurveTo(ts,10,ts*1.4,20);c.stroke();c.fillStyle='#c8302a';c.beginPath();c.moveTo(ts*1.4-4,18);c.lineTo(ts*1.4+4,18);c.lineTo(ts*1.4+3,30);c.lineTo(ts*1.4-3,30);c.fill();c.restore();
  // main gourd
  g=c.createRadialGradient(-10,-8,4,0,0,40);g.addColorStop(0,'#f0b878');g.addColorStop(.6,'#b06a2a');g.addColorStop(1,'#6a3410');c.fillStyle=g;c.beginPath();c.ellipse(-8,4,34,31,0,0,7);c.fill();c.strokeStyle='#4a2410';c.lineWidth=1.3;c.stroke();
  c.strokeStyle='#e0b04a';c.lineWidth=2.2;c.beginPath();c.ellipse(-8,4,27,24,0,0,7);c.stroke();c.fillStyle='#e8d6a0';c.beginPath();c.roundRect(10,-5,8,10,2);c.fill();c.restore()}

/* ---------- body ---------- */
function foot3(c,S,f,sd,anklet){c.fillStyle=S.skinM;c.beginPath();c.ellipse(f[0]+sd*5,f[1]-4,18,8.5,sd*.08,0,7);c.fill();c.strokeStyle=rgbaH(S.skinD,.7);c.lineWidth=1.1;c.stroke();
  c.fillStyle=S.skin;for(let i=0;i<5;i++){c.beginPath();c.ellipse(f[0]+sd*(8+i*3.2)-sd*0,f[1]-1.5+Math.abs(i-1)*.3,2.3-(i>2?.4:0),2.6,0,0,7);c.fill()}
  c.fillStyle=rgbaH(S.skinH,.3);c.beginPath();c.ellipse(f[0]+sd*1,f[1]-8,9,2.6,0,0,7);c.fill();
  if(anklet){c.fillStyle=anklet;c.beginPath();c.roundRect(f[0]-12,f[1]-17,24,5,2.5);c.fill();for(let i=-2;i<=2;i++){c.beginPath();c.arc(f[0]+i*5,f[1]-11,1.6,0,7);c.fill()}}}
function lower3(c,S,P,sw,t){const L=S.lower,wy=P.ph[1]-4,hf=L.len3??.72,col=L.col,lg=(x0,x1)=>{const g=c.createLinearGradient(x0,0,x1,0);g.addColorStop(0,L.colL);g.addColorStop(.55,col);g.addColorStop(1,L.colD);return g};
  const legs=[[P.hipL,P.fL,-1],[P.hipR,P.fR,1]].map(([h,f,sd])=>{const r=elbow(h,f,86,92,sd);return {h,f,sd,E:r.e,hem:[lerp(r.e[0],f[0],hf),lerp(r.e[1],f[1],hf)]}});
  // bare shins + feet
  legs.forEach(q=>{tapered(c,q.E,q.f,21,13,S.skin);c.globalAlpha=.38;tapered(c,[q.E[0]+q.sd*7,q.E[1]],[q.f[0]+q.sd*5,q.f[1]-6],7,5,S.skinD);c.globalAlpha=1;foot3(c,S,q.f,q.sd,S.anklet)});
  const fl=L.flare||26,A=legs[0],B=legs[1],lx0=Math.min(A.hem[0],P.hipL[0]-8)-fl,rx0=Math.max(B.hem[0],P.hipR[0]+8)+fl,mx=(A.hem[0]+B.hem[0])/2+sw*3,my=Math.min(A.hem[1],B.hem[1])-12,wv=Math.sin(t*1.6)*3;
  const sk=()=>{c.beginPath();c.moveTo(-50,wy);c.quadraticCurveTo(-60,wy+50,lx0,A.hem[1]);c.quadraticCurveTo((lx0+mx)/2,A.hem[1]+7+wv,mx,my);c.quadraticCurveTo((rx0+mx)/2,B.hem[1]+7-wv,rx0,B.hem[1]);c.quadraticCurveTo(60,wy+50,50,wy);c.closePath()};
  sk();c.fillStyle=lg(lx0,rx0);c.fill();c.save();sk();c.clip();
  c.fillStyle=rgbaH(L.colD,.42);c.beginPath();c.moveTo(mx-3,wy+96);c.quadraticCurveTo(mx-6,my-30,mx-20,my+4);c.lineTo(mx+20,my+4);c.quadraticCurveTo(mx+6,my-30,mx+3,wy+96);c.closePath();c.fill();
  c.strokeStyle=rgbaH(L.colD,.5);c.lineWidth=1.6;for(let i=-4;i<=4;i++){if(!i)continue;const bx=i<0?lerp(mx,lx0,-i/4.6):lerp(mx,rx0,i/4.6);c.beginPath();c.moveTo(i*9,wy+10);c.quadraticCurveTo(i*12+sw*2,lerp(wy,my,.55),bx,my+14);c.stroke()}
  c.fillStyle='rgba(255,245,220,.16)';c.beginPath();c.moveTo(-48,wy);c.lineTo(-20,wy);c.quadraticCurveTo(-34,lerp(wy,my,.5),lx0+30,A.hem[1]);c.lineTo(lx0,A.hem[1]);c.closePath();c.fill();c.restore();
  c.strokeStyle=L.trim;c.lineWidth=6;c.beginPath();c.moveTo(lx0,A.hem[1]-2);c.quadraticCurveTo((lx0+mx)/2,A.hem[1]+5+wv,mx,my-2);c.quadraticCurveTo((rx0+mx)/2,B.hem[1]+5-wv,rx0,B.hem[1]-2);c.stroke();
  // front pleated fall (kaccha) swaying between the legs
  const hy=my+8;
  c.fillStyle=L.colL;c.beginPath();c.moveTo(-13,wy+6);c.lineTo(13,wy+6);c.quadraticCurveTo(18,lerp(wy,hy,.5),mx+21,hy);c.lineTo(mx-21,hy);c.quadraticCurveTo(-18,lerp(wy,hy,.5),-13,wy+6);c.closePath();c.fill();
  c.strokeStyle=rgbaH(L.colD,.6);c.lineWidth=1.4;for(let i=-3;i<=3;i++){c.beginPath();c.moveTo(i*3.6,wy+8);c.quadraticCurveTo(i*5,lerp(wy,hy,.5),mx+i*6.6,hy-2);c.stroke()}
  c.fillStyle=L.trim;c.beginPath();c.moveTo(mx-22,hy-7);c.lineTo(mx+22,hy-7);c.lineTo(mx+21,hy);c.lineTo(mx-21,hy);c.closePath();c.fill();
  c.strokeStyle=L.trim;c.lineWidth=3;c.beginPath();c.moveTo(13,wy+6);c.quadraticCurveTo(18,lerp(wy,hy,.5),mx+21,hy-4);c.stroke();
  // waist: sash knot with hanging ends + gold belt
  if(S.sashTie){const st=S.sashTie;[-1,1].forEach(sd=>{const f2=Math.sin(t*1.7+sd*1.3)*4+sw*2;c.fillStyle=st;c.beginPath();c.moveTo(sd*30,wy+2);c.quadraticCurveTo(sd*(46+f2),wy+50,sd*(40+f2*1.5),wy+112);c.lineTo(sd*(26+f2*1.4),wy+108);c.quadraticCurveTo(sd*(30+f2),wy+50,sd*18,wy+6);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.18)';c.lineWidth=1.2;c.stroke();
    c.fillStyle=L.trim;c.beginPath();c.moveTo(sd*(40+f2*1.5),wy+112);c.lineTo(sd*(26+f2*1.4),wy+108);c.lineTo(sd*(26.5+f2*1.4),wy+102);c.lineTo(sd*(40.5+f2*1.5),wy+106);c.fill()})}
  c.fillStyle=S.belt||L.trim;c.beginPath();c.roundRect(-52,wy-8,104,12,5);c.fill();c.strokeStyle='rgba(90,50,0,.5)';c.lineWidth=1;c.stroke();
  if(S.belt){for(let i=-4;i<=4;i++)gem(c,i*11,wy-2,1.8,i%2?'#2a9a6a':'#d02a2a');c.fillStyle=goldG(c,-8,8);c.beginPath();c.moveTo(-8,wy+4);c.lineTo(8,wy+4);c.lineTo(0,wy+22);c.closePath();c.fill();gem(c,0,wy+10,3,'#d02a2a')}}
function torso3(c,S,P,bw){const fx=a=>a*bw,wa=S.waist||1;const tp=()=>{c.beginPath();c.moveTo(P.sL[0]-4,P.sL[1]+2);c.bezierCurveTo(fx(-56),P.ch[1]+16,fx(-44*wa),P.ch[1]+70,fx(-37*wa),P.ph[1]-6);c.lineTo(fx(37*wa),P.ph[1]-6);c.bezierCurveTo(fx(44*wa),P.ch[1]+70,fx(56),P.ch[1]+16,P.sR[0]+4,P.sR[1]+2);c.bezierCurveTo(26,P.nk[1]+2,-26,P.nk[1]+2,P.sL[0]-4,P.sL[1]+2);c.closePath()};
  const g=c.createLinearGradient(-62,0,62,0);g.addColorStop(0,S.skinH);g.addColorStop(.3,S.skin);g.addColorStop(.72,S.skinM);g.addColorStop(1,S.skinD);tp();c.fillStyle=g;c.fill();
  c.save();tp();c.clip();const m=S.muscle??.5;
  [-1,1].forEach(sd=>{c.fillStyle=rgbaH(S.skinD,.22*m+(S.old?.1:0));c.beginPath();c.moveTo(sd*4,P.ch[1]+(S.old?20:12));c.bezierCurveTo(sd*20,P.ch[1]+(S.old?34:28),sd*40,P.ch[1]+(S.old?30:22),sd*48,P.ch[1]+6);c.lineTo(sd*48,P.ch[1]+(S.old?18:12));c.bezierCurveTo(sd*36,P.ch[1]+(S.old?40:32),sd*18,P.ch[1]+(S.old?42:34),sd*4,P.ch[1]+(S.old?26:18));c.fill();
    c.fillStyle=rgbaH(S.skinH,.18*m+.06);c.beginPath();c.ellipse(sd*22,P.ch[1]+2,17,11,sd*-.2,0,7);c.fill()});
  c.strokeStyle=rgbaH(S.skinD,.35);c.lineWidth=1.6;c.beginPath();c.moveTo(0,P.ch[1]+20);c.lineTo(0,P.ph[1]-30);c.stroke();
  c.fillStyle=rgbaH(S.skinD,.6);c.beginPath();c.ellipse(0,P.ph[1]-34,2.6,3.6,0,0,7);c.fill();
  if(S.old){c.strokeStyle=rgbaH(S.skinD,.35);c.lineWidth=1.6;c.beginPath();c.moveTo(-34,P.ph[1]-48);c.quadraticCurveTo(0,P.ph[1]-36,34,P.ph[1]-48);c.stroke()}
  c.strokeStyle='rgba(255,226,170,.5)';c.lineWidth=3;c.beginPath();c.moveTo(P.sL[0]-4,P.sL[1]+6);c.bezierCurveTo(fx(-56),P.ch[1]+16,fx(-44*wa),P.ch[1]+70,fx(-37*wa),P.ph[1]-6);c.stroke();
  c.restore()}
function ornaments3(c,S,P,t,who,sw){const nk=P.nk[1];
  // sacred thread from the left shoulder to the right hip
  c.strokeStyle='#f6eed4';c.lineWidth=2.6;c.beginPath();c.moveTo(P.sR[0]-10,P.sR[1]+2);c.bezierCurveTo(20,P.ch[1]+40,-10,P.ph[1]-50,-36,P.ph[1]-8);c.stroke();c.strokeStyle='rgba(120,100,60,.4)';c.lineWidth=.8;c.stroke();
  if(who==='vishnu3'){
    c.strokeStyle=goldG(c,-30,30);c.lineWidth=6;c.beginPath();c.moveTo(-24,nk+8);c.quadraticCurveTo(0,nk+30,24,nk+8);c.stroke();for(let i=0;i<9;i++){const u=i/8;gem(c,lerp(-20,20,u),nk+11+Math.sin(u*3.14)*9,1.7,i%2?'#2a9a6a':'#d02a2a')}
    c.strokeStyle='#e8b848';c.lineWidth=3;c.beginPath();c.moveTo(-32,nk+10);c.quadraticCurveTo(0,nk+84,32,nk+10);c.stroke();
    c.fillStyle=goldG(c,-11,11);c.beginPath();c.ellipse(0,nk+48,10,12,0,0,7);c.fill();gem(c,0,nk+48,6.5,'#e0282a');glow2(c,0,nk+48,16,'255,90,70',.35);
    // vanamala: long forest garland to the knees
    const bx=sw*5,by=-150;const pt=u=>{const a=[-40,nk+8],b=[40,nk+8],m1=[-66,-250],m2=[66,-250];const s=u<.5?u*2:(1-u)*2,side=u<.5?-1:1;const A=side<0?a:b,M1=side<0?m1:m2;const q=1-s;return [q*q*A[0]+2*q*s*M1[0]+s*s*(bx),q*q*A[1]+2*q*s*M1[1]+s*s*by]};
    c.strokeStyle='#3e7a34';c.lineWidth=3;c.beginPath();for(let i=0;i<=40;i++){const p=pt(i/40);i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1])}c.stroke();
    const FC=['#e03a3a','#f4c430','#f6f0e8','#f08ab0','#e86a20'];for(let i=0;i<=34;i++){const p=pt(i/34);if(i%4===2){c.fillStyle='#4a9a3e';c.beginPath();c.ellipse(p[0]+4,p[1],6,3,.6,0,7);c.fill()}c.fillStyle=FC[i%5];c.beginPath();c.arc(p[0],p[1],4.6,0,7);c.fill();c.fillStyle='rgba(255,255,255,.4)';c.beginPath();c.arc(p[0]-1.3,p[1]-1.3,1.5,0,7);c.fill()}
    gem(c,bx,by+6,5,'#e0302a')}
  if(who==='brahma3'){c.strokeStyle=goldG(c,-30,30);c.lineWidth=4;c.beginPath();c.moveTo(-26,nk+8);c.quadraticCurveTo(0,nk+44,26,nk+8);c.stroke();gem(c,0,nk+30,4,'#2a9a6a');
    // red-maroon uttariya draped over the left shoulder, across the chest
    const fl=Math.sin(t*1.3)*3;c.fillStyle='#a8282e';c.beginPath();c.moveTo(P.sR[0]+10,P.sR[1]-4);c.bezierCurveTo(30,P.ch[1]+10,-10,P.ch[1]+60,-44,P.ph[1]-2);c.lineTo(-24,P.ph[1]+4);c.bezierCurveTo(6,P.ch[1]+66,40,P.ch[1]+40,P.sR[0]+18,P.sR[1]+30);c.closePath();c.fill();
    c.strokeStyle='#e0b04a';c.lineWidth=3;c.beginPath();c.moveTo(P.sR[0]+10,P.sR[1]-4);c.bezierCurveTo(30,P.ch[1]+10,-10,P.ch[1]+60,-44,P.ph[1]-2);c.stroke();c.strokeStyle='rgba(0,0,0,.2)';c.lineWidth=1.4;[[.3],[.6]].forEach(([u])=>{c.beginPath();c.moveTo(lerp(P.sR[0]+12,-40,u),lerp(P.sR[1],P.ph[1],u));c.lineTo(lerp(P.sR[0]+12,-40,u)+16,lerp(P.sR[1],P.ph[1],u)+10);c.stroke()});
    c.fillStyle='#a8282e';c.beginPath();c.moveTo(P.sR[0]+6,P.sR[1]);c.quadraticCurveTo(P.sR[0]+34+fl,P.sR[1]+60,P.sR[0]+26+fl,P.sR[1]+150);c.lineTo(P.sR[0]+8+fl,P.sR[1]+146);c.quadraticCurveTo(P.sR[0]+16,P.sR[1]+60,P.sR[0]-6,P.sR[1]+8);c.fill()}
  if(who==='narada3'){[[18,6.2,32],[52,5,40]].forEach(([dep,r,w],j)=>{for(let i=0;i<(j?19:13);i++){const n=j?18:12,u=i/n,bx=-w+u*2*w,by=nk+10+Math.sin(u*3.14)*dep;c.fillStyle='#6a3418';c.beginPath();c.arc(bx,by,r*.72,0,7);c.fill();c.fillStyle='rgba(255,200,150,.35)';c.beginPath();c.arc(bx-1.2,by-1.2,r*.25,0,7);c.fill()}});
    c.fillStyle='#6a3418';c.beginPath();c.arc(0,nk+66,5,0,7);c.fill();
    // ochre shawl crossing the chest from the right shoulder
    c.strokeStyle='#d88a2a';c.lineWidth=14;c.lineCap='butt';c.beginPath();c.moveTo(P.sL[0]+2,P.sL[1]+2);c.quadraticCurveTo(-4,P.ch[1]+20,40,P.ph[1]-6);c.stroke();c.strokeStyle='#b8661a';c.lineWidth=2;c.beginPath();c.moveTo(P.sL[0]+8,P.sL[1]+8);c.quadraticCurveTo(2,P.ch[1]+24,44,P.ph[1]-2);c.stroke()}}
function arm3(c,S,sh,hd,sd,w){const r=limbS(c,S,sh,hd,64,62,sd,w);armband(c,r,w[0]-2,S.armlet||'#e0b04a');
  if(S.bangle){const x=lerp(r.e[0],r.t[0],.84),y=lerp(r.e[1],r.t[1],.84),a=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);c.save();c.translate(x,y);c.rotate(a+1.57);c.fillStyle=S.bangle;c.beginPath();c.roundRect(-w[2]-2,-3.2,2*w[2]+4,4.4,2);c.fill();c.beginPath();c.roundRect(-w[2]-2,2.4,2*w[2]+4,3,1.5);c.fill();c.restore()}return r}
function drawHero3(c,S,P0,o){const who=S.id3,t=o.t||0,k=o.k||0,br=Math.sin(t*1.7)*2.2,sw=Math.sin(t*1.5)+(P0.sway||0),P=JSON.parse(JSON.stringify(P0)),bw=S.build||1;
  ['ch','nk','hd','sL','sR'].forEach(a=>{P[a][1]+=br});P.hL[1]+=br*.6;P.hR[1]+=br*.6;P.sL[0]*=bw;P.sR[0]*=bw;
  const HS=S.hs||1.14,G=P.g||{L:'relax',R:'relax'};let gL=G.L,gR=G.R;if(k>.55){if(gL==='relax')gL='fist';if(gR==='relax')gR='fist'}
  c.save();
  // behind everything: hair falling behind the shoulders (follows the head)
  if(!o.bust){if(P.sit){legsS(c,S,P,0);clothS(c,S,P,sw,0)}else lower3(c,S,P,sw,t)}
  const ln=P.lean||0;c.save();if(ln){c.translate(0,P.ph[1]);c.rotate(ln*.12);c.scale(1,1-Math.max(0,ln)*.55);c.translate(0,-P.ph[1])}
  const hsy=1-Math.max(0,ln)*.28,mood=Object.assign({},o.mood||{});if(ln>.12&&gL==='namaste'){mood.blink=Math.max(mood.blink||0,clamp((ln-.12)*6));mood.smile=Math.max(mood.smile||0,.4)}
  c.save();c.translate(P.hd[0],P.hd[1]+40);c.rotate(o.tilt||0);c.scale(HS,HS*hsy);c.translate(0,-40);hairBack3(c,S,t,who);c.restore();
  if(who==='narada3'&&P.veena!=='play')veena3(c,[-12,-336],[-176,-616],t);
  // upper (back) arms
  if(S.arms4){const Sb=Object.assign({},S,{skin:S.skinM,skinH:S.skin,skinM:shade(S.skinM,.92)});const T=[[-140,-484],[140,-484]];
    [-1,1].forEach((sd,i)=>{const A=[sd*52*bw,P.sL[1]-4],r=arm3(c,Sb,A,T[i],sd,[15,12,9.5]);const a=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);
      if(who==='vishnu3'){if(sd<0){chakra3(c,r.t[0]-2,r.t[1]-48,t,20);hand3(c,Sb,r.t,a,'chakra',sd,t)}else{hand3(c,Sb,r.t,a,'conch',sd,t);conch3(c,r.t[0]+2,r.t[1]-26,.18)}}
      else{if(sd<0){hand3(c,Sb,r.t,a,'abhaya',sd,t);mala3(c,r.t[0]+2,r.t[1]-26,t)}else{hand3(c,Sb,r.t,a,'book',sd,t);veda3(c,r.t[0],r.t[1]-30,-.08)}}})}
  if(S.uttariya){[-1,1].forEach(sd=>{const x0=sd*(Math.abs(P.sR[0])*.95),y0=P.sR[1]+2,fl=Math.sin(t*1.8+sd)*5+sw*2;const gx=c.createLinearGradient(x0-12,0,x0+12,0);gx.addColorStop(0,S.uttariya);gx.addColorStop(1,shade(S.uttariya,.72));c.fillStyle=gx;
    c.beginPath();c.moveTo(x0-sd*8,y0);c.bezierCurveTo(x0+sd*16,y0+50,x0+sd*(36+fl),y0+120,x0+sd*(28+fl*1.6),P.ph[1]+90);c.lineTo(x0+sd*(6+fl),P.ph[1]+100);c.bezierCurveTo(x0-sd*2,y0+120,x0-sd*6,y0+50,x0+sd*6,y0);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.16)';c.lineWidth=1.6;c.stroke()})}
  torso3(c,S,P,bw);
  if(S.uttariya){c.fillStyle=S.uttariya;c.beginPath();c.moveTo(-44,P.ph[1]-20);c.quadraticCurveTo(0,P.ph[1]+22+sw*2,44,P.ph[1]-20);c.lineTo(42,P.ph[1]-8);c.quadraticCurveTo(0,P.ph[1]+36+sw*2,-42,P.ph[1]-8);c.closePath();c.fill();c.strokeStyle='rgba(0,0,0,.15)';c.lineWidth=1.2;c.stroke()}
  ornaments3(c,S,P,t,who,sw);
  c.fillStyle=S.skinM;c.beginPath();c.roundRect(P.nk[0]-15,P.hd[1]+28,30,P.nk[1]-P.hd[1]+6,8);c.fill();c.fillStyle=rgbaH(S.skinD,.35);c.beginPath();c.ellipse(P.nk[0],P.hd[1]+56,15,8,0,0,7);c.fill();
  if(!o.noHead){c.save();c.translate(P.hd[0],P.hd[1]+40);c.rotate(o.tilt||0);c.scale(HS,HS*hsy);c.translate(-P.hd[0],-P.hd[1]-40);c.translate(P.hd[0],P.hd[1]);headFull3(c,S,{expr:o.expr,k:k,t:t,mood:mood},who);c.restore()}
  // front arms
  const ef=P.ef?-1:1,wA=[19,15,12],sideL=P.eL||-ef,aL=arm3(c,S,P.sL,P.hL,sideL,wA),aR=arm3(c,S,P.sR,P.hR,P.eR||ef,wA);
  [[P.sL,aL],[P.sR,aR]].forEach(([s,r],i)=>{const a=Math.atan2(r.e[1]-s[1],r.e[0]-s[0]);c.save();c.translate(lerp(s[0],r.e[0],.12),lerp(s[1],r.e[1],.12));c.rotate(a);const g=c.createLinearGradient(0,-20,0,20);g.addColorStop(0,i?S.skinM:S.skin);g.addColorStop(1,i?S.skin:S.skinM);c.fillStyle=g;c.beginPath();c.ellipse(0,0,21,18.5,0,0,7);c.fill();c.restore()});
  if(who==='narada3'&&P.veena==='play')veena3(c,[-50,-262],[191,-556],t);
  const ang=r=>Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);
  if(gL==='namaste'&&gR==='namaste'&&Math.hypot(aL.t[0]-aR.t[0],aL.t[1]-aR.t[1])<56){hand3(c,S,[(aL.t[0]+aR.t[0])/2,(aL.t[1]+aR.t[1])/2],0,'namaste',1,t)}
  else{[[aL,gL,-1],[aR,gR,1]].forEach(([r,g0,sd])=>{let g=g0==='namaste'?'abhaya':g0;const p=r.t;
    if(g==='gada')gada3(c,p[0],p[1],t);if(g==='lotus')lotus3(c,p[0]-sd*14,p[1]-44,1,t);if(g==='kamandalu')kamandalu3(c,p[0],p[1]);
    hand3(c,S,p,ang(r),g,sd,t);if(g==='lotus'){c.strokeStyle='#3e6e2e';c.lineWidth=3.4;c.beginPath();c.moveTo(p[0]-sd*14,p[1]+2);c.lineTo(p[0]-sd*14,p[1]+10);c.stroke()}})}
  c.restore();c.restore()}
function bust3(c,S,who,t,tilt){c.save();c.scale(1/1.14,1/1.14);c.translate(0,478);drawHero3(c,S,poseOf3('stand',who),{t:t,noHead:true,bust:true,tilt:tilt});c.restore()}
Object.assign(CAST,{
 vishnu3:skinSet('#4c7cd2',{id3:'vishnu3',v3:true,skinH:'#86aef0',skinD:'#24448a',lower:Object.assign(clothSet('#f4c228','#c8361e'),{type:'dhoti',len3:.6,flare:25}),sashTie:'#e8402a',belt:'#e6b84a',uttariya:'#f6e7a8',arms4:true,armlet:'#e6b84a',bangle:'#e6b84a',anklet:'#e6b84a',muscle:.7,waist:.9,
   f3:{faceW:34,jaw:26,chin:49,eyeX:14.5,eyeY:3,eyeW:11.5,lift:3.2,eyeH:5.4,lid:.36,irisR:4.9,iris:'#1c1424',lash:'#0e0a1c',browY:-12,arch:4.6,browTh:3.6,browIn:5.5,brow:'#0e0c1c',nose:{tip:22,w:6.8},mouthY:35,mouthW:9.6,lip:'#b4487a',lipD:'#5a1838',blush:'255,140,190',smile0:.3,wing:3.6,blinkPh:0,ear:'makara',tilak:'vaishnava'}}),
 brahma3:skinSet('#dc9a68',{id3:'brahma3',v3:true,old:true,lower:Object.assign(clothSet('#e2650e','#f0c048'),{type:'dhoti',len3:.94,flare:32}),sashTie:null,arms4:true,armlet:'#e0b04a',bangle:'#e0b04a',muscle:.25,build:1.02,waist:1.1,
   f3:{faceW:35,jaw:27,chin:52,eyeX:14.5,eyeY:4,eyeW:10.4,lift:-1.2,eyeH:5,lid:.28,irisR:4.3,iris:'#3a2414',lash:'#3a2418',browY:-12.5,arch:3,browTh:5.6,browIn:4.5,brow:'#f4f0e8',browEdge:'#8a7a6a',bushy:1,nose:{tip:25,w:9,hook:1.6},mouthY:37,mouthW:9.4,lip:'#a8584a',lipD:'#5a2418',blush:'230,110,90',smile0:.2,age:1,blinkPh:.33,ear:'hoop',tilak:'flame',beard:'#f4f1ea',beardLen:58}}),
 narada3:skinSet('#7c4a2c',{id3:'narada3',v3:true,lower:Object.assign(clothSet('#f4f0e6','#d8962a'),{type:'dhoti',len3:.5,flare:27}),sashTie:'#d88a2a',armlet:'#6a3418',bangle:null,muscle:.35,build:.92,waist:.92,
   f3:{faceW:32,jaw:20,chin:50,eyeX:14,eyeY:3,eyeW:11,lift:1.8,eyeH:6.2,lid:.08,irisR:5.3,iris:'#2a160c',lash:'#0c0806',browY:-13.5,arch:6,browTh:3.3,browIn:5,brow:'#0c0806',asym:3.6,nose:{tip:21,w:6.4,up:1.6},mouthY:34,mouthW:9.4,lip:'#8a4436',lipD:'#3a1410',blush:'210,90,70',smile0:.38,smirk:.65,wing:0,twinkle:1,blinkPh:.61,ear:'rudra',tilak:'vaishnava'}})
});
/*V3END*/
/* ---------- engine glue ---------- */
const V2NAMES=new Set(['narada','kumara','jaya','vijaya','villager','villager_w','prasuti','sati','diti','danu','asikli','kashyapa','indra','surya','chandra','hiranyaksha','hiranyakashipu','ravana','harihara','shiva','vishnu','hayagriva','daksha','manu','adishakti','brahmi','madhu','kaitabha','ardha','brahma','vishnu_rest','vishnu3','brahma3','narada3',...[0,1,2,3,4,5,6].map(i=>'rishi'+i)]);
const SCALE={shiva:.62,kumara:.46,default:.62};
function v2fig(who,x,y,s,t,o){
  const sc=SCALE[who]||SCALE.default,FR=clamp(o.res||s*SC_,1.4,3.9),RG=[-260,-560,520,620];
  if(who==='vishnu_rest'){glow(x-70*sc*s,y-330*sc*s,420*sc*s,'255,205,100',.30);glow(x-70*sc*s,y-330*sc*s,230*sc*s,'255,232,160',.26)}
  const c=figBegin(FR,OY,RG);if(o.flip<0)c.scale(-1,1);c.scale(sc,sc);
  const ex=o.expr||{},kk=o.k!=null?o.k:(ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0),face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(who==='shiva'){const pn=o.pose==='rage'||o.pose==='lunge'?'rage':'calm',P=mixPose(POSES.calm,POSES.rage,pn==='rage'?1:0);drawShiva(c,{P:P,t:t,rage:kk>.5,k:kk,expr:face==='closed'?'closed':undefined,imp:o.imp||0})}
  else if(who==='brahma')drawBrahmaRig(c,{t:t,k:kk,expr:face,hd:o.hd});
  else if(who==='vishnu_rest')drawReclineVishnu(c,{t:t});
  else if(who==='ardha')drawArdha(c,{t:t});
  else if(who==='harihara')drawHarihara(c,{t:t});
  else if(V3.has(who))drawHero3(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:kk,expr:face,prop:o.prop,mood:o.mood,tilt:o.tilt});
  else drawHuman(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:(CAST[who].kdef||kk),expr:face,prop:o.prop,mood:o.mood,tilt:o.tilt});
  figFinish(c,o,x,y,s,FR,OY,RG,.26,.34,true)}
function bust(c,S,o){ // neck + shoulders + garments below a head close-up, so heads never float like masks
  c.fillStyle=S.skinM;c.fillRect(-17,24,34,56);
  const g=c.createLinearGradient(-170,0,170,0);g.addColorStop(0,S.skinH);g.addColorStop(.4,S.skin);g.addColorStop(1,S.skinD);c.fillStyle=g;
  c.beginPath();c.moveTo(-190,170);c.bezierCurveTo(-180,84,-108,66,-28,58);c.lineTo(28,58);c.bezierCurveTo(108,66,180,84,190,170);c.closePath();c.fill();
  c.fillStyle='rgba(255,255,255,.12)';c.beginPath();c.ellipse(-70,84,46,16,.1,0,7);c.fill();
  if(o.sash){c.strokeStyle=o.sash;c.lineWidth=22;c.lineCap='butt';c.beginPath();c.moveTo(-150,86);c.quadraticCurveTo(-30,102,70,170);c.stroke()}
  if(o.upper){c.fillStyle=o.upper;c.beginPath();c.moveTo(-120,92);c.quadraticCurveTo(0,60,120,92);c.lineTo(150,170);c.lineTo(-150,170);c.closePath();c.fill();c.strokeStyle='#b8862a';c.lineWidth=4;c.beginPath();c.moveTo(-120,92);c.quadraticCurveTo(0,64,120,92);c.stroke()}
  if(o.beads){c.fillStyle='#6a3a20';for(let k=0;k<15;k++){const u=k/14;c.beginPath();c.arc(-42+u*84,64+Math.sin(u*3.14)*44,4.6,0,7);c.fill()}}
  if(o.garland){for(let k=0;k<17;k++){const u=k/16;c.fillStyle=k%2?'#f08ab0':'#ffd0e0';c.beginPath();c.arc(-50+u*100,64+Math.sin(u*3.14)*54,5.6,0,7);c.fill()}c.fillStyle='#e0302a';c.beginPath();c.arc(0,122,6.4,0,7);c.fill()}
  if(o.necklace){c.strokeStyle=o.necklace;c.lineWidth=5;c.beginPath();c.moveTo(-40,64);c.quadraticCurveTo(0,130,40,64);c.stroke();c.fillStyle=o.necklace;c.beginPath();c.arc(0,104,6,0,7);c.fill()}
  if(o.ash){c.strokeStyle='#e8e4ee';c.lineWidth=5;[0,1,2].forEach(i=>{c.beginPath();c.moveTo(-58+i*4,112+i*13);c.quadraticCurveTo(0,124+i*13,58-i*4,112+i*13);c.stroke()})}
  if(o.snake){c.strokeStyle='#2f5a48';c.lineWidth=15;c.lineCap='round';c.beginPath();c.moveTo(-110,78);c.bezierCurveTo(-60,124,0,128,48,98);c.bezierCurveTo(80,80,96,72,112,50);c.stroke();}
  if(o.armlets){c.fillStyle=o.armlets;[-1,1].forEach(sd=>{c.beginPath();c.roundRect(sd*150-18,100,36,18,3);c.fill()})}}
function crownB(c,hs){c.save();c.translate(0,-24);c.scale(1,hs);c.translate(0,24);c.fillStyle='#e6b84a';c.beginPath();c.moveTo(-26,-24);c.lineTo(-22,-52);c.lineTo(-10,-58);c.lineTo(-5,-96);c.lineTo(0,-128);c.lineTo(5,-96);c.lineTo(10,-58);c.lineTo(22,-52);c.lineTo(26,-24);c.closePath();c.fill();c.fillStyle='#c4882a';c.fillRect(-26,-30,52,7);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-40,4,0,7);c.fill();c.restore()}
function shivaJataSmall(c,t,rage){c.save();c.translate(0,-30);c.scale(.74,.7);c.translate(0,30);drawJata(c,0,-34,t,rage,0);c.restore()}
function v2head(who,x,y,s,t,o){ // close-up of the head with neck, shoulders and garments
  const FR=clamp(s*SC_,2,3.9),RG=[-300,-330,600,520];const c=figBegin(FR,OY,RG);const ex=o.expr||{},kk=ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0,face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  c.scale(1.5,1.5);if(who==='vishnu'||who==='hayagriva'||who==='adishakti')c.translate(0,24);
  if(V3.has(who)){const S=CAST[who];if(who==='vishnu3')c.translate(0,30);bust3(c,S,who,t,o.tilt);c.rotate(o.tilt||0);headFull3(c,S,{expr:face,k:o.k!=null?o.k:kk,t:t,mood:o.mood},who)}
  else if(who==='shiva'){c.translate(0,-6);c.scale(.82,.82);bust(c,{skin:SH.skin,skinM:SH.skinM,skinD:SH.skinD,skinH:SH.skinH},{beads:true,ash:true,snake:true,armlets:'#e0b04a'});shivaJataSmall(c,t,kk>.5);drawHead(c,0,0,{expr:face==='closed'?'closed':undefined,k:kk,t:t})}
  else if(who==='brahma'){const S=BRAHMA;bust(c,S,{sash:'#f6f0e0',armlets:'#e0b04a'});
    const side=(x2)=>{c.save();c.translate(x2,10);c.scale(.8,.8);c.filter='brightness(.8)';drawHead(c,0,0,{expr:face,k:kk,S:S,t:t});crownB(c,.7);c.filter='none';c.restore()};side(-58);side(58);
    drawHead(c,0,0,{expr:face,k:kk,S:S,t:t});crownB(c,.78)}
  else if(who==='ardha'||who==='harihara'){const A=CAST[who==='ardha'?'adishakti':'vishnu'];
    halfHead(c,()=>{bust(c,A,{necklace:A.necklace,garland:who==='harihara',upper:who==='ardha'?'#e0b04a':null});if(A.hair&&A.hair.type==='long')hairBack(c,A,{hd:[0,0],ph:[0,200]},t);drawHead(c,0,0,{expr:face,k:0,S:A,t:t});hairFront(c,A,0,0);headgear(c,A,0,0)},()=>{bust(c,{skin:SH.skin,skinM:SH.skinM,skinD:SH.skinD,skinH:SH.skinH},{beads:true,ash:true,snake:true});shivaJataSmall(c,t,false);drawHead(c,0,0,{expr:face==='closed'?'closed':undefined,k:0,t:t})})}
  else{const S=CAST[who];if(S.headType==='horse'){bust(c,S,{garland:true,armlets:S.armlet});horseHead(c,0,10,kk,t)}else{
      bust(c,S,{sash:S.sash&&!S.female?S.sash:null,beads:S.beads,garland:S.garland,necklace:S.necklace,upper:S.upper&&S.upper.col,armlets:S.armlet});
      if(S.hair&&S.hair.type==='long'){hairBack(c,S,{hd:[0,0],ph:[0,200]},t)}drawHead(c,0,0,{expr:face,k:o.k!=null?o.k:(S.kdef||kk),S:S,t:t});hairFront(c,S,0,0);headgear(c,S,0,0)}}
  figFinish(c,o,x,y,s,FR,OY,RG,.26,.34,false)}
return {has:w=>V2NAMES.has(w),fig:v2fig,head:v2head,CAST:CAST,poseOf:poseOf,drawHuman:drawHuman,drawBrahmaRig:drawBrahmaRig,drawReclineVishnu:drawReclineVishnu,drawArdha:drawArdha,drawShiva:drawShiva,drawHead:drawHead,drawJata:drawJata,POSES:POSES,mixPose:mixPose,SH:SH};
