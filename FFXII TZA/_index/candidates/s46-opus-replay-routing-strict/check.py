"""S-46: EXP-144's generator routing re-run under a STRICT world - named import bridges only and a closure fence - plus I3's
shared-stream continuity (OPUS, 2026-09-26).

CONTRACT-which-generator-serves-which-roll.md I1, I3, I5, I6 (and CONTRACT-gameplay-generators.md's one-draw-three-steps).
EXP-144 (_experiments/evidence/s46-generator-routing/check.py) runs every consumer and generator body as shipped, but its
import handler returns a constant for ANY import (a generic IAT boundary) and nothing fences which functions run. This file
imports EXP-144's module unchanged - its CASES, fixtures, planted states and snapshots - and replaces only its World with a
subclass that:
 - bridges exactly the imports named in BRIDGES, each with a documented fixed return; ANY other import fails the case by name;
 - fails the case if a function outside the case entry's static closure (graph call edges, plus the tail-jump targets
   listed in TAILS, which the graph lacks) is entered.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub.
Cases: EXP-144's nine, each asserted as EXP-144 asserts them (every consumer advances exactly its claimed generator), plus
 I3  lcg-loot-inliner then lcg-yaw in ONE world without re-planting: the second consumer continues the first one's stream -
     the LCG ends at three-rounds(three-rounds(seed)).
 I1  no case touches both MT states: the gameplay-MT cases never write 01F7F600, the graphics-MT cases never write 02EB3870.
 I5  gfxmt-seed writes the graphics state at 01F7F600 (the address 0015BCF0 loads with lea).
Writes result.json next to this file.
"""
import collections
import csv
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence", "s46-generator-routing"))
sys.path.insert(0, EXP)
import check as E                                          # EXP-144, unchanged; its __main__ guard keeps it from running
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP, UC_X86_REG_RSP

GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
BRIDGES = {"_time64": 0x1BADD00D, "clock": 0x0C0FFEE}     # the two CRT time sources inside 0015BCF0; fixed returns
TAILS = {0x18D680, 0x18D740, 0x18EE20, 0x328370, 0x2658B0, 0x863D30, 0x863BF0, 0x379CD0, 0x866B90}
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


BaseWorld = E.World


class StrictWorld(BaseWorld):
    ALLOWED = set()

    def _iat_stub(self, uc, addr):
        insn = self.gm.r(addr, 8)
        off = 1 if insn[0] in (0x48, 0x4C) else 0
        op = insn[off:off + 2]
        if op not in (b"\xff\x25", b"\xff\x15"):
            return False
        cell = addr + off + 6 + struct.unpack("<i", insn[off + 2:off + 6])[0]
        name = self.imports.get(cell)
        if name is None:
            return False
        short = name.split("!")[1]
        self.calls.append(("iat:" + name,))
        if short not in BRIDGES:
            self.faults.append(("unbridged import", name))
            uc.emu_stop()
            return True
        uc.reg_write(UC_X86_REG_RAX, BRIDGES[short])
        if op == b"\xff\x25":
            self._ret(uc)
        else:
            uc.reg_write(UC_X86_REG_RIP, addr + off + 6)
        return True

    def on_code(self, uc, addr, size, _):
        if addr in FSTARTS and addr not in self.ALLOWED:
            self.faults.append(("outside closure", "%08X" % addr))
            uc.emu_stop()
            return
        return BaseWorld.on_code(self, uc, addr, size, _)


E.World = StrictWorld
raw, secs = E.load_image()
imports = E.import_map(raw, secs)
results, fails = {}, []
for name, case in E.CASES.items():
    StrictWorld.ALLOWED = closure({case["entry"]} | TAILS) | TAILS
    results[name] = E.run_case(name, dict(case), raw, secs, imports)


def expect(name, cond, msg):
    if not cond:
        fails.append("%s: %s" % (name, msg))


for name, r in results.items():
    d = r["delta"]
    expect(name, not r["faults"], "faults %s" % (r["faults"],))
    own = {"lcg-": ("lcg",), "mt-": ("mt",), "prng-": ("prng",), "gfxmt-": ("gfx",)}
    for pre, mine in own.items():
        if name.startswith(pre) and name != "mt-weather-1":
            expect(name, any(k.startswith(m) for k in d for m in mine), "own generator unchanged: %s" % (d,))
            others = [t for t in ("lcg", "mt", "prng", "gfx") if t not in mine]
            expect(name, not any(k.startswith(t) for k in d for t in others), "another generator touched: %s" % (d,))
expect("mt-weather-1", results["mt-weather-1"]["delta"] == {}, "slot-1 arm touched a generator")
for nm in ("lcg-loot-inliner", "lcg-yaw"):
    expect(nm, results[nm]["after"]["lcg"] == results[nm]["lcg_expect"], "LCG end state is not three rounds")

# ---- I3: one stream across two consumers, no re-plant between them ----
StrictWorld.ALLOWED = closure({0x3185D0, 0x239210} | TAILS) | TAILS
case_l = dict(E.CASES["lcg-loot-inliner"])
w = StrictWorld(case_l, raw, secs, imports)
desc = w.alloc(0x40)
w.gm.w(0x2EBF0C0, E.qw(desc))
w.gm.w(desc + 4, E.dw(4))
w.gm.w(desc + 8, b"\x04\x00")
w.gm.w(desc + 0xC, E.dw(0))
table = w.alloc(0x40)
w.gm.w(table, bytes([60, 10, 90, 30, 55, 45, 80, 20, 5, 95, 40, 70, 15, 85, 25, 65]))
w.gm.w(E.RESOLVER_BASE, E.qw(table))
w.plant_states()
w.run(0x3185D0, regs=case_l["regs"])
after_loot = w.snapshot()["lcg"]
buf, sub, obj = w.alloc(0x200), w.alloc(0x800), w.alloc(0x800)
w.gm.w(sub + 0x6A0, E.qw(buf))
w.gm.w(obj + 0x30, E.qw(sub))
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_XMM1
w.run(0x239210, regs={UC_X86_REG_RCX: obj}, xmm={UC_X86_REG_XMM1: int.from_bytes(struct.pack("<f", -1.0) + b"\0" * 12, "little")})
after_yaw = w.snapshot()["lcg"]
i3 = {"after_loot": after_loot, "after_yaw": after_yaw, "expect_loot": hex(E.lcg3(E.PLANT_LCG)),
      "expect_yaw": hex(E.lcg3(E.lcg3(E.PLANT_LCG))), "faults": w.faults}
expect("I3", not w.faults and after_loot == i3["expect_loot"] and after_yaw == i3["expect_yaw"], "stream not continued: %s" % (i3,))

# ---- I1 / I5 ----
wrote = lambda r, tag: any(a[0] == tag and a[1] == "w" for a in r["accesses"])
i1 = {n: {"mt": wrote(r, "mt"), "gfx": wrote(r, "gfx")} for n, r in results.items()}
expect("I1", not any(v["mt"] and v["gfx"] for v in i1.values()) and i1["gfxmt-seed"]["gfx"] and not i1["gfxmt-seed"]["mt"]
       and i1["mt-roll-20000"]["mt"] and not i1["mt-roll-20000"]["gfx"], "MT states not disjoint: %s" % (i1,))
gfx_writes = sorted({int(a[2], 16) for a in results["gfxmt-seed"]["accesses"] if a[0] == "gfx" and a[1] == "w"})
expect("I5", gfx_writes and min(gfx_writes) >= E.GFX_STATE and max(gfx_writes) < E.GFX_STATE + 0x9C4, "graphics state writes elsewhere")
imports_seen = sorted({c[0] for r in results.values() for c in r["calls"] if c[0].startswith("iat:")})

out = {"ok": not fails, "failures": fails, "cases": len(results) + 3, "bridged_imports_reached": imports_seen, "bridges": BRIDGES,
       "tails": ["%08X" % t for t in sorted(TAILS)], "i3": i3, "i1": i1,
       "gfx_write_span": ["%X" % gfx_writes[0], "%X" % gfx_writes[-1]] if gfx_writes else None,
       "results": {n: {"delta": r["delta"], "faults": r["faults"], "calls": r["calls"][:12]} for n, r in results.items()}}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
print(json.dumps({"ok": out["ok"], "failures": fails, "imports": imports_seen}, indent=1))
