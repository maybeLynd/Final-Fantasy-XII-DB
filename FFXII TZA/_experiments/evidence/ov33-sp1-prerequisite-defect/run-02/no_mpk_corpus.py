# sp1_counts.py - OV-33 (i) data gap: the polyline copy 002DE800 never bounds dword [src+0x14]; its only authored route
# is 003631B0 -> 003638B0 -> 002DEFA0 with an SP1 emitter record. Over every shipped .mpk slot-16 SP1 block, walk the
# region-C record index {u16 bound; u16 off[]} (record = SP1 + off, as the walker computes it) and report, per record,
# shape = byte[+9] & 0x7F and count = u32[+0x14]. Question: is any class-2 (multi-point) count >= 128 (overflows the
# 128-point area at 0215E734) or >= 140 (reaches 0215EFF4)?
# Control: the map-ctrl page's census says 2,326 records, 400 of shape 2, count 1 in 2,265 - the totals must reproduce.
import sys, struct, collections
sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract
VBF = 'C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\Tools\\work\\ASTRA\\dashboard-views-eae0ed3c7-review\\vbf-chain\\positive.vbf'


def slot16(d, s):
    cnt = struct.unpack_from('<I', d, 0)[0]
    sz = struct.unpack_from('<32I', d, 4)
    off = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    for i in range(32):
        if sz[i]:
            off += 0x40
            if i == s:
                return d[off:off + sz[i]]
            off += sz[i]
    return None


f = open(VBF, 'rb')
names, blocks = vbfextract.load_index(f)
packs = sorted(n for n in names if n.lower().endswith('.mpk'))
shape = collections.Counter()
cnt1 = 0
recs = 0
big = []
top = []
for p in packs:
    b = slot16(vbfextract.read_entry(f, names, blocks, p), 16)
    if b is None or len(b) < 0x20 or b[:4] != b'SP1\0':
        continue
    offC = struct.unpack_from('<I', b, 0x0C)[0]
    if not offC or offC + 2 > len(b):
        continue
    bound = struct.unpack_from('<H', b, offC)[0]
    offs = struct.unpack_from('<%dH' % bound, b, offC + 2)
    for o in offs:
        if not o or o + 0x40 > len(b):
            continue
        recs += 1
        sh = b[o + 9] & 0x7F
        n = struct.unpack_from('<I', b, o + 0x14)[0]
        shape[sh] += 1
        cnt1 += (n == 1)
        if sh == 2:
            top.append((n, p.split('/')[-1], hex(o)))
        if sh == 2 and n >= 128:
            big.append((n, p.split('/')[-1], hex(o)))
top.sort(reverse=True)
print("packs %d  records %d  shapes %s  count==1 %d" % (len(packs), recs, dict(sorted(shape.items())), cnt1))
print("CONTROL page census: records 2326, shape-2 400, count==1 2265 ->",
      "PASS" if (recs, shape[2], cnt1) == (2326, 400, 2265) else "MISMATCH (%d, %d, %d)" % (recs, shape[2], cnt1))
print("largest shape-2 counts:", top[:8])
print("shape-2 records with count >= 128:", big if big else "NONE")
print("FAILS", 0 if not big else len(big))
