"""Expression sheets: for every humanoid character Gemini draws ONE image with six heads of the same character (neutral, smile, angry, sad, shocked, eyes closed);
we cut them into library/puppets/<id>/heads/<expr>.png (left to right order). usage: gen_expr.py [id ...]"""
import os,sys,json,base64,subprocess,time,numpy as np,concurrent.futures as cf
from PIL import Image
from scipy import ndimage as ndi
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/'
sys.path.insert(0,R+'/studio');import keyout
M=json.load(open(P+'cast.json'));animals=set(M.get('animal_ids',[]))
PAIR=True
EXPR=['neutral','smile','angry','sad','shocked','closed']
ids=sys.argv[1:] or [k for k in M['characters'] if k not in animals and os.path.exists(f'{P}{k}/full.png') and not os.path.exists(f'{P}{k}/heads/closed.png')]
TEMPLATE=("Character expression sheet with TWO characters. Draw ONLY the HEAD and neck of each character SIX times in a horizontal row, TWO rows: the TOP row is character A, the BOTTOM row is character B. Every head in a row is the exact same character, same hair, crown, jewellery and skin tone, same scale and angle, front view, evenly spaced with wide empty gaps. The six expressions left to right: 1 neutral calm, 2 gentle smile, 3 angry (heavy lowered brows, plain tight frown, NO fangs, NO face lines), 4 sad (raised inner brows, downturned mouth, watery eyes), 5 shocked (wide eyes, small open mouth), 6 eyes closed serene. "
 "SIMPLE GEOMETRIC FLAT-VECTOR style: flat solid colours with ONE darker shade tone, thin warm cream outline, minimal detail, no painterly texture. On ONE solid flat pure green (#00FF00) background, no border, no text, no labels. CHARACTER A: {a} CHARACTER B: {b}")
def gen(pair):
    ka,kb=pair[0],(pair[1] if len(pair)>1 else pair[0]);tag=ka
    for k in pair:os.makedirs(P+k+'/heads',exist_ok=True)
    for _ in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':TEMPLATE.format(a=M['characters'][ka],b=M['characters'][kb]),'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:
            raw=base64.b64decode(d['data'][0]['b64_json'])
            for k in pair:open(f'{P}{k}/heads/sheet.png','wb').write(raw)
            return pair,'ok'
        time.sleep(4)
    return pair,'FAILED'
def cut(pair):
    p=f'{P}{pair[0]}/heads/sheet.png'
    if not os.path.exists(p):return
    tmp='/tmp/_expr_keyed.png'
    try:keyout.key(p,tmp,pad=0)
    except Exception as e:print('key failed',pair,e);return
    im=Image.open(tmp).convert('RGBA');a=np.asarray(im)[...,3]>40;lab,n=ndi.label(ndi.binary_dilation(a,iterations=6))
    need=6*len(pair)
    if n<need:print('only',n,'heads for',pair);return
    sizes=ndi.sum(a,lab,index=np.arange(1,n+1));top=np.argsort(sizes)[::-1][:need]+1
    objs=ndi.find_objects(lab);boxes=[(objs[t-1],t) for t in top];boxes.sort(key=lambda b:(b[0][0].start+b[0][0].stop)/2)
    rows=[sorted(boxes[i*6:(i+1)*6],key=lambda b:b[0][1].start) for i in range(len(pair))]
    for k,row in zip(pair,rows):
        for (sl,t),name in zip(row,EXPR):
            piece=np.asarray(im).copy();piece[~(lab==t)]=0;Image.fromarray(piece,'RGBA').crop((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)).save(f'{P}{k}/heads/{name}.png')
pairs=[ids[i:i+2] for i in range(0,len(ids),2)]
with cf.ThreadPoolExecutor(3) as ex:
    for pr,st in ex.map(gen,pairs):print(pr,st,flush=True)
for pr in pairs:cut(pr)
