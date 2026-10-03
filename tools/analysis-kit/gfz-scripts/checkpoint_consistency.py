"""checkpoint_consistency.py - is this checkpoint's current state self-consistent? (OPUS, 2026-10-03)

The user's directive item 7: a checkpoint must never contain a derived surface that claims CURRENT while its
authoritative dependency has moved (the 2026-10-03 defect: L2-VERDICTS.md 48/52 beside PROGRESS.md 52/52 `CURRENT`).
An explicit STALE is legal; a silent green is not. Each check below compares a current surface with its authoritative
source IN THE SAME TREE and prints PASS / STALE (declared, legal) / FAIL:

  C1 derived bindings      every GENERATION-BINDING.json is CURRENT or declared STALE (derived_binding.py), never
                           FALSE-CURRENT or INCOHERENT
  C2 unbound CURRENT       no tracked derived surface says "**freshness:** `CURRENT`" without a binding beside it
  C3 L2 headline           PROGRESS.md's "N MET of M systems" equals the L2-VERDICTS.md rows of the same tree
  C4 L2 summary blocks     every hand-kept count table in L2-VERDICTS.md ("| contract column | systems |") equals a
                           recount of its rows - a summary that disagrees with its rows is a false current surface
  C5 goal gate             (--worktree --slow) goal_gate.py's verdict and NOT MET count equal the rows and PROGRESS.md
  C6 knowledge mirror      (--worktree) knowledge_db.py check: CURRENT, or STALE reported (fail-closed by design)
  C7 lifecycle consumers   (--worktree) check_lifecycle_consumers.py FAILS 0
  C8 status residue        (--worktree) check_status_residue.py FAILS 0 / UNMAPPED 0

Usage: python checkpoint_consistency.py [--rev REV | --worktree] [--slow] [--refresh-mirror] [--json OUT]
Exit 0 when nothing FAILs (STALE allowed), 1 otherwise. --self-test runs the fixtures."""
import collections
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DBREL = "Database/FFXII TZA"
sys.path.insert(0, HERE)
import derived_binding as B  # noqa: E402

FRESH_CURRENT = re.compile(r"\*\*freshness:\*\* `CURRENT`")
HEADLINE = re.compile(r"\*\*(\d+) MET of (\d+) systems\*\*")


def _parse_verdicts(text):
    """The L2 table rows via progress_report.parse_verdicts (the generator's own parser, so C3 and C4 cannot disagree
    with the reporter about what a row says)."""
    sys.path.insert(0, os.path.join(ROOT, DBREL, "_index", "progress"))
    import progress_report as P
    import tempfile
    fd, p = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    try:
        io.open(p, "w", encoding="utf-8").write(text)
        from pathlib import Path
        return P.parse_verdicts(Path(p))
    finally:
        os.remove(p)


def summary_tables(text):
    """[(column, {verdict: count}, line_no)] for every '| <column> column | systems |' table in L2-VERDICTS.md."""
    out = []
    lines = text.splitlines()
    for i, l in enumerate(lines):
        m = re.match(r"^\|\s*(\w+) column\s*\|\s*systems\s*\|", l)
        if not m:
            continue
        counts = {}
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) < 2:
                continue
            verdict = re.sub(r"[*`]", "", cells[0]).strip()
            n = re.sub(r"[*`]", "", cells[1]).strip()
            if n.isdigit():
                counts[verdict] = int(n)
        out.append((m.group(1).lower(), counts, i + 1))
    return out


def run(rev=None, worktree=False, slow=False, refresh_mirror=False):
    res = []

    def add(cid, status, msg):
        res.append({"check": cid, "status": status, "detail": msg})

    read = B.worktree_reader(ROOT) if worktree else B.git_reader(ROOT, rev=rev or "HEAD")
    # C1
    paths = B.bindings_in(ROOT, rev=None if worktree else (rev or "HEAD"))
    if worktree:
        extra = subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--exclude-standard"], capture_output=True,
                               text=True).stdout.splitlines()
        paths = sorted(set(paths) | {p for p in extra if p.endswith("/" + B.NAME)})
    bound_dirs = set()
    for p in paths:
        data = read(p)
        if data is None:
            continue
        b = B.load(data)
        s = B.state(b, read)
        bound_dirs.add(os.path.dirname(p))
        st = {"CURRENT": "PASS", "STALE": "STALE"}.get(s["state"], "FAIL")
        add("C1", st, "%s %s%s%s" % (b["surface"], s["state"],
                                       (" moved: " + ", ".join(s["moved"])) if s["moved"] else "",
                                       (" outputs differ: " + ", ".join(s["outputs_bad"])) if s["outputs_bad"] else ""))
    if not paths:
        add("C1", "PASS", "no bindings in this tree")
    # C2
    if worktree:
        g = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-E", r"\*\*freshness:\*\* `CURRENT`", "--", DBREL],
                           capture_output=True, text=True)
    else:
        g = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-E", r"\*\*freshness:\*\* `CURRENT`", rev or "HEAD", "--",
                            DBREL], capture_output=True, text=True)
    unbound = []
    for line in g.stdout.splitlines():
        f = line.split(":", 1)[1] if (not worktree and ":" in line) else line
        d = os.path.dirname(f)
        covered = any(f == o or d == bd for bd in bound_dirs for o in [f])
        # a binding covers the files it names as outputs
        if not covered:
            for p in paths:
                data = read(p)
                if data and f in B.load(data)["outputs"]:
                    covered = True
        if not covered:
            unbound.append(f)
    add("C2", "FAIL" if unbound else "PASS",
        ("claims CURRENT with no binding: " + ", ".join(unbound)) if unbound else "every CURRENT claim is bound")
    # C3 / C4
    l2 = read(DBREL + "/_index/L2-VERDICTS.md")
    prog = read(DBREL + "/PROGRESS.md")
    rows = _parse_verdicts(l2.decode("utf-8")) if l2 else []
    met = sum(1 for r in rows if r["l2"] == "MET")
    if prog is not None and rows:
        ptxt = prog.decode("utf-8")
        m = HEADLINE.search(ptxt)
        stale = "`STALE`" in ptxt.split("\n", 6)[3] if ptxt.count("\n") > 3 else False
        if not m:
            add("C3", "FAIL", "PROGRESS.md has no 'N MET of M systems' headline")
        elif (int(m.group(1)), int(m.group(2))) == (met, len(rows)):
            add("C3", "PASS", "PROGRESS.md %s/%s = L2-VERDICTS rows %d/%d" % (m.group(1), m.group(2), met, len(rows)))
        else:
            add("C3", "STALE" if stale else "FAIL",
                "PROGRESS.md says %s MET of %s, the rows say %d of %d%s" % (
                    m.group(1), m.group(2), met, len(rows), " (labelled STALE)" if stale else " while labelled CURRENT"))
    if l2:
        text = l2.decode("utf-8")
        for col, counts, ln in summary_tables(text):
            if col not in ("contract", "types", "relationships", "runtime", "l2"):
                continue
            real = collections.Counter(r[col] for r in rows)
            bad = {k: (v, real.get(k, 0)) for k, v in counts.items() if real.get(k, 0) != v}
            add("C4", "FAIL" if bad else "PASS",
                ("L2-VERDICTS.md line %d '%s column' summary disagrees with its rows: %s" % (
                    ln, col, ", ".join("%s says %d, rows %d" % (k, a, b2) for k, (a, b2) in sorted(bad.items()))))
                if bad else "L2-VERDICTS.md line %d '%s column' summary equals its rows" % (ln, col))
    # C9 runtime exclusions are visible (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material",
    # 2026-10-03): a MET/LIVE runtime cell with exclusion wording must cite the amendment. Cells last scored before the
    # amendment (dated 2026-10-03 or earlier) are a visible worklist (STALE); a later cell without the citation FAILs.
    if l2:
        excl = re.compile(r"out of (the|this) (runtime )?denominator|outside the (L2 |runtime )?denominator|"
                          r"outside this contract's subject|out of this contract's runtime denominator|"
                          r"static-structure|ruled outside|unreachable from every disclosed|device-gated|"
                          r"not in the denominator|callee-depth|contract-excluded", re.I)
        sys.path.insert(0, os.path.join(ROOT, DBREL, "_index", "progress"))
        import progress_report as P
        late, old = [], []
        for line in l2.decode("utf-8").splitlines():
            m = re.match(r"^\| \*\*(S-\d+)\*\*", line)
            if not m or line.count("|") < 9:
                continue
            cell = line.split("|")[5]
            if P._cell_verdict(cell) not in ("MET", "LIVE") or not excl.search(cell):
                continue
            if "exclusion may not drop" in cell or "exclusion amendment" in cell:
                continue
            dates = re.findall(r"20\d\d-\d\d-\d\d", cell)
            (late if dates and max(dates) > "2026-10-03" else old).append(m.group(1))   # the amendment landed 2026-10-03
        if late:
            add("C9", "FAIL", "runtime cells scored since the exclusion amendment exclude material without citing it: "
                + ", ".join(sorted(set(late))))
        elif old:
            add("C9", "STALE", "runtime exclusions scored before the amendment, to be re-read against the registry "
                "subject: " + ", ".join(sorted(set(old))))
        else:
            add("C9", "PASS", "no runtime cell excludes material without citing the amendment")
    if not worktree:
        return res
    gfz = HERE

    def tool(args, timeout=900):
        r = subprocess.run([sys.executable, "-B"] + args, cwd=gfz, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)
    # C5
    if slow:
        rc, out = tool(["goal_gate.py", "--json"])
        try:
            gg = json.loads(out[out.index("{"):])
            nm = re.search(r"(\d+)/(\d+) systems NOT MET", gg.get("remaining", ""))
            ok = nm is None or (int(nm.group(1)), int(nm.group(2))) == (len(rows) - met, len(rows))
            add("C5", "PASS" if ok else "FAIL", "goal_gate %s (%s); rows NOT MET %d/%d" % (
                gg.get("verdict"), gg.get("remaining"), len(rows) - met, len(rows)))
        except Exception as e:
            add("C5", "FAIL", "goal_gate output unreadable: %s" % e)
    # C6 (with --refresh-mirror a STALE mirror is rebuilt through knowledge_db's own guarded build first: a checkpoint
    # refreshes the mirror instead of carrying a stale one forward; no second freshness system)
    rc, out = tool(["knowledge_db.py", "check"])
    if "STALE" in out and refresh_mirror:
        brc, bout = tool(["knowledge_db.py", "build"], timeout=1800)
        add("C6", "PASS" if brc == 0 else "FAIL", "knowledge.sqlite was STALE; rebuilt through the guarded build: %s" % (
            (bout.strip().splitlines() or ["no output"])[-1][:200]))
        rc, out = tool(["knowledge_db.py", "check"])
    if "STALE" in out:
        add("C6", "STALE", "knowledge.sqlite STALE (fails closed): " + "; ".join(
            l.strip() for l in out.splitlines() if "STALE" in l)[:300])
    elif rc == 0:
        add("C6", "PASS", "knowledge.sqlite CURRENT")
    else:
        add("C6", "FAIL", "knowledge_db check exit %d: %s" % (rc, out.strip()[-200:]))
    # C7 / C8
    for cid, script in (("C7", "check_lifecycle_consumers.py"), ("C8", "check_status_residue.py")):
        rc, out = tool([script])
        fails = re.search(r"FAILS (\d+)", out)
        good = rc == 0 and fails is not None and fails.group(1) == "0"
        add(cid, "PASS" if good else "FAIL", "%s: %s" % (script, (out.strip().splitlines() or ["no output"])[-1][:160]))
    return res


def _self_test():
    fails = []

    def ok(c, w):
        print(("ok   " if c else "FAIL ") + w)
        if not c:
            fails.append(w)
    t = ("| contract column | systems | which |\n|---|---:|---|\n| MET | **47** | x |\n| SCOPE-SHORT | **3** | y |\n"
         "\ntext\n")
    s = summary_tables(t)
    ok(s == [("contract", {"MET": 47, "SCOPE-SHORT": 3}, 1)], "summary table parsed: %s" % s)
    ok(HEADLINE.search("| **48 MET of 52 systems**; x").groups() == ("48", "52"), "PROGRESS headline parsed")
    ok(FRESH_CURRENT.search("· **freshness:** `CURRENT` (fp `x`)") is not None, "CURRENT claim detected")
    ok(FRESH_CURRENT.search("· **freshness:** `STALE` (bound inputs moved") is None, "STALE label is not a CURRENT claim")
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return _self_test()
    rev = argv[argv.index("--rev") + 1] if "--rev" in argv else None
    res = run(rev=rev, worktree="--worktree" in argv, slow="--slow" in argv,
              refresh_mirror="--refresh-mirror" in argv)
    for r in res:
        print("%-5s %-3s %s" % (r["status"], r["check"], r["detail"]))
    n = collections.Counter(r["status"] for r in res)
    print("CHECKPOINT %s: PASS %d, STALE %d, FAIL %d" % ("--worktree" if "--worktree" in argv else (rev or "HEAD"),
                                                        n["PASS"], n["STALE"], n["FAIL"]))
    if "--json" in argv:
        json.dump(res, io.open(argv[argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
