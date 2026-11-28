"""Per-reel specs for reels/auto_briefs.py: lex = word in narration -> cast key (who appears), scenes = (sentence index or keyword in sentence, scene), scale/big/maxc/over optional."""
import sys;sys.path.insert(0,"/home/user/mahagatha-studio/reels")
from briefs_lib import pfx,name
SPEC={
 'reel17':dict(scene='night',lex={'vishnu':'vishnu','shiva':'shiva'},scenes=[(0,'night'),('demons','ember'),('wilderness','brown'),('lingam','indigo'),('thousand lotuses','indigo'),('appeared','kailash')],
   scale={'vishnu':.9,'shiva':.9},
   over={
    3:dict(scene='ember',chars=[dict(who='asura1',x=640,y=690,s=1.3,_face=.40,flip=1,pose='rage',emo='rage',look=700)],
           fx=[pfx('lightning_forks','demons',640,260,560,'lightning behind a huge scary demon',alpha=.9,behind=True),pfx('smoke_plume','demons',640,580,420,'black smoke at the demon feet',alpha=.8),pfx('red_energy_pulse','demons',640,420,420,'a red glow of danger',alpha=.7,behind=True)]),
    4:dict(scene='ember',chars=[dict(who='asura1',x=640,y=640,s=1.25,_face=.36,flip=1,pose='lunge',emo='rage',look=700),
            dict(who='deva_thin',x=478,y=740,s=.6,_face=.56,flip=1,pose='plead',emo='fear',look=700),dict(who='deva_thin2',x=806,y=745,s=.58,_face=.56,flip=-1,pose='plead',emo='fear',look=700)],
           fx=[pfx('demon_crowd','tormented',640,470,700,'dark demon shapes crowding in on the frightened gods',alpha=.85,behind=True),pfx('ember_fire','tormented',640,620,520,'fire burning around the frightened gods',alpha=.9),pfx('red_energy_pulse','tormented',640,420,420,'a red glow of terror',alpha=.6,behind=True)]),
    5:dict(scene='night',chars=[dict(who='vishnu',x=640,y=690,s=.95,_face=.42,flip=1,pose='stand',emo='calm',look=700),
            dict(who='deva_thin',x=478,y=745,s=.58,_face=.58,flip=1,pose='kneel',emo='fear',look=700),dict(who='deva_thin2',x=806,y=748,s=.56,_face=.58,flip=-1,pose='kneel',emo='fear',look=700)],
           fx=[pfx('divine_rays','begged',640,330,520,'Vishnu light falling on the begging gods',alpha=.7,behind=True)]),
    10:dict(scene='indigo',chars=[dict(who='vishnu',x=520,y=690,s=.85,_face=.46,flip=1,pose='namaste',emo='devotion',look=720)],mid=[{"o":"rock","x":780,"y":600,"s":.9,"col":"#2e2838"}],
           fx=[{"k":"lotus","word":"lotus","x":780,"y":560,"sc":.55,"open":1,"meaning":"one paper-cut lotus laid on the lingam"},pfx('divine_rays','lotus',780,520,420,'soft light on the lingam',alpha=.6,behind=True)]),
    11:dict(scene='indigo',chars=[dict(who='vishnu',x=500,y=690,s=.8,_face=.5,flip=1,pose='namaste',emo='joy',look=720)],mid=[{"o":"rock","x":785,"y":610,"s":1.25,"col":"#2e2838"}],
           fx=[{"k":"lotus","word":"thousand","x":740,"y":610,"sc":0.5,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":830,"y":616,"sc":0.5,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":785,"y":600,"sc":0.55,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":700,"y":580,"sc":0.45,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":870,"y":584,"sc":0.45,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":760,"y":560,"sc":0.5,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":820,"y":556,"sc":0.5,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":790,"y":520,"sc":0.55,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":725,"y":530,"sc":0.42,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":855,"y":534,"sc":0.42,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":780,"y":484,"sc":0.5,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":745,"y":470,"sc":0.4,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":820,"y":470,"sc":0.4,"open":1,"meaning":"a pile of lotuses covering the lingam"},{"k":"lotus","word":"thousand","x":785,"y":440,"sc":0.45,"open":1,"meaning":"a pile of lotuses covering the lingam"},pfx('divine_rays','thousand',785,470,520,'soft light on the lotus-covered lingam',alpha=.7,behind=True)]),
    13:dict(scene='indigo',chars=[dict(who='shiva',x=520,y=690,s=.85,_face=.46,flip=1,pose='point',emo='calm',look=720)],mid=[{"o":"rock","x":790,"y":600,"s":.9,"col":"#2e2838"}],
           fx=[{"k":"lotus","word":"lotus","x":560,"y":330,"sc":.4,"open":1,"meaning":"one lotus lifted away by Shiva"},pfx('divine_rays','lotus',640,330,520,'a hidden light of Shiva',alpha=.6,behind=True)]),
    14:dict(scene='indigo',chars=[dict(who='vishnu',x=520,y=690,s=.85,_face=.46,flip=1,pose='stand',emo='doubt',look=720)],mid=[{"o":"rock","x":780,"y":600,"s":.9,"col":"#2e2838"}],
           fx=[{"k":"lotus","word":"flowers,","x":740,"y":560,"sc":.45,"open":1,"meaning":"counted lotus one"},{"k":"lotus","word":"flowers,","x":830,"y":566,"sc":.45,"open":1,"meaning":"counted lotus two"}]),
    15:dict(scene='indigo',chars=[dict(who='vishnu',x=520,y=690,s=.85,_face=.46,flip=1,pose='stand',emo='fear',look=720)],mid=[{"o":"rock","x":780,"y":600,"s":.9,"col":"#2e2838"}],fx=[pfx('mist_wisps','searched',640,560,640,'dark mist while he searches',alpha=.7,behind=True)]),
   }),

 'reel08':dict(scene='night',lex={'vishnu':'vishnu','gods':'deva_thin','god':'hayagriva','brahma':'brahma','lakshmi':'lakshmi','hayagriv':'hayagriva','demon':'asura1','termites':'deva_thin','termite':'deva_thin'},scenes=[(0,'night'),('fought','ember'),('home','indigo'),('snapped','ember'),('lakshmi','brown'),('horse','indigo'),('neighed','night')]),
 'reel16':dict(scene='indigo',lex={'bala':'bala','demon':'bala','indra':'indra','gods':'deva_thin','god':'deva_thin','heaven':'indra'},scenes=[(0,'indigo'),('yajna','ember'),('flames','ember'),('jewels','night'),('diamonds','night')]),
 'reel18':dict(scene='ember',lex={'parashurama':'parashurama','parashuram':'parashurama','ravana':'ravana10','rama':'rama','brahma':'brahma','kashyapa':'kashyapa','king':'asura2','vishnu':'vishnu','mahendra':'parashurama'},scenes=[(0,'ember'),('Mahendra'.lower(),'brown'),('bow','night'),('arrow','ember')]),
 'reel19':dict(scene='night',lex={'shiva':'shiva','yama':'yama','markandeya':'markandeya','boy':'markandeya','mrikandu':'rishi2','father':'rishi2','sage':'rishi2','gods':'deva_thin','son':'markandeya'},scenes=[(0,'night'),('sixteenth','ember'),('rope','ember'),('killed','ember'),('begged','indigo'),('forever','indigo')]),
 'reel20':dict(scene='night',lex={'ashwatthama':'ashwatthama','krishna':'krishna','stranger':'ashwatthama','shiva':'shiva','people':'villager','travelers':'villager','locals':'villager','temple':'shiva'},scenes=[(0,'night'),('narmada','teal'),('wound','ember'),('krishna','indigo'),('baby','ember')]),
 'reel21':dict(scene='ember',scale={'hanuman':1.08,'kumbhakarna':1.15},lex={'hanuman':'hanuman','kumbhakarna':'kumbhakarna','giant':'kumbhakarna','sugriva':'sugriva','rama':'rama'},scenes=[(0,'ember'),('rama','indigo')]),
 'reel22':dict(scene='indigo',lex={'vishnu':'vishnu','kalki':'kalki','people':'villager','brahmin':'rishi1','families':'villager','relatives':'villager','shambhala':'kalki','vishnuyasha':'rishi1'},scenes=[(0,'indigo'),('kali','ember'),('lie','ember'),('crosses','night'),('crystal','indigo'),('name','brown')]),
 'reel23':dict(scene='ember',scale={'hanuman':1.08},lex={'hanuman':'hanuman','ravana':'ravana10','demons':'asura1','enemies':'asura1','sons':'asura2'},scenes=[(0,'ember'),('ravana','brown'),('roar','ember')]),
 'reel24':dict(scene='night',lex={'shiva':'shiva','arjuna':'arjuna','krishna':'krishna','ashwatthama':'ashwatthama','vishnu':'vishnu','brahmastra':'brahma'},scenes=[(0,'night'),('pashupatastra','ember'),('sudarshana','indigo'),('trident','night')]),
 'reel25':dict(scene='indigo',lex={'sheshnag':'naga','vishnu':'vishnu','brahma':'brahma','ananta':'naga','tortoise':'vishnu','serpents':'naga'},scenes=[(0,'night'),('lotus','indigo'),('ocean','teal'),('heavy','ember'),('mustard','night')]),
 'reel26':dict(scene='ember',lex={'ravana':'ravana10','indra':'indra','meghanada':'meghanada','son':'meghanada','brahma':'brahma','indrajit':'meghanada'},scenes=[(0,'ember'),('invisible','night'),('lanka','brown'),('brahma','indigo')]),
 'reel27':dict(scene='night',lex={'hanuman':'hanuman','parashuram':'parashurama','parashurama':'parashurama','ashwatthama':'ashwatthama','mahabali':'mahabali','vyasa':'rishi3','vibhishana':'vibhishana','kripa':'rishi4','rama':'rama','shiva':'shiva','drona':'rishi2','ravana':'ravana'},scenes=[(0,'night'),('curse','ember'),('mahendra','brown')]),
 'reel28':dict(scene='ember',lex={'ravana':'ravana10','sita':'sita','hanuman':'hanuman','brahma':'brahma','apsara':'kanya','punjikasthala':'kanya','women':'kanya'},scenes=[(0,'ember'),('palace','brown'),('cursed','night'),('carried','ember')]),
}

BOW=lambda w,cut,y=690,x=640,wd=440:pfx('bowstring',w,x,y,wd,'a drawn bow and its string: it is being chewed thinner by termites' if cut<1 else 'the bowstring snapped and whipping loose',alpha=1,snapk=cut)
TER=lambda w,n,al,y=690:pfx('termite_swarm',w,640,y,440,'little golden termites, the gods in disguise, swarming the bowstring',alpha=1,cnt=n,gath=al)
V8=lambda pose,y=600,emo='calm',s=.82:dict(who='vishnu',x=640,y=y,s=s,_face=.40,flip=1,pose=pose,emo=emo,look=700)
SPEC['reel08']['over']={
 0:dict(scene='night',chars=[V8('sleep',560)],fx=[BOW('gods',.3),TER('gods',10,.4)]),
 1:dict(scene='night',chars=[dict(who='deva_thin',x=478,y=720,s=.7,_face=.5,flip=1,pose='stand',emo='scheme',look=700),dict(who='deva_thin2',x=806,y=722,s=.68,_face=.5,flip=-1,pose='stand',emo='scheme',look=700)],fx=[pfx('mist_wisps','purpose',640,560,640,'dark mist of a secret plan',alpha=.8,behind=True)]),
 2:dict(scene='night',chars=[V8('sleep',520,s=.7)],fx=[BOW('termite.',.2,y=660),TER('termite.',22,.2,y=620)]),
 8:dict(scene='night',chars=[V8('sleep',560)],fx=[BOW('bow.',0)]),
 13:dict(scene='indigo',chars=[dict(who='brahma',x=520,y=690,s=.85,_face=.45,flip=1,pose='point',emo='scheme',look=700)],fx=[BOW('bowstring',0,x=790,y=640,wd=300),pfx('red_energy_pulse','sound',640,420,420,'the sound that would shake the sky',alpha=.6,behind=True)]),
 14:dict(scene='night',chars=[V8('sleep',520,s=.76)],fx=[BOW('termites',.35,y=660),TER('termites',16,.95,y=660)]),
 15:dict(scene='night',chars=[V8('sleep',520,s=.76)],fx=[BOW('thinner',.8,y=660),TER('thinner',26,.98,y=660)]),
 16:dict(scene='ember',chars=[V8('fall',640,'shock',.8)],fx=[BOW('snapped,',1.0,y=700),pfx('blood_splash','head.',640,400,200,'blood where the string cut',alpha=.9)]),
 17:dict(scene='ember',chars=[dict(who='vishnu',x=640,y=700,s=.9,_face=.55,flip=1,pose='sleep',emo='calm',look=700)],fx=[pfx('blood_splash','closed.',640,640,220,'blood on the floor',alpha=.8)]),
 18:dict(scene='ember',chars=[dict(who='deva_thin',x=478,y=720,s=.7,_face=.5,flip=1,pose='plead',emo='fear',look=700),dict(who='deva_thin2',x=806,y=722,s=.68,_face=.5,flip=-1,pose='plead',emo='fear',look=700)],fx=[pfx('smoke_plume','froze.',640,580,420,'dark smoke in the frozen silence',alpha=.8)]),
 21:dict(scene='brown',fx=[pfx('blood_splash','marks',640,744,200,'red footprints on the floor',alpha=.9)]),
}

HF=lambda w,n=9,y=560,wd=720,a=1:pfx('hood_fan',w,640,y,wd,'Sheshnag, huge, with a fan of cobra hoods',alpha=a,cnt=n)
GL=lambda w,x,y,wd,col=None:pfx('earth_globe',w,x,y,wd,'a world drawn as a small globe',alpha=1)
def WORLDS(w,y0=250,step=64,x=640):return [pfx('earth_globe',w,x+(-110 if k%2 else 110),y0+k*step//2,34+((k*7)%3)*6,'one of the fourteen worlds stacked one below another',alpha=.95) for k in range(14)]
SPEC['reel25']['over']={
 0:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,170,90)]),
 1:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,188,18)]),
 2:dict(scene='night',chars=[],fx=[HF(None,9,600,760,.55),pfx('mist_wisps','where',640,520,700,'dark mist hiding Sheshnag',alpha=.9)]),
 4:dict(scene='sea',chars=[dict(who='vishnu_rest',x=640,y=680,s=.95,_face=.5,flip=1,pose='lie',emo='calm',look=700)],fx=[pfx('wave_ocean','sleeping',640,660,700,'the endless ocean Vishnu sleeps on',alpha=.9)]),
 5:dict(scene='sea',chars=[dict(who='vishnu_rest',x=640,y=720,s=.8,_face=.55,flip=1,pose='lie',emo='calm',look=700),dict(who='brahma',x=640,y=440,s=.62,_face=.4,flip=1,pose='stand',emo='calm',look=700)],fx=[pfx('divine_rays','lotus',640,420,520,'golden light where Brahma appears',alpha=.7,behind=True)]),
 6:dict(scene='night',chars=[dict(who='brahma',x=640,y=470,s=.62,_face=.38,flip=1,pose='stand',emo='calm',look=700)],fx=WORLDS('lotus')),
 7:dict(scene='night',chars=[dict(who='brahma',x=640,y=470,s=.62,_face=.38,flip=1,pose='stand',emo='calm',look=700),dict(who='naga',x=640,y=720,s=.6,_face=.62,flip=1,pose='stand',emo='calm',look=700)],fx=WORLDS('top')),
 8:dict(scene='ember',chars=[],fx=WORLDS('But')+[pfx('ground_crack','heavy',640,660,520,'the worlds are too heavy and the ground cracks',alpha=.8)]),
 9:dict(scene='ember',chars=[],fx=WORLDS('stem',260)+[pfx('lightning_forks','stem',640,260,560,'danger as everything starts to fall',alpha=.7,behind=True)]),
 10:dict(scene='night',chars=[],fx=[HF(None,9,560,780),pfx('divine_rays','Then',640,300,560,'Sheshnag rising far below the lowest world',alpha=.7,behind=True)]),
 11:dict(scene='night',chars=[],fx=[HF(None,9,620,760)]+[pfx('earth_globe','lifted',640+(-40 if k%2 else 40),150-k*0+((k*17)%40),30,'worlds carried on the centre hood',alpha=.95) for k in range(6)]),
 12:dict(scene='sea',chars=[dict(who='vishnu',x=640,y=720,s=.62,_face=.62,flip=1,pose='stand',emo='calm',look=700)],fx=[HF(None,9,420,640)]),
 13:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,185,16)]),
 14:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,185,10)]),
 15:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,185,18)]),
 16:dict(scene='night',chars=[],fx=[HF(None,9,560,760),GL(None,640,185,10)]),
 17:dict(scene='night',chars=[],fx=[HF(None,9,580,760,.9),pfx('mist_wisps','That',640,540,700,'mist hiding Sheshnag',alpha=.9)]),
}
SPEC['reel23']['over']={
 0:dict(scene='ember',chars=[dict(who='hanuman',x=640,y=690,s=1.08,_face=.40,flip=1,pose='stand',emo='pride',look=700,prop='gada')]),
 1:dict(scene='ember',chars=[dict(who='hanuman',x=640,y=690,s=1.08,_face=.40,flip=1,pose='stand',emo='calm',look=700,prop='none')],fx=[pfx('smoke_plume','but',640,560,360,'the mace vanishes in smoke',alpha=.9)]),
}

# ---- reel17: proper lingam + lotus pile (dedicated props), Vishnu/Shiva beside it (crop centred between them)
LG=lambda:pfx('lingam',None,748,585,200,'a dark stone Shiva lingam on a round base',alpha=1,glow=.7)
LP=lambda n,x=748,y=520,w=215:pfx('lotus_pile',None,x,y,w,'a pile of pink paper-cut lotuses with gold centres',alpha=1,cnt=n)
V17=lambda who,pose,emo:dict(who=who,x=584,y=690,s=.7,_face=.5,flip=1,pose=pose,emo=emo,look=720)
VX={"x":650}
SPEC['reel17']['over'].update({
 8:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','open','devotion')],fx=[LG()]),
 9:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','namaste','devotion')],fx=[LG(),pfx('divine_rays',None,748,470,420,'light on the lingam as Vishnu chants',alpha=.6,behind=True)]),
 10:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','namaste','devotion')],fx=[LG(),LP(1,748,462,115)]),
 11:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','namaste','joy')],fx=[LG(),LP(14,748,520,215)]),
 12:dict(scene='indigo',vertical=VX,chars=[V17('shiva','stand','calm')],fx=[LG(),LP(14,748,520,215)]),
 13:dict(scene='indigo',vertical=VX,chars=[V17('shiva','point','scheme')],fx=[LG(),LP(13,748,520,215),LP(1,640,300,110)]),
 14:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','stand','doubt')],fx=[LG(),LP(13,748,520,215)]),
 15:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','stand','fear')],fx=[LG(),LP(13,748,520,215),pfx('mist_wisps',None,640,540,640,'dark mist while he searches',alpha=.6,behind=True)]),
 16:dict(scene='indigo',vertical=VX,chars=[V17('vishnu','stand','fear')],fx=[LG(),LP(13,748,520,215)]),
})

GM=lambda kind,n=1,w=300,x=640,y=520,al=1:pfx('gems',None,x,y,w,'paper-cut '+kind+' gemstone(s) from the story',alpha=al,kind=kind,cnt=n)
SPEC['reel16'].setdefault('over',{}).update({
 19:dict(scene='ember',chars=[],fx=[GM('mix',24,620,640,340),pfx('ground_crack',None,640,640,520,'the body breaking on the ground',alpha=.7)]),
 20:dict(scene='night',chars=[],fx=[GM('mix',30,600,640,380),pfx('divine_rays',None,640,330,520,'bright light on the new jewels',alpha=.8,behind=True)]),
 21:dict(scene='night',chars=[],fx=[GM('diamond',1,300,640,340),pfx('divine_rays',None,640,330,520,'white light of a diamond',alpha=.7,behind=True)]),
 22:dict(scene='ember',chars=[],fx=[GM('ruby',1,300,640,340),pfx('red_energy_pulse',None,640,420,420,'red glow of a ruby',alpha=.7,behind=True)]),
 23:dict(scene='night',chars=[],fx=[GM('sapphire',1,300,640,340),pfx('divine_rays',None,640,330,520,'blue glow of a sapphire',alpha=.5,behind=True)]),
 24:dict(scene='night',chars=[],fx=[GM('pearl',1,280,640,340),pfx('divine_rays',None,640,330,520,'soft white glow of a pearl',alpha=.6,behind=True)]),
 25:dict(scene='night',chars=[],fx=[GM('cat_eye',1,320,640,340),pfx('divine_rays',None,640,330,520,'golden glow of a cats eye',alpha=.6,behind=True)]),
 26:dict(scene='night',chars=[],fx=[GM('mix',9,420,640,340)+{}] if False else [GM('diamond',1,100,545,290),GM('ruby',1,100,645,290),GM('sapphire',1,100,745,290),GM('pearl',1,100,545,400),GM('cat_eye',1,105,645,400),GM('emerald',1,100,745,400),GM('topaz',1,100,545,510),GM('coral',1,100,645,510),GM('garnet',1,100,745,510)]),
 29:dict(scene='night',chars=[],fx=[GM('mix',16,520,640,380)]),
})

# ---- reel20 (Ashwatthama): the people of the story around him
VL=lambda who,x,pose,emo='calm',flip=1,s=.58:dict(who=who,x=x,y=730,s=s,_face=.64,flip=flip,pose=pose,emo=emo,look=700)
LGT=lambda:pfx('lingam',None,640,610,200,'a dark stone Shivling at a temple',alpha=1,glow=.5)
SPEC['reel20'].setdefault('over',{}).update({
 2:dict(scene='brown',chars=[],fx=[LGT(),pfx('wild_flowers',None,640,540,180,'fresh flowers lying on the Shivling',alpha=1),pfx('mist_wisps',None,640,600,640,'early morning mist in the empty temple',alpha=.7,behind=True)]),
 3:dict(scene='brown',chars=[],fx=[LGT(),pfx('wild_flowers',None,640,540,180,'fresh flowers lying on the Shivling',alpha=1),pfx('divine_rays',None,640,330,520,'first light of morning on the temple',alpha=.7,behind=True)]),
 4:dict(scene='brown',chars=[VL('villager',500,'point','surprise',1),VL('villager_w',780,'point','surprise',-1)],fx=[LGT(),pfx('wild_flowers',None,640,540,180,'fresh flowers lying on the Shivling',alpha=1)]),
 6:dict(scene='brown',chars=[dict(who='ashwatthama',x=640,y=700,s=.8,_face=.46,flip=1,pose='sitpray',emo='devotion',look=700),VL('villager',500,'namaste','devotion',1),VL('villager_w',780,'namaste','devotion',-1)],fx=[pfx('divine_rays',None,640,330,520,'light on the praying warrior',alpha=.6,behind=True)]),
 8:dict(scene='teal',chars=[dict(who='ashwatthama',x=640,y=700,s=1.05,_face=.40,flip=1,pose='stand',emo='pain',look=700),VL('villager',500,'stand','fear',1,.5),VL('villager_w',780,'stand','fear',-1,.5)],fx=[pfx('mist_wisps',None,640,600,640,'river mist at the Narmada',alpha=.8,behind=True)]),
 9:dict(scene='teal',chars=[dict(who='ashwatthama',x=640,y=700,s=1.05,_face=.40,flip=1,pose='stand',emo='pain',look=700),VL('villager',500,'stand','surprise',1,.5),VL('villager_w',780,'stand','surprise',-1,.5)],fx=[pfx('blood_splash',None,640,318,70,'a wound on the forehead that never heals',alpha=.9)]),
 10:dict(scene='teal',chars=[dict(who='ashwatthama',x=640,y=700,s=1.05,_face=.40,flip=1,pose='plead',emo='pain',look=700),VL('villager',500,'stand','calm',1,.5),VL('villager_w',780,'namaste','devotion',-1,.5)]),
})

# ---- war around the heroes: small vanara and rakshasa fighters, fires and smoke in the background
SPEC['reel21']['war']=[(458,'sugriva','lunge'),(498,'sugriva','throw'),(538,'sugriva','lunge'),(742,'asura2','rage'),(782,'asura3','lunge'),(822,'asura2','rage')]
SPEC['reel23']['war']=[(458,'asura1','fall'),(498,'asura2','lunge'),(538,'asura3','fall'),(742,'asura3','rage'),(782,'asura1','lunge'),(822,'asura2','fall')]
SPEC['reel26']['war']=[(458,'deva_thin','lunge'),(498,'deva_thin2','lunge'),(538,'deva_thin','throw'),(742,'asura2','rage'),(782,'asura3','rage'),(822,'asura1','lunge')]

# ================= reel24: the three weapons, shown alone (no characters) =================
AS=lambda kind,x=640,y=430,w=230:pfx('astra',None,x,y,w,('the golden Brahmastra arrow of flame' if kind=='brahma' else 'the white-blue Pashupatastra arrow of fire'),alpha=1,kind=kind)
TRI=lambda x=640,y=430,w=270:pfx('trishul',None,x,y,w,"Shiva's golden trident with silver prongs, damaru and red cloth",alpha=1)
CHK=lambda x=640,y=420,w=380:pfx('sudarshan_chakra',None,x,y,w,"Vishnu's spinning Sudarshana Chakra",alpha=1)
NM=lambda s,y=150:name(None,s,640,y,32)
SPEC['reel24']['over']={
 0:dict(scene='night',bg='cosmos',chars=[],fx=[AS('brahma'),NM('Brahmastra')]),
 1:dict(scene='ember',bg='cosmos',chars=[],fx=[AS('brahma'),pfx('red_energy_pulse',None,640,430,520,'its power that stops armies',alpha=.6,behind=True)]),
 2:dict(scene='indigo',bg='cosmos',chars=[],fx=[AS('pashupata'),NM('Pashupatastra')]),
 3:dict(scene='indigo',bg='cosmos',chars=[],fx=[AS('pashupata')]),
 4:dict(scene='ember',bg='storm',chars=[],fx=[AS('pashupata'),pfx('ember_fire',None,640,690,420,'the whole universe burning',alpha=.8),pfx('lightning_forks',None,640,260,560,'danger of burning the universe',alpha=.7,behind=True)]),
 5:dict(scene='night',bg='cosmos',chars=[],fx=[AS('pashupata'),pfx('magic_circle',None,640,430,500,'rings of power around the astra',alpha=.7,behind=True)]),
 6:dict(scene='night',bg='cosmos',chars=[],fx=[AS('pashupata',640,430,200),pfx('magic_circle',None,640,430,560,'it is sent by a word, a look, a thought',alpha=.8,behind=True),pfx('divine_rays',None,640,330,560,'light of a thought',alpha=.6,behind=True)]),
 7:dict(scene='indigo',bg='cosmos',chars=[],fx=[AS('pashupata',640,380,260),AS('brahma',640,640,110)]),
 8:dict(scene='brown',bg='vaikuntha',chars=[],fx=[CHK(),NM("Sudarshana Chakra")]),
 9:dict(scene='brown',bg='vaikuntha',chars=[],fx=[CHK(640,300,300),AS('brahma',640,610,150)]),
 10:dict(scene='brown',bg='vaikuntha',chars=[],fx=[CHK(),pfx('divine_rays',None,640,330,560,'Krishna lets him try',alpha=.6,behind=True)]),
 11:dict(scene='ember',bg='storm',chars=[],fx=[CHK(640,450,380),pfx('ground_crack',None,640,670,560,'the chakra too heavy to lift',alpha=.8),pfx('lightning_forks',None,640,260,560,'its mighty power',alpha=.6,behind=True)]),
 12:dict(scene='night',bg='kailash',chars=[],fx=[TRI(),NM("Shiva's Trident")]),
 13:dict(scene='night',bg='kailash',chars=[],fx=[TRI(640,400,250),AS('pashupata',640,660,110)]),
 14:dict(scene='ember',bg='storm',chars=[],fx=[TRI(),pfx('ground_crack',None,640,680,600,'the earth splitting under the trident',alpha=.9),pfx('lightning_forks',None,640,260,560,'the power to destroy the universe',alpha=.8,behind=True)]),
 15:dict(scene='indigo',bg='cosmos',chars=[],fx=[AS('brahma'),pfx('red_energy_pulse',None,640,430,520,'its power that stops armies',alpha=.5,behind=True)]),
 16:dict(scene='night',bg='cosmos',chars=[],fx=[AS('pashupata',640,190,120),CHK(640,370,230),TRI(640,590,170)]),
 17:dict(scene='night',bg='cosmos',chars=[],fx=[AS('pashupata',640,190,120),CHK(640,370,230),TRI(640,590,170),pfx('mist_wisps',None,640,560,640,'a quiet question over the three weapons',alpha=.5,behind=True)]),
}
# ================= reel25: Sheshnag, drawn properly, with the Earth on his central hood =================
SN=lambda x=640,y=520,w=430,**k:pfx('sheshnag',None,x,y,w,'giant Sheshnag with nine cobra hoods and the Earth on his central hood',alpha=1,**k)
CH=lambda who,x,y,s,pose,emo:dict(who=who,x=x,y=y,s=s,_face=.46,flip=1,pose=pose,emo=emo,look=700)
SPEC['reel25']['over']={
 0:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.07),NM('Sheshnag',130)]),
 1:dict(scene='night',bg='cosmos',chars=[],fx=[SN(seed=1)]),
 2:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.07),pfx('mist_wisps',None,640,420,700,'mist hiding Sheshnag',alpha=.75)]),
 3:dict(scene='teal',bg='sea',chars=[CH('vishnu_rest',640,690,.9,'lie','calm')],fx=[]),
 4:dict(scene='teal',bg='sea',chars=[CH('vishnu_rest',640,690,.9,'lie','calm')],fx=[pfx('wave_ocean',None,640,690,700,'the endless ocean Vishnu sleeps on',alpha=.9)]),
 5:dict(scene='teal',bg='sea',chars=[CH('vishnu_rest',640,720,.8,'lie','calm'),dict(who='brahma',x=640,y=430,s=.62,_face=.4,flip=1,pose='stand',emo='calm',look=700)],fx=[pfx('divine_rays',None,640,420,520,'golden light where Brahma appears',alpha=.7,behind=True)]),
 6:dict(scene='night',bg='cosmos',chars=[dict(who='brahma',x=640,y=470,s=.62,_face=.38,flip=1,pose='stand',emo='calm',look=700)],fx=WORLDS('lotus')),
 7:dict(scene='night',bg='cosmos',chars=[dict(who='brahma',x=640,y=470,s=.62,_face=.38,flip=1,pose='stand',emo='calm',look=700)],fx=WORLDS('top')),
 8:dict(scene='ember',bg='cosmos',chars=[],fx=WORLDS('But')+[pfx('ground_crack',None,640,660,520,'the worlds are too heavy and the ground cracks',alpha=.8)]),
 9:dict(scene='ember',bg='storm',chars=[],fx=WORLDS('stem',260)+[pfx('lightning_forks',None,640,260,560,'everything starts to fall',alpha=.7,behind=True)]),
 10:dict(scene='night',bg='sea',chars=[],fx=[SN(earth=.07),pfx('divine_rays',None,640,300,560,'Sheshnag rising from far below',alpha=.7,behind=True)]),
 11:dict(scene='night',bg='cosmos',chars=[],fx=[SN(640,670,370,stack=14,earth=.05)]),
 12:dict(scene='teal',bg='sea',chars=[],fx=[pfx('tortoise',None,640,690,400,'Vishnu as a giant tortoise holding Sheshnag up',alpha=1),SN(640,500,330,earth=.06)]),
 13:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.07)]),
 14:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.04)]),
 15:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.07),NM('Sheshnag',130)]),
 16:dict(scene='night',bg='cosmos',chars=[],fx=[SN(seed=1)]),
 17:dict(scene='night',bg='cosmos',chars=[],fx=[SN(earth=.07),pfx('mist_wisps',None,640,420,700,'mist hiding Sheshnag',alpha=.8)]),
}
# ================= reel28: Ravana and Sita; a different place and mood for every beat =================
C28=lambda who,x,s,pose,emo,flip=1,y=700:dict(who=who,x=x,y=y,s=s,_face=.46,flip=flip,pose=pose,emo=emo,look=700)
SPEC['reel28']['over']={
 0:dict(scene='ember',bg='palace',chars=[C28('ravana10',575,.8,'stand','scheme'),C28('sita',705,.72,'stand','sad',-1)],fx=[pfx('ember_fire',None,452,672,80,'a palace torch',alpha=.8)]),
 1:dict(scene='ember',bg='palace',chars=[C28('ravana10',575,.8,'stand','calm'),C28('sita',705,.72,'plead','fear',-1)],fx=[pfx('ember_fire',None,452,672,80,'a palace torch',alpha=.8)]),
 2:dict(scene='brown',bg='council',chars=[C28('ravana10',640,.88,'stand','pride')],fx=[pfx('divine_rays',None,640,330,520,'a king in his court',alpha=.5,behind=True)]),
 3:dict(scene='brown',bg='palace',chars=[C28('hanuman',575,.85,'stand','surprise'),C28('kanya',705,.6,'stand','sad',-1),C28('kanya',712,.55,'plead','fear',-1)],fx=[pfx('ember_fire',None,452,672,80,'a palace torch',alpha=.8)]),
 4:dict(scene='indigo',bg='dusk',chars=[C28('ravana10',575,.82,'stand','anger'),C28('kanya',705,.62,'plead','sad',-1),C28('kanya',712,.56,'plead','fear',-1)],fx=[pfx('mist_wisps',None,640,600,640,'a sad mist over the captives',alpha=.7,behind=True)]),
 5:dict(scene='night',bg='night',chars=[C28('kanya',575,.78,'plead','fear'),C28('ravana10',705,.82,'lunge','anger',-1)],fx=[pfx('red_energy_pulse',None,640,420,420,'danger in the dark',alpha=.6,behind=True)]),
 6:dict(scene='indigo',bg='vaikuntha',chars=[C28('brahma',640,.88,'point','anger')],fx=[pfx('curse_glow',None,640,400,460,'the curse glowing',alpha=.9),pfx('divine_rays',None,640,330,520,'Brahma in heaven',alpha=.6,behind=True)]),
 7:dict(scene='indigo',bg='cloudscape',chars=[C28('brahma',575,.85,'point','anger'),C28('ravana10',705,.8,'plead','fear',-1)],fx=[pfx('curse_glow',None,640,400,460,'the curse upon him',alpha=.8)]),
 8:dict(scene='ember',bg='storm',chars=[C28('ravana10',640,.9,'stand','horror')],fx=[pfx('lightning_forks',None,640,260,560,'lightning over the cursed king',alpha=.9,behind=True),pfx('curse_glow',None,640,300,460,'the curse around his heads',alpha=.9)]),
 9:dict(scene='teal',bg='forest',chars=[C28('ravana10',575,.82,'stand','scheme'),C28('sita',780,.72,'plead','fear',-1)],fx=[pfx('mist_wisps',None,640,600,640,'forest mist as she is carried away',alpha=.7,behind=True)]),
 10:dict(scene='brown',bg='garden',chars=[C28('sita',575,.78,'stand','pride'),C28('ravana10',705,.82,'stand','scheme',-1)],fx=[]),
 11:dict(scene='ember',bg='palace',chars=[C28('ravana10',640,.9,'stand','coldsmile')],fx=[pfx('ember_fire',None,452,672,80,'a palace torch',alpha=.8)]),
 12:dict(scene='night',bg='storm',chars=[C28('ravana10',640,.9,'stand','fear')],fx=[pfx('lightning_forks',None,640,260,560,'fear of the curse',alpha=.8,behind=True),pfx('curse_glow',None,640,420,460,'the curse he fears',alpha=.7)]),
 13:dict(scene='ember',bg='palace',chars=[C28('ravana10',575,.8,'stand','calm'),C28('sita',705,.72,'stand','sad',-1)],fx=[pfx('ember_fire',None,452,672,80,'a palace torch',alpha=.8)]),
 14:dict(scene='night',bg='night',chars=[C28('ravana10',640,.9,'stand','shame')],fx=[pfx('curse_glow',None,640,420,460,'the curse he fears',alpha=.6)]),
 15:dict(scene='brown',bg='council',chars=[C28('ravana10',640,.88,'stand','shame')],fx=[pfx('mist_wisps',None,640,600,640,'a quiet end',alpha=.6,behind=True)]),
}

# ================= reel19 (Markandeya): the Shivling is always on screen, the rope, Shiva coming out of it =================
LGM=lambda x=745,y=620,w=240,g=.8:pfx('lingam',None,x,y,w,'a dark stone Shivling with ash lines on a round base',alpha=1,glow=g)
MK=lambda x,pose,emo,s=.7:dict(who='markandeya',x=x,y=700,s=s,_face=.46,flip=1,pose=pose,emo=emo,look=700)
SPEC['reel19'].setdefault('over',{}).update({
 10:dict(scene='night',bg='temple_dummy' if False else None,chars=[MK(575,'stand','fear')],fx=[LGM(),pfx('mist_wisps',None,640,600,640,'mist around the temple at night',alpha=.6,behind=True)]),
 11:dict(scene='night',chars=[MK(585,'sitpray','devotion')],fx=[LGM(745,620,250,1.0),pfx('divine_rays',None,745,420,520,'light on the Shivling the boy is hugging',alpha=.7,behind=True)]),
 12:dict(scene='ember',bg='storm',chars=[dict(who='yama',x=545,y=690,s=.9,_face=.44,flip=1,pose='throw',emo='rage',look=700),MK(790,'sitpray','fear',.5)],fx=[LGM(760,640,200,.6),pfx('noose',None,700,560,420,'the rope of Yama thrown around the boy and the Shivling',alpha=1)]),
 13:dict(scene='ember',bg='storm',chars=[dict(who='shiva',x=600,y=700,s=.9,_face=.44,flip=1,pose='rage',emo='anger',look=700)],fx=[LGM(790,650,170,.6),pfx('lightning_forks',None,640,260,560,'the anger of Shiva',alpha=.8,behind=True),pfx('red_energy_pulse',None,640,420,420,'a red glow of rage',alpha=.7,behind=True)]),
 14:dict(scene='ember',bg='storm',chars=[dict(who='shiva',x=600,y=700,s=.95,_face=.44,flip=1,pose='rage',emo='anger',look=700),dict(who='yama',x=800,y=700,s=.6,_face=.5,flip=-1,pose='fall',emo='fear',look=700)],fx=[LGM(620,690,190,1.0),pfx('ground_crack',None,640,670,520,'the Shivling cracking open as Shiva comes out',alpha=.8),pfx('divine_rays',None,640,330,560,'blinding light from the Shivling',alpha=.8,behind=True)]),
})
# ================= reel22 (Kalki): darker and dangerous =================
SPEC['reel22']['scene']='night'
KR=lambda y_h=735,y_k=585:[dict(who='horse',x=640,y=y_h,s=.9,_fixed=True,flip=1,pose='stand',emo='anger',look=700),dict(who='kalki',x=640,y=y_k,s=.52,_fixed=True,flip=1,pose='stand',emo='rage',look=700,prop='sword')]
SPEC['reel22'].setdefault('over',{}).update({
 4:dict(scene='ember',bg='storm',chars=[dict(who='kalki',x=640,y=700,s=1.0,_face=.4,flip=1,pose='stand',emo='rage',look=700,prop='sword')],fx=[pfx('lightning_forks',None,640,260,560,'a storm over the dangerous avatar',alpha=.9,behind=True),pfx('red_energy_pulse',None,640,420,420,'a red glow of danger',alpha=.8,behind=True)]),
 12:dict(scene='ember',bg='storm',vertical={'focus':'kalki'},chars=KR(),fx=[pfx('lightning_forks',None,640,260,560,'lightning as Kalki rides out',alpha=.9,behind=True),pfx('ember_fire',None,452,672,90,'fire on the ground',alpha=.8),pfx('ember_fire',None,830,672,90,'fire on the ground',alpha=.8),pfx('red_energy_pulse',None,640,420,460,'a red glow of power',alpha=.7,behind=True)]),
 13:dict(scene='night',bg='kailash',chars=[dict(who='kalki',x=640,y=700,s=1.0,_face=.4,flip=1,pose='raise',emo='calm',look=700,prop='sword')],fx=[pfx('divine_rays',None,640,330,560,'first light of a new age',alpha=.8,behind=True)]),
 17:dict(scene='ember',bg='storm',vertical={'focus':'kalki'},chars=KR(),fx=[pfx('lightning_forks',None,640,260,560,'lightning as Kalki rides out',alpha=.9,behind=True),pfx('smoke_plume',None,640,560,520,'smoke of a burning age',alpha=.6)]),
 18:dict(scene='night',bg='dusk',vertical={'focus':'kalki'},chars=KR(),fx=[pfx('mist_wisps',None,640,600,640,'mist over the village of Shambhala',alpha=.7,behind=True),pfx('red_energy_pulse',None,640,420,460,'a red glow of power',alpha=.6,behind=True)]),
 19:dict(scene='ember',bg='storm',chars=[dict(who='kalki',x=640,y=700,s=1.0,_face=.4,flip=1,pose='stand',emo='rage',look=700,prop='sword')],fx=[pfx('lightning_forks',None,640,260,560,'a storm over the dangerous avatar',alpha=.9,behind=True),pfx('red_energy_pulse',None,640,420,420,'a red glow of danger',alpha=.8,behind=True)]),
})
