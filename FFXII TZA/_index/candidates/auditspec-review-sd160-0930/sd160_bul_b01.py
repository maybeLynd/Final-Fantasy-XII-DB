"""sd160_bul_b01.py - SWE2-AUDIT-SPEC (review of OPUS af6684173). Reads the one raw call pattern that no decoded
instruction covers (bul_b01.ebp sec+0x26E9C, all nine languages; sd160_rawgap.out): which script segment it lies in,
where that segment's linear decode stops, the bytes around it, and a decode resumed at the hit.
"""
import struct
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
b = open("D:/FFXII_TZA_extract/ps2data/plan_master/us/plan_map/bul_b/bul_b01/global/bul_b01.ebp", "rb").read()
sec = b[0x80:0x80 + U32(b, 0x84)]
d = U32(sec, 0x18); n = U32(sec, d); pool = U32(sec, 0x4C)
print("sec len %X dir %X n %d pool %X" % (len(sec), d, n, pool))
names = {}
for s in range(n):
    e = d + 4 + s * 0x30
    o = pool + U32(sec, e)
    names.setdefault(U32(sec, e + 8), sec[o:sec.find(b"\0", o)].decode("cp932", "replace"))
st = sorted(names)
x = 0x26E9C
prev = [s for s in st if s <= x]; nxt = [s for s in st if s > x]
print("segment start %X (%s), next start %s" % (prev[-1], names[prev[-1]], hex(nxt[0]) if nxt else None))
print("bytes x-24..x+12:", sec[x - 24:x + 12].hex(" "))
pc = prev[-1]; end = nxt[0] if nxt else d
while pc < end:
    op = sec[pc]
    if op > 0x63:
        print("segment decode stops at %X op %02X (hit is %X bytes later)" % (pc, op, x - pc))
        break
    pc += 3 if op >= 0x48 else 1
else:
    print("segment decoded to end %X" % pc)
print("resumed decode from x-12:")
pc = x - 12
for _ in range(10):
    op = sec[pc]
    if op >= 0x48:
        print("  %X  %02X %04X" % (pc, op, sec[pc + 1] | sec[pc + 2] << 8)); pc += 3
    else:
        print("  %X  %02X" % (pc, op)); pc += 1
