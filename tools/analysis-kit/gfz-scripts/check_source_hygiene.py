#!/usr/bin/env python3
"""check_source_hygiene.py - stray control bytes in scripts and documents.

Why this exists
---------------
A standing note in this project says: **write escaped strings with an editor, never through a shell
heredoc.** On 2026-09-03 that note was broken three times in one session:

  1. An escaped NUL inside a C snippet became a real NUL through a heredoc, and two documents went
     from "UTF-8 text" to "data" -- breaking grep, sed and every text tool **silently**, while every
     content checker stayed green.
  2. The check written to catch that was itself written through a heredoc, three minutes later, and
     acquired a NUL of its own.
  3. A regex patched through a heredoc had its `\\b` turned into a literal **backspace byte**. The
     pattern became `\\x08(0[0-9A-Fa-f]{7})\\x08` -- **a pattern that cannot match anything** -- and
     returned zero without error, leaving a checker looking merely unchanged.

Each time, the project wrote down the lesson. Each time, the lesson stayed in prose.

> **A rule that lives in a note and not in the tooling is a rule you will break while fixing the
> thing it warned you about.**

This wires it in. It is deliberately dumb: no text in this project -- source or prose -- has any
business containing a C0 control byte other than tab, newline and carriage return.

What it catches
---------------
NUL, backspace, bell, escape, form feed, vertical tab and the rest of C0. Those are the residue of
a shell mangling an escape sequence, and every one of them is invisible in a terminal.

**Especially `\\x08` inside a regex literal**, which is the failure that motivated this: it is not a
syntax error, it does not raise, and the pattern silently matches nothing forever.

Usage
-----
    python check_source_hygiene.py --paths "Database/Tools/analysis-kit" "Database/FFXII TZA"
    python check_source_hygiene.py --self-test
"""
import argparse
import collections
import io
import os
import sys

ALLOWED = {0x09, 0x0A, 0x0D}
NAMES = {0x00: "NUL", 0x07: "BEL", 0x08: "BACKSPACE", 0x0B: "VT", 0x0C: "FF", 0x1B: "ESC",
         0x1A: "SUB", 0x7F: "DEL"}
EXTS = (".py", ".md", ".ps1", ".tsv", ".txt", ".json")


def scan_bytes(data, rel, out):
    line = 1
    for i, b in enumerate(data):
        if b == 0x0A:
            line += 1
            continue
        if b < 0x20 and b not in ALLOWED or b == 0x7F:
            ctx = data[max(0, i - 24):i + 24].decode("utf-8", "replace").replace(chr(b), "<?>")
            out.append((rel, line, NAMES.get(b, "0x%02X" % b), ctx.strip()))
    return out


SELF_BAD = b"BARE = re.compile(r\"\x08(0[0-9A-Fa-f]{7})\x08\")\n"
SELF_OK = b"BARE = re.compile(r\"\\b(0[0-9A-Fa-f]{7})\\b\")\n\ttabs and newlines are fine\n"


def self_test():
    bad, ok = [], []
    scan_bytes(SELF_BAD, "<bad>", bad)
    scan_bytes(SELF_OK, "<ok>", ok)
    if len(bad) != 2 or len(ok) != 0:
        print("SELF-TEST FAILED: bad=%d (want 2) ok=%d (want 0)" % (len(bad), len(ok)))
        return 1
    print("self-test ok: catches the backspace that made a regex unmatchable, "
          "silent on tabs, newlines and a correctly escaped pattern")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=[])
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.paths:
        return ap.error("--paths required unless --self-test")

    out, files = [], 0
    for root_path in a.paths:
        if os.path.isfile(root_path):
            # A single file is a legitimate thing to want to check, and refusing it silently is
            # how this tool told its first user "no stray control bytes in 0 file(s)".
            files += 1
            scan_bytes(io.open(root_path, "rb").read(), root_path.replace(os.sep, "/"), out)
            continue
        for root, _d, names in os.walk(root_path):
            for fn in sorted(names):
                if not fn.endswith(EXTS):
                    continue
                p = os.path.join(root, fn)
                files += 1
                scan_bytes(io.open(p, "rb").read(), p.replace(os.sep, "/"), out)

    if files == 0:
        # **"Clean" and "scanned nothing" read identically to anyone not looking at the count.**
        # The first user of this tool passed a file path, got `no stray control bytes in 0 file(s)`,
        # and noticed only because the population was printed beside the number -- this project's
        # own rule, firing inside a checker rather than a document. Now it is an error, not a
        # sentence to be read carefully.
        print("SCANNED NOTHING: no file matched %s under %r" % (", ".join(EXTS), a.paths))
        print("A clean result over an empty population is not a clean result.")
        return 2

    if not out:
        print("no stray control bytes in %d file(s)" % files)
        return 0

    print("STRAY CONTROL BYTES - the residue of a mangled escape sequence")
    print("These are invisible in a terminal. A backspace inside a regex literal is not a syntax")
    print("error: the pattern silently matches nothing, forever.\n")
    by = collections.defaultdict(list)
    for rel, line, name, ctx in out:
        by[rel].append((line, name, ctx))
    for rel in sorted(by):
        print("  %s" % rel)
        for line, name, ctx in by[rel][:8]:
            print("      line %-6d %-10s %s" % (line, name, ctx[:90]))
        if len(by[rel]) > 8:
            print("      ... %d more" % (len(by[rel]) - 8))
        print()
    print("%d occurrence(s) in %d file(s), of %d scanned" % (len(out), len(by), files))
    return 1


if __name__ == "__main__":
    sys.exit(main())
