"""apply.py [--apply] - remove the EMPTY 'Homed frontier bodies' section that FABLE's H3 publish (60f3e63b3) appended to
gambit-evaluation-and-enmity.md: its record (fable-home-gambit-evaluation-and-enmity-1003) had 0 rows (its one row was
held), and the applier of the time wrote the heading, the note and a header-only table. Also gives that record's
applier copy the zero-row refusal. Anchored: the section must be the page's last, with a header-only table. Refuses a
dirty page; keeps CRLF. Prints FAILS N last."""
import io, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "09-Combat-AI-And-Gambits", "gambit-evaluation-and-enmity.md")
REC_APPLIER = os.path.join(HERE, "..", "fable-home-gambit-evaluation-and-enmity-1003", "homing_applier.py")
HEAD = "## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)"
fails = 0
if subprocess.run(["git", "diff", "--quiet", "--", P], cwd=HERE).returncode != 0:
    print("REFUSED: page dirty"); print("FAILS 1"); sys.exit(1)
raw = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
t = raw.replace("\r\n", "\n")
i = t.find(HEAD)
if i < 0:
    print("ALREADY (no empty section)")
    new = t
else:
    sec = t[i:]
    lines = [l for l in sec.rstrip("\n").split("\n")]
    table = [l for l in lines if l.startswith("|")]
    if t.count(HEAD) != 1 or len(table) != 2 or not re.match(r"^\|[-| ]+\|$", table[1]) or "## " in sec[3:]:
        print("MISS: the section is not a lone header-only table at the end of the page (table lines %d)" % len(table))
        fails += 1
        new = t
    else:
        new = t[:i].rstrip("\n") + "\n"
        print("WOULD REMOVE %d lines" % len(lines))
ap = io.open(REC_APPLIER, encoding="utf-8").read()
old = '    if HEAD.splitlines()[0].encode("utf-8") in b:\n        print("ALREADY")'
fix = ('    if not ROWS:\n        # 2026-10-03 (FABLE, on SWE2-AUDIT-SPEC batch 5): a package whose rows were all held or rejected must not\n'
       '        # append an empty section (this package did, at 60f3e63b3; removed by fable-empty-homed-section-1003).\n'
       '        print("NOTHING TO HOME (0 rows) - page untouched")\n'
       '    elif HEAD.splitlines()[0].encode("utf-8") in b:\n        print("ALREADY")')
ap_new = ap if "NOTHING TO HOME" in ap else (ap.replace(old, fix) if ap.count(old) == 1 else None)
if ap_new is None:
    print("MISS applier anchor"); fails += 1
if "--apply" in sys.argv and not fails:
    if new != t:
        io.open(P, "w", encoding="utf-8", newline="").write(new.replace("\n", nl)); print("PATCHED page")
    if ap_new != ap:
        io.open(REC_APPLIER, "w", encoding="utf-8", newline="").write(ap_new); print("PATCHED record applier")
print("FAILS %d" % fails)
