"""ddgp_corr_check.py - controls for FABLE's corrections to the DD gameplay pages on SWE2-AUDIT-SEM's review
(auditsem-review-dd-gameplay-0930, C1 and C4). Reads the shipping image; prints PASS/FAIL per check, then FAILS n.

C1 (GR-12): 00273270's two early exits land on `mov eax, 0xffff`; the only other answer is the `shr eax, 0x10` of a
     dword preset to 0x0000FFFF before the filler 0031FF70 runs.
C4 (GR-19): every rel32 call / jmp and every rip-relative lea that targets 003377C0 or 00337700, image-wide.
     Positive control: the drop gate 00319490 must be found calling 003377C0 (the call GR-19 already cites).
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000  # canonical addresses include the image base

data = open(EXE, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]
optsz = struct.unpack_from("<H", data, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + 40 * i
    name = data[o:o + 8].rstrip(b"\0").decode()
    vsz, va, rsz, raw = struct.unpack_from("<IIII", data, o + 8)
    secs.append((name, va, vsz, raw, rsz))
def off(addr):
    rva = addr - BASE
    for _, va, vsz, raw, rsz in secs:
        if va <= rva < va + max(vsz, rsz): return raw + (rva - va)
    raise ValueError(hex(addr))
def rd(addr, n): o = off(addr); return data[o:o + n]

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: fails += 1

# C1 - byte-exact instructions at the addresses the correction cites.
check("C1 0027328F je -> 002732C1", rd(0x27328F, 2) == bytes.fromhex("7430"))
check("C1 00273299 je -> 002732C1", rd(0x273299, 2) == bytes.fromhex("7426"))
check("C1 002732C1 mov eax,0xffff", rd(0x2732C1, 5) == bytes.fromhex("b8ffff0000"))
check("C1 0027329B mov eax,0xffff (preset value)", rd(0x27329B, 5) == bytes.fromhex("b8ffff0000"))
check("C1 002732A7 mov [rsp+0xcc],eax (preset store)", rd(0x2732A7, 7) == bytes.fromhex("898424cc000000"))
check("C1 002732B0 call 0031FF70 (the filler)",
      rd(0x2732B0, 1) == b"\xe8" and 0x2732B5 + struct.unpack("<i", rd(0x2732B1, 4))[0] == 0x31FF70)
check("C1 002732BC shr eax,0x10", rd(0x2732BC, 3) == bytes.fromhex("c1e810"))

# C4 - image-wide references to the two placement predicates in .text.
text = [s for s in secs if s[0] == ".text"][0]
_, va, vsz, raw, rsz = text
buf = data[raw:raw + rsz]
targets = {0x3377C0: [], 0x337700: []}
for i in range(len(buf) - 7):
    b = buf[i]
    here = BASE + va + i
    if b in (0xE8, 0xE9):
        t = here + 5 + struct.unpack_from("<i", buf, i + 1)[0]
        if t in targets: targets[t].append(("call" if b == 0xE8 else "jmp", here))
    if b in (0x48, 0x4C) and buf[i + 1] == 0x8D and (buf[i + 2] & 0xC7) == 0x05:
        t = here + 7 + struct.unpack_from("<i", buf, i + 3)[0]
        if t in targets: targets[t].append(("lea", here))
for t, refs in targets.items():
    print("refs to %08X: %s" % (t, ", ".join("%s %08X" % r for r in refs)))
calls_7c0 = [a for k, a in targets[0x3377C0] if k == "call"]
check("C4 control: 00319490 calls 003377C0", any(0x319490 <= a < 0x319490 + 0x94 for a in calls_7c0))
def in_fn(a, lo, size): return lo <= a < lo + size
check("C4 00334E00 calls 003377C0 twice", sum(in_fn(a, 0x334E00, 882) for a in calls_7c0) == 2)
check("C4 0033BD70 calls 003377C0", any(in_fn(a, 0x33BD70, 351) for a in calls_7c0))
check("C4 00317DE0 takes both by lea",
      any(k == "lea" and in_fn(a, 0x317DE0, 111) for k, a in targets[0x3377C0]) and
      any(k == "lea" and in_fn(a, 0x317DE0, 111) for k, a in targets[0x337700]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
