"""Reference sheet of the CODED cast (full body + head close-ups) -> build/ref_coded/sheet_N.jpg"""
import os,sys,json,glob,shutil,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,ROOT+'/studio');sys.path.insert(0,ROOT+'/episodes/ep03')
from shotkit import *
B=lambda:bg('cosmos',rgb='110,110,150',spin=0)
T=[('Shiva - calm',[F('shiva',640,670,1.15)]),
 ('Shiva - rage',[F('shiva',640,670,1.15,pose='rage',expr={'brow':-.95},aura='255,70,40')]),
 ('Shiva - face calm / angry',[F('shiva',330,470,2.1,head=True,expr={'eye':.2}),F('shiva',950,470,2.1,head=True,expr={'brow':-.95})]),
 ('Vishnu - full',[F('vishnu',640,670,1.15)]),('Vishnu - face',[F('vishnu',640,470,2.0,head=True)]),
 ('Brahma - full',[F('brahma',640,650,2.2)]),('Brahma - face',[F('brahma',640,470,2.0,head=True)]),
 ('Daksha - full + face',[F('daksha',330,670,1.15),F('daksha',950,470,2.4,head=True)]),
 ('Rishis 0-3',[F('rishi0',220,650,1.0),F('rishi1',520,650,1.0),F('rishi2',820,650,1.0),F('rishi3',1080,650,1.0)]),
 ('Rishis 4-6 + Narada',[F('rishi4',220,650,1.0),F('rishi5',520,650,1.0),F('rishi6',820,650,1.0),F('narada',1080,650,1.0)]),
 ('Adishakti, Manu, Brahmi',[F('adishakti',250,650,1.05),F('manu',640,650,1.05),F('brahmi',1030,650,1.05)]),
 ('Harihara',[F('harihara',640,670,1.1)]),('Ardhanarishvara',[F('ardha',640,670,1.1)]),('Vishnu on Shesha',[F('vishnu_rest',640,560,1.2)])]
film=Film();t=1.0
for n,f in T:film.add(1,t,{'bg':B(),'figs':f,'fx':[]},'cel');t+=3.2
p=ROOT+'/build/ref_coded';shutil.rmtree(p,ignore_errors=True);os.makedirs(p)
film.save(p+'/shots.json')
import build as BD;html=BD.build(1.5).replace('function subs(c2,T){','function subs(c2,T){return;',1)
ts=[round(1.0+3.2*i+.6,2) for i in range(len(T))]
subprocess.check_call(['node','studio/still.js',p+'/shots.json',ROOT+'/build/ep92/engine_timings.json',p+'/st']+[str(x) for x in ts],env=dict(os.environ,ENGINE=html),cwd=ROOT)
from PIL import Image,ImageDraw,ImageFont
fs=sorted(glob.glob(p+'/st/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]))
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
for n in range(0,len(fs),6):
    im=Image.new('RGB',(1920,1080))
    for k,f in enumerate(fs[n:n+6]):
        x=Image.open(f).convert('RGB').resize((640,360));d=ImageDraw.Draw(x);d.rectangle((0,0,640,40),fill=(0,0,0));d.text((10,4),f'{n+k+1}. {T[n+k][0]}',font=fnt,fill=(255,230,150));im.paste(x,((k%3)*640,(k//3)*360))
    im.save(f'{p}/sheet_{n//6}.jpg',quality=88)
print(len(fs))
