"""adr_tally.py - tallies on the us battle_pack.bin action table (directory +0x3C) for the action-definition-row DD drafts
(FABLE, 2026-09-30). Reads only. Uses the UQ-80 record's pack.py for the section parse."""
import sys, struct, collections
import os
# installed beside the UQ-80 record (_index/candidates/dd-content-fable-0930/); the draft copy falls back to the live tree
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_here, "..", "uq80-table-field-coverage"),
           r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates/uq80-table-field-coverage"):
    if os.path.isfile(os.path.join(_p, "pack.py")):
        sys.path.insert(0, _p)
        break
import pack
recs, _h = pack.records(0x3C)
print("rows", len(recs), "stride", len(recs[0]))
w24 = [struct.unpack_from("<H", r, 0x24)[0] for r in recs]
print("+0x24: 0xFFFF", sum(1 for v in w24 if v == 0xFFFF), "| bit15 set (not FFFF)", sum(1 for v in w24 if v != 0xFFFF and v & 0x8000),
      "| bit15 clear", sum(1 for v in w24 if not v & 0x8000), "| distinct", len(set(w24)))
bit30 = [struct.unpack_from("<I", r, 0x0C)[0] >> 30 & 1 for r in recs]
print("+0x24 bit15 set (not FFFF) and +0x0C bit30 clear:", sum(1 for v, b in zip(w24, bit30) if v != 0xFFFF and v & 0x8000 and not b))
print("  those rows:", [(i, hex(v)) for i, (v, b) in enumerate(zip(w24, bit30)) if v != 0xFFFF and v & 0x8000 and not b][:40])
print("+0x24 bit15 clear and not FFFF, sample:", collections.Counter(v for v in w24 if not v & 0x8000).most_common(8))
b0A = collections.Counter(r[0x0A] for r in recs)
b0B = collections.Counter(r[0x0B] for r in recs)
print("+0x0A byte:", b0A.most_common(12), "max", max(b0A))
print("+0x0B byte:", b0B.most_common(12))
print("+0x0B nonzero rows:", [i for i, r in enumerate(recs) if r[0x0B]][:40])
print("+0x0A for rows 0-6 (Cure..):", [recs[i][0x0A] for i in range(7)])
b28 = [(i, r[0x28]) for i, r in enumerate(recs) if r[0x28]]
print("+0x28 nonzero:", len(b28), b28)
b3A = collections.Counter(r[0x3A] for r in recs)
print("+0x3A:", b3A.most_common())
b04 = collections.Counter(r[0x04] for r in recs)
print("+0x04:", b04.most_common(8))
