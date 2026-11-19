"""Make the round joint discs match the colour of the limb/garment they sit on (slightly darker) instead of contrasting brown/black dots.
usage: recolor_joints.py [id ...]   (default: every character with full.png; writes full.png, keeps source.png untouched; full_orig.png backup)"""
import os,sys,json,shutil,numpy as np,cv2
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/'
def process(k,darken=0.90):
    src=f'{P}{k}/full.png'
    if not os.path.exists(src):return 0
    bak=f'{P}{k}/full_orig.png'
    if not os.path.exists(bak):shutil.copy(src,bak)
    im=Image.open(bak).convert('RGBA');a=np.asarray(im).copy();rgb=a[...,:3];al=a[...,3]>200
    H,W=al.shape;g=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY);g[~al]=255;g=cv2.GaussianBlur(g,(5,5),1.5)
    r0=max(8,int(H*0.012));r1=int(H*0.040)
    circ=cv2.HoughCircles(g,cv2.HOUGH_GRADIENT,dp=1.2,minDist=r0*2,param1=90,param2=18,minRadius=r0,maxRadius=r1)
    if circ is None:return 0
    n=0;yy,xx=np.mgrid[0:H,0:W]
    for x,y,r in circ[0]:
        x,y,r=int(x),int(y),int(r);inside=(xx-x)**2+(yy-y)**2<=r*r;ann=((xx-x)**2+(yy-y)**2<=(r*1.9)**2)&~((xx-x)**2+(yy-y)**2<=(r*1.15)**2)&al
        if inside.sum()<50 or ann.sum()<80:continue
        if al[inside].mean()<.9:continue
        ci=np.median(rgb[inside],axis=0);ca=np.median(rgb[ann],axis=0)
        li=ci.mean();la=ca.mean();dist=np.linalg.norm(ci-ca)
        sd=rgb[inside].std(axis=0).mean()
        # a joint disc: clearly darker/different from its surroundings AND a flat uniform fill
        if dist<45 or li>la-18 or sd>20:continue
        new=(ca*darken).clip(0,255)
        m=(xx-x)**2+(yy-y)**2<=(r+1)**2
        a[...,:3][m&al]=new.astype(np.uint8);n+=1
    # second pass: flat, compact, locally darker blobs (catches very dark or small discs that Hough missed)
    rgb=a[...,:3];al=a[...,3]>200;gg=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(np.float32)
    big=cv2.medianBlur(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY),int(H*0.06)//2*2+1).astype(np.float32)
    cand=((big-gg)>38)&al
    cand=cv2.morphologyEx(cand.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    num,lab,stats,cent=cv2.connectedComponentsWithStats(cand,connectivity=8)
    for i in range(1,num):
        x0,y0,w,h,area=stats[i]
        if not(r0*2*0.7<=w<=r1*2.4 and r0*2*0.7<=h<=r1*2.4):continue
        if area<0.7*np.pi*(min(w,h)/2)**2 or max(w,h)>1.35*min(w,h):continue
        m=lab==i;cx,cy=cent[i];rr=int(max(w,h)/2)+2
        ann=(((xx-cx)**2+(yy-cy)**2)<=(rr*1.9)**2)&~(((xx-cx)**2+(yy-cy)**2)<=(rr*1.15)**2)&al
        if ann.sum()<80:continue
        if rgb[m].std(axis=0).mean()>24:continue
        ca=np.median(rgb[ann],axis=0);new=(ca*darken).clip(0,255)
        mm=((xx-cx)**2+(yy-cy)**2<=(rr)**2)&al&(gg<ca.mean()-12);a[...,:3][mm]=new.astype(np.uint8);n+=1
    Image.fromarray(a,'RGBA').save(src);return n
if __name__=='__main__':
    ids=sys.argv[1:] or sorted(os.listdir(P))
    tot=0
    for k in ids:
        if os.path.isdir(P+k):
            n=process(k);tot+=n;print(k,n)
    print('discs recoloured:',tot)
