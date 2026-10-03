"""apply_edits.py [--apply] - replace existing type-store rows with the edited rows in edits.json beside this file
(OPUS, 2026-10-03): WidgetMessage gains its static instance at 0x01E0C0F8 (route + instance), WeaponRecipeRef.recipe
becomes WeaponRecipeBlob*. Each old row must be present verbatim. Refuses an uncommitted line in either store that is
not this record's (lines in $OPUS_APPLY_ALLOWED excepted). Idempotent (ALREADY). Prints FAILS n."""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TY = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types"))
E = json.load(io.open(os.path.join(HERE, "edits.json"), encoding="utf-8"))["edits"]
allowed = set()
if os.environ.get("OPUS_APPLY_ALLOWED"):
    allowed = set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines())
fails = done = 0
stores = {}
for e in E:
    fn = e["store"]
    if fn not in stores:
        p = os.path.join(TY, fn)
        b = io.open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in b else "\n"
        stores[fn] = [p, nl, b.rstrip("\r\n").split(nl)]
mine = {e["old"] for e in E} | {e["new"] for e in E}
for fn in stores:
    d = subprocess.run(["git", "-C", TY, "diff", "--", fn], capture_output=True, text=True, encoding="utf-8").stdout
    foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))
               and l[1:] not in mine and l[1:] not in allowed]
    if foreign:
        print("REFUSED: %s has %d uncommitted lines that are not this record's" % (fn, len(foreign)))
        fails += 1
for e in E:
    lines = stores[e["store"]][2]
    if e["new"] in lines and e["old"] not in lines:
        done += 1
        continue
    if lines.count(e["old"]) != 1:
        print("OLD ROW NOT FOUND ONCE in %s: %s" % (e["store"], e["old"][:80]))
        fails += 1
if done == len(E) and not fails:
    print("ALREADY (%d edits)" % done)
    print("FAILS 0")
    sys.exit(0)
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
for e in E:
    lines = stores[e["store"]][2]
    if e["old"] in lines:
        lines[lines.index(e["old"])] = e["new"]
for fn, (p, nl, lines) in stores.items():
    io.open(p + ".opus-tmp", "w", encoding="utf-8", newline="").write(nl.join(lines) + nl)
    os.replace(p + ".opus-tmp", p)
print("APPLIED: %d edits" % (len(E) - done))
print("FAILS 0")
