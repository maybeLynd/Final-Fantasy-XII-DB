"""Read the two achievement records inside shipped menuhandbook.bin (kind 7, id 0xC8).

SWE2-DATA, 2026-09-18, for FABLE-REQ-SWE2-DATA-HANDBOOK-MONSTER-LIST-AND-COUNTER-MASK.

The blob at [022C2550] is walked by 003165C0 / 00315FFA as a chain of u16
self-relative offsets starting at blob+8: pos += u16[pos], four hops total,
32-bit arithmetic. Hop 3 lands on the mode-7 monster-id list (u16 count at +2,
u16 ids at +4); hop 4 lands on the mode-0 override record (u16, u16, mask dword
at +4, override dwords from +8). 003165C0(id) tests bit id of the mask, counts
the set bits below id, and returns the dword at that rank.

Usage: extract us menuhandbook.bin with vbfextract.py, then
    python read_menuhandbook_hops.py <menuhandbook.bin>
Output: the TSV rows of members/menuhandbook-achievement-records.tsv.
"""
import struct, sys

d = open(sys.argv[1], "rb").read()

pos = 8
for hop in range(4):
    step = struct.unpack_from("<H", d, pos)[0]
    pos = (pos + step) & 0xFFFFFFFF

# pos is now hop-4 (fourth hop) — but we need hop-3's record too; re-walk.
pos3 = 8
for hop in range(3):
    pos3 = (pos3 + struct.unpack_from("<H", d, pos3)[0]) & 0xFFFFFFFF

count = struct.unpack_from("<H", d, pos3 + 2)[0]
ids = [struct.unpack_from("<H", d, pos3 + 4 + 2 * i)[0] for i in range(count)]
print(f"# hop3 record at +{pos3:#x}: count={count}")
for i, m in enumerate(ids):
    print(f"monster_list\t{i}\t{m:#06x}\t{m}")

R = pos
w0, n = struct.unpack_from("<HH", d, R)
mask = struct.unpack_from("<I", d, R + 4)[0]
bits = [b for b in range(32) if mask >> b & 1]
vals = [struct.unpack_from("<I", d, R + 8 + 4 * i)[0] for i in range(n)]
print(f"# hop4 record at +{R:#x}: w0={w0:#x} n={n} mask={mask:#010x} popcount={len(bits)}")
for bit, val in zip(bits, vals):
    print(f"override\t{bit}\t{val}")
print(f"# end of record {R + 8 + 4 * n:#x}, file size {len(d):#x}")
