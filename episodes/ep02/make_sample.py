import json
C={'cel':'rgba(190,200,255,0.16)','warm':'rgba(255,190,120,0.16)','red':'rgba(255,60,30,0.20)','night':'rgba(60,90,170,0.20)','pal':'rgba(255,170,90,0.14)','cool':'rgba(80,160,200,0.16)'}
def z(a,b,x0=0,x1=0,y0=0,y1=0,r0=0,r1=0): return {"from":{"z":a,"x":x0,"y":y0,"r":r0},"to":{"z":b,"x":x1,"y":y1,"r":r1}}
S=[]
def add(beat,at,draw,cam,grade,**k):
    d={"beat":beat,"at":at,"draw":draw,"cam":cam,"grade":grade}; d.update(k); S.append(d)
# ---- beat 6: Kumaras born
add(6,0,'establish',z(1.28,1.0,0,0,110,0),C['cel'],dx=0.8)
add(6,'और','brahmaClose',z(1.0,1.1,0,0,0,-20),C['cel'])
add(6,'चार','orbs',z(1.05,1.0,0,0,-60,50),C['cel'])
add(6,'सनक','kShot',z(1.0,1.1,-60,40,0,0,-0.012,0.01),C['cel'],i=0,x=640)
add(6,'सनंदन','kShot',z(1.12,1.0,0,0,0,0,0.01,-0.01),C['cel'],i=1,x=760,nx=760,bgx=-120)
add(6,'सनातन','kShot',z(1.0,1.12,60,-40,0,0),C['cel'],i=2,x=520,nx=520,bgx=120)
add(6,'सनत्कुमार','kShot',z(1.1,1.0,0,0,30,0),C['cel'],i=3,x=640)
add(6,'मन से','kLine',z(1.14,1.0,0,0,-20,0),C['warm'],cues=['मानसपुत्र'])
add(6,'हृदय','brahmaWarm',z(1.0,1.1,0,0,0,-30),C['warm'])
add(6,'पुत्रों','sendoff',z(1.0,1.05,0,0,70,-30),C['warm'],dx=0.4)
# ---- beat 9: Rudra born
add(9,0,'rageRise',z(1.0,1.16,0,0,0,-20),C['red'],dx=0.9)
add(9,'और फिर','rageFace',z(1.0,1.08,0,0,0,0),C['red'],shake=3)
add(9,'माथे','beam',z(1.0,1.0,0,0,170,-260),C['red'],shake=2)
add(9,'उस आग','fireForm',z(1.0,1.14,0,0,60,-40),C['red'],shake=2)
add(9,'दहकती','rudraEyes',z(1.0,1.07,0,0,0,0),C['red'],shake=2)
add(9,'गर्जना','roar',z(1.04,1.0,0,0,0,0),C['red'],shake=5)
add(9,'मेरा','nameQ',z(1.0,1.1,-50,30,0,0),C['red'],cues=['मेरा'])
# ---- beat 10: name + trimurti
add(10,0,'brahmaStun',z(1.0,1.08,0,0,0,0),C['red'])
add(10,'बताओ','eyesAsk',z(1.0,1.06,0,0,0,0),C['red'],shake=2)
add(10,'तब','think',z(1.0,1.08,-30,20,0,0),C['cool'],cues=['रुद्'])
add(10,'लाल','redRoar',z(1.06,1.0,0,0,0,0),C['red'],cues=['लाल','गरजना'])
add(10,'तुम्हारा','nameHero',z(1.0,1.12,0,0,90,-30),C['red'],cues=['रुद्र'],dx=0.5)
add(10,'यही','faceTwo',z(1.1,1.0,0,0,0,0,0.02,-0.02),C['red'])
add(10,'शिव','shivaMoon',z(1.0,1.1,0,0,0,-20),C['night'],dx=0.5)
add(10,'महादेव','shivaPeak',z(1.35,1.0,0,0,-60,0),C['night'])
add(10,'ब्रह्मा','palaceWide',z(1.12,1.0,0,0,0,0),C['pal'],cues=['रचयिता'],dx=0.7)
add(10,'विष्णु','palaceCU',z(1.7,1.55,0,0,-40,-30),C['pal'],who=1)
add(10,'और शिव','palaceCU',z(1.7,1.55,410,380,-40,-30),C['pal'],who=2)
add(10,'सृष्टि','trimurti',z(1.3,1.0,0,0,-60,0),C['pal'],cues=['त्रिमूर्ति'])
json.dump(S,open('sample_shots.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots')
