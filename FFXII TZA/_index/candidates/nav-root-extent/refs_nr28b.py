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
c=collections.Counter(); nz=[]; allz=collections.Counter()
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    o28=u32(s,0x28); L=len(s); c24=u32(s,0x24); t=max(0,L-o28)
    tail=s[o28:L] if t else b""
    z=tail.count(0)==len(tail)
    allz[(c24==0, z)]+=1
    c[(c24==0, L%64, (o28+15)//16*16 == o28)]+=1
    if c24 and len(nz)<6: nz.append((os.path.basename(p),c24,t,L%64,tail[:64].hex()))
print("(c24==0, tail all zero):",dict(allz))
print("(c24==0, len%64, o28 16-aligned):",c.most_common(8))
for e in nz: print(e)
