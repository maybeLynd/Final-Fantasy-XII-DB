"""apply.py [--apply] - re-point register rows AQ-2, BA-1, BQ-27 and B-3 from the gitignored Tools/work/rtti/ outputs to
the committed snapshot members/rtti-methods.tsv (FABLE, 2026-10-02). Refuses when the register has uncommitted changes
(a peer's hunk would ride along). Each row gets one exact replacement; already-applied rows print ALREADY. Prints
FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OQ = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")
LINK = "[members/rtti-methods.tsv](../00-Engine-Core-Runtime/Object-Model/members/rtti-methods.tsv)"
SNAP = "the committed snapshot of `rtti_recover.py`'s 2026-09-02 output, body byte-identical"
REPL = {
    "AQ-2": ("(`Tools/work/rtti/methods.tsv`, a body sitting", "(%s, %s; a body sitting" % (LINK, SNAP)),
    "BA-1": ("from `Tools/work/rtti/methods.tsv`:", "from %s (%s):" % (LINK, SNAP)),
    "BQ-27": ("(Tools/work/rtti/methods.tsv:", "(%s, %s:" % (LINK, SNAP)),
    "B-3": ("Outputs in `Tools/work/rtti/`.", "Outputs in `Tools/work/rtti/` (regenerable by `rtti_recover.py`; the method"
            " table is committed as %s)." % LINK),
}
if subprocess.run(["git", "diff", "--quiet", "--", OQ], cwd=HERE).returncode != 0:
    print("REFUSED: the register has uncommitted changes"); print("FAILS 1"); sys.exit(1)
raw = io.open(OQ, encoding="utf-8", newline="").read()
crlf = "\r\n" in raw
lines = raw.replace("\r\n", "\n").split("\n")
fails = 0
for rid, (old, new) in REPL.items():
    idx = [i for i, l in enumerate(lines) if l.startswith("| %s |" % rid)]
    if len(idx) != 1:
        print("MISS %s (%d rows)" % (rid, len(idx))); fails += 1; continue
    l = lines[idx[0]]
    if new in l:
        print("ALREADY", rid); continue
    if l.count(old) != 1:
        print("MISS %s (old text %d)" % (rid, l.count(old))); fails += 1; continue
    lines[idx[0]] = l.replace(old, new)
    print("PATCHED" if "--apply" in sys.argv else "WOULD PATCH", rid)
if "--apply" in sys.argv and not fails:
    t = "\n".join(lines)
    io.open(OQ, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
