"""regionA_word_stores.py - in every function that addresses the inventory registry 01EEBCC0-01EEC1E8
(rip-relative, from registry_ripscan.txt), list every 16-bit (word) memory store and every rep/stos.
A packed-count word (low10 total, high6 reserved) can only change through a word store (or a wider
store/memset/memcpy over it). Positive control: 002FD150's two known packed-word stores 002FD298 and
002FD31A must be listed.
Run from pub140-scratch: python ../ovprobes/regionA_word_stores.py"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, "..", "pub140-scratch"))
sys.argv = ['disw', '0031EB20']
exec(open('disw.py').read().split("fn = int")[0])
fns = set()
for line in open(os.path.join(HERE, "registry_ripscan.txt")):
    p = line.split()
    if len(p) > 3:
        site = int(p[1], 16)
        f = max(s for s in funcs if s <= site)
        fns.add(f)
found = set()
for f in sorted(fns):
    code = d[off(f):off(f) + funcs[f]]
    out = []
    for ins in md.disasm(code, f):
        s = ins.op_str
        if ins.mnemonic.startswith("mov") and s.startswith("word ptr [") and "rsp" not in s.split(",")[0]:
            out.append(f"{ins.address:08X} {ins.mnemonic} {s}"); found.add(ins.address)
        elif ins.mnemonic in ("inc", "dec", "add", "sub", "or", "and", "xor") and s.startswith("word ptr [") and "rsp" not in s:
            out.append(f"{ins.address:08X} {ins.mnemonic} {s}"); found.add(ins.address)
        elif ins.mnemonic.startswith("rep") or ins.mnemonic.startswith("stos"):
            out.append(f"{ins.address:08X} {ins.mnemonic} {s}")
        elif ins.mnemonic == "call" and s in ("0x861ec0", "0x861ab0"):
            out.append(f"{ins.address:08X} call {s} (memset/memcpy family)")
    print(f"== {f:08X} {names.get(f,'')} ({len(out)} word-store/bulk lines)")
    for o in out:
        print("   ", o)
print("CONTROL 002FD298 and 002FD31A listed:", 0x2FD298 in found and 0x2FD31A in found)
