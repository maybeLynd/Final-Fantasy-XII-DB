import sys, io, zlib, struct
from collections import Counter
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
from census_format_magics import load_index
BLOCK = 0x10000
VBF = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf"
f = io.open(VBF,"rb"); names, blocks = load_index(f)
def read_all(path):
    sb,size,off = names[path]; n=(size+BLOCK-1)//BLOCK; data=b""; f.seek(off)
    for i in range(n):
        csize = blocks[sb+i] or BLOCK
        chunk = f.read(csize)
        if csize != (BLOCK if i<n-1 else size-BLOCK*(n-1)): chunk = zlib.decompress(chunk)
        data += chunk
    return data
ebps = sorted(p for p in names if p.endswith(".ebp") and "/us/" in p)
fields = [(i, 0x10+i*4) for i in range(20)]
pop = {i:0 for i,_ in fields}; magic = {i:Counter() for i,_ in fields}
scnt = Counter(); bad8 = []
for p in ebps:
    d = read_all(p)
    if d[:4] != b"EBP2": continue
    scnt[struct.unpack_from("<I",d,4)[0]] += 1
    for i,off in fields:
        v = struct.unpack_from("<I",d,off)[0]
        if v:
            pop[i]+=1
            if i in (0,4,14,16,17,19):  # slots my first census missed
                magic[i][d[v:v+4]]+=1
    if struct.unpack_from("<I",d,8)[0] or struct.unpack_from("<I",d,0xC)[0]: bad8.append(p)
print("slotCount distribution:", dict(scnt))
print("nonzero +08/+0C:", bad8[:5], len(bad8))
for i,off in fields:
    m = dict(magic[i].most_common(4))
    print(f"slot {i:2d} +0x{off:02x}: populated {pop[i]:4d}/1115  magics {m if m else ''}")
