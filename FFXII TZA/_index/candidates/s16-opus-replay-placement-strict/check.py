"""S-16: EXP-145's spawn-placement execution re-run under a STRICT world - one named import bridge and a closure fence
(OPUS, 2026-09-26).

CONTRACT-spawn-placement.md I1..I5, I7 and I8 (and I6's producer half). EXP-145 (_experiments/evidence/spawn-placement-exec/
check.py) runs 00234AF0 in both modes, 00235330 / 00235340, 003209C0 -> 003DFD00, the probe 00234DA0, the validator 00322C50,
the LCG draws, the sine table and the region transform as shipped; its one scripted boundary is the tail thunk 00861F02
(`jmp qword [008C2BD0]`), which block 294 resolved to the CRT import api-ms-win-crt-math-l1-1-0.dll!atan2f.
This file imports EXP-145's module UNCHANGED - its cases, fixtures and every assertion in its check() - and replaces only:
 - its World, with a subclass that treats 00861F02 as what it is, the named import atan2f (resolved from the import directory
   at run time and asserted to be atan2f; y = xmm0, x = xmm1, the registers the shipped caller loads), fails the case on ANY
   other import, and fails the case if a function outside the static closure of the case's entries (graph call edges, plus
   the tail-jump targets in TAILS) is entered;
 - its RESULT path, so EXP-145's result.json is left as published and this run's result lands here.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub.
Writes result.json next to this file (EXP-145's check() writes it) and strict.json (the bridge / fence record).
"""
import collections
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence", "spawn-placement-exec"))
sys.path.insert(0, EXP)
import check as E                                          # EXP-145, unchanged; its __main__ guard keeps it from running
from unicorn.x86_const import UC_X86_REG_XMM0, UC_X86_REG_XMM1

GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
ENTRIES = {0x234AF0, 0x235330, 0x235340, 0x3209C0}
TAILS = {0x3DFD00, 0x328370, 0x31AC90, 0x861F02, 0x3A1960}      # 003A1960: the squared-XZ distance, reached by the thunk 0031E620 (jmp)
graph = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    if row["callee_external"] != "true":
        graph[int(row["caller"], 16)].add(int(row["callee"], 16))
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(os.path.join(GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")


def closure(starts):
    seen, st = set(), list(starts)
    while st:
        x = st.pop()
        if x not in seen:
            seen.add(x)
            st.extend(graph[x])
    return seen


ALLOWED = closure(ENTRIES | TAILS) | TAILS
BaseWorld = E.World
record = {"atan2f_calls": 0, "import_names": set(), "outside": [], "unbridged": []}


class StrictWorld(BaseWorld):
    def on_code(self, uc, addr, size, _):
        if addr == 0x861F02:
            name = self.imports.get(0x8C2BD0, "?")
            record["import_names"].add(name)
            if not name.endswith("!atan2f"):
                self.faults.append(("0x861F02 is not atan2f", name))
                uc.emu_stop()
                return
            record["atan2f_calls"] += 1
            y, x = E.fx(uc.reg_read(UC_X86_REG_XMM0)), E.fx(uc.reg_read(UC_X86_REG_XMM1))
            self.calls.append(("import:atan2f", y, x))
            uc.reg_write(UC_X86_REG_XMM0, E.xf(math.atan2(y, x)))
            self._ret(uc)
            return
        if addr in FSTARTS and addr not in ALLOWED:
            record["outside"].append("%08X" % addr)
            self.faults.append(("outside closure", "%08X" % addr))
            uc.emu_stop()
            return
        return BaseWorld.on_code(self, uc, addr, size, _)

    def _iat_stub(self, uc, addr):
        insn = self.gm.r(addr, 8)
        off = 1 if insn[0] in (0x48, 0x4C) else 0
        if insn[off:off + 2] in (b"\xff\x25", b"\xff\x15"):
            import struct
            cell = addr + off + 6 + struct.unpack("<i", insn[off + 2:off + 6])[0]
            name = self.imports.get(cell)
            if name is not None:
                record["unbridged"].append(name)
                self.faults.append(("unbridged import", name))
                uc.emu_stop()
                return True
        return False


E.World = StrictWorld
E.RESULT = os.path.join(HERE, "result.json")
E.check()
res = json.load(open(E.RESULT))
out = {"ok": not res["failures"] and not record["outside"] and not record["unbridged"] and record["import_names"] == {"api-ms-win-crt-math-l1-1-0.dll!atan2f"},
       "cases": res["cases"], "failures": res["failures"], "atan2f_calls": record["atan2f_calls"],
       "import_at_008C2BD0": sorted(record["import_names"]), "outside_closure": record["outside"], "unbridged_imports": record["unbridged"],
       "allowed_functions": len(ALLOWED), "tails": ["%08X" % t for t in sorted(TAILS)]}
json.dump(out, open(os.path.join(HERE, "strict.json"), "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1))
