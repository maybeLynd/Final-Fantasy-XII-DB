"""con195_197_202.py - SWE2-AUDIT-SPEC (batch-9 review, 2026-09-29). Independent raw-index checks.

CON-195: the fef name table is seeded at start-up through rel32 calls: 0041E3A0 (0041E40B) -> 00409F80 (00409F84) ->
         0040A230, and 0041E3A0 sits on the direct chain 0017D000 -> 0017D4C0 -> 0022A0B0 -> 003325C0 -> 003325D0 ->
         0041E3A0. Each edge is checked in the raw E8/E9/jcc index.
CON-197: 005FD050 returns one static (02CC0410) on both exits.
CON-202: 00249320's direct callers are exactly 003933F0, 00393FF0, 003F4840, 00404060 (by owning .pdata root), and the
         title call is 00394048 in 00393FF0; 003939B0 makes no direct call to it.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ddres-b1-0930"))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-opus-batch8-0929"))
import io, contextlib
import ov31_indep as T  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import disp_4a2 as R  # noqa: E402  (its .pdata root(); its own census output is discarded)
import b8dis  # noqa: E402

fails = 0


def edge(caller_root, target, site=None):
    global fails
    cs = T.rel32_callers(target) + T.jcc_callers(target)
    roots = {R.root(int(c.split()[0], 16)): c for c in cs}
    ok = caller_root in roots and (site is None or any(c.startswith("%08X" % site) for c in cs))
    fails += not ok
    print("%s  %08X -> %08X%s   (callers of target by root: %s)" % ("PASS" if ok else "FAIL", caller_root, target,
          " at %08X" % site if site else "", ", ".join("%08X" % r if r else "--------" for r in sorted(roots, key=lambda x: x or 0))))


print("== CON-195 chain")
for a, b, s in ((0x0017D000, 0x0017D4C0, None), (0x0017D4C0, 0x0022A0B0, None), (0x0022A0B0, 0x003325C0, None),
                (0x003325C0, 0x003325D0, None), (0x003325D0, 0x0041E3A0, None), (0x0041E3A0, 0x00409F80, 0x0041E40B),
                (0x00409F80, 0x0040A230, 0x00409F84)):
    edge(a, b, s)
print("== CON-197")
b8dis.dump(0x005FD050, 0x005FD080)
print("== CON-202")
cs = T.rel32_callers(0x00249320) + T.jcc_callers(0x00249320)
roots = sorted(set(R.root(int(c.split()[0], 16)) for c in cs), key=lambda x: x or 0)
want = [0x003933F0, 0x00393FF0, 0x003F4840, 0x00404060]
ok = roots == want and any(c.startswith("00394048") for c in cs) and 0x003939B0 not in roots
fails += not ok
print("%s  callers of 00249320: %s; roots %s" % ("PASS" if ok else "FAIL", cs, ["%08X" % r for r in roots]))
print("FAILS %d" % fails)
