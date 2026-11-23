"""Exact-text subtitles for a recorded voiceover, no speech model: python3 studio/make_srt.py <script.txt> <voice.mp3> <out.srt>
Cues are phrases of the ORIGINAL script text (punctuation kept, emotion tags removed), timed by speech/silence chunks + DP."""
import sys,re,math,json,numpy as np
sys.path.insert(0,__file__.rsplit('/',1)[0]);import align_voice as A
def phrases(path):
    out=[]
    for ln in open(path,encoding='utf-8'):
        ln=re.sub(r'^\s*\[[^\]]*\]\s*','',ln).strip()
        if not ln:continue
        for s in re.findall(r'.+?(?:[।?!]+[”"’\']*|$)',ln):
            s=s.strip()
            if not s:continue
            parts=[s]
            while True:
                nxt=[]
                for p in parts:
                    if len(p)<=34:nxt.append(p);continue
                    cands=[m.end() for m in re.finditer(r'[,，]["”’\']?\s',p)]
                    if not cands:cands=[m.end() for m in re.finditer(r'\s',p)]
                    c=min(cands,key=lambda e:abs(e-len(p)/2));a,b=p[:c].strip(),p[c:].strip()
                    nxt+= [a,b] if a and b else [p]
                if nxt==parts:break
                parts=nxt
            out+=parts
    return out
def ends(p):return 2 if re.search(r'[।?!][”"’\']*$',p) else (1 if re.search(r'[,][”"’\']?$',p) else 0)
def pieces(x):
    hop=.01;n=int(A.SR*hop);m=len(x)//n;e=10*np.log10((x[:m*n].reshape(m,n)**2).mean(1)+1e-10);e=np.convolve(e,np.ones(5)/5,'same')
    out=[]
    def split(a,b):
        if b-a<=.8:out.append([a,b]);return
        i0,i1=int((a+.3)/hop),int((b-.3)/hop)
        if i1<=i0:out.append([a,b]);return
        k=i0+int(np.argmin(e[i0:i1]));t=k*hop;split(a,t);split(t,b)
    for a,b in A.chunks(x):split(a,b)
    return out
def dp(U,ch,span=26):
    N=len(ch);K=len(U);W=np.array([sum(A.wt(w) for w in u.split()) for u in U]);dur=np.array([c[1]-c[0] for c in ch]);cum=np.r_[0,np.cumsum(dur)]
    gap=np.array([ch[i+1][0]-ch[i][1] for i in range(N-1)]+[0.0]);r=cum[-1]/W.sum();INF=1e18
    typ=[ends(u) for u in U]
    for it in range(2):
        f=np.full((K+1,N+1),INF);bk=np.zeros((K+1,N+1),int);f[0,0]=0
        for k in range(1,K+1):
            for j in range(k,N+1):
                best=INF;bi=0
                for i in range(max(k-1,j-span),j):
                    if f[k-1,i]>=INF:continue
                    D=cum[j]-cum[i];c=f[k-1,i]+3.0*math.log(max(D,.05)/(W[k-1]*r))**2
                    if i>0:
                        g=gap[i-1];t=typ[k-2]
                        c-= (2.5*min(g,.6)/.6 if t==2 else 1.2*min(g,.4)/.4 if t==1 else 0)
                        if t==0 and g>.45:c+=.8
                    if c<best:best,bi=c,i
                f[k,j]=best;bk[k,j]=bi
        j=N;res=[]
        for k in range(K,0,-1):i=bk[k,j];res.append((i,j));j=i
        res=res[::-1]
        if it==0:r=float(np.median([(cum[j]-cum[i])/W[k] for k,(i,j) in enumerate(res)]))
    return res,r,W,cum
def ts(t):
    h=int(t//3600);m=int(t%3600//60);s=t%60;return f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}'.replace(',1000',',999')
def wrap(p):
    if len(p)<=36:return p
    ws=p.split();best=min(range(1,len(ws)),key=lambda i:abs(len(' '.join(ws[:i]))-len(' '.join(ws[i:]))));return ' '.join(ws[:best])+'\n'+' '.join(ws[best:])
def main():
    script,voice,out=sys.argv[1:4];U=phrases(script);x=A.load(voice);total=len(x)/A.SR;ch=pieces(x)
    res,r,W,cum=dp(U,ch);cues=[]
    for k,(i,j) in enumerate(res):cues.append([ch[i][0],ch[j-1][1],U[k],(cum[j]-cum[i])/(W[k]*r)])
    for k,c in enumerate(cues):
        nxt=cues[k+1][0] if k+1<len(cues) else total;c[0]=max(0,c[0]-.05);c[1]=min(c[1]+.15,nxt-.02,total)
        if c[1]-c[0]<.5:c[1]=min(c[0]+.5,nxt-.02)
    open(out,'w',encoding='utf-8').write('\n'.join(f'{k+1}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n' for k,(a,b,t,_) in enumerate(cues)))
    json.dump([{'start':round(a,2),'end':round(b,2),'text':t,'rate':round(q,2)} for a,b,t,q in cues],open(out+'.json','w'),ensure_ascii=False,indent=0)
    bad=[(round(a,1),round(q,2),t[:30]) for a,b,t,q in cues if not .55<q<1.7]
    print(len(U),'cues,',len(ch),'pieces, total',round(total,1),'s; rate outliers:',len(bad));print(bad[:12])
if __name__=='__main__':main()
