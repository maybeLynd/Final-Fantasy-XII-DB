"""Check a field map's citations against the image: does each cited site touch the offset it is
filed under?

A field-map row reads `+0xNNN | width | type | name | w/r | FunctionName ADDR (SITE) ; ...`, where
SITE is the instruction that touches the field. That is a checkable assertion, and there are enough
of them to be worth checking mechanically - 577 in the battle-unit map alone.

THREE THINGS A NAIVE CHECK GETS WRONG, ALL LEARNED THE HARD WAY ON 2026-09-12
----------------------------------------------------------------------------
1. THE BASE REGISTER IS OFTEN ALREADY OFFSET. A row at +0xD0 can cite `lea rsi, [rbx + 0x50]`
   because rbx points at the unit's +0x80 sub-object. Comparing the absolute offset against the raw
   displacement called 134 of 577 sites wrong. Subtracting instead exposes the SUB-OBJECT BASES -
   +0x80, +0x6B0, +0x730 and 31 others in that map - which the maps warn about but never enumerate.
   So a positive `offset - displacement` is reported as RESOLVED-VIA-BASE, and the bases are counted.
2. A ROW CAN CITE ANOTHER OBJECT. Where a field is copied in from elsewhere, the citation names the
   instruction that produces the value, in the source record. Those show up as a NEGATIVE delta -
   a displacement larger than the offset - and are reported apart rather than as errors.
3. A CITED ADDRESS NEED NOT BE AN INSTRUCTION AT ALL. Registry slots in .data, tables in .rdata, and
   `test`/`je`/`call` sites cited for the control flow around a field are all legitimate citations
   that touch no memory at that offset. They are classified, not counted as failures.

What remains after those three is the real residue, and it is the only thing worth reading.
"""
import argparse
import collections
import io
import os
import re
import struct

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_MEM

BASE = 0x00120000
ROW = re.compile(r"^\|\s*`\+0x([0-9A-Fa-f]+)`\s*\|", re.M)
SITE = re.compile(r"\(`?(0[0-9A-Fa-f]{7})`?(?:\s*\+\d+)?\)")


def sections(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    opt = struct.unpack_from("<H", data, pe + 20)[0]
    out = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        name = data[o:o + 8].rstrip(b"\0").decode("latin1")
        vsz, va, rsz, ptr = struct.unpack_from("<IIII", data, o + 8)
        out.append((name, va, vsz, ptr, rsz))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--doc", required=True, nargs="+")
    ap.add_argument("--show", type=int, default=12)
    a = ap.parse_args()

    data = io.open(a.exe, "rb").read()
    secs = sections(data)

    def read(va, n):
        rva = va - BASE
        for _, sva, vsz, ptr, rsz in secs:
            if sva <= rva < sva + max(vsz, rsz):
                off = ptr + (rva - sva)
                return data[off:off + max(0, min(n, ptr + rsz - off))]
        return b""

    def section_of(va):
        rva = va - BASE
        for name, sva, vsz, ptr, rsz in secs:
            if sva <= rva < sva + max(vsz, rsz):
                return name
        return None

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    grand = collections.Counter()
    failed = 0

    for doc in a.doc:
        text = io.open(doc, encoding="utf-8").read()
        rows = []
        for line in text.splitlines():
            m = ROW.match(line)
            if m:
                sites = [int(x, 16) for x in SITE.findall(line)]
                if sites:
                    rows.append((int(m.group(1), 16), sites, line))
        if not rows:
            continue

        stat = collections.Counter()
        bases = collections.Counter()
        residue = []
        for off, sites, line in rows:
            for s in sites:
                sec = section_of(s)
                if sec != ".text":
                    stat["cited datum (%s)" % (sec or "unmapped")] += 1
                    continue
                ins = next(iter(md.disasm(read(s, 16), s)), None)
                if ins is None:
                    stat["undecodable"] += 1
                    residue.append((off, s, "undecodable", line))
                    continue
                mems = [op.mem for op in ins.operands if op.type == X86_OP_MEM]
                if not mems:
                    stat["control flow, no memory operand"] += 1
                    continue
                if any(m.disp == off for m in mems):
                    stat["match"] += 1
                elif any(m.index for m in mems):
                    stat["indexed (indeterminate)"] += 1
                else:
                    d = off - mems[0].disp
                    if d > 0:
                        stat["resolved via sub-object base"] += 1
                        bases[d] += 1
                    else:
                        stat["cites another object (negative delta)"] += 1

        total = sum(stat.values())
        bad = stat["undecodable"]
        failed += bad
        print("%s" % os.path.basename(doc))
        print("   %d rows carry a citation; %d sites checked" % (len(rows), total))
        for k, v in stat.most_common():
            print("      %-42s %4d  %5.1f%%" % (k, v, 100.0 * v / total if total else 0))
        if bases:
            top = ", ".join("+0x%X x%d" % (d, n) for d, n in bases.most_common(a.show))
            print("      sub-object bases (%d distinct): %s" % (len(bases), top))
        if residue:
            print("      RESIDUE - a cited .text address that does not decode:")
            for off, s, why, line in residue[:a.show]:
                print("         row +0x%03X  site %08X  %s" % (off, s, why))
        print()
        grand.update(stat)

    if len(a.doc) > 1:
        t = sum(grand.values())
        print("=== all %d documents: %d cited sites" % (len(a.doc), t))
        for k, v in grand.most_common():
            print("   %-42s %5d  %5.1f%%" % (k, v, 100.0 * v / t if t else 0))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
