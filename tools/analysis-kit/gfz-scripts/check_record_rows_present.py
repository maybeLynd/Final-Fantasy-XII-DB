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


def moved_fns(cfg):
    """Functions a record declares moved: {"FN": "why"} (OPUS form) or [{"fn": ...}, ...] / ["FN", ...] (FABLE form)."""
    m = cfg.get("moved") or {}
    if isinstance(m, dict):
        return {k.upper() for k in m}
    out = set()
    for x in m if isinstance(m, list) else []:
        f = x.get("fn") if isinstance(x, dict) else x
        if isinstance(f, str):
            out.add(f.upper())
    return out


def missing_rows(cfg, page_text):
    """[(fn, [missing anchors] or None when the function has no row at all)] for one record."""
    rows = row_lines(page_text)
    moved = moved_fns(cfg)
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
    have |= moved_fns(cfg)
    return sorted({r["fn"].upper() for r in (h.get("rows") or []) if isinstance(r, dict) and "fn" in r} - have)


def records(rev):
    if rev is None:
        r = git("ls-files", "-z", "--", DBP + "/_index/candidates")
    else:
        r = git("ls-tree", "-r", "-z", "--name-only", rev, "--", DBP + "/_index/candidates")
    files = set(q for q in r.stdout.decode("utf-8", "replace").split("\0") if q)
    # 2026-10-03 (hardening item 6): a record is any candidates/*/rows.json whose CONTENT has the record shape (checked
    # by is_record), whatever its applier is called - FABLE's 80 homing_applier.py records were invisible to the old
    # "rows.json + interior_applier.py" rule.
    for f in sorted(files):
        if f.endswith("/rows.json") and f.count("/") == DBP.count("/") + 4:
            yield f[:-len("/rows.json")]


def is_record(cfg):
    return (isinstance(cfg, dict) and isinstance(cfg.get("page"), str) and isinstance(cfg.get("rows"), list)
            and any(isinstance(r, dict) and "fn" in r for r in cfg["rows"]))


def _batch_read(root, env, specs):
    """{spec: bytes or None} for 'REV:path' / ':path' specs through one git cat-file --batch."""
    out = {}
    if not specs:
        return out
    r = subprocess.run(["git", "-C", root, "cat-file", "--batch"], input="".join(x + "\n" for x in specs).encode("utf-8"),
                       capture_output=True, env=env)
    data, i = r.stdout, 0
    for spec in specs:
        nl = data.index(b"\n", i)
        head = data[i:nl].decode("utf-8", "replace").split()
        i = nl + 1
        if len(head) == 3 and head[1] == "blob":
            n = int(head[2])
            out[spec] = data[i:i + n]
            i += n + 1
        else:
            out[spec] = None
    return out


def check_index(root, index_file, base, paths):
    """PUBLICATION-BOUNDARY mode (publish_paths.sh, every lane): the commit about to be made is `index_file` over
    `base`. Every record whose rows.json or page is among `paths` must, in the index, still carry each row on its page
    and must not have lost rows against `base` - unless the loss is declared ("moved" rows, or the record "retired").
    -> list of (record, page, fn, why)."""
    env = dict(os.environ, GIT_INDEX_FILE=index_file)
    touched = {x.replace(os.sep, "/") for x in paths}
    ls = subprocess.run(["git", "-C", root, "ls-files", "-z", "--", DBP + "/_index/candidates"], capture_output=True,
                        env=env).stdout.decode("utf-8", "replace").split("\0")
    rjs = [f for f in ls if f.endswith("/rows.json") and f.count("/") == DBP.count("/") + 4]
    now = _batch_read(root, env, [":" + f for f in rjs])
    cfgs = {}
    for f in rjs:
        try:
            c = json.loads(now[":" + f]) if now[":" + f] is not None else None
        except ValueError:
            c = None
        if is_record(c):
            cfgs[f] = c
    # records this publish can affect: its rows.json is published, or its page is
    hit = {f: c for f, c in cfgs.items() if f in touched or (DBP + "/" + c["page"]) in touched}
    # a published rows.json that no longer has the record shape (overwritten with garbage) is itself a loss
    for f in rjs:
        if f in touched and f not in cfgs:
            hit[f] = None
    pages = sorted({DBP + "/" + c["page"] for c in hit.values() if c})
    blobs = _batch_read(root, env, [":" + p for p in pages] + ["%s:%s" % (base, f) for f in hit])
    fails = []
    for f, c in sorted(hit.items()):
        rec = f.split("/")[-2]
        before_raw = blobs.get("%s:%s" % (base, f))
        try:
            before = json.loads(before_raw) if before_raw else None
        except ValueError:
            before = None
        if c is None:
            if is_record(before) and not before.get("retired"):
                fails.append((rec, "?", "*", "rows.json no longer has the record shape (overwritten?)"))
            continue
        if c.get("retired"):
            continue
        page = blobs.get(":" + DBP + "/" + c["page"])
        if page is None:
            fails.append((rec, c["page"], "*", "page missing from the commit"))
            continue
        for fn, miss in missing_rows(c, page.decode("utf-8", "replace")):
            fails.append((rec, c["page"], fn, "no row on the page" if miss is None else "anchors missing: " + ",".join(miss)))
        for fn in shrunk(before_raw.decode("utf-8", "replace") if before_raw else None, c):
            fails.append((rec, c["page"], fn, "rows.json lost this row against %s" % base[:12]))
    return fails


def main_index(index_file, base, paths):
    fails = check_index(REPO, index_file, base, paths)
    for rec, page, fn, why in fails:
        print("ROW-LOSS %s | %s | %s | %s" % (rec, page, fn, why))
    print("publication boundary: %d row loss(es) in the records this commit touches" % len(fails))
    print("FAILS %d" % len(fails))
    return 1 if fails else 0


def scenario_test():
    """The six publication-boundary scenarios in a throwaway git repository, through a real private index."""
    import shutil, tempfile
    bad = []
    d = tempfile.mkdtemp()
    try:
        def g(*a, env=None):
            return subprocess.run(["git", "-C", d] + list(a), capture_output=True, env=env)
        g("init", "-q")
        g("config", "user.email", "t@t")
        g("config", "user.name", "t")
        g("config", "core.autocrlf", "false")
        cand = os.path.join(d, *DBP.split("/"), "_index", "candidates")
        page_rel = "Area/p.md"
        page_abs = os.path.join(d, *DBP.split("/"), *page_rel.split("/"))
        os.makedirs(os.path.dirname(page_abs))

        def rec(name, fns, extra=None):
            c = {"page": page_rel, "rows": [{"fn": f, "anchors": [["%08X" % (int(f, 16) + 4), "nop"]]} for f in fns]}
            c.update(extra or {})
            os.makedirs(os.path.join(cand, name), exist_ok=True)
            io.open(os.path.join(cand, name, "rows.json"), "w").write(json.dumps(c))

        def row(f):
            return "| `%s` | 9 B | x | `%08X` |\n" % (f, int(f, 16) + 4)
        rec("opus-a-1003", ["00100000", "00100100"])
        rec("fable-b-1003", ["00200000"])
        io.open(page_abs, "w").write("# P\n\n" + row("00100000") + row("00100100") + "\n" + row("00200000"))
        g("add", "-A")
        g("commit", "-q", "-m", "base")
        base = g("rev-parse", "HEAD").stdout.decode().strip()
        idx = os.path.join(d, "priv.idx")

        def publish(files):
            """stage `files` {repo-relative: text} into a fresh private index over base; -> check_index fails"""
            if os.path.exists(idx):
                os.remove(idx)
            env = dict(os.environ, GIT_INDEX_FILE=idx)
            g("read-tree", base, env=env)
            for rel, text in files.items():
                ab = os.path.join(d, *rel.split("/"))
                os.makedirs(os.path.dirname(ab), exist_ok=True)
                io.open(ab, "w").write(text)
                g("add", "--", rel, env=env)
            out = check_index(d, idx, base, list(files))
            g("checkout", "-q", base, "--", ".")            # restore the worktree for the next scenario
            return out
        P = DBP + "/" + page_rel
        full = "# P\n\n" + row("00100000") + row("00100100") + "\n" + row("00200000")
        cases = [
            ("OPUS publish adding a row keeps every row", {P: full + row("00100200")}, False),
            ("second lane (FABLE) publish dropping OPUS rows from the shared page", {P: "# P\n\n" + row("00200000")}, True),
            ("later same-heading record re-rendering the earlier section",
             {P: "# P\n\n" + row("00300000") + "\n" + row("00200000"),
              DBP + "/_index/candidates/opus-c-1003/rows.json": json.dumps(
                  {"page": page_rel, "rows": [{"fn": "00300000", "anchors": [["00300004", "nop"]]}]})}, True),
            ("overwritten rows.json (another report's rows in the folder)",
             {DBP + "/_index/candidates/opus-a-1003/rows.json": json.dumps(
                 {"page": page_rel, "rows": [{"fn": "00100000", "anchors": [["00100004", "nop"]]}]})}, True),
            ("legitimate explicit move: the row is declared moved and leaves the page",
             {P: "# P\n\n" + row("00100000") + "\n" + row("00200000"),
              DBP + "/_index/candidates/opus-a-1003/rows.json": json.dumps(
                  {"page": page_rel, "moved": {"00100100": "to q.md"},
                   "rows": [{"fn": "00100000", "anchors": [["00100004", "nop"]]},
                            {"fn": "00100100", "anchors": [["00100104", "nop"]]}]})}, False),
            ("legitimate retirement: the record is retired and its rows leave the page",
             {P: "# P\n\n" + row("00200000"),
              DBP + "/_index/candidates/opus-a-1003/rows.json": json.dumps(
                  {"page": page_rel, "retired": "superseded by opus-z", "rows": [
                      {"fn": "00100000", "anchors": [["00100004", "nop"]]}]})}, False),
        ]
        for name, files, want_fail in cases:
            got = publish(files)
            if bool(got) != want_fail:
                bad.append("%s: expected %s, got %s" % (name, "FAIL" if want_fail else "PASS", got))
            print("%s %s" % ("ok  " if bool(got) == want_fail else "FAIL", name))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return bad


def main(rev):
    total = recs = 0
    fails = []
    for d in records(rev):
        raw = show(rev, d + "/rows.json")
        try:
            cfg = json.loads(raw)
        except (TypeError, ValueError):
            continue
        if not is_record(cfg) or cfg.get("retired"):
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
        rc = selftest()
        sc = scenario_test()
        print("SCENARIOS", "FAILED: " + "; ".join(sc) if sc else "ok (6 publication-boundary scenarios)")
        sys.exit(rc or (1 if sc else 0))
    if "--index" in sys.argv:
        a = sys.argv
        sys.exit(main_index(a[a.index("--index") + 1], a[a.index("--base") + 1], a[a.index("--paths") + 1:]))
    rev = sys.argv[sys.argv.index("--rev") + 1] if "--rev" in sys.argv else "HEAD"
    if "--worktree" in sys.argv:
        rev = None
    sys.exit(main(rev))
