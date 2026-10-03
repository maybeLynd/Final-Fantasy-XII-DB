"""apply.py [--apply] - FABLE's consumption of SWE2-DATA's accepted OV-42 authored-flow record (ASTRA request
ASTRA-REQ-FABLE-OV42-AUTHORED-FLOW-CONSUME-1003): insert battle.txt after the queue-reader subsection of
battle-command-availability-and-reason-codes.md (with a pointer on that subsection's first limit), and append
storage.txt to script-variables-and-their-storage-classes.md. Refuses dirty pages. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
B = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
S = os.path.join(DB, "01-Script-VM-Native-Bridge", "Interpreter-Core", "script-variables-and-their-storage-classes.md")
ANCHOR = "### FABLE 2026-10-02: what the presentation-slot allocator admits (OV-42)"
LIMIT = "  natural command-to-action path is observed or proved."
LIMIT_NEW = LIMIT + " *(Narrowed 2026-10-03 for the shipped `spc_z0000` script: next subsection.)*"
bsec = io.open(os.path.join(HERE, "battle.txt"), encoding="utf-8").read()
ssec = io.open(os.path.join(HERE, "storage.txt"), encoding="utf-8").read()
fails, out = 0, []
for p in (B, S):
    if subprocess.run(["git", "diff", "--quiet", "--", p], cwd=HERE).returncode != 0:
        print("REFUSED: %s has uncommitted changes" % os.path.basename(p)); fails += 1
if not fails:
    raw = io.open(B, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    head = bsec.splitlines()[0]
    if head in raw:
        print("ALREADY battle")
    elif raw.count(ANCHOR) != 1 or raw.count(LIMIT + nl) != 1:
        print("MISS battle anchor %d limit %d" % (raw.count(ANCHOR), raw.count(LIMIT + nl))); fails += 1
    else:
        raw = raw.replace(LIMIT + nl, LIMIT_NEW + nl).replace(ANCHOR, bsec.replace("\n", nl) + nl + ANCHOR)
        out.append((B, raw))
    raw = io.open(S, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    if ssec.splitlines()[0] in raw:
        print("ALREADY storage")
    else:
        out.append((S, raw.rstrip("\r\n") + nl + nl + ssec.replace("\n", nl)))
if not fails and "--apply" in sys.argv:
    for p, t in out:
        io.open(p, "w", encoding="utf-8", newline="").write(t); print("PATCHED %s" % os.path.basename(p))
elif not fails:
    for p, _ in out:
        print("WOULD PATCH %s" % os.path.basename(p))
print("FAILS %d" % fails)
