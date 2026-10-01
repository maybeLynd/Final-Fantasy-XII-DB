"""select_magic_static_pair_initialisers.py - EC-7 family C member selector for the
magic-static descriptor-pair initialisers declared on
lazy-statics-and-the-one-time-init-lock.md (FABLE-REQ-SWE2-EC7-LIFECYCLE-FORM-BATCH).

These are the init-CALLING siblings of the page's 61-member 115-byte descriptor-pair
accessor family: each member is a thread-safe local-static accessor under the
_Init_thread_header/footer (008092FC / 0080929C) bracket whose init payload installs a
descriptor PAIR - one statically-known pointer tagged |1 plus either a second tagged
constant or the result of one member-specific init call - then returns &static.

Three measured spellings, ONE family (same idiom, payload variation only):
  133-byte x16 - payload is inlined stores only; call set is exactly {header, footer}.
  134-byte x25 - payload calls one init function (00630180 x18 / 006301F0 x4 /
                 00630490 x3); the result is stored untagged beside the tagged constant.
  138-byte x16 - payload calls one init function (0062FF50 x7 / 006B19A0 x3 /
                 006B09E0 x2 / 006B1600 x2 / 006B33F0 / 006B0EC0); the result is stored
                 tagged |1.

Pool = frontier | (prior members - A-measured): a member that later measures A leaves
the family. Refuses to write if a skeleton matches nobody, if a member's external direct
targets are not {008092FC, 0080929C} plus at most one member-specific init callee, or if
a selected member measures A.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_magic_static_pair_initialisers.py [--write]
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
ITH, ITF = 0x008092FC, 0x0080929C
OUT = "magic-static-pair-initialisers.tsv"

SPELLINGS = [
    (133,
     "sub rsp,I; mov rax,M[]; mov ecx,M[rip]; mov edx,I; mov rcx,M[rax+rcx]; "
     "mov eax,M[rdx+rcx]; cmp M[rip],eax; jg T; lea rax,M[rip]; add rsp,I; ret ; "
     "lea rcx,M[rip]; call T; cmp M[rip],I; jne T; lea rax,M[rip]; mov M[rip],I; "
     "or rax,I; lea rcx,M[rip]; mov M[rip],rax; lea rax,M[rip]; or rax,I; "
     "mov M[rip],rax; call T; jmp T"),
    (134,
     "sub rsp,I; mov M[rsp],I; mov ecx,M[rip]; mov rax,M[]; mov edx,I; mov rcx,M[rax+rcx]; "
     "mov eax,M[rdx+rcx]; cmp M[rip],eax; jle T; lea rcx,M[rip]; call T; cmp M[rip],I; "
     "jne T; lea rax,M[rip]; or rax,I; mov M[rip],rax; call T; mov M[rip],rax; "
     "mov M[rip],I; lea rcx,M[rip]; call T; lea rax,M[rip]; add rsp,I; ret"),
    (138,
     "sub rsp,I; mov M[rsp],I; mov ecx,M[rip]; mov rax,M[]; mov edx,I; mov rcx,M[rax+rcx]; "
     "mov eax,M[rdx+rcx]; cmp M[rip],eax; jle T; lea rcx,M[rip]; call T; cmp M[rip],I; "
     "jne T; lea rax,M[rip]; or rax,I; mov M[rip],rax; call T; or rax,I; mov M[rip],rax; "
     "mov M[rip],I; lea rcx,M[rip]; call T; lea rax,M[rip]; add rsp,I; ret"),
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

def main():
    write = "--write" in sys.argv
    sizes = CD.load_functions(None)
    res = CD.evaluate(CD.DEFAULT_DB, sizes)
    frontier = res["frontier_set"]
    a_set = res["explained_set"] - res["claimed_set"]
    d = open(EXE, "rb").read()
    secs = load_sections(d)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    prior = set()
    p = os.path.join(ROOT, OUT)
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8", errors="replace"):
            t = l.split("#")[0].split("\t")[0].strip()
            try: prior.add(int(t.split()[0], 16))
            except (ValueError, IndexError): pass
    pool = set(frontier) | (prior - a_set)
    members, inits = [], collections.Counter()
    for a in sorted(pool):
        form, ts = form_and_targets(md, d, secs, a, sizes[a])
        if not any(sizes[a] == sz and form == norm(skel) for sz, skel in SPELLINGS):
            continue
        extra = ts - {ITH, ITF}
        if {ITH, ITF} - ts or len(extra) > 1:
            print("REFUSE %08X: targets %s outside the controlled set" %
                  (a, ",".join("%08X" % t for t in sorted(ts))))
            return
        if a in a_set:
            print("REFUSE: %08X measures A" % a); return
        members.append((a, next(sz for sz, skel in SPELLINGS if sizes[a] == sz and form == norm(skel))))
        for t in extra:
            inits[t] += 1
    by_sz = collections.Counter(sz for _, sz in members)
    print("%d members: %s" % (len(members), dict(by_sz)))
    print("init callees:", ", ".join("%08X x%d" % kv for kv in inits.most_common()))
    if not write:
        print("dry run"); return
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("# magic-static descriptor-pair initialisers - EC-7 family C\n")
        f.write("# Init-calling siblings of the 115-byte descriptor-pair accessors:\n")
        f.write("# thread-safe local-static accessors (Init_thread_header/footer bracket)\n")
        f.write("# that install a tagged descriptor pointer pair, then return &static.\n")
        f.write("# 133B payload: inlined stores only. 134B/138B: one member-specific init call.\n")
        f.write("address\tsize\ttargets\n")
        for a, sz in members:
            _, ts = form_and_targets(md, d, secs, a, sizes[a])
            f.write("%08X\t%d\t%s\n" % (a, sz, ",".join("%08X" % t for t in sorted(ts))))
    print("wrote", OUT, len(members))

if __name__ == "__main__":
    main()
