"""gb2_env_class.py - GB-2: every consumer of the environment class 02099DA8, and whether any tests the value 4
(FABLE, Claude Opus 5.5, 2026-09-27). Static plus the shipped .ard order sets.

  E1 image-wide RIP-relative census of 02099DA8: one read (the getter 00263E10) and one write (0026DA26, in the
     field-record initialiser); no absolute or RVA pointer to the global, the getter or its thunk.
  E2 the getter is reached only through the 5-byte thunk 00321490, whose direct E8 callers are exactly the combat
     stage's five sites in 0038B220 and one site in AiOrder_EvaluateTargetSelector (00303059).
  E3 the stage compares the value only for equality with 0, 0, 2, 1, 3 (0038B2A8, 0038B3F4, 0038B478, 0038B4FE,
     0038B584) - no arm for 4.
  E4 the selector arm at 00303059 is opcode 48/49 operand 0: getter == threshold (sete). In the 166 shipped .ard
     files it occurs 17 times, every one with threshold 0 (the Rain class), and none tests 4.
     Controls: the same census reproduces the page's opcode 7 (4,160) and opcode 6 (280) totals and 50,050 records.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import glob, os, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
WORK = ROOT / "Database/Tools/work"
d = (WORK / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def va_of(fo):
    for vs, va, rs, ro in secs:
        if ro <= fo < ro + rs: return fo - ro + va + BASE
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def one(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
text = [x for x in secs if x[1] == 0x1000][0]
lo, hi = text[3], text[3] + text[2]
# E1: rip-relative operands resolving to 02099DA8 (any instruction length), confirmed by decoding at the start
refs = []
for i in range(lo, hi - 4):
    for back in range(2, 8):
        s = i - back
        if s < lo: continue
        try:
            x = next(cs.disasm(d[s:s + 16], va_of(s)))
        except StopIteration:
            continue
        if "rip" in x.op_str and x.size >= back + 4 and s + x.size - 4 == i:
            tgt = x.address + x.size + struct.unpack_from("<i", d, i)[0]
            if tgt == 0x02099DA8: refs.append((x.address, x.mnemonic, x.op_str))
        break
refs = sorted(set(refs))
ptrs = sum(d.count(struct.pack("<Q", v)) + d.count(struct.pack("<I", v - BASE)) for v in (0x02099DA8, 0x263E10, 0x321490))
check("E1 one read (the getter) and one write, no pointer to the global or its getter",
      [a for a, _, _ in refs] == [0x263E10, 0x26DA26] and ptrs == 0, str(["%08X %s %s" % r for r in refs]) + " ptrs %d" % ptrs)
calls = []
for i in range(lo, hi - 5):
    if d[i] in (0xE8, 0xE9):
        va = va_of(i)
        t = va + 5 + struct.unpack_from("<i", d, i + 1)[0]
        if t in (0x263E10, 0x321490):
            x = one(va)
            if x.size == 5 and x.mnemonic in ("call", "jmp"): calls.append((va, x.mnemonic, t))
check("E2 the getter is reached only through its thunk; six direct call sites",
      sorted((a, t) for a, m, t in calls) == sorted([(0x321490, 0x263E10)] + [(a, 0x321490) for a in (0x38B2A3, 0x38B3EF, 0x38B473, 0x38B4F9, 0x38B57F, 0x303059)]),
      str(["%08X %s %X" % c for c in calls]))
cmps = [("%s %s" % (one(a).mnemonic, one(a).op_str)) for a in (0x38B2A8, 0x38B3F4, 0x38B478, 0x38B4FE, 0x38B584)]
check("E3 the stage tests 0, 0, 2, 1, 3 only", cmps == ["test eax, eax", "test eax, eax", "cmp eax, 2", "cmp eax, 1", "cmp eax, 3"], str(cmps))
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]; u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
s16 = lambda b, o: struct.unpack_from("<h", b, o)[0]
recs = 0; op7 = op6 = 0; env = []
for f in sorted(glob.glob(str(WORK / "repos-3f/ard/ard/*.ard"))):
    b = open(f, "rb").read(); s1 = u32(b, 0x14)
    if not s1: continue
    cnt = u16(b, s1); so = [u32(b, s1 + 4 + 4 * i) for i in range(cnt + 1)]
    for k in range(cnt):
        base = s1 + so[k]; nr = sum(b[base:base + 12])
        for r in range(nr):
            o = base + 0x20 + 24 * r; recs += 1
            for e in range(3):
                eo = o + 6 + 6 * e; operand, opcode, thr = b[eo + 2], b[eo + 3], s16(b, eo + 4)
                op7 += opcode == 7; op6 += opcode == 6
                if opcode in (48, 49): env.append((opcode, operand, thr))
arm = [("%s %s" % (one(a).mnemonic, one(a).op_str)) for a in (0x30305E, 0x303063)]
check("E4 opcode 48 operand 0 is getter == threshold; 17 shipped, all threshold 0; census controls reproduce",
      arm == ["cmp eax, esi", "sete cl"] and recs == 50050 and op7 == 4160 and op6 == 280
      and len(env) == 17 and set(env) == {(48, 0, 0)},
      "records %d op7 %d op6 %d env %s" % (recs, op7, op6, sorted(set(env))))
print("FAILS", fails)
sys.exit(1 if fails else 0)
