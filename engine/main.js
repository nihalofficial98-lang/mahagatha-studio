/* ===== v4 timeline: shots start on spoken words, dissolves, serif subtitles, camera ===== */
const SHOTS={};let LAT=false;/* LAT = English subtitles: Latin-first font stack, groups up to 42 chars (Hindi: 30) */
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
function drawShotTo(c2,it,T){ctx=c2;ctx.setTransform(SC_,0,0,SC_,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,W,H);const t=T-it.start,d=it.end-it.start;cam=camAt(it,T);
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
  subs(M,T);const fin=1-clamp(T/0.8),fout=clamp((T-(TOTAL-1.0))/1.0),a2=Math.max(fin,fout);if(a2>0){M.setTransform(SC_,0,0,SC_,0,0);M.fillStyle=`rgba(0,0,0,${a2})`;M.fillRect(0,0,W,H)}};
