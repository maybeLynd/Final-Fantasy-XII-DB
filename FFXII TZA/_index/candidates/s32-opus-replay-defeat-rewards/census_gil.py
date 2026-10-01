"""Static census (block 344): over every shipped `in` area file, how many foe definitions have both gil terms zero -
base row (by def +0x22) +0x30 and per-level row (by def +0x24) +0x30, the fields 00312280 reads at 0031253B / 00312546
through unit +0xE78 / +0xE70. Reads the files only; no execution. Prints the counts and writes census_gil.txt."""
import glob
import os
import struct

ROOT = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map"
HERE = os.path.dirname(os.path.abspath(__file__))
total = zero = files = 0
for p in sorted(glob.glob(os.path.join(ROOT, "*", "area", "*.ard"))):
    b = open(p, "rb").read()
    if len(b) < 0x30:
        continue
    s = struct.unpack_from("<8I", b, 0x10)

    def tab(off):
        if not off or b[off:off + 4] != b"st2e":
            return None
        n, st, ro = struct.unpack_from("<III", b, off + 4)
        return off + ro, n, st
    D, B, L = tab(s[2]), tab(s[5]), tab(s[6])          # categories 2 / 3 / 4 -> 02EBF120 / 02EBF148 / 02EBF140
    if not (D and B and L):
        continue
    files += 1
    for i in range(D[1]):
        d = D[0] + i * D[2]
        bi, li = struct.unpack_from("<HH", b, d + 0x22)
        if bi >= B[1] or li >= L[1]:
            continue
        total += 1
        flat = struct.unpack_from("<i", b, B[0] + bi * B[2] + 0x30)[0]
        mult = struct.unpack_from("<i", b, L[0] + li * L[2] + 0x30)[0]
        zero += flat == 0 and mult == 0
line = "area files with all three tables: %d; definitions: %d; both gil terms zero: %d" % (files, total, zero)
print(line)
open(os.path.join(HERE, "census_gil.txt"), "w", newline="\n").write(line + "\n")
