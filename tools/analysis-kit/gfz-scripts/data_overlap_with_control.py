#!/usr/bin/env python3
"""data_overlap_with_control.py - do two function groups share data because they share a FEATURE,
or because everything in the subsystem touches the same infrastructure? The control decides.

    python data_overlap_with_control.py              # the worked UQ-355 example
    python data_overlap_with_control.py --self-test  # the two instrument failures, checked

THE PATTERN THIS EXISTS FOR. "System A and system B reference the same globals, so B took over
A's job" is a tempting inference and a cheap measurement. It is also almost always wrong in this
image, because presentation code shares a stack cookie, a draw-bracket flag, an emulated-GPR
scratch block and a transform workbench. **Run a third group that is KNOWN to be unrelated. If it
scores like the hypothesis, the measurement does not discriminate and the ratio means nothing.**

The worked example below is UQ-355, where exactly that happened - see section 7 of
`99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`.

---

Written as the UQ-355 re-run, with the addressing form the first run could not see.

The queued OPUS record says the measurement collected "every rip-relative data address each body
references". `data_xref_scan.py`'s own docstring says that is the wrong instrument for this
binary:

    **This binary does not address globals RIP-relative.** It loads the image base into a
    register once and then uses `[reg + index*8 + disp]` ... A RIP-relative xref scan therefore
    returns **zero hits for globals that are demonstrably referenced.**

So the first run measured a projection of the reference set, and its overlap ratio is a ratio of
that projection. This re-run collects BOTH forms - RIP-relative and image-base-displacement -
and keeps only targets that land in a data section, so code addresses taken by `lea` are not
counted as data.

Three populations, the third being the control that killed the original result:

  DEAD    the island proper, the five functions of the page's section 5 call chain
  LIVE3X3 002D6990's 3x3 atlas patch system and the three helpers section 5 names
  CTRL    002DC290, the live box drawer, which section 5 says has "nothing to do with this
          island" and is reached from eleven unrelated callers

If CTRL scores like LIVE3X3, the measurement does not discriminate, whichever addressing form it
is run in.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP  # noqa: E402
import data_xref_scan as DX  # noqa: E402

EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")

# The UQ-355 populations, kept as the worked example and the script's self-check.
DEAD = [0x00392A10, 0x00392CE0, 0x002DD1E0, 0x002DC7F0, 0x002DD090]
LIVE3X3 = [0x002D6990, 0x002DA7C0, 0x002DAC70, 0x002DAF30]
CTRL = [0x002DC290]

DOC = {
    0x022D8F30: "shared scratch (intentionally-ownerless-functions-and-shared-scratch.md)",
    0x022D8F38: "shared scratch neighbour",
    0x022D8F40: "shared scratch neighbour",
    0x022D8F48: "shared scratch neighbour",
    0x02EBEFC0: "shared transform workbench (two-transform-primitives)",
    0x01F44830: "stack cookie - every function with a stack array",
}


def virtual_sections(blob):
    """(va, virtual_size) for every non-.text section, from the PE header.

    `data_xref_scan.sections_of` reports RAW sizes. `.data`'s raw size ends at 0x01F7E400
    while its VIRTUAL extent runs far past it, and the uninitialised globals this test is
    about - the shared scratch at 022D8F30, the transform workbench at 02EBEFC0 - live in
    that BSS tail. A data-section filter built on raw sizes therefore discards exactly the
    addresses in question and reports one hit per group. Same instrument class as the rest
    of this test: a bound that looks right and silently truncates.
    """
    pe = int.from_bytes(blob[0x3C:0x40], "little")
    nsec = int.from_bytes(blob[pe + 6:pe + 8], "little")
    optsz = int.from_bytes(blob[pe + 20:pe + 22], "little")
    base = int.from_bytes(blob[pe + 24 + 24:pe + 24 + 32], "little")
    t = pe + 24 + optsz
    out = []
    for i in range(nsec):
        e = t + i * 40
        nm = blob[e:e + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsz = int.from_bytes(blob[e + 8:e + 12], "little")
        rva = int.from_bytes(blob[e + 12:e + 16], "little")
        if nm.startswith(".text"):
            continue
        out.append((base + rva, vsz))
    return out


def sizes(path):
    out = {}
    for n, line in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        if n == 0:
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) < 3:
            continue
        try:
            out[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
    return out


def refs(blob, secs, fva, fsize, datasecs):
    """{va: form} for every data address this body references, both addressing forms."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP

    def off(va):
        for _n, ro, sz, v in secs:
            if v <= va < v + sz:
                return ro + (va - v)
        return None

    def in_data(va):
        return any(v <= va < v + sz for v, sz in datasecs)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    o = off(fva)
    out = {}
    if o is None:
        return out
    for i in md.disasm(blob[o:o + fsize], fva):
        for op in i.operands:
            if op.type != X86_OP_MEM:
                continue
            d = op.mem.disp
            if op.mem.base == X86_REG_RIP:
                ea, form = i.address + i.size + d, "rip"
            elif d > 0x100000:
                ea, form = DX.IMAGE_BASE + d, "base"
            else:
                continue
            if in_data(ea):
                out.setdefault(ea, form)
    return out


def collect(blob, secs, datasecs, sz, group):
    u = {}
    for fva in group:
        if fva not in sz:
            print("  !! %08X not in functions.tsv" % fva)
            continue
        for ea, form in refs(blob, secs, fva, sz[fva], datasecs).items():
            u.setdefault(ea, form)
    return u


def self_test():
    """The instrument's two failure modes, both of which produced confident numbers.

    Neither is about the UQ-355 answer; both are about whether the scan can SEE what it is
    asked about. A data-section filter that cannot see `.data`'s BSS tail, and a reference
    collector that only knows one of this binary's two addressing forms, each return a small
    tidy number rather than an error.
    """
    ok = True
    blob = io.open(EXE, "rb").read()
    secs = virtual_sections(blob)
    for probe, what in ((0x022D8F30, "shared scratch, in .data's BSS tail"),
                        (0x02EBEFC0, "transform workbench, in .data's BSS tail"),
                        (0x01F44830, "stack cookie, inside .data's raw extent")):
        hit = any(v <= probe < v + sz for v, sz in secs)
        ok &= hit
        print("  %08X visible to the data filter: %-3s  (%s)"
              % (probe, "yes" if hit else "NO", what))
    raw = DX.sections_of(blob)
    blind = [p for p in (0x022D8F30, 0x02EBEFC0)
             if not any(v <= p < v + s for _n, _o, s, v in raw)]
    print("  addresses a RAW-size filter would have discarded: %s"
          % (", ".join("%08X" % p for p in blind) or "none"))
    ok &= len(blind) == 2   # if this ever becomes 0 the warning below is obsolete, not passing
    print("SELF-TEST", "PASSES" if ok else "FAILS")
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    blob = io.open(EXE, "rb").read()
    secs = DX.sections_of(blob)
    datasecs = virtual_sections(blob)
    for probe in (0x022D8F30, 0x02EBEFC0, 0x01F44830):
        hit = any(v <= probe < v + sz for v, sz in datasecs)
        print("  filter control %08X in a data section: %s" % (probe, "yes" if hit else "NO"))
        if not hit:
            raise SystemExit("the data-section filter cannot see a known data address; refused")
    sz = sizes(FUNCS)

    dead = collect(blob, secs, datasecs, sz, DEAD)
    live = collect(blob, secs, datasecs, sz, LIVE3X3)
    ctrl = collect(blob, secs, datasecs, sz, CTRL)

    print("UQ-355 DATA OVERLAP, both addressing forms, data sections only")
    print("  DEAD    %d functions -> %2d distinct data addresses" % (len(DEAD), len(dead)))
    print("  LIVE3X3 %d functions -> %2d distinct data addresses" % (len(LIVE3X3), len(live)))
    print("  CTRL    %d function  -> %2d distinct data addresses" % (len(CTRL), len(ctrl)))

    dl, dc = set(dead) & set(live), set(dead) & set(ctrl)
    print()
    print("  DEAD n LIVE3X3 (the hypothesis): %d" % len(dl))
    print("  DEAD n CTRL    (the control)   : %d" % len(dc))
    print("  the control's share of the hypothesis' overlap: %d of %d"
          % (len(dl & dc), len(dl)))

    def show(title, s):
        print("\n  %s" % title)
        if not s:
            print("      (none)")
        for ea in sorted(s):
            forms = "/".join(sorted({f for f in (dead.get(ea), live.get(ea), ctrl.get(ea)) if f}))
            print("      %08X  [%-8s] %s" % (ea, forms, DOC.get(ea, "-- not documented as shared")))

    show("shared by DEAD and LIVE3X3:", dl)
    show("shared by DEAD and the CONTROL:", dc)
    show("DEAD n LIVE3X3 but NOT reached by the control (the only discriminating set):",
         dl - dc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
