"""pass6_rows.py - SWE2-AUDIT-SPEC (2026-09-30): print, for each of the 15 OPUS pass-6 disposition subjects named in
OPUS-REQ-AUDITSPEC-PASS6-OPUS-ROWS-0930, every REVIEW line check_banned_evidence.py raises on that page, with two lines
of context, and whether the registry row's evidence hash still matches (i.e. whether the signature applies).
Read-only: imports the gate's own sweep() and dispositions.Registry so the lines are exactly the gate's."""
import os, sys
K = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
sys.path.insert(0, K)
import check_banned_evidence as G
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
SUBJ = """_experiments/evidence/uc1-extent-collision-opus/README.md
_index/candidates/b2b-opus-funclet-section-split/README.md
_index/candidates/con198-exit-attribution-0930/README.md
_index/candidates/fragment-size-sweep-0929/README.md
_index/candidates/heading-full-extent-repair-0929/README.md
_index/candidates/k14-closure-stores-0930/README.md
_index/candidates/pre-audit-dry-run-0930/README.md
_index/candidates/uc1-band-257-up/README.md
_index/candidates/uc1-extent-collision-consumer-check.md
_index/candidates/uc1-held-rows-opus/README.md
_index/candidates/uc1-pass2-extent-and-tables.md
_index/candidates/uq2-caller-route/README.md
04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md
17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md
_index/candidates/text-gap-append-0930/README.md""".split()
files, counts, review = G.sweep(DB)
reg = G.DISP.Registry(DB, "check_banned_evidence.py")
by = {}
for p, i, t in review:
    by.setdefault(p.replace(os.sep, "/"), []).append((i, t))
n = 0
for s in SUBJ:
    lines = by.get(s, [])
    joined = chr(10).join(t for _, t in lines)
    print("=" * 100)
    print("%s  REVIEW lines: %d  signature applies: %s" % (s, len(lines), reg.suppressed(s, joined)))
    src = open(os.path.join(DB, s), encoding="utf-8").read().splitlines()
    for i, t in lines:
        n += 1
        print("  L%d:" % i)
        for k in range(max(1, i - 2), min(len(src), i + 1) + 1):
            print("    %s%4d| %s" % (">" if k == i else " ", k, src[k - 1][:400]))
print("total REVIEW lines on the 15 subjects:", n)
