"""slot_writers.py - SWE2-AUDIT-SPEC (2026-09-30): is anything other than the three setters a writer of ActorManagerSlot
+0x0A0 / +0x0A8 / +0x100 (slot array 02098E10, stride 0x288, 5 slots)? The package's P4 checks only the setters' callers.

Population: every function that forms a base into the array - a rip-relative or image-base-relative reference into
02098E10..+5*0x288, or a load of the current-slot pointer 02099D70 (published by 0026C8C0). In each such function
(extent: the listed function containing the reference, from functions.tsv) every instruction with a memory WRITE is
listed when its displacement makes it overlap +0xA0..+0xA7, +0xA8..+0xAF or +0x100..+0x107 relative to a slot base
(disp taken mod nothing: the fields are reached as [base + disp] or [base + index + disp]), plus every call to the
memset thunk 00861EC0 and every rep stos. Write detection is by mnemonic + first-operand-is-memory (capstone's access
flags mark movups/movq destinations as reads, a known pitfall), so vector stores are included.
Positive control: the three setters themselves must be found (their store is [rcx+rax] with the field folded into the
lea'd base, so they are matched on the rip target instead).
"""
import os, sys, bisect, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

LO, HI, CUR = 0x02098E10, 0x02098E10 + 5 * 0x288, 0x02099D70
FIELDS = [(0xA0, 8), (0xA8, 8), (0x100, 8)]
F = []
for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8").read().splitlines()[1:]:
    p = l.split("\t"); F.append((int(p[0], 16), int(p[2])))
F.sort(); ST = [f[0] for f in F]
def owner(a):
    i = bisect.bisect_right(ST, a) - 1
    return F[i] if i >= 0 and F[i][0] <= a < F[i][0] + F[i][1] else None

refs = [x[0] for x in T.rip_refs(LO, HI)] + [x[0] for x in T.imagebase_refs(LO, HI)] + [x[0] for x in T.rip_refs(CUR, CUR + 8)]
funcs = sorted(set(o for o in (owner(a) for a in refs) if o))
print("base-forming references: %d in %d listed functions (unlisted: %d)" % (len(refs), len(funcs), sum(1 for a in refs if not owner(a))))
WRITE_MN = ("mov", "movups", "movaps", "movdqu", "movdqa", "movq", "movd", "movsd", "movss", "and", "or", "xor", "add", "sub",
            "inc", "dec", "stosq", "stosd", "movlps", "movhps", "vmovups", "vmovdqu", "vmovaps", "cmpxchg", "xchg", "btr", "bts", "not", "neg", "shl", "shr", "sar")
hits = []
for (fs, fl) in funcs:
    for i in T.dis(fs, fs + fl):
        if i.mnemonic == "call" and i.op_str == "0x861ec0":
            hits.append((fs, i.address, "memset call", i.op_str))
        if i.mnemonic.startswith("rep"):
            hits.append((fs, i.address, i.mnemonic, i.op_str))
        if i.mnemonic not in WRITE_MN or not i.operands or i.operands[0].type != X86_OP_MEM:
            continue
        m = i.operands[0].mem; sz = i.operands[0].size
        if m.base == X86_REG_RIP:
            t = i.address + i.size + m.disp
            if LO <= t < HI and any(f <= (t - LO) % 0x288 < f + n or (t - LO) % 0x288 <= f < (t - LO) % 0x288 + sz for f, n in FIELDS):
                hits.append((fs, i.address, i.mnemonic, i.op_str))
            continue
        d = m.disp
        if any(d < f + n and f < d + sz for f, n in FIELDS):
            hits.append((fs, i.address, i.mnemonic, i.op_str))
print("candidate writes (disp overlapping +0xA0/+0xA8/+0x100, memset, rep) in those functions: %d" % len(hits))
for fs, a, m, o in hits:
    print("  fn %08X  %08X  %s %s" % (fs, a, m, o))
