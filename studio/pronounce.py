#!/usr/bin/env python3
"""Write Sanskrit names/terms in Devanagari for the voice AI.
usage: python3 studio/pronounce.py IN.txt OUT.txt   (reads library/pronunciation_devanagari.json)
Possessives become e.g. ब्रह्मा's. [emotion tags] and === separators are left untouched.
Prints words in IN that look Sanskrit-like but are not in the glossary (capitalised, not sentence-initial) so you can extend the map."""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
M = json.load(open(root/'library/pronunciation_devanagari.json', encoding='utf-8'))['map']
keys = sorted(M, key=len, reverse=True)
pat = re.compile(r"(?<![A-Za-z])(" + "|".join(map(re.escape, keys)) + r")(?![A-Za-z])", re.I)
lower = {k.lower(): v for k, v in M.items()}
def conv(line):
    if line.startswith('===') or not line.strip(): return line
    out, i = [], 0
    for m in re.finditer(r"\[[^\]]*\]", line):   # keep tags
        out.append(('t', line[i:m.start()])); out.append(('k', m.group(0))); i = m.end()
    out.append(('t', line[i:]))
    return ''.join(pat.sub(lambda m: lower[m.group(1).lower()], s) if k == 't' else s for k, s in out)
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding='utf-8').read()
res = '\n'.join(conv(l) for l in text.split('\n'))
open(dst, 'w', encoding='utf-8').write(res)
unk = set()
for l in text.split('\n'):
    if l.startswith('==='): continue
    for m in re.finditer(r"(?<![.?!\"“]\s)(?<!^)\b([A-Z][a-z]{3,})\b", re.sub(r"\[[^\]]*\]", "", l)):
        w = m.group(1)
        if w.lower() not in lower: unk.add(w)
print('wrote', dst, '| capitalised words not in glossary (check):', sorted(unk))
