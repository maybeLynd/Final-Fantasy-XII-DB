"""Are command 0x2C's 'from' words slot numbers of the fixed-slot motion library?

Read-only over an extracted copy of the game (FF12_EXTRACT; default D:/FFXII_TZA_extract), every version-1 *.ca.
Reading under test (FABLE, 2026-09-20): a presentation entry records the child NUMBER of the motion it plays
(entry +0x31C & 0xFFF, moved to 'previous' +0x326 by command 0x00), and the blend-in rule 0x2C matches its word +2
against that previous number. If so, in a version-1 container - whose child table is a fixed array of slots - every
from-word other than 0xFFFF should be a slot index below the table size. Whether the slot is OCCUPIED in the same file
is reported separately: a rule may name a motion that lives in another container of the same character.
"""
import os, struct, collections
ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]; u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
files = rules = below = occupied = 0; worst = 0; per = 0
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data", "obj_finish")):
    for f in fn:
        if not f.endswith(".ca"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP" or u32(d, 4) != 1:
            continue
        files += 1
        total = u32(d, 0xC); per = u32(d, 0x30); offs = struct.unpack_from("<%dI" % total, d, 0x40)
        for i, o in enumerate(offs):
            if not o or d[0x40 + o: 0x44 + o] != b"@FMC":
                continue
            b = 0x40 + o; h = b + 0x30
            for t in range(u32(d, b + 0xC)):
                ng, dist = d[h + 3], u16(d, h + 4); g = h + 6
                for _ in range(ng):
                    w = u16(d, g + 2); c = g + 4
                    for _ in range(w & 0x3F):
                        w0 = u16(d, c)
                        if w0 & 0x7F == 0x2C:
                            fr = u16(d, c + 2)
                            if fr != 0xFFFF:
                                rules += 1
                                if fr < total:
                                    below += 1
                                    occupied += bool(offs[fr])
                                worst = max(worst, fr)
                        if not (w0 >> 7):
                            break
                        c += w0 >> 7
                    g += (w >> 6) or 4
                if not dist:
                    break
                h += dist
print("version-1 containers:", files)
print("0x2C rules with a from-word other than 0xFFFF:", rules)
print("  from-word below the container's slot count:", below, "; largest from-word seen:", worst)
print("  ... and that slot is occupied in the same file:", occupied)
