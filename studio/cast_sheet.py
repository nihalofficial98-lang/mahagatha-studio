"""Character sheets of the CODED cast for owner approval (step 4 of WORKFLOW.md).
  python3 studio/cast_sheet.py brahma vishnu shiva [--out DIR] [--faces calm,anger,...] [--poses stand,walk,...]
  (no names = every human cast member)
Per human character:  <who>_faces.jpg = full figure + five face close-ups (neutral, angry, sad, surprised, joy)
                      <who>_poses.jpg = five poses (stand, walk, bow, point, pray)
                      <who>_forms.jpg = story forms / extra emotions, only for names listed in FORMS below.
Non-human figures and groups (boar, swan, ketaki, devas, jyotirlinga) get a single <name>_forms.jpg.
'walk' is the stand pose with the engine walk cycle (figure key walk:1) caught mid-stride; 'pray' = namaste."""
import os,sys,json,subprocess,argparse,shutil
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,R+'/studio')
import build as B,engine_vocab as V
from PIL import Image

FACES=[('neutral','calm'),('angry','anger'),('sad','sad'),('surprised','surprise'),('joy','joy')]
POSES=[('stand','stand',{}),('walk','stand',{'walk':1}),('bow','bow',{}),('point','point',{}),('pray','namaste',{})]
BG={'k':'plain','cols':['#f4e6c8','#e2c99c','#c9a878'],'fore':False}     # warm paper backdrop (bright EP6 look)
INK='#3a2414'
NONHUMAN={'boar','swan','ketaki'}
GROUPS={'devas','jyotirlinga'}
lab=lambda s,x,y,size=22:{'t':'text','s':s,'x':x,'y':y,'size':size,'col':INK}

# story forms (EP6): each entry = list of (label, figure dict) placed left to right, or a full frame dict
def FORMS():
    return {
 'brahma':{'title':'brahma - forms (EP6)','figs':[
    ('seated on the lotus',{'who':'brahma','x':150,'y':640,'s':.95,'emo':'calm'}),
    ('standing',{'who':'brahma','x':400,'y':650,'s':.9,'pose':'stand','lotus':False,'emo':'pride'}),
    ('pride',{'who':'brahma','x':640,'y':250,'s':.36,'head':True,'emo':'pride'}),
    ('fear (lost inside Vishnu)',{'who':'brahma','x':860,'y':250,'s':.36,'head':True,'emo':'fear'}),
    ('sly smile (the lie)',{'who':'brahma','x':1080,'y':250,'s':.36,'head':True,'mood':{'smile':.8,'lx':.8,'ly':.15,'blink':.3}}),
    ('rage (the quarrel)',{'who':'brahma','x':640,'y':545,'s':.36,'head':True,'emo':'rage'}),
    ('shame (cursed)',{'who':'brahma','x':860,'y':545,'s':.36,'head':True,'emo':'shame'}),
    ('doubt',{'who':'brahma','x':1080,'y':545,'s':.36,'head':True,'emo':'doubt'})]},
 'vishnu':{'title':'vishnu - forms (EP6)','figs':[
    ('standing',{'who':'vishnu','x':160,'y':650,'s':.95,'emo':'calm'}),
    ('admits defeat',{'who':'vishnu','x':420,'y':650,'s':.95,'pose':'namaste','emo':'devotion'}),
    ('Varaha (boar) - digging',{'who':'boar','x':780,'y':420,'s':1.05,'pose':'dig'}),
    ('Varaha - running',{'who':'boar','x':1080,'y':420,'s':.9,'pose':'run'}),
    ('rage (the quarrel)',{'who':'vishnu','x':780,'y':545,'s':.36,'head':True,'emo':'rage'}),
    ('wonder',{'who':'vishnu','x':1030,'y':545,'s':.36,'head':True,'emo':'surprise'})]},
 'shiva':{'title':'shiva - forms (EP6)','bg':{'k':'pillar','ct':-2,'px':400,'pw':120},'figs':[
    ('emerging from the cracked Jyotirlinga, furious: "Liar!"',{'who':'shiva','x':400,'y':690,'s':1.15,'pose':'rpoint','emo':'rage','flip':-1}),
    ('rage stance',{'who':'shiva','x':830,'y':660,'s':.95,'pose':'rage','emo':'rage'}),
    ('stern judgement',{'who':'shiva','x':1130,'y':250,'s':.38,'head':True,'emo':'anger'}),
    ('calm (leaving)',{'who':'shiva','x':1130,'y':545,'s':.38,'head':True,'emo':'calm'})],'labcol':'#ffe9b8'},
 'daksha':{'title':'daksha - forms (EP6 ending)','figs':[
    ('watching Shiva leave',{'who':'daksha','x':200,'y':650,'s':.95,'pose':'stand','mood':{'anger':.8,'sad':.7,'lx':.8}}),
    ('hateful + tearful',{'who':'daksha','x':560,'y':330,'s':.5,'head':True,'mood':{'anger':.85,'sad':.75,'ly':.1}}),
    ('burning hatred',{'who':'daksha','x':860,'y':330,'s':.5,'head':True,'emo':'rage'}),
    ('grief',{'who':'daksha','x':1130,'y':330,'s':.5,'head':True,'emo':'grief'})]},
 'ketaki':{'title':'ketaki - the flower that speaks (EP6)','figs':[
    ('neutral, falling',{'who':'ketaki','x':120,'y':300,'s':.8,'emo':'calm','fall':1}),
    ('speaks',{'who':'ketaki','x':325,'y':300,'s':.8,'mood':{'smile':.4,'mouth':.5}}),
    ('afraid: "a lie?"',{'who':'ketaki','x':530,'y':300,'s':.8,'emo':'fear'}),
    ('false witness',{'who':'ketaki','x':735,'y':300,'s':.8,'mood':{'smile':.6,'mouth':.45,'ly':-.3}}),
    ('shame',{'who':'ketaki','x':940,'y':300,'s':.8,'emo':'shame'}),
    ('withering',{'who':'ketaki','x':1150,'y':300,'s':.8,'wither':.55}),
    ('in the hamsa\'s beak',{'who':'swan','x':260,'y':690,'s':.9}),
    ('held up as proof',{'who':'brahma','x':720,'y':680,'s':.82,'pose':'hold','lotus':False,'emo':'pride'}),
    ('withered (fully)',{'who':'ketaki','x':1080,'y':650,'s':.8,'wither':1})],
    'extra':[{'who':'ketaki','x':452,'y':528,'s':.26,'mood':{'smile':.2}},{'who':'ketaki','x':760,'y':540,'s':.3,'mood':{'smile':.6,'mouth':.45}}]},
 'swan':{'title':'swan - Brahma as the Hamsa (EP6)','bg':{'k':'cloudscape','fore':False},'figs':[
    ('flying up past the clouds',{'who':'swan','x':330,'y':560,'s':1.3}),
    ('with the ketaki in its beak',{'who':'swan','x':880,'y':600,'s':1.2,'glide':1})],
    'extra':[{'who':'ketaki','x':1132,'y':374,'s':.32,'mood':{'smile':.2}}],'labcol':'#3a2414'},
 'boar':{'title':'boar - Vishnu as Varaha (EP6)','bg':{'k':'earth','fore':False},'figs':[
    ('digging down through the earth',{'who':'boar','x':380,'y':560,'s':1.5,'pose':'dig'}),
    ('running',{'who':'boar','x':920,'y':560,'s':1.4,'pose':'run'})]},
 'devas':{'title':'devas - the watching crowd (EP6)','figs':[
    ('indra',{'who':'indra','x':150,'y':650,'s':.86,'emo':'surprise'}),
    ('agni',{'who':'agni','x':395,'y':650,'s':.86,'emo':'fear'}),
    ('surya',{'who':'surya','x':640,'y':650,'s':.86,'emo':'calm'}),
    ('chandra',{'who':'chandra','x':885,'y':650,'s':.86,'emo':'doubt'}),
    ('vayu',{'who':'vayu','x':1130,'y':650,'s':.86,'emo':'surprise','pose':'open'})]},
 'jyotirlinga':{'title':'jyotirlinga - the endless pillar of fire (EP6)','frames':[
    {'bg':{'k':'pillar','px':640,'pw':120},'labcol':'#ffe9b8','figs':[('the pillar appears between them',{'who':'brahma','x':330,'y':690,'s':.72,'pose':'point','lotus':False,'emo':'surprise','flip':1}),
        ('',{'who':'vishnu','x':950,'y':690,'s':.72,'pose':'open','emo':'surprise','flip':-1})]},
    {'bg':{'k':'pillar','px':640,'pw':120,'ct':-2},'labcol':'#ffe9b8','figs':[('it cracks open: Shiva appears',{'who':'shiva','x':640,'y':700,'s':1.1,'pose':'rpoint','emo':'rage','flip':-1})],
        'fx':[{'t':'pfx','k':'om_symbol','x':640,'y':110,'w':120}]}]},
}

def frame_shot(T,figs,fx,bg=None):
    return {'beat':1,'at':T,'draw':'scene','grade':'cel','vig':.12,'cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,'sc':{'bg':bg or BG,'figs':figs,'fx':fx}}

def label_y(f):
    if f.get('head'):return f['y']+int(330*f['s'])
    if f['who']=='ketaki':return f['y']+38
    return min(712,f['y']+20)

def main():
    a=argparse.ArgumentParser();a.add_argument('who',nargs='*');a.add_argument('--out',default=R+'/library/characters/sheets')
    a.add_argument('--faces');a.add_argument('--poses');x=a.parse_args()
    F=FORMS();names=x.who or [w for w in V.CAST if w not in('boar','swan','ketaki','vishnu_rest','ardha','harihara')]
    bad=[n for n in names if n not in V.CAST and n not in GROUPS]
    if bad:sys.exit(f'not in the cast: {bad} (add the spec to engine/v2_cast.js CAST and V2NAMES first)')
    faces=[(e,e) if e not in dict(FACES) else (e,dict(FACES)[e]) for e in x.faces.split(',')] if x.faces else FACES
    poses=[(p,'namaste' if p=='pray' else ('stand' if p=='walk' else p),{'walk':1} if p=='walk' else {}) for p in x.poses.split(',')] if x.poses else POSES
    shots=[];outs=[];T=0
    for n in names:
        if n not in NONHUMAN and n not in GROUPS:
            full={'who':n,'x':140,'y':690,'s':1.0,'emo':'calm'}
            if n=='brahma':full.update({'s':.95,'y':680})
            figs=[full]+[{'who':n,'x':360+i*200,'y':300,'s':.42,'head':True,'emo':e} for i,(_,e) in enumerate(faces)]
            fx=[lab(l,360+i*200,470,24) for i,(l,_) in enumerate(faces)]+[lab(n,140,36,30)]
            shots.append(frame_shot(T,figs,fx));outs.append(f'{n}_faces');T+=1
            figs=[];fx=[]
            for i,(l,p,extra) in enumerate(poses):
                f={'who':n,'x':150+i*245,'y':660,'s':.9,'pose':p,'emo':'calm'};f.update(extra)
                if n=='brahma':f['lotus']=False
                figs.append(f);fx.append(lab(l,150+i*245,700,24))
            fx.append(lab(n,640,30,26))
            shots.append(frame_shot(T,figs,fx));outs.append(f'{n}_poses');T+=1
        if n in F:
            spec=F[n];frames=spec.get('frames') or [spec]
            for k,fr in enumerate(frames):
                figs=[f for _,f in fr['figs']]+fr.get('extra',spec.get('extra',[]) if k==0 else [])
                lc=fr.get('labcol',spec.get('labcol',INK));L=lambda *a:dict(lab(*a),col=lc)
                fx=[L(l,f['x'],label_y(f),19) for l,f in fr['figs'] if l]+[L(spec['title'],640,30,26)]+fr.get('fx',[])
                shots.append(frame_shot(T,figs,fx,fr.get('bg')));outs.append(f'{n}_forms'+(f'{k+1}' if len(frames)>1 else ''));T+=1
    tmp=R+'/build/cast_sheet';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp);os.makedirs(x.out,exist_ok=True)
    json.dump(shots,open(tmp+'/shots.json','w'),ensure_ascii=False)
    json.dump([{'beat':1,'audio':T+1,'duration':T+1,'words':[{'text':'.','start':0,'end':.1}]}],open(tmp+'/timings.json','w'))
    html=B.build(1.5);env=dict(os.environ,ENGINE=html,VW='1920',VH='1080')
    if 'NODE_PATH' not in env:env['NODE_PATH']=subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()
    ts=[f'{i+.5:.1f}' for i in range(T)]
    r=subprocess.run(['node',R+'/studio/still.js',tmp+'/shots.json',tmp+'/timings.json',tmp]+ts,env=env,cwd=R,capture_output=True,text=True)
    if r.returncode:sys.exit(r.stdout+r.stderr)
    for l in r.stdout.splitlines():
        if l.startswith('FX_ERRORS') and l.strip()!='FX_ERRORS []':print(l)
        if 'PAGEERR' in l or 'CONSOLE' in l:print(l)
    for i,t in enumerate(ts):
        f=f"{tmp}/t{t.rjust(5,'0')}.png";dst=f"{x.out}/{outs[i]}.jpg"
        Image.open(f).convert('RGB').save(dst,quality=88);print(dst)
main()
