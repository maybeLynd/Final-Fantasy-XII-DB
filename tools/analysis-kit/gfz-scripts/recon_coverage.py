#!/usr/bin/env python3
"""recon_coverage.py - which reconstructed functions does no test ever call?

Why
---
`PersistentFlag_Gate` sat in `flag_banks.c`, compiled, declared in the header with its own
constants, and **no case had ever called it**. It was found by hand, because a `CONTRACT_MAP` row
said `NOT EXERCISED` while the code sat a directory away.

**A written-but-unrun function is a claim, not a reconstruction.** It looks like progress in a
source tree, it compiles, it may even be correct -- and it contributes nothing to parity, because
nothing has ever compared it to anything. That is a gap the parity table cannot show: the table
scores *claims*, and a function nobody wrote a claim about is invisible to it.

What it checks
--------------
For every public function declared in `Reconstruction/Game/**/*.h`, whether any differential
driver in `Reconstruction/Tests/Differential/*.c` mentions it. A driver is the only thing that
can call the reconstruction, so a name absent from all of them is a function no test can reach.

**A mention is not a call, and this tool says so.** It reports *reachability by name*, which is an
upper bound on coverage: a driver that mentions a function inside `#if 0`, or in a comment, would
still count here. The cheap check is worth having because its FAILURES are exact -- a name that
appears nowhere is definitely uncalled -- and its passes are a weaker statement, which is stated.

Declarations are found by a deliberately narrow rule: a line at column 0 that ends in `);`, or
opens a parameter list continued on later lines, with an identifier immediately before the `(`.
Static helpers inside a `.c` are **not** public surface and are not counted.
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

ROOT = os.path.join(KP.ROOT, "Reconstruction")
DECL = re.compile(r"^[A-Za-z_][A-Za-z0-9_ \t\*]*?([A-Za-z_][A-Za-z0-9_]*)\s*\(")
SKIP = ("typedef", "#", "}", "extern \"C\"")


def declared(header):
    """-> [(name, line)] for the public functions a header declares."""
    out = []
    text = io.open(header, encoding="utf-8").read()
    # join continuation lines so a multi-line parameter list is one logical declaration
    lines, buf = [], ""
    for raw in text.split(chr(10)):
        s = raw.rstrip()
        if not s or s.lstrip().startswith("*") or s.lstrip().startswith("/*"):
            buf = ""
            continue
        buf = (buf + " " + s.strip()) if buf else s
        if s.endswith(";") or s.endswith("{") or s.endswith("}"):
            lines.append(buf)
            buf = ""
    for l in lines:
        if any(l.lstrip().startswith(k) for k in SKIP):
            continue
        if "(" not in l or not l.rstrip().endswith(";"):
            continue
        m = DECL.match(l)
        if m and m.group(1) not in ("if", "while", "for", "return", "sizeof"):
            out.append(m.group(1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    a = ap.parse_args()

    game = os.path.join(a.root, "Game")
    tests = os.path.join(a.root, "Tests", "Differential")
    headers = []
    for base, _d, files in os.walk(game):
        for f in sorted(files):
            if f.endswith(".h"):
                headers.append(os.path.join(base, f))

    drivers = [os.path.join(tests, f) for f in sorted(os.listdir(tests))
               if f.endswith("_driver.c")]
    blob = "".join(io.open(d, encoding="utf-8").read() for d in drivers)
    # A helper the reconstruction itself calls is exercised on every case that reaches its
    # caller. `PersistentFlag_BitAddress` is used by query() and set() and therefore runs on all
    # 8,064 flag-bank comparisons; reporting it as a gap would be a false alarm, and a tool that
    # cries wolf gets ignored.
    impl = ""
    for base, _d, files in os.walk(game):
        for f in sorted(files):
            if f.endswith(".c"):
                impl += io.open(os.path.join(base, f), encoding="utf-8").read()

    print("headers : %d   drivers : %d" % (len(headers), len(drivers)))
    print()
    total = reached = 0
    missing = []
    for h in headers:
        names = declared(h)
        rel = os.path.relpath(h, a.root).replace(os.sep, "/")
        direct = [n for n in names if n in blob]
        # "called somewhere other than its own definition" -- more than one mention in the
        # implementation blob means a caller exists inside the reconstruction
        indirect = [n for n in names if n not in blob and impl.count(n) > 1]
        gap = [n for n in names if n not in direct and n not in indirect]
        total += len(names)
        reached += len(direct) + len(indirect)
        print("  %-38s %2d declared  %2d direct  %2d indirect%s"
              % (rel, len(names), len(direct), len(indirect),
                 "" if not gap else "   <-- %d UNREACHED" % len(gap)))
        for n in indirect:
            print("        (indirect) %s -- called by the reconstruction, not by a driver" % n)
        for n in gap:
            missing.append((rel, n))
    print()
    print("public functions declared          : %d" % total)
    print("reached, directly or indirectly    : %d" % reached)
    print("REACHED BY NOTHING                 : %d" % len(missing))
    for rel, n in missing:
        print("    %-38s %s" % (rel, n))
    print()
    print("A name absent from every driver AND from every other reconstruction file is")
    print("definitely uncalled. The converse is weaker: this counts a MENTION, not a call, so the")
    print("reached figure is an UPPER BOUND. It caught Angle_WrapLoop, which a driver never")
    print("named because the driver had its own copy of it.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
