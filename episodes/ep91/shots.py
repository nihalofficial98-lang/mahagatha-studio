"""10-second test of the RIGGED painted Shiva puppet (pieces sliced from the approved Gemini art)."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ep03'))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep91');film=Film();A='../library/pilot/assets/'
def T(b,l,x=0.0):
    L=D[b]['lines'][l];return round(L['start']+x*(L['end']-L['start']),2)
def add(b,l,x,sc,grade='cel',**k):film.add(b,0 if (l==0 and x==0) else T(b,l,x),sc,grade,**k)
Z=cam
KB=bg('img',src=A+'bg_kailash2.png',fy=.45,z0=1.1,zv=.003)
def SH(**k):return F('shiva_p',CX,690,1.0,hpx=640,**k)
def S(figs,fx=()):return {'bg':KB,'figs':list(figs),'fx':list(fx)}
def orb(x,y,r,rgb,ga=.5):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
# calm, eyes closed, breathing
add(1,0,0,S([SH(eyes='closed')],[orb(CX,330,300,'160,190,255',.18)]),'night',cam=Z(1.0,1.06,0,0,0,-8),dx=.6)
# the mantras arrive: shock rings, he stirs
add(1,1,0,S([SH(eyes='closed',headT=-.04)],[{'t':'shock','x':1200,'y':330,'c':0,'rgb':'255,215,130','max':650},{'t':'shock','x':1200,'y':330,'c':1,'rgb':'255,215,130','max':950}]),'night',cues=['मंत्रों','गूँज'],cam=Z(1.06,1.1,0,0,0,-10),shake=1)
add(1,1,.6,S([SH(eyes='closed',headT=-.06)],[{'t':'crack','x':CX,'c':0,'d':.5},{'t':'flash','c':0,'w':.25,'rgb':'255,215,130'}]),'dark',cues=['तोड़'],shake=3)
# eyes open, anger builds: head swaps to the red-eyed face, legs widen, arm lifts
add(1,2,0,S([SH(eyes='open')],[]),'night',cam=Z(1.0,1.04,0,0,0,-6))
add(1,2,.45,S([SH(ka=[0,1,0,1.1],lunge=0)],[orb(CX,330,420,'255,60,40',.4),{'t':'flash','c':0,'w':.3,'rgb':'255,120,90'}]),'red',cues=['आग'],cam=Z(1.04,1.14,0,0,0,-14),shake=3)
print(film.save(os.path.join(HERE,'shots.json')),'shots')
