#!/usr/bin/env python3
"""Generator for reels/reel05/briefs.json "Shiva Born From Anger" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel04/briefs_gen.py: every face solved to 38-50% of the 9:16 frame height, narration = the spoken words.
Extra key `_fix`: keep the given y (crowds placed by hand)."""
import json,os
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel05/words.json'))
T=[(w['w'],w['start']) for w in W]
END=89.0
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette (bright, clean; fire stays bright gold-orange, never dark) ----------
SKY_BRAHMA=['#2456b4','#74aaea','#ffe2b4','#fff7e6']        # Brahmaloka: blue-gold
SKY_KUM=['#3a52b8','#8aa4ec','#f4dcf0','#fff6ee']           # the Kumaras: soft blue-rose
SKY_INF=['#3a3aa8','#8a7ae0','#f0d4f4','#fff4e6']           # the infinite: violet-gold
SKY_FIRE=['#d84a24','#f4843a','#ffc46a','#fff2d0']          # anger / fire, bright
SKY_FIRE2=['#c83c2a','#f07a40','#ffb860','#ffeccc']
SKY_SHIVA=['#2a4aa8','#7a9ae8','#d8e4fa','#f6f8ff']         # Shiva / Mahadev: blue-white
SKY_VISH=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']
SKY_DUSK=['#4a3aa0','#9a6ad0','#f4a8a0','#ffe8cc']          # destroyer: violet-rose, still bright
SKY_SNOW=['#2a6ad0','#7ab8f0','#dcecfa','#f8fbff']          # the Himalaya by day
RIDGE_SNOW=['#c8daf0','#a8c0e0','#8aa4cc','#7088b4']
RIDGE_WORLD=['#a8c4e4','#8ab4cc','#6aa08a','#4a8064']
def far_clouds(haze='#eef2fa',col='#ffffff',xs=(520,780),mcol='#9aaad8'):
    return {"d":"far","contents":"soft cloud banks and two hazy peaks of Brahmaloka far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-60,"y":500,"s":1.0,"col":mcol},{"o":"mountain","x":xs[1]+40,"y":510,"s":0.85,"col":mcol},
                     {"o":"cloud","x":xs[0],"y":230,"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":270,"s":1.1,"col":col}]}
def far_fire(xs=(520,780)):
    return far_clouds('#fff0dc','#fff4e0',xs,'#e8a888')
def mid_pillars(xs=(450,830),col='#ecc878',h=520):
    return {"d":"mid","contents":"two gold pillars of Brahma's hall","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810),col='#ffffff'):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":col},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":col}]}
def far_snow(xs=(500,800)):
    return {"d":"far","contents":"white snow peaks of the Himalaya in blue haze","fog":0.5,"haze":"#eef4fc",
            "items":[{"o":"mountain","x":xs[0],"y":470,"s":1.2,"col":"#b8c8e4"},{"o":"mountain","x":xs[1],"y":480,"s":1.0,"col":"#b8c8e4"},
                     {"o":"cloud","x":xs[0]+60,"y":230,"s":1.0,"col":"#ffffff"}]}
def mid_pines(xs=(450,840)):
    return {"d":"mid","contents":"deodar pines and snowy rocks on the slope","fog":0.2,
            "items":[{"o":"tree","x":xs[0],"y":610,"s":0.8,"kind":"pine","col":"#2a6a5a"},{"o":"tree","x":xs[1],"y":615,"s":0.75,"kind":"pine","col":"#2a6a5a"},
                     {"o":"rock","x":xs[0]+70,"y":650,"s":1.0,"col":"#dce4f2"},{"o":"rock","x":xs[1]-80,"y":655,"s":0.9,"col":"#dce4f2"}]}
def near_snow(xs=(450,830)):
    return {"d":"near","contents":"blurred snowy rocks in the bottom corners","dark":0.3,
            "items":[{"o":"rock","x":xs[0],"y":752,"s":1.6,"col":"#c8d4ec"},{"o":"rock","x":xs[1],"y":755,"s":1.5,"col":"#c8d4ec"}]}
def cloud_bg(sky=SKY_BRAHMA,sx=640,sy=200,**k):
    d={"k":"cloudscape","sky":sky,"sx":sx,"sy":sy};d.update(k);return d
def snow_bg(sx=700,sy=220):
    return {"k":"vista","sky":SKY_SNOW,"sx":sx,"sy":sy,"ridge":RIDGE_SNOW,"haze":"240,246,255"}
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!"')}};s.update(k);return s
def cam(move,a,b,shot_='medium',lens='normal',shake=0,mot=''):
    z0,x0,y0=a;z1,x1,y1=b
    return {"shot":shot_,"lens":lens,"move":move,"from":{"z":z0,"x":x0,"y":y0,"r":0},"to":{"z":z1,"x":x1,"y":y1,"r":0},"shake":shake,"motivation":mot}
def name(word,s,x=640,y=120,size=32,m=''):
    return {"k":"name","word":word,"s":s,"x":x,"y":y,"size":size,"meaning":m or f"the name {s} on screen as it is said"}
S=[]
# 1 ---------------------------------------------------------------- title: the god born from anger
S.append(shot("s01",0.18,
 meaning="Shiva was born out of another god's anger.",
 why="Below the title card the newborn Rudra stands in a bright gold-orange sky with his fire halo; on 'anger' his eyes blaze red and a warm glow flares behind him.",
 camera=cam("push_in",(1.0,0,0),(1.05,0,-6),"medium","normal",0,"slow push in on the god whose birth the reel tells"),
 focus={"subject":"rudra","depth":"deep"},vertical={"focus":"rudra"},
 layers=[far_fire(),mid_pillars(col='#f4c890'),near_clouds(col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sy=190),mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":690,"s":1.0,"_face":0.52,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"anger","emo":"anger","d":0.6}]}],
 effects=[{"k":"glow","word":"anger","x":640,"y":330,"r":260,"rgb":"255,150,70","ga":0.5,"par":1.0,"behind":True,"meaning":"the anger he was born from, a fire-orange light behind him"}],
 transition_in="fade"))
# 2 ---------------------------------------------------------------- not power
S.append(shot("s02",3.04,
 meaning="His first demand was not for power.",
 why="Rudra raises his hand on 'demand' but turns his blazing eyes away from a gold crown that glows faintly beside him: power is not what he wants.",
 camera=cam("dolly_left",(1.05,10,0),(1.05,-10,0),"medium","normal",0,"a sideways drift past the crown he ignores"),
 focus={"subject":"rudra","depth":"deep"},vertical={"x":610,"z":1.08,"y":0.42},
 layers=[far_fire(),mid_pillars((450,830),col='#f4c890'),near_clouds(col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sx=700),mood={"emotion":"demand","grade":"warm"},
 characters=[{"who":"rudra","x":680,"y":690,"s":1.0,"_face":0.42,"flip":-1,"pose":"stand","emo":"anger","talk":0.6,"look":800,
   "actions":[{"word":"demand","pose":"raise","emo":"anger","e":"spring","d":0.5},{"word":"power","mood":{"lx":0.6,"anger":0.7},"d":0.5}]}],
 effects=[{"k":"crown_gold","word":"first","x":505,"y":215,"w":80,"alpha":0.6,"par":1.0,"meaning":"power: a gold crown he does not even look at"}],
 transition_in="cut"))
# 3 ---------------------------------------------------------------- a name
S.append(shot("s03",5.36,
 meaning="What he demanded was a name.",
 why="Close on Rudra's face: red eyes, mouth open as he demands; an empty name plate with a question mark appears above him on 'name'.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness on the single thing he wants"),
 focus={"subject":"rudra","depth":"shallow"},vertical={"focus":"rudra"},
 layers=[far_fire(xs=(500,800)),mid_pillars((450,830),col='#f4c890')],
 background=cloud_bg(SKY_FIRE2),mood={"emotion":"demand","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":370,"s":1.1,"flip":1,"head":True,"emo":"anger","talk":0.7,"look":640,
   "actions":[{"word":"name","mood":{"anger":0.8,"mouth":0.5,"ly":-0.2},"d":0.4}]}],
 effects=[name("was","?",640,95,40,"the name he does not have yet, an empty plate with a question mark")],
 transition_in="cut"))
# 4 ---------------------------------------------------------------- Brahma, the creator
S.append(shot("s04",6.76,
 meaning="Brahma is the creator god.",
 why="Brahma sits on his pink lotus in his bright blue-gold hall, soft rays fall on him and his name plate appears as he is named.",
 camera=cam("crane_down",(1.0,0,-20),(1.0,0,0),"establishing","wide",0,"descending to the creator on his lotus"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(),mood={"emotion":"majesty","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.47,"flip":1,"pose":"sit","emo":"calm","look":640,"mood":{"smile":0.4},
   "actions":[{"word":"creator","mood":{"smile":0.6,"ly":-0.2},"tilt":0.03,"d":0.6}]}],
 effects=[{"k":"divine_rays","x":640,"y":80,"w":700,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of the creator's world"},
  name("Brahma","Brahma",640,130,32)],
 transition_in="fade"))
# 5 ---------------------------------------------------------------- four sons from his mind
S.append(shot("s05",8.46,
 meaning="Brahma had created four sons out of his mind.",
 why="A ring of light opens around Brahma's head on 'mind' and four small child sages fade in at the foot of his lotus, two on 'four', two on 'sons'.",
 camera=cam("push_in",(1.0,0,0),(1.04,0,-4),"medium","normal",0,"push in as the sons appear"),
 focus={"subject":"brahma","depth":"deep"},vertical={"x":640},
 layers=[far_clouds(),mid_pillars(),near_clouds((460,820))],
 background=cloud_bg(),mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":0.78,"_face":0.37,"flip":1,"pose":"sit","emo":"joy","look":640,"mood":{"smile":0.6,"ly":0.5},
   "actions":[{"word":"mind","mood":{"smile":0.8,"ly":0.6},"tilt":0.04,"d":0.6}]},
  {"who":"kumara","x":492,"y":690,"s":0.5,"_face":0.53,"flip":1,"pose":"namaste","emo":"joy","look":"brahma","engine_cues":{"ac":"four"},"engine":{"ad":0.6}},
  {"who":"kumara","x":566,"y":690,"s":0.52,"_face":0.54,"flip":1,"pose":"stand","emo":"joy","look":"brahma","engine_cues":{"ac":"four"},"engine":{"ad":0.6}},
  {"who":"kumara","x":714,"y":690,"s":0.52,"_face":0.54,"flip":-1,"pose":"stand","emo":"joy","look":"brahma","engine_cues":{"ac":"sons"},"engine":{"ad":0.6}},
  {"who":"kumara","x":788,"y":690,"s":0.5,"_face":0.53,"flip":-1,"pose":"namaste","emo":"joy","look":"brahma","engine_cues":{"ac":"sons"},"engine":{"ad":0.6}}],
 effects=[{"k":"halo_ring","word":"mind","x":640,"y":0,"_head":0,"w":300,"alpha":0.5,"blend":"lighter","par":1.0,"behind":True,"meaning":"the sons born from Brahma's mind, a ring of light around his head"},
  {"k":"glow","word":"four","x":640,"y":0,"_feet":1,"r":260,"rgb":"255,230,170","ga":0.45,"par":1.0,"behind":True,"meaning":"the light the four sons appear in"}],
 transition_in="cut"))
# 6 ---------------------------------------------------------------- child sages, the Kumaras
S.append(shot("s06",10.76,
 meaning="The four sons were child sages called the Kumaras.",
 why="The four boy sages stand in a row on the clouds with folded hands and ash marks, calm and young; their name appears on 'Kumaras'.",
 camera=cam("dolly_right",(1.0,-8,0),(1.0,8,0),"wide","normal",0,"a slow drift along the row of four"),
 focus={"subject":"kumara","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#f4eef8','#ffffff',(520,780)),mid_pillars((440,840)),near_clouds((460,820))],
 background=cloud_bg(SKY_KUM),mood={"emotion":"innocence","grade":"warm"},
 characters=[{"who":"kumara","x":500,"y":690,"s":0.8,"_face":0.43,"flip":1,"pose":"namaste","emo":"calm","look":640,"actions":[{"word":"sages","mood":{"smile":0.5},"d":0.6}]},
  {"who":"kumara","x":593,"y":690,"s":0.84,"_face":0.44,"flip":1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"child","mood":{"smile":0.7},"d":0.6}]},
  {"who":"kumara","x":687,"y":690,"s":0.84,"_face":0.44,"flip":-1,"pose":"namaste","emo":"calm","look":640,"actions":[{"word":"Kumaras","mood":{"smile":0.5},"tilt":0.04,"d":0.6}]},
  {"who":"kumara","x":780,"y":690,"s":0.8,"_face":0.43,"flip":-1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"Kumaras","mood":{"smile":0.7},"d":0.6}]}],
 effects=[{"k":"glow","x":640,"y":330,"r":280,"rgb":"255,236,200","ga":0.4,"par":1.0,"behind":True,"meaning":"the soft light of the boy sages"},
  name("called","Kumaras",640,130,32)],
 transition_in="cut"))
# 7 ---------------------------------------------------------------- fill the world
S.append(shot("s07",13.34,
 meaning="Brahma told the Kumaras to help him fill the world with living beings.",
 why="Brahma on his lotus talks with open hands; on 'world' the clouds below him cross-fade to a green valley with a river, the empty world he wants filled.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"medium","wide",0,"pulling back to show the world below"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[{"d":"far","contents":"hazy blue hills and white clouds over the world","fog":0.55,"haze":"#eef4fa","items":[{"o":"mountain","x":500,"y":470,"s":1.0,"col":"#9ab4d4","snow":False},{"o":"mountain","x":800,"y":480,"s":0.9,"col":"#9ab4d4","snow":False},{"o":"cloud","x":560,"y":220,"s":1.2,"col":"#ffffff"}]},
   {"d":"mid","contents":"trees of the green world below","fog":0.25,"items":[{"o":"tree","x":450,"y":640,"s":0.7,"kind":"banyan","col":"#3a8a4a"},{"o":"tree","x":840,"y":640,"s":0.7,"kind":"round","col":"#3a8a4a"}]},near_clouds()],
 background={**cloud_bg(),"change":{"word":"world","bg2":{"k":"vista","sky":SKY_BRAHMA,"sx":640,"sy":220,"ridge":RIDGE_WORLD,"river":"#5ab8e8","haze":"240,246,255"},"d":1.0}},
 mood={"emotion":"command","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":0.95,"_face":0.42,"flip":1,"emo":"calm","talk":0.7,"look":640,
   "actions":[{"word":"help","pose":"open","emo":"joy","d":0.6},{"word":"living","mood":{"smile":0.7,"ly":0.5},"d":0.6}]}],
 effects=[{"k":"glow","word":"living","x":640,"y":560,"r":260,"rgb":"200,255,190","ga":0.4,"par":1.0,"behind":True,"meaning":"the life he wants spread over the world, a green-gold light"}],
 transition_in="cut"))
# 8 ---------------------------------------------------------------- folded hands, said no
S.append(shot("s08",16.66,
 meaning="The Kumaras folded their hands and refused.",
 why="Two Kumaras in front and two behind fold their hands on 'folded'; on 'no' they gently turn their heads aside, polite but firm.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"two_shot","normal",0,"push in on the polite refusal"),
 focus={"subject":"kumara","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#f4eef8','#ffffff',(520,780)),mid_pillars((440,840)),near_clouds((460,820))],
 background=cloud_bg(SKY_KUM,sx=600),mood={"emotion":"refusal","grade":"warm"},
 characters=[{"who":"kumara","x":495,"y":660,"s":0.72,"_face":0.38,"flip":1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"folded","pose":"namaste","d":0.6},{"word":"no","mood":{"turn":-0.4,"lx":-0.5},"d":0.5}]},
  {"who":"kumara","x":785,"y":660,"s":0.72,"_face":0.38,"flip":-1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"folded","pose":"namaste","d":0.6},{"word":"no","mood":{"turn":0.4,"lx":0.5},"d":0.5}]},
  {"who":"kumara","x":575,"y":690,"s":0.95,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","look":900,"actions":[{"word":"folded","pose":"namaste","e":"spring","d":0.6},{"word":"no","mood":{"turn":-0.5,"lx":-0.6},"tilt":-0.05,"d":0.5}]},
  {"who":"kumara","x":705,"y":690,"s":0.95,"_face":0.45,"flip":-1,"pose":"stand","emo":"calm","look":380,"actions":[{"word":"folded","pose":"namaste","e":"spring","d":0.6},{"word":"no","mood":{"turn":0.5,"lx":0.6},"tilt":0.05,"d":0.5}]}],
 effects=[],transition_in="cut"))
# 9 ---------------------------------------------------------------- grateful
S.append(shot("s09",19.06,
 meaning="The Kumaras said they were grateful.",
 why="Close on one boy sage: a warm smile and a small bow of the head on 'grateful', a soft gold glow behind him.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness for a gentle word"),
 focus={"subject":"kumara","depth":"shallow"},vertical={"focus":"kumara"},
 layers=[far_clouds('#f4eef8','#ffffff',(500,800)),mid_pillars((450,830))],
 background=cloud_bg(SKY_KUM),mood={"emotion":"gratitude","grade":"warm"},
 characters=[{"who":"kumara","x":640,"y":360,"s":1.15,"flip":1,"head":True,"emo":"devotion","talk":0.6,"look":900,"mood":{"smile":0.6},
   "actions":[{"word":"grateful","emo":"joy","mood":{"smile":0.9,"blink":0.4,"ly":0.3},"tilt":0.06,"d":0.6}]}],
 effects=[{"k":"glow","word":"grateful","x":640,"y":330,"r":240,"rgb":"255,225,160","ga":0.45,"par":1.0,"behind":True,"meaning":"his gratitude as a warm light"}],
 transition_in="cut"))
# 10 --------------------------------------------------------------- not bound by life and death
S.append(shot("s10",20.28,
 meaning="They did not want to be bound by the cycle of life and death.",
 why="Two Kumaras step back with open hands while a gold wheel, the round of birth and death, turns in the sky above them on 'life'; they look away from it.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"a drift away, like their step back from the wheel"),
 focus={"subject":"kumara","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#ece8f8','#ffffff',(520,780)),mid_pillars((440,840)),near_clouds((460,820))],
 background=cloud_bg(SKY_KUM,sx=640,sy=180),mood={"emotion":"detachment","grade":"cool"},
 characters=[{"who":"kumara","x":565,"y":690,"s":0.95,"_face":0.47,"flip":1,"pose":"stand","emo":"calm","look":900,
   "actions":[{"word":"want","emo":"doubt","d":0.6},{"word":"bound","pose":"open","mood":{"ly":-0.5,"lx":0.3},"d":0.6}]},
  {"who":"kumara","x":715,"y":690,"s":0.95,"_face":0.47,"flip":-1,"pose":"stand","emo":"calm","look":380,
   "actions":[{"word":"want","emo":"doubt","d":0.6},{"word":"bound","pose":"open","mood":{"ly":-0.5,"lx":-0.3},"d":0.6}]}],
 effects=[{"k":"icon","i":"cycle","word":"want","x":640,"y":150,"sc":1.3,"par":1.0,"behind":True,"meaning":"the round of birth and death they refuse, a turning gold wheel"}],
 transition_in="cut"))
# 11 --------------------------------------------------------------- meditate on the infinite
S.append(shot("s11",23.44,
 meaning="They wanted to meditate on the infinite.",
 why="The four Kumaras sit cross-legged with closed eyes in a violet-gold sky; on 'infinite' a glowing infinity sign opens above them.",
 camera=cam("crane_up",(1.04,0,10),(1.0,0,-6),"wide","wide",0,"rising toward the infinite they meditate on"),
 focus={"subject":"kumara","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#f0e8fa','#fbf6ff',(520,780),'#a8a0d8'),{"d":"mid","contents":"low cloud banks behind the seated sages","fog":0.25,"items":[{"o":"cloud","x":470,"y":560,"s":1.1,"col":"#ffffff"},{"o":"cloud","x":820,"y":570,"s":1.0,"col":"#ffffff"}]},near_clouds((460,820))],
 background=cloud_bg(SKY_INF,sy=170),mood={"emotion":"meditation","grade":"cool"},
 characters=[{"who":"kumara","x":500,"y":640,"s":0.66,"_face":0.44,"flip":1,"pose":"sitpray","emo":"calm","mood":{"blink":1},"look":640},
  {"who":"kumara","x":780,"y":640,"s":0.66,"_face":0.44,"flip":-1,"pose":"sitpray","emo":"calm","mood":{"blink":1},"look":640},
  {"who":"kumara","x":580,"y":690,"s":0.8,"_face":0.5,"flip":1,"pose":"sitpray","emo":"calm","mood":{"blink":1},"look":640,"actions":[{"word":"meditate","mood":{"blink":1,"smile":0.4},"d":0.6}]},
  {"who":"kumara","x":700,"y":690,"s":0.8,"_face":0.5,"flip":-1,"pose":"sitpray","emo":"calm","mood":{"blink":1},"look":640,"actions":[{"word":"meditate","mood":{"blink":1,"smile":0.4},"d":0.6}]}],
 effects=[{"k":"infinity","word":"meditate","x":640,"y":150,"par":1.0,"behind":True,"meaning":"the infinite, a glowing infinity sign above them"}],
 transition_in="fade"))
# 12 --------------------------------------------------------------- never grow old
S.append(shot("s12",25.92,
 meaning="Their only wish was never to grow old.",
 why="One Kumara asks with open pleading hands on 'asked', then folds them; a pale ring of light opens behind his young face on 'never', the youth he keeps for ever.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on his one wish"),
 focus={"subject":"kumara","depth":"deep"},vertical={"focus":"kumara","z":1.1,"y":0.42},
 layers=[far_clouds('#f4eef8','#ffffff',(520,780)),mid_pillars((450,830)),near_clouds()],
 background=cloud_bg(SKY_KUM,sx=700),mood={"emotion":"wish","grade":"warm"},
 characters=[{"who":"kumara","x":640,"y":690,"s":1.05,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":540,"mood":{"smile":0.5},
   "actions":[{"word":"asked","pose":"plead","emo":"devotion","d":0.6},{"word":"old","pose":"namaste","emo":"joy","mood":{"smile":0.8},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"never","x":640,"y":0,"_head":0,"w":260,"alpha":0.45,"blend":"lighter","par":1.0,"behind":True,"meaning":"eternal youth, a pale ring of light behind his young face"}],
 transition_in="cut"))
# 13 --------------------------------------------------------------- Brahma argued, gave in
S.append(shot("s13",28.78,
 meaning="Brahma argued with them, then gave in.",
 why="Brahma on his lotus points and argues with a frown on 'argued'; on 'gave' his hands open and his eyes drop, giving in.",
 camera=cam("tilt_down",(1.04,0,-14),(1.04,0,0),"medium","normal",0,"tilting down as his argument sinks"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(sx=700),mood={"emotion":"frustration","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.44,"flip":1,"emo":"calm","talk":0.7,"look":800,
   "actions":[{"word":"argued","pose":"point","emo":"anger","e":"antic","d":0.5},{"word":"gave","pose":"open","emo":"sad","mood":{"ly":0.6},"tilt":-0.05,"d":0.7}]}],
 effects=[],transition_in="cut"))
# 14 --------------------------------------------------------------- his sons left
S.append(shot("s14",31.1,
 meaning="Brahma's sons walked away from him.",
 why="The window follows the four Kumaras walking off over the clouds to the right and fading, while Brahma at the left edge watches them go.",
 camera=cam("pan_right",(1.0,0,0),(1.0,0,0),"wide","wide",0,"the pan follows the sons leaving"),
 focus={"subject":"kumara","depth":"deep"},vertical={"x":[600,720]},
 layers=[far_clouds(xs=(560,820)),{"d":"mid","contents":"cloud banks along the path they walk","fog":0.25,"items":[{"o":"cloud","x":560,"y":560,"s":1.0,"col":"#ffffff"},{"o":"cloud","x":880,"y":570,"s":1.0,"col":"#ffffff"}]},near_clouds((460,860))],
 background=cloud_bg(sx=760),mood={"emotion":"parting","grade":"warm"},
 characters=[{"who":"brahma","x":470,"y":690,"s":0.85,"_face":0.47,"flip":1,"emo":"sad","look":800,"actions":[{"word":"left","mood":{"ly":0.2},"d":0.6}]},
  {"who":"kumara","x":610,"y":690,"s":0.66,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"sons","to_x":740,"d":1.4,"speed":1},"engine_cues":{"fo":"left"},"engine":{"fd":0.9}},
  {"who":"kumara","x":680,"y":690,"s":0.62,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"sons","to_x":810,"d":1.4,"speed":1},"engine_cues":{"fo":"left"},"engine":{"fd":0.9}},
  {"who":"kumara","x":750,"y":690,"s":0.66,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"sons","to_x":880,"d":1.4,"speed":1},"engine_cues":{"fo":"left"},"engine":{"fd":0.9}},
  {"who":"kumara","x":820,"y":690,"s":0.62,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"sons","to_x":950,"d":1.4,"speed":1},"engine_cues":{"fo":"left"},"engine":{"fd":0.9}}],
 effects=[],transition_in="cut"))
# 15 --------------------------------------------------------------- rage rose in him
S.append(shot("s15",32.4,
 meaning="Rage rose inside Brahma.",
 why="Close on Brahma's faces: brows crush down and his eyes turn red on 'rage' as the sky behind him floods bright fire-orange and a red pulse throbs.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,0),"close","tele",0,"push in on the rising anger"),
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma"},
 layers=[far_clouds(xs=(500,800)),mid_pillars((450,830))],
 background={**cloud_bg(),"change":{"word":"rage","bg2":cloud_bg(SKY_FIRE),"d":0.8}},
 mood={"emotion":"rage","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":360,"s":1.1,"flip":1,"head":True,"emo":"anger","look":640,
   "actions":[{"word":"rose","emo":"rage","e":"antic","d":0.4}]}],
 effects=[{"k":"red_energy_pulse","word":"rose","x":640,"y":330,"w":420,"alpha":0.55,"blend":"lighter","par":1.0,"behind":True,"meaning":"the rage rising in him, a throbbing red-orange light"}],
 transition_in="cut"))
# 16 --------------------------------------------------------------- a fiery being bursts from the forehead
S.append(shot("s16",33.92,
 meaning="A fiery being burst out of Brahma's forehead.",
 why="Brahma on his lotus with angry red eyes; on 'fiery' his forehead glows, then flames and a white-gold column of fire shoot up from it and a small figure with a fire halo rises in the column.",
 camera=cam("handheld",(1.0,0,0),(1.03,0,-6),"medium","normal",3,"the frame trembles with the burst"),
 focus={"subject":"brahma","depth":"deep"},vertical={"x":640},
 layers=[far_fire(),mid_pillars(col='#f4c890'),near_clouds(col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sy=170),mood={"emotion":"eruption","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":330,"s":0.42,"_fix":1,"flip":1,"pose":"raise","emo":"rage","look":640,"engine_cues":{"ac":"being","mc":"being"},"engine":{"ad":0.5,"my":-30,"md":2.0}},
  {"who":"brahma","x":640,"y":690,"s":0.9,"_face":0.52,"flip":1,"pose":"sit","emo":"rage","look":640,
   "actions":[{"word":"burst","emo":"surprise","mood":{"ly":-0.8},"d":0.4}]}],
 effects=[{"k":"glow","word":"fiery","x":640,"y":0,"_fore":1,"r":110,"rgb":"255,210,130","ga":0.85,"par":1.0,"meaning":"his forehead glowing with fire"},
  {"k":"beam","word":"being","x":640,"y":0,"_fore":1,"len":520,"w":55,"par":1.0,"behind":True,"meaning":"the column of fire bursting from his forehead"},
  {"k":"flames","word":"being","x":640,"y":0,"_fore":1,"sc":0.55,"n":7,"par":1.0,"meaning":"flames leaping from his forehead"}],
 transition_in="cut"))
# 17 --------------------------------------------------------------- stepped out with blazing red eyes
S.append(shot("s17",36.64,
 meaning="A being stepped out of the fire with blazing red eyes.",
 why="Rudra walks forward out of the column of fire, his fire halo burning behind him; on 'blazing' his eyes flare red.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in as he comes toward us"),
 focus={"subject":"rudra","depth":"deep"},vertical={"focus":"rudra","z":1.08,"y":0.42},
 layers=[far_fire(),mid_pillars(col='#f4c890'),near_clouds(col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sy=180),mood={"emotion":"birth","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":690,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"mc":"stepped"},"engine":{"my":14,"md":1.4},
   "actions":[{"word":"stepped","mood":{"ly":0.2},"e":"spring","d":0.6},{"word":"out","emo":"rage","d":0.5}]}],
 effects=[{"k":"beam","x":640,"y":700,"len":720,"w":70,"par":1.0,"behind":True,"meaning":"the column of fire he steps out of"},
  {"k":"glow","word":"red","x":640,"y":0,"_head":0,"r":160,"rgb":"255,90,60","ga":0.45,"par":1.0,"behind":True,"meaning":"the red blaze of his eyes"}],
 transition_in="cut"))
# 18 --------------------------------------------------------------- What is my name?
S.append(shot("s18",39.52,
 meaning="He roared: What is my name?",
 why="Close on Rudra roaring, mouth wide and eyes red; rings of fire-orange sound burst out from him on 'roared' and the frame shakes.",
 camera=cam("handheld",(1.0,0,0),(1.05,0,0),"close","tele",4,"the roar shakes the frame"),
 focus={"subject":"rudra","depth":"shallow"},vertical={"focus":"rudra"},
 layers=[far_fire(xs=(500,800)),mid_pillars((450,830),col='#f4c890')],
 background=cloud_bg(SKY_FIRE2,sy=170),mood={"emotion":"rage","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":360,"s":1.1,"flip":1,"head":True,"emo":"rage","mood":{"anger":1,"mouth":0.9},"talk":0.9,"look":640,
   "actions":[{"word":"roared","mood":{"anger":1,"mouth":0.8},"e":"antic","d":0.4},{"word":"name","mood":{"anger":1,"mouth":0.6,"ly":-0.2},"tilt":0.05,"d":0.5}]}],
 effects=[{"k":"shock","word":"roared","x":640,"y":380,"rgb":"255,150,80","max":700,"meaning":"the roar going out in rings"}],
 transition_in="cut"))
# 19 --------------------------------------------------------------- Brahma in awe
S.append(shot("s19",42.04,
 meaning="Brahma sat in awe of the being.",
 why="Brahma on his lotus stares up with wide eyes and parted lips, still and amazed, the orange firelight of Rudra falling on him from above.",
 camera=cam("tilt_up",(1.04,0,12),(1.04,0,0),"medium","normal",0,"tilting up with his gaze toward the being"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_fire(),mid_pillars(col='#f0d0a0'),near_clouds()],
 background=cloud_bg(['#2a56b4','#8aa8e0','#ffd0a0','#fff2e0'],sx=700,sy=200),mood={"emotion":"awe","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.46,"flip":1,"pose":"sit","emo":"surprise","look":800,"mood":{"surp":0.8,"ly":-0.7},
   "actions":[{"word":"awe","mood":{"surp":1,"mouth":0.4,"ly":-0.8},"d":0.6}]}],
 effects=[{"k":"glow","x":800,"y":90,"r":320,"rgb":"255,160,80","ga":0.5,"par":0.6,"behind":True,"meaning":"Rudra's firelight falling on Brahma from above"}],
 transition_in="cut"))
# 20 --------------------------------------------------------------- Tell me my name (stack)
S.append(shot("s20",44.02,
 meaning="The being roared again, demanding his name.",
 why="Stacked: above, Rudra lunges forward with raised hand and red eyes, roaring; below, Brahma looks up at him in fear and wonder.",
 camera=cam("pull_out",(1.04,0,0),(1.0,0,0),"two_shot","normal",2,"a small pull back as the roar hits"),
 focus={"subject":"rudra","depth":"deep"},vertical={"mode":"stack","stack":["rudra","brahma"]},
 layers=[far_fire(xs=(380,900)),mid_pillars((250,1030),col='#f4c890'),near_clouds((300,980),col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sy=180),mood={"emotion":"demand","grade":"warm"},
 characters=[{"who":"rudra","x":820,"y":660,"s":0.95,"flip":-1,"pose":"stand","emo":"rage","talk":0.9,"look":"brahma",
   "actions":[{"word":"roared","pose":"raise","mood":{"anger":1,"mouth":0.8},"e":"antic","d":0.5}]},
  {"who":"brahma","x":440,"y":680,"s":0.95,"flip":1,"pose":"sit","emo":"surprise","look":"rudra","mood":{"ly":-0.5},
   "actions":[{"word":"Tell","emo":"fear","mood":{"ly":-0.6},"d":0.5}]}],
 effects=[{"k":"shock","word":"roared","x":820,"y":380,"rgb":"255,150,80","max":600,"meaning":"the second roar going out in rings"}],
 transition_in="cut"))
# 21 --------------------------------------------------------------- Brahma remembered
S.append(shot("s21",47.12,
 meaning="Brahma remembered a root word.",
 why="Brahma on his lotus turns his eyes up and smiles as he remembers; a soft gold ring of light opens behind his heads on 'remembered'.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the moment he remembers"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.1,"y":0.42},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(['#2456b4','#7aa8e8','#ffdcb0','#fff6e6'],sx=700),mood={"emotion":"remembering","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.45,"flip":1,"pose":"sit","emo":"doubt","look":640,"mood":{"ly":-0.6},
   "actions":[{"word":"remembered","emo":"calm","mood":{"ly":-0.7,"smile":0.3},"d":0.6},{"word":"root","mood":{"smile":0.5,"ly":-0.4},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"remembered","x":640,"y":0,"_head":0,"w":280,"alpha":0.45,"blend":"lighter","par":1.0,"behind":True,"meaning":"the memory lighting up in his mind"}],
 transition_in="cut"))
# 22 --------------------------------------------------------------- red, roaring, rud
S.append(shot("s22",48.96,
 meaning="The root word for both red and roaring is rud.",
 why="Rudra below with red eyes; the word 'red' appears in red on 'red', 'roaring' on 'roaring' as his mouth opens, and the big gold root 'rud' between them on 'rud'.",
 camera=cam("dolly_right",(1.0,-8,0),(1.0,8,0),"medium","normal",0,"a slow drift while the words appear"),
 focus={"subject":"rudra","depth":"deep"},vertical={"x":640},
 layers=[far_fire(),mid_pillars(col='#f4c890'),near_clouds(col='#fff4ec')],
 background=cloud_bg(SKY_FIRE,sy=240),mood={"emotion":"meaning","grade":"warm"},
 characters=[{"who":"rudra","x":640,"y":690,"s":0.9,"_face":0.52,"flip":1,"pose":"stand","emo":"anger","look":640,
   "actions":[{"word":"red","emo":"rage","d":0.5},{"word":"roaring","mood":{"anger":1,"mouth":0.8},"d":0.5},{"word":"rud","emo":"anger","mood":{"mouth":0},"d":0.5}]}],
 effects=[{"k":"text","word":"red","s":"red","x":540,"y":95,"size":46,"col":"#ff5a3a","meaning":"the word red"},
  {"k":"text","word":"roaring","s":"roaring","x":745,"y":95,"size":42,"col":"#8a2a10","meaning":"the word roaring"},
  {"k":"text","word":"rud","s":"rud","x":640,"y":170,"size":72,"col":"#7a1a08","glow":1,"meaning":"the root word rud that means both"}],
 transition_in="cut"))
# 23 --------------------------------------------------------------- Rudra, I name you Rudra
S.append(shot("s23",51.74,
 meaning="Brahma named him Rudra.",
 why="The window pans from Brahma raising his hand in blessing to Rudra, whose red eyes calm as he is named; the name plate 'Rudra' appears over him.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan carries the name from Brahma to Rudra"),
 focus={"subject":"rudra","depth":"deep"},vertical={"x":[540,760]},
 layers=[far_clouds(xs=(540,800)),{"d":"mid","contents":"gold pillars behind both","fog":0.2,"items":[{"o":"pillar","x":390,"y":700,"s":1.0,"col":"#ecc878","h":520},{"o":"pillar","x":910,"y":700,"s":1.0,"col":"#ecc878","h":520}]},near_clouds((440,880))],
 background=cloud_bg(['#2a56b4','#8aa8e0','#ffd4a8','#fff4e4'],sx=760),mood={"emotion":"naming","grade":"warm"},
 characters=[{"who":"brahma","x":520,"y":690,"s":0.95,"_face":0.44,"flip":1,"emo":"calm","talk":0.7,"look":"rudra",
   "actions":[{"word":"Rudra","pose":"raise","emo":"joy","d":0.6}]},
  {"who":"rudra","x":775,"y":690,"s":0.95,"_face":0.42,"flip":-1,"pose":"stand","emo":"anger","look":"brahma",
   "actions":[{"word":"Rudra","emo":"calm","mood":{"smile":0.2},"d":0.8}]}],
 effects=[name("Rudra","Rudra",775,120,32),
  {"k":"glow","word":"name","x":775,"y":0,"_head":1,"r":200,"rgb":"255,220,170","ga":0.4,"par":1.0,"behind":True,"meaning":"the calm that comes with his name"}],
 transition_in="cut"))
# 24 --------------------------------------------------------------- This was Shiva, Mahadev
S.append(shot("s24",55.1,
 meaning="This being was Shiva, also called Mahadev.",
 why="Rudra's fire halo cools into Shiva's blue halo: on 'Shiva' the newborn dissolves into the familiar Mahadev with trishul and serpent, and his name plate appears on 'Mahadev'.",
 camera=cam("crane_up",(1.06,0,10),(1.0,0,-6),"medium","normal",0,"rising with the reveal of who he is"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#eef4fc','#ffffff',mcol='#a8b8e0'),mid_pillars(col='#e8d8b0'),near_clouds()],
 background=cloud_bg(SKY_SHIVA),mood={"emotion":"revelation","grade":"cool"},
 characters=[{"who":"rudra","x":640,"y":690,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"fo":"Shiva"},"engine":{"fd":1.0}},
  {"who":"shiva","x":640,"y":690,"s":1.0,"_ground":True,"flip":1,"pose":"stand","emo":"calm","look":640,"mood":{"smile":0.3},"engine_cues":{"ac":"Shiva"},"engine":{"ad":1.0},
   "actions":[{"word":"Mahadev","mood":{"smile":0.5},"tilt":0.03,"d":0.6}]}],
 effects=[{"k":"glow","word":"Shiva","x":640,"y":330,"r":260,"rgb":"190,215,255","ga":0.5,"par":1.0,"behind":True,"meaning":"Shiva's pale blue light replacing the fire"},
  name("also","Mahadev",640,120,32)],
 transition_in="fade"))
# 25 --------------------------------------------------------------- Brahma created
S.append(shot("s25",58.4,
 meaning="Brahma is the creator.",
 why="Brahma smiles on his lotus in gold light, book and mala in his hands; the plate 'Creator' appears.",
 camera=cam("push_in",(1.0,0,0),(1.05,0,-4),"medium","normal",0,"a short push on the first of the three"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(),mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.45,"flip":1,"pose":"sit","emo":"joy","look":640,"mood":{"smile":0.6},
   "actions":[{"word":"created","mood":{"smile":0.8,"ly":-0.2},"tilt":0.04,"d":0.5}]}],
 effects=[{"k":"glow","word":"created","x":640,"y":330,"r":260,"rgb":"255,215,140","ga":0.5,"par":1.0,"behind":True,"meaning":"the gold light of creation"},
  name("Brahma","Creator",640,120,32)],
 transition_in="fade"))
# 26 --------------------------------------------------------------- Vishnu preserved
S.append(shot("s26",59.7,
 meaning="Vishnu is the preserver.",
 why="Blue Vishnu stands calm and smiling in his blue-gold sky with a raised blessing hand; the plate 'Preserver' appears.",
 camera=cam("dolly_left",(1.0,8,0),(1.0,-8,0),"medium","normal",0,"a short drift to the second of the three"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(SKY_VISH),mood={"emotion":"protection","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":690,"s":1.0,"_face":0.44,"flip":1,"pose":"stand","emo":"calm","look":640,"mood":{"smile":0.7},
   "actions":[{"word":"preserved","pose":"raise","emo":"joy","d":0.5}]}],
 effects=[name("Vishnu","Preserver",640,120,32)],
 transition_in="cut"))
# 27 --------------------------------------------------------------- Shiva the destroyer
S.append(shot("s27",60.88,
 meaning="Shiva is the destroyer.",
 why="Shiva with his trishul in a violet-rose sky, his face stern; his third eye glows and the plate 'Destroyer' appears.",
 camera=cam("tilt_up",(1.04,0,14),(1.04,0,0),"medium","normal",0,"tilt up to the third of the three"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#f4e8f4','#fff4f4',mcol='#b0a0d0'),mid_pillars(col='#e0c0a8'),near_clouds()],
 background=cloud_bg(SKY_DUSK),mood={"emotion":"power","grade":"warm"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":0.44,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"destroyer","emo":"anger","mood":{"anger":0.5},"d":0.6}]}],
 effects=[{"k":"glow","word":"destroyer","x":640,"y":0,"_fore":1,"r":70,"rgb":"255,120,80","ga":0.6,"par":1.0,"meaning":"the third eye of the destroyer glowing"},
  name("Shiva","Destroyer",640,120,32)],
 transition_in="cut"))
# 28 --------------------------------------------------------------- asked him to help create
S.append(shot("s28",62.98,
 meaning="Brahma asked Shiva to help with creation.",
 why="The window pans from Brahma pleading with open hands to Shiva, who listens calmly with his head tilted.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan carries the request from Brahma to Shiva"),
 focus={"subject":"shiva","depth":"deep"},vertical={"x":[540,760]},
 layers=[far_clouds(xs=(540,800)),{"d":"mid","contents":"gold pillars behind both","fog":0.2,"items":[{"o":"pillar","x":390,"y":700,"s":1.0,"col":"#ecc878","h":520},{"o":"pillar","x":910,"y":700,"s":1.0,"col":"#ecc878","h":520}]},near_clouds((440,880))],
 background=cloud_bg(sx=700),mood={"emotion":"request","grade":"warm"},
 characters=[{"who":"brahma","x":520,"y":690,"s":0.95,"_face":0.44,"flip":1,"emo":"calm","talk":0.7,"look":"shiva",
   "actions":[{"word":"help","pose":"plead","emo":"devotion","d":0.6}]},
  {"who":"shiva","x":775,"y":690,"s":0.95,"_face":0.42,"flip":-1,"pose":"stand","emo":"calm","look":"brahma",
   "actions":[{"word":"creation","tilt":0.05,"mood":{"smile":0.3},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 29 --------------------------------------------------------------- Shiva agreed, began making beings
S.append(shot("s29",65.26,
 meaning="Shiva agreed and started to make beings.",
 why="Shiva nods with folded hands on 'agreed', then opens his hands on 'making'; a first being of light, his own shape, fades in behind him on 'beings'.",
 camera=cam("crane_down",(1.0,0,-14),(1.04,0,0),"medium","normal",0,"descending on the god at work"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#eef4fc','#ffffff',mcol='#a8b8e0'),mid_pillars(col='#e8d8b0'),near_clouds()],
 background=cloud_bg(SKY_SHIVA,sx=700),mood={"emotion":"creation","grade":"cool"},
 characters=[{"who":"rudra","x":760,"y":600,"s":0.62,"_face":0.34,"flip":-1,"pose":"stand","emo":"calm","look":"shiva","engine_cues":{"ac":"began"},"engine":{"ad":0.8,"a":0.85}},
  {"who":"shiva","x":610,"y":690,"s":1.0,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"agreed","pose":"namaste","tilt":0.05,"mood":{"smile":0.4},"d":0.6},{"word":"making","pose":"open","d":0.6}]}],
 effects=[{"k":"glow","word":"began","x":760,"y":0,"_head":1,"r":160,"rgb":"255,200,140","ga":0.45,"par":1.0,"behind":True,"meaning":"the light a new being appears in"}],
 transition_in="fade"))
# 30 --------------------------------------------------------------- copies of himself, immortal
S.append(shot("s30",67.8,
 meaning="The beings Shiva made were copies of himself, and each one was immortal.",
 why="Around Shiva, four beings with his face, jata and fire halo fade in one after another on 'copies' and 'himself'; on 'immortal' a ring of undying light opens behind them.",
 camera=cam("pull_out",(1.06,0,-6),(1.0,0,0),"wide","wide",0,"pulling back to reveal how many copies there are"),
 focus={"subject":"shiva","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#eef4fc','#ffffff',mcol='#a8b8e0'),{"d":"mid","contents":"cloud banks behind the row of beings","fog":0.25,"items":[{"o":"cloud","x":470,"y":560,"s":1.1,"col":"#ffffff"},{"o":"cloud","x":820,"y":570,"s":1.0,"col":"#ffffff"}]},near_clouds()],
 background=cloud_bg(SKY_SHIVA),mood={"emotion":"multiplication","grade":"cool"},
 characters=[{"who":"rudra","x":495,"y":600,"s":0.6,"_face":0.33,"flip":1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"ac":"copies"},"engine":{"ad":0.6}},
  {"who":"rudra","x":785,"y":600,"s":0.6,"_face":0.33,"flip":-1,"pose":"namaste","emo":"calm","look":640,"engine_cues":{"ac":"copies"},"engine":{"ad":0.6}},
  {"who":"rudra","x":530,"y":660,"s":0.7,"_face":0.4,"flip":1,"pose":"namaste","emo":"calm","look":640,"engine_cues":{"ac":"himself"},"engine":{"ad":0.6}},
  {"who":"rudra","x":750,"y":660,"s":0.7,"_face":0.4,"flip":-1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"ac":"himself"},"engine":{"ad":0.6}},
  {"who":"shiva","x":640,"y":690,"s":0.88,"_face":0.47,"flip":1,"pose":"open","emo":"calm","look":640,"mood":{"smile":0.4},
   "actions":[{"word":"immortal","emo":"joy","mood":{"smile":0.6},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"immortal","x":640,"y":300,"w":560,"alpha":0.45,"blend":"lighter","par":1.0,"behind":True,"meaning":"immortality, a ring of undying light behind them all"}],
 transition_in="cut"))
# 31 --------------------------------------------------------------- eleven Rudras before Brahma (stack)
CROWD=[(640,372,.42,1,'namaste'),(560,372,.42,1,'stand'),(720,372,.42,-1,'stand'),
       (520,430,.48,1,'stand'),(600,430,.48,1,'namaste'),(680,430,.48,-1,'namaste'),(760,430,.48,-1,'stand'),
       (478,500,.54,1,'namaste'),(585,500,.54,1,'stand'),(695,500,.54,-1,'stand'),(802,500,.54,-1,'namaste')]
S.append(shot("s31",71.46,
 meaning="Eleven Rudras now stood in front of Brahma.",
 why="Stacked: above, eleven identical Rudras with fire halos stand in three rows on the clouds; below, Brahma on his lotus looks at them in surprise.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"two_shot","normal",0,"stillness: a whole row of gods just standing there"),
 focus={"subject":"rudra","depth":"deep"},vertical={"mode":"stack","stack":["rudra","brahma"],"h":430},
 layers=[far_clouds(xs=(420,900)),{"d":"mid","contents":"cloud banks behind the rows of Rudras","fog":0.25,"items":[{"o":"cloud","x":470,"y":360,"s":1.2,"col":"#ffffff"},{"o":"cloud","x":820,"y":370,"s":1.1,"col":"#ffffff"}]},near_clouds((300,1000))],
 background=cloud_bg(sx=760,sy=160),mood={"emotion":"surprise","grade":"warm"},
 characters=[{"who":"rudra","x":x,"y":y,"s":s,"_fix":1,"flip":fl,"pose":p,"emo":"calm","look":1050} for x,y,s,fl,p in CROWD]+
  [{"who":"brahma","x":1060,"y":640,"s":0.85,"_fix":1,"flip":-1,"pose":"sit","emo":"surprise","look":640,"mood":{"surp":0.8},
   "actions":[{"word":"Brahma","mood":{"surp":1,"mouth":0.3},"d":0.6}]}],
 effects=[name("Eleven","Eleven Rudras",640,80,26)],
 transition_in="cut"))
# 32 --------------------------------------------------------------- mortals who die and are born again
S.append(shot("s32",73.84,
 meaning="Brahma said creation needed mortal beings who die and are born again.",
 why="Brahma explains from his lotus, eyes on the sky; above him the gold wheel of birth and death turns on 'die' and glows on 'born': what creation needs.",
 camera=cam("tilt_down",(1.04,0,-14),(1.04,0,0),"medium","normal",0,"tilting down from the wheel to the creator"),
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=cloud_bg(sx=640,sy=160),mood={"emotion":"explaining","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.47,"flip":1,"pose":"sit","emo":"doubt","talk":0.7,"look":800,
   "actions":[{"word":"mortals","mood":{"ly":-0.4},"tilt":0.04,"d":0.6},{"word":"again","emo":"calm","mood":{"ly":0.3},"d":0.6}]}],
 effects=[{"k":"icon","i":"cycle","word":"creation","x":640,"y":130,"sc":1.2,"par":1.0,"behind":True,"meaning":"the round of death and rebirth creation needs"},
  {"k":"glow","word":"born","x":640,"y":130,"r":180,"rgb":"255,230,170","ga":0.5,"par":1.0,"behind":True,"meaning":"birth again, the wheel lighting up"}],
 transition_in="cut"))
# 33 --------------------------------------------------------------- only immortals
S.append(shot("s33",78.12,
 meaning="Shiva answered that he could only make immortal beings.",
 why="Shiva speaks calmly with an open hand while two of his fire-haloed copies stand faint behind him.",
 camera=cam("dolly_right",(1.04,-8,0),(1.04,8,0),"medium","normal",0,"a calm drift while he answers"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#eef4fc','#ffffff',mcol='#a8b8e0'),mid_pillars(col='#e8d8b0'),near_clouds()],
 background=cloud_bg(SKY_SHIVA,sx=600),mood={"emotion":"calm","grade":"cool"},
 characters=[{"who":"rudra","x":520,"y":600,"s":0.6,"_face":0.33,"flip":1,"pose":"stand","emo":"calm","look":640,"engine":{"a":0.5}},
  {"who":"rudra","x":770,"y":600,"s":0.6,"_face":0.33,"flip":-1,"pose":"namaste","emo":"calm","look":640,"engine":{"a":0.5}},
  {"who":"shiva","x":640,"y":690,"s":1.0,"_face":0.46,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":540,
   "actions":[{"word":"only","pose":"open","d":0.6},{"word":"immortals","mood":{"blink":0.4,"smile":0.2},"tilt":-0.04,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 34 --------------------------------------------------------------- he would rather meditate
S.append(shot("s34",80.74,
 meaning="If that spoiled Brahma's plan, Shiva would rather meditate.",
 why="Shiva closes his eyes and folds his hands on 'meditate' as the hall behind him cross-fades to the white Himalaya.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in as he turns inward"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva","z":1.08,"y":0.42},
 layers=[far_snow(),mid_pines(),near_snow()],
 background={**cloud_bg(SKY_SHIVA),"change":{"word":"meditate","bg2":snow_bg(),"d":1.0}},
 mood={"emotion":"withdrawal","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","talk":0.5,"look":540,
   "actions":[{"word":"spoiled","mood":{"ly":0.4},"d":0.6},{"word":"rather","pose":"namaste","mood":{"blink":1,"smile":0.3},"d":0.7}]}],
 effects=[],transition_in="cut"))
# 35 --------------------------------------------------------------- then he left
S.append(shot("s35",83.4,
 meaning="Then Shiva walked away and left Brahma.",
 why="On a bright snowy slope Shiva walks away to the right with his trishul and fades into the white haze.",
 camera=cam("pan_right",(1.0,0,0),(1.0,0,0),"wide","wide",0,"the pan follows him walking away"),
 focus={"subject":"shiva","depth":"deep"},vertical={"x":[600,700]},
 layers=[far_snow((520,820)),mid_pines((440,880)),near_snow((450,860))],
 background=snow_bg(sx=760),mood={"emotion":"departure","grade":"cool"},
 characters=[{"who":"shiva","x":600,"y":690,"s":0.85,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"Then","to_x":740,"d":1.3,"speed":1},
   "engine_cues":{"fo":"left"},"engine":{"fd":1.0}}],
 effects=[{"k":"mist_wisps","word":"left","x":720,"y":520,"w":360,"alpha":0.6,"par":1.0,"meaning":"the white haze he disappears into"}],
 transition_in="wipe"))
# 36 --------------------------------------------------------------- what never dies
S.append(shot("s36",84.64,
 meaning="The god born from Brahma's anger could only make what never dies.",
 why="Shiva sits in meditation on the snowy peak with closed eyes; behind him a faint warm glow of the fire he was born from, and on 'never' a ring of undying light opens as the camera pulls away.",
 camera=cam("pull_out",(1.1,0,-8),(1.0,0,0),"wide","wide",0,"final pull out on the meditating god"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_snow(),mid_pines(),near_snow()],
 background=snow_bg(sx=640,sy=200),mood={"emotion":"stillness","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.05,"_face":0.47,"flip":1,"pose":"sitpray","prop":"none","emo":"calm","mood":{"blink":1,"smile":0.3},"look":640,
   "actions":[{"word":"anger","mood":{"blink":1,"smile":0.2},"tilt":0.03,"d":0.6}]}],
 effects=[{"k":"glow","word":"anger","x":640,"y":0,"_head":0,"r":260,"rgb":"255,170,100","ga":0.4,"par":1.0,"behind":True,"meaning":"the fire of anger he was born from, now a quiet glow"},
  {"k":"halo_ring","word":"never","x":640,"y":0,"_head":0,"w":460,"alpha":0.45,"blend":"lighter","par":1.0,"behind":True,"meaning":"what never dies, a ring of undying light"}],
 transition_in="fade"))
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
for s in S:
    if (s.get('vertical') or {}).get('mode')=='stack':continue
    g=None
    for f in s['characters']:
        if f.get('head') or f.get('_fix'):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        tgt=f.pop('_face',.42)
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None:g=f['y']
for s in S:
    for f in s['characters']:f.pop('_face',None);f.pop('_ground',None);f.pop('_fix',None)
# effects anchored to a figure: _head = at its face (+k*s*100 lower), _fore = its forehead, _feet = its feet; anchor = the figure that is not faded in later
def anchor(s,e):
    F=[f for f in s['characters'] if abs(f.get('x',640)-e['x'])<40 and not (f.get('engine_cues') or {}).get('ac')] or s['characters']
    f=min(F,key=lambda f:abs(f.get('x',640)-e['x']))
    fc=f['y'] if f.get('head') else f['y']-(195 if VB.seated(f) else 300)*f['s']
    return f,fc
for s in S:
    for e in s['effects']:
        if '_head' in e:f,fc=anchor(s,e);e['y']=round(fc+e.pop('_head')*100*f['s'])
        if '_fore' in e:f,fc=anchor(s,e);e.pop('_fore');e['y']=round(fc-22*f['s'])
        if '_feet' in e:f,fc=anchor(s,e);e.pop('_feet');e['y']=round(f['y']-80*f['s'])
for s in S:
    cam_={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        y0=f['y']
        while VB.face_cropped_v(f,cam_,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
for i,s_ in enumerate(S):s_['id']=f"s{i+1:02d}"
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel05","format":"vertical","shots":S},open(f'{R}/reels/reel05/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
