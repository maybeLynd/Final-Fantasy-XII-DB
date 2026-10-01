"""immpair_mem.py K I : stores of immediate K and immediate I to memory within 8 instructions of each other, image-wide
over listed functions (catches request records built in memory, e.g. {kind, id} fields). Also u8/u16/u32 adjacent
(K,I) pairs in .rdata/.data. Prints hit lists and counts."""
import sys, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
K = int(sys.argv[1], 0); I = int(sys.argv[2], 0)
exec(open("peek.py").read())
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
funcs = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
hits = 0
for f, n, sz in funcs:
    o = off(f)
    if o is None: continue
    win = []
    for ins in md.disasm(d[o:o + sz], f):
        ops = ins.operands
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_IMM and ops[1].imm in (K, I):
            win.append((ins.address, ops[1].imm, ins.op_str))
    for i, (a1, v1, s1) in enumerate(win):
        for a2, v2, s2 in win[i + 1:]:
            if a2 - a1 > 48: break
            if {v1, v2} == {K, I} and v1 != v2:
                hits += 1; print(f"  {a1:08X} {s1} | {a2:08X} {s2}   [{f:08X} {n}]")
print("code store-pair hits:", hits)
dh = 0
for (va, vs, ro, rs) in secs[1:3]:
    raw = d[ro:ro + min(vs, rs)]
    for fmt, w in (("<BB", 1), ("<HH", 2), ("<II", 4)):
        for pat in (struct.pack(fmt, K, I), struct.pack(fmt, I, K)):
            p = raw.find(pat); c = 0
            while p >= 0:
                if p % w == 0: c += 1
                p = raw.find(pat, p + 1)
            print(f"  data {va:08X} fmt {fmt} {pat.hex()} aligned hits {c}"); dh += c
print("data pair hits (aligned):", dh)
