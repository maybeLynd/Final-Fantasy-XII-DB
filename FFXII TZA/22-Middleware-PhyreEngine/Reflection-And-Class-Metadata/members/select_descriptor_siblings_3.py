"""select_descriptor_siblings_3.py - EC-7 family C member selectors, third
frontier form-cluster batch (SWE2-EC7-FRONTIER-FORM-CLUSTERS-3), declared on
class-descriptor-and-metadata-system.md.

One sibling spelling of the declared static-descriptor lazy-initialiser row:

  staticdescriptorsingletonlazyinit2 (132B) - TLS-indexed init counter via
      gs:[0x58]; bound-check then call 008092FC once-init; fetch the member
      singleton via a member getter, tag it |1 into the member rip cell,
      call shared 006301F0 for the descriptor, store it, register the
      teardown via shared 0080929C, and return the member rip descriptor
      address. Sibling of StaticDescriptorSingletonLazyInit (which calls
      shared 0062FF50 instead of 006301F0).

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_descriptor_siblings_3.py [--write]
"""
import io, os, struct, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

FAMILIES = [
    ("nativeadapter-staticdescriptorsingletonlazyinit2.tsv", 132,
     "sub rsp,I; mov M[rsp],I; mov ecx,M[rip]; mov rax,M[]; mov edx,I; "
     "mov rcx,M[rax+rcx]; mov eax,M[rdx+rcx]; cmp M[rip],eax; jle T; "
     "lea rcx,M[rip]; call T; cmp M[rip],I; jne T; call T; or rax,I; "
     "mov M[rip],rax; call T; mov M[rip],rax; mov M[rip],I; lea rcx,M[rip]; "
     "call T; lea rax,M[rip]; add rsp,I; ret",
     lambda m, c, j, x: {0x008092FC, 0x0080929C, 0x006301F0} <= set(c)
                        and len(c) == 4 and not j and not x,
     "NativeAdapter.StaticDescriptorSingletonLazyInit2 - EC-7 family C\n"
     "# TLS-indexed init counter via gs:[0x58]; bound-check then call\n"
     "# 008092FC once-init; fetch the member singleton via a member getter,\n"
     "# tag it |1, call shared 006301F0 for the descriptor, register the\n"
     "# teardown via shared 0080929C, return the member rip descriptor\n"
     "# address. Sibling of StaticDescriptorSingletonLazyInit."),
    ("nativeadapter-singletonallocdescriptorinstall.tsv", 58,
     "sub rsp,I; mov ecx,I; call T; mov rcx,M[rip]; mov edx,I; call T; "
     "test rax,rax; je T; lea rcx,M[rip]; mov M[rax],rcx; mov M[rip],rax; "
     "add rsp,I; ret",
     lambda m, c, j, x: c == {0x0016D6A0, 0x001A1470} and not j and not x,
     "NativeAdapter.SingletonAllocDescriptorInstall - EC-7 family C\n"
     "# call the ICF-folded ret-0 stub 0016D6A0 (ecx=1); allocate an 8-byte\n"
     "# record via shared 001A1470 on a member global container; install a\n"
     "# member rip descriptor pointer at [rax] and store rax into a member\n"
     "# global."),
]

def load_sections(d):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    o = pe + 24 + struct.unpack_from("<H", d, pe + 20)[0]
    secs = []
    for _ in range(n):
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, max(vsz, rsz), rptr)); o += 40
    return secs

def form_and_targets(md, d, secs, a, size):
    r = a - BASE
    off = next((rp + (r - sva) for sva, sl, rp in secs if sva <= r < sva + sl), None)
    toks, calls, jmps, jccs, imms, memw = [], set(), set(), set(), [], []
    for ins in md.disasm(d[off:off + size], a):
        ops = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                ops.append(md.reg_name(op.reg))
            elif op.type == X86_OP_IMM:
                if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
                    ops.append("T")
                    if not (a <= op.imm < a + size):
                        if ins.mnemonic == "call": calls.add(op.imm)
                        elif ins.mnemonic == "jmp": jmps.add(op.imm)
                        else: jccs.add(op.imm)
                else:
                    ops.append("I")
                    imms.append(op.imm)
            elif op.type == X86_OP_MEM:
                memw.append(op.size)
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), calls, jmps, jccs, {"imms": imms, "memw": memw, "size": size}

def prior_members(tsv):
    p = os.path.join(ROOT, tsv)
    out = set()
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8", errors="replace"):
            t = l.split("#")[0].split("\t")[0].strip()
            try: out.add(int(t.split()[0], 16))
            except (ValueError, IndexError): pass
    return out

def main():
    write = "--write" in sys.argv
    sizes = CD.load_functions(None)
    res = CD.evaluate(CD.DEFAULT_DB, sizes)
    frontier = res["frontier_set"]
    a_set = res["explained_set"] - res["claimed_set"]
    d = open(EXE, "rb").read()
    secs = load_sections(d)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    priors = {tsv: prior_members(tsv) for tsv, _, _, _, _ in FAMILIES}
    pool = set(frontier)
    for tsv in priors:
        pool |= (priors[tsv] - a_set)
    cache = {a: form_and_targets(md, d, secs, a, sizes[a]) for a in pool if a in sizes}
    ok = True
    results = {}
    for tsv, sz, skel, tcheck, header in FAMILIES:
        members = sorted(a for a, (f, c, j, x, m) in cache.items()
                         if (sz is None or sizes[a] == sz) and f == norm(skel)
                         and tcheck(m, c, j, x))
        if not members:
            print("REFUSE %s: skeleton matched nobody" % tsv); ok = False; continue
        bad = [a for a in members if a in a_set]
        if bad:
            print("REFUSE %s: %d member(s) measure A" % (tsv, len(bad))); ok = False; continue
        results[tsv] = (members, header)
        tg = collections.Counter(t for a in members for t in cache[a][1] | cache[a][2] | cache[a][3])
        print("%-46s %3d members | targets %s" %
              (tsv, len(members), ", ".join("%08X x%d" % kv for kv in tg.most_common(6))))
    if not ok or not write:
        print("dry run" if ok else "refused"); return
    for tsv, (members, header) in results.items():
        with io.open(os.path.join(ROOT, tsv), "w", encoding="utf-8", newline="\n") as f:
            f.write("# " + header.replace("\n", "\n# ") + "\n")
            f.write("address\ttargets\n")
            for a in members:
                tg = sorted(cache[a][1] | cache[a][2] | cache[a][3])
                f.write("%08X\t%s\n" % (a, ",".join("%08X" % t for t in tg)))
        print("wrote", tsv, len(members))

if __name__ == "__main__":
    main()
