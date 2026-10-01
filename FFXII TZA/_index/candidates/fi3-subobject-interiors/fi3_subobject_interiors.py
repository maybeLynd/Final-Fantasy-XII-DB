"""fi3_subobject_interiors.py - FI-3: the actor storage record's four embedded sub-objects already have their interiors
published (FABLE, Claude Opus 5.5, 2026-09-26; found by a delegated read-only pass, re-checked here).

  S1 the planter 00266AD0 plants the four interior pointers for the sequence-5..7 shape: +0xB8 = rec+0x120
     (00266B54, 00266B5B), +0xC0 = +0x120 + 0x230 = rec+0x350 (00266B62, 00266B68), +0xA0 = +0x350 + 0x188 = rec+0x4D8
     (00266B6F, 00266B79); +0xA8 is stored at 00266B9B.
  S2 each sub-object's interior is typed in the store (_types/fields.tsv): MovementContext 80 rows, SecondaryContext 28,
     ActorResourceEntry 12, ActorWaitSlot 15.
  S3 the pages that census them exist and say so: the movement and secondary context censuses page (its §2.3 and §2.4
     pointer-seeded censuses), and the record page's wait-slot and resource-entry sections.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
P = {0x266B54: "lea rax, [rdx + 0x120]", 0x266B5B: "mov qword ptr [rdx + 0xb8], rax", 0x266B62: "add rax, 0x230",
     0x266B68: "mov qword ptr [rdx + 0xc0], rax", 0x266B6F: "lea r8, [rax + 0x188]", 0x266B79: "mov qword ptr [rdx + 0xa0], r8"}
check("S1 the planter plants +0x120 / +0x350 / +0x4D8 into +0xB8 / +0xC0 / +0xA0, and stores +0xA8",
      all(at(a) == s for a, s in P.items()) and at(0x266B9B).startswith("mov qword ptr [rdx + 0xa8]"),
      str({"%08X" % a: at(a) for a in P if at(a) != P[a]}) + " | " + at(0x266B9B))
counts = {}
for line in open(DB / "_types/fields.tsv", encoding="utf-8"):
    t = line.split("\t", 1)[0]
    counts[t] = counts.get(t, 0) + 1
want = {"MovementContext": 80, "SecondaryContext": 28, "ActorResourceEntry": 12, "ActorWaitSlot": 15}
check("S2 the store types each interior", all(counts.get(t, 0) >= c for t, c in want.items()), str({t: counts.get(t, 0) for t in want}))
cen = (DB / "04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md").read_text(encoding="utf-8")
rec = (DB / "04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md").read_text(encoding="utf-8")
check("S3 the census page carries the pointer-seeded movement and secondary context censuses; the record page the wait slots",
      "movement-context-accesses.tsv" in cen and "FS-2" in cen and "FS-3" in cen and "waitSlotArray" in rec)
print("FAILS", fails)
sys.exit(1 if fails else 0)
