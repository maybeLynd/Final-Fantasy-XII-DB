"""semantic_refs.py - BM-2 vs UQ-277 (FABLE, 2026-09-30): which functions reference the 19 ChannelSemantic entries
(01F2CE40, stride 0x18) at the entry or its +0x08 link field? UQ-277 says: the composer 005C72A0, 005C6F20 (the transform
three), the 19 getters 00160BF0..00161070, the static initialiser 005C5C80 and the teardown 005CB150 - nothing else.
FAILS if any other function references an entry. Control: the composer 005C72A0 must be found."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
LO, N, ST = 0x01F2CE40, 19, 0x18
want = set()
for k in range(N):
    want |= {LO + k * ST, LO + k * ST + 8}
decoded, _raw = tk.rip_refs(LO, LO + N * ST)   # decoded entries are (insn, opindex, target)
pairs = [(x.address, t) for x, _k, t in decoded]
owners = {}
for s, tgt in pairs:
    if tgt in want:
        o, _ = tk.owner(s)
        owners.setdefault(o, set()).add(tgt)
getters = {o for o in owners if 0x00160BF0 <= o <= 0x00161070}
named = {0x005C72A0, 0x005C6F20, 0x005C5C80, 0x005CB150}
other = set(owners) - getters - named
for o in sorted(owners):
    print("%08X %-48s refs %d" % (o, tk.fname(o)[:48], len(owners[o])))
print("getters %d, named %s, other %s" % (len(getters), sorted("%08X" % o for o in named & set(owners)), sorted("%08X" % o for o in other)))
ctl = 0x005C72A0 in owners
print("CONTROL composer 005C72A0 found:", "PASS" if ctl else "FAIL")
fails = (0 if ctl else 1) + (1 if other else 0)
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
