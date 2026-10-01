"""bf5_inert_opcode_census.py - BF-5: does shipped .ebp bytecode ever emit the six opcodes the interpreter sends to its
default handler? (FABLE, Claude Opus 5.5, 2026-09-26)

The six, by the corrected mnemonic table (worldactor-scriptvm-interpreter.md §11): 0x01 LABEL, 0x02 TAG,
0x19 OPUMINUS, 0x1A OPFIXADRS, 0x31 DRET, 0x47 LONGCODESTART. The register row still quotes the rotated names
(TAG / SYSHALT / OPFIXADRS / PUSHA / REQWAIT / PUSHV) that the page withdrew.

  B1 the interpreter: the opcode table sends all six to the default handler 0025E60A (checked on the table's own
     entries), and the operand pre-decode threshold is `cmp r12b, 0x47 / jb` (0025E5A9).
  B2 the corpus: every distinct .ebp in the extract (all language packs, deduplicated by content). The code section
     and script starts are located as members/gen_req_channel_census.py does (section at 0x80, tag 0x8000000B,
     directory at +0x18, stride 0x30, start at +8). Each script is decoded linearly: 1 byte below 0x48, 3 bytes at or
     above.
     Controls: the decode must reach the end of every script with no out-of-range opcode, and the ordinary opcodes
     must be present (CALL 0x58, PUSHI 0x4E, RET 0x2D).
  B3 none of the six occurs at an opcode position. Control: all six byte values do occur inside u16 operands, so the
     zero is a property of instruction positions, not of the bytes. Scope: the .ebp script corpus; bytecode from any
     other source is not covered.
Prints the count of each of the six and PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, hashlib, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
SIX = {0x01: "LABEL", 0x02: "TAG", 0x19: "OPUMINUS", 0x1A: "OPFIXADRS", 0x31: "DRET", 0x47: "LONGCODESTART"}
# the interpreter's opcode jump table: find the indirect jump that dispatches on the opcode and read its table
L = list(cs.disasm(d[off(0x25E500):off(0x25E500) + 0x140], 0x25E500))
T = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in L}
tab = None
for x in L:
    if x.mnemonic == "mov" and "*4 + 0x" in x.op_str and x.op_str.startswith(("ecx", "eax", "edx", "r8d", "r9d")):
        tab = BASE + int(x.op_str.split("*4 + ")[1].rstrip("]"), 16); break
entries = [BASE + struct.unpack_from("<I", d, off(tab) + 4 * k)[0] for k in range(0x64)] if tab else []
dflt = [k for k, e in enumerate(entries) if e == 0x25E60A]
check("B1 the interpreter's table sends exactly the six to the default handler 0025E60A; pre-decode at 0x47",
      sorted(dflt) == sorted(SIX) and T.get(0x25E5A9) == "cmp r12b, 0x47" and T.get(0x25E5AD) == "jb 0x25e5c2",
      "table %s; default entries %s" % ("%08X" % tab if tab else None, ["0x%02X" % k for k in dflt]))
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
seen = set(); files = scripts = anomalies = 0; ops = collections.Counter(); where = collections.defaultdict(list)
operand_bytes = collections.Counter()
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes(); h = hashlib.md5(b).digest()
    if h in seen: continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    files += 1
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1; code = sec[start:end]; i = 0
        while i < len(code):
            op = code[i]
            if op > 0x63: anomalies += 1; break
            ops[op] += 1
            if op in SIX and len(where[op]) < 5: where[op].append("%s+%X" % (p.name, 0x80 + start + i))
            if op >= 0x48:
                for k in (1, 2):
                    if i + k < len(code) and code[i + k] in SIX: operand_bytes[code[i + k]] += 1
            i += 3 if op >= 0x48 else 1
print("   distinct .ebp %d, with a code section %d, scripts %d, decode anomalies %d, instructions %d"
      % (len(seen), files, scripts, anomalies, sum(ops.values())))
for k, v in SIX.items(): print("   0x%02X %-14s at an opcode position %7d; inside a u16 operand %9d" % (k, v, ops[k], operand_bytes[k]))
check("B3 none of the six occurs at an opcode position in any shipped script; control: the same six byte values occur "
      "inside operands, so the zero is about position, not about the bytes",
      all(ops[k] == 0 for k in SIX) and all(operand_bytes[k] > 0 for k in SIX),
      str({"0x%02X" % k: ops[k] for k in SIX}))
check("B2 controls: every script decodes to its end, and CALL / PUSHI / RET are present",
      files > 500 and anomalies == 0 and ops[0x58] > 0 and ops[0x4E] > 0 and ops[0x2D] > 0,
      "CALL %d PUSHI %d RET %d" % (ops[0x58], ops[0x4E], ops[0x2D]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
