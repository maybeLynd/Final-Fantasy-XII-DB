"""select_optptr_dispatch_siblings_2.py - EC-7 family C member selectors,
second frontier form-cluster pass (SWE2-EC7-FRONTIER-FORM-CLUSTERS-2), declared
on phyre-script-object-accessors.md.

Further sibling spellings of the optional-pointer dispatch idiom already
declared on this page. All guard on a pointer taken from [r8] (or a member
result); on the non-null path they tail-call shared adapter 00810620 (or the
cloned forwarder 00684080/00684090), on the null path they call shared
0080F420 (or 00810580) with a member code and tail-call the second adapter:

  optptr-offsetadd-dispatch-adapters (64B) - rdx=[r8]+member disp; lea
      r8=member record; true path tails 00810620; null path calls 0080F420
      with edx=0x19 and tails a cloned forwarder.
  optptr-membercall-dispatch-adapters (75B) - rdi=[r8] saved; call member op;
      true path tails 00810620 with rdx=rdi; null path calls 0080F420
      (edx=0x19) and tails a member op.
  optptr-membercall-resultdispatch-adapters (78B) - same with r8=call-result
      forwarded into the true-path tail.
  optptr-membercall-vcall-dispatch (87B) - member vcall on the deref; on the
      non-null path calls 00810580 with edx=0x10 then a member op; returns 1.
  optptr-membercall-forward-adapters (45B) - call member op; forward
      (result, r8, rdx) to cloned forwarder 00684080.
  tagged-outrecord-vcall-adapters (94B) - member vcall on rdx; if the out
      pointer equals member rip tag|1, store the result record {1, rcx}.
  tagged-outrecord-vcall-advance-adapters (113B) - same idiom with an
      incremented input field (add [rax+0x30],1) before the vcall.

Each group is one operand-aware byte image.
Pool = frontier | (prior members - A-measured); A beats a declaration.
Usage: python select_optptr_dispatch_siblings_2.py [--write]
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

ADAPT_A = 0x00810620
ADAPT_B = 0x00810580
DISPATCH = 0x0080F420
CLONES = {0x00684080, 0x00684090}

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

FAMILIES = [
    ("optptr-offsetadd-dispatch-adapters.tsv", 64,
     "push rbx; sub rsp,I; mov rbx,rdx; mov rdx,M[r8]; mov rcx,rbx; "
     "test rdx,rdx; je T; add rdx,I; lea r8,M[rip]; add rsp,I; pop rbx; "
     "jmp T; mov edx,I; call T; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: c == {DISPATCH} and ADAPT_A in j and j <=
     {ADAPT_A} | CLONES and not x,
     "OptPtr.OffsetAddDispatchAdapters - EC-7 family C\n"
     "# rdx=[r8]+member disp; r8=member record; true path tails shared\n"
     "# 00810620; null path calls shared 0080F420 (edx=0x19) and tails a\n"
     "# cloned forwarder 00684080/00684090."),
    ("optptr-membercall-dispatch-adapters.tsv", 75,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rdi,M[r8]; mov rbx,rdx; "
     "call T; mov rcx,rbx; test rdi,rdi; je T; mov rdx,rdi; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; jmp T; mov edx,I; call T; mov rcx,rbx; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: DISPATCH in c and len(c) == 2 and ADAPT_A in j
     and len(j) == 2 and not x,
     "OptPtr.MemberCallDispatchAdapters - EC-7 family C\n"
     "# rdi=[r8] saved; call member op; true path tails shared 00810620 with\n"
     "# rdx=rdi; null path calls shared 0080F420 (edx=0x19) and tails a\n"
     "# member op."),
    ("optptr-membercall-resultdispatch-adapters.tsv", 78,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rdi,M[r8]; mov rbx,rdx; "
     "call T; mov rcx,rbx; test rdi,rdi; je T; mov r8,rax; mov rdx,rdi; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; jmp T; mov edx,I; call T; "
     "mov rcx,rbx; mov rbx,M[rsp]; add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: DISPATCH in c and len(c) == 2 and ADAPT_A in j
     and j <= {ADAPT_A} | CLONES and not x,
     "OptPtr.MemberCallResultDispatchAdapters - EC-7 family C\n"
     "# as the 75B sibling but forwards the member call's result in r8 to the\n"
     "# true-path tail 00810620."),
    ("optptr-membercall-vcall-dispatch.tsv", 87,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,rcx; mov rdi,rdx; "
     "mov rcx,rdx; call T; test rax,rax; je T; mov rcx,rax; call M[rbx]; "
     "mov edx,I; mov rcx,rdi; mov ebx,eax; call T; mov edx,ebx; mov rcx,rdi; "
     "call T; mov eax,I; mov rbx,M[rsp]; add rsp,I; pop rdi; ret; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: {DISPATCH, ADAPT_B} <= c and len(c) == 3
     and not j and not x,
     "OptPtr.MemberCallVcallDispatch - EC-7 family C\n"
     "# member op on rdx; member vcall on the result; on the non-null path\n"
     "# call shared 00810580 (edx=0x10) then a member op; return 1."),
    ("optptr-membercall-forward-adapters.tsv", 45,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,r8; mov rdi,rdx; call T; "
     "mov r8,rax; mov rdx,rbx; mov rcx,rdi; mov rbx,M[rsp]; add rsp,I; "
     "pop rdi; jmp T",
     lambda m, c, j, x: len(c) == 1 and len(j) == 1 and j <= CLONES and not x,
     "OptPtr.MemberCallForwardAdapters - EC-7 family C\n"
     "# call a member op; forward (result, r8, rdx) to the cloned forwarder\n"
     "# 00684080/00684090."),
    ("tagged-outrecord-vcall-adapters.tsv", 94,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,r9; mov rdi,r8; "
     "mov rax,rcx; test rdx,rdx; je T; mov rcx,rdx; call M[rax]; mov rcx,rax; "
     "test rbx,rbx; je T; lea rax,M[rip]; or rax,I; cmp rdi,rax; jne T; "
     "mov M[rbx],I; mov eax,I; mov M[rbx],rcx; mov rbx,M[rsp]; add rsp,I; "
     "pop rdi; ret; xor eax,eax; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: not c and not j and not x,
     "Tagged.OutRecordVcallAdapters - EC-7 family C\n"
     "# member vcall on rdx; if the out pointer equals member rip tag|1,\n"
     "# store the result record {1, rcx}; return 1/0. No direct calls."),
    ("tagged-outrecord-vcall-advance-adapters.tsv", 113,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,r9; mov rdi,r8; "
     "mov r9,rdx; mov r8,rcx; test rdx,rdx; je T; mov rax,M[rsp]; "
     "mov rcx,r9; add M[rax],I; mov rax,M[rax]; mov edx,M[rax]; call M[r8]; "
     "mov rcx,rax; test rbx,rbx; je T; lea rax,M[rip]; or rax,I; cmp rdi,rax; "
     "jne T; mov M[rbx],I; mov eax,I; mov M[rbx],rcx; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; ret; xor eax,eax; mov rbx,M[rsp]; add rsp,I; "
     "pop rdi; ret",
     lambda m, c, j, x: not c and not j and not x,
     "Tagged.OutRecordVcallAdvanceAdapters - EC-7 family C\n"
     "# as the 94B sibling with an incremented input field (add [rax+0x30],1)\n"
     "# before the member vcall."),
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
