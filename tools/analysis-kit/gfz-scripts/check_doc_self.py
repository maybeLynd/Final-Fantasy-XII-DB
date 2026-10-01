#!/usr/bin/env python3
"""check_doc_self.py - a document contradicting its own structure, rather than its own claims.

Why this exists
---------------
`check_self_contradiction.py` catches one shape: an absence-of-write claim refuted elsewhere in
the same file. Two other shapes have cost this program real blocks, and neither is visible to it
because neither is about an address.

  EMPTY-SECTION   A document says "section 13 is empty" while section 13 has content.
                  On 2026-09-08 the `GameSettingConfig` contract's header still read
                  "*Readiness is CONTRACT READY, not RECONSTRUCTION READY -- section 13 is
                  empty*" long after `EXP-001` had filled section 13. A block was chosen on that
                  sentence, the false premise reached a commit message, and the error was only
                  caught when the section itself was finally read. **A stale sentence outlived
                  the thing it described, and it was believed over the thing itself.**

  FRONTMATTER     The frontmatter says one readiness and the body says another. The same
                  document carried `readiness: RUNTIME VALIDATED` in its frontmatter while its
                  body asserted `CONTRACT READY`. Machine-readable metadata and human-readable
                  prose drifted apart with nothing comparing them.

Both are mechanical, and both are the kind of error that survives every existing gate: links
resolve, addresses verify, questions reconcile, and the document is still wrong about itself.

Regression-tested against the case that motivated it
----------------------------------------------------
Run against the `GameSettingConfig` contract as it stood at `HEAD~1` -- before the correction --
**both classes fire**: EMPTY-SECTION reports "§13 is empty" against a §13 holding 26 non-blank
lines, and FRONTMATTER reports `RUNTIME VALIDATED` against a body asserting `CONTRACT READY`.
Against the corpus as it stands now it reports nothing. A checker that cannot catch the error that
prompted it is decoration.

What it does NOT do
-------------------
It does not judge which side is right. A disagreement is reported as a disagreement; the fix may
be to the frontmatter, the body, or the section. It also allows two lines of slack before calling
a section non-empty, because a section holding only a pointer sentence is fairly called empty.

    python check_doc_self.py --db "Database/FFXII TZA"
    python check_doc_self.py --db "Database/FFXII TZA" --control
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

# "section 13 is empty", "§13 is empty", "§13 remains empty"
EMPTY_CLAIM = re.compile(u"(?:§|[Ss]ection\\s*)(\\d+)\\s*(?:is|remains|stays)\\s+empty")

# "## 13. Runtime validation" and "### 13a. ..." -- the SUFFIX IS PART OF THE KEY. Stripping it
# made `## 13b.`'s content count toward section 13's size, so a contract whose §13 says "EMPTY"
# and whose §13b holds a differential test was reported as contradicting itself. A lettered
# subsection is a different section.
SECTION_HEAD = re.compile(r"^#{2,3}\s*(\d+[a-z]?)\.\s", re.M)

# A section that DECLARES itself empty in its opening line is empty, however much it then says
# about what would fill it. All seven of this checker's first findings were this shape -- and
# "**None. Empty deliberately, and this is the gate the subsystem fails.**" followed by the
# cheapest confirmation to run is *good* writing, not a defect. The checker must not punish it.
DECLARES_EMPTY = re.compile(r"^\W*(\*\*)?\s*(none|empty|nothing)\b", re.I)

FM_KEY = re.compile(r"^(readiness|confidence|status):\s*([A-Za-z0-9 _-]+)", re.M)
# The backticked form is matched WHOLE. Written first as `?([A-Z][A-Z0-9 _-]{2,30}?)`?[ ,.] --
# non-greedy, so "`CONTRACT READY`" yielded "CONTRACT", which compared unequal to an identical
# frontmatter value and failed the control. A ladder rung is two words as often as one.
BODY_READY = re.compile(
    r"[Rr]eadiness is\s+(?:`([A-Z][A-Z0-9 _-]{2,30})`|([A-Z]{3,}(?:\s+[A-Z]{2,})*))")

# A sentence that reports the disagreement on purpose is a correction, not a defect.
CORRECTION = re.compile(
    r"until 2026|this line said|was stale|previously (?:said|read)|corrected|no longer says",
    re.I)


def section_sizes(text):
    """number -> count of non-blank body lines, taking the largest when a number repeats."""
    heads = [(m.group(1), m.start()) for m in SECTION_HEAD.finditer(text)]
    size = {}
    for i, (num, pos) in enumerate(heads):
        end = heads[i + 1][1] if i + 1 < len(heads) else len(text)
        chunk = text[pos:end].split(chr(10), 1)
        body = chunk[1] if len(chunk) > 1 else ""
        lines = [l for l in body.split(chr(10)) if l.strip()]
        n = 0 if (lines and DECLARES_EMPTY.match(lines[0])) else len(lines)
        size[num] = max(size.get(num, 0), n)
    return size


def empty_section_claims(text):
    """(line_no, section, body_lines, snippet)."""
    size = section_sizes(text)
    out = []
    for n, line in enumerate(text.split(chr(10)), 1):
        if CORRECTION.search(line):
            continue
        for m in EMPTY_CLAIM.finditer(line):
            num = m.group(1)
            if size.get(num, 0) > 2:
                out.append((n, num, size[num], line.strip()[:110]))
    return out


def frontmatter_vs_body(text):
    """(line_no, frontmatter_value, body_value, snippet)."""
    if not text.startswith("---"):
        return []
    end = text.find(chr(10) + "---", 3)
    if end < 0:
        return []
    fm = {}
    for m in FM_KEY.finditer(text[:end]):
        fm[m.group(1).lower()] = m.group(2).strip().rstrip("#").strip()
    have = fm.get("readiness", "")
    if not have:
        return []
    out = []
    body = text[end:]
    base = text[:end].count(chr(10)) + 1
    for m in BODY_READY.finditer(body):
        line_start = body.rfind(chr(10), 0, m.start()) + 1
        line_end = body.find(chr(10), m.start())
        line = body[line_start:line_end if line_end > 0 else len(body)]
        if CORRECTION.search(line):
            continue
        said = (m.group(1) or m.group(2) or "").strip()
        if said and said.upper() != have.upper():
            out.append((base + body[:m.start()].count(chr(10)), have, said, line.strip()[:110]))
    return out


CONTROL_EMPTY_BAD = (
    "## 13. Runtime validation" + chr(10) * 2
    + "It was run and these are the results." + chr(10)
    + "A second line of real content." + chr(10)
    + "A third." + chr(10) * 2
    + "## 14. Unresolved" + chr(10) * 2 + "Nothing." + chr(10))
CONTROL_EMPTY_OK = (
    "## 13. Runtime validation" + chr(10) * 2
    + "**Empty.**" + chr(10) * 2
    + "## 14. Unresolved" + chr(10) * 2 + "Nothing." + chr(10))
CONTROL_FM_BAD = (
    "---" + chr(10) + "readiness: RUNTIME VALIDATED" + chr(10) + "---" + chr(10) * 2
    + "> Readiness is `CONTRACT READY`, not more." + chr(10))
CONTROL_FM_OK = (
    "---" + chr(10) + "readiness: CONTRACT READY" + chr(10) + "---" + chr(10) * 2
    + "> Readiness is `CONTRACT READY`, not more." + chr(10))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--control", action="store_true")
    a = ap.parse_args()

    if a.control:
        checks = [
            ("fires on a section called empty that is not",
             len(empty_section_claims("§13 is empty." + chr(10) + CONTROL_EMPTY_BAD)) == 1),
            ("silent when the section really is empty",
             len(empty_section_claims("§13 is empty." + chr(10) + CONTROL_EMPTY_OK)) == 0),
            ("fires on frontmatter disagreeing with the body",
             len(frontmatter_vs_body(CONTROL_FM_BAD)) == 1),
            ("silent when they agree",
             len(frontmatter_vs_body(CONTROL_FM_OK)) == 0),
        ]
        bad = 0
        print("CONTROL")
        for what, ok in checks:
            print("   %s  %s" % ("ok  " if ok else "FAIL", what))
            bad += 0 if ok else 1
        if bad:
            print()
            print("   the sweep below would be untrustworthy; fix the instrument first.")
            return 1
        print()

    empties, fms = [], []
    n_docs = 0
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d != "_inbox"]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, a.db).replace(os.sep, "/")
            n_docs += 1
            text = io.open(p, encoding="utf-8", errors="replace").read()
            for hit in empty_section_claims(text):
                empties.append((rel,) + hit)
            for hit in frontmatter_vs_body(text):
                fms.append((rel,) + hit)

    print("scanned %d documents (excluding _inbox/)" % n_docs)
    print()
    if empties:
        print("EMPTY-SECTION -- the document calls a section empty and the section has content")
        for rel, n, num, size, snip in empties:
            print("   %s:%d" % (rel, n))
            print("      says section %s is empty; it has %d non-blank lines" % (num, size))
            print("      | %s" % snip)
        print()
    if fms:
        print("FRONTMATTER -- the frontmatter and the body disagree about readiness")
        for rel, n, have, said, snip in fms:
            print("   %s:%d" % (rel, n))
            print("      frontmatter says %r, the body says %r" % (have, said))
            print("      | %s" % snip)
        print()
    total = len(empties) + len(fms)
    if not total:
        print("no document contradicts its own structure")
        print("With the control passing, that is a real negative.")
        return 0
    print("%d finding(s)" % total)
    return 1


if __name__ == "__main__":
    sys.exit(main())
