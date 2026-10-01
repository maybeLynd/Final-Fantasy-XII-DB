"""Byte-granular direct-reference census of EeVu0RegisterBank +0x224..+0x287 (022D9134..022D9197).
Width from the memory operand (capstone op.size); direction from capstone regs/operand access."""
import collections
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import reg_tracking as RT
import json
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import data_xref_scan as X  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_READ, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
G = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE, LO, HI = [int(x, 16) for x in sys.argv[1:4]]
blob = open(EXE, "rb").read()
secs = X.sections_of(blob)
res = X.scan(blob, secs, X.entries(G), set(range(LO, HI)))
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for _n, ro, sz, v in secs:
        if v <= va < v + sz:
            return ro + (va - v)


acc = collections.defaultdict(lambda: {"r": 0, "w": 0, "sites": set(), "fns": set()})
for a, hits in res.items():
    for ins, mn, ops, f in hits:
        o = off(ins)
        i = next(md.disasm(blob[o:o + 15], ins, 1))
        for oi, op in enumerate(i.operands):
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and i.address + i.size + op.mem.disp == a:
                w = op.size
                if i.mnemonic == "lea":
                    w = 0
                k = (a - BASE, w)
                kind = RT.op_kind(i, op, oi)  # shared policy (OPUS 2026-09-28); 'addr' / '?' count as neither
                if kind in ("r", "rw"):
                    acc[k]["r"] += 1
                if kind in ("w", "rw"):
                    acc[k]["w"] += 1
                if i.mnemonic == "lea":
                    acc[k]["r"] += 0
                acc[k]["sites"].add(ins)
                acc[k]["fns"].add(f)
out = []
for (o, w), v in sorted(acc.items()):
    out.append({"off": o, "w": w, "r": v["r"], "wr": v["w"], "sites": ["%08X" % s for s in sorted(v["sites"])],
                "fns": ["%08X" % s for s in sorted(v["fns"])]})
    print("+0x%03X w%-2d r%-3d w%-3d fns=%d  %s" % (o, w, v["r"], v["w"], len(v["fns"]), ",".join("%08X" % s for s in sorted(v["fns"])[:5])))
json.dump(out, open("span_%s.json" % sys.argv[1], "w"), indent=1)
covered = set()
for (o, w) in acc:
    covered |= set(range(o, o + max(w, 1)))
print("unreached bytes:", [hex(b) for b in range(LO - BASE, HI - BASE) if b not in covered])
