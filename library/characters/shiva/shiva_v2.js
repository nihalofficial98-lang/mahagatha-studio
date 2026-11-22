/* Shiva v2 — reference design (standalone canvas drawing; origin = between the feet, y up is negative).
   Identity cues: ash-blue skin, tripundra + third eye, jata with crescent moon,
   serpent around neck, TIGER-SKIN wrap, rudraksha mala, trident with damaru. */
const SH={skin:'#7c8fd0',skinM:'#6477b8',skinD:'#3d4a88',skinH:'#9fb0e6',hair:'#14121f',hairH:'#3a3550',
  tiger:'#d98a2b',tigerD:'#a8601a',tigerL:'#f0b050',stripe:'#1a1008',ash:'#e8e4ee',gold:'#e0b04a',goldD:'#a87820',
  snake:'#2f5a48',snakeL:'#6aa890',bead:'#6a3a20',cloth:'#efe8f4',red:'#e0402a',water:'#bfe6f5'};
const lerp=(a,b,t)=>a+(b-a)*t, rad=d=>d*Math.PI/180;
const INKC='#1e0d24';
const skinPK=S=>({b:S.skin,h:S.skinH||S.skin,d:S.skinD||S.skin,m:S.skinM||S.skin});
function inkCap(c,a,b,ra,rb,e){e=e==null?2.4:e;const an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.fillStyle=INKC;c.beginPath();c.arc(a[0],a[1],ra+e,an+Math.PI/2,an+Math.PI*1.5);c.arc(b[0],b[1],rb+e,an-Math.PI/2,an+Math.PI/2);c.closePath();c.fill()}
function crPts(P,n){const o=[];for(let i=0;i<P.length-1;i++){const p0=P[Math.max(0,i-1)],p1=P[i],p2=P[i+1],p3=P[Math.min(P.length-1,i+2)];for(let k=0;k<n;k++){const u=k/n,u2=u*u,u3=u2*u;o.push([.5*((2*p1[0])+(-p0[0]+p2[0])*u+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*u2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*u3),.5*((2*p1[1])+(-p0[1]+p2[1])*u+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*u2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*u3)])}}o.push(P[P.length-1]);return o}
function tapered(c,a,b,wa,wb,col){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;
  c.fillStyle=col;c.beginPath();c.moveTo(a[0]+nx*wa,a[1]+ny*wa);c.lineTo(b[0]+nx*wb,b[1]+ny*wb);c.lineTo(b[0]-nx*wb,b[1]-ny*wb);c.lineTo(a[0]-nx*wa,a[1]-ny*wa);c.closePath();c.fill();
  c.beginPath();c.arc(a[0],a[1],wa,0,7);c.arc(b[0],b[1],wb,0,7);c.fill()}
function elbow(S,T,l1,l2,side){const dx=T[0]-S[0],dy=T[1]-S[1];let d=Math.hypot(dx,dy);const m=l1+l2-0.5;if(d>m){T=[S[0]+dx*m/d,S[1]+dy*m/d];d=m}
  const a=(l1*l1-l2*l2+d*d)/(2*d),h=Math.sqrt(Math.max(0,l1*l1-a*a)),ux=(T[0]-S[0])/d,uy=(T[1]-S[1])/d;
  return {e:[S[0]+ux*a+side*(-uy)*h,S[1]+uy*a+side*ux*h],t:T}}
function limbShaded(c,S,T,l1,l2,side,w){const r=elbow(S,T,l1,l2,side),E=r.e;inkCap(c,S,E,w[0],w[1]);inkCap(c,E,r.t,w[1],w[2]);
  tapered(c,S,E,w[0],w[1],SH.skin);tapered(c,E,r.t,w[1],w[2],SH.skin);
  // shadow side
  c.globalAlpha=.45;const sd=(p,q,wa,wb)=>{const dx=q[0]-p[0],dy=q[1]-p[1],d=Math.hypot(dx,dy)||1,nx=-dy/d*side,ny=dx/d*side;
    c.fillStyle=SH.skinD;c.beginPath();c.moveTo(p[0]+nx*wa*0.1,p[1]+ny*wa*0.1);c.lineTo(q[0]+nx*wb*0.1,q[1]+ny*wb*0.1);c.lineTo(q[0]+nx*wb,q[1]+ny*wb);c.lineTo(p[0]+nx*wa,p[1]+ny*wa);c.fill()};
  sd(S,E,w[0],w[1]);sd(E,r.t,w[1],w[2]);c.globalAlpha=1;
  // bicep highlight
  c.fillStyle=SH.skinH;c.globalAlpha=.22;c.beginPath();c.ellipse(lerp(S[0],E[0],.4),lerp(S[1],E[1],.4),w[0]*.45,w[0]*.9,Math.atan2(E[1]-S[1],E[0]-S[0])+1.57,0,7);c.fill();c.globalAlpha=1;
  return r}
function hand(c,p,ang,grip){PK.hand(c,skinPK(SH),p,ang+Math.PI,grip?'hold':'rest')}
function armlet(c,r,w,col){const E=r.e,S=r.s;const x=lerp(S[0],E[0],.5),y=lerp(S[1],E[1],.5);c.save();c.translate(x,y);c.rotate(Math.atan2(E[1]-S[1],E[0]-S[0])+1.57);c.fillStyle=col;c.beginPath();c.ellipse(0,0,w+1.5,4,0,0,7);c.fill();c.fillStyle='rgba(0,0,0,.25)';c.beginPath();c.ellipse(0,2,w+1.5,2,0,0,7);c.fill();c.restore()}

function drawTiger(c,wx,wy,hem,sway,rage,sp=0){ // tiger-skin wrap from waist to knee; sp = leg spread so the wrap always covers the thighs
  c.save();const topW=54+sp*.25,botW=62+sway*4+sp*.62;
  c.beginPath();c.moveTo(-topW,wy);c.lineTo(topW,wy);c.lineTo(botW+4,wy+hem*0.6);
  // ragged fur hem
  const n=9;for(let i=0;i<=n;i++){const u=i/n,x=lerp(botW+4,-botW-10,u),y=wy+hem+((i%2)?10:-4)+Math.sin(u*5+sway)*4;c.lineTo(x,y)}
  c.lineTo(-topW-8,wy+hem*0.5);c.closePath();
  const g=c.createLinearGradient(-60,0,60,0);g.addColorStop(0,SH.tigerL);g.addColorStop(.45,SH.tiger);g.addColorStop(1,SH.tigerD);c.fillStyle=g;c.fill();c.strokeStyle=INKC;c.lineWidth=2.6;c.lineJoin='round';c.stroke();c.clip();
  // stripes (tapered black wedges) following the drape
  c.fillStyle=SH.stripe;for(let i=0;i<22;i++){const u=(i%11)/10,row=Math.floor(i/11);const x=lerp(-botW*(.55+.4*row),botW*(.55+.4*row),u)+row*5-3,y=wy+8+row*hem*0.42+(i%3)*6;
    const len=26+((i*7)%14),ang=(u-.5)*0.55+(row?.1:-.1);c.save();c.translate(x,y);c.rotate(ang);c.beginPath();c.moveTo(-3,0);c.quadraticCurveTo(4,len*.5,0,len);c.quadraticCurveTo(-1,len*.5,-3,0);c.fill();
    c.beginPath();c.moveTo(7,6);c.quadraticCurveTo(13,len*.35,9,len*.7);c.quadraticCurveTo(7,len*.35,7,6);c.fill();c.restore()}
  // fold shading
  c.fillStyle='rgba(60,20,0,.28)';c.beginPath();c.moveTo(topW,wy);c.lineTo(botW+10,wy+hem+10);c.lineTo(12,wy+hem+6);c.quadraticCurveTo(24,wy+hem*.4,10,wy);c.fill();
  c.fillStyle='rgba(255,230,160,.18)';c.beginPath();c.moveTo(-topW,wy);c.lineTo(-14,wy);c.quadraticCurveTo(-30,wy+hem*.5,-48,wy+hem);c.lineTo(-botW-8,wy+hem);c.closePath();c.fill();
  c.restore();
  // rope belt + knot
  c.fillStyle='#5a3a22';c.beginPath();c.roundRect(-topW-3,wy-7,2*topW+6,11,5);c.fill();c.strokeStyle='rgba(255,220,160,.35)';c.lineWidth=1.4;for(let i=-5;i<=5;i++){c.beginPath();c.moveTo(i*11-3,wy-6);c.lineTo(i*11+3,wy+3);c.stroke()}
  c.fillStyle='#4a2c18';c.beginPath();c.arc(8,wy+8,7,0,7);c.fill();c.beginPath();c.moveTo(4,wy+10);c.lineTo(-2,wy+44+sway*3);c.lineTo(5,wy+42+sway*3);c.lineTo(10,wy+12);c.fill()}

function drawSerpent(c,t,rage,L,R){ // Vasuki: coiled round the neck, hood rising over the right shoulder
  const w=Math.sin(t*2)*2,VS={b:'#3c9a4c',d:'#1c5a2c',l:'#9ce68a',belly:'#f6e48e',bellyD:'#c8a040'};
  const pts=crPts([[L[0]-8,L[1]+4],[L[0]+8,L[1]+30],[-12,L[1]+46],[16,L[1]+42],[R[0]-10,L[1]+22],[R[0]+4,L[1]+2],[R[0]+12,L[1]-14+w]],5);
  PK.tube(c,pts,9,7,VS,{scales:false,belly:1});
  PK.hood(c,R[0]+14,L[1]-62+w,.18+Math.sin(t*1.4)*.1,.5,t,VS,{ph:2,eye:rage?'#ff5a3a':'#ffd34a'})}

function drawJata(c,hx,hy,t,rage,imp=0){ // jata: hanging locks, coiled bun, crescent moon, and Ganga flowing down along the locks
  c.save();c.translate(hx,hy);const spread=rage?1.12+imp*0.12:1;
  const rope=(x0,y0,x1,y1,x2,y2,w,ph)=>{const dx=Math.sin(t*2.1+ph)*(4+imp*5),dx2=Math.sin(t*2.6+ph*1.7)*(6+imp*8);const f=cc=>{cc.moveTo(x0,y0);cc.quadraticCurveTo(x1+dx,y1,x2+dx2,y2)};
    PK.stroke(c,f,INKC,w+4.4);PK.stroke(c,f,ph%2?'#3a2c4e':'#2a2038',w);PK.stroke(c,f,'rgba(190,170,230,.3)',w*.26,{dash:[w*.9,w*.7]})};
  [-1,1].forEach((sd,k)=>{for(let i=0;i<4;i++){rope(sd*(12+i*7),-6+i*3,sd*(58+i*14)*spread,40+i*8,sd*(52+i*16)*spread+sd*imp*6,150-i*14-imp*6,13-i*1.4,i+k*2)}});
  // bun
  PK.cut(c,PK.P.ell(0,-66,41,53),PK.lg(c,-42,0,42,0,['#55446e','#2c2242','#140e20']),{lw:2.6});
  c.save();c.beginPath();PK.P.ell(0,-66,41,53)(c);c.clip();for(let i=0;i<7;i++){PK.stroke(c,cc=>cc.ellipse(0,-66-i*2,38-i*5,50-i*6.6,0,Math.PI*(1.1+i*.13),Math.PI*(2.6+i*.13)),i%2?'rgba(190,170,240,.35)':'rgba(6,4,14,.6)',3)}c.restore();
  PK.cut(c,PK.P.ell(0,-114,9,10),PK.lg(c,-9,0,9,0,['#55446e','#140e20']),{lw:1.8,sh:0});
  PK.cut(c,cc=>cc.roundRect(-34,-27,68,10,4),PK.goldG(c,-34,34),{lw:1.6,sh:0});for(let k=-2;k<=2;k++)PK.gem(c,k*12,-22,2.4,k%2?'#18a57a':'#e0234a');
  // crescent moon
  PK.glow(c,-18,-92,46,'230,240,255',.5);PK.cut(c,cc=>{cc.arc(-18,-92,16,Math.PI*.35,Math.PI*1.75);cc.arc(-12,-96,12,Math.PI*1.62,Math.PI*.45,true);cc.closePath()},PK.lg(c,-34,-108,-4,-76,['#ffffff','#f4ecc8']),{lw:1.5,sh:0});
  c.restore()}

const SHIVA_FACE={skin:SH.skin,skinM:SH.skinM,skinD:SH.skinD,skinH:SH.skinH,gold:SH.gold,ash:SH.ash,red:SH.red,tripundra:true,third:true,brow:'#0b0a14'};
function drawHead(c,hx,hy,o){ // o:{expr:'calm'|'closed'|'rage', k:0..1 anger, S:face spec, mood:{blink,smile,sad,surp,mouth,lx,ly}, t}
  const S=o.S||SHIVA_FACE,M=o.mood||{},e=o.expr||'calm',k=e==='rage'?1:(e==='calm'?(o.k||0):0),t=o.t||0;
  const bl=Math.max(M.blink||0,e==='closed'?1:0,((t*.37)%1)<.03?1:0),tri=S.third&&S.tripundra!==false;
  c.save();c.translate(hx,hy);
  PK.face(c,{skin:skinPK(S),t:t,turn:o.turn||0,must:S.mustache,blink:bl,mouth:M.mouth||0,smile:M.smile==null?(S.female?.5:.3):M.smile,lx:M.lx||0,ly:M.ly||0,anger:k,sad:M.sad||0,surp:M.surp||0,
    tilak:tri?'tripundra':(S.tilak==='vaishnava'?'vaishnava':(S.tilak==='ash'?'tripundra':null)),bindi:S.bindi||S.tilak==='dot',third:tri?k:null,beard:S.beard,beardLen:S.beardLen,
    browCol:S.brow,lip:S.female?'#c4384a':(S.lip||'#a8384e'),eyeRed:S.eyeRed,kgem:S.kgem||(S.female?'#18a57a':undefined)});
  c.restore()}

function drawTrishul(c,x,top,bot,t,rage){PK.trishul(c,x,bot,-top,t,0)}

/* poses: joints in local space */
const POSES={
 calm:{ph:[0,-262],ch:[0,-388],nk:[0,-428],hd:[0,-478],sL:[-64,-402],sR:[64,-402],hL:[-92,-248],hR:[92,-300],hipL:[-24,-258],hipR:[24,-258],kL:[-34,-130],kR:[32,-130],fL:[-40,0],fR:[40,0],tri:{x:98,top:-640,bot:0},lean:0,hem:150,sway:0},
 rage:{ph:[6,-250],ch:[-4,-372],nk:[-8,-410],hd:[-10,-458],sL:[-66,-388],sR:[60,-388],hL:[-150,-452],hR:[140,-318],hipL:[-26,-248],hipR:[34,-246],kL:[-74,-128],kR:[80,-120],fL:[-110,0],fR:[118,0],tri:{x:140,top:-610,bot:-20,rot:0.18},lean:-0.05,hem:140,sway:3}
};
function mixPose(a,b,u){const m=(x,y)=>Array.isArray(x)?x.map((v,i)=>m(v,y[i])):(typeof x==='number'?x+(y-x)*u:(u<.5?x:y));const o={};for(const k in a)o[k]=(a[k]&&typeof a[k]==='object'&&!Array.isArray(a[k]))?mixPose(a[k],b[k]||a[k],u):m(a[k],b[k]===undefined?a[k]:b[k]);return o}
const easeIO=x=>{x=Math.max(0,Math.min(1,x));return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
function drawShiva(c,o){
  const P0=o.P||POSES[o.pose||'calm'],t=o.t||0,br=Math.sin(t*1.7)*2.4,P=JSON.parse(JSON.stringify(P0));['ch','nk','hd','sL','sR'].forEach(k=>{P[k][1]+=br});P.hL[1]+=br*.6;P.hR[1]+=br*.6;const rage=(o.rage!==undefined?o.rage:o.pose==='rage'),sw=Math.sin(t*1.5)+P.sway;c.save();
  // jata strands behind
  const HS=1.18;c.save();c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);c.save();c.translate(P.hd[0],P.hd[1]-30);c.scale(.74,.7);c.translate(-P.hd[0],-P.hd[1]+30);drawJata(c,P.hd[0],P.hd[1]-34,t,rage,o.imp||0);c.restore();c.restore();
  // legs
  const stance=(h,k,f,side)=>{const r=elbow(h,f,86,92,side);inkCap(c,h,r.e,31,23);inkCap(c,r.e,f,23,14);tapered(c,h,r.e,31,23,SH.skin);tapered(c,r.e,f,23,14,SH.skin);c.fillStyle='rgba(255,255,255,.10)';c.beginPath();c.ellipse(lerp(r.e[0],f[0],.35)-side*2,lerp(r.e[1],f[1],.35),9,26,Math.atan2(f[1]-r.e[1],f[0]-r.e[0])+1.57,0,7);c.fill();
    c.globalAlpha=.4;c.fillStyle=SH.skinD;tapered(c,[h[0]+side*10,h[1]],[r.e[0]+side*8,r.e[1]],9,8,SH.skinD);tapered(c,[r.e[0]+side*7,r.e[1]],[f[0]+side*6,f[1]-6],8,6,SH.skinD);c.globalAlpha=1;
    c.fillStyle=SH.skinM;c.beginPath();c.ellipse(f[0]+side*4,f[1]-3,19,8,0,0,7);c.fill();c.fillStyle=SH.skinD;c.globalAlpha=.4;c.beginPath();c.ellipse(f[0]+side*6,f[1]-1,13,4,0,0,7);c.fill();c.globalAlpha=1};
  stance(P.hipL,P.kL,P.fL,-1);stance(P.hipR,P.kR,P.fR,1);
  // trident behind right hand
  const T=P.tri;c.save();if(T.rot){c.translate(T.x,-300);c.rotate(T.rot);c.translate(-T.x,300)}drawTrishul(c,T.x,T.top,T.bot,t,rage);c.restore();
  // torso
  const tg=c.createLinearGradient(-60,0,60,0);tg.addColorStop(0,SH.skinH);tg.addColorStop(.3,SH.skin);tg.addColorStop(1,SH.skinD);c.fillStyle=tg;
  c.beginPath();c.moveTo(P.sL[0]-6,P.sL[1]+4);c.bezierCurveTo(-52,P.sL[1]+34,-46,P.ch[1]+64,-36,P.ph[1]-6);c.lineTo(36,P.ph[1]-6);c.bezierCurveTo(46,P.ch[1]+64,52,P.sR[1]+34,P.sR[0]+6,P.sR[1]+4);c.bezierCurveTo(30,P.nk[1]+4,-30,P.nk[1]+4,P.sL[0]-6,P.sL[1]+4);c.fill();c.strokeStyle=INKC;c.lineWidth=2.6;c.lineJoin='round';c.stroke();
  // muscle definition
  c.strokeStyle='rgba(20,24,70,.38)';c.lineWidth=2.4;c.lineCap='round';
  c.beginPath();c.moveTo(0,P.nk[1]+24);c.lineTo(0,P.ph[1]-18);c.stroke();
  [-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*5,P.ch[1]+2);c.bezierCurveTo(sd*26,P.ch[1]+22,sd*44,P.ch[1]+10,sd*46,P.ch[1]-14);c.stroke();
    for(let i=0;i<3;i++){c.beginPath();c.moveTo(sd*4,P.ph[1]-86+i*22);c.quadraticCurveTo(sd*18,P.ph[1]-80+i*22,sd*26,P.ph[1]-86+i*22);c.stroke()}
    c.beginPath();c.moveTo(sd*40,P.ch[1]+24);c.quadraticCurveTo(sd*34,P.ch[1]+60,sd*30,P.ph[1]-30);c.stroke()});
  c.fillStyle='rgba(255,255,255,.12)';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*22,P.ch[1]+6,20,14,sd*-0.2,0,7);c.fill()});
  // vibhuti (ash) bands across chest
  c.strokeStyle=SH.ash;c.lineWidth=4;c.globalAlpha=.9;[0,1,2].forEach(i=>{c.beginPath();c.moveTo(-34+i*0.5,P.ch[1]+34+i*8);c.quadraticCurveTo(0,P.ch[1]+44+i*8,34-i*0.5,P.ch[1]+34+i*8);c.stroke()});c.globalAlpha=1;
  // tiger skin
  drawTiger(c,0,P.ph[1]-4,P.hem,sw,rage,Math.max(0,(P.kR[0]-P.kL[0])/2-24));
  // rudraksha mala
  c.fillStyle=SH.bead;for(let i=0;i<15;i++){const u=i/14,bx=-36+u*72,by=P.nk[1]+16+Math.sin(u*3.14)*50;c.beginPath();c.arc(bx,by,4.8,0,7);c.fill();c.fillStyle='rgba(255,220,170,.4)';c.beginPath();c.arc(bx-1.4,by-1.4,1.4,0,7);c.fill();c.fillStyle=SH.bead}
  // neck
  c.fillStyle=SH.skinM;c.beginPath();c.roundRect(P.nk[0]-16,P.hd[1]+30,32,P.nk[1]-P.hd[1]+4,8);c.fill();
  drawSerpent(c,t,rage,P.sL,P.sR);
  c.save();c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);drawHead(c,P.hd[0],P.hd[1],{expr:o.expr||(o.k!==undefined?'calm':(rage?'rage':'calm')),k:o.k,t});c.restore();
  // arms (on top)
  const aL=limbShaded(c,P.sL,P.hL,64,62,-1,[19,15,12]);aL.s=P.sL;const aR=limbShaded(c,P.sR,P.hR,64,62,1,[19,15,12]);aR.s=P.sR;
  armlet(c,aL,17,SH.gold);armlet(c,aR,17,SH.gold);
  [aL,aR].forEach((r,i)=>{c.fillStyle=SH.snake;c.beginPath();c.ellipse(lerp(r.e[0],r.t[0],.78),lerp(r.e[1],r.t[1],.78),13,5,Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0])+1.57,0,7);c.fill()});
  // shoulder pads: deltoids
  [P.sL,P.sR].forEach((s,i)=>{c.fillStyle=SH.skin;c.beginPath();c.arc(s[0],s[1],21,0,7);c.fill();c.fillStyle='rgba(255,255,255,.14)';c.beginPath();c.arc(s[0]+(i?-4:4),s[1]-6,12,0,7);c.fill()});
  hand(c,aL.t,rage?0.3:0.1,rage);hand(c,aR.t,0,true);
  // trident grip: re-draw fingers over shaft
  c.fillStyle=SH.skinM;c.beginPath();c.ellipse(aR.t[0],aR.t[1],12,10,0,0,7);c.fill();c.fillStyle=SH.skin;[-8,-3,2,7].forEach(y=>{c.beginPath();c.roundRect(aR.t[0]-13,aR.t[1]+y-2.6,26,5.6,3);c.fill()});
  c.restore()}

function drawDamaru(c,sw=0){c.save();
  const g=c.createLinearGradient(-30,0,30,0);g.addColorStop(0,'#d89a4a');g.addColorStop(.5,'#b8742e');g.addColorStop(1,'#7a4a22');c.fillStyle=g;
  [-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*26,-22);c.quadraticCurveTo(sd*8,-5,sd*3,0);c.quadraticCurveTo(sd*8,5,sd*26,22);c.closePath();c.fill()});
  c.fillStyle='#ecd9a8';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*26,0,5,22,0,0,7);c.fill();c.strokeStyle='#7a4a22';c.lineWidth=2;c.stroke()});
  c.strokeStyle='#e8d4a0';c.lineWidth=2;c.beginPath();for(let i=-3;i<=3;i++){c.moveTo(-26,i*6);c.quadraticCurveTo(0,i*1.5,26,i*6)}c.stroke();
  c.fillStyle='#8a1f1a';c.fillRect(-4,-4,8,8);
  c.strokeStyle=SH.red;c.lineWidth=2.6;c.beginPath();c.moveTo(0,3);c.quadraticCurveTo(26+sw,18,30+sw,44);c.stroke();c.fillStyle='#f0e0b0';c.beginPath();c.arc(30+sw,46,4.4,0,7);c.fill();c.restore()}
function drawSerpentHead(c,t){c.save();const w=Math.sin(t*2)*2;
  c.strokeStyle=SH.snake;c.lineWidth=18;c.lineCap='round';c.beginPath();c.moveTo(-80,150);c.bezierCurveTo(-70,90,-60,170,-20,110);c.bezierCurveTo(10,70,-20,30,0,10);c.stroke();
  c.strokeStyle=SH.snakeL;c.lineWidth=3;c.setLineDash([2,10]);c.beginPath();c.moveTo(-80,145);c.bezierCurveTo(-70,85,-60,165,-20,105);c.bezierCurveTo(10,65,-20,25,0,5);c.stroke();c.setLineDash([]);
  c.fillStyle=SH.snake;c.beginPath();c.moveTo(-30,20);c.bezierCurveTo(-52,-20,-36,-70,0,-76);c.bezierCurveTo(36,-70,52,-20,30,20);c.closePath();c.fill();
  c.fillStyle=SH.snakeL;c.globalAlpha=.5;c.beginPath();c.ellipse(0,-34,13,32,0,0,7);c.fill();c.globalAlpha=1;
  c.strokeStyle='#2a1a10';c.lineWidth=2.2;c.beginPath();c.moveTo(-14,-40);c.bezierCurveTo(-8,-52,8,-52,14,-40);c.stroke();
  c.fillStyle='#f0e060';[-9,9].forEach(x=>{c.beginPath();c.ellipse(x,-24,4,5.6,0,0,7);c.fill();c.fillStyle='#111';c.fillRect(x-1,-28,2,8);c.fillStyle='#f0e060'});
  c.strokeStyle='#d02a2a';c.lineWidth=2;c.beginPath();c.moveTo(0,-6);c.lineTo(0,6);c.moveTo(0,6);c.lineTo(-5,13);c.moveTo(0,6);c.lineTo(5,13);c.stroke();c.restore()}
