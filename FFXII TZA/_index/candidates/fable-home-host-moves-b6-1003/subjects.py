"""subjects.py - the host rule of FABLE's batch-6 host moves (FABLE, 2026-10-03).

A page DOCUMENTS an address when the address is a subject of one of its units, not a passing mention:
- a heading: every address in it;
- a table row: the row's first address (the first cell in the usual address-keyed table; the first address-bearing
  cell when the key cell is a number or a name, as in a subtype table);
- a paragraph or a list item: its first address (after any bold lead label).
Lines inside a fenced code block are not units. A line range can be skipped (a record's own section), so that a
section never qualifies its own host.

    python -B subjects.py PAGE ADDR [ADDR ...]    (prints every mention of each ADDR, subject or passing)
"""
import os, re, sys

ADDR = re.compile(r"(?<![0-9A-Za-z])[0-9A-F]{8}(?![0-9A-Za-z])")
ITEM = re.compile(r"^(?:[-*+]|\d+[.)])\s+")


def units(lines, skip=None):
    """[(kind, first line index, last line index, subject addresses)] for the page's lines (no CR)."""
    out, cur, fence = [], None, False

    def close():
        nonlocal cur
        if cur:
            m = ADDR.search(cur[3])
            out.append((cur[0], cur[1], cur[2], {m.group(0)} if m else set()))
        cur = None

    for i, raw in enumerate(lines):
        if skip and skip[0] <= i < skip[1]:
            close()
            continue
        s = raw.strip()
        if s.startswith("```"):
            close()
            fence = not fence
            continue
        if fence:
            continue
        while s.startswith(">"):
            s = s[1:].strip()
        if not s:
            close()
        elif s.startswith("#"):
            close()
            out.append(("heading", i, i, set(ADDR.findall(s))))
        elif s.startswith("|"):
            close()
            if not re.fullmatch(r"\|[\s:|-]*", s):
                m = ADDR.search(s)
                out.append(("row", i, i, {m.group(0)} if m else set()))
        elif ITEM.match(s):
            close()
            cur = ["item", i, i, s[ITEM.match(s).end():]]
        elif cur:
            cur[2] = i
            cur[3] += " " + s
        else:
            cur = ["paragraph", i, i, s]
    close()
    return out


def subject_lines(lines, addr, skip=None):
    """[(kind, 1-based line)] of every unit whose subject is addr."""
    return [(k, a + 1) for k, a, _b, subj in units(lines, skip) if addr in subj]


def page_lines(path):
    return open(path, "rb").read().decode("utf-8").replace("\r", "").split("\n")


if __name__ == "__main__":
    DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    ls = page_lines(os.path.join(DB, *sys.argv[1].split("/")))
    us = units(ls)
    for addr in sys.argv[2:]:
        print("== %s on %s" % (addr, sys.argv[1]))
        for i, l in enumerate(ls):
            if addr in l:
                u = next((x for x in us if x[1] <= i <= x[2]), None)
                tag = ("SUBJECT %s@L%d" % (u[0], u[1] + 1)) if u and addr in u[3] else "passing"
                k = l.find(addr)
                print("  L%-5d %-22s %s" % (i + 1, tag, l[max(0, k - 70):k + 90]))
