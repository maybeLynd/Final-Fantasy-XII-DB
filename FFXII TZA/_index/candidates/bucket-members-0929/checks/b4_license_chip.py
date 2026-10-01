"""B4 license_chip.bin (kind 7 idx 0x7E). Claim: 361 chip ids x 2 variants x 32-byte records (id*64 + variant*32);
a record is 4 layers x 8 bytes {u16 sprite code (0xFFFF = empty), u16 w2, u8 +4, u8 +5, s8 +6 dx, s8 +7 dy}.
Consumers: 0055BAC0 (draw loop over the 4 layers of record 2*id + (state>=5)), 00556590 (w2 of record 2*id+1),
0055F010 (w2 of record 2*id). The 0xFFFF id fallback indexes record 0x2D2/0x2D3 = byte 0x5A40/0x5A60 = file end."""
import struct
from common import *
header()
print("== static")
check("kind 7 idx 0x7E path", (kind_path(7, 0x7E) or "").endswith(r"Bin_Menu\license_chip.bin"), kind_path(7, 0x7E))
expect_ins(0x56165F, "lea r8d, [rdx + 0x77]"); expect_ins(0x561663, "call 0x249210")
expect_ins(0x561675, "mov rcx, qword ptr [rax + 8]")
expect_ins(0x561680, "mov qword ptr [rsi + 0x118], rcx")
check("0056168B publishes the buffer to 02CA9670", rip_target(0x56168B) == 0x2CA9670)
sw = open("b4_refsweep_02CA9670.txt").read()
check("raw sweep 02CA9670: 6 rip refs (1 store + 5 reads in 3 functions), no dword/qword hit",
      "(a) rip-relative confirmed: 6" in sw and "(b) dword hits: 0" in sw and "(c) qword pointer hits: 0" in sw and "CONTROL 0056168B: PASS" in sw)
# 0055BAC0 record select + layer loop
expect_ins(0x55BC20, "mov r14d, dword ptr [r13 + 0xd]"); expect_ins(0x55BC24, "shr r14d, 4")
expect_ins(0x55BC66, "setae al"); expect_ins(0x55BC61, "movzx ecx, word ptr [r13 + 3]")
expect_ins(0x55BC73, "lea rdx, [rax + rcx*2]"); expect_ins(0x55BC7B, "add rdx, 0x2d2"); expect_ins(0x55BC82, "shl rdx, 5")
check("0055BC86 adds the license_chip base", rip_target(0x55BC86) == 0x2CA9670)
expect_ins(0x55BC9D, "lea rbp, [rdx + 4]"); expect_ins(0x55BCA5, "mov r15d, 4")
expect_ins(0x55BCD0, "movzx ebx, word ptr [rbp - 4]"); expect_ins(0x55BCD4, "cmp ebx, edi")
expect_ins(0x55BCDC, "cmp ebx, 0x8000"); expect_ins(0x55BDEA, "cmp ebx, 0x4000")
expect_ins(0x55BD18, "movzx eax, byte ptr [rbp + 1]"); expect_ins(0x55BD33, "movzx eax, byte ptr [rbp]")
expect_ins(0x55BD95, "movsx eax, byte ptr [rbp + 2]"); expect_ins(0x55BDA2, "movsx eax, byte ptr [rbp + 3]")
expect_ins(0x55BE60, "add rbp, 8")
# 00556590 / 0055F010: word +2
expect_ins(0x556599, "movzx eax, word ptr [rcx + 0xe]"); expect_ins(0x5565B1, "add rax, 0x20"); expect_ins(0x5565B5, "shl rcx, 6")
expect_ins(0x5565BC, "movzx eax, word ptr [rax + 2]"); expect_ins(0x5565C8, "add rax, 0x5a60")
expect_ins(0x55F0C2, "shl rax, 6"); expect_ins(0x55F0CD, "movzx edi, word ptr [rax + 2]"); expect_ins(0x55F0DA, "add rax, 0x5a40")
print("== corpus")
files = copies("ps2data/image/ff12/myoshiok/*/bin_menu/license_chip.bin")
check("2 copies (ch, in)", len(files) == 2, str(len(files)))
blobs = {open(f, "rb").read() for f in files}
check("copies byte-identical", len(blobs) == 1)
b = next(iter(blobs))
check(f"size {len(b)} == 361 ids * 2 variants * 32 B == {361 * 64}", len(b) == 361 * 64)
check("0xFFFF fallback record 0x2D2 starts exactly at the file end (0x5A40)", 0x2D2 * 32 == len(b))
recs = [b[32 * i:32 * i + 32] for i in range(len(b) // 32)]
layers = [(r, k, struct.unpack_from("<HHBBbb", r, 8 * k)) for r in recs for k in range(4)]
empty = [L for L in layers if L[2][0] == 0xFFFF]
check(f"every empty layer (sprite 0xFFFF, {len(empty)}) has its other 6 bytes zero", all(L[2][1:] == (0, 0, 0, 0, 0) for L in empty))
nonfirst_w2 = [L for L in layers if L[1] > 0 and L[2][1] != 0]
check("word +2 is zero in layers 1-3 of every record (only layer 0 carries it; its readers read record+2 only)", not nonfirst_w2, str(len(nonfirst_w2)))
codes = [L[2][0] for L in layers if L[2][0] != 0xFFFF]
bands = {"<0x300": 0, "0x300-0x3FFF": 0, "0x4000-0x7FFF": 0, ">=0x8000": 0}
for c in codes:
    bands["<0x300" if c < 0x300 else "0x300-0x3FFF" if c < 0x4000 else "0x4000-0x7FFF" if c < 0x8000 else ">=0x8000"] += 1
print("  non-empty layer sprite-code bands (the three atlases 0055BAC0 selects by):", bands)
print("  layer-0 word +2 values:", sorted({struct.unpack_from('<H', r, 2)[0] for r in recs}))
used = sum(1 for i in range(361) if recs[2 * i][:2] != b"\xff\xff" or recs[2 * i + 1][:2] != b"\xff\xff")
print(f"  ids with at least one non-empty layer-0: {used}/361")
dx = sorted({L[2][4] for L in layers if L[2][0] != 0xFFFF}); dy = sorted({L[2][5] for L in layers if L[2][0] != 0xFFFF})
print(f"  dx range {dx[0]}..{dx[-1]}, dy range {dy[0]}..{dy[-1]}")
finish()
