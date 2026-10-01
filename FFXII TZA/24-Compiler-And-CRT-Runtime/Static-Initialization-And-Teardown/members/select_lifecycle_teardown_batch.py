"""select_lifecycle_teardown_batch.py - EC-7 family C member selectors for the lifecycle
form batch hosted on static-initialisers-and-teardowns.md (FABLE-REQ-SWE2-EC7-LIFECYCLE-FORM-BATCH).

Five outputs, each selected by an EXACT normalised instruction-form skeleton (mnemonics +
operand kinds; constants, displacements and branch/call targets dropped; registers kept -
the forms_of.py convention). Every selected group is additionally controlled on its
external direct call/jmp targets.

Outputs:
  scalar-deleting-destructors-free.tsv          - the 52-byte deleting-dtor form. This
      selector REGENERATES the whole family (the 53 previously declared members plus
      frontier additions): pool = frontier | (prior members - A-measured), so a member
      that later measures A leaves the family by design.
  scalar-deleting-destructors-shared-base.tsv   - 62-byte spelling: store the vtable,
      call the SHARED base destructor 00212CE0, then conditional free.
  scalar-deleting-destructors-inlined-dtor.tsv  - 43-byte spelling: the destructor body
      is inlined to a vtable store; no destructor call remains.
  two-deallocator-deleting-destructors.tsv      - 66-byte spelling: flags bit 2 selects
      sized operator delete 0016D6A0 over _aligned_free wrapper 00584730 (the idiom
      measured under BQ-26).
  intrusive-list-node-teardowns-115b.tsv        - 115-byte loop: walk an intrusive
      singly-linked node list, call the per-type node teardown (00220390 x32 /
      001AF2B0 x11 - one of the two per member), then a virtual call through the
      owner's vtable, until the list is exhausted.

Refuses to write if a skeleton matches nobody, if a member violates its family's target
control, or if a selected member is already A-measured or owned by another family
(checked against the live checker state).

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_lifecycle_teardown_batch.py [--write]
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

FREE = 0x00809950
BASE_DTOR = 0x00212CE0
ALIGNED_FREE = 0x00584730
SIZED_DELETE = 0x0016D6A0
TREE_DTORS = {0x00220390, 0x001AF2B0}

FAMILIES = [
    # (out tsv, size, skeleton, target predicate, header note)
    ("scalar-deleting-destructors-free.tsv", 52,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov ebx,edx; mov rdi,rcx; call T; test bl,I; "
     "je T; mov edx,I; mov rcx,rdi; call T; mov rax,rdi; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda ts: 0x00809950 in ts and len(ts) == 2,
     "scalar deleting destructors that call free - EC-7 family C\n"
     "# Each member: save rbx/rdi, save the deletion flag, call the per-type destructor,\n"
     "# conditional free(this, size), return this. Regenerated 2026-09-17 by\n"
     "# select_lifecycle_teardown_batch.py (form skeleton match, frontier union prior minus A)."),
    ("scalar-deleting-destructors-shared-base.tsv", 62,
     "mov M[rsp],rbx; push rdi; sub rsp,I; lea rax,M[rip]; mov ebx,edx; mov M[rcx],rax; "
     "mov rdi,rcx; call T; test bl,I; je T; mov edx,I; mov rcx,rdi; call T; mov rax,rdi; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda ts: ts == {BASE_DTOR, FREE},
     "scalar deleting destructors via the shared base destructor 00212CE0 - EC-7 family C\n"
     "# 62-byte spelling: install the member vtable, call 00212CE0, conditional free."),
    ("scalar-deleting-destructors-inlined-dtor.tsv", 43,
     "push rbx; sub rsp,I; lea rax,M[rip]; mov rbx,rcx; mov M[rcx],rax; test dl,I; je T; "
     "mov edx,I; call T; mov rax,rbx; add rsp,I; pop rbx; ret",
     lambda ts: ts == {FREE},
     "scalar deleting destructors, inlined-dtor spelling - EC-7 family C\n"
     "# 43-byte spelling: the destructor body is inlined to a vtable store; the only call\n"
     "# is free(this, size) under the deletion flag."),
    ("two-deallocator-deleting-destructors.tsv", 66,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; lea rax,M[rip]; mov M[rcx],rax; "
     "test dl,I; je T; test dl,I; jne T; call T; nop ; jmp T; mov edx,I; call T; nop ; "
     "mov rax,rbx; add rsp,I; pop rbx; ret",
     lambda ts: ts == {ALIGNED_FREE, SIZED_DELETE},
     "two-deallocator scalar deleting destructors - EC-7 family C\n"
     "# 66-byte spelling: flags bit 2 selects sized operator delete 0016D6A0 (edx = size)\n"
     "# over the _aligned_free wrapper 00584730 - the BQ-26 population."),
    ("intrusive-list-node-teardowns-115b.tsv", 115,
     "push r14; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov M[rsp],rsi; mov M[rsp],rdi; "
     "mov rsi,rcx; mov rbx,M[rcx]; test rbx,rbx; je T; nop M[rax+rax]; mov rdx,M[rbx]; "
     "mov rcx,rsi; call T; nop ; mov rdi,M[rbx]; mov rax,M[rsi]; mov r8d,I; mov rdx,rbx; "
     "lea rcx,M[rsi]; call M[rax]; nop ; mov rbx,rdi; test rdi,rdi; jne T; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; mov rdi,M[rsp]; add rsp,I; pop r14; ret",
     lambda ts: len(ts) == 1 and ts <= TREE_DTORS,
     "intrusive-list node-teardown loops, 115-byte form - EC-7 family C\n"
     "# Walk the intrusive node list at [rcx]: per node, call the member's teardown\n"
     "# (00220390 or 001AF2B0, exactly one per member) then a virtual call through the\n"
     "# owner's vtable slot [rax+0x18] (indirect - outside the direct-target census)."),
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
    toks, targets = [], set()
    for ins in md.disasm(d[off:off + size], a):
        ops = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                ops.append(md.reg_name(op.reg))
            elif op.type == X86_OP_IMM:
                if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
                    ops.append("T")
                    if ins.mnemonic in ("call", "jmp") and not (a <= op.imm < a + size):
                        targets.add(op.imm)
                else:
                    ops.append("I")
            elif op.type == X86_OP_MEM:
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), targets

def prior_members(tsv):
    p = os.path.join(ROOT, tsv)
    out = set()
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8", errors="replace"):
            t = l.split("#")[0].split("\t")[0].split()[0] if l.split("#")[0].strip() else ""
            try: out.add(int(t, 16))
            except (ValueError, IndexError): pass
    return out

def main():
    write = "--write" in sys.argv
    sizes = CD.load_functions(None)
    res = CD.evaluate(CD.DEFAULT_DB, sizes)
    frontier = res["frontier_set"]
    a_set = res["explained_set"] - res["claimed_set"]   # measured A = explained minus declared
    d = open(EXE, "rb").read()
    secs = load_sections(d)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    priors = {tsv: prior_members(tsv) for tsv, _, _, _, _ in FAMILIES}
    pool = set(frontier)
    for tsv, _, _, _, _ in FAMILIES:
        pool |= (priors[tsv] - a_set)
    # form-cache over the pool
    cache = {}
    for a in pool:
        cache[a] = form_and_targets(md, d, secs, a, sizes[a])
    ok = True
    results = {}
    for tsv, sz, skel, tcheck, header in FAMILIES:
        members = sorted(a for a, (f, ts) in cache.items()
                         if sizes[a] == sz and f == norm(skel) and tcheck(ts))
        bad = [a for a in members if a in a_set]
        if bad:
            print("REFUSE %s: %d member(s) measure A" % (tsv, len(bad))); ok = False; continue
        if not members:
            print("REFUSE %s: skeleton matched nobody" % tsv); ok = False; continue
        results[tsv] = (members, header)
        tg = collections.Counter(t for a in members for t in cache[a][1])
        print("%-46s %3d members | targets %s" %
              (tsv, len(members), ", ".join("%08X x%d" % kv for kv in tg.most_common(8))))
    if not ok or not write:
        print("dry run" if ok else "refused")
        return
    for tsv, (members, header) in results.items():
        with io.open(os.path.join(ROOT, tsv), "w", encoding="utf-8", newline="\n") as f:
            f.write("# " + header.replace("\n", "\n# ") + "\n")
            f.write("address\ttargets\n")
            for a in members:
                f.write("%08X\t%s\n" % (a, ",".join("%08X" % t for t in sorted(cache[a][1]))))
        print("wrote", tsv, len(members))

if __name__ == "__main__":
    main()
