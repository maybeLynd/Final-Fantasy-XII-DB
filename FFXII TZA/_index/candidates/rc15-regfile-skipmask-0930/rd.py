"""dis.py - print a function (catalogue extent) or a byte range, and the raw E8/E9 callers of an address. ORACLE 2026-09-30.
usage: python dis.py FN [FN...]      disassemble each function's extent
       python dis.py callers ADDR    raw rel32 call/jmp sites to ADDR, with owning function"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K
R = K.R
def fn_of(a):
    best = None
    for f in K.ext:
        if f <= a < f + K.ext[f] and (best is None or f > best):
            best = f
    return best
if sys.argv[1] == "callers":
    t = int(sys.argv[2], 16)
    import struct
    sec = [s for s in R.b.__dict__.get("SECS", [])] if hasattr(R.b, "SECS") else None
    for f in sorted(K.ext):
        for i in R.md.disasm(R.at(f, K.ext[f]), f):
            if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x") and int(i.op_str, 16) == t:
                print("%08X %s in %08X" % (i.address, i.mnemonic, f))
else:
    for a in sys.argv[1:]:
        f = int(a, 16)
        n = K.ext.get(f)
        if n is None:
            n = 0x80
        print("== %08X size %#x" % (f, n))
        for i in R.md.disasm(R.at(f, n), f):
            print("  %08X %-8s %s" % (i.address, i.mnemonic, i.op_str))
