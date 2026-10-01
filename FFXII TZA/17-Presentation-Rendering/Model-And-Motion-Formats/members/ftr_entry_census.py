# @FTR entry census: header fields, index table, record bounds, aux pool - all 1,066 .cm files.
# Run: FF12_VBF=<archive> python ftr_entry_census.py
#
# Checks the layout proven in 00372820/003712E0/409300/4094D0:
#   +0x04 kind == 2 in every file (the kind-0 0x4C-stride arm of the binder is dead)
#   +0x30 u32 == +0x0C u32 (duplicated count)
#   +0x40 u32[count] = {recOff << 12 | ordinal}, low 12 == index in every record of every file
#   every record offset lies inside [align16(0x40+4*count), +0x34-auxOff)
#   aux region [a34, elen) is a u32/f32 pool: length % 4 == 0
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index
BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)
def read_all(p):
    sb, size, off = names[p]; n = (size + BLOCK - 1) // BLOCK
    out = b""; f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp: c = zlib.decompress(c)
        out += c
    return out
def entries(p):
    d = read_all(p)
    assert d[:4] == b"@FRP", p
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for i in range(cnt):
        o = base + struct.unpack_from("<I", d, base + i*4)[0]
        yield d[o:o+4], o, d

tot = 0
kind = collections.Counter(); cnt_hist = collections.Counter()
w38_hist = collections.Counter(); aux_hist = collections.Counter()
dup_ok = ord_ok = inb_ok = aux4_ok = recbase_ok = 0
link_hist = collections.Counter()  # dword[rec] bits12..23 values
flag100 = collections.Counter()
for p in [q for q in names if q.lower().endswith(".cm")]:
    for tag, o, d in entries(p):
        if tag != b"@FTR": continue
        tot += 1
        w4, elen, cnt = struct.unpack_from("<III", d, o+4)
        a30, a34, a38, a3c = struct.unpack_from("<IIII", d, o+0x30)
        kind[w4] += 1; cnt_hist[cnt] += 1; w38_hist[a38] += 1
        aux_hist[elen - a34] += 1
        if a30 == cnt: dup_ok += 1
        if (elen - a34) % 4 == 0: aux4_ok += 1
        recbase = (0x40 + 4*cnt + 15) & ~15
        offs = [struct.unpack_from("<I", d, o+0x40+4*i)[0] for i in range(cnt)]
        if all((e & 0xFFF) == i for i, e in enumerate(offs)): ord_ok += 1
        if offs and min(e >> 12 for e in offs) == recbase: recbase_ok += 1
        if all(recbase <= (e >> 12) < a34 for e in offs): inb_ok += 1
        nf = 0
        for i, e in enumerate(offs):
            ro = e >> 12
            link, fl = struct.unpack_from("<II", d, o + ro)
            nxt = -1 if (link & 0xFFF000) == 0xFFF000 else (link >> 12) & 0xFFF
            link_hist[nxt] += 1
            if fl & 0x100: nf += 1
        flag100[nf] += 1
print("FTR entries:", tot)
print("kind +0x04:", kind.most_common())
print("count +0x0C:", cnt_hist.most_common(12))
print("count2 +0x30 == count:", dup_ok)
print("index low12 == ordinal:", ord_ok)
print("first rec off == align16(recbase):", recbase_ok)
print("all rec offsets in [recbase, a34):", inb_ok)
print("aux size %4 == 0:", aux4_ok)
print("word+0x38 histogram:", w38_hist.most_common(12))
print("aux size histogram:", aux_hist.most_common(10))
print("records-per-file with flag 0x100:", flag100.most_common(8))
print("rec+0 next-idx top:", link_hist.most_common(10))
