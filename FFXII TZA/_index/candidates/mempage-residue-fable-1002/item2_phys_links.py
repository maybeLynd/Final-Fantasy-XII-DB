"""item2_phys_links.py - the arena block header's +0x0C / +0x10 link pair: every writer, every reader, and where the
chain starts (FABLE, 2026-10-02). Static, read-only.

Question (memory page, "Two link pairs"): "What is NOT established is where that second list is rooted."

Method
  S1  width-aware sweep over the arena module (every listed body whose entry lies in 00369700..0036D300, the
      initializer to the free shim): every memory operand whose byte range overlaps header bytes +0x0C..+0x13
      (disp d, width w with d < 0x14 and d + w > 0x0C), stack and rip operands excluded. Each is tagged:
        DEC  a dword load into ecx that reaches ImageAddress_ResolveRuntimePointer 0020E600 (the link decode)
        ENC  a dword store of eax produced by RuntimePointer_EncodeImageAddress 0020E620 (the link encode)
        other  everything else (descriptor fields, slot records, ...), printed so nothing is silently dropped.
  S2  image-wide: every raw call/jmp to 0020E600 whose ecx was last loaded from dword [X+0x0C] or [X+0x10], and
      every raw call to 0020E620 whose eax next goes to dword [X+0x0C] or [X+0x10] - so a reader or writer OUTSIDE
      the module range is still seen. Inline decodes (rip operands on the base cell 01F83530 outside the codec) in
      functions that also touch +0x0C/+0x10 are listed.
  S3  the anchor: the initializer's stores to descriptor +0x10 / +0x90 / +0x98 and the header fill it calls.

Controls (instrument sees known sites)
  K1  0036B235 `mov ecx, dword ptr [rdi + 0xc]` -> 0020E600 in the coalescer 0036B210 (the page's citation) is DEC.
  K2  0036A4EE and 0036A501, the header fill 0036A490's encode stores to +0x0C / +0x10, are ENC.
  K3  the unlinker 0036C9D0 (EXP-078's faulting stores) shows at least one ENC at +0x0C or +0x10.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp_lib import *

DEC, ENC, BASECELL = 0x20E600, 0x20E620, 0x1F83530
LO, HI = 0x369700, 0x36D300
fails = []


def is_link(op):
    return op.type == X86_OP_MEM and op.mem.base not in (X86_REG_RIP, 0) and reg_name(op.mem.base) not in ("rsp",) \
        and op.mem.disp in (0x0C, 0x10) and op.size == 4 and op.mem.index == 0


def tag(ins, k):
    """DEC / ENC / '' for instruction k."""
    x = ins[k]
    ops = x.op_str.replace(" ", "")
    if x.mnemonic == "mov" and ops.startswith("ecx,dword") and any(is_link(o) for o in x.operands):
        for j in range(k + 1, min(k + 6, len(ins))):
            y = ins[j]
            if y.mnemonic in ("call", "jmp") and y.op_str == hex(DEC):
                return "DEC"
            if y.mnemonic.startswith("j") or y.mnemonic in ("call", "ret") or y.op_str.replace(" ", "").startswith(("ecx,", "rcx,")):
                break
    if x.mnemonic == "mov" and ops.endswith(",eax") and any(is_link(o) and (o.access & CS_AC_WRITE) for o in x.operands):
        for j in range(k - 1, max(k - 6, -1), -1):
            y = ins[j]
            if y.mnemonic == "call" and y.op_str == hex(ENC):
                return "ENC"
            if y.mnemonic == "call" or y.mnemonic.startswith("j") or y.op_str.replace(" ", "").startswith(("eax,", "rax,")):
                break
    return ""


def main():
    out = []
    p = out.append
    p("# item 2 - the +0x0C/+0x10 link pair (static). run: item2_phys_links.py at %s" % head_sha())
    fam = [f for f in all_functions() if LO <= f < HI]
    p("\n## S1 arena module: %d listed bodies in 00369700..0036D300" % len(fam))
    links = []   # (addr, fn, tag, rw, text)
    others = 0
    for fn in fam:
        ins = decode(fn)
        for k, x in enumerate(ins):
            for op in x.operands:
                if op.type != X86_OP_MEM or op.mem.base in (X86_REG_RIP, 0) or reg_name(op.mem.base) == "rsp":
                    continue
                dsp, w = op.mem.disp, op.size
                if x.mnemonic == "lea" or not (dsp < 0x14 and dsp + w > 0x0C):
                    continue
                rw = ("w" if op.access & CS_AC_WRITE else "") + ("r" if op.access & CS_AC_READ else "")
                t = tag(ins, k)
                if t:
                    links.append((x.address, fn, t, rw, x.mnemonic + " " + x.op_str))
                else:
                    others += 1
                    p("  other  %08X in %08X  w%d %-2s %s %s" % (x.address, fn, w, rw, x.mnemonic, x.op_str))
    p("  -- link-tagged accesses (DEC = decoded link read, ENC = encoded link store):")
    for a, fn, t, rw, s in links:
        p("  %s    %08X in %08X  %s" % (t, a, fn, s))
    p("  counts: DEC %d, ENC %d, other %d" % (sum(1 for l in links if l[2] == "DEC"), sum(1 for l in links if l[2] == "ENC"), others))
    known = {(l[0], l[2]) for l in links}
    if (0x36B235, "DEC") not in known: fails.append("K1")
    if (0x36A4EE, "ENC") not in known or (0x36A501, "ENC") not in known: fails.append("K2")
    if not any(l[1] == 0x36C9D0 and l[2] == "ENC" for l in links): fails.append("K3")
    # S2 image-wide
    p("\n## S2 image-wide codec sites on +0x0C/+0x10 (raw call index of the codec, decoded per owner)")
    idx = raw_index([DEC, ENC])
    p("  raw sites: 0020E600 %d (%d aligned), 0020E620 %d (%d aligned)" % (
        len(idx[DEC]), sum(1 for h in idx[DEC] if h[3]), len(idx[ENC]), sum(1 for h in idx[ENC] if h[3])))
    outside = []
    for t in (DEC, ENC):
        for site, form, o, al in idx[t]:
            if not al:
                continue
            ins = decode(o)
            k = [i for i, x in enumerate(ins) if x.address == site][0]
            hit = None
            if t == DEC:
                for j in range(k - 1, max(k - 6, -1), -1):
                    y = ins[j]
                    if y.op_str.replace(" ", "").startswith(("ecx,", "rcx,")):
                        if y.mnemonic == "mov" and any(is_link(op) for op in y.operands):
                            hit = y
                        break
                    if y.mnemonic.startswith("j") or y.mnemonic == "call":
                        break
            else:
                for j in range(k + 1, min(k + 6, len(ins))):
                    y = ins[j]
                    if y.mnemonic == "mov" and y.op_str.replace(" ", "").endswith(",eax") and any(is_link(op) and (op.access & CS_AC_WRITE) for op in y.operands):
                        hit = y; break
                    if y.op_str.replace(" ", "").startswith(("eax,", "rax,")) or y.mnemonic.startswith("j") or y.mnemonic in ("call", "ret"):
                        break
            if hit is not None and not (LO <= o < HI):
                outside.append((hit.address, o, "DEC" if t == DEC else "ENC", hit.mnemonic + " " + hit.op_str))
    p("  codec sites on a +0x0C/+0x10 dword OUTSIDE the module range: %d (DEC %d, ENC %d) in %d bodies - the same"
      " codec serves the authored tables, so these are filtered for arena awareness below" % (
        len(outside), sum(1 for o in outside if o[2] == "DEC"), sum(1 for o in outside if o[2] == "ENC"), len({o[1] for o in outside})))

    def arena_aware(fn):
        for x in decode(fn):
            if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and LO <= int(x.op_str, 16) < HI:
                return "calls %s" % x.op_str
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and 0x22D7FD0 <= rip_target(x, op) < 0x22D8F10:
                    return "arena global %08X" % rip_target(x, op)
                if op.type == X86_OP_IMM and op.imm in (0xFF12, 0xFF99):
                    return "header magic %#x" % op.imm
        return ""
    aw = {}
    for o in {o[1] for o in outside}:
        r = arena_aware(o)
        if r:
            aw[o] = r
    p("  of those bodies, arena-aware (call a module body, touch an arena global 022D7FD0..022D8F10, or use the"
      " header magic): %d" % len(aw))
    for a, o, t, s in outside:
        if o in aw:
            p("    %s %08X in %08X %s  %s   [%s]" % (t, a, o, names.get(o, ""), s, aw[o]))
    inl = set()
    for fn in all_functions():
        if fn in (DEC, ENC):
            continue
        for x in decode(fn):
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == BASECELL:
                    inl.add(fn)
    inl_link = []
    for fn in sorted(inl):
        if any(is_link(op) for x in decode(fn) for op in x.operands):
            inl_link.append(fn)
    p("  bodies reading the base cell 01F83530 directly (inline codec): %d; of those, also touching a +0x0C/+0x10 dword: %d" % (len(inl), len(inl_link)))
    for fn in inl_link:
        p("    %08X %s%s" % (fn, names.get(fn, ""), "  (in module range)" if LO <= fn < HI else ""))
    # S3 anchor
    p("\n## S3 anchor: initializer stores and the header fill")
    for x in decode(0x369D30):
        if x.address in (0x369F74, 0x369F8C, 0x369F95, 0x369FA7, 0x369FD4, 0x369F9C):
            p("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    for x in decode(0x36A490):
        if x.address in (0x36A4D3, 0x36A4EE, 0x36A4F1, 0x36A501):
            p("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    p("\nFAILS %d %s" % (len(fails), fails))
    open(os.path.join(HERE, "item2_phys_links.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


main()
