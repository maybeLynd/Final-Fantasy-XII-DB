#!/usr/bin/env python3
"""check_stale_reasons.py - a CONTRACT_MAP reason that the harness's own source contradicts.

WHY THIS EXISTS. `parity_status.py` re-reads each contract and checks the CLAIM strings against it,
so a reworded claim shows up as drift. **Nothing re-reads the REASONS.** A reason is written once,
when a row is graded, and it is never revisited when the script around it grows - so a row can say
"the suite does not drive X" long after someone added the cases that drive X.

That is not hypothetical. `frame_gate`'s row said the pilot "does not drive the second object at
`[rbx+0x10F68]`". Its own `build_script` sets that flag word, and both of the tests on it change the
trace. The row had been `NOT EXERCISED` on a reason its own file refutes.

THE SIGNAL, and it is deliberately narrow. A non-EXERCISED reason that says the suite does NOT reach
something, and names a hex constant, is suspicious when that same constant appears elsewhere in the
harness's own source - because the only reason for a harness to mention an address is to drive it.

**This reports candidates for a human read, never a verdict.** A constant can appear in a comment,
in a claim string, or in a completely unrelated case, and the check cannot tell. What it replaces is
nobody ever looking.

REGRESSION CONTROL, and the reason to believe the signal at all:

    git show 75f2c38ca~1:Reconstruction/Tests/Differential/diff_frame_gate.py > <dir>/diff_frame_gate.py
    python check_stale_reasons.py --diff <dir>

fires exactly once, on the row that was in fact wrong.

WHAT THE CORPUS LOOKS LIKE AT HEAD, read once so nobody reads it twice (2026-09-18, OPUS). **Seven
flags over 100 negative-phrased reasons, and all seven were read by hand. All seven are benign:**

- `verb_dispatch` x2 (`002621D0`) and `status_write` x3 (`0030E360`, `003876D0`, `00387730`) - the
  constant appears only in a docstring, another row's reason or a `print`, never in a driving
  context.
- `storage_read` (`00583C00`) - the reason NAMES that address as the direction it *does* drive, so
  the mention is the reason's own subject.
- `sound_request` (`001DBDB0`) - the sharpest of them, and still benign. The harness really does
  reach that address: it is `DISPATCH_FN`, a hooked tail-jump target with its own handler. But the
  reason says the pilot *stops at* it and never runs `00210C00` - and `00210C00` appears nowhere in
  the source, so the claim the row actually rests on is untouched.

**So the one true positive in this corpus was `frame_gate`, and it is fixed.** That is a useful
negative: the 300-odd non-EXERCISED rows are not riddled with stale reasons. Re-run the check when a
script grows, which is the moment a reason can go stale.

TWO NOISE SOURCES WERE THE CHECK'S OWN and are fixed: bare four-digit tokens matched the YEAR in
"REFUTED 2026-09-16", and a re-graded row **quotes** the wording it replaced, so the check flagged
its own corrections for ever.
"""
import argparse
import ast
import os
import re
import sys

import kit_paths as KP

DIFF = os.path.join(KP.ROOT, "Reconstruction", "Tests", "Differential")

# A reason that asserts the suite does NOT reach something. Only these are worth cross-checking.
NEGATIVE = re.compile(
    r"\bdoes not drive\b|\bnot driven\b|\bnever (?:runs|reach(?:es|ed)|driven|entered)\b|"
    r"\bis not (?:run|reached|entered|exercised)\b|\bnothing here\b|\bundriven\b|"
    r"\bnot among this suite\b|\bupstream\b", re.I)

REVIEWED = re.compile(r"RE-GRADED|REFUTED|WITHDRAWN|CORRECTED", re.I)
# A BARE token needs SIX to eight hex digits, because this image's addresses have that many and a
# four-digit bare token is usually a YEAR: "REFUTED 2026-09-16" gave three of the first ten flags a
# constant of 0x2026, which is the check inventing its own noise.
HEX = re.compile(r"0x([0-9A-Fa-f]{3,8})\b|\b([0-9A-F]{6,8})\b")


def contract_map_and_src(path):
    src = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None, src
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CONTRACT_MAP":
            try:
                return ast.literal_eval(n.value), src
            except ValueError:
                return None, src
    return None, src


def constants(text):
    out = set()
    for m in HEX.finditer(text):
        v = m.group(1) or m.group(2)
        try:
            n = int(v, 16)
        except ValueError:
            continue
        if n >= 0x100:                      # a one- or two-digit value is noise
            out.add(n)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", default=DIFF)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        fires = bool(NEGATIVE.search("the pilot does not drive the second object at [rbx+0x10F68]"))
        quiet = bool(NEGATIVE.search("both sides are driven at a negative record index"))
        c = constants("does not drive the second object at [rbx+0x10F68]")
        print("  control negative phrase detected            %s" % ("yes" if fires else "BROKEN"))
        print("  control positive phrase not detected        %s" % ("yes" if not quiet else "BROKEN"))
        print("  control constant extracted from the reason  %s"
              % ("yes" if 0x10F68 in c else "BROKEN"))
        print("  control small values ignored                %s"
              % ("yes" if not (constants("bit 8 and bit 2") & {8, 2}) else "BROKEN"))
        ok = fires and not quiet and (0x10F68 in c)
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    flagged = 0
    checked = 0
    for fn in sorted(os.listdir(a.diff)):
        if not (fn.startswith("diff_") and fn.endswith(".py")):
            continue
        rows, src = contract_map_and_src(os.path.join(a.diff, fn))
        if not rows:
            continue
        # the source WITHOUT the CONTRACT_MAP block, so a reason cannot corroborate itself
        body = src
        i = body.find("CONTRACT_MAP")
        j = body.find("\n]\n", i) if i >= 0 else -1
        if i >= 0 and j > i:
            body = body[:i] + body[j:]
        src_consts = constants(body)
        for claim, status, why in rows:
            if status == "EXERCISED":
                continue
            if not NEGATIVE.search(why):
                continue
            # A row whose reason records its own review is not stale by definition - and without
            # this the check flags its own corrections for ever, because a re-grade QUOTES the
            # wording it replaced.
            if REVIEWED.search(why):
                continue
            checked += 1
            hits = sorted(constants(why) & src_consts)
            if not hits:
                continue
            flagged += 1
            print("%s  [%s]" % (fn[5:-3], status))
            print("   claim : %s" % claim[:88])
            print("   reason: %s" % why[:150])
            print("   the harness's own source also mentions: %s"
                  % ", ".join("0x%X" % h for h in hits[:6]))
            print()
    print("negative-phrased reasons checked: %d" % checked)
    print("flagged for a read: %d" % flagged)
    print()
    print("A flag is a CANDIDATE, not a verdict: a constant can appear in a comment, in a claim")
    print("string, or in an unrelated case. What this replaces is nobody ever re-reading a reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
