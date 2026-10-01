#!/usr/bin/env python3
"""check_coverage_dimensions.py - the committed coverage report against what the corpus produces.

`_index/COVERAGE-DIMENSIONS.md` is written by `program_coverage.py` and **nothing verified that the
committed file still matches what the generator produces.** Measured the day this file was written:

    authored functions cited anywhere in a system document   committed 8,992   current 11,580
    recorded only in a side file, explained by no document    committed 8,381   current  9,981

Nine points of citation coverage the corpus had earned and the canonical report did not say. That
is the same gap `ADDRESS-INDEX.md` had - a generator with no verifier - and it was found the same
way: by asking which OTHER canonical files could be destroyed by a bad run, after one was.

AND THE UNDERSTATEMENT IS THE HARMLESS DIRECTION. `program_coverage.py` would, given a `--db` that
does not exist, have written this same report with every numerator 0 and every denominator correct
- the prose unchanged, the percentages 0.00 % - over the canonical file at exit 0. That refusal is
now in the generator; this file closes the other half, because a report nobody re-runs is a report
nobody notices has drifted.

WHAT FAILS, AND WHY IT IS NOT A THRESHOLD. A tree eight agents publish into makes any generated file
stale within minutes, and a gate that failed on that would be red permanently and become wallpaper.
So the question is the one `check_address_index.py` settled: **does the report owe this figure yet?**

  NO DOCUMENT IS NEWER THAN THE REPORT    nothing has been published since it was written, so the
                                          figures must match exactly. Any difference FAILS.
  SOME DOCUMENT IS NEWER                  the corpus moved after the report was committed. The
                                          differences are the queue; they clear on the next
                                          regeneration. Reported, does not fail.

The remedy is one command either way: `program_coverage.py --db <db> --out <the file>`.

THE GENERATOR IS RUN, NOT RE-IMPLEMENTED, and its exit code is read: a refusal is exit 2 here, never
a verdict about the report. A comparison against a file the current run did not produce is not a
comparison - that lesson cost a control on a synthetic repository to learn.
"""
import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
REL = "_index/COVERAGE-DIMENSIONS.md"
# `| label | numerator | denominator | pct % |` - the four-column measured rows. Bold markers are
# part of the label and the number alike, so they are stripped rather than matched around.
ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*\**([\d,]+)\**\s*\|\s*\**([\d,]+)\**\s*\|", re.M)


def figures(text):
    """{label: (numerator, denominator)} for every measured row of the report."""
    out = {}
    for m in ROW.finditer(text):
        label = m.group(1).replace("**", "").replace("`", "").strip()
        if not label or label.startswith("---") or label.lower() in ("dimension", "measure"):
            continue
        try:
            out[label] = (int(m.group(2).replace(",", "")), int(m.group(3).replace(",", "")))
        except ValueError:
            continue
    return out


def git(db, *args):
    """git, with the ambient environment stripped - GIT_DIR answers about the wrong root."""
    env = dict(os.environ)
    for var in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE"):
        env.pop(var, None)
    try:
        r = subprocess.run(("git",) + args, cwd=db, capture_output=True, text=True,
                           timeout=180, env=env)
    except Exception:
        return None
    return r.stdout if r.returncode == 0 else None


def newer_than_report(db):
    """Documents committed since the report was. -> (count, one example, report time) or None."""
    t = git(db, "log", "-1", "--format=%ct", "--", REL)
    if not t or not t.strip().isdigit():
        return None
    when = int(t.strip())
    # `--since` on the commit AFTER the report's own, so the report's own commit never counts
    # itself - a publication that regenerates the report also touches documents.
    out = git(db, "log", "--since=@%d" % (when + 1), "--name-only", "--format=", "--", "*.md")
    if out is None:
        return None
    docs = {ln.strip() for ln in out.split("\n")
            if ln.strip().endswith(".md") and not ln.strip().endswith(REL)}
    return len(docs), (sorted(docs)[0] if docs else ""), when


def verdict(moved, gone, added, since):
    """The decision, as a pure function, so both branches can be proven without waiting for one.

    -> (exit code, key). `since` is (documents published since the report, example, when) or None.
    """
    if since is None:
        return 0, "cannot-time"
    if not (moved or gone or added):
        return 0, "matches"
    return (0, "queue") if since[0] else (1, "stale")


def self_test():
    """Both branches of the verdict, and the parser, without a live tree.

    THE FAIL BRANCH CANNOT BE OBSERVED ON DEMAND in a tree eight agents publish into - there is
    almost always a newer document - and a branch that is never exercised is a branch that is not
    known to work. So it is exercised here.
    """
    ok = True
    f = figures("| a | 1 | 2 | 50 % |\n| **b** | **3,000** | 4,000 | 75 % |\n| dimension | 1 | 2 |")
    want = {"a": (1, 2), "b": (3000, 4000)}
    if f != want:
        print("  FAILED parser: %r" % (f,))
        ok = False
    cases = [([("a", (1, 2), (3, 2))], [], [], (0, "", 1), 1, "stale"),
             ([("a", (1, 2), (3, 2))], [], [], (7, "x.md", 1), 0, "queue"),
             ([], [], [], (7, "x.md", 1), 0, "matches"),
             ([("a", (1, 2), (3, 2))], [], [], None, 0, "cannot-time")]
    for moved, gone, added, since, code, key in cases:
        got = verdict(moved, gone, added, since)
        if got != (code, key):
            print("  FAILED verdict %s: got %s, wanted %s" % (key, got, (code, key)))
            ok = False
    print("  self-test %s: the parser, and all four verdict branches including the one a live"
          % ("ok" if ok else "FAILED"))
    print("  tree will not show on demand - a difference with nothing published since FAILS.")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    committed_path = os.path.join(a.db, REL.replace("/", os.sep))
    if not os.path.isfile(committed_path):
        print("CANNOT RUN: no %s under %s" % (REL, a.db))
        return 2
    gen = os.path.join(KIT, "program_coverage.py")
    if not os.path.isfile(gen):
        print("CANNOT RUN: program_coverage.py is not in the kit")
        return 2

    tmpdir = tempfile.mkdtemp(prefix="coverage-dimensions-")
    try:
        tmp = os.path.join(tmpdir, "COVERAGE-DIMENSIONS.md")
        r = subprocess.run([sys.executable, gen, "--db", a.db, "--out", tmp],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("CANNOT RUN: program_coverage exited %d and wrote nothing to compare against."
                  % r.returncode)
            print((r.stdout + r.stderr)[-500:])
            return 2
        fresh = figures(io.open(tmp, encoding="utf-8", errors="replace").read())
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    have = figures(io.open(committed_path, encoding="utf-8", errors="replace").read())
    if not fresh:
        print("CANNOT RUN: the regenerated report parsed to no rows - its table shape has changed.")
        return 2

    moved = [(k, have[k], fresh[k]) for k in sorted(set(have) & set(fresh)) if have[k] != fresh[k]]
    gone = sorted(set(have) - set(fresh))
    added = sorted(set(fresh) - set(have))
    since = newer_than_report(a.db)

    print("THE COMMITTED COVERAGE REPORT, AGAINST WHAT THE CORPUS PRODUCES NOW\n")
    print("  rows compared : %d" % len(set(have) & set(fresh)))
    print("  figures that have moved : %d" % len(moved))
    for k, (hn, hd), (fn, fd) in moved[:12]:
        print("     %-58s %s/%s -> %s/%s" % (k[:58], hn, hd, fn, fd))
    if gone:
        print("  rows in the committed report the generator no longer produces : %d" % len(gone))
        for k in gone[:6]:
            print("     %s" % k[:74])
    if added:
        print("  rows the generator produces that the committed report does not have : %d"
              % len(added))
        for k in added[:6]:
            print("     %s" % k[:74])

    code, key = verdict(moved, gone, added, since)
    if key == "cannot-time":
        print("\n  git cannot say what has been published since the report was committed, so the")
        print("  age test cannot run. Reporting only - a figure that MIGHT be the queue is not")
        print("  evidence of a stale report.")
        return code
    ndocs, example, _when = since
    if key == "matches":
        print("\n  Every figure matches what the corpus produces now.")
        return code
    if key == "queue":
        print("\n  %d document(s) have been committed since this report was - the first of them"
              % ndocs)
        print("  %s" % example[:88])
        print("  so these differences are THE QUEUE, not a stale report. Eight agents publish into")
        print("  this tree; a generated file is stale minutes after it is written, and a gate that")
        print("  failed on that would be red permanently and become wallpaper. One command clears")
        print("  it: program_coverage.py --db <db> --out <the file>")
        return code
    print("\n  NOTHING HAS BEEN PUBLISHED SINCE THIS REPORT WAS COMMITTED, so the figures must")
    print("  match what the corpus produces and they do not. The canonical coverage report")
    print("  states numbers the scorer does not produce. One command:")
    print("    python program_coverage.py --db \"%s\" --out \"%s\"" % (a.db, committed_path))
    # THE DECISION IS MADE ONCE, in verdict(), and printed here. A tool that decides in two places
    # is the defect this kit keeps finding in itself: two sides of one comparison, given different
    # scopes, disagreeing silently.
    return code


if __name__ == "__main__":
    raise SystemExit(main())
