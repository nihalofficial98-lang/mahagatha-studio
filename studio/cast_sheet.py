"""Character sheets of the CODED cast for owner approval (step 4 of WORKFLOW.md).
  python3 studio/cast_sheet.py brahma vishnu shiva [--out DIR]     (no names = every cast member)
Per character: frame A = full figure + five face close-ups (calm, joy, anger, sad, surprise);
               frame B = five poses (stand, namaste, point, bow, open).  Writes DIR/<who>_faces.jpg, DIR/<who>_poses.jpg."""
import os,sys,json,subprocess,argparse,shutil,glob
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,R+'/studio')
import build as B,engine_vocab as V
from PIL import Image
def main():
    a=argparse.ArgumentParser();a.add_argument('who',nargs='*');a.add_argument('--out',default=R+'/library/characters/sheets');x=a.parse_args()
    names=x.who or [w for w in V.CAST if w not in('boar','swan','vishnu_rest','ardha','harihara')]
    bad=[n for n in names if n not in V.CAST]
    if bad:sys.exit(f'not in the cast: {bad} (add the spec to engine/v2_cast.js CAST and V2NAMES first)')
    shots=[];T=0
    lab=lambda s,x_,y:{'t':'text','s':s,'x':x_,'y':y,'size':24}
    for n in names:
        faces=[{'who':n,'x':150,'y':700,'s':1.0,'emo':'calm'}]+[{'who':n,'x':370+i*205,'y':330,'s':0.46,'head':True,'emo':e} for i,e in enumerate(['calm','joy','anger','sad','surprise'])]
        shots.append({'beat':1,'at':T,'draw':'scene','grade':'cel','cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,
            'sc':{'bg':{'k':'plain','cols':['#3a3450','#24203a'],'fore':False},'figs':faces,'fx':[lab(e,370+i*205,520) for i,e in enumerate(['calm','joy','anger','sad','surprise'])]+[lab(n,150,40)]}});T+=1
        poses=[{'who':n,'x':150+i*245,'y':690,'s':0.72,'pose':p,'emo':'calm'} for i,p in enumerate(['stand','namaste','point','bow','open'])]
        shots.append({'beat':1,'at':T,'draw':'scene','grade':'cel','cues':[],'cam':{'from':{'z':1},'to':{'z':1}},'dx':0,
            'sc':{'bg':{'k':'plain','cols':['#3a3450','#24203a'],'fore':False},'figs':poses,'fx':[lab(p,150+i*245,40) for i,p in enumerate(['stand','namaste','point','bow','open'])]}});T+=1
    tmp=R+'/build/cast_sheet';shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp);os.makedirs(x.out,exist_ok=True)
    json.dump(shots,open(tmp+'/shots.json','w'),ensure_ascii=False)
    json.dump([{'beat':1,'audio':T+1,'duration':T+1,'words':[{'text':'.','start':0,'end':.1}]}],open(tmp+'/timings.json','w'))
    html=B.build(1.5);env=dict(os.environ,ENGINE=html,VW='1920',VH='1080')
    if 'NODE_PATH' not in env:env['NODE_PATH']=subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()
    ts=[f'{i+.5:.1f}' for i in range(T)]
    r=subprocess.run(['node',R+'/studio/still.js',tmp+'/shots.json',tmp+'/timings.json',tmp]+ts,env=env,cwd=R,capture_output=True,text=True)
    if r.returncode:sys.exit(r.stdout+r.stderr)
    for i,t in enumerate(ts):
        f=f"{tmp}/t{t.rjust(5,'0')}.png";n=names[i//2];dst=f"{x.out}/{n}_{'faces' if i%2==0 else 'poses'}.jpg"
        Image.open(f).convert('RGB').save(dst,quality=88);print(dst)
main()
