"""l2_verdict_table.py - the ONE reader of the L2-VERDICTS.md per-system table for every tool outside the reporter.

There is exactly one parser: `progress_report.parse_verdicts` / `progress_report._cell_verdict` (the reporter that writes
PROGRESS.md; the table found by its `| system | contract |` header, cells split on unescaped `|`, leading struck text
skipped, the controlled vocabulary N/A, NOT MET, SCOPE-SHORT, PARTIAL, MIXED, MET, LIVE, UNSCORED, PENDING, BLOCKED).
This module loads that parser from the repository's canonical copy and re-exports it, so goal_gate.py, readiness_view.py
and the dashboard (which reads the reporter's snapshot) cannot disagree with PROGRESS.md about a cell.

Why (SWE2-FRONTIER, 2026-10-03, OPUS-REQ-FRONTIER-ONE-VERDICT-PARSER-1003): four tools parsed the table independently.
progress_report read the STRUCK word of `~~MET~~ **SCOPE-SHORT**` (fixed by OPUS, T3s); goal_gate read it right only
because `~~` fails its `^MET`; readiness_view took the first S-id row ANYWHERE in the file and the word after its first
`|` - the contract column of the main table, or a cell of an earlier table - and reported 45 systems L2 MET against the
table's 31 (21 of 52 disagreed).

Usage: rows(path) -> [{system, name, contract, types, relationships, runtime, script_data, l2, gap, cell_text}]
       l2_by_system(path) -> {S-id: verdict word};  cell_verdict(cell) -> verdict word
       python l2_verdict_table.py --self-test"""
import importlib.util
import os
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTER = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "progress", "progress_report.py"))
_P = None


def reporter():
    """The reporter module (loaded once from its canonical path; never a copy)."""
    global _P
    if _P is None:
        spec = importlib.util.spec_from_file_location("_l2_progress_report", REPORTER)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _P = m
    return _P


def cell_verdict(cell):
    return reporter()._cell_verdict(cell)


def rows(path):
    return reporter().parse_verdicts(Path(path))


def malformed_rows(path):
    """S-ids whose verdict-table row has a different cell count from the table's header - an UNescaped `|` inside a cell
    widens the row, and a positional read would then take the wrong cell as the verdict. Such a system is dropped (reads
    unscored, fail-closed), as goal_gate's own width check did before this module (FABLE-CONTRA-GOAL-GATE-BITWISE-OR)."""
    import re
    split = reporter().CELL.split
    width, bad, seen = None, set(), set()
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(r"^\|\s*system\s*\|\s*contract\s*\|", line):
            width = len(split(line))
            continue
        if width is None:
            continue
        cells = [c.strip() for c in split(line)]
        if len(cells) >= 8 and re.match(r"(\*\*)?S-\d+", cells[1]):
            sid = re.sub(r"\*\*", "", cells[1]).split()[0]
            if sid not in seen and len(cells) != width:   # only the row l2_by_system would read (the first)
                bad.add(sid)
            seen.add(sid)
    return bad


def l2_by_system(path):
    """{S-id: L2 verdict word}; a row whose cell count disagrees with the header is left out (fail-closed)."""
    bad = malformed_rows(path)
    out = {}
    for r in rows(path):
        if r["system"] not in bad:
            out.setdefault(r["system"], r["l2"])
    return out


def _self_test():
    import tempfile
    fails = []

    def ok(c, m):
        print(("ok   " if c else "FAIL ") + m)
        if not c:
            fails.append(m)

    # T1 cell shapes: struck history never counts; the first word after it does
    for cell, want in (("**MET**", "MET"), ("~~MET~~ **SCOPE-SHORT - x**", "SCOPE-SHORT"),
                       ("~~**MET**~~ **NOT MET - y**", "NOT MET"), ("**NOT MET - z** Superseded: ~~**MET**~~", "NOT MET"),
                       ("MET - reason supplied", "MET"), ("N/A stated", "N/A"), ("", "UNSCORED")):
        ok(cell_verdict(cell) == want, "T1 %r -> %s" % (cell[:40], want))
    # T2 the table is found by its header; an S-id row in an EARLIER table is not read (readiness_view's old defect)
    doc = ("| system | contract scope | count |\n|---|---|--:|\n| **S-01** x | MET | 3 |\n\n"
           "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
           "|---|---|---|---|---|---|---|---|\n"
           "| **S-01** x | MET | MET | MET | MET | MET | ~~**MET**~~ **NOT MET - contract** | gap |\n"
           "| **S-02** y | ~~MET~~ **SCOPE-SHORT - s** | MET | MET | MET | MET | **MET** | none |\n")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "L2-VERDICTS.md")
        open(p, "w", encoding="utf-8").write(doc)
        l2 = l2_by_system(p)
        ok(l2 == {"S-01": "NOT MET", "S-02": "MET"}, "T2 L2 read from the verdict table only: %s" % l2)
        r = {x["system"]: x for x in rows(p)}
        ok(r["S-02"]["contract"] == "SCOPE-SHORT", "T3 a struck-and-corrected contract cell reads its new verdict")
        # T3b an UNescaped pipe widens the row: the system is dropped (fail-closed), an escaped one parses
        open(p, "w", encoding="utf-8").write(
            "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
            "| **S-48** x | MET | MET | MET | MET | MET | **MET** | gate `a|b` |\n"
            "| **S-49** y | MET | MET | MET | MET | MET | **MET** | gate `a\\|b` |\n")
        ok(l2_by_system(p) == {"S-49": "MET"}, "T3b raw pipe drops S-48 (fail-closed), escaped pipe keeps S-49: %s" % l2_by_system(p))
    # T4 every consumer agrees on the live table: goal_gate's NOT MET count and readiness_view's l2 equal the reporter's
    live = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "L2-VERDICTS.md"))
    if os.path.exists(live):
        rep = l2_by_system(live)
        sys.path.insert(0, HERE)
        import goal_gate
        okg, detail, _ = goal_gate.check_verdicts(os.path.dirname(os.path.dirname(live)), os.path.dirname(os.path.dirname(HERE)))
        n_unmet = sum(1 for v in rep.values() if v != "MET")
        ok(okg == (n_unmet == 0) and (n_unmet == 0 or detail.startswith("%d/" % n_unmet)),
           "T4 goal_gate agrees with the reporter (%d NOT MET): %s" % (n_unmet, detail))
        import readiness_view
        ok(readiness_view.l2_verdicts(os.path.dirname(os.path.dirname(live))) == rep,
           "T5 readiness_view's L2 equals the reporter's for all %d systems" % len(rep))
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    for s, v in sorted(l2_by_system(sys.argv[1]).items(), key=lambda kv: int(kv[0][2:])):
        print(s, v)
