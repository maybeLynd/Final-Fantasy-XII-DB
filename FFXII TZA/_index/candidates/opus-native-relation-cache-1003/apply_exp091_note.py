"""apply_exp091_note.py [--apply] - EXP-091's stub limit, qualified by the now-accepted Method A result for the body it
stubbed (OPUS, 2026-10-03, ASTRA-REQ-OPUS-UQ147-NATIVE-RELATION-CONSUMPTION-1003: "EXP091 stub did not execute this
body; now Method A local effects are separate from its Method B samples"). Appends one sentence to the stubbed-entries
bullet; changes no sample, case or result. Refuses when the record has uncommitted lines other than OPUS's own
opus-exp091-narrowings-1003 items (that record's applier must say ALREADY). Idempotent (ALREADY). Prints FAILS n."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "_experiments", "EXP-091-commit-callees-exec.md")
ANCHOR = "- **Four stubbed entries** (entry byte patched to `ret`, calls logged): `0x512F30` SINK (deep"
NOTE = ("  *(2026-10-03, OPUS: this record did not execute `0x512F30`. Its local effects are now established separately "
        "by Method A - ASTRA's `uq147-native-relation-invariant`, ACCEPTED by SWE2-AUDIT-SPEC (`b9502c733`): 26 + 11 "
        "persistent write sites, the only transfers `00513005`/`00513022` to `00512CD0`, no import or heap call; see "
        "the relation types consumed in `_index/candidates/opus-native-relation-cache-1003/`. That static result is "
        "not one of this record's Method B samples, and no case here changes.)*")
b = io.open(P, encoding="utf-8", newline="").read()
if NOTE in b:
    print("ALREADY")
    print("FAILS 0")
    sys.exit(0)
fails = 0
lines = b.split("\n")
idx = [i for i, l in enumerate(lines) if l.rstrip("\r").startswith(ANCHOR)]
if len(idx) != 1:
    print("anchor bullet found %d times (need 1)" % len(idx))
    fails += 1
nar = subprocess.run([sys.executable, "-B", "apply_narrowings.py"], cwd=os.path.join(HERE, "..", "opus-exp091-narrowings-1003"),
                     capture_output=True, text=True).stdout
dirty = subprocess.run(["git", "-C", DB, "diff", "--quiet", "--", "_experiments/EXP-091-commit-callees-exec.md"]).returncode
if dirty and "ALREADY" not in nar:
    print("REFUSED: EXP-091 has uncommitted changes that are not opus-exp091-narrowings-1003's")
    fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
# the bullet runs over several lines; insert the note after its last line (the next line that starts a new bullet or
# is blank ends it)
i = idx[0] + 1
while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith("- "):
    i += 1
eol = "\r" if lines[idx[0]].endswith("\r") else ""
lines[i:i] = [NOTE + eol]
io.open(P + ".opus-tmp", "w", encoding="utf-8", newline="").write("\n".join(lines))
os.replace(P + ".opus-tmp", P)
print("APPLIED")
print("FAILS 0")
