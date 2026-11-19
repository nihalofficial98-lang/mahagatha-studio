"""60-second test: library characters + painted backgrounds + effects + rigged Shiva."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ep03'))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep92');film=Film();A='../library/pilot/assets/'
def T(b,l,x=0.0):
    L=D[b]['lines'][l];return round(L['start']+x*(L['end']-L['start']),2)
def add(b,l,x,sc,grade='cel',**k):film.add(b,0 if (l==0 and x==0) else T(b,l,x),sc,grade,**k)
Z=cam
YG=bg('img',src=A+'bg_yagna2.png',fy=.5,z0=1.08,zv=.004)
KB=bg('img',src=A+'bg_kailash2.png',fy=.45,z0=1.1,zv=.003)
def P(n,x,y=690,h=520,**k):return F('img',x,y,1.0,src=A+'lib_'+n+'.png',hpx=h,**k)
def SH(x=CX,**k):return F('shiva_p',x,690,1.0,hpx=600,**k)
def S(bgx,figs,fx=()):return {'bg':bgx,'figs':list(figs),'fx':list(fx)}
def im(src,x,y,w,**k):d={'t':'fximg','src':A+src,'x':x,'y':y,'w':w};d.update(k);return d
def orb(x,y,r,rgb,ga=.5):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
def shock(x,y,c,mx=700,rgb='255,215,130'):return {'t':'shock','x':x,'y':y,'c':c,'rgb':rgb,'max':mx}
def flash(c,w=.25,rgb='255,255,255'):return {'t':'flash','c':c,'w':w,'rgb':rgb}

def th(a=.18):return im('fx_thunder_flash.png',CX,260,1300,alpha=a,blend='lighter')
def bolt(x,w=300,a=.8):return im('fx_lightning_bolt_a.png',x,230,w,alpha=a,blend='lighter')
FIRE=[im('fx_fire_tall.png',CX,700,300,alpha=.85,blend='lighter'),im('fx_embers.png',CX,420,520,alpha=.6,blend='lighter')]
def R(dx=0):return [P('rishi_vasishtha',250+dx,h=400),P('rishi_marichi',380+dx,h=400),P('rishi_atri',900+dx,h=400),P('rishi_angirasa',1030+dx,h=400),P('daksha',CX+dx,h=520)]
# B01 yagna, thunder on the name
add(1,0,0,S(YG,R(),FIRE),'cel',cam=Z(1.0,1.08,0,0,0,-4))
add(1,1,0,S(YG,R(),FIRE+[th(.22),bolt(980,280),flash(0,.12,'200,215,255')]),'dark',cues=['शिव'],cam=Z(1.08,1.2,0,0,0,-6),shake=4)
# B02 Kailash: calm, mantras arrive, eyes open, rage; then the hall
add(2,0,0,S(KB,[SH(eyes='closed')],[orb(CX,230,200,'160,190,255',.18)]),'night',cam=Z(1.0,1.06,0,0,0,-5))
add(2,1,0,S(KB,[SH(eyes='closed',headT=-.04)],[shock(700,230,0,430),shock(700,230,1,620)]),'night',cues=['मंत्रों','गूँज'],shake=1)
add(2,2,0,S(KB,[SH(eyes='open')],[]),'night',cam=Z(1.0,1.04,0,0,0,-4))
add(2,2,.5,S(KB,[SH(ka=[0,1,0,1.1])],[orb(CX,230,280,'255,60,40',.4),th(.2),bolt(250,300),bolt(1030,300)]),'red',cues=['आग'],cam=Z(1.04,1.16,0,0,0,-8),shake=3)
add(2,3,0,S(YG,[P('rishi_vasishtha',250,h=400),P('daksha',950,h=520),SH(560,ka=[1,1,0,.1])],FIRE+[orb(560,300,260,'255,60,40',.3)]),'red',cam=Z(1.0,1.1,0,0,0,-6),shake=2)
add(2,3,.55,S(YG,[P('rishi_vasishtha',250,h=400),P('daksha',950,h=520),SH(560,ka=[1,1,0,.1],lunge=1)],FIRE+[shock(560,400,0,520,'255,90,50'),flash(0,.1,'255,160,100')]),'red',cam=Z(1.1,1.2,0,0,0,-8),shake=5)
# B03 they scatter (cuts), Vishnu stands
add(3,0,0,S(YG,[P('daksha',520,h=520,rot=-.05),P('rishi_atri',200,h=400,rot=-.06)],FIRE+[im('fx_smoke_plume.png',800,350,620,alpha=.4)]),'cel',cam=Z(1.0,1.08,0,0,0,-4),shake=2)
add(3,1,0,S(YG,[SH(400,ka=[1,1,0,.1])],FIRE),'red',cam=Z(1.06,1.0,0,0,0,-4))
add(3,2,0,S(YG,[SH(380,ka=[1,1,0,.1]),P('vishnu',920,h=560)],FIRE+[im('fx_sparkles_gold.png',920,330,300,blend='lighter',alpha=.7)]),'cel',cam=Z(1.0,1.1,0,0,0,-4))
# B04 the clash
add(4,0,0,S(YG,[SH(420,ka=[1,1,0,.1]),P('vishnu',880,h=560)],FIRE+[orb(CX,330,480,'255,60,40',.25)]),'red',cam=Z(1.0,1.12,0,0,0,-6),shake=2)
add(4,1,0,S(YG,[SH(470,ka=[1,1,0,.1],lunge=1),P('vishnu',820,h=560)],FIRE+[shock(CX,350,0,600),shock(CX,350,1,880),flash(0,.12,'255,190,120')]),'dark',cues=['भिड़'],cam=Z(1.1,1.25,0,0,0,-8),shake=8)
add(4,2,0,S(YG,[SH(440,ka=[1,1,0,.1]),P('vishnu',860,h=560)],FIRE+[im('fx_sudarshan_chakra.png',860,230,170,blend='lighter',spin=9),bolt(470,280,.7)]),'red',cam=Z(1.12,1.2,0,0,0,-6),shake=4)
add(4,3,0,S(KB,[],[th(.25),im('fx_lightning_forks.png',450,280,460,alpha=.8,blend='lighter'),bolt(880,330),shock(CX,360,0,900,'180,200,255')]),'dark',cam=Z(1.0,1.2,0,0,0,-3),shake=6)
print(film.save(os.path.join(HERE,'shots.json')),'shots')
