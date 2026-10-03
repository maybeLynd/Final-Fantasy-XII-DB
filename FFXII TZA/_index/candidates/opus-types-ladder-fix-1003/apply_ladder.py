"""apply_ladder.py [--apply] - put three OPUS type rows back on the charter's readiness ladder (OPUS, 2026-10-03).

c6de67245 (opus-l2exp-types-1003) declared three types with readiness words the ladder does not have, and
types_index.py reports each as an ERROR at HEAD (flagged by SWE2-STRUCT's stand-in checkpoint):
- CameraContext 'STRIDE RESOLVED' -> SEMANTICALLY IDENTIFIED: what it is (camera context 0) is known, its interior
  is not measured and no field row is declared;
- ActionDefinition 'PARTIAL' -> SEMANTICALLY IDENTIFIED: the action row is identified, only +0x13 is declared and
  the size is a table stride, not a number;
- Record02EC19C0 'STRIDE RESOLVED' -> SIGNATURE RESOLVED: extent and stride 8 are PROVEN but +0x06 has no reader -
  the AudioParameterRamp case types_index.py describes (a known extent with unread bytes).
Only the readiness column of those three rows changes. Refuses on an uncommitted types.tsv line that is not this
record's (lines named in $OPUS_APPLY_ALLOWED excepted). Idempotent (ALREADY). Prints FAILS n."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types", "types.tsv"))
FIX = {"CameraContext": ("STRIDE RESOLVED", "SEMANTICALLY IDENTIFIED"),
       "ActionDefinition": ("PARTIAL", "SEMANTICALLY IDENTIFIED"),
       "Record02EC19C0": ("STRIDE RESOLVED", "SIGNATURE RESOLVED")}
b = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in b else "\n"
lines = b.rstrip("\r\n").split(nl)
fails, done, new_lines, mine = 0, 0, list(lines), set()
for i, l in enumerate(lines):
    c = l.split("\t")
    if c[0] in FIX:
        old, new = FIX[c[0]]
        if c[7] == new:
            done += 1
            mine.add(l)
            continue
        if c[7] != old:
            print("%s readiness is %r, expected %r" % (c[0], c[7], old))
            fails += 1
            continue
        c2 = list(c)
        c2[7] = new
        new_lines[i] = "\t".join(c2)
        mine |= {l, new_lines[i]}
allowed = set()
if os.environ.get("OPUS_APPLY_ALLOWED"):
    allowed = set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines())
d = subprocess.run(["git", "-C", os.path.dirname(P), "diff", "--", "types.tsv"], capture_output=True, text=True,
                   encoding="utf-8").stdout
foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))
           and l[1:] not in mine and l[1:] not in allowed]
if foreign:
    print("REFUSED: types.tsv has %d uncommitted lines that are not this record's" % len(foreign))
    fails += 1
if done == len(FIX) and not fails:
    print("ALREADY")
    print("FAILS 0")
    sys.exit(0)
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
tmp = P + ".opus-tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(nl.join(new_lines) + nl)
os.replace(tmp, P)
print("APPLIED: %d readiness values put on the ladder" % (len(FIX) - done))
print("FAILS 0")
