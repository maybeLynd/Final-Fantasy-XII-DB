#!/usr/bin/env python3
"""check_duplicate_sections.py - a section published more than once into the same document.

**A RETRIED PUBLICATION CAN APPEND THE SAME SECTION AGAIN.** On 2026-09-19 I appended one section to
`19-Save-Load-Settings/CONTRACT-save-image-buffers.md` and then re-ran the publish loop while
`@publication` was held by a peer. Each pass that got far enough re-appended it. The file ended with
**six byte-identical copies** of that section and of the roster section sharing its block - **25,520
bytes of duplication in a 75,504-byte file** - and nothing noticed, because every heading, address
and claim in it was correct. Duplication is invisible to every other check in this kit: the content
is right, there is simply more of it.

**It is not harmless.** A duplicated section inflates any census that counts sections or bytes, and a
reader who corrects one copy leaves the others standing - which is how a corrected claim silently
survives in the same file that corrects it.

THE TEST. Split each document on `^## `, keep sections of at least `--min-bytes`, and report any that
appear byte-identically more than once.

**`_index/_inbox` IS EXCLUDED, and that exclusion is the whole difficulty.** Inbox logs are
append-only reports in which `## COVERAGE`, `## AUDIT-LOG` and `## STATUS` recur once per entry -
`repos-78.md` has forty `## COVERAGE` headings and not one is a defect. The first version of this
check flagged 56 files and every top hit was an inbox log. Comparing **bodies** rather than headings
and skipping `_inbox` leaves the real class.

    python check_duplicate_sections.py --self-test
    python check_duplicate_sections.py
"""
import argparse
import collections
import io
import os
import re
import sys

import kit_paths as KP

SPLIT = re.compile(r"^## ", re.M)


def duplicates(text, min_bytes):
    """{section: count} for sections repeated byte-identically."""
    idx = [m.start() for m in SPLIT.finditer(text)]
    secs = []
    for i, s in enumerate(idx):
        e = idx[i + 1] if i + 1 < len(idx) else len(text)
        secs.append(text[s:e].rstrip())
    c = collections.Counter(s for s in secs if len(s) >= min_bytes)
    return {k: v for k, v in c.items() if v > 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--min-bytes", type=int, default=400)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        # A positive control from the repository's own history, so the zero below means something.
        ok = True
        good = "## A\n" + "x" * 500 + "\n## B\n" + "y" * 500 + "\n"
        bad = good + "## A\n" + "x" * 500 + "\n"
        for label, text, want in (("a document with no repeat", good, 0),
                                  ("the same section appended twice", bad, 1)):
            got = len(duplicates(text, a.min_bytes))
            fine = got == want
            ok = ok and fine
            print("  %-40s dup=%d  %s" % (label, got, "ok" if fine else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    hits, docs = [], 0
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if "_inbox" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            docs += 1
            t = io.open(p, encoding="utf-8", errors="replace").read()
            dup = duplicates(t, a.min_bytes)
            if dup:
                waste = sum(len(k) * (v - 1) for k, v in dup.items())
                hits.append((os.path.relpath(p, a.db), len(dup), max(dup.values()), waste, len(t)))

    hits.sort(key=lambda x: -x[3])
    print("documents scanned (excluding _inbox) : %d" % docs)
    print("with a byte-identical repeated section: %d" % len(hits))
    print()
    if not hits:
        print("  none")
    else:
        print("  %-58s %5s %5s %9s" % ("file", "dups", "max", "wasted"))
        for p, nd, mx, w, ln in hits[:30]:
            print("  %-58s %5d %5d %9d" % (p[:58], nd, mx, w))
    print()
    print("EXCLUDES `_index/_inbox`, where repeated `## COVERAGE` and `## AUDIT-LOG` headings are the")
    print("shape of an append-only log rather than a defect - 40 in one file, none of them wrong.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
