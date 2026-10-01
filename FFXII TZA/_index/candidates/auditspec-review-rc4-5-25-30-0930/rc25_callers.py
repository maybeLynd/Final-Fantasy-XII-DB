"""SWE2-AUDIT-SPEC: RC-25 L1/L2 - raw callers of the definition-record initialiser 0023AC80 and of 002EF4A0 (the
narrowing's save-restore overwrite), and the +0x04 store 0023AD8E. 2026-09-30."""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
R = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
for e in (0x23AC80, 0x2EF4A0):
    cs = R.get("%X" % e, [])
    print("raw callers of %08X: %d -> %s" % (e, len(cs), " ".join("%s(in %s)" % (c, tk.fname(int(c, 16))[:40]) for c in cs)))
for x in tk.dis(0x23AD84, 0x23AD94): print("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
