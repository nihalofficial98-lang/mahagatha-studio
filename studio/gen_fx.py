"""Generate the effects/elements library with Gemini. Additive effects are made on black and converted to alpha (blend with 'lighter');
solid elements are made on green and cut out. usage: gen_fx.py [id ...]"""
import os,sys,json,base64,subprocess,time,numpy as np,concurrent.futures as cf
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));F=R+'/library/fx/'
sys.path.insert(0,R+'/studio');import keyout
E=json.load(open(F+'effects.json'));STY=E['style']
jobs={}
for k,v in E['additive'].items():
    if not k.startswith('_'):jobs[k]=('add',v+' On a pure BLACK background (#000000), nothing else, centred, with a margin. '+STY)
for k,v in E['solid'].items():
    if not k.startswith('_'):jobs[k]=('solid',v+' Single object or element, centred, full view with a margin, on ONE solid flat pure chroma-key green (#00FF00) background with no shadow and no floor. '+STY)
ids=sys.argv[1:] or [k for k in jobs if not os.path.exists(F+k+'.png')]
os.makedirs(F+'raw',exist_ok=True)
def gen(k):
    kind,prompt=jobs[k]
    for _ in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':prompt,'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:open(F+'raw/'+k+'.png','wb').write(base64.b64decode(d['data'][0]['b64_json']));return k,'ok'
        time.sleep(4)
    return k,'FAILED'
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,ids):print(k,s,flush=True)
for k in ids:
    p=F+'raw/'+k+'.png'
    if not os.path.exists(p):continue
    kind=jobs[k][0]
    try:
        if kind=='solid':keyout.key(p,F+k+'.png')
        else:
            a=np.asarray(Image.open(p).convert('RGB')).astype(np.float32);lum=a.max(axis=2)/255.0
            alpha=np.clip((lum-.06)/.5,0,1);rgb=np.where(alpha[...,None]>0,np.clip(a/np.maximum(alpha[...,None],.15),0,255),0)
            out=np.dstack([rgb,alpha*255]).astype(np.uint8);im=Image.fromarray(out,'RGBA');bb=im.getbbox();(im.crop(bb) if bb else im).save(F+k+'.png')
    except Exception as e:print('cut failed',k,e)
