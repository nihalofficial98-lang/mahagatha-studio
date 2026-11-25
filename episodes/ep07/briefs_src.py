"""EP07 shot briefs, written by the Opus designers (cinematographer -> scene designer -> action director -> effects designer).
This file is the editable SOURCE of episodes/ep07/briefs.json: python3 episodes/ep07/briefs_src.py
Each shot = start time of its first spoken word (voice_timeline.md); narration and duration are filled from the voice timeline
(a shot lasts until the next shot starts). Places: council (heaven), ashram (dusk yard / night yard), window (Devayani's window,
morning or night), room (Kacha's room at night), feast (demon feast hall), forest (dawn / night), battle, kailash."""
import json,re,os,sys
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ---------------- voice timeline ----------------
TL=[];BEATS={}
_t=open(R+'/episodes/ep07/voice_timeline.md',encoding='utf-8').read();_b=None
for ln in _t.splitlines():
    m=re.match(r'## Beat (\d+)\s+\((\d+):([\d.]+) – (\d+):([\d.]+)\)',ln)
    if m:_b=int(m[1]);BEATS[_b]=(int(m[2])*60+float(m[3]),int(m[4])*60+float(m[5]));continue
for txt,ws in re.findall(r'\*\*L\d+\*\* [^\n]*\n([^\n]*)\n`([^`]*)`',_t):
    for tok,w in zip(txt.split(),ws.split()):
        word,t=w.rsplit('@',1);TL.append({'tok':tok,'w':word,'t':float(t)})
_bstart=sorted(BEATS.items())
for x in TL:x['beat']=max(b for b,(s,e) in _bstart if x['t']>=s-.3)
TOTAL=471.8
def idx(t):
    for i,x in enumerate(TL):
        if abs(x['t']-t)<.006:return i
    raise SystemExit(f'no word at {t}')
# ---------------- helpers ----------------
def C(z0,z1,x0=0,x1=0,y0=0,y1=0,r0=0,r1=0):return {'from':{'z':z0,'x':x0,'y':y0,'r':r0},'to':{'z':z1,'x':x1,'y':y1,'r':r1}}
def F(who,x,y,s,flip=1,emo='calm',**k):
    d={'who':who,'x':x,'y':y,'s':s,'flip':flip,'emo':emo}
    for kk in ('pose','look','talk','head','prop','halo','actions','mood','walk','turn_on','turn_d','engine','engine_cues'):
        if kk in k:d[kk]=k.pop(kk)
    if k:d.setdefault('engine',{}).update(k)    # any other rig key (tilt, filt, rim, ash, glow, rise, mat, kmood, ...)
    if 'actions' not in d:d['actions']=[]
    return d
def A(word,d=.6,**k):x={'word':word,'d':d};x.update(k);return x
def X(k,x,y,w,meaning,word=None,**o):
    d={'k':k,'x':x,'y':y,'w':w,'meaning':meaning}
    if word:d['word']=word
    d.update(o);return d
def NAME(s,x,y,word,size=30):return {'k':'name','s':s,'x':x,'y':y,'size':size,'word':word,'meaning':f'the name {s} appears the moment it is spoken'}
def TEXT(s,x,y,word,meaning,size=52,col='#ffd9a0'):return {'k':'text','s':s,'x':x,'y':y,'size':size,'col':col,'word':word,'meaning':meaning}
SHADOW=dict(filt='brightness(.07) saturate(0)',rim='rgba(255,140,70,.6)',halo=False)   # Brihaspati at night: near-black shadow, ember outline, no halo
def L(d,contents,items=None,**o):
    x={'d':d,'contents':contents}
    if items is None:x['from_background']=True
    else:x['items']=items
    x.update(o);return x
HZ='#5a2414'
def DEM(x,y,s,n,w,seed,**o):d={'o':'demons','x':x,'y':y,'s':s,'n':n,'w':w,'seed':seed};d.update(o);return d
def ST(x,y,s,h,seed,**o):d={'o':'stree','x':x,'y':y,'s':s,'h':h,'seed':seed};d.update(o);return d
def SM(x,y,w,h,col='#2a1610',a=.6):return {'o':'smoke','x':x,'y':y,'s':1,'w':w,'h':h,'col':col,'a':a}
def SH(x,y,s,col='#1a0e0a'):return {'o':'shrub','x':x,'y':y,'s':s,'col':col}
# ---------------- places (background + depth layers) ----------------
NIGHT_SKY=['#07040a','#140a0c','#2a120c','#3e1a10']
MORN_SKY=['#2a1612','#6a3420','#c8703a','#e8a85a']
def ashram(night=False,morning=False,near=True,far_dem=False,**bgo):
    bg={'k':'ashram','fire':False}
    if night:bg.update(sky=NIGHT_SKY,sx=-900,sy=200)
    if morning:bg.update(sky=MORN_SKY,sx=1000,sy=230)
    bg.update(bgo)
    far=L('far','silhouette forest trees on the far ridge in ember haze',[ST(80,540,.5,420,3),ST(900,540,.45,380,5),ST(1260,540,.5,440,7)],fog=.5,haze='#4a2018' if night else '#6a2e1e')
    if far_dem:far['items'].append(DEM(640,560,.5,16,1500,4,eyes=.8))
    mid=L('mid','shrubs and a small tulsi bush along the ashram yard',[SH(470,600,.9,'#1e120c'),SH(820,606,.8,'#1e120c')],fog=.2,haze='#3a1a10')
    out=[far,mid]
    if near:out.append(L('near','dark shrubs in the bottom corners, out of focus',[SH(30,770,1.7),SH(1250,770,1.6)],dark=.6))
    return bg,out
def window(night=False,x=900,y=640):
    bg={'k':'ashram','fire':False,'hx':260,'hx2':-600}
    bg.update(dict(sky=NIGHT_SKY,sx=-900,sy=200) if night else dict(sky=MORN_SKY,sx=420,sy=210))
    lay=[L('far','silhouette trees on the ridge behind the ashram',[ST(100,540,.5,420,3),ST(500,540,.42,360,9)],fog=.5,haze='#5a2a1e'),
         L('mid','the dark room behind Devayani\'s window'+(' lit by her oil lamp' if night else ''),[{'o':'winwall','part':'back','x':x,'y':y,'s':1,'lamp':1 if night else 0}],fog=0),
         L('near','the mud wall of her room with the window cut out, open wooden shutters, thatch eave and a jasmine vine',[{'o':'winwall','x':x,'y':y,'s':1,'lamp':1 if night else 0,'lit':'255,120,60' if night else '255,180,100'}],dark=.08 if not night else .2,blur=0,par=1.0)]
    return bg,lay
def room(lamp=1,bx=1080,near=True):
    bg={'k':'kacha_room_night','lamp':lamp,'bx':bx}
    lay=[L('far','mud-plaster back wall with the small barred window and the moon',fog=.4),
         L('mid','a wooden roof post and a hanging cloth in the lamp shadow',[{'o':'pillar','x':1230,'y':610,'s':.9,'h':560,'col':'#3a2416'}],fog=.25,haze='#1a0c08')]
    if near:lay.append(L('near','a dark wooden door-post edge on the left, out of focus',[{'o':'pillar','x':-6,'y':760,'s':1.3,'col':'#2a160c'}],dark=.65))
    return bg,lay
def feast(crowd=True,fire=1,near=True,mid=True):
    bg={'k':'feasthall','fire':fire,'crowd':crowd}
    lay=[L('far','a silhouette army of demons with ember eyes under the fire-lit arches',[DEM(640,560,.62,20,1500,4)],fog=.45,haze=HZ,blur=1.4)]
    if mid:lay.append(L('mid','two packs of horned demon silhouettes left and right',[DEM(200,640,.95,4,360,8),DEM(1080,640,.95,4,360,12)],fog=.12,haze=HZ))
    if near:lay.append(L('near','huge black demon shoulders and horns in the bottom corners',[DEM(20,850,1.7,2,200,77,eyes=.6),DEM(1270,850,1.6,2,200,91,eyes=.6)],dark=.2,blur=2))
    return bg,lay
def forest(night=False,demons=0,smoke=.8,near=True,**bgo):
    bg={'k':'forest','smoke':smoke}
    if night:bg.update(sky=['#06040a','#120a0c','#26120c','#3a1a10'],sx=-900,rays=False)
    bg.update(bgo)
    far=L('far','rows of silhouette trees fading into dawn smoke' if not night else 'black tree rows fading into the night smoke',[ST(200,560,.6,420,21),ST(760,560,.55,400,23),ST(1150,560,.6,440,25)],fog=.55,haze='#6a3a24' if not night else '#2a160e')
    if demons:far['items'].append(DEM(640,590,.7,14,1400,31))
    mid=L('mid','a low smoke bank rolling between the trunks',[SM(640,600,1800,90,'#2a1610',.55)],fog=.1,haze=HZ)
    if demons>1:mid['items']+= [DEM(170,690,1.15,3,280,41),DEM(1120,690,1.15,3,300,45)]
    out=[far,mid]
    if near:out.append(L('near','a bare black tree trunk on the left and a thicket on the right, out of focus',[ST(-30,800,1.2,900,61,bare=1),SH(1250,770,1.8,'#140a08')],dark=.7))
    return bg,out
def council(devas=True):
    bg={'k':'council'}
    lay=[L('far','dim gold arches of the heavenly hall with clouds beyond',fog=.4),
         L('mid','soft gold clouds drifting low through the arches of heaven',[{'o':'cloud','x':330,'y':520,'s':.8,'col':'#8a6a44'},{'o':'cloud','x':960,'y':500,'s':.7,'col':'#7a5a3a'}],fog=.3,haze='#3a2a18'),
         L('near','gold pillar edges at the frame sides, dark and soft',[{'o':'pillar','x':-6,'y':760,'s':1.25,'col':'#6a4a24'},{'o':'pillar','x':1286,'y':760,'s':1.25,'col':'#6a4a24'}],dark=.5)]
    return bg,lay
def battle():
    bg={'k':'forest','smoke':1,'sky':['#1a0a08','#3a140c','#7a2a14','#a8481c']}
    lay=[L('far','an army of demon silhouettes with ember eyes in the battle smoke',[DEM(640,580,.7,18,1500,51)],fog=.5,haze='#6a2a18'),
         L('mid','smoke rolling over the battlefield and two demon packs',[SM(640,610,1800,100,'#3a1a10',.6),DEM(1100,680,1.0,3,260,53)],fog=.15,haze=HZ),
         L('near','a broken black tree and rocks in the corners',[ST(-20,800,1.2,900,63,bare=1),{'o':'rock','x':1250,'y':760,'s':1.6,'col':'#1a0c08'}],dark=.7)]
    return bg,lay
def kailash():
    bg={'k':'kailash'}
    lay=[L('far','snow peaks of Kailash in a dim ember haze',[{'o':'mountain','x':300,'y':520,'s':1.1,'col':'#6a4a48'},{'o':'mountain','x':1020,'y':520,'s':1.0,'col':'#5a3e40'}],fog=.5,haze='#5a3a34'),
         L('mid','dark rocks at the foot of the peak',[{'o':'rock','x':180,'y':640,'s':1.2,'col':'#3a2a2a'},{'o':'rock','x':1120,'y':640,'s':1.1,'col':'#3a2a2a'}],fog=.2,haze='#2a1a18'),
         L('near','black rocks in the bottom corners',[{'o':'rock','x':30,'y':780,'s':2.0,'col':'#140c0c'},{'o':'rock','x':1260,'y':780,'s':1.8,'col':'#140c0c'}],dark=.6)]
    return bg,lay
SHOTS=[]
def S(t,shot,lens,move,cam,motivation,meaning,why,focus,place,emotion,chars,fx=(),tr='cut',shake=0,depth=None,change=None):
    bg,lay=place
    bg=dict(bg)
    if change:bg['change']=change
    SHOTS.append(dict(t=t,camera=dict(shot=shot,lens=lens,move=move,**cam,shake=shake,motivation=motivation),meaning=meaning,why=why,
        focus={'subject':focus,'depth':depth or ('shallow' if lens=='tele' or shot in('close','extreme_close','insert') else 'deep')},
        layers=lay,background=bg,mood={'emotion':emotion,'grade':'ep07_dark'},characters=list(chars),effects=list(fx),transition_in=tr))
# ================= B01 teaser =================
S(0.08,'close','tele','push_in',C(1.0,1.14,0,0,10,0),'slow push into his calm face as he states his own death wish',
  'Kacha, a young man, wanted to be killed: the whole episode turns on this strange wish.',
  'His face fills the frame in dark forest smoke, eyes steady and lips in a cold half-smile on "killed", so the wish reads as a plan, not despair.',
  'kacha',forest(demons=1,smoke=1),'mysterious dread',
  [F('kacha',640,330,1.25,1,'calm',head=True,mood={'blink':.3},actions=[A('killed',emo='coldsmile',d=.7)])],
  [NAME('Kacha',640,96,'Kacha'),X('embers',640,520,1100,'sparks of the fire that will burn him drift up',par=1.3)],tr='fade')
S(2.44,'low_angle','wide','tilt_up',C(1.08,1.16,0,0,30,-10),'tilt up the flames that rise around the kneeling boy',
  'Burned: Kacha will be burned in a fire.',
  'Kacha kneels with eyes closed while a paper fire burns high in front of his knees and smoke rolls past; the demon army waits in the haze.',
  'kacha',forest(demons=1,smoke=1),'dread',
  [F('kacha',640,700,.9,1,'pain',pose='kneel',mood={'blink':1},actions=[A('Burned',mood={'blink':1,'sad':.8})])],
  [X('ember_fire',640,716,170,'the fire that burns Kacha',word='Burned',d=.3),X('embers',640,500,700,'sparks and smoke rising from the burning body',par=1.1)])
S(3.45,'insert','normal','crane_down',C(1.2,1.32,0,0,-30,10),'descend onto the grey pile, the camera settles like the ash',
  'His body was ground to ash.',
  'A grey ash pile sits on the dark forest floor while a horned demon looks down at it with a satisfied smirk; sparks still float.',
  'ash pile',forest(demons=1,smoke=.9),'grim',
  [F('asura1',880,690,.82,-1,'scheme',look=640,actions=[A('ash',emo='coldsmile')])],
  [X('ash_pile',600,600,260,'Kacha ground to ash',word='Ground',h=1),X('embers',600,560,500,'the last sparks of the fire',par=1.0)])
S(4.95,'low_angle','normal','tilt_up',C(1.12,1.24,0,0,40,-10),'low angle: the enemy guru looms as he drinks',
  'And then he was swallowed by his enemy\'s guru.',
  'Old Shukracharya, huge from below in the fire-lit demon hall, tips back a wine cup with ash swirling in it, eyes half closed in pleasure.',
  'shukracharya',feast(),'dark irony',
  [F('shukracharya',640,720,1.0,1,'calm',pose='raise',prop='cup',ash=1,mood={'blink':.65,'smile':.3},actions=[A('swallowed',mood={'blink':.9,'mouth':.4})])],
  [X('embers',640,560,1200,'firelight sparks of the demon hall',par=1.2)])
S(7.43,'medium','normal','dolly_left',C(1.15,1.2,40,-40,0,0),'slide with him as he lifts the stolen secret into the light',
  'It was the only way to steal a secret.',
  'Kacha stands in the dark ashram yard holding up a glowing palm-leaf mantra and eyeing it with a scheming smile: the secret he came to steal.',
  'kacha',ashram(night=True),'scheming',
  [F('kacha',560,680,.86,1,'scheme',pose='catch',prop='leaf',glow=1,actions=[A('steal',emo='coldsmile')])],
  [X('ember_fire',1010,612,110,'the yard fire lights the night',behind=True)])
S(9.66,'wide','wide','crane_up',C(1.0,1.06,0,0,30,-20),'rise with the dead demon as he is brought back',
  'The secret could bring the dead back to life.',
  'On the smoky battlefield Shukracharya raises his palm and a shaft of light falls on a slain demon, who rises from the ground with open arms.',
  'asura2',battle(),'awe',
  [F('shukracharya',330,672,.8,1,'calm',pose='raise',look='asura2',mood={'blink':.5}),
   F('asura2',860,690,.78,-1,'pain',pose='collapse',actions=[A('bring',pose='rise',emo='shock',d=1.0,e='spring')])],
  [X('light_beam',860,690,170,'the life-giving mantra pours into the dead demon',word='bring',alpha=.55,blend='lighter')])
S(11.87,'close','tele','push_in',C(1.12,1.24,0,0,0,10),'push in on his triumphant cold smile',
  'It worked: Kacha got the secret.',
  'Kacha\'s face in the night yard with the glowing palm leaf under his chin; he smiles coldly, the light of the stolen mantra on his face.',
  'kacha',ashram(night=True),'cold triumph',
  [F('kacha',640,320,1.25,1,'coldsmile',head=True,actions=[A('worked',mood={'smirk':1,'blink':.45})])],
  [X('palm_leaf',650,520,300,'the stolen mantra in his hand',glow=1,rot=-.08)])
S(13.01,'close','tele','pull_out',C(1.25,1.1,0,0,0,0),'pull back from her tears to leave her alone in the dark',
  'But what he did to the girl who loved him was worse than death.',
  'Devayani in the dark ashram, tears on her face: her loving look breaks into pain on "loved"; a faint red curse-glow pulses behind her head.',
  'devayani',ashram(night=True),'heartbreak',
  [F('devayani',640,330,1.2,1,'love',head=True,actions=[A('loved',emo='pain',d=.7)])],
  [X('curse_glow',640,280,560,'the curse that will come from her broken heart',word='worse',behind=True,alpha=.45)])
# ================= B02 =================
S(16.95,'wide','wide','dolly_right',C(1.0,1.06,-30,40,0,0),'travel across the battle as the god strikes',
  'Every time the gods killed a demon.',
  'On a smoky battlefield Indra hurls his thunderbolt and a demon topples backwards on "killed" while a demon army burns in the haze.',
  'indra',battle(),'battle',
  [F('indra',300,672,.8,1,'fury',pose='throw',look='asura2',halo=False),
   F('asura2',880,690,.8,-1,'fury',pose='lunge',actions=[A('killed',pose='fall',emo='pain',d=.5,e='antic')],engine={'bow':-.45,'bd':.6},engine_cues={'bc':'killed'})],
  [X('vajra_thrown',600,420,300,'Indra\'s thunderbolt kills the demon',word='gods')],tr='fade',shake=2)
S(19.01,'wide','normal','crane_up',C(1.05,1.12,0,0,20,-20),'rise with the dead demon pulled back to life',
  'One old man brought the demon back to life.',
  'Old Shukracharya at the edge of the battle lifts his palm; a beam of warm light falls on the fallen demon, who rises up with his arms open.',
  'shukracharya',battle(),'dark wonder',
  [F('shukracharya',340,672,.82,1,'calm',pose='raise',look='asura2',actions=[A('old',mood={'blink':.6,'smile':.2})]),
   F('asura2',850,690,.8,-1,'pain',pose='collapse',actions=[A('brought',pose='rise',emo='shock',d=1.0,e='spring')])],
  [X('light_beam',850,690,170,'the life-giving mantra',word='brought',alpha=.6,blend='lighter')])
S(21.26,'low_angle','wide','tilt_up',C(1.0,1.09,0,0,30,-12),'low angle: the guru of the demons towers over his army',
  'His name was Shukracharya, guru of the demons.',
  'Shukracharya stands tall in the fire-lit feast hall, white beard and maroon robe, a horned silhouette army behind him; he raises his palm on "guru".',
  'shukracharya',feast(),'power',
  [F('shukracharya',640,700,.95,1,'pride',talk=.2,mood={'blink':.4},actions=[A('guru',pose='raise',d=.7)])],
  [NAME('Shukracharya',640,96,'Shukracharya'),X('embers',640,560,1200,'sparks of the hall fires',par=1.2)],tr='fade')
S(24.84,'close','tele','push_in',C(1.0,1.12,0,0,0,10),'push in on the chanting face as the secret is named',
  'His secret was Mritasanjivani, the power to revive the dead.',
  'Shukracharya\'s face, eyes closed, lips chanting; a golden yantra circle glows behind his head and the word Mritasanjivani appears.',
  'shukracharya',ashram(night=True),'mystery',
  [F('shukracharya',640,340,1.2,1,'calm',head=True,mood={'blink':1,'mouth':.3},talk=.4)],
  [X('magic_circle',640,300,560,'the mantra of the dead, Mritasanjivani',word='secret',behind=True,alpha=.55),TEXT('Mritasanjivani',640,100,'Mritasanjivani','the name of the secret appears as it is spoken',58)])
S(29.14,'wide','wide','pull_out',C(1.15,1.0,0,0,0,0),'pull out to show an endless demon army against one god',
  'As long as he held it, the gods could never win.',
  'Indra backs away on the left, afraid, as rows and rows of demon silhouettes with ember eyes fill the battlefield to the horizon.',
  'indra',battle(),'hopeless',
  [F('indra',260,672,.72,1,'fear',pose='flee',halo=False,look=800,actions=[A('never',emo='shock')])],
  [X('demon_crowd',820,690,900,'the demons who keep coming back from death',rows=3,n=7,seed=12,behind=True)])
# ================= B03 council =================
S(32.42,'establishing','wide','crane_down',C(1.0,1.06,0,0,-40,0),'descend into the council hall of heaven',
  'Brihaspati, guru of the gods, called a council in heaven.',
  'In the dim golden hall of heaven Brihaspati stands at the centre on the red runner and opens his hands; Agni, Vayu, Indra and Surya turn to him.',
  'brihaspati',council(),'grave council',
  [F('brihaspati',640,672,.82,1,'doubt',mood={'sad':.3},actions=[A('called',pose='open',d=.7)]),
   F('agni',330,660,.66,1,'calm',look='brihaspati'),F('vayu',170,655,.62,1,'doubt',look='brihaspati'),
   F('indra',960,668,.72,-1,'calm',look='brihaspati',halo=False),F('surya',1120,655,.62,-1,'doubt',look='brihaspati')],
  [NAME('Brihaspati',640,96,'Brihaspati')],tr='fade')
S(36.15,'close','tele','push_in',C(1.0,1.12),'push in on the grim face',
  'Brihaspati\'s face was grim with worry.',
  'Brihaspati\'s grey-bearded face in close-up, brows heavy and mouth turned down; the dim gold arches blur behind him.',
  'brihaspati',council(),'grim',
  [F('brihaspati',640,330,1.25,1,'doubt',head=True,mood={'sad':.5,'ly':.15},actions=[A('grim',mood={'anger':.45,'sad':.6})])])
S(37.79,'medium','normal','dolly_left',C(1.1,1.16,40,-20,0,0),'drift along the listening gods',
  'Brihaspati spoke just one word to the gods.',
  'Brihaspati, talking, raises one finger; Indra and Agni lean in to listen to the single word.',
  'brihaspati',council(),'suspense',
  [F('brihaspati',480,680,.9,1,'doubt',talk=.6,actions=[A('one',pose='point')]),
   F('indra',900,672,.82,-1,'doubt',look='brihaspati',halo=False),F('agni',1120,665,.7,-1,'calm',look='brihaspati')])
S(39.77,'extreme_close','tele','static',C(1.3,1.3,0,0,0,0),'hold still on the forbidden word',
  'The one word was Mritasanjivani, the secret of the dead.',
  'Brihaspati\'s narrowed eyes in extreme close-up while the word Mritasanjivani burns above him and a yantra glows behind.',
  'brihaspati',council(),'forbidden secret',
  [F('brihaspati',640,350,1.3,1,'scheme',head=True,talk=.5,mood={'smirk':.2})],
  [TEXT('Mritasanjivani',640,110,'Mritasanjivani','the word he speaks appears',62),X('magic_circle',640,320,600,'the secret mantra',behind=True,alpha=.4)])
S(40.78,'two_shot','normal','dolly_left',C(1.05,1.12,30,-10,0,0),'follow the question from Indra to Brihaspati',
  'Indra, king of the gods, asked if they really had to steal it from Shukracharya.',
  'Indra in his tall crown opens his hands, shocked, asking; on "steal" his face turns to doubt while Brihaspati listens gravely.',
  'indra',council(),'disbelief',
  [F('indra',800,672,.88,-1,'shock',pose='open',talk=.6,look='brihaspati',halo=False,actions=[A('steal',emo='doubt')]),
   F('brihaspati',380,676,.86,1,'doubt',look='indra')],
  [NAME('Indra, king of the gods',800,96,'Indra',28)])
S(45.28,'medium','normal','pan_right',C(1.12,1.18,-40,30,0,0),'pan to the old guru far away, clutching his secret',
  'The old guru would never share it.',
  'Far away in his dusky ashram Shukracharya holds the glowing palm-leaf mantra against his chest, brows hard and lips shut.',
  'shukracharya',ashram(),'stubborn',
  [F('shukracharya',600,680,.9,1,'calm',pose='hold',prop='leaf',glow=.7,mood={'anger':.35},actions=[A('never',mood={'anger':.6},tilt=-.05)])],
  [X('ember_fire',1010,612,110,'the guru\'s evening fire',behind=True)],tr='wipe')
S(47.56,'two_shot','normal','pull_out',C(1.14,1.04,0,0,0,0),'pull back to the calm guru stopping the war god',
  'Brihaspati said they would not use force.',
  'Back in the council Brihaspati raises a calm palm toward Indra, who lowers his thunderbolt arm and listens.',
  'brihaspati',council(),'restraint',
  [F('brihaspati',420,676,.86,1,'calm',talk=.5,look='indra',actions=[A('said',pose='raise')]),
   F('indra',840,672,.86,-1,'fury',pose='throw',look='brihaspati',halo=False,actions=[A('said',pose='stand',emo='doubt',d=.8)])],tr='wipe')
S(50.21,'medium','normal','push_in',C(1.0,1.1,-30,-10,0,0),'push in as a hidden young figure appears in the arch',
  'He had someone Shukracharya would never suspect.',
  'Brihaspati smirks to the side while, behind him in the central arch, the dark silhouette of a young man fades in: the someone.',
  'brihaspati',council(),'secret plan',
  [F('brihaspati',430,690,.92,1,'scheme',look=640),
   F('kacha',700,610,.55,1,'calm',look='brihaspati',filt='brightness(.12) saturate(0)',rim='rgba(255,170,90,.6)',engine_cues={'ac':'someone'},ad=.8)])
S(53.24,'close','tele','dutch',C(1.2,1.28,0,0,0,0,0,.035),'tilt the frame: a dangerous plan',
  'And Brihaspati already had a plan ready.',
  'Brihaspati in close-up, frame tilting, his mouth curls into a cold knowing smile.',
  'brihaspati',council(),'cunning',
  [F('brihaspati',640,330,1.2,1,'coldsmile',head=True,actions=[A('plan',mood={'smirk':1})])])
# ================= B04 the ashram =================
S(54.82,'establishing','wide','pan_right',C(1.0,1.04,-60,20,0,0),'pan with the stranger walking into the ashram',
  'A few days later, a young man walked into Shukracharya\'s ashram.',
  'At dusk a young man in a saffron shawl walks in from the left across the ashram yard toward old Shukracharya, who waits by his hut.',
  'kacha',ashram(),'arrival',
  [F('kacha',170,672,.78,1,'calm',look='shukracharya',walk={'word':'young','to_x':520,'d':2.2,'speed':1}),
   F('shukracharya',960,676,.8,-1,'calm',look='kacha')],tr='fade')
S(58.59,'two_shot','normal','push_in',C(1.06,1.16,40,60,0,0),'push in on the humble request',
  'He asked to be his student.',
  'The young man drops to his knees before Shukracharya on "asked", hands folded; the old guru looks down at him with a soft smile.',
  'kacha',ashram(),'humility',
  [F('kacha',560,676,.8,1,'devotion',actions=[A('asked',pose='kneel',e='spring',d=.6)]),
   F('shukracharya',840,676,.82,-1,'calm',look='kacha',mood={'smile':.4})])
S(60.25,'medium','normal','dolly_right',C(1.18,1.24,20,60,0,0),'slide toward the tying hands',
  'The guru tied a sacred thread on his wrist.',
  'Kneeling Kacha holds up his wrist while Shukracharya bends forward with both hands and ties a red-gold thread on it.',
  'shukracharya',ashram(),'blessing',
  [F('kacha',600,676,.8,1,'devotion',pose='kneel',look='shukracharya'),
   F('shukracharya',820,676,.82,-1,'love',pose='hold',look='kacha',actions=[A('tied',tilt=.08)])],
  [X('sacred_thread',705,480,70,'the sacred thread tied on Kacha\'s wrist',word='thread')])
S(62.76,'insert','tele','push_in',C(1.0,1.1),'push into the knot of the promise',
  'A promise to keep him safe.',
  'The red-gold raksha thread fills the frame on his wrist, its knot glowing; Kacha\'s face beside it looks down at it, calm.',
  'sacred thread',ashram(),'promise',
  [F('kacha',400,350,1.05,1,'calm',head=True,mood={'ly':.7,'lx':.5,'blink':.4},actions=[A('safe',mood={'smile':.3,'ly':.5})])],
  [X('sacred_thread',820,380,360,'the guru\'s promise to protect his student',tied=1),X('glow',820,380,260,'warm light of the promise',rgb='255,170,90',ga=.35)])
S(64.59,'two_shot','tele','pull_out',C(1.12,1.02),'pull back to show the two faces that want different things',
  'He did not know whose son the boy was.',
  'Shukracharya smiles warmly at his new student on the right, while Kacha on the left looks away with a sly, secret look.',
  'kacha',ashram(),'dramatic irony',
  [F('shukracharya',880,330,1.0,-1,'love',head=True,look='kacha'),
   F('kacha',400,340,1.0,1,'scheme',head=True,actions=[A('son',mood={'smirk':.8,'lx':-.6})])])
S(67.03,'medium','normal','dolly_left',C(1.1,1.18,30,-20,0,0),'drift toward the boy as he names himself',
  'The young man told him his name was Kacha.',
  'Kacha stands and speaks with folded hands to the old guru; his name appears above him.',
  'kacha',ashram(),'introduction',
  [F('kacha',520,676,.88,1,'calm',talk=.6,look='shukracharya',actions=[A('told',pose='namaste')]),
   F('shukracharya',900,676,.84,-1,'calm',look='kacha',mood={'smile':.3})],
  [NAME('Kacha',520,110,'name')])
S(69.54,'wide','normal','pan_left',C(1.12,1.16,80,-140,0,0),'pan from Kacha to the girl watching him',
  'Shukracharya\'s daughter was watching him from the doorway.',
  'In the lit doorway of the hut a young woman in a maroon sari leans and watches Kacha with soft eyes; Kacha, in front, does not see her.',
  'devayani',ashram(),'first love',
  [F('devayani',225,608,.6,1,'love',look='kacha',actions=[A('watching',tilt=.07)]),
   F('kacha',880,690,.86,1,'calm',look=1200,talk=.3)])
S(72.53,'two_shot','normal','push_in',C(1.08,1.16,-40,-40,0,0),'push in on the girl as she says her name',
  'She told him her name was Devayani.',
  'Devayani steps out and speaks shyly to Kacha; her name appears above her as Kacha turns and smiles at her.',
  'devayani',ashram(),'shy love',
  [F('devayani',500,676,.86,1,'love',talk=.5,look='kacha'),F('kacha',860,676,.86,-1,'calm',look='devayani',mood={'smile':.5})],
  [NAME('Devayani',500,110,'name')])
S(74.50,'close','tele','crane_down',C(1.15,1.24,0,0,-20,10),'drop with her gaze',
  'And she lowered her eyes.',
  'Devayani\'s face in close-up: she lowers her eyes and blushes into a small smile, the jasmine in her hair catching the dusk light.',
  'devayani',ashram(),'tender',
  [F('devayani',640,330,1.25,1,'love',head=True,actions=[A('lowered',mood={'ly':.95,'blink':.6,'smile':.55},tilt=.08,d=.6)])])
# ================= B05 love, and the nightly shadow =================
S(76.15,'two_shot','normal','dolly_right',C(1.04,1.1,-30,30,0,0),'slow romantic drift past the two of them at dusk',
  'Soon Devayani was in love with Kacha.',
  'Under the dusky sky Devayani gazes at Kacha with a loving smile; Kacha smiles back at her, the hut lamps glowing behind them.',
  'devayani',ashram(),'young love',
  [F('devayani',470,676,.84,1,'love',look='kacha',actions=[A('love',tilt=.07,mood={'smile':.7})]),F('kacha',830,676,.86,-1,'calm',look='devayani',mood={'smile':.5})],tr='fade')
S(78.17,'wide','normal','pan_right',C(1.0,1.06,-40,30,0,0),'pan from the singer to the girl at her window',
  'Every morning Kacha sang hymns by her window.',
  'In warm morning light Kacha stands outside a mud wall singing with a hand on his chest; Devayani leans in the open window, listening with love.',
  'kacha',window(),'morning devotion',
  [F('kacha',380,690,.86,1,'love',pose='sing',talk=.7,look='devayani'),F('devayani',900,545,.8,-1,'love',look='kacha',actions=[A('hymns',tilt=-.07,mood={'smile':.7,'blink':.4})])],tr='fade')
S(80.67,'two_shot','normal','push_in',C(1.04,1.14,0,40,0,0),'push in on the gift',
  'Every evening Kacha brought her wild flowers from the woods.',
  'At dusk Kacha holds out a bunch of red and white wild flowers; Devayani reaches out and takes them, smiling with joy.',
  'devayani',ashram(),'courtship',
  [F('kacha',520,676,.86,1,'love',pose='hold',prop='flowers',look='devayani'),F('devayani',820,676,.84,-1,'joy',look='kacha',actions=[A('brought',pose='hold',d=.7,mood={'smile':.8})])],tr='fade')
S(83.85,'wide','normal','dolly_left',C(1.0,1.07,40,-10,10,10),'creep along the wall with the shadow',
  'And every night, a shadow slipped into Kacha\'s room.',
  'In Kacha\'s lamp-lit room he sits on his reed mat; a near-black shadow figure with an ember outline slips in from the right toward him.',
  'shadow',room(),'secret',
  [F('kacha',480,640,.8,1,'calm',pose='sit',look='brihaspati'),
   F('brihaspati',1060,680,.84,-1,'calm',look='kacha',walk={'word':'shadow','to_x':840,'d':1.4,'speed':.7},**SHADOW)],tr='fade')
S(87.14,'close','tele','push_in',C(1.08,1.18),'push in to unmask the shadow',
  'The shadow was Brihaspati, Kacha\'s father.',
  'The black head of the shadow fills the frame with a thin ember outline around grey jata and beard; his name appears above it.',
  'brihaspati',room(),'revelation',
  [F('brihaspati',640,340,1.2,-1,'scheme',head=True,look=300,**SHADOW)],
  [NAME('Brihaspati',640,96,'Brihaspati')])
S(88.46,'two_shot','normal','pan_left',C(1.12,1.16,60,-20,20,20),'pan from the asking shadow to the boy',
  'Brihaspati asked Kacha if he had the secret yet.',
  'The shadow bends toward Kacha and points at him, asking; Kacha on his mat looks up at his father.',
  'brihaspati',room(),'pressure',
  [F('brihaspati',840,680,.86,-1,'scheme',pose='point',talk=.6,look='kacha',tilt=.08,**SHADOW),F('kacha',480,640,.8,1,'calm',pose='sit',look='brihaspati',actions=[A('secret',mood={'ly':-.3})])])
S(90.99,'close','tele','push_in',C(1.12,1.22,0,0,10,10),'push in on his quiet answer',
  'Kacha said: not yet.',
  'Kacha\'s face in lamplight, answering softly with a sly look aside.',
  'kacha',room(),'cunning',
  [F('kacha',600,340,1.15,1,'scheme',head=True,talk=.5,look=900)])
S(92.42,'medium','normal','pull_out',C(1.2,1.08,120,60,0,0),'pull back from the lovesick girl at her lamp-lit window',
  'But the guru\'s daughter loved him more every day.',
  'At night Devayani leans in her lamp-lit window, chin tilted, gazing toward Kacha\'s room with a dreamy, loving smile.',
  'devayani',window(night=True,x=760),'longing',
  [F('devayani',760,545,.82,1,'love',look=200,actions=[A('loved',tilt=.08,mood={'smile':.75,'blink':.45})])],tr='wipe')
# ================= B06 the wine and the terrible idea =================
S(95.31,'wide','wide','crane_down',C(1.0,1.06,0,0,-40,0),'descend into the feast hall where the wine is brewed',
  'One evening Kacha saw the demons brewing wine for their guru.',
  'In the fire-lit demon hall two demons laugh over a fire, one holding a wine cup; Kacha stands in the left foreground watching them.',
  'kacha',feast(),'curiosity',
  [F('kacha',280,700,.9,1,'doubt',look='asura3',actions=[A('brewing',mood={'wide':.3})]),
   F('asura3',820,690,.8,-1,'joy',pose='raise',prop='cup',ash=0,talk=.5,mood={'laugh':.6}),F('asura1',1040,692,.78,-1,'joy',look='asura3',mood={'laugh':.5})],
  [X('ember_fire',930,712,200,'the fire for brewing the guru\'s wine',behind=True)],tr='fade')
S(99.14,'medium','normal','push_in',C(1.1,1.2,0,0,0,0),'push into the burning deer',
  'The demons burned a deer in the fire.',
  'A spotted deer is laid down in the flames, darkening as the fire burns high around it; a horned demon watches, grinning.',
  'deer',feast(),'grim',
  [F('deer',600,650,.82,1,'pain',pose='bow',look=900,filt='brightness(.4) saturate(.4)'),F('asura1',960,690,.8,-1,'joy',look='deer',mood={'laugh':.5})],
  [X('ember_fire',600,700,280,'the fire burning the deer',word='burned',d=.3)])
S(100.21,'insert','tele','crane_down',C(1.1,1.2,0,0,-30,0),'follow the ash falling into the cup',
  'They stirred the deer\'s ashes into the wine cup.',
  'Big in frame, the golden wine cup swirls with grey ash while black flakes drop into it; the plum feaster demon peers at it from the right.',
  'wine cup',feast(near=False),'sinister',
  [F('asura3',1010,330,1.0,-1,'scheme',head=True,look='cup',actions=[A('stirred',mood={'smirk':.8})])],
  [X('wine_cup',620,420,300,'the guru\'s wine with the deer\'s ashes',ash=1,word='stirred',d=.4),X('ash_speck',620,250,140,'ashes dropping into the wine',vy=40)])
S(102.51,'medium','normal','pull_out',C(1.14,1.04,0,0,0,0),'pull out to the cheering hall',
  'Shukracharya drank it all.',
  'Shukracharya tips back the ash-swirled cup with closed eyes while two demons beside him raise their arms and laugh.',
  'shukracharya',feast(),'revelry',
  [F('shukracharya',640,690,.88,1,'joy',pose='raise',prop='cup',ash=1,mood={'blink':.8,'mouth':.4},actions=[A('drank',mood={'blink':1,'mouth':.6})]),
   F('asura3',300,694,.76,1,'joy',pose='raise',prop='cup',ash=0,look='shukracharya',mood={'laugh':.8}),F('asura1',990,694,.76,-1,'joy',look='shukracharya',mood={'laugh':.7})])
S(104.51,'close','tele','push_in',C(1.1,1.2,0,0,0,0),'push in on his fixed stare',
  'Kacha stared at the cup.',
  'Kacha\'s face in close-up, eyes wide and fixed to the right where the ash-swirled wine cup glints out of focus.',
  'kacha',feast(near=False),'fixation',
  [F('kacha',520,340,1.15,1,'shock',head=True,look=1000,mood={'wide':.6})],
  [X('wine_cup',1020,420,150,'the cup he stares at',ash=1)])
S(106.15,'extreme_close','tele','dutch',C(1.3,1.38,0,0,0,0,0,-.04),'the frame tilts as a terrible thought takes hold',
  'A terrible idea came to Kacha.',
  'Extreme close-up of Kacha\'s eyes widening and then narrowing into a scheming smirk, a red pulse throbbing behind his head.',
  'kacha',feast(near=False),'dark inspiration',
  [F('kacha',640,360,1.4,1,'horror',head=True,actions=[A('idea',emo='scheme',d=.7)])],
  [X('red_energy_pulse',640,300,520,'the terrible idea throbbing in his mind',behind=True,alpha=.5)])
S(108.15,'medium','normal','dolly_right',C(1.15,1.22,-20,40,0,0),'slide toward his open palm',
  'What if those ashes in the cup were his own?',
  'Kacha looks down at his own open palm as grey ash and sparks swirl up out of it, imagining his own body as ash.',
  'kacha',feast(),'morbid thought',
  [F('kacha',560,690,.9,1,'doubt',pose='open',mood={'ly':.6,'lx':.4},actions=[A('ashes',emo='horror',d=.7)])],
  [X('ash_speck',660,460,90,'his own body as ash',word='ashes'),X('embers',650,450,260,'his body turning to sparks and ash',word='those',par=1.0)])
S(110.13,'medium','normal','pull_out',C(1.16,1.06,0,0,20,10),'pull back to show him alone with his plan',
  'It could kill him, but it was the only way.',
  'Alone in his lamp-lit room Kacha sits on the mat, fear on his face, then his jaw sets calm on "But".',
  'kacha',room(),'resolve',
  [F('kacha',560,640,.82,1,'fear',pose='sit',look=900,actions=[A('But',emo='calm',d=.6,mood={'ly':.2})])],tr='fade')
S(113.05,'low_angle','wide','tilt_up',C(1.04,1.12,0,0,30,-10),'low angle on the hating demons',
  'The demons hated Brihaspati\'s son.',
  'A slate-green demon with a sword glares and points out of the frame, red-eyed, with the black silhouette army behind him.',
  'asura2',feast(),'hatred',
  [F('asura2',640,720,1.0,1,'fury',pose='point',talk=.4)],
  [X('embers',640,560,1200,'the hall fires flare with their hatred',par=1.2)],tr='fade')
S(115.41,'medium','normal','push_in',C(1.05,1.15,0,0,0,0),'push in on his pleasure',
  'Shukracharya loved his wine.',
  'Shukracharya lifts his wine cup in the feast hall and laughs with pleasure, eyes half shut.',
  'shukracharya',feast(),'indulgence',
  [F('shukracharya',640,690,.9,1,'joy',pose='raise',prop='cup',ash=0,mood={'laugh':.7,'blink':.5},actions=[A('loved',mood={'laugh':1})])])
S(117.37,'wide','normal','dolly_left',C(1.04,1.1,30,-30,0,0),'move across the three of them, the girl in the middle',
  'And Devayani loved Kacha exactly as much as she loved her father.',
  'At dusk Devayani stands between Kacha and her father, gazing lovingly at Kacha; on "father" she turns her loving eyes to Shukracharya.',
  'devayani',ashram(),'divided love',
  [F('kacha',290,676,.82,1,'calm',look='devayani',mood={'smile':.4}),
   F('devayani',640,676,.84,1,'love',look='kacha',actions=[A('father',look='shukracharya',turn=.2)]),
   F('shukracharya',990,676,.84,-1,'love',look='devayani')],tr='fade')
S(121.26,'close','tele','static',C(1.08,1.08),'a still, balanced frame like a pair of scales',
  'Not more. Not less: her love was perfectly balanced.',
  'Devayani\'s face in the centre, Kacha\'s face on the left and her father\'s on the right in the dark, exactly balanced on both sides of her.',
  'devayani',ashram(near=False),'balance',
  [F('devayani',640,340,1.1,1,'love',head=True,look=640,actions=[A('Not',mood={'smile':.3,'blink':.4})]),
   F('kacha',250,380,.82,1,'calm',head=True,look='devayani',filt='brightness(.55) saturate(.6)'),
   F('shukracharya',1030,380,.82,-1,'love',head=True,look='devayani',filt='brightness(.55) saturate(.6)')])
# ================= B07 the three stages =================
S(123.07,'medium','normal','push_in',C(1.04,1.14,0,0,20,20),'push in on the planner',
  'Kacha\'s plan had three stages.',
  'In his dark room Kacha sits cross-legged before three small oil lamps, scheming; the words Three stages appear above him.',
  'kacha',room(),'scheming',
  [F('kacha',560,640,.82,1,'scheme',pose='sit',mood={'ly':.6},actions=[A('plan',mood={'smirk':.8,'ly':.3})])],
  [TEXT('Three stages',640,96,'three','the plan has three stages',50),X('glow',420,600,60,'the first lamp',rgb='255,170,90',ga=.7),X('glow',700,600,60,'the second and third lamps',rgb='255,170,90',ga=.7)],tr='fade')
S(124.93,'medium','normal','dolly_left',C(1.16,1.2,40,0,0,0),'slide with his raised hand',
  'Kacha would control two of the stages.',
  'Kacha stands in his room and raises his hand with a sly smile; the numerals I and II appear: the stages he controls.',
  'kacha',room(),'control',
  [F('kacha',560,680,.9,1,'scheme',talk=.3,actions=[A('control',pose='raise',d=.5)])],
  [TEXT('I  .  II',640,96,'control','the two stages Kacha controls',54)])
S(126.51,'medium','normal','crane_down',C(1.14,1.2,120,120,-30,0),'drop to the unknowing girl',
  'The third stage was in Devayani\'s hands.',
  'Devayani leans in her lamp-lit window at night, smiling, unaware; the numeral III appears beside her, and her name.',
  'devayani',window(night=True,x=760),'innocence',
  [F('devayani',760,545,.82,-1,'love',look=300,actions=[A('third',tilt=.06)])],
  [TEXT('III',640,96,'third','the third stage belongs to Devayani',58),NAME('Devayani',760,170,'Devayani\'s')],tr='wipe')
S(128.72,'ots','tele','pull_out',C(1.12,1.02,0,0,0,0),'pull back to put his secret face beside her innocent window',
  'He would not tell her. It was better if she did not know.',
  'Kacha\'s face fills the left foreground with a cold look while, behind him, Devayani smiles in her lamp-lit window, unaware.',
  'kacha',window(night=True,x=930),'secrecy',
  [F('kacha',360,360,1.1,1,'coldsmile',head=True,look=100,actions=[A('better',mood={'smirk':.9})]),F('devayani',930,545,.72,-1,'love',look='kacha')])
# ================= B08 stage one: the feast =================
S(132.00,'establishing','wide','crane_down',C(1.0,1.05,0,0,-40,0),'descend into the wild feast',
  'Stage one: the demons held a wild feast.',
  'The feast hall roars: three demons raise their cups and laugh by the fire bowls, the silhouette army sways behind; Stage one appears.',
  'asura3',feast(),'revelry',
  [F('asura3',400,690,.8,1,'joy',pose='raise',prop='cup',ash=0,talk=.6,mood={'laugh':.9}),F('asura1',820,692,.8,-1,'joy',talk=.5,mood={'laugh':.8},look='asura3'),
   F('asura2',1080,692,.76,-1,'joy',pose='raise',look='asura1',mood={'laugh':.6})],
  [TEXT('Stage one',640,96,'Stage','the first stage of the plan begins',54)],tr='fade')
S(135.07,'medium','normal','push_in',C(1.08,1.18,-20,-30,0,0),'push in on the fake drunk',
  'Kacha picked up a cup and pretended to be drunk.',
  'Kacha lifts a wine cup and sways with a loose laughing face, head tilted; a laughing demon beside him thinks he is one of them.',
  'kacha',feast(),'pretence',
  [F('kacha',560,690,.9,1,'joy',prop='cup',ash=0,mood={'laugh':.6,'blink':.45},actions=[A('picked',pose='raise',d=.5),A('pretended',tilt=.14,mood={'laugh':.9,'blink':.6})]),
   F('asura3',920,694,.82,-1,'joy',look='kacha',mood={'laugh':.8})])
S(137.96,'two_shot','normal','dolly_right',C(1.12,1.2,0,40,0,0),'slide close to the whisper',
  'He whispered to one demon that he was the son of Brihaspati.',
  'Kacha leans to the plum feaster demon and whispers with a sly face; the demon tilts his horned head to listen, eyes widening.',
  'kacha',feast(),'secret spills',
  [F('kacha',560,690,.9,1,'scheme',talk=.4,tilt=.12,look='asura3'),F('asura3',810,694,.88,-1,'doubt',look='kacha',actions=[A('whispered',tilt=-.1,mood={'surp':.5,'wide':.4})])])
S(141.64,'close','tele','push_in',C(1.1,1.2),'push in on the choke',
  'The demon choked on his drink.',
  'The plum demon\'s face in close-up: eyes bulging and mouth open in shock as wine spits from his lips.',
  'asura3',feast(near=False),'shock',
  [F('asura3',640,340,1.15,-1,'doubt',head=True,actions=[A('demon',emo='shock',mood={'mouth':.9,'wide':.9},d=.4)])],
  [X('blood_splash',560,440,70,'the wine he spits out',word='choked',n=6,spread=.5)],shake=3)
S(143.50,'medium','normal','pan_right',C(1.1,1.12,-120,120,0,0),'pan along the whispers from demon to demon',
  'He told another demon, and that one told another.',
  'The plum demon whispers into a green demon\'s ear, and the green demon turns, shocked, to tell the brute next to him.',
  'asura2',feast(),'rumour spreads',
  [F('asura3',330,692,.82,1,'scheme',talk=.6,look='asura2'),F('asura2',640,692,.82,1,'doubt',look='asura3',actions=[A('another',emo='shock',look='asura1',d=.5)]),
   F('asura1',960,692,.82,-1,'doubt',look='asura2',actions=[A('And',emo='fury')])])
S(145.64,'low_angle','wide','tilt_up',C(1.04,1.12,0,0,30,-10),'low angle on the rising fury',
  'Soon the demons were angry.',
  'The brute demon roars with claws out, eyes red, and the fire bowls behind flare up as the whole silhouette army turns angry.',
  'asura1',feast(fire=.5),'rage',
  [F('asura1',640,720,1.0,1,'fury',pose='grasp',actions=[A('angry',mood={'anger':1,'mouth':.8})])],
  [X('embers',640,560,1200,'sparks flare with their anger',par=1.2)],change={'word':'demons','to':{'fire':1.0},'d':1.0},shake=2)
S(147.50,'high_angle','wide','crane_up',C(1.1,1.0,0,0,30,0),'rise above the ring closing on him',
  'They crowded around Kacha.',
  'Kacha stands small in the centre, afraid, while rings of demon silhouettes with glowing red eyes close in all around him.',
  'kacha',feast(mid=False),'trapped',
  [F('kacha',640,690,.78,1,'fear',look=900,mood={'wide':.6},actions=[A('crowded',look=380)])],
  [X('demon_crowd',640,660,1500,'a ring of red demon eyes closing on Kacha',rows=2,n=7,seed=50,sc=.95,behind=True,word='crowded',d=.5)])
S(149.18,'two_shot','normal','handheld',C(1.16,1.22,0,20,0,0),'shaky camera as the claws reach',
  'One demon reached for Kacha\'s throat.',
  'The green demon lunges with clawed hands at Kacha\'s throat; Kacha flinches back with fear.',
  'asura2',feast(),'violence',
  [F('kacha',520,690,.88,1,'fear',look='asura2',tilt=-.1,mood={'wide':.7}),F('asura2',800,692,.9,-1,'fury',look='kacha',actions=[A('reached',pose='grasp',e='antic',d=.5)])],shake=3)
S(150.69,'low_angle','wide','tilt_up',C(1.06,1.16,0,0,30,-10),'low angle: the guru\'s command towers over everyone',
  'Then Shukracharya shouted for them to stop.',
  'Shukracharya raises his palm high and shouts with a furious face, his white beard lit by the fire; his name appears.',
  'shukracharya',feast(),'authority',
  [F('shukracharya',640,716,.98,1,'fury',talk=.8,actions=[A('Shukracharya',pose='raise',e='spring',d=.5)])],
  [NAME('Shukracharya',640,96,'Shukracharya')],tr='flash')
S(153.07,'two_shot','normal','dolly_left',C(1.1,1.16,30,-20,0,0),'slide to the thread he points at',
  'He said the thread on Kacha\'s wrist bound him to protect his student.',
  'Shukracharya points at Kacha\'s raised wrist where the red sacred thread glows; Kacha holds it up, calm.',
  'sacred thread',feast(),'protection',
  [F('shukracharya',840,690,.88,-1,'fury',pose='point',talk=.6,look='kacha'),F('kacha',470,690,.86,1,'calm',look='shukracharya',actions=[A('thread',pose='raise',d=.5)])],
  [X('glow',540,380,90,'the sacred thread lights up',rgb='255,120,60',ga=.6,word='thread')])
S(156.99,'medium','normal','push_in',C(1.04,1.12,0,0,0,0),'push in on the order',
  'He ordered the demons to treat Kacha as one of their own.',
  'Shukracharya points his finger at the demons, who lower their heads; Kacha stands behind the guru, protected.',
  'shukracharya',feast(),'command',
  [F('kacha',330,690,.82,1,'calm',look='shukracharya'),F('shukracharya',600,690,.9,1,'fury',pose='point',talk=.7,look='asura1'),
   F('asura1',960,692,.84,-1,'fear',look='shukracharya',actions=[A('ordered',pose='bow',emo='shame',d=.7)])])
S(160.36,'wide','wide','pull_out',C(1.12,1.0,0,0,0,0),'pull back as the demons give him room',
  'The demons backed away.',
  'The demons slink back toward the dark arches; Kacha is left alone in the firelight with a hidden cold smile.',
  'kacha',feast(),'false calm',
  [F('kacha',560,690,.84,1,'coldsmile',look=1000),F('asura1',920,692,.8,-1,'shame',look='kacha',walk={'word':'demons','to_x':1180,'d':1.2,'speed':.8}),
   F('asura2',760,692,.78,-1,'fury',look='kacha',walk={'word':'backed','to_x':1060,'d':1.0,'speed':.8})])
# ================= B09 Devayani storms in =================
S(161.98,'wide','normal','handheld',C(1.02,1.08,-30,0,10,10),'restless camera for her storming anger',
  'That night, Devayani stormed into Kacha\'s room, shaking with anger.',
  'In the lamp-lit room Devayani strides in from the left with furious red eyes and clenched face; Kacha stands by his bed, surprised.',
  'devayani',room(),'anger',
  [F('devayani',150,680,.86,1,'fury',look='kacha',walk={'word':'Devayani','to_x':500,'d':1.3,'speed':1.4}),F('kacha',880,680,.86,-1,'surprise',look='devayani')],tr='fade',shake=2)
S(165.81,'two_shot','normal','push_in',C(1.08,1.18,40,60,0,0),'push in on the soothing hands',
  'Kacha soothed the angry Devayani.',
  'Kacha holds his hands out gently and speaks softly; Devayani\'s furious face melts into calm.',
  'kacha',room(),'tender manipulation',
  [F('kacha',560,680,.88,1,'love',pose='hold',talk=.4,look='devayani'),F('devayani',800,680,.86,-1,'fury',look='kacha',actions=[A('Kacha',emo='calm',d=.7,mood={'smile':.3})])])
S(167.28,'medium','normal','pan_left',C(1.08,1.1,0,-80,0,0),'pan with her as she leaves',
  'She left, calm again.',
  'Devayani turns and walks out to the left with a soft smile; Kacha watches her go with a cold, satisfied look.',
  'devayani',room(),'false peace',
  [F('devayani',560,680,.86,1,'love',look='kacha',turn_on='She',turn_d=.4,walk={'word':'left','to_x':220,'d':1.2,'speed':.9}),F('kacha',880,680,.86,-1,'coldsmile',look='devayani')])
S(169.07,'high_angle','normal','crane_up',C(1.18,1.1,0,0,40,40),'look down on him lying awake',
  'Kacha lay awake in the dark.',
  'From above, Kacha lies on his low bed in the dark room, eyes wide open, staring at the ceiling.',
  'kacha',room(bx=640),'sleepless',
  [F('kacha',640,560,.78,1,'calm',pose='sleep',mat=False,mood={'blink':0,'ly':-.5},actions=[A('awake',mood={'blink':0,'wide':.3})])])
S(170.36,'medium','normal','dolly_right',C(1.06,1.12,-30,30,0,0),'slide past the plotting demons',
  'The demons wanted Kacha dead.',
  'In the dim feast hall two demons whisper over a low fire with red eyes; the brute points out toward Kacha\'s room, murder on his face.',
  'asura1',feast(fire=.45),'murderous',
  [F('asura2',500,692,.84,1,'scheme',talk=.5,look='asura1'),F('asura1',800,692,.86,-1,'fury',look='asura2',actions=[A('dead',pose='point',d=.5)])],tr='wipe')
S(172.40,'close','tele','push_in',C(1.1,1.22),'push in on his satisfied face in the dark',
  'Exactly as Kacha had planned.',
  'Kacha\'s face in the lamplight, eyes open in the dark, lips curling into a cold smile.',
  'kacha',room(),'cold satisfaction',
  [F('kacha',640,340,1.15,1,'calm',head=True,mood={'blink':.2},actions=[A('Exactly',emo='coldsmile',d=.6)])],tr='wipe')
# ================= B10 stage two: the forest =================
S(174.23,'wide','wide','pan_right',C(1.0,1.04,-60,40,0,0),'pan with the boy and the horses into the woods',
  'Stage two: at dawn, Kacha took the guru\'s horses to graze.',
  'At dawn Kacha walks into the smoky forest leading two bay horses; the words Stage two appear.',
  'kacha',forest(smoke=.6),'quiet dread',
  [F('kacha',300,690,.8,1,'calm',look=900,walk={'word':'Kacha','to_x':560,'d':2.4,'speed':.9}),
   F('horse',690,660,.56,1,'calm',look=1200,walk={'word':'took','to_x':900,'d':2.4,'speed':.8}),F('horse',900,650,.5,1,'calm',look=1200,walk={'word':'horses','to_x':1100,'d':2.2,'speed':.8})],
  [TEXT('Stage two',640,96,'Stage','the second stage of the plan begins',54)],tr='fade')
S(178.57,'medium','normal','push_in',C(1.04,1.14,0,0,0,0),'push in as he halts deep in the trees',
  'Deep in the forest, Kacha stopped.',
  'Deep among black trunks and smoke Kacha halts and stands still, while the horses graze behind him.',
  'kacha',forest(smoke=1),'stillness',
  [F('kacha',560,690,.88,1,'calm',look=1000,walk={'word':'Deep','to_x':620,'d':.9,'speed':.8}),F('horse',960,655,.55,-1,'calm',pose='bow',look=600)])
S(180.82,'medium','tele','static',C(1.2,1.2,0,0,0,0),'hold still while he waits',
  'And Kacha waited, perfectly still.',
  'Kacha stands motionless in the smoky dawn light, eyes half closed, breathing slowly.',
  'kacha',forest(smoke=1),'waiting',
  [F('kacha',640,690,.92,1,'calm',look=900,mood={'blink':.45})])
S(181.87,'wide','wide','dolly_left',C(1.06,1.1,40,-30,0,0),'track along the trees where eyes appear',
  'He was waiting for the demons.',
  'Between the far tree trunks rows of red ember eyes glow in the smoke; Kacha stands small in the right foreground, facing them.',
  'demons',forest(demons=1,smoke=1),'menace',
  [F('kacha',1000,690,.84,-1,'calm',look=400)])
S(183.83,'close','tele','push_in',C(1.08,1.2),'push in on his calm certainty',
  'The demons were angry at him, and he knew they would come.',
  'Kacha\'s face in close-up in the dawn smoke: calm, and on "and" a small knowing smile.',
  'kacha',forest(smoke=1),'certainty',
  [F('kacha',640,340,1.15,1,'calm',head=True,look=300,actions=[A('and',emo='coldsmile',d=.5)])])
S(186.65,'wide','normal','pan_right',C(1.05,1.1,-40,40,0,0),'whip toward the sound',
  'Then a twig cracked. The demons were coming.',
  'The grazing horse jerks its head up and Kacha turns toward the sound as horned silhouettes with red eyes loom out of the smoke.',
  'demons',forest(demons=2,smoke=1),'alarm',
  [F('kacha',400,690,.84,1,'calm',look=1000,actions=[A('cracked',emo='shock',d=.4)]),F('horse',700,655,.55,1,'calm',pose='bow',look=1100,actions=[A('twig',pose='stand',d=.5)])],shake=1)
# ================= B11 the circle closes =================
S(189.43,'medium','normal','crane_down',C(1.04,1.12,0,0,-30,0),'descend to the fire he lights',
  'Kacha piled up branches and lit a fire.',
  'Kacha kneels on the forest floor beside a pile of branches; a fire flares up in front of him.',
  'kacha',forest(demons=1,smoke=.8),'ritual',
  [F('kacha',500,700,.9,1,'calm',pose='kneel',look=700,actions=[A('lit',mood={'ly':.6})])],
  [X('ember_fire',730,712,170,'the fire Kacha lights for himself',word='up',d=.8)])
S(191.85,'low_angle','wide','tilt_up',C(1.06,1.14,0,0,30,0),'ground-level view of the approaching feet',
  'The demons\' footsteps grew louder.',
  'Huge black demon silhouettes stride in at both sides of the frame, close to the camera; small in the middle Kacha kneels at his fire.',
  'demons',forest(demons=2,smoke=.8,near=False),'approach',
  [F('kacha',640,650,.6,1,'calm',pose='kneel',look=640,mood={'ly':.7})],
  [X('ember_fire',740,662,110,'his small fire',behind=True),X('demon_crowd',640,800,1700,'giant demon legs and bodies close to the camera',rows=1,n=4,seed=71,sc=2.0)])
S(194.08,'wide','normal','handheld',C(1.12,1.2,0,0,0,0),'shaking camera as they close in',
  'The demons came closer and closer.',
  'Rows of horned demons with glowing eyes stand right behind kneeling Kacha, much closer now, their weapons raised.',
  'demons',forest(demons=2,smoke=.6),'tightening',
  [F('kacha',640,700,.86,1,'calm',pose='kneel',mood={'ly':.8,'blink':.4},actions=[A('Closer',tilt=.05)])],
  [X('demon_crowd',640,640,1500,'the ring of demons closing in',rows=2,n=6,seed=73,sc=1.2,behind=True),X('ember_fire',820,712,130,'his small fire')],shake=3)
S(195.92,'close','tele','push_in',C(1.1,1.2),'push in on his lowered eyes',
  'Kacha never looked up. He only watched their feet.',
  'Kacha\'s face lit from below by the fire, eyes cast down to the ground, never lifting.',
  'kacha',forest(demons=1,smoke=.8),'restraint',
  [F('kacha',640,330,1.15,1,'calm',head=True,mood={'ly':.95,'blink':.55},actions=[A('feet',mood={'ly':1,'lx':.3})])],
  [X('glow',640,560,260,'firelight from below on his face',rgb='255,120,50',ga=.4)])
S(199.16,'medium','normal','pull_out',C(1.16,1.06),'pull out to show him sitting still among them',
  'He did not run. He did not fight.',
  'Kacha kneels with hands on his knees by the fire, absolutely still, while demon silhouettes stand on both sides.',
  'kacha',forest(demons=2,smoke=.6),'surrender',
  [F('kacha',600,700,.9,1,'calm',pose='kneel',mood={'blink':.6},actions=[A('fight',mood={'blink':.9})])],
  [X('ember_fire',820,712,140,'his fire still burns',behind=True)])
S(201.56,'low_angle','wide','tilt_up',C(1.04,1.14,0,0,40,0),'low angle on the weapons',
  'The demons had knives and claws.',
  'Two demons loom from below: the green one bares his claws and short sword, the brute lifts his mace, both with burning red eyes.',
  'asura2',forest(demons=1,smoke=.8),'threat',
  [F('asura2',500,720,1.0,1,'fury',pose='grasp',look='asura1',actions=[A('claws',mood={'anger':1,'mouth':.7})]),F('asura1',830,720,1.0,-1,'fury',pose='raise',look=300)])
S(203.90,'high_angle','wide','crane_up',C(1.08,1.0,0,0,40,0),'rise to see the whole ring',
  'They stood all around him.',
  'From above, kneeling Kacha is a small lit figure inside a dense ring of horned silhouettes that blots out the dawn.',
  'kacha',forest(demons=2,smoke=1,sx=640,sy=380),'encircled',
  [F('kacha',640,680,.66,1,'calm',pose='kneel',look=640,mood={'ly':.9})],
  [X('demon_crowd',640,650,1600,'the closed ring of demons',rows=3,n=8,seed=80,sc=1.0,behind=True),X('demon_crowd',640,780,1800,'the near side of the ring',rows=1,n=6,seed=82,sc=1.5)])
S(205.60,'medium','tele','handheld',C(1.2,1.26),'tremble with his body',
  'His body shook, but his mind was calm.',
  'Close on kneeling Kacha: his body trembles and his face shows pain, then on "but" his face settles into calm.',
  'kacha',forest(demons=2,smoke=.8),'inner calm',
  [F('kacha',640,700,1.0,1,'pain',pose='kneel',actions=[A('but',emo='calm',d=.6)])],shake=3)
S(208.53,'extreme_close','tele','push_in',C(1.3,1.4),'push in on the calm planner\'s smile',
  'Everything was going as he had planned.',
  'Extreme close-up of Kacha\'s face in firelight: the faint cold smile of a plan working.',
  'kacha',forest(demons=1,smoke=.8),'control',
  [F('kacha',640,360,1.35,1,'coldsmile',head=True,mood={'ly':.6},actions=[A('planned',mood={'smirk':1})])])
S(210.74,'low_angle','wide','dutch',C(1.06,1.12,0,0,20,0,0,.04),'the frame tilts as the weapons rise',
  'He was going to die, but he would not stay dead.',
  'Kacha kneels with his eyes closed as the demons behind him raise their weapons high over his head.',
  'kacha',forest(demons=2,smoke=.8),'doomed',
  [F('kacha',640,700,.88,1,'calm',pose='kneel',mood={'blink':1},actions=[A('die',mood={'blink':1,'smile':.2})]),
   F('asura2',400,690,.86,1,'fury',pose='throw',look='kacha'),F('asura1',880,690,.86,-1,'fury',pose='raise',look='kacha')])
# ================= B12 death and the wine =================
S(213.85,'medium','normal','handheld',C(1.12,1.2),'violent shake on the blow',
  'The demons killed Kacha.',
  'The green demon slashes down on "killed" and Kacha collapses; a red pulse flashes across the forest.',
  'kacha',forest(demons=2,smoke=.8),'violence',
  [F('kacha',620,700,.88,1,'pain',pose='kneel',actions=[A('killed',pose='collapse',emo='pain',d=.4,e='antic')]),
   F('asura2',860,692,.9,-1,'fury',pose='throw',look='kacha',actions=[A('demons',pose='lunge',d=.4,e='antic')])],
  [X('red_energy_pulse',620,480,420,'the death blow',word='killed',alpha=.6)],tr='flash',shake=6)
S(215.52,'wide','wide','crane_up',C(1.04,1.1,0,0,20,-20),'rise with the smoke of the pyre',
  'They burned his body and ground the ashes to powder.',
  'A big fire burns in the clearing with demon silhouettes around it; beside it a grey pile of ash grows where the body was.',
  'fire',forest(demons=2,smoke=1),'grim',
  [F('asura1',920,692,.86,-1,'coldsmile',look=600,actions=[A('ground',pose='hold',d=.5)])],
  [X('ember_fire',560,700,300,'the fire burning Kacha\'s body',word='burned',d=.4),X('ash_pile',800,690,160,'Kacha\'s body ground to powder',word='ground',d=.6)])
S(218.65,'insert','tele','crane_down',C(1.1,1.2,0,0,-30,0),'follow the powder into the cup',
  'They stirred the powder into Shukracharya\'s wine.',
  'The golden wine cup fills the frame, grey powder swirling in it while black flakes fall in; the plum demon watches with a sly grin.',
  'wine cup',feast(near=False),'treachery',
  [F('asura3',260,340,1.0,1,'scheme',head=True,look=640,actions=[A('stirred',mood={'smirk':.9})])],
  [X('wine_cup',680,420,300,'Kacha\'s ashes in the guru\'s wine',ash=1),X('ash_speck',680,240,150,'Kacha\'s ash falling in',vy=40)],tr='fade')
S(221.35,'two_shot','normal','dolly_right',C(1.06,1.12,-20,30,0,0),'slide with the cup toward the guru',
  'The demons did it the way they had done with the deer.',
  'The plum demon offers the wine cup with a cold smile; Shukracharya reaches for it, smiling, suspecting nothing.',
  'asura3',feast(),'deceit',
  [F('asura3',480,694,.86,1,'coldsmile',pose='hold',prop='cup',ash=1,look='shukracharya'),F('shukracharya',840,690,.88,-1,'joy',look='asura3',actions=[A('way',pose='hold',d=.6)])])
S(223.16,'low_angle','normal','tilt_up',C(1.08,1.18,0,0,30,-10),'look up as the cup goes down',
  'Shukracharya drank the whole cup.',
  'Shukracharya tips the ash-swirled cup to his lips and drains it, eyes closed, beard lit by the fire.',
  'shukracharya',feast(),'unknowing',
  [F('shukracharya',640,716,.98,1,'calm',pose='raise',prop='cup',ash=1,mood={'blink':.6},actions=[A('drank',mood={'blink':1,'mouth':.5})])])
S(225.54,'medium','normal','push_in',C(1.04,1.14,0,0,0,0),'push in on the belly where Kacha now lies',
  'Shukracharya did not know that he had just swallowed Kacha.',
  'Shukracharya rests a hand on his belly with a satisfied smile while a faint red glow pulses inside him.',
  'shukracharya',feast(),'dramatic irony',
  [F('shukracharya',640,700,.94,1,'joy',pose='hold',mood={'smile':.6,'blink':.4},actions=[A('swallowed',mood={'smile':.8,'blink':.6})])],
  [X('glow',640,520,90,'Kacha\'s ash inside the guru',word='swallowed',rgb='255,60,30',ga=.6,pulse=1)])
# ================= B13 the burnt cloth =================
S(228.70,'wide','normal','dolly_left',C(1.04,1.1,30,-20,0,0),'track her stumbling out of the dark trees',
  'That night, Devayani stumbled out of the forest.',
  'In the black night forest Devayani stumbles out from between the trunks, bent with grief, a scrap of cloth in her hand.',
  'devayani',forest(night=True,smoke=.5),'grief',
  [F('devayani',920,690,.84,-1,'grief',prop='cloth',look=300,walk={'word':'Devayani','to_x':640,'d':1.6,'speed':.6},tilt=.08)],tr='fade')
S(231.50,'insert','tele','push_in',C(1.04,1.12),'push into the cloth',
  'She was holding a piece of burnt cloth.',
  'A charred scrap of Kacha\'s saffron cloth fills the right of the frame, holes burnt through it; Devayani\'s tear-stained face looks at it.',
  'burnt cloth',forest(night=True,smoke=.5),'loss',
  [F('devayani',400,360,1.05,1,'grief',head=True,look=800,actions=[A('burnt',mood={'tears':1})])],
  [X('burnt_cloth',830,330,230,'all that is left of Kacha',word='burnt',d=.3)])
S(233.62,'two_shot','normal','pan_right',C(1.04,1.1,-30,30,0,0),'pan from daughter to father',
  'She stood before her father, Shukracharya.',
  'In the night ashram yard Devayani stands with the cloth before her father; Shukracharya turns to her, and his name appears.',
  'devayani',ashram(night=True),'confrontation',
  [F('devayani',440,676,.86,1,'grief',prop='cloth',look='shukracharya'),F('shukracharya',860,676,.88,-1,'calm',look='devayani',actions=[A('father',emo='doubt')])],
  [NAME('Shukracharya',860,110,'father'),X('ember_fire',640,612,110,'the yard fire',behind=True)],tr='fade')
S(236.21,'medium','normal','push_in',C(1.08,1.18,-40,-60,0,0),'push in on the cloth held out',
  'She told him the cloth was all that was left of Kacha.',
  'Devayani holds the burnt cloth out to her father, tears running, her voice breaking.',
  'devayani',ashram(night=True),'grief',
  [F('devayani',480,676,.9,1,'grief',pose='hold',prop='cloth',talk=.5,look='shukracharya',mood={'tears':1}),F('shukracharya',880,676,.88,-1,'doubt',look='devayani')])
S(239.05,'two_shot','normal','dolly_left',C(1.1,1.14,20,-20,0,0),'slide along her accusing finger',
  'His demons had killed Kacha.',
  'Devayani points at her father in grief and anger; Shukracharya recoils in shock.',
  'devayani',ashram(night=True),'accusation',
  [F('devayani',460,676,.88,1,'grief',pose='point',look='shukracharya',talk=.4),F('shukracharya',860,676,.88,-1,'shock',look='devayani')])
S(240.93,'low_angle','wide','tilt_up',C(1.04,1.14,0,0,30,-10),'low angle on his fury',
  'Shukracharya said he would punish every one of the demons.',
  'Shukracharya raises his fist-like palm high with a furious face, shouting vengeance in the firelit night yard.',
  'shukracharya',ashram(night=True),'fury',
  [F('shukracharya',640,716,1.0,1,'fury',talk=.8,actions=[A('punish',pose='raise',e='spring',d=.5)])],
  [X('ember_fire',980,612,120,'the yard fire flares',behind=True)])
S(243.90,'medium','tele','static',C(1.18,1.18),'freeze with him',
  'Then Shukracharya suddenly stopped.',
  'Shukracharya freezes mid-gesture, his anger turning to puzzlement as he looks at his daughter.',
  'shukracharya',ashram(night=True),'confusion',
  [F('shukracharya',640,700,.92,1,'fury',pose='raise',look=300,actions=[A('stopped',emo='doubt',d=.4)])])
S(245.16,'close','tele','push_in',C(1.1,1.2),'push in on her laugh',
  'Devayani was laughing.',
  'Devayani\'s face in close-up: she is laughing, mouth open, eyes wet.',
  'devayani',ashram(night=True),'hysteria',
  [F('devayani',640,330,1.15,1,'laughcry',head=True,mood={'tears':.6},actions=[A('laughing',mood={'laugh':1})])])
S(246.72,'extreme_close','tele','dutch',C(1.3,1.36,0,0,0,0,0,-.04),'tilted frame for her breaking mind',
  'Tears poured down her face, and she was laughing.',
  'Extreme close-up of Devayani: tears stream down her cheeks while she laughs wildly.',
  'devayani',ashram(night=True),'laughing while crying',
  [F('devayani',640,350,1.4,1,'laughcry',head=True,mood={'tears':1,'laugh':1},actions=[A('Tears',tilt=-.08)])])
S(249.81,'two_shot','normal','pull_out',C(1.14,1.04),'pull back to reveal his horror',
  'She asked how he could punish them, when he had drunk Kacha himself.',
  'Laughing and crying, Devayani points at her father\'s belly; Shukracharya\'s face fills with horror.',
  'shukracharya',ashram(night=True),'realisation',
  [F('devayani',440,676,.88,1,'laughcry',pose='point',talk=.5,look='shukracharya'),F('shukracharya',860,676,.9,-1,'doubt',look='devayani',actions=[A('punish',emo='horror',d=.6)])])
S(254.02,'close','tele','dolly_right',C(1.1,1.16,-20,20,0,0),'slide to the speck on his lips',
  'She wiped a black speck from his lips.',
  'Devayani\'s face close on the left as she reaches toward her father; on the right a black speck of ash glints on his white beard by his lips.',
  'ash speck',ashram(night=True),'discovery',
  [F('devayani',380,350,1.0,1,'grief',head=True,look='shukracharya'),F('shukracharya',880,340,1.05,-1,'horror',head=True,look='devayani')],
  [X('ash_speck',862,415,34,'the black speck of Kacha\'s ash on his lips',word='black',d=.3),X('glow',862,415,60,'the speck catches the firelight',rgb='255,150,80',ga=.4,word='black')])
S(256.44,'insert','tele','push_in',C(1.08,1.18),'push into the speck of ash',
  'The speck was Kacha\'s ash.',
  'The black ash flakes, huge in the centre, glow on Devayani\'s fingertip; her face on the left and her father\'s on the right stare at it.',
  'ash speck',ashram(night=True,near=False),'horror',
  [F('devayani',260,380,.9,1,'shock',head=True,look=640),F('shukracharya',1020,380,.9,-1,'horror',head=True,look=640)],
  [X('ash_speck',640,330,190,'Kacha\'s ash on her finger'),X('glow',640,330,200,'the ash in the firelight',rgb='255,130,60',ga=.35)])
S(258.02,'medium','normal','pan_left',C(1.08,1.12,40,-40,0,0),'memory: pan across the demon who poisoned the cup',
  'The demons had put Kacha\'s ash in his wine.',
  'In a remembered flash of the feast hall, the plum demon grins and holds up the ash-swirled wine cup.',
  'asura3',feast(fire=.6),'betrayal',
  [F('asura3',640,694,.92,1,'coldsmile',pose='raise',prop='cup',ash=1,look=300)],tr='iris')
# ================= B14 the price =================
S(260.15,'close','tele','push_in',C(1.1,1.2),'push in as he shuts his eyes',
  'Shukracharya closed his eyes in horror.',
  'Shukracharya\'s face, brows twisted in horror, eyes squeezing shut on "closed".',
  'shukracharya',ashram(night=True),'horror',
  [F('shukracharya',640,340,1.15,1,'horror',head=True,actions=[A('closed',mood={'blink':1},d=.5)])],tr='iris')
S(262.65,'low_angle','wide','tilt_up',C(1.04,1.12,0,0,30,-10),'low angle for a pronouncement',
  'Then he spoke: from that day, he said.',
  'Shukracharya stands tall in the night yard and raises his hand to make a solemn declaration.',
  'shukracharya',ashram(night=True),'judgement',
  [F('shukracharya',640,716,1.0,1,'fury',talk=.7,actions=[A('spoke',pose='raise',d=.6)])])
S(265.47,'medium','normal','pull_out',C(1.14,1.04),'pull out from the cursing hand',
  'Any Brahmin who drinks wine will lose his wisdom and his virtue.',
  'Shukracharya flings the wine cup to the ground with a furious curse, a red curse-ring flaring round his raised hand.',
  'shukracharya',ashram(night=True),'curse',
  [F('shukracharya',640,700,.94,1,'fury',pose='raise',talk=.8,actions=[A('wine',mood={'anger':1})])],
  [X('curse_glow',720,330,220,'his curse on wine',word='drinks',d=.4),X('wine_cup',880,640,90,'the cup he throws away',rot=1.7,ash=1)])
S(269.58,'close','tele','push_in',C(1.08,1.18),'push in on his guilt',
  'He had failed to keep Kacha safe.',
  'Shukracharya looks down in pain and shame; the memory of the red sacred thread he tied glows faintly beside him.',
  'shukracharya',ashram(night=True),'guilt',
  [F('shukracharya',560,340,1.1,1,'pain',head=True,mood={'ly':.8},actions=[A('failed',mood={'ly':1,'tears':.5})])],
  [X('sacred_thread',960,350,200,'the promise he broke',alpha=.6,word='failed')])
S(271.85,'two_shot','normal','dolly_left',C(1.06,1.12,20,-30,0,0),'slide to her firm face',
  'Devayani told him he knew what he had to do.',
  'Devayani faces her father firmly, hands open, telling him; Shukracharya listens with a heavy face.',
  'devayani',ashram(night=True),'determination',
  [F('devayani',460,676,.88,1,'calm',pose='open',talk=.6,look='shukracharya',mood={'anger':.3}),F('shukracharya',860,676,.9,-1,'pain',look='devayani')])
S(274.55,'close','tele','crane_down',C(1.1,1.18,0,0,-20,0),'settle on him as he accepts',
  'He did: he had to use Mritasanjivani.',
  'Shukracharya nods slowly in close-up, a gold yantra glowing behind him as the word Mritasanjivani appears.',
  'shukracharya',ashram(night=True),'acceptance',
  [F('shukracharya',640,340,1.15,1,'calm',head=True,actions=[A('did',tilt=.1,mood={'blink':.6})])],
  [X('magic_circle',640,300,560,'the mantra of the dead',behind=True,alpha=.45,word='use'),TEXT('Mritasanjivani',640,100,'use','the mantra he must use',56)])
S(277.56,'medium','normal','push_in',C(1.04,1.16,0,0,0,0),'push in on the boy inside him',
  'But Kacha was inside him.',
  'Shukracharya lays a hand on his belly, where a small red-glowing figure of Kacha is curled up inside him.',
  'shukracharya',ashram(night=True),'trapped life',
  [F('shukracharya',640,700,.94,1,'pain',pose='hold',mood={'ly':.7},actions=[A('inside',tilt=.08,mood={'ly':1})]),
   F('kacha',650,560,.26,1,'calm',pose='kneel',look=640,filt='brightness(.5) sepia(1) saturate(3) hue-rotate(-25deg)',rim='rgba(255,80,40,.9)')],
  [X('glow',650,500,110,'the life of Kacha glowing in the guru\'s belly',rgb='255,60,30',ga=.6,pulse=1)])
S(279.66,'two_shot','normal','dolly_right',C(1.06,1.12,-30,20,0,0),'slide between the girl and the father who must break',
  'To rise again, Kacha would have to tear his body apart.',
  'Devayani stares in shock as a red pulse throbs in her father\'s belly, the place Kacha would have to tear open.',
  'shukracharya',ashram(night=True),'dread',
  [F('devayani',440,676,.86,1,'shock',look='shukracharya',actions=[A('tear',emo='horror',d=.5)]),F('shukracharya',860,676,.9,-1,'pain',look='devayani')],
  [X('red_energy_pulse',860,520,200,'his body that must be torn',word='rise')])
S(283.33,'medium','normal','pull_out',C(1.14,1.06),'pull back on his quiet sacrifice',
  'Shukracharya said he was willing.',
  'Shukracharya folds his hands calmly and smiles at his daughter with love: he accepts.',
  'shukracharya',ashram(night=True),'sacrifice',
  [F('shukracharya',700,690,.94,-1,'love',talk=.5,look=300,actions=[A('willing',pose='namaste',d=.6)])])
S(285.68,'close','tele','push_in',C(1.12,1.22),'push in on her frozen face',
  'Devayani froze in shock.',
  'Devayani\'s face freezes in shock, eyes wide and mouth open.',
  'devayani',ashram(night=True),'shock',
  [F('devayani',640,340,1.15,1,'shock',head=True,look=900,actions=[A('froze',mood={'wide':1})])])
S(287.26,'medium','tele','dolly_left',C(1.16,1.2,30,-10,0,0),'drift with her realisation',
  'She had begged for a life, and not seen the price.',
  'Devayani in the foreground clutches the burnt cloth, pain on her face; behind her, out of focus, her father stands waiting.',
  'devayani',ashram(night=True),'remorse',
  [F('devayani',480,690,.96,1,'pain',prop='cloth',look=200),F('shukracharya',940,660,.72,-1,'love',look='devayani',filt='brightness(.6) blur(1.5px)')])
S(290.72,'close','tele','pull_out',C(1.12,1.04),'pull back to the three faces: a life for a life',
  'Kacha\'s life demanded another life: her father\'s.',
  'Devayani\'s pained face in the centre; on the left Kacha\'s face glows red like a ghost, on the right her father\'s face waits in the dark.',
  'devayani',ashram(night=True,near=False),'impossible choice',
  [F('devayani',640,340,1.1,1,'pain',head=True,look=1000,actions=[A('another',look=250,d=.5)]),
   F('kacha',250,380,.82,1,'calm',head=True,look='devayani',filt='brightness(.55) sepia(1) saturate(2) hue-rotate(-25deg)'),
   F('shukracharya',1030,380,.82,-1,'love',head=True,look='devayani',filt='brightness(.6) saturate(.6)')])
# ================= B15 the mantra =================
S(294.63,'medium','normal','push_in',C(1.06,1.16,-30,-40,0,0),'push in on her cry',
  'She cried out that she could not live without her father.',
  'Devayani begs with outstretched hands, crying, toward her father.',
  'devayani',ashram(night=True),'despair',
  [F('devayani',500,690,.9,1,'grief',pose='plead',talk=.6,look='shukracharya',mood={'tears':1}),F('shukracharya',900,676,.86,-1,'pain',look='devayani')])
S(297.64,'close','tele','static',C(1.08,1.08),'the same balanced frame as before: her love on two sides',
  'She loved them both. Not more. Not less.',
  'Devayani\'s crying face in the centre with Kacha\'s face on the left and her father\'s on the right, exactly balanced.',
  'devayani',ashram(night=True,near=False),'torn',
  [F('devayani',640,340,1.1,1,'grief',head=True,look=640,actions=[A('both',mood={'tears':1})]),
   F('kacha',250,380,.82,1,'calm',head=True,look='devayani',filt='brightness(.55) saturate(.6)'),
   F('shukracharya',1030,380,.82,-1,'love',head=True,look='devayani',filt='brightness(.55) saturate(.6)')])
S(300.88,'low_angle','normal','tilt_up',C(1.04,1.12,0,0,30,-10),'low angle on the hard demand',
  'Shukracharya said she must choose.',
  'Shukracharya stands over her with open hands like two pans of a scale, his face stern.',
  'shukracharya',ashram(night=True),'ultimatum',
  [F('shukracharya',640,716,.98,1,'calm',pose='open',talk=.6,mood={'anger':.4},actions=[A('choose',tilt=-.05)])])
S(303.39,'medium','normal','dolly_right',C(1.08,1.12,-40,30,0,0),'slide from the cloth to the father as her eyes move',
  'She must choose: Kacha or her father.',
  'Devayani looks to the glowing burnt cloth of Kacha on the left, then to her father on the right, torn.',
  'devayani',ashram(night=True),'dilemma',
  [F('devayani',560,690,.9,1,'pain',look=200,actions=[A('or',look='shukracharya',d=.4)]),F('shukracharya',940,676,.86,-1,'calm',look='devayani')],
  [X('burnt_cloth',230,330,150,'Kacha, what is left of him'),X('glow',230,320,160,'the cloth glows like a memory',rgb='255,120,60',ga=.4)])
S(304.86,'close','tele','push_in',C(1.1,1.22),'push in as her eyes light up',
  'Her eyes lit up. She said she did not have to choose.',
  'Devayani\'s face lights up: eyes wide, a hopeful smile breaking through her tears.',
  'devayani',ashram(night=True),'hope',
  [F('devayani',640,340,1.15,1,'grief',head=True,actions=[A('lit',emo='joy',mood={'wide':.7,'tears':.5},d=.5)])],
  [X('glow',640,320,300,'the light of her idea',rgb='255,190,110',ga=.3,word='lit')])
S(308.44,'two_shot','normal','dolly_left',C(1.06,1.12,30,-20,0,0),'slide to her outstretched hands',
  'She asked him for the mantra.',
  'Devayani holds out both hands to her father, pleading; Shukracharya hesitates.',
  'devayani',ashram(night=True),'asking',
  [F('devayani',480,690,.9,1,'joy',pose='plead',talk=.6,look='shukracharya'),F('shukracharya',880,676,.88,-1,'doubt',look='devayani')])
S(310.08,'two_shot','normal','pull_out',C(1.12,1.04),'pull back to both as she explains',
  'When Kacha came out of him, she would bring him back.',
  'Devayani explains eagerly, gesturing with open hands; her father listens, doubtful.',
  'devayani',ashram(night=True),'eager',
  [F('devayani',460,690,.88,1,'joy',pose='open',talk=.7,look='shukracharya'),F('shukracharya',860,676,.88,-1,'doubt',look='devayani',actions=[A('back',tilt=.06)])])
S(313.03,'wide','normal','crane_down',C(1.0,1.08,0,0,-40,0),'memory: descend on the old sage praying for ages',
  'He had prayed for a thousand years to earn this secret.',
  'In memory, Shukracharya sits cross-legged in prayer before the dark peaks of Kailash, a golden yantra glowing behind him.',
  'shukracharya',kailash(),'devotion',
  [F('shukracharya',640,660,.9,1,'calm',pose='sitpray',mood={'blink':1,'mouth':.2},actions=[A('prayed',tilt=.04)])],
  [X('magic_circle',640,360,480,'his thousand years of prayer',behind=True,alpha=.5)],tr='iris')
S(316.36,'close','tele','push_in',C(1.1,1.2),'push in on her pleading eyes',
  'And his daughter asked if he did not trust her.',
  'Devayani\'s face pleads with soft wet eyes and raised brows.',
  'devayani',ashram(night=True),'pleading',
  [F('devayani',640,340,1.15,1,'love',head=True,talk=.5,look=1000,mood={'sad':.5,'brow':.6})],tr='iris')
S(319.05,'close','tele','static',C(1.12,1.12),'hold while he gives in',
  'Then Shukracharya nodded yes.',
  'Shukracharya\'s face softens with love and he nods.',
  'shukracharya',ashram(night=True),'trust',
  [F('shukracharya',640,340,1.15,-1,'calm',head=True,look=300,actions=[A('nodded',emo='love',tilt=.12,d=.4)])])
S(320.55,'insert','tele','crane_down',C(1.1,1.18,0,0,-20,0),'descend onto the writing',
  'He wrote the mantra down.',
  'Seated Shukracharya writes on a glowing palm leaf held in his hand, letters of light appearing on it.',
  'palm leaf',ashram(night=True),'gift',
  [F('shukracharya',640,660,.94,1,'calm',pose='sit',mood={'ly':.8},talk=.3)],
  [X('palm_leaf',640,520,320,'the mantra written on a palm leaf',glow=1,word='wrote',d=.3)])
S(321.98,'two_shot','normal','dolly_right',C(1.06,1.12,-20,30,0,0),'slide from the leaf to his warning finger',
  'He told her to use it once, and then destroy it.',
  'Devayani holds the glowing palm leaf; her father raises one warning finger at her.',
  'devayani',ashram(night=True),'warning',
  [F('devayani',460,690,.9,1,'joy',pose='hold',prop='leaf',glow=.8,look='shukracharya'),F('shukracharya',860,676,.9,-1,'calm',pose='point',talk=.6,look='devayani',mood={'anger':.2})])
S(325.33,'medium','normal','push_in',C(1.12,1.2),'push in on her promise',
  'Devayani promised to destroy it.',
  'Devayani presses the glowing leaf to her chest and nods solemnly.',
  'devayani',ashram(night=True),'vow',
  [F('devayani',600,690,.94,1,'calm',pose='hold',prop='leaf',glow=.8,look=1000,actions=[A('promised',tilt=.08)])])
# ================= B16 the chant: the guru is torn =================
S(326.36,'wide','normal','crane_down',C(1.0,1.08,0,0,-30,0),'descend on the chanting guru',
  'Shukracharya closed his eyes and began to chant.',
  'Shukracharya sits cross-legged in the night yard, eyes closed, chanting; Devayani stands aside clutching the leaf, watching.',
  'shukracharya',ashram(night=True),'ritual',
  [F('shukracharya',640,680,.9,1,'calm',pose='sitpray',talk=.4,mood={'blink':1}),F('devayani',1000,690,.8,-1,'doubt',pose='hold',prop='leaf',glow=.6,look='shukracharya')],
  [X('ember_fire',330,612,110,'the yard fire',behind=True)],tr='fade')
S(328.95,'medium','normal','handheld',C(1.12,1.18,0,0,30,30),'the camera shakes with his body',
  'Shukracharya\'s belly began to shake.',
  'The seated guru\'s body shakes violently; dark-red paper blood bursts at his belly.',
  'shukracharya',ashram(night=True),'agony',
  [F('shukracharya',640,680,.94,1,'pain',pose='sitpray',talk=.5,mood={'blink':1})],
  [X('blood_splash',650,590,120,'his belly begins to tear',word='belly',d=.3,n=8,spread=.6)],shake=5)
S(330.23,'medium','normal','push_in',C(1.1,1.2,0,0,30,30),'push in as the tearing spreads',
  'Then his chest, his face, his arms.',
  'Blood splashes burst one after another at the guru\'s chest, face and arms as his body shakes and his face twists in pain.',
  'shukracharya',ashram(night=True),'agony',
  [F('shukracharya',640,680,.94,1,'pain',pose='sitpray',talk=.5,mood={'blink':1,'mouth':.5})],
  [X('blood_splash',650,520,140,'his chest tears',word='chest',d=.3,n=9),X('blood_splash',640,440,90,'his face tears',word='face',d=.3,n=7),X('blood_splash',520,560,90,'his arms tear',word='arms',d=.3,n=6)],shake=4)
S(333.31,'close','tele','dutch',C(1.14,1.2,0,0,0,0,0,.04),'tilted frame on the horror at his eye',
  'A finger came out of his eye.',
  'Close on Shukracharya\'s face twisted in pain, a dark-red burst of paper blood spraying from one eye.',
  'shukracharya',ashram(night=True),'horror',
  [F('shukracharya',640,340,1.15,1,'pain',head=True,talk=.5,mood={'blink':.8})],
  [X('blood_splash',600,300,110,'a finger tears out of his eye',word='finger',d=.3,n=8,spread=.6)],shake=3)
S(335.18,'medium','normal','pull_out',C(1.16,1.06,0,0,30,20),'pull back as the body opens',
  'A foot came out of his belly.',
  'The seated guru\'s body starts to split open like a torn cocoon, blood spraying from his belly as a figure pushes out.',
  'shukracharya',ashram(night=True),'horror',
  [F('shukracharya',640,690,.92,1,'pain',pose='sitpray',talk=.4,rised=3.0,engine_cues={'risec':'foot'})],
  [X('blood_splash',640,600,180,'the belly tears open',word='foot',d=.3,n=10)],shake=3)
# ================= B17 Kacha rises out of the guru =================
GURU_DEAD=lambda x=980,y=600,s=.66,**k:F('shukracharya',x,y,s,1,'pain',pose='sleep',mat=False,mood={'blink':1},look=640,actions=[],**k)
S(337.05,'wide','normal','tilt_up',C(1.06,1.14,0,0,40,0),'tilt up with Kacha as he rises out of the body',
  'Kacha came out of Shukracharya\'s body, covered in blood.',
  'The guru\'s torn body lies on the ground in a pool of dark-red paper blood and Kacha rises straight up out of his chest, bloodied, arms opening; Devayani stares in horror.',
  'kacha',ashram(night=True),'gruesome rebirth',
  [F('shukracharya',600,560,.82,1,'pain',pose='sleep',mat=False,rised=1.6,kmood={'blink':.3,'smirk':.3},look=900,engine_cues={'risec':'came'}),
   F('devayani',1060,690,.82,-1,'horror',look='shukracharya',actions=[A('blood',mood={'wide':1})])],
  [X('blood_splash',560,600,320,'the guru\'s blood around his torn body',word='came',d=.4,n=12,spread=1.1),X('ember_fire',220,612,110,'the yard fire',behind=True)])
S(340.59,'two_shot','normal','dolly_left',C(1.08,1.14,40,0,0,0),'slide around the embrace',
  'Devayani held Kacha, laughing and crying.',
  'Devayani throws her arms around blood-smeared Kacha, laughing and crying at once; behind them her father\'s torn body lies in a pool of blood.',
  'devayani',ashram(night=True),'relief and horror',
  [GURU_DEAD(1000,600,.6),F('kacha',640,690,.9,-1,'calm',look='devayani',mood={'blink':.4}),
   F('devayani',560,686,.88,1,'laughcry',pose='hug',look='kacha',actions=[A('laughing',mood={'laugh':1,'tears':1})])],
  [X('blood_splash',1000,600,240,'the blood of the torn guru',n=10),X('blood_splash',680,480,70,'blood on Kacha\'s chest',n=5,spread=.3)])
S(343.73,'close','tele','push_in',C(1.08,1.18),'push in on the eyes she cannot see',
  'She did not see his eyes.',
  'Devayani rests her head on Kacha\'s shoulder with closed eyes, weeping and smiling; above her, Kacha\'s eyes are cold and distant.',
  'kacha',ashram(night=True,near=False),'coldness',
  [F('kacha',720,320,1.1,-1,'coldsmile',head=True,look=1100,mood={'blink':.45}),F('devayani',470,390,1.0,1,'laughcry',head=True,look='kacha',mood={'blink':1})],
  [X('blood_splash',760,470,60,'his bloody shoulder',n=4,spread=.3)])
S(345.41,'extreme_close','tele','dutch',C(1.3,1.36,0,0,0,0,0,.03),'tilted extreme close-up on the changed smile',
  'He smiled, but not the way he used to.',
  'Extreme close-up of Kacha\'s face smeared with blood: a cold, crooked smile with hard eyes.',
  'kacha',ashram(night=True),'menace',
  [F('kacha',640,350,1.4,1,'calm',head=True,actions=[A('smiled',emo='coldsmile',mood={'smirk':1},d=.5)])],
  [X('blood_splash',560,330,80,'blood on his face',n=5,spread=.3)])
# ================= B18 the mantra falls =================
S(348.10,'two_shot','normal','pan_right',C(1.06,1.1,-40,40,0,0),'pan from her to the body she will revive',
  'Devayani said she must bring her father back now.',
  'Devayani holds up the glowing palm leaf and turns to her father\'s body lying in blood; Kacha stands behind her.',
  'devayani',ashram(night=True),'urgency',
  [F('kacha',300,690,.84,1,'calm',look='devayani'),F('devayani',600,690,.88,1,'joy',pose='hold',prop='leaf',glow=.8,talk=.6,look=1000),GURU_DEAD(1000,600,.6)],
  [X('blood_splash',1000,600,220,'the guru\'s blood',n=9)])
S(350.93,'two_shot','normal','push_in',C(1.06,1.16,0,0,0,0),'push in on his reaching hand',
  'Kacha asked to do it himself.',
  'Kacha holds out his open hand for the leaf with a gentle face; Devayani hesitates, doubtful.',
  'kacha',ashram(night=True),'temptation',
  [F('kacha',480,690,.88,1,'love',pose='open',talk=.6,look='devayani'),F('devayani',820,690,.88,-1,'doubt',pose='hold',prop='leaf',glow=.8,look='kacha')])
S(353.07,'medium','normal','dolly_left',C(1.1,1.16,30,-20,0,0),'slide as she turns away with the leaf',
  'She hid the mantra behind her.',
  'Devayani turns away from Kacha, pulling the glowing leaf out of his reach; Kacha\'s eyes follow it.',
  'devayani',ashram(night=True),'mistrust',
  [F('kacha',460,690,.88,1,'scheme',look='devayani'),F('devayani',780,690,.88,-1,'doubt',pose='hold',prop='leaf',glow=.8,look='kacha',turn_on='hid',turn_d=.4)])
S(355.01,'close','tele','push_in',C(1.1,1.2),'push in on her firm words',
  'She said it was her father\'s secret, and only she could use it.',
  'Devayani\'s face is firm and guarded as she speaks.',
  'devayani',ashram(night=True),'guarded',
  [F('devayani',640,340,1.15,-1,'calm',head=True,talk=.6,look=300,mood={'anger':.35})])
S(358.67,'close','tele','crane_down',C(1.1,1.18,0,0,-20,0),'settle on his soft, false face',
  'Kacha asked if he was anyone else.',
  'Kacha\'s face softens into a hurt, loving look as he asks.',
  'kacha',ashram(night=True),'manipulation',
  [F('kacha',640,340,1.15,1,'love',head=True,talk=.6,look=1000,mood={'sad':.3})])
S(361.14,'two_shot','tele','push_in',C(1.04,1.12),'push in on two faces drawing close',
  'He said he was her, and she was him.',
  'Kacha and Devayani face each other close up; his voice is tender and her guarded face melts into love.',
  'devayani',ashram(night=True,near=False),'seduction',
  [F('kacha',420,350,1.05,1,'love',head=True,talk=.6,look='devayani'),F('devayani',860,350,1.05,-1,'doubt',head=True,look='kacha',actions=[A('her',emo='love',d=.8)])])
S(364.17,'wide','normal','pan_right',C(1.04,1.08,-40,40,0,0),'pan toward the body he offers to revive',
  'The guru had given him back his life, and now he wanted to give the guru\'s life back.',
  'Kacha gestures with an open hand toward the guru\'s body lying in blood; Devayani looks at her father with hope.',
  'kacha',ashram(night=True),'persuasion',
  [F('kacha',380,690,.86,1,'love',talk=.6,look=1000,actions=[A('now',pose='open',d=.6)]),F('devayani',620,690,.84,1,'doubt',pose='hold',prop='leaf',glow=.8,look=1000),GURU_DEAD(1000,600,.6)],
  [X('blood_splash',1000,600,220,'the guru\'s blood',n=9)])
S(369.22,'extreme_close','tele','static',C(1.12,1.12),'hold the locked gaze',
  'Kacha\'s eyes held Devayani\'s gaze.',
  'Kacha\'s and Devayani\'s eyes lock in a very close double close-up, his steady, hers melting.',
  'kacha',ashram(night=True,near=False),'spell',
  [F('kacha',420,360,1.3,1,'love',head=True,look='devayani',mood={'blink':.15}),F('devayani',860,360,1.3,-1,'love',head=True,look='kacha',mood={'blink':.45})])
S(370.99,'insert','tele','tilt_down',C(1.1,1.16,0,0,-30,20),'follow the falling leaf down',
  'Her fingers loosened. The mantra fell.',
  'The glowing palm-leaf mantra tumbles down through the dark air out of Devayani\'s loosened hand.',
  'palm leaf',ashram(night=True),'fall',
  [F('devayani',380,360,1.0,1,'love',head=True,look=700,mood={'blink':.55,'ly':.5})],
  [X('palm_leaf',760,230,280,'the mantra falling from her fingers',glow=1,word='loosened',d=.3,vy=90,spin=.8)])
S(373.58,'medium','normal','push_in',C(1.1,1.2,0,0,0,0),'push in on the catch',
  'Kacha caught the falling mantra.',
  'Kacha snatches the glowing leaf out of the air with a sudden cold smile.',
  'kacha',ashram(night=True),'triumph',
  [F('kacha',600,690,.92,1,'scheme',pose='catch',prop='leaf',glow=1,look=700,actions=[A('caught',emo='coldsmile',d=.3)])])
# ================= B19 the reading; the guru understands =================
S(374.82,'wide','normal','dolly_right',C(1.04,1.1,-30,30,0,0),'slide over the body he reads above',
  'Kacha read the mantra over the guru\'s body.',
  'Kacha stands over the guru\'s bloody body and reads aloud from the glowing palm leaf; Devayani watches with hope.',
  'kacha',ashram(night=True),'incantation',
  [F('devayani',300,690,.84,1,'love',look='kacha'),F('kacha',640,690,.88,1,'calm',pose='catch',prop='leaf',glow=1,talk=.6,mood={'ly':.4}),GURU_DEAD(960,600,.62)],
  [X('blood_splash',960,600,220,'the guru\'s blood',n=9),X('light_beam',960,600,200,'the mantra\'s light falls on the body',word='read',alpha=.4,blend='lighter')])
S(376.84,'low_angle','wide','tilt_up',C(1.04,1.12,0,0,30,-10),'low angle on the proud demons',
  'The secret the demons were so proud of.',
  'In the feast hall a horned demon raises his mace proudly while the silhouette army behind him cheers.',
  'asura1',feast(),'pride',
  [F('asura1',640,720,1.0,1,'pride',pose='raise',talk=.4,mood={'smile':.4})],tr='wipe')
S(379.10,'wide','normal','crane_down',C(1.0,1.08,0,0,-40,0),'descend from the peak of Kailash',
  'The mantra was a gift from Shiva.',
  'Before the dark peaks of Kailash Shiva stands with an open hand; golden rays fall around him and his name appears.',
  'shiva',kailash(),'divine origin',
  [F('shiva',640,690,.88,1,'calm',pose='calm',look=640,mood={'blink':.4},actions=[A('gift',tilt=.04)])],
  [X('divine_rays',640,0,900,'the divine gift',alpha=.45,behind=True),NAME('Shiva',640,96,'gift')],tr='iris')
S(380.59,'close','tele','push_in',C(1.1,1.2),'push in on his lips learning the words',
  'Kacha read every word and learned it by heart.',
  'Kacha\'s face lit gold from below by the glowing leaf, lips moving as he memorises the mantra.',
  'kacha',ashram(night=True),'theft',
  [F('kacha',640,320,1.15,1,'scheme',head=True,talk=.6,mood={'ly':.7})],
  [X('palm_leaf',640,510,300,'the mantra he memorises',glow=1,rot=-.05)],tr='iris')
S(383.45,'medium','normal','tilt_up',C(1.06,1.14,0,0,30,0),'tilt up as the old man rises',
  'Shukracharya stood up, alive again.',
  'Shukracharya, bloodstained, rises to his feet from the pool of blood, his face softening as he looks for his daughter.',
  'shukracharya',ashram(night=True),'revival',
  [F('shukracharya',640,700,.92,1,'pain',pose='collapse',look=300,actions=[A('Shukracharya',pose='stand',emo='calm',d=.8)])],
  [X('blood_splash',640,700,260,'the blood he rises from',n=9)])
S(385.01,'two_shot','normal','dolly_left',C(1.06,1.12,20,-30,0,0),'move with his step',
  'He took a step toward his daughter.',
  'Shukracharya steps toward Devayani with a loving face and opening hands; she smiles back with joy.',
  'shukracharya',ashram(night=True),'reunion',
  [F('devayani',380,690,.86,1,'joy',look='shukracharya'),F('shukracharya',860,690,.9,-1,'love',look='devayani',walk={'word':'took','to_x':720,'d':1.0,'speed':.6},actions=[A('step',pose='open')])])
S(386.93,'ots','normal','pan_left',C(1.08,1.14,40,-40,0,0),'pan from the guru to the leaf in Kacha\'s hand',
  'Then he saw the mantra in Kacha\'s hand.',
  'Kacha in the foreground holds up the glowing mantra; behind him Shukracharya\'s face freezes in shock as he sees it.',
  'palm leaf',ashram(night=True),'realisation',
  [F('shukracharya',880,672,.78,-1,'love',look='kacha',actions=[A('saw',emo='shock',d=.4)]),F('kacha',440,700,.96,1,'coldsmile',pose='catch',prop='leaf',glow=1,look=900)])
S(389.60,'close','tele','push_in',C(1.08,1.2),'push in on the smile',
  'He saw Kacha smiling.',
  'Kacha\'s face: a calm, cold smile of victory.',
  'kacha',ashram(night=True),'victory',
  [F('kacha',640,340,1.15,1,'coldsmile',head=True,look=1000,mood={'smirk':1})])
S(391.24,'close','tele','static',C(1.14,1.14),'hold on the face that breaks',
  'He knew. There was no rage on his face, only pain.',
  'Shukracharya\'s face in close-up: no anger at all, only deep pain, tears in his old eyes.',
  'shukracharya',ashram(night=True),'heartbreak',
  [F('shukracharya',640,340,1.15,-1,'shock',head=True,look=300,actions=[A('knew',emo='pain',mood={'tears':.6},d=.8)])])
S(395.33,'medium','normal','crane_down',C(1.04,1.14,0,0,-20,20),'drop down with him as he falls',
  'And he fell to the ground.',
  'Shukracharya topples backwards to the ground, arms flung out; Devayani reaches toward him in shock.',
  'shukracharya',ashram(night=True),'collapse',
  [F('devayani',380,690,.86,1,'shock',look='shukracharya',actions=[A('fell',pose='plead',d=.4)]),
   F('shukracharya',820,690,.9,-1,'pain',look='devayani',bd=.6,engine_cues={'bc':'fell'},bow=.5,actions=[A('fell',pose='fall',d=.5)])])
# ================= B20 he walks away =================
S(396.76,'wide','wide','pan_right',C(1.0,1.04,-40,40,0,0),'pan with him leaving',
  'Kacha began to walk away.',
  'Kacha turns his back and walks away to the right with the glowing leaf; behind him the guru lies on the ground and Devayani kneels by him.',
  'kacha',ashram(night=True),'abandonment',
  [GURU_DEAD(330,600,.6),F('devayani',520,690,.8,-1,'shock',pose='kneel',look='kacha'),
   F('kacha',740,690,.84,1,'calm',prop='leaf',glow=.7,look=1200,walk={'word':'began','to_x':1000,'d':1.4,'speed':.8})])
S(398.55,'medium','normal','dolly_right',C(1.04,1.1,-30,40,0,0),'run alongside her',
  'Devayani ran after him.',
  'Devayani runs after Kacha with her sari flying; Kacha keeps walking away ahead of her.',
  'devayani',ashram(night=True),'pursuit',
  [F('devayani',280,690,.86,1,'fear',pose='run',look='kacha',walk={'word':'Devayani','to_x':620,'d':1.4,'speed':1.6}),F('kacha',980,690,.84,1,'calm',prop='leaf',glow=.6,look=1300)])
S(400.21,'two_shot','normal','push_in',C(1.04,1.14,0,40,0,0),'push in on her hopeful plea',
  'She said she had told her father about them, and asked Kacha to speak to the guru so they could marry.',
  'Devayani pleads with a hopeful, loving face, hands reaching; Kacha stands with his back half turned, not looking at her.',
  'devayani',ashram(night=True),'hope',
  [F('devayani',520,690,.88,1,'love',pose='plead',talk=.6,look='kacha'),F('kacha',860,690,.88,1,'calm',look=1200,mood={'blink':.4})])
S(405.10,'close','tele','pull_out',C(1.18,1.08),'pull back from his cold profile',
  'Kacha asked if she still did not understand.',
  'Kacha\'s face, turned away from her, speaks coldly with a hard look.',
  'kacha',ashram(night=True),'coldness',
  [F('kacha',640,340,1.15,1,'coldsmile',head=True,talk=.6,look=1100)])
S(407.85,'ots','normal','dolly_left',C(1.08,1.14,30,-20,0,0),'slide between his turned back and her stare',
  'He did not even look at her.',
  'Kacha in the right foreground looks off to the right; behind him on the left Devayani stares at him, hurt.',
  'devayani',ashram(night=True),'rejection',
  [F('devayani',400,676,.76,1,'pain',look='kacha'),F('kacha',860,700,.96,1,'calm',look=1300,mood={'blink':.4})])
S(409.41,'close','tele','push_in',C(1.1,1.22),'push in on her understanding',
  'Then she understood: Mritasanjivani.',
  'Devayani\'s eyes go wide with realisation as the word Mritasanjivani burns above her.',
  'devayani',ashram(night=True),'realisation',
  [F('devayani',640,350,1.15,1,'pain',head=True,actions=[A('understood',emo='shock',d=.4)])],
  [TEXT('Mritasanjivani',640,100,'understood','the word she suddenly understands',56)])
S(412.02,'close','tele','pull_out',C(1.12,1.04),'pull back to reveal the shadow behind him',
  'He told her he had come for what his father had sent him for.',
  'Kacha\'s cold face in close-up on the left while, behind him, the black shadow of his father Brihaspati looms with an ember outline.',
  'kacha',ashram(night=True),'true purpose',
  [F('brihaspati',940,560,.62,-1,'scheme',look='kacha',**SHADOW),F('kacha',480,340,1.1,1,'coldsmile',head=True,talk=.5,look=200)])
# ================= B21 sister =================
S(415.39,'close','tele','push_in',C(1.08,1.2),'push in on the blood on her cheek',
  'She touched her father\'s blood on her cheek and stared at her fingers.',
  'Devayani touches a smear of dark-red blood on her cheek and stares at her stained fingertips in horror.',
  'devayani',ashram(night=True),'horror',
  [F('devayani',640,340,1.15,1,'horror',head=True,mood={'ly':.5},actions=[A('stared',mood={'ly':.9,'wide':.7})])],
  [X('blood_splash',590,390,60,'her father\'s blood on her cheek',n=4,spread=.3,word='blood')])
S(419.35,'medium','normal','dolly_right',C(1.06,1.14,-30,20,0,0),'slide along her accusation',
  'She asked how he could be so cruel.',
  'Devayani points at Kacha with fury and grief, tears on her face.',
  'devayani',ashram(night=True),'accusation',
  [F('devayani',520,690,.92,1,'grief',pose='point',talk=.6,look=1000,actions=[A('cruel',emo='fury',d=.5)])])
S(421.81,'wide','normal','pull_out',C(1.12,1.02),'pull back to include the body between them',
  'He made her betray her father so he could keep his promise to his own father.',
  'Devayani accuses Kacha across her father\'s bloody body lying between them; Kacha stands unmoved.',
  'devayani',ashram(night=True),'betrayal',
  [F('devayani',330,690,.86,1,'fury',pose='point',talk=.6,look='kacha'),GURU_DEAD(640,600,.58),F('kacha',960,690,.86,-1,'calm',look='devayani')],
  [X('blood_splash',640,600,200,'her father\'s blood',n=8)])
S(425.85,'low_angle','wide','tilt_up',C(1.04,1.14,0,0,40,-10),'tilt up to the universe he invokes',
  'Kacha said that if he were cruel, the universe would have stopped him.',
  'Kacha opens his hands to the starry night sky, calm, as if the universe agrees with him.',
  'kacha',ashram(night=True),'self-justification',
  [F('kacha',640,716,.98,1,'calm',pose='open',talk=.6,mood={'ly':-.7},actions=[A('universe',pose='raise',d=.6)])])
S(429.94,'two_shot','normal','dolly_left',C(1.06,1.12,30,-20,0,0),'slide from his shrug to her pain',
  'He had only found a friend, and he had never made any promises.',
  'Kacha shrugs with open hands, cold and calm; Devayani listens with growing pain.',
  'kacha',ashram(night=True),'denial',
  [F('devayani',400,690,.86,1,'pain',look='kacha'),F('kacha',820,690,.88,-1,'calm',pose='open',talk=.6,look='devayani')])
S(433.96,'wide','normal','pan_left',C(1.04,1.08,40,-40,0,0),'pan along his pointing hand to the body',
  'Now that he was born from her father\'s body, he was her father\'s son too.',
  'Kacha points at the guru\'s body lying in blood; Devayani\'s eyes follow his finger to her father.',
  'kacha',ashram(night=True),'twisted logic',
  [GURU_DEAD(380,600,.6),F('devayani',640,690,.84,-1,'pain',look=380),F('kacha',940,690,.88,-1,'calm',pose='point',talk=.6,look=380)],
  [X('blood_splash',380,600,200,'the body he was born from',n=8)])
S(438.65,'close','tele','push_in',C(1.1,1.24),'push in on the word that destroys her',
  'That made her his sister.',
  'Devayani\'s face in close-up, shock collapsing into grief, tears running.',
  'devayani',ashram(night=True),'devastation',
  [F('devayani',640,340,1.15,1,'shock',head=True,actions=[A('sister',emo='grief',d=.4)])])
# ================= B22 the two curses =================
S(440.46,'wide','wide','pull_out',C(1.1,1.0),'pull back to the distance growing between them',
  'She watched Kacha go.',
  'Devayani stands in the left foreground watching small Kacha walk away into the dark on the right.',
  'devayani',ashram(night=True),'loss',
  [F('devayani',330,700,.94,1,'grief',look='kacha'),F('kacha',980,660,.56,1,'calm',prop='leaf',glow=.6,look=1300,walk={'word':'watched','to_x':1120,'d':1.4,'speed':.7})])
S(442.02,'wide','normal','dolly_right',C(1.04,1.1,-30,30,0,0),'slide from her father to the leaving man',
  'Her father lay on the ground, and the man she loved was leaving.',
  'Devayani kneels by her father\'s bloody body on the left while, far on the right, Kacha walks away.',
  'devayani',ashram(night=True),'abandoned',
  [GURU_DEAD(380,600,.62),F('devayani',620,690,.84,-1,'grief',pose='kneel',look=380,actions=[A('leaving',look='kacha',d=.6)]),F('kacha',1050,660,.56,1,'calm',look=1300)],
  [X('blood_splash',380,600,200,'her father\'s blood',n=8)])
S(445.83,'close','tele','push_in',C(1.1,1.22),'push in as grief turns to fury',
  'She was crying. Then she spoke.',
  'Devayani\'s crying face in close-up; on "Then" her eyes harden into fury.',
  'devayani',ashram(night=True),'grief to fury',
  [F('devayani',640,340,1.15,1,'grief',head=True,mood={'tears':1},actions=[A('Then',emo='fury',d=.3)])])
S(448.32,'low_angle','wide','tilt_up',C(1.06,1.16,0,0,30,-10),'low angle on the curse',
  'Devayani cursed Kacha.',
  'Devayani rises and points at Kacha, a red ring of curse-light blazing around her hand.',
  'devayani',ashram(night=True),'curse',
  [F('devayani',600,716,.98,1,'fury',pose='point',talk=.8,look=1000)],
  [X('curse_glow',800,420,260,'Devayani\'s curse',word='She',d=.3)],tr='flash')
S(449.56,'close','tele','dolly_left',C(1.12,1.18,30,-20,0,0),'slide close on her furious words',
  'The secret he had stolen, she said, would never work for him.',
  'Devayani\'s furious face, red-eyed, speaking the curse while the red curse ring burns behind her.',
  'devayani',ashram(night=True),'vengeance',
  [F('devayani',640,340,1.15,1,'fury',head=True,talk=.7,look=1000)],
  [X('curse_glow',640,290,620,'the curse on the stolen secret',behind=True,alpha=.6)])
S(452.86,'medium','normal','push_in',C(1.08,1.16),'push in as he turns back',
  'Kacha turned back to face her.',
  'Kacha, walking away, turns round to face her with a cold look.',
  'kacha',ashram(night=True),'confrontation',
  [F('kacha',640,690,.92,1,'calm',prop='leaf',glow=.6,look=1000,turn_on='Kacha',turn_d=.4,actions=[A('turned',emo='coldsmile',d=.4)])])
S(454.08,'low_angle','wide','tilt_up',C(1.04,1.14,0,0,30,-10),'low angle on his defiance',
  'He said he would teach it to others, and it would work for them.',
  'Kacha raises the glowing mantra leaf high with a cold smile, talking.',
  'kacha',ashram(night=True),'defiance',
  [F('kacha',640,716,.98,-1,'coldsmile',pose='catch',prop='leaf',glow=1,talk=.6,look=300)])
S(457.35,'medium','normal','dolly_right',C(1.06,1.12,-20,30,0,0),'slide along his curse toward her',
  'And he cursed her back.',
  'Kacha points back at Devayani, a violet curse ring flaring around his hand.',
  'kacha',ashram(night=True),'counter-curse',
  [F('kacha',800,690,.92,-1,'fury',pose='point',talk=.7,look=300)],
  [X('curse_glow',640,430,240,'Kacha\'s curse on Devayani',col='violet',word='cursed',d=.3)])
S(459.01,'wide','wide','crane_up',C(1.04,1.12,0,0,20,-30),'rise away from her, leaving her small',
  'She would never find the love she sought.',
  'Devayani sinks to her knees alone in the dark yard, a faint violet curse light around her, crying.',
  'devayani',ashram(night=True),'doomed love',
  [F('devayani',640,690,.84,1,'grief',look=640,mood={'tears':1,'ly':.7},actions=[A('never',pose='collapse',d=.6)])],
  [X('curse_glow',640,520,360,'the curse that falls on her',col='violet',alpha=.5,behind=True)])
# ================= B23 recap and question =================
S(461.26,'medium','normal','pan_right',C(1.04,1.1,-30,40,0,0),'pan with the winner walking off',
  'Kacha got the mantra.',
  'Kacha walks away into the dark holding the glowing mantra leaf, a cold smile on his face.',
  'kacha',ashram(night=True),'cold victory',
  [F('kacha',560,690,.9,1,'coldsmile',prop='leaf',glow=1,look=1300,walk={'word':'Kacha','to_x':800,'d':1.6,'speed':.8})],tr='fade')
S(462.86,'wide','wide','pull_out',C(1.12,1.0),'pull back to leave her alone',
  'Devayani lost her father\'s trust and the man she gave it up for.',
  'Devayani kneels alone beside her father\'s body in the dark yard, head bowed.',
  'devayani',ashram(night=True),'loss',
  [GURU_DEAD(520,600,.62),F('devayani',780,690,.84,-1,'grief',pose='kneel',look=520,mood={'ly':.7})],
  [X('blood_splash',520,600,200,'her father\'s blood',n=8)])
S(466.84,'two_shot','tele','push_in',C(1.04,1.1),'push in on the question between two faces',
  'Was Kacha a hero for the gods, or a thief of a girl\'s heart?',
  'Kacha\'s cold face on the left and Devayani\'s grieving face on the right; the words Hero or thief? appear between them.',
  'kacha',ashram(night=True,near=False),'question',
  [F('kacha',380,370,1.05,1,'coldsmile',head=True,look=640),F('devayani',900,370,1.05,-1,'grief',head=True,look=640,mood={'tears':.8})],
  [TEXT('Hero or thief?',640,100,'hero','the question for the viewer',56)])
S(470.70,'wide','wide','crane_up',C(1.04,1.0,0,0,0,-30),'rise up and away from the story',
  'Tell us in the comments.',
  'The dark ashram from above: Kacha a small figure walking off with the glowing leaf, Devayani kneeling by her father.',
  'ashram',ashram(night=True),'reflection',
  [F('devayani',380,690,.7,1,'grief',pose='kneel',look=1000),F('kacha',960,670,.58,1,'calm',prop='leaf',glow=.8,look=1300)])
#@@SHOTS@@
def build():
    sh=sorted(SHOTS,key=lambda s:s['t']);out=[];cnt={}
    for k,s in enumerate(sh):
        i=idx(s['t']);nt=sh[k+1]['t'] if k+1<len(sh) else TOTAL;j=i
        while j<len(TL) and TL[j]['t']<nt-.005:j+=1
        b=TL[i]['beat'];cnt[b]=cnt.get(b,0)+1
        o={'id':f'b{b:02d}_{cnt[b]}','beat':b,'start':{'t':TL[i]['t'],'word':re.sub(r'[^\w\']','',TL[i]['w'])},'duration':round(nt-s['t'],2),
           'narration':' '.join(x['tok'] for x in TL[i:j])}
        o.update({k2:v for k2,v in s.items() if k2!='t'})
        out.append(o)
    return {'episode':'07','look':'ep07_dark','shots':out}
if __name__=='__main__':
    B=build();json.dump(B,open(R+'/episodes/ep07/briefs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(len(B['shots']),'shots -> episodes/ep07/briefs.json')
