#!/usr/bin/env python3
"""gen_form_note.py - emit a PROVED BY FORM note whose every figure is measured from the image.

Why this exists
---------------
The catalogue page was built by in-session tooling that is not in the tree, and six of its 55
notes carry figures that do not reproduce (OPUS-REQ-SWE2-EC7-FORM-NOTE-FIGURES-SIX-ROWS):

  * two size histograms were capped at two groups - `most_common(2)` instead of the whole
    Counter - so they listed 9 of 13 and 9 of 12 members;
  * four byte-image counts were recorded RAW, while the other 51 rows use the wildcard
    normalisation;
  * `StaticPointerBitfieldGetter` said 6 byte images - measured 12, and 9 over the nine members
    its own truncated histogram lists. Six is the multiplicity of the largest size bucket
    (17 B x6), consistent with the figure having been taken from the first histogram group
    rather than from the image set.

This is the committed emitter so the note's every figure is redoable by anyone.

Conventions (identical to work/OPUS/verify_form_families.py, which measures the same bodies)
------------------------------------------------------------------------------------------
  * byte image  - the body with RIP-relative memory-operand displacements and direct
                  call/jmp rel32 displacements wildcarded to 0x3F. Constants (field offsets,
                  masks, immediates) are NOT wildcarded - they are what members vary.
  * form        - mnemonic + operand text with every numeric constant replaced by '#'.
  * targets     - direct call/jmp destinations OUTSIDE the member's own span.
  * shared      - targets reached by EVERY member; member-specific = total - shared
                  (NOT "reached by exactly one member" - the corpus's own rows settle that).
  * histogram   - EVERY size group, `Counter.most_common()` order. A histogram that does not
                  sum to the member count is the defect this tool exists to prevent.

Usage
-----
    python gen_form_note.py members/<file>.tsv            print the note clause
    python gen_form_note.py --all                       every PROVED BY FORM row, recomputed
    python gen_form_note.py --sync <name> [<name>...]   rewrite those rows' figures in place
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit",
                                "gfz-scripts"))
import check_dispositions as CD          # noqa: E402

PAGE = os.path.join(HERE, "..", "generated-function-families.md")
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
IMAGE = 0x120000

import capstone                          # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP   # noqa: E402

_HEX = re.compile(r"0x[0-9a-f]+|\b\d+\b")


def load_image(path):
    d = io.open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    secs, o = [], pe + 24 + optsz
    for _ in range(nsec):
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, vsz, rsz, rptr))
        o += 40

    def off(va):
        r = va - IMAGE
        for sva, vsz, rsz, rptr in secs:
            if sva <= r < sva + max(vsz, rsz):
                return rptr + (r - sva)
    return d, off


def image(md, body):
    """The body with ONLY the RIP-relative and call/jmp displacement fields wildcarded."""
    va, b = 0, bytearray(body)
    return bytes(b)


def measure(md, d, off, sizes, members):
    """(size histogram, byte images, forms, targets, shared) for a member list."""
    szs = collections.Counter()
    imgs, forms, tl = set(), set(), []
    for va in members:
        n, o = sizes.get(va, 0), off(va)
        b = d[o:o + n] if n and o is not None else b""
        szs[n] += 1
        img = bytearray(b)
        ts = []
        f = []
        for ins in md.disasm(bytes(b), va):
            ioff = ins.address - va
            if (ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x")
                    and ins.size >= 5):
                t = int(ins.op_str, 16)
                if not (va <= t < va + n):
                    ts.append(t)
                for i in range(ioff + ins.size - 4, ioff + ins.size):
                    img[i] = 0x3F
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    has_imm = any(o2.type == X86_OP_IMM for o2 in ins.operands)
                    end = ioff + ins.size - (ins.imm_size if has_imm else 0)
                    for i in range(end - 4, end):
                        if 0 <= i < len(img):
                            img[i] = 0x3F
            f.append("%s %s" % (ins.mnemonic, _HEX.sub("#", ins.op_str)))
        imgs.add(bytes(img))
        forms.add(";".join(f))
        tl.append(ts)
    tc = collections.Counter(t for ts in tl for t in ts)
    shared = sum(1 for a in tc if all(a in ts for ts in tl))
    return szs, len(imgs), len(forms), len(tc), shared


def note(n, szs, imgs, forms, targets, shared):
    """The note clause. Histogram lists EVERY size group and sums to the member count."""
    assert sum(szs.values()) == n, "histogram must sum to the member count"
    hist = ", ".join("%d B x%d" % (s, c) for s, c in szs.most_common())
    out = ("PROVED BY FORM - %d members, %s, %d byte image(s) collapsing to ONE instruction "
           "form. CONTROL: %d external target(s): %d shared across all %d members"
           % (n, hist, imgs, targets, shared, n))
    if targets - shared:
        out += ", and %d that are member-specific" % (targets - shared)
    return out + "."


def row_name(p):
    return p[0].strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", nargs="?", help="a members TSV to measure")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--sync", nargs="*", metavar="FAMILY",
                    help="rewrite the named rows' measured figures in the catalogue page")
    a = ap.parse_args(argv)

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    d, off = load_image(EXE)
    sizes = CD.load_functions(None)

    if a.tsv:
        mem = CD.read_members(PAGE, a.tsv)
        szs, imgs, forms, t, shared = measure(md, d, off, sizes, mem)
        print(note(len(mem), szs, imgs, forms, t, shared))
        if forms != 1:
            print("WARNING: %d distinct instruction forms" % forms, file=sys.stderr)
        return 0

    if a.all or a.sync is not None:
        text = io.open(PAGE, encoding="utf-8").read()
        want = set(a.sync or [])
        changed = 0
        for doc, p in CD.parse_families(os.path.dirname(os.path.abspath(PAGE))):
            if len(p) < 5 or "PROVED BY FORM" not in p[4]:
                continue
            name = row_name(p)
            if a.sync is not None and name not in want:
                continue
            mem = CD.read_members(doc, p[2])
            szs, imgs, forms, t, shared = measure(md, d, off, sizes, mem)
            new = note(len(mem), szs, imgs, forms, t, shared)
            print("%-56s %s" % (name, new))
            if a.sync is not None:
                m = re.search(re.escape(p[4]), text)
                if not m:
                    print("  !! row text not found in page", file=sys.stderr)
                    continue
                clause = re.sub(
                    r"PROVED BY FORM - .*?NOT dispositioned:",
                    new + " NOT dispositioned:",
                    p[4], count=1, flags=re.S)
                if clause != p[4]:
                    text = text.replace(p[4], clause, 1)
                    changed += 1
        if a.sync is not None:
            io.open(PAGE, "w", encoding="utf-8", newline="\n").write(text)
            print("rewrote %d row(s) in %s" % (changed, PAGE))
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
