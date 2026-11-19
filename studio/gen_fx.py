"""Effects/elements library, BATCHED: several compact items per Gemini image (grid on one background), cut apart by connected components.
Scatter-type effects are generated one per image. Additive items: black bg -> luminance alpha (blend with 'lighter'); solid items: green bg -> cutout. usage: gen_fx.py [id ...]"""
import os,sys,json,base64,subprocess,time,numpy as np,concurrent.futures as cf
from PIL import Image
from scipy import ndimage as ndi
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));F=R+'/library/fx/'
sys.path.insert(0,R+'/studio');import keyout
E=json.load(open(F+'effects.json'));STY=E['style']
SCATTER={'embers','sparkles_gold','rain_streaks','snow_flakes','star_field','mist_wisps','divine_rays','wind_swirls_vayu','flower_petals','stars_gold_big','bubbles','smoke_plume','energy_swirl'}
items={}
for k,v in E['additive'].items():
    if not k.startswith('_'):items[k]=('add',v)
for k,v in E['solid'].items():
    if not k.startswith('_'):items[k]=('solid',v)
ids=sys.argv[1:] or [k for k in items if not os.path.exists(F+k+'.png')]
single=[k for k in ids if k in SCATTER];batchable=[k for k in ids if k not in SCATTER]
groups=[]
for kind in ('add','solid'):
    ks=[k for k in batchable if items[k][0]==kind];n=4 if kind=='add' else 6
    groups+=[(kind,ks[i:i+n]) for i in range(0,len(ks),n)]
groups+=[(items[k][0],[k]) for k in single]
os.makedirs(F+'raw',exist_ok=True)
def call(prompt,out):
    for _ in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':prompt,'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:open(out,'wb').write(base64.b64decode(d['data'][0]['b64_json']));return True
        time.sleep(4)
    return False
def make(g):
    kind,ks=g;tag='__'.join(ks)[:80];out=F+'raw/'+tag+'.png'
    bgtxt='pure BLACK background (#000000)' if kind=='add' else 'ONE solid flat pure chroma-key green (#00FF00) background with no shadow and no floor'
    if len(ks)==1:p=items[ks[0]][1]+f' Single item, centred, with a margin, on a {bgtxt}. '+STY
    else:
        lst=' '.join(f'({i+1}) {items[k][1]}' for i,k in enumerate(ks))
        p=f'A sheet of {len(ks)} SEPARATE items, laid out in a neat grid (2 or 3 per row, row by row, left to right), each item as LARGE as possible so the items fill the whole image edge to edge, with only SMALL gaps between items (about 3% of the width), none overlapping, all fully visible, no empty margins or blank space, on a {bgtxt}. Items in order: {lst} '+STY
    return g,out,call(p,out)
def cut_one(kind,k,im,path):
    if kind=='solid':im.save('/tmp/_k.png');keyout.key('/tmp/_k.png',path)
    else:
        a=np.asarray(im.convert('RGB')).astype(np.float32);lum=a.max(axis=2)/255.0;alpha=np.clip((lum-.06)/.5,0,1)
        rgb=np.where(alpha[...,None]>0,np.clip(a/np.maximum(alpha[...,None],.15),0,255),0);o=Image.fromarray(np.dstack([rgb,alpha*255]).astype(np.uint8),'RGBA');bb=o.getbbox();(o.crop(bb) if bb else o).save(path)
def split(kind,ks,out):
    im=Image.open(out).convert('RGB')
    if len(ks)==1:cut_one(kind,ks[0],im,F+ks[0]+'.png');return
    arr=np.asarray(im).astype(np.int16)
    if kind=='solid':bgm=(arr[...,1]>arr[...,0]+25)&(arr[...,1]>arr[...,2]+25)
    else:bgm=arr.max(axis=2)<22
    fg=~bgm;lab,n=ndi.label(ndi.binary_dilation(fg,iterations=14))
    sizes=ndi.sum(fg,lab,index=np.arange(1,n+1));top=list(np.argsort(sizes)[::-1][:len(ks)]+1)
    if len(top)<len(ks):print('only',len(top),'items found in',ks);return
    objs=ndi.find_objects(lab);bx=[(objs[t-1],t) for t in top]
    H=im.height;rowH=H/ (2 if len(ks)<=6 else 3)
    bx.sort(key=lambda b:(int(((b[0][0].start+b[0][0].stop)/2)//(H/2.4)),b[0][1].start))
    for (sl,t),k in zip(bx,ks):
        m=(lab==t);m=ndi.binary_dilation(m,iterations=10);crop=np.asarray(im).copy();crop[~m]=(0,0,0) if kind=='add' else (0,255,0)
        sub=Image.fromarray(crop).crop((max(0,sl[1].start-12),max(0,sl[0].start-12),sl[1].stop+12,sl[0].stop+12));cut_one(kind,k,sub,F+k+'.png')
with cf.ThreadPoolExecutor(3) as ex:
    res=list(ex.map(make,groups))
for g,out,ok in res:
    print(g[1],'ok' if ok else 'FAILED',flush=True)
    if ok:
        try:split(g[0],g[1],out)
        except Exception as e:print('cut failed',g[1],e)
