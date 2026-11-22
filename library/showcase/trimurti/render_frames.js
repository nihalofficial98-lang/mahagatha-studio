// node library/showcase/trimurti/render_frames.js [frames.json] [outdir]
// Renders every entry {name, scene, t, p, cam} of frames.json to <outdir>/<name>.png at 1920x1080 (Playwright Chromium).
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const D=__dirname,list=JSON.parse(fs.readFileSync(process.argv[2]||path.join(D,'frames.json'))),out=process.argv[3]||path.join(D,'frames'),only=process.env.ONLY;
  fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1920,height:1080}});
  pg.on('pageerror',e=>console.log('PAGEERR',e.message));pg.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
  await pg.goto('file://'+path.join(D,'showcase.html'));
  for(const f of list){if(only&&!f.name.includes(only))continue;await pg.evaluate(f=>window.frame(f.scene,f.t,f.p,f.cam),f);
    await pg.screenshot({path:path.join(out,f.name+'.png')});console.log('wrote',f.name)}
  await b.close()})();
