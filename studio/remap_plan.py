"""Re-time a shot plan written against a provisional voice_timeline.md onto the real voice (build/epNN/timings.json).
Both come from the same script, so the words match one to one inside every beat: each shot's at.t is moved to the new time of the SAME word.
usage: python3 studio/remap_plan.py 06   (rewrites episodes/ep06/shot_plan.json in place; backup shot_plan.provisional.json)"""
import sys,os,re,json,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ep_frames_lib import parse_timeline_raw
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));ep=sys.argv[1]
old=parse_timeline_raw(f'{R}/episodes/ep{ep}/voice_timeline.md')   # [{beat,start,end,words:[(w,abs_t)]}]
new=json.load(open(f'{R}/build/ep{ep}/timings.json'));off=0;newb={}
for i,t in enumerate(new):newb[i+1]={'start':off,'words':[(w['text'],off+w['start']) for w in t['words']]};off+=t['duration']
pp=f'{R}/episodes/ep{ep}/shot_plan.json';plan=json.load(open(pp));S=plan['shots'] if isinstance(plan,dict) else plan
if not os.path.exists(pp.replace('.json','.provisional.json')):shutil.copy(pp,pp.replace('.json','.provisional.json'))
bad=0
for s in S:
    a=s['at']
    if not(isinstance(a,dict) and 't' in a):continue
    t=a['t'];ob=next((b for b in old if b['start']-.05<=t<b['end']+.05),old[-1]);ow=ob['words'];nw=newb[ob['beat']]['words']
    i=min(range(len(ow)),key=lambda k:abs(ow[k][1]-t))
    if len(ow)!=len(nw) or ow[i][0].strip('।,.?!"“”')!=nw[i][0].strip('।,.?!"“”'):
        # words differ in count: fall back on proportional position inside the beat
        bad+=1;fr=(t-ob['start'])/max(.01,ob['end']-ob['start']);nt=newb[ob['beat']]['start']+fr*(new[ob['beat']-1]['duration'])
    else:nt=nw[i][1]
    a['t']=round(nt,2)
json.dump(plan,open(pp,'w'),ensure_ascii=False,indent=1);print('remapped',len(S),'shots; proportional fallbacks:',bad)
