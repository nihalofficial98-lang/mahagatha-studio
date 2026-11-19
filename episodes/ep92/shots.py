"""60-second test, ORIGINAL coded cast (the characters you liked) + library effects/objects where they help."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ep03'))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep92');film=Film();A='../library/pilot/assets/'
def T(b,l,x=0.0):
    L=D[b]['lines'][l];return round(L['start']+x*(L['end']-L['start']),2)
def add(b,l,x,sc,grade='cel',**k):film.add(b,0 if (l==0 and x==0) else T(b,l,x),sc,grade,**k)
Z=cam
def Y(figs,fx=(),fire=.9):return {'bg':bg('yagna',fire=fire),'figs':list(figs),'fx':list(fx)}
def S(b,figs,fx=()):return {'bg':b,'figs':list(figs),'fx':list(fx)}
def im(src,x,y,w,**k):d={'t':'fximg','src':A+src,'x':x,'y':y,'w':w};d.update(k);return d
def shock(x,y,c,mx,rgb='255,215,130'):return {'t':'shock','x':x,'y':y,'c':c,'rgb':rgb,'max':mx}
def flash(w,rgb):return {'t':'flash','c':0,'w':w,'rgb':rgb}
def glow(x,y,r,rgb,ga):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
RAGE=dict(pose='rage',expr={'brow':-.95},aura='255,70,40');LUNGE=dict(pose='lunge',expr={'brow':-.95})
def fires(a=1.0):return [im('fx_fire_tall.png',210,640,300*a,blend='lighter',alpha=.9),im('fx_fire_tall.png',1070,640,300*a,blend='lighter',alpha=.9),im('fx_embers.png',640,420,700,blend='lighter',alpha=.6)]
bolt=lambda x,w=260:im('fx_lightning_bolt_a.png',x,230,w,blend='lighter',alpha=.85)
# B01 hall, thunder on the name
add(1,0,0,Y([F('rishi0',300,650,1.15),F('daksha',640,650,1.3),F('rishi3',980,650,1.15)]),'cel',cam=Z(1.0,1.08,0,0,0,-10))
add(1,1,0,Y([F('rishi0',300,650,1.15),F('daksha',640,650,1.3),F('rishi3',980,650,1.15)],[bolt(1000),bolt(250,220),flash(.15,'200,215,255')]),'dark',cam=Z(1.08,1.18,0,0,0,-8),shake=4)
# B02 Kailash -> rage -> hall
add(2,0,0,S(bg('kailash',mx=.22),[F('shiva',640,650,1.25,expr={'eye':.2})]),'night',cam=Z(1.0,1.06,0,0,0,-8))
add(2,1,0,S(bg('kailash',mx=.22),[F('shiva',580,650,1.25,expr={'eye':.2})],[shock(1180,340,0,650),shock(1180,340,1,900)]),'night',shake=1)
add(2,2,0,S(bg('kailash',mx=.22),[F('shiva',640,470,2.3,head=True,expr={'eye':.2})]),'night')
add(2,2,.5,S(bg('storm',r=.5),[F('shiva',640,470,3.0,head=True,expr={'brow':-.95})],[glow(640,400,380,'255,60,40',.5),bolt(220,300),bolt(1060,300),im('fx_thunder_flash.png',640,250,1100,blend='lighter',alpha=.25)]),'red',shake=2)
add(2,3,0,Y([F('shiva',420,670,1.65,**RAGE)],fires(1.1)),'red',cam=Z(1.0,1.1,0,0,0,-8),shake=2)
add(2,3,.6,Y([F('shiva',640,670,1.55,**dict(LUNGE,aura='255,70,40'))],fires(1.1)+[shock(640,420,0,900,'255,120,80'),flash(.2,'255,160,120')]),'red',shake=6)
# B03 flee, Vishnu stands
add(3,0,0,Y([F('daksha',560,650,1.3,pose='flee',vx=-120),F('rishi0',860,650,1.15,pose='flee',vx=-120),F('rishi3',1060,650,1.15,pose='flee',vx=-120)],[im('fx_smoke_plume.png',900,380,700,alpha=.4)],.7),'cel',shake=2)
add(3,0,.6,Y([F('rishi1',420,660,1.55,pose='flee',vx=-60),F('rishi4',830,660,1.55,pose='flee',vx=-60)],[],.6),'cel',shake=2)
add(3,1,0,Y([F('vishnu',640,665,1.5,aura='130,170,255')],[im('fx_sparkles_gold.png',640,330,420,blend='lighter',alpha=.8)],.5),'cel')
add(3,2,0,Y([F('shiva',300,660,1.45,**RAGE),F('vishnu',980,665,1.45,flip=-1,aura='130,170,255')],[],.5),'dark')
# B04 clash: effects and objects where they help
add(4,0,0,S(bg('voidR',rgb='255,60,30'),[F('shiva',640,670,1.6,**LUNGE)],fires(1.2)),'red',shake=3)
add(4,1,0,S(bg('cosmos',rgb='220,110,90',spin=.05),[F('shiva',410,670,1.5,**LUNGE),F('vishnu',870,670,1.5,flip=-1)],[shock(640,380,0,900,'255,180,120'),shock(640,380,1,1200,'255,200,150'),im('fx_explosion_burst.png',640,380,800,blend='lighter',alpha=.8),flash(.12,'255,220,180')]),'red',shake=7)
add(4,2,0,S(bg('cosmos',rgb='170,130,255',spin=.05),[F('shiva',260,670,1.2,**LUNGE)],[im('fx_trident_plain.png',900,330,240,alpha=.95)]),'night',shake=2)
add(4,2,.5,S(bg('cosmos',rgb='255,220,130',spin=.05),[F('vishnu',1020,670,1.2,flip=-1)],[im('fx_sudarshan_chakra.png',400,330,260,blend='lighter',spin=6)]),'cel',shake=2)
add(4,3,0,S(bg('cosmos',rgb='150,170,255',spin=.4),[],[shock(640,360,0,1000,'170,190,255'),shock(640,360,1,1200,'255,200,150'),bolt(300,320),bolt(980,320),im('fx_thunder_flash.png',640,300,1100,blend='lighter',alpha=.22)]),'dark',shake=6)
print(film.save(os.path.join(HERE,'shots.json')),'shots')
