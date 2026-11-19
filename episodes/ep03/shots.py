"""EP3 shot list: हरिहर और अर्धनारीश्वर. Every shot starts on a spoken line (or a fraction of a line), timed from build/ep03/timings.json.
Visual rules: v2 cast (Shiva/Vishnu/Brahma/Daksha/sages/Adishakti/Manu/Brahmi), new settings (yagna hall, Kailash night, garden, cosmic sea)."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.dirname(__file__))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep03');film=Film()
def T(b,l,fr=0.0):
    L=D[b]['lines'][l];return round(L['start']+fr*(L['end']-L['start']),2)
def add(b,l,fr,sc,grade='cel',**k):film.add(b,0 if (l==0 and fr==0) else T(b,l,fr),sc,grade,**k)
# --- scene builders ---
def Y(figs,fx=(),fire=1.0,fxb=(),**o):return {'bg':bg('yagna',fire=fire,**o),'figs':list(figs),'fx':list(fx),'fxb':list(fxb)}
def K(figs,fx=(),mx=.22):return {'bg':bg('kailash',mx=mx),'figs':list(figs),'fx':list(fx)}
def O(figs,fx=(),gold=0,oy=560,rgb='150,180,255',gy=340,ga=.2):return {'bg':bg('cosmicsea',gold=gold,oy=oy,rgb=rgb,gy=gy,ga=ga),'figs':list(figs),'fx':list(fx)}
def C(figs,fx=(),rgb='160,120,255',spin=.05):return {'bg':bg('cosmos',rgb=rgb,spin=spin),'figs':list(figs),'fx':list(fx)}
def G(figs,fx=()):return {'bg':bg('garden'),'figs':list(figs),'fx':list(fx)}
def R(figs,fx=(),r=.6):return {'bg':bg('storm',r=r),'figs':list(figs),'fx':list(fx)}
def V(figs,fx=(),rgb='255,60,30'):return {'bg':bg('voidR',rgb=rgb),'figs':list(figs),'fx':list(fx)}
def W(figs,fx=(),warm=True):return {'bg':bg('cel',warm=warm),'figs':list(figs),'fx':list(fx)}
# --- cast shorthands (feet position y, scale s) ---
ANG={'brow':-.95};CLS={'eye':.2}
def sh(x,y=650,s=1.25,**k):return F('shiva',x,y,s,**k)
def vi(x,y=650,s=1.25,**k):return F('vishnu',x,y,s,**k)
def br(x,y=620,s=1.1,**k):return F('brahma',x,y,s,**k)
def da(x,y=650,s=1.25,**k):return F('daksha',x,y,s,**k)
def ri(i,x,y=650,s=1.1,**k):return F('rishi%d'%i,x,y,s,**k)
def ad(x,y=650,s=1.25,**k):return F('adishakti',x,y,s,**k)
def ma(x,y=650,s=1.25,**k):return F('manu',x,y,s,**k)
def bh(x,y=650,s=1.25,**k):return F('brahmi',x,y,s,**k)
def hd(who,x=CX,y=440,s=2.3,**k):return F(who,x,y,s,head=True,**k)
def txt(s,x,y,size,c=0,col=None,glow='rgba(255,220,150,.8)',d=.7):return {'t':'text','s':s,'x':x,'y':y,'size':size,'c':c,'d':d,'glow':glow}
def nm(s,x,y,c,size=32):return {'t':'name','s':s,'x':x,'y':y,'c':c,'d':.4,'size':size}
def cn(b,**k):return k
Z=cam
# ================= B01: the hook =================
add(1,0,0,C([br(CX,560,1.35)],rgb='120,140,255'),'night',dx=.9)
add(1,0,.62,V([],[{'t':'icon','i':'vortex','x':CX,'y':320,'sc':3.0,'c':0,'d':1.0},txt('श्राप',CX,560,84,0,glow='rgba(255,70,50,.9)')],rgb='140,30,60'),'red',cues=['श्राप'],shake=2)
add(1,1,0,C([hd('brahma',CX,470,2.0,expr=CLS)],rgb='100,110,200'),'dark',cam=Z(1.0,1.08,0,0,0,-10))
add(1,1,.5,O([br(CX+120,520,.8)],oy=470,rgb='110,140,220'),'night',cam=Z(1.0,1.1,0,0,0,-14))
add(1,2,0,C([sh(300,650,1.4,dark=.25,key='80,100,200'),vi(980,650,1.4,flip=-1,dark=.25,key='80,100,200')],[{'t':'bolt','x0':420,'y0':330,'x1':860,'y1':400,'c':0,'d':.4}],rgb='170,90,90'),'dark',cues=['भिड़'])
add(1,2,.12,C([sh(CX-250,650,1.3,pose='rage',expr=ANG),vi(CX+250,650,1.3,flip=-1)],[{'t':'shock','x':CX,'y':360,'c':0,'rgb':'255,170,120','max':800}],rgb='200,90,90'),'red',cues=['भिड़'],shake=3)
add(1,2,.66,C([F('ardha',CX,660,1.5,dark=.3,aura='255,215,150')],[{'t':'glow','x':CX,'y':330,'r':340,'rgb':'255,215,150','ga':.5}],rgb='255,210,140'),'amb',cam=Z(1.0,1.12,0,0,0,-24))
# ================= B02: Daksha's yagna =================
add(2,0,0,Y([da(330,650,1.2)],fire=.45),'warm',dx=.7)
add(2,0,.5,Y([da(430,665,1.75,pose='open')],fire=.7,fx=[nm('दक्ष',760,250,0,40)]),'warm',cues=['दक्ष'])
add(2,1,0,Y([ri(i,170+i*155,650,.95,pose='namaste',ac=i if i<3 else None,ad=.4) for i in range(7)],fire=.6,fx=[nm(n,170+i*155,150,i,28) for i,n in enumerate(['वशिष्ठ','मरीचि','अत्रि'])]),'warm',cues=['वशिष्ठ','मरीचि','अत्रि'])
add(2,1,.36,Y([ri(3,500,660,1.5,pose='namaste'),ri(4,830,660,1.5,pose='namaste')],fire=.6,fx=[nm('अंगिरा',500,110,0,34),nm('पुलस्त्य',830,110,1,34)]),'warm',cues=['अंगिरा','पुलस्त्य'])
add(2,1,.7,Y([ri(5,470,660,1.5,pose='namaste'),ri(6,810,660,1.5,pose='namaste')],fire=.6,fx=[nm('पुलह',470,110,0,34),nm('क्रतु',810,110,1,34)]),'warm',cues=['पुलह','क्रतु'])
add(2,2,0,Y([ri(i,140+i*125,640,.8,pose='sit') for i in range(3)]+[ri(i,820+(i-3)*125,640,.8,pose='sit') for i in range(3,7)],fire=.85),'warm')
add(2,2,.33,Y([vi(780,665,1.45,aura='130,170,255')],fire=.7,fx=[{'t':'sparkle','x':780,'y':400,'n':24,'rx':200,'ry':240}]),'cool')
add(2,2,.7,Y([br(420,640,1.35,aura='255,225,170'),vi(850,665,1.3,aura='130,170,255')],fire=.8),'warm')
# ================= B03: the mantras =================
add(3,0,0,Y([],fire=1.0,fxb=[{'t':'sparkle','x':CX,'y':400,'n':30,'rx':180,'ry':200}]),'amb',cam=Z(1.0,1.18,0,0,0,-30),dx=.8)
add(3,0,.5,Y([ri(1,420,640,1.35,pose='sit'),ri(2,860,640,1.35,pose='sit')],fire=1.0),'warm')
add(3,1,0,C([],[txt('ॐ',CX,380,260,0,glow='rgba(255,210,120,.9)',d=.9),{'t':'shock','x':CX,'y':330,'c':0,'rgb':'255,210,130','max':900}],rgb='255,200,110'),'amb',cues=['मंत्र'])
add(3,1,.5,C([],[{'t':'ribbon','c':0,'x0':-100,'y0':240,'x1':CX,'y1':380,'dur':1.2},{'t':'ribbon','c':1,'x0':1380,'y0':520,'x1':CX,'y1':400,'dur':1.2},{'t':'sparkle','x':CX,'y':380,'n':34,'rx':500,'ry':220}],rgb='255,190,100'),'amb',cues=['ब्रह्मांड','नसों'])
add(3,2,0,{'bg':bg('dawn'),'figs':[],'fx':[{'t':'sparkle','x':CX,'y':420,'n':40,'rx':520,'ry':260},{'t':'glow','x':CX,'y':200,'r':460,'rgb':'255,235,190','ga':.5}]},'warm',cues=['पवित्रता'])
add(3,2,.5,W([ri(0,260,650,1.0,pose='sit'),ri(2,CX,650,1.0,pose='sit'),ri(5,1020,650,1.0,pose='sit')],[{'t':'sparkle','x':CX,'y':330,'n':40,'rx':520,'ry':200}]),'warm')
add(3,3,0,Y([vi(450,665,1.35),br(850,640,1.25)],fire=.8),'warm')
add(3,3,.5,Y([ri(i,150+i*105,640,.7,pose='sit') for i in range(3)]+[ri(i,860+(i-3)*105,640,.7,pose='sit') for i in range(3,7)],fire=.7),'amb',cam=Z(1.08,1.0,0,0,0,0),fxb=[])
# ================= B04: the door =================
add(4,0,0,Y([],fire=.8),'warm',cam=Z(1.0,1.06,0,0,0,-10))
add(4,0,.55,Y([],fire=.7,fx=[{'t':'shock','x':1150,'y':400,'c':0,'rgb':'180,200,255','max':700},{'t':'flash','c':0,'w':.3,'rgb':'200,210,255'}]),'dark',cues=['हलचल'],shake=2)
add(4,1,0,R([],[txt('शिव!',CX,330,170,0,glow='rgba(120,150,255,.95)',d=.35),{'t':'flash','c':0,'w':.25,'rgb':'170,190,255'}],r=.3),'dark',cues=['शिव'],shake=4)
# ================= B05: Shiva's rage begins =================
add(5,0,0,K([sh(CX,650,1.25,expr=CLS)]),'night',dx=.8)
add(5,0,.55,K([hd('shiva',CX,470,2.3,expr=CLS)]),'night',cam=Z(1.0,1.08,0,0,0,-8))
add(5,1,0,K([sh(CX-60,650,1.25,expr=CLS)],[{'t':'shock','x':1180,'y':340,'c':0,'rgb':'255,215,130','max':650},{'t':'shock','x':1180,'y':340,'c':1,'rgb':'255,215,130','max':900}]),'night',cues=['मंत्रों','गूँज'])
add(5,1,.55,K([hd('shiva',CX,470,2.6,expr=CLS)],[{'t':'crack','x':CX,'c':0,'d':.5},{'t':'flash','c':0,'w':.25,'rgb':'255,215,130'}]),'dark',cues=['तोड़'],shake=3)
add(5,2,0,K([sh(CX,650,1.25,pose='stand',expr={'brow':-.3})],[{'t':'shock','x':CX,'y':380,'c':0,'rgb':'200,210,255','max':760}]),'cool',cues=['बिखर'],shake=2)
add(5,2,.5,{'bg':bg('storm',r=.5),'figs':[hd('shiva',CX,470,3.0,expr=ANG)],'fx':[{'t':'glow','x':CX,'y':400,'r':380,'rgb':'255,60,40','ga':.5}]},'red',cam=Z(1.0,1.1,0,0,0,-12),shake=1)
add(5,3,0,Y([sh(420,670,1.65,pose='rage',expr=ANG,aura='255,70,40')],fire=.9,fx=[{'t':'flames','x':200,'y':690,'sc':1.2,'c':0},{'t':'flames','x':700,'y':690,'sc':1.2,'c':0}]),'red',cues=['घुसे'],shake=2)
add(5,3,.55,Y([sh(CX,670,1.55,pose='lunge',expr=ANG,aura='255,70,40')],fire=.8,fx=[{'t':'shock','x':CX,'y':420,'c':0,'rgb':'255,120,80','max':900},{'t':'flash','c':0,'w':.3,'rgb':'255,160,120'}]),'red',cues=['उलट'],shake=6)
# ================= B06: everyone flees, Vishnu stays =================
add(6,0,0,Y([da(560,650,1.3,pose='flee',vx=-120),ri(0,860,650,1.15,pose='flee',vx=-120),ri(3,1060,650,1.15,pose='flee',vx=-120)],fire=.7),'dark',shake=2)
add(6,0,.5,Y([ri(1,420,660,1.55,pose='flee',vx=-60),ri(4,830,660,1.55,pose='flee',vx=-60)],fire=.6),'dark',shake=2)
add(6,1,0,Y([vi(CX,665,1.5,aura='130,170,255')],fire=.5),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(6,2,0,Y([sh(300,660,1.45,pose='rage',expr=ANG),vi(980,665,1.45,flip=-1,aura='130,170,255')],fire=.5),'dark',cam=Z(1.0,1.08,0,0,0,0))
# ================= B07: the battle =================
add(7,0,0,R([hd('shiva',CX,470,2.6,expr=ANG)],[{'t':'glow','x':CX,'y':400,'r':420,'rgb':'255,60,40','ga':.5}]),'red',shake=2)
add(7,0,.6,V([sh(CX,670,1.6,pose='lunge',expr=ANG)],[{'t':'flames','x':CX-250,'y':700,'sc':1.3,'c':0},{'t':'flames','x':CX+250,'y':700,'sc':1.3,'c':0}]),'red',shake=3)
add(7,1,0,C([sh(CX-230,670,1.5,pose='lunge',expr=ANG),vi(CX+230,670,1.5,flip=-1)],[{'t':'shock','x':CX,'y':380,'c':0,'rgb':'255,180,120','max':900},{'t':'flash','c':0,'w':.3,'rgb':'255,220,180'}],rgb='220,110,90'),'red',cues=['भिड़'],shake=7)
add(7,2,0,C([sh(260,670,1.2,pose='lunge',expr=ANG)],[{'t':'icon','i':'trident','x':900,'y':330,'sc':3.4,'c':0,'d':.5}],rgb='170,130,255'),'night',cues=['त्रिशूल'],shake=2)
add(7,2,.55,C([vi(1020,670,1.2,flip=-1)],[{'t':'icon','i':'cycle','x':400,'y':330,'sc':3.4,'c':0,'d':.5}],rgb='255,220,130'),'amb',cues=['चक्र'],shake=2)
add(7,3,0,C([],[{'t':'shock','x':CX,'y':360,'c':0,'rgb':'170,190,255','max':1000},{'t':'shock','x':CX,'y':360,'c':1,'rgb':'255,200,150','max':1200}],rgb='150,170,255',spin=.4),'void',cues=['काँप','उठीं'],shake=6)
add(7,3,.38,C([],[{'t':'icon','i':'cycle','x':CX,'y':330,'sc':3.0,'c':0,'d':.8},{'t':'dim','ga':.4}],rgb='170,150,255',spin=0),'night',cues=['थम'])
add(7,3,.6,C([],[{'t':'icon','i':'flame','x':200,'y':360,'sc':1.8,'c':0,'d':.5},{'t':'icon','i':'frost','x':420,'y':360,'sc':1.8,'c':1,'d':.5},{'t':'icon','i':'vortex','x':640,'y':360,'sc':1.8,'c':2,'d':.5},{'t':'icon','i':'light','x':860,'y':360,'sc':1.8,'c':3,'d':.5},{'t':'icon','i':'lotusI','x':1080,'y':360,'sc':1.8,'c':4,'d':.5}],rgb='120,120,200'),'dark',cues=['तत्वों','डर','अपनी','आँखें','ढक'])
# ================= B08: stalemate =================
add(8,0,0,C([sh(300,670,1.35,pose='lunge',expr=ANG),vi(980,670,1.35,flip=-1)],[{'t':'crack','x':CX-160,'c':0,'d':.6},{'t':'crack','x':CX+160,'c':1,'d':.6}],rgb='220,110,90'),'red',cues=['दीवारें','दरकने'],shake=4)
add(8,1,0,C([sh(260,670,1.3,pose='lunge',expr=ANG),vi(1020,670,1.3,flip=-1)],[{'t':'scales','x':CX,'y':210,'sc':.8,'c':0,'d':.6}],rgb='170,130,255'),'night',cues=['बराबर'])
add(8,1,.55,C([hd('shiva',380,450,2.0,expr=ANG),hd('vishnu',900,450,2.0,flip=-1,expr={'brow':-.3})],[],rgb='200,120,120'),'red',cam=Z(1.0,1.06,0,0,0,0))
add(8,2,0,V([],[{'t':'icon','i':'cycle','x':CX,'y':300,'sc':2.4,'c':0,'d':.8}],rgb='255,90,40'),'red',shake=2)
add(8,2,.5,{'bg':bg('storm',r=1),'figs':[],'fx':[txt('राख',CX,360,200,0,glow='rgba(255,90,40,.9)',d=1.0)]},'red',cues=['राख'])
# ================= B09: Brahma pleads =================
add(9,0,0,C([hd('brahma',CX,470,2.1)],rgb='140,140,220'),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(9,1,0,C([br(CX,560,1.25),sh(150,640,.7,pose='lunge',expr=ANG,dark=.5),vi(1130,640,.7,flip=-1,dark=.5)],rgb='170,130,220'),'night')
add(9,1,.4,C([sh(300,670,1.3,pose='lunge',expr=ANG),vi(980,670,1.3,flip=-1)],[{'t':'scales','x':CX,'y':300,'c':0,'d':.6}],rgb='170,130,255'),'night',cues=['बराबर'])
add(9,1,.72,C([hd('shiva',340,450,1.9,expr=ANG),hd('vishnu',920,450,1.9,flip=-1)],[txt('उलट',CX,560,80,0,d=.6)],rgb='200,120,120'),'dark',cues=['उलट'])
add(9,2,0,V([],[{'t':'infinity','x':CX,'y':330,'c':0,'d':.8}],rgb='200,60,60'),'red',cues=['कभी'])
# ================= B10: the ultimatum =================
add(10,0,0,C([hd('brahma',CX,470,2.3,expr={'brow':-.2})],rgb='150,150,230'),'cool')
add(10,0,.5,C([sh(300,670,1.3,pose='lunge',expr=ANG,dark=.6),vi(980,670,1.3,flip=-1,dark=.6),br(CX,500,.7)],rgb='220,110,90'),'dark')
add(10,1,0,C([hd('brahma',CX,470,2.7,expr={'brow':-.3})],[{'t':'glow','x':CX,'y':380,'r':320,'rgb':'255,220,170','ga':.3}],rgb='200,170,255'),'warm',cam=Z(1.0,1.1,0,0,0,-12))
add(10,1,.5,C([],[{'t':'dim','ga':.6},txt('सृष्टि',CX,380,140,0,glow='rgba(255,220,150,.9)')],rgb='100,100,160',spin=0),'dark',cues=['सृष्टि'])
add(10,2,0,C([hd('shiva',340,450,1.9,expr=ANG),hd('vishnu',920,450,1.9,flip=-1)],[txt('?',CX,420,230,0,d=.8)],rgb='180,120,160'),'dark')
# ================= B11: they stop =================
add(11,0,0,C([sh(320,665,1.35),vi(960,665,1.35,flip=-1)],[{'t':'glow','x':CX,'y':340,'r':420,'rgb':'255,225,170','ga':.3}],rgb='170,150,255',spin=.02),'cool')
add(11,0,.5,W([hd('vishnu',CX,440,2.3)],[{'t':'sparkle','x':CX,'y':330,'n':20,'rx':320,'ry':220}],warm=False),'cool')
add(11,1,0,C([hd('brahma',CX,470,2.3)],[{'t':'glow','x':CX,'y':380,'r':340,'rgb':'255,225,170','ga':.35}],rgb='210,180,255'),'warm',cam=Z(1.0,1.08,0,0,0,-10))
add(11,1,.5,W([br(CX,640,1.5,aura='255,225,170')]),'warm')
add(11,2,0,{'bg':bg('dawn'),'figs':[sh(300,665,1.0,dark=.5),vi(980,665,1.0,flip=-1,dark=.5)],'fx':[{'t':'sparkle','x':CX,'y':400,'n':30,'rx':500,'ry':220}]},'warm')
# ================= B12: Hari + Hara = Harihara =================
add(12,0,0,W([hd('vishnu',CX,440,2.3)],[txt('हरि',CX,170,120,0,d=.7)],warm=False),'cool',cues=['हरि'])
add(12,0,.55,K([hd('shiva',CX,470,2.3)],[txt('हर',CX,170,120,0,d=.7)]),'night',cues=['हर'])
add(12,1,0,W([sh(340,665,1.3),vi(940,665,1.3,flip=-1)],[txt('हरने वाला',CX,200,64,0,d=.8)]),'warm',cues=['हरने'])
add(12,1,.5,C([],[{'t':'icon','i':'light','x':400,'y':330,'sc':2.8,'c':0,'d':.6},{'t':'icon','i':'light','x':880,'y':330,'sc':2.8,'c':1,'d':.6},txt('डर',400,560,70,0),txt('दुख',880,560,70,1)],rgb='255,210,150'),'amb',cues=['डर','दुख'])
add(12,2,0,W([sh(CX-170,665,1.4),vi(CX+170,665,1.4,flip=-1)],[{'t':'sparkle','x':CX,'y':420,'n':26,'rx':300,'ry':220}]),'warm')
add(12,2,.55,C([],[txt('हरि = हर',CX,360,120,0,d=.8)],rgb='255,210,150'),'amb')
add(12,3,0,{'bg':bg('dawn'),'figs':[hd('harihara',CX,450,2.4)],'fx':[{'t':'sparkle','x':CX,'y':330,'n':24,'rx':340,'ry':220}]},'warm',cues=['साथ'])
add(12,3,.6,{'bg':bg('dawn'),'figs':[F('harihara',CX,675,1.65,aura='255,225,170')],'fx':[txt('हरिहर',CX,170,130,0,d=.9),{'t':'sparkle','x':CX,'y':400,'n':36,'rx':500,'ry':240}]},'warm',cues=['हरिहर'])
# ================= B13: after the yagna =================
add(13,0,0,Y([sh(500,665,1.35,vx=70,fo=0,fd=4,flip=-1)],fire=.7),'warm')
add(13,0,.6,Y([ri(i,150+i*105,640,.7,pose='sit') for i in range(3)]+[ri(i,860+(i-3)*105,640,.7,pose='sit') for i in range(3,7)],fire=.5),'warm')
add(13,1,0,Y([vi(400,665,1.45),br(850,640,1.3)],fire=.3),'cool',cam=Z(1.0,1.08,0,0,0,-10))
# ================= B14: Vishnu asks =================
add(14,0,0,Y([vi(420,665,1.5),br(880,640,1.3)],fire=.3),'cool')
add(14,0,.4,Y([hd('brahma',CX,470,2.2,expr=CLS)],fire=.3),'dark',cam=Z(1.0,1.08,0,0,0,-8))
add(14,0,.75,Y([hd('vishnu',CX,440,2.4)],fire=.3),'cool')
add(14,1,0,Y([hd('vishnu',CX,440,2.7)],fire=.25),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(14,1,.55,Y([br(CX,640,1.5)],fire=.25),'dark')
# ================= B15: Brahma's pain =================
add(15,0,0,Y([hd('brahma',CX,470,2.3,expr=CLS)],[{'t':'tears','x':CX-60,'y':430,'dx':110,'len':120}],fire=.2),'dark')
add(15,0,.5,C([br(CX,600,1.2)],[{'t':'ribbon','c':0,'x0':CX,'y0':300,'x1':1250,'y1':520,'dur':1.4},{'t':'ribbon','c':1,'x0':CX,'y0':300,'x1':30,'y1':520,'dur':1.4}],rgb='120,140,220'),'cool',cues=['शब्द','नदी'])
add(15,1,0,C([br(CX,600,1.3,dark=.7)],rgb='100,100,160'),'dark',cam=Z(1.0,1.1,0,0,0,-10))
add(15,1,.5,C([],[{'t':'dim','ga':.5},txt('थका',CX,360,120,0,glow='rgba(160,170,230,.8)')],rgb='80,80,140',spin=0),'dark',cues=['थका'])
add(15,2,0,C([ri(0,360,660,1.0,flip=-1,dark=.3,pose='stand'),ri(1,520,660,1.0,flip=-1,dark=.3),ri(2,760,660,1.0,dark=.3),ri(3,920,660,1.0,dark=.3)],[],rgb='120,110,180'),'dark',cues=['ठुकरा'])
add(15,2,.38,C([br(CX,620,1.3,aura='255,70,60')],[],rgb='200,70,70'),'red',cam=Z(1.0,1.1,0,0,0,-14))
add(15,2,.7,O([F('vishnu_rest',CX+20,620,1.1)],[{'t':'waterfront','y':560}],gold=1,oy=560,gy=300),'cool')
# ================= B16: "maybe I should quit" =================
add(16,0,0,Y([hd('brahma',CX,470,2.5,expr=CLS)],fire=.2),'dark',cam=Z(1.0,1.1,0,0,0,-12))
add(16,0,.55,O([br(CX,520,.8,ds=-.04)],oy=470,rgb='90,110,180'),'dark',cam=Z(1.0,1.05,0,0,0,0))
# ================= B17: the white-gold pillar =================
add(17,0,0,{'bg':bg('palace'),'figs':[vi(380,665,1.4)],'fx':[{'t':'pillar','x':960,'y0':80,'y1':600,'w':76,'c':0,'d':.8}]},'cool',cues=['खंभे'])
add(17,0,.38,{'bg':bg('palace'),'figs':[],'fx':[{'t':'pillar','x':CX,'y0':40,'y1':620,'w':120}]},'warm',cam=Z(1.0,1.12,0,0,0,-24))
add(17,0,.7,C([],[{'t':'pillar','x':CX,'y0':60,'y1':600,'w':90},{'t':'sparkle','x':CX,'y':330,'n':30,'rx':200,'ry':260}],rgb='255,235,190'),'amb')
add(17,1,0,W([hd('vishnu',CX,440,2.5)],warm=False),'cool',cam=Z(1.0,1.08,0,0,0,-8))
add(17,1,.6,C([],[txt('महादेव',CX,360,150,0,glow='rgba(150,170,255,.9)',d=.9)],rgb='120,130,230'),'night',cues=['महादेव'])
# ================= B18: Brahma doubts =================
add(18,0,0,Y([hd('brahma',CX,470,2.2)],fire=.2),'dark')
add(18,1,0,C([],[{'t':'sparkle','x':CX,'y':340,'n':44,'rx':520,'ry':200},{'t':'infinity','x':CX,'y':340,'c':0,'d':.6},txt('अमर जीव',CX,560,80,1,d=.7)],rgb='255,200,130'),'amb',cues=['अमर','जीव'])
add(18,1,.35,V([sh(CX,670,1.5,dark=.35,key='255,120,70')],[{'t':'flames','x':CX-300,'y':700,'sc':1.2,'c':0},{'t':'flames','x':CX+300,'y':700,'sc':1.2,'c':0}],rgb='255,70,30'),'red',cues=['विनाश'])
add(18,1,.72,Y([hd('brahma',CX,470,2.4)],fire=.2),'dark',cam=Z(1.0,1.1,0,0,0,-10))
# ================= B19: "go to Mahadeva" =================
add(19,0,0,Y([vi(CX,665,1.55)],fire=.25),'cool')
add(19,0,.55,Y([hd('vishnu',CX,440,2.6)],fire=.25),'cool',cam=Z(1.0,1.08,0,0,0,-8))
add(19,1,0,Y([vi(400,665,1.5,pose='point')],fire=.25),'cool',cues=['जाइए'])
add(19,1,.55,Y([br(CX,640,1.5,aura='255,225,170')],fire=.25),'warm')
# ================= B20: Brahma finds Shiva meditating =================
add(20,0,0,C([br(300,560,1.0,vx=40)],[{'t':'ribbon','c':0,'x0':0,'y0':500,'x1':300,'y1':540,'dur':1.0}],rgb='150,160,240'),'cool')
add(20,0,.55,K([sh(CX,650,1.25,expr=CLS)]),'night',cam=Z(1.0,1.08,0,0,0,-8))
add(20,1,0,K([br(230,640,1.0),sh(900,650,1.1,expr=CLS,flip=-1)]),'night')
add(20,1,.5,K([hd('shiva',CX,470,2.3,expr=CLS)]),'night',cam=Z(1.0,1.08,0,0,0,-8))
add(20,2,0,K([br(CX,650,1.25)]),'cool',cues=['बैठ'])
add(20,2,.35,K([hd('brahma',CX,470,2.2,expr=CLS)]),'night',cam=Z(1.0,1.1,0,0,0,-10))
add(20,2,.68,K([br(CX,650,1.25,aura='255,230,170')],[{'t':'glow','x':CX,'y':240,'r':440,'rgb':'255,235,190','ga':.5}]),'warm')
# ================= B21: the prayer is answered =================
add(21,0,0,K([br(CX,650,1.25)],mx=.18),'night',cam=Z(1.0,1.06,0,0,0,0))
add(21,0,.55,C([br(CX,600,1.2)],[],rgb='120,140,230',spin=.5),'night')
add(21,1,0,K([hd('shiva',CX,470,2.6,expr=CLS)]),'night',cam=Z(1.0,1.08,0,0,0,-8))
add(21,1,.55,K([sh(CX+80,650,1.35),br(260,660,.95)],[{'t':'glow','x':CX+80,'y':380,'r':340,'rgb':'180,200,255','ga':.25}]),'cool',cues=['खोल'])
add(21,2,0,K([hd('shiva',CX,470,2.7)]),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(21,3,0,K([hd('brahma',CX,470,2.5)]),'night')
add(21,3,.3,K([br(CX,650,1.4)],[],mx=.22),'cool',cam=Z(1.0,1.1,0,0,0,-10))
add(21,3,.62,C([],[txt('मैं कहाँ चूका?',CX,360,100,0,d=.8)],rgb='130,140,230'),'night')
add(21,3,.82,K([hd('brahma',CX,470,2.9,expr=CLS)]),'dark',cam=Z(1.0,1.12,0,0,0,-14))
# ================= B22: "you need Shakti" =================
add(22,0,0,K([hd('shiva',CX,470,2.5)]),'cool',cam=Z(1.0,1.08,0,0,0,-8))
add(22,0,.55,K([sh(CX+100,650,1.35),br(250,660,.95)]),'night')
add(22,1,0,C([],[txt('शक्ति',CX,360,200,0,glow='rgba(255,200,120,.95)',d=.8),{'t':'sparkle','x':CX,'y':380,'n':36,'rx':420,'ry':220}],rgb='255,190,120'),'amb',cues=['शक्ति'])
add(22,2,0,K([hd('brahma',CX,470,2.4)],[txt('?',CX,230,180,0,d=.5)]),'cool')
add(22,3,0,C([],[{'t':'glow','x':CX,'y':380,'r':520,'rgb':'255,170,200','ga':.5},txt('नारी की शक्ति',CX,400,100,0,glow='rgba(255,170,200,.95)',d=.8)],rgb='255,170,200'),'warm',cues=['नारी'])
# ================= B23: Ardhanarishwara =================
add(23,0,0,K([sh(CX+60,650,1.4),br(250,660,.95)]),'night')
add(23,0,.55,K([hd('brahma',CX,470,2.3)],[{'t':'sparkle','x':CX,'y':330,'n':24,'rx':380,'ry':220}]),'cool')
add(23,1,0,K([sh(CX,650,1.4,aura='255,220,170')],[{'t':'flash','c':0,'w':.4,'rgb':'255,230,190'},{'t':'sparkle','x':CX,'y':380,'n':40,'rx':320,'ry':260}]),'warm',cues=['बदलने'])
add(23,2,0,K([F('ardha',CX,665,1.5,aura='255,215,150')],[{'t':'glow','x':CX,'y':220,'r':440,'rgb':'255,235,190','ga':.5}]),'warm',cues=['दाईं'])
add(23,2,.3,K([F('ardha',CX,665,1.5,aura='255,215,150')],[{'t':'glow','x':CX-200,'y':380,'r':300,'rgb':'255,170,190','ga':.35}]),'warm',cues=['बाईं'])
add(23,3,0,C([F('ardha',CX,675,1.65)],[txt('शिव',CX+330,170,70,0),txt('शक्ति',CX-330,170,70,1)],rgb='200,160,255'),'amb',cues=['विपरीत','एक'])
add(23,3,.5,C([hd('ardha',CX,450,2.4)],[{'t':'sparkle','x':CX,'y':330,'n':30,'rx':360,'ry':220}],rgb='255,200,170'),'amb')
add(23,4,0,C([F('ardha',CX,680,1.7,aura='255,215,150')],[txt('अर्धनारीश्वर',CX,160,110,0,d=1.0),{'t':'sparkle','x':CX,'y':400,'n':40,'rx':520,'ry':260}],rgb='255,200,150'),'amb',cues=['अर्धनारीश्वर'])
# ================= B24: Brahma in awe =================
add(24,0,0,K([hd('brahma',CX,470,2.3)]),'cool')
add(24,0,.5,K([br(250,660,.95),F('ardha',CX+120,665,1.55,aura='255,215,150')]),'warm')
add(24,1,0,C([hd('ardha',CX,450,2.6)],[],rgb='255,200,170'),'amb',cam=Z(1.0,1.1,0,0,0,-12))
add(24,1,.5,K([hd('brahma',CX,470,2.6)],[{'t':'sparkle','x':CX,'y':330,'n':24,'rx':380,'ry':220}]),'warm')
add(24,2,0,K([hd('brahma',CX-140,470,2.6),F('ardha',CX+300,665,1.3,aura='255,215,150')],[{'t':'ribbon','c':0,'x0':CX+280,'y0':380,'x1':CX-40,'y1':440,'dur':1.4}]),'warm',cues=['फुसफुसा'])
# ================= B25: the secret of creation =================
add(25,0,0,C([F('ardha',CX,675,1.65,aura='255,215,150')],rgb='255,200,150'),'amb')
add(25,0,.5,C([sh(300,670,1.2),ad(980,670,1.2,flip=-1)],[txt('स्थिर',300,110,60,0),txt('गतिशील',980,110,60,1)],rgb='200,170,255'),'amb',cues=['स्थिर','गतिशील'])
add(25,1,0,C([ad(340,675,1.4,aura='255,200,200'),sh(940,675,1.4,flip=-1)],[txt('स्त्री',340,180,70,0),txt('पुरुष',940,180,70,1)],rgb='200,170,255'),'night',cues=['स्त्री','पुरुष'])
add(25,1,.55,C([sh(CX,670,1.5,dark=.7)],[{'t':'dim','ga':.3}],rgb='120,110,180',spin=0),'dark')
add(25,2,0,C([F('ardha',CX,675,1.65,aura='255,215,150')],[{'t':'sparkle','x':CX,'y':400,'n':40,'rx':520,'ry':260}],rgb='255,200,150'),'amb',cues=['मिलेंगे'])
add(25,2,.55,C([],[{'t':'infinity','x':CX,'y':340,'c':0,'d':.8}],rgb='255,200,150',spin=.2),'amb',cues=['अंत'])
add(25,3,0,C([ad(CX,680,1.7,aura='255,215,150')],[{'t':'glow','x':CX,'y':220,'r':460,'rgb':'255,225,190','ga':.5}],rgb='255,190,160'),'amb',cues=['आदिशक्ति'])
add(25,3,.55,C([hd('adishakti',CX,450,2.5)],[{'t':'sparkle','x':CX,'y':330,'n':40,'rx':420,'ry':240}],rgb='255,190,170'),'amb',cues=['माता'])
# ================= B26: Brahma's blessing =================
add(26,0,0,K([hd('brahma',CX,470,2.4,expr=CLS)]),'warm',cam=Z(1.0,1.08,0,0,0,-8))
add(26,0,.5,C([br(300,650,1.1),ad(900,670,1.35,flip=-1,aura='255,215,150')],[],rgb='255,200,170'),'amb')
add(26,1,0,C([],[{'t':'outline','x':440,'y':520,'sc':1.2,'c':0,'d':1.0},{'t':'outline','x':840,'y':520,'sc':1.2,'c':1,'d':1.0}],rgb='255,200,160'),'amb',cues=['पहला','जोड़ा'])
add(26,1,.6,K([hd('brahma',CX,470,2.5)]),'warm')
add(26,2,0,C([hd('adishakti',CX,450,2.6)],[{'t':'sparkle','x':CX,'y':330,'n':26,'rx':360,'ry':220}],rgb='255,190,170'),'amb')
add(26,2,.55,C([ad(CX+200,670,1.35,aura='255,215,150',flip=-1),br(300,650,1.0)],[{'t':'ribbon','c':0,'x0':CX+120,'y0':400,'x1':330,'y1':420,'dur':1.4}],rgb='255,200,160'),'amb',cues=['दे'])
add(26,3,0,C([br(CX,640,1.4,aura='255,215,140')],[{'t':'sparkle','x':CX,'y':380,'n':40,'rx':420,'ry':260}],rgb='255,200,140'),'amb')
add(26,3,.5,C([hd('brahma',CX,470,2.7)],[{'t':'glow','x':CX,'y':380,'r':360,'rgb':'255,215,140','ga':.4}],rgb='255,200,140'),'amb')
# ================= B27: Manu and Brahmi =================
add(27,0,0,C([br(CX,640,1.4,aura='255,215,140')],[{'t':'glow','x':CX,'y':380,'r':420,'rgb':'255,225,170','ga':.5},{'t':'sparkle','x':CX,'y':400,'n':30,'rx':260,'ry':200}],rgb='255,200,140'),'amb')
add(27,0,.55,C([],[{'t':'outline','x':520,'y':520,'sc':1.2,'c':0,'d':.8},{'t':'outline','x':760,'y':520,'sc':1.2,'c':1,'d':.8},{'t':'sparkle','x':CX,'y':420,'n':30,'rx':260,'ry':200}],rgb='255,210,150'),'amb')
add(27,1,0,G([ma(480,665,1.45),bh(800,665,1.45,flip=-1)]),'warm',cam=Z(1.0,1.08,0,0,0,-8))
add(27,1,.38,G([hd('manu',CX,440,2.5)],[txt('मनु',CX,170,100,0,d=.7)]),'warm',cues=['मनु'])
add(27,1,.7,G([hd('brahmi',CX,440,2.5)],[txt('ब्राह्मी',CX,170,100,0,d=.7)]),'warm',cues=['ब्राह्मी'])
add(27,2,0,G([ma(300,665,1.0),bh(450,665,1.0),ma(780,665,.85),bh(920,665,.85),ma(1090,665,.75)],[{'t':'sparkle','x':CX,'y':380,'n':30,'rx':520,'ry':200}]),'warm',cues=['मनुष्य'])
# ================= B28: Brahma rejoices =================
add(28,0,0,G([hd('brahma',CX,470,2.5)]),'warm',cam=Z(1.0,1.08,0,0,0,-8))
add(28,0,.46,G([ma(430,665,1.5),bh(850,665,1.5,flip=-1)],[{'t':'glow','x':CX,'y':380,'r':520,'rgb':'255,225,170','ga':.35}]),'warm',cues=['सबसे'])
add(28,1,0,W([br(CX,640,1.5,aura='255,225,160')],[{'t':'sparkle','x':CX,'y':380,'n':40,'rx':480,'ry':260}]),'warm')
add(28,1,.6,{'bg':bg('dawn'),'figs':[],'fx':[{'t':'glow','x':CX,'y':220,'r':480,'rgb':'255,235,190','ga':.5},{'t':'sparkle','x':CX,'y':420,'n':40,'rx':540,'ry':240}]},'warm')
add(28,2,0,G([ma(520,665,1.2),bh(760,665,1.2,flip=-1)],[{'t':'sparkle','x':CX,'y':400,'n':30,'rx':520,'ry':200}]),'warm',cam=Z(1.08,1.0,0,0,0,0))
# ================= B29: the curse remembered =================
add(29,0,0,G([hd('brahma',CX,470,2.4)]),'warm')
add(29,0,.55,C([br(CX,600,1.3,dark=.8)],[{'t':'dim','ga':.3}],rgb='120,110,170',spin=0),'dark')
add(29,1,0,V([F('narada',CX,680,1.5,dark=.3,key='255,70,60')],[{'t':'icon','i':'vortex','x':CX,'y':300,'sc':3.2,'c':0,'d':1.0}],rgb='160,30,50'),'red',cues=['श्राप'],shake=3)
add(29,2,0,V([],[txt('तुम उसकी इच्छा करोगे…',CX,330,86,0,glow='rgba(255,70,50,.9)',d=1.0)],rgb='160,30,50'),'red',cues=['इच्छा'])
add(29,2,.55,V([hd('brahma',CX,470,2.6)],[txt('जिसकी इच्छा नहीं करनी चाहिए',CX,200,60,0,d=1.0)],rgb='160,30,50'),'red',cues=['जिसकी'])
add(29,3,0,{'bg':bg('storm',r=1),'figs':[],'fx':[{'t':'crack','x':CX,'c':0,'d':.8},txt('सच होने वाले थे',CX,360,100,0,glow='rgba(255,70,50,.95)',d=1.1)]},'red',cues=['सच'],shake=3)
# ================= B30: closing card =================
add(30,0,0,C([],[txt('आगे क्या हुआ, जानने के लिए…',CX,300,66,0,glow='rgba(255,215,150,.9)',d=1.0),{'t':'sparkle','x':CX,'y':360,'n':40,'rx':520,'ry':220}],rgb='255,200,150',spin=.05),'amb',cues=['आगे'],dx=.8)
add(30,0,.55,C([],[txt('मिलते हैं अगले एपिसोड में',CX,340,74,0,glow='rgba(255,215,150,.9)',d=1.0),{'t':'sparkle','x':CX,'y':360,'n':40,'rx':520,'ry':220}],rgb='255,200,150',spin=.05),'amb',cues=['मिलते'])

# ---- library (Gemini) objects/effects replace the coded icons, red crack lines and crooked flee poses ----
_A='../library/pilot/assets/';_IC={'cycle':('sudarshan_chakra',88,{'spin':1.4}),'vortex':('energy_swirl',70,{'spin':1.0}),'flame':('fire_small',60,{}),'frost':('snow_flakes',70,{}),'light':('divine_rays',80,{}),'lotusI':('lotus_pond_leaf',70,{}),'trident':('trident_plain',40,{})}
_bn=[0]
def _libfx(x):
    t=x.get('t')
    if t=='icon' and x['i'] in _IC:
        n,w,k=_IC[x['i']];e={'t':'fximg','src':_A+'fx_'+n+'.png','x':x['x'],'y':x['y'],'w':w*x.get('sc',1),'blend':'lighter','c':x.get('c',0),'d':x.get('d',1)};e.update(k);return [e]
    if t=='scales':return [{'t':'fximg','src':_A+'fx_magic_circle.png','x':x['x'],'y':x['y']+40,'w':300,'blend':'lighter','c':x.get('c',0),'d':x.get('d',1),'spin':.3},{'t':'fximg','src':_A+'fx_light_beam.png','x':x['x'],'y':x['y']+120,'w':260,'blend':'lighter','alpha':.7,'c':x.get('c',0),'d':x.get('d',1)}]
    if t=='crack':
        _bn[0]+=1;n=['lightning_bolt_a','lightning_bolt_b','lightning_forks'][_bn[0]%3]
        return [{'t':'fximg','src':_A+'fx_'+n+'.png','x':x['x'],'y':230,'w':300,'blend':'lighter','alpha':.9,'c':x.get('c',0),'d':x.get('d',.6)}]
    return [x]
for _s in film.shots:
    _sc=_s.get('sc')
    if not _sc:continue
    _sc['fx']=[y for x in _sc.get('fx',[]) for y in _libfx(x)]
    for _g in _sc.get('figs',[]):
        if _g.get('pose')=='flee':_g.pop('pose')
print(film.save(os.path.join(HERE,'shots.json')),'shots')
