/* Paper-cut backgrounds (same look as the Opus characters): layered cloud banks built from puffs of varied size, cut ridges
   with snow and rim light, wave rows with foam curls, mandala rings of cut petals, flame-petal suns, paper-cut palace hall.
   Every layer = drop shadow + gradient fill + soft ink edge.  Overrides BG.* from scenes.js; same parameters
   (sky, sun, sx, sy, seed, ridge, river, trees, px/pw/ct, strata, rgb, spin, cols ...) so every shot plan keeps working. */
(function(){
const TAU=Math.PI*2,PI=Math.PI,INK='rgba(24,8,34,.5)';
const hx=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)),hex=a=>'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
const shd=(h,f)=>hex(hx(h).map(v=>f<1?v*f:v+(255-v)*(f-1)));
const mix=(a,b,u)=>hex(hx(a).map((v,i)=>v+(hx(b)[i]-v)*u));
const lum=h=>{const c=hx(h);return(c[0]*.3+c[1]*.59+c[2]*.11)/255};
function cutP(fn,fill,o){o=o||{};ctx.save();ctx.beginPath();fn();if(o.sh!==0){ctx.shadowColor=o.shc||'rgba(10,2,24,.36)';ctx.shadowBlur=(o.blur==null?9:o.blur)*SC_;ctx.shadowOffsetY=(o.sy==null?5:o.sy)*SC_}
  ctx.fillStyle=fill;ctx.fill();ctx.shadowColor='transparent';ctx.shadowBlur=0;ctx.shadowOffsetY=0;if(o.lw!==0){ctx.lineWidth=o.lw||2;ctx.strokeStyle=o.ink||INK;ctx.lineJoin='round';ctx.stroke()}ctx.restore()}
const vg=(y0,y1,st)=>{const g=ctx.createLinearGradient(0,y0,0,y1);st.forEach((c,i)=>g.addColorStop(i/(st.length-1),c));return g};
const CC=(base)=>({light:shd(base,1.28),mid:base,dark:shd(base,.6)});

/* ---- cloud bank: puffs of varied radius at uneven heights, merged into one paper silhouette (outline only on the outside),
   a second inner row of smaller puffs cut in a lighter tone, rim highlights on the big billows only ---- */
function puffs(seed,y,rmin,rmax,x0,x1,wav){const r=rng(seed),P=[];let x=x0;while(x<x1){const big=r()<.22,rad=(rmin+(rmax-rmin)*Math.pow(r(),1.5))*(big?1.45:1);
    const yy=y-rad*.32+(r()-.5)*rmax*.55+Math.sin(x*.0042+seed)*wav;P.push([x+rad*.6,yy,rad]);x+=rad*(.55+r()*.75)}return P}
function blob(P,yb,pad){P.forEach(([x,y,r])=>{ctx.moveTo(x+r+pad,y);ctx.arc(x,y,r+pad,0,TAU)});const x0=P[0][0]-P[0][2],x1=P[P.length-1][0]+P[P.length-1][2];ctx.rect(x0-pad,Math.min(...P.map(p=>p[1])),x1-x0+2*pad,yb-Math.min(...P.map(p=>p[1]))+pad)}
function deck(seed,y,h,C,t,drift,rmin,rmax){const dx=Math.sin(t*.12+seed)*drift;ctx.save();ctx.translate(dx,0);
  const P=puffs(seed,y,rmin,rmax,-380,W+420,h*.12),yb=y+h+400;
  // ink edge + shadow (stroke pass), then the fill hides every inner seam
  ctx.save();ctx.beginPath();blob(P,yb,0);ctx.shadowColor='rgba(10,2,24,.34)';ctx.shadowBlur=11*SC_;ctx.shadowOffsetY=7*SC_;ctx.strokeStyle='rgba(24,8,34,.42)';ctx.lineWidth=4;ctx.lineJoin='round';ctx.stroke();ctx.fillStyle=C.dark;ctx.fill();ctx.restore();
  ctx.beginPath();blob(P,yb,0);ctx.fillStyle=vg(y-rmax*1.2,y+h,[C.light,C.mid,C.dark]);ctx.fill();
  // inner row: smaller puffs, lighter paper, lying lower inside the bank
  const Q=puffs(seed+101,y+rmax*.55,rmin*.55,rmax*.62,-360,W+400,h*.08).filter((p,i)=>i%3!==1);
  ctx.save();ctx.beginPath();blob(P,yb,0);ctx.clip();
    Q.forEach(([x,y2,r],i)=>{ctx.fillStyle=i%2?'rgba(255,255,255,.08)':'rgba(30,10,50,.07)';ctx.beginPath();ctx.arc(x,y2,r,PI,TAU);ctx.fill()});
  // shade at the bottom of the bank so it reads as volume
  ctx.fillStyle=vg(y+h*.25,y+h,['rgba(20,8,40,0)','rgba(20,8,40,.28)']);ctx.fillRect(-500,y,W+1000,h+400);ctx.restore();
  // rim light on the bigger billows (upper-left quarter)
  ctx.strokeStyle='rgba(255,255,255,.42)';ctx.lineCap='round';P.forEach(([x,y2,r])=>{if(r<(rmin+rmax)*.55)return;ctx.lineWidth=2.6;ctx.beginPath();ctx.arc(x,y2,r-5,PI*1.08,PI*1.5);ctx.stroke()});
  ctx.restore()}
// a few separate cloudlets floating in open sky
function cloudlets(seed,n,y0,y1,C,t,sc){const r=rng(seed);for(let i=0;i<n;i++){const cx=r()*(W+200)-100+Math.sin(t*.1+i)*12,cy=y0+r()*(y1-y0),s=(.6+r()*.7)*(sc||1);
  const P=[[cx-40*s,cy+6*s,22*s],[cx-14*s,cy-8*s,30*s],[cx+20*s,cy-2*s,26*s],[cx+44*s,cy+8*s,17*s]];ctx.save();ctx.beginPath();P.forEach(([x,y,rr])=>{ctx.moveTo(x+rr,y);ctx.arc(x,y,rr,0,TAU)});ctx.rect(cx-40*s,cy+4*s,84*s,16*s);
  ctx.shadowColor='rgba(10,2,24,.3)';ctx.shadowBlur=7*SC_;ctx.shadowOffsetY=4*SC_;ctx.strokeStyle='rgba(24,8,34,.35)';ctx.lineWidth=3;ctx.stroke();ctx.shadowColor='transparent';ctx.fillStyle=vg(cy-30*s,cy+20*s,[C.light,C.mid]);ctx.fill();ctx.restore()}}
// flame-petal sun
function sunburst(x,y,r,t,cols,g){g=g==null?1:g;ctx.save();ctx.translate(x,y);glow(0,0,r*2.6,'255,200,110',.26*g);const n=26;ctx.save();ctx.rotate(t*.05);
  for(let i=0;i<n;i++){const f=1+.08*Math.sin(t*2.6+i*1.9);ctx.save();ctx.rotate(i/n*TAU);cutP(()=>{ctx.moveTo(-r*.11,-r*.92);ctx.bezierCurveTo(-r*.13,-r*1.06,-r*.03,-r*1.12*f,r*.03,-r*1.3*f);ctx.bezierCurveTo(r*.02,-r*1.14*f,r*.13,-r*1.06,r*.11,-r*.92);ctx.closePath()},cols[1],{sh:0,lw:1.2});ctx.restore()}ctx.restore();
  const rg=ctx.createRadialGradient(0,0,r*.1,0,0,r);rg.addColorStop(0,cols[0]);rg.addColorStop(.6,cols[1]);rg.addColorStop(1,cols[2]);cutP(()=>ctx.arc(0,0,r,0,TAU),rg,{sh:0,lw:2.2});
  ctx.setLineDash([1,7]);ctx.strokeStyle='rgba(255,250,225,.85)';ctx.lineWidth=2.2;ctx.lineCap='round';ctx.beginPath();ctx.arc(0,0,r*.9,0,TAU);ctx.stroke();ctx.setLineDash([]);ctx.restore()}
// concentric leaf rings (mandala), outline only
function mandala(x,y,t,rgb,a,rings,spin){ctx.save();ctx.translate(x,y);ctx.rotate(t*(spin==null?.03:spin));ctx.globalAlpha=a;ctx.strokeStyle=`rgb(${rgb})`;ctx.lineWidth=1.6;
  for(let k=0;k<(rings||4);k++){const R=130+k*84,n=12+k*8;ctx.beginPath();ctx.arc(0,0,R,0,TAU);ctx.stroke();for(let i=0;i<n;i++){ctx.save();ctx.rotate(i/n*TAU+k*.2);ctx.beginPath();ctx.moveTo(0,-R);ctx.quadraticCurveTo(14,-R-26,0,-R-52);ctx.quadraticCurveTo(-14,-R-26,0,-R);ctx.stroke();ctx.restore()}}ctx.restore()}
// cut-paper mandala: filled petal rings in tones of one colour, each ring a layer with a soft shadow
function paperMandala(x,y,t,base,rings,spin,a){ctx.save();ctx.translate(x,y);ctx.globalAlpha*=a==null?1:a;for(let k=rings-1;k>=0;k--){const R=110+k*92,n=14+k*6,col=shd(base,1+.09*(rings-k));ctx.save();ctx.rotate(t*(spin||.02)*(k%2?-1:1)+k*.3);
  cutP(()=>{for(let i=0;i<n;i++){const a0=i/n*TAU,a1=(i+1)/n*TAU,am=(a0+a1)/2;ctx.moveTo(Math.cos(a0)*R,Math.sin(a0)*R);ctx.quadraticCurveTo(Math.cos(am)*(R+60),Math.sin(am)*(R+60),Math.cos(a1)*R,Math.sin(a1)*R)}ctx.arc(0,0,R,0,TAU)},col,{blur:10,sy:4,lw:1.4,ink:'rgba(10,4,20,.35)'});
  ctx.strokeStyle='rgba(255,240,200,.12)';ctx.lineWidth=1.4;for(let i=0;i<n;i++){const am=(i+.5)/n*TAU;ctx.beginPath();ctx.moveTo(Math.cos(am)*(R+6),Math.sin(am)*(R+6));ctx.lineTo(Math.cos(am)*(R+40),Math.sin(am)*(R+40));ctx.stroke()}ctx.restore()}
  ctx.restore()}
function waves(y,rows,cols,t,amp,foam){for(let k=0;k<rows;k++){const yy=y+k*24,off=mod(t*(14+k*6),90);ctx.beginPath();ctx.moveTo(-400,H+400);ctx.lineTo(-400-off,yy);for(let x=-400-off;x<W+500;x+=45){ctx.quadraticCurveTo(x+11,yy-amp-Math.sin(x*.01+t+k)*3,x+22,yy);ctx.quadraticCurveTo(x+34,yy+amp*.4,x+45,yy)}ctx.lineTo(W+500,H+400);ctx.closePath();
  ctx.save();ctx.shadowColor='rgba(8,8,40,.35)';ctx.shadowBlur=7*SC_;ctx.shadowOffsetY=-3*SC_;ctx.fillStyle=cols[k%cols.length];ctx.fill();ctx.restore();ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=1.8;ctx.stroke();
  if(foam){const r=rng(k*7+3);ctx.strokeStyle='rgba(255,255,255,.55)';ctx.lineWidth=2;for(let x=-400-off+22;x<W+500;x+=45*(2+Math.floor(r()*3))){ctx.beginPath();ctx.arc(x+6,yy-amp*.6,5,PI*1.1,PI*2.2);ctx.stroke()}}}}
function peaks(pts,fill,snow,rim){cutP(()=>{ctx.moveTo(pts[0][0],H+400);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(pts[pts.length-1][0],H+400);ctx.closePath()},fill,{blur:8});
  if(rim){ctx.strokeStyle=rim;ctx.lineWidth=2.4;ctx.lineCap='round';ctx.beginPath();for(let i=1;i<pts.length;i++){if(pts[i][1]<pts[i-1][1]){ctx.moveTo(pts[i-1][0],pts[i-1][1]+3);ctx.lineTo(pts[i][0],pts[i][1]+3)}}ctx.stroke()}
  if(!snow)return;pts.forEach(([x,y],i)=>{if(!i||i>=pts.length-1||pts[i-1][1]<=y||pts[i+1][1]<=y)return;const L=pts[i-1],R=pts[i+1],f=.3,a=[x+(L[0]-x)*f,y+(L[1]-y)*f],b=[x+(R[0]-x)*f,y+(R[1]-y)*f];
    cutP(()=>{ctx.moveTo(x,y);ctx.lineTo(b[0],b[1]);ctx.lineTo(b[0]-(b[0]-x)*.3,b[1]+8);ctx.lineTo(x+(b[0]-x)*.1,b[1]-2);ctx.lineTo(a[0]+(x-a[0])*.4,a[1]+10);ctx.lineTo(a[0],a[1]);ctx.closePath()},snow,{sh:0,lw:1.4})})}
const stars=(t,n,seed,ym)=>{const r=rng(seed);for(let i=0;i<n;i++){const x=r()*W,y=r()*ym,s=.5+r()*1.6,tw=.4+.6*Math.abs(Math.sin(t*1.7+i));ctx.fillStyle=`rgba(255,250,235,${(.25+.7*tw)*r()})`;ctx.beginPath();ctx.arc(x,y,s,0,TAU);ctx.fill();if(s>1.7){glow(x,y,s*6,'255,240,210',.25*tw);ctx.strokeStyle=`rgba(255,250,235,${.5*tw})`;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x-s*4,y);ctx.lineTo(x+s*4,y);ctx.moveTo(x,y-s*4);ctx.lineTo(x,y+s*4);ctx.stroke()}}};
// paper tree: trunk + three layered round crowns
function ptree(x,y,h,t,i,c,trunk){cutP(()=>ctx.roundRect(x-7,y-h*.55,14,h*.55,5),vg(0,1,[trunk||'#3a2418',shd(trunk||'#3a2418',.6)]),{blur:5});
  [[0,-h*.78,h*.32],[-h*.2,-h*.6,h*.24],[h*.2,-h*.6,h*.24]].forEach(([dx,dy,rr],k)=>cutP(()=>ctx.arc(x+dx+Math.sin(t*.8+i)*2,y+dy,rr,0,TAU),vg(y+dy-rr,y+dy+rr,[shd(c[k%2],1.25),c[k%2],shd(c[k%2],.7)]),{blur:6}))}
// a ridge line as cut paper with a lit top edge
function ridgeP(base,amp,freq,seed,col,par,rim){const r=rng(seed);const pts=[[-520,base]];for(let x=-500;x<=W+500;x+=46)pts.push([x,base-amp*(.5+.35*Math.sin(x*freq+seed)+.15*Math.sin(x*freq*3.1+seed*2))-r()*10]);
  cutP(()=>{ctx.moveTo(-520,H+400);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(W+520,H+400);ctx.closePath()},vg(base-amp,base+160,[shd(col,1.15),col,shd(col,.72)]),{blur:7});
  if(rim){ctx.strokeStyle=rim;ctx.lineWidth=2;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]+2):ctx.moveTo(p[0],p[1]+2));ctx.stroke()}return pts}

Object.assign(BG,{
 cloudscape(S,t){const sky=S.sky||['#2a3a86','#7a8ad0','#f0b8c0','#fff0d0'];skyG(sky,-300,H+300);const sx=S.sx??CX,sy=S.sy??250,sun=S.sun||'255,236,190',warm=hx(sky[sky.length-1]).reduce((a,b)=>a+b)>560,sd=S.seed||21;
  glow(sx,sy,460,sun,.38);layer(.06,()=>{stars(t,40,sd,180);rays(sx,sy,t,sun,.05,14,1500);sunburst(sx,sy,54,t,warm?['#fffbe8','#ffd36a','#e8862a']:['#ffffff','#cfe0ff','#7a90e0'],.8)});
  const b1=sky[Math.min(1,sky.length-1)],b2=sky[Math.min(2,sky.length-1)],b3=sky[sky.length-1];
  layer(.1,()=>cloudlets(sd+3,5,40,170,CC(mix(b2,b3,.5)),t,.9));
  layer(.14,()=>deck(sd,S.y1??150,240,S.c1||CC(shd(b3,.95)),t,14,30,58));
  layer(.34,()=>deck(sd+5,S.y2??300,280,S.c2||CC(mix(b2,b3,.35)),t,24,42,84));
  layer(.7,()=>deck(sd+9,S.y3??470,320,S.c3||CC(mix(shd(b2,.72),b1,.25)),t,40,56,118));
  dust(t,22,5,'255,240,210',.4,4)},
 vista(S,t){const P=S.sky||['#1a2a6a','#6a7ab8','#f0a080','#ffe0a8'];skyG(P,-300,H+300);const sx=S.sx??CX*1.2,sy=S.sy??330,sd=S.seed||7;
  glow(sx,sy,S.sr||400,S.sun||'255,214,150',.4);layer(.06,()=>{if(S.stars||lum(P[0])<.12)stars(t,70,sd,240);sunburst(sx,sy,42,t,['#fffbea','#ffd070','#e8802a'],.75)});
  layer(.1,()=>cloudlets(sd+7,4,60,200,{light:mix(P[2],'#ffffff',.45),mid:mix(P[1],P[2],.6)},t,1));
  layer(.13,()=>deck(sd,S.cy??170,180,S.cl||{light:mix(P[3],'#ffffff',.4),mid:mix(P[2],P[3],.5),dark:mix(P[1],P[2],.5)},t,12,24,46));
  const rc=S.ridge||['#7a86b4','#5a6a98','#3c4a78','#26305a'];
  rc.forEach((col,i)=>{const par=[.18,.32,.52,.78][i];layer(par,()=>{const base=300+i*70+(S.horizon||0),amp=[120,100,80,60][i]+(S.rough||0);
    const pts=ridgeP(base,amp,.0042*(i+1),sd*13+i*29,col,par,`rgba(${S.haze||'255,220,190'},${.5-i*.1})`);
    skyG(['rgba(255,236,210,0)',`rgba(${S.haze||'255,220,190'},${.18-i*.035})`],base-120,base+160);
    if(i===2&&!S.trees){const r=rng(sd+i);for(let k=0;k<7;k++){const x=r()*(W+200)-100,p=pts[Math.max(0,Math.min(pts.length-1,Math.round((x+520)/46)))];ptree(x,p[1]+10,46+r()*30,t,k,[shd(col,1.3),shd(col,1.05)],shd(col,.6))}}})});
  if(S.river)layer(.6,()=>{cutP(()=>{ctx.moveTo(CX-30,380);ctx.bezierCurveTo(CX-260,470,CX+240,520,CX-120,H+200);ctx.lineTo(CX+260,H+200);ctx.bezierCurveTo(CX+420,520,CX-30,470,CX+30,380);ctx.closePath()},vg(380,H,[mix(S.river,'#ffffff',.35),S.river]),{sh:0,lw:1.6,ink:'rgba(255,255,255,.35)'});
    ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=2;ctx.lineCap='round';for(let i=0;i<12;i++){ctx.beginPath();ctx.moveTo(CX-70+i*10+Math.sin(t+i)*30,420+i*26);ctx.lineTo(CX-30+i*14+Math.sin(t+i)*30,420+i*26);ctx.stroke()}});
  if(S.ground)layer(.9,()=>{cutP(()=>{ctx.moveTo(-400,H-150);ctx.bezierCurveTo(200,H-190,700,H-120,1700,H-170);ctx.lineTo(1700,H+300);ctx.lineTo(-400,H+300);ctx.closePath()},vg(H-170,H+300,S.ground),{blur:10});
    const r=rng(41);ctx.fillStyle=S.blade||'#1c3a24';for(let i=0;i<60;i++){const x=r()*W,h=14+r()*28;ctx.beginPath();ctx.moveTo(x-5,H-118);ctx.lineTo(x+Math.sin(t*1.5+i)*4,H-118-h);ctx.lineTo(x+5,H-118);ctx.fill()}});
  if(S.trees)layer(.85,()=>{const r=rng(S.seed||9);S.trees.forEach((tx,i)=>ptree(tx,H-70,200+r()*90,t,i,S.leaf||['#1e4a30','#2a6a3c'],S.trunk))});
  dust(t,S.dust??26,11,S.dustc||'255,230,190',.4,5)},
 plain(S,t){const c=S.cols||['#0a0610','#1c1020'],top=c[0],bot=c[c.length-1];skyG(c,-300,H+300);const m=hx(bot),lit=`${Math.min(255,m[0]*3+40)|0},${Math.min(255,m[1]*3+30)|0},${Math.min(255,m[2]*3+44)|0}`;
  glow(CX,330,560,lit,.26);
  layer(.12,()=>{paperMandala(CX,340,t,mix(bot,top,.3),4,.015,.42);mandala(CX,340,t,'242,193,78',.08,4,.02)});
  // cut-paper vignette arcs in the corners give the empty plain a frame and depth
  layer(.3,()=>{[[-60,-40,380],[W+60,-40,380],[-80,H+60,420],[W+80,H+60,420]].forEach(([x,y,r],i)=>cutP(()=>{ctx.arc(x,y,r,0,TAU)},vg(y-r,y+r,[shd(top,.9),shd(top,.55)]),{blur:14,sy:0,lw:1.6,ink:'rgba(255,220,160,.14)'}));
    ctx.strokeStyle='rgba(242,193,78,.18)';ctx.lineWidth=1.6;ctx.setLineDash([2,8]);[[-60,-40,350],[W+60,-40,350],[-80,H+60,390],[W+80,H+60,390]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.stroke()});ctx.setLineDash([])});
  dust(t,26,7,'255,225,170',.35,3)},
 cosmos(S,t){const rgb=S.rgb||'160,120,255',col=hex(rgb.split(',').map(Number));skyG(['#04030c',mix('#120c2e',col,.12),mix('#2a1a52',col,.22)],-300,H+300);glow(CX,360,540,rgb,.24);stars(t,170,3,H);
  // nebula ribbons: translucent cut bands
  layer(.08,()=>{const r=rng(31);for(let k=0;k<3;k++){const y0=140+k*170+r()*40;ctx.save();ctx.globalAlpha=.28-k*.05;cutP(()=>{ctx.moveTo(-300,y0);for(let x=-300;x<=W+300;x+=60)ctx.lineTo(x,y0+Math.sin(x*.004+k*2+t*.05)*60);for(let x=W+300;x>=-300;x-=60)ctx.lineTo(x,y0+70+Math.sin(x*.005+k*3)*50);ctx.closePath()},vg(y0-60,y0+130,[mix(col,'#ffffff',.35),col,mix(col,'#000000',.5)]),{sh:0,lw:1.2,ink:'rgba(255,255,255,.25)'});ctx.restore()}});
  layer(.12,()=>{paperMandala(CX,330,t,mix('#140e2a',col,.18),4,S.spin||.03,.32);mandala(CX,330,t,rgb,.22,4,S.spin||.03)});
  layer(.2,()=>{const r=rng(9);for(let i=0;i<6;i++){const a=r()*TAU+t*(S.spin||.03)*2,rad=180+r()*280,x=CX+Math.cos(a)*rad*1.4,y=340+Math.sin(a)*rad*.6,pr=8+r()*14,pc=[mix(col,'#ffffff',.5),mix('#e8a060',col,.4),mix('#60a0e8',col,.4)][i%3];
    cutP(()=>ctx.arc(x,y,pr,0,TAU),(()=>{const g=ctx.createRadialGradient(x-pr*.4,y-pr*.4,1,x,y,pr);g.addColorStop(0,'#ffffff');g.addColorStop(.35,pc);g.addColorStop(1,shd(pc,.4));return g})(),{blur:8,lw:1.4});
    if(i%2===0){ctx.save();ctx.translate(x,y);ctx.scale(1,.32);ctx.strokeStyle='rgba(255,240,210,.55)';ctx.lineWidth=2.4;ctx.beginPath();ctx.arc(0,0,pr*1.8,0,TAU);ctx.stroke();ctx.restore()}}});
  glow(CX,340,180,'255,230,170',.14);dust(t,26,5,'255,230,190',.35,4)},
 storm(S,t){const r=S.r??1;const col=(a,b)=>hex(hx(a).map((v,i)=>v+(hx(b)[i]-v)*r));skyG([col('#0a0e1c','#08020a'),col('#1c2236','#2a0810'),col('#3a3a52','#6a1612'),col('#7a5a5a','#d0482a')],-300,H+300);
  glow(CX,520,640,'255,90,40',.38*r);
  layer(.08,()=>{const fl=Math.max(0,Math.sin(t*5.3)*Math.sin(t*2.1));const bolt=(x0,seed,a)=>{const q=rng(seed);let x=x0,y=-20;const pts=[[x,y]];while(y<300){x+=(q()-.5)*70;y+=40+q()*30;pts.push([x,y])}
      ctx.save();ctx.globalAlpha=a;cutP(()=>{pts.forEach((p,i)=>i?ctx.lineTo(p[0]-4,p[1]):ctx.moveTo(p[0]-4,p[1]));for(let i=pts.length-1;i>=0;i--)ctx.lineTo(pts[i][0]+4+(i===pts.length-1?-4:0),pts[i][1])},'#fff4e0',{sh:0,lw:1.6,ink:'rgba(255,150,80,.8)'});ctx.restore();glow(pts[1][0],pts[1][1],160,'255,200,170',.25*a)};
    bolt(260,7,.55+.45*fl);bolt(1010,13,.4+.6*fl)});
  layer(.12,()=>deck(51,70,240,CC(col('#2c3250','#5a1814')),t,18,30,62));layer(.3,()=>deck(61,240,280,CC(col('#3a4062','#7a2218')),t,30,44,90));layer(.62,()=>deck(71,450,320,CC(col('#202640','#400c0c')),t,44,58,120));
  layer(.9,()=>{ctx.strokeStyle=`rgba(${r>.5?'255,180,150':'200,210,240'},.18)`;ctx.lineWidth=1.4;const q=rng(5);for(let i=0;i<70;i++){const x=mod(q()*W*1.3+t*120,W+200)-100,y=mod(q()*H+t*420,H+100)-50;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-8,y+26);ctx.stroke()}});
  const fl=Math.max(0,Math.sin(t*5.3)*Math.sin(t*2.1));if(fl>.55)glow(CX*.8,200,500,'255,220,200',.3*(fl-.5));embers(t,36,3,'255,120,50',1.2*r)},
 sea(S,t){skyG(['#04122e','#0a2a5a','#16407e'],-300,H+300);stars(t,70,4,240);moonAt(W*.78,120,30,t);glow(CX,220,420,'120,170,255',.2);
  layer(.12,()=>deck(17,210,120,{light:'#3a5a9a',mid:'#24427a',dark:'#142a56'},t,10,20,40));
  layer(.4,()=>waves(300,7,['#123c78','#16488c','#1c5aa6','#2470bc'],t,12,true))},
 voidR(S,t){skyG(S.cols||['#050204','#1c0408','#4a0c0c'],-300,H+300);glow(S.gx||CX,S.gy||340,520,S.rgb||'255,60,30',.42);layer(.12,()=>paperMandala(S.gx||CX,S.gy||340,t,'#2a0608',4,-.03,.4));mandala(S.gx||CX,S.gy||340,t,'255,90,60',.2,5,-.04);embers(t,60,3,'255,110,40',2)},
 amber(S,t){skyG(['#2a1808','#6a3a12','#b8701e','#e8a850'],-300,H+300);glow(CX,450,520,'255,190,110',.34);layer(.06,()=>{rays(CX,400,t,'255,220,150',.05,14,1400);sunburst(CX,400,64,t,['#fffbea','#ffd070','#e8802a'],.8)});
  layer(.12,()=>cloudlets(19,5,60,200,{light:'#f6d8a0',mid:'#d8a060'},t,1));
  layer(.22,()=>deck(19,250,240,{light:'#f0c880',mid:'#c88a40',dark:'#7a4a18'},t,16,30,64));layer(.4,()=>deck(29,380,260,{light:'#d8a060',mid:'#a86a2a',dark:'#5a3410'},t,24,40,86));
  layer(.6,()=>cutP(()=>{ctx.moveTo(-300,610);ctx.bezierCurveTo(300,570,800,640,1600,590);ctx.lineTo(1600,H+300);ctx.lineTo(-300,H+300);ctx.closePath()},vg(590,H+300,['#6a4220','#1a0c04']),{blur:10}));dust(t,40,83,'255,220,150',.45,6)},
 dusk(S,t){skyG(['#1a1440','#4a3070','#c8625a','#f0a070'],-300,H+300);glow(CX,470,500,'255,190,130',.4);layer(.06,()=>{stars(t,40,23,160);sunburst(CX,440,56,t,['#fffbea','#ffc46a','#e0602a'],.85)});
  layer(.1,()=>cloudlets(29,5,50,200,{light:'#f0b0a0',mid:'#a86a8a'},t,1));layer(.2,()=>deck(23,250,200,{light:'#f0a888',mid:'#b86a7a',dark:'#5a3a6a'},t,16,28,58));layer(.32,()=>deck(43,330,200,{light:'#d88a80',mid:'#94566e',dark:'#4a2e5a'},t,22,34,70));
  layer(.6,()=>waves(500,5,['#3a3a82','#2e2e70','#242460','#1a1a4c'],t,9,true));dust(t,34,23,'255,200,150',.4,4)},
 earth(S,t){const st=S.strata||['#5a3a24','#42281a','#2c1a12','#1a0e0a'],r=rng(17);skyG(st,-300,H+300);
  layer(.3,()=>{for(let k=0;k<5;k++){const y=80+k*150;cutP(()=>{ctx.moveTo(-400,y);for(let x=-400;x<=W+500;x+=60)ctx.lineTo(x,y+Math.sin(x*.01+k*2)*22+r()*8);ctx.lineTo(W+500,y+170);ctx.lineTo(-400,y+170);ctx.closePath()},vg(y-20,y+170,[shd(st[k%st.length],1.15),st[k%st.length],shd(st[k%st.length],.75)]),{blur:6,lw:1.8});
    ctx.fillStyle='rgba(255,220,170,.08)';for(let i=0;i<30;i++){ctx.beginPath();ctx.arc(r()*W,y+20+r()*120,1+r()*3,0,TAU);ctx.fill()}}});
  layer(.55,()=>{ctx.lineCap='round';for(let i=0;i<8;i++){let x=r()*W,y=-40;const pts=[[x,y]];for(let k=0;k<7;k++){x+=(r()-.5)*70;y+=70+r()*30;pts.push([x,y])}ctx.strokeStyle='rgba(20,8,4,.6)';ctx.lineWidth=9;ctx.beginPath();pts.forEach((p,j)=>j?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.strokeStyle='#8a5a32';ctx.lineWidth=5;ctx.stroke();ctx.strokeStyle='rgba(255,210,160,.3)';ctx.lineWidth=1.6;ctx.stroke()}});
  layer(.75,()=>{for(let i=0;i<10;i++){const x=r()*W,y=140+r()*500,s=18+r()*40;cutP(()=>{ctx.moveTo(x-s,y+s*.4);ctx.lineTo(x-s*.4,y-s*.6);ctx.lineTo(x+s*.7,y-s*.3);ctx.lineTo(x+s,y+s*.5);ctx.closePath()},vg(y-s,y+s,['#9a8a80','#5a4a44']),{blur:5,lw:1.6});
    cutP(()=>{ctx.moveTo(x-s*.4,y-s*.6);ctx.lineTo(x+s*.7,y-s*.3);ctx.lineTo(x+s*.2,y);ctx.closePath()},'rgba(255,240,220,.18)',{sh:0,lw:0})}});
  glow(S.gx??CX,S.gy??520,400,S.gc||'255,150,60',.36);dust(t,34,9,'255,170,90',.45,-6)},
 pillar(S,t){skyG(S.sky||['#05030c','#0e0a26','#2a1236'],-300,H+300);stars(t,110,5,H);const x=S.px??CX,hw=S.pw??110,ck=S.ct!=null?clamp((t-S.ct)/1.2):0;
  layer(.1,()=>{paperMandala(x,H/2,t,'#1a0e2a',4,.02,.4);mandala(x,H/2,t,'242,160,70',.12,5,.025)});glow(x,H/2,700,'255,150,60',.32);
  layer(.25,()=>{deck(83,560,200,{light:'#4a2a4a',mid:'#2a1830',dark:'#140a1a'},t,14,30,64);ctx.save();ctx.translate(0,H);ctx.scale(1,-1);deck(97,H-150,200,{light:'#3a2040',mid:'#22142c',dark:'#100816'},t,14,28,58);ctx.restore()});
  layer(.4,()=>{ctx.save();ctx.beginPath();ctx.rect(x-hw,-600,hw*2,H+1200);const g=ctx.createLinearGradient(x-hw,0,x+hw,0);g.addColorStop(0,'#a8300c');g.addColorStop(.28,'#ff9a30');g.addColorStop(.5,'#fff3c0');g.addColorStop(.72,'#ff9a30');g.addColorStop(1,'#a8300c');
    ctx.shadowColor='rgba(255,130,30,.55)';ctx.shadowBlur=34*SC_;ctx.fillStyle=g;ctx.fill();ctx.shadowBlur=0;ctx.lineWidth=3;ctx.strokeStyle='rgba(60,10,0,.75)';ctx.stroke();ctx.restore();
    ctx.save();ctx.beginPath();ctx.rect(x-hw,-600,hw*2,H+1200);ctx.clip();for(let i=0;i<14;i++){const yy=((i*97+t*60)%(H+500))-250;cutP(()=>{ctx.moveTo(x-hw,yy);ctx.quadraticCurveTo(x-hw*.2,yy-30,x,yy-70);ctx.quadraticCurveTo(x+hw*.2,yy-30,x+hw,yy);ctx.quadraticCurveTo(x,yy+24,x-hw,yy)},'rgba(255,225,130,.35)',{sh:0,lw:1.2,ink:'rgba(150,50,0,.4)'})}
      ctx.strokeStyle='rgba(255,250,220,.5)';ctx.lineWidth=2;ctx.setLineDash([2,9]);[-.55,.55].forEach(f=>{ctx.beginPath();ctx.moveTo(x+hw*f,-600);ctx.lineTo(x+hw*f,H+600);ctx.stroke()});ctx.setLineDash([]);ctx.restore();
    [-1,1].forEach(sd=>{for(let i=0;i<11;i++){const yy=((i*98+t*40)%(H+300))-150,L=50+((i*37)%30);cutP(()=>{ctx.moveTo(x+sd*hw,yy+10);ctx.quadraticCurveTo(x+sd*(hw+L*.6),yy-L*.3,x+sd*(hw+L*.25),yy-L);ctx.quadraticCurveTo(x+sd*(hw+8),yy-L*.4,x+sd*hw,yy-10)},i%2?'#ff8a28':'#ffb84a',{sh:0,lw:1.3,ink:'rgba(110,30,0,.6)'})}});
    if(ck>0){const cw=hw*1.7*ck;ctx.save();ctx.beginPath();ctx.moveTo(x,-500);ctx.lineTo(x+cw*.5,H/2);ctx.lineTo(x,H+500);ctx.lineTo(x-cw*.5,H/2);ctx.closePath();ctx.clip();const cg=ctx.createRadialGradient(x,H/2,10,x,H/2,hw*2);cg.addColorStop(0,'#fff0c0');cg.addColorStop(1,'#a01808');ctx.fillStyle=cg;ctx.fillRect(x-hw*2,-500,hw*4,H+1000);ctx.restore()}});
  dust(t,50,13,'255,200,110',.6,-14)},
 kailash(S,t){skyG(['#03051a','#0c1446','#2a3a80','#7a6aa8'],-300,H+300);stars(t,120,21,300);moonAt(W*(S.mx==null?.22:S.mx),150,38,t);
  layer(.1,()=>cloudlets(61,4,80,200,{light:'#8a90c8',mid:'#5a6098'},t,1));
  layer(.15,()=>peaks([[-500,420],[-200,340],[0,390],[200,300],[420,380],[640,160],[860,380],[1060,290],[1260,370],[1600,320],[1800,400]],vg(160,560,['#b6c2ea','#6670ae','#2e3468']),'#f6f8ff','rgba(230,236,255,.6)'));
  layer(.24,()=>deck(71,430,160,{light:'#9aa4d8',mid:'#6a74b0',dark:'#3a4280'},t,10,24,48));
  layer(.32,()=>peaks([[-500,500],[-100,420],[150,480],[380,410],[560,500],[760,470],[980,400],[1200,470],[1800,430]],vg(400,700,['#46508e','#1e2350']),'#dfe6fa','rgba(200,210,250,.45)'));
  layer(.55,()=>peaks([[-500,620],[-80,560],[200,600],[420,640],[860,640],[1080,580],[1800,620]],vg(560,760,['#2c2f5e','#14163a']),null));dust(t,40,7,'220,230,255',.45,3)},
 palace(S,t){const o=S.po||{};skyG(o.wall||['#3a1e2a','#1e1018'],-300,H+300);
  // back wall: three cusped arches open onto a starry sky, carved frieze, hanging lamps
  layer(.5,()=>{const xs=[CX-410,CX,CX+410];xs.forEach((x,i)=>{const arch=()=>{ctx.moveTo(x-118,560);ctx.lineTo(x-118,270);for(let k=0;k<5;k++){const a0=PI+k/5*PI,a1=PI+(k+1)/5*PI,am=(a0+a1)/2;ctx.quadraticCurveTo(x+Math.cos(am)*150,250+Math.sin(am)*150,x+Math.cos(a1)*118,270+Math.sin(a1)*130)}ctx.lineTo(x+118,560);ctx.closePath()};
      ctx.save();ctx.beginPath();arch();ctx.clip();skyG(o.win||['#0a1236','#2a3a7a','#7a5a8a'],110,560);const r=rng(i+3);for(let k=0;k<30;k++){ctx.fillStyle=`rgba(255,250,235,${.3+.5*Math.abs(Math.sin(t*1.2+k))})`;ctx.beginPath();ctx.arc(x-110+r()*220,130+r()*260,.6+r()*1.2,0,TAU);ctx.fill()}
      moonAt(x+40,210,i===1?20:12,t);ctx.restore();
      cutP(arch,'rgba(0,0,0,0)',{sh:0,lw:8,ink:'#c9a24a'});cutP(arch,'rgba(0,0,0,0)',{sh:0,lw:2,ink:'rgba(255,236,170,.5)'})});
    cutP(()=>ctx.rect(-300,96,W+600,40),vg(96,136,['#d8b060','#8a6424']),{blur:8,lw:2});for(let x=-300;x<W+300;x+=34){cutP(()=>{ctx.moveTo(x,136);ctx.quadraticCurveTo(x+17,160,x+34,136)},'#b88a3a',{sh:0,lw:1.4})}
    for(let x=-280;x<W+300;x+=68){ctx.fillStyle='#7a1a2a';ctx.beginPath();ctx.arc(x,116,6,0,TAU);ctx.fill();ctx.fillStyle='#e8c060';ctx.beginPath();ctx.arc(x,116,2.4,0,TAU);ctx.fill()}
    // toran garland across the top
    for(let i=0;i<30;i++){const u=i/29,x=-200+u*(W+400),y=150+Math.sin(u*PI*6)*14+18;cutP(()=>{ctx.moveTo(x,y-10);ctx.quadraticCurveTo(x+10,y,x,y+14);ctx.quadraticCurveTo(x-10,y,x,y-10)},i%2?'#2a8a4a':'#f2a020',{sh:0,lw:1})}});
  // pillars with capitals and bases, lamps hanging between them
  layer(.62,()=>{[CX-205,CX+205,CX-615,CX+615].forEach(x=>{const g=ctx.createLinearGradient(x-26,0,x+26,0);g.addColorStop(0,'#8a6430');g.addColorStop(.35,'#f0d48c');g.addColorStop(.6,'#d8b060');g.addColorStop(1,'#6a4a20');
      cutP(()=>ctx.rect(x-24,170,48,400),g,{blur:10,lw:2});for(let y=200;y<560;y+=60){ctx.strokeStyle='rgba(90,50,10,.45)';ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(x-24,y);ctx.lineTo(x+24,y);ctx.stroke()}
      [-10,0,10].forEach(dx=>{ctx.strokeStyle='rgba(90,50,10,.3)';ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(x+dx,176);ctx.lineTo(x+dx,560);ctx.stroke()});
      cutP(()=>{ctx.moveTo(x-40,170);ctx.lineTo(x+40,170);ctx.lineTo(x+30,150);ctx.quadraticCurveTo(x,136,x-30,150);ctx.closePath()},vg(136,170,['#f6dc96','#a87a30']),{blur:6,lw:2});
      cutP(()=>{ctx.moveTo(x-36,560);ctx.lineTo(x+36,560);ctx.lineTo(x+42,584);ctx.lineTo(x-42,584);ctx.closePath()},vg(560,584,['#e8c878','#8a6428']),{blur:6,lw:2})});
    [CX-410,CX,CX+410].forEach((x,i)=>{const y=236+Math.sin(t*1.1+i)*3;ctx.strokeStyle='rgba(60,30,10,.8)';ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(x,136);ctx.lineTo(x,y-12);ctx.stroke();glow(x,y+6,80,'255,190,100',.35);
      cutP(()=>{ctx.moveTo(x-16,y-10);ctx.lineTo(x+16,y-10);ctx.quadraticCurveTo(x+14,y+12,x,y+16);ctx.quadraticCurveTo(x-14,y+12,x-16,y-10)},vg(y-10,y+16,['#f2c860','#8a5a1a']),{sh:0,lw:1.4});
      cutP(()=>{ctx.moveTo(x,y-26-Math.sin(t*9+i)*2);ctx.quadraticCurveTo(x+6,y-14,x,y-10);ctx.quadraticCurveTo(x-6,y-14,x,y-26-Math.sin(t*9+i)*2)},'#ffd35a',{sh:0,lw:1,ink:'rgba(200,80,0,.7)'})})});
  // floor: tiled paper with perspective lines and a carpet runner
  layer(.8,()=>{cutP(()=>ctx.rect(-400,575,W+800,H),vg(575,H+100,['#5a3020','#1a0c08']),{blur:12,lw:2});ctx.strokeStyle='rgba(255,210,150,.12)';ctx.lineWidth=1.4;for(let k=-12;k<=12;k++){ctx.beginPath();ctx.moveTo(CX+k*60,575);ctx.lineTo(CX+k*160,H+60);ctx.stroke()}for(let y=600;y<H+60;y+=(y-560)*.35){ctx.beginPath();ctx.moveTo(-400,y);ctx.lineTo(W+400,y);ctx.stroke()}
    cutP(()=>{ctx.moveTo(CX-80,575);ctx.lineTo(CX+80,575);ctx.lineTo(CX+220,H+60);ctx.lineTo(CX-220,H+60);ctx.closePath()},vg(575,H,['#8a1a24','#4a0a10']),{sh:0,lw:1.6});ctx.strokeStyle='#e0b04a';ctx.lineWidth=3;[[-70,-200],[70,200]].forEach(([a,b])=>{ctx.beginPath();ctx.moveTo(CX+a,577);ctx.lineTo(CX+b,H+60);ctx.stroke()})});
  glow(CX,420,480,o.glow||'255,190,120',.12);dust(t,30,31,'255,230,170',.35,3)}
});
})();
