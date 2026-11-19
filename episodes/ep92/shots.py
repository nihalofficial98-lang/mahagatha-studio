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
def P(n,x,y=800,h=520,**k):return F('img',x,y,1.0,src=A+'lib_'+n+'.png',hpx=h,**k)
def SH(x=CX,**k):return F('shiva_p',x,800,1.0,hpx=640,**k)
def S(bgx,figs,fx=()):return {'bg':bgx,'figs':list(figs),'fx':list(fx)}
def im(src,x,y,w,**k):d={'t':'fximg','src':A+src,'x':x,'y':y,'w':w};d.update(k);return d
def orb(x,y,r,rgb,ga=.5):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
def shock(x,y,c,mx=700,rgb='255,215,130'):return {'t':'shock','x':x,'y':y,'c':c,'rgb':rgb,'max':mx}
def flash(c,w=.25,rgb='255,255,255'):return {'t':'flash','c':c,'w':w,'rgb':rgb}
RISH=lambda dx=0:[P('rishi_vasishtha',420+dx,h=430,walk=0),P('rishi_marichi',620+dx,h=430),P('rishi_atri',1300+dx,h=430),P('rishi_angirasa',1500+dx,h=430),P('daksha',960+dx,h=560)]
FIRE=[im('fx_fire_tall.png',960,860,420,alpha=.9,blend='lighter'),im('fx_embers.png',960,600,700,alpha=.7,blend='lighter',vx=0)]
# B01 yagna, then thunder
add(1,0,0,S(YG,RISH(),FIRE),'cel',cam=Z(1.0,1.08,0,0,0,-6))
add(1,1,0,S(YG,RISH(),FIRE+[im('fx_thunder_flash.png',CX,400,1900,alpha=.6,blend='lighter'),im('fx_lightning_bolt_a.png',1500,300,420,blend='lighter'),flash(0,.2)]),'dark',cues=['शिव'],cam=Z(1.08,1.2,0,0,0,-10),shake=4)
# B02 Kailash: calm -> mantras -> eyes open -> rage -> storms in
add(2,0,0,S(KB,[SH(eyes='closed')],[orb(CX,330,300,'160,190,255',.18)]),'night',cam=Z(1.0,1.06,0,0,0,-8))
add(2,1,0,S(KB,[SH(eyes='closed',headT=-.04)],[shock(1200,330,0,650),shock(1200,330,1,950)]),'night',cues=['मंत्रों','गूँज'],shake=1)
add(2,2,0,S(KB,[SH(eyes='open')],[]),'night',cam=Z(1.0,1.04,0,0,0,-6))
add(2,2,.5,S(KB,[SH(ka=[0,1,0,1.1])],[orb(CX,330,420,'255,60,40',.4),im('fx_thunder_flash.png',CX,300,1900,alpha=.45,blend='lighter'),im('fx_lightning_forks.png',500,300,520,blend='lighter'),im('fx_lightning_bolt_a.png',1500,300,420,blend='lighter')]),'red',cues=['आग'],cam=Z(1.04,1.16,0,0,0,-14),shake=3)
add(2,3,0,S(YG,[P('rishi_vasishtha',420,h=430),P('rishi_atri',1500,h=430),P('daksha',1200,h=560),SH(300,walk=7,vx=60,ka=[1,1,0,.1])],FIRE+[orb(300,400,380,'255,60,40',.3)]),'red',cam=Z(1.0,1.1,0,0,0,-8),shake=2)
add(2,3,.55,S(YG,[P('rishi_vasishtha',420,h=430),P('daksha',1200,h=560),SH(760,walk=7,ka=[1,1,0,.1])],FIRE+[shock(760,600,0,800,'255,90,50'),im('fx_explosion_burst.png',760,560,700,blend='lighter'),flash(0,.15,'255,160,100')]),'red',cam=Z(1.1,1.2,0,0,0,-10),shake=5)
# B03 everyone flees left; Vishnu walks in from the right
add(3,0,0,S(YG,[P('daksha',900,h=560,walk=9,vx=-200),P('rishi_marichi',520,h=430,walk=11,vx=-230),P('rishi_atri',1200,h=430,walk=10,vx=-220),P('rishi_angirasa',1450,h=430,walk=10,vx=-210)],FIRE+[im('fx_smoke_plume.png',1000,500,900,alpha=.5)]),'cel',cam=Z(1.0,1.08,0,0,0,-6),shake=2)
add(3,1,0,S(YG,[SH(520,ka=[1,1,0,.1])],FIRE),'red',cam=Z(1.06,1.0,0,0,0,-6))
add(3,2,0,S(YG,[SH(520,ka=[1,1,0,.1]),P('vishnu',1450,h=600,walk=6,vx=-120)],FIRE+[im('fx_sparkles_gold.png',1450,500,400,blend='lighter',alpha=.8)]),'cel',cam=Z(1.0,1.1,0,0,0,-6))
# B04 clash
add(4,0,0,S(YG,[SH(620,ka=[1,1,0,.1]),P('vishnu',1300,h=600)],FIRE+[orb(CX,500,700,'255,60,40',.25)]),'red',cam=Z(1.0,1.12,0,0,0,-8),shake=2)
add(4,1,0,S(YG,[SH(700,ka=[1,1,0,.1],lunge=1),P('vishnu',1200,h=600)],FIRE+[shock(960,520,0,900),shock(960,520,1,1300),im('fx_explosion_burst.png',960,520,900,blend='lighter'),flash(0,.2)]),'dark',cues=['भिड़'],cam=Z(1.1,1.25,0,0,0,-10),shake=8)
add(4,2,0,S(YG,[SH(660,ka=[1,1,0,.1]),P('vishnu',1260,h=600),],FIRE+[im('fx_sudarshan_chakra.png',1260,360,260,blend='lighter',spin=9),im('fx_lightning_bolt_a.png',700,300,420,blend='lighter')]),'red',cam=Z(1.12,1.2,0,0,0,-8),shake=4)
add(4,3,0,S(KB,[],[im('fx_thunder_flash.png',CX,500,1900,alpha=.6,blend='lighter'),im('fx_lightning_forks.png',700,400,700,blend='lighter'),im('fx_lightning_bolt_a.png',1300,400,500,blend='lighter'),shock(960,540,0,1400,'180,200,255')]),'dark',cam=Z(1.0,1.2,0,0,0,-4),shake=6)
print(film.save(os.path.join(HERE,'shots.json')),'shots')
