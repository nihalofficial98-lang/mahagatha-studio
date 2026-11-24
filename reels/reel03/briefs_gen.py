#!/usr/bin/env python3
"""Generator for reels/reel03/briefs.json "Madhu and Kaitabha" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel01/briefs_gen.py: every face is placed at 38-50% of the 9:16 frame height (above the subtitle band)."""
import json,os,sys
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel03/words.json'))
T=[(w['w'],w['start']) for w in W]
END=88.35
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette (bright, clean: blues, gold, orange accents) ----------
SKY_OCEAN=['#1f56b8','#4f92e2','#a6d6f6','#fff1cc']      # primordial ocean by day: blue to gold horizon
SKY_GOLD=['#2f4aa8','#7d9ce8','#ffd49a','#fff3d6']       # Brahma / creation
SKY_DAWN=['#3a5ab0','#8aa8e0','#ffc49a','#fff0cc']       # hope, devotion
SKY_FIGHT=['#33307e','#7a4a9a','#ff9a5a','#ffe2a8']      # battle: violet to orange
SKY_NIDRA=['#262a7a','#5458b8','#a8a8e8','#ece6fa']      # Yoga Nidra: indigo and moon-silver
SKY_THREAT=['#2a2f78','#5a62b0','#f0a080','#ffe4c4']     # menace: cool with an orange edge
SKY_VAIK=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']       # Vishnu's clear heaven
WATER={'k':'waterfront','top':'rgba(46,128,214,.86)','bot':'rgba(16,56,140,.97)'}
def water(y,meaning='the endless primordial water'):return dict(WATER,y=y,meaning=meaning)
def far_clouds(haze='#f4e6d0',col='#fff4e6',xs=(520,780),y=(230,270)):
    return {"d":"far","contents":"soft cloud banks over the far horizon of the ocean","fog":0.55,"haze":haze,
            "items":[{"o":"cloud","x":xs[0],"y":y[0],"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":y[1],"s":1.1,"col":col},{"o":"cloud","x":(xs[0]+xs[1])//2,"y":420,"s":1.4,"col":col}]}
def mid_clouds(xs=(470,820),col='#dce8fa',y=560):
    return {"d":"mid","contents":"mid-distance cloud islands resting on the water","fog":0.22,
            "items":[{"o":"cloud","x":xs[0],"y":y,"s":1.0,"col":col},{"o":"cloud","x":xs[1],"y":y+10,"s":0.9,"col":col}]}
def mid_pillars(xs=(450,830),col='#e8c878',h=520):
    return {"d":"mid","contents":"two gold pillars framing the figure","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810)):
    return {"d":"near","contents":"white mist puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":"#ffffff"}]}
def near_rocks(xs=(450,830),col='#24345e'):
    return {"d":"near","contents":"dark wet rocks blurred in the bottom corners","dark":0.5,
            "items":[{"o":"rock","x":xs[0],"y":745,"s":1.7,"col":col},{"o":"rock","x":xs[1],"y":748,"s":1.5,"col":col}]}
OCEAN=lambda sx=640,sy=300,sky=SKY_OCEAN:{"k":"cloudscape","sky":sky,"sx":sx,"sy":sy}
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!"')}};s.update(k);return s
S=[]
# 1 ------------------------------------------------------------------ title card
S.append(shot("s01",0.12,
 meaning="Vishnu, the preserver, fought two brothers.",
 why="Under the title card Vishnu stands tall over the bright ocean, mace ready; the two dark asura brothers loom faint behind him.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.05,"x":0,"y":-6,"r":0},"shake":0,"motivation":"slow push in to the preserver as the story opens"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#f0e8d8','#fff4e6'),mid_clouds(),near_clouds()],
 background=OCEAN(640,260,SKY_FIGHT),
 mood={"emotion":"conflict","grade":"warm"},
 characters=[
  {"who":"madhu","x":520,"y":560,"s":0.8,"_fix":1,"flip":1,"pose":"stand","emo":"anger","dark":0.55,"look":"vishnu","engine_cues":{"ac":"preserver"},"engine":{"ad":0.7}},
  {"who":"kaitabha","x":770,"y":565,"s":0.8,"_fix":1,"flip":-1,"pose":"stand","emo":"anger","dark":0.55,"look":"vishnu","engine_cues":{"ac":"preserver"},"engine":{"ad":0.7}},
  {"who":"vishnu","x":640,"y":690,"s":1.05,"_face":0.5,"flip":1,"pose":"stand","emo":"calm","look":800,
   "actions":[{"word":"fought","emo":"anger","tilt":0.04,"d":0.5}]}],
 effects=[water(640,"the endless primordial ocean where the fight happens"),
  {"k":"glow","x":640,"y":330,"r":240,"rgb":"190,220,255","ga":0.45,"par":1.0,"behind":True,"meaning":"Vishnu's preserving light"}],
 transition_in="fade"))
# 2 ------------------------------------------------------------------ stack: the endless fight
S.append(shot("s02",3.14,
 meaning="The fight lasted 5,000 years and Vishnu could not win.",
 why="Stacked: Vishnu above lunges with his mace, Madhu below lunges back with his sword; on 'not' Vishnu's face turns to doubt as neither gives way.",
 camera={"shot":"two_shot","lens":"normal","move":"handheld","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.03,"x":0,"y":0,"r":0},"shake":3,"motivation":"unsteady frame for a fight with no end"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"mode":"stack","stack":["vishnu","madhu"]},
 layers=[far_clouds('#f0dcd0','#fff0e4',(380,860)),mid_clouds((250,1030),'#e8d8f0'),near_clouds((300,980))],
 background=OCEAN(640,260,SKY_FIGHT),
 mood={"emotion":"struggle","grade":"warm"},
 characters=[{"who":"vishnu","x":420,"y":650,"s":0.95,"flip":1,"pose":"lunge","emo":"anger","look":"madhu",
   "actions":[{"word":"not","emo":"doubt","tilt":-0.05,"d":0.6}]},
  {"who":"madhu","x":860,"y":660,"s":0.95,"flip":-1,"pose":"lunge","emo":"rage","look":"vishnu",
   "actions":[{"word":"years","emo":"pride","mood":{"smile":0.5,"anger":0.5},"d":0.6}]}],
 effects=[water(640,"the endless ocean under the battle"),
  {"k":"glow","x":640,"y":380,"r":260,"rgb":"255,170,90","ga":0.4,"par":1.0,"behind":True,"meaning":"the heat of the clash between the two fighters"}],
 transition_in="cut"))
# 3 ------------------------------------------------------------------ mace down, gift offered
S.append(shot("s03",6.14,
 meaning="Then Vishnu put down his mace and offered the brothers a gift.",
 why="Vishnu opens his hands so the mace is gone from his grip, and a warm gold light of the gift glows before him as he smiles on 'offered'.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.08,"x":0,"y":-6,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pulling back as the fight stops and the offer opens"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.1,"y":0.42},
 layers=[far_clouds('#e8eef8','#ffffff'),mid_pillars((470,810),'#e8c878'),near_clouds((470,810))],
 background=OCEAN(640,240,SKY_VAIK),
 mood={"emotion":"calm","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","look":800,
   "actions":[{"word":"Then","pose":"open","emo":"calm","d":0.8},{"word":"offered","emo":"joy","mood":{"smile":0.6},"d":0.5}]}],
 effects=[{"k":"glow","word":"mace","x":640,"y":470,"r":170,"rgb":"255,215,130","ga":0.7,"par":1.0,"meaning":"the gift offered in Vishnu's open hands"},
  {"k":"halo_ring","word":"offered","x":640,"y":340,"w":440,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the grace of the offer"}],
 transition_in="cut"))
# 4 ------------------------------------------------------------------ the gift was never for them
S.append(shot("s04",9.44,
 meaning="The gift was a trick: it was never meant for the brothers.",
 why="Close on Vishnu's face: a small knowing smile and a sideways glance on 'never', the light behind him cooling to a deep blue.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on the secret behind the smile"},
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#dce4f4','#eef2fa'),mid_pillars((450,830),'#d8c08a')],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":240,"change":{"word":"never","bg2":{"k":"cloudscape","sky":SKY_NIDRA,"sx":640,"sy":240},"d":1.0}},
 mood={"emotion":"cunning","grade":"cool"},
 characters=[{"who":"vishnu","x":640,"y":360,"s":1.15,"flip":1,"head":True,"emo":"calm","look":640,
   "actions":[{"word":"never","mood":{"smile":0.8,"lx":0.8,"ly":0.1},"tilt":0.05,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 5 ------------------------------------------------------------------ names
S.append(shot("s05",11.60,
 meaning="The brothers were the asuras Madhu and Kaitabha.",
 why="The two horned brothers stand shoulder to shoulder over the ocean, and each name plate appears above its owner the moment the name is spoken.",
 camera={"shot":"two_shot","lens":"normal","move":"tilt_down","from":{"z":1.0,"x":0,"y":-24,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilting down from the names to the two faces"},
 focus={"subject":"madhu","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#e8dcd8','#f8eee8',(500,790)),mid_clouds((440,850),'#d8d8f0'),near_rocks((440,850))],
 background=OCEAN(640,260,SKY_THREAT),
 mood={"emotion":"menace","grade":"warm"},
 characters=[{"who":"madhu","x":555,"y":665,"s":0.88,"_face":0.45,"flip":1,"pose":"stand","emo":"pride","mood":{"smile":0.5,"anger":0.5,"ly":-0.3},
   "actions":[{"word":"Madhu","pose":"raise","emo":"pride","e":"spring","d":0.5}]},
  {"who":"kaitabha","x":730,"y":665,"s":0.88,"_ground":True,"flip":-1,"pose":"stand","emo":"anger","look":"madhu",
   "actions":[{"word":"Kaitabha","emo":"pride","mood":{"smile":0.5,"anger":0.5,"ly":-0.3},"d":0.5}]}],
 effects=[{"k":"name","word":"Madhu","s":"Madhu","x":555,"y":120,"size":30,"meaning":"Madhu's name on screen as it is spoken"},
  {"k":"name","word":"and","d":0.1,"s":"Kaitabha","x":730,"y":175,"size":30,"meaning":"Kaitabha's name on screen as it is spoken"},
  water(650,"the ocean the brothers rule")],
 transition_in="cut"))
# 6 ------------------------------------------------------------------ born from earwax
S.append(shot("s06",14.10,
 meaning="The brothers crawled out of the wax in sleeping Vishnu's ear.",
 why="Vishnu sleeps on the coils of Shesha over the water; beside his ear two tiny asuras appear in a dull amber glow on 'crawled'.",
 camera={"shot":"wide","lens":"wide","move":"dolly_right","from":{"z":1.0,"x":-8,"y":0,"r":0},"to":{"z":1.0,"x":8,"y":0,"r":0},"shake":0,"motivation":"drifting along the sleeping god to find the tiny newcomers"},
 focus={"subject":"vishnu_rest","depth":"deep"},vertical={"x":[600,620]},
 layers=[far_clouds('#e4e0f4','#f4f0fc',(500,800)),mid_clouds((440,860),'#d4d8f4',590),near_clouds((450,850))],
 background=OCEAN(640,230,SKY_NIDRA),
 mood={"emotion":"strange birth","grade":"cool"},
 characters=[{"who":"vishnu_rest","x":720,"y":560,"s":1.0,"_fix":1,"flip":1,"emo":"calm","mood":{"blink":1},"look":640},
  {"who":"madhu","x":528,"y":335,"s":0.24,"_fix":1,"flip":1,"pose":"stand","emo":"surprise","look":700,"engine_cues":{"ac":"crawled"},"engine":{"ad":0.6}},
  {"who":"kaitabha","x":630,"y":340,"s":0.22,"_fix":1,"flip":-1,"pose":"stand","emo":"surprise","look":560,"engine_cues":{"ac":"out"},"engine":{"ad":0.6}}],
 effects=[{"k":"glow","word":"crawled","x":575,"y":300,"r":130,"rgb":"255,190,90","ga":0.55,"par":1.0,"behind":True,"meaning":"the dull amber light where the brothers come out of the earwax"},
  water(600,"the water Vishnu sleeps on")],
 transition_in="iris"))
# 7 ------------------------------------------------------------------ Brahma brings forth the Vedas
S.append(shot("s07",16.02,
 meaning="This happened when Brahma, the creator, brought forth the Vedas.",
 why="Brahma sits on his lotus in gold light; the four Veda books glow into being above him as he opens his arms on 'forth'.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.04,"x":0,"y":20,"r":0},"to":{"z":1.04,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up from the creator to the knowledge he brings"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=OCEAN(640,200,SKY_GOLD),
 mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.05,"_face":0.47,"flip":1,"pose":"sit","emo":"calm","look":640,
   "actions":[{"word":"creator","emo":"joy","d":0.5},{"word":"forth","pose":"open","emo":"pride","e":"spring","d":0.6}]}],
 effects=[{"k":"books","c":-3,"x":640,"y":140,"gap":92,"names":["","","",""],"meaning":"the four Vedas appearing one by one"},
  {"k":"divine_rays","word":"brought","x":640,"y":60,"w":700,"alpha":0.4,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of the revealed Vedas"},
  {"k":"glow","word":"Vedas","x":640,"y":150,"r":260,"rgb":"255,225,150","ga":0.5,"par":0.9,"behind":True,"meaning":"the Vedas shining"}],
 transition_in="fade"))
# 8 ------------------------------------------------------------------ they grow huge
S.append(shot("s08",19.66,
 meaning="The brothers fed on the endless water and grew huge.",
 why="Waist-deep in the bright ocean the two asuras raise their arms on 'fed' and swell larger and larger through the shot, proud on 'huge'.",
 camera={"shot":"wide","lens":"wide","move":"crane_up","from":{"z":1.05,"x":0,"y":24,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"rising with them as they grow"},
 focus={"subject":"madhu","depth":"deep"},vertical={"x":645},
 layers=[far_clouds('#e8f0fa','#ffffff',(500,800)),mid_clouds((430,870)),near_clouds((450,850))],
 background=OCEAN(640,300,SKY_OCEAN),
 mood={"emotion":"menace","grade":"warm"},
 characters=[{"who":"madhu","x":570,"y":560,"s":0.6,"_fix":1,"flip":1,"pose":"stand","emo":"joy","look":"kaitabha","engine":{"ds":0.22},
   "actions":[{"word":"fed","pose":"raise","e":"spring","d":0.6},{"word":"huge","emo":"pride","mood":{"smile":0.6,"ly":-0.3},"d":0.5}]},
  {"who":"kaitabha","x":725,"y":565,"s":0.58,"_fix":1,"flip":-1,"pose":"stand","emo":"joy","look":"madhu","engine":{"ds":0.22},
   "actions":[{"word":"water","pose":"raise","e":"spring","d":0.6},{"word":"huge","emo":"pride","d":0.5}]}],
 effects=[{"k":"wave_ocean","x":470,"y":560,"w":260,"alpha":0.9,"par":1.0,"behind":True,"meaning":"a wave of the endless water they feed on"},
  {"k":"wave_ocean","x":840,"y":565,"w":240,"alpha":0.9,"par":1.0,"behind":True,"flip":-1,"meaning":"the endless water rolling around them"},
  water(520,"the endless water up to their waists")],
 transition_in="wipe"))
# 9 ------------------------------------------------------------------ bow or fight
S.append(shot("s09",22.94,
 meaning="The giant brothers found Brahma on his lotus and ordered him to bow or fight.",
 why="Brahma, small on his lotus, sits in front; the two giants tower behind him, Madhu points down at him and Kaitabha raises his mace as they order him to bow or fight as Brahma shrinks in fear.",
 camera={"shot":"low_angle","lens":"wide","move":"crane_down","from":{"z":1.0,"x":0,"y":-24,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"descending from the giants' faces to the small creator"},
 focus={"subject":"brahma","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#f0dcd0','#fff0e4',(520,780),(200,240)),mid_clouds((430,860),'#e0d4ec',600),near_clouds((450,840))],
 background=OCEAN(640,220,SKY_THREAT),
 mood={"emotion":"threat","grade":"warm"},
 characters=[{"who":"kaitabha","x":535,"y":640,"s":1.3,"_fix":1,"flip":1,"pose":"stand","emo":"anger","look":"brahma",
   "actions":[{"word":"told","pose":"raise","emo":"rage","e":"antic","d":0.5}]},
  {"who":"madhu","x":748,"y":640,"s":1.3,"_fix":1,"flip":-1,"pose":"stand","emo":"pride","mood":{"smile":0.5,"anger":0.5,"ly":0.4},"look":"brahma","talk":0.5,
   "actions":[{"word":"him","pose":"point","emo":"anger","e":"antic","d":0.5}]},
  {"who":"brahma","x":640,"y":690,"s":0.82,"_face":0.5,"flip":1,"pose":"sit","emo":"surprise","look":790,
   "actions":[{"word":"bow","emo":"fear","mood":{"ly":-0.4},"d":0.5}]}],
 effects=[water(650,"the water the giants stand in")],
 transition_in="cut"))
# 10 ----------------------------------------------------------------- silent; they shake the stem
S.append(shot("s10",27.00,
 meaning="Brahma stayed silent, so the brothers shook his lotus stem.",
 why="Close on Brahma with eyes lowered and lips shut; on 'shook' the frame shudders and his face jolts into fear while a giant arm grips the stem behind him.",
 camera={"shot":"close","lens":"tele","move":"handheld","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.02,"x":0,"y":0,"r":0},"shake":5,"motivation":"the shaking stem shakes the whole frame"},
 focus={"subject":"brahma","depth":"shallow"},vertical={"focus":"brahma","z":1.2,"y":0.42},
 layers=[far_clouds('#f0dcd0','#fff0e4',(520,780)),mid_clouds((450,840),'#e0d4ec'),near_clouds((470,820))],
 background=OCEAN(640,220,SKY_THREAT),
 mood={"emotion":"fear","grade":"warm"},
 characters=[{"who":"kaitabha","x":745,"y":690,"s":1.15,"_fix":1,"flip":-1,"pose":"lunge","emo":"rage","dark":0.75,"look":"brahma",
   "actions":[{"word":"shook","emo":"rage","tilt":0.06,"d":0.4}]},
  {"who":"brahma","x":630,"y":690,"s":1.0,"_face":0.42,"flip":1,"pose":"sit","emo":"calm","mood":{"ly":0.6,"smile":0},"look":640,
   "actions":[{"word":"shook","emo":"fear","tilt":-0.08,"e":"spring","d":0.4}]}],
 effects=[water(700,"the water around the lotus")],
 transition_in="cut"))
# 11 ----------------------------------------------------------------- Vedas slip, brothers hide them
S.append(shot("s11",29.70,
 meaning="The Vedas slipped from Brahma's hands and the brothers hid them.",
 why="The four Veda books tumble down from Brahma, who reaches after them in shock; below, Madhu catches them with a sneer and pulls them away on 'hid'.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.05,"x":0,"y":-20,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"the camera falls with the Vedas"},
 focus={"subject":"brahma","depth":"deep"},vertical={"x":650},
 layers=[far_clouds('#f0dcd0','#fff0e4',(520,780)),mid_clouds((440,860),'#e0d4ec'),near_rocks((450,850))],
 background=OCEAN(640,220,SKY_THREAT),
 mood={"emotion":"loss","grade":"warm"},
 characters=[{"who":"madhu","x":800,"y":690,"s":1.1,"_fix":1,"flip":-1,"pose":"stand","emo":"pride","mood":{"smile":0.5,"anger":0.5,"ly":-0.3},"look":"brahma",
   "actions":[{"word":"slipped","pose":"raise","e":"spring","d":0.5},{"word":"hid","pose":"hold","emo":"pride","mood":{"smile":0.7,"lx":0.6},"d":0.6}]},
  {"who":"brahma","x":565,"y":560,"s":0.78,"_face":0.32,"flip":1,"pose":"sit","emo":"surprise","look":760,
   "actions":[{"word":"slipped","pose":"open","emo":"fear","e":"spring","d":0.5}]}],
 effects=[{"k":"books","c":-3,"x":662,"y":335,"gap":66,"fall":35,"names":["","",""],"meaning":"the Vedas tumbling from Brahma's hands"},
  water(690,"the water where the Vedas are hidden")],
 transition_in="cut"))
# 12 ----------------------------------------------------------------- Brahma begs Vishnu
S.append(shot("s12",33.14,
 meaning="Brahma begged Vishnu for help.",
 why="Brahma, alone on his lotus, joins his hands in prayer as he begs and looks down toward the sleeping Vishnu, grief on his faces.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in on his plea"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.1,"y":0.44},
 layers=[far_clouds('#e4e0f4','#f4f0fc',(520,780)),mid_clouds((450,840),'#d4d8f4'),near_clouds((470,820))],
 background=OCEAN(640,230,SKY_DAWN),
 mood={"emotion":"pleading","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.0,"_face":0.44,"flip":1,"pose":"sit","emo":"sad","look":800,
   "actions":[{"word":"Brahma","pose":"sitpray","emo":"grief","mood":{"ly":0.5},"d":0.6}]}],
 effects=[water(700,"the water below his lotus"),
  {"k":"glow","word":"Vishnu","x":640,"y":390,"r":200,"rgb":"255,210,150","ga":0.45,"par":1.0,"behind":True,"meaning":"the warmth of his prayer reaching Vishnu"}],
 transition_in="cut"))
# 13 ----------------------------------------------------------------- Yoga Nidra
S.append(shot("s13",34.76,
 meaning="But Vishnu lay in Yoga Nidra, a trance between waking and sleep.",
 why="Vishnu sleeps on Shesha in moon-silver light; the indigo goddess Nidra hovers faint behind him like a dream and her name appears on 'Nidra'.",
 camera={"shot":"wide","lens":"wide","move":"pan_left","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"a slow drift along the sleeping god"},
 focus={"subject":"vishnu_rest","depth":"deep"},vertical={"x":[640,600]},
 layers=[far_clouds('#e4e0f4','#f4f0fc',(500,800)),mid_clouds((430,860),'#d4d8f4',600),near_clouds((450,850))],
 background=OCEAN(620,200,SKY_NIDRA),
 mood={"emotion":"trance","grade":"cool"},
 characters=[{"who":"nidra","x":700,"y":455,"s":0.8,"_fix":1,"flip":-1,"pose":"open","emo":"calm","mood":{"smile":0.55,"blink":0.45},"look":560,"engine":{"a":0.6}},
  {"who":"vishnu_rest","x":720,"y":600,"s":1.0,"_fix":1,"flip":1,"emo":"calm","mood":{"blink":1},"look":640}],
 effects=[{"k":"name","word":"Nidra","s":"Yoga Nidra","x":620,"y":130,"size":30,"meaning":"the name of the trance as it is spoken"},
  {"k":"halo_ring","word":"trance","x":600,"y":300,"w":420,"alpha":0.4,"blend":"lighter","par":0.9,"behind":True,"meaning":"the moon-silver circle of the trance"},
  water(640,"the cosmic water under Shesha")],
 transition_in="fade"))
# 14 ----------------------------------------------------------------- Nidra releases him
S.append(shot("s14",39.40,
 meaning="Brahma called on the goddess Nidra to release Vishnu.",
 why="Nidra stands before the sleeping Vishnu with folded hands as Brahma calls; on 'release' she opens her arms and begins to fade from him in silver light.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.05,"x":0,"y":20,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up to the goddess as she answers"},
 focus={"subject":"nidra","depth":"deep"},vertical={"focus":"nidra"},
 layers=[far_clouds('#e4e0f4','#f4f0fc',(500,800)),mid_clouds((440,850),'#d4d8f4'),near_clouds((460,820))],
 background=OCEAN(640,200,SKY_NIDRA),
 mood={"emotion":"release","grade":"cool"},
 characters=[{"who":"vishnu_rest","x":790,"y":690,"s":0.6,"_fix":1,"flip":1,"emo":"calm","mood":{"blink":1},"look":640},
  {"who":"nidra","x":620,"y":665,"s":1.05,"_face":0.44,"flip":1,"pose":"namaste","emo":"calm","mood":{"smile":0.55,"blink":0.45},"look":640,"engine_cues":{"fo":"him"},"engine":{"fd":1.0},
   "actions":[{"word":"release","pose":"open","emo":"devotion","e":"spring","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"Nidra","x":620,"y":330,"w":440,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the moon-silver light of the goddess of sleep"},
  {"k":"glow","word":"release","x":620,"y":420,"r":240,"rgb":"200,200,255","ga":0.5,"par":1.0,"behind":True,"meaning":"the trance lifting off Vishnu"}],
 transition_in="cut"))
# 15 ----------------------------------------------------------------- Hayagriva wakes
S.append(shot("s15",41.80,
 meaning="Vishnu woke as Hayagriv, the horse-headed one.",
 why="A white flash and Hayagriva stands in a blazing gold halo; he spreads his arms on 'woke', his eyes flash red on the name, and the name plate appears.",
 camera={"shot":"low_angle","lens":"normal","move":"crane_up","from":{"z":1.08,"x":0,"y":20,"r":0},"to":{"z":1.02,"x":0,"y":0,"r":0},"shake":0,"motivation":"rising with the god as he wakes"},
 focus={"subject":"hayagriva2","depth":"deep"},vertical={"focus":"hayagriva2"},
 layers=[far_clouds('#f4e6d0','#fff4e6',(500,800)),mid_pillars((450,830)),near_clouds((470,810))],
 background=OCEAN(640,220,SKY_GOLD),
 mood={"emotion":"awakening","grade":"warm"},
 characters=[{"who":"hayagriva2","x":640,"y":665,"s":1.0,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"woke","pose":"open","e":"spring","d":0.6},{"word":"Hayagriv","emo":"anger","d":0.6}]}],
 effects=[{"k":"divine_rays","word":"woke","x":640,"y":60,"w":760,"alpha":0.45,"blend":"lighter","par":0.2,"behind":True,"meaning":"the god's waking light"},
  {"k":"name","word":"Hayagriv","s":"Hayagriv","x":640,"y":130,"size":30,"meaning":"the name of the horse-headed form as it is spoken"}],
 transition_in="flash"))
# 16 ----------------------------------------------------------------- the brothers take turns
S.append(shot("s16",45.08,
 meaning="When one brother tired, the other took his place in the fight.",
 why="Stacked: Hayagriva lunges above; below, Madhu sags and fades out on 'tired' and fresh Kaitabha takes his place, mace raised, on 'other'.",
 camera={"shot":"two_shot","lens":"normal","move":"handheld","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.03,"x":0,"y":0,"r":0},"shake":3,"motivation":"the restless frame of an endless fight"},
 focus={"subject":"hayagriva2","depth":"deep"},vertical={"mode":"stack","stack":["hayagriva2","kaitabha"]},
 layers=[far_clouds('#f0dcd0','#fff0e4',(380,860)),mid_clouds((250,1030),'#e8d8f0'),near_clouds((300,980))],
 background=OCEAN(640,260,SKY_FIGHT),
 mood={"emotion":"struggle","grade":"warm"},
 characters=[{"who":"hayagriva2","x":420,"y":650,"s":0.95,"flip":1,"pose":"lunge","emo":"anger","look":"kaitabha",
   "actions":[{"word":"other","emo":"rage","d":0.5}]},
  {"who":"madhu","x":860,"y":660,"s":0.95,"flip":-1,"pose":"stand","emo":"sad","look":"hayagriva2","engine_cues":{"fo":"tired"},"engine":{"fd":0.4},
   "actions":[{"word":"tired","emo":"grief","tilt":-0.08,"d":0.4}]},
  {"who":"kaitabha","x":860,"y":660,"s":0.95,"flip":-1,"pose":"lunge","emo":"rage","look":"hayagriva2","engine_cues":{"ac":"the"},"engine":{"ad":0.2},
   "actions":[{"word":"took","pose":"raise","e":"antic","d":0.5}]}],
 effects=[water(640,"the ocean battlefield")],
 transition_in="cut"))
# 17 ----------------------------------------------------------------- strength will never win
S.append(shot("s17",47.70,
 meaning="Vishnu saw that strength alone would never win this fight.",
 why="Close on Vishnu's face, back in his own form: his eyes narrow in thought and drift sideways on 'saw' as he finds another way.",
 camera={"shot":"close","lens":"tele","move":"static","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"stillness for the moment of realisation"},
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#f0dcd0','#fff0e4',(500,800)),mid_pillars((450,830),'#d8c08a')],
 background=OCEAN(640,240,SKY_FIGHT),
 mood={"emotion":"realisation","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":360,"s":1.15,"flip":1,"head":True,"emo":"calm","mood":{"smile":0,"anger":0.25},"look":640,
   "actions":[{"word":"saw","mood":{"lx":-0.7,"ly":-0.25,"smile":0.05,"anger":0.25},"tilt":-0.04,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 18 ----------------------------------------------------------------- mace down, praise, boon
S.append(shot("s18",49.98,
 meaning="So Vishnu laid down his mace, praised the brothers' power and offered them a boon.",
 why="Vishnu lowers his mace hand and joins his palms on 'praised' in honour of their strength, then opens his hands on 'boon' as a gold halo rises.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.1,"x":0,"y":-8,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pulling back as the battle gives way to an offer"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.1,"y":0.42},
 layers=[far_clouds('#e8eef8','#ffffff'),mid_pillars((470,810),'#e8c878'),near_clouds((470,810))],
 background=OCEAN(640,240,SKY_VAIK),
 mood={"emotion":"humility","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.4,"look":800,
   "actions":[{"word":"praised","pose":"namaste","emo":"devotion","d":0.6},{"word":"boon","pose":"open","emo":"joy","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"boon","x":640,"y":340,"w":460,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the boon offered"},
  {"k":"glow","word":"power","x":640,"y":380,"r":220,"rgb":"255,215,140","ga":0.4,"par":1.0,"behind":True,"meaning":"warm praise of their power"}],
 transition_in="cut"))
# 19 ----------------------------------------------------------------- sneer
S.append(shot("s19",54.08,
 meaning="The brothers sneered at Vishnu's offer.",
 why="The two horned brothers side by side curl their lips and look down their noses on 'sneered'.",
 camera={"shot":"two_shot","lens":"normal","move":"dolly_left","from":{"z":1.15,"x":8,"y":0,"r":0},"to":{"z":1.15,"x":-8,"y":0,"r":0},"shake":0,"motivation":"a sideways slide across two contemptuous faces"},
 focus={"subject":"madhu","depth":"shallow"},vertical={"x":645},
 layers=[far_clouds('#f0dcd0','#fff0e4',(500,800)),mid_clouds((430,860),'#e0d4ec'),near_rocks((450,850))],
 background=OCEAN(640,240,SKY_THREAT),
 mood={"emotion":"contempt","grade":"warm"},
 characters=[{"who":"madhu","x":565,"y":665,"s":0.9,"_face":0.43,"flip":1,"pose":"stand","emo":"pride","look":900,
   "actions":[{"word":"sneered","mood":{"smile":0.55,"anger":0.5,"ly":-0.35},"tilt":-0.05,"d":0.5}]},
  {"who":"kaitabha","x":735,"y":665,"s":0.9,"_ground":True,"flip":-1,"pose":"stand","emo":"pride","look":400,
   "actions":[{"word":"sneered","mood":{"smile":0.55,"anger":0.5,"ly":-0.35},"tilt":0.05,"d":0.5}]}],
 effects=[water(660,"the ocean behind the brothers")],
 transition_in="cut"))
# 20 ----------------------------------------------------------------- victors give boons
S.append(shot("s20",55.58,
 meaning="Victors do not beg for boons, they said; victors give them.",
 why="Madhu speaks with chin high and points to himself on 'Victors', then flings open his hand on 'gave'; Kaitabha behind him laughs.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in on the boast"},
 focus={"subject":"madhu","depth":"deep"},vertical={"focus":"madhu","z":1.1,"y":0.4},
 layers=[far_clouds('#f0dcd0','#fff0e4',(520,800)),mid_clouds((440,860),'#e0d4ec'),near_clouds((460,830))],
 background=OCEAN(640,240,SKY_THREAT),
 mood={"emotion":"arrogance","grade":"warm"},
 characters=[{"who":"kaitabha","x":745,"y":640,"s":0.85,"_fix":1,"flip":-1,"pose":"stand","emo":"joy","dark":0.85,"look":"madhu",
   "actions":[{"word":"said","emo":"joy","mood":{"smile":1,"mouth":0.4},"d":0.5}]},
  {"who":"madhu","x":620,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"pride","talk":0.7,"look":800,
   "actions":[{"word":"Victors","pose":"raise","emo":"pride","mood":{"smile":0.5,"anger":0.5,"ly":-0.3},"e":"spring","d":0.5},{"word":"gave","pose":"open","d":0.5}]}],
 effects=[water(700,"the ocean under the boasting asura")],
 transition_in="cut"))
# 21 ----------------------------------------------------------------- they told him to ask (stack)
S.append(shot("s21",59.08,
 meaning="The brothers told Vishnu to ask for a boon himself.",
 why="Stacked: Kaitabha above holds out an open, mocking hand on 'ask'; Vishnu below listens calmly with a small smile.",
 camera={"shot":"two_shot","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-16,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"from the giver of the boon down to the one who will ask"},
 focus={"subject":"kaitabha","depth":"deep"},vertical={"mode":"stack","stack":["kaitabha","vishnu"]},
 layers=[far_clouds('#f0dcd0','#fff0e4',(380,860)),mid_clouds((250,1030),'#e0d4ec'),near_clouds((300,980))],
 background=OCEAN(640,240,SKY_DAWN),
 mood={"emotion":"irony","grade":"warm"},
 characters=[{"who":"kaitabha","x":860,"y":650,"s":0.95,"flip":-1,"pose":"stand","emo":"pride","talk":0.6,"look":"vishnu",
   "actions":[{"word":"ask","pose":"open","mood":{"smile":0.6,"anger":0.3},"d":0.5}]},
  {"who":"vishnu","x":420,"y":650,"s":0.95,"flip":1,"pose":"stand","emo":"calm","look":"kaitabha",
   "actions":[{"word":"told","mood":{"smile":0.6},"d":0.5}]}],
 effects=[{"k":"glow","x":420,"y":340,"r":200,"rgb":"190,220,255","ga":0.4,"par":1.0,"behind":True,"meaning":"Vishnu's calm light"}],
 transition_in="fade"))
# 22 ----------------------------------------------------------------- grant me that I may kill you both
S.append(shot("s22",60.74,
 meaning="Vishnu asked for his boon: that he may kill them both.",
 why="Vishnu speaks gently and raises a hand on 'Grant'; the Sudarshan chakra spins up above it and his eyes harden on 'kill'.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.1,"x":0,"y":-18,"r":0},"to":{"z":1.1,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilting from the chakra down to the face that asks"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.15,"y":0.42},
 layers=[far_clouds('#e8eef8','#ffffff'),mid_pillars((460,820),'#e8c878'),near_clouds((470,810))],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":240,"change":{"word":"kill","bg2":{"k":"cloudscape","sky":SKY_FIGHT,"sx":640,"sy":240},"d":1.0}},
 mood={"emotion":"resolve","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":800,
   "actions":[{"word":"Grant","pose":"raise","mood":{"smile":0.5},"d":0.6},{"word":"kill","emo":"anger","d":0.5}]}],
 effects=[{"k":"sudarshan_chakra","word":"Grant","x":712,"y":285,"w":64,"alpha":1,"spin":3,"par":1.0,"meaning":"the weapon that will fulfil the boon"}],
 transition_in="cut"))
# 23 ----------------------------------------------------------------- the trap closes
S.append(shot("s23",64.14,
 meaning="The brothers saw they had walked into a trap, but they had given their word.",
 why="A gold yantra circle lights up under the brothers' feet on 'trap'; they recoil in shock, then lower their eyes in shame on 'word'.",
 camera={"shot":"two_shot","lens":"normal","move":"dutch","from":{"z":1.05,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":0,"r":0.04},"shake":0,"motivation":"the tilted frame of a world that has turned on them"},
 focus={"subject":"madhu","depth":"deep"},vertical={"x":645},
 layers=[far_clouds('#e4e0f4','#f4f0fc',(500,800)),mid_clouds((430,860),'#d4d8f4'),near_rocks((450,850))],
 background=OCEAN(640,240,SKY_NIDRA),
 mood={"emotion":"trapped","grade":"cool"},
 characters=[{"who":"madhu","x":570,"y":665,"s":0.9,"_face":0.43,"flip":1,"pose":"stand","emo":"pride","look":"kaitabha",
   "actions":[{"word":"trap","pose":"flee","emo":"surprise","e":"spring","d":0.5},{"word":"word","emo":"shame","d":0.6}]},
  {"who":"kaitabha","x":730,"y":665,"s":0.9,"_ground":True,"flip":-1,"pose":"stand","emo":"pride","look":"madhu",
   "actions":[{"word":"trap","emo":"fear","e":"spring","d":0.5},{"word":"word","emo":"shame","d":0.6}]}],
 effects=[{"k":"magic_circle","word":"trap","x":650,"y":655,"w":360,"alpha":0.8,"blend":"lighter","par":1.0,"behind":True,"meaning":"the trap of their own promise closing around them"}],
 transition_in="cut"))
# 24 ----------------------------------------------------------------- no water
S.append(shot("s24",67.46,
 meaning="They asked to die only where there was no water, thinking the ocean was everywhere.",
 why="Over an endless bright ocean the brothers smirk; Madhu sweeps his hand over the waves on 'where' certain there is no dry place left.",
 camera={"shot":"wide","lens":"wide","move":"crane_up","from":{"z":1.05,"x":0,"y":20,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"rising to show water in every direction"},
 focus={"subject":"madhu","depth":"deep"},vertical={"x":[620,660]},
 layers=[far_clouds('#e8f0fa','#ffffff',(500,800)),mid_clouds((430,870)),near_clouds((450,850))],
 background=OCEAN(640,280,SKY_OCEAN),
 mood={"emotion":"cunning","grade":"warm"},
 characters=[{"who":"madhu","x":580,"y":640,"s":0.85,"_face":0.43,"flip":1,"pose":"stand","emo":"pride","talk":0.5,"look":800,
   "actions":[{"word":"die","mood":{"smile":0.6,"anger":0.3,"ly":-0.3},"d":0.5},{"word":"where","pose":"open","e":"spring","d":0.5}]},
  {"who":"kaitabha","x":735,"y":640,"s":0.85,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"madhu",
   "actions":[{"word":"only","emo":"pride","mood":{"smile":0.7},"d":0.5}]}],
 effects=[{"k":"wave_ocean","x":440,"y":590,"w":240,"alpha":0.9,"par":1.0,"behind":True,"meaning":"waves on every side"},
  {"k":"wave_ocean","x":860,"y":595,"w":220,"alpha":0.9,"par":1.0,"behind":True,"flip":-1,"meaning":"the ocean stretching everywhere"},
  water(590,"water everywhere, no dry place in sight")],
 transition_in="wipe"))
# 25 ----------------------------------------------------------------- blue mountain
S.append(shot("s25",70.50,
 meaning="Vishnu grew until he towered over the waters like a blue mountain.",
 why="Vishnu swells larger through the shot, a blue mountain shape rising behind him above the water, the camera tilting up his height.",
 camera={"shot":"low_angle","lens":"wide","move":"tilt_up","from":{"z":1.0,"x":0,"y":30,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilting up to his growing height"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#e8f0fa','#ffffff',(500,800),(180,220)),mid_clouds((430,860),'#dce8fa',620),near_clouds((450,850))],
 background=OCEAN(640,200,SKY_VAIK),
 mood={"emotion":"majesty","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":0.9,"_fix":1,"flip":1,"pose":"stand","emo":"calm","look":640,"engine":{"ds":0.12},
   "actions":[{"word":"towering","pose":"open","emo":"pride","d":0.8}]}],
 effects=[{"k":"bluemountain","word":"grew","x":640,"y":640,"s":1.1,"d":2.5,"behind":True,"meaning":"Vishnu rising like a blue mountain over the water"},
  water(640,"the waters he towers over")],
 transition_in="cut"))
# 26 ----------------------------------------------------------------- on his thighs
S.append(shot("s26",74.30,
 meaning="Vishnu placed the brothers on his thighs, the only place without water, and beheaded them.",
 why="Vast Vishnu sits above the waves with the two small brothers on his lap; the Sudarshan chakra spins beside him and on 'beheaded' a white flash ends them without blood.",
 camera={"shot":"wide","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in to the end of the trap"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},
 layers=[far_clouds('#e8eef8','#ffffff',(500,800),(180,220)),mid_clouds((430,860),'#dce8fa',640),near_clouds((450,850))],
 background=OCEAN(640,200,SKY_VAIK),
 mood={"emotion":"justice","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":640,"s":1.45,"_face":0.38,"flip":1,"pose":"sit","emo":"calm","look":640,
   "actions":[{"word":"beheaded","emo":"anger","d":0.4}]},
  {"who":"madhu","x":578,"y":492,"s":0.36,"_fix":1,"flip":1,"pose":"stand","emo":"fear","look":"vishnu","engine_cues":{"fo":"beheaded"},"engine":{"fd":0.35}},
  {"who":"kaitabha","x":702,"y":494,"s":0.36,"_fix":1,"flip":-1,"pose":"stand","emo":"fear","look":"vishnu","engine_cues":{"fo":"beheaded"},"engine":{"fd":0.35}}],
 effects=[{"k":"sudarshan_chakra","word":"placed","x":772,"y":330,"w":96,"alpha":1,"spin":4,"par":1.0,"meaning":"the chakra ready to fulfil the boon"},
  {"k":"flash","word":"beheaded","x":640,"y":360,"w":0.35,"meaning":"the stroke that ends the brothers, shown as a flash of light"},
  water(650,"the waters below Vishnu's lap")],
 transition_in="fade"))
# 27 ----------------------------------------------------------------- for killing Madhu
S.append(shot("s27",77.38,
 meaning="Because he killed Madhu...",
 why="Vishnu stands calm with the chakra returning to his raised finger above the quiet water.",
 camera={"shot":"medium","lens":"normal","move":"pan_left","from":{"z":1.05,"x":8,"y":0,"r":0},"to":{"z":1.05,"x":-8,"y":0,"r":0},"shake":0,"motivation":"following the chakra back to its master"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.1,"y":0.42},
 layers=[far_clouds('#f4e6d0','#fff4e6'),mid_pillars((460,820)),near_clouds((470,810))],
 background=OCEAN(640,220,SKY_GOLD),
 mood={"emotion":"victory","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"raise","emo":"calm","look":760,
   "actions":[{"word":"Madhu","emo":"pride","d":0.5}]}],
 effects=[{"k":"sudarshan_chakra","x":722,"y":215,"w":96,"alpha":1,"spin":3,"par":1.0,"meaning":"the chakra coming back after killing Madhu"}],
 transition_in="cut"))
# 28 ----------------------------------------------------------------- Madhusudan
S.append(shot("s28",78.48,
 meaning="Vishnu came to be called Madhusudan, the slayer of Madhu.",
 why="Vishnu in a gold halo with folded hands, the name plate 'Madhusudan' appearing above him as the name is spoken.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.0,"x":0,"y":16,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up to the new name"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#f4e6d0','#fff4e6'),mid_pillars((450,830)),near_clouds((470,810))],
 background=OCEAN(640,200,SKY_GOLD),
 mood={"emotion":"glory","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.05,"_face":0.46,"flip":1,"pose":"stand","emo":"calm","look":640,
   "actions":[{"word":"called","pose":"namaste","emo":"devotion","d":0.6}]}],
 effects=[{"k":"name","word":"called","d":0.4,"s":"Madhusudan","x":640,"y":120,"size":32,"meaning":"his new name, Madhusudan, on screen as it is spoken"},
  {"k":"halo_ring","word":"Vishnu","x":640,"y":330,"w":480,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the glory of the new name"},
  {"k":"divine_rays","x":640,"y":60,"w":700,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of victory"}],
 transition_in="flash"))
# 29 ----------------------------------------------------------------- keep saving us
S.append(shot("s29",80.92,
 meaning="Brahma asked Vishnu to keep saving the world.",
 why="Brahma on his lotus joins his hands and looks up toward Vishnu with hope as he asks, the Vedas back above him.",
 camera={"shot":"medium","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-16,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"descending to the grateful creator"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=OCEAN(640,200,SKY_DAWN),
 mood={"emotion":"gratitude","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.05,"_face":0.47,"flip":1,"pose":"sit","emo":"joy","look":800,
   "actions":[{"word":"asked","pose":"sitpray","emo":"devotion","mood":{"ly":-0.5},"d":0.6}]}],
 effects=[{"k":"books","c":-4,"x":640,"y":150,"gap":100,"names":["","","",""],"meaning":"the Vedas restored to Brahma"},
  {"k":"glow","word":"saving","x":640,"y":400,"r":230,"rgb":"255,215,150","ga":0.45,"par":1.0,"behind":True,"meaning":"the hope of being saved again"}],
 transition_in="fade"))
# 30 ----------------------------------------------------------------- perhaps I did nothing
S.append(shot("s30",83.20,
 meaning="Vishnu humbly said that perhaps he did nothing.",
 why="Close on Vishnu's gentle face: his eyes lower and a soft smile comes on 'nothing'.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"close in on his humility"},
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#f4e6d0','#fff4e6'),mid_pillars((450,830))],
 background=OCEAN(640,240,SKY_DAWN),
 mood={"emotion":"humility","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":360,"s":1.15,"flip":1,"head":True,"emo":"calm","talk":0.5,"look":640,
   "actions":[{"word":"nothing","mood":{"smile":0.7,"ly":0.5,"blink":0.35},"tilt":0.04,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 31 ----------------------------------------------------------------- the universe saved itself
S.append(shot("s31",85.64,
 meaning="Perhaps the universe saved itself through him.",
 why="Vishnu stands small and calm in a vast blue-gold cosmos; a halo ring opens on 'universe' and the light flows through him on 'through'.",
 camera={"shot":"wide","lens":"wide","move":"pull_out","from":{"z":1.12,"x":0,"y":-10,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"final pull out to the scale of the universe"},
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[{"d":"far","contents":"stars and nebula drawn by the cosmos background","fog":0.5,"from_background":True},
   {"d":"mid","contents":"a blue cloud left and a gold cloud right","fog":0.25,"items":[{"o":"cloud","x":480,"y":580,"s":1.2,"col":"#bcd4ff"},{"o":"cloud","x":810,"y":585,"s":1.2,"col":"#ffd8a8"}]},
   near_clouds((470,810))],
 background={"k":"cosmos","rgb":"150,190,255","spin":0.05},
 mood={"emotion":"resolution","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.44,"flip":1,"pose":"open","emo":"calm","look":640,
   "actions":[{"word":"saved","emo":"joy","mood":{"smile":0.6,"blink":0.3},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"universe","x":640,"y":340,"w":560,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"the universe acting through him"},
  {"k":"glow","word":"through","x":640,"y":420,"r":260,"rgb":"255,220,150","ga":0.45,"par":1.0,"behind":True,"meaning":"the light flowing through Vishnu"}],
 transition_in="fade"))
# ---------- durations + narration from the word timings ----------
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
    for f in s['characters']:
        if f.get('head') or f.pop('_fix',None):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        tgt=f.pop('_face',.42)
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None:g=f['y']
for s in S:
    for f in s['characters']:
        for k in('_face','_ground','_fix'):f.pop(k,None)
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel03","format":"vertical","shots":S},open(f'{R}/reels/reel03/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
