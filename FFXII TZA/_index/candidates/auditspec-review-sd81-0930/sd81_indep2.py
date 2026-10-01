"""sd81_indep2.py - SWE2-AUDIT-SPEC: K1 argument flow at 001FDC10 and node-size immediates in two insert-unique bodies."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
print("001FDC10 .. the 001FC420 call:")
for x in tk.dis(0x1FDC10, 0x1FDC32):
    print("   %08X  %s %s" % (x.address, x.mnemonic, x.op_str))
for fn, want in ((0x199DB0, "0x28"), (0x1FCB40, "0x60")):
    hits = ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in tk.fdis(fn)
            if x.op_str.endswith(", " + want) or "call" == x.mnemonic]
    print("%08X immediates %s and calls:" % (fn, want))
    for h in hits: print("   " + h)
