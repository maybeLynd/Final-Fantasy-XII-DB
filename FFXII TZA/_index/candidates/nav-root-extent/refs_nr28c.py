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
res=collections.Counter(); bad=[]; d0=collections.Counter(); pads=collections.Counter()
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    o28=u32(s,0x28); L=len(s); c=u32(s,0x24)
    if not c: continue
    t=L-o28; body=c*32; pad=s[o28+body:L]
    ok = t>=body and len(pad)<64 and pad.count(0)==len(pad) and (o28+body+len(pad))%64==0
    res[ok]+=1; pads[len(pad)]+=1
    if not ok: bad.append((os.path.basename(p),c,t))
    for i in range(c): d0[u32(s,o28+i*32)]+=1
print("rule holds:",dict(res)," pad sizes:",dict(pads)); print("bad:",bad[:5]); print("record +0 dword values:",d0.most_common(8))
