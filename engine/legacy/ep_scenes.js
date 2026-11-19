/* ===== Episode scene library: cosmic scenes, Brahma, Vishnu, asuras ===== */
const DIG='०१२३४५६७८९';
let TXQ=null;function txtQ(v){TXQ=v}
function txt(s,x,y,size,col,a=1,w=700,al='center'){if(TXQ){TXQ.push({k:'t',s,x,y,size,col,a:ctx.globalAlpha*clamp(a),w,al,m:ctx.getTransform()});return}ctx.save();ctx.globalAlpha*=clamp(a);ctx.font=`${w} ${size}px NDev, sans-serif`;ctx.textAlign=al;ctx.textBaseline='middle';ctx.shadowColor='rgba(0,0,0,.75)';ctx.shadowBlur=16;ctx.fillStyle=col;ctx.fillText(s,x,y);ctx.restore()}
function glow(x,y,r,rgb,a=0.6){ctx.save();ctx.globalCompositeOperation='lighter';const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);ctx.restore()}
function skyG(stops,h=H){const g=ctx.createLinearGradient(0,0,0,h);stops.forEach((c,i)=>g.addColorStop(i/(stops.length-1),c));ctx.fillStyle=g;ctx.fillRect(-400,-400,W+800,H+800)}
function view(z,cx,cy,sh,fn){ctx.save();ctx.translate(W/2+(sh?Math.sin(sh*0.0+cx)*0:0),H/2);ctx.scale(z,z);ctx.translate(-cx,-cy);fn();ctx.restore()}
function shakeOf(t,a){return [Math.sin(t*61)*a+Math.sin(t*37)*a*0.6,Math.cos(t*53)*a+Math.sin(t*29)*a*0.5]}
function ocean(t,y0,c1,c2,hi,gx){const g=ctx.createLinearGradient(0,y0,0,y0+520);g.addColorStop(0,c1);g.addColorStop(1,c2);ctx.fillStyle=g;ctx.fillRect(-400,y0,W+800,H+800);
  ctx.lineWidth=2;for(let i=0;i<10;i++){const yy=y0+8+i*i*3+i*5,amp=2+i*0.8;ctx.strokeStyle=`rgba(${hi},${0.05+i*0.02})`;ctx.beginPath();for(let x=-60;x<=W+60;x+=16){const y=yy+Math.sin(x*0.012*(1+i*0.1)+t*(0.7+i*0.08)+i*1.7)*amp;x===-60?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()}
  if(gx!=null){ctx.save();ctx.globalCompositeOperation='lighter';ctx.translate(gx,y0+50);ctx.scale(1,0.3);const gg=ctx.createRadialGradient(0,0,0,0,0,360);gg.addColorStop(0,`rgba(${hi},.35)`);gg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gg;ctx.fillRect(-360,-360,720,720);ctx.restore()}}
function dust(t,n,seed,rgb='255,230,180',a=0.6,sp=6){const r=rng(seed);ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const x=mod(r()*W+Math.sin(t*0.3+i)*20+t*sp*(0.5+r()),W),y=mod(r()*H-t*sp*(0.3+r()),H),z=0.5+r()*1.8,al=a*(0.3+0.7*Math.abs(Math.sin(t*1.2+i*3)));ctx.fillStyle=`rgba(${rgb},${al})`;ctx.beginPath();ctx.arc(x,y,z,0,7);ctx.fill()}ctx.restore()}
function splash(x,y,t0,t,sc=1){const u=t-t0;if(u<0||u>1.4)return;ctx.save();ctx.strokeStyle=`rgba(210,235,255,${0.8*(1-u/1.4)})`;ctx.lineWidth=3;for(let i=0;i<3;i++){const r=(u*70-i*14)*sc;if(r>0){ctx.beginPath();ctx.ellipse(x,y,r*1.8,r*0.45,0,0,7);ctx.stroke()}}
  ctx.fillStyle=`rgba(230,245,255,${0.9*(1-u/1.4)})`;for(let i=0;i<9;i++){const a=i/9*3.14+3.14,px=x+Math.cos(a)*u*60*sc,py=y-Math.sin(u*4+i)*u*50*sc+u*u*40;ctx.beginPath();ctx.arc(px,py,2.5,0,7);ctx.fill()}ctx.restore()}
function lotusFlower(x,y,s,open,t,a=1){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.globalAlpha*=a;ctx.shadowColor='rgba(255,230,190,.8)';ctx.shadowOffsetX=-2;
  const N=9;for(let pass=0;pass<2;pass++){for(let i=0;i<N;i++){const u=(i-(N-1)/2)/((N-1)/2),ang=-Math.PI/2+u*(0.25+open*1.25)*(pass?0.7:1),len=(pass?70:92)*(0.6+0.4*open+0.1*Math.sin(t+i));
    ctx.save();ctx.rotate(ang+Math.PI/2);ctx.fillStyle=pass?'#ffd0de':'#e8789f';ctx.beginPath();ctx.moveTo(0,0);ctx.quadraticCurveTo(-24,-len*0.55,0,-len);ctx.quadraticCurveTo(24,-len*0.55,0,0);ctx.fill();ctx.restore()}}
  ctx.fillStyle='#f0c24a';ctx.beginPath();ctx.ellipse(0,-6,34,10,0,0,7);ctx.fill();ctx.restore()}
function brahma(x,y,s,t,o={}){const e=Object.assign({eye:1,mouth:0.2,brow:0,open:0,talk:0,pose:'meditate',alpha:1,aura:null,rot:0,look:0},o);
  ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.rotate(e.rot);ctx.globalAlpha*=e.alpha;
  const br=Math.sin(t*1.8)*1.2,SK='#d98a45',SKD='#aa6330';
  if(e.aura)glow(0,-120,230,e.aura,0.45);
  ctx.shadowColor='rgba(255,215,150,.9)';ctx.shadowOffsetX=-3;ctx.shadowBlur=0;
  ctx.fillStyle=SKD;ctx.beginPath();ctx.ellipse(0,-14,96,24,0,0,7);ctx.fill();
  ctx.fillStyle='#e9c14a';ctx.beginPath();ctx.ellipse(0,-20,80,19,0,0,7);ctx.fill();ctx.fillStyle='#c23c2c';ctx.beginPath();ctx.ellipse(0,-24,40,9,0,0,7);ctx.fill();
  ctx.fillStyle=SK;ctx.beginPath();ctx.moveTo(-36,-36);ctx.lineTo(36,-36);ctx.lineTo(30,-132+br);ctx.lineTo(-30,-132+br);ctx.fill();
  ctx.shadowOffsetX=0;ctx.strokeStyle='#f4efe0';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-26,-130+br);ctx.lineTo(24,-50);ctx.stroke();ctx.shadowOffsetX=-3;
  // arms (4)
  const SH=[[-30,-124+br],[30,-124+br]],pl=e.pose==='plead';
  const tg=pl?[[-8,-98],[8,-98],[-96,-170],[96,-170]]:[[-80,-60],[80,-60],[-96,-118],[96,-122]];
  [[0,2,-1],[1,3,1]].forEach(([si,ti,dir],q)=>{});
  const arms=[[SH[0],tg[2],1],[SH[1],tg[3],-1],[[-26,-116+br],tg[0],1],[[26,-116+br],tg[1],-1]];
  arms.forEach(([S,T,dir])=>{const el=ik(S,T,38,38,dir);limb(ctx,S,[el[0],el[1]],11,SK);limb(ctx,[el[0],el[1]],el[2],10,SK);ctx.fillStyle=SK;ctx.beginPath();ctx.arc(el[2][0],el[2][1],6.5,0,7);ctx.fill()});
  if(!pl){ // kamandala + mala
    ctx.fillStyle='#d9a441';ctx.beginPath();ctx.ellipse(tg[2][0],tg[2][1]+12,13,16,0,0,7);ctx.fill();ctx.fillRect(tg[2][0]-4,tg[2][1]-8,8,10);
    ctx.strokeStyle='#7a3b1e';ctx.lineWidth=3;ctx.setLineDash([4,5]);ctx.beginPath();ctx.arc(tg[3][0],tg[3][1]+14,15,0,7);ctx.stroke();ctx.setLineDash([])}
  // side heads
  ctx.shadowOffsetX=0;
  [-1,1].forEach(sd=>{ctx.fillStyle=SKD;ctx.beginPath();ctx.ellipse(sd*52,-164+br,19,23,0,0,7);ctx.fill();ctx.fillStyle='#e9c14a';ctx.beginPath();ctx.moveTo(sd*52-16,-176+br);ctx.lineTo(sd*52,-206+br);ctx.lineTo(sd*52+16,-176+br);ctx.fill();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(sd*57,-166+br,3.5,2.6*clamp(e.eye,0.1,1),0,0,7);ctx.fill();ctx.fillStyle='#1a1010';ctx.beginPath();ctx.arc(sd*58,-166+br,1.5,0,7);ctx.fill()});
  // main head
  ctx.shadowColor='rgba(255,215,150,.9)';ctx.shadowOffsetX=-3;
  ctx.fillStyle='#f4efe6';ctx.beginPath();ctx.moveTo(-19,-150+br);ctx.quadraticCurveTo(-24,-112+br,0,-98+br+Math.sin(t*2)*1.5);ctx.quadraticCurveTo(24,-112+br,19,-150+br);ctx.fill();
  ctx.fillStyle=SK;ctx.beginPath();ctx.ellipse(0,-170+br,25,29,0,0,7);ctx.fill();ctx.shadowOffsetX=0;
  ctx.fillStyle='#e9c14a';ctx.beginPath();ctx.moveTo(-24,-190+br);for(let i=0;i<5;i++){ctx.lineTo(-24+i*9.6+4.8,-222+br-(i%2?0:8));ctx.lineTo(-24+(i+1)*9.6,-190+br)}ctx.fill();ctx.fillStyle='#d9362c';ctx.beginPath();ctx.arc(0,-196+br,3.5,0,7);ctx.fill();
  const blink=(mod(t,3.6)<0.13)?0.08:1,eh=clamp(e.eye,0.1,1.3)*blink;
  [-1,1].forEach(sd=>{ctx.fillStyle='#fbf6ea';ctx.beginPath();ctx.ellipse(sd*10,-172+br,6,4*eh,0,0,7);ctx.fill();ctx.fillStyle='#1a1010';ctx.beginPath();ctx.ellipse(sd*10+e.look*1.5,-172+br,2.4,Math.min(2.8,2.8*eh+0.2),0,0,7);ctx.fill();
    ctx.strokeStyle='#f4efe6';ctx.lineWidth=3;ctx.lineCap='round';const k=e.brow;ctx.beginPath();ctx.moveTo(sd*4,-181+br+(-k*4));ctx.lineTo(sd*17,-180+br+k*3.5);ctx.stroke()});
  ctx.fillStyle='#c0211c';ctx.beginPath();ctx.arc(0,-184+br,2.4,0,7);ctx.fill();
  const op=clamp(e.open+(e.talk?(0.35+0.3*Math.sin(t*13))*e.talk:0),0,1);
  if(op>0.08){ctx.fillStyle='#3a0f12';ctx.beginPath();ctx.ellipse(0,-150+br,7+op*2,2+op*6,0,0,7);ctx.fill()}else{ctx.strokeStyle='#7a3a2a';ctx.lineWidth=2.4;ctx.beginPath();ctx.moveTo(-8,-150+br-e.mouth*2);ctx.quadraticCurveTo(0,-150+br+e.mouth*6,8,-150+br-e.mouth*2);ctx.stroke()}
  ctx.restore()}
function shesha(x,y,s,t,o={}){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.shadowColor='rgba(180,220,255,.7)';ctx.shadowOffsetX=-2;
  const col='#4f6786',hi='#7d98b6';
  [[0,52,250,38],[10,28,222,32],[-6,6,196,28]].forEach(([dx,dy,rx,ry],i)=>{ctx.fillStyle=i%2?hi:col;ctx.beginPath();ctx.ellipse(dx,dy+Math.sin(t*0.8+i)*2,rx,ry,0,0,7);ctx.fill()});
  ctx.shadowOffsetX=0;ctx.strokeStyle='rgba(20,30,50,.35)';ctx.lineWidth=2;for(let i=-9;i<=9;i++){ctx.beginPath();ctx.moveTo(i*24,24);ctx.quadraticCurveTo(i*24+6,44,i*24,66);ctx.stroke()}
  ctx.shadowOffsetX=-2;for(let j=-2;j<=2;j++){const tx=-205+j*36,ty=-170-(2-Math.abs(j))*20+Math.sin(t*1.4+j)*5;ctx.strokeStyle=col;ctx.lineWidth=20;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-205,30);ctx.quadraticCurveTo(-205+j*14,-60,tx,ty+24);ctx.stroke();
    ctx.fillStyle=hi;ctx.beginPath();ctx.ellipse(tx,ty,26,34,0,0,7);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(tx-8,ty-4,4,0,7);ctx.arc(tx+8,ty-4,4,0,7);ctx.fill();ctx.fillStyle='#111';ctx.fillRect(tx-9,ty-7,2,6);ctx.fillRect(tx+7,ty-7,2,6)}
  ctx.restore()}
function vishnuLying(x,y,s,t,o={}){const e=Object.assign({eyes:0,lotus:0,brahma:0,aura:0},o);
  ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  if(e.aura)glow(0,0,420,'255,215,120',e.aura);
  shesha(0,40,1,t,{});
  ctx.shadowColor='rgba(190,215,255,.9)';ctx.shadowOffsetX=-2;ctx.shadowBlur=0;
  const BL='#4a78d0',BD='#335aa8',br=Math.sin(t*1.2)*1.5;
  ctx.fillStyle=BD;ctx.beginPath();ctx.ellipse(120,6,92,15,0.03,0,7);ctx.fill();ctx.beginPath();ctx.ellipse(205,2,22,9,0,0,7);ctx.fill();
  ctx.fillStyle=BL;ctx.beginPath();ctx.moveTo(-95,-6);ctx.quadraticCurveTo(-40,-34+br,60,-24);ctx.lineTo(70,20);ctx.quadraticCurveTo(-30,32,-95,22);ctx.fill();
  ctx.fillStyle='#f2c230';ctx.beginPath();ctx.moveTo(18,-26);ctx.quadraticCurveTo(95,-22,150,-6);ctx.lineTo(150,26);ctx.quadraticCurveTo(80,30,18,24);ctx.fill();ctx.fillStyle='#d9a441';ctx.fillRect(14,-28,8,54);
  ctx.fillStyle=BL;ctx.beginPath();ctx.ellipse(-20,-12,60,11,0.05,0,7);ctx.fill();
  ctx.strokeStyle='#e8ecf6';ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(-70,-12+br);ctx.quadraticCurveTo(-30,0,20,10);ctx.stroke();
  ctx.fillStyle=BL;ctx.beginPath();ctx.arc(-120,-8,27,0,7);ctx.fill();ctx.shadowOffsetX=0;
  ctx.fillStyle='#d9a441';ctx.beginPath();ctx.moveTo(-142,-22);ctx.lineTo(-136,-50);ctx.lineTo(-126,-34);ctx.lineTo(-117,-54);ctx.lineTo(-108,-34);ctx.lineTo(-98,-48);ctx.lineTo(-97,-22);ctx.fill();
  if(e.eyes>0.5){ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(-112,-10,7,4.5*e.eyes,0,0,7);ctx.fill();glow(-112,-10,50,'255,240,200',0.5)}else{ctx.strokeStyle='#14203a';ctx.lineWidth=2.4;ctx.beginPath();ctx.arc(-112,-10,6,0.2,2.9);ctx.stroke()}
  ctx.strokeStyle='#1b2a55';ctx.lineWidth=2;ctx.beginPath();ctx.arc(-104,6,5,0.2,2.8);ctx.stroke();
  if(e.lotus>0){const L=e.lotus*210,tx=-4+Math.sin(t*0.7)*4,ty=-20-L;ctx.strokeStyle='#4f8a4f';ctx.lineWidth=11;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-4,-18);ctx.quadraticCurveTo(-4+Math.sin(t)*8,-20-L*0.5,tx,ty);ctx.stroke();
    lotusFlower(tx,ty+8,0.9,clamp((e.lotus-0.6)/0.4),t);if(e.brahma>0)brahma(tx,ty-6,0.55,t,{alpha:e.brahma,aura:'255,220,140',eye:0.2})}
  ctx.restore()}
function vishnuStarFlash(a){if(a<=0)return;ctx.fillStyle=`rgba(255,255,255,${a})`;ctx.fillRect(0,0,W,H)}
function rays(cx,cy,t,rgb,a,n=14,len=1400){ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const an=i/n*6.283+t*0.08,w=0.05+0.02*Math.sin(t+i);const g=ctx.createRadialGradient(cx,cy,10,cx,cy,len);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(an-w)*len,cy+Math.sin(an-w)*len);ctx.lineTo(cx+Math.cos(an+w)*len,cy+Math.sin(an+w)*len);ctx.fill()}ctx.restore()}
function vedaScroll(x,y,s,rot,rgb,label,a=1){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);ctx.globalAlpha*=a;glow(0,0,90,rgb,0.55);ctx.fillStyle='#f4e2b0';ctx.fillRect(-26,-34,52,68);ctx.fillStyle='#b4651e';ctx.fillRect(-30,-38,60,8);ctx.fillRect(-30,30,60,8);ctx.strokeStyle='#8a4a1a';ctx.lineWidth=1.5;for(let i=0;i<5;i++){ctx.beginPath();ctx.moveTo(-18,-20+i*10);ctx.lineTo(18,-20+i*10);ctx.stroke()}
  if(label){ctx.restore();return}ctx.restore()}
function dissolveCard(P,t,d){if(!P||!P.card)return;const a=Math.min(clamp((t-0.5)/0.8),clamp((4.6-t)/0.8));if(a<=0)return;ctx.save();ctx.globalAlpha=a;const g=ctx.createLinearGradient(0,150,0,300);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(0.5,'rgba(0,0,0,.55)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,150,W,150);txt(P.card,W/2,225,54,'#ffd98a',1,700);ctx.restore()}

/* --- extra character specs + decorations --- */
Object.assign(CHARS,{
 vishnu:{skin:'#4a78d0',skinD:'#2f55a8',dhoti:'#f2c230',trim:'#d9a441',hair:'#15131f',crown:'gold',shirt:null,beard:null,must:false,head:1,sash:'#e9edf6',jew:true},
 hayagriva:{skin:'#4a78d0',skinD:'#2f55a8',dhoti:'#f2c230',trim:'#d9a441',hair:'#15131f',crown:'none',shirt:null,beard:null,must:false,head:1,sash:'#e9edf6',jew:true,horse:true},
 madhu:{skin:'#6a5499',skinD:'#44346f',dhoti:'#7a1f2b',trim:'#c28a3a',hair:'#0e0a14',crown:'none',shirt:null,beard:null,must:true,head:1.12,sash:'#3a1a1f',jew:false,horns:true,fangs:true},
 kaitabha:{skin:'#3f8a72',skinD:'#2a5c4c',dhoti:'#5a2a6a',trim:'#c28a3a',hair:'#0e0a14',crown:'none',shirt:null,beard:null,must:false,head:1.0,sash:'#2a1a3a',jew:false,horns:true,fangs:true,antennae:true}
});

/* ===== shots ===== */
Object.assign(SHOTS,{
void(t,d){const k=clamp(t/d);skyG(['#010108','#04051a','#020210']);dust(t,120,3,'200,210,255',0.5,3);
  const a=ease((k-0.45)/0.3)*(1-ease((k-0.7)/0.1));if(a>0){const r=6+a*10+Math.sin(t*5)*1.5;glow(W/2,H/2,160+a*140,'255,225,160',0.55*a);ctx.fillStyle='#fff7df';ctx.beginPath();ctx.arc(W/2,H/2,r,0,7);ctx.fill();
    for(let i=0;i<4;i++){const u=mod(t*0.5+i*0.25,1);ctx.strokeStyle=`rgba(255,225,160,${0.6*(1-u)*a})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(W/2,H/2,20+u*420,0,7);ctx.stroke()}}
  const b=ease((k-0.72)/0.15);txt('महागाथा',W/2,H/2-30,120,'#ffd98a',b,700);txt('एपिसोड 01 · सृष्टि का जन्म',W/2,H/2+70,40,'#f1e6d0',b*0.9,400)},
om(t,d,P){const k=clamp(t/d);skyG(['#0a0624','#1c1450','#2e1f6e']);dust(t,90,7,'255,230,180',0.5,4);
  const pr=1+0.06*Math.sin(t*1.6);glow(W/2,H/2,300*pr,'255,235,190',0.5);ctx.fillStyle='#fff6df';ctx.beginPath();ctx.arc(W/2,H/2,34*pr,0,7);ctx.fill();
  for(let i=0;i<6;i++){const u=mod(t*0.22+i/6,1);ctx.strokeStyle=`rgba(255,225,160,${0.5*(1-u)})`;ctx.lineWidth=3;ctx.beginPath();ctx.arc(W/2,H/2,40+u*700,0,7);ctx.stroke()}
  const o=ease((k-0.62)/0.15);if(o>0){glow(W/2,H/2,380,'255,200,110',0.5*o);txt('ॐ',W/2,H/2-6,300,'#ffe2a0',o,700)}
  dissolveCard(P,t,d)},
gunas(t,d){const k=clamp(t/d);skyG(['#0a0624','#241a5e','#3a2a7e']);dust(t,70,11,'255,230,200',0.4,4);
  const fade=1-ease((k-0.5)/0.12),cx=W/2,cy=H/2-20;
  if(fade>0){ctx.save();ctx.globalAlpha=fade;[['#f6f3ff','255,250,255','सत्व',0],['#ff5a4a','255,90,70','रजस',2.094],['#2a1646','150,90,255','तमस',4.188]].forEach(([c,g,l,ph],i)=>{const a=t*0.9+ph,x=cx+Math.cos(a)*190,y=cy+Math.sin(a)*90;glow(x,y,130,g,0.55);ctx.fillStyle=c;ctx.shadowColor=`rgba(${g},.9)`;ctx.shadowBlur=0;ctx.beginPath();ctx.arc(x,y,34,0,7);ctx.fill();txt(l,x,y+70,40,'#f6ecd8',ease((k-0.08-i*0.13)/0.08),700)});ctx.restore()}
  const E=['वायु','जल','पृथ्वी','अग्नि','आकाश'];E.forEach((n,i)=>{const a=ease((k-0.52-i*0.07)/0.08);if(a<=0)return;const x=190+i*225,y=H/2-10;ctx.save();ctx.globalAlpha=a;glow(x,y,110,['190,230,255','120,180,255','200,150,90','255,150,60','220,200,255'][i],0.4);
    ctx.lineWidth=5;ctx.lineCap='round';if(i===0){ctx.strokeStyle='#cfeaff';for(let j=0;j<3;j++){ctx.beginPath();ctx.moveTo(x-40,y-18+j*18);ctx.bezierCurveTo(x-10,y-34+j*18,x+10,y-2+j*18,x+36,y-14+j*18);ctx.stroke()}}
    if(i===1){ctx.fillStyle='#6fb4ff';ctx.beginPath();ctx.moveTo(x,y-50);ctx.quadraticCurveTo(x+46,y+10,x,y+44);ctx.quadraticCurveTo(x-46,y+10,x,y-50);ctx.fill()}
    if(i===2){ctx.fillStyle='#9a6a3a';ctx.fillRect(x-40,y-34,80,68);ctx.fillStyle='#6a8a3a';ctx.fillRect(x-40,y-34,80,14)}
    if(i===3){ctx.fillStyle='#ff7a2a';ctx.beginPath();ctx.moveTo(x-32,y+40);ctx.quadraticCurveTo(x-44,y-10,x,y-56);ctx.quadraticCurveTo(x+44,y-10,x+32,y+40);ctx.fill();ctx.fillStyle='#ffd35a';ctx.beginPath();ctx.moveTo(x-16,y+40);ctx.quadraticCurveTo(x-18,y,x,y-20);ctx.quadraticCurveTo(x+18,y,x+16,y+40);ctx.fill()}
    if(i===4){ctx.strokeStyle='#e6dcff';ctx.beginPath();ctx.arc(x,y,42,0,7);ctx.stroke();ctx.beginPath();ctx.arc(x,y,22,0,7);ctx.stroke()}
    ctx.restore();txt(n,x,y+82,40,'#f6ecd8',a,700)})},
narayana(t,d){const k=clamp(t/d);skyG(['#070b24','#18265a','#3a4f8c','#d79a78'],440);glow(W/2,440,520,'255,190,130',0.5);dust(t,60,5,'255,230,200',0.4,3);
  view(lerp(1.0,1.18,ease(k)),W/2,lerp(400,360,k),0,()=>{ocean(t,440,'#16254f','#050a1c','190,210,255',W/2);vishnuLying(W/2,420+Math.sin(t*0.9)*5,0.95,t,{})});
  const a=ease((k-0.7)/0.1);txt('नारायण',W/2,150,100,'#ffe2a0',a,700);glow(W/2,150,260,'255,210,130',0.3*a)},
egg_lotus(t,d){const k=clamp(t/d);skyG(['#070b24','#18265a','#3a4f8c','#d79a78'],440);glow(W/2,440,520,'255,190,130',0.5);dust(t,60,6,'255,230,200',0.4,3);
  const eg=ease(k/0.2)*(1-ease((k-0.55)/0.2)*0.8),zoom=lerp(1.0,1.3,ease(k));
  view(zoom,W/2,lerp(400,315,ease(k)),0,()=>{ocean(t,440,'#16254f','#050a1c','190,210,255',W/2);
   if(eg>0){ctx.save();ctx.globalAlpha=eg;const g=ctx.createRadialGradient(W/2-60,360,10,W/2,380,320);g.addColorStop(0,'rgba(255,245,200,.9)');g.addColorStop(0.7,'rgba(255,200,90,.45)');g.addColorStop(1,'rgba(255,170,60,.15)');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(W/2,390,340,250,0,0,7);ctx.fill();ctx.restore();glow(W/2,390,420,'255,210,110',0.4*eg)}
   vishnuLying(W/2,420+Math.sin(t*0.9)*4,0.95,t,{lotus:ease((k-0.5)/0.3),brahma:ease((k-0.72)/0.1)})});
  vishnuStarFlash(Math.max(0,0.5*(1-Math.abs(k-0.73)/0.03)))},
split(t,d){const k=clamp(t/d);skyG(['#05040f','#0a0820']);dust(t,80,8,'255,230,180',0.4,3);const cx=W/2,cy=H/2,R=210;
  const sep=ease((k-0.45)/0.4)*250,gl=ease(k/0.25);
  const sk=ease((k-0.7)/0.3);if(sk>0){ctx.save();ctx.globalAlpha=sk;const g=ctx.createLinearGradient(0,0,0,cy);g.addColorStop(0,'#0b1a52');g.addColorStop(1,'#5aa0e6');ctx.fillStyle=g;ctx.fillRect(0,0,W,cy-10);ctx.restore();stars(t,60)}
  if(sk>0){ctx.save();ctx.globalAlpha=sk;const g=ctx.createLinearGradient(0,cy+10,0,H);g.addColorStop(0,'#5b8a3a');g.addColorStop(0.2,'#3c6a2c');g.addColorStop(1,'#1a2a14');ctx.fillStyle=g;ctx.fillRect(0,cy+10,W,H);ctx.restore()}
  if(k<0.88){const fa=1-ease((k-0.75)/0.13);ctx.save();ctx.globalAlpha=fa;glow(cx,cy,420,'255,210,110',0.5*gl);
   [[-1,0],[1,Math.PI]].forEach(([dir,a0])=>{ctx.save();ctx.beginPath();if(dir<0){ctx.rect(0,0,W,cy-sep*0.0)}ctx.restore()});
   ctx.save();ctx.beginPath();ctx.rect(0,0,W,cy);ctx.clip();ctx.translate(0,-sep);const g=ctx.createRadialGradient(cx-50,cy-60,10,cx,cy,R);g.addColorStop(0,'#fff3c4');g.addColorStop(0.7,'#f0b23a');g.addColorStop(1,'#a8661a');ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.fill();ctx.restore();
   ctx.save();ctx.beginPath();ctx.rect(0,cy,W,H);ctx.clip();ctx.translate(0,sep);const g2=ctx.createRadialGradient(cx-50,cy-60,10,cx,cy,R);g2.addColorStop(0,'#fff3c4');g2.addColorStop(0.7,'#f0b23a');g2.addColorStop(1,'#a8661a');ctx.fillStyle=g2;ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.fill();ctx.restore();
   if(k>0.25&&k<0.5){const ca=ease((k-0.25)/0.1);ctx.strokeStyle=`rgba(255,255,255,${ca})`;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(cx-R,cy);for(let i=1;i<=8;i++)ctx.lineTo(cx-R+i*R/4,cy+(i%2?-14:14));ctx.stroke();glow(cx,cy,300,'255,240,200',0.6*ca)}
   if(sep>0){ctx.save();ctx.globalCompositeOperation='lighter';const g3=ctx.createLinearGradient(0,cy-sep,0,cy+sep);g3.addColorStop(0,'rgba(255,240,200,0)');g3.addColorStop(0.5,'rgba(255,240,200,.9)');g3.addColorStop(1,'rgba(255,240,200,0)');ctx.fillStyle=g3;ctx.fillRect(0,cy-sep,W,sep*2);ctx.restore()}
   ctx.restore()}
  if(k>0.82){const a=ease((k-0.82)/0.12);txt('स्वर्ग',W/2,110,60,'#e8f2ff',a);txt('आकाश',W/2,cy,52,'#fff3c4',a*0.9,400);txt('पृथ्वी',W/2,H-110,60,'#e8f0d0',a)}},
vedas(t,d){const k=clamp(t/d);skyG(['#0f1a4a','#3a4a8c','#d98a68','#ffcf88'],460);glow(W/2,470,520,'255,200,130',0.5);rays(W/2,300,t,'255,220,150',0.07);
  ocean(t,500,'#2a3a6c','#0a1030','255,210,170',W/2);
  const calm=1-ease((k-0.88)/0.1);lotusFlower(W/2,545,1.7,1,t);brahma(W/2,520,1.45,t,{eye:k<0.78?0.1:1,mouth:k<0.78?0.1:0.9,aura:'255,215,140'});
  const V=[['ऋग्वेद','255,120,90'],['यजुर्वेद','120,200,255'],['सामवेद','180,255,160'],['अथर्ववेद','255,220,120']];
  V.forEach(([n,c],i)=>{const a=ease((k-0.12-i*0.14)/0.1);if(a<=0)return;const ang=-2.5+i*0.62,rr=330,x=W/2+Math.cos(ang)*rr*1.1,y=250+Math.sin(ang)*rr*0.55+Math.sin(t*1.5+i)*8;vedaScroll(x,y,1.5,Math.sin(t+i)*0.08,c,true,a);txt(n,x,y+78,34,'#fff0cc',a)});
  const red=ease((k-0.9)/0.1);if(red>0){ctx.fillStyle=`rgba(120,10,10,${0.35*red})`;ctx.fillRect(0,0,W,H)}},
birth(t,d,P){const k=clamp(t/d);skyG(['#02050f','#08142e','#0e2a4a'],470);ctx.save();ctx.globalAlpha=1;moon(W*0.82,110,30,t);ctx.restore();stars(t,80);
  view(1.1,W/2,H/2+10,0,()=>{ocean(t,470,'#0c2038','#020610','150,190,230',W*0.3);vishnuLying(W*0.3,455,0.7,t,{aura:0.25});
   const asu=(x0,y0,dx,dy,col,eyec,ant,ph)=>{const u=ease((k-0.12-ph)/0.5);if(u<=0)return;const x=x0+dx*u,y=y0+dy*u+Math.sin(t*6+ph*9)*3*u;ctx.save();ctx.globalAlpha=Math.min(1,u*2);ctx.fillStyle=col;ctx.beginPath();ctx.ellipse(x,y,30,16,0,0,7);ctx.fill();ctx.beginPath();ctx.arc(x+26,y-6,15,0,7);ctx.fill();
     ctx.strokeStyle=col;ctx.lineWidth=5;ctx.lineCap='round';for(let i=0;i<3;i++){const lx=x-14+i*14,sw=Math.sin(t*10+i*2+ph*5)*5;ctx.beginPath();ctx.moveTo(lx,y+8);ctx.lineTo(lx+sw,y+24);ctx.stroke()}
     if(ant){ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(x+30,y-18);ctx.quadraticCurveTo(x+44,y-44,x+58,y-38);ctx.moveTo(x+24,y-18);ctx.quadraticCurveTo(x+30,y-50,x+46,y-52);ctx.stroke()}
     glow(x+30,y-8,34,eyec,0.9);ctx.fillStyle='#ffe27a';ctx.beginPath();ctx.arc(x+32,y-9,3.5,0,7);ctx.fill();ctx.restore()};
   asu(W*0.3-80,420,420,40,'#241a3a','255,200,60',false,0);asu(W*0.3-70,430,300,70,'#173a2e','255,120,60',true,0.12)});
  const a1=ease((k-0.5)/0.1),a2=ease((k-0.72)/0.1);txt('मधु',W*0.62,300,64,'#ffd27a',a1);txt('कैटभ',W*0.78,360,64,'#9af2c8',a2);dissolveCard(P,t,d)},
grow(t,d){const k=clamp(t/d),g=ease(k);skyG(['#02050f','#0b1a3a','#1c3a5e','#355a80'],470);stars(t,60);
  view(lerp(1.0,0.82,g),W/2,lerp(390,330,g),0,()=>{
   drawChar('madhu',W*0.34,640,lerp(0.7,2.3,g),1,t,{pose:'idle',expr:{brow:-0.4,mouth:0.6,eye:0.9,open:0.2+0.2*Math.sin(t*5)},rim:'rgba(150,200,255,.9)',rimScreen:-3,warm:'rgba(80,120,200,0.25)'});
   drawChar('kaitabha',W*0.70,640,lerp(0.6,2.1,g),-1,t,{pose:'idle',expr:{brow:-0.5,mouth:0.8,eye:0.9,open:0.2+0.2*Math.sin(t*5+1)},rim:'rgba(150,200,255,.9)',rimScreen:3,warm:'rgba(80,120,200,0.25)'});
   ocean(t,560,'rgba(12,32,56,.92)','#020610','150,190,230',W/2)})},
confront(t,d){const k=clamp(t/d);skyG(['#02050f','#0a1a3a','#1b3a64'],470);moon(W*0.15,100,26,t);stars(t,70);
  view(lerp(1.0,1.15,ease(k)),W/2,H/2,0,()=>{ocean(t,560,'#0c2038','#020610','150,190,230',W*0.2);
   drawChar('madhu',W*0.66,760,2.6,-1,t,{pose:'point',lean:-0.05,expr:{brow:-0.9,mouth:-0.4,eye:0.85,open:0.5,talk:1},rim:'rgba(150,200,255,.9)',rimScreen:3,warm:'rgba(90,120,210,0.25)'});
   drawChar('kaitabha',W*0.86,790,2.3,-1,t,{pose:'fist',lean:-0.04,expr:{brow:-0.9,mouth:-0.3,eye:0.85,talk:0.8},rim:'rgba(150,200,255,.9)',rimScreen:3,warm:'rgba(90,120,210,0.25)'});
   lotusFlower(W*0.2,590,1.4,1,t);brahma(W*0.2,570,1.0,t,{eye:1.1,brow:0.8,mouth:-0.6,aura:'255,215,140'})})},
shake(t,d){const k=clamp(t/d),[sx,sy]=shakeOf(t,6*clamp(k*5)*(1-ease((k-0.5)/0.4)*0.6));skyG(['#02050f','#0a1a3a','#1b3a64'],470);moon(W*0.15,100,26,t);stars(t,70);
  view(1.12,W/2+sx,H/2+sy,0,()=>{ocean(t,560,'#0c2038','#020610','150,190,230',W*0.2);
   drawChar('madhu',W*0.66,760,2.6,-1,t,{pose:'fist',lean:-0.06,expr:{brow:-0.7,mouth:1,eye:0.8,open:0.9,tilt:-0.18,talk:1},rim:'rgba(150,200,255,.9)',rimScreen:3,warm:'rgba(90,120,210,0.25)'});
   drawChar('kaitabha',W*0.86,790,2.3,-1,t,{pose:'fist',lean:-0.05,expr:{brow:-0.6,mouth:1,eye:0.8,open:0.9,tilt:-0.15,talk:1},rim:'rgba(150,200,255,.9)',rimScreen:3,warm:'rgba(90,120,210,0.25)'});
   ctx.save();ctx.translate(W*0.2,570);ctx.rotate(Math.sin(t*9)*0.045*clamp(k*4));ctx.translate(-W*0.2,-570);lotusFlower(W*0.2,590,1.4,1,t);brahma(W*0.2,570,1.0,t,{eye:1.3,brow:1,mouth:-0.8,open:0.6,rot:0,aura:'255,215,140'});ctx.restore();
   ['255,120,90','120,200,255','180,255,160','255,220,120'].forEach((c,i)=>{const s0=0.22+i*0.1,u=clamp((k-s0)/0.4);if(u<=0)return;const x=W*0.2+(i-1.5)*40+u*(i-1.5)*40,y=330+u*u*240;vedaScroll(x,y,1.1,u*5*(i%2?1:-1),c,true,1-ease((u-0.85)/0.15));splash(x,572,s0*d+0.4*d*0.88,t,1.2)});
  })},
plea(t,d){const k=clamp(t/d);skyG(['#05081c','#12204a','#243a72']);dust(t,70,13,'200,220,255',0.4,3);
  view(lerp(1.0,1.12,ease(k)),W/2,H/2,0,()=>{glow(W*0.68,360,400,'120,150,255',0.25);
   ctx.save();ctx.globalAlpha=0.9;vishnuLying(W*0.22,610,0.4,t,{});ctx.restore();
   lotusFlower(W*0.62,690,2.4,1,t);brahma(W*0.62,660,2.1,t,{pose:'plead',eye:1.25,brow:1,mouth:-0.8,talk:1,aura:'255,215,140'})});
  },
nidra(t,d){const k=clamp(t/d);skyG(['#050a24','#10206a','#2a3a9a','#5a6ac0']);moon(W*0.5,150,50,t);dust(t,90,17,'190,210,255',0.5,5);
  ctx.save();for(let i=0;i<7;i++){const y=380+i*40,off2=Math.sin(t*0.6+i)*80;const g=ctx.createLinearGradient(0,y,W,y);g.addColorStop(0,'rgba(80,90,200,0)');g.addColorStop(0.5,`rgba(120,130,230,${0.25})`);g.addColorStop(1,'rgba(80,90,200,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(-100,y);for(let x=-100;x<=W+100;x+=40)ctx.lineTo(x,y+Math.sin(x*0.01+t*0.8+i)*26+off2*0.2);ctx.lineTo(W+100,y+120);ctx.lineTo(-100,y+120);ctx.fill()}ctx.restore();
  lotusFlower(W*0.5,690,1.8,1,t);brahma(W*0.5,665,1.5,t,{pose:'plead',eye:0.7,brow:0.7,mouth:0.1,aura:'200,210,255'});
  const e=ease((k-0.72)/0.18);if(e>0){ctx.save();ctx.globalAlpha=e;glow(W*0.5,300,420,'255,235,180',0.5);[-1,1].forEach(sd=>{ctx.fillStyle='#fffbe8';ctx.beginPath();ctx.moveTo(W*0.5+sd*40,300);ctx.quadraticCurveTo(W*0.5+sd*130,250,W*0.5+sd*230,300);ctx.quadraticCurveTo(W*0.5+sd*130,350,W*0.5+sd*40,300);ctx.fill();ctx.fillStyle='#3a5ab0';ctx.beginPath();ctx.arc(W*0.5+sd*135,300,36,0,7);ctx.fill();ctx.fillStyle='#0a1030';ctx.beginPath();ctx.arc(W*0.5+sd*135,300,16,0,7);ctx.fill()});ctx.restore();rays(W*0.5,300,t,'255,235,180',0.1*e)}
  vishnuStarFlash(Math.max(0,(k-0.96)/0.04*0.8))},
hayagriva(t,d){const k=clamp(t/d),yr=Math.floor(ease(k)*5000),sh=shakeOf(t,3);const cyc=k*6.283*3;
  const dayA=0.5+0.5*Math.sin(cyc);skyG([dayA>0.5?'#2a3a7a':'#05071a',dayA>0.5?'#e07a55':'#0e1840',dayA>0.5?'#ffcf88':'#1c2c5a'],470);
  view(1.1,W/2+sh[0],H/2+sh[1],0,()=>{ocean(t,540,'#16254f','#050a1c','255,210,170',W/2);
   const p=Math.sin(t*3.2),c1=W*0.36+p*40,c2=W*0.74-p*30;
   drawChar('hayagriva',c1,700,2.0,1,t,{pose:'point',lean:0.1+p*0.05,expr:{brow:-0.7,mouth:-0.3,eye:0.85},rim:'rgba(255,220,160,.95)',rimScreen:-3,warm:'rgba(255,160,90,0.25)'});
   drawChar('madhu',W*0.62+(-p)*20,720,2.1,-1,t,{pose:'fist',lean:-0.1,expr:{brow:-0.9,mouth:-0.5,eye:0.9,open:0.5},rim:'rgba(255,200,150,.9)',rimScreen:3,warm:'rgba(255,150,90,0.25)'});
   drawChar('kaitabha',W*0.86+p*20,740,2.0,-1,t,{pose:'point',lean:-0.1,expr:{brow:-0.9,mouth:-0.5,eye:0.9,open:0.5},rim:'rgba(255,200,150,.9)',rimScreen:3,warm:'rgba(255,150,90,0.25)'});
   const fl=Math.max(0,Math.sin(t*3.2*2+0.4));if(fl>0.85){glow(W*0.55,420,260,'255,240,200',0.8);ctx.strokeStyle='rgba(255,255,255,.9)';ctx.lineWidth=4;for(let i=0;i<8;i++){const a=i/8*6.283;ctx.beginPath();ctx.moveTo(W*0.55+Math.cos(a)*30,420+Math.sin(a)*30);ctx.lineTo(W*0.55+Math.cos(a)*120,420+Math.sin(a)*120);ctx.stroke()}}});
  let ds='';String(yr).split('').forEach(c=>ds+=DIG[+c]);txt(ds+' वर्ष',W-60,70,60,'#ffd27a',1,700,'right')},
trick(t,d,P){const k=clamp(t/d),ph=P.phase||1;skyG(['#1a1440','#5b3a7a','#d9775a'],470);glow(W*0.5,440,520,'255,190,130',0.4);
  view(lerp(1.0,ph===3?1.35:1.12,ease(k)),W/2,lerp(H/2,ph===3?340:H/2,ease(k)),0,()=>{ocean(t,560,'#2a2a62','#0a0a22','255,200,170',W/2);
   drawChar('hayagriva',W*0.28,720,2.1,1,t,{pose:ph===1?'greet':(ph===2?'plead':'folded'),lean:0.04,expr:ph===1?{brow:0.5,mouth:0.9,eye:1,talk:1,tilt:0.04}:(ph===2?{brow:0.2,mouth:0.6,eye:1,talk:0.8}:{brow:-0.5,mouth:1,eye:0.8,tilt:-0.06}),rim:'rgba(255,215,160,.95)',rimScreen:-3,warm:'rgba(255,160,90,0.25)'});
   const L=ph===2;drawChar('madhu',W*0.66,740,2.2,-1,t,{pose:ph===3?'idle':'fist',lean:ph===3?0.08:-0.04,expr:L?{brow:-0.6,mouth:1,eye:0.8,open:0.95,tilt:-0.2,talk:1}:(ph===3?{brow:0.9,mouth:-0.7,eye:1.3,open:0.4}:{brow:-0.3,mouth:0.8,eye:0.9,talk:0.4}),rim:'rgba(255,200,150,.9)',rimScreen:3,warm:'rgba(255,150,90,0.25)'});
   drawChar('kaitabha',W*0.86,760,2.1,-1,t,{pose:ph===3?'idle':'fist',lean:ph===3?0.08:-0.04,expr:L?{brow:-0.6,mouth:1,eye:0.8,open:0.95,tilt:-0.2,talk:1}:(ph===3?{brow:0.9,mouth:-0.7,eye:1.3,open:0.4}:{brow:-0.3,mouth:0.8,eye:0.9,talk:0.4}),rim:'rgba(255,200,150,.9)',rimScreen:3,warm:'rgba(255,150,90,0.25)'})});
  if(ph===3){const a=ease(k)*0.4;ctx.fillStyle=`rgba(80,0,0,${a})`;ctx.fillRect(0,0,W,H)}},
water(t,d){const k=clamp(t/d);skyG(['#120a30','#3a2060','#c85a5a','#ffb070'],440);glow(W*0.5,440,520,'255,190,130',0.5);
  view(lerp(1.5,0.9,ease(k)),W/2,lerp(420,380,k),0,()=>{ocean(t,520,'#2a2a62','#0a0a22','255,200,170',W/2);
   const lk=Math.sin(t*1.4)*1.2;drawChar('madhu',W*0.40,690,2.0,1,t,{pose:'idle',lean:0.06,expr:{brow:0.9,mouth:-0.8,eye:1.3,open:0.5,look:lk},rim:'rgba(255,200,150,.9)',rimScreen:-3,warm:'rgba(255,150,90,0.25)'});
   drawChar('kaitabha',W*0.62,700,1.9,-1,t,{pose:'idle',lean:0.06,expr:{brow:0.9,mouth:-0.8,eye:1.3,open:0.5,look:-lk},rim:'rgba(255,200,150,.9)',rimScreen:3,warm:'rgba(255,150,90,0.25)'})})},
vgrow(t,d){const k=clamp(t/d),g=ease(clamp(k/0.62));skyG(['#0b1a52','#3a5ab0','#e2a07a','#ffd9a0'],500);glow(W/2,520,520,'255,200,140',0.5);
  ocean(t,560,'#2a3a7a','#0a1030','255,220,180',W/2);const s=lerp(1.4,4.6,g);
  drawChar('hayagriva',W/2,lerp(740,1180,g),s,1,t,{pose:'folded',expr:{brow:-0.3,mouth:1,eye:0.9},rim:'rgba(255,225,170,.95)',rimScreen:-3,warm:'rgba(255,170,100,0.25)'});
  const sm=1-ease((k-0.55)/0.08);if(sm>0){ctx.save();ctx.globalAlpha=sm;drawChar('madhu',W*0.33,lerp(620,560,g),0.5,1,t,{pose:'idle',expr:{brow:0.9,mouth:-0.8,eye:1.3,open:0.6}});drawChar('kaitabha',W*0.67,lerp(620,560,g),0.5,-1,t,{pose:'idle',expr:{brow:0.9,mouth:-0.8,eye:1.3,open:0.6}});ctx.restore()}
  const f=Math.max(0,1-Math.abs(k-0.66)/0.03);vishnuStarFlash(0.9*f);
  if(k>0.66&&k<0.78){ctx.save();ctx.strokeStyle=`rgba(255,255,255,${1-(k-0.66)/0.12})`;ctx.lineWidth=14;ctx.beginPath();ctx.moveTo(W*0.2,0);ctx.lineTo(W*0.8,H);ctx.stroke();ctx.restore()}
  const a=ease((k-0.8)/0.12);glow(W/2,250,380,'255,210,130',0.4*a);txt('मधुसूदन',W/2,250,130,'#ffe2a0',a,700)},
reflect(t,d){const k=clamp(t/d);skyG(['#1a2a6a','#6a6ab0','#f0a080','#ffe0a8'],480);glow(W*0.5,480,560,'255,215,160',0.55);rays(W/2,480,t,'255,225,170',0.06);
  ocean(t,520,'#3a4a8a','#0e1434','255,215,180',W/2);
  const sp=k<0.5;lotusFlower(W*0.24,650,1.7,1,t);brahma(W*0.24,625,1.45,t,{eye:1,brow:0.5,mouth:-0.2,talk:sp?1:0,aura:'255,215,140',pose:'meditate'});
  drawChar('vishnu',W*0.7,690,2.0,-1,t,{pose:'idle',expr:{brow:0.1,mouth:0.5,eye:0.95,talk:sp?0:1,tilt:0.04},rim:'rgba(255,225,170,.95)',rimScreen:-3,warm:'rgba(255,170,100,0.25)'})},
earth(t,d){const k=clamp(t/d);skyG(['#1a2a6a','#6a6ab0','#f0a080','#ffe0a8'],480);glow(W*0.5,480,560,'255,215,160',0.5);
  ocean(t,500,'#3a4a8a','#0e1434','255,215,180',W/2);const rise=ease(k/0.7);
  ctx.save();ctx.beginPath();ctx.rect(0,0,W,H);ctx.clip();const by=lerp(760,470,rise);ctx.fillStyle='#6a4a30';ctx.beginPath();ctx.moveTo(180,by+300);ctx.quadraticCurveTo(300,by-30,560,by);ctx.quadraticCurveTo(820,by-60,1060,by+20);ctx.lineTo(1120,by+300);ctx.fill();ctx.fillStyle='#4a8a3a';ctx.beginPath();ctx.moveTo(300,by+30);ctx.quadraticCurveTo(420,by-20,560,by-4);ctx.quadraticCurveTo(820,by-60,960,by-6);ctx.lineTo(960,by+30);ctx.fill();
  const cr=ease((k-0.45)/0.3);ctx.strokeStyle=`rgba(255,150,60,${0.9*cr})`;ctx.lineWidth=3;for(let i=0;i<6;i++){const x=240+i*150;ctx.beginPath();ctx.moveTo(x,by+10);ctx.lineTo(x+20,by+120);ctx.lineTo(x-10,by+240);ctx.stroke()}ctx.beginPath();ctx.moveTo(200,by+120);ctx.lineTo(1100,by+110);ctx.stroke();ctx.restore();
  const ve=ease((k-0.1)/0.2);['255,120,90','120,200,255','180,255,160','255,220,120'].forEach((c,i)=>{const u=clamp((k-0.08-i*0.04)/0.4);vedaScroll(lerp(W*0.5,W*0.17,ease(u)),lerp(380,200+i*30,ease(u))+Math.sin(t*2+i)*6,0.9,0,c,true,u>0?1:0)});
  lotusFlower(W*0.16,330,1.0,1,t);brahma(W*0.16,312,0.9,t,{eye:1,brow:-0.2,mouth:1,aura:'255,215,140'});
  txt('मेदिनी',W*0.62,220,92,'#ffe2a0',ease((k-0.5)/0.12),700);txt('पृथ्वी की बारह परतें',W*0.62,300,40,'#ffd1a0',ease((k-0.72)/0.1),400)},
ending(t,d){const k=clamp(t/d),dk=ease((k-0.45)/0.4);skyG(['#1a2a6a','#6a6ab0','#f0a080','#ffe0a8'],480);
  ctx.save();ctx.globalAlpha=dk;skyG(['#120408','#3a0f18','#7a1c20','#c8402a'],480);ctx.restore();glow(W*0.5,480,560,'255,215,160',0.5*(1-dk));glow(W*0.5,500,500,'255,70,40',0.4*dk);
  view(lerp(1.4,0.95,ease(k)),W/2,lerp(560,400,ease(k)),0,()=>{ocean(t,520,lerp(0x3a,0x30,dk)?'#3a4a8a':'#3a4a8a','#0e1434','255,215,180',W/2);
   lotusFlower(W*0.5,650,1.7,1,t);brahma(W*0.5,625,1.45,t,{eye:1,brow:dk*0.9,mouth:0.6-dk*1.4,aura:'255,215,140'})});
  ctx.save();ctx.globalAlpha=0.6*dk;for(let i=0;i<5;i++){ctx.fillStyle='#1a060a';const x=mod(i*300+t*20,W+600)-300;ctx.beginPath();ctx.ellipse(x,110+i*18,320,56,0,0,7);ctx.fill()}ctx.restore();
  const lf=Math.max(0,1-Math.abs(k-0.88)/0.025);vishnuStarFlash(0.85*lf)},
teaser(t,d){const k=clamp(t/d);skyG(['#02030c','#0a1030','#1a2250']);stars(t,120);moon(W*0.16,150,48,t);
  ctx.fillStyle='#0b0f22';ctx.beginPath();ctx.moveTo(-50,H);ctx.lineTo(260,420);ctx.lineTo(380,470);ctx.lineTo(560,300);ctx.lineTo(700,430);ctx.lineTo(900,360);ctx.lineTo(1100,480);ctx.lineTo(W+50,H);ctx.fill();
  ctx.fillStyle='#e8eef8';ctx.beginPath();ctx.moveTo(900,360);ctx.lineTo(980,300);ctx.lineTo(1060,372);ctx.quadraticCurveTo(980,350,900,360);ctx.fill();
  ctx.strokeStyle='#dfe6ff';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(980,250);ctx.lineTo(980,420);ctx.stroke();ctx.beginPath();ctx.moveTo(950,270);ctx.lineTo(950,245);ctx.moveTo(980,255);ctx.lineTo(980,225);ctx.moveTo(1010,270);ctx.lineTo(1010,245);ctx.moveTo(950,270);ctx.quadraticCurveTo(980,292,1010,270);ctx.stroke();
  mist(t,520,'160,180,255',0.18,3);dust(t,60,23,'200,220,255',0.4,3);
  txt('अगली कहानी',W/2,120,44,'#cfd8f0',ease((k-0.1)/0.15),400);txt('भगवान शिव का प्राकट्य',W/2,190,84,'#ffe2a0',ease((k-0.25)/0.2),700);txt('कल मिलते हैं',W/2,H-90,54,'#f4ecd6',ease((k-0.62)/0.2),700)}
});

/* ===== cutaway / insert shots ===== */
function eyeShape(cx,cy,w,h,iris,kind,t,tilt){ctx.save();ctx.translate(cx,cy);ctx.rotate(tilt||0);
  ctx.fillStyle=kind==='glow'?'#14091a':'#f7f2e4';ctx.beginPath();ctx.moveTo(-w,0);ctx.quadraticCurveTo(0,-h*1.5,w,0);ctx.quadraticCurveTo(0,h*1.5,-w,0);ctx.fill();
  ctx.save();ctx.beginPath();ctx.moveTo(-w,0);ctx.quadraticCurveTo(0,-h*1.5,w,0);ctx.quadraticCurveTo(0,h*1.5,-w,0);ctx.clip();
  const ix=Math.sin(t*0.9)*10;ctx.fillStyle=iris;ctx.beginPath();ctx.arc(ix,0,h*0.95,0,7);ctx.fill();
  if(kind==='glow'){glow(ix,0,h*1.8,'255,200,60',0.8);ctx.fillStyle='#120008';ctx.beginPath();ctx.ellipse(ix,0,h*0.16,h*0.85,0,0,7);ctx.fill()}else{ctx.fillStyle='#0c0608';ctx.beginPath();ctx.arc(ix,0,h*(kind==='wide'?0.22:0.4),0,7);ctx.fill();ctx.fillStyle='rgba(255,255,255,.85)';ctx.beginPath();ctx.arc(ix-h*0.25,-h*0.3,h*0.12,0,7);ctx.fill()}
  ctx.restore();ctx.restore()}
Object.assign(SHOTS,{
starfly(t,d,P){const k=clamp(t/d);skyG(['#02020c','#070822','#0c0f33']);const r=rng(41),cx=W/2,cy=H/2;ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<260;i++){const x=(r()-0.5)*2.2,y=(r()-0.5)*1.4,z0=r();const z=mod(z0-t*0.12,1)+0.02,pz=z+0.045;const sx=cx+x/z*W*0.32,sy=cy+y/z*W*0.32,px=cx+x/pz*W*0.32,py=cy+y/pz*W*0.32;
    ctx.strokeStyle=`rgba(${P.rgb||'220,225,255'},${clamp((1-z)*1.2)})`;ctx.lineWidth=1+(1-z)*2.4;ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(sx,sy);ctx.stroke()}ctx.restore();
  glow(cx,cy,260+k*200,P.rgb||'255,225,160',0.35+0.3*k)},
eyes(t,d,P){const k=clamp(t/d),kd=P.kind||'glow';skyG(['#05020a','#0c0618','#05020a']);const col=kd==='glow'?'#ffbb33':(kd==='wide'?'#5a3a2a':'#2a4a8a');
  view(lerp(1.0,1.18,ease(k)),W/2,H/2,0,()=>{glow(W/2,H/2,520,kd==='glow'?'255,170,40':'120,150,255',0.22);
   const bl=(mod(t,2.8)<0.12)?0.15:1,h=kd==='wide'?74:56,tl=kd==='glow'?0.18:(kd==='worried'?-0.12:0);
   eyeShape(W/2-165,H/2,125,h*bl,col,kd,t,tl);eyeShape(W/2+165,H/2,125,h*bl,col,kd,t,-tl);
   ctx.fillStyle='#05020a';ctx.save();if(kd==='glow'){ctx.beginPath();ctx.moveTo(W/2-310,H/2-100);ctx.lineTo(W/2-30,H/2-20);ctx.lineTo(W/2-30,H/2-120);ctx.lineTo(W/2-310,H/2-170);ctx.fill();ctx.beginPath();ctx.moveTo(W/2+310,H/2-100);ctx.lineTo(W/2+30,H/2-20);ctx.lineTo(W/2+30,H/2-120);ctx.lineTo(W/2+310,H/2-170);ctx.fill()}
   ctx.restore();ctx.strokeStyle='#1a0e12';ctx.lineWidth=14;ctx.lineCap='round';const bk=kd==='worried'||kd==='wide'?1:-1;[[-1],[1]].forEach(([sd])=>{ctx.beginPath();ctx.moveTo(W/2+sd*60,H/2-125+(bk>0?-20:10));ctx.lineTo(W/2+sd*290,H/2-135+(bk>0?20:-25));ctx.stroke()})});
  dust(t,40,29,'255,200,120',0.4,5)},
ripple(t,d,P){const k=clamp(t/d);skyG(['#02040c','#071230']);stars(t,70);const rgb=P.rgb||'150,190,230';ctx.save();ctx.translate(W/2,H*0.58);ctx.scale(1,0.42);
  for(let i=0;i<8;i++){const u=mod(t*0.28+i/8,1);ctx.strokeStyle=`rgba(${rgb},${0.7*(1-u)})`;ctx.lineWidth=3+u*2;ctx.beginPath();ctx.arc(0,0,20+u*620,0,7);ctx.stroke()}ctx.restore();
  glow(W/2,H*0.58,300,rgb,0.18);dust(t,40,31,rgb,0.4,3)}
});
