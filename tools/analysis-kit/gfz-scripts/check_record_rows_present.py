r"""check_record_rows_present.py [--rev REV] [--selftest] - every committed interior-citation record's rows are still on
its page (OPUS, 2026-10-03).

WHY. 890844135 applied an OPUS-drafted record (2 rows) to the Lua loader page. Its applier found the heading of the
section a different, already-published record had written (44 rows, 220 anchors, 047553008): the heading is the same
for every interior record of that mode and date. Its "re-render the block when it differs" path then rewrote that
section with its own 2 rows. 44 published rows vanished, every gate passed, and engine_explained silently lost them.
No check compared a published record with the page it claims to have written.

WHAT. For every record under _index/candidates/ whose rows.json AND interior_applier.py are tracked at REV (default
HEAD), and which is not marked "retired": each row's function must appear on the record's page (at REV) as a table
row `| \`FN\` |`, with every one of the row's anchors in that line. A record may give up rows only by declaring it:
rows.json "moved": {"FN": "reason / destination"} (a row moved to another page) or "retired": "reason".
Exit 1 on any missing row; the report names record, page, function and the anchors missing.
With --worktree, a committed record's rows.json may also not LOSE rows against HEAD (2026-10-03: interior_ingest
gave a second report for the same page and day the first record's folder name and would have overwritten its
published rows.json; the page check alone cannot see that, since it reads the overwritten file).

--selftest builds a two-record page in memory and requires the check to (1) pass when both blocks are present and
(2) fail when the second record's apply has rewritten the first's block (the 890844135 shape)."""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))     # XIIOnline/
DBP = "Database/FFXII TZA"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True)


def show(rev, path):
    if rev is None:
        p = os.path.join(REPO, *path.split("/"))
        return io.open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None
    r = git("show", "%s:%s" % (rev, path))
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def row_lines(text):
    out = {}
    for l in text.splitlines():
        m = re.match(r"\|\s*~*`([0-9A-Fa-f]{8})`", l)
        if m:
            out.setdefault(m.group(1).upper(), []).append(l)
    return out


def missing_rows(cfg, page_text):
    """[(fn, [missing anchors] or None when the function has no row at all)] for one record."""
    rows = row_lines(page_text)
    moved = {k.upper() for k in (cfg.get("moved") or {})}
    bad = []
    for r in cfg.get("rows") or []:
        if not isinstance(r, dict) or "fn" not in r:
            continue
        fn = r["fn"].upper()
        if fn in moved:
            continue
        anchors = [a[0] if isinstance(a, (list, tuple)) else a for a in r.get("anchors") or []]
        lines = rows.get(fn)
        if not lines:
            bad.append((fn, None))
            continue
        best = min(([a for a in anchors if a.upper() not in l.upper()] for l in lines), key=len)
        if best:
            bad.append((fn, best))
    return bad


def shrunk(head_raw, cfg):
    """Functions HEAD's rows.json carries that the worktree rows.json neither carries nor declares moved."""
    try:
        h = json.loads(head_raw) if head_raw else {}
    except ValueError:
        return []
    have = {r["fn"].upper() for r in cfg.get("rows") or [] if isinstance(r, dict) and "fn" in r}
    have |= {k.upper() for k in (cfg.get("moved") or {})}
    return sorted({r["fn"].upper() for r in (h.get("rows") or []) if isinstance(r, dict) and "fn" in r} - have)


def records(rev):
    if rev is None:
        r = git("ls-files", "-z", "--", DBP + "/_index/candidates")
    else:
        r = git("ls-tree", "-r", "-z", "--name-only", rev, "--", DBP + "/_index/candidates")
    files = set(q for q in r.stdout.decode("utf-8", "replace").split("\0") if q)
    for f in sorted(files):
        if f.endswith("/rows.json") and f[:-len("rows.json")] + "interior_applier.py" in files:
            yield f[:-len("/rows.json")]


def main(rev):
    total = recs = 0
    fails = []
    for d in records(rev):
        raw = show(rev, d + "/rows.json")
        try:
            cfg = json.loads(raw)
        except (TypeError, ValueError):
            continue
        if not isinstance(cfg, dict) or cfg.get("retired") or not cfg.get("page"):
            continue
        page = show(rev, DBP + "/" + cfg["page"])
        recs += 1
        total += len(cfg.get("rows") or [])
        if page is None:
            fails.append((d, cfg["page"], "PAGE MISSING", None))
            continue
        for fn, miss in missing_rows(cfg, page):
            fails.append((d, cfg["page"], fn, miss))
        if rev is None:
            for fn in shrunk(show("HEAD", d + "/rows.json"), cfg):
                fails.append((d, cfg["page"], fn, ["rows.json lost this row against HEAD"]))
    for d, pg, fn, miss in fails:
        print("MISSING %s | %s | %s | %s" % (d.split("/")[-1], pg, fn,
                                              "no row" if miss is None else "anchors " + ",".join(miss)))
    by = {}
    for d, *_ in fails:
        by[d] = by.get(d, 0) + 1
    print("records %d, rows %d, missing rows %d in %d records" % (recs, total, len(fails), len(by)))
    if not recs:
        # fail closed: a run that finds no record checked nothing (the first version did, from a wrong repo root)
        print("NO RECORDS FOUND - nothing was checked")
        return 1
    print("FAILS %d" % len(fails))
    return 1 if fails else 0


def selftest():
    a = {"page": "p.md", "rows": [{"fn": "00100000", "anchors": [["00100004", "mov"], ["00100010", "call"]]},
                                  {"fn": "00100100", "anchors": [["00100108", "lea"]]}]}
    b = {"page": "p.md", "rows": [{"fn": "00200000", "anchors": [["00200004", "jmp"]]}]}
    head = "## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)\n\n| function | size | w | a |\n|---|---|---|---|\n"
    rowa = "| `00100000` | 200 B | x | `00100004`, `00100010` |\n| `00100100` | 300 B | y | `00100108` |\n"
    rowb = "| `00200000` | 150 B | z | `00200004` |\n"
    both = "# P\n\n" + head + rowa + "\n" + head + rowb
    clobbered = "# P\n\n" + head + rowb            # the 890844135 shape: b re-rendered a's block
    partial = "# P\n\n" + head + rowa.replace("`00100010`", "") + "\n" + head + rowb
    bad = []
    if missing_rows(a, both) or missing_rows(b, both):
        bad.append("both present must pass")
    if [f for f, _ in missing_rows(a, clobbered)] != ["00100000", "00100100"]:
        bad.append("clobbered block must fail on both of a's rows")
    if missing_rows(a, partial) != [("00100000", ["00100010"])]:
        bad.append("a dropped anchor must be named")
    moved = dict(a, moved={"00100000": "to q.md", "00100100": "to q.md"})
    if missing_rows(moved, clobbered):
        bad.append("declared moves must pass")
    if shrunk(json.dumps(a), b) != ["00100000", "00100100"]:
        bad.append("a rows.json overwritten by another report must name the lost rows")
    if shrunk(json.dumps(a), a) or shrunk(json.dumps(a), moved):
        bad.append("an unchanged or move-declaring rows.json must not shrink")
    print("SELFTEST", "FAILED: " + "; ".join(bad) if bad else "ok (6 cases)")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rev = sys.argv[sys.argv.index("--rev") + 1] if "--rev" in sys.argv else "HEAD"
    if "--worktree" in sys.argv:
        rev = None
    sys.exit(main(rev))
