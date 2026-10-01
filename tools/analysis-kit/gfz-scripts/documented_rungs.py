"""What "every system documented" can and cannot mean, measured. Charter terminal-readiness support.

THE SLOGAN HIDES FOUR DIFFERENT CLAIMS. A page EXISTING, a page CALLING ITSELF COMPLETE, a page
SURVIVING FALSIFICATION and a page LEAVING NOTHING UNEXPLAINED are four different facts, and
collapsing them into one "documented" percentage is how a database congratulates itself. So, as
`program_coverage.py` does, this prints rungs and never a composite.

    R0  A PAGE EXISTS                  the document is in the corpus and carries a `system:` key
    R1  IT DOES NOT CALL ITSELF SHORT  `status:` is not PARTIAL/REOPENED and names no residual
    R2  SOMEBODY TRIED TO BREAK IT     `audit.passes >= 1` - falsification survived at least once
    R3  NOTHING IS LEFT UNEXPLAINED    the page carries no unticked checkbox

WHY R3 IS MEASURED PER PAGE AND NOT FROM THE REGISTER, which is the correction that produced this
file's current form. Two earlier versions tried to derive R3 by parsing `OPEN-QUESTIONS.md` - first
by searching whole rows for a page's filename stem, then by splitting the declared four columns - and
reported 446 open rows and then 36, a 12x disagreement. BOTH WERE WRONG, AND SO WAS THE CONCLUSION I
DREW FROM THEM, which was that the register is not machine readable. It is. `check_questions.py`
already parses it correctly and reports `rows whose cell count differs from their table header: 0`.
That script had ALREADY SOLVED every problem I thought I had found: it knows 20 distinct status
markers are in use, it knows the status lives in a different column depending on whether a row has a
link cell so the last cell is not the status, and it had already repaired the `||`-inside-a-code-span
split that mis-scored row `EE-1`. I built a parser without looking for the one that existed.

So R3 delegates: the register's state is `check_questions.py`'s to report, and this script measures
the page-local fact instead - AN UNTICKED CHECKBOX IS AN UNANSWERED QUESTION ON THAT PAGE. That needs
no attribution and no row parsing, and it is controlled here against the gate's own box totals.

AND THE DENOMINATOR IS THE PART NO PAGE CAN FIX. Every rung divides by the documents that EXIST. A
system nobody has written up is not a 0 in this table - IT IS NOT IN THE TABLE. `327 / 327 pages
exist` is a tautology, not a coverage result. The only handle on it is the code side, printed last.

Usage:  python documented_rungs.py --db "Database/FFXII TZA"
Exit 0 always: this is a measurement, not a gate.
"""
import argparse
import io
import os
import re
import sys

STATUS_COMPLETE = {"DOCUMENTED", "EXPLAINED", "AUDITED", "CONTRACT READY"}
# A status line may carry its residual inline: `PARTIAL - what the six modes mean is not established`.
# Those are the pages being honest, and they count short whatever the leading token says.
RESIDUAL = re.compile(r"\bnot (?:established|read|resolved|decoded|explained)\b"
                      r"|\b(?:remains?|stands?|still) open\b|\bunresolved\b|\bopen\b", re.I)
BOX = re.compile(r"^\s*[-*]\s*\[( |x|X)\]", re.M)


def load(db):
    docs = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)]
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), db).replace("\\", "/")
            if rel.startswith("_index/_inbox/"):
                continue
            text = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            fm, block = {}, ""
            if text.startswith("---"):
                end = text.find("\n---", 3)
                if end > 0:
                    block = text[3:end]
                    fm = dict(re.findall(r"^([a-z_]+):\s*(.*)$", block, re.M))
            docs.append({"rel": rel, "text": text, "fm_block": block,
                         "fm": {k: v.strip() for k, v in fm.items()},
                         "index": rel.startswith("_index/")})
    return docs


def passes_of(doc):
    """`audit.passes` is NESTED, so the flat frontmatter parser every other script uses cannot see
    it. Read it from the raw block rather than inheriting a silent zero."""
    m = re.search(r"^audit:\s*$(.*?)(?=^\S|\Z)", doc["fm_block"] + "\n", re.M | re.S)
    if not m:
        return None
    p = re.search(r"^\s+passes:\s*(\d+)", m.group(1), re.M)
    return int(p.group(1)) if p else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    a = ap.parse_args()

    docs = load(a.db)
    systems = [d for d in docs if not d["index"] and "system" in d["fm"]]
    n = len(systems)
    if not n:
        print("no system documents found under %s" % a.db, file=sys.stderr)
        return 2

    r1set, r2set, r3set = set(), set(), set()
    auditedset, r1status = set(), {}
    no_audit_key = 0
    boxes = unticked = 0
    for d in systems:
        st = d["fm"].get("status", "")
        lead = st.split("—")[0].split(" - ")[0].strip().strip('"')
        if lead.upper() in STATUS_COMPLETE and not RESIDUAL.search(st):
            r1set.add(d["rel"])
            r1status[lead.upper()] = r1status.get(lead.upper(), 0) + 1
        if lead.upper() == "AUDITED" and not RESIDUAL.search(st):
            auditedset.add(d["rel"])
        p = passes_of(d)
        if p is None:
            no_audit_key += 1
        elif p >= 1:
            r2set.add(d["rel"])
        found = BOX.findall(d["text"])
        boxes += len(found)
        open_here = sum(1 for g in found if g == " ")
        unticked += open_here
        if not open_here:
            r3set.add(d["rel"])

    def line(label, k, note=""):
        print("  %-52s %4d / %d   %6.2f %%  %s" % (label, k, n, 100.0 * k / n, note))

    print("")
    print("WHAT \"EVERY SYSTEM DOCUMENTED\" MEASURES, RUNG BY RUNG   (denominator: %d system documents)" % n)
    print("")
    line("R0  a page exists", n, "<- a tautology, not a coverage result")
    line("R1  it does not call itself short", len(r1set))
    line("R2  somebody tried to break it (audit.passes >= 1)", len(r2set))
    line("R3  no unticked checkbox on the page", len(r3set))
    line("R1 + R2 + R3 together", len(r1set & r2set & r3set), "<- the honest reading of the phrase")
    line("R4  the status the STANDARD calls complete", len(auditedset),
         "<- `AUDITED`; see below")
    print("")
    # WHAT R1 ACTUALLY CONTAINS, because the rung's name is not a completion claim and the two
    # lines under it used to read as though it were. EVIDENCE-STANDARD's status lifecycle:
    # "DOCUMENTED is no longer the completion bar. AUDITED is." DOCUMENTED means "All eight
    # sections filled, every claim cites a tier. NOT YET FACT." So a DOCUMENTED page with no
    # falsification pass is not a page overclaiming - it is a page in the state the standard
    # prescribes, and saying otherwise sends a reader to audit pages that are behaving correctly.
    print("  R1 IS NOT A COMPLETION CLAIM. Its members by status:")
    for k in sorted(r1status):
        print("      %-14s %d" % (k, r1status[k]))
    print("  EVIDENCE-STANDARD: `DOCUMENTED` is NOT the completion bar - `AUDITED` is, and")
    print("  `DOCUMENTED` means 'all eight sections filled, every claim cites a tier. Not yet")
    print("  fact.' So the %d page(s) in R1 without a falsification pass are in the state the"
          % len(r1set - r2set))
    print("  standard prescribes, not overclaiming. THE FIGURE THAT MATTERS IS R4 ABOVE.")
    print("  %d page(s) in R1 have a recorded falsification pass and are NOT `AUDITED` - the"
          % max(0, len(r1set & r2set) - len(auditedset)))
    print("  count is R1 and R2 minus R4, so it spans `DOCUMENTED` and `EXPLAINED` both, and is")
    print("  not a count of one status. Whether they should be promoted is their owners' call and")
    print("  the lifecycle owner's; promoting them here to move a rung is the failure this file")
    print("  exists to prevent.")
    print("  %d page(s) in R1 still carry an unticked box." % len(r1set - r3set))
    print("  %d page(s) carry no `audit:` block at all, so their pass count is absent, not zero."
          % no_audit_key)
    print("")
    print("  CONTROL: %d checkbox(es) on system documents, %d unticked. `check_questions.py` counts"
          % (boxes, unticked))
    print("  the boxes DB-wide including index pages, so its total is the larger number; if this")
    print("  count ever exceeds the gate's, one of the two parsers is wrong. THE REGISTER'S OWN")
    print("  STATE IS `check_questions.py`'s TO REPORT, NOT THIS SCRIPT'S - an earlier version of")
    print("  this file tried to re-derive it and was refuted by that gate.")
    print("")
    print("THE CEILING NOBODY CAN RAISE BY WRITING PAGES:")
    print("  Every rung above divides by the documents that EXIST. A system with no page is not a 0")
    print("  in this table - IT IS NOT IN THE TABLE. Run `program_coverage.py` for the code-side")
    print("  bound (authored functions reached by any document at all); that share, not this one, is")
    print("  what limits the phrase \"every system\".")
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
