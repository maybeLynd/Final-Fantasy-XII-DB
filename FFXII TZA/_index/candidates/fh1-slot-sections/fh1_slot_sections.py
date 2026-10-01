"""FH-1: the ActorManagerSlot's section pointers - which EBP section each holds, who sets and clears it (OPUS, 2026-09-27).

  S1 the eight slot setters. Each is a 5-instruction stub `movsxd rax, ecx / imul rcx, rax, 0x288 / lea rax, [rip ->
     02098E10 + F] / mov [rcx + rax], rdx / ret`, so it stores its second argument at slot field F. The census finds
     every such stub over the slot array and its callers.
  S2 the section handlers that call them. 003304A0, the section installer, dispatches directory slots; the handler
     for section N stores the section at 022C6xxx[m] and calls its setter (ebp2-container table):
       sec 2 00330190 -> 0026C880 -> +0xA0    sec 3 00330220 -> 0026C8A0 -> +0xA8    sec 6 00330060 -> 0026C860 -> +0xB0
       sec 8 0032FA10 -> 0026CE00 -> +0xD8    sec 9 0032FAC0 -> 0026CE20 -> +0xE0    sec 10 00331610 -> 0026D3A0 -> +0xF0
       sec 11 003316B0 -> 0026D3C0 -> +0xF8   sec 12 0032FB70 -> 0026CE40 -> +0x100
  S3 lifetime: ActorManager_BindLoadedDefinitionPayload 0026C8C0 zeroes +0xA0 +0xA8 +0xB0 +0xB8 (0026CC49-0026CC5E)
     and +0xE0 +0xF8 (0026CBFC, 0026CC10) with rbx zero; ActorResource_ResetManagerLoadState 0032ED80 calls the
     setters for sections 8-12 with rdx = 0 (0032EFCE / 0032F016 / 0032F06A / 0032F0B2 / 0032F0FA) but never the
     section 2 / 3 / 6 setters - it clears only their global mirrors 022C6CA0 / 022C6CC8 / 022C6CF0.
  S4 the +0xB0 readers include the three gauge-label verbs 0x1BC / 0x1BD / 0x1BE (00352A50 / 00352EC0 / 003534F0),
     each reaching a 7-byte stub `mov rcx, [rcx + 0xb0] / jmp` into 00408640 / 00408700 / 00408960.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]


def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
funcs = []
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = line.split("\t")
    try:
        funcs.append((int(c[0], 16), int(c[2])))
    except (ValueError, IndexError):
        continue
bodies = {e: list(cs.disasm(d[off(e):off(e) + sz], e)) for e, sz in funcs if 0 < sz <= 0x20000 and off(e) is not None}
fails = 0


def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)


setters = {}
for e, b in bodies.items():
    if len(b) >= 5 and b[0].mnemonic == "movsxd" and b[1].mnemonic == "imul" and b[1].op_str.endswith("0x288") \
            and b[2].mnemonic == "lea" and b[3].mnemonic == "mov" and b[3].op_str == "qword ptr [rcx + rax], rdx" and b[4].mnemonic == "ret":
        t = b[2].address + b[2].size + b[2].operands[1].value.mem.disp
        if 0x02098E10 <= t < 0x02098E10 + 0x288:
            setters[e] = t - 0x02098E10


def callers(t):
    return sorted(e for e, b in bodies.items() for i in b
                  if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == t)


want = {0x0026C880: (0xA0, 0x00330190), 0x0026C8A0: (0xA8, 0x00330220), 0x0026C860: (0xB0, 0x00330060),
        0x0026CE00: (0xD8, 0x0032FA10), 0x0026CE20: (0xE0, 0x0032FAC0), 0x0026D3A0: (0xF0, 0x00331610),
        0x0026D3C0: (0xF8, 0x003316B0), 0x0026CE40: (0x100, 0x0032FB70)}
got = {s: setters.get(s) for s in want}
check("S1 the eight qword setters and their slot fields", all(got[s] == want[s][0] for s in want),
      " ".join("%08X->+0x%X" % (s, got[s] or 0) for s in want))
cl = {s: callers(s) for s in want}
check("S2 each setter's section handler (plus the teardown for sections 8-12)",
      all(want[s][1] in cl[s] and set(cl[s]) <= {want[s][1], 0x0032ED80} for s in want)
      and all((0x0032ED80 in cl[s]) == (want[s][0] >= 0xD8) for s in want))
bind = "\n".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in bodies[0x0026C8C0])
check("S3a the bind zeroes +0xA0 +0xA8 +0xB0 +0xB8 +0xE0 +0xF8 from rbx = 0",
      all(("mov qword ptr [rdi + %s], rbx" % h) in bind for h in ("0xa0", "0xa8", "0xb0", "0xb8", "0xe0", "0xf8"))
      and "0026C905 xor ebx, ebx" in bind)
td = bodies[0x0032ED80]
calls0 = []
for k, i in enumerate(td):
    if i.mnemonic == "call" and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in want:
        zero = any(p.mnemonic == "xor" and p.op_str == "edx, edx" for p in td[max(0, k - 4):k])
        calls0.append((i.operands[0].imm, zero))
tds = "\n".join("%s %s" % (i.mnemonic, i.op_str) for i in td)
check("S3b the teardown clears sections 8-12's slot fields with rdx = 0 and only the GLOBAL mirror of 2 / 3 / 6",
      sorted(c for c, z in calls0 if z) == sorted([0x0026CE00, 0x0026CE20, 0x0026CE40, 0x0026D3A0, 0x0026D3C0])
      and all(("mov qword ptr [r14 + rdi*8 + %s], rbp" % g) in tds for g in ("0x21a6ca0", "0x21a6cc8", "0x21a6cf0")))
stub = {}
for f, tgt, verb in ((0x003E8F50, 0x00408640, 0x00352A50), (0x003E8FC0, 0x00408700, 0x00352EC0), (0x003E9000, 0x00408960, 0x003534F0)):
    b = bodies[f]
    stub[f] = (b[0].op_str == "rcx, qword ptr [rcx + 0xb0]" and b[1].mnemonic == "jmp" and b[1].operands[0].imm == tgt
               and any(i.mnemonic == "jmp" and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == f for i in bodies[verb]))
check("S4 the three gauge-label verbs read +0xB0 through their stubs", all(stub.values()))
print("FAILS", fails)
sys.exit(1 if fails else 0)
