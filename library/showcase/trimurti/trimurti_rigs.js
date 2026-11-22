/* Trimurti rigs + scenes in the new paper-cut painterly look. Depends on chars_new.js (window.TRIKIT).
   drawBrahma / drawVishnu / drawShiva are jointed rigs: every pose parameter can be animated over time.
   Brahma  {sprout 0..1 (side faces grow), rot (faces turn on a cylinder), bless, lift, talk, blink, glow, lotusGlow}
   Vishnu  {blink (1 = yoganidra), smile, lx, sway, bias (-1..1 hoods lean), rise, lotus (navel lotus 0..1), chakra, glow}
   Shiva   {blink, third (third eye 0..1), raise (0..1 arms up), lift (trident up), ganga, smile, glow, moon}  */
(function(G){
'use strict';
const K=G.TRIKIT,{TAU,PI,clamp,lerp,ease,L2,rng,shade,INK,PAL,lg,rg,cut,P,glow,stroke,goldG,gem,beadArc,band,face,hairCap,hairBack,kirita,jataMukuta,halo,hand,limb,limbOutline,arm,veda,mala,kamandalu,chakra,shankha,padma,gada,damaru,trishul,tube,ellPts,hood}=K;
const talkMouth=(t,k)=>k?k*(.15+.7*Math.abs(Math.sin(t*10.5))*Math.abs(Math.sin(t*3.7+1))):0;

function torso(c,sk,h,sw,ww,b){const pts=[[-ww,0],[-ww-5,-h*.32],[-sw+4,-h*.74],[-sw,-h+6+b],[-sw*.55,-h-3+b],[0,-h-1+b],[sw*.55,-h-3+b],[sw,-h+6+b],[sw-4,-h*.74],[ww+5,-h*.32],[ww,0],[0,5]];
  cut(c,P.smooth(pts),lg(c,-sw,0,sw,0,[sk.h,sk.b,sk.b,sk.d]),{lw:2.4});
  c.save();c.beginPath();P.smooth(pts)(c);c.clip();c.fillStyle='rgba(30,10,60,.17)';c.beginPath();c.ellipse(sw*.9,-h*.5,sw*.36,h*.75,0,0,TAU);c.fill();c.fillStyle='rgba(255,255,255,.12)';c.beginPath();c.ellipse(-sw*.45,-h*.62+b,sw*.3,h*.16,-.2,0,TAU);c.fill();c.restore();
  [-1,1].forEach(sd=>stroke(c,cc=>{cc.moveTo(sd*4,-h*.66+b);cc.quadraticCurveTo(sd*sw*.45,-h*.5+b,sd*sw*.8,-h*.7+b)},'rgba(40,14,40,.36)',2));
  stroke(c,cc=>{cc.moveTo(0,-h*.6+b);cc.lineTo(0,-h*.28)},'rgba(40,14,40,.25)',1.6);cut(c,P.ell(0,-h*.2,3,4),'rgba(40,14,40,.45)',{sh:0,lw:0});
  stroke(c,cc=>{cc.moveTo(-ww*.7,-h*.1);cc.quadraticCurveTo(0,-h*.04,ww*.7,-h*.1)},'rgba(40,14,40,.2)',1.4)}
function hara(c,y0,w,drops,b){drops.forEach((d,i)=>{const n=13+i*2;beadArc(c,-w+i*3,y0+b,w-i*3,y0+b,d,n,i===drops.length-1?2.4:3,i%2?PAL.pearl:PAL.gold)});gem(c,0,y0+b+drops[drops.length-1]+2,4.5,PAL.ruby)}
function petal(c,L,w,cols){cut(c,cc=>{cc.moveTo(0,0);cc.bezierCurveTo(L*.28,-w,L*.74,-w*.78,L,0);cc.bezierCurveTo(L*.74,w*.78,L*.28,w,0,0)},lg(c,0,0,L,0,cols),{lw:1.8,sh:1});stroke(c,cc=>{cc.moveTo(L*.12,0);cc.quadraticCurveTo(L*.5,-w*.12,L*.86,0)},'rgba(150,30,80,.35)',1.3)}
function lotusSeat(c,t,part,ga){ga=ga==null?1:ga;
  if(part==='back'){glow(c,0,-70,320,'255,140,190',.3*ga);for(let i=0;i<11;i++){const u=i/10;c.save();c.translate((u-.5)*230,-56);c.rotate(-PI/2+(u-.5)*2.3);petal(c,150-Math.abs(u-.5)*70,36,['#c2386e','#f27aa6','#ffd6e6']);c.restore()}return}
  for(let i=0;i<10;i++){const u=i/9;c.save();c.translate((u-.5)*300,-36);c.rotate(PI/2+(.5-u)*1.7);petal(c,82-Math.abs(u-.5)*20,30,['#9e2a5a','#d84e86','#f6a0c2']);c.restore()}
  cut(c,P.ell(0,-44,196,22),lg(c,0,-66,0,-22,['#ffe08a','#e3992b','#a8601a']),{lw:2.2});for(let i=0;i<26;i++){const a=i/26*TAU;cut(c,P.ell(Math.cos(a)*178,-44+Math.sin(a)*16,2.4,2.4),PAL.goldL,{sh:0,lw:.8})}
  for(let i=0;i<9;i++){const u=i/8;c.save();c.translate((u-.5)*300,-36);c.rotate(-PI/2+(u-.5)*1.2);petal(c,74-Math.abs(u-.5)*24,26,['#e05a90','#f7a0c2','#fff2f7']);c.restore()}
  glow(c,0,-60,180,'255,200,230',.18*ga)}

/* ===================== BRAHMA ===================== */
const SKB={b:'#eea466',h:'#ffd6a4',d:'#b86a3a',m:'#dc8c52'};
const BFX=[{smile:.45},{smile:.2,lx:.6},{blink:1,smile:.3},{smile:.3,lx:-.6,blink:.35}];
function drawBrahma(c,t,o){o=o||{};const by=Math.sin(t*1.4)*2.2,sp=o.sprout==null?1:o.sprout,rot=o.rot||0,bless=o.bless==null?.5:o.bless,lift=o.lift||0;
  halo(c,0,-376+by*.4,152,t,{g:o.glow==null?1:o.glow});
  lotusSeat(c,t,'back',o.lotusGlow);
  // back arms: Veda (left) and mala (right)
  const bL=[-50,-288+by],bR=[50,-288+by],sw=Math.sin(t*1.1)*3;
  const aBL=arm(c,SKB,bL,[-166-lift*8,-386-lift*54+sw],{bend:-1,w:[14,11,9],l1:70,l2:66});veda(c,aBL.t[0]+2,aBL.t[1]-28,-.12+lift*.1);
  const aBR=arm(c,SKB,bR,[166+lift*8,-386-lift*54-sw],{bend:1,w:[14,11,9],l1:70,l2:66});mala(c,aBR.t[0],aBR.t[1]-6,t);
  // seated legs in a crimson dhoti
  const lp=[[-160,-72],[-168,-104],[-128,-140],[-60,-150],[0,-144],[60,-150],[128,-140],[168,-104],[160,-72],[80,-60],[0,-64],[-80,-60]];
  cut(c,P.smooth(lp),lg(c,0,-150,0,-60,['#f07a40','#d23a2a','#8e1a1c']),{lw:2.4});
  [-110,-70,70,110].forEach(x=>stroke(c,cc=>{cc.moveTo(x*.7,-140);cc.quadraticCurveTo(x,-110,x*1.2,-72)},'rgba(80,10,10,.35)',1.6));
  stroke(c,cc=>{cc.moveTo(-162,-78);cc.quadraticCurveTo(-80,-54,0,-60);cc.quadraticCurveTo(80,-54,162,-78)},PAL.gold,5);
  [-1,1].forEach(sd=>{c.save();c.translate(sd*62,-138);c.scale(sd,1);c.rotate(-.18);cut(c,P.smooth([[-24,2],[-18,-8],[12,-10],[26,-4],[24,6],[-8,8]]),lg(c,0,-10,0,8,[SKB.h,SKB.b]),{lw:1.8,sh:0});
    c.fillStyle='rgba(240,120,130,.45)';c.beginPath();c.ellipse(4,2,13,3,0,0,TAU);c.fill();for(let k=0;k<5;k++)cut(c,P.ell(24+Math.sin(k)*1,-6+k*3,2.6,2),SKB.b,{sh:0,lw:1});c.restore()});
  cut(c,P.poly([[-16,-142],[16,-142],[30,-62],[-30,-62]]),lg(c,-30,0,30,0,['#ffd08a','#f6a640','#c66a20']),{lw:1.8});for(let k=-2;k<=2;k++)stroke(c,cc=>{cc.moveTo(k*5,-140);cc.lineTo(k*11,-64)},'rgba(120,50,0,.45)',1.3);stroke(c,cc=>{cc.moveTo(-30,-66);cc.lineTo(30,-66)},PAL.gold,4);
  lotusSeat(c,t,'front',o.lotusGlow);
  // torso + garments + jewellery
  c.save();c.translate(0,-138);torso(c,SKB,152,68,44,by);
  cut(c,cc=>{cc.moveTo(-64,-146+by);cc.quadraticCurveTo(-20,-110,44,-8);cc.lineTo(26,2);cc.quadraticCurveTo(-30,-86,-62,-120+by);cc.closePath()},lg(c,-60,-140,40,0,['#fffaf0','#e8dcc4']),{lw:1.8});
  stroke(c,cc=>{cc.moveTo(-60,-142+by);cc.quadraticCurveTo(-18,-108,40,-6)},PAL.gold,2.4);
  stroke(c,cc=>{cc.moveTo(-46,-146+by);cc.quadraticCurveTo(10,-90,38,-14)},'#fff8e6',1.6);
  cut(c,cc=>cc.roundRect(-44,-12,88,16,6),goldG(c,-44,44),{lw:2,sh:0});for(let k=-3;k<=3;k++)gem(c,k*12,-4,2.6,k%2?PAL.emer:PAL.ruby);
  hara(c,-150,30,[12,22,34],by);c.restore();
  // heads: four faces on a turning cylinder
  const hc=[0,-366+by];cut(c,P.caps([0,-292+by],[0,-336+by],13,13),SKB.m,{lw:2});
  cut(c,P.ell(hc[0],hc[1]-6,48,50),lg(c,-48,0,48,0,['#f4f0ea','#d8d0c8','#a8a098']),{lw:2.2,sh:0});const R=46,fs=[0,1,2,3].map(i=>{const a=rot+i*PI/2;return{i,a,x:Math.sin(a)*R,z:Math.cos(a),s:i===0?1:ease(sp)}}).filter(f=>f.z>-.45&&f.s>.02).sort((a,b)=>a.z-b.z);
  const front=fs[fs.length-1];
  fs.forEach(f=>{c.save();c.translate(hc[0]+f.x*f.s,hc[1]+(1-f.s)*40-(1-f.z)*6);const sc=(.86+.14*f.z)*f.s;c.scale(sc,sc);c.filter=`brightness(${(.8+.2*Math.max(0,f.z)).toFixed(3)})`;
    const E=BFX[f.i],isF=f===front,tn=Math.sin(f.a);
    face(c,{skin:SKB,turn:tn,t:t+f.i*1.3,beard:'#f5f1ea',tilak:'brahma',smile:E.smile,lx:E.lx||0,blink:isF?Math.max(E.blink||0,o.blink||0):(E.blink||0),mouth:isF?talkMouth(t,o.talk||0):0,browCol:'#6a5a54',lip:'#b23a3e'});
    c.save();c.scale(1-Math.abs(tn)*.3,1);c.translate(tn*5,0);hairCap(c,'#e6e0da');jataMukuta(c);c.restore();c.filter='none';c.restore()});
  // front arms: kamandalu on the knee, right hand blessing
  kamandalu(c,-112,-136);arm(c,SKB,[-64,-284+by],[-104,-170],{bend:1,w:[16,13,10],cap:1});
  arm(c,SKB,[64,-284+by],L2([96,-196],[110,-292],bless),{bend:-1,w:[16,13,10],cap:1,hand:'abhaya',ang:lerp(.5,.12,bless)});
}

function swan(c,x,y,s,t){c.save();c.translate(x,y);c.scale(s,s);const nb=Math.sin(t*1.3)*4,fl=Math.sin(t*1.7)*.04;
  stroke(c,cc=>cc.ellipse(0,6,110,12,0,0,TAU),'rgba(220,230,255,.35)',2);
  cut(c,P.smooth([[-96,-12],[-74,-50],[-10,-62],[50,-52],[82,-30],[72,2],[0,10],[-64,6]]),lg(c,0,-62,0,10,['#ffffff','#dcdaf0']),{lw:2.4});
  c.save();c.rotate(fl);[0,1,2].forEach(k=>cut(c,cc=>{cc.moveTo(-70+k*8,-34-k*6);cc.bezierCurveTo(-40,-70-k*8,20,-66-k*8,40,-40-k*6);cc.bezierCurveTo(10,-36,-30,-20,-70+k*8,-34-k*6)},k===2?'#ffffff':'#ecebf8',{lw:1.6,sh:0}));c.restore();
  for(let k=0;k<5;k++)stroke(c,cc=>{cc.moveTo(-60+k*14,-28);cc.quadraticCurveTo(-50+k*14,-40,-40+k*14,-30)},'rgba(120,120,170,.4)',1.2);
  const nk=cc=>{cc.moveTo(50,-44);cc.bezierCurveTo(96,-80+nb*.3,30,-130+nb*.6,52,-168+nb);cc.quadraticCurveTo(60,-182+nb,72,-184+nb)};stroke(c,nk,INK,27);stroke(c,nk,'#ffffff',22);stroke(c,cc=>{cc.moveTo(60,-60);cc.bezierCurveTo(90,-86+nb*.3,40,-128+nb*.6,58,-160+nb)},'rgba(150,150,200,.35)',4);
  beadArc(c,52,-112+nb*.6,74,-110+nb*.6,7,6,2.6,PAL.gold);
  cut(c,P.ell(70,-182+nb,22,16,.15),'#ffffff',{lw:2.2,sh:0});cut(c,cc=>{cc.moveTo(86,-190+nb);cc.quadraticCurveTo(110,-186+nb,124,-174+nb);cc.quadraticCurveTo(104,-174+nb,86,-174+nb);cc.closePath()},'#f08a1e',{lw:1.8,sh:0});cut(c,P.ell(84,-182+nb,3,3),INK,{sh:0,lw:0});cut(c,P.ell(83,-183+nb,1,1),'#fff',{sh:0,lw:0});
  cut(c,P.poly([[56,-196+nb],[60,-216+nb],[67,-202+nb],[74,-220+nb],[80,-200+nb]]),goldG(c,56,80),{lw:1.3,sh:0});gem(c,68,-198+nb,2.4,PAL.ruby);c.restore()}

/* ===================== VISHNU on SHESHA ===================== */
const SKV={b:'#3f74c8',h:'#7cabee',d:'#22448a',m:'#3568b8'};
const PIT={b:'#f6b81e',h:'#ffe27e',d:'#c26c0c',m:'#e09a16'};
const SN={b:'#2f9488',d:'#155456',l:'#86e0cc',belly:'#f8e6aa',bellyD:'#d8aa58'};
function foot(c,sk,p,ang){c.save();c.translate(p[0],p[1]);c.rotate(ang);cut(c,P.smooth([[-6,-10],[14,-12],[30,-8],[36,-2],[30,6],[-4,9],[-12,0]]),lg(c,0,-12,0,9,[sk.h,sk.b,sk.d]),{lw:1.8});
  c.fillStyle='#e0234a';c.beginPath();c.ellipse(6,7,16,2.4,0,0,TAU);c.fill();for(let k=0;k<5;k++)cut(c,P.ell(34-k*.6,-7+k*3.2,2.6,2),sk.b,{sh:0,lw:.9});beadArc(c,-8,-10,-8,9,4,6,2.2,PAL.gold);c.restore()}
function drawVishnu(c,t,o){o=o||{};const br=Math.sin(t*1.1),bl=o.blink==null?.6:o.blink,sway=o.sway==null?1:o.sway,bias=o.bias||0,rise=o.rise||0;
  glow(c,-240,-340,360,'255,205,110',.3*(o.glow==null?1:o.glow));
  // five hoods on necks
  const piv=[-176,-246],Rh=162+rise*28,base=[-206,-204];
  const hs=[-2,-1,0,1,2].map(k=>{const a=k*.46+Math.sin(t*.9+k*.8)*.07*sway+bias*.2,bob=Math.sin(t*1.3+k)*4*sway-rise*8;return{k,a,x:piv[0]+Math.sin(a)*Rh,y:piv[1]-Math.cos(a)*Rh+bob}});
  halo(c,piv[0],piv[1]-Rh+10,96,t,{g:.55*(o.glow==null?1:o.glow),n:26});
  [...hs].sort((a,b)=>Math.abs(b.k)-Math.abs(a.k)).forEach(h=>{const pts=[];for(let i=0;i<=12;i++){const u=i/12;pts.push([lerp(base[0]+h.k*9,h.x-Math.sin(h.a)*40,u)+Math.sin(u*PI)*h.k*10,lerp(base[1],h.y+Math.cos(h.a)*44,u)])}tube(c,pts,24,21,SN,{belly:1});
    hood(c,h.x,h.y,h.a*.85,1-.06*Math.abs(h.k),t,SN,{ph:h.k*1.7,gem:h.k===0})});
  // trunk + coiled couch
  tube(c,[[-330,-104],[-326,-146],[-300,-182],[-262,-204],[-216,-212]],50,32,SN,{dots:true,belly:1});
  [[0,-22,350,38,56],[-8,-72,330,32,50],[-14,-120,306,26,44]].forEach(([x,y,rx,ry,r])=>tube(c,ellPts(x,y,rx,ry,-PI,PI,72),r,r,SN,{dots:true,belly:1}));
  const tl=[];for(let k=0;k<=12;k++){const u=k/12;tl.push([330+u*150+Math.sin(u*3)*10,-6-Math.sin(u*2.4)*60-u*40])}tube(c,tl,46,6,SN,{belly:1});
  // Vishnu body: torso frame
  const H=[30,-196],TH=-1.33,cs=Math.cos(TH),sn=Math.sin(TH),W=p=>[H[0]+p[0]*cs-p[1]*sn,H[1]+p[0]*sn+p[1]*cs];
  // back arms (chakra, shankha)
  const sB=W([40,-142]);const aC=arm(c,SKV,sB,[-74,-398+br*2],{bend:-1,w:[14,11,9],hand:'abhaya',ang:-.2});chakra(c,aC.t[0]-2,aC.t[1]-52,25,t,o.chakra);
  const aS=arm(c,SKV,W([30,-130]),[6,-370-br*2],{bend:1,w:[14,11,9]});shankha(c,aS.t[0]+4,aS.t[1]-30,.35,1);
  // legs in pitambara
  const leg=(hp,kn,an,ft,fa)=>{limbOutline(c,hp,kn,34,27);limbOutline(c,kn,an,26,17);limb(c,PIT,hp,kn,34,27,{lw:0,sh:0});limb(c,PIT,kn,an,26,17,{lw:0,sh:0});for(let k=1;k<6;k++){const p=k<3?L2(hp,kn,k/3):L2(kn,an,(k-2)/4);cut(c,P.ell(p[0],p[1]-6,3,3),PAL.red,{sh:0,lw:.8})}[.25,.55].forEach(u=>stroke(c,cc=>{const a=L2(hp,kn,u),b=L2(kn,an,u);cc.moveTo(a[0],a[1]+8);cc.quadraticCurveTo(kn[0],kn[1]+6,b[0],b[1]+6)},'rgba(120,60,0,.35)',1.5));band(c,kn,an,.92,18,PAL.red);foot(c,SKV,ft,fa)};
  leg(W([-22,6]),[142,-180],[244,-182],[250,-184],-.05);
  leg(W([22,6]),[130,-258],[204,-200],[210,-196],.25);
  const wc=W([0,4]);cut(c,P.poly([[wc[0]-14,wc[1]-10],[wc[0]+18,wc[1]+6],[wc[0]+28,wc[1]+58],[wc[0]-8,wc[1]+64]]),lg(c,wc[0]-20,0,wc[0]+40,0,[PIT.h,PIT.b,PIT.d]),{lw:1.8});
  for(let k=0;k<4;k++)stroke(c,cc=>{cc.moveTo(wc[0]-6+k*7,wc[1]-6+k*4);cc.lineTo(wc[0]-4+k*9,wc[1]+60)},'rgba(120,60,0,.4)',1.3);stroke(c,cc=>{cc.moveTo(wc[0]-8,wc[1]+62);cc.lineTo(wc[0]+28,wc[1]+56)},PAL.red,4);
  // torso
  c.save();c.translate(H[0],H[1]);c.rotate(TH);torso(c,SKV,160,68,44,br*1.5);
  cut(c,cc=>cc.roundRect(-46,-12,92,18,6),goldG(c,-46,46),{lw:2,sh:0});for(let k=-3;k<=3;k++)gem(c,k*12,-3,2.6,k%2?PAL.emer:PAL.ruby);
  stroke(c,cc=>{cc.moveTo(-52,-150);cc.quadraticCurveTo(0,-80,38,-8)},'#fff4dc',1.8);
  hara(c,-146,28,[12,22],br*1.5);gem(c,0,-106,6,PAL.ruby);
  for(let i=0;i<24;i++){const u=i/23,x=lerp(-50,50,u),y=-146+Math.sin(u*PI)*176;cut(c,P.ell(x,y,4.6,4.6),i%3?'#f07aa6':(i%2?'#fff3a0':'#5cc070'),{sh:0,lw:1})}
  // neck + head (yoganidra)
  cut(c,P.caps([0,-148],[0,-184],13,13),SKV.m,{lw:2});
  c.save();c.translate(0,-186);c.rotate(1.12);c.translate(0,-44);hairBack(c,'#16142a',t,96);
  face(c,{skin:SKV,t:t,blink:bl,smile:o.smile==null?.45:o.smile,lx:o.lx||0,ly:o.ly||0,tilak:'vaishnava',lip:'#c23a5a',kgem:PAL.emer});
  hairCap(c,'#14122a');kirita(c,66);c.restore();c.restore();
  // front arms: upper hand holds a lotus, lower hand rests on the gada
  const aP=arm(c,SKV,W([52,-150]),[34,-258+br],{bend:-1,w:[16,13,10],l1:72,l2:70,hand:'hold',cap:1});padma(c,aP.t[0]+2,aP.t[1]-24,1.1,1,t);
  gada(c,[-138,-142],[-6,-150]);arm(c,SKV,W([-52,-150]),[-70,-146],{bend:-1,w:[16,13,10],hand:'hold',cap:1});
  // lotus rising from the navel
  const lo=ease(o.lotus||0);if(lo>.01){const nv=W([0,-36]),tp=[nv[0]+70,nv[1]-250*lo];stroke(c,cc=>{cc.moveTo(nv[0],nv[1]);cc.bezierCurveTo(nv[0]+10,nv[1]-90*lo,tp[0]+30,tp[1]+100*lo,tp[0],tp[1])},'#1e5a2a',7);stroke(c,cc=>{cc.moveTo(nv[0],nv[1]);cc.bezierCurveTo(nv[0]+10,nv[1]-90*lo,tp[0]+30,tp[1]+100*lo,tp[0],tp[1])},'#4caa4a',4);
    glow(c,tp[0],tp[1]-10,90*lo,'255,190,220',.5);padma(c,tp[0],tp[1],1.6*lo,lo,t)}
}

/* ===================== SHIVA ===================== */
const SKS={b:'#88a4c4',h:'#c2d6ec',d:'#506c90',m:'#7492b6'};
const VS={b:'#3c9a4c',d:'#1c5a2c',l:'#9ce68a',belly:'#f6e48e',bellyD:'#c8a040'};
const TIG=['#f09a30','#d86a14','#a84a0c'];
function tigerStripes(c,pts,n,seed){c.save();c.beginPath();P.smooth(pts)(c);c.clip();const r=rng(seed);let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;pts.forEach(([x,y])=>{x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y)});
  for(let i=0;i<n;i++){const x=lerp(x0,x1,(i+.5)/n)+(r()-.5)*8,w=4+r()*4;c.fillStyle='#1e0d14';c.beginPath();c.moveTo(x-w,y0-4);c.quadraticCurveTo(x+w*2,lerp(y0,y1,.4),x-w*.2,lerp(y0,y1,.4+r()*.5));c.quadraticCurveTo(x+w*.4,lerp(y0,y1,.3),x+w,y0-4);c.fill()}c.restore()}
function drawShiva(c,t,o){o=o||{};const by=Math.sin(t*1.2)*2,bl=o.blink==null?.9:o.blink,th=clamp(o.third||0),ra=ease(o.raise||0),lf=ease(o.lift||0),gl=o.glow==null?1:o.glow;
  halo(c,0,-384+by*.4,142,t,{col:['#f4f8ff','#a8c8f2','#4c5cc4','#d89a3a'],rgb:'130,170,255',rgb2:'210,230,255',petal:'rgba(235,244,255,.45)',g:gl});
  if(th>0)glow(c,0,-396,320,'255,110,40',.4*th);
  // flowing locks behind
  for(let i=0;i<12;i++){const sd=i<6?-1:1,k=i%6,sw=Math.sin(t*1.1+i*.7)*4;const x0=sd*(10+k*4),y0=-430+by,x1=sd*(44+k*9)+sw,y1=-300+k*8,x2=sd*(58+k*12)+sw*1.6,y2=-228+k*10;
    stroke(c,cc=>{cc.moveTo(x0,y0);cc.bezierCurveTo(sd*40,-420,x1,y1,x2,y2)},INK,14-k);stroke(c,cc=>{cc.moveTo(x0,y0);cc.bezierCurveTo(sd*40,-420,x1,y1,x2,y2)},k%2?'#3a2c4e':'#2a2038',10-k);
    stroke(c,cc=>{cc.moveTo(x0,y0);cc.bezierCurveTo(sd*40,-420,x1,y1,x2,y2)},'rgba(190,170,230,.25)',2,{dash:[6,8]})}
  // trident (lifted by the right hand)
  const tx=172,ty=-6-lf*86;trishul(c,tx,ty,560,t,-lf*.04);
  // rock + tiger skin
  cut(c,P.poly([[-236,0],[-252,-40],[-218,-86],[-120,-106],[40,-110],[172,-98],[236,-70],[246,-22],[226,0]]),lg(c,0,-110,0,0,['#8a88b8','#55537e','#2e2c52']),{lw:2.6});
  cut(c,P.poly([[-218,-86],[-120,-106],[-150,-60],[-236,-40]]),'rgba(255,255,255,.12)',{sh:0,lw:1.4});cut(c,P.poly([[172,-98],[236,-70],[200,-30],[120,-60]]),'rgba(0,0,0,.18)',{sh:0,lw:1.4});
  cut(c,P.poly([[-120,-106],[40,-110],[0,-60],[-90,-70]]),'rgba(255,255,255,.07)',{sh:0,lw:1.2});
  const tp=[[-196,-98],[0,-112],[196,-98],[204,-56],[176,-18],[150,-44],[120,-10],[60,-30],[0,-14],[-60,-30],[-120,-8],[-160,-40],[-196,-20],[-210,-60]];
  cut(c,P.smooth(tp),lg(c,0,-112,0,-10,TIG),{lw:2.2});tigerStripes(c,tp,16,7);
  cut(c,P.smooth([[-176,-40],[-160,-30],[-166,6],[-178,14],[-192,6],[-190,-24]]),lg(c,0,-40,0,14,TIG),{lw:1.8});for(let k=0;k<3;k++)cut(c,P.ell(-188+k*7,12,2.4,3),'#f4ead8',{sh:0,lw:.8});
  stroke(c,cc=>{cc.moveTo(190,-40);cc.bezierCurveTo(220,-10,200,30,230,52)},INK,11);stroke(c,cc=>{cc.moveTo(190,-40);cc.bezierCurveTo(220,-10,200,30,230,52)},TIG[1],7);stroke(c,cc=>{cc.moveTo(190,-40);cc.bezierCurveTo(220,-10,200,30,230,52)},'#1e0d14',7,{dash:[4,8]});
  // crossed legs
  const lp=[[-172,-96],[-162,-134],[-98,-162],[0,-152],[98,-162],[162,-134],[172,-96],[110,-84],[0,-92],[-110,-84]];
  cut(c,P.smooth(lp),lg(c,0,-162,0,-84,[SKS.h,SKS.b,SKS.d]),{lw:2.4});stroke(c,cc=>{cc.moveTo(-120,-100);cc.quadraticCurveTo(-30,-124,60,-100)},'rgba(30,20,60,.35)',2);stroke(c,cc=>{cc.moveTo(120,-104);cc.quadraticCurveTo(40,-128,-50,-110)},'rgba(30,20,60,.3)',2);
  [-1,1].forEach(sd=>{c.save();c.translate(sd*64,-146);c.scale(sd,1);c.rotate(-.2);cut(c,P.smooth([[-24,2],[-18,-8],[12,-10],[26,-4],[24,6],[-8,8]]),lg(c,0,-10,0,8,[SKS.h,SKS.b]),{lw:1.8,sh:0});for(let k=0;k<5;k++)cut(c,P.ell(24+Math.sin(k),-6+k*3,2.6,2),SKS.b,{sh:0,lw:1});c.restore()});
  const lc=[[-60,-178],[60,-178],[96,-128],[66,-104],[30,-114],[0,-98],[-30,-114],[-66,-104],[-96,-128]];cut(c,P.smooth(lc),lg(c,0,-178,0,-100,TIG),{lw:2});tigerStripes(c,lc,9,3);
  // torso
  c.save();c.translate(0,-162);torso(c,SKS,160,76,44,by);
  [-104,-96,-88].forEach(y=>stroke(c,cc=>{cc.moveTo(-40,y+by*.5);cc.quadraticCurveTo(0,y-6+by*.5,40,y+by*.5)},'rgba(250,250,245,.85)',3));
  tube(c,ellPts(0,-8,50,7,0,PI,16),8,8,VS,{scales:false});
  c.restore();
  beadArc(c,-36,-312+by,36,-312+by,64,17,4.4,'#7a3a1a','rgba(255,200,160,.5)');beadArc(c,-30,-314+by,30,-314+by,96,19,4,'#6a2e14','rgba(255,200,160,.5)');
  // Vasuki around the neck, hood over the right shoulder
  const vs=Math.sin(t*1.4)*.12,vp=ellPts(0,-318+by,44,26,PI*1.02,-.1,14);for(let k=1;k<=8;k++){const u=k/8;vp.push([lerp(44,98,u)+Math.sin(u*PI)*8,-318+by-u*96+Math.sin(u*PI)*6])}tube(c,vp,9,7,VS,{scales:false,belly:1});
  hood(c,98,-440+by,.22+vs,.68,t,VS,{ph:2,eye:'#ff5a3a'});
  // neck, head, jata
  cut(c,P.caps([0,-314+by],[0,-338+by],15,15),SKS.m,{lw:2});
  c.save();c.translate(0,-378+by);
  // jata bun
  [-1,1].forEach(sd=>{const lp=cc=>{cc.moveTo(sd*20,-60);cc.bezierCurveTo(sd*66,-70,sd*62,-128,sd*26,-118)};stroke(c,lp,INK,17);stroke(c,lp,'#2c2240',12);stroke(c,lp,'rgba(190,170,240,.3)',2.5,{dash:[5,6]})});
  const bun=[[-30,-48],[-42,-82],[-36,-120],[-16,-146],[14,-148],[36,-124],[42,-84],[30,-48]];cut(c,P.smooth(bun),lg(c,-42,0,42,0,['#55446e','#2c2242','#140e20']),{lw:2.4});
  c.save();c.beginPath();P.smooth(bun)(c);c.clip();for(let i=0;i<8;i++){stroke(c,cc=>cc.ellipse(0,-96+i*2,40-i*5,54-i*6.5,0,PI*(1.1+i*.13),PI*(2.6+i*.13)),i%2?'rgba(190,170,240,.35)':'rgba(6,4,14,.6)',3)}c.restore();
  const tk=cc=>{cc.moveTo(0,-140);cc.bezierCurveTo(-20,-168,18,-178,8,-150)};stroke(c,tk,INK,14);stroke(c,tk,'#2c2240',9);
  beadArc(c,-31,-56,31,-56,5,11,3.8,'#7a3a1a','rgba(255,200,160,.5)');
  // crescent moon
  const mg=o.moon==null?1:o.moon;glow(c,-34,-102,60,'230,240,255',.5*mg);cut(c,cc=>{cc.arc(-34,-102,17,PI*.35,PI*1.75);cc.arc(-28,-106,13,PI*1.62,PI*.45,true);cc.closePath()},lg(c,-50,-120,-20,-86,['#ffffff','#f4ecc8']),{lw:1.6,sh:0});
  // Ganga springing from the jata
  const gg=o.ganga==null?1:o.ganga;if(gg>.01){const gp=cc=>{cc.moveTo(6,-160);cc.bezierCurveTo(8,-200,60,-210,84,-170);cc.bezierCurveTo(106,-130,112,-60,124,40*gg-20)};
    glow(c,60,-170,70,'170,220,255',.4*gg);stroke(c,gp,'rgba(120,190,255,.55)',14*gg);stroke(c,gp,'rgba(220,245,255,.85)',6*gg);stroke(c,gp,'#ffffff',2.4,{dash:[10,14],off:-t*60});
    const r=rng(5);for(let i=0;i<10;i++){const u=(t*.8+r())%1;cut(c,P.ell(4+Math.sin(i)*10*u,-158-u*40,1.8,1.8),'rgba(230,248,255,.9)',{sh:0,lw:0})}}
  face(c,{skin:SKS,t:t,blink:bl,smile:o.smile==null?.25:o.smile,lx:o.lx||0,tilak:'tripundra',third:th,lip:'#7a3a5e',kgem:PAL.sapph,browCol:'#141020'});
  hairCap(c,'#241a30');cut(c,cc=>cc.roundRect(-33,-44,66,8,4),goldG(c,-33,33),{lw:1.4,sh:0});
  c.restore();
  // arms: dhyana -> raised (abhaya + trident)
  const sL=[-70,-312+by],sR=[70,-312+by];
  arm(c,SKS,sL,L2([-128,-140],[-154,-372],ra),{bend:ra>.3?-1:1,w:[18,15,11],l1:72,l2:70,cap:1,hand:ra>.5?'abhaya':'jnana',ang:ra>.5?-.15:lerp(2.6,1.2,ra)});
  arm(c,SKS,sR,L2([128,-140],[tx-1,ty-262],ra),{bend:-1,w:[18,15,11],l1:72,l2:70,cap:1,hand:ra>.5?'hold':'jnana',ang:ra>.5?-.4:lerp(-2.6,-1.2,ra),flip:ra>.5?1:-1});
}

/* ===================== backgrounds, particles, post ===================== */
function sky(c,stops,y0,y1){c.fillStyle=lg(c,0,y0,0,y1,stops);c.fillRect(-400,y0,2080,y1-y0)}
function stars(c,t,n,seed,ymax,a){const r=rng(seed);for(let i=0;i<n;i++){const x=r()*1400-60,y=r()*ymax,s=r()*1.8+.4,tw=.5+.5*Math.sin(t*2+i);c.fillStyle=`rgba(255,250,235,${(a||1)*(.3+.7*tw)*r()})`;c.beginPath();c.arc(x,y,s,0,TAU);c.fill();if(s>1.9)glow(c,x,y,8,'255,240,210',.3*tw)}}
function cloudBand(c,y,h,col,t,seed,sp){const r=rng(seed),off=(t*(sp||4))%160;c.beginPath();c.moveTo(-400,y+h);for(let x=-400-off;x<1700;x+=80){const rr=30+r()*36;c.arc(x+40,y-r()*14,rr,PI,0)}c.lineTo(1700,y+h);c.closePath();
  c.save();c.shadowColor='rgba(10,0,30,.4)';c.shadowBlur=10;c.shadowOffsetY=6;c.fillStyle=col;c.fill();c.restore()}
function motes(c,t,n,seed,rgb,box,vy,sz){const r=rng(seed);for(let i=0;i<n;i++){const x0=box[0]+r()*box[2],ph=r(),y=box[1]+box[3]-((t*vy/box[3]+ph)%1)*box[3],x=x0+Math.sin(t*.8+i)*12,s=(sz||2)*(.5+r());glow(c,x,y,s*5,rgb,.5);c.fillStyle=`rgba(${rgb},.9)`;c.beginPath();c.arc(x,y,s*.6,0,TAU);c.fill()}}
function petals(c,t,n,seed){const r=rng(seed);for(let i=0;i<n;i++){const ph=r(),x=r()*1400-60+Math.sin(t*.7+i)*40,y=((t*30/760+ph)%1)*760-30,a=t*1.5+i;c.save();c.translate(x,y);c.rotate(a);cut(c,cc=>{cc.moveTo(0,-7);cc.quadraticCurveTo(5,0,0,7);cc.quadraticCurveTo(-5,0,0,-7)},r()>.5?'#ffb0cc':'#ffd8e6',{sh:0,lw:1,ink:'rgba(120,30,60,.5)'});c.restore()}}
function waves(c,t,y,rows,cols,amp){for(let k=0;k<rows;k++){const yy=y+k*22,off=(t*(14+k*6))%90,col=cols[k%cols.length];c.beginPath();c.moveTo(-400,1300);for(let x=-400-off;x<1720;x+=45){c.quadraticCurveTo(x+11,yy-amp-Math.sin(x*.01+t+k)*3,x+22,yy);c.quadraticCurveTo(x+33,yy+amp*.4,x+45,yy)}c.lineTo(1720,1300);c.closePath();
  c.save();c.shadowColor='rgba(10,10,40,.35)';c.shadowBlur=6;c.shadowOffsetY=-3;c.fillStyle=col;c.fill();c.restore();c.strokeStyle='rgba(255,255,255,.55)';c.lineWidth=1.6;c.stroke()}}
function mountains(c,pts,fill,snow){cut(c,P.poly(pts.concat([[1700,800],[-400,800]])),fill,{lw:2,sh:0});if(!snow)return;
  pts.forEach(([x,y],i)=>{if(!i||i>=pts.length-1||pts[i-1][1]<=y||pts[i+1][1]<=y)return;const L=pts[i-1],Rr=pts[i+1],f=Math.min(.32,70/Math.max(40,Math.min(L[1]-y,Rr[1]-y))*.3+.12),a=[lerp(x,L[0],f),lerp(y,L[1],f)],b=[lerp(x,Rr[0],f),lerp(y,Rr[1],f)],zz=[];
    for(let k=1;k<6;k++){const u=k/6;zz.push([lerp(b[0],a[0],u),lerp(b[1],a[1],u)+(k%2?-8:6)])}cut(c,P.poly([[x,y],b,...zz,a]),snow,{sh:0,lw:1.4,ink:'rgba(40,50,100,.5)'});
    stroke(c,cc=>{cc.moveTo(x,y);cc.lineTo(lerp(x,b[0],.9),lerp(y,b[1],.9))},'rgba(150,170,220,.55)',3)})}
function par(c,cam,d,fn){c.save();c.translate(640,360);const z=1+(cam.z-1)*d;c.scale(z,z);c.translate(-640-cam.x*d,-360-cam.y*d);fn();c.restore()}

function bgBrahma(c,t,cam){par(c,cam,.15,()=>{sky(c,['#120a34','#3e2066','#a2407a','#f08a5a','#ffcf7a'],-300,520);stars(c,t,120,3,260,.8);glow(c,640,430,520,'255,190,110',.45)});
  par(c,cam,.3,()=>{cloudBand(c,360,200,'#7a3a7e',t,11,3);cloudBand(c,410,200,'#b05486',t,12,5);cloudBand(c,456,200,'#e88a8e',t,13,7)});
  par(c,cam,.6,()=>{c.fillStyle=lg(c,0,500,0,760,['#3a2a6a','#1c1442','#0c0a24']);c.fillRect(-400,500,2080,300);glow(c,640,520,380,'255,170,120',.25);
    for(let k=0;k<9;k++){const y=520+k*k*3.2;stroke(c,cc=>{for(let x=-200;x<1500;x+=60){cc.moveTo(x+((t*10+k*23)%60),y);cc.lineTo(x+26+((t*10+k*23)%60),y)}},'rgba(255,200,170,.25)',1.4)}
    const r=rng(41);for(let i=0;i<9;i++){const x=r()*1300,y=560+r()*140;if(Math.abs(x-640)<230)continue;cut(c,cc=>{cc.ellipse(x,y,46,14,0,.25,TAU-.1);cc.lineTo(x,y)},lg(c,0,y-14,0,y+14,['#3aa86a','#1a5a3a']),{lw:1.6});if(i%3===0)padma(c,x+10,y-4,.7,.6,t)}})}
function bgVishnu(c,t,cam){par(c,cam,.12,()=>{sky(c,['#04061c','#0e1650','#26307a','#4a3e8e','#4a3e8e'],-300,1300);glow(c,300,200,360,'140,90,220',.25);glow(c,1000,160,320,'60,180,200',.2);stars(c,t,190,8,520);glow(c,1060,130,90,'255,250,230',.6);cut(c,P.ell(1060,130,34,34),rg(c,1050,120,4,36,['#ffffff','#f2ecd8']),{sh:0,lw:0})});
  par(c,cam,.35,()=>{waves(c,t,520,3,['#9ab0e0','#b8cbee','#d6e2f6'],10)})}
function fgVishnu(c,t,cam){par(c,cam,1.05,()=>{waves(c,t,640,4,['#c8d8f2','#e2ecfa','#f4f8ff','#dfe8f8'],12);motes(c,t,24,17,'255,255,255',[0,600,1280,140],8,1.6)})}
function bgShiva(c,t,cam){par(c,cam,.1,()=>{sky(c,['#03051a','#0c1446','#2a3a80','#7a6aa8','#e0a8a0'],-300,560);stars(c,t,160,21,330);
  c.save();c.globalCompositeOperation='lighter';for(let k=0;k<3;k++){c.fillStyle=lg(c,0,80,0,330,[`rgba(${k?'120,90,230':'80,230,180'},0)`,`rgba(${k?'120,90,230':'80,230,180'},.16)`,'rgba(0,0,0,0)']);c.beginPath();c.moveTo(-100,120+k*30);for(let x=-100;x<=1400;x+=50)c.lineTo(x,120+k*30+Math.sin(x*.006+t*.3+k)*40);c.lineTo(1400,360);c.lineTo(-100,360);c.closePath();c.fill()}c.restore();
  glow(c,1040,150,140,'235,240,255',.4);cut(c,P.ell(1040,150,40,40),rg(c,1030,140,4,42,['#ffffff','#e8ecf6']),{sh:0,lw:0})});
  par(c,cam,.2,()=>mountains(c,[[-400,420],[-200,340],[0,390],[200,300],[420,380],[640,160],[860,380],[1060,290],[1260,370],[1500,320],[1700,400]],lg(c,0,160,0,560,['#b6c2ea','#6670ae','#2e3468']),'#f6f8ff'));
  par(c,cam,.35,()=>{mountains(c,[[-400,500],[-100,420],[150,480],[380,410],[560,500],[760,470],[980,400],[1200,470],[1700,430]],lg(c,0,400,0,700,['#46508e','#1e2350']),'#dfe6fa');c.fillStyle='rgba(200,215,255,.12)';c.fillRect(-400,470,2080,40)});
  par(c,cam,.55,()=>{mountains(c,[[-400,620],[-80,560],[200,600],[420,640],[860,640],[1080,580],[1700,620]],lg(c,0,560,0,760,['#2c2f5e','#14163a']),null)})}
function fgShiva(c,t,cam){par(c,cam,1,()=>{const r=rng(77);for(let i=0;i<70;i++){const ph=r(),x=(r()*1400-60+t*14+Math.sin(t+i)*20)%1400,y=((t*36/760+ph)%1)*760,s=r()*2.2+.6;c.fillStyle='rgba(245,248,255,.8)';c.beginPath();c.arc(x,y,s,0,TAU);c.fill()}})}
function bgTrio(c,t,cam){par(c,cam,.1,()=>{c.fillStyle=rg(c,640,330,40,900,['#3a1c66','#1a0e3e','#07051a']);c.fillRect(-400,-300,2080,1300);stars(c,t,220,51,720);
  c.save();c.translate(640,300);c.rotate(t*.03);c.globalAlpha=.55;for(let ring=0;ring<4;ring++){const R=120+ring*80,n=12+ring*8;stroke(c,cc=>cc.arc(0,0,R,0,TAU),'rgba(242,193,78,.5)',1.6);for(let i=0;i<n;i++){c.save();c.rotate(i/n*TAU+ring*.2);stroke(c,cc=>{cc.moveTo(0,-R);cc.quadraticCurveTo(14,-R-26,0,-R-46);cc.quadraticCurveTo(-14,-R-26,0,-R)},'rgba(242,193,78,.55)',1.4);c.restore()}}c.restore();
  glow(c,250,330,300,'255,170,120',.3);glow(c,640,300,340,'255,215,120',.3);glow(c,1030,330,300,'130,170,255',.3)});
  par(c,cam,.35,()=>waves(c,t,560,3,['#6a7ac0','#8a9ad6','#aab8e8'],9))}
function fgTrio(c,t,cam){par(c,cam,1.05,()=>{waves(c,t,650,3,['#b8c8ee','#d8e2f8','#eef3ff'],10);motes(c,t,40,9,'255,220,140',[0,100,1280,560],18,1.8)})}

let GRAIN=null;function grain(){if(GRAIN)return GRAIN;const g=document.createElement('canvas');g.width=g.height=256;const x=g.getContext('2d'),d=x.createImageData(256,256),r=rng(99);for(let i=0;i<d.data.length;i+=4){const v=r()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}x.putImageData(d,0,0);GRAIN=g;return g}
function post(c,o){o=o||{};c.save();c.fillStyle=rg(c,640,360,260,820,['rgba(0,0,0,0)','rgba(8,2,20,'+(o.vig==null?.6:o.vig)+')']);c.fillRect(0,0,1280,720);
  c.globalCompositeOperation='overlay';c.globalAlpha=.09;c.fillStyle=c.createPattern(grain(),'repeat');c.fillRect(0,0,1280,720);
  c.globalCompositeOperation='soft-light';c.globalAlpha=.25;c.fillStyle=o.wash||'#ffb060';c.fillRect(0,0,1280,720);c.restore()}

function fig(c,cam,x,y,s,fn){c.save();c.translate(640,360);c.scale(cam.z,cam.z);c.translate(-640-cam.x,-360-cam.y);c.translate(x,y);c.scale(s,s);fn();c.restore()}
const SCENES={
  brahma(c,t,p,cam){bgBrahma(c,t,cam);fig(c,cam,330,640,.82,()=>swan(c,0,0,1,t));fig(c,cam,660,650,1.0,()=>drawBrahma(c,t,p));par(c,cam,1.1,()=>{petals(c,t,26,5);motes(c,t,30,3,'255,220,150',[0,60,1280,620],16,1.6)});post(c,{wash:'#ffa060'})},
  vishnu(c,t,p,cam){bgVishnu(c,t,cam);fig(c,cam,660,600,1.06,()=>drawVishnu(c,t,p));fgVishnu(c,t,cam);par(c,cam,1,()=>motes(c,t,26,4,'255,225,150',[0,60,1280,560],14,1.6));post(c,{wash:'#9ab0ff'})},
  shiva(c,t,p,cam){bgShiva(c,t,cam);fig(c,cam,640,672,.98,()=>drawShiva(c,t,p));fgShiva(c,t,cam);post(c,{wash:'#8aa0ff'})},
  trio(c,t,p,cam){bgTrio(c,t,cam);fig(c,cam,640,566,.6,()=>drawVishnu(c,t,p.vishnu||{}));fig(c,cam,232,640,.6,()=>drawBrahma(c,t,p.brahma||{}));fig(c,cam,1050,654,.6,()=>drawShiva(c,t,p.shiva||{}));fgTrio(c,t,cam);post(c,{wash:'#ffc070'})}
};
G.TRIMURTI={SCENES,drawBrahma,drawVishnu,drawShiva,swan,
  render(canvas,scene,t,p,cam){const c=canvas.getContext('2d'),S=canvas.width/1280;K.setDPR(S);c.setTransform(S,0,0,S,0,0);c.clearRect(0,0,1280,720);c.fillStyle='#000';c.fillRect(0,0,1280,720);
    SCENES[scene](c,t,p||{},Object.assign({x:0,y:0,z:1},cam||{}))}};
})(window);
