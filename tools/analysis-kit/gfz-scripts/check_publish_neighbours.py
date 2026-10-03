#!/usr/bin/env python3
"""check_publish_neighbours.py - refuse a publish that raises UNACCOUNTED NEIGHBOUR.

FABLE's 2026-09-14 ruling, section 3, on `OPUS-REQ-FABLE-PASS22-TRIPWIRE-POLICY`:

    "The real mitigation is a pre-publish differential, the same shape as FABLE's publish.sh
     dispositions gate. Each publishing identity measures UNACCOUNTED NEIGHBOUR on HEAD and on HEAD
     plus its publish, and refuses a publish that raises the count. A streak can then be reset only
     by a regression that got past a guard, not by one note naming a far end. FABLE has run this
     measurement before every publish this session. It should become fleet practice. Owner of the
     shared script: the pass-22 tool's owner."

That owner is OPUS, and this is the script.

WHY IT IS NEEDED AT ALL
-----------------------
The terminal gate needs thirty CONSECUTIVE passing runs and a non-zero neighbour count on any run
resets the count. Forty pairs across twenty-two documents are held back from being findings by R6
alone: each becomes live the moment any document names its far-end subject outside a crossing
section. That is not hypothetical - it happened on 2026-09-14, to OPUS, between `60c846be` (16:14,
count 0) and `a1812431` (17:30, count 1), from one note.

WHAT MAKES THIS CHEAP, AND IT IS A PROPERTY OF THE AUDIT RATHER THAN A SHORTCUT
------------------------------------------------------------------------------
`audit_crossrefs` attributes every finding to the document whose citations produced it. A document's
cited set depends on that document alone, so **a publish can only add findings on the paths it
touches.** The guard therefore compares, for the published paths only, the findings this tree
produces against the findings HEAD produces - and a full second sweep of the corpus is not needed to
be sound.

HEAD is read through `git worktree add --detach`, which never touches the index, the working tree or
anybody else's staging. That matters on a shared tree: `git stash` would have been the obvious way
and it is exactly the wrong one here.

BOTH SIDES ARE WORKTREES, AND THAT IS THE 2026-09-14 FIX
--------------------------------------------------------
The first version measured the second side on the live working tree. Two identities reported the same
two consequences within eight minutes of each other (`FABLE-NOTICE-OPUS-NEIGHBOUR-GUARD-WORKTREE-SCOPE`,
`AUDITSPEC-REQ-OPUS-PUBGUARD-BATCH-SCOPE`):

1. **A peer's uncommitted edit refused somebody else's publish.** FABLE was refused over
   `battle-command-availability-and-reason-codes.md`, a page not in its batch. Filtering the verdict to
   the published paths - added later the same evening - fixes the *verdict*, but the measurement was
   still of a tree nobody controls, so the printed counts meant nothing and a peer's fix could be
   credited "accounted for by this publish". SWE2-AUDIT-SPEC saw exactly that credit appear.
2. **The audit wrote `_index/candidates/pass22-tripwires.tsv` into the shared tree** on every run, so a
   guard that exists to protect a publish was itself leaving a modified tracked file behind for the next
   agent to commit by accident.

Both follow from one thing, so one change answers both: the second side is now **HEAD plus the published
paths**, built in its own worktree, exactly as FABLE's `publish.sh` builds its dispositions export. The
guard now measures what this publish would produce and nothing else, and it writes only inside temp
directories it created. Alarm fatigue was the real hazard here - a guard that refuses on other people's
work teaches publishers to override it, which is worse than having no guard.

Usage:
    python check_publish_neighbours.py <path> [<path> ...]
    python check_publish_neighbours.py --self-test

Exit 0 when the publish adds no finding, 1 when it does, 2 on a usage or environment error.
"""
import argparse
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DB_REL = os.path.join("Database", "FFXII TZA")
GRAPH = os.path.join(ROOT, "Database", "Tools", "work", "graph")


def _load_audit():
    spec = importlib.util.spec_from_file_location(
        "ac_guard", os.path.join(HERE, "audit_crossrefs.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def findings(docs_dir, out_json):
    """Every finding the audit reports for a docs tree, as a set of (kind, doc, subject, detail)."""
    m = _load_audit()
    argv = ["audit_crossrefs.py",
            "--docs", docs_dir,
            "--functions", os.path.join(GRAPH, "functions.tsv"),
            "--edges", os.path.join(GRAPH, "edges.tsv"),
            "--json", out_json,
            "--out", out_json + ".md",
            "--quiet"]
    old = sys.argv
    sys.argv = argv
    try:
        m.main()
    finally:
        sys.argv = old
    d = json.load(io.open(out_json, encoding="utf-8"))
    return {tuple(str(x) for x in r[:4]) for r in d.get("findings", [])}


def neighbours(fset):
    return {f for f in fset if "NEIGHBOUR" in f[0].upper()}


def broken_links(docs_dir):
    """check_links --raw inside one of the guard's worktrees -> {(src, target)}.

    Raw mode because the publish side's paths are working-tree edits inside the worktree: the
    at-HEAD/working-tree split in check_links would file a link this publish breaks as not
    published debt, and the gate would pass a publish that broke it. The before/after diff below
    carries the classification instead. Links pointing outside the docs tree (the sparse side has
    no Tools checkout) break on BOTH sides equally and cancel in the diff. Pass-29 ask:
    OPUS-REQ-FRONTIER-PASS29-THIRTY-BROKEN-RELATIVE-LINKS, 2026-09-17.
    """
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_links.py"),
                        "--db", docs_dir, "--raw"], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        print("check_links --raw failed to run against %s: %s"
              % (docs_dir, (r.stderr or r.stdout).strip()[:200]), file=sys.stderr)
        return None
    return {tuple(l.split("\t")[1:3]) for l in r.stdout.splitlines()
            if l.startswith("BROKEN\t")}


def build_sides(rels, tmp):
    """Two detached HEAD worktrees; the second gets the published files copied over it.

    -> (wt_head, wt_publish, made) or (None, None, made) if git refused. `made` is what to remove.
    Nothing outside `tmp` is written, and nothing but `rels` crosses from the shared working tree.
    """
    wt_head = os.path.join(tmp, "head")
    wt_pub = os.path.join(tmp, "publish")
    made = []

    # RESOLVE HEAD ONCE. Two `worktree add ... HEAD` calls on a shared repository can land on
    # different commits, because a peer can commit in the seconds between them - observed on
    # 2026-09-14, one side at d4fbf73e and the other at 0bfac69d. The comparison would then be
    # measuring a peer's publish as well as this one, which is the very thing this guard exists to
    # stop doing.
    r = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
    if r.returncode:
        print("could not resolve HEAD: %s" % r.stderr.strip(), file=sys.stderr)
        return None, None, made
    head = r.stdout.strip()

    for wt in (wt_head, wt_pub):
        # SPARSE, BECAUSE A GUARD NOBODY RUNS IS NOT A GUARD. A full checkout is 7,283 files per
        # side and two sides made a run take tens of minutes; the audit reads nothing outside the
        # docs tree (`--functions` and `--edges` are read from the real repository, not the
        # worktree), so checking out anything else is pure cost. Cost is a correctness property
        # here: the reason the fleet was publishing without this measurement is that it was
        # expensive, and the one regression at HEAD today got in exactly that way.
        r = subprocess.run(["git", "-C", ROOT, "worktree", "add", "--no-checkout", "--detach",
                            wt, head], capture_output=True, text=True)
        if r.returncode:
            print("could not create a worktree at %s: %s" % (head[:8], r.stderr.strip()),
                  file=sys.stderr)
            return None, None, made
        made.append(wt)
        for cmd in (["sparse-checkout", "init", "--no-cone"],
                    ["sparse-checkout", "set", "--", DB_REL.replace(os.sep, "/") + "/*"],
                    ["checkout"]):
            # core.longpaths: the _experiments/evidence tree has paths past MAX_PATH under any temp
            # directory, and without it the checkout aborts (2026-10-02, OPUS).
            r = subprocess.run(["git", "-c", "core.longpaths=true", "-C", wt] + cmd, capture_output=True, text=True)
            if r.returncode:
                print("worktree %s: git %s failed: %s"
                      % (os.path.basename(wt), cmd[0], r.stderr.strip()), file=sys.stderr)
                return None, None, made
        # A PARTIAL CHECKOUT MUST NOT PASS FOR A CLEAN ONE. Long paths under a deep temp directory
        # make `git worktree add` skip files ("Filename too long") while still reporting progress;
        # a side missing documents would show every one of them as an added finding. Count what
        # landed against what the commit says should be there.
        want = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", head, "--", DB_REL],
                              capture_output=True, text=True).stdout.count("\n")
        got = sum(len(f) for _p, _d, f in os.walk(os.path.join(wt, DB_REL)))
        if want and got < want:
            print("worktree %s is INCOMPLETE: %d of %d files under %s. Re-run with a shorter temp "
                  "path (set TMP/TEMP); a partial side would report every missing document as a new "
                  "finding." % (os.path.basename(wt), got, want, DB_REL), file=sys.stderr)
            return None, None, made
    for src, rel in rels:
        dst = os.path.join(wt_pub, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    return wt_head, wt_pub, made


CACHE_DIR = os.path.join(ROOT, "Database", "Tools", "work", "graph", ".pass22-head-cache")


def head_key():
    """HEAD commit + the inputs the HEAD side depends on (function and edge tables, the audit and the link check)."""
    import hashlib
    r = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
    if r.returncode:
        return None
    h = hashlib.sha1(r.stdout.strip().encode())
    for f in (os.path.join(GRAPH, "functions.tsv"), os.path.join(GRAPH, "edges.tsv"),
              os.path.join(HERE, "audit_crossrefs.py"), os.path.join(HERE, "check_links.py")):
        try:
            st = os.stat(f)
            h.update(("%s:%d:%d" % (os.path.basename(f), st.st_size, int(st.st_mtime))).encode())
        except OSError:
            return None
    return h.hexdigest()


def head_cache_get(key):
    p = os.path.join(CACHE_DIR, key + ".json")
    try:
        d = json.load(io.open(p, encoding="utf-8"))
        return {tuple(x) for x in d["findings"]}, {tuple(x) for x in d["links"]}
    except (OSError, ValueError, KeyError):
        return None


def head_cache_put(key, fset, links):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        json.dump({"findings": sorted(fset), "links": sorted(links)},
                  io.open(os.path.join(CACHE_DIR, key + ".json"), "w", encoding="utf-8"))
    except OSError:
        pass


def build_head(tmp):
    """One detached sparse HEAD worktree (the publish side is the same worktree with the batch copied over it)."""
    made = []
    r = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
    if r.returncode:
        print("could not resolve HEAD: %s" % r.stderr.strip(), file=sys.stderr)
        return None, made
    head = r.stdout.strip()
    wt = os.path.join(tmp, "side")
    r = subprocess.run(["git", "-C", ROOT, "worktree", "add", "--no-checkout", "--detach", wt, head],
                       capture_output=True, text=True)
    if r.returncode:
        print("could not create a worktree at %s: %s" % (head[:8], r.stderr.strip()), file=sys.stderr)
        return None, made
    made.append(wt)
    for cmd in (["sparse-checkout", "init", "--no-cone"],
                ["sparse-checkout", "set", "--", DB_REL.replace(os.sep, "/") + "/*"],
                ["checkout"]):
        r = subprocess.run(["git", "-c", "core.longpaths=true", "-C", wt] + cmd, capture_output=True, text=True)
        if r.returncode:
            print("worktree: git %s failed: %s" % (cmd[0], r.stderr.strip()), file=sys.stderr)
            return None, made
    want = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", head, "--", DB_REL],
                          capture_output=True, text=True).stdout.count("\n")
    got = sum(len(f) for _p, _d, f in os.walk(os.path.join(wt, DB_REL)))
    if want and got < want:
        print("worktree is INCOMPLETE: %d of %d files under %s. Re-run with a shorter temp path (set TMP/TEMP)."
              % (got, want, DB_REL), file=sys.stderr)
        return None, made
    return wt, made


def remove_sides(made, tmp):
    for wt in made:
        subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", wt],
                       capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    # Removal can fail on a file another process still holds open, and then the worktree stays
    # REGISTERED in the shared repository even though this run is over. Pruning entries whose
    # directory is gone or broken keeps `git worktree list` honest for whoever looks next; it
    # touches nothing that still exists.
    subprocess.run(["git", "-C", ROOT, "worktree", "prune"], capture_output=True, text=True)
    # And SAY SO if one survived. Prune only forgets worktrees whose directory is gone, so a
    # directory another process still holds open stays registered and `git worktree list` quietly
    # grows a row per run. A named leftover is a thing somebody can delete; a silent one is not.
    left = [wt for wt in made if os.path.isdir(wt)]
    if left:
        print("note: %d guard worktree(s) could not be removed (a file was still open). They are "
              "inert copies of HEAD; delete them and run `git worktree prune`:" % len(left),
              file=sys.stderr)
        for wt in left:
            print("      %s" % wt, file=sys.stderr)


def resolve(paths):
    """-> (rels, error). Each entry is (absolute source, repo-relative posix path)."""
    rels = []
    for p in paths:
        src = p if os.path.isabs(p) else os.path.join(ROOT, p)
        if not os.path.isfile(src):
            return None, "not a file in this tree: %s" % p
        rel = os.path.relpath(src, ROOT)
        if rel.startswith(".."):
            return None, "outside the repository: %s" % p
        rels.append((src, rel.replace(os.sep, "/")))
    return rels, None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        # The guard's claim is that a publish can only add findings on the paths it touches, so the
        # self-test is about the COMPARISON, not about the audit: a finding present in both sets is
        # not a regression however bad it is, and a finding only in the new set is, even if the total
        # count is unchanged because something else was fixed in the same publish.
        was = {("UNACCOUNTED NEIGHBOUR", "a.md", "Audio", "5 edges"),
               ("UNLISTED CODE", "b.md", "002FE7D0", "census debt")}
        now = {("UNACCOUNTED NEIGHBOUR", "a.md", "Audio", "5 edges"),
               ("UNACCOUNTED NEIGHBOUR", "c.md", "UI", "2 edges")}
        added = neighbours(now) - neighbours(was)
        ok = (len(added) == 1 and list(added)[0][1] == "c.md"
              and not (neighbours(was) - neighbours(now)) & added)
        print("  comparison   %-4s  a pre-existing finding is not a regression, a new one is, and a "
              "net-zero count still fails" % ("ok" if ok else "FAIL"))

        # The isolation property, against the real repository. This is the one that was WRONG: the
        # second side used to be the live working tree, so a peer's uncommitted edit to any document
        # changed the measurement. Build the two sides for one published path and check that the
        # publish side carries the working-tree bytes for THAT path and HEAD's bytes for a dirty
        # path that is not in the batch.
        iso = None
        r = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--", DB_REL],
                           capture_output=True, text=True)
        dirty = [l[3:].strip().strip('"') for l in r.stdout.splitlines() if l[:2] != "??"]
        if len(dirty) >= 2:
            batch, outsider = dirty[0], dirty[1]
            tmp = tempfile.mkdtemp(prefix="pass22-guard-selftest-")
            made = []
            try:
                rels, err = resolve([batch])
                if err:
                    iso = "skipped - %s" % err
                else:
                    _h, wt_pub, made = build_sides(rels, tmp)
                    if wt_pub is None:
                        iso = "skipped - git refused a worktree"
                    else:
                        # Compare with line endings normalised on BOTH sides: a worktree checkout
                        # applies core.autocrlf, so the bytes on disk legitimately differ from what
                        # `git show` prints. Comparing raw here would report a failure that is only
                        # the checkout doing its job.
                        def body(path):
                            return io.open(path, "rb").read().replace(b"\r\n", b"\n")

                        in_batch = (body(os.path.join(wt_pub, batch.replace("/", os.sep)))
                                    == body(os.path.join(ROOT, batch.replace("/", os.sep))))
                        out = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + outsider],
                                             capture_output=True)
                        left = body(os.path.join(wt_pub, outsider.replace("/", os.sep)))
                        at_head = (left == out.stdout.replace(b"\r\n", b"\n"))
                        iso = ("ok" if (in_batch and at_head) else
                               "FAIL (batch carried=%s outsider at HEAD=%s)" % (in_batch, at_head))
                        ok = ok and in_batch and at_head
            finally:
                remove_sides(made, tmp)
        else:
            iso = "skipped - needs two modified documents in the tree to be meaningful"
        print("  isolation    %-4s  the publish side is HEAD + the batch, and a dirty document "
              "outside the batch stays at HEAD" % iso)
        print("self-test: %s" % ("pass" if ok else "FAIL"))
        return 0 if ok else 1

    if not a.paths:
        print("usage: check_publish_neighbours.py <path> [<path> ...]", file=sys.stderr)
        return 2

    # Resolve the published paths before anything is built, so a typo fails here rather than after
    # six minutes of auditing.
    rels, err = resolve(a.paths)
    if err:
        print(err, file=sys.stderr)
        return 2

    tmp = tempfile.mkdtemp(prefix="pass22-guard-")
    made = []
    try:
        # The second side is HEAD + this publish. Nothing else from the shared tree crosses over,
        # so a peer's in-flight edit can neither refuse this publish nor be credited to it.
        # 2026-10-03 (OPUS, the script's owner): one worktree instead of two, and the HEAD side cached by
        # everything it depends on. The HEAD audit + link check are computed once per HEAD commit; the published
        # files are then copied over the same worktree for the second side. Each side still runs the full audit,
        # so the comparison is unchanged; only the duplicate checkout and the repeated HEAD run are gone.
        key = head_key()
        cached = head_cache_get(key) if key else None
        wt, made = build_head(tmp)
        if wt is None:
            return 2
        if cached is not None:
            before, links_before = cached
            print("HEAD side from cache (%s)" % key[:12])
        else:
            before = findings(os.path.join(wt, DB_REL), os.path.join(tmp, "head.json"))
            links_before = broken_links(os.path.join(wt, DB_REL))
            if key and links_before is not None:
                head_cache_put(key, before, links_before)
        for src, rel in rels:
            dst = os.path.join(wt, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        after = findings(os.path.join(wt, DB_REL), os.path.join(tmp, "publish.json"))
        links_after = broken_links(os.path.join(wt, DB_REL))
    finally:
        remove_sides(made, tmp)
    if links_before is None or links_after is None:
        return 2

    added = neighbours(after) - neighbours(before)
    gone = neighbours(before) - neighbours(after)
    # Both sides are now HEAD-derived, so a difference can only come from the published paths and this
    # filter should be a no-op. It is kept as an assertion rather than a fix: if it ever drops a
    # finding, the two sides diverged somewhere they should not have, and that is worth knowing.
    mine = set()
    for _src, rel in rels:
        sub = os.path.relpath(os.path.join(ROOT, rel), os.path.join(ROOT, DB_REL))
        mine.add(sub.replace(os.sep, "/"))
    stray = {f for f in (added | gone) if f[1] not in mine}
    added = {f for f in added if f[1] in mine}
    gone = {f for f in gone if f[1] in mine}
    print("UNACCOUNTED NEIGHBOUR   HEAD %d   HEAD+publish %d   (%d path(s) in the batch)"
          % (len(neighbours(before)), len(neighbours(after)), len(mine)))
    if stray:
        print("\n  NOTE - %d finding(s) moved on a document outside the batch. Both sides are HEAD"
              "\n  plus these paths, so this should be impossible; report it rather than ignore it:"
              % len(stray))
        for f in sorted(stray):
            print("     %s :: %s" % (f[1], f[2]))
    if gone:
        print("\n  accounted for by this publish: %d" % len(gone))
        for f in sorted(gone):
            print("     %s :: %s" % (f[1], f[2]))
    # pass 29: a publish must not land broken relative links either. Same added/gone semantics as
    # the neighbour findings - a break standing at HEAD is not this publish's to answer, one the
    # publish introduces on a path it touches is.
    links_added = links_after - links_before
    links_gone = {b for b in links_before - links_after if b[0] in mine}
    if links_gone:
        print("\n  links repaired by this publish: %d" % len(links_gone))
    if links_added:
        print("\n  REFUSE - this publish breaks %d relative link(s):" % len(links_added))
        for src, tgt in sorted(links_added):
            print("     %s -> %s" % (src, tgt))
        print("\n  The number of `../` is the page's own depth - check_links.py computes the fix.")
        return 1
    if not added:
        print("\n  ADDS NOTHING. A finding already standing at HEAD is not this publish's to answer.")
        return 0
    print("\n  REFUSE - this publish ADDS %d unaccounted neighbour(s):" % len(added))
    for f in sorted(added):
        print("     %s\n        %s -- %s" % (f[1], f[2], f[3][:150]))
    print("\n  Either account for the crossing in the same edit - a section-4.2 sentence naming the")
    print("  edge and its relationship class - or do not name the far-end address outside its")
    print("  crossing section. FABLE 2026-09-14 section 3: naming one MUST add the sentence in the")
    print("  same edit.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
