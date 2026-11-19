/* ===== Episode 02 scene library ===== */
(function(){
const shade=(h,k)=>{const n=parseInt(h.slice(1),16);let r=(n>>16)&255,g=(n>>8)&255,b=n&255;r=Math.round(clamp(r*k,0,255));g=Math.round(clamp(g*k,0,255));b=Math.round(clamp(b*k,0,255));return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1)};
/* ---- characters ---- */
CHARS.rudra={skin:'#5a6fae',skinD:'#3d4f8a',dhoti:'#2a1620',trim:'#e08a2a',hair:'#0c0810',crown:'none',shirt:null,beard:null,must:false,head:1.1,sash:'#ece6f0',jew:false,eyeGlow:true,third:true,trident:true,jata:true};
const RV=['#5a6fae','#6a5aae','#5a8aae','#7a5a9a','#4a6a8a','#6a7aae','#5a5aa0','#4a8a9a','#7a6aa8','#5a7a9a','#8a6aa0'];
RV.forEach((c,i)=>{CHARS['rudra'+(i+1)]=Object.assign({},CHARS.rudra,{skin:c,skinD:shade(c,0.7)})});
const KC=[['#f4f1e8','#c98a58'],['#dfe9ff','#b9825a'],['#fff3c8','#c48e60'],['#eadfff','#bf8a5c']];
KC.forEach((c,i)=>{CHARS['kumara'+i]={skin:c[1],skinD:shade(c[1],0.75),dhoti:c[0],trim:'#d9a441',hair:'#15101a',crown:'bun',shirt:null,beard:null,must:false,head:1.5,sash:'#ffffff',jew:false}});
const RC=[['#f0e6cf','#c28a5a'],['#e8c27a','#b8825a'],['#d98a4a','#c08a5a'],['#cfe0d0','#b88050'],['#e0d0e8','#c58f60'],['#f4efe0','#a87850'],['#c9a06a','#b98558']];
RC.forEach((c,i)=>{CHARS['rishi'+i]={skin:c[1],skinD:shade(c[1],0.75),dhoti:c[0],trim:'#d98a2a',hair:'#eeeaf2',crown:'bun',shirt:null,beard:'long',must:true,head:1.02,sash:'#d9a441',jew:false}});
CHARS.narada={skin:'#c68a5a',skinD:'#9a6540',dhoti:'#f4efe0',trim:'#d9a441',hair:'#1b1318',crown:'bun',shirt:null,beard:null,must:false,head:1.0,sash:'#e8b04a',jew:true,veena:true};
CHARS.agni={skin:'#e0663a',skinD:'#b04a2a',dhoti:'#a82a1a',trim:'#ffd23a',hair:'#ff7a1a',crown:'none',shirt:null,beard:null,must:true,head:1.05,sash:'#ffd23a',jew:true,flame:true};
CHARS.kamadeva={skin:'#e8a07a',skinD:'#c07a58',dhoti:'#d94a8a',trim:'#f6d6e0',hair:'#1b1318',crown:'gold',shirt:null,beard:null,must:false,head:1.0,sash:'#ff9ac0',jew:true};
CHARS.daksha={skin:'#c08a5a',skinD:'#98643e',dhoti:'#e9dfc2',trim:'#b8862a',hair:'#2a2a30',crown:'silver',shirt:'#c9a24a',beard:'short',must:true,head:1.04,sash:'#f4efe0',jew:true};
CHARS.vishwakarma={skin:'#a8704a',skinD:'#80502e',dhoti:'#6a8a5a',trim:'#d9a441',hair:'#1b1318',crown:'bun',shirt:null,beard:'short',must:true,head:1.0,sash:'#c9a24a',jew:false};

/* ---- helpers ---- */
function stand(name,x,y,s,flip,t,o){ctx.save();ctx.fillStyle='rgba(0,0,0,0.32)';ctx.beginPath();ctx.ellipse(x,y+3,38*s,8*s,0,0,7);ctx.fill();ctx.restore();drawChar(name,x,y,s,flip,t,o)}
function flames(x,y,s,t,c1='#ff5a1a',c2='#ffc24a',n=8){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const ph=i*1.7,h=90+Math.sin(t*6+ph)*24+(i%3)*16,w=24,xx=(i-(n-1)/2)*22;[[c1,1],[c2,0.55]].forEach(([c,k])=>{ctx.fillStyle=c;ctx.globalAlpha=0.8;ctx.beginPath();ctx.moveTo(xx-w*k,0);ctx.quadraticCurveTo(xx-w*0.8*k+Math.sin(t*7+ph)*8,-h*0.6*k,xx+Math.sin(t*5+ph)*10,-h*k);ctx.quadraticCurveTo(xx+w*0.8*k+Math.sin(t*7+ph)*8,-h*0.6*k,xx+w*k,0);ctx.fill()})}ctx.restore()}
function bolt(x0,y0,x1,y1,seed,a=1){const r=rng(seed);ctx.save();ctx.globalCompositeOperation='lighter';ctx.lineCap='round';[[14,0.25],[6,0.6],[2.5,1]].forEach(([w,al])=>{ctx.strokeStyle=`rgba(200,170,255,${a*al})`;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(x0,y0);const n=12;for(let i=1;i<=n;i++){const u=i/n;ctx.lineTo(lerp(x0,x1,u)+(r()-0.5)*70*(1-Math.abs(u-0.5)),lerp(y0,y1,u)+(r()-0.5)*14)}ctx.stroke()});ctx.restore()}
function shock(x,y,t0,t,rgb,max=900,sq=0.5){const u=(t-t0)/1.4;if(u<0||u>1)return;ctx.save();ctx.translate(x,y);ctx.scale(1,sq);ctx.strokeStyle=`rgba(${rgb},${0.8*(1-u)})`;ctx.lineWidth=10*(1-u)+2;ctx.beginPath();ctx.arc(0,0,u*max,0,7);ctx.stroke();ctx.restore()}
function nameTag(s,x,y,a,col='#ffe2a0',size=40){if(a<=0)return;if(TXQ){TXQ.push({k:'tag',s,x,y,size,col,a:ctx.globalAlpha*clamp(a),w:700,al:'center',m:ctx.getTransform()});return}txt(s,x,y,size,col,a,700)}
function floor(t,y,l,d){clouds(t,{seed:5,n:12,y0:y,y1:y+120,speed:10,scale:1.2,light:l,dark:d})}
function lensFlare(x,y,t,a=1){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=a;const g=ctx.createLinearGradient(x-420,y,x+420,y);g.addColorStop(0,'rgba(255,200,120,0)');g.addColorStop(0.5,'rgba(255,230,180,.55)');g.addColorStop(1,'rgba(255,200,120,0)');ctx.fillStyle=g;ctx.fillRect(x-420,y-3,840,6);[[-0.4,30,'255,160,90'],[0.3,18,'120,180,255'],[0.7,40,'255,200,120']].forEach(([k,r,c])=>{glow(lerp(x,W/2,k),lerp(y,H/2,k),r*2,c,0.28)});ctx.restore()}
function bull(x,y,s,t,o={}){const e=Object.assign({legs:4,alpha:1},o);ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.globalAlpha*=e.alpha;ctx.shadowColor='rgba(255,230,190,.9)';ctx.shadowOffsetX=-3;ctx.shadowBlur=0;
  const W1='#e6d6b4',WD='#b8a784',br=Math.sin(t*1.6)*1.6;
  [[-74,3],[-46,2],[46,1],[76,0]].forEach(([lx,idx],i)=>{const a=clamp(e.legs-idx);if(a<=0.01)return;ctx.save();ctx.globalAlpha*=a;ctx.fillStyle=i%2?WD:W1;ctx.fillRect(lx-9,-70,18,72);ctx.fillStyle='#3a2a22';ctx.fillRect(lx-10,-6,20,8);ctx.restore();if(a<1&&a>0.02){glow(lx,-40,70,'255,220,150',0.5*(1-a))}});
  ctx.fillStyle=W1;ctx.beginPath();ctx.ellipse(0,-100+br,112,50,0,0,7);ctx.fill();ctx.beginPath();ctx.ellipse(52,-146+br,42,32,0,0,7);ctx.fill();
  ctx.fillStyle=W1;ctx.beginPath();ctx.moveTo(90,-120+br);ctx.lineTo(128,-132+br);ctx.lineTo(146,-96+br);ctx.lineTo(112,-70+br);ctx.fill();
  ctx.beginPath();ctx.ellipse(150,-92+br,34,25,0.35,0,7);ctx.fill();ctx.fillStyle='#e8b4a0';ctx.beginPath();ctx.ellipse(172,-84+br,11,8,0.35,0,7);ctx.fill();
  ctx.strokeStyle='#ece3c6';ctx.lineWidth=7;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(138,-112+br);ctx.quadraticCurveTo(130,-148+br,150,-158+br);ctx.stroke();ctx.fillStyle=WD;ctx.beginPath();ctx.ellipse(128,-116+br,10,16,-0.6,0,7);ctx.fill();
  ctx.fillStyle='#1a1010';ctx.beginPath();ctx.arc(150,-99+br,3.4,0,7);ctx.fill();
  ctx.strokeStyle=W1;ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(-108,-110+br);ctx.quadraticCurveTo(-140,-100+Math.sin(t*2.4)*14,-132,-50+Math.sin(t*2.4+1)*8);ctx.stroke();
  ctx.restore()}
function mountain(x,base,h,w,col,snow,a=1){if(h<=2)return;ctx.save();ctx.globalAlpha*=a;ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(x-w,base);ctx.lineTo(x-w*0.12,base-h);ctx.lineTo(x+w*0.12,base-h*0.98);ctx.lineTo(x+w,base);ctx.fill();if(snow){ctx.fillStyle='#f4f7ff';ctx.beginPath();ctx.moveTo(x-w*0.3,base-h*0.7);ctx.lineTo(x-w*0.12,base-h);ctx.lineTo(x+w*0.12,base-h*0.98);ctx.lineTo(x+w*0.32,base-h*0.7);ctx.lineTo(x+w*0.12,base-h*0.78);ctx.lineTo(x,base-h*0.68);ctx.lineTo(x-w*0.14,base-h*0.78);ctx.fill()}ctx.restore()}
function humanOutline(cx,cy,s,t,rgb,a=1){ctx.save();ctx.translate(cx,cy);ctx.scale(s,s);ctx.globalAlpha*=a;ctx.strokeStyle=`rgba(${rgb},.9)`;ctx.lineWidth=4;ctx.setLineDash([10,8]);ctx.lineDashOffset=-t*20;ctx.beginPath();ctx.arc(0,-180,26,0,7);ctx.moveTo(-38,-150);ctx.lineTo(38,-150);ctx.lineTo(46,-60);ctx.lineTo(18,-60);ctx.lineTo(18,40);ctx.lineTo(-18,40);ctx.lineTo(-18,-60);ctx.lineTo(-46,-60);ctx.closePath();ctx.stroke();ctx.setLineDash([]);glow(0,-70,200,rgb,0.25+0.1*Math.sin(t*3));ctx.restore()}
const DK=['#02030c','#070d24'];

