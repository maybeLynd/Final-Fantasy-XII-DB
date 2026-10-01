#!/usr/bin/env python3
"""check_generator_artifacts.py - code that leaked into prose.

Why this exists
---------------
On 2026-09-02 a session mixed `'''` and `\"\"\"` quoting conventions inside one patch script, and the
delimiters ended up **in the published document** -- a literal `''' + EM + u'''` sitting in the prose
of a live page.

**Every existing gate passed.** `check_links.py`, `verify_doc_addresses.py` and
`check_consistency.py` were all green with it there. They check links, addresses and cross-document
agreement; none of them looks at whether the text is text.

> **A generator that produced something other than what it meant to leaves no trace any
> content-level checker can see.**

It was caught by reading the rendered output, which does not scale and does not run in CI. This does.

The whole database is written by scripts appending markdown, so this is a permanent exposure rather
than one session's slip.

What it looks for
-----------------
Python and shell fragments that have no business in prose: triple quotes, `u'''`-style prefixed
literals, `+ VAR +` concatenation, unconsumed `%s`/`{}` format slots next to a `%` or `.format(`,
literal two-character `\\n` outside a code fence, and stray `\\x` escapes.

Code fences are skipped -- a document quoting a Python snippet is doing its job. So are the staging
inboxes, where a report *about* this defect legitimately contains examples of it.

Usage
-----
    python check_generator_artifacts.py --db "Database/FFXII TZA"
    python check_generator_artifacts.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

PATTERNS = [
    (re.compile(r"'''|\"\"\""),                    "python triple quote"),
    (re.compile(r"\b[urbf]{1,2}'''|\b[urbf]{1,2}\"\"\""), "prefixed python literal"),
    # `+ VAR +` needs an adjacent QUOTE to be concatenation.  Without that clause this fired on
    # "image-base + RVA + index, and absolute" -- ordinary prose describing an address computation.
    # The leak that motivated this check was `''' + EM + u'''`, and it is the delimiter that makes
    # it code.  **A pattern for "code in prose" that matches arithmetic has not understood the
    # difference between the two.**
    (re.compile(r"['\"]\s*\+\s+[A-Z_][A-Z0-9_]{1,20}\s+\+|"
                r"\+\s+[A-Z_][A-Z0-9_]{1,20}\s+\+\s*[urbf]{0,2}['\"]"),
     "string concatenation of a variable"),
    (re.compile(r"%[sd]'\s*%|\.format\(|\bf\"[^\"]*\{"), "unexpanded format call"),
    (re.compile(r"(?<!\\)\\n(?![a-zA-Z])"),        "literal backslash-n"),
    (re.compile(r"(?<!\\)\\x[0-9A-Fa-f]{2}"),      "literal hex escape"),
]

FENCE = re.compile(r"^\s*(```|~~~)")


def scan(text, rel, out):
    # A NUL byte in a markdown file is never intentional, and no pattern below can see one,
    # because by the time this runs the text has already been decoded.  On 2026-09-03 an
    # escaped NUL inside a C snippet became a real one through a shell heredoc, and the file
    # went from "UTF-8 text" to "data" -- which broke grep, sed and every text tool silently
    # while every content checker in this kit stayed green.
    #
    # **A checker built to find code in prose could not see a byte that is not prose at all.**
    #
    # And writing THIS check through a heredoc did it a second time, to this file, three
    # minutes later -- against a standing note that says to write escaped strings with an
    # editor and never through a shell heredoc.  **A rule that is written down and not wired
    # into the tooling is a rule you will break while fixing the thing it warned you about.**
    nul = chr(0)
    if nul in text:
        line_no = text.count(chr(10), 0, text.index(nul)) + 1
        out.append((rel, line_no, "NUL byte", "\\x00", "file is binary, not text"))
    fenced = False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue                       # a document quoting code is doing its job
        # Inline code spans are also legitimate quoting.
        stripped = re.sub(r"`[^`]*`", "", line)
        for pat, why in PATTERNS:
            m = pat.search(stripped)
            if m:
                out.append((rel, n, why, m.group(0), line.strip()))
                break


SELF_TEST_BAD = "The region is built at startup ''' + EM + u''' by the two hubs.\n"
SELF_TEST_OK = ("The region is built at startup by the two hubs.\n"
                "```python\n"
                "text = '''a triple-quoted block, legitimately quoted'''\n"
                "```\n"
                "And inline `'''` in a code span is fine too.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        bad, ok = [], []
        scan(SELF_TEST_BAD, "<bad>", bad)
        scan(SELF_TEST_OK, "<ok>", ok)
        if len(bad) != 1 or len(ok) != 0:
            print("SELF-TEST FAILED: bad=%d (want 1) ok=%d (want 0)" % (len(bad), len(ok)))
            return 1
        print("self-test ok: fires on the leaked delimiter, silent inside fences and code spans")
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    out = []
    for root, _d, files in os.walk(a.db):
        if "_inbox" in root.split(os.sep):
            continue                       # staging: a report about this defect contains examples
        for fn in files:
            if fn.endswith(".md"):
                p = os.path.join(root, fn)
                scan(io.open(p, encoding="utf-8", errors="replace").read(),
                     os.path.relpath(p, a.db), out)

    if not out:
        print("no generator artifacts in published prose")
        return 0

    print("CODE THAT LEAKED INTO PROSE")
    print("These are DEFECTS, not questions: the generator produced something other than")
    print("what it meant to, and no content-level checker can see it.\n")
    by = collections.defaultdict(list)
    for rel, n, why, frag, line in out:
        by[rel].append((n, why, frag, line))
    for rel in sorted(by):
        print("  %s" % rel)
        for n, why, frag, line in by[rel]:
            print("      line %d  [%s]  %r" % (n, why, frag))
            print("        %s" % line[:100])
        print()
    print("%d artifact(s) in %d document(s)" % (len(out), len(by)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
