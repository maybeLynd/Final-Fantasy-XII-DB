"""SWE2-AUDIT-SPEC: the +0xCB8 store at 00707655 that rc4b_bounds B2b does not list, and 0018715A's source register;
also 0047E4E7's function context (a +0xDAC store of r9d). 2026-09-30."""
import sys, bisect
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def pr(lo, hi, mark=()):
    for x in tk.dis(lo, hi):
        print("  %s%08X %s %s" % ("*" if x.address in mark else " ", x.address, x.mnemonic, x.op_str))
a = 0x707655
i = bisect.bisect_right(tk.fstarts, a) - 1
print("00707655: listed owner None; nearest listed function before: %08X size %d; next: %08X" % (tk.flist[i][0], tk.flist[i][1], tk.flist[i + 1][0]))
j = bisect.bisect_right(tk.pstarts, a) - 1
print("nearest .pdata range before: %08X-%08X" % tk.pdata[j])
print("bytes before 00707655 (decode from nearest listed end):")
pr(max(tk.flist[i][0] + tk.flist[i][1], a - 0x30), a + 0x10, {a})
print("0018715A context (r12d source):")
o = tk.owner(0x18715A)[0]
ins = tk.fdis(o)
r12 = [x for x in ins if x.op_str.startswith("r12") and x.mnemonic in ("mov", "xor", "lea", "movzx", "or", "and", "inc", "add", "sub", "pop") and x.address < 0x18715A]
for x in r12[-6:]: print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("0047E4E7 context:")
pr(0x47E4C0, 0x47E4F0, {0x47E4E7})
