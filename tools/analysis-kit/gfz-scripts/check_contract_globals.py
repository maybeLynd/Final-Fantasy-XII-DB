#!/usr/bin/env python3
"""For every data address a contract cites, say whether the image shows a writer.

Why this exists. Three contract-first probes in a row hit the same wall: the contract
named a global and did not resolve its VALUE or its WRITER, and the implementation could
not be finished without one. Twice the answer was reachable statically within the hour
(the coast-down time base at 01DFE0B4, a constant 2 stored once; the stop-frame counter
at +0x457, one writer whose clamp overflows the field). Once it was not (the authored
table resolver's base at 01F83530). That is a repeating, cheap-to-detect gap shape, so
it is worth detecting once instead of rediscovering per probe.

WHAT A ROW MEANS, AND WHAT IT DOES NOT. "no writer seen" is a statement about this
instrument, never about the image. The sweep sees rip-relative and absolute-disp32
accesses. It does NOT see a write through a pointer held in a register -- which is how
the authored-table registry slots are written, from a `lea` at the call site. So a
global with no visible writer is a CANDIDATE to investigate, and the thing that raises
it from candidate to finding is a second check the tool also reports: whether anything
takes the global's address with a `lea`. No writer AND no `lea` is a strong negative.
No writer WITH a `lea` means the tool is simply blind there.

.bss matters because a global past the end of its section's raw data starts as zero. A
.bss global with no visible writer and no `lea` is very likely zero for the life of the
process, and that is usually a load-bearing fact rather than a detail.

PROSE_ONLY, added 2026-09-18 (SWE2-CONTRACT, on OPUS-FINDING-CONTRACT-GLOBALS-BUCKET-IS-
MIXED).  The harvest regex takes every eight-hex-digit token, so the candidate bucket also
collects addresses a contract mentions WITHOUT citing them as globals it depends on:
range endpoints, a section's raw-extent bound used in an explanation, an address the
contract itself retracts, a counterexample, a status-mask value that happens to look like
an address.  OPUS measured the mixing: 4 of the first 6 sampled rows were artifacts.
Every remaining row was then read in context -- the exclusions below are per (address,
contract) with the reason, so the sweep stays conservative (nothing is hidden from the
writer/lea test) while "candidate" once again means "a global this contract depends on".
The excluded rows are printed separately; a retraction removed from prose must also be
removed here.

CONTROL, on every run: registry slot 02EBF138 is written -- CONTRACT-authored-table-row-
lookup names 003845F0 doing it through a pointer -- so it MUST come back "no writer seen"
with a `lea` present. If it ever reports a writer, the sweep has started seeing something
it cannot really see, and every negative it prints is suspect. Exit 2 if the control
does not behave.
"""
import collections
import bisect
import re
import struct
import sys
from pathlib import Path

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP
except ImportError:
    print("capstone is required"); sys.exit(2)

ROOT = Path(__file__).resolve().parents[3] / "FFXII TZA"
WORK = Path(__file__).resolve().parents[2] / "work"
EXE = WORK / "exe" / "FFXII_TZA.exe"
GRAPH = WORK / "graph" / "functions.tsv"

CONTROL = 0x02EBF138
# Second control, the positive one: a global written by a FLOAT store (see the end of main).
STORE_CONTROL = 0x01F82D28

# (address, contract path relative to ROOT) -> why the citation is not a dependency.
# Classified 2026-09-18 by reading every row of the bucket in context; see the docstring.
PROSE_ONLY = {
    (0x01F7E400, "02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md"):
        "the .data raw-extent bound, cited while explaining why another address is empty",
    (0x01F7E400, "17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md"):
        "the .data raw-extent bound in an explanation",
    (0x01FC3E8C, "17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md"):
        "cited precisely to say it is past .data's raw extent",
    (0x01DF6E38, "17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md"):
        "named inside a crossing paragraph about another layer's routine",
    (0x02B4052C, "17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md"):
        "an address the contract itself retracts (the gate cell is 02B40524)",
    (0x01F80544, "15-Input/Binding-Profiles/CONTRACT-binding-profiles.md"):
        "end bound of the census range 01F80130-01F80544",
    (0x01F83500, "02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md"):
        "start bound of the sweep range 01F83500-01F83560",
    (0x02EBF0D0, "02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md"):
        "a registry slot cited as a NON-qualifying counterexample",
    (0x02000000, "10-Status-Periodic-Terminal/CONTRACT-status-write.md"):
        "a cascade MASK VALUE inside a decode list, not an address",
    (0x02099A88, "04-Actor-Entity/CONTRACT-field-runtime-pass.md"):
        "a retracted address (digit transposition of 02099AB8), struck in place",
    (0x02099AB7, "04-Actor-Entity/CONTRACT-field-runtime-pass.md"):
        "end bound of slot 4's block",
    (0x02099D3F, "04-Actor-Entity/CONTRACT-field-runtime-pass.md"):
        "end bound of slot 5's block",
    (0x022C6D00, "04-Actor-Entity/CONTRACT-field-runtime-pass.md"):
        "a relocation-census range bound",
    (0x022C6D40, "04-Actor-Entity/CONTRACT-field-runtime-pass.md"):
        "a relocation-census range bound",
    (0x02649E10, "06-Movement-And-Navigation/CONTRACT-movement-body-pool.md"):
        "cited precisely to say the contract never states it and it appears nowhere",
    (0x02CB8600, "22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md"):
        "a retracted address (the misaligned-decode lea quote, struck in place 2026-09-18)",
    (0x02CAA080, "22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md"):
        "the 02CAA080-02CAA140 census range bound",
    (0x02CAA140, "22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md"):
        "the 02CAA080-02CAA140 census range bound",
    (0x01EFAC08, "08-Combat-Formula/CONTRACT-preparation-step-family.md"):
        "end bound of the 202-entry calculator table",
    (0x01F44000, "08-Combat-Formula/CONTRACT-preparation-step-family.md"):
        "an image-page base in a demand-mapping explanation",
    (0x01F43F10, "21-RNG-And-Determinism/CONTRACT-gameplay-generators.md"):
        "a pointer value inside a memory-dump quote, not a cited global",
}


def load_image():
    d = EXE.read_bytes()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        name = d[o:o + 8].rstrip(b"\0").decode(errors="replace")
        vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((name, va, vsz, ptr, rsz))
    return d, base, secs


def classify(va, base, secs):
    """section name, and whether the address is past its raw data (-> .bss, zero)."""
    r = va - base
    for name, sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return name, (r - sva) >= rsz
    return None, False


def main():
    if not EXE.exists() or not GRAPH.exists():
        print("image or function graph missing"); return 2
    d, base, secs = load_image()

    contracts = sorted(ROOT.glob("*/CONTRACT-*.md")) + \
        sorted(ROOT.glob("*/*/CONTRACT-*.md"))

    # data addresses each contract cites
    cited = {}
    for p in contracts:
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in re.findall(r"\b0[0-2][0-9A-F]{6}\b", text):
            va = int(m, 16)
            sec, _ = classify(va, base, secs)
            if sec in (".data", ".rdata"):
                cited.setdefault(va, set()).add(p)
    targets = set(cited) | {CONTROL, STORE_CONTROL}

    fns = []
    for line in GRAPH.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        f = line.split("\t")
        try:
            fns.append((int(f[0], 16), int(f[2]), f[1]))
        except (ValueError, IndexError):
            pass
    fns.sort()
    starts = [f[0] for f in fns]

    def owner(va):
        i = bisect.bisect_right(starts, va) - 1
        if i >= 0 and va < fns[i][0] + fns[i][1]:
            return fns[i][2]
        return "?"

    def v2f(va):
        r = va - base
        for _, sva, vsz, ptr, rsz in secs:
            if sva <= r < sva + max(vsz, rsz):
                return ptr + (r - sva)
        return None

    # THE WRITER TEST USED TO BE `mov add sub and or xor inc dec`, AND A GLOBAL THE GAME WRITES
    # EVERY FRAME CAME BACK AS "writable storage that nothing writes and nothing points at".
    # FABLE found it on the ramp contract (FABLE-NOTICE-OPUS-CONTRACT-GLOBALS-WRITERS, 2026-09-14):
    # 01F82D28 is written by `movsd qword [rip]` at 001E04B4/001E04CB/001E0610, and 01E02801 by
    # `sete byte [rip]` at 001D47F1.  Neither mnemonic was in the set, so both printed as
    # CANDIDATES -- a contract reader was told a live global is load-time constant.
    #
    # The gate's own control did not catch it: the control global (02EBF138) is written through a
    # POINTER, so it exercises the no-writer path and never a store mnemonic at all.  A control
    # that can only confirm the answer you already expect is not a control, so a second one is
    # added below that must come back WITH a writer.
    #
    # An allowlist is still the right shape -- `cmp [rip], 0` and `push qword [rip]` both put the
    # memory operand at index 0 and neither writes -- so the cure is to widen it and, crucially,
    # to make it SAY SO when it meets a mnemonic in neither list.  A silent drop is what this cost.
    STORES = frozenset((
        # integer store / read-modify-write
        "mov", "add", "sub", "and", "or", "xor", "inc", "dec", "adc", "sbb", "neg", "not",
        "shl", "sal", "shr", "sar", "rol", "ror", "rcl", "rcr", "shld", "shrd",
        "bts", "btr", "btc", "xadd", "xchg", "cmpxchg", "cmpxchg8b", "cmpxchg16b", "pop",
        "movbe", "movnti",
        # SSE/x87 stores.  These are loads when the memory operand is on the right; the i == 0
        # test already separates those, so listing the mnemonic is safe.
        "movss", "movsd", "movaps", "movapd", "movups", "movupd", "movdqa", "movdqu",
        "movd", "movq", "movlps", "movhps", "movlpd", "movhpd", "movntps", "movntpd",
        "movntdq", "maskmovdqu",
        # string MOVES reached through a rep prefix (prefix stripped above).  `cmps*` and
        # `scas*` are deliberately NOT here: they compare, they do not store.
        "movsb", "movsw", "movsq",
        "fst", "fstp", "fist", "fistp", "fisttp", "fbstp",
        "fnstsw", "fnstcw", "fstsw", "fstcw", "fnsave", "fsave", "fxsave",
        # string stores (capstone may render the destination explicitly)
        "stosb", "stosw", "stosd", "stosq",
    ))
    # Memory at operand 0 and NOT a write.  Listed so the unclassified counter stays meaningful
    # instead of shouting about instructions that were always correctly ignored.
    READS_WITH_MEM_DEST = frozenset((
        "cmp", "test", "push", "jmp", "call", "bt",
        # one-operand arithmetic: the memory operand is the SOURCE (divisor/multiplicand)
        "div", "idiv", "mul", "imul",
        # string compares/scans: they read, and reach here with a rep/repe prefix stripped
        "cmpsb", "cmpsw", "cmpsq", "scasb", "scasw", "scasd", "scasq",
        "fld", "fild", "fbld", "fadd", "fsub", "fmul", "fdiv", "fsubr", "fdivr", "fcom",
        "fcomp", "ficom", "ficomp", "fldcw", "fldenv", "frstor", "fxrstor",
        "prefetch", "prefetcht0", "prefetcht1", "prefetcht2", "prefetchnta",
        "nop", "ud2", "int3",
    ))

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    writers = {a: [] for a in targets}
    leas = {a: 0 for a in targets}
    unclassified = collections.Counter()
    for ent, ln, nm in fns:
        f = v2f(ent)
        if f is None or ln <= 0:
            continue
        for ins in md.disasm(d[f:f + ln], ent):
            ops = ins.operands
            for i, op in enumerate(ops):
                if op.type != X86_OP_MEM:
                    continue
                m = op.mem
                if m.base == X86_REG_RIP:
                    ea = ins.address + ins.size + m.disp
                elif m.base == 0 and m.index == 0:
                    ea = m.disp
                else:
                    continue
                if ea not in writers:
                    continue
                if ins.mnemonic == "lea":
                    leas[ea] += 1
                elif i == 0:
                    # Capstone folds prefixes into the mnemonic -- "lock xadd", "rep stosq",
                    # "lock cmpxchg".  An exact-string set test misses every one of those, so
                    # strip the prefix before looking.  Measured 2026-09-14 over all 38,161
                    # graph functions: 27 `lock xadd`, 11 `lock cmpxchg`, 92 `rep stos*`,
                    # 24 `rep movs*` and 3 `lock inc/dec` write memory at operand 0.
                    mn = ins.mnemonic
                    for pfx in ("lock ", "rep ", "repe ", "repne ", "repz ", "repnz "):
                        if mn.startswith(pfx):
                            mn = mn[len(pfx):]
                            break
                    if mn in STORES or mn.startswith("set") or mn.startswith("vmov"):
                        writers[ea].append((ins.address, owner(ins.address)))
                    elif mn not in READS_WITH_MEM_DEST:
                        # NOT a write and NOT a known read: the allowlist has met something it
                        # was never told about.  Counted and printed rather than dropped -- the
                        # whole defect this set was widened for was a silent drop.
                        unclassified[mn] += 1

    rows = []
    for va in sorted(cited):
        sec, is_bss = classify(va, base, secs)
        rows.append((va, sec, is_bss, writers[va], leas[va], cited[va]))

    # .rdata is read-only by definition: "no writer" there is the linker doing its job,
    # not a gap in a contract. Counting those as candidates buried the four that matter
    # under seventeen float constants, so they are separated rather than listed.
    silent = [r for r in rows if not r[3] and r[4] == 0 and r[1] != ".rdata"]
    consts = [r for r in rows if not r[3] and r[4] == 0 and r[1] == ".rdata"]
    blind = [r for r in rows if not r[3] and r[4] > 0]
    print("DATA GLOBALS CITED BY CONTRACTS: %d\n" % len(rows))
    print("  with a visible writer             : %d" % (len(rows) - len(silent) - len(blind) - len(consts)))
    print("  .rdata constants, no writer expected: %d" % len(consts))
    n_prose = sum(1 for va, _, _, _, _, ps in silent for p in ps
                  if (va, p.relative_to(ROOT).as_posix()) in PROSE_ONLY)
    n_rows = sum(len(ps) for _, _, _, _, _, ps in silent)
    print("  writable, no writer AND no lea      : %d  (%d citation rows: %d candidate, %d prose)" % (
        len(silent), n_rows, n_rows - n_prose, n_prose))
    print("  writable, no writer but a lea exists: %d" % len(blind))

    prose = []   # (va, tag, rel, reason) -- mentions, not dependencies
    print("\nCANDIDATES -- writable storage that nothing writes and nothing points at.")
    print("A .bss entry here is probably zero for the life of the process; a .data entry")
    print("is probably an authored table that is read and never modified:")
    candidates = 0
    for va, sec, is_bss, _, _, ps in sorted(silent, key=lambda r: (not r[2], r[0])):
        tag = ".bss (zero at load)" if is_bss else sec
        for p in sorted(ps):
            rel = p.relative_to(ROOT).as_posix()
            why = PROSE_ONLY.get((va, rel))
            if why is not None:
                prose.append((va, tag, rel, why))
                continue
            candidates += 1
            print("  %08X  %-20s %s" % (va, tag, rel))
    if prose:
        print("\nEXCLUDED PROSE CITATIONS (%d) -- cited in the text but not as a global the"
              % len(prose))
        print("contract depends on (see PROSE_ONLY; drop the row if the citation changes):")
        for va, tag, rel, why in prose:
            print("  %08X  %-20s %s -- %s" % (va, tag, rel, why))

    # CONTROL ---------------------------------------------------------------
    print("\nCONTROL: registry slot %08X is written through a pointer, so it must come" % CONTROL)
    print("back with NO visible writer but WITH a lea. Anything else means the sweep is")
    print("reporting writes it cannot actually see.")
    w, l = writers[CONTROL], leas[CONTROL]
    if w or l == 0:
        print("  CONTROL FAILED: writers=%d leas=%d -- negatives here are not trustworthy."
              % (len(w), l))
        return 2
    print("  control passed: 0 visible writers, %d lea(s)." % l)

    # SECOND CONTROL --------------------------------------------------------
    # The control above exercises only the NO-writer path, which is why it stayed green through
    # the whole time `movsd` and `sete` stores were being dropped.  This one must come back WITH
    # a writer, and it is a float store, so it fails if the store mnemonics are ever narrowed
    # again.  01F82D28 is written by `movsd qword [rip]` at 001E04B4/001E04CB/001E0610
    # (FABLE-NOTICE-OPUS-CONTRACT-GLOBALS-WRITERS).
    print("\nSECOND CONTROL: %08X is written by `movsd qword [rip]` in %d sites, so it must" % (
        STORE_CONTROL, 3))
    print("come back WITH visible writers. A control that can only confirm a negative is")
    print("not a control -- this is the one the widened store set is accountable to.")
    sw = writers.get(STORE_CONTROL, [])
    if not sw:
        print("  CONTROL FAILED: 0 visible writers -- the store mnemonics are too narrow again,")
        print("  and every CANDIDATE above may be a global the game writes every frame.")
        return 2
    print("  control passed: %d visible writer(s) -- %s." % (
        len(sw), ", ".join("%08X" % a for a, _ in sorted(sw)[:4])))

    if unclassified:
        print("\nMEMORY AT OPERAND 0, MNEMONIC IN NEITHER LIST (%d distinct).  Not counted as a"
              % len(unclassified))
        print("write and not known to be a read -- printed so the next one is found on the run")
        print("that meets it, not by a reader noticing a contract reads wrong:")
        for mn, n in unclassified.most_common():
            print("  %-14s %d" % (mn, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
