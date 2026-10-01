"""B1 mapjumpgroupflagrom.bin (FLAGROM1) - layout on every shipped copy + the loader/reader instructions.
Layout claim: +0 char[8] "FLAGROM1"; +8 u16 count; +0xA u16 offset[count] (absolute from file start, 0 = no
schedule); records are u16 lists: bits 0-14 threshold, bit 15 = last entry. Reader 00377970 walks them."""
import struct
from common import *
header()
print("== static: loader and reader")
check("kind 9 idx 0xA path", kind_path(9, 0xA) == r"PS2Data\image\ff12\in\bin\mapjumpgroupflagrom.bin", kind_path(9, 0xA))
expect_ins(0x378702, "mov edx, 0xa"); expect_ins(0x378707, "lea ecx, [rdx - 1]"); expect_ins(0x37870A, "call 0x32e400")
expect_ins(0x37874B, "lea rax, [rip")
check("completion callback is 00378BA0", rip_target(0x37874B) == 0x378BA0)
expect_ins(0x37876F, "call 0x32e620")
expect_ins(0x378BA0, "mov eax, ecx")        # 32-bit truncation of the delivered pointer
check("callback stores rax to 02ADD0C8", rip_target(0x378BA2) == 0x2ADD0C8 and "qword ptr" in ins_at(0x378BA2))
check("reader loads 02ADD0C8", rip_target(0x377976) == 0x2ADD0C8)
expect_ins(0x377984, "movzx eax, word ptr [rdx + 8]")          # count
expect_ins(0x37798F, "movzx ecx, word ptr [rdx + rax*2 + 0xa]") # offset table
expect_ins(0x377994, "test cx, cx")                            # 0 = no schedule
expect_ins(0x3779A4, "call 0x265270")                          # FieldData_GetVariable0
expect_ins(0x3779B5, "and eax, 0x7fff")                        # threshold
expect_ins(0x3779C0, "xor ebx, 1")                             # parity toggle
expect_ins(0x3779C6, "js ")                                    # bit 15 = last
check("magic FLAGROM1 not present as a literal anywhere in .text", d[0x600:0x7A0E00].find(b"FLAGROM1") < 0)
print("== corpus: every shipped copy")
files = copies("ps2data/image/ff12/*/bin/mapjumpgroupflagrom.bin")
check("9 locale copies", len(files) == 9, str(len(files)))
blobs = set()
for f in files:
    b = open(f, "rb").read(); blobs.add(b)
    n = struct.unpack_from("<H", b, 8)[0]
    offs = struct.unpack_from("<%dH" % n, b, 10)
    table_end = 10 + 2 * n
    ok_magic = b[:8] == b"FLAGROM1"
    ok_first = offs[0] == table_end
    ok_mono = all(offs[i] < offs[i + 1] for i in range(n - 1))
    ends = list(offs[1:]) + [len(b)]
    ok_term = True; nent = 0
    for o, e in zip(offs, ends):
        ws = struct.unpack_from("<%dH" % ((e - o) // 2), b, o)
        nent += len(ws)
        # exactly one terminator, and it is the last word of the record
        if (e - o) % 2 or not ws or [w >> 15 for w in ws] != [0] * (len(ws) - 1) + [1]: ok_term = False
    arith = table_end + 2 * nent == len(b)
    check(f"{f[-40:]}: magic, count {n}, offset[0]==table end {table_end:#x}, ascending, zero-free {0 not in offs}, "
          f"each record ends at its only bit-15 word, 10+2*{n}+2*{nent}=={len(b)}",
          ok_magic and ok_first and ok_mono and ok_term and arith, "")
check("all copies byte-identical", len(blobs) == 1)
b = next(iter(blobs)); n = struct.unpack_from("<H", b, 8)[0]
print(f"  count={n}; highest threshold index the image's gate call sites use is 0x67 (persistent-flag-banks.md): in range {0x67 < n}")
check("gate index 0x67 < count", 0x67 < n)
lens = {}
offs = struct.unpack_from("<%dH" % n, b, 10)
for o, e in zip(offs, list(offs[1:]) + [len(b)]): lens[(e - o) // 2] = lens.get((e - o) // 2, 0) + 1
print("  record lengths (entries: records):", dict(sorted(lens.items())))
for i in (0, 1, 4, 0xB, 0x67):
    o = offs[i]; e = offs[i + 1] if i + 1 < n else len(b)
    ws = struct.unpack_from("<%dH" % ((e - o) // 2), b, o)
    print(f"  record {i:#x} @ {o:#x}: " + " ".join(f"{w & 0x7FFF}{'|END' if w >> 15 else ''}" for w in ws))
finish()
