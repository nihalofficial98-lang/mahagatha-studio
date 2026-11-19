/* Shiva v3 — matches the owner-approved simple geometric flat-vector design (Gemini reference: library/pilot/simple/shiva_*.png).
   Pure code, fully rigged: every limb is a capsule between joints, so poses can be animated.  Origin = between the feet, y negative = up. */
const S3={skin:'#8fb1dd',skinD:'#6e92c6',skinL:'#a9c6ea',joint:'#7da0d3',hair:'#1d1b27',hairL:'#2f2c3c',beads:'#6a3a22',tiger:'#f2a03c',tigerL:'#f7b95a',stripe:'#2b1b12',fur:'#fbe7c2',gold:'#f0c13e',goldD:'#c99a22',snake:'#3fa05a',snakeD:'#2c7a42',snakeL:'#7fd08a',rope:'#5a3a24',white:'#f6f3ee',red:'#e03a30',damaru:'#6b4630',cream:'#f2e6c6'};
const lerp3=(a,b,t)=>a+(b-a)*t;
function cap(c,a,b,wa,wb,col){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,nx=-dy/d,ny=dx/d;c.fillStyle=col;c.beginPath();c.moveTo(a[0]+nx*wa,a[1]+ny*wa);c.lineTo(b[0]+nx*wb,b[1]+ny*wb);c.arc(b[0],b[1],wb,Math.atan2(ny,nx),Math.atan2(-ny,-nx),false);c.lineTo(a[0]-nx*wa,a[1]-ny*wa);c.arc(a[0],a[1],wa,Math.atan2(-ny,-nx),Math.atan2(ny,nx),false);c.closePath();c.fill()}
function ik(Sh,T,l1,l2,side){const dx=T[0]-Sh[0],dy=T[1]-Sh[1];let d=Math.hypot(dx,dy);const m=l1+l2-.5;if(d>m){T=[Sh[0]+dx*m/d,Sh[1]+dy*m/d];d=m}const a=(l1*l1-l2*l2+d*d)/(2*d),h=Math.sqrt(Math.max(0,l1*l1-a*a)),ux=(T[0]-Sh[0])/d,uy=(T[1]-Sh[1])/d;return {e:[Sh[0]+ux*a+side*(-uy)*h,Sh[1]+uy*a+side*ux*h],t:T}}
function limb3(c,A,T,l1,l2,side,w,col,opt={}){const r=ik(A,T,l1,l2,side),E=r.e;
  cap(c,A,E,w[0],w[1],col);cap(c,E,r.t,w[1],w[2],col);
  c.globalAlpha=.35;cap(c,[A[0]+side*w[0]*.35,A[1]],[E[0]+side*w[1]*.35,E[1]],w[0]*.55,w[1]*.55,S3.skinD);cap(c,[E[0]+side*w[1]*.3,E[1]],[r.t[0]+side*w[2]*.3,r.t[1]],w[1]*.5,w[2]*.5,S3.skinD);c.globalAlpha=1;
  if(opt.band){[[.62,w[1]*1.12,S3.gold]].forEach(([u,ww,cc])=>{const x=lerp3(A[0],E[0],.5),y=lerp3(A[1],E[1],.5);c.save();c.translate(x,y);c.rotate(Math.atan2(E[1]-A[1],E[0]-A[0])+1.57);c.fillStyle=cc;c.beginPath();c.roundRect(-w[0]*1.08,-7,w[0]*2.16,14,5);c.fill();c.restore()})}
  return r}
function joint3(c,p,r){c.fillStyle=S3.joint;c.beginPath();c.arc(p[0],p[1],r,0,7);c.fill();c.fillStyle='rgba(255,255,255,.18)';c.beginPath();c.arc(p[0]-r*.25,p[1]-r*.25,r*.55,0,7);c.fill()}
function hand3(c,p,fist,ang=0){c.save();c.translate(p[0],p[1]);c.rotate(ang);c.fillStyle=S3.skin;
  if(fist){c.beginPath();c.roundRect(-14,-14,28,28,9);c.fill();c.strokeStyle=S3.skinD;c.lineWidth=2.4;c.beginPath();[-5,3].forEach(x=>{c.moveTo(x,-10);c.lineTo(x,8)});c.stroke()}
  else{c.beginPath();c.roundRect(-11,-8,22,36,9);c.fill();c.fillStyle=S3.skin;c.beginPath();c.ellipse(13,6,5,11,-.4,0,7);c.fill();c.strokeStyle=S3.skinD;c.lineWidth=2;c.beginPath();c.moveTo(-3,10);c.lineTo(-3,24);c.moveTo(4,10);c.lineTo(4,25);c.stroke()}c.restore()}
function stripes3(c,x,y,w,h,seed){c.fillStyle=S3.stripe;for(let i=0;i<9;i++){const u=(i+.5)/9,px=x+u*w,l=h*(.55+((i*37+seed)%5)*.1);c.save();c.translate(px,y+((i%2)?6:0));c.rotate((u-.5)*.5);c.beginPath();c.moveTo(-5,0);c.quadraticCurveTo(2,l*.5,0,l);c.quadraticCurveTo(-1,l*.5,-5,0);c.fill();if(i%2===0){c.beginPath();c.moveTo(8,h*.3);c.quadraticCurveTo(13,h*.55,10,h*.8);c.quadraticCurveTo(7,h*.55,8,h*.3);c.fill()}c.restore()}}
const POSE3={
 calm:{hd:[0,-452],nk:[0,-388],sL:[-82,-372],sR:[82,-372],hL:[-112,-236],hR:[118,-292],hipL:[-30,-236],hipR:[30,-236],kL:[-32,-124],kR:[32,-124],fL:[-36,-8],fR:[36,-8],tri:{x:130,top:-600,bot:0},fistR:true},
 rage:{hd:[4,-444],nk:[2,-382],sL:[-84,-368],sR:[80,-366],hL:[-176,-430],hR:[128,-298],hipL:[-32,-232],hipR:[36,-230],kL:[-96,-120],kR:[104,-116],fL:[-130,-8],fR:[140,-8],tri:{x:138,top:-596,bot:-6},fistR:true,openL:true}
};
function head3(c,x,y,o){const k=o.k||0,closed=o.closed,rage=k>.5;c.save();c.translate(x,y);
  // back locks
  c.fillStyle=S3.hair;[-1,1].forEach(sd=>{for(let i=0;i<4;i++){const sw=Math.sin((o.t||0)*1.6+i+sd)*(2+(o.imp||0)*4);c.beginPath();c.moveTo(sd*(34+i*7),-30);c.bezierCurveTo(sd*(70+i*9),0,sd*(76+i*9+sw),60,sd*(58+i*10+sw),(rage?112:136)-i*10);c.lineTo(sd*(40+i*9),(rage?100:124)-i*10);c.bezierCurveTo(sd*(44+i*7),50,sd*(36+i*6),10,sd*(30+i*5),-20);c.closePath();c.fill()}});
  // bun
  const bg=c.createRadialGradient(-14,-100,6,0,-92,60);bg.addColorStop(0,S3.hairL);bg.addColorStop(1,S3.hair);c.fillStyle=bg;c.beginPath();c.ellipse(0,-92,42,50,0,0,7);c.fill();
  c.strokeStyle='rgba(255,255,255,.16)';c.lineWidth=5;c.lineCap='round';for(let i=0;i<4;i++){c.beginPath();c.ellipse(0,-92,36-i*8,44-i*10,0,.5+i*.6,Math.PI*1.6+i*.6);c.stroke()}
  c.fillStyle=S3.gold;c.beginPath();c.roundRect(-34,-52,68,11,5);c.fill();c.fillStyle=S3.beads;for(let i=-3;i<=3;i++){c.beginPath();c.arc(i*10,-46,4.4,0,7);c.fill()}
  // moon (only ornament in the hair)
  c.fillStyle=S3.white;c.beginPath();c.arc(34,-98,19,.7,5.6);c.arc(42,-98,15,5.4,.9,true);c.fill();
  // ears + rings
  c.fillStyle=S3.skinD;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*58,2,9,15,0,0,7);c.fill();c.strokeStyle=S3.gold;c.lineWidth=5;c.beginPath();c.arc(sd*60,20,10,0,7);c.stroke()});
  // face
  const fg=c.createLinearGradient(-60,0,60,0);fg.addColorStop(0,S3.skinL);fg.addColorStop(.35,S3.skin);fg.addColorStop(1,S3.skinD);c.fillStyle=fg;c.beginPath();c.moveTo(-58,-26);c.bezierCurveTo(-60,-64,60,-64,58,-26);c.bezierCurveTo(60,24,40,60,0,64);c.bezierCurveTo(-40,60,-60,24,-58,-26);c.fill();
  // ash lines + third eye
  c.fillStyle=S3.white;[-46,-38,-30].forEach((yy,i)=>{c.beginPath();c.roundRect(-22+i*1,yy,44-i*2,5,2.5);c.fill()});
  c.fillStyle=S3.red;c.beginPath();c.ellipse(0,-14,4.4,8.5,0,0,7);c.fill();c.fillStyle='rgba(255,255,255,.5)';c.beginPath();c.ellipse(-1,-16,1.4,3,0,0,7);c.fill();
  // brows
  c.fillStyle='#14121c';[-1,1].forEach(sd=>{const a=rage?-.38:-.08,l=rage?3:-2;c.save();c.translate(sd*24,-2+l);c.rotate(sd*a*-1+(sd<0?0:0));c.scale(sd,1);c.beginPath();c.roundRect(-4,-6,34,rage?11:8,5);c.fill();c.restore()});
  // eyes
  [-1,1].forEach(sd=>{const ex=sd*24,ey=16;
    if(closed){c.strokeStyle='#14121c';c.lineWidth=3.4;c.lineCap='round';c.beginPath();c.moveTo(ex-13,ey);c.quadraticCurveTo(ex,ey+8,ex+13,ey);c.stroke();return}
    if(rage){c.fillStyle='#f8f4ee';c.beginPath();c.ellipse(ex,ey,13,9,0,0,7);c.fill();c.fillStyle='#ff2a22';c.beginPath();c.arc(ex,ey,8.4,0,7);c.fill();c.fillStyle='rgba(255,230,200,.9)';c.beginPath();c.arc(ex-2,ey-2,2.6,0,7);c.fill()}
    else{c.fillStyle='#f8f4ee';c.beginPath();c.ellipse(ex,ey,13,8.5,0,0,7);c.fill();c.fillStyle='#2a1a1a';c.beginPath();c.arc(ex,ey,6.4,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(ex-2,ey-2,2,0,7);c.fill()}});
  // nose + mouth
  c.strokeStyle=S3.skinD;c.lineWidth=3;c.lineCap='round';c.beginPath();c.moveTo(-3,20);c.quadraticCurveTo(-8,34,-3,38);c.stroke();
  c.strokeStyle='#3a1f2a';c.lineWidth=3.6;c.beginPath();if(rage){c.moveTo(-14,50);c.quadraticCurveTo(0,43,14,50)}else{c.moveTo(-12,46);c.quadraticCurveTo(0,52,12,46)}c.stroke();
  c.restore()}
function serpent3(c,t,sL,sR){const w=Math.sin(t*2)*2;c.lineCap='round';c.strokeStyle=S3.snakeD;c.lineWidth=24;c.beginPath();c.moveTo(sL[0]+8,sL[1]+6);c.bezierCurveTo(sL[0]+10,sL[1]+50,-20,sL[1]+60,6,sL[1]+42);c.bezierCurveTo(34,sL[1]+28,sR[0]-4,sL[1]+12,sR[0]+12,sL[1]-14+w);c.stroke();
  c.strokeStyle=S3.snake;c.lineWidth=17;c.beginPath();c.moveTo(sL[0]+8,sL[1]+6);c.bezierCurveTo(sL[0]+10,sL[1]+50,-20,sL[1]+60,6,sL[1]+42);c.bezierCurveTo(34,sL[1]+28,sR[0]-4,sL[1]+12,sR[0]+12,sL[1]-14+w);c.stroke();
  c.strokeStyle=S3.snakeL;c.lineWidth=3;c.setLineDash([3,10]);c.beginPath();c.moveTo(sL[0]+8,sL[1]);c.bezierCurveTo(sL[0]+10,sL[1]+44,-20,sL[1]+54,6,sL[1]+36);c.stroke();c.setLineDash([]);
  const hx=sR[0]+12,hy=sL[1]-16+w;c.fillStyle=S3.snake;c.beginPath();c.moveTo(hx-14,hy+10);c.bezierCurveTo(hx-26,hy-14,hx-10,hy-40,hx+4,hy-42);c.bezierCurveTo(hx+24,hy-40,hx+30,hy-16,hx+16,hy+10);c.closePath();c.fill();c.fillStyle=S3.snakeL;c.globalAlpha=.6;c.beginPath();c.ellipse(hx+2,hy-18,8,17,0,0,7);c.fill();c.globalAlpha=1;c.fillStyle='#fff';c.beginPath();c.arc(hx-3,hy-26,3.4,0,7);c.arc(hx+9,hy-26,3.4,0,7);c.fill();c.fillStyle='#111';c.beginPath();c.arc(hx-3,hy-26,1.6,0,7);c.arc(hx+9,hy-26,1.6,0,7);c.fill()}
function trident3(c,x,top,bot,t){c.save();c.translate(x,0);c.strokeStyle=S3.goldD;c.lineWidth=9;c.lineCap='round';c.beginPath();c.moveTo(0,bot);c.lineTo(0,top);c.stroke();c.strokeStyle=S3.gold;c.lineWidth=6;c.beginPath();c.moveTo(-1,bot);c.lineTo(-1,top);c.stroke();
  c.strokeStyle=S3.gold;c.lineWidth=8;c.beginPath();c.moveTo(-34,top-58);c.lineTo(-34,top-14);c.quadraticCurveTo(0,top+26,34,top-14);c.lineTo(34,top-58);c.stroke();
  [[-34,top-58],[0,top-74],[34,top-58]].forEach(([dx,dy],i)=>{c.fillStyle=S3.gold;c.beginPath();c.moveTo(dx-9,dy);c.lineTo(dx,dy-(i===1?54:46));c.lineTo(dx+9,dy);c.closePath();c.fill()});c.beginPath();c.moveTo(0,top+20);c.lineTo(0,top-76);c.stroke();
  const sw=Math.sin(t*3)*3;c.save();c.translate(0,top+70);c.rotate(sw*.03);c.fillStyle=S3.damaru;[-1,1].forEach(sd=>{c.beginPath();c.moveTo(sd*28,-22);c.quadraticCurveTo(sd*9,-4,sd*4,0);c.quadraticCurveTo(sd*9,4,sd*28,22);c.closePath();c.fill()});c.fillStyle=S3.cream;[-1,1].forEach(sd=>{c.beginPath();c.ellipse(sd*28,0,5,22,0,0,7);c.fill()});c.strokeStyle=S3.red;c.lineWidth=3;c.beginPath();c.moveTo(0,0);c.quadraticCurveTo(26+sw,16,30+sw,46);c.stroke();c.fillStyle=S3.red;c.beginPath();c.arc(30+sw,48,5,0,7);c.fill();c.restore();c.restore()}
function drawShiva3(c,o){const P=o.P||POSE3[o.pose||'calm'],t=o.t||0,rage=o.k!=null?o.k>.5:o.pose==='rage',br=Math.sin(t*1.7)*2.2,sw=Math.sin(t*1.5)+(rage?3:0);c.save();
  const Q=JSON.parse(JSON.stringify(P));['hd','nk','sL','sR'].forEach(k=>{Q[k][1]+=br});Q.hL[1]+=br*.6;Q.hR[1]+=br*.6;
  // trident behind
  const T=Q.tri;trident3(c,T.x,T.top,T.bot,t);
  // legs
  const leg=(h,f,side)=>{const r=ik(h,f,80,84,side);cap(c,h,r.e,34,26,S3.skin);cap(c,r.e,f,26,19,S3.skin);c.globalAlpha=.3;cap(c,[h[0]+side*12,h[1]],[r.e[0]+side*9,r.e[1]],12,9,S3.skinD);c.globalAlpha=1;joint3(c,r.e,20);c.fillStyle=S3.skin;c.beginPath();c.ellipse(f[0]+side*7,f[1]-4,30,12,0,0,7);c.fill();c.fillStyle=S3.skinD;c.globalAlpha=.4;c.beginPath();c.ellipse(f[0]+side*8,f[1]-1,19,4,0,0,7);c.fill();c.globalAlpha=1;return r};
  const lL=leg(Q.hipL,Q.fL,-1),lR=leg(Q.hipR,Q.fR,1);
  // torso
  const tg=c.createLinearGradient(-70,0,70,0);tg.addColorStop(0,S3.skinL);tg.addColorStop(.4,S3.skin);tg.addColorStop(1,S3.skinD);c.fillStyle=tg;
  c.beginPath();c.moveTo(Q.sL[0]-8,Q.sL[1]);c.bezierCurveTo(-76,Q.sL[1]+40,-62,Q.hipL[1]-60,-46,Q.hipL[1]-6);c.lineTo(46,Q.hipR[1]-6);c.bezierCurveTo(62,Q.hipL[1]-60,76,Q.sR[1]+40,Q.sR[0]+8,Q.sR[1]);c.bezierCurveTo(30,Q.nk[1]-8,-30,Q.nk[1]-8,Q.sL[0]-8,Q.sL[1]);c.fill();
  c.strokeStyle='rgba(30,40,100,.4)';c.lineWidth=2.6;c.lineCap='round';c.beginPath();c.moveTo(0,Q.sL[1]+40);c.lineTo(0,Q.hipL[1]-24);[-1,1].forEach(sd=>{c.moveTo(sd*5,Q.sL[1]+30);c.quadraticCurveTo(sd*26,Q.sL[1]+54,sd*42,Q.sL[1]+34);for(let i=0;i<3;i++){c.moveTo(sd*5,Q.hipL[1]-92+i*24);c.quadraticCurveTo(sd*20,Q.hipL[1]-86+i*24,sd*28,Q.hipL[1]-92+i*24)}});c.stroke();
  c.fillStyle=S3.white;[0,1,2].forEach(i=>{c.beginPath();c.roundRect(-30+i*2,Q.sL[1]+62+i*13,60-i*4,6,3);c.fill()});
  // tiger skirt
  const wy=Q.hipL[1]-14,sp=Math.max(0,(Q.kR[0]-Q.kL[0])/2-30),topW=64+sp*.2,botW=82+sw*3+sp*.7,hem=118;
  c.save();c.beginPath();c.moveTo(-topW,wy);c.lineTo(topW,wy);c.lineTo(botW,wy+hem*.6);for(let i=0;i<=9;i++){const u=i/9,x=lerp3(botW,-botW,u),y=wy+hem+((i%2)?12:-2)+Math.sin(u*5+sw)*3;c.lineTo(x,y)}c.lineTo(-botW,wy+hem*.6);c.closePath();const kg=c.createLinearGradient(-botW,0,botW,0);kg.addColorStop(0,S3.tigerL);kg.addColorStop(.5,S3.tiger);kg.addColorStop(1,'#d98424');c.fillStyle=kg;c.fill();c.clip();stripes3(c,-topW,wy+4,2*topW,hem*.8,3);stripes3(c,-botW+8,wy+hem*.45,2*botW-16,hem*.55,9);c.fillStyle=S3.fur;c.fillRect(-botW-4,wy+hem-8,2*botW+8,16);c.restore();
  // rope belt + knot
  c.fillStyle=S3.rope;c.beginPath();c.roundRect(-topW-4,wy-9,2*topW+8,16,7);c.fill();c.fillStyle='#43291a';c.beginPath();c.arc(10,wy+2,10,0,7);c.fill();c.beginPath();c.moveTo(4,wy+8);c.lineTo(-2,wy+52+sw*3);c.lineTo(8,wy+50);c.lineTo(14,wy+10);c.fill();
  // mala
  c.fillStyle=S3.beads;for(let i=0;i<15;i++){const u=i/14,bx=-40+u*80,by=Q.nk[1]+18+Math.sin(u*3.14)*58;c.beginPath();c.arc(bx,by,5.4,0,7);c.fill()}
  // neck + serpent
  c.fillStyle=S3.skinD;c.beginPath();c.roundRect(Q.nk[0]-24,Q.hd[1]+52,48,Q.nk[1]-Q.hd[1]-34,8);c.fill();serpent3(c,t,Q.sL,Q.sR);
  // head
  c.save();c.translate(Q.hd[0],Q.hd[1]+40);c.scale(1.34,1.34);c.translate(-Q.hd[0],-Q.hd[1]-40);head3(c,Q.hd[0],Q.hd[1],{k:o.k!=null?o.k:(rage?1:0),closed:o.closed,t:t,imp:o.imp});c.restore();
  // arms
  const aL=limb3(c,Q.sL,Q.hL,60,58,-1,[27,22,18],S3.skin,{band:true}),aR=limb3(c,Q.sR,Q.hR,60,58,1,[27,22,18],S3.skin,{band:true});
  joint3(c,Q.sL,26);joint3(c,Q.sR,26);joint3(c,aL.e,18);joint3(c,aR.e,18);
  hand3(c,aL.t,!Q.openL&&false,.1);
  // right hand grips the trident
  c.fillStyle=S3.skin;c.beginPath();c.roundRect(aR.t[0]-17,aR.t[1]-14,34,28,10);c.fill();c.strokeStyle=S3.skinD;c.lineWidth=2.4;c.beginPath();[-6,2,10].forEach(y=>{c.moveTo(aR.t[0]-14,aR.t[1]+y);c.lineTo(aR.t[0]+14,aR.t[1]+y)});c.stroke();
  c.restore()}
