"""manifest_walk.py - SWE2-AUDIT-SPEC: full linear listing of the manifest loops (review of 17a146c83, RC-29).
001D0390 around 001D150F, 001D5260 around 001D537D, and 001CD0E0 around its image-base read 001CD186."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
for e, lo, hi in ((0x001D0390, 0x001D14F0, 0x001D1570), (0x001D5260, 0x001D5360, 0x001D53D0), (0x001CD0E0, 0x001CD0E0, 0x001CD1C0)):
    print("--- %08X [%08X,%08X) %s" % (e, lo, hi, tk.fname(e)))
    for x in tk.fdis(e):
        if lo <= x.address < hi:
            print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
