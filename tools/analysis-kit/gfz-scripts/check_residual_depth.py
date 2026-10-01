#!/usr/bin/env python3
"""check_residual_depth.py - which ledger residuals can be classified from prose that already exists.

`unresolved` is a TAGGING state (EVIDENCE-STANDARD addendum 2026-09-13t): a body carrying no
`GFZ.V121.CodeDomain`. Driving it to zero is checkpoint work, and the cheap end of that work is
every body the corpus has already described - whoever tags those has the evidence in hand.

THE RULE, from `99-Unresolved-Residual/the-unresolved-158.md` (OPUS):

    A citation establishes a CodeDomain when it SAYS WHAT THE FUNCTION DOES - a prototype, a verb
    about named state, or a position in a named pipeline. It does not when it only NAMES the
    function, and explicitly does not when the prose records that the function was not followed.
    Citations inside a pass-22 crossing section never establish ownership: those name the FAR END
    of an edge, which is the population R6 excludes from being a subject.

WHY THIS REPLACES `Tools/work/OPUS/residual_citation_depth.py`
-------------------------------------------------------------
That tool reported 22 classifiable and 8 needing a body read. Re-reading the 8 against the rule
above found that **7 of them are described**, and each miss has a nameable cause in the tool:

1. IT SKIPPED `99-Unresolved-Residual` ENTIRELY. That is the folder where residual bodies are
   written up. `0024B580` came back with ZERO citing lines - not BARE, zero - because the only page
   that reads it ("**It is a deferred-work queue drain.**") lives there. The exclusion was meant to
   stop the residual survey pages counting as owners; it also hid the only readings of them.
2. ITS ROLE VOCABULARY WAS VERBS ONLY. The corpus states a role as a NOUN PHRASE at least as often:
   "the item-sort bar" (`00566680`), "child-widget create+attach" (`002BA310`), "round-robin channel
   picker" (`002C3D70`). None contains a listed verb; all three say exactly what the function is.
3. `handles` WAS NOT IN THE LIST. `0020F3E0` is cited as "`0020F3E0` handles one PACKED GIF packet.
   For each register slot:" - as plain a role sentence as the corpus contains.
4. IT BANDS LINES, AND PROSE HARD-WRAPS. `001D72F0` and `001D7A20` are named on one line and their
   behaviour is on the next: "...and the two render passes `001D72F0` (from the render pass list) and
   `001D7A20` (from the slot-4 pump) / return at once while it is set". The tool's own docstring
   admits it bands lines; this is what that costs.

So the band is computed over a WINDOW of lines, not one line, and a role may be a noun phrase.
DISCLAIM still wins over ROLE inside the window, because a page that says it did not follow a
function has said the more specific thing.

THE CONTROL, AND IT IS THE REASON THE NEW SPLIT CAN BE QUOTED
-------------------------------------------------------------
The ruling above was produced with the old tool plus TWO HAND CORRECTIONS, one in each direction:
`002ABF70` moved into classifiable (a false negative) and `0036A2A0` moved out (a false positive,
because the page names it precisely to say it did not follow it). Those corrections were made by
reading, not by the tool.

Run here, this tool reports 29 DESCRIBED and **`0036A2A0` alone as CONTESTED** - it reproduces both
hand corrections unaided, from the passages, without either address being special-cased. A rewrite
that moved 7 bodies out of the expensive queue would be worth distrusting on its own; one that also
lands on the one judgement a person had to make by hand is checkable.

NOT A GATE PASS. It reports and routes; the classification itself is SWE2-EC7's.
"""
import argparse
import collections
import io
import os
import re
import sys

DISCLAIM = re.compile(
    r"\bnot traced\b|\bnot read\b|\bunread\b|\bnot followed\b|\bentry only\b|\bat its entry\b"
    r"|\bnot established\b|\bnot known\b|\bnot decoded\b|\bnot opened\b|\bnot measured\b"
    r"|\bwe do not\b|\bnobody has\b", re.I)

# A DISCLAIMER DISQUALIFIES WHAT IT NAMES, AND NOTHING NEXT TO IT (FABLE ruling 2026-09-14 §2).
#
#   kind (i)   the FUNCTION is disclaimed - its body was not read, not followed, not entered.
#              No sentence on that page establishes a CodeDomain for it.        -> DISCLAIMED
#   kind (ii)  a PROPERTY is disclaimed - an output, one effect, one field, one caller's use.
#              The positively-read sentences stand on their own evidence, and the disclaimed
#              property is residue.                    -> band on the positive sentences instead
#
# The discriminator is the OBJECT of the disclaiming verb.
#
# WHY THIS CHANGE IS MADE NOW AND WAS REFUSED EARLIER, which matters more than the diff. On
# 2026-09-14 OPUS published a byte-level reading of `0036A2A0` and noted that this checker still
# banded it CONTESTED, because the new section QUOTES the old disclaimer in order to withdraw it -
# and declined to patch the tool: "teaching an instrument to ignore a disclaimer I happen to be
# quoting would be adjusting it until my own row comes out green." The same code change is correct
# now because FABLE ruled the distinction on its merits, not because it is convenient.
#
# MEASURED BEFORE IMPLEMENTING, as the ruling required: of the thirty bodies the citation rule has
# been applied to, EXACTLY ONE BAND MOVES - `0036A2A0`, CONTESTED -> DESCRIBED. 29 DESCRIBED /
# 1 CONTESTED / 0 UNREAD becomes 30 / 0 / 0.
FUNC_DISCLAIMED = re.compile(
    r"\b(?:not (?:read|followed|entered|opened|decoded|disassembled|walked))\b"
    r"|\bbody (?:was |is )?not\b|\bnever (?:read|entered|followed)\b|\bunread\b", re.I)
PROP_DISCLAIMED = re.compile(
    r"\bwhether\b[^.]{0,120}\bis not traced\b|\bnot traced\b|\bnot established\b|\bnot measured\b"
    r"|\bnot known\b", re.I)

# A role sentence says what it DOES or what it IS. A prototype counts on its own.
ROLE_VERB = re.compile(
    r"`?0[0-9A-Fa-f]{7}`?\s*\([^)]*\)"
    r"|\b(?:builds|writes|reads|returns|walks|dispatches|selects|resolves|computes|clears|sets"
    r"|allocates|frees|draws|paints|plays|loads|stores|copies|parses|decodes|installs|advances"
    r"|updates|applies|refuses|bounds|gates|maps|emits|pushes|pops|seeds|steps|scales|wraps"
    r"|handles|collects|scans|divides|submits|evaluates|drains|queues|attaches|detaches"
    r"|iterates|indexes|samples|aims|converts)\b", re.I)
# ...or what it IS. A noun phrase naming the thing is a role; the corpus writes these in table
# cells and headings, where a verb would be redundant.
ROLE_NOUN = re.compile(
    r"\b(?:is|it is|the)\s+(?:a|an|the|one)?\s*[\w-]*\s*"
    r"(?:interpreter|builder|painter|walker|reader|writer|driver|formatter|dispatcher|resolver"
    r"|loader|gate|pass|hub|router|emitter|selector|allocator|picker|drain|queue|ramp|bar|list"
    r"|window|widget|pane|table|stepper|pump|filler|sorter|registry|tracker)\b"
    r"|\b(?:create\+attach|round-robin \w+|item-sort \w+|render pass(?:es)?|easing ramp)\b", re.I)

CROSSING_SECTION = re.compile(
    r"^#{2,3} +(?:Cross-subsystem neighbours|Crossings into other layers)"
    r"[^\n]*\n.*?(?=^#{1,3} |\Z)", re.M | re.S)

# _index is registers and link tables; _inbox is board traffic. Neither is a page about a function.
# `99-Unresolved-Residual` is NOT excluded - see defect 1 in the docstring.
SKIP_TOP = ("_index", "_inbox", "_templates", "_experiments")
WINDOW = 2          # lines either side, so a hard-wrapped sentence is read as one

# AND THE WINDOW HAS ITS OWN FAILURE, FOUND THE FIRST TIME THIS RAN.
# Widening from one line to five made `002C3D70` "classifiable" on this line:
#     `001D72F0`, `001D7A20`, `0020F3E0`, `0024B580`, `002BA310`, `002C3D70`, ... need a reading
# - the worklist itself, with role words from the sentences around it dragged in by the window. A
# line that enumerates several residual addresses is a LIST; it describes none of them. Excluding
# it is not a special case for one document: any triage table has this shape, and a fix that made
# the count look better without this would be the tool marking its own homework.
LISTY = 3           # this many residual addresses on one line makes it a list, not a description



def disclaims_the_function(ctx):
    """True only for FABLE's kind (i): the passage disclaims the FUNCTION, not a property of it.

    A passage with no disclaimer at all is False. A passage whose disclaimer names an output, an
    effect, a field or a use is False too - its positive sentences stand on their own evidence and
    the property becomes residue."""
    if not DISCLAIM.search(ctx):
        return False
    return bool(FUNC_DISCLAIMED.search(ctx)) and not PROP_DISCLAIMED.search(ctx)

def bands(db, addrs):
    band = {h: collections.Counter() for h in addrs}
    best = {h: None for h in addrs}
    for dirpath, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for name in sorted(f for f in files if f.endswith(".md")):
            rel = os.path.relpath(os.path.join(dirpath, name), db).replace(os.sep, "/")
            if rel.split("/")[0] in SKIP_TOP:
                continue
            try:
                text = io.open(os.path.join(dirpath, name), encoding="utf-8",
                               errors="replace").read()
            except OSError:
                continue
            for m in reversed(list(CROSSING_SECTION.finditer(text))):
                text = text[:m.start()] + text[m.end():]
            lines = text.split("\n")
            up = text.upper()
            for h in addrs:
                if h not in up and ("FUN_" + h.lower()) not in text:
                    continue
                for i, line in enumerate(lines):
                    lu = line.upper()
                    if h not in lu and ("FUN_" + h.lower()) not in line:
                        continue
                    if sum(1 for x in addrs if x in lu) >= LISTY:
                        band[h]["LIST"] += 1
                        continue
                    # A TABLE ROW IS SELF-CONTAINED AND THE WINDOW MUST NOT CROSS IT. The row above
                    # `002C3D70`'s in the transform-primitives table ends "Track variant, not read
                    # deeper" - about a DIFFERENT function - and the window read that disclaimer as
                    # this body's. Widening context is right for hard-wrapped prose and wrong for a
                    # table, where adjacency means nothing.
                    ctx = (line if line.lstrip().startswith("|")
                           else " ".join(lines[max(0, i - WINDOW):i + WINDOW + 1]))
                    if disclaims_the_function(ctx):
                        band[h]["DISCLAIMED"] += 1
                    elif ROLE_VERB.search(ctx) or ROLE_NOUN.search(ctx):
                        band[h]["ROLE"] += 1
                        if best[h] is None:
                            best[h] = (rel, line.strip()[:170])
                    else:
                        band[h]["BARE"] += 1
    return band, best


def self_test():
    """Each case is one of the four defects, written as the line that exposed it."""
    cases = [
        ("`0020F3E0` handles one PACKED GIF packet. For each register slot:", "ROLE"),
        ("| `00566680` | the item-sort bar (997 B) - above |", "ROLE"),
        ("| `002BA310` | 543 | child-widget create+attach: `[rdi+0xC0]` |", "ROLE"),
        ("| `002C3D70` | 1151 | round-robin channel picker: collects `[entry+0x40]&1` |", "ROLE"),
        ("**It is a deferred-work queue drain.** `0024B580` reads `[02092170]`", "ROLE"),
        # FABLE 2026-09-14 section 2 kind (ii): the disclaimer names an OUTPUT, not the function.
        # This case expected DISCLAIMED under the old rule and the EXPECTATION is what changed.
        ("whether `0036A2A0` produces blocks that carry this header is not traced.", "BARE"),
        # kind (ii) again, but with a positive sentence beside it - the positive one wins
        ("`0036A2A0` is a direct caller of the arena allocator; whether its blocks carry "
         "the header is not traced.", "ROLE"),
        # kind (i): the FUNCTION is disclaimed. Still DISCLAIMED.
        ("`0036CB00` was not read and nothing on this page follows it.", "DISCLAIMED"),
        ("| `0024B580` | 324 B | 17-Presentation-Rendering |", "BARE"),
    ]
    bad = 0
    for text, want in cases:
        if disclaims_the_function(text):
            got = "DISCLAIMED"
        elif ROLE_VERB.search(text) or ROLE_NOUN.search(text):
            got = "ROLE"
        else:
            got = "BARE"
        if got != want:
            bad += 1
            print("  SELF-TEST FAIL: %r -> %s, wanted %s" % (text, got, want))
    print("self-test: %d of %d cases correct" % (len(cases) - bad, len(cases)))
    return 1 if bad else 0


def read_residual(path):
    """The residual addresses, by COLUMN when the file is the committed TSV.

    A whole-file regex over residual-30-GN161.tsv returns SEVENTY-EIGHT addresses, not thirty: its
    evidence column cites the bodies each row was judged against. Reading the population that way
    would have inflated 30 to 78 silently, which is the census defect this database keeps finding -
    a list that counts what it reached rather than what it names. So a file with an `address`
    header is read by that column, and only a plain address list falls back to the regex.
    """
    text = io.open(path, encoding="utf-8", errors="replace").read()
    rows = [l for l in text.split("\n") if l.strip() and not l.lstrip().startswith("#")]
    if rows and rows[0].split("\t")[0].strip().lower() == "address":
        out = set()
        for l in rows[1:]:
            cell = l.split("\t")[0].strip().upper()
            if re.fullmatch(r"[0-9A-F]{8}", cell):
                out.add(cell)
        return out
    return {h.upper() for h in re.findall(r"[0-9A-Fa-f]{8}", text)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--residual", help="path to residual_addrs.txt")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")
    # THE DEFAULT WAS A GIT-IGNORED SCRATCH FILE, AND THE PATH TO IT WAS WRONG. It resolved
    # `Tools/work/verify_GFZ_PARENT/residual_addrs.txt` from three dirname() hops above --db, which
    # lands one directory ABOVE the repository and omits `Database/` - so the gate exited 2 with
    # "no residual list" on a correct checkout. Even repaired, that path is inside `Tools/work/`,
    # which .gitignore excludes: a peer who clones this repository does not have the file, so the
    # gate could never have run for anyone but its author. c65b1a16 fixed the same defect in
    # 99-Unresolved-Residual/README.md, which used to link that very file.
    #
    # The default is now the COMMITTED list. Set equality was checked, not assumed: the scratch
    # file and the address column of residual-30-GN161.tsv both hold the same 30 addresses, sorted
    # set diff empty (2026-09-16, OPUS) - the same claim c65b1a16 made for the README.
    resid = a.residual or os.path.join(os.path.abspath(a.db), "99-Unresolved-Residual",
                                       "residual-30-GN161.tsv")
    if not os.path.exists(resid):
        print("no residual list at %s - pass --residual" % resid)
        return 2
    addrs = sorted(read_residual(resid))

    band, best = bands(a.db, addrs)
    ok = [h for h in addrs if band[h]["ROLE"] and band[h]["ROLE"] > band[h]["DISCLAIMED"]]
    contested = [h for h in addrs if band[h]["ROLE"] and band[h]["ROLE"] <= band[h]["DISCLAIMED"]]
    read = [h for h in addrs if not band[h]["ROLE"]]

    print("residual classification depth - %d unresolved bodies\n" % len(addrs))
    print("  THIS IS A WORKLIST, NOT A VERDICT. It bands passages; a person reads the passage and")
    print("  decides. The ruling it implements was itself corrected twice by hand, in both")
    print("  directions, and nothing here removes that step.\n")
    print("  DESCRIBED - a passage says what it does, and no passage refuses: %d" % len(ok))
    for h in ok:
        rel, line = best[h] or ("", "")
        print("     %s  ROLE %-3d DISC %-2d BARE %-3d LIST %-2d  %s" %
              (h, band[h]["ROLE"], band[h]["DISCLAIMED"], band[h]["BARE"], band[h]["LIST"], rel))
        print("        %s" % line)
    print("\n  CONTESTED - described somewhere and refused somewhere; READ BOTH: %d" % len(contested))
    for h in contested:
        rel, line = best[h] or ("", "")
        print("     %s  ROLE %-3d DISC %-2d BARE %-3d LIST %-2d  %s" %
              (h, band[h]["ROLE"], band[h]["DISCLAIMED"], band[h]["BARE"], band[h]["LIST"], rel))
        print("        %s" % line)
    print("\n  NEEDS THE BODY READ - nothing says what it does: %d" % len(read))
    for h in read:
        print("     %s  DISCLAIMED %d / BARE %d / LIST %d"
              % (h, band[h]["DISCLAIMED"], band[h]["BARE"], band[h]["LIST"]))
    print("\n  LIST counts lines that enumerate %d or more residual addresses. Those are worklists" % LISTY)
    print("  and describe nothing; a BARE of 0 with a DISCLAIMED of 0 and a LIST above 0 means the")
    print("  only prose naming the body is the queue it is waiting in.")
    return 1 if (read or contested) else 0


if __name__ == "__main__":
    sys.exit(main())
