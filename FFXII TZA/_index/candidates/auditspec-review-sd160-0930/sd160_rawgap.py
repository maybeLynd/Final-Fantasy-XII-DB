"""sd160_rawgap.py - SWE2-AUDIT-SPEC (review of OPUS af6684173). Accounts for the raw 3-byte call patterns that the
decoded census (sd160_indep_census.py) does not count: 63,446 raw vs 63,432 decoded. For each raw hit not at a decoded
call pc, prints the file, the hit's offset relative to the section, and the decoded instruction that covers that byte
(if any) - so a real call missed by a decode stop would show as a hit NOT covered by any decoded instruction. Also
lists the .ebp files without a 0x8000000B section.
"""
import os, struct, collections

ROOT = "D:/FFXII_TZA_extract"
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = (0x265, 0x3005)
CALLS = (0x58, 0x59, 0x5D, 0x5E)
nosec, gaps = [], []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.lower().endswith(".ebp"):
            continue
        p = os.path.join(dp, f)
        b = open(p, "rb").read()
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        raws = []
        for imm in WANT:
            for op in CALLS:
                pat = bytes((op, imm & 0xFF, imm >> 8))
                i = b.find(pat)
                while i >= 0:
                    raws.append(i)
                    i = b.find(pat, i + 1)
        if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B:
            nosec.append((rel, len(b), len(raws)))
            continue
        if not raws:
            continue
        sec = b[0x80:0x80 + U32(b, 0x84)]
        d = U32(sec, 0x18); n = U32(sec, d)
        starts = sorted(set(U32(sec, d + 4 + s * 0x30 + 8) for s in range(n)))
        edges = sorted(set(starts) | {d, len(sec)})
        cover = {}          # byte offset in sec -> (instruction pc, op)
        callpcs = set()
        for cs in starts:
            end = min([x for x in edges if x > cs] or [len(sec)])
            pc = cs
            while pc < end and pc < len(sec):
                op = sec[pc]
                if op > 0x63:
                    break
                ln = 3 if op >= 0x48 else 1
                if pc + ln > end:
                    break
                for k in range(ln):
                    cover[pc + k] = (pc, op)
                if op in CALLS and ln == 3 and (sec[pc + 1] | sec[pc + 2] << 8) in WANT:
                    callpcs.add(pc)
                pc += ln
        for r in raws:
            so = r - 0x80
            if so in callpcs:
                continue
            c = cover.get(so)
            gaps.append((rel, so, "covered by pc %X op %02X" % c if c else
                         ("OUTSIDE section" if not (0 <= so < len(sec)) else "NOT covered by any decoded instruction")))
print("ebp files without a 0x8000000B section: %d" % len(nosec))
for x in nosec:
    print("  %s size %d raw-hits %d" % x)
print("raw hits not at a decoded call pc: %d" % len(gaps))
for g in gaps:
    print("  %s sec+%X %s" % g)
print("by kind:", dict(collections.Counter(g[2].split(" pc")[0] for g in gaps)))
