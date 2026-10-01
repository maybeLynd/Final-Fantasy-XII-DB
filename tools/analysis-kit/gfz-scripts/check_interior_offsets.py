"""A declared row whose INTERIOR the image addresses on its own is not one field.

THE DEFECT CLASS, found twice in one day in one type and then generalised here. Widget +0x98
was declared uint32 because the shared initialiser stores a dword there; handlers address +0x9A
on its own, twenty-two times, so +0x98 cannot be four bytes. Widget +0xA1 was declared uint16
because the initialiser stores `mov word ptr [rdi+0xa1], 0xff80`; the destructor writes +0xA2 as
a byte, so +0xA1 cannot be two. Both had stood for months with a correct citation, because the
citation was a COMBINED WRITE - one instruction setting two adjacent fields, which is ordinary
and legal and says nothing about where the boundary is.

Neither was found by reading. The first needed a census wide enough to hold both accesses; the
second fell out of `check_census_widths` the moment one existed. THE GENERAL TEST IS CHEAPER
THAN EITHER: for every declared row, ask whether the census contains an access STRICTLY INSIDE
it. If it does, the row spans a boundary the image itself uses.

WHY THIS IS NOT check_census_widths. That gate compares a row's DECLARED WIDTH against the
widths of accesses AT ITS OWN OFFSET, so a row is clean when every access at its start matches
its size - and +0x98 was clean by that test for exactly as long as nothing looked at +0x9A.
This one looks between the rows. The two are complementary and neither subsumes the other.

WHAT COUNTS AS AN INTERIOR ACCESS, and the exclusions matter more than the rule:

  * ARRAYS AND SPANS ARE SKIPPED. A row declared `u8[48]` or a span is MEANT to be addressed
    inside; reporting it would bury the real findings under the expected ones. Detected from
    the declared ctype and from size against the element width, not guessed.
  * INDEXED ACCESSES ARE SKIPPED - `[rcx + rax*8]` is an element reached through the base and
    is filed at the base displacement, which is an artefact of every census in this kit.
  * MULTI-BYTE NOPS ARE SKIPPED - `nop dword ptr [rax+rax]` carries a memory operand and
    touches nothing.
  * SIMD BLOCK COPIES ARE SKIPPED for the same reason check_census_widths skips them: an
    unrolled `movups xmmword` run is a region move, not a field.

A finding is therefore: a scalar row, of a type with a census, with an access at an offset
strictly between its start and its end.

AND A FINDING IS A LEAD, NOT A DEFECT. Some rows are legitimately one field whose parts the
image reads separately, and the first run made that obvious: TextDrawState +0x30 `textColor` is
a packed colour and +0x31/+0x32/+0x33 are its channels, which is one field read per channel
rather than four fields. Others are the real thing - GameSettingConfig `Resolution` is declared
int32 and +0x06 is ITSELF ADDRESSED five times, every one a signed word, which cannot happen
if +0x04 is one 4-byte field - and the two halves are multiplied together. (Not "nothing
wider touches those bytes": the dword reads at +0x04 of course cover +0x06. The argument
is about what is addressed, not about what is covered.) The test cannot tell those apart and does not try;
it says WHERE TO LOOK, and the difference is decided by reading the instructions. A tool that
called all nineteen defects would be wrong about several of them.

THE CONTROL IS THE TWO KNOWN CASES. Run against a store where Widget +0x98 is still uint32 and
+0xA1 still uint16, this must report both. It cannot be run that way now that both are split,
so the control is inverted and checked on every run instead: THOSE TWO ROWS MUST NOT APPEAR, and
their neighbours +0x9A, +0x9E and +0xA2 must exist as rows. A tool that cannot see the defect it
was built from is not measuring anything, and one that still reports a fixed defect is worse.

AND A LEAD THAT HAS BEEN RULED ON STOPS BEING REPORTED AS OPEN. After a day of adjudicating,
every row still in this gate's output had already been decided - so the open count could never
reach zero and a NEW lead would have arrived invisible among six settled ones. That is the
failure this kit's own sibling names: "a gate whose output is routinely non-empty gets ignored
unless it says why". A row counts as ADJUDICATED when its evidence carries one of the markers
in ADJUDICATED **with real prose after it** - the same earned-exemption rule check_census_widths
puts on WIDTH DELIBERATE, so a row cannot silence the gate by mentioning the phrase. The settled
rows are printed with their verdicts and written into the leads file under a `status` column,
because an empty table and a table of settled questions look identical to whoever opens it.

    check_interior_offsets.py [--db DB] [--all]

Exit 0 when nothing is found, 1 when a row is contradicted.
"""
import argparse
import collections
import glob
import io
import os
import re
import sys

NOP = re.compile(r"^\s*nop\b", re.I)
INDEXED = re.compile(r"\[\s*\w+\s*\+\s*\w+\s*\*\s*[1248]\s*\]")
FORMS = (("xmmword", 16), ("qword ptr", 8), ("dword ptr", 4), ("word ptr", 2), ("byte ptr", 1))
ARRAYISH = re.compile(r"\[\s*\d*\s*\]|^u8$|^uint8$", re.I)

# A LEAD THAT HAS BEEN RULED ON MUST STOP BEING REPORTED AS OPEN, or this gate joins the
# gates nobody reads. Its own sibling says it best - "a gate whose output is routinely
# non-empty gets ignored unless it says why" - and after a day of adjudicating leads, every
# single row still in the output had already been decided. The count could never reach zero,
# so a NEW lead would have arrived invisible among six settled ones.
#
# A row is ADJUDICATED when its evidence carries one of these markers AND real prose after it.
# The prose requirement is the same one check_census_widths puts on WIDTH DELIBERATE, and for
# the same reason: the exemption is earned by the REASON, not by the phrase, or a row could
# silence the gate by mentioning it.
ADJUDICATED = (
    "INTERIOR-OFFSET LEAD RULED FALSE",   # the access is a compiler narrowing, or one field
                                          # whose parts the image touches separately
    "PER-PATH UNION",                     # both readings are real and the path selects
)
ADJUDICATED_MIN = 80


def adjudication(evidence):
    """The marker this row was settled under, or None - prose after it, not just the phrase."""
    for m in ADJUDICATED:
        i = evidence.find(m)
        while i != -1:
            if len(evidence) - (i + len(m)) >= ADJUDICATED_MIN:
                return m
            i = evidence.find(m, i + 1)
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA")
# The two rows this tool was built from. Both are split now, so the control is that they are
# ABSENT from the findings and that the fields they were split into exist.
CONTROL_ABSENT = (("Widget", 0x98), ("Widget", 0xA1))
CONTROL_PRESENT = (("Widget", 0x9A), ("Widget", 0x9E), ("Widget", 0xA2))


BITOP = re.compile(r"^\s*(test|and|or|xor|bt|bts|btr|btc)\b", re.I)


def shape_of(inside):
    """How many of the interior accesses are MASKS, and how many move or compute a VALUE.

    Two confirmed classifications on the first run put the leads into two kinds, and the same
    discriminator settled both:

      A MASK OR TEST with an immediate is what a COMPILER NARROWING looks like. `and dword
      [rdi+4], 0xffefffbb` on a 64-bit flags word touches only high bits, so the compiler emits
      a 32-bit mask at +4; `test byte [rbx], 4` narrows the other way. BattleUnit +0x00 is
      entirely this and is NOT two fields.

      A MOVE OR ARITHMETIC is what a real boundary looks like. GameSettingConfig +0x06 is read
      `movsx word` and multiplied; BattleStatsRecord +0x0A is accumulated and clamped. Both
      were real.

    The label is the COUNT, not a verdict - `bit b3`, `val v2`, `mix v3/b38` - because a verdict
    would be wrong about at least one row either way: TextDrawState's packed colour is read per
    channel with `movzx`, which counts as a value access, and it is still one field. The counts
    say how hard to look, and reading decides.
    """
    bits = vals = 0
    for _, lst in inside:
        for _, _, instr in lst:
            if BITOP.match(instr):
                bits += 1
            else:
                vals += 1
    total = bits + vals
    if vals == 0:
        return "bit b%d" % bits
    if bits == 0:
        return "val v%d" % vals
    return "mix v%d/b%d" % (vals, bits)


def width(instruction):
    for token, w in FORMS:
        if token in instruction:
            return w
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--all", action="store_true", help="list every finding, not the first 40")
    a = ap.parse_args()

    # the census map lives in check_census_widths; read it rather than keep a second copy
    cw = os.path.join(HERE, "check_census_widths.py")
    src = io.open(cw, encoding="utf-8").read()
    body = src[src.index("CENSUS = {"):]
    body = body[:body.index("\n}") + 2]
    census_map = {}
    for m in re.finditer(r'"([A-Za-z0-9_]+)"\s*:\s*"([^"]+\.tsv)"', body):
        census_map[m.group(1)] = m.group(2)
    files = {os.path.basename(p): p
             for p in glob.glob(os.path.join(a.db, "**", "*-accesses.tsv"), recursive=True)}

    rows = collections.defaultdict(list)
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) < 5:
                continue
            try:
                off, size = int(c[1], 16), int(c[2])
            except ValueError:
                continue
            rows[c[0]].append((off, size, c[3], c[4], c[8] if len(c) > 8 else ""))

    findings, checked, skipped_arrays = [], 0, 0
    adjudicated = []
    for tname, fname in sorted(census_map.items()):
        path = files.get(fname)
        if not path or tname not in rows:
            continue
        acc = []
        with io.open(path, encoding="utf-8") as fh:
            head = next(fh).rstrip("\n").split("\t")
            try:
                di, ii, si = head.index("disp"), head.index("instruction"), head.index("site")
            except ValueError:
                continue
            for ln in fh:
                c = ln.rstrip("\n").split("\t")
                if len(c) <= max(di, ii, si):
                    continue
                instr = c[ii]
                if NOP.match(instr) or INDEXED.search(instr):
                    continue
                w = width(instr)
                if w is None or w == 16:
                    continue
                try:
                    acc.append((int(c[di], 16), w, c[si], instr))
                except ValueError:
                    pass
        if not acc:
            continue
        by_disp = collections.defaultdict(list)
        for d, w, site, instr in acc:
            by_disp[d].append((w, site, instr))
        for off, size, name, ctype, evid in rows[tname]:
            if size <= 1:
                continue
            if ARRAYISH.search(ctype or "") or size not in (2, 4, 8):
                skipped_arrays += 1
                continue
            checked += 1
            inside = [(d, by_disp[d]) for d in by_disp if off < d < off + size]
            if inside:
                verdict = adjudication(evid)
                if verdict:
                    adjudicated.append((tname, off, name, verdict))
                    continue
                findings.append((tname, off, size, name, ctype, sorted(inside),
                                 shape_of(inside)))

    print("INTERIOR-OFFSET CHECK  a scalar row the image addresses inside is not one field")
    print("  types with a census and declared rows : %d" % len(
        [t for t in census_map if t in rows]))
    print("  scalar rows checked                   : %d" % checked)
    print("  array/span rows skipped by design     : %d" % skipped_arrays)
    print("  ADJUDICATED, ruled and recorded on the row: %d" % len(adjudicated))
    for tn, off, nm, verdict in adjudicated:
        print("      %-26s +0x%04X %-22s %s" % (tn, off, nm, verdict))
    nb = len([f for f in findings if f[6].startswith("bit")])
    nv = len([f for f in findings if f[6].startswith("val")])
    print("  ROWS WITH AN INTERIOR ACCESS                     : %d" % len(findings))
    print("    all interior accesses are masks or tests       : %d  (usually a compiler"
          " narrowing on a flags field - read, but expect no)" % nb)
    print("    all interior accesses move or compute a value  : %d  (read closely)" % nv)
    print("    mixed                                          : %d"
          % (len(findings) - nb - nv))
    print()
    for tname, off, size, name, ctype, inside, shape in (findings if a.all else findings[:40]):
        print("  [%-7s] %-26s +0x%04X %-4s %-22s %s"
              % (shape, tname, off, size, name, ctype))
        for d, lst in inside:
            for w, site, instr in lst[:3]:
                print("        interior +0x%04X width %d   %s  %s" % (d, w, site, instr))
    if not a.all and len(findings) > 40:
        print("  ... %d more, use --all" % (len(findings) - 40))

    out_path = os.path.join(a.db, "_index", "candidates", "interior-offset-leads.tsv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        # The ADJUDICATED rows are written here too, and deliberately. An empty table and a
        # table of settled questions look identical to whoever opens the file, and this store
        # published a header-only leads table by accident once already today. A file that says
        # "six, all decided, and here is what each was decided as" cannot be misread as
        # "nothing was measured".
        fh.write("status\ttype\toffset\tsize\tname\tctype\tshape\tinterior\twidths\tsites\n")
        for tn, off, nm, verdict in adjudicated:
            fh.write("adjudicated\t%s\t0x%X\t\t%s\t\t%s\t\t\t\n" % (tn, off, nm, verdict))
        for tname, off, size, name, ctype, inside, shape in findings:
            ints = ",".join("0x%X" % d for d, _ in inside)
            ws = ",".join(str(w) for _, lst in inside for w, _, _ in lst)
            sites = " ".join(site for _, lst in inside for _, site, _ in lst)
            fh.write("open\t%s\t0x%X\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n"
                     % (tname, off, size, name, ctype, shape, ints, ws, sites))
    print("  leads written to %s" % os.path.relpath(out_path, a.db))

    print()
    print("CONTROL  the two rows this tool was built from are split, so they must be ABSENT")
    ok = True
    have = {(t, o) for t, o, _, _, _, _, _ in findings}
    for t, o in CONTROL_ABSENT:
        bad = (t, o) in have
        if bad:
            ok = False
        print("    %s +0x%02X  %s" % (t, o, "STILL REPORTED - it was not split" if bad else "absent, as it must be"))
    declared = {(t, o) for t in rows for o, _, _, _, _ in rows[t]}
    for t, o in CONTROL_PRESENT:
        miss = (t, o) not in declared
        if miss:
            ok = False
        print("    %s +0x%02X  %s" % (t, o, "MISSING - the split was reverted" if miss else "declared, as it must be"))
    if not ok:
        print("  The control failed; the findings above cannot be trusted.")
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
