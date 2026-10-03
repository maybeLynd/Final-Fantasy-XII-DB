"""apply_recuts.py [--apply] - CharacterRenderRecord +0x650..+0x65F re-read as the relation owner block (OPUS, 2026-10-03, consuming ASTRA's SPEC-accepted uq147-native-relation-invariant; every cited site re-read at the bytes by OPUS), from recuts.json beside this file.


Without --apply it only checks; with --apply it rewrites fields.tsv atomically, keeping each type's rows in offset
order. Refuses when an 'old' row is not present verbatim (and the record is not already applied), or when fields.tsv
carries uncommitted lines for these types (another lane's work). Idempotent (ALREADY). Prints FAILS n."""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types", "fields.tsv"))
spec = json.load(io.open(os.path.join(HERE, "recuts.json"), encoding="utf-8"))
olds = [x["old"] for x in spec["proposed"] if x.get("old")]
news = [x["new"] for x in spec["proposed"] if x.get("new")]
TYPES = {x["type"] for x in spec["proposed"]}
b = io.open(F, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in b else "\n"
lines = b.rstrip("\r\n").split(nl)
if all(n in lines for n in news) and not any(o in lines for o in olds):
    print("ALREADY (%d new rows present, %d old rows gone)" % (len(news), len(olds)))
    print("FAILS 0")
    sys.exit(0)
fails = 0
for o in olds:
    if o not in lines:
        print("OLD ROW NOT FOUND: " + o[:120].replace("\t", " | "))
        fails += 1
d = subprocess.run(["git", "-C", os.path.dirname(F), "diff", "--", "fields.tsv"], capture_output=True, text=True).stdout
# 2026-10-03: ANY uncommitted line that is not this record's refuses - publishing fields.tsv would carry a peer's hunks
own = set(olds) | set(news)
# sibling records apply_l2_set.py applied earlier from a clean store (their diff lines, named in $OPUS_APPLY_ALLOWED)
if os.environ.get("OPUS_APPLY_ALLOWED"):
    own |= set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines())
foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---")) and l[1:] not in own]
if foreign:
    print("REFUSED: fields.tsv has %d uncommitted lines for %s" % (len(foreign), ", ".join(sorted(TYPES))))
    fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
out = []
for l in lines:
    if l in olds:
        continue
    out.append(l)
for t in sorted(TYPES):
    idx = [i for i, l in enumerate(out) if l.split("\t", 1)[0] == t]
    block = sorted([out[i] for i in idx] + [n for n in news if n.split("\t", 1)[0] == t],
                   key=lambda l: int(l.split("\t")[1], 16))
    first = idx[0] if idx else len(out)
    out = [l for i, l in enumerate(out) if i not in set(idx)]
    out[first:first] = block
tmp = F + ".opus-tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(nl.join(out) + nl)
os.replace(tmp, F)
print("APPLIED: %d rows replaced by %d" % (len(olds), len(news)))
print("FAILS 0")
