#!/usr/bin/env python3
"""check_frontier.py - EC-4: does the roadmap still list work the ledger says is finished?

Why this exists
---------------
Block selection reads `PROGRAM-STATE.md` §5 and takes the highest-leverage open item. That only
works while the roadmap is true. Twice in two blocks it was not:

- `F-5` still read *"Sweep documents for funclet-derived conclusions (`EC-1`)"* and §4 still said
  *"**Not yet done**"* — while `OPEN-QUESTIONS.md` had recorded `EC-1` **ANSWERED** the same day.
- `F-2` still read *"Schema migration toward machine-queryable knowledge"* — while
  `knowledge_db.py` already answered 22 of charter §7's queries and named the 4 it cannot.

Each cost a block-selection: work begins, and only a direct look at the artifact reveals it is
already done. **`check_questions` passes throughout**, because it compares the question table to
the documents' checklists — never the roadmap to the ledger, and never a claim of absence to the
filesystem.

The three checks
----------------
    STALE-QUESTION  an open frontier item cites a question the ledger marks ANSWERED.
                    Hard finding: two documents contradict each other about the same work.

    CLAIMED-ABSENT  a sentence asserting something does not exist ("not yet done", "has not yet
                    produced", "no ... exists") names a file that does exist on disk.
                    Hard finding: the text is checkable and false.

    MAYBE-DONE      an open frontier item names an artifact that exists. Advisory only: a
                    partially-built tool is a real reason for an item to stay open, so this
                    reports and does not judge.

An item counts as closed when its heading is struck through or says DONE, which is how this
roadmap already marks them.

Reach, stated plainly
---------------------
This compares **roadmap prose to the ledger and to the filesystem**. It cannot tell whether an item
is *substantively* finished — only whether the document contradicts a status or a file that is
right there. An item can be honestly open with every artifact present, and this tool says so by
putting that case in MAYBE-DONE rather than in a finding.
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
ROOT = KP.ROOT

QID = re.compile(r"\b([A-Z]{1,3}-\d{1,3})\b")
ARTIFACT = re.compile(r"`([A-Za-z0-9_.\-/]+\.(?:py|sqlite|tsv|md|json|c|h))`")
CLOSED = re.compile(r"~~|(?<![A-Za-z])DONE(?![A-Za-z])")
ABSENT = [
    (re.compile(r"\*\*not yet done:?\*\*|(?<![A-Za-z])not yet done(?![A-Za-z])", re.I),
     "not yet done"),
    (re.compile(r"has not yet (?:produced|built|shipped)", re.I), "has not yet produced"),
    (re.compile(r"\bdoes not (?:yet )?exist\b", re.I), "does not exist"),
    (re.compile(r"\bno\s+[a-z ]{0,24}\bexists\b", re.I), "no ... exists"),
    (re.compile(r"\bthe database cannot\b", re.I), "the database cannot"),
]


# Charter section 38 names four first-actions, and the block-selection prompt repeats the claim
# that the program "has not yet produced" them. That sentence directs EVERY block choice, so it is
# the single highest-leverage claim in the program to keep true -- and it is checkable, because
# each capability has a concrete artifact. Neither of the two stale items that motivated this tool
# cited a question or named a file, so the checks above miss them; this one does not.
FIRST_ACTIONS = [
    ("multidimensional coverage metrics",
     ["program_coverage.py", "COVERAGE-DIMENSIONS.md"]),
    ("a machine-queryable schema",
     ["knowledge_db.py", "knowledge.sqlite"]),
    ("integrity automation",
     ["check_links.py", "check_consistency.py", "check_questions.py", "check_denominators.py",
      "verify_doc_addresses.py", "check_caller_claims.py", "sweep_funclet_claims.py"]),
    ("a reconstruction/parity skeleton",
     ["mutation_test.py", "diff_name_registry.py"]),
]


def question_states(path):
    """-> {id: state}. The markdown is the source; the sqlite index is derived from it."""
    out = {}
    for line in io.open(path, encoding="utf-8", errors="replace").read().split(chr(10)):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = QID.match(cells[0].strip().strip("`"))
        if not m:
            continue
        state = re.sub(r"[*~_]", "", cells[-1]).strip().upper()
        if state:
            out[m.group(1)] = state
    return out


def frontier_items(text):
    """-> [(heading, body, closed)] for every '### ' item in the Frontier section."""
    lines = text.split(chr(10))
    start = None
    for i, l in enumerate(lines):
        if l.startswith("## ") and "Frontier" in l:
            start = i
            break
    if start is None:
        return []
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    items, cur = [], None
    for l in lines[start + 1:end]:
        if l.startswith("### "):
            if cur:
                items.append(cur)
            cur = [l, []]
        elif cur:
            cur[1].append(l)
    if cur:
        items.append(cur)
    return [(h, chr(10).join(b), bool(CLOSED.search(h))) for h, b in items]


def exists(root, db, name):
    """Is a named artifact anywhere under the repo? -> the path, or None."""
    base = os.path.basename(name)
    for top in (os.path.join(root, "Database", "Tools"), db,
                os.path.join(root, "Reconstruction"), os.path.join(root, "Database")):
        for r, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
            if base in files:
                return os.path.relpath(os.path.join(r, base), root).replace(os.sep, "/")
    return None


def quoted(line, pos):
    """Is the character at `pos` inside a quotation? Odd number of quote marks before it."""
    q = sum(line[:pos].count(c) for c in (chr(34), chr(8220), chr(8221)))
    return q % 2 == 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--control", action="store_true",
                    help="positive control: a synthetic stale item this check MUST flag")
    a = ap.parse_args()

    ps_path = os.path.join(a.db, "_index", "PROGRAM-STATE.md")
    oq_path = os.path.join(a.db, "_index", "OPEN-QUESTIONS.md")
    text = io.open(ps_path, encoding="utf-8", errors="replace").read()
    states = question_states(oq_path)
    answered = {q for q, s in states.items() if "ANSWERED" in s or "CLOSED" in s}
    print("questions in the ledger : %d  (answered/closed: %d)" % (len(states), len(answered)))

    if a.control:
        # The expected result is a small number, and zero findings reads the same whether the
        # roadmap is clean or the parser silently matched nothing. Plant one that must be found.
        victim = sorted(answered)[0] if answered else None
        if not victim:
            print("CONTROL: cannot run -- the ledger has no ANSWERED question to cite.")
            return 2
        text = text.replace("## 5. Frontier",
                            "## 5. Frontier" + chr(10) * 2
                            + "### `F-CONTROL` synthetic stale item (`%s`)" % victim + chr(10)
                            + "- planted by --control; must be flagged STALE-QUESTION" + chr(10),
                            1)
        print("control planted: an OPEN frontier item citing %s, which the ledger says is ANSWERED"
              % victim)

    items = frontier_items(text)
    openi = [(h, b) for h, b, c in items if not c]
    print("frontier items          : %d  (%d open, %d marked done)"
          % (len(items), len(openi), len(items) - len(openi)))
    print()

    stale, maybe = [], []
    for h, b in openi:
        cited = {q for q in QID.findall(h + chr(10) + b) if q in states}
        for q in sorted(cited & answered):
            stale.append((h.strip(), q, states[q]))
        for name in sorted(set(ARTIFACT.findall(h + chr(10) + b))):
            p = exists(a.root, a.db, name)
            if p:
                maybe.append((h.strip(), name, p))

    absent = []
    for i, line in enumerate(text.split(chr(10)), 1):
        for rx, what in ABSENT:
            m = rx.search(line)
            if m:
                # A claim of absence INSIDE a quotation is a report of what was once said, not an
                # assertion. The first run flagged this file's own correction note, which quotes
                # the wording it is correcting -- a checker that cannot tell a quotation from a
                # claim will train its reader to ignore it.
                if quoted(line, m.start()):
                    continue
                for nm in ARTIFACT.finditer(line):
                    # The named file must be the OBJECT of the absence claim: inside
                    # the matched phrase or immediately beside it. An artifact merely
                    # named elsewhere on the same line is not claimed absent - the
                    # "no ... exists" pattern can never grammatically contain a
                    # filename anyway (dots/underscores break [a-z ]), so same-line
                    # association was a guaranteed false positive (the 2026-09-20
                    # flag on "no alternate path exists ... `diff_transform.py`
                    # gains a row" - the file is cited as existing and EXERCISED).
                    if not (m.start() - 60 <= nm.start() <= m.end() + 60):
                        continue
                    p = exists(a.root, a.db, nm.group(1))
                    if p:
                        absent.append((i, what, nm.group(1), p, line.strip()[:120]))

    ctrl = [s for s in stale if "F-CONTROL" in s[0]]
    stale = [s for s in stale if "F-CONTROL" not in s[0]]
    if a.control:
        if ctrl:
            print("CONTROL: FOUND -- this check can see a stale item.")
        else:
            print("CONTROL: **NOT FOUND** -- the parser sees nothing; every result below is void.")
            return 2
        print()

    print("STALE-QUESTION  an open frontier item cites an ANSWERED question : %d" % len(stale))
    for h, q, s in stale:
        print("   %s" % h)
        print("      cites %s, which the ledger marks %s" % (q, s))
    print()
    print("CLAIMED-ABSENT  a claim of absence names a file that exists      : %d" % len(absent))
    for ln, what, name, p, snippet in absent:
        print("   PROGRAM-STATE.md:%d  \"%s\" but %s exists at %s" % (ln, what, name, p))
        print("      %s" % snippet)
    print()
    print("MAYBE-DONE      an open item names an artifact that exists       : %d  (advisory)"
          % len(maybe))
    for h, name, p in maybe:
        print("   %s" % h)
        print("      names %s, which exists at %s" % (name, p))
    print()
    print("FIRST-ACTIONS   charter section 38's four, checked against the filesystem")
    unmet = 0
    for what, arts in FIRST_ACTIONS:
        found = [(n, exists(a.root, a.db, n)) for n in arts]
        have = [n for n, p in found if p]
        miss = [n for n, p in found if not p]
        ok = not miss
        if not ok:
            unmet += 1
        print("   %-34s %s  %d of %d present" % (what, "SATISFIED" if ok else "INCOMPLETE",
                                                 len(have), len(arts)))
        if miss:
            print("      missing: %s" % ", ".join(miss))
    print("   -> %d of %d satisfied. The prompt's \"has not yet produced\" sentence is true of"
          % (len(FIRST_ACTIONS) - unmet, len(FIRST_ACTIONS)))
    print("      %d of them; where it is false it misdirects every block that reads it." % unmet)
    print()
    print("A clean run means the roadmap does not contradict the ledger or the filesystem.")
    print("It does NOT mean every open item is genuinely unfinished -- an item can be honestly")
    print("open with all of its artifacts present, which is why that case is advisory.")
    return 1 if (stale or absent) else 0


if __name__ == "__main__":
    sys.exit(main())
