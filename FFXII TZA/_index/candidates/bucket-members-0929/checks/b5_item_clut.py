"""B5 Item_Clut.bin (kind 7 idx 0x99). Claim: 7 palettes x 256 entries x 4 bytes (R,G,B,A with PS2 alpha 0x80);
requested by the 10-file loop 00291C80 (kind 7, ids 0x98+i, slot table 0209BEA0 stride 16); the task 00291D90 copies
the slots into its object at +0xC8+16*i, so the Item_Clut buffer is obj+0xE0; 00292390 reads it and selects palette
(itemGraphicId >> 6) at buffer + (id>>6)*0x400, pairing with Item_Gra0N (slot (id>>6)+2)."""
import struct
from common import *
header()
print("== static")
for i, want in enumerate(["itemgra_c.tm2", "Item_Clut.bin"] + [f"Item_Gra0{k}.as7" for k in range(8)]):
    check(f"kind 7 idx {0x98 + i:#x} = {want}", (kind_path(7, 0x98 + i) or "").endswith(want), kind_path(7, 0x98 + i))
check("00291C9A: slot table base 0209BEA0", rip_target(0x291C9A) == 0x209BEA0)
expect_ins(0x291CB8, "lea edx, [rbx + 0x98]"); expect_ins(0x291CC2, "mov ecx, 7"); expect_ins(0x291CD2, "call 0x24ab90")
expect_ins(0x24AB93, "jmp 0x32e400")
expect_ins(0x291CEA, "mov qword ptr [r14 + 8], rax")
expect_ins(0x291CF3, "lea edx, [rbx + 0x98]"); expect_ins(0x291D04, "call 0x32e620")
expect_ins(0x291D0E, "lea r14, [r14 + 0x10]"); expect_ins(0x291D12, "cmp ebx, 0xa")
check("completion 00291C60 clears the slot's pending word in 0209BEA0", rip_target(0x291C63) == 0x209BEA0)
expect_ins(0x291EE3, "shl rax, 4"); expect_ins(0x291EF2, "movups xmmword ptr [rax + rdi + 0xc8], xmm0")
expect_ins(0x29207F, "mov rax, qword ptr [rdx + rax*8]"); expect_ins(0x292078, "add rax, 0xd")
expect_ins(0x2924FD, "test byte ptr [rdx + 0x168], 2"); expect_ins(0x292506, "mov rdi, qword ptr [rdx + 0xe0]")
expect_ins(0x2926C7, "test byte ptr [rdx + 0x168], 2"); expect_ins(0x2926D0, "mov r14, qword ptr [rdx + 0xe0]")
expect_ins(0x292748, "sar r15d, 6"); expect_ins(0x29278A, "shl eax, 0xa"); expect_ins(0x292790, "add rcx, r14")
expect_ins(0x292793, "mov qword ptr [rbp + 0x10], rcx")
expect_ins(0x2926A6, "sar ecx, 6"); expect_ins(0x2926A9, "add ecx, 2"); expect_ins(0x2926AC, "call 0x292050")
sw = open("b5_refsweep_0209BEA0.txt").read()
check("raw sweep 0209BEA0..0209BF40: only 00291C60/00291C80/00291D90 touch the slot table", "(a) rip-relative confirmed: 5" in sw and "(b) dword hits: 0" in sw and "CONTROL 00291C9A: PASS" in sw)
print("== corpus")
files = copies("ps2data/image/ff12/myoshiok/*/bin_menu/item_clut.bin")
check("2 copies", len(files) == 2)
blobs = {open(f, "rb").read() for f in files}
check("copies byte-identical", len(blobs) == 1)
b = next(iter(blobs))
check(f"size {len(b)} == 7 * 256 * 4", len(b) == 7 * 1024)
alpha = [b[i] for i in range(3, len(b), 4)]
check("alpha byte is 0x80 in 1791 of 1792 entries, 0x00 once (palette 3 entry 0)", alpha.count(0x80) == 1791 and alpha.count(0) == 1 and alpha[3 * 256] == 0)
gra = copies("ps2data/image/ff12/myoshiok/in/bin_menu/item_gra0*.as7")
check("8 Item_Gra0N.as7 files ship (groups 0..7) against 7 palettes", len(gra) == 8, str(len(gra)))
for g in gra:
    h = open(g, "rb").read(16)
    print(f"  {g[-15:]}: magic {h[:2]!r} size {len(open(g, 'rb').read())}")
finish()
