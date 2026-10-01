"""SWE2-AUDIT-SEM: raw UTF-16LE scan (no row parser) of every menu03/menu04.bin in the extract, counting code units in
U+00C0..U+00FF at even AND odd alignment; independent of the producer's ex00 row decoder."""
import glob, struct, collections
for p in sorted(glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/*/binaryfile/menu0[34].bin") +
                glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/*/BinaryFile/menu0[34].bin")):
    b = open(p, "rb").read()
    for al in (0, 1):
        c = collections.Counter()
        for i in range(al, len(b) - 1, 2):
            u = b[i] | b[i + 1] << 8
            if 0xC0 <= u <= 0xFF:
                c[chr(u)] += 1
        print("%-70s align %d  latin-1 accented units: %d %s" % (p[-55:], al, sum(c.values()), "".join(sorted(c)) if al == 0 else ""))
