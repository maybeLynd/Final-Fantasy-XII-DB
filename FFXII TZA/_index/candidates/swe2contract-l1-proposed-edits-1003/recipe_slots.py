#!/usr/bin/env python3
"""recipe_slots.py - settle CONTRACT-preparation-step-family §14's out-of-range-slot question against the shipped
recipes (SWE2-CONTRACT, 2026-10-03, for OPUS-REQ-CONTRACT-L1-PROPOSED-EDITS-1003 item 3).

Reads the shipping image only. For each of the 109 pointers of the recipe table 01EF96C0 (CONTRACT-weapon-recipes RW-1)
it decodes the two -1-terminated i32 slot lists (RW-2) and checks every slot against the step table's 202 entries
(0..201, CONTRACT-formula-step-table). Prints per-list extremes and every out-of-range slot, then FAILS <n>.
Controls:
  K1  the 110th qword after the table is 000000B4FFFFFFFF, not an address (RW-1's own end marker);
  K2  recipe 25 decodes to RW-2's published lists (positive control on the decoder);
  K3  sensitivity: the range check, applied to a synthetic list holding 202 and -2, flags both.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import kit_paths as KP  # noqa: E402

DATA = open(KP.EXE, "rb").read()
PE = struct.unpack_from("<I", DATA, 0x3C)[0]
NSEC = struct.unpack_from("<H", DATA, PE + 6)[0]
OPT = struct.unpack_from("<H", DATA, PE + 20)[0]
BASE = struct.unpack_from("<Q", DATA, PE + 24 + 24)[0]
SECT = PE + 24 + OPT
TABLE, COUNT, STEPS = 0x01EF96C0, 109, 202


def section(va):
    rva = va - BASE
    for i in range(NSEC):
        s = SECT + 40 * i
        name = DATA[s:s + 8].rstrip(b"\0").decode()
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", DATA, s + 8)
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return name, rptr + rva - vaddr, rva - vaddr < rsize
    return None, None, False


def q(va):
    return struct.unpack_from("<Q", DATA, section(va)[1])[0]


def lists(ptr):
    _, o, _ = section(ptr)
    out, cur = [], []
    while len(out) < 2:
        v = struct.unpack_from("<i", DATA, o)[0]
        o += 4
        if v == -1:
            out.append(cur)
            cur = []
        else:
            cur.append(v)
        if len(cur) > 512:
            raise ValueError("unterminated list at %08X" % ptr)
    return out


def out_of_range(xs):
    return [x for x in xs if not 0 <= x < STEPS]


fails = 0


def check(name, ok, detail):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


end = q(TABLE + 8 * COUNT)
check("K1 table end marker", end == 0x000000B4FFFFFFFF, "%016X" % end)
r25 = lists(q(TABLE + 8 * 25))
check("K2 recipe 25 decodes as RW-2", r25 == [[5, 6, 22, 33, 34, 35, 42], [29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]],
      r25)
check("K3 range check flags 202 and -2", out_of_range([0, 201, 202, -2]) == [202, -2], out_of_range([0, 201, 202, -2]))

bad, sizes, lo, hi, secs = [], [], 10 ** 9, -10 ** 9, set()
for rid in range(COUNT):
    ptr = q(TABLE + 8 * rid)
    name, _, raw = section(ptr)
    secs.add((name, raw))
    pre, com = lists(ptr)
    sizes.append((len(pre), len(com)))
    for which, xs in (("first", pre), ("second", com)):
        for x in xs:
            lo, hi = min(lo, x), max(hi, x)
        for x in out_of_range(xs):
            bad.append((rid, which, x))
print("recipes %d; pointer sections %s; slots per list: first %d..%d, second %d..%d; smallest slot %d, largest %d"
      % (COUNT, sorted(secs), min(s[0] for s in sizes), max(s[0] for s in sizes), min(s[1] for s in sizes),
         max(s[1] for s in sizes), lo, hi))
print("slot values in both lists, all recipes: %d" % sum(a + b for a, b in sizes))
check("R1 every shipped slot indexes the 202-entry step table", not bad, bad if bad else "no out-of-range slot")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
