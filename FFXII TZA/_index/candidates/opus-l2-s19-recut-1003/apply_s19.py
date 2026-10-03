"""apply_s19.py [--apply] - the S-19 MovementBody re-cut (OPUS, 2026-10-03; measured by repos-91, a local helper; anchors
re-read by OPUS). Replaces the census rows cut at initialiser widths with the fields the separation pass actually
accesses, from s19_recut.json beside this file.

Without --apply it only checks; with --apply it rewrites fields.tsv atomically. Refuses when:
- an 'old' row is not present verbatim and the record is not already applied;
- fields.tsv carries another lane's uncommitted MovementBody lines.
Idempotent: an applied store prints ALREADY. Prints FAILS n."""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types", "fields.tsv"))
spec = json.load(io.open(os.path.join(HERE, "s19_recut.json"), encoding="utf-8"))
olds = [x["old"] for x in spec["proposed"] if x.get("old")]
news = [x["new"] for x in spec["proposed"] if x.get("new")]
b = io.open(F, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in b else "\n"
lines = b.rstrip("\r\n").split(nl)
fails = 0
if all(n in lines for n in news) and not any(o in lines for o in olds if o not in news):
    print("ALREADY (%d new rows present, %d old rows gone)" % (len(news), len(olds)))
    print("FAILS 0")
    sys.exit(0)
missing_old = [o for o in olds if o not in lines]
for o in missing_old:
    print("OLD ROW NOT FOUND: " + o[:120].replace("\t", " | "))
fails += len(missing_old)
d = subprocess.run(["git", "-C", os.path.dirname(F), "diff", "--", "fields.tsv"], capture_output=True, text=True).stdout
# 2026-10-03: ANY uncommitted line that is not this record's refuses - publishing fields.tsv would carry a peer's hunks
own = set(olds) | set(news)
foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---")) and l[1:] not in own]
if foreign:
    print("REFUSED: fields.tsv has %d uncommitted MovementBody lines (another lane's?)" % len(foreign))
    fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
idx = [i for i, l in enumerate(lines) if l in olds]
first = min(idx)
kept = [l for i, l in enumerate(lines) if l not in olds]
block = sorted([l for l in kept if l.startswith("MovementBody\t")] + news, key=lambda l: int(l.split("\t")[1], 16))
rest = [l for l in kept if not l.startswith("MovementBody\t")]
# re-insert the MovementBody block where it stood
pos = sum(1 for l in lines[:first] if not l.startswith("MovementBody\t"))
out = rest[:pos] + block + rest[pos:]
tmp = F + ".opus-tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(nl.join(out) + nl)
os.replace(tmp, F)
print("APPLIED: %d rows replaced by %d (MovementBody block %d rows)" % (len(olds), len(news), len(block)))
print("FAILS 0")
