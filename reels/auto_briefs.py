#!/usr/bin/env python3
"""Auto-director for reels: python3 reels/auto_briefs.py reelNN  (spec in reels/auto_specs.py)
One shot per sentence (long ones are split at commas). Characters come from a per-reel lexicon (who is named in the sentence),
emotion/pose/effects from keyword tables, scene from per-reel scene rules; look = dark indigo / brown / red.
Writes reels/<id>/briefs.json through briefs_lib.Gen (hero faces solved to the 9:16 frame), then validate_brief."""
import sys,re,json
sys.path.insert(0,'/home/user/mahagatha-studio/reels')
from briefs_lib import *
import auto_specs as SP
IND=['#0e0820','#2a1850','#5a2a58','#b05a48'];EMB=['#12060c','#3a1018','#7a2020','#b04a28'];BRN=['#100a08','#2e1c14','#5e3a24','#9a6a3c'];NITE=['#06060e','#101a38','#24366a','#5a70b0'];TEAL=['#06101a','#12303a','#2a6a6a','#8ac0b0']
SK={'indigo':IND,'ember':EMB,'brown':BRN,'night':NITE,'teal':TEAL}
RIDGE={'indigo':['#3a2a5a','#2e2048','#241838','#1a1028'],'ember':['#6a2a2a','#521e22','#3a1618','#2a0e10'],'brown':['#6a4a34','#523a28','#3a281c','#2a1c12'],'night':['#2a3a6a','#202e56','#18224a','#101830'],'teal':['#2a5a5a','#204a4a','#183a3a','#102a2a']}
GRD='ep07_dark'
def layers(sc):
    r=RIDGE[sc];far_c=r[0];gr=r[2];rk=r[3]
    return [far("dark far peaks and haze",[mtn(470,470,1.0,far_c,260,160),mtn(840,480,.9,far_c,240,140),cld(520,220,1.1,SK[sc][2])],SK[sc][3],.55),
            mid("dark ground with rocks",[ground(480,gr,1100,12),{"o":"rock","x":430,"y":520,"s":.8,"col":rk},{"o":"rock","x":860,"y":516,"s":.7,"col":rk}],.2),
            near("dark rocks low in the corners",[{"o":"rock","x":440,"y":752,"s":1.6,"col":'#120a10'},{"o":"rock","x":840,"y":756,"s":1.5,"col":'#120a10'}],.5)]
def background(sc):
    if sc in SK:return bg("vista",sky=SK[sc],sx=640,sy=300,ridge=RIDGE[sc],haze="200,160,170",dust=10)
    return bg(sc)
def scene_layers(sc):return layers(sc if sc in SK else PAL.get(sc,'indigo'))
EMO=[('anger',r'\b(angry|furious|rage|cursed|curse|killed|kill|struck|attack|attacked|hit)\b'),('fear',r'\b(scared|afraid|fear|terrified|froze|trapped)\b'),('sad',r'\b(sad|pain|wound|wounded|blood|cried|wandering|lost|punishment)\b'),('surprise',r'\b(suddenly|shock|shocked|surprised|bright|jewels|amazing)\b'),('devotion',r'\b(pray|prayed|worship|worshipped|devotee|loved|blessed)\b'),('pride',r'\b(strong|strongest|powerful|beat|won|brave)\b'),('scheme',r'\b(trick|plan|idea|secret|mistake)\b'),('joy',r'\b(smiled|laughed|happy|gift)\b')]
POSE=[('sitpray',r'\b(prayed|worshipped|chanted|meditation)\b'),('sleep',r'\b(asleep|sleeping|slept)\b'),('plead',r'\b(begged|asked|forgive)\b'),('lunge',r'\b(killed|struck|attacked|threw|hit|drove|cut)\b'),('fall',r'\b(fell|collapsed|snapped)\b'),('namaste',r'\b(bowed|blessed)\b'),('point',r'\b(told|said|warned|named)\b'),('open',r'\b(spread|rose|appeared)\b')]
FX=[('ember_fire',r'\b(fire|flames|burned|burning|yajna|yagna)\b',(640,560,300)),('flower_petals',r'\b(lotus|lotuses|flower|flowers)\b',(640,420,420)),('blood_splash',r'\b(blood)\b',(640,500,260)),('curse_glow',r'\b(curse|cursed)\b',(640,420,420)),('lightning_forks',r'\b(lightning|thunder|storm)\b',(640,260,500)),('smoke_plume',r'\b(smoke|ashes|ash)\b',(640,560,300)),('wave_ocean',r'\b(ocean|sea|water|river)\b',(640,640,640)),('divine_rays',r'\b(light|glowing|shine|bright|golden|divine)\b',(640,330,520)),('sudarshan_chakra',r'\b(chakra|disc)\b',(640,400,260)),('red_energy_pulse',r'\b(boon|power|powers|weapon|astra)\b',(640,420,300)),('mist_wisps',r'\b(night|dark|silent|mystery)\b',(640,540,640))]
CAMS=[("push_in",(1.0,0,0),(1.07,0,-6),"medium"),("pull_out",(1.1,0,-6),(1.0,0,0),"close"),("pan_left",(1.04,22,0),(1.04,-22,0),"medium"),("tilt_up",(1.0,0,10),(1.06,0,0),"wide"),("pan_right",(1.04,-22,0),(1.04,22,0),"close"),("pull_out",(1.08,0,-4),(1.0,0,0),"wide"),("dolly_right",(1.0,-14,0),(1.06,14,-6),"close")]
PAL={'kailash':'night','vaikuntha':'indigo','cosmos':'night','sea':'teal','forest':'teal','ashram':'brown','palace':'ember','yagna':'ember','plain':'ember','dusk':'ember','dawn':'brown','storm':'night','night':'night'}
def sentences(words):
    out=[];cur=[]
    for i,(w,t) in enumerate(words):
        cur.append((i,w,t))
        if re.search(r'[.?!]$',w):out.append(cur);cur=[]
    if cur:out.append(cur)
    res=[]
    for s in out:   # split long sentences at a comma after 9+ words
        if s[-1][2]-s[0][2]>5.2 and len(s)>12:
            mid=len(s)//2;best=min(range(4,len(s)-4),key=lambda j:(0 if s[j][1].endswith((',',';')) else 1,abs(j-mid)));res+=[s[:best+1],s[best+1:]]
        elif len(s)>20:
            for j,(i,w,t) in enumerate(s):
                if j>=9 and w.endswith(',') and len(s)-j>6:res+= [s[:j+1],s[j+1:]];break
            else:res.append(s)
        else:res.append(s)
    m=[]
    for i,s in enumerate(res):
        end=res[i+1][0][2] if i+1<len(res) else s[-1][2]+.5
        if m and (m[-1][1]):  # previous was too short: merge this into it
            m[-1][0]+=s;m[-1][1]=False;continue
        m.append([list(s),(end-s[0][2])<1.25 and i+1<len(res)])
    return [x[0] for x in m]
def main(reel):
    cfg=SP.SPEC[reel];G=Gen(reel);S=sentences(G.T);prev=None;scene=cfg.get('scene','indigo');ci=0
    for n,s in enumerate(S):
        txt=' '.join(w for _,w,_ in s);low=txt.lower();first=s[0][1].strip(',.?!"')
        for key,sc in cfg.get('scenes',[]):
            if (isinstance(key,int) and key==n) or (isinstance(key,str) and key in low and n>=cfg.get('_',0)):scene=sc
        # characters: lexicon words in the sentence, in order
        found=[]
        for m in re.finditer(r"[a-z']+",low):
            who=cfg['lex'].get(m.group(0))
            if who and who not in [f for f,_ in found]:found.append((who,m.start()))
        who=[f for f,_ in found][:cfg.get('maxc',2)]
        if not who and prev:who=prev[:1]
        if n in cfg.get('over',{}) and 'who' in cfg['over'][n]:who=cfg['over'][n]['who']
        prev=who or prev
        emo='calm'
        for e,rx in EMO:
            if re.search(rx,low):emo=e;break
        pose='stand'
        for p,rx in POSE:
            if re.search(rx,low):pose=p;break
        ch=[]
        xs={1:[640],2:[470,810],3:[380,640,900]}.get(len(who),[640])
        for k,w in enumerate(who):
            big=w in cfg.get('big',[]);sc_=cfg.get('scale',{}).get(w,.9)
            ch.append({"who":w,"x":xs[k],"y":690,"s":sc_*(0.85 if len(who)>1 else 1),"_face":.44 if len(who)==1 else .5,"flip":1 if k==0 and len(who)>1 else (-1 if k==1 else 1),"pose":pose if k==0 else 'stand',"emo":emo if k==0 else 'calm',"look":700})
        fxs=[]
        for k,rx,(x,y,wd) in FX:
            m=re.search(rx,low)
            if m and len(fxs)<2:
                wv=m.group(0)
                fxs.append(pfx(k,([w.strip(',.?!"') for _,w,_ in s if w.strip(',.?!"').lower()==wv] or [first])[0],x,y,wd,f"{k.replace('_',' ')} as the story says '{wv}'",alpha=.8,behind=k in('divine_rays','mist_wisps','red_energy_pulse')))
        if n in cfg.get('over',{}):
            o=cfg['over'][n]
            if 'scene' in o:scene=o['scene']
            if 'fx' in o:fxs=o['fx']
        cname,ca,cb,shs=CAMS[ci%len(CAMS)];ci+=1
        sh={"id":"x","beat":1,"start":{"t":s[0][2],"word":first}};G.S.append(sh)
        sx=[640,520,760,600,700][n%5]
        for c_ in ch:c_['x']=c_['x']+(sx-640)//4;
        for c_ in ch:
            if len(ch)==1 and n%2:c_['flip']=-1
        sh.update(meaning=re.sub(r'\b(good|great|nice|very|something|anything)\b','it',txt+" (shown as a dark story frame)")[:110],why=re.sub(r'\b(something|anything|things?|stuff|good|great|nice|very)\b','it',f"{(who[0] if who else 'The scene')} in a dark {scene} world while '{txt[:50]}' is spoken."),
          camera=cam(cname,ca,cb,shs,"normal",0,"a slow move that follows the story beat"),focus={"subject":who[0] if who else "scene","depth":"deep"},
          vertical={"focus":who[0]} if who else {},layers=scene_layers(scene),background=dict(background(scene),sx=sx) if scene in SK else background(scene),mood={"emotion":emo,"grade":GRD},
          characters=ch,effects=fxs,transition_in="cut" if n else "fade")
    G.finish()
if __name__=='__main__':main(sys.argv[1])
