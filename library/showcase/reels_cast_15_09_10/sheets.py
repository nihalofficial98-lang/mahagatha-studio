"""Overview sheets of the cast for REELS 15 (Garuda), 09 (Bhasmasura), 10 (Indra, Diti, Marutas) (owner approval).  Same render pipeline as studio/cast_sheet.py (engine build + still.js),
but with custom frames: animal forms, crowds, story forms and one line-up per reel.
  python3 library/showcase/reels_cast_15_09_10/sheets.py [frame names ...]  -> library/showcase/reels_cast_15_09_10/<name>.jpg
Per-character face/pose sheets come from:  python3 studio/cast_sheet.py <names> --out library/showcase/reels_cast_15_09_10"""
import os,sys,json,subprocess,shutil
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))));sys.path.insert(0,R+'/studio')
import build as B
from PIL import Image
OUT=os.path.dirname(os.path.abspath(__file__))
INK='#3a2414'
BG={'k':'plain','cols':['#f4e6c8','#e2c99c','#c9a878'],'fore':False}
def lab(s,x,y,size=19,col=INK):return {'t':'text','s':s,'x':x,'y':y,'size':size,'col':col}
def F(who,x,y,s=.8,**k):d={'who':who,'x':x,'y':y,'s':s};d.update(k);return d

def P(k,x,y,w,**o):d={'t':'pfx','k':k,'x':x,'y':y,'w':w};d.update(o);return d
SKY={'k':'cloudscape','fore':False}
FRAMES={
 # ---------- Reel 15: Garuda ----------
 'garuda_forms':dict(title='Garuda (Reel 15): half bird, half man - wings fold / spread / beat (wing, flap keys), carries the Amrut (prop amrut)',bg=SKY,figs=[
   ('standing, wings folded',F('garuda',130,660,.78,emo='calm')),
   ('flying with the Amrut (pose fly)',F('garuda',420,600,.78,pose='fly',prop='amrut',emo='calm')),
   ('power: wings spread',F('garuda',740,660,.78,pose='spread',emo='anger')),
   ('bows to Vishnu',F('garuda',1040,660,.78,pose='bow',emo='devotion')),
   ('frozen (fear)',F('garuda',1180,250,.34,head=True,emo='fear')),('joy',F('garuda',960,250,.34,head=True,emo='joy')),('determined',F('garuda',740,250,.34,head=True,emo='anger'))],
   fx=[P('golden_feather',560,200,90,fall=1)]),
 'garuda_motion':dict(title='Garuda - flap cycle (pose fly at 4 moments), glide, carry, namaste',bg=SKY,figs=[
   ('fly',F('garuda',140,560,.62,pose='fly',prop='amrut',flap=1,wing=1)),('',F('garuda',380,560,.62,pose='fly',prop='amrut',flap=1.35)),('',F('garuda',620,560,.62,pose='fly',prop='amrut',flap=.6)),
   ('glide',F('garuda',870,560,.62,pose='glide',emo='joy')),('carry (standing)',F('garuda',1060,660,.62,pose='carry',prop='amrut')),('namaste',F('garuda',1200,660,.62,pose='namaste',emo='devotion'))]),
 'nagas':dict(title='Nagas (Reel 15): naga / naga2 crowd, naga_guard (big, crowned); pose stand | bow | point=strike | sit=coil',figs=[
   ('nagas, hoods raised',F('naga',120,640,.5,emo='anger')),('',F('naga2',250,650,.46,flip=-1)),('',F('naga',360,655,.42,pose='sit')),
   ('bowing before the pot',F('naga2',520,650,.5,pose='bow',flip=-1)),
   ('Vinata, their slave',F('vinata',700,660,.72,pose='plead',emo='grief')),
   ('the two guard snakes',F('naga_guard',900,660,.5)),('',F('naga_guard',1130,660,.5,pose='point',flip=-1,emo='rage')),
   ('naga close-up',F('naga',560,150,.3,head=True,emo='anger')),('guard close-up',F('naga_guard',800,150,.3,head=True))],fx=[P('amrut_pot',430,600,70)]),
 'reel15_props':dict(title='Reel 15 props: Amrut pot inside the ring of fire, spinning blades, golden feather, thrown Vajra',bg={'k':'storm','r':.3,'fore':False},labcol='#ffe9b8',figs=[
   ('Garuda breaks through',F('garuda',980,600,.62,pose='fly',prop='amrut',emo='anger',flap=1.2))],
   extra=[],fx=[P('fire_ring',300,610,420,part='back'),P('amrut_pot',300,560,80),P('fire_ring',300,610,420,part='front'),P('spinning_blades',660,300,230),
     P('golden_feather',650,560,110,fall=1),P('vajra_thrown',1080,170,260,flip=-1),
     lab('ring of fire + Amrut pot',300,700,17,'#ffe9b8'),lab('spinning blades',660,440,17,'#ffe9b8'),lab('golden feather',650,640,17,'#ffe9b8'),lab('thrown Vajra',1080,230,17,'#ffe9b8')]),
 # ---------- Reel 09: Bhasmasura ----------
 'bhasma_forms':dict(title='Reel 9 - Vrikasura (devotee) becomes Bhasmasura: tapasya, sword at his neck, the boon hand, the chase',figs=[
   ('Vrikasura: tapasya',F('vrikasura',130,650,.74,pose='sitpray',mood={'blink':1})),('sword at his own neck',F('vrikasura',380,650,.74,pose='selfcut',prop='sword',emo='grief')),
   ('Bhasmasura raises his hand',F('bhasmasura',640,660,.76,pose='raise',emo='anger')),('the chase',F('bhasmasura',880,660,.76,pose='run',emo='rage')),
   ('Shiva runs',F('shiva',1150,660,.74,pose='flee',emo='fear',flip=-1)),
   ('Vrikasura',F('vrikasura',300,190,.3,head=True,emo='devotion')),('Bhasmasura',F('bhasmasura',520,190,.3,head=True,emo='rage')),('stares at Parvati',F('bhasmasura',740,190,.3,head=True,mood={'smile':.6,'lx':.8,'ly':-.1}))]),
 'bhasma_ash':dict(title='Reel 9 - hand on his own head: Bhasmasura turns to ash (key ash 0..1, or ashc cue + ashd seconds)',bg={'k':'vaikuntha'},figs=[
   ('Mohini: hand on head',F('mohini',130,660,.76,pose='headtouch',mood={'smile':.7})),('he copies her',F('bhasmasura',360,660,.76,pose='headtouch',mood={'smile':.5})),
   ('ash .45',F('bhasmasura',600,660,.76,pose='headtouch',ash=.45)),('ash .75',F('bhasmasura',840,660,.76,pose='headtouch',ash=.75)),('ash 1: ash pile',F('bhasmasura',1050,660,.76,pose='headtouch',ash=1)),
   ('spin',F('mohini',1210,660,.6,pose='dance2',spin=.07,mood={'smile':.8,'mouth':.4}))]),
 'mohini_forms':dict(title='Reel 9 - Mohini: Vishnu\'s enchantress form (Vishnu-blue skin, red sari, yellow pallu): dance poses',bg={'k':'vaikuntha'},figs=[
   ('Vishnu',F('vishnu',130,660,.74,emo='calm')),('Mohini',F('mohini',330,660,.76,emo='joy')),('dance',F('mohini',520,660,.76,pose='dance',mood={'smile':.7})),
   ('dance2',F('mohini',710,660,.76,pose='dance2',mood={'smile':.7,'lx':.6})),('"Come, dance with me"',F('mohini',900,660,.76,pose='open',mood={'smile':.8,'mouth':.4})),
   ('laughs',F('mohini',1120,250,.34,head=True,mood={'smile':1,'mouth':.6,'blink':.4})),('sly',F('mohini',1120,560,.34,head=True,mood={'smile':.6,'lx':.8,'blink':.3}))]),
 'reel09_places':dict(title='Reel 9 places: Kailash (Parvati walks down the hill) and the new Vaikuntha background',bg={'k':'kailash'},labcol='#ffe9b8',figs=[
   ('Parvati',F('parvati',200,660,.78,emo='calm')),('walking',F('parvati',420,660,.78,walk=1,mood={'lx':.6})),('Narada',F('narada',600,660,.74,mood={'smile':.6,'lx':.8})),
   ('Parvati: fear',F('parvati',820,250,.34,head=True,emo='fear')),('surprise',F('parvati',1060,250,.34,head=True,emo='surprise'))]),
 'vaikuntha_bg':dict(title='new background: vaikuntha (bg k:"vaikuntha"; sx/sy sun, y1 clouds, sea = milk ocean line)',bg={'k':'vaikuntha'},figs=[
   ('"Protect me"',F('shiva',420,660,.74,pose='plead',emo='fear',flip=1)),('Vishnu',F('vishnu',820,660,.74,emo='calm',flip=-1))]),
 # ---------- Reel 10: Indra, Diti, Marutas ----------
 'diti_forms':dict(title='Reel 10 - Diti (pregnant: diti_p): tapasya, asleep with unwashed feet (pose sleep), Indra sneaking',bg={'k':'dusk'},labcol='#ffe9b8',figs=[
   ('tapasya',F('diti_p',110,650,.7,pose='sitpray',mood={'blink':1})),('standing',F('diti_p',290,660,.72,emo='calm')),
   ('asleep (sleep)',F('diti_p',560,660,.7,pose='sleep')),('Kashyapa: the rules',F('kashyapa',820,660,.7,pose='point',emo='calm')),('Indra sneaks (sneak)',F('indra',1010,660,.72,pose='sneak',mood={'lx':-.6,'anger':.3},flip=-1)),
   ('Indra throws (throw)',F('indra',1190,660,.68,pose='throw',emo='anger',flip=-1)),
   ('Diti',F('diti_p',470,170,.3,head=True,emo='calm')),('Diti asleep',F('diti_p',700,170,.3,head=True,mood={'blink':1,'smile':.1}))]),
 'womb_marutas':dict(title='Reel 10 - womb_view (n 1/7/49, cry, flash), maruta_pieces (spread, cry, born), maruta_baby crowd, grown maruta',bg={'k':'voidR','rgb':'255,120,80'},labcol='#ffe9b8',figs=[
   ('Marutas (grown)',F('maruta',1060,680,.6,emo='joy')),('',F('maruta',1200,680,.6,emo='calm',flip=-1)),('Indra',F('indra',930,680,.62,emo='joy'))],
   fx=[P('womb_view',150,200,240,n=1),P('womb_view',420,200,240,n=1,flash=1,cry=.5),P('womb_view',700,200,240,n=7,cry=1),P('womb_view',990,200,240,n=49,spread=1,cry=1),
     P('maruta_pieces',330,560,230,n=49,born=1,cry=1),P('maruta_pieces',650,540,260,n=7,born=1,cry=0),
     lab('the unborn child',150,345,16,'#ffe9b8'),lab('the Vajra flashes',420,345,16,'#ffe9b8'),lab('seven pieces, crying',700,345,16,'#ffe9b8'),lab('forty-nine',990,345,16,'#ffe9b8'),
     lab('49 crying babies (born:1)',330,712,16,'#ffe9b8'),lab('calm',650,700,16,'#ffe9b8')]),
}
LINE={
 'reel15':('Reel 15 - How did Garuda become Vishnu\'s vahana?',[('Garuda','garuda',{'pose':'carry','prop':'amrut'}),('Vinata','vinata',{'emo':'sad'}),('naga','naga',{'emo':'anger'}),('naga2','naga2',{}),('guard snake','naga_guard',{}),('Vishnu','vishnu',{'emo':'joy'}),('Indra','indra',{'pose':'throw','emo':'anger','flip':-1})]),
 'reel09':('Reel 9 - Why did Shiva run from his own devotee?',[('Narada','narada',{'mood':{'smile':.6}}),('Vrikasura','vrikasura',{'pose':'namaste','emo':'devotion'}),('Shiva','shiva',{'emo':'calm'}),('Parvati','parvati',{'emo':'calm'}),('Bhasmasura','bhasmasura',{'pose':'raise','emo':'anger'}),('Vishnu','vishnu',{}),('Mohini','mohini',{'pose':'dance','mood':{'smile':.7}})]),
 'reel10':('Reel 10 - A mother prayed 100 years for a son to kill Indra',[('Diti','diti_p',{'emo':'calm'}),('Kashyapa','kashyapa',{'pose':'point'}),('Indra (sneaking)','indra',{'pose':'sneak','flip':-1,'mood':{'lx':-.6}}),('Maruta babies','maruta_baby',{'emo':'grief'}),('','maruta_baby',{'emo':'joy'}),('Maruta (grown)','maruta',{'emo':'joy'}),('Hiranyaksha','hiranyaksha',{'emo':'anger'})]),
}
for k,(title,items) in LINE.items():
    n=len(items);dx=1180/n;figs=[]
    for i,(l,w,o) in enumerate(items):
        f=F(w,int(60+dx*(i+.5)),660,.72);f.update(o)
        if w.startswith('naga'):f['s']=.42 if w!='naga_guard' else .36
        figs.append((l,f))
    FRAMES['lineup_'+k]=dict(title=title,figs=figs)

def shot(T,fr):
    figs=[f for _,f in fr['figs']]+fr.get('extra',[]);lc=fr.get('labcol',INK)
    fx=[lab(l,f['x'],(f['y']+int(330*f['s'])) if f.get('head') else min(712,f['y']+26),17,lc) for l,f in fr['figs'] if l]+[lab(fr['title'],640,30,24,lc)]
    fx=fx+fr.get('fx',[])
    return {'beat':1,'at':T,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':fr.get('bg',BG),'figs':figs,'fx':fx}}

def main():
    names=sys.argv[1:] or list(FRAMES)
    shots=[{'beat':1,'at':0,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':BG,'figs':[],'fx':[]}}]
    for i,n in enumerate(names):shots.append(shot(i+1,FRAMES[n]))
    T=len(names)+1;tmp=R+'/build/reels_cast_sheet_15_09_10';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp)
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
