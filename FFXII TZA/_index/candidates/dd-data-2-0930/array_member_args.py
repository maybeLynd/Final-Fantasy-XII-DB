"""PClassDataMemberArray: what callers pass as a7 / a8, the values 00632A10 stores at +0x5C / +0x58 (SWE2-DATA
2026-09-30), static census over every rel32 call site of 00632A10.

  M1 00632A10 stores a7 (its [rsp+0x80] on entry) at +0x5C and a8 ([rsp+0x88]) at +0x58, and passes a7 to the base
     00632960 while handing the base 0 for a8;
  M2 census: for each call site, the last store to the outgoing [rsp+0x30] (a7) and [rsp+0x38] (a8) in the 40
     instructions before the call, as an immediate or a register; the value sets are printed;
  M3 the class's own vtable (00D58100, eleven slots) has no read of +0x58 or +0x5C;
  C1 control: the census resolves an immediate at most sites (it can read the pattern at all).
"""
import collections, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, text_range, owner, ins_at, u64, section, funcs  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


T = 0x00632A10
a = {x.address: x for x in dis(T)}
check("M1 a7 -> +0x5C and to the base; a8 -> +0x58; base gets 0 for a8",
      a[0x00632A21].op_str == "ebx, dword ptr [rsp + 0x80]" and a[0x00632A31].op_str == "dword ptr [rsp + 0x30], ebx"
      and a[0x00632A28].op_str == "qword ptr [rsp + 0x38], 0" and a[0x00632A4D].op_str == "dword ptr [rdi + 0x5c], ebx"
      and a[0x00632A58].op_str == "eax, dword ptr [rsp + 0x88]" and a[0x00632A5F].op_str == "dword ptr [rdi + 0x58], eax")

t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
sites = []
for p in range(len(blob) - 5):
    if blob[p] == 0xE8 and t0 + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == T:
        sites.append(t0 + p)
a7, a8 = collections.Counter(), collections.Counter()
resolved = 0
for s in sites:
    fn = owner(s)
    if fn is None:
        continue
    body = dis(fn)
    idx = [i for i, x in enumerate(body) if x.address == s]
    if not idx:
        continue
    win = body[max(0, idx[0] - 40):idx[0]]
    v7 = v8 = None
    for x in win:
        if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rsp + 0x30], "):
            v7 = x.op_str.split(", ")[1]
        if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rsp + 0x38], "):
            v8 = x.op_str.split(", ")[1]
    a7[v7] += 1
    a8[v8] += 1
    if v7 is not None and v7.startswith("0x") or (v7 or "").isdigit():
        resolved += 1
print("   %d call sites; a7 (+0x5C) values %s" % (len(sites), dict(a7.most_common(12))))
print("   a8 (+0x58) values %s" % dict(a8.most_common(12)))
check("M2 the census covers the call sites", len(sites) > 0, "%d sites" % len(sites))
vt = 0x00D58100
reads = []
for i in range(11):
    f = u64(vt + 8 * i)
    if f in funcs:
        reads += [x.address for x in dis(f) if ("+ 0x58]" in x.op_str or "+ 0x5c]" in x.op_str) and "rsp" not in x.op_str]
check("M3 no vtable slot of the class reads +0x58 / +0x5C", not reads, " ".join("%08X" % r for r in reads))
check("C1 control: most sites resolve a7 to an immediate", resolved * 2 > len(sites), "%d of %d" % (resolved, len(sites)))
print("RESULT the value sets above are what +0x5C / +0x58 hold at registration; the class's own methods never read them")
print("FAILS %d" % FAILS)
