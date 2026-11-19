/* v2 settings (backgrounds + effects). Concatenated after scenes.js; uses BG, FXV2, layer, skyG, glow, ridge, cloudBand,
   starsF, moonAt, ocean, dust, embers, stext, q, rng, mod, lerp, clamp, W, H, CX from the engine.
   Palette rule (owner reference): muted, cinematic - warm light against cool shadow, grain/vignette come from the grade. */

/* ---------- shared drawing helpers ---------- */
function flameTongue(cx,by,w,h,t,seed,col1,col2,col3){const ph=seed*2.3,sw=Math.sin(t*5+ph)*w*.35+Math.sin(t*9+ph*1.7)*w*.12,hh=h*(.78+.22*Math.sin(t*7+ph*1.3)),lean=Math.sin(t*3+ph)*w*.3;
  const tg=(ww,hh2,c)=>{ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(cx-ww,by);ctx.bezierCurveTo(cx-ww*1.25,by-hh2*.3,cx-ww*.9+lean,by-hh2*.62,cx-ww*.1+sw,by-hh2*.9);ctx.quadraticCurveTo(cx+sw*1.2+lean*.4,by-hh2*1.02,cx+sw*1.35,by-hh2);ctx.bezierCurveTo(cx+ww*.5+sw,by-hh2*.66,cx+ww*1.2+lean,by-hh2*.34,cx+ww,by);ctx.closePath();ctx.fill()};
  tg(w,hh,col1);tg(w*.68,hh*.74,col2);tg(w*.36,hh*.46,col3)}
function fireBank(cx,by,wid,hei,t,intensity){const f=intensity==null?1:intensity;if(f<=0)return;ctx.save();ctx.globalCompositeOperation='lighter';
  glow(cx,by-hei*.45,hei*1.7,'255,130,50',.4*f);glow(cx,by-hei*.25,hei*.9,'255,190,90',.3*f);
  const N=15;for(let i=0;i<N;i++){const u=(i-(N-1)/2)/((N-1)/2),r=(Math.sin(i*12.9898)*43758.5453)%1,x=cx+u*wid*.5+Math.sin(t*2+i)*4,h=hei*f*(1-Math.abs(u)*.55)*(.55+.45*Math.abs(r));
    flameTongue(x,by,wid/N*1.9,h,t,i*1.37+1,'rgba(235,90,25,.62)','rgba(255,170,60,.72)','rgba(255,240,190,.8)')}
  for(let k=0;k<5;k++){const x=cx+(k-2)*wid*.12,hh=hei*f*(.95+.1*Math.sin(t*4+k));flameTongue(x,by,wid*.06,hh,t,k*2.9+7,'rgba(255,130,40,.5)','rgba(255,200,90,.6)','rgba(255,250,210,.7)')}
  ctx.restore()}
function pillarShape(x,y0,y1,w,warm,dim){const g=ctx.createLinearGradient(x-w/2,0,x+w/2,0);g.addColorStop(0,warm?'#8a6a4a':'#5a6078');g.addColorStop(.5,warm?'#6a4a34':'#3e4560');g.addColorStop(1,warm?'#2c1a10':'#1a1e32');ctx.fillStyle=g;ctx.fillRect(x-w/2,y0,w,y1-y0);
  ctx.fillStyle='rgba(0,0,0,.22)';for(let k=-1;k<=1;k++)ctx.fillRect(x+k*w*.22-2,y0+30,4,y1-y0-60);
  ctx.fillStyle=warm?'#7a5a3c':'#4a5070';ctx.fillRect(x-w*.62,y0,w*1.24,34);ctx.fillRect(x-w*.55,y0+34,w*1.1,16);ctx.fillRect(x-w*.66,y1-30,w*1.32,30);
  ctx.fillStyle='rgba(255,220,160,.12)';ctx.fillRect(x-w*.62,y0,w*1.24,5)}
function garlandSwag(x1,x2,y,drop,t,col){ctx.save();ctx.lineCap='round';ctx.strokeStyle=col||'#e08a28';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(x1,y);ctx.quadraticCurveTo((x1+x2)/2,y+drop*2+Math.sin(t*.8+x1)*3,x2,y);ctx.stroke();
  for(let i=0;i<=16;i++){const u=i/16,px=(1-u)*(1-u)*x1+2*(1-u)*u*(x1+x2)/2+u*u*x2,py=(1-u)*(1-u)*y+2*(1-u)*u*(y+drop*2)+u*u*y;ctx.fillStyle=i%3?'#f0a030':'#d85a1a';ctx.beginPath();ctx.arc(px,py+4,5,0,7);ctx.fill();ctx.fillStyle='rgba(60,120,40,.8)';ctx.beginPath();ctx.arc(px+3,py+9,3,0,7);ctx.fill()}ctx.restore()}

/* ---------- backgrounds ---------- */
BG.yagna=function(S,t){const f=S.fire==null?1:S.fire,fl=.86+.14*Math.sin(t*9)+.06*Math.sin(t*23);
  skyG(['#0c0810','#201216','#3a2018','#5a3622'],-300,H+300);glow(CX,470,640,'255,140,60',.30*f*fl);
  layer(.22,()=>{ // hall: ceiling beam, pillars, garlands, pennants
    ctx.fillStyle='#1a0e0c';ctx.fillRect(-300,-300,W+600,350);ctx.fillStyle='#2a1612';ctx.fillRect(-300,40,W+600,22);
    const xs=[-60,170,410,870,1110,1340];xs.forEach(x=>{const lit=1-Math.min(1,Math.abs(x-CX)/760);pillarShape(x,40,500,78,true);ctx.fillStyle=`rgba(255,150,60,${.16*f*lit*fl})`;ctx.fillRect(x-40,40,80,460)});
    for(let i=0;i<xs.length-1;i++)if(xs[i+1]-xs[i]<400)garlandSwag(xs[i],xs[i+1],78,22,t);garlandSwag(410,870,78,34,t,'#d8782a');
    for(let i=0;i<14;i++){const x=-100+i*100;ctx.fillStyle=i%2?'#d8662a':'#e8a030';ctx.beginPath();ctx.moveTo(x,62);ctx.lineTo(x+26,62);ctx.lineTo(x+13+Math.sin(t*2+i)*3,96);ctx.closePath();ctx.fill()}
    ctx.fillStyle='rgba(8,4,6,.6)';ctx.fillRect(-300,500,W+600,60)});
  // floor with warm reflection and perspective tile lines
  const fg=ctx.createLinearGradient(0,500,0,H+300);fg.addColorStop(0,'#2e1a10');fg.addColorStop(1,'#0e0806');ctx.fillStyle=fg;ctx.fillRect(-300,500,W+600,H);
  glow(CX,590,420,'255,140,60',.28*f*fl);ctx.strokeStyle='rgba(255,200,140,.07)';ctx.lineWidth=2;for(let k=-8;k<=8;k++){ctx.beginPath();ctx.moveTo(CX+k*28,500);ctx.lineTo(CX+k*220,H+60);ctx.stroke()}for(let k=1;k<6;k++){const y=500+Math.pow(k/5,1.8)*230;ctx.beginPath();ctx.moveTo(-100,y);ctx.lineTo(W+100,y);ctx.stroke()}
  // the stepped fire pit (havan kunda)
  const kx=S.kx==null?CX:S.kx;layer(.9,()=>{ctx.fillStyle='#5a3a26';ctx.fillRect(kx-300,596,600,46);ctx.fillStyle='#76503a';ctx.fillRect(kx-236,566,472,36);ctx.fillStyle='#8c6244';ctx.fillRect(kx-176,544,352,28);
    ctx.fillStyle='rgba(255,170,90,'+(.3*f)+')';ctx.fillRect(kx-300,596,600,4);ctx.fillRect(kx-236,566,472,4);ctx.fillRect(kx-176,544,352,4);
    ctx.fillStyle='#120804';ctx.beginPath();ctx.ellipse(kx,548,150,16,0,0,7);ctx.fill();
    fireBank(kx,552,300,250,t,f);ctx.fillStyle='rgba(60,30,12,.9)';ctx.fillRect(kx-176,560,352,14);ctx.fillStyle='rgba(255,170,90,.25)';ctx.fillRect(kx-176,560,352,3);
    for(let i=0;i<8;i++){const u=mod(t*.16+i/8,1),x=kx+Math.sin(t*.9+i*2.1)*36+u*(i%2?60:-60),y=540-u*470;ctx.fillStyle=`rgba(190,180,170,${.16*(1-u)*f})`;ctx.beginPath();ctx.ellipse(x,y,26+u*70,18+u*40,0,0,7);ctx.fill()}});
  embers(t,40,11,'255,150,60',1.1*f);dust(t,26,17,'255,210,150',.25,3)};

BG.kailash=function(S,t){skyG(['#03061a','#0a1432','#18284e','#34466c'],-300,H+300);starsF(t);moonAt(W*(S.mx==null?.22:S.mx),150,38,t);glow(W*.22,150,420,'190,205,255',.18);
  layer(.12,()=>{ridge(430,190,31,'#cfd8ee','#1c2848')});layer(.22,()=>{ridge(520,140,37,'#9aa8cc','#101a34')});
  layer(.32,()=>cloudBand('klA',61,STC,380,5,t,.5));layer(.4,()=>{ridge(600,96,41,'#6c7ca8','#080e20')});
  layer(.8,()=>{ctx.fillStyle='#070b18';ctx.beginPath();ctx.moveTo(-300,H+300);ctx.lineTo(-300,640);ctx.bezierCurveTo(100,610,300,640,560,628);ctx.bezierCurveTo(820,616,1000,650,1580,620);ctx.lineTo(1580,H+300);ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(180,200,255,.18)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-300,640);ctx.bezierCurveTo(100,610,300,640,560,628);ctx.bezierCurveTo(820,616,1000,650,1580,620);ctx.stroke()});
  dust(t,40,7,'200,215,255',.35,3)};

BG.garden=function(S,t){skyG(['#1a2a5a','#5a78b4','#e8c0a0','#ffe8bc'],-300,H+300);glow(W*.72,430,560,'255,225,170',.5);layer(.12,()=>cloudBand('gdA',13,CELC2,70,4,t,.75));
  layer(.22,()=>ridge(500,80,5,'#7aa064','#20402a'));
  layer(.3,()=>{const r=rng(9);for(let i=0;i<26;i++){const x=-200+i*70+r()*30,y=470-r()*40,s=24+r()*26;ctx.fillStyle=i%3?'#2e5a34':'#3a6a3c';ctx.beginPath();ctx.arc(x,y,s,0,7);ctx.fill();ctx.fillStyle='#4a3020';ctx.fillRect(x-3,y+s*.6,6,s*.7)}});
  layer(.5,()=>{const g=ctx.createLinearGradient(0,520,0,H+300);g.addColorStop(0,'#5a8c44');g.addColorStop(1,'#1c3a20');ctx.fillStyle=g;ctx.fillRect(-300,520,W+600,H);
    ctx.fillStyle='rgba(170,215,235,.7)';ctx.beginPath();ctx.moveTo(-300,610);ctx.bezierCurveTo(200,580,500,650,900,600);ctx.bezierCurveTo(1100,575,1300,600,1580,590);ctx.lineTo(1580,650);ctx.bezierCurveTo(1300,660,1100,640,900,660);ctx.bezierCurveTo(500,700,200,630,-300,660);ctx.closePath();ctx.fill();
    const r=rng(21);for(let i=0;i<70;i++){const x=r()*W,y=660+r()*90;ctx.fillStyle=['#f6c8d8','#fff0b8','#ffffff','#f09ab0'][i%4];ctx.beginPath();ctx.arc(x,y,2+r()*2.4,0,7);ctx.fill()}});
  dust(t,50,19,'255,235,190',.4,3)};

BG.cosmicsea=function(S,t){skyG(['#02040c','#071228','#10244a','#1c3a6a'],-300,H+300);starsF(t);glow(CX,S.gy||340,640,S.rgb||'120,160,255',S.ga==null?.2:S.ga);if(S.gold)glow(CX,S.gy||340,520,'255,200,90',.3*S.gold);
  layer(.2,()=>cloudBand('csA',77,DUSKC,260,3,t,.35));ocean(t,S.oy||540,'#0a1a3c','#02060f',S.rgb||'150,180,255',CX);dust(t,40,5,'200,215,255',.3,3)};

/* ---------- effects ---------- */
// Hiranyagarbha: the golden cosmic egg; crack 0..1 shows fissures + light, split 0..1 separates the two halves (heaven above, earth below)
FXV2.egg=function(F,t,P,d,a){const x=F.x,y=F.y,sc=F.sc||1,cr=F.crack!=null?F.crack:(F.cc!=null?q(P,t,F.cc,F.cd||1.5):0),sp=F.split!=null?F.split:(F.sc2!=null?q(P,t,F.sc2,F.sd||1.5):0);
  ctx.save();ctx.globalAlpha*=a;ctx.translate(x,y);ctx.scale(sc,sc);const pulse=1+Math.sin(t*1.6)*.02;
  glow(0,0,260*pulse,'255,200,90',.55+cr*.25);
  const half=(up)=>{ctx.save();ctx.beginPath();ctx.rect(-200,up?-200-sp*90:0+sp*90,400,200);ctx.clip();ctx.translate(0,up?-sp*20:sp*20);
    const g=ctx.createRadialGradient(-40,-60,10,0,0,150);g.addColorStop(0,'#fff2b8');g.addColorStop(.5,'#f0b83e');g.addColorStop(1,'#a8701a');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(0,0,110*pulse,150*pulse,0,0,7);ctx.fill();
    ctx.strokeStyle='rgba(120,70,10,.5)';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(0,0,110*pulse,150*pulse,0,0,7);ctx.stroke();ctx.fillStyle='rgba(255,255,255,.28)';ctx.beginPath();ctx.ellipse(-44,-70,24,52,-.4,0,7);ctx.fill();ctx.restore()};
  half(true);half(false);
  if(cr>0&&sp<.98){ctx.save();ctx.strokeStyle=`rgba(255,250,220,${.9*cr})`;ctx.lineWidth=4;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-108,0);for(let i=1;i<=9;i++)ctx.lineTo(-108+i*24,(i%2?-1:1)*(10+(i%3)*6)*cr);ctx.stroke();glow(0,0,200*cr,'255,240,180',.6*cr);ctx.restore()}
  if(sp>.2){ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<9;i++){const an=-Math.PI/2+(i-4)*.32;ctx.fillStyle=`rgba(255,235,170,${.2*sp})`;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(an-.05)*700,Math.sin(an-.05)*700);ctx.lineTo(Math.cos(an+.05)*700,Math.sin(an+.05)*700);ctx.closePath();ctx.fill()}ctx.restore()}
  ctx.restore()};
// four glowing Vedas, appearing one by one (cue index c is the first)
FXV2.books=function(F,t,P,d,a){const names=F.names||['ऋग्वेद','यजुर्वेद','सामवेद','अथर्ववेद'],cols=F.cols||['#f0c850','#e8a040','#f0e070','#c8a0f0'];ctx.save();
  names.forEach((n,i)=>{const ai=q(P,t,(F.c||0)+i,.6);if(ai<=.01)return;const x=F.x+(i-1.5)*(F.gap||230),y=F.y+Math.sin(t*1.3+i)*8-(1-ai)*40+(F.fall||0)*t;ctx.save();ctx.globalAlpha*=ai*a;glow(x,y,120,'255,225,150',.5);ctx.translate(x,y);ctx.rotate((i-1.5)*.06);
    const g=ctx.createLinearGradient(-48,0,48,0);g.addColorStop(0,'#8a5a1a');g.addColorStop(.5,cols[i]);g.addColorStop(1,'#8a5a1a');ctx.fillStyle=g;ctx.beginPath();ctx.roundRect(-46,-62,92,124,6);ctx.fill();ctx.strokeStyle='rgba(60,30,0,.6)';ctx.lineWidth=3;ctx.stroke();
    ctx.strokeStyle='rgba(255,245,200,.7)';ctx.lineWidth=2;ctx.strokeRect(-36,-52,72,104);ctx.fillStyle='rgba(255,245,200,.85)';ctx.beginPath();ctx.arc(0,-8,13,0,7);ctx.fill();ctx.restore();
    stext(n,x,F.y+96,28,'#ffe9b8',ai*a)});ctx.restore()};
// Vishnu's white-gold pillar
FXV2.pillar=function(F,t,P,d,a){ctx.save();ctx.globalAlpha*=a;const x=F.x,y0=F.y0==null?60:F.y0,y1=F.y1==null?560:F.y1,w=F.w||70;glow(x,(y0+y1)/2,300,'255,235,180',.3);
  const g=ctx.createLinearGradient(x-w/2,0,x+w/2,0);g.addColorStop(0,'#c8bca0');g.addColorStop(.35,'#fff6dc');g.addColorStop(.6,'#e8d8a4');g.addColorStop(1,'#8a7a58');ctx.fillStyle=g;ctx.fillRect(x-w/2,y0,w,y1-y0);
  ctx.fillStyle='#fff2c8';ctx.fillRect(x-w*.62,y0,w*1.24,28);ctx.fillRect(x-w*.62,y1-26,w*1.24,26);ctx.strokeStyle='rgba(120,100,50,.4)';ctx.lineWidth=2;[-.22,0,.22].forEach(k=>{ctx.beginPath();ctx.moveTo(x+k*w,y0+34);ctx.lineTo(x+k*w,y1-30);ctx.stroke()});ctx.restore()};
// plain flame cluster for sacrifices/lamps
FXV2.fire=function(F,t,P,d,a){ctx.save();ctx.globalAlpha*=a;fireBank(F.x,F.y,F.w||200,F.h||180,t,F.i==null?1:F.i);ctx.restore()};
// mountain of light (Hayagriva grows into a blue mountain)
FXV2.bluemountain=function(F,t,P,d,a){const g=F.c!=null?q(P,t,F.c,F.d||3):1;ctx.save();ctx.globalAlpha*=a*g;const x=F.x,y=F.y,s=F.s||1;glow(x,y-200*s,500*s,'120,160,255',.28);
  ctx.fillStyle='#2a4aa0';ctx.beginPath();ctx.moveTo(x-420*s,y);ctx.lineTo(x-200*s,y-300*s*g);ctx.lineTo(x-60*s,y-420*s*g);ctx.lineTo(x+40*s,y-520*s*g);ctx.lineTo(x+210*s,y-330*s*g);ctx.lineTo(x+430*s,y);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(180,210,255,.3)';ctx.beginPath();ctx.moveTo(x+40*s,y-520*s*g);ctx.lineTo(x+210*s,y-330*s*g);ctx.lineTo(x+60*s,y-250*s*g);ctx.closePath();ctx.fill();ctx.restore()};

// water surface over the bottom of a figure (so a nest/boat sits IN the sea): y = waterline
FXV2.waterfront=function(F,t,P,d,a){const y=F.y;ctx.save();ctx.globalAlpha*=a;const g=ctx.createLinearGradient(0,y,0,H+300);g.addColorStop(0,F.top||'rgba(12,30,66,.78)');g.addColorStop(1,F.bot||'rgba(2,6,18,.97)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(-300,y+Math.sin(t)*3);for(let x=-300;x<=W+300;x+=40)ctx.lineTo(x,y+Math.sin(x*.02+t*1.2)*5);ctx.lineTo(W+300,H+300);ctx.lineTo(-300,H+300);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(170,200,255,.28)';ctx.lineWidth=2;for(let k=0;k<4;k++){ctx.beginPath();for(let x=-300;x<=W+300;x+=30){const yy=y+8+k*26+Math.sin(x*.018+t*1.1+k)*4;x>-300?ctx.lineTo(x,yy):ctx.moveTo(x,yy)}ctx.stroke()}
  ctx.strokeStyle='rgba(220,235,255,.5)';ctx.lineWidth=2.4;ctx.beginPath();for(let x=-300;x<=W+300;x+=30){const yy=y+Math.sin(x*.02+t*1.2)*5;x>-300?ctx.lineTo(x,yy):ctx.moveTo(x,yy)}ctx.stroke();ctx.restore()};

// the three gunas: sattva (white), rajas (red), tamas (black); F.hi highlights one
FXV2.gunas=function(F,t,P,d,a){const cols=[['#f6f2e4','सत्व','255,250,230'],['#d8402a','रजस','255,90,60'],['#17121e','तमस','150,110,220']];ctx.save();
  cols.forEach(([col,name,rgb],i)=>{const ai=F.all?1:q(P,t,(F.c||0)+i,.7);if(ai<=.01)return;const x=CX+(i-1)*(F.gap||300),y=(F.y||340)+Math.sin(t*1.2+i)*6,hi=F.hi===i?1.28:(F.hi==null?1:.8);ctx.save();ctx.globalAlpha*=ai*a;
    glow(x,y,200*hi,rgb,F.hi===i?.7:.4);const g=ctx.createRadialGradient(x-20,y-24,6,x,y,92*hi);g.addColorStop(0,i===2?'#4a3a66':'#ffffff');g.addColorStop(.5,col);g.addColorStop(1,i===2?'#07050c':shade2(col));ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,86*hi,0,7);ctx.fill();ctx.strokeStyle=`rgba(${rgb},.6)`;ctx.lineWidth=3;ctx.stroke();ctx.restore();
    stext(name,x,y+150*hi,F.hi===i?50:38,'#ffe9b8',ai*a)});ctx.restore()};
function shade2(c){return c==='#f6f2e4'?'#bcb89c':'#7a1a10'}
// one of the five elements: type vayu|jal|prithvi|agni|akash
FXV2.element=function(F,t,P,d,a){const x=F.x||CX,y=F.y||330,sc=F.sc||1,tp=F.type;ctx.save();ctx.globalAlpha*=a;ctx.translate(x,y);ctx.scale(sc,sc);const sw=Math.sin(t*2)*6;
  if(tp==='vayu'){glow(0,0,220,'190,225,255',.35);ctx.strokeStyle='#cfe6ff';ctx.lineWidth=9;ctx.lineCap='round';[-60,0,60].forEach((dy,i)=>{ctx.beginPath();ctx.moveTo(-140,dy);ctx.bezierCurveTo(-60,dy-50+sw,40,dy+50-sw,120,dy-10);ctx.bezierCurveTo(150,dy-26,150,dy+20,112,dy+26);ctx.stroke()})}
  else if(tp==='jal'){glow(0,0,220,'120,180,255',.4);const g=ctx.createLinearGradient(0,-120,0,100);g.addColorStop(0,'#bfe4ff');g.addColorStop(1,'#2a6ad0');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(0,-130);ctx.bezierCurveTo(70,-30,100,20,70,70);ctx.bezierCurveTo(40,120,-40,120,-70,70);ctx.bezierCurveTo(-100,20,-70,-30,0,-130);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=5;ctx.beginPath();ctx.arc(-18,40,40,2.4,3.6);ctx.stroke()}
  else if(tp==='prithvi'){glow(0,0,220,'150,200,110',.3);ctx.fillStyle='#6a4a2a';ctx.beginPath();ctx.moveTo(-150,100);ctx.lineTo(-40,-90);ctx.lineTo(20,-10);ctx.lineTo(80,-120);ctx.lineTo(160,100);ctx.closePath();ctx.fill();ctx.fillStyle='#4a8a3a';ctx.beginPath();ctx.moveTo(-150,100);ctx.lineTo(-100,30);ctx.lineTo(-20,70);ctx.lineTo(60,20);ctx.lineTo(120,60);ctx.lineTo(160,100);ctx.closePath();ctx.fill();ctx.fillStyle='rgba(255,255,255,.7)';ctx.beginPath();ctx.moveTo(80,-120);ctx.lineTo(55,-80);ctx.lineTo(100,-76);ctx.closePath();ctx.fill()}
  else if(tp==='agni'){fireBank(0,100,200,230,t,1)}
  else if(tp==='akash'){glow(0,0,240,'160,140,255',.4);ctx.strokeStyle='#d8ccff';ctx.lineWidth=6;ctx.beginPath();ctx.arc(0,0,100,0,7);ctx.stroke();ctx.strokeStyle='rgba(216,204,255,.5)';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(0,0,150,52,t*.4,0,7);ctx.stroke();ctx.fillStyle='#fff';for(let i=0;i<14;i++){const an=i*.9+t*.3,r=40+(i%4)*22;ctx.beginPath();ctx.arc(Math.cos(an)*r,Math.sin(an)*r,2.4,0,7);ctx.fill()}}
  ctx.restore();if(F.label)stext(F.label,x,y+(F.ly||170)*sc,F.lsize||48,'#ffe9b8',a)};
// a blooming lotus (open 0..1 driven by cue F.c)
FXV2.lotus=function(F,t,P,d,a){const op=F.c!=null?q(P,t,F.c,F.d||1.4):(F.open==null?1:F.open);ctx.save();ctx.globalAlpha*=a;lotus(F.x,F.y,F.sc||1,t,op,1);ctx.restore()};

/* ---------- painted-image support (Gemini pilot): asset preload, image background, cut-out figure ---------- */
const IMGS={};window.IMG_PENDING=0;
function imgGet(src){let e=IMGS[src];if(!e){e=IMGS[src]={img:new Image(),ok:false};window.IMG_PENDING++;e.img.onload=()=>{e.ok=true;window.IMG_PENDING--};e.img.onerror=()=>{window.IMG_PENDING--;e.err=true;console.error('image failed',src)};const key=src.split('/').pop();e.img.src=(window.ASSET_DATA&&window.ASSET_DATA[key])||src}return e}
function preloadAssets(o){if(Array.isArray(o))o.forEach(preloadAssets);else if(o&&typeof o==='object'){if(typeof o.src==='string')imgGet(o.src);for(const k in o)preloadAssets(o[k])}}
{const _init=window.init;window.init=function(sh,tm){preloadAssets(sh);return _init.apply(this,arguments)}}
BG.img=function(S,t){const e=imgGet(S.src);skyG(S.cols||['#05060c','#10131f'],-300,H+300);if(!e.ok)return;
  layer(S.d==null?.25:S.d,()=>{const w=e.img.width,h=e.img.height,z=(S.z0||1.14)+(S.zv||.004)*t,sc=Math.max(W/w,H/h)*z,fx=S.fx==null?.5:S.fx,fy=S.fy==null?.5:S.fy,dx=(W-w*sc)*fx-(S.px||0)*t,dy=(H-h*sc)*fy-(S.py||0)*t;
    ctx.drawImage(e.img,dx,dy,w*sc,h*sc);if(S.tint){ctx.fillStyle=S.tint;ctx.fillRect(-300,-300,W+600,H+600)}})};
function IMGFIG(f,x,y,s,t){const e=imgGet(f.src);if(!e.ok)return;const w=e.img.width,h=e.img.height,k=(f.hpx||520)/h*s,br=1+(f.breath==null?.006:f.breath)*Math.sin(t*1.7),sw=(f.sway||0)*Math.sin(t*1.1);
  const wk=f.walk?Math.sin(t*f.walk):0;ctx.save();ctx.translate(x,y-(f.walk?Math.abs(wk)*(f.walkAmp||10):0));
  if(f.shadow!==false&&f.anchor!=='center'){ctx.fillStyle='rgba(0,0,0,.35)';ctx.beginPath();ctx.ellipse(0,4,w*k*.34,w*k*.05,0,0,7);ctx.fill()}
  ctx.rotate(sw+wk*.04);ctx.scale((f.flip||1)*k,k*br);const ax=w/2,ay=f.anchor==='center'?h/2:h;if(f.glow){ctx.shadowColor=f.glow;ctx.shadowBlur=(f.gb||34)/k}
  ctx.drawImage(e.img,-ax,-ay,w,h);ctx.restore()}

/* ---------- rigged painted puppet: Shiva (pieces sliced from the approved Gemini art, shared source coordinates 445x943) ---------- */
const SP_SRC=['root','head_open','head_closed','head_rage','armR_up','armR_lo','armL_grp','thighL','thighR','shinL','shinR'].map(n=>'../library/pilot/assets/sp_'+n+'.png');
const SP={pivot:{head:[268,232],armR:[385,288],elbowR:[405,395],armL:[150,270],hipL:[238,640],hipR:[300,640],kneeL:[220,700],kneeR:[322,700]},H:943,W:445};
function loadShivaPuppet(){SP_SRC.forEach(imgGet)}
function spImg(n){return imgGet('../library/pilot/assets/sp_'+n+'.png')}
{const _pre=preloadAssets;preloadAssets=function(o){if(Array.isArray(o))o.forEach(preloadAssets);else if(o&&typeof o==='object'){if(o.who==='shiva_p')loadShivaPuppet();if(typeof o.src==='string')imgGet(o.src);for(const k in o)preloadAssets(o[k])}}}
function drawShivaP(f,x,y,s,t,P){
  const ok=SP_SRC.every(u=>imgGet(u).ok);if(!ok)return;
  const an=f.ka?clamp((t-f.ka[2])/(f.ka[3]||1),0,1):0,ae=an*an*(3-2*an),kk=f.ka?f.ka[0]+(f.ka[1]-f.ka[0])*ae:(f.k==null?0:f.k),k=clamp(kk,0,1),rage=k,st=f.stance==null?k:f.stance,hp=(f.hpx||640)*s,sc=hp/SP.H,fl=f.flip||1;
  const br=Math.sin(t*1.7),sw=Math.sin(t*1.1);
  const aHead=(f.head||0)+Math.sin(t*.9)*.012+(f.headT||0),aArmR=(f.armR||0)+Math.sin(t*1.3)*.012+rage*.12,aElbR=(f.elbowR||0)-.06*rage,aArmL=(f.armL||0)+Math.sin(t*1.1+1)*.01-rage*.10*(f.lunge||0)+(f.lunge||0)*(-.45);
  const aTh=.34*st,aSh=-.26*st,crouch=60*st;
  ctx.save();ctx.translate(x,y);ctx.scale(fl*sc,sc);ctx.translate(-SP.W/2,-SP.H+crouch+br*2.5);
  if(f.shadow!==false){ctx.save();ctx.fillStyle='rgba(0,0,0,.35)';ctx.beginPath();ctx.ellipse(SP.W/2,SP.H-crouch-4,150+st*70,18,0,0,7);ctx.fill();ctx.restore()}
  if(f.glow){ctx.shadowColor=f.glow;ctx.shadowBlur=26}
  const D=n=>{const e=spImg(n);ctx.drawImage(e.img,0,0)};
  const rot=(pv,a,fn)=>{ctx.save();ctx.translate(pv[0],pv[1]);ctx.rotate(a);ctx.translate(-pv[0],-pv[1]);fn();ctx.restore()};
  const WL=f.walk?Math.sin(t*f.walk):0;const thigh=(pv,kn,side,n,sn)=>rot(pv,(side<0?aTh:-aTh)+(side<0?1:-1)*.30*WL,()=>{
    // synthetic upper leg (hidden by the skirt) + visible thigh band, then the shin hinged at the knee
    ctx.save();const g=ctx.createLinearGradient(pv[0]-34,0,pv[0]+34,0);g.addColorStop(0,'#a7c4e2');g.addColorStop(.5,'#93b5d8');g.addColorStop(1,'#7fa2c8');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(pv[0]-36,pv[1]-30);ctx.lineTo(pv[0]+36,pv[1]-30);ctx.lineTo(kn[0]+34,kn[1]);ctx.lineTo(kn[0]-34,kn[1]);ctx.closePath();ctx.fill();ctx.restore();
    D(n);rot(kn,(side<0?-1:1)*Math.abs(aSh)+(side<0?-1:1)*.22*Math.max(0,(side<0?WL:-WL)),()=>D(sn))});
  thigh(SP.pivot.hipL,SP.pivot.kneeL,-1,'thighL','shinL');thigh(SP.pivot.hipR,SP.pivot.kneeR,1,'thighR','shinR');
  ctx.save();ctx.translate(SP.W/2,SP.H);ctx.scale(1,1+.004*br);ctx.translate(-SP.W/2,-SP.H);D('root');ctx.restore();
  rot(SP.pivot.armR,aArmR-.18*WL,()=>{D('armR_up');rot(SP.pivot.elbowR,aElbR,()=>D('armR_lo'))});
  rot(SP.pivot.armL,aArmL,()=>D('armL_grp'));
  rot(SP.pivot.head,aHead,()=>{const closed=f.eyes==='closed';
    if(k<.99){ctx.globalAlpha=(1-k);D(closed?'head_closed':'head_open');ctx.globalAlpha=1}
    if(k>.01){ctx.globalAlpha=Math.min(1,k*1.4);D('head_rage');ctx.globalAlpha=1}});
  ctx.restore()}

FXV2.fximg=function(F,t,P,d,a){const e=imgGet(F.src);if(!e.ok)return;ctx.save();ctx.globalAlpha*=a*(F.alpha==null?1:F.alpha);if(F.blend)ctx.globalCompositeOperation=F.blend;const w=F.w||300,h=w*e.img.height/e.img.width,sc=1+(F.grow||0)*t;ctx.translate(F.x+(F.vx||0)*t,F.y);ctx.rotate((F.rot||0)+(F.spin||0)*t);ctx.scale(sc,sc);ctx.drawImage(e.img,-w/2,-h/2,w,h);ctx.restore()};

// ---- painted (Gemini) backgrounds under the existing particle animation ----
(function(){
  const A='../library/pilot/assets/bgp_';
  const P={
    yagna:{f:'yagna',fy:.5,fx:(S,t,f,fl)=>{glow(CX,470,620,'255,140,60',.22*f*fl);layer(.9,()=>{fireBank(S.kx==null?CX:S.kx,552,300,250,t,f)});embers(t,40,11,'255,150,60',1.1*f);dust(t,26,17,'255,210,150',.25,3)}},
    kailash:{f:'kailash',fx:(S,t)=>{dust(t,46,5,'225,235,255',.5,5);glow(W*(S.mx==null?.22:S.mx),120,380,'190,205,255',.12)}},
    cosmicsea:{f:'cosmic_sea',fx:(S,t)=>{starsF(t,50);dust(t,30,9,'180,200,255',.35,3)}},
    garden:{f:'garden',fx:(S,t)=>{dust(t,34,21,'255,236,170',.55,4,1.4);dust(t,18,23,'255,190,200',.5,7,1.6)}},
    palace:{f:'palace',fx:(S,t)=>{dust(t,34,31,'255,230,170',.4,3);glow(210,260,200,'255,210,120',.18+.04*Math.sin(t*3));glow(500,260,200,'255,210,120',.18)}},
    cosmos:{f:'cosmos',fx:(S,t)=>{starsF(t,70);dust(t,44,3,S.rgb||'200,190,255',.45,2)}},
    dawn:{f:'heaven_clouds',fx:(S,t)=>{dust(t,30,41,'255,240,220',.45,3);glow(CX,150,520,'255,230,190',.16)}},
    storm:{f:'storm_red',fx:(S,t)=>{embers(t,36,7,'255,90,60',.9);glow(CX,600,520,'255,110,50',.2+.06*Math.sin(t*5))}}
  };
  Object.keys(P).forEach(k=>{const o=P[k];BG[k]=function(S,t){const f=S.fire==null?1:S.fire,fl=.86+.14*Math.sin(t*9)+.06*Math.sin(t*23);
    BG.img({src:A+o.f+'.png',fy:o.fy==null?.5:o.fy,z0:1.08,zv:.003,d:.25},t);o.fx(S,t,f,fl)}});
})();

window.imgGetV2=imgGet;
['open','closed','rage'].forEach(n=>imgGet('../library/pilot/assets/sp_hc_'+n+'.png'));
