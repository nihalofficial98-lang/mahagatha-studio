"""Reject vague or incomplete SHOT BRIEFS before anything is built.
  python3 studio/validate_brief.py NN [--brief episodes/epNN/briefs.json]    (reels: NN = reel02 / _test -> reels/<id>/briefs.json; 9:16 face rules)
Exit 1 and one line per problem if the brief is not ready. Schema: guides/SHOT_BRIEF.md (one object per shot).
Checks: every required field present and specific; words exist in the narration and the owner's voice timeline; 1.0-6.5 s;
camera move from the list with a motivation; >= 2 depth layers (far/mid/near) with objects and atmospheric fade on far;
cast, poses, emotions, effects and layer objects exist in the engine; every character acts or looks on a word;
faces stay above the subtitle band; consecutive shots do not repeat the same camera move or the same frame."""
import json,sys,os,re,argparse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import engine_vocab as V,project as PJ
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAGUE=re.compile(r'\b(nice|beautiful|good|cool|something|stuff|etc|appropriate|interesting|some kind|various|as needed|tbd|todo)\b',re.I)
SHOTS='wide medium close extreme_close insert two_shot ots pov low_angle high_angle top establishing'.split()
MOVES='push_in pull_out pan_left pan_right tilt_up tilt_down dolly_left dolly_right crane_up crane_down static handheld dutch orbit'.split()
LENS=['wide','normal','tele']
REQ=['id','beat','start','duration','narration','meaning','why','camera','focus','layers','background','mood','characters','effects','transition_in']
norm=lambda w:re.sub(r'[^\wऀ-ॿ]','',w)
def words_of(s):return [norm(w) for w in s.split() if norm(w)]
def has_word(ws,w):w=norm(w);return any(x==w or x.startswith(w) or w.startswith(x) for x in ws if x)
def text_ok(errs,sid,k,v,minlen=20):
    if not isinstance(v,str) or len(v.strip())<minlen:errs.append(f"{sid}: '{k}' must be a specific sentence (>= {minlen} chars)");return
    m=VAGUE.search(v)
    if m:errs.append(f"{sid}: '{k}' uses the vague word '{m.group(0)}': say exactly what is seen")
def face_cropped(f,cam):
    if f.get('who') in ('boar','swan'):return False
    s=f.get('s',1);x0,y0=f.get('x',640),f.get('y',500)
    if f.get('head'):top=y0-104*s;chin=y0+75*s
    else:cy=y0-300*s;top=cy-105*s;chin=cy+55*s
    for e in (cam.get('from',{}),cam.get('to',{})):
        z=e.get('z',1);sh=abs(e.get('y',0));t_=360+(top-360)*z-sh;c_=360+(chin-360)*z+sh;cx=640+(x0-640)*z
        if t_<2 or c_>590 or cx<20 or cx>1260:return True
    return False
def face_cropped_v(f,cam,vert):
    """9:16 reels: the face must sit in the portrait window above the subtitle band (64% of the height); stack mode frames faces itself"""
    if f.get('who') in ('boar','swan') or (vert or {}).get('mode')=='stack':return False
    s=f.get('s',1);y0=f.get('y',500);vz=max(1,(vert or {}).get('z',1));h=720/vz
    if f.get('head'):top=y0-104*s;chin=y0+75*s;fc=y0
    else:fc=y0-300*s;top=fc-105*s;chin=fc+55*s
    for e in (cam.get('from',{}),cam.get('to',{})):
        z=e.get('z',1);sy=lambda v:360+(v-360-e.get('y',0))*z
        w0=min(max(sy(fc)-(vert or {}).get('y',.36)*h,0),720-h) if vz>1 else 0
        if (sy(top)-w0)/h<.003 or (sy(chin)-w0)/h>.64:return True
    return False
def load_timeline(ep):
    p=f'{PJ.bdir(ep)}/timings.json'
    if not os.path.exists(p):return None
    T=json.load(open(p,encoding='utf-8'));out=[];off=0.0
    for b in T:
        out+=[(norm(w['text']),off+w['start']) for w in b['words']];off+=b['duration']
    return out
def check(brief,ep):
    errs=[];warn=[];tl=load_timeline(ep);prev=None;prev2=None;vert=PJ.fmt(ep)=='vertical'
    if tl is None:warn.append('no build/epNN/timings.json yet: start words not checked against the voice (run import_timestamps.py first)')
    ids=set()
    for i,s in enumerate(brief.get('shots',[])):
        sid=s.get('id',f'#{i}')
        if sid in ids:errs.append(f'{sid}: duplicate id')
        ids.add(sid)
        miss=[k for k in REQ if k not in s]
        if miss:errs.append(f"{sid}: missing {', '.join(miss)}");continue
        nw=words_of(s['narration'])
        if len(nw)<1:errs.append(f'{sid}: narration is empty (copy the exact spoken words of this shot)')
        for k in('meaning','why'):text_ok(errs,sid,k,s[k])
        st=s['start']
        if not isinstance(st,dict) or 'word' not in st or 't' not in st:errs.append(f"{sid}: start must be {{\"t\": seconds, \"word\": spoken word}}")
        else:
            if nw and not has_word(nw[:3],st['word']):errs.append(f"{sid}: start word '{st['word']}' is not among the first words of the narration")
            if tl is not None:
                near=[t for w,t in tl if has_word([w],st['word'])]
                if not near or min(abs(t-st['t']) for t in near)>.6:errs.append(f"{sid}: '{st['word']}' is not spoken at {st['t']}s in the voice")
        d=s['duration']
        if not isinstance(d,(int,float)) or not 1.0<=d<=6.5:errs.append(f'{sid}: duration {d} outside 1.0-6.5 s')
        c=s['camera'];cam={'from':c.get('from',{}),'to':c.get('to',{})}
        if c.get('shot') not in SHOTS:errs.append(f"{sid}: camera.shot must be one of {SHOTS}")
        if c.get('move') not in MOVES:errs.append(f"{sid}: camera.move must be one of {MOVES}")
        if c.get('lens') not in LENS:errs.append(f"{sid}: camera.lens must be one of {LENS}")
        text_ok(errs,sid,'camera.motivation',c.get('motivation'),15)
        if 'from' not in c or 'to' not in c:errs.append(f'{sid}: camera needs from/to {{z,x,y,r}}')
        for e in cam.values():
            if not .9<=e.get('z',1)<=3.1 or abs(e.get('x',0))>220 or abs(e.get('y',0))>220 or abs(e.get('r',0))>.08:errs.append(f'{sid}: camera value out of range {e}')
        fo=s['focus']
        if not fo.get('subject'):errs.append(f'{sid}: focus.subject (who/what the eye must land on)')
        L=s['layers'];ds=[l.get('d') for l in L] if isinstance(L,list) else []
        if len(ds)<2:errs.append(f'{sid}: needs at least 2 depth layers (far/mid/near), has {len(ds)}')
        for l in (L if isinstance(L,list) else []):
            if l.get('d') not in('far','mid','near'):errs.append(f"{sid}: layer d must be far, mid or near (got {l.get('d')})")
            text_ok(errs,sid,f"layers.{l.get('d')}.contents",l.get('contents'),10)
            if l.get('d') in('far','mid') and not l.get('items') and not l.get('from_background'):errs.append(f"{sid}: {l.get('d')} layer has no objects (add items, or from_background:true when the background itself draws this plane)")
            if l.get('d')=='far' and (l.get('fog',.55))<.3:errs.append(f'{sid}: far layer fog {l.get("fog")} < 0.3: far planes must fade (haze)')
            for it in l.get('items',[]):
                if it.get('o') not in V.OBJ:errs.append(f"{sid}: layer object '{it.get('o')}' unknown (use {V.OBJ})")
        bg=s['background']
        if bg.get('k') not in V.BG:errs.append(f"{sid}: background.k '{bg.get('k')}' unknown (use {V.BG})")
        ch=bg.get('change')
        if ch:
            if not ch.get('word') or not has_word(nw,ch['word']):errs.append(f'{sid}: background.change.word must be a word of the narration')
            if ch.get('bg2') and ch['bg2'].get('k') not in V.BG:errs.append(f"{sid}: background.change.bg2 unknown")
            if not ch.get('bg2') and not ch.get('to'):errs.append(f'{sid}: background.change needs bg2 (new background) or to (parameter values)')
        m=s['mood']
        if not m.get('emotion'):errs.append(f'{sid}: mood.emotion')
        if m.get('grade') not in V.GRADES and not str(m.get('grade','')).startswith('rgba('):errs.append(f"{sid}: mood.grade must be one of {V.GRADES} or rgba()")
        figs=[]
        for f in s['characters']:
            who=f.get('who')
            if who not in V.CAST:errs.append(f"{sid}: character '{who}' not in the cast (character-designer must add it first)");continue
            if f.get('pose') and who not in('boar','swan') and f['pose'] not in V.POSES:errs.append(f"{sid}: {who} pose '{f['pose']}' unknown")
            if f.get('emo') and f['emo'] not in V.EMO:errs.append(f"{sid}: {who} emo '{f['emo']}' unknown")
            if not f.get('emo') and not f.get('mood'):errs.append(f'{sid}: {who} needs emo or mood (a face must say something)')
            acts=f.get('actions',[])
            if not acts and not f.get('look') and not f.get('talk'):errs.append(f'{sid}: {who} does nothing: add an action on a word, a look, or talk')
            for a in acts:
                if not a.get('word') or not has_word(nw,a['word']):errs.append(f"{sid}: {who} action word '{a.get('word')}' not in the narration")
                if a.get('pose') and a['pose'] not in V.POSES:errs.append(f"{sid}: {who} action pose '{a['pose']}' unknown")
                if a.get('emo') and a['emo'] not in V.EMO:errs.append(f"{sid}: {who} action emo '{a['emo']}' unknown")
                if not any(k in a for k in('pose','emo','mood','tilt','look','turn','walk_to')):errs.append(f'{sid}: {who} action on {a.get("word")} changes nothing')
            for k_,w_ in (f.get('engine_cues') or {}).items():
                if not has_word(nw,w_):errs.append(f"{sid}: {who} engine cue {k_} word '{w_}' not in the narration")
            if f.get('walk') and not has_word(nw,f['walk'].get('word','')):errs.append(f'{sid}: {who} walk.word not in narration')
            if vert:
                foc=(s.get('vertical') or {}).get('focus') or fo.get('subject')
                if face_cropped_v(f,cam,s.get('vertical')):(errs if who==foc else warn).append(f"{sid}: {who} face cropped or inside the 9:16 subtitle band (y={f.get('y')}, s={f.get('s')}, vertical={s.get('vertical')})")
            elif face_cropped(f,cam):errs.append(f"{sid}: {who} face cropped or inside the subtitle band (x={f.get('x')}, y={f.get('y')}, s={f.get('s')})")
            figs.append(who)
        for e in s['effects']:
            k=e.get('k') or e.get('t')
            if k not in V.PFX and k not in V.FX:errs.append(f"{sid}: effect '{k}' unknown (pfx: {V.PFX}; engine fx: {V.FX})")
            if e.get('word') and not has_word(nw,e['word']):errs.append(f"{sid}: effect word '{e['word']}' not in the narration")
            text_ok(errs,sid,f'effects.{k}.meaning',e.get('meaning'),10)
        vt=s.get('vertical') or {}
        if vert and vt.get('mode')=='stack' and len([w for w in (vt.get('stack') or figs[:2]) if w in figs])<2:errs.append(f"{sid}: vertical stack needs two characters of this shot (vertical.stack)")
        if vert and vt.get('focus') and isinstance(vt['focus'],str) and vt['focus'] not in figs:errs.append(f"{sid}: vertical.focus '{vt['focus']}' is not a character of this shot")
        if s['transition_in'] not in V.TRANS:errs.append(f"{sid}: transition_in must be one of {V.TRANS}")
        if not figs and not s['effects'] and len(L)<3:errs.append(f'{sid}: empty frame (no character, no effect, fewer than 3 layers)')
        key=(bg.get('k'),tuple(sorted(figs)),c.get('shot'))
        if prev and prev[0]==c.get('move') and c.get('move')!='static':errs.append(f"{sid}: same camera move '{c.get('move')}' as the previous shot")
        if prev and prev2 and prev[1]==key and prev2[1]==key:errs.append(f'{sid}: third shot in a row with the same background, cast and framing')
        prev2=prev;prev=(c.get('move'),key)
    return errs,warn
def main():
    a=argparse.ArgumentParser();a.add_argument('ep');a.add_argument('--brief');x=a.parse_args()
    p=x.brief or f'{PJ.edir(x.ep)}/briefs.json';b=json.load(open(p,encoding='utf-8'))
    errs,warn=check(b,x.ep)
    for w in warn:print('WARN',w)
    for e in errs:print('ERROR',e)
    print(f"{len(b.get('shots',[]))} shots, {len(errs)} errors");sys.exit(1 if errs else 0)
if __name__=='__main__':main()
