#!/usr/bin/env python3
"""Generator for reels/reel07/briefs.json "Daksha Cursed Narada" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel04/briefs_gen.py: hero faces solved to 38-50% of the 9:16 frame height, narration = the spoken words.
Crowds (the 5,000 Haryashvas, the 1,000 Shavalashvas) are rows of the haryashva / shavalashva rigs: small figures in rows that recede
(smaller, higher and fainter = farther), placed by hand ('_fixed'), never moved by the face solver."""
import json,os
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel07/words.json'))
T=[(w['w'],w['start']) for w in W]
END=76.59
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette (bright, clean) ----------
SKY_GOLD=['#2a5cc4','#7ab0ee','#ffdca8','#fff6e2']          # Daksha's palace, clear morning
SKY_MEM=['#4a3c9c','#8a80d4','#e4cdf2','#fff2f6']           # loss / memory lavender
SKY_DIV=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']           # Narada's sky
SKY_SEA=['#2466c8','#6ab0ee','#c8ecfa','#fff8e8']           # river mouth, bright
SKY_DAWN=['#3a4ab0','#8a94dc','#ffbc8c','#ffeac4']          # sunrise road
SKY_COOL=['#2a3a8c','#5c72bc','#b4bce4','#eaeef8']          # doubt
SKY_RAGE=['#8a2a3a','#d0604a','#ffa878','#ffe4b8']          # Daksha's anger (bright, warm red)
SKY_DUSK=['#0e1240','#3a3a8a','#c88aa0','#ffd4a4']          # wandering, first stars
RIDGE_DAY=['#a8c4e4','#8ab4cc','#6aa08a','#4a8064']
RIDGE_DAWN=['#b4b4dc','#9a9ac8','#7a8aa8','#5a6a88']
STONE='#ecd8b4';WALL='#f2d6a2';GOLD='#e8c878'
def vista(sky=SKY_GOLD,sx=640,sy=250,ridge=RIDGE_DAY,**k):
    d={"k":"vista","sky":sky,"sx":sx,"sy":sy,"ridge":ridge,"haze":"240,244,255","dust":14};d.update(k);return d
def cloud_bg(sky=SKY_DIV,sx=640,sy=200):return {"k":"cloudscape","sky":sky,"sx":sx,"sy":sy}
# ---------- layers ----------
def far_sky(xs=(500,800),haze='#eef2fa',col='#ffffff',mcol='#9aaad8'):
    return {"d":"far","contents":"hazy blue peaks and white clouds far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-40,"y":420,"s":0.9,"w":260,"h":200,"col":mcol,"snow":False},{"o":"mountain","x":xs[1]+40,"y":430,"s":0.8,"w":240,"h":170,"col":mcol,"snow":False},
                     {"o":"cloud","x":xs[0],"y":200,"s":1.2,"col":col},{"o":"cloud","x":xs[1],"y":250,"s":1.0,"col":col}]}
def mid_court(cx=640,wy=450,ws=0.62,px=None,floor=STONE,lamp=False):
    """Daksha's palace: an arched sandstone wall far back, two gold pillars, a pale stone courtyard floor"""
    px=px or (cx-200,cx+200)
    return {"d":"mid","contents":"Daksha's palace: arched sandstone wall, gold pillars and a pale stone courtyard","fog":0.2,
            "items":[{"o":"wall","x":cx,"y":wy+6,"s":ws,"w":1300,"h":330,"col":WALL},{"o":"hill","x":cx,"y":wy,"s":1.0,"w":1000,"h":8,"col":floor},
                     {"o":"pillar","x":px[0],"y":wy+190,"s":1.0,"col":GOLD,"h":560},{"o":"pillar","x":px[1],"y":wy+190,"s":1.0,"col":GOLD,"h":560}]}
def near_court(xs=(450,830)):
    return {"d":"near","contents":"flowering shrubs in brass-rimmed planters low in the bottom corners","dark":0.35,"blur":2,
            "items":[{"o":"shrub","x":xs[0],"y":752,"s":1.5,"col":"#2e6a3e","flowers":"#f0a020"},{"o":"shrub","x":xs[1],"y":752,"s":1.4,"col":"#2e6a3e","flowers":"#ff7a9a"}]}
def near_clouds(xs=(470,810)):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":748,"s":1.7,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":750,"s":1.6,"col":"#ffffff"}]}
def far_sea(xs=(480,820),y=372):
    return {"d":"far","contents":"the blue sea on the horizon with pale headlands and clouds","fog":0.35,"haze":"#eef6fc",
            "items":[{"o":"mountain","x":xs[0]-60,"y":y+4,"s":1.0,"w":200,"h":70,"col":"#9ab8c8","snow":False},
                     {"o":"cloud","x":xs[0],"y":190,"s":1.1,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":240,"s":0.9,"col":"#ffffff"},
                     {"o":"hill","x":640,"y":y,"s":1.0,"w":1500,"h":4,"col":"#3a94dc"}]}
def mid_shore(rx=(830,700),sand_y=440,trees=(430,880)):
    """sand bank of the Sindhu; the river (a 'road' drawn as water) runs from the front into the sea"""
    return {"d":"mid","contents":"golden sand bank of the River Sindhu, the blue river flowing out into the sea, palms","fog":0.15,"par":1.0,
            "items":[{"o":"hill","x":640,"y":sand_y,"s":1.0,"w":1100,"h":14,"col":"#f2dca8"},
                     {"o":"road","x":rx[0],"y":740,"s":1.0,"w":170,"ex":rx[1],"ey":378,"ew":34,"bend":-60,"col":"#4aaae6","plain":True},
                     {"o":"tree","x":trees[0],"y":sand_y+30,"s":0.62,"kind":"palm","col":"#2e7a44"},{"o":"tree","x":trees[1],"y":sand_y+40,"s":0.58,"kind":"palm","col":"#2e7a44"}]}
def near_reeds(xs=(450,830),col='#2a5a3a'):
    return {"d":"near","contents":"dark blurred reeds and shrubs in the bottom corners","dark":0.45,
            "items":[{"o":"shrub","x":xs[0],"y":750,"s":1.5,"col":col,"flowers":"#f0c040"},{"o":"shrub","x":xs[1],"y":752,"s":1.4,"col":col}]}
def far_hills(haze='#f6eee6',xs=(480,820),col='#a4a8d0'):
    return {"d":"far","contents":"soft blue-violet hills in haze on the horizon","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0],"y":392,"s":1.0,"w":240,"h":110,"col":col,"snow":False},{"o":"mountain","x":xs[1],"y":396,"s":1.0,"w":220,"h":90,"col":col,"snow":False},
                     {"o":"cloud","x":xs[0]+40,"y":190,"s":1.0,"col":"#fff4ec"}]}
def mid_road(x=600,ex=760,ey=380,w=190,glow=None,grass='#7aa860',trees=(430,900),bend=40):
    r={"o":"road","x":x,"y":740,"s":1.0,"w":w,"ex":ex,"ey":ey,"ew":4,"bend":bend,"col":"#efd6a0"}
    if glow:r["glow"]=glow
    return {"d":"mid","contents":"green fields and a pale dusty road running to the horizon","fog":0.12,"par":1.0,
            "items":[{"o":"hill","x":640,"y":ey+4,"s":1.0,"w":1100,"h":10,"col":grass},r,
                     {"o":"tree","x":trees[0],"y":ey+150,"s":0.6,"kind":"round","col":"#3a7a44"},{"o":"tree","x":trees[1],"y":ey+120,"s":0.5,"kind":"round","col":"#3a7a44"}]}
def name(word,s,x=640,y=128,size=30):return {"k":"name","word":word,"s":s,"x":x,"y":y,"size":size,"meaning":f"the name {s} on screen the moment it is spoken"}
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!"')}};s.update(k);return s
def cam(move,a,b,shot_='medium',lens='normal',shake=0,mot='',r=(0,0)):
    z0,x0,y0=a;z1,x1,y1=b
    return {"shot":shot_,"lens":lens,"move":move,"from":{"z":z0,"x":x0,"y":y0,"r":r[0]},"to":{"z":z1,"x":x1,"y":y1,"r":r[1]},"shake":shake,"motivation":mot}
# ---------- crowd rows ----------
EMOS=['calm','joy','calm','doubt']
def crowd(who,rows,look=None,emos=EMOS,acts=None,cues=None,eng=None,flipto=None,mood=None):
    """rows = [(feet_y, s, xs, alpha)] listed back to front; every figure is a real rig (emo + look), placed by hand"""
    out=[];n=0
    for (y,s,xs,a) in rows:
        for x in xs:
            e=emos[n%len(emos)];n+=1
            fl=flipto if flipto else ((1 if look>x else -1) if isinstance(look,(int,float)) else (1 if n%2 else -1))
            f={"who":who,"x":x,"y":y,"s":s,"flip":fl,"pose":"stand","emo":e,"look":look if look is not None else 640,"_fixed":True}
            if mood:f["mood"]=dict(mood)
            if acts:f["actions"]=[dict(a_) for a_ in acts]
            g=dict(eng or {})
            if a<1:g["a"]=a
            if g:f["engine"]=g
            if cues:f["engine_cues"]=dict(cues)
            out.append(f)
    return out
def row(cx,n,sp,jit=0):return [round(cx+(k-(n-1)/2)*sp+(jit if k%2 else -jit)) for k in range(n)]
S=[]
# 1 ---------------------------------------------------------------- title: Daksha, son of Brahma
S.append(shot("s01",0.16,
 meaning="This is Daksha, the son of Brahma, a proud king.",
 why="Daksha in his crimson dhoti and crown stands in his bright palace court under the title card, chin up with pride; a warm gold glow rises behind him on 'Brahma'.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-6),"medium","normal",0,"slow push in to meet the father of the story"),
 focus={"subject":"daksha","depth":"deep"},vertical={"focus":"daksha"},
 layers=[far_sky(),mid_court(),near_court()],
 background=vista(),mood={"emotion":"pride","grade":"warm"},
 characters=[{"who":"daksha","x":640,"y":690,"s":1.05,"_face":0.52,"flip":1,"pose":"stand","emo":"pride","look":700,"mood":{"smile":0.3},
   "actions":[{"word":"Brahma","pose":"open","emo":"pride","mood":{"smile":0.5},"d":0.6}]}],
 effects=[{"k":"glow","word":"Brahma","x":640,"y":300,"r":240,"rgb":"255,214,140","ga":0.45,"par":1.0,"behind":True,"meaning":"the golden light of a son of Brahma"}],
 transition_in="fade"))
# 2 ---------------------------------------------------------------- lost 6,000 sons, every single one
S.append(shot("s02",2.1,
 meaning="Daksha lost all six thousand of his sons, every single one.",
 why="Daksha stands grieving in front; behind him faint rows of his green and violet sons stand in a lavender haze and fade away on 'every', leaving him alone.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"medium","normal",0,"pulling back leaves him alone as the sons fade"),
 focus={"subject":"daksha","depth":"deep"},vertical={"focus":"daksha"},
 layers=[far_sky(haze='#efe6f8',mcol='#a8a0d8'),mid_court(floor='#e8dcd0'),near_court()],
 background=vista(sky=SKY_MEM,ridge=RIDGE_DAWN),mood={"emotion":"loss","grade":"cool"},
 characters=crowd("shavalashva",[(436,0.26,row(640,9,46,4),0.5)],look=640,cues={"fo":"every"},eng={"fd":1.3})+
   crowd("haryashva",[(478,0.32,row(640,7,58),0.6)],look=640,emos=['calm','doubt'],cues={"fo":"every"},eng={"fd":1.3})+
   [{"who":"daksha","x":640,"y":690,"s":1.02,"_face":0.40,"flip":1,"pose":"stand","emo":"sad","look":640,
   "actions":[{"word":"lost","emo":"grief","mood":{"ly":0.4},"d":0.6},{"word":"one","emo":"grief","tilt":-0.05,"d":0.6}]}],
 effects=[{"k":"mist_wisps","word":"every","x":640,"y":420,"w":460,"alpha":0.6,"par":1.0,"meaning":"mist taking the rows of sons away"}],
 transition_in="cut"))
# 3 ---------------------------------------------------------------- the man who took them never raised a hand
S.append(shot("s03",5.9,
 meaning="The one who took Daksha's sons never used force: he never raised a hand.",
 why="Narada with his veena stands calmly on the clouds, his hands folded together on 'never', with a faint knowing smile: no weapon, no blow.",
 camera=cam("crane_down",(1.0,0,-20),(1.04,0,0),"medium","normal",0,"descending from the sky to the sage who came down from it"),
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[{"d":"far","contents":"soft cloud banks and two hazy peaks far behind","fog":0.55,"haze":"#eaf0fa","items":[{"o":"mountain","x":470,"y":500,"s":1.0,"col":"#9aaad8"},{"o":"mountain","x":820,"y":510,"s":0.85,"col":"#9aaad8"},{"o":"cloud","x":520,"y":230,"s":1.3,"col":"#ffffff"},{"o":"cloud","x":780,"y":270,"s":1.1,"col":"#ffffff"}]},
   {"d":"mid","contents":"a bank of white clouds the sage stands on","fog":0.15,"items":[{"o":"cloud","x":500,"y":640,"s":1.6,"col":"#ffffff"},{"o":"cloud","x":800,"y":650,"s":1.5,"col":"#f4f6ff"}]},near_clouds()],
 background=cloud_bg(),mood={"emotion":"irony","grade":"warm"},
 characters=[{"who":"narada","x":640,"y":665,"s":1.05,"_face":0.44,"flip":-1,"pose":"stand","emo":"calm","look":560,"mood":{"smile":0.3},
   "actions":[{"word":"took","mood":{"smile":0.6,"lx":-0.6,"blink":0.2},"d":0.6},{"word":"never","pose":"namaste","emo":"calm","mood":{"smile":0.8,"lx":-0.7,"ly":0.15,"blink":0.25},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"man","x":640,"y":300,"w":420,"alpha":0.35,"blend":"lighter","par":0.9,"behind":True,"meaning":"the quiet holiness of the sage, a pale ring of light"}],
 transition_in="iris"))
# 4 ---------------------------------------------------------------- Daksha had 5,000 sons
S.append(shot("s04",8.68,
 meaning="Daksha had five thousand sons.",
 why="Daksha opens his arms proudly at the left; behind him row after row of green-clad princes fill the palace courtyard, the far rows small and pale in the haze.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"wide","wide",0,"a sideways drift along the rows of sons"),
 focus={"subject":"daksha","depth":"deep"},vertical={"x":610},
 layers=[far_sky(),mid_court(cx=640,wy=400,ws=0.5,px=(420,880)),near_court((440,820))],
 background=vista(),mood={"emotion":"pride","grade":"warm"},
 characters=crowd("haryashva",[(415,0.2,row(690,9,36),0.5),(452,0.25,row(700,8,44,3),0.7),(500,0.31,row(705,6,56),0.88),(556,0.38,row(715,5,68),1)],look=500,emos=['calm','joy','calm','joy'])+
   [{"who":"daksha","x":500,"y":690,"s":0.98,"_face":0.42,"flip":1,"pose":"stand","emo":"pride","look":700,
   "actions":[{"word":"5,000","pose":"open","emo":"joy","mood":{"smile":0.8},"e":"spring","d":0.6}]}],
 effects=[{"k":"glow","word":"sons","x":700,"y":420,"r":260,"rgb":"255,226,160","ga":0.35,"par":1.0,"behind":True,"meaning":"the warm pride of a full courtyard of sons"}],
 transition_in="cut"))
# 5 ---------------------------------------------------------------- the Haryashvas
S.append(shot("s05",11.28,
 meaning="These five thousand sons were called the Haryashvas.",
 why="Three young princes in green dhotis and gold crowns stand at the front of their brothers, smiling; their name 'Haryashvas' appears above them.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"medium","normal",0,"push in to meet the brothers by name"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":640},
 layers=[far_sky(),mid_court(cx=640,wy=400,ws=0.5,px=(430,850)),near_court()],
 background=vista(),mood={"emotion":"youth","grade":"warm"},
 characters=crowd("haryashva",[(430,0.24,row(640,8,44,3),0.6),(470,0.29,row(640,6,58),0.8)],look=640,emos=['joy','calm'])+
   [{"who":"haryashva","x":520,"y":535,"s":0.66,"flip":1,"pose":"stand","emo":"joy","look":640,"_fixed":True,"actions":[{"word":"Haryashvas","mood":{"smile":0.8},"d":0.5}]},
    {"who":"haryashva","x":760,"y":535,"s":0.66,"flip":-1,"pose":"stand","emo":"joy","look":640,"_fixed":True,"actions":[{"word":"Haryashvas","mood":{"smile":0.8},"d":0.5}]},
    {"who":"haryashva","x":640,"y":550,"s":0.7,"flip":1,"pose":"stand","emo":"joy","look":700,"_fixed":True,"actions":[{"word":"Haryashvas","pose":"namaste","mood":{"smile":0.9},"d":0.5}]}],
 effects=[name("Haryashvas","Haryashvas",640,128,30)],
 transition_in="cut"))
# 6 ---------------------------------------------------------------- rule the earth and have children
S.append(shot("s06",12.54,
 meaning="Daksha ordered his sons to rule the earth and have children.",
 why="Stacked: above, Daksha points out over the land as he commands; below, a Haryashva prince listens with folded hands and a willing smile.",
 camera=cam("tilt_down",(1.0,0,-14),(1.0,0,0),"two_shot","normal",0,"from the commanding father down to the son who obeys"),
 focus={"subject":"daksha","depth":"deep"},vertical={"mode":"stack","stack":["daksha","haryashva"]},
 layers=[far_sky(xs=(380,860)),mid_court(cx=640,wy=430,ws=0.55,px=(300,980)),near_court((300,980))],
 background=vista(),mood={"emotion":"command","grade":"warm"},
 characters=[{"who":"daksha","x":470,"y":665,"s":0.95,"flip":1,"pose":"stand","emo":"pride","talk":0.7,"look":"haryashva",
   "actions":[{"word":"rule","pose":"point","emo":"pride","e":"spring","d":0.6},{"word":"children","pose":"open","emo":"joy","d":0.6}]},
  {"who":"haryashva","x":800,"y":665,"s":0.92,"flip":-1,"pose":"stand","emo":"calm","look":"daksha",
   "actions":[{"word":"earth","pose":"namaste","emo":"joy","mood":{"smile":0.7},"d":0.6}]}],
 effects=[{"k":"glow","word":"earth","x":470,"y":330,"r":200,"rgb":"255,214,140","ga":0.4,"par":1.0,"behind":True,"meaning":"the authority of the king's command"}],
 transition_in="cut"))
# 7 ---------------------------------------------------------------- they agreed
S.append(shot("s07",15.2,
 meaning="All the sons agreed to their father's command.",
 why="Rows of Haryashvas fold their hands together in agreement on 'agreed', the whole courtyard bowing at once in warm light.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"wide","wide",0,"pulling back shows the whole crowd agreeing as one"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":640},
 layers=[far_sky(),mid_court(cx=640,wy=390,ws=0.48,px=(430,850)),near_court()],
 background=vista(),mood={"emotion":"obedience","grade":"warm"},
 characters=crowd("haryashva",[(402,0.19,row(640,9,38),0.5),(442,0.24,row(640,8,46,3),0.7),(492,0.31,row(640,6,58),0.88),(552,0.39,row(640,5,72),1)],look=None,emos=['joy','calm'],
   acts=[{"word":"agreed","pose":"namaste","emo":"joy","d":0.5}]),
 effects=[{"k":"glow","word":"agreed","x":640,"y":420,"r":300,"rgb":"255,220,150","ga":0.4,"par":1.0,"behind":True,"meaning":"warm light of the sons' promise"}],
 transition_in="cut"))
# 8 ---------------------------------------------------------------- where the River Sindhu meets the sea
S.append(shot("s08",16.32,
 meaning="Before setting out, the brothers gathered where the River Sindhu flows into the sea.",
 why="Wide on a bright river mouth: the blue Sindhu runs out into the sea under a clear sky, and rows of small green-clad princes gather on the golden sand bank; the name plate reads 'River Sindhu'.",
 camera=cam("crane_down",(1.0,0,-24),(1.0,0,0),"establishing","wide",0,"descending from the open sky to the gathering at the river mouth"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":600},
 layers=[far_sea(),mid_shore(),near_reeds((440,800))],
 background=vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),mood={"emotion":"journey","grade":"warm"},
 characters=crowd("haryashva",[(448,0.17,row(560,7,32),0.6),(478,0.21,row(560,7,38,2),0.8),(516,0.26,row(565,6,46),0.95),(562,0.32,row(560,5,56),1)],look=760,emos=['calm','joy'],
   acts=[{"word":"gathered","emo":"joy","d":0.5}]),
 effects=[name("Sindhu","River Sindhu",600,128,28)],
 transition_in="fade"))
# 9 ---------------------------------------------------------------- to make offerings
S.append(shot("s09",18.98,
 meaning="They made offerings at the sacred meeting of river and sea.",
 why="Closer on the front row of princes at the water's edge, hands folded toward the sea; a golden glow of the offering rises over the water on 'offerings'.",
 camera=cam("dolly_left",(1.04,12,0),(1.04,-12,0),"medium","normal",0,"a slow drift along the row of praying princes"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":620},
 layers=[far_sea(y=380),{"d":"mid","contents":"the sand bank and the river mouth behind the praying princes","fog":0.15,"par":1.0,"items":[{"o":"hill","x":640,"y":470,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"road","x":860,"y":740,"s":1.0,"w":180,"ex":760,"ey":384,"ew":40,"bend":-40,"col":"#4aaae6","plain":True},{"o":"tree","x":420,"y":500,"s":0.6,"kind":"palm","col":"#2e7a44"}]},near_reeds((440,820))],
 background=vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),mood={"emotion":"devotion","grade":"warm"},
 characters=crowd("haryashva",[(500,0.3,row(620,6,56),0.85)],look=800,emos=['devotion','calm'],acts=[{"word":"offerings","pose":"namaste","d":0.6}])+
   crowd("haryashva",[(575,0.48,row(625,3,112),1)],look=800,emos=['devotion'],flipto=1,acts=[{"word":"sea","pose":"namaste","emo":"devotion","d":0.6}]),
 effects=[{"k":"glow","word":"offerings","x":760,"y":360,"r":220,"rgb":"255,210,120","ga":0.5,"par":1.0,"behind":True,"meaning":"the golden light of the offering over the water"},
  {"k":"light_beam","word":"offerings","x":760,"y":0,"w":120,"alpha":0.35,"par":0.6,"behind":True,"meaning":"a beam of blessing falling on the sacred river mouth"}],
 transition_in="cut"))
# 10 --------------------------------------------------------------- Narada, the divine sage
S.append(shot("s10",21.2,
 meaning="Narada, the divine sage, appears.",
 why="Narada with his veena comes down through the bright clouds in soft rays of light; his name appears as it is spoken.",
 camera=cam("crane_down",(1.0,0,-20),(1.0,0,0),"medium","normal",0,"he arrives from the sky"),
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[{"d":"far","contents":"cloud banks and pale peaks in the sky","fog":0.55,"haze":"#eef2fa","items":[{"o":"mountain","x":470,"y":520,"s":1.0,"col":"#9aaad8"},{"o":"cloud","x":520,"y":230,"s":1.3,"col":"#ffffff"},{"o":"cloud","x":790,"y":280,"s":1.1,"col":"#ffffff"}]},
   {"d":"mid","contents":"white clouds around the arriving sage","fog":0.15,"items":[{"o":"cloud","x":480,"y":600,"s":1.5,"col":"#ffffff"},{"o":"cloud","x":820,"y":610,"s":1.4,"col":"#f4f6ff"}]},near_clouds()],
 background=cloud_bg(sx=640,sy=150),mood={"emotion":"arrival","grade":"warm"},
 characters=[{"who":"narada","x":640,"y":665,"s":1.02,"_face":0.45,"flip":1,"pose":"stand","emo":"joy","look":760,"mood":{"smile":0.5},
   "actions":[{"word":"sage","pose":"open","emo":"joy","mood":{"smile":0.7},"d":0.6}]}],
 effects=[{"k":"divine_rays","x":640,"y":60,"w":700,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of the divine sage"},name("Narada","Narada",640,128,30)],
 transition_in="fade"))
# 11 --------------------------------------------------------------- on his way to them
S.append(shot("s11",22.8,
 meaning="Narada was travelling toward the brothers.",
 why="Narada walks along the bright shore with his veena toward the river mouth, the sea shining behind him.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"wide","wide",0,"the dolly travels with him toward the brothers"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[560,660]},
 layers=[far_sea(),{"d":"mid","contents":"the sand bank and palms along the shore","fog":0.15,"par":1.0,"items":[{"o":"hill","x":640,"y":470,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":440,"y":520,"s":0.7,"kind":"palm","col":"#2e7a44"},{"o":"tree","x":860,"y":520,"s":0.6,"kind":"palm","col":"#2e7a44"}]},near_reeds((450,840))],
 background=vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),mood={"emotion":"journey","grade":"warm"},
 characters=[{"who":"narada","x":540,"y":665,"s":0.95,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.4},"look":800,"walk":{"word":"was","to_x":680,"d":1.6,"speed":1},
   "actions":[{"word":"way","mood":{"smile":0.6,"lx":0.6},"d":0.6}]}],
 effects=[],transition_in="wipe"))
# 12 --------------------------------------------------------------- how can you rule a land you know nothing about
S.append(shot("s12",24.1,
 meaning="Narada asked the brothers how they could rule a land they knew nothing about.",
 why="The window pans from Narada, one hand open in a question, to the rows of green princes on the sand, who turn to listen.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan carries the question from the sage to the brothers"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[480,760]},
 layers=[far_sea(xs=(470,840)),{"d":"mid","contents":"the sand bank with a palm on each side","fog":0.15,"par":1.0,"items":[{"o":"hill","x":640,"y":440,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":330,"y":500,"s":0.7,"kind":"palm","col":"#2e7a44"},{"o":"tree","x":940,"y":490,"s":0.6,"kind":"palm","col":"#2e7a44"}]},near_reeds((380,900))],
 background=vista(sky=SKY_SEA,sx=700,sy=230,horizon=40),mood={"emotion":"question","grade":"warm"},
 characters=crowd("haryashva",[(450,0.21,row(790,6,40),0.65),(495,0.27,row(790,5,50),0.85),(560,0.35,row(780,4,64),1)],look=480,emos=['calm','doubt'],
   acts=[{"word":"land","mood":{"ly":0.2},"emo":"doubt","d":0.6}])+
   [{"who":"narada","x":470,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.7,"look":760,
   "actions":[{"word":"asked","pose":"open","emo":"doubt","d":0.6},{"word":"nothing","mood":{"smile":0.4,"lx":0.6},"tilt":0.05,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 13 --------------------------------------------------------------- too few people or too many
S.append(shot("s13",27.42,
 meaning="Narada asked how they would know if the earth had too few people or too many.",
 why="Closer on Narada asking: he lifts one hand on 'few' and spreads both hands wide on 'many', eyebrows raised in a teasing question.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the clever question"),
 focus={"subject":"narada","depth":"shallow"},vertical={"focus":"narada","z":1.12,"y":0.42},
 layers=[far_sea(xs=(500,800)),{"d":"mid","contents":"the sand bank and a palm behind the sage","fog":0.2,"par":1.0,"items":[{"o":"hill","x":640,"y":450,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":800,"y":500,"s":0.7,"kind":"palm","col":"#2e7a44"}]},near_reeds((470,820))],
 background=vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),mood={"emotion":"teasing","grade":"warm"},
 characters=[{"who":"narada","x":620,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"doubt","talk":0.7,"look":800,
   "actions":[{"word":"few","pose":"raise","emo":"doubt","mood":{"surp":0.4},"d":0.5},{"word":"many","pose":"open","mood":{"smile":0.5,"surp":0.3},"tilt":0.05,"d":0.5}]}],
 effects=[],transition_in="cut"))
# 14 --------------------------------------------------------------- no answer
S.append(shot("s14",30.92,
 meaning="The brothers had no answer to give.",
 why="Close on three Haryashva princes: their smiles are gone, they glance at each other with knitted brows and closed mouths, the rows behind them just as unsure.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness: nobody has anything to say"),
 focus={"subject":"haryashva","depth":"shallow"},vertical={"x":640},
 layers=[far_sea(xs=(480,800)),{"d":"mid","contents":"the sand bank behind the brothers","fog":0.2,"par":1.0,"items":[{"o":"hill","x":640,"y":440,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":880,"y":490,"s":0.6,"kind":"palm","col":"#2e7a44"}]},near_reeds((450,840))],
 background=vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),mood={"emotion":"doubt","grade":"cool"},
 characters=crowd("haryashva",[(450,0.27,row(640,6,52),0.7)],look=640,emos=['doubt'])+
   [{"who":"haryashva","x":515,"y":575,"s":0.74,"flip":1,"pose":"stand","emo":"doubt","look":640,"_fixed":True,"actions":[{"word":"no","mood":{"ly":0.3,"lx":0.6},"d":0.5}]},
    {"who":"haryashva","x":765,"y":575,"s":0.74,"flip":-1,"pose":"stand","emo":"doubt","look":640,"_fixed":True,"actions":[{"word":"answer","mood":{"ly":0.2,"lx":-0.6},"tilt":-0.05,"d":0.5}]},
    {"who":"haryashva","x":640,"y":590,"s":0.78,"flip":1,"pose":"stand","emo":"doubt","look":520,"_fixed":True,"actions":[{"word":"brothers","emo":"shame","mood":{"ly":0.4},"d":0.5}]}],
 effects=[],transition_in="cut"))
# 15 --------------------------------------------------------------- Narada smirked
S.append(shot("s15",33.04,
 meaning="Narada smirked at their silence.",
 why="Close on Narada's face: one corner of his mouth lifts in a sly smirk, eyes slid sideways toward the brothers.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,0),"close","tele",0,"push in on the smirk"),
 focus={"subject":"narada","depth":"shallow"},vertical={"focus":"narada"},
 layers=[far_sea(xs=(500,800)),{"d":"mid","contents":"a palm on the sand bank behind his head","fog":0.25,"par":1.0,"items":[{"o":"hill","x":640,"y":450,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":790,"y":520,"s":0.7,"kind":"palm","col":"#2e7a44"}]},near_reeds((470,820))],
 background=vista(sky=SKY_SEA,sx=700,sy=230,horizon=40),mood={"emotion":"sly","grade":"warm"},
 characters=[{"who":"narada","x":640,"y":350,"s":1.15,"flip":1,"head":True,"emo":"calm","mood":{"smile":0.5,"lx":0.6},"look":900,
   "actions":[{"word":"smirked","mood":{"smile":0.8,"lx":0.7,"ly":0.15,"blink":0.25},"tilt":0.05,"d":0.5}]}],
 effects=[],transition_in="cut"))
# 16 --------------------------------------------------------------- learn every detail about the earth first
S.append(shot("s16",34.46,
 meaning="Narada told them to first learn every detail about the earth.",
 why="The window pans from Narada pointing outward to the wide earth beyond: hills, forests and a river winding away to far blue mountains.",
 camera=cam("pan_right",(1.0,0,0),(1.0,0,0),"wide","wide",0,"the pan follows his pointing hand out over the whole earth"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[500,780]},
 layers=[{"d":"far","contents":"far blue mountain ranges and clouds across the earth","fog":0.5,"haze":"#eef4fa","items":[{"o":"mountain","x":760,"y":420,"s":1.0,"w":260,"h":200,"col":"#8aa4d0"},{"o":"mountain","x":960,"y":430,"s":0.9,"w":220,"h":160,"col":"#8aa4d0"},{"o":"cloud","x":820,"y":200,"s":1.1,"col":"#ffffff"}]},
   {"d":"mid","contents":"green hills and round trees of the wide earth","fog":0.18,"items":[{"o":"hill","x":800,"y":520,"s":1.0,"w":500,"h":60,"col":"#7aa860"},{"o":"tree","x":720,"y":540,"s":0.55,"kind":"round","col":"#3a7a44"},{"o":"tree","x":880,"y":530,"s":0.5,"kind":"pine","col":"#2e6a3e"},{"o":"tree","x":400,"y":560,"s":0.7,"kind":"palm","col":"#2e7a44"}]},near_reeds((420,880))],
 background=vista(sky=['#2f6ad0','#7ab8f0','#ffe6c4','#fff8ea'],sx=800,sy=230,river='#5ab8e8'),mood={"emotion":"advice","grade":"warm"},
 characters=[{"who":"narada","x":500,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.7,"look":800,"mood":{"smile":0.4},
   "actions":[{"word":"learn","pose":"point","emo":"calm","e":"spring","d":0.6},{"word":"earth","mood":{"smile":0.6,"lx":0.7},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 17 --------------------------------------------------------------- a higher path
S.append(shot("s17",37.64,
 meaning="Narada hinted that they might even find a higher, spiritual path.",
 why="A road of light climbs from the sand up to a shining mountain peak; Narada raises his hand toward it as golden rays fall on the summit on 'higher'.",
 camera=cam("tilt_up",(1.04,0,14),(1.04,0,-6),"medium","normal",0,"tilting up the path toward the summit"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":600},
 layers=[{"d":"far","contents":"a tall shining mountain peak far away under rays","fog":0.45,"haze":"#f2eefa","items":[{"o":"mountain","x":700,"y":400,"s":1.0,"w":220,"h":250,"col":"#a0a8d8"},{"o":"cloud","x":520,"y":220,"s":1.0,"col":"#ffffff"}]},
   mid_road(x=650,ex=700,ey=400,w=170,glow='255,226,150',trees=(470,880),bend=-30),near_reeds((440,830))],
 background=vista(sky=['#2a50c0','#7aa8ee','#ffe0b8','#fff6e4'],sx=700,sy=150),mood={"emotion":"promise","grade":"warm"},
 characters=[{"who":"narada","x":520,"y":665,"s":0.96,"_face":0.44,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":700,"mood":{"smile":0.5},
   "actions":[{"word":"higher","pose":"raise","emo":"joy","mood":{"ly":-0.6,"smile":0.6},"d":0.6}]}],
 effects=[{"k":"divine_rays","word":"higher","x":700,"y":40,"w":500,"alpha":0.4,"blend":"lighter","par":0.3,"behind":True,"meaning":"the light of a higher path on the summit"},
  {"k":"halo_ring","word":"path","x":700,"y":170,"w":240,"alpha":0.4,"blend":"lighter","par":0.4,"behind":True,"meaning":"the goal of the higher path glowing on the peak"}],
 transition_in="cut"))
# 18 --------------------------------------------------------------- doubt crept over 5,000 faces
S.append(shot("s18",39.96,
 meaning="Doubt spread across the faces of all five thousand brothers.",
 why="Rows of green princes on the shore turn to one another with doubtful faces while the bright sky fades to gray-blue and a gray shadow of mist creeps along the rows.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"wide","normal",0,"a slow push in as the doubt creeps in"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":640},
 layers=[far_sea(),{"d":"mid","contents":"the sand bank under a cooling sky","fog":0.18,"par":1.0,"items":[{"o":"hill","x":640,"y":405,"s":1.0,"w":1100,"h":12,"col":"#e6d8b8"},{"o":"tree","x":420,"y":460,"s":0.55,"kind":"palm","col":"#2e6a44"},{"o":"tree","x":880,"y":455,"s":0.5,"kind":"palm","col":"#2e6a44"}]},near_reeds((440,840),'#24484a')],
 background={**vista(sky=SKY_SEA,sx=760,sy=230,horizon=40),"change":{"word":"crept","bg2":vista(sky=SKY_COOL,sx=760,sy=230,horizon=40,ridge=RIDGE_DAWN),"d":1.4}},
 mood={"emotion":"doubt","grade":"cool"},
 characters=crowd("haryashva",[(412,0.19,row(640,9,38),0.55),(450,0.24,row(640,8,46,3),0.72),(500,0.31,row(640,6,58),0.9),(560,0.4,row(640,5,74),1)],look=None,emos=['doubt','calm','doubt','shame'],
   acts=[{"word":"Doubt","emo":"doubt","mood":{"ly":0.3},"d":0.6},{"word":"faces","tilt":0.05,"d":0.5}]),
 effects=[{"k":"mist_wisps","word":"crept","x":640,"y":470,"w":480,"alpha":0.55,"par":1.0,"meaning":"doubt creeping over the rows like a gray mist"}],
 transition_in="cut"))
# 19 --------------------------------------------------------------- the brothers left to explore the earth
S.append(shot("s19",42.7,
 meaning="The brothers set out to explore the earth.",
 why="At sunrise a long line of green princes walks away along a dusty road toward the sun, each one smaller and paler as the road runs to the horizon.",
 camera=cam("dolly_right",(1.0,-12,0),(1.0,6,0),"wide","wide",0,"the dolly moves with the brothers down the road"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":680},
 layers=[far_hills(),mid_road(x=600,ex=780,ey=380,w=200),near_reeds((470,860),'#3a5a3a')],
 background=vista(sky=SKY_DAWN,sx=780,sy=360,ridge=RIDGE_DAWN,sr=460),mood={"emotion":"departure","grade":"warm"},
 characters=[{"who":"haryashva","x":x,"y":y,"s":s,"flip":1,"pose":"stand","emo":"calm","look":900,"_fixed":True,"engine":{"walk":1,"vx":v,**({"a":a} if a<1 else {})},
   "actions":[{"word":"explore","mood":{"lx":0.6},"d":0.6}]} for (x,y,s,a,v) in [(780,386,0.08,0.45,3),(772,394,0.1,0.55,3),(760,404,0.12,0.62,4),(744,418,0.15,0.72,5),(722,437,0.19,0.82,6),(694,464,0.24,0.92,7),(658,500,0.31,1,8),(612,548,0.4,1,9)]],
 effects=[{"k":"glow","x":780,"y":360,"r":300,"rgb":"255,200,130","ga":0.45,"par":0.4,"behind":True,"meaning":"the sunrise the brothers walk into"}],
 transition_in="fade"))
# 20 --------------------------------------------------------------- no one saw them again
S.append(shot("s20",44.94,
 meaning="No one ever saw the brothers again.",
 why="The same sunrise road, now nearly empty: the last three tiny figures at the horizon fade into the light on 'saw', leaving only the road.",
 camera=cam("crane_up",(1.04,0,8),(1.0,0,-10),"wide","wide",0,"rising over the empty road"),
 focus={"subject":"road","depth":"deep"},vertical={"x":720},
 layers=[far_hills(xs=(520,860)),mid_road(x=640,ex=780,ey=380,w=210),near_reeds((500,900),'#3a5a3a')],
 background=vista(sky=SKY_DAWN,sx=780,sy=350,ridge=RIDGE_DAWN,sr=460),mood={"emotion":"emptiness","grade":"warm"},
 characters=[{"who":"haryashva","x":x,"y":y,"s":s,"flip":1,"pose":"stand","emo":"calm","look":900,"_fixed":True,"engine":{"walk":1,"vx":2,"a":0.6,"fd":1.0},"engine_cues":{"fo":"saw"}} for (x,y,s) in [(776,388,0.08),(768,395,0.09),(758,404,0.11)]],
 effects=[{"k":"mist_wisps","word":"again","x":760,"y":400,"w":300,"alpha":0.5,"par":0.6,"meaning":"morning mist where the brothers disappeared"},
  {"k":"glow","x":780,"y":360,"r":280,"rgb":"255,210,140","ga":0.45,"par":0.4,"behind":True,"meaning":"the sunrise that swallowed them"}],
 transition_in="cut"))
# 21 --------------------------------------------------------------- they never came back
S.append(shot("s21",46.34,
 meaning="The brothers never returned home.",
 why="Daksha waits alone in his empty courtyard looking out to the road; his proud smile is gone and his eyes drop in sorrow on 'never'.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the waiting father"),
 focus={"subject":"daksha","depth":"deep"},vertical={"focus":"daksha"},
 layers=[far_sky(haze='#f2ecf4'),mid_court(floor='#e8dccc'),near_court()],
 background=vista(sky=['#4a5ab4','#9aa4dc','#f0c8b8','#fff0e4']),mood={"emotion":"waiting","grade":"cool"},
 characters=[{"who":"daksha","x":640,"y":690,"s":1.02,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":800,
   "actions":[{"word":"never","emo":"sad","mood":{"ly":0.4},"d":0.6},{"word":"back","emo":"grief","tilt":-0.04,"d":0.6}]}],
 effects=[],transition_in="fade"))
# 22 --------------------------------------------------------------- Daksha and Ashikli had another thousand sons
S.append(shot("s22",47.88,
 meaning="Daksha and his wife Ashikli had a thousand more sons.",
 why="Daksha and his wife Ashikli in her blue sari stand together in the courtyard; her name appears, and on 'thousand' rows of violet-clad princes appear behind them.",
 camera=cam("pull_out",(1.06,0,-6),(1.0,0,0),"two_shot","normal",0,"pulling back to reveal the new rows of sons"),
 focus={"subject":"asikli","depth":"deep"},vertical={"x":[580,690]},
 layers=[far_sky(),mid_court(cx=640,wy=400,ws=0.5,px=(420,870)),near_court((440,840))],
 background=vista(),mood={"emotion":"new hope","grade":"warm"},
 characters=crowd("shavalashva",[(410,0.2,row(640,10,36),0.55),(448,0.25,row(640,8,46,3),0.75),(492,0.3,row(640,7,56),0.9)],look=640,emos=['joy','calm'],
   cues={"ac":"thousand"},eng={"ad":0.8})+
  [{"who":"daksha","x":560,"y":690,"s":0.98,"_face":0.41,"flip":1,"pose":"stand","emo":"calm","look":"asikli","mood":{"smile":0.4},
   "actions":[{"word":"thousand","pose":"open","emo":"joy","d":0.6}]},
  {"who":"asikli","x":710,"y":690,"s":0.96,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"daksha","mood":{"smile":0.5},
   "actions":[{"word":"Ashikli","mood":{"smile":0.7,"ly":0.2},"d":0.6},{"word":"sons","pose":"namaste","emo":"joy","d":0.6}]}],
 effects=[name("Ashikli","Ashikli",700,128,28)],
 transition_in="cut"))
# 23 --------------------------------------------------------------- the Shavalashvas
S.append(shot("s23",51.16,
 meaning="The new sons were called the Shavalashvas.",
 why="Three young princes in violet dotted dhotis and white uttariyas stand at the front of their brothers, smiling; the name 'Shavalashvas' appears above them.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"medium","normal",0,"push in to meet the second brothers by name"),
 focus={"subject":"shavalashva","depth":"deep"},vertical={"x":640},
 layers=[far_sky(),mid_court(cx=640,wy=400,ws=0.5,px=(430,850)),near_court()],
 background=vista(),mood={"emotion":"youth","grade":"warm"},
 characters=crowd("shavalashva",[(430,0.24,row(640,8,44,3),0.6),(470,0.29,row(640,6,58),0.8)],look=640,emos=['joy','calm'])+
   [{"who":"shavalashva","x":520,"y":535,"s":0.66,"flip":1,"pose":"stand","emo":"joy","look":640,"_fixed":True,"actions":[{"word":"Shavalashvas","mood":{"smile":0.8},"d":0.5}]},
    {"who":"shavalashva","x":760,"y":535,"s":0.66,"flip":-1,"pose":"stand","emo":"joy","look":640,"_fixed":True,"actions":[{"word":"Shavalashvas","mood":{"smile":0.8},"d":0.5}]},
    {"who":"shavalashva","x":640,"y":550,"s":0.7,"flip":-1,"pose":"stand","emo":"joy","look":560,"_fixed":True,"actions":[{"word":"Shavalashvas","pose":"namaste","mood":{"smile":0.9},"d":0.5}]}],
 effects=[name("Shavalashvas","Shavalashvas",640,128,28)],
 transition_in="cut"))
# 24 --------------------------------------------------------------- Narada spoke to them in exactly the same way
S.append(shot("s24",52.52,
 meaning="Narada gave the Shavalashvas exactly the same advice.",
 why="The very same shore and the very same pan: Narada, hand open, talks to rows of violet princes on the sand, who listen just as their brothers did.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the same pan as before: the same words, the same result"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[480,760]},
 layers=[far_sea(xs=(470,840)),{"d":"mid","contents":"the same sand bank with a palm on each side","fog":0.15,"par":1.0,"items":[{"o":"hill","x":640,"y":440,"s":1.0,"w":1100,"h":12,"col":"#f2dca8"},{"o":"tree","x":330,"y":500,"s":0.7,"kind":"palm","col":"#2e7a44"},{"o":"tree","x":940,"y":490,"s":0.6,"kind":"palm","col":"#2e7a44"}]},near_reeds((380,900))],
 background=vista(sky=SKY_SEA,sx=700,sy=230,horizon=40),mood={"emotion":"repetition","grade":"warm"},
 characters=crowd("shavalashva",[(450,0.21,row(790,6,40),0.65),(495,0.27,row(790,5,50),0.85),(560,0.35,row(780,4,64),1)],look=480,emos=['calm','doubt'],
   acts=[{"word":"same","emo":"doubt","mood":{"ly":0.2},"d":0.6}])+
   [{"who":"narada","x":470,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.7,"look":760,
   "actions":[{"word":"spoke","pose":"open","emo":"calm","mood":{"smile":0.5},"d":0.6},{"word":"exactly","pose":"point","mood":{"smile":0.7,"lx":0.6},"d":0.6}]}],
 effects=[],transition_in="fade"))
# 25 --------------------------------------------------------------- they vanished too
S.append(shot("s25",55.24,
 meaning="The Shavalashvas disappeared as well.",
 why="On the sunrise road a line of violet princes walks away and dissolves into the morning mist on 'vanished'.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-6,0),"wide","wide",0,"a drift against their walk as they disappear"),
 focus={"subject":"shavalashva","depth":"deep"},vertical={"x":690},
 layers=[far_hills(),mid_road(x=620,ex=790,ey=380,w=200),near_reeds((480,880),'#3a5a3a')],
 background=vista(sky=SKY_DAWN,sx=790,sy=350,ridge=RIDGE_DAWN,sr=460),mood={"emotion":"vanishing","grade":"warm"},
 characters=[{"who":"shavalashva","x":x,"y":y,"s":s,"flip":1,"pose":"stand","emo":"calm","look":900,"_fixed":True,"engine":{"walk":1,"vx":v,"fd":1.0,**({"a":a} if a<1 else {})},"engine_cues":{"fo":"vanished"}}
   for (x,y,s,a,v) in [(782,392,0.1,0.55,3),(768,404,0.13,0.65,4),(750,420,0.17,0.78,5),(726,442,0.22,0.88,6),(694,472,0.28,1,7),(654,512,0.35,1,8)]],
 effects=[{"k":"mist_wisps","word":"vanished","x":720,"y":430,"w":420,"alpha":0.75,"par":1.0,"meaning":"the mist that swallows the second brothers"},
  {"k":"glow","x":790,"y":350,"r":280,"rgb":"255,200,150","ga":0.45,"par":0.4,"behind":True,"meaning":"the sunrise they vanish into"}],
 transition_in="wipe"))
# 26 --------------------------------------------------------------- Daksha roared
S.append(shot("s26",56.34,
 meaning="Daksha roared in fury.",
 why="Daksha's face flushes with rage, red-eyed under heavy brows, as he thrusts his finger out on 'roared'; the sky behind him burns orange-red and the frame tilts.",
 camera=cam("dutch",(1.0,0,0),(1.06,0,-4),"medium","normal",4,"the tilted, shaking frame of a father's fury",r=(0.0,0.04)),
 focus={"subject":"daksha","depth":"deep"},vertical={"focus":"daksha"},
 layers=[far_sky(haze='#ffe4d0',col='#ffe8d8',mcol='#c89a9a'),mid_court(floor='#ecd0b0'),near_court()],
 background=vista(sky=SKY_RAGE,sun='255,170,120'),mood={"emotion":"rage","grade":"warm"},
 characters=[{"who":"daksha","x":620,"y":690,"s":1.04,"_face":0.43,"flip":1,"pose":"stand","emo":"anger","talk":1.0,"look":800,
   "actions":[{"word":"roared","pose":"rpoint","emo":"rage","e":"spring","d":0.4}]}],
 effects=[{"k":"red_energy_pulse","word":"roared","x":620,"y":330,"w":420,"alpha":0.5,"par":1.0,"behind":True,"meaning":"the shock wave of Daksha's roar"},
  {"k":"glow","x":620,"y":330,"r":240,"rgb":"255,120,80","ga":0.4,"par":1.0,"behind":True,"meaning":"the heat of his anger"}],
 transition_in="cut"))
# 27 --------------------------------------------------------------- who would build homes?
S.append(shot("s27",57.78,
 meaning="Daksha asked who would build homes and families if everyone became a hermit.",
 why="Daksha raises his hand in angry protest; behind him a village of empty, unlit houses stands with no one in it.",
 camera=cam("pull_out",(1.08,0,-8),(1.0,0,0),"medium","normal",0,"pulling back reveals the empty homes behind him"),
 focus={"subject":"daksha","depth":"deep"},vertical={"focus":"daksha"},
 layers=[far_sky(haze='#f4e8e0'),{"d":"mid","contents":"a village of empty, dark houses with no one in them","fog":0.3,"haze":"#ece4e4","items":[hut_ for hut_ in [{"o":"hut","x":470,"y":470,"s":0.55,"toran":False},{"o":"hut","x":630,"y":455,"s":0.48,"toran":False},{"o":"hut","x":800,"y":468,"s":0.55,"toran":False},{"o":"hill","x":640,"y":475,"s":1.0,"w":900,"h":10,"col":"#d8c49a"}]]},near_court()],
 background=vista(sky=['#6a3a6a','#c07a7a','#ffc49a','#fff0d4'],sun='255,190,140'),mood={"emotion":"protest","grade":"warm"},
 characters=[{"who":"daksha","x":620,"y":690,"s":1.02,"_face":0.42,"flip":1,"pose":"stand","emo":"anger","talk":0.9,"look":760,
   "actions":[{"word":"homes","pose":"raise","emo":"anger","d":0.5},{"word":"hermit","pose":"open","emo":"rage","tilt":0.04,"d":0.5}]}],
 effects=[],transition_in="cut"))
# 28 --------------------------------------------------------------- I only showed them a path
S.append(shot("s28",60.68,
 meaning="Narada calmly answered that he had only shown them a path.",
 why="Stacked: above, Daksha glares with clenched brows; below, Narada answers calmly with an open hand and a small serene smile.",
 camera=cam("crane_down",(1.0,0,-14),(1.0,0,0),"two_shot","normal",0,"from the angry king down to the calm sage"),
 focus={"subject":"narada","depth":"deep"},vertical={"mode":"stack","stack":["daksha","narada"]},
 layers=[far_sky(xs=(380,860),haze='#f6ecea'),mid_court(cx=640,wy=430,ws=0.55,px=(300,980)),near_court((300,980))],
 background=vista(sky=['#4a4ab0','#a090d8','#ffc8a8','#fff2e0']),mood={"emotion":"confrontation","grade":"warm"},
 characters=[{"who":"daksha","x":470,"y":665,"s":0.95,"flip":1,"pose":"stand","emo":"anger","look":"narada",
   "actions":[{"word":"path","emo":"rage","d":0.6}]},
  {"who":"narada","x":800,"y":665,"s":0.95,"flip":-1,"pose":"stand","emo":"calm","talk":0.7,"look":"daksha","mood":{"smile":0.4},
   "actions":[{"word":"shown","pose":"open","emo":"calm","mood":{"smile":0.5},"d":0.6}]}],
 effects=[{"k":"glow","x":800,"y":330,"r":200,"rgb":"200,225,255","ga":0.4,"par":1.0,"behind":True,"meaning":"the sage's calm light"}],
 transition_in="cut"))
# 29 --------------------------------------------------------------- their choice to walk it
S.append(shot("s29",63.58,
 meaning="It was the brothers' own choice to walk that path.",
 why="Narada stands calm beside a road of soft light that runs to the horizon, his hand open toward it on 'choice': the path was there, walking it was theirs.",
 camera=cam("tilt_up",(1.04,0,12),(1.04,0,-4),"medium","normal",0,"tilting up along the road to its far end"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":600},
 layers=[far_hills(xs=(520,840)),mid_road(x=700,ex=720,ey=390,w=170,glow='255,236,180',trees=(440,900),bend=-20),near_reeds((440,840))],
 background=vista(sky=['#3a5cc4','#8ab0ec','#ffd8b8','#fff4e6'],sx=720,sy=330,ridge=RIDGE_DAWN),mood={"emotion":"calm","grade":"warm"},
 characters=[{"who":"narada","x":520,"y":665,"s":0.98,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":720,"mood":{"smile":0.4},
   "actions":[{"word":"choice","pose":"open","mood":{"smile":0.6,"lx":0.6},"d":0.6},{"word":"walk","tilt":0.04,"mood":{"blink":0.3},"d":0.5}]}],
 effects=[{"k":"glow","word":"walk","x":720,"y":400,"r":200,"rgb":"255,230,170","ga":0.45,"par":0.8,"behind":True,"meaning":"the open path glowing at the horizon"}],
 transition_in="cut"))
# 30 --------------------------------------------------------------- Daksha cursed him
S.append(shot("s30",65.56,
 meaning="Daksha laid a curse on Narada.",
 why="The window pans from Daksha thrusting his finger in a curse to Narada, who is struck by a red ring of the curse and stops smiling.",
 camera=cam("pan_right",(1.0,0,0),(1.04,0,0),"two_shot","normal",5,"the pan follows the curse from the king to the sage"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[500,780]},
 layers=[far_sky(xs=(440,880),haze='#ffe4d8',col='#ffe8d8',mcol='#c8a0a8'),mid_court(cx=640,wy=440,ws=0.55,px=(330,960)),near_court((380,900))],
 background=vista(sky=SKY_RAGE,sun='255,170,120'),mood={"emotion":"curse","grade":"warm"},
 characters=[{"who":"daksha","x":490,"y":665,"s":0.98,"_face":0.42,"flip":1,"pose":"stand","emo":"rage","talk":1.0,"look":"narada",
   "actions":[{"word":"cursed","pose":"rpoint","emo":"rage","e":"spring","d":0.4}]},
  {"who":"narada","x":800,"y":665,"s":0.96,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"daksha",
   "actions":[{"word":"him","emo":"surprise","mood":{"surp":0.6},"d":0.4}]}],
 effects=[{"k":"red_energy_pulse","word":"cursed","x":800,"y":330,"w":360,"alpha":0.55,"par":1.0,"behind":True,"meaning":"the curse striking Narada"},
  {"k":"halo_ring","word":"him","x":800,"y":330,"w":380,"alpha":0.4,"blend":"lighter","par":1.0,"behind":True,"rgb":"255,110,90","meaning":"the ring of the curse closing around him"}],
 transition_in="flash"))
# 31 --------------------------------------------------------------- scattered his sons across the earth
S.append(shot("s31",67.06,
 meaning="Narada had scattered Daksha's sons all over the earth.",
 why="High over a wide green earth of hills and rivers, tiny green and violet princes stand alone, far apart, scattered across the land in the haze.",
 camera=cam("crane_up",(1.06,0,10),(1.0,0,-8),"high_angle","wide",0,"rising high to see the sons scattered far and wide"),
 focus={"subject":"haryashva","depth":"deep"},vertical={"x":640},
 layers=[{"d":"far","contents":"far blue hills and haze across the earth","fog":0.55,"haze":"#eef4fa","items":[{"o":"mountain","x":500,"y":330,"s":1.0,"w":240,"h":100,"col":"#9ab4d4","snow":False},{"o":"mountain","x":800,"y":335,"s":1.0,"w":220,"h":90,"col":"#9ab4d4","snow":False}]},
   {"d":"mid","contents":"rolling green hills with groves dotted over the land","fog":0.15,"items":[{"o":"hill","x":520,"y":430,"s":1.0,"w":360,"h":40,"col":"#8ab870"},{"o":"hill","x":800,"y":470,"s":1.0,"w":380,"h":50,"col":"#7aa860"},{"o":"tree","x":470,"y":450,"s":0.3,"kind":"round","col":"#3a7a44"},{"o":"tree","x":830,"y":500,"s":0.32,"kind":"round","col":"#3a7a44"},{"o":"tree","x":600,"y":540,"s":0.36,"kind":"pine","col":"#2e6a3e"}]},near_reeds((440,840))],
 background=vista(sky=['#2f6ad0','#7ab8f0','#ffe6c4','#fff8ea'],sx=640,sy=200,river='#5ab8e8'),mood={"emotion":"scattered","grade":"warm"},
 characters=[{"who":w,"x":x,"y":y,"s":s,"flip":f,"pose":"stand","emo":e,"look":x+f*100,"_fixed":True,**({"engine":{"a":a}} if a<1 else {}),
   "actions":[{"word":"scattered","mood":{"ly":0.3},"d":0.6}]}
   for (w,x,y,s,f,e,a) in [("haryashva",470,372,0.11,1,"sad",0.6),("shavalashva",585,358,0.1,-1,"calm",0.55),("haryashva",770,380,0.12,-1,"calm",0.62),("shavalashva",835,410,0.13,1,"sad",0.7),
     ("haryashva",505,440,0.16,1,"calm",0.8),("shavalashva",700,452,0.17,-1,"doubt",0.82),("haryashva",615,500,0.21,1,"sad",0.92),("shavalashva",470,532,0.24,1,"calm",1),("haryashva",790,540,0.25,-1,"doubt",1)]],
 effects=[{"k":"mist_wisps","word":"across","x":640,"y":420,"w":520,"alpha":0.45,"par":0.8,"meaning":"the haze of distance between the scattered sons"}],
 transition_in="cut"))
# 32 --------------------------------------------------------------- wander the three worlds, never find a home
S.append(shot("s32",69.78,
 meaning="Narada was cursed to wander the three worlds forever without ever finding a home.",
 why="Under the first evening stars Narada walks on with his veena past a lamp-lit house that is not his; on 'home' he glances back at its warm door with a sad face and keeps walking.",
 camera=cam("dolly_right",(1.0,-12,0),(1.0,12,0),"wide","wide",0,"the dolly travels with the endless wanderer"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[560,680]},
 layers=[{"d":"far","contents":"violet hills and the three worlds' sky with the first stars","fog":0.5,"haze":"#c8b8dc","items":[{"o":"mountain","x":480,"y":420,"s":1.0,"w":260,"h":150,"col":"#6a6aa8","snow":False},{"o":"mountain","x":860,"y":425,"s":1.0,"w":240,"h":120,"col":"#6a6aa8","snow":False},{"o":"cloud","x":560,"y":230,"s":1.0,"col":"#e8d8f0"}]},
   {"d":"mid","contents":"a lamp-lit village house beside the road the sage passes","fog":0.15,"items":[{"o":"hill","x":640,"y":500,"s":1.0,"w":900,"h":12,"col":"#b8a888"},{"o":"hut","x":770,"y":505,"s":0.72,"lamp":True},{"o":"tree","x":420,"y":510,"s":0.6,"kind":"round","col":"#2e5a44"}]},near_reeds((450,860),'#24304a')],
 background=vista(sky=SKY_DUSK,sx=640,sy=440,ridge=['#7a6aa8','#5a5090','#3c3a70','#2a2a58'],sun='255,190,150'),mood={"emotion":"exile","grade":"cool"},
 characters=[{"who":"narada","x":540,"y":665,"s":0.95,"_face":0.44,"flip":1,"pose":"stand","emo":"sad","look":800,"walk":{"word":"wander","to_x":660,"d":3.4,"speed":1},
   "actions":[{"word":"forever","emo":"sad","mood":{"ly":0.3},"d":0.6},{"word":"home","emo":"grief","mood":{"lx":0.8,"ly":-0.1},"tilt":-0.04,"d":0.6}]}],
 effects=[{"k":"glow","word":"home","x":770,"y":470,"r":160,"rgb":"255,200,120","ga":0.5,"par":1.0,"behind":True,"meaning":"the warm light of a home that will never be his"}],
 transition_in="fade"))
# 33 --------------------------------------------------------------- guide or thief of sons?
S.append(shot("s33",73.64,
 meaning="The question to the viewer: was Narada a guide or a thief of sons?",
 why="Close on Narada with his veena: on 'guide' a gold halo opens behind his head; on 'thief' a violet swirl takes its place and his smile turns sly.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-6),"close","tele",0,"push in on the face the viewer must judge"),
 focus={"subject":"narada","depth":"shallow"},vertical={"focus":"narada","z":1.15,"y":0.42},
 layers=[{"d":"far","contents":"soft clouds and a pale peak behind the sage","fog":0.55,"haze":"#ece6f6","items":[{"o":"mountain","x":500,"y":460,"s":1.0,"col":"#a8a8d8","snow":False},{"o":"cloud","x":560,"y":220,"s":1.2,"col":"#ffffff"},{"o":"cloud","x":780,"y":270,"s":1.0,"col":"#ffffff"}]},
   {"d":"mid","contents":"a bank of clouds at his feet","fog":0.15,"items":[{"o":"cloud","x":480,"y":640,"s":1.5,"col":"#ffffff"},{"o":"cloud","x":820,"y":650,"s":1.4,"col":"#f4f0ff"}]},near_clouds()],
 background=cloud_bg(sky=['#2a3f9e','#6a8ae0','#e0d0f4','#fff4e4']),mood={"emotion":"question","grade":"warm"},
 characters=[{"who":"narada","x":640,"y":665,"s":1.04,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":700,"mood":{"smile":0.4},
   "actions":[{"word":"guide","pose":"namaste","emo":"devotion","d":0.6},{"word":"thief","pose":"stand","emo":"calm","mood":{"smile":0.8,"lx":-0.7,"ly":0.15,"blink":0.25},"tilt":0.05,"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"guide","x":640,"y":290,"w":420,"alpha":0.5,"blend":"lighter","par":1.0,"behind":True,"meaning":"Narada as a holy guide, a gold halo"},
  {"k":"energy_swirl","word":"thief","x":640,"y":290,"w":440,"alpha":0.5,"blend":"lighter","par":1.0,"behind":True,"meaning":"Narada as the thief of sons, a violet swirl of doubt"}],
 transition_in="cut"))
# durations / narration from the next start
for i,s in enumerate(S):
    end=S[i+1]['start']['t'] if i+1<len(S) else END
    s['duration']=round(end-s['start']['t'],2)
    i0=idx(s['start']['t']);i1=idx(S[i+1]['start']['t']) if i+1<len(S) else len(T);s['narration']=span(i0,i1)
import sys;sys.path.insert(0,R+'/studio');import validate_brief as VB
def ease(k):return k*k*(3-2*k)
def face_frac(f,s,u=.55):
    c=s['camera'];A=c['from'];B=c['to'];e=ease(u)
    z=A.get('z',1)+(B.get('z',1)-A.get('z',1))*e;cy=A.get('y',0)+(B.get('y',0)-A.get('y',0))*e
    fc=f['y'] if f.get('head') else f['y']-(195 if VB.seated(f) else 300)*f['s']
    sy=360+(fc-360-cy)*z;V=s.get('vertical') or {};vz=min(max(V.get('z',1),1),2.2);h=720/vz
    w0=min(max(sy-V.get('y',.36)*h,0),720-h) if vz>1 else 0
    return (sy-w0)/h
for s in S:   # crowd shots: tilt the camera down (cam y +L) until every crowd chin clears the subtitle band at both ends of the move
    fx=[f for f in s['characters'] if f.get('_fixed')]
    if not fx or (s.get('vertical') or {}).get('mode')=='stack':continue
    L=0
    while L<70 and any(VB.face_cropped_v(f,{'from':s['camera']['from'],'to':s['camera']['to']},s.get('vertical')) for f in fx if f['s']>=0.15):
        L+=2;s['camera']['from']['y']+=2;s['camera']['to']['y']+=2
    if L:print('  lift',s['id'],L)
for s in S:
    if (s.get('vertical') or {}).get('mode')=='stack':continue
    g=None
    for f in s['characters']:
        if f.get('head') or f.get('_fixed'):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        tgt=f.pop('_face',.42)
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None:g=f['y']
for s in S:
    fx=[f for f in s['characters'] if f.get('_fixed')]
    if fx:print('  crowd',s['id'],len(fx),'faces %.2f-%.2f'%(min(face_frac(f,s) for f in fx),max(face_frac(f,s) for f in fx)))
for s in S:
    cam_={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        if f.get('_fixed'):continue
        y0=f['y']
        while VB.face_cropped_v(f,cam_,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
for s in S:
    for f in s['characters']:
        for k in('_face','_ground','_fixed'):f.pop(k,None)
for i,s_ in enumerate(S):s_['id']=f"s{i+1:02d}"
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel07","format":"vertical","shots":S},open(f'{R}/reels/reel07/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
