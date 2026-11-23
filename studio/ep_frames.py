"""Render one still per shot of an episode with the CURRENT engine, using the voice_timeline.md word times
(no TTS / network needed).  python3 studio/ep_frames.py 06 [--out DIR] [--only 0,5,9-12] [--at 0.55] [--q 86]
Writes <out>/<NNN>_<shotid>.jpg (1920x1080) and contact sheets <out>/sheet_NN.jpg."""
import os,re,sys,json,glob,subprocess,argparse,shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,ROOT+'/studio')
from PIL import Image,ImageDraw
import build as B
def parse_timeline(p):
    t=open(p,encoding='utf-8').read();beats=[];cur=None
    for ln in t.splitlines():
        m=re.match(r'## Beat (\d+)\s+\((\d+):([\d.]+) – (\d+):([\d.]+)\)',ln)
        if m:
            n=int(m[1]);s=int(m[2])*60+float(m[3]);e=int(m[4])*60+float(m[5]);cur={'beat':n,'start':s,'end':e,'words':[]};beats.append(cur);continue
        if cur and ln.startswith('`') and '@' in ln:
            for w in re.findall(r'(\S+)@([\d.]+)',ln.strip('`')):cur['words'].append((w[0],float(w[1])))
    out=[]
    for b in beats:
        ws=[];W=b['words']
        for i,(w,s) in enumerate(W):
            e=W[i+1][1] if i+1<len(W) else min(b['end'],s+.4);ws.append({'text':w,'start':round(s-b['start'],3),'end':round(max(s+.12,min(e,s+.9))-b['start'],3)})
        out.append({'beat':b['beat'],'audio':round(b['end']-b['start'],3),'duration':round(b['end']-b['start'],3),'words':ws})
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('ep');ap.add_argument('--out');ap.add_argument('--only');ap.add_argument('--at',type=float,default=.55);ap.add_argument('--q',type=int,default=86);ap.add_argument('--scale',type=float,default=2.0)
    a=ap.parse_args();epd=f'{ROOT}/episodes/ep{a.ep}';work=f'{ROOT}/build/ep{a.ep}';os.makedirs(work,exist_ok=True)
    out=a.out or f'{ROOT}/library/showcase/ep{a.ep}_frames';os.makedirs(out,exist_ok=True)
    tm=work+'/engine_timings.json';tgt=str(json.load(open(epd+'/episode.json')).get('target_sec',0))
    subprocess.run(['node',ROOT+'/studio/render_ep.js',work,epd+'/shots.json','/dev/null'],env=dict(os.environ,PREPARE_ONLY='1',TARGET_SEC=tgt),check=True,stdout=subprocess.DEVNULL)   # engine_timings.json from the REAL voice timings (build/epNN/timings.json)
    html=B.build(a.scale);env=dict(os.environ,ENGINE=html,VW=str(int(1280*a.scale)),VH=str(int(720*a.scale)))
    info=json.loads(subprocess.check_output(['node',ROOT+'/studio/still.js','--info',epd+'/shots.json',tm],env=dict(env,MISSONLY='1'),cwd=ROOT,text=True))
    inf=info['info'];print('shots',len(inf),'cue misses',info['miss'][:8])
    ids=[s.get('id') for s in json.load(open(epd+'/shot_plan.json'))['shots']]
    sel=range(len(inf))
    if a.only:
        sel=[]
        for part in a.only.split(','):
            if '-' in part:x,y=part.split('-');sel+=list(range(int(x),int(y)+1))
            else:sel.append(int(part))
    tmp=work+'/stills';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp)
    ts=[round(inf[i][1]+inf[i][2]*a.at,2) for i in sel]
    subprocess.run(['node',ROOT+'/studio/still.js',epd+'/shots.json',tm,tmp]+[str(t) for t in ts],env=env,cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    files=[tmp+'/t%s.png'%str(t).rjust(5,'0') if False else None for t in ts]
    fs=sorted(glob.glob(tmp+'/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]));byT={float(os.path.basename(f)[1:-4]):f for f in fs}
    done=[]
    for i,t in zip(sel,ts):
        f=byT.get(float(t))
        if not f:print('missing frame',i,t);continue
        dst=f'{out}/{i:03d}_{ids[i] if i<len(ids) else i}.jpg';Image.open(f).convert('RGB').resize((1920,1080),Image.LANCZOS).save(dst,quality=a.q);done.append((i,dst))
    for n in range(0,len(done),20):
        im=Image.new('RGB',(1920,270*5),(12,10,20))
        for k,(i,dst) in enumerate(done[n:n+20]):
            x=Image.open(dst).resize((384,216));d=ImageDraw.Draw(x);d.rectangle((0,0,92,16),fill=(0,0,0));d.text((4,2),os.path.basename(dst)[:12],fill=(255,230,80));im.paste(x,((k%5)*384,(k//5)*270))
        im.save(f'{out}/sheet_{n//20:02d}.jpg',quality=82)
    print('wrote',len(done),'frames to',out)
main()
