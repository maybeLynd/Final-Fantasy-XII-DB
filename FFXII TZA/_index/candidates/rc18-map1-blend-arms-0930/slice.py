"""slice.py - for each unknown-offset site of rc18_map1_writers.out, the instructions of its function up to the site
that define or scale the store's base/index registers (a linear backward slice, 60 instructions)."""
import re, sys, collections, img
from capstone import x86 as X
sites = collections.defaultdict(set); cur = None
for l in open("rc18_map1_writers.out"):
    if l.startswith("FUNCTION"): cur = int(l.split()[1], 16); continue
    m = re.match(r"  ([0-9A-F]{8}) (.*?)\s+base (\S+)\s+value", l)
    if m and cur and not all(re.match(r"A\+0x", p) for p in m.group(3).split(",")):
        sites[cur].add(int(m.group(1), 16))
fam = lambda n: {"e":n}  # placeholder
def regs_of(x):
    rs = set()
    for o in x.operands:
        if o.type == X.X86_OP_MEM:
            for r in (o.mem.base, o.mem.index):
                if r: rs.add(img.md.reg_name(r))
        if x.mnemonic == "call" and o.type == X.X86_OP_IMM: pass
    return rs
def norm(r):
    t = {"eax":"rax","ebx":"rbx","ecx":"rcx","edx":"rdx","esi":"rsi","edi":"rdi","ebp":"rbp"}
    r = t.get(r, r)
    return re.sub(r"(r\d+)[dwb]$", r"\1", r)
for f in sorted(sites):
    ins = img.fn_ins(f)
    idx = {x.address: k for k, x in enumerate(ins)}
    print("=== %08X" % f)
    for s in sorted(sites[f]):
        k = idx.get(s)
        if k is None: continue
        want = set(norm(r) for r in regs_of(ins[k]))
        out = []
        for x in reversed(ins[max(0, k - 60):k]):
            try:
                _, w = x.regs_access()
            except Exception:
                w = []
            wn = set(norm(img.md.reg_name(r)) for r in w)
            if want & wn and x.mnemonic not in ("cmp", "test"):
                out.append(x)
                r_, _ = x.regs_access()[0], None
                want |= set(norm(img.md.reg_name(r)) for r in x.regs_access()[0])
            if len(out) > 8: break
        t = ripmem = img.ripmem
        print("  %08X %s %s   <= %s" % (s, ins[k].mnemonic, ins[k].op_str,
              " | ".join("%08X %s %s%s" % (x.address, x.mnemonic, x.op_str, (" [%08X]" % ripmem(x)) if ripmem(x) else "") for x in out)))
