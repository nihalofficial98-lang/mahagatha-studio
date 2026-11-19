"""Director's toolkit used by episodes/epNN/shots.py. Every shot = (beat, spoken-word trigger, scene, grade, camera)."""
import json,itertools,os
GRADES={'cel':'rgba(190,200,255,0.14)','warm':'rgba(255,190,120,0.16)','red':'rgba(255,60,30,0.20)','night':'rgba(60,90,170,0.20)','pal':'rgba(255,170,90,0.14)','cool':'rgba(80,160,200,0.16)','dark':'rgba(20,10,40,0.22)','amb':'rgba(255,170,80,0.16)','earth':'rgba(120,200,120,0.10)','void':'rgba(120,40,200,0.16)'}
CX=640
def cam(z0,z1,x0=0,x1=0,y0=0,y1=0,r0=0,r1=0): return {"from":{"z":z0,"x":x0,"y":y0,"r":r0},"to":{"z":z1,"x":x1,"y":y1,"r":r1}}
# push-in / pull-out / drift variants rotated so consecutive shots never move the same way
CAMS=[cam(1.0,1.09,0,0,0,-14),cam(1.1,1.0,-30,20,0,0),cam(1.0,1.08,40,-30,10,0,-0.006,0.006),cam(1.09,1.0,0,0,-12,10),cam(1.0,1.07,-40,30,0,-10,0.006,-0.004)]
class Film:
    def __init__(s): s.shots=[];s._c=itertools.count()
    def add(s,beat,at,sc=None,grade='cel',cam=None,draw='scene',**k):
        d={"beat":beat,"at":at,"draw":draw,"cam":cam or CAMS[next(s._c)%5],"grade":GRADES.get(grade,grade)}
        if sc is not None:d["sc"]=sc
        d.update(k);s.shots.append(d)
    def save(s,path):
        out=[];
        for b in sorted({x['beat'] for x in s.shots}): out+=[x for x in s.shots if x['beat']==b]
        json.dump(out,open(path,'w'),ensure_ascii=False,indent=0);return len(out)
def F(who,x,y,s,**k): d={"who":who,"x":x,"y":y,"s":s};d.update(k);return d
def bg(k,**o): d={"k":k};d.update(o);return d
