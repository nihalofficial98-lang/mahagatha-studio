/* Paper-cut backgrounds (same look as the Opus characters): layered scalloped cloud decks, cut ridges with snow, wave rows,
   mandala rings, flame-petal sun/halo, ink-tinted outlines and soft paper shadows.  Overrides BG.* from scenes.js; same parameters
   (sky, sun, sx, sy, seed, ridge, river, trees, px/pw/ct, strata, rgb, spin ...) so every shot plan keeps working. */
(function(){
const TAU=Math.PI*2,PI=Math.PI,INK='rgba(24,8,34,.5)';
const hx=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)),hex=a=>'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
const shd=(h,f)=>hex(hx(h).map(v=>f<1?v*f:v+(255-v)*(f-1)));
function cutP(fn,fill,o){o=o||{};ctx.save();ctx.beginPath();fn();if(o.sh!==0){ctx.shadowColor='rgba(10,2,24,.36)';ctx.shadowBlur=(o.blur==null?9:o.blur)*SC_;ctx.shadowOffsetY=(o.sy==null?5:o.sy)*SC_}
  ctx.fillStyle=fill;ctx.fill();ctx.shadowColor='transparent';ctx.shadowBlur=0;ctx.shadowOffsetY=0;if(o.lw!==0){ctx.lineWidth=o.lw||2;ctx.strokeStyle=o.ink||INK;ctx.lineJoin='round';ctx.stroke()}ctx.restore()}
const vg=(y0,y1,st)=>{const g=ctx.createLinearGradient(0,y0,0,y1);st.forEach((c,i)=>g.addColorStop(i/(st.length-1),c));return g};
const CC=(base)=>({light:shd(base,1.5),mid:base,dark:shd(base,.62)});
// a deck of overlapping round clouds, with a paper highlight along every crest
function deck(seed,y,h,C,t,drift,rmin,rmax){const r=rng(seed),arcs=[];let x=-320;while(x<W+380){const rad=rmin+r()*(rmax-rmin);arcs.push([x+rad,y+r()*18-rad*.2,rad]);x+=rad*1.25}
  const dx=Math.sin(t*.12+seed)*drift;ctx.save();ctx.translate(dx,0);
  cutP(()=>{ctx.moveTo(-340,y+h);arcs.forEach(([cx,cy,rad])=>ctx.arc(cx,cy,rad,PI,0));ctx.lineTo(W+400,y+h);ctx.closePath()},vg(y-rmax,y+h,[C.light,C.mid,C.dark]),{blur:11,sy:7});
  ctx.strokeStyle='rgba(255,255,255,.38)';ctx.lineWidth=3;ctx.lineCap='round';arcs.forEach(([cx,cy,rad])=>{ctx.beginPath();ctx.arc(cx,cy+3,rad-6,PI*1.12,PI*1.62);ctx.stroke()});
  ctx.strokeStyle='rgba(30,10,50,.16)';ctx.lineWidth=2;arcs.forEach(([cx,cy,rad])=>{ctx.beginPath();ctx.arc(cx,cy+rad*.1,rad*.7,PI*.15,PI*.8);ctx.stroke()});ctx.restore()}
// flame-petal sun
function sunburst(x,y,r,t,cols,g){g=g==null?1:g;ctx.save();ctx.translate(x,y);glow(0,0,r*3.2,'255,200,110',.32*g);const n=26;ctx.save();ctx.rotate(t*.05);
  for(let i=0;i<n;i++){const f=1+.08*Math.sin(t*2.6+i*1.9);ctx.save();ctx.rotate(i/n*TAU);cutP(()=>{ctx.moveTo(-r*.11,-r*.92);ctx.bezierCurveTo(-r*.13,-r*1.06,-r*.03,-r*1.12*f,r*.03,-r*1.3*f);ctx.bezierCurveTo(r*.02,-r*1.14*f,r*.13,-r*1.06,r*.11,-r*.92);ctx.closePath()},cols[1],{sh:0,lw:1.2});ctx.restore()}ctx.restore();
  const rg=ctx.createRadialGradient(0,0,r*.1,0,0,r);rg.addColorStop(0,cols[0]);rg.addColorStop(.6,cols[1]);rg.addColorStop(1,cols[2]);cutP(()=>ctx.arc(0,0,r,0,TAU),rg,{sh:0,lw:2.2});
  ctx.setLineDash([1,7]);ctx.strokeStyle='rgba(255,250,225,.85)';ctx.lineWidth=2.2;ctx.lineCap='round';ctx.beginPath();ctx.arc(0,0,r*.9,0,TAU);ctx.stroke();ctx.setLineDash([]);ctx.restore()}
// concentric leaf rings (mandala)
function mandala(x,y,t,rgb,a,rings,spin){ctx.save();ctx.translate(x,y);ctx.rotate(t*(spin==null?.03:spin));ctx.globalAlpha=a;ctx.strokeStyle=`rgb(${rgb})`;ctx.lineWidth=1.6;
  for(let k=0;k<(rings||4);k++){const R=130+k*84,n=12+k*8;ctx.beginPath();ctx.arc(0,0,R,0,TAU);ctx.stroke();for(let i=0;i<n;i++){ctx.save();ctx.rotate(i/n*TAU+k*.2);ctx.beginPath();ctx.moveTo(0,-R);ctx.quadraticCurveTo(14,-R-26,0,-R-52);ctx.quadraticCurveTo(-14,-R-26,0,-R);ctx.stroke();ctx.restore()}}ctx.restore()}
function waves(y,rows,cols,t,amp){for(let k=0;k<rows;k++){const yy=y+k*24,off=mod(t*(14+k*6),90);ctx.beginPath();ctx.moveTo(-400,H+400);ctx.lineTo(-400-off,yy);for(let x=-400-off;x<W+500;x+=45){ctx.quadraticCurveTo(x+11,yy-amp-Math.sin(x*.01+t+k)*3,x+22,yy);ctx.quadraticCurveTo(x+34,yy+amp*.4,x+45,yy)}ctx.lineTo(W+500,H+400);ctx.closePath();
  ctx.save();ctx.shadowColor='rgba(8,8,40,.35)';ctx.shadowBlur=7*SC_;ctx.shadowOffsetY=-3*SC_;ctx.fillStyle=cols[k%cols.length];ctx.fill();ctx.restore();ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=1.8;ctx.stroke()}}
function peaks(pts,fill,snow){cutP(()=>{ctx.moveTo(pts[0][0],H+400);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(pts[pts.length-1][0],H+400);ctx.closePath()},fill,{blur:8});
  if(!snow)return;pts.forEach(([x,y],i)=>{if(!i||i>=pts.length-1||pts[i-1][1]<=y||pts[i+1][1]<=y)return;const L=pts[i-1],R=pts[i+1],f=.3,a=[x+(L[0]-x)*f,y+(L[1]-y)*f],b=[x+(R[0]-x)*f,y+(R[1]-y)*f];
    cutP(()=>{ctx.moveTo(x,y);ctx.lineTo(b[0],b[1]);ctx.lineTo(b[0]-(b[0]-x)*.3,b[1]+8);ctx.lineTo(x+(b[0]-x)*.1,b[1]-2);ctx.lineTo(a[0]+(x-a[0])*.4,a[1]+10);ctx.lineTo(a[0],a[1]);ctx.closePath()},snow,{sh:0,lw:1.4})})}
const stars=(t,n,seed,ym)=>{const r=rng(seed);for(let i=0;i<n;i++){const x=r()*W,y=r()*ym,s=.5+r()*1.6,tw=.4+.6*Math.abs(Math.sin(t*1.7+i));ctx.fillStyle=`rgba(255,250,235,${(.25+.7*tw)*r()})`;ctx.beginPath();ctx.arc(x,y,s,0,TAU);ctx.fill();if(s>1.7)glow(x,y,s*6,'255,240,210',.25*tw)}};

Object.assign(BG,{
 cloudscape(S,t){const sky=S.sky||['#2a3a86','#7a8ad0','#f0b8c0','#fff0d0'];skyG(sky,-300,H+300);const sx=S.sx??CX,sy=S.sy??250,sun=S.sun||'255,236,190',warm=hx(sky[sky.length-1]).reduce((a,b)=>a+b)>560;
  glow(sx,sy,560,sun,.5);layer(.08,()=>{rays(sx,sy,t,sun,.07,14,1500);sunburst(sx,sy,58,t,warm?['#fffbe8','#ffd36a','#e8862a']:['#ffffff','#cfe0ff','#7a90e0'],.9)});
  const b2=sky[Math.min(2,sky.length-1)],b3=sky[sky.length-1];
  layer(.14,()=>deck((S.seed||21),S.y1??120,260,S.c1||CC(shd(b3,.95)),t,18,36,62));
  layer(.34,()=>deck((S.seed||21)+5,S.y2??270,300,S.c2||CC(shd(b2,1.05)),t,30,46,80));
  layer(.7,()=>deck((S.seed||21)+9,S.y3??450,320,S.c3||CC(shd(b2,.78)),t,46,60,104));
  dust(t,26,5,'255,240,210',.5,4)},
 vista(S,t){const P=S.sky||['#1a2a6a','#6a7ab8','#f0a080','#ffe0a8'];skyG(P,-300,H+300);const sx=S.sx??CX*1.2,sy=S.sy??330,sd=S.seed||7;
  glow(sx,sy,S.sr||440,S.sun||'255,214,150',.5);layer(.1,()=>sunburst(sx,sy,44,t,['#fffbea','#ffd070','#e8802a'],.8));if(S.stars)stars(t,90,sd,300);
  layer(.12,()=>deck(sd,S.cy??150,200,S.cl||{light:'#f6e8d8',mid:'#d8b8c0',dark:'#9a88a8'},t,14,30,50));
  const rc=S.ridge||['#7a86b4','#5a6a98','#3c4a78','#26305a'];
  rc.forEach((col,i)=>{const par=[.18,.32,.52,.78][i],r=rng(sd*13+i*29);layer(par,()=>{const base=300+i*70+(S.horizon||0),amp=[120,100,80,60][i]+(S.rough||0),pts=[[-520,base]];
    for(let x=-500;x<=W+500;x+=70)pts.push([x,base-amp*(.5+.5*Math.sin(x*.0045*(i+1)+i*2.1+sd))-r()*16]);
    cutP(()=>{ctx.moveTo(-520,H+400);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(W+520,H+400);ctx.closePath()},vg(base-amp,base+120,[shd(col,1.12),col,shd(col,.8)]),{blur:7});
    skyG(['rgba(255,236,210,0)',`rgba(${S.haze||'255,220,190'},${.2-i*.035})`],base-120,base+160)})});
  if(S.river)layer(.6,()=>{cutP(()=>{ctx.moveTo(CX-30,380);ctx.bezierCurveTo(CX-260,470,CX+240,520,CX-120,H+200);ctx.lineTo(CX+260,H+200);ctx.bezierCurveTo(CX+420,520,CX-30,470,CX+30,380);ctx.closePath()},S.river,{sh:0});
    ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=2;for(let i=0;i<12;i++){ctx.beginPath();ctx.moveTo(CX-70+i*10+Math.sin(t+i)*30,420+i*26);ctx.lineTo(CX-30+i*14+Math.sin(t+i)*30,420+i*26);ctx.stroke()}});
  if(S.ground)layer(.9,()=>{cutP(()=>{ctx.moveTo(-400,H-150);ctx.bezierCurveTo(200,H-190,700,H-120,1700,H-170);ctx.lineTo(1700,H+300);ctx.lineTo(-400,H+300);ctx.closePath()},vg(H-170,H+300,S.ground),{blur:10});
    const r=rng(41);ctx.fillStyle=S.blade||'#1c3a24';for(let i=0;i<60;i++){const x=r()*W,h=14+r()*28;ctx.beginPath();ctx.moveTo(x-5,H-118);ctx.lineTo(x+Math.sin(t*1.5+i)*4,H-118-h);ctx.lineTo(x+5,H-118);ctx.fill()}});
  if(S.trees)layer(.85,()=>{const r=rng(S.seed||9);S.trees.forEach((tx,i)=>{const h=190+r()*90,c=S.leaf||['#1e4a30','#2a6a3c'];cutP(()=>ctx.roundRect(tx-9,H-230,18,160,6),vg(0,1,[S.trunk||'#3a2418',shd(S.trunk||'#3a2418',.6)]),{blur:5});
    [[0,-h*.5,72],[-48,-h*.3,54],[48,-h*.3,54]].forEach(([dx,dy,rr],k)=>cutP(()=>ctx.arc(tx+dx+Math.sin(t*.8+i)*3,H-170+dy,rr,0,TAU),vg(H-170+dy-rr,H-170+dy+rr,[shd(c[k%2],1.25),c[k%2],shd(c[k%2],.7)]),{blur:7}))})});
  dust(t,S.dust??30,11,S.dustc||'255,230,190',.5,5)},
 plain(S,t){const c=S.cols||['#0a0610','#1c1020'];skyG(c,-300,H+300);const m=hx(c[c.length-1]);glow(CX,330,520,`${Math.min(255,m[0]*3+30)|0},${Math.min(255,m[1]*3+24)|0},${Math.min(255,m[2]*3+36)|0}`,.28);
  mandala(CX,340,t,'242,193,78',.07,4,.02);dust(t,22,7,'255,225,170',.35,3)},
 cosmos(S,t){skyG(['#04030c','#120c2e','#2a1a52'],-300,H+300);const rgb=S.rgb||'160,120,255';glow(CX,360,560,rgb,.3);stars(t,170,3,H);
  mandala(CX,330,t,rgb,.3,4,S.spin||.03);layer(.2,()=>{const r=rng(9);for(let i=0;i<7;i++){const a=r()*TAU+t*(S.spin||.03)*2,rad=140+r()*300,x=CX+Math.cos(a)*rad*1.4,y=340+Math.sin(a)*rad*.6;sunburst(x,y,9+r()*10,t+i,['#ffffff','#ffe6a0',`rgb(${rgb})`],.35)}});
  glow(CX,340,200,'255,230,170',.18);dust(t,28,5,'255,230,190',.4,4)},
 storm(S,t){const r=S.r??1;const col=(a,b)=>hex(hx(a).map((v,i)=>v+(hx(b)[i]-v)*r));skyG([col('#0a0e1c','#08020a'),col('#1c2236','#2a0810'),col('#3a3a52','#6a1612'),col('#7a5a5a','#d0482a')],-300,H+300);
  glow(CX,520,700,'255,90,40',.45*r);layer(.12,()=>deck(51,60,260,CC(col('#2c3250','#5a1814')),t,20,40,70));layer(.3,()=>deck(61,230,300,CC(col('#3a4062','#7a2218')),t,34,50,86));layer(.62,()=>deck(71,440,320,CC(col('#202640','#400c0c')),t,46,60,104));
  const fl=Math.max(0,Math.sin(t*5.3)*Math.sin(t*2.1));if(fl>.55)glow(CX*.8,200,500,'255,220,200',.35*(fl-.5));embers(t,40,3,'255,120,50',1.2*r)},
 sea(S,t){skyG(['#04122e','#0a2a5a','#0e3a74'],-300,H+300);stars(t,60,4,260);glow(CX,200,420,'120,170,255',.25);waves(300,7,['#123c78','#16488c','#1c5aa6','#2470bc'],t,12)},
 voidR(S,t){skyG(S.cols||['#050204','#1c0408','#4a0c0c'],-300,H+300);glow(S.gx||CX,S.gy||340,560,S.rgb||'255,60,30',.5);mandala(S.gx||CX,S.gy||340,t,'255,90,60',.2,5,-.04);embers(t,60,3,'255,110,40',2)},
 amber(S,t){skyG(['#2a1808','#6a3a12','#b8701e','#e8a850'],-300,H+300);glow(CX,470,560,'255,190,110',.4);layer(.1,()=>sunburst(CX,400,70,t,['#fffbea','#ffd070','#e8802a'],.9));layer(.25,()=>deck(19,250,260,{light:'#f0c880',mid:'#c88a40',dark:'#7a4a18'},t,20,40,70));
  layer(.6,()=>cutP(()=>{ctx.moveTo(-300,610);ctx.bezierCurveTo(300,570,800,640,1600,590);ctx.lineTo(1600,H+300);ctx.lineTo(-300,H+300);ctx.closePath()},vg(590,H+300,['#6a4220','#1a0c04']),{blur:10}));dust(t,50,83,'255,220,150',.5,6)},
 dusk(S,t){skyG(['#1a1440','#4a3070','#c8625a','#f0a070'],-300,H+300);glow(CX,470,540,'255,190,130',.5);layer(.1,()=>sunburst(CX,440,56,t,['#fffbea','#ffc46a','#e0602a'],.9));layer(.3,()=>deck(23,300,220,{light:'#f0a888',mid:'#b86a7a',dark:'#5a3a6a'},t,20,34,60));waves(500,5,['#3a3a82','#2e2e70','#242460','#1a1a4c'],t,9);dust(t,40,23,'255,200,150',.5,4)},
 earth(S,t){const st=S.strata||['#5a3a24','#42281a','#2c1a12','#1a0e0a'],r=rng(17);skyG(st,-300,H+300);
  layer(.3,()=>{for(let k=0;k<5;k++){const y=80+k*150;cutP(()=>{ctx.moveTo(-400,y);for(let x=-400;x<=W+500;x+=60)ctx.lineTo(x,y+Math.sin(x*.01+k*2)*22+r()*8);ctx.lineTo(W+500,y+170);ctx.lineTo(-400,y+170);ctx.closePath()},vg(y-20,y+170,[shd(st[k%st.length],1.15),st[k%st.length],shd(st[k%st.length],.75)]),{blur:6,lw:1.8})}});
  layer(.55,()=>{ctx.lineCap='round';for(let i=0;i<8;i++){let x=r()*W,y=-40;const pts=[[x,y]];for(let k=0;k<7;k++){x+=(r()-.5)*70;y+=70+r()*30;pts.push([x,y])}ctx.strokeStyle='rgba(20,8,4,.6)';ctx.lineWidth=9;ctx.beginPath();pts.forEach((p,j)=>j?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.strokeStyle='#8a5a32';ctx.lineWidth=5;ctx.stroke()}});
  layer(.75,()=>{for(let i=0;i<10;i++){const x=r()*W,y=140+r()*500,s=18+r()*40;cutP(()=>{ctx.moveTo(x-s,y+s*.4);ctx.lineTo(x-s*.4,y-s*.6);ctx.lineTo(x+s*.7,y-s*.3);ctx.lineTo(x+s,y+s*.5);ctx.closePath()},vg(y-s,y+s,['#8a7a72','#5a4a44']),{blur:5,lw:1.6})}});
  glow(S.gx??CX,S.gy??520,420,S.gc||'255,150,60',.4);dust(t,34,9,'255,170,90',.5,-6)},
 pillar(S,t){skyG(S.sky||['#05030c','#0e0a26','#2a1236'],-300,H+300);stars(t,110,5,H);const x=S.px??CX,hw=S.pw??110,ck=S.ct!=null?clamp((t-S.ct)/1.2):0;
  mandala(x,H/2,t,'242,160,70',.14,5,.025);glow(x,H/2,780,'255,150,60',.4);
  layer(.4,()=>{ctx.save();ctx.beginPath();ctx.rect(x-hw,-600,hw*2,H+1200);const g=ctx.createLinearGradient(x-hw,0,x+hw,0);g.addColorStop(0,'#a8300c');g.addColorStop(.28,'#ff9a30');g.addColorStop(.5,'#fff3c0');g.addColorStop(.72,'#ff9a30');g.addColorStop(1,'#a8300c');
    ctx.shadowColor='rgba(255,130,30,.6)';ctx.shadowBlur=40*SC_;ctx.fillStyle=g;ctx.fill();ctx.shadowBlur=0;ctx.lineWidth=3;ctx.strokeStyle='rgba(60,10,0,.75)';ctx.stroke();ctx.restore();
    ctx.save();ctx.beginPath();ctx.rect(x-hw,-600,hw*2,H+1200);ctx.clip();for(let i=0;i<14;i++){const yy=((i*97+t*60)%(H+500))-250;cutP(()=>{ctx.moveTo(x-hw,yy);ctx.quadraticCurveTo(x-hw*.2,yy-30,x,yy-70);ctx.quadraticCurveTo(x+hw*.2,yy-30,x+hw,yy);ctx.quadraticCurveTo(x,yy+24,x-hw,yy)},'rgba(255,225,130,.35)',{sh:0,lw:1.2,ink:'rgba(150,50,0,.4)'})}ctx.restore();
    [-1,1].forEach(sd=>{for(let i=0;i<9;i++){const yy=((i*118+t*40)%(H+300))-150;cutP(()=>{ctx.moveTo(x+sd*hw,yy);ctx.quadraticCurveTo(x+sd*(hw+30),yy-26,x+sd*(hw+10),yy-70);ctx.quadraticCurveTo(x+sd*(hw+4),yy-30,x+sd*hw,yy)},'#ff8a28',{sh:0,lw:1.3,ink:'rgba(110,30,0,.6)'})}});
    if(ck>0){const cw=hw*1.7*ck;ctx.save();ctx.beginPath();ctx.moveTo(x,-500);ctx.lineTo(x+cw*.5,H/2);ctx.lineTo(x,H+500);ctx.lineTo(x-cw*.5,H/2);ctx.closePath();ctx.clip();const cg=ctx.createRadialGradient(x,H/2,10,x,H/2,hw*2);cg.addColorStop(0,'#fff0c0');cg.addColorStop(1,'#a01808');ctx.fillStyle=cg;ctx.fillRect(x-hw*2,-500,hw*4,H+1000);ctx.restore()}});
  dust(t,60,13,'255,200,110',.7,-14)},
 kailash(S,t){skyG(['#03051a','#0c1446','#2a3a80','#7a6aa8'],-300,H+300);stars(t,120,21,300);moonAt(W*(S.mx==null?.22:S.mx),150,38,t);
  layer(.15,()=>peaks([[-500,420],[-200,340],[0,390],[200,300],[420,380],[640,160],[860,380],[1060,290],[1260,370],[1600,320],[1800,400]],vg(160,560,['#b6c2ea','#6670ae','#2e3468']),'#f6f8ff'));
  layer(.32,()=>peaks([[-500,500],[-100,420],[150,480],[380,410],[560,500],[760,470],[980,400],[1200,470],[1800,430]],vg(400,700,['#46508e','#1e2350']),'#dfe6fa'));
  layer(.55,()=>peaks([[-500,620],[-80,560],[200,600],[420,640],[860,640],[1080,580],[1800,620]],vg(560,760,['#2c2f5e','#14163a']),null));dust(t,40,7,'220,230,255',.5,3)}
});
})();
