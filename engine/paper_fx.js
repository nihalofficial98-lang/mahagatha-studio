/* Code-drawn paper-cut EFFECTS / props (replaces the deleted Gemini fx images; same names, so old plans keep working).
   Use in a shot:  {"t":"pfx","k":"<name>","x":640,"y":300,"w":400, "alpha":1, "c":0,"d":0.6, "par":1.0, "spin":0, "vx":0, "grow":0, "rot":0}
   Legacy form {"t":"fximg","src":".../fx_<name>.png"} or {"t":"img","src":"<name>"} is routed here too.
   (x,y) = centre of the object, w = its width in the 1280x720 plan.  Solid props ignore blend:'lighter' (paper must stay paper).
   Extra options: ketaki ("flower_petals"): wither 0..1 or wc (cue) + wd, fall:1 (petals drop), glow 0..1.  ground_crack: grows with the fade-in.
   Also defines: SHOTS.scene with depth layers (sc.layers), background change on a cue (sc.bg2 + bgc/bgd) and bg parameter tween (sc.bgTo + bgc/bgd). */
(function(){
const {cutP,cutU,vg,shd,mix,hx,drawLayers,OBJ}=window.PS,TAU=Math.PI*2,PI=Math.PI;
window.IMG_PENDING=0; // no images are loaded any more (renderers still wait on this flag)
const gold=(y0,y1)=>vg(y0,y1,['#fff4c0','#f2c14e','#b87a1a']);
const gem=(x,y,r,c)=>cutP(()=>ctx.arc(x,y,r,0,TAU),(()=>{const g=ctx.createRadialGradient(x-r*.3,y-r*.3,0,x,y,r);g.addColorStop(0,'#ffffff');g.addColorStop(.35,c);g.addColorStop(1,shd(c,.45));return g})(),{sh:0,lw:1.2});
const add=fn=>{ctx.save();ctx.globalCompositeOperation='lighter';fn();ctx.restore()};
function boltPts(seed,len,jit,steps){const r=rng(seed),P=[[0,0]];let x=0;for(let i=1;i<=steps;i++){x+=(r()-.5)*jit;P.push([x,i/steps*len])}return P}
function boltDraw(P,wd,a){cutP(()=>{P.forEach((p,i)=>i?ctx.lineTo(p[0]-wd*(1-i/P.length),p[1]):ctx.moveTo(p[0]-wd,p[1]));for(let i=P.length-1;i>=0;i--)ctx.lineTo(P[i][0]+wd*(1-i/P.length)+1,P[i][1])},'#fffbe8',{sh:0,lw:2.4,ink:`rgba(150,170,255,${a})`});
  add(()=>{ctx.strokeStyle=`rgba(170,190,255,${.35*a})`;ctx.lineWidth=wd*5;ctx.lineJoin='round';ctx.beginPath();P.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke()})}
const flick=(t,F)=>F.c!=null?1:(.55+.45*Math.max(0,Math.sin(t*5.3)*Math.sin(t*2.1+1)));

const E={
 boulder:{s:1,f(w,t){const r=rng(5),P=[];for(let i=0;i<10;i++){const a=i/10*TAU,rr=w*.5*(.78+r()*.22);P.push([Math.cos(a)*rr,Math.sin(a)*rr*.72])}
  cutP(()=>{P.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath()},vg(-w*.36,w*.36,['#b4a49a','#7a6a62','#3e322e']),{blur:10,sy:6,lw:2.4});
  cutP(()=>{ctx.moveTo(P[5][0],P[5][1]);ctx.lineTo(P[6][0],P[6][1]);ctx.lineTo(P[7][0],P[7][1]);ctx.lineTo(-w*.05,-w*.05);ctx.closePath()},'rgba(255,240,220,.28)',{sh:0,lw:1});
  cutP(()=>{ctx.moveTo(P[1][0],P[1][1]);ctx.lineTo(P[2][0],P[2][1]);ctx.lineTo(w*.08,w*.08);ctx.closePath()},'rgba(20,10,30,.25)',{sh:0,lw:0});
  ctx.strokeStyle='rgba(30,16,20,.55)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-w*.1,-w*.2);ctx.lineTo(-w*.02,-w*.04);ctx.lineTo(-w*.12,w*.12);ctx.stroke()}},
 cloud_white_cluster:{s:1,am:2,f(w,t){ // two rows of paper puffs: a lighter back row, a fuller front row with rim light
  const row=(seed,y,rmin,rmax,cols,rim)=>{const r=rng(seed),P=[];let x=-w*.48;while(x<w*.48){const rr=w*(rmin+(rmax-rmin)*r())*(1-Math.abs(x/w)*.7);P.push([x+rr*.5,y-rr*.35+Math.sin(t*.25+x)*3,rr]);x+=rr*(.7+r()*.5)}
    cutU(()=>{P.forEach(([px,py,pr])=>{ctx.moveTo(px+pr,py);ctx.arc(px,py,pr,0,TAU)});ctx.rect(-w*.48,y,w*.96+P[P.length-1][2],w*.06)},vg(y-w*rmax,y+w*.06,cols),{blur:12,sy:6,lw:2.2});
    if(rim){ctx.strokeStyle='rgba(255,255,255,.75)';ctx.lineWidth=2.4;P.forEach(([px,py,pr])=>{if(pr<w*rmax*.7)return;ctx.beginPath();ctx.arc(px,py,pr-4,PI*1.1,PI*1.55);ctx.stroke()})}};
  row(3,-w*.04,.035,.07,['#ffffff','#eae4f8','#c8c0e4'],false);row(9,w*.03,.05,.095,['#ffffff','#f2eefc','#b4acd4'],true)}},
 crown_gold:{s:1,f(w,t){const h=w*.8,b=h*.3;add(()=>glow(0,0,w*.9,'255,210,120',.35));
  [[-.34,.55],[0,1],[.34,.55]].forEach(([u,k])=>cutP(()=>{const x=u*w,hh=h*k;ctx.moveTo(x-w*.17,b*.2);ctx.lineTo(x-w*.12,-hh*.45);ctx.quadraticCurveTo(x-w*.06,-hh*.75,x,-hh*.95);ctx.quadraticCurveTo(x+w*.06,-hh*.75,x+w*.12,-hh*.45);ctx.lineTo(x+w*.17,b*.2);ctx.closePath()},gold(-h,b),{blur:8,lw:2.2,ink:'rgba(90,40,0,.7)'}));
  cutP(()=>ctx.roundRect(-w*.5,0,w,b,6),gold(0,b),{blur:8,lw:2.2,ink:'rgba(90,40,0,.7)'});
  for(let i=0;i<7;i++){const x=(i-3)/3*w*.42;gem(x,b*.5,b*.22,i%2?'#18a57a':'#d0243a')}gem(0,-h*.5,w*.06,'#d0243a');gem(-w*.34,-h*.22,w*.04,'#2a6ad0');gem(w*.34,-h*.22,w*.04,'#2a6ad0');
  ctx.fillStyle='#fffbe8';for(let i=0;i<9;i++){ctx.beginPath();ctx.arc((i-4)/4*w*.46,b+5+Math.sin(t*2+i)*1.5,3.2,0,TAU);ctx.fill()}}},
 divine_rays:{s:0,f(w,t,F,a){const n=13,L=w*.75;for(let i=0;i<n;i++){const an=PI/2+(i-(n-1)/2)*.17+Math.sin(t*.3)*.03,sp=.045+.02*(i%2),k=.6+.4*Math.abs(Math.sin(t*.7+i*1.3));
   const rg=ctx.createRadialGradient(0,0,0,0,0,L);rg.addColorStop(0,i%2?`rgba(255,226,150,${.42*k})`:`rgba(255,250,225,${.5*k})`);rg.addColorStop(1,'rgba(255,240,200,0)');ctx.fillStyle=rg;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(an-sp)*L,Math.sin(an-sp)*L);ctx.lineTo(Math.cos(an+sp)*L,Math.sin(an+sp)*L);ctx.closePath();ctx.fill()}
   glow(0,0,w*.28,'255,240,200',.7)}},
 // reels (reel 4): a stream of round sand grains blowing away from (0,0) toward +x and up (w = length of the stream); "what slips away like sand"
 sand_drift:{s:0,f(w,t){for(let k=0;k<4;k++){const u=(k+.5)/4;glow(u*w,-u*u*w*.3,w*(.1+u*.1),'240,212,160',.16*(1-u*.6))}
  const r=rng(17);for(let i=0;i<80;i++){const ph=r(),sp=r()-.5,sz=1.8+r()*2.8,dk=r()<.35,u=((t*.38+ph)%1),x=u*w+Math.sin(t*2.2+i)*4*u,y=-u*u*w*.3+sp*w*.28*u+Math.cos(t*1.7+i)*3*u,al=Math.min(1,u*7)*(1-u)*1.3;
   if(al<=.02)continue;ctx.fillStyle=dk?`rgba(196,150,86,${Math.min(1,al)})`:`rgba(246,222,170,${Math.min(1,al)})`;ctx.beginPath();ctx.arc(x,y,sz*(1-u*.35),0,TAU);ctx.fill()}}},
 embers:{s:0,f(w,t){const r=rng(11);for(let i=0;i<46;i++){const ph=r(),u=((t*.22+ph)%1),x=(r()-.5)*w+Math.sin(t*1.3+i)*20,y=w*.3-u*w*.7,s=2+r()*4,al=Math.sin(u*PI);
   ctx.save();ctx.translate(x,y);ctx.rotate(t*2+i);ctx.fillStyle=`rgba(255,${120+((i*37)%90)},40,${al})`;ctx.beginPath();ctx.moveTo(0,-s);ctx.lineTo(s*.6,0);ctx.lineTo(0,s);ctx.lineTo(-s*.6,0);ctx.closePath();ctx.fill();ctx.restore();glow(x,y,s*4,'255,150,60',.25*al)}}},
 energy_swirl:{s:0,am:1.4,f(w,t){glow(0,0,w*.45,'200,160,255',.5);for(let k=0;k<4;k++){ctx.save();ctx.rotate(k*TAU/4);
   ctx.fillStyle=k%2?'rgba(255,210,140,.55)':'rgba(190,150,255,.55)';ctx.beginPath();for(let i=0;i<=30;i++){const u=i/30,R=w*.08+u*w*.42,an=u*3.2;ctx.lineTo(Math.cos(an)*R,Math.sin(an)*R)}for(let i=30;i>=0;i--){const u=i/30,R=w*.08+u*w*.42-w*.06*Math.sin(u*PI),an=u*3.2+.12;ctx.lineTo(Math.cos(an)*R,Math.sin(an)*R)}ctx.closePath();ctx.fill();ctx.restore()}
   glow(0,0,w*.14,'255,250,230',.8)}},
 flower_petals:{s:1,f(w,t,F,a,P){ // the KETAKI flower (screw-pine): long cream-gold bracts in a fan, golden spadix, saw-edged green leaves
  const wi=F.wc!=null?q(P,t,F.wc,F.wd||1.5):(F.wither||0),sw=Math.sin(t*1.2)*.04*(1-wi),h=w*1.05;ctx.save();ctx.translate(0,h*.25);
  if(F.glow!==0)add(()=>glow(0,-h*.35,w*.85,wi>.5?'200,150,120':'255,235,160',(F.glow??.45)*(1-wi*.7)));
  [[-1,.5],[1,.45],[-1,.25],[1,.2]].forEach(([sd,k])=>{ctx.save();ctx.rotate(sd*(.55+k*.4+wi*.4));cutP(()=>{ctx.moveTo(-w*.03,0);for(let i=0;i<=8;i++){const u=i/8;ctx.lineTo(-w*.035*(1-u)+(i%2?-3:0),-u*h*.6)}for(let i=8;i>=0;i--){const u=i/8;ctx.lineTo(w*.035*(1-u)+(i%2?3:0),-u*h*.6)}ctx.closePath()},vg(-h*.6,0,[mix('#7ab04a','#7a6a3a',wi),mix('#2e6a2a','#4a3a1a',wi)]),{blur:6,lw:1.6});ctx.restore()});
  const n=9;for(let i=0;i<n;i++){const u=(i-(n-1)/2)/((n-1)/2),an=u*(.62+wi*.55)+sw,L=h*(.78-Math.abs(u)*.22)*(1-wi*.15),bw=w*.075;ctx.save();ctx.rotate(an);
   const c1=mix(i%2?'#fff6d0':'#f8e8a8','#a8845a',wi),c2=mix('#e8c860','#6a4a2a',wi);cutP(()=>{ctx.moveTo(-bw,0);ctx.quadraticCurveTo(-bw*1.3,-L*.55,0,-L);ctx.quadraticCurveTo(bw*1.3,-L*.55,bw,0);ctx.closePath()},vg(-L,0,[c1,c1,c2]),{blur:6,sy:3,lw:1.6});
   ctx.strokeStyle=`rgba(150,110,40,${.4*(1-wi*.5)})`;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(0,-6);ctx.lineTo(0,-L*.85);ctx.stroke();ctx.restore()}
  const m=n%2;for(let i=0;i<5;i++){const u=(i-2)/2,an=u*.35+sw,L=h*.5;ctx.save();ctx.rotate(an);cutP(()=>{ctx.moveTo(-w*.05,0);ctx.quadraticCurveTo(-w*.07,-L*.5,0,-L);ctx.quadraticCurveTo(w*.07,-L*.5,w*.05,0);ctx.closePath()},vg(-L,0,[mix('#ffffff','#c8a070',wi),mix('#f6dc80','#8a6a3a',wi)]),{blur:4,sy:2,lw:1.4});ctx.restore()}
  cutP(()=>ctx.ellipse(0,-h*.22,w*.05,h*.2,sw,0,TAU),vg(-h*.42,0,[mix('#ffe070','#9a7040',wi),mix('#d89020','#5a3a1a',wi)]),{blur:4,lw:1.4});
  ctx.fillStyle=`rgba(255,250,200,${1-wi})`;for(let i=0;i<14;i++){ctx.beginPath();ctx.arc(Math.sin(i*2.4)*w*.03,-h*.06-i*h*.025,1.6,0,TAU);ctx.fill()}
  if(F.fall||wi>.4){const r=rng(3);for(let i=0;i<6;i++){const u=((t*.35+r())%1),x=(r()-.5)*w*.8+Math.sin(t*2+i)*14,y=-h*.4+u*h*1.1;ctx.save();ctx.globalAlpha*=Math.sin(u*PI);ctx.translate(x,y);ctx.rotate(t*2+i);cutP(()=>ctx.ellipse(0,0,w*.025,w*.07,0,0,TAU),mix('#f8e8a8','#a8845a',wi),{sh:0,lw:1});ctx.restore()}}
  ctx.restore()}},
 ground_crack:{s:1,f(w,t,F,a){const r=rng(7),g=Math.min(1,a*1.05),br=(x0,y0,dir,len,dep)=>{let x=x0,y=y0;const P=[[x,y]];const st=8;for(let i=0;i<st;i++){x+=dir*len/st*g;y+=(r()-.5)*len*.12;P.push([x,y])}
   ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle='rgba(20,6,6,.9)';ctx.lineWidth=(10-dep*3);ctx.beginPath();P.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();
   add(()=>{ctx.strokeStyle='rgba(255,120,40,.9)';ctx.lineWidth=(4-dep);ctx.stroke();ctx.strokeStyle='rgba(255,200,120,.35)';ctx.lineWidth=14-dep*4;ctx.stroke()});
   if(dep<2)for(let k=2;k<P.length;k+=3)br(P[k][0],P[k][1],dir,len*.35,dep+1)};
  br(0,0,1,w*.5,0);br(0,0,-1,w*.5,0);add(()=>glow(0,0,w*.3*g,'255,110,40',.35));
  for(let i=0;i<10;i++){const x=(r()-.5)*w*g,y=-6-r()*10-g*8*Math.sin(t*3+i);cutP(()=>{ctx.moveTo(x-6,y);ctx.lineTo(x,y-7);ctx.lineTo(x+6,y);ctx.closePath()},'#6a5048',{sh:0,lw:1})}}},
 halo_ring:{s:0,am:1.3,f(w,t){const R=w*.36;glow(0,0,w*.5,'255,220,150',.35);ctx.save();ctx.rotate(t*.15);ctx.strokeStyle='rgba(255,226,150,.9)';ctx.lineWidth=w*.018;ctx.beginPath();ctx.arc(0,0,R,0,TAU);ctx.stroke();
  ctx.fillStyle='rgba(255,240,190,.7)';const n=32;for(let i=0;i<n;i++){ctx.save();ctx.rotate(i/n*TAU);ctx.beginPath();ctx.moveTo(-w*.012,-R);ctx.quadraticCurveTo(0,-R-w*.07,w*.012,-R);ctx.fill();ctx.restore()}
  ctx.setLineDash([2,7]);ctx.lineWidth=2;ctx.strokeStyle='rgba(255,250,225,.8)';ctx.beginPath();ctx.arc(0,0,R*.9,0,TAU);ctx.stroke();ctx.restore()}},
 havan_kund:{s:1,f(w,t){const h=w*.3;[[1,0],[.8,-h*.33],[.62,-h*.62]].forEach(([k,y],i)=>cutP(()=>ctx.rect(-w*k/2,y,w*k,h*.36),vg(y,y+h*.36,[['#c8784a','#b8683a','#a85a30'][i],'#6a3018']),{blur:8,lw:2}));
  ctx.strokeStyle='#f2c14e';ctx.lineWidth=3;[[1,0],[.8,-h*.33],[.62,-h*.62]].forEach(([k,y])=>{ctx.beginPath();ctx.moveTo(-w*k/2,y+2);ctx.lineTo(w*k/2,y+2);ctx.stroke()});
  ctx.fillStyle='#e8e0d0';for(let i=0;i<6;i++){ctx.beginPath();ctx.arc(-w*.4+i*w*.16,h*.18,4,0,TAU);ctx.fill()}
  fireBank(0,-h*.6,w*.5,w*.55,t,1);for(let i=0;i<5;i++){const u=(t*.2+i/5)%1;ctx.fillStyle=`rgba(200,190,185,${.25*(1-u)})`;ctx.beginPath();ctx.ellipse(Math.sin(t+i*2)*20,-h*.6-w*.5-u*w*.6,20+u*50,14+u*30,0,0,TAU);ctx.fill()}}},
 light_beam:{s:0,f(w,t){const top=-900,bot=w*.6,g=ctx.createLinearGradient(-w/2,0,w/2,0);g.addColorStop(0,'rgba(255,240,190,0)');g.addColorStop(.3,'rgba(255,240,190,.45)');g.addColorStop(.5,'rgba(255,255,240,.85)');g.addColorStop(.7,'rgba(255,240,190,.45)');g.addColorStop(1,'rgba(255,240,190,0)');
  ctx.fillStyle=g;ctx.fillRect(-w/2,top,w,bot-top);glow(0,bot,w*.8,'255,230,160',.5);for(let i=0;i<14;i++){const u=(t*.3+i/14)%1;ctx.fillStyle=`rgba(255,250,220,${.8*Math.sin(u*PI)})`;ctx.beginPath();ctx.arc(Math.sin(i*3.1)*w*.3,bot-u*(bot-top)*.6,2.4,0,TAU);ctx.fill()}}},
 lightning_bolt_a:{s:0,f(w,t,F){const k=flick(t,F),P=boltPts(17+Math.floor(t*3)%3,w*1.2,w*.35,9);ctx.translate(0,-w*.6);ctx.globalAlpha*=k;boltDraw(P,w*.025,1)}},
 lightning_forks:{s:0,f(w,t,F){const k=flick(t,F),sd=23+Math.floor(t*3)%3,P=boltPts(sd,w*1.1,w*.35,10);ctx.translate(0,-w*.55);ctx.globalAlpha*=k;boltDraw(P,w*.022,1);
  [3,5,7].forEach((j,i)=>{const Q=boltPts(sd+i*5,w*.45,w*.25,5).map(([x,y])=>[P[j][0]+x+(i%2?1:-1)*y*.6,P[j][1]+y*.8]);boltDraw(Q,w*.012,.8)})}},
 magic_circle:{s:0,am:1.2,f(w,t){const R=w*.48;glow(0,0,R*1.1,'255,200,120',.3);ctx.strokeStyle='rgba(255,214,140,.95)';ctx.lineWidth=Math.max(2,w*.008);
  [1,.9,.62].forEach(k=>{ctx.beginPath();ctx.arc(0,0,R*k,0,TAU);ctx.stroke()});const n=16;for(let i=0;i<n;i++){ctx.save();ctx.rotate(i/n*TAU);ctx.beginPath();ctx.moveTo(-R*.1,-R*.62);ctx.quadraticCurveTo(0,-R*.98,R*.1,-R*.62);ctx.stroke();ctx.restore()}
  [0,PI].forEach(o=>{ctx.beginPath();for(let i=0;i<3;i++){const an=o-PI/2+i*TAU/3;ctx.lineTo(Math.cos(an)*R*.58,Math.sin(an)*R*.58)}ctx.closePath();ctx.stroke()});ctx.fillStyle='rgba(255,240,200,.9)';ctx.beginPath();ctx.arc(0,0,R*.05,0,TAU);ctx.fill()}},
 mandara_mountain:{s:1,f(w,t){const h=w*1.15,P=[[-w*.5,h*.45],[-w*.3,0],[-w*.16,-h*.3],[-w*.06,-h*.55],[w*.04,-h*.55],[w*.16,-h*.25],[w*.3,0],[w*.5,h*.45]];
  cutP(()=>{P.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath()},vg(-h*.55,h*.45,['#8a9ad0','#4a6a8a','#22384a']),{blur:10,lw:2.2});
  cutP(()=>{ctx.moveTo(-w*.01,-h*.55);ctx.lineTo(w*.04,-h*.55);ctx.lineTo(w*.16,-h*.25);ctx.lineTo(w*.3,0);ctx.lineTo(w*.5,h*.45);ctx.lineTo(w*.05,h*.45);ctx.closePath()},'rgba(10,4,30,.2)',{sh:0,lw:0});
  cutP(()=>{ctx.moveTo(-w*.06,-h*.55);ctx.lineTo(w*.04,-h*.55);ctx.lineTo(w*.1,-h*.4);ctx.lineTo(w*.03,-h*.44);ctx.lineTo(-w*.04,-h*.38);ctx.lineTo(-w*.11,-h*.42);ctx.closePath()},'#f6f8ff',{sh:0,lw:1.2});
  for(let i=0;i<9;i++){const u=i/8,x=-w*.36+u*w*.72,y=h*.3-Math.abs(u-.5)*h*.1;PS.OBJ.tree(x,y,.22,t,{kind:'pine',col:'#2a5a44'})}
  PS.OBJ.cloud(-w*.25,h*.02,w/500,t,{col:'#f4f0ff'});PS.OBJ.cloud(w*.24,-h*.12,w/620,t,{col:'#f4f0ff'})}},
 mist_wisps:{s:0,am:1.8,f(w,t){for(let k=0;k<4;k++){const y=(k-1.5)*w*.07,dx=Math.sin(t*.25+k)*w*.06;ctx.fillStyle=`rgba(240,236,255,${.32-k*.05})`;ctx.beginPath();ctx.moveTo(-w*.5+dx,y);
  for(let i=0;i<=10;i++){const u=i/10;ctx.lineTo(-w*.5+dx+u*w,y-Math.sin(u*PI)*w*.05-Math.sin(u*9+t+k)*5)}for(let i=10;i>=0;i--){const u=i/10;ctx.lineTo(-w*.5+dx+u*w,y+Math.sin(u*PI)*w*.03)}ctx.closePath();ctx.fill()}}},
 om_symbol:{s:1,f(w,t){add(()=>glow(0,0,w*.7,'255,200,110',.55));const sz=w*.85;ctx.font=`700 ${sz}px NSer, serif`;ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.save();ctx.shadowColor='rgba(40,10,0,.6)';ctx.shadowBlur=14*SC_;ctx.shadowOffsetY=6*SC_;ctx.lineWidth=sz*.05;ctx.strokeStyle='#5a2a08';ctx.lineJoin='round';ctx.strokeText('ॐ',0,0);ctx.restore();
  ctx.fillStyle=gold(-sz*.4,sz*.4);ctx.fillText('ॐ',0,0);ctx.lineWidth=2;ctx.strokeStyle='rgba(255,250,220,.6)';ctx.strokeText('ॐ',-1,-1)}},
 palace_gate:{s:1,f(w,t){const h=w*1.3,bw=w*.9,by=h*.5,gy=h*.05;   // temple gateway (gopuram): tiered tower over a doorway
  for(let i=0;i<5;i++){const k=1-i*.16,y0=gy-i*h*.1;cutP(()=>{ctx.moveTo(-bw*k/2,y0);ctx.lineTo(-bw*k*.44,y0-h*.1);ctx.lineTo(bw*k*.44,y0-h*.1);ctx.lineTo(bw*k/2,y0);ctx.closePath()},vg(y0-h*.1,y0,[['#f0c890','#e8b878','#e0a868','#d89858','#d08848'][i],'#8a5a30']),{blur:7,lw:1.8});
   ctx.fillStyle='rgba(90,40,20,.45)';for(let j=-2;j<=2;j++)ctx.fillRect(j*bw*k*.16-3,y0-h*.075,6,h*.05)}
  const ty=gy-h*.5;cutP(()=>{ctx.moveTo(-bw*.2,ty+4);ctx.quadraticCurveTo(0,ty-h*.12,bw*.2,ty+4);ctx.closePath()},gold(ty-h*.12,ty),{blur:6,lw:1.6});cutP(()=>ctx.ellipse(0,ty-h*.12,w*.03,w*.05,0,0,TAU),gold(ty-h*.17,ty-h*.07),{sh:0,lw:1.2});
  cutP(()=>{ctx.moveTo(0,ty-h*.16);ctx.lineTo(0,ty-h*.3);ctx.lineTo(w*.14+Math.sin(t*3)*4,ty-h*.26);ctx.lineTo(0,ty-h*.22)},'#ef8a1f',{sh:0,lw:1.4});
  cutP(()=>{ctx.rect(-bw/2,gy,bw,by-gy)},vg(gy,by,['#e8c08a','#a8784a']),{blur:9,lw:2});
  cutP(()=>{ctx.moveTo(-bw*.2,by);ctx.lineTo(-bw*.2,gy+h*.17);ctx.quadraticCurveTo(0,gy+h*.04,bw*.2,gy+h*.17);ctx.lineTo(bw*.2,by);ctx.closePath()},vg(gy,by,['#ffd890','#a85a20','#3a1a10']),{sh:0,lw:2.4,ink:'#e0b04a'});
  [-1,1].forEach(sd=>PS.OBJ.pillar(sd*bw*.34,by,h/1400,t,{h:300,w:60}))}},
 red_energy_pulse:{s:0,f(w,t){glow(0,0,w*.45,'255,40,30',.45);for(let i=0;i<4;i++){const u=(t*.6+i/4)%1;ctx.strokeStyle=`rgba(255,${60+i*20},40,${.85*(1-u)})`;ctx.lineWidth=10*(1-u)+2;ctx.beginPath();
  for(let j=0;j<=48;j++){const an=j/48*TAU,R=w*.5*u*(1+.06*Math.sin(an*9+t*4));ctx.lineTo(Math.cos(an)*R,Math.sin(an)*R*.55)}ctx.closePath();ctx.stroke()}}},
 smoke_plume:{s:1,am:1.1,f(w,t){ // one rising paper silhouette of billows; top billows shrink as they rise
  const B=[];for(let i=0;i<9;i++){const u=(t*.12+i/9)%1,x=Math.sin(t*.6+i*1.7)*w*.12+u*w*.1,y=w*.1-u*w*.75,R=w*(.07+u*.14)*Math.min(1,(1-u)*3);if(R>2)B.push([x,y,R])}
  const path=()=>B.forEach(([x,y,R])=>[[0,0,1],[-.6,.2,.7],[.6,.25,.75]].forEach(([dx,dy,k])=>{ctx.moveTo(x+dx*R+R*k,y+dy*R);ctx.arc(x+dx*R,y+dy*R,R*k,0,TAU)}));
  cutU(path,vg(-w*.7,w*.2,['#efeaf0','#bab2c0','#7a7084']),{blur:8,lw:1.4,ink:'rgba(40,30,50,.35)'});
  ctx.strokeStyle='rgba(255,255,255,.45)';ctx.lineWidth=2;B.forEach(([x,y,R])=>{ctx.beginPath();ctx.arc(x,y,R-3,PI*1.1,PI*1.5);ctx.stroke()})}},
 sudarshan_chakra:{s:1,f(w,t){const R=w*.46;add(()=>{glow(0,0,R*1.6,'255,170,60',.5);glow(0,0,R*.9,'255,230,150',.4)});const n=28;
  cutP(()=>{for(let i=0;i<n;i++){const a0=i/n*TAU,a1=(i+.5)/n*TAU,a2=(i+1)/n*TAU;ctx.lineTo(Math.cos(a0)*R*.86,Math.sin(a0)*R*.86);ctx.lineTo(Math.cos(a1)*R,Math.sin(a1)*R);ctx.lineTo(Math.cos(a2)*R*.86,Math.sin(a2)*R*.86)}ctx.closePath()},gold(-R,R),{blur:10,lw:2,ink:'rgba(110,50,0,.7)'});
  cutP(()=>{ctx.arc(0,0,R*.78,0,TAU);ctx.moveTo(R*.6,0);ctx.arc(0,0,R*.6,0,TAU,true)},vg(-R,R,['#ffe9a0','#d8962a']),{sh:0,lw:1.6,ink:'rgba(110,50,0,.6)'});
  for(let i=0;i<12;i++){ctx.save();ctx.rotate(i/12*TAU);cutP(()=>{ctx.moveTo(-R*.04,-R*.18);ctx.lineTo(0,-R*.62);ctx.lineTo(R*.04,-R*.18);ctx.closePath()},'#f2c14e',{sh:0,lw:1.2,ink:'rgba(110,50,0,.6)'});ctx.restore()}
  cutP(()=>ctx.arc(0,0,R*.2,0,TAU),gold(-R*.2,R*.2),{sh:0,lw:1.6});gem(0,0,R*.09,'#d0243a')}},
 water_splash:{s:1,f(w,t){const u=(t*.8)%1.4,k=Math.min(1,u);cutP(()=>{ctx.moveTo(-w*.1,w*.15);ctx.quadraticCurveTo(-w*.04,-w*.2*k,0,-w*.32*k);ctx.quadraticCurveTo(w*.04,-w*.2*k,w*.1,w*.15);ctx.closePath()},vg(-w*.3,w*.15,['#e8f6ff','#5aa8e0']),{blur:6,lw:1.6,ink:'rgba(10,40,90,.5)'});
  for(let i=0;i<11;i++){const an=-PI/2+(i-5)*.26,d=w*(.18+.3*k),x=Math.cos(an)*d,y=Math.sin(an)*d*.8+k*k*w*.15,s=w*.022*(1.2-Math.abs(i-5)*.08);ctx.save();ctx.translate(x,y);ctx.rotate(an+PI/2);cutP(()=>{ctx.moveTo(0,-s*2.2);ctx.quadraticCurveTo(s,0,0,s);ctx.quadraticCurveTo(-s,0,0,-s*2.2)},vg(-s*2,s,['#ffffff','#7ac0f0']),{sh:0,lw:1.2,ink:'rgba(10,40,90,.5)'});ctx.restore()}
  cutP(()=>ctx.ellipse(0,w*.15,w*.42,w*.06,0,0,TAU),'rgba(230,246,255,.85)',{sh:0,lw:1.6,ink:'rgba(10,40,90,.4)'})}},
 wave_ocean:{s:1,f(w,t){const h=w*.42,s=Math.sin(t*1.1)*w*.02;cutP(()=>{ctx.moveTo(-w*.5,h*.5);ctx.lineTo(-w*.5,h*.05);ctx.bezierCurveTo(-w*.2,-h*.1+s,w*.05,-h*.75+s,w*.22,-h*.55+s);ctx.bezierCurveTo(w*.34,-h*.42+s,w*.3,-h*.2,w*.18,-h*.22);
   ctx.bezierCurveTo(w*.26,-h*.05,w*.38,h*.05,w*.5,h*.1);ctx.lineTo(w*.5,h*.5);ctx.closePath()},(()=>{const g=ctx.createLinearGradient(0,-h*.7,0,h*.5);g.addColorStop(0,'#5ab0e8');g.addColorStop(.55,'#1a5aa0');g.addColorStop(1,'rgba(10,42,90,0)');return g})(),{blur:10,lw:2.2,ink:'rgba(5,20,60,.6)'});
  cutP(()=>{ctx.moveTo(w*.02,-h*.6+s);ctx.bezierCurveTo(w*.12,-h*.78+s,w*.32,-h*.6+s,w*.28,-h*.34);ctx.bezierCurveTo(w*.24,-h*.5+s,w*.14,-h*.58+s,w*.02,-h*.6+s)},'#f2faff',{sh:0,lw:1.6});
  ctx.strokeStyle='rgba(230,246,255,.7)';ctx.lineWidth=2.4;for(let i=0;i<4;i++){ctx.beginPath();ctx.moveTo(-w*.45+i*w*.12,h*(.12+i*.08));ctx.quadraticCurveTo(-w*.35+i*w*.12,h*(.04+i*.08)+Math.sin(t*2+i)*4,-w*.25+i*w*.12,h*(.12+i*.08));ctx.stroke()}
  for(let i=0;i<7;i++){ctx.fillStyle='#ffffff';ctx.beginPath();ctx.arc(w*(.04+i*.04),-h*(.66-Math.sin(i)*.05)+s-Math.abs(Math.sin(t*3+i))*8,3+i%3,0,TAU);ctx.fill()}}},
 // reels 15/09/10 (drawn by engine/v2_cast.js REELFX): amrut_pot (x,y = centre) · fire_ring (part:'back'|'front' to put a pot or Garuda inside) · spinning_blades (sp = rad/s)
 // golden_feather (fall:1 sways; use vy to drop) · vajra_thrown (flies toward +x with a lightning trail; flip:-1 flies left) · ash_pile (h 0..1)
 // embryo (cry 0..1) · womb_view (n 0|1|7|49, spread, cry, flash 0..1) · maruta_pieces (n 7|49, spread 0..1, cry, born:1 = crying babies)
 amrut_pot:{s:1,f(w,t,F){V2.FX.amrut_pot(ctx,w,t,F)}},
 fire_ring:{s:0,f(w,t,F){V2.FX.fire_ring(ctx,w,t,F)}},
 spinning_blades:{s:1,f(w,t,F){V2.FX.spinning_blades(ctx,w,t,F)}},
 golden_feather:{s:1,f(w,t,F){V2.FX.golden_feather(ctx,w,t,F)}},
 vajra_thrown:{s:0,f(w,t,F){V2.FX.vajra_thrown(ctx,w,t,F)}},
 ash_pile:{s:1,f(w,t,F){V2.FX.ash_pile(ctx,w,t,F)}},
 embryo:{s:0,f(w,t,F){V2.FX.embryo(ctx,w,t,F)}},
 womb_view:{s:0,f(w,t,F){V2.FX.womb_view(ctx,w,t,F)}},
 maruta_pieces:{s:0,f(w,t,F){V2.FX.maruta_pieces(ctx,w,t,F)}},
 // EP07 dark look (Nov 2026). demon_crowd: rows of black asura silhouettes with ember eyes (rows 1-3, n per row, w = width, seed, sway, eyes 0..1, haze = smoke colour; x,y = middle of the front row's feet)
 demon_crowd:{s:0,f(w,t,F){const rows=F.rows||2,n=F.n||8,hz=F.haze||'#5a2414';for(let k=rows-1;k>=0;k--){const sc=1-k*.22;OBJ.demons(0,-k*34,sc*(F.sc||1),t,{n:Math.round(n*(1+k*.35)),w:w/sc,seed:(F.seed||3)+k*17,fog:k*.28,haze:hz,eyes:F.eyes??1,sway:F.sway})}}},
 // smoke_bank: a dark rolling smoke band (w wide, h tall, col, v drift speed)
 smoke_bank:{s:0,f(w,t,F){OBJ.smoke(0,0,1,t,{w:w,h:F.h||w*.1,col:F.col||'#2a1814',a:1,seed:F.seed||5,v:F.v??10})}},
 // ember_fire: a matte paper campfire of crossed branches (fire 0..1 = how high it burns; logs:false hides the wood); x,y = base
 ember_fire:{s:0,f(w,t,F){const k=F.fire??1,h=w*.9*k;glow(0,-h*.35,w*1.1,'255,120,40',.35*k);
  const logs=[[-.5,.06,.42,-.22],[-.45,-.12,.5,.1],[-.2,.1,.15,-.3],[.3,.08,-.1,-.32]];if(F.logs!==false)logs.forEach(([a,b,c2,d2])=>{ctx.save();ctx.lineCap='round';ctx.strokeStyle='#1a0c06';ctx.lineWidth=w*.1;ctx.beginPath();ctx.moveTo(a*w,b*w);ctx.lineTo(c2*w,d2*w);ctx.stroke();ctx.strokeStyle='#4a2a16';ctx.lineWidth=w*.07;ctx.stroke();ctx.strokeStyle='rgba(255,110,40,.5)';ctx.lineWidth=w*.015;ctx.setLineDash([w*.03,w*.05]);ctx.stroke();ctx.restore()});
  for(let i=0;i<7;i++){const x=(i-3)*w*.09,f=Math.sin(t*7+i*1.9)*w*.04,hh=h*(.55+.45*Math.abs(Math.sin(i*2.1)))*(.85+.15*Math.sin(t*9+i));if(hh<2)continue;
   [[1,['#f0a040','#d8501a','#7a140a']],[.55,['#fff0b0','#ffc050','#e8761c']]].forEach(([q,cols])=>cutP(()=>{ctx.moveTo(x-w*.07*q,0);ctx.quadraticCurveTo(x-w*.08*q+f,-hh*.55*q,x+f*1.4,-hh*q);ctx.quadraticCurveTo(x+w*.08*q+f,-hh*.55*q,x+w*.07*q,0);ctx.closePath()},vg(-hh*q,0,cols),{sh:0,lw:1,ink:'rgba(80,10,0,.55)'}))}
  for(let i=0;i<14;i++){const u=(t*.35+i/14)%1;ctx.fillStyle=`rgba(255,${120+(i*23)%90},40,${(1-u)*.9})`;ctx.beginPath();ctx.arc(Math.sin(i*3.3+t)*w*.3*u,-h*.6-u*w*.9,1.4+(i%3)*.6,0,TAU);ctx.fill()}
  if(F.smoke!==false){ctx.save();ctx.globalAlpha*=.5;OBJ.smoke(0,-h-w*.3,.5,t,{w:w*2.2,h:w*.35,col:'#3a2620',a:.7,seed:4,v:6});ctx.restore()}}},
 // curse_glow: a matte red (or col:'violet') ring of jagged rays around a hand or a figure (pulses)
 curse_glow:{s:0,f(w,t,F){const R=w*.5,rgb=F.col==='violet'?'150,70,200':(F.rgb||'200,30,20'),pu=.8+.2*Math.sin(t*4);glow(0,0,R*1.1,rgb,.45*pu);
  ctx.save();ctx.rotate(t*.4);for(let i=0;i<18;i++){ctx.save();ctx.rotate(i/18*TAU);const L=R*(.7+.3*Math.abs(Math.sin(i*1.7+t*2)));cutP(()=>{ctx.moveTo(-R*.035,-R*.35);ctx.lineTo(R*.02,-L*.7);ctx.lineTo(-R*.01,-L*.72);ctx.lineTo(0,-L);ctx.lineTo(R*.035,-R*.35);ctx.closePath()},`rgba(${rgb},.8)`,{sh:0,lw:1,ink:'rgba(30,0,0,.6)'});ctx.restore()}ctx.restore();
  ctx.strokeStyle=`rgba(${rgb},.9)`;ctx.lineWidth=w*.02;ctx.setLineDash([w*.04,w*.03]);ctx.beginPath();ctx.arc(0,0,R*.34,0,TAU);ctx.stroke();ctx.setLineDash([])}},
 // ash_speck: a few black ash flakes (the speck on the guru's lips / on a fingertip)
 // sacred_thread: the red-gold raksha cord tied on Kacha's wrist (insert close-up; tied 0..1 closes the knot)
 sacred_thread:{s:0,f(w,t,F){const k=F.tied??1,R=w*.32;ctx.save();ctx.lineCap='round';[['#6a0c0c',w*.075],['#c42820',w*.055]].forEach(([c2,lw])=>{ctx.strokeStyle=c2;ctx.lineWidth=lw;ctx.beginPath();ctx.ellipse(0,0,R,R*.36,0,.15,.15+(PI*2-.3)*k);ctx.stroke()});
  ctx.strokeStyle='#e8b040';ctx.lineWidth=w*.014;ctx.setLineDash([w*.025,w*.03]);ctx.beginPath();ctx.ellipse(0,0,R,R*.36,0,.15,.15+(PI*2-.3)*k);ctx.stroke();ctx.setLineDash([]);
  const sw=Math.sin(t*2)*w*.02;[[-1,.5],[1,.62]].forEach(([sd,L])=>{ctx.strokeStyle='#c42820';ctx.lineWidth=w*.04;ctx.beginPath();ctx.moveTo(R*.98,0);ctx.quadraticCurveTo(R*1.15,sd*w*.1,R*1.1+sw,sd*w*L*.5);ctx.stroke();cutP(()=>ctx.ellipse(R*1.1+sw,sd*w*L*.5+sd*w*.03,w*.03,w*.045,0,0,TAU),'#e8b040',{sh:0,lw:1})});
  cutP(()=>ctx.ellipse(R,0,w*.06,w*.05,0,0,TAU),'#a81818',{sh:0,lw:1.2,ink:'#3a0404'});ctx.restore()}},
 // reel 8: a drawn bow with its string (F.cut 0..1: the string thins as termites chew it, then SNAPS at 1 and the two ends whip apart)
 bowstring:{s:0,f(w,t,F){const k=F.snapk??0,h=w*.62,snap=k>=.98,thin=Math.max(.25,1-k*.8);ctx.save();ctx.lineCap='round';
  ctx.strokeStyle='#1a0c06';ctx.lineWidth=w*.07;ctx.beginPath();ctx.moveTo(w*.46,-h*.5);ctx.quadraticCurveTo(-w*.22,0,w*.46,h*.5);ctx.stroke();
  ctx.strokeStyle='#8a5a2a';ctx.lineWidth=w*.045;ctx.beginPath();ctx.moveTo(w*.46,-h*.5);ctx.quadraticCurveTo(-w*.22,0,w*.46,h*.5);ctx.stroke();
  ctx.strokeStyle='#f0e4c8';ctx.lineWidth=Math.max(1.2,w*.016*thin);
  if(!snap){ctx.beginPath();ctx.moveTo(w*.46,-h*.5);ctx.lineTo(w*.46,h*.5);ctx.stroke()}
  else{const a=Math.sin(t*14)*w*.02;ctx.beginPath();ctx.moveTo(w*.46,-h*.5);ctx.quadraticCurveTo(w*.1+a,-h*.2,-w*.02,-h*.34);ctx.stroke();ctx.beginPath();ctx.moveTo(w*.46,h*.5);ctx.quadraticCurveTo(w*.3-a,h*.22,w*.12,h*.4);ctx.stroke();
   glow(w*.46,0,w*.5,'255,240,200',.5)}ctx.restore()}},
 // reel 8: a swarm of little golden termites (the gods in disguise); F.n count, F.along 0..1 gathers them on the bowstring
 termite_swarm:{s:0,f(w,t,F){const n=F.cnt||14,r=rng(21),al=F.gath??.6;for(let i=0;i<n;i++){const u=r(),ph=r()*6,bx=(r()-.5)*w*.9,by=(r()-.5)*w*.7,tx=w*.46*.0+(u-.5)*0*w,ty=-w*.31+u*w*.62;
   const x=bx*(1-al)+(w*.46-Math.abs(u-.5)*0)*al+Math.sin(t*3+ph)*w*.012,y=by*(1-al)+ty*al+Math.cos(t*3+ph)*w*.01,sz=w*(.045+r()*.02),ang=al>.5?Math.PI/2:r()*6;
   ctx.save();ctx.translate(x,y);ctx.rotate(ang);
   ctx.strokeStyle='#3a2410';ctx.lineWidth=Math.max(1,sz*.12);for(let l=-1;l<=1;l++){ctx.beginPath();ctx.moveTo(l*sz*.35,-sz*.2);ctx.lineTo(l*sz*.5,-sz*.62);ctx.moveTo(l*sz*.35,sz*.2);ctx.lineTo(l*sz*.5,sz*.62);ctx.stroke()}
   cutP(()=>ctx.ellipse(-sz*.7,0,sz*.5,sz*.34,0,0,TAU),'#e0c070',{sh:0,lw:1,ink:'#3a2410'});cutP(()=>ctx.ellipse(0,0,sz*.55,sz*.4,0,0,TAU),'#d8b060',{sh:0,lw:1,ink:'#3a2410'});cutP(()=>ctx.ellipse(sz*.72,0,sz*.38,sz*.32,0,0,TAU),'#9a6a30',{sh:0,lw:1,ink:'#3a2410'});
   cutP(()=>{ctx.moveTo(sz*.62,-sz*.3);ctx.lineTo(sz*.72,-sz*.62);ctx.lineTo(sz*.86,-sz*.3);ctx.closePath()},'#f2c14e',{sh:0,lw:.8,ink:'#5a3a10'});
   ctx.restore()}}},
 ash_speck:{s:0,f(w,t){const r=rng(9);for(let i=0;i<7;i++){const x=(r()-.5)*w,y=(r()-.5)*w*.5,sz=w*(.05+r()*.07);cutP(()=>{ctx.moveTo(x-sz,y);ctx.lineTo(x-sz*.2,y-sz*.8);ctx.lineTo(x+sz,y-sz*.2);ctx.lineTo(x+sz*.3,y+sz*.7);ctx.closePath()},'#141010',{sh:0,lw:.6,ink:'rgba(120,110,100,.5)'})}}},
 // props drawn by engine/v2_cast.js (also figure prop keys): wine_cup (ash 0..1 swirl), burnt_cloth, palm_leaf (glow 0..1, rot), blood_splash (dark-red paper drops; n, spread), wild_flowers
 wine_cup:{s:0,f(w,t,F){V2.FX.wine_cup(ctx,w,t,F)}},
 burnt_cloth:{s:0,f(w,t,F){V2.FX.burnt_cloth(ctx,w,t,F)}},
 palm_leaf:{s:0,f(w,t,F){V2.FX.palm_leaf(ctx,w,t,F)}},
 blood_splash:{s:0,f(w,t,F){V2.FX.blood_splash(ctx,w,t,F)}},
 wild_flowers:{s:0,f(w,t,F){V2.FX.wild_flowers(ctx,w,t,F)}},
 whirlpool_churn:{s:0,am:1.8,f(w,t){ctx.save();ctx.scale(1,.5);glow(0,0,w*.5,'90,170,230',.35);for(let k=0;k<5;k++){ctx.save();ctx.rotate(k*TAU/5);ctx.strokeStyle=k%2?'rgba(170,225,255,.75)':'rgba(60,140,210,.8)';ctx.lineWidth=w*.03*(1-k*.08);ctx.lineCap='round';ctx.beginPath();
  for(let i=0;i<=40;i++){const u=i/40,R=w*.48*(1-u),an=u*4.4;ctx.lineTo(Math.cos(an)*R,Math.sin(an)*R)}ctx.stroke();ctx.restore()}glow(0,0,w*.1,'10,30,70',.8);ctx.restore()}}
};
window.PFX=E;
/* looks: a shot preset chosen by its grade name (shot.look or shot.grade = 'ep07_dark'): soft-light tint, heavy vignette, low bloom, and for
   every figure (unless the figure sets its own): warm firelight key + soft ember rim + matte filter (less saturation, no gloss) */
window.LOOKS={ep07_dark:{grade:'rgba(150,60,20,0.26)',vig:.66,bloom:.02,key:'255,140,70',rim:'rgba(255,140,70,.38)',filt:'saturate(.78) brightness(.9) contrast(1.05)'}};
function pfxName(F){if(F.k)return F.k;const s=String(F.src||'').split('/').pop().replace(/\.png$/,'');return s.replace(/^fx_/,'')}
FXV2.pfx=FXV2.fximg=function(F,t,P,d,a){const nm=pfxName(F),e=E[nm];if(!e){(window.FX_ERRORS=window.FX_ERRORS||[]);const m='pfx: unknown effect '+nm;if(window.FX_ERRORS.indexOf(m)<0)window.FX_ERRORS.push(m);return}
  if(F.par!=null&&!F._in){layer(F.par,()=>FXV2.pfx(Object.assign({},F,{_in:1,par:null}),t,P,d,a));return}
  const al=Math.min(1,a*(F.alpha==null?1:F.alpha)*(e.am||1)),go=()=>{ctx.translate(F.x+(F.vx||0)*t,F.y+(F.vy||0)*t);ctx.rotate((F.rot||0)+(F.spin||0)*t);const sc=1+(F.grow||0)*t;ctx.scale(sc*(F.flip||1),sc);e.f(F.w||300,t,F,a,P)};
  if(e.s&&al<.98){ // translucent paper: draw opaque on a spare canvas, then lay it down once (no seams between overlapping pieces)
    const main=ctx,M=ctx.getTransform(),ga=ctx.globalAlpha;if(!SPARE)SPARE=document.createElement('canvas');if(SPARE.width!==main.canvas.width||SPARE.height!==main.canvas.height){SPARE.width=main.canvas.width;SPARE.height=main.canvas.height}
    const o=SPARE.getContext('2d');o.setTransform(1,0,0,1,0,0);o.clearRect(0,0,SPARE.width,SPARE.height);o.setTransform(M);o.globalAlpha=1;ctx=o;try{go()}finally{ctx=main}
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=ga*al;ctx.drawImage(SPARE,0,0);ctx.restore();return}
  ctx.save();ctx.globalAlpha*=al;if(!e.s&&F.blend)ctx.globalCompositeOperation=F.blend;go();ctx.restore()};
let SPARE=null;

/* ---- scene: depth layers + background that changes with the story ---- */
const lerpBg=(A,B,u)=>{const o=Object.assign({},A);for(const k in B){if(typeof B[k]==='number'&&typeof A[k]==='number')o[k]=A[k]+(B[k]-A[k])*u;else if(u>=.5)o[k]=B[k]}return o};
let OFF=null;
function bgDraw(S,t,P){let bg=S.bg;if(S.bgTo&&!S.bg2)bg=lerpBg(bg,S.bgTo,q(P,t,S.bgc||0,S.bgd||1.5));BG[bg.k](bg,t);
  if(S.bg2){const u=q(P,t,S.bgc||0,S.bgd||1.2);if(u<=0)return;if(u>=1){BG[S.bg2.k](S.bg2,t);return}
    const main=ctx,M=ctx.getTransform();if(!OFF){OFF=document.createElement('canvas')}OFF.width=main.canvas.width;OFF.height=main.canvas.height;const o=OFF.getContext('2d');o.setTransform(M);ctx=o;BG[S.bg2.k](S.bg2,t);ctx=main;
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=u;ctx.drawImage(OFF,0,0);ctx.restore()}}
SHOTS.scene=function(t,d,P){const LK=window.LOOKS[P.look]||window.LOOKS[P.grade];let S=P.sc;
  if(LK){if(!P.look)P.look=P.grade;if(window.LOOKS[P.grade])P.grade=LK.grade;if(P.vig==null)P.vig=LK.vig;if(P.bloom==null)P.bloom=LK.bloom;S=Object.assign({},S,{figs:(S.figs||[]).map(f=>Object.assign({key:LK.key,rim:LK.rim,filt:LK.filt},f))})}
  if(S.bg)bgDraw(S,t,P);
  if(S.layers)drawLayers(S.layers,t,'back');
  layer(1,()=>(S.fxb||[]).forEach(F=>drawFx(F,t,P,d)));
  layer(S.depth??1,()=>(S.figs||[]).forEach(f=>drawWho(f,t,P)));
  const SCR={text:1,dim:1,flash:1};layer(1,()=>(S.fx||[]).forEach(F=>{if(!SCR[F.t])drawFx(F,t,P,d)}));
  if(S.cfl)layer(0.9,()=>{cloudBand('celF',37,CELC,S.cfl-40,14,t,1,1.2);skyG(['rgba(150,146,200,0)','rgba(70,64,130,.9)'],S.cfl+60,H+400)});
  if(S.layers)drawLayers(S.layers,t,'front');
  if(!(S.layers||[]).some(l=>l.d==='near')&&S.bg&&S.bg.fore!==false&&window.BGF[S.bg.k])BGF[S.bg.k](S.bg,t);
  (S.fx||[]).forEach(F=>{if(SCR[F.t])drawFx(F,t,P,d)})};
})();
