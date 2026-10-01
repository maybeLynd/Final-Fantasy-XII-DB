"""manifest_rows.py - SWE2-AUDIT-SPEC: the .rdata block at 008FCE00 read as the stride its three readers use
(row = [obj+0xA88] * 0x16 dwords + column), rows 0..17, non-zero dwords only, plus where each row ends."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
B = 0x008FCE00
for r in range(18):
    a = B + r * 0x16 * 4
    v = [tk.u32(a + 4 * i) for i in range(0x16)]
    print("row %2d @%08X: %s" % (r, a, " ".join("%X" % x for x in v)))
