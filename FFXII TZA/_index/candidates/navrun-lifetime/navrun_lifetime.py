"""navrun_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. The NavRunStateBlock copy's lifetime, which its type row
left OPEN ("the copy's own release was not found"). STATIC, certified EXE only (other images REFUSED, exit 2).

  A1 allocation (already recorded): the map-pack loader 00378BC0 copies the nav section into a fresh block and stores it
     in the pack slot 02ADCFE8 (00378D4C).
  B1 bind: 00378120 moves the slot into the ACTIVE slot 02ADD008 (00378198 / 0037819F) and publishes it with 00384160
     (003781A6), which stores 02AEDFB0 (0038416D).
  R1 release: 00378230 loads 02ADD008 (003782AF), frees it through 003697F0 (003782BB) - the same null-guarded free the
     loader uses on the pack's original (00378D33) - zeroes the active slot (003782C2) and calls 00384160(0) (003782C9).
  R2 00384160 null-guards its argument: test rcx, rcx / je to the epilogue (00384164 / 00384167 -> 003842CF), so the
     teardown call does NOT clear 02AEDFB0. The global keeps the freed block's address.
  C1 the only clear of 02AEDFB0 is Navigation_ClearDataset 00383A20 (a qword store of 0), called from 002341C0 and
     002368D0 (BattleStorage_InitializeWorkArrays) per the call graph; the next bind overwrites it (B1).
  S  REGRESSION: the NavRunStateBlock type row states the release and the window (FAILS before the patch)
  P1 the readiness predicate 00383C80 is 'cmp qword [02AEDFB0], rax(0)': it cannot tell a freed block from a live one.
Not claimed: whether any query runs between R1 and C1 / the next bind (call order across 002628B0 / 00378A60 and the
reset paths is not established here); no live observation.
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None
    return x.mnemonic, x.op_str, t
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

check("A1", at(0x378D4C)[0] == "mov" and at(0x378D4C)[2] == 0x2ADCFE8 and at(0x378D4C)[1].endswith("rdi"),
      "00378D4C stores the copy in the pack slot 02ADCFE8")
check("B1", at(0x378198)[2] == 0x2ADCFE8 and at(0x37819F)[2] == 0x2ADD008 and at(0x37819F)[1].endswith("rcx")
      and at(0x3781A6)[:2] == ("call", "0x384160") and at(0x38416D)[2] == 0x2AEDFB0,
      "00378120 moves 02ADCFE8 -> 02ADD008 and publishes it through 00384160 into 02AEDFB0")
check("R1", at(0x3782AF)[2] == 0x2ADD008 and at(0x3782BB)[:2] == ("call", "0x3697f0") and at(0x378D33)[:2] == ("call", "0x3697f0")
      and at(0x3782C2)[2] == 0x2ADD008 and at(0x3782C0)[:2] == ("xor", "ecx, ecx") and at(0x3782C9)[:2] == ("call", "0x384160"),
      "00378230 frees [02ADD008] with 003697F0, zeroes the slot and calls 00384160(0)")
check("R2", at(0x384164)[:2] == ("test", "rcx, rcx") and at(0x384167)[:2] == ("je", "0x3842cf")
      and at(0x3842CF)[:2] == ("add", "rsp, 0x28"),
      "00384160(0) returns without storing: 02AEDFB0 keeps the freed address")
edges = [l.rstrip("\n").split("\t") for l in open(os.path.join(ROOT, "Tools", "work", "graph", "edges.tsv"), encoding="utf-8")]
callers = sorted({e[0] for e in edges if len(e) > 1 and e[1] == "00383A20"})
check("C1", at(0x383A20)[0] == "mov" and at(0x383A20)[1].endswith(", 0") and at(0x383A20)[2] == 0x2AEDFB0
      and callers == ["002341C0", "002368D0"], "Navigation_ClearDataset 00383A20 clears 02AEDFB0; callers %s" % callers)
check("P1", at(0x383C82)[:2] == ("cmp", "qword ptr [rip + 0x276a327], rax") and at(0x383C82)[2] == 0x2AEDFB0,
      "the readiness predicate 00383C80 compares the pointer with zero only")
T = {l.split("	")[0]: l.split("	") for l in open(os.path.join(ROOT, "FFXII TZA", "_types", "types.tsv"), encoding="utf-8").read().splitlines()}
row = T.get("NavRunStateBlock", [""] * 7)
check("S", "RELEASE FOUND 2026-09-28" in row[6] and "00383A20" in row[6] and "sole NON-NULL setter" in row[3],
      "the type row records the release, the dangling window and the qualified setter (FAILS before the patch)")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
