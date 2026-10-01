# OPUS 2026-09-25 block 248; slot-4 parser copied from nav_root_extent.py
import os,struct,glob,collections
ROOT=os.environ.get("FF12_EXTRACT","D:/FFXII_TZA_extract")
paths=sorted(glob.glob(os.path.join(ROOT,"ps2data","plan_master","map_ctrl","**","*.mpk"),recursive=True))
def slot4(d):
    count=struct.unpack_from("<I",d,0)[0]; sizes=struct.unpack_from("<%dI"%count,d,4)
    pos=((count+1)*4+0x3F)&~0x3F
    for i,s in enumerate(sizes):
        if not s: continue
        pos+=0x40
        if i==4: return d[pos:pos+s]
        pos+=s
    return None
u32=lambda b,o: struct.unpack_from("<I",b,o)[0]

import collections
r=collections.Counter(); slack=collections.Counter(); maxv=collections.Counter()
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    n=struct.unpack_from("<H",s,0x0A)[0]; np_=struct.unpack_from("<H",s,0x08)[0]
    o1c=u32(s,0x1C); o20=u32(s,0x20); need=n*n*2
    r[o20-o1c>=need]+=1; slack[(o20-o1c)-need]+=1
    vals=struct.unpack_from("<%dH"%(n*n),s,o1c) if n else ()
    maxv[(max(vals) if vals else 0) < max(np_,1)]+=1
print("gap >= n*n*2:",dict(r)); print("slack:",slack.most_common(6)); print("max entry < portalCount:",dict(maxv))
