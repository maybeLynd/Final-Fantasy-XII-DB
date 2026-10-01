"""B7 summoneffectdata.bin (kind 9 idx 0x2A). The file is read straight INTO the .data buffer 02AD9B60 (0032E620's
r8 is the destination, callback 0). Claim: 64 records x 10 bytes {u8 r1,g1,b1 (x0.01), u8 r2,g2,b2 (x0.01),
u8 c0,c1,c2,c3}, indexed by (003B5340() - 1); tail +0x280 f32, +0x284 f32, +0x288 f32, +0x28C f32, +0x290 u32,
+0x294 u32, +0x298 8 bytes (no reader). 640 + 16 + 8 + 8 = 672."""
import struct
from common import *
header()
print("== static")
check("kind 9 idx 0x2A path", (kind_path(9, 0x2A) or "").endswith(r"common\summoneffectdata.bin"), kind_path(9, 0x2A))
expect_ins(0x3B53CB, "mov edx, 0x2a"); expect_ins(0x3B53EA, "lea ecx, [rdx - 0x21]"); expect_ins(0x3B5407, "call 0x32e400")
check("003B541D: destination buffer r8 = 02AD9B60 (lea, not a pointer load)", rip_target(0x3B541D) == 0x2AD9B60 and ins_at(0x3B541D).startswith("lea r8"))
expect_ins(0x3B5411, "mov qword ptr [rsp + 0x20], 0"); expect_ins(0x3B5427, "call 0x32e620")
# record readers
check("0036FC12 lea base 02AD9B60", rip_target(0x36FC12) == 0x2AD9B60)
expect_ins(0x36FC19, "dec eax"); expect_ins(0x36FC1B, "lea rdx, [rax + rax*4]")
for a, k in ((0x36FC34, "[rcx + rdx*2]"), (0x36FC28, "[rcx + rdx*2 + 1]"), (0x36FC1F, "[rcx + rdx*2 + 2]"),
             (0x36FC7B, "[rcx + rdx*2 + 3]"), (0x36FC6F, "[rcx + rdx*2 + 4]"), (0x36FC66, "[rcx + rdx*2 + 5]")):
    expect_ins(a, "movzx eax, byte ptr " + k)
check("0036FC0A scale constant is 0.01", struct.unpack_from("<f", d, off(rip_target(0x36FC0A)))[0] == struct.unpack("<f", struct.pack("<f", 0.01))[0])
check("0036FA09 lea base 02AD9B60", rip_target(0x36FA09) == 0x2AD9B60)
for a, k in ((0x36FAC8, "+ 6]"), (0x36FAE5, "+ 7]"), (0x36FB02, "+ 8]"), (0x36FB1F, "+ 9]")):
    expect_ins(a, "movzx eax, byte ptr [rcx + rdx*2 " + k)
for a, t in ((0x36FA30, 0x2AD9DE0), (0x36FA46, 0x2AD9DE4), (0x36F7AA, 0x2AD9DE8), (0x36F5AE, 0x2AD9DEC), (0x36F583, 0x2AD9DF0), (0x36F561, 0x2AD9DF4)):
    check(f"{a:08X} reads buffer +{t - 0x2AD9B60:#x}", rip_target(a) == t, ins_at(a))
expect_ins(0x36F592, "sub ecx, r8d"); expect_ins(0x36F576, "mov eax, 0x55555556")
sw = open("b7_refsweep_02AD9B60.txt").read()
check("raw sweep 02AD9B60..02AD9E00: 9 rip refs (loader lea + 8 reads), none at +0x298..+0x29F, no dword/qword hit",
      "(a) rip-relative confirmed: 9" in sw and "02AD9DF8" not in sw and "02AD9DFC" not in sw and "(b) dword hits: 0" in sw and "(c) qword pointer hits: 0" in sw)
expect_ins(0x3B53A8, "movzx eax, byte ptr [rsp + 8]")   # the 1-based index is a byte
print("== corpus")
files = copies("ps2data/image/ff12/**/summoneffectdata.bin")
check("one shipped copy", len(files) == 1, str(files))
b = open(files[0], "rb").read()
check(f"size arithmetic 64*10 + 4*4 + 2*4 + 8 == {len(b)}", 64 * 10 + 16 + 8 + 8 == len(b))
recs = [b[10 * i:10 * i + 10] for i in range(64)]
neutral = bytes([100] * 6 + [0x80, 0x80, 0x80, 0x20])
nn = [i for i, r in enumerate(recs) if r != neutral]
print(f"  non-neutral records: {len(nn)} -> indices {nn[0]}..{nn[-1]}; neutral record = scale 1.00 x6, colour 80 80 80 20")
check("records 28..63 are the neutral record exactly", nn == list(range(len(nn))) and all(r == neutral for r in recs[len(nn):]))
check("colour byte +9 is 0x30 (or 0x20/0x32/0x26 etc) - every record's +9 <= 0x80", all(r[9] <= 0x80 for r in recs))
f = struct.unpack_from("<4f", b, 0x280); u = struct.unpack_from("<2I", b, 0x290)
print(f"  tail: f32 {[round(x, 4) for x in f]}  u32 {u} ({[hex(x) for x in u]})  pad {b[0x298:].hex()}")
check("tail u32 pair are 16-bit values (<= 0xFFFF), consistent with (0xFFFF - v) << 12 | 0xFF0 at 0036F8EC..0036F905", all(x <= 0xFFFF for x in u))
check("+0x298..+0x29F zero", b[0x298:] == bytes(8))
for i in (0, 1, 27):
    r = recs[i]; print(f"  rec {i}: scale1 {[x / 100 for x in r[:3]]} scale2 {[x / 100 for x in r[3:6]]} colour {r[6:].hex(' ')}")
finish()
