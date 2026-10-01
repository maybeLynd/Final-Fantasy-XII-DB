"""registry_fn_stores.py - every non-stack memory store (any width) in the functions that rip-address the
inventory registry 01EEBCC0-01EEC1E8 (registry_ripscan.txt), to test whether any of them writes a registry
count (+0x3C) or other descriptor field through a register base. Control: the rebase 0030B6A0's
`mov dword ptr [r8 + 0x40], r9d` (0030B6F1) must be listed.
Run from pub140-scratch: python ../ovprobes/registry_fn_stores.py"""
import os, sys
from capstone.x86 import X86_OP_MEM
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, "..", "pub140-scratch"))
sys.argv = ['disw', '0031EB20']
exec(open('disw.py').read().split("fn = int")[0])
md.detail = True
fns = set()
for line in open(os.path.join(HERE, "registry_ripscan.txt")):
    p = line.split()
    if len(p) > 3:
        site = int(p[1], 16)
        fns.add(max(s for s in funcs if s <= site))
seen = set()
STORE_MN = ("mov", "add", "sub", "or", "and", "xor", "inc", "dec", "movups", "movdqu", "movsd", "movss", "movaps", "movq", "movd", "stos")
for f in sorted(fns):
    code = d[off(f):off(f) + funcs[f]]
    out = []
    for ins in md.disasm(code, f):
        if not ins.mnemonic.startswith(STORE_MN) or not ins.operands:
            continue
        o0 = ins.operands[0]
        if o0.type == X86_OP_MEM and ins.reg_name(o0.mem.base) not in ("rsp",):
            out.append(f"{ins.address:08X} {ins.mnemonic} {ins.op_str}"); seen.add(ins.address)
    print(f"== {f:08X} {names.get(f,'')} ({len(out)} stores)")
    for o in out:
        print("   ", o)
print("CONTROL 0030B6F1 listed:", 0x30B6F1 in seen)
