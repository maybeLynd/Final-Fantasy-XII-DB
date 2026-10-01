"""arena_select.py - which arena ids code SELECTS through the push 0036C1D0(arena, category), the only way an allocation
through the wrappers 0036A100 / 0036A1A0 picks an arena (the memory page: the wrappers take no arena argument and pass
the active arena 022D89BC). SWE2-CONTRACT, 2026-09-30, for the boot page's "whether code selects id 10". Static.

Callers: every function with an edge to 0036C1D0 in Tools/work/graph/edges.tsv. At each call/jmp the last write to ecx
is resolved (immediate; xor; lea reg+n with reg known from the last immediate write in the body). Positive controls:
the published count of 135 push sites in 109 functions must be reproduced, and 0025A990's push must resolve to 5 (the
memory page: `0036C1D0(5, 5)`). Unresolved sites are printed, not guessed.
"""
import collections, io, os, sys
import capstone
import block_writer_disjoint as b

TARGET = 0x0036C1D0


def regval(ins, k, reg32):
    """last write to reg32 before index k: an int, or None when not an immediate/xor/known lea."""
    known = {}
    for p in ins[:k]:
        o = p.op_str.replace(" ", "")
        dst = o.split(",", 1)[0]
        if p.mnemonic == "xor" and o.split(",")[0] == o.split(",")[-1]:
            known[dst] = 0
        elif p.mnemonic == "mov" and "," in o and (o.split(",", 1)[1].startswith("0x") or o.split(",", 1)[1].isdigit()):
            v = o.split(",", 1)[1]
            known[dst] = int(v, 16) if v.startswith("0x") else int(v)
        elif p.mnemonic == "mov" and "," in o and o.split(",", 1)[1] in known and "[" not in o:
            known[dst] = known[o.split(",", 1)[1]]
        elif p.mnemonic == "lea" and o.startswith(dst + ",[") and "rip" not in o:
            inner = o.split("[", 1)[1].rstrip("]")
            sign = -1 if "-" in inner else 1
            base, _, disp = inner.replace("-", "+").partition("+")
            b32 = {"r8": "r8d", "r9": "r9d", "rax": "eax", "rbx": "ebx", "rcx": "ecx", "rdx": "edx", "rsi": "esi",
                   "rdi": "edi", "rbp": "ebp", "r10": "r10d", "r11": "r11d", "r12": "r12d", "r13": "r13d",
                   "r14": "r14d", "r15": "r15d"}.get(base, base)
            if b32 in known and disp:
                known[dst] = known[b32] + sign * int(disp, 16 if disp.startswith("0x") else 10)
            else:
                known.pop(dst, None)
        elif p.mnemonic == "call":
            for r in ("eax", "ecx", "edx", "r8d", "r9d", "r10d", "r11d"):
                known.pop(r, None)
        elif dst in ("ecx", "rcx", "eax", "rax", "edx", "rdx", "r8d", "r8", "r9d", "r9", "ebx", "rbx", "esi", "rsi",
                     "edi", "rdi", "ebp", "rbp", "r12d", "r13d", "r14d", "r15d") and p.mnemonic not in ("cmp", "test", "push"):
            known.pop(dst, None)
            known.pop({"rcx": "ecx", "rax": "eax", "rdx": "edx", "r8": "r8d", "r9": "r9d", "rbx": "ebx", "rsi": "esi",
                       "rdi": "edi", "rbp": "ebp"}.get(dst, dst), None)
    return known.get(reg32)


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    rows = io.open(os.path.join(b.DB, "..", "Tools", "work", "graph", "edges.tsv"), encoding="utf-8").read().splitlines()[1:]
    callers = sorted(set(int(l.split("\t")[0], 16) for l in rows if l.split("\t")[1] == "0036C1D0"))
    got, unres, sites = collections.Counter(), [], 0
    per = {}
    for f in callers:
        ins = list(md.disasm(at(f, ext[f]), f))
        for k, i in enumerate(ins):
            if i.mnemonic in ("call", "jmp") and i.op_str == hex(TARGET):
                sites += 1
                v = regval(ins, k, "ecx")
                per.setdefault(f, []).append(v)
                if isinstance(v, int):
                    got[v] += 1
                else:
                    unres.append((f, i.address))
    fails = 0
    c1 = (sites, len(callers)) == (135, 109)
    c2 = per.get(0x0025A990) == [5]
    for ok, name in ((c1, "C1 sites/functions = %d/%d (published 135/109)" % (sites, len(callers))),
                     (c2, "C2 0025A990 selects %s (published 5)" % per.get(0x0025A990))):
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        fails += not ok
    print("resolved: %s" % ", ".join("arena %d x%d" % kv for kv in sorted(got.items())))
    print("id 10 selected at a resolved site: %s" % (10 in got))
    print("unresolved sites: %d" % len(unres))
    for f, a in unres:
        print("  UNRESOLVED %08X %08X" % (f, a))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
