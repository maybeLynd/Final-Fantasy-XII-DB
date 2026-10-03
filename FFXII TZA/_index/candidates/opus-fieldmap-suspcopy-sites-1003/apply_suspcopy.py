"""apply_suspcopy.py [--apply] - the battle-unit field map's +0x730..+0x790 rows cite the suspend / restore copy loop's
TAIL sites, which address +0xB30..+0xB90; each is replaced by the loop-body site that reaches the row's offset (on the
pass whose pointer sits at +0x7B0), struck and annotated (OPUS, 2026-10-03, SWE2STRUCT-REQ-OPUS-FIELDMAP-SUSPCOPY-SITES-1003).

Bytes (retool.py, re-read by OPUS): 0030EDA0's restore loop and 0030EFF0's snapshot loop each run nine 0x80-byte passes
from +0x6B0 (`lea rcx/rax, [+0x80]` at the top or after the first load), so the seven tail moves after the loop
(0030EE13..0030EE44, 0030F0A9..0030F0DD) address +0xB30..+0xB90; +0x730..+0x790 are reached by the body's
0030EDC7..0030EDF7 (writes [rcx-0x80..-0x20]) and 0030F05D..0030F093 (reads) on the second pass. Idempotent; a row
edit applies once (skipped when its new text is present, FAIL when the old cell text is missing). CRLF-safe.
"""
import io
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
P = os.path.join(DB, "04-Actor-Entity", "Battle-Unit", "the-battle-unit-field-map.md")
C = " *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0x%s; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*"


def site(old, new, tail):
    return ("(`%s`)" % old, "(~~`%s`~~ `%s`%s)" % (old, new, C % tail))


# (row prefix, [(old cell text, new cell text)]) - each row is matched by its offset cell
EDITS = [
    ("| `+0x730` |", [site("0030EE13", "0030EDC7", "B30")]),
    ("| `+0x740` |", [site("0030EE1A", "0030EDCF", "B40"), site("0030F0B5", "0030F06B", "B40")]),
    ("| `+0x750` |", [site("0030F0BD", "0030F073", "B50")]),
    ("| `+0x760` |", [site("0030EE2A", "0030EDDF", "B60"), site("0030F0C5", "0030F07B", "B60")]),
    ("| `+0x770` |", [site("0030F0CD", "0030F083", "B70")]),
    ("| `+0x780` |", [site("0030EE3A", "0030EDEF", "B80")]),
    ("| `+0x790` |", [site("0030EE44", "0030EDF7", "B90"), site("0030F0DD", "0030F093", "B90"),
                      ("reached by immediate displacement only inside the snapshot's block copy (`0030F0DD`; `+0x6B0` for `0x4F0` bytes)",
                       "~~reached by immediate displacement only inside the snapshot's block copy (`0030F0DD`; `+0x6B0` for `0x4F0` bytes)~~ "
                       "reached only through the suspend / restore block copy's loop body (`0030F093` read, `0030EDF7` write, on the "
                       "pass whose pointer sits at `+0x7B0`; the copy covers `+0x6B0` for `0x4F0` bytes) *(corrected 2026-10-03, OPUS: "
                       "`0030F0DD` is the loop tail and reads `+0xB90`; SWE2-STRUCT's loop attribution)*")]),
]


def main():
    apply = "--apply" in sys.argv
    t = io.open(P, encoding="utf-8", newline="").read()
    lines = t.split("\n")
    fails = done = 0
    for prefix, subs in EDITS:
        # several tables start rows with the same offset: the row is the one citing the site (or already corrected)
        idx = [i for i, l in enumerate(lines) if l.startswith(prefix) and (subs[0][0] in l or subs[0][1] in l)]
        if len(idx) != 1:
            print("FAIL row %s x%d" % (prefix, len(idx))); fails += 1; continue
        i = idx[0]
        for old, new in subs:
            if new in lines[i]:
                print("SKIP", prefix, old[:30]); continue
            if lines[i].count(old) != 1:
                print("FAIL", prefix, "cell x%d:" % lines[i].count(old), old[:40]); fails += 1; continue
            lines[i] = lines[i].replace(old, new); done += 1
            print("APPLY" if apply else "WOULD", prefix, old[:30])
    if apply and done and not fails:
        io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("FAILS %d" % fails)


if __name__ == "__main__":
    main()
