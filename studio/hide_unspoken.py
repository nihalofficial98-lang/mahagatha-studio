"""After import_timestamps: script words the narrator did NOT say get hide:true (cues still work, subtitles skip them);
sentences the narrator DID say that the script lacks are APPENDED (after the script words; the engine sorts by time). Danda stripped from word text (no-op for English).
usage: python3 studio/hide_unspoken.py 06 <timestamps.json>"""
import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import import_timestamps as T
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));ep,tsf=sys.argv[1:3]
B=json.load(open(f'{R}/build/ep{ep}/beats.json',encoding='utf-8'))['scenes'];asr=T.parse(tsf)
W=[(bi,w) for bi,sc in enumerate(B) for seg in sc['narration'] for w in seg['t'].split()];p=T.match([w for _,w in W],asr);used=set(p.values())
TM=json.load(open(f'{R}/build/ep{ep}/timings.json'));pos=[(bi,k) for bi,b in enumerate(TM) for k in range(len(b['words']))]
assert len(pos)==len(W),(len(pos),len(W))
starts=[];off=0
for b in TM:starts.append(off);off+=b['duration']
runs=[];j=0                                   # ASR-only runs = spoken but not in the script
while j<len(asr):
    if j in used:j+=1;continue
    k=j
    while k<len(asr) and k not in used:k+=1
    if k-j>=3 and asr[k-1][2]-asr[j][1]>.8:runs.append((j,k))
    j=k
spans=[(asr[a][1]-.3,asr[b-1][2]+.3) for a,b in runs];hid=[];i=0
while i<len(W):
    if i in p:i+=1;continue
    j=i
    while j<len(W) and j not in p:j+=1
    for k in range(i,j):
        bi,wk=pos[k];t=starts[bi]+TM[bi]['words'][wk]['start']
        if j-i>=4 or any(a<=t<=z for a,z in spans):TM[bi]['words'][wk]['hide']=1
    hid.append(' '.join(w for _,w in W[i:j]));i=j
added=[]
for a,b in runs:
    for q in range(a,b):
        t=asr[q][1];bi=max(x for x in range(len(TM)) if starts[x]<=t+.001);TM[bi]['words'].append({'text':asr[q][0],'start':round(t-starts[bi],3),'end':round(asr[q][2]-starts[bi],3),'extra':1})
    added.append(' '.join(x[0] for x in asr[a:b]))
for b in TM:
    for w in b['words']:w['text']=w['text'].replace('।','') or w['text']
json.dump(TM,open(f'{R}/build/ep{ep}/timings.json','w'),ensure_ascii=False)
print('script words not spoken (hidden):',sum(1 for b in TM for w in b['words'] if w.get('hide')),'| extra spoken sentences added:',len(added))
