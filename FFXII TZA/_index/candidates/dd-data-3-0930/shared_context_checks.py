"""the-shared-drawing-context (DD batch 3, SWE2-DATA 2026-09-30), static.

S1 the §3d counts: the rip-relative operands into 0209CC48 / 0209CC50 / 0209E5A0, classified by function (a write
   is a mov whose destination is the cell), give 11 writers / 14 readers, 11 / 11 and 6 / 6. The instrument is the
   function-list-independent raw_rip_refs sweep of pe.py.
S2 the two stores of 0x7D00 into the text block's +0x8C: 002B3400 at 002B3469 and 002A4830 at 002A49C2 (r10w loaded
   at 002A492D).
S3 the fade's lag +0x9D is written by the reveal stepper 002ABF70 (002AC0BF, 002AC116, 002AC129), and its bound +0x9E
   is set to 8 by the initialiser 002AC1E0 (002AC232).
C1 control: the same sweep over 0209CC40 gives 1 writer and 25 reader functions, 121 sites - the counts §2 and the
   2026-09-13 pass reproduced by another route.
"""
import os, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import raw_rip_refs, owner, dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


refs = raw_rip_refs(0x0209CC40, 0x0209CC58) + raw_rip_refs(0x0209E5A0, 0x0209E5A8)
W, R, N = defaultdict(set), defaultdict(set), defaultdict(int)
for a, mn, op, t in refs:
    (W if (mn == "mov" and "rip" in op.split(",")[0]) else R)[t].add(owner(a))
    N[t] += 1
cnt = {t: (len(W[t]), len(R[t])) for t in (0x0209CC40, 0x0209CC48, 0x0209CC50, 0x0209E5A0)}
check("S1 0209CC48 11/14, 0209CC50 11/11, 0209E5A0 6/6 writer/reader functions",
      cnt[0x0209CC48] == (11, 14) and cnt[0x0209CC50] == (11, 11) and cnt[0x0209E5A0] == (6, 6), str(cnt))
check("C1 control: 0209CC40 1 writer, 25 readers, 121 sites", cnt[0x0209CC40] == (1, 25) and N[0x0209CC40] == 121,
      "%s %d" % (cnt[0x0209CC40], N[0x0209CC40]))
a = {x.address: x for x in dis(0x002B3400)}
b = {x.address: x for x in dis(0x002A4830)}
check("S2 the two 0x7D00 stores to +0x8C",
      a[0x002B345B].op_str == "eax, 0x7d00" and a[0x002B3469].op_str == "word ptr [rdi + 0x8c], ax"
      and b[0x002A492D].op_str == "r10d, 0x7d00" and b[0x002A49C2].op_str == "word ptr [rbx + 0x8c], r10w")
s = {x.address: x for x in dis(0x002ABF70)}
i = {x.address: x for x in dis(0x002AC1E0)}
check("S3 the stepper writes the lag +0x9D; the initialiser sets its bound +0x9E = 8",
      all(s[k].op_str.startswith("byte ptr [rbx + 0x9d]") for k in (0x002AC0BF, 0x002AC116, 0x002AC129))
      and i[0x002AC232].op_str == "byte ptr [rbx + 0x9e], 8")
print("RESULT the §3d counts reproduce by function; the +0x8C 0x7D00 defaults are 002B3400 and 002A4830; +0x9D is the "
      "stepper's lag")
print("FAILS %d" % FAILS)
