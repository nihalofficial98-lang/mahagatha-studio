import json,itertools,os
HERE=os.path.dirname(os.path.abspath(__file__))
C={'cel':'rgba(190,200,255,0.14)','warm':'rgba(255,190,120,0.16)','red':'rgba(255,60,30,0.20)','night':'rgba(60,90,170,0.20)','pal':'rgba(255,170,90,0.14)','cool':'rgba(80,160,200,0.16)','dark':'rgba(20,10,40,0.22)','amb':'rgba(255,170,80,0.16)','earth':'rgba(120,200,120,0.10)','void':'rgba(120,40,200,0.16)'}
def z(a,b,x0=0,x1=0,y0=0,y1=0,r0=0,r1=0): return {"from":{"z":a,"x":x0,"y":y0,"r":r0},"to":{"z":b,"x":x1,"y":y1,"r":r1}}
CAMS=[z(1.0,1.09,0,0,0,-14),z(1.1,1.0,-30,20,0,0),z(1.0,1.08,40,-30,10,0,-0.006,0.006),z(1.09,1.0,0,0,-12,10),z(1.0,1.07,-40,30,0,-10,0.006,-0.004)]
cc=itertools.count()
S=[]
def add(beat,at,sc,grade='cel',cam=None,draw='scene',**k):
    d={"beat":beat,"at":at,"draw":draw,"cam":cam or CAMS[next(cc)%5],"grade":C.get(grade,grade)}
    if sc is not None:d["sc"]=sc
    d.update(k);S.append(d)
def F(who,x,y,s,**k):
    d={"who":who,"x":x,"y":y,"s":s};d.update(k);return d
def bg(k,**o):
    d={"k":k};d.update(o);return d
CX=640
# ===== sample beats reused (6, 9, 10)
for s in json.load(open(os.path.join(HERE,'sample_shots.json'))):
    if s['beat']==6: pass
SAMPLE=json.load(open(os.path.join(HERE,'sample_shots.json')))
def sample(b): 
    for s in SAMPLE:
        if s['beat']==b: S.append(s)
# ---------------- B01
add(1,0,{'bg':bg('night'),'figs':[F('brahma',CX,610,1.5,aura='150,170,255',pose='rest',expr={'eye':1,'mouth':0.1})],'fx':[{'t':'glow','x':CX,'y':420,'r':260,'rgb':'150,170,255','ga':0.3}]},'night',dx=0.9)
add(1,'पर ब्रह्मा',{'bg':bg('night'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'brow':0.8,'mouth':-0.3,'eye':1.1})]},'night',cam=z(1.0,1.1,0,0,0,-30))
add(1,'अगली',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'crack','x':CX-320,'c':0,'d':0.5},{'t':'crack','x':CX,'c':1,'d':0.5},{'t':'crack','x':CX+320,'c':2,'d':0.5},{'t':'text','s':'तीन मुसीबतें','x':CX,'y':330,'size':64,'c':2,'d':0.8,'glow':'rgba(255,90,40,.7)'}]},'red',cues=['अगली','तीन','मुसीबतें'])
add(1,'किसी',{'bg':bg('storm',r=0.25),'figs':[],'fx':[{'t':'icon','i':'asuras','x':CX,'y':330,'sc':2.6,'c':0},{'t':'icon','i':'ban','x':CX,'y':330,'sc':3.6,'c':1,'d':0.3}]},'dark',cues=['असुर','नहीं'])
add(1,'वो आईं',{'bg':bg('night'),'figs':[F('brahma',CX-230,640,1.5,aura='255,200,120',expr={'brow':0.3,'mouth':0.1})]+[F('kumara%d'%i,CX+60+i*150,620,1.0,pose='namaste',ac=0,a=0.0,tail=False) for i in range(4)],'fx':[]},'night',cues=['बेटों'])
S[-1]['sc']['figs'][1:]=[F('kumara%d'%i,CX+90+i*130,620,0.95,pose='namaste',ac=0,ad=0.8,dark=0.8,tail=False) for i in range(4)]
add(1,'और उनके',{'bg':bg('voidR'),'figs':[F('brahma',CX,660,1.7,aura='255,60,30',key='255,90,50',rim='rgba(255,170,110,.95)',expr={'brow':-0.9,'mouth':-0.6})],'fx':[{'t':'flames','x':CX-300,'y':690,'sc':1.3,'c':0},{'t':'flames','x':CX+300,'y':690,'sc':1.3,'c':0}]},'red',cues=['अपने'],shake=2)
# ---------------- B02
add(2,0,{'bg':None,'mts':[],'fx':[]},'earth',draw='earth',cues=['धरती'],dx=0.6)
S[-1]['sc']={'mts':[],'fx':[{'t':'text','s':'मधु-कैटभ की चर्बी से…','x':CX,'y':160,'size':46,'c':0,'d':0.9,'fade':None}]}
add(2,'ब्रह्मा ने आठ',{'mts':[(None,0,CX-480,170,'#4a5a8a',170),(None,0,CX-320,260,'#5a6a9a',200),(None,0,CX-140,340,'#6a7aaa',230),(None,0,CX+40,300,'#5a6a9a',210),(None,0,CX+200,240,'#4a5a8a',190),(None,0,CX+340,320,'#6a7aaa',210),(None,0,CX+480,190,'#4a5a8a',170)]},'earth',draw='earth',cues=['आठ'],shake=2)
S[-1]['sc']['mts']=[(n,0,x,h,c,w) for (n,_,x,h,c,w) in S[-1]['sc']['mts']]
add(2,'सुमेरु',{'mts':[('सुमेरु',0,CX-420,300,'#6a7aaa',200),('कैलाश',1,CX-140,360,'#8a9aca',210),('हिमालय',2,CX+140,330,'#7a8aba',210),('मलय',3,CX+420,250,'#5a7a6a',190)]},'earth',draw='earth',cues=['सुमेरु','कैलाश','हिमालय','मलय'])
add(2,'सात',{'c':[1,2,3,3],'sw':0,'fx':[]},'cool',draw='map',cues=['बनाए','जंबूद्वीप','कुशद्वीप','पुष्करद्वीप'])
add(2,'नदियाँ',{'c':[-1,-1,-1,-1],'rv':0,'fx':[]},'cool',draw='map',cues=['नदियाँ'])
add(2,'समंदर',{'bg':bg('dusk'),'figs':[],'fx':[{'t':'sparkle','x':CX,'y':480,'n':30,'rx':420,'ry':70,'a':0.8}]},'warm')
add(2,'पेड़',{'mts':[('',-1,CX-420,200,'#5a7a6a',230),('',-1,CX,260,'#6a8a7a',260),('',-1,CX+420,200,'#5a7a6a',230)],'trees':0},'earth',draw='earth',cues=['पेड़'])
add(2,'सब',{'c':[-1,-1,-1,-1],'bloom':0,'fx':[]},'earth',draw='map',cues=['खिल'])
# ---------------- B03
T3=lambda **k:dict({'cv':-1,'c1':-1,'c2':-1,'c3':-1,'c4':-1,'c5':-1,'c6':-1},**k)
add(3,0,T3(c1=0,c2=1,cv=9,c3=9,c4=9,c5=9,c6=9,pan=[(None,600),(1,1000)]),'night',draw='tower',cues=['स्वर्गलोक','भूलोक'],dx=0.7)
add(3,'नीचे',T3(c3=0,c4=1,c5=9,c6=9,cv=9,pan=[(None,1000),(1,1450)]),'dark',draw='tower',cues=['अतल','वितल'])
add(3,'सुतल',T3(c3=-1,c4=-1,c5=0,c6=1,cv=9,pan=[(None,1450),(1,1900)]),'dark',draw='tower',cues=['सुतल','पाताल'])
add(3,'और इन',T3(cv=0,pan=[(None,1800),(0,250)]),'warm',draw='tower',cues=['वैकुंठ'])
# ---------------- B04
add(4,0,{'bg':bg('cosmos'),'figs':[F('brahma',CX,640,1.4,aura='190,170,255',expr={'eye':1})],'fx':[{'t':'icon','i':'cycle','x':CX,'y':250,'sc':2.2,'c':0,'d':1.0}]},'void',cues=['चार'],dx=0.7)
add(4,'सफ़ेद',{'pc':[0,1,None,None]},'night',draw='pillars',cues=['सफ़ेद','लाल'])
add(4,'पीला',{'pc':[None,None,0,1],'pre':2},'night',draw='pillars',cues=['पीला','काला'])
add(4,'चारों',{'pc':[None]*4,'pre':4,'ring':0,'fx':[{'t':'text','s':'महायुग','x':CX,'y':140,'size':64,'c':1,'d':1.0,'glow':'rgba(255,220,150,.7)'}]},'amb',draw='pillars',cues=['बने','महायुग'])
# ---------------- B05
add(5,0,{'bg':bg('dawn'),'figs':[],'fx':[{'t':'outline','x':CX,'y':520,'sc':1.5,'c':0,'d':1.5}]},'warm',cues=['मनुष्य'],dx=0.7)
add(5,'पर यहीं',{'bg':bg('storm',r=0.6),'figs':[F('brahma',CX,700,1.5,aura='255,80,40',expr={'brow':0.5,'mouth':-0.3})]},'red',cues=['अगली'])
add(5,'अगली',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'crack','x':CX,'c':0,'d':0.6},{'t':'text','s':'अगली मुसीबत','x':CX,'y':340,'size':72,'c':0,'d':0.9,'glow':'rgba(255,60,30,.8)'}]},'red',shake=3,cues=['मुसीबत'])
S[-1]['sc']['fx'][1]['c']=0
sample(6)
# ---------------- B07
K4=lambda **k:[F('kumara%d'%i,CX-470+i*130,640,1.0,pose='namaste',tail=False,**k) for i in range(4)]
add(7,0,{'bg':bg('cel'),'figs':K4()+[F('brahma',CX+330,700,1.3,aura='255,225,170',expr={'eye':1})]},'cel',dx=0.5)
add(7,'नहीं',{'bg':bg('cel'),'figs':[F('kumara0',CX,460,0.0)],},'cel')
S[-1]['sc']['figs']=[F('kumara1',CX,900,2.7,pose='namaste',tail=False,aura='255,240,200')]
add(7,'नहीं',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':1.3,'open':0.3,'brow':0.7})],'fx':[{'t':'text','s':'?','x':CX+330,'y':220,'size':120,'c':0,'d':0.3,'glow':'rgba(255,255,255,.6)'}]},'cel',cues=['नहीं'])
add(7,'नहीं परमपिता',{'bg':bg('cel'),'figs':[F('kumara%d'%i,CX-300+i*200,640,1.25,pose='namaste',tail=False) for i in range(4)]},'cel')
add(7,'ब्रह्मा चौंक',{'bg':bg('cel',floor=True),'figs':[F('brahma',CX,660,1.7,aura='255,225,170',expr={'eye':1.3,'open':0.4,'brow':0.8})],'fx':[{'t':'shock','x':CX,'y':520,'c':0,'rgb':'255,255,255','max':800}]},'cel',cues=['चौंक'],shake=2)
add(7,'तुम अपने',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'brow':-0.3,'mouth':-0.4,'eye':1.1,'open':0.2})]},'warm')
add(7,'क्षमा',{'bg':bg('cel',warm=True),'figs':[F('kumara3',CX,640,1.8,pose='namaste',tail=False,aura='255,240,200')]},'warm')
add(7,'हमें जन्म',{'bg':bg('cosmos'),'figs':[],'fx':[{'t':'icon','i':'cycle','x':CX,'y':330,'sc':3.2,'c':0,'d':0.8},{'t':'icon','i':'ban','x':CX,'y':330,'sc':4.2,'c':1,'d':0.4}]},'void',cues=['चक्र','बँधना'])
add(7,'जब पूरा',{'bg':bg('cosmos',spin=0.12,rgb='120,200,255'),'figs':K4(a=0.0)},'night',cam=z(1.0,1.25,0,0,0,30))
S[-1]['sc']['figs']=[F('kumara%d'%i,CX-300+i*200,690,0.9,pose='namaste',tail=False,dark=0.35,ds=0) for i in range(4)]
add(7,'हम परब्रह्म',{'bg':bg('cel',warm=True),'figs':[F('kumara%d'%i,CX-300+i*200,640,1.25,pose='cross',tail=False,aura='255,235,190') for i in range(4)],'fx':[{'t':'glow','x':CX,'y':330,'r':380,'rgb':'255,240,200','c':0,'d':1.4,'ga':0.6}]},'warm',cues=['ध्यान'])
add(7,'क्या आपको',{'bg':bg('cel'),'figs':[F('brahma',CX,680,1.5,aura='255,225,170',pose='open',expr={'brow':0.5})],'fx':[{'t':'sparkle','x':CX,'y':400,'n':20,'rx':300,'ry':200,'c':0,'d':0.8},{'t':'threads','x':CX,'y':400,'to':[[120,160],[1160,160],[120,520],[1160,520]],'c':0,'d':0.8}]},'cel',cues=['दिशाओं'])
# ---------------- B08
add(8,0,{'bg':bg('cel'),'figs':[F('brahma',CX-300,700,1.45,pose='open',expr={'brow':0.9,'mouth':-0.1}),]+[F('kumara%d'%i,CX+100+i*120,640,0.95,pose='cross',tail=False) for i in range(4)]},'cel',dx=0.4)
add(8,'पर कुमार',{'bg':bg('cel'),'figs':[F('kumara%d'%i,CX-300+i*200,640,1.25,pose='cross',tail=False,expr={'brow':0.1}) for i in range(4)]},'dark')
add(8,'उन्होंने बस',{'bg':bg('cel',warm=True),'figs':[F('kumara2',CX,900,2.7,pose='open',tail=False,aura='255,240,200')],'fx':[{'t':'name','s':'एक वरदान','x':CX,'y':600,'c':0,'d':0.5}]},'warm',cues=['वरदान'])
add(8,'हम सदा',{'bg':bg('cel',warm=True),'figs':[F('kumara%d'%i,CX-300+i*200,640,1.25,pose='open',tail=False,aura='255,245,210') for i in range(4)],'fx':[{'t':'name','s':'सदा बालक','x':CX,'y':260,'c':0,'d':0.6,'size':44},{'t':'icon','i':'ban','x':CX,'y':380,'sc':2.2,'c':1,'d':0.3}]},'warm',cues=['बालक','बूढ़े'])
add(8,'और ब्रह्मा',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':0.5,'brow':0.9,'mouth':-0.5})]},'dark',cam=z(1.0,1.08,0,0,0,-20))
add(8,'चारों बाल',{'bg':bg('cel',warm=True),'figs':[F('kumara%d'%i,CX-240+i*160,620,1.1,pose='stand',tail=False,vy=-8,fo=0,fd=3.0,ds=-0.07) for i in range(4)]},'warm',cues=['चले'])
add(8,'ब्रह्मा अकेले',{'bg':bg('cel',fy=660),'figs':[F('brahma',CX,640,1.2,aura='200,200,255',expr={'eye':0.7,'mouth':-0.3})]},'dark',cam=z(1.3,1.0,0,0,-40,0))
add(8,'और उनके',{'bg':bg('storm',r=0.4),'figs':[F('brahma',CX,985,3.1,aura='255,70,30',key='255,90,50',rim='rgba(255,170,110,.95)',expr={'brow':-0.5,'mouth':-0.2,'eye':1})],'fx':[{'t':'glow','x':CX,'y':620,'r':360,'rgb':'255,70,30','c':0,'d':2.0,'ga':0.5}]},'red',cues=['सुलगने'],cam=z(1.0,1.1,0,0,0,-20))
sample(9);sample(10)
# ---------------- B11
add(11,0,{'bg':bg('storm',r=0.5),'figs':[F('brahma',CX-330,700,1.4,pose='namaste',expr={'brow':0.5}),F('rudra',CX+330,700,1.75,pose='tri',key='255,90,50',rim='rgba(255,170,110,.95)',lx=1,flip=-1,expr={'brow':-0.8,'eye':1.1},exprB={'brow':0,'eye':1,'mouth':0.2},ec=0)]},'red',cues=['शांत'],dx=0.5)
add(11,'रुद्र मान',{'bg':bg('cel',warm=True),'figs':[F('rudra',CX,430,3.4,head=True,expr={'brow':-0.1,'eye':0.9,'mouth':0.2},key='255,214,160')]},'warm')
add(11,'और फ़ौरन',{'bg':bg('cel',warm=True),'figs':[F('rudra',CX,650,1.7,pose='open',key='255,214,160',expr={'mouth':0.1})],'fx':[{'t':'orbs','items':[{'c':0,'x0':CX,'y0':430,'x1':CX-440,'y1':300,'rgb':'255,255,200','keep':1,'dur':1.0},{'c':1,'x0':CX,'y0':430,'x1':CX+440,'y1':300,'rgb':'180,255,200','keep':1,'dur':1.0},{'c':2,'x0':CX,'y0':430,'x1':CX-240,'y1':180,'rgb':'255,200,255','keep':1,'dur':1.0},{'c':3,'x0':CX,'y0':430,'x1':CX+240,'y1':180,'rgb':'200,230,255','keep':1,'dur':1.0}]}]},'warm',cues=['बाद','एक','जीव','रचने'])
add(11,'ब्रह्मा के चेहरे',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,985,3.1,aura='255,225,170',expr={'eye':0.2,'mouth':0.9,'brow':0.3})],'fx':[{'t':'sparkle','x':CX,'y':350,'n':24,'rx':420,'ry':200}]},'warm')
add(11,'आख़िरकार',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX-300,700,1.4,aura='255,225,170',expr={'mouth':0.7,'eye':0.5}),F('rudra',CX+300,700,1.7,pose='tri',key='255,214,160',flip=-1,lx=1,expr={'eye':0.9,'mouth':0.2})],'fx':[{'t':'glow','x':CX,'y':420,'r':260,'rgb':'255,230,170','c':0,'d':1.5,'ga':0.5}]},'warm',cues=['साथी'])
add(11,'पर वो',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':0.2,'mouth':0.9,'brow':0.3},exprB={'eye':1.2,'mouth':-0.3,'brow':0.8,'open':0.2},ec=0)],'fx':[{'t':'frost','x':CX,'y':400,'c':0,'d':1.2}]},'cool',cues=['जम'])
# ---------------- B12
add(12,0,{'bg':bg('storm',r=0.3),'figs':[F('rudra',CX,690,1.3,pose='open',key='255,170,110',rim='rgba(255,170,110,.9)'),F('rudra1',CX-340,690,1.3,pose='open',key='255,170,110',ac=0,ad=0.6,a=0.0),F('rudra2',CX+340,690,1.3,pose='open',key='255,170,110',ac=0,ad=0.6,a=0.0)],'fx':[{'t':'shock','x':CX,'y':560,'c':0,'rgb':'160,170,255'}]},'night',cues=['दोहरा'],dx=0.4)
S[-1]['sc']['figs'][1]['ac']=0;S[-1]['sc']['figs'][2]['ac']=0
add(12,'एक रुद्र',{'bg':bg('storm',r=0.3),'figs':[F('rudra',CX-340,690,1.2,pose='tri',key='255,170,110',ac=0,ad=0.4),F('rudra1',CX,690,1.2,pose='tri',key='255,170,110',ac=1,ad=0.4),F('rudra2',CX+340,690,1.2,pose='tri',key='255,170,110',ac=2,ad=0.4)]},'night',cues=['एक','दूसरा','तीसरा'])
add(12,'और सब',{'bg':bg('cosmos',rgb='255,150,90'),'figs':[F('rudra',CX-340,690,1.2,pose='tri',key='255,170,110'),F('rudra1',CX,690,1.2,pose='tri',key='255,170,110'),F('rudra2',CX+340,690,1.2,pose='tri',key='255,170,110')],'fx':[{'t':'infinity','x':CX,'y':250,'c':0,'d':0.8}]},'void',cues=['अमर'])
R11=lambda **k:[F(('rudra' if i==0 else 'rudra%d'%i),CX-525+i*105,540,0.72,pose='stand',key='255,170,110',tail=False,**k) for i in range(11)]
add(12,'ग्यारह',{'bg':bg('storm',r=0.4),'figs':R11()+[F('brahma',CX,740,1.0,expr={'eye':1.2,'brow':0.7},aura=None)],'fx':[{'t':'text','s':'११ रुद्र','x':CX,'y':110,'size':56,'c':0,'d':0.6,'glow':'rgba(255,120,60,.7)'}]},'red',cues=['ग्यारह'])
add(12,'रुको',{'bg':bg('storm',r=0.4),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':1.3,'open':0.5,'brow':0.9})]},'red',shake=3,cam=z(1.0,1.12,0,0,0,-20))
add(12,'तुम अमर',{'bg':bg('storm',r=0.3),'figs':[F('brahma',CX-330,700,1.5,pose='raiseR',expr={'brow':0.8,'open':0.3}),F('rudra',CX+330,700,1.8,pose='tri',flip=-1,lx=1,key='255,170,110',expr={'brow':-0.2})]},'night')
add(12,'क्यों नहीं',{'bg':bg('cosmos',rgb='120,140,255'),'figs':[F('shiva',CX,430,3.4,head=True,expr={'brow':0.1,'eye':0.9,'mouth':0.05},key='200,220,255')]},'night')
add(12,'अगर कोई',{'bg':bg('cosmos',rgb='255,210,120'),'figs':[],'fx':[{'t':'icon','i':'cycle','x':CX,'y':330,'sc':3.4,'c':0,'d':0.8},{'t':'crack','x':CX,'c':1,'d':0.5}]},'void',cues=['जन्म','टूट'])
add(12,'पूरा संतुलन',{'bg':bg('cosmos',rgb='255,120,90'),'figs':[],'fx':[{'t':'scales','x':CX,'y':330,'c':0,'d':0.8},{'t':'shock','x':CX,'y':330,'c':1,'rgb':'255,150,90','max':700}]},'red',cues=['संतुलन','बिगड़'],shake=2)
add(12,'मर्त्य',{'bg':bg('storm',r=0.2),'figs':[F('brahma',CX-300,700,1.5,pose='open',expr={'brow':0.6})],'fx':[{'t':'icon','i':'person','x':CX+260,'y':380,'sc':2.2,'c':0,'d':0.6},{'t':'icon','i':'person','x':CX+420,'y':380,'sc':2.2,'c':0,'d':0.9},{'t':'icon','i':'person','x':CX+340,'y':250,'sc':1.7,'c':0,'d':1.2}]},'night',cues=['प्राणी'])
# ---------------- B13
add(13,0,{'bg':bg('moon'),'figs':[F('shiva',CX,430,3.4,head=True,expr={'eye':0.7,'mouth':0.0},key='200,220,255')]},'night',dx=0.5)
add(13,'मैं केवल',{'bg':bg('cosmos',rgb='130,150,255'),'figs':[F('shiva',CX,700,1.9,pose='tri',key='200,220,255',lx=1)],'fx':[{'t':'infinity','x':CX+320,'y':260,'c':0,'d':0.8}]},'night',cues=['अमर'])
add(13,'अगर यह',{'bg':bg('moon'),'figs':[F('brahma',CX-330,700,1.35,expr={'brow':0.5}),F('shiva',CX+330,700,1.75,pose='tri',key='200,220,255',flip=-1,lx=1,expr={'brow':0.1})]},'night')
add(13,'मैं तपस्या',{'bg':bg('moon'),'figs':[F('shiva',CX,985,3.1,pose='tri',key='200,220,255',lx=1,expr={'brow':0.1,'eye':0.9})]},'night')
add(13,'और महादेव',{'bg':bg('moon'),'figs':[F('shiva',CX,640,1.6,pose='tri',key='200,220,255',lx=1,fo=0,fd=3.2,ds=-0.1,vx=-10)]},'night',cues=['चले'],dx=0.6)
# ---------------- B14
add(14,0,{'bg':bg('cel'),'figs':R11()+[F('brahma',CX,740,1.0,expr={'brow':0.2})]},'cel',dx=0.5)
for f in S[-1]['sc']['figs'][:11]: f['key']='255,214,160'
add(14,'ब्रह्मा ने उन्हें',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,700,1.6,pose='open',aura='255,225,170',expr={'mouth':0.3})]},'warm')
add(14,'एक को',{'bg':bg('cel',warm=True),'figs':[F('rudra',CX,650,1.9,pose='namaste',key='255,214,160')],'fx':[{'t':'icon','i':'heart','x':CX,'y':420,'sc':1.2,'c':0,'d':0.8}]},'warm',cues=['हृदय'])
RGB5=['255,200,150','200,230,255','190,255,210','255,150,90','210,180,255']
add(14,'पाँच को पाँच',{'bg':bg('cel'),'figs':[F(('rudra' if i==0 else 'rudra%d'%(i+1)),CX-440+i*220,660,1.15,pose='stand',tail=False,aura=RGB5[i],key='255,214,160') for i in range(5)],'fx':[{'t':'name','s':'पाँच इंद्रियाँ','x':CX,'y':215,'c':0,'d':0.6,'size':42}]},'cel',cues=['इंद्रियाँ'])
add(14,'और पाँच',{'bg':bg('cel'),'figs':[F(('rudra%d'%(i+6)),CX-440+i*220,660,1.15,pose='stand',tail=False,aura=['255,120,60','100,170,255','110,200,110','200,230,255','190,150,255'][i],key='255,214,160') for i in range(5)],'fx':[{'t':'name','s':'पाँच तत्व','x':CX,'y':215,'c':0,'d':0.6,'size':42}]},'cel',cues=['तत्व'])
add(14,'रुद्र चले',{'bg':bg('cel',warm=True),'figs':[F(('rudra' if i==0 else 'rudra%d'%i),CX-525+i*105,560,0.8,tail=False,fo=0,fd=2.0,vy=-6,key='255,214,160') for i in range(11)]+[F('brahma',CX,740,1.1,expr={'mouth':0.1})]},'warm',cues=['गए'])
add(14,'ब्रह्मा फिर',{'bg':bg('cel',fy=660),'figs':[F('brahma',CX,640,1.25,aura='190,190,255',expr={'eye':0.8,'mouth':-0.3})]},'dark',cam=z(1.2,1.0,0,0,-30,0))
add(14,'तब उन्हें',{'bg':bg('cel'),'figs':[F('brahma',CX-320,700,1.5,expr={'brow':0.4})],'fx':[{'t':'icon','i':'flame','x':CX+170,'y':380,'sc':1.8,'c':0,'d':0.6},{'t':'icon','i':'lotusI','x':CX+420,'y':380,'sc':1.8,'c':1,'d':0.6}]},'cel',cues=['विनाश','सृजन'])
add(14,'ये काम',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'brow':0.6,'eye':1.1,'mouth':0.0})]},'cel')
add(14,'उन्होंने फिर',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,690,1.6,aura='255,225,170',pose='fist',expr={'brow':-0.4,'mouth':0.2})],'fx':[{'t':'glow','x':CX,'y':450,'r':300,'rgb':'255,225,170','c':0,'d':1.5,'ga':0.5}]},'warm',cues=['कमर'])
add(14,'पर आख़िरी',{'bg':bg('storm',r=0.35),'figs':[F('brahma',CX,690,1.5,aura='255,80,40',expr={'brow':0.3,'eye':1.1})],'fx':[{'t':'crack','x':CX+260,'c':0,'d':0.8}]},'red',cues=['बाक़ी'])
# ---------------- B15
add(15,0,{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,700,1.6,pose='cross',aura='255,225,170',expr={'eye':0.2,'mouth':0.2})],'fx':[{'t':'sparkle','x':CX,'y':400,'n':26,'rx':420,'ry':200}]},'warm',dx=0.6)
RN=['वशिष्ठ','मरीचि','अत्रि','अंगिरा','पुलस्त्य','पुलह','क्रतु']
add(15,'वशिष्ठ',{'bg':bg('cel',warm=True),'figs':[F('rishi%d'%i,CX-480+i*160,610,1.15,pose='namaste',tail=False,ac=i,ad=0.5) for i in range(7)],'fx':[{'t':'name','s':RN[i],'x':CX-480+i*160,'y':640,'c':i,'d':0.4,'size':26} for i in range(4)]},'warm',cues=RN[:4])
add(15,'पुलस्त्य',{'bg':bg('cel',warm=True),'figs':[F('rishi%d'%i,CX-480+i*160,610,1.15,pose='namaste',tail=False,ac=(i-4 if i>=4 else None),ad=0.5) for i in range(7)],'fx':[{'t':'name','s':RN[i],'x':CX-480+i*160,'y':640,'c':(i-4 if i>=4 else None),'d':0.4,'size':26} for i in range(7)]},'warm',cues=RN[4:])
add(15,'यही',{'bg':bg('night'),'figs':[],'fx':[{'t':'threads','x':CX-300,'y':300,'to':[[CX-170,220],[CX-60,260]],'c':0,'d':0.8}]},'night',cues=['सप्तर्षि'])
S[-1]['sc']['fx']=[{'t':'glow','x':x,'y':y,'r':60,'rgb':'255,240,190','ga':0.9,'c':0,'d':0.8} for x,y in [(300,200),(430,230),(560,270),(690,310),(800,230),(910,170),(1010,250)]]+[{'t':'text','s':'सप्तर्षि','x':CX,'y':480,'size':64,'c':0,'d':1.0,'glow':'rgba(255,230,170,.7)'}]
add(15,'यही',{'bg':bg('night'),'figs':[F('rishi%d'%i,CX-480+i*160,610,1.1,pose='cross',tail=False,aura='255,240,190') for i in range(7)]},'night',cues=['सप्तर्षि'])
S.pop(-2)  # keep the star-pattern shot? (replace with constellation + rishis combined)
# ---------------- B16
add(16,0,{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,985,3.1,aura='255,225,170',expr={'eye':0.3,'mouth':0.3})],'fx':[{'t':'glow','x':CX,'y':660,'r':220,'rgb':'255,220,160','ga':0.6}]},'warm',dx=0.6)
add(16,'धर्म का',{'bg':bg('cel',warm=True),'figs':[F('bull',CX,700,1.9,ac=0,ad=1.2,aura='255,230,170')]},'warm',cues=['बैल'])
add(16,'चार पैर',{'bg':bg('cel',warm=True),'figs':[F('bull',CX,700,1.8)],'fx':[{'t':'name','s':n,'x':CX-300+i*200,'y':220,'c':i,'d':0.5,'size':34} for i,n in enumerate(['सत्य','तप'])]},'warm',cues=['सत्य','तप'])
add(16,'पवित्रता',{'bg':bg('cel',warm=True),'figs':[F('bull',CX,700,1.8)],'fx':[{'t':'name','s':n,'x':CX-300+i*200,'y':220,'c':(i-2 if i>=2 else None),'d':0.5,'size':34} for i,n in enumerate(['सत्य','तप','पवित्रता','करुणा'])]},'warm',cues=['पवित्रता','करुणा'])
add(16,'ब्रह्मा ने भविष्य',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'brow':0.5,'mouth':-0.2})]},'dark')
add(16,'सतयुग',{'bg':bg('dawn'),'figs':[F('bull',CX,700,1.9,aura='255,240,200')],'fx':[{'t':'name','s':'सतयुग · ४ पैर','x':CX,'y':200,'c':0,'d':0.4,'size':38,'col':'#fff'}]},'warm',cues=['सतयुग'])
add(16,'त्रेता',{'bg':bg('dusk'),'figs':[F('bull',CX,700,1.9,l1=0)],'fx':[{'t':'name','s':'त्रेता · ३ पैर','x':CX,'y':200,'c':0,'d':0.4,'size':38,'col':'#ffb09a'}]},'amb',cues=['तप'])
S[-1]['sc']['figs'][0]['l1']=0
add(16,'द्वापर',{'bg':bg('amber'),'figs':[F('bull',CX,700,1.9,la0=[1,0,1,1],l2=0)],'fx':[{'t':'name','s':'द्वापर · २ पैर','x':CX,'y':200,'c':0,'d':0.4,'size':38,'col':'#ffd980'}]},'amb',cues=['पवित्रता'])
add(16,'और कलियुग',{'bg':bg('storm',r=0.2),'figs':[F('bull',CX,700,1.9,la0=[1,0,0,1],l3=0,key='170,170,210',rim='rgba(190,190,230,.7)')],'fx':[{'t':'name','s':'कलियुग · १ पैर','x':CX,'y':200,'c':0,'d':0.4,'size':38,'col':'#c7c7e8'}]},'dark',cues=['करुणा'])
add(16,'धर्म ने पूछा',{'bg':bg('storm',r=0.15),'figs':[F('bull',CX,700,2.0,la0=[1,0,0,0],bow=0.0,key='170,170,210',rim='rgba(190,190,230,.7)')]},'dark')
add(16,'ब्रह्मा ने बस',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':0.25,'brow':0.9,'mouth':-0.5})],'fx':[{'t':'tears','x':CX-60,'y':470,'dx':110,'len':120}]},'dark',cam=z(1.0,1.08,0,0,0,-15))
# ---------------- B17
add(17,0,{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,690,1.7,aura='255,225,170',pose='open')],'fx':[{'t':'sparkle','x':CX,'y':400,'n':34,'rx':500,'ry':220,'c':0,'d':0.6}]},'warm',cues=['प्रकट'],dx=0.4)
def birth(who,name,fx,at,cue):
    add(17,at,{'bg':bg('cel',warm=True),'figs':[F('brahma',CX-330,700,1.35,aura='255,225,170',expr={'mouth':0.2}),F(who,CX+300,700,1.55,pose='stand',ac=0,ad=0.8,key='255,214,160',aura=fx[0])],'fx':[{'t':'name','s':name,'x':CX+300,'y':170,'c':0,'d':0.5,'size':34}]+fx[1]},'warm',cues=[cue])
birth('agni','अग्नि',('255,120,50',[{'t':'flames','x':CX+300,'y':330,'sc':0.7,'c':0,'d':0.6}]),'अग्नि','अग्नि')
birth('kamadeva','कामदेव',('255,120,170',[{'t':'icon','i':'heart','x':CX+300,'y':320,'sc':1.0,'c':0,'d':0.6}]),'कामदेव','कामदेव')
birth('daksha','दक्ष',('255,230,160',[{'t':'glow','x':CX+300,'y':430,'r':140,'rgb':'255,230,160','c':0,'d':0.7}]),'दक्ष','दक्ष')
birth('vishwakarma','विश्वकर्मा',('200,230,255',[{'t':'sparkle','x':CX+300,'y':430,'n':16,'rx':150,'ry':120,'c':0,'d':0.6}]),'विश्वकर्मा','विश्वकर्मा')
add(17,'और नारद',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX-330,700,1.35,aura='255,225,170'),F('narada',CX+300,700,1.55,pose='stand',ac=0,ad=0.8,key='255,214,160',aura='255,235,190')],'fx':[{'t':'name','s':'नारद','x':CX+300,'y':170,'c':0,'d':0.5,'size':36},{'t':'glow','x':CX+300,'y':400,'r':120,'rgb':'255,240,200','c':1,'d':0.7}]},'warm',cues=['नारद','कंठ'])
# ---------------- B18
add(18,0,{'bg':bg('cel',warm=True),'figs':[F('brahma',CX-300,700,1.45,pose='open',expr={'mouth':0.3,'eye':0.6}),F('narada',CX+300,700,1.6,pose='stand',flip=-1,key='255,214,160')]},'warm',dx=0.5)
add(18,'जाओ पुत्र',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,985,3.1,aura='255,225,170',expr={'mouth':0.4,'eye':0.5})]},'warm')
add(18,'पर नारद',{'bg':bg('cel'),'figs':[F('narada',CX,430,3.4,head=True,expr={'brow':0.1,'mouth':-0.05,'eye':1})]},'cel')
add(18,'क्षमा',{'bg':bg('cel'),'figs':[F('narada',CX,660,1.8,pose='namaste',key='255,214,160',aura='255,235,190')]},'cel')
add(18,'जन्म',{'bg':bg('cosmos',rgb='170,130,255'),'figs':[F('narada',CX-330,700,1.5,pose='stand',key='200,200,255')],'fx':[{'t':'icon','i':'vortex','x':CX+250,'y':320,'sc':3.0,'c':0,'d':0.8}]},'void',cues=['भँवर'])
add(18,'मुझे नारायण',{'bg':bg('cel',warm=True),'figs':[F('narada',CX-330,700,1.5,pose='open',key='255,214,160')],'fx':[{'t':'icon','i':'vaikuntha','x':CX+250,'y':330,'sc':2.8,'c':0,'d':0.8}]},'warm',cues=['नारायण'])
add(18,'आप मुझे',{'bg':bg('cel'),'figs':[],'fx':[{'t':'icon','i':'body','x':CX-300,'y':340,'sc':2.4,'c':0,'d':0.6},{'t':'icon','i':'light','x':CX+300,'y':340,'sc':2.4,'c':1,'d':0.6},{'t':'text','s':'देह','x':CX-300,'y':480,'size':44,'c':0},{'t':'text','s':'चेतना','x':CX+300,'y':480,'size':44,'c':1}]},'cel',cues=['देह','चेतना'])
# ---------------- B19
add(19,'बस',{'bg':bg('voidR'),'figs':[F('brahma',CX,985,3.1,aura='255,60,30',key='255,90,50',rim='rgba(255,170,110,.95)',expr={'brow':-1,'mouth':-1,'eye':1.25,'open':0.4})],'fx':[{'t':'flash','c':0,'w':0.3,'rgb':'255,200,160'}]},'red',cues=['ब्रह्मा'],shake=5,dx=0.12)
add(19,'पहले',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'icon','i':'asuras','x':CX-300,'y':330,'sc':2.2,'c':0,'d':0.5},{'t':'icon','i':'kids','x':CX+300,'y':330,'sc':2.2,'c':1,'d':0.5}]},'red',cues=['मधु','कुमारों'],shake=2)
add(19,'फिर रुद्र',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'icon','i':'trident','x':CX-250,'y':330,'sc':2.4,'c':0,'d':0.5},{'t':'icon','i':'person','x':CX+250,'y':330,'sc':2.6,'c':1,'d':0.5},{'t':'shock','x':CX+250,'y':330,'c':1,'rgb':'255,120,80','max':500}]},'red',cues=['रुद्र','बेटा'],shake=3)
add(19,'क्रोध ने',{'bg':bg('voidR',gx=CX,gy=300),'figs':[F('brahma',CX,985,3.1,aura='255,60,30',key='255,90,50',rim='rgba(255,170,110,.95)',expr={'brow':-1,'mouth':-0.7,'eye':0.25})]},'red',shake=3)
add(19,'और उनके',{'bg':bg('voidR'),'figs':[F('brahma',CX-330,700,1.5,pose='point',aura='255,60,30',key='255,90,50',rim='rgba(255,170,110,.95)',expr={'brow':-1,'mouth':-0.7}),F('narada',CX+330,700,1.5,pose='stand',key='255,140,110',flip=-1)],'fx':[{'t':'ribbon','c':0,'x0':CX-250,'y0':380,'x1':CX+300,'y1':430,'dur':1.4}]},'red',cues=['श्राप'],shake=2)
add(19,'नारद',{'bg':bg('voidR'),'figs':[F('narada',CX,430,3.4,head=True,key='255,140,110',expr={'eye':1.3,'open':0.3,'brow':0.8})],'fx':[{'t':'ribbon','c':0,'x0':-100,'y0':250,'x1':CX,'y1':400,'dur':0.8},{'t':'flash','c':1,'w':0.25,'rgb':'255,170,230'}]},'red',cues=['नारद','तू'],shake=4)
add(19,'तू गंधर्व',{'bg':bg('cosmos',rgb='190,90,255'),'figs':[F('narada',CX,690,1.7,pose='open',key='230,170,255',aura='190,90,255')],'fx':[{'t':'sparkle','x':CX,'y':420,'n':30,'rx':260,'ry':200}]},'void')
add(19,'अगर सब',{'bg':bg('voidR'),'figs':[F('brahma',CX,985,3.1,aura='255,60,30',expr={'brow':0.9,'mouth':-0.5,'eye':1.2,'open':0.25},key='255,120,90')]},'red')
# ---------------- B20
add(20,0,{'bg':bg('cel'),'figs':[F('brahma',CX-300,700,1.4,expr={'eye':1.2,'brow':0.8,'open':0.3},dark=0.7),F('narada',CX+300,700,1.5,key='255,214,160',dark=0.7,flip=-1)],'fx':[{'t':'dim','ga':0.35}]},'dark',dx=0.5)
add(20,'और तब',{'bg':bg('cel'),'figs':[F('narada',CX,430,3.4,head=True,expr={'brow':-0.5,'eye':0.9,'mouth':-0.1})]},'cool')
add(20,'बेटे ने',{'bg':bg('voidR',rgb='150,90,255'),'figs':[F('narada',CX+300,700,1.8,pose='point',flip=-1,key='230,170,255',aura='170,100,255',expr={'brow':-0.7}),F('brahma',CX-330,720,1.2,expr={'eye':1.2,'brow':0.8},dark=0.8)],'fx':[{'t':'shock','x':CX+300,'y':500,'c':0,'rgb':'190,100,255','max':800}]},'void',cues=['श्राप'],shake=2)
add(20,'जिस तरह',{'bg':bg('voidR',rgb='150,90,255'),'figs':[F('narada',CX,430,3.5,head=True,key='230,170,255',expr={'brow':-0.8,'mouth':-0.4,'eye':1.1})]},'void')
add(20,'उसी तरह',{'bg':bg('voidR'),'figs':[F('brahma',CX,985,3.1,aura='255,60,30',expr={'eye':1.2,'brow':0.8,'open':0.2})]},'red')
add(20,'आप उसकी',{'bg':bg('voidR',rgb='255,120,170'),'figs':[F('brahma',CX-330,700,1.4,expr={'brow':0.6}),F('kamadeva',CX+300,700,1.5,dark=0.5,key='255,150,190',ac=0,ad=1.0,a=0.0)],'fx':[{'t':'icon','i':'heart','x':CX+300,'y':300,'sc':1.6,'c':0,'d':0.8}]},'red',cues=['कामना'])
add(20,'और उसकी',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'scales','x':CX,'y':330,'c':0,'d':0.6}]},'dark',cues=['चुकाएँगे'])
S[-1]['sc']['fx']=[{'t':'scales','x':CX,'y':330,'c':0,'d':0.6},{'t':'text','s':'क़ीमत','x':CX,'y':560,'size':60,'c':0,'d':0.8,'glow':'rgba(255,100,70,.7)'}]
add(20,'आप उसकी',{'bg':bg('voidR'),'figs':[F('brahma',CX,985,3.1,aura='255,60,30',expr={'brow':0.9,'mouth':-0.6,'eye':1.3,'open':0.3})]},'red',shake=3)
S.pop()
# ---------------- B21
add(21,0,{'bg':bg('cosmos',spin=0.5,rgb='255,120,100'),'figs':[],'fx':[{'t':'shock','x':CX,'y':360,'c':0,'rgb':'255,150,130','max':900}]},'void',cues=['सिकुड़'],cam=z(1.3,0.9,0,0,0,0),dx=0.4)
add(21,'तीनों',{'c1':-1,'c2':-1,'cv':-1,'c3':-1,'c4':-1,'c5':-1,'c6':-1,'pan':[(None,1000)]},'red',draw='tower',shake=6)
add(21,'इतिहास',{'bg':bg('voidR',rgb='255,100,80'),'figs':[F('brahma',CX-330,700,1.4,expr={'brow':0.8,'eye':1.1}),F('narada',CX+330,700,1.5,flip=-1,key='255,140,110',expr={'brow':-0.7})],'fx':[{'t':'bolt','x0':CX-250,'y0':430,'x1':CX+250,'y1':430,'at':1.0,'w':0.4}]},'red',shake=2)
add(21,'नारद के',{'bg':bg('storm',r=0.5),'figs':[F('narada',CX,640,1.6,key='255,140,110',fo=0,fd=3.0,vx=-4,ds=-0.08)]},'dark',cues=['चले'])
# ---------------- B22
add(22,0,{'bg':bg('cel',fy=660),'figs':[F('brahma',CX,640,1.2,aura='170,170,230',expr={'eye':0.7,'mouth':-0.4})]},'dark',cam=z(1.3,1.0,0,0,-30,0),dx=0.7)
add(22,'उनकी आँखों',{'bg':bg('cel'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':0.3,'brow':0.9,'mouth':-0.5})],'fx':[{'t':'tears','x':CX-60,'y':470,'dx':110,'len':140}]},'dark')
add(22,'दुख इतना',{'bg':bg('cel'),'figs':[F('brahma',CX,690,1.7,aura='170,170,230',dark=0.75,expr={'eye':0.3,'brow':0.8,'mouth':-0.4})],'fx':[{'t':'petals','n':9,'x':CX,'y':640,'sp':40,'len':220,'c':0}]},'dark',cues=['पंखुड़ियाँ'])
add(22,'उन्हें लगा',{'bg':bg('night'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':0.7,'brow':0.9,'mouth':-0.3,'tilt':0.04})]},'night',cam=z(1.0,1.1,0,0,0,-20))
# ---------------- B23
add(23,0,{'bg':bg('night'),'figs':[F('brahma',CX,650,1.4,aura=None,dark=0.6,expr={'eye':0.7,'mouth':-0.2})],'fx':[{'t':'glow','x':CX,'y':160,'r':120,'rgb':'255,240,200','c':0,'d':2.0,'ga':0.5}]},'night',cues=['मदद'],dx=0.6)
add(23,'एक ऐसी',{'bg':bg('dawn'),'figs':[F('brahma',CX,690,1.5,aura='255,230,170',expr={'eye':1.2,'mouth':0.1,'brow':0.5})],'fx':[{'t':'beam','x':CX,'y':140,'len':600,'w':40,'c':0,'d':1.0},{'t':'flash','c':0,'w':0.3,'rgb':'255,240,210'}]},'warm',cues=['जगह'],cam=z(1.0,1.1,0,0,0,-10))
add(23,'जिसकी',{'bg':bg('night'),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'eye':1.2,'brow':0.6,'mouth':0.0})],'fx':[{'t':'glow','x':CX,'y':100,'r':260,'rgb':'255,235,190','ga':0.6,'pulse':1}]},'warm')
# ---------------- B24
add(24,0,{'bg':bg('cosmos',rgb='200,160,255'),'figs':[],'fx':[{'t':'text','s':'?','x':CX,'y':330,'size':260,'c':0,'d':1.0,'glow':'rgba(255,230,170,.8)'}]},'void',cues=['कौन'],dx=0.6)
add(24,'अगली',{'bg':bg('dawn'),'figs':[],'fx':[{'t':'outline','x':CX,'y':520,'sc':1.6,'c':0,'d':1.6}]},'warm',cues=['मनुष्य'])
add(24,'कल',{'bg':bg('night'),'figs':[],'fx':[{'t':'text','s':'कल मिलते हैं','x':CX,'y':330,'size':74,'c':0,'d':1.4,'glow':'rgba(255,220,160,.7)'},{'t':'sparkle','x':CX,'y':330,'n':26,'rx':380,'ry':110,'a':0.7}]},'warm',cues=['मिलते'])
# order shots by beat (stable)
S2=[];
for b in range(1,25):
    S2+= [s for s in S if s['beat']==b]
json.dump(S2,open(os.path.join(HERE,'shots.json'),'w'),ensure_ascii=False,indent=0)
print(len(S2),'shots')
