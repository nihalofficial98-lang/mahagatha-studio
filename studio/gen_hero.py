"""Hero heads for 4K close-ups: ONE character per Gemini image, six heads in a 3x2 grid (each ~340 px) -> library/puppets/<id>/heads_hero/<expr>.png"""
import os,sys,json,base64,subprocess,time,numpy as np,concurrent.futures as cf
from PIL import Image
from scipy import ndimage as ndi
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/'
sys.path.insert(0,R+'/studio');import keyout
M=json.load(open(P+'cast.json'));EXPR=['neutral','smile','angry','sad','shocked','closed']
LEADS=['shiva','vishnu','brahma','narada','daksha','adishakti','madhu','kaitabha','sati','indra','krishna','rama','parvati','ganesha','durga']
animals=set(M.get('animal_ids',[]))
if sys.argv[1:]==['ALL']:ids=['shiva']+[k for k in M['characters'] if k not in animals and k not in ('brahma',) or k=='brahma' ]
else:ids=[k for k in (sys.argv[1:] or LEADS) if k in M['characters'] or k=='shiva']
ids=[k for k in ids if not os.path.exists(f'{P}{k}/heads_hero/neutral.png')]
DESC={**M['characters'],'shiva':"Lord Shiva: ash-blue skin, black coiled jata bun with ONLY a small white crescent moon, long black locks beside the face, vertical red third eye, three white ash lines, gold ear rings, rudraksha mala, a green serpent on the neck."}
T=("Hero expression sheet. {d} Draw ONLY the HEAD and neck of this one character SIX times in a 3 columns by 2 rows grid, each head as LARGE as possible so the grid fills the whole image edge to edge with only SMALL gaps (about 3% of the width) and no blank margins, all at exactly the same scale and angle, front view, same hair, crown, jewellery and skin tone. "
 "Row 1 left to right: neutral calm, gentle smile, angry (heavy lowered brows, plain tight frown, NO fangs, NO face lines). Row 2 left to right: sad (raised inner brows, downturned mouth, watery eyes), shocked (wide eyes, small open mouth), eyes closed serene. "
 "SIMPLE GEOMETRIC FLAT-VECTOR style: flat solid colours with ONE darker shade tone, thin warm cream outline, minimal detail, no painterly texture. ONE solid flat pure green (#00FF00) background, no border, no text.")
def gen(k):
    os.makedirs(P+k+'/heads_hero',exist_ok=True)
    for _ in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':T.format(d=DESC[k]),'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:open(f'{P}{k}/heads_hero/sheet.png','wb').write(base64.b64decode(d['data'][0]['b64_json']));return k,'ok'
        time.sleep(4)
    return k,'FAILED'
def cut(k):
    p=f'{P}{k}/heads_hero/sheet.png'
    if not os.path.exists(p):return
    tmp='/tmp/_hero_keyed.png';keyout.key(p,tmp,pad=0)
    im=Image.open(tmp).convert('RGBA');a=np.asarray(im)[...,3]>40;lab,n=ndi.label(ndi.binary_dilation(a,iterations=6))
    if n<6:print('only',n,'heads for',k);return
    sizes=ndi.sum(a,lab,index=np.arange(1,n+1));top=np.argsort(sizes)[::-1][:6]+1;objs=ndi.find_objects(lab);b=[(objs[t-1],t) for t in top]
    b.sort(key=lambda x:(x[0][0].start+x[0][0].stop)/2);rows=[sorted(b[:3],key=lambda x:x[0][1].start),sorted(b[3:],key=lambda x:x[0][1].start)]
    for (sl,t),name in zip(rows[0]+rows[1],EXPR):
        piece=np.asarray(im).copy();piece[~(lab==t)]=0;Image.fromarray(piece,'RGBA').crop((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)).save(f'{P}{k}/heads_hero/{name}.png')
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,ids):print(k,s,flush=True)
for k in ids:
    try:cut(k)
    except Exception as e:print('cut failed',k,e)
