#!/usr/bin/env python3
"""check_literal_base_access.py - the third addressing pattern a reference map cannot see.

THE QUESTION THIS ANSWERS (`IB-2`). A reference map keyed on `[rip + disp]` operands sees where a
literal data address is *loaded* and nothing after it. When a function `lea`s a literal base into a
register, does ARITHMETIC on that register - an index, a scale, an add - and only then dereferences
it, the map records the `lea` and misses the accessor, its stride and its field offsets. The database
has been bitten by this twice (`DD-1`, and `022D94B0`, whose section 21 found two such functions BY
HAND). `IB-2` recorded that "a prototype built for this block **failed its positive control on
`0036E320`**, the very function the document names, and was not shipped", and that the population was
unmeasured.

WHY PATTERN MATCHING FAILED AND THIS DOES NOT. A pattern matcher asks whether an instruction *looks
like* the idiom, and the idiom's whole point is that the load and the use are several instructions
and one arithmetic step apart. This propagates a TAINT instead: a register derived from a literal
base stays derived through `lea`, `add`, `sub`, `imul`, `shl`, `and`, `or`, `inc`, `dec`, `movsxd`
and a plain register copy; it stops being derived when something unrelated is written into it, and
the volatile registers are dropped at every `call`. That is dataflow at one function's scope, which
is what the question said it needed.

WHAT COUNTS AS A HIT, AND WHAT DELIBERATELY DOES NOT. Only an access whose base register was
MODIFIED since the `lea`, or which carries a scaled index. A plain `[base + constant]` is exactly
what a reference map already sees, so counting it would inflate the population with the very cases
that are not the question.

THE CONTROL IS THE POINT, AND IT IS ASSERTED. `0036E320` and `0036E540` must both appear. They are
the two functions `022D94B0` section 21 found by hand, and they are the control the earlier prototype
failed. **If they do not appear this exits non-zero and says the run is not evidence** - a sweep that
cannot see the cases a human already found cannot be trusted to have measured the rest.

    python check_literal_base_access.py            # the census, with the control
    python check_literal_base_access.py --all      # every function, not the top 15
    python check_literal_base_access.py --base 022D94B0     # one literal base only

Exit 0 when the control passes, 1 when it fails, 2 on a usage or environment error.
"""
import argparse
import collections
import hashlib
import io
import os
import struct
import sys

try:
    import capstone
except ImportError:                                     # pragma: no cover
    capstone = None

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uc1_band
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
GRAPH = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
AUTHORITY = "73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8"
BASE = 0x120000
CONTROL = (0x0036E320, 0x0036E540)

VOLATILE_NAMES = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
KEEPS = {"add", "sub", "imul", "shl", "sal", "and", "or", "inc", "dec", "lea", "movsxd"}
WRITERS = {"mov", "movss", "movsd", "movups", "movaps", "movzx", "movsx", "or", "and",
           "add", "sub", "xor", "inc", "dec"}


def sections(buf):
    pe = struct.unpack_from("<I", buf, 0x3C)[0]
    nsec = struct.unpack_from("<H", buf, pe + 6)[0]
    optsz = struct.unpack_from("<H", buf, pe + 20)[0]
    off = pe + 24 + optsz
    out = []
    for i in range(nsec):
        s = buf[off + i * 40: off + (i + 1) * 40]
        name = s[:8].rstrip(b"\0").decode("ascii", "replace")
        vsize, vaddr, rawsz, rawptr = struct.unpack_from("<IIII", s, 8)
        out.append((name, vaddr, vsize, rawptr, rawsz))
    return out


def load_functions(path):
    """-> (sorted entries, {entry: end}). The walk must not cross a function boundary: a taint is a
    fact about one frame, and the next function's prologue does not inherit it."""
    import bisect as _b
    ents, ends = [], {}
    with io.open(path, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        ie, ib = head.index("entry"), head.index("body_bytes")
        inm, iow = head.index("name"), head.index("owner")
        meta = {}
        for line in fh:
            r = line.rstrip("\n").split("\t")
            if len(r) <= max(ie, ib, inm, iow):
                continue
            try:
                e, n = int(r[ie], 16), int(r[ib])
            except ValueError:
                continue
            ents.append(e)
            ends[e] = e + n
            meta[e] = (r[inm], r[iow] or "(none)")
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(GRAPH):
        _b = uc1_band.load()
        for e in _b["removed"]:
            ends.pop(e, None)
            meta.pop(e, None)
        for e, en in _b["extend"].items():
            if e in ends:
                ends[e] = en
        for st, sz in _b["frontier"].items():
            ends[st] = st + sz
            meta[st] = ("UC1-FRONTIER-%08X" % st, "(none)")
        ents = sorted(ends)
    else:
        ents.sort()
    return ents, ends, meta, _b


def sweep(only_base=None):
    """-> (hits, meta). hits is {function entry: [(addr, base, kind, mnemonic, ops)]}."""
    buf = io.open(EXE, "rb").read()
    digest = hashlib.sha256(buf).hexdigest().upper()
    if digest != AUTHORITY:
        raise SystemExit("image is not the authority build: %s" % digest)
    secs = sections(buf)
    data = [(BASE + v, BASE + v + max(vs, rs)) for n, v, vs, rp, rs in secs
            if n in (".data", ".rdata")]
    text = [s for s in secs if s[0] == ".text"][0]
    _, vaddr, vsize, rawptr, rawsz = text
    start = BASE + vaddr
    code = buf[rawptr:rawptr + rawsz]

    ents, ends, meta, bisect = load_functions(GRAPH)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    X = capstone.x86
    volatile = {getattr(X, "X86_REG_" + n.upper()) for n in VOLATILE_NAMES}
    RIP = X.X86_REG_RIP

    def in_data(va):
        return any(lo <= va < hi for lo, hi in data)

    def owner(a):
        i = bisect.bisect_right(ents, a) - 1
        if i < 0:
            return None
        e = ents[i]
        return e if e <= a < ends[e] else None

    # Linear sweep; capstone stops at the first undecodable byte (padding, data-in-text), so
    # resume one byte later rather than losing the rest of the section.
    insns = []
    pos = 0
    while pos < len(code):
        got = 0
        for ins in md.disasm(code[pos:], start + pos):
            insns.append(ins)
            got = ins.address - (start + pos) + ins.size
        pos += max(got, 1)

    hits = collections.defaultdict(list)
    cur, taint = None, {}
    for ins in insns:
        o = owner(ins.address)
        if o != cur:
            cur, taint = o, {}
        if o is None:
            continue
        ops = ins.operands

        for n, op in enumerate(ops):
            if op.type != X.X86_OP_MEM or op.mem.base == 0:
                continue
            t = taint.get(op.mem.base)
            if not t:
                continue
            base, moved = t
            if only_base is not None and base != only_base:
                continue
            if not (moved or op.mem.index != 0):
                continue                       # a plain [base + const] is already on the map
            # `cmp` and `test` put their first operand first and write neither, so operand
            # position alone would call every bounds check a write.
            kind = "write" if (n == 0 and ins.mnemonic in WRITERS) else "read"
            hits[o].append((ins.address, base, kind, ins.mnemonic, ins.op_str))

        if ins.mnemonic == "call":
            for r in [r for r in taint if r in volatile]:
                del taint[r]
            continue
        if not ops or ops[0].type != X.X86_OP_REG:
            continue
        d = ops[0].reg
        if ins.mnemonic == "lea" and len(ops) == 2 and ops[1].type == X.X86_OP_MEM:
            m = ops[1].mem
            if m.base == RIP:
                tgt = ins.address + ins.size + m.disp
                # A `lea` off RIP REPLACES whatever the register held. If the new target is not in
                # a data section the register is simply no longer a literal data base - it must not
                # keep the taint it had a moment ago.
                if in_data(tgt):
                    taint[d] = (tgt, False)
                else:
                    taint.pop(d, None)
            elif m.base in taint:
                taint[d] = (taint[m.base][0], True)     # lea off a tainted base IS the arithmetic
            elif m.index in taint:
                taint[d] = (taint[m.index][0], True)
            else:
                taint.pop(d, None)
            continue
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X.X86_OP_REG \
                and ops[1].reg in taint:
            taint[d] = taint[ops[1].reg]
            continue
        if ins.mnemonic in KEEPS and d in taint:
            taint[d] = (taint[d][0], True)
            continue
        if ins.mnemonic in ("test", "cmp"):
            continue
        taint.pop(d, None)
    return hits, meta


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--base")
    a = ap.parse_args(argv)
    if capstone is None:
        print("capstone is required", file=sys.stderr)
        return 2
    if not os.path.isfile(EXE):
        print("the authority image is not at %s" % EXE, file=sys.stderr)
        return 2

    hits, meta = sweep(int(a.base, 16) if a.base else None)
    sites = sum(len(v) for v in hits.values())
    print("LITERAL BASE + ARITHMETIC, then dereferenced")
    print("  %d function(s), %d site(s)" % (len(hits), sites))

    ok = all(c in hits for c in CONTROL)
    print("\n  POSITIVE CONTROL - %s" % ("PASS" if ok else "FAIL"))
    for c in CONTROL:
        rows = hits.get(c, [])
        print("     %08X  %-38s %d site(s)%s"
              % (c, meta.get(c, ("?",))[0][:38], len(rows), "" if rows else "   <- NOT FOUND"))
        for addr, base, kind, m, o in rows[:4]:
            print("         %08X  %-5s base %08X   %s %s" % (addr, kind, base, m, o))
    if not ok:
        print("\n  THE RUN IS NOT EVIDENCE. 0036E320 and 0036E540 are the two functions 022D94B0")
        print("  section 21 found by hand; a sweep that cannot see them has not measured anything.")
        return 1

    byfn = sorted(hits.items(), key=lambda kv: -len(kv[1]))
    print("\n  functions by site count:")
    for o, rows in (byfn if a.all else byfn[:15]):
        nm, ow = meta.get(o, ("?", "?"))
        print("     %08X  %-44s owner=%-20s %3d site(s), %d base(s)"
              % (o, nm[:44], ow, len(rows), len({r[1] for r in rows})))
    w = sum(1 for v in hits.values() for r in v if r[2] == "write")
    print("\n  %d write(s), %d read(s)" % (w, sites - w))
    print("\n  Each site is a field access a `[rip + disp]` reference map does not have. The count is")
    print("  the POPULATION of the blind spot, not a defect list: most of these are ordinary table")
    print("  walks that happen to be invisible to that one instrument.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
