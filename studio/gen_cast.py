"""Generate full-body rig-friendly source art for every cast member with Gemini, cut out the backdrop. usage: gen_cast.py [id ...]  (default: all missing)"""
import os,sys,json,base64,subprocess,time,concurrent.futures as cf
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/'
M=json.load(open(P+'cast.json'))
ids=sys.argv[1:] or [k for k in M['characters'] if not os.path.exists(f'{P}{k}/source.png')]
def gen(k):
    os.makedirs(P+k,exist_ok=True);prompt=M['characters'][k]+' '+(M['animal_prompt'] if k in M.get('animal_ids',[]) else M['standard_prompt'])
    for attempt in range(3):
        r=subprocess.run(['curl','-sS','-m','170','-X','POST','https://generativelanguage.googleapis.com/v1beta/openai/images/generations','-H','Content-Type: application/json','-d',json.dumps({'model':'gemini-2.5-flash-image','prompt':prompt,'n':1,'response_format':'b64_json'})],capture_output=True,text=True)
        try:d=json.loads(r.stdout)
        except Exception:time.sleep(3);continue
        if isinstance(d,list):d=d[0]
        if 'data' in d:open(f'{P}{k}/source.png','wb').write(base64.b64decode(d['data'][0]['b64_json']));return k,'ok'
        time.sleep(4)
    return k,'FAILED'
with cf.ThreadPoolExecutor(4) as ex:
    for k,s in ex.map(gen,ids):print(k,s,flush=True)
sys.path.insert(0,R+'/studio');import keyout
for k in ids:
    if os.path.exists(f'{P}{k}/source.png'):
        try:keyout.key(f'{P}{k}/source.png',f'{P}{k}/full.png')
        except Exception as e:print('keyout failed',k,e)
