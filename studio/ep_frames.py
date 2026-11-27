"""Render one still per shot of an episode with the CURRENT engine, using the voice_timeline.md word times
(no TTS / network needed).  python3 studio/ep_frames.py 06 [--out DIR] [--only 0,5,9-12] [--at 0.55] [--q 86]
Writes <out>/<NNN>_<shotid>.jpg (1920x1080) and contact sheets <out>/sheet_NN.jpg.
Reels (9:16, format from reels/<id>/reel.json or --format vertical): python3 studio/ep_frames.py reel02 -> library/showcase/reel02_frames/
<NNN>_<shotid>.jpg at 1080x1920 (--scale 1.5 default; 1.0 = 720x1280) with the title card and reel subtitles drawn."""
import os,re,sys,json,glob,subprocess,argparse,shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,ROOT+'/studio')
from PIL import Image,ImageDraw
import build as B,project as PJ
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
    if 'NODE_PATH' not in os.environ:os.environ['NODE_PATH']=subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()   # playwright is installed globally
    ap=argparse.ArgumentParser();ap.add_argument('ep');ap.add_argument('--out');ap.add_argument('--only');ap.add_argument('--at',type=float,default=.55);ap.add_argument('--q',type=int,default=86);ap.add_argument('--scale',type=float);ap.add_argument('--format',default='auto',choices=['auto','16:9','vertical'])
    a=ap.parse_args();epd=PJ.edir(a.ep);work=PJ.bdir(a.ep);os.makedirs(work,exist_ok=True);vert=PJ.fmt(a.ep,a.format)=='vertical'
    if a.scale is None:a.scale=1.5 if vert else 2.0
    out=a.out or f'{ROOT}/library/showcase/'+(f'{a.ep}_frames' if PJ.is_reel(a.ep) else f'ep{a.ep}_frames');os.makedirs(out,exist_ok=True)
    tm=work+'/engine_timings.json';tgt=str(PJ.target(a.ep))
    subprocess.run(['node',ROOT+'/studio/render_ep.js',work,epd+'/shots.json','/dev/null'],env=dict(os.environ,PREPARE_ONLY='1',TARGET_SEC=tgt),check=True,stdout=subprocess.DEVNULL)   # engine_timings.json from the REAL voice timings (build/epNN/timings.json)
    if vert:html=B.build(a.scale,fmt='vertical');VW,VH=int(720*a.scale),int(1280*a.scale);SIZE=(VW,VH)
    else:html=B.build(a.scale);VW,VH=int(1280*a.scale),int(720*a.scale);SIZE=(1920,1080)
    env=dict(os.environ,ENGINE=html,VW=str(VW),VH=str(VH))
    raw=subprocess.check_output(['node',ROOT+'/studio/still.js','--info',epd+'/shots.json',tm],env=dict(env,MISSONLY='1'),cwd=ROOT,text=True)
    info=json.loads([l for l in raw.splitlines() if l.startswith('{')][-1])
    for l in raw.splitlines():
        if l.startswith(('PAGEERR','CONSOLE')):print(l)
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
    if sel and sel[0]==0 and sel[0] in range(len(inf)):ts[0]=round(inf[0][1]+min(inf[0][2]*a.at,1.2),2)   # first shot: still taken while the title card is up
    r=subprocess.run(['node',ROOT+'/studio/still.js',epd+'/shots.json',tm,tmp]+[str(t) for t in ts],env=env,cwd=ROOT,capture_output=True,text=True)
    if r.returncode:print(r.stderr[-2500:],r.stdout[-800:]);sys.exit('still.js failed')
    for l in r.stdout.splitlines():
        if l.startswith(('PAGEERR','CONSOLE','FX_ERRORS')) and l!='FX_ERRORS []':print(l)
    files=[tmp+'/t%s.png'%str(t).rjust(5,'0') if False else None for t in ts]
    fs=sorted(glob.glob(tmp+'/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]));byT={float(os.path.basename(f)[1:-4]):f for f in fs}
    done=[]
    for i,t in zip(sel,ts):
        f=byT.get(float(t))
        if not f:print('missing frame',i,t);continue
        dst=f'{out}/{i:03d}_{ids[i] if i<len(ids) else i}.jpg';im_=Image.open(f).convert('RGB');(im_ if im_.size==SIZE else im_.resize(SIZE,Image.LANCZOS)).save(dst,quality=a.q);done.append((i,dst))
    if vert:   # 9:16 contact sheets: 6 portrait tiles (3 x 2), each captioned with the shot number, id and the spoken line (briefs.json narration)
        from PIL import ImageFont
        nar={}
        bp=epd+'/briefs.json'
        if os.path.exists(bp):nar={b_['id']:b_.get('narration','') for b_ in json.load(open(bp,encoding='utf-8'))['shots']}
        def font(sz):
            for f_ in ('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf','/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'):
                if os.path.exists(f_):return ImageFont.truetype(f_,sz)
            return ImageFont.load_default()
        F1,F2=font(22),font(17);TW,TH,CAP=420,746,96
        for n in range(0,len(done),6):
            im=Image.new('RGB',(3*TW,2*(TH+CAP)),(12,10,20));d=ImageDraw.Draw(im)
            for k,(i,dst) in enumerate(done[n:n+6]):
                x0,y0=(k%3)*TW,(k//3)*(TH+CAP);im.paste(Image.open(dst).resize((TW,TH)),(x0,y0))
                sid=os.path.basename(dst)[4:-4];d.text((x0+8,y0+TH+6),f'#{i+1:02d}  {sid}',font=F1,fill=(255,214,90))
                ws=nar.get(sid,'').split();ln=[];cur=''
                for w_ in ws:
                    if d.textlength(cur+' '+w_,font=F2)>TW-16 and cur:ln.append(cur);cur=w_
                    else:cur=(cur+' '+w_).strip()
                if cur:ln.append(cur)
                for r_,t_ in enumerate(ln[:3]):d.text((x0+8,y0+TH+34+r_*20),t_,font=F2,fill=(240,236,224))
            im.save(f'{out}/sheet_{n//6:02d}.jpg',quality=84)
        print('wrote',len(done),'frames to',out);return
    for n in range(0,len(done),20):
        im=Image.new('RGB',(1920,270*5),(12,10,20))
        for k,(i,dst) in enumerate(done[n:n+20]):
            x=Image.open(dst).resize((384,216));d=ImageDraw.Draw(x);d.rectangle((0,0,92,16),fill=(0,0,0));d.text((4,2),os.path.basename(dst)[:12],fill=(255,230,80));im.paste(x,((k%5)*384,(k//5)*270))
        im.save(f'{out}/sheet_{n//20:02d}.jpg',quality=82)
    print('wrote',len(done),'frames to',out)
main()
