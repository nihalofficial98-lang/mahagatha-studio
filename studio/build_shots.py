"""Build shots.json from a scene director's shot_plan.json, timed to the owner's voice (word timestamps). Validates as it builds.
 python3 studio/build_shots.py 04 [--plan episodes/ep04/shot_plan.json] [--out episodes/ep04/shots.json]
 Reels: python3 studio/build_shots.py reel02 (reels/reel02/, timings from reels/build/reel02/; first shot gets the reel.json title card)
Plan format: see library/ENGINE_CAPABILITIES.md ("Shot plan"). Hand-coded exceptions go in episodes/epNN/custom_shots.py and are referenced with {"custom": name, "args": {...}}."""
import json,sys,os,re,shutil,importlib.util
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__))))
from shotkit import Film
import engine_vocab as V,project as PJ
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=R+'/library/pilot/assets/'
<<<<<<< HEAD
WHO=set(V.CAST)
BGK=set(V.BG)
FXT=set(V.FX)|{'heart','sparkle'}   # the last two are rejected below as banned
RESERVED={'id','at','cues','bg','figs','fx','fxb','cam','grade','note','custom','args','len_hint','layers','bg2','bgTo','bgc','bgd'}
=======
WHO=set('shiva vishnu brahma vishnu3 brahma3 narada3 daksha narada manu adishakti brahmi madhu kaitabha harihara ardha vishnu_rest hayagriva kumara jaya vijaya villager villager_w prasuti sati diti danu asikli kashyapa indra surya chandra hiranyaksha hiranyakashipu ravana boar swan'.split())|{f'rishi{i}' for i in range(7)}
BGK=set('vista cloudscape earth pillar cel storm voidR night dusk moon palace dawn amber cosmos sea plain yagna kailash garden cosmicsea img'.split())
FXT=set('text name glow orbs sparkle petals shock flash bolt crack ribbon beam light flames fire pillar infinity scales trident heart tears threads outline egg books gunas element lotus bluemountain waterfront vaikuntha clock dim fximg skull arrow asuras ban body cycle flame frost icon kids lotusI person vortex'.split())
RESERVED={'id','at','cues','bg','figs','fx','fxb','cam','grade','note','custom','args','len_hint'}
>>>>>>> origin/main
def norm(w):return re.sub(r'[^\wऀ-ॿ]','',w)
def pfx_name(src):
    """legacy image names ('fx_boulder', '../library/pilot/assets/fx_boulder.png', 'boulder') -> code-drawn effect name"""
    n=os.path.basename(str(src));n=n[:-4] if n.endswith('.png') else n
    return n[3:] if n.startswith('fx_') else n
def load_actions(epdir):
    import os,json
    p=os.path.join(epdir,'action_plan.json')
    return json.load(open(p,encoding='utf-8')).get('shots',{}) if os.path.exists(p) else {}
def main():
    ep=sys.argv[1];E=PJ.edir(ep);BD=PJ.bdir(ep);VERT=PJ.fmt(ep)=='vertical';plan_p=f'{E}/shot_plan.json';out_p=f'{E}/shots.json'
    if '--plan' in sys.argv:plan_p=os.path.abspath(sys.argv[sys.argv.index('--plan')+1])
    if '--out' in sys.argv:out_p=os.path.abspath(sys.argv[sys.argv.index('--out')+1])
    plan=json.load(open(plan_p,encoding='utf-8'));T=json.load(open(f'{BD}/timings.json',encoding='utf-8'));Bt=json.load(open(f'{BD}/beats.json',encoding='utf-8'))['scenes']
    ACT=load_actions(E)
    for s_ in (plan['shots'] if isinstance(plan,dict) else plan):
        a_=ACT.get(s_.get('id'))
        if not a_:continue
        for k_,spec in (a_.get('figs') or {}).items():
            try:s_['figs'][int(k_)].update(spec)
            except Exception:pass
        for w_ in (a_.get('cues_add') or []):
            s_.setdefault('cues',[])
            if w_ not in s_['cues']:s_['cues'].append(w_)
    beats=[];off=0.0;allw=[]
    for t,sc in zip(T,Bt):
        i=0;lines=[]
        for seg in sc['narration']:
            n=len(seg['t'].split());ws=[(norm(w['text']),off+w['start'],off+w['end']) for w in t['words'][i:i+n]];i+=n;lines.append(ws);allw+=ws
        beats.append({'beat':sc['beat'],'start':off,'end':off+t['duration'],'lines':lines});off+=t['duration']
    total=off;errs=[];warns=[];film=Film();custom=None
    cp=f'{E}/custom_shots.py'
    if os.path.exists(cp):
        spec=importlib.util.spec_from_file_location('custom_shots',cp);custom=importlib.util.module_from_spec(spec);spec.loader.exec_module(custom)
    def beat_of(t):
        for b in beats:
            if b['start']-1e-6<=t<b['end']:return b
        return beats[-1]
    def resolve(a,sid):
        if 't' in a:
            t=float(a['t'])
            if a.get('word'):
                w=norm(a['word']);near=[x for x in allw if x[0]==w or x[0].startswith(w) or w.startswith(x[0])]
                if not near or min(abs(x[1]-t) for x in near)>.6:errs.append(f"{sid}: word '{a['word']}' is not at {t}s in the voice (closest {None if not near else round(min(abs(x[1]-t) for x in near),2)}s away)")
            return t
        b=next((x for x in beats if x['beat']==a['beat']),None)
        if b is None:errs.append(f"{sid}: beat {a.get('beat')} not found");return 0.0
        if 'word' in a:
            w=norm(a['word']);hit=[x for ln in b['lines'] for x in ln if x[0]==w or x[0].startswith(w)]
            if not hit:errs.append(f"{sid}: word '{a['word']}' not in beat {a['beat']}");return b['start']
            return hit[0][1]
        ln=b['lines'][a.get('line',0)];return ln[0][1]+a.get('frac',0)*(ln[-1][2]-ln[0][1])
    shots=[]
    for i,s in enumerate(plan['shots']):
        sid=s.get('id',f's{i+1:03d}');t=resolve(s['at'],sid);shots.append((t,sid,s))
    shots.sort(key=lambda x:x[0]);firsts={}
    for k,(t,sid,s) in enumerate(shots):
        b=beat_of(t);rel=t-b['start']
        if b['beat'] not in firsts:
            firsts[b['beat']]=True
            if rel>.6:errs.append(f"{sid}: first shot of beat {b['beat']} starts {rel:.2f}s after the beat starts (a beat needs a shot at its start)")
            rel=0.0
        nxt=shots[k+1][0] if k+1<len(shots) else total;dur=nxt-t
        if dur<1.0:warns.append(f"{sid}@{t:.2f}s lasts only {dur:.2f}s (<1.0)")
        if dur>6.5:warns.append(f"{sid}@{t:.2f}s lasts {dur:.2f}s (>6.5)")
        if s.get('custom'):
            if not custom or not hasattr(custom,s['custom']):errs.append(f"{sid}: custom function '{s['custom']}' not found in custom_shots.py");continue
            sc=getattr(custom,s['custom'])(**(s.get('args') or {}))
        else:
            bgd=s.get('bg','plain');bgd={'k':bgd} if isinstance(bgd,str) else dict(bgd)
            if bgd.get('k') not in BGK:errs.append(f"{sid}: unknown background '{bgd.get('k')}'")
            figs=[]
            for f in s.get('figs',[]):
                f=dict(f)
                if f.get('who') not in ('boar','swan') and f.get('pose') and isinstance(f.get('pose'),str) and f['pose'] not in V.POSES:errs.append(f"{sid}: unknown pose '{f['pose']}'")
                if f.get('emo') and f['emo'] not in V.EMO:errs.append(f"{sid}: unknown emo '{f['emo']}'")
                if f.get('who') not in WHO:errs.append(f"{sid}: unknown character '{f.get('who')}'")
                figs.append(f)
            def fxs(L):
                out=[]
                for x in L:
                    x=dict(x)
                    if x.get('t') in('img','image','fximg'):x={k_:v_ for k_,v_ in x.items() if k_!='src'}|{'t':'pfx','k':pfx_name(x.get('src',''))}
                    if x.get('t')=='pfx' and x.get('k') not in V.PFX:errs.append(f"{sid}: unknown pfx effect '{x.get('k')}' (known: {', '.join(V.PFX)})")
                    if x.get('t') not in FXT:errs.append(f"{sid}: unknown effect '{x.get('t')}'")
                    _src=str(x.get('src','')).lower()
                    if x.get('t') in('heart','sparkle','stars','star_field') or any(w in _src for w in('heart','star','sparkle')):errs.append(f"{sid}: BANNED effect/image '{x.get('t')} {x.get('src','')}' (owner rule: no hearts, stars or sparkles)")
                    if x.get('t')=='threads' and not x.get('to'):errs.append(f"{sid}: 'threads' needs x, y and a 'to' list of [x,y] endpoints")
                    if x.get('t')=='orbs' and not x.get('items'):errs.append(f"{sid}: 'orbs' needs an 'items' list")
                    if x.get('t')=='beam' and not x.get('len'):errs.append(f"{sid}: 'beam' needs x, y and len")
                    if x.get('t')=='infinity' and ('x' not in x or 'y' not in x):errs.append(f"{sid}: 'infinity' needs x and y")
                    if x.get('t')=='text' and not x.get('s'):errs.append(f"{sid}: 'text' needs 's'")
                    out.append(x)
                return out
            sc={'bg':bgd,'figs':figs,'fx':fxs(s.get('fx',[])),'fxb':fxs(s.get('fxb',[]))}
            for k2 in('bg2','bgTo','bgc','bgd'):
                if k2 in s:sc[k2]=s[k2]
            if s.get('bg2') and s['bg2'].get('k') not in BGK:errs.append(f"{sid}: unknown bg2 '{s['bg2'].get('k')}'")
            if s.get('layers'):
                for ly in s['layers']:
                    for it in ly.get('items',[]):
                        if it.get('o') not in V.OBJ:errs.append(f"{sid}: unknown layer object '{it.get('o')}' (known: {', '.join(V.OBJ)})")
                sc['layers']=s['layers']
        cam=s.get('cam')
        if cam:
            for e in('from','to'):
                c=cam.get(e,{})
                if not .9<=c.get('z',1)<=3.1 or abs(c.get('x',0))>220 or abs(c.get('y',0))>220 or abs(c.get('r',0))>.08:warns.append(f"{sid}: camera '{e}' looks extreme {c}")
        if not VERT and 'sc' in dir() and isinstance(sc,dict) and sc.get('figs') is not None:   # 16:9 face rule (reels: validate_brief.py checks the 9:16 window)
            for ff in sc['figs']:
                if ff.get('who') in (None,'img','boar','swan','bull'):continue
                fs=ff.get('s',1);fx0,fy0=ff.get('x',640),ff.get('y',500)
                if ff.get('head'):cy=fy0;top=fy0-104*fs;chin=fy0+75*fs
                else:cy=fy0-(195 if ff.get('pose') in ('sit','sitpray') else 300)*fs;top=cy-105*fs;chin=cy+55*fs   # seated rigs: face ~195*s above y
                for e in((cam or {}).get('from',{}),(cam or {}).get('to',{})) if cam else [{}]:
                    z=e.get('z',1);cy_=e.get('y',0)
                    t_=360+(top-360-cy_)*z;c_=360+(chin-360-cy_)*z;cx_=640+(fx0-640-e.get('x',0))*z   # exact engine camera
                    if t_<2 or c_>640 or cx_<20 or cx_>1260:
                        errs.append(f"{sid}: FACE CROPPED '{ff.get('who')}' (x={fx0}, y={fy0}, s={fs}, head={bool(ff.get('head'))}): crown at {t_:.0f}, chin at {c_:.0f} on a 720-high frame. Move the figure so the whole face is visible above the subtitles.");break
        ncue=len(s.get('cues') or [])
        for x in (sc.get('fx',[])+sc.get('fxb',[])):
            if isinstance(x,dict) and x.get('c') is not None and x['c']>=ncue:warns.append(f"{sid}: effect '{x.get('t')}' fades in on cue c={x['c']} but the shot lists {ncue} cue word(s): it will stay invisible. Add the cue word to 'cues' (or drop 'c').")
        extra={k2:v for k2,v in s.items() if k2 not in RESERVED}
        if VERT and k==0:   # reels: the first-frame title card from reel.json
            M=PJ.meta(ep)
            if M.get('title'):extra['title']={'text':M['title'],'sec':M.get('title_sec',2.5)}
        film.add(b['beat'],round(rel,2),sc,s.get('grade','cel'),cam=cam,cues=s.get('cues'),**{k2:v for k2,v in extra.items()})
        if s.get('cues'):
            for cw in s['cues']:
                bw=[norm(x[0]) for ln in b['lines'] for x in ln]
                if not any(x.startswith(norm(cw)) for x in bw):errs.append(f"{sid}: cue word '{cw}' is not in beat {b['beat']}")
    for b in beats:
        if b['beat'] not in firsts:errs.append(f"beat {b['beat']} has no shot")
    n=film.save(out_p)
    durs=[(shots[k+1][0] if k+1<len(shots) else total)-shots[k][0] for k in range(len(shots))]
    print(f'{n} shots -> {out_p}; average {sum(durs)/len(durs):.2f}s (rule 2.6–4.2), shortest {min(durs):.2f}s, longest {max(durs):.2f}s')
    for w in warns:print('WARN',w)
    for e in errs:print('ERROR',e)
    if errs:sys.exit(1)
if __name__=='__main__':main()
