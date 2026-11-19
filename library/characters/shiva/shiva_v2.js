/* Shiva v2 — reference design (standalone canvas drawing; origin = between the feet, y up is negative).
   Identity cues: ash-blue skin, tripundra + third eye, jata with crescent moon,
   serpent around neck, TIGER-SKIN wrap, rudraksha mala, trident with damaru. */
const SH={skin:'#7c8fd0',skinM:'#6477b8',skinD:'#3d4a88',skinH:'#9fb0e6',hair:'#14121f',hairH:'#3a3550',
  tiger:'#d98a2b',tigerD:'#a8601a',tigerL:'#f0b050',stripe:'#1a1008',ash:'#e8e4ee',gold:'#e0b04a',goldD:'#a87820',
  snake:'#2f5a48',snakeL:'#6aa890',bead:'#6a3a20',cloth:'#efe8f4',red:'#e0402a',water:'#bfe6f5'};
const lerp=(a,b,t)=>a+(b-a)*t, rad=d=>d*Math.PI/180;
function tapered(c,a,b,wa,wb,col){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;
  c.fillStyle=col;c.beginPath();c.moveTo(a[0]+nx*wa,a[1]+ny*wa);c.lineTo(b[0]+nx*wb,b[1]+ny*wb);c.lineTo(b[0]-nx*wb,b[1]-ny*wb);c.lineTo(a[0]-nx*wa,a[1]-ny*wa);c.closePath();c.fill();
  c.beginPath();c.arc(a[0],a[1],wa,0,7);c.arc(b[0],b[1],wb,0,7);c.fill()}
function elbow(S,T,l1,l2,side){const dx=T[0]-S[0],dy=T[1]-S[1];let d=Math.hypot(dx,dy);const m=l1+l2-0.5;if(d>m){T=[S[0]+dx*m/d,S[1]+dy*m/d];d=m}
  const a=(l1*l1-l2*l2+d*d)/(2*d),h=Math.sqrt(Math.max(0,l1*l1-a*a)),ux=(T[0]-S[0])/d,uy=(T[1]-S[1])/d;
  return {e:[S[0]+ux*a+side*(-uy)*h,S[1]+uy*a+side*ux*h],t:T}}
function limbShaded(c,S,T,l1,l2,side,w){const r=elbow(S,T,l1,l2,side),E=r.e;
  tapered(c,S,E,w[0],w[1],SH.skin);tapered(c,E,r.t,w[1],w[2],SH.skin);
  // shadow side
  c.globalAlpha=.45;const sd=(p,q,wa,wb)=>{const dx=q[0]-p[0],dy=q[1]-p[1],d=Math.hypot(dx,dy)||1,nx=-dy/d*side,ny=dx/d*side;
    c.fillStyle=SH.skinD;c.beginPath();c.moveTo(p[0]+nx*wa*0.1,p[1]+ny*wa*0.1);c.lineTo(q[0]+nx*wb*0.1,q[1]+ny*wb*0.1);c.lineTo(q[0]+nx*wb,q[1]+ny*wb);c.lineTo(p[0]+nx*wa,p[1]+ny*wa);c.fill()};
  sd(S,E,w[0],w[1]);sd(E,r.t,w[1],w[2]);c.globalAlpha=1;
  // bicep highlight
  c.fillStyle=SH.skinH;c.globalAlpha=.22;c.beginPath();c.ellipse(lerp(S[0],E[0],.4),lerp(S[1],E[1],.4),w[0]*.45,w[0]*.9,Math.atan2(E[1]-S[1],E[0]-S[0])+1.57,0,7);c.fill();c.globalAlpha=1;
  return r}
function hand(c,p,ang,grip){c.save();c.translate(p[0],p[1]);c.rotate(ang);c.fillStyle=SH.skinM;c.beginPath();c.ellipse(0,0,10,12,0,0,7);c.fill();
  if(!grip){c.fillStyle=SH.skin;[-6,-2,2,6].forEach((x,i)=>{c.beginPath();c.ellipse(x,11+Math.abs(x)*0.1,3,8,0,0,7);c.fill()})}
  c.fillStyle=SH.skinD;c.globalAlpha=.4;c.beginPath();c.ellipse(4,2,6,9,0,0,7);c.fill();c.globalAlpha=1;c.restore()}
function armlet(c,r,w,col){const E=r.e,S=r.s;const x=lerp(S[0],E[0],.5),y=lerp(S[1],E[1],.5);c.save();c.translate(x,y);c.rotate(Math.atan2(E[1]-S[1],E[0]-S[0])+1.57);c.fillStyle=col;c.beginPath();c.ellipse(0,0,w+1.5,4,0,0,7);c.fill();c.fillStyle='rgba(0,0,0,.25)';c.beginPath();c.ellipse(0,2,w+1.5,2,0,0,7);c.fill();c.restore()}

function drawTiger(c,wx,wy,hem,sway,rage,sp=0){ // tiger-skin wrap from waist to knee; sp = leg spread so the wrap always covers the thighs
  c.save();const topW=54+sp*.25,botW=62+sway*4+sp*.62;
  c.beginPath();c.moveTo(-topW,wy);c.lineTo(topW,wy);c.lineTo(botW+4,wy+hem*0.6);
  // ragged fur hem
  const n=9;for(let i=0;i<=n;i++){const u=i/n,x=lerp(botW+4,-botW-10,u),y=wy+hem+((i%2)?10:-4)+Math.sin(u*5+sway)*4;c.lineTo(x,y)}
  c.lineTo(-topW-8,wy+hem*0.5);c.closePath();
  const g=c.createLinearGradient(-60,0,60,0);g.addColorStop(0,SH.tigerL);g.addColorStop(.45,SH.tiger);g.addColorStop(1,SH.tigerD);c.fillStyle=g;c.fill();c.clip();
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

function drawSerpent(c,t,rage,L,R){ // Vasuki around the neck, hood over right shoulder
  const w=Math.sin(t*2)*2;c.save();c.lineCap='round';
  c.strokeStyle=SH.snake;c.lineWidth=15;c.beginPath();c.moveTo(L[0]-6,L[1]+8);c.bezierCurveTo(L[0]+10,L[1]+34,-14,L[1]+44,12,L[1]+30);c.bezierCurveTo(34,L[1]+20,R[0]-6,L[1]+4,R[0]+10,L[1]-16+w);c.stroke();
  c.strokeStyle='rgba(255,255,255,.0)';c.strokeStyle=SH.snakeL;c.lineWidth=3;c.setLineDash([2,9]);c.beginPath();c.moveTo(L[0]-6,L[1]+3);c.bezierCurveTo(L[0]+10,L[1]+29,-14,L[1]+39,12,L[1]+25);c.bezierCurveTo(34,L[1]+15,R[0]-6,L[1]-1,R[0]+10,L[1]-21+w);c.stroke();c.setLineDash([]);
  // hood + head
  const hx=R[0]+10,hy=L[1]-22+w;c.fillStyle=SH.snake;c.beginPath();c.moveTo(hx-12,hy+6);c.bezierCurveTo(hx-22,hy-14,hx-8,hy-34,hx+4,hy-36);c.bezierCurveTo(hx+22,hy-34,hx+30,hy-14,hx+16,hy+6);c.closePath();c.fill();
  c.fillStyle=SH.snakeL;c.globalAlpha=.55;c.beginPath();c.ellipse(hx+2,hy-16,7,14,0,0,7);c.fill();c.globalAlpha=1;
  c.fillStyle='#f0e060';c.beginPath();c.ellipse(hx-3,hy-24,2.6,3.6,0,0,7);c.ellipse(hx+9,hy-24,2.6,3.6,0,0,7);c.fill();
  if(rage){c.strokeStyle='#d02a2a';c.lineWidth=1.6;c.beginPath();c.moveTo(hx+3,hy-8);c.lineTo(hx+3,hy+2);c.moveTo(hx+3,hy+2);c.lineTo(hx-1,hy+8);c.moveTo(hx+3,hy+2);c.lineTo(hx+7,hy+8);c.stroke()}
  c.restore()}

const PHS='../library/pilot/assets/sp_hc_';
function PHok(){const g=window.imgGetV2;return !!g&&g(PHS+'open.png').ok&&g(PHS+'closed.png').ok&&g(PHS+'rage.png').ok}
function PH(c,hx,hy,expr,k){ // approved painted Shiva head (jata, moon, third eye) on the coded body
  if(!PHok())return false;const g=window.imgGetV2,KS=.72,draw=(n,a)=>{const e=g(PHS+n+'.png'),w=e.img.width*KS,h=e.img.height*KS;c.save();c.globalAlpha*=a;c.drawImage(e.img,hx-w*.52,hy+60-h,w,h);c.restore()};
  if(expr==='closed')draw('closed',1);else{const kk=expr==='rage'?1:(k||0);draw('open',kk>=.98?0:1-Math.min(1,kk)*.9);if(kk>0)draw('rage',Math.min(1,kk))}return true}
function drawJata(c,hx,hy,t,rage,imp=0){ // bun of coiled jata + hanging ropes, crescent moon
  c.save();c.translate(hx,hy);const sw=Math.sin(t*1.6)*2;
  const rope=(x0,y0,x1,y1,x2,y2,w,ph)=>{ // one rope strand with a light twist highlight
    const dx=Math.sin(t*2.1+ph)*(4+imp*5),dx2=Math.sin(t*2.6+ph*1.7)*(6+imp*8);
    c.lineCap='round';c.strokeStyle='#15122a';c.lineWidth=w;c.beginPath();c.moveTo(x0,y0);c.quadraticCurveTo(x1+dx,y1,x2+dx2,y2);c.stroke();
    c.strokeStyle='rgba(200,190,240,.22)';c.lineWidth=w*.28;c.setLineDash([w*.9,w*.7]);c.beginPath();c.moveTo(x0-w*.2,y0);c.quadraticCurveTo(x1+dx-w*.2,y1,x2+dx2-w*.2,y2);c.stroke();c.setLineDash([])};
  const spread=rage?1.12+imp*0.12:1;
  [-1,1].forEach((sd,k)=>{for(let i=0;i<4;i++){rope(sd*(12+i*7),-6+i*3,sd*(58+i*14)*spread,40+i*8,sd*(52+i*16)*spread+sd*imp*6,150-i*14-imp*6,13-i*1.4,i+k*2)}});
  // topknot of thick matted locks: irregular, swaying, with twist marks
  const sway=Math.sin(t*1.3)*2.5;
  const lock=(x0,y0,cx,cy,x1,y1,w,col)=>{
    const P=(u)=>[(1-u)*(1-u)*x0+2*(1-u)*u*cx+u*u*(x1+sway*u),(1-u)*(1-u)*y0+2*(1-u)*u*cy+u*u*y1];
    c.lineCap='round';c.lineJoin='round';
    c.strokeStyle='#0a0816';c.lineWidth=w+5;c.beginPath();c.moveTo(x0,y0);c.quadraticCurveTo(cx,cy,x1+sway,y1);c.stroke();
    c.strokeStyle=col;c.lineWidth=w;c.beginPath();c.moveTo(x0,y0);c.quadraticCurveTo(cx,cy,x1+sway,y1);c.stroke();
    c.strokeStyle='rgba(215,205,250,.34)';c.lineWidth=1.8;
    for(let u=.08;u<.95;u+=.12){const [px,py]=P(u),[qx,qy]=P(u+.02),dx=qx-px,dy=qy-py,L=Math.hypot(dx,dy)||1,nx=-dy/L,ny=dx/L,m=w*.4;
      c.beginPath();c.moveTo(px-nx*m-dx/L*2,py-ny*m-dy/L*2);c.lineTo(px+nx*m+dx/L*2,py+ny*m+dy/L*2);c.stroke()}};
  c.fillStyle='#14112a';c.beginPath();c.ellipse(0,-44,38,20,0,0,7);c.fill();
  lock(-8,-44,-30,-96,-8,-138,16,'#2c2849');
  lock(8,-44,14,-100,28,-136,16,'#34305a');
  lock(-24,-40,-54,-80,-34,-120,16,'#2a2646');
  lock(24,-40,56,-78,40,-114,15,'#312d54');
  lock(0,-46,-8,-92,-22,-106,13,'#3c3868');
  // twine binding the knot
  c.strokeStyle='#8a6a2a';c.lineWidth=5;c.beginPath();c.ellipse(0,-50,30,9,0,0.1,Math.PI-0.1);c.stroke();
  c.fillStyle=SH.gold;c.beginPath();c.roundRect(-34,-26,68,9,4);c.fill();
  // crescent moon
  c.fillStyle='#f4f0e0';c.beginPath();c.arc(-22,-70,12,.5,5.8);c.arc(-17.5,-70,9.8,5.5,.8,true);c.fill();c.fillStyle='rgba(255,240,180,.35)';c.beginPath();c.arc(-22,-70,16,0,7);c.fill();
  c.restore()}

const SHIVA_FACE={skin:SH.skin,skinM:SH.skinM,skinD:SH.skinD,skinH:SH.skinH,gold:SH.gold,ash:SH.ash,red:SH.red,tripundra:true,third:true,brow:'#0b0a14'};
function drawHead(c,hx,hy,o){ // o:{expr:'calm'|'closed'|'rage', k:0..1 anger blend, S:face spec, t}
  const S=o.S||SHIVA_FACE;const e=o.expr||'calm',k=e==='rage'?1:(e==='calm'?(o.k||0):0),closed=e==='closed',L=(a,b)=>a+(b-a)*k;c.save();c.translate(hx,hy);
  // ears + kundala
  [-1,1].forEach(sd=>{c.fillStyle=S.skinM;c.beginPath();c.ellipse(sd*37,2,8,15,sd*-0.12,0,7);c.fill();c.strokeStyle=S.gold;c.lineWidth=3.2;c.beginPath();c.arc(sd*38,22,8,0,7);c.stroke();c.fillStyle=S.gold;c.beginPath();c.arc(sd*38,31,2.6,0,7);c.fill()});
  // head (jaw squares up and widens when angry)
  const g=c.createLinearGradient(-34,0,34,0);g.addColorStop(0,S.skinH);g.addColorStop(.35,S.skin);g.addColorStop(1,S.skinD);c.fillStyle=g;
  const jw=24;c.beginPath();c.moveTo(-34,-14);c.bezierCurveTo(-36,-44,36,-44,34,-14);c.bezierCurveTo(36,16,jw,44,0,50);c.bezierCurveTo(-jw,44,-36,16,-34,-14);c.fill();
  c.fillStyle='rgba(20,20,60,.22)';c.beginPath();c.moveTo(-31,12);c.bezierCurveTo(-24,42,-10,46,0,47);c.bezierCurveTo(10,46,24,42,31,12);c.bezierCurveTo(20,30,8,30,0,30);c.bezierCurveTo(-8,30,-20,30,-31,12);c.fill();
  // tripundra + third eye
  if(S.tripundra!==false){c.strokeStyle=S.ash;c.lineWidth=3.4;c.lineCap='round';[-33,-27,-21].forEach((y,i)=>{c.beginPath();c.moveTo(-23+i*0.6,y+6);c.quadraticCurveTo(0,y+(i?1:-1)+k*(i-1)*2,23-i*0.6,y+6);c.stroke()})}
  if(S.third!==false&&k>0.05){const gl=c.createRadialGradient(0,-22,0,0,-22,32);gl.addColorStop(0,`rgba(255,120,60,${.9*k})`);gl.addColorStop(1,'rgba(255,60,20,0)');c.fillStyle=gl;c.beginPath();c.arc(0,-22,32,0,7);c.fill()}
  if(S.third!==false){c.fillStyle=k>.5?'#ffcf70':S.red;c.beginPath();c.ellipse(0,-22,L(3.2,4),L(6.5,10),0,0,7);c.fill();if(k>.3){c.fillStyle='#ff3a14';c.beginPath();c.ellipse(0,-22,2,L(3,7),0,0,7);c.fill()}}
  // other marks: vaishnava tilak (U), simple dot/bindi, ash lines for sages
  if(S.tilak==='vaishnava'){c.strokeStyle='#f4efe6';c.lineWidth=3;c.lineCap='round';c.beginPath();c.moveTo(-6,-36);c.lineTo(-6,-20);c.moveTo(6,-36);c.lineTo(6,-20);c.moveTo(-6,-20);c.quadraticCurveTo(0,-15,6,-20);c.stroke();c.fillStyle='#d02a2a';c.beginPath();c.ellipse(0,-27,2,5,0,0,7);c.fill()}
  if(S.tilak==='dot'||S.bindi){c.fillStyle='#d02a2a';c.beginPath();c.arc(0,S.bindi?-18:-24,S.bindi?3.4:3,0,7);c.fill()}
  if(S.tilak==='ash'){c.strokeStyle=S.ash||'#e8e4ee';c.lineWidth=3;c.lineCap='round';[-30,-24].forEach((y,i)=>{c.beginPath();c.moveTo(-18,y+5);c.quadraticCurveTo(0,y-1,18,y+5);c.stroke()});c.fillStyle='#d02a2a';c.beginPath();c.arc(0,-18,2.6,0,7);c.fill()}
  // furrow between the brows
  if(k>0.1){c.strokeStyle=`rgba(15,18,60,${.6*k})`;c.lineWidth=2.2;[-3,0,3].forEach(x=>{c.beginPath();c.moveTo(x,-12);c.quadraticCurveTo(x*1.4,-4,x,2);c.stroke()})}
  // brows: heavy, steep, pulled low and together
  c.fillStyle=S.brow||'#0b0a14';[-1,1].forEach(sd=>{const inY=L(-8,1),outY=L(-9,-19),th=L(4.5,8.5);
    const bg=S.browGap!=null?S.browGap:3;c.beginPath();c.moveTo(sd*bg,inY);c.bezierCurveTo(sd*(bg+9),L(-16,inY-6),sd*24,outY-2,sd*33,outY);c.lineTo(sd*33,outY+th*.6);c.bezierCurveTo(sd*22,outY+th+2,sd*(bg+7),inY+th*.8,sd*bg,inY+th);c.closePath();c.fill()});
  // eyes
  [-1,1].forEach(sd=>{const ex=sd*16,ey=L(3,5);
    if(closed){c.strokeStyle='#0b0a14';c.lineWidth=2.6;c.beginPath();c.moveTo(ex-9,ey);c.quadraticCurveTo(ex,ey+5,ex+9,ey);c.stroke();return}
    // sclera
    if(k>.05){const eg=c.createRadialGradient(ex,ey,2,ex,ey,22);eg.addColorStop(0,`rgba(255,60,40,${.45*k})`);eg.addColorStop(1,'rgba(255,60,40,0)');c.fillStyle=eg;c.beginPath();c.arc(ex,ey,22,0,7);c.fill()}
    c.fillStyle=`rgb(${Math.round(244-8*k)},${Math.round(240-125*k)},${Math.round(236-130*k)})`;c.beginPath();c.moveTo(ex-11,ey+1);c.quadraticCurveTo(ex,ey-L(6,8),ex+11,ey+1);c.quadraticCurveTo(ex,ey+L(5,6),ex-11,ey+1);c.fill();
    c.save();c.beginPath();c.moveTo(ex-11,ey+1);c.quadraticCurveTo(ex,ey-L(6,8),ex+11,ey+1);c.quadraticCurveTo(ex,ey+L(5,6),ex-11,ey+1);c.clip();
    // iris (glowing red-orange when angry) + pupil
    const ig=c.createRadialGradient(ex,ey+.5,0,ex,ey+.5,6);ig.addColorStop(0,k>.35?'#ff7a30':'#40304a');ig.addColorStop(.5,k>.35?'#ff1a0e':'#1a1020');ig.addColorStop(1,k>.35?'#a00808':'#0a0810');c.fillStyle=ig;c.beginPath();c.arc(ex,ey+.5,L(4.6,6.2),0,7);c.fill();
    c.fillStyle='#3a0606';c.beginPath();c.ellipse(ex,ey+.5,L(1.8,1.1),L(2.4,3.2),0,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ex-1.6,ey-1.2,1.2,0,7);c.fill();
    if(k>.3){c.strokeStyle=`rgba(210,40,30,${.7*k})`;c.lineWidth=.9;for(let v=0;v<4;v++){c.beginPath();c.moveTo(ex+sd*(10-v*1.2),ey+(v-1.5)*1.6);c.lineTo(ex+sd*(5.5-v*0.6),ey+(v-1.5)*.8);c.stroke()}}
    // heavy upper lid, angled down toward the nose when angry
    c.fillStyle='rgba(12,10,30,.92)';c.beginPath();c.moveTo(ex-13,ey-12);c.lineTo(ex+13,ey-12);c.lineTo(ex+13,ey+L(-1,-4.5)-sd*L(0,2));c.lineTo(ex-13,ey+L(-1,-4.5)+sd*L(0,2));c.closePath();c.fill();
    c.restore();
    c.strokeStyle='rgba(8,6,20,.85)';c.lineWidth=2.2;c.beginPath();c.moveTo(ex-11,ey+1);c.quadraticCurveTo(ex,ey-L(6,8),ex+11,ey+1);c.stroke();
    if(k>.3){c.strokeStyle=`rgba(255,90,50,${.5*k})`;c.lineWidth=1.4;c.beginPath();c.moveTo(ex-9,ey+3.5);c.quadraticCurveTo(ex,ey+L(5,7.5),ex+9,ey+3.5);c.stroke()}});
  // nose: bridge, wings flare when angry, nostrils
  c.strokeStyle='rgba(20,20,70,.5)';c.lineWidth=2;c.beginPath();c.moveTo(-3,6);c.quadraticCurveTo(-6,18,-L(8,10),23);c.moveTo(3,6);c.quadraticCurveTo(6,18,L(8,10),23);c.stroke();
  c.beginPath();c.moveTo(-L(8,11),25);c.quadraticCurveTo(0,L(29,27),L(8,11),25);c.stroke();
  if(k>.2){c.fillStyle=`rgba(10,8,30,${.7*k})`;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*5.5,25,2.6,3.6*k+.5,sd*.6,0,7);c.fill()})}
  // mouth: calm = soft closed line; angry = bared-teeth snarl
  if(k<0.12){c.strokeStyle='#2a1030';c.lineWidth=2.4;c.beginPath();c.moveTo(-10,36);c.quadraticCurveTo(0,40-k*10,10,36);c.stroke()}
  else{const w=10,dn=L(0,4),op=L(.5,2.6);
    // clenched, downturned mouth: corners pulled down, lips pressed hard
    c.fillStyle='#240a12';c.beginPath();c.moveTo(-w,36+dn);c.quadraticCurveTo(0,35-dn*.6,w,36+dn);c.quadraticCurveTo(0,35-dn*.6+op+1.5,-w,36+dn);c.fill();
    if(k>.45){c.save();c.beginPath();c.moveTo(-w+2,36+dn-.5);c.quadraticCurveTo(0,35-dn*.6,w-2,36+dn-.5);c.quadraticCurveTo(0,35-dn*.6+op+1,-w+2,36+dn-.5);c.clip();
      c.fillStyle='#ece4d8';c.fillRect(-w,34-dn*.6,2*w,op+3);c.strokeStyle='rgba(60,30,30,.55)';c.lineWidth=.9;for(let q=-3;q<=3;q++){c.beginPath();c.moveTo(q*w/3.4,33);c.lineTo(q*w/3.4,42);c.stroke()}c.restore()}
    c.strokeStyle='#14040a';c.lineWidth=2.6;c.lineCap='round';c.beginPath();c.moveTo(-w-1,36+dn+1);c.quadraticCurveTo(0,34.5-dn*.6,w+1,36+dn+1);c.stroke();
  }
  if(S.beard){c.fillStyle=S.beard;const bl=S.beardLen||34;c.beginPath();c.moveTo(-31,6);c.bezierCurveTo(-34,28,-24,46,-10,50);c.bezierCurveTo(-6,50+bl,6,50+bl,10,50);c.bezierCurveTo(24,46,34,28,31,6);c.bezierCurveTo(26,20,20,24,12,26);c.bezierCurveTo(6,24,-6,24,-12,26);c.bezierCurveTo(-20,24,-26,20,-31,6);c.closePath();c.fill();
    c.fillStyle='rgba(255,255,255,.16)';c.beginPath();c.ellipse(-10,40,5,14,.2,0,7);c.fill();c.fillStyle=S.mustache||S.beard;c.beginPath();c.moveTo(-14,29);c.quadraticCurveTo(0,24,14,29);c.quadraticCurveTo(0,33,-14,29);c.fill();
    // mouth drawn again on top of the beard so the expression still reads
    if(k<0.12){c.strokeStyle=S.mouthCol||'#4a2030';c.lineWidth=2.4;c.beginPath();c.moveTo(-8,36);c.quadraticCurveTo(0,39,8,36);c.stroke()}else{c.strokeStyle='#14040a';c.lineWidth=2.8;c.lineCap='round';c.beginPath();c.moveTo(-9,38.5);c.quadraticCurveTo(0,34.5,9,38.5);c.stroke()}}
  if(S.female){c.strokeStyle='#14101a';c.lineWidth=2;[-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*16+sd*10,3);c.lineTo(sd*16+sd*14,-1);c.moveTo(sd*16+sd*9,5);c.lineTo(sd*16+sd*13,4);c.stroke()});if(k<0.12){c.fillStyle='#c4384a';c.beginPath();c.moveTo(-8,36);c.quadraticCurveTo(0,32,8,36);c.quadraticCurveTo(0,43,-8,36);c.fill()}}
  c.restore()}

function drawTrishul(c,x,top,bot,t,rage){ // trident with damaru + ribbons
  c.save();c.translate(x,0);const sw=Math.sin(t*3)*3;
  c.strokeStyle='#5a4028';c.lineWidth=7;c.lineCap='round';c.beginPath();c.moveTo(0,bot);c.lineTo(0,top);c.stroke();
  c.strokeStyle='rgba(255,220,160,.35)';c.lineWidth=2;c.beginPath();c.moveTo(-2,bot);c.lineTo(-2,top);c.stroke();
  const m=c.createLinearGradient(-30,0,30,0);m.addColorStop(0,'#fff6d0');m.addColorStop(.5,SH.gold);m.addColorStop(1,SH.goldD);c.fillStyle=m;c.strokeStyle=m;c.lineWidth=6;
  c.beginPath();c.moveTo(-30,top-48);c.lineTo(-30,top-8);c.quadraticCurveTo(0,top+22,30,top-8);c.lineTo(30,top-48);c.stroke();
  [[-30,top-48],[0,top-62],[30,top-48]].forEach(([dx,dy],i)=>{c.beginPath();c.moveTo(dx-8,dy);c.lineTo(dx,dy-(i===1?46:40));c.lineTo(dx+8,dy);c.closePath();c.fill()});
  c.lineWidth=6;c.beginPath();c.moveTo(0,top+14);c.lineTo(0,top-64);c.stroke();
  c.fillStyle=SH.goldD;c.beginPath();c.ellipse(0,top+34,9,6,0,0,7);c.fill();
  c.strokeStyle='#8a1f1a';c.lineWidth=2.4;c.beginPath();c.moveTo(0,top+58);c.lineTo(0,top+72);c.stroke();c.save();c.translate(0,top+72);c.rotate(sw*0.05);c.scale(.8,.8);c.translate(0,26);drawDamaru(c,sw);c.restore();
  // ribbon
  c.fillStyle='#c83a3a';c.beginPath();c.moveTo(2,top+44);c.quadraticCurveTo(36+sw*3,top+54,50+sw*4,top+90);c.quadraticCurveTo(26+sw*2,top+70,2,top+62);c.fill();
  c.restore()}

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
  const HS=1.18;c.save();c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);c.save();c.translate(P.hd[0],P.hd[1]-30);c.scale(.74,.7);c.translate(-P.hd[0],-P.hd[1]+30);if(!PHok())drawJata(c,P.hd[0],P.hd[1]-34,t,rage,o.imp||0);c.restore();c.restore();
  // legs
  const stance=(h,k,f,side)=>{const r=elbow(h,f,86,92,side);tapered(c,h,r.e,31,23,SH.skin);tapered(c,r.e,f,23,14,SH.skin);c.fillStyle='rgba(255,255,255,.10)';c.beginPath();c.ellipse(lerp(r.e[0],f[0],.35)-side*2,lerp(r.e[1],f[1],.35),9,26,Math.atan2(f[1]-r.e[1],f[0]-r.e[0])+1.57,0,7);c.fill();
    c.globalAlpha=.4;c.fillStyle=SH.skinD;tapered(c,[h[0]+side*10,h[1]],[r.e[0]+side*8,r.e[1]],9,8,SH.skinD);tapered(c,[r.e[0]+side*7,r.e[1]],[f[0]+side*6,f[1]-6],8,6,SH.skinD);c.globalAlpha=1;
    c.fillStyle=SH.skinM;c.beginPath();c.ellipse(f[0]+side*4,f[1]-3,19,8,0,0,7);c.fill();c.fillStyle=SH.skinD;c.globalAlpha=.4;c.beginPath();c.ellipse(f[0]+side*6,f[1]-1,13,4,0,0,7);c.fill();c.globalAlpha=1};
  stance(P.hipL,P.kL,P.fL,-1);stance(P.hipR,P.kR,P.fR,1);
  // trident behind right hand
  const T=P.tri;c.save();if(T.rot){c.translate(T.x,-300);c.rotate(T.rot);c.translate(-T.x,300)}drawTrishul(c,T.x,T.top,T.bot,t,rage);c.restore();
  // torso
  const tg=c.createLinearGradient(-60,0,60,0);tg.addColorStop(0,SH.skinH);tg.addColorStop(.3,SH.skin);tg.addColorStop(1,SH.skinD);c.fillStyle=tg;
  c.beginPath();c.moveTo(P.sL[0]-6,P.sL[1]+4);c.bezierCurveTo(-52,P.sL[1]+34,-46,P.ch[1]+64,-36,P.ph[1]-6);c.lineTo(36,P.ph[1]-6);c.bezierCurveTo(46,P.ch[1]+64,52,P.sR[1]+34,P.sR[0]+6,P.sR[1]+4);c.bezierCurveTo(30,P.nk[1]+4,-30,P.nk[1]+4,P.sL[0]-6,P.sL[1]+4);c.fill();
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
  c.save();c.translate(P.hd[0],P.hd[1]+40);c.scale(HS,HS);c.translate(-P.hd[0],-P.hd[1]-40);{const ex=o.expr||(o.k!==undefined?'calm':(rage?'rage':'calm'));if(!PH(c,P.hd[0],P.hd[1],ex,o.k))drawHead(c,P.hd[0],P.hd[1],{expr:ex,k:o.k,t})}c.restore();
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
