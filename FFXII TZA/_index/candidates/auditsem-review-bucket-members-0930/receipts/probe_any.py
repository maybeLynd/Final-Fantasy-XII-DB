"""SWE2-AUDIT-SEM: every rel32 call site in .text (to ANY target) whose constant arg registers hold both K and I
(any two of rcx/rdx/r8/r9). usage: probe_any.py K I [K I ...]. Control pairs are given the same way."""
import sys, collections
import reqsites as R, wrappers as W
pairs = [(int(sys.argv[i], 0), int(sys.argv[i + 1], 0)) for i in range(1, len(sys.argv), 2)]
found = collections.defaultdict(list)
n = 0
for tgt, sites in R.refs.items():
    for c, kind in sites:
        if kind != "call":
            continue
        n += 1
        k = W.const_regs(R.decode_back(c, 12))
        vals = [k.get(r) for r in ("rcx", "rdx", "r8", "r9")]
        for K, I in pairs:
            if K in vals and I in vals and (K != I or vals.count(K) > 1):
                found[(K, I)].append("%08X->%08X %s" % (c, tgt, [None if v is None else hex(v) for v in vals]))
print("direct call sites scanned:", n)
for p in pairs:
    print("pair (%s,%s): %d" % (hex(p[0]), hex(p[1]), len(found[p])))
    for s in found[p][:12]:
        print("   ", s)
