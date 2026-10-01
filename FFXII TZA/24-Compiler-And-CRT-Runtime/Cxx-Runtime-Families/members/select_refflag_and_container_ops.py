"""select_refflag_and_container_ops.py - EC-7 family C member selectors for the
ref-flag handle and container-emplace idioms declared on
object-construction-destruction-and-static-lifetime.md
(SWE2-EC7-FRONTIER-FORM-CLUSTERS).

The ref-flag record is {dword size|own-flag, qword ptr} like the counted-buffer
families declared beside these; bit 31 of the first field is the ownership flag.

  refflag-handle-store-with-release.tsv (109B x15) - reject a negative
      (bit31-set) r8d with return 5; if the record's stored ptr differs from
      rdx and its own-flag is clear, btr the flag and call a member-specific
      release on the old ptr; commit {size=r8|bit31, ptr=rdx}; return 0.
  refflag-handle-reset.tsv (69B x13) - if the record's own-flag is clear, btr
      and call a member-specific release on the stored ptr; either way zero
      the record's {size, ptr} fields.
  intrusive-virtual-node-dispose-loop.tsv (93B x12) - walk the intrusive
      circular list rooted at [rcx]; virtual-call [rdi+0x10][0x18](node, 0x18)
      on each node until back at the head. No direct external targets.
  malloc-record-emplace-adapters.tsv (144B x14) - malloc(0x18), optional
      member-specific record init, push the record into the caller's
      capacity-bounded container (growth via shared 001AB570), then call the
      member-specific fetch 0018B4E0 shape and tail-jump shared 0018AFF0.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_refflag_and_container_ops.py [--write]
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

MALLOC = 0x0085E730
GROW = 0x001AB570
FETCH = 0x0018B4E0
CONT = 0x0018AFF0

def one_member_release(c, j, x):
    return len(c) == 1 and not j and not x

FAMILIES = [
    ("refflag-handle-store-with-release.tsv", 109,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov ebx,r8d; "
     "mov rsi,rdx; mov rdi,rcx; test r8d,r8d; jns T; mov eax,I; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret; mov rcx,M[rcx]; cmp rcx,rsi; "
     "je T; mov edx,M[rdi]; mov eax,edx; shr eax,I; not al; test al,I; je T; "
     "btr edx,I; call T; bts ebx,I; mov M[rdi],rsi; mov rsi,M[rsp]; "
     "xor eax,eax; mov M[rdi],ebx; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     one_member_release,
     "ref-flag handle store with release - EC-7 family C\n"
     "# negative r8d -> return 5; if stored ptr differs and own-flag clear,\n"
     "# btr + member release on old ptr; commit {size|bit31, ptr}; return 0."),
    ("refflag-handle-reset.tsv", 69,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; mov edx,M[rcx]; "
     "mov eax,edx; shr eax,I; not al; test al,I; je T; btr edx,I; "
     "mov rcx,M[rcx]; call T; nop; xor eax,eax; mov M[rbx],rax; "
     "mov M[rbx],eax; jmp T; xor eax,eax; mov M[rcx],rax; mov M[rcx],eax; "
     "add rsp,I; pop rbx; ret",
     one_member_release,
     "ref-flag handle reset - EC-7 family C\n"
     "# if the record's own-flag is clear, btr + member release on the stored\n"
     "# ptr; either way zero the {size, ptr} fields."),
    ("intrusive-virtual-node-dispose-loop.tsv", 93,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov M[rsp],rsi; "
     "mov rdi,rcx; mov rbx,M[rcx]; cmp rbx,rcx; je T; nop M[rax]; "
     "nop M[rax+rax]; mov rdx,rbx; mov rbx,M[rbx]; mov rax,M[rdi]; mov r8d,I; "
     "lea rcx,M[rdi]; call M[rax]; nop; cmp rbx,rdi; jne T; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     lambda c, j, x: not c and not j and not x,
     "intrusive virtual node-dispose loop - EC-7 family C\n"
     "# walk the intrusive circular list at [rcx]; virtual-call\n"
     "# [rdi+0x10][0x18](node, 0x18) per node until back at head.\n"
     "# No direct external targets."),
    ("malloc-record-emplace-adapters.tsv", 144,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov rdi,rcx; "
     "or r8d,I; xor edx,edx; lea ecx,M[rdx]; call T; mov M[rsp],rax; "
     "mov M[rsp],rax; test rax,rax; je T; mov rcx,rax; call T; mov rbx,rax; "
     "jmp T; xor ebx,ebx; mov M[rsp],rbx; mov rdx,M[rdi]; cmp rdx,M[rdi]; "
     "jae T; lea rax,M[rdx]; mov M[rdi],rax; test rdx,rdx; je T; "
     "mov M[rdx],rbx; jmp T; lea r8,M[rsp]; mov rcx,rdi; call T; "
     "mov rbx,M[rsp]; call T; mov rcx,rax; mov rdx,rbx; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; jmp T",
     lambda c, j, x: {MALLOC, GROW, FETCH} <= c and len(c) == 4
                     and j == {CONT} and not x,
     "malloc record emplace adapters - EC-7 family C\n"
     "# malloc(0x18) + optional member init + push into the caller's\n"
     "# capacity-bounded container (growth 001AB570) + member fetch 0018B4E0\n"
     "# shape; tail-jump shared 0018AFF0."),
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
    toks, calls, jmps, jccs = [], set(), set(), set()
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
            elif op.type == X86_OP_MEM:
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), calls, jmps, jccs

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
        members = sorted(a for a, (f, c, j, x) in cache.items()
                         if sizes[a] == sz and f == norm(skel) and tcheck(c, j, x))
        if not members:
            print("REFUSE %s: skeleton matched nobody" % tsv); ok = False; continue
        bad = [a for a in members if a in a_set]
        if bad:
            print("REFUSE %s: %d member(s) measure A" % (tsv, len(bad))); ok = False; continue
        results[tsv] = (members, header)
        tg = collections.Counter(t for a in members for t in cache[a][1] | cache[a][2] | cache[a][3])
        print("%-52s %3d members | targets %s" %
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
