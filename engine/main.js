/* ===== v4 timeline: shots start on spoken words, dissolves, serif subtitles, camera ===== */
const SHOTS={};let LAT=false,VERT=false;/* VERT = 9:16 reel build (studio/build.py --format vertical); false = the 16:9 episode engine, unchanged *//* LAT = English subtitles: Latin-first font stack, groups up to 42 chars (Hindi: 30) */
const SUBFONT=fs=>LAT?`600 ${fs}px NSerLat, 'Noto Serif', 'Source Serif 4', Georgia, 'Liberation Serif', 'DejaVu Serif', NSer, serif`:`600 ${fs}px NSer, serif`;let SHOTLIST,WORDS=[],GROUPS=[],GROUPOF=[],TOTAL=0,CW_=1920,CH_=1080;
const norm=x=>x.replace(/[।,.!?…"'“”‘’\-–—:;()‌‍]/g,'').trim();
function findPhrase(bw,ph,from){const toks=ph.split(/\s+/).map(norm);for(let i=from;i<bw.length;i++){let ok=true;for(let j=0;j<toks.length;j++){const w=bw[i+j];if(!w){ok=false;break}const wt=norm(w.text);if(!(wt.startsWith(toks[j])||toks[j].startsWith(wt))){ok=false;break}}if(ok)return i}return -1}
window.init=(shots,beats)=>{const bs={};let a=0;beats.forEach(b=>{bs[b.beat]={start:a,dur:b.duration};b.words.slice().sort((x,y)=>x.start-y.start).forEach(w=>WORDS.push({text:w.text,start:a+w.start,end:a+w.end,beat:b.beat,hide:w.hide}));a+=b.duration});TOTAL=a;window.total=a;LAT=WORDS.some(w=>/[A-Za-z]/.test(w.text));window.CUEMISS=[];
  const cursor={};const raw=[];
  shots.forEach(sh=>{const B=bs[sh.beat],bw=WORDS.filter(w=>w.beat===sh.beat);let st;if(typeof sh.at==='number')st=B.start+sh.at;else{const i=findPhrase(bw,sh.at,cursor[sh.beat]||0);if(i<0){window.CUEMISS.push(sh.at);st=(raw.length?raw[raw.length-1].start+1.5:B.start)}else{st=bw[i].start;cursor[sh.beat]=i+1}}raw.push(Object.assign({},sh,{start:st}))});
  raw.forEach((it,i)=>{it.end=i<raw.length-1?raw[i+1].start:TOTAL;
    if(it.cues){const bw=WORDS.filter(w=>w.beat===it.beat);let from=Math.max(0,bw.findIndex(w=>w.start>=it.start-0.01)),out=[];it.cues.forEach(ph=>{const j=findPhrase(bw,ph,from);if(j<0){window.CUEMISS.push(ph);out.push(null)}else{out.push(bw[j].start-it.start);from=j+1}});for(let q=0;q<out.length;q++)if(out[q]==null)out[q]=q?out[q-1]+0.6:0.3;it.cueT=out}});
  SHOTLIST=raw;
  let cur=[],pv=null;WORDS.forEach((w,i)=>{if(w.hide)return;const p=pv;pv=w;if(cur.length&&(w.beat!==p.beat||w.start-p.end>0.25||cur.reduce((n,j)=>n+WORDS[j].text.length+1,0)+w.text.length>(LAT?42:30))){GROUPS.push(cur);cur=[]}cur.push(i);GROUPOF[i]=GROUPS.length});if(cur.length)GROUPS.push(cur);
  window.SHOTINFO=SHOTLIST.map(s=>[s.draw,+s.start.toFixed(2),+(s.end-s.start).toFixed(2)]);
  return document.fonts.load('600 36px NSer','अ').then(()=>document.fonts.ready)};
function subs(c2,T){let wi=-1;for(let i=0;i<WORDS.length;i++){if(WORDS[i].hide)continue;if(WORDS[i].start<=T+0.03)wi=i;else break}if(wi<0||T-WORDS[wi].end>0.5)return;const g=GROUPS[GROUPOF[wi]];c2.save();c2.setTransform(SC_,0,0,SC_,0,0);
  let fs=36;c2.font=SUBFONT(fs);let sp=c2.measureText(' ').width+6,tot=0,ws=[];const meas=()=>{tot=0;ws=g.map(i=>{const m=c2.measureText(WORDS[i].text).width;tot+=m+sp;return m});tot-=sp};meas();if(tot>W-160){fs=Math.floor(fs*(W-160)/tot);c2.font=SUBFONT(fs);sp=c2.measureText(' ').width+6;meas()}
  const gr=c2.createLinearGradient(0,H-150,0,H);gr.addColorStop(0,'rgba(6,4,18,0)');gr.addColorStop(1,'rgba(6,4,18,.62)');c2.fillStyle=gr;c2.fillRect(0,H-150,W,150);let x=(W-tot)/2;const y=H-58;c2.textBaseline='middle';c2.textAlign='left';g.forEach((wj,j)=>{const on=wj===wi,past=wj<wi;c2.save();c2.lineJoin='round';c2.lineWidth=5;c2.strokeStyle='rgba(8,6,24,.6)';c2.strokeText(WORDS[wj].text,x,y);c2.shadowColor='rgba(0,0,0,.85)';c2.shadowBlur=10;c2.shadowOffsetY=2;c2.fillStyle=on?'#fff6dc':(past?'rgba(250,244,228,.92)':'rgba(250,244,228,.42)');c2.fillText(WORDS[wj].text,x,y);c2.restore();x+=ws[j]+sp});c2.restore()}
const OA=mk(1,1),OB=mk(1,1),MAINC=()=>document.getElementById('c').getContext('2d');
function camAt(it,T){const k=clamp((T-it.start)/Math.max(0.01,it.end-it.start)),f=it.cam||{},A=Object.assign({x:0,y:0,z:1,r:0},f.from||{}),B=Object.assign({},A,f.to||{}),u=f.lin?k:ease(k);return{x:lerp(A.x,B.x,u),y:lerp(A.y,B.y,u),z:lerp(A.z,B.z,u),r:lerp(A.r||0,B.r||0,u)}}
function drawShotTo(c2,it,T){if(VERT)return drawShotV(c2,it,T);ctx=c2;ctx.setTransform(SC_,0,0,SC_,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,W,H);const t=T-it.start,d=it.end-it.start;cam=camAt(it,T);
  const sw=(it.shake||1);cam.x+=(Math.sin(T*0.9)*1.6+Math.sin(T*2.3)*0.8)*sw;cam.y+=(Math.cos(T*0.7)*1.3+Math.sin(T*1.9)*0.7)*sw;cam.r+=(Math.sin(T*0.6)*0.0016)*sw+(it.tilt||0);
  SHOTS[it.draw](t,d,it,clamp(t/d));ctx.setTransform(SC_,0,0,SC_,0,0);ctx.globalAlpha=1;post(c2,T,it,CW_,CH_);ctx.setTransform(SC_,0,0,SC_,0,0)}
/* scene transitions (shot.tr): fade (default dissolve), wipe (torn paper edge sweeps left to right), iris (circle opens
   from the centre), flash (white bloom, for impact). dx = length in seconds. */
function transit(M,TR,u){if(TR!=='wipe'&&TR!=='iris'&&TR!=='flash'){M.globalAlpha=u;M.drawImage(OB,0,0);return}
  if(TR==='flash'){M.globalAlpha=u;M.drawImage(OB,0,0);M.globalAlpha=Math.max(0,1-Math.abs(u*2-1))*.85;M.fillStyle='#fff8e8';M.fillRect(0,0,CW_,CH_);return}
  const path=()=>{M.beginPath();if(TR==='iris'){M.arc(CW_/2,CH_/2,u*Math.hypot(CW_,CH_)*.55,0,7)}else{const ex=u*(CW_+260*SC_)-130*SC_;M.moveTo(-10,-10);for(let k=0;k<=24;k++){const y=k/24*CH_;M.lineTo(ex+Math.sin(k*2.7)*26*SC_+(k%2?14:-10)*SC_,y)}M.lineTo(-10,CH_+10);M.closePath()}};
  M.save();path();M.clip();M.drawImage(OB,0,0);M.restore();M.save();path();M.shadowColor='rgba(10,2,24,.6)';M.shadowBlur=14*SC_;M.lineWidth=4*SC_;M.strokeStyle='#f4ead0';M.stroke();M.restore()}
window.seek=(T)=>{let i=SHOTLIST.length-1;while(i>0&&T<SHOTLIST[i].start)i--;const sh=SHOTLIST[i],lt=T-sh.start,TR=sh.tr||'fade',DX=sh.dx??({wipe:.55,iris:.6,flash:.4}[TR]||0.28);const M=MAINC();
  if(OA.width!==CW_){OA.width=OB.width=CW_;OA.height=OB.height=CH_}
  if(i>0&&lt<DX){const u=ease(lt/DX);drawShotTo(OA.getContext('2d'),SHOTLIST[i-1],T);drawShotTo(OB.getContext('2d'),sh,T);M.setTransform(1,0,0,1,0,0);M.globalAlpha=1;M.clearRect(0,0,CW_,CH_);M.drawImage(OA,0,0);transit(M,TR,u);M.globalAlpha=1}
  else drawShotTo(M,sh,T);
  if(VERT)vOverlay(M,T,sh);else subs(M,T);const fin=VERT?0:1-clamp(T/0.8),fout=clamp((T-(TOTAL-1.0))/1.0),a2=Math.max(fin,fout);if(a2>0){M.setTransform(SC_,0,0,SC_,0,0);M.fillStyle=`rgba(0,0,0,${a2})`;M.fillRect(0,0,W,H)}};
/* ===== VERTICAL 9:16 reels (only when VERT; studio/build.py --format vertical sets VERT=true, canvas CW_xCH_ = 720x1280 * scale, SC_ = CH_/720).
   Scenes, characters and effects still draw in the 1280x720 16:9 frame (after the shot camera). The reel shows that frame through a
   portrait WINDOW (full height x 405 wide at z 1) centred on the focus figure, or a native vertical STACK of two figures.
   shot.vert = {focus:'who'|index (default: the largest figure), x: frame x or [x0,x1] pan (plan units, overrides focus), z: extra zoom 1..1.8,
                y: where the focus face sits in the window 0..1 (default .36, used when z>1), mode:'crop' (default) | 'stack',
                stack:['who','who'] (top, bottom; default the first two figures), h: stack crop height (default 330*s)}
   Title card (from reel.json via the first shot's `title`:{text,sec}) and big word-grouped subtitles are drawn in the reel safe area. */
const VWIN=405,VFONT=fs=>`700 ${fs}px NSerLat, 'Noto Serif', 'Source Serif 4', Georgia, 'Liberation Serif', 'DejaVu Serif', serif`;
function vFig(it,f){const F=((it.sc&&it.sc.figs)||[]).filter(g=>g&&g.who);if(typeof f==='number')return F[f];if(f)return F.find(g=>g.who===f)||null;let b=null;F.forEach(g=>{if(!b||(g.s||1)>(b.s||1)+1e-6)b=g});return b}
function vFigX(f,t,P){let x=f.x??640;if(f.walkTo){const W2=f.walkTo,d2=W2.d||Math.abs(W2.x-f.x)/(W2.v||120);x+=(W2.x-f.x)*clamp((t-cuT(P,W2.c||0))/Math.max(.1,d2))}if(f.mx)x+=f.mx*q(P,t,f.mc||0,f.md||1.2);return x+(f.vx||0)*t}
const vScr=(x,y)=>[W/2+(x-W/2-cam.x)*cam.z,H/2+(y-H/2-cam.y)*cam.z];
const vSeated=g=>g.pose==='sit'||g.pose==='sitpray'||(g.who==='brahma'&&g.lotus!==false&&(!g.pose||g.pose==='stand'));   /* seated rigs: face ~195*s above y, standing ~300*s */
const vFaceY=g=>g.head?(g.y??500):((g.y??500)-(vSeated(g)?195:300)*(g.s||1));
function vViews(it,T){const V=it.vert||{},t=T-it.start,d=Math.max(.01,it.end-it.start);
  if(V.mode==='stack'){const st=V.stack||[0,1],half=CH_/2,gap=Math.round(CH_*.004),out=[];
    [[vFig(it,st[0]),0,half-gap,.5],[vFig(it,st[1]),half+gap,CH_-half-gap,.3]].forEach(([g,oy,oh,ff])=>{if(!g)return;
      let h=clamp(V.h||330*(g.s||1)*cam.z,200,H),w=h*CW_/oh;if(w>W){w=W;h=w*oh/CW_}const p=vScr(vFigX(g,t,it),vFaceY(g));
      out.push({ox:0,oy,ow:CW_,oh,x0:clamp(p[0]-w/2,0,W-w),y0:clamp(p[1]-ff*h,0,H-h),w,h})});if(out.length===2)return out}
  const z=clamp(V.z||1,1,2.2),h=H/z,w=VWIN/z;let fx=W/2,fy=H*.4;const g=vFig(it,V.focus);
  if(Array.isArray(V.x))fx=vScr(lerp(V.x[0],V.x[1],ease(clamp(t/d))),0)[0];else if(typeof V.x==='number')fx=vScr(V.x,0)[0];
  else if(g)fx=vScr(vFigX(g,t,it),0)[0];
  if(g)fy=vScr(0,vFaceY(g))[1];
  return [{ox:0,oy:0,ow:CW_,oh:CH_,x0:clamp(fx-w/2,0,W-w),y0:z>1?clamp(fy-(V.y??.36)*h,0,H-h):0,w,h}]}
function drawShotV(c2,it,T){const t=T-it.start,d=it.end-it.start,SC0=SC_;let c0=camAt(it,T);
  const sw=(it.shake||1);c0.x+=(Math.sin(T*0.9)*1.6+Math.sin(T*2.3)*0.8)*sw;c0.y+=(Math.cos(T*0.7)*1.3+Math.sin(T*1.9)*0.7)*sw;c0.r+=(Math.sin(T*0.6)*0.0016)*sw+(it.tilt||0);
  cam=c0;const views=vViews(it,T);c2.setTransform(1,0,0,1,0,0);c2.globalAlpha=1;c2.clearRect(0,0,CW_,CH_);c2.fillStyle='#000';c2.fillRect(0,0,CW_,CH_);
  views.forEach(v=>{const k=v.ow/v.w;c2.save();c2.beginPath();c2.rect(v.ox,v.oy,v.ow,v.oh);c2.clip();SC_=k;cam=Object.assign({},c0);ctx=c2;
    ctx.setTransform(k,0,0,k,v.ox-v.x0*k,v.oy-v.y0*k);ctx.globalAlpha=1;try{SHOTS[it.draw](t,d,it,clamp(t/d))}finally{SC_=SC0;c2.restore()}});
  cam=c0;ctx=c2;c2.setTransform(1,0,0,1,0,0);c2.globalAlpha=1;post(c2,T,it,CW_,CH_);
  if(views.length===2){const u=CW_/720,y=views[1].oy-Math.round(CH_*.004);c2.save();c2.setTransform(u,0,0,u,0,0);const Y=y/u;c2.beginPath();c2.moveTo(-5,Y-7);
    for(let i=0;i<=36;i++)c2.lineTo(i*20,Y-7+Math.sin(i*2.3)*3.5+(i%2?2:-2));for(let i=36;i>=0;i--)c2.lineTo(i*20,Y+7+Math.sin(i*1.7)*3.5+(i%2?-2:2));c2.closePath();
    c2.shadowColor='rgba(10,2,24,.7)';c2.shadowBlur=12;c2.fillStyle='#f1e4c4';c2.fill();c2.restore()}
  ctx.setTransform(SC_,0,0,SC_,0,0)}
/* word groups for reels: the same rule as studio/reel_prepare.py cues() (max 6 words, 36 chars, 3.2 s, break on a 0.45 s gap and at . ? !, or , ; : after 3 words) */
let VG=null;const VGOF=[];
function vGroups(){const G=[];let cur=[];const flush=()=>{if(cur.length){G.push(cur);cur=[]}};
  WORDS.forEach((w,i)=>{if(w.hide)return;if(cur.length){const p=WORDS[cur[cur.length-1]],f=WORDS[cur[0]],txt=cur.map(j=>WORDS[j].text).concat(w.text).join(' ');
    if(cur.length>=6||txt.length>36||w.end-f.start>3.2||w.start-p.end>0.45||w.beat!==p.beat)flush()}
    cur.push(i);if(/[.?!]["”]?$/.test(w.text)||(/[,;:]$/.test(w.text)&&cur.length>=3))flush()});flush();G.forEach((g,k)=>g.forEach(i=>VGOF[i]=k));return G}
function vLines(c2,ids,maxW){const sp=c2.measureText(' ').width,ws=ids.map(i=>c2.measureText(WORDS[i].text).width),wid=(a,b)=>ws.slice(a,b).reduce((s,x)=>s+x,0)+sp*Math.max(0,b-a-1);
  if(wid(0,ids.length)<=maxW||ids.length<2)return{L:[[0,ids.length]],ws,sp,mw:wid(0,ids.length)};let best=null;
  for(let k=1;k<ids.length;k++){const m=Math.max(wid(0,k),wid(k,ids.length));if(!best||m<best.mw)best={L:[[0,k],[k,ids.length]],mw:m}}return Object.assign(best,{ws,sp})}
function vSubs(M,T,sh){if(!VG)VG=vGroups();let wi=-1;for(let i=0;i<WORDS.length;i++){if(WORDS[i].hide)continue;if(WORDS[i].start<=T+0.03)wi=i;else break}
  if(wi<0||T-WORDS[wi].end>0.5)return;const g=VG[VGOF[wi]],u=CW_/720,stack=sh&&sh.vert&&sh.vert.mode==='stack',cx=344,cy=stack?640:900,maxW=560;
  M.save();M.setTransform(u,0,0,u,0,0);let fs=64;M.font=VFONT(fs);let L=vLines(M,g,maxW);if(L.mw>maxW){fs=Math.floor(fs*maxW/L.mw);M.font=VFONT(fs);L=vLines(M,g,maxW)}
  const lh=fs*1.2,n=L.L.length,y0=cy-(n-1)*lh/2;M.fillStyle='rgba(8,4,2,.42)';M.beginPath();M.roundRect(cx-L.mw/2-24,y0-lh/2-10,L.mw+48,n*lh+20,18);M.fill();
  M.textBaseline='middle';M.textAlign='left';M.lineJoin='round';
  L.L.forEach(([a,b],r)=>{const lw=L.ws.slice(a,b).reduce((s,x)=>s+x,0)+L.sp*(b-a-1);let x=cx-lw/2;const y=y0+r*lh;
    for(let j=a;j<b;j++){const id=g[j],on=id===wi;M.save();M.lineWidth=fs*.16;M.strokeStyle='rgba(14,6,2,.95)';M.strokeText(WORDS[id].text,x,y);M.shadowColor='rgba(0,0,0,.8)';M.shadowBlur=8;M.shadowOffsetY=3;
      M.fillStyle=on?'#ffd23f':'#fffaf0';M.fillText(WORDS[id].text,x,y);M.restore();x+=L.ws[j]+L.sp}});M.restore()}
/* first-frame title card: fully visible from frame 0 (thumbnail), upper safe area (14-30% of height), fades out after `sec` */
function vTitle(M,T){const tc=SHOTLIST[0]&&SHOTLIST[0].title;if(!tc||!tc.text)return;const sec=tc.sec||2.5,a=1-clamp((T-sec)/0.5);if(a<=0)return;const u=CW_/720;
  M.save();M.setTransform(u,0,0,u,0,0);M.globalAlpha=a;const sc=1+0.035*clamp(T/sec);
  let fs=tc.size||92;M.font=VFONT(fs);const words=String(tc.text).split(/\s+/);const lay=()=>{const sp=M.measureText(' ').width,w=words.map(x=>M.measureText(x).width);let best=null;
    for(let k=1;k<=words.length;k++){const l1=w.slice(0,k).reduce((s,x)=>s+x,0)+sp*(k-1),l2=k<words.length?w.slice(k).reduce((s,x)=>s+x,0)+sp*(words.length-k-1):0,m=Math.max(l1,l2);if(!best||m<best.m-1)best={k,m}}return best};
  let b=lay();if(b.m>600){fs=Math.floor(fs*600/b.m);M.font=VFONT(fs);b=lay()}
  const lines=[words.slice(0,b.k).join(' '),words.slice(b.k).join(' ')].filter(Boolean),lh=fs*1.08,bh=lines.length*lh+56,bw=Math.min(700,b.m+90);
  const cy=Math.max(300,190+bh*sc/2)-14*(1-a);M.translate(360,cy);M.scale(sc,sc);M.rotate(-0.022);   /* top edge stays below 14% of the height (platform UI) */
  const r=rng(7);M.beginPath();M.moveTo(-bw/2,-bh/2);for(let i=1;i<=20;i++)M.lineTo(-bw/2+bw*i/20,-bh/2+(r()-.5)*9);for(let i=1;i<=6;i++)M.lineTo(bw/2+(r()-.5)*9,-bh/2+bh*i/6);
  for(let i=19;i>=0;i--)M.lineTo(-bw/2+bw*i/20,bh/2+(r()-.5)*9);for(let i=5;i>=1;i--)M.lineTo(-bw/2+(r()-.5)*9,-bh/2+bh*i/6);M.closePath();
  M.save();M.shadowColor='rgba(10,2,4,.75)';M.shadowBlur=22;M.shadowOffsetY=8;const gr=M.createLinearGradient(0,-bh/2,0,bh/2);gr.addColorStop(0,'#8a2414');gr.addColorStop(1,'#5a120c');M.fillStyle=gr;M.fill();M.restore();
  M.lineWidth=4;M.strokeStyle='#f1d89a';M.stroke();M.textAlign='center';M.textBaseline='middle';M.lineJoin='round';
  lines.forEach((s,i)=>{const y=(i-(lines.length-1)/2)*lh+fs*.04;M.lineWidth=fs*.14;M.strokeStyle='rgba(30,6,2,.95)';M.strokeText(s,0,y);M.fillStyle='#ffe9a8';M.shadowColor='rgba(255,190,90,.55)';M.shadowBlur=16;M.fillText(s,0,y);M.shadowBlur=0});
  M.restore()}
function vOverlay(M,T,sh){vSubs(M,T,sh);vTitle(M,T)}
