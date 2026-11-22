/* Trimurti showcase - NEW look ("paper-cut painterly"): bold layered flat shapes, ink outlines,
   paper drop-shadows, gold / indigo / saffron palette, ornate jewellery, flaming halos.
   Standalone: does NOT use engine/. Every character is a jointed, parametric rig (pure function of t + params),
   so the same code renders stills or animation.  Logical canvas 1280x720 (draw() is given a ctx pre-scaled). */
(function(G){
'use strict';
const TAU=Math.PI*2,PI=Math.PI;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),lerp=(a,b,u)=>a+(b-a)*u,ease=u=>{u=clamp(u);return u*u*(3-2*u)};
const L2=(a,b,u)=>[lerp(a[0],b[0],u),lerp(a[1],b[1],u)];
function rng(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const hexRgb=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
const toHex=a=>'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
const shade=(h,f)=>toHex(hexRgb(h).map(v=>f<1?v*f:v+(255-v)*(f-1)));
let DPR=1.5;
const INK='#1e0d24';
const PAL={gold:'#f2c14e',goldL:'#fff0b0',goldD:'#b0701a',saff:'#ee7b22',red:'#c42b3a',ruby:'#e0234a',emer:'#18a57a',sapph:'#3b7cf0',pearl:'#fff7e8'};

/* ---------- drawing kit ---------- */
function lg(c,x0,y0,x1,y1,st){const g=c.createLinearGradient(x0,y0,x1,y1);st.forEach((s,i)=>Array.isArray(s)?g.addColorStop(s[0],s[1]):g.addColorStop(i/(st.length-1),s));return g}
function rg(c,x,y,r0,r1,st){const g=c.createRadialGradient(x,y,r0,x,y,r1);st.forEach((s,i)=>Array.isArray(s)?g.addColorStop(s[0],s[1]):g.addColorStop(i/(st.length-1),s));return g}
// one paper-cut layer: soft drop shadow, flat/gradient fill, ink outline
function cut(c,path,fill,o){o=o||{};c.save();c.beginPath();path(c);
  if(o.sh!==0&&fill){c.shadowColor=o.shc||'rgba(14,4,26,.42)';c.shadowBlur=(o.blur==null?5:o.blur)*DPR;c.shadowOffsetX=(o.sx==null?2:o.sx)*DPR;c.shadowOffsetY=(o.sy==null?4:o.sy)*DPR}
  if(fill){c.fillStyle=fill;c.fill()}c.shadowColor='rgba(0,0,0,0)';c.shadowBlur=0;c.shadowOffsetX=0;c.shadowOffsetY=0;
  if(o.lw!==0){c.lineWidth=o.lw||2.4;c.strokeStyle=o.ink||INK;c.lineJoin='round';c.lineCap='round';c.stroke()}c.restore()}
const P={
  ell:(x,y,rx,ry,r)=>c=>c.ellipse(x,y,rx,ry,r||0,0,TAU),
  poly:(pts)=>c=>{c.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)c.lineTo(pts[i][0],pts[i][1]);c.closePath()},
  smooth:(pts)=>c=>{const n=pts.length,m=i=>[(pts[i%n][0]+pts[(i+1)%n][0])/2,(pts[i%n][1]+pts[(i+1)%n][1])/2];const s=m(n-1);c.moveTo(s[0],s[1]);for(let i=0;i<n;i++){const q=m(i);c.quadraticCurveTo(pts[i][0],pts[i][1],q[0],q[1])}c.closePath()},
  caps:(a,b,ra,rb)=>c=>{const an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.arc(a[0],a[1],ra,an+PI/2,an+PI*1.5);c.arc(b[0],b[1],rb,an-PI/2,an+PI/2);c.closePath()}
};
function glow(c,x,y,r,rgb,a){if(a<=0||r<=0)return;c.save();c.globalCompositeOperation='lighter';const g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(.45,`rgba(${rgb},${a*.35})`);g.addColorStop(1,`rgba(${rgb},0)`);c.fillStyle=g;c.beginPath();c.arc(x,y,r,0,TAU);c.fill();c.restore()}
function stroke(c,fn,col,w,o){o=o||{};c.save();c.beginPath();fn(c);c.strokeStyle=col;c.lineWidth=w;c.lineCap=o.cap||'round';c.lineJoin='round';if(o.dash)c.setLineDash(o.dash);if(o.off!=null)c.lineDashOffset=o.off;if(o.a!=null)c.globalAlpha*=o.a;c.stroke();c.restore()}
function ik(s,tg,l1,l2,bend){let dx=tg[0]-s[0],dy=tg[1]-s[1],d=Math.hypot(dx,dy);d=clamp(d,Math.abs(l1-l2)+.5,l1+l2-.5);const a=Math.atan2(dy,dx),A=Math.acos(clamp((l1*l1+d*d-l2*l2)/(2*l1*d),-1,1)),ea=a+bend*A;
  return{s:s,e:[s[0]+Math.cos(ea)*l1,s[1]+Math.sin(ea)*l1],t:[s[0]+Math.cos(a)*d,s[1]+Math.sin(a)*d]}}
const goldG=(c,x0,x1)=>lg(c,x0,0,x1,0,[PAL.goldL,PAL.gold,PAL.goldD]);
function gem(c,x,y,r,col){cut(c,P.ell(x,y,r,r*1.15),col,{sh:0,lw:1.2});c.fillStyle='rgba(255,255,255,.7)';c.beginPath();c.arc(x-r*.35,y-r*.4,r*.32,0,TAU);c.fill()}
function beadArc(c,x0,y0,x1,y1,drop,n,r,col,hi){for(let i=0;i<n;i++){const u=i/(n-1),x=lerp(x0,x1,u),y=lerp(y0,y1,u)+Math.sin(u*PI)*drop;cut(c,P.ell(x,y,r,r),col,{sh:0,lw:1});if(hi){c.fillStyle=hi;c.beginPath();c.arc(x-r*.3,y-r*.35,r*.35,0,TAU);c.fill()}}}
function band(c,a,b,u,w,col){const x=lerp(a[0],b[0],u),y=lerp(a[1],b[1],u),an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.save();c.translate(x,y);c.rotate(an);cut(c,cc=>cc.roundRect(-4.5,-w-2,9,2*w+4,3),goldG(c,-5,5),{sh:0,lw:1.4});gem(c,0,0,2.6,PAL.ruby);c.restore()}

/* ---------- faces ---------- */
// F: {skin:{b,h,d,m}, turn -1..1, blink 0..1, mouth 0..1, smile, lx, ly, brow, tilak, third, beard, lip, t}
function face(c,F){const sk=F.skin,tn=clamp(F.turn||0,-1,1),sq=1-Math.abs(tn)*.3,fx=tn*12,bl=clamp(F.blink||0),an=clamp(F.anger||0),sd_=clamp(F.sad||0),su=clamp(F.surp||0),mo=clamp(Math.max(F.mouth||0,su*.75)),sm=(F.smile==null?.35:F.smile)*(1-clamp(an+sd_+su))-an*1.15-sd_*.95,lx=(F.lx||0)+tn*.5,ly=F.ly||0,t=F.t||0;
  c.save();c.scale(sq,1);
  [-1,1].forEach(sd=>{if(tn*sd<-.6)return;const ex=sd*33;cut(c,P.ell(ex,4,7.5,13,sd*-.15),sk.m,{sh:0,lw:2});
    if(F.kundala!==false){c.save();c.translate(ex+sd,17);c.rotate(Math.sin(t*1.7+sd)*.14);cut(c,cc=>{cc.moveTo(0,-2);cc.bezierCurveTo(10,6,9,20,0,27);cc.bezierCurveTo(-9,20,-10,6,0,-2)},goldG(c,-9,9),{lw:1.6,sh:0});gem(c,0,13,3.2,F.kgem||PAL.ruby);c.restore()}});
  const hp=[[-34,-8],[-31,-34],[-16,-46],[0,-48],[16,-46],[31,-34],[34,-8],[31,16],[19,36],[0,47],[-19,36],[-31,16]];
  cut(c,P.smooth(hp),lg(c,-34,0,34,0,[sk.h,sk.b,sk.d]),{lw:2.6});
  c.save();c.beginPath();P.smooth(hp)(c);c.clip();c.fillStyle='rgba(30,10,60,.1)';c.beginPath();c.ellipse(31+fx*.6,8,12,48,0,0,TAU);c.fill();
  c.fillStyle='rgba(255,105,110,.17)';[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*19+fx,20,8,5,0,0,TAU);c.fill()});c.restore();
  c.save();c.translate(fx,0);
  // brows
  [-1,1].forEach(sd=>{const ex=sd*15,r=(F.brow||0)*4+su*6+sd_*1.5,ia=an*7.5-sd_*7,oa=-an*3.5+sd_*3,m=(ia+oa)*.4-an*2,th=4+an*2.6;c.fillStyle=F.browCol||INK;c.beginPath();c.moveTo(ex-sd*10,-15-r*.6+ia);c.quadraticCurveTo(ex+sd*3,-24.5-r+m,ex+sd*17,-14.5-r*.3+oa);c.quadraticCurveTo(ex+sd*3,-24.5-r+m+th,ex-sd*10,-15-r*.6+ia+an*2);c.fill()});
  // lotus-petal eyes with kajal wings; the lid slides down for blinks / meditation
  [-1,1].forEach(sd=>{const ex=sd*15,inn=[ex-sd*10,1],out=[ex+sd*13,-3],cy=lerp(-11.5,6,bl);
    const eye=cc=>{cc.moveTo(inn[0],inn[1]);cc.quadraticCurveTo(ex,-12,out[0],out[1]);cc.quadraticCurveTo(ex+sd,7.5,inn[0],inn[1]);cc.closePath()};
    if(bl<.96){c.save();c.beginPath();eye(c);c.clip();c.fillStyle='#fbf5e8';c.fill();
      const ix=ex+lx*4.2,iy=.5+ly*2;c.fillStyle=rg(c,ix,iy,0,6.6,(an>.35||F.eyeRed)?[[0,'#ff7a40'],[.55,'#c81e14'],[.85,'#6a0808'],[1,'#240404']]:[[0,'#3a1c0a'],[.6,'#5a3214'],[.82,'#22100a'],[1,'#0c0604']]);c.beginPath();c.arc(ix,iy,6.3,0,TAU);c.fill();
      c.fillStyle='#050203';c.beginPath();c.arc(ix,iy,2.8,0,TAU);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ix-2,iy-2.3,1.6,0,TAU);c.fill();
      if(an>.02||sd_>.02){const yi=-9+an*9.5,yo=-9+an*1.5+sd_*7.5;c.fillStyle=sk.m;c.beginPath();c.moveTo(inn[0]-sd*5,-18);c.lineTo(out[0]+sd*5,-18);c.lineTo(out[0]+sd*5,yo);c.lineTo(inn[0]-sd*5,yi);c.closePath();c.fill();stroke(c,cc=>{cc.moveTo(inn[0]-sd*5,yi);cc.lineTo(out[0]+sd*5,yo)},INK,2.4)}
      c.fillStyle=sk.m;c.beginPath();c.moveTo(inn[0]-sd*4,-17);c.lineTo(out[0]+sd*4,-17);c.lineTo(out[0]+sd*3,out[1]);c.quadraticCurveTo(ex,cy,inn[0],inn[1]);c.closePath();c.fill();c.restore()}
    if(an>.35||F.eyeRed)glow(c,ex+sd*2,-3,15,'255,60,40',.38*Math.max(an,F.eyeRed?.8:0));
    if(sd_>.5){const tx=ex+sd*7,ty=9+sd_*8;cut(c,cc=>{cc.moveTo(tx,ty-6);cc.quadraticCurveTo(tx+4,ty+1,tx,ty+4);cc.quadraticCurveTo(tx-4,ty+1,tx,ty-6)},'rgba(190,225,255,.85)',{sh:0,lw:.9,ink:'rgba(60,90,140,.7)'})}
    stroke(c,cc=>{cc.moveTo(inn[0],inn[1]);cc.quadraticCurveTo(ex,cy,out[0],out[1])},INK,3.1);
    c.fillStyle=INK;c.beginPath();c.moveTo(out[0]-sd*2.5,out[1]-1.6);c.lineTo(out[0]+sd*8,out[1]-5.5);c.lineTo(out[0],out[1]+1.6);c.closePath();c.fill();
    if(bl<.9)stroke(c,cc=>{cc.moveTo(inn[0]+sd*2,inn[1]+1.5);cc.quadraticCurveTo(ex+sd,6.5,out[0]-sd,out[1]+1)},'rgba(30,13,36,.55)',1.3);
    stroke(c,cc=>{cc.moveTo(inn[0]+sd,inn[1]-4.5);cc.quadraticCurveTo(ex,lerp(-14,-4,bl),out[0]-sd,out[1]-4.5)},'rgba(30,13,36,.33)',1.2)});
  // nose
  stroke(c,cc=>{cc.moveTo(-2,-5);cc.quadraticCurveTo(-5,10,-6.5,17);cc.quadraticCurveTo(0,22.5,6.5,17)},'rgba(40,14,30,.55)',1.8);
  c.fillStyle='rgba(40,10,40,.22)';c.beginPath();c.ellipse(1,19.5,6,2.4,0,0,TAU);c.fill();
  // beard (behind the lips)
  if(F.beard){const bc=F.beard,bw=Math.sin(t*1.3)*1.5;cut(c,cc=>{cc.moveTo(-31,8);cc.bezierCurveTo(-35,40,-24,62,-12,76);cc.quadraticCurveTo(-5+bw,86,0+bw,93);cc.quadraticCurveTo(5+bw,86,12,76);cc.bezierCurveTo(24,62,35,40,31,8);cc.bezierCurveTo(26,28,18,40,10,41);cc.quadraticCurveTo(0,45,-10,41);cc.bezierCurveTo(-18,40,-26,28,-31,8);cc.closePath()},lg(c,0,10,0,92,[bc,shade(bc,.8)]),{lw:2,sh:0});
    [-18,-9,0,9,18].forEach((x,i)=>stroke(c,cc=>{cc.moveTo(x*1.1,46);cc.quadraticCurveTo(x*.9,64,x*.4+bw,84-Math.abs(x)*.6)},'rgba(120,110,130,.45)',1.3))}
  // lips (talking mouth opens)
  const my=30,cw=10,cu=sm*3,lo=mo*7;
  if(mo>.04){c.fillStyle='#3a0a16';c.beginPath();c.ellipse(0,my+1.5+lo*.45,cw*.78,1.2+lo*.6,0,0,TAU);c.fill();c.fillStyle='#f6eee2';c.fillRect(-5,my-.4,10,1.3+mo)}
  c.fillStyle=F.lip||'#b8324a';c.beginPath();c.moveTo(-cw,my-cu);c.quadraticCurveTo(-5,my-4.6,0,my-2.6);c.quadraticCurveTo(5,my-4.6,cw,my-cu);c.quadraticCurveTo(0,my+.4,-cw,my-cu);c.fill();
  c.beginPath();c.moveTo(-cw*.8,my-cu*.5+lo*.4);c.quadraticCurveTo(0,my+6.5+lo,cw*.8,my-cu*.5+lo*.4);c.quadraticCurveTo(0,my+1.6+lo,-cw*.8,my-cu*.5+lo*.4);c.fill();
  stroke(c,cc=>{cc.moveTo(-cw,my-cu);cc.quadraticCurveTo(0,my+1+lo*.6+sm*1.6,cw,my-cu)},INK,1.5);
  c.fillStyle='rgba(255,255,255,.35)';c.beginPath();c.ellipse(2,my+3.4+lo,3,1,0,0,TAU);c.fill();
  if(F.beard){const bc=F.beard;[-1,1].forEach(sd=>{const m=cc=>{cc.moveTo(sd*1,25.5);cc.quadraticCurveTo(sd*12,23.5,sd*17,29.5);cc.quadraticCurveTo(sd*21,33,sd*25,27)};stroke(c,m,INK,6.2);stroke(c,m,bc,4)})}
  // marks
  if(F.bindi){c.fillStyle=PAL.ruby;c.beginPath();c.arc(0,-21,2.6,0,TAU);c.fill()}
  if(F.tilak==='vaishnava'){stroke(c,cc=>{cc.moveTo(-6,-40);cc.lineTo(-5,-21);cc.quadraticCurveTo(0,-15,5,-21);cc.lineTo(6,-40)},'#fff8ee',2.6);stroke(c,cc=>{cc.moveTo(0,-38);cc.lineTo(0,-21)},PAL.ruby,2.8)}
  if(F.tilak==='tripundra'){[-37,-32,-27].forEach(y=>stroke(c,cc=>{cc.moveTo(-23,y+2);cc.quadraticCurveTo(0,y-2.5,23,y+2)},'#f6f4ee',2.5))}
  if(F.tilak==='brahma'){c.fillStyle=PAL.ruby;c.beginPath();c.ellipse(0,-24,2.4,5.5,0,0,TAU);c.fill();c.fillStyle=PAL.gold;c.beginPath();c.arc(0,-33,2.2,0,TAU);c.fill()}
  if(F.third!=null){const o3=clamp(F.third);if(o3>.02){glow(c,0,-22,10+40*o3,'255,110,30',.5*o3);glow(c,0,-22,6+8*o3,'255,220,150',.45*o3)}
    c.save();c.translate(0,-22);const h3=lerp(.6,6,o3);cut(c,cc=>{cc.moveTo(0,-7.5);cc.quadraticCurveTo(h3,0,0,7.5);cc.quadraticCurveTo(-h3,0,0,-7.5)},o3>.12?'#ffe3a0':PAL.ruby,{sh:0,lw:1.4});
    if(o3>.12){c.fillStyle='#e0300e';c.beginPath();c.ellipse(0,0,h3*.38,3.6,0,0,TAU);c.fill()}c.restore()}
  c.restore();c.restore()}
function hairCap(c,col,o){o=o||{};cut(c,cc=>{cc.moveTo(-35,-6);cc.bezierCurveTo(-40,-44,-16,-54,0,-53);cc.bezierCurveTo(16,-54,40,-44,35,-6);cc.bezierCurveTo(30,-24,18,-34,0,-33);cc.bezierCurveTo(-18,-34,-30,-24,-35,-6);cc.closePath()},col,{lw:2,sh:0});
  stroke(c,cc=>{cc.moveTo(-12,-50);cc.quadraticCurveTo(-20,-40,-28,-22)},'rgba(255,255,255,.18)',2)}
// long curls falling behind the head (Vishnu)
function hairBack(c,col,t,len){const sw=Math.sin(t*1.2)*3;
  cut(c,P.smooth([[-30,-44],[-46,-14],[-52,len*.4],[-48+sw,len*.8],[-30+sw,len],[-14,len*.86],[0,len*.95],[14,len*.86],[30+sw,len],[48+sw,len*.8],[52,len*.4],[46,-14],[30,-44],[0,-52]]),lg(c,-50,0,50,0,['#2a2650',col,'#06050e']),{lw:2.2,sh:0});
  for(let i=-2;i<=2;i++)stroke(c,cc=>{cc.moveTo(i*14,0);cc.bezierCurveTo(i*22,len*.3,i*20+sw,len*.6,i*16+sw,len*.9)},'rgba(160,150,230,.28)',2.2)}

function kirita(c,h){h=h||100;
  [-1,1].forEach(sd=>cut(c,cc=>{cc.moveTo(sd*30,-30);cc.bezierCurveTo(sd*56,-36,sd*62,-62,sd*50,-84);cc.bezierCurveTo(sd*46,-62,sd*38,-52,sd*26,-48);cc.closePath()},lg(c,0,-84,0,-30,[PAL.goldL,PAL.gold,PAL.goldD]),{lw:1.8}));
  const top=-42-h;cut(c,cc=>{cc.moveTo(-33,-40);cc.lineTo(-26,-42-h*.5);cc.lineTo(-17,-42-h*.82);cc.quadraticCurveTo(-6,-42-h*.95,0,top);cc.quadraticCurveTo(6,-42-h*.95,17,-42-h*.82);cc.lineTo(26,-42-h*.5);cc.lineTo(33,-40);cc.closePath()},goldG(c,-32,32),{lw:2.2});
  [.28,.55,.8].forEach((f,i)=>{const y=-42-h*f,w=lerp(32,14,f);stroke(c,cc=>{cc.moveTo(-w,y+3);cc.quadraticCurveTo(0,y-4,w,y+3)},PAL.goldD,3);for(let k=-2;k<=2;k++)if(Math.abs(k)*7<w)gem(c,k*w/2.6,y-1+Math.abs(k)*.8,2,i%2?PAL.emer:PAL.ruby)});
  cut(c,cc=>{cc.moveTo(0,-42-h*.5);cc.quadraticCurveTo(11,-42-h*.32,0,-48);cc.quadraticCurveTo(-11,-42-h*.32,0,-42-h*.5)},PAL.ruby,{lw:1.4,sh:0});
  cut(c,cc=>{cc.moveTo(-36,-24);cc.quadraticCurveTo(0,-37,36,-24);cc.lineTo(34,-42);cc.quadraticCurveTo(0,-54,-34,-42);cc.closePath()},goldG(c,-36,36),{lw:2});
  for(let k=-3;k<=3;k++)gem(c,k*9.5,-33-Math.cos(k*.4)*3.6,2.6,k%2?PAL.emer:PAL.ruby);
  cut(c,P.ell(0,top-6,6,8),goldG(c,-6,6),{lw:1.6,sh:0});gem(c,0,top-7,2.6,PAL.sapph);
  beadArc(c,-30,-24,30,-24,8,11,1.8,PAL.pearl)}
function jataMukuta(c){ // Brahma: tiered gold crown with lotus band
  cut(c,cc=>{cc.moveTo(-30,-38);cc.bezierCurveTo(-34,-74,-22,-104,0,-112);cc.bezierCurveTo(22,-104,34,-74,30,-38);cc.closePath()},goldG(c,-30,30),{lw:2.2});
  [-60,-78,-94].forEach((y,i)=>stroke(c,cc=>{const w=30-i*7;cc.moveTo(-w,y+4);cc.quadraticCurveTo(0,y-3,w,y+4)},PAL.goldD,2.6));
  [-1,0,1].forEach(k=>gem(c,k*12,-68+Math.abs(k)*2,2.6,k?PAL.emer:PAL.ruby));gem(c,0,-86,3,PAL.sapph);
  for(let i=-3;i<=3;i++){c.save();c.translate(i*9.5,-37);cut(c,cc=>{cc.moveTo(-5,0);cc.quadraticCurveTo(-5,-12,0,-16);cc.quadraticCurveTo(5,-12,5,0);cc.closePath()},lg(c,0,-16,0,0,['#fff4f8','#f392b6']),{lw:1.2,sh:0});c.restore()}
  cut(c,cc=>{cc.moveTo(-34,-24);cc.quadraticCurveTo(0,-34,34,-24);cc.lineTo(32,-38);cc.quadraticCurveTo(0,-47,-32,-38);cc.closePath()},goldG(c,-34,34),{lw:2});
  for(let k=-3;k<=3;k++)gem(c,k*9,-31-Math.cos(k*.4)*3,2.3,k%2?PAL.ruby:PAL.pearl);
  cut(c,P.ell(0,-117,5,7),goldG(c,-5,5),{lw:1.4,sh:0})}

/* ---------- halo (prabhavali) ---------- */
function halo(c,x,y,r,t,o){o=o||{};const C=o.col||['#fff3c0','#f6c040','#e8661c','#7a1030'],g=o.g==null?1:o.g;c.save();c.translate(x,y);
  glow(c,0,0,r*2.1,o.rgb||'255,190,80',.32*g);glow(c,0,0,r*1.2,o.rgb2||'255,235,170',.22*g);
  const n=o.n||30;c.save();c.rotate(t*.06);for(let i=0;i<n;i++){const f=1+.09*Math.sin(t*3.1+i*1.9);c.save();c.rotate(i/n*TAU);
    cut(c,cc=>{cc.moveTo(-r*.1,-r*.95);cc.bezierCurveTo(-r*.12,-r*1.08,-r*.03,-r*1.14*f,r*.03,-r*1.3*f);cc.bezierCurveTo(r*.02,-r*1.16*f,r*.12,-r*1.08,r*.1,-r*.95);cc.closePath()},lg(c,0,-r*.95,0,-r*1.3,[C[1],C[2]]),{sh:0,lw:1.3});c.restore()}c.restore();
  cut(c,P.ell(0,0,r,r),rg(c,0,0,r*.1,r,[[0,C[0]],[.55,C[1]],[.85,C[2]],[1,C[3]]]),{lw:2.6,sh:0});
  c.save();c.rotate(-t*.1);for(let i=0;i<16;i++){c.save();c.rotate(i/16*TAU);cut(c,cc=>{cc.moveTo(0,-r*.5);cc.quadraticCurveTo(r*.12,-r*.66,0,-r*.84);cc.quadraticCurveTo(-r*.12,-r*.66,0,-r*.5)},o.petal||'rgba(255,248,220,.5)',{sh:0,lw:1,ink:'rgba(120,40,10,.5)'});c.restore()}c.restore();
  stroke(c,cc=>cc.arc(0,0,r*.92,0,TAU),'rgba(255,250,225,.9)',2.4,{dash:[1,7]});stroke(c,cc=>cc.arc(0,0,r*.46,0,TAU),'rgba(130,40,10,.45)',1.6);
  c.restore()}

/* ---------- hands, arms ---------- */
// wrist at origin, fingers toward local -y; type: abhaya | hold | rest | jnana | varada
function hand(c,sk,p,ang,type,fl){c.save();c.translate(p[0],p[1]);c.rotate(ang);c.scale(fl||1,1);const f=sk.b,o={sh:0,lw:1.5};
  if(type==='abhaya'||type==='varada'){[[-7.5,-14,3.4,-29],[-2.5,-16,3.6,-33],[2.5,-16,3.6,-32],[7.3,-14,3.2,-27]].forEach(([x,y,r,ty])=>cut(c,P.caps([x,y],[x*1.1,ty],r,r*.85),f,o));
    cut(c,P.caps([-10,-3],[-17,-14],3.8,3.2),f,o);cut(c,P.smooth([[-11,-17],[11,-17],[11.5,0],[7,8],[-7,8],[-11.5,0]]),lg(c,-11,0,11,0,[sk.h,sk.b]),o);
    c.fillStyle='#e0234a';c.beginPath();c.arc(0,-7,3.6,0,TAU);c.fill();c.strokeStyle='rgba(224,35,74,.7)';c.lineWidth=1;c.beginPath();c.arc(0,-7,6,0,TAU);c.stroke()}
  else if(type==='jnana'){cut(c,P.smooth([[-10,-2],[10,-2],[12,-14],[6,-22],[-6,-22],[-12,-14]]),lg(c,-11,0,11,0,[sk.h,sk.b]),o);
    [[3,-22,-2,-31],[8,-19,9,-31],[11,-14,14,-25]].forEach(([x,y,x2,y2])=>cut(c,P.caps([x,y],[x2,y2],3.2,2.8),f,o));
    stroke(c,cc=>cc.arc(-6,-25,4.5,0,TAU),INK,1.5);cut(c,P.caps([-10,-12],[-8,-24],3.6,3),f,o);cut(c,P.caps([-3,-20],[-4,-28],3.4,3),f,o)}
  else if(type==='rest'){cut(c,P.smooth([[-10,0],[10,0],[11,-14],[7,-20],[-7,-20],[-11,-14]]),lg(c,-11,0,11,0,[sk.h,sk.b]),o);
    [[-6,-19,-7,-30],[-2,-20,-2,-33],[2.5,-20,3,-32],[6.5,-18,7.5,-28]].forEach(([x,y,x2,y2])=>cut(c,P.caps([x,y],[x2,y2],3.2,2.8),f,o));cut(c,P.caps([-10,-6],[-16,-15],3.6,3),f,o)}
  else{ // fist gripping something
    cut(c,P.smooth([[-11,0],[11,0],[13,-14],[9,-24],[-9,-24],[-13,-14]]),lg(c,-12,0,12,0,[sk.h,sk.b,sk.d]),o);
    [-7.5,-2.5,2.5,7.5].forEach(x=>cut(c,P.ell(x,-24,3.4,4),f,{sh:0,lw:1.2}));cut(c,P.caps([-12,-8],[-3,-19],3.8,3.4),f,o)}
  c.restore()}
function limb(c,sk,a,b,ra,rb,o){o=o||{};const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d,mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;
  cut(c,P.caps(a,b,ra,rb),lg(c,mx+nx*ra,my+ny*ra,mx-nx*ra,my-ny*ra,ny<0?[sk.h,sk.b,sk.d]:[sk.d,sk.b,sk.h]),{lw:o.lw==null?2.2:o.lw,sh:o.sh})}
function limbOutline(c,a,b,ra,rb,open){c.save();c.beginPath();if(open){const an=Math.atan2(b[1]-a[1],b[0]-a[0]);c.moveTo(a[0]+Math.cos(an-PI/2)*ra*.9,a[1]+Math.sin(an-PI/2)*ra*.9);c.arc(b[0],b[1],rb,an-PI/2,an+PI/2);c.lineTo(a[0]+Math.cos(an+PI/2)*ra*.9,a[1]+Math.sin(an+PI/2)*ra*.9)}else P.caps(a,b,ra,rb)(c);c.lineWidth=4.6;c.strokeStyle=INK;c.lineJoin='round';c.stroke();c.restore()}
function arm(c,sk,s,tg,o){o=o||{};const r=ik(s,tg,o.l1||68,o.l2||64,o.bend||1),w=o.w||[15,12,9.5];
  limbOutline(c,s,r.e,w[0],w[1]*1.05,o.cap);limbOutline(c,r.e,r.t,w[1],w[2]);limb(c,sk,s,r.e,w[0],w[1]*1.05,{lw:0,sh:0});limb(c,sk,r.e,r.t,w[1],w[2],{lw:0,sh:0});
  stroke(c,cc=>{const a=Math.atan2(r.t[1]-r.e[1],r.t[0]-r.e[0]);cc.arc(r.e[0],r.e[1],w[1]*.6,a+.6,a+2.2)},'rgba(30,10,40,.3)',1.4);
  band(c,s,r.e,.42,w[0]*.95,PAL.gold);
  band(c,r.e,r.t,.82,w[2]*1.1,PAL.gold);band(c,r.e,r.t,.7,w[2]*1.2,PAL.gold);
  const dir=Math.atan2(r.t[0]-r.e[0],-(r.t[1]-r.e[1]));if(o.hand!=='none')hand(c,sk,r.t,o.ang!=null?o.ang:dir,o.hand||'hold',o.flip);return r}

/* ---------- props ---------- */
function veda(c,x,y,a){c.save();c.translate(x,y);c.rotate(a||0);cut(c,cc=>cc.roundRect(-38,-9,76,18,4),'#f2e4bc',{lw:2});for(let i=-1;i<=1;i++)stroke(c,cc=>{cc.moveTo(-36,i*4);cc.lineTo(36,i*4)},'rgba(140,100,40,.6)',1.2);
  cut(c,cc=>cc.roundRect(-40,-12,80,6,3),'#7a3a1c',{lw:1.6,sh:0});cut(c,cc=>cc.roundRect(-40,7,80,6,3),'#7a3a1c',{lw:1.6,sh:0});stroke(c,cc=>{cc.moveTo(-14,-12);cc.lineTo(-14,13);cc.moveTo(14,-12);cc.lineTo(14,13)},'#c42b3a',2.4);
  glow(c,0,0,46,'255,230,150',.35);c.restore()}
function mala(c,x,y,t){const n=20,ph=t*.6;for(let i=0;i<n;i++){const a=PI/2+((i/n)*TAU+ph*0)%TAU,rx=15,ry=24,u=(i/n+ph*.05)%1,an=-PI/2+u*TAU;const bx=x+Math.cos(an)*rx,by=y+22+Math.sin(an)*ry;cut(c,P.ell(bx,by,3.3,3.3),i%5?'#7a3818':PAL.gold,{sh:0,lw:1})}cut(c,P.ell(x,y+50,4,6),'#c42b3a',{sh:0,lw:1})}
function kamandalu(c,x,y){c.save();c.translate(x,y);stroke(c,cc=>{cc.moveTo(-18,-14);cc.bezierCurveTo(-28,-44,28,-44,18,-14)},INK,5);stroke(c,cc=>{cc.moveTo(-18,-14);cc.bezierCurveTo(-28,-44,28,-44,18,-14)},PAL.gold,3);
  cut(c,cc=>{cc.moveTo(20,-4);cc.quadraticCurveTo(38,-8,44,-22);cc.lineTo(40,-24);cc.quadraticCurveTo(32,-12,20,-12)},goldG(c,20,44),{lw:1.6,sh:0});
  cut(c,P.ell(0,6,24,22),rg(c,-8,-2,2,28,['#ffe6a0','#d99a32','#7a4612']),{lw:2.2});cut(c,cc=>cc.roundRect(-8,-20,16,10,3),goldG(c,-8,8),{lw:1.6,sh:0});stroke(c,cc=>{cc.moveTo(-22,4);cc.quadraticCurveTo(0,12,22,4)},'rgba(90,40,0,.55)',2);c.restore()}
function chakra(c,x,y,r,t,g){c.save();c.translate(x,y);glow(c,0,0,r*3.2,'255,200,90',.42*(g==null?1:g));glow(c,0,0,r*1.6,'255,245,200',.4*(g==null?1:g));c.rotate(t*2.2);
  for(let i=0;i<16;i++){c.save();c.rotate(i/16*TAU);cut(c,cc=>{cc.moveTo(-r*.18,-r*.92);cc.quadraticCurveTo(-r*.05,-r*1.2,r*.12,-r*1.42);cc.quadraticCurveTo(r*.08,-r*1.15,r*.2,-r*.92);cc.closePath()},lg(c,0,-r*.9,0,-r*1.4,['#ffd35a','#ff7a1a']),{sh:0,lw:1.1});c.restore()}
  cut(c,P.ell(0,0,r,r),goldG(c,-r,r),{lw:2,sh:0});cut(c,P.ell(0,0,r*.74,r*.74),'#7a1630',{lw:1.6,sh:0});
  for(let i=0;i<12;i++){c.save();c.rotate(i/12*TAU);cut(c,cc=>{cc.moveTo(-r*.07,-r*.18);cc.lineTo(0,-r*.74);cc.lineTo(r*.07,-r*.18);cc.closePath()},PAL.gold,{sh:0,lw:1});c.restore()}
  cut(c,P.ell(0,0,r*.22,r*.22),goldG(c,-r*.2,r*.2),{lw:1.4,sh:0});gem(c,0,0,r*.1,PAL.ruby);c.restore()}
function shankha(c,x,y,a,s){c.save();c.translate(x,y);c.rotate(a||0);c.scale(s||1,s||1);glow(c,0,-6,48,'235,245,255',.35);
  cut(c,cc=>{cc.moveTo(0,26);cc.bezierCurveTo(-16,22,-24,0,-20,-14);cc.bezierCurveTo(-16,-30,-4,-38,4,-44);cc.bezierCurveTo(10,-32,22,-22,22,-4);cc.bezierCurveTo(22,12,12,24,0,26);cc.closePath()},lg(c,-20,0,22,0,['#ffffff','#f2ece0','#c8bca8']),{lw:2});
  [-22,-12,-2,8].forEach((yy,i)=>stroke(c,cc=>{cc.moveTo(-17+i*2,yy);cc.quadraticCurveTo(2,yy-7,19-i,yy+3)},'rgba(150,120,90,.6)',1.4));
  stroke(c,cc=>{cc.moveTo(2,24);cc.quadraticCurveTo(6,6,4,-40)},'rgba(230,140,160,.6)',2);cut(c,cc=>cc.roundRect(-8,22,16,9,3),goldG(c,-8,8),{lw:1.4,sh:0});c.restore()}
function padma(c,x,y,s,op,t){op=op==null?1:op;c.save();c.translate(x,y);c.scale(s,s);glow(c,0,-14,46*op,'255,170,210',.4*op);
  const row=(n,L,w,spread,col)=>{for(let i=0;i<n;i++){const u=n===1?.5:i/(n-1),a=-PI/2+(u-.5)*spread*op;c.save();c.rotate(a);cut(c,cc=>{cc.moveTo(0,0);cc.bezierCurveTo(-w,-L*.3,-w*.8,-L*.8,0,-L);cc.bezierCurveTo(w*.8,-L*.8,w,-L*.3,0,0)},lg(c,0,0,0,-L,col),{sh:0,lw:1.3});c.restore()}};
  row(5,30,10,2.6,['#e2508a','#ffd0e2']);row(4,27,9,1.5,['#f07aa6','#fff0f6']);row(3,22,8,.7,['#ff9ec0','#ffffff']);cut(c,P.ell(0,-4,6,3.5),'#ffd85a',{sh:0,lw:1});c.restore()}
function gada(c,a,b){const an=Math.atan2(b[1]-a[1],b[0]-a[0]),d=Math.hypot(b[0]-a[0],b[1]-a[1]);c.save();c.translate(a[0],a[1]);c.rotate(an);
  cut(c,cc=>cc.roundRect(0,-4.5,d,9,4),goldG(c,0,0),{lw:1.8});for(let k=1;k<5;k++)cut(c,cc=>cc.roundRect(d*k/6,-6,5,12,2),PAL.goldD,{sh:0,lw:1});
  cut(c,P.smooth([[d-6,-10],[d+20,-24],[d+44,-20],[d+56,0],[d+44,20],[d+20,24],[d-6,10]]),rg(c,d+20,-8,2,40,['#fff2b0','#f2c14e','#9a5e12']),{lw:2.2});
  [12,26,40].forEach(k=>stroke(c,cc=>{cc.moveTo(d+k,-20+Math.abs(k-26)*.2);cc.quadraticCurveTo(d+k+5,0,d+k,20-Math.abs(k-26)*.2)},'rgba(110,60,0,.6)',1.6));gem(c,d+26,0,4,PAL.ruby);
  cut(c,P.ell(d+60,0,6,6),goldG(c,-6,6),{lw:1.4,sh:0});c.restore()}
function damaru(c,x,y,a,t){c.save();c.translate(x,y);c.rotate(a||0);const sw=Math.sin(t*9)*.25;
  [-1,1].forEach(sd=>cut(c,cc=>{cc.moveTo(sd*24,-17);cc.quadraticCurveTo(sd*6,-4,sd*2.5,0);cc.quadraticCurveTo(sd*6,4,sd*24,17);cc.closePath()},lg(c,-24,0,24,0,['#e2a35a','#a8642a','#e2a35a']),{lw:1.8}));
  [-1,1].forEach(sd=>cut(c,P.ell(sd*24,0,4.5,17),'#f3e3b8',{lw:1.5,sh:0}));cut(c,cc=>cc.rect(-4,-4,8,8),'#c42b3a',{lw:1.2,sh:0});
  [-1,1].forEach(sd=>{const ax=sd*Math.cos(sw*sd)*18,ay=14+Math.sin(sw*sd)*10;stroke(c,cc=>{cc.moveTo(0,3);cc.quadraticCurveTo(sd*8,12,ax,ay)},'#5a2a10',1.6);cut(c,P.ell(ax,ay,3.4,3.4),PAL.gold,{lw:1,sh:0})});c.restore()}
function trishul(c,x,yb,len,t,tilt){c.save();c.translate(x,yb);c.rotate(tilt||0);const top=-len;
  cut(c,cc=>cc.roundRect(-4.5,top+40,9,len-40,4),lg(c,-5,0,5,0,['#d8b26a','#8a5a24','#5a3414']),{lw:1.8});
  for(let k=0;k<4;k++)cut(c,cc=>cc.roundRect(-6.5,top+120+k*90,13,7,3),goldG(c,-7,7),{sh:0,lw:1});
  const g=goldG(c,-40,40);
  cut(c,cc=>{cc.moveTo(-6,top+46);cc.bezierCurveTo(-28,top+44,-44,top+26,-42,top-6);cc.lineTo(-50,top-18);cc.lineTo(-34,top-12);cc.bezierCurveTo(-34,top+12,-22,top+28,-6,top+30);cc.closePath()},g,{lw:2});
  cut(c,cc=>{cc.moveTo(6,top+46);cc.bezierCurveTo(28,top+44,44,top+26,42,top-6);cc.lineTo(50,top-18);cc.lineTo(34,top-12);cc.bezierCurveTo(34,top+12,22,top+28,6,top+30);cc.closePath()},g,{lw:2});
  cut(c,cc=>{cc.moveTo(-7,top+40);cc.lineTo(-8,top-14);cc.quadraticCurveTo(-6,top-40,0,top-62);cc.quadraticCurveTo(6,top-40,8,top-14);cc.lineTo(7,top+40);cc.closePath()},g,{lw:2});
  cut(c,P.ell(0,top+44,13,8),goldG(c,-13,13),{lw:1.8,sh:0});gem(c,0,top+44,3.4,PAL.ruby);gem(c,0,top+8,3,PAL.sapph);
  const fl=Math.sin(t*2.4)*6;cut(c,cc=>{cc.moveTo(3,top+56);cc.bezierCurveTo(34,top+60+fl*.4,48+fl,top+90,56+fl,top+130);cc.bezierCurveTo(40+fl*.6,top+104,26,top+78,3,top+72);cc.closePath()},lg(c,0,top+56,50,top+130,['#e8344a','#a01830']),{lw:1.6,sh:0});
  cut(c,cc=>{cc.moveTo(-3,top+56);cc.bezierCurveTo(-26,top+64-fl*.3,-34-fl*.6,top+90,-40-fl*.6,top+118);cc.bezierCurveTo(-26,top+98,-16,top+80,-3,top+72);cc.closePath()},lg(c,0,top+56,-40,top+118,['#ffffff','#d8d0c0']),{lw:1.4,sh:0});
  stroke(c,cc=>{cc.moveTo(0,top+76);cc.lineTo(0,top+96)},'#7a2a10',2);damaru(c,0,top+112,Math.sin(t*2)*.2,t);
  c.restore()}

/* ---------- serpent kit (Shesha, Vasuki) ---------- */
function tube(c,pts,r0,r1,S,o){o=o||{};const n=pts.length,R=k=>lerp(r0,r1,k/(n-1));
  const pass=(col,wm,off)=>{c.strokeStyle=col;c.lineCap='round';c.lineJoin='round';for(let k=0;k<n-1;k++){const a=pts[k],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1;let nx=-dy/d,ny=dx/d;if(ny>0){nx=-nx;ny=-ny}
    const ra=R(k),rb=R(k+1);c.lineWidth=(ra+rb)*wm;c.beginPath();c.moveTo(a[0]+nx*off*ra,a[1]+ny*off*ra);c.lineTo(b[0]+nx*off*rb,b[1]+ny*off*rb);c.stroke()}};
  pass(INK,1+5/(r0+r1),0);pass(S.d,1,0);if(o.belly)pass(S.bellyD,.34,-.62);pass(S.b,.72,.2);pass(S.l,.26,.52);if(o.belly)pass(S.belly,.2,-.66);
  if(o.scales!==false){c.save();c.strokeStyle=S.sc||'rgba(10,40,40,.35)';c.lineWidth=1.4;for(let k=1;k<n-1;k+=1){const a=pts[k-1],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,ux=dx/d,uy=dy/d,r=R(k);
    for(let j=-1;j<=1;j++){const cx=pts[k][0]-uy*r*.45*j,cy=pts[k][1]+ux*r*.45*j;c.beginPath();c.arc(cx,cy,r*.22,Math.atan2(uy,ux)+.4,Math.atan2(uy,ux)+PI*2-.4,true);c.stroke()}}c.restore()}
  if(o.dots){c.save();for(let k=1;k<n-1;k+=2){const r=R(k),a=pts[k-1],b=pts[k+1],dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,ux=dx/d,uy=dy/d;let nx=-uy,ny=ux;if(ny>0){nx=-nx;ny=-ny}
    const cx=pts[k][0]+nx*r*.18,cy=pts[k][1]+ny*r*.18,L=Math.min(d*.5,r*.7),wd=r*.34;cut(c,P.poly([[cx-ux*L,cy-uy*L],[cx+nx*wd,cy+ny*wd],[cx+ux*L,cy+uy*L],[cx-nx*wd,cy-ny*wd]]),S.d,{sh:0,lw:1.3,ink:'rgba(242,193,78,.85)'});
    cut(c,P.ell(cx,cy,2.2,2.2),PAL.gold,{sh:0,lw:0})}c.restore()}}
function ellPts(cx,cy,rx,ry,a0,a1,N){const p=[];for(let k=0;k<=N;k++){const a=lerp(a0,a1,k/N);p.push([cx+Math.cos(a)*rx,cy+Math.sin(a)*ry])}return p}
function hood(c,x,y,ang,s,t,S,o){o=o||{};c.save();c.translate(x,y);c.rotate(ang);c.scale(s,s);
  const hp=[[0,-48],[26,-46],[44,-22],[46,8],[32,40],[14,58],[0,62],[-14,58],[-32,40],[-46,8],[-44,-22],[-26,-46]];
  cut(c,P.smooth(hp),lg(c,-46,0,46,0,[S.l,S.b,S.d]),{lw:2.6});
  const ip=hp.map(([a,b])=>[a*.52,b*.82+7]);cut(c,P.smooth(ip),lg(c,0,-34,0,60,[S.belly,S.bellyD]),{lw:1.5,sh:0});
  c.save();c.beginPath();P.smooth(ip)(c);c.clip();for(let k=-30;k<70;k+=8)stroke(c,cc=>{cc.moveTo(-26,k+3);cc.quadraticCurveTo(0,k-3,26,k+3)},'rgba(120,80,20,.45)',1.3);c.restore();
  [-1,1].forEach(sd=>{stroke(c,cc=>cc.ellipse(sd*29,-6,7,10,sd*.35,0,TAU),PAL.gold,3.2);cut(c,P.ell(sd*29,-6,2.8,3.6),INK,{sh:0,lw:0})});
  for(let k=0;k<5;k++){const a=-PI*.9+k*.2*PI*.9;cut(c,P.ell(Math.cos(a)*38,Math.sin(a)*30-8,2.4,2.4),PAL.gold,{sh:0,lw:.8})}
  // head
  cut(c,P.smooth([[0,-80],[17,-76],[24,-62],[18,-46],[0,-41],[-18,-46],[-24,-62],[-17,-76]]),lg(c,-24,0,24,0,[S.l,S.b,S.d]),{lw:2.2});
  stroke(c,cc=>{cc.moveTo(-9,-72);cc.quadraticCurveTo(0,-76,9,-72)},'rgba(10,30,30,.4)',1.4);
  [-1,1].forEach(sd=>{cut(c,P.ell(sd*11.5,-61,4.6,3.6,sd*-.3),o.eye||'#ffd34a',{sh:0,lw:1.2});cut(c,P.ell(sd*11.5,-61,1.1,3),INK,{sh:0,lw:0})});
  [-1,1].forEach(sd=>cut(c,P.ell(sd*4,-47,1.2,1.6),INK,{sh:0,lw:0}));
  const tf=Math.max(0,Math.sin(t*3.3+(o.ph||0)));if(tf>.2){const L=8+tf*14;stroke(c,cc=>{cc.moveTo(0,-42);cc.lineTo(0,-42+L);cc.lineTo(-4,-38+L+4);cc.moveTo(0,-42+L);cc.lineTo(4,-38+L+4)},'#d8283e',2)}
  if(o.gem){glow(c,0,-90,34,'140,255,230',.7);cut(c,P.poly([[0,-101],[7,-90],[0,-80],[-7,-90]]),'#c8fff4',{sh:0,lw:1.4})}
  c.restore()}

G.TRIKIT={TAU,PI,clamp,lerp,ease,L2,rng,shade,INK,PAL,lg,rg,cut,P,glow,stroke,ik,goldG,gem,beadArc,band,face,hairCap,hairBack,kirita,jataMukuta,halo,hand,limb,limbOutline,arm,veda,mala,kamandalu,chakra,shankha,padma,gada,damaru,trishul,tube,ellPts,hood,setDPR:v=>{DPR=v}};
})(window);
