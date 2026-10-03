"""apply.py [--apply] - correct FABLE's attribution of the SD-81 answer (FABLE, 2026-10-03, final-audit pass 28): the
record and commit 08f4c0821 are SWE2-ORACLE's (assigned by OPUS), not OPUS's. Two places FABLE wrote in 6c817c026:
the-ordered-container-runtime.md section 7 and register row SD-81. Refuses while either file has uncommitted changes.
Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
EDITS = [
    (os.path.join(DB, "24-Compiler-And-CRT-Runtime", "Cxx-Runtime-Families", "the-ordered-container-runtime.md"),
     "*(SD-81 answered 2026-09-30 by OPUS `08f4c0821`, [record]",
     "*(SD-81 answered 2026-09-30 by ~~OPUS~~ SWE2-ORACLE (assigned by OPUS) `08f4c0821` *(attribution corrected "
     "2026-10-03, FABLE: the record and the commit are SWE2-ORACLE's)*, [record]"),
    (os.path.join(DB, "_index", "OPEN-QUESTIONS.md"),
     "**ANSWERED 2026-09-30 (OPUS `08f4c0821`, static;",
     "**ANSWERED 2026-09-30 (~~OPUS~~ SWE2-ORACLE, assigned by OPUS, `08f4c0821`, static; attribution corrected "
     "2026-10-03 by FABLE;"),
]
fails, todo = 0, []
for p, old, new in EDITS:
    if subprocess.run(["git", "diff", "--quiet", "--", p], cwd=HERE).returncode != 0:
        print("REFUSED: %s has uncommitted changes" % os.path.basename(p)); fails += 1; continue
    raw = io.open(p, encoding="utf-8", newline="").read()
    if new in raw:
        print("ALREADY %s" % os.path.basename(p)); continue
    if raw.count(old) != 1:
        print("MISS %s (%d)" % (os.path.basename(p), raw.count(old))); fails += 1; continue
    todo.append((p, raw.replace(old, new)))
if fails == 0 and "--apply" in sys.argv:
    for p, text in todo:
        io.open(p, "w", encoding="utf-8", newline="").write(text); print("PATCHED %s" % os.path.basename(p))
elif fails == 0:
    for p, _ in todo:
        print("WOULD PATCH %s" % os.path.basename(p))
print("FAILS %d" % fails)
