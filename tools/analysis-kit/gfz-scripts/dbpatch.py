#!/usr/bin/env python3
"""Validate-then-commit editing for database documents.

Written after a real failure on 2026-09-02: an audit-log entry was written by one script
while the document patch it described aborted on a failed exact-match assert in another.
For a few minutes the log recorded a correction that did not exist. The log's own rule is
that an unrecorded audit did not happen; the converse is worse -- a *recorded* audit that
did not happen is a false claim in the permanent record.

The fix is ordering. Every edit is staged and every match validated BEFORE any file is
written, so a mismatch aborts the whole batch with nothing on disk changed.

Usage:

    from dbpatch import Batch
    b = Batch(r"...\\Database\\FFXII TZA")
    b.replace("09-.../doc.md", old_text, new_text)      # exact, must match exactly once
    b.append("09-.../doc.md", section_text)
    b.insert_after_line("_index/OPEN-QUESTIONS.md", r"^\\| V-10 \\|.*$", row)
    b.commit()                                           # validates all, then writes all

Nothing here is clever. It only guarantees that partial application cannot happen.
"""
import io
import os
import re


class Batch:
    def __init__(self, root):
        self.root = root
        self.ops = []

    def _path(self, rel):
        return os.path.join(self.root, rel.replace("/", os.sep))

    def replace(self, rel, old, new, count=1):
        self.ops.append(("replace", rel, old, new, count))
        return self

    def append(self, rel, text):
        self.ops.append(("append", rel, None, text, 0))
        return self

    def insert_after_line(self, rel, pattern, text):
        self.ops.append(("insert", rel, pattern, text, 0))
        return self

    def commit(self, verbose=True):
        # ---- phase 1: load, apply in memory, validate. No writes.
        bufs = {}
        problems = []
        for kind, rel, a, b, n in self.ops:
            p = self._path(rel)
            if rel not in bufs:
                try:
                    bufs[rel] = io.open(p, encoding="utf-8").read()
                except OSError as e:
                    problems.append(f"{rel}: cannot read ({e})")
                    continue
            t = bufs[rel]
            if kind == "replace":
                hits = t.count(a)
                if hits != n:
                    head = a.strip().split("\n")[0][:70]
                    problems.append(f"{rel}: expected {n} match(es), found {hits} for: {head!r}")
                    continue
                bufs[rel] = t.replace(a, b, n)
            elif kind == "append":
                bufs[rel] = t.rstrip() + "\n" + b
            elif kind == "insert":
                m = re.search(a, t, re.M)
                if not m:
                    problems.append(f"{rel}: no line matched {a!r}")
                    continue
                bufs[rel] = t[:m.end()] + b + t[m.end():]

        if problems:
            print("dbpatch: ABORTED, nothing written")
            for p in problems:
                print("   " + p)
            raise SystemExit(1)

        # ---- phase 2: commit. Every edit validated, so writes cannot be partial
        #      for match reasons. (Disk errors are still possible; nothing helps there.)
        for rel, text in bufs.items():
            io.open(self._path(rel), "w", encoding="utf-8", newline="\n").write(text)
        if verbose:
            print(f"dbpatch: committed {len(self.ops)} edit(s) across {len(bufs)} file(s)")
            for rel in bufs:
                print("   " + rel)
        return self
