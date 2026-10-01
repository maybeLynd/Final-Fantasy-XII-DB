"""SWE2-AUDIT-SPEC: prologue of 001EA3C0 (rcx -> rsi untouched?) and the receiver the other two raw callers pass."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def show(e, lo, hi):
    for x in tk.fdis(e):
        if lo <= x.address < hi: print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
print("[001EA3C0 prologue]"); show(0x1EA3C0, 0x1EA3C0, 0x1EA3E0)
for e, site in ((0x1C1D40, 0x1C1E04), (0x1C2980, 0x1C2BFD)):
    print("[%s, call at %08X]" % (tk.fname(e), site)); show(e, site - 0x24, site + 5)
