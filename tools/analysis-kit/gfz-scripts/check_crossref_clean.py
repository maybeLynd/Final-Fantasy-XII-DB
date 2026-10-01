#!/usr/bin/env python3
"""check_crossref_clean.py - enforce the ONE canonical meaning of `crossref_clean:`.

REVIEWED AND IN THE KIT. Proposed 2026-09-15 (OPUS, OPUS-SPEC-CROSSREF-CLEAN-CANONICAL-DEFINITION),
accepted 2026-09-16 by SWE2-AUDIT-SPEC on OPUS-REQ-AUDITSPEC-REVIEW-CROSSREF-CLEAN-DEFINITION:
*"the definition is well-formed, the checker implements it faithfully, and its self-test passes"*,
record `Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-P30-CROSSREF-CLEAN.md`, journal `26cb7ea7`.
FINAL-AUDIT pass 30 asks for one canonical definition, independently reviewed, THEN enforced
mechanically. The review is the reason this file is here rather than in proposals/.

THE ONE LIMIT THE REVIEW RECORDED, AND THE DECISION TAKEN ON IT. Freshness compares the report's
mtime against DOCUMENT mtimes only, but `audit_crossrefs` also consumes `functions.tsv`,
`edges.tsv`, the unlisted-code registries and the pass-22 disposition registry, so a report built
on a stale INPUT still validates `true` claims. The reviewer left it explicitly to OPUS - *"either
is defensible, but it should be a decision, not an oversight"*.

**DECIDED: documents only, and the limit is stated rather than closed.** Extending freshness to the
graph inputs would couple this checker to a GN161 re-export cadence it does not control, and would
make a `true` claim fail for a reason that has nothing to do with the document - which is the 
class of manufactured defect this kit keeps having to undo. What a stale graph input actually
produces is a WRONG FINDING SET, and that is pass 2's and pass 4's subject, not pass 30's. Pass 30
asks whether the field says what the checker says; it is not the instrument that certifies the
checker's inputs. A reader who needs that guarantee should read the ledger, and the same
reasoning is why the AUDIT-SPEC ruling on `audit_crossrefs --at` puts whole-revision
materialisation in THAT tool rather than here.

The definition this enforces
----------------------------
1. DOMAIN. The frontmatter key `crossref_clean` on every `.md` outside `_index/`, README.md
   excluded - the population this checker has always walked.
2. VALUES. Exactly `true` or `false`. An absent key makes no claim. Any other value is MALFORMED
   (three documents at HEAD 54b14368 carry `dispositioned`) and fails, because a status field
   whose vocabulary is open cannot be checked.
3. `true` ASSERTS that a fresh `audit_crossrefs.py --json` report over the database reports ZERO
   DOCUMENT-DEFECT findings against the document. Every finding kind is a document defect EXCEPT
   the kinds named in CENSUS_DEBT_KINDS below, which the audit tool itself labels as facts about
   the function list rather than the document (`UNLISTED CODE`: "census debt, not a document
   defect"). A kind audit_crossrefs adds later is a defect kind unless it is added to that constant
   by name - the exclusion is closed, by kind, never by document. Registry-dispositioned neighbour
   pairs are not findings at all (audit_crossrefs already moves them to their own class).
4. `false` ASSERTS NOTHING. It means "not asserted clean". A `false` document with zero defect
   findings is reported as ELIGIBLE, never as a failure: on 2026-09-03 the 24 such documents were
   stale through audit_crossrefs becoming fairer, not through their own error, and the correction
   there was to record provenance, not to flip them. 264 are in that state at HEAD.
5. FRESHNESS is re-derived, not stamped. The report must be newer than every document it judges;
   a report older than any document is REFUSED (exit 2) instead of used. The 2026-09-03
   `crossref_checked` / `crossref_report` provenance keys become optional: 0 of the 52 `true`
   documents at HEAD carry them, and a re-derivation on every run is stronger than a stamp.

Exit status: 0 clean (advisories printed), 1 a `true` with a defect finding or a malformed value,
2 unusable input (missing or stale report).

Usage
-----
    python audit_crossrefs.py --docs "Database/FFXII TZA" --functions ... --edges ... --json r.json
    python check_crossref_clean.py --db "Database/FFXII TZA" --report r.json
    python check_crossref_clean.py --self-test
"""
import argparse
import collections
import datetime
import io
import json
import os
import re
import sys

FIELD = re.compile(r"^\s*crossref_clean:\s*(\S+)\s*$", re.M)

# Closed list, by kind name. Each entry must be a kind whose own detail text in audit_crossrefs.py
# says it is not a document defect.
CENSUS_DEBT_KINDS = ("UNLISTED CODE",)

MALFORMED = object()


def frontmatter(text):
    """The frontmatter block, or '' when the document has none."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[:end] if end != -1 else ""


def declared(text):
    """True / False / None (field absent) / MALFORMED for crossref_clean."""
    m = FIELD.search(frontmatter(text))
    if not m:
        return None
    v = m.group(1).strip().lower().rstrip(",")
    if v == "true":
        return True
    if v == "false":
        return False
    return MALFORMED


def walk(db):
    for root, _d, files in os.walk(db):
        if "_index" in root.split(os.sep):
            continue
        for fn in sorted(files):
            if fn.endswith(".md") and fn != "README.md":
                yield os.path.join(root, fn)


def check(db, findings_by_doc):
    fail, eligible, debt_only = [], [], []
    for p in walk(db):
        rel = os.path.relpath(p, db).replace(os.sep, "/")
        says = declared(io.open(p, encoding="utf-8", errors="replace").read())
        if says is None:
            continue
        rows = findings_by_doc.get(rel, ())
        defects = [r for r in rows if r[0] not in CENSUS_DEBT_KINDS]
        if says is MALFORMED:
            fail.append((rel, "MALFORMED VALUE - crossref_clean must be true or false"))
        elif says and defects:
            fail.append((rel, "CLAIMS CLEAN, HAS %d DOCUMENT-DEFECT FINDING(S): %s"
                         % (len(defects), ", ".join(sorted({r[0] for r in defects})))))
        elif says and rows:
            debt_only.append((rel, len(rows)))
        elif says is False and not defects:
            eligible.append(rel)
    return fail, eligible, debt_only


def self_test():
    doc = "---\ntitle: x\naudit:\n  crossref_clean: %s\n---\n\nbody\n"
    checks = [
        (declared(doc % "true") is True, "parses true"),
        (declared(doc % "false") is False, "parses false"),
        (declared("---\ntitle: x\n---\nbody\n") is None, "absent is no claim"),
        (declared(doc % "dispositioned") is MALFORMED, "a third value is malformed"),
        (declared(doc % "yes") is MALFORMED, "yes is not a synonym - the vocabulary is closed"),
        (declared("---\ntitle: x\n---\n\nWe set `crossref_clean: true` after.\n") is None,
         "prose is not frontmatter"),
    ]
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        def put(name, value):
            io.open(os.path.join(d, name), "w", encoding="utf-8").write(doc % value)
        put("a.md", "true")      # census debt only       -> passes, listed
        put("b.md", "true")      # a real defect          -> fails
        put("c.md", "false")     # no findings            -> eligible, passes
        put("d.md", "dispositioned")
        by = {"a.md": [("UNLISTED CODE", "a.md", "002FE7D0", "")],
              "b.md": [("BODY DRIFT", "b.md", "00100000", "")]}
        fail, eligible, debt = check(d, by)
        checks += [
            ([f[0] for f in fail] == ["b.md", "d.md"], "fails exactly the defect and the malformed"),
            (eligible == ["c.md"], "false with nothing is eligible, not failed"),
            (debt == [("a.md", 1)], "census debt alone does not fail a true"),
        ]
    bad = [why for ok, why in checks if not ok]
    if bad:
        print("SELF-TEST FAILED: " + "; ".join(bad))
        return 1
    print("self-test ok: %d checks" % len(checks))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--report", help="JSON from audit_crossrefs.py --json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.db or not a.report:
        return ap.error("--db and --report required unless --self-test")
    if not os.path.isfile(a.report):
        print("REFUSED: no report at %s" % a.report)
        return 2

    rep_m = os.path.getmtime(a.report)
    newest = max((os.path.getmtime(p), p) for p in walk(a.db))
    if newest[0] > rep_m:
        print("REFUSED: the report is older than %s - re-run audit_crossrefs first"
              % os.path.relpath(newest[1], a.db))
        return 2

    rep = json.load(io.open(a.report, encoding="utf-8"))
    by = collections.defaultdict(list)
    kinds = collections.Counter()
    for row in rep.get("findings", ()):
        if len(row) >= 2:
            by[str(row[1]).replace(os.sep, "/")].append(row)
            kinds[row[0]] += 1
    print("report %s written %s: %d finding(s) over %d document(s)"
          % (os.path.basename(a.report),
             datetime.datetime.fromtimestamp(rep_m).strftime("%Y-%m-%d %H:%M"),
             sum(kinds.values()), len(by)))
    print("census-debt kinds excluded from the definition, by name: %s  (%s)"
          % (", ".join(CENSUS_DEBT_KINDS),
             ", ".join("%s %d" % (k, kinds[k]) for k in CENSUS_DEBT_KINDS)))

    fail, eligible, debt = check(a.db, by)
    if debt:
        print("\n`true` with census debt only - passes, listed so it stays visible (%d):" % len(debt))
        for rel, n in debt:
            print("  %s  (%d)" % (rel, n))
    print("\n`false` with no document-defect finding - ELIGIBLE to be raised, not a failure: %d"
          % len(eligible))
    if fail:
        print("\ncrossref_clean VIOLATES ITS DEFINITION (%d):" % len(fail))
        for rel, what in fail:
            print("  %-72s %s" % (rel, what))
        return 1
    print("\nevery crossref_clean satisfies its definition")
    return 0


if __name__ == "__main__":
    sys.exit(main())
