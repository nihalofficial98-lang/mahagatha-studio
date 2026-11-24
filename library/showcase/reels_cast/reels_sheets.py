"""Overview sheets of the REELS cast (owner approval).  Same render pipeline as studio/cast_sheet.py (engine build + still.js),
but with custom frames: animal forms, crowds, story forms and one line-up per reel.
  python3 library/showcase/reels_cast/reels_sheets.py [frame names ...]     -> library/showcase/reels_cast/<name>.jpg
Per-character face/pose sheets come from:  python3 studio/cast_sheet.py <names> --out library/showcase/reels_cast"""
import os,sys,json,subprocess,shutil
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))));sys.path.insert(0,R+'/studio')
import build as B
from PIL import Image
OUT=os.path.dirname(os.path.abspath(__file__))
INK='#3a2414'
BG={'k':'plain','cols':['#f4e6c8','#e2c99c','#c9a878'],'fore':False}
def lab(s,x,y,size=19,col=INK):return {'t':'text','s':s,'x':x,'y':y,'size':size,'col':col}
def F(who,x,y,s=.8,**k):d={'who':who,'x':x,'y':y,'s':s};d.update(k);return d

FRAMES={
 # ---------- Brahmi as Shatarupa ----------
 'shatarupa_forms':dict(title='Shatarupa - Brahmi\'s animal forms (Reel 2): gold necklace + green gem = Brahmi',figs=[
   ('Brahmi (moving away)',F('brahmi',120,660,.82,emo='fear',mood={'lx':-.8},flip=-1)),
   ('cow',F('cow',380,640,.7)),('mare',F('mare',740,640,.62)),('doe',F('doe',1050,640,.8)),
   ('duck',F('duck',1210,400,.9)),
   ('cow - head',F('cow',420,250,.42,head=True)),('mare - head',F('mare',660,250,.42,head=True)),('doe - head',F('doe',900,250,.42,head=True)),('duck - head',F('duck',1140,140,.3,head=True,mood={'blink':0}))]),
 'animals_motion':dict(title='animal forms - poses: stand / walk:1 / run (legs swing) / bow (head lowered); flip:-1 faces left',figs=[
   ('cow run',F('cow',220,330,.55,pose='run')),('cow bow',F('cow',560,330,.55,pose='bow')),('mare run',F('mare',930,330,.5,pose='run')),
   ('mare bow',F('mare',220,680,.5,pose='bow')),('doe run',F('doe',560,680,.62,pose='run')),('doe bow',F('doe',860,680,.62,pose='bow')),('duck run, facing left',F('duck',1130,680,.75,pose='run',flip=-1))]),
 # ---------- Kapali / Brahma's fifth head ----------
 'kapali_forms':dict(title='Kashi story (Reel 2): five-headed Brahma, Shiva in fury, Kapali',figs=[
   ('Brahma, five heads (seated)',F('brahma5',170,640,.78,emo='calm')),
   ('five heads, standing: gazing',F('brahma5',430,660,.8,pose='stand',lotus=False,mood={'smile':.4,'lx':.8})),
   ('Shiva in fury',F('shiva',690,660,.8,pose='rage',emo='rage')),
   ('the head stuck to his hand',F('kapali',940,660,.8,prop='head',emo='sad')),
   ('Kapali: only the skull remains',F('kapali',1170,660,.8,emo='sad',mood={'ly':.3})),
   ],extra=[F('brahma5',1000,150,.3,head=True,emo='shame')]),
 # ---------- Rudra ----------
 'rudra_forms':dict(title='Rudra (Reel 5): born from Brahma\'s anger - fire halo, blazing red eyes; the eleven Rudras',figs=[
   ('"What is my name?"',F('rudra',170,660,.85,pose='raise',emo='rage')),
   ('rage close-up',F('rudra',420,190,.4,head=True,emo='rage')),('calm close-up',F('rudra',660,190,.4,head=True,emo='calm')),
   ('meditating (leaves)',F('rudra',1080,650,.75,pose='sitpray',mood={'blink':1})),
   ('Brahma in awe',F('brahma',820,650,.62,emo='surprise')),
   ]),
 'rudras_crowd':dict(title='the eleven Rudras (Reel 5): one rig repeated, flipped and scaled',bg={'k':'cloudscape','fore':False},figs=[('',f) for f in
   [F('rudra',140+i*100,520+(i%2)*40,.48+(i%2)*.04,flip=1 if i<5 else -1,emo='calm',pose='namaste' if i%3==0 else 'stand') for i in range(11)]]),
 # ---------- Reel 6 ----------
 'swaha_forms':dict(title='Reel 6 - Swaha: starving gods, Kamadeva, Agni, Prakriti, Swaha',figs=[
   ('starving gods',F('deva_thin',90,660,.72,emo='sad')),('',F('deva_thin2',210,660,.72,emo='grief',pose='plead')),('Indra (thin)',F('indra_thin',350,660,.74,emo='sad',pose='open')),
   ('Kamadeva blames',F('kama',520,660,.76,pose='point',emo='anger')),('Agni: "my fault"',F('agni',700,660,.76,pose='namaste',emo='shame')),
   ('Prakriti',F('prakriti',880,660,.76,emo='calm')),('Swaha',F('swaha',1050,660,.76,pose='namaste',emo='joy')),('Vishnu',F('vishnu',1210,660,.7,emo='calm'))]),
 # ---------- Reel 4 ----------
 'maya_family':dict(title='Reel 4 - Narada\'s maya: the young woman, the family, the old householder',figs=[
   ('Narada (veena)',F('narada',110,660,.76,emo='calm')),('the young woman at the river',F('kanya',290,660,.76,emo='joy',mood={'lx':-.6})),
   ('Narada, householder',F('narada_g',470,660,.76,emo='joy')),('children',F('balak',610,660,.76,emo='joy')),('',F('balika',700,660,.76,emo='joy',flip=-1)),
   ('Narada, grandfather',F('narada_old',880,660,.76,emo='calm',pose='open')),('grandchildren',F('balika',1010,660,.62,emo='joy')),('',F('balak',1090,660,.62,emo='surprise',flip=-1)),
   ('swept away: grief',F('narada_old',1210,660,.76,emo='grief',pose='plead',flip=-1))]),
 # ---------- Reel 3 ----------
 'nidra_forms':dict(title='Reel 3 - Madhu and Kaitabha: Yoga Nidra releases Vishnu',figs=[
   ('Vishnu in Yoga Nidra',F('vishnu_rest',330,660,.62)),('Nidra devi',F('nidra',700,660,.82,pose='namaste',mood={'blink':.45,'smile':.4})),
   ('Hayagriva',F('hayagriva2',900,660,.8,emo='calm')),('Madhu',F('madhu',1060,660,.8,emo='rage',pose='lunge')),('Kaitabha',F('kaitabha',1210,660,.8,emo='anger',flip=-1)),
   ('Nidra close-up',F('nidra',560,170,.36,head=True,mood={'blink':.5,'smile':.45})),('Hayagriva fights',F('hayagriva2',900,170,.36,head=True,emo='anger')),('Hayagriva calm',F('hayagriva2',1150,170,.36,head=True,emo='calm'))]),
 # ---------- Reel 7 ----------
 'sons_crowd':dict(title='Reel 7 - Daksha\'s sons: Haryashvas (green) and Shavalashvas (violet) - crowd rigs',figs=[('',f) for f in
   [F('haryashva',70+i*84,430+(i%2)*18,.4,flip=1 if i%3 else -1,emo='doubt' if i%2 else 'calm') for i in range(8)]+
   [F('shavalashva',700+i*84,430+(i%2)*18,.4,flip=-1 if i%3 else 1,emo='doubt' if i%2 else 'calm') for i in range(7)]]+[
   ('Daksha roars',F('daksha',200,690,.74,pose='point',emo='rage')),('Asikli',F('asikli',380,690,.74,emo='sad')),
   ('Haryashva',F('haryashva',560,690,.74,emo='doubt')),('Shavalashva',F('shavalashva',740,690,.74,emo='doubt')),
   ('Narada smirks',F('narada',920,690,.74,mood={'smile':.8,'lx':-.7,'ly':.15,'blink':.25},flip=-1)),('Narada cursed: wanders',F('narada',1120,690,.74,emo='calm',walk=1,flip=-1))]),
}
# one line-up per reel (everyone who appears, at a common scale)
LINE={
 'reel01':('Reel 1 - Did Shiva create the first humans?',[('Brahma (grief)','brahma',{'emo':'sad'}),('Vishnu','vishnu',{}),('Shiva meditating','shiva',{'pose':'sitpray','mood':{'blink':1}}),('Ardhanarishwara','ardha',{}),('the Goddess (Shakti)','adishakti',{'pose':'open','emo':'calm'}),('Manu','manu',{'emo':'joy'}),('Brahmi','brahmi',{'emo':'joy'})]),
 'reel02':('Reel 2 - Why people go to Kashi',[('Narada (curse)','narada',{'pose':'point','emo':'anger'}),('Brahma, five heads','brahma5',{'pose':'stand','lotus':False,'mood':{'smile':.4,'lx':.8}}),('Brahmi','brahmi',{'emo':'fear','flip':-1}),('Marichi','rishi1',{'pose':'raise','emo':'anger'}),('Atri','rishi2',{'pose':'point','emo':'doubt'}),('Shiva in fury','shiva',{'pose':'rage','emo':'rage'}),('Kapali','kapali',{'emo':'sad'})]),
 'reel03':('Reel 3 - Madhu and Kaitabha',[('Brahma on the lotus','brahma',{'emo':'fear'}),('Vishnu','vishnu',{'emo':'calm'}),('Nidra','nidra',{'mood':{'blink':.45}}),('Hayagriva','hayagriva2',{}),('Madhu','madhu',{'emo':'pride'}),('Kaitabha','kaitabha',{'emo':'pride','flip':-1})]),
 'reel04':('Reel 4 - Narada and Maya',[('Narada','narada',{'emo':'doubt'}),('Vishnu smiling','vishnu',{'emo':'joy'}),('the young woman','kanya',{'emo':'joy'}),('Narada, householder','narada_g',{'emo':'joy'}),('child','balak',{'emo':'joy'}),('child','balika',{'emo':'joy'}),('Narada, old','narada_old',{'emo':'grief'})]),
 'reel05':('Reel 5 - Shiva born from Brahma\'s anger',[('Brahma','brahma',{'emo':'anger'}),('Kumara','kumara',{'pose':'namaste'}),('Kumara','kumara',{'pose':'namaste'}),('Rudra (fiery birth)','rudra',{'pose':'raise','emo':'rage'}),('Rudra (calm)','rudra',{'emo':'calm'}),('Shiva / Mahadeva','shiva',{'emo':'calm'})]),
 'reel06':('Reel 6 - Swaha',[('Brahma','brahma',{'emo':'doubt'}),('starving god','deva_thin',{'emo':'sad'}),('Indra','indra_thin',{'emo':'sad','pose':'open'}),('Kamadeva','kama',{'pose':'point','emo':'anger'}),('Agni','agni',{'pose':'namaste','emo':'shame'}),('Vishnu','vishnu',{}),('Prakriti','prakriti',{}),('Swaha','swaha',{'emo':'joy'})]),
 'reel07':('Reel 7 - Daksha cursed Narada',[('Daksha','daksha',{'pose':'point','emo':'rage'}),('Asikli','asikli',{'emo':'sad'}),('Haryashva','haryashva',{'emo':'doubt'}),('Shavalashva','shavalashva',{'emo':'doubt'}),('Narada (smirk)','narada',{'mood':{'smile':.8,'lx':-.7,'ly':.15,'blink':.25},'flip':-1})]),
}
for k,(title,items) in LINE.items():
    n=len(items);dx=1180/n;figs=[]
    for i,(l,w,o) in enumerate(items):
        f=F(w,int(60+dx*(i+.5)),660,.74);f.update(o)
        if w=='brahma' and 'pose' not in o:f.update({'s':.6,'y':650})
        if w=='shiva' and o.get('pose')=='sitpray':f.update({'y':650})
        figs.append((l,f))
    FRAMES['lineup_'+k]=dict(title=title,figs=figs)

def shot(T,fr):
    figs=[f for _,f in fr['figs']]+fr.get('extra',[]);lc=fr.get('labcol',INK)
    fx=[lab(l,f['x'],(f['y']+int(330*f['s'])) if f.get('head') else min(712,f['y']+26),17,lc) for l,f in fr['figs'] if l]+[lab(fr['title'],640,30,24,lc)]
    return {'beat':1,'at':T,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':fr.get('bg',BG),'figs':figs,'fx':fx}}

def main():
    names=sys.argv[1:] or list(FRAMES)
    shots=[{'beat':1,'at':0,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':BG,'figs':[],'fx':[]}}]
    for i,n in enumerate(names):shots.append(shot(i+1,FRAMES[n]))
    T=len(names)+1;tmp=R+'/build/reels_cast_sheet';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp)
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
