"""Render stills of an episode at given times only: python3 studio/still_at.py 05 360.5 380 ... -> build/epNN/quick/"""
import sys,os,subprocess,shutil,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import studio as S
n=sys.argv[1];ts=sys.argv[2:]
import build as B
html=B.build(1.5)
class A:pass
a=A();a.n=n
S.prepare(a,S.target(a))
d=S.bd(n)+'/quick';shutil.rmtree(d,ignore_errors=True)
S.sh(['node','studio/still.js',S.ep(n)+'/shots.json',S.bd(n)+'/engine_timings.json',d]+ts,env=dict(S.node_env(),ENGINE=html))
print(d)
