"""EP07 (Kacha Steals the Secret of the Dead) - DARK CINEMATIC look sheets for owner approval: the five dark places with
silhouette crowds and depth layers, expression strips (love, scheming, fear, fury, grief, laughing while crying, horror, cold
smile, pain without rage, shock), the story poses, the asuras, the props and Shukracharya's tearing / Kacha's rising.
Every frame uses the look preset grade 'ep07_dark' (tint + vignette + matte firelit figures).
  python3 library/showcase/ep07_cast/sheets.py [frame names ...]  -> library/showcase/ep07_cast/<name>.jpg
Per-character face/pose sheets: python3 studio/cast_sheet.py kacha devayani shukracharya brihaspati asura1 asura2 asura3 indra"""
import os,sys,json,subprocess,shutil
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))));sys.path.insert(0,R+'/studio')
import build as B
from PIL import Image
OUT=os.path.dirname(os.path.abspath(__file__))
LC='#f2dcb4'
def lab(s,x,y,size=17,col=LC):return {'t':'text','s':s,'x':x,'y':y,'size':size,'col':col}
def F(who,x,y,s=.8,**k):d={'who':who,'x':x,'y':y,'s':s};d.update(k);return d
def P(k,x,y,w,**o):d={'t':'pfx','k':k,'x':x,'y':y,'w':w};d.update(o);return d
DARKPAPER={'k':'plain','cols':['#1a0c0a','#2a1410','#3a1c12'],'fore':False}
SHADOW={'filt':'brightness(.07) saturate(0)','rim':'rgba(255,140,70,.55)','halo':False}   # Brihaspati as a shadow at night
HAZE='#5a2414'
CROWD_FAR={'d':'far','fog':.45,'haze':HAZE,'blur':1.4,'items':[{'o':'demons','x':640,'y':560,'s':.62,'n':20,'w':1500,'seed':4}]}
CROWD_MID={'d':'mid','fog':.12,'haze':HAZE,'items':[{'o':'demons','x':230,'y':640,'s':.95,'n':4,'w':360,'seed':8},{'o':'demons','x':1060,'y':640,'s':.95,'n':4,'w':360,'seed':12}]}

FACES=[('love','love',0),('secret scheming','scheme',.06),('fear','fear',-.05),('fury','fury',0),('grief','grief',.1),
       ('laughing while crying','laughcry',-.08),('horror','horror',0),('cold smile','coldsmile',.07),('pain (no rage)','pain',.1),('shock','shock',-.04)]
def strip(who,title,s=.78,picks=None):
    items=[f for f in FACES if not picks or f[1] in picks];cols=5;figs=[]
    for i,(l,e,tl) in enumerate(items):
        x=150+(i%cols)*245;y=215+(i//cols)*335
        figs.append((l,F(who,x,y,s,head=True,emo=e,tilt=tl)))
    return dict(title=title,bg=DARKPAPER,figs=figs,hlab=118)

FRAMES={
 # ---------- the five dark places ----------
 'scene_ashram':dict(title='ashram at dusk (bg k:"ashram"): Kacha asks to be a student; the guru ties the sacred thread; Devayani watches from the doorway',
   bg={'k':'ashram'},layers=[{'d':'far','fog':.4,'haze':'#5a2a1e','items':[{'o':'stree','x':560,'y':520,'s':.55,'h':420},{'o':'stree','x':880,'y':520,'s':.5,'h':380}]}],figs=[
   ('Devayani (love)',F('devayani',250,610,.6,emo='love',flip=1,tilt=.06)),
   ('Kacha kneels, wrist offered',F('kacha',560,660,.74,pose='kneel',emo='calm',flip=1)),
   ('Shukracharya ties the thread',F('shukracharya',820,665,.78,pose='hold',emo='calm',flip=-1))]),
 'scene_kacha_room_night':dict(title='Kacha\'s room at night (bg k:"kacha_room_night"): oil lamp, mat, bed, small barred window; Brihaspati comes as a SHADOW every night',
   bg={'k':'kacha_room_night'},figs=[
   ('Kacha (secret: "not yet, father")',F('kacha',520,640,.74,pose='sit',emo='scheme',flip=1)),
   ('Brihaspati as a shadow (filt brightness .07 + ember rim)',dict(F('brihaspati',860,665,.8,emo='calm',flip=-1,tilt=-.05),**SHADOW))]),
 'scene_feasthall':dict(title='demon feast hall (bg k:"feasthall"): far + mid silhouette crowd layers (o:"demons"), ring of red eyes; the guru halts them',
   bg={'k':'feasthall'},layers=[CROWD_FAR,CROWD_MID],figs=[
   ('asura (feaster, cup)',F('asura3',150,690,.72,emo='fury',flip=1,pose='grasp')),
   ('Kacha: "Shall I tell you a secret?"',F('kacha',470,675,.72,prop='cup',pose='raise',emo='scheme',flip=1,ash=0)),
   ('Shukracharya: "Halt!"',F('shukracharya',830,680,.76,pose='raise',emo='fury',flip=-1)),
   ('asura (brute)',F('asura1',1120,690,.7,emo='fury',flip=-1,pose='grasp'))]),
 'scene_forest':dict(title='forest at dawn, smoke (bg k:"forest"): Kacha lights a fire and waits; the circle of demons closes and blots out the sun',
   bg={'k':'forest','smoke':.9},layers=[{'d':'far','fog':.5,'haze':'#6a3a24','items':[{'o':'demons','x':640,'y':590,'s':.7,'n':14,'w':1400,'seed':31}]},
     {'d':'mid','fog':.1,'haze':HAZE,'items':[{'o':'smoke','x':640,'y':600,'s':1,'w':1800,'h':90,'col':'#2a1610','a':.6},{'o':'demons','x':170,'y':690,'s':1.15,'n':3,'w':280,'seed':41},{'o':'demons','x':1120,'y':690,'s':1.15,'n':3,'w':300,'seed':45}]}],
   figs=[('the guru\'s horses graze',F('horse',1000,640,.55,pose='bow',flip=-1)),('Kacha kneels by the fire, body shakes, soul calm',F('kacha',560,680,.74,pose='kneel',emo='pain',flip=1,tilt=.08))],
   fx=[P('ember_fire',740,670,120)]),
 'scene_council':dict(title='council in heaven, dim gold-brown (bg k:"council"): Brihaspati, grave: "Mritasanjivani." Indra: "You want us to steal it?"',
   bg={'k':'council'},figs=[('Brihaspati (grave)',F('brihaspati',420,665,.8,emo='doubt',pose='point',flip=1,mood={'smile':0,'sad':.35,'ly':.2})),
     ('Indra (shock)',F('indra',840,665,.8,emo='shock',pose='open',flip=-1))]),
 # ---------- expression strips ----------
 'faces_kacha':strip('kacha','Kacha - expressions (head tilt with tilt)'),
 'faces_devayani':strip('devayani','Devayani - expressions; laughing while crying = emo laughcry'),
 'faces_shukracharya':strip('shukracharya','Shukracharya - expressions; horror = emo horror'),
 'faces_brihaspati':strip('brihaspati','Brihaspati and Indra - grave council faces',picks=('scheme','fear','fury','grief','shock','pain','coldsmile')),
 # ---------- poses ----------
 'poses_ep07':dict(title='EP07 poses: kneel, sing, sleep, collapse, hug, run, grasp, catch, fall (+ bow, point exist)',bg={'k':'ashram','fire':False},figs=[
   ('kneel',F('kacha',95,650,.6,pose='kneel',emo='calm')),('sing (hymns)',F('kacha',255,650,.6,pose='sing',emo='love',talk=.6,tilt=-.08)),
   ('sleep',F('kacha',460,650,.5,pose='sleep')),('collapse',F('kacha',660,650,.6,pose='collapse',emo='fear')),
   ('run',F('devayani',820,650,.6,pose='run',emo='fear')),('grasp',F('asura2',990,650,.6,pose='grasp',emo='fury')),
   ('fall',F('shukracharya',1170,650,.6,pose='fall',emo='pain'))]),
 'poses_ep07b':dict(title='hug ("Kacha!" she held him), catch (the mantra falls, Kacha catches it), bow, point, guru seated chanting',bg={'k':'ashram','fire':False},figs=[
   ('',F('kacha',280,665,.68,emo='coldsmile',flip=-1,pose='stand')),('Devayani hugs Kacha (laughcry)',F('devayani',215,660,.66,pose='hug',emo='laughcry',flip=1)),
   ('catch (prop leaf)',F('kacha',520,665,.68,pose='catch',prop='leaf',glow=.6,emo='scheme')),('bow',F('devayani',710,660,.66,pose='bow',emo='shame')),
   ('point (curse)',F('devayani',900,660,.66,pose='point',emo='fury')),('seated, chanting',F('shukracharya',1130,650,.66,pose='sitpray',mood={'blink':1,'mouth':.3}))]),
 # ---------- the guru torn open / Kacha rises (tasteful: light through cracks, dark-red paper) ----------
 'guru_rise':dict(title='Shukracharya chants: tear 0..1 = cracks of light (eye, navel, chest, skull), the body shakes; no gore, light from inside',
   bg={'k':'ashram','fire':False},figs=[
   ('seated, chanting (tear 0)',F('shukracharya',200,690,.95,pose='sit',mood={'blink':1,'mouth':.35})),
   ('tear .35: the eye',F('shukracharya',640,690,.95,pose='sit',tear=.35,emo='pain')),
   ('tear .9: eye, navel, chest, skull',F('shukracharya',1080,690,.95,pose='sit',tear=.9,emo='pain'))]),
 'guru_rise2':dict(title='rise 0..1: the body opens like a cocoon and Kacha rises (kmood = his face), dark-red paper splashes; then Devayani holds him',
   bg={'k':'ashram','fire':False},figs=[
   ('rise .45',F('shukracharya',220,690,.9,pose='sitpray',rise=.45,emo='pain')),
   ('rise 1: drenched in blood',F('shukracharya',640,690,.9,pose='sitpray',rise=1,kmood={'smirk':.5,'blink':.3})),
   ('',F('kacha',1080,690,.74,emo='coldsmile',flip=-1)),('"Kacha!" (hug, laughcry)',F('devayani',1010,680,.72,pose='hug',emo='laughcry',flip=1))],
   fx=[P('blood_splash',640,690,300)]),
 'guru_rise_lying':dict(title='B17 (owner note): the torn body LIES on the ground while Kacha rises out of it (pose sleep + rise 0..1, mat:false)',
   bg={'k':'ashram','fire':False},figs=[
   ('Devayani (horror)',F('devayani',150,660,.7,emo='horror',flip=1)),
   ('rise .4',F('shukracharya',470,640,.66,pose='sleep',mat=False,rise=.4)),
   ('rise 1: Kacha stands out of the body',F('shukracharya',930,640,.66,pose='sleep',mat=False,rise=1,kmood={'smirk':.5,'blink':.3}))]),
 'guru_after':dict(title='after: the guru lies dead (sleep, mat:false + blood_splash); revived, he sees the mantra, no rage, only pain, and falls',
   bg={'k':'ashram','fire':False},figs=[
   ('the guru lies torn (sleep)',F('shukracharya',260,650,.6,pose='sleep',mat=False)),
   ('Kacha reads the mantra over him',F('kacha',540,665,.7,pose='catch',prop='leaf',glow=1,emo='coldsmile',flip=-1)),
   ('Shukracharya: pain, no rage',F('shukracharya',800,665,.7,emo='pain')),('...and he falls',F('shukracharya',1100,665,.7,pose='fall',emo='pain',bow=-.5))],
   fx=[P('blood_splash',260,640,300)]),
 # ---------- asuras + crowd ----------
 'asuras':dict(title='asuras: asura1 (brute, mace), asura2 (swordsman), asura3 (feaster, wine cup); clawed feet, red eyes; silhouette crowd behind',
   bg={'k':'feasthall','crowd':False,'fore':False},layers=[CROWD_FAR],figs=[
   ('asura1',F('asura1',230,670,.74,emo='fury')),('asura2',F('asura2',520,670,.74,emo='scheme',pose='point')),('asura3',F('asura3',800,670,.74,emo='joy',mood={'laugh':.8})),
   ('reaching for his throat',F('asura2',1080,670,.74,pose='grasp',emo='fury',flip=-1))]),
 'crowd_layers':dict(title='silhouette crowd helper: layer object "demons" (far + mid, fog/haze) and pfx demon_crowd (rows); ember eyes, horns, weapons, sizes, sway',
   bg={'k':'feasthall','crowd':False,'table':False,'fore':False},layers=[CROWD_FAR],figs=[('Kacha surrounded: a ring of red eyes',F('kacha',640,690,.72,emo='fear',mood={'wide':.6}))],
   fxb=[P('demon_crowd',640,650,1500,rows=2,n=7,seed=50,sc=.95)]),
 # ---------- props ----------
 'props':dict(title='EP07 props (pfx + hand props): wine cup with ash swirl, burnt cloth, mantra palm leaf, wild flowers, ember fire, curse glow, blood, ash speck, smoke',
   bg=DARKPAPER,figs=[('sacred thread on the wrist (kacha)',F('kacha',1130,250,.36,head=True,emo='calm')),('',F('kacha',1150,680,.6,pose='raise',emo='calm'))],fx=[
   P('wine_cup',130,220,110,ash=1),lab('wine_cup (ash 1)',130,330),P('burnt_cloth',340,200,90),lab('burnt_cloth',340,330),
   P('palm_leaf',580,210,190,glow=.8),lab('palm_leaf (glow)',580,260),P('wild_flowers',800,220,70),lab('wild_flowers',800,330),
   P('ember_fire',130,560,130),lab('ember_fire',130,620),P('curse_glow',370,500,200),lab('curse_glow',370,620),P('curse_glow',590,500,160,col='violet'),lab('curse_glow col violet',590,620),
   P('blood_splash',790,520,220),lab('blood_splash',790,620),P('ash_speck',960,240,40),lab('ash_speck',960,330),P('sacred_thread',1000,520,150),lab('sacred_thread',1000,620),
   P('smoke_bank',640,700,1300,h=70,col='#3a2018'),
   ]),
 'animals':dict(title='horse (the guru\'s horses: bay, dark mane, no necklace) and deer (burned for the wine), pose stand / bow (graze) / run',bg={'k':'forest'},figs=[
   ('horse',F('horse',230,640,.6)),('horse grazing (bow)',F('horse',620,640,.6,pose='bow')),('deer',F('deer',980,640,.75)),('deer run',F('deer',1180,640,.55,pose='run',flip=-1))]),
 'lineup':dict(title='EP07 cast line-up in the ep07_dark look',bg={'k':'ashram'},figs=[
   ('Kacha',F('kacha',120,665,.72,emo='calm')),('Devayani',F('devayani',280,665,.72,emo='love')),('Shukracharya',F('shukracharya',450,665,.72,emo='calm')),('Brihaspati',F('brihaspati',630,665,.72,emo='doubt')),
   ('Indra',F('indra',800,665,.72,emo='calm')),('asura1',F('asura1',970,665,.66,emo='anger')),('asura2',F('asura2',1100,665,.66,emo='anger')),('asura3',F('asura3',1210,665,.62,emo='anger',flip=-1))]),
}

def shot(T,fr):
    figs=[f for _,f in fr['figs']]+fr.get('extra',[]);lc=fr.get('labcol',LC)
    fx=[lab(l,f['x'],(f['y']+int(fr.get('hlab',240)*f['s'])) if f.get('head') else min(712,f['y']+28),16 if not fr.get('hlab') else 20,lc) for l,f in fr['figs'] if l]+[lab(fr['title'],640,26,18,lc)]
    sc={'bg':fr.get('bg',DARKPAPER),'figs':figs,'fx':fr.get('fx',[])+fx}
    if fr.get('layers'):sc['layers']=fr['layers']
    if fr.get('fxb'):sc['fxb']=fr['fxb']
    return {'beat':1,'at':T,'draw':'scene','grade':fr.get('grade','ep07_dark'),'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':sc}

def main():
    names=sys.argv[1:] or list(FRAMES)
    shots=[{'beat':1,'at':0,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':DARKPAPER,'figs':[],'fx':[]}}]
    for i,n in enumerate(names):shots.append(shot(i+1,FRAMES[n]))
    T=len(names)+1;tmp=R+'/build/ep07_cast_sheet';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp)
    json.dump(shots,open(tmp+'/shots.json','w'),ensure_ascii=False)
    json.dump([{'beat':1,'audio':T+1,'duration':T+1,'words':[{'text':'.','start':0,'end':.1}]}],open(tmp+'/timings.json','w'))
    env=dict(os.environ,ENGINE=B.build(1.5),VW='1920',VH='1080')
    if 'NODE_PATH' not in env:env['NODE_PATH']=subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()
    ts=[f'{i+.5:.1f}' for i in range(T)]
    r=subprocess.run(['node',R+'/studio/still.js',tmp+'/shots.json',tmp+'/timings.json',tmp]+ts,env=env,cwd=R,capture_output=True,text=True)
    if r.returncode:sys.exit(r.stdout+r.stderr)
    for l in r.stdout.splitlines():
        if (l.startswith('FX_ERRORS') and l.strip()!='FX_ERRORS []') or 'PAGEERR' in l or 'CONSOLE' in l:print(l)
    for i,n in enumerate(names):
        dst=f'{OUT}/{n}.jpg';Image.open(f"{tmp}/t{ts[i+1].rjust(5,'0')}.png").convert('RGB').save(dst,quality=88);print(dst)
main()
