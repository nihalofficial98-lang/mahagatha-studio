#!/usr/bin/env python3
"""Generator for reels/reel04/briefs.json "Narada's Maya Test" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel01/briefs_gen.py: every face solved to 38-50% of the 9:16 frame height, narration = the spoken words."""
import json,os
R='/home/user/mahagatha-studio'
W=json.load(open(f'{R}/reels/build/reel04/words.json'))
T=[(w['w'],w['start']) for w in W]
END=82.76
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette (bright, clean) ----------
SKY_VAIK=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']
SKY_VAIK2=['#2a3f9e','#6a8ae0','#d8c8f4','#fff2e0']          # Vaikuntha with a violet tint for "Maya"
SKY_MEM=['#3a2a7a','#7a6ac0','#c8b8ec','#f4ecff']            # dream / memory violet
SKY_RIVER=['#2f6ad0','#7ab8f0','#ffe6c4','#fff8ea']           # bright morning by the river
SKY_SPRING=['#3a78d0','#8ac4f0','#ffd8e4','#fff6f4']
SKY_AUTUMN=['#3a58b0','#d88a5a','#ffc070','#fff0cc']
SKY_GRAY=['#56607a','#8a94aa','#b8c0ce','#e2e6ee']
RIDGE_RIVER=['#a8c4e4','#8ab4cc','#6aa08a','#4a8064']
RIDGE_GRAY=['#a0a8bc','#8890a8','#6e7890','#566078']
RIVER='#5ab8e8'
def far_clouds(haze='#eaf0fa',col='#ffffff',xs=(520,780)):
    return {"d":"far","contents":"soft cloud banks and two hazy peaks of Vaikuntha far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-60,"y":500,"s":1.0,"col":"#9aaad8"},{"o":"mountain","x":xs[1]+40,"y":510,"s":0.85,"col":"#9aaad8"},
                     {"o":"cloud","x":xs[0],"y":230,"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":270,"s":1.1,"col":col}]}
def mid_pillars(xs=(450,830),col='#e8c878',h=520):
    return {"d":"mid","contents":"two gold pillars of Vishnu's hall framing the figure","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810)):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":"#ffffff"}]}
def far_hills(haze='#eef4fa',xs=(500,800),col='#9ab4d4'):
    return {"d":"far","contents":"low blue hills and white clouds in haze on the horizon, above where the river begins","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0],"y":392,"s":1.0,"w":230,"h":120,"col":col,"snow":False},{"o":"mountain","x":xs[1],"y":395,"s":1.0,"w":200,"h":90,"col":col,"snow":False},
                     {"o":"cloud","x":xs[0]+40,"y":200,"s":1.1,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":250,"s":0.9,"col":"#ffffff"}]}
def sand(x=640,y=650,h=50,col='#f4dca8'):
    return {"o":"hill","x":x,"y":y,"s":1.0,"w":620,"h":h,"col":col}
def mid_bank(xs=(440,850),sx=640,tree2='palm',flowers=None,col='#2e7a44'):
    return {"d":"mid","contents":"the sandy river bank with a banyan and a palm","fog":0.18,
            "items":[{"o":"tree","x":xs[0],"y":610,"s":0.8,"kind":"banyan","col":col,**({"flowers":flowers} if flowers else {})},
                     {"o":"tree","x":xs[1],"y":605,"s":0.75,"kind":tree2,"col":col},sand(sx)]}
def near_reeds(xs=(450,830),col='#2a5a3a'):
    return {"d":"near","contents":"dark blurred reeds and shrubs in the bottom corners","dark":0.45,
            "items":[{"o":"shrub","x":xs[0],"y":748,"s":1.5,"col":col,"flowers":"#f0c040"},{"o":"shrub","x":xs[1],"y":750,"s":1.4,"col":col}]}
def hut_item(x=640,y=640,s=1.0,**k):
    d={"o":"hut","x":x,"y":y,"s":s};d.update(k);return d
def river_bg(sky=SKY_RIVER,sx=700,sy=230,**k):
    d={"k":"vista","sky":sky,"sx":sx,"sy":sy,"ridge":RIDGE_RIVER,"river":RIVER,"haze":"240,246,255"};d.update(k);return d
def vaik_bg(sky=SKY_VAIK,sx=640,sy=190):return {"k":"cloudscape","sky":sky,"sx":sx,"sy":sy}
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!"')}};s.update(k);return s
def cam(move,a,b,shot_='medium',lens='normal',shake=0,mot=''):
    z0,x0,y0=a;z1,x1,y1=b
    return {"shot":shot_,"lens":lens,"move":move,"from":{"z":z0,"x":x0,"y":y0,"r":0},"to":{"z":z1,"x":x1,"y":y1,"r":0},"shake":shake,"motivation":mot}
S=[]
# 1 ---------------------------------------------------------------- Vaikuntha, the asker
S.append(shot("s01",0.16,
 meaning="Narada is a great sage, the one who will ask the question.",
 why="Narada stands with his veena in Vishnu's bright blue-gold hall below the title card; he lifts his hand in greeting on 'sage' as soft rays fall on him.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-6),"medium","normal",0,"slow push in to meet the hero of the story"),
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background=vaik_bg(),mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"narada","x":640,"y":690,"s":1.05,"_face":0.52,"flip":1,"pose":"stand","emo":"calm","look":640,"mood":{"smile":0.4},
   "actions":[{"word":"sage","pose":"open","emo":"joy","e":"spring","d":0.6}]}],
 effects=[{"k":"divine_rays","x":640,"y":80,"w":700,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of Vaikuntha where the sage stands"}],
 transition_in="fade"))
# 2 -------------------------------------------------------------- the question
S.append(shot("s02",2.12,
 meaning="Narada asks Vishnu, the preserver, what Maya is.",
 why="The window pans from Narada, hands raised in a question, to blue Vishnu, who turns to him with a knowing smile as 'Maya' is said and a violet glow stirs behind him.",
 camera=cam("pan_right",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan carries the question from Narada to Vishnu"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":[540,760]},
 layers=[far_clouds(xs=(540,780)),{"d":"mid","contents":"gold pillars behind the sage and the god","fog":0.2,"items":[{"o":"pillar","x":390,"y":700,"s":1.0,"col":"#e8c878","h":520},{"o":"pillar","x":910,"y":700,"s":1.0,"col":"#e8c878","h":520}]},near_clouds((440,880))],
 background=vaik_bg(sx=700),mood={"emotion":"curiosity","grade":"warm"},
 characters=[{"who":"narada","x":530,"y":665,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","emo":"doubt","talk":0.6,"look":"vishnu",
   "actions":[{"word":"asked","pose":"plead","emo":"doubt","d":0.6}]},
  {"who":"vishnu","x":770,"y":665,"s":1.0,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"narada",
   "actions":[{"word":"Maya","emo":"joy","mood":{"smile":0.8,"lx":-0.4},"d":0.6}]}],
 effects=[{"k":"glow","word":"Maya","x":770,"y":330,"r":220,"rgb":"200,170,255","ga":0.5,"par":1.0,"behind":True,"meaning":"the mystery of Maya, a soft violet light behind Vishnu"}],
 transition_in="cut"))
# 3 -------------------------------------------------------------- no explanation, a request
S.append(shot("s03",5.56,
 meaning="Vishnu did not explain Maya; instead he asked for water.",
 why="Close on Vishnu: he gives no lecture, only a calm smile, and on 'water' he holds out an open, empty hand.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness: the god says nothing and simply asks"),
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu","z":1.25,"y":0.4},
 layers=[far_clouds(xs=(520,770)),mid_pillars((470,820)),near_clouds((480,800))],
 background=vaik_bg(),mood={"emotion":"calm","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.4,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.6},"look":640,
   "actions":[{"word":"explain","mood":{"smile":0.8,"blink":0.4},"tilt":0.04,"d":0.6},{"word":"water","pose":"open","emo":"calm","d":0.6}]}],
 effects=[],
 transition_in="cut"))
# 4 -------------------------------------------------------------- the answer is that he never brought it
S.append(shot("s04",8.46,
 meaning="Narada never brought the water, and that failure was itself the answer.",
 why="Narada stands alone with empty open hands in a hall turning violet; on 'answer' a pale halo ring opens behind him, the riddle he does not yet understand.",
 camera=cam("pull_out",(1.1,0,-6),(1.0,0,0),"medium","normal",0,"pulling back leaves him small with the unanswered errand"),
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[far_clouds('#ece4fa','#f8f4ff'),mid_pillars(col='#e0c890'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":200,"change":{"word":"answer","bg2":{"k":"cloudscape","sky":SKY_MEM,"sx":640,"sy":200},"d":1.0}},
 mood={"emotion":"mystery","grade":"cool"},
 characters=[{"who":"narada","x":640,"y":665,"s":1.05,"_face":0.43,"flip":1,"pose":"open","emo":"doubt","look":640,
   "actions":[{"word":"never","emo":"shame","mood":{"ly":0.6},"d":0.6},{"word":"answer","emo":"surprise","mood":{"ly":-0.3},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"answer","x":640,"y":330,"w":460,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the hidden answer glowing behind him"}],
 transition_in="iris"))
# 5 -------------------------------------------------------------- flashback: arriving in Vaikuntha
S.append(shot("s05",11.84,
 meaning="Narada had come to Vaikuntha, Vishnu's home.",
 why="Wide on Vaikuntha: a gold temple gateway shines on the clouds and Narada walks in with his veena; the name plate appears as 'Vaikuntha' is said.",
 camera=cam("crane_down",(1.0,0,-24),(1.0,0,0),"establishing","wide",0,"descending from the sky of Vaikuntha to the arriving sage"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[600,660]},
 layers=[{"d":"far","contents":"cloud banks and pale peaks around Vishnu's home","fog":0.55,"haze":"#eef2fa","items":[{"o":"mountain","x":470,"y":500,"s":1.1,"col":"#9aaad8"},{"o":"mountain","x":820,"y":500,"s":0.9,"col":"#9aaad8"},{"o":"cloud","x":520,"y":230,"s":1.3,"col":"#ffffff"}]},
   mid_pillars((450,830),h=480),near_clouds((460,820))],
 background=vaik_bg(sy=200),mood={"emotion":"arrival","grade":"warm"},
 characters=[{"who":"narada","x":560,"y":665,"s":0.9,"_face":0.47,"flip":1,"pose":"stand","emo":"joy","look":700,"walk":{"word":"come","to_x":640,"d":1.6,"speed":1},
   "actions":[{"word":"Vaikuntha","emo":"joy","mood":{"ly":-0.4,"smile":0.7},"d":0.6}]}],
 effects=[{"k":"palace_gate","x":640,"y":420,"w":250,"alpha":0.85,"par":0.4,"behind":True,"meaning":"the gateway of Vaikuntha, Vishnu's home"},
  {"k":"name","word":"Vaikuntha","s":"Vaikuntha","x":640,"y":130,"size":30,"meaning":"the name of Vishnu's home on screen when it is spoken"}],
 transition_in="fade"))
# 6 -------------------------------------------------------------- the news: his curse on Brahma
S.append(shot("s06",14.72,
 meaning="He had come to tell Vishnu how his curse had come true on his own father, Brahma.",
 why="Narada talks eagerly with an open hand; behind him a faint memory of Brahma glows in a rose light, the father his curse came true on.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in as he gets to the news he came to tell"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":620,"z":1.1,"y":0.46},
 layers=[far_clouds('#f4e6ee','#fff4f4',(520,780)),mid_pillars((450,840)),near_clouds((470,820))],
 background=vaik_bg(sky=['#3a4aa8','#8a9ae0','#f0c8d0','#fff2ec']),mood={"emotion":"telling","grade":"warm"},
 characters=[{"who":"brahma","x":735,"y":560,"s":0.55,"_face":0.30,"flip":-1,"pose":"stand","lotus":False,"emo":"sad","look":"narada","engine":{"a":0.45},
   "actions":[{"word":"curse","emo":"grief","mood":{"ly":0.5},"d":0.6}]},
  {"who":"narada","x":545,"y":665,"s":1.0,"_face":0.46,"flip":1,"pose":"stand","emo":"pride","talk":0.7,"look":900,
   "actions":[{"word":"tell","pose":"open","emo":"joy","d":0.6},{"word":"curse","pose":"point","emo":"pride","e":"spring","d":0.5}]}],
 effects=[{"k":"glow","word":"curse","x":735,"y":360,"r":180,"rgb":"255,140,150","ga":0.45,"par":1.0,"behind":True,"meaning":"the curse that came true on Brahma, a rose-red memory light"}],
 transition_in="cut"))
# 7 -------------------------------------------------------------- "it was all Maya"
S.append(shot("s07",18.5,
 meaning="Vishnu smiled and said that it was all Maya.",
 why="Vishnu smiles knowingly; on 'Maya' a violet swirl of light turns behind him and the sky softens to violet.",
 camera=cam("tilt_up",(1.05,0,16),(1.05,0,0),"medium","normal",0,"tilt up to the god who knows the secret"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#ece4fa','#ffffff'),mid_pillars(),near_clouds()],
 background={"k":"cloudscape","sky":SKY_VAIK,"sx":640,"sy":190,"change":{"word":"Maya","bg2":{"k":"cloudscape","sky":SKY_VAIK2,"sx":640,"sy":190},"d":1.0}},
 mood={"emotion":"knowing","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.05,"_face":0.42,"flip":1,"pose":"stand","emo":"calm","talk":0.5,"look":540,
   "actions":[{"word":"smiled","emo":"joy","mood":{"smile":0.9,"lx":-0.4},"d":0.6},{"word":"Maya","pose":"open","d":0.6}]}],
 effects=[{"k":"energy_swirl","word":"Maya","x":640,"y":330,"w":460,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"Maya, the turning illusion, as a violet swirl of light"}],
 transition_in="cut"))
# 8 -------------------------------------------------------------- what does that mean?
S.append(shot("s08",21.6,
 meaning="Narada asked what that meant.",
 why="Close on Narada's face: brows knit in doubt, head tilted, eyes on Vishnu as he asks.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,0),"close","tele",0,"push in on his confusion"),
 focus={"subject":"narada","depth":"shallow"},vertical={"focus":"narada"},
 layers=[far_clouds('#e8ecf8','#ffffff',(500,800)),mid_pillars((450,830)),near_clouds()],
 background=vaik_bg(sky=SKY_VAIK2),mood={"emotion":"doubt","grade":"cool"},
 characters=[{"who":"narada","x":640,"y":360,"s":1.15,"flip":1,"head":True,"emo":"calm","mood":{"surp":0.4,"smile":0},"talk":0.6,"look":900,
   "actions":[{"word":"asked","mood":{"surp":0.6,"ly":-0.2},"tilt":0.07,"d":0.5}]}],
 effects=[],transition_in="cut"))
# 9 -------------------------------------------------------------- "I am thirsty"
S.append(shot("s09",23.54,
 meaning="Vishnu said he was thirsty.",
 why="Vishnu, still smiling, opens his empty hand toward Narada as he says he is thirsty, his eyes on the sage.",
 camera=cam("dolly_left",(1.05,12,0),(1.05,-12,0),"medium","normal",0,"a sideways drift as the god changes the subject"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.1,"y":0.42},
 layers=[far_clouds(xs=(520,780)),mid_pillars((460,830)),near_clouds((470,810))],
 background=vaik_bg(sx=700),mood={"emotion":"calm","grade":"warm"},
 characters=[{"who":"vishnu","x":650,"y":665,"s":1.0,"_face":0.42,"flip":-1,"pose":"stand","emo":"calm","mood":{"smile":0.7},"talk":0.6,"look":420,
   "actions":[{"word":"thirsty","pose":"open","emo":"calm","mood":{"smile":0.5,"ly":0.2},"tilt":-0.04,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 10 ------------------------------------------------------------- go fetch water
S.append(shot("s10",25.32,
 meaning="Vishnu told Narada to fetch some water; then he would answer.",
 why="The window pans from Vishnu pointing out of his hall on 'fetch' to Narada, who bows with folded hands on 'answer', ready to go.",
 camera=cam("pan_left",(1.0,0,0),(1.02,0,0),"two_shot","normal",0,"the pan follows the errand from the god to the sage"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[750,550]},
 layers=[far_clouds(xs=(540,780)),{"d":"mid","contents":"gold pillars behind both","fog":0.2,"items":[{"o":"pillar","x":400,"y":700,"s":1.0,"col":"#e8c878","h":520},{"o":"pillar","x":900,"y":700,"s":1.0,"col":"#e8c878","h":520}]},near_clouds((440,880))],
 background=vaik_bg(sx=640),mood={"emotion":"errand","grade":"warm"},
 characters=[{"who":"vishnu","x":760,"y":665,"s":1.0,"_face":0.42,"flip":-1,"pose":"stand","emo":"calm","talk":0.6,"look":"narada",
   "actions":[{"word":"fetch","pose":"point","emo":"joy","d":0.6}]},
  {"who":"narada","x":540,"y":665,"s":1.0,"_ground":True,"flip":1,"pose":"stand","emo":"calm","look":"vishnu",
   "actions":[{"word":"water","emo":"joy","mood":{"smile":0.6},"d":0.5},{"word":"answer","pose":"namaste","emo":"devotion","d":0.6}]}],
 effects=[],transition_in="cut"))
# 11 ------------------------------------------------------------- to the river
S.append(shot("s11",28.84,
 meaning="Narada walked out of Vaikuntha to the river outside.",
 why="A bright morning river valley: Narada walks along the sandy bank with his veena, the blue river winding behind him.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"wide","wide",0,"the dolly travels with him to the river"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":[560,660]},
 layers=[far_hills(),mid_bank((450,860)),near_reeds((450,840))],
 background=river_bg(),mood={"emotion":"journey","grade":"warm"},
 characters=[{"who":"narada","x":520,"y":665,"s":0.95,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.4},"look":800,"walk":{"word":"walked","to_x":680,"d":1.8,"speed":1},
   "actions":[{"word":"river","emo":"joy","d":0.6}]}],
 effects=[],transition_in="wipe"))
# 12 ------------------------------------------------------------- the young woman
S.append(shot("s12",30.94,
 meaning="By the river bank Narada saw a young woman.",
 why="The window pans from Narada, who stops in surprise, to the young woman in a rose sari standing by the water.",
 camera=cam("pan_right",(1.0,0,0),(1.0,0,0),"two_shot","normal",0,"the pan follows his gaze to her"),
 focus={"subject":"kanya","depth":"deep"},vertical={"x":[540,760]},
 layers=[far_hills(xs=(540,800)),{"d":"mid","contents":"the bank with a flowering tree behind her and a palm","fog":0.18,"items":[{"o":"tree","x":400,"y":605,"s":0.75,"kind":"palm","col":"#2e7a44"},{"o":"tree","x":880,"y":610,"s":0.85,"kind":"round","col":"#3a8a4a","flowers":"#ff9ac0"},sand(660)]},near_reeds((430,900))],
 background=river_bg(sx=760),mood={"emotion":"enchantment","grade":"warm"},
 characters=[{"who":"narada","x":530,"y":665,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":"kanya",
   "actions":[{"word":"saw","emo":"surprise","mood":{"surp":0.7},"d":0.5}]},
  {"who":"kanya","x":770,"y":665,"s":0.98,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"narada","mood":{"smile":0.5,"ly":0.3},
   "actions":[{"word":"woman","mood":{"smile":0.6,"ly":0.4,"lx":-0.4},"tilt":0.05,"d":0.6}]}],
 effects=[],transition_in="cut"))
# 13 ------------------------------------------------------------- so lovely
S.append(shot("s13",33.36,
 meaning="The young woman was so lovely that Narada was captivated.",
 why="Close on her face: a shy smile, eyes lowered, a warm rose glow and a halo of light behind her head.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"close","tele",0,"push in as he is drawn to her"),
 focus={"subject":"kanya","depth":"shallow"},vertical={"focus":"kanya"},
 layers=[far_hills(xs=(520,780)),{"d":"mid","contents":"pink blossoms of a flowering tree beside her","fog":0.25,"items":[{"o":"tree","x":470,"y":600,"s":0.85,"kind":"round","col":"#3a8a4a","flowers":"#ff9ac0"},{"o":"tree","x":830,"y":610,"s":0.8,"kind":"round","col":"#3a8a4a","flowers":"#ffd0e0"}]}],
 background=river_bg(sky=SKY_SPRING,sx=640),mood={"emotion":"love","grade":"warm"},
 characters=[{"who":"kanya","x":640,"y":360,"s":1.15,"flip":-1,"head":True,"emo":"calm","mood":{"smile":0.6,"ly":0.4,"lx":-0.4},
   "actions":[{"word":"lovely","emo":"joy","mood":{"smile":0.8,"ly":0.5,"lx":-0.5},"tilt":0.05,"d":0.6}]}],
 effects=[{"k":"glow","word":"lovely","x":640,"y":330,"r":260,"rgb":"255,190,200","ga":0.5,"par":1.0,"behind":True,"meaning":"her loveliness as a warm rose light"}],
 transition_in="cut"))
# 14 ------------------------------------------------------------- he forgets everything
S.append(shot("s14",34.6,
 meaning="He forgot Vishnu, his errand and his own thirst.",
 why="Narada gazes at her with a dreamy smile while a faint image of Vishnu behind him fades into mist on 'Vishnu' and is gone by 'thirst'.",
 camera=cam("pull_out",(1.08,0,-4),(1.0,0,0),"medium","normal",0,"pulling back as the memory of Vishnu drifts away"),
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[far_hills(xs=(520,800)),mid_bank((440,850),flowers="#ff9ac0"),near_reeds((460,830))],
 background=river_bg(sky=SKY_SPRING,sx=700),mood={"emotion":"enchantment","grade":"warm"},
 characters=[{"who":"vishnu","x":760,"y":540,"s":0.6,"_face":0.32,"flip":-1,"pose":"stand","emo":"calm","mood":{"smile":0.6},"look":"narada","engine":{"a":0.5,"fd":1.6},"engine_cues":{"fo":"Vishnu"}},
  {"who":"narada","x":610,"y":665,"s":1.02,"_face":0.45,"flip":1,"pose":"stand","emo":"joy","mood":{"smile":0.8,"ly":-0.1},"look":900,
   "actions":[{"word":"forgot","mood":{"smile":1,"blink":0.5},"tilt":0.06,"d":0.7}]}],
 effects=[{"k":"mist_wisps","word":"forgot","x":740,"y":380,"w":420,"alpha":0.7,"par":1.0,"meaning":"mist swallowing the memory of Vishnu and the errand"}],
 transition_in="cut"))
# 15 ------------------------------------------------------------- the wedding
S.append(shot("s15",37.9,
 meaning="He married her right there by the river.",
 why="Narada, now a householder in a yellow shawl, and the young woman fold their hands to each other as husband and wife inside a ring of marigold light.",
 camera=cam("push_in",(1.0,0,0),(1.05,0,-4),"two_shot","normal",0,"push in on the vow"),
 focus={"subject":"narada_g","depth":"deep"},vertical={"x":[640,660]},
 layers=[far_hills(xs=(520,780)),{"d":"mid","contents":"two flowering trees on the river bank","fog":0.2,"items":[{"o":"tree","x":440,"y":600,"s":0.85,"kind":"round","col":"#3a8a4a","flowers":"#f0a020"},{"o":"tree","x":850,"y":605,"s":0.8,"kind":"round","col":"#3a8a4a","flowers":"#ff9ac0"},sand(640)]},near_reeds((460,830))],
 background=river_bg(sky=SKY_SPRING),mood={"emotion":"marriage","grade":"warm"},
 characters=[{"who":"narada_g","x":570,"y":665,"s":0.98,"_face":0.44,"flip":1,"pose":"stand","emo":"joy","look":"kanya",
   "actions":[{"word":"married","pose":"namaste","emo":"joy","mood":{"smile":0.9},"d":0.6}]},
  {"who":"kanya","x":730,"y":665,"s":0.96,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"narada_g","mood":{"smile":0.7,"ly":0.3},
   "actions":[{"word":"married","pose":"namaste","emo":"joy","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"married","x":650,"y":360,"w":520,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the sacred ring of the marriage vow"},
  {"k":"glow","word":"married","x":650,"y":400,"r":260,"rgb":"255,200,110","ga":0.45,"par":1.0,"behind":True,"meaning":"marigold light of the wedding"}],
 transition_in="fade"))
# 16 ------------------------------------------------------------- the house on the sand
S.append(shot("s16",39.5,
 meaning="He built a house on the sand by the river.",
 why="Wide: a thatched mud house stands on the sand with the river behind it; Narada opens his arms to show it and his wife smiles at the door.",
 camera=cam("crane_up",(1.06,0,10),(1.0,0,-6),"wide","wide",0,"crane up to show the new home and the river"),
 focus={"subject":"narada_g","depth":"deep"},vertical={"x":[600,660]},
 layers=[far_hills(xs=(500,800)),{"d":"mid","contents":"the thatched house on the sand with a palm beside it","fog":0.12,"items":[hut_item(650,600,1.05),{"o":"tree","x":860,"y":600,"s":0.75,"kind":"palm","col":"#2e7a44"},sand(640,660,40)]},near_reeds((450,840))],
 background=river_bg(sx=760),mood={"emotion":"home","grade":"warm"},
 characters=[{"who":"narada_g","x":560,"y":680,"s":0.85,"_face":0.5,"flip":1,"pose":"stand","emo":"joy","look":700,
   "actions":[{"word":"house","pose":"open","emo":"joy","e":"spring","d":0.6}]},
  {"who":"kanya","x":740,"y":680,"s":0.82,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"narada_g","mood":{"smile":0.7},
   "actions":[{"word":"sand","mood":{"smile":0.9,"ly":-0.2},"d":0.6}]}],
 effects=[{"k":"glow","word":"house","x":650,"y":470,"r":240,"rgb":"255,220,150","ga":0.45,"par":0.55,"behind":True,"meaning":"warm light over the new home"}],
 transition_in="cut"))
# 17 ------------------------------------------------------------- years pass (seasons)
S.append(shot("s17",41.72,
 meaning="Years passed while Narada lived in the house by the river.",
 why="The same house through the seasons: pink spring blossoms drift down, while from 'Years' the sky turns to golden autumn and the light deepens.",
 camera=cam("dolly_left",(1.02,10,0),(1.02,-10,0),"wide","wide",0,"a slow drift like time going by"),
 focus={"subject":"hut","depth":"deep"},vertical={"x":[660,620]},
 layers=[far_hills(xs=(500,800)),{"d":"mid","contents":"the house with a blossom tree and an autumn tree beside it","fog":0.12,"items":[{"o":"tree","x":470,"y":610,"s":0.8,"kind":"round","col":"#3a8a4a","flowers":"#ff9ac0"},hut_item(650,610,1.0,lamp=True),{"o":"tree","x":830,"y":615,"s":0.8,"kind":"round","col":"#d0802a"},sand(640,670,40)]},near_reeds((450,840),'#5a4a2a')],
 background={**river_bg(sky=SKY_SPRING),"change":{"word":"Years","bg2":river_bg(sky=SKY_AUTUMN),"d":1.0}},
 mood={"emotion":"time passing","grade":"warm"},
 characters=[],
 effects=[{"k":"petals","word":"Years","x":640,"y":120,"n":22,"sp":30,"len":560,"meaning":"blossoms falling as the seasons turn"},
  {"k":"glow","word":"passed","x":650,"y":470,"r":160,"rgb":"255,200,120","ga":0.45,"par":1.0,"meaning":"the lamp of the house glowing through the years"}],
 transition_in="fade"))
# 18 ------------------------------------------------------------- a father
S.append(shot("s18",42.92,
 meaning="Narada became a father of a son and a daughter.",
 why="Narada the householder stands before his house with his little son and daughter, opening his arms to them with joy on 'father'.",
 camera=cam("push_in",(1.0,0,0),(1.04,0,-4),"medium","normal",0,"push in on the growing family"),
 focus={"subject":"narada_g","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_hills(xs=(520,790)),{"d":"mid","contents":"the house behind the family and a tree","fog":0.2,"items":[hut_item(820,600,0.9,lamp=True),{"o":"tree","x":440,"y":605,"s":0.75,"kind":"round","col":"#3a8a4a"},sand(640,660,40)]},near_reeds((460,830))],
 background=river_bg(sky=SKY_RIVER,sx=700),mood={"emotion":"family","grade":"warm"},
 characters=[{"who":"narada_g","x":620,"y":665,"s":1.0,"_face":0.38,"flip":1,"pose":"stand","emo":"joy","look":"balak",
   "actions":[{"word":"father","pose":"open","emo":"joy","mood":{"smile":1},"d":0.6}]},
  {"who":"balak","x":755,"y":665,"s":0.84,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"narada_g",
   "actions":[{"word":"father","pose":"open","d":0.6}]},
  {"who":"balika","x":495,"y":665,"s":0.82,"_ground":True,"flip":1,"pose":"stand","emo":"joy","look":"narada_g",
   "actions":[{"word":"father","mood":{"smile":1},"d":0.6}]}],
 effects=[{"k":"glow","word":"father","x":620,"y":380,"r":220,"rgb":"255,225,170","ga":0.4,"par":1.0,"behind":True,"meaning":"the warmth of becoming a father"}],
 transition_in="fade"))
# 18b ------------------------------------------------------------ then a grandfather (same frame, cross-fade = years)
S.append(shot("s18b",44.44,
 meaning="Then Narada became a grandfather.",
 why="A cross-fade in the same place: Narada is now white-bearded and old, the sky has turned autumn gold, and two small grandchildren stand at his side.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"medium","normal",0,"the frame holds still so the dissolve reads as the years passing"),
 focus={"subject":"narada_old","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_hills(xs=(520,790),haze='#fbf0e0'),{"d":"mid","contents":"the same house, now under an autumn tree","fog":0.2,"items":[hut_item(820,600,0.9,lamp=True),{"o":"tree","x":440,"y":605,"s":0.75,"kind":"round","col":"#c88a2a"},sand(640,660,40)]},near_reeds((460,830),'#5a4a2a')],
 background=river_bg(sky=SKY_AUTUMN,sx=700),mood={"emotion":"old age","grade":"warm"},
 characters=[{"who":"narada_old","x":620,"y":665,"s":1.0,"_face":0.38,"flip":1,"pose":"open","emo":"joy","look":"balak",
   "actions":[{"word":"grandfather","mood":{"smile":1,"blink":0.3},"tilt":0.04,"d":0.6}]},
  {"who":"balak","x":740,"y":665,"s":0.72,"_ground":True,"flip":-1,"pose":"open","emo":"joy","look":"narada_old"},
  {"who":"balika","x":505,"y":665,"s":0.7,"_ground":True,"flip":1,"pose":"stand","emo":"joy","look":"narada_old",
   "actions":[{"word":"grandfather","mood":{"smile":1},"d":0.6}]}],
 effects=[{"k":"glow","word":"grandfather","x":620,"y":380,"r":220,"rgb":"255,215,150","ga":0.45,"par":1.0,"behind":True,"meaning":"the golden light of his old age"}],
 transition_in="fade"))
# 19 ------------------------------------------------------------- his whole world
S.append(shot("s19",45.82,
 meaning="The house had become his whole world.",
 why="Old Narada stands before his lamp-lit house with his wife and the children around him; a warm ring of light circles the house: everything he has is here.",
 camera=cam("pull_out",(1.08,0,-6),(1.0,0,0),"wide","wide",0,"pull out until the house is the whole picture of his life"),
 focus={"subject":"narada_old","depth":"deep"},vertical={"x":[640,640]},
 layers=[far_hills(xs=(500,800),haze='#fbf0e0'),{"d":"mid","contents":"the lamp-lit house on the sand","fog":0.12,"items":[hut_item(700,505,0.85,lamp=True),sand(640,620,40)]},near_reeds((450,830),'#4a5a2a')],
 background=river_bg(sky=SKY_AUTUMN,sx=640,sy=260),mood={"emotion":"contentment","grade":"warm"},
 characters=[{"who":"narada_old","x":565,"y":680,"s":0.85,"_face":0.38,"flip":1,"pose":"stand","emo":"joy","look":"kanya",
   "actions":[{"word":"world","pose":"open","emo":"joy","mood":{"smile":1},"d":0.6}]},
  {"who":"kanya","x":665,"y":680,"s":0.82,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"narada_old","mood":{"smile":0.8}},
  {"who":"balak","x":480,"y":680,"s":0.76,"_ground":True,"flip":1,"pose":"open","emo":"joy","look":"narada_old"},
  {"who":"balika","x":770,"y":680,"s":0.74,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"kanya",
   "actions":[{"word":"house","mood":{"smile":1},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"world","x":680,"y":400,"w":520,"alpha":0.4,"blend":"lighter","par":0.9,"behind":True,"meaning":"the house as his whole world, circled in light"}],
 transition_in="cut"))
# 20 ------------------------------------------------------------- the sky turns gray
S.append(shot("s20",48.48,
 meaning="Then one day the sky turned gray.",
 why="Old Narada looks up in unease as the bright sky over the river cross-fades to gray from 'day' to 'gray'.",
 camera=cam("tilt_up",(1.05,0,10),(1.05,0,-6),"medium","normal",0,"tilt up with his eyes to the changing sky"),
 focus={"subject":"narada_old","depth":"deep"},vertical={"focus":"narada_old"},
 layers=[far_hills(xs=(500,800)),{"d":"mid","contents":"the house and a tree on the bank","fog":0.18,"items":[hut_item(820,600,0.9),{"o":"tree","x":460,"y":605,"s":0.75,"kind":"round","col":"#3a7a4a"},sand(640,660,40)]},near_reeds((460,830))],
 background={**river_bg(sky=SKY_RIVER),"change":{"word":"day","bg2":river_bg(sky=SKY_GRAY,ridge=RIDGE_GRAY,river='#7a98b8',haze='220,226,236'),"d":1.2}},
 mood={"emotion":"unease","grade":"cool"},
 characters=[{"who":"narada_old","x":640,"y":665,"s":1.02,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","look":700,
   "actions":[{"word":"sky","emo":"doubt","mood":{"ly":-0.7},"d":0.6},{"word":"gray","emo":"fear","mood":{"ly":-0.6},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 21 ------------------------------------------------------------- thunder, rain, flood
S.append(shot("s21",51.04,
 meaning="Thunder roared, rain poured and the river flooded.",
 why="Rain streaks over the house; a lightning fork flashes far in the sky on 'Thunder', and on 'flooded' a big paper wave of river water rises at the bank as the family huddles.",
 camera=cam("handheld",(1.0,0,0),(1.04,0,0),"wide","wide",2,"a slight tremor of the storm"),
 focus={"subject":"narada_old","depth":"deep"},vertical={"x":[620,660]},
 layers=[{"d":"far","contents":"gray hills under the rain","fog":0.6,"haze":"#9aa4b8","items":[{"o":"hill","x":520,"y":470,"s":1.0,"w":380,"h":90,"col":"#6a7a98"},{"o":"hill","x":800,"y":480,"s":1.0,"w":340,"h":70,"col":"#6a7a98"}]},
   {"d":"mid","contents":"the house on the sand in the storm","fog":0.15,"items":[hut_item(800,600,0.9),sand(640,660,40,'#d8c49a')]},
   {"d":"near","contents":"dark wet reeds in the corners","dark":0.5,"items":[{"o":"shrub","x":450,"y":750,"s":1.5,"col":"#2a4a4a"},{"o":"shrub","x":840,"y":750,"s":1.4,"col":"#2a4a4a"}]}],
 background={"k":"storm","r":0},mood={"emotion":"storm","grade":"cool"},
 characters=[{"who":"narada_old","x":560,"y":665,"s":0.95,"_face":0.38,"flip":1,"pose":"stand","emo":"fear","look":"kanya",
   "actions":[{"word":"Thunder","emo":"fear","mood":{"ly":-0.6},"d":0.5},{"word":"flooded","pose":"flee","emo":"fear","e":"spring","d":0.5}]},
  {"who":"kanya","x":690,"y":665,"s":0.92,"_ground":True,"flip":-1,"pose":"open","emo":"fear","look":"narada_old"},
  {"who":"balak","x":780,"y":665,"s":0.8,"_ground":True,"flip":-1,"pose":"stand","emo":"fear","look":"kanya"}],
 effects=[{"k":"lightning_forks","word":"Thunder","x":560,"y":120,"w":260,"alpha":0.9,"par":0.25,"behind":True,"meaning":"thunder roaring far in the gray sky"},
  {"k":"wave_ocean","word":"flooded","x":860,"y":650,"w":520,"alpha":0.95,"par":1.0,"vy":-10,"meaning":"the river rising over the bank in a flood"}],
 transition_in="fade"))
# 22 ------------------------------------------------------------- swept away
S.append(shot("s22",54.72,
 meaning="The flood water swept his family away.",
 why="A great blue wave rolls across; his wife and children slide away into the water and fade, while old Narada reaches after them in grief.",
 camera=cam("dolly_right",(1.0,-8,0),(1.0,8,0),"medium","normal",0,"the dolly drifts with the water carrying them off"),
 focus={"subject":"narada_old","depth":"deep"},vertical={"x":[610,650]},
 layers=[{"d":"far","contents":"gray hills under the rain","fog":0.6,"haze":"#9aa4b8","items":[{"o":"hill","x":560,"y":470,"s":1.0,"w":420,"h":90,"col":"#6a7a98"}]},
   {"d":"mid","contents":"the bank half under water","fog":0.15,"items":[sand(560,670,30,'#d8c49a')]},
   {"d":"near","contents":"dark wet reeds in the corners","dark":0.5,"items":[{"o":"shrub","x":440,"y":752,"s":1.5,"col":"#2a4a4a"}]}],
 background={"k":"storm","r":0},mood={"emotion":"loss","grade":"cool"},
 characters=[{"who":"narada_old","x":520,"y":665,"s":0.98,"_face":0.38,"flip":1,"pose":"stand","emo":"grief","look":"kanya",
   "actions":[{"word":"swept","pose":"open","emo":"grief","e":"spring","d":0.5},{"word":"away","emo":"grief","tilt":-0.06,"d":0.6}]},
  {"who":"kanya","x":670,"y":665,"s":0.9,"_ground":True,"flip":-1,"pose":"open","emo":"fear","look":"narada_old","engine_cues":{"mc":"swept","fo":"family"},"engine":{"mx":170,"my":-20,"md":1.8,"fd":1.4}},
  {"who":"balika","x":750,"y":665,"s":0.8,"_ground":True,"flip":-1,"pose":"open","emo":"fear","look":"narada_old","engine_cues":{"mc":"swept","fo":"family"},"engine":{"mx":160,"my":-30,"md":1.5,"fd":1.3}}],
 effects=[{"k":"wave_ocean","x":800,"y":640,"w":560,"alpha":0.95,"par":1.0,"vx":30,"meaning":"the flood wave rolling over the family"},
  {"k":"water_splash","word":"swept","x":700,"y":600,"w":220,"alpha":0.85,"par":1.0,"meaning":"spray where the water takes them"}],
 transition_in="cut"))
# 23 ------------------------------------------------------------- suddenly back in Vaikuntha
S.append(shot("s23",56.98,
 meaning="Suddenly Narada was back in Vaikuntha, standing before Vishnu.",
 why="A white flash and the storm is gone: stacked, Vishnu above in the bright hall smiles; below, young Narada with his veena stands blinking in surprise.",
 camera=cam("crane_down",(1.0,0,-16),(1.0,0,0),"two_shot","normal",0,"from Vishnu down to the sage who has just woken"),
 focus={"subject":"narada","depth":"deep"},vertical={"mode":"stack","stack":["vishnu","narada"]},
 layers=[far_clouds(xs=(380,860)),mid_pillars((250,1030)),near_clouds((300,980))],
 background=vaik_bg(),mood={"emotion":"awakening","grade":"warm"},
 characters=[{"who":"vishnu","x":800,"y":650,"s":0.95,"flip":-1,"pose":"stand","emo":"calm","mood":{"smile":0.8},"look":"narada",
   "actions":[{"word":"Vishnu","emo":"joy","mood":{"smile":0.9},"d":0.6}]},
  {"who":"narada","x":460,"y":665,"s":0.95,"flip":1,"pose":"stand","emo":"surprise","look":"vishnu",
   "actions":[{"word":"Suddenly","emo":"surprise","mood":{"surp":1},"d":0.4},{"word":"standing","emo":"fear","mood":{"ly":-0.3},"d":0.6}]}],
 effects=[{"k":"glow","x":800,"y":330,"r":220,"rgb":"190,220,255","ga":0.45,"par":1.0,"behind":True,"meaning":"Vishnu's calm light in Vaikuntha"}],
 transition_in="flash"))
# 24 ------------------------------------------------------------- where is the water?
S.append(shot("s24",60.88,
 meaning="Vishnu asks where the water is: he had said he was thirsty.",
 why="Vishnu holds out his empty open hand and asks with a gentle teasing smile; his eyes rest on Narada.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the simple question that holds the whole lesson"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu","z":1.12,"y":0.42},
 layers=[far_clouds(xs=(520,780)),mid_pillars((460,830)),near_clouds((470,810))],
 background=vaik_bg(),mood={"emotion":"gentle irony","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.0,"_face":0.42,"flip":-1,"pose":"stand","emo":"calm","talk":0.6,"look":420,"mood":{"smile":0.7},
   "actions":[{"word":"water","pose":"open","emo":"joy","mood":{"smile":0.8},"d":0.6},{"word":"thirsty","tilt":0.05,"mood":{"smile":0.9,"blink":0.3},"d":0.6}]}],
 effects=[],transition_in="cut"))
# 25 ------------------------------------------------------------- stunned
S.append(shot("s25",64.819,
 meaning="Narada stood stunned.",
 why="Close on Narada's face staring straight ahead, mouth open in shock, a pale ring of light behind his head: he understands no time has passed.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"close","tele",0,"stillness: he cannot move"),
 focus={"subject":"narada","depth":"shallow"},vertical={"focus":"narada"},
 layers=[far_clouds('#e8ecf8','#ffffff',(500,800)),mid_pillars((450,830)),near_clouds()],
 background=vaik_bg(sky=SKY_VAIK2),mood={"emotion":"shock","grade":"cool"},
 characters=[{"who":"narada","x":640,"y":340,"s":1.15,"flip":1,"head":True,"emo":"surprise","mood":{"surp":1,"mouth":0.7,"ly":0,"lx":0},
   "actions":[{"word":"stood","emo":"surprise","mood":{"surp":1,"mouth":0.8,"ly":0,"lx":0},"d":0.4}]}],
 effects=[{"k":"halo_ring","word":"stunned","x":640,"y":300,"w":520,"alpha":0.4,"blend":"lighter","par":0.9,"behind":True,"meaning":"the shock of waking from the dream, a pale ring of light"}],transition_in="cut"))
# 26 ------------------------------------------------------------- none of it was real
S.append(shot("s26",66.54,
 meaning="His wife, his children and his home: none of it had been real.",
 why="A violet dream: his wife, then his son and daughter float faintly in the mist beside the house as each is named, then dissolve away on 'none'.",
 camera=cam("pull_out",(1.06,0,-6),(1.0,0,0),"wide","normal",0,"pulling back as the dream thins out"),
 focus={"subject":"kanya","depth":"deep"},vertical={"x":[640,640]},
 layers=[{"d":"far","contents":"violet dream clouds","fog":0.6,"haze":"#e8e0fa","items":[{"o":"cloud","x":520,"y":230,"s":1.3,"col":"#f4eeff"},{"o":"cloud","x":780,"y":280,"s":1.1,"col":"#f4eeff"}]},
   {"d":"mid","contents":"the faint house of the dream on a pale sand bank","fog":0.45,"haze":"#e0d8f4","items":[hut_item(650,560,0.9),sand(640,640,40,'#e8d8c0')]},
   near_clouds((470,820))],
 background={"k":"cloudscape","sky":SKY_MEM,"sx":640,"sy":220},mood={"emotion":"unreal","grade":"cool"},
 characters=[{"who":"kanya","x":590,"y":665,"s":0.92,"_face":0.39,"flip":1,"pose":"stand","emo":"calm","mood":{"smile":0.6,"blink":0.3},"look":700,
   "engine_cues":{"ac":"wife","fo":"none"},"engine":{"ad":0.6,"fd":1.0}},
  {"who":"balak","x":720,"y":665,"s":0.78,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"kanya","engine_cues":{"ac":"children","fo":"none"},"engine":{"ad":0.5,"fd":1.0}},
  {"who":"balika","x":790,"y":665,"s":0.76,"_ground":True,"flip":-1,"pose":"stand","emo":"joy","look":"kanya","engine_cues":{"ac":"children","fo":"none"},"engine":{"ad":0.5,"fd":1.0}}],
 effects=[{"k":"mist_wisps","word":"home","x":640,"y":560,"w":520,"alpha":0.8,"par":1.0,"meaning":"the dream mist the whole family is made of"},
  {"k":"glow","word":"real","x":640,"y":380,"r":260,"rgb":"220,200,255","ga":0.5,"par":1.0,"behind":True,"meaning":"the empty light left when the dream is gone"}],
 transition_in="iris"))
# 27 ------------------------------------------------------------- that was Maya
S.append(shot("s27",71.06,
 meaning="Vishnu explains that this was Maya: attachment to a world that does not last.",
 why="Vishnu speaks with an open teaching hand inside a violet swirl; the name 'Maya' appears and on 'last' a small faint house drifts behind him and is gone.",
 camera=cam("tilt_down",(1.06,0,-20),(1.04,0,0),"medium","normal",0,"tilting down from the light to the god who explains"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#ece4fa','#ffffff'),mid_pillars(col='#e8c8a0'),near_clouds()],
 background=vaik_bg(sky=SKY_VAIK2),mood={"emotion":"teaching","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.05,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":540,"mood":{"smile":0.5},
   "actions":[{"word":"Maya","pose":"open","emo":"calm","d":0.6},{"word":"last","emo":"sad","mood":{"ly":0.3,"smile":0.3},"tilt":-0.04,"d":0.6}]}],
 effects=[{"k":"energy_swirl","word":"Maya","x":640,"y":330,"w":460,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"Maya as a turning violet light"},
  {"k":"name","word":"Maya","s":"Maya","x":640,"y":120,"size":32,"meaning":"the word Maya on screen as Vishnu names it"}],
 transition_in="fade"))
# 28 ------------------------------------------------------------- slips away like sand
S.append(shot("s28",75.74,
 meaning="Maya makes us chase what slips away like sand.",
 why="Young Narada on the empty river bank reaches out; a stream of golden sand blows out of his open hands and away from him.",
 camera=cam("dolly_left",(1.04,10,0),(1.04,-10,0),"medium","normal",0,"a drift that follows the sand blowing away"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":620,"z":1.08,"y":0.44},
 layers=[far_hills(xs=(520,800),haze='#f4eefa'),{"d":"mid","contents":"the empty sand bank where the house stood","fog":0.2,"items":[{"o":"tree","x":450,"y":605,"s":0.75,"kind":"palm","col":"#2e7a44"},sand(640,660,50)]},near_reeds((460,830))],
 background=river_bg(sky=['#3a5ab8','#9ab0e8','#f4d8c8','#fff4ea'],sx=760),mood={"emotion":"longing","grade":"warm"},
 characters=[{"who":"narada","x":560,"y":665,"s":1.0,"_face":0.45,"flip":1,"pose":"stand","emo":"sad","look":800,
   "actions":[{"word":"chase","pose":"open","emo":"sad","d":0.6},{"word":"slips","mood":{"ly":-0.3},"emo":"grief","d":0.6}]}],
 effects=[{"k":"sand_drift","word":"chase","x":665,"y":445,"w":200,"alpha":1,"par":1.0,"meaning":"grains of golden sand slipping out of his reach and blowing away"}],
 transition_in="wipe"))
# 29 ------------------------------------------------------------- much more Maya to come
S.append(shot("s29",78.62,
 meaning="Vishnu smiles and warns Narada that much more Maya is still to come.",
 why="Vishnu smiles warmly and raises a warning hand on 'warned'; a violet swirl and halo open behind him on 'Maya' as the camera pulls away.",
 camera=cam("pull_out",(1.12,0,-8),(1.0,0,0),"wide","wide",0,"final pull out: the lesson is only beginning"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},
 layers=[far_clouds('#ece4fa','#ffffff'),mid_pillars(),near_clouds()],
 background=vaik_bg(sky=SKY_VAIK2),mood={"emotion":"promise","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":665,"s":1.05,"_face":0.42,"flip":1,"pose":"stand","emo":"joy","mood":{"smile":0.9},"talk":0.5,"look":540,
   "actions":[{"word":"smiled","mood":{"smile":1},"d":0.6},{"word":"warned","pose":"raise","emo":"calm","mood":{"smile":0.7},"d":0.6}]}],
 effects=[{"k":"energy_swirl","word":"Maya","x":640,"y":330,"w":480,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"more Maya to come, the violet swirl returning"},
  {"k":"halo_ring","word":"smiled","x":640,"y":330,"w":520,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"Vishnu's divine knowing"}],
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
    cam_={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        if f['who'] in('balak','balika'):continue   # children stand on the adults' ground; their faces are checked in the stills
        y0=f['y']
        while VB.face_cropped_v(f,cam_,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
for i,s_ in enumerate(S):s_['id']=f"s{i+1:02d}"
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel04","format":"vertical","shots":S},open(f'{R}/reels/reel04/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
