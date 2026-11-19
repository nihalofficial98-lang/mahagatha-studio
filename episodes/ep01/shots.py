"""EP1 shot list: सृष्टि का जन्म और मधु-कैटभ (same script as before, new visuals). Shots start on spoken lines / words (timings from build/ep01/timings.json)."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'));sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','ep03'))
from shotkit import *
import lines as LN
HERE=os.path.dirname(os.path.abspath(__file__));D=LN.load('ep01');film=Film()
def T(b,l,x=0.0):
    L=D[b]['lines'][l]
    if isinstance(x,str):
        ws=D[b]['words'][L['w0']:L['w0']+L['n']]
        for w in ws:
            if w['text'].strip('"“”।,.…!?:').startswith(x):return round(w['start'],2)
        raise KeyError((b,l,x))
    return round(L['start']+x*(L['end']-L['start']),2)
def add(b,l,x,sc,grade='cel',**k):film.add(b,0 if (l==0 and x==0) else T(b,l,x),sc,grade,**k)
# --- scene builders ---
def Vd(figs=(),fx=(),a=.2):return {'bg':bg('plain',cols=['#000000','#03030a']),'figs':list(figs),'fx':list(fx)}
def O(figs=(),fx=(),gold=0,oy=560,rgb='150,180,255',gy=340,ga=.2):return {'bg':bg('cosmicsea',gold=gold,oy=oy,rgb=rgb,gy=gy,ga=ga),'figs':list(figs),'fx':list(fx)}
def C(figs=(),fx=(),rgb='160,120,255',spin=.05):return {'bg':bg('cosmos',rgb=rgb,spin=spin),'figs':list(figs),'fx':list(fx)}
def R(figs=(),fx=(),r=.6):return {'bg':bg('storm',r=r),'figs':list(figs),'fx':list(fx)}
def VR(figs=(),fx=(),rgb='255,60,30'):return {'bg':bg('voidR',rgb=rgb),'figs':list(figs),'fx':list(fx)}
def W(figs=(),fx=(),warm=True):return {'bg':bg('cel',warm=warm),'figs':list(figs),'fx':list(fx)}
def DW(figs=(),fx=()):return {'bg':bg('dawn'),'figs':list(figs),'fx':list(fx)}
WF=lambda y=600:{'t':'waterfront','y':y}
# --- cast ---
ANG={'brow':-.95};CLS={'eye':.2}
def vi(x,y=650,s=1.25,**k):return F('vishnu',x,y,s,**k)
def vr(x,y=620,s=1.1,**k):return F('vishnu_rest',x,y,s,**k)
def hy(x,y=650,s=1.25,**k):return F('hayagriva',x,y,s,**k)
def br(x,y=620,s=1.1,**k):return F('brahma',x,y,s,**k)
def mk(x,y=650,s=1.3,**k):return F('madhu',x,y,s,**k)
def kt(x,y=650,s=1.3,**k):return F('kaitabha',x,y,s,**k)
def sh(x,y=650,s=1.25,**k):return F('shiva',x,y,s,**k)
def ni(x,y=650,s=1.25,**k):return F('adishakti',x,y,s,dark=.75,aura='150,110,255',**k)
def hd(who,x=CX,y=440,s=2.3,**k):return F(who,x,y,s,head=True,**k)
def txt(s,x,y,size,c=0,glow='rgba(255,220,150,.8)',d=.7):return {'t':'text','s':s,'x':x,'y':y,'size':size,'c':c,'d':d,'glow':glow}
def orb(x,y,r,rgb,ga=.5):return {'t':'glow','x':x,'y':y,'r':r,'rgb':rgb,'ga':ga}
def spk(x,y,n=30,rx=300,ry=200):return {'t':'sparkle','x':x,'y':y,'n':n,'rx':rx,'ry':ry}
Z=cam
# ================= B01: nothing existed =================
add(1,0,0,Vd(),'dark',dx=1.2)
add(1,0,'आसमान',Vd([],[txt('न आसमान, न धरती',CX,330,70,0,glow='rgba(180,190,255,.7)',d=1.0)]),'dark',cues=['आसमान'])
add(1,0,'सूरज',Vd([],[txt('न सूरज, न चाँद',CX,330,70,0,glow='rgba(180,190,255,.7)',d=1.0)]),'dark',cues=['सूरज'])
add(1,0,'दिन',Vd([],[txt('न दिन, न रात',CX,330,70,0,glow='rgba(180,190,255,.7)',d=1.0)]),'dark',cues=['दिन'])
add(1,1,0,Vd([],[txt('न कोई आवाज़',CX,330,70,0,glow='rgba(180,190,255,.7)',d=1.0)]),'dark',cues=['आवाज़'])
add(1,2,0,Vd([],[txt('कुछ भी नहीं',CX,340,120,0,glow='rgba(200,210,255,.9)',d=.9)]),'dark',cues=['कुछ'])
add(1,3,0,Vd([],[orb(CX,360,60,'255,235,190',.0)]),'dark')
add(1,3,'पहली',Vd([],[orb(CX,360,120,'255,235,190',.7),{'t':'sparkle','x':CX,'y':360,'n':14,'rx':60,'ry':60}]),'dark',cues=['पहली'])
add(1,3,'हिला',Vd([],[orb(CX,360,300,'255,225,170',.8),{'t':'shock','x':CX,'y':360,'c':0,'rgb':'255,235,190','max':700},{'t':'shock','x':CX,'y':360,'c':0,'rgb':'255,235,190','max':1000}]),'amb',cues=['हिला'])
# ================= B02: today's story =================
add(2,0,0,C([],[orb(CX,340,380,'255,215,150',.55),spk(CX,340,30,360,200)],rgb='255,200,130'),'amb',dx=.9)
add(2,0,'जन्म',C([],[orb(CX,340,560,'255,225,170',.8),{'t':'shock','x':CX,'y':340,'c':0,'rgb':'255,225,170','max':1100}],rgb='255,210,150',spin=.3),'amb',cues=['जन्म'])
add(2,0,'ख़तरे',R([],[orb(CX,380,420,'255,60,50',.35)],r=1),'red')
add(2,0,'पैदा',VR([],[{'t':'glow','x':CX-120,'y':330,'r':60,'rgb':'255,60,40','ga':.9},{'t':'glow','x':CX+120,'y':330,'r':60,'rgb':'255,60,40','ga':.9}],rgb='80,10,10'),'dark',cam=Z(1.0,1.08,0,0,0,0))
# ================= B03: Parabrahma =================
add(3,0,0,C([],[orb(CX,340,300,'255,235,200',.6)],rgb='255,225,170',spin=0),'amb',dx=.9)
add(3,0,'परब्रह्म',C([],[orb(CX,340,420,'255,235,200',.8),txt('परब्रह्म',CX,560,110,0,d=.9)],rgb='255,225,170',spin=0),'amb',cues=['परब्रह्म'])
add(3,1,0,C([],[{'t':'infinity','x':CX,'y':340,'c':0,'d':.8},orb(CX,340,360,'255,230,190',.4)],rgb='255,220,170',spin=.02),'amb',cues=['आदि'])
add(3,1,'रूप',C([],[orb(CX-200,340,200,'255,200,120',.5),orb(CX+200,340,200,'160,180,255',.5)],rgb='255,220,170',spin=.1),'amb')
add(3,1,'विचारों',C([],[{'t':'ribbon','c':0,'x0':-100,'y0':200,'x1':CX,'y1':340,'dur':1.2},{'t':'ribbon','c':1,'x0':1380,'y0':500,'x1':CX,'y1':340,'dur':1.2},orb(CX,340,300,'255,235,200',.5)],rgb='200,180,255',spin=.1),'amb',cues=['विचारों','इंद्रियों'])
add(3,2,0,C([],[orb(CX,340,340,'255,235,200',.6),spk(CX,340,60,300,220)],rgb='255,225,170',spin=.1),'amb')
add(3,3,0,C([],[orb(CX,340,400,'255,235,200',.7)],rgb='255,225,170',spin=0),'amb')
add(3,3,'इच्छा',C([],[orb(CX,340,520,'255,225,160',.8),{'t':'shock','x':CX,'y':340,'c':0,'rgb':'255,225,170','max':900},txt('इच्छा',CX,580,100,0,d=.8)],rgb='255,215,150',spin=.2),'amb',cues=['इच्छा','इच्छा'])
# ================= B04: Om =================
add(4,0,0,C([],[{'t':'shock','x':CX,'y':340,'c':0,'rgb':'255,225,170','max':700},{'t':'shock','x':CX,'y':340,'c':1,'rgb':'255,225,170','max':1000}],rgb='255,215,150',spin=.1),'amb',cues=['कंपन','पैदा'],dx=.8)
add(4,0,'ध्वनि',C([],[{'t':'ribbon','c':0,'x0':-100,'y0':340,'x1':CX,'y1':340,'dur':1.0},{'t':'ribbon','c':1,'x0':1380,'y0':340,'x1':CX,'y1':340,'dur':1.0},orb(CX,340,360,'255,225,170',.5)],rgb='255,215,150'),'amb',cues=['ध्वनि','ध्वनि'])
add(4,1,0,C([],[txt('ॐ',CX,400,320,0,glow='rgba(255,210,120,.95)',d=.5),{'t':'flash','c':0,'w':.3,'rgb':'255,225,170'},{'t':'shock','x':CX,'y':340,'c':0,'rgb':'255,225,170','max':1200}],rgb='255,210,130'),'amb',cues=['ॐ'])
add(4,2,0,C([],[txt('ॐ',CX,400,240,0,glow='rgba(255,210,120,.9)',d=.5),spk(CX,360,60,520,260)],rgb='255,210,130',spin=.15),'amb')
# ================= B05: three gunas + five elements =================
add(5,0,0,C([],[{'t':'gunas','x':CX,'c':0,'hi':None}],rgb='200,160,255'),'night',cues=['सत्व','रजस','तमस'],dx=.7)
add(5,0,'सत्व',C([],[{'t':'gunas','c':0,'hi':0,'all':True}],rgb='255,250,230'),'cool',cues=['सत्व'])
add(5,0,'रजस',C([],[{'t':'gunas','c':0,'hi':1,'all':True}],rgb='255,120,90'),'red',cues=['रजस'])
add(5,0,'तमस',C([],[{'t':'gunas','c':0,'hi':2,'all':True}],rgb='120,90,190'),'dark',cues=['तमस'])
add(5,1,0,C([],[orb(CX,340,420,'255,235,200',.6),spk(CX,340,40,320,200)],rgb='255,225,170'),'amb',cues=['मेल'])
add(5,1,'वायु',C([],[{'t':'element','type':'vayu','x':CX,'y':330,'label':'वायु'}],rgb='170,210,255'),'cool')
add(5,1,'जल',C([],[{'t':'element','type':'jal','x':CX,'y':320,'label':'जल'}],rgb='120,170,255'),'cool')
add(5,1,'पृथ्वी',C([],[{'t':'element','type':'prithvi','x':CX,'y':330,'label':'पृथ्वी'}],rgb='160,200,120'),'earth')
add(5,1,'अग्नि',C([],[{'t':'element','type':'agni','x':CX,'y':330,'label':'अग्नि'}],rgb='255,140,70'),'red')
add(5,1,'आकाश',C([],[{'t':'element','type':'akash','x':CX,'y':330,'label':'आकाश'}],rgb='180,160,255'),'void')
# ================= B06: Narayana on the waters =================
add(6,0,0,O([],[],oy=520,gy=360),'night',cam=Z(1.0,1.1,0,0,0,-14),dx=.9)
add(6,0,'अथाह',O([],[],oy=500,gy=320,ga=.3),'night',cam=Z(1.1,1.0,0,0,0,0))
add(6,0,'तैर',O([vr(CX,640,.7)],[WF(590)],gold=.6,oy=560),'amb',cam=Z(1.0,1.08,0,0,0,0))
add(6,1,'नर',O([],[txt('नर = जल',CX,300,100,0,d=.8)],oy=520),'night',cues=['नर'])
add(6,1,'अयन',O([],[txt('अयन = ठिकाना',CX,300,100,0,d=.8)],oy=520),'night',cues=['अयन'])
add(6,1,'जिसका',O([vr(CX,640,1.05)],[WF(600)],gold=.8,oy=560),'amb',cam=Z(1.0,1.08,0,0,0,-8))
add(6,2,0,O([vr(CX,650,1.4,aura='255,215,140')],[WF(610),txt('नारायण',CX,170,120,0,d=.9)],gold=1,oy=570),'amb',cues=['नारायण'],cam=Z(1.0,1.1,0,0,0,-12))
# ================= B07: egg, lotus, Brahma =================
add(7,0,0,O([vr(CX,640,.95)],[WF(600),{'t':'sparkle','x':CX,'y':420,'n':30,'rx':180,'ry':120}],gold=.8,oy=560),'amb',dx=.8)
add(7,0,'बीज',O([vr(CX-300,640,.9)],[WF(600),orb(CX+200,300,80,'255,215,110',.9),{'t':'shock','x':CX+200,'y':560,'c':0,'rgb':'255,225,150','max':500}],gold=.6,oy=560),'amb',cues=['बीज'])
add(7,0,'अंडा',O([vr(CX-340,640,.8)],[WF(600),{'t':'egg','x':CX+200,'y':330,'sc':.9,'c':0,'d':1.2}],gold=.8,oy=560),'amb',cues=['अंडा'])
add(7,0,'हिरण्यगर्भ',O([],[{'t':'egg','x':CX,'y':330,'sc':1.5},txt('हिरण्यगर्भ',CX,640,90,0,d=.8),WF(620)],gold=1,oy=580),'amb',cues=['हिरण्यगर्भ'],cam=Z(1.0,1.08,0,0,0,-10))
add(7,1,0,O([vr(CX-340,640,.8,fo=0,fd=3.0)],[{'t':'egg','x':CX+160,'y':330,'sc':1.3},WF(600),{'t':'sparkle','x':CX,'y':330,'n':30,'rx':260,'ry':200}],gold=1,oy=560),'amb',cues=['विष्णु'])
add(7,2,0,O([vr(CX,650,1.5)],[WF(640),{'t':'lotus','x':CX-30,'y':470,'sc':.35,'c':0,'d':1.5}],gold=1,oy=590),'amb',cues=['कमल'],cam=Z(1.0,1.12,0,0,0,-18))
add(7,2,'कमल',O([],[{'t':'lotus','x':CX,'y':560,'sc':1.1,'c':0,'d':1.2},{'t':'glow','x':CX,'y':380,'r':420,'rgb':'255,200,220','ga':.35},WF(640)],gold=.8,oy=590),'amb',cues=['खिला'])
add(7,2,'चौदह',O([],[{'t':'lotus','x':CX,'y':560,'sc':1.1,'open':1},txt('१४ पंखुड़ियाँ',CX,170,90,0,d=.8),WF(640)],gold=.8,oy=590),'amb',cues=['चौदह'])
add(7,2,'कमंडल',O([br(CX,620,1.35,ac=0,ad=1.0,aura='255,225,170')],[WF(640)],gold=1,oy=590),'amb',cues=['कमंडल'])
add(7,2,'ब्रह्मा',O([br(CX,620,1.5,aura='255,225,170')],[WF(640),spk(CX,360,36,300,220)],gold=1,oy=590),'amb',cam=Z(1.0,1.1,0,0,0,-10))
add(7,2,'रचयिता',O([br(CX-180,640,1.0),vr(CX+300,650,.7)],[WF(620),txt('रचयिता',CX,150,90,0,d=.9)],gold=1,oy=570),'amb',cues=['रचयिता'])
# ================= B08: the egg splits =================
add(8,0,0,O([br(CX,500,.6,aura='255,225,170')],[{'t':'egg','x':CX,'y':400,'sc':1.3}],gold=1,oy=620),'amb',dx=.7)
add(8,0,'सीप',O([],[{'t':'egg','x':CX,'y':380,'sc':1.7},spk(CX,380,34,300,260)],gold=1,oy=620),'amb',cam=Z(1.0,1.1,0,0,0,-10))
add(8,0,'दो',O([],[{'t':'egg','x':CX,'y':380,'sc':1.7,'cc':0,'cd':1.0}],gold=1,oy=620),'amb',cues=['दो'],shake=2)
add(8,1,0,O([],[{'t':'egg','x':CX,'y':390,'sc':1.7,'crack':1,'sc2':0,'sd':1.2},{'t':'flash','c':0,'w':.4,'rgb':'255,240,200'}],gold=1,oy=620),'amb',cues=['ऊपर'])
add(8,1,'स्वर्ग',{'bg':bg('dawn'),'figs':[],'fx':[txt('स्वर्ग',CX,200,150,0,d=.9),spk(CX,230,40,500,100)]},'warm',cues=['स्वर्ग'])
add(8,1,'नीचे',O([],[txt('पृथ्वी',CX,300,150,0,d=.9)],gold=.4,oy=520),'earth',cues=['पृथ्वी'])
add(8,1,'आकाश',{'bg':bg('cel',warm=False),'figs':[],'fx':[spk(CX,360,50,520,260)]},'cool')
# ================= B09: the Vedas =================
add(9,0,0,W([br(CX,640,1.2)],[]),'warm',cam=Z(1.0,1.08,0,0,0,-8),dx=.7)
add(9,0,'मौन',{'bg':bg('cel',warm=True),'figs':[hd('brahma',CX,450,2.2,expr=CLS)],'fx':[]},'warm',cam=Z(1.0,1.1,0,0,0,-10))
add(9,0,'ध्यान',C([br(CX,640,1.3,aura='255,225,170')],[orb(CX,360,420,'255,220,160',.5),spk(CX,360,36,300,220)],rgb='255,215,150'),'amb')
add(9,0,'प्रकट',C([br(CX,700,1.0,aura='255,225,170')],[{'t':'books','x':CX,'y':250,'c':0,'gap':260},orb(CX,300,420,'255,225,160',.4)],rgb='255,215,150'),'amb',cues=['ऋग्वेद','यजुर्वेद','सामवेद','अथर्ववेद'])
add(9,0,'सामवेद',C([],[{'t':'books','x':CX,'y':340,'c':0,'gap':260},orb(CX,340,500,'255,225,160',.4)],rgb='255,215,150'),'amb',cues=['सामवेद','अथर्ववेद'])
add(9,1,0,W([hd('brahma',CX,450,2.4)],[]),'warm',cam=Z(1.0,1.1,0,0,0,-10))
add(9,1,'सब',O([br(CX,620,1.1,aura='255,225,170')],[WF(640)],gold=.8,oy=570),'amb',cam=Z(1.08,1.0,0,0,0,0))
add(9,2,0,O([],[WF(600)],oy=520,gold=0,rgb='150,60,60',ga=.3),'dark',cam=Z(1.0,1.08,0,0,0,0))
# ================= B10: Madhu and Kaitabha are born =================
add(10,0,0,O([vr(CX,650,1.5)],[WF(640),{'t':'books','x':CX+300,'y':220,'c':0,'gap':110}],gold=.6,oy=590),'dark',cues=['वेद'],cam=Z(1.0,1.1,0,0,0,-12))
add(10,0,'कान',O([hd('vishnu',CX,430,2.4,expr=CLS)],[],gold=.4,oy=590),'dark',cam=Z(1.0,1.1,0,0,0,-10))
add(10,0,'रेंगती',O([hd('vishnu',CX-120,430,2.2,expr=CLS),mk(CX+300,520,.55),kt(CX+420,540,.5)],[],gold=.3,oy=590),'red',cam=Z(1.0,1.08,0,0,0,0))
add(10,1,0,C([mk(CX-220,670,1.4,dark=.35),kt(CX+220,670,1.4,dark=.35,flip=-1)],[{'t':'glow','x':CX-220,'y':250,'r':80,'rgb':'255,70,40','ga':.9},{'t':'glow','x':CX+220,'y':250,'r':80,'rgb':'255,70,40','ga':.9}],rgb='120,30,40'),'dark',shake=2)
add(10,2,0,O([hd('madhu',CX-240,450,2.2),hd('kaitabha',CX+250,450,2.2,flip=-1)],[WF(680)],oy=620,rgb='255,140,110'),'dark',cam=Z(1.0,1.1,0,0,0,-12))
add(10,2,'मधु',O([mk(CX,660,1.5)],[WF(630),txt('मधु',CX,150,110,0,d=.8)],oy=600,rgb='255,170,80',ga=.25),'amb',cues=['मधु'])
add(10,2,'दूसरा',O([kt(CX,660,1.5)],[WF(630),txt('कैटभ',CX,150,110,0,d=.8)],oy=600,rgb='255,120,100',ga=.25),'red',cues=['कैटभ'])
add(10,2,'कीट',O([hd('kaitabha',CX,450,2.7)],[WF(680)],oy=620,rgb='255,120,100'),'red',cam=Z(1.0,1.1,0,0,0,-12))
# ================= B11: they grow =================
add(11,0,0,O([mk(CX-170,650,1.3),kt(CX+170,650,1.3,flip=-1)],[WF(630)],oy=590),'dark',dx=.8)
add(11,0,'भूख',O([mk(CX,660,1.6,pose='stand')],[WF(640)],oy=600),'dark',cam=Z(1.0,1.08,0,0,0,-8))
add(11,0,'पानी',O([],[WF(560)],oy=480),'night',cam=Z(1.0,1.1,0,0,0,-12))
add(11,0,'जल',O([hd('madhu',CX-200,440,1.9),hd('kaitabha',CX+240,440,1.9,flip=-1)],[WF(640)],oy=590),'dark')
add(11,1,0,O([mk(CX-220,700,.9,ds=.12),kt(CX+220,700,.8,ds=.12,flip=-1)],[WF(640)],oy=600),'dark',cues=['बढ़ने'])
add(11,1,'पहाड़',O([mk(CX-250,760,2.2),kt(CX+250,760,2.1,flip=-1)],[WF(690)],oy=620),'dark',cam=Z(1.0,1.1,0,0,0,-20))
add(11,1,'घमंड',O([hd('madhu',CX-220,450,2.2),hd('kaitabha',CX+230,450,2.2,flip=-1)],[WF(660)],oy=620),'red')
add(11,2,0,O([mk(CX-280,760,2.0,pose='open'),kt(CX+280,760,2.0,pose='open',flip=-1)],[WF(690),{'t':'sparkle','x':CX,'y':160,'n':20,'rx':520,'ry':100}],oy=620,rgb='255,160,120'),'red',cam=Z(1.0,1.1,0,0,0,-14))
# ================= B12: they reach Brahma =================
add(12,0,0,O([mk(150,720,1.7),kt(350,740,1.6),br(CX+300,620,.9)],[WF(640),{'t':'shock','x':CX+300,'y':590,'c':0,'rgb':'255,255,255','max':200}],oy=600),'dark',dx=.7)
add(12,1,0,O([mk(CX-300,760,2.1,expr=ANG),br(CX+330,640,.85)],[WF(690)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-14))
add(12,1,'ऊँचे',O([hd('madhu',CX,450,2.8,expr=ANG)],[WF(680)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-12))
add(12,2,0,O([hd('brahma',CX,450,2.3,expr=CLS)],[WF(650)],oy=600),'cool')
add(12,2,'चुप्पी',O([mk(CX-300,760,2.1,expr=ANG),kt(CX+300,760,2.1,expr=ANG,flip=-1)],[WF(690)],oy=620),'red',shake=2)
add(12,3,0,O([hd('kaitabha',CX,450,2.8,expr=ANG)],[WF(680)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-12))
add(12,3,'हमसे',O([mk(CX-320,770,2.2,pose='point',expr=ANG),br(CX+340,640,.8)],[WF(690)],oy=620),'red')
# ================= B13: the Vedas fall =================
add(13,0,0,O([mk(150,700,1.7),kt(1130,700,1.6,flip=-1),br(CX,520,1.0)],[WF(620)],oy=600),'dark',shake=2)
add(13,0,'तब',O([br(CX,560,1.15)],[WF(640),{'t':'shock','x':CX,'y':640,'c':0,'rgb':'200,220,255','max':400}],oy=600),'dark',shake=6,cues=['हिलाना'])
add(13,1,0,O([br(CX,560,1.3)],[WF(640),{'t':'books','x':CX,'y':200,'c':0,'gap':110}],oy=600),'dark',shake=5,cues=['चारों'])
add(13,1,'फिसल',O([br(CX,560,1.3)],[{'t':'books','x':CX,'y':260,'c':0,'gap':110,'fall':140},WF(640)],oy=600),'dark',shake=4,cues=['वेद'])
add(13,2,0,O([],[{'t':'books','x':CX,'y':80,'c':0,'gap':200,'fall':160},WF(600),{'t':'shock','x':CX,'y':610,'c':1,'rgb':'200,220,255','max':600}],oy=560),'cool',cues=['वे','पानी'])
add(13,3,0,O([mk(CX-300,760,2.0,expr=ANG),kt(CX+300,760,2.0,expr=ANG,flip=-1)],[WF(690),orb(CX,420,90,'255,225,160',.6)],oy=620),'red')
add(13,4,0,O([hd('madhu',CX-240,450,2.4,expr=ANG),hd('kaitabha',CX+250,450,2.4,expr=ANG,flip=-1)],[WF(680)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-12))
add(13,4,'रचना',R([mk(CX-300,760,2.2,expr=ANG),kt(CX+300,760,2.2,expr=ANG,flip=-1)],[{'t':'flash','c':0,'w':.3,'rgb':'255,160,120'}],r=1),'red',cues=['मिटा'],shake=4)
# ================= B14: calling Vishnu =================
add(14,0,0,O([hd('brahma',CX,450,2.4)],[WF(650)],oy=600),'dark',cam=Z(1.0,1.1,0,0,0,-12))
add(14,1,0,O([br(CX,600,1.5,aura='150,160,255')],[WF(650),{'t':'shock','x':CX,'y':400,'c':0,'rgb':'180,200,255','max':800}],oy=600),'cool',cues=['रक्षक'])
add(14,1,'आपके',O([hd('brahma',CX,450,2.6)],[WF(660)],oy=610),'dark',cam=Z(1.0,1.1,0,0,0,-14))
add(14,1,'सुन',O([br(CX-330,620,1.0),vr(CX+300,640,.8)],[WF(640),{'t':'ribbon','c':0,'x0':CX-250,'y0':430,'x1':CX+240,'y1':520,'dur':1.4}],gold=.4,oy=600),'cool',cues=['सुन'])
add(14,2,0,O([vr(CX,650,1.4)],[WF(640)],gold=.6,oy=590),'cool',cam=Z(1.0,1.08,0,0,0,-8))
add(14,2,'योगनिद्रा',O([hd('vishnu',CX,430,2.5,expr=CLS)],[txt('योगनिद्रा',CX,150,100,0,d=.9),WF(660)],oy=610),'cool',cues=['योगनिद्रा'])
add(14,2,'नींद',O([vr(CX,650,1.25)],[WF(640),txt('न नींद, न जागना',CX,150,80,0,d=.9)],gold=.5,oy=590),'cool',cues=['नींद'])
add(14,2,'चीख़ों',O([vr(CX+60,650,1.2)],[{'t':'shock','x':CX-300,'y':440,'c':0,'rgb':'200,210,255','max':500},{'t':'shock','x':CX-300,'y':440,'c':1,'rgb':'200,210,255','max':800},WF(640)],gold=.5,oy=590),'cool',cues=['चीख़ों','असर'])
add(14,2,'ठहाके',O([mk(CX-300,760,2.0,expr=ANG),kt(CX+300,760,2.0,expr=ANG,flip=-1)],[WF(690)],oy=620),'red',shake=2)
# ================= B15: Nidra and the awakening =================
add(15,0,0,O([br(CX,610,1.3,aura='255,225,170')],[WF(650),spk(CX,380,30,260,220)],oy=600),'cool')
add(15,0,'निद्रा',C([ni(CX+200,670,1.5)],[orb(CX+200,380,420,'150,110,255',.45),spk(CX+200,380,40,300,240)],rgb='130,90,220'),'night',cam=Z(1.0,1.1,0,0,0,-10))
add(15,1,0,C([hd('brahma',CX-260,450,2.0),ni(CX+300,670,1.3)],[orb(CX+300,380,360,'150,110,255',.4)],rgb='130,90,220'),'night')
add(15,1,'तुम्हारे',C([ni(CX,680,1.6)],[orb(CX,400,460,'150,110,255',.5),spk(CX,400,40,300,240)],rgb='130,90,220'),'night',cam=Z(1.0,1.1,0,0,0,-12))
add(15,1,'उन्हें',C([hd('brahma',CX,450,2.4)],[orb(CX,380,340,'150,110,255',.3)],rgb='130,90,220'),'night')
add(15,2,0,C([ni(CX,680,1.6,fo=0,fd=3.5)],[orb(CX,400,420,'150,110,255',.45)],rgb='130,90,220'),'night',cam=Z(1.0,1.08,0,0,0,0))
add(15,2,'विष्णु',O([hd('vishnu',CX,430,2.6)],[WF(660),{'t':'sparkle','x':CX,'y':360,'n':24,'rx':260,'ry':200}],gold=.6,oy=610),'cool',cues=['आँखें'])
# ================= B16: Hayagriva =================
add(16,0,0,O([hd('vishnu',CX,430,2.8)],[WF(660)],oy=610),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(16,0,'नया',C([vi(CX,660,1.5)],[{'t':'flash','c':0,'w':.4,'rgb':'200,220,255'},{'t':'shock','x':CX,'y':400,'c':0,'rgb':'180,210,255','max':800}],rgb='130,160,255'),'cool',cues=['नया'])
add(16,0,'घोड़े',C([hd('hayagriva',CX,440,2.5)],[orb(CX,380,360,'255,240,200',.4)],rgb='200,200,255'),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(16,0,'हयग्रीव',C([hy(CX,670,1.6,aura='200,220,255')],[txt('हयग्रीव',CX,150,120,0,d=.8),spk(CX,380,30,260,240)],rgb='180,200,255'),'cool',cues=['हयग्रीव'])
add(16,1,0,O([hy(CX-260,680,1.5,pose='lunge'),mk(CX+250,720,1.8,expr=ANG,flip=-1)],[WF(680),{'t':'shock','x':CX,'y':420,'c':0,'rgb':'255,220,170','max':900},{'t':'flash','c':0,'w':.3,'rgb':'255,240,210'}],oy=620),'red',shake=6,cues=['युद्ध'])
add(16,2,0,O([hy(CX-300,690,1.6,pose='lunge'),kt(CX+270,720,1.8,expr=ANG,flip=-1)],[WF(680),{'t':'bolt','x0':CX-120,'y0':300,'x1':CX+100,'y1':420,'c':0,'d':.3}],oy=620),'red',shake=4)
add(16,2,'पाँच',C([],[{'t':'icon','i':'cycle','x':CX,'y':330,'sc':2.6,'c':0,'d':.8},txt('५००० वर्ष',CX,560,100,0,d=.8)],rgb='200,160,255',spin=.4),'night',cues=['पाँच'])
add(16,3,0,O([hy(CX,680,1.5,dark=.8)],[WF(680)],oy=620),'dark',cam=Z(1.0,1.1,0,0,0,-12))
# ================= B17: the trick =================
add(17,0,0,O([hd('vishnu',CX,430,2.7,expr=CLS)],[WF(660)],oy=610),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(17,0,'ताक़त',O([hy(CX-300,690,1.5,dark=.8),mk(CX+300,740,1.8,flip=-1,dark=.7)],[WF(680)],oy=620),'dark')
add(17,0,'दिमाग़',C([hd('vishnu',CX,440,2.6)],[{'t':'glow','x':CX,'y':250,'r':260,'rgb':'255,230,160','ga':.6},spk(CX,250,30,200,120)],rgb='200,200,255'),'amb',cam=Z(1.0,1.1,0,0,0,-12))
add(17,1,0,O([vi(CX,680,1.5)],[WF(680)],oy=620),'cool',cam=Z(1.0,1.08,0,0,0,-8))
add(17,1,'हाथ',O([vi(CX,690,1.6,pose='plead')],[WF(690)],oy=630),'cool')
add(17,2,0,O([hd('vishnu',CX,440,2.7)],[WF(670)],oy=620),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(17,2,'तुम',O([mk(CX-300,760,2.1),kt(CX+300,760,2.1,flip=-1)],[WF(690)],oy=620),'red')
add(17,2,'प्रसन्न',O([hd('vishnu',CX,440,2.9)],[WF(670)],oy=620),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(17,2,'माँगो',C([hd('vishnu',CX,440,2.6)],[txt('वरदान',CX,170,110,0,d=.8),spk(CX,300,30,300,160)],rgb='255,225,170'),'amb',cues=['वरदान'])
# ================= B18: asuras laugh =================
add(18,0,0,O([hd('madhu',CX-240,450,2.4,expr=ANG),hd('kaitabha',CX+250,450,2.4,expr=ANG,flip=-1)],[WF(680)],oy=620),'red',shake=2,dx=.5)
add(18,1,0,O([mk(CX,760,2.4,pose='open',expr=ANG)],[WF(690)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-14))
add(18,1,'थककर',O([hd('kaitabha',CX,450,2.8,expr=ANG)],[WF(680)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-12))
add(18,1,'विजेता',O([mk(CX-300,770,2.2,pose='point'),kt(CX+300,770,2.2,pose='open',flip=-1)],[WF(690)],oy=620),'red')
add(18,1,'माँग',O([hd('madhu',CX,450,2.8)],[WF(680)],oy=620),'red',cam=Z(1.0,1.1,0,0,0,-12))
add(18,2,0,O([hd('vishnu',CX,440,2.7)],[WF(670)],oy=620),'cool')
add(18,3,0,O([mk(CX-300,770,2.2,expr=ANG),kt(CX+300,770,2.2,expr=ANG,flip=-1)],[WF(690),txt('कुछ भी!',CX,200,110,0,d=.3)],oy=620),'red',cues=['कुछ'],shake=3)
add(18,4,0,O([hd('vishnu',CX,440,2.7)],[WF(670),{'t':'glow','x':CX,'y':400,'r':340,'rgb':'255,225,170','ga':.35}],oy=620),'warm',cam=Z(1.0,1.1,0,0,0,-12))
# ================= B19: the trap =================
add(19,0,0,O([hd('vishnu',CX,440,2.8)],[WF(670)],oy=620),'cool',cam=Z(1.0,1.1,0,0,0,-14))
add(19,0,'वध',O([hd('vishnu',CX,440,3.1)],[WF(670),txt('वध',CX,170,110,0,glow='rgba(255,80,60,.9)',d=.5)],oy=620),'dark',cues=['वध'])
add(19,1,0,Vd([],[]),'dark')
add(19,2,0,O([hd('madhu',CX-240,450,2.4),hd('kaitabha',CX+250,450,2.4,flip=-1)],[WF(680)],oy=620),'dark',cam=Z(1.0,1.1,0,0,0,-12))
add(19,2,'शब्दों',C([mk(CX-300,760,2.0),kt(CX+300,760,2.0,flip=-1)],[{'t':'threads','x':CX,'y':350,'c':0,'d':1.0,'rgb':'200,170,255','to':[[120,120],[1160,120],[120,640],[1160,640],[CX,40],[300,60],[980,60],[60,380],[1220,380]]}],rgb='160,120,200'),'night',cues=['जाल'])
add(19,2,'वचन',C([],[txt('वचन',CX,360,170,0,glow='rgba(255,220,150,.9)',d=.8)],rgb='200,160,255'),'amb',cues=['वचन'])
add(19,2,'पीछे',O([mk(CX-300,760,2.0),kt(CX+300,760,2.0,flip=-1)],[WF(690)],oy=620),'dark',cam=Z(1.0,1.08,0,0,0,0))
# ================= B20: the last trick =================
add(20,0,0,O([hd('madhu',CX-240,450,2.4),hd('kaitabha',CX+250,450,2.4,flip=-1)],[WF(680)],oy=620),'red',shake=2)
add(20,0,'चाल',O([hd('kaitabha',CX,450,2.7)],[WF(670),{'t':'flash','c':0,'w':.3,'rgb':'255,240,200'}],oy=620),'amb',cues=['कौंधी'])
add(20,0,'जल',O([],[WF(540)],oy=470,rgb='120,160,230'),'night',cam=Z(1.0,1.1,0,0,0,-14))
add(20,1,0,O([mk(CX-300,770,2.2,pose='open',expr=ANG),kt(CX+300,770,2.2,pose='open',expr=ANG,flip=-1)],[WF(690)],oy=620),'red',shake=3)
add(20,1,'जहाँ',R([hd('madhu',CX,450,2.8,expr=ANG)],[],r=.8),'red',cam=Z(1.0,1.1,0,0,0,-12))
# ================= B21: the blue mountain, the thighs, Madhusudana =================
add(21,0,0,O([hd('hayagriva',CX,440,2.6)],[WF(660),orb(CX,380,360,'255,240,200',.35)],oy=610),'warm',cam=Z(1.0,1.1,0,0,0,-12))
add(21,0,'आकार',O([hy(CX,680,1.0,ds=.12)],[WF(660)],oy=610),'cool',cues=['बड़ा'])
add(21,0,'बड़ा',O([hy(CX,780,2.0,ds=.1)],[WF(700)],oy=620),'cool',cam=Z(1.0,1.1,0,0,0,-18))
add(21,0,'नीले',O([hy(CX,1250,3.6,aura='160,190,255'),mk(CX-420,690,.45),kt(CX+420,690,.45,flip=-1)],[WF(690)],oy=640,rgb='120,160,255'),'cool',cam=Z(1.0,1.06,0,0,0,-10))
add(21,0,'आसमान',O([hy(CX,1700,5.0,aura='160,190,255')],[{'t':'sparkle','x':CX,'y':140,'n':20,'rx':400,'ry':80}],oy=640,rgb='120,160,255'),'cool',cam=Z(1.0,1.05,0,0,0,-6))
add(21,1,0,O([hy(CX,1250,3.6,aura='160,190,255'),mk(CX-210,760,.42),kt(CX+210,780,.42,flip=-1)],[WF(700)],oy=640,rgb='120,160,255'),'cool',cam=Z(1.0,1.06,0,0,0,-10))
add(21,1,'जाँघों',O([hd('madhu',CX-220,440,2.0),hd('kaitabha',CX+220,440,2.0,flip=-1)],[WF(680),txt('जाँघ पर — जल नहीं',CX,170,70,0,d=.8)],oy=620),'cool')
add(21,2,0,R([hy(CX,720,1.7,pose='lunge')],[{'t':'flash','c':0,'w':.5,'rgb':'255,255,255'},{'t':'shock','x':CX,'y':400,'c':0,'rgb':'255,240,200','max':1100}],r=0),'cool',cues=['वार'],shake=8)
add(21,3,0,O([vi(CX,680,1.6,aura='255,225,170')],[WF(690),txt('मधुसूदन',CX,160,130,0,d=.9),spk(CX,360,40,300,220)],gold=.6,oy=620),'amb',cues=['मधुसूदन'])
# ================= B22: Brahma and Vishnu talk =================
add(22,0,0,O([hd('brahma',CX,450,2.4)],[WF(650)],oy=600),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(22,0,'मिटाने',O([br(CX-330,630,1.2),vi(CX+300,680,1.5)],[WF(680)],oy=620),'cool')
add(22,1,0,O([hd('vishnu',CX,440,2.7)],[WF(670)],oy=620),'cool',cam=Z(1.0,1.1,0,0,0,-12))
add(22,1,'ब्रह्मांड',C([],[orb(CX,340,500,'255,225,170',.5),spk(CX,340,50,500,240)],rgb='255,215,160'),'amb')
add(22,1,'मेरे',O([vi(CX,690,1.5)],[WF(690),{'t':'glow','x':CX,'y':400,'r':380,'rgb':'255,225,170','ga':.3}],oy=620),'warm')
# ================= B23: the Vedas return, the earth is made =================
add(23,0,0,O([br(CX,620,1.3,aura='255,225,170')],[{'t':'books','x':CX,'y':260,'c':0,'gap':110,'fall':-60},WF(650)],oy=600),'warm',cues=['वेदों'],dx=.7)
add(23,0,'चर्बी',O([hd('vishnu',CX,440,2.5)],[WF(670),txt('मेद',CX,170,110,0,d=.8)],oy=620),'cool',cues=['मेद'])
add(23,0,'धरती',{'mts':[(None,0,CX-480,170,'#4a5a8a',170),(None,0,CX-320,260,'#5a6a9a',200),(None,0,CX-140,340,'#6a7aaa',230),(None,0,CX+40,300,'#5a6a9a',210),(None,0,CX+200,240,'#4a5a8a',190),(None,0,CX+340,320,'#6a7aaa',210),(None,0,CX+480,190,'#4a5a8a',170)]},'earth',draw='earth',shake=3)
add(23,0,'मेदिनी',{'bg':bg('dawn'),'figs':[],'fx':[txt('मेदिनी',CX,330,170,0,d=.9),spk(CX,420,40,520,200)]},'warm',cues=['मेदिनी'])
add(23,1,0,{'bg':bg('dawn'),'figs':[],'fx':[txt('बारह चट्टानी परतें',CX,330,100,0,d=.9)]},'earth',cues=['बारह'])
# ================= B24: back on the lotus =================
add(24,0,0,O([br(CX,620,1.3,aura='255,225,170')],[WF(650)],gold=.4,oy=600),'warm',cam=Z(1.0,1.08,0,0,0,-8))
add(24,0,'सृष्टि',O([br(CX,620,1.1)],[WF(650),spk(CX,330,40,400,240),orb(CX,330,420,'255,225,170',.3)],gold=.4,oy=600),'amb')
add(24,0,'उम्मीद',O([hd('brahma',CX,450,2.4)],[WF(650)],gold=.3,oy=600),'warm',cam=Z(1.0,1.1,0,0,0,-10))
add(24,1,0,O([br(CX,620,1.2,dark=.85)],[WF(650)],oy=600),'dark',cam=Z(1.0,1.08,0,0,0,0))
add(24,2,0,R([hd('brahma',CX,450,2.5)],[txt('पहली मुसीबत',CX,170,90,0,glow='rgba(255,70,50,.9)',d=.9)],r=1),'red',cues=['पहली'],shake=2)
# ================= B25: teaser =================
add(25,0,0,Vd([F('shiva',CX,680,1.6,dark=.08,aura='120,150,255')],[orb(CX,340,360,'120,150,255',.3)]),'dark',dx=.9)
add(25,0,'जिनका',C([],[orb(CX,340,420,'140,170,255',.45),spk(CX,340,40,300,220)],rgb='120,150,255'),'night',cam=Z(1.0,1.1,0,0,0,-10))
add(25,0,'प्रकट',{'bg':bg('kailash'),'figs':[sh(CX,650,1.3,dark=.4)],'fx':[orb(CX,340,380,'160,190,255',.4)]},'cool')
add(25,1,0,{'bg':bg('kailash'),'figs':[sh(CX,650,1.4)],'fx':[txt('शिव का प्राकट्य',CX,170,100,0,d=.9)]},'night',cues=['शिव'],cam=Z(1.0,1.1,0,0,0,-10))
add(25,2,0,C([],[txt('कल मिलते हैं',CX,360,110,0,d=1.0)],rgb='200,170,255'),'night',cues=['कल'])

# library (Gemini) chakra instead of the coded cycle icon (the five-thousand-year war of Vishnu/Hayagriva)
for _s in film.shots:
    _sc=_s.get('sc')
    if not _sc:continue
    _sc['fx']=[({'t':'fximg','src':'../library/pilot/assets/fx_sudarshan_chakra.png','x':x['x'],'y':x['y'],'w':88*x.get('sc',1),'blend':'lighter','spin':1.4,'c':x.get('c',0),'d':x.get('d',1)} if x.get('t')=='icon' and x.get('i')=='cycle' else x) for x in _sc.get('fx',[])]
print(film.save(os.path.join(HERE,'shots.json')),'shots')
