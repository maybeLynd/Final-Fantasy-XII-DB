"""select_refflag_alignedfree_siblings.py - EC-7 family C member selectors,
second frontier form-cluster pass (SWE2-EC7-FRONTIER-FORM-CLUSTERS-2), declared
on object-construction-destruction-and-static-lifetime.md.

Sibling spellings of the declared ref-flag handle rows on this page. Those
call a member release target; these call the shared aligned-free wrapper
00584730 on the stored pointer when the flag bit is clear, then zero the
{size, ptr} fields and return 1:

  refflag-invertedbit-alignedfree-returntrue (43B) - dword flag: load
      [rdx+0x30], not+test a member bit; if the record flag is set, free
      [rdx+0x18] via 00584730; zero {+0x18,+0x30}; return 1.
  refflag-dwordflag-alignedfree-reset-returntrue (61B) - same operation with
      the flag read from [rdx] (shr eax,0x12): inverted bit selects the free;
      also clears [rbx+8]; return 1.

Each group is one operand-aware byte image with c=={00584730}.
Pool = frontier | (prior members - A-measured); A beats a declaration.
Usage: python select_refflag_alignedfree_siblings.py [--write]
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
ALIGNED_FREE = 0x00584730

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

FAMILIES = [
    ("refflag-invertedbit-alignedfree-returntrue.tsv", 43,
     "sub rsp,I; mov M[rsp],I; mov rcx,M[rdx]; test rcx,rcx; je T; "
     "mov eax,ecx; not al; test al,I; je T; call T; nop; mov al,I; "
     "add rsp,I; ret",
     lambda m, c, j, x: c == {ALIGNED_FREE} and not j and not x,
     "RefFlag.InvertedBitAlignedFreeReturnTrue - EC-7 family C\n"
     "# dword flag bit inverted-test on [rdx+0x30]; if the record flag is set,\n"
     "# free [rdx+0x18] via shared aligned-free wrapper 00584730; zero the\n"
     "# {+0x18,+0x30} fields; return 1."),
    ("refflag-dwordflag-alignedfree-reset-returntrue.tsv", 61,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; mov eax,M[rdx]; "
     "shr eax,I; not al; test al,I; je T; mov rcx,M[rdx]; test rcx,rcx; "
     "je T; call T; xor eax,eax; mov M[rbx],rax; mov M[rbx],eax; mov al,I; "
     "add rsp,I; pop rbx; ret",
     lambda m, c, j, x: c == {ALIGNED_FREE} and not j and not x,
     "RefFlag.DwordFlagAlignedFreeResetReturnTrue - EC-7 family C\n"
     "# flag read from [rdx] (shr eax,0x12, inverted bit); if set, free\n"
     "# [rdx+8] via shared aligned-free wrapper 00584730; zero {+8,+0} and\n"
     "# the flag dword; return 1."),
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
