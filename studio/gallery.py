"""Reference gallery: renders every character, pose, expression and background with the CURRENT engine into
library/gallery/v<VERSION>/ so improvements over time are visible side by side (open two version folders)."""
import json,os,re,subprocess,sys,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,ROOT+'/studio')
from PIL import Image,ImageDraw
import build as B
ver=open(ROOT+'/engine/VERSION').read().strip();out=f'{ROOT}/library/gallery/v{ver}';os.makedirs(out,exist_ok=True);tmp=ROOT+'/build/_gallery';os.makedirs(tmp,exist_ok=True)
art=open(ROOT+'/engine/art.js').read();scn=open(ROOT+'/engine/scenes.js').read()
CHARS=['kumara0','rudra','shiva','vishnu','narada','agni','kamadeva','daksha','vishwakarma','rishi0','rishi3','rudra4']
BGS=re.findall(r"^ (\w+)\(S,t\)\{",scn,re.M)
POSES=['stand','namaste','raiseR','open','cross','fist','hold','point','bow','cup','tri']
shots=[];names=[]
def add(name,sc):shots.append({"beat":1,"at":len(shots)*2.0,"draw":"scene","cam":{"from":{"z":1,"x":0,"y":0,"r":0},"to":{"z":1,"x":0,"y":0,"r":0}},"grade":"rgba(0,0,0,0)","sc":sc,"dx":0.01});names.append(name)
for c in CHARS: add('char_'+c,{'bg':{'k':'cel','warm':True},'figs':[{'who':c,'x':640,'y':690,'s':1.9,'pose':'stand'}]})
add('char_brahma',{'bg':{'k':'cel','warm':True},'figs':[{'who':'brahma','x':640,'y':690,'s':1.7}]})
add('char_bull',{'bg':{'k':'cel','warm':True},'figs':[{'who':'bull','x':640,'y':700,'s':1.9}]})
for i in range(0,len(POSES),4): add('poses_%d'%i,{'bg':{'k':'cel'},'figs':[{'who':'vishnu','x':200+j*280,'y':680,'s':1.15,'pose':p,'tail':False} for j,p in enumerate(POSES[i:i+4])]})
add('expr_brahma',{'bg':{'k':'cel'},'figs':[{'who':'brahma','head':False,'x':180+j*300,'y':520,'s':0.7,'expr':e} for j,e in enumerate([{'brow':-1,'mouth':-1},{'brow':0.9,'mouth':-0.5},{'eye':0.2,'mouth':0.9},{'eye':1.3,'open':0.4,'brow':0.8}])]})
for b in BGS:
    if b!='palace' or True: add('bg_'+b,{'bg':{'k':b},'figs':[]})
json.dump(shots,open(tmp+'/shots.json','w'));N=len(shots)*2.0
json.dump([{'beat':1,'audio':N,'duration':N,'words':[]}],open(tmp+'/engine_timings.json','w'))
html=B.build(1.5,ROOT+'/engine/_built_gallery.html')
subprocess.run(['node',ROOT+'/studio/still.js',tmp+'/shots.json',tmp+'/engine_timings.json',tmp]+[str(i*2.0+1.0) for i in range(len(shots))],env=dict(os.environ,ENGINE=html),check=True)
fs=sorted(glob.glob(tmp+'/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]))
for f,n in zip(fs,names): Image.open(f).convert('RGB').save(f'{out}/{n}.jpg',quality=85)
print(len(names),'reference images ->',out)
from PIL import Image,ImageDraw
im=Image.new('RGB',(1920,270*((len(names)+3)//4)))
for i,n in enumerate(names):
    x=Image.open(f'{out}/{n}.jpg').convert('RGB').resize((480,270));ImageDraw.Draw(x).text((6,6),n,fill=(255,255,0));im.paste(x,((i%4)*480,(i//4)*270))
im.save(f'{out}/_index.jpg',quality=80)
