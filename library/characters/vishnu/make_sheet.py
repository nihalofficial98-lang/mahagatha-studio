"""Builds library/characters/vishnu/sheet.html from the shared v2 rig (shiva_v2.js + engine/v2_cast.js)."""
import os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
rd=lambda *p:open(os.path.join(R,*p),encoding='utf-8').read()
core=rd('library','characters','shiva','shiva_v2.js');cast=rd('engine','v2_cast.js')
stubs="const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));let ctx=null,SC_=1,OY=0;function figBegin(){}function figFinish(){}function lotus(){}\n"
js=stubs+"const V2=(function(){"+core+"\n"+cast+"\n})();\n"
page=r'''<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:NSer;font-weight:600;src:url('../../../node_modules/@fontsource/noto-serif-devanagari/files/noto-serif-devanagari-devanagari-600-normal.woff2')}
@font-face{font-family:NSer;font-weight:400;src:url('../../../node_modules/@fontsource/noto-serif-devanagari/files/noto-serif-devanagari-devanagari-400-normal.woff2')}
body{margin:0;background:#15120f}canvas{display:block}</style><canvas id=cv width=2400 height=1500></canvas><script>
__JS__
const X=document.getElementById('cv').getContext('2d');
function figure(draw,w,h,ox,oy,rim='rgba(255,236,200,.95)',key='255,200,130'){const F=document.createElement('canvas');F.width=w;F.height=h;const c=F.getContext('2d');c.translate(ox,oy);draw(c);
  c.setTransform(1,0,0,1,0,0);c.globalCompositeOperation='source-atop';let g=c.createLinearGradient(0,0,w,0);g.addColorStop(0,`rgba(${key},.30)`);g.addColorStop(.55,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(6,8,30,.38)');c.fillStyle=g;c.fillRect(0,0,w,h);c.globalCompositeOperation='source-over';
  const S=document.createElement('canvas');S.width=w;S.height=h;const s=S.getContext('2d');s.drawImage(F,0,0);s.globalCompositeOperation='source-in';s.fillStyle=rim;s.fillRect(0,0,w,h);
  const O=document.createElement('canvas');O.width=w;O.height=h;const o=O.getContext('2d');for(let k=0;k<8;k++)o.drawImage(S,Math.cos(k*.785)*2.4,Math.sin(k*.785)*2.4);o.drawImage(F,0,0);return O}
function txt(s,x,y,size,col='#f4e6c8',al='left',w=600){X.font=`${w} ${size}px NSer, serif`;X.fillStyle=col;X.textAlign=al;X.fillText(s,x,y)}
function lab(px,py,y,label,sub,ox,oy,S,n){const x1=ox+px*S,y1=oy+py*S;X.fillStyle='#ffdc96';X.beginPath();X.arc(x1,y1,16,0,7);X.fill();txt(String(n),x1,y1+7,20,'#241a0c','center');X.fillStyle='#ffdc96';X.beginPath();X.arc(88,y+2,17,0,7);X.fill();txt(String(n),88,y+9,20,'#241a0c','center');txt(label,120,y+8,30,'#ffe9b8');if(sub)txt(sub,120,y+38,22,'#c9b894','left',400)}
function go(){
  const g=X.createLinearGradient(0,0,0,1500);g.addColorStop(0,'#1c2a3a');g.addColorStop(.6,'#2a2a2c');g.addColorStop(1,'#14100c');X.fillStyle=g;X.fillRect(0,0,2400,1500);
  let r=X.createRadialGradient(760,560,40,760,640,900);r.addColorStop(0,'rgba(120,170,255,.18)');r.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=r;X.fillRect(0,0,2400,1500);
  X.fillStyle='rgba(255,240,210,.05)';X.fillRect(1560,70,800,1380);X.strokeStyle='rgba(255,220,160,.25)';X.lineWidth=2;X.strokeRect(1560,70,800,1380);
  X.strokeStyle='rgba(255,220,160,.2)';X.lineWidth=2;X.beginPath();X.moveTo(60,1265);X.lineTo(1530,1265);X.stroke();
  txt('विष्णु — चरित्र संदर्भ (v2 मसौदा)',70,110,64,'#ffe9b8');txt('Vishnu · character reference · Mahagatha Studio',72,156,28,'#c9b894','left',400);
  const S=1.22,ox=700,oy=1265,C=V2.CAST;
  const A=figure(c=>{c.scale(S,S);V2.drawHuman(c,C.vishnu,V2.poseOf('stand','vishnu'),{t:1.2,expr:'calm'})},900,1000,450,920);X.drawImage(A,ox-450,oy-920);
  const B=figure(c=>{c.scale(S,S);V2.drawHuman(c,C.hayagriva,V2.poseOf('stand','hayagriva'),{t:1.2,expr:'calm',k:.4})},900,1000,450,920,'rgba(255,220,170,.95)','255,210,130');X.drawImage(B,1230-450,oy-920);
  txt('सामान्य रूप',ox,1335,38,'#ffe9b8','center');txt('calm · preserver · default',ox,1375,24,'#c9b894','center',400);
  txt('हयग्रीव रूप',1230,1335,38,'#ffe9b8','center');txt('Hayagriva · the war with Madhu–Kaitabha',1230,1375,24,'#c9b894','center',400);
  lab(0,-648,230,'किरीट मुकुट · वैष्णव तिलक','tall gold crown, white U-tilak',ox,oy,S,1);
  lab(-134,-492,380,'सुदर्शन चक्र','chakra, spinning, upper left hand',ox,oy,S,2);
  lab(134,-492,530,'पाञ्चजन्य शंख','conch, upper right hand',ox,oy,S,3);
  lab(98,-250,680,'कौमोदकी गदा','mace, lower right hand',ox,oy,S,4);
  lab(-96,-292,830,'पद्म (कमल)','lotus, lower left hand',ox,oy,S,5);
  lab(0,-330,980,'वनमाला · कौस्तुभ','garland with the red Kaustubha gem',ox,oy,S,6);
  lab(0,-120,1130,'पीतांबर (पीला धोती)','pleated yellow dhoti + draped upper cloth',ox,oy,S,7);
  const PX=1560;txt('मुख-भाव',PX+30,140,36,'#ffe9b8');
  [['calm','शांत'],['closed','योगनिद्रा'],['rage','दृढ़ संकल्प']].forEach(([e,n],i)=>{const H=figure(c=>{c.scale(1.5,1.5);V2.drawHead(c,0,0,{expr:e==='closed'?'closed':'calm',k:e==='rage'?.6:0,S:C.vishnu,t:1});
    const S2=C.vishnu;c.save();c.translate(0,0);c.fillStyle='#10101c';c.beginPath();c.moveTo(-36,-8);c.bezierCurveTo(-42,-56,42,-56,36,-8);c.bezierCurveTo(26,-30,-26,-30,-36,-8);c.closePath();c.fill();c.restore();
    c.fillStyle='#e6b84a';c.beginPath();c.moveTo(-28,-22);c.lineTo(-22,-74);c.lineTo(-10,-62);c.lineTo(0,-118);c.lineTo(10,-62);c.lineTo(22,-74);c.lineTo(28,-22);c.closePath();c.fill();c.fillStyle='#c4882a';c.fillRect(-28,-30,56,8);c.fillStyle='#e0302a';c.beginPath();c.arc(0,-40,4.4,0,7);c.fill()},400,440,200,300);X.drawImage(H,PX+10+i*262,170,300,330);txt(n,PX+10+i*262+150,525,26,'#ffe9b8','center')});
  txt('शेषशायी विष्णु (योगनिद्रा)',PX+30,600,34,'#ffe9b8');
  const hg=X.createRadialGradient(PX+330,880,20,PX+330,880,300);hg.addColorStop(0,'rgba(255,215,120,.42)');hg.addColorStop(1,'rgba(255,200,90,0)');X.fillStyle=hg;X.fillRect(PX-30,560,820,640);
  const R=figure(c=>{c.scale(.58,.58);V2.drawReclineVishnu(c,{t:1.2})},900,640,420,590);X.drawImage(R,PX-30,600,860,610);
  txt('रंग-पट्टिका',PX+30,1200,32,'#ffe9b8');
  [['#4f7fd6','त्वचा'],['#f2c230','पीतांबर'],['#e6b84a','स्वर्ण'],['#f6e7a8','उत्तरीय'],['#d02a2a','कौस्तुभ'],['#e8ecf6','शेष']].forEach(([c,n],i)=>{X.fillStyle=c;X.beginPath();X.roundRect(PX+30+i*128,1230,110,56,8);X.fill();X.strokeStyle='rgba(255,255,255,.3)';X.stroke();txt(n,PX+85+i*128,1316,20,'#c9b894','center',400)});
  const id=X.getImageData(0,0,2400,1500),d=id.data;let sd=7;for(let i=0;i<d.length;i+=4){sd=(sd*16807)%2147483647;const n=((sd/2147483647)-.5)*14;d[i]+=n;d[i+1]+=n;d[i+2]+=n}X.putImageData(id,0,0);
  const v=X.createRadialGradient(1200,750,500,1200,750,1500);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.45)');X.fillStyle=v;X.fillRect(0,0,2400,1500);document.title='done'}
document.fonts.load('600 40px NSer').then(()=>document.fonts.load('400 24px NSer')).then(go).catch(e=>{console.error(e);go()});
</script>'''
open(os.path.join(R,'library','characters','vishnu','sheet.html'),'w',encoding='utf-8').write(page.replace('__JS__',js))
print('ok')
