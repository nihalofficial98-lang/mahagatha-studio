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
function blob(P,yb,pad){P.forEach(([x,y,r])=>{ctx.moveTo(x+r+pad,y);ctx.arc(x,y,r+pad,0,TAU)});const x0=P[0][0]-P[0][2],x1=P[P.length-1][0]+P[P.length-1][2];P.forEach(([x,y,r])=>ctx.rect(x-r*.98-pad,y,2*r*.98+2*pad,yb-y+pad));const yr=Math.max(...P.map(p=>p[1]+p[2]));ctx.rect(x0-pad,yr,x1-x0+2*pad,yb-yr+pad)}
function deck(seed,y,h,C,t,drift,rmin,rmax){const dx=Math.sin(t*.12+seed)*drift;ctx.save();ctx.translate(dx,0);
  const P=puffs(seed,y,rmin,rmax,-380,W+420,h*.12),yb=y+h+400;
  // ink edge + shadow (stroke pass), then the fill hides every inner seam
  ctx.save();ctx.beginPath();blob(P,yb,0);ctx.shadowColor='rgba(10,2,24,.34)';ctx.shadowBlur=11*SC_;ctx.shadowOffsetY=7*SC_;ctx.strokeStyle='rgba(24,8,34,.42)';ctx.lineWidth=4;ctx.lineJoin='round';ctx.stroke();ctx.fillStyle=C.dark;ctx.fill();ctx.restore();
  ctx.beginPath();blob(P,yb,0);ctx.fillStyle=vg(y-rmax*1.2,y+h,[C.light,C.mid,C.dark]);ctx.fill();
  ctx.save();ctx.beginPath();blob(P,yb,0);ctx.clip();
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

/* ---- paper-cut overrides for the shared effects: name plate, shock ring, flames, lotus ---- */
pill=function(s,x,y,a,col,size){col=col||'#ffe9b8';size=size||32;if(a<=0.01)return;ctx.save();ctx.globalAlpha*=clamp(a);ctx.font=`700 ${size}px NSer, serif`;const w=ctx.measureText(s).width+56,h=size*1.6,cx=clamp(x,70+w/2,W-70-w/2),cy=clamp(y,60,H-130);
  const plate=()=>{ctx.moveTo(cx-w/2,cy);ctx.lineTo(cx-w/2+h*.35,cy-h/2);ctx.lineTo(cx+w/2-h*.35,cy-h/2);ctx.lineTo(cx+w/2,cy);ctx.lineTo(cx+w/2-h*.35,cy+h/2);ctx.lineTo(cx-w/2+h*.35,cy+h/2);ctx.closePath()};
  cutP(plate,vg(cy-h/2,cy+h/2,['#3a1a2a','#1a0c1c']),{blur:8,sy:4,lw:3,ink:'#e0b04a'});ctx.save();ctx.beginPath();plate();ctx.clip();ctx.strokeStyle='rgba(255,230,170,.35)';ctx.lineWidth=1.4;ctx.setLineDash([2,6]);ctx.strokeRect(cx-w/2+10,cy-h/2+6,w-20,h-12);ctx.setLineDash([]);ctx.restore();
  [-1,1].forEach(sd=>{ctx.fillStyle='#e0b04a';ctx.beginPath();ctx.arc(cx+sd*(w/2-h*.2),cy,3.4,0,TAU);ctx.fill()});ctx.restore();stext(s,cx,cy+1,size,col,a,700,'center','rgba(255,210,140,.35)')};
shockF=function(x,y,u,rgb,max,sq){max=max||900;sq=sq||.5;if(u<0||u>1)return;ctx.save();ctx.translate(x,y);ctx.scale(1,sq);const R=u*max,al=1-u;ctx.globalAlpha*=al;
  ctx.strokeStyle='rgba(24,8,34,.6)';ctx.lineWidth=12*(1-u)+5;ctx.beginPath();ctx.arc(0,0,R,0,TAU);ctx.stroke();ctx.strokeStyle=`rgb(${rgb})`;ctx.lineWidth=9*(1-u)+2;ctx.stroke();
  const n=24;for(let i=0;i<n;i++){ctx.save();ctx.rotate(i/n*TAU+u);cutP(()=>{ctx.moveTo(-8,-R);ctx.quadraticCurveTo(0,-R-26*(1-u)-6,8,-R);ctx.closePath()},`rgb(${rgb})`,{sh:0,lw:1.2});ctx.restore()}ctx.restore()};
flamesF=function(x,y,s,t,n,c1,c2){n=n||8;c1=c1||'#ff5a1a';c2=c2||'#ffc24a';ctx.save();ctx.translate(x,y);ctx.scale(s,s);glow(0,-50,140,'255,140,50',.35);for(let i=0;i<n;i++){const ph=i*1.7,h=90+Math.sin(t*6+ph)*24+(i%3)*16,w=24,xx=(i-(n-1)/2)*22;
  [[c1,1,'#ff3a10'],[c2,.55,'#fff0a0']].forEach(([c,k,c3])=>cutP(()=>{ctx.moveTo(xx-w*k,0);ctx.quadraticCurveTo(xx-w*.8*k+Math.sin(t*7+ph)*8,-h*.6*k,xx+Math.sin(t*5+ph)*10,-h*k);ctx.quadraticCurveTo(xx+w*.8*k+Math.sin(t*7+ph)*8,-h*.6*k,xx+w*k,0);ctx.closePath()},vg(-h*k,0,[c3,c]),{sh:0,lw:1.4,ink:'rgba(110,20,0,.6)'}))}ctx.restore()};
const inkWrap=f0=>function(){ctx.save();ctx.shadowColor='rgba(30,13,36,.85)';ctx.shadowBlur=2.6*SC_;ctx.shadowOffsetY=1.2*SC_;f0.apply(null,arguments);ctx.restore()};
drawSwan=inkWrap(drawSwan);drawBoar=inkWrap(drawBoar);
lotus=function(x,y,s,t,open,a){open=open==null?1:open;ctx.save();ctx.globalAlpha*=a==null?1:a;V2.PK.setDPR(SC_);V2.PK.padma(ctx,x,y,s*2.2,Math.max(.05,open),t);ctx.restore()};

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
    if(i<2)ctx.filter=`blur(${((2-i)*1.1*SC_).toFixed(2)}px)`;const pts=ridgeP(base,amp,.0042*(i+1),sd*13+i*29,i<2?mix(col,'#dcd8f0',.35-i*.15):col,par,`rgba(${S.haze||'255,220,190'},${.5-i*.1})`);ctx.filter='none';
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
  layer(.4,()=>waves(300,13,['#123c78','#16488c','#1c5aa6','#2470bc','#1a5098'],t,12,true))},
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
// reels: Vaikuntha, Vishnu's abode: golden light, white cloud banks, a far golden palace with domes, the ocean of milk with lotuses
BG.vaikuntha=function(S,t){skyG(['#fff4d8','#ffe2a0','#f6c070','#f0a858'],-300,H+300);const sx=S.sx??CX,sy=S.sy??250;glow(sx,sy,600,'255,240,190',.5);
  layer(.05,()=>{rays(sx,sy,t,'255,245,210',.08,16,1500);sunburst(sx,sy,58,t,['#fffef4','#ffe88a','#f2b040'],.7)});
  layer(.1,()=>cloudlets(31,6,50,200,{light:'#ffffff',mid:'#f8ead0'},t,1));
  layer(.18,()=>{const base=372,gold=vg(170,base,['#fff2b8','#f2c14e','#b87a1a']);
    [[sx-260,70,120],[sx+260,70,120],[sx-130,95,170],[sx+130,95,170],[sx,130,230]].forEach(([x,w,h])=>{cutP(()=>ctx.rect(x-w/2,base-h,w,h),gold,{blur:6,lw:1.8,ink:'rgba(120,70,10,.6)'});
      cutP(()=>{ctx.moveTo(x-w*.55,base-h);ctx.quadraticCurveTo(x-w*.5,base-h-w*.75,x,base-h-w*.95);ctx.quadraticCurveTo(x+w*.5,base-h-w*.75,x+w*.55,base-h);ctx.closePath()},gold,{blur:6,lw:1.8,ink:'rgba(120,70,10,.6)'});
      cutP(()=>{ctx.moveTo(x-3,base-h-w*.95);ctx.lineTo(x,base-h-w*.95-26);ctx.lineTo(x+3,base-h-w*.95);ctx.closePath()},'#fff2b8',{sh:0,lw:1});
      for(let k=0;k<3;k++){const ax=x-w*.3+k*w*.3;cutP(()=>{ctx.moveTo(ax-8,base-8);ctx.lineTo(ax-8,base-h*.45);ctx.quadraticCurveTo(ax,base-h*.6,ax+8,base-h*.45);ctx.lineTo(ax+8,base-8);ctx.closePath()},'rgba(150,90,20,.55)',{sh:0,lw:0})}})});
  layer(.3,()=>deck(33,S.y1??350,220,{light:'#ffffff',mid:'#f6ecd8',dark:'#cdbb98'},t,14,30,62));
  layer(.55,()=>{const y0=S.sea??560;cutP(()=>{ctx.moveTo(-300,y0);for(let x=-300;x<=W+300;x+=40)ctx.quadraticCurveTo(x+10,y0-6+Math.sin(x*.02+t)*3,x+20,y0);ctx.lineTo(W+300,H+300);ctx.lineTo(-300,H+300);ctx.closePath()},vg(y0,H+60,['#fffcf2','#f2e8d6','#d8c8aa']),{blur:8,lw:2,ink:'rgba(150,120,80,.5)'});
    for(let k=0;k<6;k++){const yy=y0+20+k*24,off=(t*12*(1+k*.3))%80;ctx.strokeStyle='rgba(200,180,140,.35)';ctx.lineWidth=2;ctx.beginPath();for(let x=-300-off;x<W+300;x+=80){ctx.moveTo(x,yy);ctx.quadraticCurveTo(x+20,yy-5,x+40,yy)}ctx.stroke()}
    [[110,600,.7],[300,640,.55],[1000,610,.65],[1180,650,.75],[640,690,.5]].forEach(([x,y,s2])=>{cutP(()=>ctx.ellipse(x+20*s2,y+8*s2,46*s2,12*s2,0,0,TAU),'#5a9a4a',{sh:0,lw:1.4,ink:'#2a5a2a'});V2.PK.padma(ctx,x,y,s2,1,t)})});
  dust(t,30,9,'255,245,210',.5,4)};


/* ---- paper-cut OBJECTS with atmospheric perspective (owner rule: every scene has 2-3 depth layers).
   Every object: (x, y = base on the ground, s = scale, t, o) with o.fog 0..1 (mix toward o.haze), o.dark 0..1 (foreground
   silhouette), o.col (main colour). Far objects: fog .45-.7; mid: .15-.3; near: 0 with dark .3-.6 and a little blur. ---- */
// union cut: ink + shadow drawn first, fill second, so overlapping puffs read as ONE paper silhouette (no inner seams)
function cutU(fn,fill,o){o=o||{};ctx.save();ctx.beginPath();fn();ctx.shadowColor=o.shc||'rgba(10,2,24,.34)';ctx.shadowBlur=(o.blur==null?9:o.blur)*SC_;ctx.shadowOffsetY=(o.sy==null?5:o.sy)*SC_;
  ctx.lineWidth=(o.lw||2)*2;ctx.strokeStyle=o.ink||INK;ctx.lineJoin='round';if(o.lw!==0)ctx.stroke();ctx.fillStyle=fill;ctx.fill();ctx.restore();ctx.save();ctx.beginPath();fn();ctx.fillStyle=fill;ctx.fill();ctx.restore()}
const FOGC=(c,o)=>{let r=o.fog?mix(c,o.haze||'#d8d4ec',o.fog):c;if(o.dark)r=mix(r,o.darkc||'#140a1c',o.dark);return r};
const fogO=o=>({blur:(o.fog?4:9)*(1-(o.fog||0)*.6),sy:(o.fog?2:5),lw:o.fog>.5?1:1.8,ink:`rgba(24,8,34,${(.5*(1-(o.fog||0)*.8)).toFixed(3)})`,shc:`rgba(10,2,24,${(.34*(1-(o.fog||0))).toFixed(3)})`});
const OBJ={
 tree(x,y,s,t,o){const kind=o.kind||'round',lc=o.col||'#2f6a3c',tc=FOGC(o.trunk||'#4a2e1c',o),sw=Math.sin(t*.8+x*.01)*2*s,O=fogO(o);
  if(kind==='palm'){cutP(()=>{ctx.moveTo(x-6*s,y);ctx.quadraticCurveTo(x+14*s,y-120*s,x+sw+6*s,y-230*s);ctx.lineTo(x+sw+16*s,y-228*s);ctx.quadraticCurveTo(x+24*s,y-120*s,x+8*s,y);ctx.closePath()},vg(y-230*s,y,[shd(tc,1.3),tc]),O);
   const hx0=x+sw+11*s,hy0=y-230*s;for(let i=0;i<8;i++){const an=-PI/2+(i-3.5)*.42+(i<4?-.25:.25),L=(95+(i%2)*25)*s,ex=hx0+Math.cos(an)*L,ey=hy0+Math.sin(an)*L+Math.abs(Math.cos(an))*L*.45,nx=-Math.sin(an)*14*s,ny=Math.cos(an)*14*s,mx=(hx0+ex)/2,my=(hy0+ey)/2-10*s;
    cutP(()=>{ctx.moveTo(hx0,hy0);ctx.quadraticCurveTo(mx+nx,my+ny,ex,ey);ctx.quadraticCurveTo(mx-nx,my-ny,hx0,hy0);ctx.closePath()},FOGC(i%2?lc:shd(lc,1.2),o),O);
    ctx.strokeStyle=`rgba(20,40,20,${.4*(1-(o.fog||0))})`;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(hx0,hy0);ctx.quadraticCurveTo(mx,my,ex,ey);ctx.stroke()}
   cutP(()=>ctx.arc(hx0,hy0+4*s,9*s,0,TAU),FOGC('#6a4a2a',o),{sh:0,lw:1});return}
  if(kind==='pine'){cutP(()=>ctx.rect(x-6*s,y-40*s,12*s,40*s),tc,O);for(let k=0;k<4;k++){const yy=y-40*s-k*42*s,w=(70-k*14)*s;cutP(()=>{ctx.moveTo(x-w+sw*k*.3,yy);ctx.lineTo(x+sw*k*.5,yy-70*s);ctx.lineTo(x+w+sw*k*.3,yy);ctx.closePath()},vg(yy-70*s,yy,[FOGC(shd(lc,1.25),o),FOGC(shd(lc,.8),o)]),O)}return}
  // round / banyan: trunk with two branches, three to five layered crowns, banyan adds hanging roots
  const ban=kind==='banyan',H_=(ban?190:210)*s,cw=ban?1.5:1;
  cutP(()=>{ctx.moveTo(x-14*s*cw,y);ctx.quadraticCurveTo(x-6*s,y-H_*.4,x-30*s*cw,y-H_*.62);ctx.lineTo(x-18*s*cw,y-H_*.66);ctx.quadraticCurveTo(x,y-H_*.5,x+16*s*cw,y-H_*.7);ctx.lineTo(x+26*s*cw,y-H_*.64);ctx.quadraticCurveTo(x+8*s,y-H_*.4,x+14*s*cw,y);ctx.closePath()},vg(y-H_,y,[shd(tc,1.25),tc,shd(tc,.7)]),O);
  if(ban){ctx.save();ctx.strokeStyle=FOGC('#5a3a24',o);ctx.lineWidth=2.2*s;for(let i=0;i<9;i++){const rx=x+(i-4)*22*s;ctx.beginPath();ctx.moveTo(rx,y-H_*.72);ctx.quadraticCurveTo(rx+Math.sin(t+i)*3,y-H_*.35,rx+(i%3-1)*4,y-(i%2?0:H_*.15));ctx.stroke()}ctx.restore()}
  const C=[[0,-.86,.36],[-.32,-.72,.27],[.32,-.72,.27],[-.16,-.98,.22],[.18,-.96,.2]];
  C.forEach(([dx,dy,rr],k)=>{const cx=x+dx*H_*cw+sw,cy=y+dy*H_,R=rr*H_;const c0=FOGC(k%2?shd(lc,1.12):lc,o);
    cutU(()=>{for(let j=0;j<6;j++){const a=j/6*TAU+k;ctx.moveTo(cx+Math.cos(a)*R*.55+R*.55,cy+Math.sin(a)*R*.4);ctx.arc(cx+Math.cos(a)*R*.55,cy+Math.sin(a)*R*.4,R*.55,0,TAU)}},vg(cy-R,cy+R,[shd(c0,1.3),c0,shd(c0,.68)]),O)});
  if(!o.fog||o.fog<.4){ctx.fillStyle=`rgba(255,250,220,${.25*(1-(o.dark||0))})`;C.slice(0,3).forEach(([dx,dy,rr])=>{ctx.beginPath();ctx.arc(x+dx*H_*cw-rr*H_*.3+sw,y+dy*H_-rr*H_*.3,rr*H_*.18,0,TAU);ctx.fill()})}
  if(o.flowers){const r=rng(Math.round(x));for(let i=0;i<12;i++){ctx.fillStyle=FOGC(o.flowers,o);ctx.beginPath();ctx.arc(x+(r()-.5)*H_*.9*cw,y-H_*(.62+r()*.4),3.2*s,0,TAU);ctx.fill()}}},
 rock(x,y,s,t,o){const r=rng(o.seed||Math.round(x*7)),n=7,c=FOGC(o.col||'#8a7a74',o),P=[];for(let i=0;i<=n;i++){const a=PI+i/n*PI;P.push([x+Math.cos(a)*(60+r()*16)*s,y+Math.sin(a)*(46+r()*24)*s])}
  cutP(()=>{ctx.moveTo(x-64*s,y);P.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(x+64*s,y);ctx.closePath()},vg(y-70*s,y,[shd(c,1.25),c,shd(c,.65)]),fogO(o));
  cutP(()=>{ctx.moveTo(P[2][0],P[2][1]);ctx.lineTo(P[3][0],P[3][1]);ctx.lineTo(P[4][0],P[4][1]);ctx.lineTo(x,y-12*s);ctx.closePath()},`rgba(255,245,225,${.22*(1-(o.dark||0))})`,{sh:0,lw:0});
  if(o.moss){cutP(()=>{ctx.moveTo(P[1][0],P[1][1]);ctx.quadraticCurveTo(x-20*s,y-60*s,P[5][0],P[5][1]);ctx.lineTo(P[4][0],P[4][1]);ctx.lineTo(P[2][0],P[2][1]);ctx.closePath()},FOGC('#4a7a3a',o),{sh:0,lw:1})}},
 cloud(x,y,s,t,o){const c=o.col||'#f4f0ff',dx=Math.sin(t*.15+x)*10*s,P=[[-70,6,30],[-36,-14,40],[6,-24,48],[46,-10,38],[80,6,26]].map(([a,b,rr])=>[x+dx+a*s,y+b*s,rr*s]);
  cutU(()=>{P.forEach(([px,py,rr])=>{ctx.moveTo(px+rr,py);ctx.arc(px,py,rr,0,TAU)});ctx.rect(x+dx-70*s,y,150*s,16*s)},vg(y-70*s,y+20*s,[FOGC(shd(c,1.05),o),FOGC(shd(c,.86),o)]),fogO(o));
  ctx.strokeStyle=`rgba(255,255,255,${.5*(1-(o.fog||0))})`;ctx.lineWidth=2;P.forEach(([px,py,rr])=>{if(rr<35*s)return;ctx.beginPath();ctx.arc(px,py,rr-4,PI*1.1,PI*1.5);ctx.stroke()})},
 mountain(x,y,s,t,o){const c=FOGC(o.col||'#6a74a8',o),h=(o.h||320)*s,w=(o.w||300)*s,r=rng(o.seed||Math.round(x)),pts=[[x-w,y]];for(let i=1;i<8;i++){const u=i/8,px=x-w+u*2*w,py=y-h*(1-Math.abs(u-.5)*2)*(.85+r()*.15);pts.push([px,i===4?y-h:py])}pts.push([x+w,y]);
  cutP(()=>{ctx.moveTo(pts[0][0],pts[0][1]);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.closePath()},vg(y-h,y,[shd(c,1.2),c,shd(c,.7)]),fogO(o));
  cutP(()=>{ctx.moveTo(x,y-h);ctx.lineTo(pts[5][0],pts[5][1]);ctx.lineTo(pts[6][0],pts[6][1]);ctx.lineTo(x+w,y);ctx.lineTo(x+w*.1,y);ctx.closePath()},'rgba(10,4,30,.16)',{sh:0,lw:0});
  if(o.snow!==false){const sn=FOGC('#f6f8ff',o);cutP(()=>{ctx.moveTo(x,y-h);ctx.lineTo(x+w*.22,y-h*.76);ctx.lineTo(x+w*.1,y-h*.8);ctx.lineTo(x+w*.02,y-h*.72);ctx.lineTo(x-w*.1,y-h*.8);ctx.lineTo(x-w*.22,y-h*.74);ctx.closePath()},sn,{sh:0,lw:1.2})}
  if(o.trees){for(let i=0;i<6;i++){const u=(i+.5)/6,tx=x-w*.8+u*w*1.6,ty=y-4;OBJ.tree(tx,ty,.22*s,t,Object.assign({},o,{kind:'pine',col:'#2a4a3a'}))}}},
 pillar(x,y,s,t,o){const h=(o.h||420)*s,w=(o.w||46)*s,c=o.col||'#e8c878',c2=FOGC(c,o),g=ctx.createLinearGradient(x-w/2,0,x+w/2,0);g.addColorStop(0,FOGC(shd(c,.6),o));g.addColorStop(.35,FOGC(shd(c,1.2),o));g.addColorStop(.65,c2);g.addColorStop(1,FOGC(shd(c,.5),o));const O=fogO(o);
  cutP(()=>ctx.rect(x-w/2,y-h,w,h),g,O);ctx.strokeStyle=`rgba(60,30,10,${.35*(1-(o.fog||0))})`;ctx.lineWidth=1.4;[-.25,0,.25].forEach(k=>{ctx.beginPath();ctx.moveTo(x+k*w,y-h+20*s);ctx.lineTo(x+k*w,y-24*s);ctx.stroke()});
  for(let yy=y-h+60*s;yy<y-30*s;yy+=90*s)cutP(()=>ctx.rect(x-w*.56,yy,w*1.12,8*s),FOGC(shd(c,.85),o),{sh:0,lw:1});
  cutP(()=>{ctx.moveTo(x-w*.85,y-h);ctx.lineTo(x+w*.85,y-h);ctx.lineTo(x+w*.6,y-h-24*s);ctx.quadraticCurveTo(x,y-h-36*s,x-w*.6,y-h-24*s);ctx.closePath()},vg(y-h-36*s,y-h,[FOGC(shd(c,1.3),o),FOGC(shd(c,.7),o)]),O);
  cutP(()=>ctx.rect(x-w*.8,y-24*s,w*1.6,24*s),vg(y-24*s,y,[FOGC(shd(c,1.15),o),FOGC(shd(c,.6),o)]),O)},
 wall(x,y,s,t,o){const w=(o.w||520)*s,h=(o.h||300)*s,c=o.col||'#c89a6a',O=fogO(o);cutP(()=>ctx.rect(x-w/2,y-h,w,h),vg(y-h,y,[FOGC(shd(c,1.15),o),FOGC(shd(c,.7),o)]),O);
  const n=Math.max(1,Math.round(w/(170*s)));for(let i=0;i<n;i++){const ax=x-w/2+(i+.5)*w/n,aw=48*s,top=y-h*.72;cutP(()=>{ctx.moveTo(ax-aw,y-h*.12);ctx.lineTo(ax-aw,top+aw);ctx.quadraticCurveTo(ax-aw,top,ax,top-aw*.5);ctx.quadraticCurveTo(ax+aw,top,ax+aw,top+aw);ctx.lineTo(ax+aw,y-h*.12);ctx.closePath()},vg(top,y,[FOGC('#3a2a5a',o),FOGC('#1a1230',o)]),{sh:0,lw:2,ink:FOGC('#e0b04a',o)})}
  cutP(()=>ctx.rect(x-w/2-8*s,y-h-22*s,w+16*s,22*s),FOGC(shd(c,1.3),o),O);for(let xx=x-w/2;xx<x+w/2;xx+=30*s)cutP(()=>{ctx.moveTo(xx,y-h-22*s);ctx.lineTo(xx+15*s,y-h-40*s);ctx.lineTo(xx+30*s,y-h-22*s);ctx.closePath()},FOGC(shd(c,1.1),o),{sh:0,lw:1})},
 shrub(x,y,s,t,o){const c=o.col||'#3a7a44';[[-40,-20,30],[0,-34,38],[40,-18,30]].forEach(([dx,dy,r],k)=>cutU(()=>ctx.arc(x+dx*s+Math.sin(t+k)*1.5,y+dy*s,r*s,0,TAU),vg(y-72*s,y,[FOGC(shd(c,1.25),o),FOGC(shd(c,.7),o)]),fogO(o)));
  if(o.flowers){const r=rng(Math.round(x));for(let i=0;i<8;i++){ctx.fillStyle=FOGC(o.flowers,o);ctx.beginPath();ctx.arc(x+(r()-.5)*100*s,y-(10+r()*50)*s,3.4*s,0,TAU);ctx.fill()}}},
 hill(x,y,s,t,o){const c=FOGC(o.col||'#5a8a4a',o),w=(o.w||700)*s,h=(o.h||120)*s;cutP(()=>{ctx.moveTo(x-w,y+400);ctx.lineTo(x-w,y);ctx.bezierCurveTo(x-w*.5,y-h,x+w*.5,y-h,x+w,y);ctx.lineTo(x+w,y+400);ctx.closePath()},vg(y-h,y+200,[shd(c,1.2),c,shd(c,.6)]),fogO(o))},
 // reels (reel 4): village house on the river sand: mud walls on a plinth, thatched roof, arched doorway (o.lamp = warm light inside), window, mango-leaf toran
 hut(x,y,s,t,o){const w=(o.w||240)*s,h=(o.h||140)*s,c=o.col||'#e0b07a',rf=o.roof||'#d8a040',O=fogO(o),L=x-w/2,top=y-h;
  cutP(()=>ctx.rect(L-12*s,y-16*s,w+24*s,16*s),vg(y-16*s,y,[FOGC(shd(c,.95),o),FOGC(shd(c,.6),o)]),O);
  cutP(()=>ctx.rect(L,top,w,h-16*s),vg(top,y,[FOGC(shd(c,1.12),o),FOGC(shd(c,.78),o)]),O);
  ctx.strokeStyle=FOGC('rgba(120,60,30,.35)',o);ctx.lineWidth=1.6*s;ctx.beginPath();ctx.moveTo(L,y-40*s);ctx.lineTo(L+w,y-40*s);ctx.stroke();
  const dx=x-w*.14,dw=27*s,dt=y-16*s-h*.62;cutP(()=>{ctx.moveTo(dx-dw,y-16*s);ctx.lineTo(dx-dw,dt+dw);ctx.quadraticCurveTo(dx-dw,dt,dx,dt-dw*.2);ctx.quadraticCurveTo(dx+dw,dt,dx+dw,dt+dw);ctx.lineTo(dx+dw,y-16*s);ctx.closePath()},vg(dt,y,[FOGC(o.lamp?'#a85a2a':'#4a2a1c',o),FOGC(o.lamp?'#5a2a14':'#22120c',o)]),{sh:0,lw:1.8,ink:FOGC('#7a3a18',o)});
  if(o.lamp)glow(dx,y-50*s,60*s,'255,200,120',.5*(1-(o.fog||0)));
  const wx=x+w*.24,wy=top+h*.22,ws=34*s;cutP(()=>ctx.rect(wx-ws/2,wy,ws,ws),FOGC(o.lamp?'#8a4a20':'#3a2218',o),{sh:0,lw:1.6,ink:FOGC('#7a3a18',o)});
  ctx.strokeStyle=FOGC('#b07a3a',o);ctx.lineWidth=2.4*s;for(let k=-1;k<=1;k++){ctx.beginPath();ctx.moveTo(wx+k*ws*.28,wy);ctx.lineTo(wx+k*ws*.28,wy+ws);ctx.stroke()}
  const ov=44*s,rh=h*.82,sw=Math.sin(t*.6+x)*1.2*s;
  cutP(()=>{ctx.moveTo(L-ov,top+10*s);ctx.quadraticCurveTo(L+w*.12,top-rh*.55,x-w*.08+sw,top-rh);ctx.lineTo(x+w*.08+sw,top-rh);ctx.quadraticCurveTo(L+w*.88,top-rh*.55,L+w+ov,top+10*s);
   ctx.quadraticCurveTo(x,top+26*s,L-ov,top+10*s);ctx.closePath()},vg(top-rh,top+20*s,[FOGC(shd(rf,1.3),o),FOGC(rf,o),FOGC(shd(rf,.7),o)]),O);
  ctx.save();ctx.strokeStyle=FOGC('rgba(110,60,10,.45)',o);ctx.lineWidth=1.3*s;for(let i=1;i<14;i++){const u=i/14,bx=L-ov+u*(w+2*ov),by=top+10*s+Math.sin(u*PI)*14*s;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(x+(u-.5)*w*.16+sw,top-rh+6*s);ctx.stroke()}ctx.restore();
  cutP(()=>{ctx.moveTo(L-ov,top+10*s);ctx.quadraticCurveTo(x,top+26*s,L+w+ov,top+10*s);ctx.lineTo(L+w+ov,top+18*s);ctx.quadraticCurveTo(x,top+36*s,L-ov,top+18*s);ctx.closePath()},FOGC(shd(rf,.75),o),{sh:0,lw:1});
  if(o.toran!==false){ctx.strokeStyle=FOGC('#6a4a20',o);ctx.lineWidth=1.4*s;ctx.beginPath();ctx.moveTo(dx-dw-10*s,dt-dw*.2-6*s);ctx.quadraticCurveTo(dx,dt+4*s,dx+dw+10*s,dt-dw*.2-6*s);ctx.stroke();
   for(let i=0;i<7;i++){const u=i/6,lx=dx-dw-10*s+u*(2*dw+20*s),ly=dt-dw*.2-6*s+Math.sin(u*PI)*9*s;cutP(()=>{ctx.moveTo(lx-4*s,ly);ctx.lineTo(lx,ly+13*s);ctx.lineTo(lx+4*s,ly);ctx.closePath()},FOGC(i%2?'#3a8a3a':'#f0a020',o),{sh:0,lw:.8})}}},
 // reels (reel 7): dusty road from (x,y) (half-width o.w) narrowing to the horizon point (o.ex,o.ey) (half-width o.ew); o.bend curves it,
 // o.col sand colour, o.glow (rgb string) = a path of light, o.plain = no ruts/stones but ripple lines (a river: col blue); ruts + edge stones fade with distance
 road(x,y,s,t,o){const w=(o.w||200)*s,ex=o.ex??x+120,ey=o.ey??y-260,ew=(o.ew||5)*s,bd=(o.bend||0)*s,c=o.col||'#ecd29a',mx=(x+ex)/2+bd,my=(y+ey)/2;
  const side=k=>{ctx.moveTo(x+k*w,y+300);ctx.lineTo(x+k*w,y);ctx.quadraticCurveTo(mx+k*(w+ew)*.42,my,ex+k*ew,ey)};
  cutP(()=>{side(-1);ctx.lineTo(ex+ew,ey);ctx.quadraticCurveTo(mx+(w+ew)*.42,my,x+w,y);ctx.lineTo(x+w,y+300);ctx.closePath()},vg(ey,y+60,[FOGC(mix(c,'#fff6e0',.45),o),FOGC(c,o),FOGC(shd(c,.86),o)]),Object.assign(fogO(o),{blur:4,sy:2}));
  if(o.glow){ctx.save();ctx.globalCompositeOperation='lighter';ctx.beginPath();side(-1);ctx.lineTo(ex+ew,ey);ctx.quadraticCurveTo(mx+(w+ew)*.42,my,x+w,y);ctx.lineTo(x+w,y+300);ctx.closePath();
   const g=ctx.createLinearGradient(0,ey,0,y);g.addColorStop(0,`rgba(${o.glow},.32)`);g.addColorStop(1,`rgba(${o.glow},.04)`);ctx.fillStyle=g;ctx.fill();ctx.restore()}
  if(o.plain){ctx.save();ctx.strokeStyle=`rgba(255,255,255,${.45*(1-(o.fog||0))})`;ctx.lineWidth=2*s;for(let i=0;i<9;i++){const u=.08+i*.1,qx=(1-u)*(1-u)*x+2*u*(1-u)*mx+u*u*ex,qy=(1-u)*(1-u)*y+2*u*(1-u)*my+u*u*ey,hw=((1-u)*w+u*ew)*.5;ctx.beginPath();ctx.moveTo(qx-hw+Math.sin(t+i)*hw*.3,qy);ctx.lineTo(qx+hw*.2+Math.sin(t+i)*hw*.3,qy);ctx.stroke()}ctx.restore();return}
  ctx.save();ctx.strokeStyle=FOGC(shd(c,.72),o);ctx.globalAlpha*=.5;ctx.lineWidth=2*s;[-.35,.35].forEach(k=>{ctx.beginPath();ctx.moveTo(x+k*w,y+60);ctx.quadraticCurveTo(mx+k*(w+ew)*.2,my,ex+k*ew*.5,ey+4);ctx.stroke()});ctx.restore();
  const r=rng(o.seed||Math.round(x+ex));for(let i=0;i<18;i++){const u=r(),k=r()<.5?-1:1,qx=(1-u)*(1-u)*(x+k*w)+2*u*(1-u)*(mx+k*(w+ew)*.42)+u*u*(ex+k*ew),qy=(1-u)*(1-u)*y+2*u*(1-u)*my+u*u*ey,rs=(1-u*.85)*7*s;
   cutP(()=>ctx.ellipse(qx+k*rs*.6,qy,rs*1.3,rs*.8,0,0,TAU),FOGC(i%3?'#b8a488':'#9a8a76',o),{sh:0,lw:.8})}}
};
const LDEF={far:{par:.2,fog:.55,blur:1.2,dark:0},mid:{par:.55,fog:.22,blur:0,dark:0},near:{par:1.35,fog:0,blur:1.6,dark:.55}};
/* layered scenery: L = [{d:'far'|'mid'|'near', par?, fog?, haze?, blur?, dark?, items:[{o:'tree'|'rock'|'cloud'|'mountain'|'pillar'|'wall'|'shrub'|'hill', x, y, s, ...object options}]}]
   which = 'back' draws far+mid (behind the actors), 'front' draws near (in front of them). After the far layer a haze band softens it. */
function drawLayers(L,t,which){(L||[]).forEach(ly=>{const D=LDEF[ly.d]||LDEF.mid,front=ly.d==='near';if((which==='front')!==front)return;const o0={fog:ly.fog??D.fog,haze:ly.haze||'#d8d4ec',dark:ly.dark??D.dark,darkc:ly.darkc};
  layer(ly.par??D.par,()=>{const b=ly.blur??D.blur;if(b>0)ctx.filter=`blur(${(b*SC_).toFixed(2)}px)`;(ly.items||[]).forEach(it=>{const f=OBJ[it.o];if(f)f(it.x,it.y,it.s||1,t,Object.assign({},o0,it))});ctx.filter='none';
    if(ly.d==='far'&&ly.hazeBand!==false){const c=hx(o0.haze);skyG([`rgba(${c},0)`,`rgba(${c},${(.22*(ly.hazeA??1)).toFixed(3)})`,`rgba(${c},0)`],(ly.hy??420)-200,(ly.hy??420)+160)}})})}

// the old lollipop tree now draws the proper paper tree (keeps every background that calls ptree)
ptree=function(x,y,h,t,i,c,trunk){OBJ.tree(x,y,h/200,t,{col:c[1]||c[0],trunk:trunk||'#3a2418',kind:i%4===3?'pine':'round'})};
/* default FOREGROUND per background (drawn in front of the actors, blurred and darker = shallow focus). Kept to the bottom
   corners so faces stay clear. Turn off with bg.fore:false, or replace with a 'near' layer in sc.layers. */
const FG=(items,o)=>drawLayers([Object.assign({d:'near',items},o||{})],0,'front');
window.BGF={
 vista:(S,t)=>FG([{o:'rock',x:50,y:H-6,s:2.1,col:'#5a6a7a',moss:1},{o:'shrub',x:190,y:H+4,s:1.5,col:'#2a5a3a'},{o:'shrub',x:1170,y:H+6,s:1.7,col:'#2a5a3a',flowers:'#f0c040'},{o:'rock',x:1280,y:H,s:1.8,col:'#5a6a7a'}],{dark:.3}),
 kailash:(S,t)=>FG([{o:'rock',x:40,y:H+40,s:2,col:'#c8d0ec'},{o:'rock',x:1250,y:H+50,s:1.7,col:'#c8d0ec'}],{dark:.35,darkc:'#0a1030'}),
 cloudscape:(S,t)=>FG([{o:'cloud',x:-20,y:H-10,s:2.4,col:'#ffffff'},{o:'cloud',x:1300,y:H,s:2.2,col:'#ffffff'}],{dark:.08,blur:2}),
 amber:(S,t)=>FG([{o:'cloud',x:-10,y:H,s:2.2,col:'#ffe0b0'},{o:'cloud',x:1290,y:H+10,s:2,col:'#ffe0b0'}],{dark:.12,darkc:'#5a2a08',blur:2}),
 dusk:(S,t)=>FG([{o:'cloud',x:-10,y:H,s:2.1,col:'#f0b0a0'},{o:'cloud',x:1290,y:H+10,s:2,col:'#f0b0a0'}],{dark:.15,blur:2}),
 garden:(S,t)=>FG([{o:'shrub',x:70,y:H+20,s:1.6,col:'#2e6a34',flowers:'#f6c8d8'},{o:'shrub',x:1210,y:H+20,s:1.7,col:'#2e6a34',flowers:'#fff0b8'}],{dark:.3}),
 storm:(S,t)=>FG([{o:'rock',x:40,y:H+40,s:1.9,col:'#3a3040'},{o:'rock',x:1250,y:H+40,s:1.6,col:'#3a3040'}],{dark:.45}),
 vaikuntha:(S,t)=>FG([{o:'cloud',x:-20,y:H-10,s:2.4,col:'#ffffff'},{o:'cloud',x:1300,y:H,s:2.2,col:'#ffffff'}],{dark:.06,blur:2}),
 palace:(S,t)=>FG([{o:'pillar',x:-6,y:H+30,s:1.25,col:'#e8c878'},{o:'pillar',x:1286,y:H+30,s:1.25,col:'#e8c878'}],{dark:.35,darkc:'#2a0a10'})
};
/* ---- EP07 dark cinematic look (Nov 2026): matte earth palette (burnt sienna, ember orange, dark maroon, charcoal), firelight only.
   Silhouette layer objects: demons (a row of black asura silhouettes with ember eyes, horns, weapons, sizes, sway), stree (forest
   silhouette tree), smoke (dark rolling smoke band).  Backgrounds: ashram (dusk), kacha_room_night (night interior, oil lamp, mat, bed,
   window), forest (dawn, smoke), feasthall (demon feast hall, firelight, back-row crowd), council (heaven council, dim gold-brown). ---- */
const SIL='#0e0709';
function demonSil(x,y,h,kind,t,col,eyeA,seed,sway){const r=rng(seed),sw=Math.sin(t*(1.1+r()*.8)+seed)*.035*(sway??1),wd=.85+r()*.35,arm=r(),weap=kind%4;ctx.save();ctx.translate(x,y);ctx.rotate(sw);ctx.scale(h*wd,h);
  const lw=.075;ctx.lineCap='round';ctx.lineJoin='round';
  const body=()=>{ctx.moveTo(-.16,0);ctx.lineTo(-.1,-.42);ctx.lineTo(-.15,-.46);ctx.lineTo(-.26,-.7);ctx.quadraticCurveTo(-.12,-.78,-.05,-.76);ctx.lineTo(-.06,-.8);ctx.lineTo(.06,-.8);ctx.lineTo(.05,-.76);ctx.quadraticCurveTo(.12,-.78,.26,-.7);ctx.lineTo(.15,-.46);ctx.lineTo(.1,-.42);ctx.lineTo(.16,0);ctx.lineTo(.05,0);ctx.lineTo(0,-.28);ctx.lineTo(-.05,0);ctx.closePath();
    ctx.moveTo(.085,-.86);ctx.ellipse(0,-.86,.085,.095,0,0,TAU);
    const hk=kind%3;[-1,1].forEach(sd=>{if(hk===0){ctx.moveTo(sd*.05,-.92);ctx.quadraticCurveTo(sd*.16,-.96,sd*.15,-1.06);ctx.quadraticCurveTo(sd*.1,-.98,sd*.02,-.94)}
      else if(hk===1){ctx.moveTo(sd*.06,-.93);ctx.lineTo(sd*.07,-1.08);ctx.lineTo(sd*.01,-.94)}
      else{ctx.moveTo(sd*.06,-.9);ctx.bezierCurveTo(sd*.2,-.98,sd*.22,-.8,sd*.12,-.8);ctx.quadraticCurveTo(sd*.15,-.88,sd*.05,-.86)}})};
  ctx.beginPath();body();ctx.fillStyle=col;ctx.fill();
  ctx.strokeStyle=col;ctx.lineWidth=lw;const L=[[-.24,-.7],[-.3,-.56],[-.33,-.42]];const Rr=arm<.5?[[.24,-.7],[.33,-.82],[.36,-.96]]:[[.24,-.7],[.36,-.6],[.42,-.66]];
  [L,Rr].forEach(a=>{ctx.beginPath();ctx.moveTo(a[0][0],a[0][1]);ctx.lineTo(a[1][0],a[1][1]);ctx.lineTo(a[2][0],a[2][1]);ctx.stroke()});
  const hx=Rr[2][0],hy=Rr[2][1];ctx.lineWidth=.022;ctx.beginPath();
  if(weap===0){ctx.moveTo(hx,hy+.45);ctx.lineTo(hx,hy-.36);ctx.stroke();ctx.beginPath();ctx.moveTo(hx-.035,hy-.34);ctx.lineTo(hx,hy-.48);ctx.lineTo(hx+.035,hy-.34);ctx.closePath();ctx.fill()}
  else if(weap===1){ctx.moveTo(hx,hy+.08);ctx.lineTo(hx,hy-.3);ctx.stroke();ctx.beginPath();ctx.arc(hx,hy-.33,.06,0,TAU);ctx.fill()}
  else if(weap===2){ctx.moveTo(hx,hy+.04);ctx.lineTo(hx+.18,hy-.3);ctx.lineWidth=.035;ctx.stroke()}
  else{ctx.moveTo(hx,hy+.1);ctx.lineTo(hx,hy-.26);ctx.stroke();ctx.beginPath();ctx.moveTo(hx,hy-.26);ctx.quadraticCurveTo(hx+.14,hy-.3,hx+.12,hy-.14);ctx.lineTo(hx,hy-.16);ctx.closePath();ctx.fill()}
  ctx.restore();
  if(eyeA>0){const ex=x+Math.sin(sw)*h*.86,ey=y-h*.87,fl=.75+.25*Math.sin(t*3+seed);[-1,1].forEach(sd=>{const px=ex+sd*h*.03*wd;glow(px,ey,h*.05,'255,90,30',.55*eyeA*fl);ctx.fillStyle=`rgba(255,${150+((seed*7)%60)},60,${eyeA*fl})`;ctx.beginPath();ctx.ellipse(px,ey,Math.max(.8,h*.012),Math.max(.6,h*.007),sd*.25,0,TAU);ctx.fill()})}}
Object.assign(OBJ,{
 demons(x,y,s,t,o){const n=o.n||7,w=(o.w||900)*s,seed=o.seed||5,r=rng(seed),col=FOGC(o.col||SIL,o),eyes=(o.eyes??1)*(1-(o.fog||0)*.55);
  const P=[];for(let i=0;i<n;i++){const u=n>1?i/(n-1):.5;P.push([x-w/2+u*w+(r()-.5)*w/n*.6,y+(r()-.5)*10*s,(150+r()*90)*s*(o.h||1),Math.floor(r()*12),seed*31+i])}
  P.sort((a,b)=>b[2]-a[2]).reverse();P.forEach(([px,py,h,k,sd])=>demonSil(px,py,h,k,t,col,eyes,sd,o.sway))},
 stree(x,y,s,t,o){const col=FOGC(o.col||'#140a0a',o),h=(o.h||520)*s,r=rng(o.seed||Math.round(x)),sw=Math.sin(t*.5+x*.01)*3*s;
  cutU(()=>{ctx.moveTo(x-18*s,y);ctx.quadraticCurveTo(x-9*s,y-h*.5,x-5*s+sw*.3,y-h);ctx.lineTo(x+5*s+sw*.3,y-h);ctx.quadraticCurveTo(x+9*s,y-h*.5,x+18*s,y);ctx.closePath();
    for(let i=0;i<4;i++){const yy=y-h*(.42+i*.13),sd=i%2?1:-1,L=(50+r()*50)*s;ctx.moveTo(x,yy+6*s);ctx.quadraticCurveTo(x+sd*L*.5,yy-L*.15,x+sd*L+sw,yy-L*.4);ctx.lineTo(x+sd*L*.92+sw,yy-L*.3);ctx.quadraticCurveTo(x+sd*L*.4,yy+2*s,x,yy+14*s);ctx.closePath()}
    if(!o.bare){const n=7;for(let i=0;i<n;i++){const u=i/(n-1),cx=x+(u-.5)*h*.42+sw,cy=y-h*(.78+Math.sin(u*PI)*.18)+r()*20*s,R=h*(.07+r()*.04);ctx.moveTo(cx+R,cy);ctx.ellipse(cx,cy,R,R*.8,0,0,TAU)}}},col,{blur:6,sy:3,lw:1,ink:'rgba(0,0,0,.35)'})},
 smoke(x,y,s,t,o){const w=(o.w||1400)*s,h=(o.h||120)*s,col=o.col||'#2a1814',a=o.a??.75,r=rng(o.seed||3),dx=(t*(o.v??8))%(w*.25);ctx.save();ctx.globalAlpha*=a;ctx.filter=`blur(${(h*.12*SC_).toFixed(1)}px)`;
  ctx.beginPath();for(let i=0;i<16;i++){const px=x-w/2+((i/16)*w+dx)%w,py=y-h*.3-r()*h*.5,R=h*(.35+r()*.45);ctx.moveTo(px+R,py);ctx.arc(px,py,R,0,TAU)}ctx.rect(x-w/2,y-h*.3,w,h*.8);
  ctx.fillStyle=vg(y-h,y+h*.6,[FOGC(shd(col,1.12),o),FOGC(col,o),FOGC(shd(col,.75),o)]);ctx.fill();ctx.filter='none';ctx.restore()}
});
/* winwall (EP07, Devayani's window): x = window centre, y = ground, s. part:'back' = the dark room behind the window (lamp glow; put it in a
   mid layer), part:'front' (default) = the mud wall with the window cut out, wooden frame, open shutters, thatch eave and a jasmine vine
   (put it in a near layer with dark ~0, blur 0, par 1): a figure standing behind it is seen through the window. l/r = wall extent left/right
   of the window, lit = light colour on the wall ('255,170,90'), lamp 0..1 (night: warm lamp inside), wy = window centre height above y. */
Object.assign(OBJ,{
 winwall(x,y,s,t,o){const ww=170*s,wh=160*s,cy=y-(o.wy||330)*s,L=x-(o.l??300)*s,R=x+(o.r??760)*s,top=y-(o.h||560)*s,lit=o.lit||'255,170,90',lamp=o.lamp??0;
  const hole=()=>{ctx.moveTo(x-ww/2,cy+wh/2);ctx.lineTo(x+ww/2,cy+wh/2);ctx.lineTo(x+ww/2,cy-wh*.25);ctx.quadraticCurveTo(x+ww/2,cy-wh/2-ww*.2,x,cy-wh/2-ww*.28);ctx.quadraticCurveTo(x-ww/2,cy-wh/2-ww*.2,x-ww/2,cy-wh*.25);ctx.closePath()};
  if(o.part==='back'){ctx.save();ctx.beginPath();ctx.rect(x-ww,cy-wh*1.3,ww*2,wh*2.8);ctx.fillStyle=vg(cy-wh,cy+wh*1.4,['#1a0c08','#2a140c','#120806']);ctx.fill();
    if(lamp>0){glow(x+ww*.55,cy+wh*.1,ww*1.2,'255,140,60',.55*lamp);glow(x+ww*.55,cy+wh*.1,ww*.4,'255,200,120',.5*lamp)}ctx.restore();return}
  const wall=()=>{ctx.moveTo(L,top);ctx.lineTo(R,top);ctx.lineTo(R,y+120);ctx.lineTo(L,y+120);ctx.closePath();hole()};
  ctx.save();ctx.beginPath();wall();ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=16*SC_;ctx.fillStyle=vg(top,y+120,['#7a4a2a','#6a3e22','#3a2012']);ctx.fill('evenodd');ctx.restore();
  ctx.save();ctx.beginPath();wall();ctx.clip('evenodd');const r=rng(23);ctx.fillStyle='rgba(30,12,4,.12)';for(let i=0;i<30;i++){ctx.beginPath();ctx.ellipse(L+r()*(R-L),top+r()*(y+120-top),20+r()*60,10+r()*26,r(),0,TAU);ctx.fill()}
    const g=ctx.createRadialGradient(x-ww*1.4,cy-wh,10,x-ww*1.4,cy-wh,ww*4);g.addColorStop(0,`rgba(${lit},.32)`);g.addColorStop(1,`rgba(${lit},0)`);ctx.fillStyle=g;ctx.fillRect(L,top,R-L,y+120-top);
    if(lamp>0){const g2=ctx.createRadialGradient(x,cy,ww*.4,x,cy,ww*1.6);g2.addColorStop(0,`rgba(255,140,60,${.35*lamp})`);g2.addColorStop(1,'rgba(255,140,60,0)');ctx.fillStyle=g2;ctx.fillRect(L,top,R-L,y+120-top)}
    ctx.strokeStyle='rgba(20,8,2,.35)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(L,y-60*s);ctx.lineTo(R,y-60*s);ctx.stroke();ctx.restore();
  ctx.save();ctx.lineJoin='round';ctx.beginPath();hole();ctx.lineWidth=16*s;ctx.strokeStyle='#4a2a16';ctx.stroke();ctx.lineWidth=2;ctx.strokeStyle='#160a04';ctx.stroke();ctx.restore();
  cutP(()=>ctx.rect(x-ww/2-22*s,cy+wh/2,ww+44*s,16*s),vg(cy+wh/2,cy+wh/2+16*s,['#7a4a26','#3a200e']),{blur:6,lw:1.4});
  [-1,1].forEach(sd=>{const hx=x+sd*(ww/2+8*s),fw=ww*.42;cutP(()=>{ctx.moveTo(hx,cy-wh*.35);ctx.lineTo(hx+sd*fw,cy-wh*.42);ctx.lineTo(hx+sd*fw,cy+wh*.52);ctx.lineTo(hx,cy+wh*.48);ctx.closePath()},vg(cy-wh*.4,cy+wh*.5,['#6a3e1e','#3a200e']),{blur:5,lw:1.6,ink:'#160a04'});
    ctx.strokeStyle='rgba(20,8,2,.5)';ctx.lineWidth=1.4;for(let k=1;k<4;k++){ctx.beginPath();ctx.moveTo(hx+sd*fw*k/4,cy-wh*.36-k*2);ctx.lineTo(hx+sd*fw*k/4,cy+wh*.5);ctx.stroke()}});
  cutP(()=>{ctx.moveTo(L-30,top-10*s);ctx.lineTo(R+30,top-10*s);ctx.lineTo(R+30,top+46*s);for(let i=0;i<=40;i++){const u=i/40;ctx.lineTo(R+30-u*(R-L+60),top+46*s+(i%2?10:0)*s)}ctx.closePath()},vg(top-10*s,top+56*s,['#8a6a34','#5a401c','#2a1a0a']),{blur:8,lw:1.6});
  const vx=x-ww/2-36*s;ctx.strokeStyle='#2a3a1a';ctx.lineWidth=3*s;ctx.beginPath();ctx.moveTo(vx,y+40);for(let i=0;i<=12;i++){const yy=y+40-i*(y+40-cy+wh*.6)/12;ctx.lineTo(vx+Math.sin(i*1.3+t*.4)*10*s,yy)}ctx.stroke();
  for(let i=0;i<14;i++){const yy=y+20-i*(y+20-cy+wh*.6)/14,xx=vx+Math.sin(i*1.3)*10*s+(i%2?9:-9)*s;cutP(()=>ctx.ellipse(xx,yy,7*s,3.5*s,i%2?.6:-.6,0,TAU),'#3a5a24',{sh:0,lw:.6});
    if(i%3===1)cutP(()=>{for(let k=0;k<5;k++){const a=k/5*TAU;ctx.moveTo(xx+Math.cos(a)*5*s,yy-8*s+Math.sin(a)*5*s);ctx.arc(xx+Math.cos(a)*5*s,yy-8*s+Math.sin(a)*5*s,3*s,0,TAU)}},'#f4ecd8',{sh:0,lw:.5,ink:'rgba(120,90,60,.6)'})}}
});
const EMB=(t,n,seed)=>embers(t,n,seed,'255,130,50',.8);
function diya(x,y,s,t){glow(x,y-14*s,140*s,'255,140,50',.35);glow(x,y-14*s,50*s,'255,200,120',.4);cutP(()=>{ctx.moveTo(x-18*s,y-6*s);ctx.quadraticCurveTo(x,y+8*s,x+18*s,y-6*s);ctx.lineTo(x+22*s,y-10*s);ctx.lineTo(x-20*s,y-8*s);ctx.closePath()},vg(y-10*s,y+6*s,['#a8602a','#5a2a12']),{blur:4,lw:1.4});
  const f=Math.sin(t*9)*2*s;cutP(()=>{ctx.moveTo(x+12*s,y-10*s);ctx.quadraticCurveTo(x+4*s+f,y-22*s,x+10*s+f,y-36*s);ctx.quadraticCurveTo(x+20*s,y-22*s,x+16*s,y-10*s);ctx.closePath()},vg(y-36*s,y-10*s,['#fff0b0','#ffa83a','#d8501a']),{sh:0,lw:1,ink:'rgba(120,30,0,.6)'})}
Object.assign(BG,{
 ashram(S,t){skyG(S.sky||['#1a0a0e','#3a1414','#7a2e18','#b8561e'],-300,H+300);const sx=S.sx??W*.7,sy=S.sy??360;glow(sx,sy,380,'255,120,50',.28);
  layer(.05,()=>{cutP(()=>ctx.arc(sx,sy,40,0,TAU),vg(sy-40,sy+40,['#f0a050','#c8501e']),{sh:0,lw:0});stars(t,18,7,140)});
  layer(.12,()=>cloudlets(13,4,90,230,{light:'#6a2a1e',mid:'#3a1612'},t,1.1));
  layer(.18,()=>{ridgeP(380,90,.004,31,'#3a1a16',.18,'rgba(255,130,60,.35)');skyG(['rgba(120,50,30,0)','rgba(120,50,30,.25)'],320,520)});
  layer(.35,()=>{[[150,470,.9],[1120,460,1.1],[420,480,.7]].forEach(([x,y,s2],i)=>OBJ.tree(x,y,s2,t,{kind:i?'round':'banyan',col:'#2a1a14',trunk:'#1a0e0a',fog:.45,haze:'#4a2018'}))});
  layer(.55,()=>{cutP(()=>{ctx.moveTo(-400,560);ctx.bezierCurveTo(300,530,900,560,1700,540);ctx.lineTo(1700,H+300);ctx.lineTo(-400,H+300);ctx.closePath()},vg(530,H,['#4a2a1a','#1a0c08']),{blur:10});
    OBJ.hut(S.hx??250,560,.95,t,{col:'#6a3e24',roof:'#4a2e18',lamp:S.lamp!==false,fog:.15,haze:'#3a1a10',dark:.15});OBJ.hut(S.hx2??1060,566,.8,t,{col:'#5a3420',roof:'#3e2614',lamp:S.lamp!==false,fog:.2,haze:'#3a1a10',dark:.2});
    if(S.fire!==false){const fx=S.fx??640;glow(fx,560,220,'255,120,40',.3);for(let k=-2;k<=2;k++)cutP(()=>ctx.ellipse(fx+k*14,566-Math.abs(k)*1.5,8,5,0,0,TAU),'#3a2a22',{sh:0,lw:1})}});
  dust(t,24,7,'255,150,80',.35,3)},
 kacha_room_night(S,t){skyG(['#120a0a','#1e1210','#2a1810'],-300,H+300);const wx=S.wx??250,lx=S.lx??860,lamp=S.lamp??1;
  layer(.3,()=>{// back wall (mud plaster) with a small barred window onto the night
    cutP(()=>ctx.rect(-300,40,W+600,560),vg(40,600,['#2a1a14','#3a2218','#24140e']),{sh:0,lw:0});const r=rng(4);ctx.fillStyle='rgba(0,0,0,.07)';for(let i=0;i<26;i++){ctx.beginPath();ctx.ellipse(r()*W,60+r()*520,20+r()*50,12+r()*24,r(),0,TAU);ctx.fill()}
    ctx.save();ctx.beginPath();ctx.rect(wx-80,170,160,150);ctx.clip();skyG(['#0a0e22','#1a2240','#2a2a44'],170,320);stars(t,26,11,320);moonAt(wx+40,210,14,t);ctx.restore();
    ctx.save();ctx.beginPath();ctx.rect(wx-96,154,192,182);ctx.rect(wx+80,170,-160,150);ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=8*SC_;ctx.shadowOffsetY=4*SC_;ctx.fillStyle='#4a2e1c';ctx.fill();ctx.shadowColor='transparent';ctx.lineWidth=2;ctx.strokeStyle='#120804';ctx.stroke();ctx.restore();
    for(let k=-1;k<=1;k++)cutP(()=>ctx.rect(wx+k*40-4,170,8,150),'#2a1810',{sh:0,lw:1});glow(wx,330,160,'110,130,200',.08);
    // shelf with the oil lamp, a water pot, a hanging cloth
    cutP(()=>ctx.rect(lx-90,330,180,12),vg(330,342,['#6a4428','#3a2212']),{blur:6,lw:1.4});diya(lx,330,1.2,t);
    cutP(()=>{ctx.ellipse(lx-56,312,16,18,0,0,TAU)},vg(294,330,['#8a4a22','#4a220e']),{blur:4,lw:1.2});
    if(lamp){glow(lx,300,420*lamp,'255,130,50',.22*lamp);glow(lx,300,180,'255,170,90',.2*lamp)}});
  layer(.6,()=>{// floor, a reed mat, a low wooden bed with a folded cloth
    cutP(()=>ctx.rect(-300,590,W+600,400),vg(590,H,['#2a1810','#120806']),{blur:10,lw:0});
    cutP(()=>{ctx.moveTo(300,606);ctx.lineTo(700,606);ctx.lineTo(740,656);ctx.lineTo(260,656);ctx.closePath()},vg(606,656,['#8a6a3a','#5a4024']),{blur:6,lw:1.4});ctx.strokeStyle='rgba(30,16,6,.45)';ctx.lineWidth=1.4;for(let x=270;x<740;x+=12){ctx.beginPath();ctx.moveTo(x+30*(x-500)/400,606);ctx.lineTo(x,656);ctx.stroke()}
    const bx=S.bx??1080;cutP(()=>ctx.rect(bx-170,500,340,26),vg(500,526,['#5a3a22','#2a180c']),{blur:8,lw:1.8});[-160,150].forEach(dx=>cutP(()=>ctx.rect(bx+dx,520,12,90),'#2a180c',{blur:4,lw:1.2}));
    cutP(()=>{ctx.moveTo(bx-160,500);ctx.quadraticCurveTo(bx,486,bx+160,500);ctx.lineTo(bx+160,506);ctx.lineTo(bx-160,506);ctx.closePath()},vg(486,506,['#c8b088','#8a7050']),{sh:0,lw:1.2});
    cutP(()=>ctx.roundRect(bx+70,480,70,22,8),vg(480,502,['#a08060','#6a5038']),{sh:0,lw:1.2})});
  if(lamp)glow(lx,300,620,'255,120,40',.1*lamp);dust(t,14,5,'255,170,100',.25,2)},
 forest(S,t){const sm=S.smoke??.7;skyG(S.sky||['#140c0c','#2e1612','#6a3018','#a85a24'],-300,H+300);const sx=S.sx??CX+120,sy=S.sy??420;glow(sx,sy,460,'255,140,60',.3);
  layer(.05,()=>cutP(()=>ctx.arc(sx,sy,34,0,TAU),vg(sy-34,sy+34,['#f0b060','#d8641e']),{sh:0,lw:0}));
  layer(.12,()=>{for(let i=0;i<9;i++){const x=-60+i*170,h=380+((i*53)%120);OBJ.stree(x,560,.8,t,{h:h,fog:.6,haze:'#6a3a24',seed:i+3})}});
  layer(.2,()=>OBJ.smoke(CX,470,1,t,{w:1800,h:140,col:'#5a3424',a:.55*sm,seed:7,v:6}));
  layer(.34,()=>{for(let i=0;i<6;i++){const x=40+i*250+((i*71)%60),h=520+((i*37)%100);OBJ.stree(x,600,1,t,{h:h,fog:.28,haze:'#4a2418',seed:i+11})}});
  layer(.42,()=>{if(S.rays!==false){ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<5;i++){const x0=sx-200+i*110,g=ctx.createLinearGradient(x0,0,x0-220,H);g.addColorStop(0,'rgba(255,150,70,.12)');g.addColorStop(1,'rgba(255,150,70,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(x0-10,0);ctx.lineTo(x0+14,0);ctx.lineTo(x0-180,H);ctx.lineTo(x0-240,H);ctx.closePath();ctx.fill()}ctx.restore()}
    OBJ.smoke(CX,560,1,t,{w:1900,h:110,col:'#3a2018',a:.65*sm,seed:13,v:10})});
  layer(.62,()=>{cutP(()=>{ctx.moveTo(-400,600);ctx.bezierCurveTo(200,580,800,610,1700,590);ctx.lineTo(1700,H+300);ctx.lineTo(-400,H+300);ctx.closePath()},vg(580,H,['#3a2016','#100604']),{blur:10});
    const r=rng(9);ctx.strokeStyle='#1a0c08';ctx.lineCap='round';for(let i=0;i<14;i++){const x=r()*W,y=610+r()*90,L=30+r()*60,a=(r()-.5)*.6;ctx.lineWidth=3+r()*4;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+Math.cos(a)*L,y+Math.sin(a)*L*.3);ctx.stroke()}});
  dust(t,30,17,'255,150,80',.35,2);EMB(t,10,3)},
 feasthall(S,t){skyG(['#0c0606','#1e0c0a','#3a1610'],-300,H+300);const fire=S.fire??1;
  layer(.2,()=>{// far wall: rough stone arches lit from below
    const xs=[CX-430,CX,CX+430];xs.forEach((x,i)=>{const arch=()=>{ctx.moveTo(x-130,600);ctx.lineTo(x-130,300);ctx.quadraticCurveTo(x-130,170,x,150);ctx.quadraticCurveTo(x+130,170,x+130,300);ctx.lineTo(x+130,600);ctx.closePath()};
      ctx.save();ctx.beginPath();arch();ctx.clip();skyG(['#2a0c0a','#5a1e10','#8a3a14'],150,600);glow(x,560,260,'255,110,40',.4*fire);ctx.restore();cutP(arch,'rgba(0,0,0,0)',{sh:0,lw:10,ink:'#1a0c0a'})});
    const r=rng(8);ctx.strokeStyle='rgba(0,0,0,.14)';ctx.lineWidth=1.4;for(let y=70;y<600;y+=34){ctx.beginPath();ctx.moveTo(-300,y);ctx.lineTo(W+300,y);ctx.stroke();for(let x=-300+((y/34)%2)*40;x<W+300;x+=80+r()*30){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+34);ctx.stroke()}}
    if(S.crowd!==false)OBJ.demons(CX,600,.9,t,{n:S.crowdN||16,w:1500,fog:.35,haze:'#5a2014',seed:21,eyes:1})});
  layer(.4,()=>{[CX-640,CX-215,CX+215,CX+640].forEach(x=>{cutP(()=>ctx.rect(x-34,120,68,500),vg(0,1,['#2a1612','#0e0606']),{blur:10,lw:2,ink:'#000'});ctx.strokeStyle='rgba(255,120,50,.25)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x+30,140);ctx.lineTo(x+30,610);ctx.stroke()});
    [CX-430,CX+430].forEach((x,i)=>{const y=520;glow(x,y-60,240,'255,110,40',.45*fire);cutP(()=>{ctx.moveTo(x-50,y);ctx.lineTo(x+50,y);ctx.lineTo(x+36,y+40);ctx.lineTo(x-36,y+40);ctx.closePath()},vg(y,y+40,['#5a3420','#1a0c06']),{blur:6,lw:1.6});
      for(let k=0;k<5;k++){const f=Math.sin(t*8+k*1.7+i)*6,hh=(60+((k*29)%40))*fire;cutP(()=>{ctx.moveTo(x-34+k*17,y);ctx.quadraticCurveTo(x-44+k*17+f,y-hh*.6,x-30+k*17+f,y-hh);ctx.quadraticCurveTo(x-20+k*17,y-hh*.5,x-20+k*17,y);ctx.closePath()},vg(y-hh,y,['#ffd070','#e8661c','#8a1a0a']),{sh:0,lw:1,ink:'rgba(90,10,0,.6)'})}})});
  layer(.75,()=>{cutP(()=>ctx.rect(-400,600,W+800,H),vg(600,H+100,['#3a1a10','#0a0404']),{blur:12,lw:2});ctx.strokeStyle='rgba(255,140,80,.08)';ctx.lineWidth=1.4;for(let k=-10;k<=10;k++){ctx.beginPath();ctx.moveTo(CX+k*70,600);ctx.lineTo(CX+k*170,H+60);ctx.stroke()}
    if(S.table!==false){cutP(()=>{ctx.moveTo(CX-420,640);ctx.lineTo(CX+420,640);ctx.lineTo(CX+460,672);ctx.lineTo(CX-460,672);ctx.closePath()},vg(640,672,['#5a3420','#2a140a']),{blur:8,lw:1.8});
      const r=rng(12);for(let i=0;i<9;i++){const x=CX-380+i*95;cutP(()=>{ctx.moveTo(x-12,640);ctx.lineTo(x-14,618);ctx.lineTo(x+14,618);ctx.lineTo(x+12,640);ctx.closePath()},vg(618,640,['#b07a3a','#5a3416']),{sh:0,lw:1});cutP(()=>ctx.ellipse(x+40,636,22,6,0,0,TAU),'#4a2410',{sh:0,lw:1})}}});
  embers(t,40,5,'255,120,40',1.2);dust(t,20,9,'255,140,70',.3,2)},
 council(S,t){skyG(['#120c08','#2a1c10','#4a3218'],-300,H+300);
  layer(.18,()=>{const xs=[CX-410,CX,CX+410];xs.forEach((x,i)=>{const arch=()=>{ctx.moveTo(x-116,560);ctx.lineTo(x-116,280);ctx.quadraticCurveTo(x-116,150,x,140);ctx.quadraticCurveTo(x+116,150,x+116,280);ctx.lineTo(x+116,560);ctx.closePath()};
      ctx.save();ctx.beginPath();arch();ctx.clip();skyG(['#3a2a1a','#6a4a24','#8a6a34'],140,560);cloudlets(41+i,3,200,420,{light:'#8a6a44',mid:'#5a4228'},t,.9);ctx.restore();cutP(arch,'rgba(0,0,0,0)',{sh:0,lw:7,ink:'#8a6a30'})});
    cutP(()=>ctx.rect(-300,92,W+600,36),vg(92,128,['#8a6a34','#4a3418']),{blur:8,lw:1.6})});
  layer(.45,()=>{[CX-205,CX+205,CX-615,CX+615].forEach(x=>OBJ.pillar(x,590,1.05,t,{col:'#8a6a3a',fog:.15,haze:'#3a2a18',h:440}));
    [CX-410,CX+410].forEach(x=>{glow(x,250,120,'255,180,90',.2);diya(x,250,1,t)})});
  layer(.7,()=>{cutP(()=>ctx.rect(-400,590,W+800,H),vg(590,H+100,['#4a3420','#120a06']),{blur:12,lw:2});cutP(()=>{ctx.moveTo(CX-90,590);ctx.lineTo(CX+90,590);ctx.lineTo(CX+240,H+60);ctx.lineTo(CX-240,H+60);ctx.closePath()},vg(590,H,['#5a1a14','#2a0a08']),{sh:0,lw:1.4})});
  glow(CX,380,520,'230,170,90',.1);dust(t,22,19,'240,200,140',.3,2)}
});
Object.assign(window.BGF,{
 ashram:(S,t)=>FG([{o:'shrub',x:60,y:H+24,s:1.7,col:'#1a0e0a'},{o:'shrub',x:1230,y:H+24,s:1.6,col:'#1a0e0a'}],{dark:.6,darkc:'#0a0404'}),
 kacha_room_night:(S,t)=>FG([{o:'pillar',x:-10,y:H+40,s:1.3,col:'#3a2416'}],{dark:.6,darkc:'#080404'}),
 forest:(S,t)=>FG([{o:'stree',x:-20,y:H+60,s:1.2,h:900,bare:1},{o:'shrub',x:1240,y:H+30,s:1.8,col:'#140a08'}],{dark:.7,darkc:'#060202'}),
 feasthall:(S,t)=>FG([{o:'demons',x:90,y:H+120,s:1.6,n:2,w:200,seed:77,eyes:.6},{o:'demons',x:1200,y:H+120,s:1.5,n:2,w:200,seed:91,eyes:.6}],{dark:.2}),
 council:(S,t)=>FG([{o:'pillar',x:-6,y:H+30,s:1.25,col:'#6a4a24'},{o:'pillar',x:1286,y:H+30,s:1.25,col:'#6a4a24'}],{dark:.5,darkc:'#140a04'})
});
window.PS={cutP,cutU,vg,shd,mix,hx,hex,lum,CC,puffs,blob,deck,cloudlets,sunburst,paperMandala,mandala,waves,peaks,ptree,ridgeP,stars,OBJ,drawLayers,FOGC,fogO};
})();
