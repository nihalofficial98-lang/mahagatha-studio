"""Slice the approved Gemini Shiva images into rig pieces (full-canvas RGBA PNGs sharing source coordinates).
Source body = library/pilot/tall/calm_b_cut.png (445x943). Heads: calm_b (eyes open), calm_a (eyes closed), rage_b (angry)."""
import os,numpy as np
from PIL import Image,ImageDraw,ImageFilter
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));T=R+'/library/pilot/tall/';O=R+'/library/pilot/assets/'
body=Image.open(T+'calm_b_cut.png').convert('RGBA');W,H=body.size;a=np.asarray(body).astype(np.int16);al=a[...,3]>40
yy,xx=np.mgrid[0:H,0:W]
skin=(a[...,2]>a[...,0]+8)&(a[...,2]>95)&al                      # blue-ish skin pixels (not orange skirt, not brown discs)
def save(mask,name,src=a):
    m=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.7))
    im=Image.fromarray(src.astype(np.uint8),'RGBA');al2=np.minimum(np.asarray(im)[...,3],np.asarray(m));im.putalpha(Image.fromarray(al2.astype(np.uint8)));im.save(O+name);return mask
def poly(pts):
    im=Image.new('L',(W,H),0);ImageDraw.Draw(im).polygon(pts,fill=255);return np.asarray(im)>0
# ---- pieces (masks on the SAME source canvas) ----
head=al&(yy<236)&(xx>=186)
armR_up=al&(xx>=370)&(yy>=276)&(yy<376)
armR_lo=al&(xx>=378)&(yy>=372)
left_grp=al&((xx<112)|poly([(112,246),(168,256),(158,300),(128,362),(112,404),(60,420),(60,246)]))
left_grp&=~head
leg_zone=(yy>=618)
kneeL=(xx-220)**2+(yy-700)**2<28**2;kneeR=(xx-322)**2+(yy-700)**2<28**2
band=(yy>=684)&(yy<716)
thighL=al&band&(xx<272)&(xx>150)&(skin|kneeL)
thighR=al&band&(xx>=272)&(skin|kneeR)
shinL=al&(yy>=712)&(xx<272)&(xx>150)
shinR=al&(yy>=712)&(xx>=272)
used=head|armR_up|armR_lo|left_grp|thighL|thighR|shinL|shinR
root=al&~used
for n,m in [('head_open',head),('armR_up',armR_up),('armR_lo',armR_lo),('armL_grp',left_grp),('thighL',thighL),('thighR',thighR),('shinL',shinL),('shinR',shinR),('root',root)]:
    save(m,f'sp_{n}.png');print(n,int(m.sum()))
# heads from other images, aligned to calm head by chin position
def top_of(arr):
    ys,xs=np.where(arr[...,3]>40);y0=ys.min();x0=int(np.median(xs[ys<y0+6]));return x0,int(y0)
def head_from(path,name):
    im=Image.open(T+path).convert('RGBA');b=np.asarray(im).astype(np.int16);Hh,Ww=b.shape[:2]
    cx,cy=top_of(np.asarray(body));ox,oy=top_of(b);dx,dy=cx-ox,cy-oy
    full=np.zeros((H,W,4),np.int16)
    for y in range(Hh):
        ty=y+dy
        if ty<0 or ty>=236:continue
        for_x0=max(0,-dx);for_x1=min(Ww,W-dx)
        row=b[y,for_x0:for_x1,:].copy();xs=np.arange(for_x0,for_x1)+dx;ok=xs>=186
        row[~ok]=0;full[ty,for_x0+dx:for_x1+dx,:]=row
    Image.fromarray(full.astype(np.uint8),'RGBA').save(O+name)
head_from('rage_b_cut.png','sp_head_rage.png');head_from('calm_a_cut.png','sp_head_closed.png')
print('done')

# ---- consistent heads: mirror the open head so the moon matches the rage head, then derive the closed-eyes head from it ----
from PIL import ImageChops
o=Image.open(O+'sp_head_open.png').convert('RGBA');X0=268
fl=o.transpose(Image.FLIP_LEFT_RIGHT);fl=ImageChops.offset(fl,2*X0-(W-1),0);fl.save(O+'sp_head_open.png')
arr=np.asarray(fl).astype(np.int16);dark=(arr[...,0]<95)&(arr[...,1]<85)&(arr[...,2]<95)&(arr[...,3]>200)
band=np.zeros_like(dark);band[126:152,215:330]=True;m=dark&band;ys,xs=np.where(m)
cxm=xs.mean();L=xs[xs<cxm];R=xs[xs>=cxm];ly=ys[xs<cxm].mean();ry=ys[xs>=cxm].mean();lx=L.mean();rx=R.mean()
cheek=tuple(int(v) for v in arr[int(ly)+4,int((lx+rx)/2)+2,:3]);print('eyes',(lx,ly),(rx,ry),'skin',cheek)
cl=fl.copy();d=ImageDraw.Draw(cl)
for ex,ey in ((250,138),(291,137)):
    d.ellipse((ex-15,ey-9,ex+15,ey+8),fill=cheek+(255,))
    d.arc((ex-13,ey-8,ex+13,ey+6),25,155,fill=(28,22,30,255),width=3)
cl.save(O+'sp_head_closed.png')
