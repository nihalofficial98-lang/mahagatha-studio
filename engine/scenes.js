/* ===== data-driven scenes: backgrounds, figures, effects — every event cued to a spoken word ===== */
const cuT=(P,i)=>cu(P,i);
const lerpO=(a,b,u)=>{const o={};const ks=new Set([...Object.keys(a||{}),...Object.keys(b||{})]);ks.forEach(k=>{const x=(a||{})[k]??0,y=(b||{})[k]??x;o[k]=lerp(x,y,u)});return o};
function ocean(t,y0,c1,c2,hi,gx){const g=ctx.createLinearGradient(0,y0,0,y0+520);g.addColorStop(0,c1);g.addColorStop(1,c2);ctx.fillStyle=g;ctx.fillRect(-400,y0,W+800,H+800);ctx.lineWidth=2;for(let i=0;i<9;i++){const yy=y0+8+i*i*3+i*5,amp=2+i*0.8;ctx.strokeStyle=`rgba(${hi},${0.05+i*0.02})`;ctx.beginPath();for(let x=-60;x<=W+60;x+=16){const y=yy+Math.sin(x*0.012*(1+i*0.1)+t*(0.7+i*0.08)+i*1.7)*amp;x===-60?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()}if(gx!=null){ctx.save();ctx.globalCompositeOperation='lighter';ctx.translate(gx,y0+50);ctx.scale(1,0.3);const gg=ctx.createRadialGradient(0,0,0,0,0,360);gg.addColorStop(0,`rgba(${hi},.35)`);gg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gg;ctx.fillRect(-360,-360,720,720);ctx.restore()}}
function starsF(t,n=90){const r=rng(5);ctx.fillStyle='#fff';for(let i=0;i<n;i++){const x=r()*W,y=r()*H*0.62;ctx.globalAlpha=(0.3+0.6*Math.abs(Math.sin(t*1.2+i)))*0.7;ctx.fillRect(x,y,1.6,1.6)}ctx.globalAlpha=1}
function moonAt(x,y,r,t){glow(x,y,r*8,'200,215,255',0.3);ctx.fillStyle='#f4f2ff';ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill();ctx.fillStyle='rgba(150,160,210,.3)';ctx.beginPath();ctx.arc(x-r*0.25,y-r*0.2,r*0.26,0,7);ctx.arc(x+r*0.35,y+r*0.3,r*0.18,0,7);ctx.fill()}
function mountainP(x,base,h,w,col,snow,a=1){if(h<=2)return;ctx.save();ctx.globalAlpha*=a;const g=ctx.createLinearGradient(x-w,0,x+w,0);g.addColorStop(0,col);g.addColorStop(1,'#10142a');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(x-w,base);ctx.lineTo(x-w*0.12,base-h);ctx.lineTo(x+w*0.12,base-h*0.98);ctx.lineTo(x+w,base);ctx.fill();if(snow){ctx.fillStyle='#e6ecfa';ctx.beginPath();ctx.moveTo(x-w*0.3,base-h*0.7);ctx.lineTo(x-w*0.12,base-h);ctx.lineTo(x+w*0.12,base-h*0.98);ctx.lineTo(x+w*0.32,base-h*0.7);ctx.lineTo(x+w*0.12,base-h*0.78);ctx.lineTo(x,base-h*0.68);ctx.lineTo(x-w*0.14,base-h*0.78);ctx.fill()}ctx.restore()}
function flamesF(x,y,s,t,n=8,c1='#ff5a1a',c2='#ffc24a'){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const ph=i*1.7,h=90+Math.sin(t*6+ph)*24+(i%3)*16,w=24,xx=(i-(n-1)/2)*22;[[c1,1],[c2,0.55]].forEach(([c,k])=>{ctx.fillStyle=c;ctx.globalAlpha=0.8;ctx.beginPath();ctx.moveTo(xx-w*k,0);ctx.quadraticCurveTo(xx-w*0.8*k+Math.sin(t*7+ph)*8,-h*0.6*k,xx+Math.sin(t*5+ph)*10,-h*k);ctx.quadraticCurveTo(xx+w*0.8*k+Math.sin(t*7+ph)*8,-h*0.6*k,xx+w*k,0);ctx.fill()})}ctx.restore()}
function shockF(x,y,u,rgb,max=900,sq=0.5){if(u<0||u>1)return;ctx.save();ctx.translate(x,y);ctx.scale(1,sq);ctx.strokeStyle=`rgba(${rgb},${0.8*(1-u)})`;ctx.lineWidth=10*(1-u)+2;ctx.beginPath();ctx.arc(0,0,u*max,0,7);ctx.stroke();ctx.restore()}
function boltF(x0,y0,x1,y1,seed,a=1,rgb='255,200,170'){const r=rng(seed);ctx.save();ctx.globalCompositeOperation='lighter';ctx.lineCap='round';[[12,0.25],[5,0.6],[2,1]].forEach(([w,al])=>{ctx.strokeStyle=`rgba(${rgb},${a*al})`;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(x0,y0);for(let i=1;i<=12;i++){const u=i/12;ctx.lineTo(lerp(x0,x1,u)+(r()-0.5)*70*(1-Math.abs(u-0.5)),lerp(y0,y1,u)+(r()-0.5)*14)}ctx.stroke()});ctx.restore()}
function pill(s,x,y,a,col='#ffe9b8',size=32){if(a<=0.01)return;ctx.save();ctx.globalAlpha*=clamp(a);ctx.font=`700 ${size}px NSer, serif`;const w=ctx.measureText(s).width+44,h=size*1.55,cx=clamp(x,70+w/2,W-70-w/2),cy=clamp(y,60,H-130);ctx.fillStyle='rgba(8,6,22,.58)';ctx.strokeStyle='rgba(255,220,150,.45)';ctx.lineWidth=1.5;ctx.beginPath();ctx.roundRect(cx-w/2,cy-h/2,w,h,h/2);ctx.fill();ctx.stroke();ctx.restore();stext(s,cx,cy+1,size,col,a,700,'center','rgba(255,210,140,.35)')}
function iconF(k,x,y,s,a,t){if(a<=0.01)return;ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.globalAlpha*=clamp(a);
  if(k==='asuras'){[[-1,'#6a5499'],[1,'#3f8a72']].forEach(([sd,c])=>{ctx.fillStyle=c;ctx.beginPath();ctx.arc(sd*34,-10,24,0,7);ctx.fill();ctx.fillRect(sd*34-20,12,40,46);ctx.fillStyle='#ece3c6';[-1,1].forEach(h=>{ctx.beginPath();ctx.moveTo(sd*34+h*16,-26);ctx.lineTo(sd*34+h*26,-58);ctx.lineTo(sd*34+h*4,-30);ctx.fill()})})}
  else if(k==='kids'){for(let i=0;i<4;i++){const xx=(i-1.5)*34;ctx.fillStyle=['#f4f1e8','#dfe9ff','#fff3c8','#eadfff'][i];ctx.beginPath();ctx.arc(xx,-18,12,0,7);ctx.fill();ctx.fillRect(xx-10,-4,20,42)}}
  else if(k==='trident'){ctx.strokeStyle='#e0b050';ctx.lineWidth=6;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(0,50);ctx.lineTo(0,-50);ctx.moveTo(-22,-50);ctx.lineTo(-22,-20);ctx.quadraticCurveTo(0,0,22,-20);ctx.lineTo(22,-50);ctx.stroke();glow(0,-20,60,'255,120,60',0.5)}
  else if(k==='person'){ctx.fillStyle='#f4efe0';ctx.beginPath();ctx.arc(0,-26,18,0,7);ctx.fill();ctx.fillRect(-18,-6,36,56);ctx.fillStyle='#1b1318';ctx.beginPath();ctx.arc(0,-40,10,0,7);ctx.fill()}
  else if(k==='heart'){ctx.fillStyle='#ff5a8a';ctx.beginPath();ctx.moveTo(0,28);ctx.bezierCurveTo(-52,-14,-26,-50,0,-22);ctx.bezierCurveTo(26,-50,52,-14,0,28);ctx.fill();glow(0,0,70,'255,90,140',0.5)}
  else if(k==='flame'){flamesF(0,40,0.55,t)}
  else if(k==='vortex'){ctx.strokeStyle='rgba(190,170,255,.9)';ctx.lineWidth=5;for(let i=0;i<4;i++){ctx.beginPath();for(let j=0;j<=30;j++){const r=j*3+i*8,an=j*0.45+t*2+i*1.6;ctx.lineTo(Math.cos(an)*r,Math.sin(an)*r*0.5)}ctx.stroke()}}
  else if(k==='vaikuntha'){glow(0,0,110,'255,235,160',0.6);ctx.fillStyle='#f6d870';[-48,-16,16,48].forEach(xx=>ctx.fillRect(xx-7,-30,14,60));ctx.beginPath();ctx.moveTo(-64,-30);ctx.lineTo(0,-62);ctx.lineTo(64,-30);ctx.fill()}
  else if(k==='body'){glow(0,0,90,'255,150,100',0.55);ctx.fillStyle='#ffb48a';ctx.beginPath();ctx.arc(0,0,34,0,7);ctx.fill()}
  else if(k==='light'){glow(0,0,100,'200,230,255',0.7);ctx.strokeStyle='#e8f4ff';ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,0,30,0,7);ctx.stroke()}
  else if(k==='ban'){ctx.strokeStyle='#ff4a4a';ctx.lineWidth=9;ctx.beginPath();ctx.arc(0,0,44,0,7);ctx.moveTo(-31,-31);ctx.lineTo(31,31);ctx.stroke()}
  else if(k==='cycle'){ctx.strokeStyle='#ffe2a0';ctx.lineWidth=8;ctx.beginPath();ctx.arc(0,0,48,0.4,5.9);ctx.stroke();ctx.fillStyle='#ffe2a0';ctx.beginPath();ctx.moveTo(40,-24);ctx.lineTo(62,-6);ctx.lineTo(34,-2);ctx.fill();glow(0,0,90,'255,226,160',0.4)}
  else if(k==='lotusI'){ctx.fillStyle='#f4a6c0';[-30,0,30].forEach(x=>{ctx.beginPath();ctx.ellipse(x,-10,16,34,x*0.02,0,7);ctx.fill()});glow(0,0,80,'255,220,230',0.4)}
  ctx.restore()}
/* ---------- backgrounds ---------- */
const AMB={light:'#9a6a46',mid:'#6e4630',dark:'#3a2218',speck1:'20,8,4',speck2:'255,200,140'},DUSKC={light:'#5a5a86',mid:'#3c3a62',dark:'#22203e',speck1:'10,8,28',speck2:'170,160,220'};
const BG={
 cel(S,t){const w=S.warm;skyG(w?['#241f58','#62609e','#c08aa0','#f2c8a0']:['#121842','#3a4486','#7c84c4','#b8bce8'],-300,H+300);glow(CX,340,520,w?'255,205,150':'215,220,255',0.45);layer(0.12,()=>{rays(CX,330,t,w?'255,225,170':'235,240,255',0.06);cloudBand('celA',11,CELC,40,5,t,0.9)});layer(0.3,()=>cloudBand('celB',23,CELC2,230,9,t,0.95));dust(t,60,5,'240,240,255',0.5,5);if(S.floor!==false)layer(0.9,()=>{cloudBand('celF',37,CELC,(S.fy||640)-40,14,t,1,1.2);skyG(['rgba(150,146,200,0)','rgba(70,64,130,.9)'],(S.fy||640)+60,H+400)})},
 storm(S,t){const r=S.r??1;skyG(['#0a0e1c','#1c2236','#3a3a52','#7a5a5a'],-300,H+300);layer(0.1,()=>cloudBand('stA',51,STC,20,7,t,0.95));layer(0.25,()=>cloudBand('stB',61,STC,200,12,t,0.9,1.1));if(r>0){ctx.save();ctx.globalAlpha=r;skyG(['#08020a','#2a0810','#6a1612','#d0482a'],-300,H+300);glow(CX,520,700,'255,90,40',0.5);layer(0.1,()=>cloudBand('srA',71,STR,20,7,t,0.95));layer(0.25,()=>cloudBand('srB',81,STR,200,12,t,0.9,1.1));ctx.restore()}layer(0.4,()=>ridge(600,90,4,r>0.5?'#2a0c10':'#1a1a2a','#0a0406'));embers(t,90,9,'255,120,40',2*r+0.2)},
 voidR(S,t){skyG(S.cols||['#050204','#1c0408','#4a0c0c'],-300,H+300);glow(S.gx||CX,S.gy||340,560,S.rgb||'255,60,30',0.45);embers(t,60,3,'255,110,40',2)},
 night(S,t){skyG(['#02030a','#0a1024','#141a3a'],-300,H+300);starsF(t);layer(0.2,()=>cloudBand('dkA',99,DUSKC,100,4,t,0.45));ocean(t,S.oy||540,'#0a1226','#02040a','120,140,200',S.og==null?CX:S.og)},
 dusk(S,t){skyG(['#1a1440','#4a3070','#c8625a','#f0a070'],-300,H+300);glow(CX,470,520,'255,190,130',0.5);ocean(t,520,'#2a2a62','#0a0a22','255,200,170',CX);dust(t,50,23,'255,200,150',0.5,4)},
 moon(S,t){skyG(['#050a1c','#101c3a','#24345a','#46608a'],-300,H+300);starsF(t);moonAt(W*0.78,170,34,t);layer(0.15,()=>cloudBand('mnA',91,STC,120,6,t,0.55));layer(0.4,()=>ridge(600,120,9,'#101a30','#05080e'))},
 palace(S,t){layer(0.7,()=>palace(t,S.po||{}))},
 dawn(S,t){skyG(['#1a2a6a','#6a7ab8','#f0a080','#ffe0a8'],-300,H+300);glow(CX,470,640,'255,215,160',0.55);rays(CX,470,t,'255,225,170',0.06);layer(0.15,()=>cloudBand('dwA',13,CELC2,60,6,t,0.9));layer(0.3,()=>ridge(540,60,6,'#4a4a7a','#1a1a38'))},
 amber(S,t){skyG(['#2a1808','#6a3a12','#b8701e','#e8a850'],-300,H+300);glow(CX,470,520,'255,190,110',0.35);rays(CX,470,t,'255,200,130',0.03);layer(0.2,()=>cloudBand('amA',19,AMB,80,5,t,0.55));const g=ctx.createLinearGradient(0,590,0,H+300);g.addColorStop(0,'#5a3a18');g.addColorStop(1,'#1a0c04');ctx.fillStyle=g;ctx.fillRect(-300,590,W+600,H);dust(t,55,83,'255,220,150',0.5,6)},
 cosmos(S,t){skyG(['#04030c','#120c2e','#2a1a52'],-300,H+300);const r=rng(3);for(let i=0;i<190;i++){const a=r()*6.283+t*(S.spin||0.05),rad=r()*620,x=CX+Math.cos(a+rad*0.008)*rad*1.5,y=360+Math.sin(a+rad*0.008)*rad*0.55;ctx.fillStyle=`rgba(255,255,255,${0.35+0.5*r()})`;ctx.beginPath();ctx.arc(x,y,0.8+r()*2,0,7);ctx.fill()}glow(CX,360,400,S.rgb||'160,120,255',0.25)},
 sea(S,t){skyG(['#04122e','#0a2a5a','#0e3a74'],-300,H+300);ctx.strokeStyle='rgba(120,190,255,.2)';ctx.lineWidth=2;for(let i=0;i<9;i++){ctx.beginPath();for(let x=0;x<=W;x+=20){const y=40+i*80+Math.sin(x*0.02+t+i)*8;x?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke()}},
 plain(S,t){skyG(S.cols||['#0a0610','#1c1020'],-300,H+300)},
 vista(S,t){ // coded depth landscape: sky, sun, four ridge layers at different parallax, haze, optional river and foreground trees
  const P=S.sky||['#1a2a6a','#6a7ab8','#f0a080','#ffe0a8'];skyG(P,-300,H+300);const sx=S.sx??CX*1.2,sy=S.sy??330;glow(sx,sy,S.sr||420,S.sun||'255,214,150',0.55);
  if(S.stars)starsF(t,70);
  layer(0.1,()=>cloudBand('vsC',S.seed||7,S.cl||{light:'#f6e8d8',mid:'#d8b8c0',dark:'#9a88a8'},S.cy??120,3,t,0.55));
  const rcols=S.ridge||['#7a86b4','#5a6a98','#3c4a78','#26305a'];
  rcols.forEach((col,i)=>{const par=[.18,.32,.52,.78][i],r=rng((S.seed||7)*13+i*29);layer(par,()=>{const base=300+i*70+(S.horizon||0),amp=[120,100,80,60][i]+(S.rough||0);
    ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(-500,H+300);let y=base;for(let x=-500;x<=W+500;x+=40){y=base-amp*(0.5+0.5*Math.sin(x*0.0045*(i+1)+i*2.1+(S.seed||7)))-r()*14;ctx.lineTo(x,y)}ctx.lineTo(W+500,H+300);ctx.closePath();ctx.fill();
    skyG(['rgba(255,236,210,0)',`rgba(${S.haze||'255,220,190'},${0.22-i*0.04})`],base-120,base+160)})});
  if(S.river){layer(0.6,()=>{ctx.fillStyle=S.river;ctx.beginPath();ctx.moveTo(CX-30,380);ctx.bezierCurveTo(CX-260,470,CX+240,520,CX-120,H+200);ctx.lineTo(CX+260,H+200);ctx.bezierCurveTo(CX+420,520,CX-30,470,CX+30,380);ctx.closePath();ctx.fill();ctx.globalAlpha=.25;ctx.fillStyle='#fff';for(let i=0;i<14;i++){ctx.fillRect(CX-60+Math.sin(t+i)*40+i*8,420+i*26,40+i*4,2)}ctx.globalAlpha=1})}
  if(S.ground)layer(0.9,()=>{skyG(S.ground,H-170,H+300);const r=rng(41);ctx.fillStyle=S.blade||'#1c3a24';for(let i=0;i<70;i++){const x=r()*W,h=14+r()*30;ctx.beginPath();ctx.moveTo(x-5,H-120);ctx.lineTo(x+Math.sin(t*1.5+i)*4,H-120-h);ctx.lineTo(x+5,H-120);ctx.fill()}});
  if(S.trees)layer(0.85,()=>{const r=rng(S.seed||9);S.trees.forEach((tx,i)=>{const h=190+r()*90,x=tx;ctx.fillStyle=S.trunk||'#2a1a14';ctx.fillRect(x-8,H-220,16,150);const c=S.leaf||['#1e4a30','#2a6a3c'];[[0,-h*.5,70],[-46,-h*.32,52],[46,-h*.32,52]].forEach(([dx,dy,rr],k)=>{ctx.fillStyle=c[k%2];ctx.beginPath();ctx.arc(x+dx+Math.sin(t*.8+i)*3,H-170+dy,rr,0,7);ctx.fill()})})});
  dust(t,S.dust??30,11,S.dustc||'255,230,190',0.5,5)},
 cloudscape(S,t){ // heaven / sky seen from above or among clouds: gradient, sun rays, three drifting cloud decks, light
  skyG(S.sky||['#2a3a86','#7a8ad0','#f0b8c0','#fff0d0'],-300,H+300);const sx=S.sx??CX,sy=S.sy??250;glow(sx,sy,560,S.sun||'255,236,190',0.6);
  ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<14;i++){const a=-1.1+i*0.17+Math.sin(t*.3+i)*.02;ctx.fillStyle=`rgba(${S.sun||'255,236,190'},${0.05+0.03*Math.sin(t*.7+i)})`;ctx.beginPath();ctx.moveTo(sx,sy);ctx.lineTo(sx+Math.sin(a-.05)*1400,sy+Math.cos(a-.05)*1400);ctx.lineTo(sx+Math.sin(a+.05)*1400,sy+Math.cos(a+.05)*1400);ctx.fill()}ctx.restore();
  layer(0.12,()=>cloudBand('csA',S.seed||21,S.c1||{light:'#fff4e8',mid:'#e8c8d0',dark:'#b098c0'},S.y1??80,2.5,t,0.8));
  layer(0.35,()=>cloudBand('csB',(S.seed||21)+5,S.c2||{light:'#ffe8d8',mid:'#d8a8c0',dark:'#9078b0'},S.y2??250,5,t,0.9));
  layer(0.7,()=>cloudBand('csC',(S.seed||21)+9,S.c3||{light:'#f0d8e8',mid:'#b890c0',dark:'#705098'},S.y3??430,9,t,1,1.15));
  dust(t,24,5,'255,240,210',0.45,4)},
 earth(S,t){ // underground cross-section: strata, roots, stones, glowing veins, a dug tunnel
  skyG(S.strata||['#5a3a24','#42281a','#2c1a12','#1a0e0a'],-300,H+300);const r=rng(17);
  layer(0.3,()=>{for(let i=0;i<46;i++){ctx.fillStyle=`rgba(${20+r()*40|0},${12+r()*20|0},8,${.25+r()*.25})`;ctx.beginPath();ctx.ellipse(r()*W,r()*H,30+r()*90,12+r()*28,r()*3,0,7);ctx.fill()}});
  layer(0.55,()=>{ctx.strokeStyle='rgba(120,80,40,.5)';ctx.lineWidth=5;for(let i=0;i<9;i++){ctx.beginPath();let x=r()*W,y=-40;ctx.moveTo(x,y);for(let k=0;k<7;k++){x+=(r()-.5)*70;y+=70+r()*30;ctx.lineTo(x,y)}ctx.stroke()}});
  layer(0.75,()=>{for(let i=0;i<10;i++){const x=r()*W,y=140+r()*500,s=18+r()*40;ctx.fillStyle='#6a5a52';ctx.beginPath();ctx.moveTo(x-s,y+s*.4);ctx.lineTo(x-s*.4,y-s*.6);ctx.lineTo(x+s*.7,y-s*.3);ctx.lineTo(x+s,y+s*.5);ctx.fill();ctx.fillStyle='rgba(255,255,255,.12)';ctx.fillRect(x-s*.4,y-s*.5,s*.5,4)}});
  glow(S.gx??CX,S.gy??520,420,S.gc||'255,150,60',0.35);dust(t,34,9,'255,170,90',0.5,-6)},
 pillar(S,t){ // an endless pillar of fire through the middle of a dark cosmos; optionally cracks open (S.ct = seconds into the shot)
  skyG(S.sky||['#05030c','#0e0a26','#2a1236'],-300,H+300);starsF(t,80);const x=S.px??CX,hw=S.pw??110,ck=S.ct!=null?clamp((t-S.ct)/1.2):0;
  glow(x,H/2,760,'255,150,60',0.35);
  layer(0.4,()=>{const g=ctx.createLinearGradient(x-hw,0,x+hw,0);g.addColorStop(0,'#a8300c');g.addColorStop(.3,'#ff9a30');g.addColorStop(.5,'#fff0b0');g.addColorStop(.7,'#ff9a30');g.addColorStop(1,'#a8300c');ctx.fillStyle=g;ctx.fillRect(x-hw,-500,hw*2,H+1000);
    ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<26;i++){const yy=((i*83+t*70)%(H+400))-200,w=hw*(.4+.5*Math.abs(Math.sin(i*1.7+t*2)));ctx.fillStyle='rgba(255,200,90,.22)';ctx.beginPath();ctx.ellipse(x+Math.sin(i*2.3+t*1.4)*hw*.5,yy,w*.5,40+i%5*10,0,0,7);ctx.fill()}ctx.restore();
    if(ck>0){const cw=hw*1.7*ck;skyG(['#2a0606','#8a1a08'],-500,H+500);ctx.save();ctx.beginPath();ctx.moveTo(x,-500);ctx.lineTo(x+cw*.5,H/2);ctx.lineTo(x,H+500);ctx.lineTo(x-cw*.5,H/2);ctx.closePath();ctx.clip();const cg=ctx.createRadialGradient(x,H/2,10,x,H/2,hw*2);cg.addColorStop(0,'#fff0c0');cg.addColorStop(1,'#a01808');ctx.fillStyle=cg;ctx.fillRect(x-hw*2,-500,hw*4,H+1000);ctx.restore()}});
  dust(t,60,13,'255,200,110',0.7,-14)},

};
/* ---------- figures ---------- */
function drawBoar(x,y,sc,t,f){ // Vishnu as Varaha, paper-cut: slate-blue body, bristle mane, ivory tusks, gold crown + necklace with the red Kaustubha; pose 'dig' (head down, front hoof scraping) | 'run'
  const {cutP,vg,shd}=window.PS,TAU=Math.PI*2;ctx.save();ctx.translate(x,y);ctx.scale(sc*(f.flip||1),sc);const dig=(f.pose||'dig')==='dig',bob=Math.sin(t*1.7)*2;
  const col='#4a5f98',colD='#2c3a66',colH='#7088c4',INKB='#141a30',o={lw:2.4,ink:INKB,blur:6,sy:3};
  ctx.fillStyle='rgba(0,0,0,.22)';ctx.beginPath();ctx.ellipse(0,4,130,13,0,0,TAU);ctx.fill();
  const leg=(lx,ph,front,far)=>{ctx.save();ctx.translate(lx,-66+bob);const a=(front&&dig?(.5+.5*Math.sin(t*9+ph))*-.9:Math.sin(t*6+ph)*.35);ctx.rotate(a);
    cutP(()=>{ctx.moveTo(-15,-6);ctx.quadraticCurveTo(-18,30,-10,58);ctx.lineTo(10,58);ctx.quadraticCurveTo(16,24,15,-6);ctx.closePath()},vg(-6,58,far?[colD,shd(colD,.8)]:[col,colD]),Object.assign({},o,{sh:0}));
    cutP(()=>{ctx.moveTo(-12,54);ctx.lineTo(12,54);ctx.lineTo(14,70);ctx.lineTo(1,66);ctx.lineTo(-14,70);ctx.closePath()},far?'#9a8c70':'#e8dcc0',{lw:1.6,ink:INKB,sh:0});
    cutP(()=>ctx.roundRect(-12,40,24,7,3),'#e6b84a',{lw:1.2,ink:INKB,sh:0});ctx.restore()};
  leg(-72,0,false,true);leg(52,1,true,true);
  // tail
  cutP(()=>{ctx.moveTo(-104,-100+bob);ctx.quadraticCurveTo(-146,-112+Math.sin(t*4)*8,-140,-70);ctx.quadraticCurveTo(-136,-62,-130,-72);ctx.quadraticCurveTo(-132,-100,-100,-90+bob);ctx.closePath()},colD,{lw:1.8,ink:INKB,sh:0});
  // body
  cutP(()=>ctx.ellipse(-4,-88+bob,108,56,0,0,TAU),vg(-150,-30,[colH,col,colD]),o);
  ctx.save();ctx.beginPath();ctx.ellipse(-4,-88+bob,108,56,0,0,TAU);ctx.clip();ctx.strokeStyle='rgba(20,26,60,.18)';ctx.lineWidth=2;for(let i=0;i<5;i++){ctx.beginPath();ctx.moveTo(-80+i*34,-124+bob);ctx.quadraticCurveTo(-72+i*34,-96+bob,-82+i*34,-66+bob);ctx.stroke()}
    ctx.fillStyle='rgba(255,255,255,.12)';ctx.beginPath();ctx.ellipse(-20,-118+bob,70,14,-.05,0,TAU);ctx.fill();ctx.restore();
  // bristle mane (one cut piece)
  cutP(()=>{ctx.moveTo(-92,-124+bob);for(let i=0;i<=14;i++){const bx=-92+i*13,lift=Math.abs(i-8)*1.8;ctx.lineTo(bx+6,-160+bob+lift*1.4+Math.sin(t*3+i)*3);ctx.lineTo(bx+13,-134+bob+lift)}ctx.quadraticCurveTo(40,-120+bob,-92,-124+bob);ctx.closePath()},vg(-165,-120,[shd(colD,1.3),colD,INKB]),{lw:1.8,ink:INKB,sh:0});
  leg(-40,2,false,false);leg(82,3,true,false);
  // gold necklace with the red gem
  ctx.save();ctx.lineCap='round';ctx.strokeStyle=INKB;ctx.lineWidth=9;ctx.beginPath();ctx.moveTo(48,-128+bob);ctx.quadraticCurveTo(76,-70,60,-40+bob);ctx.stroke();ctx.strokeStyle='#e6b84a';ctx.lineWidth=6;ctx.stroke();ctx.restore();
  cutP(()=>ctx.arc(70,-66+bob,7,0,TAU),'#e0302a',{lw:1.6,ink:INKB,sh:0});
  // head, lowered when digging
  ctx.save();ctx.translate(98,-92+bob+(dig?24:0));ctx.rotate(dig?.42:.05);
  cutP(()=>{ctx.moveTo(-30,-34);ctx.lineTo(-10,-70);ctx.lineTo(8,-32);ctx.closePath()},vg(-70,-30,[colH,colD]),{lw:1.8,ink:INKB,sh:0}); // ear
  cutP(()=>{ctx.moveTo(-40,-18);ctx.quadraticCurveTo(-30,-40,6,-36);ctx.quadraticCurveTo(50,-24,90,-4);ctx.lineTo(94,24);ctx.quadraticCurveTo(50,32,0,32);ctx.quadraticCurveTo(-40,30,-40,-18);ctx.closePath()},vg(-44,40,[colH,col,colD]),o);
  cutP(()=>ctx.ellipse(94,10,8,15,0,0,TAU),'#8a98c8',{lw:1.6,ink:INKB,sh:0});ctx.fillStyle='#0c1020';[-1,1].forEach(sd=>{ctx.beginPath();ctx.ellipse(95,10+sd*6,2.2,3,0,0,TAU);ctx.fill()});
  // tusks
  [[0,1],[1,-1]].forEach(([i])=>cutP(()=>{ctx.moveTo(54,24+i*3);ctx.bezierCurveTo(82,32+i*4,98,8,94,-26);ctx.bezierCurveTo(86,2,72,16,54,18+i*3);ctx.closePath()},vg(-26,30,['#ffffff','#f2e8cc','#c8b890']),{lw:1.6,ink:INKB,sh:0}));
  // eye (gold iris, gentle)
  cutP(()=>ctx.ellipse(16,-12,8,6.4,-.1,0,TAU),'#fff6dc',{lw:1.6,ink:INKB,sh:0});ctx.fillStyle='#d8a020';ctx.beginPath();ctx.arc(18,-12,4,0,TAU);ctx.fill();ctx.fillStyle='#10101c';ctx.beginPath();ctx.arc(18.6,-12,2,0,TAU);ctx.fill();
  ctx.strokeStyle=INKB;ctx.lineWidth=2.4;ctx.beginPath();ctx.moveTo(4,-22);ctx.quadraticCurveTo(16,-28,28,-20);ctx.stroke();
  // vaishnava tilak + small gold crown
  cutP(()=>{ctx.moveTo(30,-34);ctx.lineTo(34,-18);ctx.lineTo(38,-34);ctx.closePath()},'#fff4dc',{lw:1,ink:INKB,sh:0});ctx.fillStyle='#d0243a';ctx.fillRect(33,-30,2,10);
  cutP(()=>{ctx.moveTo(-26,-38);ctx.lineTo(-20,-62);ctx.lineTo(-10,-46);ctx.lineTo(0,-72);ctx.lineTo(10,-46);ctx.lineTo(20,-62);ctx.lineTo(26,-38);ctx.closePath()},vg(-72,-38,['#fff4c0','#f2c14e','#b87a1a']),{lw:1.8,ink:'#5a3200',sh:0});
  cutP(()=>ctx.arc(0,-50,3.4,0,TAU),'#18a57a',{lw:1,ink:'#5a3200',sh:0});
  ctx.restore();ctx.restore()}
function drawSwan(x,y,sc,t,f){ // Brahma as the Hamsa, paper-cut: white layered feathers, long S-neck, orange beak (tip at 210,-196), gold crown + red-gold neck band
  const {cutP,vg}=window.PS,TAU=Math.PI*2;ctx.save();ctx.translate(x,y);ctx.scale(sc*(f.flip||1),sc);if(f.rot)ctx.rotate(f.rot);const fl=Math.sin(t*5.2)*(f.glide?.3:1),bob=Math.sin(t*2.4)*5;
  const INKS='#4a5070',o={lw:2.2,ink:INKS,blur:8,sy:4};
  const wing=(back)=>{ctx.save();ctx.translate(-10,-96+bob);ctx.rotate((back?-.2:0)+fl*.55-(back?.3:.55));
    const c0=back?['#e6eaf6','#c4cae0','#9aa2c4']:['#ffffff','#eef1fb','#c8cee6'];
    for(let i=0;i<7;i++){const an=-2.66+i*.1,L=138-i*9;ctx.save();ctx.translate(-120+i*12,-50+i*4);ctx.rotate(an);cutP(()=>{ctx.moveTo(0,-13);ctx.quadraticCurveTo(L*.55,-20,L,-2);ctx.quadraticCurveTo(L*.7,16,0,13);ctx.closePath()},vg(-14,14,c0),{lw:1.6,ink:INKS,sh:0});ctx.strokeStyle='rgba(120,130,170,.5)';ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(4,0);ctx.lineTo(L*.9,0);ctx.stroke();ctx.restore()}
    cutP(()=>{ctx.moveTo(0,0);ctx.bezierCurveTo(-40,-96,-130,-138,-200,-104);ctx.bezierCurveTo(-170,-80,-150,-56,-124,-30);ctx.bezierCurveTo(-84,-30,-40,-16,0,0);ctx.closePath()},vg(-130,0,c0),o);
    ctx.save();ctx.beginPath();ctx.moveTo(0,0);ctx.bezierCurveTo(-40,-96,-130,-138,-200,-104);ctx.bezierCurveTo(-170,-80,-150,-56,-124,-30);ctx.bezierCurveTo(-84,-30,-40,-16,0,0);ctx.clip();
      ctx.strokeStyle='rgba(110,120,170,.45)';ctx.lineWidth=1.6;for(let r=0;r<3;r++)for(let i=0;i<7;i++){const cx=-30-i*24-r*8,cy=-24-r*22-i*6;ctx.beginPath();ctx.arc(cx,cy,11,.1,Math.PI-.1);ctx.stroke()}ctx.restore();
    ctx.restore()};
  wing(true);
  // neck: filled S-curve (sampled bezier, tapering), then the head
  const B=(u,p0,p1,p2,p3)=>{const v=1-u;return v*v*v*p0+3*v*v*u*p1+3*v*u*u*p2+u*u*u*p3};const L=[],Rr=[];
  for(let i=0;i<=20;i++){const u=i/20,px=B(u,58,112,98,140),py=B(u,-100,-122,-190,-196)+bob,dx=B(Math.min(1,u+.02),58,112,98,140)-B(Math.max(0,u-.02),58,112,98,140),dy=B(Math.min(1,u+.02),-100,-122,-190,-196)-B(Math.max(0,u-.02),-100,-122,-190,-196),d=Math.hypot(dx,dy)||1,w=15-u*4;L.push([px-dy/d*w,py+dx/d*w]);Rr.push([px+dy/d*w,py-dx/d*w])}
  cutP(()=>{L.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));Rr.reverse().forEach(p=>ctx.lineTo(p[0],p[1]));ctx.closePath()},vg(-200,-100,['#ffffff','#eef1fb']),{lw:2,ink:INKS,sh:0});
  // tail fan + body
  cutP(()=>{ctx.moveTo(-70,-96+bob);ctx.lineTo(-156,-78+bob);ctx.lineTo(-140,-70+bob);ctx.lineTo(-160,-62+bob);ctx.lineTo(-84,-66+bob);ctx.closePath()},vg(-100,-60,['#ffffff','#d8def0']),{lw:1.8,ink:INKS,sh:0});
  cutP(()=>ctx.ellipse(0,-86+bob,94,42,-.08,0,TAU),vg(-128,-44,['#ffffff','#f2f4fc','#c8cee6']),o);
  // red-gold neck band (Brahma's colours)
  ctx.save();ctx.translate(96,-136+bob);ctx.rotate(-.9);cutP(()=>ctx.roundRect(-16,-5,32,10,4),'#d23a2a',{lw:1.4,ink:'#5a1a10',sh:0});ctx.fillStyle='#f2c14e';ctx.fillRect(-16,-1,32,2.4);ctx.restore();
  cutP(()=>{ctx.moveTo(164,-206+bob);ctx.lineTo(212,-197+bob);ctx.lineTo(166,-185+bob);ctx.closePath()},vg(-206,-185,['#ffb048','#f0902a','#c8641a']),{lw:1.6,ink:'#6a3a10',sh:0});
  cutP(()=>ctx.ellipse(146,-198+bob,25,20,.2,0,TAU),vg(-218,-178,['#ffffff','#eef1fb']),{lw:2,ink:INKS,sh:0});
  cutP(()=>{ctx.moveTo(160,-210+bob);ctx.quadraticCurveTo(168,-198+bob,162,-188+bob);ctx.lineTo(168,-194+bob);ctx.closePath()},'#1a1018',{lw:0,sh:0});
  ctx.fillStyle='#1a1018';ctx.beginPath();ctx.arc(151,-204+bob,3.8,0,TAU);ctx.fill();ctx.fillStyle='#ffffff';ctx.beginPath();ctx.arc(152.2,-205.2+bob,1.3,0,TAU);ctx.fill();
  cutP(()=>{ctx.moveTo(130,-213+bob);ctx.lineTo(134,-236+bob);ctx.lineTo(142,-222+bob);ctx.lineTo(148,-242+bob);ctx.lineTo(154,-222+bob);ctx.lineTo(162,-234+bob);ctx.lineTo(162,-212+bob);ctx.closePath()},vg(-242,-212,['#fff4c0','#f2c14e','#b87a1a']),{lw:1.6,ink:'#5a3200',sh:0});
  cutP(()=>ctx.arc(148,-222+bob,2.6,0,TAU),'#d0243a',{lw:.8,ink:'#5a3200',sh:0});
  wing(false);
  ctx.restore()}

function drawKetaki(x,y,sc,t,f,M,P){ // the KETAKI flower as a speaking character: the paper ketaki (PFX.flower_petals) with a gentle face on its heart.
  // x,y = base of the flower; f.wither 0..1 or f.wc (cue) + f.wd: bracts brown and droop, face saddens; f.fall:1 petals drop; f.talk 0..1 moves the mouth.
  const w=240*sc,h=w*1.05,wi=f.wc!=null?q(P,t,f.wc,f.wd||1.5):(f.wither||0),PSX=window.PS,cutP=PSX.cutP,mix=PSX.mix,vg=PSX.vg;M=Object.assign({},M||{});
  if(wi>0){M.sad=Math.max(M.sad||0,wi);M.smile=(M.smile||0)*(1-wi);M.ly=Math.max(M.ly||0,wi*.6)}
  if(f.talk){const ts=t*11+(f.x||0);M.mouth=Math.max(M.mouth||0,f.talk*(.25+.45*Math.abs(Math.sin(ts))*Math.abs(Math.sin(ts*.37+1))))}
  ctx.save();ctx.translate(x,y);ctx.scale(f.flip||1,1);ctx.rotate(wi*.32);ctx.translate(0,-h*.25+wi*h*.06);
  window.PFX.flower_petals.f(w,t,{wither:wi,fall:f.fall,glow:f.glow},1,P);
  // face on the flower's heart (drawn in the same frame the ketaki uses: its base is at +h*.25)
  const fx=0,fy=h*.25-h*.4+Math.sin(t*1.2)*1.5,R=w*.145,an=(M.anger||0),sd=(M.sad||0),sp=(M.surp||0),sm=(M.smile||0),mo=(M.mouth||0),bl=Math.max(M.blink||0,((t*.41)%1)<.035?1:0);
  ctx.save();ctx.translate(fx,fy);ctx.rotate(Math.sin(t*1.2)*.04*(1-wi));
  cutP(()=>ctx.ellipse(0,0,R*.86,R,0,0,Math.PI*2),vg(-R,R,[mix('#fffaf0','#d8b890',wi),mix('#fbe8b0','#b89060',wi),mix('#efc870','#8a6a3a',wi)]),{blur:5,sy:2,lw:1.8});
  ctx.strokeStyle=`rgba(200,150,50,${.55*(1-wi*.5)})`;ctx.lineWidth=1.6;ctx.beginPath();ctx.ellipse(0,0,R*.74,R*.88,0,0,Math.PI*2);ctx.stroke();
  // cheeks
  ctx.fillStyle=`rgba(240,120,110,${.22*(1-wi)})`;[-1,1].forEach(s2=>{ctx.beginPath();ctx.ellipse(s2*R*.46,R*.26,R*.15,R*.09,0,0,Math.PI*2);ctx.fill()});
  // eyes (almond), irises look by lx/ly
  const ex=R*.33,ey=-R*.06,ew=R*.22,eh=R*(.13+sp*.09)*(1-bl*.92)*(1-sd*.25);
  [-1,1].forEach(s2=>{ctx.save();ctx.translate(s2*ex,ey);ctx.fillStyle='#fffdf6';ctx.beginPath();ctx.moveTo(-ew,0);ctx.quadraticCurveTo(0,-eh*2,ew,0);ctx.quadraticCurveTo(0,eh*1.4,-ew,0);ctx.fill();
    if(eh>1){ctx.save();ctx.clip();ctx.fillStyle=an>.5?'#c81e1e':'#3a2414';ctx.beginPath();ctx.arc((M.lx||0)*ew*.4,(M.ly||0)*eh*.5,eh*.95,0,Math.PI*2);ctx.fill();ctx.fillStyle='#120a08';ctx.beginPath();ctx.arc((M.lx||0)*ew*.4,(M.ly||0)*eh*.5,eh*.45,0,Math.PI*2);ctx.fill();ctx.restore()}
    ctx.strokeStyle='#3a2014';ctx.lineWidth=2;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-ew,0);ctx.quadraticCurveTo(0,-eh*2,ew,0);ctx.stroke();
    // brow: anger pulls the inner end down, sadness lifts it
    const bi=-R*.27+an*R*.15-sd*R*.08-sp*R*.06,bo=-R*.27-sp*R*.06+sd*R*.06+an*R*.02;ctx.strokeStyle='#6a4020';ctx.lineWidth=2+an*1.6;ctx.beginPath();ctx.moveTo(-s2*ew*.15,bi);ctx.quadraticCurveTo(s2*ew*.5,Math.min(bi,bo)-R*.07*(1-an),s2*ew*1.1,bo);ctx.stroke();ctx.restore()});
  ctx.fillStyle='#d0243a';ctx.beginPath();ctx.arc(0,-R*.34,R*.045,0,Math.PI*2);ctx.fill();
  // tear when sad
  if(sd>.5){ctx.fillStyle='rgba(170,215,255,.9)';ctx.beginPath();const tx=ex*.9,ty=ey+R*.16+((t*.6)%1)*R*.3;ctx.moveTo(tx,ty-5);ctx.quadraticCurveTo(tx+4,ty+2,tx,ty+5);ctx.quadraticCurveTo(tx-4,ty+2,tx,ty-5);ctx.fill()}
  // mouth: smile curve, frown, or open
  const my=R*.36,mw=R*(.2+sm*.08-sp*.06),cv=(sm*.9-sd*.8-an*.6)*R*.16,op=Math.max(mo,sp*.7)*R*.3;
  if(op>1.2){ctx.fillStyle='#7a2a2a';ctx.beginPath();ctx.ellipse(0,my+op*.3,mw*.55,op,0,0,Math.PI*2);ctx.fill()}
  ctx.strokeStyle='#a03a3a';ctx.lineWidth=2.4;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-mw,my-cv*.3);ctx.quadraticCurveTo(0,my+cv,mw,my-cv*.3);ctx.stroke();
  ctx.restore();ctx.restore()}

/* emotion presets (face): f.emo or acts[i].emo; explicit mood values override */
const EMO={calm:{smile:.3},joy:{smile:1,surp:.15},anger:{anger:1,smile:0},rage:{anger:1,mouth:.35},sad:{sad:1,ly:.45},grief:{sad:1,ly:.7,mouth:.2},surprise:{surp:1,mouth:.45},fear:{surp:.7,sad:.4,mouth:.25},shame:{sad:.7,ly:.95,lx:.3},pride:{smile:.55,ly:-.3},doubt:{sad:.35,lx:.6,smile:0},devotion:{smile:.45,ly:-.5,blink:.35}};
function drawWho(f,t,P){const a=(f.ac!=null?q(P,t,f.ac,f.ad||0.5):(f.a??1))*(f.fo!=null?1-q(P,t,f.fo,f.fd||1.2):1);if(a<=0.01)return;const ex=f.exprB?lerpO(f.expr,f.exprB,q(P,t,f.ec,0.4)):(f.expr||{});
  let WK=f.walk||0,WX=0;if(f.walkTo){const W2=f.walkTo,d2=W2.d||Math.abs(W2.x-f.x)/(W2.v||120),m=clamp((t-cuT(P,W2.c||0))/Math.max(.1,d2));WX=(W2.x-f.x)*m;if(m>0&&m<1)WK=W2.sp||1}
  const x=f.x+(f.vx||0)*t+WX,y=f.y+(f.vy||0)*t,s=f.s*(1+(f.ds||0)*t);ctx.save();ctx.globalAlpha*=a;if(f.mx||f.my){const m=q(P,t,f.mc||0,f.md||1.2);ctx.translate((f.mx||0)*m,(f.my||0)*m)}
  if(f.bow){const bb=q(P,t,f.bc||0,f.bd||0.8);ctx.translate(x,y);ctx.rotate(f.bow*bb);ctx.translate(-x,-y)}
  if(f.kneel){const kk=q(P,t,f.kc||0,f.kd||0.6)*f.kneel;ctx.translate(x,y);ctx.scale(1,1-kk*0.3);ctx.translate(-x,-y)}
  let HD=null;if(f.hd){HD={};['l','r','t','b'].forEach(k=>{const v=f.hd[k];HD[k]=v==null?0:(typeof v==='number'?v:q(P,t,v.c||0,v.d||0.7))})}
  if(f.dark!=null)ctx.filter=`brightness(${f.dark})`;
  const o={pose:f.pose||'stand',expr:ex,flip:f.flip||1,key:f.key||'255,214,160',rim:f.rim||'rgba(255,238,210,.95)',lx:f.lx??-1,tail:f.tail!==false};
  if(f.aura)glow(x,y-130*s,240*s,f.aura,0.26);
  if(f.turnc!=null){const u=q(P,t,f.turnc,f.turnd||.5),sx=Math.cos(u*Math.PI);ctx.translate(x,0);ctx.scale(Math.abs(sx)<.05?.05*Math.sign(sx||1):sx,1);ctx.translate(-x,0)}
  if(V2.has(f.who)){let PO=f.pose,MOOD=Object.assign({},EMO[f.emo]||{},f.mood||{}),TILT=f.tilt||0;
    if(f.acts||WK){PO=JSON.parse(JSON.stringify(V2.poseOf(f.pose||'stand',f.who)));
      (f.acts||[]).forEach(a=>{let u=q(P,t,a.c||0,a.d||.6);if(u<=0)return;if(a.emo)a=Object.assign({},a,{mood:Object.assign({},EMO[a.emo],a.mood||{})});if(a.e==='spring'&&u<1){u=1-Math.exp(-5.5*u)*Math.cos(9*u)}else if(a.e==='antic'&&u<1){u=u<.22?-.12*Math.sin(u/.22*3.14):(u-.22)/.78*1.0;u=Math.max(-.12,u)}if(a.pose)PO=V2.mixPose(PO,V2.poseOf(a.pose,f.who),u);
        if(a.mood)for(const k in a.mood)MOOD[k]=(MOOD[k]||0)+(a.mood[k]-(MOOD[k]||0))*u;if(a.tilt!=null)TILT+=(a.tilt-TILT)*u});
      if(WK){const w=Math.sin(t*4.2*WK),w2=Math.sin(t*4.2*WK+Math.PI),lift=a=>Math.max(0,a)*26;
        PO.fL[0]+=w*34;PO.fL[1]-=lift(w);PO.fR[0]+=w2*34;PO.fR[1]-=lift(w2);PO.kL[0]+=w*20;PO.kL[1]-=lift(w)*.8;PO.kR[0]+=w2*20;PO.kR[1]-=lift(w2)*.8;
        PO.hL[0]+=w2*26;PO.hR[0]+=w*26;PO.hd[1]-=Math.abs(w)*3;PO.ch[1]-=Math.abs(w)*3}}
    if((o.flip||1)<0){if(MOOD.lx)MOOD.lx=-MOOD.lx;TILT=-TILT}
    if(f.talk){const ts=t*11+(f.x||0);MOOD.mouth=Math.max(MOOD.mouth||0,f.talk*(.25+.45*Math.abs(Math.sin(ts))*Math.abs(Math.sin(ts*.37+1))));TILT+=Math.sin(t*1.9)*.025*f.talk}
    const vo={pose:PO,expr:ex,flip:o.flip,key:o.key,rim:o.rim,lx:o.lx,k:f.k,prop:f.prop,imp:f.imp,hd:HD,mood:MOOD,tilt:TILT,lotus:f.lotus,halo:f.halo};
    if(f.head)V2.head(f.who,x,y,s,t,vo);else V2.fig(f.who,x,y,s,t,vo)}
  else if(f.who==='brahma')drawBrahma(x,y,s,t,{aura:null,expr:ex,key:o.key,rim:o.rim,lx:o.lx,lotus:f.lotus!==false});
  else if(f.who==='boar')drawBoar(x,y,s,t,f);
  else if(f.who==='swan')drawSwan(x,y,s,t,f);
  else if(f.who==='ketaki'){const MO=Object.assign({},EMO[f.emo]||{},f.mood||{});(f.acts||[]).forEach(a=>{const u=q(P,t,a.c||0,a.d||.6);if(u<=0)return;const am=Object.assign({},EMO[a.emo]||{},a.mood||{});for(const k in am)MO[k]=(MO[k]||0)+(am[k]-(MO[k]||0))*u});drawKetaki(x,y,s,t,f,MO,P)}
  else if(f.who==='bull'){const b0=f.la0||[1,1,1,1],la=[b0[0],b0[1]*(f.l1==null?1:1-q(P,t,f.l1,0.9)),b0[2]*(f.l2==null?1:1-q(P,t,f.l2,0.9)),b0[3]*(f.l3==null?1:1-q(P,t,f.l3,0.9))];drawBull(x,y,s,t,{key:o.key,rim:o.rim,la:la,bow:(f.bow||0)*q(P,t,f.bc,1.2)})}
  else if(f.head)drawHead(CH[f.who],x,y,s,t,{key:o.key,rim:o.rim,lx:o.lx,expr:ex});
  else drawFig(CH[f.who],x,y,s,t,o);
  ctx.restore()}
/* ---------- effects ---------- */
const FXV2={};
function drawFx(F,t,P,d){try{drawFx0(F,t,P,d)}catch(e){(window.FX_ERRORS=window.FX_ERRORS||[]);const m=(F&&F.t)+': '+e.message;if(window.FX_ERRORS.indexOf(m)<0)window.FX_ERRORS.push(m)}}
function drawFx0(F,t,P,d){const a=F.c!=null?q(P,t,F.c,F.d||0.5):(F.a??1),k=F.t;if(a<=0.005&&k!=='orbs'&&k!=='shock')return;if(FXV2[k]){FXV2[k](F,t,P,d,a);return}
  if(k==='text')stext(F.s,F.x,F.y,F.size||50,F.col||'#ffe9b8',a*(F.fade!=null?1-q(P,t,F.fade,0.5):1),F.w||700,'center',F.glow);
  else if(k==='name')pill(F.s,F.x,F.y,a*(F.fade!=null?1-q(P,t,F.fade,0.5):1),F.col,F.size||32);
  else if(k==='flames'){ctx.save();ctx.globalAlpha*=a;flamesF(F.x,F.y,F.sc||1,t,F.n||8,F.c1,F.c2);ctx.restore()}
  else if(k==='glow')glow(F.x,F.y,(F.r||200)*(F.grow?0.4+0.6*a:1),F.rgb||'255,220,160',(F.ga??0.5)*a*(F.pulse?0.8+0.2*Math.sin(t*4):1));
  else if(k==='shock'){const t0=F.c!=null?cuT(P,F.c):F.at||0;shockF(F.x,F.y,(t-t0)/1.4,F.rgb||'255,170,100',F.max||900,F.sq||0.5)}
  else if(k==='bolt'){const t0=F.c!=null?cuT(P,F.c):F.at||0,fl=Math.max(0,1-Math.abs(t-t0)/(F.w||0.3));if(fl>0){boltF(F.x0,F.y0,F.x1,F.y1,Math.floor(t*12),fl,F.rgb);if(F.flash){ctx.fillStyle=`rgba(255,210,180,${0.35*fl})`;ctx.fillRect(0,0,W,H)}}}
  else if(k==='flash'){const t0=F.c!=null?cuT(P,F.c):F.at||0,fl=Math.max(0,1-Math.abs(t-t0)/(F.w||0.25));if(fl>0){ctx.fillStyle=`rgba(${F.rgb||'255,230,210'},${(F.ga??0.6)*fl})`;ctx.fillRect(0,0,W,H)}}
  else if(k==='beam'){ctx.save();ctx.globalCompositeOperation='lighter';const g=ctx.createLinearGradient(F.x,F.y,F.x,F.y-F.len);g.addColorStop(0,`rgba(255,230,170,${a})`);g.addColorStop(1,'rgba(255,70,20,0)');ctx.fillStyle=g;ctx.fillRect(F.x-(F.w||26)*a,F.y-F.len,(F.w||26)*2*a,F.len);ctx.restore();glow(F.x,F.y,160*a,'255,210,150',0.8*a)}
  else if(k==='threads'){ctx.save();ctx.globalCompositeOperation='lighter';ctx.strokeStyle=`rgba(${F.rgb||'255,240,210'},${0.55*a})`;ctx.lineWidth=2.5;F.to.forEach(([x,y])=>{ctx.beginPath();ctx.moveTo(F.x,F.y);ctx.quadraticCurveTo((F.x+x)/2,F.y+(y-F.y)*0.5+(F.bend||0),x,y);ctx.stroke()});ctx.restore()}
  else if(k==='orbs'){F.items.forEach((it,i)=>{const t0=cuT(P,it.c),u=ease((t-t0)/(it.dur||1.2));if(u<=0)return;const x=lerp(it.x0,it.x1,u),y=lerp(it.y0,it.y1,u)-Math.sin(u*3.14)*(it.arc||40);glow(x,y,it.r||70,it.rgb||'255,255,255',0.9*(it.keep?1:Math.min(1,2-2*u)));ctx.fillStyle=`rgb(${it.rgb||'255,255,255'})`;ctx.beginPath();ctx.arc(x,y,it.sz||7,0,7);ctx.fill()})}
  else if(k==='tears'){for(let i=0;i<5;i++){const u=mod(t*0.7+i*0.2,1);ctx.fillStyle=`rgba(190,220,255,${0.9*(1-u)*a})`;ctx.beginPath();ctx.ellipse(F.x+(i%2?F.dx:-F.dx),F.y+u*F.len,3.5,6,0,0,7);ctx.fill()}}
  else if(k==='petals'){for(let i=0;i<F.n;i++){const st=cuT(P,F.c)+i*0.22,u=clamp((t-st)/1.8);if(u<=0)continue;ctx.fillStyle=`rgba(${230-i*3},120,160,${1-u})`;ctx.save();ctx.translate(F.x+(i-F.n/2)*F.sp+Math.sin(u*6+i)*20,F.y+u*F.len);ctx.rotate(u*3+i);ctx.beginPath();ctx.ellipse(0,0,14,6,0,0,7);ctx.fill();ctx.restore()}}
  else if(k==='ribbon'){const t0=cuT(P,F.c),u=ease((t-t0)/(F.dur||1.3));if(u<=0)return;ctx.save();ctx.globalCompositeOperation='lighter';ctx.lineCap='round';for(let j=0;j<5;j++){ctx.strokeStyle=`rgba(${F.rgb||'120,20,150'},${0.75*(1-j*0.14)})`;ctx.lineWidth=30-j*5;ctx.beginPath();for(let i=0;i<=40;i++){const v=i/40*Math.max(0.1,u),x=lerp(F.x0,F.x1,v),y=lerp(F.y0,F.y1,v)+Math.sin(v*13+t*8+j)*30*(1-v*0.3);i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke()}ctx.restore()}
  else if(k==='arrow'){const t0=cuT(P,F.c),u=ease((t-t0)/0.8);if(u<=0)return;ctx.save();ctx.strokeStyle=F.col;ctx.fillStyle=F.col;ctx.lineWidth=9;ctx.beginPath();ctx.moveTo(F.x0,F.y);ctx.lineTo(lerp(F.x0,F.x1,u),F.y);ctx.stroke();const dr=Math.sign(F.x1-F.x0),xe=lerp(F.x0,F.x1,u);ctx.beginPath();ctx.moveTo(xe+dr*26,F.y);ctx.lineTo(xe,F.y-20);ctx.lineTo(xe,F.y+20);ctx.fill();ctx.restore()}
  else if(k==='crack'){ctx.save();ctx.strokeStyle=`rgba(255,80,50,${a})`;ctx.lineWidth=6;ctx.beginPath();const r=rng(7);ctx.moveTo(F.x,0);for(let i=1;i<=7;i++)ctx.lineTo(F.x+(r()-0.5)*90*a,i*62*a);ctx.stroke();ctx.restore();glow(F.x,200,260,'255,60,30',0.4*a)}
  else if(k==='frost'){ctx.fillStyle=`rgba(190,225,255,${0.28*a})`;ctx.fillRect(0,0,W,H);ctx.save();ctx.strokeStyle=`rgba(225,242,255,${0.9*a})`;ctx.lineWidth=3;for(let i=0;i<16;i++){const an=i*0.4;ctx.beginPath();ctx.moveTo(F.x+Math.cos(an)*150,F.y+Math.sin(an)*140);ctx.lineTo(F.x+Math.cos(an)*(150+44*a),F.y+Math.sin(an)*(140+40*a));ctx.stroke()}ctx.restore()}
  else if(k==='outline')humanOutline(F.x,F.y,F.sc||1,t,F.rgb||'255,230,180',a);
  else if(k==='icon')iconF(F.i,F.x,F.y,F.sc||1,a,t);
  else if(k==='dim'){ctx.fillStyle=`rgba(${F.rgb||'0,0,10'},${(F.ga??0.45)*a})`;ctx.fillRect(0,0,W,H)}
  else if(k==='sparkle'){ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<(F.n||24);i++){const an=i*0.5+t,x=F.x+Math.cos(an)*(F.rx||220),y=F.y+Math.sin(an*1.3+i)*(F.ry||120);ctx.fillStyle=`rgba(255,250,210,${0.8*a})`;ctx.beginPath();ctx.arc(x,y,3,0,7);ctx.fill()}ctx.restore()}
  else if(k==='infinity'){ctx.save();ctx.globalAlpha*=a;ctx.strokeStyle='#ffd980';ctx.lineWidth=9;ctx.beginPath();for(let i=0;i<=60;i++){const an=i/60*6.283,x=F.x+Math.cos(an)*120/(1+Math.sin(an)**2),y=F.y+Math.sin(an)*Math.cos(an)*120/(1+Math.sin(an)**2);i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke();ctx.restore();glow(F.x,F.y,160,'255,217,128',0.5*a)}
  else if(k==='scales'){ctx.save();ctx.globalAlpha*=a;ctx.translate(F.x,F.y);ctx.strokeStyle='#ffe2a0';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(-250,-40);ctx.lineTo(250,-40);ctx.moveTo(0,-40);ctx.lineTo(0,150);ctx.stroke();[-1,1].forEach(sd=>{ctx.beginPath();ctx.arc(sd*250,60,70,0,3.14);ctx.stroke();ctx.beginPath();ctx.moveTo(sd*250-70,60);ctx.lineTo(sd*250,-40);ctx.lineTo(sd*250+70,60);ctx.stroke()});ctx.restore();iconF('flame',F.x-250,F.y-10,1.2,a,t);iconF('lotusI',F.x+250,F.y-10,1.2,a,t)}
}
SHOTS.scene=function(t,d,P){const S=P.sc;if(S.bg)BG[S.bg.k](S.bg,t);
  layer(1,()=>(S.fxb||[]).forEach(F=>drawFx(F,t,P,d)));
  const order=S.figs||[];layer(S.depth??1,()=>order.forEach(f=>drawWho(f,t,P)));
  if(S.cfl)layer(0.9,()=>{cloudBand('celF',37,CELC,S.cfl-40,14,t,1,1.2);skyG(['rgba(150,146,200,0)','rgba(70,64,130,.9)'],S.cfl+60,H+400)});
  const SCR={text:1,dim:1,flash:1};layer(1,()=>(S.fx||[]).forEach(F=>{if(!SCR[F.t])drawFx(F,t,P,d)}));(S.fx||[]).forEach(F=>{if(SCR[F.t])drawFx(F,t,P,d)})};
/* ---------- special scenes ---------- */
SHOTS.tower=function(t,d,P){const S=P.sc;skyG(['#05040f','#120c2e','#1a1038'],-300,H+300);starsF(t,80);
  const B=[[0,400,['#fff0b0','#f6c860'],'वैकुंठ',S.cv],[400,800,['#6ab0ff','#2a5ab0'],'स्वर्गलोक',S.c1],[800,1200,['#7ac060','#2a7a3a'],'भूलोक',S.c2],[1200,1400,['#6a3a5a','#4a2a4a'],'अतल',S.c3],[1400,1600,['#5a2a4a','#3a1a3a'],'वितल',S.c4],[1600,1800,['#4a1a3a','#2a1030'],'सुतल',S.c5],[1800,2000,['#2a0a22','#12040e'],'पाताल',S.c6]];
  const key=S.pan.map(([c,y])=>[c==null?0:cuT(P,c),y]);let cy=key[key.length-1][1];for(let i=0;i<key.length-1;i++){if(t<key[i+1][0]){cy=lerp(key[i][1],key[i+1][1],ease((t-key[i][0])/Math.max(0.01,key[i+1][0]-key[i][0])));break}}
  ctx.save();ctx.translate(0,H/2-cy);B.forEach(([y0,y1,c,n,ci])=>{const act=ci==null?1:q(P,t,ci,0.7),al=0.28+0.72*act;ctx.save();ctx.globalAlpha=al;const g=ctx.createLinearGradient(0,y0,0,y1);g.addColorStop(0,c[0]);g.addColorStop(1,c[1]);ctx.fillStyle=g;ctx.fillRect(120,y0+6,W-240,y1-y0-12);
    if(n==='वैकुंठ'){ctx.fillStyle='rgba(255,255,255,.5)';[-3,-2,-1,0,1,2,3].forEach(k=>ctx.fillRect(CX+k*130-10,y0+60,20,260))}if(n==='भूलोक'){for(let i=0;i<7;i++)tree(SYM2(i,7,150),y1-30,t,i)}if(n==='स्वर्गलोक'){for(let i=0;i<5;i++){ctx.fillStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.ellipse(SYM2(i,5,200)+Math.sin(t*0.6+i)*14,y0+250,90,22,0,0,7);ctx.fill()}}
    if(act>0.5){ctx.strokeStyle='rgba(255,226,160,.9)';ctx.lineWidth=5;ctx.strokeRect(120,y0+6,W-240,y1-y0-12);glow(CX,(y0+y1)/2,300,'255,226,160',0.25)}ctx.restore()});ctx.restore();
  B.forEach(([y0,y1,c,n,ci])=>{const sy=(y0+y1)/2-cy+H/2;if(sy>-40&&sy<H+40)stext(n,CX,sy,56,'#fff6d8',0.4+0.6*(ci==null?1:q(P,t,ci,0.7)),700)});dust(t,40,19,'255,230,180',0.5,10)};
const SYM2=(i,n,sp)=>CX+(i-(n-1)/2)*sp;
function tree(x,y,t,i){ctx.save();ctx.translate(x,y);ctx.fillStyle='#3a2a20';ctx.fillRect(-5,-60,10,60);[['#103a1c',0],['#1b5a2b',-6],['#2f8a3c',-12]].forEach(([c,dy],k)=>{ctx.fillStyle=c;ctx.beginPath();ctx.arc(Math.sin(t*0.8+i)*2,-80+dy,32-k*5,0,7);ctx.fill()});ctx.fillStyle=i%2?'#e8452a':'#f08a35';for(let k=0;k<6;k++){ctx.beginPath();ctx.arc(Math.sin(k*2+i)*20,-80+Math.cos(k*3)*16,2.8,0,7);ctx.fill()}ctx.restore()}
SHOTS.earth=function(t,d,P){const S=P.sc;BG.dawn({},t);const rise=q(P,t,0,2.0),gy=lerp(800,560,rise);layer(0.6,()=>{ctx.fillStyle='#3a6a3a';ctx.fillRect(-400,gy,W+800,500);ctx.fillStyle='#2a5a34';for(let i=0;i<16;i++){ctx.beginPath();ctx.ellipse(i*90,gy+22+(i%3)*8,100,16,0,0,7);ctx.fill()}if(rise<1){ctx.strokeStyle=`rgba(255,160,80,${1-rise})`;ctx.lineWidth=3;for(let i=0;i<8;i++){const x=SYM2(i,8,150);ctx.beginPath();ctx.moveTo(x,gy);ctx.lineTo(x+8,gy+60);ctx.stroke()}}
  (S.mts||[]).forEach(([n,c,x,h,col,wd],i)=>{const u=q(P,t,c,1.0);mountainP(x,gy,h*u,wd||190,col,true);if(n)pill(n,x,gy-h*u-30,u,'#fff0c8',30)});
  if(S.trees){for(let i=0;i<12;i++){const u=q(P,t,S.trees,0.4+i*0.05);if(u>0){ctx.save();ctx.globalAlpha=u;tree(60+i*105,gy+70+(i%4)*24,t,i);ctx.restore()}}}});
  (S.fx||[]).forEach(F=>drawFx(F,t,P,d))};
SHOTS.map=function(t,d,P){const S=P.sc;BG.sea({},t);const I=[[CX,330,1.4,'जंबूद्वीप',S.c[0]],[CX-190,180,1.0,'कुशद्वीप',S.c[1]],[CX+190,180,1.0,'पुष्करद्वीप',S.c[2]],[CX-380,330,0.9,'',S.c[3]],[CX+380,330,0.9,'',S.c[3]+0.3],[CX-190,480,0.9,'',S.c[3]+0.6],[CX+190,480,0.9,'',S.c[3]+0.9]];
  const rv=S.rv!=null?q(P,t,S.rv,0.8):0;if(rv>0){ctx.save();ctx.strokeStyle=`rgba(150,215,255,${0.9*rv})`;ctx.lineWidth=5;ctx.lineCap='round';ctx.setLineDash([16,12]);ctx.lineDashOffset=-t*50;I.slice(1).forEach(([x,y])=>{ctx.beginPath();ctx.moveTo(CX,330);ctx.quadraticCurveTo((CX+x)/2,(330+y)/2+20,x,y);ctx.stroke()});ctx.restore()}
  I.forEach(([x,y,s,n,c],i)=>{const a=i<3?q(P,t,c,0.6):ease((t-(cuT(P,S.c[2])+0.7+(i-3)*0.3))/0.6);if(a<=0)return;ctx.save();ctx.globalAlpha=a;glow(x,y,150*s,'255,215,120',0.45);ctx.fillStyle='#4a8a3a';ctx.strokeStyle='#e8d890';ctx.lineWidth=4;ctx.beginPath();ctx.ellipse(x,y,100*s,56*s,0,0,7);ctx.fill();ctx.stroke();ctx.restore();if(n)pill(n,x,y,a,'#fff4d0',30)});
  if(S.sw!=null)shockF(CX,330,(t-cuT(P,S.sw))/1.4,'150,200,255',700);
  if(S.bloom!=null){const tr=rng(5);I.forEach(([x,y,s],i)=>{for(let j=0;j<12;j++){const px=x+(tr()-0.5)*170*s,py=y+(tr()-0.5)*80*s,u=ease((t-cuT(P,S.bloom)-(i*12+j)*0.035)/0.3);if(u>0){ctx.fillStyle=j%3?'#2f8a3c':'#f08ab0';ctx.beginPath();ctx.arc(px,py,4+4*u*(j%3?1:0.6),0,7);ctx.fill()}}})}
  (S.fx||[]).forEach(F=>drawFx(F,t,P,d))};
SHOTS.pillars=function(t,d,P){const S=P.sc;skyG(['#05040f','#0e0a24','#1a1038'],-300,H+300);starsF(t);const C=[['#f4f6ff','सतयुग'],['#ff5a4a','त्रेतायुग'],['#ffd23a','द्वापरयुग'],['#6a6a88','कलियुग']],rg=S.ring!=null?q(P,t,S.ring,1.8):0;
  C.forEach(([c,n],i)=>{const ci=S.pc[i],u=ci==null?(S.pre>i?1:0):q(P,t,ci,0.9);if(u<=0)return;const ang=i*1.5708+Math.PI/4+t*0.45*rg,x=lerp(SYM2(i,4,300),CX+Math.cos(ang)*300,rg),yb=lerp(600,H/2+60+Math.sin(ang)*105,rg),h=360*u*(1-rg*0.7);ctx.save();glow(x,yb-h/2,200,i===3?'140,120,200':'255,240,200',0.4*u);const g=ctx.createLinearGradient(0,yb-h,0,yb);g.addColorStop(0,c);g.addColorStop(1,'#222234');ctx.fillStyle=g;ctx.shadowColor=i===3?'rgba(170,150,255,.9)':'rgba(255,255,255,.9)';ctx.shadowOffsetX=-3;ctx.fillRect(x-38,yb-h,76,h);ctx.beginPath();ctx.moveTo(x-50,yb-h);ctx.lineTo(x,yb-h-32);ctx.lineTo(x+50,yb-h);ctx.fill();ctx.restore();pill(n,x,yb+56,u*(1-rg),'#fff0c8',34)});
  if(rg>0){ctx.save();ctx.globalAlpha=rg;ctx.translate(CX,H/2+60);ctx.scale(1,0.36);ctx.lineWidth=14;C.forEach(([c],i)=>{ctx.strokeStyle=i===3?'#4a4a68':c;ctx.beginPath();ctx.arc(0,0,300,i*1.5708+t*0.45,(i+1)*1.5708+t*0.45);ctx.stroke()});ctx.restore()}
  (S.fx||[]).forEach(F=>drawFx(F,t,P,d))};

function humanOutline(x,y,sc,t,rgb,a){ctx.save();ctx.translate(x,y);ctx.scale(sc,sc);glow(0,-60,260,rgb,0.35*a);ctx.strokeStyle=`rgba(${rgb},${0.95*a})`;ctx.fillStyle=`rgba(${rgb},${0.12*a})`;ctx.lineWidth=5;ctx.lineJoin='round';ctx.beginPath();ctx.arc(0,-190,44,0,7);ctx.moveTo(-90,-130);ctx.quadraticCurveTo(0,-160,90,-130);ctx.lineTo(110,40);ctx.lineTo(70,40);ctx.lineTo(60,200);ctx.lineTo(10,200);ctx.lineTo(0,60);ctx.lineTo(-10,200);ctx.lineTo(-60,200);ctx.lineTo(-70,40);ctx.lineTo(-110,40);ctx.closePath();ctx.fill();ctx.stroke();for(let i=0;i<10;i++){const an=i*0.7+t;ctx.fillStyle=`rgba(255,250,215,${0.8*a})`;ctx.beginPath();ctx.arc(Math.cos(an)*150,-40+Math.sin(an*1.3)*190,3,0,7);ctx.fill()}ctx.restore()}
