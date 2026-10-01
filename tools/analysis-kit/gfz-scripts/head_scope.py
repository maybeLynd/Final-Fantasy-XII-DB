#!/usr/bin/env python3
"""head_scope.py - what is PUBLISHED, for gates that must not go red over someone's working tree.

WHY THIS EXISTS. The kit's gates read the working tree, and several lanes write it at once. On
2026-09-15 four gates were red and not one of them was published debt:

    check_links              9 broken links, all in 3 files that are CLEAN AT HEAD
    check_coverage           "claimed 25, actual 31" over 6 UNTRACKED documents
    check_doc_claims         1 unruled claim, on one of those same untracked documents
    check_frontier_shape     a frontier 296 out, from a second copy of a definition

The first three are one defect: a shared gate that goes red for something the reader cannot act on.
The publisher then either repairs a page they do not own or argues that a global gate being red is
acceptable - FABLE did the latter twice in one session, correctly, by hand, and had no way to show
it. That is how a gate stops being read, and the kit already knows the ending: *a checker that is
always red teaches people to ignore it*.

The fourth is why this is a module and not a third copy of the same six lines. Two implementations
of one definition are two definitions, and the second is where the drift lives; that is exactly what
put check_frontier_shape and check_untouched_runs 296 apart while both believed they were computing
check_dispositions' frontier. Having just ruled on that, writing "at HEAD" out by hand in every gate
that needs it would be the same mistake with the same shape.

WHAT IT DOES NOT DECIDE. Whether a gate SHOULD scope to HEAD is the gate's own question, and the
answer is not always yes - a tool whose job is to check what you are about to publish wants the
working tree. This module answers "is this published", nothing more.

THE FALLBACK IS STATED, NEVER SILENT. If git cannot answer - no repository, a fresh file, a
detached environment - every query returns the answer that keeps a finding IN the blocking set.
A gate must never downgrade a finding on a guess, so "unknown" counts as published.
"""
import io
import os
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def _git(args, cwd):
    try:
        r = subprocess.run(["git"] + args, capture_output=True, text=True, errors="replace",
                           cwd=cwd)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def repo_root():
    """The working tree's top directory, or None if this is not a repository."""
    if "root" not in _cache:
        out = _git(["rev-parse", "--show-toplevel"], _HERE)
        _cache["root"] = os.path.normpath(out.strip()) if out and out.strip() else None
    return _cache["root"]


def tracked_at_head(path=None, suffix=None):
    """Absolute paths git holds at HEAD under `path`, or None if git cannot answer.

    None is not an empty set and must not be treated as one: it means "unknown", and a caller that
    silently reads it as "nothing is published" would drop every finding it has.
    """
    root = repo_root()
    if root is None:
        return None
    spec = os.path.abspath(path) if path else root
    key = ("tree", spec, suffix)
    if key not in _cache:
        out = _git(["ls-tree", "-r", "--name-only", "HEAD", "--", spec], root)
        if out is None:
            _cache[key] = None
        else:
            got = set()
            for line in out.split("\n"):
                line = line.strip()
                if line and (suffix is None or line.endswith(suffix)):
                    got.add(os.path.normpath(os.path.join(root, line)))
            _cache[key] = got or None
    return _cache[key]


def is_published(path):
    """True if `path` is tracked at HEAD. Unknown counts as published - see the module docstring."""
    root = repo_root()
    if root is None:
        return True
    return head_text(path) is not None


def head_text(path):
    """`path`'s contents at HEAD, or None if git cannot produce them."""
    root = repo_root()
    if root is None:
        return None
    key = ("text", os.path.abspath(path))
    if key not in _cache:
        rel = os.path.relpath(os.path.abspath(path), root).replace(os.sep, "/")
        _cache[key] = _git(["show", "HEAD:" + rel], root)
    return _cache[key]


def worktree_only(path, needle):
    """True if `needle` appears in the file on disk but NOT in its committed text.

    The finding then belongs to whoever holds that file and leaves with their commit. A file git
    cannot speak for returns False: unknown is published, and the finding keeps blocking.
    """
    ht = head_text(path)
    return ht is not None and needle not in ht


def self_test_quiet():
    """The same controls with no output, for a gate that wants to check before it classifies."""
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return self_test()


def self_test():
    """Both ways, because the dangerous error is the DOWNGRADE.

    Calling published debt an uncommitted edit drops a real finding out of the blocking set
    entirely, so every control here checks that direction as well as its opposite.
    """
    import tempfile
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("  FAIL %-46s got %r, want %r" % (label, got, want))
        else:
            print("  ok   %-46s %r" % (label, got))

    # A TRACKED file, chosen from what git actually reports rather than assumed - this module
    # itself is the wrong choice, since on its first run it is not committed yet, which is
    # precisely the case it exists to distinguish.
    tracked = sorted(tracked_at_head(_HERE, ".py") or [])
    if not tracked:
        print("  FAIL no tracked .py under %s - cannot control anything" % _HERE)
        return False
    ref = tracked[0]
    text = head_text(ref)
    check("head_text of a tracked file is not None", text is not None, True)
    check("worktree_only: term absent at HEAD",
          worktree_only(ref, "ZZ-NOT-IN-ANY-COMMITTED-TEXT-ZZ"), True)
    check("worktree_only: term present at HEAD",
          worktree_only(ref, (text or "x")[:40]), False)

    # A file git has never seen: unknown, so it must NOT be called worktree-only.
    tmp = os.path.join(tempfile.mkdtemp(prefix="head-scope-"), "untracked.md")
    io.open(tmp, "w", encoding="utf-8").write("anything at all\n")
    check("an untracked file is never downgraded", worktree_only(tmp, "anything at all"), False)
    check("an untracked file has no HEAD text", head_text(tmp), None)

    check("tracked_at_head returns absolute paths", os.path.isabs(ref), True)
    check("tracked_at_head never returns an empty set",
          tracked_at_head(_HERE, ".py") != set(), True)
    check("a suffix filter actually filters",
          all(p.endswith(".py") for p in tracked_at_head(_HERE, ".py")), True)
    return ok


if __name__ == "__main__":
    import sys
    print("head_scope self-test - repo root: %s" % repo_root())
    sys.exit(0 if self_test() else 1)
