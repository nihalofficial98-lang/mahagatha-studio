// node render_ep.js <build_dir> <shots.json> <out.mp4> [workers] [fps]
// Parallel 1080p renderer: splits frames across worker processes, then concatenates + muxes voice.
// PREPARE_ONLY=1: only write engine_timings.json. VOICE_ONLY=1: also build voice.wav, then stop (studio/render_chunks.py uses both).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {spawn,execSync}=require('child_process');
const A=process.argv.slice(2);const ENG=process.env.ENGINE||'engine.html',VW=+(process.env.VW||1920),VH=+(process.env.VH||1080),CRF=process.env.CRF||'21',JQ=+(process.env.JQ||93);
async function worker(B,shotsF,part,f0,f1,fps){
  const tm=JSON.parse(fs.readFileSync(B+'/engine_timings.json')),sh=JSON.parse(fs.readFileSync(shotsF));
  const b=await chromium.launch();const pg=await b.newPage({viewport:{width:VW,height:VH}});
  pg.on('pageerror',e=>console.log('PAGEERR',e.message));
  await pg.goto('file://'+path.resolve(__dirname,ENG));await pg.evaluate(([s,t])=>window.init(s,t),[sh,tm]);await pg.waitForFunction(()=>window.IMG_PENDING===0,null,{timeout:120000});
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf',CRF,'-pix_fmt','yuv420p','-threads','2',part],{stdio:['pipe','inherit','inherit']});
  for(let f=f0;f<f1;f++){await pg.evaluate(t=>window.seek(t),f/fps);const buf=await pg.screenshot({type:'jpeg',quality:JQ});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if((f-f0)%240===0)console.log(`[${path.basename(part)}] ${f-f0}/${f1-f0}`)}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close()}
(async()=>{
 if(A[0]==='--worker'){const [,B,S,part,f0,f1,fps]=A;await worker(B,S,part,+f0,+f1,+fps);return}
 const [B,S,out,W_='3',FPS='24']=A;const fps=+FPS,nW=+W_;
 const tm=JSON.parse(fs.readFileSync(B+'/timings.json')),beats=JSON.parse(fs.readFileSync(B+'/beats.json')).scenes;
 const RAW=tm.reduce((a,t)=>a+t.duration,0),TARGET=+(process.env.TARGET_SEC||0),TEMPO=TARGET?Math.max(1,Math.min(1.25,RAW/TARGET)):1.06;console.log('raw',RAW.toFixed(1),'s tempo',TEMPO.toFixed(3));tm.forEach((t,i)=>{t.beat=beats[i].beat;t.audio/=TEMPO;t.duration/=TEMPO;t.words.forEach(w=>{w.start/=TEMPO;w.end/=TEMPO})});fs.writeFileSync(B+'/engine_timings.json',JSON.stringify(tm));if(process.env.PREPARE_ONLY){console.log('prepared');return}
 // voice track
 let list='';tm.forEach((t,i)=>{const n=String(i).padStart(2,'0');execSync(`ffmpeg -y -v error -i ${B}/audio/${n}.mp3 -af atempo=${TEMPO},apad=pad_dur=${(t.duration-t.audio).toFixed(3)} -t ${t.duration.toFixed(3)} -ar 44100 -ac 2 ${B}/audio/v${n}.wav`);list+=`file 'v${n}.wav'\n`});
 fs.writeFileSync(B+'/audio/vlist.txt',list);execSync(`ffmpeg -y -v error -f concat -safe 0 -i ${B}/audio/vlist.txt -c copy ${B}/voice.wav`);if(process.env.VOICE_ONLY){console.log('voice ready');return}
 const total=tm.reduce((a,t)=>a+t.duration,0),N=Math.round(total*fps);console.log(`total ${(total/60).toFixed(2)} min, ${N} frames, ${nW} workers`);
 const per=Math.ceil(N/nW),parts=[];const t0=Date.now();
 await Promise.all([...Array(nW)].map((_,i)=>{const f0=i*per,f1=Math.min(N,f0+per),part=`${B}/part${i}.mp4`;parts.push(part);
   return new Promise(r=>{const c=spawn('node',[__filename,'--worker',B,S,part,f0,f1,fps],{stdio:'inherit'});c.on('close',r)})}));
 fs.writeFileSync(B+'/parts.txt',parts.map(p=>`file '${path.basename(p)}'`).join('\n'));
 if(process.env.SILENT)execSync(`ffmpeg -y -v error -f concat -safe 0 -i ${B}/parts.txt -c:v copy -an ${out}`);else execSync(`ffmpeg -y -v error -f concat -safe 0 -i ${B}/parts.txt -i ${B}/voice.wav -c:v copy -c:a aac -b:a 192k -shortest ${out}`);
 console.log('done',out,((Date.now()-t0)/1000).toFixed(0)+'s')})();
