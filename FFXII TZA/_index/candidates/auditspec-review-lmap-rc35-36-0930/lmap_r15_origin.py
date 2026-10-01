"""SWE2-AUDIT-SPEC: where 003C2320's r15 comes from, and the 003BDDE0 return-value reads (2026-09-30)."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def pr(lo, hi):
    for x in tk.dis(lo, hi):
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("003C2320 prologue (r15 origin):"); pr(0x3C2320, 0x3C2360)
print("003C2320 around the r15 reads and the two 003BDDE0 calls:"); pr(0x3C23E0, 0x3C2400); pr(0x3C2525, 0x3C25CC)
print("003BE3A0 before the call at 003BE554:"); pr(0x3BE500, 0x3BE55A)
