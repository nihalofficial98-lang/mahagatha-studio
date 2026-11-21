"""Cut painted characters out of a green backdrop -> RGBA PNG (trimmed).
Only green regions CONNECTED to the image border are removed, so green parts of the figure (serpent, dhoti) stay.  usage: keyout.py in.png out.png"""
import sys,numpy as np,colorsys
from PIL import Image,ImageFilter
from scipy import ndimage as ndi
def key(src,dst,pad=6,hmax=125):
    im=Image.open(src).convert('RGB');a=np.asarray(im).astype(np.float32)/255.0;r,g,b=a[...,0],a[...,1],a[...,2]
    mx=np.maximum(np.maximum(r,g),b);mn=np.minimum(np.minimum(r,g),b);d=mx-mn+1e-6;v=mx;s=d/(mx+1e-6)
    h=np.where(mx==g,60*(2+(b-r)/d),np.where(mx==r,60*(((g-b)/d)%6),60*(4+(r-g)/d)))%360
    green=(h>55)&(h<hmax)&(s>0.16)&(v>0.22)&(g>=r)&(g>=b)
    green=np.pad(green,4,mode='edge');green=ndi.binary_closing(green,iterations=2)[4:-4,4:-4]   # pad so closing does not erode the border
    lab,n=ndi.label(green);border=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]]));border=border[border>0]
    bg=np.isin(lab,border)
    # enclosed pockets (between an arm and the body, between figures) that match the backdrop colour are backdrop too
    ref=a[bg].mean(axis=0) if bg.any() else None
    if ref is not None:
        areas=ndi.sum(np.ones_like(lab),lab,index=np.arange(1,n+1));means=[ndi.mean(a[...,c],lab,index=np.arange(1,n+1)) for c in range(3)]
        for i in range(n):
            L=i+1
            if L in border or areas[i]<120:continue
            dist=np.sqrt(sum((means[c][i]-ref[c])**2 for c in range(3)))*255
            if dist<42:bg|=(lab==L)
    bg=ndi.binary_dilation(bg,iterations=1)                      # eat the green fringe
    alpha=(~bg).astype(np.float32);alpha=ndi.gaussian_filter(alpha,0.9)
    # despill: on the figure's edge pixels, pull green back toward the other channels
    edge=(alpha>0.02)&(alpha<0.98)                    # despill only the feathered edge, never the figure's own greens
    g2=g.copy();g2[edge]=np.minimum(g[edge],np.maximum(r[edge],b[edge])+0.02)
    # drop tiny stray bits (e.g. a floating arc) that are not part of the main figure
    solid=alpha>0.5;l2,n2=ndi.label(solid)
    if n2>1:
        sizes=ndi.sum(solid,l2,index=np.arange(1,n2+1));keep=np.isin(l2,[i+1 for i,z in enumerate(sizes) if z>=0.04*sizes.max()])
        keep=ndi.binary_dilation(keep,iterations=6);alpha=alpha*keep
    out=(np.dstack([r,g2,b,alpha])*255).clip(0,255).astype(np.uint8);img=Image.fromarray(out,'RGBA')
    bb=img.getbbox()
    if bb:img=img.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(img.width,bb[2]+pad),min(img.height,bb[3]+pad)))
    img.save(dst);return img.size
if __name__=='__main__':print(key(sys.argv[1],sys.argv[2]))
