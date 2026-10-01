"""select_registry_fetch_traversal_adapters.py - EC-7 family C member selector for the
registry-fetch reflection traversal adapters declared on
class-descriptor-and-metadata-system.md (FABLE-REQ-SWE2-EC7-LIFECYCLE-FORM-BATCH).

PhyreEngine-generated adapters, one per bound type. Each member tests its flag argument
(r8b), calls a member-specific registry getter, then delegates to the shared
Reflection.ObjectTraversal 0063E2E0(registry, object, flag) - the flag selects the
in/out direction - and returns true. Two spellings of one idiom:

  70-byte x69 - xor ecx,ecx clears the getter argument before the flag test.
  68-byte x15 - no argument clear.

In BOTH spellings the getter and ObjectTraversal are each called twice: once on the
flag-true path and once on the flag-false path (the compiler duplicated the tail rather
than sharing it).

Pool = frontier | (prior members - A-measured). Refuses to write if a skeleton matches
nobody, if a member's external direct targets are not exactly {0063E2E0 x2, one
member-specific getter x2}, or if a selected member measures A.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_registry_fetch_traversal_adapters.py [--write]
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
TRAV = 0x0063E2E0
OUT = "registry-fetch-traversal-adapters.tsv"

SPELLINGS = [
    (70,
     "push rbx; sub rsp,I; xor ecx,ecx; mov rbx,rdx; test r8b,r8b; je T; call T; "
     "mov r8b,I; mov rdx,rbx; mov rcx,rax; call T; mov al,I; add rsp,I; pop rbx; ret ; "
     "call T; xor r8d,r8d; mov rdx,rbx; mov rcx,rax; call T; mov al,I; add rsp,I; pop rbx; ret"),
    (68,
     "push rbx; sub rsp,I; mov rbx,rdx; test r8b,r8b; je T; call T; mov r8b,I; "
     "mov rdx,rbx; mov rcx,rax; call T; mov al,I; add rsp,I; pop rbx; ret ; "
     "call T; xor r8d,r8d; mov rdx,rbx; mov rcx,rax; call T; mov al,I; add rsp,I; pop rbx; ret"),
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

def calls(md, d, secs, a, size):
    """Ordered external direct call targets (duplicates kept)."""
    r = a - BASE
    off = next((rp + (r - sva) for sva, sl, rp in secs if sva <= r < sva + sl), None)
    toks, tg = [], []
    for ins in md.disasm(d[off:off + size], a):
        ops = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                ops.append(md.reg_name(op.reg))
            elif op.type == X86_OP_IMM:
                if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
                    ops.append("T")
                    if ins.mnemonic == "call" and not (a <= op.imm < a + size):
                        tg.append(op.imm)
                    elif ins.mnemonic == "jmp" and not (a <= op.imm < a + size):
                        tg.append(op.imm)
                else:
                    ops.append("I")
            elif op.type == X86_OP_MEM:
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), tg

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
    members = []
    getters = collections.Counter()
    for a in sorted(pool):
        form, tg = calls(md, d, secs, a, sizes[a])
        hit = next((sz for sz, skel in SPELLINGS if sizes[a] == sz and form == norm(skel)), None)
        if hit is None:
            continue
        if len(tg) != 4 or collections.Counter(tg) != collections.Counter([tg[0], tg[0], TRAV, TRAV]) \
           or tg[0] == TRAV:
            print("REFUSE %08X: call set %s is not {getter x2, 0063E2E0 x2}" %
                  (a, ",".join("%08X" % t for t in tg)))
            return
        if a in a_set:
            print("REFUSE: %08X measures A" % a); return
        members.append((a, hit, tg[0]))
        getters[tg[0]] += 1
    by_sz = collections.Counter(sz for _, sz, _ in members)
    print("%d members: %s | %d distinct registry getters" % (len(members), dict(by_sz), len(getters)))
    if not write:
        print("dry run"); return
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("# registry-fetch reflection traversal adapters - EC-7 family C\n")
        f.write("# PhyreEngine generated adapters, one per bound type: fetch the type's\n")
        f.write("# registry via its member-specific getter, then call\n")
        f.write("# Reflection.ObjectTraversal 0063E2E0(registry, object, flag) - flag\n")
        f.write("# selects direction - and return true. Getter and traversal are each\n")
        f.write("# called twice (flag-true / flag-false tails). 70B x69 + 68B x15 spellings.\n")
        f.write("address\tsize\tgetter\n")
        for a, sz, g in members:
            f.write("%08X\t%d\t%08X\n" % (a, sz, g))
    print("wrote", OUT, len(members))

if __name__ == "__main__":
    main()
