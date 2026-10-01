"""RC-32 support sweep: which listed functions index a 0x20-stride slot array whose base is a dword at +0x10 of the
same object (the `.mg` sub-mesh name-slot directory form: slot j = sub + s32[sub+0x10] + j*0x20)?

Pattern (per function, linear disassembly): an instruction `movsxd R, dword ptr [B + 0x10]` followed within 10
instructions by `shl S, 5` (the 0x20 stride). Positive controls: 00555A50 (the slot getter) and 00555400 (the
slot loop at 00555660) must be reported. Prints each hit and FAILS N (controls missing)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import funcs, dis, names

hits = []
for fn in sorted(funcs):
    if funcs[fn] <= 0 or funcs[fn] > 0x20000:
        continue
    try:
        ins = dis(fn)
    except Exception:
        continue
    for i, x in enumerate(ins):
        if x.mnemonic == "movsxd" and x.op_str.endswith("+ 0x10]") and "dword ptr" in x.op_str:
            for y in ins[i + 1:i + 11]:
                if y.mnemonic == "shl" and y.op_str.endswith(", 5"):
                    hits.append((fn, x.address, x.op_str, y.address))
                    break
for fn, a, s, b in hits:
    print(f"{fn:08X} {names.get(fn, '')}  {a:08X} movsxd {s}  shl@{b:08X}")
got = {h[0] for h in hits}
fails = 0
for c in (0x00555A50, 0x00555400):
    ok = c in got
    print(f"control {c:08X}: {'PASS' if ok else 'FAIL'}")
    fails += not ok
print(f"hits {len(hits)} in {len(got)} functions")
print(f"FAILS {fails}")
