"""Single source of truth for what the engine can draw, read straight from the engine source (so docs, briefs and
validators never drift from the code).  python3 studio/engine_vocab.py  -> prints the vocabulary as JSON."""
import os,re,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));E=R+'/engine/'
rd=lambda f:open(E+f,encoding='utf-8').read()
def _cast():
    m=re.search(r"V2NAMES=new Set\(\[(.*?)\.\.\.",rd('v2_cast.js'),re.S)
    return sorted(set(re.findall(r"'(\w+)'",m.group(1)))|{f'rishi{i}' for i in range(7)}|{'boar','swan','ketaki'})
def _pfx():return re.findall(r"^ (\w+):\{s:",rd('paper_fx.js'),re.M)
def _obj():
    s=rd('paper_scenes.js');a=s.index('const OBJ={');b=s.index('\n};',a)
    return re.findall(r"^ (\w+)\(x,y,s,t,o\)",s[a:b],re.M)
def _poses():
    s=rd('v2_cast.js');a=s.index('const PZ={');b=s.index('const poseOf=')
    return sorted(set(re.findall(r"^ (\w+):\{",s[a:b],re.M))|set(re.findall(r"PZ\.(\w+)=",s[a:b])))
def _emo():
    m=re.search(r"const EMO=\{(.*?)\};",rd('scenes.js'),re.S);return re.findall(r"(\w+):\{",m.group(1))
def _bgf():
    m=re.search(r"window\.BGF=\{(.*?)\n\};",rd('paper_scenes.js'),re.S);return re.findall(r"^ (\w+):",m.group(1),re.M)
CAST=_cast();PFX=_pfx();OBJ=_obj();POSES=_poses();EMO=_emo();FORE=_bgf()
BG='vista cloudscape earth pillar cel storm voidR night dusk moon palace dawn amber cosmos sea plain yagna kailash garden cosmicsea vaikuntha'.split()
BANNED_FX={'heart','sparkle','fximg'}   # owner rule: no hearts, stars, sparkles; fximg = legacy alias of pfx
FX=sorted((set(re.findall(r"k==='(\w+)'",rd('scenes.js')))|set(re.findall(r'FXV2\.(\w+)=',''.join(rd(f) for f in ('v2_scenes.js','paper_fx.js')))))-BANNED_FX)
GRADES='cel warm red night pal cool dark amb earth void'.split()
TRANS=['cut','fade','wipe','iris','flash']
MOOD_KEYS='smile sad surp anger mouth lx ly blink turn'.split()
if __name__=='__main__':
    print(json.dumps(dict(cast=CAST,pfx=PFX,objects=OBJ,poses=POSES,emo=EMO,backgrounds=BG,foreground_auto=FORE,fx=FX,grades=GRADES,transitions=TRANS,mood=MOOD_KEYS),ensure_ascii=False,indent=1))
