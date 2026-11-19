"""Assemble engine/engine.html from the base engine (hindi-video prototype), episode scenes and new main loop."""
import re, os, sys
SCALE=float(os.environ.get("SCALE","1.5")); OFFS=int(os.environ.get("OFFS","2")); OUT=os.environ.get("OUT","engine.html")
CW=int(1280*SCALE); CH=int(720*SCALE)
base = open('/home/user/story-videos/engine/base_engine.html').read()
s = base.replace('node_modules/@fontsource/noto-sans-devanagari/files/','fonts/')
def rep(a,b):
    global s
    assert a in s, 'PATCH MISS: '+a[:80]
    s = s.replace(a,b,1)
s = s.replace('<canvas id="c" width="1280" height="720">', '<canvas id="c" width="%d" height="%d">'%(CW,CH))
s = s.replace("const W=1280,H=720,cv=document.getElementById('c'),ctx=cv.getContext('2d');", "const W=1280,H=720,SC_=%s,cv=document.getElementById('c');let ctx=cv.getContext('2d');" % SCALE)
s = s.replace("off.width=760;off.height=760;", "off.width=%d;off.height=%d;" % (760*OFFS, 760*OFFS))
s = s.replace("c.setTransform(1,0,0,1,0,0);c.clearRect(0,0,760,760);c.save();c.translate(380,700);", "c.setTransform(%d,0,0,%d,0,0);c.clearRect(0,0,760,760);c.save();c.translate(380,700);" % (OFFS, OFFS))
rep("c.fillStyle=P.skinD;c.fillRect(-12,-36,10,34);c.fillRect(2,-36,10,34);c.fillStyle='#4a2a22';c.beginPath();c.ellipse(-5,-1,11,4,0,0,7);c.ellipse(9,-1,11,4,0,0,7);c.fill();",
 "const wk=o.walk||0,ws=o.walkSpeed||7;c.fillStyle=P.skinD;[-1,1].forEach(sd=>{const an=Math.sin(t*ws+(sd>0?Math.PI:0))*0.55*wk;c.save();c.translate(sd*7,-36);c.rotate(an);c.fillStyle=P.skinD;c.fillRect(-5,0,10,34);c.fillStyle='#4a2a22';c.beginPath();c.ellipse(sd*-1+2,35,11,4,0,0,7);c.fill();c.restore()});")
s = s.replace("ctx.drawImage(off,-380,-700);", "ctx.drawImage(off,-380,-700,760,760);")
deco = r'''
  if(P.horns){c.fillStyle='#ece3c6';[[-1,-9],[1,7]].forEach(([sd,x0])=>{c.beginPath();c.moveTo(x0-3,-182+hb);c.quadraticCurveTo(x0+sd*8,-200+hb,x0+sd*3+sd*7,-214+hb);c.quadraticCurveTo(x0+sd*2,-198+hb,x0+4,-183+hb);c.fill()})}
  if(P.fangs){c.fillStyle='#fff';c.beginPath();c.moveTo(6,-156+hb);c.lineTo(7.6,-151+hb);c.lineTo(9,-156+hb);c.moveTo(10,-156.5+hb);c.lineTo(11.4,-151.5+hb);c.lineTo(12.8,-156.5+hb);c.fill()}
  if(P.antennae){c.strokeStyle=P.skinD;c.lineWidth=2.4;c.lineCap='round';c.beginPath();c.moveTo(-2,-183+hb);c.quadraticCurveTo(-4,-208+hb,10,-214+hb);c.moveTo(4,-183+hb);c.quadraticCurveTo(10,-208+hb,24,-208+hb);c.stroke();c.fillStyle=P.skinD;c.beginPath();c.arc(10,-214+hb,2.4,0,7);c.arc(24,-208+hb,2.4,0,7);c.fill()}
  if(P.jata){c.fillStyle=P.hair;for(let i=0;i<7;i++){const a0=-0.9+i*0.3,hh=34+(i%3)*12+Math.sin(t*3+i)*3;c.beginPath();c.moveTo(-10+i*3.4,-186+hb);c.quadraticCurveTo(-14+i*5+Math.cos(a0)*6,-186-hh*0.6+hb,-18+i*6+Math.sin(a0)*14,-186-hh+hb);c.quadraticCurveTo(-4+i*3,-186-hh*0.4+hb,4+i*3.4,-186+hb);c.fill()}c.fillStyle='#e8eef8';c.beginPath();c.arc(-2,-218+hb,8,0.6,5.7);c.arc(1,-218+hb,6.5,5.5,0.8,true);c.fill()}
  if(P.flame){for(let i=0;i<6;i++){c.fillStyle=i%2?'#ff7a1a':'#ffd23a';c.beginPath();const bx=-12+i*5;c.moveTo(bx-4,-184+hb);c.quadraticCurveTo(bx-6+Math.sin(t*8+i)*3,-200+hb,bx+Math.sin(t*7+i)*4,-214-(i%3)*6+hb);c.quadraticCurveTo(bx+6,-198+hb,bx+4,-184+hb);c.fill()}}
  if(P.horse){const jw=clamp(op,0,1)*5;
    c.fillStyle='#3a2a22';c.beginPath();c.moveTo(-10,-186+hb);c.quadraticCurveTo(-26+Math.sin(t*2.2)*3,-170+hb,-24+Math.sin(t*2.6)*4,-140+hb);c.lineTo(-6,-146+hb);c.fill();
    c.fillStyle='#efe9dc';c.beginPath();c.moveTo(-9,-186+hb);c.lineTo(-8,-204+hb);c.lineTo(0,-188+hb);c.quadraticCurveTo(16,-184+hb,28,-172+hb);c.quadraticCurveTo(46,-160+hb,45,-150+hb);c.quadraticCurveTo(44,-144+hb+jw,32,-143+hb+jw);c.quadraticCurveTo(14,-146+hb,4,-150+hb);c.lineTo(-9,-146+hb);c.closePath();c.fill();
    c.fillStyle='#d8cfc0';c.beginPath();c.ellipse(41,-152+hb,2.6,1.8,0.3,0,7);c.fill();c.fillStyle='#fffdf6';c.beginPath();c.ellipse(13,-172+hb,4.2,3*eyeH,0,0,7);c.fill();c.fillStyle='#1a1010';c.beginPath();c.arc(14.2,-172+hb,2,0,7);c.fill();
    c.strokeStyle='#3a2a22';c.lineWidth=2.4;c.beginPath();c.moveTo(7,-178+hb-k*3);c.lineTo(20,-177+hb+k*3);c.stroke()}
'''
marker = "if(P.jew){c.fillStyle=GOLD;c.beginPath();c.arc(-1,-161+hb,2.2,0,7);c.fill()}\n  c.restore();c.restore();c.restore();"
assert marker in s
s = s.replace(marker, "if(P.jew){c.fillStyle=GOLD;c.beginPath();c.arc(-1,-161+hb,2.2,0,7);c.fill()}\n"+deco+"  c.restore();c.restore();c.restore();")

rep("const br=Math.sin(t*2.1)*1.3,sw=Math.sin(t*1.7),fl=Math.sin(t*3.1);","const br=Math.sin(t*2.1)*1.3,sw=Math.sin(t*1.7),fl=Math.sin(t*3.1);if(o.walk){c.translate(0,-Math.abs(Math.sin(t*(o.walkSpeed||7)))*3*o.walk)}")
props = r'''
  if(P.trident){const hx=e1[2][0],hy=e1[2][1];c.save();c.shadowOffsetX=0;c.strokeStyle='#d9a441';c.lineWidth=5;c.lineCap='round';c.beginPath();c.moveTo(hx,hy+72);c.lineTo(hx,hy-96);c.stroke();c.beginPath();c.moveTo(hx-17,hy-132);c.lineTo(hx-17,hy-100);c.quadraticCurveTo(hx,hy-84,hx+17,hy-100);c.lineTo(hx+17,hy-132);c.moveTo(hx,hy-96);c.lineTo(hx,hy-142);c.stroke();c.fillStyle='#e8d9a0';[[-17,-132],[0,-142],[17,-132]].forEach(([dx,dy])=>{c.beginPath();c.moveTo(hx+dx-4.5,hy+dy);c.lineTo(hx+dx,hy+dy-14);c.lineTo(hx+dx+4.5,hy+dy);c.fill()});c.restore()}
  if(P.veena){c.save();c.shadowOffsetX=0;c.translate(-4,-116);c.rotate(-0.9);c.strokeStyle='#7a4a22';c.lineWidth=5;c.beginPath();c.moveTo(-70,0);c.lineTo(78,0);c.stroke();c.fillStyle='#b8742e';c.beginPath();c.ellipse(-70,0,20,15,0,0,7);c.ellipse(70,0,16,13,0,0,7);c.fill();c.strokeStyle='#efe4cd';c.lineWidth=1.2;[-3,0,3].forEach(yy=>{c.beginPath();c.moveTo(-60,yy);c.lineTo(66,yy);c.stroke()});c.restore()}
'''
rep("  if(P.jew){c.fillStyle=GOLD;c.beginPath();c.arc(lerp(S1[0],e1[0],0.55)", props+"  if(P.jew){c.fillStyle=GOLD;c.beginPath();c.arc(lerp(S1[0],e1[0],0.55)")
rep("c.fillStyle='#1a1010';c.beginPath();c.ellipse(ex1+0.6,","c.fillStyle=(P.eyeGlow?'#ff2a1a':'#1a1010');c.beginPath();c.ellipse(ex1+0.6,")
rep("c.ellipse(5.8,-168+hb,3.8,2.5*eyeH,0,Math.PI*1.05,Math.PI*1.95);c.stroke();","c.ellipse(5.8,-168+hb,3.8,2.5*eyeH,0,Math.PI*1.05,Math.PI*1.95);c.stroke();if(P.eyeGlow){const gg=c.createRadialGradient(6,-168+hb,0,6,-168+hb,24);gg.addColorStop(0,'rgba(255,60,30,.75)');gg.addColorStop(1,'rgba(255,60,30,0)');c.fillStyle=gg;c.fillRect(-20,-196+hb,52,56)}if(P.third){c.fillStyle='#d62a1a';c.beginPath();c.ellipse(8,-181+hb,1.9,5.2,0,0,7);c.fill()}")

a = s.index('/* ---------- subtitles ---------- */')
s = s[:a]
s += open('/home/user/story-videos/engine/ep_scenes.js').read()
import os as _os
s += open('/home/user/story-videos/engine/post.js').read()
if _os.path.exists('/home/user/story-videos/engine/ep02_shots.js'): s += open('/home/user/story-videos/engine/ep02_head.js').read() + open('/home/user/story-videos/engine/ep02_shots.js').read()
s += r'''
/* ---------- timeline / subtitles / render ---------- */
let SHOTLIST=[],WORDS=[],GROUPOF=[],GROUPS=[],TOTAL=0;
window.init=(shots,beats)=>{const bs={};let a=0;beats.forEach(b=>{bs[b.beat]={start:a,dur:b.duration};b.words.forEach(w=>WORDS.push({text:w.text,start:a+w.start,end:a+w.end,beat:b.beat}));a+=b.duration});TOTAL=a;window.total=a;

  const norm=x=>x.replace(/[।,.!?…"'“”‘’\-–—:;()‌‍]/g,'').trim();window.CUEMISS=[];window.CUELOG={};
  function resolveCues(sh,pStart){if(!sh.cues)return;const bw=WORDS.filter(w=>sh.beats.includes(w.beat));let from=0;const out=[];
    sh.cues.forEach(ph=>{const toks=ph.split(/\s+/).map(norm);let found=-1;for(let i=from;i<bw.length&&found<0;i++){let ok=true;for(let j=0;j<toks.length;j++){const w=bw[i+j];if(!w){ok=false;break}const wt=norm(w.text);if(!(wt.startsWith(toks[j])||toks[j].startsWith(wt))){ok=false;break}}if(ok)found=i}
      if(found<0){out.push(null);window.CUEMISS.push([sh.shot,ph])}else{out.push(bw[found].start-pStart);from=found+1}});
    for(let i=0;i<out.length;i++)if(out[i]==null)out[i]=i>0?out[i-1]+0.8:0.4;sh.cueT=out;window.CUELOG[sh.shot+'@'+sh.beats[0]]=out.map(v=>+v.toFixed(2))}
  shots.forEach(sh=>{const f=bs[sh.beats[0]],l=bs[sh.beats[sh.beats.length-1]],ps=f.start,pe=l.start+l.dur,span=pe-ps,cuts=(sh.cuts&&sh.cuts.length)?sh.cuts:[{to:1}];resolveCues(sh,ps);let prev=0;
    cuts.forEach((c,ci)=>{SHOTLIST.push({shot:c.shot||sh.shot,insert:!!c.shot,start:ps+prev*span,end:ps+c.to*span,pStart:ps,pEnd:pe,first:ci===0,focus:c.focus,params:Object.assign({},sh,c)});prev=c.to})});
  (function(){const MAXC=4.0,out=[];SHOTLIST.forEach((it,ix)=>{const d=it.end-it.start;if(!(it.params&&it.params.cine)){out.push(it);return}
    const f=it.focus||{z:[1,1.07],c:[[640+(ix%2?-30:30),360],[640+(ix%2?30:-30),360]]};
    if(it.params.nosplit||d<=MAXC*1.3){out.push(Object.assign({},it,{focus:f}));return}
    const n=Math.max(2,Math.round(d/MAXC)),mk=u=>({z:lerp(f.z[0],f.z[1],u),x:lerp(f.c[0][0],f.c[1][0],u),y:lerp(f.c[0][1],f.c[1][1],u)});
    for(let j=0;j<n;j++){const A=mk(j/n),B=mk((j+1)/n),pn=(j%2===1)?1.3:1.0,dr=(j%2===0)?1.06:1.03;
      out.push(Object.assign({},it,{start:it.start+d*j/n,end:it.start+d*(j+1)/n,first:it.first&&j===0,focus:{z:[A.z*pn,B.z*pn*dr],c:[[A.x,A.y],[B.x,B.y]]}}))}});SHOTLIST=out})();
  let cur=[];WORDS.forEach((w,i)=>{const p=WORDS[i-1];if(cur.length&&(w.beat!==p.beat||w.start-p.end>0.25||cur.reduce((n,j)=>n+WORDS[j].text.length+1,0)+w.text.length>34)){GROUPS.push(cur);cur=[]}cur.push(i);GROUPOF[i]=GROUPS.length});if(cur.length)GROUPS.push(cur);
  return document.fonts.load('700 40px NDev','अ').then(()=>document.fonts.ready)};
function subs2(T){let wi=-1;for(let i=0;i<WORDS.length;i++){if(WORDS[i].start<=T+0.03)wi=i;else break}if(wi<0||T-WORDS[wi].end>0.45)return;const g=GROUPS[GROUPOF[wi]];
  let fs=40;ctx.font=`700 ${fs}px NDev, sans-serif`;let sp=ctx.measureText(' ').width+5,tot=0,ws=[];const meas=()=>{tot=0;ws=g.map(i=>{const m=ctx.measureText(WORDS[i].text).width;tot+=m+sp;return m});tot-=sp};meas();
  if(tot>W-140){fs=Math.floor(fs*(W-140)/tot);ctx.font=`700 ${fs}px NDev, sans-serif`;sp=ctx.measureText(' ').width+5;meas()}
  const gr=ctx.createLinearGradient(0,H-185,0,H);gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(0,0,0,0.72)');ctx.fillStyle=gr;ctx.fillRect(0,H-185,W,185);
  let x=(W-tot)/2;const y=H-56;ctx.textBaseline='alphabetic';ctx.textAlign='left';
  g.forEach((wj,j)=>{const on=wj===wi,past=wj<wi;ctx.save();ctx.shadowColor='rgba(0,0,0,.95)';ctx.shadowBlur=9;ctx.shadowOffsetY=2;ctx.fillStyle=on?'#ffd27a':(past?'#f7eddb':'rgba(247,237,219,0.55)');ctx.fillText(WORDS[wj].text,x,y);ctx.restore();x+=ws[j]+sp})}
const CW_=%d,CH_=%d;
const OA=document.createElement('canvas'),OB=document.createElement('canvas');[OA,OB].forEach(c=>{c.width=CW_;c.height=CH_});
const MAIN=cv.getContext('2d');
function drawShotTo(c2,it,T){ctx=c2;ctx.setTransform(SC_,0,0,SC_,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,W,H);cam={x:0,y:0,z:1};
  const t=it.insert?T-it.start:T-it.pStart,d=it.insert?it.end-it.start:it.pEnd-it.pStart,P=it.params||{},cine=!!P.cine;if(cine)txtQ([]);else txtQ(null);
  ctx.save();if(cine){const sw=sway(T,P);ctx.translate(W/2+sw.sx,H/2+sw.sy);ctx.rotate(sw.rot);ctx.scale(1.03,1.03);ctx.translate(-W/2,-H/2)}
  if(it.focus){const u=clamp((T-it.start)/Math.max(0.01,it.end-it.start)),f=it.focus,z=lerp(f.z[0],f.z[1],u),cx0=lerp(f.c[0][0],f.c[1][0],u),cy0=lerp(f.c[0][1],f.c[1][1],u),cx=clamp(cx0,W/(2*z),W-W/(2*z)),cy=clamp(cy0,H/(2*z),H-H/(2*z));it._subj={x:(W/2+(cx0-cx)*z)*SC_,y:(H/2+(cy0-cy)*z)*SC_};
    ctx.save();ctx.translate(W/2,H/2);ctx.scale(z,z);ctx.translate(-cx,-cy);SHOTS[it.shot](t,d,it.params);ctx.restore()}
  else SHOTS[it.shot](t,d,it.params);
  ctx.restore();ctx.setTransform(SC_,0,0,SC_,0,0);ctx.globalAlpha=1;vignette();if(cine){postFX(c2,T,it);const q=TXQ;txtQ(null);flushText(c2,P,q)}ctx.setTransform(SC_,0,0,SC_,0,0)}
window.seek=(T)=>{let i=SHOTLIST.length-1;while(i>0&&T<SHOTLIST[i].start)i--;const sh=SHOTLIST[i],lt=T-sh.start,DX=sh.first?0.6:0.14;
  if(i>0&&lt<DX){const u=ease(lt/DX),pr=SHOTLIST[i-1];const a=OA.getContext('2d'),b=OB.getContext('2d');drawShotTo(a,pr,T);drawShotTo(b,sh,T);
    ctx=MAIN;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,CW_,CH_);ctx.drawImage(OA,0,0);ctx.globalAlpha=u;ctx.drawImage(OB,0,0);ctx.globalAlpha=1}
  else drawShotTo(MAIN,sh,T);
  ctx=MAIN;ctx.setTransform(SC_,0,0,SC_,0,0);subs2(T);
  const fin=1-clamp(T/0.9),fout=clamp((T-(TOTAL-1.2))/1.2),a2=Math.max(fin,fout);if(a2>0){ctx.fillStyle=`rgba(0,0,0,${a2})`;ctx.fillRect(0,0,W,H)}};
</script></body></html>
'''
s=s.replace('const CW_=%d,CH_=%d;','const CW_=%d,CH_=%d;'%(CW,CH))
open('/home/user/story-videos/engine/'+OUT,'w').write(s)
print('engine.html', len(s))
