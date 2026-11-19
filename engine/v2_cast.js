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
const poseOf=(n,who)=>(who==='vishnu'||who==='hayagriva')&&(!n||n==='stand')?poseOf0('vstand'):poseOf0(n);
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
  const sp=Math.max(0,(P.kR[0]-P.kL[0])/2-24),HS=S.female?1.06:1.14,fem=!!S.female;c.save();
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
  if(!o.noHead){c.save();c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);
  if(S.headType==='horse')horseHead(c,P.hd[0],P.hd[1]+10,k,t);
  else{drawHead(c,P.hd[0],P.hd[1],{expr:o.expr||'calm',k:k,S:S,t:t});hairFront(c,S,P.hd[0],P.hd[1]);headgear(c,S,P.hd[0],P.hd[1])}
  c.restore()}
  // arms
  const arm=(sh,hd,sd)=>limbS(c,S,sh,hd,64,62,sd,[fem?15:19,fem?11:15,fem?9:12]);
  const ef=P.ef?-1:1,aL=arm(P.sL,P.hL,-ef),aR=arm(P.sR,P.hR,ef);
  if(S.armlet){armband(c,aL,fem?13:17,S.armlet);armband(c,aR,fem?13:17,S.armlet)}
  [P.sL,P.sR].forEach((s,i)=>{c.fillStyle=S.skin;c.beginPath();c.arc(s[0],s[1],fem?16:21,0,7);c.fill();c.fillStyle='rgba(255,255,255,.14)';c.beginPath();c.arc(s[0]+(i?-4:4),s[1]-6,fem?9:12,0,7);c.fill()});
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
  head(-62,-286+br,.84,true);head(62,-286+br,.84,true);head(0,-292+br,1.04,false);
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

/* ---------- engine glue ---------- */
const V2NAMES=new Set(['harihara','shiva','vishnu','hayagriva','daksha','manu','adishakti','brahmi','madhu','kaitabha','ardha','brahma','vishnu_rest',...[0,1,2,3,4,5,6].map(i=>'rishi'+i)]);
const SCALE={shiva:.62,default:.62};
function v2fig(who,x,y,s,t,o){
  const sc=SCALE[who]||SCALE.default,FR=clamp(o.res||s*SC_,1.4,3.9),RG=[-260,-560,520,620];
  if(who==='vishnu_rest'){glow(x-70*sc*s,y-330*sc*s,420*sc*s,'255,205,100',.30);glow(x-70*sc*s,y-330*sc*s,230*sc*s,'255,232,160',.26)}
  const c=figBegin(FR,OY,RG);if(o.flip<0)c.scale(-1,1);c.scale(sc,sc);
  const ex=o.expr||{},kk=o.k!=null?o.k:(ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0),face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(who==='shiva'){const pn=o.pose==='rage'||o.pose==='lunge'?'rage':'calm',P=mixPose(POSES.calm,POSES.rage,pn==='rage'?1:0);drawShiva(c,{P:P,t:t,rage:kk>.5,k:kk,expr:face==='closed'?'closed':undefined,imp:o.imp||0})}
  else if(who==='brahma')drawBrahmaRig(c,{t:t,k:kk,expr:face});
  else if(who==='vishnu_rest')drawReclineVishnu(c,{t:t});
  else if(who==='ardha')drawArdha(c,{t:t});
  else if(who==='harihara')drawHarihara(c,{t:t});
  else drawHuman(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:(CAST[who].kdef||kk),expr:face,prop:o.prop});
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
  if(who==='shiva'){bust(c,{skin:SH.skin,skinM:SH.skinM,skinD:SH.skinD,skinH:SH.skinH},{beads:true,ash:true,snake:true,armlets:'#e0b04a'});shivaJataSmall(c,t,kk>.5);drawHead(c,0,0,{expr:face==='closed'?'closed':undefined,k:kk,t:t})}
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
