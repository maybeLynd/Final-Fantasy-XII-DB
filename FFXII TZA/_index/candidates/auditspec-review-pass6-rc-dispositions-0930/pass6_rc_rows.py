"""pass6_rows.py - SWE2-AUDIT-SPEC (2026-09-30): print, for each of the 5 ORACLE-record pass-6 disposition subjects named in
ORACLE-REQ-AUDITSPEC-PASS6-RC-DISPOSITIONS-0930, every REVIEW line check_banned_evidence.py raises on that page, with two lines
of context, and whether the registry row's evidence hash still matches (i.e. whether the signature applies).
Read-only: imports the gate's own sweep() and dispositions.Registry so the lines are exactly the gate's."""
import os, sys
K = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
sys.path.insert(0, K)
import check_banned_evidence as G
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
SUBJ = """_index/candidates/rc11-arena-ten-0930/README.md
_index/candidates/rc12-footer-channels-runstate-0930/README.md
_index/candidates/rc20-float-push-verbs-0930/README.md
_index/candidates/rc22-as7-pages-0930/README.md
_index/candidates/rc8-cascade-count-0930/README.md""".split()
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
