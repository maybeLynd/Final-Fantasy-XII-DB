#!/usr/bin/env python3
"""tsv_io.py - read and write the store's TSVs without assuming the line terminator.

WHY THIS EXISTS, and it is not hypothetical. Every script in this kit does

    lines = io.open(path, encoding="utf-8", newline="").read().split("\\n")
    ...
    io.open(path, "w", encoding="utf-8", newline="").write("\\n".join(out))

which is correct exactly while the working copy uses LF - and GIT DECIDES THAT, not the author.
On 2026-09-19 a `git stash pop`, during an unrelated validator comparison, put `fields.tsv`
through git's eol normalisation and left it CRLF. After that, `split("\\n")` leaves a trailing
`\\r` on the LAST COLUMN of every row, so the idiom the whole kit uses to append to an evidence
cell -

    c[8] += " || " + note

- puts a carriage return in the MIDDLE of the cell. Python's `split("\\n")` does not treat a lone
`\\r` as a line break, so the script sees nothing wrong and writes a file that LOOKS fine; the
next reader that uses universal newlines - `types_index.py` does - sees a line break there and
reports `references unknown type " || SPLIT 2026-09-19 (OPUS) ..."`. Six rows, four errors, one
revert.

That is the SECOND time the same day. The first was caught by an index lookup failing before
anything was written, and the hazard was written up as something that deserved a shared reader.
It was not built, and it bit the next package.

    hdr, rows, term = read(path)      # rows are lists of cells, no terminator anywhere
    write(path, hdr, rows, term)      # the SAME terminator goes back

The terminator is read off the file rather than configured, because the point is to survive
whatever git most recently did. `check(path)` reports a lone `\\r` anywhere in the file, which is
the signature of the corruption this module prevents, and is worth running after any edit made
by a script that does not use this module.
"""
import io
import sys


def read(path):
    """(header cells, list of row-cell-lists, terminator). No cell contains a terminator."""
    raw = io.open(path, "rb").read()
    term = "\r\n" if raw.count(b"\r\n") * 2 > raw.count(b"\n") else "\n"
    text = raw.decode("utf-8")
    parts = text.split(term)
    rows = [p.split("\t") for p in parts]
    return rows[0], rows[1:], term


def write(path, hdr, rows, term):
    """Write with the terminator that was read. A cell containing one is refused, not escaped:
    it means the caller built a value out of something it should not have, and silently
    mangling it is how the corruption above happened."""
    out = [hdr] + list(rows)
    for r in out:
        for cell in r:
            if "\r" in cell or "\n" in cell:
                raise ValueError("cell contains a line terminator: %r" % cell[:80])
    body = term.join("\t".join(r) for r in out)
    io.open(path, "wb").write(body.encode("utf-8"))


def check(path):
    """A lone carriage return anywhere is the signature of a mangled cell. Returns the count."""
    raw = io.open(path, "rb").read()
    return raw.count(b"\r") - raw.count(b"\r\n")


def main():
    bad = 0
    for p in sys.argv[1:]:
        n = check(p)
        bad += n
        hdr, rows, term = read(p)
        print("%-60s %-6s %5d row(s)  lone CR %d"
              % (p.rsplit("/", 1)[-1], repr(term), len(rows), n))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
