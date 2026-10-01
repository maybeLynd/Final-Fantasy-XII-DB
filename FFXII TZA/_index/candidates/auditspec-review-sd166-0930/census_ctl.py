"""census_ctl.py - SWE2-AUDIT-SPEC (2026-09-30): positive control for S1's "never called" on class-2 verbs.
Runs the kit's script_verb_census.census() (read-only import) with EVERY catalogued verb id of class 2 (0x2000..0x2FFF)
and class 3 (0x3000..0x3FFF) wanted, and prints the call count per class and per id. If class-3 ids (btlAtel*) are found
but no class-2 id is, the decoder does see ids >= 0x1000 and the class-2 absence is a property of the data.
"""
import collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, K)
import script_verb_census as S  # noqa: E402

cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(S.DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402
verbs = G.load_verbs()
os.chdir(cwd)
want = {k: v[2] for k, v in verbs.items() if 0x2000 <= k < 0x4000}
print("wanted ids: class 2 %d, class 3 %d" % (sum(1 for k in want if k < 0x3000), sum(1 for k in want if k >= 0x3000)))
rows, total = S.census(want)
print("CALL-family sites decoded: %d; matching: %d" % (total, len(rows)))
byc = collections.Counter(int(r[3], 16) >> 12 for r in rows)
print("matches by class: %s" % dict(sorted(byc.items())))
byid = collections.Counter(r[3] for r in rows)
for k, n in sorted(byid.items()):
    print("   %s %-32s %d" % (k, want[int(k, 16)], n))
