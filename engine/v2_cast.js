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
  const hem=-wy-12,topW=(S.female?44:52)+sp*.22,botW=(S.female?(S.lower.type==='sari'?74:62):60)+sw*4+sp*.7;
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
  c.fillStyle='rgba(255,235,170,.85)';for(let i=-3;i<=3;i++){c.beginPath();c.moveTo(i*8,-60);c.bezierCurveTo(i*18+sw,-20,i*22-sw,40,i*20,110+Math.abs(i)*10);c.bezierCurveTo(i*12,40,i*10,-10,i*8+6,-60);c.fill()}
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

/* ---------- Shesha: the cosmic serpent. Thick sinuous coils with belly scales + five jewelled cobra hoods ---------- */
function drawShesha(c,t){c.save();
  const pearl=['#fbfbff','#dfe4f6','#a9b1d6'],ink='#5a6498';
  glow2(c,-170,-330,300,'200,220,255',.34);
  // coils: three overlapping S-curves forming a heap/bed (bottom → top)
  const coil=(y,amp,half,w,ph,tail)=>{const pts=[];for(let k=0;k<=30;k++){const u=k/30,x=lerp(-half,half,u),yy=y+Math.sin(u*Math.PI*2.2+ph)*amp+(tail&&u>.86?(u-.86)*-160:0);pts.push([x,yy,w*(tail&&u>.8?Math.max(.15,1-(u-.8)*4):1)])}
    const line=(off,col,wm)=>{c.strokeStyle=col;c.lineCap='round';c.lineJoin='round';for(let k=0;k<pts.length-1;k++){c.lineWidth=pts[k][2]*wm;c.beginPath();c.moveTo(pts[k][0],pts[k][1]+off*pts[k][2]);c.lineTo(pts[k+1][0],pts[k+1][1]+off*pts[k+1][2]);c.stroke()}};
    line(0,ink,1.12);line(.02,pearl[2],1);line(-.06,pearl[1],.78);line(-.2,pearl[0],.38);
    c.strokeStyle='rgba(90,100,160,.45)';c.lineWidth=2;for(let k=1;k<pts.length-1;k++){if(k%2)continue;const a=pts[k-1],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d,w2=pts[k][2]*.46;c.beginPath();c.moveTo(pts[k][0]+nx*w2,pts[k][1]+ny*w2);c.lineTo(pts[k][0]-nx*w2,pts[k][1]-ny*w2);c.stroke()}};
  coil(-34,12,340,54,0,true);coil(-86,14,300,50,2.2,false);coil(-136,12,250,46,4.1,false);
  // necks + hoods from the left end of the top coil, arching over Vishnu's head like a canopy
  const base=[-262,-112],H=[[-380,-352,.78],[-318,-424,.92],[-214,-452,1.04],[-108,-424,.92],[-40,-352,.78]];
  H.forEach(([hx,hy,sz],i)=>{const sw=Math.sin(t*1.3+i*1.1)*4,bob=Math.sin(t*1.7+i)*2.5,hx2=hx+sw,hy2=hy+bob;
    const neck=(w,col)=>{c.lineCap='round';c.strokeStyle=col;c.lineWidth=w;c.beginPath();c.moveTo(base[0],base[1]);c.bezierCurveTo(base[0]+(hx-base[0])*.1,base[1]-130,hx2-(hx-base[0])*.05,hy2+150,hx2,hy2+58*sz);c.stroke()};
    neck(30*sz,'#4e5890');neck(25*sz,'#c8cfe8');neck(10*sz,'#f4f6ff');
    c.save();c.translate(hx2,hy2);c.scale(sz,sz);
    const hg=c.createLinearGradient(-58,0,58,0);hg.addColorStop(0,'#9aa4cf');hg.addColorStop(.45,'#fbfcff');hg.addColorStop(1,'#7e88b6');c.fillStyle=hg;c.strokeStyle='#4e5890';c.lineWidth=4;
    c.beginPath();c.moveTo(-12,66);c.bezierCurveTo(-30,44,-60,20,-56,-26);c.bezierCurveTo(-52,-66,-20,-84,0,-84);c.bezierCurveTo(20,-84,52,-66,56,-26);c.bezierCurveTo(60,20,30,44,12,66);c.closePath();c.fill();c.stroke();
    c.strokeStyle='rgba(78,88,144,.35)';c.lineWidth=2;for(let r=0;r<5;r++)for(let q=-2;q<=2;q++){const x=q*20+(r%2)*10,y=-52+r*22;if(Math.abs(x)<48-Math.abs(r-2)*3){c.beginPath();c.arc(x,y,10,.15,Math.PI-.15);c.stroke()}}
    c.strokeStyle='#4e5890';c.lineWidth=3;c.beginPath();c.moveTo(0,-62);c.lineTo(0,56);c.stroke();
    c.fillStyle='#ffe66a';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*15,-30,4.4,5.6,0,0,7);c.fill();c.fillStyle='#1a1020';c.fillRect(sd*15-1,-35,2,10);c.fillStyle='#ffe66a'});
    glow2(c,0,-68,22,'255,70,60',.7);c.fillStyle='#e02a3a';c.beginPath();c.moveTo(0,-80);c.lineTo(7,-68);c.lineTo(0,-56);c.lineTo(-7,-68);c.closePath();c.fill();c.fillStyle='#ffb0b8';c.beginPath();c.arc(-2,-70,1.8,0,7);c.fill();
    c.restore()});
  c.restore()}

/* ---------- Vishnu in yoganidra on Shesha (reclining): the standing rig, rotated, with a hand under the cheek ---------- */
function drawReclineVishnu(c,o){const t=o.t||0,S=Object.assign({},CAST.vishnu,{arms4:false,uttariya:null}),br=Math.sin(t*1.2)*1.6;c.save();
  drawShesha(c,t);
  const ox=250,oy=-196+br,rot=-Math.PI/2+.06;                       // body lies along the top coil, feet to the right
  const tx=(x,y)=>[ox+(x*Math.cos(rot)-y*Math.sin(rot)),oy+(x*Math.sin(rot)+y*Math.cos(rot))];
  // head first (so the propping hand is drawn over its lower edge)
  const hp=tx(2,-482);c.save();c.translate(hp[0]-2,hp[1]-4);c.rotate(-.34);c.scale(1.12,1.12);drawHead(c,0,0,{expr:'closed',k:0,S:S,t:t});hairFront(c,S,0,0);headgear(c,S,0,0);c.restore();
  c.save();c.translate(ox,oy);c.rotate(rot);
  drawHuman(c,S,poseOf('lie','vishnu'),{t:t,noHead:true,expr:'calm'});
  const hp2=poseOf('lie','vishnu');lotusFlower(c,hp2.hR[0]+10,hp2.hR[1]-6,.9);
  c.restore();c.restore()}

/* ---------- Ardhanarishwara: Shiva (right half) joined to Adishakti (left half) ---------- */
function drawArdha(c,o){const t=o.t||0;c.save();c.beginPath();c.rect(0,-900,600,1000);c.clip();drawShiva(c,{P:POSES.calm,t:t,rage:false,k:0,pose:'calm'});c.restore();
  c.save();c.beginPath();c.rect(-600,-900,600,1000);c.clip();drawHuman(c,Object.assign({},CAST.adishakti,{build:1.0}),Object.assign(poseOf('stand'),{}),{t:t,expr:'calm'});c.restore()}

/* ---------- engine glue ---------- */
const V2NAMES=new Set(['shiva','vishnu','hayagriva','daksha','manu','adishakti','brahmi','madhu','kaitabha','ardha','brahma','vishnu_rest',...[0,1,2,3,4,5,6].map(i=>'rishi'+i)]);
const SCALE={shiva:.62,default:.62};
function v2fig(who,x,y,s,t,o){
  const sc=SCALE[who]||SCALE.default,FR=clamp(o.res||s*SC_,1.4,3.9),RG=[-260,-560,520,620];
  const c=figBegin(FR,OY,RG);if(o.flip<0)c.scale(-1,1);c.scale(sc,sc);
  const ex=o.expr||{},kk=o.k!=null?o.k:(ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0),face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  if(who==='shiva'){const pn=o.pose==='rage'||o.pose==='lunge'?'rage':'calm',P=mixPose(POSES.calm,POSES.rage,pn==='rage'?1:0);drawShiva(c,{P:P,t:t,rage:kk>.5,k:kk,expr:face==='closed'?'closed':undefined,imp:o.imp||0})}
  else if(who==='brahma')drawBrahmaRig(c,{t:t,k:kk,expr:face});
  else if(who==='vishnu_rest')drawReclineVishnu(c,{t:t});
  else if(who==='ardha')drawArdha(c,{t:t});
  else drawHuman(c,CAST[who],poseOf(o.pose,who),{t:t,k:o.k!=null?o.k:(CAST[who].kdef||kk),expr:face,prop:o.prop});
  figFinish(c,o,x,y,s,FR,OY,RG,.26,.34,true)}
function v2head(who,x,y,s,t,o){ // close-up of the head and shoulders
  const FR=clamp(s*SC_,2,3.9),RG=[-200,-300,400,420];const c=figBegin(FR,OY,RG);const ex=o.expr||{},kk=ex.brow!=null&&ex.brow<-.2?clamp(-ex.brow*1.1,0,1):0,face=ex.eye!=null&&ex.eye<.5?'closed':'calm';
  c.scale(1.5,1.5);
  if(who==='shiva'){drawJata(c,0,-34,t,kk>.5,0);drawHead(c,0,0,{expr:face==='closed'?'closed':undefined,k:kk,t:t})}
  else if(who==='brahma'){const S=BRAHMA;c.save();c.translate(-50,6);c.scale(.8,.8);drawHead(c,0,0,{expr:face,k:kk,S:S,t:t});c.restore();c.save();c.translate(50,6);c.scale(.8,.8);drawHead(c,0,0,{expr:face,k:kk,S:S,t:t});c.restore();drawHead(c,0,0,{expr:face,k:kk,S:S,t:t});
    c.fillStyle='#e6b84a';c.beginPath();c.moveTo(-26,-24);c.lineTo(-22,-52);c.lineTo(-10,-58);c.lineTo(-5,-96);c.lineTo(0,-128);c.lineTo(5,-96);c.lineTo(10,-58);c.lineTo(22,-52);c.lineTo(26,-24);c.closePath();c.fill()}
  else{const S=CAST[who];if(S.headType==='horse')horseHead(c,0,10,kk,t);else{if(S.hair&&S.hair.type==='long'){hairBack(c,S,{hd:[0,0],ph:[0,200]},t)}drawHead(c,0,0,{expr:face,k:o.k!=null?o.k:(S.kdef||kk),S:S,t:t});hairFront(c,S,0,0);headgear(c,S,0,0)}}
  figFinish(c,o,x,y,s,FR,OY,RG,.26,.34,false)}
return {has:w=>V2NAMES.has(w),fig:v2fig,head:v2head,CAST:CAST,poseOf:poseOf,drawHuman:drawHuman,drawBrahmaRig:drawBrahmaRig,drawReclineVishnu:drawReclineVishnu,drawArdha:drawArdha,drawShiva:drawShiva,drawHead:drawHead,drawJata:drawJata,POSES:POSES,mixPose:mixPose,SH:SH};
