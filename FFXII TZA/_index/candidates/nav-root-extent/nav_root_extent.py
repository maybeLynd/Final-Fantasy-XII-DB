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
first=collections.Counter(); v24=collections.Counter(); v28=collections.Counter(); minall=collections.Counter(); secsizes=[]
order=collections.Counter(); n=0; zero24=0
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    n+=1; secsizes.append(len(s))
    offs={k:u32(s,k) for k in (0x0C,0x10,0x14,0x18,0x1C,0x20)}
    o28=u32(s,0x28); v24[u32(s,0x24)]+=1
    m=min(offs.values()); first[m]+=1
    minall[min(m,o28 if o28 else 1<<30)]+=1
    v28[("0" if o28==0 else ("in" if o28<len(s) else "out"))]+=1
    order[tuple(sorted(offs,key=offs.get))]+=1
print("sections",n)
print("smallest of the six offsets:",first.most_common(6))
print("smallest incl +0x28:",minall.most_common(6))
print("+0x24 values:",v24.most_common(6))
print("+0x28:",dict(v28))
print("offset order (by value) top:",order.most_common(3))
cor=collections.Counter(); b2c=collections.Counter(); w0=collections.Counter(); w8=collections.Counter()
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    c24=u32(s,0x24); o28=u32(s,0x28)
    cor[(c24==0, "0" if o28==0 else ("in" if o28<len(s) else "out"))]+=1
    b2c[s[0x2C:0x30].hex()]+=1
    w0[u32(s,0)]+=1
print("(+0x24==0, +0x28):",dict(cor))
print("+0x2C..+0x2F:",b2c.most_common(4))
print("+0x00:",w0.most_common(3))
eq=collections.Counter(); tailsz=collections.Counter()
for p in paths:
    s=slot4(open(p,"rb").read())
    if s is None: continue
    c24=u32(s,0x24); o28=u32(s,0x28); L=len(s)
    if o28>=L: eq["==len" if o28==L else ("len+%d"%(o28-L) if o28-L<0x100 else "far")]+=1
    else:
        # bytes from +0x28 target to end, per entry
        if c24: tailsz[(L-o28)//c24 if (L-o28)%c24==0 else "rem%d/%d"%((L-o28)%c24,c24)]+=1
        else: tailsz[("c0 tail",L-o28)]+=1
print("out cases:",dict(eq))
print("tail bytes per +0x24 entry:",tailsz.most_common(8))
