"""SWE2-AUDIT-SPEC independent checks of ov58d-pointer-flow-0930 (OPUS, a67cad059), 2026-09-30. Image only.
I1 (C6) 002EF4A0: the two lea's (source 02166480, destination 021B290C) and the copy size.
I2 (C7) 00253970: the store of image + 0x8200 into 020927C0.
I3 (C8) 00320AB0: the record formula and the bound on k (cmp al, 0x27 and the branch that follows);
        the end of the record array as arithmetic, compared with region A's start +0x4748.
I4 00234ED0: the r9 loop (start, step, end) and its store displacements.
I5 raw callers of 002EF4A0 and 00320AB0 (raw call index).
"""
import sys, json, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def ript(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and x.reg_name(op.mem.base) == "rip":
            return x.address + x.size + op.mem.disp
    return None
def listing(e, pred, cap=40):
    n = 0
    for x in tk.fdis(e):
        if pred(x):
            t = ript(x)
            print("  %08X %s %s%s" % (x.address, x.mnemonic, x.op_str, ("  -> %08X" % t) if t else ""))
            n += 1
            if n >= cap: break
print("I1 002EF4A0 (size %s): rip operands, immediates, loop control" % tk.fsize(0x2EF4A0))
listing(0x2EF4A0, lambda x: ript(x) is not None or x.mnemonic in ("mov", "cmp", "sub", "dec", "add") and re.search(r"0x[0-9a-f]{3,}", x.op_str) or x.mnemonic.startswith("j") or x.mnemonic.startswith("rep"))
print("I2 00253970: stores to rip targets and the value's formation")
listing(0x253970, lambda x: ript(x) is not None or "0x8200" in x.op_str)
print("I3 00320AB0 full body:")
for x in tk.fdis(0x320AB0): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("I3 arithmetic: records = 8 + 0x1C8*k, k in 0..39 -> last record 0x%X..0x%X (end exclusive); region A starts 0x4748"
      % (8 + 0x1C8 * 39, 8 + 0x1C8 * 40))
print("I4 00234ED0: r9 and store operands")
listing(0x234ED0, lambda x: "r9" in x.op_str or (x.mnemonic.startswith("mov") and x.operands and x.operands[0].type == X86_OP_MEM), cap=60)
for e in (0x2EF4A0, 0x320AB0, 0x234ED0):
    cs = RAW.get("%X" % e, [])
    print("I5 raw callers of %08X: %d %s" % (e, len(cs), " ".join(cs[:15])))
