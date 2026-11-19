"""Pilot (45 s): painted Gemini art + our effects. Scene = EP3 B05-B07 (Shiva's anger, everyone flees, Vishnu stands, they clash)."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ep03'))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep90');film=Film();A='../library/pilot/assets/'
def T(b,l,x=0.0):
    L=D[b]['lines'][l]
    if isinstance(x,str):
        for w in D[b]['words'][L['w0']:L['w0']+L['n']]:
            if w['text'].strip('"“”।,.…!?:').startswith(x):return round(w['start'],2)
        raise KeyError((b,l,x))
    return round(L['start']+x*(L['end']-L['start']),2)
def add(b,l,x,sc,grade='cel',**k):film.add(b,0 if (l==0 and x==0) else T(b,l,x),sc,grade,**k)
Z=cam
def KB(**o):return bg('img',src=A+'bg_kailash.png',fy=.42,z0=1.12,zv=.003,**o)
def YB(**o):return bg('img',src=A+'bg_yagna.png',fy=.72,z0=1.12,zv=.003,**o)
def IM(name,x,y,hpx,**k):return F('img',x,y,1.0,src=A+name+'.png',hpx=hpx,**k)
def S(b,figs=(),fx=(),fxb=()):return {'bg':b,'figs':list(figs),'fx':list(fx),'fxb':list(fxb)}
def orb(x,y,r,rgb,ga=.5):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
def spk(x,y,n=30,rx=300,ry=200):return {'t':'sparkle','x':x,'y':y,'n':n,'rx':rx,'ry':ry}
RAGE='rgba(255,60,40,.55)'
# ---------------- B01: meditation, the mantras, the anger ----------------
add(1,0,0,S(KB(),[IM('shiva_sit',CX,670,500,sway=.004)],[spk(CX,380,30,420,200)]),'night',cam=Z(1.0,1.08,0,0,0,-10),dx=.8)
add(1,0,'ध्यान',S(KB(fx=.5),[IM('shiva_calm_bust',CX,390,720,anchor='center',sway=.003)],[orb(CX,380,340,'160,190,255',.25)]),'night',cam=Z(1.0,1.06,0,0,0,-6))
add(1,1,0,S(KB(),[IM('shiva_sit',CX-60,670,500,sway=.004)],[{'t':'shock','x':1200,'y':330,'c':0,'rgb':'255,215,130','max':650},{'t':'shock','x':1200,'y':330,'c':1,'rgb':'255,215,130','max':950}]),'night',cues=['मंत्रों','गूँज'],shake=1)
add(1,1,'तपस्या',S(KB(),[IM('shiva_calm_bust',CX,390,720,anchor='center')],[{'t':'crack','x':CX,'c':0,'d':.5},{'t':'flash','c':0,'w':.25,'rgb':'255,215,130'}]),'dark',cues=['तोड़'],shake=3)
add(1,2,0,S(KB(),[IM('shiva_sit',CX,670,520,sway=.01)],[{'t':'shock','x':CX,'y':380,'c':0,'rgb':'200,210,255','max':760}]),'cool',cues=['बिखर'],shake=2)
add(1,2,'आँखें',S(KB(),[IM('shiva_calm_bust',CX,390,740,anchor='center')],[]),'night',cam=Z(1.0,1.1,0,0,0,-12))
add(1,2,'आग',S({'k':'img','src':A+'bg_kailash.png','fy':.42,'z0':1.12,'zv':.003,'tint':'rgba(120,10,10,.35)'},[IM('shiva_angry_bust',CX,390,760,anchor='center',glow='rgba(255,70,40,.8)')],[orb(CX,330,420,'255,60,40',.45),{'t':'flash','c':0,'w':.3,'rgb':'255,120,90'}]),'red',cues=['आग'],cam=Z(1.0,1.1,0,0,0,-12),shake=2)
add(1,3,0,S(YB(),[IM('shiva_rage_full',420,700,600,sway=.006)],[{'t':'sparkle','x':CX,'y':420,'n':40,'rx':520,'ry':240}]),'red',cam=Z(1.0,1.08,0,0,0,-8),shake=2)
add(1,3,'उलट',S(YB(),[IM('shiva_rage_full',CX,730,720,sway=.01)],[{'t':'flash','c':0,'w':.3,'rgb':'255,170,120'},{'t':'shock','x':CX,'y':420,'c':0,'rgb':'255,130,90','max':900}]),'red',cues=['उलट'],shake=6)
# ---------------- B02: everyone flees; Vishnu stays ----------------
add(2,0,0,S(YB(),[IM('flee_group',1000,650,300,vx=-110,breath=.012)],[{'t':'sparkle','x':CX,'y':420,'n':30,'rx':520,'ry':240}]),'dark',shake=2)
add(2,1,0,S(YB(),[IM('vishnu_full',CX,700,600,sway=.003,glow='rgba(150,190,255,.7)')],[orb(CX,380,360,'150,190,255',.25)]),'cool',cam=Z(1.0,1.1,0,0,0,-10))
add(2,2,0,S(YB(),[IM('shiva_rage_full',330,700,560,sway=.006),IM('vishnu_full',950,700,600,sway=.003,glow='rgba(150,190,255,.6)')],[]),'dark',cam=Z(1.0,1.06,0,0,0,0))
# ---------------- B03: the clash ----------------
add(3,0,0,S({'k':'img','src':A+'bg_yagna.png','fy':.5,'z0':1.12,'zv':.003,'tint':'rgba(120,10,10,.3)'},[IM('shiva_angry_bust',CX,390,760,anchor='center',glow='rgba(255,70,40,.8)')],[orb(CX,330,440,'255,60,40',.45)]),'red',cam=Z(1.0,1.1,0,0,0,-12),shake=2)
add(3,0,.62,S(YB(),[IM('shiva_rage_full',330,700,580,sway=.01),IM('vishnu_full',950,700,620,sway=.004)],[{'t':'flames','x':330,'y':700,'sc':1.0,'c':0}]),'red',shake=3)
add(3,1,0,S(YB(),[IM('shiva_rage_full',CX-190,710,640,sway=.015),IM('vishnu_full',CX+190,710,660,sway=.006)],[{'t':'flash','c':0,'w':.35,'rgb':'255,220,180'},{'t':'shock','x':CX,'y':420,'c':0,'rgb':'255,180,120','max':900}]),'red',cues=['भिड़'],shake=7)
add(3,2,0,S(YB(),[IM('shiva_rage_full',300,700,560,sway=.008)],[{'t':'icon','i':'trident','x':900,'y':330,'sc':3.4,'c':0,'d':.5}]),'dark',cues=['त्रिशूल'],shake=2)
add(3,2,'चक्र',S(YB(),[IM('vishnu_full',980,700,620,sway=.004)],[{'t':'icon','i':'cycle','x':380,'y':330,'sc':3.4,'c':0,'d':.5}]),'warm',cues=['चक्र'],shake=2)
print(film.save(os.path.join(HERE,'shots.json')),'shots')
