"""Shared helpers for reel brief generators (reels 15/09/10). Same method as reels/reel07/briefs_gen.py:
cinematographer -> scene -> action -> effects written as data; hero faces solved to a target fraction of the 9:16 height;
narration = the spoken words; shot starts found by phrase in the real word timings."""
import json,sys,os,re
R='/home/user/mahagatha-studio'
sys.path.insert(0,R+'/studio')
import validate_brief as VB
class Gen:
    def __init__(s,reel):
        s.reel=reel;s.W=json.load(open(f'{R}/reels/build/{reel}/words.json'));s.T=[(w['w'],w['start']) for w in s.W]
        s.END=json.load(open(f'{R}/reels/{reel}/reel.json'))['duration'];s.S=[]
        s.norm=[re.sub(r"[^a-z0-9']",'',w.lower()) for w,_ in s.T]
    def at(s,phrase,nth=0):
        p=[re.sub(r"[^a-z0-9']",'',x.lower()) for x in phrase.split()];c=0
        for i in range(len(s.norm)-len(p)+1):
            if s.norm[i:i+len(p)]==p:
                if c==nth:return s.T[i][1]
                c+=1
        raise SystemExit(f'phrase not found: {phrase} #{nth}')
    def idx(s,t):
        for i,(w,st) in enumerate(s.T):
            if abs(st-t)<.02:return i
        raise SystemExit(f'no word at {t}')
    def shot(s,phrase,nth=0,**k):
        t=s.at(phrase,nth);i0=s.idx(t);d={"id":"x","beat":1,"start":{"t":t,"word":s.T[i0][0].strip(',.?!"')}};d.update(k);s.S.append(d);return d
    def finish(s,face_default=.42):
        S=s.S;T=s.T
        for i,sh in enumerate(S):
            end=S[i+1]['start']['t'] if i+1<len(S) else s.END
            sh['duration']=round(end-sh['start']['t'],2)
            i0=s.idx(sh['start']['t']);i1=s.idx(S[i+1]['start']['t']) if i+1<len(S) else len(T);sh['narration']=' '.join(w for w,_ in T[i0:i1])
        def ease(k):return k*k*(3-2*k)
        def face_frac(f,sh,u=.55):
            c=sh['camera'];A=c['from'];B=c['to'];e=ease(u)
            z=A.get('z',1)+(B.get('z',1)-A.get('z',1))*e;cy=A.get('y',0)+(B.get('y',0)-A.get('y',0))*e
            fc=f['y'] if f.get('head') else f['y']-(195 if VB.seated(f) else 300)*f['s']*f.get('_fh',1)
            sy=360+(fc-360-cy)*z;V=sh.get('vertical') or {};vz=min(max(V.get('z',1),1),2.2);h=720/vz
            w0=min(max(sy-V.get('y',.36)*h,0),720-h) if vz>1 else 0
            return (sy-w0)/h
        for sh in S:
            fx=[f for f in sh['characters'] if f.get('_fixed')]
            if not fx or (sh.get('vertical') or {}).get('mode')=='stack':continue
            L=0
            while L<70 and any(VB.face_cropped_v(f,{'from':sh['camera']['from'],'to':sh['camera']['to']},sh.get('vertical')) for f in fx if f['s']>=0.15):
                L+=2;sh['camera']['from']['y']+=2;sh['camera']['to']['y']+=2
        for sh in S:
            if (sh.get('vertical') or {}).get('mode')=='stack':continue
            g=None
            for f in sh['characters']:
                if f.get('head') or f.get('_fixed'):continue
                if f.pop('_ground',False) and g is not None:f['y']=g;continue
                tgt=f.pop('_face',face_default)
                for _ in range(400):
                    fr=face_frac(f,sh)
                    if abs(fr-tgt)<.004:break
                    f['y']=round(f['y']-(fr-tgt)*300)
                if g is None:g=f['y']
        for sh in S:
            cam_={'from':sh['camera']['from'],'to':sh['camera']['to']}
            for f in sh['characters']:
                if f.get('_fixed'):continue
                y0=f['y']
                while VB.face_cropped_v(f,cam_,sh.get('vertical')) and y0-f['y']<80:f['y']-=2
                if f['y']!=y0:print('  fit',sh['id'],f['who'],y0,'->',f['y'])
        for sh in S:
            for f in sh['characters']:
                for k in('_face','_ground','_fixed','_fh'):f.pop(k,None)
        for i,sh in enumerate(S):sh['id']=f"s{i+1:02d}"
        order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
        S=[{k:sh[k] for k in order if k in sh} for sh in S]
        json.dump({"episode":s.reel,"format":"vertical","shots":S},open(f'{R}/reels/{s.reel}/briefs.json','w'),ensure_ascii=False,indent=1)
        print(len(S),'shots',[x['duration'] for x in S])
        assert ' '.join(x['narration'] for x in S).split()==[w for w,_ in T],'narration gap'
def cam(move,a,b,shot_='medium',lens='normal',shake=0,mot='',r=(0,0)):
    z0,x0,y0=a;z1,x1,y1=b
    return {"shot":shot_,"lens":lens,"move":move,"from":{"z":z0,"x":x0,"y":y0,"r":r[0]},"to":{"z":z1,"x":x1,"y":y1,"r":r[1]},"shake":shake,"motivation":mot}
def name(word,s,x=640,y=128,size=30):return {"k":"name","word":word,"s":s,"x":x,"y":y,"size":size,"meaning":f"the name {s} on screen the moment it is spoken"}
def glow(word,x,y,r,rgb,ga=.4,meaning="a soft glow behind the figure",behind=True):return {"k":"glow","word":word,"x":x,"y":y,"r":r,"rgb":rgb,"ga":ga,"par":1.0,"behind":behind,"meaning":meaning}
def pfx(k,word,x,y,w,meaning,alpha=1,par=1.0,behind=False,**kw):
    d={"k":k,"word":word,"x":x,"y":y,"w":w,"alpha":alpha,"par":par,"behind":behind,"meaning":meaning};d.update(kw);return d
def mtn(x,y,s,col,w=240,h=150,snow=False):return {"o":"mountain","x":x,"y":y,"s":s,"w":w,"h":h,"col":col,"snow":snow}
def cld(x,y,s=1.2,col="#ffffff"):return {"o":"cloud","x":x,"y":y,"s":s,"col":col}
def far(contents,items,haze='#eef2fa',fog=.55):return {"d":"far","contents":contents,"fog":fog,"haze":haze,"items":items}
def mid(contents,items,fog=.18):return {"d":"mid","contents":contents,"fog":fog,"items":items}
def near(contents,items,dark=.35,blur=2):return {"d":"near","contents":contents,"dark":dark,"blur":blur,"items":items}
def ground(y,col,w=1100,h=10):return {"o":"hill","x":640,"y":y,"s":1.0,"w":w,"h":h,"col":col}
def shrub(x,y=752,s=1.5,col="#2e6a3e",fl="#f0a020"):return {"o":"shrub","x":x,"y":y,"s":s,"col":col,"flowers":fl}
def tree(x,y,s=.6,kind="round",col="#3a7a44"):return {"o":"tree","x":x,"y":y,"s":s,"kind":kind,"col":col}
def bg(k,**p):d={"k":k};d.update(p);return d
def sleep_opt():pass
