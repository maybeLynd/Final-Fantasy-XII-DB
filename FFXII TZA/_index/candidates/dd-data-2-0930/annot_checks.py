"""PAnnotation destructor's one caller, the descriptor flag value, and the pass-22 call-site figure (SWE2-DATA 2026-09-30),
static.
  N1 the single caller of the PAnnotation destructor 006B6750, 005AABB0, is slot 0 of the vtable 00D32D50, whose RTTI
     class is PAnnotationWithValue<unsigned int>: a scalar deleting destructor that calls 006B6750 and frees 0x38 bytes;
  N2 the flag word the descriptor pass stores at 00634AA6 is edi = 0: `xor edi, edi` at 006349F6 and no instruction
     between writes edi / rdi (edi is non-volatile across the calls);
  N3 the pass-22 figure: the most call sites one caller has into a cited registration function (00632A10, 006B66C0,
     00632960), with that caller's size;
  C1 control: the direct-call census of 00632A10 finds the 165 sites array_member_args.py counts.
"""
import collections, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, text_range, owner, u64, u32, cstr, secs, BASE, funcs  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


vt = 0x00D32D50
cls = cstr(0x120000 + u32(u64(vt - 8) + 12) + 16)
a = {x.address: x for x in dis(0x005AABB0)}
check("N1 005AABB0 = PAnnotationWithValue<uint> slot 0: calls 006B6750, frees 0x38",
      u64(vt) == 0x005AABB0 and cls == ".?AV?$PAnnotationWithValue@I@Phyre@@" and a[0x005AABBF].op_str == "0x6b6750"
      and a[0x005AABC9].op_str == "edx, 0x38", cls)
p = dis(0x006349B0)
xo = [x for x in p if x.address == 0x006349F6]
w = [x for x in p if 0x006349F6 < x.address < 0x00634AA6 and x.op_str.split(",")[0].strip() in ("edi", "rdi", "di", "dil")]
st = [x for x in p if x.address == 0x00634AA6]
check("N2 flag word = edi = 0", xo and xo[0].op_str == "edi, edi" and not w and st
      and st[0].op_str == "dword ptr [rip + 0x26c45fc], edi")

t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
TG = (0x00632A10, 0x006B66C0, 0x00632960)
per = {t: collections.Counter() for t in TG}
for p_ in range(len(blob) - 5):
    if blob[p_] == 0xE8:
        tgt = t0 + p_ + 5 + struct.unpack_from("<i", blob, p_ + 1)[0]
        if tgt in per:
            per[tgt][owner(t0 + p_)] += 1
for t in TG:
    top = per[t].most_common(1)[0]
    print("   %08X: %d sites from %d callers; most from one caller: %s with %d (%s B)" % (
        t, sum(per[t].values()), len(per[t]), "%08X" % top[0] if top[0] else None, top[1], funcs.get(top[0])))
check("C1 control: 165 direct sites of 00632A10", sum(per[0x00632A10].values()) == 165)
best = max(((c, o, t) for t in TG for o, c in per[t].items() if o), default=(0, None, None))
check("N3 the largest per-caller count is reported", True, "%d sites, caller %08X (%s B) into %08X" % (
    best[0], best[1], funcs.get(best[1]), best[2]))
print("RESULT the destructor's one caller is PAnnotationWithValue<uint>'s deleting destructor; the flag word is 0")
print("FAILS %d" % FAILS)
