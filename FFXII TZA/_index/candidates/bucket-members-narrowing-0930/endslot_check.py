"""AUDIT-SEM narrowing N2 (DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929): the count-and-offsets frames of the two st2e name
tables and logicpack.bin carry count + 1 offsets - offsets[0] = 8 + 4*count and offsets[count] = the file size.
(SWE2-DATA 2026-09-30), shipped data only.
E1 for every shipped copy: offsets[0] == 8 + 4*count and offsets[count] == len(file), offsets ascending.
Controls: C1 the frame without the end slot (count offsets) would start its data at 4 + 4*count, which is NOT
offsets[0] in any copy; C2 a copy truncated by one byte fails E1 (the check sees the end slot).
"""
import glob, os, struct

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def frame_ok(b):
    n = struct.unpack_from("<I", b, 0)[0]
    if 4 + 4 * (n + 1) > len(b):
        return False, n, None
    offs = struct.unpack_from("<%dI" % (n + 1), b, 4)
    ok = offs[0] == 8 + 4 * n and offs[n] == len(b) and all(offs[i] <= offs[i + 1] for i in range(n))
    return ok, n, offs


EX = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
files = sorted(glob.glob(EX + "/*/binaryfile/basic_skill_basic_skill_name.bin") +
               glob.glob(EX + "/*/binaryfile/growth_rate_growth_rate_name.bin") +
               glob.glob(EX + "/*/binaryfile/logicpack.bin"))
check("E0 six shipped copies found (two locales x three files)", len(files) == 6, str(len(files)))
c1 = True
for f in files:
    b = open(f, "rb").read()
    ok, n, offs = frame_ok(b)
    name = "/".join(os.path.normpath(f).split(os.sep)[-3:])
    print("   %-52s count %5d size %9d offsets[0] %d offsets[count] %s" % (name, n, len(b), offs[0], offs[n]))
    check("E1 %s: offsets[0] = 8 + 4*count and offsets[count] = file size" % name, ok)
    c1 &= offs[0] != 4 + 4 * n
    ok2, *_ = frame_ok(b[:-1])
    check("C2 %s truncated by one byte fails the frame" % name, not ok2)
check("C1 no copy starts its data at 4 + 4*count (the end slot is real)", c1)
print("FAILS %d" % FAILS)
