"""refs.py - every instruction whose rip-relative operand (lea/mov) resolves to ADDR, with its function. ORACLE 2026-09-30."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K
from capstone import x86 as X
R = K.R
T = set(int(a, 16) for a in sys.argv[1:])
for f in sorted(K.ext):
    for i in R.md.disasm(R.at(f, K.ext[f]), f):
        for op in i.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP and i.address + i.size + op.mem.disp in T:
                print("%08X in %08X: %s %s -> %08X" % (i.address, f, i.mnemonic, i.op_str, i.address + i.size + op.mem.disp))
