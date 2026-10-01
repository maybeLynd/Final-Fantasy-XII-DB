"""scan_bit13.py - who sets bit 13 (0x2000) of the dword at [0209AC30] + 0x400 (the flags word 00228130 tests before
running the skip loop 00360880)? Lists (1) every function with a rip reference to 0209AC30, and in each, instructions
with disp 0x400 or 0x3F8, and every `or`/`bts` with 0x2000 / 13; (2) image-wide `or dword [r+0x400], imm` with bit 13.
ORACLE 2026-09-30."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K
from capstone import x86 as X
R = K.R
G = 0x0209AC30
refs = set()
wide = []
for f in sorted(K.ext):
    ins = list(R.md.disasm(R.at(f, K.ext[f]), f))
    hit = False
    for i in ins:
        for op in i.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP and i.address + i.size + op.mem.disp == G:
                hit = True
        if i.mnemonic in ("or", "bts") and len(i.operands) == 2 and i.operands[0].type == X.X86_OP_MEM and \
                i.operands[0].mem.disp == 0x400 and i.operands[1].type == X.X86_OP_IMM and \
                ((i.mnemonic == "or" and i.operands[1].imm & 0x2000) or (i.mnemonic == "bts" and i.operands[1].imm == 13)):
            wide.append((f, i))
    if hit:
        refs.add(f)
        for i in ins:
            t = i.op_str
            if ("0x400]" in t or "0x3f8" in t or "0x2000" in t or (i.mnemonic == "bts" and t.endswith(", 0xd"))):
                print("%08X %08X %-6s %s" % (f, i.address, i.mnemonic, t))
print("functions referencing 0209AC30: %d" % len(refs))
print("image-wide or/bts of bit 13 at +0x400:")
for f, i in wide:
    print("  %08X %08X %s %s" % (f, i.address, i.mnemonic, i.op_str))
