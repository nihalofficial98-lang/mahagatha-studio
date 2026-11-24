#!/usr/bin/env python3
"""Generator for reels/reel06/briefs.json "Why Say Swaha?" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel04/briefs_gen.py: every face solved to 38-50% of the 9:16 frame height, narration = the spoken words.
Look: bright clean colours, warm gold fire (not muddy); Brahmaloka = blue-gold cloudscape with gold pillars and a gateway;
earth = bright morning village with a brick havan kund; the offering path = a column of light from the kund up to the gateway
of Brahmaloka with round light motes (orbs) travelling up it. Stack layout only for heaven/earth and for the two dialogues."""
import json,os,sys
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel06/words.json'))
T=[(w['w'],w['start']) for w in W]
END=82.76
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette (bright, clean, warm gold fire) ----------
SKY_LOKA=['#2f56c0','#7eaaf0','#ffd8a8','#fff6e0']      # Brahmaloka, blue-gold
SKY_DAWN=['#3a5ab8','#9ab0ea','#ffc890','#fff0d8']      # Brahmaloka at morning
SKY_HUNGRY=['#5466a4','#9ca8cc','#e6dccc','#f6f0e6']    # pale heaven of the starving gods
SKY_EARTH=['#2f6ad0','#7ab8f0','#ffe6c4','#fff8ea']     # bright morning on earth
SKY_FIRE=['#3a4ab0','#e8946a','#ffc878','#fff2d0']      # warm fire-gold sky for Agni
SKY_NATURE=['#2a72c8','#86cce4','#e4f4c4','#fffbe8']    # Prakriti's green world
SKY_WED=['#4656b8','#f2a478','#ffda94','#fff6de']       # wedding gold
SKY_GRAY=['#6a7490','#a0a8bc','#d4d6dc','#eeeef0']      # an offering that never arrives
RIDGE_EARTH=['#a8c4e4','#8ab8c8','#6aa47e','#4a8a5a']
RIDGE_NATURE=['#a8d0e0','#88c0a8','#5aa86a','#3a8a4a']
GOLD='#e8c878'
def far_loka(haze='#eef0fa',col='#ffffff',xs=(500,800),mc='#a4b0dc'):
    return {"d":"far","contents":"soft cloud banks and two hazy peaks of Brahmaloka far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-60,"y":500,"s":1.0,"col":mc},{"o":"mountain","x":xs[1]+40,"y":510,"s":0.85,"col":mc},
                     {"o":"cloud","x":xs[0],"y":230,"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":270,"s":1.1,"col":col}]}
def mid_pillars(xs=(450,830),col=GOLD,h=520):
    return {"d":"mid","contents":"two gold pillars of Brahma's hall framing the figure","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810),col='#ffffff'):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":col},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":col}]}
def far_hills(haze='#eef4fa',xs=(500,800),col='#9ab4d4'):
    return {"d":"far","contents":"low blue hills and white clouds in haze on the horizon","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0],"y":392,"s":1.0,"w":230,"h":120,"col":col,"snow":False},{"o":"mountain","x":xs[1],"y":395,"s":1.0,"w":200,"h":90,"col":col,"snow":False},
                     {"o":"cloud","x":xs[0]+40,"y":200,"s":1.1,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":250,"s":0.9,"col":"#ffffff"}]}
def ground(x=640,y=660,w=640,h=60,col='#c8d890'):return {"o":"hill","x":x,"y":y,"s":1.0,"w":w,"h":h,"col":col}
def mid_village(xs=(440,850),hut=None,flowers='#f0a020',gx=640):
    it=[{"o":"tree","x":xs[0],"y":610,"s":0.8,"kind":"banyan","col":"#2e7a44"},{"o":"tree","x":xs[1],"y":605,"s":0.75,"kind":"round","col":"#3a8a4a","flowers":flowers}]
    if hut:it.insert(1,{"o":"hut","x":hut[0],"y":hut[1],"s":hut[2],"lamp":True})
    it.append(ground(gx))
    return {"d":"mid","contents":"the village yard: a banyan, a flowering tree, a thatched house and the beaten earth of the yard","fog":0.18,"items":it}
def near_shrubs(xs=(450,830),col='#2a5a3a'):
    return {"d":"near","contents":"dark blurred shrubs with marigolds in the bottom corners","dark":0.45,
            "items":[{"o":"shrub","x":xs[0],"y":748,"s":1.5,"col":col,"flowers":"#f0c040"},{"o":"shrub","x":xs[1],"y":750,"s":1.4,"col":col}]}
def earth_bg(sky=SKY_EARTH,sx=700,sy=230,**k):
    d={"k":"vista","sky":sky,"sx":sx,"sy":sy,"ridge":RIDGE_EARTH,"haze":"240,246,255"};d.update(k);return d
def loka_bg(sky=SKY_LOKA,sx=640,sy=190):return {"k":"cloudscape","sky":sky,"sx":sx,"sy":sy}
def kund(x,y,w=180,word=None,front=True):
    e={"k":"havan_kund","x":x,"y":y,"w":w,"alpha":1,"par":1.0,"meaning":"the brick fire altar of the yajna with its bright fire"}
    if word:e["word"]=word
    if not front:e["behind"]=True
    return e
def glow(x,y,r,rgb,ga,word=None,behind=True,meaning="warm firelight"):
    e={"k":"glow","x":x,"y":y,"r":r,"rgb":rgb,"ga":ga,"par":1.0,"behind":behind,"meaning":meaning}
    if word:e["word"]=word
    return e
def name(word,s,x,y=120,size=30):return {"k":"name","word":word,"s":s,"x":x,"y":y,"size":size,"meaning":f"the name {s} on screen when it is spoken"}
def orbs(items,word,meaning):
    """light motes travelling on a path; items: (x0,y0,x1,y1,cue_word,dur[,keep]) -> engine orbs items (c filled in later)"""
    its=[{"x0":a,"y0":b,"x1":c,"y1":d,"_w":w,"dur":du,"r":46,"rgb":"255,224,140","sz":6,"arc":10,**({"keep":True} if len(r)>0 and r[0] else {})} for (a,b,c,d,w,du,*r) in items]
    return {"k":"orbs","word":word,"items":its,"par":1.0,"meaning":meaning}
def gate(x,y,w,a=0.9,par=0.4):return {"k":"palace_gate","x":x,"y":y,"w":w,"alpha":a,"par":par,"behind":True,"meaning":"the gold gateway of Brahmaloka, heaven, at the top of the path"}
def beam(x,y,w,a=0.6,word=None):
    e={"k":"light_beam","x":x,"y":y,"w":w,"alpha":a,"blend":"lighter","par":1.0,"behind":True,"meaning":"the path of light from the fire up to heaven"}
    if word:e["word"]=word
    return e
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!"')}};s.update(k);return s
def cam(move,a,b,shot_='medium',lens='normal',shake=0,mot=''):
    z0,x0,y0=a;z1,x1,y1=b
    return {"shot":shot_,"lens":lens,"move":move,"from":{"z":z0,"x":x0,"y":y0,"r":0},"to":{"z":z1,"x":x1,"y":y1,"r":0},"shake":shake,"motivation":mot}
# heaven-above / earth-below scene for the stack shots: heaven on the left of the 16:9 frame, earth on the right
def stack_layers(bright=True):
    return [{"d":"far","contents":"cloud banks of heaven on the left, low blue hills of earth on the right","fog":0.55,"haze":"#eef2fa",
             "items":[{"o":"cloud","x":380,"y":230,"s":1.3,"col":"#ffffff"},{"o":"cloud","x":300,"y":420,"s":1.4,"col":"#ffffff"},
                      {"o":"mountain","x":900,"y":520,"s":1.0,"w":260,"h":120,"col":"#9ab4d4","snow":False},{"o":"mountain","x":1080,"y":525,"s":1.0,"w":220,"h":90,"col":"#9ab4d4","snow":False}]},
            {"d":"mid","contents":"gold pillars in heaven; the green yard, a thatched house and a banyan on earth","fog":0.18,
             "items":[{"o":"pillar","x":250,"y":700,"s":1.0,"col":GOLD if bright else '#d8c8a0',"h":520},{"o":"pillar","x":560,"y":700,"s":1.0,"col":GOLD if bright else '#d8c8a0',"h":520},
                      {"o":"tree","x":1090,"y":600,"s":0.8,"kind":"banyan","col":"#2e7a44"},{"o":"hut","x":760,"y":590,"s":0.8,"lamp":True},
                      {"o":"hill","x":900,"y":700,"s":1.0,"w":560,"h":120,"col":"#c8d890"}]},
            {"d":"near","contents":"white cloud puffs under the gods, marigold shrubs on earth","dark":0.1,"blur":2,
             "items":[{"o":"cloud","x":330,"y":690,"s":1.8,"col":"#ffffff"},{"o":"cloud","x":520,"y":700,"s":1.5,"col":"#ffffff"}]}]
S=[]
# 1 ---------------------------------------------------------------- hook: offerings to Agni
S.append(shot("s01",0.16,
 meaning="Every offering made to Agni, the fire god, is the subject of this story.",
 why="Agni, ember-skinned with his flame crown and fire halo, stands behind a blazing brick fire altar in a bright village yard below the title card and opens his arms over the flames on 'fire'.",
 camera=cam("push_in",(1.0,0,0),(1.05,0,-6),"medium","normal",0,"slow push in to meet the god the whole story is about"),
 focus={"subject":"agni","depth":"deep"},vertical={"focus":"agni"},
 layers=[far_hills(),mid_village((450,830)),near_shrubs()],
 background=earth_bg(sky=SKY_FIRE,sx=640,sy=200),mood={"emotion":"reverence","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":690,"s":1.0,"_face":0.49,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.4},"look":640,
   "actions":[{"word":"fire","pose":"open","emo":"joy","e":"spring","d":0.6}]}],
 effects=[glow(640,360,300,"255,170,80",0.5,meaning="Agni's warm fire light around him"),kund(640,668,230)],
 transition_in="fade"))
# 2 ---------------------------------------------------------------- ends with Swaha
S.append(shot("s02",2.48,
 meaning="Each of those offerings ends with one word: Swaha.",
 why="A village priest sits at the altar and pours an offering into the fire; as he says the last word the flames flare gold and the name 'Swaha' appears above.",
 camera=cam("dolly_right",(1.05,-10,0),(1.05,10,0),"medium","normal",0,"a sideways drift from the priest to the fire he feeds"),
 focus={"subject":"villager","depth":"deep"},vertical={"x":[630,660]},
 layers=[far_hills(xs=(520,800)),mid_village((440,860),hut=(560,590,0.75)),near_shrubs((460,830))],
 background=earth_bg(sx=760),mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"villager","x":575,"y":670,"s":1.0,"_face":0.43,"flip":1,"pose":"sitpray","emo":"devotion","talk":0.6,"look":760,
   "actions":[{"word":"word","pose":"open","emo":"devotion","d":0.6}]}],
 effects=[kund(745,650,190),glow(745,520,200,"255,190,90",0.6,word="Swaha",meaning="the fire flaring gold as the word is said"),
  orbs([(640,430,740,560,"word",0.9),(650,420,745,555,"Swaha",0.9)],"word","a handful of offering falling into the fire as round light motes"),
  name("Swaha","Swaha",650,118)],
 transition_in="cut"))
# 3 ---------------------------------------------------------------- the gods once starved
S.append(shot("s03",4.54,
 meaning="Once, the gods themselves were starving.",
 why="High and wide over a pale, empty hall of heaven: three thin gods sit slumped on the clouds between faded pillars, heads hanging.",
 camera=cam("crane_down",(1.0,0,-20),(1.0,0,0),"high_angle","wide",0,"looking down on the gods from above shows how low they have fallen"),
 focus={"subject":"deva_thin","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_loka('#eceef4','#f6f6fa',mc='#b0b8d0'),mid_pillars((450,830),col='#d8ccaa'),near_clouds()],
 background=loka_bg(sky=SKY_HUNGRY),mood={"emotion":"hunger","grade":"cool"},
 characters=[{"who":"deva_thin","x":640,"y":660,"s":0.85,"_face":0.45,"flip":1,"pose":"sit","emo":"sad","mood":{"ly":0.6},"look":700,
   "actions":[{"word":"starved","emo":"grief","tilt":-0.06,"d":0.5}]},
  {"who":"deva_thin2","x":540,"y":640,"s":0.72,"_face":0.41,"flip":1,"pose":"sit","emo":"sad","mood":{"ly":0.5},"look":640},
  {"who":"indra_thin","x":745,"y":640,"s":0.72,"_face":0.41,"flip":-1,"pose":"sit","emo":"sad","mood":{"ly":0.5},"look":640}],
 effects=[],
 transition_in="fade"))
# 4 ---------------------------------------------------------------- while humans fed the fire (stack: heaven above, earth below)
S.append(shot("s04",5.94,
 meaning="Down on earth, humans fed the sacred fire regularly while the gods went hungry.",
 why="Stacked: above, a thin god in pale heaven looks down with sad eyes; below, on bright earth, a villager pours offerings into a blazing fire altar.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"two_shot","normal",0,"two still worlds side by side make the contrast plain"),
 focus={"subject":"villager","depth":"deep"},vertical={"mode":"stack","stack":["deva_thin","villager"]},
 layers=stack_layers(False),
 background=loka_bg(sky=SKY_HUNGRY,sx=900,sy=200),mood={"emotion":"contrast","grade":"warm"},
 characters=[{"who":"deva_thin","x":400,"y":650,"s":0.95,"flip":1,"pose":"stand","emo":"sad","mood":{"ly":0.6},"look":900,
   "actions":[{"word":"fed","emo":"grief","mood":{"ly":0.7},"d":0.6}]},
  {"who":"villager","x":860,"y":680,"s":0.95,"flip":1,"pose":"sitpray","emo":"devotion","look":1000,"talk":0.5,
   "actions":[{"word":"fed","pose":"open","d":0.6}]}],
 effects=[kund(985,665,170),glow(985,560,180,"255,180,80",0.55,meaning="the bright fire on earth"),
  orbs([(930,520,985,600,"fed",0.9),(940,510,990,600,"fed",1.3)],"fed","offerings falling into the fire as light motes")],
 transition_in="cut"))
# 5 ---------------------------------------------------------------- Agni said it was his fault
S.append(shot("s05",8.5,
 meaning="Agni, the fire god, admitted that the gods' hunger was his own fault.",
 why="Close on Agni with folded hands: his fire halo burns low and on 'fault' he lowers his eyes and bows his head in shame.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"close","tele",0,"push in on the admission of guilt"),
 focus={"subject":"agni","depth":"shallow"},vertical={"focus":"agni","z":1.2,"y":0.42},
 layers=[far_loka('#f8ece0','#fff4ea'),mid_pillars((470,810)),near_clouds((480,800))],
 background=loka_bg(sky=SKY_FIRE),mood={"emotion":"guilt","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"namaste","emo":"sad","talk":0.6,"look":640,
   "actions":[{"word":"himself","emo":"shame","d":0.5},{"word":"fault","emo":"shame","mood":{"ly":0.7},"tilt":-0.07,"d":0.6}]}],
 effects=[glow(640,330,220,"255,150,70",0.4,meaning="Agni's own fire, burning low with his guilt")],
 transition_in="fade"))
# 6 ---------------------------------------------------------------- one morning the gods came to Brahma
S.append(shot("s06",11.32,
 meaning="One morning the starving gods came to Brahma, the creator.",
 why="Morning sun over the gold hall of heaven: two thin gods walk in from the left and the window pans with them to four-headed Brahma on his lotus, who looks up as his name is said.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan travels with the gods to the creator"),
 focus={"subject":"brahma","depth":"deep"},vertical={"x":[500,780]},
 layers=[far_loka(xs=(520,820)),{"d":"mid","contents":"gold pillars of Brahma's hall","fog":0.2,"items":[{"o":"pillar","x":330,"y":700,"s":1.0,"col":GOLD,"h":520},{"o":"pillar","x":980,"y":700,"s":1.0,"col":GOLD,"h":520}]},near_clouds((420,900))],
 background=loka_bg(sky=SKY_DAWN,sx=820,sy=300),mood={"emotion":"arrival","grade":"warm"},
 characters=[{"who":"brahma","x":800,"y":660,"s":1.0,"_face":0.45,"flip":-1,"pose":"sit","emo":"calm","look":"deva_thin",
   "actions":[{"word":"Brahma","emo":"surprise","mood":{"surp":0.4},"d":0.5},{"word":"creator","emo":"calm","mood":{"smile":0.3},"d":0.6}]},
  {"who":"deva_thin","x":470,"y":665,"s":0.9,"_face":0.45,"flip":1,"pose":"stand","emo":"sad","look":"brahma","walk":{"word":"came","to_x":580,"d":1.6,"speed":1}},
  {"who":"deva_thin2","x":380,"y":665,"s":0.88,"_ground":True,"flip":1,"pose":"stand","emo":"sad","look":"brahma","walk":{"word":"came","to_x":480,"d":1.6,"speed":1}}],
 effects=[name("Brahma","Brahma",760,118),glow(820,300,240,"255,220,150",0.4,meaning="morning light in Brahmaloka")],
 transition_in="fade"))
# 7 ---------------------------------------------------------------- in Brahmaloka
S.append(shot("s07",14.48,
 meaning="They met him in Brahmaloka, Brahma's own heaven.",
 why="Wide on Brahmaloka: a gold gateway stands on the clouds, Brahma sits on his pink lotus before it, and the name plate appears as 'Brahmaloka' is said.",
 camera=cam("crane_up",(1.04,0,12),(1.0,0,-8),"establishing","wide",0,"rising to show the whole heaven of the creator"),
 focus={"subject":"brahma","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_loka(xs=(500,800)),mid_pillars((450,830),h=480),near_clouds((460,820))],
 background=loka_bg(sky=SKY_LOKA,sy=220),mood={"emotion":"majesty","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":665,"s":0.85,"_face":0.47,"flip":1,"pose":"sit","emo":"calm","mood":{"smile":0.4},"look":560,
   "actions":[{"word":"Brahmaloka","mood":{"smile":0.6,"ly":-0.2},"d":0.6}]}],
 effects=[gate(640,330,240,0.85),name("Brahmaloka","Brahmaloka",640,110),
  {"k":"divine_rays","x":640,"y":60,"w":640,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of Brahma's heaven"}],
 transition_in="cut"))
# 8 ---------------------------------------------------------------- thin and weak, nothing to eat
S.append(shot("s08",15.86,
 meaning="The gods were thin and weak because they had nothing to eat.",
 why="Two thin gods in faded cloth stand close together; one sags on 'weak', and on 'nothing' both open their empty hands to Brahma.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-6),"two_shot","normal",0,"push in on their hunger"),
 focus={"subject":"deva_thin","depth":"deep"},vertical={"x":[640,640],"z":1.05,"y":0.42},
 layers=[far_loka('#eceef4','#f6f6fa',mc='#b0b8d0'),mid_pillars((440,840),col='#d8ccaa'),near_clouds()],
 background=loka_bg(sky=SKY_HUNGRY,sx=700),mood={"emotion":"weakness","grade":"cool"},
 characters=[{"who":"deva_thin","x":575,"y":665,"s":1.0,"_face":0.44,"flip":1,"pose":"stand","emo":"sad","look":800,
   "actions":[{"word":"weak","emo":"grief","tilt":-0.07,"d":0.6},{"word":"nothing","pose":"open","emo":"grief","d":0.6}]},
  {"who":"deva_thin2","x":710,"y":665,"s":0.98,"_ground":True,"flip":-1,"pose":"stand","emo":"sad","look":500,
   "actions":[{"word":"thin","emo":"grief","mood":{"ly":0.5},"d":0.6},{"word":"eat","pose":"open","emo":"sad","d":0.6}]}],
 effects=[],
 transition_in="cut"))
# 9 ---------------------------------------------------------------- Brahma explains
S.append(shot("s09",19.48,
 meaning="Brahma explained how the gods were meant to be fed.",
 why="Brahma on his lotus speaks with an open teaching hand, his Veda book at his side and a soft gold ring of light behind his heads.",
 camera=cam("dolly_left",(1.12,12,0),(1.12,-12,0),"medium","normal",0,"a calm drift while the creator explains"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.12,"y":0.42},
 layers=[far_loka(xs=(520,780)),mid_pillars((460,820)),near_clouds((470,810))],
 background=loka_bg(sky=SKY_LOKA,sx=700),mood={"emotion":"teaching","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":660,"s":1.05,"_face":0.44,"flip":-1,"pose":"sit","emo":"calm","talk":0.6,"look":420,"mood":{"smile":0.3},
   "actions":[{"word":"explained","pose":"open","emo":"calm","d":0.6},{"word":"eat","mood":{"smile":0.5,"ly":0.2},"tilt":0.04,"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"explained","x":640,"y":300,"w":420,"alpha":0.4,"blend":"lighter","par":0.9,"behind":True,"meaning":"the creator's knowledge as a ring of gold light"}],
 transition_in="cut"))
# 10 --------------------------------------------------------------- humans held a yajna
S.append(shot("s10",22.02,
 meaning="On earth humans hold a yajna, a sacred fire ritual.",
 why="Bright earth: a village man and woman sit facing each other across a blazing brick fire altar in their yard, hands folded, and the word 'Yajna' appears above the fire.",
 camera=cam("crane_down",(1.0,0,-20),(1.0,0,0),"wide","wide",0,"descending from heaven down to the fire on earth"),
 focus={"subject":"villager","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_hills(),mid_village((440,850),hut=(640,575,0.75)),near_shrubs()],
 background=earth_bg(sx=640,sy=200),mood={"emotion":"ritual","grade":"warm"},
 characters=[{"who":"villager","x":548,"y":668,"s":0.85,"_face":0.45,"flip":1,"pose":"sitpray","emo":"devotion","look":"villager_w",
   "actions":[{"word":"ritual","mood":{"blink":0.6,"smile":0.4},"d":0.6}]},
  {"who":"villager_w","x":735,"y":668,"s":0.82,"_ground":True,"flip":-1,"pose":"sitpray","emo":"devotion","look":"villager",
   "actions":[{"word":"yajna","mood":{"smile":0.5},"d":0.6}]}],
 effects=[kund(642,668,170),glow(642,560,200,"255,180,80",0.55,meaning="the fire of the yajna lighting the yard"),name("yajna","Yajna",640,118)],
 transition_in="iris"))
# 11 --------------------------------------------------------------- they poured offerings
S.append(shot("s11",24.72,
 meaning="They poured offerings of grain and ghee into the fire.",
 why="Closer: the village woman stretches both hands over the altar and a stream of round gold offering-motes falls from her hands into the flames, which flare up on 'fire'.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"medium","normal",0,"push in on the act of giving"),
 focus={"subject":"villager_w","depth":"deep"},vertical={"x":[650,680],"z":1.1,"y":0.42},
 layers=[far_hills(xs=(520,800)),mid_village((450,880)),near_shrubs((470,840))],
 background=earth_bg(sx=700),mood={"emotion":"offering","grade":"warm"},
 characters=[{"who":"villager_w","x":610,"y":668,"s":1.0,"_face":0.43,"flip":1,"pose":"sitpray","emo":"devotion","look":760,
   "actions":[{"word":"poured","pose":"open","emo":"joy","d":0.5}]}],
 effects=[kund(760,662,190),glow(760,540,220,"255,190,90",0.6,word="fire",meaning="the flames flaring as they take the offering"),
  orbs([(690,440,755,570,"poured",0.8),(700,430,760,570,"poured",1.1),(690,445,765,570,"fire",0.8)],"poured","grain and ghee falling into the fire as round gold motes")],
 transition_in="cut"))
# 12 --------------------------------------------------------------- Agni, the mouth of the gods
S.append(shot("s12",26.92,
 meaning="Agni is the mouth of the gods: he receives what is offered to them.",
 why="Agni rises out of the altar fire, arms open to receive, his flame crown blazing; the name 'Agni' appears above him.",
 camera=cam("tilt_up",(1.0,0,18),(1.0,0,0),"medium","normal",0,"tilt up with the god rising out of the flames"),
 focus={"subject":"agni","depth":"deep"},vertical={"focus":"agni"},
 layers=[far_hills(xs=(500,800),haze='#fbf0e0'),mid_village((440,850)),near_shrubs()],
 background=earth_bg(sky=SKY_FIRE,sx=640,sy=180),mood={"emotion":"power","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","look":640,"mood":{"smile":0.3},
   "actions":[{"word":"Agni","pose":"open","emo":"joy","e":"spring","d":0.5},{"word":"mouth","mood":{"smile":0.6,"mouth":0.4},"d":0.5}]}],
 effects=[glow(640,330,280,"255,160,70",0.55,meaning="the blaze of the fire god"),kund(640,690,260),name("Agni","Agni",640,112)],
 transition_in="cut"))
# 13 --------------------------------------------------------------- carried them to heaven (the path)
S.append(shot("s13",28.7,
 meaning="Agni carried the offerings up from earth to the gods in heaven.",
 why="A column of light rises from the altar fire at the bottom of the frame to the gold gateway of Brahmaloka in the clouds at the top; Agni rides up the column with raised arms and gold offering-motes climb past him to the gate.",
 camera=cam("pull_out",(1.08,0,10),(1.0,0,-6),"wide","wide",0,"pulling out to show the whole road from earth to heaven"),
 focus={"subject":"agni","depth":"deep"},vertical={"x":[640,640]},
 layers=[{"d":"far","contents":"bright cloud banks of heaven across the top of the sky","fog":0.5,"haze":"#f6f2ea","items":[{"o":"cloud","x":500,"y":130,"s":1.4,"col":"#ffffff"},{"o":"cloud","x":790,"y":120,"s":1.3,"col":"#ffffff"},{"o":"mountain","x":420,"y":540,"s":1.0,"w":220,"h":90,"col":"#9ab4d4","snow":False}]},
   {"d":"mid","contents":"a banyan and a flowering tree on earth beside the altar","fog":0.2,"items":[{"o":"tree","x":470,"y":640,"s":0.7,"kind":"banyan","col":"#2e7a44"},{"o":"tree","x":820,"y":640,"s":0.65,"kind":"round","col":"#3a8a4a","flowers":"#f0a020"},ground(640,690,600,50)]},
   near_shrubs((450,840))],
 background=earth_bg(sky=['#3a6ad0','#8ab8f0','#ffe2b0','#fff6e4'],sx=640,sy=120),mood={"emotion":"ascent","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":520,"s":0.72,"_face":0.40,"flip":1,"pose":"raise","emo":"joy","look":640,"mood":{"ly":-0.6},
   "actions":[{"word":"heaven","mood":{"smile":0.8,"ly":-0.8},"d":0.5}]}],
 effects=[beam(640,640,120,0.55),gate(640,95,120,0.95,0.6),kund(640,670,170),
  orbs([(620,600,630,95,"carried",1.2),(660,620,650,95,"carried",1.6),(640,610,640,95,"heaven",1.6),(630,600,640,95,"heaven",1.2)],"carried","the offerings travelling up the light to heaven as gold motes"),
  glow(640,95,140,"255,230,160",0.6,word="heaven",meaning="the gate of heaven lighting up as the offerings arrive")],
 transition_in="cut"))
# 14 --------------------------------------------------------------- in return, blessings (stack)
S.append(shot("s14",30.18,
 meaning="In return the gods sent blessings down to the humans.",
 why="Stacked: above, a god in bright heaven raises a blessing hand; below, the villager at his fire folds his hands with joy as warm rays fall on him.",
 camera=cam("tilt_down",(1.0,0,-10),(1.0,0,0),"two_shot","normal",0,"tilting down with the blessing as it falls to earth"),
 focus={"subject":"villager","depth":"deep"},vertical={"mode":"stack","stack":["deva_thin2","villager"]},
 layers=stack_layers(True),
 background=loka_bg(sky=SKY_LOKA,sx=900,sy=200),mood={"emotion":"blessing","grade":"warm"},
 characters=[{"who":"deva_thin2","x":400,"y":650,"s":0.95,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.6},"look":900,
   "actions":[{"word":"gave","pose":"raise","emo":"joy","d":0.6}]},
  {"who":"villager","x":860,"y":680,"s":0.95,"flip":1,"pose":"sitpray","emo":"joy","look":1000,
   "actions":[{"word":"blessings","mood":{"smile":0.9,"ly":-0.4},"d":0.6}]}],
 effects=[kund(985,665,170),{"k":"divine_rays","word":"gave","x":880,"y":300,"w":420,"alpha":0.45,"blend":"lighter","par":0.6,"behind":True,"meaning":"the blessing falling on the man as warm rays of light"},
  glow(860,470,200,"255,226,150",0.5,word="blessings",meaning="the blessing reaching him")],
 transition_in="fade"))
# 15 --------------------------------------------------------------- Indra
S.append(shot("s15",33.04,
 meaning="Indra, one of the leaders of the gods, spoke up.",
 why="Thin Indra, still in his tall crown with his vajra, stands in the pale hall with a dimmed blue halo; his name appears as it is said.",
 camera=cam("crane_up",(1.04,0,12),(1.04,0,-4),"medium","normal",0,"rising to the king of the gods"),
 focus={"subject":"indra_thin","depth":"deep"},vertical={"focus":"indra_thin"},
 layers=[far_loka('#eceef4','#f6f6fa',mc='#b0b8d0'),mid_pillars((450,830),col='#d8ccaa'),near_clouds()],
 background=loka_bg(sky=SKY_HUNGRY),mood={"emotion":"pride","grade":"cool"},
 characters=[{"who":"indra_thin","x":640,"y":665,"s":1.02,"_face":0.43,"flip":1,"pose":"stand","emo":"sad","look":560,
   "actions":[{"word":"leader","emo":"pride","mood":{"ly":-0.2},"d":0.6}]}],
 effects=[name("Indra","Indra",640,115),glow(640,320,200,"170,190,255",0.35,meaning="Indra's dimmed blue halo")],
 transition_in="cut"))
# 16 --------------------------------------------------------------- humans held yajnas all the time
S.append(shot("s16",34.9,
 meaning="Indra said that humans held fire rituals all the time.",
 why="Indra points down toward earth as he speaks; far below the clouds three little columns of yajna smoke rise from the villages, proof that the rituals go on.",
 camera=cam("dolly_right",(1.08,-10,0),(1.08,10,0),"medium","normal",0,"a drift that follows his pointing arm"),
 focus={"subject":"indra_thin","depth":"deep"},vertical={"focus":"indra_thin","z":1.08,"y":0.42},
 layers=[far_loka('#eceef4','#f6f6fa',mc='#b0b8d0'),mid_pillars((440,860),col='#d8ccaa'),near_clouds((460,830))],
 background=loka_bg(sky=SKY_HUNGRY,sx=760),mood={"emotion":"complaint","grade":"cool"},
 characters=[{"who":"indra_thin","x":600,"y":665,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"doubt","talk":0.7,"look":800,
   "actions":[{"word":"humans","pose":"point","emo":"anger","d":0.5},{"word":"time","emo":"doubt","mood":{"ly":0.3},"d":0.6}]}],
 effects=[{"k":"smoke_plume","x":735,"y":520,"w":110,"alpha":0.7,"par":0.3,"behind":True,"meaning":"smoke of a yajna rising far below on earth"},
  {"k":"smoke_plume","x":800,"y":540,"w":80,"alpha":0.6,"par":0.3,"behind":True,"meaning":"a second far yajna fire on earth"}],
 transition_in="cut"))
# 17 --------------------------------------------------------------- nothing reached heaven
S.append(shot("s17",37.32,
 meaning="Yet none of those offerings ever reached heaven.",
 why="Above, a thin god sits on a cloud with an empty gaze looking down; below, the smoke and gold motes rising from an earth altar thin out and vanish into a gray mist halfway up.",
 camera=cam("tilt_up",(1.0,0,16),(1.0,0,0),"wide","normal",0,"tilting up along the path that goes nowhere"),
 focus={"subject":"deva_thin","depth":"deep"},vertical={"x":[640,640]},
 layers=[{"d":"far","contents":"pale clouds of heaven along the top","fog":0.55,"haze":"#eceef4","items":[{"o":"cloud","x":500,"y":150,"s":1.3,"col":"#f4f4f8"},{"o":"cloud","x":800,"y":170,"s":1.2,"col":"#f4f4f8"}]},
   {"d":"mid","contents":"a cloud ledge under the god and the hazy earth with a tree far below","fog":0.3,"items":[{"o":"cloud","x":640,"y":470,"s":1.6,"col":"#ffffff"},{"o":"tree","x":470,"y":660,"s":0.6,"kind":"round","col":"#4a8a5a"},ground(640,700,600,50)]},
   near_clouds((450,840),'#f0f0f4')],
 background=loka_bg(sky=SKY_GRAY,sx=640,sy=160),mood={"emotion":"emptiness","grade":"cool"},
 characters=[{"who":"deva_thin","x":640,"y":430,"s":0.75,"_face":0.39,"flip":1,"pose":"sit","emo":"grief","look":640,"mood":{"ly":0.8},
   "actions":[{"word":"nothing","emo":"grief","tilt":-0.06,"d":0.5}]}],
 effects=[kund(640,690,140),{"k":"smoke_plume","x":640,"y":650,"w":180,"alpha":0.7,"par":1.0,"meaning":"smoke of the offering rising from the altar"},
  orbs([(630,640,640,470,"nothing",1.0),(650,640,640,460,"nothing",1.4)],"nothing","offering motes rising and fading out before they reach heaven"),
  {"k":"mist_wisps","x":640,"y":510,"w":460,"alpha":0.8,"par":1.0,"meaning":"a gray mist where the offerings are lost"}],
 transition_in="fade"))
# 18 --------------------------------------------------------------- Kamadev
S.append(shot("s18",38.98,
 meaning="Another god, Kamadev, the god of love, stepped in.",
 why="Kamadev in a rose dhoti and parrot-green shawl, his sugarcane bow in hand, turns with a proud, sharp look as his name appears.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the accuser"),
 focus={"subject":"kama","depth":"deep"},vertical={"focus":"kama"},
 layers=[far_loka(xs=(520,800)),mid_pillars((450,830)),near_clouds()],
 background=loka_bg(sky=['#3a52b0','#e0a0c0','#ffd0b0','#fff2e4']),mood={"emotion":"anger","grade":"warm"},
 characters=[{"who":"kama","x":640,"y":665,"s":1.02,"_face":0.43,"flip":-1,"pose":"stand","emo":"pride","look":440,
   "actions":[{"word":"Kamadev","emo":"anger","mood":{"anger":0.6},"d":0.5}]}],
 effects=[name("Kamadev","Kamadev",640,115),glow(640,330,200,"255,170,200",0.35,meaning="Kamadev's rose light")],
 transition_in="cut"))
# 19 --------------------------------------------------------------- blamed Agni (stack)
S.append(shot("s19",40.64,
 meaning="Kamadev blamed Agni for the gods' hunger.",
 why="Stacked: above, Kamadev jabs a finger downward in anger; below, Agni hears the charge and lowers his eyes in shame.",
 camera=cam("handheld",(1.0,0,0),(1.02,0,0),"two_shot","normal",1,"a slight tremor of the quarrel"),
 focus={"subject":"agni","depth":"deep"},vertical={"mode":"stack","stack":["kama","agni"]},
 layers=[far_loka(xs=(400,860)),{"d":"mid","contents":"gold pillars of Brahma's hall behind both gods","fog":0.2,"items":[{"o":"pillar","x":230,"y":700,"s":1.0,"col":GOLD,"h":520},{"o":"pillar","x":1050,"y":700,"s":1.0,"col":GOLD,"h":520}]},near_clouds((300,980))],
 background=loka_bg(sky=SKY_LOKA),mood={"emotion":"accusation","grade":"warm"},
 characters=[{"who":"kama","x":420,"y":650,"s":0.95,"flip":1,"pose":"point","emo":"anger","talk":0.7,"look":"agni",
   "actions":[{"word":"blamed","emo":"anger","mood":{"anger":0.8},"d":0.4}]},
  {"who":"agni","x":860,"y":660,"s":0.95,"flip":-1,"pose":"stand","emo":"sad","look":"kama",
   "actions":[{"word":"Agni","emo":"shame","mood":{"ly":0.5},"d":0.5}]}],
 effects=[],
 transition_in="cut"))
# 20 --------------------------------------------------------------- Agni stepped forward with folded hands
S.append(shot("s20",41.98,
 meaning="Agni stepped forward before everyone with folded hands.",
 why="Agni walks forward out of the group of thin gods, palms folded; the gods behind him turn their eyes to him.",
 camera=cam("dolly_right",(1.04,-14,0),(1.04,10,0),"medium","normal",0,"the dolly moves with his step forward"),
 focus={"subject":"agni","depth":"deep"},vertical={"focus":"agni"},
 layers=[far_loka(xs=(520,800)),mid_pillars((430,850)),near_clouds()],
 background=loka_bg(sky=SKY_LOKA,sx=700),mood={"emotion":"humility","grade":"warm"},
 characters=[{"who":"deva_thin","x":800,"y":600,"s":0.72,"_face":0.40,"flip":-1,"pose":"stand","emo":"sad","look":"agni","engine":{"a":0.8}},
  {"who":"agni","x":560,"y":665,"s":1.0,"_face":0.44,"flip":1,"pose":"namaste","emo":"sad","look":700,"walk":{"word":"stepped","to_x":650,"d":1.4,"speed":1},
   "actions":[{"word":"folded","emo":"shame","mood":{"ly":0.3},"d":0.6}]}],
 effects=[glow(620,330,200,"255,160,80",0.35,meaning="Agni's fire, low and humble")],
 transition_in="cut"))
# 21 --------------------------------------------------------------- he was to blame
S.append(shot("s21",44.4,
 meaning="Agni said that he himself was to blame.",
 why="Close on Agni's face: he speaks with his eyes lowered and his head bowed, owning the fault.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"close","tele",0,"push in on the confession"),
 focus={"subject":"agni","depth":"shallow"},vertical={"focus":"agni"},
 layers=[far_loka('#f8ece0','#fff4ea',(500,800)),mid_pillars((450,830)),near_clouds()],
 background=loka_bg(sky=SKY_FIRE),mood={"emotion":"confession","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":360,"s":1.15,"flip":-1,"head":True,"emo":"sad","talk":0.6,"mood":{"ly":0.4},
   "actions":[{"word":"blame","emo":"shame","mood":{"ly":0.7},"tilt":-0.06,"d":0.5}]}],
 effects=[],
 transition_in="cut"))
# 22 --------------------------------------------------------------- he could burn the offerings
S.append(shot("s22",46.02,
 meaning="Agni could burn the offerings that humans gave him.",
 why="Agni stands over a roaring altar fire with an open hand: the flames leap high and the offerings burn bright gold.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"medium","normal",0,"pulling back to show the great fire he commands"),
 focus={"subject":"agni","depth":"deep"},vertical={"focus":"agni"},
 layers=[far_hills(xs=(500,800),haze='#fbf0e0'),mid_village((440,850)),near_shrubs()],
 background=earth_bg(sky=SKY_FIRE,sx=640,sy=200),mood={"emotion":"power","grade":"warm"},
 characters=[{"who":"agni","x":640,"y":665,"s":1.0,"_face":0.44,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"burn","pose":"open","emo":"pride","d":0.5}]}],
 effects=[glow(640,450,300,"255,160,60",0.6,word="burn",meaning="the fire roaring as it burns the offerings"),kund(640,690,280),
  {"k":"flames","word":"burn","x":640,"y":560,"sc":1.2,"n":8,"meaning":"tall flames of the burning offerings"}],
 transition_in="fade"))
# 23 --------------------------------------------------------------- but he could not carry them
S.append(shot("s23",47.34,
 meaning="Agni could not carry the offerings up to the gods; he did not have that skill.",
 why="Agni looks up and lifts his hands as gold offering-motes drift up from him and fade out in the empty sky; on 'skill' he drops his eyes in sorrow.",
 camera=cam("tilt_up",(1.0,0,14),(1.0,0,-6),"medium","normal",0,"tilting up after the offerings that never arrive"),
 focus={"subject":"agni","depth":"deep"},vertical={"focus":"agni"},
 layers=[{"d":"far","contents":"empty pale clouds high above","fog":0.55,"haze":"#eceef4","items":[{"o":"cloud","x":520,"y":140,"s":1.3,"col":"#f4f4f8"},{"o":"cloud","x":780,"y":180,"s":1.1,"col":"#f4f4f8"}]},
   mid_village((440,850)),near_shrubs()],
 background=earth_bg(sky=SKY_GRAY,sx=640,sy=160),mood={"emotion":"helplessness","grade":"cool"},
 characters=[{"who":"agni","x":640,"y":665,"s":1.0,"_face":0.45,"flip":1,"pose":"plead","emo":"sad","look":640,"mood":{"ly":-0.6},
   "actions":[{"word":"carry","mood":{"ly":-0.8},"d":0.5},{"word":"skill","emo":"grief","mood":{"ly":0.6},"tilt":-0.06,"d":0.6}]}],
 effects=[orbs([(610,300,580,70,"carry",1.4),(670,300,700,80,"carry",1.1),(640,290,650,60,"carry",1.8)],"carry","the offerings drifting up and fading before they reach the gods"),
  {"k":"mist_wisps","x":640,"y":120,"w":520,"alpha":0.6,"par":0.8,"meaning":"the gray mist where the offerings are lost"}],
 transition_in="cut"))
# 24 --------------------------------------------------------------- Brahma had no answer
S.append(shot("s24",51.34,
 meaning="Brahma, the creator, had no answer to the problem.",
 why="Brahma on his lotus sits silent and still with a troubled frown, his eyes lowered; the gold light of his hall cools on 'answer'.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness: the creator is stuck"),
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma","z":1.2,"y":0.42},
 layers=[far_loka(xs=(520,780)),mid_pillars((470,820)),near_clouds((480,800))],
 background={"k":"cloudscape","sky":SKY_LOKA,"sx":640,"sy":190,"change":{"word":"answer","bg2":{"k":"cloudscape","sky":SKY_HUNGRY,"sx":640,"sy":190},"d":1.0}},
 mood={"emotion":"doubt","grade":"cool"},
 characters=[{"who":"brahma","x":640,"y":660,"s":1.05,"_face":0.43,"flip":1,"pose":"sit","emo":"doubt","look":640,"mood":{"ly":0.4},
   "actions":[{"word":"no","emo":"doubt","mood":{"ly":0.6},"tilt":0.05,"d":0.6}]}],
 effects=[],
 transition_in="cut"))
# 25 --------------------------------------------------------------- Vishnu, the preserver
S.append(shot("s25",53.16,
 meaning="Vishnu, the preserver, came forward.",
 why="Blue four-armed Vishnu appears in a ring of light in the gold hall and opens his hand; his name appears as it is said.",
 camera=cam("tilt_down",(1.04,0,-16),(1.04,0,0),"medium","normal",0,"tilting down from the light to the god who has the answer"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_loka(xs=(520,780)),mid_pillars((450,830)),near_clouds()],
 background=loka_bg(sky=SKY_LOKA),mood={"emotion":"hope","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.02,"_face":0.43,"flip":-1,"pose":"stand","emo":"calm","mood":{"smile":0.5},"look":500,
   "actions":[{"word":"preserver","pose":"open","emo":"joy","d":0.6}]}],
 effects=[name("Vishnu","Vishnu",640,115),{"k":"halo_ring","word":"Vishnu","x":640,"y":320,"w":480,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"Vishnu's arrival in a ring of light"}],
 transition_in="fade"))
# 26 --------------------------------------------------------------- pray to Prakriti (stack)
S.append(shot("s26",54.7,
 meaning="Vishnu told Brahma to pray to Prakriti, Mother Nature.",
 why="Stacked: above, Vishnu speaks and points the way; below, Brahma on his lotus folds his hands in prayer while a green light of Mother Nature glows around him on 'Prakriti'.",
 camera=cam("crane_down",(1.0,0,-12),(1.0,0,0),"two_shot","normal",0,"from the adviser above down to Brahma who prays"),
 focus={"subject":"brahma","depth":"deep"},vertical={"mode":"stack","stack":["vishnu","brahma"]},
 layers=[far_loka(xs=(380,860)),{"d":"mid","contents":"gold pillars of the hall behind both","fog":0.2,"items":[{"o":"pillar","x":230,"y":700,"s":1.0,"col":GOLD,"h":520},{"o":"pillar","x":1050,"y":700,"s":1.0,"col":GOLD,"h":520}]},near_clouds((300,980))],
 background=loka_bg(sky=SKY_LOKA),mood={"emotion":"counsel","grade":"warm"},
 characters=[{"who":"vishnu","x":420,"y":650,"s":0.95,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":"brahma","mood":{"smile":0.5},
   "actions":[{"word":"told","pose":"point","d":0.5}]},
  {"who":"brahma","x":860,"y":660,"s":0.95,"flip":-1,"pose":"sit","emo":"calm","look":"vishnu",
   "actions":[{"word":"pray","pose":"sitpray","emo":"devotion","d":0.6}]}],
 effects=[glow(860,500,220,"150,230,120",0.5,word="Prakriti",meaning="the green light of Mother Nature answering the prayer")],
 transition_in="cut"))
# 27 --------------------------------------------------------------- Prakriti creates a young goddess
S.append(shot("s27",57.72,
 meaning="Prakriti, Mother Nature, created a young goddess.",
 why="In a green flowering world Prakriti opens her hands and, in a burst of warm light beside her, the young goddess Swaha in a flame-orange sari takes shape.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan carries us from the mother to the goddess she creates"),
 focus={"subject":"prakriti","depth":"deep"},vertical={"x":[580,700]},
 layers=[far_hills(xs=(520,800),col='#9ac4cc'),{"d":"mid","contents":"flowering trees and lotus-green shrubs of Prakriti's garden","fog":0.18,"items":[{"o":"tree","x":420,"y":605,"s":0.85,"kind":"round","col":"#3a9a4a","flowers":"#ff9ac0"},{"o":"tree","x":880,"y":610,"s":0.8,"kind":"round","col":"#3a9a4a","flowers":"#ffd040"},ground(640,665,640,50,'#b8e090')]},near_shrubs((440,880),'#2a6a3a')],
 background=earth_bg(sky=SKY_NATURE,sx=700,ridge=RIDGE_NATURE),mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"prakriti","x":570,"y":665,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.6},"look":"swaha",
   "actions":[{"word":"created","pose":"open","emo":"joy","d":0.6}]},
  {"who":"swaha","x":730,"y":665,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"prakriti","mood":{"smile":0.6},
   "engine_cues":{"ac":"created"},"engine":{"ad":0.8},
   "actions":[{"word":"goddess","pose":"namaste","emo":"devotion","d":0.6}]}],
 effects=[glow(730,360,240,"255,190,110",0.55,word="created",meaning="the warm light in which the young goddess appears"),
  glow(570,330,200,"160,230,130",0.4,meaning="Prakriti's green halo light"),name("Prakriti","Prakriti",600,115)],
 transition_in="fade"))
# 28 --------------------------------------------------------------- to carry offerings from earth to heaven (the path, fixed)
S.append(shot("s28",59.54,
 meaning="Swaha was made to carry the offerings from earth up to heaven.",
 why="The road of light again, now complete: Swaha rises up the column of light from the altar fire, arms raised, and the gold offering-motes she carries reach the shining gateway of Brahmaloka at the top.",
 camera=cam("crane_up",(1.06,0,14),(1.0,0,-6),"wide","wide",0,"rising with her from earth to heaven"),
 focus={"subject":"swaha","depth":"deep"},vertical={"x":[640,640]},
 layers=[{"d":"far","contents":"bright gold cloud banks of heaven across the top","fog":0.5,"haze":"#fff6e4","items":[{"o":"cloud","x":500,"y":130,"s":1.4,"col":"#fff8ec"},{"o":"cloud","x":790,"y":120,"s":1.3,"col":"#fff8ec"},{"o":"mountain","x":420,"y":540,"s":1.0,"w":220,"h":90,"col":"#9ab4d4","snow":False}]},
   {"d":"mid","contents":"a banyan and a flowering tree on earth beside the altar","fog":0.2,"items":[{"o":"tree","x":470,"y":640,"s":0.7,"kind":"banyan","col":"#2e7a44"},{"o":"tree","x":820,"y":640,"s":0.65,"kind":"round","col":"#3a8a4a","flowers":"#ff9ac0"},ground(640,690,600,50)]},
   near_shrubs((450,840))],
 background=earth_bg(sky=['#3a62d0','#8ab4f0','#ffd8a0','#fff4dc'],sx=640,sy=110),mood={"emotion":"fulfilment","grade":"warm"},
 characters=[{"who":"swaha","x":640,"y":520,"s":0.74,"_face":0.40,"flip":1,"pose":"raise","emo":"joy","look":640,"mood":{"ly":-0.6,"smile":0.7},
   "actions":[{"word":"carry","mood":{"smile":0.9,"ly":-0.8},"d":0.5}]}],
 effects=[beam(640,640,130,0.7),gate(640,95,130,1.0,0.6),kund(640,670,170),
  orbs([(620,600,640,95,"carry",1.0,True),(660,610,640,95,"offerings",1.0,True),(640,600,640,95,"offerings",1.4,True)],"carry","the offerings carried all the way up to heaven as gold motes"),
  glow(640,95,170,"255,230,150",0.7,word="offerings",meaning="the gate of heaven lighting up as the offerings arrive"),
  {"k":"halo_ring","word":"carry","x":640,"y":95,"w":240,"alpha":0.55,"blend":"lighter","par":0.6,"behind":True,"meaning":"heaven receiving the offering"}],
 transition_in="cut"))
# 29 --------------------------------------------------------------- Brahma asked her name
S.append(shot("s29",62.0,
 meaning="Brahma asked the young goddess her name.",
 why="Brahma on his lotus leans toward the right with an open, welcoming hand and a curious smile as he asks.",
 camera=cam("dolly_left",(1.1,10,0),(1.1,-8,0),"medium","normal",0,"a gentle drift toward the one he speaks to"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.1,"y":0.42},
 layers=[far_loka(xs=(520,780)),mid_pillars((460,820)),near_clouds((470,810))],
 background=loka_bg(sky=SKY_LOKA,sx=760),mood={"emotion":"curiosity","grade":"warm"},
 characters=[{"who":"brahma","x":620,"y":660,"s":1.05,"_face":0.44,"flip":1,"pose":"sit","emo":"joy","talk":0.6,"look":900,"mood":{"smile":0.5},
   "actions":[{"word":"asked","pose":"open","mood":{"smile":0.6,"surp":0.3},"tilt":0.05,"d":0.5}]}],
 effects=[glow(760,330,200,"255,200,120",0.35,meaning="warm light from the young goddess beside him")],
 transition_in="cut"))
# 30 --------------------------------------------------------------- "Swaha," she said
S.append(shot("s30",63.5,
 meaning="The goddess answered that her name was Swaha.",
 why="Close on Swaha: a gentle smile as she says her own name, her small fire halo glowing, and the name 'Swaha' appears above her.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"close","tele",0,"push in on the name the whole story is about"),
 focus={"subject":"swaha","depth":"shallow"},vertical={"focus":"swaha"},
 layers=[far_loka('#fbeee0','#fff6ea',(500,800)),mid_pillars((450,830)),near_clouds()],
 background=loka_bg(sky=SKY_WED),mood={"emotion":"grace","grade":"warm"},
 characters=[{"who":"swaha","x":640,"y":370,"s":1.15,"flip":-1,"head":True,"emo":"joy","talk":0.5,"mood":{"smile":0.6,"mouth":0.4},
   "actions":[{"word":"Swaha","mood":{"smile":0.7,"mouth":0.5,"ly":0.2},"tilt":0.04,"d":0.5}]}],
 effects=[name("Swaha","Swaha",640,118,32),glow(640,330,260,"255,180,90",0.45,meaning="Swaha's small fire halo glowing")],
 transition_in="cut"))
# 31 --------------------------------------------------------------- Brahma declared
S.append(shot("s31",65.16,
 meaning="Brahma declared that every offering to Agni must end with Swaha's name.",
 why="Brahma, standing between Agni and Swaha, raises his hand to proclaim the rule; Agni folds his hands on his name and Swaha on 'name', as a gold ring of light opens behind Brahma.",
 camera=cam("tilt_up",(1.0,0,14),(1.0,0,0),"medium","normal",0,"tilting up to the creator as he proclaims the law"),
 focus={"subject":"brahma","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_loka(xs=(500,800)),mid_pillars((430,850)),near_clouds((450,830))],
 background=loka_bg(sky=SKY_LOKA),mood={"emotion":"proclamation","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":665,"s":0.9,"_face":0.41,"flip":1,"pose":"stand","lotus":False,"emo":"calm","talk":0.6,"look":640,
   "actions":[{"word":"declared","pose":"raise","emo":"pride","d":0.6}]},
  {"who":"agni","x":515,"y":665,"s":0.78,"_ground":True,"flip":1,"pose":"stand","emo":"calm","look":"brahma",
   "actions":[{"word":"Agni","pose":"namaste","emo":"joy","d":0.6}]},
  {"who":"swaha","x":765,"y":665,"s":0.76,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"brahma",
   "actions":[{"word":"offering","pose":"namaste","emo":"devotion","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"declared","x":640,"y":330,"w":460,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the weight of Brahma's decree as a ring of gold light"}],
 transition_in="fade"))
# 32 --------------------------------------------------------------- without it the offering would not reach
S.append(shot("s32",69.24,
 meaning="Without the word Swaha an offering would not reach the gods.",
 why="On earth the village woman pours into the fire, but the motes rise only a little and thin into gray smoke; she looks up, doubtful.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"medium","normal",0,"pulling back on an offering that goes nowhere"),
 focus={"subject":"villager_w","depth":"deep"},vertical={"x":[620,640]},
 layers=[far_hills(xs=(520,800),haze='#eef0f4',col='#a8b4c8'),mid_village((440,860)),near_shrubs((460,830))],
 background=earth_bg(sky=SKY_GRAY,sx=700),mood={"emotion":"futility","grade":"cool"},
 characters=[{"who":"villager_w","x":580,"y":668,"s":1.0,"_face":0.43,"flip":1,"pose":"sitpray","emo":"calm","look":740,
   "actions":[{"word":"Without","pose":"open","d":0.5},{"word":"reach","emo":"doubt","mood":{"ly":-0.6},"d":0.6}]}],
 effects=[kund(730,660,180),{"k":"smoke_plume","x":730,"y":560,"w":160,"alpha":0.6,"par":1.0,"meaning":"the offering turning to gray smoke instead of rising to heaven"},
  orbs([(720,540,725,330,"Without",1.2),(740,540,735,320,"reach",1.2)],"Without","offering motes rising and fading out in the smoke")],
 transition_in="fade"))
# 33 --------------------------------------------------------------- a chant without Swaha
S.append(shot("s33",72.18,
 meaning="Brahma says a chant without the word Swaha would be empty.",
 why="Brahma stands with one finger raised as he speaks the comparison, his face stern and certain.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the teaching"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.1,"y":0.42},
 layers=[far_loka(xs=(520,780)),mid_pillars((460,820)),near_clouds((470,810))],
 background=loka_bg(sky=SKY_LOKA,sx=600),mood={"emotion":"teaching","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":665,"s":1.0,"_face":0.43,"flip":-1,"pose":"stand","lotus":False,"emo":"calm","talk":0.7,"look":420,
   "actions":[{"word":"chant","pose":"point","d":0.5},{"word":"Swaha","emo":"doubt","mood":{"ly":0.2},"d":0.6}]}],
 effects=[],
 transition_in="cut"))
# 34 --------------------------------------------------------------- a tree without fruit
S.append(shot("s34",74.06,
 meaning="Like a tree that bears no fruit.",
 why="A lone tree stands on a pale bare field: green leaves but not a single fruit or flower on it, under a quiet sky.",
 camera=cam("tilt_down",(1.0,0,-14),(1.0,0,0),"wide","wide",0,"tilting down the empty branches to the bare ground"),
 focus={"subject":"tree","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_hills(xs=(520,800),haze='#f0f0f0',col='#b0bccc'),
   {"d":"mid","contents":"one lone leafy tree with no fruit on a bare field","fog":0.12,"items":[{"o":"tree","x":640,"y":600,"s":1.4,"kind":"round","col":"#6a8a5a"},ground(640,650,640,60,'#d8d0b0')]},
   {"d":"near","contents":"dry grass tufts in the bottom corners","dark":0.4,"items":[{"o":"shrub","x":460,"y":748,"s":1.4,"col":"#6a6a4a"},{"o":"shrub","x":830,"y":750,"s":1.3,"col":"#6a6a4a"}]}],
 background=earth_bg(sky=SKY_GRAY,sx=640,sy=200),mood={"emotion":"barrenness","grade":"cool"},
 characters=[],
 effects=[{"k":"mist_wisps","x":640,"y":560,"w":520,"alpha":0.5,"par":1.0,"meaning":"a thin haze over the barren field"}],
 transition_in="cut"))
# 35 --------------------------------------------------------------- a snake without venom, a man without knowledge
S.append(shot("s35",75.44,
 meaning="Like a snake without venom, or a man without knowledge: each one missing the very thing that gives it power.",
 why="A village man stands with empty open hands and a lost, puzzled face; the gold light that should glow around his head is only a faint ring.",
 camera=cam("dolly_left",(1.06,10,0),(1.06,-10,0),"medium","normal",0,"a slow drift around a man without what makes him whole"),
 focus={"subject":"villager","depth":"deep"},vertical={"focus":"villager","z":1.1,"y":0.42},
 layers=[far_hills(xs=(520,800),haze='#f0f0f0',col='#b0bccc'),mid_village((440,860)),near_shrubs((460,830),'#4a5a3a')],
 background=earth_bg(sky=SKY_GRAY,sx=640),mood={"emotion":"emptiness","grade":"cool"},
 characters=[{"who":"villager","x":640,"y":665,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"doubt","look":640,
   "actions":[{"word":"venom","pose":"open","emo":"doubt","d":0.5},{"word":"knowledge","emo":"sad","mood":{"ly":0.4},"tilt":-0.05,"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"man","x":640,"y":340,"w":300,"alpha":0.2,"blend":"lighter","par":0.9,"behind":True,"meaning":"a faint empty ring where knowledge should shine"}],
 transition_in="fade"))
# 36 --------------------------------------------------------------- the marriage
S.append(shot("s36",78.78,
 meaning="Then Brahma gave Swaha in marriage to Agni.",
 why="Agni and Swaha face each other with folded hands inside a ring of marigold light, while Brahma, faint behind them, raises his hand in blessing.",
 camera=cam("push_in",(1.0,0,0),(1.05,0,-4),"two_shot","normal",0,"push in on the vow"),
 focus={"subject":"agni","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_loka('#fbeee0','#fff6ea',(500,800)),mid_pillars((430,850)),near_clouds((450,830))],
 background=loka_bg(sky=SKY_WED),mood={"emotion":"marriage","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":520,"s":0.55,"_face":0.30,"flip":1,"pose":"stand","lotus":False,"emo":"joy","look":640,"engine":{"a":0.55},
   "actions":[{"word":"gave","pose":"raise","d":0.6}]},
  {"who":"agni","x":565,"y":665,"s":0.98,"_face":0.44,"flip":1,"pose":"stand","emo":"joy","look":"swaha",
   "actions":[{"word":"marriage","pose":"namaste","emo":"joy","mood":{"smile":0.9},"d":0.6}]},
  {"who":"swaha","x":720,"y":665,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"agni","mood":{"smile":0.7,"ly":0.3},
   "actions":[{"word":"Swaha","pose":"namaste","emo":"joy","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"marriage","x":645,"y":360,"w":520,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the sacred ring of the marriage vow"},
  glow(645,400,260,"255,200,110",0.45,word="Swaha",meaning="marigold light of the wedding")],
 transition_in="fade"))
# 37 --------------------------------------------------------------- never parted
S.append(shot("s37",81.12,
 meaning="Agni and Swaha were never parted again.",
 why="Agni and Swaha stand side by side, their two fire halos merged into one warm glow, as light motes rise around them and the camera pulls away.",
 camera=cam("pull_out",(1.1,0,-6),(1.0,0,0),"two_shot","wide",0,"final pull out: the pair together for ever"),
 focus={"subject":"agni","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_loka('#fbeee0','#fff6ea',(500,800)),mid_pillars((430,850)),near_clouds((450,830))],
 background=loka_bg(sky=SKY_WED,sy=230),mood={"emotion":"union","grade":"warm"},
 characters=[{"who":"agni","x":590,"y":665,"s":0.98,"_face":0.43,"flip":1,"pose":"stand","emo":"joy","look":"swaha","mood":{"smile":0.8},
   "actions":[{"word":"two","mood":{"smile":1},"d":0.6}]},
  {"who":"swaha","x":695,"y":665,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"agni","mood":{"smile":0.8},
   "actions":[{"word":"never","mood":{"smile":1,"blink":0.3},"tilt":0.04,"d":0.6}]}],
 effects=[glow(642,340,300,"255,170,80",0.55,meaning="their two fires burning as one"),
  orbs([(560,560,540,220,"and",2.0),(720,560,740,230,"two",2.0),(640,580,650,200,"never",2.0)],"and","warm light motes rising around the joined pair")],
 transition_in="cut"))
# ---------------------------------------------------------------- durations / narration from the next start
for i,s in enumerate(S):
    end=S[i+1]['start']['t'] if i+1<len(S) else END
    s['duration']=round(end-s['start']['t'],2)
    i0=idx(s['start']['t']);i1=idx(S[i+1]['start']['t']) if i+1<len(S) else len(T);s['narration']=span(i0,i1)
sys.path.insert(0,R+'/studio');import validate_brief as VB
def ease(k):return k*k*(3-2*k)
def face_frac(f,s,u=.55):
    c=s['camera'];A=c['from'];B=c['to'];e=ease(u)
    z=A.get('z',1)+(B.get('z',1)-A.get('z',1))*e;cy=A.get('y',0)+(B.get('y',0)-A.get('y',0))*e
    fc=f['y'] if f.get('head') else f['y']-(195 if VB.seated(f) else 300)*f['s']
    sy=360+(fc-360-cy)*z;V=s.get('vertical') or {};vz=min(max(V.get('z',1),1),2.2);h=720/vz
    w0=min(max(sy-V.get('y',.36)*h,0),720-h) if vz>1 else 0
    return (sy-w0)/h
for s in S:
    if (s.get('vertical') or {}).get('mode')=='stack':continue
    g=None
    for f in sorted(s['characters'],key=lambda f:bool(f.get('_ground'))):   # faces first, then figures that stand on the first placed figure's ground
        if f.get('head'):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        tgt=f.pop('_face',.42)
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None and not f.get('engine',{}).get('a'):g=f['y']
for s in S:
    for f in s['characters']:f.pop('_face',None);f.pop('_ground',None)
for s in S:
    cam_={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        y0=f['y']
        while VB.face_cropped_v(f,cam_,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
# orbs: each light mote starts on the cue index of its word (same cue order as studio/brief_to_plan.py)
import brief_to_plan as BP
for s in S:
    for e in s['effects']:
        if e.get('k')!='orbs':continue
        cues=BP.convert(s,True)['cues']
        for it in e['items']:
            w=VB.norm(it.pop('_w'))
            if w not in cues:raise SystemExit(f"{s['id']}: orb word {w} is not a cue word {cues}")
            it['c']=cues.index(w)
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel06","format":"vertical","shots":S},open(f'{R}/reels/reel06/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
