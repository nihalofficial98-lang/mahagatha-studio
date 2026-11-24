#!/usr/bin/env python3
"""Generator for reels/reel01/briefs.json (cinematographer -> scene -> action -> effects passes, written as data)."""
import json,os
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel01/words.json'))
T=[(w['w'],w['start']) for w in W]
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(word,t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette ----------
SKY_GOLD=['#2f4aa8','#7d9ce8','#ffd49a','#fff3d6']
SKY_SORROW=['#2c3c72','#5d70a8','#aab8d8','#e4e8f4']
SKY_VAIK=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']
SKY_KAIL=['#3a6ac0','#86b6ea','#d8ecfa','#fff8ec']
SKY_SHAKTI=['#7a2a72','#c75c8e','#ffb48a','#fff0cc']
SKY_DAWN=['#3a5ab0','#8aa8e0','#ffc49a','#fff0cc']
SKY_VIOLET=['#251a5a','#5a4aa0','#b09ad8','#ecdff4']
def far_clouds(haze='#f4e6d0',col='#fff4e6',xs=(520,780)):
    return {"d":"far","contents":"soft cloud banks and two hazy peaks far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-60,"y":500,"s":1.0,"col":"#9a9ac8"},{"o":"mountain","x":xs[1]+40,"y":510,"s":0.85,"col":"#9a9ac8"},
                     {"o":"cloud","x":xs[0],"y":230,"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":270,"s":1.1,"col":col}]}
def mid_pillars(xs=(450,830),col='#e8c878',h=520):
    return {"d":"mid","contents":"two gold pillars framing the figure","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810)):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":"#ffffff"}]}
def far_snow(haze='#dce8f8',xs=(470,820)):
    return {"d":"far","contents":"snow peaks of Kailash in pale blue haze","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0],"y":480,"s":1.25,"col":"#8a9ccc"},{"o":"mountain","x":xs[1],"y":490,"s":1.05,"col":"#8a9ccc"},{"o":"cloud","x":640,"y":200,"s":1.1,"col":"#ffffff"}]}
def mid_pines(xs=(450,840)):
    return {"d":"mid","contents":"pines and a grey rock on the mountain shelf","fog":0.22,
            "items":[{"o":"tree","x":xs[0],"y":610,"s":0.75,"kind":"pine","col":"#2f6a52"},{"o":"rock","x":xs[1],"y":630,"s":1.0,"col":"#7a88a8"},{"o":"tree","x":xs[1]+60,"y":600,"s":0.65,"kind":"pine","col":"#2f6a52"}]}
def near_rocks(xs=(450,830),col='#3a4660'):
    return {"d":"near","contents":"dark blurred rocks in the bottom corners","dark":0.5,
            "items":[{"o":"rock","x":xs[0],"y":745,"s":1.7,"col":col},{"o":"rock","x":xs[1],"y":748,"s":1.5,"col":col}]}
def shot(id,t,i1,**k):
    i0=idx(None,t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!')},"narration":span(i0,i1)};s.update(k);return s
S=[]
nxt=lambda t:None
# 1 ---------------------------------------------------------------------------------
S.append(shot("s01",0.16,9,
 meaning="The common belief: Brahma, the creator, made the first humans.",
 why="Brahma sits on his lotus in a bright gold heaven below the title card; he opens his arms on 'creator' as rays of creation fall on him.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-6,"r":0},"shake":0,"motivation":"slow push in while the familiar claim is stated"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":190},
 mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.1,"_face":0.5,"flip":1,"pose":"sit","emo":"calm","look":640,
   "actions":[{"word":"creator","pose":"open","emo":"pride","e":"spring","d":0.6},{"word":"humans","emo":"joy","d":0.5}]}],
 effects=[{"k":"divine_rays","x":640,"y":80,"w":700,"alpha":0.4,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of creation that everyone credits to Brahma"}],
 transition_in="fade"))
# 2
S.append(shot("s02",4.38,15,
 meaning="But Brahma could not make the first humans.",
 why="Close on Brahma's three faces: confidence drains, eyes drop and the brows knit on 'not' as the gold light cools.",
 camera={"shot":"close","lens":"tele","move":"pull_out","from":{"z":1.1,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pulling back leaves him small with his failure"},
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma"},
 layers=[far_clouds('#d8dcec','#eef0f8'),mid_pillars(col='#d8c08a'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200,"change":{"word":"not","bg2":{"k":"cloudscape","sky":SKY_SORROW,"sx":640,"sy":200},"d":1.0}},
 mood={"emotion":"doubt","grade":"cool"},
 characters=[{"who":"brahma","x":640,"y":350,"s":1.15,"flip":1,"head":True,"emo":"doubt","look":640,
   "actions":[{"word":"not","emo":"sad","mood":{"ly":0.6},"tilt":-0.06,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 3
S.append(shot("s03",6.42,27,
 meaning="Brahma's own mind-born sons refused to create, and the work of creation was exhausting him.",
 why="Brahma pleads toward his child-sage sons; on 'rejected' they turn their backs and walk away, and on 'wearing' he sags into grief in a cooling blue sky.",
 camera={"shot":"wide","lens":"wide","move":"pan_right","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":10,"y":0,"r":0},"shake":0,"motivation":"pan follows the sons as they walk out of his life"},
 focus={"subject":"brahma","depth":"deep"},vertical={"x":[610,630]},
 layers=[far_clouds('#d8dcec','#eef0f8',(560,800)),
   {"d":"mid","contents":"a gold pillar and a pale rock on the cloud floor","fog":0.25,"items":[{"o":"pillar","x":440,"y":700,"s":0.9,"col":"#d8c08a","h":480},{"o":"rock","x":860,"y":640,"s":0.9,"col":"#a8b0c8"}]},
   near_clouds((450,830))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200,"change":{"word":"wearing","bg2":{"k":"cloudscape","sky":SKY_SORROW,"sx":640,"sy":200},"d":1.2}},
 mood={"emotion":"sorrow","grade":"cool"},
 characters=[{"who":"brahma","x":510,"y":660,"s":1.0,"_face":0.4,"flip":1,"pose":"stand","lotus":False,"emo":"sad","look":"kumara",
   "actions":[{"word":"sons","pose":"plead","emo":"sad","d":0.6},{"word":"wearing","pose":"stand","emo":"grief","tilt":-0.08,"d":0.8}]},
  {"who":"kumara","x":660,"y":660,"s":1.05,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"brahma","turn_on":"rejected","walk":{"word":"him","to_x":800,"d":2.6,"speed":1},"actions":[{"word":"rejected","emo":"pride","mood":{"lx":0.9},"d":0.5}]},
  {"who":"kumara","x":750,"y":655,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"brahma","turn_on":"rejected","walk":{"word":"him","to_x":900,"d":2.6,"speed":1},"actions":[{"word":"rejected","emo":"pride","mood":{"lx":0.9},"d":0.5}]}],
 effects=[],transition_in="cut"))
# 4
S.append(shot("s04",10.54,39,
 meaning="Who showed Brahma how? The one god he thought could not create: Shiva.",
 why="An iris opens on violet night at Kailash: Shiva meditates in silhouette and his blue halo brightens on 'god', the answer to the riddle.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.05,"x":0,"y":-30,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilting down from the night sky finds the hidden answer"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[{"d":"far","contents":"Kailash peaks and moon drawn by the background","fog":0.5,"from_background":True},
   {"d":"mid","contents":"the snow rock Shiva sits on and rocks either side","fog":0.15,"items":[{"o":"rock","x":640,"y":586,"s":4.0,"col":"#3e4878","fog":0.05},{"o":"rock","x":470,"y":650,"s":1.0,"col":"#7a86b8"},{"o":"rock","x":820,"y":655,"s":0.9,"col":"#7a86b8"}]},
   near_rocks((460,820),'#232a48')],
 background={"k":"kailash","mx":0.42},
 mood={"emotion":"mystery","grade":"night"},
 characters=[{"who":"shiva","x":640,"y":640,"s":1.05,"_face":0.4,"flip":1,"pose":"sitpray","emo":"calm","mood":{"blink":1,"smile":0.3},"aura":"150,180,255",
   "actions":[{"word":"god","mood":{"blink":1,"smile":0.5},"d":0.8}]}],
 effects=[{"k":"halo_ring","word":"god","x":640,"y":340,"w":420,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"the god he doubted lights up as the answer"}],
 transition_in="iris"))
# 5
S.append(shot("s05",14.92,47,
 meaning="Vishnu the preserver saw how grieved Brahma was.",
 why="Stacked: Vishnu in his bright blue-gold heaven looks down with concern on 'noticed', Brahma below sits in grief with eyes lowered.",
 camera={"shot":"two_shot","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-20,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"descending from Vishnu's heaven to Brahma's sorrow"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"mode":"stack","stack":["vishnu","brahma"]},
 layers=[far_clouds('#e0ecf8','#ffffff',(380,860)),mid_pillars((250,1030)),near_clouds((300,980))],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":180},
 mood={"emotion":"compassion","grade":"warm"},
 characters=[{"who":"vishnu","x":420,"y":650,"s":0.95,"flip":1,"pose":"stand","emo":"calm","look":"brahma",
   "actions":[{"word":"noticed","emo":"sad","mood":{"ly":0.5},"tilt":0.05,"d":0.6}]},
  {"who":"brahma","x":880,"y":680,"s":0.85,"flip":-1,"pose":"sit","emo":"grief","mood":{"ly":0.7},
   "actions":[{"word":"grief","tilt":-0.07,"emo":"grief","d":0.6}]}],
 effects=[{"k":"glow","x":420,"y":330,"r":220,"rgb":"190,220,255","ga":0.45,"par":1.0,"behind":True,"meaning":"Vishnu's preserving light"}],
 transition_in="fade"))
# 6
S.append(shot("s06",18.24,59,
 meaning="Vishnu told Brahma to go to Mahadev, which is another name for Shiva.",
 why="Vishnu speaks and on 'Mahadev' points toward the far snow peak of Kailash, which glows as 'Shiva' is said.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in on the advice that sets the story moving"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.15,"y":0.38},
 layers=[{"d":"far","contents":"the snow peak of Kailash far behind Vishnu's pointing hand","fog":0.5,"haze":"#e4eefa","items":[{"o":"mountain","x":760,"y":470,"s":1.3,"col":"#9aaad4"},{"o":"cloud","x":520,"y":230,"s":1.1,"col":"#ffffff"}]},
   mid_pillars((470,830)),near_clouds((480,800))],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":760,"sy":200},
 mood={"emotion":"guidance","grade":"warm"},
 characters=[{"who":"vishnu","x":600,"y":650,"s":1.0,"_face":0.38,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":800,
   "actions":[{"word":"Mahadev","pose":"point","emo":"joy","e":"spring","d":0.6}]}],
 effects=[{"k":"glow","word":"Shiva","x":760,"y":330,"r":200,"rgb":"200,220,255","ga":0.6,"par":0.3,"behind":True,"meaning":"Kailash, home of Shiva, glows when his name is said"}],
 transition_in="cut"))
# 7
S.append(shot("s07",21.56,67,
 meaning="Brahma objected that Shiva, the destroyer, could not create.",
 why="Brahma, standing, shakes his head in doubt; behind him a red storm glow rises on 'destroyer' to show what he thinks of Shiva.",
 camera={"shot":"medium","lens":"normal","move":"dolly_left","from":{"z":1.05,"x":10,"y":0,"r":0},"to":{"z":1.05,"x":-10,"y":0,"r":0},"shake":0,"motivation":"sideways drift as Brahma backs away from the idea"},
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma","z":1.15,"y":0.42},
 layers=[far_clouds('#e8d8e0','#f8eef0',(520,800)),mid_pillars((460,820),'#d8c08a'),near_clouds((470,810))],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":200,"change":{"word":"destroyer","bg2":{"k":"cloudscape","sky":["#3a1a3a","#8a3a4a","#e08a6a","#f8d8b8"],"sx":640,"sy":200},"d":1.0}},
 mood={"emotion":"doubt","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":665,"s":1.0,"_face":0.4,"flip":-1,"pose":"stand","lotus":False,"emo":"doubt","talk":0.6,"look":420,
   "actions":[{"word":"destroyer","emo":"fear","tilt":0.06,"d":0.5},{"word":"create","pose":"plead","emo":"doubt","tilt":-0.06,"d":0.6}]}],
 effects=[{"k":"glow","word":"destroyer","x":640,"y":260,"r":260,"rgb":"255,110,80","ga":0.35,"par":0.25,"behind":True,"meaning":"the fearsome 'destroyer' Brahma imagines"}],
 transition_in="cut"))
# 8
S.append(shot("s08",24.12,79,
 meaning="Vishnu answered that Shiva may not create, but he would surely give counsel.",
 why="The window pans from Vishnu, open-handed and smiling, to Brahma, whose doubt softens into hope on 'counsel'.",
 camera={"shot":"two_shot","lens":"normal","move":"pan_right","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.02,"x":0,"y":0,"r":0},"shake":0,"motivation":"the pan carries Vishnu's reassurance over to Brahma"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":[560,760]},
 layers=[far_clouds('#e0ecf8','#ffffff',(560,780)),{"d":"mid","contents":"gold pillars behind both gods","fog":0.2,"items":[{"o":"pillar","x":410,"y":700,"s":1.0,"col":"#e8c878","h":520},{"o":"pillar","x":900,"y":700,"s":1.0,"col":"#e8c878","h":520}]},near_clouds((450,880))],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":660,"sy":190},
 mood={"emotion":"hope","grade":"warm"},
 characters=[{"who":"vishnu","x":550,"y":660,"s":1.0,"_face":0.4,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":"brahma",
   "actions":[{"word":"might","pose":"open","emo":"joy","d":0.6}]},
  {"who":"brahma","x":780,"y":665,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","lotus":False,"emo":"doubt","look":"vishnu",
   "actions":[{"word":"counsel","emo":"surprise","mood":{"smile":0.5},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 9
S.append(shot("s09",28.34,83,
 meaning="Brahma went to Kailash and found Shiva deep in meditation.",
 why="On bright snowy Kailash Brahma walks in from the left toward Shiva, who sits still in meditation; Brahma stops in awe.",
 camera={"shot":"wide","lens":"wide","move":"dolly_right","from":{"z":1.0,"x":-10,"y":0,"r":0},"to":{"z":1.0,"x":10,"y":0,"r":0},"shake":0,"motivation":"dolly travels with Brahma's journey to Shiva"},
 focus={"subject":"brahma","depth":"deep"},vertical={"x":[560,650]},
 layers=[far_snow(),{"d":"mid","contents":"pines and the snow rock Shiva sits on","fog":0.15,"items":[{"o":"tree","x":420,"y":600,"s":0.75,"kind":"pine","col":"#2f6a52"},{"o":"rock","x":740,"y":585,"s":4.0,"col":"#4a5680","fog":0.05}]},near_rocks((440,880),'#2f3c5a')],
 background={"k":"vista","sky":SKY_KAIL,"sx":760,"sy":200,"ridge":["#b8c8e8","#98acd8","#7a90c0","#5a70a0"],"haze":"230,240,255"},
 mood={"emotion":"arrival","grade":"cool"},
 characters=[{"who":"brahma","x":450,"y":665,"s":0.95,"_face":0.4,"flip":1,"pose":"stand","lotus":False,"emo":"calm","look":"shiva","walk":{"word":"Brahma","to_x":530,"d":1.4,"speed":1},
   "actions":[{"word":"meditating","emo":"surprise","mood":{"ly":-0.2},"d":0.6}]},
  {"who":"shiva","x":740,"y":665,"s":1.0,"_face":0.4,"flip":-1,"pose":"sitpray","emo":"calm","mood":{"blink":1,"smile":0.3},
   "actions":[{"word":"meditating","mood":{"blink":1,"smile":0.4},"d":0.6}]}],
 effects=[{"k":"glow","x":740,"y":420,"r":220,"rgb":"180,200,255","ga":0.4,"par":1.0,"behind":True,"meaning":"the calm light of Shiva's meditation"}],
 transition_in="wipe"))
# 10
S.append(shot("s10",30.4,94,
 meaning="Brahma sat down and prayed to Shiva with his whole soul.",
 why="Close on Brahma seated with folded hands; on 'prayed' he closes his eyes in devotion and a warm glow rises around him on 'soul'.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.15,"x":0,"y":0,"r":0},"to":{"z":1.25,"x":0,"y":-8,"r":0},"shake":0,"motivation":"push in to the depth of his prayer"},
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma","z":1.2,"y":0.42},
 layers=[far_snow('#e4ecf8',(500,800)),mid_pines((470,820)),near_rocks((470,820),'#2f3c5a')],
 background={"k":"vista","sky":SKY_KAIL,"sx":640,"sy":200,"ridge":["#b8c8e8","#98acd8","#7a90c0","#5a70a0"],"haze":"230,240,255"},
 mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.05,"_face":0.42,"flip":1,"pose":"sit","emo":"devotion","look":800,
   "actions":[{"word":"sat","pose":"sitpray","d":0.6},{"word":"prayed","emo":"devotion","mood":{"blink":1,"smile":0.35},"d":0.7}]}],
 effects=[{"k":"glow","word":"soul","x":640,"y":420,"r":260,"rgb":"255,215,150","ga":0.5,"par":1.0,"behind":True,"meaning":"the warmth of prayer from the depth of his soul"}],
 transition_in="cut"))
# 11
S.append(shot("s11",33.7,98,
 meaning="Shiva opened his eyes.",
 why="Extreme close on Shiva's face: the closed eyes open on 'opened' and a pale blue halo ring pulses out behind his head.",
 camera={"shot":"extreme_close","lens":"tele","move":"static","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"stillness so the opening eyes are the event"},
 focus={"subject":"shiva","depth":"shallow"},vertical={"focus":"shiva"},
 layers=[far_snow('#e4ecf8',(480,820)),{"d":"mid","contents":"pine branches beside his head","fog":0.25,"items":[{"o":"tree","x":450,"y":600,"s":0.8,"kind":"pine","col":"#2f6a52"},{"o":"tree","x":840,"y":610,"s":0.75,"kind":"pine","col":"#2f6a52"}]}],
 background={"k":"vista","sky":SKY_KAIL,"sx":640,"sy":220,"ridge":["#b8c8e8","#98acd8","#7a90c0","#5a70a0"],"haze":"230,240,255"},
 mood={"emotion":"awakening","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":350,"s":1.2,"flip":1,"head":True,"emo":"calm","mood":{"blink":1},
   "actions":[{"word":"opened","mood":{"blink":0,"surp":0.3,"ly":0.2},"d":0.5}]}],
 effects=[{"k":"halo_ring","word":"opened","x":640,"y":330,"w":520,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"his awareness turns outward"}],
 transition_in="cut"))
# 12
S.append(shot("s12",35.52,111,
 meaning="Shiva explained that new life cannot be born the way Brahma made his sons, from mind alone.",
 why="Shiva speaks with an open teaching hand on 'reproduction'; on 'sons' he looks down kindly, the faint child sages behind him recalling the failed way.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.12,"x":0,"y":-6,"r":0},"to":{"z":1.04,"x":0,"y":0,"r":0},"shake":0,"motivation":"pull out as the lesson widens"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva","z":1.1,"y":0.42},
 layers=[far_snow('#e4ecf8',(480,820)),mid_pines((440,860)),near_rocks((450,840),'#2f3c5a')],
 background={"k":"vista","sky":SKY_KAIL,"sx":640,"sy":200,"ridge":["#b8c8e8","#98acd8","#7a90c0","#5a70a0"],"haze":"230,240,255"},
 mood={"emotion":"teaching","grade":"cool"},
 characters=[{"who":"kumara","x":520,"y":560,"s":0.7,"_face":0.36,"flip":1,"pose":"stand","emo":"calm","look":640,"engine":{"a":0.35},
   "actions":[{"word":"sons","emo":"doubt","d":0.6}]},
  {"who":"shiva","x":660,"y":665,"s":1.0,"_face":0.4,"flip":-1,"pose":"stand","emo":"calm","talk":0.6,"look":420,
   "actions":[{"word":"reproduction","pose":"open","d":0.6},{"word":"sons","emo":"sad","mood":{"ly":0.4},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 13
S.append(shot("s13",39.5,121,
 meaning="What Brahma needed was Shakti, the feminine power.",
 why="Adishakti appears in a rose-saffron sky on 'Shakti', arms opening, with golden rays and a halo behind her.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.05,"x":0,"y":20,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up to her divinity"},
 focus={"subject":"adishakti","depth":"deep"},vertical={"focus":"adishakti"},
 layers=[far_clouds('#f8dcd0','#fff0e8',(520,780)),mid_pillars((450,830),'#f0c890'),near_clouds((470,810))],
 background={"k":"cloudscape","sky":SKY_SHAKTI,"sx":640,"sy":220},
 mood={"emotion":"grace","grade":"warm"},
 characters=[{"who":"adishakti","x":640,"y":650,"s":1.05,"_face":0.4,"flip":1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"ac":"Shakti"},"engine":{"ad":0.8},
   "actions":[{"word":"Shakti","pose":"open","emo":"joy","e":"spring","d":0.7}]}],
 effects=[{"k":"divine_rays","word":"Shakti","x":640,"y":120,"w":760,"alpha":0.45,"blend":"lighter","par":0.2,"behind":True,"meaning":"Shakti, the feminine power, shining out"},
  {"k":"halo_ring","word":"power","x":640,"y":330,"w":460,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the power of the feminine"}],
 transition_in="flash"))
# 14
S.append(shot("s14",43.62,125,
 meaning="Then Shiva's body began to change.",
 why="Shiva stands in a swirl of gold and blue light, eyes closing; on 'body' a seam of light runs down his middle and on 'changed' he dissolves into the half-Goddess form.",
 camera={"shot":"medium","lens":"normal","move":"handheld","from":{"z":1.05,"x":0,"y":0,"r":0},"to":{"z":1.1,"x":0,"y":-4,"r":0},"shake":2,"motivation":"slight tremor as the body transforms"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[{"d":"far","contents":"star field and nebula drawn by the cosmos background","fog":0.5,"from_background":True},
   {"d":"mid","contents":"two clouds lit gold and blue either side","fog":0.25,"items":[{"o":"cloud","x":470,"y":560,"s":1.1,"col":"#cfe0ff"},{"o":"cloud","x":820,"y":570,"s":1.1,"col":"#ffe2b0"}]},
   near_clouds((470,810))],
 background={"k":"cosmos","rgb":"255,200,130","spin":0.05},
 mood={"emotion":"transformation","grade":"warm"},
 characters=[{"who":"shiva","x":640,"y":665,"s":1.0,"_face":0.4,"flip":1,"pose":"stand","emo":"calm","mood":{"blink":0.5},"engine_cues":{"fo":"changed"},"engine":{"fd":0.8},
   "actions":[{"word":"Shiva's","mood":{"blink":1,"smile":0.4},"d":0.5}]},
  {"who":"ardha","x":640,"y":665,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":640,"engine_cues":{"ac":"changed"},"engine":{"ad":0.8}}],
 effects=[{"k":"energy_swirl","word":"Shiva's","x":640,"y":420,"w":520,"alpha":0.6,"blend":"lighter","par":1.0,"behind":True,"meaning":"the force of the change swirling around his body"},
  {"k":"light_beam","word":"body","x":640,"y":0,"w":120,"alpha":0.5,"blend":"lighter","par":1.0,"meaning":"a seam of light running down the middle of his body"}],
 transition_in="flash"))
# 15
S.append(shot("s15",45.68,147,
 meaning="His right side became male and his left side female, divided exactly down the middle.",
 why="Ardhanarishvara stands full figure: blue light floods the male half on 'male', rose-gold the female half on 'female', and a seam of light runs down the centre on 'split'.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.15,"x":0,"y":-30,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt down the length of the divided body"},
 focus={"subject":"ardha","depth":"deep"},vertical={"focus":"ardha"},
 layers=[{"d":"far","contents":"star field drawn by the cosmos background","fog":0.5,"from_background":True},
   {"d":"mid","contents":"a blue cloud on the male side and a gold cloud on the female side","fog":0.25,"items":[{"o":"cloud","x":480,"y":560,"s":1.1,"col":"#bcd4ff"},{"o":"cloud","x":810,"y":570,"s":1.1,"col":"#ffd8a8"}]},
   near_clouds((470,810))],
 background={"k":"cosmos","rgb":"200,180,255","spin":0.04},
 mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"ardha","x":640,"y":665,"s":1.05,"_face":0.38,"flip":-1,"pose":"stand","emo":"calm","look":640}],
 effects=[{"k":"glow","word":"male","x":560,"y":380,"r":230,"rgb":"120,170,255","ga":0.6,"par":1.0,"behind":True,"meaning":"the male half (Shiva) lit in blue"},
  {"k":"glow","word":"female","x":720,"y":380,"r":230,"rgb":"255,170,140","ga":0.6,"par":1.0,"behind":True,"meaning":"the female half (the Goddess) lit in rose-gold"},
  {"k":"light_beam","word":"split","x":640,"y":0,"w":60,"alpha":0.45,"blend":"lighter","par":1.0,"meaning":"the exact split down the middle"}],
 transition_in="cut"))
# 16
S.append(shot("s16",50.94,156,
 meaning="This form is called Ardhanarishvara, the androgynous one.",
 why="Close on the half-Shiva, half-Goddess face inside a gold halo ring as the name is spoken; the name plate sits above the head.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in as the form is named"},
 focus={"subject":"ardha","depth":"shallow"},vertical={"focus":"ardha"},
 layers=[far_clouds('#f0e4f4','#fff4f0',(500,800)),mid_pillars((450,830),'#e8c878'),near_clouds((470,810))],
 background={"k":"cloudscape","sky":SKY_VIOLET,"sx":640,"sy":260},
 mood={"emotion":"reverence","grade":"warm"},
 characters=[{"who":"ardha","x":640,"y":380,"s":1.15,"flip":-1,"head":True,"emo":"calm","look":640}],
 effects=[{"k":"halo_ring","word":"Ardhanarishvara","x":640,"y":360,"w":560,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"the sacred form named"},
  {"k":"name","word":"Ardhanarishvara","s":"Ardhanarishvara","x":640,"y":150,"size":30,"meaning":"the name of the form on screen when it is spoken"}],
 transition_in="fade"))
# 17
S.append(shot("s17",54.72,174,
 meaning="Shiva taught that masculine and feminine are the two halves of the cosmos and neither works without the other.",
 why="Ardhanarishvara stands between a blue half and a gold half of the cosmos; on 'halves' two glows meet at the seam, and on 'without' they pulse together.",
 camera={"shot":"wide","lens":"wide","move":"pull_out","from":{"z":1.12,"x":0,"y":-10,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pull out to the scale of the cosmos"},
 focus={"subject":"ardha","depth":"deep"},vertical={"focus":"ardha"},
 layers=[{"d":"far","contents":"stars and nebula drawn by the cosmos background","fog":0.5,"from_background":True},
   {"d":"mid","contents":"blue cloud left, gold cloud right","fog":0.25,"items":[{"o":"cloud","x":470,"y":580,"s":1.2,"col":"#bcd4ff"},{"o":"cloud","x":820,"y":585,"s":1.2,"col":"#ffd8a8"}]},
   near_clouds((470,810))],
 background={"k":"cosmos","rgb":"220,190,255","spin":0.05},
 mood={"emotion":"unity","grade":"warm"},
 characters=[{"who":"ardha","x":640,"y":660,"s":1.0,"_face":0.42,"flip":-1,"pose":"stand","emo":"calm","look":640}],
 effects=[{"k":"glow","word":"masculine","x":520,"y":300,"r":300,"rgb":"110,160,255","ga":0.55,"par":0.6,"behind":True,"meaning":"the masculine half of the cosmos"},
  {"k":"glow","word":"feminine","x":760,"y":300,"r":300,"rgb":"255,190,110","ga":0.55,"par":0.6,"behind":True,"meaning":"the feminine half of the cosmos"},
  {"k":"halo_ring","word":"halves","x":640,"y":330,"w":560,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the two halves joined in one form"}],
 transition_in="cut"))
# 18
S.append(shot("s18",60.82,184,
 meaning="Brahma bowed to the Goddess and asked her to create the female.",
 why="Stacked: the Goddess above, gentle and radiant; Brahma below bows on 'bowed' and joins his hands in namaste on 'asked'.",
 camera={"shot":"two_shot","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-16,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"from the Goddess down to the bowing creator"},
 focus={"subject":"brahma","depth":"deep"},vertical={"mode":"stack","stack":["adishakti","brahma"]},
 layers=[far_clouds('#f8dcd0','#fff0e8',(380,860)),mid_pillars((260,1020),'#f0c890'),near_clouds((300,980))],
 background={"k":"cloudscape","sky":SKY_SHAKTI,"sx":640,"sy":200},
 mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"adishakti","x":800,"y":650,"s":0.95,"flip":-1,"pose":"stand","emo":"calm","look":"brahma",
   "actions":[{"word":"asked","pose":"open","emo":"joy","d":0.6}]},
  {"who":"brahma","x":440,"y":670,"s":0.95,"flip":1,"pose":"stand","lotus":False,"emo":"devotion","look":"adishakti",
   "actions":[{"word":"bowed","pose":"bow","e":"spring","d":0.6},{"word":"asked","pose":"namaste","emo":"devotion","d":0.6}]}],
 effects=[{"k":"glow","x":800,"y":330,"r":220,"rgb":"255,200,170","ga":0.45,"par":1.0,"behind":True,"meaning":"the Goddess's grace"}],
 transition_in="fade"))
# 19
S.append(shot("s19",64.24,190,
 meaning="The Goddess gave Brahma the generative force.",
 why="The Goddess raises her hand on 'gave' and a stream of gold light flows from her to Brahma, who receives it with joy on 'force'.",
 camera={"shot":"two_shot","lens":"normal","move":"pan_left","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pan follows the gift travelling from her to him"},
 focus={"subject":"adishakti","depth":"deep"},vertical={"x":[700,560]},
 layers=[far_clouds('#f8dcd0','#fff0e8',(520,760)),mid_pillars((420,860),'#f0c890'),near_clouds((450,850))],
 background={"k":"cloudscape","sky":SKY_SHAKTI,"sx":700,"sy":200},
 mood={"emotion":"grace","grade":"warm"},
 characters=[{"who":"adishakti","x":730,"y":650,"s":0.95,"_face":0.4,"flip":-1,"pose":"stand","emo":"calm","look":"brahma",
   "actions":[{"word":"gave","pose":"raise","emo":"joy","e":"spring","d":0.6}]},
  {"who":"brahma","x":520,"y":670,"s":0.95,"_ground":True,"flip":1,"pose":"namaste","lotus":False,"emo":"devotion","look":"adishakti",
   "actions":[{"word":"force","pose":"open","emo":"joy","d":0.6}]}],
 effects=[{"k":"orbs","word":"gave","items":[{"c":0,"x0":700,"y0":330,"x1":540,"y1":420,"rgb":"255,220,140","r":70,"sz":8,"dur":1.2,"keep":True},{"c":0,"x0":700,"y0":360,"x1":540,"y1":450,"rgb":"255,200,120","r":60,"sz":6,"dur":1.5,"keep":True}],"meaning":"the generative force flowing from her to Brahma"},
  {"k":"glow","word":"force","x":540,"y":420,"r":240,"rgb":"255,215,140","ga":0.55,"par":1.0,"behind":True,"meaning":"Brahma filled with the generative force"}],
 transition_in="cut"))
# 20
S.append(shot("s20",66.38,201,
 meaning="From his own body Brahma made the first man, Manu.",
 why="Brahma glows with gold light from his own body; Manu takes shape beside him out of the light as 'Brahma made a man' is said, and joins his hands on 'Manu'.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in to the moment of creation"},
 focus={"subject":"manu","depth":"deep"},vertical={"x":[590,680]},
 layers=[far_clouds('#f4e6d0','#fff4e6',(520,780)),mid_pillars((420,860)),near_clouds((450,850))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":190},
 mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma","x":530,"y":670,"s":0.95,"_face":0.4,"flip":1,"pose":"stand","lotus":False,"emo":"calm","look":"manu",
   "actions":[{"word":"made","pose":"open","emo":"joy","d":0.6}]},
  {"who":"manu","x":740,"y":660,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","emo":"surprise","look":"brahma","engine_cues":{"ac":"Brahma"},"engine":{"ad":0.7},
   "actions":[{"word":"Manu","pose":"namaste","emo":"joy","d":0.6}]}],
 effects=[{"k":"glow","word":"body","x":520,"y":420,"r":220,"rgb":"255,220,150","ga":0.55,"par":1.0,"behind":True,"meaning":"life drawn from Brahma's own body"},
  {"k":"halo_ring","word":"man","x":720,"y":380,"w":380,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the first man forming in light"},
  {"k":"embers","word":"man","x":720,"y":520,"w":360,"alpha":0.5,"blend":"lighter","par":1.0,"rgb":"255,230,160","meaning":"motes of creation light around the new man"}],
 transition_in="fade"))
# 21
S.append(shot("s21",69.52,206,
 meaning="Brahma also made the first woman, Brahmi.",
 why="Brahmi forms out of rose-gold light beside Manu on 'woman' and folds her hands on 'Brahmi'; Manu turns to her with joy.",
 camera={"shot":"two_shot","lens":"normal","move":"dolly_right","from":{"z":1.02,"x":-6,"y":0,"r":0},"to":{"z":1.02,"x":6,"y":0,"r":0},"shake":0,"motivation":"dolly reveals the second new life"},
 focus={"subject":"brahmi","depth":"deep"},vertical={"x":[680,700]},
 layers=[far_clouds('#f4e6d0','#fff4e6',(560,820)),mid_pillars((480,920)),near_clouds((500,900))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":700,"sy":190},
 mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"manu","x":600,"y":660,"s":1.0,"_face":0.4,"flip":1,"pose":"namaste","emo":"joy","look":"brahmi",
   "actions":[{"word":"Brahmi","pose":"open","emo":"joy","d":0.6}]},
  {"who":"brahmi","x":790,"y":660,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","emo":"surprise","look":"manu","engine_cues":{"ac":"woman"},"engine":{"ad":0.6},
   "actions":[{"word":"Brahmi","pose":"namaste","emo":"joy","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"woman","x":790,"y":380,"w":380,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the first woman forming in light"},
  {"k":"glow","word":"woman","x":790,"y":420,"r":200,"rgb":"255,190,160","ga":0.5,"par":1.0,"behind":True,"meaning":"rose-gold light of the first woman"}],
 transition_in="cut"))
# 22
S.append(shot("s22",71.3,212,
 meaning="All humanity descends from Manu.",
 why="Manu and Brahmi walk together into a bright dawn valley with trees and a river, the world their children will fill.",
 camera={"shot":"wide","lens":"wide","move":"crane_up","from":{"z":1.08,"x":0,"y":10,"r":0},"to":{"z":1.0,"x":0,"y":-6,"r":0},"shake":0,"motivation":"crane up to the wide world of their descendants"},
 focus={"subject":"manu","depth":"deep"},vertical={"x":[650,690]},
 layers=[{"d":"far","contents":"blue hills and clouds in dawn haze","fog":0.55,"haze":"#f8e4d0","items":[{"o":"hill","x":520,"y":520,"s":1.0,"w":420,"h":90,"col":"#8aa0c8"},{"o":"cloud","x":760,"y":220,"s":1.1,"col":"#fff4e6"}]},
   {"d":"mid","contents":"a banyan and a palm along the river bank","fog":0.2,"items":[{"o":"tree","x":470,"y":620,"s":0.85,"kind":"banyan","col":"#2e6a3c"},{"o":"tree","x":880,"y":610,"s":0.75,"kind":"palm","col":"#2e6a3c"}]},
   {"d":"near","contents":"flowering shrubs in the bottom corners","dark":0.45,"items":[{"o":"shrub","x":480,"y":748,"s":1.5,"col":"#2a5a3a","flowers":"#f0c040"},{"o":"shrub","x":860,"y":748,"s":1.4,"col":"#2a5a3a"}]}],
 background={"k":"vista","sky":SKY_DAWN,"sx":680,"sy":300,"river":"#6ab0e0"},
 mood={"emotion":"hope","grade":"warm"},
 characters=[{"who":"manu","x":600,"y":665,"s":0.95,"_face":0.42,"flip":1,"pose":"stand","emo":"joy","look":"brahmi","walk":{"word":"human","to_x":650,"d":1.8,"speed":0.8}},
  {"who":"brahmi","x":740,"y":665,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"manu","walk":{"word":"human","to_x":740,"d":1.8,"speed":0.8},
   "actions":[{"word":"descends","mood":{"smile":1},"d":0.6}]}],
 effects=[],transition_in="wipe"))
# 23
S.append(shot("s23",73.44,218,
 meaning="So Shiva the destroyer did not make the first humans.",
 why="Back on Kailash, Shiva stands calm with a gentle knowing smile and an open hand; he did not create them, and he looks down kindly on 'humans'.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-6,"r":0},"shake":0,"motivation":"slow push in on the answer to the opening question"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva","z":1.1,"y":0.42},
 layers=[far_snow(),{"d":"mid","contents":"pines and a grey rock on the snow shelf","fog":0.15,"items":[{"o":"tree","x":450,"y":600,"s":0.75,"kind":"pine","col":"#2f6a52"},{"o":"rock","x":820,"y":640,"s":1.2,"col":"#7a88a8"},{"o":"tree","x":850,"y":600,"s":0.65,"kind":"pine","col":"#2f6a52"}]},near_rocks((450,840),'#2f3c5a')],
 background={"k":"vista","sky":SKY_KAIL,"sx":640,"sy":200,"ridge":["#b8c8e8","#98acd8","#7a90c0","#5a70a0"],"haze":"230,240,255"},
 mood={"emotion":"calm","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":665,"s":1.05,"_face":0.4,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"not","pose":"open","emo":"calm","mood":{"smile":0.6},"d":0.6},{"word":"humans","mood":{"ly":0.4,"smile":0.7},"d":0.6}]}],
 effects=[{"k":"glow","x":640,"y":420,"r":220,"rgb":"180,200,255","ga":0.4,"par":1.0,"behind":True,"meaning":"Shiva's quiet light"}],
 transition_in="fade"))
# 24
S.append(shot("s24",76.12,len(T),
 meaning="Shiva showed the creator what creation needs: both halves, masculine and feminine.",
 why="Ardhanarishvara stands in gold light, blue and gold halves glowing; a halo ring opens on 'both halves', the answer made visible.",
 camera={"shot":"wide","lens":"wide","move":"pull_out","from":{"z":1.1,"x":0,"y":-8,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"final pull out to resolve the story"},
 focus={"subject":"ardha","depth":"deep"},vertical={"focus":"ardha"},
 layers=[far_clouds('#f4e6d0','#fff4e6',(500,800)),mid_pillars((450,830)),near_clouds((470,810))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200},
 mood={"emotion":"resolution","grade":"warm"},
 characters=[{"who":"ardha","x":640,"y":665,"s":1.05,"_face":0.4,"flip":-1,"pose":"stand","emo":"calm","look":640}],
 effects=[{"k":"glow","word":"creation","x":560,"y":360,"r":220,"rgb":"120,170,255","ga":0.5,"par":1.0,"behind":True,"meaning":"the masculine half"},
  {"k":"glow","word":"creation","x":720,"y":360,"r":220,"rgb":"255,180,120","ga":0.5,"par":1.0,"behind":True,"meaning":"the feminine half"},
  {"k":"halo_ring","word":"both","x":640,"y":340,"w":580,"alpha":0.6,"blend":"lighter","par":0.9,"behind":True,"meaning":"both halves joined: what creation needed"}],
 transition_in="fade"))
# durations from the next start
for i,s in enumerate(S):
    end=S[i+1]['start']['t'] if i+1<len(S) else 79.65
    s['duration']=round(end-s['start']['t'],2)
    i0=idx(None,s['start']['t']);i1=idx(None,S[i+1]['start']['t']) if i+1<len(S) else len(T);s['narration']=span(i0,i1)
    # check narration ends where next starts
import sys;sys.path.insert(0,R+'/studio');import validate_brief as VB
import math
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
        if f.get('head'):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        tgt=f.pop('_face',.42)
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None:g=f['y']
for s in S:
    for f in s['characters']:f.pop('_face',None);f.pop('_ground',None)
for s in S:
    cam={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        y0=f['y']
        while VB.face_cropped_v(f,cam,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel01","format":"vertical","shots":S},open(f'{R}/reels/reel01/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
# narration continuity check
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
