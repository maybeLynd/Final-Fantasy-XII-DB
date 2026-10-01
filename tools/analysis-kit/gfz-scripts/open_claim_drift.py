#!/usr/bin/env python3
"""open_claim_drift.py - report-only consumer-drift report.

FABLE-REQ-FRONTIER-STALE-OPEN-CLAIM-REPORT: consumers whose words still call a
question id open/unresolved while its OPEN-QUESTIONS row is ANSWERED/CLOSED are
live drift (the answer never reached them). Two FABLE scanners already exist:

  _index/candidates/contract-open-drift/contract_drift.py  (CONTRACT-*.md)
  _index/candidates/page-open-drift/page_open_drift.py     (every other .md)

This driver runs both, dedups their hits, and prints them. It NEVER refuses:
a hit can be a dated falsification sentence kept as history, or an id cited for
an unanswered sub-scope - every hit wants hand review, so this is a report, not
a gate. Wired in two places: `check_questions.py` (audit findings) and
`publish_paths.sh` (hits on files being published, printed as notes).

Usage:
  open_claim_drift.py [--root REPO] [--paths FILE ...] [--db-subtree REL]
"""
import argparse, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # repo root (…/XIIOnline)
DB = ROOT / "Database" / "FFXII TZA"
SCANNERS = [
    DB / "_index" / "candidates" / "contract-open-drift" / "contract_drift.py",
    DB / "_index" / "candidates" / "page-open-drift" / "page_open_drift.py",
]
# scanner line: "QID      status     relpath:lineno  text"
HIT = re.compile(r"^(\S+)\s+(\S+)\s+(.+?):(\d+)\s{2}(.*)$")


def drift_hits(root=ROOT, only_paths=None):
    """Run both scanners; return a deduped list of
    (qid, status, path, lineno, text). only_paths limits the report to hits
    inside those repo-relative files (publish-time filter); None = whole DB."""
    wanted = None
    if only_paths:
        # publish passes repo-relative paths; scanners report DB-relative
        # tails (last 55 chars), so suffix-match on the DB-relative form
        prefix = "Database/FFXII TZA/"
        wanted = set()
        for p in only_paths:
            w = str(Path(p).as_posix())
            wanted.add(w[len(prefix):] if w.startswith(prefix)
                       else os.path.basename(w))
    hits, seen = [], set()
    for scanner in SCANNERS:
        if not scanner.exists():
            # a missing scanner is not "no drift" - say so loudly, still rc 0
            hits.append(("SCANNER-MISSING", "", str(scanner), "", ""))
            continue
        r = subprocess.run([sys.executable, str(scanner)],
                           capture_output=True, text=True)
        for line in r.stdout.splitlines():
            m = HIT.match(line.strip())
            if not m:
                continue
            qid, st, rel, ln, text = m.groups()
            rel = rel.replace("\\", "/")
            if wanted is not None and not any(w.endswith(rel) for w in wanted):
                continue
            key = (qid, rel, ln)
            if key in seen:
                continue
            seen.add(key)
            hits.append((qid, st, rel, ln, text.strip()))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=None,
                    help="limit the report to hits in these repo-relative files")
    a = ap.parse_args()
    hits = drift_hits(only_paths=a.paths)
    for qid, st, rel, ln, text in hits:
        print("%-8s %-10s %s:%s  %s" % (qid, st, rel, ln, text[:110]))
    print("-- %d open-claim drift candidate(s) (report-only; hand review)" %
          len(hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
