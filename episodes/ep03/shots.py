import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','studio'))
from shotkit import *
HERE=os.path.dirname(os.path.abspath(__file__));f=Film();add=f.add
GL='rgba(255,230,170,.8)'
# ---- B01: Daksha's yagna
add(1,0,{'bg':bg('cel',warm=True),'figs':[F('daksha',CX,700,1.7,aura='255,225,170',expr={'eye':1})],'fx':[{'t':'sparkle','x':CX,'y':420,'n':26,'rx':420,'ry':200}]},'warm',dx=0.6)
add(1,'सप्तऋषि',{'bg':bg('cel',warm=True),'figs':[F('rishi%d'%i,CX-480+i*160,610,1.15,pose='namaste',tail=False) for i in range(7)],'fx':[]},'warm')
add(1,'पूरा',{'bg':bg('cosmos',rgb='255,210,140'),'figs':[],'fx':[{'t':'text','s':'ॐ','x':CX,'y':330,'size':220,'c':0,'d':1.0,'glow':GL},{'t':'sparkle','x':CX,'y':330,'n':30,'rx':420,'ry':160}]},'void',cues=['भक्ति'])
# ---- B02: Shiva storms in
add(2,0,{'bg':bg('storm',r=0.4),'figs':[],'fx':[{'t':'text','s':'शिव!','x':CX,'y':330,'size':150,'c':0,'d':0.5,'glow':'rgba(120,150,255,.9)'},{'t':'flash','c':0,'w':0.3,'rgb':'170,190,255'}]},'dark',cues=['शिव'],shake=3)
add(2,'मंत्रों',{'bg':bg('night'),'figs':[F('shiva',CX,430,3.4,head=True,key='200,220,255',expr={'eye':0.3,'brow':-0.4,'mouth':-0.3})]},'night')
add(2,'वे',{'bg':bg('voidR'),'figs':[F('shiva',CX,700,1.9,pose='tri',key='255,150,120',aura='255,60,30',expr={'brow':-0.9,'mouth':-0.5})],'fx':[{'t':'flames','x':CX-320,'y':690,'sc':1.3,'c':0},{'t':'flames','x':CX+320,'y':690,'sc':1.3,'c':0}]},'red',shake=2)
add(2,'दक्ष',{'bg':bg('storm',r=0.5),'figs':[F('daksha',CX-250,640,1.5,key='255,140,110',fo=0,fd=3.0,vx=-5,ds=-0.08),F('rishi0',CX+150,640,1.2,pose='namaste',tail=False,fo=0,fd=3.0,vx=-4,ds=-0.08),F('rishi3',CX+400,640,1.2,pose='namaste',tail=False,fo=0,fd=3.0,vx=-4,ds=-0.08)]},'dark')
add(2,'पर',{'bg':bg('cel',fy=660),'figs':[F('vishnu',CX,700,1.9,aura='120,170,255',expr={'brow':0.3})]},'cool')
# ---- B03: the battle and Brahma's plea
add(3,0,{'bg':bg('voidR'),'figs':[F('shiva',CX-330,700,1.7,pose='tri',key='200,220,255',expr={'brow':-0.7}),F('vishnu',CX+330,700,1.7,flip=-1,key='160,200,255',expr={'brow':-0.5})],'fx':[{'t':'bolt','x0':CX-200,'y0':300,'x1':CX+200,'y1':420,'c':0},{'t':'shock','x':CX,'y':400,'c':0,'rgb':'255,200,150','max':700}]},'red',cues=['युद्ध'],shake=4)
add(3,'आकाशगंगाएँ',{'bg':bg('cosmos',spin=0.6,rgb='150,170,255'),'figs':[],'fx':[{'t':'shock','x':CX,'y':360,'c':0,'rgb':'170,190,255','max':900}]},'void',cues=['काँप'],shake=5)
add(3,'समय',{'bg':bg('cosmos',rgb='170,150,255'),'figs':[],'fx':[{'t':'icon','i':'cycle','x':CX,'y':330,'sc':2.8,'c':0,'d':0.8}]},'night',cues=['थम'])
add(3,'ब्रह्मा',{'bg':bg('cel',fy=660),'figs':[F('brahma',CX,985,3.1,aura=None,expr={'brow':0.9,'mouth':-0.3,'eye':1.2})]},'dark')
add(3,'आप',{'bg':bg('cel'),'figs':[F('brahma',CX-380,720,1.4,aura='255,225,170',expr={'brow':0.5})],'fx':[{'t':'scales','x':CX+250,'y':340,'c':0,'d':0.6}]},'cel',cues=['बराबर'])
add(3,'यह',{'bg':bg('voidR'),'figs':[],'fx':[{'t':'infinity','x':CX,'y':320,'c':0,'d':0.8}]},'red',cues=['कभी'])
# ---- B04: Harihara
add(4,0,{'bg':bg('dawn'),'figs':[F('shiva',CX-330,700,1.6,key='255,230,200'),F('vishnu',CX+330,700,1.6,flip=-1,key='255,230,200')]},'warm',dx=0.7)
add(4,'ब्रह्मा',{'bg':bg('cel',warm=True),'figs':[F('brahma',CX,985,3.1,aura='255,225,170',expr={'mouth':0.5,'eye':0.5,'brow':0.2})]},'warm')
add(4,'हरि',{'bg':bg('cel'),'figs':[F('vishnu',CX-330,520,2.6,head=True,key='200,220,255'),F('shiva',CX+330,520,2.6,head=True,key='200,220,255')],'fx':[{'t':'text','s':'हरि','x':CX-330,'y':680,'size':80,'c':0,'d':0.5,'glow':GL},{'t':'text','s':'हर','x':CX+330,'y':680,'size':80,'c':1,'d':0.5,'glow':GL}]},'cel',cues=['हरि','हर'])
add(4,'दोनों',{'bg':bg('dawn'),'figs':[],'fx':[{'t':'text','s':'हरि = हर','x':CX,'y':340,'size':96,'c':0,'d':0.8,'glow':GL}]},'warm')
add(4,'हरिहर',{'bg':bg('cosmos',rgb='255,210,150'),'figs':[F('vishnu',CX-120,700,1.7,aura='140,180,255'),F('shiva',CX+120,700,1.7,key='200,220,255',aura='170,160,255')],'fx':[{'t':'text','s':'हरिहर','x':CX,'y':200,'size':120,'c':0,'d':1.0,'glow':GL},{'t':'sparkle','x':CX,'y':420,'n':30,'rx':420,'ry':220}]},'amb',cues=['हरिहर'])
print(f.save(os.path.join(HERE,'shots.json')),'shots')
