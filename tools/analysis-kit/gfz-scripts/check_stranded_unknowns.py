#!/usr/bin/env python3
"""check_stranded_unknowns.py - a document's OPEN unknown that another document already answered.

Why this exists
---------------
`check_answered_not_established.py` finds a document contradicting *itself*: a negative phrase
beside an id the register calls ANSWERED, in the same block.  Its own docstring records the gap
it cannot reach (the stale statement in a *different* block).  This tool is about a third shape,
measured twice on 2026-09-13:

  the-all-ones-empty-convention.md   S6: "What the +0x695/+0x696 and +0xB8/+0xB9 pairs hold.
                                     Their sentinel behaviour is read; their subject is not."
                                     -- the-battle-unit-field-map.md already names both PROVEN
                                     (`actionPresentationSlot`, `secondActionPresentationSlot`).

  which-roll-is-on-which-generator.md S10: "What FUN_00319530 rolls for. It is the eighth LCG
                                     draw site and is unnamed."  -- AD-6 answered it 2026-09-02,
                                     the day BEFORE that page's own last_reviewed, and CQ-1/AE-3
                                     finished it on 2026-09-12, naming the caller and all seven
                                     outcomes.

**Neither is reachable from inside the document.**  The answer is somewhere else entirely, and the
question stays open because nobody walks from a generator's page to its consumer's.  The shape is
specific: the answer lands where it was *found* -- in the consumer's page, or in the register -- and
the page that asked keeps asking.

The rule
--------
For each list item in a "what is not known" section that is **not** already ticked or struck, take
the addresses it names, and report:

  * OPEN-QUESTIONS.md rows carrying that address whose verdict reads ANSWERED-class, and
  * ticked checklist items (`- [x]`) in OTHER documents that carry the same address.

Both are strong signals because both are a *recorded closure* naming the same address, not mere
adjacency.  A hit is a QUESTION, not a defect: a page may legitimately keep a narrower unknown open
beside a broader answer, and it may be the page that is right.

Deliberately NOT done
---------------------
Bare co-citation.  An address appearing in another document's prose says nothing -- that is what
`check_already_answered.py` is for, at authoring time.  This tool only fires on a closure.

Two filters, each from a false positive in the first live run (259 hits)
-----------------------------------------------------------------------
MANY_ADDRS  An un-closed unknown that names more than two addresses is a LIST, not a question
            about one of them.  `cross-subsystem-accessor-hubs.md` S? enumerates sixteen hub
            members in a single bullet; `the-world-tick-and-the-field-frame.md`:633 names five
            callees.  Every address in such a bullet matched something, and none of the matches
            was about the bullet.
SUBJECT     The address must appear in the register row's QUESTION cell, not anywhere in the row.
            `FZ-28` is a question about `02099DE5`-`02099DE7` that happens to mention `002628B0`
            as the writer; matching on the whole row made it a closure for `002628B0`, which it
            is not.

MEASURED (2026-09-13, first live runs)
--------------------------------------
    259  first run, no filters
     62  + MANY_ADDRS and SUBJECT
     54  + the widened CLOSED_ITEM (thirty bullets were already struck and were reported anyway)
     53  after the first real defect it found was fixed

**The first defect it found, and the reason to keep it.**  `the-record-behind-every-actor.md`:194
asked *"Who calls 00266530, and therefore when a slot is recycled. Not traced. EH-6."*  `EH-6` had
been ANSWERED on **2026-09-08**, and its answer says in so many words that it *overturned that
document's headline* -- the pool is one allocation `memset` to zero, so slots are never recycled.
The page's section 2 carries the correction.  **Three statements elsewhere in the same page did
not**: that bullet, a modding note in section 7 telling readers a recycled slot keeps its previous
occupant's bytes, and an evidence row still reading **PROVEN** for *"it recycles rather than
constructs"*.  All three survived a falsification pass on 2026-09-12.

**An honest note on precision.**  That true positive was found for the wrong reason: the tool matched
it through an unrelated register row, because `EH-6`'s question cell names the function by NAME and
this tool keys on addresses.  Recall found the defect; the cited evidence did not explain it.  Read
the hit, not the citation.

The residual class is a hot address whose IDENTITY is answered while a question about one of its
FIELDS stays open -- `01F82D20` accounts for three hits that way.  Those are near-misses, not noise,
and are deliberately left in: the tool's output is a reading list, not a defect list.
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

ANSWERED = ("ANSWERED", "CLOSED", "DONE", "DISSOLVED", "REFUTED", "WITHDRAWN", "SUPERSEDED",
            "SATISFIED", "MEASURED", "TRIAGED", "BOUNDED", "RESOLVED", "DUPLICATE", "REVISED",
            "CONFIRMED")

# A heading that opens a document's own list of open unknowns.  The corpus writes it four ways.
UNKNOWN_HEAD = re.compile(
    r"^#{2,4}\s*(?:\d+[a-z]?\.\s*)?(?:what\s+)?(?:this\s+document\s+|is\s+)?"
    r"(?:not\s+known|does\s+not\s+establish|is\s+not\s+known|not\s+established|"
    r"what\s+is\s+not\s+known|open\s+questions?)\b", re.I)
ANY_HEAD = re.compile(r"^#{1,6}\s")
ADDR = re.compile(r"\b(?:0x)?(0[0-9A-Fa-f]{7})\b")

# A bullet naming more than this many addresses is a list, not a question about one of them.
MANY_ADDRS = 2

# An item that has already been closed in place.  Each of these was seen on a real closed bullet.
# `~~` had to move behind the bullet marker: `- ~~What X computes.~~ Answered` is the corpus's
# commonest closed form and an unanchored alternation never matched it, so thirty already-closed
# bullets were reported in the first run.  `[~]` is a real checkbox state here too ("ANSWERED
# STRUCTURALLY").
CLOSED_ITEM = re.compile(
    r"^\s*[-*]\s*(?:\[[x~]\]|~~)"
    r"|\*\*(?:answered|narrowed|corrected|closed|struck|revised)"
    r"|ANSWERED", re.I)


def docs_of(db):
    for root, _d, files in os.walk(db):
        top = os.path.relpath(root, db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for fn in sorted(files):
            if fn.endswith(".md") and fn != "README.md":
                yield os.path.join(root, fn)


def unknown_items(text):
    """-> [(line number, item text)] for every un-closed bullet in an unknowns section."""
    out = []
    lines = text.split("\n")
    inside = False
    cur = None
    start = 0
    for n, line in enumerate(lines, 1):
        if ANY_HEAD.match(line):
            if cur:
                out.append((start, "\n".join(cur)))
                cur = None
            inside = bool(UNKNOWN_HEAD.match(line))
            continue
        if not inside:
            continue
        if re.match(r"^\s*[-*]\s", line):
            if cur:
                out.append((start, "\n".join(cur)))
            cur, start = [line], n
        elif cur is not None:
            if line.strip() == "":
                out.append((start, "\n".join(cur)))
                cur = None
            else:
                cur.append(line)
    if cur:
        out.append((start, "\n".join(cur)))
    return [(n, t) for n, t in out if not CLOSED_ITEM.match(t)]


def closures(db):
    """-> (addr -> [register rows]), (addr -> [(doc, ticked line)])."""
    reg, tick = {}, {}
    for root, _d, files in os.walk(db):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for line in t.split("\n"):
                addrs = set(a.upper() for a in ADDR.findall(line))
                if not addrs:
                    continue
                if fn == "OPEN-QUESTIONS.md" and line.startswith("|"):
                    bare = re.sub(r"[*~`]", "", line).upper()
                    if any(("| " + k) in bare or ("|**" + k) in bare for k in ANSWERED):
                        # SUBJECT: only the question cell counts.  A row about one address that
                        # merely names another as its writer is not a closure for the writer.
                        cells = line.split("|")
                        q = cells[2] if len(cells) > 2 else ""
                        qa = set(x.upper() for x in ADDR.findall(q))
                        for a in addrs & qa:
                            reg.setdefault(a, []).append((rel, line.strip()))
                elif re.match(r"^\s*[-*]\s*\[x\]", line):
                    for a in addrs:
                        tick.setdefault(a, []).append((rel, line.strip()))
    return reg, tick


def run(db, limit):
    reg, tick = closures(db)
    findings = []
    for p in docs_of(db):
        rel = os.path.relpath(p, db).replace(os.sep, "/")
        t = io.open(p, encoding="utf-8", errors="replace").read()
        for n, item in unknown_items(t):
            named = sorted(set(x.upper() for x in ADDR.findall(item)))
            if len(named) > MANY_ADDRS:      # a list, not a question about one address
                continue
            for a in named:
                hits = [(k, r, l) for k, rows in (("register", reg), ("ticked", tick))
                        for r, l in rows.get(a, []) if r != rel]
                if hits:
                    findings.append((rel, n, a, item.strip(), hits))
    print("checked %d documents; %d un-closed unknown(s) name an address that a closure elsewhere "
          "already carries" % (sum(1 for _ in docs_of(db)), len(findings)))
    print("A hit is a QUESTION, not a defect. The open page may be the one that is right.\n")
    for rel, n, a, item, hits in findings[:limit]:
        first = item.strip().split("\n")[0]
        print("%s:%d" % (rel, n))
        print("   asks about %s : %s" % (a, first[:120]))
        for k, r, l in hits[:3]:
            print("      %-8s %-52s %s" % (k, r[:52], l[:110]))
        print("")
    if len(findings) > limit:
        print("...%d more, pass --limit" % (len(findings) - limit))
    return findings


SELF_DOC = """---
system: x
---
# x
## 6. What is not known

- **What the `+0x695` pair at `00306760` holds.** Its sentinel behaviour is read; its subject is not.
- [x] ~~**Already closed here** at `00512CD0`.~~ answered
"""
SELF_OTHER = "- [x] `00306760` is `actionPresentationSlot`, PROVEN.\n"
SELF_REG = ("| ID | Q | V |\n"
            "| CQ-1 | What is `00512CD0`? | **ANSWERED** |\n")


def self_test(tmp):
    d = os.path.join(tmp, "01-A")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "page.md"), "w", encoding="utf-8").write(SELF_DOC)
    io.open(os.path.join(d, "other.md"), "w", encoding="utf-8").write(SELF_OTHER)
    idx = os.path.join(tmp, "_index")
    os.makedirs(idx, exist_ok=True)
    io.open(os.path.join(idx, "OPEN-QUESTIONS.md"), "w", encoding="utf-8").write(SELF_REG)
    f = run(tmp, 10)
    got = set((x[2], x[4][0][0]) for x in f)
    assert ("00306760", "ticked") in got, "the ticked-elsewhere fixture did not fire"
    assert not any(x[2] == "00512CD0" for x in f), "a closed bullet was reported"
    print("self-test OK: the cross-document closure fires, the already-closed bullet does not")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.path.join(KP.ROOT, "Database", "FFXII TZA"))
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self_test(tmp)
        return 0
    run(a.db, a.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
