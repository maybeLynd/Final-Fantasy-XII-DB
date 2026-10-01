"""Checked Git source lookup for the A23 release capture (SWE2-FRONTIER, 2026-09-30).

Repairs ASTRA-REQ-FRONTIER-A23-GIT-LOOKUP-ADMISSION: release.py's first headsha() took `git show` / `git log` stdout
and never read their exit codes, so a failed lookup (e.g. a missing -C directory: exits 128/128) came back as
SHA256(b"") and an empty commit - a normal-looking digest. Here every Git call's exit, stderr and stdout size are kept,
and the lookup is ok only when both calls exit 0 and the last-commit is a 40-hex id. A caller must test `ok` before
comparing digests; bind() does that and never reports equality for a failed lookup.
"""
import hashlib, re, subprocess

HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _git(repo, args):
    try:
        p = subprocess.run(["git", "-C", str(repo)] + args, capture_output=True)
        return {"argv": ["git", "-C", str(repo)] + args, "exit": p.returncode, "stdout": p.stdout,
                "stderr": p.stderr.decode("utf-8", "replace").strip()[-500:]}
    except OSError as e:   # git missing or not executable: a failure, never an empty success
        return {"argv": ["git", "-C", str(repo)] + args, "exit": None, "stdout": b"", "stderr": "%s: %s" % (type(e).__name__, e)}


def lookup(repo, rel, rev="HEAD"):
    """-> dict: ok, blob_sha256 (None unless ok), last_commit (None unless ok), why, and per-call receipts."""
    show = _git(repo, ["show", "%s:%s" % (rev, rel)])
    co = _git(repo, ["cat-file", "--filters", "%s:%s" % (rev, rel)])   # the bytes a checkout writes (eol filters)
    log = _git(repo, ["log", "-1", "--format=%H", rev, "--", rel])
    commit = log["stdout"].decode("ascii", "replace").strip()
    why = []
    if show["exit"] != 0:
        why.append("git show exit %s: %s" % (show["exit"], show["stderr"]))
    if co["exit"] != 0:
        why.append("git cat-file --filters exit %s: %s" % (co["exit"], co["stderr"]))
    if log["exit"] != 0:
        why.append("git log exit %s: %s" % (log["exit"], log["stderr"]))
    elif not HEX40.match(commit):
        why.append("git log named no commit for %s at %s" % (rel, rev))
    ok = not why
    rec = lambda c: {"argv": c["argv"], "exit": c["exit"], "stdout_bytes": len(c["stdout"]), "stderr": c["stderr"]}
    return {"ok": ok, "rel": rel, "rev": rev,
            "blob_sha256": hashlib.sha256(show["stdout"]).hexdigest() if ok else None,
            "checkout_sha256": hashlib.sha256(co["stdout"]).hexdigest() if ok else None,
            "last_commit": commit if ok else None, "why": "; ".join(why) or None,
            "calls": [rec(show), rec(co), rec(log)]}


def bind(repo, rel, recorded_sha256, rev="HEAD"):
    """Compare a recorded sha256 with the Git blob, raw or in its checkout (eol-filtered) form, and say which.
    equal is True/False only for a successful lookup, else None (INCOMPLETE) - a failed lookup can never read as a
    match or as a mismatch."""
    r = lookup(repo, rel, rev)
    r["recorded"] = recorded_sha256
    if not r["ok"]:
        r["equal"], r["state"] = None, "INCOMPLETE"
    elif not isinstance(recorded_sha256, str) or not recorded_sha256:
        r["equal"], r["state"] = None, "INCOMPLETE (no recorded hash)"
    elif recorded_sha256 == r["blob_sha256"]:
        r["equal"], r["state"] = True, "BOUND (raw blob)"
    elif recorded_sha256 == r["checkout_sha256"]:
        r["equal"], r["state"] = True, "BOUND (checkout form, eol-filtered)"
    else:
        r["equal"], r["state"] = False, "MISMATCH"
    return r
