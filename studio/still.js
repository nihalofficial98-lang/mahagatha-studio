const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{let A=process.argv.slice(2);const INFO=A[0]==='--info';if(INFO)A=A.slice(1);const [sf,tf,od,...Ts]=A;const sh=JSON.parse(fs.readFileSync(sf)),tm=JSON.parse(fs.readFileSync(tf));if(!INFO)fs.mkdirSync(od,{recursive:true});
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1920,height:1080}});pg.on('pageerror',e=>console.log('PAGEERR',e.message));pg.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
await pg.goto('file://'+path.resolve(process.env.ENGINE));await pg.evaluate(([s,t])=>window.init(s,t),[sh,tm]);await pg.waitForFunction(()=>window.IMG_PENDING===0,null,{timeout:120000});
if(INFO){const mi=await pg.evaluate(()=>window.CUEMISS),inf=await pg.evaluate(()=>window.SHOTINFO);console.log(JSON.stringify(process.env.MISSONLY?{miss:mi,info:inf}:inf));await b.close();return}
console.log('MISS',JSON.stringify(await pg.evaluate(()=>window.CUEMISS)),JSON.stringify(await pg.evaluate(()=>window.SHOTINFO)).slice(0,600));
for(const T of Ts){await pg.evaluate(t=>window.seek(t),+T);await pg.screenshot({path:`${od}/t${String(T).padStart(5,'0')}.png`})}console.log('FX_ERRORS',JSON.stringify(await pg.evaluate(()=>window.FX_ERRORS||[])));await b.close()})();
