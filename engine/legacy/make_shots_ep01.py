"""Visual plan (edit decision list) for Episode 01 -> shots_ep01.json. f(z0,z1,(x0,y0),(x1,y1)) = camera focus move."""
import json
def f(z0,z1=None,c0=(640,360),c1=None):
    z1=z0 if z1 is None else z1; c1=c0 if c1 is None else c1
    return {"z":[z0,z1],"c":[list(c0),list(c1)]}
def ins(to,shot,**k): d={"to":to,"shot":shot}; d.update(k); return d
def cut(to,focus): return {"to":to,"focus":focus}
S=[
 {"shot":"void","beats":[1,2],"cuts":[ins(.28,"starfly",rgb="200,210,255"),cut(.52,f(1,1.25)),cut(.76,f(1.5,1.9)),cut(1,f(1))]},
 {"shot":"om","beats":[3,4],"card":"भाग 1 — सृष्टि का जन्म","cuts":[cut(.2,f(1,1.15)),ins(.42,"starfly",rgb="255,225,160"),cut(.68,f(1.3,1.6)),cut(1,f(1.15,1))]},
 {"shot":"gunas","beats":[5],"cuts":[cut(.33,f(1.3,1.5,(640,340))),cut(.52,f(1,1.1)),cut(1,f(1))]},
 {"shot":"narayana","beats":[6],"cuts":[cut(.25,f(1,1.1)),cut(.5,f(2.0,2.3,(520,430))),cut(.72,f(1.7,1.5,(450,300),(450,320))),cut(1,f(1))]},
 {"shot":"egg_lotus","beats":[7],"cuts":[cut(.22,f(1,1.1)),cut(.45,f(1.8,2.0,(640,390))),cut(.7,f(1.1,1.4,(640,330),(640,200))),cut(1,f(1.6,2.2,(640,200),(640,150)))]},
 {"shot":"split","beats":[8],"cuts":[cut(.28,f(1,1.2)),cut(.5,f(1.5,1.7)),cut(.78,f(1)),cut(1,f(1,1.1))]},
 {"shot":"vedas","beats":[9],"cuts":[cut(.25,f(1,1.1)),cut(.5,f(1.8,2.0,(640,300))),cut(.8,f(1)),cut(1,f(1.7,1.9,(640,300)))]},
 {"shot":"birth","beats":[10],"card":"भाग 2 — मधु और कैटभ","cuts":[cut(.3,f(1,1.1)),cut(.55,f(1.8,2.0,(420,440))),ins(.72,"eyes",kind="glow"),cut(1,f(1.1,1))]},
 {"shot":"grow","beats":[11],"cuts":[cut(.3,f(1.1,1.4,(560,420))),cut(.6,f(1)),cut(.8,f(1.5,1.7,(430,300))),cut(1,f(1,1.15,(640,300)))]},
 {"shot":"confront","beats":[12],"cuts":[cut(.22,f(1,1.1)),cut(.45,f(2.0,2.2,(990,360))),cut(.62,f(2.2,2.4,(240,400))),cut(.82,f(1.8,1.9,(859,320))),cut(1,f(1.1,1.2,(640,380)))]},
 {"shot":"shake","beats":[13],"cuts":[cut(.25,f(1.1,1.3)),cut(.5,f(1.8,1.8,(256,420))),cut(.7,f(1,1,(640,400))),cut(1,f(1.7,2.0,(1000,360)))]},
 {"shot":"plea","beats":[14],"cuts":[cut(.3,f(1,1.15,(794,330))),cut(.5,f(2.8,3.0,(290,600))),cut(.75,f(1.9,2.1,(794,310))),cut(1,f(1.2,1))]},
 {"shot":"nidra","beats":[15],"cuts":[cut(.3,f(1,1.2,(640,420))),ins(.55,"ripple",rgb="150,170,255"),cut(.78,f(1.4,1.6,(640,380))),cut(1,f(1.2,1,(640,300)))]},
 {"shot":"hayagriva","beats":[16],"cuts":[cut(.2,f(1,1.1)),cut(.4,f(1.8,2.0,(560,390))),cut(.6,f(1,1.05)),cut(.8,f(1.9,1.9,(1000,380))),cut(1,f(1.1,1.2,(700,400)))]},
 {"shot":"trick","beats":[17],"phase":1,"cuts":[cut(.35,f(1.1,1.4,(358,380))),cut(.7,f(1,1.2)),cut(1,f(1.8,2.0,(358,367)))]},
 {"shot":"trick","beats":[18],"phase":2,"cuts":[cut(.3,f(1.7,1.9,(950,380))),cut(.55,f(1.5,1.6,(358,380))),cut(.8,f(1,1.1)),cut(1,f(2.0,2.2,(840,370)))]},
 {"shot":"trick","beats":[19],"phase":3,"cuts":[cut(.4,f(1.4,1.8,(358,370))),cut(.7,f(2.0,2.4,(980,380))),ins(1,"eyes",kind="wide")]},
 {"shot":"water","beats":[20],"cuts":[cut(.3,f(1,1.1)),cut(.55,f(2.2,2.2,(512,354))),cut(.8,f(2.2,2.2,(794,381))),cut(1,f(1))]},
 {"shot":"vgrow","beats":[21],"cuts":[cut(.3,f(1.0,1.3,(640,400))),cut(.55,f(1.5,1.2)),cut(.72,f(1)),cut(1,f(1,1.1,(640,250)))]},
 {"shot":"reflect","beats":[22],"cuts":[cut(.3,f(1.6,1.8,(307,379))),cut(.6,f(1.1,1.2,(640,400))),cut(1,f(1.7,1.9,(896,354)))]},
 {"shot":"earth","beats":[23],"cuts":[cut(.3,f(1,1.2,(640,560))),cut(.55,f(1.4,1.6,(205,200))),cut(.8,f(1,1.1)),cut(1,f(1))]},
 {"shot":"ending","beats":[24],"cuts":[cut(.4,f(1,1.5,(640,380))),cut(.7,f(1.6,1.6,(640,380))),cut(1,f(1))]},
 {"shot":"teaser","beats":[25],"cuts":[cut(.5,f(1,1.1)),cut(1,f(1))]}
]
json.dump(S,open("engine/shots_ep01.json","w"),ensure_ascii=False,indent=1)
print(sum(len(s["cuts"]) for s in S),"cuts in",len(S),"shots")
