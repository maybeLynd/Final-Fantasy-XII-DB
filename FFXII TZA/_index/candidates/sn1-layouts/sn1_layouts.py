"""SN-1 (OPUS, 2026-09-27): the .sbn line index and the .dbg native-command name directory, read from the four ATEL
control-script companions (ctrl, btlctrl, evctrl, mapctrl; ps2data/image/ff12/in/bin).

  S1 .sbn = u32 blockCount; u32 blockOffset[blockCount]; each block = u32 lineCount, then ceil(lineCount / 32) groups.
     Group 0 = u32 base (the block header's second word) + u16 lineStart[32]; each later group = u32 base + u16
     lineStart[<= 32]. A line starts at base + lineStart, relative to its group's base. Zero bytes follow the last group
     up to group 0's base, where the NUL-separated text begins. Checked in all 10 blocks: line total = lineCount, every
     line start lies in the block's text and follows a NUL, every group's base = its first line, and the gap is zeros.
     So the header's 'second word' is the ABSOLUTE FILE OFFSET of the block's text.
  S2 the plain reading 'u16[lineCount] line-start offsets' fails: past 32 lines it takes a base's halves as line starts.
  D1 .dbg +0x2C = u32 sectionOffset[16]; section k = u32 count + u32 nameOffset[count], each relative to the string pool
     whose offset is the header's second pair (+0x08). Every name in every section of all four files is a string start.
  D2 section k, entry i names native command (k << 12) + i: 7,297 of the 7,303 names agree with the verb catalogue
     (gen_req_channel_census.load_verbs, which disambiguates repeats with an '_<index>' suffix). The other six are one
     pair: 0x20C8 / 0x20C9 are debug_set / get_jfdemo_status in ctrl, btlctrl and mapctrl, e3demo in evctrl and the
     catalogue - the modules were built from different verb tables.
  D3 a constant shift from file offset 0 does not resolve the names (the pool base is required).
  D4 section 0's offsets fall back ('reset') only where the name already occurred earlier in the section: the pool
     stores each name once, so the '67 ascending sub-lists' are de-duplication, not a category directory.
  S3 the published reading of the page trailer as the chunk's LAST byte (lines of later pages one byte on) puts most
     line starts off a NUL boundary; S4 the trailer is a u32 - its high half is non-zero once text passes 64 KB.
Not claimed: the .dbg header's first and third pairs ({u32 count; u32 offset[..]} over records not read here), the
.msb flag, or what the per-module class-0 counts (1,410 / 1,389 / 1,436 / 1,407) say about build dates.
Usage: python sn1_layouts.py [dir]
"""
import os, re, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "agent_flow", "tools")))  # vbfextract, which the census module imports
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok


def sbn_blocks(b):
    n = struct.unpack_from("<I", b, 0)[0]; offs = struct.unpack_from("<%dI" % n, b, 4)
    return list(zip(offs, list(offs[1:]) + [len(b)]))


def sbn_group_read(b, o):
    L, base = struct.unpack_from("<II", b, o); p = o + 8; lines, groups, rem = [], [base], L
    while rem > 0:
        k = min(32, rem); lines += [base + r for r in struct.unpack_from("<%dH" % k, b, p)]; p += 2 * k; rem -= k
        if rem > 0:
            base = struct.unpack_from("<I", b, p)[0]; p += 4; groups.append(base)
    return L, groups, lines, p


def ok_lines(b, lines, X, e):
    return all(X <= a < e and (a == X or b[a - 1] == 0) for a in lines) and lines == sorted(lines)


s1 = s2 = True; nb = 0; tot = after_plus1 = 0; trailers = hi = 0
for m in MODS:
    b = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    for o, e in sbn_blocks(b):
        nb += 1
        L, groups, lines, p = sbn_group_read(b, o); X = groups[0]
        s1 &= len(lines) == L and ok_lines(b, lines, X, e) and all(groups[j] == lines[32 * j] for j in range(len(groups))) \
              and p <= X and not any(b[p:X])
        plain = [X + r for r in struct.unpack_from("<%dH" % L, b, o + 8)]
        for j, a in enumerate(lines):  # the published 'chunkEnd = last byte' reading puts later pages one byte on
            tot += 1; a2 = a + (1 if j >= 32 else 0); after_plus1 += b[a2 - 1] == 0
        for base in groups[1:]:
            trailers += 1; hi += (base >> 16) != 0
        s2 &= not (L > 32 and ok_lines(b, plain, X, e))
check("S1 .sbn 32-line groups, second word = absolute text offset", s1 and nb == 10, "(%d blocks)" % nb)
check("S2 plain u16[lineCount] reading rejected", s2)
check("S3 'chunkEnd = last byte of the chunk' (+1) reading rejected", after_plus1 < tot // 2, "(%d of %d line starts follow a NUL, against %d of %d)" % (after_plus1, tot, tot, tot))
check("S4 the page trailer is a u32, not {u16 chunkEnd; u16 0}", hi > 0, "(%d of %d trailers have a non-zero high u16)" % (hi, trailers))

import gen_req_channel_census as G
V = G.load_verbs()
d1 = d3 = d4 = True; total = 0; diff = set(); nres = []
for m in MODS:
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    pool = struct.unpack_from("<I", b, 8)[0]; tab = struct.unpack_from("<16I", b, 0x2C)
    for k, s in enumerate(tab):
        c = struct.unpack_from("<I", b, s)[0]
        offs = struct.unpack_from("<%dI" % c, b, s + 4) if c else ()
        for i, o in enumerate(offs):
            a = pool + o; total += 1
            d1 &= b[a - 1] == 0 and 0x20 < b[a] < 0x7F
            nm = b[a:b.index(b"\0", a)].decode("cp932", "replace"); vid = (k << 12) + i
            if not (vid in V and re.sub(r"_%x$" % i, "", V[vid][2]) == nm): diff.add((m, vid, nm))
        if k == 0:  # D4: the section's 'reset' points are exactly the names already seen earlier in it
            names = [b[pool + o:b.index(b"\0", pool + o)] for o in offs]
            resets = [i for i in range(1, len(offs)) if offs[i] < offs[i - 1]]
            d4 &= bool(resets) and all(names[i] in names[:i] for i in resets)
            nres.append(len(resets) + 1)
        if len(offs) > 16:
            d3 &= not all(b[o - 1] == 0 and 0x20 < b[o] < 0x7F for o in offs[:16])
check("D1 .dbg names resolve through the pool at the header's second pair", d1, "(%d names)" % total)
JF = {(m, v, n) for m in ("ctrl", "btlctrl", "mapctrl") for v, n in ((0x20C8, "debug_set_jfdemo_status"), (0x20C9, "debug_get_jfdemo_status"))}
check("D2 section k entry i = native command (k << 12) + i", diff == JF, "(%d of %d agree; the 6 others are 0x20C8 / 0x20C9 named jfdemo in ctrl, btlctrl, mapctrl, e3demo in evctrl and the catalogue)" % (total - len(diff), total))
check("D3 unshifted offsets do not resolve", d3)
check("D4 section 0's 'sub-list resets' are repeated names (the pool stores a name once)", d4, "(sub-list counts %s)" % nres)
print("FAILS", fails); sys.exit(1 if fails else 0)
