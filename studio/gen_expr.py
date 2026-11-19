"""Expression sheets: for every humanoid character Gemini draws ONE image with six heads of the same character (neutral, smile, angry, sad, shocked, eyes closed);
we cut them into library/puppets/<id>/heads/<expr>.png (left to right order). usage: gen_expr.py [id ...]"""
import os,sys,json,base64,subprocess,time,numpy as np,concurrent.futures as cf
from PIL import Image
from scipy import ndimage as ndi
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/'
sys.path.insert(0,R+'/studio');import keyout
M=json.load(open(P+'cast.json'));animals=set(M.get('animal_ids',[]))
EXPR=['neutral','smile','angry','sad','shocked','closed']
ids=sys.argv[1:] or [k for k in M['characters'] if k not in animals and os.path.exists(f'{P}{k}/full.png') and not os.path.exists(f'{P}{k}/heads/closed.png')]
TEMPLATE=("Character expression sheet. {desc} Draw ONLY the HEAD and neck of this exact same character SIX times in ONE horizontal row, evenly spaced with wide empty gaps, all at exactly the same scale and angle, front view, same hair, crown, jewellery and skin tone in every head. The six expressions left to right: 1 neutral calm, 2 gentle smile, 3 angry (heavy lowered brows, plain tight frown, NO fangs, NO face lines), 4 sad (raised inner brows, downturned mouth, watery eyes), 5 shocked (wide eyes, small open mouth), 6 eyes closed serene. "
 "SIMPLE GEOMETRIC FLAT-VECTOR style: flat solid colours with ONE darker shade tone, thin warm cream outline, minimal detail, no painterly texture. On ONE solid flat pure green (#00FF00) background, no border, no text, no labels.")
def gen(k):
    os.makedirs(P+k+'/heads',exist_ok=True)
    for _ in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':TEMPLATE.format(desc=M['characters'][k]),'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:open(f'{P}{k}/heads/sheet.png','wb').write(base64.b64decode(d['data'][0]['b64_json']));return k,'ok'
        time.sleep(4)
    return k,'FAILED'
def cut(k):
    p=f'{P}{k}/heads/sheet.png'
    if not os.path.exists(p):return
    tmp=f'{P}{k}/heads/_keyed.png'
    try:keyout.key(p,tmp,pad=0)
    except Exception as e:print('key failed',k,e);return
    im=Image.open(tmp).convert('RGBA');a=np.asarray(im)[...,3]>40;lab,n=ndi.label(ndi.binary_dilation(a,iterations=6))
    if n<6:print('only',n,'heads for',k);return
    sizes=ndi.sum(a,lab,index=np.arange(1,n+1));top=np.argsort(sizes)[::-1][:6]+1
    boxes=sorted([(ndi.find_objects(lab==t)[0],t) for t in top],key=lambda b:b[0][1].start)
    for (sl,t),name in zip(boxes,EXPR):
        piece=np.asarray(im).copy();piece[~(lab==t)]=0;Image.fromarray(piece,'RGBA').crop((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)).save(f'{P}{k}/heads/{name}.png')
    os.remove(tmp)
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,ids):print(k,s,flush=True)
for k in ids:cut(k)
