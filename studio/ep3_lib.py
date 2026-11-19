"""Build EP3 frame sheets from Gemini library cut-outs (planted, breathing) + painted backgrounds + library effect images.
Reads episodes/ep03/shots.json -> episodes/ep03/shots_lib.json, renders stills, numbered sheets."""
import json,os,sys,glob,subprocess,shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A='../library/pilot/assets/'
sh=json.load(open(ROOT+'/episodes/ep03/shots.json',encoding='utf-8'))
LIB={'brahma':'brahma','vishnu':'vishnu','vishnu_rest':'vishnu','adishakti':'adishakti','manu':'manu','narada':'narada','daksha':'daksha','brahmi':'brahmi',
 'rishi0':'rishi_vasishtha','rishi1':'rishi_marichi','rishi2':'rishi_atri','rishi3':'rishi_angirasa','rishi4':'rishi_kratu','rishi5':'rishi_pulaha','rishi6':'rishi_pulastya'}
HP={'daksha':1.0,'brahma':1.0,'vishnu':1.05}
BGM={'yagna':'bg_yagna2.png','kailash':'bg_kailash2.png'}
ICON={'vortex':('energy_swirl',130,{'spin':1.2}),'cycle':('fire_ring',120,{'spin':.8}),'light':('divine_rays',140,{}),'trident':('trident_plain',70,{}),'flame':('fire_small',90,{}),'frost':('snow_flakes',130,{}),'lotusI':('lotus_pond_leaf',110,{})}
def fig(g,beat,i):
    w=g['who']
    if w=='shiva':
        rage=beat in(5,6,7) or (g.get('expr') or {}).get('brow',0)<-.6
        d={'who':'shiva_p','x':g['x'],'y':g['y']+170,'s':1.0,'hpx':600*g.get('s',1)/1.0*.8}
        if rage:d['ka']=[1,1,0,.1]
        else:d['eyes']='open'
    elif w in LIB:
        d={'who':'img','src':A+'lib_'+LIB[w]+'.png','x':g['x'],'y':g['y']+170,'s':1.0,'hpx':560*g.get('s',1)*HP.get(w,.95)}
    else:return g
    if g.get('head') and d['who']=='shiva_p':d['hpx']=900;d['y']=1000
    elif g.get('head'):d['hpx']=max(d['hpx'],1250);d['y']=90+d['hpx']
    elif d['hpx']>640:d['hpx']=640
    if 'flip' in g:d['flip']=g['flip']
    if d['who']=='shiva_p' and not g.get('head'):d['hpx']=min(d['hpx'],700)
    return d
out=[]
for i,s in enumerate(sh):
    s=json.loads(json.dumps(s));sc=s.get('sc')
    if sc:
        b=sc.get('bg')
        if isinstance(b,dict) and b.get('k') in BGM:sc['bg']={'k':'img','src':A+BGM[b['k']],'fy':.5,'z0':1.08,'zv':.004}
        sc['figs']=[fig(g,s['beat'],i) for g in sc.get('figs',[])]
        nf=[]
        for x in sc.get('fx',[]):
            t=x.get('t')
            if t=='icon' and x['i'] in ICON:
                n,w,k=ICON[x['i']];e={'t':'fximg','src':A+'fx_'+n+'.png','x':x['x'],'y':x['y'],'w':w*x.get('sc',1),'blend':'lighter','c':x.get('c',0),'d':x.get('d',1)};e.update(k);nf.append(e)
            elif t=='flames':nf.append({'t':'fximg','src':A+'fx_fire_tall.png','x':x['x'],'y':x['y'],'w':280*x.get('sc',1),'blend':'lighter','c':x.get('c',0),'d':x.get('d',2)})
            elif t=='pillar':nf.append({'t':'fximg','src':A+'fx_light_beam.png','x':x['x'],'y':(x['y0']+x['y1'])/2,'w':max(260,x.get('w',200)*2),'blend':'lighter','alpha':.8,'c':x.get('c',0),'d':x.get('d',2)})
            else:nf.append(x)
        sc['fx']=nf
    out.append(s)
json.dump(out,open(ROOT+'/episodes/ep03/shots_lib.json','w',encoding='utf-8'),ensure_ascii=False)
sys.path.insert(0,ROOT+'/studio');import build as B;html=B.build(1.5)
ts=sorted(float(os.path.basename(f)[1:-4]) for f in glob.glob(ROOT+'/build/ep03/stills/t*.png'))
d=ROOT+'/build/ep03/stills_lib';shutil.rmtree(d,ignore_errors=True)
env=dict(os.environ,ENGINE=html)
subprocess.check_call(['node','studio/still.js',ROOT+'/episodes/ep03/shots_lib.json',ROOT+'/build/ep03/engine_timings.json',d]+[str(t) for t in ts],env=env,cwd=ROOT)
from PIL import Image,ImageDraw
fs=sorted(glob.glob(d+'/t*.png'),key=lambda f:float(os.path.basename(f)[1:-4]));o=ROOT+'/build/ep03/sheets_lib';shutil.rmtree(o,ignore_errors=True);os.makedirs(o)
for n in range(0,len(fs),12):
    im=Image.new('RGB',(1920,1080))
    for k,f in enumerate(fs[n:n+12]):
        x=Image.open(f).convert('RGB').resize((640,360));ImageDraw.Draw(x).text((8,8),str(n+k),fill=(255,255,0));im.paste(x,((k%3)*640,(k//3)*360))
    im.save(f'{o}/sheet_{n//12}.jpg',quality=84)
print(len(fs),'frames',o)
