#!/usr/bin/env python3
"""tsv_lines.py - read and write a _types TSV without disturbing its line endings.

TWO DISTINCT HAZARDS, both met in one sitting on 2026-09-20, both recorded because either
one silently corrupts a row or a diff.

1. A CELL'S TRAILING CR IS A LINE BREAK TO THE READER.  `types_index.read_tsv` opens the
   file in Python's UNIVERSAL NEWLINE mode, so on a CRLF working tree every row's last
   column ends in a CR that the reader treats as the end of the line.  It is harmless only
   while nothing follows it - the empty tail is dropped by `if not ln.strip(): continue`.
   Append to the last column without stripping that CR first and the row splits in two,
   the second half's first column being prose.  That is exactly how a correction to
   `Widget +0x048` produced

       ERROR  fields.tsv references unknown type ' || setter 00247570; 137 call sites ...'

2. "IS THIS FILE CRLF?" IS THE WRONG QUESTION.  `core.autocrlf` is true here, so a
   `git checkout` of a file whose blob is LF hands back a CRLF working tree, while a file
   already present may still be LF.  Deciding the terminator ONCE for the whole file and
   re-applying it rewrites every line that disagreed - a two-row edit that reports 3,905
   lines changed, which buries the actual change and would sweep an unrelated ending into
   the commit.

   So this module keeps EACH LINE'S OWN TERMINATOR.  An LF file stays LF, a CRLF file
   stays CRLF, and a lone stray CR stays exactly where it was.  New rows inherit the
   terminator of the row they are inserted beside, which is what `term_of` is for.
"""
import io


def load(path):
    """-> (lines, keeps).  `lines` have NO terminator; `keeps[i]` is line i's own."""
    raw = io.open(path, encoding="utf-8", newline="").read()
    parts = raw.split("\n")
    lines, keeps = [], []
    for p in parts:
        if p.endswith("\r"):
            lines.append(p[:-1])
            keeps.append("\r")
        else:
            lines.append(p)
            keeps.append("")
    return lines, keeps


def save(path, lines, keeps):
    if len(lines) != len(keeps):
        raise ValueError("lines and keeps must stay in step (%d vs %d)"
                         % (len(lines), len(keeps)))
    io.open(path, "w", encoding="utf-8", newline="").write(
        "\n".join(l + k for l, k in zip(lines, keeps)))


def term_of(keeps, i):
    """The terminator a row inserted at index i should carry."""
    return keeps[i] if 0 <= i < len(keeps) else ""


def cols(line):
    return line.rstrip("\r").split("\t")
