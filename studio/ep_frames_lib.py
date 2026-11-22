import re
def parse_timeline_raw(p):
    beats=[];cur=None
    for ln in open(p,encoding='utf-8').read().splitlines():
        m=re.match(r'## Beat (\d+)\s+\((\d+):([\d.]+) – (\d+):([\d.]+)\)',ln)
        if m:cur={'beat':int(m[1]),'start':int(m[2])*60+float(m[3]),'end':int(m[4])*60+float(m[5]),'words':[]};beats.append(cur);continue
        if cur and ln.startswith('`') and '@' in ln:
            for w in re.findall(r'(\S+)@([\d.]+)',ln.strip('`')):cur['words'].append((w[0],float(w[1])))
    return beats
