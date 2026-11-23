"""Re-time shot_plan at.t from one timings.json to another for the same script (same words, one to one).
usage: python3 studio/remap_plan2.py 06 build/ep06/timings.est.json   (new = build/ep06/timings.json; backup shot_plan.est.json must exist or is made)"""
import sys,os,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));ep=sys.argv[1]
def absw(p):
    t=json.load(open(p));off=0;out=[]
    for b in t:out.append({'start':off,'end':off+b['duration'],'words':[(w['text'],off+w['start']) for w in b['words']]});off+=b['duration']
    return out
old=absw(sys.argv[2]);new=absw(f'{R}/build/ep{ep}/timings.json')
pp=f'{R}/episodes/ep{ep}/shot_plan.json';plan=json.load(open(pp));S=plan['shots'] if isinstance(plan,dict) else plan;bad=0
for s in S:
    a=s['at']
    if not(isinstance(a,dict) and 't' in a):continue
    t=a['t'];bi=next((i for i,b in enumerate(old) if b['start']-.05<=t<b['end']+.05),len(old)-1);ow=old[bi]['words'];nw=new[bi]['words']
    if len(ow)!=len(nw):bad+=1;nt=new[bi]['start']+(t-old[bi]['start'])/(old[bi]['end']-old[bi]['start'])*(new[bi]['end']-new[bi]['start'])
    else:i=min(range(len(ow)),key=lambda k:abs(ow[k][1]-t));nt=nw[i][1]
    a['t']=round(nt,2)
json.dump(plan,open(pp,'w'),ensure_ascii=False,indent=1);print('remapped',len(S),'shots; fallbacks',bad)
