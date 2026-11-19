/* ===== cinematic post-processing + always-moving camera ===== */
const NOISE=[];(function(){for(let i=0;i<4;i++){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d'),d=x.createImageData(256,256),r=rng(900+i);for(let p=0;p<d.data.length;p+=4){const v=r()*255;d.data[p]=d.data[p+1]=d.data[p+2]=v;d.data[p+3]=255}x.putImageData(d,0,0);NOISE.push(c)}})();
const DOFC=document.createElement('canvas'),BLOOMC=document.createElement('canvas');
function postFX(c2,T,it){const P=it.params||{};const cw=CW_,ch=CH_;const f=it.focus,zoom=f?Math.max(f.z[0],f.z[1]):1;const sj=it._subj||{x:cw/2,y:ch/2};
  // pseudo depth-of-field: blurred copy masked toward the edges, stronger on close-ups
  if(P.dof!==false&&zoom>=1.45){DOFC.width=cw;DOFC.height=ch;const d=DOFC.getContext('2d');d.setTransform(1,0,0,1,0,0);d.clearRect(0,0,cw,ch);d.filter=`blur(${Math.round(ch/160)}px)`;d.drawImage(c2.canvas,0,0);d.filter='none';
    d.globalCompositeOperation='destination-in';const g=d.createRadialGradient(sj.x,sj.y,ch*0.42,sj.x,sj.y,ch*0.95);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,0.85)');d.fillStyle=g;d.fillRect(0,0,cw,ch);d.globalCompositeOperation='source-over';
    c2.setTransform(1,0,0,1,0,0);c2.drawImage(DOFC,0,0);c2.setTransform(SC_,0,0,SC_,0,0)}
  // bloom (cheap: downsample, upscale additively)
  const bw=Math.round(cw/10),bh=Math.round(ch/10);BLOOMC.width=bw;BLOOMC.height=bh;const b=BLOOMC.getContext('2d');b.filter='brightness(1.1) contrast(1.5)';b.drawImage(c2.canvas,0,0,bw,bh);b.filter='none';
  c2.save();c2.setTransform(1,0,0,1,0,0);c2.globalCompositeOperation='lighter';c2.globalAlpha=P.bloom??0.12;c2.imageSmoothingEnabled=true;c2.drawImage(BLOOMC,0,0,cw,ch);c2.restore();
  // colour grade
  if(P.grade){c2.save();c2.setTransform(1,0,0,1,0,0);c2.globalCompositeOperation=P.gradeMode||'soft-light';c2.fillStyle=P.grade;c2.fillRect(0,0,cw,ch);c2.restore()}
  // film grain
  c2.save();c2.setTransform(1,0,0,1,0,0);c2.globalCompositeOperation='overlay';c2.globalAlpha=0.04;const pat=c2.createPattern(NOISE[Math.floor(T*24)%4],'repeat');c2.fillStyle=pat;c2.translate(-(Math.floor(T*60)%97),-(Math.floor(T*47)%89));c2.fillRect(0,0,cw+120,ch+120);c2.restore();
  // letterbox
  if(P.letterbox){const bh2=(H-W/2.39)/2*SC_;c2.save();c2.setTransform(1,0,0,1,0,0);c2.fillStyle='#000';c2.fillRect(0,0,cw,bh2);c2.fillRect(0,ch-bh2,cw,bh2);c2.restore()}
}
/* handheld sway: always a little motion, more when tense */
function sway(T,P){const a={still:0.35,calm:1,tense:2.6,violent:7}[P.shake||'calm'];const sx=(Math.sin(T*0.9)*2.2+Math.sin(T*2.3)*1.2)*a,sy=(Math.cos(T*0.7)*1.8+Math.sin(T*1.9)*1.0)*a,rot=(Math.sin(T*0.6)*0.0022+Math.sin(T*1.7)*0.0012)*a+(P.tilt||0);return {sx,sy,rot}}

/* ===== safe-area overlay text: never zoomed, fitted and clamped inside the frame ===== */
function flushText(c2,P,q){if(!q||!q.length)return;c2.save();c2.setTransform(SC_,0,0,SC_,0,0);c2.textBaseline='middle';
  const lb=P.letterbox?(H-W/2.39)/2:0,top=40+lb,bot=H-(lb?lb+28:125),mx=70;
  q.forEach(it=>{const m=it.m;let px=(m.a*it.x+m.c*it.y+m.e)/SC_,py=(m.b*it.x+m.d*it.y+m.f)/SC_;if(it.a<=0.01||px<-60||px>W+60||py<-60||py>H+60)return;
    let size=it.size;const pad=it.k==='tag'?44:0;c2.font=`${it.w||700} ${size}px NDev, sans-serif`;let tw=c2.measureText(it.s).width+pad;
    if(tw>W-2*mx){size*=(W-2*mx)/tw;c2.font=`${it.w||700} ${size}px NDev, sans-serif`;tw=c2.measureText(it.s).width+pad}
    const al=it.al||'center',lx=al==='center'?clamp(px,mx+tw/2,W-mx-tw/2):(al==='left'?clamp(px,mx,W-mx-tw):clamp(px,mx+tw,W-mx));
    const ly=clamp(py,top+size*0.7,bot-size*0.7);c2.save();c2.globalAlpha=clamp(it.a);
    if(it.k==='tag'){const r=size*0.62,h=size*1.25;c2.fillStyle='rgba(8,6,20,.66)';c2.beginPath();c2.moveTo(lx-tw/2+r,ly-h/2);c2.lineTo(lx+tw/2-r,ly-h/2);c2.arc(lx+tw/2-r,ly,h/2,-1.5708,1.5708);c2.lineTo(lx-tw/2+r,ly+h/2);c2.arc(lx-tw/2+r,ly,h/2,1.5708,4.7124);c2.fill();c2.strokeStyle='rgba(255,226,160,.35)';c2.lineWidth=1.5;c2.stroke()}
    c2.shadowColor='rgba(0,0,0,.8)';c2.shadowBlur=12;c2.fillStyle=it.col;c2.textAlign=it.k==='tag'?'center':(al==='center'?'center':(al==='left'?'left':'right'));
    const tx=it.k==='tag'?lx:(al==='center'?lx:(al==='left'?lx:lx));c2.fillText(it.s,tx,ly);c2.restore()});c2.restore()}
