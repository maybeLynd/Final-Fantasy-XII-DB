"""log_channels.py - the channel argument (ecx) at every call or tail jump to the formatted log call 005CDAA0, and the
format string (rdx) where it is a rip-relative literal. SWE2-CONTRACT, 2026-09-30. Static. Reads only.

Callers are the functions with an edge to 005CDAA0 in Tools/work/graph/edges.tsv (calls and tail jumps). For each site
the nearest preceding write to ecx/rcx within the same body is read: an immediate, or `xor ecx,ecx`, else the
instruction is printed as UNRESOLVED. Positive control: the page's §9 count of 136 non-EH callers must be reproduced by
the edge list (distinct caller functions), and every site found must be a direct call/jmp to 005CDAA0.
"""
import collections, io, os, sys
import capstone
import block_writer_disjoint as b

TARGET = 0x005CDAA0


def last_write(prev, reg32, reg64):
    for p in reversed(prev):
        o = p.op_str.replace(" ", "")
        if o.startswith(reg32 + ",") or o.startswith(reg64 + ","):
            if p.mnemonic == "mov" and (o.split(",", 1)[1].startswith("0x") or o.split(",", 1)[1].isdigit()):
                v = o.split(",", 1)[1]
                return int(v, 16) if v.startswith("0x") else int(v)
            if p.mnemonic == "xor" and o in (reg32 + "," + reg32, reg64 + "," + reg64):
                return 0
            return p
        if p.mnemonic == "call":
            return None
    return None


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    rows = io.open(os.path.join(b.DB, "..", "Tools", "work", "graph", "edges.tsv"), encoding="utf-8").read().splitlines()[1:]
    callers = sorted(set(int(l.split("\t")[0], 16) for l in rows if l.split("\t")[1] == "005CDAA0"))
    chan = collections.Counter()
    unresolved, sites = [], 0
    fmts = collections.defaultdict(list)
    for f in callers:
        ins = list(md.disasm(at(f, ext[f]), f))
        for k, i in enumerate(ins):
            if i.mnemonic in ("call", "jmp") and i.op_str == hex(TARGET):
                sites += 1
                v = last_write(ins[max(0, k - 30):k], "ecx", "rcx")
                fmt = None
                for p in reversed(ins[max(0, k - 30):k]):
                    if p.mnemonic == "lea" and p.op_str.startswith("rdx, [rip"):
                        t = p.address + p.size + p.operands[1].mem.disp
                        d = at(t, 96)
                        fmt = d.split(b"\0")[0].decode("latin-1") if d else None
                        break
                    if p.mnemonic == "call":
                        break
                if isinstance(v, int):
                    chan[v] += 1
                    if fmt and len(fmts[v]) < 3:
                        fmts[v].append(fmt[:70])
                else:
                    unresolved.append((f, i.address, v.mnemonic + " " + v.op_str if v is not None else "none before a call"))
    ok = len(callers) == 136
    print("%s  control: distinct caller functions in the edge list = %d (page: 136)" % ("PASS" if ok else "FAIL", len(callers)))
    print("call/jmp sites: %d; channel resolved: %d; unresolved: %d" % (sites, sum(chan.values()), len(unresolved)))
    for c, n in sorted(chan.items()):
        print("  channel %d: %d site(s); e.g. %s" % (c, n, fmts.get(c, [])))
    for u in unresolved:
        print("  UNRESOLVED %08X %08X %s" % u)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
