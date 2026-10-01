"""gen_delta_staleness.py - the one way a parent advance can have made a document wrong.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/delta_staleness.py`, which
`.gitignore` excludes. `_index/candidates/snapshot-delta-reliance-20.tsv` names it in its
header as the converse measurement - *"the converse slice was measured separately and did
find work: delta_staleness.py looked for ..."* - so a reader asked to compare two slices
could reproduce one of them.

THE BODY BELOW IS THE ORIGINAL, UNCHANGED, for the reason the other published generators
give: the tool in the kit must be the tool that produced the figure beside it. The only
addition resolves the repository root from `__file__` so its repo-relative paths work from
any working directory.

**ITS FIGURES ARE GN158 -> GN160 AND SAY SO.** The certified parent is GN161; the span this
measures is two advances back, and its own prose names the span in every sentence. Read it
as the measurement it was, not as a statement about the current parent -
`check_delta_additivity.py` is the instrument for that and covers every span.

NAMED `gen_*`, NOT `check_*`: `run_gates.py` globs `check_*.py`.
"""
import os as _os

# The repository root, four levels above this file.
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# delta_staleness.py - the one way the parent advance can have made a document wrong.
#
# The GN158 -> GN160 advance is **purely additive**, measured rather than assumed: 21 rows differ out
# of 38,161, no entry / name / body size differs anywhere, **no tag was lost on any row**, and every
# one of the 21 had `comment_len 0` before - no prior annotation at all. 20 gained a
# `GFZ.V121.CodeDomain.Presentation.*` tag, 1 `InputGameplay`.
#
# SO A PRIOR VERIFICATION CANNOT HAVE BEEN FALSIFIED BY IT. A verification breaks when something it
# relied on changes; nothing changed except annotations appearing where there were none. A document
# could not have verified against an annotation that did not exist.
#
# **EXCEPT IN ONE DIRECTION, AND THAT DIRECTION IS CHECKABLE.** A document that *asserts* one of these
# 21 is unclassified - "unowned", "untagged", "no owner" - made a claim that WAS true against GN158
# and is FALSE against the certified parent. That is not a stale stamp; it is a stale sentence, and it
# is the only thing the advance can have broken. "Nothing classifies this" is exactly the kind of
# absolute the evidence discipline says to challenge.
#
# FIVE VERDICTS, because the raw matches are mostly not defects:
#
#   STALE           asserts one of the 21 is unclassified. The claim was true and is not any more.
#   SELF-AWARE      the page already records the change - "unclassified in the 01:09 dump, classified
#                   by 01:23", "stale by the two functions the GN checkpoint closed". **The corpus
#                   caught some of this itself**, and counting those as defects would be wrong.
#   LINK-TEXT       the word is inside a markdown link title - `[the-largest-unclassified-functions]
#                   (...)`. A filename is not a claim, and ADDRESS-INDEX is generated.
#   HISTORY         `AUDIT-LOG.md`, which is append-only. A historical statement is correct AS
#                   history and must not be rewritten.
#   NEEDS-READ      the word describes something else on the line and whether the claim is affected
#                   needs the page.

import io, os, re, sys, collections

DB = "Database/FFXII TZA"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from provenance_transfer import load, EXPORTS, ADDR

UNCLASSIFIED = re.compile(
    r"unclassified|unowned|no owner|without an owner|untagged|no tag\b|no GFZ tag|"
    r"carries no annotation|no annotation|not annotated|no CodeDomain|"
    r"the GFZ does not|GFZ has no|no ledger tag|final_no_owner|FinalNoPrimaryOwner", re.I)
LINKSPAN = re.compile(r"\[[^\]]*\]\([^)]*\)")
AWARE = re.compile(r"classified by|now classified|GN checkpoint closed|stale by|since classified|"
                   r"01:23|closed by the GN|no longer unclassified|corrected 2026", re.I)
# A claim EXPLICITLY SCOPED to an older program state is correct as written and must not be
# "fixed". `the-unresolved-158.md` sits under the heading "A stale export, caught by disagreeing
# with itself" and says both functions have no owner "**in that file**" - bolding the scope. The
# sentence is ABOUT the stale export. I had it as a defect until I read the heading.
SCOPED = re.compile(r"in that file|in the 01:09 dump|in that (?:dump|export|snapshot)|"
                    r"stale export|against GN15\d|as of GN15\d", re.I)


def codedomain(tags):
    """The CodeDomain classification, not whichever tag happens to sort last.

    00313A00 carries ContextAuditV105;ContextAuditV99;GFZ.V121.CodeDomain.InputGameplay...,
    and taking the last element reported it as 'now V99_CombatActionCategoryParse' - a context
    audit marker, not the classification the advance added. Misleading in a report whose whole
    subject is what the function is now classified as.
    """
    for t in tags.split(";"):
        if "CodeDomain" in t:
            return t
    return tags.split(";")[-1]


def verdict(rel, line, m, para):
    """`para` is the surrounding paragraph; `line` is only for the link test.

    THE SENTENCE IS NOT THE LINE, and this is the third time today that assumption produced a
    wrong verdict. `the-unresolved-158.md` wraps its scope onto the NEXT line -

        ... Both genuinely have no owner, no finalNo
        and no CodeDomain **in that file**.

    - so a line-scoped test sees the claim without the qualifier that makes it correct. The link
    test stays line-scoped because a markdown link cannot span lines.
    """
    if rel == "_index/AUDIT-LOG.md":
        return "HISTORY"
    for lm in LINKSPAN.finditer(line):
        if lm.start() <= m.start() < lm.end():
            return "LINK-TEXT"
    if SCOPED.search(para):
        return "SCOPED-TO-OLD-STATE"
    if AWARE.search(para):
        return "SELF-AWARE"
    return "STALE"


def main():
    h0, A = load(EXPORTS[0])
    h1, B = load(EXPORTS[1])
    ti = h0.index("tags")
    moved = {e.upper(): B[e][ti] for e in A if A[e] != B[e]}

    hits, scanned = [], 0
    for root, dirs, files in os.walk(DB):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, DB).replace(os.sep, "/")
            scanned += 1
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            for n, line in enumerate(lines, 1):
                m = UNCLASSIFIED.search(line)
                if not m:
                    continue
                # Reach far enough FORWARD to see a correction note that follows the paragraph.
                # A corrected claim is normally left standing with the correction underneath it, so
                # a window that stops at the paragraph's own last line reports the claim and misses
                # its retraction - which is how line 213 of the glyph-quads page read STALE while
                # line 214, one line closer to the same note, read SELF-AWARE.
                para = " ".join(lines[max(0, n - 4):n + 9])
                for a in sorted(set(x.upper() for x in ADDR.findall(line)) & set(moved)):
                    lo = max(0, m.start() - 90)
                    hits.append((rel, n, a, moved[a], m.group(0), verdict(rel, line, m, para),
                                 " ".join(line[lo:m.end() + 110].split())))

    print("Sentences the additive parent advance may have falsified\n")
    print("  functions the parent newly classified : %d" % len(moved))
    print("  documents scanned                     : %d" % scanned)
    print("  matching sentences                    : %d\n" % len(hits))
    c = collections.Counter(h[5] for h in hits)
    for k in ("STALE", "SCOPED-TO-OLD-STATE", "SELF-AWARE", "LINK-TEXT", "HISTORY"):
        if c[k]:
            print("      %-12s %d" % (k, c[k]))
    print()
    for rel, n, a, tag, phrase, v, line in hits:
        if v != "STALE":
            continue
        print("  STALE  %s:%d   (\"%s\")" % (rel, n, phrase))
        print("      %s is now %s" % (a, codedomain(tag)[:96]))
        print("      ...%s..." % line)
        print()

    out = os.path.join(DB, "_index", "candidates", "parent-advance-stale-sentences.tsv")
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        for l in (
            "# Sentences calling a function unclassified that the certified parent has since classified.",
            "#",
            "# The GN158 -> GN160 advance is PURELY ADDITIVE, measured: 21 rows of 38,161 differ, no",
            "# entry/name/body size differs anywhere, no tag was lost on any row, and all 21 had",
            "# comment_len 0 before - no prior annotation at all. A prior verification therefore",
            "# cannot have been falsified by it: nothing changed except annotations appearing where",
            "# there were none.",
            "#",
            "# The one exception is a document that ASSERTS one of the 21 is unclassified. That claim",
            "# was true against GN158 and is false against the certified parent.",
            "#",
            "#   STALE       the claim was true and is not any more",
            "#   SELF-AWARE  the page already records the change - the corpus caught some itself",
            "#   LINK-TEXT   the word is inside a markdown link title; a filename is not a claim",
            "#   HISTORY     AUDIT-LOG, append-only; correct AS history and not to be rewritten",
            "#",
            "# document\tline\taddress\tverdict\tmatched\tnew_tag\tsentence",
        ):
            fh.write(l + "\n")
        for rel, n, a, tag, phrase, v, line in hits:
            fh.write("\t".join([rel, str(n), a, v, phrase, codedomain(tag), line]) + "\n")
    print("  wrote %s (%d rows)" % (out, len(hits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
