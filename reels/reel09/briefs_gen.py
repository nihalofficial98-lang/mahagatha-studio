#!/usr/bin/env python3
"""reels/reel09/briefs.json "Why Did Shiva Run From His Own Devotee?" (data; helpers reels/briefs_lib.py)"""
import sys;sys.path.insert(0,'/home/user/mahagatha-studio/reels')
from briefs_lib import *
G=Gen('reel09');A=G.shot
SKY_DUSK=['#2a2a6a','#6a5aa8','#e49a9a','#ffd8a8']
SKY_HOT=['#6a2a3a','#c8604a','#ffa86a','#ffe4b0']
SKY_DAY=['#2466c8','#6ab0ee','#c8ecfa','#fff8e8']
SKY_NITE=['#0e1240','#3a3a8a','#8a78b8','#e8c8c0']
SKY_VK=['#2a5cc4','#7ab0ee','#ffdca8','#fff6e2']
def kail():return bg("kailash",mx=.42)
def vk():return bg("vaikuntha",sx=640,sy=250)
def vista(sky=SKY_DAY,ridge=['#a8c4e4','#8ab4cc','#6aa08a','#4a8064'],**k):
    d=bg("vista",sky=sky,sx=640,sy=300,ridge=ridge,haze="240,244,255",dust=12);d.update(k);return d
def L_kail():return [far("pale snow peaks and cloud banks far behind",[mtn(470,470,1.0,'#b4c4e8',260,170,True),mtn(840,480,.9,'#b4c4e8',240,150,True),cld(520,220,1.2)],'#eef2fc',.55),
    mid("a snowy ledge on the Kailash slope with pines",[ground(480,'#e8eefc',1100,12),tree(420,520,.6,"pine",'#2e5a4a'),tree(880,516,.55,"pine",'#2e5a4a')],.15),
    near("snow-dusted rocks low in the bottom corners",[{"o":"rock","x":440,"y":752,"s":1.6,"col":"#8a96b0"},{"o":"rock","x":840,"y":756,"s":1.5,"col":"#8a96b0"}],.4)]
def L_forest(h='#e8d8c8',col='#4a7a5a'):return [far("hazy forest hills far behind",[mtn(470,470,1.0,'#8aa0a0',260,150),mtn(840,480,.9,'#8aa0a0',240,130),cld(520,220,1.1,'#fff0e0')],h,.55),
    mid("a dusty forest ground with trees",[ground(480,'#b89a68',1100,12),tree(410,520,.62,"round",col),tree(880,516,.58,"round",col)],.15),
    near("dark leaves and shrubs low in the corners",[shrub(450,752,1.5,'#2a4a38','#e0a040'),shrub(830,752,1.4,'#2a4a38')],.45)]
def L_vk():return [far("a golden palace and pale clouds far behind",[cld(500,230,1.2,'#fff4dc'),cld(800,270,1.0,'#fff4dc'),mtn(470,470,.9,'#d8b88a',200,120)],'#fff0d4',.5),
    mid("lotus-dotted golden shore of the milk ocean",[ground(470,'#f2dca8',1100,12),cld(430,640,1.5,'#fff8ec'),cld(850,650,1.4,'#fff8ec')],.15),
    near("golden lotus leaves low in the corners",[shrub(450,752,1.5,'#3a7a54','#ffd0e0'),shrub(830,752,1.4,'#3a7a54','#ffe8b0')],.35)]
def L_cloud():return [far("pale peaks and white clouds far behind",[mtn(470,470,1.0,'#9aaad8'),mtn(830,480,.85,'#9aaad8'),cld(520,220,1.3),cld(790,270,1.0)],'#eef2fa'),
    mid("a bank of white clouds at the figures' feet",[cld(480,640,1.6),cld(810,650,1.5,'#f4f6ff')]),near("white cloud puffs low in the bottom corners",[cld(450,750,1.7),cld(830,752,1.6)],.1)]
def L_desert():return [far("red-brown hills in haze far behind",[mtn(470,470,1.0,'#b87a6a',260,150),mtn(840,480,.9,'#b87a6a',240,130),cld(520,220,1.1,'#ffd8b0')],'#f0c8a8',.55),
    mid("a dry road across red earth with rocks",[ground(480,'#c08a5a',1100,12),{"o":"rock","x":430,"y":520,"s":.8,"col":"#8a5a3a"},{"o":"rock","x":870,"y":516,"s":.7,"col":"#8a5a3a"}],.15),
    near("dark rocks low in the corners",[{"o":"rock","x":440,"y":752,"s":1.6,"col":"#4a2a22"},{"o":"rock","x":840,"y":756,"s":1.5,"col":"#4a2a22"}],.5)]
GLD="255,214,140"
# 1
A("Why did Shiva",meaning="The question: why did Shiva, the destroyer of worlds, run for his life from a demon he had blessed himself?",
 why="Shiva runs in fear across the Kailash snow with his hair and tiger skin flying and a worried face; the title card sits above him.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-6),"medium","normal",0,"a slow push in on the god who is afraid"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_kail(),background=kail(),mood={"emotion":"fear","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":.52,"flip":1,"pose":"flee","emo":"fear","look":560,"actions":[{"word":"destroyer","pose":"flee","emo":"surprise","d":.5}]}],
 effects=[pfx("sand_drift","run",420,640,420,"snow blowing past the running god",alpha=.5)],transition_in="fade")
# 2
A("The demon's gift",meaning="The demon's gift could turn anyone to ash.",
 why="Bhasmasura raises his glowing right hand and stares with red eyes; ash grey sparks drift off his hand on 'ash'.",
 camera=cam("tilt_up",(1.0,0,10),(1.08,0,-2),"medium","normal",0,"tilting up to the dangerous hand"),
 focus={"subject":"bhasmasura","depth":"deep"},vertical={"focus":"bhasmasura"},layers=L_desert(),background=vista(SKY_HOT,['#b87a6a','#9a5a5a','#7a4a4a','#5a3a3a']),mood={"emotion":"menace","grade":"warm"},
 characters=[{"who":"bhasmasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"raise","emo":"anger","look":700,"engine":{"hand":1},"actions":[{"word":"ash","emo":"rage","d":.5}]}],
 effects=[pfx("embers","ash",640,420,300,"grey sparks rising from the boon hand",alpha=.6)],transition_in="cut")
# 3
A("and only Vishnu",meaning="Only Vishnu could save Shiva.",
 why="Vishnu stands calm in a golden light with a hand raised in protection while Shiva stands anxious beside him.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","normal",0,"a slide across the one who can save and the one who needs saving"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"hope","grade":"warm"},
 characters=[{"who":"shiva","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"plead","emo":"fear","look":720,"actions":[{"word":"save","emo":"fear","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"open","emo":"calm","look":560,"actions":[{"word":"Vishnu","emo":"calm","d":.5}]}],
 effects=[glow("Vishnu",735,300,230,GLD,.4,"the golden light around Vishnu")],transition_in="cut")
# 4
A("Vishnu needed a trick",meaning="Vishnu needed a trick to do it.",
 why="A close Vishnu with a sly quiet smile and eyes glancing sideways, a pale halo behind his head.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"close","tele",0,"push in on the smile that hides a plan"),
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu"},layers=L_vk(),background=vk(),mood={"emotion":"cunning","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":300,"s":.8,"head":True,"flip":1,"pose":"stand","emo":"calm","look":600,"mood":{"smile":.7,"lx":-.6},"actions":[{"word":"trick","emo":"calm","mood":{"smile":.9,"lx":-.7,"blink":.3},"d":.6}]}],
 effects=[pfx("halo_ring","trick",640,320,360,"the halo of a god with a plan",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 5
A("The demon was Vrikasura",meaning="The demon was called Vrikasura.",
 why="Vrikasura, a thin ascetic demon with small horns and matted hair, stands with folded hands and a humble face; his name appears on 'Vrikasura'.",
 camera=cam("static",(1.04,0,0),(1.04,0,0),"medium","normal",0,"the camera rests on the introduction"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_forest(),background=vista(SKY_DAY),mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"namaste","emo":"devotion","look":700,"actions":[{"word":"Vrikasura","emo":"devotion","d":.5}]}],
 effects=[name("Vrikasura","Vrikasura",640,128,32)],transition_in="cut")
# 6
A("The sage Narada",meaning="The sage Narada told him to win a boon, a gift from a god.",
 why="Narada with his veena smiles and points a finger up toward the sky while Vrikasura listens with folded hands, nodding.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"sliding from the adviser to the listener"),
 focus={"subject":"narada","depth":"deep"},vertical={"x":640},layers=L_forest(),background=vista(SKY_DAY),mood={"emotion":"advice","grade":"warm"},
 characters=[{"who":"narada","x":735,"y":690,"s":.85,"_face":.43,"flip":-1,"pose":"point","emo":"joy","look":560,"actions":[{"word":"boon","emo":"joy","mood":{"smile":.8},"d":.5}]},
   {"who":"vrikasura","x":545,"y":690,"s":.85,"_face":.44,"flip":1,"pose":"namaste","emo":"devotion","look":720,"actions":[{"word":"gift","emo":"joy","d":.5}]}],
 effects=[glow("boon",640,260,200,GLD,.3,"a faint gold light of the promised boon")],transition_in="cut")
# 7
A("He prayed for hundreds",meaning="He prayed for hundreds of years.",
 why="Vrikasura sits cross-legged with closed eyes and folded hands in deep prayer while fallen leaves drift by to show passing years.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"a slow push in shows time passing around his stillness"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_forest('#e0c8b0'),background=vista(SKY_DUSK),mood={"emotion":"patience","grade":"warm"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"devotion","mood":{"blink":1},"look":640,"actions":[{"word":"years","emo":"devotion","d":.5}]}],
 effects=[pfx("sand_drift","hundreds",420,560,420,"dry leaves and dust drifting by as years pass",alpha=.5),glow("prayed",640,330,230,GLD,.3,"the quiet glow of tapasya")],transition_in="cut")
# 8
A("Shiva did not come",meaning="Shiva did not come, so he started cutting off his own flesh.",
 why="Vrikasura opens his eyes with a sad hurt face, then lifts a sword toward his body on 'cutting' in a grim, desperate pose.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back leaves him alone and desperate"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_forest('#e0c8b0'),background=vista(SKY_DUSK),mood={"emotion":"despair","grade":"cool"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"sad","look":700,"prop":"sword","actions":[{"word":"started","pose":"selfcut","emo":"grief","d":.6}]}],
 effects=[],transition_in="cut")
# 9
A("As his sword",meaning="As his sword reached his neck, Shiva caught his arm.",
 why="Vrikasura holds the sword level at his own neck at the left while Shiva steps in from the right and grips his arm with a firm calm face.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"two_shot","normal",2,"a quick shaky push at the moment of rescue"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"x":640},layers=L_kail(),background=kail(),mood={"emotion":"rescue","grade":"cool"},
 characters=[{"who":"vrikasura","x":545,"y":690,"s":.82,"_face":.46,"flip":1,"pose":"selfcut","prop":"sword","emo":"grief","look":640,"actions":[{"word":"neck","emo":"grief","d":.4}]},
   {"who":"shiva","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"point","emo":"calm","look":560,"actions":[{"word":"caught","emo":"surprise","d":.4}]}],
 effects=[{"k":"flash","word":"caught","x":640,"y":340,"meaning":"a white flash as Shiva catches the arm"}],transition_in="flash")
# 10
A("\"Make me magical,\"",meaning="Make me magical, said the demon.",
 why="Vrikasura kneels and pleads with open eyes and hands pressed together, looking up at Shiva.",
 camera=cam("dolly_right",(1.0,-10,0),(1.04,10,0),"medium","normal",0,"a slide across the demand"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_kail(),background=kail(),mood={"emotion":"desire","grade":"cool"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"plead","emo":"devotion","look":720,"talk":.8,"actions":[{"word":"said","emo":"joy","d":.5}]}],
 effects=[],transition_in="cut")
# 11
A("\"Anyone I touch",meaning="Anyone he touches on the head turns to ash.",
 why="The demon points a glowing hand at his own head, ash-grey light and drifting sparks around it, with a greedy smile.",
 camera=cam("tilt_up",(1.0,0,10),(1.08,0,-2),"medium","normal",0,"rising to the hand that will turn everything to ash"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_kail(),background=kail(),mood={"emotion":"greed","grade":"cool"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"devotion","look":700,"talk":.7,"actions":[{"word":"touch","pose":"plead","emo":"joy","d":.5},{"word":"ash.\"","pose":"namaste","emo":"devotion","d":.5}]}],
 effects=[glow("touch",640,330,220,"200,200,210",.3,"a grey light for the ash that the boon will make")],transition_in="cut")
# 12
A("\"But that is cruel,\"",meaning="But that is cruel, said Shiva.",
 why="Shiva frowns with worried eyes and a raised hand, shaking his head slowly at the demand.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back as he hesitates"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_kail(),background=kail(),mood={"emotion":"doubt","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"surprise","look":560,"talk":.8,"tilt":-.05,"actions":[{"word":"Shiva","emo":"calm","tilt":.05,"d":.5}]}],
 effects=[],transition_in="cut")
# 13
A("\"If you give it,",meaning="If you give it, it proves you love me.",
 why="Vrikasura clasps his hands and looks up with a pleading smile that shows devotion, a light glow around him.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the devotion that is used as a lever"),
 focus={"subject":"vrikasura","depth":"deep"},vertical={"focus":"vrikasura"},layers=L_kail(),background=kail(),mood={"emotion":"pleading","grade":"cool"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"namaste","emo":"devotion","look":720,"talk":.8,"mood":{"smile":.4},"actions":[{"word":"love","emo":"joy","mood":{"smile":.6},"d":.5}]}],
 effects=[glow("love",640,320,220,"255,200,160",.3,"a warm pleading glow")],transition_in="cut")
# 14
A("Shiva agreed",meaning="Shiva agreed to give the boon the demon asked for.",
 why="Shiva lowers his head in a slow sad nod with one open hand giving the blessing, light spilling from his palm.",
 camera=cam("tilt_down",(1.0,0,-8),(1.04,0,4),"medium","normal",0,"tilting down with the heavy nod"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_kail(),background=kail(),mood={"emotion":"consent","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"sad","look":600,"tilt":.06,"actions":[{"word":"agreed","emo":"calm","tilt":.08,"d":.5}]}],
 effects=[pfx("light_beam","agreed",640,330,480,"light from Shiva's blessing hand",alpha=.4,blend="lighter",behind=True)],transition_in="cut")
# 15
A("He named him",meaning="He named him Bhasmasura, the ash demon.",
 why="The ascetic now stands as Bhasmasura with horns, red eyes and ash streaks and a glowing right hand, his name on the screen as a violet swirl rises.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the new form"),
 focus={"subject":"bhasmasura","depth":"deep"},vertical={"focus":"bhasmasura"},layers=L_kail(),background=kail(),mood={"emotion":"power","grade":"cool"},
 characters=[{"who":"vrikasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"devotion","look":700,"engine_cues":{"fo":"Bhasmasura,"},"engine":{"fd":.8},"actions":[]},
   {"who":"bhasmasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"pride","look":700,"engine":{"a":0},"engine_cues":{"ac":"Bhasmasura,"},"actions":[{"word":"ash","emo":"anger","d":.5}]}],
 effects=[name("Bhasmasura,","Bhasmasura",640,128,32),pfx("energy_swirl","named",640,340,420,"a swirl of energy as the new name is given",alpha=.45,blend="lighter",behind=True)],transition_in="cut")
# 16
A("Then Parvati",meaning="Then Parvati, Shiva's wife, walked down the hill.",
 why="Parvati in a red sari with a lotus walks gently along a green hillside with a calm face; her name is on the screen.",
 camera=cam("dolly_right",(1.0,-12,0),(1.0,12,0),"medium","normal",0,"a dolly that follows her walk"),
 focus={"subject":"parvati","depth":"deep"},vertical={"focus":"parvati"},layers=L_forest('#e8e0d0','#4a8a5a'),background=vista(SKY_DAY),mood={"emotion":"grace","grade":"warm"},
 characters=[{"who":"parvati","x":580,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"stand","emo":"calm","look":700,"walkTo":{"x":700,"c":"Parvati,","d":2.6,"sp":.7},"actions":[{"word":"hill","emo":"calm","d":.5}]}],
 effects=[name("Parvati,","Parvati",640,128,32)],transition_in="cut")
# 17
A("The demon stared",meaning="The demon stared at her.",
 why="Bhasmasura stares with wide red eyes toward the right, his mouth slightly open and his eyes fixed on her.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"medium","normal",0,"push in on the gaze"),
 focus={"subject":"bhasmasura","depth":"deep"},vertical={"focus":"bhasmasura"},layers=L_forest('#e8e0d0'),background=vista(SKY_DAY),mood={"emotion":"obsession","grade":"warm"},
 characters=[{"who":"bhasmasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"surprise","look":900,"mood":{"lx":.9},"engine":{"hand":0},"actions":[{"word":"her","emo":"anger","mood":{"lx":.9},"d":.5}]}],
 effects=[],transition_in="cut")
# 18
A("He wanted her",meaning="He wanted her, and her husband was in the way.",
 why="A close bust of Bhasmasura with a dark angry scowl and a sly sideways glance as the thought forms; red glow behind his head.",
 camera=cam("crane_down",(1.04,0,-10),(1.1,0,0),"close","tele",0,"descending on the dark thought"),
 focus={"subject":"bhasmasura","depth":"shallow"},vertical={"focus":"bhasmasura"},layers=L_forest('#e8c8b8'),background=vista(SKY_HOT),mood={"emotion":"lust","grade":"warm"},
 characters=[{"who":"bhasmasura","x":640,"y":300,"s":.8,"head":True,"flip":1,"pose":"stand","emo":"anger","look":900,"mood":{"lx":.7},"actions":[{"word":"way","emo":"rage","d":.5}]}],
 effects=[glow("husband",640,300,260,"255,100,80",.4,"a red glow of the dark wish")],transition_in="cut")
# 19
A("He raised his hand",meaning="He raised his hand to touch Shiva with the boon.",
 why="Bhasmasura lifts his glowing right hand high above his head with a wild grin, ash-grey light flaring from his palm.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,-2),"medium","normal",0,"rising with the raised hand"),
 focus={"subject":"bhasmasura","depth":"deep"},vertical={"focus":"bhasmasura"},layers=L_forest('#e8c8b8'),background=vista(SKY_HOT),mood={"emotion":"threat","grade":"warm"},
 characters=[{"who":"bhasmasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"raise","emo":"rage","look":600,"engine":{"hand":1},"actions":[{"word":"hand","emo":"rage","d":.4}]}],
 effects=[pfx("embers","hand",640,380,320,"grey sparks from the raised hand",alpha=.6)],transition_in="cut")
# 20
A("Shiva stepped back",meaning="Shiva stepped back, then he ran.",
 why="Shiva leans away in alarm with hands out and then turns into a run with his hair streaming; a gust of dust behind him.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"medium","normal",2,"a shaking slide as he bolts"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_forest('#e8c8b8'),background=vista(SKY_HOT),mood={"emotion":"flight","grade":"warm"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":.43,"flip":-1,"pose":"plead","emo":"surprise","look":820,"actions":[{"word":"ran","pose":"flee","emo":"fear","d":.4}]}],
 effects=[pfx("sand_drift","ran",760,640,460,"dust kicked up by the running god",alpha=.5)],transition_in="cut")
# 21
A("He ran in all",meaning="He ran in all ten directions.",
 why="Shiva sprints across a red desert road with his hair and tiger skin flying; speed dust streams behind him.",
 camera=cam("pan_right",(1.0,-14,0),(1.0,14,0),"wide","normal",3,"a hard pan follows the sprinting figure"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_desert(),background=vista(SKY_HOT,['#b87a6a','#9a5a5a','#7a4a4a','#5a3a3a']),mood={"emotion":"panic","grade":"warm"},
 characters=[{"who":"shiva","x":600,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"run","emo":"fear","look":700,"walkTo":{"x":680,"c":"ran","d":2,"sp":1.2},"actions":[{"word":"directions","emo":"fear","d":.4}]}],
 effects=[pfx("sand_drift","ran",380,640,480,"dust streaming behind the runner",alpha=.6)],transition_in="wipe")
# 22
A("Every time he looked",meaning="Every time he looked back, the demon was there.",
 why="Shiva runs at the left and glances back over his shoulder in terror while the demon, a smaller figure with a glowing hand, follows close behind at the right.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","wide",2,"a tracking slide with the chase"),
 focus={"subject":"shiva","depth":"deep"},vertical={"x":640},layers=L_forest('#e8d0b8'),background=vista(SKY_DUSK),mood={"emotion":"pursuit","grade":"warm"},
 characters=[{"who":"bhasmasura","x":740,"y":610,"s":.6,"_fixed":True,"flip":-1,"pose":"run","emo":"rage","look":560,"engine":{"hand":1},"actions":[{"word":"there","emo":"rage","d":.4}]},
   {"who":"shiva","x":560,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"run","emo":"fear","look":760,"mood":{"lx":-.7,"turn":-.5},"actions":[{"word":"back","emo":"fear","d":.4}]}],
 effects=[pfx("sand_drift","looked",380,640,460,"dust of the chase",alpha=.5)],transition_in="cut")
# 23
A("Only one place",meaning="Only one place was left: Vaikuntha, the home of Vishnu.",
 why="Shiva, exhausted, stands small at the gates of golden Vaikuntha with the golden palace and milk ocean ahead; the name Vaikuntha appears.",
 camera=cam("crane_up",(1.0,0,10),(1.0,0,-10),"wide","wide",0,"rising to reveal the refuge"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_vk(),background=vk(),mood={"emotion":"refuge","grade":"warm"},
 characters=[{"who":"shiva","x":640,"y":690,"s":.9,"_face":.46,"flip":1,"pose":"stand","emo":"fear","look":700,"actions":[{"word":"Vaikuntha,","emo":"calm","d":.6}]}],
 effects=[name("Vaikuntha,","Vaikuntha",640,128,32),glow("home",640,300,300,GLD,.4,"the golden light of Vaikuntha")],transition_in="fade")
# 24
A("\"Protect me,\"",meaning="Protect me, said Shiva.",
 why="Shiva pleads with pressed hands and a frightened face before Vishnu, who stands calm and listening at the right.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"two_shot","normal",0,"push in on the plea"),
 focus={"subject":"shiva","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"plea","grade":"warm"},
 characters=[{"who":"shiva","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"plead","emo":"fear","look":720,"talk":.8,"actions":[{"word":"Shiva","emo":"fear","d":.4}]},
   {"who":"vishnu","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"said","emo":"calm","d":.4}]}],
 effects=[],transition_in="cut")
# 25
A("Vishnu vanished",meaning="Vishnu vanished from Vaikuntha in front of Shiva.",
 why="Vishnu dissolves into a bright flash of gold light and swirling shimmer, fading out as Shiva watches with wide eyes.",
 camera=cam("static",(1.04,0,0),(1.04,0,0),"two_shot","normal",0,"the camera holds still while he disappears"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"magic","grade":"warm"},
 characters=[{"who":"shiva","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"stand","emo":"surprise","look":720,"actions":[{"word":"vanished","emo":"surprise","d":.4}]},
   {"who":"vishnu","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"open","emo":"calm","look":560,"engine_cues":{"fo":"vanished."},"engine":{"fd":.9},"actions":[]}],
 effects=[{"k":"flash","word":"vanished.","x":735,"y":340,"meaning":"a flash of light as Vishnu changes"},pfx("energy_swirl","vanished.",735,360,420,"shimmering swirl of the transformation",alpha=.5,blend="lighter")],transition_in="cut")
# 26
A("A beautiful woman",meaning="A woman of great charm, Mohini, stood in his place.",
 why="Mohini, blue-skinned in a red sari with garland and crown, stands in a graceful dance pose in the golden light, her name appearing on 'Mohini'.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the enchantress"),
 focus={"subject":"mohini","depth":"deep"},vertical={"focus":"mohini"},layers=L_vk(),background=vk(),mood={"emotion":"charm","grade":"warm"},
 characters=[{"who":"mohini","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"dance","emo":"joy","look":700,"engine":{"a":0},"engine_cues":{"ac":"woman"},"actions":[{"word":"Mohini.","pose":"dance2","emo":"joy","d":.5}]}],
 effects=[name("Mohini.","Mohini",640,128,32),pfx("halo_ring","woman",640,320,360,"a soft glow around the new form",alpha=.45,blend="lighter",behind=True)],transition_in="cut")
# 27
A("The demon forgot",meaning="The demon forgot his gift.",
 why="Bhasmasura gazes dreamily at Mohini with a soft goofy smile, his glowing hand hanging down, forgotten.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"medium","normal",0,"a slow drift as he drifts into the spell"),
 focus={"subject":"bhasmasura","depth":"deep"},vertical={"focus":"bhasmasura"},layers=L_vk(),background=vk(),mood={"emotion":"enchantment","grade":"warm"},
 characters=[{"who":"bhasmasura","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"joy","look":820,"mood":{"smile":.7,"lx":.8},"engine":{"hand":.2},"actions":[{"word":"gift","emo":"joy","mood":{"smile":.9,"lx":.9},"d":.5}]}],
 effects=[glow("forgot",640,320,240,"255,190,200",.35,"a rosy enchantment glow")],transition_in="cut")
# 28
A("\"Come,\"",1,meaning="Come, she said. Dance with me.",
 why="Mohini beckons with an open hand and a bright smile, her sari swaying in a dance pose.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back on the invitation"),
 focus={"subject":"mohini","depth":"deep"},vertical={"focus":"mohini"},layers=L_vk(),background=vk(),mood={"emotion":"invitation","grade":"warm"},
 characters=[{"who":"mohini","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"joy","look":600,"talk":.8,"actions":[{"word":"Dance","pose":"dance","emo":"joy","d":.5}]}],
 effects=[],transition_in="cut")
# 29 stack
A("Then she put",meaning="Then she put her hand on her head, and so did he.",
 why="Stacked: Mohini above puts her hand on her head in the dance; below the demon copies her and touches his own head with his glowing hand.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"two_shot","normal",0,"two stacked crops show the copy"),
 focus={"subject":"mohini","depth":"deep"},vertical={"mode":"stack","stack":["mohini","bhasmasura"]},layers=L_vk(),background=vk(),mood={"emotion":"trap","grade":"warm"},
 characters=[{"who":"mohini","x":420,"y":690,"s":.9,"flip":1,"pose":"dance","emo":"joy","look":640,"actions":[{"word":"head","pose":"headtouch","emo":"joy","d":.5}]},
   {"who":"bhasmasura","x":860,"y":690,"s":.9,"flip":-1,"pose":"dance","emo":"joy","look":520,"engine":{"hand":1},"actions":[{"word":"he.","pose":"headtouch","emo":"pride","d":.4}]}],
 effects=[],transition_in="wipe")
# 30
A("Mohini laughed",meaning="Mohini laughed and spun around a pile of ash.",
 why="Mohini spins in a joyful dance beside a heap of grey ash where the demon stood, and grey flakes drift in the golden light.",
 camera=cam("orbit",(1.0,-10,0),(1.04,10,0),"medium","normal",0,"the camera circles the dancing figure"),
 focus={"subject":"mohini","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"triumph","grade":"warm"},
 characters=[{"who":"mohini","x":570,"y":690,"s":.85,"_face":.43,"flip":1,"pose":"dance2","emo":"joy","look":700,"engine":{"spin":.6},"actions":[{"word":"ash.","emo":"joy","d":.4}]}],
 effects=[pfx("ash_pile","laughed",700,700,300,"a pile of ash where the demon stood",h=1),pfx("embers","ash.",700,580,260,"grey flakes drifting up from the ash",alpha=.5)],transition_in="cut")
# 31
A("Shiva ran because",meaning="Shiva ran because his own gift would not spare even him.",
 why="Shiva stands with a worried face looking back at the empty path, one hand open, and a faint grey spark glows in the air where the gift hung.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"medium","normal",0,"a slow look back at the danger that is now gone"),
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},layers=L_vk(),background=vk(),mood={"emotion":"reflection","grade":"warm"},
 characters=[{"who":"shiva","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"fear","look":500,"mood":{"lx":-.7},"actions":[{"word":"even","emo":"surprise","d":.5},{"word":"him.","emo":"calm","d":.6}]}],
 effects=[pfx("embers","gift",500,500,240,"grey sparks of the boon hanging in the air",alpha=.5)],transition_in="cut")
# 32
A("Vishnu saved him",meaning="Vishnu saved him by making the demon dance into it.",
 why="Vishnu and Shiva stand together in golden light, Vishnu with a calm smile and Shiva relaxed with a thankful face.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"two_shot","normal",0,"the last pull back on the pair"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"relief","grade":"warm"},
 characters=[{"who":"shiva","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"namaste","emo":"calm","look":720,"actions":[{"word":"dance","emo":"joy","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"open","emo":"joy","look":560,"actions":[{"word":"saved","emo":"joy","mood":{"smile":.8},"d":.5}]}],
 effects=[glow("saved",640,300,300,GLD,.45,"the gold of relief")],transition_in="cut")
print([s["start"]["t"] for s in G.S]);G.finish()
