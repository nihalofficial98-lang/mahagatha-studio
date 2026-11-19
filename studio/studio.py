#!/usr/bin/env python3
"""Mahagatha Studio — one CLI for the whole pipeline.
  studio.py new 03 "title"        scaffold episodes/ep03
  studio.py check 03              lint the script (length, beats, cue tags)
  studio.py voice-docs 03         write voiceover files (tagged for AI voice, clean for you) into voiceovers/
  studio.py tts 03                guide voice + word timings (stand-in until your own recording)
  studio.py shots 03              run the director's edit list -> shots.json
  studio.py stills 03             contact sheets of every shot (build/ep03/sheets)
  studio.py qa 03 [--video f]     automated QA (cue misses, shot lengths, frozen/black frames)
  studio.py render 03 [--res 4k]  render film (1080p default, --res 4k for 3840x2160)
  studio.py feedback 03 "text" --cat visual|audio|script|timing --shot N   log feedback
  studio.py learn                 rebuild library/BACKLOG.md from open feedback
  studio.py gallery               reference stills of the asset library for the current engine version
"""
import argparse,json,os,re,subprocess,sys,glob,datetime,shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,os.path.join(ROOT,'studio'))
def ep(n): return os.path.join(ROOT,'episodes','ep'+n)
def bd(n): return os.path.join(ROOT,'build','ep'+n)
def sh(cmd,**k):
    print('+',cmd if isinstance(cmd,str) else ' '.join(cmd));env=dict(os.environ);env.update(k.pop('env',{}))
    r=subprocess.run(cmd,shell=isinstance(cmd,str),cwd=ROOT,env=env,**k)
    if r.returncode:sys.exit(r.returncode)
    return r
def node_env():
    e={}
    try:e['NODE_PATH']=subprocess.check_output(['npm','root','-g'],text=True).strip()
    except Exception:pass
    return e
def beats(n):
    txt=open(os.path.join(ep(n),'script.md'),encoding='utf-8').read();out=[];cur=None
    for line in txt.split('\n'):
        m=re.match(r'\*\*B(\d+)\*\*\s*(\[[^\]]*\])?',line.strip())
        if m: cur={'beat':int(m.group(1)),'cue':m.group(2) or '','lines':[]};out.append(cur);continue
        l=line.strip()
        if cur and l and not l.startswith(('#','---','*समाप्त')): cur['lines'].append(l)
        if l.startswith('---'):cur=None
    return out
def cmd_new(a):
    d=ep(a.n)
    if os.path.exists(d):sys.exit('exists')
    os.makedirs(d)
    open(d+'/script.md','w',encoding='utf-8').write(f"# एपिसोड {a.n} — {a.title}\n\n**अनुमानित समय:** 8–9 मिनट\n**स्रोत:** (story numbers from source/)\n\n---\n\n**B01** [धीमे, रहस्यमयी]\n(Hook: 3–4 short lines; end on a question/danger.)\n\n**B02** [भव्य]\n\n---\n*समाप्त*\n")
    open(d+'/shots.py','w').write('''import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'))
from shotkit import *
HERE=os.path.dirname(os.path.abspath(__file__));f=Film();add=f.add
# add(beat, spoken-word trigger | seconds, scene-dict, grade, cam=None, draw='scene', cues=[words], shake=n, dx=dissolve_s)
# scene = {'bg':bg('cel'),'figs':[F('brahma',CX,700,1.5)],'fx':[{'t':'name','s':'ब्रह्मा','x':CX,'y':200,'c':0}]}
# see guides/DIRECTION.md for the shot grammar and library/CHARACTERS.md for the cast
print(f.save(os.path.join(HERE,'shots.json')),'shots')
''')
    open(d+'/feedback.md','w').write('# Feedback for ep'+a.n+'\n(use: studio.py feedback '+a.n+' "text")\n')
    print('created',d)
def cmd_check(a):
    b=beats(a.n);words=0;warn=[]
    for x in b:
        w=sum(len(l.split()) for l in x['lines']);words+=w
        if not x['cue']:warn.append(f"B{x['beat']:02d}: no [emotion cue]")
        if w>130:warn.append(f"B{x['beat']:02d}: {w} words — long; split it (shots need fresh words every 3–4 s)")
        if w==0:warn.append(f"B{x['beat']:02d}: empty")
        if re.search(r'[A-Za-z]{4,}',' '.join(x['lines'])):warn.append(f"B{x['beat']:02d}: Latin text in narration")
    est=words*0.575
    print(f'{len(b)} beats, {words} words, ~{est/60:.1f} min at guide pace (rule: 8–10 min, aim 8.5–9.5)')
    if not 492<=est<=588:warn.append('length outside the safe 8.2–9.8 min band (hard rule: video must be 8–10 min)')
    print('\n'.join('WARN '+w for w in warn) or 'script OK')
def cmd_voice(a):
    b=beats(a.n);os.makedirs(os.path.join(ROOT,'voiceovers'),exist_ok=True)
    t=[f"**B{x['beat']:02d}** {x['cue']}\n"+'\n'.join(x['lines']) for x in b]
    open(f'{ROOT}/voiceovers/ep{a.n}_tagged.md','w',encoding='utf-8').write('\n\n'.join(t))
    open(f'{ROOT}/voiceovers/ep{a.n}_clean.md','w',encoding='utf-8').write('\n\n'.join('\n'.join(x['lines']) for x in b))
    print('wrote voiceovers/ep%s_tagged.md (AI-voice tool, with emotion cues) and _clean.md (read aloud, no tags)'%a.n)
def cmd_tts(a):
    os.makedirs(bd(a.n),exist_ok=True)
    sh(['python3','studio/parse_script.py',ep(a.n)+'/script.md',bd(a.n)+'/beats.json'])
    sh(['python3','studio/tts.py',bd(a.n)+'/beats.json',bd(a.n)])
def cmd_shots(a): sh(['python3',ep(a.n)+'/shots.py'])
def prepare(a,target):
    sh(['node','studio/render_ep.js',bd(a.n),ep(a.n)+'/shots.json','/dev/null'],env=dict(node_env(),PREPARE_ONLY='1',TARGET_SEC=str(target)))
def target(a): 
    try:return json.load(open(ep(a.n)+'/episode.json')).get('target_sec',0)
    except Exception:return 0
def info(a,html):
    out=subprocess.check_output(['node','studio/still.js','--info',ep(a.n)+'/shots.json',bd(a.n)+'/engine_timings.json'],env=dict(os.environ,ENGINE=html,**node_env()),cwd=ROOT,text=True)
    return json.loads(out)
def cmd_stills(a):
    import build as B;html=B.build(1.5);prepare(a,target(a));d=bd(a.n)+'/stills';shutil.rmtree(d,ignore_errors=True)
    inf=info(a,html);ts=[round(s+dur*0.55,2) for _,s,dur in inf]
    sh(['node','studio/still.js',ep(a.n)+'/shots.json',bd(a.n)+'/engine_timings.json',d]+[str(t) for t in ts],env=dict(node_env(),ENGINE=html))
    from PIL import Image,ImageDraw
    fs=sorted(glob.glob(d+'/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]));os.makedirs(bd(a.n)+'/sheets',exist_ok=True)
    for n in range(0,len(fs),16):
        im=Image.new('RGB',(1920,1080))
        for i,f in enumerate(fs[n:n+16]):
            x=Image.open(f).convert('RGB').resize((480,270));ImageDraw.Draw(x).text((6,6),str(n+i),fill=(255,255,0));im.paste(x,((i%4)*480,(i//4)*270))
        im.save(f'{bd(a.n)}/sheets/sheet_{n//16}.jpg',quality=82)
    print('sheets in',bd(a.n)+'/sheets')
def cmd_qa(a):
    import build as B;html=B.build(1.5);prepare(a,target(a));rules=json.load(open(ROOT+'/library/rules.json'));bad=[]
    out=subprocess.check_output(['node','studio/still.js','--info',ep(a.n)+'/shots.json',bd(a.n)+'/engine_timings.json'],env=dict(os.environ,ENGINE=html,MISSONLY='1',**node_env()),cwd=ROOT,text=True)
    data=json.loads(out);inf=data['info'];miss=data['miss']
    if miss:bad.append(f'cue words not found in narration: {miss}')
    durs=[d for _,_,d in inf];avg=sum(durs)/len(durs)
    for i,(k,s,d) in enumerate(inf):
        if d>rules['max_shot_sec']:bad.append(f'shot {i} ({k}@{s}s) lasts {d}s > {rules["max_shot_sec"]}')
        if d<rules['min_shot_sec']:bad.append(f'shot {i} ({k}@{s}s) only {d}s < {rules["min_shot_sec"]}')
    shots=json.load(open(ep(a.n)+'/shots.json'))
    for i in range(1,len(shots)):
        if shots[i]['draw']==shots[i-1]['draw']=='scene' and json.dumps(shots[i].get('sc'),sort_keys=True)==json.dumps(shots[i-1].get('sc'),sort_keys=True):bad.append(f'shots {i-1},{i} identical (repeated frame)')
    total=sum(b['duration'] for b in json.load(open(bd(a.n)+'/engine_timings.json')))
    try:is_test=json.load(open(ep(a.n)+'/episode.json')).get('test',False)
    except Exception:is_test=False
    if not is_test and not rules['min_video_sec']<=total<=rules['max_video_sec']:bad.append(f'video length {total/60:.2f} min outside {rules["min_video_sec"]//60}–{rules["max_video_sec"]//60} min rule')
    print(f'video length {total/60:.2f} min'+(' (test episode, length rule skipped)' if is_test else f' (rule {rules["min_video_sec"]//60}–{rules["max_video_sec"]//60})'))
    print(f'{len(inf)} shots, avg {avg:.2f}s (rule {rules["avg_shot_sec"][0]}–{rules["avg_shot_sec"][1]})')
    if not rules['avg_shot_sec'][0]<=avg<=rules['avg_shot_sec'][1]:bad.append('average shot length out of range')
    if a.video:
        r=subprocess.run(['ffmpeg','-v','info','-i',a.video,'-vf','freezedetect=n=-60dB:d=%s,blackdetect=d=0.5:pix_th=0.05'%rules['max_freeze_sec'],'-an','-f','null','-'],capture_output=True,text=True).stderr
        fz=re.findall(r'freeze_start: ([\d.]+)',r);bl=re.findall(r'black_start:([\d.]+)',r)
        if fz:bad.append(f'frozen picture >{rules["max_freeze_sec"]}s at {fz[:8]}')
        bl=[b for b in bl if 1<float(b)]; 
        if bl:bad.append(f'black frames at {bl[:6]}')
    print('\n'.join('FAIL '+b for b in bad) or 'QA PASS');sys.exit(1 if bad else 0)
def cmd_render(a):
    import build as B;sc=3 if a.res=='4k' else (1 if a.res=='720p' else 1.5);html=B.build(sc);os.makedirs(ROOT+'/renders',exist_ok=True)
    W,H=(3840,2160) if a.res=='4k' else ((1280,720) if a.res=='720p' else (1920,1080));out=f'{ROOT}/renders/ep{a.n}_{a.res}.mp4'
    sh(['node','studio/render_ep.js',bd(a.n),ep(a.n)+'/shots.json',out,str(a.workers),'30'],env=dict(node_env(),ENGINE=html,VW=str(W),VH=str(H),CRF='26' if a.res in ('4k','720p') else '20',JQ='90',TARGET_SEC=str(target(a))))
    print(out)
def cmd_feedback(a):
    rec={'date':datetime.date.today().isoformat(),'ep':a.n,'cat':a.cat,'shot':a.shot,'text':a.text,'status':'open'}
    open(ROOT+'/library/feedback.jsonl','a',encoding='utf-8').write(json.dumps(rec,ensure_ascii=False)+'\n');print('logged');cmd_learn(a)
def cmd_learn(a):
    rows=[json.loads(l) for l in open(ROOT+'/library/feedback.jsonl',encoding='utf-8') if l.strip()];seed=open(ROOT+'/library/BACKLOG_SEED.md',encoding='utf-8').read()
    o=['# Improvement backlog (auto-generated by `studio.py learn`)\n','Work top-down. When fixed: set status to `done` in library/feedback.jsonl and add a line to CHANGELOG.md.\n']
    for cat in ('visual','audio','timing','script'):
        r=[x for x in rows if x['cat']==cat and x['status']=='open']
        if r:o.append(f'\n## {cat} ({len(r)} open)');o+= [f"- [ep{x['ep']}{' shot '+str(x['shot']) if x.get('shot') is not None else ''}] {x['text']}" for x in r]
    o.append('\n'+seed);open(ROOT+'/library/BACKLOG.md','w',encoding='utf-8').write('\n'.join(o));print('library/BACKLOG.md updated')
def cmd_gallery(a):
    sh(['python3','studio/gallery.py'])
if __name__=='__main__':
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='c',required=True)
    for name,f in [('new',cmd_new),('check',cmd_check),('voice-docs',cmd_voice),('tts',cmd_tts),('shots',cmd_shots),('stills',cmd_stills),('qa',cmd_qa),('render',cmd_render),('feedback',cmd_feedback),('learn',cmd_learn),('gallery',cmd_gallery)]:
        q=s.add_parser(name);q.set_defaults(f=f)
        if name not in('learn','gallery'):q.add_argument('n')
        if name=='new':q.add_argument('title')
        if name=='qa':q.add_argument('--video')
        if name=='render':q.add_argument('--res',default='1080p');q.add_argument('--workers',type=int,default=4)
        if name=='feedback':q.add_argument('text');q.add_argument('--cat',default='visual');q.add_argument('--shot',type=int)
    a=p.parse_args();a.f(a)
