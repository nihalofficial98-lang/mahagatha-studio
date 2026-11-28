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
KIND_BY_THEME={'forest':'forest_dusk','temple':'temple_dawn','sea':'sea_night','cosmos':'cosmos','lanka':'palace_night','palace':'palace_night','heaven':'heaven','battle':'battle_fire','village':'village_dusk','hills':'hills_night','ashram':'forest_dusk'}
KIND_BY_BG={'palace':'palace_night','council':'palace_night','garden':'forest_dusk','forest':'forest_dusk','dusk':'village_dusk','storm':'battle_fire','night':'hills_night','cloudscape':'heaven','vaikuntha':'heaven','sea':'sea_night','cosmos':'cosmos','kailash':'kailash','plain':'battle_fire','ashram':'forest_dusk'}
def layers(sc,theme='hills'):
    r=RIDGE[sc];sil=r[3];sil2=r[2];sk=SK[sc]
    snow=theme in('temple',)
    fars=[mtn(420,470,1.1,r[0],230,190,snow),mtn(550,478,.9,r[1],200,130),mtn(700,468,1.25,r[0],250,215,snow),mtn(835,480,.95,r[1],210,150),mtn(480,490,.6,r[1],160,90),cld(500,200,1.0,sk[2]),cld(790,250,.9,sk[2])]
    if theme=='sea':fars=[mtn(430,505,.8,r[1],260,60),mtn(840,508,.7,r[1],230,50),mtn(640,500,.5,r[0],180,40),cld(500,210,1.1,sk[2]),cld(790,260,1.0,sk[2])]
    if theme in('palace','heaven','lanka'):fars+=[{"o":"wall","x":600,"y":470,"s":.8,"col":sil2},{"o":"pillar","x":470,"y":525,"s":.5,"col":sil2},{"o":"pillar","x":560,"y":525,"s":.45,"col":sil2},{"o":"pillar","x":720,"y":525,"s":.45,"col":sil2},{"o":"pillar","x":810,"y":525,"s":.5,"col":sil2}]
    L=[far("layered dark mountains and distant clouds",fars,sk[3],.6)]
    ms=[ground(482,sil2,1100,12)]
    line=lambda kinds:[tree(x,508,.3+.05*((x//45)%3),kinds[(x//45)%len(kinds)],sil2) for x in range(405,880,45)]
    if theme in('forest','ashram'):ms+=line(['pine','banyan','palm'])+[tree(448,522,.7,"banyan",sil),tree(838,518,.66,"pine",sil),{"o":"hut","x":520,"y":528,"s":.4,"col":sil}]
    elif theme=='village':ms+=line(['palm','round'])+[{"o":"hut","x":462,"y":526,"s":.6,"col":sil},{"o":"hut","x":826,"y":524,"s":.55,"col":sil},{"o":"road","x":640,"y":560,"s":1.0,"col":sil2}]
    elif theme in('palace','heaven','lanka'):ms+=[{"o":"pillar","x":452,"y":545,"s":.8,"col":sil},{"o":"pillar","x":834,"y":545,"s":.8,"col":sil},{"o":"wall","x":640,"y":505,"s":.7,"col":sil2}]+line(['round','palm'])[:4]
    elif theme=='temple':ms+=[{"o":"pillar","x":455,"y":545,"s":.7,"col":sil},{"o":"pillar","x":830,"y":545,"s":.7,"col":sil},{"o":"rock","x":560,"y":525,"s":.7,"col":sil2},{"o":"rock","x":730,"y":525,"s":.6,"col":sil2}]
    elif theme=='battle':ms+=[{"o":"wall","x":500,"y":515,"s":.45,"col":sil},{"o":"wall","x":790,"y":515,"s":.4,"col":sil},{"o":"rock","x":450,"y":525,"s":.95,"col":sil},{"o":"rock","x":840,"y":520,"s":.85,"col":sil},{"o":"rock","x":640,"y":515,"s":.5,"col":sil2}]
    elif theme=='sea':ms+=[{"o":"rock","x":470,"y":528,"s":.5,"col":sil},{"o":"rock","x":820,"y":526,"s":.45,"col":sil}]
    else:ms+=line(['pine','round'])+[{"o":"rock","x":450,"y":522,"s":.9,"col":sil},{"o":"rock","x":840,"y":518,"s":.8,"col":sil}]
    L.append(mid("faded dark silhouettes of the place far behind the figures",ms,.5))
    nr=[{"o":"rock","x":432,"y":758,"s":.9,"col":'#0a0610'},{"o":"rock","x":852,"y":760,"s":.85,"col":'#0a0610'}]
    L.append(near("small low dark rocks at the very bottom corners, nothing in front of the faces",nr,.5))
    return L
THEMES=[('forest',r'\b(forest|wilderness|woods|ashram|mahendra|jungle|trees?)\b','forest'),('temple',r'\b(temple|shivling|lingam|kailash|chanted|worshipped|worship|thousand names|lotus eyes)\b','kailash'),('sea',r'\b(ocean|sea|river|narmada|waters?)\b','sea'),('cosmos',r'\b(universe|worlds?|fourteen|14|creation)\b','cosmos'),('lanka',r'\b(lanka|palace|throne|ravana)\b','palace'),('battle',r'\b(war|battle|spear|army|armies|enemies|weapons?|demons?|astra|arrow|fought|fighting)\b','plain'),('heaven',r'\b(heaven|gods|yajna|council|vaikuntha|lakshmi|indra)\b','palace'),('village',r'\b(village|people|families|relatives|travelers|locals|shambhala|home)\b',None)]
def background(sc):
    if sc in SK:return bg("vista",sky=SK[sc],sx=640,sy=300,ridge=RIDGE[sc],haze="200,160,170",dust=10)
    return bg(sc)
def scene_layers(sc,theme='hills'):return layers(sc if sc in SK else PAL.get(sc,'indigo'),theme)
GROUPS=[(r'\b(people|locals|travelers|villagers|families|relatives|devotees|crowd)\b',[('villager',-1,'namaste'),('villager_w',1,'namaste')]),
 (r'\b(gods|devas)\b',[('deva_thin',-1,'plead'),('deva_thin2',1,'plead')]),
 (r'\b(demons|enemies|army|asuras|rakshasas)\b',[('asura1',-1,'rage'),('asura2',1,'rage')]),
 (r'\b(sages|rishis|brahmins?)\b',[('rishi1',-1,'namaste'),('rishi2',1,'namaste')])]
GW={'people','locals','travelers','villagers','families','relatives','devotees','crowd','gods','devas','demons','enemies','army','asuras','rakshasas','sages','rishis'}
WALKRX=r'\b(walked|walking|wandering|wander|wandered|went|moved|entered|approached|came|comes|stopped him on the road|marched|ran)\b'
EMO=[('anger',r'\b(angry|furious|rage|cursed|curse|killed|kill|struck|attack|attacked|hit)\b'),('fear',r'\b(scared|afraid|fear|terrified|froze|trapped)\b'),('sad',r'\b(sad|pain|wound|wounded|blood|cried|wandering|lost|punishment)\b'),('surprise',r'\b(suddenly|shock|shocked|surprised|bright|jewels|amazing)\b'),('devotion',r'\b(pray|prayed|worship|worshipped|devotee|loved|blessed)\b'),('pride',r'\b(strong|strongest|powerful|beat|won|brave)\b'),('scheme',r'\b(trick|plan|idea|secret|mistake)\b'),('joy',r'\b(smiled|laughed|happy|gift)\b')]
POSE=[('sitpray',r'\b(prayed|worshipped|chanted|meditation)\b'),('sleep',r'\b(asleep|sleeping|slept)\b'),('plead',r'\b(begged|asked|forgive)\b'),('lunge',r'\b(killed|struck|attacked|threw|hit|drove|cut)\b'),('fall',r'\b(fell|collapsed|snapped)\b'),('namaste',r'\b(bowed|blessed)\b'),('point',r'\b(told|said|warned|named)\b'),('open',r'\b(spread|rose|appeared)\b')]
FX=[('ember_fire',r'\b(fire|flames|burned|burning|yajna|yagna)\b',(640,560,300)),('blood_splash',r'\b(blood)\b',(640,500,260)),('curse_glow',r'\b(curse|cursed)\b',(640,420,420)),('lightning_forks',r'\b(lightning|thunder|storm)\b',(640,260,500)),('smoke_plume',r'\b(smoke|ashes|ash)\b',(640,560,300)),('wave_ocean',r'\b(ocean|sea|water|river)\b',(640,640,640)),('divine_rays',r'\b(light|glowing|shine|bright|golden|divine)\b',(640,330,520)),('sudarshan_chakra',r'\b(chakra|disc)\b',(640,400,260)),('red_energy_pulse',r'\b(boon|power|powers|weapon|astra)\b',(640,420,300)),('mist_wisps',r'\b(night|dark|silent|mystery)\b',(640,540,640))]
EVENTS=[(r'\b(tore|pulled|plucked|placed)\b.*\beye\b|\beye\b.*\b(tore|pulled|plucked|placed)\b|\b(plucked|pulled) out his eye\b','selfcut','pain',[('blood_splash',640,330,150,1.0,False),('divine_rays',640,330,380,.7,True)]),
 (r'\b(cut off|snapped|whipped|beheaded|cut off vishnu)\b','fall','shock',[('blood_splash',640,360,200,.9,False),('red_energy_pulse',640,420,420,.6,True)]),
 (r'\bchakra\b|\bdisc\b','open','calm',[('sudarshan_chakra',640,330,320,1.0,False),('divine_rays',640,330,520,.6,True)]),
 (r'\b(spear)\b','lunge','anger',[('red_energy_pulse',640,420,380,.8,False),('blood_splash',640,520,220,.8,False)]),
 (r'\b(mountains?|peaks?)\b.*\b(threw|throw)|\bthrew mountains\b','throw','rage',[('mandara_mountain',640,330,360,.9,False),('smoke_plume',640,560,360,.6,False)]),
 (r'\b(prayed|worshipped|chanted)\b','sitpray','devotion',[('divine_rays',640,330,520,.6,True),('mist_wisps',640,560,640,.7,True)]),
 (r'\b(asleep|slept)\b','sleep','calm',[('mist_wisps',640,560,640,.8,True)]),
 (r'\b(curse|cursed)\b','point','anger',[('curse_glow',640,400,440,.9,False)]),
 (r'\b(jewels?|diamonds?|rubies|pearls?)\b','open','surprise',[('divine_rays',640,330,520,.8,True)]),
 (r'\b(fell|fall|crumbled)\b','fall','fear',[('ground_crack',640,640,520,.8,False)])]
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
    cfg=SP.SPEC[reel];G=Gen(reel);S=sentences(G.T);prev=None;scene=cfg.get('scene','indigo');ci=0;cam_end=(1.0,0,0);cur=None;lastchg=0
    for n,s in enumerate(S):
        txt=' '.join(w for _,w,_ in s);low=txt.lower();first=s[0][1].strip(',.?!"')
        for key,sc in cfg.get('scenes',[]):
            if (isinstance(key,int) and key==n) or (isinstance(key,str) and key in low and n>=cfg.get('_',0)):scene=sc
        # characters: lexicon words in the sentence, in order
        found=[]
        for m in re.finditer(r"[a-z']+",low):
            who=None if m.group(0) in GW else cfg['lex'].get(m.group(0))
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
        extras=[]
        for rx,gl in GROUPS:
            if re.search(rx,low):extras=gl;break
        evx=None
        for rx,ep,ee,efx in EVENTS:
            if re.search(rx,low):evx=(ep,ee,efx);break
        if evx:pose,emo=evx[0],evx[1]
        ch=[]
        xs={1:[640],2:[470,810],3:[380,640,900]}.get(len(who),[640])
        for k,w in enumerate(who):
            big=w in cfg.get('big',[]);sc_=cfg.get('scale',{}).get(w,.9)
            ch.append({"who":w,"x":xs[k],"y":690,"s":sc_*(0.85 if len(who)>1 else 1),"_face":.44 if len(who)==1 else .5,"flip":1 if k==0 and len(who)>1 else (-1 if k==1 else 1),"pose":pose if k==0 else 'stand',"emo":emo if k==0 else 'calm',"look":700,**({"prop":"none"} if w in ("hanuman","sugriva") else {})})
        if extras and len(ch)==1 and ch[0]['who'] not in [e for e,_,_ in extras]:
            ch[0]['s']=ch[0]['s']*.9
            for e_,sd,ps in extras:ch.append({"who":e_,"x":640+sd*140,"y":725,"s":.5,"_face":.64,"flip":-sd,"pose":ps,"emo":"calm","look":700})
        elif extras and not ch and prev:pass
        fxs=[]
        for k,rx,(x,y,wd) in FX:
            m=re.search(rx,low)
            if m and len(fxs)<2:
                wv=m.group(0)
                fxs.append(pfx(k,([w.strip(',.?!"') for _,w,_ in s if w.strip(',.?!"').lower()==wv] or [first])[0],x,y,wd,f"{k.replace('_',' ')} as the story says '{wv}'",alpha=.8,behind=k in('divine_rays','mist_wisps','red_energy_pulse')))
        if evx:
            wv=[w.strip(',.?!"') for _,w,_ in s][0]
            fxs=[pfx(k,wv,x,y,wd,f"{k.replace('_',' ')} showing what the narration says",alpha=a,behind=b) for k,x,y,wd,a,b in evx[2]][:3]
        mt=re.search(r'\b(lotus|lotuses)\b',low)
        if mt and cfg.get('autolotus') and not ('fx' in cfg.get('over',{}).get(n,{})):
            lw=([w.strip(',.?!"') for _,w,_ in s if w.strip(',.?!"').lower()==mt.group(0)] or [first])[0]
            fxs=[{"k":"lotus","word":lw,"x":640,"y":610,"sc":.8,"open":1,"meaning":"a paper-cut lotus placed where the story says lotus"}]+fxs[:1]
        extra_mid=[]
        if n in cfg.get('over',{}):
            o=cfg['over'][n]
            if 'chars' in o:
                ch=[dict(c_) for c_ in o['chars']];who=[c_['who'] for c_ in ch]
            if 'mid' in o:extra_mid=o['mid']
            if 'scene' in o:scene=o['scene']
            if 'fx' in o:fxs=[dict(f_,word=(f_['word'] or first)) for f_ in o['fx']]
        theme=cfg.get('theme','hills');bgk=None
        for th,rx,bk in THEMES:
            if re.search(rx,low):theme=th;bgk=bk;break
        want=(scene,theme,bgk)
        if n==0 or n in cfg.get('over',{}) and 'scene' in cfg['over'][n]:cur=want;lastchg=n
        elif want!=cur and n-lastchg>=2:cur=want;lastchg=n
        scene,theme,bgk=cur
        if cfg.get('over',{}).get(n,{}).get('bg'):bgk=cfg['over'][n]['bg']
        AMB={'forest':[('mist_wisps',640,600,640,.5,True)],'palace':[('ember_fire',466,664,70,.8,False),('ember_fire',818,664,70,.8,False)],'lanka':[('ember_fire',466,664,70,.8,False),('ember_fire',818,664,70,.8,False)],'temple':[('mist_wisps',640,600,640,.5,True),('ember_fire',470,668,60,.8,False)],'battle':[('smoke_plume',640,480,560,.3,True),('ember_fire',455,672,70,.7,False)],'sea':[('wave_ocean',640,690,640,.6,False)],'cosmos':[('divine_rays',640,330,560,.4,True)],'heaven':[('divine_rays',640,330,560,.4,True),('ember_fire',466,664,60,.7,False)],'village':[('smoke_plume',520,520,220,.35,True)],'hills':[('mist_wisps',640,600,640,.45,True)]}
        if len(fxs)<2 and not cfg.get('war') and theme in AMB:
            for k_,x_,y_,w_,a_,b_ in AMB[theme]:fxs.append(pfx(k_,first,x_,y_,w_,f"{k_.replace('_',' ')} giving the {theme} its atmosphere",alpha=a_,behind=b_))
        if cfg.get('war') and ch:
            hero_=ch[0]['who']
            for wx,wk,wp in cfg['war']:
                if wk==hero_:wk={'sugriva':'hanuman','hanuman':'sugriva'}.get(wk,'asura1')
                ch.append({"who":wk,"x":wx,"y":690,"s":.26,"_ground":True,"flip":1 if wx<640 else -1,"pose":wp,"emo":"anger","look":700})
            fxs=fxs[:1]+[pfx('ember_fire',None,452,672,95,'burning fire on the battlefield at the left',alpha=.8),pfx('ember_fire',None,830,672,95,'burning fire on the battlefield at the right',alpha=.8),pfx('smoke_plume',None,640,470,560,'war smoke over the battlefield',alpha=.3,behind=True)]
            fxs=[dict(f_,word=(f_.get('word') or first)) for f_ in fxs]
        kind_=KIND_BY_BG.get(bgk) if bgk else None
        kind_=kind_ or KIND_BY_THEME.get(theme,'hills_night')
        pal_=scene if scene in SK else PAL.get(scene,'indigo')
        fxs=[pfx('scene_kit',first,640,360,1280,'a full paper-cut landscape of the place where this happens',alpha=1,behind=True,kind=kind_,pal=pal_)]+[f_ for f_ in fxs if f_.get('k')!='scene_kit']
        cname,ca,cb,shs=CAMS[ci%len(CAMS)];ci+=1
        # planned camera (owner: dramatic, planned moves, not constant zoom): reveal first, impact shake on violent beats, push-in on tension, tilt/pull-out on calm, pull back to close
        tense=emo in ('anger','rage','fury','fear','horror','shock','pain');soft=emo in ('calm','devotion','sad','joy','love','pride')
        imp=bool(evx) or bool(re.search(r'\b(lightning|snapped|killed|struck|curse|cursed|fell|cut|spear|thunder|roar|boon)\b',low))
        z0=cam_end[0] if cam_end[0]<1.12 else 1.03;shk=0;rr=(0,0);shs='medium'
        if n==0:ca=(1.2,0,6);cb=(1.02,0,0);cname='pull_out';shs='wide';mot='reveal: pull back from a close start to show the whole place'
        elif n==len(S)-1:ca=(max(z0,1.1),0,0);cb=(1.0,0,0);cname='pull_out';shs='wide';mot='closing: slowly pull back as the story ends'
        elif imp:ca=(1.04,0,0);cb=(1.12,0,-4);cname='handheld';shk=2;rr=(0,.04 if ci%2 else -.04);mot='impact: handheld shake and a quick push as it happens'
        elif tense:ca=(z0,0,0);cb=(min(z0+.15,1.2),0,-6);cname='push_in';shs='close';rr=(0,.025 if ci%2 else -.025);mot='tension builds: a slow push toward the face with a slight tilt'
        elif soft and ci%3==0:ca=(1.05,0,12);cb=(1.05,0,0);cname='tilt_up';mot='calm: a slow tilt up to the figure and the sky'
        elif soft and ci%3==1:ca=(z0,0,0);cb=(1.0,0,0);cname='pull_out';shs='wide';mot='calm: a gentle pull back'
        else:ca=(z0,-10,0);cb=(z0+.04,10,0);cname='dolly_right' if ci%2 else 'dolly_left';mot='calm: a slow sideways drift'
        cam_end=cb
        trk=False
        if re.search(WALKRX,low) and ch and not cfg.get('war') and n not in cfg.get('over',{}) and ch[0]['who'] not in ('naga','vishnu_rest','shiva_lingam') and (s[-1][2]-s[0][2])>=1.8:
            trk=True;dur_=max(1.8,min(6.0,(S[n+1][0][2] if n+1<len(S) else s[-1][2]+1.5)-s[0][2]))
            ch[0]['x']=560;ch[0]['walk']={"word":first,"to_x":740,"d":round(dur_*.9,1),"speed":1};ch[0]['pose']='stand'
            for e_ in ch[1:]:e_['x']=e_['x']+30
            ca=(1.04,-50,0);cb=(1.04,70,0);cam_end=cb;cname='pan_right';shs='wide'
        sh={"id":"x","beat":1,"start":{"t":s[0][2],"word":first}};G.S.append(sh)
        sx=640
        sh.update(meaning=re.sub(r'\b(good|great|nice|very|something|anything)\b','it',txt+" (shown as a dark story frame)")[:110],why=re.sub(r'\b(something|anything|things?|stuff|good|great|nice|very)\b','it',f"{(who[0] if who else 'The scene')} in a dark {scene} world while '{txt[:50]}' is spoken."),
          camera=cam(cname,ca,cb,shs,"normal",shk,mot,rr),focus={"subject":who[0] if who else "scene","depth":"deep"},
          vertical={"focus":who[0]} if who else {},layers=[dict(l_,items=l_['items']+extra_mid) if l_['d']=='mid' else l_ for l_ in scene_layers(scene,theme)],background=(bg(bgk) if bgk and (not cfg.get('over',{}).get(n,{}).get('scene') or cfg.get('over',{}).get(n,{}).get('bg')) else (dict(background(scene),sx=sx) if scene in SK else background(scene))),mood={"emotion":emo,"grade":GRD},
          characters=ch,effects=fxs,transition_in="cut")
        ov=cfg.get('over',{}).get(n,{})
        if 'vertical' in ov:sh['vertical']=ov['vertical']
    G.finish()
    bp=f'/home/user/mahagatha-studio/reels/{reel}/briefs.json';bj=json.load(open(bp));bj['flow']=True;json.dump(bj,open(bp,'w'),ensure_ascii=False,indent=1)
if __name__=='__main__':main(sys.argv[1])
