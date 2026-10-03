"""check.py (SWE2-AUDIT-SPEC, 2026-10-03): the three census2 disposition amendments, re-read at the bytes.

1. S-31 `0208E680` is a qword POINTER cell: `002369A3` loads it as a qword, `002369AF` releases it through `00384500`,
   `002369B4` stores a qword back. Control: the same decoder pointed at `0208E681` finds no access (sensitive to the cell).
2. S-10 `01EF93FC` is an initialised cell: `0036D990` stores f32 1.0 to it and zeros to `01EF93F0` (qword) / `01EF93F8`
   (dword). Control: the stored constant `[01CEBBA8]` must read 1.0f - a model claiming 0.0 disagrees.
3. S-25 `AiOrderSet` already has the static route 0x02089378 in `_types/types.tsv`. Control: a lookup of a wrong base
   0x02089370 finds no route.
Exit 0 with FAILS 0."""
import os, re, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
os.chdir(ROOT / "Database/Tools/work/FABLE/pub140-scratch")
exec(open("disw.py").read().split("fn = int")[0])
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def ok(c, m):
    global fails
    print(("PASS  " if c else "FAIL  ") + m)
    fails += 0 if c else 1


def ins(s, e):
    out = []
    for i in md.disasm(bytes(d[off(s):off(e)]), s):
        t = None
        m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
        if m:
            t = i.address + i.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
        out.append((i.address, i.mnemonic, i.op_str, t))
    return out


w = ins(0x002369A3, 0x002369BB)
acc = lambda cell: [(a, mn, op) for a, mn, op, t in w if t == cell]
a1 = acc(0x0208E680)
ok(any(a == 0x002369A3 and mn == "mov" and op.startswith("rcx, qword ptr") for a, mn, op in a1), "1a 002369A3 loads qword 0208E680")
ok(any(a == 0x002369AF and mn == "call" and op == "0x384500" for a, mn, op, t in w), "1b 002369AF releases it through 00384500")
ok(any(a == 0x002369B4 and mn == "mov" and op.startswith("qword ptr") for a, mn, op in a1), "1c 002369B4 stores a qword to 0208E680")
ok(acc(0x0208E681) == [], "1C control: the decoder finds no access to 0208E681")

v = ins(0x0036D990, 0x0036D9DA)
st = {t: (mn, op) for a, mn, op, t in v if t and op.split(",")[0].strip().endswith("]")}
one = struct.unpack_from("<f", d, off(0x01CEBBA8))[0]
ok(0x01EF93FC in st and st[0x01EF93FC][0] == "movss", "2a 0036D990 stores an f32 to 01EF93FC (from [01CEBBA8])")
ok(one == 1.0, "2b the stored constant [01CEBBA8] = %r (1.0f)" % one)
ok(st.get(0x01EF93F0, ("", ""))[1].endswith(", 0") and st.get(0x01EF93F8, ("", ""))[1].endswith(", 0"),
   "2c zeros stored to 01EF93F0 (qword) and 01EF93F8 (dword)")
ok(one != 0.0, "2C control: a model claiming the cell is stored 0.0 disagrees with the bytes")

types = (ROOT / "Database/FFXII TZA/_types/types.tsv").read_text(encoding="utf-8").splitlines()
row = [l for l in types if l.startswith("AiOrderSet\t")]
ok(len(row) == 1 and "0x02089378 + setIndex * 0x170" in row[0], "3a types.tsv AiOrderSet carries the static route 0x02089378 + setIndex * 0x170")
ok(not any("0x02089370" in l for l in row), "3C control: no route at the wrong base 0x02089370")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
