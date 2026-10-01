"""Check each declared width against the instruction the row itself cites.

WHY THIS EXISTS, AND WHY IT IS NOT ANOTHER CENSUS CHECKER
---------------------------------------------------------
`check_census_widths.py` compares a declared width against an access census. That is strong
evidence and it reaches ten types. After it was repaired to print its own denominator it
reported the problem plainly: 699 of 1585 rows checked, and **858 rows in 212 types outside
its reach entirely**, because those types have no census. No width in them had ever been
compared against anything.

But an instruction carries its operand width, and most rows already QUOTE the instruction
that establishes them - `002667D3 mov word [rbx+0x16],ax`, `00300D69 movsx ebx, word ptr
[rsi+0x4c]`. The check was sitting in the evidence column unread. A census covers a type;
a citation covers a row, which is a narrower unit and a much wider axis.

THE DISCRIMINATOR THAT MAKES IT SOUND
-------------------------------------
An evidence cell routinely mentions several fields - neighbours, the constructor's other
stores, a peer type. Matching any instruction in the text would compare a row against
somebody else's operand. So a citation counts ONLY when its displacement equals the row's
own offset. `+0x16` in a row at +0x016 is evidence about that row; `+0x4C` in the same cell
is not. A bare `[reg]` with no displacement does NOT count as a citation about offset 0 -
its base is whatever the register happens to hold, which the text does not settle; those are
counted in their own bucket and can neither agree nor contradict.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not treat silence as agreement - the lesson ASTRA's fixtures taught this checker's
sibling. Rows with no parseable citation at their own displacement are COUNTED and reported,
never passed. Arrays and whole spans are skipped by the same rule the census checker uses,
since an element width is expected to differ from a declared extent, and a row carrying
`WIDTH DELIBERATE` states its own exception and is listed rather than failed.

It is also weaker evidence than a census by construction, and says so: a census counts every
access at a displacement, while a citation is one instruction a human chose to quote. It can
confirm and it can contradict; it cannot establish a dominant form.

    check_evidence_widths.py [--verbose] [--self-test]
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")

WIDTHS = (("xmmword", 16), ("qword", 8), ("dword", 4), ("byte", 1), ("word", 2))
# "mov word ptr [rbx + 0x16], ax" / "movsx ebx, word ptr [rsi+0x4c]" / "cmp byte [rcx+5], 1"
CITE = re.compile(
    r"\b(?P<w>xmmword|qword|dword|word|byte)\s*(?:ptr\s*)?"
    r"\[\s*[a-z0-9]{2,4}\s*(?:\+\s*[a-z0-9]{2,4}\s*\*\s*[1248]\s*)?"
    r"(?:\+\s*(?P<disp>0x[0-9a-f]+|\d+)\s*)?\]", re.I)
NOPCITE = re.compile(r"\bnop\b[^.;]{0,40}$", re.I)


def width_token(tok):
    for name, w in WIDTHS:
        if tok.lower() == name:
            return w
    return None


def citations_at(evidence, offset):
    """(widths, unresolved_base) for THIS row's displacement. A citation about a neighbour is
    evidence about the neighbour.

    A BARE `[reg]` IS NOT A CITATION ABOUT OFFSET 0. It was, and that was wrong: the parser
    read `mov edx, dword ptr [rbx]` out of WorldLootDropEntry's evidence and called it a
    4-byte itemId at +0, when the same evidence says in words that rbx sits on the entry's
    SECOND member. A bare dereference addresses whatever the register holds, which the text
    alone does not settle - the same 'resolve the target, never assume it' rule that a
    pointer-versus-object mistake taught check_instance_aliases. Such citations are counted
    separately and can neither agree nor contradict."""
    found, unresolved = [], 0
    for m in CITE.finditer(evidence):
        d = m.group("disp")
        if d is None:
            if offset == 0:
                unresolved += 1
            continue
        disp = int(d, 16) if d.lower().startswith("0x") else int(d)
        if disp != offset:
            continue
        # a multi-byte NOP pads with a memory operand and touches nothing
        head = evidence[max(0, m.start() - 42):m.start()]
        if re.search(r"\bnop\b\s*$", head, re.I):
            continue
        w = width_token(m.group("w"))
        if w:
            found.append(w)
    return found, unresolved


def num(s):
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s)
    except ValueError:
        return None


def _shared():
    """The exemption predicate, IMPORTED from check_census_widths rather than copied.

    Both instruments grant the same WIDTH DELIBERATE exemption. On 2026-09-13 only one of them was
    hardened to require a reason after the marker, which would have left a row able to take the
    exemption here on a bare mention and not there. A second copy of one rule is the defect this
    kit had already found twice that day."""
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "_cw", os.path.join(here, "check_census_widths.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MARKER, mod.reason_after


MARKER, reason_after = _shared()

EMIT_CHECKED = []   # (type, offset) actually compared -- for the union-coverage measurement


def run(fields_path, verbose=False):
    checked = agreed = 0
    disagree, stated, spans, no_reason = [], [], [], []
    uncited = collections.Counter()
    barebase = collections.Counter()
    total = 0
    for n, line in enumerate(io.open(fields_path, encoding="utf-8")):
        if not n or not line.strip():
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 9 or c[0] == "type":
            continue
        off, size = num(c[1]), num(c[2])
        if off is None or size is None:
            continue
        total += 1
        tname, name, ctype, ev = c[0], c[3], c[4], c[8]
        if size > 16 or ctype.strip().endswith("]"):
            spans.append((tname, off, size, name))
            continue
        cites, unresolved = citations_at(ev, off)
        if not cites:
            if unresolved:
                barebase[tname] += 1
            else:
                uncited[tname] += 1
            continue
        checked += 1
        EMIT_CHECKED.append((tname, off))
        if size in cites:
            agreed += 1
            continue
        if MARKER in ev:
            # The same predicate check_census_widths uses, IMPORTED rather than copied. Both
            # instruments grant the same exemption, and on 2026-09-13 only one of them was
            # hardened to require a reason after the marker -- which would have left the store
            # able to take the exemption here on a bare mention and not there. A second copy of
            # one rule is the defect this kit had already found twice that day.
            if reason_after(ev):
                stated.append((tname, off, size, name, sorted(set(cites))))
            else:
                no_reason.append((tname, off, size, name))
            continue
        disagree.append((tname, off, size, name, sorted(set(cites))))

    if verbose or disagree:
        print("ROWS WHOSE DECLARED WIDTH CONTRADICTS THEIR OWN CITED INSTRUCTION: %d" % len(disagree))
        for tname, off, size, name, cites in disagree:
            print("  MISMATCH %-24s +0x%04X declared %-3d %-26s cited %s"
                  % (tname, off, size, name[:26], cites))
    if verbose and stated:
        print()
        print("declared against their citation with a stated reason: %d" % len(stated))
        for tname, off, size, name, cites in stated:
            print("  stated   %-24s +0x%04X declared %-3d %-26s cited %s"
                  % (tname, off, size, name[:26], cites))

    print()
    print("COVERAGE -- a citation is one quoted instruction, not a census, and proves less")
    print("  declared rows read:                                  %d" % total)
    print("  arrays and whole spans, width not comparable:         %d" % len(spans))
    print("  CHECKED against their own cited instruction:          %d" % checked)
    print("    agreed:                                            %d" % agreed)
    print("    stated exception:                                  %d" % len(stated))
    if no_reason:
        print("    DEFECT -- marker with no reason after it:           %d" % len(no_reason))
        for tname, off, size, name in no_reason:
            print("        %-22s +0x%04X declared %-4s %s" % (tname, off, size, name[:24]))
    print("    CONTRADICTED:                                      %d" % len(disagree))
    print("  no instruction cited at the row's own displacement:   %d in %d types"
          % (sum(uncited.values()), len(uncited)))
    print("  cited only through a bare [reg], base unresolved:      %d in %d types"
          % (sum(barebase.values()), len(barebase)))
    if verbose:
        for tname, k in uncited.most_common(14):
            print("      %-30s %d" % (tname, k))
    if not checked:
        print("NO COMPARISON WAS PERFORMED. This result proves nothing about any width.")
    return len(disagree), checked


FIXTURES = [
    # (size, offset, ctype, evidence, expect_checked, expect_bad)
    ("agrees", "4", "0x010", "uint32", "00100000 mov eax, dword ptr [rcx + 0x10]", 1, 0),
    ("contradicts", "1", "0x010", "uint8", "00100000 mov eax, dword ptr [rcx + 0x10]", 1, 1),
    ("neighbour only", "4", "0x010", "uint32", "00100000 mov al, byte ptr [rcx + 0x4c]", 0, 0),
    ("bare reg is not offset 0", "8", "0x000", "void*", "00100000 mov rax, qword ptr [rcx]", 0, 0),
    ("bare reg cannot contradict", "2", "0x000", "uint16",
     "0031995A mov edx, dword ptr [rbx]", 0, 0),
    ("nop is not an access", "1", "0x010", "uint8", "00100000 nop dword ptr [rax + 0x10]", 0, 0),
    ("span skipped", "56", "0x020", "uint8[56]", "00100000 mov al, byte ptr [rcx + 0x20]", 0, 0),
    ("no citation", "4", "0x010", "uint32", "written at 00100000 by the initialiser", 0, 0),
]


def self_test():
    import tempfile
    ok = True
    for label, size, off, ctype, ev, want_checked, want_bad in FIXTURES:
        fd, path = tempfile.mkstemp(suffix=".tsv")
        os.close(fd)
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write("type\toffset\tsize\tname\tctype\tmeaning\treadiness\tconfidence\tevidence\n")
            fh.write("\t".join(["T", off, size, "f", ctype, "", "", "", ev]) + "\n")
        sys.stdout = open(os.devnull, "w")
        try:
            bad, checked = run(path, verbose=False)
        finally:
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        os.unlink(path)
        good = (checked, bad) == (want_checked, want_bad)
        ok &= good
        print("  %-24s checked=%d bad=%d  expected (%d,%d)  %s"
              % (label, checked, bad, want_checked, want_bad, "ok" if good else "FAILED"))
    print()
    print("fixtures: %s" % ("all behave correctly" if ok else "A FIXTURE FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    bad, checked = run(FIELDS, verbose="--verbose" in sys.argv)
    raise SystemExit(1 if bad else (0 if checked else 2))
