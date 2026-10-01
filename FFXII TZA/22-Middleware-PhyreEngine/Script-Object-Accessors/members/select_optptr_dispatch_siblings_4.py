"""select_optptr_dispatch_siblings_4.py - EC-7 family C member selectors,
fourth pass (SWE2-EC7-FRONTIER-FORM-CLUSTERS-4), declared on
phyre-script-object-accessors.md.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_optptr_dispatch_siblings_4.py [--write]
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

def leaf(m, c, j, x):
    return not c and not j and not x
def one_call(m, c, j, x):
    return len(c) == 1 and not j and not x
def call_tail(m, c, j, x):
    return len(c) == 1 and len(j) == 1 and not x
def jcc_tail(m, c, j, x):
    return not c and not j and len(x) == 1
def shared_only(*ts):
    want = set(ts)
    return lambda m, c, j, x: c == want and not j and not x
def shared_calls(*ts):
    want = set(ts)
    return lambda m, c, j, x: want <= set(c) and not j and not x
def shared_any(*ts):
    want = set(ts)
    return lambda m, c, j, x: want <= (set(c) | set(j) | set(x))
def targets_exact(nc, nj, nx):
    return lambda m, c, j, x: len(c) == nc and len(j) == nj and len(x) == nx
def form_only(m, c, j, x):
    return True

FAMILIES = [
    ("nativeadapter-optptrmembercallvcallforward.tsv", 103,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,rcx; mov rdi,rdx; "
     "mov rcx,rdx; call T; mov rcx,rax; call M[rbx]; mov rcx,rdi; "
     "test rax,rax; je T; lea r8,M[rip]; mov rdx,rax; call T; mov eax,I; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; ret; mov edx,I; call T; "
     "mov rcx,rdi; call T; mov rbx,M[rsp]; mov eax,I; add rsp,I; pop rdi; "
     "ret",
     shared_any(0x0080F420, 0x00810620),
     "NativeAdapter.OptPtrMemberCallVcallForward - EC-7 family C\n"
     "call a member lookup on arg1; vcall [this+8] slot on the result; if\n"
     "# non-null forward via cloned forwarder 00684090 with a member rip\n"
     "# descriptor; else shared 0080F420 + 00810620 fallback; return 1."
),
    ("nativeadapter-optptrallocrecordinstall.tsv", 104,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,rdx; mov rdi,r8; "
     "mov rcx,rbx; mov edx,I; call T; mov edx,I; mov rcx,rbx; call T; "
     "test rax,rax; je T; lea rcx,M[rip]; mov M[rax],rdi; mov M[rax],rcx; "
     "lea r8,M[rip]; mov edx,I; mov rcx,rbx; call T; mov edx,I; "
     "mov rcx,rbx; mov rbx,M[rsp]; add rsp,I; pop rdi; jmp T",
     shared_any(0x0080F420, 0x0080FA50, 0x00810240, 0x00810F60),
     "NativeAdapter.OptPtrAllocRecordInstall - EC-7 family C\n"
     "push arg1 onto the optptr stack via shared 0080F420; allocate a 0x10\n"
     "# record via shared 00810240; install member rip descriptor + arg3; call\n"
     "# shared 0080FA50 with a member tag; tail shared 00810F60 with edx=-2."
),
    ("nativeadapter-optptrmemberoffsetvcall.tsv", 120,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rbx,rcx; "
     "mov rdi,rdx; mov rcx,rdx; call T; mov rcx,rdi; mov rsi,rax; call T; "
     "test rax,rax; je T; movsxd rcx,M[rbx]; mov rdx,rsi; add rcx,rax; "
     "call M[rbx]; mov edx,I; mov rcx,rdi; mov ebx,eax; call T; "
     "mov edx,ebx; mov rcx,rdi; call T; mov eax,I; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x0080F420, 0x00810580),
     "NativeAdapter.OptPtrMemberOffsetVcall - EC-7 family C\n"
     "call member ops 005BCD20 + 005BC4D0-shape on arg1; if non-null vcall\n"
     "# [this+8] at member offset +[this+0x10]; then shared 0080F420 + 00810580\n"
     "# pop/store; return 1."
),
    ("nativeadapter-optptrmembercallclonedforward.tsv", 80,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rdi,rcx; mov rbx,rdx; "
     "mov rcx,rdx; call T; test rax,rax; je T; mov rcx,rax; call M[rdi]; "
     "lea r8,M[rip]; mov rcx,rbx; mov rdx,rax; call T; mov eax,I; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; ret; mov rbx,M[rsp]; add rsp,I; "
     "pop rdi; ret",
     shared_any(0x00684080),
     "NativeAdapter.OptPtrMemberCallClonedForward - EC-7 family C\n"
     "call a member lookup on arg1; if non-null vcall [this+8]; forward via\n"
     "# cloned forwarder 00684080 with a member rip descriptor; return 1."
),
    ("nativeadapter-optptrfloatpipelinelookup.tsv", 171,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rbx,rdx; "
     "mov rdi,rcx; mov rcx,rbx; xor r8d,r8d; or edx,I; call T; mov edx,I; "
     "mov rcx,rbx; mov rsi,rax; call T; mov rcx,rbx; call T; test rax,rax; "
     "je T; mov edx,esi; mov rcx,rax; call M[rdi]; mov rcx,rbx; "
     "test rax,rax; je T; lea r8,M[rip]; mov rdx,rax; call T; mov eax,I; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret; mov edx,I; "
     "call T; mov rcx,rbx; call T; mov eax,I; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x00684080, 0x0080F420, 0x00810620, 0x00811130, 0x00811470),
     "NativeAdapter.OptPtrFloatPipelineLookup - EC-7 family C\n"
     "run shared 00811470 + 0080F420 + 00810620 on arg1; if non-null vcall\n"
     "# [this+8] slot on it; if still non-null forward via cloned 00684080 +\n"
     "# shared 00811130; return 1 else shared fallback path."
),
    ("nativeadapter-optptrmembercallvcallresult.tsv", 116,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rbx,rcx; "
     "mov rdi,rdx; mov rcx,rdx; call T; mov rcx,rdi; mov rsi,rax; call T; "
     "test rax,rax; je T; mov rdx,rsi; mov rcx,rax; call M[rbx]; mov edx,I; "
     "mov rcx,rdi; mov ebx,eax; call T; mov edx,ebx; mov rcx,rdi; call T; "
     "mov eax,I; mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x0080F420, 0x00810580),
     "NativeAdapter.OptPtrMemberCallVcallResult - EC-7 family C\n"
     "call member ops on arg1; if non-null vcall [this+8] on the second\n"
     "# result; then shared 0080F420 + 00810580; return 1."
),
    ("nativeleaf-taggedoutrecordvptrstore.tsv", 103,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,r9; mov r9,rcx; "
     "mov rdi,r8; test rdx,rdx; je T; movsxd rax,M[rcx]; lea rcx,M[rdx]; "
     "add rcx,rax; call M[r9]; mov rcx,rax; test rbx,rbx; je T; "
     "lea rax,M[rip]; or rax,I; cmp rdi,rax; jne T; mov M[rbx],I; "
     "mov eax,I; mov M[rbx],rcx; mov rbx,M[rsp]; add rsp,I; pop rdi; ret; "
     "xor eax,eax; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     leaf,
     "NativeLeaf.TaggedOutRecordVptrStore - EC-7 family C\n"
     "if arg1 non-null vcall [this+8] at member offset +[this+0x10] on\n"
     "# arg1-8+index; if arg3 matches a member rip|1 tag, store the result into\n"
     "# the out record and return 1 else 0."
),
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
