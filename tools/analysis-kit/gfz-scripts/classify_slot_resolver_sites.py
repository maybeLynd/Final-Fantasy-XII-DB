#!/usr/bin/env python3
"""Which BANK does each 002ED570 call site resolve against? The element types depend on it.

002ED570 is the slot resolver shared by all three of the render root's banks - EXP-117 executed
its field algebra and it reads the container's +0x30 handle, +0x48 rowStride, +0x4C bankShift
and +0x50 indexMask. Its RETURN is an element pointer, and the element's TYPE depends entirely
on which container went in: a 0x50 resource entry, a 0xC0 element, or a 0x260
RenderModelInstance.

So before either undeclared element can be censused, every call site has to be attributed to a
bank, and a call site that cannot be attributed has to be EXCLUDED rather than guessed - which
is exactly what went wrong in reverse with 0046E420, where two of four callers pass a container
reached by [X+0x330] with no path from any root slot to it.

METHOD, and its limit stated up front. For each call to 002ED570, the last definition of rcx
in program order is taken: `mov rcx, [reg + disp]` attributes the site to the slot at that
displacement; `mov rcx, reg` chains are followed transitively; a register never written in the
body is that function's argument, so the classification recurses - every call site of the
containing function contributes its own arg-k provenance, to a fixed point. A site whose
feeders disagree, or any path that cannot be proven, stays UNATTRIBUTED. THE UNATTRIBUTED
COUNT IS A RESULT, not a failure: it is the population that must be left out of any element
census. site_slot_map() is the engine; the route-seeded census's `bank=` qualifier and this
report run on the same attribution.
"""
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/"
                   "gfz-scripts")
import data_xref_scan as DX  # noqa: E402

EXE = "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe"
FUNCS = "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/graph/functions.tsv"
TARGET = 0x002ED570

SLOT = {0xD90: "RenderResourceEntryBank   (root +0x00, stride 0x50)",
        0xD98: "RenderStrideC0Bank        (root +0x60, stride 0xC0)",
        0xDA0: "RenderModelInstanceContainer (root +0xF0, stride 0x260)",
        0xDA8: "PresentationEntryReferenceContainer (root +0x160) - NOT a 002ED570 descriptor"}


def load():
    """(blob, secs, funcs, md) - shared with any caller that wants the attribution."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    blob = io.open(EXE, "rb").read()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return blob, DX.sections_of(blob), DX.entries(FUNCS), md


ARG_REGS = ("rcx", "rdx", "r8", "r9")
_WRITES = ("mov", "movzx", "movsx", "movsxd", "lea", "xchg", "movabs")


def _breg(name):
    """Canonicalise a capstone register name to its 64-bit form."""
    import re
    name = re.sub(r"^e([abcd]x|[sd]i|[sb]p)$", r"r\1", name)
    return re.sub(r"^r(\d+)([dwb])$", r"r\1", name)


def _def_class(insns, site, reg, md):
    """Provenance classes of `reg` at instruction `site` in a decoded body.

    A class is ('fld', disp) when the register was last written by a plain
    `mov reg, [base + disp]` field load (RIP and stack slots excluded, lea forms
    included - a `lea rcx, [base + disp]` computes the same address the slot
    holds), ('arg', k) when the register is the function's k-th argument and
    this body never writes it, 'imm' for a constant, 'unk' for anything the
    slice cannot prove. Register copies are followed transitively, bounded.
    """
    from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
    seen, wk, out = set(), [(reg, site)], set()
    while wk and len(seen) < 64:
        r, st = wk.pop()
        if (r, st) in seen:
            continue
        seen.add((r, st))
        defs = []
        for ins in insns:
            if ins.address >= st:
                break
            po = ins.operands
            if (po and po[0].type == X86_OP_REG and ins.mnemonic in _WRITES
                    and _breg(md.reg_name(po[0].reg)) == r):
                defs.append(ins)
        if not defs:
            out.add(("arg", ARG_REGS.index(r)) if r in ARG_REGS else "unk")
            continue
        # the LAST def in program order: the qualifier only claims 'the load
        # nearest the call', so a multi-def register resolves by its latest
        # write; a def on a merging alternate path the linear scan cannot see
        # is the documented residual risk of the bank= qualifier
        ins = defs[-1]
        s = ins.operands[1] if len(ins.operands) > 1 else None
        if s is None:
            out.add("unk")
        elif s.type == X86_OP_MEM:
            m = s.value.mem
            if m.index or not m.base or _breg(md.reg_name(m.base)) in ("rsp", "rip"):
                out.add("unk")
            else:
                out.add(("fld", m.disp))
        elif s.type == X86_OP_REG:
            wk.append((_breg(md.reg_name(s.reg)), ins.address))
        elif s.type == X86_OP_IMM:
            out.add("imm")
        else:
            out.add("unk")
    return frozenset(out) or {"unk"}


def site_slot_map(bodies, entries, md, target, arg_reg="rcx", hops=8):
    """{(entry, site): frozenset(classes)} for every call/jmp site to `target`.

    `bodies` maps an entry to its decoded instruction list (or is a callable
    body(entry) -> list); `entries` enumerates function entries. rcx's class is
    taken directly at each site; a class of ('arg', k) is resolved over the
    callee's callers - every call site of the function contributes its own arg-k
    class, transitively, until no site still names an argument. A site that any
    feeding path cannot prove stays 'unk' - exclusion is the safe direction.
    """
    from capstone.x86 import X86_OP_IMM
    if not isinstance(bodies, dict):
        get_body = bodies
        bodies = {e: get_body(e) for e in entries}
    calls = collections.defaultdict(list)
    for e, insns in bodies.items():
        for ins in insns:
            if (ins.mnemonic in ("call", "jmp") and ins.operands
                    and ins.operands[0].type == X86_OP_IMM):
                calls[ins.operands[0].imm].append((e, ins.address))
    sites = {}
    for f, site in calls.get(target, ()):
        sites[(f, site)] = _def_class(bodies[f], site, arg_reg, md)
    for _ in range(hops):
        changed = False
        for (f, site), cls in list(sites.items()):
            if not any(isinstance(c, tuple) and c[0] == "arg" for c in cls):
                continue
            new = set()
            for c in cls:
                if isinstance(c, tuple) and c[0] == "arg":
                    agg = set()
                    for cf, csite in calls.get(f, ()):
                        agg |= _def_class(bodies[cf], csite, ARG_REGS[c[1]], md)
                    new |= (agg or {"unk"})
                else:
                    new.add(c)
            new = frozenset(new)
            if new != cls:
                sites[(f, site)] = new
                changed = True
        if not changed:
            break
    return sites


def classify(blob=None, secs=None, funcs=None, md=None):
    """[(fn, call_site, verdict, detail)] for every 002ED570 call site.

    Exposed as a function because the element census cannot be seeded without it: the
    resolver's return is an element whose TYPE is whichever bank went in, so an element
    census must take only the sites this attributes to its own bank.
    """
    if blob is None:
        blob, secs, funcs, md = load()
    rows, _t = _classify(blob, secs, funcs, md)
    return rows


def _rows_from_map(smap):
    """site_slot_map output -> the (fn, site, verdict, detail) row shape classify()
    has always returned, so the tool's report and any row consumers are unchanged."""
    rows = []
    for (fva, site), cls in sorted(smap.items()):
        flds = {c[1] for c in cls if isinstance(c, tuple) and c[0] == "fld"}
        if len(cls) == 1 and len(flds) == 1:
            d = next(iter(flds))
            verdict = "slot 0x%X" % d if d in SLOT else "other +0x%X" % d
            detail = "provenance: rcx field load at +0x%X (transitive)" % d
        else:
            verdict, detail = "UNATTRIBUTED", "resolved classes: %s" % (
                ", ".join(sorted(map(str, cls))))
        rows.append((fva, site, verdict, detail))
    return rows


def _classify(blob, secs, funcs, md):
    """Rows + tally for the tool's report, driven by the SAME engine the census gate
    uses - site_slot_map - so the standalone report and the instrument cannot
    diverge. The original two-pass local scan is superseded: transitive argument
    resolution attributes the arg-forwarded helpers exactly, and a site fed by
    disagreeing callers stays UNATTRIBUTED in both views."""
    from capstone.x86 import X86_OP_IMM

    def off(va):
        for _n, ro, sz, v in secs:
            if v <= va < v + sz:
                return ro + (va - v)

    bodies = {}
    for fva, fsz in funcs:
        o = off(fva)
        if o is None or fsz <= 0:
            continue
        bodies[fva] = list(md.disasm(blob[o:o + fsz], fva))
    smap = site_slot_map(bodies, list(bodies), md, TARGET)
    rows = _rows_from_map(smap)
    tally = collections.Counter(r[2] for r in rows)
    return rows, tally


def main():
    blob, secs, funcs, md = load()
    rows, tally = _classify(blob, secs, funcs, md)

    print("002ED570 CALL SITES: %d" % len(rows))
    print("\nATTRIBUTION")
    for v, c in tally.most_common():
        note = SLOT.get(int(v.split("0x")[1], 16), "") if v.startswith("slot ") else ""
        print("  %-22s %3d   %s" % (v, c, note))

    att = sum(c for v, c in tally.items() if v.startswith("slot "))
    print("\n  attributable to a render-root slot : %d of %d" % (att, len(rows)))
    print("  NOT attributable, must be EXCLUDED : %d" % (len(rows) - att))

    for slot in sorted(SLOT):
        sel = [r for r in rows if r[2] == "slot 0x%X" % slot]
        if not sel:
            continue
        print("\n%s  -- %d site(s) in %d function(s)"
              % (SLOT[slot], len(sel), len({r[0] for r in sel})))
        for fva, site, _v, d in sel[:12]:
            print("    fn %08X  call %08X   <- %s" % (fva, site, d))
        if len(sel) > 12:
            print("    ... %d more" % (len(sel) - 12))
    return 0


if __name__ == "__main__":
    sys.exit(main())
