"""Decode the address a row cites and compare the operand width to the declared width.

THE GAP THIS ADDRESSES, AND HOW FAR IT ACTUALLY GETS
----------------------------------------------------
`check_census_widths.py` reaches the types with an access census (seventeen as of 2026-09-13, imported not restated). `check_evidence_widths.py`
reaches any row that QUOTES its instruction. Neither reaches a row that cites only an ADDRESS -
and 692 of the 776 rows outside both were exactly that: `00235F50`, `001DE092-001DE0C4`, a site
recorded without its operand form. The evidence names the instruction; nobody decoded it.

So this decodes it. The result is honest and small: **67 rows**, all agreeing (71 when this was
written, 72 before the census map grew, 67 once the CENSUSED set below stopped being a stale copy).
It does not close the unguarded surface, and the measurements below are why - they are kept here
because the negative is the more useful half.

The window table that follows was measured in 2026-09 against the ten-type CENSUSED list. Its rows
shift by a few percent under the seventeen-type map; its CONCLUSION does not, because the signal and
the background move together. It is left as measured rather than silently re-stated.

WHY ONLY THE FIRST INSTRUCTION AT THE CITED ADDRESS
---------------------------------------------------
The obvious improvement - decode a window from the cited address, not just one instruction -
was measured against a control at a neighbouring ALIGNED displacement (off+8 and off-8, which
is what a row does NOT claim). Hits at the true offset against that background:

    window   true    +8    -8      usable?
       1       71     1     1      yes - background about 1%
       8      116    13    36      no
      40      131    22    51      no - background is a third of the signal

Past the first instruction the extra hits arrive at roughly the same rate as the control, so
widening buys noise, not coverage. A displacement is not an identity: `[rcx+0x60]` and
`[rsi+0x60]` are different structures, and only the cited SITE ties a displacement to this row.

FOUR ARTEFACT CLASSES, EACH FOUND BY A CONTROL RATHER THAN BY INSPECTION
-----------------------------------------------------------------------
* **A misaligned control proves nothing.** The first control used off+1 and found 1 hit against
  274 - which looked like proof the wide window was sound. It was not: misaligned displacements
  are rare in compiled code, so the control was confounded. An aligned control on the same data
  found a third of the hits were background. A control must differ from the claim in one respect
  only.
* **Stack frames.** `[rsp+8]` matches any row declared at +0x008. Two apparent width errors were
  register spills. RSP and RBP bases are excluded.
* **`lea` is not an access.** It computes an address and reads nothing, so its operand size is
  meaningless. The last surviving disagreement was `0032817B lea rax,[rdx+0x30]` read as an
  8-byte access to a 2-byte field.
* **Undeclared is not a claim.** Rows with size 0 - Phyre SDK imports carrying no width - were
  reported as disagreeing with every decoded width. They are skipped; they are candidates to be
  POPULATED from this evidence, not corrected by it.

    check_cited_site_widths.py [--verbose] [--control-only]
"""
import collections
import io
import os
import re
import struct
import sys

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RSP, X86_REG_RBP
except ImportError:
    raise SystemExit("capstone is required: this checker decodes the shipping image")

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")

ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")
CITE = re.compile(r"\b(?:xmmword|qword|dword|word|byte)\s*(?:ptr\s*)?\[", re.I)
SIZES = {1: 1, 2: 2, 4: 4, 8: 8, 16: 16}
# Types with an access census are already covered by check_census_widths.py -- IMPORTED from it,
# not restated. This list was hardcoded with ten names and went stale: by 2026-09-13 the census map
# held seventeen, so this checker treated 378 declared rows across seven types (SpawnRecord,
# CharacterRenderRecord, CharacterRenderObject, CharacterRenderSystemTail, GameSettingConfig,
# BattleFormulaScratch, EvaluationContext) as uncensused, inflating its own "no census" figures and
# duplicating the stronger instrument's work. Two checkers maintaining two copies of one fact is a
# conflict waiting for someone to quote the wrong one -- and someone did, in EVIDENCE-STANDARD
# amendment 13h, on the same day. One source now.
def _censused():
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "_cw", os.path.join(here, "check_census_widths.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(mod.CENSUS) | set(mod.STATIC_CENSUS)


CENSUSED = _censused()


def _exemption():
    """The WIDTH DELIBERATE predicate, IMPORTED rather than copied - same reason as _censused."""
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "_cw2", os.path.join(here, "check_census_widths.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.reason_after


reason_after = _exemption()


class Image(object):
    def __init__(self, path):
        d = open(path, "rb").read()
        self.d = d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        optsz = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
        self.secs = [struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8)
                     for i in range(nsec)]

    def read(self, va, n):
        rva = va - self.base
        for vsz, sva, rsz, ro in self.secs:
            if sva <= rva < sva + max(vsz, rsz):
                return self.d[ro + rva - sva: ro + rva - sva + n]
        return b""


def num(s):
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s)
    except ValueError:
        return None


def candidate_rows(fields_path):
    """Declared rows that cite an address, quote no instruction, and have no census."""
    out = []
    for n, line in enumerate(io.open(fields_path, encoding="utf-8")):
        if not n or not line.strip():
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 9 or c[0] == "type" or c[0] in CENSUSED:
            continue
        off, size = num(c[1]), num(c[2])
        # size 0 is UNDECLARED, not a claim; spans and arrays are not element-width comparable
        if off is None or not size or size > 16 or c[4].strip().endswith("]"):
            continue
        if CITE.search(c[8]):
            continue
        addrs = [int(a, 16) for a in ADDR.findall(c[8])][:6]
        if addrs:
            out.append((c[0], off, size, c[3], addrs, c[8]))
    return out


def widths_at(img, md, addrs, disp):
    """Operand widths of the FIRST instruction at each cited address touching `disp`."""
    found = set()
    for a in addrs:
        buf = img.read(a, 16)
        if not buf:
            continue
        for ins in md.disasm(buf, a):
            # a NOP pads with a memory operand and touches nothing; lea computes an
            # address and reads nothing at all
            if ins.mnemonic.startswith("nop") or ins.mnemonic == "lea":
                break
            for op in ins.operands:
                if (op.type == X86_OP_MEM and op.mem.disp == disp and op.mem.base != 0
                        and op.mem.base not in (X86_REG_RSP, X86_REG_RBP)):
                    w = SIZES.get(op.size)
                    if w:
                        found.add(w)
            break
    return found


def main():
    verbose = "--verbose" in sys.argv
    if not os.path.exists(EXE):
        raise SystemExit("shipping image not found: %s" % EXE)
    img = Image(EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    rows = candidate_rows(FIELDS)

    hit = agree = 0
    bad, stated, nohit = [], [], 0
    for tname, off, size, name, addrs, ev in rows:
        w = widths_at(img, md, addrs, off)
        if not w:
            nohit += 1
            continue
        hit += 1
        if size in w:
            agree += 1
        elif reason_after(ev):
            # THE SAME EXEMPTION THE OTHER TWO INSTRUMENTS GRANT, and it was missing here.
            # Added 2026-09-20 (OPUS): both rows this check reported were already dispositioned
            # in prose - Category +0x78 says in so many words that the 8-byte store is "the
            # compiler merging two adjacent zeroes", and NameBindingEntry +0x30 is one of three
            # ids the allocator seeds with a -1 qword across the first two. A kit that grants an
            # exemption in two instruments and not the third reports a settled question as open.
            stated.append((tname, off, size, name, sorted(w)))
        else:
            bad.append((tname, off, size, name, sorted(w)))

    # The control is not optional. A result without it cannot be told from background.
    ctrl = 0
    for tname, off, size, name, addrs, _ev in rows:
        for delta in (8, -8):
            if off + delta >= 0 and widths_at(img, md, addrs, off + delta):
                ctrl += 1
                break

    print("ROWS WHOSE DECLARED WIDTH DISAGREES WITH THEIR CITED SITE: %d" % len(bad))
    for tname, off, size, name, w in bad:
        print("  MISMATCH %-26s +0x%04X declared %-3d %-24s decoded %s"
              % (tname, off, size, name[:24], w))
    print()
    print("COVERAGE AND CONTROL -- one cited instruction, decoded; weaker than a census")
    print("  rows citing an address but quoting no instruction, no census: %d" % len(rows))
    print("    cited site decodes to an access at the row's own offset:    %d" % hit)
    print("      stated exception (WIDTH DELIBERATE with a reason):         %d" % len(stated))
    for tname, off, size, name, w in stated:
        print("        exempt %-24s +0x%04X declared %-3d decoded %s"
              % (tname[:24], off, size, w))
    print("      agreed:                                                  %d" % agree)
    print("      DISAGREED:                                               %d" % len(bad))
    print("    no such access at any cited address:                       %d" % nohit)
    print("  CONTROL, same probe at a neighbouring aligned displacement:  %d" % ctrl)
    if hit and ctrl * 4 > hit:
        print("  CONTROL IS TOO CLOSE TO THE SIGNAL - treat these results as background.")
        return 2
    if not hit:
        print("NO COMPARISON WAS PERFORMED. This result proves nothing about any width.")
        return 2
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
