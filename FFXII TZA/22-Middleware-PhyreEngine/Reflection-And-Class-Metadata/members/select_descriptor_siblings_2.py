"""select_descriptor_siblings_2.py - EC-7 family C member selectors, second
frontier form-cluster pass (SWE2-EC7-FRONTIER-FORM-CLUSTERS-2), declared on
class-descriptor-and-metadata-system.md.

Three new Phyre-side sibling groups measured off the live frontier:

  object-lifecycle-lookup-adapters (69B) - if rdx non-null, call shared
      Phyre.Reflection.ObjectLifecycleDispatch 0063BC00 on a member rip
      record; on a non-null result store this in the stack slot and call a
      member op on (this, result); return 1.
  shared-runtime-identity-dispatch-adapters (118B) - call shared
      Phyre.Reflection.SharedRuntime 00639850 through a global vtable slot;
      compare the result identity/field against this+off and arg3; call a
      member op on the matching branch.
  static-descriptor-singleton-lazyinit-adapters (150B) - bounds-check a
      global index table, call shared CRT init 008092FC, then shared
      Phyre.Reflection.StaticDescriptorSingleton 0062FF50; or-flag a global
      tag twice via member ops, call shared 0080929C; install a member rip
      pointer. The magic-static spelling of the descriptor singleton.

Each group is one operand-aware byte image.
Pool = frontier | (prior members - A-measured); A beats a declaration.
Usage: python select_descriptor_siblings_2.py [--write]
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

LIFECYCLE = 0x0063BC00
SHARED_RUNTIME = 0x00639850
SINGLETON = 0x0062FF50
CRT_INIT = 0x008092FC
CRT_TERM = 0x0080929C

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

FAMILIES = [
    ("object-lifecycle-lookup-adapters.tsv", 69,
     "mov M[rsp],rdx; push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; "
     "lea rcx,M[rip]; call T; test rax,rax; je T; mov M[rsp],rbx; "
     "test rbx,rbx; je T; mov rdx,rax; mov rcx,rbx; call T; nop; mov al,I; "
     "add rsp,I; pop rbx; ret",
     lambda m, c, j, x: LIFECYCLE in c and len(c) == 2 and not j and not x,
     "Phyre.ObjectLifecycleLookupAdapters - EC-7 family C\n"
     "# if rdx non-null, call shared ObjectLifecycleDispatch 0063BC00 on a\n"
     "# member rip record; on a non-null result call a member op on\n"
     "# (this, result); return 1."),
    ("shared-runtime-identity-dispatch-adapters.tsv", 118,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov rax,M[rip]; lea rdi,M[rcx]; mov rbp,rcx; mov ebx,r8d; "
     "lea rcx,M[rip]; mov rsi,rdx; call M[rax]; cmp rsi,rdi; jne T; "
     "cmp ebx,I; jne T; test rax,rax; je T; mov r8d,ebx; mov rdx,rdi; "
     "mov rcx,rax; call T; jmp T; mov r8d,ebx; mov rdx,rsi; mov rcx,rbp; "
     "call T; mov rbx,M[rsp]; xor eax,eax; mov rbp,M[rsp]; mov rsi,M[rsp]; "
     "add rsp,I; pop rdi; ret",
     lambda m, c, j, x: SHARED_RUNTIME in c and len(c) <= 4 and not j and not x,
     "Phyre.SharedRuntimeIdentityDispatchAdapters - EC-7 family C\n"
     "# call shared SharedRuntime 00639850 through a global vtable slot;\n"
     "# compare the result identity/field against this+off and arg3; call a\n"
     "# member op on the matching branch; return 0."),
    ("static-descriptor-singleton-lazyinit-adapters.tsv", 150,
     "sub rsp,I; mov M[rsp],I; mov ecx,M[rip]; mov rax,M[]; mov edx,I; "
     "mov rcx,M[rax+rcx]; mov eax,M[rdx+rcx]; cmp M[rip],eax; jle T; "
     "lea rcx,M[rip]; call T; cmp M[rip],I; jne T; lea rax,M[rip]; or rax,I; "
     "mov M[rip],rax; call T; or rax,I; mov M[rip],rax; call T; "
     "mov M[rip],rax; mov M[rip],I; lea rcx,M[rip]; call T; lea rax,M[rip]; "
     "add rsp,I; ret",
     lambda m, c, j, x: {SINGLETON, CRT_INIT, CRT_TERM} <= c and not j
     and not x,
     "Phyre.StaticDescriptorSingletonLazyInitAdapters - EC-7 family C\n"
     "# bounds-check a global index table; call shared CRT init 008092FC then\n"
     "# shared StaticDescriptorSingleton 0062FF50; or-flag a global tag twice\n"
     "# via member ops; call shared 0080929C; install a member rip pointer."),
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
